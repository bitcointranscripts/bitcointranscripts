---
title: BIP324 Hiding from Global Passive Observer
tags:
  - bitcoin-core
  - p2p
  - bip324
  - privacy
date: 2026-05-07
---

BIP 324: Hiding from Global Passive Observer

Topic and goal

- Discussion of next steps for BIP 324 (encrypted Bitcoin P2P
  transport).
- Central question: what can a passive observer (NSA, ISP, etc.) learn
  from Bitcoin packets, and what should Bitcoin Core do about it?

Threat model: who is the adversary?

- unsophisticated local observer. Can inspect network traffic (size,
  timing, type) with basic tools like Wireshark. Think hotel / school /
  simple corporate firewall. Usually only wants to block, not analyze.
- ISP.** More sophisticated, but constrained by economics. Recording
  everything for every customer isn't viable; targeted recording (e.g.,
  one customer under court order) is.
- Low-sophistication active observer (e.g., China-style). Makes
  connections, completes handshakes, harvests node addresses.
- Global passive observer. Intelligence agencies operating on a "record
  now, analyze later" model.

What harms are we actually trying to prevent?

1. Being blocked by a firewall.
2. The observer detecting that the user is running Bitcoin at all.
3. The observer learning application-level data (e.g., which
   transactions a node originated).

Where Bitcoin Core's responsibility ends

- We should not try to reinvent traffic shaping (padding, fixed-size
  messages at fixed intervals). Tor already does this.
- Tor, however, doesn't necessarily hide Bitcoin-specific traffic
  patterns.
- Open question: what does Bitcoin Core want to provide itself vs. punt
  to other tools? Plausible framing: *"If you need strong anonymity,
  use Tor."*
- Traffic shaping always worsens latency. Miners care a lot; most other
  users don't. So shaping *transaction relay* specifically would barely
  affect miners.

Possible application-level approaches

- Replace variable-size `INV` with a uniform data stream to peers.
- Shape only transaction relay, targeting the same (or slightly worse)
  latency as today.
- This hides transaction origin but does **not** hide that a node is
  running.
- To hide the node itself, change the default port (away from 8333).
  - Problem: DNS seeds don't support ports. May need to drop DNS seeds.
  - DNS caching is good for privacy against seed nodes, but not against
    your ISP (which you'd hit).

Global traffic shaping considerations

- BIP 324 produces a pseudorandom byte stream, but very little other
  traffic looks like this — Bitcoin ends up standing out. Some firewalls
  are already blocking it (link in the BIP).
- The hope is that more protocols adopt pseudorandom byte streams over
  time.
- Mimicking TLS is very hard, especially since TLS keeps changing.
- Web traffic becoming pseudorandom would help, but probably won't
  happen.
- Port 443 would help with blending in, but requires root.

Limits

- Node addresses are relayed on the network. Anyone running a node can
  collect them, so they can identify other nodes.
- The upper bound on what an attacker can learn is therefore: whatever
  an attacker running their own node can learn.

Promising directions

- Fix the port situation** so that blocking 8333 doesn't trivially
  work. On first startup, pick a random port and persist it so the
  announced IP stays reachable. (Question: is anyone else already doing
  random server-side ports?)
- Application-level shaping for transaction origin against passive
  observers — uniform intervals and message sizes, or padding
  transactions up to a fixed or dynamic size (with an upper bound). Does
  not defend against active attacks.

Research questions

- Can a passive observer reliably detect the `INV` → `GETDATA` → `TX`
  exchange and extract the transaction size?
