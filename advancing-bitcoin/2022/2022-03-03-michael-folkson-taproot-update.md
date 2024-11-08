---
title: State of the Taproot Address 2022
transcript_by: Michael Folkson
tags:
  - taproot
speakers:
  - Michael Folkson
date: 2022-03-03
media: https://www.youtube.com/watch?v=8RNYhwEQKxM
---
Slides: <https://www.dropbox.com/s/l31cy3xkw0zi6aq/Advancing%20Bitcoin%20presentation%20-%20Michael%20Folkson.pdf?dl=0>

## Intros

Ok, so good morning. So earlier this week there was the State of the Union Address so I thought I’d make a bad joke first up. This talk is going to be the “State of the Taproot Address”. I promise all the bad jokes that I make in this presentation will all be Drake gifs, there will be no other jokes involved. This is the “State of the Taproot Address 2022”.

## Our thoughts with those affected in Ukraine

I briefly wanted to say we’ve got friends who can’t be here who are going some very hard times at the moment. Obviously we hope that Gleb and others stay safe and they can get back to Bitcoin development activity as soon as possible.

## Timeline

* 2008: Schnorr signatures patent expires
* ~2012: Russell O’Connor discusses the idea of a Merkle tree of spending conditions on IRC
* April 2016: Johnson Lau creates BIP 114 (Merkelized Abstract Syntax Tree)
* August 2017: Multiple authors create BIP 116 (OP_MERKLEBRANCHVERIFY). SegWit activates this month too.
* January 2018: Greg Maxwell posts “Taproot: Privacy preserving switchable scripting” to bitcoin-dev mailing list
* September 2019: Bitcoin Optech Taproot workshops
* November 2019: 100+ people participate in Taproot BIP structured review IRC meetings
* August 2020: Last semantics change to the BIPs
* October 2020: Merged into the Bitcoin Core codebase (without activation)
* February 2021:  Taproot activation IRC meetings start
* June 2021: Taproot locks in after miner signaling threshold reached
* November 2021: Taproot activates on mainnet

On the regularity of soft forks: <https://gnusha.org/url/https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-October/019535.html>

Stumbling into a contentious soft fork activation attempt: <https://gnusha.org/url/https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-January/019728.html>

So there is a very long timeline for how we got Taproot into Bitcoin. I wanted to highlight a few points just so that we think about some of these things when we make future soft fork proposals. A couple of points from this timeline, one it took a very long time. If you go back to 2008 when the Schnorr signature patent expired, people were talking about Schnorr post 2008. The idea for spending from a Merkle tree of scripts dates back to 2012. There were various proposals from that point onwards. There was [BIP114](https://github.com/bitcoin/bips/blob/master/bip-0114.mediawiki), there was [BIP116](https://github.com/bitcoin/bips/blob/master/bip-0116.mediawiki), and these all moved the conversation forward and it was really valuable work. I think it is important that we remember that we do need to get the best proposals into Bitcoin and we need to be confident and clear as a community that when we embark on a soft fork activation process that we are as confident as possible that this is the best proposal to enable the functionality that we want and that it is not going to be replaced by something better in the short to medium term. Obviously the idea of using Schnorr and Taproot, the Taproot proposal was early 2018, I certainly think and presumably we all think because we activated this soft fork that the proposal that we activated was the best proposal. If we’d activated some of these earlier proposals perhaps they wouldn’t be used and we’d have to continue to support them in full node implementations like Bitcoin Core. That is not the best way to go, certainly in my opinion. We need the best proposals into Bitcoin, we need overwhelming community support that whatever we’re activating is the best possible proposal for Bitcoin. I suppose the last point I’d like to make, in a decentralized community it is just impossible to have an authority figure that says “Yes we are going to do this soft fork. This soft fork is going ahead.” In a decentralized community it is really hard. Anyone can stand up, I could stand up today and say “We are going to do a soft fork tomorrow for whatever, a new opcode in 6 months”. Hopefully you would all say “Michael you can’t speak for the community, no one person can say this soft fork is going to happen” which does it make tricky. I think the only solution to this problem is that things go really, really slow. Whenever an activation process starts for a soft fork everyone knows about it. If you’ve paid any attention to Bitcoin technology whatsoever you know about it. The only way you get to do that is community engagement, there were various things, Bitcoin Optech, Taproot workshops, structured review, IRC meetings, tonnes of stuff. This was all really valuable work to get the community to a point where they’d heard about Taproot, they knew the benefits and we were all confident that it was the best proposal to get into Bitcoin. I could talk a bit about activation but I’ll leave activation. That’s probably another talk in itself.

## More Drake gifs

I did promise the only bad jokes would be Drake gifs. We’ve got another Drake gif, [this](https://twitter.com/fiatjaf/status/1499043339487821825?s=20&t=oi1OY4gJMxy7IuH50ZRK_Q) was fiatjaf on Twitter. Who knows what is going to be in the next soft fork and when it will be? Personally I think it will be a bundle of opcodes, sighash flags or Simplicity. Or perhaps both. That would be my prediction but I could be totally wrong and I have no idea how the community will converge on whatever the next soft fork is. But this is a Taproot presentation and there is still tonnes of Taproot work to be done.

## The “real work” begins

Another [tweet](https://twitter.com/pwuille/status/1459778730369368067?s=20&t=2cAoMRNx50daYabUT7Z-Pw) from Pieter (Wuille). This is back when Taproot activated. He said “the real work will be in building wallets/protocols that build on top of it to make use of its advantages”. The “real work” hasn’t started. He is being self deprecating, there were 5 to 10 years of hard work from Pieter and others but there is still so much work to do for various projects. I’ll do a high level overview of the various projects and how they can leverage Taproot, or are in the process of leveraging Taproot. There is still so much work to do to take advantage of the benefits.

## What do/did we have pre-Taproot?

P2SH, P2WSH address that reveals the entire script when spent from

e.g.
```
<key_1> OP_CHECKSIG OP_SWAP <key_2> OP_CHECKSIG OP_ADD OP_SWAP
 <key_3> OP_CHECKSIG OP_ADD OP_SWAP OP_DUP OP_IF <a032>
 OP_CHECKSEQUENCEVERIFY OP_VERIFY OP_ENDIF OP_ADD 3 OP_EQUAL
```

Jimmy gave a great intro to Taproot itself. Obviously before Taproot, a script is saying how certain Bitcoin in a UTXO can be spent. Before Taproot you would have a very long script such as the one below and it would be behind a hash. Whenever you spent from that script you’d have to satisfy the conditions from that very long script. The key point was that it was a very long script and whenever you spend from that script it goes onchain.

## What is Taproot?

With Taproot as Jimmy was saying we can now split this script up into various parts. There is the key path and there is the script path. You would expect to use the key path most of the time, it is a single key spend every time you use the key path in Taproot, only a single key and a single signature are going onchain. Interestingly you can do some multisig schemes, you can use MuSig, perhaps FROST, where it is a multisig protocol but only a single key and a single signature are going onchain. As far as the blockchain knows, whenever you spend from a key path only a single key and a single signature are going onchain. Even if there is some fancy protocol behind how you construct that single key and single signature. The script path would generally be considered the exit scenario when something goes wrong with that key path. I’ve said “Tap me if you need me”. Generally you’d expect to use the key path but you can encode various different spending conditions within this Merkle tree. If you do need them you tap that Merkle root, you prove that the leaf script that you are spending from is in the Taproot tree. Then you satisfy the conditions of that leaf script to be able to spend from that pay-to-taproot (P2TR) address. This really should be imprinted on your minds. Certainly if you are thinking of doing anything with Taproot or leveraging Taproot.

`Q = P + H(P | c)G`

* Q is the tweaked public key
* P is the internal public key (P = xG where x is the private key)
* H is the hash function
* | is concatenation
* c is the commitment to the Taproot tree
* G is the generator point

<https://github.com/bitcoinops/taproot-workshop/blob/master/2.2-taptweak.ipynb>

Alternatively if you prefer a math formula, that’s the math formula for Taproot. You are committing to the internal pubkey, the Taproot tree and that’s all combined into the Taproot pubkey which is encoded into the Taproot address.

## Sending and receiving to P2TR addresses

So the first step, any project, any business in the space should be thinking about is supporting sending to P2TR addresses and also ideally receiving to P2TR addresses. Murch has this [wiki page](https://en.bitcoin.it/wiki/Bech32_adoption) where he is monitoring community adoption for the various projects, wallets, protocols etc that are supporting sending to P2TR.

## Working towards a circular P2TR address economy

Murch had an interesting point on [Twitter](https://twitter.com/murchandamus/status/1493234619021504512?s=20&t=2cAoMRNx50daYabUT7Z-Pw) where he said it is really important that projects don’t wait for other projects to start adopting Taproot. The really important thing is that if a project looks around and is going “No one else supports sending to a P2TR address” they are not going to support receiving to a P2TR address.

## What is a P2TR address?

What Bitcoin Core and Lightning implementations have done is enable sending to any future SegWit version. There is an example of a P2TR address, the `p` represents `1` so this is SegWit version 1. Whenever you see a `bc1p` that is a mainnet Taproot address. It is really important that all businesses, projects support sending to this because if they don’t support this you can’t give out a Taproot address. If there is a wallet that can’t send money to a Taproot address then you can’t give them a Taproot address to send to. As Murch said you can even support sending to future versions because it is the responsibility of the person giving out the Taproot address that they don’t give out Taproot addresses they can’t spend from or that anyone can spend from. Ideally the approach everyone would take is to support sending to any future SegWit version even at this point, whether it is SegWit version 2, 3, 4 and who knows whether we’ll have any of them. We are back into the world of speculating future soft forks.

## Taproot’d wallets (including Bitcoin Core)

So I talked about sending to Taproot addresses, obviously generating Taproot addresses and receiving to those addresses is a bit more complicated. You need to know how to spend from that Taproot address and that is a lot more complicated than just being able to send to a Taproot address. There are various levels of support. Hopefully people will support spending from key paths, script paths and eventually supporting constructions of complex Taproot trees of scripts.

## The Taproot descriptor tr()

`tr(pk_1,{pk_2,pk_3})`

<https://bitcoin.stackexchange.com/questions/115227/how-to-represent-a-taproot-output-with-more-than-2-scriptleaves-as-a-descriptor>

Support for the `tr()` descriptor was included in Bitcoin Core 22.0. Only creates `tr()` descriptor in fresh wallets.

PR 22051 (Basic Taproot derivation support for descriptors): <https://github.com/bitcoin/bitcoin/pull/22051>

An open PR 23417 to allow old wallets to generate Taproot descriptors: <https://github.com/bitcoin/bitcoin/pull/23417>

I think the best practice now, especially for a new wallet, is to use descriptors. Andrew Chow has introduced a new Taproot descriptor `tr()`. In Core it only supports spending from pubkeys on both the key path and the script path. If you go back to that Taproot tree diagram even if you are spending from the Taproot tree currently the Bitcoin Core wallet will only let you spend from a single pubkey even if you are using a script path, a leaf script. You are only spending from a single pubkey currently. Obviously there is work being done such that that restriction will be lifted. The Core wallet and other wallets, they’ll support from sending from complex scripts within the Tapleaf of a Taproot tree.

## multi_a() and sortedmulti_a()

* PR 24043 (Add multi_a descriptor for k-of-n multisig inside tr): <https://github.com/bitcoin/bitcoin/pull/24043>
* Added to milestone for Bitcoin Core 24.0

Interestingly Script didn’t change much. “Tapscript” is the terminology we are using, this upgrade to Script. Script hasn’t actually changed much, it was just that Taproot tree structure that we introduced. One of the few changes to Script as part of the Taproot soft fork was the replacement for CHECKMULTISIG, CHECKSIGADD is not yet supported in the Bitcoin Core wallet but that are descriptors that map to the use of this new multisig opcode. And presumably other projects will also use these updated multisig descriptors that support CHECKSIGADD in the future. Obviously totally different to MuSig and FROST which are doing a multisig protocol but only a single key and single signature going onchain. With CHECKMULTISIG and with these multisig descriptors multiple signatures and multiple keys are still going onchain. There are lots of different areas to multisig and Jimmy did a great job of going through some of those.

## Taproot’d Miniscript

Once we get onto enabling complex scripts, I totally agree with previous speakers, I think Policy and Miniscript is going to be the way to go. Sanket is talking on Miniscript later and doing a workshop tomorrow. I certainly recommend attending those.

## Miniscript (recap)

<https://bitcoin.sipa.be/miniscript/>

Policy: `thresh(3,pk(key_1),pk(key_2),pk(key_3),older(12960))`

Miniscript: `thresh(3,pk(key_1),s:pk(key_2),s:pk(key_3),sdv:older(12960))`

Miniscript from C++ compiler has since changed: <https://bitcoin.stackexchange.com/questions/115288/why-has-the-miniscript-for-this-particular-policy-changed-over-the-past-few-mont/>

When you are constructing a script or tweaking a script I think the future will be interacting at the Policy level. If you compare the complexity of the script to the policy the policy seems a lot easier to construct. The Miniscript compiler will generate that Miniscript for you and that Miniscript is just an encoding of Script. The problems with trying to construct one of those scripts for yourself without using something like Policy and Miniscript, it is very easy to get things wrong. You can very easily lock up funds accidentally, you can have hidden spending paths that you didn’t realize you had that could allow parties in your multiparty protocol to steal your funds or a hacker to steal your funds. There is just so much that can go wrong when you try to start constructing your own script. There is work to do to finalize the first version of Miniscript. But I certainly think that’s going to be the way to go if we are going to be writing complex scripts ourselves and perhaps tweaking them depending on the demands or interests of particular projects because they will all want different scripts presumably. Lots of different combinations and multisigs, timelocks, hashlocks whatever.

## Taproot’d Miniscript

Miniscript is not yet finalized or in Core. darosior is doing work to get that into Core, that’s been a long term project, this is the Core wallet obviously. There are a few open questions. Does Policy and Miniscript ignore these multisignature protocols where only one single key and one single signature go onchain? Do you just effectively put a pubkey into your Policy and then Policy and Miniscript doesn’t know anything about these complex multisignature protocols? Or does Miniscript tell you to use MuSig and FROST because it is more efficient and less data is going onchain? They are kind of open questions. Updating the Policy to Miniscript compiler is going to be a big project potentially. This would be the Miniscript compiler constructing that Taproot tree for you. You effectively say “These are all the conditions I want. I am likely to spend from this one but I might not spend from these others.” Then the Miniscript compiler would construct that Taproot tree for you, very ambitious, Sanket will tell you more on whether we’ll be able to get there. The running theme is there is still so much work to do now that we have Taproot and on various projects we are kind of just scratching the surface. We are certainly nowhere near the end destination for enabling a lot of this Taproot functionality.

## Taproot’d Lightning

* Closing a channel to a P2TR address
* Opening a channel from a P2TR address
* Taproot multisig for 2-of-2 (OP_CHECKSIGADD)
* MuSig(2) for cooperative closes (space savings, privacy)
* Using the Taproot tree for alternative script paths
* PTLCs
* Other Taproot ideas (additional spending path if peer comes back online)

Oliver (Gugger) will be talking about Taproot’d Lightning later. I chatted to him a couple of days ago, just to check I wasn’t going to repeat what he was going to say later. I’ll say a couple of things on Lightning. There are some people who are very enthusiastic about upgrading Lightning for Taproot. t-bast has a great [doc](https://github.com/t-bast/lightning-docs/blob/master/taproot-updates.md). I did say all my gifs would be Drake ones but I lied. Anyway that’s t-bast’s. There is a lot of enthusiasm but it is a big project in itself. The Lightning implementations, as far as I know, all support closing a channel to a P2TR address. Again everyone should, Lightning wallets etc. Opening a channel from a P2TR address is a work in progress. Then there are various questions. Are we going to use this new Taproot multisig opcode (CHECKSIGADD) or are we going to wait for MuSig? Are the Lightning template scripts going to use the Taproot tree? PTLCs is a whole other problem. With HTLCs you have a hash and a preimage, the preimage goes from the destination back to the source. If we are going to have PTLCs you are going to have the equivalent of a private key to a public key getting exchanged back from the destination to the source. And so it is not just a question of upgrading a channel between peers, it is can we use PTLCs from source A to destination B. That’s going to be a real problem because it is not just upgrading a channel, it is looking at the whole route and checking that PTLCs are enabled from the source to the destination. Long term project, lots to discuss, barely scratching the surface.

## Taproot’d Lightning - upgrading Lightning gossip

<https://btctranscripts.com/c-lightning/2021-11-01-developer-call/#future-possible-changes-to-lightning-gossip>

One thing there has been quite a lot of work so far on Lightning that I don’t think Oliver is going to cover later, upgrading Lightning gossip. If Lightning was to upgrade to using MuSig, rather than the 2-of-2 with 2 signatures and 2 pubkeys going onchain it would only be one pubkey and one signature going onchain. It would be very difficult to identify onchain what the channel opens and channel closes are. But currently Lightning gossip still gossips which UTXO you are committing to when you are opening a channel. You are getting the privacy benefit on the blockchain but if anybody, Chainalysis or any of these bad guys, is monitoring gossip they still can currently determine which UTXO you’ve committed to. Ideally we would sever that link entirely and we’d have a gossip protocol on the Lightning Network where you are able to prove that you had those funds to open a channel and not actually say which UTXO it is. There have been various discussions on how to do that. So far the conclusion sadly has been that a lot of the cryptographic magic like ring sigs, ZK proofs aren’t mature, have very large proofs which makes it problematic to use new cryptographic magic to achieve that severing of gossip ties. Possibly you could just commit to a small UTXO and then make lots of large channels because you’ve committed to a single small UTXO. But obviously that is opening up a partial DoS vector because you could prove that you own 0.1 Bitcoin and then open channels with 10 Bitcoin and you don’t actually own 10 Bitcoin. Still in discussion but there has been movement in terms of upgrading Lightning gossip. There are other questions like do you use stuff like [Minisketch](https://btctranscripts.com/c-lightning/2022-03-07-developer-call/#minisketch-and-gossip-spam) and do a big gossip update or do we just stick to Taproot stuff? Still lots and lots to discuss, still scratching the surface.

## Taproot’d Lightning - Views on the way forward

ZmnSCPxj <https://bitcoinops.org/en/newsletters/2021/09/01/#preparing-for-taproot-11-ln-with-taproot>

AJ Towns <https://gnusha.org/url/https://lists.linuxfoundation.org/pipermail/lightning-dev/2021-October/003278.html>

There are differing views on what should be prioritized. I just have two people, Z-man and AJ, but various people have different levels of enthusiasm/time to prioritize this. It is going to take a lot of work, if you went to the Lightning event a couple of days ago, the spec process is 2 implementations implementing a new feature and formalizing a particular spec or BOLT. It is not just the case of an individual implementation implementing it and running with it, we want compatibility across implementations on the Lightning Network ideally.

## Taproot’d Lightning - Channel upgrades

BOLT 2 (upgrade protocol on reestablish): <https://github.com/lightning/bolts/pull/868>

I’lll skip that because I think I’m coming up on time.

## Taproot’d Liquid

* New opcodes enabled through OP_SUCCESS mechanism
* PSBT v2 for confidential transactions (PSET)
* The 11-of-15 threshold sig peg in/out using  FROST or a similar threshold scheme
* Simplicity

There is some interesting stuff on Liquid. Taproot is activated on Liquid but there are some new opcodes on Liquid. It would be really cool if we get Simplicity on Liquid. That certainly seems a strong candidate for a future soft fork. Simplicity is a complete replacement of Script itself, a lot of the problems with Script that Miniscript tries to resolve. Simplicity would be a complete replacement of Script, at least for that Tapleaf version taking Script out completely.

## Other protocols

* Coinswap/Teleport (currently using ECDSA 2-of-2, could use MuSig2 in future)
* Atomic swaps
* Scriptless scripts/adaptor signatures
* DLCs

There are other protocols. Before Taproot was activated there was lots of enthusiasm for all these off-chain protocols using Schnorr and Taproot. Hopefully that enthusiasm will come back. Now we’ve got Schnorr I don’t know why people aren’t revisiting all the ideas they had for building off-chain protocols with Schnorr. Hopefully people will digest that we actually have Schnorr signatures onchain now and the cool ideas they had for using Schnorr are now possible.

## Future possible soft fork(s) built on Taproot

* New sighash flags (e.g. SIGHASH_ANYPREVOUT)
* New opcode(s) e.g. OP_CTV, OP_TLUV, OP_CAT, OP_CHECKSIGFROMSTACK etc
* Simplicity enabled on a new Tapleaf version
* Graftroot, G’root etc
* Cross input signature aggregation (needs Taproot successor)

Lots of ideas for future possible soft forks. We will hear about some of them at the conference. But as I said let’s, as a community, be very slow and cautious and ensure that whatever is in the next soft fork, whenever that is, is the best possible proposal for Bitcoin and won’t be replaced something superior a year or two afterwards.

## Q&A

Q - How often do you look at other wallet implementations and other node implementations?

A - I try to follow Bitcoin Core and Lightning spec. I feel as if I’m stretched way too thin doing that. I do follow Murch’s wiki site to see what the community adoption of Taproot is. I am aware that Laolu and Oliver have got a bunch of Taproot stuff into btcd, the Go alternative full node implementation to Core. I try to monitor it at a high level but I feel as if I’m stretched way too thin just trying to follow Core and Lightning but doing my best.

