---
title: 'Breakout Session: DropKick'
transcript_by: Localhost Research
date: 2026-08-28
weight: 7
tags:
  - quantum
  - lifeboat
speakers:
  - conduition
---

**Reframing "rescue"**
- Rescue protocols are often conflated with confiscation — **but confiscation is not a requirement**. The key concept is **knowledge asymmetry**.

**The post-Q-Day landscape**
- Today, everyone is on legacy (pre-quantum) addresses. After a PQ output type is deployed, on Q-Day there will be coins that are PQ-safe and coins that are not — **we only worry about the latter**.
- Those users' keys are usually BIP32-derived, sometimes behind hashes. Crucially, **these users know things a quantum computer does not** — but this isn't uniform across the UTXO set:
  - A never-used **P2PKH** address: the owner knows the preimage of their pubkey hash → asymmetry exists (*assuming* they never shared an xpub or the pubkey — a big assumption).
  - A used **P2WPKH** address: the pubkey is exposed → no hash asymmetry. **But** they may have another one — BIP32 **hardened derivation is quantum-secure**, and most wallets never share root-level xpubs, so most BIP32 wallets retain this asymmetry.
- These asymmetries are **not provable on-chain** as-is — but we can introduce encumbrances on those UTXOs that let owners prove them (e.g., *"prove you knew your public key before the quantum computer did"*). That's what rescue protocols do.

**What counts as an asymmetry**

| ✅ Asymmetries | ❌ Not asymmetries |
|---|---|
| Hashed addresses | Encrypted WIFs |
| BIP32 hardened derivation (≥1 hardened step) | FROST keys |
| MuSig key aggregation | FROST signature nonces |
| BIP39 | |
| Knowledge of tapscript / Taproot tweaks | |

- Generalization: think of each asymmetry as a **quantum-hard one-way function**, a statement *f(x) = y*. Abstracting to that generic object lets you plug any of them into a rescue protocol: **proving you knew the witness before the quantum attacker did**.

**Why not just create new asymmetries / migrate today?**
- If people were willing to act, they'd just move to PQ outputs. They may not want to reveal themselves or pay fees.
- If you *are* standardizing ahead of time, why not standardize **pre-registration** (an obvious on-chain action)? Note: pre-registration must be standardized *before* use, or you risk making a commitment you can't redeem. That's out of scope here — this session covers **what we can do after Q-Day**.

**Two flavors of rescue protocol**

**1. ZK protocols**
- Prototypes exist (STARKs over BIP32 hardened derivation):
  - roasbeef: proving time of a few seconds, but very large proofs
  - P11: fast, but also large
- Proofs can be aggregated (complicated across different hash functions). Proof sizes can shrink from ~500 KB to ~50 KB with more proving time.
- Drawback: ZK only works for *certain* knowledge asymmetries; others require posting your witness with the spending transaction.
- Perspective: in a world where rescue protocols are in play, *"we don't care so much about hard forks."*

**2. Commit/reveal protocols**
- Requirements: a **timestamping system** (the blockchain itself) and a hash function.
- Mechanics: hash your witness commitment together with a message, hide it in a particular block → wait → then reveal the witness and message. Anyone (assuming reorgs are impossible past some depth) can verify. Effectively, *f(x)* becomes a public key: anyone who knew *x* could have made the commitment.
- **DropKick** and **Lifeboat** are the two examples.

**Lifeboat vs. DropKick: locating commitments**
- *How does a verifier find the commitment on-chain?*
- **Lifeboat:** uses an **index** — commitments flagged at the end of an OP_RETURN. But nothing proves a flagged entry is a *true* commitment, so **the index can be griefed**.
- **DropKick:** no index — the **signer supplies a proof π** (OpenTimestamps-style) that the commitment was included in a specific block: a Merkle/SPV-style proof revealing the path to the block hash.
  - Upside: verifiers keep no indexes.
  - Downside: π can be ~1 KB — *"not the end of the world."* (But is the index really that bad?)

**Miner censorship & game theory**
- **Lifeboat is not vulnerable** to censorship-based theft: the index lets you show you were the *first* valid commitment.
- **DropKick offers no such protection:** a miner seeing your reveal in the mempool could censor/reorg it and insert their own commitment in the meantime.
- DropKick therefore relies on **game-theoretic arguments**: each reveal must carry a fee proportional to the input value — roughly **fee > (input value) / (blocks you must wait)** — to incentivize miners to include your transaction rather than attack it.
