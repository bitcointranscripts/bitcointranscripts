---
title: The P2P network
transcript_by: varmur via review.btctranscripts.com
media: https://podcasters.spotify.com/pod/show/chaincode/episodes/Pieter-Wuille--Amiti-Uttarwar-and-the-P2P-network---Episode-16-e19bgv7
tags:
  - erlay
  - p2p
speakers:
  - Pieter Wuille
  - Amiti Uttarwar
summary: P2P experts Amiti Uttarwar and Pieter Wuille discuss various aspects of peer-to-peer communication in Bitcoin, with Adam Jonas facilitating the conversation. They delve into the challenges and objectives of address relay, highlighting its complexities and the importance of propagating IP addresses to maintain network connectivity and prevent partitioning and eclipse attacks. The discussion covers the design and evolution of AddrMan, introduced in 2012 to manage IP addresses, and the impact of changes like rate-limiting address gossip to mitigate spam. Pieter and Amiti also touch on the significance of maintaining separate network stacks for different network protocols and the potential of employing ASMAP to improve network resilience. The conversation underscores ongoing efforts and future directions for enhancing Bitcoin's P2P network.
episode: 16
date: 2021-10-26
additional_resources:
  - title: FIBRE Episode with Matt Corallo
    url: https://podcast.chaincode.com/2020/03/12/matt-corallo-6.html
  - title: 'PR #787'
    url: https://github.com/bitcoin/bitcoin/pull/787
  - title: Eclipse Attack paper
    url: https://eprint.iacr.org/2015/263.pdf
  - title: Sybil attack
    url: https://en.wikipedia.org/wiki/Sybil_attack
  - title: Addrman and eclipse attacks wiki page
    url: https://github.com/bitcoin-core/bitcoin-devwiki/wiki/Addrman-and-eclipse-attacks
  - title: 'Anchors connections - PR #17428'
    url: https://github.com/bitcoin/bitcoin/pull/17428
  - title: Connection exhaustion issue
    url: https://github.com/bitcoin-core/bitcoin-devwiki/wiki/Addrman-and-eclipse-attacks#open-questions-and-areas-for-research
  - title: paper
    url: https://arxiv.org/abs/1905.10518
  - title: BIP
    url: https://github.com/naumenkogs/bips/blob/bip_0330_updates/bip-0330.mediawiki
  - title: 'Limiting addr black holes - PR #21528'
    url: https://github.com/bitcoin/bitcoin/pull/21528
  - title: Rate limiting on address gossip in 22.0
    url: https://github.com/bitcoin/bitcoin/pull/22387
  - title: Leaky bucket rate limiter
    url: https://en.wikipedia.org/wiki/Leaky_bucket
  - title: Estimating the Node Degree of Public Peers and Detecting Sybil Peers Based on Address Messages in the Bitcoin P2P Network
    url: https://arxiv.org/abs/2108.00815
  - title: Coinscope paper
    url: https://www.cs.umd.edu/projects/coinscope/coinscope.pdf
  - title: TxProbe
    url: https://arxiv.org/abs/1812.00942
  - title: ASMAP
    url: https://blog.bitmex.com/call-to-action-testing-and-improving-asmap/
aliases:
  - /chaincode-labs/chaincode-podcast/the-p2p-network-2/
---
## Introduction

Caralie: 00:00:05

Hi everyone.
Welcome to the Chaincode Podcast.
This is Caralie, and it's been a while.
Hi Jonas.

Adam Jonas: 00:00:10

Hey Caralie.
Welcome back.

Caralie: 00:00:11

Thank you.
It's nice to be here.
Tell me more about this episode we've got.

Adam Jonas: 00:00:16

This episode was designed for two P2P experts, Amiti and Pieter, to sit down and talk about all things P2P.

Caralie: 00:00:24

That sounds very exciting.

Adam Jonas: 00:00:25

It was very exciting.
I was supposed to be a fly on the wall, but then I asked a lot of questions and so...

Caralie: 00:00:30

Yeah, fly on the wall is not your strong suit.

Adam Jonas: 00:00:32

It is not.
I enjoyed it quite a bit.
I was happy to be here, and I think you'll enjoy listening to it.

Caralie: 00:00:37

Well, great.
Looking forward to it.

Adam Jonas: 00:00:44

So, Pieter, this is your first episode as actually part of the Chaincode team.
So welcome to Chaincode.
It's been a while in the making.

Pieter Wuille: 00:00:52

Yeah, thanks.
It's great to finally actually be here.

Adam Jonas: 00:00:57

I agree.
So luckily we still have Amiti in the office.
Maybe we can start where we left off our episode with you, Amiti.
For those that are just joining us and haven't listened to that episode, you should go listen to it.
But let's start with `AddrMan` and `AddrRelay`, take it from there.

## AddrRelay high-level goals and constraints

Amiti Uttarwar: 00:01:13

Cool.
I talked a little bit about `AddrRelay` as a concept and how IP addresses are important for nodes to learn about.
Pieter, do you have any initial thoughts of what are the high-level goals and constraints of address relay?

Pieter Wuille: 00:01:32

Yeah, that's a hard and I guess good question.
I think address relay is a really not well-defined problem, because we're still figuring out what its exact goals should be.
It's not like transactions or blocks, where we have this fairly strict requirement that every node eventually learns about all of them.
So clearly, there's some desire for IP addresses to propagate well on the network, for some metric of 'well,' but maybe that doesn't mean everyone needs to hear about everything all the time, because that's clearly an unscalable problem. If the number of nodes goes up and they all broadcast their existence on the network at a fixed frequency, eventually all the bandwidth will be eaten up by such messages.

So that's a difficulty but at the same time, as I said, it's maybe not a strict requirement that everyone hears about everything.
So ultimately, the reason why IP addresses are rumored to have a network that's connected, that's resistant to partitioning: that is, partitioning being the unintentional splitting of the network, and I guess eclipse attacks being the term for when it's an attacker driven attempt to break someone's connectivity with the network.
Both of those, but just in general, it's both a hard problem and a not very well defined goal.

Amiti Uttarwar: 00:03:14

Yeah, definitely agree with that.
I think even the premise of whether or not addresses should be able to propagate to all nodes on the network is something that established P2P contributors don't agree on.

Pieter Wuille: 00:03:31

Yeah and you have to see it in context.
Maybe at the current size of network and activity of nodes, that's a reasonable thing to do, but it wouldn't be if the network grows a hundred times in size.
So maybe the goal can be up to a certain level of activity that's reached, but after that maybe not anymore.

Amiti Uttarwar: 00:03:53

To play devil's advocate a little bit, don't we expect all transactions and blocks to be propagated to all nodes on the network regardless of how it scales?

Pieter Wuille: 00:04:03

Yes.
This is definitely true for blocks.
If a node cannot hear about a block, it is dysfunctional.
Fortunately for blocks, it is easy.
Blocks are incredibly expensive to create, so there is no spam problem for blocks.
For transactions we have something similar, it's a bit more complicated and fuzzy, but at least in Bitcoin Core the mempool policy has this this notion called marginal fee rate, which is the minimum fee rate we expect transactions to pay, and the reasoning is that whenever we relay a transaction on the network, its cost is accounted for somewhere.

### Marginal fee rate

Pieter Wuille: 00:04:49

So either we assume it will eventually confirm and pay for itself, or it is maybe evicting some other transaction and it is paying for that evicted transaction in addition to its own.
So with that kind of reasoning you essentially set a cost in terms of Bitcoin value on the propagation for a transaction across the network.
But something like this is not possible for IP addresses.
At the same time, there's no way of... what is a valid IP address?
I can rumor anything.
Is it valid when you can connect to it?
Is it valid when it is an honest node?
There's no such...

Amiti Uttarwar: 00:05:38

Even if you can connect to it once, doesn't mean it will stay online.

## Should we consider different transport layers?

Adam Jonas: 00:05:42

Should there be different transport layers for these different messages that are being sent around?
Obviously, going back to Amiti's design goals, the reliability, the timeliness, the privacy, these are different levers that could be pulled for these different messages that could be passed around.

Pieter Wuille: 00:05:58

This is, I think, an easier question if you're talking about blocks and transactions, because for example, initial block download has purely bandwidth constraint, you don't even care about partition resistance.
Like okay a node can't get up, fine it'll find some other solution in the worst case, while block relay at the tip, there the problem occurs, because now you want it fast, you want it reliable, you want it resistant to partition attacks and so forth.

But transactions, the timeliness isn't there to the same extent anymore.
But, say, due to the design of compact blocks, so this is [BIP 152](https://github.com/bitcoin/bips/blob/master/bip-0152.mediawiki), is a mechanism where when a block is announced, it is sent to supporting nodes only with short hashes for the transactions, and since it can be assumed that the receiver node will have most of those already, this is at least a giant bandwidth gain, but in many cases a very significant latency gain too, because most blocks propagate on the network with no round trips at all.
The receiver has all of them.
But that critically relies on the receiver having those transactions in the first place.
So that puts some moderate timeliness constraints on transactions, too.

## FIBRE Episode with Matt Corallo

Adam Jonas: 00:07:37

To harken back to some of Matt's thoughts on this, obviously [FIBRE was this experiment](https://podcast.chaincode.com/2020/03/12/matt-corallo-6) of even changing to UDP and being able to take advantage of not having bandwidth constraints.
So separating those things out seems to make some sense.

Pieter Wuille: 00:07:54

I don't know if it really needs to be completely separated out, but we are somewhat going into that direction by having block-only connections now, and maybe more variety on those things will appear where some connections don't fulfill all of them because they're in conflict, right?
If you have a high bandwidth transaction stream, it's not really a problem these days, but maybe for super low connectivity things...  the bandwidth of the transaction is in conflict with the timeliness of blocks and maybe this is easier to solve with separate connections.
I think it's just good to think about these things as having very different goals.
To get back to address relay, there timeliness is not a concern at all.
Even reliability is probably fine if an IP address just gets to 99% of nodes rather than 100%.

Amiti Uttarwar: 00:08:53

Yeah, that makes sense.

## The introduction of `AddrMan` in 2012, PR #787

Adam Jonas: 00:08:55

Let's go back to 2012.
`AddrMan` v1 was when you introduced it in [PR #787](https://github.com/bitcoin/bitcoin/pull/787), if you're keeping track at home.
So maybe before we start getting into the design of `AddrMan` and what that was like, I actually don't really understand what there was before `AddrMan`.
There was this `addr.dat` file, but can you explain what it actually was doing?

Pieter Wuille: 00:09:20

So it was just a set of addresses and it basically stored all IP addresses that we received from other nodes.
There were some tests on it, but it had lots of problems.
Like, it was unbounded as far as I can tell.
I'd need to check to make sure, but it was effectively trivial to just spam a node with IP addresses and both its memory usage and its disk usage would blow up.

Adam Jonas: 00:09:49

And do you recall that being just a known problem that you were going after?

Pieter Wuille: 00:09:55

At the time, DoS resistance was not a thing.
You can find multiple quotes by Satoshi where he says the software is not very DoS resistant.
It is a hard problem, right?
I really don't remember all the thinking and reasoning that led to `AddrMan`.
Unfortunately, if you go look at what is available in terms of logs, times were different.
PR was open, someone said I tested it, it works, and it was merged.

Adam Jonas: 00:10:31

Seemed to be an upgrade though, and it held up pretty well.

Pieter Wuille: 00:10:35

Pretty well.
It was very ad hoc, there was not much research that went into it.
It wasn't that we went over the design goals or whatever.
Yeah there's a few that you can just derive by looking at the pull request at a time, like it's finite in size.
That is a big constraint, and it's an obvious one, because we just don't want things to grow unboundedly.
From that, if it's finite in size, you need limits and you need a replacement strategy.

So what `AddrMan` did was make a distinction between IP addresses that we know work, and addresses we have just heard about, because they're pretty fundamentally different in terms of our confidence in them.
You also want both in that there's this notion of trust on first use, which is like your SSH client tells you you're connecting to a server with these fingerprints, I haven't seen it before, and you say yep that's a good thing and it doesn't tell you again.
So you don't want to always make completely random connections, because under the assumption that not every IP address is an attacker, if you constantly hop, your probability of eventually hitting an attacker is virtually 100% and not doing that gives you...
You may still be connecting to an attacker, but in that case you have a problem anyway.
So you want some connections to be drawn from the set of peers, and I really don't like to say trust because the level of trust we place in these is extremely low, but there has to be some assumption of not every node in the network is an attacker.
If it were, we have a problem.
So we can just reasonably assume that that's not the case, and if that's not the case, well, you probably want to use the connections you've used before.

Adam Jonas: 00:12:47

Right, some combination of having some memory and then also adding diversity.

Pieter Wuille: 00:12:53

Right, because you want a network to learn.
If a new node joins, over time it should get connections, so the network should learn, and I think this is where this balance from completely separating tried and new entries, and dealing with them separately comes from.
Then within each, there is this idea of bucketing them based on where the information comes from.
The idea there is that a single source, where a source would be defined as not just a single IP address but a range of IP addresses that are presumably geographically or administratively close to each other, only have access to a certain part of the database.
Every source IP range is mapped to a subset of the table, and the things it rumors can only enter those places in the table.
The idea there is we need this replacement strategy and how do you prevent a malicious spammer who is trying to poison your database?
How do you prevent, or to the extent possible, minimize its impact?
That's where that came from, and all the rest I think is just some made up numbers.
What's a reasonable memory usage?
How many table entries should there be?
There's this magical constant of never revealing more than 23% of the table, I have no idea where it comes from (laughter).

Amiti Uttarwar: 00:14:30

So just some context for listeners, this is by and large still the fundamental tools that we currently use to store addresses in Bitcoin Core right now.
So far it seems to be holding up.
Really well.

Pieter Wuille: 00:14:46

It's evolved a bit over time, right?

Amiti Uttarwar: 00:14:49

Definitely.

## Eclipse Attack paper

Pieter Wuille: 00:14:49

In 2015, there was a [paper published by Ethan Heilman](https://eprint.iacr.org/2015/263.pdf) and others on eclipse attacks, which I think was the first academic look at this kind of problem, because I think before that we had talked about it as a Sybil attack, this problem of having lots of bad peers, but I think it was recognized that a Sybil attack is really something different, because I think the history there is that Sybil is the name of a character in a book...

Amiti Uttarwar: 00:15:27

Oh, interesting.

Pieter Wuille: 00:15:28

It's like a multiple personality disorder story, and a [Sybil attack](https://en.wikipedia.org/wiki/Sybil_attack) is something that appears where you have a number of trusted peers, and you trust them to be all distinct parties, but if there's someone who is really controlling multiple of these, they can do a confidence attack on you, where you think, oh, most of my peers think this, but it's really just one party.
That is not really a problem in a Bitcoin setting, because fundamentally our hope is to have at least one connection to the honest network, and it doesn't really matter how many bad ones we have as long as there is one honest one.
So really the problem is eclipsing, not so much Sybil-ing.
So eclipsing is an attacker managing to make sure all your peers are malicious.

Adam Jonas: 00:16:27

That's such a remarkable trait though.

Amiti Uttarwar: 00:16:29

It really is.

Adam Jonas: 00:16:30

That everything could go wrong except for one, and you're still okay.

Pieter Wuille: 00:16:34

Yeah.
Of course, this is only true for the blocks and transaction parts, because presumably if an attacker manages to be most of your connections in terms of addresses, this increases their ability to poison you, which over time leads to eclipse attacks.
So all these sorts of problems were analyzed in this paper, and it gave, I think, like seven or eight mitigation strategies for how the situation could be improved.
Over time, all of them have been implemented, I think.
Or maybe there's...

Adam Jonas: 00:17:16

Yeah, there's still a few outstanding, or in progress, but yeah, there's a few that are undeployed or partially deployed.

Amiti Uttarwar: 00:17:25

The vast majority have been implemented, and I think one of the...

Adam Jonas: 00:17:29

It was done very quickly, too.

Amiti Uttarwar: 00:17:30

Oh yeah.

Adam Jonas: 00:17:31

It seemed like your collaboration with Ethan went quite well.
Before the paper came out there was a push, and then over time things got fixed also pretty quickly.

Pieter Wuille: 00:17:44

Yeah, so I think there were two big ones that were done pretty much immediately after the paper came out.
One was making a table bigger, just increasing the number of buckets and the sizes of the buckets.
A couple of years had passed, I guess we were fine with using a bit more memory.
The other one was giving addresses deterministic placement in the buckets.
This reduced the ability of repeatedly trying to insert the same thing in a bucket.
If it only has one place, it goes there or it doesn't.
Then after that there were a few more.
Some of them took several years.
One was feeler connections and retest before evicts policy.

Adam Jonas: 00:18:34

By the way, Pieter's doing all this from memory.
I'm sitting in front of the answers and Pieter's just doing it in perfect order.
It's impressive (laughter).

Amiti Uttarwar: 00:18:41

So I thought it was interesting, the idea of inbound versus outbound peers, and ensuring that just because you're connected to an inbound peer, if you mark them as, hey, this is a good Bitcoin connection, I can use it again in the future, that allows attackers to abuse that to write themselves into the tried table.
That was one.

Pieter Wuille: 00:19:04

Oh yeah, right I had forgotten about that one, that we even did that.
It seems so obvious in retrospect. [(`AddrMan` and eclipse attacks wiki page)](https://github.com/bitcoin-core/bitcoin-devwiki/wiki/Addrman-and-eclipse-attacks)

Adam Jonas: 00:19:11

And then [anchors](https://github.com/bitcoin/bitcoin/pull/17428), which was the most maybe the most recent.

Amiti Uttarwar: 00:19:13

Oh yeah totally, because we used block relay only.
So anchors are connecting to nodes that you already know about when you start up versus selecting more randomly.

Adam Jonas: 00:19:27

So a few others that he suggested, more outgoing connections, which I think, some of that because of the two outbound block relay only connections.

Pieter Wuille: 00:19:37

Block only connections have that, but at the same time those don't relay addresses, so they're not really participating there.

Adam Jonas: 00:19:45

Maybe Erlay will help us move this.

Pieter Wuille: 00:19:46

Yeah, exactly.

## Connection exhaustion issue

Pieter Wuille: 00:19:48

The big issue with outbound connections is, somewhere early on in Bitcoin's history, I don't remember exactly, there was a time when the network ran out of connectable inbound slots.
Every node has a finite number of connections on the inbound side it accepts.
Sum all of those up, that is an upper bound on the number of connections that can be made.
At the time, Bitcoin didn't have any NAT-PMP or mini-UPnP to automatically open firewalls.
Probably a vast majority of nodes were running behind home routers.
This explains the hesitancy that developers have had to increase the number of outbound connections.
In an attack scenario, an easy way to increase your partition resistance is adding more connections.
But it's been years, and this hasn't been a problem for a long time, but it still drives decisions around the number of connections.

## Erlay ([Paper](https://arxiv.org/abs/1905.10518), [BIP](https://github.com/naumenkogs/bips/blob/bip_0330_updates/bip-0330.mediawiki))

Pieter Wuille: 00:20:55

So that's where Erlay really comes in, because Erlay is ultimately a mechanism, without going into too much detail, for increasing the number of connections without increasing bandwidth.
With Erlay deployed, it would be more reasonable for people to increase the number of inbound connections a node can have, or even changing the default about that.
That in turn might make it more reasonable to increase the number of outbound connections.

Adam Jonas: 00:21:31

Given that that's obviously a strong intuition, how do you go about testing that?
How do you go about actually changing that default?

Pieter Wuille: 00:21:39

That's very hard.

Amiti Uttarwar: 00:21:40

Very carefully.

Pieter Wuille: 00:21:43

Doing it gradually is a possibility, and watching metrics, but it's hard because deploying software, especially something like Bitcoin Core, takes a long time.
It has very intentionally no auto upgrade mechanism, or something like that, to avoid software maintainers from having too much power over pushing changes to the network.
From that, so you can't just say, one release increase it a bit, and increase it a bit more.
It takes time.
Given that we haven't seen a shortage in connections for a number of years, and we can reason pretty easily about things like bandwidth usage and CPU usage that more connections bring.
Those things you can just test in isolation, so it's not an entirely uninformed decision.

Adam Jonas: 00:22:43

It seems like, just generally, we can be more sophisticated than the way you described your 2012 design (laughter).
Which, by the way, again, has held up very well.
It's not a slight in any way.
It's just, I wonder whether simulated networks or just simulations in general would give us some more information?

Pieter Wuille: 00:23:05

So for Erlay specifically, Gleb has been doing lots of simulation work to reason about bandwidth usage and so on.

## AddrRelay

Amiti Uttarwar: 00:23:13

Cool, so can I pop us back to address relay and some more of that?
I think in version 22 there were two big changes to address relay.
One was one I introduced about [reducing black holes](https://github.com/bitcoin/bitcoin/pull/21528).
Let's not talk about that, let's talk about the other one...

Pieter Wuille: 00:23:33

Okay, happy to talk about that one too (laughter).

Amiti Uttarwar: 00:23:36

About rate limiting address gossip.
Can you tell us about what the mechanism is?

Pieter Wuille: 00:23:41

There was just an observation we had that the total amount of IP addresses rumored on the network today, like if you start a node and run it for a couple of weeks and just see how many addresses you see from various nodes, it is a really low number.
It's like one every couple of seconds.
I don't remember the exact number.
Then if you compare that with how much we would permit there to be relayed...
So this is the old mechanism I'm describing from earlier releases that had been used since time immemorial, was, I think there was a buffer of the set of addresses we want to relay to every peer.
It was capped at a thousand.
If more things would enter this buffer, it would randomly start overwriting things out of those thousands.
There was a certain rate at which this buffer is flushed, like just every so often, I don't know, 2 minutes or something?
Was it 10 minutes?
Is it an hour?
There is a Poisson timer, or is it every 10 seconds?
I really don't know.

Adam Jonas: 00:24:59

There's going to be some constant in there.

Pieter Wuille: 00:25:02

Like beeeep (laughter), this is where we insert, we look it up and we will insert it.
So every so often we check, hey, for every peer, what's in this set of addresses, we want a rumor and just send it out.
So this puts a natural rate limit on the outbound side of IP relay.
It is at most a thousand addresses every this many seconds on average.
If you compare that number to the amount that was actually being used on the network, it was some enormous factor, like a factor of a 100 more or something.

Amiti Uttarwar: 00:25:46

Yeah, I think it was between like a hundred and thousand x.

Pieter Wuille: 00:25:52

Yeah, something like that.
That's concerning because in a way this means that the presumably mostly honest activity on the network today is using far less than what the network would permit relaying, and that is exploitable.
It's not completely non-trivial, but if someone finds a way to get this buffer full enough, they could have their set of addresses propagated way, way better than others in the network.
Given the fact there effectively is already this funnel effect at the outbound side, it seemed like a fairly easy solution was to apply that at the inbound side as well, and just limit at what rate we process incoming connections.
So we made some statistics, like looking at a bunch of nodes, what kind of activity level do we see, and picked a number based on that. ([Rate limiting on address gossip in 22.0](https://github.com/bitcoin/bitcoin/pull/22387))

### Leaky bucket rate limiter

Pieter Wuille: 00:26:56

So this is a known technique in networking called the [leaky buckets rate limiter](https://en.wikipedia.org/wiki/Leaky_bucket), and the idea is that you have a bucket with tokens, and say every `X` seconds a token is added to this bucket, but the bucket can overflow, it can never go over about a thousand say, and whenever an address is processed it takes a token from the bucket unless there is none.

What this gives you is a mix between a relatively low sustained rate, but at the same time also permitting occasional spikes that go way beyond it, without really changing the long-term average, because ultimately everything is limited by the rate at which these tokens are added to the buckets.
This was necessary because the existing behavior on the network is very spiky due to the way these things are buffered and sent out every so often.
Obviously, the big question with a design like this is: is it exploitable?
Can someone overload you?

The answer is yes, I think.
This does indeed mean that someone spamming you is going to be able to indirectly reduce the propagation.
Because this is on the inbound side, this is one step removed, but if I'm going to spam you, Jonas, then honest IP address being relayed by me to you, you'll try to send out both to someone else, but together it's too much, so my spam is effectively reducing her honest traffic.

Adam Jonas: 00:28:45

The noise drowns out the signal.

Pieter Wuille: 00:28:46

Yes, but you do it on the inbound side, which is better than doing it at the outbound side, because then it would be you directly already having it.
At the same time, this problem already exists, because there is already this rate limiting that is unintentional and not really designed as a rate limit, but the set of a thousand with random replacement strategy effectively allows the same thing already, just at a much higher threshold.

## Address Spam

Amiti Uttarwar: 00:29:18

On the topic of address spam, I think we saw some really interesting address spam when this PR was up.

Pieter Wuille: 00:29:25

Yeah, I don't know what happened there, but there was this report all of a sudden of lots of apparently random IP addresses being relayed on the network just a couple of days after this pull request came up.
So I guess it was in time.
As far as I know, it was not related in any way.
We don't know because I don't think anyone figured out who exactly was doing it.

Amiti Uttarwar: 00:29:53

No one's stepped forward and so... it was me (laughs).
So the behavior that was observed was there would be nodes that would spin up and connect to public peers and send packets of 500 `addr` messages with 10 addresses each, and this 10 number is magical in Bitcoin Core because above that and you won't forward those addresses, so that gives the merging effect from different peers that you were mentioning before, but then the nodes would just disconnect.

There were a few properties of the addresses that were observed.
One was that the time associated with the message was perfectly placed, I think, nine minutes in the future, because if it's too far in the future, we won't propagate addresses anymore, and similarly if it's too far in the past.
So by putting it as far in the future as possible, that ensures that you have the largest window of time that nodes will continue trying to propagate these addresses.

### Estimating the Node Degree of Public Peers and Detecting Sybil Peers Based on Address Messages in the Bitcoin P2P Network by Matthias Grundmann

Pieter Wuille: 00:31:02

Yeah, and there was a [paper](https://arxiv.org/abs/2108.00815) written about this.
A researcher called Matthias Grundmann wrote a paper on this behavior and formulated a theory about what it was doing, pointing out this nine minute in the future aspect too, and hypothesizing that this is to ensure the longest possible time these addresses propagate on the network, and there was an attempt to map the network.

Adam Jonas: 00:31:31

This is inferring topologies.

Pieter Wuille: 00:31:34

Yes exactly.

Adam Jonas: 00:31:34

We don't know, but that was one of the theories.

Amiti Uttarwar: 00:31:34

That was one of the suspected biggest reasons that you would do it, and essentially be able to say, how many peers is this public node connected to?

Pieter Wuille: 00:31:46

Right, trying to count the connectivity of nodes.

### Coinscope paper

Adam Jonas: 00:31:46

How is that different than the [Coinscope paper](https://www.cs.umd.edu/projects/coinscope/coinscope.pdf)?
Coinscope is the long-lived connections and using timestamps, inferring topology through how those are propagated because they're unique.
You can connect to a peer from another angle and be able to reconcile that data to see whether they were propagated.

### TxProbe

Pieter Wuille: 00:32:07

Yeah, there have been other techniques like [TxProbe](https://arxiv.org/abs/1812.00942) where you send conflicting transactions and see how those propagate to infer who is connected to who?

Amiti Uttarwar: 00:32:17

Honestly, I think the amount of information you can get is kind of... it's getting harder.
So in this, I think the main thing you could extract was how many peers each of these public nodes are connected to.

Pieter Wuille: 00:32:29

It's not who.

Amiti Uttarwar: 00:32:30

Yeah, the previous ones were identifying techniques for _who_ nodes are connected to.

Pieter Wuille: 00:32:36

Yeah.
In TxProbe, you literally connect to two nodes and you want to know, are these connected to each other?

Adam Jonas: 00:32:44

That makes sense, yeah.

Pieter Wuille: 00:32:45

So it's different aspects of, different projections of topology data you get out.
I think we have to live with the fact that you can't make it completely impossible to prevent that information from being revealed.
There are people whose opinion is that this information should just be public so it can be used...

Amiti Uttarwar: 00:33:10

The information of node topology?

Pieter Wuille: 00:33:12

Yeah.

Amiti Uttarwar: 00:33:13

Oh, interesting.

Pieter Wuille: 00:33:14

I think there have been papers that argued for making node topology public, because that makes it available for research.

Amiti Uttarwar: 00:33:23

Oh, okay.
But wouldn't that also make the network easier to attack?

Pieter Wuille: 00:33:27

_Yes_ (laughter).

Adam Jonas: 00:33:28

You have to raise new defenses.

Pieter Wuille: 00:33:30

To be clear, what's a concern here is if topology is known, that helps a potential partitioning attacker figure out where to focus their efforts, right?
If you assume it is possible for this information, if we think that all these techniques for inferring topology are...

Amiti Uttarwar: 00:33:54

...sufficiently able to retrieve that...

Pieter Wuille: 00:33:57

...then maybe that is indeed the right decision to just make it not hard, but I don't think that's the case.
I think that there's always going to be some signal there, but there are lots of possibilities for improving.

Adam Jonas: 00:34:11

Yeah, can't there be some combination of how Lightning does it in terms of your public connectivity and then your private connectivity?
The private connectivity at least gives you a little bit of, again, all you need is one honest, you just have one honest connection.

Pieter Wuille: 00:34:28

I can't really compare Lightning nodes because...

Adam Jonas: 00:34:32

I don't want to compare it.
I'm saying the concept of having a public versus a private, and the idea of... there's different kinds of trust when you're talking about public versus private.
But you introduce a little bit of reputation when you're talking about public, and private maybe those are longer lasting connections and it's up to you as to who you're trusting.

Pieter Wuille: 00:34:50

The problem with any kind of reputation is that there has to be something at stake that you lose when you behave badly.
In Lightning Nodes, nodes have an identity and have connections with money that is at stake.
In Bitcoin nodes don't have an identity intentionally, because we want to hide the topology, but also there can't be an identity that... you don't want something like a Proof-of-Stake before you can run a node.
So that makes it very hard to say what is an honest node.

Adam Jonas: 00:35:30

I guess another way that is different is the ephemeral nature of these connections, and if you watch a node and see the disconnection and connection, and when I was a new user and seeing that that was happening often was a little surprising.
It's like, wait, I don't maintain these relationships any longer than is actually occurring, it felt counterintuitive.

Amiti Uttarwar: 00:35:53

Yeah, and in fact we have mechanisms to very carefully have potential for rotation, such as every so often, I think five or 10 minutes, we connect to an additional block relay only.
If that node provides us a block that we didn't know about, then we will prioritize it...

Pieter Wuille: 00:36:15

...and make it replace an old connection, yeah.

Amiti Uttarwar: 00:36:16

Yeah.
So in the logs, that shows a bunch of disconnecting and connecting, even if that might not actually change your long-lasting peers.
Similarly we have one for when we haven't gotten a block in a long time, that might be normal, or you might be eclipsed so as this last ditch effort you make a full relay connection to an additional node and say...

Pieter Wuille: 00:36:43

...a fabled ninth one...

Amiti Uttarwar: 00:36:45

...which is also short-lived.

Adam Jonas: 00:36:47

Any closing thoughts before we...

Amiti Uttarwar: 00:36:50

I'm very glad we got to cover all of P2P...

Adam Jonas: 00:36:52

... all of it... (laughter)
We now understand everything.

Amiti Uttarwar: 00:36:55

Every little detail (laughs).

Adam Jonas: 00:36:58

It's complex, but you know, we have our best people working on it.
It'll be fine.

Pieter Wuille: 00:37:06

There's lots of work still to be done there.

Adam Jonas: 00:37:09

If you had more time, Pieter, what would you like to work on?
What's something that you would like to address?

## Separate network stack

Pieter Wuille: 00:37:14

For example, what we were talking about just before, topology, one possibility is, for example, run a completely separate `AddrMan` or even going further, a completely separate network stack for every public IP you have.
Like say, run on Tor simultaneously with IPv4 and IPv6, just give them their own completely independent network stack.
That is not a complete solution because you're still not going to give them each their own mempool for resource reasons, probably.
So that's probably still some leakage between them, but things like that would, I think, help a lot.
It's just a one thought.
There are so many things.

Amiti Uttarwar: 00:38:01

That was actually what popped up in my mind, is top of wish list as well.
I think we have so many different fingerprint attacks of identifying this node through different networks, which is actually also that paper on the address spam was hypothesizing that that was an additional piece of information you could get, because each one of those addresses had unique attributes to it.
So if you send it over an IPv4 address and then you see it on a IPv6, or what would be worse is on these privacy networks that you're trying to keep private for some reason.
So I think the fingerprint attacks are a whole class that are pretty hard to attack individually, but if we're able to separate the components and just have different network managers for different networks, then it would really diminish the surface area of that potential.

## ASMAP

Pieter Wuille: 00:38:58

I think another thing that would be nice to see more work on is [asmap](https://blog.bitmex.com/call-to-action-testing-and-improving-asmap/).
Since a couple of releases, Bitcoin Core has had functionality of loading a database telling it which IP ranges are controlled by the same network operators, like ISPs and similar level things.
But this needs infrastructure, like where do you get that database?
What's the supply chain for providing users with that, which is as much a technical problem as it is logistical and trust question one.
So that's something I'd like to work on.

Adam Jonas: 00:39:43

You couldn't imagine that being hard-coded or distributed from the same way that the bootstrapping is done and the IP addresses?

Pieter Wuille: 00:39:52

Yeah, the problem with that is that it is transient.
This information changes constantly, but it is available.
You can find these databases from various sources, they gather them.
But the problem is it is constantly changing, so it's not like you can have a verification procedure about it, where you do it as part of your deterministic build, and people will repeat it and get the same thing out.
So that probably implies we need tools to say diff two databases and see that there's some value judgment there like, hey, there's suddenly this change here, is this is this expected or not?
So I think a lot about it is just giving transparency in what is it and the ability to change it.
But I would hope that a mechanism can be found with sufficient eyes that it can indeed be just shipped as part of the Bitcoin Core distribution and at least you have a default.

Adam Jonas: 00:40:53

Well, thank you both for making such a glorious return to the studio.

Amiti Uttarwar: 00:40:57

Thank you.

Pieter Wuille: 00:40:58

Thanks for having us.

## Wrap-Up

Caralie: 00:41:04

Well, that was great.

Adam Jonas: 00:41:02

You're never gonna leave disappointed with Pieter around.
So that was fun.

Caralie: 00:41:07

Yeah, and a treat to have Amiti here as well.
What more could you really ask for when it comes to talking about P2P?

Adam Jonas: 00:41:12

You can't.
You can't ask for anything more, Caralie.

Caralie: 00:41:14

Well, glad we got that straightened out.
Thanks everyone for listening.

Adam Jonas: 00:41:18

Hopefully we will be seeing you soon.
