---
title: 'Breakout Session: Post Quantum Cryptography for Hardware Wallets'
transcript_by: Localhost Research
date: 2026-08-28
tags:
  - quantum
  - hardware-wallet
speakers:
  - Charles Guillemet
additional_resources:
  - title: Slides
    url: https://btctranscripts.com/bitcoin-transcript/quantum-workshop/2026-08/breakout-session-post-quantum-cryptography-for-hardware-wallets-slides.html
---

_For slides, please see the 'Extra Info' tab_

**Why act now**
- The Bitcoin community's perspective on PQ has clearly evolved — not because a quantum computer is coming tomorrow, but because a **non-zero probability creates fear**, and if trust erodes, that must be addressed.
- Migration requires picking the algorithm *and* answering broader questions: What does it mean for blockchains (block size, etc.)? What's the timeline and execution plan?
- This session focuses mostly on the **algorithm choice**, given its impact on hardware wallets.

**How hardware wallets work today**
- Core security property: **seed/key confidentiality**, generated with high entropy.
- Built on **secure elements** (smart card technology — effectively a small computer), with Ledger's operating system on top managing applications:
  - Different coins → different applications
  - Mono-threaded architecture; apps isolated from the OS
  - **Derivation path locks** — the Bitcoin app can only derive Bitcoin keys
- **"What you see is what you sign"**: the host is *not* trusted; the device's own screen makes that trust unnecessary.
- **Attestation**: genuine device proofs, firmware upgrades with strong guarantees of authenticity. ⚠️ The current secure channel is **not post-quantum**.

**The constraint problem**
- Current secure elements are deliberately tiny: **10→64 KB RAM, 320 KB→1.5 MB flash, 28→70 MHz CPU.**
- Hardware acceleration exists for AES, DES, and modular multiplication (RSA/EC) — **nothing for PQ**. PQ must be implemented in software on-device, with constrained performance.
- And they'll need to implement *all* the algorithms, because they support so many blockchains.

**Benchmarks**
| Scheme | vs. ECDSA |
|---|---|
| Falcon | ~20× slower |
| Full SPHINCS (current SE) | ~300× slower — **~7 minutes** |
| Full SPHINCS (next-gen SE with PQ support) | ~60× — several dozen seconds |
| **SHRINCS** | **Completely acceptable performance** |

**PQ secure channel work**
- Ledger has designed a **PQ upgrade and attestation protocol**, KEM-TLS-inspired, with a **proof written in Lean 4**, currently being audited.
- No standard exists for PQ secure channels in embedded setups — **they will share the standard they create**.

**Discussion note**
- On Trezor-style open-source secure elements: hard to compete with a well-resourced actor.
