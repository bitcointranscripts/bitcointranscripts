---
title: Wallet / Chain tracking
tags:
  - bitcoin-core
  - wallet
date: 2025-02-25
---

- There is a wallet crash that was observed on testnet (explained in
  [#31824](https://github.com/bitcoin/bitcoin/pull/31824))
- Needs a combination of a reorg and an unclean shutdown to be triggered.
- Crash fixed in [#31757](https://github.com/bitcoin/bitcoin/pull/31757), but
  even after, the wallet can have a wrong balance ->
  [#30221](https://github.com/bitcoin/bitcoin/pull/30221) would resolve this
- Root issue: wallet transaction data is synced with disc continuously, best
  block locator only on chainstate flushes -> mixed state in case of unclean
  shutdowns
- Two ways to deal with it:
  - It could be acceptable, but then we’d need a cleanup process in addition to
    rescanning that would iterate over all inactive / abandoned transaction on
    restart and check if they may actually be in the chain.
  - Or, we could change the syncing behavior such that the best block locator is
    flushed whenever we change something in a block. -> this direction seemed to
    be preferred by participants
- Flushing the best block locator during IBD for each block could be bad for
  performance
- Next steps: Adapt #30221 to not update the block locator for each block, but
  always update it if the block affected the wallet
- Related but separate topic: Batching of effects of block connection
