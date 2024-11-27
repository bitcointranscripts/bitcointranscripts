---
title: Kernel
tags:
  - bitcoin-core
  - build-system
date: 2024-10-15
additional_resources:
  - title: 'Block-linearizer branch'
    url: https://github.com/TheCharlatan/bitcoin/tree/kernelLinearize
---
## STATUS

Two recent Kernel workshops on what an API would look like and to polish the API. Also consideration on how Kernel would interplay with multiprocess

- External C header API PR opened #30595
  - Script validation
  - Logging
  - Block validation
  - Reading block and undo data

Initial scope to these few things. Yet powerful.

Tx processing, header processing, coinsdb on a separate branch. Not a big addition to add that in eventually

- Example applications using it coded up
  - block-linearizer
  - bitcoin-chainstate replacement
- Working on polishing internals
  - More ergonomic for future versions of the API

## RUST-BITCOINKERNEL 

- Unit and fuzz tests helped expose a crash bug also present in the old libbitcoinconsensus interface

Separate fuzzing interface convenient and easier to iterate on

- Crate has been used for an example indexer and silent payment scanner

Josie helped with silent payment scanner

- He is also working on a tx indexer to read block data from disc and build index from that
- Also electrs integration replacing RPC calls, much faster

## API LIMITATIONS

- No concurrent reads of a bitcoin data directory
- Accessing subclasses is annoying with C functions opaque pointers
- No distinguishing in the logs between multiple instances of the same data structure

Replacing leveldb with something that allows parallel read-only access would be useful, replacing the parsing of block dat files

Concerns discussed about ensuring database consistency, especially during reorganizations

Cant have separate bitcoind process and kernel reading same data

## DOGFOODING

- How can the API be re-used by our Project?
- Utilities using the kernel, .e.g. block-linearizer, reindexing tool, data dump tools
- Maybe re-use it in the RPCs, or one of the interfaces?

Big question today: how to dogfood this API?

- Initial idea was small utilities exercising parts of it. Its “kind of ok”, grasping at straws. Also need to maintain these utilities, increased maintenance burden.

RPC calls

- He did this for a few, but it's a bit complicated. Wrapping and upwrapping C/C++ types.
- Might not have a good way to dogfood the API within the project
  - But perhaps de-duplicate business logic across ZMQ, RPC, multiprocess, kernel
    - Consolidate that logic within the multiprocess interfaces

This is a c++ project, just have a c++ library?
1:1 c:c++ headers

## Misc Discussion

Block-linearizer, was it faster? Yes, faster, and also simpler.
See: https://github.com/TheCharlatan/bitcoin/tree/kernelLinearize 
It is using c++ wrapper around c api

Dont think its a good idea to expose everything in the kernel library externally. Example of soft forks causing issues.
