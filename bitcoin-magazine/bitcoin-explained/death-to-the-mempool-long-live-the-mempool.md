---
title: "Death to the Mempool, Long Live The Mempool"
transcript_by: davidgumberg via review.btctranscripts.com
media: https://www.youtube.com/watch?v=SPOESGI4xnw
tags: ["mempool","miners","incentives"]
speakers: ["Sjors Provoost","Aaron van Wirdum"]
categories: ["podcast"]
date: 2021-11-26
---
## Preamble

Aaron van Wirdum: 00:00:20

Live from Utrecht, this is Bitcoin Explained.

Sjors Provoost: 00:00:23

Hello.

Aaron van Wirdum: 00:00:24

Hey Sjors.

Sjors Provoost: 00:00:25

What's up?

Aaron van Wirdum: 00:00:26

I'm doing well.

We're still in Utrecht as I just said, but only for a couple more days, I'm on my way back to El Salvador for a couple of conferences and I think you're gonna be traveling as well.

Sjors Provoost: 00:00:40

Hopefully, if it's warmer.

Aaron van Wirdum: 00:00:43

And if the COVID situation allows it.

Sjors Provoost: 00:00:46

Well, wherever the COVID situation allows it.

Aaron van Wirdum: 00:00:48

So anyways, the reason I mention that is because we're recording this episode ahead of time.

We're recording this episode probably at least two weeks before it's actually published.
And we're going to discuss a thread from the Bitcoin development mailing list that was published a couple weeks ago.

Sjors Provoost: 00:01:11

That's right.

Aaron van Wirdum: 00:01:11

So by the time people are listening to this, they are going to be hearing a discussion on a thread that's at least a month old.

Sjors Provoost: 00:01:18

But it's good.
You need to be reminded occasionally of the things that are important.
And besides, last episode, I think we talked about something from three months ago.

Aaron van Wirdum: 00:01:28

Yeah, if you want fresh content, Bitcoin Explained is not the place for you.
But if you want exciting and interesting content and from the top expert in the space, Sjors Provoost, then Bitcoin Explained is perfect.

Sjors Provoost: 00:01:45

If you want it translated by the top journalist in the space, then Bitcoin Explained is also perfect.

Aaron van Wirdum: 00:01:48

Oh, stop it.

Sjors Provoost: 00:01:50

Okay.

## Intro

Aaron van Wirdum: 00:01:51

All right, enough about that.
Let's get to the point.
We are going to be discussing a thread.
Do you have a name of the thread in front of you?

Sjors Provoost: 00:01:56

That's right. It's called Death to the Mempool, Long Live the Mempool.

Aaron van Wirdum: 00:02:01

It's a proposal to basically abolish the mempool.
Who started the thread?

Sjors Provoost: 00:02:12

niftynei.
She's a C Lightning developer at Blockstream.
Now, we don't really know whether this proposal is super serious or more of a thought exercise, but it resulted in a very interesting discussion.

Aaron van Wirdum: 00:02:28

Yeah.
When I first saw the thread, it felt a little bit like homework.
It felt a little bit like an exam, where the teacher says, all right, why don't we redesign Bitcoin to get rid of the mempool?
And well, we'll explain what the exact proposal is.
Then you as the student have to sort of figure out why that's not a good idea.
That was sort of my first reading.
That's sort of what it did with my brain.

Sjors Provoost: 00:02:55

Yeah, and it helps you remind you why this mempool is useful in the first place.

Aaron van Wirdum: 00:03:00

Right, exactly.
The interesting thing for me was, I could figure out one or two reasons why I didn't like the proposal, but then the thread kept going for a while with more reasons and counter arguments, and it became more interesting than I anticipated at first, I would say.

Sjors Provoost: 00:03:22

Yeah, and then also lots of semi-related interesting proposals, for example, by ZmnSCPxj (pseudonymous)

## What is a mempool?

Aaron van Wirdum: 00:03:31

Okay, so Sjors, let's just get into it.
First question, what is a mempool?

Sjors Provoost: 00:03:39

So the mempool, we talked about the mempool in at least in episodes 19, 26 and 38, so if you want then listen to those (episodes).

The mempool is a place where Bitcoin transactions go.
So basically transactions go into blocks, but before they go into blocks, they have to be proposed somehow.
And the way people propose transactions is just to send them to everybody and everyone.
And then every node has a list of transactions that are not yet in a block, probably about 300 megabytes worth of those, depending on the mempool weather, as people would call it.

And this is generally kept in memory, though as Eric Voskuil pointed out in the mailing list, it doesn't have to be done in memory.
His Bitcoin client Libbitcoin keeps it all on disk.
It doesn't really matter.

The way he would describe it is: All these transactions that are proposed transactions, you can just put them on a disk and then you can say, okay, here's a block and the block points to all these transactions now.
That's essentially what a block is, it just points to all these transactions and then you're done.
Yeah, I guess that's the mempool.

Aaron van Wirdum: 00:05:05

That last part about how Libbitcoin works was a little bit of a sidestep, but in general, the mempool is just a collection of transactions that nodes keep and that miners keep and forward to other nodes, just the nodes that are sort of propagated over the network.
Every node has its own mempool and the miners use their own mempool to select transactions which they're going to mine on and hopefully become the new block.

Sjors Provoost: 00:05:31

Yes, but in general most of the transactions that are in your mempool will eventually be in a block and that's kind of important for the discussion ahead.

## The Problems

Aaron van Wirdum: 00:05:40

So what is the problem?

Sjors Provoost: 00:05:43

Well, there's many...

Aaron van Wirdum: 00:05:45

What is the problem that this mailing list thread sought to address and wanted to solve?

Sjors Provoost: 00:05:50

One problem is bandwidth, so at least as it was explained, sending all these transactions around all the time to all your peers, uses up quite a bit of bandwidth.


And the second is that, and that's I think what we covered in episode 38, we discussed then there was a bug in Bitcoin Core with the way RBF (replace-by-fee) was implemented and then we tried to explain how that impacted Lightning in unpleasant ways and we failed to explain how that impacted Lightning because it is very complicated.

And this complexity is the problem.
So it is very difficult for people, especially working on things like Lightning, to make the protocol safe against all the little gotchas that exist in this mempool.
The mempool looks very simple as we just described it, but there's lots of intricate details that you really have to understand and if you don't understand those correctly, then what could happen is you try to broadcast a transaction, for example to take money back from your channel because somebody cheated on you on the channel, and then that other person can do some shenanigan, put some other transaction in the mempool, or lots of transactions in the mempool and all of a sudden your transaction never gets confirmed and theirs does.
This is very difficult to reason about and so that's why the suggestion was: why don't we just get rid of the mempool?

Aaron van Wirdum: 00:07:15

I think the heart of the problem, which you just explained, is that sometimes it's important that your transaction actually makes it in the mempool at least, but there are restrictions on how big everyone's mempool can be because everyone has to do that and that just requires resources.
So there's a cap on that, but because of that cap, that means your transaction can't always get in and that opens the door to niche types of attacks.
And we're not going to get into that in detail, but that's sort of the short version of it.

Sjors Provoost: 00:07:46

It's worse than just having a cap on the size of the mempool.
There's all sorts of rules.
Like, if 100 transactions are related to each other, and you want to replace one of those 100 transactions, then that can cause problems too.

Aaron van Wirdum: 00:08:00

There are a number of limitations that sort of ensure that nodes don't get overloaded, but these limitations then open the door to potential weaknesses or attacks.

Sjors Provoost: 00:08:13

And this is also an incentive problem, really, because the incentive for things like Lightning is to be secure for the users of the Lightning channels, but the incentives for the people running a node, well, they're just having that mempool there, partially altruistically.
They have slightly different incentives.
They don't want to get overloaded, but their incentive is not to protect the Lightning network.
And this can cause some friction because the incentives are slightly different.


## The proposed 'solution'

Aaron van Wirdum: 00:08:39

Okay, so what we've now explained in our great podcast Bitcoin Explained, what the mempool is and what the issues with it are, in some circumstances, and then this thread offered a solution.
So what was the solution that was proposed.

Sjors Provoost: 00:08:58

Well, get rid of the mempool.

Aaron van Wirdum: 00:09:00

Get rid of the mempool altogether.

Sjors Provoost: 00:09:03

And of course that immediately poses a question.
If I have a transaction and I wanted to get it in a block, but there is no mempool, well then what do I do?
Do I just scream on the streets?

Aaron van Wirdum: 00:09:16

I mean in a way that's actually how it works now.
You're just screaming it to the network.

Sjors Provoost: 00:09:20

Yeah, that's correct.

Aaron van Wirdum: 00:09:23

Screaming to the streets is probably not an upgrade, but they proposed, why not just send your transaction directly to a miner?
Because miners, that's the one that actually needs the transactions.
They're in a way the only ones, but definitely the main ones that need a transaction, because they're the ones creating blocks.
So why don't we create a system where we send the transactions directly to miners, right?

Sjors Provoost: 00:09:48

Yes, but probably to a mining pool not to an individual miner, but still the question then is, well, who are the miners?
How many are there?

Aaron van Wirdum: 00:10:00

Where do you send the transactions?

Sjors Provoost: 00:10:01

Where are they?
And do we want to send it to their home address by envelope or how are we going to do that?

The proposal there was--we want to preserve miner anonymity, that was still a goal.
The way it could be done is miners could publish a onion service, so a Tor service, a hidden service, like a dark website I guess.
And to this "dark website", you send your transaction.

Automatically, of course, your wallet might have a list of a hundred different miners and it would just send the transaction to all 100 of them. That would be the idea.

Aaron van Wirdum: 00:10:41

Yeah so if you're a miner or maybe we should say more specifically, if you're a mining pool.
Because that's sort of the point, that a lot of the transactions or a lot of the blocks, all of the blocks essentially, I think, are currently mined by mining pools and as long as there's a manageable number of mining pools, then you can get all of their addresses and send it to them directly.

Sjors Provoost: 00:11:10

Yeah, that's the proposal.

Aaron van Wirdum: 00:11:12

When I say addresses, like you mentioned, it's like a Tor address.

Sjors Provoost: 00:11:17

Yeah, like a hidden service.
So this poses a problem or a number of problems.

Aaron van Wirdum: 00:11:23

Are we ready to get into the problems?
I think we captured the essence of the proposal:

Rather than having a mempool, rather than having every node on the network transmit every transaction to everyone else, to every other node, rather as a user sending your transaction just to the Bitcoin network, instead you'll send them to a number of mining pools.

Sjors Provoost: 00:11:48

Yeah, and one thing you can do there also is you can have, since you have a communication channel with the miner anyway, you can ask what fees they want, rather than guessing. That could be an advantage or not, but that's another possibility.
The reason why this might be useful is it gives you better privacy against the whole network.
So if you're doing something with your transaction, others might not know about it until it's confirmed and this makes it more difficult for the other side to start playing tricks that exploit some weird aspect of the mempool to cause problems for you.

Aaron van Wirdum: 00:12:24

Yeah but I think that the main reason for this, if I'm understanding this correctly, is simply that presumably mining pools have more resources available to just store whatever transactions are sent to them, so we don't have to be as limiting with the resources?

Sjors Provoost: 00:12:41

Yeah, I guess that's another argument.

Aaron van Wirdum: 00:12:43

And that's sort of how you solve the problem that we discussed when we started recording this podcast.

Sjors Provoost: 00:12:49

I guess one way to put it is there's a lot of these intricate rules about the mempool that are there because it has to be somewhat small and careful with resources and if you have giant resources a 10 gigameg computer then you can have fewer subtle rules and therefore the whole system is a bit more predictable.

Aaron van Wirdum: 00:13:08

Yeah, miners have a clear financial incentive to actually have that sort of resources.

Sjors Provoost: 00:13:15

Yeah, because they're investing pretty heavily anyway, especially a pool, right?
It's not even a single miner.

Aaron van Wirdum: 00:13:19

Yeah, and they want to earn the fees that they'll win if they set up these sorts of resources.

## Problems with the proposed 'solution'

### Miner Privacy

Sjors Provoost: 00:13:26

So, problems?

Aaron van Wirdum: 00:13:28

We're not going to follow the order of the thread, obviously.
But one thing that's important to notice at first is: it's not an option, actually, as a user to send your transaction just to one miner and then have the miners share it with each other.

That's not incentive compatible because if you send it to one miner, that one miner will have an incentive to just keep that transaction for itself.

So that miner...from now on, when we say miner, we mean mining pool...
Every individual mining pool will have an incentive to not share a transaction. They want to keep the transaction for themselves. So that way, they will be the ones that mine it. So really, you do need in this system to be able to send your transaction to all miners.

Sjors Provoost: 00:14:19

Yeah, because otherwise you have to wait forever.
If you only send it to one miner, and let's say the pool has 5% of the hash power, then it's going to take 20 blocks for you to get confirmed statistically and that's even assuming that your fee is high enough.

Aaron van Wirdum: 00:14:36

Then I think the next problem from there is how do you figure out who are all the miners and how to reach all of them?

Sjors Provoost: 00:14:43

Well we could hire Vitalik again and he could make a list and say these are the miners.

Aaron van Wirdum: 00:14:47

Why Vitalik?

Sjors Provoost: 00:15:49

Because we trust him.

Aaron van Wirdum: 00:15:51

Okay, fair enough.

Sjors Provoost: 00:15:52

And just to illustrate that may not be an optimal solution:
We'd rather not have a centralized list, obviously, and of course the proposal didn't really go into that, but I'm pretty sure they would agree with that constraint.
So then the question is, how would you go about...

Aaron van Wirdum: 00:15:10

Wait, what's the problem with the centralized list?

Sjors Provoost: 00:15:13

Somebody is in charge of it.
So they can tell miners they have to pay a fee in order to join that list.

Aaron van Wirdum: 00:15:19

Yeah, or they can tell miners you're only getting on the list if you censor these transactions.

Sjors Provoost: 00:15:26

Oh, we've done another episode about mining pool censorship.

Aaron van Wirdum: 00:15:29

So having a centralized list is not an option because you basically completely defeat the point of Bitcoin itself if you have a centralized list.

Sjors Provoost: 00:15:39

So another option would be to just allow gossiping of these mining pools.
So there's maybe a new peer-to-peer message and every node would tell every other node about every pool it knows about.
Problem there is how do you stop spam?
I could spin up a node and broadcast a million different potential mining pools.

Aaron van Wirdum: 00:16:02

Yeah, this sounds a little bit like our previous episode, where we discussed how nodes right now gossip IP addresses of other Bitcoin nodes, and then they would do the same thing with the addresses for miners.
And as we discussed in the last episode, this system was actually being attacked.
It wasn't really a denial of service attack, but it was still a brutal attack, as we discussed.
So this would open up that possibility of attack if you have to gossip.

Sjors Provoost: 00:16:36

And the impact of an attack is much worse because if you're just talking about gossiping the address of peers, you only need to connect to one honest peer in order to get the right blockchain.
So the gossip doesn't have to be very good as long as you at least have one connection that actually leads you to an honest node, then you're fine.
But not so with the mining pools, because as we just talked about, you really should be sending your transactions to every pool out there.
So if there are a million potential pools being gossiped about, you have to essentially just try all million of them, or at least you have to keep trying them until you think you have most of the hash power (aside from the question of how you would even know that you have most of the hash power)
So there has to be some limit on this gossip mechanism.
And the question is, how would you do that limit?

Aaron van Wirdum: 00:17:31

By limit you mean not everyone should be able to publish any address, essentially, right?

Sjors Provoost: 00:17:36

But we also don't want the limit to be set by an authority, so there has to be some sort of neutral limit, or there has to be some cost.
And so ZmnSCPxj said we could have some sort of staking involved and this is not proof of stake, so you don't have to have a stake in order to mine, but you would have to prove that you own some sort of some small amount of Bitcoin in order for your pool to be gossiped about.
So it's just about being gossiped about and then you can prioritize a little bit by who's staking enough coins.

So that could work.
It's more complicated (than what we have now), but it could work.
Right now, everybody can be a miner and just listen in.
Now they have to stake some coins and then some of the objections that were raised against that:
One of them is that ideally you want miners to have very good privacy so you want them to constantly stake different coins between different blocks, so that you can't see that it's the same pool or miner that you're dealing with.
But, if they have to constantly stake new coins, well, that's expensive.
So now they're incentivized to have the same identity over a long period of time.
And that's not very good.

On the other hand, as he points out, miners are really bad at privacy right now anyway, because they're all revealing what pool they are, but they don't have to do that.

Aaron van Wirdum: 00:21:01

Yeah, and I think in the OP, in the original email, is this idea that the way Bitcoin currently works, or the current topography of the network, or at least the level of mining centralization means that is in practice today, we only have 100 or whatever mining pools and they self-identify anyways.
So some of these arguments don't necessarily hold up against the current state of Bitcoin, like it's kind of similar.
However, we're also designing Bitcoin for a potential future where mining really is banned worldwide essentially.

And that's where privacy becomes very important.
And that's where a staking solution like you mentioned just now, which potentially harms privacy, would therefore potentially harm mining privacy and therefore Bitcoin itself.

I think that's a key thing to take into account is that the way Bitcoin is being designed is not for today but for a potential worst tomorrow.

Sjors Provoost: 00:22:10

Yeah, of course, also for today.

Aaron van Wirdum: 00:22:15

Well you say that, but I don't know if we want to go on a side quest on this particular topic, but should we?
I'll just mention very briefly that I actually don't think Bitcoin is being optimized for today.
That's one of Paul Sztorc's arguments for sidechains, for example, that while we live in an environment and in a world and in a regulatory environment where Bitcoin is actually just allowed and legal, then optimizing it for adversarial conditions gives it a disadvantage against systems that are not optimized for adversarial conditions because they can be more efficient and fast and so you're sort of losing some competitive edge in that environment.

Sjors Provoost: 00:23:00

Yeah, that makes sense.
It depends on what aspect of the protocol you're looking at, right?
There are already adversaries out there, so lots of privacy improvements are already being made with the idea that there already are chain analysis, chain analytics companies out there.

Aaron van Wirdum: 00:23:15

Yeah, that's true but at least not really for mining, apart from China and the solution there is to just migrate from China.
So we're really sort of designing for a world where Bitcoin mining is banned everywhere, (similar to the situation in) China everywhere, as Eric Voskuil literally explained it in the thread itself at some point.

Sjors Provoost: 00:23:35

You want to at least have that option to be able to exist in such a system.

### Miner Centralization

Sjors Provoost: 00:23:39

Another downside here is that it's very tempting for wallets to say:
I'm not going to send it to *every* miner out there, every new stake out there.
I might look at the pie and only send to whatever represents 80% of the mining capacity, because maybe with 20% of the connections you'll get your transaction to 80% of the miners.
And that creates a problem for new miners.

Aaron van Wirdum: 00:24:05

The reason for that is essentially because it's just a hassle to go and look for all of these small pools.
It's much easier to just say "All right, if I get it to these 10 or these 5, then it's 90% of hash power and it will almost certainly confirm"

Sjors Provoost: 00:24:20

Yeah, and the wallet software is probably not going to do all this verification, it's probably going to be the wallet authors that put in a hard-coded list of common miners or common pools.
So that's a problem.
And as sipa (Pieter Wuille) pointed out, new pools could also be censored: If you're trying to announce a new pool by staking some coins, then the existing miners could try to make sure that you never get to stake your coins.
So there's all sorts of risks there too, that it becomes a cartel.

Aaron van Wirdum: 00:24:48

Right, yeah, that was an interesting argument.
But let's take a small step back to the previous one.
What was the previous one?

Sjors Provoost: 00:24:56

That basically wallets have an incentive to only pick a subset of the pools.
And so if you're starting a new pool, you're probably very small, so nobody's going to send you any transactions.

Aaron van Wirdum: 00:25:07

Right, exactly.
So if wallets, out of convenience, prioritize the bigger pools, then it sort of locks these bigger pools in place, and it becomes much harder to compete with these pools, which is bad for, again, decentralization, for example, because these big pools can be regulated more easily.
And if competition is more difficult, then it becomes harder to find your way out of such a centralized solution.
And what was the one that you said after that?

Sjors Provoost: 00:25:43

Censorship by other miners.

Aaron van Wirdum: 00:25:45

Oh yeah so ZmnSCPxj was going on this sort of thought experiment, let's assume that we really want to do this, then what are the ways to do that?
And then one of the ways, which we just described, is to use staking as an anti-denial service type of solution, but then you need the existing miners to allow the stake to be confirmed on the blockchain, which they have an incentive not to do, of course, because that's also a way to keep the competition out.
So yeah, that was an interesting case.

Sjors Provoost: 00:26:21

I'm sure you could continue that conversation and come up with a system that prevents even that censorship, etc.
But it's still a can of worms that you're opening.
This whole proposalserves to close one can of worms, but as we're starting to discover now, the proposal is opening several other cans of worms.
So the net number of worms might actually go up if we do this.

Aaron van Wirdum: 00:26:43

I prefer less worms, but I think we're going to see even more worms from now.

Sjors Provoost: 00:26:47

Yes.

### Bandwidth

Sjors Provoost: 00:26:48

One of the arguments that was used to advocate this proposal was bandwidth.And it may be good to point out that in reality what happens is there's a lot of bandwidth to sort of gossip about which transactions exist, which is done using short identifiers.
But, the actual transactions themselves are usually only sent once. 

So, your node gets a bunch of ID's and is like,"Okay, give me the transactions that I don't know yet."
And that only happens once and then...

Aaron van Wirdum: 00:27:18

These are recent improvements or optimizations?

Sjors Provoost: 00:27:23

I don't know what recent means, is it multiple years.

Aaron van Wirdum: 00:27:26

Well, at least it wasn't there from the start?

Sjors Provoost: 00:27:27

Yeah.

Aaron van Wirdum: 00:27:28

Because it used to be the case indeed that every transaction was sent over the whole network, and then a block was found, and then the block full of all of these transactions was sent over the network as well.

Sjors Provoost: 00:27:41

Well, that's the second part of this.

So the transactions themselves are only sent once, but also every block is sent without the transactions in it.
At least if you're using this, your node will probably do that using this compact block idea where the compact block just says, "Here's the header of the block and here's the list of transactions that are in the block, you already have these transactions so you can construct the block locally.
You don't have to get them from me and if you are missing any transactions, just ask."

And in practice, that means the blocks are propagated really, really quickly.

Aaron van Wirdum: 00:28:15

Yeah, so there's two benefits:

It costs less bandwidth, which is a resource, and therefore it costs less resource, which is a benefit.

And it transmits over the network faster, which again, also helps against pool centralization, which is another topic which I think we probably shouldn't get into.

Sjors Provoost: 00:28:39

Basically it's important to have very few orphans or stale blocks, where if the block is still propagating around, then somebody else might also find a block at the same height and that just increases the opportunity for double spends and it causes lost revenue for those miners which would means it's better to be a big miner, etc.

Now, if you want to talk about block propagation in general, how to get blocks across the network fast, there is a really good talk by Greg Maxwell from 2017 at the San Francisco Bitcoin Developer Meetups, it's called [Advances in Block Propagation]({{ ref "/greg-maxwell/2017-11-27-gmaxwell-advances-in-block-propagation.md" }}).

So, the bandwidth argument is not as strong because it turns out there's already a lot of deduplications and we've talked about in one episode about how to do mempool even more efficient.
So the bandwidth argument is not as strong, plus if bandwidth is a constraint for you, just don't relay transactions because you're free to turn the mempool off on your own node.

So, I think the main argument for the proposal was complexity, not bandwidth, (given that) the bandwidth argument was not very strong.

Aaron van Wirdum: 00:30:19

Is there more?
This is the point where it starts feeling like the exam that I mentioned earlier.
Let's see how much of the thread we can remember.

### Transparency

Sjors Provoost: 00:30:29

Well, That's why I have notes.
There's a couple of nice one-liners in this whole thread, but I'll cite one by sipa.
Normally everybody can see what's happening in a mempool, right?
But in this proposal, there is no mempool and only select miners can see what's going on.
And so he (sipa) would say, "replacing socialized transparency with a few who get to see the actual details."
That, actually, doesn't sound as good as it is but, basically, normally everybody can see what's going on and now you can't see it.
So, you don't know whether there's any complexity, but there might be all sorts of mining shenanigans going on.
You don't know if pools are colluding or not, or if they have one view of the network and you have a different view of the network.

Aaron van Wirdum: 00:31:16

You would prefer that everyone can just see what's going on with the mempool and the blocks rather than just a select group of miners?

Sjors Provoost: 00:31:25

Exactly.
So a couple of things that were also mentioned in the paper, there are proposals like BetterHash and P2Pool, which are ways to get more mining pools or even to solo mine.
But, if everybody is solo mining or if mining pools get super, super small, that doesn't really work well with this, what we just discussed, because then the list of places where you'd have to send your transactions would be quite large.

### Fee estimation and other smaller problems

Aaron van Wirdum: 00:33:44

Oh, I have another one.
The fee estimation becomes harder because right now fee estimation actually takes the mempool into account to determine how much fee a node will include in the next transaction that it creates.
If I'm going to be paying you, then my node will essentially look at the mempool as well as past blocks.
If my node doesn't have a mempool, then I can't use that for fee estimation, and therefore I might be overpaying in fees or waiting too long before my transaction finally confirms.

Sjors Provoost: 00:34:16

Because the mempool makes it more difficult for miners to sort of cheat when it comes to fees.
So what a miner could do is if they just compose the block themselves, they could put a bunch of transactions inside the block that pay really high fees, but it's just money moving from themselves to themselves and the fee also goes to themselves.
So then it looks like the fee is really high.
But given that the mempool exists, if you broadcast a transaction like that, it'll get mined by your competitors.
So it's a transaction from you to yourself, but the fee goes to your competitors so it's very expensive to lie about the fees.

Aaron van Wirdum: 00:34:52

In general, one of the things that was mentioned, and we already mentioned a form of it, at least, which was that your wallets might not have the incentive to look for smaller pools.
The same is true even if your wallet does have the incentive or even if you do try, even then there's going to be new miners joining the network and a very new miner might not be included in the list yet, or there's a delay between joining the network and letting people know that you're accepting transactions, while right now in Bitcoin, (we) just plug in and are ready from the get-go.

Sjors Provoost: 00:35:32

Yeah, well, we already talked about centralization in general, right?
And as a reminder why centralization could be bad, if there's just 50 pools or 10 pools, then it creates very clear denial-of-service targets or DDoS targets.
If an attacker wants to take out certain nodes using any of the attacks we've previously talked about, they would know which nodes to focus their attack on.

Whereas right now, if you look at the network, at least naively, any node could be a miner, so you have no idea which Bitcoin node to attack to actually bother a miner, so it's kind of nice that miners can hide out in the crowd in general.

Aaron van Wirdum: 00:36:10

Yeah, you kind of want every node to look the same. You want every node to look like a peer on the network, and then some of these peers might be mining.

And there are ways to de-anonymize that already.
That was also mentioned in the thread.
You can analyze to see where new blocks emerge on the network, and then that's presumably miners.

Sjors Provoost: 00:36:33

But it's still a bit probabilistic, because you're not listening to all nodes at the same time, and there's some tricks in there.

Aaron van Wirdum: 00:36:37

And I'm sure we can think of future optimizations to decrease that problem as well.
You know, Dandelion, that kind of stuff, you can maybe do those for blocks.
That's a tangent.

Sjors Provoost: 00:36:48

So I can bring up one more little tangent that was brought up that was interesting from this discussion that's not really an upside or a downside.
This is that nodes right now for the most part, are relaying altruistically, but there is some self-interest, right? There is the self-interest of being able to calculate fees, for example.
And there's a self-interest of making sure blocks are propagated fast because that makes it less likely that your confirmations get cancelled.

So that's all good, but it would be nice if there was a more direct way to make money from being a node, a relayer.
And what ZmnSCPxj proposes roughly is that each node could try and compose packages of transactions, look at the mempool and basically construct packages that are economically efficient.
Because it's mathematically quite a hard problem to make the most optimal block given a set of transactions if you have 300 megabytes of transactions to actually select them in a way that you maximize your revenue.
And so you could outsource that computational difficulty task to individual nodes and they would send you package proposals.
And in exchange for a good proposal, you would get paid.

Now, this is very hand-wavy, because there's all sorts of things like, how would you actually do this?
But it was a cool idea.

Aaron van Wirdum: 00:38:16

I lost the plot on that one.
Hopefully the listeners did not.

Sjors Provoost: 00:38:19

That's okay if you did.
Yeah, I think that's roughly the whole discussion that we did.
So you should give it a read.

Aaron van Wirdum: 00:38:27

Yeah, I hope we passed our exam.
I hope our listeners paid attention for when they get their exam.
We probably forgot some things.
If you're really interested in this stuff, obviously check out the thread itself.
It kept going for a while and there were some surprisingly interesting insights.
Some I hope we conveyed, but we probably forgot at least one or two.

Sjors Provoost: 00:38:49

All right, so you got anything else then?

Aaron van Wirdum: 00:38:53

No, I'll see you in, I guess a month from now or something like that.

Sjors Provoost: 00:38:56

Who knows? 
Thank you for listening to Bitcoin Explained.
