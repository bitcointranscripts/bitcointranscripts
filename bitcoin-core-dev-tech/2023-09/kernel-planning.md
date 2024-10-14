---
title: Kernel Planning
tags:
  - bitcoin-core
  - build-system
date: 2023-09-20
speakers:
  - thecharlatan
---
Undecided on where to take this next

Carl purposely didn't plan beyond what we have

Options:
Look for who the users currently are of kernel code and polish those interfaces. We'll end up with a bunch of trade-offs. And I don't see us piecemeal extracting something that is useable to core and someone on the outside.

- The GUI much high level to be on this list. The GUI uses a node interface, it doesn't call an validation right now. It does use some of the data structures.
  - Feel like we've ruled out the GUI as a starting point.
  - what would the changes be?

- The tests (or some of them) - could slim down some of the test code. Init.cpp file that could be slimmed down. - Marco
  - where the kernel has picked up momentum is where it is useful already. It would be cool to encourage people to write tests with stripped down version of bitcoind and encourage those types of application tests. It is currently the kitchen sink and we test it that way.
  - port this functional test to kernel tests. Can look at existing tests that could be rewritten as kernel tests.
  - Bitcoin kernel should have all of its own test suite. Use bitcoinchainstate rather than bitcoind. Lots of different ways to tests - could create a bitcoinchainstate bin that we feed blocks, can do that in python just fine.
  - it is a win that doesn't run through the RPC interface.
  - would like to just run the validation tests and nothing else.
  - other util bins ported and if we add other utils they would also be a user of bitcoin kernel
- Net_processing
  - Started thinking of ways to slim down the amount of functions we have and that immediately impact net_processing.
  - What functions?
  - When we wanted to introduce handling for fatal errors, they end up bubbling up to net_processing - how to handle those in the net_processing loop which are unhandled right now - they are unhandled in the moment but it is handled when convenient
  - Disk corruption - handle those cases seems like the priority
  - What would the changes actually be if you started there?
  - I'm getting the feeling that chainstate and net_processing where intertwined. And refactoring that would be beneficial to the app. See what calls are happening and figuring out what makes sense. Detangle that particular layer (or at least document).
  - do we think the current code makes sense? Net_processing is using the validation interface. Sounds like this would be something that we would benefit from some exploration.
- Multiprocess if we work on it now and get those interfaces, it will help us deglobalize things we need to do for the kernel (I'm for that). The two have nothing to do with each other, but the kernel will benefit from the work there.
  - Putting a boundary between the node and wallet - it's a separate issue - standardize the node interface or at least came up with an interface. I see the parallels but I don't see the overlap.
  - What would the code changes be? Not entirely clear.
- Working on new utils that are using the library
  - The linux philosophy - would be cool to give ppl composable tools to interact with bitcoin
  - Open an issue to brainstorm about utils or what tests could be useful
  - Move reindex and reindex_chainstate to utils (may even have a branch - cory)
    - Changes assumptions - eliminates state changes
    - In the GUI - we have the options to reindex when a problem is detected.
    - It does complicate shipping things to end users somewhat.
    - Removes the pressure where people add new utils with more dependencies to these “nonsense” tools
    - Maybe end up with 5 or 6 utils things - ship a bitcoind and other things (like CLI)
- Writing an alternative full node implementation for 6 months and propose an API based on what I had there
  - These two things happen completely in parallel
  - Imagine we are using bitcoin chainstate - none of those things matter internally. The goal of cleaning it up is only an external user goal.
  - Testing and writing utils can happen in parallel
  - on the fence. If I go that route, I will be focusing on different things. In conflict? No.
  - the only reason to clean up the API soon or quickly like exposing cBlock and cTransactions externally? I suspect we won't.
  - Disagree. I think we will.
- how would it look like without cBlock/cTX?
  - not important to figure out what is _THE API_, but what some decisions on how externally what we are going to hand out. We couldn't have done this 6 months ago. But now we are at the point of what functions we are going to expose.
  - cblock index should just be an opaque pointer. We can make this an experimental API and then we can make those decisions later. When we are writing these utils then we'll get a better feel and then we'll can make another abstraction. Backwards compatibility. Would this be in rust.
  - could we write some of these utils, you could do them in rust to introduce it to the codebase.
  - we could write an alternative implementation in
  - new rust linter - bash, python, rust, tidy - kernel will open up lots of pathways for experimentation. Dependencies and more.
  - we could optionally support rust code because they don't touch bitocind.
  - but if you were writing a test runner or fuzzing stuff that doesn't get shipped to the end user, go nuts.

## Mempool

Does it belong in or out?

- Some prefer to have some components of the mempool inside but maybe not the entirety
- And the interaction between blocks arriving and blocks being reorg'ed
- BOOST feels risky, I'd like to get rid of it.
- it'd be nice to have the kernel to just be code and not dependencies
- exposing BOOST was my complaint. Now I don't care now that it's gone. I think there are other interesting reasons that is now purely philosophical.
- We have to ensure that the mempool is actually optional.
- Presumably we could have an abstract mempool API and in another scenario you could define your own mempool.
- Mempool maintainer says "out!"
  - Why it belongs out: it's not consensus - mempool and policy on not consensus
  - Why in: it's useful to keep with consensus - bitcoin is more useful if everyone is participating in tx relay
    - Benefits to having homogenous mempool policy
    - The more you diverge the more cache misses you get in compact block
    - If this is the minimal set of things we imagine a full node having - then mempool is useful
- the mempool is an almost necessary for performance of block validation - a prevalidation cache is _actually_ what is required but it doesn't have to be a mempool. We could create a small abstract role for a pre-validation cache and it could be a mempool or something else if someone wanted something else. Does that make sense?
  - vextraTx, scriptCache, …
  - It doesn't have to be the data structure itself. If we were to generalize mempool to pre-validation cache it would make sense to have a plugin for it.
  - It has nothing to do with the mempool itself.
  - cluster mempool - maybe we could do it with the kernel rewrite - could do a custom mempool doing that and that might help with the infrastructure.
  - you could create a bin that implements it and then write tests against it.
  - parallel mempool - does it cover something like that?
  - if you have a cache and not just a mempool you could optimize it that way
  - imagining the interface - there are some easy things. I have this tx, have I already checked this sig before. Is this UTXO already loaded in my coinsviewcache, what would that look like if we had a separate pre-validation cache. An arg to keep it in is to keep it in is that it is easier
  - that'd all be in memory - but that sucks, it does need to do to disk
  - fee estimation - could move it in and then keep an eye on cutting it out
  - when you say exclude the fee estimator - the fee estimator is not in txmempool anymore?
  - there is a PR that pulls it out of txmempool. So it is possible.
  - are there any good reasons to keep it out except philosophical reasons. Is this something we need to get to with the kernel right away.
  - utils, test infrastructure, and other things we could write without the mempool.
  - if you are talking about other implementations
  - we might not want to encourage people to roll their own policies
  - There is a lot of WIP in mempool so there will be lots of rebasing to be done.
  - so it's staying in for now.
  - agreement that it doesn't belong there, but we aren't pulling it out yet. We can just introduce a pre-validation cache in the kernel. If you provide one, then the client can't screw it up.
  - the mempool is opinionated
  - Needs to be configurable if anything. There is a lot we could provide to make sure users don't f it up but then we just end up with bitcoind. Keep it in for now and figure it out as we go along.
  - would prefer that we not ship it with an mempool, but we are a long way of shipping something.
  - Ties into other decisions behind core policy and if they don't then we need infra to inject it back in

## AssumeValid

3 approaches:

1) Leave as is
2) Remove all of the Core specific behavior (hashes)
3) Remove the entire functionality
    - And pass our hashes back in

- Counts for checkpoints, assumevalid, minchainwork, and AsssumeUTXO as well.
  - AssumeUTXO - has the hash baked in and it doesn't have an option to change
  - We can just remove the checkpoints
  - Disk space, chain params we update for each release
  - levelDB, should the only option, google is kind of sun setting it
    - We could pull the upstream one more time
    - Marco is making patches in the CI for levelDB UB. Should bring in the patches into our subtree.
  - We need this in but we are deciding which layer they are in.

- Testnet, signet - no one has strong opinions.
  - Are there validation changes for signet specifically? Can we add that on top of kernel?

- Invalidate block - do we want to support in kernel
  - Usecase is testing or everyone decide that some blocks should be invalid for forking off
- For assumevalid, hard to do it safely where you might say don't validate signatures for this block which introduces the opportunity to screw it up
- Opinionated API vs configurable API
  - If you have configurability then the opinionated API is just for bitcoin core
- Would have to expose the configurability in any case
  - Also a question of how much infra you have available - how many options you make available - chainstateman, validation, etc

## Steps forward

Immediate

- bubbling up the fatal errors. Decide on an approach. Use userresult and populate it with warnings when we go through voidfunction. (need the latest PR to be merged first #25665 - adding warnings and return codes to functions that don't have them)
  - can always do this stuff without changing behavior
  - If we trigger or interrupt on the kernel level or whether let the caller take care of that.
  - The client handles their own control flow.
  - There might be a behavior change in there, there are some functions that check to see if there is an interrupt.
  - There is a branch - Currently we have a fatal error - this, fatal error, return error code and then the client triggers the interrupt. Give bitcoind its own util for that. But it could change behavior because we aren't interrupting them at that point in time.
  - This is the next plan for the next few months.
  - hope is that you don't get too bogged down in this with the tests and utils. Don't want this to be an endless PR.
  - these could be considered bug fixes
  - arguing against changing behavior. Not clear whether these cases are good or bad - flushsys call - that fails - does that mean you don't want to write more to disk when these flush calls happen. It's not clear to me that when an flush calls fails, we want to stop everything and shut down.
  - if the fsync or a flush call fails we assume a hardware failure and we the way we proceed is that we stop.
  - that might have been definitive but that not what I would choose. It is a good thing to do, but is that a priority? When we make changes, when you don't have to make a change then don't. It should just be a separate thing.
- play with reindex and reindex chainstate
- it would be good in general to open issues for what utils we should have and what tests would be useful to replicate
  - having a hard time coming up with the usecases
  - just a matter of looking at the tests and seeing what should be moved over

## Removal of kernel as an active project priority

Weeks from removing the kernel from the priority projects. All the patches, just need to get it through review. Once the next 3 get in, pull from priority.

- 2 biggish PRs - 1 is open, 1 is a draft but close
- Cory has medium PR for removing the endianness compatibility code from the headers
  - unsure about the approach taken
  - c++20 would be nice.
  - will probably have it by 27.0. Get span. Get rid of endiness. And other nice things. Solves some of these problems. Marco is interested writing more robust code using c++20. Did the build system changes and pulled out the detection.
  - will PR the endiness change and can merge after branch off.
- we are at the end of the first stage, next step would be to integrate it as an internal lib. The kernel becomes one of the static libraries - should we integrate it for bitcoind, bitcoin-QT
- Integrate it into the build system (trivial)
- it matters to me. I think it's a priority project. It makes things easier in the future even if it doesn't give us immediate rewards.
- made a lot of progress on initial abstraction - less concrete PRs - writing utils or experimentation - less focused review work - this will all continue regardless of whether it is on the priority list or not.
- Nice to have the regular check-in at the IRC meeting. For the next year or two - that there is forward progress.
- maybe we can talk about priority of reviews vs. weekly updates

Libbitcoind - would contain the kernel and that is what QT would use. QT would use some sort of library functions and that is an area of work.
