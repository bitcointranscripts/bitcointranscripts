---
title: Bitcoin Core V0.17
transcript_by: Michael Folkson
tags:
  - bitcoin-core
speakers:
  - John Newbery
media: https://www.youtube.com/watch?v=f33HlAvJUFw
---
slides: <https://www.dropbox.com/s/9kt32069hoxmgnt/john-newbery-bitcoincore0.17.pptx>

<https://twitter.com/kanzure/status/1031960170027536384>

# Introduction

I am John Newbery. I work on Bitcoin Core. This talk is going to be mostly about Bitcoin Core 0.17 which was branched on Monday. Hopefully the final release will be in the next couple of weeks.

# whoami

I live in New York and work at Chaincode Labs. I'm not actually a native born New Yorker. It's nice to be back in London and talking with you guys about bitcoin. I know Michael started London Bitcoin Devs inspired by SF Bitcoin Devs which itself was inspired by BitDevs NYC. It's nice to be here.

Like I said, I work at Chaincode Labs. It's best described as a non-commercial research & development lab. Maybe that's a bit pompous, but that's basically what we do.

I started bitcoin optech earlier this year. The aim of bitcoin optech is to help bitcoin companies adopt scaling technologies such as segwit, transaction batching, coin selection, fee estimation, that kind of thing.

I contribute to Bitcoin Core. Usually I give a bit more color and background on all those things and projects but we're filming this so the guys at home want to get to the main course. If we have time at the end, I can talk about some of those projects.

# Bitcoin Core v0.17

v0.17 is currently going through release preparation. I'll give some fun facts and figures about the release, and then highlight some interesting pull requests. If you have questions then please interrupt.

Bitcoin Core is the reference implementation of bitcoin. Bitcoin Core does not equal bitcoin. It's an implementation, and it's the most widely run implementation. Probably 99% of nodes on the network run Bitcoin Core.

Bitcoin does not have a detailed specification or a prescribed spec from which you can write an implementation. The best we can do is describe the system as it is, and the best description as it is is the source code for Bitcoin Core.

Bitcoin Core is a continuation of Satoshi Nakamoto's original clients released in January 2009. The repository is hosted on github.com/bitcoin/bitcoin and the project page is bitcoincore.org where you can download binaries.

# Lifecycle

In the Bitcoin Core lifecycle, we have a major release every 6-7 months. The last one was v0.16 in February 2018. That was about 6 months ago. We use minor releases for bug releases when necessary, the most recent was v0.16.2. You can look at the lifecycle page on bitcoincore.org/en/lifecycle/ for more information.

# Bitcoin Core v0.17

On to v0.17 now.... There's always a github issue for a release:

<https://github.com/bitcoin/bitcoin/issues/12624>

If you go to PR 12624, you'll see the timeline for the release. We're about here. Back on July 2nd, there was some translation work for strings so that strings can get translated into local languages. Then there's a feature freeze after which only bugfixes go in. The branch happened on Monday, then we do the release candidates, people start testing it, then we do deterministic builds, and we're aiming for a release on September 8th, 2018.

Everyone happy with that so far?

Q: So this is a reference implementation... how would you define the reference implementation, is it the one most widely used?

A: We can't proscribe a spec for bitcoin because it's a decentralized system. We can describe the activity we see in the network, what people are running, and most people are running Bitcoin Core. So de facto if not de juror, it's the specification for bitcoin.

Q: So if most of the nodes moved to btcd tomorrow, then btcd is now the reference implementation?

A: That's a very sybil attackable definition. If the economic majority decides to run btcd then maybe that's arguably the reference implementation.

Q: Some people say you can't have a spec for this system. So effectively, Bitcoin Core is the definition of bitcoin as a piece of software.

A: I'm sympathetic to that argument. You can't tell people what the spec of bitcoin is. Bitcoin is what people are running. If people choose to run Bitcoin Core then that's bitcoin for them. If everyone is running Bitcoin Core then that's the best possible description because it includes all the bugs and the behavior you would see on the network.

Q: Do you think it's dangerous for people to run alternative implementations?

A: It's dangerous. Philosophically, I would like people to run alternative implementations because it seems like a better way for decentralization. But Satoshi and petertodd are in agreement here that an alternative implementation is a menace to the system. If you want to stay in consensus with Bitcoin Core, then oyu need to replicate all of Bitcoin Core's behavior, bugs and all. It's very difficult to do that. Human brains are not good at thinking out all the edge cases.

Q: ... alternative implementation.. Neutrino... or parts.

A: Neutrino is a new lightclient mode that was proposed by roasbeef and others. It's a protocol in itself, really. It was implemented in btcd and it's being implemented in Bitcoin Core. Neutrino is not a consensus protocol, it's a p2p protocol between a full node and a lite node.

Q: You don't run any other implementations, personally?

A: Personally? I do not, no.

# Facts and figures for Bitcoin Core v0.17

Okay, so that's how far we got. Here are some facts and figures. Don't count commits. They are a really lousy metric for individual contributions to a project and overall development velocity for a project for a few reasons. Commits are not fungible. I could open a pull request with 20 commits that are refactoring and meanwhile Suhas could open a pull request with 1 commit that is fixing a critical DoS vulnerability. Which one is more important? The second one, but mine had 19 more commits. It's looking at the wrong thing: we're not constrained on people writing code. Anyone can write code. We're bottlenecked instead on good code review and deep understanding of the system. Count commits at your own peril.

But with that disclosure, I am going to count some commits and I'm going to start by looking at "git log 0.16..0.17" for this data.

* 195 days

* 1225 non-merge commits (6.3/day)

* 748 PRs merged (3.8/day)

* 135 unique commit authors (67 new authors)

* 958 files changed, +45370/-65542 (568/day)

I am going to assume one author is one person here. But you could have more than one github user committing or maybe people could share github users. But it's a close heuristic-- 67 new authors. Every few days we get a new committer to Bitcoin Core. And again lines of code, 568 lines of code changed every day. That's pretty fast. If people tell you that Bitcoin Core is slow moving, then I would disagree with them. Show them that number. I think that's it- any questions about any of those things?

Q: Is it moving too fast?

A: I should add another disclaimer. I ran these scripts. I didn't have other people check my results. Things like this, maybe fiery names count. So- large scale refactors will change a lot of lines. If you want to audit those numbers, I'll try to post the commands I used.

Other interesting figures from the GitHub API, we can look at review comments-- there were 9553 PR and review comments (49/day). 182 unique commenters. I think that's probably a better measure of the activity in this project. MarcoFalke is a maintainer and he ha sa bot that tells you that your PR needs rebasing, and he wins obviously. Wladimir is another maintainer. Promag and PracticalSwift do a lot of reviewing... also very active.. I'd say that's pretty good.

To give you some context over the previous 3 releases, in parentheses are commits per day, fairly steady, between 5.7 to 7... 3-4 PRs/day merged.. new authors, every single release we've had an increasing number of new authors, which I think is pretty good as a health metric for the project. If people tell you that Bitcoin Core is centralized then tell them how many authors we actually have. Lots of comments increasing-- even if Marco has lots of bots and comments, we still have other comments and reviewing activity.

Another metric for you is the Blockstream Core FUD index, which is the fraction of commits or comments by Blockstream employees or interns. It's not many. ((Hmm where's the Chaincode Labs FUD index?) If they are trying to co-opt the Bitcoin Core open-source project, then I would say they are doing a lousy job. Most of the commits are from Pieter Wuille and the remainder are mostly from Andrew Chow. They are really not pulling their weight. Any questions about these numbers?

Q: I would expect it to be noisier, with more people that knows what's going on commenting. People who really understand what's going on.

A: It's a completely open system. Commenting and opening PRs is open to everyone. Generally, you get some trolls, but not that many. Most people are actually trying to help. You might disagree with what they are saying, and maybe they are doing nitpicking about underscores here or there, but on the whole I'd say they are pretty good.

Q: Is there an ability to mute?

A: If someone is trolling, then they can be banned from the github project. If an individual PR attracts brigading then it can be locked. It doesn't happen much.

Q: A lot of what you'r esaying seems to counteract the narrative that it's a stagnant project. Where do you think that comes from? I found it strange.

A: I don't know. There's a lot of strange narratives surrounding bitcoin. I think the numbers speak for themselves.

Q: Some people might say.. say they are into ethereum.. compare to this... I think these numbers are more than ethereum.

A: If you take what I say about commits being a terrible metric, then you can, say, comparing commits is an even worse thing to do. All of this is- changes to an implementation of bitcoin. There were no protocol changes in any of these version v0.15-v0.17. The bitcoin protocol moves fast- or slowly depending on what your preference is. Bitcoin Core is much more active than the protocol.

Q: How do you think about the choppyness of PRs? Some are open for months with lots of comments. But then there are some that are not so popular. In software you want some smoothness and predictability. On the whole, these metrics seme to be positive. But how do you think about the nature of the inertia of large PRs or when they move on?

A: Are you talking about individual PRs and what people struggle to get review and attention?

Q: I don't think it's review, it's the idea that there are- again- building a software team, you're looking for an even flow. It's a measure of velocity. With something like this, that has so many different pieces and so many different interests, how do you think about PRs that are open for a long time- there's code inertia there. If you leave something open for a few months at a time, things get stale, people get angry.

A: I'd argue it's not a team. Bitcoin Core is an open-source process where we have maintainers that click the button to merge but they are not directing or allocating resources. It's different from a proprietary project. It's open-source and decentralized in the extreme, much more than Linux where there's a benevolent dictator. The bigger picture, you can see that it smooths itself out in terms of PRs and commits and there's activity and I would argue it's fairly rapid. For an individual PR, it's an open-source project and if you want something merged, it's your responsibility to write the code and entice people to review it. Once it has acceptance from a large enough number of people, then it might get merged. Some people can't or won't do that. Other people are more successful at that. I think it's the nature of the open-sourceness and decentralization of the project. Does that answer your question?

Q: It's a tough question. It's different from a commercial team.

Q: .. PRs.. consensus... are there any special.. to.. or are there PRs that need to take longer to bring them into testing environments?

A: Anything that touches consensus code receives a lot more attention and the bar for review is much higher. We have wladimir, marco, pieter and jonas and they are the ones that push the button. They look at how critical the PR is, and the bar for merging is higher for something that requires consensus. People are very, very, very careful about consensus-critical code, and rightly so. I've had PRs rejected.

Q: It's based on review? Is there external testing?

A: Individual reviewers will test more thoroughly, probably. We have an integration test suite that runs against every PR, an extended test suite that runs every night on master. I would say the integration testing is pretty good, and it's gotten better over the past 2 years. Unit testing could improve, we could get better test coverage. It's mainly down to individual reviewers and maintainers sensitivity to knowing and experience, wisdom knowing that this PR is going to need more attention.

Q: Has there ever been an attempt to formally identify which parts of the code are consensus-critical? Or is it something tha you build up with knowledge?

A: It would be nice if there was a separate libconsensus but we're not there yet. That's an eventual aim. I don't know if you guys were around back in 2013-2014 when the database backing the blockchain changed from berkeleydb to leveldb which was incompatible. It was consensus but not consensus code... there's wisdom and built-up experience here.

Any other questions on the big picture? Alright.

# Interesting PRs

I spend a lot of time looking at the wallet. There's a lot of interesting wallet changes. I wont read htem out to you. And then there are some other PRs in different parts of the code base. I'm not sure if it's because I spend more time looking at the wallet that I selected these as interesting.

# watchonly wallets

I don't have the PR number here, but it's in that first slide. Our wallet for a long time has had the concept of watchonly keys and addresses where you say I'm interested in this key or address and you don't have the private key so you can't sign transactions and send money away from it, but you're watching it and including it in your balance. Jonas added an option to create a new wallet that only allows watchonly. So you have your addresses on your Bitcoin Core instance, but your private keys might be in a hardware wallet. For some people this might be a better security model where you don't kee pyour cryptographic secrets online, you only use the node to watch for transactions. We don't have full hardware wallet integration support yet, but this is a good step towards that.

# Branch and bound coin selection

Bitcoin is a UTXO system. You don't have an account in bitcoin. Bitcoin doesn't know about accounts. You hold a collection of coins or UTXOs. You might have a 5 BTC UTXO and a 2 BTC UTXO and you know about all of those so you know you have a balance of 7 BTC but there's no concept of accounts in bitcoin.

When you go to spend, if oyu want to spend 2 BTC out of your collection of coins, you need to choose which coins are inputs to that transaction. Every wallet that needs to spend BTC needs to do coin selection in some way. Bitcoin Core used to have a bad way of doing coin selection. And we now are using Branch and Bound coin selection based on Mark's master thesis.

This improves the behavior of the wallet. It uses the effective value of UTXOs instead of their face value, if you like. If you have a 5 BTC UTXO and you want to spend it... because that input into the transaction takes up space, I need to attach fee to that, and it costs money to add a new input. So it's not really worth 5 BTC, it's actually worth 4.999 BTC. We use the effective value now instead of the actual value, and this makes it a more simple knapsack problem  because the values aren't changing as you go about solving the problem. Also we have an efficient search algorithm for exact matches, so that you can avoid change outputs, which adds one more UTXO to your wallet. If you can create a transaction that avoids change, then that reduces your fees.

Q: Is it ... what counts as an exact match?

A: Yes.

Q: How often would you find an exact match?

A: Quite often. Mark said 20% in his data set. He was using a large wallet. If you're an institution or Coinbase then almost-- because you have so many UTXOs, almost all the time you will be able to avoid change. But for a consumer with only a handful of different UTXOs, they might not be able to find exact coins of course.

# Dynamic wallet load/create/unload

Next up, this is something that I worked on. In v0.16, we added the ability to have multiple wallets running from a single node. That's really nice if you have some kind of service and you have clients and you're running nodes on their behalf. Or you have a business wallet and a personal wallet, for whatever reason. You can now completely segregate those wallets and have them running off the same full node.

Prior to this release, you would have had to specify all the wallets at startup on the command line saying which wallets you wanted to start with. This just means we can now load new wallets on the fly, or create them, on the fly. It's just a bit nicer.

# scantxoutset RPC method

Next up is a new RPC method called scantxoutset. When you start bitcoin for the first time and you have a wallet with keys, or you import a new wallet into Bitcoin Core, you want to check the UTXO set and you want to check which coins you own. Your wallet might contain some addresses or keys but you don't know if any of those keys are associated with UTXOs. When we load a new wallet in Bitcoin Core, we scan the entire blockchain from the start and that can take some time. If you're impatient, you might not want to do that every time you import a new address or import a new key. This scantxoutset RPC method allows you to specify a key, address or a script, you can specify the set of unspent coins still in existence and find the ones that match with my script or address. This outputs an array and then you can either sign or do whatever you want with that array.

Q: That seems like a huge win. I always wondered why we had this -rescan parameter.

A: Nobody got around to doing this. You lose your history- you lose your withdrawals and deposits. It's only what you got now. But you could have a hbyrid mode where you do this initially to figure out your balance, and then you backfill.

# An aside on output descriptors

This is something new, it's kind of a shift in the way we think about wallets and how we think about keys, addresses and wallets. Output descriptors was proposed by Pieter Wuille in the last 3-6 months.

The problem he's trying to solve is that if you're trying to import a new key into your wallet, such as a private key, that private key doesn't contain any information about the type of script you're listening for transactions on. A private key will map to a public key, and you can use that public key to create a p2pk, or p2pkh, or p2wpkh, or p2wpkh wrapped in p2sh, or others. So if I just give you a key, or you just give me a key, I would need to construct all of those different scripts and scan the blockchain for every single one. It's inefficient and inflexible.

Output descriptors are a new language for describing pubkeys and private keys that I'm interested in. And scantxoutset uses output descriptors. It's the first RPC that uses that new model for thinking about keys and addresses.

In the future, other RPCs will be updated to use this method. The hope is that the whole wallet will be refactored around this idea of descriptors for outputs, instead of keys and adhoc attempting to determine the scripts for those keys.

This is a gist from sipa: I can send out the lsides and if you're interested in reading..

# Multiwallet for the GUI

In v0.16, we had multiwallet, which was only accessible through RPCs. It's now accessible through the GUI. People using the QT GUI can now access multiple wallets and send from multiple wallets.

# Introduce interface for signing providers

This is another PR that steps towards that output descriptors design for the wallet.

It introduces an interface between the key store and the signing logic. It's a small step, but it's in the right direction. I expect in v0.18 or v0.19 that we will move more in that direction of an output descriptor based wallet and it will be quite a large refactor.

# Remove accounts API

Next up is the accounts API. Has anyone here ever used accounts in Bitcoin COre? Do you know what the accounts were? Accounts was a bolt-on system to the wallet. Bitcoin itself, the protocol, or the network, has no concepts of accounts. The feature of accounts was bolted on into the Bitcoin Core wallet. It doesn't scale. You could end up with negative balances if you had conflicting balances. Our thinking is that accounting should be done outside of Bitcoin Core. You have the wallet, which deals with UTXOs, and then any kind of higher-level logic can live outside of that and you can have accounts outside of Bitcoin Core. We retained the ability to label an address, but there's no longer any concept of those labels having a balance. Accounts have been deprecated and they will be removed fully in v0.18.

# Implement partially signed bitcoin transactions (PBST)

This is bip174 for partially-signed bitcoin transactions (PBST). This was specced out by achow101 and implemented in Bitcoin Core by achow101. This is a way to pass around a transaction that is not complete. We have a format for a transaction that is complete- it's the format for bitcoin transactions of course. Until now, there was no format for a transaction that maybe had one signature but was maybe waiting for a cosigner to sign the second one. There was no way to specify which part to sign. PBST is that format. It would allow me for example if I had a Bitcoin Core instance and a trezor wallet and I had one key on my Bitcoin Core wallet and one key in the trezor wallet then I could sign the transaction in Bitcoin Core and then pass it to the hardware wallet and then submit it to the network. This is a nice interop thing for having some keys in Bitcoin Core and some keys in a different wallet. It should be good if other wallets adopt this standard. Bitcoin Core has now adopted this. It added some RPC commands like decodepbst, createpbst, finalizepbst, etc.

Q: .. it's only going to be available through RPCs?

A: In v0.17, it's only RPCs. That's normally the way things go- if there's a new feature, then initially it's RPC only, and then eventually it might end up in the GUI. PRs welcome, of course.

# Always create signatures with low R values

To understand htis, we have to get into signatures and signature encoding. When Satoshi created bitcoin, he decided that ECDSA signatures in bitcoin would be DER encoded. It's an inefficient encoding for signatures, and it doesn't have to be that inefficient. There's a bunch of non-required bytes. Interestingly, there are two values in a signature-- the (r, s) values. Depending on whether they are low or high, they could be 32 bytes or 31 bytes. The s value must always be low, that's a standardness rule-- it's not a consensus rule, you can have a block with a high s value. But nodes wont propagate high s transactions. R can be high or low (32 bytes)- but R is a random nonce. If you get a R that ends up being 33 bytes then you can just pick another R, and you might be able to get smaller transactions out of this, and you can save up to half a byte on average one every signature. This might not sound like anything, but it's a few thousand bytes a day if everyone does this. Anyone not using Bitcoin Core also benefits from this because they have more space to put their transactions into the blockchain.

Q: There are counterarguments against this, right? You have to screw around the rfc6791 nonce generator right? You do need to... I think it's 1 bit of entropy in your signature that you're losing.

A: That's correct.

Q: So I mean, another person made a comment... adding this as a stretch... slightly watermarks Bitcoin Core wallets on the network. I think this is a stretch.

A: I agree that's a stretch.

Q: I wonder if there's any point to doing this- like half a byte? In transactions?

A: It's a very small win. It all goes back to the encoding. There's really only 64 bytes in the signature that are actually important, but we have fluff around it because that's the encoding that Satoshi used. When we, if we get Schnorr signatures which hopefully we will, we're free to choose our own encoding, and in fact Pieter Wuille has proposed a BIP, which uses 64 bytes, because that's all that a signature needs to be.

Q: If.. assuming there's a high probability of that happening then this is a waste of time if Schnorr signatures happen.

A: Schnorr signatures will not replace ECDSA in bitcoin. ECDSA will still be valid. All the UTXOs in existence are using ECDSA. They still need to be spent. Even after Schnorr gets implemented and activated on the bitcoin network, people will still be using ECDSA. Segwit has been active for just over a year, and about 40% of transactions have segwit inputs. There's still some ways to go with ECDSA. It's not a big change, right? You create your signature and if your R is large then you increment your random nonce by one and try again. It's a pretty easy change and you win a byte.

# Specialized double-SHA256 with 64 byte inputs with SSE4.1 and AVX2

Here's another efficiency gain... this has to do with when we hash 64-byte inputs, which we do a lot in Bitcoin. If you recall that the way we commit to transactions in a block is by placing the root of a merkle tree in the blockheader. A merkle tree here is created by hashing all the transactions and pairwise hashing the digests, where you have a 32-byte output from the first one and a 32-byte output from the other one and you join them together. We had a generic algorithm but Pieter Wuille has implemented a more efficient one using these instruction sets SSE4.1 and AVX2. If you hash a merkle root with thousands of leaves, that takes a handful of milliseconds with the previous algorithm. But with these new optimizations, it's about a 6x win. Even without AVX2 and SSE4.1, even one way, you get a bit of a win, a 30% win. We're talking about milliseconds here, and it might not sound like much, but we do this a lot. We do this hashing a lot. It's the main delay between receiving a block and propagating it on. You receive the block, you get all the transactions and you verify that they hash down to the commitment in the block header and you can't propagate the block until you do that, so this is in the critical path for block propagation. There are several other related PRs that use different instruction sets that are all around the same theme.

I have finished the wallet PRs. That last one was more of a node PR.

# Separating the GUI from the wallet and node

This was a refactor. Normally I wouldn't talk about refactors because it's all under the hood and perhaps not interesting to users. But this is nice because it modularizes the code base a little bit. Until now, it's been a giant blob and different components call into each other in weird places. But this refactor is nice because it implements an interface between the GUI QT code and the node and the wallet code. There's more separation there, now. This is good for hygiene. It's better to have modularization. It's good for testing because you can mock up different components. Starting with this work, we can start to separate hte processes that the GUI is running on, from the process that the node is running on. Eventually we will do the same with the wallet, and then they will all run on different processes, and your private keys will no longer be in the same memory space as your node which is connecting out to the network so this will be good for security and moving the software in the right direction. It's also good from a software project standpoint because doing htis kind of separation means that perhaps in the future we will be able to separate the components out into different projects and be able to work on them in parallel instead of working on just one huge project.

Q: Does it replicate.. does it duplicate code or test.. or .. one thing handles the wallet?

A: The integration test or functional test suite uses the RPC interface and it uses the p2p interface. So at the moment it treats the entire node plus wallet as a single unit. The GUI we don't test with that functional test suite. If we separated out the wallet and had a well-defined interface, then you could separate out the wallet and test it by poking it over that interface. You could test that interface by having a separate test suite attached to that interface.

# Build txindex in parallel with validation

This is Jim Posen's PR. It b uilds the txindex in parallel wwith validation. The txindex is an additional index in the database. Prior to this, it was the same database that mapped the transaction id to the block and the position in the block or more precisely the txid to the blockfile and the position in that file. That's ncie because if you want to look up a transaction then you can use the txindex and find it in your blockfiles and then you can find it. If you don't have txindex on, then once the transaction output is spent then there's no way to find it. Some people run with -txindex enabled. jimpo has separated out that txindex from the rest of the database so it's now its own database. He has also changed the code so that it's built on a separate thread, in parallel with validation, and it never blocks main validation. During initial block download and it's downloading all the blocks and bringing you up to the tip, txindex would block that and slow it down. But now IBD can go all the way up to the tip and txindex can work in the background to fill up the index. Why is he doing this? He is one of the co-implementors of Neutrino, which adds an additional index for each block it creates a new filter on which you match. So he has gone about this by creating a modular design where you cna have any number of indexes running on separate threads going over the history of the blocks. Here this one is just the txindex, and the other one will be the Neutrino index or liteclient index which would run on another thread and create that index as well and eventually serve that up to lite clients. That works, and jimpo has done good work there.

Alright, those are all the PRs I had. That was not quite as long as I expected. Thank you.

# Q&A

<https://www.youtube.com/watch?v=f33HlAvJUFw&t=46m>
