---
title: Private Broadcast After Merge
tags:
  - bitcoin-core
  - p2p
  - privacy
date: 2026-05-06
---

## Adding to wallet

- Wallet adds txs naively, we need to support adding txs in order but
  not in mempool
- Allow recipient adding parent
- No privacy fingerprint if we give parent or any ancestors, but no
  siblings
- getdata must be for the inv we sent
- we have GetAncestors API to whitelist all getdata for all inputs
- we need a txgraph of the private broadcast queue
- Up from the tx we broadcast, pick from mempool all ancestors to add to
  private broadcast as well, then start with child and parent

## Package relay

- 1p1c
- we get for free with above

## Persistence

- can't remove based on mempool checks for the above
- write to a file every add of a new tx
- on startup, read the file and add txs to private broadcast
- debatable if we need it

## Decoys

- every hour or so pick one of your last txs and private broadcast them
