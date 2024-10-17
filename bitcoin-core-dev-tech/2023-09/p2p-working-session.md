---
title: P2P working session
tags:
  - bitcoin-core
  - p2p
date: 2023-09-19
---
## Erlay

- Gleb is active and ready to move forward - [#21515](https://github.com/bitcoin/bitcoin/pull/21515)
- Are there people generally interested in review?
  - I wanted first to convince myself that this is useful. I couldn't [reproduce](https://github.com/vasild/bitcoin/wiki/Erlay) the numbers from the paper - 5% was what I got with ~100 connections. My node is listening on a non-standard port. It may be that I don't have a normal sample. There is a [pull request](https://github.com/bitcoin/bitcoin/pull/27534) that could add RPC stats to bitcoind - that might get better numbers. Current stats are per peer and we lose those stats once the peer disconnects.
  - How much of INV traffic is redundant? Erlay claims to reduce the redundancy.
  - I looked into this as well. 8-12 erlay peers. 10-20% was what I recall. The numbers and call for feedback is on Gleb's repo.
  - 86 of 95MB are INVs on my node.
- how much does this interact with package relay?
  - sketches are a replacement for INVs. Good to think about the interaction - Gloria was under the impression that they don't interact much.
- Should there be an issue rather than the meta PR?
- Numbers should be verified

## ASMAP (Fabian)

- Workshop at TabConf - there was a bug in the RKPI verification that meant it was not fully reproducible. We can either dockerify it within the tool and then it was cross platform or should I just build it for linux?
- Who do you expect to run this? The plan isn't clear to me.
  - Whoever wants to. I would say devs who verify releases and power users.
- Are there multiple software packages that are needed?
  - It's the tool that I am providing. It looks at the certs.
- It makes it harder to make it consistent. It would be easier to run it against this data to compare against.
  - I can talk to the maintainer but it's not really their use case.
  - It may be worth trying.
  - also talked with Sjors about this. Docker then becomes a dependency. Another thing, when I put together this workshop - I'd like a clear distinction between the encoding and decoding code and data collection. I'd like to put the encoding/decoding tools into Bitcoin Core.
- How tightly the ASMAP code is tied to the bitcoin core project?
  - it is a necessity for us to use the ASMAP code
  - we already have some of the code in bitcoin core in python already.
  - sounds reasonable to me
- What problem is ASMAP solving?
  - replacing the bucketing logic of IPs (/16s) by autonomous systems
  - easier for attackers to get in the outbound rotation, slash 16 IPV4 with a few exceptions. ASMAP in general is being able to customize that. The data is uses autonomous systems and with bottleneck analysis where we can make improvements. Inbound evictions, addrman bucket, and 10 connections uses IPs
  - I took all addresses from my addrman, chose 10 random ones with different /16 prefix and checked in how many distinct ASs they belong and it was 8 or 9, always more than 6 autonomous systems.
  - is this worth spending time on. An attacker that only has access to Google cloud or AWS, how easy would it be to do?
  - you should run it when a different /16 with an empty addrman. You already have data and if you take out that restriction.
  - this will influence on the connections of the network (as it grows). ASs are one approximation for control. How good we don't know, but better than slash 16s. AWS probably has double digits AS numbers and thousands of IP ranges.
  - botnets have different looking IPs in many different ranges. Scattered.
  - If you could do a botnet and the network grew and then an attacker could position themselves to get more connections (Virtu presentation described effects of scaled up network with constant shares between ASs)
  - In the case of 100x scale-up, random selection might be better than ASMap selection if [virtu's research](https://cryptic.to/advancing-bitcoin-2023/) is a correct. /16s make no difference.
- AWS has multiple AS numbers, this softens the effect virtu described
- we could choose to merge all of AWS into a virtual AS. The question is where do we get the data from. I don't know where the place to have this sort of discussion apart from here. Does it belong on an issue or the mailing list?
- before it is included in a release, it makes sense to post it on the mailing list.

## Broadcasting out all txs through Tor (Vasil)

- The idea is to change how we broadcast local transactions from the wallet or RPC - right now we broadcast to all peers, which makes it easy to correlate txs to IP addresses.
- Only broadcast to Tor peers if possible. Send to someone random and disconnect. If I only tell Tor peers add a safety net to tell if it is propagated and if not broadcast to all.
- Can see the timing and where txs originate from.
- The trickling mechanism adds randomness and doesn't obscure things from an attacker that sees everything
- Inspired by [Linking Lion](https://b10c.me/observations/05-inbound-connection-flooder-down/)
- If we send it to a few peers over Tor and some of them are spies, they have a privileged position to see. If they come to our mempool and ask and they can confirm if it is yours. Then if some asks and then we pretend we don't have it.
  - you are changing the behavior of what we allow in the mempool.
  - If some sends an INV or sends GETDATA - parent and child issues also complicate things. Convinced I can hide it.
- Now I'm leaning the other way, which is to broadcast without putting it in the mempool. Need to store it on disk too before it as been received by the network, so that it does not get lost if the the node restarts. In the mempool there are unbroadcasted txs. The code is already there. If it doesn't come back, you need to store it safely for retry later.
- There are two cases to think about. It comes from your wallet or it's from RPC. What happens if the RPC comes from the wallet?
- `sendrawtransaction` would put in your mempool. Subject to trickling mechanism will go in the ToBeINVed.
  - What about announcing to some of your peers, wait to see it echoed back and then send to all if it does not come back.
  - How bitcoin core worked until 0.5
  - It's not trivial I think. Need to act differently for that Txs than Txs coming from elsewhere which may also be a tell. And also need a more aggressive broadcast mechanism until it is echoed back.
  - we don't want to send it to everyone. Then we send through Tor, then you could skip all the rest and then you destroy the assumption of the attacker.
  - if you fluff it, then someone can assume that you are the source wallet. Even if none of the behavior changes, it destroys the assumption reliability. It lowers the confidence level.
  - chainalysis can't see where it originates
- if you have a time-sensitive protocol, that might be an issue
- after 20 min try the same
  - 20 min seems enormous. Should only be a few mins. An attacker watching all the connections. If you only send it to 1 then they can't do the timing connection. It would be nice as a stretch goal, to obscure that the mechanism is being used.
  - In addition to Tor peers, send to clearnet connections through Tor. In I2P, use transient source addresses.
- can you coin flip this, by coinflip
- if you do it twice then they can tell it is yours
- what do you think about sending out once immediately and after a short delay (seconds) do it again.
- This happens now because we have only 2 threads for the connection manager. So it is going to take some time. Should I broadcast it to 5 unconditionally or 1, then another one and then another one and stop as soon as the transaction is echoed back.
- do we broadcast after we see it?
  - we broadcast like we've never seen it before.
  - a goal is to treat our transactions like others. By keeping it out of the mempool, that goal is achieved.
  - so we will keep it out of the mempool
- Then we can think about wallet interaction
  - Not going to see 0 balance, but now we will see the same balance.
  - can't do this by default until we have the wallet interaction in place. And we deal with the case that someone makes a dependent tx because then we use the privacy advantages. The correct solution is a new state in the wallet for transactions that can't be spent.
- start with the RPC
  - when you send it over RPC, the RPC will return immediately and then start sending the transaction to the network. When the RPC returns, it does not mean that the transaction is seen by the network.
  - could do wait to broadcast or something like that.
  - new RPC, would not overload `sendrawtransaction`. Can call it an experimental API and then roll it in or include in `sendrawtransaction`. Don't return the RPC as a string but as a JSON object. Everything should be an object.

## Increase block-relay only inbound connections (Amiti/Martin)

- Introduced as two block-only connections, always with the idea we wanted a bigger number
  - Having more connections that isn't a resource drain
  - Have had other work, like `addrRelay`, network stuff to prep for this
    - You cannot know whether you will send inbound connections but it also doesn't matter because validation is cheap. It's the sending of Txs are expensive.
    - What is important is predicting whether or not the peer wants to you to send TXs
  - Increasing the number of default outbound block-only conns, we propose 8 block-only connections
  - Needs to increase the number of inbound slots available. Not just increase the number, but add additional slots that would only be used for inbound block-only traffic. (130-140 slots)
  - Main open question is about the ratio
- If you don't offer the bloomfilter, you know it's blockrelay or another implementation
  - We send this flag to our peers, but if we are in blocks only mode and if we send rawtx and we can still txs to our peers unless they have already sent
- There is no way to say, I'm not sending your transactions
  - The relay flag in the version message.
  - If I send the set the `fRelay` flag false, I cannot deduce will they ever send me a tx doesn't seem possible
  - You may guess that a connection is treated a block relay only connection and then you start treating it as a full one
- For inbound peers we need to do inbound eviction. This takes place right after the conn takes place. We treat every conn as a tx connect. When we get a version message we can know for sure based on the flags.
- If I know that we aren't going to send a tx, we don't care if everyone is going to give us conns we need to know whether we are sending txs, that the expensive part. If bloomfilters are disabled we know for sure. (and they will know after the version message). The reason we are OK for block-relay only conns. Is it necessary to have two separate classes. Could you have an system where tx is 4 points and 1 point of block relay and we cut it off after X points. We could be mispredicting the resource costs. We may want to push up the resources now and then it will naturally shift
  - There are traffic costs (most important consideration, cpu costs and memory costs - if someone limits their conns because of memory, it may mean a different limit for different profiles.)
- How do we come up with those limits or parameters?
  - Maybe we can raise the number from 125 to something else. The change does two things. Increases the resource costs for a node and it raises the number of block-only connections.
  - Should quantify that by measuring memory costs of block-only peers
  - On outbound it's easier, unless there is a 4MB block, we won't send such a thing. How much memory do you save in the worst and average case?

## Bug fixes and CVE disclosure (Fanquake)

- How are we disclosing bugs after end of life?
- Who would write them up?
  - it shows we care about it.
- Disclosing the bugs also gives a reason to upgrade.
- The openSSL project, they have a classification of the level of bug
- The highest level that it fixes is this level (doesn't disclose which one)

## Junk addr spikes across the network (0xB10C)

- Seeing addr spikes across the network. And they are junk addr. There is no node actually there. I cannot connect to the port.
- What is the length of the spike?
  - 20 or so min
- Could be one actor
- are these only coming from inbound?
  - this has been going on since march and still going on.
- We were seeing huge amounts of the 10 min in the future. Guarantees the longest time to relay. They were randomly generating addresses. There is a paper written by KIT guess about this attack. Introduced at the same time at the rate limiting patch - might be related. The PR was opened but it wasn't merged yet.
- this doesn't actually cause any problems?
  - correct

## Additional servers available (0xB10C)

- I have p2p monitoring. I also have access to 6 servers from DCI and we can use this as passive monitoring nodes to extract stats. Like for orphan handling for example. They are just on AWS. We can collect on these.
- Are you using a custom version of core?
- It runs tracepoints and but otherwise is master. Release candidate or run a PR is also necessary.

## Functional tests for 324 and need reviews (Ruhi)

- We send stuff to bitcoind and we can examine the responses, they have different in the test framework to test downgrading.
- Test the prefix as well
- What are some other things we should test?
  - testing manual connections vs. connections made through addr
  - the general solution to that problem is warnet. That is a harness that has different IPs and random slash 16s. There are interactions between BIP324 and deciding
  - what we can't do add address to addrman and it connects automatically
  - to a large extent, these two types of connections remain the same. We actually later forget how we made the connection. We can't test for preferential peers which on purpose doesn't exist.
- need to distinguish the two types of tests. The majority just spin up bitcoinds and use RPCs and test that everything is good
- How about testing previous versions?
- We have tests between v1 and v2 nodes. We have some infra for testing old versions I'm not familiar with. There shouldn't be a difference (hahaha). There are things that are specifically useful from bitcoind. Decoy messages is the big one. There are a few other things - protocol deviations that are allowed but aren't implemented on the sender side like non-empty garbage authenticator packets. In p2p v2 handshake, then garbage, then garbage auth packet, want both node decide on what the garbage is - normal packet structure commits to the garbage. It has contents too that says ignore it so you could send data in there and it should be ignored. The garbage auth packet has a header byte and even if the decoy flag is set it still ignores it. That shouldn't change anything. We should call it the decoy bit rather than the ignore bit. There is a good reason for it.
- The version message too, the sender should send nothing b/c that means no extensions. All those things are in the units test but they are limited. They are very flexible but they are annoying to write.
- Created another class called p2p encrypted state and if you support v2 and you do the handshake functions using that class. A function that was added before the handshake happens. Is there a better way to do that?
- I will have a look at the code. Within a python framework but we can do things simpler.
- We have unit, fuzz and functional tests that compare the session ID.

## Warnet (Josibake)

- Why not just use regtest or signet?
- We can create network topologies using graphml
- There is a bunch of tooling that exists where you could create topologies or you can create your own
- What is generated is a graphml file then you pass that graphml file into warnet and warnet turns it it into a docker compose file
- The edges are the peer to peer connections
- Docker composes turns these into images and starts the network and runs a script that adds all the add edges.
- addr bucketing will actually work. Nodes will start gossiping. Can turn that off and don't want the nodes to make more connections. We have a DNS seeder as well.
- You start with a topology and then nodes act as normal
- Those could be on multiple machines. We should just run it on kubernetes. It's only 1 subnet.
- We have a Tor test network and allows us to have our own tor authority within it.
- Stuck with docker because warnet should be abstracted from the hardware running on it. The only restriction should be cost.
- Graphml that has it running on docker compose.
- Zipkin took the test framework class, self.nodes is a list of docker containers. Can copy open existing tests. These are called scenarios.
- Scenario in a loop: a mining scenario. Or could also execute once and shut down.
- Transaction scenarios that bring the network to life and then you could run your scenarios on top of that.
- Network set up is deterministic and the scenario is deterministic.
- Log aggregation needs the most work and needs the most input:
- Prometheus: we are running a graphana service, prometheus service and fork monitor.
- Ideally we have all the logs aggregated somewhere. Needs
- A p2p monitor would be something I'd like to put in there.
- Have a dashboard where you can see what is happening.
- WarnetCLI can going into a specific container or run RPC command
- be able to track how a message went from one place to another
- Could be a tx tracker that travels from node to node
- How many can you run on a laptop?
- we could do 0-50 nodes on your laptop or you want to do something that is long running figure out where else to put it
- I've put up 500 on a dev box
- Could also attract academics and give them some tooling to test a PR. Even testing an attack. Could deploy that.
- there should be a place we should be testing this long term - private closed group of people. Have this up and running and drop 500k txs and then wait a couple of days.
- can't we just do this on signet?
- lack of determinism, and it's public. This is meant to be insane, pathological environment.
- Are you talking about the public signet or spinning up your own signet?
- next steps - erlay testing and measuring bandwidth seems like a good scenario to test
- could also show the blend of the erlay vs. random nodes. Better tool for collaborating on these bigger updates. Can model progressive upgrades like mempool full-RBF or BIP-324.
- Goal from the front end is to be able to deploy it from the front end
- Warcli network start
- Docker does not let us run different subnets but because bucketing happens on the /16 level the addresses do get bucketed randomly.
- Could use own ASMap - could assign different IPs to an AS
- The scenarios: subclasses the bitcoin test framework. Can run multiple scenarios at the same time and they shouldn't interfere with each other.
- we have the ability to make a Pynode - can make a python node and you don't need to have wallets and other stuff
- INV flooding - what happens to the node?
- Anything you can get into a Docker container, we can run. Would like to collect all these and maintain them for people to use in the future.
- can you change the topology dynamically
- can run individual RPC commands on nodes and can look at the messages between commands. Can also get the war debug log.
- could add Shadow for a backend if we want determinism of a scenario
