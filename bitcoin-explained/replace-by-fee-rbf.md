---
title: Replace By Fee (RBF)
transcript_by: varmur via review.btctranscripts.com
media: https://www.youtube.com/watch?v=E9L1CRP3W8k
tags:
  - rbf
speakers:
  - Aaron van Wirdum
  - Sjors Provoost
date: 2021-02-05
episode: 26
summary: 'In this episode of The Van Wirdum Sjorsnado, hosts Aaron van Wirdum and Sjors Provoost discuss Replace By Fee (RBF). Aaron and Sjors explain three advantages of RBF: the option the “speed up” a transaction (1), which can in turn result in a more effective fee market for block space (2), as well as the potential to make more efficient use of block space by updating transactions to include more recipients (3). The main disadvantage of RBF is that it makes it slightly easier to double spend unconfirmed transactions, which was also at the root of last week’s “double spend” controversy that dominated headlines. Aaron and Sjors discuss some solutions to diminish this risk, including “opt-in RBF” which is currently implemented in Bitcoin Core. Finally, Sjors explains in detail how opt-in RBF works in Bitcoin Core, and which conditions must be met before a transaction is considered replaceable. He also notes some complications with this version of RBF, for example in the context of the Lightning Network.'
---
## Introduction

Aaron van Wirdum: 00:01:33

Live from Utrecht, this is the The Van Wirdum Sjorsnado.
Sjors, I heard Bitcoin is broken.

Sjors Provoost: 00:01:40

It is.
Yeah, it was absolutely terrible.

Aaron van Wirdum: 00:01:43

A double spend happened.

Sjors Provoost: 00:01:44

Yep, ruined.

Aaron van Wirdum: 00:01:45

And this is because - "a fatal flaw in the Bitcoin protocol."
That's how it was reported, I think, in Bloomberg?

Sjors Provoost: 00:01:54

Yeah, I couldn't find the original report by Bloomberg.
I think Cointelegraph reported it more or less in that way, and then Bloomberg referred to it.

Aaron van Wirdum: 00:02:01

Oh yeah, I think that's what happened.

Sjors Provoost: 00:02:03

But at least more recent articles I saw from Bloomberg were saying, oh, noobs thought it was broken and they were all googling double spends.

Aaron van Wirdum: 00:02:10

Oh, they corrected it?

Sjors Provoost: 00:02:11

I wouldn't say corrected it.
They were more like, you know, going meta on it.

Aaron van Wirdum: 00:02:16

On their own mistake?

Sjors Provoost: 00:02:18

So I don't know if it was their own mistake because I've only seen the haters basically saying that they made that mistake.

Aaron van Wirdum: 00:02:25

Fair enough.
Okay so to be clear Bitcoin is not actually broken.

Sjors Provoost: 00:02:30

Nope it's working as expected.

Aaron van Wirdum: 00:02:33

It's working exactly as expected.
Now we could get into a discussion on whether or not a double spend happens or not, and that gets into the definition of double spend but we're not going to do that Sjors, instead we're going to explain what was sort of this alleged fatal flaw in the protocol, which was Replace By Fee, RBF.

Sjors Provoost: 00:02:53

Yes.

Aaron van Wirdum: 00:02:53 

That was sort of why this alleged double spend could have happened?

Sjors Provoost: 00:02:58

Yeah, it could have happened even without that, but...

Aaron van Wirdum: 00:03:00

Oh, sure, yeah.
And I guess that's the sort of stuff we're going to discuss in this great podcast today.

Sjors Provoost: 00:03:05

Exactly, so stay with us and you'll learn more.

## RBF Overview

Aaron van Wirdum: 00:03:08

Okay, first of all, Sjors, this thing is called Replace By Fee.
Just in brief terms, what does it mean?
What is Replace By Fee?

Sjors Provoost: 00:03:15

So it means you have a transaction that might be going from A to B, and you're paying a fee to the miners and you decide it's taking too long because miners will mine the biggest fee first generally, and so you can send the new transaction with the same origin, same destination if you like, and you increase the fee, and then that gets propagated to your peers.

Aaron van Wirdum: 00:03:39

Now you've already sort of described the use case.
If we want to put it in more abstract terms, it basically means that if there are conflicting transactions, the miner will pick the highest one, right?

Sjors Provoost: 00:03:54

Exactly.
So conflicting transactions means spending the same input.

Aaron van Wirdum: 00:03:57

I said highest one, I mean the transaction with the highest transaction fee.

Sjors Provoost: 00:04:01

Yes, that's right.

Aaron van Wirdum: 00:04:02

Yeah, so you just described one use case, you're sending a transaction and it's taking too long to confirm, so you send a new transaction with a higher fee.

Sjors Provoost: 00:04:11

Yeah, and that's a very  reasonable use case, you're sending a transaction with maybe one satoshi per byte because you're not in a hurry but then after a couple days you're like okay this is ridiculous and you bump it to 100 satoshi per byte and it goes in the next block.

Aaron van Wirdum: 00:04:25

Or after a month.
Right now we have transactions in the mempool that have been there for a month that pay one satoshi.
This is the first time ever I think this has happened.

Sjors Provoost: 00:04:34

Okay.

Aaron van Wirdum: 00:04:35

So, fee market is working, which Sjors, is the next point I want to make.
This is another argument in favor of Replace By Fee, is that it actually allows for more effective fee markets to happen?

Sjors Provoost: 00:04:48

Yeah, that's right.
Because in 2017, what we saw is that because people did not use Replace By Fee, they saw the mempool was quite full.
They thought, OK, currently the fees might be 50 satoshi per byte.
But I can't change it anymore.
So I'm just going to be safe and I'm going to set it to 100 satoshi per byte.
And then the next person would say - "Oh, well, that looks really expensive, let's make it 200 satoshi per byte."
So people were really bidding up against each other much more than was necessary.

Aaron van Wirdum: 00:05:15

Exactly.
With Replace By Fee, they could have instead paid, say one satoshi and then keep an eye on the mempool maybe and see, okay, you know what, it looks like my one satoshi transaction isn't going to confirm in the next block.
So you know what, I'm going to bump it to five.
And then sort of keep an eye on the mempool or wait for half an hour or however much in a hurry they are.
And in that way, sort of make sure that transaction confirms fast enough, but not overpay to make sure.

Sjors Provoost: 00:05:44

Exactly, yeah.

Aaron van Wirdum: 00:05:45

So we've got two benefits already.
One of the benefits is your transaction gets stuck, you want to get it unstuck.
The second benefit is it allows for better fee markets.
There's a third interesting benefit and I think there are more if we want to get into the details.
But one pretty obvious one is that with Replace By Fee, you can make more efficient use of the Bitcoin blockchain.
So for example, I'm paying you, Sjors, and then next I'm paying Ruben, who's not here today, but I'm also paying Ruben.
The way I could do that with Replace By Fee is I send you one transaction first, and after it I decide that I want to send Ruben a transaction. So now I create a transaction that pays you both and then include a good fee in that.
So now instead of using two different transactions, I can use one transaction, which is more efficient block space wise.

Sjors Provoost: 00:06:42

Yeah, and exchanges can do this at a much larger scale, right?
So they have lots of customers that they need to pay out and so they create one transaction and that's going to be in the mempool for a while, and so every time another user withdraws coins they just expand that transaction, and then whichever gets in the block - gets in the block and the rest will just make a new transaction.

Aaron van Wirdum: 00:07:02

Exactly, they can sort of keep updating this transaction by including more and more recipients.

Sjors Provoost: 00:07:07

Yeah, which also means more efficient use of the blockchain.
So you get more value for your fee bytes.

Aaron van Wirdum: 00:07:14

So there are three pretty good benefits.
One of them is getting transactions unstuck.
The second one is allowing for a more effective fee market.
And the third one is more block space efficiency.

Sjors Provoost: 00:07:26

Yeah, and I can mention a fourth one that will actually create a nice bridge to the downside.
Which is, let's say you make a one satoshi per byte transaction to an exchange, and that exchange is called Mt. Gox, and you read on Twitter that this is maybe not a very good exchange.
So you're like, okay maybe I don't want to do this anymore, and you can cancel a transaction because you can create a transaction with a higher fee that just goes back to you.

Aaron van Wirdum: 00:07:50

So you're describing it as a benefit now, but like you said, this is what critics of Replace By Fee would consider a detriment.

Sjors Provoost: 00:08:00

And it is, of course.

Aaron van Wirdum: 00:08:02

In a way.
There aren't that many critics of RBF anymore I think.
But yeah, the detriment, the downside is that it allows for double spending if the recipient isn't going to wait for confirmations.
So it's easier to double spend unconfirmed transactions with RBF.

Sjors Provoost: 00:08:20

Yeah, and this was of course a big discussion, say in 2015, 2016, when this, what we're going to talk about was introduced.
A lot of merchant applications would like to be able to just have an instant confirmation essentially, but it wouldn't be confirmed.
So that's inherently risky, but as I guess we'll explain, by default, if everybody played reasonably nice, it wasn't very risky.
But of course, in Bitcoin, we think long term and we don't want to rely on something that just requires too much kumbaya.

Aaron van Wirdum: 00:08:50

That was indeed a big discussion on whether or not we should allow RBF in the protocol; I'm saying protocol, but to be clear either way it's not actually a consensus rule.

Sjors Provoost: 00:09:02

There's a difference between consensus as in what is allowed inside of a block.
So if you see a block with something in it that's not consensus compatible, you will not accept the block, and so the miners won't get their reward, and it's really bad.

Aaron van Wirdum: 00:09:15

It's just an invalid transaction, invalid block.

Sjors Provoost: 00:09:17

Yeah, but there's all sorts of rules that pertain to how the network works, rules about which transactions a node will relay or which ones it will reject.
And those rules are written in the code.
So if you run the code as it comes, it'll do that, but there's not really any enforcement other than that.
You can change the code or change the setting and it will behave differently.

Aaron van Wirdum: 00:09:39

Yeah, these are like peer-to-peer layer rules.
And importantly, this is also for miners.
This is how they decide which transactions they include in blocks.

Sjors Provoost: 00:09:49

Yeah, but there it's even more important to realize that miners, of course, are very conscious of their revenue.
So they will probably change something if the code does something that's not favorable for them economically, and they can get away with it, they will do it.
Presumably, if it's not some edge case.

Aaron van Wirdum: 00:10:05

Yeah, so the reason it was sort of controversial at all in the first place is because the discussion was on whether or not RBF was to be included in Bitcoin Core.
And most Bitcoin nodes on the network are Bitcoin Core.
So if all Bitcoin Core nodes would, for example, reject Replace By Fee transactions, then it would actually be very hard to get your Replace By Fee transaction to a miner because nodes wouldn't relay it over the network.

Sjors Provoost: 00:10:34

Right, so you'd have to know who the miner is or there would have to be some nodes that would relay it anyway.

Aaron van Wirdum: 00:10:39

Yeah, or you'd have to be a miner or something like that.
So by including Replace By Fee in Bitcoin Core, that's how it would become a bit more easy to make an unconfirmed double spend.

Sjors Provoost: 00:10:53

Yes.

Aaron van Wirdum: 00:10:54

Okay, so that's sort of the argument against Replace By Fee.
Now let's debunk that argument, Sjors.
Can we?

Sjors Provoost: 00:11:00

Go ahead. Well, we already did it...

Aaron van Wirdum: 00:11:02

Well, I will first mention...
Did we?

Sjors Provoost: 00:11:05

Well, we at least brought up the point that we don't want to rely on people being nice and people using default settings.

## "First-seen-safe" RBF

Aaron van Wirdum: 00:11:11

Sure, that's the most obvious argument that it's possible whether you like it or not.
But like I said, whether it's included in Bitcoin Core kind of makes a difference on how easy it's going to be.
Well, I will mention, first of all, there's a thing called "First-seen-safe" RBF, which people were discussing back in like 2015, 2016.

Sjors Provoost: 00:11:31

Okay, how does that work?

Aaron van Wirdum: 00:11:32

The idea behind "First-seen-safe" RBF is that you can only replace transactions if the output, if the recipients, get at least the same amount of money.
So that way even an unconfirmed transaction is relatively safe under this context that we're talking about.
Because the transaction can be replaced, but only by adding even more recipients.

Sjors Provoost: 00:11:58

But there's a huge problem with that, which is that the blockchain has no idea who the change address is.
So normally what happens is...

Aaron van Wirdum: 00:12:06

Well, there's no change address at all.

Sjors Provoost: 00:12:08

Well yeah, but that's already a problem with Replace By Fee.
But let's say I'm sending you 0.1 Bitcoin and I use a coin worth 0.2 Bitcoin.

Aaron van Wirdum: 00:12:17

Oh, sorry, there is a change address.
There isn't a fee address.
I was confused.

Sjors Provoost: 00:12:21

Exactly.
That's good to remind the reader, there is no fee address.
There is just how much I'm sending you and then how much I'm sending myself as change.
And the difference between that is the fee.
The problem is if I send you 0.1 using a 0.2 coin, the change is going to be 0.1.
Then if I want to raise the fee, normally what I would do is I would just lower the change amount.
But with this rule that you just explained, you can't lower the change amount because the blockchain doesn't know, they might think I'm actually cheating the intended recipient rather than myself.

Aaron van Wirdum: 00:12:53

Right, that's a good point.

Sjors Provoost: 00:12:54

So that means you have to add another input every time you want to bump the transaction fee.
But that actually uses more block space, so it gets really expensive really fast.

Aaron van Wirdum: 00:13:05

Well, it could still work in the situation we described where an exchange adds new recipients in the payout to the rest, for example.

Sjors Provoost: 00:13:13

No, they would have the same problem.
Every time they add a new recipient, they would have to add a new input.

Aaron van Wirdum: 00:13:19

But that's fine.

Sjors Provoost: 00:13:20

Well, they'd have to have a Sahara Desert of dust to be able to keep doing that.
Because if they want to pay a thousand people, they need a thousand inputs.

Aaron van Wirdum: 00:13:29

I guess you're right.

Sjors Provoost: 00:13:30

So it does not sound very practical.
I've never seen this proposal myself.
I was not active at all in Bitcoin Core when this played out.
So, maybe this argument has been mentioned, maybe not.

## Opt-in RBF

Aaron van Wirdum: 00:13:41

Maybe I hadn't heard it actually, but you're right.
Then there is Opt-in Replace By Fee.

Sjors Provoost: 00:13:47

Okay.

Aaron van Wirdum: 00:13:48

This is what's actually in Bitcoin Core, right?

Sjors Provoost: 00:13:50

That's right.

Aaron van Wirdum: 00:13:51

Well, what Opt-in Replace By Fee means is the only way Bitcoin Core nodes will replace a transaction, if it includes a higher fee, is if the first transaction includes a special flag, so a sign that tells these nodes, it's fine to replace this transaction if it has a higher fee.

Sjors Provoost: 00:14:15

Right, and so this is still a way to be nice basically, but if you're a merchant and you're relying on this zero confirmation, if you see this flag you know that this thing might disappear from under you and Bitcoin Core nodes won't try to stop that.

Aaron van Wirdum: 00:14:31

Yeah, so the most practical sort of use case for this is if you are a merchant like BitKassa in the Netherlands, I think they will accept an unconfirmed transaction.
So if you're at a bar and you're buying a beer, they have a payment terminal and they will accept unconfirmed transactions unless it has a RBF flag because in that case they're just gonna say we're not sure enough that this transaction is not going to be replaced so this is a rejection from us.

Sjors Provoost: 00:14:59

Yeah and they have to do that in addition to checking the fee because if you're sending a transaction with a very low fee then it might also never get confirmed and you have a lot of time to try and replace it.
So it's still a can of worms I think is emergent to do this.
It's fine for small amounts I guess.
But then if it's fine for small amounts, why worry about RBF?
But also I guess the discussion now is not as critical as it was then, because now we have Lightning and we have pretty user-friendly wallets to the point where if you really want to accept something fast, Lightning is just much safer and better privacy too.
So back then that wasn't ready yet.

Aaron van Wirdum: 00:15:38

Right.
Yeah, there are still some proponents of full RBF as well.
I think Peter Todd is an obvious example, I'm sure there are more.
I probably would consider myself one.

Sjors Provoost: 00:15:48

I vaguely remember a mailing list post maybe a year ago where somebody suggested just turning on full RBF.

Aaron van Wirdum: 00:15:56

Right.

Sjors Provoost: 00:15:57

At some point in the future.
I think that didn't end up happening.

Aaron van Wirdum: 00:16:01

Right, Peter Todd's arguments, I don't know if these arguments have changed because it's been a couple of years since I wrote this article and spoke with him about this.
But his argument was that the way these types of merchants can be relatively sure that a double spend isn't going to happen with an unconfirmed transaction is by monitoring the network.
So having nodes on different parts of the network and see if there are any conflicting transactions going on.
And this is in itself a problem that they feel the need to do this because for one, it's bad for privacy, arguably.
Well, that's his argument anyways, because these nodes now have a better idea of where transactions originated.
And two, it's requiring resources from nodes on the network because these spying nodes or whatever you want to call them, these double-spend checking nodes, they have to get blocks and transactions from different nodes on network.
So, they're sort of wasting resources.
So it would be better, Peter Todd would argue, to just go for full RBF to make this kind of practices useless.

Sjors Provoost: 00:17:11

Yeah, but then those practices don't seem to be happening at a scale that's problematic, as far as I know.
So I don't know whether you want to change it or not.
The other thing is now that everybody's running Lightning nodes, those nodes will have pretty much all of the same problems that you just described.
They have to make sure that nobody's trying to close the channel on them or does anything fancy so, I think we're already at the place where you really need to pay attention to what's happening in the mempool.

Aaron van Wirdum: 00:17:38

Right, so there is now a version of Opt-in RBF in Bitcoin Core, and by the way mentioning Peter Todd I think he still maintains like a bunch of nodes that do full RBF.

Sjors Provoost: 00:17:50

Yeah he used to have a separate release that was full RBF and if you were sure that he wasn't trying to hack you, then...
I don't know if he released binaries or just code.
It's just a one-line change.

Aaron van Wirdum: 00:18:00

Right, so and the idea was there that people could still use full RBF if they want to, and I'm pretty sure that some miners actually do use full RBF.
Which makes sense because it's incentive compatible for them to do so.
They make the most money if they do so.
So anyways, but in Bitcoin Core, there is the Opt-in RBF version, and I think you have some more details about what it actually does.

Sjors Provoost: 00:18:22

Yeah, so I guess it's fun to describe it in a little bit more detail.
So given a transaction, like I said, I sent you money and I have some change back to myself, there are five rules that Bitcoin Core will check if I want to replace that transaction.
And this has been the case since 0.12.
So it's quite a while.

Aaron van Wirdum: 00:18:39

Five years ago?

Sjors Provoost: 00:18:41

Something like that.
Yeah, 2016.
So if a transaction spends one or more of the same inputs, right, that's the first condition...

Aaron van Wirdum: 00:18:50

That's what makes it RBF in the first place.

Sjors Provoost: 00:18:53

Yeah, because I can spend twice, that's a bad idea.
I could send you 0.1 Bitcoin and have a fee and then create a new transaction that uses different inputs, then of course the blockchain will just mine both of them and I have a problem.
So I have to replace the input and if I do that, then first of all I have to opt into this thing with the flag that we talked about.
That's rule number one.
And then the rule is the replacement transaction may only include an unconfirmed input if that input was included in one of the original transactions.
Which is a kind of a roundabout way of saying the opposite.
I can add new inputs to this new transaction because maybe I want to increase the fee, so I need some extra inputs or I want to add other people.
But this input has to be confirmed if it's a new one.
And my guess is that this is just to prevent a can of worms where I have a transaction that is unconfirmed and I'm sending it across all the nodes and it doesn't depend on any unconfirmed inputs.
And now I bump it, but now it does depend on all sorts of unconfirmed inputs.
And now I'm forcing everybody to figure out where those unconfirmed inputs are and maybe they have a super low fee and I guess it's too complicated to implement.

Aaron van Wirdum: 00:20:09

Right, yeah, I can see that.

Sjors Provoost: 00:20:12

Because think about what this code looks like on Bitcoin core. You see this new transaction and what are you going to do?
Oh now some of these dependencies are unconfirmed, I have to traverse that whole tree, I don't want to think about that, I only want to think about my descendants.

Aaron van Wirdum: 00:20:28

Yeah it would basically allow for types of denial of service attacks I guess where you just...

Sjors Provoost: 00:20:34

Yeah my guess is it's both for a denial of service but also just to make the code easier to implement for anybody who writes this this kind of node software.
Then, rule number three.
The replacement transaction pays an absolute fee of at least the sum of the original transactions.
Because you can replace one transaction plus a bunch of its descendants, the things spending from that, but the absolute fee has to be the same.

Aaron van Wirdum: 00:21:02

Or higher.

Sjors Provoost: 00:21:02

Yeah, the same or higher, exactly.
Which also means that if I paid you and then you paid somebody else and I want to replace my transaction, then the transaction that you paid to somebody else, I have to at least pay the same fee that was in there.
It's kind of a disincentive for me to re-org from under you because that's one of the annoying things with RBF, right?
I'm paying you, you're paying somebody else, now I bump the fee.
Oh, oops, the transaction you paid to somebody else is now gone.

Aaron van Wirdum: 00:21:30

Right.

Sjors Provoost: 00:21:30

And, well, I would have to really deliberately do that because I would have to increase the fee on my own transaction by enough that it also covers that transaction of yours that I just destroyed.
So in practice, this wouldn't happen.
We would either both agree to send the new transaction and somehow package them, or not.

Aaron van Wirdum: 00:21:49

Yeah, there are probably very little, if any, real-world examples where an RBF transaction would have a lower fee.
So it's just to prevent weird attacks and complications.

Sjors Provoost: 00:22:02

It is an annoying rule, and maybe we'll get to it, but it's probably necessary.
And then the fourth rule is - it has to increase the fee rate by the minimum relay fee.

Aaron van Wirdum: 00:22:12

Sure.

Sjors Provoost: 00:22:13

So usually at least one satoshi per byte, but if a mempool is full then the minimum relay fee is going to be higher.
So if the mempools are very full then you cannot bump by just one satoshi per byte you may have to bump by 10 satoshis per byte.

Aaron van Wirdum: 00:22:27

Right, this could differ from node to node. 
If they have different mempools for whatever reason then they might have a different idea of what the minimum relay fee is.
So it might make its way through parts of the network, but not others.
It's possible.

Sjors Provoost: 00:22:41

Yeah, this is a tricky bit, right?
Because you know from your own node how much is in the mempool, and so you have to estimate what the minimum fee rate is that still goes into your mempool.
But if you just start your node after stopping it, the mempool might be incomplete and so you might be more optimistic about how low the fee increment can be, so it's kind of annoying.
But it does make sense that you don't want people to spam the network.

Aaron van Wirdum: 00:23:08

Yep.

Sjors Provoost: 00:23:08

The fifth rule is, the number of original transactions and their descendant transactions to be evicted from mempool, must not exceed a total of 100 transactions.
So I guess a simple way to say this is that if you do something convoluted that touches more than 100 transactions, it's not going to work.
And another caveat that I don't think is in these rules, but it is there, is that if you replace a transaction, it has to opt into it, right?
Every one of its inputs has to opt into allowing this fee bump, but also for all the descendants, this has to be true.
So if I send a transaction to you and you send to somebody else, but your transaction does not opt into RBF, then I can't replace my own.
And also I can opt out of RBF.
I can bump the fee once and then I can say, now it's final, so I opt out in the last bump.

Aaron van Wirdum: 00:24:05

Oh, that's actually possible?

Sjors Provoost: 00:24:06

Yeah.
And this is probably also why there's so many problems, because we could talk about problems.

Aaron van Wirdum: 00:24:12

Oh, there are problems?

Sjors Provoost: 00:24:13

There are problems.

Aaron van Wirdum: 00:24:13

Darn.

Sjors Provoost: 00:24:15

Especially, well, let's start with a simple problem that I don't think I've seen a solution for.
Let's say I'm sending you a transaction, but I'm also sending Ruben a transaction.
I think we mentioned that example.
And those are two separate transactions.
But now I think, oh my God, what if I combine those transactions?
Because that will be more efficient.

Aaron van Wirdum: 00:24:37

It would be.

Sjors Provoost: 00:24:37

I can use fewer inputs in particular, because I have one input that goes to you, and I have one input that goes to Ruben, and if I combine them, then they go to both of you.
So that saves me a number of bytes.
But we talked about rule number three, so I don't think we can do that.

Aaron van Wirdum: 00:24:57

Oh, because it has a lower absolute fee in that case?

Sjors Provoost: 00:24:59

Yeah.

Aaron van Wirdum: 00:25:00

Right.
So there actually is a normal example where it would be handy.

Sjors Provoost: 00:25:03

Yeah, exactly.
So because I've increased the fee rate, because I have to increase the fee rate, but unless I double the fee rate, or I don't know what the factor is, because I've made the transaction smaller, the absolute fee is going to be lower.
So generally merging two transactions is not going to work with the current RBF rules.

Aaron van Wirdum: 00:25:20

So the way to go then would be my solution to just not make two separate transactions, but the second one needs to already be the RBF one, needs to already combine the two.

Sjors Provoost: 00:25:32

The downside of that is you need to track a little bit more things of what's going on.
Because in the example I gave you, if one of them confirms, so if the one with the combined one, if it confirms, then you're done.
If one of the original two confirms, then the combined one won't happen.
So it's more clear which one you need to bump.
But if you start combining things, you need to track more, because one of those versions will confirm, you need to remember which ones to add but you probably have to do something like that anyway, and a wallet can automate it.
This is not really a consumer use case that often because you might send more than one transaction per unit of time but usually it'll probably be confirmed before you get to the next one.
But for exchanges, it's irrelevant, they can build the automatic tracking software.
So maybe this is a non-issue, but I just wanted to bring it up to illustrate the rule.

And then there is transaction pinning, which is a problem with Lightning.
And here, I think the simplest way to say is, is with Lightning, you have two parties that craft a transaction together, but they have to decide in advance what the fee is going to be.
And that's annoying because fees can go all over the place.
So when two Lightning nodes are connected, they are constantly renegotiating those transactions and creating new ones, just because they want to take into account the fee weather.

Aaron van Wirdum: 00:26:58

Yeah, what you mean, I think, to be clear, is in Lightning, you need to create a transaction with your channel partner, but then sometimes you'll only broadcast that transaction months later, while at the time of negotiating the transaction, that's when you're deciding on what the fee is gonna be.
While months later maybe that fee is not gonna be enough.
That's the problem.

Sjors Provoost: 00:27:22

Yeah but as your lightning node is running it's talking to the other side and it will renegotiate.
So it's not too bad.

Aaron van Wirdum: 00:27:30

Okay.

Sjors Provoost: 00:27:30

Regardless, if the channel closes, maybe you don't reach each other, and it might be a very unfavorable fee.
So the idea here would be, wouldn't it be nice if you can agree on a very low fee, but you can RBF it yourself later.
And so there was some complicated thing done with these lightning transactions as well as a rule in Bitcoin Core that would let you add extra outputs to it.
And then each of the parties could RBF that, if they wanted to.

Aaron van Wirdum: 00:27:56

Right.
Yep.

Sjors Provoost: 00:27:57

But the weakness in that story is that if I'm evil, I could basically add a transaction to RBF it, and it would say, opt out of RBF, and the fee would be very low.
Because we talked about this rule that all of the descendants have to opt into RBF.
Does that make sense?

Aaron van Wirdum: 00:28:17

Can you repeat the last part?

Sjors Provoost: 00:28:19

So I'm doing this RBF transaction, but I'm opting out of it in that RBF transaction.
I'm using a very low fee.

Aaron van Wirdum: 00:28:24

Yeah, yeah.

Sjors Provoost: 00:28:24

So now you want to bump that.

Aaron van Wirdum: 00:28:27

Oh, right.
Yeah.
Got it.

Sjors Provoost: 00:28:29

You can't even add your own RBF anymore because one of the descendants is now opting out.
And there's various shenanigans like that.
You could add a chain of 99 transactions to it, so you violate the 100 maximum rule.
You add 99 transactions with a super low fee, now the other side cannot add number 100 or 101.
And all sorts of annoying shenanigans that if you go to a Lightning Developer mailing list, it is full of this sort of pure headache.
I don't think that just going for a full RBF would really solve that, because the other problem we talked about in another episode is just package relay in general.
Like, what do you do with these if somebody wants to replace a chain of 100 transactions?
That can of worms, I'm just going to leave it open, just saying that every now and then on the mailing list you'll see threads and people proposing different solutions and then people explaining why that doesn't work.

## The double spend that wasn't.

Aaron van Wirdum: 00:29:24

Yeah.
Okay, well, that was getting very into the weeds.
Let's get back to the beginning.
What actually happened with this double spend concretely?

Sjors Provoost: 00:29:32

Back to our amazing adventure that made it all the way to Bloomberg and crashed the market by 7%.

Aaron van Wirdum: 00:29:36

Allegedly, maybe.

Sjors Provoost: 00:29:38

No, I don't actually believe in astrology.
So basically what happened is [forkmonitor.info](https://forkmonitor.info), a site that I also work on, by BitMEX Research, detected two blocks at the same height.
It's called a stale block, or at least one of them is gonna be stale.

Aaron van Wirdum: 00:29:54

One of them is definitely gonna be stale, because, well, for obvious reasons.

Sjors Provoost: 00:29:57

Yeah, because other miners will see two blocks, and then there's some heuristics, like just build on the first one you saw, for example.
Also nodes will do that.
They will, if all things equal, they'll pick the first one they saw.
And at some point miners will build on one side or the other and that's going to be the final blockchain.
But now what happens is, in one of those blocks is a transaction that sends money to you, and in the other block is the same input but it goes to me.
That would be a double spend.
Now in this case what seemed to be happening is that somebody did an RBF fee bump, but the higher fee ended up in the shortest chain and the lower fee ended up in the longest chain.
This probably wasn't any nefarious thing it's just that those transactions and the fee bumps are moving around the mempools all over the Bitcoin network and you find a block just before you see the increased fee and you miss it.

Aaron van Wirdum: 00:30:53

Yeah so that's probably what happened is that there was one fee, and then there was a replacement fee, and while the replacement fee was still making its way over the network and reached one miner that mined a block, it hadn't yet reached another miner that also mined a block at the same time.
So now there were conflicting transactions in the two blocks.

Sjors Provoost: 00:31:13

Right, and if I remember correctly, this particular transaction also had an `OP_RETURN` script.
So it was probably some sort of protocol, like that's doing some sort of token thing.
And the `OP_RETURN` script was also changing.
So that's why it was marked as a double spend and not as a fee bump.
Because I wrote the detection code for that.
And one of the rules was, if the fee changes by a little bit, I'll consider it a fee bump with or without the RBF flag, because maybe people use it or they don't.
But if something weird changes, then it says, just manually investigate, this might be double spend.
And that, you know, crashed the market.
But yeah, there was nothing going on.

Aaron van Wirdum: 00:31:50

Yeah, it resolved exactly like you would expect it to resolve, exactly like how Bitcoin is designed.

Sjors Provoost: 00:31:55

All right.
Anything else then?

Aaron van Wirdum 00:31:57

No. 

Sjors Provoost: 00:31:57

All right.
Thank you for listening to the Van Wirdum Sjorsnado!

Aaron van Wirdum: 00:32:00

There you go.
