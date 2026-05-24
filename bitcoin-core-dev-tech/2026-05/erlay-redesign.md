---
title: Erlay Redesign
tags:
  - bitcoin-core
  - p2p
  - erlay
date: 2026-05-05
---

What's the plan/direction for Erlay? It's been a long-standing project,
and we have to ask if the code complexity and other tradeoffs are
actually worth it. The bandwidth/latency tradeoff has been a major focus
in the past, but the primary goal is to add more connections to increase
partition resistance. A more cohesive network.

The original idea for Erlay was to replace all full (tx) relay
connections with "full Erlay" connections that intelligently switch
between fanout and set reconciliation. However, the P2P logic for this
is (grew to be) complex and the changes are pretty extensive.

Instead of full Erlay, a simpler alternative would be to add pure
reconciliation (recon) connections while keeping our normal tx relay
connections. This means we'd have three distinct connection types:
1. Full relay (fanout)
2. Recon-only
3. Block-only

## Benefits of Recon-only

- Scalability: Set reconciliation improves how connections scale. We can
  add more tx relay connections without causing a linear increase in tx
  announcements.
- Partition Resistance: Recon connections would act as a reliable backup
  for transaction relay. If a node is facing an eclipse attack or
  censorship on its normal tx relay connections, the recon connections
  can take over, at the cost of slower propagation of transactions.
  Latency remains the same in the honest case, but increases in the
  dishonest case, which is better than having txs not propagate at all.
- Simplicity: It's a lot less complex to just add a new connection type
  than to build a full Erlay implementation that decides when to fanout
  vs when to reconcile. Ultimately, it seems to be boiling down to
  either doing recon-only or simply adding more full fanout relay
  connections (same as the 8 connections used today), rather than
  pursuing full Erlay or not adding any more connections.

## Tradeoffs and Cost of Adding More Connections

- Privacy: Should recon connections be private (i.e. not sending
  addresses over them) like block-only connections? Probably not.
  Block-only connections are just pings and blocks, but with tx relay
  recon connections, it's hard to hide your mempool contents and tx data
  anyway. They'll likely need address relay just like full relay
  connections. In terms of timers, normal relay uses a Poisson timer for
  privacy. Will the recon timer be Poisson, or will it be a predictable
  interval (like exactly every 30 seconds)?
- Memory: There is very significant memory usage per peer, even just
  doubling inbound slots from 125 to 250. It forces a peer to allocate
  maybe 10-14MB per connection. For 100 extra connections, that's an
  extra GB of RAM.
- CPU: Since set reconciliation isn't validation-related, we could
  potentially put the CPU work in its own thread without any locks. If
  we do that, the CPU overhead for adding these connections might
  essentially be "free."

## Current State and Next Steps

- How partition-resistant is the network right now? It's hard to answer
  and difficult to reason about. For testing and evaluating
  costs/tradeoffs of this new connection type, we should take into
  account the worst-case scenario an attacker could pull off.
- Topology: This change needs to account for both outbound recon
  connections and inbound recon slots for reachable nodes. It could be
  possible to estimate how many open slots exist today. Some context, in
  2011 the network ran out of connection slots which originally led to
  the desire to add more connections.
- The immediate next step is to write a C++ implementation of these
  recon-only connections so we can do some proper testing (real nodes
  and Warnet).
