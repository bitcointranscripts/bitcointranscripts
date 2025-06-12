---
title: Block Validation Logic
tags:
  - bitcoin-core
date: 2025-02-27
---

There are multiple stages to validating a block:

- [1) Header Received](#1-header-received)
- [2) Receive full block](#2-receive-full-block)
- [3) Connect block](#3-connect-block)

The three steps can happen in different orders. In IBD, we first receive all the headers up to `Consensus::Params::nMinimumChainWork` before we ask for any blocks. Then we download up to 1024 blocks ahead of time, so we may be missing a block's predecessors. So the steps cannot be done sequentally. This is also why the IBD logs are "janky": sometimes nothing happens for a few seconds (because blocks are being downloaded), and then suddenly a lot of blocks can be connected. Downloading can be in parallel, but validation needs to be sequentially.

Downloading a block does partial validation of the block, but we cannot do certain checks such as whether a block's transaction spend from non-existing outputs until we've built the chain.

But for each step, the fact that we have first received the header is helpful. Some historical bugs in 2) and 3) can only be triggered by miners, because we first need a valid header (which requires PoW).

Three ways block validation gets triggered
- In IBD, we first do download all the headers (i.e. step 1). Then, steps 2) and 3) occur in random order
- In post-IBD, when a new block is announced, we got through 2) 3) sequentally (we don't first request the header separately)
- In reindex, we only do 3)

### 1) Header Received

If something fails here (i.e. the header is invalid), it's like it never happened. We don't cache any failures.
If header validation succeeds, we insert it into `m_block_index`, and set `nStatus` to `BLOCK_VALID_TREE`. `BLOCK_VALID_TREE` means that the header is valid on itself, and als that it points to a valid previous header (which in turn points to a valid header, etc). This also means that if a block (header) later gets invalidated (e.g. through RPC), we iterate over all the later header, and invalidate them. However, even though we don't store/cache invalid headers when received from peers, we do keep (now invalidated) headers in `m_block_index` when they were first valid but then later invalidated. `invalidateblock` should be a very rare occasion, so we won't focus on it too much more here.

### 2) Receive full block

`ProcessNewBlock()` first calls `CheckBlock()`. `CheckBlock()` does quick, context-free checks. If it fails, it doesn't mark the block as invalid, but it just ignores it. We do this because we could have received a mutated block for an otherwise valid header.

If `CheckBlock()` succeeds, `AcceptBlock()` is called, which in turns calls `AcceptBlockHeader()`,  `ContextualCheckBlockHeader()` and `ContextualCheckBlock()`. We the save the block to disk, and call `ChainstateManager::ReceivedBlockTransactions()`, updating the `nStatus` to `BLOCK_VALID_TRANSACTIONS` and updating `Chainstate::setBlockIndexCandidates`. We now have all the data that would in principle allow us to connect the block (if it were part of the most-work chain).

Finally, we call `ActivateBestChain()`. It's a function that doesn't require any input, but takes an optional _hint_ to help it find the best chain more efficiently (but will ignore the hint if it's wrong). It just tries to get the chainstate to the place where it has the most-work chain.

### 3) Connect block

`ActivateBestChain()` calls `Chainstate::FindMostWorkChain()`, which gives the most-work block that we want to get to. In this process, we may call `DisconnectBlock()` if we need to re-org, and then call `ConnectBlock()` to make progress to the new tip. When the block is connected, `nStatus` is updated to `BLOCK_VALID_SCRIPTS`.

Currently, `ActivateBestChain()` is blocking, so `ProcessNewBlock()` can not return until we've connected to the most-work chain. There is ongoing discussion to run `ActivateBestChain()` in a separate thread, so networking can continue during this process.

`ActivateBestChain()` has two loops, the inner one of which calls `ActivateBestChainStep()`.

`m_best_header` is not guaranteed to point to the best header, but this is not currently used in any consensus-critical codes. For example, it is used for AssumeValid to check if we're close enough to start validating scripts again, and for certain RPC calls. But iterating over the block index to find the best header is quite expensive, so until now we've been okay with this. However, with new headers pre-sync algorithm, we know that headers have valid PoW which reduces the DoS vector of this attack.
