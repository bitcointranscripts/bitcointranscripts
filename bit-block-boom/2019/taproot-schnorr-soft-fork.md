---
title: Taproot, Schnorr, and the next soft-fork
transcript_by: Bryan Bishop
tags:
  - schnorr-signatures
  - taproot
  - soft-fork-activation
  - musig
  - adaptor-signatures
speakers:
  - Mike Schmidt
media: https://www.youtube.com/watch?v=yWEbIkytDJs
---
<https://twitter.com/kanzure/status/1162839000811548672>

## Introduction

I am going to speak about this potential next version of bitcoin. Who here has heard of these words? Taproot? Schnorr? Who has heard these buzzwords these days? Yeah, so, the proposed next soft-fork is going to involve both of these technologies sort of interplaying. We want to talk about what are these technologies and how do we use thse things and why is it important that a bitcoin user or holder understands these technologies? What value does it add? This is going to be not technical enough for the technical people, and too technical for the non-technical people. I'll be at the dinner tonight at Three Forks if you want to talk about it.

## Bitcoin Optech

I contribute to bitcoinops.org, Bitcoin Optech. We try to facilitate communication between exchanges and the Bitcoin Core community. We build those relationships and we have a newsletter. I am not representing Optech for the purposes of this presentation. I was previously a web developer before I fell down the bitcoin rabbit hole a few years ago. I love bitcoin and I am excited to be part of the space.

## Improving bitcoin

How can bitcoin be better? Well, price. Number go up. We talked about that. What other enhancements might make sense that could support the number go up hypothesis and support the price from a technical perspective? If you ask some people, they might say scalability, or efficiency, or more on-chain capacity, cheaper transaction fees, and then maybe only paying for what you use and what I mean by only paying for what you usze this is a screenshot for blockstream.info block explorer, and you need to reveal this script regardless of whether you execute part of the script or all of it, and this can lead to paying large fees for using a complex script, or just not wanting to use the script in general. There are large scripts where you could have many conditionals and it becomes prohibitively expensive to spend. Scaling is one improvement we could talk about.

Other people might say something like privacy. Since these scripts are visible, you can tell what kind of output a certain kind of spend is. This is not good for privacy. The scripts themselves are visible and you can see what the logic are, and you can see the keys of the participants not in a meatspace way but if it's a multisig then you can see which keys are participating. Also, you can tell what the number of required signers are, as this might give away information since different wallets use different default values for this. Scripts can also reveal the nature of a transaction. Everyone can see your script on the blockchain. You can tell that something like Bitgo is transacting or something like Blockstream Green since they do 2-of-3 and 2-of-2. Also, taking money out of the liquid network, you can see that because you can go look for 11-of-15 multisig scripts. Atomic swaps also have a certain transaction structure as well.

Some people think scalability is important, others focus on privacy, and there's a third group that focuses on innovation. Scripts are expensive and therefore people aren't using them. There's a limited number of operations you can do in script, limiting the innovation you can have in the smart contracts. Bitcoin is this immutable thing and it's hard to add to. Also, capping the number of multisig participants. So you have scalability, privacy, or innovation.

## Schnorr and taproot proposals

"In our view, the benefits associated with this soft-fork are not likely to be controversial. It's a win for capability, scalability and privacy." This was from the bitmex blog post about the schnorr and taproot soft-fork proposal. So great, they can help with some of those problems but what the hell are they?

All bitcoins are locked. Only the owner with the key can spend. But you don't just send your key out on the network to spend your coins, since someone else can see your private key and they would be able to spend. You prove ownership of the key by doing a signature. That's how you prove that you have the key. The signatures play the role between the key and the lock in this analogy.

To look at this visually, here is a crude visualization and the technical people are rolling their eyes at me right now. So a public key fits a lock, and the signature is the thing that connects the private key and the public key and a message. We're replacing that digital signature, in Schnorr, with ECDSA and replacing that with a Schnorr signature. It's a different type of signature. You can continue to use ECDSA, it's backwards compatible.

## Schnorr signatures

Let's talk about Schnorr signatures. In an oversimplified nutshell, Schnorr signatures are a way of stuffing in more additional data into a signature itself. This is oversimplified but gives you an idea. There are some interesting things you can put in there. The first kind of hidden data you can put into a Schnorr signature is additional signatures. Say we have a 2-of-2 Schnorr signature address, and in order for the funds to be spent, they must first sign off of the transaction. So that's Alice and Bob and they both must supply the signature. But with Schnorr signature, you have Alice + Bob = Alice and Bob's signature. So the color here is to help you understand that that green encapsulates both the yellow and blue all in one signature without having two separate signatures.

Some people might say, why would you ever choose ECDSA? Why not Schnorr from the get go? Well, that has to do with the fact that there was a Schnorr patent held for 20 years and it expired just around the time that bitcoin was released by Satoshi. So that patent stifled innovation for a long time, and I think that played a large role in why Satoshi picked ECDSA.

Schnorr signatures have key aggregation where you can do 50-of-50 with 1 signature instead of 50 signatures in ECDSA CHECKMULTISIG. Schnorr signatures have other things as well; there's a linearity property where you can add signatures together and aggregate them into a single signature. Call this magic, I guess. We saw that we swap out the signature algorithm in that animation--- you can actually use existing private and public keys with Schnorr, which is great because you don't need a separate keychain for these private and public keys, you can use the existing infrastructure to build on top of Schnorr so we don't have to reinvent a lot of this stuff. Also, Schnorr signatures give some scaling space savings of 10%. These signatures are 10% smaller than ECDSA signatures. Also, there's a formal security proof for Schnorr and there's not one available for ECDSA. Finally, it's just better, just this category of things like the signature can't be malleated which helps with a variety of second layer protocols. It's simpler, and a few other things that I won't get into.

## MuSig key aggregation

There's also MuSig key aggregation. So we have our 3 keys, the 3 of us that want to be in this multisiganture, and we want to be able to have this aggregated key. I have glossed over how that works. One available technology to do that is called Musig. The Blockstream guys put out that paper. It's a way to combine those keys into one key. There are other proposals, too and people are working on this problem. The MuSig scheme and I believe all the other known ones, require off-chain interactivity. Alice and Bob and Charlie all have to work together outside of the bitcoin network to coordinate and get that key created and then signing as well.

## Adaptor signatures

You can also use adaptor signatures, which allow you to have this decoder light that lets you see something else there and that secret allows you to do some interesting things that nobody can detect except the party that has this detector light your partner in this scenario. By signing the coins, you're revealing additional information. This is basically invisible ink. You can do atomic swaps. For maximalists, that is not appealing, but perhaps you are swapping coins within the bitcoin network for fungibility purposes. You can swap between liquid and bitcoin, or to other chains of course, like swapping to an altcoin but why would you ever want to do that. An atomic swap means that if I am sending you bitcoin and you're sending me litecoin, then both of those operations happen or they don't happen at all. It's pretty cool because it's an atomic commitment protocol, and you could atomic swap into the Liquid network and then swap back and it would be embedded in the signature without revealing much information.

Another example of adaptor signatures is coinswap, which is similar to coinjoin and tumblebit. It's a tumbler without revealing which coins are being swapped. I think I put tumblebit in the handout as well. Andrew Poelstra wizard level--- the ability to, his example is, I could give you a proof that I have a solution to a sudoku puzzle but not give you the solution but just prove to you in zero-knowledge that I have a solution. When you send me a bitcoin payment to reveal that sudoku solution, it's revealed in that payment. ((That's just a zero-knowledge contingent payment.))

We can also implement Schnorr payment channels with adaptor signatures. There's also scriptless scripts, which a lot of the math people are working on.

## Taproot

Taproot is where you put a script in there. The simplified version is: it's the hiding of a script in a normal looking transaction using Schnorr signatures. Just like we were hiding atomic swaps, you could also hide a script in there, which enables some interesting things.

There is no more spending to a key or to a script, because all addresses will be scripts and keys. The coins will be able to spent in one or either of those ways. So I've seen this termed as "pay-to-taproot" (P2TR). You can have the key in this scenario, the key can be a Schnorr signature like 1-of-1, 2-of-2, 5-of-7, etc. And you can spend using that aggregated key construction. You can also spend, though, using the script. The script can be multiple scripts, they could be large scripts, and we'll get into the metrics on that. It's hidden unless you use that script, in which case you reveal it after that the script was there and what path ytou have taken on this.

This is the next version of segwit, it's segwit v1. The first version was segwit v0.

What could we do with our hidden script? You can spend using the key path which is a 2-of-3, or you can have a fallback script like a series of fallbacks so that you can immediately spend using a 2-of-2 with your backup hardware wallet and maybe a third-party service that does some 2FA like a phone call to make sure that I actually wanted to sign. After six months, I could have a 2-of-3 with my mom, brother and bitstein and to recover the funds after 9 months I can have something like my lawwyer to recover the funds. Nobody can tell that any of this is going on, with taproot. We don't want to reveal the entirety of the script when we have to spend one of those scripts.  With MAST, you can reveal only the scriptpath you want. You can potentially have hundreds of scripts, and only show the one that you want to execute.  MAST is how you do that. This is great for privacy because people don't know I have those backup clauses, and I don't have to pay for the ones I don't use only the ones that I do use.

## Other examples of taproot

There's a bunch of examples related to exchanges and thresholds. There's telescoping multisig, which is either getting larger or smaller over time. You can start with 15-of-20 and then after a timeout you could have a script that is 10-of-13 and then I can go into a 2-of-3 eventually after a few more months for different business use cases. Additionally, there's the idea of a server honey pot that Blockstream wrote about a few years back. It's in the handout. Also, puzzles are an interesting one. There's a million dollar bitcoin game where there's all these pieces like with Shamir secret sharing shards hidden all over the world and there's teams trying to get those puzzle pieces and try to get the reward. Something like that might work, like collect the signatures.

## Scalability benefits

There are large multisig fee savings, like 30-75%. Multisig doesn't cost any additional amount in these scenarios. So why wouldn't you be using multisig? There's going to be a proliferation of multisig usage in the coming years, assuming these upgrades get adoption and get rolled out. Also, there can be more parties to the custody. You don't want to spend the money for an 11-of-15 because that's going to spend more to transact with; but the fact that you can transact with bigger multisig parties, it means that I think the average multisig set size is going to go up actually. Like revealing scripts that you wanted and not the others. There's also future batch validation with Schnorr signatures giving 2.5x faster block validations. If you want to run a full node or think that's important, then batch verification would be a huge win there.

On the privacy benefits, the all outputs are indistinguishable. The cooperative (key spend) transactions path is also indistinguishable, and nobody can tell that you have a multisig behind it. You're not revealing that you're using multisig to all the participants, and all those negative things we talked about before. The fallback script lets you reveal something, but only if you tell it to.

## Innovation benefits

There are large multisig set sizes made possible by this. You can use up to 4 billion scripts. There are a lot of interesting things we can think about doing with that much free space. Segwit v1 with schnorr/taproot introduces a versioning field to taproot itself, which enables 256 versions of taproot. So you can use different features within each version of that, which is interesting because some people complain well isn't there 16 segwit versions- sure, but you can have subversions of those as well. MAST is just the first version of that.

## Improvements

You don't want to write taproot scripts by hand, or tapscripts. This is not easy to write in bitcoin script. Miniscript and script descriptors can help you write these policies at a higher policy, so you don't have to write all of the lower-level code. That's something being worked on.

bip174 PSBT is the format in which you can pass around a partially-signed bitcoin transaction. You can pass the partial transaction to the different signing machines.

Another thing is that Schnorr and Taproot help incentivize coinjoins. They also have been talking about cross-input signature aggregation where one input has one signature regardless of the number of inputs in the transaction. It's cheap, and you can get economies of scale rather than just to set a regular transaction with 1 input 1 output yourself. This incentivies people to do coinjoins .You will probably not be doing it overtly for privacy reasons, but probably for space savings.

There's some interesting things around lightning and channel factories and being able to onboard a lot of people in a single transaction. These things are further in the future, and interesting, but I don't think they are big enough right now.

## What is Schnorr/Taproot not?

Taproot is not graftroot or g'root or graft'groot or whatever. Also, these proposals do not include SIGHASH\_NOINPUT or ANYPREVOUT. There is also another soft-fork called "the great consensus cleanup" to fix some other bugs, and that's not this. Also, people talk about quantum resistance, and this isn't that either. We talked about cross-input signature aggregation (one signature for the whole tx) and that's not that either. Also people talk about one signature for the whole block, but that isn't part of this yet.

## Bitcoin upgrades

How does bitcoin upgrade? I thought this thing was immutable. There's a lifecycle for possible consensus changes. Read bip1 to see how some of it works. There's an idea, then discussions, then a bitcoin improvement proposal, then getting even more feedback from the community, and that rolls into getting enough feedback on your implementation, and then people talk about how activation is going to happen, and then you need the network activation to really get going, and then eventually the users adopt some technology.

Schnorr and Taproot are still collecting feedback. The implementation is ready, and it's going to happen. From what I'm gathering, there's not a lot of negative feedback about this, so perhaps it wont be too contentious.

This upgrade is only 500 lines of consensus code, which I am not a Bitcoin Core developer, but I've been told this is not a large amount of code to review. This is always something you want to be safe about. This is going to be an easier technical upgrade for ecosystem partners like wallets or exchanges to adopt, because it's a matter of just flipping the segwit version up. Introducing segwit-- it was a bigger jarring change. Don't expect it to take too long to be adopted.

This is completely opt-in, you don't have to know it exists or use it ever. So that's awesome. It's a backward-compatible soft-fork and that means the new version is compatible with the previous versions.




