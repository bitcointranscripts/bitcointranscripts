---
title: Covenants
tags:
  - bitcoin-core
  - covenants
date: 2024-10-17
---
## 1) What are we solving?

- scaling? 10x, 20x, 100x?
- new use cases?
- giving users sovereignty?
- MEV concerns?

## 2) Different groups (some overlap with above):

- "ticking clock" for self-custody
- slow and steady
- buildoors
- ossification now

## 3) Various approaches:

a. One weird trick (CAT? CTV?)

b. App-specific (APO), "LNHANCE"

c. minimal batched toolset: TXHASH(CTV), CSFS, CAT, TAPTWEAK, ???, Could keep going on this: OP_MUL, other general tools

d. overhaul: Great Script Restoration (GSR) - (overhaul of script engine sigops-> varops)

e. rewrite: Simplicity

## 4) Sensibly talking about L2s

## 5) "Consensus"

Discussion of what is Consensus, individual definitions of consensus.

“If you can’t find a bug in this PR” is not consensus.

Discussion of privacy aspects, not just scaling.

Discussion of what the current usage of these proposals and the layer 2s on top
of them says about actual need/demand.

More clear goals are helpful. Rigor around data and research to back up approaches.
