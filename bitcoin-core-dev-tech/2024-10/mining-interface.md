---
title: Mining Interface
tags:
  - bitcoin-core
  - stratum-v2
  - mining
date: 2024-10-15
additional_resources:
  - title: 'PR #31003'
    url: https://github.com/bitcoin/bitcoin/pull/31003
  - title: 'Issue #31002'
    url: https://github.com/bitcoin/bitcoin/issues/31002
---
Main use case is a Stratum v2 client connecting over IPC.

Most of the proposed interface is already merged:
[https://github.com/bitcoin/bitcoin/blob/master/src/interfaces/mining.h](https://github.com/bitcoin/bitcoin/blob/master/src/interfaces/mining.h)

Open PR to add waitFeesChanged: [https://github.com/bitcoin/bitcoin/pull/31003](https://github.com/bitcoin/bitcoin/pull/31003)

We walked through the interface.

Discussion about memory management: any time getBlock is called the node creates a new block template, which contains many transaction references. If the mempool drops these transactions they’ll stay in memory. How to limit the additional memory footprint?

1. Add interface method to request current memory usage
2. If memory usage exceeds some (configurable) value, refuse to make more templates.

Leave it to client to choose which templates to drop to free up memory. If a nonce is found for such a template, the resulting block can no longer be reconstructed and broadcast. We also can’t assume that all ASIC’s are mining on the most recent template. So this choice is a very mining application specific decision. 

Questions:

- What is the scriptpubkey argument for, and is it used outside of solo (CPU) mining?
- Should the current fees, or template, be passed to waitfeeschanged?
- Should getTransactionsUpdated, processNewBlock and/or testBlockValidity be dropped, since sv2 doesn’t use them? (but getblocktemplate RPC does)
- Does Datum need any interface changes? So far no answer [https://github.com/bitcoin/bitcoin/issues/31002](https://github.com/bitcoin/bitcoin/issues/31002)
