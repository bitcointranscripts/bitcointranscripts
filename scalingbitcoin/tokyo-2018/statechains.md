---
title: 'Statechains: Off-chain transfer of UTXOs'
transcript_by: Bryan Bishop
tags:
  - statechains
speakers:
  - Ruben Somsen
---
I am the education director of readingbitcoin.org, and I am going to be talking about statechains for off-chain transfer of UTXOs.

<https://twitter.com/kanzure/status/1048799338703376385>

## Statechains

This is another layer 2 scaling solution, by avoiding on-chain transactions. It's similar to lightning network. The difference is that coin movement is not restricted. You deon't have these channels where you have to have a path and send an exact amount. There's some synergy with lightning; it's not a replacement for lightning.

It has some similarities to federated sidechains as well, however the difference is that the federation doesn't have full control over the coins. You're not handing the coins over to a group that can take the coins. It's a little bit close, we'll get into that. It's mixed in terms of security between lightning and federated sidechains, but maybe closer to the federated sidechains.

One unique limitation is that you can only move a full UTXO. It has some advantages by doing this.

## What does this build on?

It builds on Schnorr signatures, adaptor signatures, eltoo and graftroot. This is thanks to Pieter Wuille, Andrew Poelstra, roasbeef, gmaxwell, cdecker and many others. It's not specifically to bitcoin-only, but it does require these components to be in there. Graftroot is optional but a nice to have.

## Overview

What we're trying to achieve is having one bitcoin and moving it in a channel from it being locked up between Alice and Bob to Alice and Charlie and Alice and Darrel. We want to change the ownership off-chain and we want to guarantee redemption. We want the last person in this chain to be able to get the coins. It's facilitated by the statechain entity, called by "A" in this presentation. "A" can collude with the prior owners. "D" might be the owner but the statechain entity can collude with the prior members in the statechain. If the statechain entity does that, then the cheating will be provable and it will ruin the reputation of the statechain entity.

## Statechains in detail

You have Bob locking up the coin with the statechain entity. If you send this to the bitcoin blockchain, who actually owns it? It depends on what the timelock transaction says- you either have it in a script or off-chain depending on the system you use. If you have this offchain transaction going from AB to B then that means Bob is the owner. We're utilizing eltoo here. It's a more complex script, it's "AB or (B in 5 days)".

Can ew just transfer this from Bob to Carol? We kind of can, but it's not great. We can just say, we can change this off-chain transaction and give it to Carol and Carol has no power over it, and Bob and Alice can change their mind at any time, and Carol wants to send this on-chain right away to get the money.

Instead, we introduce something called a transistory key X. This key is what Bob locks up his money with the statechain entity.. He has key B and he has key X. When we create this transaction, we pass on the transitory key from Bob to Carol. So now both Bob and Carol know the private key of X.

## The role of the statechain entity

The role of the statechain entity is that they promise to only cooperate with the last owner, even after a state transition or transfer. Here, the statechain entity is just one person, but you could use Schnorr signatures and have it be an actual federation like 8-of-10 or things like that. We might be talking about a single key, but really think of it as a federation.

The federation keeps a statechain or multiple statechains listing every UTXO in its control. You don't want duplicate history. You want to know which UTXOs the statechain claims to control. Every time a UTXO moves on the statechain, there needs to be a signature. When the money moves from Bob to Carol, the statechain needs a signature from Bob stating that this is what Bob wanted. There is some key X under control of the statechain, and when we transfer the money, we have an off-chain transaction to... on the statechain side, Bob signs a message saying I want this money to go to Carol and Carol receives the off-chain transaction that allows her to redeem it on-chain if she chooses to.

We are using eltoo: you can string these transactions together, you can publish the intermediates or you can publish the latest one. Thanks to eltoo, you can use transaction cut-through.

## Problem: Who goes first?

If we just give this to Carol, then on the statechain then it looks like the statechain entity is cheating and giving the money to Carol on-chain. On the statechain there's no signature from Bob. That's no good. Other way around, same problem. It looks like Carol has received the money but she has no signature there...

## Scriptless scripts

So we utilize adaptor signatures and scriptless scripts, which has been explained to you before. Basically, you give an incomplete signautre to all the parties involved. As soon as one of the signatures gets completed on the statechain side, together with Bob and Carol's help, once this signature hits the public-- the statechain is a public ledger-- once you see this publicized, that's the moment when Carol learns the full transaction on the bitcoin side.

## Security model

Moving coins always requires the permission of the statechain entity (typically a federation), and a transitory key holder (who held the UTXO). However, the statechain entity must cooperate with the last transitory key holder and if they do not do so then there will be evidence of fraud. With adaptor signatures, we're always guaranteeing that there was a signature that was supposed to move.

## What could go wrong?

The statechain entity could obtain a bunch of transitory keys somehow, and then he could proceed to steal the money and this will be provable fraud that everyone will be able to see. This will prompt everybody whose transitory key has not been compromised to withdraw on-chain, and they are able to do that because they have a valid on-chain transaction. As many transitory keys can be obtained and potentially stolen in the case that the statechain entity is malicious.

Even though the transitory key assumption is kind of weak, you can definitely if you try hard you could get those keys... the statechain entity doesn't actually have control over the coins. If they get hacked, that's not enough. You need to hack the statechain entity and also get the transitory keys.

Imagine there's some court order to freeze the coins or confiscate the coins. The statechain entity cannot actually do that or help you with that because they do not have the full set of keys.

## Swapping

One of the downsides was that you're only able to send a full face-value UTXO. What if I want to pay someone with less than the money I have? Well, you can swap. If you have 2 BTC, then you swap with someone who has 2x 1 BTC. You can do this atomically, with adaptor signatures. It's possible to do this with bitcoin-bitcoin or bitcoin-litecoin and cross-chain swapping, same process.

## Microtransactions

Anything smaller than an economically viable UTXO cannot be transferred in the statechain. If you do that, and they want to redeem it on chain, they will receive nothing because the fees are too high. So there's a limit related to the actual fees. If the statechain entity wants to charge fees then that's a big problem. Ideally, you want to solve this without adding trust to the system. The statechain entity does not have any control over any coins whatsoever. Maybe you could trust them for small amounts? Ideally we want nothing like htat; we want the statechain entity to have no direct control over coins.

## Lightning channels on top of statechains

We could create a lightning channel on top of the statechain. Instead of sending from Bob to Carol, we can send to Bob-Carol. So now there's a channel between Bob and Carol. The creation process would be the other way around; you would create the lightning transaction before making the statechain transaction. You now have a lightning cahnnel on top of the statechain.

This allows channels updated together with multi atomic swaps. Small channels can allow up to the smallest UTXO. In the uncooperative case where you have to close your channel, it's actually the same cost as eltoo, the same number of transactions.

Splicing-in and splicing-out is all off-chain here. You can close channels, reopen channels, add coins to channels. It's no problem because it's already off-chain.

## Potential use cases

Obviously, you could send payments off-chain. You could utilize this as a platform between lightning network and the bitcoin blockchain and have an easy way to open, close channels and have splice in/out channels. Also this could facilitate betting. If you want to do a bet, on lightning it's sort of complex, it requires either the entire channel or the entire hops you're going through to have the money locked up throughout the bet or you have to put another channel on top of the existing channel and it gets messy. You'd rather not do that, and create a new channel with the person you're betting with. Normally you would have to do that on-chain, but now you can use statechains. And statechains has good synergy with discreet log contracts or a regular multisig bet.

Another interesting use case is that because we have these UTXOs not moving on-chain, it means that if there's a fork, those coins are still inside of that UTXO. So even if you're moving that UTXO from person to person, you're literally moving every potential fork that happened during that time simultaneously. With graftroot, we can allow an easy way to get your coins out. If you want to redeem those coins and get out of the statechain and into the bitcoin blockchain, or maybe there's some bitcoin hard-fork... assuming we have graftroot, the statechain entity could give a graftroot signature to the final owner when they want to get out, and using the graftroot signature they could go on and if there's replay protection they could create the necessary signatures to withdraw from any chain they want. For an ETF where the question is which coins are going to be honored during a hard-fork, you could honor them all if you wanted to do it like this. Same goes for exchanges, but they might be less interested in a system like this.

## Further topics

Currently, the statechain system is interactive. To send money from Bob to Carol, Carol also needs to provide a signature. There might be a way to make it non-interactive but this requires more thinking and some tradeoffs.

We could also use a hardware security module to transfer transitory keys using attestation. Everyone has touched this transistory key. We could insert a hardware security module and transfer the key through the HSM and as long as the HSM is secure, which I think is a big assumption by the way considering we have seen SGX hacked and things like that- so maybe more for future purposes, but then there's literally no way the statechain entity can cheat because as soon as the transitory key moves, if Bob moves to Carol, then the transitory key gets deleted on the hardware. Since you always have htis redemption transaction you could send to the bitcoin blockchain, you don't have to store that on the HSM hardware. You still have access to the bitcoin because you store that transaction outside the HSM in case it breaks.

Also, I talked about graftroot providing withdrawals allowing the redemption of coins from multiple forks.

You could also succinctly store and relay statechain (per UTXO). All of the coins always move in a straight line, at least from the view of the statechain entity itself. Even if you add a lightning channel there, since we're using Schnorr, it looks like a single signature so the statechain entity doesn't even know there's a lightning channel there. If you control a UTXO, you have to keep track of that history. You have ot know that everything that happened up to that point, that nothing funky is going on in history, keep track of everything and making sure the statechain entity is not cheating-- there might be some ways to do that in a way that doesn't require getting the entire history, perhaps you could summarize the history somehow.

Another interesting one is that we could make the statechain entity not actually know what they are signing, if we were to utilize blind signatures. We could make it so that you're locking up money with the statechain entity with some transitory key X, and even though you're doing that, the statechain entity doesn't need to be aware of what coins they own. They just blindly sign whatever you tell them to sign- Bob goes to the statechain entity and sign a message please, but really it might be signing an off-chain eltoo-style transactoin that allows them to redeem the money. The statechain entity will not really be aware they are doing that, in the blind signature scheme. When a recipient receives money, they will need to verify all the blind signatures. The statechain entity has to publish the blind signatures they have made, and this is the trust here that they have made only those signatures and none others. Every time someone receives the money, they have to unblind the signatures themselves to verify whether the correct things were signed- you don't accept the money if that's not true.

paper: <https://goo.gl/RWQ4ue>

## See also

<https://diyhpl.us/wiki/transcripts/scalingbitcoin/tel-aviv-2019/edgedevplusplus/statechains/>
