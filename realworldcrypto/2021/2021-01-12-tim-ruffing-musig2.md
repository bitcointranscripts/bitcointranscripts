---
title: 'MuSig2: Simple Two-Round Schnorr Multi-Signatures'
transcript_by: Michael Folkson
tags:
  - musig
date: 2021-01-12
speakers:
  - Tim Ruffing
media: https://www.youtube.com/watch?v=DRzDDFetS3E
---
MuSig2 paper: <https://eprint.iacr.org/2020/1261.pdf>

## Introduction

This is about MuSig2, simple two round Schnorr multisignatures. This is joint work with Jonas Nick and Yannick Seurin. Jonas will be available to answer questions as I will be of course.

## Multi-Signatures

The idea that with multisignatures is that `n` signers can get together and produce a single signature on a single message. To be clear for this talk when I talk about multisignatures what I mean is n-of-n signatures and not the more general setting of threshold signatures where you can have a threshold `t` that is smaller than `n` and have something like a t-of-n signatures. The focus of this talk is n-of-n.

## Multi-Signatures in Bitcoin

The motivation for our work is multisignatures for use in Bitcoin and cryptocurrencies. They make it very easy to organize shared ownership of Bitcoin. This has applications in the secure storage of coins but also in more sophisticated applications such as payment channels, think of the Lightning Network or federated sidehchains and so on. As soon as you have multisignatures in Bitcoin you can build a lot of interesting applications on top of them.

## Schnorr Signatures in Bitcoin

The context for our work is the hopefully upcoming introduction of Schnorr signatures in Bitcoin. The idea here is to have onchain support for the verification of Schnorr signatures. These are simple ordinary single signer Schnorr signatures. One motivation to have Schnorr signatures instead of ECDSA, what is currently used in Bitcoin, they allow for easier construction of advanced signing protocols. Once we have Schnorr signatures we can build multisignatures and other interesting primitives, for example threshold signatures or even blind signatures. We can run those protocols in an offchain manner. This layered design is pretty nice because first of all we keep the consensus layer simple. The only thing we do there is introduce verification of Schnorr signatures. Remember the consensus layer, this is the hard thing to change in Bitcoin. We only do a small change there but then we can run all of our interesting applications on top of this change. The second thing is if the only data that ends up onchain is a Schnorr signature or a Schnorr public key this is also great for privacy because it hides the fact that we are running our advanced protocols. If you only see a Schnorr signature in the end you can’t tell if you’re using a multisignature scheme in the background. This is great for privacy too.

## Multi-Signatures That Look Like Ordinary Schnorr Signatures

In order to make that work what we need is a multisignature scheme that has the property that the output of the scheme looks like an ordinary Schnorr signature.

`SchnorrVerify(pk, sig, m)`

(`pk` is an ordinary Schnorr public key obtained via non-interactive public algorithm. `sig` is an ordinary Schnorr signature obtained via interactive signing protocol with n signers.)

This has two parts to it. The first part is of course creating the signature. Here we need an interactive protocol that we can run with our set of n signers. But we also need to care about the public key.

`pk = AggKey(pk_1,… pk_n)`

Here we need some method to be able to get a bunch of public keys of individual signers and be able to aggregate them into a single public key that again looks like a single normal Schnorr public key. In order to be practical we also want this algorithm to be non-interactive and public. Let’s try to construct this.

## (Ordinary) Schnorr Signatures

First let’s have a look at Schnorr signatures again. We are in the discrete logarithm setting so the secret key is a scalar, the public key is the corresponding group element `g^x`. The signer draws a secret nonce (`r`),  computes the public part (`R = g^r`). Then uses this to compute the Fiat-Shamir style challenge by hashing the public key, the public nonce and the message (`c=H(pk, R, m)`). And then the signer solves this challenge by giving the element `s` which is the secret key times the challenge blinded by the secret nonce (`s = x.c + r`). The signature is just R and s (R,s). Verification is very similar in a sense. It recomputes the hash as a challenge (`c = H(pk, R, m)`). Then it checks this main equation here in terms of public elements (`g^s = X^c . R`). If you look at this main equation it is very nicely linear. You could say it is linear in s, linear in X and linear in R. Of course this holds for the public part as well as for the secret part because those are homomorphic. This nice linearity forms the foundation of every advanced Schnorr signature protocol.

## Strawman Multi-Signatures

If we want to build multisignatures from this idea we first need a key aggregation method. Let’s say we have two signers, the public keys, `pk1` and `pk2`. The simplest thing we can do for these public keys is to multiply them. We get the aggregate key `pk = pk1.pk2`. When it comes to the interactive signing protocol the idea is that both signers contribute their shares of the nonce. Both signers send their public nonce (`R1` and `R2`). Then we can multiply those nonces to get the combined nonce (`R1.R2`). We can compute a single combined challenge and then every signer can solve this challenge on their own using his nonce. (`c = H(pk, R1.R2, m)`) In the end what we will get is a Schnorr signature which looks like `R1.R2` and here we get `s1 + s2`. This is just an ordinary Schnorr signature `(R1.R2, s1+s2)`. The protocol is functionally perfectly correct, it produces a Schnorr signature but don’t do this at home because it is not at all secure. There are multiple reasons why this is not secure. The first reason is rogue key attacks which have been known for decades where one of the signers chooses his public key depending on the public key of the other signers. This has been dealt with in other works. For example in MuSig1, I call it MuSig1 so as not to confuse it with our work MuSig2.

## MuSig(1)

The recent and neat defense against rogue key attacks is to instead of only multiplying the public keys, have some additional exponents `a_1` and `a_2` here which are derived via a hash function.

`pk = pk_1^(a_1) . pk_2^(a_2)`

`a_i = H(i , pk_1, pk_2)`

This is already enough to defend against rogue key attacks and we don’t need to care about this further. Another thing that MuSig1 needs to introduce is a third round. This is a pre-commitment round where the individual signers first send commitments to their nonces before they reveal the nonces. This is a commit and reveal protocol. This is to get security in parallel sessions. If you dropped this round then the protocol becomes vulnerable to attacks based on Wagner’s algorithm. This pre-commitment round was already [introduced](https://cseweb.ucsd.edu/~mihir/papers/multisignatures.pdf) in 2006 by Bellare and Neven at CCS. They have many attempts to get rid of this round in some protocols proposed but all of these attempts have been shown to be broken. It was an open problem how to get rid of this round. In this work this is exactly the thing that we tackle.

## This Work: MuSig2

In our protocol, MuSig2, the key aggregation looks exactly the same as MuSig1, we don’t modify this.

`pk = pk_1^(a_1) . pk_2^(a_2)`

`a_i = H(i , pk_1, pk_2)`

But instead of having this pre-commitment round what we do instead is let every signer send two nonces, let’s call them pre-nonces for now.

`(R’_1, R’’_1)` and `(R’_2, R’’_2)`

The randomness here is again derived via a hash function.

`R_i = R’_i (R’’_i)^b`

`b = H(pk, R’_1R’_2, R’’_1R’’_2, m)`

This is pretty similar to what we do above here, it is not exactly the same but it is a similar idea. The rest of the protocol is exactly the same.

`c = H(pk, R_1R_2, m)`

return `(R_1R_2, s_1 + s_2)`

We compute the combined challenge and the signers can send their `s` values. Then we get a signature. As you can see this is a very simple protocol. The only changes from the MuSig1 protocol are in the blue text. It is still simple, we just send one group element more and we have one exponentiation more here. But this is a very practical protocol. We still get concurrent security.

## Almost Non-Interactive Signing

Now you can ask if you still need to run an interactive protocol is 2 rounds so much better than 3 rounds? Interactivity is bad so it doesn’t really matter if you have 2 or 3 rounds. My answer here is that MuSig2 is even nicer because it has the property that the first round can be performed without knowing the message to sign. This makes signing effectively non-interactive because you can pre-share the nonces. For example if you have a Lightning channel between 2 participants you can pre-share some pre-nonces when you set up the channel. As soon as a message arrives that you want to sign, signing is just an additional round. In fact if you have 2 parties it is just one additional message. This property is a novel property in a discrete logarithm setting without pairings. I claim you probably can’t do better than this. It would be a major breakthrough to get a fully non-interactive scheme without pairings. If you have pairings then you can use BLS and everything is nice. But this is not the setting that we work in.

## Key Technical Idea

To wrap up, our key technical idea is that every signer uses a random linear combination of multiple pre-nonces as a nonce. This is the right place to mention that interestingly this idea was discovered independently by three different groups. There is the FROST [paper](https://eprint.iacr.org/2020/852.pdf) by Komlo and Goldberg and there is a [paper](https://eprint.iacr.org/2020/1245.pdf) by Alper and Burdges. All work in slightly different settings. For example FROST is in the more general threshold setting. They all have slightly different provable security guarantees but they all discovered the same key idea to use multiple pre-nonces to obtain the 2 round scheme.

## MuSig2

To conclude, MuSig2 is a multisignature scheme where signatures look like ordinary Schnorr signatures. That makes them compact and the verification is fast. It is a very practical protocol and it is simple, it is 2 rounds. In fact you can pre-compute the first round without knowing the message which makes signing almost non-interactive. For provable security we prove the security of this protocol under concurrent sessions in the random oracle model (ROM) plus Algebraic Group Model (AGM), under the One-More Discrete Logarithm (OMDL) assumption. If you have this combination of ROM plus AGM plus OMDL you can get the security proof for the version I’ve shown you with 2 pre-nonces. Interestingly if you want to drop the Algebraic Group Model (AGM) you can still get a security proof but then you need 4 pre-nonces. There is an interesting story to tell here but of course I don’t have time to do this. If you are interested have a look at our [pre-print](https://eprint.iacr.org/2020/1261.pdf). Thanks for your attention. I am happy to answer your questions.

## Q&A

Q - Why do you call it multisignature and not threshold signature for the threshold access structure with 2 parties? What is the difference between multisignatures and threshold signatures?

A - I mentioned on one of my first slides, in the academic space when you say multisignature, this is what people call n-of-n. You have a group of n signers and all need to be present and willing to sign to obtain a signature. With threshold signatures you still have a group of n signers but in order to produce the signature you only need a subset of size t of those n signers.

Q - I think the question was about the 2 user case. If there are only 2 users is there a difference?

A - If there are only 2 users there’s probably not a difference. You could have a weird 1-of-2 scheme but I don’t think this is particularly helpful. Let me note that our scheme works for arbitrary n. The example I had on the slides was for 2 parties.

Q - If you wanted to do t-of-n this generalizes pretty naturally as long as t is small?

A - There is the concurrent [paper](https://eprint.iacr.org/2020/852.pdf) by Chelsea Komlo and Ian Goldberg, the FROST scheme. This is in the threshold setting. It has the same idea of using multiple pre-nonces to get the 2 round scheme in the threshold scheme. We think our provable security guarantees are a little bit better than this scheme but it should be possible to marry these two papers together and get a t-of-n multisignature with our provable guarantees and our key aggregation method. All of this should be possible. There are a lot of possible design decisions you can make there.

Q - If you have a n-of-n scheme you can always build a t-of-n scheme by looking at all n choose t subsets as long as n is small. That could also work pretty well. None of these techniques will apply to ECDSA? This is a strict benefit of Schnorr over ECDSA?

A - This is true. This exploits the nice linearity of Schnorr signatures. ECDSA is kind of designed to break this linearity. Multisignature protocols for ECDSA can be pretty cumbersome.

Q - The move to Schnorr in Bitcoin is a very welcome development.

A - Yes.

