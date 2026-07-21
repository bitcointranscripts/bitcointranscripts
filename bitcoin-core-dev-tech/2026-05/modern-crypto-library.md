---
title: Modern Crypto Library Discussion
tags:
  - bitcoin-core
  - cryptography
date: 2026-05-08
---

- what would a modern PQ crypto library look like? So that it at least
  has a chance of getting merged in core.
- should it be just hash based signature (or) only lattice based
  signature (more parameters, more complex) maybe library could support
  both?

1. Audience
2. Language? C89 - no, C++ - no, rust, SHA-NI,
   - architecture specific assembly = SHA256 (faster)
     - won't clang produce better than manually crafted asm?
     - Inline assembly is verifiable? No - much less projects which have
       formal verification.
   - it doesn't need to be C89
   - formal verification is part of "modern crypto library". The
     community is mostly looking at rust.
   - VST used for formal verification (being used for libsecp, looks
     like in 90s, loads quickly, lindy effect), remix person online
     (verified C implementation of OTS using LLM - he has experience
     producing proofs)
   - no verificable C++
   - what would a rust crypto library for core look like? we don't
     necessarily need to use rust over C.
   - hash based signatures are not rocket science, someone can vibe code
     it in 2 hours.
   - Rust stability is a problem. Bootstrapping rust is complex in guix.
     No other problem.
   - Current contributors know C. Not sure how much C contributors
     prefer writing C89. Decision of cryptography contributors.
     - C code for years, might not be confident with rust. If the
       compiler can help you - that's better. We've overlooked stuff
       that looks obvious in hindsight.
     - C formal verification is more cumbersome. But still doable.
   - signing HSM might get complex. C at least runs on every
     microcontroller.
   - what rust version?

- contributing.md says scope -
  https://github.com/bitcoin-core/secp256k1/blob/master/CONTRIBUTING.md#scope.
  we can always add new stuff (adapter signature, DLC etc..)
- separate repo for hash based primitives.
  - in libsecp not very critical for fast hash based
  - in PQ - super critical for super fast hashes
- better error handling.
- hopefully no dynamic memory allocation + scratch space
- how do you do spec? Spec in formal language is very complicated.
  Hacspec is out of fashion. rocq/coq nowadays.

3. BIP reference implementation/spec

Any don'ts?

- no dependencies
- no openssl

How do you do runtime detection of hardware optimisation? The library
doesn't implement SHA. This PQ library won't implement SHA? Having to
compile in every system + benchmark - makes sense for where hashing is.
Runtime detection - can't happen in the library.

Anything similar in testing? Particularly:

- constant time test smart in rust. Writing rust crypto code + fighting
  compilers. Lot of crypto code written in rust. Standardised ways -
  comparison crate you need to import etc.. C you can copy over from
  libsecp.

Is writing language bindings possible in rust? yes.
