---
title: State of Post-Quantum Cryptography
transcript_by: Localhost Research
date: 2026-08-28
tags:
  - quantum
  - cryptography
speakers:
  - Dan Boneh
additional_resources:
  - title: Slides
    url: https://btctranscripts.com/bitcoin-transcript/quantum-workshop/2026-08/state-of-post-quantum-cryptography.pdf
---

_For slides, please see the 'Extra Info' tab_

### Setting the Stage: "When is Q-Day?"

- There is a lot of noise in the press ("PoW is going to collapse," etc.). It would be good for Bitcoin to have an answer to that noise.
- On hardware timelines: Boneh used to be more pessimistic; he is now more optimistic — or realistic — about quantum computers arriving in the "coming years," particularly given advances in **neutral atom** approaches.
- If pushed on a date: *"If it doesn't happen by 2040, something has gone wrong and we don't know when it will happen."*
- Fundamentally, though, **"when" is the wrong question**. The right question is: **how do we make sure Bitcoin survives Q-Day whenever it happens?** Answering that restores and preserves trust in Bitcoin *today*, even before a quantum computer exists.

### Which Signature Family?

Options on the table: **lattice-based, hash-based, isogenies, multivariate, and zk-proof-of-preimage**.

- **Boneh's personal preference (were he "king for a day"): lattice-based.**
  - Historically, the *algebraic structure* of signatures has been enormously useful for blockchains: threshold signing, multisignatures, aggregation.
  - Many of those properties translate to lattices. It keeps the research community active and is more feature-rich.
- **But the world seems to be going hash-based** (both Ethereum and Bitcoin are focusing there), and that comes at a cost:
  - Non-hardened key derivation appears impossible.
  - Some features are simply lost.
- zk-proof-of-preimage can technically function as a hash-based signature, but the ecosystem seems to be converging on SLH-DSA and similar schemes.

### Terminology: The Hash-Based Signature Spectrum

| Scheme type | Property |
|---|---|
| **OTS** (one-time signatures) | Secure if at most **one** signature is issued per public key |
| **Stateless FTS** (few-time) | Secure for "a few" signatures per key — an ambiguous upper bound, up to a few thousand. Security degrades as more signatures are issued |
| **Stateful FTS** | Short signatures, but state must be maintained. Reusing state exposes you to forgery |
| **Many-time** (SPHINCS+ / SLH-DSA) | Effectively stateless, huge signature budgets |

- **Stateful schemes are a major footgun** — people will have trouble ensuring state is never reused. If used at all, perhaps deploy as a **hybrid** (stateful + EC).
- **SLH-DSA (SPHINCS+ NIST standard):** supports 2⁶⁴ signatures, but signatures are massive — inappropriate for a blockchain as-is.
  - Reducing the budget to 2²⁴ drops signature size to ~3.8 KB, at the cost of very long signing time (~1B hashes). The benefit: **verification is very fast** (~311 hashes).
  - Many other parameterizations exist (e.g., 2¹⁴ budgets with faster signing; **SHRINCS** is another stateless variant).
- **ML-DSA:** the issue is that public keys must be included, and they are quite large.

### Threshold Hash-Based Signatures

Approaches to thresholdizing hash-based schemes:

- **Multi-signing** — very large signatures
- **SNARK-based aggregation** — requires consensus-level understanding of SNARKs
- **Universal thresholdizer (BGG '18)** — single round, but slow: signing must run inside an FHE system; not practical yet without GPUs
- **Generic MPC**
- **PRWNS** — applies to hash-based signatures; the resulting signature is threshold but *looks like a regular single-sig*. The threshold mechanism is implemented with lattice techniques. Supports large *n* and *t*, updatable, single round — but **only applicable to few-time signatures** for now.

### Research Is Not Done — Expect a Two-Step Migration

- PQ signature research is still ongoing. **ML-DSA is not the endgame** — NIST possibly standardized it too early.
- There is **no theorem ruling out a 100-byte signature** with all the features we want. Building it is the major challenge for the community — such a scheme may well arise, but we can't wait forever.
- Likely migration shape: **two steps, not one**:
  1. E.g., Taproot with **ECDSA + SHRINCS** now
  2. Later, **ECDSA + "DreamPQSig"** when a better scheme arrives (possibly dropping ECDSA before then; assume the dream scheme won't be hash-based)

### A Second Reason for Two Steps: Is SHA-256 Actually PQ-Secure?

*(Boneh: "I don't mean to raise false alarms — but you should be aware.")*

- **Classical collision attacks:** birthday attacks; the rho method (sequential, with parallel variants). All need ~√n evaluations of the hash function.
- **Quantum collision finding:** the **BHT algorithm** runs in cube-root-of-n time — and crucially makes only **cube-root-of-n queries** to the hash function.
- There's no reason a **constant-space quantum collision finder** couldn't exist. In theory: ~2⁸⁶ time to find a SHA-256 collision.
- Options: move to **SHA-384**, or decide not to care.

### Q&A

**On Grover's algorithm:**
- The quadratic speedup from Grover is very slow in practice — *"borderline fictitious."* That's why SLH-DSA's 128-bit parameters are fine even though they're nominally 64-bit under Grover.
- Grover **cannot be parallelized**, so it's largely ignorable here.

**Q: How does the cube-root collision finding relate to Grover?**
- BHT actually uses Grover as a subroutine (Grover inverts a function in √n time), which is how the cube-root collision algorithm arises. Bottom line: don't worry too much about this.

**Q: What about non-linear quantum speedups to PoW mining?**
- A recent paper found this completely impractical. Grover matters even less here: the smaller the problem, the smaller the effective speedup, and because quantum machines are so slow at Grover, the problem size must be gigantic before the quadratic advantage shows up at all.

**Q: Any cracks in the fundamental SHA primitives (Merkle–Damgård)? Could quantum do better than classical there?**
- Classical attacks are definitely progressing — e.g., alongside breaking HAWK, AI-assisted work broke **7-round AES**. Could models reach 8 rounds next year? Unknown; we can't predict.
- Notably, **few people are studying quantum attacks on specific block ciphers / SHA-256** — the research communities are fairly disjoint. Some papers exist but little progress. Quantum doesn't seem very helpful against symmetric systems so far — but that could change.

**Closing thought:** we should use *system context* to design better schemes — signatures designed for the specific system they live in. (Segue to Antonio: e.g., a short-term key stored in Ethereum account metadata, updated across transactions.)
