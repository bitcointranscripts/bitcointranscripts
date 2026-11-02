---
title: "LLM-assisted review: preparing PRs and managing findings"
tags:
  - bitcoin-core
date: 2026-10-16
---

## Sharing practices without losing diversity

The session considered whether tighter integration of large language models (LLMs) into development and review could help the project ship faster.

One question was whether contributors should distill and share best practices to avoid duplicating effort. Participants also recognized a tension: standardizing approaches could reduce wasted work, but a diversity of strategies may uncover problems that a single shared approach misses.

A “spell checker” analogy was raised as a way to frame LLM assistance. Rather than replacing substantive review, it could catch routine issues and help contributors prepare code for human attention.

## Preparing pull requests for review

Will’s Ralphbot was mentioned in connection with using LLMs as a CI-like preparation step: tidying code and resolving issues before asking reviewers to spend time on it. The notes do not describe the tool’s implementation or establish a preferred configuration.

The discussion also considered where automated review output should appear. One proposal was to keep the main PR discussion focused on human reviewers and link to LLM reviews elsewhere. This would make the automated analysis available without allowing it to dominate the review thread.

A related distinction was between:

- Comments posted directly by an LLM.
- LLM-generated comments that a contributor has checked and explicitly endorsed.

The latter approach received support in principle. It would place a human judgment step between generated findings and requests for other contributors’ attention. No formal requirement or posting policy was agreed.

## Intensive review near merge

Another proposal was to deploy an “agent swarm”—multiple review agents—when a strong candidate PR was close to merging.

This was acknowledged to be expensive. The potential benefit was a concentrated review pass that might help a ready PR reach a merge decision faster.

The notes do not establish how agents would divide the work, how their findings would be validated, or what evidence would be needed to show that this shortened review rather than adding more work.

## Handling a continuing stream of bugs

Loupe and Red Team were discussed in connection with hundreds of reported actual bugs, distinguished in the discussion from vulnerabilities. The notes cite a continuing flow of roughly **20–100 new findings every couple of weeks**, without providing a breakdown by tool or severity.

This raised a practical question: what should the project do with that volume of findings?

Simply ignoring them would not stop subsequent scans from rediscovering them. Participants asked whether the answer should be to fix them directly or batch the fixes to make the work more manageable. No batching or prioritization policy was recorded.

There was also uncertainty about how long the flow would continue. The “shaking the tree” analogy captured the question: were these scans exposing a finite backlog that would eventually diminish, or should the project expect a sustained stream of findings?

## Open questions

The discussion identified several possible roles for LLMs: preparing code before review, supplying contributor-verified review comments, concentrating automated scrutiny near merge, and discovering bugs across the codebase.

The unresolved issue was how to turn that output into **less human review work and faster delivery**, rather than simply more findings to process. Shared practices, separation of automated output from the main review thread, human endorsement of comments, and batching fixes were all raised as possible parts of that workflow—not as settled policy.