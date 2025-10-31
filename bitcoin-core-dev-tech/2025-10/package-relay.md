---
title: Package Relay
tags:
  - bitcoin-core
  - package-relay
date: 2025-10-22
---

Tracking issue: we have come very far

Idea was that after cluster mempool, you would be able to do arbitrary packages

There are branches to do arbitrary package validation, but imperfect

arbitrary package RBF is maybe still impossible: linearization and chunking
doesn’t take conflicts into account, there isn’t a simple way to discount
conflicts because submitting in different orders can give you different results.
Easy to come up with an example that would go wrong. Even if we could freeze
time and try all possibilities, we can’t generally define what “better” means.

For example, if submitting these transactions in order individually/in pairs
would have worked, arbitrary package validation can’t reject them

Maybe we should again focus on just enabling the use cases we care about, since
arbitrary is impossible.

We have 1p1c, we can propagate them reliably, we know how to resolve conflicts
in that context.

About as robust as possible for this topology.

In BIP 331 it was proposed to get rid of txid-based transaction relay. In all
cases we use wtxid, except when we are missing a parent and only have the txid
to go on.

Is this compatible with Libbitcoin? They don’t have a mempool

Here are the 3 things we can still do

1: BIP 331 to get rid of TXID Relay:

* Bandwidth savings, because wtxids are unambiguous, txid could have various
  witnesses and we always re-request over and over again until we’ve asked
  everybody (even if they all have the same witness)
* Potentially some DOS concerns because txids can be retried
* It would be nice to get rid off txid relay, but not high priority
* BIP 331 allows to request ancestor information and request all of the relevant
  transactions from any peer
* BIP 331 also prescribes messages for requesting/giving ancestor package
  information
* In case of multiple generations, it would save a number of roundtrips to
  request ancestor information instead of getting parents from orphans,
  similarly for multiple missing parents
* For 1p1c, BIP 331 is more round trips and more bandwidth. But means no txid
  relay
* 4 out of 10 useful, but 10/10 complexity to implement as mentioned above
* Currently package rbf can only handle packages of two packages, longer chains
  that conflict at grandparent or more ancestral will not be resolved properly
* Currently, groups of transactions cannot be submitted together, we are limited
  to 1p1c, there is preliminary work to try this
  * Does something make the mempool better
  * can replacements pay for themselves
  * resource limits may be order sensitive
  * Package cannot be acceptable if the individual parts processed independently
    would be rejected

2: Sender initiated package relay

* 2 out of 10 implementation complexity, 6 out of 10 useful, depending on usage
* Where 1p1c is reactive, child goes in orphanage, parent is requested,…
* Sender should be able to recognize that the zero-fee parent will never be
  around before the child is requested, so the sender should instead use
  `pkgtxns` to announce both at once
* Potential downside is that it wastes bandwidth even more
* Replacement cycling a concern? If it based on “do you already have this,” we
  won’t send again, but we just fall back to receiver asking again

3: Supporting more different topologies next to 1p1c?

* Splice into a unilateral close?
* Closing after zeroconf
* Ark branch to VTXO, zero-fee ancestor chain?
* Longer chains than 1p1c?
* More topologies can perhaps be supported even without package relay protocol
  (e.g. combine orphanage and vextrapool, smarter orphanage logic)
