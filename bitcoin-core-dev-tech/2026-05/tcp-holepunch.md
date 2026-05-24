---
title: TCP Holepunch
tags:
  - bitcoin-core
  - p2p
  - networking
date: 2026-05-08
---

- Suspect NATPMP hasn't improved inbound slot availability a great deal
  on home networks
  - Maybe NATPMP is not widely supported?
  - Maybe this is because of node-in-a-box + docker?

- TCP hole punching succeeds ~60% of the time to make a symmetric
  connection when two are behind NAT
- A and B connect to a coordinator C; C can coordinate a simultaneous
  SYN between A and B to the correct port; maybe the NAT reuses the
  mapping and they can connect to each other
  - There's an RFC for it?

- This has different properties from traditional inbound and outbound
  connections — maybe symmetric inbound?

- e.g. protocol: a listening node A has all inbound slots occupied and
  one of the existing inbound connections B advertises support for
  connection handoff; someone C attempts to connect to A, they get
  handed off to B and A disconnects from B

- Next steps: have a Python script and get data on how well tcp hole
  punch works on various hardware / networks

- Could C grief by interfering with connection, maybe predicting SYNs?
  Maybe not an issue with BIP 324

- libp2p implements tcp hole punching

- An alternative protocol closer to real outbound: A makes a special
  non tx/block relaying connection to a coordinating node C that offers
  hole-punch services; A advertises in some new `ADDR` message that it
  can be connected to via C; B sees in its addrman node A and attempts
  connection via hole-punch coordinator C
  - This allows C to sybil by pretending to control many addresses; it
    can e.g. stuff AS space that it doesn't control with bogus addresses
    - Instead treat all nodes with address C or that use relay C as one
      address with address C; when C is selected from addrman, try a
      random address either C or that C can coordinate TCP holepunch with
    - This is still a real outbound, increases the amount of inbound
      capacity on the network by making reachable what otherwise
      wouldn't have been, but it does not increase the number of parties
      N that are part of the 1 of N trust assumption of network
      participation

Related Delving Bitcoin discussion:
https://delvingbitcoin.org/t/tcp-hole-punching-for-bitcoin-nodes-behind-home-nats/2497
