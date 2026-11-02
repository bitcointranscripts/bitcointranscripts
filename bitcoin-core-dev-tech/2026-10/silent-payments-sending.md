---
title: Silent Payment Sending
tags:
  - bitcoin-core
date: 2026-10-13
---

## Scope and status

The session covered ongoing work to merge silent payment sending support: constructing a transaction that pays a silent payment address. A list of related pull requests was referenced, but the notes do not include their identifiers.

The discussion focused on the interactions with fee bumping, wallet persistence, coin selection, and compatibility when downgrading to an older version.

## RBF and the information the wallet must retain

Supporting replace-by-fee (RBF) requires persisting additional information, including the recipient’s static payment code. Constructing the initial transaction is therefore only part of the implementation: the wallet must retain the information needed to construct a replacement.

One alternative was to sign multiple versions of the transaction at different feerates in advance. This was raised alongside concerns about the overhead of storing additional wallet data, but the notes do not record a preferred approach.

## Downgrade compatibility

A central concern was that, after downgrading, an older node would not have the support needed to fee-bump a silent payment transaction correctly.

Several approaches were discussed:

| Approach | Consideration raised |
|---|---|
| Make the transaction appear already replaced | Described as the current solution for preventing fee bumping after a downgrade, but with unresolved pitfalls. |
| Set a wallet flag unknown to older software | Another compatibility guard, also considered problematic. |
| Introduce a per-transaction flag | Considered desirable as a more targeted alternative to a wallet-wide flag. |
| Use child-pays-for-parent (CPFP) | Raised as another fee-bumping option. |

Participants wanted a supported path back to older versions, potentially through a backport. The notes do not specify what that backport would contain or settle on a compatibility mechanism.

## Coin selection

Silent payment sending requires at least one silent-payment-eligible input. Coin selection must account for that requirement rather than selecting solely on the usual criteria.

Existing eligibility filters, including height and amount constraints, were mentioned as relevant infrastructure. The notes do not establish how the additional requirement would be incorporated.

## RPC workflows and persistence

Some existing transaction-construction workflows do not persist the resulting transaction in the wallet. That creates a compatibility problem for the proposed sending support, which depends on retaining additional information.

Two cases were identified:

- Using `send` without adding the transaction to the wallet.
- Using a silent payment address as the change address in `fundrawtransaction`, where the necessary information would not be persisted through that workflow.

## Outstanding work

The remaining questions were how to retain the information needed for RBF, prevent unsupported fee bumping after a downgrade, incorporate input eligibility into coin selection, and handle RPC workflows that do not save transactions to the wallet.

The notes do not record final decisions on these issues.