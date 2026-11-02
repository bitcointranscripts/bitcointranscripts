---
title: Quantum Priorities
tags:
  - bitcoin-core
date: 2026-10-16
---

## Proactive versus reactive approaches

The discussion distinguished two broad categories of quantum-resistance work:

- **Proactive measures:** introducing output types and cryptography that allow users to migrate before a quantum threat materializes.
- **Reactive measures:** recovery or migration mechanisms used after “Q-day,” including scenarios where vulnerable funds have already been frozen.

Many participants expressed little interest in the reactive category, preferring to focus on migration before an emergency. This was a preference expressed during the session, not a recorded decision to exclude recovery research.

## Recovery protocols and migration incentives

The reactive discussion referenced rescue protocols and commit–reveal mechanisms, including Lifeboat associated with Tadge, Dropkick associated with conduition, work associated with roasbeef, and an Anchorage-associated “turnstile” proposal. The notes do not provide enough detail to reconstruct or compare those designs.

A central objection concerned incentives: **the expectation of a future rescue mechanism could discourage timely proactive migration**. Users might postpone moving funds if they believed recovery would remain possible after the threat became immediate.

Participants also questioned the knowledge-asymmetry assumptions and game theory underlying some recovery approaches. The notes characterize these foundations as uncertain but do not capture a specific attack analysis or resolution.

## Proactive output types

The proactive discussion covered both output formats and the signature schemes that could support them.

P2TRv2 and P2QR were named as output-type proposals. 

The relevant BIP work was described as not set in stone, leaving room for changes as the cryptographic and operational trade-offs became clearer.

## Signature schemes and operational trade-offs

Several signature approaches were discussed:

| Scheme or approach | Points raised |
|---|---|
| **SHRINCS** | Described as the most widely discussed option, but also as highly constrained. The notes do not enumerate those constraints. |
| **Stateful signatures** | Offer more compact signatures, but introduce state-management risks that can lead to loss of funds. |
| **Stateless signatures** | Discussed as an alternative path, alongside the compactness advantages and operational risks of stateful designs. |
| **FAEST** | Discussed in connection with AES, possible use of SHA-256, higher verification costs, and the NIST process. Participants noted that the SHA-based approach would not treat SHA purely as a black box. The notes do not establish a precise variant or standardization status. |
| **PRAWNS** | Described as a threshold, stateful hash-based signature scheme, with interaction required to generate a Winternitz one-time signature (WOTS). |

The stateful-versus-stateless distinction was particularly important because it connects cryptographic efficiency to wallet safety. Smaller signatures are not the only consideration: a design must also account for the consequences of managing signing state incorrectly.

## Development priorities

The session also raised a resource-allocation question: how much developer effort should go toward improvements to existing classical signature schemes, and how much should go toward optimizing post-quantum alternatives?

## Outstanding questions

The discussion left several issues open:

- Whether reactive recovery mechanisms provide a useful fallback or weaken incentives to migrate early.
- Which output types and signature schemes are suitable for proactive deployment.
- Whether the compactness of stateful signatures justifies their operational risks.
- How to divide development effort between existing cryptography and post-quantum work.

The clearest emphasis in the notes was on **proactive migration**.