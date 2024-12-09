---
title: Mempool Optimization
date: 2024-11-20
tags:
  - cluster-mempool
---

### Problem description

Bitcoin today uses some mempool algorithms that date back to about a decade ago. These algorithms use heuristics which compute the descendent set with the lowest fee rate. The existing algorithms don't address multiple children paying for a parent, or one child paying for multiple parents adequately.

It is desirable to design new algorithms that yield a total ordering of transactions. In particular, the first to mine is the last to remove, depending on the space constraints of the mempool. Also, the first to remove is the one with the lowest fee rate, i.e., fee divided by size.

### Assumptions

- Truth-telling fees. Not considering pinning attacks. Not considering incentive compatibility.
- Knapsack problem with exact block size is to be ignored. The boundary effect is minor as a block typically accommodates many transactions. (Solution for an exact size is also hard.)
- Cluster size is bounded from above, e.g., 64 transactions at most.

### Question: Can we quantify how good an ordering is? Can we compare two orderings?

Use a fee-size diagram. For every size, what’s the cumulative fee? A convenient simplification is to think of the convex hull of all fee-size curves achieved by all possible topologically consistent orderings. According to Pieter, an optimal topological ordering of all transactions exists.

Using the convex hull, the problem is not quite a knapsack problem because the transactions are much smaller than the total block size.

The challenge is to design an algorithm for computing the ordering within a cluster. There already is an efficient algorithm for merging clusters.

- Question: What about attacking security by displacing some clusters?

This is interesting as a separate investigation.

It’s suggested the problem (and solution) may have to do with matroids.

A linear program is also proposed for solving for the first group with the highest fee rate:

$
\text{Maximize} \quad \frac{\sum_i f_i x_i}{\sum_i s_i x_i}
$

Subject to:

$
0 \leq x_i \leq 1 \text{ for every } i
$

$
\sum_i x_i > 0
$

$
x_i \geq x_j \text{ if } i \text{ is j’s parent}
$
