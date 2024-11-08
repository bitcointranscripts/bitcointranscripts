---
title: 'A2L: Anonymous Atomic Locks for Scalability and Interoperability in Payment Channel Hubs'
transcript_by: Bryan Bishop
tags:
  - research
  - lightning
  - adaptor-signatures
speakers:
  - Pedro Moreno-Sanchez
date: 2019-09-12
media: https://www.youtube.com/watch?v=Uh6Ywxrobzw&t=4480s
---
paper: <https://eprint.iacr.org/2019/589.pdf>

<https://github.com/etairi/A2L>

<https://twitter.com/kanzure/status/1172116189742546945>

## Introduction

I am going ot talk about anonymous atomic locks for scalability and interoperability in payment-channel hubs. This is joint work with my colleagues.

## Scalability

I will try to keep this section as short as possible. This talk is also about scalability in bitcoin. You're probably aware of the scalability issues. There is decentralized data structure recording each transaction in order to provide public verifiability. Global consensus is required, such that everyone checks the whole blockchain.

## Payment channels

To see how this works, see the talk I gave half an hour ago. Payment channel hubs are useful because one cannot open payment channels with everyone in the world. The expectation is that everyone opens a channel with the hub.

## Atomicity in PCHs

One problem with atomicity is that we can't simply trust that the payment channel hub (PCH) will forward a coin from Alice to Carol. There is a need to have atomicity somehow. Either the gateway forwards the payment to Carol if he gets it from Alice, or the gateway can't get the payment from Alice in the first place.

## Privacy and unlinkability in PCHs

Unlinkability is that when looking at the payments between Alice and Carol, the adversary should not be able to figure out if Alice is paying to Carol between other possible disambiguations.

## Interoperability in PCHs

We want to create a PCH payment protocol backwards compatible with bitcoin. It's not an easy task. There's a lot of them like Perun, liquidity network, BOLT, TeeChain, Blind swaps, tumblebit. Tumblebit doesn't work in cryptocurrencies without scripting, like Monero. Also the efficiency of tumblebit can be improved. Blind swaps require Schnorr signatures, which are not yet deployed. TeeChain requires a trusted execution environment like SGX which is a drawback.

## Adaptor signatures

Our approach uses adaptor signatures. A few talks here have explained how adaptor signatures work. We're using adaptor signatures. Just as a recap, it's a protocol where we have two users Alice and Bob and each of them have a private key and a public key. We have an adaptor, which I see as another pair of public and private key. The public half is known to Alice and Bob, and the private part isn't known to either of them in advance.

The goal is that Alice can create a "half-signature" that Bob can only finish by knowing the adaptor skc. If Bob finishes the signature, then Alice learns skc. Here, the adpator is (pkc, skc).

I am calling this a "2-party adaptor signature". If you think about this, this is basically a lock mechanism. It's a protocol where Bob gets something like a signature. He needs to learn something to unlock the coins and get the signature itself. When Bob eventually learns that, he can put as input the private part of the adaptor and the output of this interaction is that he gets the whole signature. Alice will also get the signature and get to learn the adaptor itself. I will call this the "release phase". So first there is a "lock phase" and then there is a "release phase".

* "Threshold scriptless scripts" Scaling Bitcoin 2019 (Omer Shlomovits)
* "Workshop on scriptless scripts" Scaling Bitcoin 2018 (Andrew Poelstra)
* "Anonymous multi-hop locks" NDSS 2019
* One-way homomorphic functions, Schnorr signatures, or ECDSA (building on 2p-ECDSA of Lindell) but also in the talk from Omer yesterday we learned that 2p-ECDSA can be changed, we could use threshold scriptless scripts based on ECDSA. It's really versatile.

## Payment channel hubs using adaptor signatures

The gateway is going to use the same adaptor on both sides. It's both Alice and Bob. Only the gateway knows the private part of the adaptor signature lock. There's a 2-party adaptor signature lock between Alice and the hub and then a 2-party adaptor signature lock between the hub and Bob. This scheme has atomicity and it's the same on both sides.

The problem comes from the privacy point of view. The gateway learns that the same adaptor is used on both sides. The unlinkability property means that there's a gateway who sees the same adaptor on the left and the right, which is enough to link that Alice is paying Bob. So unlinkability is trivially broken by this proposal.

## A2L: Protocol overview

We first do the setup between the gateway and Bob with an 2-party adaptor signature. We allow Alice and Bob to introduce their own randomness. The gateway runs the lock with Bob. He gets a half-signature. But as you can see, the gateway will also include the encryption which can only be decrypted by the gateway, of the adaptor itself. At this point, Bob does two steps. The first step is that Bob takes this adaptor this public key and randomizes it with his own randomness, sends it to Alice, and Alice randomizes it as well with her own randomness. This is the adaptor we use between Alice and Bob. This is randomized by both of the parties Alice and Bob. The second thing that Bob does is that if you think about it, the secret key for this is not known to anybody because it's composed of three elements that are distributed among the three parties. We need to somehow reconstruct it between the three parties. Bob gets an encryption of the secret key, and includes the randomness from himself inside, this is possible because the encryption has homomorphic properties, which allows him to include his randomness. Then he sends it to Alice and Alice does the same. Because this was encrypted by the gateway, the gateway can decrypt it and run the release part of this two-party adaptor signature. The hub gets the signature and Alice learns the signature.

The adaptor is being randomized between Alice and the gateway, and this randomization is sent out on the protocol in terms of the encryption itself.

Atomicity is held, and unlinkability is not breached because the adaptor looks different on the left and the right. It's secret sharing between the three of them.

## Discussion

A2L achieves atomicity and unlinkability. This has been formally proven in the UC framework. 2-party adaptor signatures can be instantiated with one-way homomorphic functions or Schnorr or ECDSA. This is backwards compatible with bitcoin. It's also compatible if bitcoin adopts Schnorr signatures.

If you have noticed, it only requires signature verification and timelocks instead of HTLCs. This means that this is interoperable with scriptless cryptocurrencies like monero.

This protocol is good for fungibility because the protocol results in a valid signature that is identical to any other transaction. Other information, like encryptions, are not included in the transaction itself that hits the blockchain.

## Evaluation

Either with Schnorr or ECDSA adaptor signatures are both more performant than tumblebit. With A2L schnorr, we have a computation overhead of 70 ms and 8x faster than tumblebit. With A2L ECDSA, we are 110 ms or 5x faster than tumblebit. A2L Schnorr in ocmmunication overhead is 3.5 KB, which is a 95x reduction, or with A2L ECDSA it's 5 KB or a 65x reduction from tumblebit. nThe number of operations and communication overhead are asymptotically reduced. Tumblebit uses cut-and-choose. Size of exchanged messages grows non-linearly in the security parameter.


