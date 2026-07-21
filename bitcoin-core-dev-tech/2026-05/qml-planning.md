---
title: QML Planning
tags:
  - bitcoin-core
  - gui
  - qml
date: 2026-05-07
---

Last year, around this time, johnny09 started working on wallet
controllers: basic wallet send and receive etc. During summer, pinheadmz
helped rebase and restructure and update the project. Also around that
time, basically every contributor burned out, got a new job or
disappeared. Situation where a lot was working, but the idea of ever
fully replacing the current widgets GUI (1-1 functionality) didn't seem
feasible, given the tooling and feature gap. So time to figure out
alternative steps to release the project, but it didn't make sense to
replace the QT widgets without having most of the functionality working.
Alternatives considered included multiprocess, separate repo, .. The
project came to a halt for several months, until....

Codex and claude got very, very good at QML, which made him pick it up
again a bit later. Identified all the feature gaps, and identified ~22
core chunks of missing features (github issues opened for all of them).
For a lot of these, code / PRs now exists. A lot was done in the last
2-3 months. Also, 2 new contributors joined the project: epicleafies and
pseudoramdom.

With so much new code, the review burden went up a lot as well. But the
review threshold is much lower, the goal now is to just get everything
working.

One big change too is the test framework, which is challenging. New
TestBridge class is a new approach to automatically click through
multiple screens/objects, allowing for a powerful test suite. Is there
no existing functionality for testing QML logic? There is the qt-squish
product, it's commercial. Nothing open source. TestBridge is probably
the most impactful change since last year. There is now also unit testing
on all models and controllers, currently using gmock - people might not
like additional dependencies here, so might need refactoring. There are
also QML tests (e.g. qml_test_password_wallet.py).

With all of that in place, the next step is thinking about how to release
this. The goal is to fully replace the widgets UI now. E.g. PR that
deletes qt folder, adds qml folder. Can we chunk it up? Not sure how
that would work. It's different to how review usually works (in small
chunks), but it also wouldn't really make sense. QML can just be
reviewed in one big go. The amount of QML code is large, but LoC for
controllers etc is reasonable. The controllers look familiar, but
there's almost no more overlap with QT controllers.

How does the rest of the project get confidence in the review of QML? We
need to start publishing "releases" (or milestones) that users can test.
Three stages:

- preview: the first release where we actively want feedback from
  developers: how it feels to use, features to see improved
- beta: the PR is setup
- v1: ready to merge

There's a "QML GUI Roadmap" GitHub project to overview the WIP and work
ahead: project management.

Do we expect development pace to stay high after we've switched out QT?
Yes, because more users should attract more developers. How do we square
that with the bitcoin/bitcoin development process and maintenance
standards? TBD. Development is going to be design-first, going forward.

The app was initially designed for mobile. The side-effect of that is
that there's wasted space on a desktop GUI, e.g. the settings screen.
Redesign is necessary. That's going to be done before v1, there are
ideas on how to fix them. Also getting inspiration from other wallet
projects, e.g. Blockstream wallet (also in QML).

Has any work been done on decoupling GUI and bitcoind, i.e. using public
interfaces? Not really, but since GUI uses the existing node interfaces,
swapping that over should be fairly straightforward, even if there will
be some overhead from IPC.
