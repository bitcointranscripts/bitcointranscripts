---
title: Private tx broadcast
tags:
  - bitcoin-core
  - p2p
date: 2024-04-08
---
Updates:

- TX is validated before broadcast (using mempool test).
- The sender ignores incoming messages from the receiver (except the handshake
  and PONG), so the sender cannot send back the tx before disconnection.
- When it receives the tx back, it becomes "just a tx in mempool".


TODO/NICE TO HAVE

- Check if the wallet is going to rebroadcast a tx it has created but has been
  broadcast via private broadcast and if yes, prevent that.
- Consider disabling `walletbroadcast=1` if `privatebroadcast=1`, or in other
  words - enforce `walletbroadcast=0`.
- RPC to check the stats.
