---
title: 'Breakout Session: SHRINCS'
transcript_by: Localhost Research
date: 2026-08-28
weight: 5
tags:
  - quantum
  - cryptography
speakers:
  - Jonas Nick
---

**Motivation**
- Building on the day's hash-based signature discussion (SPHINCS+/SLH-DSA): over the past summer, the team examined how to adapt these schemes for Bitcoin — specifically via different parameterizations.
- The most prominent lever is the **signature budget**: reducing it shrinks signatures, but only up to a point — go too far and the scheme is no longer stateless. **It's a spectrum, with a hard limit.**

**Core design: a stateful/stateless hybrid**
- Original insight: if signing only a few times *statefully*, signatures can be **very compact**.
- Model: a signing device generates a seed; you write the seed down; **the state never leaves the device**.
- If the seed is imported into a *new* device, that device must use the **stateless path**.

**Q: Why present both tree roots rather than a hash of both?**
- Merging gives two options: (a) append the stateless pubkey root to every signature (~16 bytes) for black-box compatibility, or (b) omit it and lose black-box compatibility.
- **Both roots are presented to preserve compatibility.**

**Operational note**
- Helpfully, **state is public** — the host in a hardware-wallet setup can act as belt-and-suspenders.
	- if the signing device can store even a single hash securely as a commitment to the state, then the host device doesn't need to be trusted. The commitment offers a way for low-memory signers to authenticate the state given by a host. The host can even guess-and-check from blockchain data to re-derive the correct state based on the commitment.
- You **cannot use stock SLH-DSA parameters** for this.
- Multisig setups offer additional fault tolerance for state loss. Signers can check and store state for each other. 
  - This however requires consensus among signers, BFT, and additional interactivity. 
  - MuSig already has interactivity, so perhaps acceptable. However, very few actually use MuSig!
- Wallets could reserve specific state for the assumed state-loss scenario. If you lose state, you use one of the reserved counters, that way you don't have to fall back to the stateful path. You would however rollover to a new keypair thereafter. 

**FXMSS — flexible tree structures**
- To sign many times via the stateful path, balance the tree to maximize capacity.
- Tradeoff with unbalanced trees: **smaller early signatures, larger later ones**.
- Structures can be mixed and matched — the format is flexible enough to design exotic layouts (e.g., very small first signatures, switching to balanced trees at the 8th signature, after which sizes blow up to a constant but with a large budget).
- **Recommendation: only two standard structures — balanced or unbalanced.**

**Q: Do different structures need different consensus-level verifiers?**
- No — the verifier is **agnostic to tree shape**, like the Taproot verifier.

Q: How do you handle restoring on multiple devices?
Each device must have a unique ID, which is mixed into the KDF when deriving keys. IDs can be public but seed stays secret. 

**Some concerns about statefulness voiced**:
- If you lose the state, you fall back on the stateless scheme that is huge (in terms of computation and size)
- State replay is a major challenge, you lose the funds. Managing data consistency is always a big issue.
- How to manage 2 different signers that share the same seed (happens often)
- How to manage potential TSS (even if it seems quite difficult to design)
- You would have to manage one state per key-pair. Users sometimes have 100s of UTXOs, 100s of accounts, 10s of different chains. All these states must be properly managed. Storing them in the device could be a possibility, however it doesn't scale, and comes with drawbacks when you need to recover your seed. So you could implement a merkle tree of monotonic counters, store the root in the device and the states outside. So that the device knows if the state is valid or not, and wouldn't sign with an invalid state. It requires a close collaboration between the software in the host and the device. Today the device is essentially stateless, the whole state is onchain and can be retrieved by the wallet. So, with SHRINCS, if a user creates his accounts with Ledger Wallet app, the state would be stored in the app. As soon as he goes to Metamask, these states wouldn't be shared... Potentially wallets could decide to only manage the stateless signature path
 - It's also important to be able to recover funds ONLY from the seed. With SHRINCS, it's not that obvious. Recovering your wallet, you would lose the states and fallback to the stateless path. HOWEVER, you still need the Wallet ID to sign on the stateless path, that is for now not derived from the seed. We need a solution for that.
