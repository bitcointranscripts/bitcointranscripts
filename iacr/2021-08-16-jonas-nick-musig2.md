---
title: 'MuSig2: Simple Two-Round Schnorr Multi-Signatures'
transcript_by: Michael Folkson
tags:
  - musig
speakers:
  - Jonas Nick
date: 2021-08-16
media: https://www.youtube.com/watch?v=Dzqj236cVHk
---
MuSig2 paper: <https://eprint.iacr.org/2020/1261.pdf>

## Introduction

This is a talk about MuSig2, simple two round Schnorr multisignatures. I am Jonas Nick and this work is a collaboration with my colleague Tim Ruffing at Blockstream and Yannick Seurin.

## Multi-Signatures

Multisignatures allow n signers to produce a single signature on a single message. The signing protocol can be interactive and require multiple communication rounds. We distinguish between multisignatures where n-of-n signers can produce a signature and threshold signatures where any subset of size t out of n signers can produce a signature. This work covers only multisignatures.

## Multi-Signatures in Bitcoin

Our interest in Schnorr multisignatures mainly stems from its potential applications to Bitcoin. Bitcoin allows setting up policies that require multiple parties to cooperate and create signatures to spend a coin. This is commonly referred to as multisig policy in Bitcoin. It can be used simply to store Bitcoin on multiple devices to achieve a higher level of security. Moreover many advanced offchain protocols which are also called smart contracts require a multisig policy. For example a Lightning payment network and federated sidechains.

## Trivial Multi-Signatures

It is trivial to construct multisignatures from standard signatures. Just concatenate individual public keys and individual signatures. This is possible in Bitcoin today using ECDSA. But for n signers this requires O(n) space and verification time. This is particularly bad in blockchain systems where storage is very expensive and all nodes need to verify all signatures on the blockchain.

## Schnorr Signatures in Bitcoin

The Bitcoin network will support Schnorr signatures soon. The Schnorr signature specification called Bitcoin Improvement Proposal 340 is part of the ongoing Taproot soft fork. It has been locked in for activation in November. There are a few reasons to prefer Schnorr signatures over ECDSA. Provable security, efficiency and most importantly for this work Schnorr signatures allow easier construction of advanced signing protocols.

## Vision

The vision is to have a layered design. On the onchain layer we will just have support for Schnorr signature verification. That means nodes on the Bitcoin network will be able to verify ordinary Schnorr signatures and this is part of the consensus rules. This simple functionality enables us to deploy advanced signing protocols in an offchain manner without the need to change the consensus code every time. For example we can build multisignatures on top as we do in this work but we can also build threshold signatures, blind signatures and possibly other advanced signing protocols. As long as the output of the signing protocol looks like an ordinary Schnorr signature it will be understood by the nodes on the network. This design has multiple advantages. First of all the onchain consensus layer is kept simple and the complexity is moved to offchain protocols. What ends up onchain is just an ordinary Schnorr public key and signature. This is great for privacy because just by looking at the chain an observer cannot tell that a complex protocol is in fact going on in the background. Moreover this approach is efficient and the onchain data is very compact (everything O(1)).

## Multi-Signatures That Look Like Ordinary Schnorr Signatures

To make this vision reality we need a multisignature scheme that is compatible with ordinary Schnorr signature verification.

`SchnorrVerify(pk, sigma, m)`

The first challenge here is that we need an interactive signing protocol that enables n signers to produce an ordinary Schnorr signature. The second challenge is we want a non-interactive key aggregation algorithm so everyone should be able to combine a multi set of public keys into a single aggregate key.

## Fully Compatible Schnorr Multi-Signatures

We call this scheme with these two properties a fully compatible Schnorr multisignature scheme. If we look at existing schemes in the literature one nice scheme with this property is MuSig, which we are going to call MuSig1 to distinguish it clearly from our work here. MuSig1 works in the plain public key model. Other multisignature schemes typically require proofs of possession in their public keys to avoid rogue key attacks. Usually signers need to prove in zero knowledge that they really know the secret key corresponding to their public key. The novelty of MuSig1 is to avoid this. But the main drawback of MuSig1 is that signing requires 3 rounds of communication. We recently worked on another variant of MuSig called MuSig-DN. The DN here stands for deterministic nonces. The primary goal of this work was not to obtain a 2 round scheme but to achieve a deterministic signing protocol. The background is that discrete logarithm based signature schemes usually need a random nonce. In single signer signatures the nonce is in practice derived deterministically from the secret key and the message in order to avoid catastrophic failures in real world random number generators. For example repeating randomness. If you reuse randomness as a signer everyone can extract your secret key. Interestingly you cannot do this deterministic derivation easily in multisignature schemes. In fact if you apply the same techniques to multisignatures naively the security of the resulting scheme breaks down entirely. One way to fix this problem is to use a large enough hammer and add an expensive zero knowledge proof to the signing protocol. As a nice side effect one can obtain a two round signing scheme. Due to the complexity of this zero knowledge proof this protocol is not at all simple and it is currently unfeasible to use on dedicated signing devices such as hardware wallets as commonly used for storing Bitcoin.

## History of Two Round Schemes

It is insightful to look at previous attempts to construct two round schemes secure under concurrent sessions, when the attacker can open multiple signing sessions with the victim concurrently. An early revision of the MuSig1 paper in fact was a 2 round scheme but Drijvers et al discovered a flaw in the security proof that we will discuss later in this talk. Not only did they show that the proof was flawed but they also gave a super polynomial but practical (subexponential forgery) attack against the scheme. And they gave a meta reduction that rules out a security proof against polynomial adversaries. In response a third communication round was added to MuSig1 before it was published in DCC 2019. At EUROCRYPT 2021 a better attack was found that not only requires polynomial running time. In fact the attack is efficient enough so that you can properly form it on your pocket calculator. Surprisingly the exact issue that was overlooked in the flawed MuSig1 proof was already identified and described by Nicolosi et al 15 years earlier in their work on 2 party signatures. In fact Nicolosi et al had to limit the number of concurrent sessions supported by their scheme in order to sidestep the issue and obtain a valid security proof. But apparently neither the MuSig1 authors nor Drijvers et al were aware of this work. Also we learned about the work only when it was brought to our attention after we presented a preliminary version of MuSig2 at Real World Crypto earlier this year.

## Outline of the Talk

We will continue by warming up our memory of Schnorr signatures and examine MuSig1 and why it is a 3 round protocol. Then we move our focus to MuSig2 and explain how to properly get rid of the communication round that had been added in MuSig1. We will obtain a simple 2 round protocol and we will explain why in some situations it is even more efficient than 2 rounds.

## Schnorr signatures

Before we get to multisignature let us quickly go over the definition of Schnorr signatures. We have a secret key `x` and a public key that is `g^x` where `g` is the generator of a group and which we assume the discrete logarithm is hard. Note that we are using multiplicative notation for the group operations. In order to sign a message `m` with a secret key we draw a fresh scalar `r` and compute a commitment `R` equal to `g^r`. `R` is typically called the nonce. Then we obtain a Fiat-Shamir style challenge by hashing the public key, the nonce and the message.

`c = H(pk, R, m)`

We compute `s` as the secret key times the challenge plus `r` and return `(R, s)`

`s = x.c + r`

In order to verify a signature `(R,s)` of a message `m` for a public key we first compute the challenge hash and then use group operations to verify that the `s` value was computed correctly.

`c = H(pk, R, m)`

`g^s == X^c . R`

## MuSig1: Schnorr Multi-Signatures with Key Aggregation

Let’s look at MuSig1, Schnorr multisignatures with key aggregation.

## Strawman Multi-Signatures

Conceptually it is straightforward to construct correct but insecure multisignatures from what we’ve already seen about Schnorr signatures. Assume for simplicity that we only have two signers, each with a secret and a public key. We can multiply the public keys to create an aggregate public key and similarly we can multiply the nonces.

`X = X_1. X_2`

`R = R_1. R_2`

`c = H(X, R, m)`

It is easy to check if the signers create partial signatures `s_1` and `s_2` for the same message. The sum `s`  of the partial signatures and the product `R` of nonces is a valid Schnorr signature for the aggregate public key.

`s = s_1 + s_2`

return `(R, s)`

This scheme is insecure for two reasons. The first reason is that it is vulnerable to rogue key attacks in which the attacker chooses his public key depending on the public key of the victim’s signer in order to cancel out the public key of the victim’s signer. The rogue key attack.

## MuSig1

The common defense against rogue key attacks is to add a proof of possession to each public key. That is a zero knowledge proof of knowledge that shows that the owner of the public key knows the corresponding secret key. The contribution of MuSig1 was to avoid the need for proofs of possession. Instead the individual public keys are not just multiplied but there are additional exponents that are derived via a hash function. To create key aggregation exponent `a_i` we hash the `i`th key together with the multi set of all keys.

`a_i = H(X_i, (X_1, X_2))`

The second essential improvement over the insecure strawman scheme is that MuSig1 has a third round which runs before the other two rounds. In that round everyone sends a hash based commitment to their nonce before they reveal their nonce in the second round. The main purpose of MuSig2 is to get rid of this round.

## Why can’t we just drop the commitment round?

Why can’t we just drop the commitment round? If we drop the commitment round we will arrive at the flawed 2 round scheme in the early revision of MuSig1. The simple answer to this question is that when we drop the round there will be known attacks. I mentioned the attacks by Drijvers et al and by Benhamouda et al. But it is insightful to look at why the security proof was flawed.

## One More DL (OMDL)

The security proof of the flawed MuSig1 scheme is based on the One More Discrete Logarithm problem. It is a natural generalization of the discrete logarithm problem. First the adversary gets `k` discrete logarithm from the challenger who is then able to ask for `k-1` discrete logarithm oracle queries. The adversary wins if it computes the discrete logarithm of all `k` challenges. One can see that the ordinary discrete logarithm corresponds to OMDL with `k=1`. OMDL has been used for other interactive variants of Schnorr signatures, for example blind signatures. OMDL is useful in security proofs because it lets the reduction “borrow” DL oracle queries during runtime and only needs to solve challenges in the end. As a side note in the MuSig2 paper we in fact don’t use the OMDL assumption but instead the weaker Algebraic OMDL or AOMDL assumption. We are the first to describe this assumption which is immediately implied by the OMDL assumption. In contrast to OMDL the benefit of AOMDL is that it is a falsifiable assumption. A quick look at the existing literature reveals that essentially all positive security results that are based on OMDL can be based on the weaker AOMDL. In the remainder of the talk we will ignore AOMDL and stick to the well known but stronger OMDL assumption for simplicity. But if you are interested in the details of AOMDL or if you are planning to use the OMDL assumption in the future we recommend that you have a look at our paper.

## Proof Outline (OMDL in ROM)

Here’s an outline of a proof that attempts to prove the flawed MuSig1 scheme is secure under the OMDL assumption in the random oracle model. Given a successful forger `A` there is a reduction `B` against OMDL which first gets a DL challenge `U = g^u` and sets public key `X_1` equal to `U`. Then `B` runs forger `A` on public key `X_1`. Somehow `B` simulates the honest signer without the secret key where the secret key is equal to the discrete logarithm of the challenge (`x_1 = u`). And somehow `B` needs to fork the execution of the forger `A` to obtain the secret key `x_1` from the forgery. Finally `B` outputs the secret key which is also the solution of the first DL challenge `x_1 = u`. The Forking Lemma will take care of the details and the probabilities. At this high level of abstraction there is only a single DL challenge and this outline looks like a normal reduction to DL. OMDL will come to play only when simulating the honest signer. For this step the reduction `B` will obtain additional DL challenges. For each additional DL challenge the reduction gets one DL oracle query for free as long as it is able to solve all additional challenges. In order to solve the OMDL problem the reduction needs to make sure that there is a one-to-one correspondence between DL challenges and DL oracle queries during the simulation. Then the first DL challenge `U` is exactly the one more challenge that the reduction will solve.

## Simulating Signing (OMDL)

We will now see how the reduction can simulate signing without the secret key in the OMDL setting. On the right side we have the insecure MuSig1 scheme. The reduction plays signer 1, the forger is signer 2. For every signing query the reduction gets a fresh DL challenge `R_1` and sends it as nonce to the forger. Then in order to sign without the secret key `x_1` the reduction makes use of the DL oracle. It computes partial signature `s_1` by querying the DL oracle with `X` to the power of aggregation exponent `a` times signature challenge `c` multiplied by `R_1`.

`s_1 = DL(X_1^(a_1.c).R_1)`

In the end the reduction learns the secret key `x_1` and can solve the signature equation `s = x_1.c + r_1` for the DL challenge `r_1`. To understand what can go wrong here we focus on the signature challenge `c`. The forger can choose `R_2` after having seen `R_1` and is therefore able to bias the hash `c`.

`c = H(X, R, m)`

We will see why this is a problem on the next slide. This will not be possible with the initial nonce commitment round in the secure MuSig1 scheme.

## OMDL and Forking Do Not Go Together Easily

What we want is for a DL challenge `R_1` the reduction makes a single DL query to obtain `s_1`.

`s_1 = DL(X_1^(a_1.c).R_1)`

However if the forger is forked after seeing `R_1` and before sending its own nonce `R_2` it can send a different `R_2` which results in a different signature challenge `c’` in the upper execution.

`s_1 = DL(X_1^(a_1.c’).R_1)`

This means for a single DL challenge the reduction has to make two DL oracle queries in order to simulate signing which ultimately prevents the reduction from winning the OMDL game.

## Forking

Since both MuSig1 and MuSig2 support key aggregation without proofs of possession it is not sufficient to fork the execution of the forger only once. Instead the forking lemma is applied twice. First to the random oracle queries for the key aggregation exponent and then to the queries for the signature challenge. This results in four executions of the attacker and in the worst case the reduction may need even 4 DL queries for a single DL challenge.

## MuSig2: How To Fix the OMDL Idea

We will now see how MuSig2 fixes this.

## How Can We Fix This?

How can we fix this? Remember that we obtain one DL query per DL challenge. Remember that the DL challenge is used as a nonce. So the simple answer is that the signer uses 4 nonces.

## Getting the Reduction Four DL Challenges

Instead of sending just a single nonce every signer `i` sends 4 nonces `R’_i`, `R’’_i`, `R’’’_i` and `R’’’’_i` and effectively uses a random linear combination.

`R_i = R’_i (R’’_i)^b (R’’’_i)^(b^2) (R’’’’_i)(b^3)`

The exponent `b` is set by hashing what is essentially the entire protocol input and transcript after the nonce exchange round: the aggregate public key, the message and the nonces of all signers. Note that we don’t simply concatenate all nonces but instead we multiply them. This is a minor tweak that can be ignored for the purpose of this talk. The randomness in `b` will ensure that the resulting linear combination is different in each of the executions and thus the reduction obtains a linear independent equation system that it can solve for the DLs in all 4 involved DL challenges. The simple idea is the main insight of our proof but we note that very careful programming of the involved random oracles is necessary to obtain a full rigorous security proof. For obvious reasons we can’t show the full proof here in the talk but refer you to the paper instead.

## Four Nonces in the ROM

We promised a simple scheme but now we require 4 nonces per signer. The number 4 corresponds to the 4 executions of the forger. The question arises, is this an artifact of the proof technique? The answer is yes most likely since only 2 nonces are needed for MuSig2 in the Algebraic Group model. We don’t go into detail about the AGM proof because it is very mechanical and tedious. Luckily Alper and Burdges independently developed a proof in the AGM of an almost identical multisignature scheme that confirms our results.

## Provable Security of MuSig2

We summarize the security results for a given number of nonces in the following table. With a single nonce we know a practical attack. MuSig2 with 4 or more nonces can be proven secure under (A)OMDL in the ROM. With 2 nonces it is secure under (A)OMDL in the ROM when we additionally assume the Algebraic Group Model. This result is shared with the concurrent [work](https://eprint.iacr.org/2020/1245.pdf) titled “Two Round Trip Schnorr Multisignatures via Delinearized Witnesses” by Alper and Burdges which appears at the very same conference as this work.

## This Work: MuSig2

We finally have a look at this scheme that was developed in the work MuSig2. It differs from the earlier flawed variant of MuSig1 by letting each signer generate 2 and send 2 nonces instead of 1. This is the variant secure in the AGM. Each signer’s effective nonce `R_i` is a random linear combination of its 2 nonces with random exponent `b`. This exponent is the hash of the aggregate public key, the message, the product of all signers’ first nonces and the product of all signers’ second nonces. Each signer then creates a partial signature using their effective nonce.

`R_i = R’_i (R’’_i)^b`

`b = H_non( X, m, R’_1.R’_2, R’’_1.R’’_2)`

`c = H_sig(X, R_1.R_2, m)`

return `(R_1 R_2, s_1 + s_2)`

## Almost Non-Interactive Signing

Why do we bother with the distinction between 2 and 3 rounds if the scheme is interactive anyway? The answer is that it is not only the number of rounds that matter in practice. The first round of MuSig2 can be securely performed without knowing the message `m`. This makes signing effectively non-interactive. At any time that is convenient to the signers the nonces can be pre-shared by executing the first communication round. For example the two ends of a payment channel can pre-share nonces when the connection is established. Then when a message to sign arrives, for example a payment forward, signing is just a single message on the wire. This is a novelty in a DL setting without pairings and it is probably the best round efficiency you achieve without pairings (BLS).

## Recap

To recap, the key technical idea of our work is that every signer uses a random linear combination of multiple nonces instead of a single nonce. A remarkable fact is that this idea appeared concurrently in 3 works. It is great to see that the idea has been independently confirmed. We already mentioned the work by Alper and Burdges. In addition the FROST scheme by Komlo and Goldberg uses the very same idea in the threshold setting instead of the multisignature setting. All 3 results differ in the detail of their schemes and provable security guarantees but a detailed comparison is out of scope for this talk.

## MuSig2

With MuSig2 multisignatures look like ordinary Schnorr signatures which are compact and allow for fast verification. MuSig2 is a practical and simple 2 round signing protocol. The first round can be precomputed without knowing the message `m` so signing is almost non-interactive. MuSig2 has concurrent security under (A)OMDL in ROM for 2 nonces or ROM plus AGM for 4 nonces. If you want to learn more about MuSig2 then have a look at our [paper](https://eprint.iacr.org/2020/1261.pdf).

