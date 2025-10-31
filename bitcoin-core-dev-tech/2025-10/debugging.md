---
title: Debugging
tags:
  - bitcoin-core
date: 2025-10-23
---

Debugging Workshop

- Shilling of https://github.com/bitcoin/bitcoin/pull/31723
  - Wanting to debug bitcoind in the context of functional tests
  - Showing how it's possible to debug certain bitcoind runs.
  - Mention of recently added commit which adds support to be able to tweak
    functional test code to be able to trigger a specific node (re)start to
    happen inside the debugger. Convenient in many cases, but may be more than a
    one-line change for cases where the node is started by code in the
    underlying framework.
- Talk around setting memory breakpoints on different debuggers and using pdb to
  debug Python side.

Feedback

- Would it be possible to do as a contrib script instead of adding complexity to
  test framework? Maybe modifying bitcoind.cpp is still okay.
- Maybe have the test framework output the bitcoind binary and command line it
  would have started, so one can run that within the debugger and debug from
  static initialization onward, avoiding having to modify bitcoind.cpp or having
  the additional CMake variable.
