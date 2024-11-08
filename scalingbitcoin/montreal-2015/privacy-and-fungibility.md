---
title: Privacy and Scalability
transcript_by: Bryan Bishop
tags:
  - privacy-problems
  - privacy-enhancements
---
Even though Bitcoin is the worst privacy system ever, everyone in the community very strongly values privacy.

There are at least three things:
privacy
censorship resistance
fungibility

The easiest way to censor things is to punish communication, not prevent communication. Privacy is the weakest link in censorship resistance. Fungibility is an absolute necessity for any medium of exchange. The properties of money include fungibility. Without privacy you may not be able to have fungibility.

Understanding this technical issue that all privacy approaches have some overhead in terms of scalability, like in mixing, to increase privacy by measuring your anonymity set.

CryptoNote leaves a trail of transaction outputs that are ambiguously spent, you can’t tell if coins have been spent or not. You have to keep the UTXO set around forever. The use of lightning network for example would allow some increase in privacy, and move stuff off-chain at the same time.

If you imagine a very hypothetical optimally-scalable bitcoin using tech that doesn’t necessarily exist, you can imagine schemes where a miner shows you a change to the state of the system, a compact zero knowledge proof of modification to the UTXO set. This would be the most scalable kind of architecture. If you had that, it would by side effect have perfect privacy. A lot of the privacy systems don’t improve the scalability.

Are these constant-factor overheads? That’s not too bad. Or something where it is worse than constant-factor.

A lot of the privacy of Lightning Network is based on onion routing or how you do the payment routing. Assuming that the middle nodes forget the transaction, then you can have privacy. There are many ways to break onion routing for lightning network. There is research required to see if lightning network preserves privacy.

Routing protocol for lightning network can be arbitrarily bad and be less private.

Do the programmers believe in privacy? Some people don’t believe that certain privacy should exist. There should be a bigger emphasis on explaining what the privacy is for, and why the general public needs it. Describing the necessity of fungibility may help.

Later retroactive deanonymization is a constant threat in the future. Weak privacy can burn users. Retroactive privacy is probably impossible.

Someone is sybil attacking the bitcoin network to determine the origin of transactions on the network. We can apply pre-existing tor, mixmaster or high-latency relay networks.

What do we want to have happen as a result of our discussion?

    Graph the known disagreements about privacy as it relates to scalability.

    Ideal features for bitcoin to have.

Privacy is a long-running risk and you can’t retroactively fix it. And you may not think of it correctly in advance.

Opt-in privacy, if you participate in a mix to mix your BTC with someone else’s BTC, it may not help you. What would help you is if everyone participated in mixes.

Confidential Transaction schedule

The privacy tech should not be extra. Perhaps the default lightning network settings should have privacy-enhancing features. Would be a lightning-only anonymity set.

Anti-privacy features have activation energy, like “oh man I have to type my name into this?”.

* coinjoin
* confidential transactions

Is the UX the problem?

A lot of this runs into overhead questions. Stealth addresses require an ephemeral key in the transactions, which can be a 20% increase in transaction fees.

<a href="http://diyhpl.us/wiki/transcripts/gmaxwell-confidential-transactions/">Confidential Transactions</a> make the values of the transactions, the amounts, are hidden. Coinjoin’s privacy is usually degraded by the non-privacy of the values. If your concern is bandwidth or disk storage, it has maybe a 70x overhead on conventional transactions.

Transaction fees are for competition for space in blocks. Socializing cost of privacy on all the users of the system. Subsidize this because privacy is a public good. The benefit of privacy is not you, it protects other people from being attacked.

The people most excited by confidential transactions were banks. They found that non-privacy of bitcoin transactions was bad for them. These were US banks.

You can layer on AML and KYC on top of privacy, but you can’t do it the other way around.

* cost metrics
* privacy-benefit metrics
* privacy-delivered
* anonymity set metrics

k-anonymity set

Measure the entropy or the uncertain of that the adversary has over who did what; uniform distribution is perfect anonymity. Measuring anonymity if they have a skewed distribution, then it’s slightly more likely, but putting that to a single number is sort of impossible. If it touches one person, you can follow the trail, the means by which they have to follow the trail increases.

In some cases, the property that you really need is that you’re not more likely to have sent money to an evil organization than anyone else in the world. You need that level of anonymity. In strong rule of law countries, you can say there’s reasonable doubt. But in other countries, they don’t have that- like “80% chance it was you, so we would go with that”. There’s also a difference between prosecution and conviction.

Fungibility is a metric for privacy in bitcoin. If there were markets where you could get lower quality bitcoin at a discount, which do exist, then that would be a good indication that there’s not good privacy in the system. You would measure privacy delivered by weighted over all users, it would be bad if some users are very vulnerable would be bad, but doing it over coins would be better.

At the system-wide level, you might have really great privacy for 99% of the people, but if you’re in the 1% because you’re gay in Russia or something, that doesn’t help you. And also, do you know you’re in the 1%?

Say there’s only 1% of people that are worried about a coin, it might not move the price if 99% of the people are fine to have it. People are going to care about different BTC for non-privacy reasons, like totally random reasons. It’s possible that the fungibility will occur.

Actual privacy vs. perceived privacy

You’re using a mixing tool that is supposed to be good for privacy, but nobody else is using it, so it doesn’t help.

Lack of colored coins might be a good metric for fungibility.

Payment information is not usually stand-alone. There is other data related to the interaction to consumers, whether it’s mailed to you. Transactional privacy may not add to the lack of privacy that exists in various relationships. Personally identifiable information. It may be interesting to think about the context of the payment in that broader spectrum of data.

The thing about zerocash with bitcoin is that the basic idea of zerocash has a … regardless of the constant factors, it changes bitcoin scalability. They both have an accumulator that keeps growing. The thing that is ever-accumulating is not the accumulator itself, it’s the spent transactions. Same thing that Monero has.

You can’t have a validating device that has storage constant-in-size. It breaks pruning. The validator has to keep everything.

There’s a memory/bandwidth tradeoff. Or you can just pay the ever-growing costs for storage for validators.

We have careful comprehensive analysis of what information is not disclosed in confidential transactions and other problems. You call it a sidechannel when your analysis missed it the first time.

How distinguishables are most people’s transactions are, such as when you get paid and when you pay your rent? That might be identifiable. Relay systems might hide some of this.

Non-fungibility market. There exist people doing OTC trading. At the moment they sell for 1-2%. There’s joinmarket which implements coinjoin. The market can only expose what is publicly available. False alarms and false silences.
