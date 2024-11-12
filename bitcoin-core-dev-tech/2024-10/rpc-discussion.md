---
title: RPC Discussion
tags:
  - bitcoin-core
  - rpc
date: 2024-10-16
additional_resources:
  - title: 'Issue #29912'
    url: https://github.com/bitcoin/bitcoin/issues/29912
  - title: 'PR #31065'
    url: https://github.com/bitcoin/bitcoin/pull/31065
---
## Spec

Issue: [https://github.com/bitcoin/bitcoin/issues/29912](https://github.com/bitcoin/bitcoin/issues/29912)

Core Lightning is using JSON-schema to generate a lot of stuff, should see if we can replicate that for our RPC interface. Enables generating Rust client bindings, Golang, JavaScript?...

Having generated client code could help decrease maintained code in bitcoin CLI, like special handling of non-string args.

Exact currency units should be defined in the schema to avoid past confusion. Still some concerns over more complex units like BTC/KvB and sats/vB.

## REST

New PR for posting transactions to REST: [https://github.com/bitcoin/bitcoin/pull/31065](https://github.com/bitcoin/bitcoin/pull/31065)

Current REST interface is read-only and not authenticated.

Historical context: REST was there because it's faster than RPC, but IPC should be even faster.

Concerns over it being hard to remove transaction submission from REST once it's in.

Users can use per-user whitelist in bitcoind to limit what an RPC user can do, to avoid giving access to wallets.

Action: Should communicate current philosophy to keep REST readonly and recommend RPC with whitelist.

REST is potentially dangerous because of cross site scripting attacks.

### Standalone application

Idea/direction to make a REST standalone application (web server), similar to HWI. Using future IPC (Cap’n Proto) interfaces.

Start small with REST converted to use limited IPC interface, then possibly break out RPC server repo. Should make sure the IPC interface is stable first. Nice to eventually remove dependencies in the main repo.

Possibly expose IPC to clients eventually, but way too early now.

## Misc

Kernel has a monopoly on the datadir. Should the kernel itself have an IPC interface? Way too early.

You might be able to do more flexible IPC transaction interaction than RPC.

Multiprocess will officially be finished in 10 years. :) But some are hopeful for initial release in v29.

RPC is private compared to P2P, so prefer using that. Also, P2P is more complicated to interact with than RPC.
