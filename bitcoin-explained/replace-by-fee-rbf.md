---
title: "Replace By Fee (RBF)"
transcript_by: varmur via review.btctranscripts.com
media: https://www.youtube.com/watch?v=E9L1CRP3W8k
tags: ["rbf","fee-management"]
speakers: ["Aaron van Wirdum","Sjors Provoost"]
categories: ["podcast"]
date: 2021-02-05
---
Speaker 0: 00:01:33

Live from Utrecht, this is the The Van Wirdum Sjorsnado.
Shorts, I heard Bitcoin is broken.

Speaker 2: 00:01:40

It is.
Yeah, it was absolutely terrible.

Speaker 0: 00:01:43

A double spend happened.

Speaker 2: 00:01:44

Yep, ruined.

Speaker 0: 00:01:45

And this is because a fatal flaw in the Bitcoin protocol.
That's how it was reported, I think, in Bloomberg?

Speaker 2: 00:01:54

Yeah, I couldn't find the original report by Bloomberg.
I think Cointelegraph reported it more or less in that way, and then Bloomberg referred to it.

Speaker 0: 00:02:01

Oh yeah, I think that's what happened.

Speaker 2: 00:02:03

But at least more recent articles I saw from Bloomberg were saying, oh, noobs thought it was broken and they were all googling double spends.

Speaker 0: 00:02:10

Oh, they corrected it?

Speaker 2: 00:02:11

I wouldn't say corrected it.
They were more like, you know, going meta on it.

Speaker 0: 00:02:16

On their own mistake?

Speaker 2: 00:02:18

So I don't know if it was their own mistake because I've only seen the haters basically saying that they made that mistake.

Speaker 0: 00:02:25

Fair enough.
Okay so to be clear Bitcoin is not actually broken.

Speaker 2: 00:02:30

Nope it's working as expected.

Speaker 0: 00:02:33

It's working exactly as expected.
Now we could get into a discussion on whether or not a double spend happens or not and that gets into the definition of double spend but we're not going to do that shorts no instead we're going to explain what was sort of this alleged fatal flaw in the protocol, which was replaced by fee, RBF.
Yes.
That was sort of why this alleged double spend could have happened?

Speaker 2: 00:02:58

Yeah, it could have happened even without that, but...

Speaker 0: 00:03:00

Oh, sure, yeah.
And I guess that's the sort of stuff we're going to discuss in this great podcast today.

Speaker 2: 00:03:05

Exactly, so stay with us and you'll learn more.

Speaker 0: 00:03:08

Okay, first of all, this thing is called replaced by fee.
Just in brief terms, what does it mean?
What is replaced by fee?

Speaker 2: 00:03:15

So it means you have a transaction that might be going from A to B and you're paying a fee to the miners and you decide it's taking too long because miners will mine the biggest fee first generally and so you can send the new transaction with the same origin same destination if you like and you increase the fee And then that gets propagated to your peers.

Speaker 0: 00:03:39

Yeah, well, now you've already sort of described the use case.
If we want to put it in more abstract terms, it basically means that if there are conflicting transactions, the miner will pick the highest one, right?

Speaker 2: 00:03:54

Exactly.
So conflicting transactions means spending the same input.

Speaker 0: 00:03:57

I said highest one, I mean the transaction with the highest transaction fee.

Speaker 2: 00:04:01

Yes, that's right.

Speaker 0: 00:04:02

Yeah, so you just described one use case, you're sending a transaction and it's taking too long to confirm, so you send a new transaction with a higher fee.

Speaker 2: 00:04:11

Yeah, and that's a very, you know, reasonable use case, you know, you're sending a transaction with maybe one satoshi per byte because you're not in a hurry but then after a couple days you're like okay this is ridiculous and you bump it to 100 satoshi per byte and it goes in the next block

Speaker 0: 00:04:25

yeah or after a month right now we have transaction in the mempool that have been there for a month that pay once a Toshiba.
This is the first time ever I think this has happened.
Okay.
So, fee market is working, which is the next point I want to make.
This is another argument in favor of replace by fee.
Is that it actually allows for more effective fee markets to happen?

Speaker 2: 00:04:48

Yeah, that's right.
Because in 2017, what we saw is that because people did not use replaceByFee, they saw the mempool was quite full.
They thought, OK, currently the fees might be 50 satoshi per byte.
But I can't change it anymore.
So I'm just going to be safe and I'm going to set it to 100 satoshi per byte.
And then the next person would say, Oh, well, that looks really expensive.
Let's make it 200 satoshi per byte.
So people were really bidding up against each other much more than was necessary.

Speaker 0: 00:05:15

Exactly.
With replace by fee, they could have instead paid say one satoshi and then keep an eye on the mempool maybe and see, okay, you know what, it looks like my one Satoshi transaction isn't going to confirm in the next block.
So you know what, I'm going to bump it to five.
And then sort of keep an eye on the mempool or wait, you know, half an hour, however much in a hurry they are.
And in that way, sort of make sure that transaction confirms fast enough, but not overpay to make

Speaker 2: 00:05:44

sure.
Exactly.

Speaker 0: 00:05:45

Yeah.
So we've got two benefits already.
One of the benefits is your transaction gets stuck.
You want to get it unstuck.
The second benefit is it allows for better fee markets.
There's a third interesting benefit and I think they're more if we want to get into the details.
But one pretty obvious one is that with ReplaceByFee, you can make more efficient use of the Bitcoin blockchain.
So for example, I'm paying you, Shors, and then next I'm paying Ruben, who's not here today, but I'm also paying Ruben.
And the way I could do that with replace by fee is I send you one transaction first and after it I decide that I want to send Ruben a transaction so now I create a transaction that pays you both and then include a good fee in that.
So now instead of using two different transactions, I can use one transaction, which is more efficient block space wise.

Speaker 2: 00:06:42

Yeah, and exchanges can do this at a much larger scale, right?
So they have lots of customers that they need to pay out and so they create one transaction and that's going to be the mempool for a while and so every time a user withdraws another user withdraws coins they just expand that transaction and then whichever gets in the block gets in the block and the rest will just make a new transaction.

Speaker 0: 00:07:02

Exactly, they can sort of keep updating this transaction by including more and more recipients.

Speaker 2: 00:07:07

Yeah, which also again means more efficient use of the blockchain.
So you get more value for your feebytes.

Speaker 0: 00:07:14

So there are three pretty good benefits.
One of them is getting transactions on stock.
The second one is allowing for a more effective fee market.
And the third one is more block space efficiency.

Speaker 2: 00:07:26

Yeah, and I can mention a fourth one that will actually create a nice bridge to the downside, Which is, let's say you make a one satoshi provide transaction to an exchange and that exchange is called Mt. Gox and you read on twitter that you know this is maybe not a very good exchange.
So you're like, okay maybe I don't want to do this anymore and So you can cancel a transaction because you can create a transaction with a higher fee that just goes back to you.

Speaker 0: 00:07:50

Right.
Yeah.
So you're describing it as a benefit now, but like you said, this is what critics of ReplaceByFee would consider a detriment.

Speaker 2: 00:08:00

And it is, of course.

Speaker 0: 00:08:02

In a way.
There aren't that many critics of RBF anymore I think.
But yeah, the detriment, the downside is that it allows for double spending if the recipient isn't going to wait for confirmations.
So it's easier to double spend on confirmed transactions with RBF.

Speaker 2: 00:08:20

Yeah, and this was of course a big discussion, say in 2015, 2016, when this, what we're going to talk about was introduced.
You know, a lot of merchant applications would like to be able to just have an instant confirmation essentially, but it wouldn't be confirmed.
So that's inherently risky, but as I guess we'll explain, by default, if everybody played reasonably nice, it wasn't very risky.
But of course, in Bitcoin, we think long term and we don't want to rely on something that just requires too much kumbaya

Speaker 0: 00:08:50

yeah so that was indeed a big discussion on whether or not we should allow rbf in the protocol I'm saying protocol but to be clear either way it's not actually a consensus rule

Speaker 2: 00:09:02

yeah so there's a difference between consensus as in what is allowed inside of a block.
So if you see a block with something in it that's not consensus compatible, you will not accept the block, and so the miners won't get their reward, and it's really bad.

Speaker 0: 00:09:15

It's just an invalid transaction, invalid block.

Speaker 2: 00:09:17

Yeah, but there's all sorts of rules that pertain to how the network works.
Things that which transactions a node will relay or which ones it will reject.
And those rules are, you know, they're written in the code.
So if you run the code as it comes, it'll do that, but there's not really any enforcement other than that.
You can change the code or change the setting and it will behave differently.

Speaker 0: 00:09:39

Yeah, these are like peer-to-peer layer rules.
And importantly, this is also for miners.
This is how they decide which transactions they include in blocks.

Speaker 2: 00:09:49

Yeah, but there it's even more important to realize that miners, of course, are very conscious of their revenue.
So they will probably change something if the code does something that's not favorable for them economically, and they can get away with it, they will do it.
Presumably, if it's not some edge case.

Speaker 0: 00:10:05

Yeah, so the reason it was sort of controversial at all in the first place is because it was going to be...
The discussion was on whether or not RBF replaced by fee was to be included in Bitcoin Core.
And most Bitcoin nodes on the network are Bitcoin Core.
So if all Bitcoin Core nodes would, for example, reject ReplaceByFee transactions, then it would actually be very hard to get your ReplaceByFee transaction to a miner because nodes wouldn't relay it over the network.

Speaker 2: 00:10:34

Right, so you'd have to know who the miner is or there'd have to be some nodes that would relay it anyway.

Speaker 0: 00:10:39

Yeah, or you'd have to be a miner or something like that.
So by including ReplaceByFee in Bitcoin Core, by including it, that's how it would become a bit more easy to make an unconfirmed double spend.

Speaker 2: 00:10:53

Yes.

Speaker 0: 00:10:54

Okay, so that's sort of the argument against replace by fee.
Now let's debunk that argument, Sjoerd.
Can we?

Speaker 2: 00:11:00

Go ahead.

Speaker 0: 00:11:02

Well, I will first mention...
Did we?

Speaker 2: 00:11:05

Well, we at least brought up the point that we don't want to rely on people being nice and people using default settings.

Speaker 0: 00:11:11

Sure, that's the most obvious argument that it's possible whether you like it or not.
But like I said, whether it's included in Bitcoin Core kind of makes a difference on how easy it's going to be.
Yeah.
Okay.
Well, I will mention, first of all, there's a thing called First Seen Safe Replaced by Fee, which people were discussing back in like 2015, 2016.

Speaker 2: 00:11:31

Okay, how does that work?

Speaker 0: 00:11:32

The idea behind first seen safe replaced by fee is that you can only replace transactions if the output, if the recipients, get at least the same amount of money.
So that way even an unconfirmed transaction is relatively safe under this context that we're talking about.
Because the transaction can be replaced, but only by adding even more recipients.

Speaker 2: 00:11:58

But there's a huge problem with that, which is that the blockchain has no idea who the change address is.
So normally what happens is...

Speaker 0: 00:12:06

Well, there's no change address at all.

Speaker 2: 00:12:08

Well yeah, but that's already a problem with replace by fee.
But let's say I'm sending you 0.1 Bitcoin and I use a coin worth 0.2 Bitcoin.

Speaker 0: 00:12:17

Oh, sorry, there is a change address.
There isn't a fee address.
I was confused.

Speaker 2: 00:12:21

Exactly.
So yeah, so that's good to remind the listener, there is no fee address.
There is just how much I'm sending you and then how much I'm sending myself as change.
And the difference between that is the fee.
The problem is if I send you 0.1 using a 0.2 coin, the change is going to be 0.1, and then if I want to raise the fee, well, normally what I would do is I would just lower the change amount.
But with this rule that you just explained, you can't lower the change amount because the blockchain doesn't know.
They might think I'm actually cheating the intended recipient rather than myself.

Speaker 0: 00:12:53

Right, that's a good point.

Speaker 2: 00:12:54

So that means you have to add another input every time you want to bump the transaction fee.
But that actually uses more block space, so it gets really expensive really fast.

Speaker 0: 00:13:05

Well, it could still work in the situation we described where an exchange adds new recipients in the payout to this, for example.

Speaker 2: 00:13:13

No, They would have the same problem.
Every time they add a new recipient, they would have to add a new input.

Speaker 0: 00:13:19

But that's fine.

Speaker 2: 00:13:20

Well, they'd have to have like a Sahara Desert of dust to be able to keep doing that.
Because if they want to pay a thousand people, they need a thousand inputs.

Speaker 0: 00:13:29

I guess you're right.

Speaker 2: 00:13:30

So it does not sound very practical.
I've never seen this proposal myself.
I was not very active in the...
I was not active at all in Bitcoin Core when this played out.
So, maybe this argument has been mentioned, maybe not.

Speaker 0: 00:13:41

Maybe I hadn't heard it actually, but you're right.
Then there is opt-in replaced by fee.

Speaker 2: 00:13:47

Okay.

Speaker 0: 00:13:48

This is what's actually in Bitcoin Core, right?

Speaker 2: 00:13:50

That's right.

Speaker 0: 00:13:51

So opt-in replaced by fee is replaced by fee.
Well, what it means is the only way Bitcoin Core nodes will replace a transaction, if it includes a higher fee, is if the first transaction includes a special flag, so a sign that tells these nodes, it's fine to replace this transaction if it has a higher fee.

Speaker 2: 00:14:15

Right, and so this is still a way to be nice basically, but if you're a merchant and you're relying on this zero confirmation, if you see this flag you know that this thing might disappear from under you and Bitcoin Core nodes won't try to stop that.

Speaker 0: 00:14:31

Yeah, so the most practical sort of use case for this is if you are a merchant like Bitcosa in the Netherlands, I think they will accept an unconfirmed transaction.
So if you're at a bar and you're buying a beer, they have a payment terminal and they will accept unconfirmed transactions unless it has a RBF flag because in that case they're just gonna say we're not sure enough that this transaction is not going to be replaced so this is a rejection from us.

Speaker 2: 00:14:59

Yeah and they have to do that in addition to checking the fee because if you're sending a transaction with a very low fee then it might also never get confirmed and you have a lot of time to try and replace it.
So it's still a can of worms I think is emergent to do this.
It's fine for small amounts I guess But then if it's fine for small amounts, why worry about RBF?
But also I guess the discussion now is not as critical as it was then, because now we have Lightning and we have pretty user-friendly wallets to the point where if you really want to accept something fast, Lightning is just much safer and better privacy too.
So back then that wasn't ready yet.

Speaker 0: 00:15:38

Right.
Yeah, there are still some proponents of full RBF as well.
I think Peter Toss is an obvious example And I'm sure there are more.
I probably would consider myself one.

Speaker 2: 00:15:48

I vaguely remember a mailing list post maybe a year ago where somebody suggested just turning on full RBF.

Speaker 0: 00:15:56

Right.

Speaker 2: 00:15:57

At some point in the future.
I think that didn't end up happening.

Speaker 0: 00:16:01

Right.
Yeah.
His arguments, Peter Todd's arguments from...
I don't know if these arguments have changed because it's been a couple of years since I wrote this article and spoke with him about this.
But his argument was that the way these types of merchants can be relatively sure that a double spend isn't going to happen with an unconfirmed transaction is monitoring the network.
So checking, you know, having nodes on different parts of the network and see if there are any conflict transactions going on.
And this is in itself a problem that they feel the need to do this because for one, it's bad for privacy, arguably.
Well, that's his argument anyways, because these nodes now have a better idea of where transactions originated.
And two, it's requiring resources from nodes on the network because these spying nodes or whatever you want to call them, these double-span checking nodes, they have to get blocks and transactions from different nodes on network.
So, they're sort of wasting resources.
Yeah, but- So it would be better, Peter Thal would argue, to just go for full RBF to make this kind of practices useless.

Speaker 2: 00:17:11

Yeah, but then those practices don't seem to be happening at a scale that's problematic, as far as I know.
So I don't know whether you want to change it or not.
The other thing is now that everybody's running Lightning nodes, those nodes will have pretty much all of the same problems that you just described.
They have to make sure that nobody's trying to close the channel on them etc does anything fancy so I think we're already at the place where you really need to pay attention to what's happening in the mempool

Speaker 0: 00:17:38

right okay so there is now a version of optin RBF in Bitcoin Core yep and by the way mentioning Peter Todd I think he still maintains like a bunch of nodes that do full RBF.

Speaker 2: 00:17:50

Yeah he used to have a separate release that was full RBF and if you were sure that he wasn't trying to hack you then I don't know if he released binaries or just code.
It's just a one-line change.

Speaker 0: 00:18:00

Right so and the idea was there that people could still use full RBF if they want to.
And I'm pretty sure that some miners actually do use full RBF.
Yeah.
Which makes sense because it's incentive compatible for them to do so.
They make the most money if they do so.
So anyways, But in Bitcoin Core, there is the opt-in RBF version.
And I think you have some more details about what it actually does.

Speaker 2: 00:18:22

Yeah, so I guess it's fun to describe it in a little bit more detail.
So given a transaction, like I said, I sent you money and I have some change back to myself.
There are five rules that Bitcoin Core will check if I want to replace that transaction.
And this has been the case since 0.12.
So it's quite a

Speaker 0: 00:18:39

while.
Five years ago?

Speaker 2: 00:18:41

Something like that.
Yeah, 2016.
So if a transaction spends one or more of the same inputs, right, that's the first condition.
So

Speaker 0: 00:18:50

remember, that's what makes it RBF in the first place.

Speaker 2: 00:18:53

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

Speaker 0: 00:20:09

Right, yeah, I can see that.

Speaker 2: 00:20:12

Because, you know, think about what this code looks like on the Bitcoin core end, you have to write, you see this new transaction and what are you going to do?
Oh now some of these dependencies are unconfirmed, I have to traverse that whole tree, I don't want to think about that, I only want to think about my descendants.

Speaker 0: 00:20:28

Yeah it would basically allow for types of denial of service attacks I guess where you just...

Speaker 2: 00:20:34

Yeah I think it's my guess is it's both for a denial of service but also just to make the code easier to implement

Speaker 0: 00:20:39

for

Speaker 2: 00:20:39

anybody who writes this this kind of node software.
Then rule number three the replacement transaction pays an absolute fee of at least the sum of the original transactions.
Because you can replace one transaction plus a bunch of its descendants, the things spending from that, but the absolute fee has to be the same.
So if I paid...

Speaker 0: 00:21:02

Or higher.

Speaker 2: 00:21:02

Yeah, the same or higher, exactly.
Which also means that if I paid you and then you paid somebody else and I want to replace my transaction, then the transaction that you paid to somebody else, I have to at least pay the same fee that was in there.
It's kind of a disincentive for me to re-org from under you because that's one of the annoying things with RBF, right?
I'm paying you, you're paying somebody else, now I bump the fee.
Oh, oops, the transaction you paid to somebody else is now gone.

Speaker 0: 00:21:30

Right.

Speaker 2: 00:21:30

And, well, I would have to really deliberately do that because I would have to increase the fee on my own transaction by enough that it also covers that transaction of yours that I just destroyed.
So in practice, this wouldn't happen.
We would either both agree to send the new transaction and somehow package them or not?

Speaker 0: 00:21:49

Yeah, there are probably very little, if any, real-world examples where an RBF transaction would have a lower fee.
So it's just to prevent weird

Speaker 2: 00:21:59

attacks and complications.
It is an

Speaker 0: 00:22:01

annoying rule,

Speaker 2: 00:22:02

and maybe we'll get to it, but it's probably necessary.
And then the fourth rule is it has to increase the fee rate by the minimum relay fee

Speaker 0: 00:22:12

sure

Speaker 2: 00:22:13

so usually at least one satoshi per byte but if a mempool is full then the minimum relay fee is going to be higher so if the mempools are very full then you cannot bump by just one satoshi per byte you may have to bump by 10 satoshi per byte

Speaker 0: 00:22:27

right this could differ from node to node if they have different mempools for whatever reason then they might have a different idea of what the minimum relay fee is.
So it might make its way through parts of the network, but not others.
It's possible.

Speaker 2: 00:22:41

Yeah, this is a tricky bit, right?
Because you know from your own node how much is in the mempool, and so you have to estimate what the minimum fee rate is that still goes into your mempool.
But if you just start your node after stopping it, the mempool might be incomplete and so you might be more optimistic about how low the fee increment can be, so it's kind of annoying.
But it does make sense that you don't want people to spam the network and you want to keep.

Speaker 0: 00:23:08

Yep.

Speaker 2: 00:23:08

So, and the fifth rule is, the number of original transactions to be replaced and their transcendent transactions will be evicted from mempool, must not exceed a total of 100 transactions.
So I guess a simple way to say is that if you do something convoluted that touches more than 100 transactions, it's not going to work.
Right.
And another caveat that I don't think is in these rules, but it is there, is that if you replace a transaction, it has to opt into it, right?
Every one of its inputs has to opt into allowing this fee bump, but also for all the descendants, This has to be true.
So if I send a transaction to you and you send to somebody else, but your transaction does not opt into RBF, then I can't replace my own.
And also I can opt out of RBF.
I can bump a few ones and then I can say, now it's final, so I opt out in the last bump.

Speaker 0: 00:24:05

Oh, that's actually possible?

Speaker 2: 00:24:06

Yeah.
Right.
And this is probably also why there's so many problems, because we could talk about problems.

Speaker 0: 00:24:12

Oh, there are problems?
There are problems.
Darn.

Speaker 2: 00:24:15

Especially, well, let's start with a simple problem that I don't think I've seen a solution for.
Let's say I'm sending you a transaction, but I'm also sending Ruben a transaction.
I think we mentioned that example.
And those are two separate transactions.
But now I think, oh my God, what if I combine those transactions?
Because that will be more efficient.

Speaker 0: 00:24:37

It would be.

Speaker 2: 00:24:37

Yeah, but because maybe I can, yeah, I can use fewer inputs in particular, because I have one input that goes to you, and I have one input that goes to Ruben, and if I combine them, then they go to both of you.
So that saves me a number of bytes.
But we talked about rule number three, so I don't think we can do that.

Speaker 0: 00:24:57

Oh, because it has a lower absolute fee in that case?
Yeah.
Right.
So there actually is a normal example where it would be handy.

Speaker 2: 00:25:03

Yeah, exactly.
So because I've increased the fee rate, because I have to increase the fee rate, but unless I double the fee rate, or I don't know what the factor is, because I've made the transaction smaller, the absolute fee is going to be lower.
So generally merging two transactions is not going to work with the current RBF rules.

Speaker 0: 00:25:20

So the way to go then would be my solution to just not make two separate transactions, but the second one needs to already be the RBF one.

Speaker 2: 00:25:32

The downside of that is you need to track a little bit more things of what's going on.
Because in the example I gave you, if one of them confirms, so if the one with the combined one, if it confirms, then you're done.
If one of the original two confirms, then the combined one won't happen.
So it's more clear which one you need to bump.
But if you start combining things, you need to track, I guess, because one of those versions will confirm you need to remember which ones to add but you probably have to do something like that anyway and a wallet can automate it yeah and this is not really a consumer use case that often because you know you might send more than one transaction per unit of time but usually it'll probably be confirmed before you get to the next one.
But for exchanges, it's irrelevant, but for exchanges they can build the automatic tracking software.
So maybe this is a non-issue, but I just wanted to bring it up to illustrate the rule.
And then there is transaction pinning, which is a problem with Lightning.
And here, I think the simplest way to say is, is with Lightning, you have two parties that craft a transaction together, but they have to decide in advance what the fee is going to be.
And That's annoying because fees can go all over the place.
So when two Lightning nodes are connected, they are constantly renegotiating those transactions and creating new ones, just because they want to take into account the fee weather.

Speaker 0: 00:26:58

Yeah, well, what you mean, I think, is to be clear, in Lightning, you need to create a transaction with your channel partner, but then sometimes you'll only broadcast that transaction months later, while at the time of negotiating the transaction, that's when you're deciding on what the fee is gonna be.
While months later maybe that fee is not gonna be enough.
That's the problem.

Speaker 2: 00:27:22

Yeah but as your lightning node is running it's talking to the other side and it will renegotiate.
So it's not too bad.

Speaker 0: 00:27:30

Okay.

Speaker 2: 00:27:30

Regardless yeah if the channel closes you know maybe you don't reach each other and it might be a very unfavorable fee.
So the idea here would be, wouldn't it be nice if you can agree on a very low fee, but you can RBF it yourself later.
And so there was some complicated thing done with these lightning transactions, as well as a rule in Bitcoin Core that would let you add extra outputs to it.
And then each of the parties could RBF that

Speaker 0: 00:27:56

if they wanted to.
Right.
Yep.

Speaker 2: 00:27:57

But the weakness in that story is that if I'm evil, I could basically add a transaction to RBF it, and it would say, opt out of RBF, and the fee would be very low.
Because we talked about this rule that all of the descendants have to opt into RBF.
Does that make sense?

Speaker 0: 00:28:17

Can you repeat the last part?

Speaker 2: 00:28:19

So I'm doing this RBF transaction, but I'm opting out of it in that RBF transaction.
Oh, right.
I'm using a

Speaker 0: 00:28:24

variable fee.
Yeah, yeah.

Speaker 2: 00:28:24

So now you want to bump that.

Speaker 0: 00:28:27

Oh, right.
Yeah.
Got it.

Speaker 2: 00:28:29

You can't even add your own RBF anymore because one of the descendants is now opting out.
And there's various shenanigans like that.
You could add a chain of 99 transactions to it, so you violate the 100 maximum rule.
You add 99 transactions with a super low fee.
Now the other side cannot add number 100 or 101.
And all sorts of annoying shenanigans that if you go to a Lightning Developer mailing list, it is full of this sort of pure headache.
And I don't think that just going for a full RBF would really solve that, because the other problem we talked about in another episode is just package relay in general.
Like, what do you do with these if somebody wants to replace a chain of 100 transactions?
Yeah, that kind of worm, I'm just going to leave it open, just saying that this is every now and then on the mailing list you'll see threads and people proposing different solutions and then people explaining why that doesn't work.

Speaker 0: 00:29:24

Yeah.
Okay, well, that was getting very into the weeds.
Let's get back to the beginning.
What actually happened with this double spend concretely?

Speaker 2: 00:29:32

Back to our amazing adventure that made it all the way to Bloomberg and crashed the market by 7%

Speaker 0: 00:29:36

Allegedly, maybe.

Speaker 2: 00:29:38

No, I don't actually believe in astrology.
So basically what happened is forkmonitor.info is a site that I also work on by BitMEX Research, detected two blocks at the same height.
It's called a stale block, or at least one of them is gonna be stale.

Speaker 0: 00:29:54

One of them is definitely gonna be stale, because, well, for obvious reasons.

Speaker 2: 00:29:57

Yeah, because other miners will see two blocks, and then there's some heuristics, like just build on the first one you saw, for example.
Also nodes will do that.
They will, if all things equal, they'll pick the first one they saw.
And at some point miners will build on one side or the other and that's going to be the final blockchain.
But now what happens if in one of those blocks is a transaction that sends money to you and in the other block is the same input but it goes to me.
That would be a double spend.
Now in this case what seemed to be happening is that somebody did an RBF fee bump basically but the winning like the higher fee ended up in the shortest chain and the lower fee ended up in the longest chain

Speaker 0: 00:30:40

and

Speaker 2: 00:30:40

this probably wasn't any nefarious thing it's just that those transactions and the fee bumps are moving around the mempools all over the Bitcoin network and you find a block just before you see the increased fee and you miss it.

Speaker 0: 00:30:53

Yeah so that's probably what happened is that there was one fee and then there was a replacement fee and while the replacement fee was still making its way over the network and reached one miner that mined a block, it hadn't yet reached another miner that also mined a block at the same time.
So now there were conflicting transactions in the two blocks.

Speaker 2: 00:31:13

Right, and if I remember correctly, this particular transaction also had an upreturn script.
So it was probably some sort of protocol, like that's doing some sort of token thing.
And the upreturn script was also changing.
So that's why it was marked as a double spend and not as a fee bump.
Because I wrote the detection code for that.
And one of the rules was like, if the fee changes by a little bit, I'll consider it a fee bump with or without the RBF flag, because maybe people use it or they don't.
But if something weird changes, then it just says, just manually investigate.
This might be double spend.
And that, you know, crashed the market.
Right.
But yeah, there was nothing going on.

Speaker 0: 00:31:50

Yeah, it resolved exactly like you would expect it to resolve, exactly like how Bitcoin is designed.

Speaker 2: 00:31:55

All right.
Anything else then?
No. All right.
Thank you for listening to the Van Weerdam Shorts NATO.

Speaker 0: 00:32:00

There you go.
