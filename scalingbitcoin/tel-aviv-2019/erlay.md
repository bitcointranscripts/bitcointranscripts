---
title: Erlay
transcript_by: Bryan Bishop
tags:
  - P2P
speakers:
  - Gleb Naumenko
---
Erlay: Bandwidth-efficient transaction relay for bitcoin

<https://twitter.com/kanzure/status/1171744449396953090>

paper: <https://arxiv.org/abs/1905.10518>

# Introduction

Hi, my name is Gleb. I work at Chaincode Labs. I am working on making nodes better and stronger and make the network more robust. I've been working on erlay with Pieter and Greg and some other guys.

# Bitcoin p2p network

There are private nodes that are behind firewalls like ones run at home. If your node is connected to a router, your router tries to protect you from the internet accessing your endpoint. There's about 60k bitcoin nodes like that on the network today. There's also about 10k nodes that are open to the network and allow private nodes to connect with them. Without public nodes, the network would not really be functional.

Private nodes run at home have a default of 8 outbound connections while public nodes will do the same but they also accept connections. So by default they have 125 inbound slots. I would say that this is a really simplified structure. There is a network of universities that are connected to each other and available to each other, and closed from the internet. So it may be even more complex, but this general structure is enough for us to do research regarding transaction relay.

The bitcoin network is used to relay transactions. You want to be able to send and receive money. Transaction relay is the most important feature of bitcoin, I would say.

The bitcoin network is redundant because it's probably enough to connect to one node and learning everything from it, like transactions and blocks. But it is redundant so that we have more security. For example, your one connected peer might be malicious. You double check what you get against multiple peers. The chance that all 8 of your connections are malicious is pretty low outside of sybil attacks. By increasing connectivity, you lower it even more. Redundany provides security.

Currently, transactions are relayed through the network by flooding which means you announce the transaction to all of the peers except the one you received the transaction from. This is how transactions are relayed through the network. Within a few seconds, every node in the network knows about your transaction.

# Lifecycle of a bitcoin transaction

A transaction gets created and signed, then it's relayed to other nodes, it's validated by other nodes, and then it's included in a mined block, then a block is relayed and validated, and then more blocks are mined on to pof that block, and finally the transaction is confirmed. My work focuses on transaction relay, which is important to get transactions included in a block eventually.

# Properties of transaction relay

The fundamental properties of transaction relay are bandwidth, latency and privacy and security. You can measure bandwidth in bytes. The latency is how long it takes for a transaction to be relayed across the network. How long does it take for one transaction to be relayed from one node to all the nodes in the network. For privacy and security, the concern is how easy is it for surveillance spies to detect a link between addresses and nodes. We're doing our best to prevent that kind of analysis from being viable.

There are other interesting rpoperties like complexity of the code. We don't want to implement something very complex in bitcoin because it makes code review difficult and introduces additional bugs. But these are some of the fundamental properties.

# Current protocol (BTCflood)

I would call the current protocol BTCflood. You receive a transaction, and then you flood it to everyone. A typical node uses 18 GB/month to relay transactions if you're a private node. Much more bandwidth for a public node of course. 18 GB/month is fine for most nodes in the United States but some ISPs have hidden data caps. This is pretty bad for Asia and Africa. You can analytically measure how many announcements you need in a network to relay the transactions, based on seeing the transactions in a block it can be estimated.

Latency is where you measure how long it takes for all the nodes to know about a transaction. It seems to be about 3.15 seconds to reach all the nodes.

Privacy and security are alright. There are some techniques for surveillance, and then we try to defeat it by adding code. It's constantly improving. We'll be looking for these three properties when designing a new protocol.

My work is about how to optimize bandwidth without sacrificing latency or privacy or security. How to reduce the bandwidth that every node spends per month to participate in the bitcoin network and relay transactions, which is the most important feature.

We have talked about how we announce transactions. Let me explain it again. The protocol is a little more optimized actually. When you receive a transaction, you announce a hash first not a full transaction. The nodes will lookup in a local database as to whether they have it, and they request the missing transaction with GETDATA. I will send them the missing transaction after that, because I know for sure that they need it. The full transaction is maybe 250 bytes, and the announcement is 32 bytes. So the protocol looks pretty efficient and not much to optimize here, but actually that's not true because 85% of the announcements like this are redundant or duplicate.

Public nodes can receive 100 announcements of the same transaction at once, when it really only needs one such announcement.

# Bandwidth consumption by redundant announcements

Regular announcement INV announcements are 32 bytes, and then GETDATA is 32 bytes, and then the transaction is 250 bytes. This is the best case, which is what we want. The redundant INVs consume about 220 bytes which is nearly the same size of the transaction. It would be nice to eliminate this redudnancy.

# Increasing the connectivity

Increasing the connectivity makes it harder to execute an eclipse attack. Eclipsing basically means that if all 8 of your peers are the attacker, then it can feed you a fake blockchain and they can pretend that they have paid you money when they actually haven't. It's possible to connect to 8 malicious peers. Increasing connectivity increases the costs to an attacker.

It's harder to deanonymize transactions with increased connectivity. Basically, attackers are trying to link transactions to IP addresses of the node that first broadcasts the transaction.

Increasing the connectivity will also make it harder to infer the topology of the network. In the bitcoin community, we believe that we should preserve the privacy of the topology of the bitcoin network so that it's harder to attack it, unless someone shows us that this isn't necessary or not true. We want to make it expensive for an attacker to infer the topology.

But if we increase the connectivity, then there will be even more INV announcements. So the bandwidth costs go up.

# Prior work

There was some related prior work.

There are some block relay protocols like compact blocks, graphene, xthin, bloxroute. You relay blocks every 10 minutes on bitcoin. You really care about latency in block relay. If you relay blocks slower, then your hashrate proportion of the network becomes lower and the network becomes less secure. This isn't useful for our case. Transaction relay has different properties. We're okay with high latency, but we really want to save that bandwidth.

There's also topology-based routing policies like freenet, Efa, chord, pastry (non-byzantine). If a network is constructed as everybody connects to one hub, that would be super efficient. You relay to the hub, and in a star topology, the hub relays to everyone else. But unforutnatley this is not robust and if the hub goes down the whole thing fails.

There's also feedback-based approachs, where you attach a timestamp to the transaction and you can know when to stop trying to relay it. Unfortunately this leaks information. You can look at the timestamps and infer the topology of the network. We decided that we would be building on different techniques.

# Erlay: efficient transaction relay

The idea is to relay transactions across public nodes in a fast way. You don't relay to everyone, only to the public nodes in the network, the 10,000 that help everyone to connect to eachother. Then everyone else learns about the transaction through set reconciliation which is an efficient way to exchange transactions that you know about.

We're trying to keep the latency low. We know that flooding is very fast, so we are willing to take on some latency. We want to be more efficient than flooding in bandwidth. You can build a full reconciliation based protocol where you do this set reconciliation but it would be inherently very slow, even if it was super efficient probably.

So the idea is to flood it across public nodes in a well-connected public reachable nodes. Every node keeps a reconciliation set for every one of its peers. We will record what transactions we would send to each peer, but not actually send. This can use the minisketch set reconciliation library to converge to the same transactions in the network.

Q: How do you determine a public node or a private node?

A: This is a good question. You really don't want to have this flag in the Bitcoin Core software. You don't want to have "if public, do this" and "if private, do that". You flood transactions to your 8 outbound connections. It just converges to relaying across public nodes.

Q: So you don't know?

A: It will just naturally work that way, because of using this policy.

Q: So the assumption is that you have outbound connections to public nodes.

A: Private nodes aren't outbound to anybody. So that's why it works.

# Transaction set reconciliation to bridge gaps

Let's talk about set reconciliation a bit. The goal is to take two sets and converge to one set with minimum communication overhead. The idea is to exchange information in a way so that we both have the same view of the network and save bandwidth while doing this. It's not just recent transactions but also making sure we have the same view of the network.

Transaction reconciliation works like this. Every node maintains a set of transactions it would have sent to every one of its peers. Each one of these are set reconciliation sets. There's a timer on the node and it says reconcile with the peer on a defined schedule. When the timer is triggered, they use this efficient protocol using minisketch which I will explain in further slides. They exchange their view of the network. After that, the nodes will have exchanged their missing transactions. The sets are then cleared. We will make this set empty, and over on this other node, he sets his sit empty for that peer.

# Finding set difference with BCH codes

Bob and Alice never communicated before, but they think they share most of the transactions and want to help each other. We can do this exchange in two messages, instead of the naieve implementation of Alice telling all the hashes of all the transactions to Bob which involves many messages. We can do this in just two messages. This is a guarantee that I can explain in a moment.

Alice estimates the size of the set difference, carefully. If she underestimates, then the protocol fails. Alice needs to estimate the difference, and she can estimate 2 or 4 or more. If she estimates 1, then the protocol will fail. Alice computes a sketch of her set. Based on this, then, just computes a compressed representation of this. Alice sends a sketch to Bob. Bob computes his own sketch of his transactions. He combines the two sketches into one with a XOR, and from that he can find that he's missing Tx10 and that Alice is missing Tx15 in this example.

# Minisketch: Computing with BCH codes

Each transaction ID can be represented as an element in a field. You do a summary of syndromes. First syndrome is you add all the elements in the field. It's basic arithmetic math. You compute all the transaction IDs into one number. For the second syndrome, you sum all the second powers of the identifiers. This is just 64 bytes in this case. You can send just these two numbers to Bob and Bob will look at this and find the difference using his own part and this part.

# Minisketch (pinsketch implementation) benchmark

A bunch of time was spent on optimizing minisketch. The reconciliation timer can be tweaked to get optimal properties. In our case, we reconcile every 16 seconds. It takes about a nanosecond on a regular machine to do the math.

# Erlay bandwidth benchmark via simulation

By increasing the connectivity, the bandwidth costs almost don't go up. This is super cool for increasing the connectivity of the network. You can see here that the bandwidth goes down. We need to do other optimizations in Bitcoin Core but we could certainly do 16 connections right now with erlay, without any cost.

# Erlay latency benchmark by simulation

Erlay increases transactions from 4 seconds (using BTCflood) to 6 seconds. This is okay because block time is 10 minutes, and you don't really want to accept an immediate transaction 2 seconds later. They should wait for confirmations. So it's fine to increase the latency a little bit.

Does latency increase matter? We don't care about users in this case, since it's just one or two seconds in the interface. If you relay transactions slower, then compact blocks is less efficient and works slower which might affect the the stale block rate or orphan block rate. You really don't want to have orphan blocks on the network. Increasing transaction propagation latency might actually increase the orphan block rate.

Public nodes will learn transactions much faster, and miners could connect to those nodes or run public nodes themselves. So in effect, the security of the network goes up because we improve block relay through that mechanism.

# Erlay benchmark, prototype

I used 100 Azure machines running Bitcoin Core software and relaying 500 transactions. Announcement cost goes down from 42 MB to 15 MB, and latency went up from 1.85 seconds to 2.05 seconds. This confirmed that our estimates were correct about erlay.

# Various configurations of the erlay-like protocols

BTCflood is high bandwidth and low latency. Erlay is higher latency, but really low bandwidth. This is what we chose.

# Erlay

The advantage of erlay is that we save about 40% of bandwidth for every node, and we can now increase node connectivity safely.


