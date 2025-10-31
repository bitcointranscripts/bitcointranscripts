---
title: Private broadcast
tags:
  - bitcoin-core
  - privacy
date: 2025-10-20
---

Discussion of https://github.com/bitcoin/bitcoin/pull/29415

**The proposal**: Just send the tx for one connection (Tor or I2P) and leave it
to broadcast it.

- Vasild started to split this PR into small PRs - some have been merged. The
  goal is to facilitate the review.

- It’s going to have 1p1c on this - in a follow-up - there is no current support
  for it.

- INV, GETDATA, then send the transaction - close the connection after sending
  the tx. The reason is to not send unsolicited txs because we might want to
  reject it in the future.

- It currently sends it to 3 peers.

- We try to not leak any information of us when opening the connection - we fake
  UA.

- Peerman has the transactions to be broadcasted and the private relay is done
  by the connman. It’s ordered by priority.

- “The transaction comes from nowhere” - there is no tor address related.

- This proposal would change the number of churn in the network.

- 64 max concurrent connections	 - what about I want to send a bunch of
  transactions? Is this number enough?

- Log category for private broadcast should be in the same PR, It doesn’t make
  sense to have it in a separated PR.

- `-onlynet=` (automated connections only with this network). However, using a
  proxy could relay private tx to ipv4/6 peers.

- "Using wireshark, can you identify this pattern?" - No.

- We should not update our addrman when doing the private broadcast - leave no
  traces.
