---
title: 'Plasma Cash: Towards more efficient Plasma Constructions'
transcript_by: Bryan Bishop
tags:
  - research
  - sidechains
  - proof-systems
speakers:
  - Georgios Konstantopoulos
date: 2019-09-12
media: https://www.youtube.com/watch?v=Uh6Ywxrobzw&t=2799s
---
Non-custodial sidechains for bitcoin utilizing plasma cash and covenants

<https://twitter.com/kanzure/status/1172108023705284609>

paper: <https://github.com/loomnetwork/plasma-paper/blob/master/plasma_cash.pdf>

slides: <https://gakonst.com/scalingbitcoin2019.pdf>

## Introduction

We have known how to do these things for at least a year, but the question is how can we find the minimum changes that we can figure out to do in bitcoin if any on how to explore the layer 2 space in a better sense rather than just accepting that lightning network is the dominant solution? When I talk about layer 2, I mean scaling solutions that have realistic assumptions. Multisig is not sufficient. I don't want to assume that the path you're working with doesn't collude with someone else. Lightning might be okay.

## Related work

* Plasma
* Plasma on EthResearch forum
* NOCUST
* CoinCovenants using SCIP signatures
* Preventing consensus fraud with commitments and single-use seals
* one more

## Scaling

One idea is to make transactions smaller or use off-chain transactions. Or bigger blocks, but I won't talk about that.

## Sidechannels considered harmful

Sidechains operate under the basic idea that you lock some funds on the original chain, then you provide some proof on the other chain, and somehow the same asset you lock doesn't get created on the other place. In the PoW sidechannel situation, you mint BTC when you transfer it over, and then you burn the BTC when you transfer it back to mainnet. The problem with this is that there's no succinct SPV proof-- they all have tradeoffs.

One possible problem with sidechains is that they might not allow you to withdraw your coins because the fedpeg multisigners might not like your withdrawal.

## Statechains considered harmful

It's similar to sidechains, you have a multisig with this entity, but if you are here, it can collude with any previous owner of the coin which is also not good. We don't want that. So how can we do better than that?

## Plasma Cash tradeoffs

Plasma Cash has been proposed for some time. It has some specific tradeoffs. Similar to the statechains construction, you have one party called the operator. It can be one person or many people. He can't steal, but they might be able to censor transactions. The feature of this scheme is that this party puts a constant-sized commitment on the layer 1 chain he wants to use. He's able to "finalize" an arbitrary number of transactions in one on-chain transaction.

There are no overcollateralization requirements like in lightning. There's no need to sign to receive a payment. Also, can receive funds without on-chain transactions. There is no notion here of inbound liquidity.

There are fixed denomination transfers. If I deposit 5 BTC into this, then I can only move 5 BTC around. It's safe only under liveness assumption, and it has O(1) stale state fraud proofs. You have to watch the chain every some number of days to make sure that somebody can't steal the money, like the owner of the coin or some collusion with the operator. Also, it requires high base chain quality, so that dispute resolutions can reliably get included. The chain has to be uncongested. These are our security assumptions.

## Plasma cash

Instead of having two separate sytsems, the operator commits each block root to the "parent chain". It creates a merkle root or some other accumulator whatever one you want to use. It takes the merkle root, and it publishes it on the root chain as we call it.

I need to prove the whole UTXO history to the party receiving coins. I need to prove that the money was not spent in between, also.  We need to prove exclusion of a payment in the previous history. The history I need to transfer grows linearly with the number of blocks. There are approahces to solve that problem, but that's not the focus of this talk.

Similar to lightning, when you make a deposit, you lock funds on layer 1. If you want to take your money out, you spend it from the deposit script to an exit script and it has all the dispute resolution logic. After some amount of time, the money is yours. There's also a spend to a fraud-proof script to exit.

An on-chain entity can challenge and spend the money back to the deposit script.

We use a sparse merkle tree. There is a transactoin hash at each UTXO\_ID index. You can make merkle inclusion proofs using the sibling pair-level merkle proof. For a proof of exclusion, you basically prove that you included zero in that tree. Prove that coin 7 didn't move in this block is basically a proof that in this block, a hash of 0 was included, for that serial number.

There is an invalid history challenge construction where you can provide proofs from the sparse merkle tree.

## Covenant designs

My favorite is OP\_CHECKSIGFROMSTACK. There's OP\_CHECKOUTPUT (MES'16). OP\_CHECKOUTPUTHASHVERIFY but it doesn't let you do a turing-complete state machine. There's also OP\_SECURETHEBAG (Rubin 2019). Also OP\_PUSHTXDATA (Lau 2017). Also another idea is to use pre-signed transactions which recently Bryan Bishop published a spec for it, where everyone signs on all the possible states and you trust that everyone holds the necessary signatures and trust that you can be safe. It doesn't require any changes to the protocol, however it doesn't scale to many many participants.

## Implementing Plasma Cash on bitcoin

We want a state machine. Every coin is a state machine.

## Merkle proof verification

I need merkle proof verification like VerifyIncluded(UTXO\_ID, ROOT, TX\_HASH, PROOF). This is similar to OP\_MERKLEBRANCHVERIFY from maaku.

There's also CHECKSIGFROMSTACKVERIFY where you would use BLOCK\_NUM, ROOT, SIG. You need to check that the operator signed on the block that was published, because bitcoin doesn't have a global state like ethereum. So this would concatenate them, hash them, then check if the operator actually signed on this blob. If they have signed on this, and the merkle proof verification passes.

You also need to verify that the transaction format is valid.

EnforceSpentTo is also required, which enforces UTXO is spent to the next state. I want to be able to go the next state, but also go back to the previous state in case someone challenges me. You can use PICK to dynamically construct the covenants with the scriptSig args.

## Summary

We have off-chain fixed-denomination payments. We can compress any amount of transactions to O(1) commitment on layer 1. The operator can censor, but he cannot steal under the liveness assumption. This requires restrictions on spending outputs, and merkle proof verification, and another thing.

Plasma Cash unlike lightning has exploding history, but checkpoints or accumulators might fix this. On the other hand, plasma cash can receive payments when keys are cold, and it's capital efficient with collateral, and no on-chain transactions are required to transact. One downside might be that plasma cash requires fixed denominations.

An accumulator or checkpoint might be able to compress all the inclusion proofs.

