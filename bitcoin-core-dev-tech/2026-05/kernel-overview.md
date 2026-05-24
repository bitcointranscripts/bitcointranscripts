---
title: Kernel and What it Can Do
tags:
  - bitcoin-core
  - kernel
date: 2026-05-05
---

- Public interface was merged 8ish months ago
  - People have started to use it, although the interface can and will
    break
- Design goal is to minimize differences in public interface code
- Floresta is using kernel, which is a utreexo light client
  - Great for mobile wallets
  - Using script interpreter
  - Cannot use all of the current functionality
- Work to add functions that do not require UTXO context
  - Block validation is one such example
- Other users
  - SwiftSync PoC
  - SwiftSync hintsfile generation
  - `kernel-node` Rust full-node
- Current interface is very high level and cannot be called intermediate
  states (`ProcessBlock`)
  - `CheckBlock` is one of the first internals is that is exposed from
    block validation
- Defining the scope of the kernel
  - `Chainstate` is apart of the kernel, but should it move out, i.e.
    should the kernel be pure validation
  - Ergonomics of the C API can be difficult to use
    - Returning pointers to types can raise questions as to who cleans
      up the pointer
  - API must get to a point where kernel can be used internally
- How safe is the interface in a multi-threaded context
- Is there a multi-threaded fuzzer to check races
  - Probably not
- Back to the theme, what can you do?
  - Build your own node
  - Read data
  - Research
  - Limitations
    - Cannot be run in parallel to Bitcoin Core
