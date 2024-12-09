---
title: What is the process to arrive to rough consensus about a soft fork proposal
date: 2024-11-21
---

## Definition of rough consensus

How do we define the group to have rough consensus on? For instance, a sub-group could have rough consensus on a proposal just because the largest group of experts isn’t interested in participating. Both groups may have a very different perception of the consensus.

The stakeholders defined in a recently published document could be a good starting point.

Different groups don’t talk much to each other, so it’d be hard to get rough consensus across all those groups.

**How did it go for previous soft forks?**

- For the early ones: YOLO.
- Later ones had a testnet with a demonstration of the feature enabled (for instance, CSV with Lightning is mentioned).

Some questions are written on the boards:

- Who is affected by the proposal?
- Who really wants the proposal?

## Thought experiment

What if there is a threat of quantum computers and people can’t agree between 5 different PQ algorithms being proposed?

It’s brought up that if there is a sub-group of experts in a sub-domain championing a change (whether it is PQ crypto or covenants) with a broader group that has no interest in deliberating, it’s the responsibility of the champions to agree on one proposal to propose to the broader group.

For the 5 different PQ algorithms, not everybody's opinion matters.

## Talking about the role of Bitcoin Core

It is pointed out that it’s not a “real Scotsman” issue. Instead, the concern is that there just won’t be enough nodes on the network enforcing the new rules if it’s not in Core (or a close fork of Core).

## What if the working group (say on covenants) had inside people who did not have a dog in the fight? Like a non-partisanship council?

The worry is that the process becomes a popularity contest.

Someone doesn’t think it’s a good idea: the purpose of a working group is to produce information, not to make decisions.

## The working groups that happened for Taproot

They were broad, grassroots, some happened in person, some happened on IRC.

Someone suggests a working group for covenants should be held on Delving. Mailing list is a broadcast system, more adapted to share outcomes of working groups, not every step of the deliberation.

The worst thing a working group can do is decide by themselves. They should produce information, not decide, or they will fail.

## Where do core developers sit in all this?

“Core developers” is ill-defined. They are only individuals. Some may participate in some working groups or others, some might not be interested.

We now have a draft of a process on the flipchart.

![Rough consensus process](https://raw.githubusercontent.com/bitcointranscripts/media/refs/heads/main/bitcoin-research-week-2024/rough-consensus/process.png)

## Summary

- Some people have a soft fork proposal.
- They get together and form a working group, produce information.
- Share results to the broader group, probably through the mailing list.
- If necessary, repeat the last two steps.

Quotes from participants:

- “Too many people feel like we are still in the brainstorming phase. This would help going from here to an evaluation phase.”
- “I feel for a lot of those proposals it’s a solution in search of a problem.”

The first thing to define for a working group should be

- “What problem are we trying to solve?”

Steelmaning?

- This process helps us answer how to solve a given problem, not what problem we should be trying to solve.

Questions you want to answer:

- \<snip, didn’t catch that\>

One person participating who is also a champion of a proposal said they were worried about following this working group process, that it could be seen as conspiratorial. Participants all agree that, on the contrary, this is necessary but **should not come across as making decisions**, but producing information.

Also, the information produced by the working group should be high SNR. Don’t try to drown people in information. Distill, maybe a page per week. Optech is mentioned as striking a good balance.

Core maintainers were mentioned a few times. It should be explicit that it’s not about maintainers. Maintainers just reflect what the larger group of Core contributors is interested in working on. You can’t just “get maintainers to merge something.” It’s rather “get contributors, experts in this area, to come and review this.”

Another person mentions they were clumsy in talking about Core maintainer. Rather, they said they wanted to point out that Core contributors / Core experts should be put in the loop early on, potentially to chime in on the approach. Their familiarity with how the system is actually implemented may be very valuable in how a proposal is designed.
