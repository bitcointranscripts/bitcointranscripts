---
title: Developing secure Bitcoin contracts using BitML
transcript_by: Bryan Bishop
tags:
  - research
  - contract-protocols
speakers:
  - Stefano Lande
date: 2019-09-11
media: https://www.youtube.com/watch?v=-gdfxNalDIc&t=5542s
---
paper: <https://arxiv.org/abs/1905.07639>

<https://twitter.com/kanzure/status/1171695588116746240>

This is shared work with my collaborators and coauthors.

## Smart contracts

I am sure everyone here knows what a smart contract is. It's a program that can move cryptoassets. It's executed in a decentralized environment. Generally speaking, we can say there's two classes of smart contracts. A smart contract is a program.  While in blockchain like bitcoin, smart contracts are cryptographic protocols. This effects how we can reason about a blockchain; bitcoin has many more security proofs for script than ethereum.

As a consequence, though, programming a smart contract on ethereum feels easier because of high-level danger languages like Solidity. While on bitcoin, you can only work with the script language. You have to get creative when thinking about writing scripts.

There's also a difference for automatic verification. There are many tools that can apply standard verification techniques to verify contracts. Still, in bitcoin, you have to build complex cryptographic proofs usually in academic papers.

Can we get the best of both worlds? Can we build another language that supports for automatic verification and can also be deployed on a blockchain?

This slide is to give you an idea of smart contracts on bitcoin and their complexity. This example is a hash commitment. It's a small game where either a hash preimage is revealed, or an absolute timelock timeout lets another key spend.

## Languages for bitcoin scripts

There's a few languages for formalizing bitcoin scripts, like Balzac, miniscript, ivy (chain), and simplicity. Say we use these kinds of languages to build a language for cryptographic protocols, and then compile down to bitcoin transactions. It's not entirely easy to use though.

## BitML: Bitcoin modeling language

We designed a high-leve language for smart contracts on bitcoin, it's called bitcoin modeling language or BitML. A contract can be a choice between one or more contracts. We have contracts that are either withdrawal that transfers the whole balance, split which splits the balance between concurrently executed contracts, or we have A : D which means wait for A's authorization, we have after t : D which means wait until time t has passed, then we have put x . C which collects deposits x at run time. Finally, we have reveal a b ... if p . C where we reveal secrets a, b, and p is a predicate we can express on those secrets.

## A basic example

Say Alice wants to buy something from Bob's online store. The payment contract would say if Alice is satisfied, she sends bitcoin to Bob, otherwise Bob refunds her. The contract has a precondition saying that Alice must pay bitcoin to this contract.

## Mediating disputes (with oracles)

We can use an oracle that acts as a mediator in the contract. So we can build a contract that includes escrow. It's the same contract as before, but it has two more branches. These branches can be applied unilaterally either by Alice or Bob to activate the contract for resolving which involves the oracle. Some payment goes to the mediator for his service, and then the bitcoin goes either to Alice or Bob depending on the mediator.

## Time commitment in BitML

The time commitment requires Alice to deposit a bitcoin, and commit a secret that we call little a. The contract has reveal little a and withdraw A. In the second branch, which is active after time t has passed, then withdraw B meaning Bob can get the bitcoin.

## Compiled time commitment

BitML features a compiler to turn contracts into sets of bitcoin transactions. Executing these equates to applying the sum of these to the blockchain. In this example, either Alice or Bob can redeem the coins, based on different conditions. We need the signatures of both Alice and Bob. These signatures are exchanged during this situation in the contract. Before the contract hits the blockchain, you setup the transaction tree and sign it before you fund it, thus no player can refuse to sign after funding which would be bad.

## A two-players lottery

Time commitment is useful for more involved contracts like a two-player lottery. The precondition of the contract requires each player to choose a secret and deposit two bitcoin for collateral. The contract is a split between three subcontracts. One is a time commitment for Alice. The other is a time commitment for Bob. Then there's another one. The lottery is active after both players reveal the secret. If the secrets are different, then Bob wins. If the secrets are identical, then Alice wins.

This contract has a problem because it's extremely unfair to Alice. She can't guess Bob's entropy because Bob can use arbitrarily high amounts of entropy. So we constrain Bob to using a value of zero or one, so an honest player has at least a 50% chance of winning the lottery. Bob can commit to this secret. He will for sure win the lottery because of probability, but he will lose the collateral in the time commitment.

## Compiler security

How can we be sure that the BitML compiler doesn't introduce security vulnerabilities during compilation? One of our main results is that our compiler is computationally sound, so we can trust the compiler. We can trust the compiler, but can we trust the developers of smart contracts. Are they going to make errors when they design contracts?

## Verification

We have a way of doing automatic verification of contract properties. We can verify both contract-dependent properties (expressed as LTL formulae) and liquidity (funds are never frozen in the contract).

## BitML toolchain

We have a secure analyzer that can check the properties. There's a compiler that turns from BitML to a transaction then to standard bitcoin transactions. There are also benchmarks and tool demos. We showed some lotteries in the demos. There's a correlation between the number of players, the number of transactions, and the verification time. In particular, you can see a big jump in the number of transactions in the 2 player lottery and we were limited because scripts had to be max of 520-bytes, so we needed to use more than one step and because of that the verification time exploded but in other cases verification is a matter of seconds at most.

In all of these use cases, the transactions are standard and are limited to 520 bytes of length.

## BitML wishlist

To conclude, I want to talk about some future developments of BitML that would make it more useful in practice. We're open to any type of collaboration regarding BitML. If you're interested, please talk with me.

We want to overcome the fact that BitML is not "bitcoin complete" and it can't express every bitcoin contract. For example, a contract is fixed at compile time. We should be able to use sighash modes to let escrow express contracts like escrow funding where we don't care who adds the money, anyone can add money to a BitML contract in that case.

We want to explore relative timelocks so that we can express time constraints relative to the last BitML case that was executed.

We're also working on dynamic stipulation of subcontracts, which would allow BitML to express payment channels.

We are currently working on executing BitML contracts off-chain because in the current execution model, each BitML step corresponds to a transaction that will change. This doesn't scale well, because a complex contract can require dozens of transactions on-chain. We want to move off-chain and have participants verify correctness of execution.

Finally, we would like BitML over taproot. This would exploit forthcoming MAST and Schnorr signature proposals. Unexpected script branches remain off-chain, and this is more space efficient and increases expressivity (520 bytes limit). It's also private, so BitML contract execution won't hit the blockchain.
