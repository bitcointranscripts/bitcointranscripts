---
title: 'TxProbe: Discovering bitcoin''s network topology using orphan transactions'
transcript_by: Bryan Bishop
tags:
  - topology
  - research
speakers:
  - Sergi Delgado-Segura
---
<https://twitter.com/kanzure/status/1171723329453142016>

paper: <https://arxiv.org/abs/1812.00942>

<https://diyhpl.us/wiki/transcripts/scalingbitcoin/coinscope-andrew-miller/>

## Introduction

I am Sergi. I will be presenting txprobe. This is baout discovering the topology of the bitcoin network using orphan transactions. There are a bunch of coauthors and collaborators.

## What we know about the topology

I want to start by talking a little bit about what we know about the network topology without using txprobe.

When we talk about topology, we know a few things beforehand. We know the number of nodes that are reachable, and the location of them based on IP address geomapping. But when we talk about topology, at the end of the day, we're talking about graphs. Just having the geolocations isn't a map. We need the edges. The edges are hidden by design. This opens some discussion between whether these edges should be hidden or not. Should we have an open or closed topology?

## Hidden topology

Let me motivate why we decided to do this analysis.

An open topology could ease different types of attacks. There's transaction deanonymization and network-based approaches like eclipse attacks. Having an open topology would make the network more vulnerable. The current approach of Bitcoin Core is to keep the topology hidden.

Having a closed topology has some disadvantages. Is the network decentralized? Are there supernodes in the network that are controlling the traffic like doing information withholding or censorship? Are there parts of the network that can be easily partitioned by removing a few nodes? This is basically why we decided to kind of have some kind of network topology health metrics to have some way to know if the network is the one we want to have.

Security by obscurity is probably not the way to go.

## Topology should look random

We wanted to know how nodes choose peers in the network. They choose 8 outbound connections by default. It's psuedorandomly chosen from addrman. No pair of nodes are in the same /16 (ipv4). There's also 117 inbound connections by default with no IP restriction.

This is the approach of Bitcoin Core and also all the forks of bitcoin these days.

## Background

Okay, that's enough motivation or overview of the network. But as I was saying in the beginning, this study is based on orphan transactions and transaction propagation. We have to talk about transaction propagation, orphan transactions and double spending.

## Transaction propagation in bitcoin

Right now, the way that transaction propagation works-- Gleb is going to be talking about his improvements-- but here's how it works right now. When a node receives a transaction and it is validated, it gets into the local mempool. Eventually, this transaction will get propagated to other nodes on the network. The goal is to get these transactions to be included in blocks.

The first thing that a node would do is to be to announce the existence of the transaction to his peers. So he does an INV announcement message, and then the other node asks for the data with get\_data and asks for the data. There will be a 2 minute window here where Alice has to reply. If she doesn't do so, Bob cancels the request. Otherwise, he receives the transaction back. Later on, this is going to be one of the key things we're using for txprobe.

## Orphan transactions

Orphan transactions are a little bit different from normal transactions. Orphan transactions are one where the reference UTXOs are unknown. It's spending from phantom or unknown transactions. Let's say that our node receives a transaction that spends from a known UTXO, so no problem. But our node receives a transaction with a UTXO being spent that we don't know about.

They can't be validated, so they are stored in a separated data structure known as MapOrphanTransactions or OrphanPool for short. We're not able to completely validate this transaction because we're missing the inputs.

Another important thing we're going to be using is that if we try to offer this transaction back to the node, so the node is just storing the transaction and we offer it again, he's not going to reply back. That's really important because it's different from what happens with normal transactions. This is what is going to help us with knowing about edges in the network.

## Double spends

Double spending transactions are quite straightforward. It's a second transaction spending the same coins. If we send a double spend to a node, the node will only accept the first transaction but not the second.

## Basic topology inference technique

So now we can build a topology inference technique. We need two nodes, and three transactions that look like the following. Also we need an observation tool like coinscope. We have a parent transaction, a flood transaction that conflicsts with the parent, and the parent has a child called a marker transaction. You can use any kind of modified nodes that can connect to lots of nodes and send messages out of order and so on, but we used coinscope.

## Positive inference technique

So the first thing to do is connect our node to two separate nodes. We will assume that the mempools are empty, just for the sake of simplicity. So we send one transaction to Alice and one transaction to Bob. We assume our transactions arrive at the same time, which we will fix later. At some point, those two nodes are going to try to send their transactions between each other. But this will fail because it conflicts. Later, we send the parent. Alice has the parent. So at some point, she will decide to send that parent and child along to Bob. But the problem is Bob didn't have the parent. So for Bob, this is going to be an orphan because he doesn't have the parent and Alice doesn't send the parent.

## Negative interference technique

Consider the same scenario, but Alice and Bob don't share an edge. We can see that the only difference of having an edge and not having an edge is that when we have an edge, the orphan transaction gets into the pool, and when we don't have an edge, it doesn't get into the pool. The only thing missing now is to ask Bob about that transaction. If Bob asks about the transaction, then he doesn't know about it. So there's no edge. On the other hand, if he doesn't reply, then that means he knows the transaction. The only way he could have known the transaction since we only sent the transaction to Alice, is for them to share an edge.

## Not that easy

It's not going to be that easy. That works with two nodes. But if you add a third node to the picture, it's going to break, right? Imagine a link between Alice and Bob through Carol.

There's something we can do to fix this middleman. If we're able to force Alice to not send an INV to Carol, then all the messages are never going to be sent to Carol so the marker transaction will never make it through Carol to Bob. So how can we do this? We can do an old technique called invblocking which was introduced by Andrew Miller and his coauthors in a paper.

## Required properties

We need to achieve three properties to make this scheme work. We need isolation, synchrony, and efficiency.

Isolation property: once we send some of the transactions to one node, we want to make sure those transactions stay in that node and only that node.

Synchrony property: assume that both transactions go there at the same time. We don't want to have to time the things. We want to make sure the trnasactions get there and don't get overridden.

## invblocking

If we send an INV message to all the nodes in the network, or at least the nodes that we want to prevent transaction propagation through, then they are going to start the timing I told you about at the beginning. It's a two minute window. They ask about the transaction. If any of the other nodes tries to send a message to them, those messages are going to be queued until the information expected is delivered.

This means that we have a 2 minute window where we have the isolation property and the synchrony property. Cool.

## Simplified txprobe

Once the network has been invblocked, let's see a simplified topology of the network. So this way, ew can guarantee that Bob will accept the flood. If we ask all the network about the market transaction, then we can see Carol knows about the market transaction so there's no edge...

## Txprobe protocol overview

So we choose a target node, create parent, marker and flood transactions, INVBLOCK the network, send flood to all connected nodes but target, let flood propagate, send parent to target, send marker to target, let marker propagate, request marker back from all node sbut target. Then do this for every node in the network. This is where the efficiency thing comes from.

## Txprobe costs estimation

In a network of 10k nodes, that will take about 8.25 hours to run. The cost will be about 5 sat/byte which will be about $20-30. It can be reduced a lot because you don't care about the transactions getting into the blockchain or not. You can almost always get this down to $0 if you plan cleverly.

## Data validation

We decided to do some validation on testnet not mainnet. We ran 5 Bitcoin Core nodes as ground turth. Our precision or recall by checking how well we can infer the ground turth nodes connections. Over 40 trials and with 95% confidence, our precision was 100%, and recall was 93.86% - 95.45%.

## Testnet topology

We basically drew the graph of testnet by running some graph analysis over it. Here we can see how the size of these nodes represent a grid, and the color is community unfolding algorithm. The graphs we were able to draw, have higher community structure than a random graph of the same size and same properties. The modularity was higher than expected too.

## Conclusions

Even though the code was written in a way that was supposed to make a random network, the networks we end up having are not quite as random. We can't extrapolate the results to mainnet because the incentives for running a testnet node and a mainnet node are different.

Is the goal to have a hidden topology as the design goal, or are we trying to achieve transaction privacy with that property? Maybe dandelion would be a better solution for that, which doesn't imply a hidden topology protocol design goal.
