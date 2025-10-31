---
title: Fuzzamoto
tags:
  - bitcoin-core
  - fuzz-testing
date: 2025-10-21
---

See also:
https://docs.google.com/presentation/d/1wR7ln1Seoonf--ocZVIUgihVFj5EEx7JJ3g_6ZdzVa4/edit?usp=sharing 

## Basics

https://github.com/dergoegge/fuzzamoto

More detailed docs: https://dergoegge.github.io/fuzzamoto/

- Fuzzing but at the same level as the functional tests, i.e. testing happens
  through rpc/p2p/ipc
- Full system snapshot fuzzing

Workflow:

1. start the test
2. spawn one/multiple bitcoinds and generate state
3. create snapshot
4. for each fuzzing iterations the state resets to the snapshot

The snapshots are important for determinism.

The fuzzamoto approach can find crashes, hangs, consensus bugs, ... Pretty much
any of the properties we care about. False positive rate is similar to
functional test suite, i.e. crashes most likely indicate real issues (whereas
fuzzing failures often indicate fuzzing harness bugs rather than logic bugs)

Harness runs inside virtual machine and iterfaces with bitcoind. Harness
receives inputs from fuzzer. Fuzzer is driven by AFL++, or one test is using
libAFL.

## Scenarios

- "Harness" is similar to a functional test
- Each scenario:
  - setups up some initial state (i.e. snapshot state)
  - defines a test execution function that is given some input bytes

Example scenarios already implemented:

- compact block relay
- testing the HTTP server
- RPC interface, tests the whole interface

## Custom LibAFL fuzzer

- Custom designed for fuzzing processing of sequences of messages
- Uses intermediate representation for test cases
- Contains structural and type information

For P2P messages, dergoegge implemented his own fuzzer because p2p messages are
very structured: serialized using a custom format, contain many cryptographic
primitives and many other requirements (e.g. block header must point to prior
block via its hash). This tool intelligently creates and mutates those messages.
The mutator doesn't operate on the raw bytes of the messages themselves, but has
Intermediate Representation of the messages that represent programs/instructions
that create the messages.

## Bugs found so far

- Wallet loading crashes
- IPC uncaught exceptions
- Blockindex check assertion failure
- (PR) Erlay message deser assertion failure
- A couple of yet undisclosed ones

## How you can use Fuzzamoto

- Run fuzzamoto-libafl on your own changes or PRs
  - Modify the state setup: you can get pretty creative with this (e.g. adding
    complex mempool state)
  - Modify the Intermediate Representation
- Write your own scenarios
  - e.g. maflcko wrote one for IPC fuzzing
  - Currently only possible in Rust but python would be possible if there is
    demand
    - Python particularly could be nice because we can reuse (parts of) the
      functional test suite
- Fuzz other projects
  - dns seeders, ...
- Caveat: you need a bare metal x86 machine (amd or intel)

Which ones can you translate to a functional test? Manually, for pretty much
anything, but automatically you can also do that using the Intermediate
Representation, or some hybrid to generate most of the test automatically and
then tweak it manually.

Should fuzzamoto be added to our CI system? Currently it's only ran on master,
or manually on PRs that look interesting. Adding running all the existing inputs
(cfr what we do with fuzzing) could be helpful on all PRs, but still too early
stage for that - we'd also need to self-host. 

To reproduce a bug: you can run the test cases without the fancy VM / all kinds
of special features (but it's much slower).

Why is the custom libAFL dergoegge wrote better at finding interesting cases
than the structured fuzzing example? He noticed that there was a lot of overlap
between different scenarios that he wanted to write (e.g. producing
transactions), so building a generic more global approach made it easier to
reuse logic across tests.

## Future work

- Extensions to the Intermediate Representation
  - E.g. add compact block logic
  - Should soon be complete to completely cover the protocol
  - More help coming in from Brink interns starting in November
- Achieving 100% determinism
  - Custom hypervisor inspired by https://antithesis.com, they have good
    documentation and blog posts
  - Building our own Bitcoin Core specific hypervisor might be feasible, but
    more research necessary
- Advanced bug oracles
  - e.g. differential testing against btcd, libbitcoin, old core versions
  - Things like checking for inflation, index sync oracle (do all indexes
    eventually catch up), ...
- Feedback other than coverage (state space exploration)
- Incremental snapshots
- Benchmark, Performance, Debug tooling (functional test converter)
  - Performance: performance initially quite good (on 32 core machine: start at
    ~2000 iterations per second, and a week later drops to 400, as more
    interesting inputs are found more complex interesting scenarios are executed
    that take more time).

At the core of all known determinism is the hardware that the software runs on.
For example, time and random number generators. VM's OS is also not
deterministic. To solve that, you need a layer between hardware and software
you're running, e.g. the custom hypervisor. If the exact same input doesn't lead
to the same code coverage every time, more and more inputs are added to the
corpus without adding actual coverage.

For differential fuzzing, this custom hypervisor is quite essential, because
most of the other implementations don't have mocktime implemented.

Two types of assertions: 1) invariants that should always hold, and 2)
"sometimes, this state should be reached" (*"Sometimes Assertions"*)

Incremental snapshots allow to increasingly advance the state to interesting
ones, and quickly building from there. You explore the state of your program
more thoroughly this way. Antithesis has this functionality already.

Is it possible to reduce memory usage? Currently using 32gig, which was
surprising, because the snapshot (i.e. the VM, 4gig) should exist in memory only
once. Further investi

Could IR be upstream to bitcoin/bitcoin? In theory, fuzz tests could accept IR
inputs, but a couple of issues because it doesn't have the VM it'd be
non-deterministic and quite slow.

When a new input is found, it is minimized, i.e. reduced/simplified as much as
possible while still hitting the same branch.

How can we test our PR with fuzzamoto? See the Dockerfiles in
https://github.com/dergoegge/fuzzamoto, they produce an instrumented bitcoind
that can be pointed to a PR. Running fuzzamoto makes most sense on PRs that
change a lot. For specific/narrow PRs, this might not be very efficient (takes a
long time to find bugs). Instead of instrumenting everything, can also
specifically instrument files of interest using the `ENV AFL_LLVM_DENYIST` or
`AFL_LLVM_ALLOWLIST` vars.

## Action items

- **Call to action:** people to start using fuzzamoto so dergoegge doesn't have
  to do it himself.
