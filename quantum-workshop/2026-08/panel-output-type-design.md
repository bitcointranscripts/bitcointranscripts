---
title: Output Type Design Considerations
transcript_by: Mike Schmidt
date: 2026-08-28
weight: 4
tags:
  - quantum
  - output-script-design
  - tripwire
  - signature-aggregation
speakers:
  - Pieter Wuille, conduition
---

This panel was moderated by Justin of Localhost Research. 

*Reference: [delvingbitcoin.org — PQC output type discussion](https://delvingbitcoin.org/t/pqc-output-type-discussion/2749)*

### Framing

- Topic: how do PQ schemes hook into Bitcoin consensus — output types and their design?
- This isn't Bitcoin's first output-type transition (BIP11, BIP16, SegWit, Taproot) — but this time **we're more informed**, with real usage and migration data.

### The Two Main Proposals

**P2TRv2 (Pieter)**
- Background: Taproot's key path / script path design, with unused paths hidden. Taproot hasn't seen the adoption hoped for — partly because the low-feerate environment blunts its space savings.
- P2TRv2 = P2TR with **PQC opcodes / leaf types added**.
- Crucially, with the **explicit agreement and clear expectation** that a user opting into this output type accepts that **EC spending can and will be disabled**.

**P2MR (Conduition)**
- P2TR with **EC key tweaking removed** (~360 origins).
- **No depth-zero trees** — removes the mal-incentive toward a single spending condition, which degraded privacy.
- Possible combinations with other ideas: CISA, key recovery — since P2MR is less efficient to use pre-Q-Day.

### The Tripwire

- Codifies the expectation of disabling EC spending: **if secp DLP is demonstrably broken** (example triggers were listed), EC spending in P2TRv2 is disabled.
- Disabling applies **only to P2TRv2** — not P2TR or other types. Because it's explicit in the output type, it avoids being seen as confiscation.
- Pieter doesn't actually expect EC disabling to happen *via* the tripwire — its purpose is an **upper bound** that forces users to take EC-disabling seriously, removes doubt, and removes the risk of EC disabling in it being considered confiscatory among users and potential migrators.
- Criticisms and alternatives discussed:
  - Some see it as *"at best a psychological thing."*
  - Similar proposals use **toy curves** — a ladder of increasing curve sizes — but there's no way to know whether attack progress will be fast or slow, and individuals can run such demonstrations independent of consensus rules.
  - Tripwires could serve other purposes too (e.g., triggering **rescue protocols**), not just EC disabling.
  - Incentivization: tripping the wire is a public good (cf. Google's demonstrations) — people could **donate to the tripwire address to form a bounty**.

### Steal vs. Freeze — "The Existential Threat"

- *"The biggest threat, the hardest problem, is the steal-vs-freeze discussion"* over Satoshi-era coins:
  - **Letting quantum computers steal** violates the expectations people have of cryptocurrency — what's the point?
  - **Freezing coins** — then what distinguishes Bitcoin from anything else, if coins can be frozen?
- **Taking coins out of this equation — via migration — is the priority.**

### Witness Structure & Costing PQ Signatures

- Pieter: introducing a **new witness** is a big step (but slightly less than segwit was), especially for hash-based signatures, given the bytes-vs-cost distinction.
- Effectively a block size increase available **only to PQ signatures** — justified because those bytes are easier to process.
- On costing: you *could* price PQ sigs per-byte like Schnorr, but that doesn't make sense — instead  I argue for something based on both bandwidth and computation costs.
-  Audience member comment: keep throughput the same and adjust the costs, alternatively
Response to the above: Keeping the throughput the same is a technical possibility, not a goal on itself..
- **PQ data blob / new witness lessons learned:** DoS concerns exist just at the P2P layer, plus data structures get duplicated everywhere. You can introduce a new witness and nest the old hash inside it — somewhat less painful to upgrade than the original SegWit witness.

### Should We Wait for Better Cryptography?

- Today's cryptography doesn't let Bitcoin migrate *fully* to PQ (no HD keys, limited confidence in schemes, etc.).
- To avoid the freeze/steal dilemma, migration should start sooner — especially for the long tail. The scheme should be reasonably adoptable by everyone (industry, Lightning, etc.).
- Having *"something"* people can adopt is enough to establish Bitcoin as quantum-ready ("street cred"). Throwing more features in risks delaying implementation and activation.
- Real-world adoption constraints:
  - Engineering cost for the ecosystem (wallets — including multicoin wallets that rarely ship Bitcoin updates)
  - Users must *want* to adopt it; fee considerations matter
  - Witness changes are more invasive and more political

### Recommendations & Comparison

- **Pieter's short-term recommendation: P2TRv2 with tripwire, using the simplest PQ signature scheme. P2MR later, or with a more advanced scheme.**
- User/usage types influence the approach: assuming *perfect* usage (no address reuse or key disclosure), P2MR is PQ-secure — but assuming perfection isn't great. Thus **the tripwire applies equally to both proposals**.
- **P2TRH** was covered at a high level — summarized as *"a weird middle ground"* and not an easy-to-roll-out solution.
- A **hash-based first step** is the conservative option and can migrate the long tail of users without further action on their part.

### CISA / Signature Aggregation Impact

- Brief overview of cross-input signature aggregation (DahLIAS, etc.): more efficient blockspace use, lower fees.
- **More beneficial to P2TRv2 than P2MR** (P2MR needs the pubkey among other fields; 64-byte lower bound; half-agg gives ~96 bytes with P2MR).
- Note: these benefits exist **only pre-Q-Day**. Audience comment: this incentive muddies the waters.

### Audience Q&A

- **Should the output type discussion be tied to a new PQ opcode?** Runs into confiscation risks; P2TRv2 already carries both EC and PQ options. There's no realistic enforcement mechanism — that's what the tripwire is for — and people could just add a dummy key if forced. Since P2TRv2 has no other advantages, the whole point of using it *is* PQ.
- **Spending from PQ back to quantum-vulnerable outputs defeats confidence — can it be made one-way?** Idea floated: a standardness rule refusing to relay PQ→quantum-vulnerable spends. Pieter sees this as unrealistic — you couldn't pay "anyone" anymore.
- **Special key-path key signaling the key path is disabled?** No benefit vs. P2MR; feels hacked-in. (Debate about whether it eases deployment.)
- **NUMS point generation for the tripwire?** Options discussed for a BIP-specified generation process; also an OP_RETURN-with-private-key option; also: a Taproot script-only key put on chain — if it's ever spent via key path, that's proof DLP is broken. Counterpoint: a rational attacker will simply avoid the tripwire.
- **Is the tripwire immediate, or does it take effect next targeting period?** *(Raised; discussion not captured.)*
