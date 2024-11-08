---
title: CMake Update
tags:
  - bitcoin-core
  - build-system
date: 2023-09-21
speakers:
  - Cory Fields
---
## Update

Hebasto has a branch he has been PRing into his own repo. Opened a huge CMake PR for Bitcoin core.

Introducing it chunk by chunk on his own repo

QT and GUIX is after that

## Next steps

How to get this into Core?

We don’t have something clean. Still have something wonky and how and what to do with autotools.

Ideally introduce CMake for a full cycle. It might still be a little too rough to ship on day 1 of the v27 cycle.

We could deviate from the beginning of the cycle plan. Half way through a release cycle half way through a cycle is better than a crash and burn at the beginning of a cycle.

This is for people’s setups. There is a real possibility that people here wouldn’t be able to work.

Every branch is going to need to rebase, reinstalling stuff, etc. It will be a hit for productivity.

In an IRC meeting. If you think this is weird or just try it out. Try it now or for a month from now, but you are going to have to go through the pain.

If we wait until after branch off, how much of a difference will that be.

If you have 6 weeks, is that not enough time?
Ping people and have them try it.

Miners running old operating system, maybe will have the flow downstream. (C++ 11)

It is going to be a painful release.

We now have a split in the build systems, like backporting, now every PR has to rebase.

The goal is after the branch off to merge CMake and delete autotools.

## The plan

Ping individual people to test - there is a [PR to test](https://github.com/hebasto/bitcoin/pull/31). Goal is to have conviction on whether to merge after branch off.
Once things gets merged and that you can’t build, it’s on you.
