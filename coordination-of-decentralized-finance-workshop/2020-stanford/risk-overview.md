---
title: Overview of Risk in Decentralized Financial Systems
transcript_by: Bryan Bishop
speakers:
  - Byron Gibson
date: 2020-02-18
---
<https://twitter.com/kanzure/status/1229878346709782528>

# Introduction

This is an overview of catastrophic failure risk in decentralized systems. There are certain degrees of risk in this system where losses can be moderate but not entirely destructive, but also potential failure modes where losses can be serious and ruinous equivalent to the global financial crisis.

From a regulator's perspective, there's a couple of primary mandates that regulators are tasked with making rules for. One is consumer protection, another is financial transparency and accountability, money laundering and sanctions and terrorist funding, and organized crime, and then there's safety and soundness.

For this talk, I want to talk about soundness of financial systems.

# A question for the cryptocurrency industry

The traditional financial system has evolved over a period of roughly 300 years. It has evolved in an unplanned and organic manner. It's built to provide certain services based on the tech capabilities of the time. As problems arised, these were addressed and fixed and repeat that process for 300 years. It's a complex system with emergent behavior.

There's normal boom-bust cycles that we have become accustomed to. They are largely understood and socially tolerable, but Global Recession and similar events are abrupt, acute, and socially intolerable because the losses caused by these are simply too great.

It's also difficult to change or reform the current financial system because so much already depends on it. It's the platform on which most of the economy runs.

The question for the cryptocurrency industry is that since this is a new industry, and two since this is based on software, is it possible to intentionally design a blockchain-based financial system which is significantly less prone to financial crises and collapses than the traditional financial system? There's a lot of different components to answering this question. It starts with understanding what are the sources of systemic failure risk.

# Sources of risk in decentralized financial systems

One of the sources is cryptography: Dan Boneh, head of the Stanford Center for Blockchain Research, said one of his favorite things about cryptocurrency is that new cryptography is getting deployed and experimented with quickly. By comparison, when it comes to deploying new cryptography to the internet, it takes 10-20 years for that to happen, for the cryptography to get vetted, understood and to the point where all the decision makers are reasonably confident that it's solid and that it doesn't have flaws or subtle bugs. Whereas in cryptocurrency industry, it's been highly experimental and still relatively limited in its user base, and yet new cryptography is being deployed constantl.y It adds a lot of value, and there's new risk, but that's the way the industry is. When we're thinking about identifying sources of systemic failure risks, cryptography is one of those.

The second one is the overall architecture or protocol of these systems. How can consensus be broken by malicious attackers or accidentally? What happens when the architecture of these systems breaks?

Finally, there's financial and economic failure risk. This is something that has been less worked at than the first two until very recently. I believe last year was the first time I noticed-- people like Tarun Chitra-- studying cascading failure risk in the financial and economic side of these systems. A professor at Cornell is also studying this. We hope to have her here but unfortunately she couldn't make it. Until last year, there wasn't a lot of sophisticated financial engineering or analysis of how the systemic risk works.

# Cryptographic risk

The problem with building cryptosystems... and this is largely borrowed from a 2015 Andrew Poelstra presentation..  that these systems are difficult to build, maintain and secure. In cryptography, there's no range of severity of errors. Cryptography is "it either works or it's broken" and any subtle flaw could result in a total breach of the system. In cryptography, there's zero tolerance for any kind of defect.

Also, cryptosystems are subject to active opposition. You have clever, adaptive adversaries attempting to break it and steal all the money from it.

Failures in these systems tend to be catastrophic, and you usually don't notice until after the damage is done and money is stolen or burned. There can also be a high variance time lag between the time that a bug is introduced and the time that the system is breached, and you might not realize it until someone smarter than you finds the flaw and exploits it.

Permissionless cryptocurrency is an anonymous bearer asset meaning whoever controls the keys controls the asset, just like a physical bearer asset. If the thief steals it, it's difficult or impossible to undo the theft and clawback.

Blockchain represents a restructuring and replacement of core infrastructure, rather than building on top of tried and true infrastructure. When you combine these risks togethre, this is the engineering and architecture problem that we're faced with in the industry.

# Architecture and protocol level risk

Cryptography components along with consensus systems and other engineering components are put together to make a cryptocurrency system. The cryptographic primitives have their own set of challenges, as discussed. The system as a whole also has its own problems as well. The bitcoin community has lists and lists of different types of attacks against the consensus layer, with all kinds of different names like timewarp attack, 51% attack, withholding attacks, etc. These are all ways that the system can be broken, that a malicious attacker can cause the system to catastrophically fail.

# Financial and economic risks

One of the ones that Tarun has just talked about this morning is "compositional risk". In the traditional financial system, you can make derivatives of derivatives of derivatives. The compositional risk of how these things become increasingly complex is something that we're starting to pay more attention to.

There are also monetary design considerations as well. Stablecoins have been a big topic for the past few years. There's a philosophical question here: are stablecoins truly stable? The philosophical question is, in complex systems it may be impossible to control the variance.  You can maybe create an impression of control or impression of stability, but what you're doing is building up greater volatility or blow-up risk over time. It's essentially like a volcano which looks stable for a long time, until it explodes all of the sudden.

Finally, there's the base money of cryptocurrency systems itself. Ethereum has its base money of ether and then there's tokens built on top of it. The monetary system design of the base money is still something that the industry is early stage on, and there's probably a lot of exploration of different monetary systems coming over the next 10 years.

# Conclusion and discussion

Do regulators think about these questions? I'm aware that central bankers do, but what about the others? How can the industry be helpful in thinking about analyzing these problems and challenges?

Q: If I was a regulator, or at the world economic forums, we often talk about the Financial Stability Board... for me, a cheat sheet on the key issues that is maybe-- with input across from academic and blockchain ecosystem... would be really useful.

A: I'd be happy to work on that. One of my concerns is that I have seen, and I don't know for sure, that central banks are looking at this technology and I would hope that we're able to very clearly understand the challenges of deploying this stuff at the level that central banks operate at, before rushing headlong into it. PBOC has announced that they will be creating a digital currency.

Q: So what are the issues, the different types of attacks... if you can make that, please send that to me and the OECD. I try to map the regulator and oversight bodies.

Q: What if protocol designers are not interested in some of those questions? For example, economists warned that bitcoin's deflation schedule would be disastrous. I don't think that outcome has really happened.

A: I think their prediction was that not quite catastrophic things would happen.

Q: So is the prediction that transaction fees would go up?

BB: Yes, and I think high transaction fees would be good.

A: Yeah a lot of things in bitcoin are counterintuitive like that.

Instead of creating value, how do we prevent major harm? That is a way of creating value, obviously. This is a question for the financial guys. What is the regulatory perspective on soundness in general? How does this fit into the mandates that regulators have to think about? Are there things that regulators could use help from the cryptocurrency industry?

The two discussion groups will be, one is putting together a checklist for regulators to review. Bryan understands the protocol risk side really well. Those sound like good subgroups.

Q: In the law school, we have a center for informatics and one for blockchain law and policy where exactly these questions are open for debate and contribution. You write an essay, it gets peer reviewed, but that was the intention of the Blockchain Law Journal.

A: I think they are going to leave some of the journals out during the main conference.

Q: Are these types of forums where you are seeing the most productive conversations where we're engaging multiple stakeholders from regulators, industry and development? Do we need to evolve these conversations or are you confident that authorities outside this room and regulators are seeking the right inputs to make those decisions?

A: Good question. I know these conversations are happening in subcommunities. The soundness discussion happens among the protocol engineers, but I'm not sure if it happens at a broader level or within the regulator communities.

So I suggest long-term stability of decentralized system has two aspects: economic stability, and the other is technological stability. So let's divide the two groups that way. So one will talk about economic stability, and the other will talk about technological stability.

These transcripts are <a href="https://twitter.com/ChristopherA/status/1228763593782394880">sponsored</a> by <a href="https://blockchaincommons.com/">Blockchain Commons</a>.


Tweet: Transcript: "Overview of risk in decentralized financial systems" https://diyhpl.us/wiki/transcripts/coordination-of-decentralized-finance-workshop/2020-stanford/risk-overview/ @byrongibson @CBRStanford #SBC20
