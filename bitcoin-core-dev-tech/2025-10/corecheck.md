---
title: CoreCheck
tags:
  - bitcoin-core
  - testing
date: 2025-10-21
---

On PRs, Drahtbot provides a link to CoreCheck results. That's probably most
people's interaction with CoreCheck.

## Coverage check

Using gcc at the moment, too many false positives so probably will need to move
to clang. It doesn't seem to be used very regularly atm (getting few reports
when the tool is down).

Why not being used? Attendants reported unreliability to be the main reason: if
it fails once, you stop looking at it. Also, slow: pages would load slowly.
Also, when PRs are updated, the results need ~an hour to be updated.

The tool shows how PRs change coverage, specifically which lines are affected.

## Homepage

The homepage used to be quite slow, using datadog in the backend, which is
triggering tracking prevention in browsers, so it's now routed through a proxy.
The proxy is a lambda, which is not always up, adding a lag to initial homepage
load in case of cold start.

Homepage has a couple of vanity metrics - look nice but not super useful.

Datadog is used for legacy reasons, no real reason couldn't use e.g. Grafana.
Datadog doesn't differentiate between prod and dev.

## Benchmarks

Will highlight if PR is >10% slower than master, which works quite well. Less
happy about the SonarQube loud code smell tests, generally not too useful. Also
measures static binary size.

One attendant suggested the overview is quite dense, maybe adding tabs / letting
the user choose the information they see. Also, if only one component of the
website is unreliable, that makes people doubt the whole website/project.

## Mutation testing

Only for some files, not the whole codebase. Coverage slowly increasing.

You can see source code. Red line: unkilled mutant, i.e. that change does not
cause any tests to fail.

Tests are ran every Friday, takes approx 20 hours to run. Slowness comes mostly
from functional test suite, tests taking > minutes to run. Much more of a factor
than compilation, which is quite fast thanks to ccache. A manual selection of
tests is ran, that are deemed relevant to the code covered. We can also compile
this list from test coverage, but e.g. for coinselection that doesn't work. A
lot of tests use coinselection, but that doens't mean they test coinselection
logic.

A good example of a PR that fixed a bug from mutation testing:
http://github.com/bitcoin/bitcoin/pull/33047

One attendant suggested it would be nice to be able to run mutation testing for
a single PR. The issue here is that it just takes a really long time to run even
for a small number of files. However, if a PR changes ~20 lines of code, we
should be able to get much more specific with the mutation testing. People can
easily run it locally, see https://github.com/brunoerg/bcore-mutation

The tool tried to avoid useless mutations based on regex (e.g. logging, ...).
The tool has support for generating mutants only for LoC that have test
coverage, because otherwise it just won't catch anything anyway.

The mutation testing could be extended to cover libsecp256k1.

A recent paper indicated that it's also helpful to mutate the tests themselves,
not just the tested code.

## Discussion

- do we keep developing this? Is it useful?
  - could we add an overview of which fuzz tests are slow?
- corecheck is doing a lot of things. we could spend a lot of time talking about
  what it's doing now/usefulness, but maybe we should think about the problem
  statement? Which problem are we trying to solve in Core?
  - because right now it's trying to do a lot of things at the same time
  - it's become a kitchen sink. At the moment there's no real problem statement.
- Some tools are useful to have, but can't easily be fit into CI etc. Having a
  place like CoreCheck is useful, because running them locally might be too
  inconvenient. Also, tracking this information over time is helpful, e.g. for
  test duration and binary size
- One participant was surprised that mutation testing only runs once per week,
  should be documented better
- CoreCheck is one tool, but really is a collection of components. One
  participant did not see why this is specific to Bitcoin, would be useful for
  any repo. E.g. the ui, scheduling of jobs, mutation testing, communication
  back to github, ... CMake already provides 2 of those components: CTest can
  drive the tests, collect results and send to dashboard, and CDash can act as
  the dashboard. The overlap could be reduced by implementing a CDash proxy,
  that would make CoreCheck useful for any OSS cmake-based project.
