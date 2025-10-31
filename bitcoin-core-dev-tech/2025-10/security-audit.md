---
title: Security Audit
tags:
  - bitcoin-core
  - security
date: 2025-10-21
---

OSTIF helped us find a good security company to work with. Most companies
declined because they assumed they wouldn't find much and didn't want to risk
their reputation. One provided agreed to do it, had a couple of engineers spending
a few days at the Brink office leveling up on the codebase and different
components we wanted them to focus on.

The output is a Technical Security Audit Report.

## Technical Security Audit Report

Why we did this? As far as we know, this has never been done before in the
Bitcoin Core codebase. Initial expectations were pretty low, both from our side
as well as from the provider. For first engagement, we didn't give them a very
fine-grained scope, but told them about the attack surface we care about (p2p),
and left it to them to decide what to look at in detail.

tl;dr: they didn't find anything critical. A couple of informational things wrt
threading.

Research did not involve supply chain attacks.

Initially they were thinking about doing fault-injection type stuff, but didn't
end up going that route because there was no time left. They did a manual code
review, and looked at existing fuzz tests - as well as writing a couple new
ones.

Our code has different code for different platforms in some places. The security
firm didn't do any platform-specific testing, and we assume they only tested x86
linux (unverified).

The report is going to be made public after we've provided feedback on the
draft, expecting a couple more iterations.

The new fuzz tests may be PR'd, but they had to hack around things a bit which
might not be worth integrating into our codebase.

We don't expect any of the researchers to continue contributing to the Bitcoin
Core codebase. They did seem enthusiastic working on the project, despite later
frustration of not finding any big issues.

We don't expect to issue a follow-up project, at least a broad one, since we're
not expecting meaningful results.  Potentially we might contract externally for
a very specific, narrowly scoped project, e.g. reviewing Cluster Mempool.

The (lack of outcome) is not surprising, and was considered a very possible
outcome at the start, but is still a nice confirmation of our best practices,
given the experience of the third party engineers.

We don't want to frame this as "Bitcoin Core is audited" like some crypto
projects do, this is just part of our ongoing security efforts.

Part of the reason they didn't find anything is probably because they weren't
intimately familiar with the code before this 4-month project.

Did they use any special tooling for their research? Nothing out of the ordinary
/ things we don't use: they used static analysis, fuzzing (same fuzzers that we
use), ...

One of the architectural issues found is, when fuzzing chainstate you need to
clean the filesystem which is expensive. They introduced a "Virtual FileSystem",
mocking the diskio stuff to be in-memory. We might be able to use this directly
in our code.
