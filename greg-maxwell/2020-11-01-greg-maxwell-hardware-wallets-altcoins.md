---
title: Hardware Wallets Altcoins
transcript_by: Michael Folkson
speakers: ['Greg Maxwell']
tags: ['hardware wallet', 'altcoin', 'wallet']
date: 2020-11-01
---

Location: Reddit

https://www.reddit.com/r/Bitcoin/comments/jlwxpq/why_do_you_think_coldcard_doesnt_support_altcoins/gasoyuj?utm_source=share&utm_medium=web2x&context=3

# Why do hardware wallets not support altcoins?

They're an enormous distraction and hazard to software development. It's hard enough to correctly and safely write software to support one system. Every minute spent creating and testing the software for some alternative is a minute taken away from supporting Bitcoin.

I can say first hand that my efforts to review hardware wallet code against possible vulnerabilities have been actively thwarted by hardware wallet codebases being crapped up with support for altcoins. It's easy for cross-system behaviour differences to turn into outright vulnerabilities, for multi-system complexity to hide them, or for the need to support multiple systems forcing out highly reviewed reference code in favor of some adhoc multi-system implementation.

That said, the coldcard's software is based off the trezor-crypto codebase which has already been crapped up with altcoin support, and is objectively worse off for it... so they don't get the full benefit here.

Supporting altcoins also inevitably means supporting extremely sketchy projects and their participants-- Different people can draw the scam line in different places but "we support just the altcoins we think have merit" is just a receipt for customer support headaches and constant demands to support more stuff, and eventually crossing whatever line you hoped to draw. "Only Bitcoin" is a crisp, clear, defensible line, that saves you from distraction, saves you having to work with creeps or scams, and doesn't require constant debate or justification.
