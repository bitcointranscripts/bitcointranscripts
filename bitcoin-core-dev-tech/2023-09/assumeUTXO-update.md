---
title: AssumeUTXO Update
tags:
  - bitcoin-core
  - assumeutxo
date: 2023-09-20
---
- One remaining PR
  - [#27596](https://github.com/bitcoin/bitcoin/pull/27596)
  - Adds loadtxoutset and getchainstate RPC, documentation, scripts, tests
  - Adds critical functionality needed for assumeutxo validation to work: net processing updates, validation interface updates, verifydb bugfix, cache rebalancing
  - Makes other improvements so pruning, indexing, -reindex features are compatible with assumeutxo and work nicely
  - Adds hardcoded assumeutxo hash at height 788,000
    - Probably this should be moved to separate PR?

- Questions about initial next steps (unanswered):
  - Which release is this PR targeted for?
  - Does it make sense to merge code changes first, then hash later?
  - Maybe staged rollout makes sense? First merge code changes, then merge hash, then distribute snapshots?
    - Assumeutxo is a new feature which needs testing.
    - Start by merging functionality but require modifying source to actually use it.
    - Then add hardcoded hash and let binary users create snapshots, verify snapshots, and load snapshots.
    - Later work on distributing snapshot files, making the feature more accessible.

- Longer term questions
  - Should snapshots hash be configurable, allowed to be specified on command line?
    - Potentially risky to allow but not allowing might incentivize using unofficial builds
  - Should other hashes by added or supported?
    - Muhash would make it a easier for someone running a node to verify snapshot hashes hardcoded in source code are correct, because no it will no longer require rolling back chainstate
    - Bittorrent infohash could be distributed outside of source so user can know they are using the right torrent without having to download the whole thing and try to load it with the RPC
  - Should hashes eventually be removed from source code?
    - Having snapshot hashes could be considered a regression, since we are in the process of removing checkpoint hashes
    - Having snapshot hashes potentially incentivizes modified Bitcoin Core binaries that provide more recent snapshots that could be malicious
  - Should source code contain only one snapshot hash, or historical snapshots?
  - Concerns about no one validating the hash
    - Future Bitcoin developers could provide invalid hashes
    - The attack would be a public, non stealth attack
    - Switching to muhash could make it easier for more people to verify the hash
  - P2P way of distributing snapshots and hashes separate from source distribution
    - Have a new hash every 50,000 block
    - Or some other fixed N blocks
    - Release would have the most recent one
    - One of the original ideas was distributing over the P2P network

- Misc
  - Reliability of stop at height
  - Jameob’s makesnapshot script resolves this
