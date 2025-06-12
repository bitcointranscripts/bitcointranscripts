---
title: Multiprocess
tags:
  - bitcoin-core
date: 2025-02-27
---

Think of multiprocess in terms of the features it provides.

## Multiprocess Features

The first main feature is modularization. Having a separate binary for gui,
wallet, node, that prevent lockups between processes. This also allows to e.g.
spin up multiple GUIs to a single node, or a node without wallet, ...

The second feature is the `-ipcbind` feature. In addition to be able to spawn
process, we can listen to a socket which anyone can connect to. This allows
third-parties (e.g. Stratum V2 as one current practical example) to hook into
Bitcoin Core internals. `ipcbind` was of course _required_ for the first feature
(modularization), but it just offers more flexibility on top of that.

This separation leads to a multitude of binaries, which can get confusing for
users. One solution explored is to add a new `bitcoin` top-level wrapper binary,
similar to how `git` is organized with a single wrapper that calls one of
hundreds of binaries through subcommands.

At a high level, the first step was to introduce interfaces between parts of the
codebase, instead of everyone accessing the same global functions and state.
Interfaces are classes with virtual methods. The IPC code is able to leverage
that, by providing a subclass for each of those interfaces. When you want to
access an interface in a different process, you just use the subclass instead of
the usual interface.

## IPC Features

Cap'n Proto is in some ways more helpful than gRPC would be because it can track
objects with state. E.g. mining interface can return a reference to a
blocktemplate object to an sv2 client, and because of reference counting, the
node will keep the blocktemplate (and transactions in it) in memory as long as
the sv2 client holds a reference to it, behaving a bit like a shared_ptr.

CaPnP supports multiple languages, so we can use different languages for
different processes.

## Libmultiprocess

What exactly does libmultiprocess add over CaPnP? It does a lot of different
things:

- each method has a context parameter, which is a libmultiprocess interface to
  handle threading.
- simplifies function calls. Without libmultiprocess, you'd first have to ask
  capnp to allocate a request object, set all the fields, send the request, wait
  for a response, then access the return value from the response struct.
- libmultiprocess is both run-time (e.g. simplifying function calls) and
  compile-time (generating the C++ subclasses based on interfaces and capnp
  files)
- threading: ensures calls execute in "the same thread" across processes.
  Bitcoin Core's requirements are atypical here in that it can rely on global
  locks (e.g. `cs_main`). The server creates a corresponding thread for every
  thread the client has (and that it uses to communicate over IPC). This also
  allows callback parameters to work: a lock can be acquired, a std::function
  parameter can be passed as an IPC method parameter, and the std::function
  object can be called and run on the same thread which acuired the lock.

Question:
> Should maybe some libmultiprocess functionality be upstreamed to CaPnP?

Answer: That's probably out of scope, it's too tailored to Bitcoin Core needs
and could be useful to some Capn'Proto applications but not most.

### Capnp files

Instead of manually writing .capnp files, we could add annotations to c++
interface classes and generate the .capnp files automatically. This would better
ensure everything stays in sync. But this is tricky to implement (requires
parsing c++ in some fashion). Also having .capnp files in repository does make
them either to consume from other languages (rust, python).

### Serialization

Question:
> If a function takes a dataclass as a parameter, is it serialized using our own
> serialization, or capnp's?

CaPnP is not opinionated on this, so it's all possible. If libmultiprocess needs
to serialize a parameter, it does so based on the type. To minimize our code
overhead, the current implementation checks if we have a native Bitcoin Core
serialization method and use that. Serialization can be overridden with
`BuildField()` and `ReadField()`

Within Bitcoin Core, serialization is kind of an implementation detail because
(de)serialization is handled automatically, but of course this is important for
third-party processes that don't use our capnp subclasses.

### Performance

Question:
> is there an impact on performance, e.g. for wallet rescan?

Currently yes, especially if a lot of data needs to be serialized (e.g. sending
all blocks). Instead, IPC-friendly functions should try to be organized in such
a way that less data needs to be sent, e.g. by letting the server do more
computations locally and then send the summary back to the client. There's also
the possibility to do cut-through.
