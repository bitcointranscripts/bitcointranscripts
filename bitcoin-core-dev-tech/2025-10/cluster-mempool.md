---
title: Cluster Mempool
tags:
  - bitcoin-core
  - cluster-mempool
date: 2025-10-20
---

Cluster Mempool consists of 3 layers:

- top: cluster linearization: a bunch of transactions with fees and
  dependencies, what's the right order to mine them in? This code is heavily
  algorithmic, and mostly completed.
- middle: TxGraph: a stripped-down mempool that only knows about fee/size
  dependencies, but has no full notion of what a transaction is. You can ask it
  what's the worst chunk to kick out, or to give the next group of transactions
  to include. The notion of staging exists: make changes (add/remove
  transactions), look at the staged diff to analyze what the changes mean, and
  then commit (or not accept it, e.g. if policy limits are violated).
- lower: mempool logic. Currently, mempool covers all 3 layers. Final PR is
  replacing existing logic with new TxGraph interface.

A couple of the indexes in multi-index will go away with cluster mempool:

- ancestor score
- descendant score

There is an orthogonal project of getting rid of the boost multi-index with an
in-house implementation by theuni, but that is not relevant here.

The descendant and ancestor limits will go away and are replaced with cluster
limits. Within the PR, there is a moment in-between commits where we have both
cluster limits and descendant/ancestor limits. This also means RPC error
messages etc will change.

PR (#33629) review: we need to have teams with different focuses, and make sure
everything is covered (e.g. reorgs, fuzzing, mining, ...). Same for docs,
release notes, ...

- fuzzamoto is going to be important here
- testing miner stack, making lots of templates

The idea of using an earlier-mentioned signet reorg approach was mentioned,
where signet would reorg every now and then. Signet transactions are made by
other people, but typically not very "natural-looking".

For people not very familiar with the logic, there are a lot of test commits
(incl bench etc) that are a good starting point to look at. They are well
structured and documented, and sometimes replace complex logic with simplified
logic that is easier to understand.

Do we have an overview of behaviour change? Not really, could be useful. Changes
include:

- computational limit guarding (ancestor/descendant -> cluster)
- RBF stuff (incl removal of carve-out)

Cluster limit is currently still set at 64. Cluster linearization algo does
pretty well on today's and historical transactions, but you can construct
pathological things that take minutes to linearize optimally (although it
wouldn't, because we use a computational budget (hard-coded ~CPU-cycles)), and
should never do worse than the current algo. Under non-adversarial situations,
literally everything should always be optimally sorted, so running the old algo
can seem like a waste.

RBF is very different with cluster mempool. E.g. instead of limiting the amount
of transactions that can be evicted, to limiting number of touched clusters
(100).

Are there any changes to CTxMempool's interface (also wrt kernel)? They should
be minimal, and the goal is to have minimal drag to get #33629 merged. Look at
the follow-up PR #33591, which slims down the interface.

Will cluster mempool change what the mempool contents look like? Unpredictable,
depends on usage. One notable use case is that currently, one parent can only be
bumped by one child, so that's how wallets implement it. With cluster mempool,
multiple children can bump a parent, so that may change user behaviour.

## Action items

- someone needs to go through all error messages (e.g. in RPC) and ensure they
  no longer reference descendant/ancestor limits
- writing comprehensive document of changes/release notes/FAQ
- review https://github.com/bitcoin/bitcoin/pull/33629 and
  https://github.com/bitcoin/bitcoin/pull/33591
- think about/organise review focus groups
