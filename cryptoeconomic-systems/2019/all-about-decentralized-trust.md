---
title: All About Decentralized Trust
transcript_by: Bryan Bishop
speakers:
  - Ittai Abraham
---
-- Disclaimer --
1.  These are unpaid transcriptions, performed in real-time and in-person during the actual source presentation. Due to personal time constraints they are usually not reviewed against the source material once published. Errors are possible. If the original author/speaker or anyone else finds errors of substance, please email me at kanzure@gmail.com for corrections.

2.  I sometimes add annotations to the transcription text. These will always be denoted by a standard editor's note in parenthesis brackets ((like this)), or in a numbered footnote. I welcome feedback and discussion of these as well.
--/Disclaimer --

It's all about decentralized trust

Ittai Abraham (VMware Research Group)

Hi everyone, let's get started. We have Ittai Abraham talking about "it's all about decentralized trust".

# Introduction

Thank you so much for coming today. Generally I would like to talk about my latest and greatest research on blockchain and distributed computing. But both Andrew and Neha asked me to say a few words about building a new field.

# Invitation to Advances in Financial Technology 2019

I want to start by inviting you to October in Zurich in a few weeks, for the first ACM conference on Advances in Financial Technology (AFT'19). It's an interdisciplinary project related to research in blockchain, distributed computing and cryptocurrency.

# Agenda

I want to talk about "follow the money" and one of the academic pillars of this new field. I also want to talk about what is decentralized trust. I will also talk about scalable byzantine fault tolerance, which is what I would talk about if I had to only speak about academic work.

# Follow the money

You're probably aware there's a lot of money in cryptocurrency. Last time I checked, the valuation of the markets was over $200 billion. A lot of people have made considerable money in this space. You'll hear a bunch of different speakers today, and my recommendation is to follow the money. People tend to have transparent, or clear, reasons to say what they're saying. There's a lot of money involved here. You have to figure out and understand, who's talking and what are their motivations?

# Transparency: Funding

The way that I recommend addressing this while building a field is to focus on this notion of transparency. Transparency is about operating in such a way that it is easy for others to see what has been done. The first aspect of transparency is transparency of funding and investments. We're here in the media lab. There's an elephant in the room, related to funding. I don't think that transparency alone would solve it; you have to have good moral judgement and be transparent. I'm calling for more transparency in this space. If you're personally invested in something, then people should know that. That's part of what you have to explain if you're in this field. If you are funded by some other entities, then you should also be transparent about it so that people know what are these economic forces acting on you.

# Transparency: Conflict of interest

Also, there's transparency of conflict of interest. This is also something that happens a lot in the academic world. There's a lot of ties and it's important to understand relationships between the different conflicts. There are people who work together, or who don't work together, histories of collaborations... I'm against the notion of this binary approach of there is or isn't a conflict. If you worked with them in the past 2 years, then you can't review their work, but if it's 2 years and 3 days then no problem. I don't believe that. There should be transparency and you should explain all the different conflicts of interest. Anonymity in submissions can sometimes hamper the effort to be transparent because then people could say well I don't know where this paper is from, so then you lose out on the transparency of conflict of interest.

# Transparency: mathematical results and others

I am calling for more transparency in reproducible full proofs and theorems. There's also transparency in system research, like ACM Research Artifact evaluation: availability and functionality. Is it available, and does it run. The most important thing is reproducibility, though. This is the ability to actually replicate the experiments you're claiming in the paper. Without a field that does repeatable experiments, we're going to get into manuscripts that make wild claims and there's no way to progress the field by trying to compare these claims.

# Transparency: peer review

Transparency in peer review needs to be taken into consideration. There's often public review and public rebuttal of reviews. I think we can learn from the open source community and the developers. In addition to a private peer review process, there should be a public peer review process.

# Transparency: selection

I am privileged to have been selected today. But in the cases where there is a selection process, we should identify who the committee is, and here's the criteria by which they made they selections.

# Academic pillars

Back in 2007 I gave a talk at Microsoft Research. This was the slide I used there. This same slide fits here. Here's the three things I'm most interested in. It's the interdisciplinary area between economics, cryptography and distributed computing. Economics is the study of how people react to scarce resources and to incentives. There's microeconomic game theory questions and also macroeconomic policy questions. The thing that economics is bad at is evaluating protocols and software, it's more about evaluating what people do. Cryptography is an amazing advance in humanity in general. Cryptography is the ability to replace trusted third parties. So if you have a signature scheme, one of its properties is that a trusted party is saying this message came from this person. A zero-knowledge proof is that there's a trusted party that verifies this proof and says it's correct. The idea of universal composability and indistinguishability are an advanced way of replacing trusted third parties in a very formal mathematical way. This is a huge breakthrough to humanity, the ability to replicate trusted third parties. We're seeing advances in cryptography in the last few years which are amazing, both at the rates these results are arriving and the rate at which the results are being practical. Cryptography is leveraging core ideas in theoretical computer science and complexity theory to show that these trusted third parties can be made to do work that is much less than expected, like the succinct proofs that can be verified more quickly. Cryptography usually has the good guy bad guy notion, and it doesn't think about incentives necessarily. My personal expertise is in distributed computing. I believe in blockchain and cryptocurrency, distributed computing has an important role and it tries to capture an understanding of how to build large-scale distributed systems and networks and how do we build systems that can tolerate failures. I think the interaction of these 3 areas is key for this new field.

This was my take back in 2007. But my new take is that there's more things that need to be taken into account. There's a new area I would add, which is the notion of governance. I don't mean on-chain governance. This is really about, how does this whole field is related to public policy, politics and to law? How does governance effect the effect of the institutions and social orders that we have? I think this interdisciplinary research has to understand this topic too.

Academically, since this is a subfield of computer science which is a subfield of mathematics, then we should maintain a high degree of rigor. If you're doing theory, you should have mathematical rigor, and if you're doing cryptotgraphy then you should be held to cryptographic standards. If you're doing game theory or economic claims, then you should be held to economic standards. If you're doing distributed computing, then you should be held to those standards. Legal claims should also meet the highest standards.

For systems research, it's important to have reproducible results. I can't stress how important this is. I've seen many manuscripts claiming different things. It's hard to validate these statements and see if it's true or false. In addition to reproducibility, we need comparability so that we can measure it and compare it to previous results and see whether this new system is somehow better or breaks or does not break your hypothesis relative to previous work. We need to develop new benchmarks and common workloads and common ways to measure fault tolerance and security, and this is important for our community.

# Decentralized trust

This is an email that Satoshi Nakamoto wrote in 2008. He claimed that proof-of-work is a solution to the Byzantine Generals' Problem. I learned about this email quite recently, a few years ago. I learned about this email through a NY Times article that Marc Andreessen wrotee. He's a well known venture capitalist. He said, bitcoin is the first practical solution to a long-standing problem in computer science in his article "Why bitcoin matters". This has been my work for years; I thought he was joking. He's a venture capitalist, writing in the NY Times, and he's saying something about my work, and I think he's completely wrong. What I have learned actually is that there's a lot of truth in what he said. We actually know now that Satoshi's work has major advances in byzantine fault tolerance, and it breaks the F/M lower bound and so on. It took me a while to realize this.

I want to relate byzantine generals' problem with decentralized trust. Here's a quote from a16z-- "... where unique capability is trust between users, developers, and the platform itself". To me, decentralized trust is about practically and economically viable solutions for the byzantine generals' problem and more. Decentralized trust is about not depending on a single monopoly power. There's no central authority, and you try to decentralize decision making into a group. The properties of your system, like liveness, immutability, privacy and safety, don't rely on a single individual. So even if the system is compromised, then the system still behaves correctly. We talk about an adversary that controls some fraction of the system.

Liveless means that good things eventually happen, and nobody is blocked from taking actions, even when an adversary is trying to block the system. The other property we want is safety. In cryptocurrency, this is about avoiding double spends. Safety and liveness if those are the two properties-- that's cryptocurrency's requirements right there. But there's a notion of trust, where what people were worried about was platforms where some monopoly power could change the rules as the system continues to work. We've seen this in other cases where monopolies had agreements with us, but over times they changed their privacy policy or they changed pricing on us and how they extract value out of us. Part of trust is the ability to be immutable, in the sense that if you want to change how the system works, you can't do it with monopoly power. You need consensus of the participants to make those changes. I think this is part of the value of these new systems.

I also think privacy is a very important aspect here. I don't think about an extreme version of privacy, but rather some ability to have privacy guarantees between the users of the system and what the system provides. Whatever those guarantees are, then those are the ones that are held. Privacy means-- obtaining the right privacy balance, adversary cannot learn more info.

In decentralized trust, who has the power to make decisions? If you think about it, today we live in a world where we presumably have voting rights. But who puts items on the ballot and what do those items correspond to really? The idea that women can vote is a modern idea in society. It used to be not the case. Less than 100 years ago, in 1920.... the choice of who can and cannot vote is important. We can talk about "adversary power", and we try to limit the ways that the adversary has control over the system by figuring out what fraction of the vote the adversary has, assuming votes are all powerful and have real correspondence to action. But how do you distribute votes among the population? You could have a closed membership group, like a Libra Association with 27-28 members and each one has 1 voting right. That's one way to decide among membership. Another membership approach is to say, if you have CPU then you have a vote. One CPU is one vote. If you have a fast CPU then maybe you have more votes. If you have cheap electricity, then maybe you have more voting rights. We're seeing new models like proof-of-stake. The more tokens you have, the more voting rights you have. Ethereum 2.0 is taking this approach where you spend 32 ETH and you get 1 voting right in this validation system. We're seeing new types of results, used for example, the ability to claim storage as a voting right. To me, when I think about voting, I boil it down to things that these are all things you can buy through money. You can buy CPU through money and coins through money. It begs the question, are all of these systems building a notion of plutocracy and are they leading to decentralization?

"I like to quote a 2018 study of bitcoin and ethereum (Gencer et al 2018). Even though we think about these as completely decentralized, in fact there's a small group of mining pools that control all the miners in the world. There's a small number of ASIC providers and you can't do bitcoin mining today with your laptop. You have to buy dedicated ASICs to do this. There's few vendors that do this. So they have monopoly power. The claim is that PoW forces you to centralize. People who live near cheap electricity get more voting power. Then there's the argument that PoW is wasteful.

How do we change this? Is it the only case that the only way we can do is say the way these systems work is that the more economic power you have, the more voting rights you have. How do you make money less useful? How do you prevent briberies and vote buying? How do you prevent this centralization and this rich getting richer effect where a small group of people have a large amount of monetary power?

PoW and PoS are just means to decide who gets voting rights. Once you have voting rights, you can decide what kind of consensus system you're running. It's true that bitcoin has PoW. But you can mix and match things in many different ways. Let's use the right kind of vocabulary. PoW and PoS talk about who has voting rights. But what's the consensus protocol? Is it Nakamoto consensus, asynchronous, partial synchrony BFT, or what?

# Scalable byzantine fault tolerance

We were thinking about a decentralized trust architecture. The first layer is byzantine fault tolerance state machine replication (BFT-SMR). The middle layer is a smart contract layer like EVM or otherwise with different kinds of smart contract languages and execution engines. The third layer is distributed applications that run on top of it. This is not a new vision. This is pretty old, it comes from research in byzantine fault tolerance and state machine replication. Barbara Liskov did this work in the early 1990s. It developed extensively in the last 30 years. The high level approach of BFTSMR is this primary-backup paradigm where every node replicates state, and in every view there's one primary and a bunch of backups. There's a way to switch from one primary to another primary. What these systems have are these two properties-- they are always safe, and they have no disagreement, even if the system is completely async. When the system stabilizes and there's enough synchrony in the system, then it makes progress. All of this is done under the assumption that the adversary has less than 1/3rds of the votes in the system. It has liveness when the system stabilizes.

SBFT is a scalable version of BFTSMR. This was published this year in DSN 2019 under Guy Gueta et al. It uses new algorithmic ideas and modern cryptography to get more scalability in BFT. We use collectors to avoid quadratic communication. We found that running systems that have a linear amount of communication is better at scale. You can also replicate the collectors, and have a group of collectors and then have fault tolerance between the collectors. We're using more modern cryptography in order to get smaller and faster signatures, so using the BLS signatures to reduce proof length. One of our algorithmic advances was to reach consensus in one round. Typically BFT systems take 2 to 3 rounds to reach consensus. But this work is unique because it requires only one round to do consensus, it's low latency and very efficient. And then we have a new correct view change protocol. This is an interesting theoretical result, but one of the first academic results that has been rigorously tested and studied with benchmarks and repeated with previous benchmarks used in the past on other projects. On 200 nodes, running real workloads like EVM smart contracts, we get 2x the throughput relative to previous types of systems.

This work is now part of VMware's effort to build an enterprise-grade solution. It's available on github as Concord-BFT. One effort that we're doing at VMware related to blockchain and using this technology.

# Conclusion

I talked about a few things. Follow the money, ask yourself. I talked about academic pillars like economics, cryptograhpy, distributed computing, and governance. I talked about what is decentralized trust, and voting. I also talked about scalable byzantine fault tolerance.



