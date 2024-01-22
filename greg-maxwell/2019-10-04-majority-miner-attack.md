---
title: "Should we be more concerned by the prospect of a 51 percent mining attack?"
speakers: ['Greg Maxwell']
transcript_by: Michael Folkson
tags: ['mining', 'security']
date: 2019-10-04
media: https://www.reddit.com/r/Bitcoin/comments/ddddfl/comment/f2g9e7b/?utm_source=share&utm_medium=web2x&context=3
---
I think questions like this are ultimately the result of a fundamental lack of understanding about what Bitcoin is doing.

The problem Bitcoin is attempting to solve is getting everyone everywhere to agree on the same stable history of transactions. This is necessary because in order to prevent users from printing money from nothing the system must have a rule that you can't spend a given coin more than once-- like I have a dollar then pay both alice and bob that dollar, creating a dollar out of nothing.

The intuitive way to prevent that excessive spending is to decide that first transaction that spends a coin is valid and any additional spends are invalid. However, in a truly decentralized system "first" is actually logically meaningless! As an inescapable result of relativity the order which different parties will perceive events depends on their relative positions, no matter how good or fast your communication system is.
So any system that needs to prevent duplication has to have a way to artificially assign "firstness". Centralized systems like ripple, eos, iota, blockstream liquid, etc. just have a single party (or a virtual single party) use its idea of whatever came first and everyone else just has to accept its decision.

A decentralized system like Bitcoin uses a public election. But you can't just have a vote of 'people' in a decentralized system because that would require a centralized party to authorize people to vote. Instead, Bitcoin uses a vote of computing power because it's possible to verify computing power without the help of any centralized third party.
If we didn't have the constraint that this system needed to work online, then you could imagine an alternative where consensus could be determined by people presenting large amounts of some rare element. ... but you can't prove you control osmium online, it appears that computing power is the only thing that can work for this purpose online.
When people talk about "51%" all they're really talking about is people rigging that election, so that they can override what everyone previously thought was the accepted order of transactions with a new order that changes some of their payments from one party to another.

With this understanding maybe you can see that the concern doesn't even depend on a single person having too much of the hash-power. The attack would work just as well if there were 100 people each with an equal amount and a majority of them colluded to dishonestly override the result.

Also, any mechanism that would let you prevent one party (much less a secret collusion) from having too much authority would almost certainly let you just replace mining entirely. The only known way to do that is to introduce centralization and if you're willing to do that it's trivial, if you're not it appears impossible. People have cooked up 1001 complicated schemes that claim to do it without introducing centralization, but careful analysis finds again and again that these fixes centralize the system but just hide the centralization.
I think people obsess far too much about "51%"-- it has some kind of attractive mystery to it that distracts people. If you're worried that someone might reorder history using a high hash-power collusion-- just wait longer before you consider your transactions final.
A far bigger risk to Bitcoin is that the public using it won't understand, won't care, and won't protect the decentralization properties that make it valuable over centralized alternatives in the first place. ... a risk we can see playing out constantly in the billion dollar market caps of totally centralized systems. The ability demonstrated by system with fake decentralization to arbitrarily change the rules out from under users is far more concerning than the risk that an expensive attack could allow some theft in the case of over-eagerly finalized transactions.

There is really two classes of things that that colluding majority can do:
	•	They can undermine the stability of consensus, e.g. making continual reorgs against the tip (though to do this successfully over a realistic time frame they need a lot more than 51%). After some brief transition where some active transactors might get robbed by the attackers before everyone realizes the consensus isn't stable, this turns into a network wide denial of service attack that essentially delays all use of the system.
	•	They could censor particular users or uses, creating an immediate denial of service against those users/uses.
The first of these is less concerning to me because since it effects everyone and makes the system much less usable it's pretty clear that the users will resolve it somehow, e.g. potentially with a nuclear option of firing the miners by changing the work function. Because of the inevitability of that outcome it makes the whole attack fairly unattractive from a game theory perspective.

I find the second more concerning because since it targets a subset it may be much harder to gain the political will to undertake a costly or risky fix, especially if the targets are somehow politically or legally disadvantaged.

This is a major motivation behind many Bitcoin developer's interest in privacy/fungibility: Sure, we also care about financial privacy for its own sake as a necessary contributor to other widely recognized human rights ... but making transactions from different users and use-cases more indistinguishable makes that weaker point of the system much less exploitable. If some malicious or coerced consortium of miners can't distinguish transactions they can't target a subset to censor.

It's also another reason why some kinds of second layer systems are important-- if users could continue transacting bitcoin value without interruption even while censorship or instability is causing multi-day delays in confirmation then the incentive to attempt such an attack is greatly reduced.

Likewise, it's part of the reason that many care about node operating costs. Keeping it so that Bitcoin could keep reliability operating underground over covert blocking resistant channels is a reason it doesn't have to. If someone thought they could kill Bitcoin by forcing it underground there would be a lot more incentive to try it, but if that happened today it's likely that it would convince people that its unkillable.

Both of the above attacks in their denial-of-service form also only hurt as long as they go one, applications which don't mind massive delays probably don't care too much about them.
Often when people talk about security in the context of computers they get caught into the trap of absolute security. With basic computer security and cryptography it's realistically possible to build systems which have effectively unbreakable security. Where unbreakable is economical it should be the goal. But when you talk about physical systems, social standards, or decentralized consensus it appears that strong-sense unbreakable security isn't realistically possible-- and that doesn't mean the result is insecure, it means that security needs to arise out of a balance of costs, risks, and incentives. There isn't such thing as an unbreakable bank-vault, but there certainly is such a thing as a vault where the cost of breaking it isn't worth the pay-off or where the time to break it almost guarantees that an attacker will get caught.


