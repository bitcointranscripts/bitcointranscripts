---
title: Shielded CSV Deep Dive
date: 2024-11-21
---

CSV is a way to build a new Layer 1 blockchain

- L1 is defined as a transaction protocol, separate from defining consensus/ordering

L1 - Bitcoin Tx Verification / CSV

L0.5 - Blockchain PoW

## Recipe

1.  Sender prepares a tx

2.  Sender derives a nullifier from the tx. Used to nullify the tx inputs that have been spent in the tx.

3.  Put nullifier onchain to prevent double-spending. The nullifier is short (64 B) regardless of how big the tx is. The nullifier reveals nothing about the tx.

4.  Receiver processes the blockchain by scanning the blockchain for CSV nullifiers and builds a database of nullifiers it has seen.

5.  Send the rest of the tx data to the receiver, and the receiver will connect the data received to the nullifier to consider the transaction \"confirmed\"

    a. Coin

    b. Coin proof

## Background

- Colored coins were clients that could \"color\" UTXOs and interpret them to represent some other asset

- Embedded consensus protocols such as Omni (nee Mastercoin), Counterparty, Blockstack, etc, interpreted data that was embedded in the `OP_RETURN` field.

- CSV protocols only put a commitment onchain and pass the rest of the data offchain.

  - Taproot Assets and RGB both need to pass the coin and full coin history to recipients, so that recipients can verify that the coin is valid

  - zkCoins and Shielded CSV both only pass the coin and a proof of valid history to recipients. Nullifiers can be batched by a "publisher" and duplicates can be filtered out by clients.

Quotes from participants:

- "one of the most compelling applications of PCD"
- "... and one of the most compelling applications of zk in bitcoin overall"

## Table of Shielded CSV features

| Positives                                                                                    | Addressable Challenges                                         | Inherent Challenges                                                                                                                          |
| -------------------------------------------------------------------------------------------- | -------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| 64 byte nullifiers (100 tx/s)                                                                | Needs a bridge                                                 | Forever growing nullifier set (maybe addressable? see zkCoins epoch design)                                                                  |
| Privacy (hide tx details from the public, and sender identity + coin history from recipient) | (Anonymous) communication channel between sender and recipient | Losing wallet state -> coins are burned                                                                                                      |
| Cheap bitcoin block validation                                                               | Proving costs                                                  | MEV: incentive to be a publisher to be the first to claim publishing fees (maybe addressable by defining a canonical publisher for time _t_) |
| No UTXO set bloat                                                                            | Communication channels with publishers i.e. "mempool"          | Re-orgs are complex to deal with                                                                                                             |
| No sequencing                                                                                | LN compatibility                                               |                                                                                                                                              |
| No soft fork necessary                                                                       |                                                                |                                                                                                                                              |
| Private reusable addresses                                                                   |                                                                |                                                                                                                                              |
