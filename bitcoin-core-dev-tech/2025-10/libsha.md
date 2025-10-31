---
title: libsha
tags:
  - bitcoin-core
date: 2025-10-21
---

## context

* sha256 = just implementation details when we first started libsecp (RFC 6979
  needed it)
  * RFC 6979 = deliberately super conservatively designed spec - order of
    magnitude slower.
  * non-trivial = now matters since we optimised other stuff
* we don’t use it with schnorr (BIP340 = our standards = more performant)
* we could have done our own standard for ECDSA
* don’t bring complexity of hardware detection - let’s not expose it - it’s not
  intended to be good implementation - just an internal dependency we need it
* uses of sha = tagged hash, ecdh, musig, batch validation
* legacy sig - SIGHASH_SINGLE , input index without corresponding output - you
  sign message hash 1 (not message 1) - given by satoshi - designed like that
  maybe not a good design
  * ECDSA is completely broken if message is not hashed
  * implementation is unsafe if we don’t hash message

## options

1. initial idea = caller bring own implementation = work for core + might work
   for hardware wallets which bring their own embedded code. not useful for
   software wallets.
    1. caller brings init, transform, finalise
    2. for a static library, can you bring it at compile time? (could benchmark,
       embedded device might need static build)
    3. Would we ever change sha256? insecure + broken only then we would.
    4. batch validation - faster PRNG (we don’t need a hash function per say)
2. have a library where we extract bitcoin core hashing algo

Why is 2 better than 1? easier for some customers of the library.

    3. do both

    1. optional dependency
    2. more config testing + small runtime overhead (negligible compared to entire hash)

    4. copy-paste code from core to secp.

we have linking anyways - we could just link in library + make it

What's the scope? just sha or other hash primitives? or other stuff? chacha too.
maybe later.

scenario 1:

libhash is required dependency of secp25621

* should run + test it in all platforms where we run secp256k1
* architecture specific code - what extensions your CPU has (might not be
  terrible to have in secp256k1 either - separate discussion)
* feels ugly - partially intended to be usable for bitcoin specific applications
  depending on the library used for bitcoin specific applications. secp256k1 is
  a general purpose library. if we’re just doing sha256, it’s ok. if we bring
  everything else - doesn't make sense.
  * BIP32 module - needs sha512
  * merkle tree optimisations
* core side - not much upside. get a new subtree. benchmarking framework for
  repo. add another hash function. 2 projects which require different compiler
  requirements. own build-system + people update it. Our CI is broken because
  someone added something we don’t.
  * crypto code doesn’t rot. more one-shot work than others.
  * cmake it twice?

is it just sha2? rimpemd? sip hash? murmur3?

narrow scope to just sha256

sha256 (pure sha256, leave merkle tree stuff in bitcoin core?)

* parallel merle double sha256 or just sha256?
* makes the library limited in scope.

if it’s just pure sha256 + modern arch/fast - shouldn’t we expose it? copying
just pure sha256 (not merkle tree specific) - putting it in libsecp +
transliterate to C + run benchmarks.

* should core just ignore copy in secp? inconsistency.

so many options.

copy-pasting won’t hurt. add an API. before copying, we need CPU detection.

we can copy + arch optimisation + expose.

* no separate library maintenance.
* translating c++ → c is just line by line, class → struct
* bitcoin core prolly won’t use it.
* 99% effort is CI + libsecp stuff
  * hard part is testing on all architectures + core does good job
* Is the maintenance burden something we want to take on?

20% of CPU time in ECDSA is hashing.

motivation = performance (1% schnorr verification + 20% ecdsa performance)

## conclusion

* provide different nonce function for ecdsa in libsecp itself
* better compatibility for hardware wallet - don’t remove it.
* set_context_hash_function in self tests for people who want to bring their own
  sha256
* sign_fast function in libsecp for ECDSA
* one shot + streaming API options for hash

    1. internally libsecp = streaming API
    2. TaggedHash = initial state
* we have our own sha256 - use a particular way of representing state - maybe
  different from how libsecp sha256 uses to represent state.
    1. least efficient - sha256_allocate_state + deallocate_state which such
    2. put an upper limit - 128 bytes. - that’s enough - pointer to 128 bytes
    3. we move the layer of abstraction slightly, no initialise + update+
       finalise. there’s only sha256 transfers: 64 bytes → 32 bytes. all you
       need to bring is a transform function.
        1. you lose performance improvement
        2. you get an array of 8-32 bit integer. you need to bring transform
           function.
            1. compatible with all implementations. may not be compatible with
               hardware wallets.
            2. How much can we guarantee alignment? for 32 bit integer. C
               standard can guarantee. same trick for scratch space.
