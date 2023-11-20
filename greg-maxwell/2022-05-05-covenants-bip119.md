---
title: Covenants and BIP119
speakers: ['Greg Maxwell']
transcript_by: Michael Folkson
tags: ['covenants']
date: 2022-05-05
---

Location: Reddit

<https://www.reddit.com/r/Bitcoin/comments/uim560/bip_119/i7dhfpb/>

# Covenants and BIP119

I was asked by an old colleague to respond to your post because I came up with the term covenant as applied Bitcoin many years ago back when I was still a Bitcoin developer.

> does bip 119 completely mess the fungibility of bitcoin. If the idea of covenants is that you can create bitcoin that can only be sent to certain addresses, doesnt that make two classes of bitcoin?

No. That's disinformation which, ironically, appears to be created and promoted by the creator of BIP119 as a strawman.

You're only paid in bitcoin if their payment exactly specifies the terms determined by your address. If they do, then the funds are yours free and clear (or otherwise covered by terms you agree to), if they don't you'll never see the payment at all.

For example, imagine I owe you money. Well it's possible for me to go dig a hole in my back yard put some money in a tupperware container marked "TO: Ok_Aerie3546" and bury it up. Has the fungibility of the dollar been compromised because I stashed some under unreasonable conditions? No: You just haven't been paid!

The author has also promoted some conspiracy theories about "KYC bitcoin"-- like that people might be coerced into accepting encumbered bitcoins that could only be spent with government approved counter-parties as a transparent excuse for the gratuitous limitations of 119, but this too is obvious nonsense: If someone wanted to attempt that plain old multisignature would suffice to accomplish that (and because MPC ECDSA exists, it couldn't be blocked even if multisig were blocked in bitcoin!). What prevents that is that people won't accept it, and anyone trying to impose it on you when they owe you funds would be guilty of theft, plain and simple. (and you can wag your arms and say 'but what if a government tries to engage in theft' -- well that's always a possibility: they have the tanks and jails, after all).

I think BIP119 is a poor proposal being pushed through in an ill advised way, but I think the concern you're raising isn't a legitimate one.

I regret ever introducing the term covenant. My intent was to point out that it was inevitable that any sufficiently expressive rules could allow for encumbrances that ran with the coin, and as a result one shouldn't generally accept encumbered coins unless you are extremely sure of what you are doing. Fortunately, there is no risk of doing so accidentally. Just like the example with multisig shows it's already possible to create persistently encumbered coins and it's fundamentally impossible foreclose that possibility through technical means. The protection from it being a problem is already built into every single wallet out there: no wallet will accept/display a payment except under terms set by itself. So the only way anyone could 'force' you to accept some encumbered coin is the same as their ability to just not pay you at all as they're the same thing. Simultaneously, there are plenty of extremely useful, pro-security, pro-privacy, pro-autonomy ways people could conceivably temporarily encumber their own coins... sadly almost none of them are enabled by bip119.

If you're concerned about fungibility, go bother exchanges and minining pools that lock users to withdraw to a single address or don't support all common address types thereby denying users their choice of payment rules.
