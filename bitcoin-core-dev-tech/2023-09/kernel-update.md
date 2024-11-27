---
title: Kernel Update
tags:
  - bitcoin-core
  - build-system
date: 2023-09-18
speakers:
  - thecharlatan
---
Original roadmap decided by carl was:

- Stage 1
  - Step 1 Introduce bitcoin-chainstate "kitchen sink"

- Step 2 (wrapped up ~2mon ago) remove non-valiation code

- Step 3 (where we are rn) remove non-validation headers from bitcoin-chainstate
  - We have mostly implemented

- Step 4 integrate libbitcoinkernel as a static library
  - Have the implementation on personal repo
  - Need to look into breaking up files or live with code organization not being super logical

- Stage 2 (we should talk about this now) improve libbitcoinkernel interface

## Open problems

(no opinions on what to do yet, we can discuss later this week)

- Bubbling up fatal errors
- Cory is working on leveraging clang-tidy to enforce this
- Also need to figure out how to do this without
- What we should do with mempool and policy. If not in the kernel, how to isolate?
- Should kernel have any Bitcoin Core-specific functionality like assumevalid and checkpoints?
- Can these features be "clients" of kernel?
- Do kernel users have to use Core’s state model?
- E.g. UTreeXO data model. Maybe we should make it plugable
- Defining a C header, guarantee stable api?
- Should we expose system resources like thread/file handles in these headers
- Compile-time vs run-time config, e.g.
- Abstraction?
  - Layer (1) opinionated elegant simple API on top of (2) kitchen sinky one

In the last few months, had convos with potential kernel users

- Alternative full node implementations
- People who want to validate on embedded devices
- Data science utilities that need to use Bitcoin Core data structures etc. and value high performance

## Q&A

- Do you want to have fights about these things now or tomorrow?
- Who’s going to write the C headers api? Manually = very complicated. Is one option to generate them?
- Currently thinking we can wrap every function with Russ’ util::Result for coherence. Then come up with clever macro
- Seems like a lot of these questions may be determined by the use cases. Other people can define their own C headers
- What’s important to me is that there is utility to Core. If not useful to Core, then we shouldn’t do much.
- C headers should be the last thing then.
- Data model is interesting. One reason this took so long is discussion about doing this safely. Wasn’t sure about giving client this abstraction as it can be footgun. Question might be what is the use case instead of what is safe.

- What project is most likely to be the first user?
  - #1 is bitcoind, #2 is the Bitcoin Core project. Secondary is external users like alternative implementations.
  - Our usage:
    - Maybe tests, as a lot of things can be tested without full bitcoind
    - Standard utility like a rescan util
    - Get the kernel separated and if we get that far, then others would probably find that interesting

- We made some bad calls with bitcoinconsensus that we shouldn’t repeat. We tried to make it as clean as possible, but that made it a little bit useless. We should try to focus on making this useful.
