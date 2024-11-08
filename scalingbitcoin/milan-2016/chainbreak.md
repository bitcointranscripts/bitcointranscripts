---
title: Chainbreak
transcript_by: Bryan Bishop
---
<div id="table-of-contents">
<h2>Table of Contents</h2>
<div id="text-table-of-contents">
<ul>
<li><a href="#sec-1">1. braids</a>
<ul>
<li><a href="#sec-1-1">1.1. Properties of a braid system</a>
<ul>
<li><a href="#sec-1-1-1">1.1.1. Inclusivity</a></li>
<li><a href="#sec-1-1-2">1.1.2. Delayed tx fee allocation</a></li>
<li><a href="#sec-1-1-3">1.1.3. Network size measured by graph structure</a></li>
<li><a href="#sec-1-1-4">1.1.4. cohort algorithm / sub-cohort ordering</a></li>
<li><a href="#sec-1-1-5">1.1.5. outstanding problem - merging blocks of different difficulty</a></li>
</ul>
</li>
<li><a href="#sec-1-2">1.2. fee sniping</a>
<ul>
<li><a href="#sec-1-2-1">1.2.1. what even is fee sniping?</a></li>
</ul>
</li>
<li><a href="#sec-1-3">1.3. definition of a cohort</a></li>
<li><a href="#sec-1-4">1.4. tx processing system must process all txs</a></li>
<li><a href="#sec-1-5">1.5. can you have both high blocktime and a braid?</a>
<ul>
<li><a href="#sec-1-5-1">1.5.1. problem is double spends</a></li>
<li><a href="#sec-1-5-2">1.5.2. two ways to get paid - inflation, and tx fees</a></li>
<li><a href="#sec-1-5-3">1.5.3. braids are a constant-factor improvement, not "scalability"</a></li>
</ul>
</li>
</ul>
</li>
<li><a href="#sec-2">2. Bitcoin conflates source-of-scarcity with source-of-value</a></li>
<li><a href="#sec-3">3. treechains</a>
<ul>
<li><a href="#sec-3-1">3.1. goal</a>
<ul>
<li><a href="#sec-3-1-1">3.1.1. miners are working as a team to make replay/rewind of history difficult</a></li>
<li><a href="#sec-3-1-2">3.1.2. we want to make their job easier, so they don't have to track everything to contribute to this effort</a></li>
</ul>
</li>
<li><a href="#sec-3-2">3.2. how do you keep your spot?</a></li>
<li><a href="#sec-3-3">3.3. potentially infinite depth of chains</a></li>
<li><a href="#sec-3-4">3.4. this is a proof-of-publication system</a></li>
<li><a href="#sec-3-5">3.5. everyone has top chain</a>
<ul>
<li><a href="#sec-3-5-1">3.5.1. broadness of chain backups decreases as chain depth increases</a></li>
</ul>
</li>
<li><a href="#sec-3-6">3.6. you can pick which depth you target based on your hashpower</a></li>
<li><a href="#sec-3-7">3.7. validators don't know validity, but do notice changes</a>
<ul>
<li><a href="#sec-3-7-1">3.7.1. does including data in your block reduce the chance other miners will build on it?</a></li>
</ul>
</li>
<li><a href="#sec-3-8">3.8. validity of separate outputs within a single transaction is independent?</a>
<ul>
<li><a href="#sec-3-8-1">3.8.1. transactions must specify precise flow from each input to each output</a></li>
</ul>
</li>
<li><a href="#sec-3-9">3.9. treechains could be implemented with bitcoin as the root - undetectably</a>
<ul>
<li><a href="#sec-3-9-1">3.9.1. don't need to put all data in the chain, only commitments</a></li>
</ul>
</li>
</ul>
</li>
</ul>
</div>
</div>

# braids<a id="sec-1" name="sec-1"></a>

## Properties of a braid system<a id="sec-1-1" name="sec-1-1"></a>

### Inclusivity<a id="sec-1-1-1" name="sec-1-1-1"></a>

Equal pay for equal proof-of-work

### Delayed tx fee allocation<a id="sec-1-1-2" name="sec-1-1-2"></a>

You can't allocate tx fees until you see the state of the network

1.  do you split fees?

    1.  if you don't, you can fee-snipe

    2.  if you do, smart wallets will cheat the fee reallocation

        1.  smart wallets that pay specific miners compromise centralization

        2.  tx fees should be the best way to get your tx confirmed

    3.  could eliminate gossip broadcast of txs ("p2p layer")

        1.  PoW required to get any transaction confirmed

        2.  PoW started as a spam prevention mechanism, becomes this again

    4.  "deep mempool"

        situation in bitcoin today - more txs waiting than the content of a block

        1.  arguably you always have this, because there is always demand for backing up data, at a lower price

### Network size measured by graph structure<a id="sec-1-1-3" name="sec-1-1-3"></a>

1.  cohort can only be delineated once no blocks appear for a certain period

2.  can a system not depend on cohort delineation?

    (yes - that's Jute)

### cohort algorithm / sub-cohort ordering<a id="sec-1-1-4" name="sec-1-1-4"></a>

### outstanding problem - merging blocks of different difficulty<a id="sec-1-1-5" name="sec-1-1-5"></a>

1.  question of how bead/block difficulty is determined

    1.  chains are synchronous, block is a network-wide event

    2.  braids are parallel, beads appear simultaneously

    3.  can difficulty & reward algorithms have multiple values at different points in the graph?

## fee sniping<a id="sec-1-2" name="sec-1-2"></a>

### what even is fee sniping?<a id="sec-1-2-1" name="sec-1-2-1"></a>

1.  miner sees high-fee tx in one block

2.  makes competing block with same tx

## definition of a cohort<a id="sec-1-3" name="sec-1-3"></a>

series of blocks where everything before is an ancestor of everything that comes after

## tx processing system must process all txs<a id="sec-1-4" name="sec-1-4"></a>

tx never sits in limbo indefinitely

## can you have both high blocktime and a braid?<a id="sec-1-5" name="sec-1-5"></a>

### problem is double spends<a id="sec-1-5-1" name="sec-1-5-1"></a>

double spending is free

1.  use a miner

2.  try to double-spend

3.  in bitcoin, if you get 5 out of 6 blocks but fail on the 6th, your 5 blocks' worth of work is wasted

4.  in an inclusive DAG, you submit those blocks late, and still get paid

### two ways to get paid - inflation, and tx fees<a id="sec-1-5-2" name="sec-1-5-2"></a>

### braids are a constant-factor improvement, not "scalability"<a id="sec-1-5-3" name="sec-1-5-3"></a>

# Bitcoin conflates source-of-scarcity with source-of-value<a id="sec-2" name="sec-2"></a>

# treechains<a id="sec-3" name="sec-3"></a>

## goal<a id="sec-3-1" name="sec-3-1"></a>

### miners are working as a team to make replay/rewind of history difficult<a id="sec-3-1-1" name="sec-3-1-1"></a>

### we want to make their job easier, so they don't have to track everything to contribute to this effort<a id="sec-3-1-2" name="sec-3-1-2"></a>

## how do you keep your spot?<a id="sec-3-2" name="sec-3-2"></a>

## potentially infinite depth of chains<a id="sec-3-3" name="sec-3-3"></a>

## this is a proof-of-publication system<a id="sec-3-4" name="sec-3-4"></a>

## everyone has top chain<a id="sec-3-5" name="sec-3-5"></a>

### broadness of chain backups decreases as chain depth increases<a id="sec-3-5-1" name="sec-3-5-1"></a>

## you can pick which depth you target based on your hashpower<a id="sec-3-6" name="sec-3-6"></a>

## validators don't know validity, but do notice changes<a id="sec-3-7" name="sec-3-7"></a>

### does including data in your block reduce the chance other miners will build on it?<a id="sec-3-7-1" name="sec-3-7-1"></a>

## validity of separate outputs within a single transaction is independent?<a id="sec-3-8" name="sec-3-8"></a>

### transactions must specify precise flow from each input to each output<a id="sec-3-8-1" name="sec-3-8-1"></a>

## treechains could be implemented with bitcoin as the root - undetectably<a id="sec-3-9" name="sec-3-9"></a>

### don't need to put all data in the chain, only commitments<a id="sec-3-9-1" name="sec-3-9-1"></a>
