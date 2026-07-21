---
title: Kernel Session
tags:
  - bitcoin-core
  - kernel
date: 2026-05-08
---

no pres, just discussion over direction of kernel / scope

one of the overall architectural problems is the idea of having kernel
library that doesn't use any system resources, vs kernel library which
for example, has one entry block called ProcessBlock / ProcessTransaction.
tend towards one functional interface, pure functions; but we're far from
that, unsure if we can get there.
it would certainly have advantages.
have PR open that does parts of it.
difficult thing is all the threads we have / threading model.
kernel should just say "this is a valid block" , but to do that we have
a threading model.
could offer a default where expose all knobs you configure, but here's a
default way.
historical issue: incremental optimizations to how we do validation etc
beyond that, extra caching, scriptcheck threads, optimizations 7/8 years
ago on selection for checking (?)
all introduce some form of technical debt.
open PR mutates coinCV from doing validation.
you're responsible for the threading model, problem is its a mix of
stuff that is pure vs stuff that needs to be handled.
removing recursive mutexes in BlockTree or BlockManager, probably an
easy win.
two fields need sync, both recursive mutexes, possible but needs
thinking. Concept NACK / impl NACK ?
status of one file per block ?
unrelated, it might be useful,
a sans-IO kernel would be useful. People can see how useful for things
like Utreexo.
what's the limiation for the validation function itself? where spent
coins are passed as input.
is that sufficient, or what is reason why validation can't be a pure
function?
bc Script verifier threads ; mutating UTXO set ; it spawns threads.
to do validation in parallel.
anytime something is spent, script caches can go away? not really.
tx objects live everywhere.
responsibilities are not cleanly separated.
really annoying thing is , "just put a kernel function in the correct
place", we still hit the mutexes, so you can't use it for validation
performance,
and suddenly that kernel API endpoint bc that deviates from our impl.
Horrible.
what's the alternative? implement validation from scratch?
use the kernel, but some primitives but not the whole thing.
if we provide a library, but not used by Core, its doomed. we must use
that lib.
what's the goal/approach? more effort into refactoring?
incremental refactors seem to be failing?
blocker is hard to review.
need a plan for the flow, code changes, etc
north star hack job implementation might be useful
currently have an impl and API for that impl, but would prefer spec that
says what impl should do.
gives us freedom to make changes internally without breaking clients.
mempool in kernel? nope
if i'm making a new node, i def want to use the kernel.
should have a libmempool, would be nice to have this as a library.
how would you describe "a mempool" ? transaction cache?
does the kernel have tests? yes
time as argument instead of syscall

example of use of mempool as lib: braidpool wants to apply policy as if
they were consensus rules for their DAG

in the beginning, consensus library. should we have a "libvalidation",
that's pure and doesn't do IO ?

needs an abstraction for talking to UTXO set.
validation only works on a UTXO set (??)
validation in two ways: get original scriptPubKeys, ...

different ways to validate blocks, but all of them need inputs
(libbitcoin, utreexo, core)
what is the fundamental unit of validation? tx, input?
that would be the value of a libvalidation,
maybe we only give the super low level stuff, no threading I/O etc...
Different plan / direction
force users to validate per block or not etc

libvalidation would be used
implementing those functions without CBlock / CIndex etc
need abstraction for chain? ideally don't need one
an input and tx no, but tx yes needs a chain
first step would be validating a tx, without passing in the chain
a library that does this would be a good start.
what info is needed form the chain? does it need things that are NOT
part of the chain?
we could pass an abstraction of a chain?
validation per block, then tx can refer to tx within block,
but don't need headers
if you're validating a tx, you just need a previous transaction
interesting to see other models like libbitcoin

apart from difficulty, do you see anything that would prevent this path?
anything that involves caches. ScriptCache/ CCache.
no point in making them global, they're unique per tx.
FCheck?

we would like to be able to validate a tx without the CTx context
scary to touch this code :)

need better documentation so people don't have to recall this from mind.
