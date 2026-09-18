---
title: The Ethereum Perspective on Post-Quantum Cryptography
transcript_by: Localhost Research
date: 2026-08-28
weight: 2
tags:
  - quantum
  - ethereum
  - cryptography
speakers:
  - Antonio Sanso
additional_resources:
  - title: Slides
    url: https://btctranscripts.com/bitcoin-transcript/quantum-workshop/2026-08/ethereum-perspective-on-pq-cryptography-slides.pdf
---

_For slides, please see the 'Extra Info' tab_

### Ethereum's Three Layers — All Depend on Elliptic Curves

| Layer | Current cryptography |
|---|---|
| Execution | secp256k1 |
| Consensus | BLS12-381 |
| Data availability sampling | BLS12-381 |

(The DA layer is more explicit in Ethereum than in Bitcoin. Each layer has many client implementations, all sharing the underlying EC assumptions.)

### The Roadmap (with a governance caveat)

- **Caveat:** this "strawman" reflects the Ethereum Foundation's vision, not a guarantee — Ethereum governance is complicated, and this is an attempt to *guide* the community.
- Currently shipping **Glamsterdam**; introducing **frame transactions**.
- **LeanVM:** where STARK-based aggregation of signatures for all three layers will live. Plan is to ship **leanSPHINCS**.
- Direction: **account abstraction + no precompiles + aligned architecture across consensus/DA**.
- **Going all-in on hash-based signatures. No lattices.** Rationale (from Q&A below): minimal assumptions, alignment across all three layers.

### Hash Function Choice: Dropping Poseidon

- For years Ethereum pushed **Poseidon** (Sanso personally was not a fan).
- A recent paper, **Flock**, means Poseidon is no longer needed: **hundreds of thousands of signatures can be proven in zk quickly** with standard hashes.
- Poseidon isn't considered *broken* — it's just no longer worth the risk.

### Stateful for Consensus, Stateless for Transactions

- **Consensus layer: stateful signatures.** Interesting fit, because signing many blocks already gets you slashed — the protocol punishes state reuse anyway.
- **Transaction layer: stateless — a SPHINCS+ variant.**
  - SPHINCS+ has many tunable parameters trading off signature size, hash counts for signing/verification, and key lifetime.
  - SPHINCS+ isn't *truly* stateless — the signature budget is just so large (2⁶⁴) that it behaves statelessly. That budget was recognized as bigger than needed: **most ETH addresses have sent fewer than 3,000 transactions.**
  - But shrinking budgets can push signing cost too high (e.g., 1.45B hashes in one example).

### SPHINCS-G and Hardware Wallet Signing

- Baseline SPHINCS on a Ledger Nano S Plus: **47.5s to sign** — not ideal but better than before.
- **SPHINCS-G** (recent): 2²⁴ signature budget, **32-byte public keys**.
- Key insight: **parts of SPHINCS are public and can be computed outside the hardware wallet's secure element** — only the Winternitz chains touching secrets must stay inside.
  - Requires lots of host↔device interaction; precomputation happens offline ahead of signing, plus grinding at signing time.
  - This changes the SPHINCS security proof, which will need to be adapted (they're precomputing different parts of the XMSS/hypertree — conceptually similar to hypertree pruning).

**Path forward:**
- Formalize and analyze the SPHINCS-G construction properly
- Experiment with non-standard, more aggressive SPHINCS variants (non-conventional **WOTS+C / FORS+C**)
- Formally verify the signature contracts

### Q&A

**Q: Would this be an online/offline signature — always requiring preprocessing, or one-time?**
- There are many different scenarios under consideration.

**Q: If the host selects the randomizer, can't it bias the result?**
- Yes — they're aware of this and adapting the design to account for it.

**Q: Why hash-based given the tradeoff space?**
- The required assumptions are minimal, plus alignment across all three layers. And there's growing research on thresholdization/MPC for hash-based schemes, so the picture there isn't as dark as feared.

**Q: Where are signatures verified?**
- At the **account abstraction level**, with an **aggregator at the mempool level** calling the STARK precompile. Without a precompile it's not too expensive since cost is amortized via aggregation. (For comparison: ML-DSA without a precompile would cost 8–10M gas — though people have implemented MPC on Dilithium, and that may be acceptable if you really care about a given transaction.)

**Q: Exact parameter choices? SPHINCS+C optimizations?**
- Parameters not yet picked — and they matter less as long as aggregation and outsourced signing exist. **Amortization plays the biggest role.** Announcement coming soon.

**Other notes:** a new actor will be responsible for aggregation, aggregating every few milliseconds; there was discussion of enshrining the aggregation scheme.
