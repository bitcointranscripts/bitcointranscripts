---
title: 'DATUM: Decentralizing Bitcoin Mining Through Sovereign Block Template Creation'
transcript_by: 'muchai254 via review.btctranscripts.com'
media: 'https://youtu.be/FJ0Hye52Ib8'
date: '2025-05-07'
tags:
  - 'mining'
  - 'pooled-mining'
  - 'stratum-v2'
  - 'scalability'
  - 'security'
  - 'btcplusplus'
speakers:
  - 'Jason Hughes'
categories:
  - 'conference'
source_file: 'https://youtu.be/FJ0Hye52Ib8'
summary: 'Jason Hughes (VP of Engineering at Motion Mining, creator of DATUM at Ocean) presents a deep dive into DATUM — Decentralized Alternative Templates for Universal Mining — an MIT-licensed, C-based protocol that lets individual miners build their own block templates and submit blocks directly to the network while still earning pooled rewards, built from scratch rather than on Stratum V2 due to SV2''s decade of development with no decentralized adoption, its centralized design assumptions, and firmware-level coinbase size constraints that SV2 does not handle; the talk covers the Datum Gateway''s Stratum V1 server, its encrypted handshake with Datum Prime via libsodium, the CoinBaser command for non-custodial payout list negotiation, backwards proof-of-work validation, spot-check template integrity, and the aggregation benefits that cut bandwidth from 200 GB/day for 8,000 direct connections to roughly 8 GB/day, with over 200 mainnet blocks already mined by the software as of the talk.'
---
## Introduction & Agenda

Jason Hughes: 00:00:00

I will preface this with I do not usually do these things.
We will see how this goes, and I will do my best to get through this and make sure everybody learns something in the process.
I am Jason from OCEAN, like you said.
I created DATUM, and we are going to just kind of dive into what that is, why it is, and how it works.
We will go from there.
If anybody wants my PGP key, feel free to snap a shot of that.
And that's the one I pretty much use for everything important.
If you need to get a hold of me, you can use that email.
That email works for whatever.
I've got a little bit of an agenda.
We'll go through some introductions of things and kind of what DATUM is.
Why not SV2?
That's probably the biggest question that we get when we talk about DATUM.
And why C and not Rust or something else?
I mean, those are kind of elephants in the room that we need to touch on.
And then how did we start on DATUM?
Like, where did it begin and what did it start as?
And then what did it become, and how did it evolve into what it is now?
So there's our rough agenda.
Nothing too crazy.
I'm happy to take questions throughout.
If there's anything that I'm not explaining clearly, just kind of raise your hand.
I'll call on people.
I'm cool.
We'll see what we can do.
We'll save some time for like pure Q&A at the end, but obviously if there's something that you just want to touch on now, I'm not going to stop you.
Oops.
All right.

## Jason Hughes' Background in Bitcoin Mining

Jason Hughes: 00:01:28

So who am I?
I don't go to these conferences that often, so most people here don't recognize me.
I'm Jason Hughes.
I was known in the BitcoinTalk and whatnot as WizKid057.
I kind of dropped the kid part after a while.
When I got into my 40s, I figured that was a little silly, So I'm just WK057 now, VP of engineering and development at OCEAN Mining.
And I formerly operated the Eligius mining pool with Luke from like 2011 to 2017.
We mined like 10,000 blocks, 300,000 somewhat Bitcoin.
Cool stuff.
Definitely been involved in the Bitcoin community for a long time.
Again, I'm better at the technical stuff than presentations, so bear with me here.
I also ran a pretty large early mining operation with some of the early ASICs, FPGAs, GPUs, you name it, when that was still a thing on Bitcoin, just to give you an idea of kind of how long I've been around here.
Lurking in the shadows for the most part.
And one of the things you can find about me, I do a lot of security research stuff on the side.
I was awarded the single largest bug bounty by Tesla.
Mechanic here tells the story way better than I do.
So if you ever get bored, ask him to tell that for you.

## Why DATUM Exists

Jason Hughes: 00:02:46

All right, so why am I here?
We're talking about DATUM, and I hope that everybody here knows what DATUM is at least a little bit.
It's a protocol that OCEAN  has developed and is pushing for decentralized template creation.
I personally want to see decentralized mining and template creation back in Bitcoin.
That used to be a bigger thing than it was.
Than it is now, it used to be a bigger thing, when you had more people actually mining blocks themselves.
You had kind of a mix of pools.
You had some protocols like GBT that came along that allowed it.
And that's kind of gone by the wayside, as we have Foundry and Antpool and friends, if you've seen the other talk over there, well over 50% of the network.
But I basically created DATUM, the protocol, the gateway, and the server kind of from scratch over the last year.
And it's worked out pretty well.
So what is a DATUM?
DATUM is an acronym, because I love acronyms, for Decentralized Alternative Templates for Universal Mining.
And the idea behind it is to make a protocol that is just for decentralized mining.
It's not for just pointing your miners at a pool and calling it a day.
You have to do the work.
You have to run your node.
You have to actually do what a miner was originally supposed to do back when you could mine with a CPU.
You created your block.
You picked the transactions from your mempool.
And you set the policies for that mempool, which is kind of the overarching theme of this conference, is pools and mempool.
The pools right now, if you just point your miner at Foundry or at something, you are not a miner.
You are a hasher.
And I think other people have gone over that.
But you are just doing what they tell you to do.
You are a mercenary.
Unless you are pure solo mining against your own node, you are not a miner.
And we're trying to fix that.
We're trying to make it so that everybody from the guy with one Bitaxe all the way up to the guy with 100 exahash farm can do their own mining and make their own blocks again.
So DATUM, in order to do that, has to be a pool server that the miners run themselves.
Because you have to have somewhere to point your miners to be able to give them the work that you create to actually accomplish that.
And you can't accomplish that without a pool server.
And we have to work with what we got.
We have thousands, tens of thousands, hundreds of thousands of miners that run the Stratum version 1 protocol.
Those miners can be pointed at things, and we want to make that easy.
You have to be able to point that at something to make your own block and reap the rewards of that.
So the miners make the blocks with DATUM.
The miners submit the blocks directly to the network.
We don't have to be involved in that.
Like, no pool has to be involved in it.
You can run DATUM and be a completely sovereign miner just by running the DATUM gateway.
It's pretty lightweight and pretty cool that it does that.
So it is a pool server in itself.
And the idea is we wanted it to be open source.
We released the DATUM gateway under the MIT license.
I don't think it can get much better than that.
And the other thing is you want to make sure that the blocks that you make, you know what you're making too, because there's some coordination with the pool.
You want to be able to make your own blocks, but you don't want to have to wait until you mine your own block to get paid.
So you can see what your block is going to be paying in the coinbase non-custodially to other miners and yourself.
And you can see that in your own DATUM gateway.
So here's a little overview of how the DATUM setup works.
On the, I guess it's my right and your right, on the right-hand side, you have what you would run as a DATUM miner.
So your miners, your actual ASICs, the Bitaxe, the S21s, whatever you have, you would point them at your actual DATUM gateway software.
And we'll get into what that is in general.
But you would point them
at your actual DATUM Gateway software and we'll get into kind of what that is in general but but you would point them at your DATUM Gateway.
The DATUM Gateway then uses your node.
Bitcoin Knots, Bitcoin Core works with both.
Obviously, I'm going to suggest Knots, but I'm not going to derail this conversation into that one.
There seems like there's plenty of time for that later.
I'm just trying to get you to make your own templates.
If you want to make them with Core, I can't stop you.
And that's the cool part about this.
But at the end of the day, you are an actual solo miner.
When you run DATUM and you use your own node, you are a solo miner.
And that is, by definition, what solo is.
If you point a miner at a solo pool, per se, you're still just a mercenary.
You just happen to be getting all the reward when the block is found, maybe, depending on that pool.
You're trusting them to do that.
With this, you don't have to.
If you want to actually mine, lotto mine is kind of the correct term for that, lotto solo.
You can do that as a sovereign miner.
You don't have to pay anybody a fee.
You don't have to do anything.
You could set this up in five minutes with your node and just be mining and do it.
Now, that's not great for everybody else.
Most people want to pool, because you can't go five years without finding a block.
And you wouldn't want to, because over difficulty changes and things, you would eventually kind of undercut yourself if you don't find blocks regularly.
And most people can't if you don't have a huge operation.
So you want to mine on a pool.
So the DATUM Gateway connects to the DATUM pool, which we call the server side of that DATUM Prime.
And that coordinates with the pool that you are working on work that will pay the miners of that pool.
And that's an encrypted link between your DATUM gateway and the pool.
So as a benefit of that, your DATUM gateway becomes an aggregator.
The DATUM gateway only has to communicate once with the pool for however many miners you have behind it.
You can set your difficulty high enough so that your bandwidth usage from the DATUM gateway to the pool for an entire mining farm, and we'll get into that a little bit more detail, is pretty low.
It's an aggregator that you can use right now.
And there's not a whole lot of those.
There's some for Stratum V1.
But even aggregating on Stratum V1 is higher bandwidth than using DATUM or even SV2, some kind of aggregation that uses a slightly more sane protocol.
SV1 works.
It's not the greatest.
It's kind of slapped together to serve a purpose and really grew out of proportion, but we're stuck with it for now.
So we had to work with it.
So the DATUM Gateway runs the Stratum V1 server, connects to that, makes sure that your shares are working for the pool.
You're making valid blocks, and everybody's happy because now you're making your own blocks and getting rewarded by a pool.
That's the best of both worlds there.

## Why Not Stratum V2?

Jason Hughes: 00:09:27

So the elephant in the room, why didn't we do Stratum V2?
There's a bunch of reasons for it.
I don't want to dunk on the Stratum V2, guys.
This isn't about that.
We tried to come up with a way to make this super easy for miners to do.
And after a lot of discussion, we kind of came up with, we needed to do our own thing.
It's a protocol.
It's going to be open source.
It is open source.
And we couldn't think of a better way to do that.
And there's some bullet points that I'll just run through really quick.
Again, this isn't bash Stratum v2.
This is just some bullet point reasoning.
So Stratum v2 has been around a long time.
Ever since Stratum v1 was a thing at all, people were talking about upgrading the protocol to be a little more sane, because it's text JSON.
Your shares and things are in ASCII hex.
This is not a sane protocol for large deployments of tens of thousands of miners now.
You're doubling the possible bandwidth use, even if you just made that binary.
So it's not scalable in the ways that it needed to be.
So Stratum V2 has been a thing for a long time.
That was an immediate thing.
I mentioned that back in, I don't even know the date, but back when I ran the pool, like why aren't we upgrading it to something better before everybody latches onto this protocol that's terrible?
And it just never happened.
And it still hasn't happened.
There's been a decade of development on Stratum V2 with no adoption.
I hate Rust.
I'm just going to throw that out there.
I think it's the worst thing that's ever happened to development.
You can flame me for it, but it's terrible.
That's a whole talk in itself.
Maybe we'll do that one next time.
But DATUM's written in C.
It's lightweight.
The entire binary with a whole pool server coordination with the pool can handle tens of thousands of miners connect to it is like less than 500 kilobytes.
It runs on a Raspberry Pi 3 at exahash levels.
This is stuff that you can't really do unless you get deeper than C.
Rust has too much overhead for stuff like that.
It's just you're not going to scale something like that with Rust.
Maybe eventually.
I think people are trying to do it, but it's not there yet, in my opinion.
And that's just that.
Stratum V2 was still originally made as a centralized protocol.
Its current implementations, and the only implementations in the wild are centralized implementations.
You can't mine a decentralized block on Stratum V2 today.
You can.
You can connect to Braiins Pool and use Braiins firmware to connect to Stratum V2 on their protocol there, but that's still centralized.
They're giving you all the work.
Not super helpful for decentralizing.
That was kind of bolted on.
That was something that was bolted on to the protocol later, because everybody's like, well, why don't we make a decentralized protocol?
OK.
So DATUM was the opposite.
The protocol doesn't support that at all.
If you don't have your own node, you can't do anything with DATUM.
That's kind of the framework of it.
This is built on top of a node.
If you don't have your own block to work on, like DATUM won't even tell you, the server won't even tell you there's a new network block.
Your node has to do that.
There's nothing that you can use from the actual pool side or anything to be able to make valid work with DATUM without actually running a node.
So that was the ground up thing that didn't exist anywhere else.
And kind of morphing Stratum V2 into that was more work than making this from scratch.
And again, to date, there's no adoption.
There's no adoption for SV2 in a decentralized way, whereas DATUM, as of right now, and as of like 45 minutes ago, we just found another block mined by the software on mainnet.
Over 200 mainnet blocks mined by the DATUM software.
Over 100 of those mined by individual miners that were making their own templates.
Like, this is today.
This is happening now.
If you have a Bitaxe here, you can set this up on your laptop and it'll work.
And you can make your own blocks.
So there's no one else doing that, so we had to do it.
I have a couple more slides of bullet points for this, but I'm going to try to skim through them.
Stratum V2 wasn't designed for decentralized payouts.
That's actually a problem with miner firmware.
One of the other talks earlier, the P2Pool talk, touched on why that's a problem.
Antpool, Bitmain, and whatnot, and some of the other miner creators just assumed that we would never need coinbase payouts larger than 500 bytes, a kilobyte maybe.
That's not enough to run a non-custodial pool fully, because you just can't cram everybody's payout in every block.
Well, we want to do that.
And that's the best.
That's what we can do.
And actually, some of the push from OCEAN has accomplished that.
The latest WhatsMiner's firmware supports like six kilobytes.
The S21s are up to like 2.5 kilobytes.
It's being fixed in a way that works, but we can't just throw that at everybody.
So DATUM is designed as much as possible to be able to cram the biggest coinbase transaction possible.
So it fingerprints the miners, it can give different work to different miners from the same server and give them the biggest possible work they can do.
And I didn't see any way to accomplish that within the framework of Stratum V2.
Those guys can correct me on that.
It seemed like a lot to pull that off.
The Stratum V2 stuff needed a modified Bitcoin node, last I knew.
That's a lift.
You can only use the implementation that has those patches.
And DATUM doesn't.
With the getblocktemplate (GBT) has existed for over 10 years.
It's the standard for mining and getting your template from your node.
Just use that.
Why not?
So DATUM just needs GBT.
Any node that can make GBT, whether it be Knots, be it Core, whatever you can get, your modified Core, Libre Relay, I don't care.
DATUM will take it.
It'll work with what exists now.
And part of Stratum v2, the core underpinning of it is that the miners have to get permission from the pool to mine their template.
That's been the argument, like, oh, well, if that pool doesn't accept it, you can just go elsewhere.
But why?
Just have it so that the pool doesn't care.
The pool's not supposed to care about what you're mining, as long as you're paying the miners on that pool.
And so DATUM was designed with that in mind from the beginning, so that eventually, and I cannot say that it is right this second, eventually DATUM can be blind entirely to the templates, even though right now it is like 90 percent blind to the templates.
That is a ground-up change, where another reason just to kind of get away from something else that has the tech debt of Stratum V2.
Stratum V2, one of the things it needs is adoption on the miners.
It's a new protocol that's designed for centralized mining.
I don't disagree with the need for that, because Stratum V1, again, is terrible.
So we need to get a point where people can roll this out today.
We don't want to wait for decentralized template creation 10 years from now when Bitmain and everybody gets on board with some new protocol.
That's a lift.
So work with what we've got.
So we need, Stratum V2 needs the Stratum V2 pool, the translator.
Again, I didn't want to spend more than like five minutes on this whole thing.
But there's a host of reasons.
I'm happy to chat about it.
And I guess at that point, does anybody have any questions about that part of why we didn't do Stratum v2?

[Audience]: 00:16:54

Just a question on something you said.
You said you were going to pay later.
Could it be aligned with the template?
Are you still thinking about the coinbase

Jason Hughes: 00:17:02

The coinbase, I don't consider part of the template, because everybody knows who you're going to have to pay.
And the question was that the coinbase needs to be validated by the pool.
And yes, you're correct.
That we want to know that you're paying the correct miners.
If you're not, then that's not valid pool work.
It's valid, you have a valid block, but that's not valid for the pool.
So that, I mean, that's reasonable to expect the pool not to accept your work if you're not actually paying the miners.
That's the limit of how far we want that to go.
But everything else should be offloaded to other miners via their proof of work to prove that this miner has the best interest of the pool at heart.
They're actually doing everything they're supposed to.
They have validated that your template is good along with these other 20 miners.
The pool has to accept that and never needs to see it.
So that's the goal.
Right now, the DATUM pool server will spot check templates where the pool does get some visibility.
We wanted to get this out the door tomorrow, back six months ago.
Rolling out an issue number one on the GitHub for the DATUM gateway is to not do that anymore.
So does that answer your question?
Okay.
Anybody else on that one?

[Audience]: 00:18:17

How do you prevent miners from submitting empty transaction...
Oh, sorry.
So how do you prevent miners from submitting templates that have no transactions in them?
Just empty blocks?

Jason Hughes: 00:18:28

We can't.
That's valid work.

[Audience]: 00:18:30

Right.
It's valid, but then as a pool, doesn't that hurt you because you're getting less?

Jason Hughes: 00:18:35

So that's a topic for a whole other talk, but in short, yes, there has to be a weighting mechanism for that.
The idea is that if you are mining a block that is worth X and it would take you T amount of time to find that block.
Over that amount of time, you should get X from the pool.
And nobody else should get anything different from their blocks.
If you're mining X times two blocks, you should get X times two over time.
And that's the goal of the weighting mechanism behind that.
And obviously there has to be some buffer in it.
I'll get into some of that.
But that's a whole other talk.
But yes.
But yes.
There's a mechanism.
But the idea is an empty block is a valid block.
I mean, I'm not going to say no to it when somebody finds one for the pool.
So...

[Audience]: 00:19:25

So what stops me from...

Jason Hughes: 00:19:28

Where we at?

[Audience]: 00:19:29

What stops me from mining a coinbase that claims that there were high fees paid when there actually weren't.

Jason Hughes: 00:19:37

So right now the spot checks kind of prevent that because we have to validate the blocks and if you fail a spot check at any time, your work up to the last spot check is no good.
So that's the current thing about it.
And there's obviously some protections that will trigger a spot check for stuff like that right now.
Eventually, that won't be the case.
Eventually, what will happen is your block that claims that it has 20 Bitcoin worth of fees will need to be validated by some quorum of other miners on the pool before it's accepted fully by those miners.

[Audience]: 00:20:08

So you mean I can 51% attack the pool's payout itself?

Jason Hughes: 00:20:12

Sure.
You could.
There's some things designed into that that prevent it a little bit better than just being able to 51% attack the pool.
But again, that's the share weighting and stuff like that.
That's kind of the decentralizing of the template validation is the next talk.
So we could definitely get into that in more detail.
I'm happy to talk to you about it.
All right, we're good?
Let's keep going.

## Why DATUM Is Written in C

Jason Hughes: 00:20:43

So why C?
And I'm spending more time on this little aspect of it than I wanted to.
But C is just faster for these.
I'm not afraid of memory management.
I've written C for 20 plus years.
And it's just one of those things where if you can get it done in C, you can get it done the best.
And the only way you can do better on certain things without C would be to write it in Assembly, which I could do.
And there's some Assembly stuff and some of the other things that I've written recently.
There's a lot of reasons to use C.
Dynamically linked libraries, if we need to upgrade like Libsodium or some of the thing that this links to in order to upgrade it.
Let's say there's a vulnerability in cURL or something like that.
Well, we don't have to recompile the whole thing.
You just install the updated version of that library, restart the process, and you're upgraded.
That doesn't exist in some other things.
C is battle proven.
It's insanely efficient.
Like I said, the DATUM Gateway binary is like 500 kilobytes.
In one of my tests, I asked one of our miners to point an exahash at a Raspberry Pi 3, and it was at like 12% CPU.
You're not going to pull that off with many other languages and implementations.
And it's just bulletproof.
I love it.

## Designing DATUM Around Existing Mining Hardware

Jason Hughes: 00:21:56

So where did this all start?
Obviously, we made a protocol out of thin air.
This had to start somewhere.
So we want to figure out, what do we know about the people who will use this?
And the people who use this are actual Bitcoin miners, people who want to actually make their own blocks and want to both pool mine and make their own blocks, be real Bitcoiners again.
That's a growing segment.
I mean, people today, like I've talked to so many miners that just don't even know that they are not really miners.
When you point your miner at some pool that you're not making your blocks, you're mining for that pool, but you are not a miner.
And what do these people have?
What are we working with and what are we starting with that these people have?
Because we're trying to make a protocol out of thin air that somebody can use with the things that they have.
People have petahash and exahashes of hardware.
We want that to work with this.
So what do they have?
They have Stratum V1 compatible miners.
So that's what we work with.
I'm not going to go through and make firmware for every single miner to convert it to some new protocol just to make this work when you don't have to.
Pools already do this.
Pools already make work for Stratum v1 miners.
There was no point.
And how hard is it going to be to get this to the people that we want to run it?
Well, making it lightweight, portable, and efficient broadens that tremendously to the point where we're able to get this to as many people as possible.
People run this on Start9s and Umbrels and all of these implementations where they're one-click just trying to make it painless.
I mean and that's there's nothing out there like that for this type of thing.
And this is the only one still.
So we had to do that.
And where do you have to start?
We have to start with a server that these miners could connect to.
So we have to start with the pool server.
And how do we do that?
So we start planning.
Where do we start with the pool server?
And this is the thought process.

## Evaluating Existing Open-Source Pool Servers

Jason Hughes: 00:23:51

Well, there's open source pool servers already.
Can we use any of those?
Do any of those work as a starting point for this project?
And we went through a lot of them.
Obviously, CKPool is an open source C-based mining pool.
Great.
It's proven in the wild.
It has mainnet blocks.
We could definitely use that as a building block.
The code base is somewhat complex to modify to do what we wanted it to do with decentralized blocks.
It could be done, but would that time be spent better doing something else?
It's GPLv3, open source, decent.
We're pretty much there.
There's some friction between some of the OCEAN team and the author of CKPool that I won't get into, but that exists.
So kind of weighing the pros and cons of that.
There's another pool server out there, Public Pool.
It's written in TypeScript.
That makes me vomit.
That is not a serious thing for a pool server.
It just isn't.
I'm sorry.
The name's ambiguous.
It's both a service and a code base.
No offense to the people making it.
They're trying to do some cool stuff.
And I like what they're doing with the Bitaxe community and all that.
It's just it could be done way better.
As of the time we were investigating this for DATUM, there were no public pool blocks in the wild.
I do believe there are two now.
So congratulations to them on that.
That's kind of a proven thing that kind of proves the software, which is cool.
I've seen inefficiencies with it.
When the guys, when they were working on stratum.work, and I have my own internal version of that, I would very commonly see the public pool instances that I see people running blocks behind mainnet.
That means you're just wasting your work.
So GPLv3 was a pro, but couldn't get over the hump of a lot of these other things.
And then Eloipool was the old Eligius pool software that I ran that pool successfully on for years.
It's battle proven.
10,000 or more mainnet blocks that I know of.
And we know other people ran Eloipool.
So I mean, there was a Chinese pool that ran it at one point that I knew of.
It definitely had adoption.
And it works.
It definitely works.
The OCEAN launch was done on the Eloipool with some modifications for AsicBoost and things that I think we're in the process of trying to release at some point.
But it's not scalable.
It's written in Python.
I think the thought process behind that was Python was pretty popular.
People know Python.
Let's get some people interacting with the code base and doing some things.
That did happen a little bit.
But at this moment, with your worker to hash rate ratio being very low as the network scales.
Individual machines have been about the same at 100 to 200 terahash for the longest time.
You need to linearly scale that.
And Python does not scale in this way.
It just can't do it.
I have a note here somewhere about the...
To run an exahash with Eloipool was taking five metal servers with 24 cores a piece with huge amounts of RAM just to run an exahash at eight shares per minute per worker.
And it's cool.
It works really well.
And it can be done.
But that's just throwing a lot of resources at Python itself.
AGPL, cool.
Could possibly limit the licensing and stuff of a new protocol.
I thought it would be fine.
But we can do better.
So let's do better.
And it kind of just boiled down to, if you want something done right, you've got to do it yourself.
I mean, that's the bottom line of the entire reason DATUM exists.
There just was nothing to build upon that would make it perfect.
And that's what we were going for.

## Building the DATUM Gateway From Scratch

Jason Hughes: 00:27:37

So started out with a DATUM pool server, MIT open source license.
It's called the DATUM Gateway.
It started as a pool server, because we have to, the first thing that we talked about that the DATUM system has to do is get connections from these existing miners so that they can do work with our new system.
And to do that, we have to give them work, and we have to run Stratum V1.
And that's where this started, as a written from scratch, from the ground up, Stratum V1 server.
At the end of the day, Stratum V1 is terrible, but it's not complicated.
It's a simple protocol.
It's probably as simple as you can possibly get on a protocol.
It's not well-defined spec-wise, because nobody abides by any particular spec on it.
And we'll get into the weeds of that a little bit.
But it's definitely something that has been adopted weirdly.
Like, for example, Bitmain has their own quirks about Stratum V1.
WhatsMiners have their own quirks of Stratum V1.
Every pool implements Stratum V1 differently.
So you kind of have to find the happy medium for what works for everything.
And that's what we had to do.
We needed it to be super efficient, because we don't know what people are going to run this on.
This isn't going to be run in data centers.
This is going to be run on a server next to your Bitaxe.
This is going to be run on a server that's somewhere near the routing equipment of 100 Petahash mining farm.
We don't know what people are going to do.
So it needs to be efficient.
It needs to be usable.
And it needs to just scale well.
So what are the minimum viable features that you need to write software to start a mining pool, to start a pool server?
Well, the pool needs to know what it's working on.
We have to get templates from a node.
So GBT exists for that.
Let's use it.
One thing out of the way.
No need to modify Core, modify Knots.
We don't need to get any PRs merged.
We can just do this.
So we need to generate, we need to create the generation transaction.
How do we do that?
Well, the most basic mining pool just pays you.
You tell it who to pay.
And that's where this starts.
You just tell it to pay either this one address or this list of addresses, and we go from there.
It needs to serve work to the miners, and it needs to validate the work that comes back from those miners and make sure that they can't pull shenanigans, like submitting the same work 1,000 times over or submitting work for blocks long past.
And that's kind of the basics of what it needs to do.
If you want to have a reward system underpinning this, you have to log those shares.
And obviously, I glossed over, you have to submit any blocks that you find to the network.
Because one thing that people in mining don't tend to realize, and I'd be curious what percentage of the room here even realizes.

## Mining Shares and the First DATUM Mainnet Block

Jason Hughes: 00:30:19

When you when your miner submits a share to the pool what exactly is it doing.
It's that is a block that just has not met the proof of work of the Bitcoin network.
It's met the proof of work of the pool of the server but it's not valid to Bitcoin yet.
It's just not something compelling to the Bitcoin network to accept.
But it's still everything else about it is right.
You can validate the generation transaction.
You can validate the block and the transactions.
Everything's there.
And that's a eureka moment for a lot of people in mining that I found.
So maybe not so much here, but that's interesting.
So that was done.
We made that part of the software.
And the real first DATUM block that was ever mined was when parts of OCEAN were starting to move over to using the DATUM gateway instead of Eloipool.
And that was block 857812 back in August, just to show you how quickly this has progressed.
That wasn't that long ago, less than a year, the very first block mined by the software.
So we got there.
We got to the pool server part.
We were hosting miners efficiently, everything working perfectly fine, mining real mainnet blocks, obviously after thousands of test net blocks.
But those don't matter.
You've got to get a mainnet block in there somewhere.
So that was the easy part.
We got the easy part out of the way.
Pool servers exist.
People have done that.
We're just kind of redoing what people have already done in a better way.
We need a protocol on top of that, that is able to decentralize the actual pooled mining part of it.
And excuse me just one second.
Leave you with that for a moment.
And I guess, does anybody have any questions up to this point?
I don't want to leave people hanging.

[Audience]: 00:32:05

I just have one more question.
The coinbase, sorry.
Thank you.

Jason Hughes: 00:32:10

You're fine.
I can repeat it if you need.

[Audience]: 00:32:11

In DATUM, the coinbase is not just generated locally, right?
So you have an API.
You have an endpoint where it can receive coinbase.

Jason Hughes: 00:32:18

Right.
So we'll get into that as part of the protocol.

[Audience]: 00:32:21

Okay.

Jason Hughes: 00:32:22

But yes, the question was does DATUM generate the coinbase?
It generates the transaction, but it uses something as the list of who to pay.
And how that happens is either local, or it's either local in your configuration to pay you, or it comes from the pool.
Like, I have a block that's worth this much.
The pool says, well, if you have a block that's worth this much, this is who we need to pay, because these are the shares that people submitted.
So this is what we need to do.
So that's part of the protocol.
Obviously, if we're doing mining, we want to do encryption.
We need encryption between the pool and the DATUM gateway.
That's just a no-brainer at this stage in the game.
We need to be able to validate the work with the server.
We need to be able to support aggregation, which the gateway does.
So we don't want a thousand connections to the pool for a thousand miners.
We just want the DATUM gateway to connect to the pool and deal with all those work.
We don't want to care about what pool you're using.
We don't want to care if you're lotto mining or if you're just using a pool.
Any pool should be able to use this, and it shouldn't impact them in any negative way to do so.
The protocol itself is open source, so we needed that.
We wanted people to adopt this.
We needed to be quickly developable.
We needed to get this out the door because this is something that's needed in the community yesterday.
The actual centralization of mining is a real threat.
And there's been panels on it here that have just kind of outlined that.
And I feel like that threat hasn't been made real to a lot of people yet.
Importantly, non-custodial coinbase payouts.
So when the block is found, as much of that needs to go directly to the people that contributed to the pool as possible immediately, not going through the pool.
We're not going to pay Foundry and then have Foundry pay us.
That's just not the way to go about it to this day.
It needs to be efficient on resources.
So for example, one of our large miners on OCEAN runs this with an exahash-ish.
Their server that they run this on has, you can't even tell DATUM is running on it.
It's the Bitcoin node is the lift.
The Bitcoin node is the heavy part of this whole process.
The DATUM gateway serving the miners is just efficient and great.
So the DATUM Prime is the server side.
It needs to serve the DATUM gateways.
So now we have the people running their own mining pools with the DATUM gateway.
So they're making their own blocks, making their own work, using their own templates.
I'm glossing over a lot of stuff as far as that goes.
How you make the templates is how your node makes the templates.
So they're doing all that.
They're sovereign miners again.
Well, they want to get paid.
So we have to pool this in some sane way.
So we need DATUM Prime.
What serves the DATUM gateways is to do pooled solo mining.
And this needs to validate the work that's coming in from those miners.
Yes, they're making a valid block.
Is this a valid proof of work in the first place?
Did they include everybody who was supposed to be paid?
We give the miners, the actual DATUM gateway, a lot of leeway in this because of bugs in mining firmware.
Like some miners, like you talked about in the P2Pool talk, you can only fit 15 outputs, give or take.
Well, some miners can do 100.
Some miners can do the entire block as the generation transaction without a problem.
The Bitaxe will do it up until it runs out of RAM, which isn't an entire block, but it'll do it, which is crazy that the Bitmain stock firmware doesn't.
That's one of the most limiting ones at about 700 bytes or so.
So we have to work with what we got.
Again, back to one of the core premises we have to work with what we have, with what the clients have, what the miners have.
So the DATUM Prime doesn't know what kind of miners you have.
Like, we don't even know what miners make work behind the DATUM gateway.
All we know is we have a DATUM gateway submitting valid work.
And part of that is those miners need to, those DATUM gateways need to be able to split that work in a way that makes sense for their miners.
It needs to give the smaller coinbase data to an Antminer.
It needs to give the larger one to a WhatsMiner.
And we can't control how they do that.
And as things expand and as we fingerprint more, that can be incorporated into the DATUM gateway.
But we need to give them everything.
So we give them the entire list of everybody who's got to be paid in that block that they're trying to make of whatever value.
And you can also use that to verify that we're being sane.
Because you can tell me that you're making a block of 500 Bitcoin.
OK, well, here's the list of everybody who needs to get paid when you mine a block of 500 Bitcoin.
You don't have to try to submit work for that, but that's a cool way to verify that the pool is doing what it's saying it's doing.
But yeah, we have to track the variations of those jobs because those coinbase transactions, we don't know.
So we need to know them, we need to know what the miner is actually doing so that we can validate and rebuild the proof of work, kind of in reverse of the way Stratum V1 does.
Because they're giving the Stratum V1 work to the miners, we need to untangle that back to a proof of work based on what they gave their miners so that we can prove it again.
And that's a little more complicated than just kind of trusting what they tell us.
So again, there's multiple coinbase transactions per job.
That complicates a lot of that.
If you generate one template, one job, then that might have, I think right now, up to six different variations of the generation transaction in it.
So we need to know how you did that.
So that needs to be communicated to the server in an efficient way so that when you submit those proofs of work that we validate a share that meets a target that you can be rewarded for, that you've done exactly what you tell us that you've done.
And it's kind of that, again, a backwards validation of the work.
So we need to reconstruct all of that so that we can accomplish it.
And so now we're about to dive into a little more technical than I've gotten so far.
Again, any questions up to this point?
Cool.
Oh, maybe?
Yes?
No?

[Audience]: 00:38:22

So for the nature of this, at a very high level, Your servers have to be up online the whole time running this, right?
Is there a contingency if your servers go offline to not run the validation from a continuity of the propagation of the pool and the network?

Jason Hughes: 00:38:40

Realistically, let's be completely honest about it.
Yes, there has to be a server to accept the work, but there doesn't have to be a server to accept the block.
The pool side can eventually untangle what you did.
It may not be able to be perfect on par if it missed some of that connection in between the time that you switched from mining on the pool to mining yourself, if a block was found in that time.
But that block is yours.
We can't stop you from submitting it.

[Audience]: 00:39:06

Broadcasting it, right.

Jason Hughes: 00:39:07

Right.

[Audience]: 00:39:08

Okay.
And just from the decentralization architecture, understanding, and this is just I guess the nature of since you're coordinating across many different actors you have to kind of be that right air traffic controller making sure everything's kind of running above 

Jason Hughes: 00:39:22

Yeah and the interesting thing about it and I have a slide kind of about like ongoing improvements one of the things that will be able to be done is to move as much of that as possible away from away from the pool.
There's more things that can be moved off of the pool than are already, but I think we've pulled off like the 90th percentile of bullet points of things that you would need to be able to say you're mining as a sovereign miner at this point.

[Audience]: 00:39:42

And is that server side of the code open viewable or no, that's your guess?

Jason Hughes: 00:39:46

As of right now, no.
Okay.
It is planned to be.

[Audience]: 00:39:49

Okay.

Jason Hughes: 00:39:50

The protocol itself is, so you could make a server.
I can't stop you from doing that.
Again, MIT license, you're pretty free to do some things.

[Audience]: 00:39:59

Just a real quick question.
Who publishes the block when one is found?
Is it the client or the server?

Jason Hughes: 00:40:05

The client publishes it.
So their node submits the block to the network.
If the, right now, if the pool had validated it, it can also submit it when it's found.
And eventually, the same thing of other miners that will have validated that work.
It can be broadcast from multiple nodes down the road.

[Audience]: 00:40:21

I'm struggling to understand part of this.

Jason Hughes: 00:40:24

Sure, let's go.

[Audience]: 00:40:26

The way I think about a traditional mining pool is that, like, okay, obviously the pool makes the block template, and you're trying to find a nonce and you have kind of a search space.
It could be anywhere from zero to N and you're gonna divide up that search space and every miner in the pool is gonna work on a different part of the search space.
But it seems like with this, every miner's constructing their own block template and with slight variations in mempools, there could be differences in the blocks.
And so I guess what I'm trying to figure out is how does it, how is it still maintain efficiency as a Pool if there's the possibility that people are working on different templates.

Jason Hughes: 00:41:05

So it doesn't matter what template you're working on at the end of the day.
Yes, they're going to be unique kind of organically.
I think what you're getting at is if we're kind of wasting work, just to be clear, is that what your question kind of implies?

[Audience]: 00:41:16

Yeah, I think so.

Jason Hughes: 00:41:18

So if you're working on lotto solo work, not with the pool
Let's just start there, you're going to be mining to your own Address for one.
You can add a unique ID to your config if you're running ten of these, and that makes sure your work is unique.
With the pool, when you connect to the pool, again, your template's going to be different, so that helps, but the pool also assigns you a unique ID that you have to include in the actual coinbase input script.

[Audience]: 00:41:43

Okay, so wait, it almost sounds like it's because the other people in the pool, through the DATUM protocol, I can be somewhat assured that the other miners in the pool are including my address in the coinbase.
So even if a miner, even if we're having some redundant work if somebody else manages to mine something with a block template, even though it's a different block template than the one I was working on, I still get paid.
So it kind of balances out.

Jason Hughes: 00:42:08

Yeah.

[Audience]: 00:42:09

OK, interesting.

Jason Hughes: 00:42:10

They won't get their work accepted by the pool if they're not including that split as they're supposed to.
Because you're submitting valid work to the pool, they're submitting valid work to the pool.
It's the pool's job to make sure that that happens the way it's supposed to.
And that's the heavy lift, that's the part that's hard to decentralize, but not impossible, but very difficult to decentralize fully.
But we're gonna try to get as close as we can possibly get to making that both auditable and just generally verifiable so that you can be assured that that's happening without having to trust me.
I saw one, two, three.
I didn't know if there were any more.
Got this guy here.

[Audience]: 00:42:49

You mentioned end-to-end encryption being another gain.
You mentioned end-to-end encryption being another gain with DATUM.
Can you highlight some attacks maybe that prevents...

Jason Hughes: 00:43:00

Yes, I mean, right now, if you have your miners just mining to a generic Stratum v1 mining pool your ISP can intercept that point it wherever you want and you're mining for them now
So you can't really do that with end-to-end encryption that's done properly and especially with the aggregation of it now now your ISP doesn't even know how many miners you have, because you've aggregated all of them into one connection that's so obfuscated that they can't even know.
So the amount of information that your ISP or a man in the middle can glean from end-to-end encryption is less than to almost nothing.
They know that you're connected to a DATUM pool at most, but they don't know what you're doing.
You could just be connecting to monitor things.
I mean, that's, who knows?
And then the other side of it, yes, the next part of this is somebody who's going to ask probably is, well, SV1's not encrypted.
No, it's not, but you should trust your LAN at least a little bit more than you would trust your ISP.
So.

[Audience]: 00:43:52

Would this prevent some previous BGP hijack attacks?

Jason Hughes: 00:43:56

Would it prevent BGP hijack attacks?
To an extent, but no.
I wouldn't say yes, but for example, if for whatever reason you lost your connection to the pool, your DATUM gateway did, you can still submit a block to the network and that time window is longer than it would be than if you were just mining on the pool, it's basically between network blocks.
Your work is valid at that point.
So, I would say it's like 1% more helpful, but BGP attack is still a BGP attack.

[Audience]: 00:44:27

The BGP attack wouldn't allow them to take the workers and just run them through the pool.

Jason Hughes: 00:44:32

Right, and Luke was saying that the BGP attack wouldn't allow them to get new information from the pool.
It wouldn't be able to interrupt you doing the work.
Like right now, a BGP attack could stop you from mining on a pool entirely.
It could stop you from mining, whereas with DATUM, it wouldn't really be able to do that as long as you have other peers outside of where that attack is happening.

[Audience]: 00:44:55

One more question.

Jason Hughes: 00:44:57

Sure.

[Audience]: 00:44:57

Over here.

Jason Hughes: 00:44:58

I'm going to leave this one up here while that goes.

[Audience]: 00:45:00

You mentioned miners validating other miners work.

Jason Hughes: 00:45:03

Oh, over here.

[Audience]: 00:45:04

Is that live?
And if so, how do they get the other miners block templates to validate?

Jason Hughes: 00:45:10

It is not live, it is inactive development.
And I have some testing going on of that.
The idea is that the pool side can coordinate that in an, in a blind way.
So we can say, no, this miner has this much hash rate.
We would like you to validate the work of this miner.
Here's their public key.
Let's get you talking.
They send the command over to them and say, hey, they wanted me to validate this work.
The pool passes that.
They validate the work, say yay or nay, the pool tallies that.
They tell the pool, I validated this guy's work, it looks good.
Okay, we'll get 10 other miners to do the same, depending on a lot of factors.
Obviously, this is a risk management thing.
We don't need to validate every template.
It would be nice if we could but that's resource-intensive 
We can trust that miners are being honest to an extent because we already do that 
We're already trusting them not to block withhold
We're already trusting them not to do a whole host of things that they could do as miners that this is just building a layer on and it's not necessarily making it any easier.
So yes, we need validation because people will misconfigure nodes.
People will, there have been invalid blocks mined by people in the past.
We don't want people configuring the nodes like that.
It's not for the purpose of seeing what's in the block, it's the purpose is to see that the block is valid when it's submitted to the network.
Does that answer your question?

[Audience]: 00:46:27

Yeah, I think so, but you raised another one.
What do you think about block withholding?
Do you have any?

Jason Hughes: 00:46:32

Block withholding, to solve that needs a hard fork.
I mean, there's no way to prevent block withholding completely with any pooled mining setup.
I mean, that is just the honest truth of it.
You can detect it sometimes, you can put algorithms in place to monitor, to see if it's likely that somebody's block withholding.
That becomes an even more bigger problem when you have a permissionless pool like OCEAN, because we don't know who our miners are half the time, more than half the time.
And so you have to have things in place to try to detect these patterns and things.
But block withholding is a thing of Bitcoin as it stands because you can't prove block withholding but you can prove proof of work.
You can't do the inverse.

[Audience]: 00:47:17

Thank you.

Jason Hughes: 00:47:18

Yep.
This guy one more time, and then I'm going to move on to code, because I got 10 minutes.

[Audience]: 00:47:23

OK, let's move on.

Jason Hughes: 00:47:24

Yeah.
OK.
So the protocol itself, I'm going to fly through a little bit of these because this is all open source and you can kind of look at it yourself.
I honestly didn't know how low level I was supposed to make this talk, so I tried to keep a lot of it high level and conceptual because that resonates with the most amount of people.
But we'll dive into some code stuff.
The DATUM protocol is pretty dang simple.
We have a 4-byte header that goes on everything that has a command.
It has whether or not this is signed, whether or not this is encrypted to the pool's public key or the other end's public key, more specifically, or if it's encrypted to the currently open channel with those two endpoints.
Because you need to have that kind of handshake to establish that and determine what should be sent.
Because so part of the DATUM protocol is you have to have the pool's public key in order to even connect.
You can't even send your first message to the pool without its public key.
So you get that from some source that you assume is trusted, like the pool's website, or some other miner that's been using that pool.
I'm not going to tell you how to do that, but that is part of the system is you need that key to initiate the handshake.
So the actual protocol is incredibly simple from a protocol standpoint.
The actual commands are the hello and handshake.
Those are just a back and forth that establish the session with the mining pool for the encrypted channel.
That's pretty basic stuff, uses Libsodium, some creative license there on making that useful and lightweight.
And then the actual decentralized mining commands of I need to know who to pay.
We call it the coinbaser.
I don't remember who coined that word, but when you get a list of miners to pay in Eloipool, it was called the coinbaser.
So I kind of adopted that as well.
So I have a block that I think is worth, four Bitcoin, who do I pay?
And that's that.
And then the miner, the next thing it needs to do is submit a proof of work.
So the pool side can respond to the coinbase request with this is the list of miners.
It can respond to the shares like, yes, this was a good share.
And if it's not, this was why, and this is what you need to fix about it.
Generally, that's just, well, you're not mining on the right block anymore.
Or you didn't pay everybody you said that we told you you were supposed to pay.
Basic things that the pool would need to protect its other miners from.
There's the client configuration command, which sets things like, let me make sure I'm not jumping ahead of myself.
But there's client configure.
And then there is a block notify command that's not currently used and I think will be deprecated.
Again, keeping the protocol as simple as it can possibly be without going off the rails.
The job validation stuff is when the pool says, I would like to make sure that you're mining on a real template.
Please send me the details on that.
And it actually has to go back through and does effectively a compact block transfer between the pool and the DATUM gateway to validate that.
Again, spot checks.
Got to make sure people are being honest.
We have to protect the other miners.

## Session Handshake and Authentication

Jason Hughes: 00:50:35

So the protocol initiates the connection with the gateway, says hello.
That's encrypted with the server's public key.
It contains the client's public key, which can either be static or randomly generated at runtime.
That's currently the default.
And then it sends metadata, like I'm running DATUM Gateway version 0.3, et cetera.
The server comes back, like, OK, thank you for saying hello.
Here is my new session key.
It encrypts that with the session key that the client provided.
It signs it with the server's public key so that you know that that came back from the server, and you're not man in the middle.
It echoes the keys provided by the client so that somebody man in the middling can't just use the session key and say, I'm really the server.
And the pool provides some other metadata, like the coinbase tag.
So it'll say, you need to include ocean.xyz in your block header, in your block coinbase.
The unique ID that we talked about a minute ago to make sure that there was unique work amongst everybody, even if you're mining the exact same template, which does happen during empty blocks.
So that's a thing.
The minimum difficulty of the shares that the pool is willing to accept.
Currently, I think OCEAN does like 131k minimum difficulty just to keep things kind of sane.
A fun little message of the day.
It could be important, probably not.
And it moves on.
So that may or may not be legible on there.
I don't know.
But that's just the console of the DATUM gateway running, just doing everything I just described.
So we went over these a little bit.

## Coinbase Fetch and Share Submission

Jason Hughes: 00:52:11

The `datum_protocol_coinbaser_fetch command`, it asks the pool server for a list of payouts.
So I have a block that's worth this much.
Who do I pay?
Excuse me.
And the server responds back, here's the entire list of everybody who could possibly pay with that amount of money, and please pay as many of them as you can.
Obviously, the gateway is not going to be able to do that with all miners, and it has the leeway to do that.
So the client stores that with a unique identifier with the job so it can use that across multiple jobs if it needs to if they're the same amount.
That generally doesn't happen, but it can do it.
So when it submits that back to the pool, we have to know what coinbase response it's working with so that we can reconstruct that on the pool side because this is all deterministic stuff.
If I have this much Bitcoin to pay at this moment in time, then these are the people who are supposed to be paid at that moment in time.
That won't change anymore, at least not with the TIDES reward system.
So go from there.
Again, I don't know if that's legible on here or not, but this is kind of a flowchart of the proof of work process.
And I'll just rattle it off just to make sure.
You start with, I have work to submit to the pool.
So I need to send a message to the pool with my personal job ID.
I don't care what that is.
The coinbase ID that we negotiated a minute ago.
Any flags that we want to communicate, most of these are reserved for later.
The time, the `ntime`, same as Stratum V1.
The nonce that you found, and the version, because AsicBoost is a thing that's not going away.
You can set your own extra nonce size.
So you are in charge of the Stratum V1 server.
Doesn't matter to us.
Tell us what it is.
And the username that you want this to reward it to.
Generally a Bitcoin address.
But since the gateway is the arbiter of that, you can set the username on your miner side to whatever you want, as long as the pool knows who to reward.
This could be for a job that's already been established.
So if we don't have the Merkle branches, those will have to be submitted to the pool along with the first share.
And then if this block is only for the subsidy, if it's an empty block, then there's a couple other paths that have to be followed to make sure that that makes sense.
So if we, yeah, basically we have to validate that you are submitting everything you need for us to prove that you have done proof of work for the pool.
And this is kind of a basic way to do that.
The code's a little more complicated, but that's kind of the premise.
And this seems like a nice spot to ask if anybody has any questions on that.
It's a speed up.
It's just a speed up because now we know we don't need anything else other than this is the subsidy and whatnot.
To be honest, I don't know why I included it in the flow chart, because it is a simpler thing.
But it's an easy out why we ask for the subsidy, if it's a subsidy only block.

## Server-Side Share Validation

Jason Hughes: 00:55:08

So some challenges of the server side with actually being able to validate decentralized work is we need to track multiple jobs per client.
We have to different generation transactions at different times.
Miners aren't going to invalidate work immediately when the client thinks they do, because they could be generating templates every 10 seconds, but the miner might still have one from a minute ago.
That's still valid work as far as I'm concerned.
So we need to keep track of all that.
There are some guardrails on how many of these we will keep track of, but it's pretty liberal.
We want you to be able to work on templates how you want to work on them.
If your template's changing every five seconds, that's a little extreme, but we'll go with it.
We need to validate the coinbase split.
So we basically have to deconstruct the transaction again, make sure that everybody's being paid again, make sure the block's not stale.
It has to meet the target of the proof of work that you promised us you were trying to meet, because another aspect of this is you can set your own share target.
You, again, are running the entire pool.
So if you want to set your minimum difficulty at a million for a share, you can do that.
But we have to be able to prove that you said that that was where you started, and that's where you got.
So that's included in the proof of work as well.
And we have to, once again, go back, make sure you said the right thing.
That's in the proof of work, and that's where you got to.
We need to reject duplicate work, because you could be working on the same thing and tell me that this is a share that's valid twice.
So all of that has to be tracked for the entire scope of the block for you, for that same previous block.
It's heavy.
It's a heavy thing that needs to be done.
We have to validate all the basics, that the time is within the realm of what the Bitcoin network will accept.
The version is within the realm of what the network will accept.
And then the server has to make determinations right now on whether or not we think we need to validate your entire block.
If this man here said he sends a 50 Bitcoin coinbase, yeah, you're going to trigger a validation.
We're going to want to see that.
Again, later on, that'll be like, OK, yeah, we want to see it, but we don't want to see it.
We want these other miners to tell us that you're not cheating us.
And we will pick who those are.
And maybe not.
And then we provide the share actual proof of work to the back end of the pool for rewarding after all of that's done.
It ends up being a little complicated, but It does work.
At the end of the day, it's a pool server in reverse, because the client, the DATUM gateway, is the pool server.
The target's a whole other thing that I kind of got into just then and got ahead of myself.
So the target is, how often do you want your miners submitting shares to your pool server?
Well, as often as it makes sense for you.
I don't care.
But you can set that, and the pool accept it as long as it's above the minimum of the pool.
We have to embed that in the proof of work.
I'm running out of time, so I need to kind of speed through this.
But that's the basics of it.
We can prove that you met the target, that you promised us that you would prove.

## Performance Benefits of DATUM

Jason Hughes: 00:58:10

And what does this get us?
Like, what do we get after we're done with all of this on just the benefit side?
Well, quick thing, let's say you have 40 miners.
Well, now you have no latency to your pool.
Your pool is on site.
It's generating the work as quick as it can get it from the Bitcoin network itself.
So your rejects are lower because you're not working on stale work.
You can be working on a block that the pool doesn't even know about yet, as long as it's valid.
And the bandwidth usage of that for like 40 miners on DATUM is like 300 megabytes a day.
On Stratum v1, same thing, direct to the pool, you're at like 1.5 gigabytes a day on average.
It depends on the pool.
It depends on a lot of things.
But that's a metric.
So you're saving on that.
You can actually deploy this somewhere as an aggregator to both be sovereign and get the benefits of not hammering your internet.
And when we scale that out to something like 8,000 workers, with DATUM, 8,000 workers is about 8 gigabytes a day at the current defaults, 8 gigs a day.
You don't get any bandwidth spikes.
Every time the pool is like, hey, I need you to work on this new block, let me tell these 8,000 miners that you need to work on this new block.
Obviously, there's some proxies that exist for that to help it, but you're still within the bounds of the Stratum V1 protocol at that point.
On your local network, you might have a gigabit or 10 gig to work with to talk to your miners.
You can tell them very quickly, get on this new work, reducing stales, and all that.
If you connected 8,000 workers directly to OCEAN, you would use 200 gigabytes a day in bandwidth to just provide those miners with work.
That's kind of outrageous.
Let's aggregate that.
Aggregation is the thing that was kind of a core concept of making this work.
Again, you are your own pool server.
Other things worth mentioning, yeah, so the DATUM Gateway Stratum V1 server, it doesn't spike work.
Like, every pool you connect to, for the most part, will, like, on an interval, just send you new work.
And that's just a bandwidth spike, a bandwidth spike.
That's dumb.
You only need to do that when there's a new block and we need to get everybody on the same work right away.
And so what the DATUM Gateway will do, just the regular SV1, it'll do those spikes for new block changes, but then it will spread every other work notify across the entire time span of notifies, which levels out that bandwidth and makes it tolerable to somebody who has a big farm, if they're hosting it remotely or something.
Let's say you have your DATUM gateway at your house, and you have 20 hosted miners.
Well, this helps you, because now you have just a really smooth bandwidth profile.
The empty block speedup is still a thing.
And yeah, empty blocks are not a bad thing.
So in order to get SV, it's a limitation of SV1
You want to still get your miners on the work as fast as possible.
And how do you get work to your miners as fast as possible?
Make that work as small as possible.
And even on your LAN, that kind of matters.
Not as much.
And you can turn it off if you want to.
But it does help.
And an empty block is not necessarily a bad thing.
Right now, maybe down the road, but not now.

## Future Improvements

Jason Hughes: 01:01:16

What are we improving on?
Again, I mentioned issue one was to no longer send the block templates to the pool.
We want to do that.
That is issue number one.
We don't want to know what you're mining.
I don't care what you're mining.
We want you to be the sovereign miner.
That's the whole purpose of DATUM.
You make your templates.
You can mine them for yourself or for a pool.
That is one of the main things.
We want to just make general features like that.
DATUM Gateway has a web interface and stuff.
I didn't get into any of that.
There's a web interface.
There's a small local API you can use.
We want to be able to integrate that with other software.
And we want to make all that better.
It's open source.
Feel free to contribute.
PR is welcome, basically.
The overall user experience is already pretty good.
Let's make it better.
Right now, there's a few one-click installers that do work that will spin up a node and a DATUM gateway, and you're off to the races.
Let's make that better.
There's no reason not to.
So the goal is decentralized mining as much as we possibly can.
Making the templates is the biggest part of that, in my opinion.
And this accomplishes that.
We need more innovation in the space.
We need more non-custodial payouts.
We need support for spot-checking the templates with the miners.
There's a lot of things to improve, and that's coming.
But right now, this is available today.
You can use DATUM right now.
And that's the important part.
There's already blocks in the wild, this is already deployed in the real world.
There's no reason you should be letting a pool make your templates for you.
If you are, you're not a miner.
And that's kind of the bottom line there 
Open it up to just questions.
I don't know how much time I have left.
I lost the clock What do I got?
Am I done?
Okay, can I do like one or two questions if they got them?
All right.
What do we got?
Anything?
Well, I'm going to take that as I did a good job for the most part, but yeah.

[Audience]: 01:03:08

Okay.
So there are a lot of different ways in your pool that miners are inequivalent, hashers are inequivalent, right?

Jason Hughes: 01:03:13

Sure.

[Audience]: 01:03:14

You could have one hasher who's mining empty blocks, another hasher who's mining, you know, profit maximizing, mining full blocks, and a third miner who's mining monkey JPEGs and taking payments on the side, right?
And there's a social contract inherent in a pool that says, I will pay you if you pay me.
That's fundamentally the way, you know, a decentralized type pool works, right?
But they're not the same.
They're absolutely not the same.
One of them is going to earn more rewards than another.
And I don't expect, you know, if I'm profit maximizing, someone else is not, and someone else is taking fees out of band, it's not fair for me to pay them for my profit maximizing block while they are not paying me in a proportional manner.
There are other ways that miners are inequivalent too.
For instance, let's say one guy's mining with a Bitaxe on a Raspberry Pi and you have not spot checked the work yet.
There's one node in the network that knows what this block is when he mines it, and it's a Raspberry Pi, and it's on a dial-up line.
And maybe this guy's even screwing around.
He's got a quadratic hashing bug in that block, right?
So it's going to take forever to validate once he finally uploads it.
So A, he's uploading it slowly.
B, it's a block you wouldn't want to mine.
You don't want to mine the quadratic hashing bug, right?
And so because it takes him forever to upload it, forever to get it on the network, his orphan rate is wildly different than other nodes in the network, right?

Jason Hughes: 01:04:30

Yeah.
There's a lot to unpack there.
For the squashing of rewards, that's a whole other talk.
I'm happy to talk to you on the side about it.
I could spend another hour going over how that's able to be evened out so that as you mine your block worth X, you get X reward over the expected amount of time, and he gets X over his X amount of time.
That is mostly a solved thing, and that again, a whole other talk.
The orphan rate thing, that's a real thing.
I mean, that's just something that has to be accepted within the network and it is it is a risk in any decentralized protocol and we're moving towards decentralization.
It's already a risk in the Bitcoin P2P network.
That's kind of a thing we have to accept to be decentralized.

[Audience]: 01:05:16

We have solutions for all of this.
Come see my talk tomorrow.

Jason Hughes: 01:05:19

Let's do it.
Let's do it.
Was there any more.
I'm going to flash that up there one more time.
And thank you very much for listening.
I appreciate your time.


