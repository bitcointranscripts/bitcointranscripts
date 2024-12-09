---
title: List of Upgrades and Feasibility
date: 2024-11-20
---

- **Is Activation part of this discussion?**  
  Yes, activation is part of feasibility.

- **List upgrades on Sticky Notes**

  - **Categories**
    - Consensus cleanup
    - Total script replacement/alternative
    - Covenant proposals (discussion of what `lnhance` is)
    - Various amounts of script restoration
    - UTXO commitments stuff (block commitments (maybe lagging - `muhash`))
    - Streaming hash
    - Cross-input signature aggregation
    - `OP_ZKP`
    - Quantum resistance

- **UTXOs**  
  Two options: support inclusion proofs or just verify the UTXO set.

  - Is UTXO commitment worth it without inclusion proofs?
  - Can you build a succinct inclusion proof into the committed UTXO set?
  - Alternative node implementations dislike UTXOs and would push back against them.
  - Technically, UTXO is Core-specific, e.g., choice of unspendable coins.

- **What is Quantum-resistant Taproot?**

- **Cross-input signature aggregation** has little benefit due to only small transaction weight improvement (?).

## Organize by impact vs feasibility

![Diagram of features organized by impact vs feasibility](https://raw.githubusercontent.com/bitcointranscripts/media/refs/heads/main/bitcoin-research-week-2024/list-of-upgrades-and-feasibility/impact-vs-feasibility.jpg)

- **Observations:**
  - `OP_CAT` has relatively high impact/feasibility.
  - Maybe `OP_ANYPREVOUT`.
  - Consensus cleanup has low impact and high feasibility but could have high impact if a timewarp attack actually occurs.
