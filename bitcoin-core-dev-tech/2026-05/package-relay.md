---
title: The Future of Package Relay in Bitcoin
tags:
  - bitcoin-core
  - p2p
  - mempool
date: 2026-05-05
---

*Notes from an in-person discussion on the current state of package
relay, its limitations, and possible directions forward.*

## Framing

What's already in the codebase? Some contributors are riding off into
the sunset, so the question is: where's the appetite for doing more?

## Current State: 1p1c Opportunistic Relay

Today we have **1-parent-1-child (1p1c) opportunistic relay**. The
mechanism works roughly as follows:

- We use the **orphanage** to hold on to child transactions until we
  hear about the parent, then connect the two.
- We deduplicate by memory and DoS count.
- We restrict the number of orphans we've heard about. Once we exceed
  that limit, we have to prune.

### The "Package Relay Jam" Problem

One failure mode that can happen today: if there's too much orphan
traffic, we start losing transactions. This is what we'd call a
**package relay jam**.

The root cause is that `inv` messages don't carry explicit feerate
claims, so the receiver has no way to judge the "juiciness" of a
transaction. An attacker can exploit this by using low-feerate
transactions to induce orphanage activity cheaply — with feerates well
below what would make it into the next block.

### How much do current DoS prevention mechanisms help?

- The current limit is **3,000 announcements across all peers**.
- Memory is allocated per active peer: each peer gets a bucket of
  **101 kvB**.

It can still be attacked. Orphans are trimmed on a **per-peer basis**
once they reach the limit, even if it was another peer that pushed the
orphanage to its total limit.

## Structural Limits

There's an inherent structural limit to how we can resolve these jams.
For example, a Lightning channel peer can manipulate this behavior. The
period during which you request and resolve a parent can stretch to ~2
minutes in some cases over the lifetime of a given orphan entry.

## Possible Directions

### Sender-Initiated / Orphanage List

One idea floated: what if we could give peers more information up front
— anticipate their needs?

In today's scheme, when the parent is 0-fee and the child is the fee
bringer, we **don't advertise the parent** at all. It just gets put in
an inventory queue.

We could imagine an alternative where we provide **topological
information** — something along the lines of BIP 331: "I like these two
together." The receiver would then need to be updated to understand the
new message and request both at the same time.

Another variant: a new message where the requesting peer issues a
`getdata` for the child, and the sending peer — knowing the requester
doesn't have the package — sends both.

The tradeoff is: **how do you predict when to send the parent?**

> Closed PR: a rolling bloom filter per peer to track what you have and
> haven't sent.

### Does the inv approach work with Erlay?

It should.

## Test Utilities: `testmempoolaccept` vs. `testsubmitpackage`

We don't really have a `testonlysubmitpackage`. We have
`testmempoolaccept`, which takes an array of transactions and tells you,
more or less one-by-one, what would happen when you try to enter them
into the mempool. It was designed pre-package-relay, and it currently
uses the package-unaware path.

We need utilities to analyze whether a package would be considered
legitimate. Even with ephemeral dust, you can't do that today.

The thought is: first, keep it constrained to 1p1c. Figure out what's
acceptable to the RPC, and keep the RPC and relay behavior consistent.

## How Far Does 1p1c Get Us?

1p1c alone probably gets us ~90% of what we want. To get the rest,
you'd want to handle:

- A string of transactions, or
- **Batch CPFP** (n parents, 1 child).

This would be helpful for **Ark**-style constructions. But doing it
would be a lot of work — it needs generalized eviction.

## Pragmatic Focus

Without more contributors, it's better to focus on what we can
realistically do. One concrete use case: **private transaction relay**.
Today, if you get a conflicting transaction in your mempool, you can use
`testmempoolaccept`, see that it's conflicted, and stop trying to
resubmit. We need the same thing for package relay.

During cluster mempool, there's a two-layer `txgraph` that captures all
relationships. For a proper `submitpackage`, you'd need a **three-layer
`txgraph`**.

### Short List

- Do we want to stop relying on orphanage relay? And if so, how?
- A `testonlysubmitpackage` would be nice to have.
- Revisit less strict topologies. How do we get and process the
  messages? A lot of the constraints may have shifted now that we have
  cluster mempool.

### On Receiver-Initiated Relay

Receiver-initiated relay (the path that goes through the orphanage — no
good name yet, maybe `package inv` vs. `package tx`) seems to carry
more complexity. It's hard to reason about the **cycling problem**:

> What if the receiver has the parent but not the child, only asks for
> the child, and the parent gets cycled out in the meantime?

## Looking Ahead

In the short term, generalized package relay is unlikely to land. We're
not even sure **BIP 331** is the right design anymore. Now that we have
cluster mempool, we could have multiple CPFPs — and maybe not only
ancestors, but also **siblings and uncles**. A "cluster prefix relay"
of some kind? It's not clear yet what that looks like.
