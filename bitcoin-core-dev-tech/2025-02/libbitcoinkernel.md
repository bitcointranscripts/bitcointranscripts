---
title: Libbitcoinkernel - outstanding questions
tags:
  - bitcoin-core
  - libbitcoinkernel
date: 2025-02-27
---

## `BlockManager`, `Chainstate`, `ChainstateManager`

`Chainstate` keeps their own `CChain` class for keeping track of their chain of
blocks, which is basically just BlockIndex entries, and manages the UTXO set.

`ChainstateManager` is there to orchestrate interactions between `BlockManager`
and `Chainstate` and facilitate AssumeUTXO's multiple chainstates.

Currently, only `ChainstateManager` is exposed in kernel API. Should we instead
expose structures that allows users to implement AssumeUTXO functionality by
themselves? We could expose a `Chainstate` and `Blockmanager` to facilitate
that.

Question:
> What is the benefit of implementing your own assumeutxo instead of using what
> we now have in ChainstateManager?

-> It feels like a bit of a layer violation.

Separating and exposing the `BlockManager` and `Chainstate` structs separately
is going to be a lot more work and delay the kernel API. Part of the difficulty
comes from pruning functionality, which we also could not include in the kernel
initially and then expose as an API feature later on.

## Parallel block reading

Kernel library cannot currently read blocks while bitcoind is running, because
LevelDB can only be used by a single process.

Currently, we load the blocktree in the blockmap at startup, and we only write
to it when we flush, which happens only every now and then. One approach that
would be very hacky is opening/closing the database before every operation, but
this can pose problems with flushing. LevelDB also has a snapshot feature, but
that doesn't seem to help us either - looked at it earlier, but we may have
missed something.

Blocktreedb is an append-only structure, we never delete anything. So maybe
using a key-value store for a structure this simple is a bit overkill? We could
switch to a flat-file structure that any process can access? But that would
still even get us only halfway there, because bitcoind is only flushing every
couple of hours, ... But, there also shouldn't be a reason why bitcoind can't
start flushing more often (outside of IBD). LevelDB writes async, so we could be
flushing in background thread with zero overhead.

Question:
> Is there a historical reason why blocktree isn't stored as a flat-file anyway?

-> No idea

## Directory locks

If kernel and bitcoind both run on the same blockdirectory, you want to present
the user with a nice indication that another process is already using the
directory. But taking the lock can raise a whole range of errors (e.g.
filesystem errors, permissions, multiple bitcoin processes), so how do we
distinguish between them?

In #31860, the blocksdir lock is acquired by BlockManager RAII-style. Because we
have to instantiate it and pass it to another function, we must ensure that the
user can only pass it once.

Instead of directory locks, it might be better to take file locks. This is more
flexible, but it also can make surfacing errors more difficult: on init, do we
then need to iterate over all the files to check that we're able to access them?
Or do we switch to a model where processes only lock files for the minimum
amount of time needed to read/write the file, or a portion of it. But we also
still need to make sure that e.g. no 2 bitcoind instances are running on the
same directory, so we'll end up needing a directory-level application lock (as
is currently the case) in addition to the file-level locks.

## Block headers

One of the key things left out of the current API is handling block headers.
Should we expand the scope of the initial API and add it in? It seems to be
requested by potential users, but it would add another ~2,000 LoC to the PR. It
would allow node implementations to do headers pre-sync, and avoid required
third-party libraries to parse the block header.

Where do we draw the boundary wrt inspecting kernel structs? Especially once we
have exposed transaction logic, the goal would be to increase visibility into
headers, blocks, ... to avoid relying on third-party libraries for structs that
we expect to not change too often.

Conclusion seems to be that: because there are no conflicts, it can easily be
added in later, so there is no point increasin the PR size now.

## Ideas

Maybe a lot of the current C API code can be automatically generated (e.g.
through SWIG) by annotating existing code. There were also concerns raised about
the C API PR remaining unmerged for too long, just growing endlessly until it
gets too big for non-WG contributors to review it.

Signal seems to autogenerate a huge C library, perhaps that's relevant to us?
https://github.com/signalapp/libsignal/blob/main/swift/Sources/SignalFfi/signal_ffi.h

## Shipping

What is the view for shipping kernel? Not sure yet, perhaps the first version
could get merged before v30, but whether or not we'll ship the compiled library
and header remains TBD.

A lot of the conversation at the end revolved around a pragmatic way forward to
make progress. Specifically splitting the BlockManager and Chainstate would
involve significant changes to validation, and probably take years to get
merged, but could offer a much better interface. Do we try to get the current
iteration merged already, and iterate to the desired/target API? What does the
target API look like, and which issues does it solve (e.g. allow clients to
build AssumeUTXO)?

Consensus seemed to fall on merging ~the current API, and make progress from
there. Once it's in master, the barrier for people to consume the API and build
applications for it (and from there, inform us which functionality they'd need)
seems like a good way to make progress.
