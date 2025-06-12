---
title: Consensus Cleanup
tags:
  - bitcoin-core
  - consensus-cleanup
date: 2025-02-27
---

- refresher on timewarp and Murch-Zawy attacks
- miners take ages to upgrade therefore we need to make preparatory changes asap to make sure they never create invalid once/if such a soft fork is activated
- tried to get feedback about whether they'd be comfortable doing so. Been told it's fine but we need a BIP with concrete specs of potentially-coming soft fork first.
- concrete preparations:
  - always respect the timewarp rule in the block template creator (done in 29.0)
  - always set the coinbase's nLockTime to current height - 1 in the block template creator (will open PR for 30.0)
  - the new sigop limit was chosen such that no regular standard transaction may be invalidated. However it's still standard to have p2sh inputs such that their redeem script is packed with CHECKSIGs. So the sigop limit needs to be enforced at the standardness level to make sure such pathological transactions don't relay / miners don't include them by the time we activate if we do.
