---
title: Consensus Protocol Risks And Vulnerabilities
transcript_by: Bryan Bishop
tags:
  - cryptography
speakers:
  - Bram Cohen
date: 2020-02-19
---
<https://twitter.com/kanzure/status/1229906447808360450>

# Introduction

I am going to talk about why cryptocurrencies matter. I am going to take the skeptics side. I am going to start from a banker's standpoint why a lot of the things that cryptocurrency people land say don't make any sense.

# Where are the engineers coming from?

An engineer will look at something like Visa and say this is horrible. These are systems from 50-100 years ago. It's not using public key cryptography, it's not using secure hashes. It's a disaster and I can build something better. So they prototype something that is objectively better, and if everyone was using this then the world would be more secure, and this is a low bar given the technology used in the financial sector today.

So they built a great thing- and then they are told, you can't just setup shop and that's against the law, and then the engineer rails about how regulators are holding back technology. That's where the engineers are coming from when they go on these triads.

# Regulations aren't evil

The problem is that engineers are missing a few hundred years of experience. We tried unregulated banking in the 1800s and it did not go well. There were crises every 10-15 years, they kept happening. If you're a banker, there's a straightforward business model of "oops we accidentally your whole account" and that's an effective business model if you're a banker, much easier than doing real work. More recently, the shadow banking sector- these things that were effectively acting as banks even though they weren't called banks- de-regulated themselves. There's some huge fraction of all tech in the finance industry is obfuscating leverage. It's taking leverage, and the math is making it disappear from the books. It's not gone, it's just gone from the books. This causes the whole system to be leveraged up again, and then we had another banking crisis.

And then you have this general problem that if you start de-regulating it, you don't get engineers coming in and building stuff. You get some of that. But mostly you get scam artists coming in. Any random scam artist can make a product with a huge checklist of features that are amazing that they don't have to build, and engineers are by comparison hobbled by their actual quality rather than the scammer's self-reported quality. So this doesn't work, you can't just de-regulate.

# Regulations are still getting in the way

So what is the core of our issue here? What is the fundamental issue with de-regulation? The real issue is that you need a trusted third party. If you have a trusted tthird party, it would be better for it to be vetted and subject to punishment if they do something bad, rather than some total random that a reputation system is supposed to manage. Trying to get rid of this TTP is extremely difficult, and if you wanted to do this, yo uwould need a secure distributed database.

How can you have a database that tracks how much money everyone has, without people being able to spam the system with fake peers and change people's balanceS? How is this supposed to be made to happen?

It turns out that we can. Bitcoin does this. It has some problems. But it legitimately does in fact implement a secure distributed database.

# Bitcoin feels like a step backwards

Bitcoin has a lot of problems. When people are working with bitcoin.... bitcoin has some big improvements. It brings in public key cryptography, which is a low bar- it's absurd that we're not already using it everywhere... Bitcoin uses public key cryptography, secure hash based histories. You do this thing where the bank has a blockchain group that is supposed to be doing blockchain stuff, and they decide their job is to make the bank use secure hash based audit trails which isn't blockchain but a huge improvement, so I'm glad they are doing it. They should have done it 30 years ago, but I'm glad they are doing it now even though it has nothing to do with blockchain.

Bitcoin's problem is that it feels like you're carrying around suitcases full of $100 dollar bills. Banks do provide security features. They have ways of slowing things down and reversing mistakes which makes things significantly less scary. However, they do it completely opaquely. They just decide how it is going to work. You as a retail customer of the bank gets no say in this. The bank makes their decisions about processes, and they won't tell you their decisions or what they are, they just do these things for you.

But they're doing it better than bitcoin does today. However, it doesn't have to be this way. Cryptocurrencies can in real pragmatic terms do this better, like with appropriate smart transaction functionality, these cryptocurrencies can have these same security features in a transparent way and under complete end-user control.

# Payment security feature example

You could have a wallet that only pays to authorized payees. This is common in organizations: there are vendors and employees, and you don't want employees to be phished or embezzling money. You want them to have permission to make payments, but only to those vendors.

You want something where you have a wallet and it can spend but only at some rate, and if it spends quicker than that rate then it is stopped from doing so. There's some way of going back and saying oh there was a problem, I'm going to clawback everything using this other procedure like getting a key out of cold storage, and I walk into a bank and do it, or something like this. This helps you fix things when you get hacked.

On the flip side, what about having recovery material on a piece of paper, but you're worried about that piece of paper getting compromised. So you can have a system where what's on that piece of paper allows you to do a recovery process. If someone steals that key material, or someone gets access to it, and starts a recovery process, then you can stop it. It's the opposite side of a ratelimited wallet.

These are examples of the kinds of things that banks do today, but badly and without end-user control, and these could be done better in cryptocurrency.

# More thoughts

What happens if the government wants to seize your funds? They go to the bank and seize the funds. In practice, what does it really mean? If you have cash, then government can decide to seize your cash, and then they have to go do it. Cryptocurrency is more like physical custody of your cash and nobody can magically spirit it away from you. In principle, we could have a regulatory system where the government could figure out the serial numbers on the bills you have, and then prevent you from spending the dollars, but thankfully this is not the system we have today. The requirement of saying "the government can take this" is actually vague. When people build backdoors for government, these turn out to be huge security holes in the system and you have people fraudulently use them, you have government agencies get compromised, you have government officials being abusive. In MtGox, the police going after it outright pocketed and stole money. Having real audit systems in place there, is in my view not a bad thing.

Crypto does one thing very differently: it's absolute. Maybe at the heat death of the universe you will crack the key. But in general you won't get that. You combine that with the first amendment, and you have a regulatory regime where trustless trust can't really be stopped. This is one of the fundamental changes that a blockchain with Nakamoto consensus creates. The government only has a few things they can do to stop you: they can stop you from publishing the source code, they could say you can't run it but frankly it's hard to stop you from running software at home. It becomes hard to control the core capability of wealth storage and transfer. Once that's the case, you have to regulate with that assumption in mind. Tangibly, I wanted to launch a digital cash in 1998 and my now-wife said "you mean I'm going to be stuck on a carribean island with armed guards and never be allowed back to the US?" Yes, that was the case then, but Nakamoto's core change was that it was trustless trust: you don't have to trust him for the network to continue to work, even if he gets shot and killed by the Marines.

People jump way too quickly to this whole question of "what can regulators do to you as a consumer". When it comes to banking, you first and foremost need to secure the customer's funds against thieves. That's several orders of magnitude bigger than a problem than anything interacting with a government whatsoever. Just in terms of value to society and costs to them, and costs even to the police and people who have to help with this thing, you get tremendous benefits just from doing that job properly. So that should be the first priority of what you do. Things I have talked about in this presentation have given examples of how to do these things much better.

How about one discussion about the responsibility among stakeholders in the ecosystem. How about community-based regulation that comes from the community itself, self-regulation, versus having a third-party come and enforce a regulation.

There are plenty of places to do regulation in the cryptocurrency space. There are things that claim that they are decentralized and then hard-fork all the time. If someone is a software vendor, then they have a responsibility to not jack customer funds when they do that. It looks like there's lax enforcement of rules against people doing things they really shouldn't be doing, and it is directly hurting consumers. Outright fraud and thievery.

Q: What are your thoughts on on-chain governance and ability to upgrade these protocols as we learn new mechanism design constructs and whether to continuously improve the system?

A: There's a question as to what you mean by on-chain governance. All too often, saying on-chain governane is this euphemism for "actually this is a centralized system" and I don't think you should be able to have it both ways. It should either be a decentralized system, or it shouldn't. If you're trying to have it both ways, then you should start having responsibility for things that happen.

Central third parties as mandates by the general public (e.g. for fingerpointing in the event of financial catastrophes in the public markets, or having someone "responsible" for regulating crashes out of existence), versus what should be offered to the general public instead? Ratings agencies? Regulatory oversight and regulatory sandboxes? Regulations shouldn't be about ordering people around, but really helping with coordination and engineering and things more like NIST standards.

With tor, people have mixed feelings about tor. The government funds Tor. In practice, Tor is mostly - it appears to be mostly used by people who are either behind somekind of firewall either government-wide or employer-wide or school-wide and the firewall is just getting in the way of normal things they want to get done, and not the darknet things that the general public associates with it. So how do we feel about privacy coins? If you have proven you have control of funds, then you now have responsibility over those coins, and you shouldn't be able to have it both ways. The trend is inevitably moving towards when you do upgrades they are in the presence of general purpose functionality, simply because upgrades are so painful.

Q: Could you elaborate on your NIST comments?

A: Sure. Cryptography predates cryptocurrency by a long time. Government agencies like to take a cloak-and-dagger approach telling you what to do with cryptography, in the early days, and that didn't work really well. These days, the relationship between academic cryptographers and cryptographers working in industry, and cryptographers working for government, are mostly collegial relationships. NIST is the National Institutes of Standards and Technology. A lot of the cryptographic primitives we use, including AES and SHA-2 straight out of the NSA either came from the government or the government shepherded them forward. The traditional view was that you have to put backdoors into everything, but it turns out that's a disaster and makes everything insecure. It's more in the government's interest so that people aren't being stolen from all the time. Using actually good, standard, interoperable cryptography is important. So the governments mostly just been helping with that process for the past few decades. That's been the main things.

Q: What about regulatory sandboxes?

A: I would like first for regulators to stop scam pump and dump companies. That would be appreciated, as step one, before we get into anything else. I think there's precedence for things like blockchain. The Fed Wire system has these rules... and if you get scammed on the FedWire system, then even though this is a government-run database, you can't go say hey I got scammed give it back to me. As far as they are concerned, the money has left your hands and it can't be undone. It's done that way because the burdens of trying to do it any other way are just totally impractical, and at some point you need a database that actually means something. That's obviously an extremely regulated system. We do have precedent for things that look like cryptocurrency, and it mostly has to do with people's relations with each other, that you're not allowed to cheat other people in the system and there are responsibilities and liabilities for things that happen there.

Q: Is there a feature of digital currencies, for you, that would represent a quantum leap from finance 1.0 to finance 2.0? Is there something significantly missing? Or innately digital currencies already take us to finance 2.0?

A: Digital currencies today don't take us to finance 2.0. It's important to be clear about this. Cryptocurrency doesn't change the nature of leverage. If you loan someone money, you're taking risk and that hasn't changed. If you loan someone money, they need to be vetted. Cryptocurrencies don't help with that. What cryptocurrencies help with is clearing and payments and doing those things better. Then you can start layering things on top of that, like talking about the identities of the entities in the system are, but even the most base level thing is like-- it's hard to understand how much room there is for improvement. If you have ever sent an international wire transfer, it's so so unbelievably sketchy. It's a scary thing to go ahead and do. It costs a lot of money, takes way more time than it should, and there's a lot of international wire transfer fraud happening in the world. Just making those systems follow 20th century practices would be a hugely valuable thing itself, and should not be understated.

Q: But that isn't solved by cryptocurrency?

A: You can't just say the word cryptocurrency three times, tap your heels and have it magically happen. What cryptocurrency can do is allow for processes that make this a lot easier. If you want to be able to make payments that happen internationally, between countries, with well-defined security processes about how these have to happen and knowing what the ceremonies hav to be to actually do it, and low probability of there being some accidental screw-up along the way. Cryptocurrency with some enhancement to smart contract capability they have today, can totally do that, if you're transacting with cryptocurrencies, but there's a lot more things to build. Building these processes needs to be done, and making it better than the existing banking system.

Q: I am trying to think about how blockchain where exactly it helps with cross-border payments. I keep coming up across frictions that I don't think blockchain solves. I'm not a payment experts. One is, foreign exchange transaction fee is still going to exist.

A: Sort of. One of the problems with cryptocurrency is that they are their own thing. You do have to have some floating exchange rate between a cryptocurrency and other things. You can also use stablecoins, and banks could issue their own stablecoins. If you have a reasonably well-trusted ledger that can actually get you many of the benefits of cryptocurrency while allowing you to basically stay within a single currency, and not have to pay exchange rates on that.

For remittances, what's happening is that they are using Amazon gift cards and it's only slightly more expensive than Moneygram. But the advantage is that you can do this from home. So remittance crypto companies are finding that once you find someone in your local area, you just go back to them again rather than the market.

You don't want to use correspondent banking, becaues you don't want to tie up the capital. Not all banks agree on what banks are okay to transfer money with. With cryptocurrency, you get the benefit that you can define what processes will be followed to get the funds from point A to point B. As long as you have a system based on trusted third parties, it's always going to be hobbled.

With central bank digital currencies, with or without blockchain, can remove the need for correspondent banking, if they allow foreign banks to hold accounts with them. So then you have one ledger, and they are able to credit and debit the two parties without the need for a flow with correspondent banking. This could be done with blockchain and decentralized ledger... Nobody really cares it's a ledger, but you care that the value has been transferred in a way that cannot be reversed. Censorship resistance matters because your local thief is a freedom fighter in Hong Kong, which might violate local law. Once you have local law on your bi-party or tri-party ledger, it starts to look interesting economically and from a risk perspective to have trustless trust. Banks can also work towards not getting left behind in the long run, by making lightly trusted local ledgers, as the tech improves for doing things on top of cryptocurrencies, just make them do the same things verbatim, and they just publish the state... so if you trust us, this is going to be pretty fast and have a high transaction throughput. This would be a reasonable thing for banks to start doing, and it would be good for the world. The smart transaction systems aren't really there yet, but they are getting better. Also, banks aren't exactly known for being ahead of the game on these things.

Q: What are some things that developers and regulators don't see eye-to-eye on?

A: Developers tend to not think too much about regulators. I don't know what regulators think.

Q: They think about risk and what could go wrong.

A: The things that developers spend their time worrying about- we don't tend to worry about getting charged with something nefarious by securities regulators, because they're not even charging people that are doing things that are actually egregiously illegal right now. What keeps developers up at night is the fear that AML/KYC will start applying to like everyone, like anyone who does business with anyone on their system will have to start doing AML/KYC with that other person, and this would hobble the whole system. It would seem that if you go buy something from someone in the street, you exchange cash and you're done, and it seems like the same rules should apply to cryptocurrency but there's been rumblings and motions and making it so that these extremely onerous regulations would apply to anyone transferring anything to anyone else, which would be extremely frictional.

Q: What about the principle of privacy? This is explicitly related to AML/KYC.

A: That one varies a lot. There's this myth that bitcoin is very private. There's this idea that bitcoin is very good for money laundering. Which actually, it's not. Bitcoin is terrible for that. Partially this myth was promulgated by the FBI was publicly stating that bitcoin is super private and we can't do anything about it and people are laundering money through it constantly.... and they got away with this for a while, they managed to bust a lot of stupid people by convincing them to do their nefarious activity on bitcoin. But there are privacy coins, which are slightly different animals. There are significant technical disadvantages to doing a privacy coin. It's harder to make anything work, they are much less auditable, they are much less scalable, there's lots of headaches and even more technical issues unlisted here. Most of the focus in the space is not in privacy coins right now, just on these things that are very public and auditable and mostly just good at moving funds from point A to point B and not good at giving privacy to them. I personally don't view privacy as an unalloyed good, it's a complicated thing. The privacy questions are more the focus of the people who are into privacy coins and everyone else is pretty happy to say why don't you go argue with those people if you really care so much about that topic.

Q: So you said developers don't really think about regulators... but do they have at least some notion of what regulators have especially with respect to the financial system? As a former central banker, I know they hate the notion that developers in this industry just want to move fast and break things.

A: That's not a bitcoin thing. That's an ethereum thing. Bitcoin Core developers are extremely careful and conservative about how they do things and have very very negative views of the ethereum ethos of behaving that way.

Q: Okay. In general, do people realize that the regulators are the ones that have to pick up the pieces when things break?

A: Developers are a diverse lot of people. Most of them don't know any regulators. The different development groups have their own cultures within them. A lot of the... the more serious developers in cryptocurrency who are building things and aren't scam artists, are saying, could the regulators go after the scam artists please?

A: Some developers just don't care about the market consequences... they want to protect their users, but they don't feel responsible for systemic stability of the whole market, only for what they produce.

A: In the cryptocurrency space, there's a lot of projects that spout a lot of technical mumbojumbo that is just gibberish. There's other projects that spout technical mumbojumbo that isn't gibberish, but you need to get deep in the weeds to figure out who is saying nonsense and who isn't. The problem is that the smart friends that people go to also don't know. So you have this second level thing... you have to figure out which of your smart friends are capable of figuring out who to trust, it's one level out, and it makes it hard to sort through the general space of who are the scammers and who aren't.

Q: Right, but smart friends can also be catastrophically wrong. This is true across the board.

A: The amount of crank economic theories spouted everywhere is really crazy. It's hilarious that you get these situations where you get people spouting the theories of Karl Marx calling the fans of Milton Friedman socialists... There's public massive disinformation campaigns about finance and so on, and there's obviously a lot of financial gain to benefit from the general public being very confused. This is not just a problem in cryptocurrency; this is a problem in general. The legitimacy of the Federal Reserve is an issue today, and the competence of people being put in charge of that entity.

Q: What if a regulator is a developer?

A: There's no way that regulators are going to be signing off on code themselves, directly. No, that's not going to happen. I can tell you, if you go to the cryptography professors here at Stanford, that they can tell you who is for real in this space. They can give you some idea of what's real tech and what's garbage. Sometimes with some nuance and where things aren't clear, things like that... there are projects with real technical weight that are doing things that aren't a good idea, and then there's some pretty good ideas with small technical flaws, often the answers will be nuanced. To the extent that you want somebody to trust, I would say trust to use Stanford professors as the schilling point isn't a bad heuristic.

These transcripts are <a href="https://twitter.com/ChristopherA/status/1228763593782394880">sponsored</a> by <a href="https://blockchaincommons.com/">Blockchain Commons</a>.


Tweet: Transcript: "Consensus protocol risks and vulnerabilities" https://diyhpl.us/wiki/transcripts/coordination-of-decentralized-finance-workshop/2020-stanford/consensus-protocol-risks-and-vulnerabilities/ @bramcohen @CBRStanford #SBC20
