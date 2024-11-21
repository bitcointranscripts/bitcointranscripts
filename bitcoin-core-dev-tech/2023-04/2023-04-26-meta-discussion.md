---
title: Project Meta Discussion
tags:
  - bitcoin-core
date: 2023-04-26
aliases:
  - /bitcoin-core-dev-tech/2023-04-26-meta-discussion/
---
# Part 1

## What makes bitcoin core fun

- Intellectual challenge/problems
- Interesting, diverse, open source project collaborators
- Meaningful project goals
- Culturally the project is a meritocracy
- Scientific domain intersecting with real world problems
- Real world usage

## What makes bitcoin core not fun

- Long delivery cycles -> lack of shippers high
- Soft fork activation
- Antagonism (internal and external)
- Ambiguity of feature/code contribution usage
- Relationships
- Financial stability
- Unclear goals

# Part 2

- Fitting rocks, pebbles, and sand in a jar analogy
- Time based releases vs feature based releases?

Feature based releases:

- How to handle CVEs in feature based releases?
- Partial features can be shipped (parts of BIP324 for example)
- Scope of refactoring if they conflict with features
- "What is likely to make it in?" mindset stops the bigger projects being shipped
- "High priority for review" list is uncoordinated. Maybe we as a project should say that this feature should make it in
- Be more vocal about what to get in and people need to be comfortable with that

### IRC

- Weekly meetings have been very quiet lately. Could use those meetings to coordinate
- IRC channel in general is pretty quiet, it’s a good venue to get one off opinions

Setting priorities for 26.0?

- Wlad had a say in previous releases, but with current group, we dont have as much of that direction
- Excitement around coredev, but fizzles after without direction
- Without goals, it's hard to get the big project (rocks) in
- Self directed nature of the project in conflict with priorities. We would all have to actually commit to the priority projects
- Having to sell oneself for purposes of getting grants can be in conflict with putting effort in toward long term projects
- Suggestion of post-release meeting to discuss the next releases projects to include
- Writing down the priorities makes it concrete, and is itself a projects "concept ACK"
- And then using regular checkins on those projects through the release cycle
- Inclusion of these projects in weekly IRC meetings, would solve empty meeting problem as well as keeping the project on everyones top of mind (own as well as potential reviewers)
- Onus of project owner to attend meetings
- Project Issue Trackers, consider pinning them as they are hard to find
- Use GitHub Projects?
- Feature prioritization is good, but one "big rock" is the project not falling over: Attestations, backport reviews, bitcoincore.org PRs, "keep the lights on" work, release process work, package management work. Shouldn't lose track of these pieces as well
- Who does it? "Release captain?"
- Group largely in agreement of priorities.

# Part 3

## Working in public vs progress via private collaboration

Rocks that succeed in getting into the project seem to have project working groups taken privately to coordinate
Not just us (trolls, reporters) in the IRC channel anymore. Seems like important conversations have moved off of there (some think this is due to folks not wanting to spam the IRC channel), but where is it next? (not bitcointalk, not IRC, maybe not mailing list).

- IRC subchannels
- Signal groups
- People like working in private without disruptions/distractions. More direct communication is more efficient
- Risk of missing out on valuable contributions/contributors when project is less public
- Technical design decisions via starting small group and growing slowly
- Recent "Mempool clustering" as an example
- Stop energy risk and impedance to progress with broader audience being involved
- Consideration of putting a lot of energy into a project privately and then being resistant/attached when pushing it publicly
- Tension of moving quickly vs. getting public attention
- Consensus, policy, p2p as more valuable (for internal and external parties) public feedback, vs. internal arguments about the internals of guix for example

## Stop energy vs. forward motion

- Counterpoint of wanting to "NACK" something to give honest feedback
- Stop energy spilling out of the project contributors into social media and snowballing is dangerous as well
- Distinction between stop energy with no constructive criticism vs technically well founded nack
- And reacting to each of these differently
- Stop energy vs being afraid of stop energy
- For example a PR with no formal ACK, but a lot of nits
- Pushing for more concept acks earlier, assumeutxo example
- Private conversations about objections to early technical approaches that were merged, but the objections weren't given early and now objectors distanced themselves from the effort instead of correcting

## Trolls

- Find controversy and amplify it
- Non-technical abuse
- Making the project contributors experience unpleasant
- Repeated assertions of bad faith behavior?

## Is this a project with intention?

- Goals of discussion is to help make this a project you all want to work on
- Retention of contributors is achieved by helping contributors achieve their goals
- If you want something different, we need to do things differently
