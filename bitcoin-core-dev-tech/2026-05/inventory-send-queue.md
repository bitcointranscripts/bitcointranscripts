---
title: Inventory Send Queue Rework
tags:
  - bitcoin-core
  - p2p
  - mempool
date: 2026-05-06
---

## Motivation

We relay tx to our peers (up to 120ish)

We keep a queue of txs to announce (invs_to_send). This is per peer. This allows
to deduplicate (2s for outs 5s to invs).

We don't have a way to rate limit txs being received (we do for outgoing). atm
we add all txs to all peers. When we process them we aim to send 75 to 100 txs
per peer to rate limit the output. The issue is that since the inbound is not
rate limited, the queues can grow rather large (and this been per peer makes it
even worse).

This queue needs to be sorted by feerate to decide what transactions to be sent
first to your peers. This is not a DoS concern as it used to be, but it will
slowdown your node. mem usage grows with 50 x 100ish peers. Increasing the peer
count will make this blow up

## Solution (PR is #34628)

Instead of an unbounded queue per peer we may want to have a global queue (this
is the approach of the PR). Under normal conditions we still use the per peer
queue. If traffic grows to big we use the backlog global queue instead of the
per peer queues. We still need to sort that queue but only once, not per peer.
We rate limit via token buckets. We extract from the backlog when both token
buckets have room. The queues can stick grow big, but not as much (e.g. 300 txs
instead of 15000).

How easy is to test the refactoring of the logic? You can test the backlog
behavior by setting the bandwidth bellow 7txps

What are the downsides? Its more complicated (more data structures). There is no
de-duplication in the backlog.

What frequency do you run thus draining of the global queue to the local queues?
It runs it when the size bucket is not empty and when the per tx bucket has
enough to send a full inv

How long it takes for a tx to get into your mempool until it gets sent out to
your peer. With no backlog, same as now. With the backlog, if its at the top of
the mempool, an extra 50% of time on top of the current logic (5s inbounds/2s
outbounds). If its in the bottom of the mempool, it needs to wait until the
backlog is cleared, so it depends

## Sentiment

SHIP IT
