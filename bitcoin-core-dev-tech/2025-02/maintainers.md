---
title: Maintainers
tags:
  - bitcoin-core
date: 2025-02-26
---

- a lot more than just a GPG key in the file
- want more of people taking ownership over knowledge, functions, sub-projects
    e.g. security, P2P, monitoring
- maintainers have responsibility for shipping code, and keeping it secure
- project doesn't have a lot of definition of what maintainer is
  - "a button pusher"
  - actually make sure the release process is followed on time
  - functioning website, upload the binaries for each release
  - general repository maintenance
  - assign PRs for review, close abandon or stale PRs
  - if there's sporadic CI failures, open new issues
  - make sure projects set for release get in to that release
- do we need more maintainers?
  - depends on what the definition is
  - lack of leaders (for lack of better word) for sections of codebase
    - someone who can tie-break when there is a debate
    - track CVEs make sure they're fixed
  - someone needs to be accountable
    - get stuff ready in time for feature freeze
    - bugs that need to be fixed in time
    - if there's a feature in a half-merged state, merge the rest or pull it out
- if someone wants to be a leader of some part of the codebase they can just start DOING that
- part of the job is taking heat from the community
- maintainers.md file attempted by never finalized, trying to define the role
- repos like qa-assets have their own "maintainers", lower stakes
- "bystanders" rely on maintainers to do all this
- how does the linux kernel project work?
  - trusted lieutenants for sub systems
  - Other OSS like Go, Rust, Kubernetes
    - steering committees
    - hard spec'd documents for their process
    - special interest groups with various levels of autonomy
  - doesn't linux have "merging periods"? but they also have a rapid release cycle
- code-owners file:
  - no one used it, it got killed
- people ignore PRs, effectively a silent NACK like a pocket veto
  - need more concept ACK / NACK early in PR life cycle
- Maintainers remember old discussions like auto updates etc "we're not doing that"
  - new contributors show up with an old idea, maybe even get some ACKs
  - Maintainers block things as experienced contributors, not necessarily as maintainers
