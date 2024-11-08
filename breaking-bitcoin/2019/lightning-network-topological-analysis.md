---
title: Topological Analysis of the Lightning Network
transcript_by: Bryan Bishop
tags:
  - research
  - security-problems
  - topology
  - lightning
speakers:
  - Istvan Andras Seres
date: 2019-01-15
media: https://www.youtube.com/watch?v=1iAfJnlGJ6c
---
paper: <https://arxiv.org/abs/1901.04972>

<https://github.com/seresistvanandras/LNTopology>

## Introduction

Knowing the topology is not necessarily a vulnerability, but it gives you a lot of information. If I know Bryan's full node is connected to some other nodes, I will have an easier time to cut Bryan out of the network or launch attacks against him. Knowing the topology is not necessarily a vulnerability, but it's really strong information.

## Recent research

There were some recent papers published on this topic:

* TxProbe: Discovering bitcoin's network topology using orphan transactions
* Timing analysis for inferring the topology of the bitcoin peer-to-peer network
* Exploring the Monero peer-to-peer network

Layer 0 topology is hard to get and hard to see. But layer 2 is easier to look at.

## Scaling slide

We all know that bitcoin is pretty slow and 4 orders of magnitude slowe than VISA or MasterCard. The question is how can we scale bitcoin because we would like to be able to achieve mass adoption, right? I would like to give a birds eye view of what a payment channel looks like. It's like a string and along the string are beads. The idea is to do payments off-chain by starting with a commitment transaction and signing different update transactions that can later get into the base layer chain, without any counterparty risk other than reactionary security. I assume mos tof you know how HTLC works. I am happy to talk about it, or you can just ask roasbeef after the panel. Just accept the fact that we can route payments in an atomic way without any counterparty risk, that's all you need to know to understand my talk.

We can model the lightning network as a weighted multi-graph where nodes are people and organizations, and edges between these nodes are payment channels. The weight of the edge is the capacity of the payment channel.

## Research questions

* What structure does LN have?
* How centralized is LN?
* How robust is LN?
* How can we increase the robustness of LN if we can at all?

I can't tell roasbeef to open a payment channel with Bryan, because it's a permissionless setting. It's not even obvious how we can make the network more robust, if we can at all. We as a community either bitcoin or lightning we shouldn decide if it's an explicit design goal to achieve high robustness or not.

I was not the first person to think about these issues and talk about. There are several people on reddit like jessquit and bitcointalk.org and StopAndDecrypt... but they lack any scientific argument. "Them lightning network nodes sure do look centralized to me! What gives?". You could just say the opposite too; if you don't back it with any real arguments then it doesn't mean anything. So I got pissed off and decided to look at this in a more rigorous and scientific way.

## Analysis

I made a snapshot on January 3rd, the 10th anniversary of our beloved bitcoin. What I found is that the number of nodes was more htan 2300, the number of payment channels was 16000, the average node has 7 payment channels open. There were 2 connected components, and the density was 0.00605. The total BTC held in the lightning network was more than 543.6185 BTC. The s-metric was 0.6878. It's a small-world graph. The diameter is 6 and the radius is 3. Everyone is pretty close to each other. The mean shortest path was 2.80623. Transitivity was 0.1046. Average clustering coefficient was 0.304. The degree assortativity was -0.269. If Kevin knows me and Kevin knows Bryan then transitivity is trying to close in behavior the number of triangles. In social graphs, we have such behavior because if kevin knows me and kevin knows bryan then most likely kevin will introduce bryan to me. In social graph, there's triangle closing behavior or transitivity. In lightning, there's no financial reason to do that. So in lightning network we won't have these triangle local structures. It's no surprise that transitivity is quite low. Degree assortativity is negative, meaning that nodes tend to connect to dissimilar nodes. If a node has a few payment channels, then it will most likely connect to a node that has many payment channels.

Let's look at the degree histogram, with a log n graph. I am using a log-lin scale graph. The vast majority of nodes have very few payment channels, usually fewer than 20. There are a handful of hops that basically dominate the network. Only a handful of people have a tremendous number of payment channels. LN is a scale-free graph. It's a skewed distribution that doesn't look gaussian at all, it's a power law.

I then focused in our paper on network robustness. How robust is LN? In LN most of the IP addresses are visible. Only a few dozen people use Tor at all. So it's easy to target people and figure out who they are. Modeling targeted attacks is not far from reality. What we did here was we removed high degree nodes one by one and the corresponding payment channels in the graph and measured how many connected components after removal of these nodes... what we found is that if we remove the 30 highest degree nodes, then we will see more than 400 connected components meaning that 400 people will be just cutoff from the network and they cannot use lightning network anymore if there was a targeted attack.

Let me introduce a percolation threshold which can assess network robustness. What we usually see with real-world networks is that we remove nodes, we attack nodes, we remove the node and the corresponding payment channel edges in the network. The networks are pretty robust up to a certain point called percolation threshold and we remove a single node and it collapses entirely.

## Node removal attack

There is an attack effect on path length. If we remove thirty high degree nodes then this ratio would increase dramatically to 3.3 so we would have a harder time routing payments in the face of a targeted attacks. Thankfully the bitcoin community liked our work, and some people in the network science community. It's great that more people started to look at lightning network topology.

## Payment channel exhaustion attack.

There was a follow-up paper from Elias Rohrer. In our work, we focused on node removal based attack. They instead proposed channel removal based attacks. This attack is called a payment channel exhaustion attack and he showed that the lightning network is susceptible to this attack.

## Node isolation attack

A companion attack is the node isolation attack. You can deplete outbound capacity, which prevents a node from routing payments in the network, thus isolating them on the lightning network and they are now a useless participant on the lightning network. Elias showed that the lightning network is susceptible to such an attack.

## Dynamic network analysis

I made a snapshot of the network and argued about several properties only looking at the snapshot. Now instead we are doing an active analysis and we're creating snapshots or even a video of how the lightning network topology changes over time. Here's a nice graph of showing the average degree increases over time. I have a nicer graph where you can see that as long as the average degree increases then obviously the diameter of the graph decreases. Here you can see the mean average path length doesn't really change over time so routing doesn't get any better or any worse. The robustness of the network is kind of constant over time.

## Other research

* On the difficulty of hiding the balance of lightning network channels
* Discharged payment channels arxiv.org/pdf/1904.10253v1.pdf
* Sergi delgado-Segura et al arxiv.org/abs/1812.00942
* Bitcoin timing analysis paper
* Mccory, Gervais, off the chain transactions on eprint.iacr.org/2019/360
