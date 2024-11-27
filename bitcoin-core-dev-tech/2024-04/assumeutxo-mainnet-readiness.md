---
title: assumeUTXO Mainnet Readiness
tags:
  - bitcoin-core
  - assumeutxo
date: 2024-04-10
---
- Conceptual discussion about the point raised by Sjors in the Tracking issue: [https://github.com/bitcoin/bitcoin/issues/29616#issuecomment-1988390944](https://github.com/bitcoin/bitcoin/issues/29616#issuecomment-1988390944)
- The outcome is pretty much the same as in the issue: Some people think it’s better to keep the params, and the rest agree that at least it’s better to keep them for now
- A perspective on the options: With the params, it puts more responsibility (and potentially pressure) on the maintainers, if they are removed the users have to do much more due diligence which snapshot is ok to use. But the thread to the users is a much more practical attack, at least it seems like it shortly.
- Removing the params takes away the chance for users to skip the background sync entirely in the future (launching into a pruned node state). Not everyone agrees that this would be a useful feature any time soon. In its current state, this would also screw up nchaintx.
- Discussion of open PRs on the tracking issue: [https://github.com/bitcoin/bitcoin/issues/29616#issue-2177880415](https://github.com/bitcoin/bitcoin/issues/29616#issue-2177880415)
- [https://github.com/bitcoin/bitcoin/pull/29612](https://github.com/bitcoin/bitcoin/pull/29612)
    - Needs response to the latest comments
    - General agreement the requested changes are good ideas
- [https://github.com/bitcoin/bitcoin/pull/29519](https://github.com/bitcoin/bitcoin/pull/29519)
    - Not as critical as originally believed but since it’s a bug it should still be fixed before the mainnet params
    - Needs review
- [https://github.com/bitcoin/bitcoin/pull/29726](https://github.com/bitcoin/bitcoin/pull/29726)
    - Potentially ready for merge already
- [https://github.com/bitcoin/bitcoin/pull/28553](https://github.com/bitcoin/bitcoin/pull/28553)
    - There will be a new PR once #29612 is merged
    - Probably adding a mainnet checkpoint for the halving and another params can be added before the next release as well
