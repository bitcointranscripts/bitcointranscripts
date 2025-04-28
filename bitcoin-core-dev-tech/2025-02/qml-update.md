---
title: QML Update
tags:
  - bitcoin-core
  - gui
date: 2025-02-28
---

Meta:

- QML is only currently-supported QT framework

Background:

- Design team has put a lot of effort into constructing UI, including multisig
  and other features
- Goal: get parity to current UI. One-to-one, plus more
- There is a well documented 'design framework' that goes with this, including
  Figma toolkits
- Design framework allows people to expand the featureset in a natural way, from
  a design-first way, which reduces engineering work
- Mobile-friendly designs available.
- QML flexible and can be deployed in different environments, so designers are
  taking advantage of that by supporting mobile, even if no immediate plans to
  do so in Bitcoin Core
- Main focus however is /not/ mobile, it's the desktop version
- New contributors have been able to get involved quickly as a by-product of the
  Figma and design tooling available

Current/Completed Development

- Navigational structure is in place
- Basic forms are setup e.g. tx list page: pagination and filtering
- Working on early stage support of multiprocess
- Belief that multiprocess support could be completed in a week
- Node functionality was first milestone and are available

Note: known bugs in coin control that should not be carried over

- Concern that there are so many tiny wallet and gui fixes that might not be on
  the development list. How are these being tracked?
 	- This is where feedback, user testing is extremely helpful; some of those
 	  features are exposed in existing UI in non-obvious ways
 	- Do we have test for these?
 	- Do we need to go through the entire history of GUI PRs?

High level strategy:

- Not to reinvent much. Just looking at the interfaces and grabbing out the
  valuable components. e.g. how to process events.
- The core of the controllers and models are very similar. There are some
  differences, e.g. more separation of concerns, but overall the implementation
  approach is similar.
- Models are becoming far more stable now, want to ensure unit tests are
  available for each c++ module.
- In the future there is a desire for GUI tests. Familiarity on how to do that
  with QML. It's fairly easy to hook into and run end-to-end tests in QML. Goal
  s to add python library that can hook into qml engine, add helper tests, and
  then write natural end-toend- tests with infrastructure that'a already there
  (e.g. puppetteer). Infra challenges but we aren't there yet. There is an old
  QML bridge
- Working group is something we will really lean into. Communication hasn't been
  great within the project, so hopefully WG will help that.

- Wallet is getting close where it would be good for people to play with it.
  Want to figure out how to start getting user feedback

In light of upcoming migration to QT6, what expectations are there? Nice-to-have
features? Specific to QML

- Not too much that has dramatically changes, related to the feature-set
  relevant to us. Android framework stuff, perhaps
- No need to do any rewriting
- Not yet based on CMake

Any work on legacy wallet?

- e.g. In legacy wallet you can spend watchonly vs spendable balance.
- Legacy wallet support should not be dragged into new gui.

- How does the new UI framework fit into the review framework?
- How is feedback given? Where do these designers live, discord? Will they be
  around in 5 years?
- Github issues on github QML repo is the proper place to report problem.
- Work to bring them into IRC
- Bitcoin design community is growing and getting funding, getting momentum.
  Getting more fault-tolerant
- We stand to learn a lot from this community, given their study of the
  ecosystem
