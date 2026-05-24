---
title: Post Cluster Mempool, Mining, and Fee Estimation
tags:
  - bitcoin-core
  - mempool
  - mining
  - fee-estimation
date: 2026-05-06
---

Asynchronous mempool updates via validation interface

- Return mempool updates before and after the fee rate diagram. (of
  update affected chunk)
- To be used for efficient mining and chunk best block policy fee
  estimation

The changes needed are minimal

- Wire the chunk refs in GetMainStagingDiagrams

- Refactor GetPackageHash to a generic GetHashFromWitnessIds
- Cache the chunks returned from GetMainStagingDiagrams
- Extract the dependency addition of UpdateTransactionsFromBlock into
  it's function
- On each mempool mutation collect the witness id of all chunks
  removed/added reason for removal chunk fee rate and fire mempool
  updated validation interface notification

Most changes are straightforward, maybe, but it is worth going through
what the function each commit changes, and then we talked about it.

Commit 1 txgraph: populate chunk refs in `GetMainStagingDiagrams` result

- AppendChunks for Singleton we just grab the ref and fee rate and
  append it but for generic cluster we loop through the chunks and grab
  their refs. So we create and fill a 2D vector of Chunk and Chunk fee
  rates.
- GetMainStagingDiagrams: Computes the conflicts between the main and
  staging. Then get the chunks of these conflicting clusters. For
  staging, compute the chunk fee rate of the clusters in staging. All
  using AppendChunks, and return those vectors; This is what is used for
  replacement evaluation. tradeoff some vector additions.

Commit 2 refactor: move-only: split GetPackageHash Straighforward

Commit 3 mempool: cache fee rate diagrams as chunks in ChangeSet

Commit 4 mempool: add GetAndSaveMainStagingDiagram to ChangeSet

Commit 5 refactor: move-only: extract dependency addition into a
seperate method

Commit 6 refactor: move-only: extract dependency addition into a
seperate method

UpdateTransactionFromBlock is called during after a reorg has happen
and we collect all the transactions that are successfully added and
then call UpdateTransactionFromBlock with them.

We then addDependency between this transaction and all its children
that are in the mempool.

Then we trim if cluster limit is busted, so we extract the transaction
dependency addition into it's own commit.

Commit 7 mempool: add and fire MempoolUpdated signal on each mempool
update path
We add a new validation interface notification that is emitted on each
mempool mutation update.

On each mutation, we get the staging and main diagram chunks and then
emit a new notification.

In all cases the before/after chunks are obtained from
changeSet->GetFeeRateDiagramChunks() after committing the staging graph.

- Note on UpdateTransactionsFromBlock, a naive single-pass approach
  calling Trim() directly on the main graph fails because oversized
  clusters cannot be linearized, so GetMainStagingDiagram cannot
  produce a valid before/after diff. The fix is a two-stage process:
- Phase 1 (optimistic): Create a txgraph staging , call
  addDependenciesFromBlock to register all new parent-child
  relationship, then call Trim().
- If Trim() returns nothing — no cluster exceeded the limit, compute
  the diagram, commit staging emit MempoolUpdated(SIZELIMIT), done.
- If Trim() returns evicted transactions, the optimistic path failed.
  Abort the staging we roll back to main, open a fresh staging, call
  RemoveTransaction for each evicted tx to remove them from staging,
  call addDependenciesFromBlock again (evicted txs are silently skipped
  since they are no longer in the graph), commit, compute the
  before/after diagram, emit MempoolUpdated(SIZELIMIT), then call
  RemoveStaged to remove evicted transactions from the mempool fully.
- Reorgs are rare, and reorgs that burst the cluster size limit are
  also rarer still, so in the optimistic common case, we apply
  dependencies only once.
- We compute the chunk hash lazily in the scheduler thread because the
  mempool update is a hot path. see thread mempool: asynchronous
  mempool fee rate diagram updates via validation interface #34803
  (comment)

Commit 8 Added a new mempool_update_tests: unit test suite covering all
MempoolUpdated emission paths

We do not need the chunk IDs for the block template. We can track the
last index at which we start the bin packaging. All chunks with a fee
rate above that are in the block template, so we can use that directly
to compute the delta after the fee rate increase.
We still need the notification for using the suggested approach.
What's the motivation for using this approach instead of blocking the
template every 1 second, to avoid redundancy, and reduce memory usage
when the fee increase is not in the top block template?
