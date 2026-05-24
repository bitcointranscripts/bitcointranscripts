---
title: Coins Cache Cleanup
tags:
  - bitcoin-core
  - utxo-set
date: 2026-05-05
---

- Currently there is a large interface that promises a lot
  - In-memory and disk implement the same interface
  - Mempool needs a read-only interface for the cache
  - Override does not make any sense for read-only (i.e. batch write)
  - Codebase has been "append only" rather than a proper refactor
- Goal is to restrict the interface depending on the context
  - Will this method be able to write to the cache?
  - Is this multi-thread safe?
- Multi-threaded coin fetch is now much cleaner
- An invalid use case is the `HaveCoin` retrieves the coin data but does
  not deserialize it
  - Inevitably the coin will be deserialized later, so this is a
    pointless roundtrip
- Invalid states should immediately crash in the case of disk corruption
  or serious serialization issues
  - `HaveCoin` returns true regardless of if the data is valid or not
    - Has caused an "invalid block" which caused user IBD to fail
- Interface changes to avoid side effects
  - `Get` coin may not be necessarily thread safe
  - `Peek` is used to access coins in a thread-safe way
- Another approach would be separate readers, writers, and cache-less
- Functional changes should ideally be separated from refactoring changes
- It is debatable if cleanups should go before or after functional changes
  - Refactor can inform functional changes
  - 5 refactor PRs were merged that now simplify validation changes like
    parallel coin fetch
- The line between changes and refactors can be muddled
  - Changes to dead code may be effected regardless
  - Changes to templates are difficult to discern between dead code or
    not
- The current interface promises too much
