---
title: Refactors
tags:
  - bitcoin-core
date: 2023-04-25
aliases:
  - /bitcoin-core-dev-tech/2023-04-25-refactors/
speakers:
  - Fabian Jahr
---
One take-away from the Chaincode residency in 2019 was: Don’t do refactors (unless you really need it)

A marked increase from 2019 to today
(Chart on the increase of refactors)

The comments and PRs are steady but the refactors are increasing

Quibble about how regular reviewers are counted (should be higher than 5 comments)

Project reasons:

- Ossification?
- Natural way mature projects progress/Boy Scout Rule

Personal reasons:

- Time commitment of large review may not be possible (extended period of singular focus)
- Merged PRs as proof of work, could help with the next grant
- Feels good to ship

What is the effect?

- Working on refactors takes away from other work
- Leads to rebases, sisyphus work for authors and reviewers
- Speeds up for new-comers but slows down experienced contributors
- Renamed variables as example

Refactoring has been fully commoditized with LLMs

- If there is a good refactor from GPT, we should take that too

PRs from newcomers

- We allow for less complex topics

Part of the problem is too much politeness

- You don’t have to ignore it
- It does have value
- But it depends on whether it’s a problem
- In 2014: people have also been complaining about paying too much attention to small things
- If reviewers have preference for picking smaller things to look at first, that also detracts
- This is probably a problem because of reviewers choosing to review smaller things
- Harsh feedback scares people away
- More pushback on the individual level

If you are part time, it’s easier to do small things

- Full timers - more comfortable to jump into something that is deeper - we don’t have
- Like to work on larger domains but grants may not value that as much
- Open a lot of smaller refactors to make it seem like they are doing something

High value refactors:

- Fuzz targets
- Some refactors that are high value that never get addressed
- Significant PRs can have refactor commits and sometimes those are the best kind
  - The reason why the big projcects have refactors is because it is addressing the technical debt
- We need to be more proactive and vocal about what we want and don’t want

Onboarding perspective - if you are mentoring someone, be mindful for what they are working on

Funding matters when it comes to diving into something deeper vs nights/weekend contribution

Don’t have enough good first issues anymore, label isn’t used much lately
We should give better guidance to newcomers and those that may be experienced but don’t have much time
"I don’t think we should have follow-ups to fix your nits"
"If you are the 3rd person to ack a PR and you leaving 30 nits, then it probably doesn’t matter"

Q: Did the refactor moratorium ever have any effect?

A: It was never instituted

Q: Do we have any guidance on the contributing guidelines?

A: Yes

Q: Do nit changes need to invalidate ACKs where the maintainers can clearly see that they don’t impact functionality?

A: The merge script won’t pick up something from the older commits

Q: Could change the merge script to add the stale acks, but the commits they ack disappear

A: If you want attribution, you can re-ack

You are allowed as an author to ignore nits, but it’s good for you to acknowledge them, even if you are going to ignore them
