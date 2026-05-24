---
title: AI Slop Session
tags:
  - bitcoin-core
date: 2026-05-07
---

Transcript #1

- Getting a couple of AI/LLM Pull Requests per day, 15-20 per week
- Trend is rising in volume, but even worse it gets harder to identify
  over time, taking more time, interaction makes it obvious but takes
  even more time
- If they are just the middleman to Claude/remotely prompting, just do
  it ourselves
- Don't merge to not give them the recognition they seek and encourage
  even more of these
- Users don't understand what has changed or why, seems to be the core
  issue
- Distracting regular contributors. Multiple pings-> close it right away
- Targets?
  - Scanning open issues
  - "Good First Issue" tag is/was one of the targets, now it's basically
    gone
  - Sometimes AI open an issue and AI then also PRs
  - Sometime AI PR author and AI reviewer iterating against one another
- Merging encourages further PRs
- Motives?
  - Airdrops
  - Commit count
- Gray areas
  - Some newer/junior contributors, even if they have potential, use AI
    initially
  - Language barrier considerations
- Even regular contributors have AI-sloppy PR description
  - Don't write pull descriptions with AI
  - Don't use markdown headlines, otherwise drahtbot may auto close them
- Remedies?
  - Hacker News policy: "Don't paste content from an LLM"
  - Authors provide a disclosure of their usage, penalize accordingly if
    a violation
  - Discussion of tradeoffs of false positives vs time drain of project
  - Point to contributing docs, which might need better documentation for
    these types of users
    - "You are expected to understand each line of what you are
      submitting…"
  - Other projects have moved initial vetting to github discussions where
    someone needs to "vouch" for a user before they can be whitelisted
    to open issues and PRs
    - https://github.com/mitchellh/vouch
- TODO:
  - More aggressive with closing suspect stuff
  - Someone can write improved content for contrib, leaving the door
    open for people who want to improve. Canned comment as potential
    input
  - Suggestion/Discussion on disclosure policy in PR

One contributor's canned comment:

> Thx, but LLM output is not accepted if the author can not properly
> explain, test or could have written the change themselves.
>
> The bottleneck in this project has always been review and testing, not
> writing code. Development here is intentionally conservative and slow,
> and reviewer attention is the scarcest resource we have. LLMs have
> made this worse, anyone can now prompt them and post their output as
> PRs. There is an infinite amount plausible looking "improvements" for
> LLMs to suggest and work on.
>
> Unless we fully trust LLMs to both write and review code, humans still
> have to spend time understanding the proposed changes, which incurs a
> non-zero cost for every opened PR.
>
> I understand that contributing to this project can be intimidating,
> and using LLMs may seem tempting, but it really creates more issues
> for this project than it solves. The best way to help this project, is
> to review and test changes. You can use LLMs for this, but you
> shouldn't solely rely on them, or just post their output.
>
> I'm not asking you to close this PR. I am asking you to reconsider
> whether it's something you genuinely think the project should pursue,
> independent of what your LLM suggested.
>
> I'll close this for now, but the issue stays open for now.

***

Transcript #2

It's obvious to everyone that a lot of AI generated stuff has come up
recently. Do we have any numbers? Not really. Maybe around 15-20 per
week, and with numbers raising. The volume doesn't tell the whole
story: it's getting harder to identify them. One approach that still
works is asking the contributor some simple questions, which often gives
away if they're LLM.

Some of the PRs are very small, so it's hard to distinguish between LLM
and human. But it's fine to merge those. We mostly should be
aggressively closing larger slop PRs. One concern is that merging small
PRs might encourage more similar PRs to be opened - but so far it seems
most first-time LLM contributors don't come back for seconds.

There are cases where there are actual people try to contribute, but
very heavily rely on LLMs for their first contributions, especially
junior ones. If new contributors genuinely want to learn, we should
provide helpful feedback to them. We need to distinguish that from
remote prompting.

A big problem is when people open PRs without understanding the change.

A side-effect of the slop is that it distracts people interacting with
the repo, filling up their (human) context. Sometimes LLMs find actual
problems, but then fix it in a ridiculous way. At that point, it's
often better to just close the PR and properly fix it yourself.

DrahtBot was doing a decent job at autoclosing slop, but it's getting
harder, partially because real contributors are opening AI-slop adjacent
PRs. Should we ask authors to write PR descriptions themselves? Cfr new
hackernews rule: don't paste any LLM-generated comments. No one likes
the super verbose review comments, anyway.

Having a disclosure policy could solve the problem / help identify
whether someone is sincere. If something looks like slop, and there's no
disclosure, we can assume bad faith and act accordingly. "bad faith"
meaning the person doesn't actually want to learn, so we don't need to
invest time in that person. But can we enforce that policy?

Are we going to fight against AI contributions, or are we going to
moderate them?

More than disclosure, we need to have a policy that everyone is
responsible for every word they post. If it's crap, not concise, you're
out. But how do we enforce that? More aggressively close AI-looking
stuff? Do we have contributor buy-in for that policy? We will sometimes
get it wrong, so we should have a nice canned response / guidelines to
help people who are new to open source and genuinely mean well.

We need to make it clear that there is a big difference between
AI-assisted development vs just letting the AI do everything. But
writing rules on what AI can/cannot do is pointless, it's not going to
do anything.

Another repo uses discussions, you first need to open a discussion
before you can open a PR. Anyone can then reply "vouch" which allows
you to open a PR. It adds a little barrier for first-time contributors.

GitHub will soon be rolling out new moderation tools, including how many
PRs new contributors can open. Problematically, the cost of identity is
almost zero now.

If we have a disclosure policy, what if people just start saying they're
using an LLM for everything?

We need to require and expect from people that they have read and
understood every single line

One good way of reviewing is to quiz the (new) author, and see how they
respond.

Does anyone want to write-up a contributing guideline, and a canned
response? One contributor already has some materials ready.

Can we use AI to help identify and find AI contributions? There was
skepticism that this is possible/productive.

Should we add barriers to contribution? We already struggle to find new
contributors. Most new contributors are sloppy, though. Some people use
LLMs as a language barrier tool.
