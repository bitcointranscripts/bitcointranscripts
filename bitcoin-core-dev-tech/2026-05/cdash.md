---
title: CDash
tags:
  - bitcoin-core
  - ci
  - testing
date: 2026-05-07
---

Wanted to propose adding a CTestConfig.cmake file in order to collect nightly,
continuous and experimental build and test data in one place. This actually got
done ~ during the meeting, in https://github.com/bitcoin/bitcoin/pull/35222

With the result that now you can visit
https://my.cdash.org/index.php?project=bitcoin-core and see various esoteric
bitcoin core builds.

This get even more valuable if we can get contributors, users, package
maintainers etc to submit their esoteric/unusual builds there too. I have an
example ctest script here for how to interface and upload to the dashboard:
https://gist.github.com/willcl-ark/421caf263c3aa10c4e0293a9049bbf8b

But any LLM will generate one for you too. It can be configured to run nightly
or continuously very easily, and the dashboard is currently un-authenticated.

We would welcome more specialised builds, and builds on exotic hardware from
those that have these things. It was discussed how the aim of the dashboard
could be to **try** and break builds, with the maintainers/contributors' job to
fix them. We want to see breakages on here!
