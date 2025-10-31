---
title: Low Level Sockets Abstraction
tags:
  - bitcoin-core
  - p2p
date: 2025-10-23
---

Conceptual conversation around PR 30988 [Split
CConnman](https://github.com/bitcoin/bitcoin/pull/30988)

`Peerman` and `CConnman` are currently interacting quite a bit, because we
provide callbacks between each other. In `CConnman`, we have

- code and logic that is specific to bitcoin p2p code
- low-level sockets stuff. Sockets and P2P code is intermixed

The newly proposed `SockMan` class idea is to isolate the sockets logic inside
`CConnman`, and give it a nice interface. `CConnman` is too big and too hard to
reason about. In isolation, the separation/interface seems like a good idea,
makes everything more testable.

Are we trying to keep behaviour the same? Yes, behaviour should not be changed
at all. 

Do we have any actual use cases of re-using `SockMan`? Yes, HTTP server. E.g.
{new connection, someone sends data on the socket, disconnect, listen for new
connections}: http server has to do most of that. Similar logic for Stratum V2
(sv2), the work of which is now abandoned.

Did the `SockMan` approach make things easier for fuzzing? Hasn't been tried
yet, could be an argument in favour of this refactoring even without additional
consumers of the interface.

What are the cons of this refactor? Somebody has to do it, somebody has to
review. There was pushback on sv2 being a use-case, since that's no longer a
goal as we're using the sidecar approach. Someone argued it's the wrong level of
abstraction: 

- `SockMan` is not reusable
- is extremely opinionated wrt our p2p code

Even if we ignore the http and sv2 use cases (i.e. no reuse), isn't it still
easier to reason about socket stuff? The concern is about trying to make
`SockMan` generic. If we're swapping in `SockMan` or libevent - we'll find
`SockMan` is very opinionated, e.g. runs in a single thread. Reimplementing http
server on top of that would mean we can't control the event loop etc. So, this
should be squashed down: `SockMan` just does p2p. 

If we're going to do HTTP layer with our own socket implementation, we have
`EventsPerSock` and sock class, and you can build your own event loop and server
on top of that, supporting e.g. multiple threads. This is a relatively trivial
effort, we don't need a virtual class in between there. We can avoid the map
lookups from virtual fn calls, and just integrate it tightly.

An alternative approach would be using libuv. That means adding another
dependency - which some people argued we're trying to avoid. Not necessarily,
argued others, we're trying to get rid of *unmaintained* dependencies.

Let's say we want to start using libuv. If we have the `SockMan` interface
abstraction, swapping in libuv should become easier. 

The question was raised if people would feel comfortable with the refactor if
`SockMan` is kept specific to p2p, without the goal to reuse it for e.g. http.
There were no concerns raised against that conceptually. E.g. `NodeId` is a
handle that can be passed between layers, but in http library, everything can
live in that same layer, and you can share memory between socket and http.

One downside of `SockMan` interface is it adds virtual calls. It would be
undesired if P2P performance and inspectability decrease because of an
abstraction layer that we want to be using somewhere else. If there's only one
user, the methods don't necessarily have to be virtual.

It's hard to create these kinds of abstractions in the correct way, that's both
general purpose and performant, generally you have to pick one of both.

Most p2p logic does a bunch of business logic, with socket logic intertwined.
What the #30988 is doing, is extract the socket logic into separate functions,
to improve readability.

Has performance been benchmarked? Not yet. Behaviourally, is obvious that
nothing should be changing, except for smaller things like virtual function
overhead. Is there an easy benchmark that can be done? IBD was raised as the
most interesting thing to measure.

[PR #32747](https://github.com/bitcoin/bitcoin/pull/32747)  introduces
`SockMan`"light", that doesn't introduce any http logic, and then http logic
introduced in [#32061](https://github.com/bitcoin/bitcoin/pull/32061). The http
PR is only for http server, it's not abstracting code, it's not touching p2p
code. A concern was raised that we shouldn't work on the http part until we've
decided on the broader abstraction question.

We haven't decided yet if ripping libevent out is a goal, or if it is a goal
now. E.g. we could also wait for new c++ features.

If we implement payjoin in wallet, wallet will need to make outbound requests.
However, we already have `Sock` and other primitives that should do the trick:
Sock, http, and event loop.

Initially `SockMan`-light was based on the `SockMan` pr, but in current shape
they don't depend on each other. So the same code is in both PRs.

Any reasonable C++ code that implements http from scratch, would use an event
loop. The go-to choice at the moment is libev. It works for free, state of the
art performance, tested, bulletproof, low level socket stuff. Here, however,
we'd be implementing our own abstraction to implement a tiny fraction of that,
potentially poorly. Either we should be using state-of-the-art, or use existing
low-level stuff. Is there room for middle ground? If we decide to use external
library in the future, swapping that in will be easier if we have a sockets
interface.

What's the pressing need to replace libevent today? It still compiles, it still
works, ... It's not pressing, but it would be nice. Is it worth a thousand eng
hours? If we can wait a bit and do it better later? We already had libevent bugs
(e.g. remote crash through rpc) in the past, it's hard to reason about. But one
participant thinks our own generic interface would probably be also hard to
reason about.

Sjors' sv2 client has 50ms latency for every message that gets sent. Nobody
complained. pinheadmz's http server had similar latency issues in the beginning.
This was because of optimistic send. Our event loop works in a specific way,
allowing outside world to send a message without queuing up. It wasn't obvious
at all why using our opinionated interfaces was causing significant performance
degradation. tl;dr servers should be bundled with their own event loops, because
getting the details correct is hard.

## Action items

- more conceptual review on the PRs
- get pinheadmz's thoughts on this, as the author of the `SockMan`-light / http
  PR
- show that there is no performance degradation because of the interface,
  especially in IBD. This can be done at a later stage when there is a rough
  consensus around the interface.
