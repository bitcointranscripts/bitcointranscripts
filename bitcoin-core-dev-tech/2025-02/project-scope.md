---
title: Bitcoin Core Project Scope
tags:
  - bitcoin-core
date: 2025-02-26
media: https://antoinep.com/presentations/coredev_2025_scope.pdf
---

_Note: this summary was drafted after the event on 2025-03-06_

## Duplication of project infrastructure?

Yes, but the projects infra setup and ongoing work is essentially subsidized for
the wallet and GUI now. So a separation would simply bring that to light and
alleviate non GUI/wallet devs.

Discussion of wallet / GUI funding: If there isn't funding for wallet or GUI,
doesn't that say something? But there is funding, it just goes mostly into
non-Core wallets GUI has funding but not sure what tangible other show for it? A
separation could allow for more contributors, faster iterations, showing more
progress to garner more funding

Discussion of “bars” for merge: Bitcoin Core has high bar for merge, but should
that same bar apply to all project or parts of the codebase Discussion around
“bars” being applied at a project level vs at a per PR level.

Discussion of how much work it is: Example of a software rewrite in a separate
project that ended up being way more work than thought and they still had to use
and manage both versions. It was pointed out this was not really a rewrite.

Discussion that separating the project was really just an extension of the multi
process work that has been going on for nearly 10 years.

Discussion that multi process, repositories, and different binaries are all
separate considerations.

Discussion that it’s unrealistic to merge a QML rewrite without project
separation. Nobody is going to review the use patchset after it’s done.

GUI-involved developer previously tried something akin to this but without
multiprocess in the past.

Discussion that a group is working on implementing it to see what the actual
trade offs are in practice.
