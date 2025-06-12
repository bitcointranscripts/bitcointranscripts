---
title: Merge/PR Workflow/Process
tags:
  - bitcoin-core
date: 2025-02-26
---

## Should we revisit / change the PR / merge PR workflow?

- In general, no major complaints
- general feeling that things are merged rather too quickly instead of too slow
- testing PRs are merged too slowly
- maybe people are more afraid of invalidating ACKs (not making changes / postponing to a follow-up) than necessary
- maintainers look at who gives the ACKs and weigh by their history/knowledge
- maintainer don't usually merge their own PRs (Ci and Test may be exceptions)
- sometimes merging triggers review (maybe things that were not really ready were merged and this caused more review and them actually to get ready) - this is risky, but may have worked in the past
- how many ACKs are enough? in general, 2-3 but depends on area and maintainer's judgement
- everyone gets frustrated if their stuff doesn't get merged, review is the bigger holdup than merging

## Trivial PRs:

- should trivial PRs be merged without ACKs? currently the process seems a bit random (some get merged, others just closed)
- people get rewarded with shitcoins for getting PR merged -> LLM-written, trivial PRs, don't wanna reward that / incetivise more

## Problems during Review:

- often silence to PRs after a NACKs without explanation
- silent merge conflicts ->  regular CI re-runs, (some) maintainers do multiple builds before merging
- many functional tests fail intermittently after merge -> can something be done about that?
