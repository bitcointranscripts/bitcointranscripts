---
title: Static Builds
tags:
  - bitcoin-core
  - build-system
date: 2026-05-05
---

- Fully static builds for Bitcoin Core are very desirable
  - Pruning dependencies and runtime libraries
  - Down to `libc` and similar
  - Switch to statically compiled `libc` has a small drawback
  - static compilation is broken and they don't seem to care about
    fixing it
  - `libc` will try to DL open
  - Latest version of `libc` is built in guix
  - `std::sort` vs `qsort`, the C++ one is template derived anyway
  - Switch to static build is able to run on Ubuntu 12
  - What is stopping us from doing this?
    - Linux-only with a subset of architectures
    - No GUI because of runtime load of fonts, etc
    - Split release builds into two for GUI and non-GUI
      - How do we want to split the scripts up
    - GUI won't get the benefits of a fully static build
  - Could be possible to bundle QT such that it can be built statically
    and still interact with OS
  - GUI is not a blocker for static `bitcoind` and utilities
  - Static Bitcoin Core with GUI that depends on OS (multiprocess vision)
  - `libevent` removal then fully static Bitcoin is nearly there
