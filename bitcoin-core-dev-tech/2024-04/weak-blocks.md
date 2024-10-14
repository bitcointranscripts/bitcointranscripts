---
title: Weak Blocks
tags:
  - bitcoin-core
  - mining
date: 2024-04-08
---
Weak blocks: propagate stuff with low PoW as you are building it

- use cases / why you wouldn’t hear of stuff
  - nonstandard to you
  - somehow didn’t propagate to you
  - miner’s prioritisetransaction stuff with no fees
- why is this coming up now?
  - more mempool heterogeneity
  - “accelerate nonstandard transactions” services
- poc code: submits to mempool, rejected ones are stored in separate cache

Questions

- why would a miner do this? (similar to compact blocks?)
- add to mempool?
- what if invalid/nonstandard?
- good for fee estimation
- why didn’t we do weak blocks before, years ago?
  - some of it was pre-compact blocks

