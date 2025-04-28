---
title: Macro Benchmarking
tags:
  - bitcoin-core
  - benchmarking
date: 2025-02-25
---

Add a macro benchmark suite with longer-running operations, exercising a
different set of functionality that is performance-critical.

* One of them could be the speed of an assumeUTXO load-and-dump (this would
  check block read/write and (de)serialization, but only part of validation).
* Another one could be an actual IBD for 840-880k blocks (small part of IBD, but
  should produce a representative comparison quickly).
* Another one would be a reindex-chainstate up to e.g. 880k blocks (more
  realistic, but takes long and doesn't involve reading/writing blocks).
* Lastly, several full IBDs to make sure the previous quick checks are
  representative (likely only required for big changes). We don't have to run
  all of these for every PR; it could be tied to labels added to PRs where the
  author/reviewers think they're relevant (e.g., not for doc typo fixes). This
  would require integration with CoreCheck.

### Other suggested macro benchmarks by the participants

* Compact block reconstruction: Set up a node by syncing to e.g. 840k blocks,
  loading transactions from the following blocks into the mempool, and benchmark
  replaying compact block announcements for those blocks, measuring its
  performance (we could test empty/full mempool cases or ratios suggested by
  data collected by B10C).
* Data collection: We need to ensure the macro benchmarks are realistic and rely
  on existing data instead of guesses.
* Kernel block-linearization-based script instead of IBD: Eliminate the
  unpredictability of IBD over the network from actual nodes. We can have a
  quick benchmark leveraging the Bitcoin Kernel project to load/save/validate
  blocks. This may make the runs more reliable, but less realistic.
  Alternatively we can create a simple node that serves local blocks to the node
  under test.
* We shouldn't use assumeUTXO (a user-facing feature) for benchmarking code;
  instead, copy the data dir or use the Kernel project. Alternatively, we could
  reconstruct the starting condition via a local IBD up to the assumeUTXO height
  using a kernel-based script (just copy the blocks and construct the state
  without any validation, rather than actual assumeUTXO or blocks-dir-copy),
  then run the benchmarks using this state.
