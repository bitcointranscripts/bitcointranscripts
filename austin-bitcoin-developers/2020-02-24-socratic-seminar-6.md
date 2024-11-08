---
title: Socratic Seminar 6
date: 2020-02-24
transcript_by: Bryan Bishop
tags:
  - taproot
---
<https://www.meetup.com/Austin-Bitcoin-Developers/events/268812642/>

<https://bitdevs.org/2020-02-12-socratic-seminar-101>

<https://twitter.com/kanzure/status/1232132693179207682>

# Introduction

Alrighty, let's get started. Gather around. Phil could use some company here. Nobody likes the front row. Maybe the benches.  So I have a little different format for how I want to do it this week. Usually I cover a broad series of topics that I steal from the New York's meetup list. Going through that, I thought there was something that looked interesting which was the new taproot proposals that were finally posted by Pieter Wuille.

My experience with BIPs is that they can be very informative because they are an exac specification, motivation and description of changes to the protocol. But they can be very dense and hard to read, hard to get through, especially if you are a little newer. I always thought it would be nice to be able to discuss these things in a group. The first time you approach a BIP- that would be better than trying to get through it yourself.

Eventually we might go over the segwit BIPs or the wallet bips like bip32 the really important ones. This is a good test. I have the normal things queued up over here, so if we find this too boring, then we could switch over to that. Let me know. We might want the whiteboard. If you could just roll that out... we might find that useful.

# Introductions

((skipped))

# bip340

<https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki>

The transcript here might be boring because I am just going to read the BIP. There are three BIPs: bip340 (bip-schnorr), bip341 (bip-taproot), bip342 (bip-tapscript). The last one is the shortest, it's script changes for taproot.

Q: Why? What's the short reason for any of this?

A: There's a motivation section here. "This proposal aims to improve privacy, efficiency, and flexibility of bitcoin's scripting language capabilities without adding new security assumptions. Attempts to minimize the information leakage you have. And allows for the upgrades."

Bitcoin uses ECDSA signatures. Schnorr signatures have a few benefits. They have provable security. There's a security proof that you can't forge signatures under a certain set of assumptions. To give an equivalent proof in ECDSA you need stronger assumptions. There's a better mathematical proof that signatures can't be forged.  It's better to have a proof that something can't happen.

Another aspect is non-malleability. We have had problems with malleability in the past. What's a good way to describe malleability? ((bryan explains)) It seems like a good thing to have non-malleability but is the main benefit anti-spam, or is it that you're trying to prove that you don't own a private key... do we just assume non-malleability is good? Well, malleability makes your accounting hard. This is what MtGox claims happened. They said malleability made it hard for their system to account for duplicate withdrawals so they slowly bled funds over months, to the tune of 8 figures and nobody noticed. So another reason is simplicity. Segwit solves malleability for lightning. If I want to sign a refund transaction for something that hasn't happened yet, you would like to live in a world where signatures don't effect transaction IDs.

    17:30 < kanzure> in the taproot bip, non-malleability is a motivation: why? segwit solves this right? i like non-malleability of course.
    17:41 < aj> kanzure: wtxid malleability is still nice to avoid, as is having different sizes of witness data which might let people malleate your fee rate over p2p?
    17:48 < sipa> also tx propagation is hurt by malleability, which indirectly contributes to block propagation in compact blocks & co
    18:00 < kanzure> thank you. we're in a socratic seminar at the moment :).

Linearity (pubkey aggregation) is also pretty cool. But taproot doesn't really motivate key aggregation on its own. Taproot could use ECDSA multisignatures inside each branch.

Signature encoding- people have to put bytes into the blockchain and serialize it. ECDSA has this DER encoding. It's 72 bytes. We can go down to 64 bytes for Schnorr signatures. A public key is a pair of numbers- they are just 32 bytes. We are just storing those two numbers and nothing else. We save at least 8 bytes, that's pretty good, better than 10%.

Instead of using compressed 33-byte encodings of elliptic curve points, in this proposal public keys are encoded as 32 bytes. It's the x or y-coordinate. Here we just choose one of them. It's the even one.

They are also standardizing how to do batch verification.

Completely specified- it's deterministic. With ECDSA there's some problems, like see bip66.

The last point is that bip-schnorr uses the same secp256k1 elliptic curve math to do the signatures and verification. Also the same hash functions. We can retain existing methods for secrets and public keys. We don't need new ways to produce secrets or public keys, nor do we need new assumptions. It's the same math behind it, just a different way of applying it. Any questions there?

## bip340 design

Schnorr signature overview: <https://www.youtube.com/watch?v=FU-rA5dkTHI&t=18m40s>

slides (slide 21?): <https://docs.google.com/presentation/d/1QXZBtELcVMoCq6wx-rJr31KvtsqxxcWIewMvuSTpsa4/edit#slide=id.g24158d2d92_0_15>

((thanks tadge this saved our collective butts here))

This crypto system has a few functions: generate key, sign message, verify message given a signature and a message. So Schnorr has existed for decades; the question is what format to serialize this for bitcoin.

Schnorr signatures can be batch verified. Batch verification is leveraging the linearity property of schnorr. This will make initial block download a little faster. IBD is still i/o bound. It won't make it slower, that's for sure. "We choose R-option because it supports batch verification".

I don't understand the key prefixing and related key attacks. We're behind schedule so let's skip this section.

There's a few different ways to encode the temporary nonce and the public nonce. There's a few different ways. The first one is a little bit more efficient for verification, the third one is smaller and results in a smaller bitcoin data directory so they choose the third option. The tradeoff is that instead of being quick at verifying, it's slower but it's less data that you have to keep around. They do this by only including the x-coordinate.

There's also some other information about serializing the different primitives involved in Schnorr signatures, including the quadratic residue.

Tagged hashes...

    18:04 < kanzure> for tagged hashes, in what situation is nonce reuse expected? like low-entropy nonces ..?
    18:04 < aj> do you mean tag reuse?
    18:05 < kanzure> "For example, without tagged hashing a BIP340 signature could also be valid for a signature scheme where the only difference is that the arguments to the hash function are reordered. Worse, if the BIP340 nonce derivation function was copied or independently created, then the nonce could be accidentally reused in the other scheme leaking the secret key."
    18:05 < kanzure> this would only be true for low-entropy nonces right?
    18:05 < aj> or if the nonce is deterministic
    18:06 < kanzure> oh i see, i can see ways that deterministic nonces would conflict.

Let's move on to applications. Adaptor signatures.... useful for privacy in lightning so that each hop doesn't reveal preimages or let observers know what protocol was really occurring once things get on chain. Okay, so yeah. Cool.

There's some stuff for blind signatures, meaning protocols where you're able to sign something without knowing what the message is. Another example is wasabi and samourai coinjoins where you don't give them your inputs, you give them an encrypted version of it, they sign it, then you reveal it after they signature it. They don't know who registered each inputs.

They have test vectors and a python implementation of this. This is readable. It's 120 lines. IT's pretty crazy, maybe we should have just read this instead of bip340.

That was one full BIP. I don't feel like that went very well. I'll admit it. I don't know if this is the best format. What do you guys think? We got a little bogged down. There was this one thing that I meant to go over. I was a little flustered at the time. One thing that is interesting is if you just search terrylab schnorr... it's this interesting article that gives rust-bitcoin examples for a lot of these things. This is an example of the signature aggregation example. If you have two pubkeys, you can take the sum of them.....  The aggregated signature can be constructed, it's equal to the sum of the two signatures. This is the signature aggregation thing. The problem with doing this is that basically there's a-- you can compose, you're doing something with people you don't trust... if their pubkey i.... the problem is that you tell them your pubkey is yours minus theirs and you're able to subtract out your public key. Musig has solved this problem. You have to be smart about how to do this. Musig is an attempt at how to solve this. Linearity has some foot-guns.

# bip341

<https://github.com/bitcoin/bips/blob/master/bip-0341.mediawiki>

Do you want to go over taproot? The schnorr bip took way longer than I was expecting. Taproot is a bigger BIP. It's really hard-core. We could do an executive summary maybe. Let's do motivations and applications.

We already read the motivation section. They sell taproot as a tradeoff that implements some previous things (like bip114, bip117, etc, for MAST) and also a few other things like graftroot, g'root, etc.

There's two ways-- tapscript can be two things: it can either be like, these pubkeys added together and do a signature with these or you can have this tree of different execution conditions and you choose one of these paths along the tree and supply a proof or whatever. This helps preserve the privacy of your other spending conditions. Your three primitives are hashes, signatures or timelocks. Those three things you can build whatever tree of conditions you can come up with. Those are the three things you have to build with, though.

They introduced annex in the witness, it's not used yet, but it might be used eventually. It also commits to other information in the sighash. It always commits to the scriptpubkey which I guess it doesn't use in segwit bip141. The pubkey is included directly in the output. This is pretty dense material.

"Public key hashes are said to protect against quantum adversaries, but the protection is very weak. Actual resistance to such systems can be introduced by relying on different cryptographic assumptions." All of Satoshi's coins are pay-to-pubkey so that's kind of interesting. Ther'es a lot of improvements you can do. Pay-to-pubkey can be used as a tor identity for communication identity in tor. That's interesting, I haven't heard that one. This changes the narrative that pay-to-pubkey isn't necessarily a bad thing. Quantum computers are going to break this anyway, so until we have something better, we should try a variety of cryptosystems.

You won't get legacy addresses here. You can't have legacy taproot addresses. Using P2SH-wrapped outputs provides only 80-bit collision security due to the use of a 160-bit hash. The main concern is that if it's multi-party... if you have one person, if you have 2-of-2, .... they will have half the script of his pubkey. This is all really in the weeds.

"Why does the message you sign include the scriptPubKey?" This prevents lying to offline signing devices about the output being spent. This proves to a hardware wallet what unused execution paths exist.

# bip342

<https://github.com/bitcoin/bips/blob/master/bip-0342.mediawiki>

This one includes changes to the script system. Let's quickly run through this one and then go get some barbeque. One of the interesting things is that they have replaced OP\_CHECKMULTISIG and OP\_CHECKMULTISIGVERIFY.. The description didn't say anything about incompatibility with ECDSA, it just said it's inefficient and this new one is batchable. Can we see an example of OP\_CHECKSIGADD and batchable verification?

You use CHECKSIGADD to get the 1's and 0's and you add them up to see if the CHECKSIGs add up to some number. You can do NUMEQUAL afterwards. You can batch the signatures and see if the threshold is sufficient. If you had a 2-of-3 and 2-of-3, you would add up all six and see if it was four. I am not sure the explanation is strong enough in bip342 for how this is supposed to work versus how it used to work.

Musig is when you're adding signatures and pubkeys together. Musig requires 3 rounds of interaction. You can do k-of-n asynchronously. With musig, everyone needs to commit nonces, and then we all reveal our nonces and then we all sign. Musig is the next one. Musig you only get one pubkey representing the whole thing and one signature at the end, but at the cost of a complex protocol. In this one, you get bigger scripts but you don't have interactivity.

The last one is native schnorr threshold signatures, but you need an interactive protocol. Some of these protocols like Musig seem really complicated.


Sorry this was a little disorganized. Maybe we won't use this format in the future.


