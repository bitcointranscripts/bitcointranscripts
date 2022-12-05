---
title: Liquid Censorship Resistance
speakers: ['Greg Maxwell']
transcript_by: Michael Folkson
date: 2020-06-08
---

Location: Reddit

https://www.reddit.com/r/Bitcoin/comments/gye0yv/liquid_censorship_resistance/ftcllcm?utm_source=share&utm_medium=web2x&context=3

# Is Liquid censorship resistant?

Liquid isn't particularly censorship resistant. If someone tells you it is they're confused.

Back when I worked at Blockstream there was thought in the design to mitigate some of the risks: make transactions difficult to identify, even the peg outs use a ring signature to authorize them, and Blockstream should have no ability to change the software in use (instead, they'd have to convince each of the functionaries to run replacement software if they wanted it deployed-- and the software is open source). At some point engineering made a tool that would analyze a proposed membership and work out the implications of geopolitical correlated failures. The system was designed to hide the operating locations from the functionaries from each other. But like other multiparty system's its still centralized even though the centralization is distributed, so countermeasures can only go so far. The reason it has them is because the centralization makes them all the more important, but it doesn't make it non-centralized. [To be clear, I have absolutely no operating knowledge about Liquid-- I left Blockstream before it was in production and things could have changed after I left.]

For Bitcoin, Liquid is an alternative to straight up exchange custody and has some potentially useful security trade-offs compared to that. But if you wouldn't leave bitcoins with an exchange then they probably shouldn't be in Liquid either, because even though there are probably countermeasures it's probably impossible for any of us to validate that they're actually in place and working or reason about their implications.

One of the things that frustrates me about this space though is that some of the same people who go on about liquid not being censorship resistant are happy to promote extremely centralized altcoins or single point exchanges which are no better.
