---
title: Tooling Panel
transcript_by: Bryan Bishop
tags:
  - developer-tools
speakers:
  - Eric Voskuil
  - Nicolas Dorier
  - Kevin Loaec
  - Lawrence Nahum
date: 2018-07-03
media: https://www.youtube.com/watch?v=fjtmyaH6MG8
---
<https://twitter.com/kanzure/status/1014167542422822913>

What kind of tools do we need to create, in order to facilitate building on bitcoin? We are going to open questions to the floor. The guys will be there to get your questions. The panel will be about 20 minutes long, and then we will go for food.

LN: I work at Blockstream. I work on low-level wallets and tooling for wallets.

ND: I am working on a library called Nbitcoin for programming bitcoin in C#. I am also the developer of btcpay.

EV: I've worked in the past few years on libbitcoin, a C++ developer toolkit for bitcoin. It's one of the oldest full node implementations of bitcoin apart from Satosh's implementation.

KL: Should there be other full node implementatons?

EV: I don't have strong opinions on it.It's an inevitability. There's going to be whatever code that people want to run. There's many versions of bitcoin core even within its own distribution. To me, it's not an interesting question. It's going to happen.

KL: It's alright. I can take it.

EV: If there are certain things that people want to do, then they will do it.

LN: Some version of Core had issues with 32-bit vs 64-bit on Linux and that caused a consensus failure. But in general you might run into consensus failures even within the same software. The argument is that as you implement other versions, you have to re-implement all the same bugs that everyone knows about, and including the ones that people don't know about. Many years ago I thought, maybe I'll run all of the node versions, and then pick the one that behaves in a certain way, but it doesn't help you actually make the choice anyway. It's not just about me, it's also about what the rest of the network does when there's a consensus version. It's not just tribes and grousp of people deciding about the future-- it's technical failure.

ND: When I first discovered bitcoin, and coding it, I took pieces into a library. I did that to learn about bitcoin. Afterwards, I had an idea of writing a full node implementation to learn about bitcoin. I learned many things but one thing I learned was that the code was too complex to do it all by myself at that time. So I stopped doing this. Later, I did it again because there was a community that went to me and they said they wanted a full node in C# and I explained that I think it's dangerous in terms of consensus failures and you need to know that some people are risking money on this and there will be consensus failure because there's no way that my implementation would be a 100% identical implementation of Bitcoin Core. But their reply was that, we might use to for altcoins. On my side, I prefer not to write code for altcoins. So I said I'll do it for bitcoin, and then you can use it for altcoins or litecoin or whateer. The C++ code is hard to maintain and there's few engineers that want to do it. But on my side, in bitcoin, I would be scared to run anything lese other than Bitcoin Core in production.

KL: So then you also have tools that serve different purposes and are better fit. Iguess, would you guys, have any tools that you would recommend that maybe, you believe most of the people in this room are not aware of, so....

ND: .. it's an interesting question actually, because, I think that's, most of the tooling that has worked for bitcoin ... Electrum, not a great protocol. A lot of this was before hdwallet existed. People tried to use the same protocol as the one that existed before and they tried to retrofit it, and it made the protocol not adapted to what modern bitcoin development should be. While developing the btcpay server, I decided to not use any existing block explorers. I didn't want electrum because it was not adapted for... so I did my own block explorer called Nexplorer. It's very simple IPI... right now I'm using my own tools, including a block explorer, for things that Bitcoin Core doesn't do. Bitcoin Core should stay focused on being a full node. It will never meet everyone's use cases.

KL: What tools could you recommend?

KL: The wallet should be separated from the rest so that people can choose. I'm talking about Bitcoin Core. The wallet should be separated. One thing that many not know about, and many people have been working on libwallet. The idea was that we couldn't find a library that did we what we wanted which was compatible on IOS, Mac, Linux, Windows,  and that sort of thing. Rather than cannibalizing another library, we decided to start from scratch with libsecp256k1. It has support for bip32, bip39, and others. The idea is to support bitcoin and potentialy Liquid as well. This library- we use already in multi-wallets and on the backend. I've been testing it on small hardware gadgets. It should be able to run on any cheap ARM chips. It's a small bitcoin library.. doesn't do any caching, or file systems, it's just crypto primitivies plus some BIPs on top.

KL: How does transaction relay there work then?

KL:It depends on the wlalet you are talkign about. It might be server-client, so it might be SPV or bip70 or directly to the merchant. Eric, do you have any tools?

EV: My knowledge of tools is limited to the tools that I write or rewrite. I can describe what Ihave. libbitcoin is a toolkit, but it's also applications built on top of the toolkit, including full node, server, client stack, admin tools, and to me that's really important if you're going to build a toolkit for other developers. You need at least one implementation that makes use of your API. libbitcoin is 10 different independent repositories on github, and an 11th which is a build sytem. We put a heavy emphasis on automation, code generation, building, testing. It's about 500k LOC. The system repo is like a crypto primitives stack, with bip38, bip39, bip32, a whole bunch, can't even remember them all. If you want to build basic bitcoin stuff from the ground up, you start there. There's a p2p network lirbary and you can build on top of that and do bitcoin protocol stuff... there's a database, which is completely hand-rolled memory mapped files, it's very efficient. There's another libbitcoin blockchain which maintains the chain. There's a node library which basically, it combines network and blockchain with a database to build a full node. It's useless unless you can communicate with it. We do continuous integration on OSX, Linux and Windows. We also have builds on Windows- pretty soon, we'll have autotools builds as well.

KL: Would this be on mobile as well?

EV: With C++, it's a little heavier than C, and you get robust error handling. One of the reasons... the library was started by Amri Taaki and he had his own specific use cases. What do I want to work on and stuff? If I was going to work on it, it had to be C++, even though I hadn't worked with C++ in years. It depends on what type of small device you're talking about. There's been implementations of various things built for mobile and it's not a problem. People have compiled it for raspberry pi or something. What's the bar?  Embedded, maybe what's your scenario? Devices tend to get more capable and the code stays the same. We made the decision at one point-- Amir made the decision to optimize for ssd. He figured why bother. The technology was advancing.  There's a number of... in terms of the node and database and blockchain, it was designed for the most reasonable scenario, not optimizing for everything. And on top of that other stuff, there's a client-server server stack, and there's a proprietary API which allows us to talk wit hthe node, and then you can communicate with your node in a high-performance manner.

KL: For each scenario, you guys need to build a new tool because there is no one-size fits all tool. None of you were finding the right tools, so you all had to build your onw. If everyone in the room did this, then what progress would be made?

LN: Well, by then, the tools will definitely exist. Nobody really intends to reinvent the wheel. I think this space moves too fast to have standards. Inevitably, wallets will have different things on top. Even with bip44, some wallets support subaccounts, others don't. If you try to migrate to a different wallet, you might not get all of the levels of derivation, and that's bad, you basically lose money.

ND; Something interesting I noticed. I came into bitcoin in 2014. Before that, I heard that everything was built into bitcoin-qt. Everything inside one single binary. As time goes forward, what we're seeing is that, as the industry matures, slowly, things get difficult from Bitcoin Core. And my hope is that-- Icame from Windows background. In Windows, you have one big tool that does everything. Recently I am using more unix stuff, learning the linux way, lots of small tools that do one thing well and you just pipe them together and get results. I think that's how bitcoin is moving forward. Before, it waso ne big blob binary-- which makes sense, because Bitcoin was originally developed on Windows. At the end of the day, we should be using small tools piping thiings together in tne right way. At the end of the day, Bitcoin Core should focus on full-node implementation.

EV: Standards develop economically. It's not economically feasible for everyone to be doing development. We've been focusing on electrum for wallet-client server communication. This happened as the internet evolved- there were some standards that were important to talk about and sit down and talk about, but it wasn't mandatory, and people sometimes come back later and rationalize the things that have survived. There are things being factored out of Bitcoin Core's giant binary blob. It's not just Bitcoin Core, many things are designed in that model. There's just too much in one place. Mining, for example, a lot of these pieces.

ND: As a preview of my talk, I talk about wallets, and I think walets weigh too much. I think they should talk to a trusted server which you own. If you have your own server with your own bitcoin node and an explorer you control, then you can use your mobile device to connect directly to it, then...

LN: Has to be optional, not everyone is going to do that.

ND: It needs to be decoupled, like wallet and UI, and hard parts put on other servers somewhere. I think it's easier in the long-term.

KL: Do we have questions?

Q: I wanted to ask about smart contracts as an off-chain solution like second layer or lightning network. I was in real estate industry and I was thinking about off-chain registry for property... but the transactions should be made on bitcoin, and whatever arranged through smart contracts off-chain, gets connected through some specific payment somehow. I don't actually want the smart contract in the blockchain. I'm thinking about off-chain solutions where people open channels, for example.
