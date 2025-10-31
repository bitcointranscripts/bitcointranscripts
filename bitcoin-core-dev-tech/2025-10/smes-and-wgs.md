---
title: Subject matter experts and working groups
tags:
  - bitcoin-core
date: 2025-10-23
---

## What is maintenance?

* Different from just merge access and not just done by maintainers. It takes a
  village
* GitHub admin and moderation
* Continuous integration
* Releases and release process, backports, translations, GUIX, website (checkout
  the release-notes file)
* Security, disclosures, advisories
* Perceived “tech leads” in different areas of the codebase

## How are maintainers added?

* Avoid public nominations or popularity contests
* Anonymous nominations
* Maintainers review list and nominate on IRC
* Public IRC discussion

## Frequent contributors

* Not much wrt permissions. Can edit bitcoin-core/devwiki
* But can be tagged in review
* Main/only reason to be in that list
* Usually updated when someone new needs to be tagged
* Periodically people remove who are no longer contributing
* If you think you should/shouldn’t be in it, just ping us

## Triage permissions

* Add labels, tag issues

## Moderation FYI

* Locking means nobody can comment. everybody except maintainers
* Do not unlock for a comment and then relock (see OP_RETURN)
* Perspective is locking meaning everyone stop, cooldown period
* Moderation from the public look like the “organization” executed the action
  “bitcoin”
* Moderators can hide, not delete comments. Maintainers can delete
* “.” title for closed PRs usually means someone cleaned up obvious spam, so you
  can safely ignore

## Things to further take of maintainers plate

* Someone to run the IRC meetings? (see IRC meeting cheat sheet in the wiki)
  * Speak up if you want to be on the IRC meeting ping list

## Working Groups

* Please show up to IRC meetings to provide WG updates, even if it’s “no update”
* Pretype your updates to save time

## GUIX builders

* Want more GUIX builders. Initially 20, now less. Especially for minor releases
* GUIX builders, subscribe to release tracking issues
* Minimum GUIX builds required to upload to the website. More signatures,
  sooner, the better

## Website

* Looking for maintainers for the [bitcoincore.org](bitcoincore.org) website?

## Packaging

* Separate packing repo, for script and artifacts for many random things,
  looking for volunteers

## Subject Matter Experts (SMEs)

* People who have familiarity with a certain area of the codebase
* No feedback is worse than negative feedback in many cases. Silence deafening
  * Can maybe lose newer contributors due to this
* Informal tech lead position, somewhat already exists, but can formalize that
* Nice to have someone quickly concept ACK or concept NACK PRs
  * Avoids scenarios when PRs are opened and sit dead for weeks
  * Reviewers unsure whether to review
  * Author unsure of status/approach/etc
* Adds to burnout, confusion
* For PRs in certain areas of the codebase, SMEs can give future direction to
  PRs sooner
* Can also serve as a tiebreaker when mutually exclusive PRs are proposed
* Less of an owner of that code, but more of as an unblocker
* Names and areas will be public
* Expectation is that each PR in a given area will be reviewed (for concept ACK
  or concept NACK) within 2 two weeks. This is not a full review.
* Of course anyone else can ALSO do this
* Should bigger PR projects actually get an ACK before completely developing it?
  * Bring it up on IRC
