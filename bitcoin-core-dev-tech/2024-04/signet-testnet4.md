---
title: Signet/Testnet4
tags:
  - bitcoin-core
  - signet
date: 2024-04-10
---
* Signet
    * Reset is less of a priority right now because the faucet is running again, still seeing huge number of requests
    * Should still reset because of money making from signet coins
    * Participants agree that getting coins doesn’t seem to be that hard, just need to ask on IRC or so
    * Some people get repetitive messages about coins
    * Signet can be reorged easily with a more work chain, that is actually shorter. Such a chain already exists and can be used any time. This effectively kills the current chain, even if the users have the old blocks they would need to actively invalidate the new chain and they could still not continue mining on it
    * Would give about 1 month warning before doing it
    * Someone is working on making regular reorgs of ~5 blocks a reality but harder to do than it seemed, still a solvable problem but needs a bit more time and effort
    * Using invalidate block doesn’t really work well for this use case
    * Would be cool to also mine double spends in the reorgs
    * There is a PR open for doing signet blocks faster than 10min
    * Signet block weight was restricted at some point due to spam leading to consistently full blocks
    * Does the more work reorg break pruned nodes on signet? Probably
* Testnet
    * What is different to Signet? Allows you to test mine, closer to mainnet
    * Stratum v2 doesn’t work with signet challenges (yet?)
    * Testnet3 should still be supported for one release
    * Higher minimum difficulty is discussed with no clear outcome, suggestion is to set it a bit lower than 1 million as suggested on ML
    * Adjustment of retargeting period also discussed, slightly out of favor
    * For the open PR: Needs test fix to get CI green, then will get review
    * Several agree that the time to lower the difficulty at 6 hours seems too long
