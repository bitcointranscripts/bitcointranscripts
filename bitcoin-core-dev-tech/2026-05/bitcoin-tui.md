---
title: Bitcoin TUI
tags:
  - bitcoin-core
  - tools
date: 2026-05-07
---

## Bitcoin-tui demo

### Intro

The Bitcoin-tui is a small terminal UI for a Bitcoin node, written in C++, based
on the FTXUI framework. There was a small (limited) demo of the current
capabilities of the tui, that showed the dashboard, the mempool explorer
(including recent blocks), peers dashboard and the tools tab which also contains
a tool to broadcast a (raw) transaction.

### basic demo

There where some question if the transaction visualizations where already on the
level of mempool.space (with all the arrows) and if this could be achieved with
a TUI. Currently the visualization of the transaction is somewhat limited but it
should be possible to create the same style in the TUI, given that FTXUI
supports a Canvas object. But could limited to terminal support.  

### Lua Tabs demo

In the yet to be released version there is support for Lua scripting "tabs",
users can write custom tabs for their own ideas and visualizations. One of these
Lua Tabs is a view only wallet function, which was demoed and the new QR code
visual was also shown. Lua is also very suitable for users who use LLM's to
create  their own visualizations.

### direction of project

There was a short discussion of the direction of the project, where was
indicated that the current C++ tabs will be re-written to LUA versions. The UI
elements will be made available to the LUA scripting side via build in
Components.

The interaction with the node is currently via RPC, which also give the ability
to use bitcoin cores ability of allowlisting RPC commands. On the question if
there where plans to extend the connectivity to IPC, there is no objection to
that but also no direct plans.

The next release of the TUI will be soon, the wait is also for the next release
of FTXUI. FTXUI has indicated to work towards a new release soon, which is
better documented and has increased stability.
