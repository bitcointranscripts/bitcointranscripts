---
title: Self Reproducing Coins As Universal Turing Machine
transcript_by: Bryan Bishop
tags:
  - research
  - contract-protocols
speakers:
  - Alexander Chepurnoy
---
paper: <https://arxiv.org/abs/1806.10116>

## Introduction

This is joint work with my colleagues. I am Alexander Chepurnoy. We work for Ergo Platform. Vasily is an external member. This talk is about turing completeness in the blockchain. This talk will be pretty high-level. This talk is based on already-published paper, which was presented at the CBT conference. Because of copyright agreements with Springer, you will not find the latest version on arxiv.

The general question of scalability is how can we do more with less until we can do everything with nothing? We can already do smart contracts in bitcoin. But we want to do more. How can we do more without spending much effort? There's some research in the community about aggregated signatures. This is another direction I'd like to propose, which is how to have more complex contracts without sacrificng much.

## Questions

Can we achieve Turing completeness without jump (or equivalent) opcodes? Do we need a general purpose programming language? Can we do it in the utxo model we have in bitcoin? And if we can do turing complete computations on the blockchain, then how practical is that?

## Outline

I will talk about turing completeness in blockchain environments, then scripting language pre-requesities, and so on.

## Turing completeness

The question is, what is turing completeness in the first place? Turing complete system is a system which can emulate a universal Turing machine. It's a system that can run any algorithm or any computation. We have many turing complete models. If you have a program in a Turing complete system like a random access machine which is about a modern personal computers, alright so, if we are switching to another Turing complete system like building circles or a system to you consider later.. so you don't have explosive growth or exponential growth in your program length, so you have some reasonable overhead switching from one Turing complete system to another. And any Turing complete system can emulate another Turing complete system, and can emulate a universal Turing machine system.

Blockchain requires constant block validation time. It needs to be basically constant. There's some very strictly limited propagation time, and validation time has to be limited and has to be very restricted.

A popular belief is that for turing completeness on the blockchain, you need a general purpose language like with jump instructions, loops or recursion.

But imagine a version of ethereum where there is a gas limit per block and all the state changes are reversed after transaction script execution (and payment amount is not dependent on the program) then this new ethereum version is not turing complete.

## Bitcoin: boxes, registers, scripting

I'm going to show how to make a bitcoin-like turing complete system, called bitcoin plus. In bitcoin, we have a notion of outputs and unspent outputs usually... let's switch to a more general term, a transaction is spending some boxes or some coins. A transaction is creating new boxes. In addition to monetary value and a spending condition or restriction condition, we allow for some number of arbitrary typed general purpose data sets. Let's assume that there is a register mandatory, r0, which is called monetary value... r1 is guarding script, r2 is general purpose, and r9 is general purpose too. So now we have some data in the coins.

The scripting language needs to be able to do basic arithmetic operations like bitcoin script already does. We need if-then-else clauses. We need cryptographic primitives like bitcoin. Array declaration (predefined size) and access operations. And context data- such as height, self, inputs, and outputs. Unlike bitcoin, we are going to add some context data. When we're validating a transaction, there is some context. In bitcoin, we can ask for amount of time, we can access current blockheight or blocktime. In addition to height, there's "self" in our proposal.

## Rule 110 cellular automata

One of the most simple turing-complete systems is rule 110 by Stephen Wolfram. It's the simplest one-dimensional cellular automata. It was proven 15 years ago that this rule 110 is turing complete.

* "Universality in elementary cellular automata" <https://git.io/vj6ew>

Use transaction chaining to share memory between the transactions. <https://git.io/vj6rX> This can be done with constant block validation time, with a relatively minimal scripting language. We're not doing much, but this allows for running arbitrary computations on the blockchain.

## Is this practical?

For even simple computations, rule 110 string could be billions and billions of bits... so it doesn't give you much, since you can't run large programs like that on the blockchain. And the programs can't run in any reasonable time. What I think is important to show is that this correspondence, this possible correspondence, to be set between input and output, the possibility to set conditions on outputs, dependent on input state, and also possibility to get it over the program itself... so we can, many, practical things, such as demurrage currency, crowdfunding, authenticated states, decentralized exchanges, oracles that authenticate the UTXO state, and so on.

<https://github.com/ergoplatform/ergo/blob/master/papers/yellow>
