---
title: LN Simulation Workshop
date: 2024-11-21
---

## Tools and Frameworks

- **Warnet**
- **SimLN**
- **Scaling Lightning**
- **Polar**
  - Good for teaching because of the GUI

## Goals

- What's best for research/writing papers
- Pressing issue: padding

## Payment Channel Networks (PCN)

Are there any frameworks for PCN besides LN?

- **Sprites (?)** - Patrick McCory paper
  - Master smart contract
  - Doesn't have the increasing time lock issue that LN does

## WARNET

- **Helm, k8s**: Launches a p2p network of core nodes with LN nodes attached
  - Hundreds of nodes
  - Imports “neighborhood” of the mainnet LN graph
  - Potential use case: more than one LN node per BTC node
    - Or Electrum or Neutrino
- Documentation is OK, can also be a service
- Internet connection adjustments at the network level:
  - Netem
  - Most realistic simulation includes traffic patterns, geolocation, latency, etc.
- Can run locally with Minikube or Docker Desktop
- `IsRoutable()` hack for Bitcoin Core to gossip addresses

## SIMLN

- Handles payments between nodes and channels
- Orchestrates nodes to work with Warnet
- Supports defined activity vs random activity
- Not for specific attacks, more for background noise. Attacks carried out by separate processes
- Possible to spin up two clusters and connect nodes such that every link goes across the internet between clusters

## Related Tools

### PlanetLab

- Universities host machines locally, offering a slice of every machine worldwide
- Used for networking experiments (low CPU availability)

### TransitPortal

- Geographic distribution
- Includes an AS to the internet for attack experiments

### Shadow

- Tor simulator

## Warnet/SimLN Requests

- Support for laptop use cases
- Multiple LN nodes per Bitcoin Core backend
  - Regtest Core nodes
- Private channels
- **NetworkX** graph models
- Customizable interface for many nodes with opinionated defaults
- High-frequency LN payments for stress testing
- SimLN: Mix random and preset payment activity
- More client versatility:
  - Clients that change payloads
  - Use local images with attack mods
- How do we measure "emergent properties" (hard to define)
- Support for: CLN, Eclair, LDK

## Ideas for Simulations

- Model activity from other payment networks (e.g., LTC from a few years ago) onto LN
  - Roles like payment processors, users, sinks, faucets, etc.
  - Sender/receiver profiles
  - Could be run in multiple Warnet scenarios
- Long-Term Simulations
  - A different simulation class; would not rely on k8s clusters
- Bitcoin Network Topology
  - Simulate with node birth/death over time, fast forward to observe results

## Research Experiment: Padding LN Messages

- **“Vuvuzela”**: Send all messages to all neighbors
- Gossip messages look different than payment messages

![Flipchart 1](https://raw.githubusercontent.com/bitcointranscripts/media/refs/heads/main/bitcoin-research-week-2024/ln-simulation-workshop/flipchart1.jpg)

![Flipchart 2](https://raw.githubusercontent.com/bitcointranscripts/media/refs/heads/main/bitcoin-research-week-2024/ln-simulation-workshop/flipchart2.jpg)

![Flipchart 3](https://raw.githubusercontent.com/bitcointranscripts/media/refs/heads/main/bitcoin-research-week-2024/ln-simulation-workshop/flipchart3.jpg)

![Flipchart 4](https://raw.githubusercontent.com/bitcointranscripts/media/refs/heads/main/bitcoin-research-week-2024/ln-simulation-workshop/flipchart4.jpg)
