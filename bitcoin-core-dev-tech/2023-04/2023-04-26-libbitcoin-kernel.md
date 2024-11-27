---
title: Libbitcoin kernel
tags:
  - bitcoin-core
  - build-system
date: 2023-04-26
aliases:
  - /bitcoin-core-dev-tech/2023-04-26-libbitcoin-kernel/
speakers:
  - thecharlatan
---
## Questions and Answers

Q: bitcoind and bitcoin-qt linked against kernel the libary in the future?

- presenter: yes, that is a / the goal

Q: Have you looked at an electrum implementation using libbitcoinkernel?

- audience: yes, would be good to have something like this!
- audience: Also could do the long proposed address index with that?
- audience: not only address index, other indexes too.

Q: Other use-cases:

- audience: be able to run stuff on iOS

Q: Should the mempool be in the kernel?

- presenter: there are some mempool files in the kernel
- audience: No, it should not be.
- audience: Why not? Should people implement their own?
- audience: it's policy, not consensus
- audience: maybe libbitcoinmempool..? also libs for addrman, p2p, ..?
- audience: what are we trying to achieve? avoid net-splits between different implementations?
- audience: include a default mempool impl but possibility to use own/custom mempool?
- audience: depends on what people need. Some want it. Maybe finish this project and then look from there.
- audience: do we want to maintain libmempool or other libs?
- audience: if we use it ourselves it shouln't be a problem
- audience: will help with repo seperation in the future if we have multiple libs
- audience: yes, will help maintenance tremendously. Kill the monolith. people can build on libs and don't need to pollute the `bitcoin` repo.
- audience: bitcoin (Core) needs this in the long run
- audience: allows moving e.g. RPCs into many smaller tools that access a running kernel lib
- audience: will more/multiple libs get less review? Not really, maybe.

Q: Presenter: Feedback on approach to building smaller PoC in private to find out what the API can look like?

- (no responses)

Q: Many places that call shutdown. Errors should bubble up with "this function called shutdown".

- audience: To do this, we'd have to change a lot of code - huge diff.
- audience: we can use a scripted-diff which makes review easier.
- audience: alternative is catching exceptions: e.g. UTXO set corrupt, disk is full
- audience: the lib user should make these decisions. seems terrible to review all the code.
