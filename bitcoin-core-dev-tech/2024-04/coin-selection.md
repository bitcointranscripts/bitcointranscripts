---
title: Coin Selection
tags:
  - bitcoin-core
  - coin-selection
date: 2024-04-08
---
- Todo: Overview PR that states goal of replacing Knapsack
- Introduce Sand Compactor
- Demonstrate via Simulations that situation is improved vs Knapsack
    - Potential privacy leak: all algorithms would be deterministic, but feels insignificant or at least would not make it worse
- Should we clear out negative effective value UTXOs?
    - Users seem to indicate that they would prefer to empty wallets completely even if they pay more
    - General agreement that we should continue to spend negative effective value UTXOs
    - SRD and SandCompactor will allow spending them, maybe below discardfeerate, maybe below 5 s/vB, maybe even below 10 s/vB
- Fallback mechanisms if no other solution found
    - There is a gap between changeless solutions and minChange
    - No don’t fall back to Lowest Larger
    - CoinGrinder
    - Pick whole wallet
- Should we fall back to CoinGrinder when fees are large compared to recipient amount?
    - No, it’s fine for wallets to be smarter than the user 😛
- What were the changeless Knapsack solutions that were found by Knapsack and not BnB? 
- Idea: Remove changeless solutions from Knapsack
- Separate from Knapsack removal Idea: For large UTXO pools create a sample subset randomly and do coin selection on that
- Privacy improvement Idea: Slightly change fees on UTXOs randomly by a minor amount to change
    - Easier to implement: Just increases, because decreases can cause issues around minFeerate and changeless solution
- Unrelated idea: After we have privacy metric, cover APS as privacy score
