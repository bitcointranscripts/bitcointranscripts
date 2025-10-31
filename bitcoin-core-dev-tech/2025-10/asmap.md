---
title: ASMap
tags:
  - bitcoin-core
  - asmap
date: 2025-10-22
---

- Kartograf - is a tool that gets data from resources and builds the map (it’s a
  deterministic process and depends on RPKI)
- Asmap-data is a repository where the maps are stored (we usually do
  collaborative launches) - a timestamp is specified to do the launch. It’s
  required everyone to start at the same exact time. People post the results
  (hash) and we check if the hashes have matched. We expected 5 people (at
  least) attending and we expect a majority of people with same results.
- It’s hard to interpret the diffs between the results.
- We try to do it on the first IRC meeting of the month.
- The result of kartograf is a raw file and we use Pieter’s algorithm to encode
  it.
- “Is it filled or unfilled?” - We usually upload both! 
- RPKI is just the primary source, there are other ones.
- “Other P2P protocols use it?” - There are commercial services that does it as
  service, we haven’t found any open source project doing something similar as
  us.
- “Should we put it in binary?” - PR is open for review. The encoding/decoding
  code is the hardest to review. We agreed a documentation (or better
  documentation) would be very valuable. 
- It will be released once per release (major release).
- With PCP we can have more listening nodes.
- `-asmap` option accepts a boolean or the path to the map file. 
- On master, `-asmap=1` looks for the default file. 
- We agreed that separated options would be better. It’s already done in the
  Fabian’s PR.
- ASMap makes the attack specified in
  https://delvingbitcoin.org/t/eclipsing-bitcoin-nodes-with-bgp-interception-attacks/1965
  harder.
