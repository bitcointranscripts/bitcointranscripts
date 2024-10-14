---
title: ASMap
tags:
  - bitcoin-core
  - security-enhancements
  - p2p
date: 2024-04-11
---
## From virtu's presentation

- Distribution of nodes in ASes is low
- 8k reachable clearnet nodes / 30k unreachable
- A contributor has different statistics that show a lot more nodes, not sure which numbers are (more) correct. These numbers are would mean that some of the simulations are already a reality.
- Most nodes from Hetzner and AWS
- Shift compute and bandwidth to nodes in small ASes
- Unreachable nodes cannot sustain ten outbound connections 

## Discussions

- Ignore AS for blocks-only connections?
- ASMap could not be so effective for nodes running in big AS
- Extra connection from a node in same network
- Simulations should consider eviction logic
- Do not protect outbound conns if we have more than one outbound
connection for that ASN
- Update `contrib/seeds/README.md` to recommend kartograf instead of getting file
from sipa's server
