---
title: "The Bitcoin Core Wallet"
transcript_by: kouloumos via tstbtc v1.0.0 --needs-review
media: https://podcasters.spotify.com/pod/show/chaincode/episodes/Andrew-Chow-and-the-Bitcoin-Core-Wallet---Episode-30-e204vdj
tags: ['bitcoin-core', 'coin-selection', 'descriptors', 'hardware-wallet', 'hwi', 'psbt', 'wallet']
speakers: ['Andrew Chow']
categories: ['podcast']
summary: "Andrew Chow joins us to discuss Bitcoin Core wallet development, PSBT, Output Descriptors, and HWI."
episode: 30
date: 2023-03-10
additional_resources:
-   title: Hardware Wallet Integration (HWI)
    url: https://bitcoinops.org/en/topics/hwi/
-   title: Partially Signed Bitcoin Transactions (PSBT
    url: https://bitcoinops.org/en/topics/psbt/
-   title: Survey Results
    url: https://github.com/achow101/2021-core-survey
-   title: Bitcoin Core GUI
    url: https://github.com/bitcoin-Core/gui
-   title: Bitcoin Core GUI-QML
    url: https://github.com/bitcoin-Core/gui-qml
-   title: Descriptor
    url: https://bitcoinops.org/en/topics/output-script-descriptors/
---
Speaker 0: 00:00:00

Well, I will not say this is an unreasonable approach for a first implementation.

Speaker 1: 00:00:06

Sure.
But this is where, you know, Satoshi's been gone for a little bit.
Interesting.
Hey Jonas.
Hey Merch.
We are here with one of your wallet collaborators, HL101.

Speaker 2: 00:00:24

Wow, the wallet guy.

Speaker 1: 00:00:26

Yeah, but he's still, you're still a collaborator.

Speaker 2: 00:00:28

Sure, sure.
So Andy has been working on the Bitcoin Core wallet for many years, and he's covered a lot of different topics, and we're going to pick his brain on them.

Speaker 1: 00:00:37

Descriptor wallets, the big refactor that he did a couple years ago, PSBTs, hardware wallet integration, this migration from legacy wallet to descriptor wallets.
Lots to cover.
Hope you enjoy the episode.
So the first question I'm going to ask you is,

## Why do we need a wallet in Bitcoin Core?

Speaker 1: 00:00:58

why do we need a wallet in Bitcoin Core?

Speaker 0: 00:01:00

Well, you got to make transactions somehow.
If we didn't have transactions, we wouldn't have Bitcoin.

Speaker 1: 00:01:04

Yeah, but like other people are doing wallets.

Speaker 2: 00:01:08

They're doing it full time.

Speaker 1: 00:01:10

Yeah, they got nice GUIs.

Speaker 0: 00:01:12

They're building nice features.
So the Bitcoin Core wallet can be used for some more power usery things.
Okay.
And I guess maybe not the wallet itself, but the Bitcoin Core provides a lot of utilities for doing some fairly low level things.
And some of those are in the wallet, and you can do some weird stuff with your transactions.

Speaker 1: 00:01:36

Do we want weird stuff with our transactions to be the value prop of the wallet?
That's a good point.

Speaker 0: 00:01:45

I guess a good way to look at it is it's a research and development product.
You use this to do research, you use it to do experimentation.
And if you wanted to build a wallet that targets something, like a specific type of script, a specific use case, You could start with experimenting on the Bitcoin Core wallet before you move out to whatever specific thing you're trying to target.

Speaker 2: 00:02:09

I think generally Bitcoin Core will be on the forefront of what's possible with wallets.
Not feature-wise, but script-wise and protocol-wise.
So we're working on many script descriptors.
With Create Raw Transaction you can build non-standard transactions which hardly any wallet can do.

Speaker 1: 00:02:32

But again, why is that the value problem?

Speaker 2: 00:02:36

I think it's important to have one wallet that shows what's possible for other wallets to make use of that in features.
There's a few wallets, for example, a Liana wallet came out recently with an interesting script that I hadn't seen in another wallet yet, which is essentially a decaying multisig where at some point other keys get access to your coins.
But if you just keep moving your funds about three times a year, it'll remain under your sole control.

Speaker 1: 00:03:09

That's the re-vault folks.
Yes, exactly.
So this is like sort of a vaulting mechanism.
It's actually a dead man's switch kind of thing.

Speaker 2: 00:03:17

Yeah, exactly.
Built in bequesting of your Bitcoins.

Speaker 0: 00:03:21

The other thing is, well, Bitcoin Core has always had a wallet.

Speaker 2: 00:03:25

There are some people that will not trust other Bitcoins out there at Bitcoin Core.

Speaker 0: 00:03:32

Going back to the value proposition thing, there's something to be said for having a wallet that is attached to a full node.
And because having your own full node means that it gives you better security, better privacy, generally.
And so having a wallet that's attached to the full node is what a lot of people want, I think.
And part of that, even if you had separate software for this, you've raised the barrier of entry.
So if someone wants to have a full node wallet, they might have to, oh, they have to download Bitcoin Core.
Then they got to go find some other wallet, figure out how to connect it to Bitcoin Core, and then they can have their full node wallet.
Whereas if you just use Bitcoin Core, then everything's all there for you.

Speaker 2: 00:04:14

There is some wallets that actually do use Bitcoin Core, but I think some of them are on Mac.
There are some hardware wallets, but you have to get multiple projects to work together in some fashion.

Speaker 1: 00:04:27

Yeah.
I guess I'm just confused about who we're catering to.
And if I can be so bold as to tell the person who's been working on Bitcoin Core Wallet for five years and has made immeasurable contributions to the wallet, the value prop for me is that there's a higher bar for review and security than anywhere else.
And that it's more balanced in terms of showing things like privacy and the innovation pieces, like first half SegWit, first half Taproot, etc.
But the security and soundness principles, you're not going to find anywhere else.

Speaker 0: 00:05:02

I'm going to contest you on the Asmor review.

Speaker 1: 00:05:04

Oh, great.
Wonderful.

Speaker 2: 00:05:07

I think we should have that.
Actually, we've had a few People come in last year and do more on the wallet, but for a while, the wallet was definitely a part of the code base that got very little action.

Speaker 1: 00:05:25

But the wallet is hopping right now.
It's hopping.

Speaker 0: 00:05:28

Yeah, a little bit.
I mean, It's been getting more review, more work on it.
But the area that we have, there's always some focus that most contributors are looking at at one time.
It's not intentional, but I've noticed this over the years that There'll be a focus on P2P, a focus on validation, a focus on networking, a focus on the wallet.
And it moves around.
So a couple years ago, we had a pretty big focus on the wallet, and we've kind of moved off that, just naturally,

Speaker 1: 00:05:58

I think.

Speaker 0: 00:05:58

What was the big focus a couple years ago?
Mostly on the refactor and the whole thing with the scripted wallets.

Speaker 1: 00:06:05

All right.
Well, we're going to put a pin in that and then come back to it because it's important.
But what do you think is the hottest area right now?

Speaker 0: 00:06:13

I think right now it's with P2P and relay, transaction relay.

Speaker 1: 00:06:19

Mempool.
Mempool.
So hot right now.
Yeah.
All right.
It starts with memes.
Let's go back a couple of years now and talk about the refactor and the descriptor wallet.
Kind of go back to the glory days and tell us about, tell us about what those projects were about.

Speaker 0: 00:06:39

So a long time ago, at this point, Peter O'Walla came up with the idea of these output script descriptors.
And the point was to have one string that could be used to represent several scripts, all of the scripts in a wallet, actually.
And here we're using a script to also mean address they are interchangeable.
So you could have a string that contained all the keys, it contained how to derive those keys, it contained other markers to say like what kind of script to produce and what kind of script probably to produce, which tells us what address we will make.
And the goal was to have this in the wallet.
A wallet would use these descriptors to produce the addresses.
So this would make it really easy to determine what belongs to the wallet.
It also makes it a lot easier to upgrade wallets because then you can just say, here's a new descriptor and you put it in the wallet, and the new descriptor has its definitions will automatically generate all the things.
So after Peter had come up with this idea, there was a fork into Miniscript, kind of, and then we started trying to implement it into Bitcoin Core.
So this was a fairly big effort, and it turns out that the way that Bitcoin Core was structured was not very good for doing these descriptors.
And so before we could even get to that point, we refactored half of it.
And there was a lot of work from myself, from Russ, from Mesh Collider, and then a ton of people were reviewing all of these things, testing it out and experimenting with it.
So eventually we got the refactor through and we got the script to wallets afterwards, which was also quite a bit of work.

Speaker 1: 00:08:20

And I guess looking back on that, first of all, those are two big efforts from someone who you had had contributions before, but not led anything like that.
Can you tell us what that process was like?
It was like leading those giant efforts.
I remember when that sort of like gist of this is what the refactor is going to look like came out.
I was like, well, that's, it looks like a lot of work.
And I was right.

Speaker 0: 00:08:41

Yeah.
That also was like, I think that was also the third attempt to get Descriptor to roll us through.
So we have these core dev in-person events and a lot of the discussion around how we were going to do it ended up taking place during a couple of those, like multiple of them.
So this was spread out over quite a while.
I guess like it wasn't even that I wanted to lead the project or like lead this effort.
I found it interesting and then I just wrote it and being the one to write something ends up putting you in charge of it.
So It sure does.
So, so like I wrote the PR, I wrote a couple of different branches and eventually one of them became a PR and people started reviewing it and giving comments and then like that's basically how I ended up in charge of this whole effort just because I went through the effort of writing it, I think.

Speaker 2: 00:09:32

Was that before or after you were nominated for wallet maintainer?

Speaker 0: 00:09:36

That was long before that.

Speaker 1: 00:09:37

Yeah, I mean, these are like, These are like,

Speaker 0: 00:09:40

This is like 2018, 2019, something like that.

Speaker 2: 00:09:43

Oh, two years ago.

Speaker 0: 00:09:44

Yeah, two years ago.
Yeah.

Speaker 1: 00:09:47

For those who can't see us at home, it's, that was, those are air quotes.
Okay.
So you did the refactor, you got descriptor wallets in.
Are you happy with where things are at?
I mean, I disagree in terms of you're not getting attention.
There's the guy sitting at the table with us.
There's Ferzi.
There's Josie.
What else do you want, man?

Speaker 0: 00:10:10

Well, OK.
When I started doing that refactor, I eventually realized, Actually, the way the wallet, as it is currently written, is kind of really not that great.

Speaker 1: 00:10:20

OK, so the refactor ended up not being that great?

Speaker 0: 00:10:23

No, like just in doing the refactor, I learned a lot about how the wallet itself actually works.

## Refactoring the Wallet codebase to build Output Descriptors (5:59)Should we rewrite the wallet?

Speaker 0: 00:10:29

Got it, yeah.
And in doing that, it occurred to me that actually this code is not that good.
And well, part of it is that you can trace a significant portion of it back to Satoshi.

Speaker 1: 00:10:40

God, does he know how to write code?

Speaker 0: 00:10:42

This is not the highest quality of code.
And it makes it hard to implement new changes, and it's also not very performant.
So around that time I also had the idea of, well, why don't we just rewrite this thing?
This is not a new idea.
Actually, if you look at our IRC meetings, This meme has come up multiple times over many years of, why don't we just rewrite the wallet?
Actually, at some point, I think it became, why don't we just delete the wallet?
Because it was getting that hard to work with.
And the change to the descriptor wallets ended up rewriting, I would say, probably like a third of the wallet.
And so there's still two thirds I'm looking at wanting to do.
But there just doesn't seem like the appetite for reviewers to look at these changes and to go through with a lot of the things involved in doing this kind of rewrite.

## Changes to Coin Selection

Speaker 1: 00:11:35

And what do you think that other two-third rewrite will get us?

Speaker 2: 00:11:38

So I looked the first time really at the wallet in 2014 when I got interested in coin selection.
And you could probably pretty easily still figure out that all of Bitcoin was a part of a single file at some point, almost.
It all came out of main.cpp and people had then pulled out a few things.
For example the coin selection stuff had not really been touched since 2011.
Somebody introduced an app sack then.
Before that, I think it was just either largest first selection or oldest first selection.

Speaker 1: 00:12:12

No, it used all UTXOs for every transaction.
Yes, at some point it used all UTXOs for every transaction.

Speaker 0: 00:12:18

I don't remember this.
I know.

Speaker 1: 00:12:20

Guy has a master's thesis, I wouldn't mess with him.

Speaker 0: 00:12:23

The very first version of Bitcoin chose coins by TXID order.
It used a standard map, which is a sorted data structure, and it was sorted by TXID.
So it would take the first thing out of standard map.
If it wasn't enough, take the second one, the third one, and so on.
And so...
It seems very efficient.
Oh, it's very fast.
I'm sure it's very fast.
Quite performant.

Speaker 1: 00:12:48

You're accusing Satoshi of not being performant.

Speaker 0: 00:12:51

But it's not very good for the optimization.
Like anything else.

Speaker 2: 00:12:54

Yeah, anyway, somebody put in knapsack.
Knapsack is terrible.
We still have knapsack.
And then I think Alex Marcos fixed something about the looping behavior after my master thesis and then nobody touched that part of the wallet until 2018.

Speaker 0: 00:13:14

Until 2017, something like that.
So the way that we did coin selection changes was people would use it.
They would find, oh, there's this really weird behavior.
If you do this one really specific thing, and you're like, OK, we will fix that thing.
Here's an if statement for some wild condition that you probably shouldn't hit, but it's there and it resolves this problem.
And that's how we did coin selection.
It was completely ad hoc.

Speaker 1: 00:13:38

It was like an elegant solution.
What could go wrong?

Speaker 0: 00:13:41

Yeah.
It was just completely ad hoc.
And there was no overall, Like, what do we want coin selection to do?
What are we trying to target with it?
What kind of coins do we want?
What fee rates?
All that stuff.
None of that was really in consideration, I think.
And it was mostly just like, here's a thing that we inherited from people who wrote something several years ago, and now it doesn't work.
It's completely black magic.
We don't know why it doesn't work.
We don't know what the hell it's actually doing.
And we're just going to throw some special case in for this one broken behave.

Speaker 1: 00:14:12

Yeah, so one of the things that I think seems to have helped with some of that as you have recently done some simulation work so that you can actually simulate some of this behavior.
So tell me more about that project.

Speaker 0: 00:14:24

So, well, so this started when I was interning at Blockstream in 2017.
And One of my projects then was to implement Merger's coin selection algorithm in Bitcoin Core.
And of course, because coin selection was at that time just a black box, no one knew how it actually worked.
There was a question of, well, can you demonstrate that this is better for some definition of better that is still undefined?

Speaker 1: 00:14:48

So I wrote a whole thesis about that.
What's the framework of better, then?

Speaker 2: 00:14:54

Well, there's different metrics that you could use.
Mine was, what is the overall fee cost, and how healthy is the wallet in the end.
As in, if you keep fragmenting your wallet more and more, your long-term fees that you have essentially, for every UTXO that you have in your wallet, you will have to spend money in the future to spend it.
So the more fragmented your wallet is, the more future costs you have already locked in.

Speaker 1: 00:15:20

But there are other metrics associated with that.
So for example, just like a human, be like, well, my cholesterol is high, but my pulse is good.
Am I healthy?

Speaker 0: 00:15:28

Who knows?

Speaker 2: 00:15:29

So, so I mean, I mean, not that strictly where you can look at a single number and you can say, oh, my health score is like that.
But we found ways to compare different approaches and see which one is better.

Speaker 1: 00:15:42

And are those being integrated into our criteria?

Speaker 0: 00:15:47

Like The waste metric is kind of an aggregate of all of these.

Speaker 2: 00:15:51

The waste metric is one of these.
With Josie I've been talking on and off about how the waste metric should only be one of multiple things that contribute to the score and we would like to have some scoring mechanism for privacy as a second contributor to which inputs we select.
So I don't think it's been our focus yet but we've been bouncing around some ideas.

Speaker 0: 00:16:17

With coin selection, I think, well, so I ended up using a lot of Merge's stuff because he was the only one who actually seemed to know anything about coin selection.
There was a master's thesis.

Speaker 1: 00:16:31

That's why we hired him.

Speaker 2: 00:16:33

I thought it was for my Stack Exchange answers.

Speaker 0: 00:16:38

So in 2017, I implemented the coin merges algorithm, which we call branch and bound.
And then in doing that, you know, learn about how coin selection works and doesn't work and realize how our coin selection algorithm was not that good.
And this also led to another refactor that ended up being delayed quite a long time.
Just to like clean up coin selection and get rid of some other dumb behavior that we had in it.

## Wallet interoperability

Speaker 1: 00:17:09

Yeah.
So you've taken us on this tour of getting to coin selection and talking about, you know, simulating behavior, which gives us actually some criteria to compare against, which seems like a good idea.
But these aren't your only projects.
You've also been thinking about, like, You led the effort on PSBTs. There's hardware integration.
How do these all fit together?

Speaker 0: 00:17:35

At some point I got a hardware wallet and I was like, why can't I use this with Bitcoin Core?
Turns out,

Speaker 2: 00:17:45

because it's very hard.
So basically you were saying, hey, I want to be able to transfer an unsigned transaction between one device and another device and I need a standardized format for that.
And it turns out that introducing a format for talking about unsigned or half-signed or partially signed transactions is something that a lot of people actually also need and have implemented before, but having a single standard for it was pretty awesome.
And down the road, what it makes much, much easier is multi-party transactions.

## Hardware Wallet Integration (HWI)

Speaker 0: 00:18:20

Yeah, so it started with, so I wrote HWI as mostly just a toy and for experimentation.
So Trezor provided a Python library, So I wrote it in Python.
Which I really enjoyed.
Yeah, it was a brilliant idea.

Speaker 1: 00:18:34

Ha ha ha ha ha ha ha ha ha ha ha ha ha ha ha ha ha ha ha ha ha ha ha ha ha ha ha ha ha Ledger also provided a Python library.

Speaker 0: 00:18:39

And then, what was the other one I had at the time?
CodeCard?
No, that didn't exist yet.
Digital Bitbox.
They had a really simple protocol that I could implement in Python.
And there might have also been a Python library.
So I did it all in Python, mostly for myself.
And I found out that, OK, I can get a thing for that Bitcoin Core can watch.

## Partially Signed Bitcoin Transactions (PSBT)

Speaker 0: 00:19:01

But how do I get transactions out of Bitcoin Core into to the script and get that to all the devices, including all the other information that they need to sign?
And that stuff includes, oh, for each of those devices, they have different protocols.
So you now need to take it in some common format that can give to my program that needs to convert it into all these other protocols that I can send out to the device.
And so...

Speaker 2: 00:19:27

And then recombine it all.

Speaker 0: 00:19:29

And it all has to come back out and go the other way into Bitcoin Core.
So it turns out that in doing that, I decided to write PSPT as that common data format to transfer information from Bitcoin Core to HWI.
And so these two projects were, PSPT and HWI were intrinsically linked from the start.
And of course it turns out that a way to transfer data about transactions to be signed between two different pieces of software is actually really useful, even if one end is not a hardware wallet.
Because all of that hardware wallet signing stuff is abstracted away.
So being able to have something that I can pass around between different compatible software, it was really useful for the ecosystem.

Speaker 1: 00:20:13

Besides the implicit, it's useful.
What other things are using this kind of thing?

Speaker 0: 00:20:17

Well, so the other thing is like multi-party transactions.
Because we can, just the way that I had written it, and this was also kind of on my mind when I was doing it, but it allows us to do things like multi-sigs, or...
Coin joins.
Coin joins.
Yeah, anything that required having multiple people involved was made easier by having PSPT because now it was a common data format that contained all the information you needed to know in order to sign it, except for the private keys, obviously.
And so you can just pass it around to everyone, they can sign it, and it just makes life a lot easier.

Speaker 2: 00:20:48

And then now on the other side of this equation, of course, wallets started saying, hey, wait, there is a shared format for talking about partially signed Bitcoin transactions.
And now the hardware wallets and other wallets are implementing that and we get a global standard in how wallets can communicate with each other.

Speaker 0: 00:21:09

One thing I found was that the idea of having a format containing information you need in order to sign is not new.
There was a BIP 10, something like that.
It was very old, that did something similar to PSBT, but not quite, and it ended up being withdrawn for some reason.

Speaker 1: 00:21:27

Who wrote it?
Do you know?

Speaker 0: 00:21:29

The Armory guy, Alan Reiner.
It was like, it was not the same.
I did, someone pointed this out to me.
I was like, oh, I just didn't realize this existed.
I read it, it's not the same.
And it was missing a bunch of things, I think.
But this is not new.
Like Electrum had their own custom format.
Bitcoin Core did a thing where it would shove signatures into the raw transaction.

Speaker 2: 00:21:50

I mean, BitGo had its own format too.

Speaker 0: 00:21:52

Yeah, I know BitGo had their own format.
Zappo had their own format, just like internal use.
And no one ever thought to standardize it until I came along and wrote my own thing.
I was like, maybe this would be useful for everyone else.

## Becoming Maintainer

Speaker 1: 00:22:06

It's clear that you've developed this affinity for the wallet.
Merck already mentioned it, like you became maintainer within the last, it's been about a year, right?
December?

Speaker 0: 00:22:16

Yeah, I think so.

Speaker 1: 00:22:17

So has that changed things for you?
Has it changed things, how you approach the wallet, how you think about its future?
I mean, we sort of have this idea around maintainership is it's not like an explicit lead, but it often goes to the person who's most active in that area.
So how does that change things for you?

Speaker 0: 00:22:35

It doesn't change a whole lot in terms of the things that I want to do.
It changes how much time I have to do them.
So since I became a maintainer, I've been doing a lot more review.
And not just of wallet stuff, because we know, relatively recently, both Peter and VitaMir have stepped down as maintainers.
And we do need maintainers to look at all parts of the code base.
Things still need to be merged, and I've started doing a bit more of that, just looking around at other parts of the code base, reviewing things that aren't in the wallet, reviewing things that I don't write code for.
And so that has of course eaten into the amount of time I can spend on the wallet.

Speaker 1: 00:23:20

Is spend a pun there?
Is that a pun?
We'll cut that bit.

Speaker 0: 00:23:28

So yeah, it's eaten into the amount of time I spend on the wallet.
But I still have a plan.
I still have things I want to work on.
It just takes a little bit longer.
I already knew it would take a long time.

## Tracking the UTXO pool

Speaker 2: 00:23:43

So what do you want to work on?
What's next?

Speaker 0: 00:23:44

So what's next?
I have five branches named wallet UTXO set.
They're all failed attempts at doing this next thing.

Speaker 1: 00:23:53

What is that?
So what's the next thing?

Speaker 2: 00:23:55

What is the motivation for that one?

Speaker 0: 00:23:58

So the name might not mean a whole lot, But what I want to achieve is to have the wallet actually track its own UTXOs. And you might be wondering, well, it doesn't already do that.
It doesn't.
So when you ask the wallet, what's my balance?
We have some caching, but it will say, let me check every single transaction I've stored, look at every single output, determine does this output belong to the wallet, and I will add it to a running total.
And it does that with some caching to figure out what's your balance.
It does the same thing for what UTXOs are mine and that I can spend.
It doesn't explicitly maintain a data structure for our UTXOs.

Speaker 2: 00:24:36

But every single time you build a transaction, it will recalculate its UTXO pool from all the history of the wallet.

Speaker 0: 00:24:44

So for really big wallets, this is kind of problematic.
Fortunately, C++ is extremely fast.

Speaker 1: 00:24:52

Or in this case, unfortunately, because you have to do this ridiculous operation.

Speaker 2: 00:24:57

People that try to run a business using Bitcoin Core wallets have noticed this problem.

Speaker 0: 00:25:03

It used to be worse before there was caching.
So we do caching now.

Speaker 1: 00:25:06

I don't assume that other wallets run this way.

Speaker 0: 00:25:09

Well, I will not say this is like an unreasonable approach for a first implementation.

Speaker 1: 00:25:14

Sure, but this is, you know, Satoshi's been gone for a little bit.

Speaker 0: 00:25:20

Interesting.
So the next thing I want to do in this rewrite of the wallet is to change how we do UTXO tracking, to actually store UTXOs and to do things where we load in a bunch of transactions that are completely irrelevant because every single output's been spent.
Or we load in transactions because they exist on disk and maybe they are completely irrelevant.
So something that I've been thinking about and working on and off and have had multiple failed attempts at is to change how we do transaction and UTXO management.

Speaker 1: 00:25:54

Sounds like a pretty big swing.

Speaker 0: 00:25:56

Yeah.

## Main components of the Bitcoin Core Wallet

Speaker 2: 00:25:57

So you mentioned to me earlier that in your mind the wallet really consists of three different components.
Do you want to elaborate?

Speaker 0: 00:26:05

So I think there is the key and script management component.
And this is the descriptor wallet kind of stuff.
Doing the refactor for the descriptor wallets produced a separate component for key and script management.
The next part I would say is transaction creation.
So this covers coin selection, just generally how we create transactions, some privacy things like do we do anti-fee sniping and What are the user's desires for their transaction?

Speaker 2: 00:26:32

Output grouping.

Speaker 0: 00:26:34

Output grouping, all that kind of stuff.
And then the last part is transaction storage and management.
You take some management.

Speaker 2: 00:26:40

Wallet history.

Speaker 0: 00:26:42

Wallet history, yeah.
I guess actually there's a fourth part, which is just metadata.
Like address book data, data about comments on transactions, that kind of stuff.
But that doesn't seem to be problematic yet.

Speaker 1: 00:26:53

I want to return to an earlier theme a little bit.
You had said that the wallet in Bitcoin Core was important because you didn't want any barriers for new users running in code.

## Who uses Bitcoin Core Wallet?

Speaker 1: 00:27:02

Do we know much about our users?
Obviously, there's not tracking, but you were involved in that MIT study.

Speaker 0: 00:27:08

Yeah, there was this spawn from an offhand comment I made to Mesh Collider a couple years ago.

Speaker 1: 00:27:15

I was like, why don't we just like run a survey of our users?

Speaker 0: 00:27:18

Like post a survey, see what people respond to it.

Speaker 1: 00:27:20

It didn't go as I expected it to go.
Which is you wanted it to go.
It went better than you thought.

Speaker 0: 00:27:26

Not quite.
How did it go?
I don't think we could get very much usable, actionable data out of it.
I have posted all, I think I've posted all of the raw data online, so if someone wants to do some analysis on it, they can do that.
But I think what ended up happening was that the questions that we asked were probably not that good.
And so what we got out of it, garbage in, garbage out.
So I don't know if, or when I was looking at it last time I looked at it, I didn't think that there was much actionable results from it.
We did learn a couple things.
There are a lot of people who use Bitcoin Core because it is attached to a full node.
There are people who use it because they have-

Speaker 1: 00:28:10

Of the respondents of the server.

Speaker 0: 00:28:11

Yeah, of the respondents.
There are people who use Bitcoin Core because they were using Spectre and it says, use Bitcoin Core.
So there's a mix of both of people who want just Bitcoin Core because it's full node and people who are like, I wanted something that was full node and the software I'm using said use Bitcoin Core.
So basically, but we didn't really get any data on how People were using the wallet.
Although one other thing I did learn is that no one changes their defaults.

Speaker 2: 00:28:38

I think that's pretty That's not expected unexpected so I guess to a degree you could say that wallet development is squeaky wheel gets the oil.
When somebody reports an issue, we might be like, oh, this is interesting, maybe we should do something about this.

Speaker 0: 00:28:55

Yeah.
So a lot of changes have been prompted by people doing something and reporting an issue.
Like, The reason I actually started looking at transaction management, not because it was inefficient when I read the code.
I noticed that and I was like, cool.
But No one's really complained about this yet.
And then someone complained about it.
And someone with an enormous wallet.

## What’s the future of the GUI?

Speaker 1: 00:29:21

But there's people complaining about the GUI and the GUI gets no love.

Speaker 0: 00:29:26

That's not true.
The GUI does.

Speaker 1: 00:29:29

Tell me more about the GUI.

Speaker 0: 00:29:30

It gets love in a different repo.
We have a separate repo for overhauling the GUI entirely using QML.
And that's actually been getting a lot of activity in designing a new interface, designing something that doesn't suck.

Speaker 1: 00:29:43

Right.
So apparently, Hot news on this podcast, it will be released within the next two weeks TM.
But Harold and team are hard at work at it.

Speaker 0: 00:29:54

Essentially the GUI redesign is something that has been getting a lot of eyes.
The current GUI doesn't, But that's mostly because it's bad, I think.

Speaker 1: 00:30:04

But this is the whole point.
If something's bad and people complain, I've heard, you're just not the right user.
Drop down to the command line, it'll work great.
But then you tell us that it actually doesn't.

Speaker 0: 00:30:16

I don't like responses like that.
I don't know if I collected this in the survey, but I think most people who use Bitcoin core actually like you use it actually as a wallet, use it through the GUI, including myself.
When I want to use it as a wallet, I use it through the GUI because I'm lazy.
So having a good user experience in the GUI is important.
And.

Speaker 1: 00:30:37

But do you think that'll drastically affect the raw number of users that will use it?
Or like, What is that going to change?
Because if people are using a Bitcoin Core wallet, because it's attached to a full node, making it an amazing user experience, is it really going to outcompete these newfangled wallets that have a big design team, etc.?

Speaker 0: 00:31:02

I think it can.
Or perhaps the bar is just really low right now.

Speaker 1: 00:31:08

And so we're all striving for.

Speaker 2: 00:31:10

I mean, especially for desktop wallets, it's just not that much.

Speaker 0: 00:31:13

So if you go on Bitcoin Talk, which I do far more frequently than I should, and you look at like,

Speaker 1: 00:31:21

As long as you're not on Twitter, that's fine.

Speaker 0: 00:31:24

And you look at what new users are opening new threads about.
If they're talking about Bitcoin Core, there's a lot of time it'll be like, how do I do this in Bitcoin Core?
And the response is, well, you got to open the debug console, you got to type these commands in.
And it's like, that's not a good user experience.
And they're like, okay, how can I?
And then they have trouble doing it.
And so then the response is, just switch to Electrum or just switch to this other wallet because it's a better user experience.
And I think if we can improve the GUI, as I said, the bar is pretty low.
So if we can improve the GUI so that people don't feel like they need to switch to a different software in order to use it.

Speaker 1: 00:31:59

It just feels like All the elements are there for the big use case, which I think continues to be lacking in the ecosystem.
I know there's Sparrow and I know there's Spectre and there's some other solutions out there, Electrum of course, but a really nice multi-sig with hardware wallet integration, I think that would be a game changer.

Speaker 0: 00:32:17

Yeah, probably.
And I think there are some people who have been working on stuff like that Yeah, but but not necessarily in a nice GUI form Cool.

Speaker 1: 00:32:27

Anything else we want to talk about?

Speaker 2: 00:32:28

Maybe the move from legacy wallet to descriptor wallet There's users that have had their Bitcoin Core wallet for a decade, and I know that a recent version had a converter that allows you to convert a legacy wallet to a descriptor wallet.
New wallets obviously created by recent versions will be descriptor wallets already.
Can you tell us a little bit about that?

## Switch to Descriptor-based wallets

Speaker 0: 00:32:52

Yeah.
So descriptor wallets, after we did the whole refactor, it turned out, well, because descriptor wallets was so fundamentally different that we had to do the refactor, they're just completely incompatible with the old style of wallet, which we would call legacy wallets.
Legacy is not a great term to be using here.
It's used in too many places.

Speaker 1: 00:33:10

MAX WIETHE-SMITH Deprecated wallets?

Speaker 0: 00:33:11

ADAM ROGOWE I guess.
I don't know.
But the main thing was, we didn't want to break forwards compatibility.
So if you, in theory, if you take a wallet from 0.2-ish, you can open it in current 24.0 and it will load and it will be missing all of the modern features, but it will still work and you can use that wallet.
With descriptor wallets, it's completely different.
So if we had a software that was descriptor wallet only, and you tried to do that, it would just tell you, this wallet, we don't know what this wallet is.
And you wouldn't be able to do that.
So we wanted to at least make it possible.

Speaker 1: 00:33:49

People would freak out.
Yeah.
They would freak out.

Speaker 0: 00:33:53

Yeah.
So, so there's, so we wanted to have a way to one, to, to just convert those kinds of wallets to Descriptive Wallets after we get rid of the Legacy Wallet.
And then we also want to have, you know, a smoothed-out deployment timeline.
So we start with, okay, we introduce Descriptive Wallets as a new thing, but it's not the default.
Then we change it to the default.
Then we say, if you start loading a legacy wallet, we're going to tell you, hey, this thing is deprecated and it's going to go away eventually.
And then we upgrade that later to, hey, this thing is deprecated and it's going to go away soon.
And then it's, hey, this thing is deprecated, you need to turn on this option to use it.
And then it's, hey, this thing doesn't exist anymore.

Speaker 1: 00:34:31

And so for that last part, I mean, there's a fundamental Bitcoin philosophy that you should be able to wake up sometime in the future and your money will still be your money.
But that seems to be broken here.

Speaker 0: 00:34:45

Not quite.
So somewhere in the middle of that is a migration tool, which we've added in 24.0. And so the migration tool takes the legacy wallet and converts it entirely into a descriptor wallet so you can continue to use it.
When I was writing this tool, one of the things I wanted to do was make sure that this thing can work even after the legacy wallet has been removed.
So there's an open PR to replace the database back end that it uses from BDB to a self-written implementation of just a BDB parser.
So after we've removed the legacy wallet and you get the error saying, hey, we can't load this anymore, it will also say, but you can migrate it.
If you click this button or type this command, we will convert your wallet into a descriptor wallet, and you will not be missing anything.
You won't be missing anything if you do that.
So that's the goal for this whole rollout of descriptor wallets, or the plan, that is hopefully going to happen soon.
Because developers have been getting increasingly annoyed with BDB.
And that conversion tool will stay in the codebase forever?
Yeah, so this conversion tool will live in the codebase forever, but it's a very small subset of all the legacy wallet things that it won't be hard to maintain, and it can just live in its own couple of files.

Speaker 1: 00:36:00

Got it.

Speaker 2: 00:36:01

So one of the issues with the legacy wallets, for example, is that we simply had a chain of keys, and we don't know what output they were used for.
So each key could be any type of output.
And In descriptor wallets, of course, a big advantage is that we store explicitly what output we're generating.
So are descriptor wallets more performant then?

Speaker 0: 00:36:25

Sometimes.
We don't really have benchmarks for this, so it's hard to say.
So one of the things with legacy wallets is that there was no, there's no like explicitly defined set of scripts that we are watching for.
And actually this set was unbounded for a very long time.
So there's the obvious ones like, So the way that it would work is you would see some script, and we'd say, figure out what kind of script is this.
Like, is it P2PKH?
Is it P2WPKH?
Is it P2SH?
Or is it a bare multisig?
And then we would say, do we have any keys that would match this?
So if we got like a P2PKH script, we'd be like, do we have any keys whose hash matches this one?
And be like, if we do, okay, this is ours.
And so that actually, that's pretty easy to determine the set of scripts for you.
You just hash all your keys, right?
Same thing for P2WPKH and nested P2WPKH.
But when you get to bare multisig, so bare multisig is a script that's just the multisig script, but in an output and not behind a P2SH.
And the way we would look at those is, does any of our keys appear in this bare multisig?
And then do we have enough keys in the bare multisig to sign it?
So you could have, I think the standardness is up to three keys, but I believe this would work on any bear multi-sig that shows up in the blockchain, which is up to 15 keys.
And we only need whatever the N number is.
So this is literally infinite.
You could have one of 15, one of my thousand keys is in here, and then I have 15 unrelated keys.
And our wallet would be like, yep, that's ours.
So that turns the set from, OK, we can calculate to just hash all the keys to it's literally any bear multi-sig.
And this posed a huge problem.
And then someone had the foresight of saying that if we wanted bare multisigs, then you had to explicitly import them to your wallet.
But this was a breaking change, right?
So if you were, for some reason, expecting a bare multisig to be seen by your wallet as belonging to it.
And then you upgraded that new version that had this change of required explicit bare multistake import, suddenly those would no longer be yours.
But also, no one does bare multistake, so it doesn't matter.

Speaker 2: 00:38:45

Yeah, because they write the data now to inputs instead.

Speaker 1: 00:38:50

Does any of this matter?
I guess we'll, you know.
Awesome.
Thank you for the discussion.
We covered a lot of ground here.
Good talking with you.
All things wallet.
I don't know if we can talk about wallets anymore.
It's a lot of wallet stuff.

Speaker 2: 00:39:12

It feels like, I hope nobody's shocked when they Listen to us talking about the Bitcoin Core wallet.
There seem to be a lot of construction sites.

Speaker 1: 00:39:21

I think when you're so close to something, you see all the flaws.
But I stand by the fact that it has the most review and the highest bar in terms of security.

Speaker 2: 00:39:34

I think that it definitely benefits from a lot of the people that actually do use Bitcoin Core Wallet, being the Bitcoin Core developers.
And frequently when they have some sort of feature they want, they come in and look at it and implement something for it to scratch their own itch.
And yeah, so that's I think where we get some of the more unique features and Definitely also some of the unique review.

Speaker 1: 00:40:02

Cool.
Well, I hope you enjoyed the episode and I think we're going to try to get another one in soon.
I don't know.
If we start doing them once a week, what happens to us?

Speaker 2: 00:40:10

I don't know.
People will probably get bored.

Speaker 1: 00:40:15

Hopefully not us.
All right.
We'll see you
