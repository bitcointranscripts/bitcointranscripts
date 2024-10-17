---
title: Multiple-path Payments (MPP)
transcript_by: Jeff Czyz, Stéphan Vuylsteke
tags:
  - multipath-payments
speakers:
  - Alex Bosworth
date: 2019-06-25
media: https://youtu.be/Og4TGERPZMY
aliases:
  - /chaincode-labs/chaincode-residency/2019-06-25-alex-bosworth-mpp/
---
Location: Chaincode Residency 2019

## Bigger, Faster, Cheaper - Multiplexing Payments

Alex: How to do multiple path payments. So there's a question: why do we even need multiple path payments? So you have a channel -- like -- we don't have them now, so are we really hurting for them? So I kind of like describing different situations where you would need it. So in the first quadrant you can see I have two channels. One of my channels has three coins on my side. I want to buy something that costs two coins. So that's actually a situation where we're fine today. That's normally you know what's happening. We want people to make channels that are big, that are going to be able to accommodate multiple repeated purchases. That's kind of like the whole idea of channels. So that's why at the moment we actually don't have a huge problem as far as needing multiplexing different channels together.

In the second quadrant you can actually see that if you have two channels where you don't have insufficient balance but you actually have inbound capacity on one of the channels, it's actually still possible, even without multiplexing payments to pay for that three coin item. And the way that that would work is you can actually move funds from channel A to channel B, and then in the second quadrant you can see I have four coins total but they're split up incorrectly. So just naively I won't be able to buy this three coin item. But in my second channel I have one coin that's inbound balanced. So I can receive one coin. So what I can do if I really wanted to buy this three coin item is I could take channel one, and I could pay back to myself on channel 2, and then channel 2 would have three and then that channel would now have sufficient balance to actually buy that three coin item. So that's a way to do larger payments without even having multiplexing.

So today we have these two cases where you could if you need to buy something and it costs a bunch, that these are possible ways to do it. So the third case is where we run into trouble. You have two channels and both of them have insufficient coins for what you want to buy, and so you're kinda out of luck. That's where multiplexing multi-path payments comes in as a solution.

## The Wallets Have Eyes - Privacy Implications of Multiple Paths

So there's another thing to consider with multi-path. It's not just about “can I pay” or “can I not pay”? It's also “can somebody observe that I'm paying?”. If you can look on this in the upper half I kind of show an example of somebody who's buying a Y'all's article. And so if that person A is sending 150 satoshis across the network, then person C kind of see as they pass that 150 satoshis across to yalls.org it can kind of have an idea that that payment is going to y'alls.org because it's 150 and that's like the standard cost of an article on Y'all's, so it's a pretty good idea that that's what you're doing.

So one advantage of multi-path payments in the future could be that we could split up these values to make it less obvious, so we could say instead of spending a 150, A is going to spend, you know, some random amount through C and some other random amount through B, and together they're gonna add up to 150 on the other side but it makes it harder for C to tell that that payment is actually going to Y'alls.org. So that's another reason why you would want to use multi-path and a limitation of the current protocol that doesn't really have multi-path.

## Link Level AMP - Smarter Edges

So there's multiple ways to do multi-path, and one way that I'm not talking about is what we propose at Lighting Labs called “atomic multi-path payments” which uses sharded preimages, and that idea is that you would split up the preimage into multiple different components, and then the only way to put it back together is if the payment has completed atomically, so I get all of the payments together. But it's kind of complicated to implement. So we have different ideas of how we can do multi-path payments before we get to that complicated state. And one of the easiest ways to do multi-path payments is this idea called link level of multi-path payments. And I can kind of show how that works. It's very simple. So in this diagram you can see that the route begins on the left and then it goes through the router and then it gets to the end. And this is representing -- so -- at the start I have two channels and both of them have one coin. And I go to the router and my goal is -- with the router -- is that they're gonna relay my payment of both of these different one coins into a two coin payment. So if you think about how HTLCs work, it's kind of like a two-phase commit system. So I get in HTLC and then that becomes part of my commitment transaction, and then I pass forward that commitment to the next node and so on and so forth. And then only after everything is already kind of locked into the commitment transactions do we then begin the second phase of the commit which is to reveal the preimage and then roll it back.

So what we have today is: we have a situation where -- in LND -- we have people who have a bunch of channels -- like I have multiple channels to the same peer. So what I could do is I could actually talk to my peer and I could say, listen, I want you to forward these two coins, but I don't have a single channel that has enough for these two coins. I only have a one-coin channel and another one-coin channel. So what I'm going to do is I'm going to put one HTLC on you and I'm going to ask you to forward a two HTLC. So I'm gonna put one coin on you and then I'm gonna say, “oh can you send a two coin” and that peer is gonna say, “Well I'm not gonna do that because I'm gonna get one and then I'm gonna spend two, that's not gonna make sense.” So but then I can say, “oh well actually I have another channel which has another coin, so before you forward that on, I'm gonna attach another one coin to you”. So you're gonna have two incoming HTLCs and they’re gonna be locked to the same preimage, and when you have this commitment transaction you're going to know that oh I have these two incoming HTLCs and they both are locked to the same preimage. So that's going to make it now make sense to me that I'm gonna be able to pass out an HTLC on the other side that spends two, because I'm gonna be able to – once I send this out and I get the preimage to get two then I'm gonna be able to collect these two separate payments on both these different channels.

So you can kind of arrange this without even telling anybody on the network around about it, but you do need to have some kind of protocol so that both of the different peers understand how to talk about this.

Rene (Pickhardt): Do I have to have two channels with the route, or would this technically work in the sense of I have one channel with the route and then the other one is just another route to the route. So I would tell the route, “hey, you accept this HTLC and there's another one incoming,” on some way?

Alex: Yeah I think it should be fine but you want to be a little bit careful, One thing to think about with this type of strategy is you're kind of breaking the rule of never use the same preimage twice. In the two-phase commitment scheme you have to be careful that you're in the first phase where you're just kind of waiting to reveal the preimage. But otherwise it could potentially work but it just might be a little bit more complicated. So the big advantage of link-level AMP is you are really only caring about these two different peers and they can have their own protocol that nobody else in the network really needs to care about.

Okay, so this is the smarter edges, and it only extends one peer, so that’s the benefit of it and it's also the limitation. And you know, Rene has a good point that potentially it could be extended more, and oh I'll kind of get into that now with base amp.

## Base AMP - Economic Code

So base amp is using the same principle, but it's making it a little bit more general. So in this example you can see I'm trying to buy something that costs two, and the seller is selling this thing that cost two. He has two inbound channels, and both of them have one coin only. So normally he wouldn't be able to receive the two coins because he only has these one coin channels. But if we can arrange things so that you'll wait, I can actually still pay him too. And the way that that will work is that I'll first pay him one over the top channel. So I can do that because I have two coins in my channel and then the routing node has a one coin channel. So I'll first pay him, but he won't accept that HTLC because the item cost two coins, so you know that's not enough to actually give over the item. So then what I'll do is I'll pay another payment and it'll be locked to the same preimage, and it's safe to do it because the preimage hasn't been revealed yet, and we're still in this first phase of the two-phase commit where we're just setting up our commitment transactions. So he'll get the second payment and he'll then do the math, he’ll be like oh well I can add up, I have a 1 coin incoming HTLC and have another 1 coin incoming HTLC, and now it's safe for me to reveal the preimage because I'm gonna get the payment that I want, and everybody's already locked into their positions. So it's not like you can mess around and then use that preimage to steal money from somebody. So it will then rewind back to the beginning of – in the same way that payments normally go, and you will have successfully bought something for two, even though there's no channel that exists that has two by itself.

Question: How would you prevent the merchant from not revealing the preimage before the second HTLC is constructed? You pay me one, but not enough, so tough luck, or I don’t know?

Alex: Yeah that's kind of a problem, so you need to make sure that this protocol is followed and the – I call like economic code, so it's based on economic logics. Why would I accept a one coin for something that I'm selling for two coins, especially if we pre-negotiated this. If I told you, oh, I'm not gonna be able to pay you all in one HTLC, you’re gonna have to wait for multiple HTLCs to come in, then why would you take that one coin? But technically you could, so that's why something like atomic multi-path payments that uses like a sharded preimage might be preferable in some situations.

Christian (Decker): In combination with an invoice you're actually providing for a proof of payment for a partial payment, so I would have an invoice and I would have the payment preimage, I could then go and and say okay, I paid right, now give me my coffee, but the merchants only received like half of the payment, and is now forced to to act on that partial payment. So it's an economic argument.

Alex: Yeah yeah, but the advantage of this scheme as well is that it doesn't really require any network changes, as far as the nodes see that you can take different paths through, and the economic logic works at every step. So even if you don't want to commit to two HTLCs at the same preimage, you don't have to. So this is something that we could even see as being useful, like submarine swaps. So that's something that we're thinking about how we would actually put this into use if you wanted to swap multiple channels. So I want to do a submarine swap or I want to reduce the on-chain footprint of my swap. So what I can do is, I can empty out lots and lots of channels, and then I can turn those all back into one on-chain transaction. So in that case we also don't have to really worry too much about this – the economic argument is a lot stronger in that case. Because it's like, why would I ever accept less than what the thing cost? So I think there's a lot of different applications, and this is more like a near term solution that we could deploy to the network without having to wait for Schnorr soft forks or anything like that.

Okay, I guess I can move on to key sending, that's all that I had on multi-path. Maybe there's some questions about multi-path though? Cool, covered everything. Oh Rene?

Rene: I mean, I talk about multi-path payments a little bit too tomorrow, so I mean there are some criticisms with multi-path payments, so the questions (Audience: no there aren’t) should – I mean we could discuss them now but I have them on my slides tomorrow, so.

Alex: I mean, I’m interested, maybe I don’t have an answer to that. What are some criticisms?

Rene: So for example with multi-path payments you would lock up more HTLCs statistically, so overall you put more data on the blockchain.

Christian: Well but you – it's limited to 20 X multiplier of your own funds, so the maximum route length that you can lock up for HTLCs is 20 times your funds that you are spending yourself, and that doesn't change whether you split them all out.

Rene: But if it's over more paths, it's different onions that you send out.

Christian: You mean your on-chain footprint changes?

Rene: So the thing is, first of all there's more HTLCs locked up in the entire network, and if channels break then also more HTLCs will hit the chain (Christian: right, yeah) right. So this entire thing where we try to make the lightning network reduce load from the chain, we now put more load on the chain, you know?

Alex: Yeah, I mean I think a lot of these subjects we’re talking about they all interlink with each other. By reducing the size of the HTLCs I'm reducing the economic incentive to pass it forward right, because maybe, I'm creating some risk that it would go to chain, and now it's like, if it does fail and go to chain it could go to chain in a lot of different places instead of just one place. But there's also a question of complexity, how do I figure out the route for this? So, instead of just figuring out one route now I'm figuring out lots of different routes. It's a problem with the <inaudible> of multi-path payments where to like go to flow routing

Christian: So, the one thing that we're looking into is basically having an adaptive multi-path payment. So we try the first attempt and then if that doesn't work due to capacity constraints, we split that and try two different ones. Generally speaking we are discouraging people from using too many HTLCs, because we still have a base fee that is not proportional to the amount, and so you're actually paying for the HTLCs you consume. But I mean there is the impact on on-chain footprint that might be negative.

Rene: Yeah but this also goes in the direction that – AMP routing is not so fast as regular lightning payments, right? Because whatever <inaudible> (Christian: but it works where the others don't) Yeah but if one route times out – I mean, we just covered this yesterday that we have to wait (Christian: oh, okay) yeah, so now I'm splitting over 100 paths – one path is timing out, all the others are locking the HTLCs for this amount of time, the entire payment is the maximum time of like…

Alex: Yeah, yeah, I’d definitely say this is more of like an optimization that you wouldn't necessarily need all the time, and really the key usefulness is if you run out of the liquidity in your channels – and hopefully you're not doing that all the time right? You want to be making your channels of a sufficient size that they can support many many many many repeated payments and you're not running into this thing where you need to combine a bunch of different channels together in order to pay that one thing. In that case, you might just want to go to the chain.

Christian: So the one key advantage that I usually mention is that it's a huge increase in user-friendliness, because you don't have to think about how do I look at my channels, I can actually bundle all of my channels. So I can actually go back and have a single off-chain balance and not care about how these are actually mapped to individual channels, because the total amount that I have is always available independently of how I split it up

Alex: Yeah, there's definitely UI considerations, but even then – I think we're still figuring out how to represent lightning channels to users. In Lightning Labs app we actually already show you the unified balance. And we've been working on how to like messages but also, you kind of should think about not spending your entire balance all in one go with lightning. You should kind of have that consideration that this is a spending wallet that you use multiple times, right. You shouldn't really have this idea that like, I have this one balance and I’m going to spend it all just in one shot because maybe the receiver couldn't…

Christian: No I totally agree that you should be showing channels by default to users but I disagree about me not being able to spend the hundred bucks I have on my wallet when I want to spend one hundred bucks.

Alex: I mean, it’s definitely good…

Christian: I want to educate users less, not more, about what is good and what is not good. And so the abstraction that I'm able to bundle channels such that I can perform bigger payments is a net win for me, and we shouldn't reintroduce this technical detail from underlying layers back into the user behaviour.

Alex: Yeah, I don't know exactly what the right abstractions are. I think as we develop and then release it to users and see what they get confused by, we'll figure out more about what you have to know about, and what we can decide.
