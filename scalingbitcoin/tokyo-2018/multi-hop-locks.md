---
title: Multi-Hop Locks for Secure, Privacy-Preserving and Interoperable Payment-Channel Networks
transcript_by: Bryan Bishop
tags:
  - research
  - multisignature
  - privacy-enhancements
  - lightning
speakers:
  - Giulio Malavolta
  - Pedro Moreno-Sanchez
  - Matteo Maffei
date: 2018-10-06
media: https://www.youtube.com/watch?v=3mJURLD2XS8&t=1717s
---
Giulio Malavolta (Friedrich-Alexander-University Erlangen-Nuernberg), Pedro Moreno-Sanchez (Purdue University), Clara Schneidewind (Vienna University of Technology), Aniket Kate (Purdue University) and Matteo Maffei (Vienna University of Technology)

<https://eprint.iacr.org/2018/472.pdf>

<https://twitter.com/kanzure/status/1048476273259900928>

This is joint work with my colleagues. I promise I will talk slower than the last talk. In a multi-hop network, the security tool is a hash-time lock contract (HTLC) where the payment is conditioned on revealing the pre-image of a hash function. This is pretty much the main setup for the lightning network today. You can chain multiple hash timelock contracts to chain payments into a multi-hop situation even in the presence of malicious intermediaries.

We have looked at a novel wormhole attack. The idea is to exclude intermediate honest users from successful completion. Intermediaries in the path can collude and prevent honest users from successful completion of the path. They can steal the transaction fees from the honest users. This attack can be generalized. The same conditoin along the path enables this attack. More intermedaries, more benefits. This is important because fees are the basis for the payment channel networks.

What about the privacy situation in the lightning network? As we saw this morning, privacy is an important topic as Ian mentioned this morning. What do we mean by privacy in the setting of lightning and the payment channel network? In our work, we define privacy as the notion of relationship anonymity which is similar to anonymity set size in the tor network. An adversary sitting in the middle of the path should not be able to tell who is paying to whom in any of the payments.

We are introducing 2-party channels in ECDSA. What if we can encode the conditions of the payments in the signature itself? Can we encode the conditions in the hash functions? Can we encode that into the signatures? The ansewr is yes. This is using scriptless scripts for Schnorr signatures, originally proposed by Andrew Poelstra. You take this condition and encode it into the payment condition within the Schnorr signature. In our work, we have a formal description and analysis. Unfortunately, Schnorr signatures is not used in many cryptocurrencies today.

2-party ECDSA signing can be used to jointly construct a signature on a transaction, enabling payment channel open and close transactions to occur with a single public key, preserving the privacy of the channel participants.

In our paper, we provide a formal description and analysis of scriptless scripts using ECDSA. We have a 2-party ECDSA conditional signing where Alice can create a half-signature that Bob can finish only with the signing key for the condition. If Bob creates a signature, Alice learns that. Bob can only finish this if he manages to get the secret key for the pubkey. The only important point we need is that Alice would also be able to learn the secret key from that activity from Bob, in order to forward back and redeem the coins from the previous.

Multiple "chained" ECDSA conditional payments allow multi-hop payments in the presence of malicious intermedaries. This is an ECDSA-based payment channel network.

One-way homomorphic functions suffice for multi-hop locks in full script setting. It's possible to combine OWH-Schnorr-ECDSA locks in the same path, including one-way hash functions (OWH).

Q: Does your scheme solve the wormhole attack that you described at the beginning?

A: Every condition is randomized differently. To open each of the hops, you need a secret key which is unique to each of the hops. If one user in the middle opens the sum of n keys, he doesn't know ... party... he doesn't know which is the ith condition that he could forward it to someone else in the path.
