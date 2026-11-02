---
title: "Libmultiprocess: Windows support and client integration"
tags:
  - bitcoin-core
date: 2026-10-12
---

# Libmultiprocess: Windows support and client integration

## Scope

The session covered Windows support for libmultiprocess and Bitcoin Core’s inter-process communication (IPC), together with the corresponding client-side work in `sv2-tp`. The notes identified three related pull requests and focused on compiler testing and a possible version 33 target. [^4]

## Implementation work

The work spans the underlying library, Bitcoin Core’s integration, and an application connecting to Core over IPC.

| Pull request | Purpose |
|---|---|
| [libmultiprocess #231: Add Windows support](https://github.com/bitcoin-core/libmultiprocess/pull/231) | Adds Windows support to the IPC library, including spawning child processes connected to their parent. It generalizes interfaces that previously assumed Unix file descriptors to work with stream types. |
| [Bitcoin Core #32387: IPC Windows support](https://github.com/bitcoin/bitcoin/pull/32387) | Integrates Windows IPC support into Bitcoin Core as part of the process-separation project. It combines the library work with Core-side build and platform-compatibility changes. |
| [sv2-tp #93: Windows](https://github.com/stratum-mining/sv2-tp/pull/93) | Adds the corresponding Windows client support, incorporating the library and Core IPC adaptations, dependencies, and Windows testing needed for `sv2-tp` to connect to Core. |

The library changes provide Windows-specific handling for sockets and process creation. In particular, the proposed implementation uses a named pipe to pass duplicated socket information to a child process, allowing parent and child to communicate without relying on Unix process and file-descriptor behavior. [^1] [^1]

The Core PR is an integration draft dependent on the underlying library work, rather than a standalone, merge-ready change. The client PR likewise depends on Windows support in both libmultiprocess and Bitcoin Core. Its testing includes native and cross-built Windows configurations, with mining and backend-disconnection scenarios. [^2] [^2] [^3] [^3]

## Compiler testing and portability

The main feedback recorded in the session was to **test with `clang-cl`**, because Bitcoin Core might move to that compiler. Participants also suggested that doing so could simplify some compatibility work, citing a static assertion in the Core PR as an example. This was a possibility to investigate, not a recorded compiler-migration decision. [^4]

For context, the PR includes a workaround for a compile-time assertion involving Cap’n Proto’s `MAX_DOUBLE` constant. Under MSVC, that floating-point constant is not available as a constant expression, so the assertion cannot compile. The proposed guard skips that assertion under MSVC while retaining it for Clang; the integer-constant assertions remain enabled. This illustrates the kind of compiler-specific workaround that `clang-cl` testing could help assess. [^2]

## Release goal

The stated hope was to get the work into **version 33**. The notes do not record a firm commitment or merge decision. The concrete follow-up was to test the Windows implementation with `clang-cl` alongside the server- and client-side integration work. [^4]

**References**

[^1]: [Add windows support by ryanofsky · Pull Request #231 · bitcoin-core/libmultiprocess · GitHub](https://github.com/bitcoin-core/libmultiprocess/pull/231) (34%)
[^2]: [ipc: add windows support by ryanofsky · Pull Request #32387 · bitcoin/bitcoin](https://github.com/bitcoin/bitcoin/pull/32387) (32%)
[^3]: [Windows by Sjors · Pull Request #93 · stratum-mining/sv2-tp · GitHub](https://github.com/stratum-mining/sv2-tp/pull/93) (19%)
[^4]: [Libmultiprocess Windows support session · GitHub](https://gist.github.com/Sjors/2e415423eefbd139bde09f1f0ab6bd07) (15%)