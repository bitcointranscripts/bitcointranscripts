---
title: Are We Too Late for Privacy?
date: 2024-11-19
---

## Discussion Points

Is speculating on market behavior in scope? Would it matter if people adopt privacy tools regardless, or would people avoid privacy regardless?

- Wants to work on privacy tools that achieve PMF (Product-Market Fit) and substantially move the needle.
- Wants to know if there’s a use for ZK (Zero-Knowledge proofs) in privacy on Bitcoin.
- Doesn’t think it’s too late. Suggests coming up with a list of privacy improvements.

We’ve seen plenty of ideas in other systems; also concerns (e.g., auditability, bugs, regulatory scrutiny, and chain splits) related to such concerns.

There have been developers arrested for working on privacy. Wasabi had to do chain analysis (did it voluntarily).

**Topics**

- Adoption mechanisms
- Regulatory constraints act as headwinds for adoption
- Solutions that need a fork
- Solutions that work today

**Claim:** Even if Layer 2 is private, leaks on Layer 1 must still be addressed.

- In Zcash, most coins/transactions are still transparent.

**If we could do one thing, what would it be?**

- O(1) accumulators: UTXO sharing with O(1) exit costs.
- A ZK verifier would enable building any kind of privacy protocol on Bitcoin.

**Is Lightning a good solution for privacy?**  
Sometimes; it depends.

- What existing solutions are worth investing in to improve?
- Many are complementary; for example, combining CoinJoin with opening a Lightning Network channel.

**Goals**  
Users should have a diversity of tools to defend against a range of threat models.

- Improving privacy on one dimension may involve tradeoffs in others, e.g., privacy against counterparties vs. privacy against the public.
- Can existing solutions “upgrade” to stronger privacy with a soft fork, e.g., CoinJoins to CoinPools, Lightning Network to Ark (LSP to ASP)?

**Consideration**  
Would the existence of strong privacy provoke stronger regulations?

- Adoption of imperfect privacy tools can lead to general support for and optimism about privacy by making it more common.
- Privacy tools used to save money might appear more acceptable to regulators.

## Where Do We Go From Here?

- Piggyback on existing privacy laws to promote Bitcoin privacy.
- Gain better clarity on which laws/regulations apply to developers and specific types of software.
- Be able to measure privacy (on-chain and off-chain).
- Compose existing privacy solutions.

## More Takeaways

- Enable (practical) ZK verification in Script.
- Develop O(1) accumulator that is able to economically and provably exit.
- Create privacy metrics.
- Make privacy visible and attainable:
  - Allow users to see their own transaction score.
- Onboarding to privacy must be easy
  - Do it by default, low cost
- Build compliance tools that provide the bare minimum and push for asking “why?”:
  - Leverage ZK?
