---
title: Useful Proof Of Work 
date: 2020-07-05
speakers: ['Greg Maxwell']
transcript_by: Michael Folkson
---

Why can’t hash power be used for something useful?

Location: Reddit

https://www.reddit.com/r/Bitcoin/comments/hlu2ah/why_cant_hash_power_be_used_for_something_useful/fx1axlt?utm_source=share&utm_medium=web2x&context=3

# Why can’t hash power be used for something useful?

There is a general game theory reason why this doesn't work out:

Imagine that you are considering attempting to reorder the chain to undo a transaction. You could decide to not attempt the attack in which case your cost is just the payment you made, or you could attempt the attack in which case the cost is the energy you put into the plus the cost of the payment times your odds of failure. Attacking makes sense of the second figure is less than the first.

If you imagine that the proof of work is perfectly useful and efficient, the energy you put into the attack is perfectly matched by the external pay-off of doing that work-- so why not attack? it's free!

Of course, no system would be likely to be perfectly useful or perfectly efficient, but this analysis shows that the security comes only from the part of your work that was put at risk-- in other worse, only from the part that someone might call a "waste" if they disregarded the very real value of securing Bitcoin.

Game theory aside, it's also the case that "useful" problems almost never make for good proof of work: proof of work has to be uniformly hard and there must be a way to smoothly and predictably vary the difficulty, it must be extremely cheap to verify, it must be generally free of short-cuts or approximations, or any way to make progress (work that makes future work easier). Few things that people would normally call useful meet these requirements.

Instead: I'd like to point out that Bitcoin mining is useful: It makes Bitcoin secure. We don't generally expect our other security measures to do double-duty in entirely non-security ways. No one expects their padlocks to cure cancer.
