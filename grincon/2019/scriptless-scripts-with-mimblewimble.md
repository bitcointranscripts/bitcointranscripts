---
title: Scriptless Scripts With Mimblewimble
transcript_by: Bryan Bishop
tags:
  - adaptor-signatures
speakers:
  - Andrew Poelstra
---
## Introduction

Hi everyone. I am Andrew Poelstra. I am the research director at Blockstream. I want to talk about deploying scriptless scripts, wihch is something I haven't talked much about over the past year or two.

## History

Let me give a bit of history about mimblewimble. As many of you know, this was dead-dropped anonymously in the middle of 2016 by someone named Tom Elvis Jedusor which is the French name for Voldemort. It had no scripts in it. The closest thing to bitcoin script were these digital signatures. These were just basic cryptographic signatures to demonstrate that people spending coins had the right to spend those coins. You couldn't do multisignatures, you coudln't do timelocks, you couldn't do hash preimages. It wasn't clear that you would be able to do something like lightning, which requires intricate scripting support, much less any of the other crazy stuff people are doing in blockchain.

Voldemort mentioned this at the end of his document. He wanted to figure out a way to translate script operations into discrete log operations. He wants some way to get these basic cryptographic signatures these schnorr signatures with the semantics of a scripting system. And it wasn't clear that this was possible. Voldemort had no idea whether this was possible. He didn't give any hints as to what to do, and that's what scriptless scripts are. It's a direct answer to his question. It's a way to transform script operations into a discrete log.

## Kernels in mimblewimble

<http://diyhpl.us/wiki/transcripts/sf-bitcoin-meetup/2016-11-21-mimblewimble/>

Let me quickly say how bitcoin and ethereum and UTXO-based cryptocurrencies typically work. The state of your blockchain is a giant list of unspent transaction outputs which are amounts and some sort of cryptographic key associated with it. It's a script public key, some sort of script that requires satisfaction in order to spend the coins. Typically this requires just a digital signature, but it can require timelocks, hash preimages, or other requirements. This is the functionality that we have in bitcoin, which we couldn't get in mimblewimble.

We have all these nice features to do whatever we want in these blockchains, but then there's issues with privacy, scalability and so forth. It's an open research problem on the bitcoin side of things- how can we improve the privacy and fungibility story? The cool thing about scriptless scripts is that it gave us a big privacy boost while improving scalability and fungibility.

Mimblewimble is still a UTXO-based blockchain model. We still have a lot of unspent outputs. You need to select some of these coins from this list, produce a transaction that takes those coins as inputs, creates some new outputs. It destroys the old coins, and creates new coins.

There are no scriptpubkeys or public keys associated with the outputs. Mimblewimble requires that- if you add up these outputs, which you can do it's a notion from confidential transactions. It's na interesting algebraic propert.y. The requirement is that if you add the outputs and subtract the inputs, then the result should be zero in terms of the amounts. Because mimblewimble outputs don't have amounts, they have commitments to amounts, so if you subtract your commitments and so on, you have to get a sum to zero. There's a lot of cryptography I'm skipping over. This is basically using homomorphic commitments. It's a neat algebraic property.

There's a further neat algebraic property where a commitment to zero is only such if it's a multisignature key. There's a system of homomorphic commitments and a system of signatures. This is a kernel. Kernels are a commitment to zero that correspond to these two signatures. Your mimblewimble transactions look like ordinary transactions, they have a kernel hanging off, and a kernel proof is hanging off. It's a proof that this object, which anyone can verify, is actually a commitment to zero. This proof looks like a multisignature, typically. This also doubles as authentication.

Here's where the cool part comes in. If you subtract all the inputs from all the outputs across all the transactions, you can do this in bulk non-interactively. These inputs and outputs now look like they are part of the same transaction. But it makes no difference to transaction validity if they were gone. I had something on the right hand side of my equation, or the left side of the equation, it makes no difference whether I add that or not. My kernels stick around, of course.

In mimblewimble, you do this over every transaction in the blockchain. The only outputs remaining are the currently unspent outputs. The only inputs remaining are the coinbases. And this causes a lot of scalability. Basically only the kernels remain.

If you delete this data from the blockchain, then how can you attach more spending conditions to those outputs, if you can't expect validators to even see those outputs? The only thing you can expect validators to see in the long-term are these kernels. There's nothing associating those kernels to those transactions. They are independent objects with proofs attached to them showing htey are commitments to zeros, and there's nothing that would link a kernel to some particular transaction other than maybe time analysis or chain analysis or underhanded things that you can't expect validators to be doing reliably.

So how could you attach any script information to these? Well, let me switch from pictures to algebra to try to answer that question.

## Adaptor signatures

These kernel proofs are looking like Schnorr multisignatures. We talked a lot about Schnorr multisignatures in the crypto space. If you sign your private key, it's a zero knowledge proof of knowledge of the private key. A schnorr multisig is a fiat-shamir transform of the schnorr zero-knowledge protocol.

A schnorr multisig is one created where multiple parties, say 2 parties, add their public keys together, get a new public key which is the sum of their public keys. The summing is an elliptic curve operation. It's the same operation that occurs when you add homomorphic commitments. They add their public keys together. When they want to sign, they create two independent signatures, and then make a single signature. There's two stages to this: to do a multisignature, the parties agree to a message, then they exchange nonces which is one half of a Schnorr signature, which is an ephemeral keypair only for the purpose of this signature. So first they exchange nonces, to agree on the sum of nonces, then they produce signatures. Once they have exchanged the nonces, then the only way to complete the signature other than by restarting and doing a new one, is by producing a specific schnorr signature. They add these two together to get the final one.

After the nonce exchange protocol, the schnorr signatures are in a sense unique signatures. This is a property that BLS signatures have as well. Using this uniqueness, they can come up with some extra secret, and they can encrypt a secret value to their partial signature before they give it to their counterparty. The algebra works out that they can verify that there's some secret that has been encrypted ot the signature. You create your partial signature, then you add the secret to it, and you give that to your friend. If he learns the secret, then he can subtract that off and get the signature. It's the equivalence of learning something that is happening here.

So how can we use this? Well, one party has to reveal a secret to complete the protocol.

## Atomic cross-chain swaps

<http://diyhpl.us/wiki/transcripts/layer2-summit/2018/scriptless-scripts/>

Bob gives Alice an adaptor signature. They are secrets encrypted to the signatures. Bob gives these to Alice on both chains. Before Bob contributes either of his signatures, he does the encryption thing. Now Alice knows that if she sees the signature giving her her coins, or rather if she sees a signature giving Bob his coins then if she learns a secret she can then produce a signature for getting her own coins.

We're not dependent, at all, at what these signatures are signing. We aren't depending on the blockchain signatures supporting any kind of encryption or challenge-reveal protocol or anything like that. We're depending on locktimes existing, for backup reasons, which I will talk about in a minute. We really need very little from the blockchain itself.

In particular, mimblewimble kernels are sufficient for this.

## Features of adaptor signatures

Adaptor signatures are better than the way that people have been doing these things in bitcoin or ethereum. You can do really general things. You can do zero-knowledge contingent payments in bitcoin where the secret you reveal during the signing keys, that the encryption key is a committed secret to the location of buried treasure or something.

You can also chain these things. You can do something like lightning. If you can deal with locktimes in some way, you could get a lightning netwokr payment network on top of mimblewimble. Most of us thought this would be impossible when the mimblewimble paper came out.

There's this re-blinding property- you can exploit algebraic structure here. You can get improved privacy properties, you can join multiple channels and arbitrary DAG shapes, and you can do this dynamically... you can have an existing output and then decide later that you want to use it for an adaptor signature protocol.

Let me say more about privacy. We have a very strong privacy property here, called deniability. If I take any two signatures I can find laying around, like on the grin blockchain, and I can invent my own secret encrypted value, and generate a complete transcript showing that those are actually atomic transactions and they did an atomic swap or something. And the fact I can do that with any two signatures on the chain, says that these transcripts are meaningless and they prove nothing at all. If you are concerned about the privacy of atomic swaps, which is something you should be concerned about, especially in lightning where you don't want all of your payments and financial contacts to be very visible and permanently correlated, then this is a really important privacy property that we were struggling with in lightning for quite a while.

## Limits of adaptor signatures

Let me talk about the limitations here. It depends on Alice being able to look at the blockchain, being able to subtract off her contribution and Bob's contribution. If you have multiple parties, then it gets hard to separate this. It's difficult to extend this to multi-signer protocols. As long as two people are signing, if you're doing a 2-of-3 threshold scheme then you're still okay.

It depends on publication of complete signatures. Dan Boneh just said that one of his top three features is signature aggregation. Unfortunately, signature aggregation breaks this system. We've been brainstorming this, it's very difficult, it seems it may not be possible. But we said that about everything else we're talking about, so I'm no longer worried about things that seem impossible.

## Witness encryption

Witness encryption is my preferred moon math method of doing timelocks. I mentioned a couple slides ago that you could do a zero-knowledge contingent payment, where you do an adaptor signature and instead of sharing a secret across two transactions, instead you generate a zero-kinowledge proof showing that this secret is the encryption key to some NP problem, like a complete transaction on another blockchain or a digital signature from a third-party on some message, or a proof that you found a satellite image that you found oil reserves or something. There's weird applications of zero-knowledge proofs that you can use here.

But these all require that the party knows the secret they are encrypting. In particular, it requires that they know the secret and how that secret solves whatever problem they are claiming it solves. But there's something different, called witness encryption.

Witness encryption lets someone encrypt some data to the solution of some problem without knowing the solution itself. This might sound really moonmathy or impossible. We use "moon math" to describe zero-knowledge proofs in the past. But now we know how to do that. So I want to co-opt the term moon math.

There was a 2013 paper by Garg, Gentry, Sahai, Waters showing that you can do witness encryption with some technology called multilinear maps. I don't know if there are any candidate constructions that aren't broken. Using witness encryption, I could have a problem like: starting from the current blockchain, I want 1000 blocks, and I want to encrypt a proof of that. I want to encrypt one of my mimblewimble signatures to that. I'm using the bitcoin blockchain as a time oracle, committing to a future bitcoin block, which would let me reveal my private key after that timelock. So we can get a refund transaction that will only take effect in the far future. This is something I can do with reference to any time oracle that I want to use that I think will be reasonably efficient and I can describe cryptogrpahically. Any timestamping service that provides timestamping with a predictable key can be used. You don't need any support from bitcoin, or even mimblewimble. You only need the two parties engaged in the protocol to be able to support this.

This is really exciting. This is basically hte most immediate application. I could put up coins up on mimblewimble, and let them take it if they can prove the reimann hypothesis or something, or the twin prime conjecture. In principle, that would be possible.

## Timelocks in mimblewimble

So that's my preferred solution for timelocks. There's some other ways. Absolute timelocks can be added to mimblewimble by having kernels sign a minimum blockheight before which they may not be included in the blockchain.

Relative timelocks are much harder, because kernel signatures are independent of transaction outputs, and transaction outputs are not even guaranteed to be visible to verifiers.

Somsen and Friedenbach in 2016 personal communication had an idea to let kenrels reference .....

## Open problems

That's it, that's the end of my talk. Let's figure out timelocks, scriptless scsripts with BLS, and multiparty 3+ party scriptless scripts. And what about standards and interoperability.
