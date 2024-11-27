---
title: Package Relay Planning
tags:
  - bitcoin-core
  - package-relay
date: 2023-09-20
speakers:
  - Gloria Zhao
---
## Package Relay Planning

What can we do better, keep doing?

This is all the work that needs to be done for package relay -> big chart

![package relay PRs](/bitcoin-core-dev-tech/2023-09/package-relay-todos.png)

Left part is mempool validation stuff. It’s how we decide if we put transactions in the mempool after receiving them “somehow”.

Right is peer to peer stuff

Current master is accepting parents-and-child packages(every tx but last must be a parent of child), one by one, then all at the same time.

It's a simplification, but also economically wrong. Missing general ancestor packages. Required topo sorting. Allows “parent pays for child” weirdness.

What does [#26711](https://github.com/bitcoin/bitcoin/pull/26711) do? Sipa's recap:

1) topo sort
2) linearization step, Ancestor set scoring
3) one by one evaluate subpackages in linearized order
4) is this package acceptable to mempool from fee perspective?
5) if so, accept try submitting, if not, keep going
6) If accepted, ends up in mempool
7) if failure(should be non-fee related), drop the rest of the package

Rationale: No quadratic validation, easier to reason about, captures most of the economic value in CPFP situations.

We don’t want to cause additional relay failure due to inconsistency

Don't trust just "total package feerate", parent-pays-for-child. Hard to prove who is being pathological though, no way to punish. Just drop those last transactions in that case.

Get submitpackage to MVP, on mainnet? Get it out for experimentation.

## P2P

Modularize orphan handling to make more robust,
only behavior change is we can try resolution
with multiple peers. Required change for package relay.
Attacker announces packages first, withholds.

Second part introduces some p2p messages
including negotiation, ancestor package messages.
Get all unconfirmed transactions by WTXID.

Third introduces rest. Adds getpkgtxns,  pktxns, use
ProcessNewPackage. Exposes package relay in proper,
allows package CPFP.

Orphanage token system. Don't want honest users knocked
out of mempool.

Laid out her plan of attack, what can be done to make
review more open or appealing?

"Does it make sense to have both of these branches in parallel?" meaning
Does it make sense to focus on one side or another?

Focus on package evaluation, get that in, then rebase p2p on that?

Could put all other PRs in draft, currently only top
p2p one is not in draft.

Ask people if targeting 27.0 for submitpackage mainnet?

Find the people who have the depth of understanding on the systems
you are trying to design. Would a design document help? Did it help
previous projects? Could just be it's hard to rally review for other
reasons.

Based on our current understanding, the package evaluation
PRs look to be approach ACK'd. Right hand p2p side less so. There
are scattered docs, combine and present to key stakeholders.

Start review on left, document right.
