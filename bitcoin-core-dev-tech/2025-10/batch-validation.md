---
title: Batch Validation
tags:
  - bitcoin-core
  - batch-validation
date: 2025-10-21
---

- Batch Verification was already specified in BIP340 (Schnorr):
  https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki#batch-verification
- There is a PR open on libsecp256k1 that adds a new module:
  https://github.com/bitcoin-core/secp256k1/pull/1134
- The PR has gone through a few iterations already, but needs more review
- A few more comments have come in recently, hopefully the PR review can pick up
  momentum
- Pippenger support not added yet
- Interface still likely to change somewhat
- Draft PR in Core has went through some iterations as well:
  https://github.com/bitcoin/bitcoin/pull/29491
- Block validation performance now close to what would be expected (without
  Pippenger)
- Old benchmarks and graphics in the PR were confusing to people, there should
  be full benchmarks and new graphics added to make clear what the latest state
  is
- PR currently not rebased frequently due to anticipated changes to the secp
  implementation
- Discussion if we need to have a special way to deploy this (ability to turn
  the feature off, build without it etc.)
- If some combination of signatures show up that verify correctly together but
  not individually then this would fork the chain
- We should either be confident that this is secure and make it the default or
  we should not do it at all, so likely no special way to deploy it
- Changes to checkqueue are not ideal yet, potential for refactoring checkqueue
  first
- Discussion about lock freedom that keeps coming up, likely limited minor
  performance upside from this though, prior attempts failed because of this
- Potential focus on simplifying the code without much performance impact, that
  could be a win as well
- On Core PR: Open to review and approach feedback to changes in checkqueue,
  scriptcache and validation
- Wrapper object on secp functions (`BatchVerifier`) should make impact on the
  rest of the changes small if secp interface changes
