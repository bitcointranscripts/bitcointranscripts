---
title: SLP324 Scaling Bitcoin off-chain with Matt Corallo, Alex Bosworth, Lisa Neigut, and Graham Krizek
transcript_by: Stephan Livera
speakers:
  - Lisa Neigut
  - Alex Bosworth
  - Graham Krizek
  - Matt Corallo
date: 2021-11-27
media: https://stephanlivera.com/download-episode/4129/324.mp3
---
podcast: https://stephanlivera.com/episode/324/

Stephan Livera:

So guys, thanks for joining us. We’re talking about off-chain scaling. And so obviously Lightning is the first thing that comes to our mind, but maybe we could start with this idea of What is off-chain scaling? I think Lisa, you had something to add on this, didn’t you?

Matt Corallo:

We had a meeting in the back and we decided we were moving Lightning to TRON. And so we think that’ll scale Lightning,

Stephan Livera:

Right, yeah.

Lisa Neigut:

When you talk about off-chain Bitcoin transactions, like if you have a centralized exchange, how many Bitcoin transactions are happening? Would you call those Bitcoin transactions? Maybe this is a little off -topic, but I think it’s interesting to bring this up because it’s like, Okay, there’s a lot of Bitcoin transactions that are happening across the ecosystem. Some of them maybe we could say have been on ETH so like wrapped stuff. Some of them happen in centralized exchanges or on the Cash App just between two users. But my understanding of what we’re going to be talking about on the panel today is what I would call non-custodial—I dunno, how would you guys describe the projects that we work on?

Alex Bosworth:

I think it’s scaling the properties of Bitcoin. So you want to have the property of: anybody can enter it and you don’t need a central party to run it and nobody can revoke your thing—you have privacy. You want to get all those great benefits, but you also don’t want to have the trade-off of like, Oh, well, if it grows too big, then we have to become expensive.

Graham Krizek:

Yeah. And I would elaborate on that a little bit of really scaling in a Bitcoin-native way, whereas when you talk about scaling through exchanges or custodial services, that’s not like a Bitcoin-native way. That’s kind of the old way of doing things that have their place, I guess. But when I think about Lightning Network or whatnot it’s scaling things that still keep the ethos and the assurances that the base layer brings. And just enabling more things on top of it.

Stephan Livera:

Matt, do you have anything to add there?

Matt Corallo:

No, I thought that hit the nail on the head.

Stephan Livera:

Excellent. Lightning is probably the big one that most of you guys on stage are working on now or known for. So maybe if we could just compare—what do you think the possibilities are with the Lightning Network? People might, as an example, compare the Lightning Network to the payment processors of the world—the Visas, the MasterCards of the world. How would you compare them from a capacity or even transactions-per-second point of view?

Matt Corallo:

I think we still don’t know. Like, the jury is still out in a lot of contexts on how far Bitcoin can scale. But Lightning has this weird concept of pre-committed capacity and you can only send as much as the channel has capacity and like adding or removing capacity you could do, but that takes an on-chain transaction. And so there’s a lot of different games you can play around how you allocate different capacity and how that impacts your on-chain transaction volume. And you see a lot of users who use some of these mobile Lightning apps like Muun, Breez, Phoenix, whatever—you know, you receive funds and a lot of the time that ends up with an on-chain transaction. So then it’s a question of, What is the ratio of on-chain to off-chain? And it depends a lot on user behavior. And then you have to create a bunch of complicated heuristics on the server-side to decide how to allocate your capacity among your users. Lightning is still early, and so the user behavior is going to change materially, especially over the next year or two. And so anything that works now might not work in a year. Either way, both today and in the future, this is a fundamentally hard problem. It’s hard to create heuristics to allocate capital to where it’s going to be needed in the future. And if you get it wrong, it means more on-chain transactions and maybe there’s enough on-chain capacity and maybe that’s okay, or maybe there’s not and then maybe suddenly fees are going up and you’re paying a lot of money for that. And so obviously Lightning can scale Bitcoin 10x from where it is with just on-chain, or maybe it’s 100x or maybe it’s 1000x, but we just don’t know yet. And it depends a lot on solving engineering questions, but more fuzzy engineering questions that don’t have a concrete answer. And if you get it right, then it works really well. And if you don’t get it right, maybe you end up with a lot of on-chain transactions.

Stephan Livera:

Yeah. So maybe as an example, you could get like a 10x improvement or maybe it might be literally thousands in terms of how much you can pack into one transaction. I mean, just as an example, I saw Nicholas Burtey from Galoy and the Bitcoin Beach wallet. Now granted—the Lightning aspect of it is custodial. But as an example, as you mentioned, there were something like 14,000 transactions in a week or so. And that’s like 5,000-10,000 users. And the amount of on-chain transactions was like 14!

Matt Corallo:

Right. And if you pass it through a custodial service, you get—

Stephan Livera:

Dramatic scaling.

Matt Corallo:

It’s when you have the end users with their own channels that it gets very complicated and starts to have scaling questions. If you’re talking about like, How do you accelerate transactions and moving funds between one custodial service and another between exchanges so people can arbitrage, suddenly you’re talking about like, Well, yeah, you just open a big fat channel and maybe you do one transaction a day and it doesn’t really matter how much capacity you have—you have enough liquidity for it. And suddenly it scales basically ad infinitum.

Stephan Livera:

Yeah. Anyone else on the panel want to add something?

Lisa Neigut:

I wanted to add on to something that Matt said, it’s like when you’re comparing speed, you have this like trade-off between taking things off-chain which are fast and then on-chain, and how much of a mix of your transactions end up being—off-chain versus on-chain. And maybe put some timescales around those. So in theory—on Lightning—when you’re doing off-chain transactions, how fast does that go? The answer is: as fast as your computer can send and receive messages and maybe write some things to disk. So at that point the best-case scenario of an off-chain transaction—you’re looking at physical limits of your hardware and your computers in your network and your computer system—

Matt Corallo:

Speed of light.

Lisa Neigut:

Yeah, speed of light. And then when you start bringing in the on-chain transaction things, at that point you start looking at congestion of the entire network, right? Like how many other people are attempting to transact on-chain at the same time, how fast their blocks are getting mined at that particular time period, how much are you willing to pay in order for that transaction to go through. And as soon as you start entering into the on-chain territory, the constraints about your speed of transaction changes a little bit. So yeah, in theory if everything was off-chain—if you could have all of your transactions be off-chain transactions—then yeah it’s the speed of light, it’s the bandwidth that your computer is physically capable of processing. And to compare that to Visa, I think Visa has some really nice hardware—they run mainframes, et cetera. So the hardware that they’re running their transactions on is quite great. I’m assuming they have pretty large—

Matt Corallo:

Yeah, Raspberry Pi Lightning nodes hang all the time. They just sit there and spin for a good few seconds, and then they’ll forward the payment—maybe.

Lisa Neigut:

Yeah. So I think that’s totally a different way of looking at it, but it’s definitely an interesting way of comparing the Visa network to how Lightning Network works. Another thing that’s interesting about the Visa network—I really like looking at things at the nuts and bolts level—the Visa network is really like a couple of nodes at a couple of banks across the country. So the total number of computers that you’re having to touch to run a Visa transaction is probably less than 10. I would be surprised if it’s more than half of that. Like, that order of magnitude. In theory, depending on how well-connected your Lightning payment is, maybe you’re talking to a similar number of computers.

Stephan Livera:

Right. And given the multi-hop nature of the Lightning Network, you’re waiting for this back and forth for that as well. Graham, I wanted to throw it to you because some of the earlier comments were about how it might work on a lower powered device, but also you’re working on this idea of hosted nodes as well. So maybe you could touch on that a little bit and maybe the difference in the capacity of the hosted node aspect versus everyone running on a Raspberry Pi?

Graham Krizek:

Yeah. I think that’s a good point. When you think about Lightning and running your own nodes, what’s nice about the Visa network is: Visa handles all of that for you. If you’re running your own node, well you are responsible for how fast your node can process payments. And much like you said, it’s your own bottleneck. You are resource-constrained by your Raspberry Pi. Or if you’re running it in the Cloud on some bigger server, you can probably do more payments. So it does have a much more direct relationship between the size of your node or the hardware that it’s running on, to be able to figure out how fast you can transact. So when we think about running nodes for a business or someone that has needs, they want speed, they want really high success rates on their payments—things like that—we’ll put them on faster hard drives, bigger servers because they might have a hundred channels and they need it to function really well. And maybe an individual doesn’t need the same assurances—they can run it cheaper and have a little bit smaller payments. So it’s really just all about what you are trying to get out of it and what you want your experience to be. And then additionally, touching on what Matt said earlier too is: a lot of this is still being actively developed. So I think that a lot of the ways that we transact on the Lightning Network today might shift. A lot of it will be fairly similar, but I think a lot of this is still evolving and there’s still a lot of things that are being developed to enhance the network as a whole. So there’s a lot of improvements that can still be made on top of the network as we grow it.

Matt Corallo:

When we talk about how quickly can you push payments through, there is a trade-off here that may be worth mentioning, and that’s privacy, right? So if you deliberately delay the payments, you might actually be able to get some real privacy on Lightning from an adversary who sees the timing of payments flow through the networks. This is a common problem in TOR and other anonymity networks that rely on bouncing something around through a network to get privacy, is that if you see a payment come from here and go to here and come back, and it all happens at the same time and there’s not really many other payments at the same time, you know exactly who sent it and who received it and where it went. So there is going to be some tension going forward in the Lightning Network about how much do you delay a payment to get some kind of batching factor versus how much is that going to cause a payment to be delayed and how much privacy does that gain and what is your policy around that? This is also an interesting open question that we’ll have to figure something out.

Lisa Neigut:

Yeah I think the privacy aspect is an interesting kind of thing. Comparing differences between on-chain or off-chain. The privacy story on Lightning is quite different than the privacy story on-chain. On-chain, all of your transactions are written into a giant ledger. You’re kind of hoping that at some point in the future, no one figures out who your public keys belong to because it’s all on-chain. There’s always this retroactive threat that someone could figure out what your transaction history was and who you’re transacting with just because of the way that blockchains are permanent records, whereas on Lightning, the privacy of your payments is all off-chain, right? So what does it mean when it’s off-chain? It means that the movement of funds is ephemeral and that you don’t really keep track of who’s sending money to who, and we have this privacy thing that makes it—as much as possible—difficult to tell where the payment originated from and where it’s going to after the payment is completed. There’s really no record of it.

Matt Corallo:

Only the nodes that are involved in the direct payment learn about it.

Lisa Neigut:

Learn about it. And the only record is what they’ve written into their private data stores. So if you for some reason had it such that you were deleting certain payment data, it’s difficult to do. No, you can delete—how much can you delete with the verification stuff?

Matt Corallo:

Ehh, it’s kind of there, yeah.

Stephan Livera:

It’s not like an Eltoo. Once we’re in an Eltoo world that would be better, right?

Lisa Neigut:

I think that’s right, yeah.

Matt Corallo:

Eltoo, but also even Taproot. The PTLCs, you get at least a unique identifier for your node, so it’s a little better.

Stephan Livera:

So this also gets into payment de-correlation and stuff. But Alex, we haven’t heard much from you—let’s hear a little bit from you. I know you’re obviously very involved—or at least you were a pioneer in terms of people swapping on- and off-chain. Maybe you want to touch a little bit on that for us? What does that look like?

Alex Bosworth:

Yeah I think it was said before, but you have the limitation of flow constraints in the Lightning Network. So your bottleneck in terms of transmission speed isn’t how many signatures can you do, it’s how much Bitcoin do you have that needs to flow in a certain direction. So that’s the thing that I worked on a lot, is: how can we bring the benefits of both? Like when you hit a flow constraint, how do you deal with that? If I look at my own nodes, I have millions of states on my past channels, and I’ve made probably well under a thousand Bitcoin transactions. So the scaling factor there is 1000x. But if I look over the past year, I’ve probably forwarded $15 million or $16 million, but that’s versus $4 million worth of capacity that’s deployed to the node. So the factor of scaling is really for smaller payments where you can just do a signature. And the difficulty where we need tooling, we need better market systems, is where you go from how much can I stretch this capital that I’ve deployed? I’ve deployed this amount of money and I need it to power a huge size in terms of volume. And that’s the limit of the Lightning Network.

Matt Corallo:

2000 sat payments always work. A few million sats payments—ehhh, not so much.

Stephan Livera:

Not so much right now.

Lisa Neigut:

I think Alex brings up a really good point in terms of capacity for Lightning Network or any L2 really. So L2s are built using lots of little bitty pools of Bitcoin capital that’s been locked into these channels. So at some point—in terms of the actual dollar volume of transactions that are able to happen in Lightning—it’s going to be a function of the amount of Bitcoin that’s been committed to the Layer 2 thing. There’s only 21 million Bitcoin—what fraction of that Bitcoin is going to make itself available to be locked into channels is a big question. And then once you have it locked into channels, is it locked into places that are actually usable? I don’t know how hard it is to predict where payments are going to go. Maybe it’s quite trivial, but having capital deployed to the right places is also going to be a bit of a factor there. To compare it to Visa—because I think this is interesting—so Lightning is a factor of how much Bitcoin is locked into Lightning channels. How much transaction volume Visa can do is a function of how much credit has been extended to the people that hold Visa cards.

Stephan Livera:

Yeah. So it’s a difference of kind, right? It’s credit versus actual settlement. So that’s a big, big difference and I think a lot of people don’t grasp that. For all we know it could be that the Lightning fees will rise. And so it’s like a similar thing. I think Rusty has given a talk on this idea as well, that in the early days of Bitcoin it’s cheap and free and it’s fast, but actually in Lightning world that may change and people will need to understand there the category difference that Lightning is actually settlement, it’s not credit.

Matt Corallo:

You can see a lot of the mobile Lightning wallets that are non-custodial, when the LSP has to extend their liquidity to you for you to receive a payment, some of them actually charge reasonable fees. I mean, it’s still lower than Visa by a large margin, but they charge significantly higher fees than people running around saying Lightning is free, it’s great. And again, we’ll see how that shakes out—what the cost of capital is. But it’s not completely free and it’s remains to be seen exactly where that lands.

Stephan Livera:

Yeah. Graham, I’m curious if you’ve got any views around—so part of what we were talking about earlier is not knowing where that payment is going, and part of what you’re doing as well with Voltage is around spinning up a node for somebody, and I don’t know how much channel management goes into that as well for them. How do you think about that kind of challenge or that problem?

Graham Krizek:

Yeah. I mean we’re trying to come up with solutions to make that easier as we go. We do definitely try to help our customers as much as we can with channel management, deploying where they need it to be depending on what their use case is. Maybe I’m a little bit over-optimistic here, but I think that there will be a day where the tooling will be so good that you don’t really have to think about channel management as much as you do today. Like when you create a node, the first thing you have to do is create a channel before you can even send a payment. And I think that we’ll get to the point in tooling where a lot of that will be abstracted away and you can get up speed much easier and quicker than it is today. So we’re working on some tools to make that easier for people to connect with others and get channels in the network to get up to speed faster. So it goes back to the comments you guys were saying about where do you deploy your capital on the Lightning Network? And it’s really just a function of what your objectives are. And I think that there’s going to be a lot of innovation in that space, like a lot of what Alex works on. There will be a lot of tooling to make this less of a problem than it is today.

Stephan Livera:

Yeah. So Alex, I’m curious what are the hopes then on, as an example, LND Autopilot or this kind of idea of a node scoring so that you know, Okay, when I spin up this node, who am I going to open my channel with? What are the hopes for automation?

Alex Bosworth:

From my perspective, I see specialization as the answer, where you are running a node, but you don’t necessarily need to be a routing node. So if you’re the end user then you connect to a routing node and there’s a big selection for you. Anybody can be a routing node, but you don’t need to do that yourself. And I think that that’s how the market will mature over time. Also on the other side if you’re a merchant, you don’t necessarily need to operate a routing node as a merchant, you can focus on just being a great merchant and you can connect to a variety of routing nodes and evaluate them for performance. And that’s one thing that I definitely work on even as a routing node, is evaluating performance. Is this routing node actually delivering good service to me? And that’s where I see a lot of useful automation tooling coming around because you have so much data. Like this node forwarded this many payments to me and this node hasn’t been active for a while, or it’s a source of errors. So I think that there’ll be more automation around using your own data to solve your own problems.

Stephan Livera:

Yeah. I’m curious, Matt, what’s the approach there around like rust-lightning?

Matt Corallo:

Yeah. So we obviously work in a very different market segment than LND or c-lightning. LND and c-lightning are designed to be a node that you can operate that maybe they have some tooling, maybe there’s some good plugins for doing all kinds of automation and whatnot. LDK (Lightning Dev Kit) and rust-lightning which powers it are much more of a toolkit with which you can build a Lightning node, not necessarily a Lightning node. And so that’s targeted at like—so we’ve had a number of conversations with people who want to build mobile Lightning experiences. And there, you’re talking much more about Lightning service provider models, where you’re gonna run c-lightning or LND on your server to be a routing node for your clients. And then the LDK node will be configured to only open channels with that, or maybe use zero-conf channels, or all kinds of additional features you might provide. So we leave it up to the user. We don’t currently do any work in that space directly, because we have users who have very different models, and Alex does a good job with various scoring here. And users can just use that and not have to—

Stephan Livera:

Yeah. And Lisa, I’d love to hear a bit more from you with the c-lightning and Blockstream approach. Could you tell us a little bit about liquidity advertisements? Like, what are they? How would they work?

Lisa Neigut:

Yeah, so liquidity advertisements—this is in the theme of: there’s only going to be so much Bitcoin available, and of all the Bitcoin available only so much of it is going to be interested in making itself available to Lightning capacity, so to speak. So given this assumption that there’s a subset of Bitcoin that wants to be deployed to the Lightning Network but needs help figuring out where to deploy itself to, the idea with liquidity ads is it’s a Lightning spec proposal, so our hope is that it’ll get adopted by other implementations and then be part of the Lightning spec. So anyone who runs a Lightning node will have access to it. But what it does generally is it allows for anyone who runs a node to advertise that they have Bitcoin on their node that they’re willing to allocate to channels with other nodes. So if you start up a new node, you can basically start gossiping with the other peers, you collect all of these liquidity advertisements that any other node on the network is advertising. You can see who’s advertising it, you can talk to some data providers about, Hey, tell me about this node? What’s it’s reputation like? As a node in the network with my inbound liquidity needs, how much should I value what they’re offering me? And then decide—basically, you pay them for the service of them giving you inbound liquidity. Inbound liquidity—for those of you who aren’t really familiar with Lightning terminology—basically is the ability to receive payments. So this is when you open a channel, the other side of the channel needs to have funds on it, so that whenever you receive a payment, those funds can be pushed to you. So this gives you a way to source from any node on the network. Currently only nodes that are running c-lightning and have the stuff set up exactly correctly [allow this], but hopefully in the future, any node in Lightning Network that wants to be able to advertise liquidity will be able to. And any node that wants to be able to purchase some inbound liquidity from them will be able to do it. So it’s very decentralized. There’s no centralized market. You have to decide how much you want to price your liquidity at on your own. We don’t really have a lot of help for that, but it is super-decentralized. And hopefully it allows people in the market who have liquidity the ability to set up a signal such that people who are looking for inbound liquidity—if they’re willing to pay for it—we hope that that means that they’re going to make good use of it, right? Because clearly they have a use for it. So this is a way of decentralized matching—via a billboard system—who has liquidity that they want to deploy and people who would like to make use of that. I’ll be giving a talk on it tomorrow morning, if you want to learn more about how they work.

Stephan Livera:

Excellent. Maybe a little bit out there as well—as an example with El Salvador, the 6 million people who are coming on to the Lightning Network—you guys are all working on the Lightning Network in some way, shape or form. Do you have any thoughts on that? Does that represent a stress-test of Lightning? Or do you think it’s early days and there’s essentially still a lot of on-chain usage—they’re not really using as much Lightning yet?

Graham Krizek:

It is a good stress test, just to get more people using it. You’re going to find where the needs are of the people and what needs to be fixed and all those things. So it is a good stress test, but a large amount of the El Salvador stuff is custodial right now. So it’s not necessarily stressing the lower level—like the network itself a lot. But it’s really helping a lot of people that are starting to use nodes in a much more serious way, instead of just having these small nodes that do a few payments a day or something. They’re actually doing substantial payments. So it’s a good stress-test—any usage is good. Right now I think it’s more testing the implementations themselves than the network itself, which is good. That’s a natural step in evolving the network, is helping us figure out where are the gaps in these implementations, and then also in the tooling of all of these things.

Matt Corallo:

We’re still obscenely early in Lightning’s lifetime. Certainly volume of payments-wise, and also people saw the CVEs (Common Vulnerabilities and Exposures) that came through a few weeks ago, which can best be described as: prior to a few weeks ago, the security model of Lightning included, “You shall not open a Lightning channel with any Bitcoin miners.” And even today, depending on the exact channel types, that’s maybe a little true. So the security model of Lightning still has a long way to go and we’re still tightening a lot of issues up. So the point about custodial wallets—to some extent today with Lightning, if you want to open a reasonably large amount of funds into a channel that you want those funds back—you probably want to know your counterparty, or at least know that your counterparty is not actively malicious, or you’re not going to put in some amount of work to steal your funds. We’re getting there quickly, but we’re still getting there—and at least make sure they’re not a miner.

Stephan Livera:

Anything else you guys wanted to add around that?

Alex Bosworth:

The whole system is the network. I think it is a stress-test of how easy is it for developers to get up and running? How easy is it for users to get going? So I definitely see the stress right now. Like we’re talking to people in El Salvador who are deploying, and they don’t necessarily care about the technical details. They just need to provide the solutions to people. And I think we do have a lot of people who are falling back to the chain because this is a brand new system that they have to just suddenly wake up and support. And the people who were there already were more familiar with the chain. The chain has the benefit of 10 years of all sorts of libraries and simple ways to access it, and so we have to do everything from the network layer all the way to the user layer to scale that up.

Lisa Neigut:

It’s important to point out more differences between on-chain versus off-chain. And why on-chain is so much easier to deploy and get set up and running is the level of technical know-how that you need in order to interact with any layer 1 typically is a lot lower than anything that you need to run and operate a Lightning node. And the reason for that is a lot of the whole burden of storing state and the connectivity is really abstracted away from you as a transactor. So you as the transactor, all you really have to do is keep track of a few pieces of data on the chain. If you lose it, for the most part, as long as you have your secret seed key, [you’d] be able to figure it out again because someone else is keeping track of it. Because someone else has all the Bitcoin nodes and the networks that have the full block history. Whereas on Lightning, there’s so much more complexity because all of a sudden—and this is one of the big trade-offs between layer 1s and layer 2s—layer 1 is, and the reason they’re so slow, is that the state (which is all the history of the transactions) is in one big place and everyone knows it and you share it with everyone. And so everyone knows what the state is or the history is altogether. Whereas L2, the way that you get these speed-ups is that all of a sudden there’s this localized little history or state that you need to remember, and that takes some level of infrastructure. You’ve got to have a node set up running and that sort of thing. So yeah, it is a lot more infrastructure-heavy to run L2s just in general.

Graham Krizek:

Yeah. The biggest challenge maybe is even people that are familiar with Bitcoin—Lightning is just so different than on-chain Bitcoin. There’s still a hurdle of just learning it and figuring out all of the details. That’s just one challenge is that this is still Bitcoin, but they operate so much differently that it’s still all a big learning curve.

Matt Corallo:

Yeah, you still can’t receive funds while offline. So everyone, especially those coming at it from the on-chain world where they’re like, Yeah, we have this address. We can hand it to someone and then you can send funds whenever. And then suddenly you’re like, Whoa whoa whoa whoa, the recipient has to be online at the same time as the sender. And suddenly they’re like, Wait, what? How do we build a user experience around that? There’s a lot of these things that just require even fundamentally rethinking your user experience in a way that will take some time to come around to.

Stephan Livera:

From an infrastructure perspective, I know that some of the exchanges are getting more advanced around how they do their Lightning. So probably the well-known exchanges who do Lightning are Bitfinex, River, OkCoin, I believe, I know Kraken have said they’re going to do it soon. Anyway, the point is they are doing approaches like having one node in front and one node behind. What do you guys think that looks like? As you were saying, people who are trying to support El Salvador or elsewhere, they’re trying to build a more professionalized-level Lightning stacks. What does that look like as compared to let’s say the typical one guy with his Raspberry Pi, one guy with his box at home kind of thing?

Graham Krizek:

Yeah. We’re working on the evolution now, where previously no one was really putting any sizable amount of money on the Lightning Network and it was fine to just be on a Raspberry Pi. And now people are putting large amounts of money on the network. So that’s being looked at—all of the implementations and figuring out what is the best security models to do access controls for your node and being able to keep your keys. They have to be online but in a separate server or something. So that’s the next phase of infrastructure, in my opinion, is being able to run it with the same assurances that you get when you think about a bank or even just doing cold storage on layer 1 Bitcoin. Just being able to bring in a lot of that same security into the Lightning Network is really where things are headed next.

Lisa Neigut:

This is like one of the projects that we’re working on at Blockstream right now that I’m really excited about, is this project called Greenlight. And what’s so cool about that from an infrastructure perspective is that we’re proposing—so for Lightning, every time a transaction happens, you need keys to be online to sign Bitcoin transactions—this is just the way that Lightning works. Every Lightning node is basically a hot wallet—so all the funds [on there are hot]. And that’s because in order to make use of funds in Lightning channels, you need to be producing signatures for transactions, which means you need keys. So what Greenlight is proposing to do—which is really exciting—is we basically take this requirement for the keys and we move it to someone’s cell phone or a browser extension or some remote computer [that] clearly isn’t going to be processing thousands of transactions or doing anything super crazy. And then we can move the liveness node requirement to a big backend. So we would basically have almost like the AWS of your Lightning node, and when you receive a payment, we spin up a node for you and contact your keys and ask for your keys to sign a thing. But in general, all of the infrastructure of the actual node—keeping up with what payments are coming in for you, that sort of stuff—you can abstract [that] away from the maintenance of the funds, et cetera, which hopefully that’ll make it easier to scale Lightning infrastructure.

Matt Corallo:

Right. And shout out to devrandom and Ken Sedgwick who are working on actually enforcing policy constraints on those signing devices, and the work that they’ve done on Lightning signer project.

Stephan Livera:

Yeah. I recall another related idea: the guys at CoinCorner did this thing called Hoffline wallet and it’s like two Raspberry Pis. And the idea is it’s like a funny little way of having a warm wallet let’s call it, and you could set up policy rules and yeah—sort of related to the idea of having a Lightning warm wallet, if you will.

Matt Corallo:

Right, I think the signer folks want to do similar stuff like that. They’re working on replacing it in the HSM in c-lightning, and you can do it in LDK, and being able to enforce policy constraints on the device that’s signing, which is separate from the device that’s doing stuff like making TCP connection and actually being exposed to the Internet and that kind of thing.

Stephan Livera:

Yeah. And there’s all these considerations around things like redundancies or backups as well. Also latency. So if you’ve got another node behind another—and Lightning is meant to be fast payments, right?—and well if it’s actually behind another layer then every time you’re routing, maybe that’s a slowdown in the speed as well. So these are some of the engineering challenges people are working with, right?

Matt Corallo:

There’s big liquidity considerations there too. And we’ve seen different companies explore different models where if you’re a large merchant or a large exchange, you might run one big node and have big fat channels with everyone else on that one node. Or I know on Zap, every time you create an invoice, that gets put against a different node. And they have a bunch of nodes in the back end that are all freestanding nodes that have their own channels, and you have make sure you send to the right node—obviously the invoice does this—but you can only send to that one of their nodes and not all of their nodes. There’s trade-offs there. There’s models where you maybe have multiple nodes, but you can generate an invoice that works across all of them but then you can’t use MPP (multipath payment). And so maybe that doesn’t work for larger payments but maybe for smaller payments—there’s still a lot of exploration to be done, and a lot of different models that people are exploring and trying. We’ll see where things shake out and what works for people and what doesn’t.

Stephan Livera:

I wanted to hear a little bit more about dual-channel funding. So, Lisa, do you want to tell us a little about that?

Lisa Neigut:

Yeah. So this is a spec proposal that liquidity ads requires, basically. We also call it channel V2. So it’d be V2 opens. This has been a long-running project of mine to change how the spec for Lightning works just for when you’re opening a channel. The biggest change is that—when you open a Lightning channel in the current day, only one side of the channel constructs a transaction, figures out what the funding transaction is going to look like, and where the funding output is, and then tells the other peer. And that’s at the protocol layer of Lightning—this is the protocol that every Lightning node speaks. So what we’ve done on c-lightning is we’ve changed the underlying protocols such that now, when you open a channel, both sides construct a transaction together, and this ability to construct this channel together at the same time means that both sides have the opportunity to put funds in it. Currently when you open channels with things like LND or with ACINQ, only one side will have funds on the channel. But on c-lightning, if you use the funding channel and you both have V2 enabled, both sides will have the opportunity to put funds in the channel at the beginning of it. And this means that you can immediately send and receive payments in the same channel. It’s only a single on-chain transaction, which is really nice. It’s really lightweight. So you get this deployment of capital from two different sides on a single transaction. And we’ve actually written the protocol in such a way that—c-lightning has this command that’s been in there a long time called multifund channel which lets you open multiple channels in the same transaction—and we extended it to work with this V2 version. So you can use multifund channel, and if you’re using liquidity ad—so liquidity ads is a coordination mechanism for the V2 channel stuff, so that’s the way to let people know to put money in the channel for you by paying them for it—so in theory (I haven’t done it) you could definitely do a multifund channel where you lease funds from five different channels all in the same transaction. And so you would open five channels that are balanced to whatever degree you wanted them to be, all in a single transaction on-chain.

Stephan Livera:

So there’s a lot of batching saving there in that way, because now instead of, let’s say as an example I wanted to open a channel, one of each of you—that’s four transactions on-chain I’m doing. But in that model we’re all using c-lightning and then it could be one transaction to open four channels, one with each of you. So that’s a cool batch saver.

Lisa Neigut:

Yeah. And they’d all have funds in both directions. So you could immediately, in theory, send and receive through all of them immediately, which is pretty cool. So we’re pretty excited about it. The people that I know who have used seem to think it’s pretty cool. It’s very decentralized. So all of this happens only between the nodes that are creating channel.

Stephan Livera:

They’re collaborating on the transactions.

Lisa Neigut:

Yeah. I mean I could get some stats, but I don’t have any stats on how many of these transactions have been done.

Stephan Livera:

It might be interesting as well from a privacy point of view that it starts to cut against some of the normal heuristics that are used—this idea that, Ah, common ownership heuristic—if actually now this one transaction represents like five people all creating channels together, then it stops them. Messes them up a bit.

Lisa Neigut:

Yeah the privacy benefits start getting bigger when you don’t do change outputs. So if you put all of the money from your UTXOs into channels then there’s no change.

Stephan Livera:

Gotcha. Yeah. So as an example, let’s say we did that. Let’s say I did a V2 channel with you, Lisa, and then I get some change—or it’s stopping me doing a change output. That’s probably the important one. Because right now, if somebody tries to chain surveil you on the Lightning Network and Bitcoin on-chain, they’re looking at, Oh hey, what was Stephan’s change output. Ah, see that’s his change output—let me see where that goes next. Ah, I’ve got him now. But in this example, if every channel open is a V2 channel, you’re taking away that heuristic. So that might be an interesting privacy benefit there, as well as the scalability aspect because we’re using Lightning. So that’s an interesting one there. I know Alex, you’ve got probably a similar idea there around batching as well with looping in and out but for multiple channels at the same time, right?

Alex Bosworth:

Yeah sometimes people say you can get a scalability benefit by taking a lot of different transactions and then merging them into one transaction. But actually you have to look at the inputs and the outputs. If I’m spending one input and making many outputs, that’s way different from having many different transactions that are all spending one input and having one output and then just joining them together into the same transaction. So it’s a difference probably between a 5% increase and it may be a 500% increase. So you have to think about it, not just like, Okay, I’m reducing the number of transactions. But I’m reducing the on-chain footprint—and that is the idea behind Loop. The idea is that you have very long-lived channels that are staying around for a year or two years. But then you have liquidity needs, like maybe the balance is just shifted too much. And that also plays back to the security needs. Maybe I don’t need to have a big hot wallet because I’m a merchant. I need to get those funds over, but I don’t want to just be closing all the channels with all my peers—I want to be maintaining those good channels that I have with them. So that’s where we get a lot of usage. We say, Okay, just find your set of peers who are delivering great service to you, monitor them, make sure that they’re continuing to do that. That’s a decentralized process—you can pick any peer you want, and then you use a Loop service. And what we do there is we do batching. So we have mega inputs, we have the big input, and then we create swaps with all the people and we delay it. So we say, Okay, unless you pay us extra, we’re going to match you with a bunch of other people, and they’re all gonna make swaps—so: many outputs, and one input. And then with Schnorr—with Taproot that’s activating—we’ll be able to create new forms of how we actually create these swaps so that we can represent everybody’s keys in these swaps. But actually on-chain, it’s only going to be one key, one signature. So I think next year, that’s something that we’re investing a lot in—reducing our on-chain footprint there.

Lisa Neigut:

I had a question about the Loop stuff. Well, two questions. So I’ve never used it, and that’s because my understanding is it’s LND only. Have you guys made it available for other Lightning implementations?

Alex Bosworth:

Actually, I’ve used it with c-lightning before. Because the concept is just: you get a payment request. So the idea is: I get this payment request and it’s locked to a hash. And then the server sends on-chain some funds to the same hash. And what you need to do is you need to present the pre-image—so the user creates a secret—and they use the secret to take the funds on the chain. And that’s actually something that anybody can do because the server has no idea who’s paying. That’s an interesting aspect of how Loop works, is: we actually have no idea of who the customers are because they’re all paying us through the Lightning Network. So all that we see is: we generated a payment request, somebody paid the payment request, and somebody swept it on-chain. So there’s multiple implementations, actually, of the client. And we have a reference implementation that does work with LND and it’s MIT-licensed. But that’s something that maybe we could explore in the future of like, How can we decouple it? And we have already done that with Loop in. So the way the Loop in works is—you can use LND with it—but you could also use it with any generic exchange. You can just have them generate an on-chain address. And then you send to the on-chain address and you’re auditing the on-chain address. You’re saying, Is this on-chain address actually an HTLC, and it does it include my key? And does it include the correct pre-image and the correct secret? So that’s something that we can maybe expand, although yeah—we’re working on lots of different projects.

Lisa Neigut:

My other question about Loop is: so you mentioned that it was really useful when you have a lot of peers to rebalance the balances that you have with your existing peers. Again, I brought up the fact that I haven’t used it because I don’t know a lot about the current architecture of it, but do you guys only have one node that is the Loop node? Because I would imagine that that makes it difficult for all the nodes that are connected to it. If everyone’s pushing money over to them to do loop outs or whatever, wouldn’t that have an adverse impact on the balances of all the channels that were on that path to do rebalancing? So the question is: do you guys only have one Loop server, or do you have a bunch of them throughout the network?

Alex Bosworth:

Fewer Loop servers is better from the cost perspective, because what we want is for the peers of the Loop server to create enormous channels that can forward enormous amounts, and then close and aggregate all of those different Loops into one on-chain transaction. And we also want to of course have the traffic flow in the other direction. But in order for traffic to flow bi-directionally we need to have capital that is going to allow for wait time, because traffic isn’t going to flow bi-directionally [with] every transaction. You’re maybe going to have to have a buffer. And we also need to improve the services that we have and the pricing that we have around the movement in the other direction. So currently—yeah, we do have a situation with the Loop server where if you peer with a Loop server, number one, you need to have a large channel—our minimum channel size is the maximum channel size of the standard channel. And it’s recommended that you probably do 10 times that. I would think of it as: if you have inbound liquidity that’s in excess on your node—you have too much inbound liquidity—Loop is a great peer, because you can charge a routing fee to pay the Loop. And what we’ve seen develop is an organic market. People recognize that, Oh, if I peer with Loop and I have a lot of excess inbound liquidity, I can reduce my excess inbound liquidity, somebody else who wants it is going to buy it, and they’re going to buy it through me and pay me that. And that’s also going to ripple out through the network. So their peers are going to have the same experience. Like if too much traffic is going to them, they’re going to have a similar experience. And that’s the challenge of Loop. We can’t just build a one-on-one liquidity service. We need you to be able to get liquidity from the broad network. And it also ties Lightning Labs’s business model to creating a diverse network. What we want is for this liquidity to be something that you need to have as a global network—not just as: you buy it from one peer and you only transact with them.

Stephan Livera:

Yeah. Very interesting to think about. We’ve got about 10 minutes left, so maybe let’s start looking at some of those more future ideas that might be interesting as well. Like I know Christian Decker has written about this idea of multi-party channel, aka channel factories and things. Maybe you guys could tell us a little bit about your thoughts on that, or what do you see as the future of Lightning and off-chain scaling? Anyone?

Matt Corallo:

Yeah, channel factories are awesome. They obviously continue the constraint that everyone’s online at the same time. So that’s particularly annoying. One of the really great things about channel factories is—you’re not talking about like large merchants who have a lot of liquidity and they can put it in big channels—you’re talking about smaller amounts of liquidity that you want to be able to more dynamically rebalance across channels. So maybe individuals who want to create a payment pool and do liquidity-sharing across channel factories and split that liquidity up across their channels dynamically. And sadly, once you start talking about individuals, you start talking about online requirements and then things start to fall apart. It’s like, Well, I wanted to run it on my phone and my phone’s not always online. And so that falls apart pretty quickly. But we can save it—we can get back a lot of that utility with covenants. So features in Bitcoin on-chain to enable much, much more expressive things. And we can use those as primitives to build much fancier Lightning models like channel factories. When we start talking about large, large LSPs, you want to talk about how far can you scale being a large LSP like Breez or Muun or Phoenix or whatever. That’s a really hard problem—How do you scale that liquidity? And one thing you really, really want to be able to do—which you can’t do, again, because of this online requirement—is dynamically rebalance your liquidity without on-chain transactions, or at least with minimal on-chain transaction footprint. And there are a lot of potential avenues there that require covenants, where you can do a lot of really cool stuff, but you can’t do it today with Bitcoin as it exists today. But hopefully we’ll be able to do it with one of these like CHECKTEMPLATEVERIFY or CHECKSIGFROMSTACK or TAPLEAFUPDATEVERIFY. There’s a few proposals in that space right now, and needs more engineering time and more research and more whatever to get there. But I’m particularly optimistic in stuff in that direction, because again, I look at Lightning a lot because—where LDK fits into the picture—is I look at it a lot through, How do we get end-users who don’t actually want to buy a Raspberry Pi and keep it online all the time? I mean, I know maybe people in this room love that, but it turns out most people like to use phones or whatever. How do we get them a good Lightning experience that’s not custodial? And right now the answer is custodial or these LSPs that work, but you can’t receive while you’re offline. And there’s a lot of hairy problems there. And how do we get them to be more capital-efficient so that they can charge a lower fee? So I view a lot of things through that lens and there’s a lot of upcoming work in that space that I’m excited about.

Stephan Livera:

Yeah. Very intelligent comment.

Graham Krizek:

Yeah. There’s also a need—as we do all of these new things on Lightning at the protocol level—there’s also a big need of easier tools and developer tools and all these things just to get up to speed on usability of Lightning. And we’re working on a lot of things in that department. And that’s just a big need across the network. There’s a lot of protocol level improvements that can be done, but then also allowing a lot of people to get up to speed easier, but then also doing more participating—like maybe you don’t want to be a big LSP and you want to let others participate with liquidity ads or pools, and leverage those to get liquidity for your users. There’s just more tooling around the space outside of the protocol level that we’re looking forward to.

Matt Corallo:

Totally, yeah. And that’s a conversation we’ve had with some of our users is like, I want to add Lightning non-custodial to my wallet—and I don’t want to be the one that run the LSP. And you’re like, Well, I mean, you could let your users do manual channel management and open with a bunch of different people, but you can’t do zero-confs. And so: where is the open source LSP in a box? That’s a long ways away. And tooling like that. And how do we enable people to build—especially non-custodial experiences around Lightning that obviously you guys are great with, with merchants and hosting stuff—and then when we talk about end-users, it’s a long ways away from really enabling developers to do that stuff from scratch without a ton of legwork.

Lisa Neigut:

We’re an off-chain panel, but all of the improvements that Matt was pointing out are all on-chain improvements, right? So to some extent, a lot of the stuff that moves off-chain stuff forward really depends on improvements on the chain layer. So that’s definitely something that we’re very happy that there’s a lot of really smart and great people that are working on the layer 1 stuff. And yeah, covenants will be really interesting with that.

Matt Corallo:

And package relay, so we can finally fix the Lightning security model and make Lightning actually secure.

Alex Bosworth:

We need hats.

Graham Krizek:

So what I was really curious about—because I haven’t heard your comments on this—but BOLT 12, like yay/nay, too much? What are the thoughts on BOLT 12?

Matt Corallo:

BOLT 12 is awesome. I mean, we’re going to talk about it in 15 minutes. We’re going to have a chat with, well, BOLT 12 specifically, but with Andre who skipped our panel and I’m not mad at Andre. But Andre and I are going to chat especially about receiving while offline and this issue that’s cropped up with like Twitter—you can only receive tips if you opt into a custodial service and KYC yourself. And how do we fix stuff like that? And I guess from my naive view before I had spent any time with BOLT 12, I was like, Oh, BOLT 12 probably fixes a bunch of this stuff. And it’s like, Actually, no BOLT 12 was just scoped smaller, and I think it’s gotten scoped even smaller. Like I think Rusty now wants to talk about deploying it without recurrence. And so to get it there, it’s gotten scoped smaller and it relies on these onion message primitives which I think are going to be critical. I had this back of the envelope proposal for doing offline payment receipts or like partially offline payment receipts which I think might be cool eventually, but first we need onion messages. And onion messages are also needed before BOLT 12. And so it’s still a ways off in that sense. And sadly, I think all of the Lightning implementers have just been too busy with other stuff to spend a lot of time on spec, except for maybe c-lightning?

Lisa Neigut:

ACINQ has a draft PR for Offers.

Matt Corallo:

Cool. Yeah. They’ve had a little more time. Yeah. We’ve been massively underwater. LND I know has been underwater on trying to do more business stuff or work on Loop and other products than just work on LND, moving the spec forward. And so there’s just been a lack of that, but they are trying to hire I know, c-lightning’s trying to hire, we’re trying to hire, so there’s more headcount coming in that department. And then I think from there, hopefully, we can accelerate some of that and get things like onion messages broadly supported. And then from there we can build new, cool stuff based on it like BOLT 12 and maybe offline receipts. There’s so much to do in the spec department, and there’s just so few resources there. And I think everyone with a Lightning implementation right now is hiring. So if you’re an engineer and you know something about Lightning or want to learn about Lightning, talk to anyone with a Lightning implementation because they have a job for you.

Alex Bosworth:

Yeah. I mean, even just the Lightning industry, I mean, people who are building solutions like Voltage, there’s so many opportunities to create new companies based on Lightning. And so many people who already have companies, they need help to integrate Lightning and make it work.

Stephan Livera:

I think we’re down to the last five minutes, so let’s just get a final comment, yeah.

Lisa Neigut:

Okay. So we’ve been talking about on-chain versus off-chain stuff. One fun way to think about L2s—L2s fundamentally require Bitcoin to be locked into them to make them functional at all. So in some ways—I know people buy and invest in Bitcoin for a variety of reasons—but I just want to add to your list of reasons to invest in Bitcoin, and that is that at some level it is a way of participating in or deploying capital to these layer 2 networks that are going to require people who hold Bitcoin to commit it to these networks in order for them to succeed. And if you think that in the future Lightning Network will be a very big payment network and there’s going to be a lot of traffic, as a Bitcoin holder that means that there might be opportunities in the future for you to participate in some of the fees that are generated through Lightning. That’s very probably controversial or whatever, but I definitely think it’s interesting to think about when you’re valuing like, What is a Bitcoin worth?

Matt Corallo:

This poor guy has had his hand up for like—

Stephan Livera:

It’s gotta be quick. We got to wrap up. Just come up to the microphone just up there. Super quick though, because we’ve got about a minute left on this panel.

Matt Corallo:

I didn’t have anything to close with anyway.

Audience Question:

What is the priority or timeline to get Taproot?

Stephan Livera:

Yeah. So the question just for the stream: What is the priority to get Taproot on Lightning?

Matt Corallo:

I think again, there is a significant lack—there are definitely not enough resources right now on Lightning spec implementation work. I think maybe with the exception of c-lightning—Lisa’s gonna start kicking me here in a second. But they focus a little more on that and I think others maybe have been behind on that because we’ve had other focuses and are trying to hire for that and then move that forward. There are so many spec changes coming in Lightning—messages and whatever. So I don’t have a number—two weeks?

Alex Bosworth:

And it’s not just one Taproot integration. There’s many different ways that Taproot is going to interact with Lightning.

Matt Corallo:

Right.

Lisa Neigut:

We’ll be talking about this a little more on the Socratic Seminar tomorrow. So come hang out.

Stephan Livera:

Excellent. Well guys, I think that’s about all we’ve got time for. So can everyone put your hands together for our panelists: Matt, Lisa, Graham, and Alex—thank you.
