---
title: Mempool Clustering
tags:
  - cluster-mempool
date: 2023-04-25
aliases:
  - /bitcoin-core-dev-tech/2023-04-25-mempool-clustering/
speakers:
  - Suhas Daftuar
  - Pieter Wuille
---
## Current Problems

lot of problems in the mempool

1. eviction is broken
2. mining algorithm is part of the problem, it’s not perfect
3. RBF is like totally broken we complain all the time, sometimes we do/don't RBF when we should/shouldn't

## Eviction

- Eviction is when mempool is full, and we want to throw away the worst tx.
- Example, we think a tx is worst in mempool but it’s a descendant of a "good" tx.
- Mempool eviction is kinda the opposite of the mining algorithm.
- For example the first thing you'd evict may be the first tx you'd mine
- The first thing you'd evict is the small fee parent, but its descendant fee rate is desirable for mining.

## Mining algorithm has problems

- Mining algorithm is something we can't run in reverse
- What you wanna do is run mining algorithm on whole mempool - look at top for block, bottom for eviction, but this won’t work because of processing time.

- We don't know what fee rate tx will be included in blocks.
- The current mining algorithm is quadratic - infeasible for mempool eviction

## RBF

- Compare incoming fee rate tx with conflicting tx
- We do NOT look at the child tx fee rates
  - PR [#26451](https://github.com/bitcoin/bitcoin/pull/26451) starts to fix this
- BIP125 rules are a bit silly (e.g. no new unconfirmed parents)
- None of the fee rates we talk about in mempool tell us where a tx will end up in a block

"so let's do that"

## TOTAL ORDERING

- These are improvements to block mining will also then improve mempool eviction, etc
- This should make RBF much much better
- Eliminate the uncertainty about how good a tx is
- We can compare 2 txs and decide which is better
- It won’t totally solve pinning, total fee rate rule is still an issue, v3 relay addresses that

- "obvious" solution - at all points in time, sort mempool
- ancestor fee rate solution is already n^2, optimal algorithm is clearly exponential, so that wouldn't work to run on whole mempool

- why don't we just limit size of connected components of mempool?
- Imagine the mempool is a graph, edges between parent/child txs
- Sort each connected component separately, then do something simple to merge all those together

- Clusters can’t affect each other because they are not connected

- Run quadratic algorithm on every connected component of the mempool

- This introduces a new policy rule
- Today there is no cluster limit, entire mempool could just be one huge cluster

- “Introducing”: cluster size limit. Is this something users can deal with?
- It could mean unrelated people have txs related by cluster

- Right now there is max 25 ancestor count
- We would probably still need an ancestor limit, but maybe not need a descendant limit anymore
- We might need some kind of carve out like CPFP too

## Definitions

- cluster: set of txs connected in graph
- linearization: any topologically valid sort of txs in mempool

- normally we talk about it within a cluster
- block building is linearization as well
- lots of ways to do this (ancestor feerate-based algorithm is what we use today)

- f(cluster) -> linearization
- This tells you in what order to include things

## Steps:

1. Identify clusters in mempool
2. linearize each cluster
3. ?

- hard part is done, we figured out the best strategy for all the dependencies
- block template - use that information to pull off the best fee rate parts of each cluster until block is full

## chunks

Given a linearization, we can calculate where the chunk breaks are, where we pick txs into the block. We always start at beginning, but only go in as far as you want to go to maximize fee rate. Look at all the prefixes to pick highest fee rate, everything is safe to cut off, but where is the most optimal cut point… always start on the left.

## Chunk Example

- where could this linearization have come from?
- Once you have the linearization, the original graph doesn't matter any more
- The linearization function adds redundant dependencies

## How do we calculate the chunks

Starting at the left, calculate fee rate as you go in to the block (moving to the right) fee rates go up, then down (stop at the peak point). For every prefix, you compute fee rate for each prefix
then see which prefix has the highest fee rate.
(It’s n values, not 2^n values because we respect the linearization sort)

1st chunk has been selected, now we look at fee rates for txs after the first chunk.
“example looks quadratic, but it is actually a linear algorithm”

## Back to Mining

- We get our clusters, we linearize the clusters
- (what do you do when you violate sigops limit ?!) we need a heuristic to prevent that from happening, i.e. use a modifier to multiply * tx size if we think the tx has more sigops than we think it should have. It’s significantly harder to include sigops because then you're optimizing for two values not just one.

- The problem still gets knapsack-y towards the end, maybe use packages that are small relative to the block

- Anyway, eviction is now the EXACT opposite of the mining algorithm.

- Chunks are usually descending in fee rate, because if they weren't - you would have merged those in to one chunk. Top chunk will be highest fee rate in the cluster. So for eviction, look at the last chunk in each cluster, therefore we evict the last things we would mine.

- The mempool always organizes chunks, mining picks top chunks, eviction picks bottom chunks.
Within a cluster, chunks are always decreasing fee rate. We can think of the mempool as just one giant list of chunks. We maintainthe data structure in mempool all the time, as new txs come in.

## RBF policy

- We ensure that chunk feerate of new thing is better than chunk fee rate of everything that would be evicted. By talking about chunk fee rate, we are using same score the mining algorithm uses. For a new tx, you look if it has parents and grab all the clusters. A new tx can merge clusters together. Throw new tx into the cluster, sort it, figure out which chunk new tx would be in, then you already have the mining scores of everything about to be evicted.

- So we can create a new mini mempool (just a fake virtual cluster) for each new incoming tx to test its cluster properties.

## "What about RBF carve out?"

- Virtual cluster is affected by cluster size limit as well. Each new incoming tx might merge clusters into a too-big cluster.

- Higher fee rate, higher total fee, we still need these rules for network DoS
- When you evict something, you need to re-linearize the cluster. We still need some kind of limit so we don't have to re-sort the whole mempool when RBF happens. The clusters don't have an ordering with respect to each other. We only sort the clusters during mining or eviction, but maybe we can optimize the tracking best chunk of each cluster.

- Each tx has its own chunk fee rate based on which chunk it appears in based on the cluster its in. This is its individual score, used for RBF.

## Revisiting Our Problems

- We no longer have asymmetry between mining & eviction
- If we limit cluster size enough maybe we could run the mining algorithm on the cluster

- "if you want to get your tx mined, don't make a cluster" ?
- It’s no longer simple to RBF your txs anymore. It doesn't matter though, people follow simple rules: "if you're paying more it'll get picked.” So… linearization algorithms should allow what people typically will do, maybe they CPFP with a few children. After that, it’s just about attack prevention. Can an attacker create a cluster that triggers not-incentive-compatible behavior?
An attacker can throw your tx into a large cluster.

## Open Questions I

- BIP 125 was rules and terms that users could understand, that produce deterministic results. You could tell ahead of time what will work, but yes you need a mempool to do so. This new approach is more opaque, running an expensive algorithm on the cluster, sorting, etc - turns the algorithm into a black box. We could have an RPC that returns the scores… BIP125 is already too hard to model, and it’s not incentive compatible. The thing that people do: “bumpfee, bumpfee, bumpfee” until it relays.

- "What is the cost of memory usage for this algorithm?"
  - We don't know, probably negligible.

- Just because we see large clusters doesn't mean anyone really needs them. Its probably OK to split up clusters between blocks. A cluster limit is worse than a descendant limit, but if you risk running in to one, you risk running in to the other.

- Maybe a user wants to fee-bump two separate txs but by bumping them, it joins two clusters together which now violates the limit. (open question)

- Maybe cluster limit is like 50 or 100, replacing descendant limit of 25

## Open Questions II

- sibling limit
- simple: reject anything that would bust cluster limit
- We’re punting on sibling eviction for now - could be another pinning attack where attacker can evict your tx by merging clusters, and we still have to manage total relay fee.

"next block fee rate" can be confusing now too, and coin selection gets harder if you're spending unconfirmed coins:

- Wallet need to figure out what cluster each coin is in
- Choosing coin A might re-score coin B that I might also want to use
- "That cluster is full so you can’t spend from it at all", etc

3rd parties cant make your tx score worse, only better

- When attaching more children, the parent tx can only get better score (until cluster limit is reached)

Optimal Sort vs Ancestor Sort

- maybe differently sized clusters get handed differently
- maybe miners optimize how they sort clusters better than relay nodes

Could there be a problem introducing non-determinism to the network?

- Are we going to break more stuff?
- The non-determinism doesn't matter, what matters is the baseline of what we guarantee:
- For example, we run the ancestor algorithm always, and then sometimes we do more
- Then no real use case can rely on anything higher than that bar

We had a hard time coming up with examples in which our mining algorithms don't do the right thing.

Maybe we can even relay sorted clusters, maybe someone has a better sort than you, let’s share it

A new tx comes in, we could just throw it on the end of its cluster and then re-linearize later. i.e. have multiple linearizations for same cluster, then merge them together.

## Open Questions III

- We take the worst chunk across all clusters and evict that chunk.
- "free relay problem" - if you can evict a chunk using only one new incoming tx, that’s bad.
- Maybe we need a chunk size limit and a cluster size limit
- We still need ancestor size limit currently its 101 kvb?

## Future Work

- Solve cluster size limits
- Downstream effects: positive impact on package relay and package validation
- Maybe we need to reconsider fee estimation overall (fee estimation is broken because of CPFP)

## DEMO time

y axis: total cumulative fee
x axis: total vBytes
"lol someones paying huge fees right now, messing up the chart!""

`getblocktemplate` is much faster with this
