---
title: Ant routing for the Lightning Network
transcript_by: Bryan Bishop
tags:
  - lightning
  - routing
speakers:
  - Ricardo Perez-Marco
date: 2018-07-04
media: https://www.youtube.com/watch?v=nmqniwbwCg0
---
Decentralized anonymous routing algorithm for LN

<https://twitter.com/kanzure/status/1014530761398145025>

<https://twitter.com/rperezmarco/status/1013938984718884866>

# Introduction

I wanted to present some ideas for alternative ideas for routing on LN. This was published on [arxiv: 1807.00151 (July 2018)](https://arxiv.org/abs/1807.00151v2).

<http://webusers.imj-prg.fr/~ricardo.perez-marco>

# Overview

I am going to talk about what I understand to be decentralized network. Fabrice has already explained most of what is LN about and some history about it. I will just recall a few properties that I need in order to address the mathematical problem of routing.

Here is a picture of the LN network. It looks impressive, right? It looks rich, connected. In some sense, it's decentralized. Decentralization does not mean it's homogenous. It's a fact of life that there will always be nodes with more connections. Pareto is already well at work here.

The fact that we have this picture is sort of weird. To have knowledge of the topology of the network is a vector of attack. It's nice for making graphics but bad for privacy.

# Decentralization

Here are some necesary conditions for decentralization. Here are some properties we want to see for talking about a decentralized network.

It needs open and affordable access to the network (liberte). Nodes can process the information they want (liberte). YOu should follow the rules. Nodes have access to the same information. Nodes have the same power. Egalite egalite egalite-- nodes should follow the same protocol. And ownership of nodes should be well distributed (diversite). And they should be richly connected to thousands of nodes. And they should be randomly connected (diversite). All nodes check the information shared. Nobody trusts anyone, and everyone verifies everyone.

# Payment channels

Payment chanenls allow off-chain transactions. Only the initial commitment transaction and one settlement transaction are on-chain.

There are unidirectional or bidirectional payment channels.

It's not clear to me that in a practical sense that bidirectioanl channels are significantly better than unidirectioanl channels. The reason is that unidirectional channels are easy to model, represent and implement.

Payments most of the time go in one direction anyway, so bidirectional might not be that interesting.

Each channel has a maximum volume decided by the two peers forming the payment channel. The transactions are instantaneous and anonymous. The payment channels are composaible-- it's a transitive property. This is helpful for routing like, if three people are connected, then the two people on the end can pay each other even if they are not 1-to-1 connected with each other, through the third person.

# LN setup

The network is a weighted oriented graph. The mathematical problem is to find routes of payments. We assume that on top of LN there is a communication network.

I assume that nodes reserve mempool space for routing purposes.

So we need a decentralized payment path finding algorithm without too much knowledge of the geometry of the network.

# Problems and difficulties

Global knowledge of the geometry of the network is a vector of attack. There are solutions being implemented with "beacon nodes" with rich routing tables. Beacon nodes or supernodes violate decentralization as well.

Some hints: the bitcoin network does not use routing tables to propagate transactions. The network is for a different purpose but it's interesting that the flood network works. Zero-confirmation transactions seem to appear instantly, and it propagates very quickly, and the connected is well networked.

# Ant search

Ant path finding algorithms are efficiently and highly decentralized. These are efficient algorithms for finding paths.

Ants are efficient because there has been natural selection for better algorithms. And the better algorithms have survived and propagated instead of the worse algorithms.

Goss et al 1989 figured out ant search algorithms. Over time, ants prefer the short path over a long path if it goes to the same destination. Ants don't have global information--t hey leave a trace of pheromones. They have a social effect on the ant community. They keep a trail and they leave information. If you block the short channel, the pheromones are already on the long channel and the ants will continue to follow that even if you unblock the short path. The paths are reinforced with pheromones. They have an algorithm to find the good path, but over time, they can optimize, and they can change the geometry of their path if food changes places.

# Pheromone seeds algorithm

I am going to explain a simple algorithm using this pheromone idea. Alice wants to pay Bob. The first thing they do is they agree on a common random number R with 100 bits or something.

Alice constructs a pheromone seed S(A) by concatenating 0 with R and Bob does the same with concatenation of 1 and R.

The derived seed is if S = X concatenated to R, then the derived seed is S' = R. The conjugate seed is ....

Alice and Bob prospectively propagates their seed on their end with the neighbors on the LN. They send the seeds to their neighbors with which they have an open channel.

# Propagation and matching

There's some propagation on the network. Any node that receives the pheromone seed.... it notes the neighbor from which it is receivied. ... if none of them were received, he stores it in the mempool and propagates to other neighbors. If it was already in the mempool but not the conjugate seed, then nothing else needs to be done, it's always been received earlier and propagated.

Suppose the conjugate seed is in the mempool, then that means a match has been found. The node constructs a matched seed and propagates it to the neighbos that send the pheromone seeds S(A) and S(B). He propagates it back because he knows from which it came.

# Confirmation and payment

Alice waits. After some time... under the assumption that the graph is rich and connected... Alice waits for several matched seeds to arrive, and chooses one and constructs the confirmed seed which is the conjugation of 0 and Sm to make Sc value.

Alice propagates the confirmed seed to the neighbor that sends her the matched seed and waits for Bob the confirmation of the path.

Next, you can use concatenation of the... to make the payment.

This doesn't take into account volume or fees. You can add that in different ways.

# Amount and fee

You can add several feeds to the pheromone seed like an amount field, maximal fee field, and a current fee field initialized to 0. Nodes only propagate the pheromone seed to channels that are compatible with the volume. If the amount to be paid is larger, then... don't provide that information to that neighbor.

Nodes increase the current fee field with their fee. If he is too greedy then it will reach the maximal amount field and then it will no longer be propagated. There will be a natural market of fees that can be developed in this way.

The node matching the two pheromone seeds will update the amount of the fee field adding his fee both the fee amounts, and checks that this is lower than the maximal fee.

If the maximal fee is chosen then the downside is that maybe Alice picks another path that advertized a lower fee.

# Mempool management

The poitn is to renew this mempool... this should be done in a few seconds, the data should be discarded after some threshold time, it could be 5 seconds or something. He can manage the data and figure out what is optimal for him.

Alice can also choose her own waiting time, like a few seconds or longer. The longer she waits, the more options she gets for paths. She probably wants to use the minimal fee path. There's a tradeoff between waiting more time and getting lower fees. She's free to choose these parameters.

Seeds are a random number and should not conflict with another random number in a few seconds. Probably something like 30 bytes should be acceptable.... if the time interval before memory wipe is 2 seconds, then the constraining factor is speed of communication really. All of these pheromone seeds are circulating everywhere.

With a mempool space of a few megabytesi s that it should be enough to process thousands of transactions per second.

Bandwidth is another issue.

You need to do some numerical simulations to figure out realistic or interesting parameters.

# Self-improvement

Nodes are not forced to broadcast pheromone seeds to all of their neighbors. They could make a selection of their neighbors. They have historical data about their neighbors and which ones are efficient. They might prefer some neighbors to others. In some situations, they might prefer to relay the pheromone seed to the more efficient ones. Also, the topology of the network changes over time. If the network is changing, then good vs bad neighbors might change.

Each node could store historical information and compare it to short-term information, and then put some weighting on his neighbors to see which ones are more efficient.

Nodes that do the best analysis will increase traffic and earn more profit. There's an incentive to be more effective here.

# Numerical simulations

I plan to be doing this soon. The arxiv paper is just a description of what I've described. Numerical simulations are necessary toe valuate scalability and resources.

Communication speed seems to be the main bottleneck.

# Properties

There is no global routing table. Also, other nodes don't know about the details of transactions or channels. This is also good for decentralization because all nodes have equal roles. And also there's this self-improvement routing feature.

Thank you.
