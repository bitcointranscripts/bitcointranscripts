---
title: IBD, Utreexo, UTXO Commitments
date: 2024-11-21
---

## IBD

### libbitcoin approach to IBD

- General idea: maximize parallelism
  - Transaction table, input table, output table
  - Remove force ordering (caused by UTXO model)
  - Perform checks whenever a matching input/output pair has arrived
- Aggressive on P2P (>100 connections)
- Adding a new block to the tip is slower as a result
- Does not work well in a low-memory environment

### Alternative thoughts

- Pre-assumevalid: could we do the same?
- Is it focusing on the wrong thing?
  - IBD is just a few hours, so it's a fraction of the total uptime of a node
- During IBD, privacy and latency are less critical, so it’s okay to approach things differently.

## Utreexo

- Giant Merkle tree
- Commitments in the binary
- UTXOs get numbered; list of indices that get deleted
- "Headers" contain metadata

### Server-client model

- Increases total network traffic
- Archival nodes provide blocks
- Utreexo archival nodes provide proofs
- Tradeoff: how much of the UTXO set you store yourself vs. how much gets proven to you
  - Plan for what you want to cache:
    - Old UTXOs are less likely to be spent
    - Newest UTXOs are cached
- Can check blocks out of order

### Older ideas

- Don't store UTXOs, just hashes
- With each block, provide UTXOs:
  - Enables more parallelism
  - Blocks can be received in arbitrary order and do signature validation.

## Modularization / libbitcoinkernel

- The kernel currently includes the UTXO set: should the LevelDB part be separated?
- Should we have a safe API, plus a more experimental "Hazmat" API?

### Consensus-relevant code

- Code has varying levels of consensus relevance; it's not binary:

  - **Script interpreter**: Any behavior change is at least a soft fork
  - **RPC code**: No consensus implications
  - **In between**: Database layer, P2P code
    - Shouldn't influence consensus but can if broken

- Therefore, much code outside of core ends up re-implementing consensus-relevant code (even unintentionally).
- Encouraging experimentation:
  - Modularization helps, even if only internally.

## UTXO Commitments

### Placement

- Would be in the block header or coinbase
- Some canonical ordering must be defined:
  - Methods differ in cost, complexity, and supported use cases.

### Ordering by address scriptPubKey

- Could give an exclusion proof to SPV clients:
  - Lying by omission becomes impossible
- Costs:
  - Increases per-block validation costs
  - UTXO set updates become more complex
  - UTXO updates require log(n) operations instead of 1.

### Another use case

- Fetch the UTXO set from anywhere (similar to assumeUTXO):
  - Lower requirements for ordering
  - Downside: More trust in miners
- AssumeUTXO would be more useful combined with a P2P distribution mechanism.
