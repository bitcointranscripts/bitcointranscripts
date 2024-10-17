---
title: Bitcoin Core 24.0
transcript_by: realdezzy via review.btctranscripts.com
media: https://www.youtube.com/watch?v=3UfrB7_ZOx0
tags:
  - bitcoin-core
  - rbf
  - coin-selection
  - descriptors
  - miniscript
speakers:
  - Sjors Provoost
  - Aaron van Wirdum
date: 2022-10-07
episode: 65
aliases:
  - /bitcoin-magazine/bitcoin-explained/bitcoin-core-v24
---
## Intro

Aaron van Wirdum: 00:00:20

Live from Utrecht, this is Bitcoin

Sjors Provoost: 00:00:23

Explained.

Aaron van Wirdum: 00:00:24

Hey Sjors.

Sjors Provoost: 00:00:25

What's up?

Aaron van Wirdum: 00:00:26

I'm good.

Sjors Provoost: 00:00:27

How do you like the weather?

Aaron van Wirdum: 00:00:29

It was too hot all summer and then it was nice for about a week and now we're back to too cold.

Sjors Provoost: 00:00:36

This is gonna be a great winter.

Aaron van Wirdum: 00:00:39

That's winter for you at least for now it's still a little bit light.
For example while we're recording It's still light and it's past six.
That's the really dreadful moment for me when the clock changes.

Sjors Provoost: 00:00:55

Well, we go to standard time, although some people want to change it and make the summertime the default, which I think is terrible.

Aaron van Wirdum: 00:01:03

I would definitely prefer that, just because I don't get up that early anyways so I like to optimize my sun hours

Sjors Provoost: 00:01:13

I mean ultimately you can just get up whenever you want to get up right unless you have to be in a physical place.

Aaron van Wirdum: 00:01:19

But you are kind of reliant on the rest of society around you, right?
Stores close at a certain time and people get out of work at a certain time, might be your friends, or you want to record a podcast at a certain time because you want to eat at a certain time.
So I don't have that full flexibility that you suggest because of all these people around me.

Okay, Sjors, I'm going to shill the conference one more time.
Conference is coming up.
You can get a 10% discount if you know how to spell Sjorsnado, that's your discount code.
Sjorsnado on I think it's b.tc/amsterdam.
I think that's the website for the conference.
All right, Sjors, We're going to discuss the new Bitcoin Core release that's coming up.
It's not here yet.

## What does it mean

Aaron van Wirdum: 00:02:09

It's Bitcoin Core 24.0, that's the upcoming one.
Real quick for maybe there are some new listeners, What does it mean that there's a new Bitcoin Core release coming out?

Sjors Provoost: 00:02:18

Because Bitcoin Core does not have a roadmap or anything like that, there is just a new release every six months or so.
And things that are ready go into that new release and things that are not ready may go into another release.
So there's nothing very special about these releases.
And so it's time for number 24.

Aaron van Wirdum: 00:02:37

It's just an update that happens twice a year.
Generally, whatever is done is done.

Sjors Provoost: 00:02:41

Yes. And then there are some minor updates throughout the rest of the year.
That might be 24.1, 24.2, etc.
And those typically are just bug fixes, but no major changes.

Aaron van Wirdum: 00:02:51

And right now there's a release candidate.
At the time of recording this podcast, there's I think the first release candidate for Bitcoin Core 24.

## Release Candidate

What does a release candidate mean?

Sjors Provoost: 00:03:01

Kind of what the word suggests, it's a candidate for the release.
So if all goes well, then the actual release will be made identical to the last candidate.
But the idea is that people who know what they're doing should be downloading that release candidate and or compiling it themselves and playing around with it and making sure that nothing crashes the things they use especially if you run some sort of automated service like you might be running an exchange or maybe you're running BTC pay or something like that you want to make sure nothing breaks in your setup because Bitcoin Core tries to not break things that use it but it happens occasionally.

Aaron van Wirdum: 00:03:39

If there's no report of anything breaking then this release candidate will basically be the release right?

Sjors Provoost: 00:03:45

Yeah, but I think there are already some things that have been improved so there will definitely be a second release candidate.

Aaron van Wirdum: 00:03:51

okay yeah, and I think in previous Bitcoin core releases there were an average of four or so.

Sjors Provoost: 00:03:56

Yeah, I'd say that's typical.
So usually there's two weeks between them, So you release it and then maybe after a week or so, people start fixing things, and then after two weeks, there is a new one.

Aaron van Wirdum: 00:04:06

Right, so realistically well technically the new Bitcoin Core 24 release could be released any day now, but practically speaking will probably be at least a couple more weeks, right?

Sjors Provoost: 00:04:17

Yeah, I'd say so.
I think there is a release, attempted release schedule on the Bitcoin Core repository, which I think is for mid-October.

Aaron van Wirdum: 00:04:28

So, there are a bunch of new features as well as bug fixes and improvements, sorry, performance improvements in this new release.
We're going to discuss a couple of these.
This is kind of just our selection.
If this podcast was made by two other people, by Ors and Sharon, they might make a different selection.
But we, Sjors and Aaron, we made the selection.

Sjors Provoost: 00:04:59

You can look at all the commits, so all the atomic changes that go into a release, and there could be a thousand of them, but most of them are very boring, or at least they are very boring unless you are really into details of how compilers work or into cleaning up code for the sake of cleaning it up.
So there's a lot of changes that are just not very interesting to discuss, although they are important and they should be, they are being, you know, they always get reviewed because any of those changes could of course be a really scary thing.

Aaron van Wirdum: 00:05:29

Yeah, I'm just saying we made a selection of some of the changes that we think are probably the most interesting
to you, our dear listener.

## Download headers from peers

Sjors Provoost: 00:05:38

That's right.

Aaron van Wirdum: 00:05:40

Okay, so let's start.
Sjors, I think that this one is the first one mentioned in the release notes as well.
It's about the peer-to-peer and network changes.
Is that a typo?
Should you just say peer-to-peer changes?
Peer-to-peer network changes?
Whatever.

Sjors Provoost: 00:05:55

Peer-to-peer networking.

Aaron van Wirdum: 00:05:57

Let's move on.
So it says that there's a change and you're gonna explain to me what this is.
That's the format of the podcast in case you forgot.
It says download headers from peers so downloading of headers from peers has been reworked.
That's right somehow.

Sjors Provoost: 00:06:18

Yeah, this one might be worth a separate episode, but I think we can explain the gist of it now.
So when your node first starts up, it is going to find peers, which we discussed in an earlier episode, and then it's going to download headers from peers, which we've also discussed in earlier episodes.
So it tries to get all the headers first.

Aaron van Wirdum: 00:06:36

Hang on, so every block has a header which is essentially the hash of the block itself, right?

Sjors Provoost: 00:06:41

Plus a little bit of extra info that, for example, contains the timestamp and the amount of proof of work.
Well, the amount of proof of work follows in the hash.

Aaron van Wirdum: 00:06:52

It's basically hash plus some extra info.
So it's not the whole block.
So first you start downloading not the whole block, or not all of the blocks, but you start downloading the headers, right?

Sjors Provoost: 00:07:04

Yes, and the idea is that you first want to make sure that the chain that you're following has enough proof of work that it's even worth downloading the blocks for.
Now that's been improved many years ago.
It used to be that I think it would just download headers and then some blocks and then some headers and then some blocks and that has been changed many years ago to first download all the headers and only then when you know for sure that you have enough proof of work because you can check that based on the headers then you start downloading the blocks.
This prevents you from wasting time chasing and basically chasing dead ends.

Aaron van Wirdum: 00:07:32

Okay, that was already the case.
So even in Bitcoin Core 23, you would already start with downloading only the headers and only later the blocks.
Okay, so what has changed?

### Download headers twice

Sjors Provoost: 00:07:41

So what has changed now is that we're going to download the headers twice.
And that might take some explanation on why you want to do that.
So there is the potential problem that you're worried about with headers is that you could receive quite a lot of them.
Because you know right now there have been about 700,000 blocks since the Genesis but a miner could manipulate the timestamps and they could create a fake blockchain with blocks that are every second and that would be billions and billions of blocks.

Aaron van Wirdum: 00:08:10

I guess anyone can only a miner can do that?

Sjors Provoost: 00:08:13

Well anyone who can mine.

Aaron van Wirdum: 00:08:15

You do need basically the ASIC hardware to do that.

Sjors Provoost: 00:08:18

Well, you'd have to do the math on what kind of hardware you would need to do it.
I mean, in principle, you don't need an ASIC to mine blocks, right?

Aaron van Wirdum: 00:08:24

You need the proof of work, is what I'm saying.
You need the actual proof of work,

Sjors Provoost: 00:08:27

Yeah. But I mean, you know, the proof of work in the beginning was quite low, so you can do that with a CPU, but maybe if you wanna do some damage, maybe you need more power.
Anyway, so the worry is that you get a billion headers from a chain and it's not the real chain, but it's a lot of low-work nonsense.
And the problem with that is that not just do you have to download it because that's kind of hard to avoid But you also tend to store it on your disk because maybe you receive half a billion headers But and those don't go anywhere, but you don't know maybe there's another half a billion headers on top of that that do take you to the real tip.
So you can't really throw those headers away that easily.
And so the attack would be that lots of headers are sent to you.
And that attack has been known for a long time.
And the solution to that so far has been checkpoints.

Aaron van Wirdum: 00:09:16

Okay, hang on, let's summarize this.
So first the problem was solved...

Sjors Provoost: 00:09:24
The first problem was just getting lots of spam blocks.

Aaron van Wirdum: 00:09:26

Yes, so that problem was solved by only checking the headers.
But now basically a new problem is introduced, namely someone could just send you a boatload of fake headers, essentially.
And then while downloading all these headers, you also have to store it.
This is resource-intensive.

Sjors Provoost: 00:09:43

Yeah, so it's basically the general category of problem is called a resource exhaustion attack.
So I'm trying to exhaust one of your resources.

Aaron van Wirdum: 00:09:51

And then you mentioned this was solved with checkpoints.

Sjors Provoost: 00:09:54

This has been solved very early on.
That's kind of what the checkpoints are for.
Fortunately, Checkpoints have not been added since 2013 because they are not a very nice way to do it.

Aaron van Wirdum: 00:10:05

Just to be very clear, what is a checkpoint?

### Checkpoints

Sjors Provoost: 00:10:07

What a checkpoint does is it says this specific block with this hash must exist in the chain.
Right.
So it's not optional.
Right.
And that has always been done retroactively, like a long time after.
So a way to abuse checkpoints is to say, well, somebody stole my coins.
I'm going to now introduce a checkpoint that happened before somebody stole my coins for a new block that I've created.
That does not steal my coins.
And then, you know, we start history again.
That's the worst case.

Aaron van Wirdum: 00:10:34

Well, that should be after some of, well

Sjors Provoost: 00:10:37

Yeah, so somebody steals my coins.
Let's say that happens today.
Then I call up a miner and say, could you make a couple of new blocks that don't steal my coins?
Here's the double-spend version that I want to include in that block.
They mine it for me and then I release a new version of Bitcoin Core that says here's a checkpoint.
You must ignore like the real big chain that has built on top of the hack and actually go for this other chain.

Aaron van Wirdum: 00:10:59

Yeah so with the checkpoint you can sort of overrule the longest chain rule.

Sjors Provoost: 00:11:04

That's right and that has been done in many altcoins.
So the concern is that we don't want that to happen in Bitcoin.
So one way to prevent that has, I think, has been from the beginning to introduce the checkpoints only much after they've already happened.
So you already know they're part of the longest chain, everybody can verify that, and the checkpoint is buried quite deeply.
But it's still not a very pretty solution, and so people stopped doing it.
So it'd be nice, but it'd be very nice...

Aaron van Wirdum: 00:11:29

Did you mention when the last checkpoint was?

Sjors Provoost: 00:11:31

I think it was 2013.
It's quite a long time ago.

Aaron van Wirdum: 00:11:33

It's a while.

Sjors Provoost: 00:11:35

And so it'd be nice to get rid of those things entirely because, you know, they are confusing and, you know, we probably don't want to add new ones.
So In order to get rid of them, you still need to fix this resource exhaustion attack that we just talked about.
So then how do you do that?
Well, the trick is to download headers twice, as I said.
So what you do is you download them once, and when you're downloading them once, you don't save them.
You just look at them, check if they're correct, and you throw them away.
This means it does not use any of your disk space.
Then if you see enough work at the end, if you checked all the headers and you see the proof of work is enough, it's the longest chain, Then you ask the peer, hey, can you send them again, please?
And you download them again.

Aaron van Wirdum: 00:12:21

I think I mentioned yesterday when we went over this in our preparation, this is kind of how my attention span usually works.

Sjors Provoost: 00:12:28

Exactly.
You first let me ramble on a bit, and then you think, this might actually be interesting.
And then you say, what did you say again?
Please repeat.

Aaron van Wirdum: 00:12:35

Can you repeat that for me?

Aaron van Wirdum: 00:12:37

Yeah, so this is how Bitcoin nodes now actually work.

Sjors Provoost: 00:12:39

That's right.

Aaron van Wirdum: 00:12:40

They first listen, they don't store anything, but then if it sounds actually interesting, if they see the proof of work, they just ask again and they get all the blocks.

Sjors Provoost: 00:12:47

They're like, wow, that's cool.

Aaron van Wirdum: 00:12:48

But they get all the headers again, I guess.
Or do they now also get the blocks?

Sjors Provoost: 00:12:51

Well, then once those headers have been downloaded the second time, things continue as always.
You just start fetching blocks for the headers.
Now there's, of course, a little gotcha there because, well, who says that the second time you're getting the same headers as the first time?
You don't know that, because you didn't store them.
So what you do instead is you store one checksum, which is a one-bit checksum, every 50,000 blocks or so.
So every 50,000 headers you store a zero or a one depending on the contents of those headers and you do that every 50,000 headers.
That is very little information but it turns out that it's actually quite difficult for anybody to fake that information.
So it's for anybody to create fake headers that do match your checksum, even though it's a very small checksum.

### checksums

Aaron van Wirdum: 00:13:36

Right, yeah, a checksum is essentially you add up all kinds of numbers and you get a very short number which doesn't in itself prove anything, but I guess if you do it a bunch of times then.

Sjors Provoost: 00:13:46

If you add up the same numbers you're gonna get the same checksum.
So if you have 50,000 headers, you add all those up together, then you get either a one or a zero.
If you change any of the headers, well, you'll either get a one or a zero, but it might be a different one.
Now that, of course, is a 50-50 chance.
Yeah.
So that's pretty easy for a hacker to go after, but there are many blocks.
So it turns out that if for long enough, I might be wrong on the exact number, it might be less than 50,000, but if you have enough of those one-bit checks, basically, then it becomes quite hard for an attacker to create a fake chain that has enough proof of work but that is different from the last one they sent you.

Aaron van Wirdum: 00:14:23

Yep okay, that makes sense.
So there's still a small part of the problem left which is you do still need to download it the first time.
Yes.
But it solves another part of the problem essentially.

Sjors Provoost: 00:14:37

Yes, so the downside is you're downloading headers twice so that might be another 100 megabytes or so in the ideal case.
However, compared to the size of the blockchain, it's not too bad.
And compared to the worst-case attack, it's definitely not bad.

Aaron van Wirdum: 00:14:53

And of course, even if an attacker would want to try this for some reason, it's also costing the attacker resources because he has to upload all the same data you have to download.
It doesn't really do much, this attack, right?
It can't allow you to steal coins or anything like that.

Sjors Provoost: 00:15:10

Well, with this defense, no, because all they can do is waste your bandwidth.
And there are many ways to waste your bandwidth, right?
An attack can just send you a gigabyte block and it would or just complete gibberish in general so that's not a new problem

Aaron van Wirdum: 00:15:24

okay so this was included in Bitcoin Core 24 and will be

Sjors Provoost: 00:15:28

And the checkpoints are still there But the idea would be to remove them eventually.

Aaron van Wirdum: 00:15:32

Okay, so that would be removed in a future release?

Sjors Provoost: 00:15:36

Yeah, and of course, you know, there has to be some additional discussion to make sure that that was really the last thing we needed, that the checkpoints are not also protecting against something else that we forgot about.

## Full-RBF

Aaron van Wirdum: 00:15:44

Okay, well, that's the peer-to-peer part of Bitcoin 24.
Then the next point is Mempool uses full-RBF now or can use full RBF?

Sjors Provoost: 00:15:57

Can use full-RBF.
So it used to be that if you wanted, I think we've done an episode about replace by fee, RBF.
So I think the listeners should listen to that.

Aaron van Wirdum: 00:16:06

You can summarize it in two sentences.

Sjors Provoost: 00:16:08

So basically the Bitcoin protocol itself, when you have one transaction and then you want to double spend it, there's nothing stopping you from doing that before it's in a block.
Now, from an incentive point of view, miners are most likely to include the block with the highest fee, but they don't necessarily have to.

And so there was a proposal by Peter Todd many, many years ago to say, well, normally the nodes, well, let's go one step back.
So what miners do is ultimately up to miners.
You have no control over that.
And Bitcoin Core can change things in the software, but miners will do whatever they do, because what the mempool does is not consensus.

However, the nodes will relay transactions.
And so you can change the nodes to say, well, I'm gonna broadcast some transactions and not gonna rebroadcast other transactions.
And so this new rule, opt-in replaced by fee, opt-in RBF, basically said that normally we only broadcast the first version of the transaction we see, regardless of the second one.
Doesn't matter if the second one pays more fees.
But if you put a flag in a transaction that says, I want to opt-in to replace by fee, then nodes will refer, will relay transactions that pay a higher fee only and a bunch of other constraints.
And so this gives the recipient some assurance, not much, but some assurance that if this flag is present, this transaction could be replaced anytime.
You really have to wait for it to confirm.
If it doesn't have this flag, it might still disappear.
It's just a little bit less likely.

Aaron van Wirdum: 00:17:35

Yeah, I want to clarify one thing because you mentioned double spending in this context.
And you are of course right that this can be used to double spend until it's included in a block, as you said.
But the main purpose or the main idea for using a flag, for example, is to increase the fee on your own transaction, right?

Sjors Provoost: 00:17:54

I don't know how long that idea has been around because the idea of being stuck in a mempool, that concept didn't even exist until 2015 or 2016.
That was never a problem.

### RBF summary

Aaron van Wirdum: 00:18:04

But it was the flag was introduced around that time and definitely in the context of that, that was the debate.
Yeah, I'm sure about that.
So to summarize that, At least the idea for the flag was you send a transaction, but the mempool was full, and therefore your transaction is not confirming.
Now with the RBF flag, you can basically resend the same transaction with a higher fee, and therefore, because the flag is included, nodes will actually forward it to miners and it can be included in a block.

Now you don't actually need to include the flag anymore.
If this setting is turned on?

Sjors Provoost: 00:18:44

Yeah, I think that if you turn this setting on, then the flag does no longer have to be in there, it'll relate anyway so then I'm guessing there are other rules though because I assume the fee has to go up but I'm not sure about that

Aaron van Wirdum: 00:18:56

So in my case, if so far I was running Bitcoin Core 23, my node would not forward a transaction even if it had a higher fee and it conflicted with the previous transaction.
It would not do that.
But now with Bitcoin 24 I can switch the setting and now it will actually forward that transaction.

Sjors Provoost: 00:19:22

Yeah, I think that's it and it basically means that if you're relying on this opt-in RBF system to prevent double spends, basically to prevent double spends, you should now rely on that less so, because there's going to be more nodes that will relay this thing regardless.

Aaron van Wirdum: 00:19:37

I don't know about almost certainly, but there's definitely a much bigger chance that a conflict in a transaction will make it to a miner now, right?
Because I think there only needs to be a relatively small amount of notes on the network that actually do it for a transaction to just find its way over the entire network.

Sjors Provoost: 00:19:54

But there were already ways to do it, right?
There was a patch by Peter Todd which was pretty small and you could use that to modify your nodes.
So there's already some nodes doing it.
Now there's more, presumably.

### Merchants

Aaron van Wirdum: 00:21:06

So does this mean that some merchants are going to be unhappy?

Sjors Provoost: 00:21:12

Well, they might be for that reason.


Aaron van Wirdum: 00:21:13

There are still some merchants that rely on zero-conf.

Sjors Provoost: 00:21:15

Yeah, there are definitely merchants that do that.
But the flip side is that there are also merchants that use Lightning and Lightning is generally bothered a lot by this, by the existing RBF rules because they make it much more complicated to deal with penalty transactions.
So they may get, in the long run, they may get a better lightning experience out of this.

Aaron van Wirdum: 00:21:36

I mean, my personal opinion is that this should just be the general rule.
Transactions should always be broadcast and forwarded, especially if they have a higher fee.

Sjors Provoost: 00:21:48

I mean, maybe, we've already had this discussion during that episode, I guess, but I would also say that if you just turn on the RBF flag by default, it shouldn't bother you either.
But I think the bigger problem is that this RBF flag has very specific rules.
It's not just that you set the flag, you also have to do a few other things and those other things cause complications.
So that could be a reason to say, you know what, let's forget about this opt-in RBF completely and relay everything that is reasonable.
But there are trade-offs.
One is just bandwidth because if my node relays everything that you sent to it, I could send you one transaction and then increase it by one satoshi per byte or increase it by.
Don't even increase the fee, but just change the destinations a bit, and I could send you millions and millions of variations of the same transaction, basically wasting everybody's bandwidth.
So it's not entirely without trade-offs.

## Descriptor Wallet Migration

Aaron van Wirdum: 00:22:39

All right, let's move on to the third point.
So we mentioned the change on the peer-to-peer network, the block header thing, and we just mentioned RBF.
And then the third point is this related to descriptor wallets and migration to the descriptor wallets?

Sjors Provoost: 00:22:52

Yeah, I'm not sure how much we covered the descriptor wallets so far but the gist of it is that the Bitcoin Core wallet is quite old.

It used to be just a bag of keys and then given a private key, the wallet would have to pay attention to certain scripts.
I think in one of the first episodes we explained what scripts are.

But the simplest scripts is just that anybody with the public key can spend this coin.
The second simplest script is that anybody with the hash of the public key can spend the coin or anybody with the public key for which the hash is blah, blah, blah.
And then there was, but then later on came SegWit and that created another two variations of how you could spend the coins.
Because you had the address of BC1, and you had the address that looked like a P2SH address with SegWit wrapped in it.
So the wallet just became a giant mess.

Aaron van Wirdum: 00:23:42

Because you have multi-sig writes and stuff like that.

Sjors Provoost: 00:23:45

Well, yeah, that makes it even more complicated.
But basically the Bitcoin Core wallet became a bit unwieldy.
And so one of the improvements that was introduced was to create a new way to store data and basically saying, well, here's keys, but more importantly, here's exactly what scripts you want to watch for.
So you can specifically say, I only want to check for Taproot transactions for this private key, and not also for legacy transactions for this private key.
Now your wallet handles all this.

Aaron van Wirdum: 00:24:14

What are the practical benefits of that?
Just less resources?

Sjors Provoost: 00:24:17

For the end user, this doesn't matter.

Sjors Provoost: 00:24:19

It just means that their wallet software is better maintained.
Because it's less of a headache for the wallet developers to deal with this.
So it basically involved the giant rewrite, mostly done by Andrew Chow.
And one of the challenges there is we have this old wallet and we want to move people over to the new wallet.
And so the first step for that is this new RPC call called `migratewallet`, which does what it says it does.

Aaron van Wirdum: 00:24:43

It will migrate your wallet?

Sjors Provoost: 00:24:45

And for the simplest cases, you know, if you created a wallet in the last couple years and you didn't do anything super fancy, very complicated, multi-sig setups, whatever, this will work.
If you did do something complicated, then please test it.
It'll make a backup, but maybe make your own backup too.
And we'd like to see bug reports basically, because maybe you have some super complicated wallet setup that does not migrate properly.

Aaron van Wirdum: 00:25:09

So basically what this does is your wallet software will just go over all of the UTXOs and say, what, this is a paid to public key?
This is a multisig.
And throw them into different buckets

Sjors Provoost: 00:25:19

No, it will not go over the UTXOs.

Sjors Provoost: 00:25:22

No, it will go over the keys inside the wallet.
The transaction list you have is kind of the same.
It'll look through what keys you have in the wallet and it will restructure those as descriptors.

Aaron van Wirdum: 00:25:31

It will throw these in the different buckets?
Okay, instead of one big bucket.

Sjors Provoost: 00:25:36

That's right.

Aaron van Wirdum: 00:25:37

Okay, I think that's clear enough then.
And as mentioned, this is mostly to benefit just the developers, not so much users.

Sjors Provoost: 00:25:46

I mean yeah, the users benefit indirectly, but yeah, it does.
I mean, descriptors have already been used to allow taproot.
So if you wanted to use Taproot, you either need to create a whole new wallet or you need to migrate to a descriptor wallet and then add Taproot to it.
So there is that too.

## Miniscript Support

Aaron van Wirdum: 00:26:04

Okay, there's been moving on to the fourth point, Miniscript support.
Has Miniscript support been added to Bitcoin Core?

Sjors Provoost: 00:26:11

Yes, in very limited fashion.
I think we have done a whole episode about Miniscript, but it basically lets you do very advanced scripting systems.
So something like I want to spend with two keys or I want two signatures or after five years I want one signature Or if somebody has the pre-image of this SHA-256 hash, then they only need one signature plus whatever.
Miniscript allows you to do fairly arbitrarily complicated things.
And Bitcoin Core can now, if you have a piece of Miniscript, it can now watch that.
You cannot spend from it yet.

Aaron van Wirdum: 00:26:48

I mean, the other way to put it, the simple way to put it maybe is miniscript allows for smart contracting type of stuff, right?

Sjors Provoost: 00:26:59

Yeah, I guess.
I mean that might be overselling it a bit, but yeah.
To the degree that Bitcoin can support smart contracts, the Bitcoin script language is very complicated.
You don't want to write Bitcoin script by hand, you will make mistakes.
Like even Andrew Poelstra and people like that will make mistakes.
So, Miniscript is designed to get the most out of the existing Bitcoin script system in a safe way.
That's, I think, the most fair way to put it.

Aaron van Wirdum: 00:27:26

Right, sorry, and what does it mean that it's been added now?
In what way has it been added?

Sjors Provoost: 00:27:31

It means you can create a wallet.
So if you create a new wallet, you can put a piece of miniscript inside of that wallet and it will basically let you create addresses for that miniscript and you can send coins to those addresses.
But you can't spend them.

Aaron van Wirdum: 00:27:44

I see.
So, you can't spend them.
Not yet.

Sjors Provoost: 00:27:48

So you shouldn't do that.

Aaron van Wirdum: 00:27:49

Okay, yeah, don't do it yet.
And this sounds like you might need to run a separate wallet or a separate piece of software that you connect to your Bitcoin Core node.

Sjors Provoost: 00:28:00

No, well, yeah, in order to create the miniscript itself, you will need separate software.
There is a miniscript compiler, but you can write miniscript by hand too if you want to.
So, in principle, you don't need a second piece of software.
Now, the idea is that a future version of Bitcoin Core will also be able to sign for it.
But you shouldn't count on that, you shouldn't use it until it does.

Aaron van Wirdum: 00:28:21

Okay, well this sounds like a pretty big step then, doesn't it?
It sounds to me like it's a pretty big step.

Sjors Provoost: 00:28:26

I think it is pretty big, yeah.
And the other constraint is that it only works for the first version of SegWit.
So those are addresses with BC1Q.
So it does not work for Taproot yet.
And because there's a lot of work that needs to be done, or at least there is work that needs to be done in order to have Miniscript work with Taproot at all.
And then once it does that in general, so the specification of the manuscript can handle it, then the next challenge is to actually get that into Bitcoin Core and to really use Taproot and Miniscript well, you probably want musig to the signature aggregation stuff.
That also needs to be added to Bitcoin Core.
So there is a ton of work still left to do.
But this is one step.

Aaron van Wirdum: 00:29:06

Is there currently, so we're right now talking about Bitcoin Core, obviously.
Is there currently other Bitcoin software that already allows you to create and use Miniscript?

Sjors Provoost: 00:29:17

No, as far as I know, there is there's basically a library called Rust Miniscript and a library written by CPython that does Miniscript and C++ Those libraries you can use but they're not fully functional wallets So I don't know if anybody is using Miniscript in the wild, maybe Blockstream is for their what is it?
Liquid sidechain stuff, I would know.

Aaron van Wirdum: 00:29:36

Okay, well interesting, like I said that sounds like a pretty big step actually.

Sjors Provoost: 00:29:43

Yeah, and it would also I think This is the longer-term trend of hopefully turning Bitcoin Core from a not a very good wallet, was quite slow, quite weird, to hopefully a very good wallet.
And at least a very good wallet for power users, right?
So maybe exchanges want to use it more.
My hope is that if this wallet becomes very powerful, then more people will help review the code and more people will help improve it.
So you kind of get this self-amplifying effect.
Once it's useful enough, more people will look at it, but it takes a very long time to become useful enough because it's not useful enough so not enough people are working on it.
It's really I think maybe four people.

## Opt-in RBF

Aaron van Wirdum: 00:30:27

All right moving on to the next point.
The next point on our list is another point about RBF.

Sjors Provoost: 00:30:36

This is just about opt-in RBF, that the wallet will, the wallet RPC, so the command line wallet will now use it by default.

Aaron van Wirdum: 00:30:45

Oh, that's right.
Okay, wait, so we're not talking about the GUI, right?

Sjors Provoost: 00:30:49

No, the GUI already switched to use RBF by default.

Aaron van Wirdum: 00:30:53

And now the command line does as well?

Sjors Provoost: 00:30:54

Yeah.

Aaron van Wirdum: 00:30:56

Okay, go on.
Maybe I should just let you finish.

Sjors Provoost: 00:30:58

So why didn't it?

Aaron van Wirdum: 00:30:59

Yeah, why didn't it yet?

Sjors Provoost: 00:31:00

So one of the reasons is that people are using the Bitcoin Core wallet in some automated systems.
So if you're running a Bitcoin ATM, you may have some really old software that does not know that RBF exists, maybe because it's really old, and it might get confused if it's turned on by default.
So for those kind of systems you don't want to change things too quickly.
But I think it's been five years now so might be a good time to switch to default.

Aaron van Wirdum: 00:31:24

That should be enough time.

Sjors Provoost: 00:31:26

Well hopefully.

Aaron van Wirdum: 00:31:28

Okay, so would we expect more RBF transactions on the network now?

Sjors Provoost: 00:31:34

We'll have to see.
It depends on when people start using it.
My hope is no because my hope is that anybody who builds this kind of software already decided whether they want RBF on or off because it's just a default value.
You probably should already set that default to what you want it to be so that you're not surprised by this update.
So I hope to see no difference.

Sjors Provoost: 00:31:55

Because the worst-case scenario would be that some major company that has RBF turned off for some reason now suddenly turns it on and starts producing lots of RBF transactions confusing everybody in their ecosystem.

Aaron van Wirdum: 00:32:08

Yeah, it wouldn't really harm them in any way, would it?

Sjors Provoost: 00:32:12

I don't know, maybe people are using that service to send coins to some other service that does not like it when transactions are RBF.

Aaron van Wirdum: 00:32:20

Yeah that does not accept RBF transactions.

Sjors Provoost: 00:32:22

Or gets confused by them.

Aaron van Wirdum: 00:32:24

Yeah, these are out there.
Okay, makes sense.

Sjors Provoost: 00:32:28

So that's why you want to be a little bit slow with these command line tools to change them.

## Change Output

Aaron van Wirdum: 00:32:33

Right, okay, I think we've covered five points now and we got seven in total, so we got two more to go.

Sjors Provoost: 00:32:40

All right.

Aaron van Wirdum: 00:32:42

Number six.
The change output amounts are randomized.
It says that's what it says.

Sjors Provoost: 00:32:52

It's very cool.
Yeah, so basically this has to do I mean I don't know the precise change, but the general problem is that when you're looking at the blockchain, you can kind of guess which address is changed and which address is not changed if you have an assumption about how the wallet picks coins.
So if the wallet is very efficient, it will look for the smallest coin possible to spend and then it will create as little change as possible.
But that means that generally when you see two outputs to a transaction, the biggest one is probably the amount that's being sent and the smallest one is probably the change.

Aaron van Wirdum: 00:33:30

Well, is that necessarily true?
That's maybe true if there are several inputs, right?
That logic only holds up if there are several inputs, I think.

Sjors Provoost: 00:33:41

Or if there's one input.

Sjors Provoost: 00:33:44

Let's say you, well, if there is, depends on how much there is available, right?
But you're looking at the chain, so you don't know what was available.
But if your wallet is looking at a bag of coins, it might start with the smallest coin saying, nah, it's not big enough.
And then keep looking and then find one coin that's big enough.
And then use that to spend it.
And it doesn't really matter, but if you know what software the person was using based on some other fingerprinting aspects, you can start then.
You know how that software works, you know how that software does its coin selection, you can use that against the user.

Aaron van Wirdum: 00:34:17

Okay so do you know what algorithm Bitcoin Core was using up till now?

Sjors Provoost: 00:34:22

It's using a bunch of algorithms.

Aaron van Wirdum: 00:34:25

Oh several, and do you know which ones or no?

Sjors Provoost: 00:34:26

No, I should ask Murch.
He wrote a whole thesis on it and implemented a bunch of things.
One of them is-

Aaron van Wirdum: 00:34:31

But something changed.

Sjors Provoost: 00:34:33

I think originally the system was called the knapsack.
And I think the knapsack basically meant you just grabbed coins randomly and then see if it was enough.
And then if it wasn't, you try it again.
And then there was a new thing called branch and bound, which was a bit more smarter way to find coins.
And there's also the trying to find a single coin that is exactly the right value strategy.


Sjors Provoost: 00:34:57

There's a bunch of things that are happening.
It's a bit complicated.
But what this basically does is make it more difficult to tell which one is the input, sorry, which one is the change and which one is the destination.
And the way you do that is basically saying, well, rather than looking for the coin of the exact right size to spend, I'm going to look for a coin that is the amount that I need to spend plus two times the, yeah, I'm going to look for a coin that is at least three times, I guess, the amount that I'm trying to spend.

Aaron van Wirdum: 00:35:25

Right, so you want to spend one Bitcoin, so you're going to look for UTXO of three Bitcoins.

Sjors Provoost: 00:35:29

Yeah, except you're not going to do that.
You're going to say, I'm going to pick a number between the amount I want to spend and three times the amount I want to spend between one and three yeah and I'm gonna pick that number randomly right so that means sometimes the biggest sometimes you're gonna pick a very high number and so the change address will actually be the smaller will be the bigger output And sometimes I pick the lower random number and the change output will be the biggest amount.

Aaron van Wirdum: 00:35:53

Okay, so we're basically gonna keep using the algorithm that we were using, or at least, I don't know, but that's my assumption.

Sjors Provoost: 00:35:59

Yeah, I think that doesn't change.

Aaron van Wirdum: 00:36:01

However, we're now going to look for coins as if we're looking for one to three times more than what we are actually spending.

Sjors Provoost: 00:36:09

Exactly.
And that number is random.

Aaron van Wirdum: 00:36:10

That sounds interesting.
Doesn't that mean that you sometimes end up using more UTXOs than you would actually require?
In other words, wouldn't you make transactions bigger than they really need to be?

Sjors Provoost: 00:36:25

Yeah, I think that might mean that sometimes you are spending more coins than necessary.

Aaron van Wirdum: 00:36:31

Okay, so it's not optimizing for fees then or it's not also optimizing.

Sjors Provoost: 00:36:35

I don't think so but there may be some caveats in that code you'd have to read through it to see what exactly it's doing maybe there's some some protection against spending too much on fees.

Aaron van Wirdum: 00:36:44

Right Maybe it only works if this is not the case.


Sjors Provoost: 00:36:49

I mean, if you're using the GUI, you can also do your coin selection completely manually.
There is a little menu where you can see what your inputs are and just select which ones you want to spend.

Aaron van Wirdum: 00:36:58

So there might be trade-offs that we're not completely clear on, but the general idea is you're going to look for more coins than you actually need for privacy purposes.
That's ultimately the benefit, right?

Sjors Provoost: 00:37:09

Yeah. I suppose one day we should do an episode about coin selection.
This is also something I haven't specialized in.

Aaron van Wirdum: 00:37:14

Yeah, we should maybe.
That does sound like an interesting topic.
We can go over all of this.
Last point, Sjors.

## SendAll

Sjors Provoost: 00:37:23

Yeah, this one isn't super interesting.
It's a new RPC called `sendall`.
And so this is a command line tool.
And the name suggests that you're sending all your money.
That's not actually true.
You can use it to send all your money away to a different wallet, let's say if you're trying to migrate.
But you can also say, take these coins, so these specific input coins, and send them all to a specific destination.
This is stuff that you could already do because there was one command line tool called `sendmany` and `sendtoaddress`.
There basically were already calls to do this.

Aaron van Wirdum: 00:37:55

Yeah, also in the GUI this is already possible, right?

Sjors Provoost: 00:37:58

Yeah.
So the underlying motivation here is actually that there are different intentions that the user might have.
They might want to send an entire coin to an exchange for privacy reasons or they might want to send an exact amount to an exchange and in retrospect, you don't really know what the user intended so that creates problems when you try to bump the fee.
But also the code that actually implements this is a bit of a mess because it has all these different features.
So you can do all these different things for different use cases.
That means your code is full of if, then, else, if, if, else, else, if.
And so basically this is the first step to splitting that up to saying okay if you want to do this specific thing use the `sendall` method if you want to do this other thing use the send method and that's the first step to just you know at the command line it's easier to tell users to start using two different commands for two different things and then eventually I guess under the hood there will be some changes to the GUI to also use the separation.

Aaron van Wirdum: 00:38:52

I mean, this sounds like something that basically all wallets already do.

Sjors Provoost: 00:38:58

I don't know.
Like I said, it's not a new piece of functionality.

Aaron van Wirdum: 00:39:01

The insulting thing though, is that other wallets, the universally accepted term for this is send-max.

Sjors Provoost: 00:39:07

Yeah, but it's send-max given a set of coins.

Aaron van Wirdum: 00:39:12

That's also what send-max is I think or not?

Sjors Provoost: 00:39:14

I don't know yeah could be.

Aaron van Wirdum: 00:39:15

That's how I use it.
That's how I think about it.
No, but I get your point.
Okay, yeah, this was not the most exciting future of the seven, but I'm happy we covered it, Sjors.
Are you?

Sjors Provoost: 00:39:24

Last but not least.
Yeah, like I said, there's probably at least probably 500 or maybe a thousand individual changes that could each be worth their own episode if you were truly interested in how compilers work and whatever.

Aaron van Wirdum: 00:39:36

Well, we covered the highlights.
At least we covered our highlights.
I think so too.
And I think that makes for another successful episode, Sjors.

Sjors Provoost: 00:39:45

We'll see thank you for listening to Bitcoin

Aaron van Wirdum: 00:40:45

Explained.
