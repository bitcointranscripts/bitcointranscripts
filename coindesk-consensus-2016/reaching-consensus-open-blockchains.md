---
title: Reaching Consensus on Open Blockchains
transcript_by: Bryan Bishop
tags:
  - consensus-enforcement
speakers:
  - Pindar Wong
  - Gavin Andresen
  - Vitalik Buterin
  - Neha Narula
  - Eric Lombrozo
---
Preliminary notes:



Contact me- <https://twitter.com/kanzure>

Reaching consensus on open blockchains

Moderator- Pindar Wong

Gavin Andresen, MIT Digital Currency Initiative

Vitalik Buterin, Ethereum Foundation

Eric Lombrozo, Ciphrex and Bitcoin Core

Neha Narula, MIT Media Lab Digital Currency Initiative

Please silence your cell phone during this session. Thank you. Please silence your cell phones during this session. Thank you. Ladies and gentlemen, please take your seats. The session is about to begin.

Please welcome Pindar Wong, Gavin Andresen, Vitalik Buterin, Neha Narula, Eric Lombrozo.

PW: Thank you. I will be moderating the session. I would like to do some housekeeping ot let you know that if you would like to send questions, about 20 minutes into the session we will be feeding questions from the audience. As we heard this morning, there was a wonderful slide about the distinction between open and closed source proects. There was another great slide in terms of leadership comparing Linux open-source software with Linus being the figurehead, and Vitalik with Ethereum Foundation, and a giant questionmark over Bitcoin. Recognizing this morning's news, I would like to ask Gavin Andresen to say some words. This is Mr. Wong asking about Mr. Wrong. ((applause)) Just to recognize that, there will be some time, but I don't want that to overshadow the panel. We do have some business. Gavin, could you say some words?

GA: I was not hacked. The dot ninja domain is indeed my words. I still believe that Craig Wright is beyond a reasonable doubt in my head Satoshi Nakamoto. I imagine there will be Q&A questions about this. Let's talk about tech and governance instead.

PW: This news article broke this morning. As a public peer-to-peer protocol, there was peer review on reddit already talking about why Wright again may not be Satoshi Nakamoto. This gives you an example of the power of an open peer-to-peer process. This is an open protocol. Here to discuss many issues on scaling and how to reach consensus on open blockchains. Peer review is not new. We have had it for several hundred years, at least in the academic sphere with peer reviewed papers. What I would like to do, one of the key aspects of scaling this tech, where are the engineers and those trained in these crypto protocols, where will they come from? ... I think what we learned last year is that nuance does not scale. It's very difficult to articulate why these open protocols are constructed the way they are, why scaling them is a nuanced discussion. So from the academic perspective we have the MIT DCI, one of the contributors to Consensus2016, it has just now been over a year that since April 2015 that they have... we are privileged to have Neha, and I hope she will share some views about what DCI is looking at in terms of scaling.

NN: Hi everyone. I am new to this community. I started 5 or 6 months ago. I started in computer science. I think what's exciting about crypto tech is that it is slowly becoming a legitimate academic discipline. It pulls in so many different areas like computer science, theory, cryptography, there's financial models. We didn't have the vocabulary for putting all these areas together and figuring out how to do peer review and real research. I think this will be a really exciting next few years as the academic community works with the industry and start to get a good framework and structure for tackling these problems.

PW: Over the past year, we will be moving from pilot to production. I think in March, ethereum had a launch, I think .. full market cap... what do you feel was different about open blockchain technologies? ... ....

VB: I think open blockchains in general are really unique and they aren't like traditional corporations or software system. There is no one group that controls Bitcoin. It becomes interesting because the review mechanism that actually controls it is also unspecified. There's no sort of consensus that this SPV by which could be adopted in the future might be changed, instead it's this kind of interesting game where people have to get consensus on a purely social level. It's like, the one analogy might be, let's imagine let's say, the english language, let's say english word development institute might try to launch new words from time to time, adding s after verbs in the third-person that's stupid let's remove that. You could even imagine classical institute development and let's say they disagree with each other, the point is that there's no way for us to agree.

PW: This whole notion of consensus is frustrating for the business community. Who's in charge? And you're sometimes presented as a figurehead for Ethereum Foundation. Similarly in Bitcoin, it's open-source, you can fork it, but whether the code is accepted or pushed out to production is by choice of those who have developed. What is the difference between open source and open blockchain?

VB: The blockchain is a continuation of open-source. In the original software movement with Richard Stallman, he specifically in his presentations talked about how valuable it is for a person to be in control of the source code they are running. The whole concept of the free software movement was started in the 1980s. In the 2000s, what happened is that it moved to cloud computing, which is even worse than proprietary software like Windows because if you're running Windows at the very least you can reverse engineer it, which is harder on the cloud. So people are watching for open-source ounterparts for that.

PW: In the bitcoin space, since lsat year, we've had XT, Classic, we have the original Core, as examples in the space. What are the differences? Eric, what is Bitcoin Core?

EL: Bitcoin Core is the open source software project that builds the backbone of the Bitcoin network. It is also home to where the protocol definition is made. The definition itself is in the code. It's hard to document these rules in a way where we know for sure all nodes will be running the same rules. So it's become a reference implementation. We would like to separate the consensus rule definitions from the software, have different approaches and different programming languages to implement these nodes. One of the things about consensus networks is going beyond most osftware projects is the requirement for compatibility. There is really little tolerance, because if two nodes disagree about the rules they can be forked into different networks. In Bitcoin Core we have been trying a decentralized process for upgrading the network. The biggest thing we focus on is compatibility. How can we deploy new features that doesn't break old nodes off the network? With the whole segregated witness, it's basically the biggest protocol improvement to Bitcoin since the beginning. Part of this is allowing for extensibility, allowing you to commit other kinds of data into the blockchain. What this means is that you can add new features to the protocol in a way where old nodes will not check those new validity rules but wthey will still consider those blocks. So part of what we're trying to do, we have no way to specify the software yet, people run whatever they want, and you know we can make recommendations and that's what we try to do, but in the end we want to preserve compatibility so that's been the biggest focus of this.

PW: Gavin, what do you think about that?

Gavin: 7000 nodes?

PW: So they just download the software they want to run?

Gavin: They are not all running the same software. There's a tension between compatiblity and diversity. Diversity is great if you can maintain compatibility. It's great that you can choose many companies and ethernet equipment. I agree with Eric that we need to get more serious about this is the bitcoin protocol.

PW: Consensus protocols in computer science have been around for a while. I don't quite understand why blockchain consensus protocols are so not well understood mathematically? Neha?

NN: It's quite frustrating because there's so many... in computer science... servers and... it's interesting to see... interesting ways, what's novel about what's happening right now is that, because you believe, ... but right now there's this open access model, this is something that people typically forget. Open access consensus protocols, that's what's brand new right now. That's definitely exciting. It's an open interoperable protocol which ends up with.. and when you have this kind of model, this kind of platform, it spurs all kinds of innovatio.

PW: This morning we heard a reference to Marc Andreessen that we're a few years away from the same kind of boom from the Internet. I think you can compare this with the Internet. There's a distributed database called DNS, there was a time when there was one software implementation that had 100% implementation and deployment, called bind. We realized this was not healthy. If there is something that goes wrong with it, there might be a systemic failure. What's interesting is that this might happen in consensus-- so Eric, will we ever have a specification first? I think there's btcd is an example of another implementation.

VK: Ethereum's spec is in english.

PW: Why?

VK: If the spec is an implementation, and the developers of that implementation become a central point of failure... Software that is finished is software that is dead.

PW: So, open systems are in an adversarial environment. I think people are actively trying to take this system down. You have lots of eyeballs trying to find new spaces. The difference between open and closed matters. There's a comparison between intranets and internets. Some of the discussion about permissioned and closed ledgers versus open ledgers is, there's this point about interoperability. In all of these separate innovations, using blockchain as a platform, are they going to interoperate between private permissioned ledgers and open permissioned ledgers? Is that possible?

VK: One interesting project is TC Relay. This is a contract. It's a bitcoin transaction verification smart contract. By Blockstream's definition, this is a sidechain that validates that. We have launched the first production sidechain. This is cross-chain interop, you can have ground code that launches into ethereum and pay to it in bitcoin, that model that can be expanded between any database blockchain. You can do it between consortium chains or anything.

PW: Would you have predicted this 4 years ago, Gavin?

Gavin: Interop stuff happening on blockchains?

PW: Yes.

Gavin: Yeah it was just bitcoin. The network effect from money is really strong. I think the world wants there to be one money. It remains to be seen whether bitcoin is that one digital money that bitcoin works. I still tell people to not invest their life savings in bitcoin because it might not turn out to be that popular. But I still tell them to get a little becaues it might be. There are 100s of alternatives to bitcoin, ethereum being the 2nd biggest right now. It doesn't surprise me that tech exists to move currency between blockchains. ... It wouldn't surprise me if there are blockchains going in other directions. Innovation can be borrowed from anywhere. And that's fantastic. All of these monies are better than fiat monies which are closed and highly controlled.

VK: Programmable money is wonderful.

PW: We're at the beginning of open blockchain database technology. Some of the interest is in private blockchains. I don't know what they are quite yet. Transparency, different kind of model, which has interesting characterstics. These characteristics about openness means open to innovation and open to involve and ... the question is the rate, .... there are a couple things in there...

EL: In Bitcoin Core, we do want to have a spec in english. The problem is that natural language tends to be ambiguous. It's hard to get things defined strictly. Subtle misinterpretations or slight bugs could result in bugs or problems on a financial netwrok. In code, at least you know what it is supposed to do, that it can be analyzed. We want to get it close to making it not dependent on a particular implementation. In ethereum, that's been done a lot due to the collaboration between the teams working in different programming languages and there's a lot fo communication there. We have that kind of communication and it's possible to agree with the rules in english. As far as the multi-chain stuff, back to what we were talking about, we were really excited about the idea about having smart contracts operating on multiple chains. Even if two different chains have different rules, you can have off-chain contracts where you can redeem these contracts on different chains is promising. One of the problems we've been having with exploring these different areas of what we can do with different coins is that it's divergent. It's hard for people to take innovations from different innovations and merge them together. It would be nice to have a more layered architectured where we can have some validation at the base level, and allow innovation on top of that which might not require changes to consensus rules, like Script itself, or the execution environments for these smart contract Scripts, and make sure the results are what everyone agrees on.

PW: Before we move to questions, what can we learn from the Internet, we have standards organizations, we have lots of ideas available there. What could the blockchain tech community learn about onboarding engineers and that? Getting involved, what's the status?

VK: I think we're conflating two issues... one is increasing developers, the other is ensuring consensus on protocol upgrades. I think the first is a kind of education problem which will have to be solved by the community to work together to make dev tools easier, work on education, etc. Regarding the second problem, I think it's unique because of the cultural constraints we have around being concerned about decentralization and censorship resistance. With basically with, a lot of people are not going to have the ethereum exist and standards body, and the board of directors is controlled by like 5 major software companies. This is something we can't force a model from the top dow, the constraints are fundamentally different, this is not something we have seen before. I think the approach we are going through currently, like price, that might be the best we can do.

PW: There was an article that... the capture issue like that... the existing model, this concept of decentralized administration or decentralized governance. What do we mean when we talk about decentralized? Is that a beautiful concept? Does it mean global? What does decentralized mean?

VK: I would argue that the way you measure decentralization is difficulty of consensus.

PW: Could you use blockchain tech to do governance?

VK: If you mean, reading protocol changes, the answer is maybe, but then the second challenge is, what do you want the rules to be? Can the community decide? Are they going to agree on what the rules are going to be? Do you even want a process on that? Or do you want the users to consent to it? There was a case which was to some degree arguably has a some kind of multi governance model, where the second chamber is like the 5 or 10 miners in China who... there has been some blog posts that say hard-forks are bad because they put too much power in the second chamber of a few miners and sometimes you might want to make changes.

PW: The miners... the power of getting people together. There was a great quote. Every ... and we had lots of emotion and drama in the Bitcoin space. I think at the same time, the consensus at Scaling Bitcoin Montreal, we got everyone together face to face, irrspective, it was a human process of people coming together trying to harmonize vocabularly. What do you mean by X? What do you mean by Y? When we got to Hong Kong, we had a translation issue as well. I would like to open up to questions now. I am losing my voice. Is liberty worth sacrificing for convenience?

GA: How much convenience are you giving up for how much anonymity?

EL: You should be able to choose how much you want to give up. A lot of these environments, you see you are either completely anonymous or you have to reveal everything even if the info shouldn't be relevant to purchasing something on the internet. For every use, this is more of an identity management thing, maybe you want to reveal certain aspects but not everything. It should be the user's choice, whether it's worth the convenience is their choice.

NN: What are we getting with anonymity? It's not just anonymity for anonymity's sake. It's censorship resistance. It's open access. It's ensuring freedoms. It's not proxy word like anonymity.

VB: If you look at the kinds of systems that people are ubilding, privacy and anonymity are not just limited to buying stuff on Silk Road. It's also simple concerns like financial markets not getting screwed up by frontend attacks.

PW: An anonymous question is, which is very convenient for them....

GA: Law enforcement would rather have every transaction have clear identity that they can get at, which nobody else can get at. They want a backdoor. That's the system they would like. I don't think they get this in the real world with cash transactions. Credit card companies, I don't know what processes they have to get information.

VB: Overseas, there's a couple of months ago I went to Mexico, I took some money out of an ATM and that ATM was actually- I was able to tell -- I had a valid balance of something like 2 million pesos, and it was a lot less worth I guess, but my community bank was giving this random information to this ATM in Mexico. Wow.

PW: Should digital identity be managed by government?

VB: Regarding identities, government as identity providers is completely legitimate. Another ethereum project is an integration with Estonia e-residency program, which could enable full surveillance inside of an ethereum contract. The nice property of this is that it's voluntary for that government, I think number two it's not one centralized source, but one where you assume at the base level that people have identities, people can make claims about identities, and claims about trust should be left to the edge.

GA: I have huge faith in the open process. It's crazy. It's three steps forward, two steps back. I think it's the best system that we have for innovation. I think innovation is the key. Making things better. Making the world better. How can people track innovation? It's hard. It's open. There's no one source of information that will tell you everything. The best sources of information are aggregators like Bryan. I can't keep track of everything going on in the bitcoin world.

PW: There's a cambrian explosion of innovation.

VB: There are open processes. It's important to know there are many kinds of open processes. In general, processes that look like market processes are processes that look like, people that like different ideas can try them in parallel, they work better if you can get away with them, rather than people fighting over one particular thing. If you can, have, I think anti-fragility comes not even necessarily at the level of one project but at the level of the entire U.S.S.R... if two people have transcendental values, if people just have different opinoins and one of them is proven right and more people are doing different things and can learn from each other.

NN: We are still at the beginning of this grand experiment. It remains to be seen how steep this curve is. We are still at the beginning. It's exciting to see these areas coming together. Some of these areas are very old. Cryptography here is not cutting edge, although we're adding cutting edge features to it. Databases are a really old field. Extremely old. But what's new? This open access platform, using rationality, using a currency, using markets. There's a lot of talk about closed versus open blockchain databases. I think that's missing the entire point of this bitcoin revolution, it's an open platform for people to interact and have innovation.

EL: I think that we need to-- right now we have lots of investment in applications. We really I think we need to find more ways to collaborate as an inudstry to figure out interop standards and get better communication. There's a lot of misinformation spread, a lot of people, it's kind of hard to figure out if a source is good or not, we need to do a better job of having forums where we can discuss things and make sure everyone is on the same page. With open-source, we are trying to incentivize computing that allows people to get paid for providing a service to the network. That service can be validation, making sure that we agree a transaction took place. This is something adding. We need to figure out how we can work together. I'm optimistic that we're going to find more serivces that we can find this thing for. We can build a more decentralized internet where people can build services for the internet and have trustless incentives for them to be in order to do that.

PW: One of these things that these face to face meetings help with is collaboration and perhaps out of this is an emerging consensus process. We will be around. Please grab us. We will be available for the next few days. Gavin, you have the floor.

GA: I was surprised I wasn't asked about Craig. I posted on reddit that he signed in my presence on a computer that was not tampered with other than the software it was installed. That kind of sealed the deal for me, since he had to install software on to the demonstration laptop. I feel like he's the inventor of bitcoin. He's human. I am sure he makes mistakes. I am sure he has made some mistakes in the past. He wants his privacy. I am going to draw a line. If you ask me questions about this, I draw the line at, I will explain why I am convinced, but I will not go into personal details of the discussion I've had.

VB: I will explain why I think he's probably not Satoshi. ((applause)) He had the opportunity to take two different paths of proving this. One path would have been to make this exact proof, make a signature from the first bitcoin block, put the signature out in public, make a simple 10 line blog post, so that Dan Boneh would be convinced and verified.... he would let the crypto community verify this. But instead he has written a huge blog post that is long and confusing and it has bugs in the software and he also says he wont release the evidence. Signaling theory says that if you have a good way to prove something and you have a noisy way to do it, then the reaosn why you picked the noisy way was because you couldn't do it the good way in the first place.

PW: Thank you very much everyone.
