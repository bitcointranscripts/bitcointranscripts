---
title: Attacks on Lightning
date: 2024-11-20
---

## Three Categories of Attacks:

1. **Loss of Funds**
2. **Privacy**
3. **Quality of Service**

## Brainstorming of Existing Attacks

![Diagram of existing attacks](https://raw.githubusercontent.com/bitcointranscripts/media/refs/heads/main/bitcoin-research-week-2024/attacks-on-lightning/comparison-table.jpg)

- **Jamming**

  - **Slow**
    - Proposed solution: Reputation.
  - **Fast**: Send a large number of HTLCs in a short time.
    - Proposed solution: Fees.
  - Mitigation has been proposed but not implemented.

- **DoS Attacks**

  - Implementations may not be well-prepared.
  - Not HTTP-based, so common tooling (e.g., Cloudflare) is not applicable.

- **Route Hijacking**

- **Probing / Balance Discovery**

  - Purpose: Track individual payments.
  - Becomes harder with increased traffic and noise on the network.

- **Discovering Hidden Channels**

- **Using Tor**
  - Both Lightning and Bitcoin may face disadvantages when using Tor.

## Network-Level Attacks

- All communications in Lightning are encrypted, with onion routing for payments.
- However, these may not be sufficient.

### Attack Scenario

An attacker (e.g., a large ISP or AS controller) could:

1. Correlate packets based on timing and packet size. _(Revelio)_
2. Infer the sender and/or receiver.

### Mitigation Ideas

- **Padding**: Could help but raises questions about implementation:

  - Padding to a constant size vs a distribution of sizes.
  - Should mobile users have the option to opt out?

- **Commitment Batching**:
  - Breaks patterns and may provide some protection.
  - Challenges:
    - Attackers might adjust.
    - Only benefits large routing nodes. Except we do cover HTLCs (probes) on each individual node.

### Open Questions

1. What is the contribution of timing vs message size in attacks?
2. Is a constant bitrate necessary?
