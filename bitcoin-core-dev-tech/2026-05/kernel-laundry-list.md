---
title: Kernel Laundry List
tags:
  - bitcoin-core
  - kernel
date: 2026-05-07
---

Laundry list: https://gist.github.com/sedited/b69197582527749e467a81435f81297d

There are ~10 things that sedited has been working on, in various states
of completion, that should be done and fixed for the library. They're
spread over various domains, not necessarily related to each other.

## Link kernel library with common library

Would be nice to be able to link utility binaries to kernel library, and
then use API headers to dogfood them. Problematic: translations. At the
moment, we can't use library internally because of `G_TRANSLATION_FUN`.
It's currently statically defined because it does all the translation
fillings at compile-time, if translation function is available.

How can a compile-time expression access a global variable? Actually, it
doesn't access the global variable, but we need to have it defined.

One question is: should there be translations in the kernel. A more
fundamental question is: should there be _strings_ in the kernel?
Generally, we'd prefer not - there is a branch that removes translation
strings, turns them into normal strings. We currently have normal
strings in the kernel, e.g. for logging.

Feels like a gigantic task.

Does the kernel need to do translations? No, but the problem is that
the source (i.e. kernel) needs to indicate that a string can be
surfaced to the user, i.e. it needs to be annotated. Kernel does not
directly translate anything, just annotates them. In theory, gui could
intercept strings at runtime to translate/map them, but if there's no
compile-time map of strings, that makes having translations pretty
impractical. Note: we're dealing with error messages (often containing
context).

## Return fatal error codes

First - why don't we want strings in the kernel API? A string-based
interface is very brittle, and you're dealing with heap allocation.

The problem is two-fold: returning strings upon error is not a good
pattern for the API. We also have some fatal errors that we don't
properly propagate as a return type. E.g. in `ActivateBestChain()`, we
have one callstack where we flush, and if something happens during
flushing, we just carry on and pretend everything is fine. That's
obviously bad if you consume the API, because then the return value
becomes meaningless. User now has to inspect e.g. context state.

sedited's approach (#29642) uses a clang-tidy plugin that enforces that
any error is properly bubbled upwards. ryanofsky didn't like that approach,
he (#29700) also bubbles up error but retains error strings, as context
is important.

We're also kind of phasing out our own bitcoin-clang-tidy, so
all-in-all, #29642 is probably kind of dead.

What does bubbling up mean? It means recursively passed up in the
callstack.

Would using exceptions be an approach here? People are cagey about
using exceptions in Bitcoin Core. One attendee pointed out Bitcoin Core
might be the prime example of a project that should be using exceptions.
We're not doing anything near real-time. So maybe using exceptions would
be a good approach to consider for anyone who's keen to open a new PR
here. Note: we need to properly define what constitutes errors, i.e.
finding an invalid block is NOT an error, but e.g. disk failure is.

## Compatibility with bare metal systems

https://github.com/bitcoin/bitcoin/pull/31425

We recently had a changed that introduced a new allocated for our AES
module in crypto library, and that required hacking around (removed it
from build system) in #31425.

## Internal kernel library

https://github.com/bitcoin/bitcoin/pull/28690

Using internal library to inform which sources we use in the external
library. Old PR, it's stalled again. We can't seem to decide on how to
do the exact split between them. It mostly seems like bikeshedding, but
it looks like we're close. Hopefully we get more review soon.

## CheckedBlock type

https://github.com/sedited/bitcoin/tree/check_block_cbc

A new type for a block that has ran through the CheckBlock function,
which could have prevented some of the bugs on PR #32317.

In a C API, that would require memory allocation, and maybe even
completely requiring the block. So there, it probably might make most
sense to always (by default) CheckBlock, and only for the cases that
need it, expose a separate UnChecked type.

How did you want to deal with the various types of checking (i.e.
flags)? Not sure yet. Probably the most elegant solution would be to
reduce/remove the flags.

Perhaps in C API we should have one type, and then in language bindings
have multiple types. Because in some other languages, the cast can be
done without overhead, whereas in C it requires a copy.

## Abstract reader/writer classes for block file storage

https://github.com/sedited/bitcoin/tree/blockstoreReaderWriter

Allows you to run a node completely in-memory, no needs for tempfs or
anything like that. This could be useful for fuzz. Anyone keen to take
this on?

## Remove the bidirectional relationship between chainman and chainstate

https://github.com/sedited/bitcoin/tree/chainmansplit

A lot of time spent on this branch already, and probably about 3/4 of
the way there. Could be done incrementally. Anyone keen to pick this up?

Main blockers: `IsInitialBlockDownload()` and `ReculculateCacheSizes()`
are making this very complicated, because they need to be aware of the
other chainstates. They're not used very much, so maybe we can just
work around them.

Once this is done, we're very close to making assumeutxo a client of
kernel interface, and chucking it out of the interface completely.

Ideally, we would then have net_processing call the chainstatemanager
class, that then calls the chainstate. ChainstateManager class then
moved to its own module in node.

Keeping this PR rebased is tough.

## Fix cs_LastBlockFile to become non-recursive and add proper annotations

https://github.com/sedited/bitcoin/tree/last_blockfile_mutex

We have this weird recursive mutex in blockman that protects the last
block file that we've previously written to. it lacks annotations in
the correct places, it doesn't lock every time we actually should be
locking, so it's buggy, and it's a recursive mutex so we can't reason
about it at all.

All of that is fixed in the branch, but ran into some problem where
unsure if there was some interaction between `cs_main` and
`cs_LastBlockFile`, and couldn't figure out how to deal with that yet.

Reason why tis one is interesting is because it protects when we write,
and it's basically one step to make our writing of steps parallelizable.
E.g. with SwiftSync, with this change, you can write blocks in parallel,
which will be a pretty big boost.

## Remove the mempool from the kernel library

https://github.com/sedited/bitcoin/tree/mempoolout_interface

This branch does everything to split the mempool. It works. There are 2
problem areas:

1. need to take a lock for the mempool when doing reorgs, because we
   need to take stuff out of mempool - and then once done, put stuff you
   previously remved back in. During that time, mempool must be locked
   to avoid another peer process affecting a transaction, updates
   coinsviewcache
   - solved with "ugly" `ChainstateUpdateGuard` object
   - can we use "TxGraph" staging to solve this? but we're not just
     updating the mempool items, also the mempool coinsviewcache.
     - `MaybeUpdateMempoolForReorg` uses cache too. But we can still
       just lock cs_main
     - Do we actually hit the mempool during a reorg? No (only at the
       beginning and end), but the issue is that we shouldn't be reading
       any of the stale stuff during reorg (we still issue
       notifications), and that might trigger reads from the mempool
       stage - and that might be protected.
2. kernel needs to surface the scriptcache for the mempool validation.
   that's a bit ugly, because if you split the two, you'd expect script
   cache to be internal to the kernel (exposing it is dangerous), but
   when splitting it up the cache would have to become public.
   - one alternative is to create a second mini coins cache. We
     validate twice: once with the policy rules, and that validation
     step doesn't mutate script cache, because we don't want to insert
     a cache hit against the policy rules.

Would be nice to carve out a separate file (e.g.
`mempool_validation.cpp`) to clean up the big `validation.cpp`.
