---
title: Fingerprinting
tags:
  - bitcoin-core
  - privacy
date: 2025-10-23
---

General Fingerprinting Strategy

## Overview

Discussion focused on fingerprinting vectors in the network, strategies for
mitigation, and the balance between security improvements and engineering
effort.

***

## Key Challenges Identified

### Fingerprinting Vectors

- Multiple fingerprinting vectors exist and are difficult to fix
- Easy to introduce new vectors in the future (whack-a-mole problem)
- General lack of awareness about fingerprinting issues among users

### Types of Fingerprints

- **Global vs Local fingerprints** - Important consideration when prioritizing
  fixes. Global ones allow to detect pairs of connected nodes network-wide
  without prior suspicion, local ones confirm a suspected match.
  - Example: addrman fingerprint
- **Node uptime patterns** - Nodes being turned off/on creates fingerprinting
  vector
- Nodes send same transactions (invs) at same time
  - Recent change to timing behavior
    - Correlation still possible despite timers

***

## Proposed Strategies

### 1. Dual Node Approach

- Run two connected nodes on different networks

### 2. Selective Fixing Approach

- Fix easy-to-remove vectors
- Deprioritize vectors requiring significant engineering effort
- Consider effort vs benefit for each case
- Potential refactoring at netprocessing layer (significant effort)

### 3. Accept Limitations

- Acknowledge that complete non-fingerprintability requires huge effort
- Focus on what's reasonable rather than perfect
- New features should not be blocked on fingerprinting risk

***

## Technical Details

### Addrman Cache Mechanism

- **Previous behavior**: Each request leaked some IPs
  - Vulnerability: Repeated requests could expose full addrman
- **Current behavior**: Response is cached and reused for one day
  - Prevents full addrman exposure through repeated requests

### Tor/Clearnet Considerations

- **Why run on both networks?**
  - Protection from eclipse attacks
  - Protection from partition attacks
  - Reference to old paper explaining risks of Tor-only operation
  - IBD (Initial Block Download) significantly slower on onion-only

- **Bridge node concerns**
  - Risk of losing bridge nodes if behavior changes announced publicly
  - Bridge nodes provide important network connectivity

### Lightning Node Implications

- Difficulty in leveraging fingerprints to steal money

***

## Proposed Solutions

### Outbound-Only Configuration

- Allow only outbound connections on different networks
- Benefits:
  - Still provides bridging functionality
  - Increases privacy
  - Makes attacks harder (attacker must obtain connection slot)

***

## Documentation & Communication

### Transparency Considerations

- **Question**: How public should fingerprinting information be?
  - Options discussed: Private gist vs private repo
  - No good solution identified

### Recommendations

- Document known issues in Bitcoin wiki if not fixing
- Announce as known problem and encourage specific behaviors
- Balance transparency with security concerns
