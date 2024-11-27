---
title: Discussion on open Coin Selection matters
tags:
  - bitcoin-core
  - coin-selection
date: 2023-09-19
---
* **Topic: review of https://github.com/bitcoin/bitcoin/pull/27601**
    * Problem statement: when doing manual RBF (without using bumpfee RPC) we treat previous change output as a receiver and thus create two outputs to the same address
    * Proposal: combine amount on outputs to the same address
    * What are valid use-cases for having the same address for change and output?
        * Consolidation with payment
            * Alternative: Use sendall with two outputs one with an amount and yours without an amount
        * Payment and send at least X to yourself
        * Consolidate with automatic coin selection of at least X
            * Alternative: Implement "Send at least" as a separate and explicitly feature
    * Consider just giving an error if change destination is the same with one of the outputs
        * Should we do the enforcement only at RPC level?
            * No, because this is risky
    * We don't want to fix manual RBF, because we have bumpfee RPC
        * Maybe you can also take original TX and give to fundrawtransaction
* **Topic:  https://github.com/bitcoin/bitcoin/pull/26732**
    * CreateTransactionInternal should remove UTXOs conflicting with preselected
* **Topic: Where do we make change decisions? During tx building or coin selection?**
    * Whether we create change, how big it is and the type
    * We determine the size of the change twice
        * One time to feed into coinselection
        * Second time when we do the actual tx building
    * One approach is to let coinselection pick change type
    * Conclusion so far: Status quo remains
* **Topic: Bug when BnB produce change https://github.com/bitcoin/bitcoin/issues/28180**
    * Min_viable_change is different from cost_of_change and it doesn't include change_fee
            * Zeroing out coins selection params for SFFO is bad
        * We need to fix change_fee
    * One solution: Reduce upper bound for BnB when SFFO
    * Another solution: disable BnB and exact knapsack when user requested SFFO
    * SFFO use cases are still unclear
* **Topic: Coin grinder algorithm**
    * Find a solutions with minimum weight and always creating change
    * Differences from BnB
        * when fee rate is lower than LTFR
        * Always find a solutions because we have change
    * Why lower first?
        * To minimize liquidity in flight
    * How to avoid grinding it to very small UTXO set
        * Only use it at high fee rates
        * Use multiple of LTFR
    * Next steps: Run the simulations
* **Topic: Knapsack removal**
    * Useful because consolidatory
    * Need more research on changeless solutions not found by BnB
    * CoinGrinder replaces lowest larger
    * Garbage collection for negative effective value
