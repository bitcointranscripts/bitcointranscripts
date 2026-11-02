---
title: pruneassumevalid
tags:
  - bitcoin-core
date: 2026-10-13
---

## Goal and proposed optimizations

The proposal combines pruning with `assumevalid` to obtain the UTXO set as quickly as possible, reducing historical data downloads and unnecessary disk I/O.

The starting argument was that, where `assumevalid` already skips script verification, a pruned node could avoid additional work:

- Downloading witness data.
- Building and saving undo data.
- Writing historical blocks to disk only to delete them shortly afterward.

These were proposed optimizations, not a description of existing behavior. The mode would remain one way to perform initial block download (IBD), rather than replacing all other synchronization options.

## Does this change the trust model?

The main disagreement concerned whether omitting further checks merely extends the existing `assumevalid` assumption or introduces a different kind of assumption.

Participants specifically questioned skipping witness-commitment and signature-operation-limit checks. The sigops discussion distinguished checking individual signatures from enforcing the block’s signature-operation limit: a block could theoretically violate that limit even if signature correctness was not being checked.

Some considered the additional sigops risk negligible in practice. Data availability prompted a more substantive objection.

With the proposed mode, the node would not have received the witness data at all. Participants argued that relying on others to have checked data is different from possessing that data but omitting some verification. The discussion therefore separated two concerns:

- **Validity:** whether skipped checks could allow an invalid historical block to be accepted.
- **Data availability:** what the node can establish about data it has never downloaded.

One characterization of `assumevalid` was “we trust proof of work.” That framing did not resolve whether omitting witness downloads stayed within its intended trust model.

## Configuration and user expectations

Participants noted that Bitcoin Core already exposes many configuration choices and that `assumevalid` itself can be confusing. Users may be surprised to learn that some historical script checks are skipped.

The proposed mode was explicitly framed around speed: obtaining the UTXO set as quickly as possible, rather than performing every historical check locally.

Making `assumevalid` non-default was raised as a possible improvement to the broader configuration model. The notes do not record agreement on that change or on how the new mode would be presented to users.

Two possible ways to perform additional work later were also raised:

- A “revalidate” option.
- Downloading witnesses in the background.

Neither idea was developed into a concrete design in the recorded discussion.

## Storage, out-of-order processing, and indexes

Avoiding block writes is not simply a matter of discarding each block immediately. Participants noted that storage supports out-of-order processing, so the proposal would need to preserve the buffering and ordering required for synchronization.

Indexes introduce another constraint. They do not have to remain at exactly the same height as validation, but they can lag and cannot run ahead. Before discarding data needed by an index, processing would have to wait for that index to catch up.

These dependencies limit how aggressively historical data can be discarded without being saved.

## Resource targets and motivation

A practical goal was to reduce the cost of syncing pruned nodes on inexpensive hardware, including addressing complaints that high-volume or “spam” data makes such nodes difficult to operate.

Participants pointed to larger witness data around block height 800,000 onward, alongside costly validation, as motivation for avoiding unnecessary work.

A configuration with approximately **1 GB of `dbcache` and a 1,024-block window** was described as accommodating machines with as little as **4 GB of RAM**. The notes do not include benchmarks or a detailed memory breakdown.

## Outstanding questions

The discussion left three main design questions open:

- Which checks and data downloads can be omitted without changing the intended `assumevalid` trust model?
- How can block and undo-data I/O be reduced while preserving out-of-order processing and index operation?
- Should users have a supported path to download omitted data or revalidate history later?

The core tension was between treating historical data as unnecessary work for a fast, pruned bootstrap and preserving the distinction between **skipping verification of received data** and **never receiving that data at all**.