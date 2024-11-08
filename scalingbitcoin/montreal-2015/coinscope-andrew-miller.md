---
title: Coinscope
transcript_by: Bryan Bishop
tags:
  - mining
speakers:
  - Andrew Miller
  - Dave Levin
---
<http://cs.umd.edu/projects/coinscope/>

I am going to talk about a pair of tools, one is a simulator and another one is a measurement station for the bitcoin network. So let me start with the bitcoin simulator framework. The easiest approach is to create a customized model that is a simplified abstraction of what you care about- which is like simbit, to show off how selfish-mining works. What you put in is what you get, so the model is actually different from the actual behavior of the bitcoin network means that you don't learn anything really. You can have a local private network where you see the real bitcoin code. You don't then don't have as full control over the network; perhaps race conditions are hard to repeat. And you need a very powerful computing system, so you need as many cores as you have nodes. The approach I am going to talk about is a cross between simulation and emulation, running on an entirely simulated network, but everything is emulated. This decouples the virtual simulation time from the real world time.

This is started by the shadow framework, started by Rob Jansen. It's a framework that works like that. He used it to study bittorrent and tor. For my summer internship with Rob, I upgraded the shadow framework so that it could support bitcoin. Shadow is really only made to handle applications with simple event loops, like a single threaded event loop with blocking io, but bitcoind has multiple threads and so on. We had to rearchitect shadow to support this. We did that. We are able to run simulated networks with up to 6000 nodes with only 64 nodes. It runs 1/16th real time, but all the times are simulated anyway.

But we need to bootstrap the network topology. What does it look like? That's a big problem.

Coinscope is able to measure the bitcoin network overlay topology. We ran scans every 4 hours periodically. Our focus is network health, not deanonyization. We're not like Chain Analysis. getaddr is the gold standard for bitcoin node measurement. You can see the nodes on the network, where they are distributed and which versions; but you don't learn how they are connected together. We think that bitcoin strives to have a random graph, and it's because up to 117 incoming connections and 8 outgoing connections, and nodes store and propagate information about peers they are going to be connecting to.

We periodically scrape all getaddr outputs of every node we can connect to. The getaddr data is important for information propagation. Peers share data with each other through first relaying addresses to each other. This begins whenever a connection is formed and then the initiator of the connection sends that address and it sends it to couple more peers and so on, and every peer announces itself every 24 hours. The ohter way is that if a node sends a getaddr message, then the peer sends 2500 of its addresses along that connection. And now the relay part is that you actually get the same timestamps, you get the addr message of that timestamp time when it percolates through the network. SWhen you get a response to a getaddr, you add a 2 hour penalty.

If you look at a node and you look at all of the timestamps with the addr messages that show up, you see these weird clustering effects. You see one cluster where there's a lot of timestamps, and you see these echoes of various layers of 2 hour penalties applied, so you can see a signal there that is representing the initial connection event. You can see that the outgoing connection continues to be updated which is a leading edge of the current connection.

So you can stack up all of the addr messages from all the nodes about all the nodes. The size of the node corresponds to all of the addr messages that have the same timestamp. You can identify when the most recent connection was formed by a node, and you can see from this frontier of timestamps within 20 minutes new are active current connections.

We can create cool looking snapshots of these networks, we can draw the graph. The size of the node represents its degree. This is a subset of the graph. We are only looking at reachable nodes and connections from reachable nodes to other reachable nodes; we don't learn about mobile nodes behind firewalls. Nodes have fairly low degree, but there are some cool supernodes. This is a snapshot from almost a year ago. A large number of the most affiliated nodes were mostly from the mining network, they all have bitcoin affiliate mining listed on it, they each have 1000+ connections.

Here's the caveat. There's a patch in v0.10.1 that breaks this; I think that Core developers knew that I was doing this, and it doesn't have a clear deanonymization problem against users; but jonas nick pointed out that the property that we use to do this might be used for deanonymization, so it no longer works but arguably it's an improvement to privacy. There's also txprobe, you can use mempools and transaction data structure, it's sort of invasive, and you have to spend BTC to pull it off, but we don't intend to do it.

The visible network may not matter that much, we can only see the ordinary nodes that follow this behavior, we can't see private peering agreements which might turn out to be really crucial for block propagation.

I would like to see metrics and measurements being a deliberate goal of bitcoin design. There are some ohter precedents for this, like tor has a nice usage statistics collection which is privacy-preserving but is useful for geolocation of nodes and users. There's also statoshi, which is interesting for collecting status of nodes and its data structures. It would be interesting to create privacy-preserving versions of this.

There are many denial-of-service (dos) problems with bitcoin; if we have large changes, then this will have impacts on what we think about block size and other scaling questions.

We are launching an academic journal for cryptocurrency research called Ledger. We want to be able to bridge academia and the bitcoin development community. This will be open-access because paywalls are gross. Reviews will be published next to each article. We're going to do some other features that are totally understandable to you, but for some reason this isn't done elsewhere like timestamping and signing documents.

That's all, thanks.
