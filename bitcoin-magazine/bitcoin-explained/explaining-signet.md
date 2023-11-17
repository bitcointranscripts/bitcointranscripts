---
title: Explaining Signet
transcript_by: spraveenitpro via review.btctranscripts.com
media: https://www.youtube.com/watch?v=lGJaIbpf6bk
tags: ["signet"]
speakers: ["Sjors Provoost","Aaron Van Wirdum"]
categories: ["podcast"]
date: 2020-09-24
---

## intro

Speaker 0: 00:00:07

Live from Utrecht, this is the fan weirdum Sjoerds Nedo. Hello! Sjoerds, welcome.

Speaker 1: 00:00:12

Thank you. It's good to be back. Well, I never left, but...

Speaker 0: 00:00:15

Yeah, well, we're at your home now, so you never left, I think.

Speaker 1: 00:00:18

Well, we are...

Speaker 0: 00:00:19

You probably literally never left because of corona

Speaker 1: 00:00:21

exactly we're at my secret location how

Speaker 0: 00:00:25

are you enjoying the second wave

Speaker 1: 00:00:26

it's amazing

Speaker 0: 00:00:28

it is it is happening isn't it

Speaker 1: 00:00:30

yeah it's clearly happening we've crossed every threshold value there is

Speaker 0: 00:00:34

now it's just waiting for things to get worse

Speaker 1: 00:00:37

yeah I mean the amazing measure after three weeks of warnings that was taken was to close bars like one hour earlier that's not gonna do it yeah

Speaker 0: 00:00:46

it was like the R value was way too high so now they made a very strict measure of closing bars one hour early.

Speaker 1: 00:00:53

Yeah which I'm sure will reduce.

Speaker 0: 00:00:54

Nothing's gonna change obviously.

Speaker 1: 00:00:56

Well yeah but the number still keeps going up so eventually there's probably going to be some sort of lockdown? Because the difference between now and the last time is the last time the numbers were bad and everybody was worried and now the numbers are bad and nobody's worried.

Speaker 0: 00:01:10

Yeah. Are you expecting a real full-blown lockdown this time in the Netherlands?

Speaker 1: 00:01:15

Well, we never had one. I don't know. I think it will be more strict than last time, but I don't think it'll be Australian style.

Speaker 0: 00:01:22

Right. Yeah. So anyways, this episode is not about Corona. Nope. This episode is about SIGNET. Indeed, SIGNET. So SIGNET. So this is a new version of testnet. So let's start with testnet.

Speaker 1: 00:01:34

Yeah, or start with mainnet.

Speaker 0: 00:01:37

Are you going to explain everything about mainnet now first?

Speaker 1: 00:01:39

No, just to point out that

## Explaining the diff between testnet and the real Bitcoin network technically.

in the early days Bitcoin was practically worthless, so you could just test everything on production.

Speaker 0: 00:01:46

Okay.

Speaker 1: 00:01:47

And now that Bitcoin is not worthless, you know, you don't want to test things on production. In general, you do not want to test things on production. So there's this additional network that is identical to Bitcoin and that's called Testnet.

Speaker 0: 00:02:00

Yeah, it's basically a clone of mainnet which was created I think by, I think Gavin and Driesen created this back in, what would have been 2011, 12, 13? Probably before, I don't know.

Speaker 1: 00:02:13

But it was designed to be worthless, but of course some people are idiots, so they started trading it. Because, you know, it's probably better than any altcoin.

Speaker 0: 00:02:21

Right, because it's just Bitcoin.

Speaker 1: 00:02:24

Well, Bitcoin with a few gotchas. I think the main gotcha is that if nobody mines a block, the difficulty goes back down, so that anyone can mine a block again.

Speaker 0: 00:02:33

Oh, the difficulty adjusts faster on testnet?

Speaker 1: 00:02:36

Yeah, there's basically after 20 minutes and what we would now call emergency difficulty adjustment, which just basically sets the difficulty right back to zero or whatever the lowest number

Speaker 0: 00:02:46

is. Right, right, right.

Speaker 1: 00:02:48

So what you see is usually 20 minutes, nothing, and then all of a sudden, one block comes in or a whole series of block comes in.

Speaker 0: 00:02:55

And that just resets difficulty to one? Difficulty to one?

Speaker 1: 00:02:58

Exactly, and the problem is that some joker with a big ASIC miner mines a bunch of blocks on testnet and creates really high difficulty because the difficulty keeps adjusting up and then they just go away. And nobody can mine a block anymore. But after 20 minutes it goes back.

Speaker 0: 00:03:15

So first of all, I think what you were going to say, but I'm not sure, is that the thing about testnet is

## Aaron and Sjors explain whats wrong with testnet

that it's not supposed to have any value. And then if for some reason it does get value, like some people start trading it and hoarding it and holding it, then actually the whole testnet is just reset because people are really punished in a way for giving it value.

Speaker 1: 00:03:35

Yeah, I think that happened once or twice. The current testnet is called testnet3.

Speaker 0: 00:03:39

Right, so just to make sure that it has no value, that's the whole point of having this network. It should have no value so people can use it to test stuff on.

Speaker 1: 00:03:48

That's right.

Speaker 0: 00:03:48

Okay, so then the problem is, and that was the other thing you were explaining, is that this network, this test network, because it has no value, there's no real incentive and mining economy around hash power, and therefore it's unstable. So sometimes blocks are, like you mentioned, mined very fast and all of a sudden you have, you have a whole bunch of blocks and then this ASIC clown leaves and then there's no blocks for a while and it's unstable and this does not make for an ideal test environment.

Speaker 1: 00:04:24

There's other problems like you might have a reorg of 15,000 blocks, which is not realistic, or I think in the beginning, SegWit blocks didn't get mined. I don't even think it was censorship, it was just nobody was bothering.

Speaker 0: 00:04:38

Right.

Speaker 1: 00:04:39

So all these kind of problems, yeah,

Speaker 0: 00:04:41

it's time

Speaker 1: 00:04:41

to get rid of it. So you have- Well, not to get rid of it, but time to have something else as well.

Speaker 0: 00:04:45

Yeah, so you have a proof-of-work chain without all the benefits of proof of work.

Speaker 1: 00:04:51

Yeah it's basically the worst of both worlds. It's all the downsides of proof-of-work because you do need to you know have it but you just you don't have the incentives that go with it so it's just a mess.

Speaker 0: 00:05:00

It's a messy test environment. There is another sort of... So what's RekNet? Is that what it's called? RekTest?

Speaker 1: 00:05:07

Yeah RekTest. So basically regression testing there is another version that you can spin up that's called regtest

Speaker 0: 00:05:14

it's version of testnet

Speaker 1: 00:05:16

it's testnet ish but it's a different kind of network. So Bitcoin Core defines three types of networks, mainnet, testnet, and regtest. And the last one...

Speaker 0: 00:05:25

Just to be clear about this, because this is maybe slightly interesting for someone who... I wasn't even sure about this. So Bitcoin Core actually embeds this stuff. Bitcoin Core embeds testnet. There's like an option in Bitcoin Core to use testnet.

Speaker 1: 00:05:39

Yeah, you launch Bitcoin Core with dash testnet.

Speaker 0: 00:05:42

Right, so you download the Bitcoin Core software and then you can choose mainnet or testnet. Or regtest. Or regtest, which you're gonna explain now.

Speaker 1: 00:05:50

And so I think the biggest difference with regtest is that it has no difficulty adjustment.

Speaker 0: 00:05:55

Okay.

Speaker 1: 00:05:55

Or something like that. Is that the biggest? Basically the use case for that is you run a test on your own computer. So Bitcoin Core has a whole bunch of tests. Right. And those tests actually spin up a node that really produces blocks and re-orgs and makes transactions and rejects transactions and all these things. But you don't want to have this huge CPU waste when you're running your tests to have this difficulty. So I think they're all just trivially easy.

Speaker 0: 00:06:19

But it's only on your own computer, this one. You're not sharing it with other people.

Speaker 1: 00:06:24

Yeah, not necessarily, but in practice, that's how you use it. You spin up a bunch of nodes on your own computer. Now in principle, they're nodes, so they can run all over the network but the problem then is because anybody can create blocks you can just wipe out each other's chains and it wouldn't be very suitable to use with between different people on different networks it's not ideal for that.

Speaker 0: 00:06:44

It's even worse than testnet for that. Yeah. Right. Okay so we have testnet that's instable, we have Racktest that's even more unstable especially if you use it with other people, but a bit better probably if you use it on your own. But we're looking for something better.

Speaker 1: 00:06:59

Yes. And so we want

Speaker 0: 00:07:00

something better or not sure.

Speaker 1: 00:07:02

I would like something better.

Speaker 0: 00:07:03

That's what I thought. I don't really care either way, I'm not a developer, but for you, you want something better for sure.

Speaker 1: 00:07:10

Yes, it's nice to be able to develop on something and try it with other people. So when you're working with other people, it's nice to have perhaps an explorer somewhere that you can point to, a faucet somewhere, some, you know, maybe somebody takes care of occasional re-orgs, so you can write software that you know every day or every hour, it's gonna be three block re-org, and you can just make sure your software actually handles that. Always kind of things you can do. So testnet is, or sorry, SIGNET is...

Speaker 0: 00:07:38

Yeah, so SIGNET is the new testnet.

Speaker 1: 00:07:40

It's not the new testnet, it's another form.

Speaker 0: 00:07:43

It's a new testnet. Yeah. Okay, so the new Bitcoin, if you download Bitcoin Core, once there's a Bitcoin core software release that has this implemented then you have four options so you have Bitcoin mainnet you have Bitcoin testnet you have Bitcoin rack test and now you have another option which is Bitcoin SIGNET.

Speaker 1: 00:08:03

That's right. Cool.

Speaker 0: 00:08:04

Yeah what is SIGNET?

Speaker 1: 00:08:05

So

## Sjors explains how Signet solves some of the issues with test net.

SIGNET is signed essentially. So what happens is and it's completely centralized. Every block is signed. And well

Speaker 0: 00:08:14

every block must be signed for it to be valid.

Speaker 1: 00:08:16

Correct. So when you receive a new block, you check the proof of work, but that can be trivially low and then...

Speaker 0: 00:08:23

Right, it still has proof of work as well.

Speaker 1: 00:08:25

It does, yes.

Speaker 0: 00:08:26

And then you need a valid signature on top of the proof of work for the block to be valid.

Speaker 1: 00:08:31

Correct.

Speaker 0: 00:08:31

Plus of course the rest of the block needs to be valid like always all the transactions. Okay so

Speaker 1: 00:08:37

the signature is included in in one of the Coinbase transactions or in the Coinbase transaction as one of the outputs. I see. Basically what you do is you create a block and then you add the signature to it and then you start grinding to find a proof of work.

Speaker 0: 00:08:53

Right.

Speaker 1: 00:08:53

And there's a couple of fields you cannot change when you do that. But in principle, you know, you can try a couple of nonces and then you sign again and you try some other nonces. Right.

Speaker 0: 00:09:03

And

Speaker 1: 00:09:03

eventually you mine a block. So that's all the same.

Speaker 0: 00:09:05

So who's creating the signature?

Speaker 1: 00:09:07

So the idea is that there can be more than one SIGNET, so we'll get into that, but in this case, the main SIGNET, the default SIGNET, is probably a better way to say it, is checked by a one of two multi-sig. So a SIGNET can have any arbitrary rules for what the block should be signed with,

Speaker 0: 00:09:24

and

Speaker 1: 00:09:24

the rule that's picked for the main one is a one out of two multi-sig. So there are two public keys out there, And I think, yeah, it's this close on the list. So it's Kalle Alm and AJ Towns. They have either of the keys. So if one of their computers disappears, Signet will go on. But it's very clearly very centralized in this sense. So they sign the block and then it's fine. And they sign one every 10 minutes.

Speaker 0: 00:09:51

One of them signs one every 10 minutes.

Speaker 1: 00:09:54

Exactly.

Speaker 0: 00:09:54

Right, so you know for sure. And the other

Speaker 1: 00:09:55

one just stands by if one of

Speaker 0: 00:09:57

them goes away. Just in case. Yeah. Right, so you know for sure there's gonna be one block every 10 minutes, so that makes it stable?

Speaker 1: 00:10:03

That's the idea. And because they can both agree not to annoy each other with increasing the difficulty, you won't have that kind of problems.

Speaker 0: 00:10:13

Right.

Speaker 1: 00:10:13

Now, it's just a SIGNET. It's a default that Bitcoin Core will ship with, but you have a simple parameter that you can start Bitcoin Core with to find any other SIG net. So anybody can create their own super centralized SIG net. That's kind of the trade-off. And they can have arbitrary conditions. So you could have, especially with Taproot, a 1000 out of 300,000 multi-sig weird construction that could be valid too for a signet there's probably no reason to do it it's probably enough to just have a one of two or one of three

Speaker 0: 00:10:44

right you can use it to test your new software or whatever you're testing. I would imagine that because of this structure, wouldn't it also make it unsuited to test certain stuff? I'm just thinking out loud here, but if you want to test something proof-of-work related or something like that, I can imagine that it's actually getting in the way as well sometimes or not.

Speaker 1: 00:11:07

I would say you can test whatever you want, because it still has proof-of-work. So you could have a one-of-two signature and one of the two could increase the work, could just start mining with more work. And so triggering reorgs that way.

Speaker 0: 00:11:21

Are there any trade-offs or downsides then to Cygnet or do you think it's just strictly better than testnet?

Speaker 1: 00:11:27

Well, it's extremely centralized, the default Cygnet, but because everybody can make their own signet that's kind of not an issue either

Speaker 0: 00:11:35

yeah so plus it's just for testing anyways and it's valueless anyways

Speaker 1: 00:11:39

exactly so I don't see any downside I also don't see any no reason to get rid of testnet but this is just an option you have. And yeah, so Kalle says hello. I talked to him earlier today.

Speaker 0: 00:11:52

Hello.

Speaker 1: 00:11:53

And one of the things he pointed out is that you can test soft forks with this pretty easily by just shipping a new version of the Signet code, or running your own branch of the Signet code, your own Bitcoin Core branch, which happens to check that soft fork, whereas others can simply ignore the soft fork. Right. So let's say they do an update that has taproot in it, and they say, well, as of SIGNET block 1000, taproot is now activated. And so if you run the old version of SIGNET code, the one that's in Bitcoin Core now, you'll just ignore it because this is off work.

Speaker 0: 00:12:35

Yeah, well you'll still follow the chain, you'll still be fine with it, you're just not enforcing.

Speaker 1: 00:12:41

You're not checking any

Speaker 0: 00:12:42

of the taproot rules. Yes, exactly.

Speaker 1: 00:12:43

But if you have that version you will check the Taproot rules. And now what if Taproot rules are changed? Because it's still work in progress so the consensus rules around Taproot might change, right? Or there could be a bug in the first implementation. Well it's very simple. You ship a new version of this Taproot Signet code and you activate it later. So you basically say well now we activate taproot at block 2000 and anything before that is ignored. So that means you can have a single signet chain that everybody can point to that can have all sorts of soft forks going on at the same time and it's not really bothering anybody else. So it's kind of nice because with testnet you really, I guess you can do the same on testnet but yeah.

Speaker 0: 00:13:29

All right any other benefits? What else do our listeners need to know

## The main benefits of signet.

about Signet? I think

Speaker 1: 00:13:33

the main benefit is that you can run your own if you have some sort of, you know, a large operation and you want to test all sorts of scenarios. If you want to test re-ORGs, then you can either ask, you know, some of the current Signet operators to do reworks for you or you can run your own Signet and have reworks on it and if you you want to be cool and you want to do 10,000 block reworks then you can do that you know and you can have other people join in you can spin up an explorer and people can point to it.

Speaker 0: 00:14:02

All right.

Speaker 1: 00:14:03

So I think it's pretty cool, but it's not like life changing or anything.

Speaker 0: 00:14:07

It's been in development for a while, right?

Speaker 1: 00:14:09

Correct, and there's actually already, it's already used in Sea Lightning. So you can use an older version of Signet inside of Sea Lightning.

Speaker 0: 00:14:17

Okay.

Speaker 1: 00:14:18

But they changed the Genesis block again a couple times. So CLightning will be updated, I think, to have the new version of it.

Speaker 0: 00:14:25

Right.

Speaker 1: 00:14:26

And so that's nice. You can test Lightning stuff on a Cygnet, which is, you know, it's interesting because you want to have multiple nodes with weird latency all over the world and Cygnet is a nice thing for that. Testnet is absolutely horrible for for lightning because if you get a 15,000 block re-org you know your channels just blow up.

Speaker 0: 00:14:42

Yeah okay so and this was merged into Bitcoin Core last week or something like that?

Speaker 1: 00:14:48

A few days ago.

Speaker 0: 00:14:49

And that means it will be included in the next Bitcoin Core release? Yep. Which is scheduled for

Speaker 1: 00:14:54

a couple months from now? This fall.

Speaker 0: 00:14:57

This fall. All right. Sjoerd, anything else we need to discuss about Cygnet? Or is that it?

Speaker 1: 00:15:04

No, I think it's a pretty brief one.

Speaker 0: 00:15:06

Yeah, great. I like brief ones.

Speaker 1: 00:15:10

All right, so thank you for listening to the Van Weerdum Sjoerds' NATO. There you go. Music

Speaker 0: 00:15:17

music music music music
