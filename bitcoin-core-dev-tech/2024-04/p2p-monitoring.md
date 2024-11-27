---
title: P2P Monitoring
tags:
  - bitcoin-core
  - p2p
  - developer-tools
date: 2024-04-09
---
[Slides](https://github.com/kouloumos/bitcointranscripts/blob/temp_core_dev_slides/bitcoin-core-dev-tech/2024-04/files/2024-04-Peer-observer-CoreDev-Berlin-2024.pdf)

- Started working on this about 2 years ago; in 2021. After we accidentally observed the address flooding anomaly/attack
- Primarily uses https://github.com/0xB10C/peer-observer to extract data from Bitcoin Core nodes with tracepoints.
- The infrastructure also includes a fork-observer connected to each node as well as an addrman-observer for each node. Additionally, detailed Bitcoin Core debug logs are avaliable. The main part are the Grafana dashboards. 
- There’s a public version at public.peer.observer, which is redacted to not leak honeynode IP addresses. Happy to provide access to an internal version. 
- Grafana dashboard shown, for example:
	- in and outbound P2P messages per node
		- observed drop in inbound version coming in when linking lion was down
	- current inbound connections
	- block connection duration
	- transaction rejected from mempool
- More automated alerting and anomaly detection is a todo.

