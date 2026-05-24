---
title: External Interface Discussion
tags:
  - bitcoin-core
  - rpc
  - ipc
date: 2026-05-06
---

External interfaces discussion
(JSON-RPC / REST / ZMQ / IPC / `-blocknotify` `-walletnotify`)

- goal: think about future directions for interfaces
  - when new features and changes are proposed, discuss how to evaluate
    and have a consistent approach
  - discuss whether there are any interfaces we want to replace /
    deprecate
- ZMQ interface
  - sends block and transaction notifications
  - read-only interface
  - zmq has not been worked on in recent years, just one significant pr
  - best effort, no guarantees
  - mostly used used by lightning (lnd, eclair) also used by
    mempool.space
- JSON-RPC interface
  - canonical interface
  - documented on website
  - has overhead from json
- REST interface
  - was created originally to offer an unauthenticated alternative to
    JSON-RPC, and also enables bypassing JSON serialization overhead,
    can return raw blocks & transactions
  - also used for convenience, subset of RPC
- IPC interface
  - new kid on block
  - goal: high performance interface
  - over time could replace JSONRPC/REST/ZMQ for some use-cases
- Q: Do we want to continue supporting ZMQ?
  - ZMQ has some maintenance burden: requires suppressing some sanitizers
  - Another reason to remove might be that having multiple interfaces
    could be confusing to users, unclear which to use
  - Equivalent IPC interfaces not yet available
- Shell notification interface: `-blocknotify`, `-walletnotify`
  - could remove these, replace with other interfaces
  - but these are convenient and comparatively simple to maintain
  - removing would require recepients to use long running processes
    which they do not need currently
- Option: IPC interface could be extended to be a replacement for ZMQ
  - IPC Chain interface #29409 provides similar notifications
  - IPC is also not a direct replacement for ZMQ because IPC only
    listens on unix sockets, not TCP sockets
    - Exposing IPC over TCP would require restricting what methods could
      be called based on connection type, which is is not done currently
  - If ZMQ support removed, backwards compatibility could be provided
    through shim. Instead of bitcoind sending ZMQ notifications,
    external shim could translate IPC notifications to ZMQ notifications
- Option: C++ interface classes in `src/interfaces/` needed for IPC could
  be used by JSON-RPC, REST, etc to avoid duplicate code between
  implemenations
  - Some JSON-RPC mining methods currently use `Mining` c++ interface
- Option: REST and JSON-RPC interfaces could be unified
  - JSON-RPC methods could be marked "authentication not required" to be
    exposed over REST
  - REST request handler could also accept authentication heads and
    expose privileged methods
- Question: What to do if new REST endpoints are requested?
  - Lightning developers have requested txospenderindex access over
    REST, want unauthenticated access
  - We could require new REST endpoints to be be implemented as
    JSON-RPC methods, but would be nontrivial
- Question: Should encourage IPC for new requests?
  - Example: getting transaction at position from block
  - Using ipc has tradoeffs
    - requires capnproto, not accessible from all programming languages
    - requires long lived connection, more round trips
    - JSON/REST tooling is nicer: curl, jq
- Overall problem is duplication: need to replement things like
  txospenderindex access for multiple interfaces
  - JSON-RPC is not ideal canonical interface because has overhead
  - IPC interface (C++ classes in src/interfaces/) may be better
    candidate
  - Even if reuse implementations, duplicate documentation may still be
    required
    - Example: submitBlock is same for RPC and IPC needs to be
      documented twice, maybe should be reused
    - Example: RPC getblocktemplate method and IPC mining implementation
      have a lot of differences, so documentation can't be reused
    - If generating shared documentation, using IPC doxygen
      documentation would require extra builds steps, while JSON-RPC
      documentation is more structured and easily accessible
- Goal could be to move all business logic out of interface
  implementations
  - Current JSON-RPC implementation mixes application logic with
    UniValue parsing and generation. Creates JSON result object first,
    then populates it.
  - Current REST implementation has lots of conditionals based on output
    format
- Question: How to expand IPC interface?
  - IPC Chain interface PR exists but has lots of methods shouldn't be
    used externally
    - don't want expose kitchen sink
  - IPC interfaces could have stable & unstable methods, while only
    supporting stable methods externally
  - First use-case for IPC could be supporting external indexes, and
    support for external wallets could build on that
- All interfaces have PRs currently open for review
- Question: How to deal with RPC methods that take many positional
  parameters (`createwallet`)
  - Confusing to decide whether to add new positional parameters or use
    named-only parameters (options objects)
  - Rule for new optional params could be to use named-only by default,
    and allow passing by position when have a specific reason (parameter
    is required or very common)
- Problem: IPC interface can be awkward to call due to threading
  - Clients have to choose which thread asynchronous calls execute on,
    and create threads for calls to execute on
  - Could be improved by server executing requests on a thread pool when
    client does not specify an execution thread
