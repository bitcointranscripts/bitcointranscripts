---
title: Remove the legacy wallet and updating descriptors
tags:
  - bitcoin-core
  - wallet
date: 2023-09-21
speakers:
  - Andrew Chow
---
## Wallet migration + legacy wallet removal

The long-term goal targeted for v29 is to delete BDB and drop the legacy
wallet. The migration PR for the GUI was just merged recently, so that
will be possible for the next release v26. The "Drop migratewallet
experimental warning" PR (#28037) should also go in before v26.
Migrating without BDB should be possible for v27 (PRs "Independent BDB"
[#26606](https://github.com/bitcoin/bitcoin/pull/26606) and "Migrate without BDB" [#26596](https://github.com/bitcoin/bitcoin/pull/26596)). Priority PRs for now are:

- [#20892](https://github.com/bitcoin/bitcoin/pull/20892) "Both wallet types in each test case"
This PR solves the annoying problem of having to run wallet tests twice
for both descriptor and legacy wallet individually in the functional
test framework.

- [#26008](https://github.com/bitcoin/bitcoin/pull/26008) "Caching for migrated non-HD"
Wallet with non-ranged descriptors have a poor performance right now,
this PR fixes that.

- [#28037](https://github.com/bitcoin/bitcoin/pull/28037) "Drop migratewallet experimental warning" (goal v26)
- [#28027](https://github.com/bitcoin/bitcoin/pull/28027) "Backwards compatibility tests"
- [#26606](https://github.com/bitcoin/bitcoin/pull/26606) "Independent BDB" (goal v27)
- [#26596](https://github.com/bitcoin/bitcoin/pull/26596) "Migrate without BDB" (goal v27)

PRs for "Stop making legacy" and "Delete BDB, drop legacy" are not
available yet. These will be 2-4 PRs, the goal is to have them in at the
start of 2025.

A: Can't we remove the legacy wallet earlier?
B: Okay, let's move everything up one release, so the goal is v28.

Batching DB writes should be done before v27.0, a PR for that will be made available soon.

## Descriptor wallet upgrading

If you made a taproot wallet before taproot activation, it's not
possible to add a taproot descriptor until you do it manually. These two
PRs solve this issue:

- [#26728](https://github.com/bitcoin/bitcoin/pull/26728) "wallet: Have the wallet store the key for automatically generated descriptors"
- [#25907](https://github.com/bitcoin/bitcoin/pull/25907) "wallet: rpc to add automatically generated descriptors"
