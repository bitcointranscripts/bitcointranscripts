---
title: P2P Design Goals
tags:
  - bitcoin-core
  - p2p
date: 2023-09-20
---
## Guiding Questions

- _What are we trying to achieve?_
- _What are we trying to prevent?_
- _How so we weight performance over privacy?_
- _What is our tolerance level for net attacks?_

- Are we trying to add stuff to the network or are we trying to prevent people getting information?
  - Network topology: By design we are trying to prevent the topology being known

- Information creation, addresses, txs or blocks
  - We want blocks at tips fast - consensus critical information needs to be as fast as possible - ability to get the information - forgetting that there are multiple networks - the purpose is to know what the current most work chain tip is
    - Even the addr relay network - everything falls apart if you can’t get that information
    - The crux of the p2p network is to propagate what is the most work
  - Txs can take much much longer but don’t want to leak the source of the origin
    - The privacy implications of Txs makes it difficult

Could give up fast propagations for privacy for txs that would be fine but not for blocks. Speed is the most important factor.

More difficult to censor transactions because we have this decentralized network

Want a transaction to get to a miner

If there is an attacker which censors a transaction so that it is not propagated is a bigger concern. So the number 1 concern for a tx is censorship resistance then.

This is where different kind of actors come into play. If you try to stop the block propagation then

The pools are running bitcoin core nodes - fast connection to get to send in the blockshares and get the blocktemplate but they connect to pools

Censoring the chaintip is a big deal but not having your tx in my mempool isn’t a huge problem

- addrRelay exists to support these goals
  - The goal of addr is decentralization
  - Addr message may reveal about the network topology for example

Censorship resistance - create a network where everyone where connects and passes around information

- Your node doesn’t know if you are a reachable node. The network will tell you if it is reachable. From a network perspective:
  - Is providing inbounds purely altruistic
  - From a personal standpoint, are there any advantages to accepting inbounds?
    - Diversity? You have no guarantees that they aren’t the same entities.
    - If you are enabling inbounds - surface area vulnerability - we have mitigations in place but we have more influence on who you outbounds are over time
    - We need peers that accept inbound connections because we need that for the network to run

- We have completely different goals of outbound vs inbound conns
  - Inbound - DoS defense and diversity
  - Why are spynodes alway connected?
    - They may be evicted but then they will just reconnect
    - Or can connect from a different IP address
    - They can use a different port
    - It is intractable to keep track of them

- Is Inbound defense below our tolerance level for network attacks?
  - A ton of inbound conns to every listening node
  - They would be evicted
  - E.g. [Linking Lion](https://b10c.me/observations/06-linkinglion/):
    - They would disconnect their own conn when they make a new conn (which was stupid)

- Transaction requirements:
  - As a user we want some degree to
  - We are currently slowing down transactions for privacy considerations
  - Dandelion might slow down propagation is on the order of 3 to 7 slow down - this is the current trickling?
    - If there were requests to lower the propagation speed, would we push back?
    - Network wide - we would index more on protecting the topology of the network over speed of propagation.
  - Any transaction propagation delay around a block for LN is an issue. Would change all the computations for fee bumpings, etc.
  - What is the threshold for slowing down the transactions for privacy benefits?
  - Our design goals depends on who the user is
  - NoBan... - turns off trickling for transactions - it’s not safe, it’s something we use in the tests

- What do you feel is the tolerance level of attacks?
  - This comes up for fingerprinting?
    - Should we not care or not try to fix it?
    - If you had infinite resources - you could partition the network and do bad things
  - Think about it in terms of the cost of the attack
    - Partition the network may cost X
    - Map the topology may cost Y
    - How do we make that cost go higher? How do we make the decision for how much is enough.
