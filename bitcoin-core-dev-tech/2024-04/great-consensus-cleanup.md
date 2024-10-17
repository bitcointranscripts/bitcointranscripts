---
title: Great Consensus Cleanup
tags:
  - bitcoin-core
  - consensus-cleanup
date: 2024-04-08
---
How bad are the bugs?

How good are the mitigations?

Improvements to mitigations in the last 5 years?

Anything else to fix?

The talk is a summary of [https://delvingbitcoin.org/t/great-consensus-cleanup-revival/710](https://delvingbitcoin.org/t/great-consensus-cleanup-revival/710) .

## Time warp

- What is it?
    - Off by one in the retargeting period
    - 2015 blocks instead of 2016
- Impact
    - Spam (since difficulty is 1 and block times are what restricts tx)
        - UXTO set growth for the same reason
    - 40 days to kill the chain
    - Empowers 51% attacker
    - Political games (users individually incentivized short-term to benefit from more block space, miners individually incentivized short-term to benefit of more subsidy)
    - Minority miners not incentivized to try but it doesn’t cost anything
    - Original mitigation is good
        - Mandating new restrictions on the timestamp of the first block of a retarget period in relation to last blocks timestamp

## Merkle tree attacks w/64 byte txs

- Fake SPV inclusion
    - &lt;visual merkle tree diagram illustrating issue>
    - Years ago the attack required more work than proof of work, so was less of a concern, not so now
    - Arbitrary confs, less work
    - Simple mitigation
        - Require the coinbase transaction too, as all transactions on the same level of the merkle tree
- Block malleability
    - Separate but similar attack
    - Fork nodes
    - Simple mitigation
        - Dont cache context-less checks
- BIP’s original Mitigation
    - Forbid &lt;=64 byte transactions
        - No need to disable &lt;64 bytes transactions, since 64 is the issue
        - Concern about existing, unbroadcasted 64 byte transaction?
            - Would have to be insecurely small
    - AJ has an implementation

## Block validation time (DETAILS ARE PRIVATE)

- Was able to come up with 3 minutes block validation time on modern laptop, 90 minutes on Rpi4B
    - Quadratic hashing: 700GB
- Bypass mitigations from the original proposal
- How much data is too much?
    - Down to 1.2GB with simple mitigations, more requires being aggressive
- How bad is it?
    - Attack other miners
    - Stall cheap hardware
    - Anything else? Block propagation?
- What about transactions >100k? Confiscation concern
    - Simple hack, only apply new rules after outputs created after a certain block height

## Unique txids

- Not in the original GCC proposal, but could be useful to add
- BIP30 validation after block 1,983,702 turned back on
    - Originally enabled around block 200k
        - BIP30 was activated earlier, BIP34 was around this height.
    - Duplicate coinbase transactions
- Height in nLockTime? Mandate witness commitment?
    - Or use version field?
- Hardcode the two historical BIP34 block violations?
    - It was later pointed out this wouldn't work. It's unclear whether this can be done short of using a checkpoint.
- Does any early block exist with an OP_RETURN output which could be interpreted as a witness commitment (ie could technically be duplicate in the future). Sjors checked and there is no OP_RETURN output in any of the coinbase transactions prior to BIP34 activation.

Wishlist: Additional items to consider for inclusion?

- None discussed
- Fixing the year 2106 problem, but this is a hard fork so would rather not bundle it with the other more pressing mitigations.