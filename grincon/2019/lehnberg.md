---
title: Grin update
transcript_by: Bryan Bishop
tags:
  - adaptor-signatures
  - altcoins
speakers:
  - Daniel Lehnberg
date: 2019-03-26
media: https://www.youtube.com/watch?v=sPgJqAdKkhY
---
## Mimblewimble pros and cons

There are no amounts, no addresses, and improved scaling. But one of hte problems is that it requires interactive transactions. But this is a pro because of this you have to participate in mining. You can send money to addresses without having to accept the money. Just as you saw here, you can identify the blue box as an output or an input. You could build up a transaction graph. There are some attacks that are possible.

I think Andrew is going tobe talking about scriptless scripts later today.

## Project history

* Announced 2016-10-20 by "Ignotus Peverell". It was the first mimblewimble implementation. It's written in rust. It's open-source, community driven, funded by donations. There's no ICO, CEO, advisors, investors, founders, premines, pre-ASICs, no pre-anything. The goal was to make something fair.

## Why bother?

We felt that mimblewimble's technology was worth experimenting with. It wasn't possible to do it as well with bitcoin or a sidechain. Sidechains were still a theoretical or mythical beast.

Some mimblewimble-native concepts are impossible in bitcoin. And mimblewimble can move faster and implement state-of-the-art techniques that bitcoin can't push as quickly.

Whether it works or not or whether it proves to be good, that remains to be seen.

## Words I use to describe the project

I describe the grin project as open, fair in the sense of how it was launched and how it is run. It's honest because you can be honest because you have no incentives to not be honest. It's minimal, we tried to do absolutely the-- keep the protocol level as small as possible which is quite tricky. It's rational in that we try to rely on scientific principles for the way wre work... and it's transparent.

## Governance

What counts as a governance model?

One way to summarize our thoughts on this is that governance is really hard. It's definitely a human problem. It's a political problem. There is no grin foundation. There's a technocratic council. We try to do the least harm as possible. We try to keep it as simple as possible. Decisions are taken in the open bi-weekly development and governance meetings where possible.

We still encourage anyone to create a new foundation if they want. There's no "grin" foundation though.

We are constantly second guessing ourselves about the council and its role. We try to take all of the meetings in the open. We do it every Tuesday. Anyone can join and participate in that. It's working right now. We don't know how long it will continue to work.

## Technologies used

* Schnorr signatures give us smaller signatures and scriptless scripts.

Bulletproofs give us smaller range proofs, required for confidential transactions. We use rangeproofs to prove there's not a negative amount.

Scriptless scripts- Andrew is going to talk about this later today. It enables atomic swaps in grin and some other scripting behavior.

Dandelion too, it's a privacy-preserivng transaction propogation and aggregation. It helps obfuscate where transactions came from.

## Future areas of research (maybe)

Flyclient- a lite client for grin.

Lightning network is possible.

Confidential assets is possible.

We've been thinking about universal accumulators.

We've been thinking about BLS signatures.

## Emission schedule

It's 1 grin/second, forever. It's realized through proof-of-work. It has one-minute bock time. It's 60 grin constant coinbase reward. It's simple, and it's fair. It douscrages an unfair advantage for early adopters. There's nothing for us to gain from that. Anybody can join, they don't need to be there first to get a headstart advantage, since they can get the headstart advantage later.

## Cuckoo cycle family

We start with a hash table with a lot of nodes, in the billions. You want to clear those up so that you can end up with a cycle or a loop. This is the high-level summaryz of John Tromp's cuckoo cycle proof-of-work.

We have two variants. One is for GPUs and the other is for ASICs. The GPU one is CuckARoo29 and the ASIC algorithm is CuckAToo31+. We're looking to migrate away from the GPU proof-of-work and to an ASIC-hardened proof-of-work.

It's quite hard to bootstrap a fair network in 2019. We don't want ASIC manufacturers to have an early advantage. So it starts off at 10% at first and then linearly increases over time.

## Current status

Grin launched 10 days ago. Fairly smooth. Yeah. Business as usual after that.

## What's in the box?

There's a node, a mining protocol, a wallet with basic commands. You can use keybase. There's minin gsoftware for nvidia and AMD GPUs for both algorithms.

## What's next?

A lot of this depends on quality of life, security, stability, performance, improving documentation and nurturing the ecosystem. The design being minimal means we expect a lot of the end user solutions to come from other people rather than the core project. The project is very minimal.

## Exchange integrations

We don't do applications. We don't do NDAs. There's no legal entity. We don't pay listing fees, we're broke. We do try to be helpful, and we do welcome integrations, and contributions to the dev fund.

Exchanges have begun to show interest and every once in a while they announce support. It seems to be working okay.

## Selected community projects

<https://github.com/grinplusplus/grinplusplus>

grin-pool.org

grinscan.net and grinexplorer

https://tmgox.com/ sells swag and all the profits from this go directly to the developer fund.d

grinnews.substack.com is a weekly newsletter. It summarizes development news each week.

## Contributing

If you want to contribute, as hashmap says, "just do it". We need rust developers, researchers, frontend developers, grpahic designers, UI/UX specialists, technical writers, and community memnbers in general to help us test and improve our governance.

## Get involved

Don't ask for permission, just do it. Be excessively police and nice. I think that's a good rule when we try to apply this in general in the public.

<https://grin-tech.org>

## Fund yeastplume

He would like to work full time on Grin from March - Aug 2019. His goal is to raise about $55,000 euros. This is a good way to protect your grin investment. The best way to do this is to help fund developers.

https://www.grin-forum.org/

## Take a technical crash course

There was a last conference in Berlin. There's some slides available on grincon.org look it up.

## Value proposition

Grin is not perfectly private, yet. But it does the job quite well. Privacy is turned on by default, and can only selectively be turned off. Being community driven is a core strength, not a weakness. We really want the community to protect the council. People expect there's a developer company building this. But me as a community member are just a consumer, a user. We want everyone to contribute and help grow the community. And the fact that we had a fair launch and emission schedule aligns our interests and protect integrity. It's easy for us to stand up and say we're not perfectly private. It keeps us all honest and self-selects people who want to get involved because it's not an immediate way to have a financial gain from this.

## Q&A

Q: Will the presentation be posted?

A: There's a place we keep our meeting notes and presentations.

Thank you daniel.
