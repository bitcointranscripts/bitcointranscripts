---
title: Silent Payments Update
tags:
  - bitcoin-core
  - silent-payments
date: 2026-05-07
---

- The current way we do payments in Bitcoin is broken
  - Where should I pay you? Please generate an address for me?
  - Users like static codes like bank account numbers
  - We want to preserve privacy
  - Anyone that knows an address of an HD wallet may traverse the history
- Silent payment addresses are an "ingredient" of how to derive a
  dynamic address
- Tradeoffs:
  - Expensive to scan for
  - Look through every transaction and perform an expensive EC
    multiplication
  - Sending side is easier to implement
  - Sparrow has implemented sending, receiving is experimental
- Works great with BIP353 DNS resolution
  - Was not a great idea before to post a static address, now it is
- Retroactive privacy loss in the presence of a (relevant) quantum
  computer
- Recipient decides on the use of labels
  - Cheaper than generating a new SP address
  - Labels are also used for change
  - Controversy in `libsecp` to support many labels or not
    - Currently can support many, many labels
    - Alternative approach would cause linear increase in cost for each
      additional
  - Wallet metadata BIP includes label data to assist in scan
- We are on take 4 of the `libsecp` PR
  - PR needs review
  - Test vectors are up to date from BIP-352
  - No security proof yet (what are extra assumptions)
