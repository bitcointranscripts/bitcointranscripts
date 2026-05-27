---
title: "SwiftSync: Hints File, Utreexo Overlap, and Path to the Kernel"
tags:
  - bitcoin-core
  - utxo-set
  - kernel
date: 2026-05-08
---

*Notes from an in-person discussion on SwiftSync — covering hints file
encoding, the relationship with Utreexo, BIP drafts, and how this fits
with the kernel project.*

## The Hints File

The naive encoding of the hints file weighs in somewhere around **450
MB** — not great. Over the last few months, time was spent looking at
different encoding schemes:

- Current best: **~116 MB**, with some overlap with ASMap-style
  encoding.
- Further research indicates compression down to **~90 MB**.

That seems to be the bound: **90–100 MB**. Pretty decent — technically
below the git commit size.

### Distribution: Bundle or Download?

The most conservative thing to do would be to just **hash the file and
download it externally**, following the same model as AssumeUTXO.

> Can't you bundle it? In theory, yes — but there's some anxiety about
> adding blobs to the build process.
>
> How is that different from bundling ASMap? ASMap is much smaller.

## Fully Validating SwiftSync

The fully validating case needs to rebase on **sans-IO block
validation**, where you just pass a vector of coins. If you're
interested in this, it trickles back to that PR.

### Insight from the Utreexo People

Outside of Core, the Utreexo folks discovered/thought through something
useful: the state of their "forest" accumulator has a nice property —
if you add an element and later remove it, it's as if you never did
anything at all. The root before and after is the same.

**You can abuse that property to do SwiftSync.**

The mechanics:

- Some UTXOs will survive (as indicated by the hints file).
- Everything else has a position it *would have been at* in the forest
  had it not been removed — but you still have to remember enough to
  hash it up at the end.
- For surviving UTXOs: remember the hash.
- For non-surviving (spent) outputs: remember where they would be in
  the tree.
- At the end, combine them to get the root hash.

This lets them **circumvent downloading the historical proofs**.

### "Proofless" Utreexo

Once you hash everything up at the end of SwiftSync, you're also left
with the Utreexo accumulator. This was discussed on the MIT livestream
with Tadge.

Effectively, this is **proofless Utreexo**: they don't care if there's
a proof for the leaf, they just do SwiftSync and then only request
proofs thereafter. This brings the bandwidth way down.

### Full Validation Performance

Utreexo leaf data is exactly the **undo data**. So they can do the
fully-validating version with the kernel, where they use it to actually
check scripts as they're doing SwiftSync. Interested to see the actual
performance when doing full validation.

## Draft BIPs

Three BIPs have been drafted. The first two are **implementable without
SwiftSync**:

- The hints file — even if we don't actually trust it — can still be
  used **optimistically to cache coins efficiently**. If we know a coin
  is going to be in the final UTXO set, write it straight to disk and
  don't waste memory on it. Someone could slow you down by trying to
  make you read it, but that's the worst case.

### Open Question

> Is that useful? How many cache misses do we get? Does this actually
> give us speedups?

## Distribution Realities

Regarding files sourced outside Bitcoin Core: **it just doesn't happen
in practice**. It might be worth going straight for **P2P sharing**.

## Relationship with the Kernel

The general approach with the kernel is to keep it **unopinionated**.
With AssumeUTXO, the feature is baked into the kernel, which makes it
hard to stay unopinionated.

With SwiftSync, the question is: **how far are we from being able to
live outside the kernel?**

We'd need something like a **sans-IO block evaluator** — and it's not
clear if that updates the UTXO set. That's where it gets hairy: we'd
want the block validation model to be separated from IO. The same is
true for Utreexo. That's the direction the kernel is going anyway.

Keep this in mind to make separation easier in the future.

## Interplay with AssumeUTXO

The UTXO set itself is a good hints set. You could still have
**background validation of AssumeUTXO** — there's some interplay if you
wanted to keep both, and they can benefit one another. Overlap between
users is potentially large.

### Limitation

One thing is that **you can't validate the undo data from the network**.

### Open Discussion: Committing to Undo Data?

Maybe there's some reason we'd want to **commit to the undo data**? If
we committed to everything we needed in blockwork, what would that
afford us? Worth discussing.

The case where you *can* trust it: if you were doing Utreexo normally,
you'd have proofs that those inputs were actually in the UTXO set — but
that requires the big bandwidth tradeoff. This has already been explored
as a way of getting around having to commit to anything.
