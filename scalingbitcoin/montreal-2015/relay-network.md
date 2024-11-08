---
title: Bitcoin Relay Network
transcript_by: Bryan Bishop
tags:
  - mining
speakers:
  - Matt Corallo
media: https://www.youtube.com/watch?v=mhAsnzidtZ8&t=1346s
---
It was indicative of two issues. A lot of people were reducing their security model by not validating their bitcoin. It was potentially less secure. That's not something that relay networks try to address. The big issue with the decreasing number of nodes, which the relay network doesn't address, is that it reduces the resilience against attack. If there's only 100 nodes, there's really only some 100 VPses that you have to knock offline before the bitcoin network stops working. This is potentially very easy because knocking offline 100k nodes is not that hard. The relay network is a pseudo alternative. It's not designed to be efficient. It's a pseudo-centralized second network to connect to.

A second issue is that a lot of people were concerned aobut the selfish-mining attack. The paper claimed, and it was mostly true, that you can with 33% of the mining hashrate pull off a short-term 51% attack. This is much eassier, and you can do this with less mining network, if you have visibility into how the network is laid out. At the time, and still today to some extent, we have very little visibility into the way the network is layed out. There is a lot of potential for someone to connect both smartly and to a lot of nodes and get much better visibility into when a block is announced.

So the relay network can sort of address that. ... If you're a smaller miner, you don't have time to invest to build a giant relay network. It started as some centralized nodes that did SPV validation and relayed things quickly. That wasn't quick because java and low-latency doesn't really work.

Now it does pseduo-compression and takes each transaction in every block, it says that it was sent 5 seconds ago and references recently-transmitted transactions.

Runs as a simple nth-last-transmitted protocol. At the moment a lot of the transactions on the bitcoin network (during a spam attack?) has the same fee per kilobyte rate.

So this is a map of the various nodes in the relay network. It's very interesting because I had to spend a lot of time coming up with this topology. Routing in Asia is terrible, especially into mainland China. Routing into mainland China, it has to go through Japan and then through Los Angeles. If you're trying to get to Europe, you don't want to go through the US. There is a cable through Siberia, but you need to get a node there if you want to route through it. Small miners are not going to look into doing this because they don't have time to figure it out. Big miners might, because it could significantly save them orphan rate. But the p2p network is not going to find a quick route from Beijing to Amsterdam through Siberia. A randomly-networked network is not going to find this route on its own.

There's tension between a decentralized network that we can throw nodes at and it relays transactions, versus something that is going to shave off orphan rate because it's centrally designed and centrally planned and actually works well. There is a huge opportunity cost to just not using a centralized network. This is a wonderful graph of time-to-relay things around the network. This is really relevant for block transmission around the network. On the left axis, you can see the block size that is actually sent over the wire, and the bottom you can see the milliseconds for it to get around the globe. There's a strong correlation after you send a few packets. The block relay network takes a few TCP packets at most. TCP over long-haul links, it has nothing to do with gigabit links or anything directly to backbone connections, it just has to do with the latency and the packet loss. Once you lose a packet or two, things get pretty slow.

Those 10 sec you see on the far right is 1.5% lost revenue for miners, which is kind of significant.

I am also here to ask for help. This project is something that I have been doing on my own for a while. There's a github. It's pretty simple. It proves the effective hashrate of bitcoin with just software. There's a roundtable on this later.

<https://github.com/TheBlueMatt/RelayNode/issues>

<http://bitcoinrelaynetwork.org/>
