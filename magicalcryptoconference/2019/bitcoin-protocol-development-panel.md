---
title: Bitcoin Protocol Development Panel
transcript_by: Bryan Bishop
tags:
  - mining
  - lightning
  - taproot
speakers:
  - Eric Lombrozo
  - Matt Corallo
  - John Newbery
  - Luke Dashjr
  - Katherine Wu
media: https://youtu.be/8B1fX2i4dMY
---
Bitcoin protocol development panel

KW: We have some wonderful panelists today. Let's kick it off. Let's start with Eric. Who are you and what role do you play in bitcoin development?

EL: I got into bitcoin in 2011. I had my own network stack. I almost had a full node implementation but I stopped short because it wasn't as well tested or reviewed as Bitcoin Core. So I started to look into the community a little bit. I became really interested in the development process itself.

KW: Matt?

MC: I have been around since 2011 as well. At various points, on and off contributing to Bitcoin Core. I had various parts of the stack especially on the network side and also a lot of work in the mining protocol design and mining block propagation improvements. I did some work on lightning. I've done a few things I guess.

JN: Hi everyone I'm John. I work with Matt at Chaincode Labs. I work on Bitcoin Core most of the time. I write pull requests and tests. At Chaincode, we have the freedom to work on what we think is useful and important to bitcoin. I spend some of my time working on bitcoinops.org or Bitcoin Optech which helps disseminate knowledge and education.

luke-jr: I came across bitcoin in 2010. In 2011, I had my first pull request. I've been all over the place in bitcoin. Lately I have been focusing on mobile wallets.

KW: Awesome. Let's start with a super macro question. I would like an answer from each of you. What does bitcoin mean to you, and what motivates you to work on it?

EL: The monetary aspect is the most fascinating. The technology is intriguing. Cryptography is very fascinating, and there's applications still not fully exploited. But in bitcoin, you have this programmed scarcity and there's no way to violate that by some sort of institution. We all agree on a certain set of rules to make sure nobody is cheating. I think that's one of the most fundamental things. The monetary aspect is way beyond other systems. Most people don't have choices in the fiat system. There's never been anything like this situation. Bitcoin lets you opt-out of this. The government starts to get corrupt and all this bad stuff happens, but if you can opt-out then you don't have to be subject to that. To me, that's the most important aspect.

MC: Bitcoin is fascinating because it gives us this alternative, it's competition to super centralized systems. If for whatever reason you can't use existing financial infrastructure-- maybe you're one of the 30-40% of people in the US who do not have access to financial services-- maybe you're in Venezuela and the government is screwing you. There are many reasons why. But maybe there's some reason you can't use the existing system. It might not be as usable as centralized systems, but I'm working hard on improving it to get it as close as we can.

JN: I think bitcoin can be an excellent payment platform. We're seeing that with lightning. I couldn't stop thinking about bitcoin so that's how I got into it.

luke-jr: There's the joy of solving difficult problems. There are things that need solutions to make life more livable.

KW: I'm curious because I sit on the outside of this. How does the coordination work among different developers when it comes to bitcoin improvement proposals? How do these proposals get adopted?

luke-jr: The technical details need to be public otherwise people wouldn't be able to agree. There's no top-down options here. Developers can choose to adopt standards, and then people can choose to adopt the developer's software.

KW: What are the communication channels?

luke-jr: These days it's mostly the IRC and the bitcoin-dev mailing list. That's pretty much where all the discussion happens.

KW: Apart from mailing lists, what about forums? Do they play a big role in getting ideas?

luke-jr: I don't think forums are used much anymore. Early on bitcointalk.org was used a lot.

KW: Has this formalized the process a little bit?

luke-jr: There's some formal ways that we measure support of a BIP whether it has been successful or not, but there's no formula. There's some description of what's supposed to hpapen and reasons to adopt it. Nobody has to follow those recommendations. It's a pretty flexible process.

KW: John, a pretty hot topic recently has been around privacy in bitcoin. Since bitcoin not fully anonymous, it's pseudonymous, what are your thoughts on privacy in bitcoin? There's a taproot soft-fork proposal which would increase privacy. How would that happen and what's the challenges of having that kind of change deployed and activated?

JN: It's going to be difficult to summarize an answer to all of those questions. Bitcoin as a rule of thumb has been bad for privacy because it's an open ledger where everyone sees everything. By it's nature, that's bad for privacy. A good rule of thumb or a good starting point is the less data you can put on the blockchain, the better it is for privacy, fungibility and scalability. We have made progress in that direction for the last 10 years. The taproot proposal is the next step in that. It would allow us to utilize the programmable money aspect of bitcoin and create a much smaller footprint on the blockchain. In bitcoin, when you send a transaction you encumber the outputs of that transaction with certain spending conditions. This is written in Bitcoin script. These are attached on the outputs of each transaction so that anyone can see the details. In 2011-2012, p2sh bip16 made it so that there's a hash commitment to that, and the conditions to spend are revealed only when the output is spent. Taproot takes this another step further where the conditions to spend are committed in a "tweaked" public key. It looks like a standard public key, but to the rest of the world there's a commitment burried in that public key and you could do cooperative closure or you could do uncooperative closure where you reveal the script on the blockchain. In the cooperative case, you preserve privacy and also reduce costs and blockchain bloat is minimized.

KW: What exactly would be the major challenge for getting the taproot soft-fork activated? So it's technically possible, but do you see friction for its adoption occurring?

JN: That's a great question. Two years or three years ago, segwit was proposed and then implemented and then activation was quite a struggle. That proved to be difficult. I think the expectation is that it should be less difficult for this, because taproot and Schnorr and tapscript are very clear wins for privacy and scalability. It's more contained in the way that transactions are structured. We hope that activation will be less difficult. Taproot and Schnorr will get a round of feedback from the community and have been flotaing around for quite a while. I think in the next 6 months or year, it will be implemented, and hten anohter 6 to 12 months for activation. But there's no way to know and no direct way to make it so.

KW: Speaking of political decisions, I want to bring up the recent reorg discussion. Just for those who aren't familiar, Binance suffered a breach that resulted in a 7,000 BTC loss. In the aftermath of the breach, cz hosted a meeting where he discussed the possibility of a reorg. For those of us who don't know, tell me on a high level, what does that really mean?

MC: This has come up a number of times at various points when exchanges were hacked. There was a much quicker discussion after the 2016 Bitfinex hack which was maybe even a more significant hack in terms of the amount of funds stolen. The propsoal is to say let's reach out to all the big mining players or the big pools and let's have them try to run a completely parallel chain and let's rollback to where the funds were stolen and let's include an alternative transaction where the funds are paid bcak to the exchange instead of the attacker, and start mining on that fork instead of the other chain. This is a coordinated 51% attack. The entire network would reorganize and switch to this chain where the funds weren't stolen, and you're creating a parallel history and if you can get more PoW then the network will switch to this alternate history where nothing was stolen.

KW: Thank you. I would love to hear from each of you your particular take. It has been heated online. Some people have come out saying it's okay, and others are vehemently against it.

EL: This has been discussed a lot in the past. This is not the first time this topic has come up. It's fundamental to how bitcoin works. It's very rare to have a 100 block reorg, which would be disastrous for the network. The risks and the incentives-- while I think it's a non-starter because of the coordination effort.... it's good for people to discuss it, it's an important topic, I wish someone would try it just so that we have a good lesson in practice about what happens. The question is whether they can do it or not. If someone says they can do it, it's more interesting to see if they can actually do it.

<https://bitcoin.stackexchange.com/questions/87652/51-attack-apparently-very-easy-refering-to-czs-rollback-btc-chain-how-t/87655#87655>

KW: Do you take any issue to how cz presented the issue?

EL: He was under a lot of stress. It's hard to figure out how to do the right thing. I think the way Jeremy presented it was a little rushed. It's good to have people come up with new ideas and try to think out of the box and figure out new solutions, but if you try to publicize this and get a lot of attention to it, it leads to a lot of discussion where it proposes things that don't make sense. I'm glad people are discussing it, but we have to see someone try it out.

KW: Interesting.

MC: Bitfinex did try. In the case of the cz discussion, this was like 6-12 hours or a day afterwards so the amount of wokr required to create this alternate history is very significant. In the case of Bitfinex, they were on the phone immediately. A huge percentage of the bitcoin they had was stolen. Within an hour, they were on the phone with a lot of pools trying to figure out if they can get their money back as they are expected to do. Their business was at risk at that point. They have a custodial responsibility to do this. There's a number of interesting frames from which to look at this. There's the individual business who lost the funds- I would expect them to try this. They have to do what's best for their usiness. They have a legal obligation to do that. From the point of view of the pure technicals, which I think is really where Jeremy was coming from, yeah sure it's possible. From the bitcoin networks' perspective, the rules say that the PoW chain with the best proof of work is the valid chain. It would be a major problem, though, for the users of bitcoin as a whole. Most people accept deposits and payments with 6 confirmations, and a reorg would change blockhashes. If you were to reorg deeper than 6 blocks, then this sets a precedent around how bitcoin works and destroys a lot of businesses and causes them serious harm perhaps impacting the long-term future of bitcoin. If you destroy a lot of businesses, then they won't trust bitcoin or continue using it. This is why you saw a lot of pools saying no we're not going to participate in this process. At the end of the day, cryptocurrencies are social systems. We need to set good precedent about how changes are made and how reorgs work and how mining is done, so that in the future the community as a whole enforces that on its own. This is why these discussions are healthy- the community reacted with outrage, that's the correct response. The social consensus around bitcoin is to say no you must not do that, and it must not be how bitcoin works. This is an important backstop on which the network relies. In the long-term, we want more decentralized and more secure mining. We want this to be less practical at least from a technical point of view, to become something that becomes completely impractical because the number of people you have to get on the phone because you don't know who they are or how to contact them becomes impractical. In the long-term, if mining gets more decentralized and a healthy community then it will become completely impossible. But we're not there yet. We have to enforce a social consensus to provide a backstop for now, and have the right precedents set for the future even if it's not the world we want in the end.

JN: You could theoretically create an attacker chain and broadcast that to miners and they could voluntarily join. Right now the bitcoin network will not propagate an attacker chain, so they need their own network to propgate it. I don't see full decentralization as a complete solution, nor do I see social consensus as a complete solution. We need a bitcoin where entities act according to incentive. That's what bitcoin is. If you start thinking about bitcoin as being something where we want miners to follow social rules, well we don't have any way to sanction miners that violate those social rules anymore. Yes we can use social norms but we shouldn't rely on those. We need a complete solution. It makes sense for Binance to try to reorg in the minutes after the heist.



