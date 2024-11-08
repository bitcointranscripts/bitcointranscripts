---
title: Lightning Network
transcript_by: Bryan Bishop
tags:
  - lightning
speakers:
  - Tadge Dryja
date: 2016-06-30
---
I am going to talk about blockchain scalability using payment channel networks. I am working on Lightning Network. It's currently being built in bitcoin but it can support other things. One of the fundamental problems with blockchain is scalability. How can you have millions of users and rapid transactions?

Fundamentally, the blockchain is shared. You can call it a DLT but it's really a copied ledger. Every user has a copy. When you're at a conference and everyone is using the same wifi AP, it's pretty slow. You really want a segmented network where everyone is plugged into their own switch.

Global consensus is important but inefficient. HOw do you segment the network without losing the properties of the blockchain? Well, the way to do it is with payment channels. It's not quite a cryptographic primitive yet, but I think in the future people will consider it a crypto primitive.

The way that it works is that in the case of bitcoin, you send it to a shared multisig address. Then you share signatures that lay claim to those coins. You keep sending messages back and forth offline. That alone is complex, I don't have time to go into how that works. This allows you to establish channels where you send one output to the channel, then you can move money back and forth. For payments, you can't have just one person, you need to be able to pay multiple people.

How do you explain this to multiple people? Cryptographically, Alice has a channel with Bob who has a channel with Carol who has a channel with Dave. Alice wants to use the existing channel rather than creating a new channel when she wants to pay Dave, because to do otherwise would cost money. Dave makes a random number R. Payments contingent on knowledge of the preimage of the hash. So you make a cascading chain of these obligations. As long as there's a path, payments can be routed.

If you would like to learn more about this, then please ask me more after the talk.
