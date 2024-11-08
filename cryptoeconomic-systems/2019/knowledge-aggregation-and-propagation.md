---
title: Knowledge Aggregation And Propagation
transcript_by: Bryan Bishop
tags:
  - research
  - bitcoin-core
speakers:
  - Bryan Bishop
date: 2019-10-06
---
Intro
=====

<https://docs.google.com/document/d/1a1uRy10dBBcxrnzjdUaO2y03f5H34yFlxktOcanvVYE/edit>

<https://cess.pubpub.org/pub/knowledge-aggregation/branch/2/>

I'll be the contrarian - I think academia is awful and should be
destroyed.

Reputation is completely independent of content and should not be the
mechanism by which you judge the quality of research; *your reputation
is worthless to me*. (laughter)

*My perspective*: \[first, slidemaker's [*regret! might have reorganized
this\]*]()
[*I'm a bitcoin core developer. Also*]() worked at LedgerX (4 years). I
also work on biotech on the hobbyist side, garage engineering -- what I
was doing when bitcoin was launched. This is a community that recognized
there are amazing advances in science, you can do all sorts o things on
your own. You don't need to be on the manuscript treadmill and go to a
lab to do that work.

Transcripts
-----------

All conferences should have them! This is a great way to respect your
audience. The logistics of going to conference talks and conferences is
itself ridiculous. The economic cost of going to confs is quite high.
You should multiply the \# of participants by $1k to figure out how much
they spent — more if you include hotels and food.

Text is more convenient for mass consumption, takes up less of people’s
time. Do it real-time and publish immediately after. Immediate ones are
more valuable! I started doing this to try prove the content being
delivered in high school was awful and not worth my time. I did this for
every class for 4 years. It turns out no one cares. Kind of of how I
felt about high school itself.

I’ve experimented with this: If I wait a day or two about transcripts,
no one cares. They like having them **immediately**. *Example conference
coverage*:



There are many arcane topics only talked about at these confs, you could
only learn them by attending. And people might not realize they want to
learn those things unless they see them \[in context\]. See for instance
the MIT Bitcoin Expo, Scaling Bitcoin, and CoreDev (including EdgeDev++
for training developers in basic and advanced structures — also
available as videos).

People seem to like these; it is very competitive. They take videos and
post them. It’s fun to do. (hi Jim Carrey!) I use markdown, git, and
Ikiwiki.

Bookmarks, discovery, stats
----------------

I also do bookmarking from the commandline: using jotmuch/buku.

Use google scholar; exclude the site hosting the transcript, and find
other links to them. Human genome discussions, FBI interest, then some
nice bitcoin papers referencing the transcripts in formal publication,
and patents!

Over 10y of doing this, 1.5M words and 10MB of text. If you have
questions like “have any bitcoin devs considered how the fee market
would work without a subsidy?” the answer is “yes”.

How can we get more scribes?
-----------------

I can’t go to all confs. Other people should do this; help fund people
other than me to go to confs and type things (or commercial / court
stenographers?)

Turns out that court stenos make a lot of money - similar to software
developers (easily 200k/y).

Open research questions
------------

What about **machine learning for speech recognition**? First approach
had a 20% error rate w/ word recognition. Mozilla later redid the same
algorithm and made a better implementation; but both are trained on
audiobooks, not conference speakers. \[**Area for future research**!\]

**Improving conference quality**: Use surveys before/after. Has anyone
studied this? I’ve been to only 2 confs that have done this.

**Conference submissions tools** need improvement. Easychair is common,
but we should select talks more carefully. Commission or invite specific
talks from experts — don’t just hope that people who hear about and can
attend the conf submit something relevant.

Small improvements have large effects.

Bridges/resources for academia
-------------------

bitcoin-dev, IRC logs (bitcoin-wizards, bitcoin-core-dev), and
bitcointalk.org

It turns out LF doesn’t like email anymore and are deprecating
supporting email lists, so we’re looking for another solution.

If you’re thinking about studying something, find out who has done it
before and read their work /go talk to them \[I encourage you do to
both\]

Asides and alternatives
=======================

### Proof of Stake?

I see there’s a lot of talk about PoS here \[at this conf!\]. We looked
into that years ago and proved that it doesn’t work. It’s like
reputation; not costly and doesn’t work.

### Bookmarking

Use jotmuch/buku — back up your data! About 8 yrs ago I lost all my
marks in a tragic boating accident.

Alternatives to transcripts
----------------

**(Speculative) Meetlogs**— a homebrew crm, record all conversations,
track who people are talking to and about what, trace the origin of
ideas, and their frequency and contagion.

There are high bus-factors in our communities, if those people leave the
knowledge goes away. Track the sharding factor for ideas people care
about.

Alternatives to academia
-------------

Academia is broken. Publishing in particular. What to do?

Today we talked about reputation tokens; prediction markets, derivatives
markets… Sci-hub and piracy to avoid \[intermediaries\]

~ I don’t understand how prediction markets could help here, but \[Robin
Hanson\] often talks about this. Someone has to fund your prediction;
isn’t the fundaental problem getting funding in the first place? And you
need reputation again to inspire prediction…

*Sci-hub*: I may have accidentally doxxed Alexandra Elbakyan —
revognized her profile picture because I had seen her at a Harvard conf
in 2010. I said that in public…. Ireally like sci-hub! but it does have
problems. Namely: I’ve been looking for a complete copy of the 50TB
dataset. Sci-hub is the only entity that has it, apparently. Librarians
should have copies but they all seem to have sold out to OCLC. I also
have a rant against libraries, obviously!

Increase connection from academics to bitcoin devs
-----------------

Old concepts posted on forums and lists only sometimes get cited; is
often folklore but still a valuable source of knowledge.
