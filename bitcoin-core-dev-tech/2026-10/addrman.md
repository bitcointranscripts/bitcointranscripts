---
title: How To Fix addr Relay and addrman
tags:
  - bitcoin-core
date: 2026-10-15
---

## Scope and observed behavior

The session examined address relay and its interaction with the address manager, `addrman`. The primary question was not how nodes select peers, but **how easily a newly reachable node can obtain inbound connections**.

A new node advertises its address, but that address must enter other nodes’ address managers before they can select it for an outbound connection. DNS seeds help new nodes find outbound peers; they do not directly solve the problem of attracting inbound connections.

In one reported test, obtaining connections from ordinary peers took almost three weeks, excluding connections attributed to monitoring nodes. Participants recalled this happening much faster a few years earlier. The observation motivated investigation, but was not presented as a network-wide measurement.

## Timestamp-refreshing spam

The reported spam involved an entity collecting gossiped addresses, refreshing their timestamps, and redistributing them. This could make an address appear fresh even if the node had changed IP addresses a month earlier.

Participants identified two consequences:

- Address-relay bandwidth is spent repeatedly circulating old information.
- Existing `addrman` entries remain apparently fresh, making it harder for newly advertised addresses to displace them.

The distinction was important: **address relay can successfully spread a new address without receiving nodes admitting it into `addrman`.**

Existing entries are generally retained unless they meet replacement criteria, including being classified as `IsTerrible`. Examples discussed included an address not being advertised for 30 days or accumulating failed connection attempts. Refreshing timestamps interferes with age-based removal; addresses that still work are also less likely to be classified as terrible.

The spammer’s motivation was unknown. Griefing or experimentation were suggested, but no conclusion was reached. Compared with flooding the network with fabricated addresses, recycling plausible or working addresses was considered harder to detect.

Participants also noted that these replacement rules were longstanding, with some changes made in response to eclipse-attack research. Changing them requires considering the protections they provide, not just their effect on turnover.

## What should timestamps mean?

Several proposals sought to separate address freshness from information supplied by remote peers.

One suggestion was to stop updating an entry’s timestamp after admission. Another was to remove timestamps from the P2P address format while retaining a local insertion time in `addrman`.

The discussion distinguished two uses of timestamps:

- **Relay:** timestamps support self-advertisement and a limited propagation window, described as approximately ten minutes.
- **Storage:** timestamps help determine whether an address is stale and eligible for replacement.

Changing one use would not necessarily require changing the other. For example, timestamps could remain part of relay while no longer controlling retention in the same way.

There were trade-offs. An honestly supplied old timestamp is useful information: a recipient can discard an already-stale address. Participants also raised the incentive to advertise future timestamps if a timestamp becomes a fixed basis for retention, potentially undermining its meaning.

Other possibilities included making entries become terrible sooner, applying periodic decay, or dropping a fraction of stored addresses over time. No replacement policy was selected.

## Propagation and address-manager saturation

Participants questioned whether every individual address announcement needs to reach the entire network. Because nodes advertise themselves repeatedly, any one announcement may only need to reach a subset of peers.

Alternative relay ideas included a hop counter, slower propagation, and forwarding addresses only when they had not previously been seen. One broader suggestion was to constrain propagation speed rather than rely primarily on expiration. Participants acknowledged that this would be a substantially different design and potentially difficult to reason about.

The discussion also considered whether new nodes receive their first connections mainly from other new nodes with available address-manager capacity. That possibility had not been measured.

Reportedly, the `NEW` table could become saturated within roughly one to three days, while the `TRIED` table filled much more slowly. Participants suggested that spam could leave new nodes relying heavily on seed-derived addresses.

## More frequent reachability checks

Increasing feeler frequency was proposed as a way to gather more information about addresses and populate `TRIED` with reachable peers. An interval of 30 seconds was suggested, with no obvious downside identified in that exchange, though it was not adopted as a decision.

A lighter-weight probe was also discussed: for a small fraction of addresses, attempt a quick ping or reachability check before admitting them to `NEW`, rather than completing a full handshake.

The concern was whether widely relaying a new address could cause many nodes to probe it simultaneously, creating a denial-of-service risk.

More frequent feelers were not thought to require a larger `TRIED` table. Its approximately 16,000-entry capacity was considered likely sufficient.

## Outbound connection rotation

Another proposal was to extend reachability testing into actual outbound connection rotation.

A node would continue making new outbound connections and, after a candidate passed some threshold, consider replacing an existing connection. This could provide more connection turnover while making candidate connections useful beyond a brief feeler test.

The suggested approach borrowed from inbound eviction:

- Protect selected connections, such as the oldest connection or one that recently delivered a block first.
- Apply an age-weighted selection among the remaining connections.
- Usually replace a recent connection, while occasionally replacing another.

Participants noted that multiple protection criteria are harder to game collectively, even if individual criteria can be manipulated. The proposal remained exploratory; the notes do not establish a selection algorithm or a completed security analysis.

## Prioritizing tested addresses in `getaddr`

A separate proposal concerned `getaddr` responses rather than gossip relay.

A responding node could reserve a position in its response for an address from `TRIED`. The recipient could then perform a feeler check, potentially allowing the address to reach its own `TRIED` table without first competing for ordinary admission to `NEW`.

A temporary holding area was suggested so the candidate would not need to occupy a `NEW` slot before being checked.

This could make useful addresses easier to acquire, but participants explicitly identified an eclipse risk: preferential treatment could amplify the influence of an attacker supplying addresses. Successful reachability checks would not by themselves resolve that concern.

## Address-manager eviction and open questions

The discussion returned to whether `addrman` needs an explicit turnover policy rather than relying entirely on `IsTerrible`.

Possibilities included randomizing replacement decisions or allowing new addresses to replace some fraction of existing entries. Figures such as 10% and 25% were floated as questions, not recommendations.

Participants cautioned that `IsTerrible` is used for purposes beyond eviction. A policy intended to improve address-manager turnover may therefore need to be separate from the existing classification.

No single remedy was chosen. The main unresolved questions were how to admit genuinely new addresses despite timestamp-refreshing spam, how much turnover is desirable, and how to improve inbound connectivity without weakening eclipse resistance or creating excessive probing traffic.