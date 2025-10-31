---
title: net - net_processing split
tags:
  - bitcoin-core
  - p2p
date: 2025-10-23
---

Net Processing Refactor Discussion (transcript #1)

## Overview

This discussion covers two refactoring proposals for Bitcoin Core's peer-to-peer
networking layer:

1. **Sockman refactor**: Isolating socket management from peer connection logic
2. **CNode-to-Peer refactor**: Separating peer state management from connection
   management

***

## Part 1: The Sockman Refactor

### Current Architecture Issues

- **CConnman** contains mixed responsibilities:
  - Bitcoin P2P network-specific logic
  - Low-level socket operations
  - Callback interfaces to PeerMan
  - "Kitchen sink" of accumulated code

- **Problem**: Socket management and network logic are tightly coupled, making
  the code difficult to test, reason about, and reuse.

### Proposed Solution: Sockman

**Goal**: Isolate socket management into a separate, modular component

**Benefits**:

- Better separation of concerns
- Improved testability
- Easier to reason about code
- Potential reusability (HTTP server, sv3 connman)
- Easier for fuzzing
- Maintains existing external behavior (backward compatible)

### Key Arguments Against Sockman

#### Abstraction Level Concerns

- **The abstraction is too opinionated**: Sockman is not truly reusable; it's
  designed specifically for Bitcoin's P2P network requirements
- **Conflicts with general-purpose socket libraries**: Using libevent or similar
  multiplex libraries would be more flexible
- **Performance trade-offs**: Creating abstractions often requires sacrificing
  either generality or performance

#### Specific Technical Issues

- **Virtual method overhead**: Adds function call indirection, potentially
  impacting performance
- **Difficult to get right**: Both sv2 client and HTTP implementations that
  tried using Sockman had ~50ms latency issues due to the abstraction's
  complexity
- **Opinionated by design**: CConnman races through receives and sends, allowing
  direct message writes without queue overhead—this behavior is hard to abstract
  without losing performance

#### Library Replacement Arguments

- Sockman lacks features of a mature library
  - **Better to use established libraries**: libevent, libuv, etc. are
    battle-tested and performant
- **C++ 26 might provide better primitives**: Waiting for language improvements
  could yield better solutions

### Resolution

- Proceed with the original Sockman PR (code reorganization only, no behavior
  changes)
- **Probably close the "Sockman Lite" PR** (which included HTTP code)
- **Require benchmarking** (particularly Initial Block Download scenarios) to
  validate performance
- The boundary between P2P and socket management can be redrawn if someone
  proposes a better line

***

## Part 2: CNode-to-Peer Architecture Refactor

### Current State: The "Kitchen Sink"

**CConnman structure** (created 8 years ago):

- Started as a simple peer manager
- Accumulated peer-to-peer responsibilities over time
- Now bundles:
  - **CNode**: Massive class representing an entire connection's state
  - **State from higher layers**: IBD status, bootstrap state, etc.
  - **Coupled with PeerMan**: Peer management logic intertwined through complex
    interactions

**Example of tight coupling—disconnection logic**:

```
Disconnect initiated 
  → boolean flag set in CNode 
  → CConnman detects flag 
  → CConnman notifies PeerMan 
  → multi-step teardown dance
```

### Proposed Solution: Move to Per-Peer Architecture

**Core idea**:

- Move all state PeerMan needs into a separate **Peer** object
- Turn CNode into a pure implementation detail of CConnman
- Create clean interfaces between CConnman and PeerMan

**Scope**: Massive refactor (~200 commits)

- **Easier moves**: Connection-level data (ping time, etc.)
- **Harder conceptual moves**: Messaging handling thread, async disconnections

### Benefits of Peer Separation

#### State Management

- Decouple per-peer state from global state
- Move messaging handling thread into PeerMan
- **Enables parallel message processing** (currently serialized by what CConnman
  does with each CNode)
- Disconnects become asynchronous rather than synchronous

#### Testing & Modularity

- PeerMan no longer requires a full CConnman stub for testing
- Can pass mock objects instead
- Easier fuzzing without creating elaborate test infrastructure
- **Standalone PeerMan**: Can be tested independently with just interface calls

#### Interface Simplification

- CNode interface reduced to ~5-6 functions
- PeerMan becomes self-contained with its own event loop
- Enables **multiple CConnman instances per PeerMan** (theoretical: separate
  IPv4/IPv6 connmans, etc.)

#### Concurrency

- Two systems can operate out of sync, which is actually fine
- State reasoned about separately
- Protections achieved through ref counting: PeerMan increments ref count, runs
  event loop, decrements

### Advanced Outcomes: Multiprocess Architecture

**Natural evolution of the separation**:

- All socket handling (CConnman, Tor server, local IP discovery) in separate
  process
- Enables multiprocess Bitcoin Core with minimal additional work
- **2 commits on top** of the full refactor to enable multiprocessing
- CConnman can become a library with 6 function calls
- IBD can be done in ~100 lines of glue code (with custom net processing)

**Significance**: The fact that this is possible proves the architecture is
correct.

### Limitations & Realistic Scope

#### What Won't Change

- **No per-peer locks** at scale (doesn't work well)
- **No per-peer threads** (scalability issues)
- **Global PeerMan state** is reasonable and needed

#### Validation Layer Coupling

- **CNodeState** must remain separate (touches CSmain/validation)
- Next refactor target, but blocked by validation layer dependencies
- Goal: Separate validation state from peer-related state

#### Per-Network Architecture (Future Discussion)

- Considering: One PeerMan per network
- **Against**: Per-network mempool (too far)
- **Consider**: Caching validation state in Peer (10ms staleness acceptable, no
  need to "stop the world")

### State Duplication is Acceptable

- Both CNode and Peer end up holding copies of the same state (Tor status, etc.)
- Avoids lifetime/shared state issues
- Copies can be made because values are mostly snapshots (best block, etc.)
- **Same approach applies to validation state**: Just copy it across the
  boundary

***

## Part 3: Libevent and Broader Architecture

### Current libevent Issues

- Difficult to read and maintain
- Remote crash bugs due to libevent interface complexity
- Hard to handle general-purpose callbacks correctly at library level
- **Fundamental problem**: Inherent to any general-purpose library design

### Long-term Strategy

- **Don't wait for C++ 26**: Too nebulous, timeline uncertain
- **Keep Sockman-focused**: Rather than trying to replace the entire event
  system now
- **Evaluate trade-offs**: Engineering hours vs. potential future rewrites

***

## Part 4: Prefill & Connection State Abstraction

### Current Challenge

- Prefill depends on PeerMan knowing TCP window size and connection buffer
  capacity
- Can be abstracted: "There is a buffer you can't send too much to"
- Requires PeerMan-level visibility into connection state

### Address Manager Observability

- **AddrMan should not know current connection state** (observable by other
  peers = privacy issue)
- Bootstrap state is shared between PeerMan and validation layer
- Requires careful boundary definition

***

## Part 5: Next Steps

### Immediate Actions

1. **Clarify PR status**:
   - Original Sockman PR: soft agreement to proceed
   - Sockman Lite: **close (defer HTTP refactoring)**
   - Benchmarking: **required before merging**

2. **Form working group**:
   - Recruit additional conceptual reviewers
   - Current discussion limited to a few contributors
   - Need broader perspective

3. **CNode-to-Peer refactor**:
   - Start fresh with clear scope
   - Create draft PR with full implementation
   - Open as proof-of-concept
   - **Multiprocess demo** as eventual goal

***

Net Processing Refactor Discussion (transcript #2)

**GOAL**: turn `CNode` into a shared_ptr inside of `CConnman`, because it
clarifies lifetimes. Move all the state that `PeerManager` needs to node into
`Peer`, and make `CNode` an implementation detail of `CConnman`.

p2p and sockman stuff are mixed together, as demonstrated in [[Low level sockets
abstraction]]. The overlap of `PeerManager` and CConman is `CNode`. There is a
bit of an interface around `CNode`, but we violate it all of the time, e.g. for
disconnecting. When either side wants to disconnect, it updates a bool inside
`CNode`, `CConnman` picks it up and notifies `PeerManager`, starting a teardown
dance.

`CNode` was intended to go away. `CConnman` became a kitchen sink, which was
then intended to be broken up (but that hasn't happened yet). The
net/net_processing split work is orthogonal to [[Low level sockets abstraction]]
work.

`CConnman` and `PeerManager` are separated, but they depend on the state of each
other. `CConnman` tells `PeerManager` how to run.

`CNode` is a giant class that represents the entire state of a connection on the
p2p network, but it also has higher-level state. E.g. `CConnman` needs to know
if its connected, how much bytes sent, ... but it shouldn't need to know e.g.
"Am I finished with IBD?"?

`Peer` was created to store higher-level state for `PeerManager`, e.g.
synchronization status, and it takes cs_main. There was an earlier big effort to
add multiple locks to reduce cs_main usage. Last ping-time probably should be a
net thing, but is currently a messaging layer thing.

Another effort was to take things out of `CNodeState` into `Peer` (using the
individual locks).

Right now, we have `CNode` and pointers to it here and there, and manually count
references to `CNode`. When refs drop to zero, we delete it. This manual
approach could be replaced with a shared_ptr, however we have a need for
specific teardown sequence - i.e. we need certain code to be executed upon
deletion.

`PeerManager` takes a copy of all of `CConnman`'s `CNode`'s, ups the refcount
for all of them, runs through the even loop, and then drop the refs. Ideally,
`CNode` should not be leaked out of `CConnman`.

This work is pretty hard because code is very entangled. 

One example of difficulty: both `PeerManager` and `CConnman` need to know about
eviction. E.g. `CConnman` says "something needs to be evicted", and then
`PeerManager` decides what gets evicted. Further complicated by whitelists. If
`PeerManager` and `CConnman` were running in totally separate processes, which
should be in charge of that eviction logic? 

When PR? The code change is huge: 200 commits, mostly moving stuff from `CNode`
to `Peer`. The logic is very chunkable, luckily. Some things are easily moved,
but others are complicated.

`PeerManager` can run its own event loop once all the `CNode` logic it needs is
moved into `Peer`s. Changes like that are tougher to review conceptually, but it
allows more things to run async, and you can reason about state much better.
It's possible that you're trying to send messages to a peer that's already
disconnected, but that's no issue except for wasting a bit of time. Makes
testing and fuzzing a ton easier. Because net/net_processing distinction is now
so much clearer, you can now e.g. have 2 `CConnman` instances (e.g. tor and
ipv4, even thought that's probably not a great idea) for just 1 `PeerManager`.

Going further, net (`CConnman`) can run in a separate process with IPC. Once the
separation is done (~175 commits), adding multiprocess is trivial (~2 commits).
net/`CConnman` can also be turned into a library. That in combination with
kernel, means you can write a node does that ibd with just a few hundred lines
of glue code. Separating it out as a library may not be a goal, but is a good
indicator that it's a healthy approach.

One idea suggested is to have a `PeerManager` per-network.

The new approach e.g. copies `fDisconnect` so that `PeerManager` and `CConnman`
have their own view. This makes sense conceptually, e.g. if you send a tx and
then disconnect, then `CConnman` should treat that as disconnected, but
`PeerManager` shouldn't yet, because there is still work to do. The definition
of "disconnected" is different for both sides.

We've gone through these splitting exercises in the past a couple of times, and
there was support each time. If this is going to be pushed forward.

One concern raised: some of the prefill logic depends on factors like size of
the TCP window. That can be abstracted, however.

Instead of separating `PeerManager` and `CConnman`, another approach would be to
merge them together more. This could be beneficial for performance by e.g.
avoiding `NodeId` lookups using shared memory.

The plan is to form a working group to get reviewers and move things forward.
It's a large project, but attendants suggested this can still progress quickly
if there is good enthusiasm, let's not already assume that it's going to take 2
years.

## Action items

- don't stuff more things into `CNode` while we work on this separation
- open draft PR to showcase how all of this works
- talk to ajtowns about conceptual approach, there have been historical concerns
  here
- form a working group to get reviewers
