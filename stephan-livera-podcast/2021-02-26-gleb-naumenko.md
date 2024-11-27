---
title: The Label, Bitcoin Dev & Consulting
transcript_by: Stephan Livera
speakers:
  - Gleb Naumenko
tags:
  - lightning
date: 2021-02-26
media: https://www.youtube.com/watch?v=gqDB0e5irdQ
---
podcast: https://stephanlivera.com/episode/255/

Stephan Livera:

Gleb welcome back to the show.

Gleb Naumenko:

Hi, it’s good to be back

Stephan Livera:

Glad you’ve been pretty busy with how you’ve started up a new Bitcoin development venture and you’re up to a few different things. Tell us what you’ve been working on lately.

Gleb Naumenko:

Yeah, last year it was like, I think it’s been maybe half a year or more since I came last time, I’ve been mostly working on actually lightning and related stuff like research wise, breaking lightning and fixing some existing issues. And yeah you can find my work on my Twitter. That was pretty exciting because lightning has so many new opportunities to explore stuff like unsolved problems for Bitcoin. It’s also true, but Bitcoin is a bit more mature. So for lightning it’s even crazier apart from that. Yes, we can talk about that separately. We’re starting this new thing with Antoine called The Label. It’s going to be a really small team. We are thinking like four people at most to be very efficient.

Gleb Naumenko:

We have these two directions. One is to keep working on Bitcoin, sometimes working separately as we do all the time. Sometimes having some joint projects, like most of my research projects in lightning was together with Antoine because he has more experience there on how it actually works. I have some new high level ideas, which nobody seems to be ever discussed or discussed, but it was a visit to use them. The second part would be consulting businesses or HODLers, or like whoever needs help with the advanced Bitcoin features. Like let’s say, We all know that’s quite problematic sometimes when they don’t integrate SegWit or lightning lately. There is a lot of complaints about that. So people are waiting. I think this venture is, it could be an answer to that. Like how to facilitate that process. How to stop exchanges from being hacked, how to stop, how to help users to be more, to use more privacy features while not just facilitating them from the core side but also from the wallet side, for example, or something.

Stephan Livera:

Yeah. So helping that exchange implement some kind of feature, you mean things like that?

Gleb Naumenko:

Yeah, right. Also there’s like this new and new protocols coming up, like I saw just this morning and some new statechains implementation, which would facilitate lightning faster. And just building, helping those projects, building their protocols more secure is also another direction where we’re exploring.

Stephan Livera:

I see. And because with many of these, it can be quite complicated, the different rabbit holes that you go down in terms of are there ways that someone can cheat the other party or some way that it’s insecure or some way that you can try to mitigate or change the level of trust required in, especially in some of these ones where you are reliant on other people. And I think this is something you probably are really known for talking about is some of the stuff that kind of happens across layers, right? So things like some lightning that requires you to be able to watch what’s happening on the blockchain and make sure you respond in time and get your response in, that kind of thing. Right?

Gleb Naumenko:

Yeah, definitely. It’s very difficult to make this correct from the first attempt before getting hacked. So, and there are two aspects to it. One is like theoretically, how to build the protocol and that’s what I cover. And then the second is how to actually implement it properly. Like without some implementation bug. And that’s where Antoine is mostly known for. He’s like published like 10 CVEs, which break lightning over the last year. Some of them are probably not known yet. We have this expertise trying to cover most of this stuff. If we get to invite somebody else, if this thing like works out super well, and there’s a lot of demand, we’re also thinking of onboarding probably a cryptographer. Like there are a couple of names who would cover that part and somebody who knows hardware. That’s my intuition so that that would match our team and provide like coverage on any single question. Possibly people can be interested in.

Stephan Livera:

So what’s the setup here? Is it essentially like a kind of cypherpunk development organization or what’s the, what’s the structure

Gleb Naumenko:

It’s like super flat. We’re not planning to hire many people and to manage anybody like we might find somebody like help with hiring. For example, let’s say there is an exchange which wants to get lightning. We might tell them to find developers and then help those developers, but we’re not going like manage them. It is pretty like dictatorship based like yesterday, there was a like Russian speaking outlet talking to me about this. And they asked who going decide who is joining this venture. It’s just two of us are going to decide, but we are also very happy to help somebody else to set up something similar and share our experience.The big part is so as I said, we want to be as efficient as possible. Meaning yeah, there is no management, no bureaucracy just by default we’re independent, trying to get different funding from different sources. Sometimes when it makes sense, we collaborate. If somebody needs more attention than one person can provide, we can work together or we consult with each other. I said the experience like our background is pretty complementary that’s the goal. Just having a small team of independent people collaborating when they need to. Cool.

Stephan Livera:

This organization, I understand it is going to be remote only. Is it going to be like Bitcoin only in terms of funding and stuff, or you have Fiat options or what’s the plan there?

Gleb Naumenko:

There are two parts to funding. And I think that what is really different from other, other similar projects in this space that Ferris to be a, gonna keep accepting grants for open source, like Bitcoin core or lightning development, like as we do now, like me from BitMEX and Antoine got funding from John Pfeffer and now you’ll see some new announcement next week about him, a second part to this to the open source finding, I think we would like to try to facilitate some per project finding where somebody says, okay, I want to fix this. I want this particular problem to get fixed. Like, for example, this channel jamming on lightning. There is our idea. Then there is used, came up with something different how to fix channel and on lightning. And we would like to see somebody like showing up and saying, I want to sponsor this.

Gleb Naumenko:

If they’re just getting dollars and please, can you try to focus on this, like on the next month? So that’s not there yet. It’s a rare thing. It only happened, I think with Chris Belcher working on what is it CoinJoin?

Stephan Livera:

CoinSwap.

Gleb Naumenko:

CoinSwap. So, yeah, so seeing more of that would be cool. And then we can focus our joint efforts on that. The second component to our finding is consulting fees. Which would be, yeah, just, just well, we are like super Bitcoin bullish and we, I’m pretty sure we will give stack in Bitcoin or not. I don’t know what Antoine is doing. We don’t discuss this then, but we’re probably going provide discounts for Bitcoin for people for when I pay in Bitcoin. But yeah, whatever, whatever people can do. I know there are like some of American exchanges are like regulated companies and they probably cannot make those payments. So yeah. We’ll see how it goes.

Stephan Livera:

Yeah. Gotcha. It’s an interesting how a lot of people seemingly seeing issues around getting a normal Fiat banking right. So I remember John Newbery mentioned this also when he was trying to set up Brink that he was finding these kinds of issues. So obviously the Bitcoin option is the ideal solution but obviously not feasible for everyone. So let’s talk a little bit about what you are hoping to focus on or what you’re interested in. I think you are mostly known in the space around peer to peer aspects of Bitcoin, correct?

Gleb Naumenko:

Yeah, I’d say so. Although like with lightning, my experience over the last year was wider and I was thinking how there’s attacks where Bitcoin and lightning work together and you try to break a bridge between them or somehow affect one thing to steal money from another thing. So I’m trying to expand it to, so now I’m referring to this as high level problems. Like those problems you draw on paper, like making python tests like very high level where there is no notion of Bitcoin whatsoever, or there are just nodes which sends something or do something like for example, there’s this whole like direction. I see, I’m thinking of lately of doing side chains. We all know Liquid, but what if you change a Federation with something else? So that’s also a high-level problem. Like how to make a new consensus for a side chains. There is like a bunch of different ideas around that. And actually one of my first like consulting contracts, I got just before announcing it was focused on this thing. I think it’s pretty cool. And we’ll see more of those in the next year. I like new kinds of side chains. Those high-level ideas, not just peer to peer, but of course I still enjoy working on peer to peer.

Stephan Livera:

Of course. I wasn’t saying you only do peer to peer. And so in terms of the cross layer stuff, I guess let’s go a little bit further into some of those and maybe chat a bit more in detail about how some of those things are operating and how to think about some of those things. So maybe, I guess if we started with like a more example that people might know about, right. So I think you were talking about the interaction between Bitcoin and lightning, and so this idea of the time dilation attack could you tell us a little bit about that?

Gleb Naumenko:

Yeah. Okay. So before, since like 2013 or something the eclipse attack was known against the Bitcoin. There was no lightning at that point. It’s when you eclipse a node you occupy all of its connections. So a Bitcoin node makes eight connections to the network. If an attacker controls all eight of them and that’s difficult, but under some conditions it’s possible. So if they do that, they can do a lot of bad stuff. They can double spend the victim because they control of the chain of the victim. So they can feed you the fake blockchain or pretend that there is no blocks or something, so they can double spend you, they can mess up with your mind in, for example, you’re a miner or you’re trying to submit a block to the network, but they just delay your block for 30 seconds.

Gleb Naumenko:

So that’s some other miners going to be faster than you now. They can obviously spy on you because they see all the messages you send and receive. So that’s what we knew before, with lightning. It turns out that and the defenses against eclipse, we are always focused on this aspect. Like for example, for double spends and attacker will have to produce a new chain. That’s why there will be like, they cannot get a little cachet that once that means that the blocks will be slower, but the Bitcoin core has protections from that. Like if blocks are like, too slow the node starts to search for new beers, and that’s how they can break, break from eclipse. So we came up with this idea that for the lightning, it’s very important to act on time, because if you’re a counterparty, if you’re like channel a counterparty tries to settle some previous state like example, I paid you $10, but then I tried to settle on chain, the state previously to that when I didn’t pay, you’re supposed to react, you’re supposed to go on chain and send the punishment transaction, which would, which would give you actually reminders. So you’re supposed to watch when to the chain for those activities, but if you’re eclipsed, that’s the same problem. You just don’t see it. But, but what if instead of eclipse and then attack or just feeds you blocks slower. So normally you’re getting blocks on average every 10 minutes. If you get, if an attacker just sends you a blocks, every 15 minutes, it’s very difficult to detect because like statistically, I think seven blocks a day are longer than 30 minutes. So it’s very difficult to say that something’s wrong going on. If an attacker is good enough, if they just been a bit slower, like five minutes, slower per block, but at the same time after 10 blocks, you’re like one hour lagging. And if you didn’t submit this punishment transaction during that one hour, your funds are stolen because, you can’t find it on the, during a certain time. So if they force you to be late, then, then your funds are gone and we explore how this is possible and to reach actions, Bitcoin core and lightning should do to prevent this kind of things.

Stephan Livera:

It’s really fascinating when you think about how that works. And I guess there may be different ways to like, people could try to defend or think about how they stop that attack. Maybe they have multiple ways of checking the blockchain and so on. But I guess, firstly, how feasible is that kind of attack? Like, would it require somebody to maybe an example would be they. If you had like a malicious version of Bitcoin core that you installed and it had the wrong peers, the wrong peer data, and you only calling out to the, basically your evil peers. So they’re the ones feeding you the bad blocks, is that like one way it would work or how likely and how would that kind of thing happen that you got into that scenario where all eight of your connections were bad ones?

Gleb Naumenko:

Yeah, sure. Like natively in Bitcoin, that’s quite difficult now because we put a lot of effort into not allowing this. My asmap projects. I think we discussed last time of diversifying peers across different internet providers just makes that very difficult against normal Bitcoin, unless your internet provider itself is malicious. If you’re like connected to one internet provider and they mess up with you have no like, no hope basically. Well, you can be a bit more smart than just a ringing the bell, like having an alarm where something goes wrong, but that’s as much as you can do with lightning, the big problem. I think what makes it really feasible is that lightning often uses light clients. Light clients are those a small Bitcoin nodes for mobile devices, which don’t store the entire blockchain and don’t download entire blocks.

Gleb Naumenko:

They just download block headers. And then if they see that there is some protocol helps them to realize that some block contains their transactions. So they see that the block contains their transaction. They ask for a full block to see the transaction and to verify it. So the problem with that, and there is very few nodes which support lightclient protocols, because it’s a bit more advanced than normal Bitcoin core what we do in the peer to peer network. It’s not enabled by default. That’s why there is not so many nodes on the network. We should do that. Like, I think only the a hundred or a couple of hundreds like the serving nodes, there is a lot of clients, a lot of mobile clients doing that. I think 10,000 or more, but only several hundred are full nodes, like serving them.

Gleb Naumenko:

And just yesterday on Twitter, somebody told that his node with that feature enabled, like the server side was spending one terabyte per month on serving light clients while normal node spends like a thirty times less. So it means that like a lot of clients were connected to just one person. And if that person was malicious, they can do everything. Light clients also tried to do many connections, but if there is a little choice, there is no help. And at that grid can spawn like 1000 nodes tomorrow, and then it’s very likely that they will eclipse some of the victims

Stephan Livera:

Yeah, tricky. Hey, it kind reminds me of how people talk about the whole the surveillance Electrum servers. Right. And the idea is that the surveillance companies have an incentive to run the surveillance Electrum server to try and figure out everyone’s data. And I guess maybe that’s a similar dynamic, a where if you’re trying to surveil,

Gleb Naumenko:

it is very similar.

Stephan Livera:

It’s like, you could be the surveillance, yeah go on –

Gleb Naumenko:

Actually eclair. Like it’s one of the most popular lightning implementations for their Phoenix wallet. I think they use Electrum or Electrum protocol they might be using. They might be used using like dedicated servers, like not connecting to random people in the network, but use their own which makes it a bit better. But still, yes. So it’s very relevant. You’re right.

Stephan Livera:

Yeah. So I guess even in that example with Phoenix, I think you can set for example, your own Electrum server, but I think it does just, I mean, If they’re maybe if they’ve coded in their own list of quote unquote good Electrum servers, maybe that’s something there. But yeah, you’re right certainly that’s, that will be a lot of people coming in who will just use a quote unquote, easy lightning world where it’s all set up and all good to go for them. And that means it might mean Phoenix, or it might mean Blue Wallet, the custodial lightning version of it and not the non-custodial lightning version. So yeah, certainly an interesting aspect. So how do you kind of see that ecosystem building out?

Gleb Naumenko:

We started on it needed to think about it more. It’s a shame we don’t have. I know the Coronavirus thing, but it would be so helpful to have a core dev meeting at this point where we can talk about priorities for future, because I think that’s worth discussing. I think lightning light clients might need much more attention. I had, I just, yesterday there is a hackathon in where I’m from it’s not Bitcoin it’s like broader. But I’m thinking of hacking a solution for a much faster light clients now and more secure based on zero knowledge. So basically what you do is you can verify that you’re on the valid blockchain and the server feeds you the valid chain. But in a very compressed way, you don’t have to download entire blocks because like, there are issues with it, even with headers, there are problems with syncing up.

Gleb Naumenko:

So I think like part of my attention next year will be on light clients not just making them better, but just go in and review and that they do everything correct. Because last time is I looked at neutrino, I think it’s like btcd light client. I think they like address management is pretty, pretty bad, meaning that the database of other nodes in the network they store it’s like, it’s easy to trick, I think. Or there were some other issues. Well just going and looking at what are the current projects and trying to help them. I think that will be one of my priorities next year.

Stephan Livera:

I’m also curious as well. So you mentioned earlier around the lightning channel jamming attack and how you had a different approach to Joost Jager’s approach. Can you maybe start with just an overview? What is the channel jamming attack? And then tell us a little bit about how you were thinking on mitigating it. Yeah.

Gleb Naumenko:

Yeah. So since the lightning network is permissionless and also anonymous, I can send the payment to myself, let’s say through five hops. And then on the receiving side let’s say I pretend that I went to offline. So the while, while they nodes which facilitated this payment, like they’re out in nodes in between cannot fail it immediately because they cannot assume that the well, everybody is very responsive, so they cannot fail immediately. So they have to hold on their coins, which were used for this transfer because like, while, you’re routing you freeze the coins from one side, like you move them from one side to another, but you keep them in flight. So that’s why to do basically paralyze part of the route you just like on the receiving side, you pretend you’re offline or you just don’t respond if they implement nd then they cannot charge fees for that until the payment is past because currently in the light and we charge fees on the first successful payments, it cannot really be solved with just fail in payments in 10 seconds. Let’s say for out knows, because an attacker can do the same thing in 10 seconds. The, one of the, like the crappiest part about is that let’s say an attacker can dedicate one Bitcoin to this attack effectively because they can use up to 20 hops in the network. That means that like collectively with one Bitcoin, they can jam 20 Bitcoins because like one Bitcoin on each hop and that’s like, even if they have enough effort. They can paralyze the network. Some routing nodes can paralyze other outer nodes to take all the fees, for example.

Gleb Naumenko:

So that’s clearly a problem and it’s very real, like used to thinks it’s the most important problem with lightning and we need to take immediate action to it. I think not that many people look at it at this point, unfortunately. So Joost’s idea, it’s based on previous discussion on let’s take fees, even for failed payments. Like when you just start the route, you just pay a small fee. So that’s an attacker cannot do this all the time. And too often that’s a bit problematic because honest users will have to pay like zero fee. And now an attacker can be a routing node, which fails the payments on purpose just to collect fees. So let’s say an attacker controls, two routing nodes in a row on the second. Now they fail the payment. But the first node, then will take the fee from the sender.

Gleb Naumenko:

And that’s the way to steal funds from honest clients, there might be some solutions in the updated versions of this proposal to this particular problem. But generally I think I’m not sure this is an ideal solution. Our alternative, is to use a zero knowledge proofs. So we have this idea of some kind of reputation system where reputation is based on the UTXO. When you send a payment, you prove to them. The routing nodes that you own some UTXO in the network. If you do the second time and third time they see, Oh, this guy sends a payment based on the same UTXO ownership like why does he send payments every second? Currently, it’s not possible to tell that the sender is the same because in routing nodes only aware of the previous hop and the next hop that’s done for privacy, but now we can attach this blinded UTXO fingerprint to every payment.

Gleb Naumenko:

So zero knowledge proofs are needed so that we don’t commit to a particular UTEC. So, because then you can associate payments easily. You can tell like.

Stephan Livera:

that Gleb owns this piece of Bitcoin, this UTXO, right?

Gleb Naumenko:

That’s something like that. So we need to blend it somehow. There is this idea of committing to some UTXO from a set, without telling which one and idea is how to use these proof to solve this problem. And then like, let’s say you show this proof, you get credit for 100 payments or something. If you do, if you want to do more than 100 payments a day, sorry, but you need another proof or like, something like that, like you need another, UTXO or,

Gleb Naumenko:

Or if your reputation is good and you made good payments last like yesterday, and they all were successful. We will increase your reputation based on this UTXO, so that’s the idea. The problem is that zero knowledge proofs are pretty experimental, and we’re still not sure if we want to put them in the kind of core protocols over the lightning network. I think it’s totally possible that we’ll have these alternatives. If you want to route you can pay fees up front, or you can use it as a zero knowledge proof. I think that’s pretty cool.

Stephan Livera:

Gotcha. So in that example, what about people who are genuinely doing lots of payments? I mean, an example might be someone using Sphinx app to stream payments, to pay for every few seconds of podcast they listen to, or I don’t know, maybe some of the lightning gaming people, I wonder, does that break somebody else’s use case?

Gleb Naumenko:

We should think about use cases more because so far we were more designed in protocols for general payment thing. Like, let’s say, you pay for beer five times during an hour, and then you go like rest for the go to sleep or something. But, so I think, well, as long as your payments are successful, everything’s good. Like, you don’t waste your reputation on the, on the successful payments. You just got get more reputation. So, it should be fine.

Stephan Livera:

Yeah. And then on the zero knowledge side, again, I’m not an expert at all on this, but from what I understand, they often have like more computational load or there’s more kind of other tradeoff in other ways, like, would that work with say mobile lightning nodes and things like that? Or would that just be like still within the tolerable or reasonable ranges there?

Gleb Naumenko:

Yeah. So that’s definitely what we should consider when we implement these protocols. Fortunately some of the zero-knowledge constructions are fast and small while they need a trusted setup, which would be not acceptable for like Bitcoin core layer, of course. But in this case, I think it’s pretty fine because in this case, there is only the one prover and one way or far verifier. Unless like ledger system based on zero knowledge where verifiers this, everybody. So if you join late, you cannot be confident in the trusted ceremony here, when there is on the one prover and one verifier, it’s totally fine to use any construction, like where just the two can can contribute to the trusted setup. So that’s why I say we can use almost any, any zero knowledge protocol and the most efficient yeah.

Stephan Livera:

And with the whole idea of having a reputation in the lightning network, and people talk about things like, Hey, having a web of trust idea. I see some people try to push back there because they worry that that might create a lightning network where everybody is public and doxxed, and they want it to be that let’s say, every man, the retail individual can afford to run his or her own lightning node on commodity hardware and do it in an anonymous way. So I guess that’s also one of the other considerations when you start to bring in things that look like like some form of reputation system.

Gleb Naumenko:

Yeah, definitely. That’s like, I think that’s a pretty cool anonymous reputation, like sort of implementation. I’m pretty sure hubs will be public and docs anyway like the big actors in the middle of the network with like hundreds of channels, but for end users for like Leafs of the network. I think that’s a good idea. I think we should keep exploring it.

Stephan Livera:

Yeah. And I’m curious then in that kind of, let’s say we have that kind of world where there are a bunch of big lightning hubs and they’ve like, they’ve got all the big channels and then you’ve got all these more, whatever you want to call it, sovereign individual lightning hubs out there. Do you think it would be like, maybe you could route through the sovereign individuals and maybe you get a little bit more privacy that way, but maybe you have to pay a little bit more. Do you think it would work that way? Or how do you think it might look?

Gleb Naumenko:

Yeah, well definitely. Well there is a little disadvantage to that generally. Well, I think that’s totally feasible. I think paying a bit more for security and that’s not like that’s not even just about privacy. There is like in my head, this idea you just explained comes up again and again, for example, because channels have different configurations like the safety for how long you can punish a counterparty, for example, like if you can punish only up to an hour, it’s not safe to be offline for more than an hour. So sometimes you want to be to have this configuration for a day that meaning that channels have different safety and security parameters. I totally see that more safer channels will have higher fees. There are little disadvantages to this way forward because if we have like very diverse policies. It will be easier to probe channels like channel probing is another research topic, like, which will be probably still not solved for a bit from now. When you just infer the balances. So it’s just a bit easier to infer the balances when channels have different, different properties.

Stephan Livera:

Yeah, I see. I think I’ve heard Antoine talk about this idea of trying to infer based on the CLTV Delta. So that’s check lock time verify, and that’s like one of the. I guess the parameters that sets how long you are going to have to wait. I guess the idea there is that people who are trying to surveil the lightning network might try to look for those differences in the CLTV and then try to figure out based on that to try and narrow it down and try to deanonymize participants on the lightning network.

Gleb Naumenko:

Yeah, that’s it definitely, but that’s like the only disadvantage of this different policies I see. Otherwise I see, that’s a pretty cool feature, so we’ll see where we get.

Stephan Livera:

Of course. Yeah. And so one other thing, so I understand and correct me if I’m getting this wrong, but as I understand Joost’s approach with Mission Control on this whole channel jamming attack, and then the mission control approach is to try to restrict the number of inflight HTLC’s that’s hash time locked contracts. So what’s your view on doing that kind of approach where you have your own, the node might have its own internal view of other parties on the network and then start saying, this guy is legit. I hear he’s, I’m okay to take an HTLC from here. How does that work for you or in your mind?

Gleb Naumenko:

I would admit I’m a bit behind of what you suggest. I didn’t have the time to read the latest in.

Stephan Livera:

Gotcha.

Gleb Naumenko:

Sounds like yes. Something along the same thing can we have with Antoine? So we probably should somehow merge ideas, at some point, or at least learn from each other.

Stephan Livera:

Yeah. Gotcha. Oh, well, Hey I might not have summarize that correctly though, but I think just from what I’ve seen and read and heard and things like that’s one example of kind of things people are talking about, but I guess ultimately what we’re getting to here. The risk here is that people can have their channels griefed and be stopped out for some time. And in some cases it doesn’t mean they necessarily lose money in the channel. They’re still get it back, but they just have to wait for that timeout to for that timelock to release.

Gleb Naumenko:

Well, you can, yeah. The attacker can paralyze the network and if there’s a kind of a general jamming or griefing.

Stephan Livera:

It’d be like at the overall level, and then maybe for you at an individual level, it just means you wouldn’t be able route payments at that time, which obviously would be a huge pain. But then I guess you would still get at least most of your money back if you had to close out the channel.

Gleb Naumenko:

Yeah, no as a routing node, you will lose routing fees as an honest user of the network, you will not be able to pay through it, but the problem is this attack is essentially free now. And attacker has just to lock some Bitcoins, but never spend them that’s the biggest problem.

Stephan Livera:

Yeah. I see I know Antoine is very focused on privacy and I think potentially you are also have you looked at any of these other ideas around things like there was a paper recently about cross layer deanonymization in terms of Bitcoin or lightning. And so the idea was if you combined like a chain analysis, chain surveillance approach alongside a lightning surveillance approach, and you were to look at channel ID in the lightning gossip data, and then try to figure out who holds what UTXOs and things like that. Is that something you’re also thinking about?

Gleb Naumenko:

Yeah, definitely. I’m just like, I’m noticing that there is enough people excited about UTXO, what do you call it? When you mark some UTXO, so illegal?

Stephan Livera:

Tainting, so to speak.

Gleb Naumenko:

Yeah. Tainting, I think there is enough research going in that direction and it’s pretty cool. It’s getting like merged with lightning, but I’m trying to focus on the actual on the peer-to-peer side. You look at the Bitcoin gossip, you look at the lightning gossip, for example, or you look at where they located some delays, some like you send a transaction and see if they propagate it or not. So I’m just, I’m just putting my attention more in the place where nobody else looking. But that’s also cool. What they’re doing, we definitely like at the end attackers will use all the methods they can afford them. They can find, so it’s definitely good to keep in mind. Alternative vectors. Yeah.

Stephan Livera:

Yeah. It seems like obviously lightning is still very early but it does seem to be growing. And so it’s one of those things where I guess maybe it hasn’t been worth the while maybe yet for any of the big players to really, really go hard on surveillance of it. Although I have seen some, I think there was a US government contract that went out for, I think it was chain analysis or one of the other surveillance firms on basically how to surveil the lightning network. So I guess these things are starting. So I guess these are things to think about also.

Gleb Naumenko:

Well there is a lot of I don’t even know, like, those companies are probably, well, they work with the American government, which is largely not qualified to judge. Of course there is like, what is it, FBI or something, which might, as we know from the, I think Snowden’s documents that they were interested in, like secret services were interested in Bitcoin, but I think all this chain analysis stuff is like they work directly with the state governments, which have no clue. So they know Bitcoin, but they don’t know like lightning. That’s why chain analysis is not probably even thinking about lightning yet at the same time. As I know, they were pretty like not qualified. So what they can do is they can go to some big exchange and ask them for a list of their users and wallets. So that’s what they can do and then try to link those UTXOs like a couple of hops away from the exchange, but like, I’m pretty sure that they have no idea how to do peer to peer layer stuff yet, at least that’s why they know from like two years ago when I talked to some of their people.

Stephan Livera:

I see. Yeah. So I guess the hypothetical sovereign, private individual who let’s say they bought coins, non KYC, they maybe they use coin joined to fund the lightning node. Maybe they use some combo. Maybe they do Tor only in private channels. I guess that kind of person who really wants to be private, I guess they can still have some reasonable level of privacy, but I suppose it might be a little bit harder for them to route if they’ve only got private channels and things like that. Right.

Gleb Naumenko:

Yes, that’s pretty much the case.

Stephan Livera:

Yeah, I see and also your website mentions a little bit around transaction relay jamming. Can you tell us a little bit about that aspect of it and how that works?

Gleb Naumenko:

Just a bit like I’m pretty excited. Like the whole, like DeFi thing, we might have different opinions on it. I’m pretty sure it would be cool if Bitcoin facilitated or was able to facilitate all this financial markets. Like for example, I have one Bitcoin, but I want to invest in, gold for a bit. So I find somebody who is who is willing to join a bet with me. Let’s say I’m betting on the gold price of $100 or one Bitcoin for like 100 grams of gold or something. They bet on like less than 100 grams and in a month we settle that super simple contract, would allow to facilitate and just draw a lot of attention from traditional financial markets here, because it’s going to be much cheaper than what they do.

Gleb Naumenko:

It would be noncustodial it would be pretty private. I think those use cases would make Bitcoin stronger. Because you know, this like latest, criticism is more of Taleb or whatever you call him. I think, well, I’m in his, he obviously like betrayed us, but I think it is fair at some like to some degree, and it would be cooler if if Bitcoin had this kind of exposure to more stability and maybe not through buying ice cream for Bitcoin, but perhaps through facilitating the financial markets. So the same stuff in Ethereum is very popular now, I think DLC would be able to facilitate some of those use cases, but in a much better way without like paying $200 in fees, because it can be on lightning. It can be almost free with the like good Oracle market where you’re don’t, like try some like chain link for providing data. But like, there’s a big actors with reputation, which also don’t see the deal so they cannot even make, they cannot influence much. I’m just seeing DLC is a really good way to bring all that stuff to be.

Stephan Livera:

Right. So you’re bullish on lightning DLCs then?

Gleb Naumenko:

Yeah pretty much. I wish I had more time on joining the actual spec building, but I can only do as much. Like 24 hours. Yeah.

Stephan Livera:

Of course only 24 hours in the day, so, okay. So I guess we’ve spoken a little bit about lightning and some of the cross layer aspects there. What about some of the other components of Bitcoin scaling? I mean, you were chatting a little bit earlier as well, about side chains and other ways of interacting with the Bitcoin blockchain. What are some of the things you’re looking at these days?

Gleb Naumenko:

So just yesterday in the Sydney what is it in a Bitcoin meet up telegram group AJ posted a way to scale lightning to billions of people by making lightning banks. I think we need a soft forks for that. Like we need, but they’re not very difficult. Like when it sig hash no inputs, and we need some full construction, either something similar to Coinpool we did, or Jeremy Rubins thing, what is it, OP CSV? So all right now lightning currently can facilitate, I think about 7 million users and months. That’s my estimate based on that if one person does one transaction on chain and months then like Bitcoin blocks are still limited. It’s I think I computed about 7 million. So the one, the way to break that scaling barrier is to see apart from increasing the block size of course, is to use joint UTXO ownership. When one UTXO and one transaction basically belongs to a hundreds of people. So basically his idea is to build banks on one UTXO. So one year is year. So it was a bank of 5,000 people or 50,000 people. That’s why you can scale. It might be beyond that’s a pretty promising approach. It’s very important for now to stay honest and fair in judgments and like, not bet not building a bank today and bet on a soft fork, because that’s a terrible conflict of interest.

Stephan Livera:

Yeah. And so this would require any prev out, right?

Gleb Naumenko:

Yes. Some alternative of, like those kind. So they’re not very difficult, soft forks. They’re not like crappy tailored to this particular use case. There’ll be the general, but, but yeah, we’ll need that.

Stephan Livera:

Gotcha. Oh yeah. I see. I’m just checking it now. I actually didn’t see this, I hadn’t caught this discussion. But yeah, I think that’s really interesting because it’s like this idea of how do you bring this to the masses because not literally every person can, you know, run a lightning node and do everything for themselves because we’re literally going to run out of chain space for them. So at some point you’re going to have to scale beyond that. And I’ve seen some approaches, like, for example, I’ve seen BTC pay server guys. I think it was Dennis Reimann who was working on this idea of I think he called it LN bank as well. And this idea was like, do you a BTCPay server that can have multiple users onboarded to it and use that as like a kind of a bank. And I guess even now blue wallet has the LND hub, which is like a thin wrapper for LND and then same kind of idea. You can have your one lightning node, but then onboard all these people onto that. But then I guess what we’re talking about here with this idea of using more advanced techniques is actually doing it in like a more, I guess, protocol based way, as opposed to pushing it up a layer into the software, the kind of applications that we use on lightning. Right.

Gleb Naumenko:

Well, it doesn’t matter really at which layer we do this. I just think this protocol way is more sovereign in the us and users still will be able to do whatever with their funds in the bank. I’m not sure, like I’m not familiar with those approaches, but all the software approaches are probably at least a bit custodial. So yeah. Yeah. So that’s the difference?

Stephan Livera:

Oh, they are. They are. Absolutely. Yeah. So, but it’s more, I guess the idea is it’s kind of like community custodial, but yeah, certainly I think this approach is more like a long term proper scaling up way. So I guess the challenge in these cases where let’s say, you know, let’s say this thing goes huge and someday down the line, you know, not enough people or basically multiple people would have to have a claim yeah. Like to a UTXO on chain and then people would have to sort of if they had to like split out or go to a different factory or some channel factory or channel grouping, I guess that is that’s kind of what this idea is getting at, right?

Gleb Naumenko:

Yeah. Yeah, definitely. So, yeah, I can’t even believe there is like at this point, so many ideas and we just need building them. I keep like, people keep around, keep asking me what’s the bottleneck in Bitcoin. And last year I just realized it’s developers. It’s the efforts we can put, like, there is enough funding. I’m pretty sure we can onboard like 10 more people and find funding for them. But there is just, no good people who are willing to do this. I don’t understand. Now I’m starting to really appreciate the chaincode efforts, what Brink will do the like that, that kind of stuff. Like it’s and I’m in, Blockstream started doing that even, even before me and Achow (Andrew Chow). Well, achow (Andrew Chow) was a contributor before bloodstream. I think just a bit. I was, I was absolutely not. That’s how I came into this space and yeah, that’s a big one.

Stephan Livera:

Yeah. I wonder how so I think like, as most things in the space, it’s all indexed to number go off, right? Like as the price runs up, then you see a lot more interest. You see more, developers, you see more funding, more mining, everything. Right. So I guess you know, maybe later this year, we’ll start to see a kind of a new crop of people who come in because they see the number go off and then they start thinking and they start researching and maybe they start developing,

Gleb Naumenko:

Well, it should work this way. I’m not sure it well, like I cannot guarantee this because it all depends on the, on those like sponsors or people who are willing to fund because right now it’s pretty like not structured that’s totally good, like, I’m always saying that Bitcoin has a good precedent of this like open source funding from the industry. But the scaling part is unclear yet. Like we’ll find out it, there might be some lag. Like Bitcoin went up five times. I did we see more funding or more developers? I think not yet. So we’ll see this year is like, yeah.

Stephan Livera:

Yeah. So maybe it’s on a bit of a lag then. Bitcoin runs whatever, some crazy number who knows. And then six months later is actually when like the development funding comes or something like that.

Gleb Naumenko:

Yeah we’ll find out.

Stephan Livera:

Yeah. So anything else you’re interested in or anything else you’re looking at?

Gleb Naumenko:

Well, we just like for the last month we were focusing on watching the label thing. There’s like a legal part when we were trying to prepare some like contracts, which will be like suit to the industry, clients as much as possible while like to maintain the best relationship trying to see what are our priorities should be this actually, we started as a way to what is it for selfgrowth? Because I was sitting with Antoine, he visited me here. Like I’m in Ukraine now. And this is one of the few free places in Europe where like, there is like, there is no lock down and all that. And so, yeah. So I was thinking how I should like grow further because yeah, I am a core developer and I’m like, I think I’m getting more productive every year, but also wanted to have some other direction. I was thinking of academia, but universities are so bad now. The most brilliant people in the universities have to spend half of their time on teaching some classes they’re not interested in because they are forced to, or like doing bureaucratic stuff. That’s like, yeah, it’s super underpaid and all that. And starting businesses

Stephan Livera:

There, you can work on what you actually enjoy. Yeah,

Gleb Naumenko:

Yeah. Yeah. I started in businesses is a bit early that’s our vision because we think we need to take time and like make more protocol strong enough and like held Bitcoin scale and all that. And if you start a business at this point, it will take all our time and we will not be able to focus on core. I’m like, well, I’m blessed unless we manage to raise a lot of funds and then hire other core developers. This consultant effort, was a way to self grow initially, like, like try this new thing use our knowledge. I’ve built like exchanges and wallets previously in Ukraine. Antoine like has some other background. I’m not sure he wants me to talk about. So this for me, at least this was like started as a self-growth idea.

Gleb Naumenko:

And then I realized that diversify and find it would be good because grants are cool, but I don’t know what if they disappear or what if number goes down. So when you have this like different source of income, which is like, based on like, the actual needs, not just good will and secondly. It seems like industry would use some help, like integrating lightning security, new protocols yeah, there’s a bunch of stuff. I’m pretty sure our expertise would be useful. And the idea is that we can like focus on that for, I don’t know, for a month like cumulatively or like a week a month and then, and then spend all the rest of the time on core development. So that’s what we were focusing on over the last couple of weeks.

Stephan Livera:

Cool. And speaking of core development, have are there any updates on erlay?

Gleb Naumenko:

Yes. people started looking at it very closely now, because last year we were revisited as a building, like some requirements, some like preconditions, right. Not sexy, not sexy, but like the, the, the work, which has to be done before doing it. We started looking at it. I just got a lot of help in how to shape it better. I’m finishing, shaping it better like today, tomorrow. And then I think they at work would be pretty active. We’re going to merge. So there’s this minisketch project, which is another requirement for erlay. I think that will be merged very soon. I think. Well I hate talking about time now because.

Stephan Livera:

yeah, because you never know.

Gleb Naumenko:

But yeah, I’m not, I haven’t given up, like for sure. I’m pretty bullish on this one too. It just, yeah. All of us, like, again, I’m saying developers like smart people that are probably the biggest bottleneck here now, because there are, there is like hundreds of real and people in the repo, but the amount of work has to be done is more than that.

Stephan Livera:

Yeah, for sure. Okay. So I guess just turning to Bitcoin more broadly, what are you excited about over this coming year? Is there anything in particular you want to see or anything that you are, kind of looking forward to?

Gleb Naumenko:

It’s pretty cool. It’s getting more mainstream. I’m afraid it’s growing too fast. Like earlier when like in 2018, I heard from like more experienced developers that you cannot, if it grows too fast when it was hitting 20. I didn’t understand that now. Now I do like again, if the industry cannot keep up with the finding and with all this stuff, the number go up, I think it might be scary. Like, for example, when we hit, I don’t know, 200 thousand, but the scaling is not solved. There will be like hundreds of dollars in fees per transaction. I mean, assuming the users like as of today if nobody integrates lightning or like it’s not it’s what a limited integration. I see a lot of work. So to keep up with number go up, because there is a clear demand, there is yes, we need to support the growth. We need to maintain the infrastructure. We need to keep scaling. We need to keep the security and, and face the I don’t know, closer attention of the governments to this thing. That’s what I see for the future. Yeah.

Stephan Livera:

Are there any areas that you, I guess, where are the kind of areas that you think most need help from a, let’s say security perspective?

Gleb Naumenko:

Well, I’m very happy to see the new multisig efforts because it’s still largely not usable. I think the Specter thing it’s pretty cool, do you know what I’m talking about?

Stephan Livera:

Yeah. Yeah. I’m a big fan of Specter. I’ve interviewed Stepan Snigirev and Ben Kaufman on the show, and I often she’ll specter. So I’m hopeful.

Gleb Naumenko:

Yeah. I think the, the biggest shame is not, not having a useful multisig. Well, hopefully that project is getting good. And then the what is it? Nunchuk? It’s something similar, right? So, that one, I’m just happy people building software for secure use of Bitcoin. I think on the core part we’re doing pretty well. Like I think the security part is actually was our priority for the last couple of years. So that should be fine. The software needs to keep up like the light clients that said need to keep up with, I don’t know how many users they have because it’s not experimental anymore. A lot of people use mobile lightning. And you can not just say in the repo that your software is experimental. Well, I mean, I know they’re open source developers and they have no choice, but yeah. There should be more attention to that stuff.

Stephan Livera:

Yeah. I see. It’s a professionalization of some of the software and things that everyone is using, I guess. Yeah.

Gleb Naumenko:

I’m not blaming the open source developers. But, but yeah, maybe that’s something industry should consider that fiveX number go up. It’s not like, it doesn’t come for free.

Stephan Livera:

Yeah, of course. And I think it’ll take maybe some listeners out there who are interested in funding development work, or maybe listeners out there who have maybe they’re working in a job that’s not Bitcoin related and then they can start working in a Bitcoin job. Maybe that’s part of the answer there.

Gleb Naumenko:

I will be very happy with this as the outcome of this podcast.

Stephan Livera:

Well, I don’t think it’s a one podcast thing. I think it’s more just like an overall focus and not just people listening to my show, but just the, the discussion and the conversation, like what people are saying on Twitter or the mailing list and whatever, everything IRC, et cetera.

Gleb Naumenko:

Yeah.

Stephan Livera:

All right. Well, cool. I think that’s probably a good spot to finish up here. Gleb, where can listeners find you online?

Gleb Naumenko:

So my Twitter username is @ffstls, or you just like search for my name and our website, thelab31.xyz. It’s like the lead language.

Stephan Livera:

Well, thanks very much for Glen for joining me.

Gleb Naumenko:

It’s always a pleasure.
