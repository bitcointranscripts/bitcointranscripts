---
title: Multiprocess Binaries
tags:
  - bitcoin-core
date: 2024-10-15
---
Should we make separate multiprocess binaries, and where should they be placed?

The mining binary ideally gets released in the v29 release so SV2 users don't need to compile their own binaries.

## Builds

Do we just turn multiprocess on for depends builds? E.g. that wouldn't test multiprocess in all current CI jobs. Whereas if we enable multiprocess by default, that
But besides the build flag, at least some functional tests also need changes to test the multiprocess binaries. But we also shouldn't switch _all_ functional tests over to only use multiprocess binaries.

So we probably just need a new option just for CI that allows picking which tests are ran with multiprocess.

## Wrapper

We at least currently probably don't want to expose users to all the new multiprocess binaries, so we're going to start with a `bitcoin` wrapper with subcommands such as `node`, `wallet`, ....

- Will using this make debugging harder?
- What about codesigning?
  - If you want to run `bitcoind` on macOS, you _need_ to codesign (at least for arm64), so we'd need to sign more binaries

## Windows support

What do we need to do to add Windows support? There's a missing include file (related to sockets) at the moment, but it's not that complicated to fix. Also, more recent Windows versions support UNIX sockets, so relying on newer Windows versions is one avenue to explore, even though we don't want to push requirements too high. Windows 10 Redstone 5 was one suggestion (but unverified if that supports UNIX sockets).

Consensus was that Windows support does not necessarily need to be in the first release (v29) and can be added later.

## Review priority

A tracking issue is going to be opened to keep track of the mining interface progress, that should be the review priority.

## Next release

For v29, we expect to release 2 new binaries in a separate `lib_exec` directory: `bitcoin-node` and `bitcoin-wallet`, and a new `bitcoin` binary in the `bin` directory.

## Versioning

Should we have some kind of versioning in the interface for e.g. if we _want_ to break backwards compatibility (which cap'n'proto documentation discourages by never changing things, just adding)? Adding a semver-like version number could address that. But also, versioning is actually already built-in through `MakeMiner()` - because cpnp already adds numbers to functions anyway.

For now, at least for the mining interface, breaking changes shouldn't be an issue (incl for the SRI folks) as long as we communicate. We're still early.

## Source code organization

Any expected changes to how code is organized because of multiprocess, or will everything just remain in the `build/src/` directory? I.e., will `cmake` need to make any updates? Currently, the plan isn't to change any of that, even though for multiprocess we might put them in `build/bin/`.
