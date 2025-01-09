---
title: P2P Attacks
date: 2024-11-19
---

### Avoidable Attack in May 2023: Ordinals

Specifics of the attack aren't as important. Issue is that a simple DOS was possible in the wild and it  wansn't noticed before it happened.

- **Context:** Ordinals/Runes/etc.
- **Impact:** Nodes became unresponsive, maxing CPU (DOS-like behavior).
- **Cause:**
  - A sorted list used as a queue to send transactions to the network.
  - Queue became huge, creating a feedback loop where sorting couldn’t keep up and the queue never cleared.

#### Questions & Discussion

- **Q:** Unconfirmed transactions?  
  **A:** Yes, mempool.

- **Q:** Separate queue for each peer or combined?  
  **A:** Separate. Each queue was full.

- **Q:** Where is the problem? Should the queues be dumped when they get full?  
  **A:** The problem lies in sorting.

- **Q:** What was the fix?  
  **A:** Drain at a rate proportional to how full the queue is, rather than using a constant rate.

- **Q:** Do we kick/ban nodes for sending too many `inv` messages?  
  **A:** Not at the moment.

### Broader Concerns

We have people who look at the code, write functional tests, fuzz testing. But how do we catch issues like these before they happen? How do we prevent the next one?

#### Suggestions & Observations

- **Systemic vs. Unit/Functional Testing:**

  - Simulations could be helpful but are resource-intensive.
  - Kubernetes-based frameworks like Warnet could simulate dozens or hundreds of nodes.
  - Tools like Polar allow spinning up multiple instances for Lightning Network testing.
  - Minimal subsets of `bitcoind` as opposed to full instances might help in testing.

- **Simulation Challenges:**

  - Requires clarity on what to test. Unknown unknowns are particularly difficult to address.

- **Fuzzing:**

  - Helpful but can be dangerous because it requires refactor and touching scary code paths.

- **Extreme Testing:**
  - Internet-scale testnet as the ideal.
  - Kubernetes and stress-testing with simulated nodes as practical alternatives.

#### Known Testing Framework Gaps

- The current framework is simple and only identifies known issues.

### Strategies for Addressing Unknown Unknowns

- **Ideas:**

  - Network fuzzing.
  - Chaos Monkey.
  - Red Team exercises.

- **Additional Suggestions:**
  - Man-in-the-middle setups to amplify observations.
  - Multi-layered security approaches incorporating all strategies.
  - A year-long Red Team competition.
  - Differential testing with multiple P2P implementations to avoid a single point of failure.

### Bug Bounty Discussion

- **Q:** Does Bitcoin Core have a bug bounty?  
  **A:** No official program exists due to the lack of an organization and potential for exploitative incentives - indentives are hard, devs could try to sneak in attacks in order to fix them. However, external parties could fund bounties.

### Current & Future Threat Models

- **DOS Attacks:** Easy to spot.
- **Eclipse Attacks:**
  - Eclipse-type problems are harder to find.
  - Mitigations exist but unknown unknowns remain.
- **Other Concerns:**
  - BGP hijacking.
  - Malicious P2P messages (e.g., handshake procedures).

#### Suggestions:

- Hard to discuss these because the behavior isn't documented anywhere. Need to describe how things should work
- Document expected behaviors as a state machine with self-describing rules.
- Stress-test individual message types.

### Code Quality & Changes

- **Q:** Is the code getting more unweildy or spaghettified? Or cleaner as time goes?  
  **A:** There's a tension, some want cleaner/modularized code, others want faster with layer violations. Hopefully cleaner over time but always a moving target.

- **Q:** How often does the implementation change beyond bug fixes?  
  **A:** Frequently. Examples of newish major changes include encrypted P2P and package relay.

- **Comment:** The dominance of a majority client aids in deploying new features network-wide efficiently.
