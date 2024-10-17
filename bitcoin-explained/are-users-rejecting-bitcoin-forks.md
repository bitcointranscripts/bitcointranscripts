---
title: User Rejected Soft Forks (URSFs)
transcript_by: Radiokot via review.btctranscripts.com
media: https://www.youtube.com/watch?v=Ua3W9p1Z_RA
tags:
  - soft-fork-activation
speakers:
  - Sjors Provoost
  - Aaron van Wirdum
date: 2022-05-07
episode: 57
aliases:
  - /bitcoin-magazine/bitcoin-explained/are-users-rejecting-bitcoin-forks
---
## Intro

Aaron: Live from Utrecht, this is **Bitcoin, Explained**. Hey Sjors.

Sjors: What's up?

Aaron: Sjors Provoost, Bitcoin Core contributor and author.

Sjors: Oh yes.

Aaron: Congratulations!

Sjors: Thank you.

Aaron: Your new book, [Bitcoin: A Work in Progress](https://www.btcwip.com/) is now available on Amazon?

Sjors: On everywhere. You go to [btcwip.com](https://www.btcwip.com/), which is Work in Progress. There's links to various Amazons and other sites where you can hopefully buy the book.

Aaron: What is the book?

Sjors: It is basically based on this podcast. So if you like this podcast, you will like the book. So what I did is I took a couple of the episodes and had a transcript made and then worked with an editor to turn the transcripts into chapters with a lot of back and forth. So some of them will look similar to the episodes and others will look completely different than the episode. So even if you've listened to every episode, I think you'll learn something new from the book.

Aaron: Great, and you'll also learn something new in this episode.

Sjors: That's right.

Aaron: We are gonna discuss **URSF**s which stands for **U**ser-**R**esisted **S**oft **F**ork or **U**ser-**R**ejected **S**oft **F**ork. I think it's sort of settling on user resisted soft fork but the acronym is the same anyways so URSF.

Sjors: Well a rejection is an outcome and resistance is an attempt, right? Well, I guess you can succeed in either.

Aaron: So, wait, which one do you prefer then?

Sjors: Well, I would say rejected, because then you say we actually rejected it.

Aaron: Yeah, I think that's a bit more accurate as well. All right, so before, let's just start with what a URSF is exactly, like what it technically is. Do you want me to explain or do you want to?

Sjors: No, you go ahead.

## What is URSF?

Aaron: All right. So basically, there's different ways of implementing it exactly. But as the name suggests, it is a way to reject or resist. I'm going to go with reject, I think. It's a way to reject a soft fork. And the way this can be done technically, you know, there's multiple ways to do it. But the way that makes most sense if you ask me in the way it hasn't been implemented at all yet. There's no client that does this. It's more of a concept. So a little bit of background; the first time I heard about it was Jorge Timón, one of the former Bitcoin Core contributors. He came up with this concept. That's the first time I heard about it, and this was during the Taproot discussion. Now, it wasn't implemented back then, but now we have a new discussion going on about [CTV, CHECKTEMPLATEVERIFY](https://github.com/bitcoin/bips/blob/master/bip-0119.mediawiki). In that context, there has now actually been some code produced by Jeremy Rubin, who's also the main proponent of CTV. So now the concept is getting a bit more real, and it's probably a good time to start talking about this. So, what it does essentially, a software can be activated, has been activated so far through blockchain signaling. We've talked about this in previous episodes. So for example, Taproot used Speedy Trial, which required that 90% of all blocks within one difficulty period had to had an activation signal in it, which is something that miners put in the block. Once 90% of all blocks have this, then it indicates that the software is going to be active. What a URSF does is it will actually reject the last block. Let's stick to the simple example. It will reject the last signaling block before activation. So I think it's a difficulty period has 2016 blocks, 90% of that is 1815 blocks. So a URSF client will accept up to 1814 blocks that signal, but the 1815th block will be rejected. So at that point it will basically create a blockchain split and on the side of the split that the URSF is accepting, there will not be a soft fork.

Sjors: Yeah, so I guess, I mean the specific details can probably be varied, but the idea is that when you're signaling for a soft fork, at least the way it's done in BIP 9 and in other proposals, you are expecting a signal and in the case of this you would actually require there to be not a signal. And so I guess that the easiest thing to compare this to is the **UASF**, the **U**ser-**A**ctivated **S**oft **F**ork, because a user-activated soft fork is where your node requires there to be a signal at a certain date. So then I guess there's three mechanisms that we can sort of look at.

Aaron: Yeah, it's like the mirror of a UASF. I think that's an accurate way to put it. If the UASF requires that a soft fork will be activated, the URSF will reject it if that happens.

Sjors: Yeah. And the key part here is that you're not actually rejecting the soft fork, you're rejecting the activation flagging of the soft fork. The specific thing that your node is looking for is not the software rules itself, but is the activation rules.

Aaron: Again, there's probably different implementation details, but this does seem or is, in my opinion, at least the most straightforward way of doing it. So we've covered what it technically is. Hopefully, our listeners will now understand what the concept is. And now, we'll try to explain why this does or does not make sense to actually have around. Right? Okay. So, let me see. I'll take the lead on this one and then you can comment. That's kind of the opposite of how we usually do it, I think, but let's see how it goes. All right. I want to emphasize something first. I'm going to use the word UASF a lot in this episode, and so will you probably. But when I use it, I guess you can make up your own mind. When I use it throughout this episode, I just mean a client that will enforce the soft fork rules for sure. So I don't necessarily mean an alt client, because that's sort of another debate, like do soft forks need to be activated through Bitcoin Core or through an alt client. That's not what I'm talking about.

Sjors: I think I understand what you mean.

Aaron: Let me finish real quick. A UASF in my definition can be implemented in Bitcoin Core.

Sjors: Yeah, I think there's nothing inherent about a UASF that can't be implemented in Bitcoin Core. It's just that the last two times that somebody proposed a UASF, it wasn't in Bitcoin Core. But the general idea of a UASF, at least these implementations so far, were that they required signaling. So where Bitcoin Core would use [BIP 9](https://github.com/bitcoin/bips/blob/master/bip-0009.mediawiki) which allows signaling and if the signaling happens then the soft fork happens, a UASF, whoever releases it, requires the signaling to take place which has the advantage of that then other nodes on the network that may not look at the UASF, they will see the signaling and know that the soft fork is going to activate.

Aaron: No, I disagree, or I think you're wrong. You can also do an UASF without signaling, but I'll get to that in a minute. For now, I just wanted to emphasize, because there is another debate, there is the debate that some people think that any soft fork should be released outside of Bitcoin Core, because otherwise Bitcoin Core developers have too much control or the perception of control. But that's not the argument I'm talking about at all. So I just wanted to emphasize that before I start to actually lay out the soft fork strategy.

Sjors: Okay. I just think that the scenario with signaling is the easiest to explain, right? You have with BIP 9 there's optional signaling, with UASF there's a mandatory signaling.

Aaron: Sure, sure, sure. This is the next step. I'll get to this right now.

Sjors: Okay.

Aaron: And then you can comment on it.

Sjors: Okay.

## Dealing with miners

Aaron: All right. So basically, ideally, we want miners to signal and to activate the soft fork that way. And that's how it has been done with previous soft forks, definitely before SegWit, that's how we did soft forks. And the reason for that is that if miners enforce the soft fork, then you are sure that the network stays in consensus because even non-upgraded nodes will follow the majority chain. The problem with this, and we've talked about this in previous episodes, I'm not gonna rehash all of it, but in short the problem with this is that it allows miners to block the upgrade. Miners can just refuse to signal and then the soft fork, the upgrade, doesn't happen. Okay, now there's three ways to deal with that situation.

Aaron: **Option one** is to accept that miners have a veto. You just agree that miners should be allowed to block a soft fork. That's one option. That's an opinion you can have. And there are people that have this opinion. Okay. That's optional. I don't like this option, but I think inherently the rules of Bitcoin are defined by the users when they accept money. I will define which rules I want my money to adhere to. And the miners are more like commodity producers. And if they don't produce the blocks that I want, then I'm just not going to value whatever coins they mine. I think users are fundamentally in control of the system, but you can be of the opinion, you can have a different opinion.

Sjors: You can have a more Zen interpretation instead of saying miners should be able to block soft fork, you could also say, well, it's true that miners can block a soft fork, even if you don't think that's a good thing. But anyway, option two.

Aaron: Right. So, **option two**, and this has not been done yet, but I think it makes more sense to explain it in this order. Option two, I think it was defined in [BIP 149](https://github.com/bitcoin/bips/blob/master/bip-0149.mediawiki). It has been discussed in context of SegWit years ago, and then during a Taproot discussion as well. BIP 149, I guess I'm just going to call it that, it's a flag day activation. So in the case of BIP 149 or a flag day activation, you don't actually use miner signaling. You just say, you just embed in the client, you say, on this block height or this date and time in the future, I prefer block heights, but whatever, it doesn't really matter for the purpose of the argument, your node is just going to enforce new soft fork rules. If a block is mined that breaks these rules, your node will just reject it. There's no signaling involved in this case.

Sjors: This is in fact how soft forks worked in the very beginning. When Satoshi was making soft forks, he would just put in an activation height, and it would just happen after a certain height.

Aaron: I guess you're right actually. Yeah, This is how the very first soft forks happened. Yeah, you're right. There was no signaling back then.

Sjors: Well, the very first intentional soft forks, maybe there were accidentals that didn't even have a height in it. But yeah.

Aaron: Right, right. Even if they even had a height, that you bring it up, were there ever flag day activations, actually? Or was it just a new code release?

Sjors: The block size decrease, for example, had an activation height in it.

Aaron: Oh, it did? Okay.

Sjors: But there may have been other changes that didn't.

Aaron: All right. So this is an option. Again, there are people that would prefer this. So if miners don't cooperate, you just implement a flag day. I have a problem with this because At that point, the blockchain...

Sjors: Maybe we should just say what option three is.

Aaron: No, no, this matters. There could be a split in the blockchain at some point because some users have upgraded and some have not.

Sjors: Yeah. And in fact, this has happened in the past, right? Where miners would not be running the same update, and then you get a split, and then it's up to the nodes, but not everybody upgrades their node.

Aaron: Right. And to add to that, this split can happen at any time. At any time a miner could break the rules, and then some nodes are going to enforce, and some of them are not. You can't know in advance when that's going to happen. It might happen on Christmas Eve, and no one is around to coordinate some solution, and now you have an even bigger problem. It's unpredictable, which I don't like. Now, there's another more subtle thing I don't like about it, which is soft forks, the nodes that are running stricter rules, they sort of have this asymmetric advantage, right? Because whoever is enforcing the soft fork, worst case scenario, they end up on a minority chain, while if you're not adhering to the strict rules, the loser rules, that chain can be re-orged away, right? So you've accepted money and now all of a sudden the soft fork chain is getting longer and now the money you accepted just disappears because your chain disappeared. So the only way to sort of be really sure that this doesn't happen to you is you need to be on the soft fork side, right? So in this case, with the flag day activation, you kind of really just need to follow along. And I think that gives a sort of subtle or maybe not so subtle implicit power to developers. Because if developers and specifically Bitcoin Core developers, in this case, if Bitcoin Core is the de facto reference implementation, then you better just do what they released, because otherwise you're running this re-org risk. So there's sort of a, you know, I think there's sort of a hidden power that could, you know...

Sjors: Or in the case of a UASF, well, I wouldn't, let's not use that term, but in case of this mechanism being used not even by Bitcoin Core, but by any group of people who, then maybe you would say, well, it's better to do whatever that group of people says, because otherwise I might get re-orged. But that gets back to the long debates about UASFs in general.

Aaron: But that's exactly where the URSF comes in, in a minute. We're getting there.

Sjors: Okay, so option one was you just accept the unpleasant fact that miners could not signal. Option two is you just start enforcing the new rules without any signaling. Option three...

Aaron: And **option three** – that's essentially what BIP 148 was in the SegWit context, which is mandatory signaling. So that's the UASFs that we've seen and that we remember and that we've done podcasts on. It's when your node mandates signaling at some point.

Sjors: And the advantage over that, over option two, is that now you know exactly when the conflict is going to happen, because you know what block should signal and not. So you're not waiting until the rules are actually violated, you're already having the fight in the signaling phase. And a secondary benefit is that because the signaling is mandatory, if the signaling therefore happens and everybody understands what's going on, whether or not they're running the mandatory signaling client.

Aaron: All right. So if I understand your arguments or what you just said correctly, the first thing you said is, if there is a split between nodes that are enforcing different things, then in the case of mandatory signaling, at least it happens at a predictable time as opposed to some unknown time in the future.

Sjors: Right. First, there's the discussion about whether the new rules shall apply, and that discussion is settled.

Aaron: Yeah. So, there's always a chain split risk, or at least in both of these cases, and it's arguably better to have it at a predictable time. I tend to agree with that.

Sjors: And also to have the split over something as simple as signaling rather than the actual rules, right?

Aaron: Why is that a benefit, do you think?

Sjors: Well, right now, I mean, I think there was somebody before Taproot activated who created a transaction that was invalid under the Taproot rules. And then you have discussions about whether or not that's a problem. We talked about that in the context of burying the soft forks. If you want to say, I don't like these new rules, then you would make a transaction that's invalid under the rules, but it's kind of difficult to do that. A signal is much easier to understand.

Aaron: Yeah. And then the other thing you said is if there are other nodes on the network that are just looking at the signaling but won't mandate it, then they can also be activated through this UASF. Some people would consider it a detriment. I don't really understand why personally, but I've seen that argument.

Sjors: Well, in any case, that's relevant in the case where a small minority or anyway, a minority releases such a UASF client. In the case where Bitcoin Core releases a UASF client, I would guess there is no other group. It's just everybody would be running that. There wouldn't be somebody running a regular BIP 9 optional signaling client.

Aaron: Right. Exactly.

## Chain splits

Aaron: Well, so far that I understand this concern at all, I think, and this actually gets to our next point. It's sort of the problem of UASFs or mandatory signaling type of UASFs. And that is that, again, there's this asymmetric advantage over enforcing it. And therefore, a small group of users may sort of impose their will on the majority.

Sjors: Yeah, exactly.

Aaron: Okay. This is where the URSF comes in. So if the problem is that a small minority can start enforcing the rules, they essentially incentivize miners to just go along with them because that way they won't split the chain and they presumably maximize profits. But you know that not everyone likes this small minority kind of controlling things idea. So a URSF as the mirror of a UASF gives other users a way out. So if they really don't like the rules that are being proposed in this UASF, and that will be mandated in this UASF, then the URSF gives everyone who wants out an option out. Now the problem of course is that this would split the chain. But I guess if there's one group of people, an intolerant minority, that definitely wants something, and there's another group of people that definitely don't want that, then the chain should split. I think that's what should happen. If people want different things – they want different things.

Sjors: And the nice thing about this situation where you have a UASF versus a URSF is that it's a clean split, right? It basically means that there's not gonna be a re-org ever because The UASF side wants to see signals and the URSF side does not want to see signals. So whatever happens in the future, whichever of these chains gets longer in the future, it doesn't matter because they will never accept each other because of that presence or absence of the signal.

Aaron: Yeah, well, there's one caveat there, right? So you are right. It is correct that the UASF clients will definitely follow the soft fork chain and the URSF clients will definitely follow the URSF chain, the soft fork rejecting chain. So even if one chain is longer for a while, but then another chain overtakes it, it doesn't matter for these clients. However, it does matter for non-upgraded clients. So let's say, for example, there is an alt client that does a UASF, and then there's an alt client that does a URSF and Bitcoin Core does neither and people keep running and using Bitcoin Core, then these people can actually suffer re-orgs.

Sjors: Yeah, this sounds like a plausible scenario because if there is such a big battle between people who absolutely want a soft fork and people who absolutely don't want it I would guess Bitcoin Core would do absolutely nothing and wait and see what happens. So in that case indeed the Bitcoin Core nodes would follow one side of the camp and then after a while, because one camp beats the other, it would follow the other side of the camp. And so those two battling camps would actually cause a lot of economic damage even outside of them.

Aaron: Yeah, potentially. So, I think...

Sjors: Assuming the market doesn't fix this and I guess that's where you come in.

Aaron: Yeah, well, I mean, I think given all the trade-offs so far, I still think that UASFs are the way to do soft forks. I don't want miner vetoes. I think that's just the way soft fork should be done. But then I also think that a URSF should basically be a standard option that is also given.

Sjors: So basically you're saying if you get rid of the BIP 9 system because miners have this veto power, then you would be okay with UASF as long as there's also the URSF. So you have to have both in order to have a balance.

Aaron: Right, yeah, obviously just my personal opinion that I'm giving on the podcast, this isn't some technical truth, but yeah, given all the options, I don't want miner vetoes. I don't like the flag day activation for the reasons I explained. And given all the trade-offs, my personal preference moving forward with these kinds of things is to do UASF, mandatory signaling, and then standard also give users a way out.

Sjors: Right. And this is where we probably don't really agree because I don't like the miner vetoes just as much as you don't like them, but I'm not willing to replace it with something that I think is unsafe. Which I think, well the UASF without anything else I definitely think is unsafe as I've explained in other episodes and I think this combination is still unsafe, despite it having some cool features. So I'd rather deal with the current annoying situation than to open the other can of worms. But we can explore what that can of worms looks like.

## Mitigating re-org risk through futures market

Aaron: Well, I was just sort of prefacing this. I was saying, okay, given the trade-offs and my knowledge of how the system works and the risk and my personal preference, is that any soft fork should be a UASF in Core or maybe somewhere else. That's not part of this podcast discussion. I think it should be UASF with mandatory signaling and standard users should also be given the option to opt out through a URSF. So that opinion sort of stands on itself. Now to mitigate the risk, and this was what you're getting at. So to mitigate the re-org risk and that kind of stuff, I think it would be much better if this sort of battle happens without any casualties. And I think that this can be accomplished fairly well through futures markets. So instead of actually splitting the chain and only then allowing trade between the coins and now all of a sudden one coin is more valuable than another while the market is sort of figuring this out live and it's been traded live and there are replay attacks and who knows what else and then what re-orgs and, you know, the Bitcoin Core user in the middle suffers, and so instead of doing that live I think it can be done sort of virtually through futures markets.

Sjors: So basically you have an exchange that sells two sites that basically says, here's, you know, you deposit a Bitcoin now and it'll tell you you'll get either...

Aaron: You'll get both at first.

Sjors: You'll get both back after the split. And then it's up to the market to decide which half of that is worth more. This has been done by Bitfinex in the past.

Aaron: Exactly. So you get both back after split, you get coins on both sides of splits, but before the split, you can trade between them. And if you trade between them, if I sell all my UASF coins for URSF coins, then I get two URSF coins and zero UASF coins after split. So this way the market can figure out which option they think is more valuable, which version of Bitcoin the market really wants. Do they want the soft fork version or do they want the version that rejected the soft fork. And by allowing the market to figure this out before there's actually chain split chaos, miners can see: all right, users clearly want the soft fork, so we're just going to mine the software because we want to make as much money as possible.

Sjors: So miners will have to pick a side based on the market estimate. And get some data from the market.

Aaron: Exactly. So I think if the futures markets work as I expect them to, then there won't actually be any re-org chaos afterwards. If you're still worried about that, you can still use the client you want, but this is sort of a way to mitigate that extra risk that otherwise sort of neutral users that aren't aware of what's going on might suffer. So you use futures markets for that and then the miners can react to that.

Sjors: So as much as I think futures markets are super cool, I don't like the idea and I guess I have roughly three reasons for that. But I don't know if you wanted to finish something.

Aaron: No, no, no, go ahead. I think that's sort of my case.

Sjors: So one is this adds a whole bunch of complexity compared to what we have now and I don't want to say Proof-of-Stake complexity but you know some complexity at least because now it depends on how much market power you have and what happens to the protocol. So the second is that personally I don't believe in, I don't believe in the strong efficient market theory. So the idea of an efficient market theory is that the markets, the collective knowledge in the market will know, well collectively will be able to make a good prediction of what's actually going to happen taking everything into account. But my impression is that, you know, the market very often does not take things into account, especially black swan events. But I also think if they just don't understand the subject matter, the market can be very, very wrong. But even if it was, the question is whether the implementation of the market would be correct. And if you're dealing with a very short-term soft fork activation, though of course you could make the term longer.

Aaron: I definitely think it should be at least a year.

Sjors: Yeah, and probably more because if you look at, you know, somebody just sets up a quick futures market like Bitfinex did, there's going to be discussions about whether the market is fair. There's going to be a lot of discussions about market manipulation. So that's kind of where I come up with my earlier argument. If the future market is not super well structured, it could be manipulated by people with a lot of money to push the result one way or the other.

Aaron: Well, I think with UASF versus URSF, it's pretty clear, right? You get paid on that client, whatever chain that client is.

Sjors: Yeah, but there's all sorts of shenanigans that the exchanges that are trading these tokens can do, right? They can manipulate the order book. There can be people pushing money around. I mean, every problem you have on an unregulated exchange or commodities market you're gonna have here. So eventually you can iron all that out because the species has hundreds of years of experience with how to set up a stock market and how to set up a securities market or a commodities market. But then maybe we'd need like 10 years of SEC enforcement and whatever to really get a proper futures market that is really reliable. But maybe that's acceptable, right? Maybe we say, okay, we don't do another soft fork for the next 10-20 years while we figure out this futures market thing and make sure it's completely fair. That could be. And maybe that actually ends up happening over the long run anyway. What was my third one? No, I think this is my third one. So my first argument was, I think this ads complexity, including, you know, giving power to rich people. The second, I don't believe in efficient markets in general.

Aaron: Okay, so let me me respond to that live now.

Sjors: Oh, okay. I just wanted to recap it.

Aaron: We are recapping it. So your first argument is it gives power to rich people. So I don't think that argument is very compelling because there's nothing really new about futures markets. Like right now, you know, the Winklevoss twins and Michael Saylor and whoever could release an alt client and then start selling their Bitcoin and buying these alt coin or new Bitcoin version of it. The only thing the future market does is sort of make that virtual instead of having to do it live. There's no actual difference other than that. I don't see any other difference. So there's nothing new going on here. It's not some sort of Proof-of-Stake kind of system where the rich get to vote. No, it's actual trading. Like people actually trade in the same way that people already trade between Bitcoin and altcoins. And like, Michael Saylor can decide to sell all his Bitcoin tomorrow and buy whatever shitcoin he wants. That's trading. So there's nothing new there, in my view. And then your second point?

Sjors: Well, my second point was that I don't believe in general in the efficient market hypothesis, at least a strong one. So that's difficult to debate here, I guess.

Aaron: Yeah, that's difficult to debate. I just have a strong... I think it's just the best we have, basically, and maybe you don't.

Sjors: Well, I'm not saying it's not the best we have, I'm just saying it's not good enough.

Aaron: But if it's the best we have, we should do it, right?

Sjors: No, because we could just either stick to what we're doing with BIP 9 and just accept that it may be very difficult to get some soft forks through if miners really don't like it.

Aaron: Right. Yeah. Remember that. Again, my point about futures market isn't an argument in favor of why I think there should be UASF and URSF. I think that should be the case anyways. I just think a futures market is a way to make it safer. And then your third point?

Sjors: My third point is that even if in theory futures market could work, in practice it's going to be very difficult to get it to work because of all the shenanigans that can happen on markets.

Aaron: I mean, that I probably agree with. Like in an ideal scenario, we all work towards a future where we can do these kinds of things trustless on Bitcoin with smart contracts, or I don't know what that would look like, but that would be ideal.

Sjors: Maybe. I'm super skeptical about that because I think Bitcoin solves one specific problem and I don't think blockchain technology quote-unquote is useful for something like a stock market. I think some things are fine in centralized systems.

Aaron: Yeah, I'm not going to think out loud of ways you could do this. But it seems plausible to me that you could somehow lock Bitcoins up in a certain way and then only be able to unlock them anyways. Yeah, so that was sort of my point on futures markets, which I'll say it for the third time, that's not even an argument in favor of URSFs. I think URSFs should exist either way and UASFs as well. I just think futures markets would make it the safest way to do it.

Sjors: Yeah, exactly. But I think without the futures market, it would be super unsafe. And with the futures market, it would be unsafe. Or something like that.

Aaron: Yeah, I mean, you like miner vetoes. I can tell.

Sjors: Yeah, I love miner vetoes. So maybe it is useful to talk about this concept of rough consensus, or even what is supposed to happen under good circumstances with protocol upgrades.

Aaron: Yes, that's true.

Sjors: Because it's probably a good reminder that there was another way to do it, which has worked a few times. So the idea of rough consensus is defined in some internet engineering task force standard, which is a very hippie document. It talks about humming and rough consensus, and it's definitely written by people in San Francisco. But the idea there is that when you make a new technical proposal, when you make a proposal for a change, you're supposed to, well, first of all you should spec it out in a way that people can read it. You should write some working code that actually does the thing that you're saying, so you don't have all these pie-in-the-sky perpetual motion machines. And then other people should be paying attention to it, should be reviewing it, and if they have, if they don't have any objections, then you can go forward with it. If they do have objections, and those objections are of a technical nature, not of a political, like, "I don't like the color green" kind of nature, then you should address those technical objections. You should explain either why the objection is wrong or you should find a solution for that. And if you follow that process, it does kind of mean that proposals move forward by definition. Because there's not really a way to stop these things from happening there. So things may get stranded because there may be objections and you can't fix them. So then the proposal stops and there may not be anybody willing to review your proposal because people just don't care about it, in which case it stops. But if enough people review it and they don't find problems with it, well then I guess within the current mechanism you would then propose something like a BIP 9 upgrade where miners can signal for it and if they do signal for it, it just happens. But notice that there's no mechanism that could politically say...

Aaron: It could still also be UASF, right? UASF could make it through this process?

Sjors: Yes, but what I'm saying is more like there's no obvious way how something will be stopped other than to have an articulated technical reason why it should be stopped. And so what is missing, you could say, maybe that's not good, because we have seen that miners can sort of randomly veto something if they don't like it, even if they have no reason for it, but there's no way for users to veto something. And so that could be another perspective of why something like a URSF could be interesting, even if I'm skeptical about this proposal. But the idea could be there could be soft forks that there's no technical objection to, yet for some interesting political reason, we just don't want it.

Aaron: Well, the other reason could of course be, you know, like this is a good process or these are good principles, but developers could still get lost in their own biases. They're still humans. They could become corrupted.

Sjors: That could be one scenario where developers indeed just go off on a tangent. They come up with some soft fork that nobody has a good technical objection to, but actually nobody wants it either. Because something went wrong with the developers. And then, yeah, the question is what do you do about that? One thing could be simply that nobody downloads it out of apathy, maybe. But then because developers keep releasing new versions that also fix bugs, you could get into a situation where you kind of have to. So, and then there's not an obvious way to resist that. So, I'm not saying that the problem is unsolved.

Aaron: These are obviously good principles or at least they sound like obviously good principles. I think I've personally become a bit less worried about, You know, the concrete example would be an alt client that releases in UASF outside of this process. I've personally become a little less worried about that. And the reason for that is what I just discussed is the futures markets. If someone thinks the process doesn't work, well, let them test it against the market. If they're right, the market will just reject it and there will never be a split and no miners will mine it. Or maybe they're right and they help Bitcoin forward and move past a broken process. But either way, I've become noticeably less worried about all the clients because I think, right, hope. But I think futures markets will sort of solve that problem.

Sjors: Yeah. But again, we talked about that. That hinges on how much you trust future markets as well as their specific implementations.

Aaron: Or just market efficiency, yeah.

Sjors: Maybe I can bring up one more point, which we did talk about before. So far we've talked about rejecting a software based on signaling. We also talked about flag day, but in this URSF concept, the idea is that you reject a signal for a soft fork. But there are soft forks that don't have a signal. And flag days are one obvious example of that, where there's simply nothing to reject, because the new rules apply at this date and there's nothing you can stop basically. And another very pernicious example of a soft fork that you can't stop this way would be like a mandatory KYC miner whitelisting kind of thing where miners only mine blocks that are compliant in some bizarre way, and there's nothing on the blockchain that shows that they are. So there's nothing you can do then other than that you would say: well we mandate that certain transactions be in there, but that's a really weird rule to have as a user. So in general, I would say we don't really have a good way to reject soft forks. Maybe this could be a way to reject signaled soft forks?

Aaron: Well, so I think what you're describing now is a 51% attack. And I guess sort of what we're discussing or the way I see it is engineering principles, like how should we do things. And yeah, sure, the system can still be attacked in other ways, but what should we strive for? What should we do if we want to upgrade the protocol?

Sjors: It's true. I guess the difference between a 51% attack and a soft fork in the example we talked about with KYC stuff is that as soon as the attack stops, basically, the system reverts back to normal where all transactions are accepted because nodes are not rejecting those transactions, only miners are. Whereas the soft fork, the idea would be that it's permanent. So after whether or not miners signal, at some point those rules have been enforced for a while and we can assume that they'll always be enforced. They're not going to be reverted.

Aaron: Yeah, I mean if we wanted to, but I'm not sure if we want to. Essentially this sort of gets to a philosophical discussion of what is even Bitcoin, like what are the Bitcoin rules, what is a full node, and in that sense, this is sort of how I would define it, I guess.

Sjors: You do not want to be the first person to run a hard fork that stops enforcing SegWit, basically. So that's sort of a mechanism that keeps enforcing the rules that are activated in a soft fork. But those rules would actually have to be in the code and they're in the code that miners run, they're in the code that exchanges run, they're in the code that users run. And if you want to be the first one to relax those rules, it's usually not a good place, so you'd really have to organize that.

Aaron: Yeah, well, what I was going to say is I would maybe even argue or make the case that the way I would define the protocol upgrade is there needs to be something on the blockchain that signals that and that can be recognized as such so people can either upgrade to the new rules or reject it. At this point, the discussion is getting philosophical.

Sjors: Yeah, I mean, we've had soft forks without signaling, but I agree that signaling is a good way to do it. Okay, I think we've probably covered this concept and the episode may be a little bit confusing, but at the same time, hopefully interesting.

Aaron: They usually are, I think, Sjors.

Sjors: Well, sometimes we have a very clear concept that we're going to explain, and it's a little bit less philosophical.

Aaron: This was a bit different than usual, yeah.

Sjors: Anyhow, that all?

Aaron: I think that was it.

Sjors: All right, then. Thank you for listening to Bitcoin, Explained.
