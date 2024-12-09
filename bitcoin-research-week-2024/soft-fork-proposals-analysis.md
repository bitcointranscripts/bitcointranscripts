---
title: Soft Fork Proposals Analysis
date: 2024-11-21
---

## Taproot

| Benefits                                     | Cost/risks                                                   |
| -------------------------------------------- | ------------------------------------------------------------ |
| Larger anonsets                              | Easier/cheaper jpegs                                         |
| Cost effectiveness                           | Raised script limits - yet unknown possibilities             |
| Fixed sighash                                | Temporary splitting of anonymity set due to new address type |
| Schnorr - batch validation, PTLC/Musig/FROST | More complexity                                              |
| Less bandwidth for signers                   | Quantum risk                                                 |
| Raised script limits -> more capable scripts | General soft fork risks                                      |

## CTV

| Benefits                                                     | Cost/risks              |
| ------------------------------------------------------------ | ----------------------- |
| Reduced interactivity in some shared UTXO protocols e.g. Ark | General soft fork risks |
| Timeout trees                                                |
| Congestion control                                           |

## CAT

| Benefits                                                                                                    | Cost/risks                                                                |
| ----------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| Trustless bridging to sidesystems: Scaling, Privacy, More expressivity (safer/easier languages than Script) | General soft fork risks                                                   |
| Non-equivocation contracts                                                                                  | Bigger txs could lead to harder knapsack problem -> miner centralization? |
| Makes multiplication in script more efficient                                                               | MEVil: Miner enforced tokens                                              |

Question: Did we do this backward? Start with use-cases and see which soft forks enable/fix them?

If no one uses the soft fork, then the drawbacks don\'t matter (but neither do the benefits) (well, except for the general risk of soft fork, so if we expect no one to use it, why do it?)
