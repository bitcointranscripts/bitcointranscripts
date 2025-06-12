---
title: IBD
tags:
  - bitcoin-core
  - ibd
date: 2025-02-25
---

There were two sessions about IBD, these notes are from the first of the two
sessions.

Summary of what the facilitator presented:

The motivation for improving IBD performance is that it reduces the cost of a
node reaching the tip of the network, and with each marginal reduction in cost,
some new number of nodes or node operators that otherwise would not have joined
the network because of the associated costs do so.

Below the assumevalid checkpoint, IBD is generally bound by I/O, we are
validating that the inputs spent in blocks that we connect to the tip exist in
the UTXO set, which we cache in CCoinsViewCache, also called the dbcache, and
persist to disk using the leveldb CCoinsViewDB or coinsdb.

Two naive paths for improving the input fetching performance during IBD are:

Improving the coinsdb: A different KVDB than leveldb that has faster reads
and/or writes. Some investigation was done into whether LMDB, or MDBX might
improve IBD performance in bitcoin core, and while significant read performance
improvements were observed, write performance was bad enough to make the benefit
a little fuzzier. One hypothesis for the write performance issue is that because
entries are inserted sorted, and outpoints are close to random, on flushes we
end up dirtying almost every page in the b-tree, and are forced to do a utxo-set
sized write on each flush. There are also increased disk-space requirements that
might be unacceptable. There is more work to be done to investigate whether
there are designs that make the right set of tradeoffs that fit the needs of the
coinsdb.

Improving the cache:

Two directions that could be persued.

1. An improved caching strategy, in the vein of:
https://github.com/LarryRuane/bitcoin/issues/7, some kind of compact encoding of
hints for what coins won't be spent soon and should be flushed from the cache
first, and/or which coins will be spent soon and are worth hanging onto for a
little longer.
1. Making the cache more compact means we could fit more UTXO's in it, and have
to fall back to disk less frequently, one idea is that we don't need
scriptpubkeys when validating blocks below the assumevalid checkpoint, so we
might be able to flush them to disk when a coin would have otherwise been
dropped from the cache and hang onto the output for a bit longer while we are
below the assumevalid checkpoint.

One participant suggested that the size of the preallocated vector (currently at
28 bytes) used for scriptpubkeys is not large enough to fit P2WSH and P2TR
outputs, this results in a second allocation when these are stored in memory. In
the past, there were not enough of these outputs to justify the memory overhead,
but they suggest that things might be different now, and those interested in IBD
improvements should check this.

Another participant suggested dynamically sizing the prevector based on the
height, but someone said that they tried this and it might be too complex to be
worth it.

Later on, after the session, the conversation continued and one participant
suggested using a pointer to perhaps the txid, fCoinbase, and nHeight of a
transaction to save on redundant txid, fCoinbase, and nHeight (33 bytes) storage
in the per-outpoint model, where we duplicate this information for each
outpoint, without reintroducing the DOS vector of the old per-transaction model.

Another participant was supportive of work to improve IBD, but questioned
whether or not engineering resources are worth spending on the complexity of any
of these solutions when they could instead be spent on bringing AssumeUTXO over
the finish line, and a conversation ensued which sketched in broad strokes what
the missing peer-to-peer protocol for txoutset distribution might look like.
