---
title: Socratic Seminar - AssumeUTXO
transcript_by: Michael Folkson
tags:
  - assumeutxo
  - utreexo
speakers:
  - James O'Beirne
  - Calvin Kim
  - Tadge Dryja
date: 2021-11-02
media: https://www.youtube.com/watch?v=JottwT-kEdg
---
Reading list: <https://gist.github.com/michaelfolkson/f46a7085af59b2e7b9a79047155c3993>

## Intros

Michael Folkson (MF): This is a discussion on AssumeUTXO. We are lucky to have James O’Beirne on the call. There is a reading list that I will share in a second with a bunch of links going right from concept, some of the podcasts James has done, a couple of presentations James has done. And then towards the end hopefully we will get pretty technical and in the weeds of some of the current, past and future PRs. Let’s do intros.

James O’Beirne (JOB): Thanks Michael for putting this together and for having me. It is nice to be able to participate in meetings like this. My name is James O’Beirne. I have been working on Bitcoin Core on and off for about 6 years. Spent some time at Chaincode Labs and continue to work full time on Bitcoin Core today. Excited to talk about AssumeUTXO and to answer any questions anybody has. The project has been going on for maybe 2 and a half years now which is a lot longer than I’d anticipated. Always happy to talk about it so thanks for the opportunity.

## Why do we validate the whole blockchain from genesis?

<https://btctranscripts.com/andreas-antonopoulos/2018-10-23-andreas-antonopoulos-initial-blockchain-download/>

MF: We generally start with basics, some people who are beginners will get lost later. I am going to pick on some volunteers to discuss some of the basics. The first question is what is initial block download? Why do we do it? Why do we bother validating the whole blockchain from genesis?

Openoms (O): The whole point is to build the current UTXO set so we can see what coins are available to be spent currently and which have been spent before. We do it by validating all the blocks, downloading all the blocks from the genesis block, from the beginning. Going through which coins have been spent and ending up with the current chain tip which will end up building the current UTXO set. We can know what has been spent before and what is available now.

JOB: At a very high level if you think of the state of Bitcoin as being a ledger you want to validate for yourself without taking anything for granted the current state of the ledger. The way you would do that is by replaying every single transaction that has ever happened to create the current state of the ledger and verifying for yourself that each transaction is valid. That is essentially what the initial block download is.

MF: We are replaying absolutely everything from genesis, all the rule changes, all the transactions, all the blocks and eventually we get to that current blockchain tip.

## How long does the initial block download take?

<https://blog.bitmex.com/bitcoins-initial-block-download/>

<https://blog.lopp.net/bitcoin-full-validation-sync-performance/>

<https://blog.lopp.net/2020-bitcoin-node-performance-tests/>

MF: This does take a very long time to do. There are a few posts from BitMEX and Jameson Lopp on how long this takes. Although there have been improvements in recent years it still can take hours or days depending on your machine and your hardware. Any experience from the people on the call on how long this takes? Has anyone done a IBD recently?

O: A couple of hours on high end hardware with a I7 processor and a decent amount of RAM. On a Raspberry Pi with 4GB of RAM and a SSD it is between 2 and 3 days.

Stephan (S): I was using Raspiblitz and it took me like 5 days with a SSD. Similar magnitude.

O: It depends a lot on the peers you end up downloading from. For example if you have a full node on your local network and you add it as a peer then it can be quite quick in that sense. Also if you are downloading through Tor that can slow down things a lot.

## Assumedvalid and checkpoints

<https://bitcoincore.org/en/2017/03/08/release-0.14.0/#assumed-valid-blocks>

MF: So obviously from a convenience perspective spending hours or days in this state where you can’t do anything isn’t ideal. From a convenience perspective a better thing to do would be to try to shorten that time. An obvious thing to do would be to just download blocks or validate blocks from a certain point in time rather than from genesis. The first attempt at either bringing this time down or at least providing some assurance to users that they are not spending hours or days verifying the wrong blockchain was assumed valid. Is anyone on the call aware of assumed valid other than James?

Fabian Jahr (FJ): Assumed valid is a point in the blockchain, a certain block height and/or block hash, from which point it is assumed that this is not going to be re-orged out. These are hardcoded in the Bitcoin Core codebase. This feature, this is before I got active in Bitcoin Core, I don’t know what the conversation around it was exactly, it is not really used anymore. There are no new assumed valid points introduced regularly into the codebase. But I am not 100 percent sure what the discussion was around that, what the latest status is, what are people’s opinions on that.

MF: I just highlighted what I’ve got on the shared screen, it was introduced in 0.3.2 so very early. The intention was more to prevent denial of service attacks during IBD rather than shortening the time of IBD. Presumably at 0.3.2 the time of IBD wasn’t anywhere near as long as it is now. James can correct me, it did at that point or later, it skipped validating signatures up until that assumed valid block?

JOB: Yes. It looks like when it was introduced it was called checkpoints which ended up being a pretty controversial change. A checkpoint dictates what the valid chain is. That is subtly different from what assumed valid does today which is just say “If you are connecting blocks on this chain and you are connecting a block that is beneath the block designated by the assumed valid hash then you don’t have to check the signature”. It is not ruling out other chains which is what checkpoints do. The idea was to prevent denial of service attacks. Maybe someone sends you a really long chain of headers but that chain of headers has really low difficulty associated with it. Checkpointing is a different thing than assumed valid. As you said assumed valid really just skips the signature checks for each transaction below a certain block as an optimization. It doesn’t rule out another longer valid chain from coming along. For example if someone had been secretly mining a much longer chain than we have on mainnet with some unknown hash rate that is much greater than the hash rate we’ve been using, they could still come along and re-org out the whole chain hypothetically. Based on use of assumed valid whereas checkpoints don’t allow that. Checkpoints are a little bit controversial because they hardcode validity in the source code whereas assumed valid is just an optimization. It is worth noting that with assumed valid we are obviously still checking a lot about the block. We are checking the structure of the block, we are checking that the transactions all hash to the Merkle root and the Merkle root is in the block header and the block headers connect. You are still validating quite a bit about the block, you are just not doing the cryptographic signature checks that the community has done over and over again.

S: To be clear assumed valid is still being used today, it is just the checkpoints that are deprecated?

JOB: Yes. Assumed valid is used by default. It is the default configuration. Typically every release the assumed valid value is bumped to a recent block as of the time of the code. That typically happens every release. Calvin (Kim) is saying that checkpoints are still used. They are probably just really low height and could probably be removed. Assumed valid is still very much maintained. It is the default setting. If you want to opt out of it and do a full signature check for the entire chain you can do that by passing the value `0` for an assumed valid configuration.

Calvin Kim (CK): Just a point on removing the old checkpoints. Technically that is a hard fork.

JOB: Yeah, exactly. It would broaden the consensus rules, it would allow blocks that were previously invalid to be valid. You are right about that Calvin.

MF: With the existing checkpoints it is technically impossible to validate a chain which has different checkpoints to those checkpoints say in Core or another Bitcoin implementation. It is impossible.

JOB: Yes.

MF: Obviously these are unlikely scenarios but let’s say you were validating a chain that didn’t meet an assumed valid, it didn’t agree or match the assumed valid. What is the user experience then? Is it just flagged to the user? Is there a log that says the assumed valid in the code doesn’t match the chain that you are validating? Or is it based on proof of work? What’s the user experience if that assumed valid isn’t matched with your experience of validating the chain?

JOB: It is still possible. If we were considering a chain that was more work than the chain that we know now that violated the hardcoded assumed valid default, that would indicate a re-org of thousands and thousands of blocks. It would probably be catastrophic at a higher level. I think the most that you would get as a user is maybe a log statement. I don’t even know if we have a log statement for that case. If something is on a chain that isn’t assumed valid you just do the signature validation. It is not any kind of special behavior.

S: The difference in performance would be that you skip signature validation until the previous assumed valid? There is only one valid hash in the binary? It is not like you can go back to the previous valid hash? It is all or nothing? If there is a re-org with a couple of thousand blocks the user would have to validate all signatures since the genesis block and not use the assumed valid hash of the previous Core release?

JOB: That sounds right. I am not sure offhand, I’d have to check the code.

S: There is only a single hash in the code right? Whereas checkpoints you have one every I don’t know 50,000 blocks. But for assumed valid it is only a single hash.

CK: That hash is backed by minimum chain work. There are some checks to make sure you are on the right chain.

JOB: Yeah minimum chain work is definitely another relevant setting here. That prevents someone from sending a really long chain of headers that may be longer in a strict count than mainnet but is lower work.

MF: This is relevant in an AssumeUTXO context because the concept is that you are going to validate only a fraction of the chain and then potentially do transactions. Pay or receive having only done a fraction of the initial block download. The rest of it from genesis would be happening in the background but you are already functional, you are already up and running, you are already potentially doing transactions, paying and receiving.

JOB: That’s the sketch of AssumeUTXO. With assumedvalid you are still downloading all the blocks. You have all the data onhand. AssumeUTXO allows you to take a serialized snapshot of the UTXO set, deserialize that, load that in from a certain height. In the same way as with assumedvalid we expect that by the time the code is distributed there are going to be hundreds if not thousands of blocks on top of the assumedvalid value, the same would go for AssumeUTXO. We would expect that the initial block download that you have to is truncated but it is not completely eliminated. You are still downloading a few thousand blocks on top of that snapshot. In the background we then start a full initial block download.

## The AssumeUTXO concept

Bitcoin Optech topics page: <https://bitcoinops.org/en/topics/assumeutxo/>

MF: Let’s go over the concept of AssumeUTXO. I’ve got the Optech topics page up. We are bootstrapping new full nodes, we are reducing this initial blockchain download time by only doing a fraction of it before we are able to send and receive transactions, before we are up and running. During IBD you can still play around with your node. You can still make RPC calls and do CLI commands etc. But you can’t do anything with the wallet until you’ve fully completed IBD, is that right?

JOB: That’s right.

MF: One thing it says in Optech is “embedded in the code of the node would be a hash of the set of all spendable bitcoins”. Is that correct? Are there alternatives to embedding it in the code of Core? I think you’ve talked before James about getting this UTXO snapshot out of band and then using a RPC command to start the process. Then it wouldn’t necessarily be in the code of Core or the implementation you are using?

JOB: The value that’s important to hardcode is the hash. If you take the UTXO set, the collection of unspent coins, you order them somehow, and then you hash them up. You get a single value like you might get at the root of a Merkle tree or something. Hardcoding that is important. It is more important to hardcode that and not allow it to be specified through the command line say in the same way as assumedvalid. If you can allow an attacker to give you a crafted value of that hash and then give you a bad snapshot then they can really mislead you about the current state of the UTXO set before you’ve finished back validating. We decided in the early stages of designing this proposal that that value should be hardcoded in the source code and shouldn’t be user specifiable. Unless you are recompiling the source code in which case anybody can tell you to make any change and potentially cause loss of funds that way. To your question once you have the UTXO set hash hardcoded you have to actually obtain the file of the UTXO set itself which is serialized out. That is going to be on the order of 4 gigabytes (correction) or so depending on how big the UTXO set is of course. In the early days of the proposal there was a phase 1 and phase 2. Phase 1 just added a RPC command that allowed you to activate a UTXO snapshot that you had obtained somehow, whether that’s through HTTP or torrent or Tor or whatever. The idea there is it really doesn’t matter how you obtain it because if you are doing a hash based on the content of the file anyway the channel that you get it through doesn’t have to be secure. When you download a copy of Bitcoin Core you don’t necessarily care about the HTTPS part if you are checking the binary hash validates against what you expect. It is the same idea here. Phase 2 is going to be building in some kind of distribution mechanism to the peer-to-peer network. In my opinion Phase 2 is looking less and less likely just because it would be a lot of work to do. It requires the use of something called erasure coding to ensure we can split up UTXO snapshots so no one is burdened with storing too much. It would be a really big job. In my opinion it doesn’t matter how you get the snapshot. There are lots of good protocols for doing decentralized distribution of this kind of stuff via torrents say. I think it is less likely there will be a bundled way of getting the snapshot within Core although that is certainly not out of the question.

MF: These are the two phases you’ve discussed in other forums, podcasts and presentations. You said Phase 1 was allowing snapshot use via RPC with no distribution. This would be getting the snapshot from potentially anywhere, a friend, a torrent, whatever. Phase 2 which you say is unlikely now is building the distribution into the peer-to-peer layer. I was thinking that sounds very difficult. Then you have questions over how many nodes are supplying it and whether you can get a hold of it. Core and other implementations have to decide how recent a snapshot they need to provide which gets hairy right?

JOB: Absolutely.

S: Is the problem that you are making it very difficult for novice users to use AssumeUTXO? They have to go and find those binaries themselves in addition to making sure they get the right version of Bitcoin Core? If it is not bundled they are probably not going to do it or they are going to rely on third parties like Umbrel or Raspiblitz to bundle it for them. If you push towards that model you are relying on those third parties.

JOB: I think you are totally right, there is a convenience trade-off there. It is unfortunate that it is not easier for us to make this a seamless experience. My hope I guess is that eventually once the RPC commands are merged we can work on a GUI change that will allow someone to drag and drop the serialized UTXO set into the GUI or something. Maybe also link to a torrent for the snapshot from [bitcoincore.org](https://bitcoincore.org/) where you get the binary. It could say “If you want to expedite the IBD then do this”. You are totally right that it does complicate things for the end user. I thought that these changes were fairly simple for Phase 1 and I thought they would be integrated within a year and a half or so. It is now two and a half years later. We are maybe 60-70 percent done with Phase 1. I am very pessimistic about the pace of doing what I think is a much more complicated change in terms of the distribution stuff.

FJ: The types of users that really want this, the question is who really wants to get started within a hour or so of plugging the node in? There is a big overlap of the people who really want that and the people who get a Raspiblitz or Umbrel or whatever comes next that is really plug and play. This feature matches really well with that user base. Making it available for other people who are on the self sovereign side and do more by themselves, that would be great for them as well. But where I see the biggest leverage and adoption, Raspiblitz people are asking for it all the time. BTCPay Server built their own type of feature that was hacky and not completely trustless. There is a very good overlap of people that are going to use this and from this crowd.

O: There is a use case for example for the [Specter wallet](https://github.com/cryptoadvance/specter-desktop). Some people would want to use a self validating wallet connected to Bitcoin Core and get started as soon as possible. They have a similar solution to what BTCPay Server uses but even more trusted. The website is [prunednode.today](https://prunednode.today/). You can download a signed version of a pruned snapshot from a node of Stepan Snigirev. Get started with a pruned node so you don’t even need to have the storage available for the whole blockchain. There is another alternative that LND uses already on mobile by default, the Breez wallet for example, which is Neutrino (BIP 157/158). Also the Wasabi wallet on desktop uses this. You only download the block hashes as needed and not more than that. It is more like a light wallet function rather than a fully validating one.

JOB: Yeah that’s a good point. In the early days of this proposal we were actually debating whether it would be easier to just integrate a more SPV or light client like behavior into Bitcoin Core instead of a proposal like this. It turned out that for a variety of reasons this seemed preferable. One, it seemed like less of an implementation burden because to build in SPV behavior to the node in a first class way would be a big change. Secondly I think the validation model here is quite a bit better than SPV. With a full view of the UTXO set you can do first class validation for recent blocks at the tip, better assurance.

O: There is no risk of having information withheld from you like with Neutrino. That’s the worry there, you are getting blocks which are not containing the transaction you are after.

JOB: Exactly.

## Security model of AssumeUTXO

MF: We are kind of on the security model now. We won’t spend too much time on this but we should cover it. Presumably this has slowed progress on it. There are different perspectives. There is a perspective that perhaps you shouldn’t make any transactions, send or receive, until you’ve done a full initial block download. I’m assuming some people think that. Then you’ve got people in the middle that are kind of like “It is ok if the snapshot is really, really deep”, like years deep. Others will say months deep, some would say weeks. Are concerns over security slowing progress on this or have slowed progress up until this point?

JOB: I think at the beginning there were some misconceptions about security. There was really only one developer that had consistent misconceptions about security. That was Luke Dashjr. I think he is now in favor of the proposal. There are a few important aspects here. Number one, as someone mentioned earlier, there are a variety of approaches now with PGP signed data directories that people are passing around that I think are very subpar. I think everybody who is doing that has good intentions but it is the kind of thing where if one person’s PGP key gets compromised or one hosting provider gets compromised then you have the possibility of some really bad behavior. Number two, initial block download is a process that is linear with the growth of the chain. If the growth of the chain is going to continue indefinitely that’s an infinite process. At some point this needs to be truncated to something that is not infinite which AssumeUTXO does. I think that needs to happen at some point and I think this is the most conservative implementation of that. The third thing, this is an opt-in feature. Unlike assumedvalid which is a default setting you have to proactively use this. At least at this point given this implementation users aren’t nudged into doing AssumeUTXO in the same way as they are with assumedvalid. I think that’s an important consideration. Maybe one day this will be some kind of default but there is a lot more that would go into that before that’s the case. It is important to think about what kind of risks this introduces over assumedvalid. One of the main differences between assumedvalid and AssumeUTXO, in assumedvalid you still have the block, you still have the structure of the block and you are validating that the Merkle root hashes check out. Whereas with AssumeUTXO all you have are the results of that computation, the UTXO set. The way you would attack AssumeUTXO is to both give someone a malicious UTXO set hash that they are going to put in their source code and then to give them a maliciously constructed UTXO snapshot. Right now if you give them a maliciously constructed UTXO snapshot its contents will be hashed and the hash won’t validate against the hardcoded hash in the source code. The thinking there was that if someone can modify your source code arbitrarily, if someone can insert a bad AssumeUTXO hash into your source code there are all kinds of easier ways to cause loss of funds or steal your Bitcoin. If you assume someone can get to your source code and recompile your binary then you are already cooked anyway so it doesn’t really matter. Aside from that there really aren’t any practical differences in the security model between assumedvalid and AssumeUTXO. I am curious if anybody else has thinking on that.

MF: In a model where Core was putting a snapshot into the codebase that was thousands of blocks deep, months or years worth of blocks deep, as you say the only concern there is someone having control over the binary in its entirety in which case they can do anything. I am thinking about this scenario where people are passing around snapshots between friends. Perhaps someone uploads a snapshot that is way too recent. How is Core or another codebase going to stop people from using snapshots that are way too recent? Let’s say 6 blocks ago or 3 blocks ago, how do you stop them from doing that?

JOB: If someone say generates a snapshot that is 3 blocks old what would happen is they’d give that snapshot to someone else. If you were using an unmodified version of Bitcoin Core you would attempt to load that snapshot, we would hash the contents of the snapshot and we wouldn’t be able to find an entry in the AssumeUTXO data structure in the source code to validate against that. We would reject it as invalid. You can think about it like a whitelist of snapshots that are allowed per the code.

O: Transacting with an unsynced node there is a big difference between sending and receiving. If you can send and the network accepts it and especially if the receiver receives it then you don’t need to verify that anymore. The question is when you are receiving something and you want confirmation. That would need the new blocks fed to you as well which is a much more complicated question.

JOB: That’s a great point. There is an asymmetry there.

O: You wouldn’t be able to verify without reaching the chain tip, fully sychronizing. You might be able to construct a transaction without doing that and then broadcast it.

JOB: Yes.

MF: So this is sounding less controversial than I thought it was initially.

Ross Clelland (RC): Are there concerns where the snapshot is being taken when a Lightning channel is opened? It is subsequently closed but you’ve given that snapshot to someone, they think the channel is still open so they could use that. Or would Lightning itself prevent that money from being sent?

JOB: I think that’s equivalent to the simple payment example where someone gives you a snapshot, you load in the snapshot. Until you’ve gotten to the network tip, the most recent block that everyone has seen, you can’t make assertions about what is spent and what is unspent. I think they are analogous.

MF: I’m wavering on this now. I came into this thinking you would definitely want the user to complete that initial block download from genesis. As you say this is conservatively designed in that you do actually complete the full IBD, it is just you do the from genesis part after you are up and running. This argument of whether you should actually do that IBD from genesis and what’s the point of that seems like a question.

JOB: It is a question. I agree that the value of doing the background IBD is debatable. From my perspective as the person proposing this and doing the implementation I wanted to make it as appealing and as conservative as I could so I didn’t strip that out. But there are certainly other engineers who thought that it was necessary. If you were willing to accept the UTXO security model for a few days or a few weeks… In assumedvalid we don’t in the background validate all the signatures after we are done syncing. The analog for AssumeUTXO wouldn’t be to do background validation. I figured I’d rather people default into doing the initial block download at some point and having the block data on hand, being able to serve it to their peers if necessary, than not. But I think you raise a good question that frankly still could be debated and at some point could change.

MF: There would definitely be people that oppose that.

O: AssumeUTXO, would it be able to start in a pruned node and not need to download the full chain then?

JOB: AssumeUTXO is compatible with pruning. You still have to retain enough data to be able to arrive at the UTXO set that you started the snapshot from. It basically for most intents and purposes doesn’t change pruning.

O: The big benefit of having a validated chain or having a full chain, validated or not, is if you want to be able to use an already used wallet with some transaction history. You should have the blocks which are containing those transactions at hand so you rescan and be able to reproduce the history of a used wallet. A pruned node is all fine until you need to rescan. Then you would need to start from the beginning most of the time unless you didn’t prune long enough.

JOB: Exactly. Even with that one interesting line of thinking is to use the compact block filters and to index those compact block filters. If you need to rescan, use the filters, decide which blocks you are interested in and go out and retrieve those from the network as necessary. That’s an unrelated question.

O: There is an implementation of a similar idea called [btc-rpc-proxy](https://github.com/Kixunil/btc-rpc-proxy). That is outside Bitcoin Core but it is a service that simulates a full chain to the software calling the Bitcoin RPC interface. It sits behind Bitcoin Core and the Bitcoin RPC basically. You still have a pruned node but there is a request getting to a block which is not on the chain anymore because it is pruned. It requests it like with the block filters and serves it to the requester software. To that software it looks like it is an unpruned node but in reality it is not. There is this full node company called Embassy who are running on a SD card by default and they use a pruned chain. They also develop and use this btc-rpc-proxy which allows them to not need 300 GB of storage, they just need a SD card with the OS and the pruned node. This is something in between the block filters and the pruned, full node trade-off.

MF: I’m guessing the strongest argument for still doing IBD from genesis is what you said James, in principle ideally we want everyone to be able to fetch and validate the whole chain. And so if we relaxed and become less conservative, don’t do that by default, release that conservatism, then perhaps those blocks and transactions from the first few years of Bitcoin are just impossible to retrieve.

JOB: Right. Someone early in the proposal made the argument, in theory everybody is incentivized just to run a pruned node. Why would you keep the extra storage around? I don’t think they are quite comparable. Running a pruned node doesn’t make the IBD go faster. Pretty much everyone wants IBD to go faster. If it was easy enough almost everybody would want to do AssumeUTXO, it gives you an operable node much more quickly. In that case you would then have the default of not having the blocks. In practice it may be the case that many more people don’t have the full chain history on disk. I think you are right.

MF: There would be disagreement I think on relaxing that conservative default. I’m sure some people would oppose that. Is there anything else on the security model of AssumeUTXO?

S: James you mentioned if you already trust the developers and the Core binaries to be secure, trusting the AssumeUTXO hash wouldn’t introduce extra vulnerabilities. Isn’t that a dangerous path because we know the different parts of the codebase have different levels of scrutiny? Some code is reviewed much more in depth than maybe some test PR. The implications of a malicious AssumeUTXO has is pretty big. It is a magic number that would get updated every Core release? Or maybe in 5 years time people won’t be surprised if they see a new hash and it won’t get reviewed as much. The impact this can have is huge. If this was ever changed maliciously it would have huge implications on the reliability and trust of the ecosystem. Whereas if the assumedvalid hash is wrong it is no big deal. People might take longer to do IBD but no money can be stolen. There is no perceived inflation and so on. There is a scale of trust in developers and you don’t want to assume everything is correct all the time.

JOB: This is a really, really good question. It gets to the heart of the design with AssumeUTXO which I feel really optimistic about. In exactly the way you are saying there are certain parts of the codebase that are scrutinized more heavily than others. In my experience working on some of the code that handles the UTXO set it can be very, very difficult to reason about. Even for people who are well versed in C++, even for people who know the Core codebase. What I love about the AssumeUTXO design is that it is very easy for even someone who is semi technical to verify that an AssumeUTXO hash is correct or not correct. As long as they have a full node they can run a script and check that value. Whereas if we try to do optimizations that are slightly more sophisticated or opaque or technically complicated there are very few people capable of actually scrutinizing those changes. It is very hard to read a lot of Core’s code. Not many people these days casually browse the repo with C++ knowledge sufficient to do that. I really like the idea of crystallizing validation into this one value. You are right, it is toxic waste and has to be scrutinized, but it is very readily scrutinized by a wider variety of people than say the CCoin cache is.

S: Independent nodes keeping a full state, that could be checked to make sure the hash is always correct.

JOB: Definitely. You could automatically parse the chain params, the cpp file, extract out the AssumeUTXO values and validate that against your own node pretty trivially. That is a great idea.

MF: I was thinking there would be a warning in the GUI if you say made a payment or received a payment without having completed IBD. I was thinking there would be information to the user “You haven’t completed IBD. Therefore there is a slightly higher risk”. But I’m thinking that is not even necessary. The risk is not zero, there could be some crazy re-org back there but it is basically zero to many decimal places.

JOB: I agree. I don’t know what the user’s action would be subsequently. It is such a vanishingly low probability that there would be some kind of attack there. If you assume that the user got a malicious binary that had a bad AssumeUTXO hash in it they would strip out that warning too.

Thaddeus Dryja (TD): It seems like the only thing you can do is crash. The binary is not self consistent. It is like “Hey this binary has detected a state where the binary itself is assured that it would never happen”. So crash or something.

## How AssumeUTXO interacts with other projects like Utreexo

Utreexo: <https://dci.mit.edu/utreexo>

Utreexo paper: <https://eprint.iacr.org/2019/611.pdf>

Utreexo demo release: <https://medium.com/mit-media-lab-digital-currency-initiative/utreexo-demo-release-0-2-ac40a1223a38>

Faster Blockchain Validation with Utreexo Accumulators: <https://blog.bitmex.com/faster-blockchain-validation-with-utreexo-accumulators/>

MF: The next topic I have up, it is good Tadge and Calvin are here, how this interacts with other projects. From where I’m sitting this lays some foundations for doing more interesting stuff with IBD to reduce IBD time. With AssumeUTXO this is the first step to not having a linear IBD from genesis to tip. This is the first heavy lifting and refactoring of the Core codebase to allow that to happen. One potential next step is Tadge’s and Calvin’s project which is [Utreexo](https://dci.mit.edu/utreexo). You could perhaps, I don’t know the viability of this, have two or multiple fractions of the chain being validated in parallel. Rather than just having the snapshot to the tip and when that’s done the genesis to the snapshot, you could perhaps have genesis to the snapshot being verified at the same time as snapshot to tip. We can go to James first for thoughts on whether this does actually lay foundations for Utreexo and then we’ll go to Tadge and Calvin and anybody else who has more thoughts on that.

JOB: Definitely eager to hear Calvin and Tadge talk about Utreexo. I am really that it seems like a lot of the prerequisite refactoring for AssumeUTXO has already paid some dividends in terms of a project from Carl Dong called [libbitcoinkernel](https://github.com/bitcoin/bitcoin/issues/24303). This is trying to in a really rigorous way separate out the consensus critical data structures and runtime from Bitcoin Core so we can have other implementations safely wrap the consensus stuff, do different implementations of the mempool or peer-to-peer network. Some general background, refactoring in Bitcoin Core is not often kindly looked upon. Having the AssumeUTXO project as justification allowed me to do some fairly fundamental refactoring that would have been hard to justify otherwise. The way that things previously worked was in the codebase there was a global chainstate object that managed a single view of the UTXO set, a single view of the blocks and the headers. What we did in lieu of that is introduce an object called the [ChainstateManager](https://github.com/bitcoin/bitcoin/issues/20049) which abstracts a bunch of operations on the chain and allows us in the particular case of AssumeUTXO to have a background chainstate and a foreground or active chainstate. That is what we do right now. In principle the abstraction of the ChainstateManager allows us to do pretty much anything. We could have any number of particular chainstates running round doing things, being validated and use the ChainstateManager to abstract that. It is a nice feature of the code now to be able to do that.

TD: Calvin has written a bunch of code to do exactly that, running multiple threads at once or even multiple machines at once doing it.

CK: James talked about how you could have a background IBD and a little bit of IBD from the AssumeUTXO set. The Utreexo project represents the UTXO set in a bunch of different Merkle trees. It allows you to represent the UTXO set in a very few hashes. Just the roots of each Merkle tree. This reduces the size of how you could represent things. With AssumeUTXO you have to hash the entire UTXO set, with Utreexo it is Merkle tree-ified. You take these roots and that is what you would validate against. That is essentially your UTXO set. What you could do is represent the UTXO set at a height in less than a kilobyte. That allows a lot of flexibility. Whereas before you had to download these 4GB, now you don’t really have to. It is possible to fit everything into a binary. That almost solves the problem of distributing these 4GB. It introduces a bit of other problems but yeah. The projects that I have been working on, you have a bunch of different threads going and each thread is syncing a different part of the chain. Let’s say you start up 3 threads, one would be syncing 0 to 1000, another would be syncing 1001 to 2000 and the third 2001 to 3000. Once all those are finished you would check against the Utreexo set representation. If you start from genesis and that block 1000, that’s where you were provided the cumulated root. You would compare against it, if they match up great you just saved a bunch of time. You already started verifying from 1000 to 2000. You do this a lot. It allows for more efficient use of your CPU cores. You could go further and say “We don’t even need to do this on a single machine. You could split the IBD into multiple machines.” A really fun thing you could do is have a phone and your laptop do IBD validation at the same time. It doesn’t even have to be continuous. If you have a Raspberry PI going in the background you could be like “I’m sleeping. I don’t need my laptop. I am going to use my laptop to help my Raspberry Pi sync up.” Those are some fun things you could do. Or if you are like “I trust my family. Could you bring your laptop? We’ll do the IBD.”

TD: We have software that does is, testing software, it does seem to give a big speedup. Even on one machine, if you are like “Let me have 8 threads that are all independently doing IBD from different points in the blockchain”. You get a lot better usage of your CPU because you have got so many different things going on. They are small enough that you can throw them around and keep them in CPU cache. You do get a bit of a speedup there.

MF: From a high level perspective this seems like a big change rather than like a refactoring type reorganization change that AssumeUTXO seems to be.

TD: Different peer-to-peer messages, yeah.

MF: I’ve heard Utreexo has a different commitment structure so it can’t use rolling hashes. How much of this is building on AssumeUTXO?

TD: Conceptually there are some similarities. It would be really cool if there was a way to switch between them. Somehow to say “If you have your AssumeUTXO giant UTXO commitment you could turn that into a Utreexo style commitment or vice versa.” It is not super obvious how you do that. In Utreexo it matters the order the things were inserted and deleted because of how the accumulator works. It is not like you can just given the UTXO set generate the commitment state of Utreexo. Maybe someday we can make something like that, that would be really useful, but we don’t have any software right now to say “Take a current node that is synced up. It has got its `chainstate` folder with the LevelDB of the 80 million or whatever UTXOs that exist. That is what the Utreexo accumulator represents. Take all that data and turn it into a Utreexo accumulator.” We can’t right now because the order things were added and deleted changes the accumulator unfortunately. It is not just what is in it. Utreexo does need its own weird messages, you have to send proofs. Whereas in AssumeUTXO nobody is going to know you are using this. Nobody you are connected to sees any difference. Maybe if they are really trying they can be like “He asked for block 700,000 and then a few hours later he asked for block 5. That’s weird.” But even that, you’d have to be connected to the same serving nodes and it would be hard to tell. Whereas something like Utreexo, it is totally different messages. It is very clear. If no one is there to serve you these things you are not going to be able to use it. It is a bigger change in that sense.

JOB: I think the strongest relationship between the two is that the AssumeUTXO work from a Core implementation standpoint paved the way to make it easier to do Utreexo in a sense. Some of the abstractions that it introduced are going to make it a lot easier to error lift in the Utreexo operations. It took probably a year to get in the really foundational refactoring necessary to move away from a single chainstate and a single UTXO set.

TD: The stuff we’ve been working on, some of it dealing with multiple chainstates, but also dealing with not having a database. It is kind of like “Wait, what?”. There is no database. A lot of the software definitely assumes that you’ve got LevelDB there. That is what you are using when you are validating blocks and stuff. A lot of software is like “There are ways to pretend that it is there or make a disposable chainstate every time you validate a block and things like that”. That’s some of the refactoring we’ve been looking at. That is probably going even further than the changes in AssumeUTXO. But definitely using that and changing even more.

JOB: For anybody who is not familiar with Utreexo, Utreexo kind of inverts the validation process. Instead of checking some all encompassing UTXO set whether a coin is spendable you basically attach a proof along with the transaction that shows that given a Merkle root for the entire Utreexo set at some height the coin exists in that tree and is spendable.

TD: One thing I do want to clarify, a lot of people think it is a UTXO commitment scheme. In the software we are using and I think just theoretically it bears no commitment. The miners or the blocks never tell you what that UTXO set is. Similar to today, if you are downloading a block there is no indication what the UTXO set is. You generate it yourself and hopefully everyone’s UTXO set is the same because they started from nothing and built the same thing based on the blocks. In Utreexo as well no one gives you that, you build it yourself. It is very much a direct replacement for the database. No one is going to give it to you but you build it yourself. Hopefully everyone’s is the same. It is a bit different in that if everyone’s is not the same it breaks. Whereas today, hopefully we don’t, it is a bug, but you may have a slightly different UTXO set than someone else. One bug we saw when we were working on this, stuff like OP_RETURN or `is_unspendable`, things you immediately can see. I’m not going to even put that in the UTXO set because you are never going to spend that. You can totally run a Bitcoin Core node where you put all the OP_RETURNs in the UTXO database. It will work, it is a waste of space because they are never going to get spent but you could do that, it’ll still work. With something like Utreexo that becomes a consensus rule which is kind of scary. If everyone doesn’t have the same set the proofs are no longer compatible. If someone says “I put in OP_RETURNs” or “I put in these kinds of things” they are going to be incompatible. That is a little scary. That’s another issue. I did want to clarify that. There has been so much talk over the years about commitments, “Let’s commit to the UTXO set in some kind of message the miner makes”. This does not do that. That maybe something that you could do later do with the same technology but that is a whole other can of worms. None of these are doing that right now.

JOB: It is worth noting as well that at some point there was talk about incorporating a UTXO set hash into the block header. Instead of having a specifically hardcoded AssumeUTXO hash in the codebase we could use the block headers. But as Tadge is saying that is a much bigger question.

TD: A lot of people think it is this. I don’t know that it actually gives you that much in either case. Even AssumeUTXO, you are going to want to validate the last couple of weeks or months anyway. You can hardcode that far back in the binary. Does it really help that much to have miners committing to these things? I don’t know.

JOB: That’s a fundamental shift of trust towards the miners as well.

TD: Even if you were willing to do that, “Let’s make this a commitment” there are a lot of downsides. The biggest that I’ve talked to people about, at least for Utreexo, it keeps changing. We have cool ideas and now it is twice as fast as it was last month or something. We definitely don’t want to commit to some kind of soft fork because what if you find a way better idea in a year but now you’ve got this soft fork thing stuck in that no one wants to use anymore. Also it doesn’t seem to get you that much. For the risk and the change in trust it seems like you can do a lot of really cool things without that. I haven’t really even looked into that much because it doesn’t seem it will help us that much. Let’s not even go there. It is the same sort of idea with AssumeUTXO? It doesn’t seem like there is any need to involve miners?

JOB: Absolutely. Given it has taken two and a half years just to do the implementation I didn’t want to undertake anything even getting close to a soft fork.

TD: That’s what is cool about it. These improvements that aren’t even forks at all. If you want to use it, cool and if you don’t… That’s one of the things we talk about a lot with Utreexo, it is a big enough change that it is going to be hard to get into Bitcoin Core and rightly so. Bitcoin Core is quite conservative with changing all this stuff and it is a pretty big change. Let’s try testnet versions that aren’t Core and play around with that first. Maybe it is the kind of the thing where people use it for a year or two without it being merged into Core. Then it is long enough and well tested enough that people are like “We can move it in now”.

JOB: I was going to say that hopefully with [libbitcoinkernel](https://github.com/bitcoin/bitcoin/issues/24303) it might even be practical or advisable to do Utreexo as a separate project. At the same time I think you guys are going to be modifying so much of what is considered consensus critical. The benefits of having a shared library like libbitcoinkernel probably aren’t as much as if you just want to do your own mempool or do a different peer-to-peer relay.

TD: The messages are different. I have talked to other people who are interested in libbitcoinkernel, libconsensus, that kind of stuff. Getting rid of the database code as consensus code is something people are very interested in. Talking to fanquake, fanquake got rid of OpenSSL in Bitcoin Core a year or two ago. He was like “If we could get rid of LevelDB that would be amazing”. LevelDB is pretty big and does affect consensus. It would be great if it didn’t or if it was walled off or isolated a bit more. LevelDB seems fine and everyone is using it. The transition from BerkeleyDB to LevelDB was this big unintentional hard fork. That’s a scary thing to do if you want to change database stuff. But you may want to in the future. Walling that off would be another project that we want. This is part of it. You sort of need to wall it off a bit to do things like AssumeUTXO as well.

MF: We could definitely have a whole session on Utreexo but we should probably move on. Final question, I am just trying to understand how they could potentially play together. Could you perhaps do a normal IBD from snapshot to tip and then use Utreexo from genesis to snapshot? How are they going to play together? Would you use both?

TD: That you could. You couldn’t do the opposite. You couldn’t say “I am going to do normal IBD from snapshot to tip without doing the genesis to snapshot through Utreexo”. Unfortunately right now Utreexo does need to build itself up from scratch if you want to prove things. You could potentially do something like that. That is sort of a weird case, “I want to start really fast but then I want to be able to provide all possible services to everyone”. It could be a use case.

CK: Just to note, feature wise I think they are fairly different. It is just conceptually and in terms of code a lot of stuff that needs to happen are the same. That’s where they are similar.

TD: It would be cool and something we should look at. I did talk about that a little bit a few weeks ago, a different accumulator design. Maybe there are ways to switch from a complete UTXO set and into the accumulator itself. Right now AssumeUTXO does have this hash that it hardcodes in, “Here’s the UTXO set. Go download it and make sure it matches this hash.” If you could also make that something that would accept Utreexo proofs then that is really cool. It works for both. Maybe nodes that support one could provide UTXO set data to the other and stuff. I don’t know how to do that yet. I have some vague ideas that I need to work on. That would be cool if it were possible, it might not be.

MF: There are a few other proposals or mini projects I thought we’d briefly cover. The impact of the [rolling UTXO set hash](https://gist.github.com/fjahr/fa4892874b090d3a4f4fccc5bafa0210) on AssumeUTXO. Have you used this as part of AssumeUTXO? At least in my understanding there was an intersection between these two projects. Is that correct?

FJ: There is not really an intersection. The hashes that they use now, they could use MuHash instead. But right now it uses the “legacy” hash of the UTXO set. James was already working on AssumeUTXO when I got started with this stuff. The whole UTXO set project was based on the old style of hash. It was very unclear if and when the rolling hash, MuHash, would get in. There was really no reason to change that. Now it is in there could be potentially in the future, instead of the serialized hash, the MuHash could be used. That would give some upside if you run the CoinStats index. It is much easier to get hashes of UTXO sets that are in the past. James has a script to do it with a node but I guess the node is not really operational while you are running the script. It is a bit hacky. This could potentially make it a lot nicer but then of course you would still need to make changes in the sense that these saved hashes in the codebase would need to be MuHash hashes. Of course you could have both in there. That is still a bit off, MuHash first needs to be considered 100 percent safe. We still need to watch it a bit more and get a bit more experience with it and give it a bit more time before that makes sense.

JOB: Definitely. As Fabian mentioned the process right now for checking the AssumeUTXO hash on your own node is pretty hacky because what you have to do is call `invalidateblock` on the block after the snapshot block so that you roll your chain back to the snapshot point. Then you calculate the hash. All the while obviously your node is not at network tip and so not operable. You have to reconsider a block and rewind back to tip. That does take probably 15 minutes at least.

MF: It says here “It is conceivable that AssumeUTXO could use the rolling UTXO set hash but it doesn’t currently”. That’s right yeah?

JOB: AssumeUTXO is really agnostic in terms of the particular commitment as long as you hardcode it. As Fabian said you could imagine that if we decide MuHash has the security properties that we’re comfortable with you could have a side by side listing or something to facilitate migration, just move to MuHash.

MF: There were a couple more that were interesting. I don’t know if James or anybody else wants to comment on these. There was the [periodic automatic UTXO database backup](https://github.com/bitcoin/bitcoin/issues/8037) that has been open for a number of years from Wladimir.

JOB: I haven’t really looked at this in depth.

MF: The other one was the UHS, I don’t know what UHS stands for but that was a [post](https://gnusha.org/url/https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2018-May/015967.html) from Cory Fields back in 2018.

TD: Unspent hash set I think.

MF: Full node security without maintaining a full UTXO set.

TD: I know a little bit about that. Definitely talking to Cory about that stuff was one of the things that led to Utreexo. Let’s keep LevelDB, the UTXO set, instead of storing the outpoint and the pubkey script and the amount, let’s just take the hash of all that. You do need to send these proofs, the preimages, when you are spending a transaction but they are very small. Most of the data you can get from the transaction itself. You just can’t get the amount I guess because you don’t know exactly how many satoshis. The txid and the index itself you’ll see right there in the input of the transaction. The fun thing is most of the time you don’t need the pubkey script. You can figure it out yourself. With regular P2PKH you see the pubkey posted in the input and the signature, you can just that pubkey and see if it matches. It should if it works. You only have to send 12 bytes or something for each UTXO you are spending. We use this code and this technique in Utreexo as well. This is a much simpler thing though because you still have the UTXO set in your database, it is just hashes instead of the preimage data. It is not that much smaller. It cuts in half-ish.

## The AssumeUTXO implementation in Bitcoin Core

<https://github.com/bitcoin/bitcoin/pull/15606>

MF: Let’s talk about the implementation in Core then to finish. The evolution of this, you have the [prototype](https://github.com/bitcoin/bitcoin/pull/15606) just to check it works or convince yourself and convince others that this was worth pursuing. You said this wasn’t mergeable, this was just a prototype. Any interesting things that came out of this other than just initial feedback?

JOB: That started out as a rough prototype. I think it was a single commit when I opened. It has slowly evolved into something resembling mergeable. At the moment I think it needs a rebase but beyond that from my perspective it is code that could be considered for merging. What I’ve been doing is trying to carve off little bits of it and open separate PRs so each change can get the appropriate level of scrutiny. Maybe people can goad me into actually writing unit tests and things like that. This PR does represent the current state of everything needed to do AssumeUTXO. I am regularly testing it.

MF: I misunderstood then. I thought you’d spun off all the other PRs and that was the implementation of it that you thought was going to get merged. This was just the first attempt. But I’ve misunderstood that.

JOB: It initially was just the first attempt. Bit by bit I’ve been keeping it up to date with the changes I do make. All the merged PRs so far have been commits that I’ve carved off from this one. One of the incidental sad things about that PR is that it has got so many comments and so much discussion now that it is almost impossible to navigate based on GitHub’s UI. I don’t know what is to be done about that.

MF: A lot of people complain about the GitHub UI and comments, it is a massive headache.

JOB: Can’t live with it, can’t live without it kind of thing.

MF: You also talked earlier about Carl’s work. He [deglobalized ChainstateManager](https://github.com/bitcoin/bitcoin/issues/20049) which I’m assuming allowed progress on AssumeUTXO. You needed to get rid of various globals to be able to do AssumeUTXO at all?

JOB: Yeah there were a few globals. One, `pcoinsTip` was a pointer into the UTXO set itself, the `CCoinsView` cache which is the in-memory cache entry point into the UTXO set. Another was `ChainstateActive` or `CChain` or something, I can’t remember the name of it. It was a global representing the `Chainstate` object. The block index was a separate global itself. I had to take a few globals and package them up into this `ChainstateManager` which itself became a global. Then Carl came along and made the good change of removing that global favoring passing the `chainman` as an argument to the various places that it is needed. That allows us to do better testing, not rely on global state as much. And I guess to eventually consolidate all the consensus critical stuff into a shared library which is what he is working on now.

MF: That was a big project in itself wasn’t it? I suppose you could still have a global ChainstateManager that manages two chainstates.

JOB: Yeah exactly, that is the whole point of the ChainstateManager versus a particular chainstate object.

MF: Then there’s the (open) PRs. This is the [issue](https://github.com/bitcoin/bitcoin/issues/15605).

JOB: The issue and the original prototype PR got a little bit muddled. There was some conceptual talk in both places.

MF: The [project](https://github.com/bitcoin/bitcoin/projects/11) has all the PRs. We won’t go through them one by one. Quite a few of them are refactors, certainly the early ones were refactors. Add ChainstateManager was an early one we were just discussing that has been deglobalized by Carl. Any particular ones that have been merged that are worth discussing or worth pulling out at this point? James has dropped off the call. We’ll see if James comes back. Let’s go back to Utreexo for a moment. What’s the current status of the project? I saw there was an implementation in Go using the btcd implementation.

TD: We’ve been mostly working in Go. Nicolas and Calvin are making some C++ code but we are working more in Go initially to try things out and then port it over to C++. Someone was working on a Rust version as well.

CK: That was me.

TD: If anyone wants to join Utreexo IRC channel on Libera, utreexo.

MF: In terms of the PRs that have been merged, are there any particular ones that are worth discussing and pulling up? And then we’ll discuss what still needs to be merged.

JOB: The UTXO snapshot activation thing could be worth a look. The `ChainstateManager` introduction is kind of interesting. But to talk through them here is probably kind of laborious. I would just say if you are interested they should hopefully be fairly clearly titled. You can go and read through the changes for any you are particularly interested in.

MF: Any particular context for reviewing current PRs?

JOB: No, I think a lot of the stuff that got merged is pretty self contained. The upshot of what you need to know is that now there is this `ChainstateManager` object, there is an active chainstate, the chainstate that is being consulted for the legacy operation of the system. If you want to check if a coin is spendable or do validation you consult the active chainstate but there may or may not be this background chainstate doing stuff in the background. That’s the current state of where we are. Right now for example [one of the PRs](https://github.com/bitcoin/bitcoin/pull/23174) that’s open, the “have LoadBlockIndex account for snapshot use” is really just adapting different parts of the system, in this case part of the initialization to account for the possible presence of a background chainstate that we have to treat a little bit differently than the active chainstate.

MF: In terms of the review and testing, it looks like you’ve only got one PR left to get merged? Will that be Phase 1 completed?

JOB: I wish that were the case. There is another PR that is open, fanquake has been very kindly maintaining this project because I don’t have the GitHub permissions to add stuff to projects. There is another change in parallel that is being considered in addition to those 3 or 4 PRs up there. What I don’t want to do is open all the PRs I want to get merged at once. I think that will overwhelm people. I gradually as merges happen open up new PRs. If you want to see all the commits that have yet to go in for the completion of Phase 1 you can go to the AssumeUTXO [PR](https://github.com/bitcoin/bitcoin/pull/15606). That has all the commits that are required for that to happen. That is a listing of all the commits that are left to go in.

MF: What’s an easy way to test it? I saw Sjors had found a bug or two and done some good reviews by playing around with it. What could people do to be useful? Is it functional in a way that you can use the RPC and try to do IBD from the snapshot?

JOB: It should be pretty usable. Right now there’s a hardcoded hash at I think 685,000 maybe. Sjors and I have at various points been hosting the UTXO snapshot over Torrent. You can clone this branch, build it and play around with doing an IBD using that snapshot. We should probably create a more recent one but I haven’t thought to do that recently. I bundled a little [script](https://github.com/bitcoin/bitcoin/blob/master/contrib/devtools/utxo_snapshot.sh) in `contrib` that allows you to do a little mock usage on mainnet. It will spin up a new data directory, it will sync maybe 50,000 blocks that happens very quickly. It will generate a snapshot and then it will tell you what to recompile your code with to allow you to accept that snapshot so you can demonstrate to yourself that the change works. I use that as a system or functional test to make sure the main branch still works.

MF: It is functional yet there are still a lot of commits and a lot of code still to merge.

JOB: Absolutely, yeah.

MF: It is working on your branch, gotcha. Any edge cases or tests that need to be written? I was trying to think of edge cases but the edge cases I was thinking of would be like a snapshot that was really recent and then there was a re-org or something. But that is not possible.

JOB: It would be great to have a test for doing pruning and building all the indexes to make sure that code still works. I don’t think I’ve tested all that stuff very rigorously. There is no reason it shouldn’t work but it definitely needs to be tested with pruning and indexing both enabled.

MF: Why might this be a problem?

JOB: There are some accounting complexities. The way that the indexers work is they consume these events on something called the validation interface queue. I had to introduce a new kind of event, a block connected event. I have to distinguish for the purpose of index building between a block connection on an active chainstate versus a background chainstate. The index is now being built out of order instead of in order. If you are connecting blocks from the tip and then afterwards connecting blocks early on that’s a change in assumptions that the indexers are making. On pruning there is some new pruning logic that ensures that when we prune the active chainstate we don’t erase blocks needed by the background chainstate. There are a few changes in there. It would be good if someone tested that stuff. I will at some point, hopefully in a formalized functional test in the test suite. Right now there is a functional test but it just does pretty basic UTXO snapshot operations. It does test a sync between two separate nodes using snapshots. But I haven’t gotten around to writing tests for the indexers and pruning.

FJ: I have a pull request open where I change the way pruning is blocked when indexers are running. There I extend the tests for pruning and indexers together quite a lot. I think it would be easy to add that on after that gets merged.

JOB: That’s right, I think I ACKed that.

FJ: I hope so. There are some comments that I need to address.

JOB: I think I reviewed that a couple of months ago. That would be a really good change to get in. If anybody is looking for things to do reviewing that PR is a good one.

MF: What’s the PR number?

FJ: [21726](https://github.com/bitcoin/bitcoin/pull/21726)

MF: Ok we’ll wrap up. Thanks James and thanks to everyone who attended, it was great to hear about some other projects. The YouTube video will be up and I’lll do a transcript as well.

JOB: Thank you for having me. Really great to hear from everybody, some really insightful stuff.

