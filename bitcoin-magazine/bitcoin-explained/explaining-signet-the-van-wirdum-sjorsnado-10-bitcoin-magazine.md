---
title: "Explaining Signet"
transcript_by: sir-oro via review.btctranscripts.com
media: https://www.youtube.com/watch?v=lGJaIbpf6bk
tags: ["signet"]
speakers: ["Sjors Provoost","Aaron van Wirdum"]
categories: ["podcast"]
date: 2020-09-25
---
## Intro

Aaron van Wirdum: 00:00:07

Live from Utrecht, this is the Van Wirdum Sjorsnedo.
Hello! Sjors, welcome.

Sjors Provoost: 00:00:12

Thank you.
It's good to be back.
Well, I never left, but...

Aaron van Wirdum: 00:00:15

Yeah, well, we're at your home now, so you never left, I think.
You probably literally never left because of corona

Sjors Provoost: 00:00:21

Exactly we're at my secret location

Aaron van Wirdum: 00:00:25

How are you enjoying the second wave?

Sjors Provoost: 00:00:26

It's amazing

Aaron van Wirdum: 00:00:28

It is happening isn't it?

Sjors Provoost: 00:00:30

Yeah it's clearly happening we've crossed every threshold value there is.

Aaron van Wirdum: 00:00:34

Now it's just waiting for things to get worse

Sjors Provoost: 00:00:37

Yeah I mean the amazing measure after three weeks of warnings that was taken was to close bars like one hour earlier, that's not gonna do it, so...

Aaron van Wirdum: 00:00:46

Yeah, it was like the R value was way too high, so now they made a very strict measure of closing bars one hour early.

Sjors Provoost: 00:00:53

Yeah which I'm sure will reduce.

Aaron van Wirdum: 00:00:54

Nothing's gonna change obviously.

Sjors Provoost: 00:00:56

Well yeah but the number still keeps going up so eventually there's probably going to be some sort of lockdown.
Because the difference between now and the last time is the last time the numbers were bad and everybody was worried and now the numbers are bad and nobody's worried.

Aaron van Wirdum: 00:01:10

Yeah.
Are you expecting a real full-blown lockdown this time in the Netherlands?

Sjors Provoost: 00:01:15

Well, we never had one.
I don't know.
I think it will be more strict than last time, but I don't think it'll be Australian style.

Aaron van Wirdum: 00:01:22

Right.
Yeah.
So anyways, this episode is not about Corona.
Nope.
This episode is about Signet.

Sjors Provoost: 00:01:29

Indeed, Signet.

## Explaining the difference between Testnet and the real Bitcoin network technically.

Aaron van Wirdum: 00:01:30

So Signet.
So this is a new version of Testnet.
So let's start with Testnet.

Sjors Provoost: 00:01:34

Yeah, or start with Mainnet.

Aaron van Wirdum: 00:01:37

Are you going to explain everything about Mainnet now first?

Sjors Provoost: 00:01:39

No, just to point out that in the early days Bitcoin was practically worthless, so you could just test everything on production.

Aaron van Wirdum: 00:01:46

Okay.

Sjors Provoost: 00:01:47
And now that Bitcoin is not worthless, you know, you don't want to test things on production.
In general, you do not want to test things on production.
So there's this additional network that is identical to Bitcoin and that's called Testnet.

Aaron van Wirdum: 00:02:00

Yeah, it's basically a clone of Mainnet which was created I think by, I think Gavin Andresen created this back in, what would have been 2011, 12, 13?
Probably before, I don't know.

Sjors Provoost: 00:02:13

But it was designed to be worthless, but of course some people are idiots, so they started trading it.
Because, you know, it's probably better than any altcoin.

Aaron van Wirdum: 00:02:21

Right, because it's just Bitcoin.

Sjors Provoost: 00:02:24

Well, Bitcoin with a few gotchas.
I think the main gotcha is that if nobody mines a block, the difficulty goes back down, so that anyone can mine a block again.

Aaron van Wirdum: 00:02:33

Oh, the difficulty adjusts faster on Testnet?

Sjors Provoost: 00:02:36

Yeah, there's basically after 20 minutes what we would now call emergency difficulty adjustment, which just basically sets the difficulty right back to zero or whatever the lowest number is.

Aaron van Wirdum: 00:02:46

Right, right, right.

Sjors Provoost: 00:02:48

So what you see is usually 20 minutes, nothing, and then all of a sudden, one block comes in or a whole series of block comes in.

Aaron van Wirdum: 00:02:55

And that just resets difficulty to one?

Sjors Provoost: 00:02:58

Exactly, and the problem is that some joker with a big ASIC miner mines a bunch of blocks on Testnet and creates really high difficulty because the difficulty keeps adjusting up and then they just go away.
And nobody can mine a block anymore.
But after 20 minutes it goes back.

## Aaron and Sjors explain what's wrong with Testnet

Aaron van Wirdum: 00:03:15

So first of all, I think what you were going to say, but I'm not sure, is that the thing about Testnet is that it's not supposed to have any value.
And then if for some reason it does get value, like some people start trading it and hoarding it and holding it, then actually the whole Testnet is just reset because people are really punished in a way for giving it value.

Sjors Provoost: 00:03:35

Yeah, I think that happened once or twice.
The current Testnet is called Testnet3.

Aaron van Wirdum: 00:03:39

Right, so just to make sure that it has no value, that's the whole point of having this network.
It should have no value so people can use it to test stuff on.

Sjors Provoost: 00:03:48

That's right.

Aaron van Wirdum: 00:03:48

Okay, so then the problem is, and that was the other thing you were explaining, is that this network, this test network, because it has no value, there's no real incentive and mining economy around hash power, and therefore it's unstable.
So sometimes blocks are, like you mentioned, mined very fast and all of a sudden you have, you have a whole bunch of blocks and then this ASIC clown leaves and then there's no blocks for a while and it's unstable and this does not make for an ideal test environment.

Sjors Provoost: 00:04:24

There's other problems like you might have a reorg of 15,000 blocks, which is not realistic, or I think in the beginning, SegWit blocks didn't get mined.
I don't even think it was censorship, it was just nobody was bothering.

Aaron van Wirdum: 00:04:38

Right.

Sjors Provoost: 00:04:39

So all these kind of problems, yeah, it's time to get rid of it.
Well, not to get rid of it, but time to have something else as well.

Aaron van Wirdum: 00:04:45

Yeah, so you have a proof-of-work chain without all the benefits of proof-of-work.

Sjors Provoost: 00:04:51

Yeah it's basically the worst of both worlds.
It's all the downsides of proof-of-work because you do need to you know have it but you just you don't have the incentives that go with it so it's just a mess.

Aaron van Wirdum: 00:05:00

It's a messy test environment.
So what's Regnet?
Is that what it's called?
Regtest?

Sjors Provoost: 00:05:07

Yeah, Regtest.
So basically regression testing.
There is another version that you can spin up that's called Regtest

Aaron van Wirdum: 00:05:14

It's version of Testnet

Sjors Provoost: 00:05:16

It's Testnet-ish but it's a different kind of network.
So Bitcoin Core defines three types of networks: Mainnet, Testnet, and Regtest.
And the last one...

Aaron van Wirdum: 00:05:25

So, just to be clear about this, because this is maybe slightly interesting for someone who...
I wasn't even sure about this.
So Bitcoin Core actually embeds this stuff.
Bitcoin Core embeds Testnet.
There's like an option in Bitcoin Core to use Testnet.

Sjors Provoost: 00:05:39

Yeah, you launch Bitcoin Core with "-testnet".

Aaron van Wirdum: 00:05:42

Right, so you download the Bitcoin Core software and then you can choose Mainnet or Testnet.

Sjors Provoost: 00:05:48

Or Regtest.

Aaron van Wirdum: 00:05:49

Or Regtest, which you're gonna explain now.

Sjors Provoost: 00:05:50

And so I think the biggest difference with Regtest is that it has no difficulty adjustment.
Or something like that.

Aaron van Wirdum: 00:05:55

Okay. Is that the biggest?

Sjors Provoost: 00:05:55

Basically the use case for that is you run a test on your own computer.
So Bitcoin Core has a whole bunch of tests.
And those tests actually spin up a node that really produces blocks and reorgs and makes transactions and rejects transactions and all these things.
But you don't want to have this huge CPU waste when you're running your tests to have this difficulty.
So I think they're all just trivially easy.

Aaron van Wirdum: 00:06:19

But it's only on your own computer, this one.
You're not sharing it with other people.

Sjors Provoost: 00:06:24

Yeah, not necessarily, but in practice, that's how you use it.
You spin up a bunch of nodes on your own computer.
Now in principle, they're nodes, so they can run all over the network but the problem then is because anybody can create blocks you can just wipe out each other's chains and it wouldn't be very suitable to use with between different people on different networks it's not ideal for that.

Aaron van Wirdum: 00:06:44

It's even worse than Testnet for that.
Okay so we have Testnet that's unstable, we have Regtest that's even more unstable especially if you use it with other people, but a bit better probably if you use it on your own.
But we're looking for something better.

Sjors Provoost: 00:06:59

Yes.

Aaron van Wirdum: 00:07:00

We want something better or not Sjors?.

Sjors Provoost: 00:07:02

I would like something better.

Aaron van Wirdum: 00:07:03

That's what I thought.
I don't really care either way, I'm not a developer, but for you, you want something better for sure.

Sjors Provoost: 00:07:10

Yes, it's nice to be able to develop on something and try it with other people.
So when you're working with other people, it's nice to have perhaps an explorer somewhere that you can point to, a faucet somewhere, some, you know, maybe somebody takes care of occasional reorgs, so you can write software that you know every day or every hour, it's gonna be three block re-org, and you can just make sure your software actually handles that.
Always kind of things you can do.

Aaron van Wirdum: 00:07:38

So Signet is the new Testnet.

Sjors Provoost: 00:07:40

It's not the new Testnet, it's another form.

Aaron van Wirdum: 00:07:43

It's a new Testnet.
Okay, so once there's a Bitcoin core software release that has this implemented then you have four options. So you have Bitcoin Mainnet you have Bitcoin Testnet, you have Bitcoin Regtest and now you have another option which is Bitcoin Signet.

Sjors Provoost: 00:08:03

That's right.

## Sjors explains how Signet solves some of the issues with Testnet

Aaron van Wirdum: 00:08:04

Yeah what is Signet?

Sjors Provoost: 00:08:05

Signet is signed essentially and it's completely centralized.
Every block is signed.

Aaron van Wirdum: 00:08:14

Every block must be signed for it to be valid.

Sjors Provoost: 00:08:16

Correct.
So when you receive a new block, you check the proof-of-work, but that can be trivially low and then...

Aaron van Wirdum: 00:08:23

Right, it still has proof-of-work as well.

Sjors Provoost: 00:08:25

It does, yes.

Aaron van Wirdum: 00:08:26

And then you need a valid signature on top of the proof-of-work for the block to be valid.

Sjors Provoost: 00:08:31

Correct.

Aaron van Wirdum: 00:08:31

Plus of course the rest of the block needs to be valid like always all the transactions.

Sjors Provoost: 00:08:37

The signature is included in in one of the Coinbase transactions or in the Coinbase transaction as one of the outputs.
Basically what you do is you create a block and then you add the signature to it and then you start grinding to find a proof-of-work.
And there's a couple of fields you cannot change when you do that.
But in principle, you know, you can try a couple of nonces and then you sign again and you try some other nonces.

Sjors Provoost: 00:09:03

Eventually you mine a block.
So that's all the same.

Aaron van Wirdum: 00:09:05

So who's creating the signature?

Sjors Provoost: 00:09:07

So the idea is that there can be more than one Signet, so we'll get into that, but in this case, the main Signet, the default Signet, is probably a better way to say it, is checked by a **one of two multi-sig**.
So a Signet can have any arbitrary rules for what the block should be signed with, and the rule that's picked for the main one is a one out of two multi-sig.
So there are two public keys out there, and I think, yeah, it's disclosed on the list.
So it's Kalle Alm and AJ Towns.
They have either of the keys.
So if one of their computers disappears, Signet will go on.
But it's very clearly very centralized in this sense.
So they sign the block and then it's fine.
And they sign one every 10 minutes.

Aaron van Wirdum: 00:09:51

One of them signs one every 10 minutes.

Sjors Provoost: 00:09:54

Exactly.
And the other one just stands by if one of them goes away.

Aaron van Wirdum: 00:09:57

Just in case.
Right, so you know for sure there's gonna be one block every 10 minutes, so that makes it stable?

Sjors Provoost: 00:10:03

That's the idea.
And because they can both agree not to annoy each other with increasing the difficulty, you won't have that kind of problems.

Aaron van Wirdum: 00:10:13

Right.

Sjors Provoost: 00:10:13

Now, it's just a Signet.
It's the default that Bitcoin Core will ship with, but you have a simple parameter that you can start Bitcoin Core with to find any other Signet.
So anybody can create their own super centralized Signet.
That's kind of the trade-off.

And they can have arbitrary conditions.
So you could have, especially with Taproot, a 1000 out of 300000 multi-sig weird construction that could be valid too for a Signet there's probably no reason to do it it's probably enough to just have a one of two or one of three.

Aaron van Wirdum: 00:10:44

Right, you can use it to test your new software or whatever you're testing.
I would imagine that because of this structure, wouldn't it also make it unsuited to test certain stuff?
I'm just thinking out loud here, but if you want to test something proof-of-work related or something like that, I can imagine that it's actually getting in the way as well sometimes or not?

Sjors Provoost: 00:11:07

I would say you can test whatever you want, because it still has proof-of-work.
So you could have a one-of-two signature and one of the two could increase the work, could just start mining with more work.
And so triggering reorgs that way.

Aaron van Wirdum: 00:11:21

Are there any trade-offs or downsides then to Signet or do you think it's just strictly better than Testnet?

Sjors Provoost: 00:11:27

Well, it's extremely centralized, the default Signet, but because everybody can make their own Signet that's kind of not an issue either

Aaron van Wirdum: 00:11:35

Yeah, plus it's just for testing anyways and it's valueless anyways

Sjors Provoost: 00:11:39

Exactly, so I don't see any downside.
I also don't see any reason to get rid of Testnet but this is just an option you have.
And yeah, so Kalle says "Hello".
I talked to him earlier today.

Aaron van Wirdum: 00:11:52

Hello.

Sjors Provoost: 00:11:53

And one of the things he pointed out is that you can test soft forks with this pretty easily by just shipping a new version of the Signet code, or running your own branch of the Signet code, your own Bitcoin Core branch, which happens to check that soft-fork, whereas others can simply ignore the soft fork.
So let's say they do an update that has Taproot in it, and they say, well, as of Signet block 1000, taproot is now activated.
And so if you run the old version of Signet code, the one that's in Bitcoin Core now, you'll just ignore it because this is a soft-fork.

Aaron van Wirdum: 00:12:35

Yeah, well you'll still follow the chain, you'll still be fine with it, you're just not enforcing.

Sjors Provoost: 00:12:41

You're not checking any of the Taproot rules.
But if you have that version you will check the Taproot rules.
And now what if Taproot rules are changed?
Because it's still work in progress so the consensus rules around Taproot might change, right?
Or there could be a bug in the first implementation.
Well it's very simple.
You ship a new version of this Taproot Signet code and you activate it later.
So you basically say well now we activate Taproot at block 2000 and anything before that is ignored.
So that means you can have a single Signet chain that everybody can point to that can have all sorts of soft forks going on at the same time and it's not really bothering anybody else.
So it's kind of nice because with Testnet you really, I guess you can do the same on Testnet but yeah.

## The main benefits of Signet

Aaron van Wirdum: 00:13:29

All right, any other benefits?
What else do our listeners need to know about Signet?

Sjors Provoost: 00:13:33

I think the main benefit is that you can run your own if you have some sort of, you know, a large operation and you want to test all sorts of scenarios.
If you want to test reorgs, then you can either ask, you know, some of the current Signet operators to do reorg for you or you can run your own Signet and have reorgs on it, and if you want to be cool and you want to do 10000 block reworks then you can do that.
And you can have other people join and you can spin up an explorer and people can point to it.

Aaron van Wirdum: 00:14:02

All right.

Sjors Provoost: 00:14:03

So I think it's pretty cool, but it's not like life changing or anything.

Aaron van Wirdum: 00:14:07

It's been in development for a while, right?

Sjors Provoost: 00:14:09

Correct, and it's already used in C-Lightning.
So you can use an older version of Signet inside of C-Lightning.

Aaron van Wirdum: 00:14:17

Okay.

Sjors Provoost: 00:14:18

But they changed the Genesis block again a couple times.
So C-Lightning will be updated, I think, to have the new version of it.
And so that's nice.
You can test Lightning stuff on a Signet, which is, you know, it's interesting because you want to have multiple nodes with weird latency all over the world and Signet is a nice thing for that.
Testnet is absolutely horrible for for lightning because if you get a 15000 block reorg you know your channels just blow up.

Aaron van Wirdum: 00:14:42

Yeah okay so and this was merged into Bitcoin Core last week or something like that?

Sjors Provoost: 00:14:48

A few days ago.

Aaron van Wirdum: 00:14:49

And that means it will be included in the next Bitcoin Core release?

Sjors Provoost: 00:14:52

Yep.

Aaron van Wirdum: 00:14:53

Which is scheduled for a couple months from now?

Sjors Provoost: 00:14:56

This fall.

Aaron van Wirdum: 00:14:57

This fall.
All right.
Sjors, anything else we need to discuss about Signet?
Or is that it?

Sjors Provoost: 00:15:04

No, I think it's a pretty brief one.

Aaron van Wirdum: 00:15:06

Yeah, great.
I like brief ones.

Sjors Provoost: 00:15:10

All right, so thank you for listening to the Van Wirdum Sjorsnado.

Aaron van Wirdum: 00:15:17

There you go.
