---
title: TCP Hole Punching
tags:
  - bitcoin-core
date: 2026-10-15
---

Reference: [TCP hole punching for Bitcoin nodes behind home NATs](https://delvingbitcoin.org/t/tcp-hole-punching-for-bitcoin-nodes-behind-home-nats/2497)

## 1. Motivation and overview

The idea, raised at the previous CoreDev meeting, is to implement TCP hole punching so Bitcoin nodes behind home NAT routers can accept inbound connections without conventional port forwarding.

Early experiments reportedly worked on hotel and conference Wi-Fi, in-flight networks, Starlink, and even through some VPN configurations. The key mechanism is TCP simultaneous open.

## 2. How TCP hole punching works

### NAT behavior

A home node typically connects through a router:

```text
Bitcoin node → NAT router/firewall → Internet
```

The NAT table maps internal ports to externally visible ports and governs which return packets may be admitted.

When a node sends an outbound packet, the router may create a temporary mapping. Even if the remote side is not yet accepting a connection, that mapping may remain open briefly.

### TCP simultaneous open

When two NATed nodes initiate TCP connections toward each other at approximately the same time, their outgoing packets can create reciprocal mappings. Packets may cross in transit, allowing a TCP connection to establish.

TCP simultaneous open is described in TCP RFCs. The discussion noted that competing connections might arise and one may be dropped.

### Timing and compatibility

The discussion estimated a window of roughly one to two minutes for many firewalls, beginning when a node sends an outbound packet. Both peers must act within a compatible window.

NAT mapping and filtering behavior—including endpoint-independent filtering—affect whether this works. UDP hole punching is generally easier because UDP carries less connection state.

## 3. Discovering and reusing external ports

Bitcoin’s `version` message tells a node which IP address and port a peer sees. This information can help determine the externally visible NAT mapping. The operating system normally assigns different ephemeral ports to outbound connections, but an application can bind a particular local source port.

The proposed sequence is:

- Make an outbound connection to an already reachable node.
- Learn the external IP address and port reported by that peer.
- Reuse the appropriate local source port and listen for potential connections.
- Send an outbound packet toward each desired destination to open the NAT mapping.
- Complete simultaneous open when the other peer sends its corresponding packet.

A listening port can serve multiple connections, but a fresh outbound attempt is needed for each peer. The method depends on compatible NAT behavior.

## 4. Implementation options

### Option 1 — Coordinator-assisted hole punching

```text
Home node A ↔ Coordinator C ↔ Home node B
```

The eventual TCP connection is direct between A and B.

- A is behind NAT, wants inbound connections, and is already connected to coordinator C.
- A advertises its address through `addrv2` with an indication that it is reachable through C.
- B learns about A through address gossip, contacts C, and asks to connect to A.
- C tells both sides to initiate their TCP attempts.
- B establishes a direct connection to A; C may optionally disconnect afterward.

This proposal requires a new hole-punching address type or encoding in `addrv2`. Privacy concerns arise if everyone relies on one coordinator or if nodes reuse coordinator connections for unrelated activity.

### Option 2 — Tor-assisted coordination

A runs a Tor onion service and advertises `addrv2` information linking its clearnet address and Tor address. B uses Tor to coordinate the hole punch, then the peers communicate directly over clearnet.

Potential benefit: faster direct connectivity.

Open question: if Tor already supports inbound reachability, how much additional value does switching to clearnet offer?

### Option 3 — Peer-eviction handoff

When coordinator C is full and needs to evict two inbound peers, it could introduce them to each other via hole punching rather than merely disconnecting them.

A concern is that each peer would receive a connection it did not independently select, despite Bitcoin’s stronger trust assumptions for self-selected outbound connections.

### Option 4 — Proactive coordinator matching

Like Option 3, except coordinator C pairs peers proactively rather than only during eviction. The peer-selection and trust questions remain.

### Option 5 — Manual RPC coordination

Add an RPC for initiating a hole punch. Two node operators coordinate out of band—for example, using IRC or Nostr—and arrange the connection themselves.

### Option 6 — Coordinatorless ephemeral-key scheme

Each node advertises its IP address and an ephemeral public key through `addrv2`. These keys are not intended as long-lived identities.

- A and B encounter each other’s advertised public keys through address gossip.
- Both derive shared cryptographic material and use the current block hash as salt.
- They derive a common timestamp at which to attempt the hole punch.
- Among candidate pairs, they favor the pair whose derived value has the most leading zero bits, expecting both sides to choose the same match.

Open issues include reliable mutual selection, timing, and malicious advertisements containing false IP addresses. Address-relay spam already exists, but this feature could introduce new incentives.

## 5. Group discussion: What problem does this solve?

### Increasing available inbound slots

The central concern is insufficient inbound capacity. Rough figures mentioned during the discussion were approximately 20,000 reachable nodes versus 60,000–80,000 nodes that cannot receive inbound connections. These are informal estimates, not verified counts.

More hole-punchable home nodes could increase capacity, but only if those connections serve the required network role.

### Network resilience

The discussion recalled a node supporting about 80,000 inbound connections going offline, prompting a large wave of reconnections and peer evictions. This was used to argue for distributing inbound capacity and overprovisioning inbound slots.

### Sybil and censorship resistance

A greater share of independently operated home nodes could diversify the network beyond commercial data centers and potentially reduce the impact of certain Sybil attacks.

Hosting-provider restrictions, with Hetzner and DigitalOcean mentioned as examples, were cited as a censorship-resistance motivation. Neither benefit is automatic: selection rules and peer treatment matter.

### Privacy

A port opened only in response to a coordinated attempt may be less visible to unsolicited port scanning than a conventional public listening port. That advantage has to be balanced against metadata exposure through coordinators or address advertisements.

### Existing precedent

The group pointed to NAT-PMP being enabled by default (`natpmp=1`) as evidence that improving home-node inbound reachability is already a network goal.

## 6. Implementation status

The experimental patch was described as roughly 1,000 lines, much of it tests and documentation, and the work was characterized informally as “vibe-coded.” Several real-world network tests had been tried.

No final implementation option or adoption decision was recorded in these notes.

## 7. Open questions and trade-offs

| Area | Question |
|---|---|
| Network benefit | Does improved home-node reachability materially improve the network topology? |
| Peer trust | Should hole-punched connections count as inbound or outbound for peer-selection security? |
| Coordination | Can a coordinator be used without unacceptable privacy costs? |
| Scale | How would matchmaking or coordination operate across many nodes? |
| NAT compatibility | What fraction of deployed NAT devices reliably support the needed behavior? |
| Abuse resistance | Could attackers spam false endpoints or coordination requests? |
| Durability | How stable are connections on restricted and mobile networks? |
| Protocol complexity | Are the benefits worth changes to P2P address handling and connection logic? |

## 8. Main takeaways

- TCP hole punching appears plausible for many Bitcoin nodes behind NAT, based on early experiments.
- The central engineering challenge is peer discovery and coordination, not just TCP simultaneous open.
- Six approaches were discussed: coordinator introductions, Tor assistance, eviction handoff, proactive matching, manual RPC, and ephemeral-key scheduling.
- More reachable nodes do not automatically improve security: inbound/outbound classification and peer choice remain important.
- Potential benefits include inbound capacity, resilience, infrastructure diversity, censorship resistance, and reduced port-scanning exposure.
- The discussion was exploratory; whether these benefits justify the complexity remained unresolved.

***

*Editorial note: Notes have been reorganized and spelling standardized. Tentative proposals, estimates, and uncertainties are retained as such. No external technical verification was performed.*