---
title: Multiprocess and mining interface
tags:
  - bitcoin-core
  - multiprocess
  - mining
date: 2025-10-21
---

## Context Arguments in IPC Methods

### Issue/PR: None

#### Current Behavior

- Every method has a context argument, but it's not mandatory
- Some methods exists without a context argument

### The Problem

Without a context argument, methods run on the I/O thread blocking the server,
which:

- Ignores new requests while processing
- Particularly problematic for waitNext() call, which waits for the next block
  to become available and would block the entire server. Fortunately waitNext()
  does have context, we checked. checkBlock doesn’t, while it should, but it’s
  not an urgent issue.

### Proposed Solutions

- Linter option: Add a linter to enforce context argument requirement
- Syntax change: Make context argument mandatory

### Compatibility Considerations

- Breaking changes in minor versions: Acceptable while feature is experimental
  - Users would need to recompile (with the new capnp file)
  - Team maintains an issue tracking desired small breaking changes
  - Plan: Bundle small breaking changes with any larger breaking change

## Breaking compatibility could enable other cleanups like providing safer default values

- C++ integrations: No current issues with default values
- Rust and similar languages: Don't support default values, currently need to
  provide their own

## Cancelling waitNext() Calls in Mining Interface

- Status: Nothing to discuss, solution is clear, needs implementation
- Expected behavior:
  - With two different block templates calling waitNext() on both, cancellation
    should only affect one
  - Global cancellation already occurs when node shuts down

## PR #33582 - Python Testing Interface

### Tool: pycapnproto

- Not well maintained
- Uses "free-threaded Python" (more like a normal programming language)

### Current Status

- Nothing really broken, just a warning, which in turn trips the functional test
  runner.

### Concerns

- If free-threaded Python is used, timing issues may break other components
- May need to report issue upstream to suppress the warning

## Crash on Submit Solution Call with Invalid Coinbase

### Root Cause

- Old code throws exceptions not designed to be IPC-compatible
- Serialization exceptions thrown by IPC code during
  deserialization/serialization process

#### Solution

- Need to catch exceptions on the Core side (not the IPC side)
- Example scenario: Passing an empty block to Core shouldn't throw exceptions,
  but serialization will fail during the process if there are any transactions

## Developer Feedback: Reusing Outside libmultiprocess

Current Issues

- Difficult to access libumltiprocess files
- Current workaround: Copying files into git repository

## Requested Improvements

- Add CMake install directory with #include directory
- Include header files in standard location for easier integration
- Make schema files available via standard include paths

### Compatibility Note

- Bitcoin Core 29.x and older: Don’t work with latest versions of
  libmultiprocess
- Resolution: libmultiprocess now has version tags to make it easier to document
  compatibility
