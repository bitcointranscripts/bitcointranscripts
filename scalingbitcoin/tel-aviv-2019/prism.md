---
title: 'Prism: Scaling Bitcoin to Physical Limits'
transcript_by: Bryan Bishop
tags:
  - research
speakers:
  - Vivek Bagaria
---
## Introduction

Prism is a consensus protocol which is a one-stop solution to all of bitcoin's scaling problems. The title is 7 to 70000 transactions per second. We have a full stack implementation of prism running and we were able to obtain 70,000 transactions/second. Before we get started, here are my collaborators.

This workshop is on scaling bitcoin so I won't spend any time justifying why we would want to scale bitcoin. So let's talk about performance.

## Bitcoin performance

Bitcoin has been running for over 10 years, and the important properties are security, transaction throughput and confirmation latency. Bitcoin has only 7 transactions/second. Confirmation latency is hours. It has very good security, but low throughput and it's time intensive.

## Physical limits

Is 7 transactions per second the best we can do? Is it 70? 700? Is there a natural way to scale bitcoin to these limits? Let me start with the physical limits.

Bitcoin runs on the internet. The most important parameter of the internet is the network capacity. It is typically the capacity each node has available. The second important property is the speed of light propagation today. It's typically the time taken for the peers on the internet to talk with each other, and let's say that's roughly one second.

It's easy to see that the transaction throughput of any protocol is upper-bounded by the network capacity of the system. The confirmation latency is fundamentally lower bounded by the delay due to the speed of light constraint.

Can you design a protocol which has the same security of-- obtains throughput all through the network capacity and confirmation capacity all the way up to.. okay?

## Prism work

In this work, we deconstruct the bitcoin protocol into individual components and then we scale the individual components to get Prism and close to the physical limits.

## Bitcoin protocol

In the bitcoin protocol, there is a block that follows various rules. Every block gets proposed to the network. About every 10 minutes, there's a new block proposed to be added to the ledger. Every 10 minutes, we have a new set of transactions being added to the network. Because we are mining at a low rate, like one block every 10 minutes, this low mining rate is the main reason for the limited throughput of the system.

After proposing, there's a voting process. Every block is voting on its parent block to confirm the transactions in the ancestor blocks. Let's understand this with an example. Say I give you 1 BTC, and you pay for a car, and this transaction is in this block. Can you immediately confirm the transaction and hand me over the keys? The answer is no, because Satoshi said so basically. This statement is straight out of Satoshi's whitepaper now called Satoshi's tables which says that if you confirm a transaction after 1 block deep then as little as 30% of the hashrate of the network can revert your transaction with unacceptably high probability.

## Decreasing the block interval

Increasing the mining rate makes the blockchain a mess because there's a lot of orphan blocks that get produced. The simple approach of just scaling the mining rate and still keeping around the longest chain rule, wouldn't work.

There have been many DAG approaches proposed which try to modify some of the rules. What we do instead, is we take a slightly different approach.

## Deconstruct bitcoin and scale

So first we deconstruct the bitcoin protocol, and remove it, then we scale the system. Every block in bitcoin has two rule, one is that it proposes transactions and then second it confirms transactions by voting on parent blocks. Instead of performing one structure that perhaps both of these.

What, if instead, the system maintains two separate chains. One chain does the proposing and the other chain does the voting.

You select the votes along the longest voter chain, and then order the proposer blocks by votes. This is a very simple protocol. It enjoys the same performance guarantees as bitcoin, like the 50% security guarantee, and the same latency and throughput. We have decoupled the bitcoin protocol without losing any of its properties.

Instead of having one voting chain, we have many voting chains. Having many voting chains gives fast confirmations. The way that the ledger is constructed in this protocol is that for every level in the proposal tree, propose a chain, select a block that has a maximum or the most number of votes, and that makes it to the ledger. Let's see how that helps you confirm transactions faster.

## Fast confirmation

Confirming with one deep is not good in bitcoin because the adversary has a high probability of being able to revert the transaction. In Prism, the question is do you have to wait for each of these votes? We have 1000 voter trees. Let's see happen when each of the voters-- wait just one block. Each vote can be changed with a probability, but changing all of them requires--- you have to change more than 500 votes to change the proposal. The property of changing more than 500 votes is much smaller than 0.0006 and this is by simple law of large miners.

So we have designed a protocol which can confirm transactions when voting blocks are just one block deep, and it has the same guarantees as bitcoin with 25 deep.

This is similar to a technique using machine learning where you take a lot of weak classifiers and you make a strong classifier.

## Prism

This is how we scale or improve the confirmation latency of a layer 1 protocol. Decoupling the proposing and voting rule, and ... achieves... A vote is just confirming the hash of a proposed block. It's a confirmation.

Next, we re-apply this idea for the proposing blocks. When the proposer blocks, don't store the proposer transactions themselves. The proposer block merely just references those transactions. Now this system achieves high throughput because you mine transaction blocks while mining each of the chains at a very low rate. The reason why this protocol achieves high throughput and fast confirmation is because this part here is responsible for the security, and since each of the chain is mined at a low rate, there's no forking. All the throughput comes from the voting chains.

## Security theorems

We prove a few theorems. For throughput, one says that an adversary with less than 50% hashrate, Prism achieves some amount of throughput. And for latency, one says that for adversary with <50% hashrate, Prism confirms transaction with guarantee 1 - epsilon where epsilon is defined as ((some formula)) latency.

* Bagaria et al., "Deconstructing the blockchain to approach physical limits"

## Demo

<http://bit.do/prismdemo>

