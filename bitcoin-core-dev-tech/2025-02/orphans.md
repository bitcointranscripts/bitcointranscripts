---
title: Orphan Handling + TxOrphanage
tags:
  - bitcoin-core
date: 2025-02-27
---

Discussion on [p2p: improve TxOrphanage denial of service bounds and increase
-maxorphantxs](https://github.com/bitcoin/bitcoin/pull/31829)

TxOrphanage has 2 goals:

1. limit resource usage (DoS) resistance, both in terms of memory and
   computation
2. try to guarantee usage / not to be easily censorable

Today, we perform well on 1) and poorly on 2). The current TxOrphanage efforts
aim to improve 2) while keeping 1).

## Terminology

- `count limit`: number of orphans
- `announcement limit`: # of unique {orphan, peer} pairs
- `memory limit`: total weight of orphans -> deduplicated if an orphan is
  announced by multiple peers
- `per-peer DoS score`: max(CPU Score, Mem Score) - `CPU Score` = (#
	announcements by peer) / (# allowed per peer) - `Mem Score` =
	(non-deduplicated memory usage) / (allowed memory usage)

Trimming logic: while orphanage exceeds limits, 1) pick DoSiest peer, then 2)
delete ~~random~~oldest* _announcement_ by peer. (The orphan only gets deleted
when it is no longer announced by any peer). This also means that orphans
announced by many peers are less likely to be evicted, which is great, because
it's probably one we're more likely to want to keep.

\*: we used to pick randomly, but actually, since a peer can now only churn its
own orphan announcements, we can simplify this and just pick the oldest one, is
faster.

Question:
> Can we punish peers for sending dishonest announcements?

No, we can't check if they're honest/dishonest. But with this new trimming
logic, peers can only churn through their own announcements, not those of other
peers.

Question:
> Could we use actual transaction memory usage, instead of using weight as a
> proxy?

Yes, using weight as a proxy was a shortcut to get it implemented faster (in
v29), but this may be reconsidered.

## Limits

**Constant limits** (i.e. independent of number of peers):

- Global announcement limit: 3,000 (i.e. 125 peers x 24). - The number 24 is
	based on the 25 tx ancestor/dependant limit, of which at most 24 can have a
	parent missing. - This can be overridden with `-maxtxorphans` startup option
- Per-peer memory limit = 404kWu, i.e. each peer has at least 1 maximally-sized
  transaction (or 404 TRUC transactions).

**Variable limits** (i.e. depend on number of peers):

- Global memory limit: variable, (# of peers) x `per-peer memory limit`
- Per-peer announcement limit: variable, (`global announcement limit`) / (# of
  peers)

Note:

- maximum memory usage scales linearly with the number of peers, whereas
  announcements are hard capped at 3,000 to preserve computational bounds.
- memory usage is deduplicated for the global limit, but not for the per-peer
  limit. This means that the sum of all per-peer memory usage can exceed the
  global maximum memory limit.

Terminology: per-peer limits aren't really limits in the strict sense, because
peers can exceed their per-peer allowance. The "limits" only apply when the
global limits are reached.

## Pathological case

If all your peers are attackers, and all send you the same transaction, each in
a different order, so you're just under the global limits. Then one honest peer
comes in, sends you an honest, small transaction, pushing you over the limit.
Because the attackers all have the highest DoS scores, their announcements will
be evicted first. Because they all announced the same transactions, and because
they're in different order, it's possible that we have to loop over the entire
announcement set before a transaction is evicted. This is why we need a global
announcement limit.

Question:
> Is this pathological case made worse by evicting the oldest announcement,
> instead of a random one?

Yes, it does make it slightly easier for an attacker to hit the global
announcement limit, but only slightly (10% or so).
