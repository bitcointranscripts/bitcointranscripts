---
title: PR Review Club
tags:
  - bitcoin-core
date: 2025-02-28
---

## What are the goals of the review club?

1) Helping newcomers learn, beyond the conceptual/protocol knowledge
2) We all have PRs that we all want to review, and having people to bounce
   questions/ideas on is really helpful, so why don't we all come together

Are these goals compatible? They could be: to answer newbie's questions, we also
need experienced developers there to answer them.

Some attendees mentioned they learned a lot from review club in their early
contributor days, both from attending as well as hosting clubs.

Someone mentioned their PRs being reviewed, without them even being aware it
happened. This might also have been part of the initial design goal of review
club, where the initial goal explicitly wasn't to make progress with the PR
getting merged, but really just to help contributors. However, we don't have to
stick to the initial design goals.

Other people mentioned when their PRs got reviewed, they got a lot of useless
comments. It seems like some folks are less bothered about "useless comments"
than others.

Other feedback included:

- it used to be on more of a fixed schedule, every week. This is currently less
	so. - Preparing the review club takes a fair amount of work, and that became a
	bit untenable with the amount of people showing up. - Do we have enough people
	willing to host regular slots?
- We could prompt feedback on which PRs want to be reviewed? Make a little
  leaderboard, perhaps?
- A weekly review club made it difficult to move beyond concept/approach review,
  and finalize the actual code review before the next review club.

There are lots of working groups who want their PRs reviewed. Perhaps they can
propose PRs to get merged, and discuss them in IRC? That would be a cool output
of WGs, make them more transparent, and share information with the wider group.
-> Someone commented: if the entire WG likes/ACKs it, what's even the point of
hosting a review club on it.

About ~8 people raised their hand when asked if they would be interested in
hosting a review club every now and then.

What do people think about the author of the PR hosting, instead of someone
else? It's less work for the author to do so, but there is also benefit to
someone else doing it - offering a different perspective on what's easy/hard. If
someone else is hosting, it might be useful to check in with the author about
which kind of feedback/comments they are looking for.

We can also check-in on the IRC bitcoin-core-dev meeting wrt hosts for the next
meeting.

Another idea was to let the previous host of the review nominate another
person/WG to host the next one.

There can be a spreadsheet where people can fill in the PR they want to review.

Some people found it useful to prepare a review club when they just wanted to
review a PR. Review club prep notes could also flow back into the PR
description.

Regularity seems to be a big topic for everyone. Some people also got busy with
other things. One person noted this was during lunch time. Someone suggested
prioritizing PRs where there aren't too many comments yet / force-pushed. We can
also provide per-PR instructions on what's a good etiquette to interact with the
PR based on the state it's in.

bitcoin/bitcoin PRs aren't tagged with Review Club label anymore.

Someone mentioned they won't merge PRs with unaddressed comments, which review
clubs can make more difficult, because what if the author doesn't address
newbies comments? But other people said that wasn't really a review club
problem, because anyone could leave comments on a PR. Authors should feel free
to just say they won't address a comment.

People repeated often that regularity is important, so should we move back to a
weekly frequency? But both the prep and review burden is pretty high. Given the
high burden, it would be ideal if we reviewed PRs that are actually important.
But there was no clear consensus on what a good frequency is.

It was suggested to move the IRC meeting one hour earlier ( -> Wed 16:00 UTC),
and everyone seemed in favour.

Someone suggested asking the PR author if it's okay to post a comment linking to
the review club.

Someone suggested it's not necessarily about getting a PR merged, but about
concluding whether a PR is a right approach etc.
