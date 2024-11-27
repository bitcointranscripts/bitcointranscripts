---
title: AssumeUTXO update
tags:
  - bitcoin-core
  - assumeutxo
date: 2023-04-27
aliases:
  - /bitcoin-core-dev-tech/2023-04-27-assumeutxo/
speakers:
  - James O'Beirne
---
## Goals

- allow nodes to get a utxo set quickly (1h)
- at the same time, no major security concessions

## Approach

- Provide serialized utxo snapshot
- get headers chain first, load snapshot and deserialize, sync to tip from that
- then start background verification with a 2nd snapshot
- finally, compare hashes when background IBD hits snapshot base

## Progress update

- lots of refactoring has been done; `ChainStateManager `was introduced, globals removed, mempool / blockstorage refactored
- init / shutdown logic changes have been merged
- wallet changes done
- p2p changes still under review (i.e. picking the chainstate to which to append new blocks )

## Open issues

`nFile` order gets fragmented, potential problems with pruning and/or reindex
-> Introduce blockfile nFile counter per chainstate types (simple change)

## Pruning

- currently, pruning target w/ trailing window
- do the same, but with two tips - different possiblities to achieve this

## Indexing

`validationinterface` signals are picked up by indices

- could build out of order, but some indexes (coinstats) cant be build out of order
- simple solution: just disable all indexes until sync completes
- fancy solution: disable some indexers only

- Introduce rpc to load chainstate
- Put actual assumeutxo hashes into chainparams
- In total, only ~1k loc left, although mostly in important places

## Approach re-ack discussion

- Do we really need background sync?
- not doing the background sync is simpler, but changes security assumptions
- Also, it would remove the necessity that every node must be able to sync the chain
