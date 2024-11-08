---
title: The Quest for Practical Threshold Schnorr Signatures
transcript_by: Bryan Bishop, Michael Folkson
tags:
  - research
  - threshold-signature
speakers:
  - Tim Ruffing
date: 2019-10-06
media: https://www.youtube.com/watch?v=Wy5jpgmmqAg
---
Slides: https://slides.com/real-or-random/schnorr-threshold-sigs-ces-summit-2019

## Introduction

It's great to be here. My name is Tim Ruffing and I work for the research team at Blockstream. This is a talk about practical threshold Schnorr signatures and our quest for constructing them.

## Disclaimer

First of all, this is work in progress. It's pretty early work in progress, mostly based on discussions with people at Blockstream. I describe the problem we want to solve, and we have some initial ideas, but they are very initial and I have tried to put one or two sentences about those ideas into the slides but nothing is really done yet. If you think what I say doesn't make sense, or the problem is already solved and you have looked into the literature already then please interrupt and tell me.

## Threshold signatures

What are threshold signatures? You have a group of n peers. The idea is that if you have any subset of size t of those n peers they should be able to produce a signature. If you have fewer peers you shouldn't be able to produce a signature. More formally you get an unforgeability property. That means t-1 malicious peers cannot produce a valid signature even if they collude and are malicious. On the other hand you have robustness. This means that t honest peers should be able to produce a valid signature even if the other peers are malicious and try to prevent them from getting a signature. There is the special case where t=n. We call this multisignatures.

## Why Threshold or Multi-signatures?

Why do you need threshold or multisignatures in a Bitcoin or cryptocurrency setting? Mostly for smart contracts. If you think about smart contracts there is always some aspect where some funds are controlled by a set of peers. For example in a payment channel, typically payment channels between two parties, the funds are locked up and you need agreement from both parties to spend them. This is a 2-of-2 scenario. Another scenario could be two factor authentication which would also be 2-of-2. Bitfinex is a large Bitcoin exchange. Apparently they use 3-of-6 threshold signatures for their cold wallet to enhance security. If you look at our own products at Blockstream. One of our products is Liquid. Liquid is a sidechain which means that you can send Bitcoin into this sidechain and transfer it on the sidechain more efficiently and more privately. From the point of view of the Bitcoin system these Bitcoin are held by a federation and are stored on a 11-of-15 threshold signature. There are many more scenarios.

## Goals

Our goal in this talk is to obtain threshold signatures that look like ordinary signatures. The reason for that is first of all they are much more efficient than what we currently have on Bitcoin. They also offer privacy advantages.

## Taproot

`pk = g^(x + H(g^x, script))`

Hopefully Taproot will get deployed in bitcoin at some point, it is currently proposed. The idea is that your UTXO on the Bitcoin blockchain reduces to a single public key. This public key has a secret key in it (x), but it also has a commitment to a script. This enables you to spend it in two ways. Either you can use key-path spending where you just produce a valid signature and a pk. You can do that because the combined secret key is x plus this hash. No one will ever notice in that case that there was a script in there. It's great for privacy and it looks like a normal signature. If you really want to use the script and you don't want to use key-path spending, then you can do script-path spending by revealing g^x and the script and then you can fulfill the script and do whatever the script requires you to do.

The cool thing is that in the key-path spending the script is not revealed at all, this looks like an ordinary spend. In smart contracts the typical case is that all parties agree. You have a lot of rules that keep you secure for cases when parties go malicious or want to disrupt but usually you just get agreement from all parties. You can produce a threshold signature, use key path spending and the only thing that remains on the chain is the public key and the signature. No one will ever notice that there was a script involved or a smart contract.

## Schnorr signatures

`sk = x`

`pk = g^x`

The signature scheme for ordinary signatures that we want here is Schnorr signatures. Maybe you have seen this before maybe not. The secret key is a simple scalar, an elliptic curve group scalar. The public key is g^x. So this looks like ECDSA so far, we don't have to switch the key generation. For signing, you take a random nonce r and you compute a public nonce g^r. You compute the challenge by hashing the public key, the public nonce and the message you want to sign. Then you compute this s value which is the second part of the signature by multiplying the challenge with your secret key and adding the nonce as blinding. This is constructed from Fiat-Shamir protocol. The signature is the public nonce and the s value. Verification is very simple, you re-compute this hash and you check the main equation and the exponent which you can do. If your public key is X then you can write the equation like that and check it.

## Draft for Bitcoin Improvement Proposal (BIP)

There's a [draft](https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki) for integrating Schnorr signatures into Bitcoin. It comes with the proposal for Taproot and other things. If you are interested please take a look. It is on GitHub. It is written by Pieter Wuille, myself and many others. We have a full technical specification, design rationale, reference code. Everything you expect from a specification. Introducing a new signature scheme is quite a big step. If you are interested we need more eyeballs. Go to this short [URL](https://bit.do/schnorr) or scan this QR code or talk to me. If you do applied crypto and you are interested please have a look.

## Naive Multisignatures

`x = x_1 + x_2 + x_3 +…. + x_n`

`r = r_1 + r_2 + r_3 +…. + r_n`

`X_1 = g^(x_1)`

`R_1 = g^(r_1)`

These are Schnorr signatures. How can we get to multisignatures or threshold signatures? Let’s start with multisignatures. The idea is that we split the secret key x into n parts for n parties. For the nonce we want to do the same. Instead of having a single r we have a sum of a lot of r’s. Each of those components belongs to one of our peers.

The public versions of those scalars, because everything homomorphic if you multiply you get the sum and the exponent here. We do this for all the parties. This is a high level view. This is naive because it is not secure. There are multiple problems with that but all of them are solvable. There are full solutions available. For example the MuSig [scheme](https://eprint.iacr.org/2018/068.pdf) invented by people from Blockstream and others in 2018. Concurrently the MSDL-pop [scheme](https://eprint.iacr.org/2018/483.pdf) by Boneh, Drijvers and Neven that solves the same problem in a slightly different way. Both are very good schemes I think.

## From Multi to Threshold

How would we go from multisignatures to threshold signatures? A simple way to depict the idea is like this. The idea is using secret sharing. Under the hood we probably want to use Shamir secret sharing. I won’t explain how it works because it is not important. What it actually gives you is something like this. You have a party on the left hand side. It has a secret a. Let’s say we have a 2-of-3 threshold secret sharing scheme. The party on the left can create three shares and send it to the parties. Maybe send it even to himself to simplify the diagram. Since this is 2-of-3 even if one of those parties on the right hand side goes offline and is not available, doesn’t want to respond, two of the parties can reconstruct this secret a. It is not only that they can reconstruct it, they can actually do computation with it. This is how we use it within in Schnorr. This is only one of the steps.

## Distributed key generation

The second required step is going to fully distributed key generation. We have x. We split it into x_1 + x_2 + x_3 that belongs to different parties. The blue peer here secret shares its own secret x_1 with all the participants including himself. We have this secret x which is split into three parts, each of these parts is individually secret shared amongst all the parties. I depicted it only for the blue peer but the green peer and the yellow peer do the same.

## DKG for Key and Nonce

What I have described so far is doing this for the secret key. You can do this only for the secret key and you get a working for a scheme. We haven’t done a security proof for this yet but it looks reasonable. If you do this only for the secret key, this distributed key generation, then you probably get a protocol that doesn’t have a constant number of rounds. You get O(f) where f is the number of disruptive parties that try to prevent you from getting a signature. This is 2-of-3. If you have 3-of-3 we don’t need the threshold secret sharing at all. We can just use a multisignature scheme as I have shown before. Here we get O(f) rounds. The basic reason is that we have to commit to the set of signers upfront and then maybe you choose a signer that later wants to go offline and then you have to restart. That’s a detail that I don’t have time to explain.

The solution to that is to do distributed key generation also for the nonce. So we do the same as for the key setup but now we have to run a distributed key generation protocol whenever we have a signing session because the nonce is generated during the signing algorithm. If we do that we can go down to a constant number of rounds. Even though we have to add a few rounds to run the DKG protocol.

## History of DKG for DLog

To put this into context these ideas are pretty old. Pedersen in 1991 proposed a distributed key generation algorithm for DLog that uses Feldman’s verifiable secret sharing. It turned out to be wrong. Gennaro, Jarecki, Krawcyz and Rabin in 1999 figured out the Pedersen scheme is broken because the attacker can bias the keypair. They proposed a better DKG scheme that uses Pedersen’s VSS. Note that this is very confusing if you read the paper. Pedersen scheme uses Feldman’s VSS and then Gennaro et al fixed by it using Pedersen’s VSS. Whatever. Even better three years later they figured out the scheme by Pedersen from 1991 is actually good enough for Schnorr threshold signatures. The attacker can bias the public key or can bias the secret key but with Schnorr threshold signatures it doesn’t matter for security. That means that we have two simple schemes available. Either the one by Pedersen in 1991 or the one by Gennaro et al in 1999.

## Why do these schemes fail in practice?

You may ask what’s the point? What are you trying to tell me now? I want to show you why those schemes in practice if you want to apply them.

## Issue 1: Trust Assumption

There are two main issues. The first issue is that there is a trust assumption. All those schemes assume that t-1 is less than half of all the peers. If you remember t-1 was the maximum number of malicious parties. What this translates is an honest majority assumption. If you look at the examples that I showed in the beginning some of them are doable, some not. 2-of-3 is ok, we can do it. 11-of-15 wouldn’t work with this assumption. 3-of-6 wouldn’t work with this assumption. This is not possible in this model. Let me explain why they need this assumption. Let’s use a counterexample. We have a scheme where we don’t have a honest majority, 6-of-9. For unforgeability 5 malicious peers shouldn’t be able to produce a signature. But robustness would say that 6 honest peers can produce a signature. If 5 peers are malicious then there are only 4 honest left. You can never achieve unforgeability and robustness at the same time. That’s actually not true. This is the worst case assumption.

## Assumption Ignores Good Cases

If you look at this assumption, the maximum number of malicious peers should be 5. What if only 3 peers are malicious? Then I can indeed produce a signature. When I set up a scheme I have to choose a t but if I choose t=5 it doesn’t mean that immediately 5 parties are malicious. It just means it is the maximum it can tolerate. Even if 5 people are malicious in the first scenario I can’t obtain a valid signature. This might be acceptable. What shouldn’t happen that those 5 parties can forge. This setting still makes sense. If you saw the [talk](https://www.youtube.com/watch?v=HCwRpOjgP3Q) yesterday by Dahlia Malkhi she talked about flexible BFT in a live but corrupt nodes. This is exactly the setting we have here. If those two peers in the middle, the yellow ones, are live but corrupt which means that they are trying to attack safety, which in our case is unforgeability but they won’t attack liveness this is exactly the model we need.

## Drop the Assumption?

Can we fix these schemes? Maybe there was a weird reason why the papers make this honest majority assumption. Can we drop the assumption and have a scheme where it is indeed the case that if I have 5 malicious peers they can’t break unforgeability, they can only stop the system? Unfortunately no. The security proof relies on the fact that the majority of peers is honest. If you’re a cryptographer the idea is that the security reduction runs all the honest peers internally because it has an honest majority. It gets enough shares from the malicious peers and uses those shares to extract all the secrets of the attacker. This is how the reduction works. We can’t make that reduction work without changing the scheme in this stronger setting. We have one idea how to fix this and this would be to use other commitments in Pedersen’s verifiable secret sharing scheme that enables a reduction to extract some things even without having an honest majority. This is a very early idea, we haven’t looked deeply into it. Maybe it is an insecure scheme, we need to see.

## Issue 2: Broadcast assumption

The second issue is that those schemes assume a broadcast channel. This means that every peer has a reliable and secure way of broadcasting messages to every other peer. This is a reasonable assumption for robustness because if we want liveness we need to assume that this network works in some sense. I think it is an unreasonable assumption for unforgeability. You should fail gracefully. If the network is broken it shouldn’t happen that suddenly people can forge signatures. If you look at those schemes this is what happens.

## Attack on Unforgeability

This is a simple attack in both of those schemes. Let’s say the attacker is the guy in the middle, the broadcast channel. There are 4 peers. What the attacker can do is split the view of 4 peers into two worlds. In the left world he claims that peer 1 and peer 2 are offline. In the second world he claims that peer 3 and peer 4 are offline. What these protocols do now is they reconstruct the secret nonces of the other parties. On the left hand side you would reconstruct r_1 and r_2. On the right hand side you would reconstruct r_3 and r_4. Now the attacker can run one of those worlds to the end. Then he obtains a combined nonce r and by completing one of those protocols the attacker can also obtain a signature. Now given the full private nonce and the signature he can compute the secret key. This means that if you use those protocols naively, if the network is insecure you lose unforgeability. There wasn’t even a malicious peer involved, just the network was malicious.

## Malicious vs Offline

The underlying problem is that malicious and offline are just two different things. If a peer is offline you can’t assume he is malicious. There is no reason to assume this. A nice subtitle for this slide would be Theory vs Practice. Just because a peer is offline doesn’t mean that you should reconstruct his secret in public. The simple idea to fix this is instead of reconstructing the nonce you could just reconstruct the partial signature that the peer is supposed to give. This looks like an easy fix and maybe it works but maybe it doesn’t work. We haven’t tried to prove it is secure but it looks ok.

## Wish list

This is my wish list for threshold signatures. It should be a scheme that produces ordinary Schnorr signatures. There should be no restrictions on the parameter t. It should be unforgeable even if the broadcast mechanism is malicious. We should have robustness and O(1) rounds. It should terminate in a constant number of rounds. We want reasonable message complexity and it should be secure in parallel sessions. I didn’t mention it but it is also a problem in the context of multisignatures.

## Bonus list

If we have that maybe there are some things we can do on top where we don’t really have an idea. Asynchrony would be nice but it seems very hard unless you want to blow up the protocol exponentially. Deterministic nonces is interesting. Usually when you do Schnorr signatures or ECDSA you choose your nonce by applying a hash function to your secret key and your message to make sure you can’t screw up your randomness. But if you do this with multisignatures it is the other way round. If you do it deterministically you immediately leak your private key. We are working on another project where we try to solve this using a zero knowledge proof. I’m not sure it is a practical solution but at least it is a step towards a solution. Another thing we are interested in is looking at the setup algorithm. I have talked mostly about designing but what properties do we expect from setup? Do we want asynchrony or is it ok that the setup is more complex because we need to run it only once. Maybe we can have a real meeting. We need to look into these properties. Also adaptive security which means that corrupted nodes are not fixed at the beginning. I’m not sure how important that is. Then the other interesting property is accountability. Accountability means that if you look at the signature you can tell which of the peers have signed and which haven’t. This really depends on your setting whether you want that. An easy argument is if your signatures should look like ordinary Schnorr signatures then you probably can’t have this property. It looks like an ordinary Schnorr signature signed by a single party so how can you tell who signed? There are other schemes that have this property and it would be interesting to look at those.

## Q&A

Q - Can you expand on why a malicious broadcast channel is fine?

A - You have to assume something about the network. Let’s say the network doesn’t work at all, you can’t have robustness.

Q - If the broadcast channel is malicious you could say that you could easily know that. Or removing the whole assumption on a broadcast channel

A - If you can get for example a scheme that works asynchronously it doesn’t rely on broadcast itself, this would be nice. One simple thing you can do is if you have a scheme that at least is unforgeable even if the broadcast channel is insecure then you can say “I have at most f malicious nodes”. I take f+1 leaders and run the broadcast through these f+1 leaders and I run f+1 instances of the protocol. This is safe because the protocol is unforgeable even if f of those leaders are malicious. Then I get robustness but it increases communication a lot. You can also run a reliable broadcast protocol but this increases communication even more. Maybe this is a simple and practical way to go once you have a scheme that stays unforgeable if the broadcast is malicious.

Q - I thought I remembered that it was possible to construct a composite public key if it was any monotone boolean function of the constituent public keys for a Schnorr signature.

A - I think this is true. I have not looked into those schemes but I think it is possible.

Q - I am a little disappointed you are using Shamir secret sharing, it is fine, it works but it is a completely different mechanism for the threshold. If I can construct a monotone boolean function I can say “Key 1 plus Key 2 OR Key 2 plus Key 3 OR Key 1 plus Key 3”. I was expecting you to go in that direction. Is that not possible? Is there something completely broken about that direction?

Q - The way I am aware of is to use Shamir secret sharing. You can write any monotone function. You have all these groups of n-of-n keys and you have a disjunction. You can have the members of the first group do distributed key generation to all the members of the other group. Now there is a total key that was generated by the first group of participants. Every group is able to reconstruct that key independently using Shamir. That is the only way I am aware of.

A - This is related. The reason why I focused on threshold was it is a simpler setting to start with. What you are saying is one of the most natural extensions. I should have listed it.

Q - The statement I am unclear on is whether it is generally possible to construct a composite public key that is an arbitrary monotone boolean function of the constituent public keys. You give me a signature algorithm which would say “I am going to subtract out all the missing parties that are not signing.” That becomes a pubkey tweak. Then you sign with the ones that are present.

Q - You want the constituent keys to be known upfront?

A - In general you can do monotone functions.

Q - If we assume there is a dishonest majority in a 11-of-15 we cannot guarantee liveness unless assuming that you are going for this f round that you mentioned. There is no escape from that? In this round you don’t say anything. In the next round somebody else will not say anything.

A - Unless we go to this f+1 setting and I don’t think this f+1 setting is unrealistic. Doing the broadcast on f+1 leaders. This is what I have shown here. If you do DKG for the key and for the nonce we can recover the rest of the nonce so we can finish the session. We don’t have to restart the session. One thing we need to be careful about is even if we assume that a lot of people are malicious it is not like we want to solve consensus here. It could be for example in this simple protocol where you run f+1 protocol instances on f+1 leaders they could all obtain different signatures. Having a threshold signature doesn’t mean that we solve consensus. We need to be careful.
