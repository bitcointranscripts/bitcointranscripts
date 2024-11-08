---
title: Atomic Multi-Channel Updates with Constant Collateral in Bitcoin-Compatible Payment-Channel Networks
transcript_by: Bryan Bishop
tags:
  - research
  - lightning
speakers:
  - Pedro Moreno-Sanchez
date: 2019-09-12
media: https://www.youtube.com/watch?v=Uh6Ywxrobzw&t=1022s
---
paper: <https://eprint.iacr.org/2019/583>

<https://twitter.com/kanzure/status/1172102203995283456>

## Introduction

Thank you for coming to my talk after lunch. This talk today is about atomic multi-channel updates with constant collateral in bitcoin-compatible payment-channel networks. It's a long title, but I hope you will understand. This is collaborative work with my colleagues.

## Scalability

We're at Scaling Bitcoin so you're probably not suprised that I think bitcoin has scaling issues. It's a decentralized data structure called blockchain where we store every transaction that happens. Visa has a higher transaction rate and yet uses an entirely different system so this indicates that bitcoin is broken.

There are various solutions proposed such as on-chain consensus tweaks, DAGs, sharding, off-chain, payment channels, lightning network, bolt, perun, liquidity network, raiden network, etc.

## Background on payment channels

I am pretty sure that you're all familiar with payment channels, but I am going to describe them again anyway. This is based on a commitment transaction that is funded only after the rest of the transaction tree is pre-signed. Once the channel is open, Alice can now pay Bob. This allows payments over the channel.

## Payment channel networks (PCNs)

Since you can't open channels with everyone, the alternative is to use a payment channel network where payments are routed between different payment channels using a multi-hop protocol. To prevent fraud between the source and the destination, there are some mechanisms to enforce a timeout or justice transactions. Also, fees are paid to routing nodes on the payment channel network

## Hash timelock contracts (HTLCs) for multi-hop payments

A hashed timelock contract is used to enforce that a transaction is valid only once the middle nodes learn certain information that only occurs in the event that the payment has been correctly routed. A timeout mechanism is used so that after some amount of time, the middle nodes and all other participants are able to reset the state to recover from the failed payment attempt. Bob can only spend the coins if he learns the preimage to the hash function. This is the only cryptography we need for a multi-hop payment network. All of the coins in the route path are locked up for some time period. The timelock on one side needs to be shorter than the timelocks on the other side. You have to make sure there is enough time to claim the coins before they expire under the assumption of a failure. The more hops we have, the longer the timelocks need to start with.

## Security and privacy issues in existing payment channel networks

There's some security and privacy problems in HTLC-based payment channel networks.

## Expressiveness and collateral management in payment channel networks

There are two open challenges. One is that in the current PCNs, we have restricted expressiveness and functionality. Current bitcoin-compatible PCNs restricted to single path-based payments. Also, current PCNs require high collateral meaning that coins need to be locked for a long time.

What we want here is to improve expressiveness beyond paths. Atomic multi-path payments are a first step towards expressiveness beyond single path-based payments. We would like to achieve full expressiveness, in other words we want to support arbitrary paths with any number of senders, any number of receivers. This allows new applications like crowdfunding, channel rebalancing, netting, and other applications.

The second goal is to improve how the collateral is actually managed in PCNs. Each payment of k coins along a n-channel path requires locking coins at each hop. Also, each user has to lock her coins for a time lock where the delta is the time to safely close a channel. This means that coins can be locked for a very long time. There's too much timelocking of coins here. The timelock value depends on the position along the path.

## Griefing attack

This opens the network to some problems, including a griefing attack. The attacker can create a payment that pays to himself. The adversary is able to lock up coins among the path nodes. He is able to lock up coins in n-2 channels from honest users. He only locks in one channel for a certain amount, but he has an amplification effect including a time amplification factor. Also, the attacker can use several paths.

## Goal: Constant collateral

Our goal is that the time that how long coins are locked at each channel should not be dependent on the position, but it should be a constant number, and it should not be dependent on where you are in the path between the sender and the receiver. This reduces the amplification factor of the griefing attack.

This is feasible in ethereum-based PCNs like Sprites ("Sprites and state channels: payment networks that go faster than lightning"). They conjectured in that paper that it was not possible for bitcoin. They suggested that bitcoin would require modifications, like "constant collateral would be burned".

The main result of our work is atomic multi-channel updates where we show it is possible to have a constant collateral factor, and it's possible with current bitcoin script. We don't need to add any opcodes or additional operation to bitcoin.

## Atomic multi-channel updates (ACMU)

I'll give an example of a payment between two users. Alice has a channel with Bob. She wants to transfer 8 coins (out of the 10 she has). Bob wants to transfer 7 of the coins he has, out of 30, with Carol. First, there is a setup phase between Alice and Bob. Later, there is a setup phase between Bob and Carol. Alice and Bob split their money into two separate multisig contracts. One is the amount that they want to involve in this protocol, and the other is the amount they want to keep.

Next, phase 2 is where they make a lock for Alice and Bob where if something goes wrong the users are able to get their money back. They take the money they locked here, and they spend it to another account that belongs to them, but with a timelock. Now we have time delta to perform whatever protocol we want, and if something goes wrong, then at time delta then they would be able to get their money back. Now that they are happy and they know they can get their money back, they enter the third step.

The third phase is consume, which is where they send the ... to spend you need money in a fresh account, which does not have any money yet, this is key towards atomicity. These are the coins used to pay to the receiver, in this case Bob. They don't have the money yet, and it can't be put in the blockchain yet. This is the key towards atomicity. After this, every channel has a transaction that spends from the funded address to the next hop (in this case Bob).

The last step is to fund these addresses, atomically. We have to make sure that all of these addresses get money at the same time, or none of them get money at the same time. Phase 4 is where each pair takes the channel which was part of the game, and they fund all of these fresh addresses at the same time with a multi-output transaction.

You can see there's two possible states in the channel now. One is the setup plus a lock. The other is setup transaction, enable transaction, and consume transaction. We have to make sure that only one of the two can be enforced. What we do is to make sure that these can be ... some time in the future. For that, we do a transaction that basically takes the money of the .... This is a phase 5 transaction called disable. It sends the coins back to the users themselves. We can revoke the enable transaction and send the money back to fresh addresses or the channel between Alice and Bob.

## Security and privacy analysis

AMCU achieves atomicity. In particular, if the coins at one channel are ready to be sent to expected receiver, then all channels ready to forward payments. Otherwise, coins remain at a channel owned by original owners.

AMCU does not achieve relationship anonymity. Every user in the path collaborates with each other.

Instead, it is constant collateral (coins locked constant time), it's backwards compatible with current bitcoin scripting language, and it has accountability where it is possible to show a proof of misbehavior.







