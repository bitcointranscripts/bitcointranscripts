---
title: "Ocean Tides"
transcript_by: kouloumos via tstbtc v1.0.0 --needs-review
media: https://bitcoinexplainedpodcast.com/@nado/episodes/episode-86-ocean-tides-hktbg
tags: []
speakers: ['Sjors Provoost', 'Aaron van Wirdum']
categories: []
date: 2023-12-06
---
Speaker 0: 00:00:21

Live from Utrecht, this is Bitcoin Explained.
Hey Sjoerds.
Hello.
Sjoerds, we have a sponsor.

Speaker 1: 00:00:28

That is correct.
We have a new sponsor.

Speaker 0: 00:00:30

Isn't that great?

Speaker 1: 00:00:31

That's right.
Our new sponsor is Coinkind, the company behind the cold card.
And dear listener, if you have no idea what a cold card is, please let us know because then we'll explain it because otherwise it's a bit ridiculous if we explain it because we I think we we think you all know.

Speaker 0: 00:00:48

Oh my God, this is the worst ad read in history, Sjoerds.
Excellent.
Can we at least mention it's a hardware wallet?

Speaker 1: 00:00:56

Yes, it's a hardware wallet.

Speaker 0: 00:00:57

It's a hardware wallet you can use to store Bitcoin.
All right.
Sjoerds, today we're going to discuss a new mining pool launched.
Well, kind of.
Ocean Pool.
I was invited to the launch event.
It was sort of a mini conference.

Speaker 1: 00:01:15

I felt a very strong FOMO for that one.
I saw the video, you guys were in the middle of nowhere and some like, like video, like some horror movie video shoot game basically scene.

Speaker 0: 00:01:26

Right.
Yeah.
Well, it was quite nice actually.
There was like this hydro plant, a very, what's a good English word for this?
Rustic?
I don't know if that's the right word.

Speaker 1: 00:01:35

Maybe, but

Speaker 0: 00:01:36

it was nice.
Let's just say it was nice, nice environment.
And yeah, they launched this pool.
So it's really the relaunch or re-brand or re something of Elytius.
If that's how I pronounce that pool, the Luke Dasher pool.
This time it's backed by Jack Dorsey, my other investors.
And their goal, their intention is to re-decentralize mining essentially, or decentralized mining.

Speaker 1: 00:02:04

Right.
And they're calling it Ocean.

Speaker 0: 00:02:07

Yeah.
Didn't I mention that?
No. Okay.
Yes.
Ocean, ocean pool.
Yeah, so decentralizing mining pools or at least this one or mining in general, ultimately is the goal.
The sort of most notable innovation that they started with, that they launched with, is they have this non-custodial setup.
Kinda.
Or I mean, that's the goal, that's the intention.

Speaker 1: 00:02:34

I guess one diplomatic way to call it would be custody minimized.
I mean, you can have long legal discussion about what custody means, but I think we care most about the technical sides of it.
And then you can ask practical questions like could the mining pool steal your money?
Could the big forces steal your money?
Etc.
And we can try to get into some of the nuance there of what they're actually doing.

Speaker 0: 00:02:57

So to clarify this, what mining pools usually do is, well I don't want to get into the whole thing, but basically when a mining pool finds new coins, the mining pool gets these coins.
And in fact, these coins can't be spent for a hundred blocks, right?
Yeah.
And then after these a hundred blocks, well, that's actually not what happens with most pools.
I was, I w I was going to say after a hundred blocks, these coins are distributed to the miners, but that's not actually how money pools work.

Speaker 1: 00:03:28

I would say there's a bigger separation there, right?
The mining pool as a whole has a wallet and the coins they earn go into that wallet and the miners are paid from that wallet but it is a bit of an omnibus and not necessarily trivial to understand which mindset belongs to which specific individual miner.

Speaker 0: 00:03:46

Yeah a way that they will explain it or Bitcoin Mechanic, for example, is essentially most Bitcoin miners or hashers, as we've also called it, aren't actually mining Bitcoin.
They're just selling their hash power to a mining pool, basically.
And the pool operator is the one that's actually...

Speaker 1: 00:04:03

Well, that sounds a little bit like a separate issue, though it's a bit related to whether you know you're really...
What it is that you're doing as a miner.
Are you producing blocks or are you just delivering hash rate to a buyer?
And that depends on the incentive model, the exact business model.
I think we'll get into that a bit later, but the idea of holding coins custody, you know, you could, you could do that with this model too, I think you just don't have to.

Speaker 0: 00:04:30

Right.
Yeah.
It is a slightly separate issue.
I just wanted to point it out real quick, but yes.
Yeah.
So the main innovation here is essentially that hashers as well.
They'll call them.
So to clarify that there's the mining pool or the mining pool operator, that's, you know, doing most of the Bitcoin stuff, you know, downloading blockchain and constructing the blockchain template, which is a big part of it, which might not happen in the future with Stratum V2, but we've made another episode about that, at least right now, most mining pools still create block templates or which transactions go into a block.
And I lost my train of thought, but I think I was going to say with Ocean, the new coins are directly paid to the hashers.
Oh, I was still explaining.

Speaker 1: 00:05:16

So the coin-based transaction, which is what every new block contains, has a number of outputs and typically these just go to the general wallet of the pool.
But with this new Ocean Pool, as much as possible, the coin-based transactions go directly to the miners.
Right.
With the caveat that you cannot do that for all mine transactions.
Not for all miners.
And there are two

Speaker 0: 00:05:41

reasons for that.
Okay, so let's get into that.
First let's point out some advantages of this.
And the biggest one is probably, so right now, if you're a hasher and you want to join a pool, most pools have sort of KYC stuff going on, like you need to actually tell the pool who you are, at least some of the big ones have this.
And Ocean does not have this.

Speaker 1: 00:06:00

Yeah, but I don't think that's inherent to this model at all.
Like you could still have KYC in this model or not.

Speaker 0: 00:06:07

Yeah, so well, I mean, I guess in their view or what they will argue or what they think or what they believe is that they, that it's sort of a, this way it's legally possible to not do KYC.

Speaker 1: 00:06:18

Well, we're not lawyers.
We're, I'm a developer, you're a journalist, but let's,

Speaker 0: 00:06:23

but in any case, they aren't doing KYC stuff.
That's for sure.
Right

Speaker 1: 00:06:26

now, you can just plug

Speaker 0: 00:06:27

in and start mining.

Speaker 1: 00:06:28

One thing that they're doing very practically is that you as a miner don't create an account or you don't have to.
You just provide a Bitcoin address straight as you're directly from the miner.

Speaker 0: 00:06:40

Right.
Okay.
So you mentioned, so you, So you get paid directly from the Coinbase as a hasher to the extent that it is possible.

Speaker 1: 00:06:52

Yeah, and that extent is quite limited because of two reasons.
One is a Coinbase transaction can only have this many outputs.
Or even if you could have as many as you want, at some point it's just not worth paying the fees.
Or not so much paying the fees because the Coinbase transaction doesn't pay fees, but you are forgoing, you know, you're using up space that others could pay, that other people are paying you fees as a pool.

Speaker 0: 00:07:17

So if

Speaker 1: 00:07:17

you make a one megabyte Coinbase transaction, then you can do that and you pay zero fees for it, but you are now no longer mining anything.

Speaker 0: 00:07:25

Right, well, you could create a four megabyte Coinbase transaction.

Speaker 1: 00:07:28

I don't think so because there's no witness.

Speaker 0: 00:07:30

Maybe two.
Oh, Oh, right.
Okay, let's separate these issues.
So first of all, you said you can't necessarily pay every hasher because the number of outputs in the Coinbase transaction is limited?

Speaker 1: 00:07:42

Or at least, I don't know if there's an actual limit there that matters, but basically it's just not worth the opportunity cost of making very small payments in the Coinbase.
But there is a second...

Speaker 0: 00:07:52

So it's the same issue.
There is no actual limit to the number of outputs in the Coinbase transaction.

Speaker 1: 00:07:56

I think it's just a regular transaction, whatever that limit is.
It might not be one.
Okay.

Speaker 0: 00:08:01

I

Speaker 1: 00:08:01

should know that, I guess.
So the second limit, the second limit is a little bit more mundane.
Apparently some of the mining hardware out there starts to panic if you put more than 20 outputs in a coin based transaction.
So that has nothing to do with the Bitcoin limits.
It's just that some mining equipment just panics when there's too many outputs.
So in practice, the limit is about 20.
So the 20, and in this case, the top 20 miners get paid directly from the Coinbase.
Then there's some amount left and that essentially goes to a wallet you could say, but they make sure that from that wallet after a hundred blocks, because then you can spend it, it immediately goes to the correct miners as if they were part of the Coinbase essentially.

Speaker 0: 00:08:49

Right.
Okay.
So we just, so I thought wrongly probably that there was a limit on the number of transactions on the Coinbase output.
And you just said, That's probably not the case, but there some hardware has this issue.
That's, that's where the limit comes from.
Yeah.
Okay.
And you say that limit is 20.
I apparently roughly 20.
20 ish.
Okay.
There can only be 20 transaction outputs from a Coinbase transaction.

Speaker 1: 00:09:16

So, So that secondary transaction, which can only happen after a hundred blocks, because the Coinbase maturity rule, that's a consensus rule.
That transaction is kind of just like it was part of the Coinbase itself, right?
It also has the same fee trade-offs here where yes, you can put whatever giant transaction you want in there as a pool, but then you're foregoing fee revenue from other transactions.
This transaction just spends from the Coinbase.

Speaker 0: 00:09:40

Okay.
So if there's just too many hashers that need to be paid from the Coinbase, if it's more than 20 essentially, then some of them will be paid later, still as soon as possible, but later.
And then the other thing was, if you mine, if you're a hasher and you don't earn enough from a block, then you'll only, also won't get paid immediately.

Speaker 1: 00:10:03

Right, So then the idea is to basically wait until you, until you've accumulated enough credit as it were, and then you get paid.
So there, it really starts looking like just a wallet that's custodial, but only for small amounts.

Speaker 0: 00:10:18

Sjoerd Right.
Okay.
So that's how it works today.
And then there are some ideas in the future, for the future to improve that a little bit more.
So one of them is using Lightning for payouts.

Speaker 1: 00:10:32

Arno Yeah, that kind of makes intuitive sense.
When you have very small miners that want to collect small rewards, maybe they get like 20 Satoshis every block.
Lightning is a way to do that.
Then the question is, can you, you know, how non-custodial can you make lightning?
I believe if you listen to the Stefan Levera podcast, Bitcoin Mechanic explains some ideas of how to do that roughly, using, I believe, some sort of market where, like, if you have, if you have lightning liquidity, you essentially buy the rights to the payouts from the pool.
So the pool is not doing the lightning payouts.
They're just, they're just giving payouts to addresses, but then you, somebody else does some swapping of who gets which points.

Speaker 0: 00:11:15

Right.
And then there's another potentially cool idea, which is not possible yet on the Bitcoin network, but with check template verify, it could actually be implemented that if this 20 limit threshold in the Coinbase is reached, then the other hashers are still guaranteed their payment through a CTV transaction because of that.

Speaker 1: 00:11:39

Yeah, and even better than that, regardless of this 20 limit, right now, if you're putting something, you have to put the addresses in the Coinbase right now.
And so you kind of don't want to do that when fees are really high because that's an opportunity cost.
But maybe you want to pay people when fees are low.
So CTV is quite interesting for that.
We have not really discussed that in any podcast, but it's basically a software proposal that commits to certain transactions happening in the future.
And one of the intended use cases is congestion control.
And this would be a very nice use case for it, where the Coinbase only has one output, or maybe a couple, which is the CTV transaction.
And then all the miners know for sure that they will get those coins, but they'll wait until fees are low and then they'll get them.

Speaker 0: 00:12:26

Right.
All right.
That was the non-custodial part of the pool, which is probably kind of the main innovation, but it's not the only thing going on.

Speaker 1: 00:12:36

Yeah.
Or the custody minimized part of the pool.
Right.

Speaker 0: 00:12:38

Right.
I'm sorry, Sjoerd.
You're very right.
The other thing is, so the block template is transparent.
So usually at most pools right now, because they have this FPPS model, which I briefly mentioned earlier, where hashers are basically just selling their hash power to a mining pool and the mining pool just makes a block with it.
Now on Ocean it's completely transparent what the block will actually look like that everyone is working on, right?

Speaker 1: 00:13:09

Yeah, so I don't know how inherent this limitation is in normal pools.
I do know that Stratum V2 doesn't have this problem.
In Stratum V2 you know exactly what you're mining, but in this case OceanPool will show you what you're mining without even using Stratum V2.
And typically you don't know what you're mining, you just get a hash and you're grinding away on that hash.
Now you can go to, at least you can go to an API and check.
And this could be interesting, especially for bigger miners because bigger miners they're paid directly from the Coinbase.
So they can see that they're mining a block that pays them.
Like they know for sure.
Smaller miners Again, with the CTV technique, they might also be able to check this.
Probably not in real time, right?
Because you don't want to spend 10 seconds calculating if you're mining the correct block.
You just want to start mining.
But you can at least, within a few seconds, say, hey, I'm being scammed.
I'm going to stop mining now.
So that's quite nice.
For tiny miners that have to be paid through Lightning.
I don't think this offers any benefit in terms of knowing that you're going to be paid, but you still know what you're mining.
You might realize that you're censoring certain stuff that you're not happy with, et cetera.
So that's good.

Speaker 0: 00:14:18

Yeah.
The counter or one of the examples that, you know, Bitcoin mechanic, for example, bring up is that, there've been pools that have minds blocks that are basically one big inscription or have big inscriptions in them.
And hashers had no idea that that's what they were doing.
Now, maybe they also don't care that that's what they're doing, but maybe they do care.
In any case, with Ocean, hashrers will actually know what they're doing.

Speaker 1: 00:14:41

Yeah, but also with Stratum V2, I believe they'll know.

Speaker 0: 00:14:45

So, yeah, about Stratum V2, we already made an episode about that and I also already mentioned that, but, it does seem like that sort of on the roadmap for ocean, but they don't,

Speaker 1: 00:14:56

I'm sure it is, but I'm always skeptical of roadmaps, right?

Speaker 0: 00:14:59

Right.

Speaker 1: 00:14:59

Show it to me.

Speaker 0: 00:15:00

Yeah.
They don't have it now yet in any case.

Speaker 1: 00:15:03

I'm sure they will, but they don't have it yet.

Speaker 0: 00:15:07

All right.
And then we get to possibly the most complex topic of, of all of them.
Yesterday we had a sort of preparation call with also with Bethke mechanic and with the CTO of the pool, Jason Hughes.
And it was one of these calls where I was on it and Shorts was just sort of Going on adventure with the CTO and I couldn't really keep up with everything you were discussing.
So let's see what you've figured out.

Speaker 1: 00:15:38

Yeah.
So in case people think that I confidently understand stuff spontaneously, no, that takes a lot of effort.
Right.

Speaker 0: 00:15:45

Okay.
So I'm barely even sure how to introduce this.

Speaker 1: 00:15:50

Well, I think we should generally talk about shares a little bit without any of the crazy mechanics that are being used generally.
But the idea is if you are mining, you need to prove to the pool that you are actually doing some work.

Speaker 0: 00:16:03

Yeah, how does the pool decide which hashers get how much Bitcoin?

Speaker 1: 00:16:07

And I think we discussed this also in the Stratum V2 episode, by the way, so you could re-listen to that.
But the general idea is that you will mine a block with a much, much, much lower difficulty.
And for example, the block that you're trying to mine, the pool wants to see it if it is like a thousand times easier than the real block.

Speaker 0: 00:16:25

Yeah, you're basically mining invalid blocks.

Speaker 1: 00:16:28

Yeah, but they're not randomly invalid.
They are like as if the proof of work difficulty was still at the level it was when Satoshi started, basically.
And the nice thing is that when you do that, you cannot lie about it.
You are providing proof of work, just a little bit less proof of work because you're only sharing it with the pool operator and not the whole internet.
Yeah.
So it's fine to have a little bit more spam.
And generally they'll aim to have like eight blocks a second, sorry, eight blocks per minute.
That's, I believe often an interval.

Speaker 0: 00:16:58

You're basically proving to the pool that you're at least trying to find the block.

Speaker 1: 00:17:02

Exactly.
Right.
And then occasionally you will find a block.

Speaker 0: 00:17:05

Right.
Exactly.
And yes.
Okay.
So Ocean has this way, it's called tides.
So how do you decide which hasher gets how much Bitcoin?

Speaker 1: 00:17:16

Yeah, that is the hard question.
And I think we'll also get a little bit into how other pools do that, but I actually don't really understand how other pools do it.
And I think I do understand how this pool does it.
Cause it's, I think it's a fairly elegant and simple system.

Speaker 0: 00:17:29

Well, I think how other pools do it is that's the FPPS system, right?
So basically a pool just says, we'll pay you X amount of Bitcoin for X amount of hashes, and that's just it.

Speaker 1: 00:17:42

Yeah, but there's a little nuance of how much X is.

Speaker 0: 00:17:46

How X is calculated, you mean?

Speaker 1: 00:17:48

Yeah.
So let's

Speaker 0: 00:17:50

try and explain this.

Speaker 1: 00:17:50

I've never really looked into that

Speaker 0: 00:17:51

and let's skip that.
That's the easiest thing to do here.
And let's get into how Ocean actually does it.

Speaker 1: 00:17:57

Right.
That was, that was sort of the idea.
Okay.
So basically the idea is that there is a bucket, or it's not really a bucket, it's a queue.
And you are adding work, little loads of work, little shares of work into a queue.
Let's say the two of us are mining, I've got my little vintage S9 that I've clocked down to 1 terahertz so that a tera hash so that it uses less power and makes less noise and it can sit here in my living room basically without driving me nuts.
And you have the same so we're each hashing away.

Speaker 0: 00:18:32

It just not clocked down and it's driving me crazy because I don't know how to do that.
Oh. Go on.

Speaker 1: 00:18:38

Anyway, so both of us are mining and what we do is to the pool we're proving that we're doing this amount of work.
And so the pool is keeping track of that.
You're submitting a share, I'm submitting a share, you're submitting a share, I'm submitting a share, and over time this builds up.
And eventually a block is found, and then in the simplest case, we've both submitted the same number of shares, and the shares are adjusted for how strong our miners are so but in this case we assume the miners are equally strong.
The block arrives then half the coinbase transaction output goes to me, half the coinbase output transaction goes to you.
This is very simple.
Now, let's, so this bucket of shares does not fill up to infinity.
So if we do this for a few years, then we're not gonna, the division who gets how much is not, does not depend on the total amount of shares we submitted throughout history, but it only depends on the recent past.
It's kind of like a rolling window.

Speaker 0: 00:19:42

How recent?

Speaker 1: 00:19:43

The equivalent, so this is where it gets a little more complicated is the equivalent of eight blocks of work for the whole network.
So the number of hashes, or sorry, the number of shares it would take statistically to produce eight blocks.
You know, with my miner that would be, I don't know, two million years worth of blocks or something.
Or two million years worth of mining, let's say, and for you the same thing.
But as soon as the mining pool has more shares than that, it starts discarding all shares,

Speaker 0: 00:20:15

or

Speaker 1: 00:20:15

at least it starts ignoring them.
So in practice, let's take another example where we actually have two really fast miners.
In fact, our miners are as fast as the whole Bitcoin network.
Somehow we've turned off all the other miners in the network, and so this this Elysium pool, sorry, the Ocean pool is now the only pool and we are continuing with the Bitcoin network at the same hash power.
So just to keep the analogy a bit simple here.

Speaker 0: 00:20:45

Yes, please.

Speaker 1: 00:20:47

Yes, Now in this case, actually, sorry, our miners are a little bit different.
That is my miner is as strong as the entire Bitcoin network is, and your miner is as strong as the entire Bitcoin network is.
I'm going to turn it on, you're not, and then at the end you're going to turn it on and I'm going to turn it off.
Because then the question is, how much do we get?
So let's take the simplest possible example, or about 40 minutes, I turn it on and then for 40 minutes you turn it on and By just complete coincidence Blocks are found exactly every 10 minutes.
Mm-hmm.
So then the question is what happens?
Initially I Turn it on first, right?
So initially I get everything for the first block, second block, third block, fourth block,

Speaker 0: 00:21:37

because I

Speaker 1: 00:21:37

was the only one mining and I'm the only one in the history, ignoring that there's a further past.
Now You turn on your miner and I've turned off mine.
So what happens in the next block?
Well, it's looking back at the equivalent of eight blocks, which is more than so far what we've collected.
And so you are going to get one fifth and I'm going to get four fifth of the next block.
And then...

Speaker 0: 00:22:02

That sounds very unfair.

Speaker 1: 00:22:04

It doesn't because if we look at that history for the last eight blocks, you have done one fifth of the work and I've done four fifth of the work.

Speaker 0: 00:22:12

I'm not getting one fifth of the Bitcoin.

Speaker 1: 00:22:15

You are getting one fifth of Bitcoin.

Speaker 0: 00:22:17

Not of all Bitcoins that have been issued so far.

Speaker 1: 00:22:19

No, you're getting one fifth of the next block.
Yeah, it's always what you get in the next block.

Speaker 0: 00:22:23

Uh-huh.

Speaker 1: 00:22:24

Now the block after that,

Speaker 0: 00:22:25

you're getting...
It feels like I'm being scammed here, Sjoerd.

Speaker 1: 00:22:27

I don't think so.

Speaker 0: 00:22:28

Go on.

Speaker 1: 00:22:28

I think the next block, you're getting two sixth of it.
Then the next block, you're getting three sixth of it.
And then the next, sorry, three seventh of it.
And then the next block you're getting half of it, four out of eight, because now you have done half the work in the past eight blocks.

Speaker 0: 00:22:42

I'm still being scammed.
Like you got all the Bitcoins of the first four and you still get part of the Bitcoins of the last four.
Even though we both,

Speaker 1: 00:22:50

it sounds pretty evil, doesn't it?
But, but now, we continue in time and you keep hashing and I don't.
And it goes up, you get five, eight, six, eight, seven, eight, eight, eight.
You get all of it.

Speaker 0: 00:23:02

Yeah, but now I still did two thirds of the workshops and I didn't get two thirds of the Bitcoin, I think.
Anyways, I, I do think probably if you keep the logic going long enough, then it will probably work out, but so far I'm still being scammed here.

Speaker 1: 00:23:16

I don't think you're getting scammed, but it is true that it's a bit hard to reason about it because one of the problems is if you stop and there's no other miner, then, then you get nothing.
Right.
But if I then take over, you will continue to get rewards for the next eight blocks or so.
It'll decrease as your, your work goes back into the past.
So I think it works out.
But

Speaker 0: 00:23:40

wasn't there a thing, wasn't there a thing that with the first, like the actual first eight blocks, so including the actual first eight blocks that I think Ocean is mining, the logic is a bit different.
So aren't you now explaining the logic that will work fine later on, but not for the first eight?

Speaker 1: 00:24:01

No, I think it was fine for the first 8 too, because we are simply splitting the work between us in that case.

Speaker 0: 00:24:10

No, but we just established that I got scammed.

Speaker 1: 00:24:15

I don't think you got scammed, I think you're just bad at math, but I don't know for sure either.

Speaker 0: 00:24:21

Surely I'm not bad at math.
Like in your example, you mined the first four and I mined the last eight and we're still splitting the coins, the total coins 50-50.

Speaker 1: 00:24:31

So you've mined the last eight, but you still will get rewards in the future, right?
So you haven't

Speaker 0: 00:24:36

had it

Speaker 1: 00:24:37

yet, but you will get it

Speaker 0: 00:24:38

right, right, right, right.

Speaker 1: 00:24:39

But somebody has to do the mining.
So the question then is when, when is that game done?
Well, if I then take over, you will get the part that you still owed.

Speaker 0: 00:24:47

Right, yes.
Okay, now that actually makes sense.
For direct, I am bad at math.
But in this case, I was still kind of right, I think.
But yes, you're right that if you keep it going, then yes.

Speaker 1: 00:24:57

Slightly different experiment, because in reality, blocks do not arrive every 10 minutes.
And so the question then is, well, what if blocks arrive really quickly and then it takes a really long time?
How does that division work?
Right?
It's not that the blocks, that the rewards are equally divided between the actual blocks.
It's based on the effort you're putting into the system.
So an example that I just wrote down this morning or afternoon would be this.
I am mining, I mine seven blocks, again we are the entire pool, I mine seven blocks, one every minute.
And then I stop and you start mining.
And, and only after two hours you find block number eight.

Speaker 0: 00:25:44

Is it, But that's just because of bad luck in your example, right?
Yes.
It's not lower hash power on my end, it's bad luck.

Speaker 1: 00:25:51

It's just bad luck.

Speaker 0: 00:25:52

Yeah, okay.

Speaker 1: 00:25:53

And so in this scenario, I got lucky.
Well, again, this is kind of the bootstrapping problem, but if we kind of ignore that, I get lucky.
The first seven times I get a hundred percent of the work of the coins even though I only mine for seven minutes that's just because of the luck mm-hmm and then but you have been mining now for eight hours or sorry two hours or one hour and 53 minutes whatever you want to say mm-hmm the question then is and you find a block how much do you get and how much do I get?

Speaker 0: 00:26:26

I mean, judging by your logic so far, I'm going to be scammed somehow, so tell me.

Speaker 1: 00:26:31

No, you get a hundred percent.

Speaker 0: 00:26:33

Because of what?

Speaker 1: 00:26:34

Of the reward in that eighth block.
Oh, right.

Speaker 0: 00:26:38

And so this is the, because statistically there's been eight blocks on the network, even though there haven't, right?

Speaker 1: 00:26:44

Yeah.
Or in, You know, the accounting system is checking how much work you submitted and you have submitted more than eight blocks worth of work now because it's two hours.
So that's about, you know, normally you'd expect 12 blocks in that time period.
So you have submitted eight blocks, roughly worth of equivalent worth of work.
And therefore all the old stuff that I submitted no longer counts for the accounting, you get all of it.
You still got unlucky, but in a way it's fair.
Well, that depends on your definition of fair, but yeah.
Yeah.
But this is to make the distinction between, it's not actually eight blocks.
It's not the last eight blocks.
It's about the equivalent amount of work that went into the pool.

Speaker 0: 00:27:23

Yes.
And that's calculated just based on the difficulty.

Speaker 1: 00:27:27

Yes, that is exactly.
That's based on the current difficulty.
So it gets a bit more complicated, I guess, if the difficulty goes up or down.
But every two weeks, you know, the difficulty is constant and then it changes once.
So as long as you don't go over that boundary, the math is pretty simple.
But this is, I believe, also one reason why alt shares are not thrown away.
Because you could be in a situation where the difficulty goes up and now the equivalent of 8 days is more than it was before and so you need to go back in time and look into the log of the people that were doing something a little bit before the window.
Let's say the difficulty doubles, right, overnight.
Now you're looking at the equivalent of eight days, which is in reality would have been 16 days of actual work

Speaker 0: 00:28:16

if

Speaker 1: 00:28:17

you're looking at the past.
So you cannot throw away the past, or at least, you know, not unreasonably.

Speaker 0: 00:28:22

All right.
Well, I'm glad you sort of understand this part of the ocean pool.
Did we cover this part sufficiently, you think?

Speaker 1: 00:28:30

I think so.

Speaker 0: 00:28:31

Okay, good.

Speaker 1: 00:28:33

Yeah, so the funny thing is we did not cover a number of topics that are quite popular when talking about mining pools.
We did not talk about pool hopping.
We did not talk about PPS and FPPS and all these different rewards systems, but not in much detail.
Partially is because I don't fully understand those systems.
But partially is because, you know, we already explained this system and you guys are getting tired and our editors getting tired.
So we might, we might actually come back to it some other time.

Speaker 0: 00:29:04

Right.
Yeah.
Maybe that's an episode on its own, I guess.
Let's stick to Ocean for now.
There's one other aspect about it that's kind of controversial, which is that they're filtering for quote unquote spam.
They're filtering transactions that they consider to be spam.
So the most often...
Yeah, so

Speaker 1: 00:29:26

I believe to be precise, they are using Bitcoin Nod's default settings.
So that's an alternative version of Bitcoin Core by Luke Dasher.
And it does not relay transactions with an operator of more than 20 bytes, I believe.
So that's less than the default in Bitcoin Core.
And because it doesn't relay them, it doesn't have it in its mempool and so when it generates a block template these things are not in there.
It also does not have a transaction accelerator right so so in general these big ordinal transactions are not in there.
The big ones that so I guess there's three things right normal pools don't just they don't filter out stuff mostly with one exception that we talked about last episode.
But they also don't include very large things.
They don't include transactions over, I think it's 400 kilobyte.

Speaker 0: 00:30:20

Right.
So

Speaker 1: 00:30:20

this pool doesn't put anything in there with opportunities more than 20 bytes.

Speaker 0: 00:30:25

Right.
Yeah.
I guess I'm not really sure.
Do you have an opinion on this?
Let's just start there or what would you, I guess the problem or the critique or the controversy or whatever you want to call it, is that this would potentially make the pool less profitable because if there's a transaction that pays a high fee, but has a too big up return, then this pool isn't going to, Ocean pool is not going to include it while another pool might.

Speaker 1: 00:30:51

Yeah, but the most fair comparison would be another equivalent of Ocean pool, Ocean two pool, which would include those transactions.
And then I think it's fairly straightforward that the other pool would just make more money.

Speaker 0: 00:31:03

Yeah, well, let's break it down a little bit.
So because I did discuss this with Bitcoin Mechanic and also Jason, the CTO.
So what they will argue, I just want to mention what they will argue.
So they will argue that this is not necessarily true because there are, yeah.
So like you said, it's kind of an unfair comparison if you compare it to other mining pools.
So it's not necessarily true.

Speaker 1: 00:31:25

I think if you compare it to an ocean two pool, it's very clear.
It's better to include more, But if you compare it to actual other pools, it's a different story.

Speaker 0: 00:31:33

Right, exactly.
And the reason for that is that Ocean does have other benefits that other pools don't have, including profitability benefits.
So, one obvious example is some of the pools have, once in a while there's this thing in the news that someone accidentally paid a hundred Bitcoin fee or something like that.

Speaker 1: 00:31:53

That seems to be a trend.

Speaker 0: 00:31:54

And then the mining pool will pay it back just because they're being nice to whoever accidentally included that high fee.

Speaker 1: 00:32:02

They may be nice, so they may not want to get sued.
Some combination of both.

Speaker 0: 00:32:06

Yeah, in either case, Ocean will not do that because they essentially cannot or well,

Speaker 1: 00:32:12

they can, but they will.

Speaker 0: 00:32:13

They cannot because the hashers are directly paid from the Coinbase, but now the hashers themselves have to decide if they want to give it back or not.

Speaker 1: 00:32:20

Yeah, that's true for the first.
But it depends.
So it depends on how quickly they figure out it's an accident.
If they figure it out while it's in the mempool, they could theoretically not mine it, I guess that would be the easiest thing, Or they could mine it and then not include it in the rewards for those people.
But that would obviously require some serious intervention and some very quick intervention.
Now the miners...

Speaker 0: 00:32:44

Right now they're not doing it.

Speaker 1: 00:32:45

No, and the miners that they pay out after 100 blocks, they have 100 blocks to think about it.
So they could again, you know, but then you would be treating the first 20 miners different from the rest.
So it's certainly a lot less easy for them to decide that on behalf of the individual miners.

Speaker 0: 00:33:03

Yeah.
Another argument would be that FPPS, which I mentioned, which most pool use, which is that the mining pool basically just pays you for a hash power, is essentially undervalued.
And one of the reasons for that is that, miners will collect out of band payments.
Wait, I don't know if it makes sense what I just said.

Speaker 1: 00:33:23

Well, so the problem is more about transparency.
So if we very briefly explain FPP as it is basically saying that you get paid for the hash power that you're putting into it, which is then how much SATs should you be paid for your hash power and that calculation is based on the block reward plus the sort of the expected fees or the average fees over time or some whatever complicated algorithm.
It's not that trivial to compare.
So when a miner receives, when such a pool processes payments out of bound, like an accelerator, they may or may not pay their miners for that.
It's non-trivial to figure out if that's happening or not.
Whereas in this pool example, it's very clear when it's not happening.

Speaker 0: 00:34:05

Right.
In either case, I think we both sort of agree that if there was an Ocean 2 pool that just does everything exactly the same as Ocean and somehow they also have the same size and same hash power, the same variance, the same lock.
And Ocean does not include these transactions while Ocean 2Pool would, then Ocean 2Pool would at least be as profitable and usually more profitable.

Speaker 1: 00:34:31

Yes, and Ocean 2Pool could also have an out-of-band transaction accelerator and not pay the individual miners.
However, it would be kind of obvious that their transaction is being included at a implausibly low fee.
And so as a miner, you would definitely notice that and you'd say, Hey, I am definitely not getting sats for that because I can see exactly how many sats I am getting from these transactions.
So, you know, somebody is getting the sats and it's not me.
Therefore, you know, maybe I'll switch to another pool or yeah.

Speaker 0: 00:35:01

Right.
Yeah, just to point this out, Jason and, Mechanic also disagree with it or this, or at least they weren't necessarily agreeing, they seem to be disagreeing.
They seem to Their argument was that there could be more complex things going on, like child pays for parents type of stuff that Ocean 2 pool would not see an Ocean pool like their pool would actually include.
And therefore they would still be more profitable.

Speaker 1: 00:35:30

The way you're describing that to me makes no sense, but that is because it's like a Chinese whispers game.
So.

Speaker 0: 00:35:35

Yeah, right.
I'm just sort of trying to convey someone else's argument here, which I'm not very convinced by, but you know, I'm, I am trying my best to, in the case anyone is wondering, the reason we don't have them on the podcast is because we just want to do our podcast in person, not over calls or internet or Zoom or whatever else is available.

Speaker 1: 00:35:59

Exactly, Which is also the reason why we didn't do a lot of episodes in the last couple of months.
But we are back in this very cold country.
And I guess that's all?

Speaker 0: 00:36:07

I think so, Sjoerd.

Speaker 1: 00:36:08

All right then, thank you for listening to Bitcoin.
Explain.
