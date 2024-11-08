---
title: Federated Chains, Sidechains
transcript_by: Bryan Bishop
tags:
  - sidechains
speakers:
  - Greg Sanders
media: https://www.youtube.com/watch?v=WbSaGEfuRlw
date: 2018-10-05
aliases:
  - /scalingbitcoin/tokyo-2018/edgedevplusplus/sidechains-and-federation-models
---
<https://twitter.com/kanzure/status/1048008467871666178>

## Introduction

The name "sidechain" is overloaded. My favorite private sidechain is my coach. That's my private sidechain. Hopefully I can explain the high-level concepts of a sidechain, at a 10,000 foot view. What are these? What do they give you?

## Sidechain components

First you need a blockchain. It has to be something that builds a consensus history. The state of the ledger has to be recorded, or the account model, or whatever you're doing. As a digression, we need not just timestamping but proof-of-publication, proof-of-non-publication to allow us to have this shared history. It has to fulfill the proof-of-publication requirement. It's not necessarily the main chain, it's something connected to another chain. Thus it's a sidechain. It's not just a blockchain that's not bitcoin (because then litecoin would be a sidechain), but it has a communication channel that allows it to move value to and from the parent chain.

A user wants to take his bitcoin, put it into a new system, and puts it into the new system, operates in that new consensus system and at some point asks for the money to be moved out of the sidechain. Meanwhile, the parent chain doesn't have to know anything about the sidechain semantics of the system or the consensus building history requirements. I'll go more into that later. There's different ways of doing each of these components.

## Blockchain

A blockchain has consensus history, and then it has consensus rules. You can have arbitrary consensus rules in a sidechain system. You can have faster block times, DAG instead of a tree, you can do privacy, scaling, and so on. And you don't need backwards compatibility. Most of these systems that are deployed have confidential transactions, confidential assets, and the root stock sidechain is based on the ethereum virtual machine model so you move bitcoin from a UTXO model to an account model. It doesn't need to be compatible at all.

## Blockchain making

Who makes the history? It's miners. Commitments are put inside both blocks, thus allowing this history to be tethered to the bitcoin blockchain. Miners get to vote to make blocks on the sidechain. The other version of sidechains is where you have block signers. Instead of miners, you have block signers, where there's a specific set of people that are allowed to create new history in the sidechain

## Sidechain mining

You get to retain the dynamic set of signers. In bitcoin, miners can come and leave. This allows robustness at the cost of things like needing proof-of-work which is energy-intensive. I left out proof-of-stake because that's an entirely separate topic. Assuming you have some fancy script or some opcode that allows this to happen, the consensus changes for the sidechain don't have to occur on the main chain. But it raises miner requirements to stay profitable in the case that the sidechain is successful. There are some schemes to allow even non-participating bitcoin miners to get fees from the sidechains, called blind merged mining. Paul Sztorc has some schemes for this. You have to think about the analysis and game theory about this and think about who's being profitable when it's being created.

One problem is that if the sidechain is not mined enough by enough miners, then it's easily attacked, there's reorg vulnerabilities, and so on.

An example of a merged mined blockchain that is merge mined against bitcoin is namecoin, which was the DNS replacement sidechain which as far as I know doesn't have any use. BitDNS was also proposed early on in bitcoin history.

## Federated blocksigners

It's a closed set of signers. It could be dynamic, although not in the same way. It's permissioned: to enter the set of blocksigners, you must have permission from the signing set that was there originally. There's no way to break your way in; you can't manufacture a miner and just start mining or whatever, you have to ask permission to be added or removed from the federation.

In general, this looks like an m-of-n signature scheme.

There's no energy requirement to sign multiple histories, so as a result it's more easy to forge histories. You have to trust the miners to not double spend.

There are no consensus change requirements on bitcoin for this, and no raised requirements for bitcoin miners to keep up with fee revenue. It relies, though, on opsec of fixed and possibly-known entities.

You can do simple consensus algorithms that don't have the same reorgs problems that Bryan talked about earlier today.

## Blockchain hybrid model

Rootstock has a hybrid model that starts as a federated model, but as miners start doing commitments into the sidechain, but the weight of the vote gets slid over to miners. Optimally, ostensibly for their design, the optimal thing to do is merged mining and no block signers.

## Sidechain features

We talked about block making on a sidechain, and now let's talk about sidechain features and how funds are moved in and out of the system. At a high level, funds are locked on the bitcoin network, and then unlocked on the sidechain. After the user is done participating in the sidechain, the same thing happens in reverse.

This can be thought of as a contract: I put some bitcoin into sidechain A, and whoever is controlling these I don't want htese funds to move until someone has a valid claim to take these funds. In each case, the pooled funds is a big slush funds. If 100 people put in 1 BTC each, then it doesn't matter that I get my bitcoin when I want to leave, only that I get 1 BTC it could be any of the bitcoin.

Who enforces this contract? It's the miners on the bitcoin blockchain, and the federated wallet or watchmen. At Blockstream, we call watchmen- they are watching for people moving funds in and out of the bitcoin blockchain.

## Miner contract enforcement

You can use proof-of-proof-of-work, it's a compact proof that the money you put into this lock stayed in the lock and wont be reorged out due to some short-term 51% attack. It's secure against reorgs. Paul Sztorc's drivechain model which was released recently- they have very long peg-out periods on the order of months. I'll get back to why it's so long in a moment. You can have shorter as well, but then your security buffer is shorter.

In bitcoin, miners that do a 51% attack can't take your coins other than censoring a transaction or something.

## Federated enforcement

You can use [pay-to-contract](https://arxiv.org/pdf/1212.3257.pdf). You take a bunch of pubkeys, you tweak them by the hash of the public key appended to a script, and this script is something you will use to spend on the other side, the scriptpubkey. User directly gives funds to the federation wallet, using pay-to-contract (p2c). Before segwit, you could have only up to 15 participants in the multisig federation. Post-segwit, it's actually larger, it's n-of-67 multisig. But standardness rules; so you could only get up to 67 members in the federation. With fancier math, you could do unbounded, but many rounds requirement--- you could use pairing-based cryptography tricks and do m-of-n Schnorr signature but using ECDSA. The consensus algorithm would have to do more back-and-forth communication which increases time and latency and so on. For federated enforcement, you would do a batched withdrawal from the sidechain every few minutes on a schedule.

## Putting it all together

There's a lot of parts and pieces to build a sidechain. These pieces require careful selection, though. There's a lot of hype at the beginning about letting the miners do everything, like merge mine all the things. But you have to think about what you're trying to solve. Who do you trust? Do you trust miners? Or do you trust some companies? Do you trust other people? There are tradeoffs everywhere. I'm partial to the federated model, but I also like proof-of-work.

There are also some failure modes to think about. Miners can censor federation funds. If miners detect it and they don't like it, then they can censor it. Also, miners can steal merge-mined funds. Also, more subtly, a merged-mined sidechain can degenerate into extension blocks. Before I said that sidechains have no consensus backwards-compatibility requirements... but if everyone is using a sidechain then it almost de facto becomes bitcoin, and if the miners cheat on the sidechain then the block should be invalidated on bitcoin, and at that point it's basically an extension block. Full nodes on the bitcoin network would then be required to run those new rules, and this might add consensus risks that you otherwise wouldn't have wanted.

## References

* <http://blockstream.com/sidechains.pdf>

* Non-interactive proofs of proof-of-work <https://eprint.iacr.org/2017/963.pdf>

* pay-to-contract <https://arxiv.org/pdf/1212.3257.pdf>

* <https://github.com/ElementsProject/elements>
