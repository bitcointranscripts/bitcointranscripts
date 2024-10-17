---
title: Scaling to Billions of Users
transcript_by: tijuan1 via review.btctranscripts.com
media: https://www.youtube.com/watch?v=5yPVp6vNHiY
tags:
  - scalability
  - sidechains
speakers:
  - Sjors Provoost
  - Aaron van Wirdum
date: 2023-07-10
episode: 82
summary: In this episode, Aaron and Sjors discuss a recent blog post by Bitcoin Core developer Anthony Towns, “Putting the B in BTC”, in which he outlines a vision for scaling Bitcoin to facilitate billions of users. As Aaron and Sjors walk through the article, they explain what some of Towns’ proposed solutions are, and which tradeoffs they entail.
---
## Introduction

Aaron: 00:01:54

It's a little bit of a different episode as usual because we're now really going to discuss one particular technical topic.
We're more describing an outline of a vision for Bitcoin.
And To be precise, it's going to be Anthony Towns' sort of scaling vision.
Right?

Sjors: 00:02:23

That's right.
Anthony Towns had a vision.

Aaron: 00:02:26

Who's Anthony Towns?

Sjors: 00:02:27

He's a Bitcoin developer.

Aaron: 00:02:28

He's one of the most prolific Coin Core developers.
So Anthony Towns wrote a blog post called "[Putting the B in BTC](https://www.erisian.com.au/wordpress/2023/06/21/putting-the-b-in-btc)".
That's B for billions of people he writes in his blogpost.
So the plan is we want to scale Bitcoin to billions of people and now he wrote a blog post on how we can do this.
So to start what we're gonna do is we're gonna kind of just run through this blog post and you're gonna comment on it and maybe I'll comment on it as well a little bit but we're kind of just For people that are too lazy to read it, we're going to just sort of explain what the idea is.
So how are we going to scale Bitcoin to billions of people?
All right, so essentially Anthony writes there are three kind of main ideas of doing that.
There are sort of three roads to get there if you will.
One is just make the tech super efficient.
Then the second one is don't have everyone validate every transaction.
And the third one is have most people transact off blockchain.
I guess first of all, these three strategies, is there a fourth one?
Do you agree with these three?
Is this sort of...

Sjors: 00:03:45

I think it's reasonable to say like, so the premise of how you use Bitcoin is that you run a full node and you validate all the blocks, but that gets harder and harder as blocks get bigger and since every transaction that people make takes up space, if you scale to a billion people then naively, you know, you end up with very large blocks in the easiest case.
So you could say, well, maybe we can make the validation of these large blocks simpler.
Or you can say, well, I guess it's not possible for everyone to validate.
Then we just say, you know, fewer people will do it.
Or you can say, okay, there should be fewer transactions, so that everybody can still validate the blockchain.
I think that's a reasonable triangle.
You can probably draw another one, but it's fine.

Aaron: 00:04:26

So we've had the block size wars a couple of years ago, of course, and this was sort of the central, you know, it's kind of a continuation of that debate we had back then.
And there were indeed different ideas.

Sjors: 00:04:43

And back in the days, people were especially doing number one in practice, making the tech more efficient.
You know, I've done an experiment in 2017 where I would take identical computers and try to sync the blockchain of that date using older and older versions of Bitcoin Core.
And what you can see is that for the same blockchain and the same computer Bitcoin Core was getting objectively faster every year.
But that has slowed down a bit.

## Technological Innovations

Aaron: 00:05:08

Okay, so...

Sjors: 00:05:08

But you could continue that process.

Aaron: 00:05:10

Anthony shared some thoughts on each of these approaches.
So let's just kind of walk through them.
So improving the tech.
He gives some examples of projects that are in development right now that would accomplish this.
So, one of them is Utreexo, which I think we did a whole episode on, right?

Sjors: 00:05:29

Yes, we did.

Aaron: 00:05:29

Well, what is Utreexo?
Do you want to summarize this in...

Sjors: 00:05:33

Utreexo helps with one of the many bottlenecks in Bitcoin.
I would say memory usage.
So basically what happens is...
One second.
So basically what happens, is that you have this thing called the UTXO set, which is the list of who owns which coin.
And you try to keep, your node keeps track of the list who owns which coin.
And that if, you know, if billions of people own a coin, then that list gets extremely long.
And so Utreexo fixes that by putting the entire ownership list in a Merkle tree and then rather than everybody having the full list when you want to spend a coin you need to prove that that coin exists in the first place.
So I don't have to as a node operator, I don't have to remember who owns which coin.
If you think you own a coin, you have to prove it to me and send me some data.

Aaron: 00:06:23

So as we mentioned, there are, I mean, there are essentially several bottlenecks when you want to scale Bitcoin up.
If everyone wants to check every transaction, then one of the things they need to do is keep this UTXO set.
So they need to keep a record of who owns what essentially.
And UTXO is a way to decrease the size of that record, right?

Sjors: 00:06:47

Mm-hmm.

Aaron: 00:06:48

Okay, so that's one bottleneck.
And then another one he mentioned is ZeroSync.
I don't know, do we...

Sjors: 00:06:55

We have not covered that in any episode.
I mean, there's more to it, I guess, but one of the objectives is to make it easier to catch up if you start from scratch.
So the first time you download the blockchain, maybe you can use zero knowledge proofs, which is fancy math, to say, okay, I'm just gonna assume that, or no, I know that everything that happened so far is correct, so just give me the latest UTXO set.
So instead of giving me all the blocks from the past to the present, give me the current set of who owns what and approve that this set was constructed using the official validation rules.
And ZeroSync tries to achieve that and I think they've done some of that work, like showing that enough proof of work is actually in the blockchain, but by far not all of it.
And that would help at least new users, which is part of the reasons why it's hard to run a node, because you have to catch up.

Aaron: 00:07:47

So that's another one of the bottlenecks that it could potentially help resolve.
So if one of the bottlenecks is the size of the UTXO set, then another bottleneck is the time it takes to sync the entire blockchain.

Sjors: 00:07:58

Assume UTXO is another approach to do that, where instead of delivering any proofs, or maybe you can combine these things, right?
You just say, okay, this is the UTXO set as of so many years ago, and then you're just kind of trusting that the past is real.
But maybe you can combine that.

Aaron: 00:08:16


Another example that Anthony mentioned is silenced payments which I think we also did an episode on with Ruben right?

Sjors: 00:08:23

So that's not an example of a scaling technology but that is an example of saying why it is important to be able to check every single transaction in every single block.
Because in order to use silent payments, which we have done an episode about, you as the recipient, as a sender it doesn't matter, but as a recipient, you have to scan every block and every transaction in a block to see if there is a payment to you.
And so if blocks become massive, or yeah, then that scanning effort becomes a problem.
It isn't right now it seems pretty lightweight but it could be if we make blocks a hundred times bigger.

Aaron: 00:08:58

Right okay well so in any case this is these are some examples that fit in bucket one, it's improving the technology.
However, I think Anthony's point is essentially that while there is room to grow here, this alone, it doesn't look like it's going to get us to a billion users.

Sjors: 00:09:18

No, and he mentions another thing with regard to the silent payments, if I see it correctly.
We mentioned the zero sync idea of catching up from start, but you could also imagine using something like zero sync to make jumps.
So instead of validating every block as it comes in, you can say, well, I'm just going to wait, you know, a month and then check whatever happened, get a compressed summary of the last month.
That could also be a way to keep track of a much bigger blockchain.
But you can't do that with something like silent payments because then you'd have to wait a month to know that you got paid.

## Challenges in Validation

Aaron: 00:09:47

Right, okay.
So that's bucket one, improving the tech, which will help us grow a bit, but it's not going to be able to get us to a billion, right?
So then we move to category two: Solutions, which is don't validate.
So here we really get into what the block size wars were about for a big part.
I think is that some people, and they still exist on other blockchains, they have this vision that it's actually not necessary for every user to validate every transaction.
Which can go in two directions, right?

Sjors: 00:10:24

You can say only some users validate everything, or you can say, well, most users validate some things, but not all users validate all the things.

Aaron: 00:10:33

Wait, can you elaborate on that?

Sjors: 00:10:35

Well, so the latter would be, let's say everybody runs an SPV wallet, which is just checking the headers.
It's still checking that there's proof of work, that headers are building on top of each other, that there's no funny things with timestamps, but it is not checking any of the transactions and the signatures in the block.
So that's a scenario where not everybody checks all the things.

Aaron: 00:10:54

No, that's a scenario where everybody checks not all the things.

Sjors: 00:10:58

That's the same thing.

Aaron: 00:11:00

No, no, that's a difference, right?

Sjors: 00:11:01

Not everybody checks all the things.
So there will still be people who run a full node and check all the things.

Aaron: 00:11:05

I guess that's also true.

Sjors: 00:11:06

But some people will only check some things.
Now, there's other blockchains, I think, like probably things like Solana, where really there is just a small number of people who check all the things, maybe.
But most people check nothing, basically.
So it's very black and white.

Aaron: 00:11:20

So basically, some people check everything and then everyone else asks these people, hey, what's going on?
Right?
That's essentially what it comes down to.
I mean, it's automated, obviously.
People are using APIs and that kind of stuff but that's what it comes down to.

Sjors: 00:11:34

And if you push that too far you know you have a centralized point of failure which they could either lie or they could exclude you from the system you know you basically go back to Paypal, worst case.

Aaron: 00:11:46

Yes, the people that are checking everything they could either collude to change the rules, make more than 21 million Bitcoin, or they can be regulated and introduce censorship, or they can do all kinds of things that we don't really want.

Sjors: 00:12:02

And just add my own thoughts here I think you could probably think about something in the middle where some people validate some things and some people validate other things but it's it's hard to reason whether or not that's gonna be safe.
We know the current approach works, it's like everybody checks everything. And how much of that you can, you know, how far you can go on the gray scale towards one person checking everything.
There's some point at which it goes horribly wrong.
So it's better to be on the safe side, I think.

Aaron: 00:12:29

Well, essentially, so this option, it's included in the blog, sort of more as an example of what not to do, right?

Sjors: 00:12:38

And he also says that even this pushes to the limits of even those few people that validate if they really want to process every transaction of every person on the planet still becomes a problem or it's a fragile system that's easy to mess with.

## Off-Blockchain Transactions

Aaron: 00:12:53

So then we get to the third option which is kind of I would say the heart of the article like this is kind of deficient really which is get off the blockchain.

Sjors: 00:13:03

Get off the blockchain.

Aaron: 00:13:04

So not all transactions need to happen on the Bitcoin blockchain.
So what does that look like?

Sjors: 00:13:11

Well, I mean, the most obvious example of that is Lightning, where instead of every time you want to send a satoshi you create a bitcoin transaction now you create a bitcoin transaction to open a channel you use the lightning network for a while to make a bunch of payments and then after a while you close the channel either because you want to or because you're forced to. Unfortunately if you run the numbers on that, which has been done by Tadge Dryja seven years ago, I think, you still end up with like, it's not going to fit the whole population.
Just a few tens of millions.

Aaron: 00:13:44

The problem with that is that even if you use Lightning, you still need some transactions on the blockchain, right?

Sjors: 00:13:50

Yes, if you do the math on like every person opens one channel per year or closes one channel per year, then that still doesn't fit the whole world population onto the Bitcoin blockchain.
So you still have to answer the question that we asked before.
Like, okay, does that mean some people don't use the blockchain or do we make blocks bigger and then do we not validate them, etcetera.
So that doesn't solve it all the way.

## Sidechains and Federated Systems

Aaron: 00:14:16

So Lightning doesn't solve the problem completely, but there is another idea, Sjors, there is another idea called sidechains.
Yes.
What's your opinion on sidechains?
We've done an episode or two or we've...

Sjors: 00:14:30

Well, we've talked about some examples of sidechain-ish systems,
like drivechains and other things.

Aaron: 00:14:35

Basically every time Ruben was here, it was something sidechain-ish, right?

Sjors: 00:14:40

That's right.
So just look for the episodes with Ruben and you can learn all you want about that topic.
Problem is, so far it hasn't been proven out.
So critically, it is very easy to move your Bitcoin assets onto some sort of other chain, but moving them back always requires some unpleasant trade-offs.

Aaron: 00:15:00

Well, kind of the...
Well, yes, but it also kind of depends.

Sjors: 00:15:03

Either like a custodian, like in the Liquid case where it's just, you're essentially just using a custodian with some benefits or in the case of drive chains where you, you know, you have a very long withdrawal window in which you have to do some fighting and stuff.
So it's, there's no like clean mechanism.
Ideally, the ideal of a sidechain is there's this other chain with completely different rules doesn't matter what it is could be small blocks could be big blocks could be smart contracts or not and you can move one Bitcoin onto it and as long as that other chain doesn't implode, you can take that Bitcoin off of it.
But the problem is that other chain tends to be much less secure from a censorship resistant point of view as the Bitcoin blockchain.
So in a worst case, you're depending on a custodian actually giving you money back and slightly better cases is still not as strong as getting your money out of say a lightning channel.

Aaron: 00:15:50

Well in the case of Liquid, it's not necessarily one custodian, right?
It's allegedly at least a federation of custodians.
We don't know who's in the Federation, but it's supposedly a group of companies that all hold sort of keys to a multi-sig.

Sjors: 00:16:06

They've, you know, they've built in a lot of automation, etc, etc.
And you can swap with other people.
So it's not horrible, but it's still not as secure as Bitcoin itself.

Aaron: 00:16:15

There's a trade-off there.
So that's an idea.
Another idea which is newer is something like Fedimint, right?
Have we done an episode of Fedimint?

Sjors: 00:16:26

Yes, we have.
We've done an episode about federated e-cash in general, where we explained the whole history from David Chaum onto the latest.
I mean, it has evolved a little bit, but we have explained it.

Aaron: 00:16:36

Yes, we did.
I remember now, yes, that's right.
So that's another idea, which is also a federated custodian.

Sjors: 00:16:43

I would just say that's a custodian, but it's a custodian with benefits.

Aaron: 00:16:48

Well, Fedimint has also a federated custodian model, right?
Sure, in theory.
Again, yes, you still have to sort of trust them.

Sjors: 00:16:57

I mean, a federation could also just be one company that has three different staff members in different parts of the world.
But in any case, it at least makes, you know, you can make custodians suck less.
I think that might be one way to frame it.
So Liquid makes custodians suck less because the custodians are spread out over different companies and they use a bunch of automation and they can't necessarily see what you're doing.
Fedimint, similarly, you have a lot of privacy against your own custodian, so they can rug you, but other than that, they can't really see what you're doing, so that's good.
And then, I think as the article says, there are just regular old custodians.

Aaron: 00:17:34

Exchanges, for example, and hosted wallets, that kind of stuff.
So what's the idea here?
Sjors, do you just want to get to the point of the article, I guess, at this point?

Sjors: 00:18:43

I'm not sure if it's making a very explicit point here.
I think you're saying you could have a number of custodians in the thousands or tens of thousands.
If you have that many different custodians, then at least there's lots of choice in the market and people can move between them.
And then it would fit with the current transaction counts.

Aaron: 00:19:02

I think if you do some back of a napkin math, the idea sort of is that if you have a lot of custodians that suck a little bit less, and they are connected through Lightning, then you can actually get to the point where Bitcoin could support billions of users.
So anyone can sort of choose the custodian and the trade-offs that they want.
So that can be a sidechain, it can be a venement kind of thing, it can be like an actual custodian of an exchange.
And these custodians in general would talk with each other over Lightning.
So then you can sort of do the math of how many on-chain transactions that would require per custodian and how many custodians we need and that would sort of get us to billions of users, right?
I think that's kind of the summary of the article that sort of considering the trade-offs that we're dealing with that's maybe the most viable vision right now?

Sjors: 00:20:06

Though my concern with custodians is that generally in economics you get this power law distribution of one or two massive custodians and then you know 10,000 very small ones and my issue is not with those 10,000 very small ones but with those very big ones that could have some pretty undue influence over the whole protocol and of course... 

Aaron: 00:20:29

Can you explain what you mean by that?
What's your concern?

Sjors: 00:20:34

I mean, I don't know, if somebody owns and controls 50% of all the Bitcoin, and they can do all sorts of shenanigans, right?
If there's a fork, they can...

Aaron: 00:20:44

What kind of shenanigans?

Sjors: 00:20:45

I don't know, like SegWit2x?

Aaron: 00:20:48

Can they though?
So what, spell it out, spell it out.
I want to hear the concept.

Sjors: 00:20:53

Well, so in this case, you know, we remember from the 2017 situation where there was a bunch of companies that got together and said, hey, we're going to double the block size and we're just going to tell our customers, at least that was the initial plan, we're going to tell our customers that Bitcoin didn't change, we just upgraded it, even though they actually just put you on something that would be considered a hard fork.
Now, at the time, there were not that many people running nodes, but if you look at probably the ratio of people running nodes versus people using these custodians, that's probably gonna get worse in this far future.

Aaron: 00:21:24

Well, that is that is..

Sjors: 00:21:26

the universe.

Aaron: 00:21:27

Yes, exactly.
Yes.

Sjors: 00:21:29

And presumably they're also gonna be more competent because I think one of the reasons SegWit2x didn't work out is because they just couldn't get the software working.
Now that might change if you know the whole world is using Bitcoin.
Hopefully there'll be far more competent people.
Well hopefully in the sense that it'll be good for Bitcoin but not hopefully in the sense that these very competent people will be working for those companies.
So, because they're paying the money.
I'm basically worried about-

Aaron: 00:21:56

The point here though, Sjors, is- 

Sjors: 00:21:58

If you're not validating the rules, then it seems much, much easier.
If 99% of users are not holding their own UTXOs and are not validating blocks, then yeah, 1% is going to notice the hard fork.
Then all you have left is to hopefully that this minority rule thing works, that that 1% is often enough to stop the fork.

Aaron: 00:22:21

Well, no, not exactly.
So I think the better way of understanding this vision, so to say, is We are keeping the block size limited explicitly so that people can still validate the rules.

Sjors: 00:22:39

Even if I guess you could say it's true that you could use a custodian, but still run a full node, right?
It's just that your coins are not on it.
All you know is where your coins are maybe within the custodian.

Aaron: 00:22:48

So you still know that there are only 21 million coins.
Now, I guess the more realistic risk, which is or the risk that I would be more concerned about, which is also mentioned in the article, is more like fractional reserve kind of problems.
So there's still only 21 million Bitcoin, that can change that you're still validating that.
However, you're not sure that the custodian that you are trusting is really holding the coins that it says it's holding and it's not issuing more.
Now that can maybe be because you can choose your custodian that can maybe be sort of tackled with proof of reserves or that kind of stuff, which is not perfect, but it's at least better than nothing.
And that's how you can sort of keep them in check.
And again, because you can switch custodians, whatever you want.
So that's, I guess my opinion about this is this seems to me like the most viable and best vision we have so far and then hopefully over time people can figure things out that are even better but so far this seems like this this can work with the technology that we have today, with our knowledge of Bitcoin that we have today, this seems like probably the best vision considering all the trade-offs?

Sjors: 00:24:09

I mean there's one other option, which is that you just don't get billions of users, you only get a few tens of millions of users, in which case, you know, Bitcoin would not be the global reserve currency, but it might be the global international trade currency or something like that.
In that case, you know, we don't need too many massive technological breakthroughs because it'll work.

Aaron: 00:24:31

So in that, so in that vision, Bitcoin is kind of the currency you use when the other things don't work.
You would usually just use PayPal, except if you want to buy drugs.

Sjors: 00:24:42

Maybe slightly better than that.
Maybe it is the preferred currency if you're doing international trade, say outside, you know, from Europe to America or something like that.
But I don't know if that's even likely.
I mean, that is an option.
Like there's no, nobody says that billions of people want to use Bitcoin.
Maybe it's, it doesn't need that many users.
It's, But though I would prefer if we do have a way to support the entire world population.
But so far I don't really see a way to do that other than, yeah, I guess what's described here, but that's not a very satisfactory solution.

Aaron: 00:25:13

I mean it's not perfect, But it's good to have at least an idea of how you can scale if we need to, right?
That's what I think anyways.

Sjors: 00:25:22

So I'm just hoping for a big breakthrough.
And maybe that's not unreasonable.
Maybe in the next couple decades, somebody comes up with a way to say, okay, we can add two more zeros to the number of users, and now we're good.

Aaron: 00:25:35

Finally, before we end this episode, so there's kind of Anthony Towns lays out how to get from here to there.
I don't think there's anything particularly shocking there.
It's kind of what you would expect.
It's, you know, stuff.

Sjors: 00:25:50

I think what he's describing here is a phenomenon that we only, developers only fix problems when they become actual problems.
So we all know the theoretical things that can go wrong with Lightning, but until they actually start happening, until Burak hits the button and blows up a bunch of nodes, bugs don't get fixed.
So I think what he's saying here is that at some point, more and more people start using Lightning, then we start running into the bottlenecks, the known ones, but also maybe some surprises.
And as those get fixed, well, at some point we'll also hit the hard limits of what these systems can do, you know, as we work through the bottlenecks.
And then people will jump to the next best alternative.
So Maybe if lightning becomes too expensive, they'll use liquid or something like that.

Aaron: 00:26:34

Yes.
I mean, that's sort of what the plan sounds like.
Let's run into the bottlenecks and then people will find alternatives, right?

Sjors: 00:26:45

Exactly.
So fee pressure could go up that can force people to go to alternatives or other usabilities could cause that too.
So that's just a, yeah, sort of a guess of how it could, how the network might scale in practice.
So not smoothly, but more in, I guess, in bumps and innovations.

Aaron: 00:27:03

Okay.
I think that sort of covers it, Sjors.
What do you think?

Sjors: 00:27:06

I think so too.

Aaron: 00:27:07

So nothing too shocking in this episode, but we still want to give you an episode before we take a break, because you're going traveling on holiday, Sjors.
Is that right?

Sjors: 00:27:16

Probably yes.

Aaron: 00:27:18

And then we'll see you when?

Sjors: 00:27:19

We'll keep you posted.
Thank you for listening to Bitcoin

Aaron: 00:27:23

Explained.
