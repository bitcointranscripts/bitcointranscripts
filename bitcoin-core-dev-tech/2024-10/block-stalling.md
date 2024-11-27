---
title: Block Stalling
tags:
  - bitcoin-core
date: 2024-10-15
additional_resources:
  - title: 'PR #29664'
    url: https://github.com/bitcoin/bitcoin/pull/29664
---
[https://github.com/bitcoin/bitcoin/pull/29664](https://github.com/bitcoin/bitcoin/pull/29664)

There are 2 mechanisms to deal with stalling.

1. If we're close to the tip - we download from additional peers via compact blocks.
2. If we're far behind the tip (1024 blocks or more) - we kick stalling peers.

Between these regimes there's no existing mechanism to deal with block stalling - except fixed 10 minute timeout.

We could extend mechanism 1 or 2 to this inermediate zone(not at tip + not deep inside blockchain). But there's disadvantage to applying these mechanisms in this zone:

1. we kick too many peers if we extend IBD mechanism.
2. If we download from more peers in parallel, then if we have very slow connection we'll never keep upto the chain.

## Brainstorming Ideas

Replace 30 sec limit (limit to add another peer if we haven't heard block from any peer in 30 sec - see [PR#29664](https://github.com/bitcoin/bitcoin/pull/29664)) with a dynamic limit based on data from historical events. How can we put a lower bound on a peer's bandwidth and our bandwidth?

Most common use case for near tip IBD is flipping on the laptop again after a night.

How can we test IBD on low powered devices? We could simulate throttling internet and try it on warnet/mocktime/test framework. Have a simulating bandwidth option.

Compact block anti stalling mechanism is too eager if everything is being out of band mined or if the mempool is not filled yet (right after startup for example)

Currently nodes can keep up with the chain if they download 1 block every 10 mins. Do we want to lower this limit? Probably not. Where are slow environments in the world? segwit made the problem a lot worse.

how much hash power was increasing over time? 10 min has never been enough on average.

We only fetch from outbound peers. Should we change that? We don't have inbound at IBD. We only have Sybil's as inbound.

Other possibility is to put it in documentation that minimum requirements are this. and the peer is not guaranteed to catch up to tip.

## Conclusion

Change approach to use historical data. And don't lower 10 minute per block minimum requirement. Maybe also apply historical data to IBD stalling mechanism.
