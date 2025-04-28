---
title: Batch Validation + CheckQueue
tags:
  - bitcoin-core
  - batch-validation
date: 2025-02-27
---

## Prior Batch Validation Work

* A pull request (PR) for libsecp256k1 to implement batch validation (Strauss) seems abandoned; Fabian has rebased and is maintaining a branch, along with a Bitcoin Core PR.
  
  * Batch Validation PR in secp by siv2r: [bitcoin-core/secp256k1#1134](https://github.com/bitcoin-core/secp256k1/pull/1134)
  * Rebased branch maintained by fjahr, supports cmake now: https://github.com/fjahr/secp256k1/tree/pr1134-rebase-2024
  * Batch Validation PR in Bitcoin Core by fjahr: [bitcoin/bitcoin#29491](https://github.com/bitcoin/bitcoin/pull/29491)
* Novo created both a benchmark and a multithreading patch, but this approach may not be ideal long-term.
  
  * Novo patch to support multi-threading (benchcoin PR [bitcoin-dev-tools/benchcoin@173f07d](https://github.com/bitcoin-dev-tools/benchcoin/commit/173f07dc4493de3d3a9420f6a966606913277e9d)
  * Batch schnorr sigs of every vChecks allocation and verify afterwards
  * Batch size appears to be much smaller than optimal (probably)
  * `vChecks` may contain mix of schnorr sigs and non-schnorr sigs
  * Performance may behave differently with number of available threads
* Novo has been researching the potential performance gains from Schnorr signature batch validation, demonstrating that even with partial Schnorr usage there is a speedup, with greater potential if Schnorr becomes more widely used.
  
  * BlockConnect benchmark PR by Novo that has been used for this: [bitcoin/bitcoin#31689](https://github.com/bitcoin/bitcoin/pull/31689)

## Current Batch Validation Considerations

* Currently `check()` is self-contained. That needs to change to make this work.
* The current batch size of 106 in secp can be changed. Larger batch sizes might benefit from a different algorithm (e.g., Pippenger), which can offer more than a 20% speedup.
* Multithreading can help create batches in parallel, but we must consider overheads like public key loading and script interpretation.
* Larger batches could be more efficient, depending on the number of signatures. Large batches can also be created and verified in parallel
* One strategy might be to do a single large batch at the end of block validation, potentially splitting it into sub-batches if threads are available.
* Another strategy could be to have two types of queues (and `vChecks` handling): one for batching and one for non-batching, might not be necessary with Pippenger algorithm
* The script verification function could return both a result (pass/fail) and a list of signatures to be batch-verified later (i.e., `pair(bool, vector<signatures>)`)

## CCheckQueue (nNow) and Future Refactoring

* We need benchmarks to compare performance across varying numbers of available threads
* Is `nNow` calculation ideal even without batching?
  
  * "Try to account for idle jobs which will instantly start helping."
    
    * more idle means less allocation
    * But they can get started right away while we don't know when the other become available, so why not give them more work?
    * In the starting state all are idle necessarily, so in that case it seems like we should be able to give them larger numbers than we do
  * Benchmark different `nNow` algorithms
  * (demonstration with logging of sync to tip that more work is given to threads when less idle threads are available, agreement that this is not ideal)
* The nNow variable in the code could be refactored for clarity, and scheduling more work when fewer jobs are idle might boost performance.
* A lock-free CheckQueue would support truly parallel processing, avoiding bottlenecks. Hebasto previously worked on such an implementation (PR #9938).
* Although earlier benchmarks did not show large speedups, revisiting and refining a lock-free approach could yield benefits—especially if the design also supports batch validation in the future.
* A good next step would be to benchmark the current implementation with different script verification threads (e.g., [1,2,...16])
