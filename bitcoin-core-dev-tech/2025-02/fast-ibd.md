---
title: Fast IBD
tags:
  - bitcoin-core
  - ibd
date: 2025-02-28
---

Idea is to speed up IBD by giving "hints" to whoever does it

- With Core, there would be some information that we give to every client that
  tells them whether or not an output is going to enter the utxo set
  - For simplicity take asssumevalid, you take the same points, the question is,
    once we reach that point, are the outputs gonna be in the utxo set, create a
    bitfield, 200mb of data, compressable because you have a bunch of 0s and
    very few 1s. Not going be much.
  - When you have this, on the output side, when it enters the utxo set, great,
    write it to disk, append-only
  - If it doesn't enter utxo set, spent by the time you reach that point, the
    question is what do you need in order to validate the spending of this
    output
- With assumevalid you can say, we dont need the scripts. the output scripts
  become irrelevant for the transition
- If we take some liberties with assumevalid and we take the remaining checks,
  e.g. coinbase output, you need height, and nsequence fields, you also need
  height.
  - We put them under the umbrella of assumevalid, dont need coinbase or height
    bits, can even the forgo the amounts. could be controversial. Would mean
    core no longer checking amounts. For simplicity leave that out. all that's
    left are the outpoints
  - All that's left is whether an outpoint was consumed - Nearly stateless.  A
    single MuHash where you add the hashed outpoints that didn't enter the utxo
    set
  - When checking the inputs you hash the outpoint and subtract it from the
    muhash
  - If the hints were correct, you end up with a muhash of 0
  - You could check the amounts too, but you would need to receive extra data
    (the amounts for each input) to support this
  - An extra 15gb? roughly, 2.5% more data. How you receive the data is not part
    of this discussion
  - Without checking the amounts is most elegant
  - This is 100% parallelizable
  - Doesn't matter if you remove the inputs first, then add the outputs, you
    still end up with 0
  - No disk writes other than writing the utxo set to disk. state is a single
    muhash
- To what extent is this diff from downloading utxo set? assumeutxo?
  - Still validating that outputs are spent once, dont check the scripts, dont
    check the spending happens after the creation of an output anymore?
  - Fundamental difference when you skip checking amounts: you don't check for
    inflation bugs
- Other than the order, everything else -- you don't need assumevalid - you need
  more data. 15% more
- We can at the end just sum the values in the utxo set, and make sure the 21M
  limit is preserved
- Are there any things in the utxo not taken into account? Burn coins?
- What if your helper data contains for every spent utxo you dont have just a
  bitset, but inform what height it was set. then you can add that height into
  the muhash commitments, and at spending time remove them. so if anyone lies
  about what has been spent it will be considered a failure
- If you add the heights at creation time and amounts at spending time, if you
  wanted to validate everything.
- If you were to check everything, it's 100GB. Now whenever you are checking the
  input, someone needs to give you the data (similar to utreexo), but more
  parallelizable
- Maybe similar to XYZ idea where you have utxo set where it just stores the
  hash of utxo, at spending time you change the block format to express which
  utxo you are spending. you can't do script validation statically. disentangle
  the utxo creation and removal. if you process things out of order you can
  store the hash of the utxo being spent as a spent-but-not-created-yet. utxo
  set contains both created but unspent output hashes but also spent but not yet
  created hashes, then you can process in any order. but significant bandwidth
  changes

- We could have this simple case vs complexity case, but maybe interesting
  tradeoffs
- Do version without assumevalid (AV) now you have more data, but could
  reintroduce a cache, e.g. some in cache so you dont have to re-download. Save
  bandwidth but lose some parallelization benefits

- Version with AV: for every input you need to download the entire output script
  (similar to other idea described XYZ).
- Version without AV: but now you download the UTXO set AND every output script.
  need to commit to more things

You can combine this with assumeutxo where you do background validation with ibd
and now you don't need two chainstates. Does mean you need this fast-IBD version
for assumeutxo

This could be extended even beyond the assumevalid point if you trust a third
party with further hints up to the tip, though this part would not use
assumevalid and thus use more bandwidth

Expect codebase to commit to these hints? YES

- Packing it together with the assumeutxo snapshot may make sense in this
  context.

Is MuHash performant enough?

- Even if slower, should be okay if throwing lots of cores at it?
- Perhaps it appears slower because the "finalize" step. Doing that on every
  block connection. But in this Fast IBD design you don't need to finalize
  except for once at the end. But possibility of overflow, so may need to
  finalize more than once (not often)
