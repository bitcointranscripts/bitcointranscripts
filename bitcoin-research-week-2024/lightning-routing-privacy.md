---
title: Lightning Routing Privacy
date: 2024-11-19
---

## Different privacy topics

- HTLC/MPP correlation
- Balance Discovery
- Intra-LSP payment
- Network level attacks
- Async Payment privacy
- Client Fingerprinting

## Top 3 list

### Balance Discovery

- Some mitigation by payment splitting
- More traffic, more noise? How precise can BDA even be?

### Network level attacks

- **AS-level attacks**
  - Constant size packets
  - Constant bitrate
- **On-path attacks**
  - Route randomization
  - PTLC

### Intra-LSP payment

- Unclear how to solve
- Maybe something something Tumblebit?
- Maybe route randomization/longer routes + PTLCs?

![Whiteboard](https://raw.githubusercontent.com/bitcointranscripts/media/refs/heads/main/bitcoin-research-week-2024/lightning-routing-privacy/whiteboard.jpg)
