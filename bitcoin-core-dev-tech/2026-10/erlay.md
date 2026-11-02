---
title: Erlay
tags:
  - bitcoin-core
date: 2026-10-14
---

## Scope of the discussion

I want to recap what we discussed in Barcelona, cover the state of the pull request, and raise some questions that came up during the reimplementation.

In Barcelona, we discussed changing the approach. Rather than using Erlay primarily to minimize bandwidth, the idea is to use it more as a fallback for eclipse protection.

We have focused on hybrid connections for a few years, trying to make the trade-offs worth the complexity. Instead, why not maintain the existing number of connections and add some fallback reconciliation peers?

These would be the transaction equivalent of block-relay-only connections: additional connections that, under normal operation, use virtually no bandwidth. They become useful if you start getting eclipsed.

## Reconciliation intervals and bandwidth

What is the logic for those connections kicking in?

The reconciliation period is longer than it used to be. The idea now is to reconcile every 30–60 seconds rather than every 8 seconds.

By the time you reconcile, the differences between your sets should be almost empty. The overhead is mostly just initiating reconciliation. Under an eclipse attack, there would be some additional bandwidth cost.

The whole point is to increase connectivity without paying a linear bandwidth cost.

There is also a question about whether these connections should relay blocks.

## Connection establishment and capability signaling

Let’s start with connection establishment and work down to performance.

According to BIP 330, we signal reconciliation support during connection establishment. That was sufficient for hybrid connections.

Now, however, these are a different connection type. There is no normal transaction fanout: we are supposed to use them for reconciliation.

We do not advertise this distinction in advance, so we do not know whether a peer supports it until we establish the connection.

In the current implementation, if you proactively tell your peer that you want to use reconciliation, the connection is treated as a reconciliation connection, and both sides know that. But if the peer does not have a slot available, you try other peers. That could create a lot of churn.

I started by establishing normal connections first and reconciliation connections afterward, but the approach is not settled. What should take priority? Should we start with one type and fall back to the other?

Why not use a service flag?

We could. Should we amend the BIP?

But service bits can be lied about. Even if I advertise support, you do not know whether I have any slots left.

If you have to attempt the connection anyway, perhaps it would be better to say that support is available from a particular version onward.

Could we use “434 negotiation”? That would add negotiation steps. [The reference to “434” is unclear in the source notes.]

## Deployment and connection churn

Deployment creates a problem, especially while most peers do not support this. If peers upgrade slowly, many nodes could repeatedly try to establish reconciliation connections with peers that do not support them, effectively hammering those peers.

Could we use feeler connections?

That has the same problem.

We currently set the bit but do not do anything with it.

One solution would be a two-phase deployment. First, release the announcement part, so peers advertise support but nobody attempts to establish these connections. Once there is enough coverage, release the actual connection support.

Could we start with more slots and reduce the number later? The current number is a magic number.

## Relationship to full-relay connections

These connections are being treated as full outbound connections, and they should be: they relay addresses, blocks, and transactions.

That means we account for them in eviction, diversify them, and apply the other logic used for full outbound connections.

To me, they are the same as full outbound connections, just with a different transaction relay mechanism. Having them side by side makes sense.

## Sketch capacity and computational cost

At the last CoreDev meeting, we discussed performance and how expensive this would be. That may be a problem with the current implementation.

We currently create sets with roughly 2,000–3,000 elements, so there can be up to 6,000 differences between two sets.

Although we do not create them ourselves, we accept sketches with much larger capacities, up to 8,000.

I thought that limit came from BIP 330, but I checked, and BIP 330 does not specify a maximum capacity.

Unfortunately, sketch decoding takes quadratic time with respect to capacity. If sketches are too large, they can tie up the message handler. At the upper end of what we accept—around 8,000—we can run into problems.

You would not expect this in normal operation, but it matters in an adversarial case.

That seems like an excessive upper limit. In general, this scales poorly.

Could decoding run on a background thread?

Yes. Perhaps we should move it to a background thread. That is not how it works now, but it probably should be.

## Removing sketch extensions

Extensions make this worse. If reconciliation fails, an extension allows the capacity to double.

We want to remove extensions. They make the state machine too complex and are a leftover from the original design priorities.

The rest of the code is heavily tested and benchmarked. I have not worked as much on extensions. Unless someone objects, I would like to remove them.

If the differences become too large, reconciliation can fail and trigger an extension.

## What happens when reconciliation fails?

The old fallback was fanout. If reconciliation failed, we would fall back to announcing transactions through fanout. I do not know whether that is still the best approach.

Previously, those connections were intended to be hybrid: try one mechanism, then fall back to another.

What happens with the new approach? These connections are supposed to provide a fallback without adding much load. Imagine connecting to a group of malicious peers that always make reconciliation fail. You would then treat them as fanout peers.

That could effectively double the number of fanout peers. A peer could cause this simply by never reconciling, allowing the set to fill up.

I am leaning toward not falling back to fanout for these connections.

The problem with having no fallback is that, if all your initial connections fail and none of the reconciliation connections successfully reconcile, you have no way to get transactions out. You are eclipsed. Would falling back to fanout help in that situation?

Even if you are fully eclipsed, a set growing to 3,000 transactions suggests something is wrong.

If we disconnect rather than fall back to fanout, someone might be able to create enough churn to cause reconciliation disconnections. That might only work as a direct attack.

If we do not disconnect, the worst case is the same as fanout: a malicious peer refuses to participate in reconciliation and forces you to promote the connection to normal transaction relay.

We should not change the existing block-relay-only logic, because that has other uses. But reconciliation connections could behave like block-relay-only connections in some circumstances.

The concern with eviction has always been avoiding churn. Even when a peer performs poorly, it can be difficult to determine why.

## Benefits and costs

Why is this better than a block-relay-only connection?

The idea is that you would receive more transactions. It addresses a different threat model. If you do not care about unconfirmed transactions, you do not care about this.

What are the benefits and costs?

| Area | Point raised in the discussion |
|---|---|
| Transaction connectivity | Additional peers provide another path for transaction relay. |
| Computation | Nodes must construct sketches and perform reconciliation. |
| Complexity | Reconciliation introduces a new state machine. |
| Connection slots | Additional connections require slots. The slots added in the latest release were described as reserved for non-transaction-relay peers and therefore unavailable for Erlay peers. |
| Relay speed | Speeding up transaction relay was previously a goal, but that has been dropped. |
| Bandwidth | The intended normal-case cost is a small, roughly constant overhead. |

In the normal case, reconciliation should amount to a message initiating the exchange and an empty difference or sketch.

## Could we reduce the number of fanout peers?

Could we eventually reduce the number of fanout peers?

Possibly. We are currently overprovisioning fanout.

But what happens if we start limiting those slots? Would transaction propagation times increase?

That brings us back to the same balance we had with the hybrid design.

## Should reconciliation connections be more specialized?

Have you considered a more specialized connection type that only performs transaction reconciliation, without relaying blocks or other data?

It could work that way.

The decision has followed the underlying connection-handling model: pings, blocks, and addresses are exchanged.

But block relay is basically free. Why not include it?

You could also just add more block-relay-only connections.

If narrowing the connection type does not save much complexity, there is little reason to do it.

## Tracking announcements against reconciliation

Reconciliation first tells us what we are missing. We then send the `inv` messages and the transactions.

An `inv` should correspond to a sketch exchange. If you receive an `inv` that is not associated with a sketch, you could track that.

As a separate point, we should not accept transactions that were not previously announced with an `inv`. Accepting those is legacy behavior.