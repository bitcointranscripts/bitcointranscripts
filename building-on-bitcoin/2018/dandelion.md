---
title: 'Dandelion: Privacy-preserving transaction propagation in Bitcoin''s p2p network'
transcript_by: Bryan Bishop
tags:
  - dandelion
speakers:
  - Giulia Fanti
date: 2018-07-03
media: https://www.youtube.com/watch?v=SrE6KdBgI1o
---
<https://twitter.com/kanzure/status/1014196927062249472>

Today I will be talking to you about privacy in bitcoin's p2p layer. This was joint work with some talented colleagues.

## Bitcoin p2p layer

I want to give a brief overview of the p2p layer. Users in bitcoin are connected over a p2p network with tcp links. Users are identified by ip address and port number. Users have a second identity, which is their address or public key or however you want to think about it.

When Alice wants to send a payment to Bob, she broadcasts a payment transaction to the network, and then miners start racing to append this transaction to the blockchain.

Alice's address and her real identity need to remain unlinked. In this talk, I am concerned with linking Alice's bitcoin address to her IP address. This is not completely deanonymizing someone, but it's an important step, and you can sometimes narrow down who that person is.

My claim is that the way that the current bitcoin network works is that it amkes it relatively easy to link someone's address to their IP address.

## Transaction propagation

Today, messages on the network spread according to a process of diffusion. Nodes spread transaction with exponential random delay. Each node independently chooses fresh independent delay.

If we have a set of corrupt nodes, they can use the node graph to infer the source node of a particular transaction and they can make that linkage.

The problem is that diffusion is vulnerable to source detection. This has been explored in a bunch of papers including a few tailored to bitcoin's p2p network. The point is, without expending too many resources, you can make this linkage with probabilities that are exceeding like 50%. They are scary numbers.

## Dandelion

Dandelion is a project to build a lightweight transaction propagation algorithm with theoretical rpovable anonymity guarantees. I am going to be talking about what those guarantees are and give you some intiution about why dandelion works.

Why not use existing solutions like tor or i2p? The idea with Tor is that, Alice has a transaction and send it through Tor to a randomly selected other node and the blue node will diffuse the message for her. Because she is using Tor, the blue node doesn't know who Alice is and she gets privacy here. This is addressing the same problem and if you're worried about privacy then you can or should use tor. However, one of the issues is that in order to adopt this solution, you have to be aware of the privacy problems of bitcoin, and some users aren't aware, or even if they are then they might not have the expertise to do this routing through tor. It's important to build in mechanisms that protect all users, not just the ones that are particularly concerned about privacy.

The other solution that people discuss is why not build some kind of onion routing into the network itself? For example, monero has been integrating i2p into their p2p network since I think 2014. This also addresses the problem we're trying to solve, but one of the problems seems to be that implementing this is actually really time-intensive, requires a lot of developer hours and expertise. Okay, 2014, and it's soon to be implemented, it's not done yet. Okay, so 2014, that puts us at 4 years. It's a substantial implementation effort. It would be nice if there was something more lightweight and easier to implement.

Our goal with dandelion was to propose a system that has theoretical privacy guarantees, benefits everyone in the network, and is lightweight and easy to implement.

## Model and assumptions

I am going to talk about the model and the solution next.

The adversarial model is that we have some network with some fraction of the nodes are corrupt or acting as spies. Some fraction p is spies. So p is the fraction of spies. The identities of spies is unknown and they observe all metadata coming to them, including timestamps and packets. These devices collude with each other. They are honest but curious- they generally follow the protocol, but eventually I will relax this assumption and deal with byzantine nodes as well.

In bitcoin, you have many users and each user could be generating multiple transactions. We're going to assume we have n users, and each user is creating one transaction. The goal of these spy nodes is to create a mapping from transactions to users. The level of deanonymization that they achieve is a measure of how good is this mapping. To measure the quality of the mapping, we use a metric from machine learning literature, called decision and recall. In the context of this example, recall is measured by looking at the mapping an counting the number of correct errors, mapping the red transaction to the red guy in this diagram.  There's 3 users, so we have a recall of 1/3. This is similar to probability of detection, it's a commonly studied metric in the anonymity metric.

Precision is measured as follows: for each correct arrow in this mapping, how many other transactions were mapped to this guy? We have other transactions mapped to this same guy in this diagram. We do the same exercise for all the users in this example. The average of all of those is going to be 13/rd over 3. So this is recall and precision. The goal of the adversary is to maximize its precision and recall.

Our goal is to design a distributed flooding protocol that minimizes the maximum precision and recall achievable by a computationally-unbound adversary.

There's some fundamental limits to these variables. Suppose that we fix a spreading protocol, like difufsion, and we fix an estimator that the adversary is using to fix transactions to users. So that coupling of a spreading protocol and an estimator can be mapped to one point on this plane and it has some expected precision and recall. The first thing we show is that the point has to lie between the blue and red lines. The reason for that is because we have coupled our precision and recall by assuming that each user has one transaction. This is unusual for precision and recall curves, but we'll relax that later. Now suppose that we cycle over all possible estimators that the adversary could use, associated with some point in this place. The union of all those estimators is an achievable region for a particular spreading protocol. So the next results we show is that no matter what spreading protocol you use, your purple region is always going to be to the right of the vertical dotted line with a certain maximum recall. You have a maximum precision of at least p squared, where p is the fraction of spies. No matter what spreading protocol you use, the best we can nohope for is that green triangle at the bottom. We're trying to match the green triangle, basically.

So, how do we improve the anonymity properties of the p2p network?

There are two basic properties that we want. We want assymetry-- in diffusion, you're spreading the message symmetrically, and I'm spreading them at the same rae to my neighbors on my p2p graph.  The spies can collect this information. We can break that symmetry by spreading faster in some directions on the graph and slower in the other. The second property I want is mixing, and not in the chaumian sense. Let's say that we have a sequence of nodes with a spy at the end. The spy is going to get 4 different transactions, and because they are all coming in on the same edge, it has no ways to know that the transactions are belonging to that last node. So we want asymmetry and mixing.

We can control the spreading protocol-- given a p2p graph topology, what is the spreading method? Right now, bitcoin is using diffusion. The second property is the topology. What does the underlying graph topology look? Bitcoin is using a regular approximately-random construction. And the third is dynamicity, how often does the p2p graph change? For now, the p2p graph is changing much slower than the time it takes for a single transaction to propagate.

## Spreading protocol: Dandelion

It has two phases. There's the anonymity or stem phase, and then the spreading phase or fluff phase. Suppose the source node is this far left node. The source is going to pick exactly one of its neighbors and pass the messae to its neighbor. The neighbor will flip a coin and if it lands heads then he continues and passes it to one one neighbor. This continues until someone flips tails. And then we switch into fluff phase. The reason why we call this a dandelion is because the spreading pattern looks like a seed head from a dandelion.

Dandelion spreading has an optimally low maximum recall. The recall always has to be at least p. Dandelion achieves p + (1/n) where ni s number of nodes. So now we only need to optimize precision. This makes the optimization problem easier and more well defined.

There were two other knobs to toggle- the first one is the graph topology. We're going to use a line graph. We will add an overlay graph called the anonymity graph. When a transaction comes in, it propagates clockwise over the anonymity graph until someone flips tails. Similarly, if a second transaction comes in, then it also rpopagates clockwise over the same cycle until someone flips tails. It's important to notice here that all of the transactions are propagating over the same line graph and they aren't taking independent graphs.

The other thing we change is the dy namicity. We are going to change the structure of this cycle graph, frequently.

We use dandelion spreading, it has a line graph topology, and it changes the anonymity graph frequently.

Under these assumptions, dandelion has nearly optimal maximal precision, which is a logarithmic factor away from the lower bound. Theoretically, this is giving us some nice properties. If we go back to that picture I showed you earlier, here's some green traingle over there, and dandelion gets us there pretty close. If you compare to diffusion, we're getting a substantial improvement in privacy guarantees.

Just to give you some intuition about why this is the right thing to do, I am going to tell you about two types of graphs that don't work well.

Imagine a tree graph where nodes pass transactions up to some root node in the tree. This has precision pretty bad. The spy nodes in the second to the bottom layer, that spy is able to automatically deanonymize two nodes with perfect precision and recall. In a tree or regular tree, you have a linear number of nodes in the second to last layer, because there's too many leaves in tree graphs. So we want a topology without too many leaves.

Another type of graph we tried was a complete graph where eeryone is connected to everyone, like in crows or tor. This is suboptimal too, but for a subtle reason. To get good anonymity, you want different transations to be progressing over the same route in the graph. In a complete graph, you have so many edges that the probability of any transaction traversing the same paths, is actually really low. So you can't have too many internal paths. Cycle graphs have only one path that transactions can traverse over.

Some of you might be thinking, how are we going to construct a perfect cycle graph and that's totally unrealistic. Well, that's true. So in practice, we're proposing that, each node, is going to look at their outbound edges in the p2p network for the edges they initiated. They are going to pick exactly one edge ... to be their dandelion relay. If a transaction comes from someone else or their own transaction, they relay over that dandelion edge and the recipient will choose one of their outbound edges to be their dandelion edge, and so forth, until someone flips into fluff phase. Each node picks one outbound edge, and we end up with an anonymity graph that might not be a perfect cycle, but it looks similar and it ends up having similar anonymity properties.

There's a number of ... this was our initial proposal, for dandelion, and we spent the last year or so trying to strengthen dandelion against more realistic adversarial models. What happesn if you have byzantine nodes that are disobeying protocol in arbitrary ways? In our recent ublication, we talked about a number of these  issues to make the system more robust to some of these attacks. Some of these include adversaries that can learn the graph precisely, ,or adversaries looking at many transactinos, or maybe I'm generating 100 transactions and each one takes independent paths.

One of the main takeways from Dandelion++paper was that maybe instead of using a line graph (too regular of a graph), maybe a four regular graph where each node picks two outbound edges instead of one.

We also implemented dandelion and ran some tests on mainnet. We ran 30 dandelion nodes in geographically diverse locations. We wanted to evaluate the main tradeoff, which was latency. By sending transactions across this path, you're delaying the time for everyone to get the transaction. The time for the transaction to reach 10% of the network in seconds... so as the path length increases... to about 8 seconds.. when you do have dandelion running. This 2 second overhead in latency is might be a problem in low-latency cryptocurrencies... but for bitcoin which can tolerate high-latency and high confirmation times, I think that can be very reasonable.

## Take home messages

Bitcoin's p2p layer has weak anonymity properties right now. Dandelion may be a lightweight solution against large-scale deanonymization attacks. Don't replace Tor-- this is just for large-scale privacy vaccination.

We have a draft BIP, and we would welcome feedback on this. And we have a reference implementation.

<https://github.com/dandelion-org/bips>

<https://github.com/dandelion-org/bitcoin>

## Q&A

Q: When you talk about flipping a coin, what is the parameter?

A: Good question. We actually choose 0.1.

Q: How do you know that the path you're taking isn't compromised and you keep feeding it with new information?

A: The location of the transaction is a markov chain. Once you reach a compromised node, anything that happens after that isn't helping your privacy. You might run into a malicious node in your stem, so that's accounted for.

Q: What about backwards compatibility for deployment?

A: We did some analysis on trying to understand what happens if you partially deploy dandelion.. where only a subset of nodes are running it. If you're the only running dandelion, you get some privacy benefit, and then the benefits grow as adoption increases. For backwards compatibility, the way we have implemented it, if you are connected to someone who does not yet support dandelion then you are starting the fluff phase prematurely. There are no compatibility issues.

Q: How do you deal with sybils?

A: Sybils are captured in this parameter p. If an adversary were to flood this network with sybil nodes, then this means you have a higher p fraction. That's certainly a problem, but what would happen in the current networking stack versus dandelion? You end up with a probability of detection of 1 with the current bitcoin code. If you have too many malicious nodes in the network trying to deanonymize you, then there's not really much you can do anyway.
