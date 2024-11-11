---
title: Erlay
tags:
  - bitcoin-core
  - erlay
  - p2p
date: 2024-10-17
---
Idea from 2018, code since 2021
code-wise, only 20% of the high-level code is merged (not counting low-level minisketch code): The basic structure, plus code for peer signaling has been merged
-> good time to join, Review is needed

Open questions mostly concern policies (decisions of nodes) - there are various details still under discussion, such as picking parameters, details in logic etc.
BIP330 only defines protocol, but not the policy decisions

Minisketch parameters are hard to analyze analytically, other parameters such as decisions where to flood may be more important so these are more of a focus right now.

Simulators in Java and Rust exist to help make decisions on these, plus to help answer the big questions, whether it is worth doing (theoretical happy case vs real world).

Transaction trickle: Time between sending out queued batches of INVs- this will be be lowered for Erlay transactions - this has implications on privacy etc.
With the current parameter set, propagation times would be larger, which is th reason the trickle interval is being reduced with Erlay.

Reconciliation isn't done with all peers - some transactions are flooded - The intention is to have a minimally functional flooding, and have Erlay fix up the missing parts.
Also, the intention is that flooding should reach most of the public (reachable) nodes, while it’s fine if non-reachable nodes do more of the reconciliation.

Current Erlay policy: One outbound peer per transaction is picked per transaction for flooding plus a percentage for inbound peers - this will vary for different transactions.

Possibly create a document for design choices.

Testing:
One next step is to do simulations using the full implementation on warnet, with a set of ~1000 nodes
A simulator can deal with larger networks  - it’s more efficient, but less realistic than simulations with the actual code such as Warnet - both are needed.
Interesting scenario for simulations is to simulate scaling behavior when outbound slots are increased from 8 to 16 and analyze traffic.
