---
title: Stratum V2
tags:
  - bitcoin-core
  - stratum-v2
date: 2024-10-17
additional_resources:
  - title: 'Issue #31098'
    url: https://github.com/bitcoin/bitcoin/issues/31098
---
Overall question: Do we include it in Bitcoin Core or do we have it maintained separately as an IPC mining interface (multi-process approach)?

Pros of including in Core:

- Would be exposed to a higher level of review and so the code itself would likely end up being of higher quality
- Would possibly be easier for new miners to enter the space if it’s simply included in the bitcoin core binary (vs two binaries)

Cons:

- Adding to the (already large) workload of the project. Project bloat in general.
- Complicated Noise protocol, encryption, etc. How much refactoring would need to be done?
- Making it part of the review cycle could be a hindrance for miners that want to update this software. Iterating would be significantly easier without having to be in contact with Core.

StratumV2 has been designed with the idea of roles, with the idea that Bitcoin Core would play the block template provider role. Will having a public mining interface mean that third-party entities become template providers?

Big pro of using the multiprocess approach is the language agnosticism. If miners prefer Rust for example they can use that language and more easily address any issues that come up on their own, without having to really understand or work through the Core codebase.

If stratumV2 ends up being a separate project, who is going to maintain it?  If it is maintained by Core, when/how do we get feedback that this is being used and that it is worth continuing to maintain?

How will StratumV2 get included in hardware? It’s probably not going to start with the big mining pools in China. It’ll likely start with smaller mining pools, although Foundry might be a friendly larger pool that could help with adoption.

For newer smaller miners, it does seem easier to just acquire some ASICs, point them to Bitcoin Core software and have StratumV2 work. Instead of being provided an IPC interface and working with a separate application.

If multiprocess makes progress and is included in a release soon (possibly v29), then the interface approach might emerge naturally as the option we go with.

See [https://github.com/bitcoin/bitcoin/issues/31098](https://github.com/bitcoin/bitcoin/issues/31098) for issue tracking and additional discussion.
