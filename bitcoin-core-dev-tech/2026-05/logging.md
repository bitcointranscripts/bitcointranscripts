---
title: Logging
tags:
  - bitcoin-core
  - logging
date: 2026-05-06
---

logging interface
do we have a vision for logging?
diff opinions, diff priorities are good;
structured logging: #34374

- kernel loggin takes a string: all users have to implement string
  parsing to use it. instead of a string, use a struct.
- x wants log parseable as json.
- takes the kernel C API logging and cleans it up -- way nicer.
- structured logging uncontroversial

if kernel doesn't rely on logging, then it shouldn't drive logging
design

why do we need filtering at all in kernel?

- need it in code, and code goes in kernel; if we do filtering
  efficiently, we can't have callbacks for all the stuff.

the atomics would go into util log, and the kernel exposes the thing
that sets all the bits

kernel won't need much more, net however...

Context aware logging

not in favor of creating a custom logger with wallet as parameter
instead function that takes wallet as param

consolidate PRs, review them

logging categories:

- log source locations, automatic
- debug.log, some things have brackets some don't, would be annoying
