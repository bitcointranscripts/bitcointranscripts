---
title: Ocean Tides
transcript_by: aassoiants via review.btctranscripts.com
media: https://bitcoinexplainedpodcast.com/@nado/episodes/episode-86-ocean-tides-hktbg
tags:
  - pooled-mining
speakers:
  - Sjors Provoost
  - Aaron van Wirdum
date: 2023-12-06
episode: 86
summary: In this episode of Bitcoin, Explained, Aaron and Sjors explain what features are offered by Ocean, the relaunched and rebranded Eligius mining pool. They discuss how payouts from this pool are (partially) non-custodial, how the block template creation is fully transparent, and how payout distribution is determined. Aaron and Sjors also briefly touch on the “spam” filtering employed by Ocean, and how that potentially affects profitability of the pool.
---
## Introduction

Aaron van Wirdum: 00:00:21

Live from Utrecht, this is Bitcoin Explained.
Hey Sjors.

Sjors Provoost: 00:00:26

Hello.

Aaron van Wirdum: 00:00:57

Sjors, today we're going to discuss a new mining pool launched.
Well, kind of.
Ocean Pool.
I was invited to the launch event.
It was sort of a mini conference.

Sjors Provoost: 00:01:15

I felt a very strong FOMO for that one.

I saw the video, you guys were in the middle of nowhere.
And some like some horror movie video shoot game basically scene.

Aaron van Wirdum: 00:01:26

It was quite nice actually.
There was like this hydro plant.
What's a good English word for this?
Rustic?
I don't know if that's the right word.
But it was nice.
Let's just say it was nice, nice environment.
They launched this pool.
So it's really the relaunch or re-brand of Eligius.
The Luke Dashjr pool.
This time it's backed by Jack Dorsey, among other investors.
And their goal, their intention is to re-decentralize mining essentially, or decentralize mining.

Sjors Provoost: 00:02:04

Right.
And they're calling it Ocean.

Aaron van Wirdum: 00:02:07

Yeah.
Ocean Pool.
So decentralizing mining pools or at least this one, or mining in general, ultimately is the goal.
The most notable innovation that they started with, that they launched with, is they have this non-custodial setup.
Kinda.
Or I mean, that's the goal, the intention.

## How Ocean Pool Works Relative to Mining, Custody, and Coinbase Rewards

Sjors Provoost: 00:02:34

I guess one diplomatic way to call it would be custody minimized.
You can have long legal discussion about what custody means, but I think we care most about the technical sides of it.
And then you can ask practical questions like could the mining pool steal your money?
Could the big forces steal your money?
And we can try to get into some of the nuance of what they're actually doing.

Aaron van Wirdum: 00:02:57

To clarify this, what mining pools usually do is.
When a mining pool finds new coins, the mining pool gets these coins.
These coins can't be spent for a hundred blocks.
Well, that's actually not what happens with most pools...
I was going to say after a hundred blocks, these coins are distributed to the miners, but that's not actually how mining pools work.

Sjors Provoost: 00:03:28

I would say there's a bigger separation there.

The mining pool has a wallet.
The coins they earn go into that wallet.
And the miners are paid from that wallet.

But it is a bit of an omnibus, and not necessarily trivial to understand which mined sat belongs to which specific individual miner.

Aaron van Wirdum: 00:03:46

A way that they will explain it or Bitcoin Mechanic is essentially: most bitcoin miners or hashers, as we've also called it, aren't actually mining bitcoin.
They're just selling their hash power to a mining pool.

Sjors Provoost: 00:04:03

That sounds a little bit like a separate issue, though it's a bit related too.
What it is that you're doing as a miner.
Are you producing blocks or are you just delivering hash rate to a buyer?
And that depends on the incentive model, the exact business model.
I think we'll get into that a bit later.
But the idea of holding coins custody, you could do that with this model too, I think you just don't have to.

Aaron van Wirdum: 00:04:30

Yeah.
It is a slightly separate issue.
I just wanted to point it out real quick.
The main innovation here is essentially that hashers, as we’ll call them.

To clarify that: there's the mining pool or the mining pool operator, that's doing most of the bitcoin stuff.
Downloading blockchain and constructing the block template, which is a big part of it.
Which might not happen in the future with Stratum V2.
But we've made another episode about that.

At least right now, most mining pools still create block templates.
Which transactions go into a block.
I lost my train of thought, but I think I was going to say with Ocean, the new coins are directly paid to the hashers.

Sjors Provoost: 00:05:16

The coinbase transaction, which is what every new block contains, has a number of outputs.
And typically these just go to the general wallet of the pool.
But with this new Ocean Pool, as much as possible, the coinbase transactions go directly to the miners.

With the caveat that you cannot do that for all mined transactions.
Not for all miners.
And there are two reasons for that.

Aaron van Wirdum: 00:05:41

Let's get into that.
First let's point out some advantages of this.
The biggest one is.
Right now, if you're a hasher and you want to join a pool, most pools have KYC stuff going on.
You need to actually tell the pool who you are, at least some of the big ones have this.
And Ocean does not have this.

Sjors Provoost: 00:06:00

Yeah, but I don't think that's inherent to this model at all.
Like you could still have KYC in this model or not.

Aaron van Wirdum: 00:06:07

I guess in their view or what they will argue or what they think or what they believe is that this way it's legally possible to not do KYC.

Sjors Provoost: 00:06:18

We're not lawyers.
I'm a developer.
You're a journalist.

Aaron van Wirdum: 00:06:23

But in any case, they aren't doing KYC stuff.
That's for sure.
Right now, you can just plug in and start mining.

Sjors Provoost: 00:06:29

One thing that they're doing very practically is that you as a miner don't create an account or you don't have to.
You just provide a bitcoin address straight, directly from the miner.

Aaron van Wirdum: 00:06:40

Right.
You get paid directly from the coinbase as a hasher, to the extent that it is possible.

Sjors Provoost: 00:06:52

Yeah, and that extent is quite limited because of two reasons.
One is a coinbase transaction can only have this many outputs.
Or even if you could have as many as you want, at some point it's just not worth paying the fees.
Or not so much paying the fees, because the coinbase transaction doesn't pay fees.
But you are using up space that others could pay.
That other people are paying you fees as a pool.
If you make a one megabyte coinbase transaction, then you can do that.
And you pay zero fees for it.
But you are now no longer mining anything.

Aaron van Wirdum: 00:07:25

Well, you could create a 4 megabyte coinbase transaction.

Sjors Provoost: 00:07:28

I don't think so because there's no witness.

Aaron van Wirdum: 00:07:30

Maybe two?
Right.
Let's separate these issues.
First of all, you said you can't necessarily pay every hasher because the number of outputs in the coinbase transaction is limited?

Sjors Provoost: 00:07:42

I don't know if there's an actual limit there that matters.
But basically it's just not worth the opportunity cost of making very small payments in the coinbase.
But there is a second...

Aaron van Wirdum: 00:07:52

It's the same issue?
There is no actual limit to the number of outputs in the coinbase transaction.

Sjors Provoost: 00:07:56

I think it's just a regular transaction, whatever that limit is.
It might not be one.
I should know that.
The second limit, the second limit is a little bit more mundane.
Apparently, some of the mining hardware out there starts to panic if you put more than 20 outputs in a coinbase transaction.

That has nothing to do with the bitcoin limits.
It's just that some mining equipment just panics when there's too many outputs.

In practice, the limit is about 20.
The top 20 miners get paid directly from the coinbase.
Then there's some amount left.
And that essentially goes to a wallet.
But they make sure that from that wallet, after a hundred blocks, because then you can spend it, it immediately goes to the correct miners, as if they were part of the coinbase essentially.

Aaron van Wirdum: 00:08:49

I thought, wrongly probably, that there was a limit on the number of transactions on the coinbase output.
And you just said, that's probably not the case, but some hardware has this issue.
That's where the limit comes from.

Sjors Provoost: 00:09:04

Yeah.

Aaron van Wirdum: 00:09:05

Okay.
And you say that limit is 20.

Sjors Provoost: 00:09:07

Apparently roughly 20.

Aaron van Wirdum: 00:09:09

20 ish.
There can only be 20 transaction outputs from a coinbase transaction.

Sjors Provoost: 00:09:16

That secondary transaction, which can only happen after a hundred blocks, because of the coinbase maturity rule, that's a consensus rule.
That transaction is kind of just like it was part of the coinbase itself, right?
It also has the same fee trade-offs here where yes, you can put whatever giant transaction you want in there as a pool, but then you're foregoing fee revenue from other transactions.
This transaction just spends from the coinbase.

Aaron van Wirdum: 00:09:40

If there's just too many hashers that need to be paid from the coinbase, if it's more than 20 essentially, then some of them will be paid later, still as soon as possible, but later.
Then the other thing was.
If you're a hasher and you don't earn enough from a block, then you also won't get paid immediately.

Sjors Provoost: 00:10:03

Right.
Then the idea is to basically wait until you've accumulated enough credit, as it were, and then you get paid.
So there, it really starts looking like just a wallet that's custodial, but only for small amounts.

## Future Ocean Pool Ideas & CHECKTEMPLATEVERIFY (CTV)

Aaron van Wirdum: 00:10:18

So, that's how it works today.
And then there are some ideas for the future to improve that a little bit more.
One of them is using Lightning for payouts.

Sjors Provoost: 00:10:32

Yeah, that kind of makes intuitive sense.
When you have very small miners that want to collect small rewards, maybe they get like 20 satoshis every block.
Lightning is a way to do that.
Then the question is how non-custodial can you make lightning?
I believe if you listen to the Stefan Livera podcast, Bitcoin Mechanic explains some ideas of how to do that roughly.
Using some sort of market, where if you have lightning liquidity, you essentially buy the rights to the payouts from the pool.
The pool is not doing the lightning payouts.
They're just giving payouts to addresses, but somebody else does some swapping of who gets which points.

Aaron van Wirdum: 00:11:15

Right.
Then there's another potentially cool idea, which is not possible yet on the bitcoin network.
But with CHECKTEMPLATEVERIFY, it could actually be implemented that if this 20 limit threshold in the coinbase is reached, then the other hashers are still guaranteed their payment through a CTV transaction because of that.

Sjors Provoost: 00:11:39

Yeah, and even better than that, regardless of this 20 limit.
You have to put the addresses in the coinbase right now.

You don't want to do that when fees are really high, because that's an opportunity cost.
But maybe you want to pay people when fees are low.
CTV is quite interesting for that.
We have not really discussed that in any podcast.
But it's basically a software proposal that commits to certain transactions happening in the future.
One of the intended use cases is congestion control.
This would be a very nice use case for it, where the coinbase only has one output, or maybe a couple, which is the CTV transaction.
Then all the miners know for sure that they will get those coins.
But they'll wait until fees are low, and then they'll get them.

Aaron van Wirdum: 00:12:26

That was the non-custodial part of the pool.
Which is probably kind of the main innovation, but it's not the only thing going on.

Sjors Provoost: 00:12:36

Or the custody minimized part of the pool.

## Ocean Pool & the Block Template

Aaron van Wirdum: 00:12:38

You're very right.
The other thing is, so the block template is transparent.
At most pools right now, because they have this FPPS model, where hashers are basically just selling their hash power to a mining pool and the mining pool just makes a block with it.
Now on Ocean, it's completely transparent what the block will actually look like that everyone is working on, right?

Sjors Provoost: 00:13:09

I don't know how inherent this limitation is in normal pools.
I do know that Stratum V2 doesn't have this problem.
In Stratum V2 you know exactly what you're mining.

But in this case, Ocean Pool will show you what you're mining without even using Stratum V2.
Typically, you don't know what you're mining.
You just get a hash.
And you're grinding away on that hash.
At least you can go to an API and check.
This could be interesting, especially for bigger miners.
Because bigger miners are paid directly from the coinbase.
They can see that they're mining a block that pays them.
They know for sure.
Smaller miners, with the CTV technique, they might also be able to check this.
Probably not in real time, right?
Because you don't want to spend 10 seconds calculating if you're mining the correct block.
You just want to start mining.
But you can at least, within a few seconds, say, hey, I'm being scammed.
I'm going to stop mining now.
So that's quite nice.

For tiny miners that have to be paid through lightning, I don't think this offers any benefit.
In terms of knowing that you're going to be paid.
But you still know what you're mining.
You might realize that you're censoring certain stuff that you're not happy with, et cetera.
So that's good.

Aaron van Wirdum: 00:14:18

The counter, or one of the examples that Bitcoin Mechanic brings up, is there've been pools that have mined blocks that are basically one big inscription or have big inscriptions in them.
And hashers had no idea that that's what they were doing.
Maybe they also don't care that that's what they're doing, but maybe they do care.
In any case, with Ocean, hashers will actually know what they're doing.

Sjors Provoost: 00:14:41

Yeah, but also with Stratum V2, I believe they'll know.

Aaron van Wirdum: 00:14:45

About Stratum V2, we already made an episode about that.
And I also already mentioned that.
It does seem like that sort of on the roadmap for Ocean, but they don't,

Sjors Provoost: 00:14:56

I'm sure it is, but I'm always skeptical of roadmaps, right?
Show it to me.

Aaron van Wirdum: 00:15:00

They don't have it now yet in any case.

Sjors Provoost: 00:15:03

I'm sure they will, but they don't have it yet.

## Regarding Shares, Payouts for Hashers, and How Hashers Prove They’re Doing Work

Aaron van Wirdum: 00:15:07

And then we get to possibly the most complex topic of all of them.
Yesterday we had a preparation call with Bitcoin Mechanic, and with the CTO of the pool, Jason Hughes.
It was one of these calls where I was on it, and Sjors was going on adventure with the CTO.
And I couldn't really keep up with everything you were discussing.
Let's see what you've figured out.

Sjors Provoost: 00:15:38

In case people think that I confidently understand stuff spontaneously, no.
That takes a lot of effort.

Aaron van Wirdum: 00:15:45

I'm barely even sure how to introduce this.

Sjors Provoost: 00:15:50

I think we should generally talk about shares.
Without any of the crazy mechanics that are being used.
The idea is if you are mining, you need to prove to the pool that you are actually doing some work.

Aaron van Wirdum: 00:16:03

Yeah, how does the pool decide which hashers get how much bitcoin?

Sjors Provoost: 00:16:07

I think we discussed this also in the Stratum V2 episode, so you could re-listen to that.
The general idea is that you will mine a block with a much, much, much lower difficulty.
For example, the block that you're trying to mine, the pool wants to see it if it is like a thousand times easier than the real block.

Aaron van Wirdum: 00:16:25

Yeah, you're basically mining invalid blocks.

Sjors Provoost: 00:16:28

Yeah, but they're not randomly invalid.
They are as if the proof of work difficulty was still at the level it was when Satoshi started, basically.
The nice thing is that when you do that, you cannot lie about it.
You are providing proof of work, just a little bit less proof of work.
Because you're only sharing it with the pool operator and not the whole internet.
So, it's fine to have a little bit more spam.
Generally, they'll aim to have 8 blocks per minute.

Aaron van Wirdum: 00:16:58

You're basically proving to the pool that you're at least trying to find the block.

Sjors Provoost: 00:17:02

Exactly.
And then occasionally you will find a block.

Aaron van Wirdum: 00:17:05

Right.
Ocean has this way, it's called tides.
So how do you decide which hasher gets how much bitcoin?

Sjors Provoost: 00:17:16

That is the hard question.
I think we'll also get a little bit into how other pools do that.
But I actually don't really understand how other pools do it.
I think I do understand how this pool does it.
Cause it's a fairly elegant and simple system.

Aaron van Wirdum: 00:17:29

Well, I think how other pools do it, is that's the FPPS system.
A pool just says, we'll pay you X amount of bitcoin for X amount of hashes, and that's just it.

Sjors Provoost: 00:17:42

Yeah, but there's a little nuance of how much X is.

Aaron van Wirdum: 00:17:46

How X is calculated, you mean?

Sjors Provoost: 00:17:48

Yeah.
So let's try and explain this.

Aaron van Wirdum: 00:17:50

I've never really looked into that.
Let's skip that.
That's the easiest thing to do here.
Let's get into how Ocean actually does it.

Sjors Provoost: 00:17:57

Right.
That was, that was sort of the idea.
The idea is that there is a queue.
And you are adding little loads of work, little shares of work into a queue.
Let's say the two of us are mining, I've got my little vintage S9 that I've clocked down to 1 terahash, so that it uses less power and makes less noise.
And it can sit here in my living room basically without driving me nuts.
And you have the same.
So we're each hashing away.

Aaron van Wirdum: 00:18:32

It just not clocked down.
And it's driving me crazy because I don't know how to do that.
Go on.

Sjors Provoost: 00:18:38

Anyway, so both of us are mining.
And what we do is we're proving to the pool that we're doing this amount of work.
So the pool is keeping track of that.
You're submitting a share.
I'm submitting a share.
You're submitting a share.
I'm submitting a share.
And over time this builds up.
Eventually a block is found.
And then in the simplest case, we've both submitted the same number of shares.
And the shares are adjusted for how strong our miners are.
But in this case we assume the miners are equally strong.
The block arrives, half the coinbase transaction output goes to me, half the coinbase output transaction goes to you.
This is very simple.
So this bucket of shares does not fill up to infinity.
If we do this for a few years, the division of who gets how much does not depend on the total amount of shares we submitted throughout history.
But it only depends on the recent past.
It's kind of like a rolling window.

Aaron van Wirdum: 00:19:42

How recent?

Sjors Provoost: 00:19:43

This is where it gets a little more complicated.
The equivalent of 8 blocks of work for the whole network.
The number of shares it would take statistically to produce 8 blocks.
With my miner that would be, I don't know, two million years worth of blocks or something.
Or two million years worth of mining, and for you the same thing.
As soon as the mining pool has more shares than that, it starts discarding old shares.
Or at least it starts ignoring them.
In practice, let's take another example where we actually have two really fast miners.
In fact, our miners are as fast as the whole bitcoin network.
Somehow, we've turned off all the other miners in the network.
The Ocean pool is now the only pool.
And we are continuing with the bitcoin network at the same hash power.
So just to keep the analogy a bit simple here.
Sorry, our miners are a little bit different.
My miner is as strong as the entire bitcoin network is, and your miner is as strong as the entire bitcoin network is.
I'm going to turn it on, you're not.
And then at the end, you're going to turn it on, and I'm going to turn it off.
Because then the question is, how much do we get?
Let's take the simplest possible example.
For 40 minutes, I turn it on.
And then for 40 minutes you turn it on.
And by just complete coincidence, blocks are found exactly every 10 minutes.
Then the question is what happens?

Initially, I get everything for the first block, second block, third block, fourth block.
Because I was the only one mining.
And I'm the only one in the history, ignoring that there's a further past.
Now, you turn on your miner and I've turned off mine.
So what happens in the next block?
Well, it's looking back at the equivalent of 8 blocks, which is more than so far what we've collected.
So, you are going to get one fifth and I'm going to get four fifth of the next block.

Aaron van Wirdum: 00:22:02

That sounds very unfair.

Sjors Provoost: 00:22:04

It doesn't.
Because if we look at that history for the last 8 blocks, you have done one fifth of the work.
And I've done four fifth of the work.

Aaron van Wirdum: 00:22:12

Yes, and I'm not getting one fifth of the bitcoin.

Sjors Provoost: 00:22:15

You are getting one fifth of bitcoin.

Aaron van Wirdum: 00:22:17

Not of all bitcoins that have been issued so far.

Sjors Provoost: 00:22:19

No, you're getting one fifth of the next block.
Yeah, it's always what you get in the next block.
Now the block after that…

Aaron van Wirdum: 00:22:25

It feels like I'm being scammed here, Sjors.

Sjors Provoost: 00:22:27

I don't think so.
The next block, you're getting two sixth of it.
Then the next block, you're getting three seventh of it.
And then the next block you're getting half of it, 4 out of 8, because now you have done half the work in the past 8 blocks.

Aaron van Wirdum: 00:22:42

I'm still being scammed.
You got all the bitcoins of the first 4 and you still get part of the bitcoins of the last 4.

Sjors Provoost: 00:22:50

It sounds pretty evil, doesn't it?
But now, we continue in time and you keep hashing and I don't.
And it goes up, you get five eighth, six eighth, seven eighths, eight eighths.
You get all of it.

Aaron van Wirdum: 00:23:02

Yeah, but now I still did two thirds of the workshop.
And I didn't get two thirds of the bitcoin.
I do think probably if you keep the logic going long enough, then it will probably work out.
But so far, I'm still being scammed here.

Sjors Provoost: 00:23:16

I don't think you're getting scammed.
But it is true that it's a bit hard to reason about it.

Because one of the problems is, if you stop and there's no other miner, then you get nothing.
But if I then take over, you will continue to get rewards for the next 8 blocks or so.
It'll decrease as your work goes back into the past.
So, I think it works out.

Aaron van Wirdum: 00:23:40

Wasn't there a thing where the actual first 8 blocks, including the actual first 8 blocks that Ocean is mining, the logic is a bit different.
So aren't you now explaining the logic that will work fine later on, but not for the first 8?

Sjors Provoost: 00:24:01

No, I think it was fine for the first 8 too.
Because we are simply splitting the work between us in that case.

Aaron van Wirdum: 00:24:10

No, but we just established that I got scammed.

Sjors Provoost: 00:24:15

I don't think you got scammed, I think you're just bad at math.
But I don't know for sure either.

Aaron van Wirdum: 00:24:21

Surely I'm not bad at math.

Like in your example, you mined the first 4, and I mined the last 8.
And we're still splitting the total coins 50-50.

Sjors Provoost: 00:24:31

You've mined the last 8, but you still will get rewards in the future.
So you haven't had it yet, but you will get it.
But somebody has to do the mining.
The question then is when, when is that game done?
Well, if I then take over, you will get the part that you still owed.

Aaron van Wirdum: 00:24:47

Right.
Okay, now that actually makes sense.
For the record, I am bad at math.

Sjors Provoost: 00:24:52

So am I.

Aaron van Wirdum: 00:24:53

But in this case, I was still kind of right.
You're right that if you keep it going, then yes.

Sjors Provoost: 00:24:57

So now let’s take a slightly different experiment.
Because in reality, blocks do not arrive every 10 minutes.
So the question then is, what if blocks arrive really quickly and then it takes a really long time?
How does that division work?
It's not that the rewards are equally divided between the actual blocks.
It's based on the effort you're putting into the system.

An example that I just wrote down this afternoon would be this: We are the entire pool.
I mine 7 blocks, 1 every minute.
And then I stop, and you start mining.
Only after two hours you find block number 8.

Aaron van Wirdum: 00:25:44

That's just because of bad luck in your example, right?

Sjors Provoost: 00:25:48

Yes.

Aaron van Wirdum: 00:25:49

It's not lower hash power on my end, it's bad luck.

Sjors Provoost: 00:25:51

It's just bad luck.
And in this scenario, I got lucky.
Well, this is kind of the bootstrapping problem, but if we kind of ignore that…

I get lucky.
The first 7 times I get a hundred percent of the work, of the coins.
Even though I only mine for 7 minutes.
That's just because of the luck.

But you have mining 1 hour and 53 minutes.
And you find a block.

How much do you get, and how much do I get?

Aaron van Wirdum: 00:26:26

Judging by your logic so far, I'm going to be scammed somehow, so tell me.

Sjors Provoost: 00:26:31

No, you get a hundred percent.

Aaron van Wirdum: 00:26:33

Of what?

Sjors Provoost: 00:26:34

Of the reward in that eighth block.

Aaron van Wirdum: 00:26:38

Because statistically there's been 8 blocks on the network, even though there haven't, right?

Sjors Provoost: 00:26:44

Yeah.
The accounting system is checking how much work you submitted.
And you have submitted more than 8 blocks’ worth of work now because it's two hours.
Normally, you'd expect 12 blocks in that time period.
You have submitted 8 blocks’, roughly worth of equivalent worth of work.
Therefore, all the old stuff that I submitted no longer counts for the accounting.
You get all of it.
You still got unlucky, but in a way it's fair.
Well, that depends on your definition of fair.
This is to make the distinction between, it's not actually 8 blocks.
It's not the last 8 blocks.
It's about the equivalent amount of work that went into the pool.

Aaron van Wirdum: 00:27:23

Yes.
And that's calculated just based on the difficulty.

Sjors Provoost: 00:27:27

Yes, exactly.
That's based on the current difficulty.
It gets a bit more complicated if the difficulty goes up or down.
But every two weeks, you know, the difficulty is constant and then it changes once.
As long as you don't go over that boundary, the math is pretty simple.
But this is also one reason why old shares are not thrown away.
Because you could be in a situation where the difficulty goes up.
And now the equivalent of 8 days is more than it was before.
So, you need to go back in time and look into the log of the people that were doing something a little bit before the window.
Let's say the difficulty doubles overnight.
Now you're looking at the equivalent of 8 days.
Which in reality would have been 16 days of actual work, if you're looking at the past.
You cannot throw away the past.
Or at least, you know, not unreasonably.

Aaron van Wirdum: 00:28:22

All right.
Well, I'm glad you sort of understand this part of the Ocean Pool.
Did we cover this part sufficiently, you think?

Sjors Provoost: 00:28:30

I think so.

Aaron van Wirdum: 00:28:31

Okay, good.

Sjors Provoost: 00:28:33

The funny thing is we did not cover a number of topics that are quite popular when talking about mining pools.

We did not talk about pool hopping.
We did not talk about PPS and FPPS and all these different rewards systems.

Aaron van Wirdum: 00:28:46

I did, a little bit.

Sjors Provoost: 00:28:47

But not in much detail.
Partially is because I don't fully understand those systems.
But partially is because, we already explained this system and you guys are getting tired and our editors is getting tired.
So we might actually come back to it some other time.

## Ocean Pool, Filtering, and Profitability

Aaron van Wirdum: 00:29:04

Yeah.
Maybe that's an episode on its own.
Let's stick to Ocean for now.
There's one other aspect about it that's kind of controversial, which is that they're filtering for quote unquote spam.
They're filtering transactions that they consider to be spam.

Sjors Provoost: 00:29:26

To be precise, they are using Bitcoin Knot’s default settings.
That's an alternative version of bitcoin Core by Luke Dashjr.
It does not relay transactions with an `OP_RETURN` of more than 20 bytes, I believe.
So that's less than the default in Bitcoin Core.
Because it doesn't relay them, it doesn't have it in its mempool.
So, when it generates a block template, these things are not in there.
It also does not have a transaction accelerator.
So, in general, these big ordinal transactions are not in there.
There's three things.
Normal pools, they don't filter out stuff mostly.
With one exception that we talked about last episode.
But they also don't include very large things.
They don't include transactions over, I think it's 400 kilobyte.
But this pool doesn't put anything in there with `OP_RETURN` of more than 20 bytes.

Aaron van Wirdum: 00:30:25

I guess the problem, or the critique, or the controversy is that this would potentially make the pool less profitable.
Because if there's a transaction that pays a high fee, but has a too big of an `OP_RETURN`, then Ocean Pool is not going to include it while another pool might.

Sjors Provoost: 00:30:51

Yeah, but the most fair comparison would be another equivalent of Ocean Pool, Ocean 2 Pool, which would include those transactions.
Then, I think it's fairly straightforward that the other pool would just make more money.

Aaron van Wirdum: 00:31:03

Let's break it down a little bit.
Because I did discuss this with Bitcoin Mechanic and also Jason, the CTO.
They will argue that this is not necessarily true because like you said, it's kind of an unfair comparison if you compare it to other mining pools.

Sjors Provoost: 00:31:25

I think if you compare it to an Ocean 2 Pool, it's very clear.
It's better to include more.

But if you compare it to actual other pools, it's a different story.

Aaron van Wirdum: 00:31:33

Right, exactly.
And the reason for that is that Ocean does have other benefits that other pools don't have, including profitability benefits.

One obvious example is some of the pools have… Once in a while there's this thing in the news that someone accidentally paid a hundred bitcoin fee or something like that.

Sjors Provoost: 00:31:53

That seems to be a trend.

Aaron van Wirdum: 00:31:54

The mining pool will pay it back.
Just because they're being nice to whoever accidentally included that high fee.

Sjors Provoost: 00:32:02

They may be nice, or they may not want to get sued.
Some combination of both.

Aaron van Wirdum: 00:32:06

In either case, Ocean will not do that because they essentially cannot or well…

Sjors Provoost: 00:32:12

They can…

Aaron van Wirdum: 00:32:13

But they cannot.
Because the hashers are directly paid from the coinbase.
Now the hashers themselves have to decide if they want to give it back or not.

Sjors Provoost: 00:32:20

It depends on how quickly they figure out it's an accident.
If they figure it out while it's in the mempool, they could theoretically not mine it.
That would be the easiest thing.

Or they could mine it and then not include it in the rewards for those people.
That would obviously require some serious intervention and some very quick intervention.
Now the miners...

Aaron van Wirdum: 00:32:44

Now they're not doing it.

Sjors Provoost: 00:32:45

No. And the miners that they pay out after 100 blocks, they have 100 blocks to think about it.
But then you would be treating the first 20 miners different from the rest.
It's certainly a lot less easy for them to decide that on behalf of the individual miners.

Aaron van Wirdum: 00:33:03

Yeah.
Another argument would be that FPPS, which I mentioned, which most pools use, which is that the mining pool basically just pays you for your hash power, is essentially undervalued.
One of the reasons for that is that is that miners will collect out of band payments.
Wait, I don't know if it makes sense what I just said.

Sjors Provoost: 00:33:23

The problem is more about transparency.
If we very briefly explain FPPS.
It is basically saying that you get paid for the hash power that you're putting into it.
But how much sats should you be paid for your hash power?
That calculation is based on the block reward plus the expected fees or the average fees over time or some whatever complicated algorithm.
It's not that trivial to compare.
When such a pool processes payments out of bound, like an accelerator, they may or may not pay their miners for that.
It's non-trivial to figure out if that's happening or not.
Whereas in this pool example, it's very clear when it's not happening.

Aaron van Wirdum: 00:34:05

Right.
In either case, I think we both sort of agree that if there was an Ocean 2 Pool, that just does everything exactly the same as Ocean.
And somehow they also have the same size, and same hash power, the same variance, the same luck.
And Ocean does not include these transactions while Ocean 2 Pool would, then Ocean 2 Pool would at least be as profitable and usually more profitable.

Sjors Provoost: 00:34:31

Yes, and Ocean 2Pool could also have an out-of-band transaction accelerator and not pay the individual miners.
However, it would be kind of obvious that their transaction is being included at an implausibly low fee.
So as a miner, you would definitely notice that.
And you'd say, “Hey, I am definitely not getting sats for that.
Because I can see exactly how many sats I am getting from these transactions.
Somebody is getting the sats and it's not me.
Therefore, maybe I'll switch to another pool.”

Aaron van Wirdum: 00:35:01

Just to point this out, Jason and Mechanic also disagree with it.
Or at least they weren't necessarily agreeing.
They seem to be disagreeing.
Their argument was that there could be more complex things going on.
Like child-pays-for-parent type of stuff, that Ocean 2 Pool would not see, and Ocean Pool would actually include.
And therefore, they would still be more profitable.

Sjors Provoost: 00:35:30

The way you're describing that to me makes no sense.
But that is because it's like a Chinese whispers game.

Aaron van Wirdum: 00:35:35

Right.
I'm trying to convey someone else's argument here.
Which I'm not very convinced by.
I am trying my best.

In the case anyone is wondering, the reason we don't have them on the podcast is because we just want to do our podcast in person, not over calls, or internet, or Zoom, or whatever else is available.

Sjors Provoost: 00:35:59

Which is also the reason why we didn't do a lot of episodes in the last couple of months.
But we are back in this very cold country.
And I guess that's all?

Aaron van Wirdum: 00:36:07

I think so, Sjors.

Sjors Provoost: 00:36:08

All right then, thank you for listening to Bitcoin Explained.
