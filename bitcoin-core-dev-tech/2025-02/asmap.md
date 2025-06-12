---
title: PR Review Club
tags: ['bitcoin-core', 'asmap']
date: 2025-02-28
media: https://gist.github.com/fjahr/1cc55d7a5a2f9cf2ac09978ceea2ee5f
---

## Scribe 1:

PR 23792: is the only PR that's left for ASMAP (needs cmake changes first) -
hope to get this into v30.0

### How does ASMAP ends up in a Asmap file?

- Kartograph tool, based on rpki-client-nix ()
- use tool from bitcoin Core encode and compress it
- multiple people will run the Kartograph tool

### How often should you refresh it?

- using an old one should be better than /16
- but using a fresh asmap is better
- quality drops off slowly, probably five years or so. A years one is fine
- if we ship one in Core, it should be fine while the version is supported
- /16 is slighly better than random
- there is a healthcheck in the debug logs

in the asmap-data repo we do a collaborative launch multiple people join in does
not make it fully deterministic, but getting close to very good results there is
a tool to diff the results, but hard part is to interpret the diff

usually 5 people, often with high matches seperate PR for compressed files,
needs to ACK

Are you using the "combining unused ranges": no I don't think so, we can look
into this. This would make it smaller. using option `-f`

Urraca joined and is helping out. Speedups and testcoverage.

### Why is the PR still open, why is this not in the upcoming v29 release?

- Still open questions?
- Might need more research and data
- is there anything that would help make the ASMAP thing easier and more welcome
  to review
- concern about decay. How can you show this?
- tool that compares the asmap health scores?

### Communication on IRC channel

### Virtus concerns open?

- can be addresses before we turn it on by default
- "this might have a big impact on the network": yes this the goal
- once you have more people running in listening node from their home with PCP,
  this might help
- for block download you can connect all peers, and do it differently after IBD

### Are people fine with the distribution method?

- we discussed the a couple of different approaches
- the current on the the favored approach. but needs more review

## Scribe 2:

- New contributor to asmap tooling: Julien Urraca
- asmap Github org
- kartograph repo: creates the blob
- blob stored in repo asmap-data
- half life of the data set: Someone guesstimates 5 years. Presenter says we
  should always be better off than today. That said a malicious blob is *much*
  worse than current situation.
- Timestamp mocking in the tool which makes it almost deterministic (Presenter
  says it was for the past 6 tries him and the other contributor did)
- The diff tooling is available but the diff data doesn't give you much
  information at all
