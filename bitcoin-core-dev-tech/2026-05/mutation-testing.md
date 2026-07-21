---
title: Mutation Testing
tags:
  - bitcoin-core
  - testing
date: 2026-05-05
---

- Work has been done for about one year
- Lots of mutation testing tools for C++ and Rust
- Need for a specific tool for Bitcoin Core is likely required
- `bcoremutation` is a tool designed for mutation testing of Bitcoin Core
  specifically
- Weekly mutation testing takes a subset of files and publishes results
  on corecheck
- When someone opens a PR, we would like incremental mutation testing on
  the changes
- Setup is very manual at the moment
  - What tests should we run?
- Example is branch and bound algo improvements
- When a mutant survives, all tests were run and no test caught the bug
- Mutation tester looks at test coverage first then decides which lines
  to mutate
- Weekly based on `master` has manual testing of both source and test
  selection
- When people change code, they often change the test, so it could be
  used as an indicator
  - Not all the time, like in a refactor
- LLM could potentially be used to find which tests correspond to which
  file
- Dashboard for surviving mutants
  - To avoid spammy PRs
- How to avoid unproductive mutants
  - Changed code results in no tests, like for example changing the logs
  - Get AST of code and avoid mutating things like logs
    - Pattern match with regex (`LogDebug` for example)
- Mutation testing to evaluate changes to fuzz targets
  - For example adding more asserts to fuzzing
  - If someone changes the fuzz target it may effect the corpus
- Using LLMs to propose fixes to the unit tests to kill surviving
  mutants
