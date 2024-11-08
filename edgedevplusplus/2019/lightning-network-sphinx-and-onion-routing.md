---
title: Lightning Network Sphinx And Onion Routing
transcript_by: Bryan Bishop
tags:
  - anonymity-networks
  - lightning
  - routing
speakers:
  - Antoine Riard
date: 2019-09-10
aliases:
  - /scalingbitcoin/tel-aviv-2019/edgedevplusplus/lightning-network-sphinx-and-onion-routing
---
## Introduction

Hi everyone. I am a developer of rust-lightning, it started in 2018 by BlueMatt. I started contributing about a year ago now. It's a full featured, flexible, spec-compliant lightning library. It targets exchanges, wallet vendors, hardware, meshnet devices, and you can join us on Freenode IRC in the #rust-bitcoin channel which is a really nice one.

## Privacy matters

Privacy matters on the blockchain. This is the reason why lightning is taking so much time. We want the privacy to be done right. Whoever can see your payments can basically nudge you. Say I am your landlord and I can see how much you're paid. I can then raise the rents based on seeing the payments. So privacy matters. This is why in lightning we're using onion routing.

TCP/IP original flaw is-- you see both the source address and the destination address. They were thinking about this back in the 70s and 80s. This was RFC 791. Now we have to wonder, is this really all public information? With bitcoin, is it flaw to have like a pubkey being in every output? Maybe, maybe not. Maybe we will be able to solve this with fancy confidential transactions or other kinds of things. But with lightning, we're trying to solve this.

## Off-chain payments with lightning

Payment channels are private. Global public addresses are replaced by private balances between parties involved in payment. You can chain off-chain payments to get scale. Off-chain balances are not published to the chain until closing. This disconnects payment throughput from chain write throughput. Taproot can also be a big privacy boost for lightning too.

## How to avoid leaking payer and payee in lightning?

A public graph of channels combined with plaintext payment instructions would leak positions in the payment route. Anyone can sit in the route and get all of the information about the entire route. Everyone would be able to see where people are in the payments paths, and where payments are going. That's not really desirable.

## Anonymous network studies: Tor, i2p, PIR, ...

There's been a lot of work in anonymity networks like tor, i2p, private information retrieval, etc. They focus on unobservability, anonymous sets, unlinkability, integrity, mixnet vs onion routing, etc.

Tor is the most widely deployed anonymity net. You have plaintext wrapped in the first onion which is wrapped in the second onion and wrapped in the .. and so on. At each onion layer, it gets peeled off and eventually it's at an exit node that unwraps the last layer and sends off the data into the public internet.

## Sphinx onion packet

"Sphinx: A compact and provably secure mix format". I think this is only used on lightning really. It's used in higher-protocols like HORNET and Loopix. BOLT 4 is the lightning implementation of Sphinx.

The basic building cryptographic building blocks are sha256, ECDH which is for deriving shared secrets from parties based on elliptic curve. Then HMAC which is a keyed hash message authentication code. And then ChaCha20 is a high-speed stream cipher.

## High-level view of packet structure

Here's a diagram of the lightning network packet structures.

## Generating shared secrets

Shared secrets are generated through some protocol.

## Sending back errors and failure messages

<https://diyhpl.us/wiki/transcripts/breaking-bitcoin/2019/lightning-network-routing-security/>

## Future protocols

* Trampoline onion packet (indirection routing layer)
* rendezvous routing
* Active message like pay-per-API call, ordered chain of API calls
* Multi-party computation (auctions, lotteries, ...)

I don't know how people are going to use it, but if you're an application developer then maybe you should try to build something with this.


