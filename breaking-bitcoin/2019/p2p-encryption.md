---
title: Bitcoin P2P Encryption
speakers:
  - Jonas Schnelli
date: 2019-06-08
transcript_by: Bryan Bishop
tags:
  - v2-p2p-transport
media: https://www.youtube.com/watch?v=mcJa1YvzrFs
---
bip324: v2 message transport protocol

<https://twitter.com/kanzure/status/1137312478373851136>

slides: <https://twitter.com/_jonasschnelli_/status/1137389541512351749>

## Previous talks

<https://btctranscripts.com/scalingbitcoin/milan-2016/bip151-peer-encryption/>

<https://btctranscripts.com/sf-bitcoin-meetup/2017-09-04-jonas-schenlli-bip150-bip151/>

<https://btctranscripts.com/bitcoin-core-dev-tech/2019-06-07-p2p-encryption/>

## Introduction

This will be a technical talk. I hope you're prepared for some cryptography. By the way, this now has a bip number as of this morning. This is bip324. I call it v2 message transport protocol. It's not a consensus change, it's purely a p2p network layer change. It's not all about encryption, but mainly about encryption. It's only a building block. It doesn't solve a direct user need, but rather it solves a kind of fundamental thing that will lead to eventually things that we can use as end users.

## Goals of the v2 message protocol proposal

The goal is to add opportunistic encryption, which itself isn't about making secure connections but helping to build secure connections. It has some nice properties and might eliminate the non-detectability of observers. It also eliminates undetectable message manipulation. It's also extendable with various authentication schemes. Also, this is a chance to optimize the p2p protocol which was kind of set in stone when Satoshi made the first client. This proposal is split between encryption and authentication so that we can have new authentication schemes.

## Why v2? What about bip151?

bip151 was proposed years ago, as most stuff in bitcoin development- it's slow. bip151 is kind of dead now. I couldn't alter it, because people have started to implement bip151. It would be unfair to alter it, and then there would be confusion about what version of bip151. So it's dead now.

There are some major differences between bip324 and bip151. I think it makes more sense to call this v2 message format. There's also a new message structure, new service flag, short command IDs. It's not just about encryption.

## Why encryption?

Bitcoin is public, transactions are public, blocks are public. So why encryption? It's all true. But p2p traffic is not meant to be public. Where transactions are originally coming from is data that we don't want to be public. We also know that the bitcoin network is under active surveillance and there are other tools kind of doing that. Encryption with the possibility of authentication may eliminate passive observers on the network. Again, this is a building block. The potential will be brought to the users in layers above this layer.

## Required crypto primitives

This proposal doesn't invent any crypto. There are existing tools out there, like TLS 1.3, tor, and others. What we tend to do is reduce the dependency set. To have something that is stable and controllable with our own stack. Bitcoin Core made sure that OpenSSL is out of consensus and soon out of the code base so that we have a controlled stack of what's running in there. There's nothing bad about running our encryption on top of Tor.

We are using the secp256k1 curve, the same that we use for bitcoin signing. We also use Diffie-Hellman key exchange on the secp256k1 curve. We use a new construct called HKDF which is hashing a hash or hashing a secret to get a key. It's standardized in an RFC implementation, it's super easy. HKDF sha256 L32. We also use ChaCha20 as the cipher as to how we encrypt data. Also, Poly1305 is a fairly old construct and proven which generates the MAC message authentication code.

## Handhsake

So, how does the handshake work? It's pretty simple. When a node connects to another node, it doesn't send a version number. Instead  it sends a 32 byte pubkey. A pure pubkey, no header, nothing else. The responder reads the pubkey and checks whether it starts with a v1 network magic which is a few predefined bytes. If those 32 bytes start with this, then it's considered a v1 connection. This is how it is backwards compatible.

If that's not the case, then it does Diffie-Hellman exchange and it sends back its own pubkey to the other side. This is the handshake for v2. I assume you're familiar with the Diffie-Hellman key exchange technique. These slides will be available later.

At the end, both sides have a shared secret without a man-in-the-middle being able to figure out what that secret is. From that point on, they can enable encryption.

I will not go into the details of this. We will probably not have time to dive into this.

Some of you have asked, why pubkeys are 32 bytes? We are only going to take odd pubkeys. If it's not an odd pubkey during the generation of connection, then you can just negate the private key and generate the pubkey again and you have an odd pubkey. One slight beneficial thing of this is that because if you always send as a first thing, 33 bytes, then it's super easy to identify a bitcoin handshake. It's not a goal of the protocol to make everything random and do censorship resistance, because the port is already revealing that you're doing bitcoin and some other protocol semantics.. but using 32 bytes makes it a little bit harder for analysis tools to figure out what's going on. It's not reducing the security either, so we should do it.

## Session ID and keys

Once we have the Diffie-Hellman secret on each side, then we use HKDF. If you're not familiar with this construct, then just imagine you're hashing the secret in order to generate the keys and a session ID. The session ID has a nice property which I am going to show here. Because it's opportunistic encryption, which means we're not going to authenticate at that layer, a man-in-the-middle could intercept the handshake and could stand between those connections. He's just taking one side and kind of intercepting the handshake as a traditional man-in-the-middle during handshake and intercepting keys on both sides. Without authentication, we can't eliminate this man-in-the-middle. But there's the property of the session ID. Since we generate a session ID of the shared secret, that session ID can be compared. Not that this is practical, but it can be compared. It's like on Signal on your phone, you should verify the cryptographic number with the other person. You should be doing that verification. It would reveal to you if a man-in-the-middle is present, only for a certain percentage of connections. What's really important is that right now on the current bitcoin network, if someone is intercepting bitcoin traffic, there's no possibility to detect that, because we don't have any HMACs. It's not possible to detect if anyone is manipulating or observing packets. With session IDs, it's possible to notice this. Someone observing the network now needs to take the risk that he can be detected, which is very essential, in my opinion, for security.

## Authentication and man-in-the-middle

Peter Todd said back when bip151 was being discussed "Bip151 provides excellent defence against government attackers with MITM capability: you can detect such attacks and change behaviour. This is a huge improvement over the status quo of having no way of knowing if we're being attacked".

## Authentication?

We're usually familiar with certificate authorities like doing an SSL connection. There's a central list of companies and they have certificates and keys. The problem is that this is not something we want to have in bitcoin, like a static list of centralized companies that verify other companies. The other thing we're familiar with is the TOFU concept, which is that once you connect over ssh the first time, you usually get a server fingerprint and you press yes; the idea is that if my first connection is man-in-the-middle then I am screwed, but if I'm intercepted in the future then you can tell. We probably don't want this in bitcoin either; authentication for now is out of scope. There's some good proposals and people are writing them but I think that should be a separate proposal.

## v2 message table

We need to avoid central planning. There's no reason to overhaul the BIP every half-year with a new command. I consider this a static set of messages. Once made, it's static. The short IDs should be decided upfront.

## Make v2 faster and smaller!

Sometimes, when thinking about networking, you want to make everything faster, so you disable TLS or something. Or you disable a VPN because it slows you down. That's often the case, but we found that using encryption in v2 is actually faster than v1. How is this possible?

In the v1 p2p protocol, the messages were double hashed. The structure was 4 bytes net magic, 12 bytes message command, 4 bytes length, 4 bytes double-SHA256 checksum, and the whole packet is at least 24 bytes. The checksum is a double-sha256 hash over the payload and truncated down to 4 bytes. It's a very expensive checksum. Satoshi made that decision... and we can get rid of that.

In v2, we can drop some things and optimize some elements. It's a 3 bytes encrypted length, 1-13 byte message command, a variable length payload, and a 16 bytes MAC (message authentication code) and the whole message is at least 20 bytes. The maximum message size is 8 MB in the v2 protocol.

Before, an INV was at least 12 bytes, but here the INV can be just one byte in the v2 message protocol.

Is 8 megabytes enough for a message type? Absolutely. It doesn't mean you can't send messages larger than 8 megabytes. It's just the maximum packet size; you should split up big messages into multiple 8 megabyte chunks anyway.

## Rekeying

Rekeying is very important. In our scheme, we cannot reuse nonces. So, at some point, ssh at like 1 gigabyte you should use the next key or the next symmetric key. That's why the client in v2 can trigger by a single bit that a rekeying should happen. If it doesn't happen after being requested, then you should immediately disconnect.

## Custom AEAD construct

We have a Diffie-Hellman key exchange, and after that we use symmetric encryption like AES but in our case ChaCha20 which is from [djb 2008][ChaCha-paper]. It's fairly widely used, like on Android, certain TLS connections use it... It's usually pretty fast if you don't have native instructions. If you have native instructions on your CPU, then AES tends to be a bit faster. It matters on low-cost hardware, and on low-cost hardware ChaCha20 is faster than AES. You can pre-compute the random stream and then use XOR operations whenever you need an encrypted byte.

We use a specific form of that scheme because we have figured out how to optimize it for our traffic semantics. Originally the ChaCha20Poly1305 construction was proposed in IETF RFC 7539. Then OpenSSH modified it for their use case. We have taken the openssh version and modified it a little bit. I am not going to go into every detail, but how did we optimize it? You do a ChaCha20 round and you encrypt the length. In the openssh version, they added that the length is encrypted so that it's possible to pad the message and nobody can figure out what was the length of the message. They always have a ChaCha20 round which always produces 64 bytes, but then only encrypt 4 bytes with it. It's like throwing away 60 bytes of computation on every message. Maybe they didn't care, but in our case maybe we should care.

## Performance

I analyzed the performance of the v2 message protocol. Usually our messages are less than 64 bytes, like INV and pongs or something. It's rather important that we optimize for that message size. On average, we use only 2.048 ChaCha20 rounds rather than 3 ChaCha20 rounds that OpenSSH uses. For pruned nodes, the amount of small messages is very high. In my benchmarks, I was comparing optimized sha256 against an unoptimized ChaCha20. Still we can see that on smaller messages, ChaCha20 is significantly faster. Hashing one megabyte takes more time than encrypting one megabyte, it's almost twice as fast on an Intel x64 i7-8700 computer to encrypt rather than hash one megabyte of data.

## Conclusion

We can encrypt traffic, we can make a building block and it's faster and it's less bytes. So I think there's big opportunity to kind of make the p2p network more robust. It's not solving "I want to connect to my home node" in the first place, but it's a step forwards where I can connect to my home node and addnode not just with an IP address but I can really make a secure connection if I want to.

## Next steps

Bitcoin Core has already merged ChaCha20 and Poly1305 into the source code. bip324 needs more review. If you're a cryptographer or know anyone really interested in this, take a look at the proposal and figure it out. The whole AEAD encryption thing is available in an open Bitcoin Core pull request for you to test out and review at least conceptually. We could deploy it as an optional experimental feature.

[ChaCha-paper]: https://cr.yp.to/chacha/chacha-20080120.pdf