---
title: The State of ASMap
tags:
  - bitcoin-core
  - p2p
  - asmap
date: 2026-05-06
---

*Notes from an in-person discussion on ASMap's progress, the
collaborative run process, reproducibility, and open questions around
tooling and releases.*

## Where We Are

ASMap is embedded in the latest release. That's a milestone — but
there's still a lot left to do. Many of you have already participated
in the process.

## Collaborative Runs

### Recap

The goal of collaborative runs is to gain assurance that the ASMap file
isn't pulled out of thin air: multiple independent participants should
be able to produce the same map.

The last couple of runs had **more indeterminism than we're used to**.
The most recent run had only **6 out of 20** matching, where we'd
expect a much higher percentage. We're still trying to figure out why.

### New: Web UI for Result Uploads

We've built a web UI for uploading final results files. It runs a
**diff between submissions** to show exactly how many differences there
are, rather than just comparing hashes. It's a starting point before
going deeper into debugging.

## Release Attestation Process

Closer to releases, we want a process for **attesting to the ASMap file
we embed**, similar to what we do for Guix:

- When you submit your file, you sign it with your PGP key.
- A repo similar to `guix.sigs` — call it `asmap.sigs`.
- Cadence: maybe monthly, definitely for every release.
- A signature should be **required** alongside every submission.

### Tooling: One Encoder, Not Two

There's a branch with an **x++ encoder and decoder**. It's
deterministic, but not identical to the Python one. We shouldn't
maintain two tools in parallel.

There's an open PR for doing the encoding plus signing. The outstanding
question is **where the signing repo should live**:

- Under `bitcoin-core`? Guix artifacts aren't put on GitHub at all.
- Proposal: put it in the existing **`asmap-data` repo** — no new
  repos. Start putting sigs there and update the README accordingly.

## On Reproducibility and the Matching Threshold

> Housekeeping and processes around releases. Sigs + data packaging
> seems fine. But where did we land on the threshold of matching? What's
> the intuition on how much non-determinism matters?

What we really care about is **reproducibility** — it's the silver
bullet. But if I participate in a run and get a different result, I
should be worried: are other people conspiring to produce a malicious
one?

So this depends strongly on **what's actually causing the diffs**. Why
does your file differ? If the reason is acceptable, I might be inclined
to sign off on someone else's diff.

The goal of many people doing the same thing isn't reproduction for its
own sake — it's confidence that the process was carried out honestly.
The process may have **inherent non-determinism**. As long as it's
explainable, that's okay. If it's not explainable, it's not shippable.

## Long-Term Monitoring

We want a **dashboard to analyze ASMap decay over time**. We've done
this ad hoc; the idea is to build more things on top of that data.

The main question around **enabling ASMap by default** has been: what
happens to the file over time? We'll use our old run data — comparing
the actual complete map against the nodes observed on the Bitcoin
network.

### AS Number Lookups

Can we map names to AS numbers? Is there a public way of getting this
data easily? **Cloudflare Radar** should work — but the data isn't in
RPKI.

## Kartograf and Data Ownership

People have asked about moving data out of Kartograf if others are
using it. It's a bit weird that the software is external but the data
is internal — but practically, we don't really care.

## Releases

We've moved away from doing releases of the tooling, because we've seen
roughly **80% of participants just running `master`** anyway. Trying to
keep everyone in sync on releases hasn't worked.

Counterpoint: **you should do releases and tell people which release to
run**. Including the release version in the command forces it on
participants, which is an effective way to keep everyone aligned.

## Small Improvement: Source Annotations

On every line, add a comment — a dash followed by the **source of that
information**. Small change, big win for traceability.

Zipping final result file makes it small enough for sharing (in GitHub
for example)

asmap_tool.py in Bitcoin Core repo can be used for deduplications in
raw input file by just running the decoding step without any other
parameters.
