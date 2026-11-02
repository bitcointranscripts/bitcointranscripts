---
title: Mutation Testing
tags:
  - bitcoin-core
date: 2026-10-13
---

## Surviving mutants and test coverage

The session focused on the challenge of investigating surviving—or “live”—mutants: generated code changes that the test suite does not detect.

Participants reported that [bitcoincore.space](https://bitcoincore.space) listed 431 surviving mutants, including many in consensus code. Two had been verified as meaningful gaps, and pull requests had been opened to add tests that detected them. Many other candidates remained to be investigated.

The raw count does not directly measure the number of testing gaps. Some mutations do not change observable behavior and therefore do not require a test to distinguish them. Each surviving mutant needs verification before it can be treated as evidence of missing coverage.

The scale also depends on how mutations are generated. One tool was described as producing at least one mutation per line of code. A set of 46 mutants in `net_processing` was mentioned as worth investigating, although participants cautioned against concluding that the affected behavior was untested without examining the mutations.

## Workflow and coordination

The current investigation was focused on consensus code. Participants asked how candidates were selected, including whether easier-to-test mutants were being prioritized, but the notes do not capture a definite selection policy.

[mutanttest.space](https://mutanttest.space) was mentioned in response to a question about coordinating work and avoiding duplicate investigations.

Two tooling approaches were discussed:

- `bcore-mutation`, which was being run manually.
- A separate AI-enabled mutation harness, described as nondeterministic and capable of rearranging lines of code.

The number of generated mutations needs to be limited to keep execution time manageable. Using a small AI model to generate changes was also mentioned, without a detailed proposal.

## Test execution and review costs

Functional-test performance was a major bottleneck. Determining whether a mutant survives can require running the full test script, making investigation slow even when the number of candidates appears manageable.

Two pull requests had been opened to improve functional-test performance, and participants saw further opportunities to speed up the framework. More powerful hardware could also reduce execution time.

Review capacity was another constraint. Mutation-driven test PRs were reportedly being merged fairly quickly, but at least one participant emphasized that their review was not exhaustive. Large test additions could take substantial time to assess, and reviewers were not necessarily able to spend half a day examining each one.

The discussion therefore distinguished between producing tests that detect mutations and having enough capacity to understand and review those tests thoroughly.

## Further work

The proposed next steps were to:

- Run the mutation harness and Bruno’s tool on consensus-critical code in `validation.cpp`.
- Continue investigating surviving mutants and adding tests for verified coverage gaps.
- Improve functional-test performance.
- Explore integration with DrahtBot.

Mutation testing was also considered useful for identifying potentially dead code. Participants cautioned, however, that genuinely dead code must be distinguished from code that is merely difficult to reach or exists specifically to support testing.