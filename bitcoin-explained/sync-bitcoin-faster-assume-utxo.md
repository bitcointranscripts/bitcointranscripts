---
title: Sync Bitcoin Faster! Assume UTXO
transcript_by: Sjors, edilmedeiros
media: https://www.youtube.com/watch?v=S9pk_NqKCBE
tags:
  - bitcoin-core
  - assumeutxo
speakers:
  - Sjors Provoost
  - Aaron van Wirdum
date: 2020-10-23
episode: 14
summary: "On this episode of The Van Wirdum Sjorsnado, Aaron and Sjors discuss “Assume UTXO, ” a proposal and project by Chaincode Labs alumnus James O’Beirne.\n \nOne of the biggest, if not the biggest, bottlenecks for scaling Bitcoin is initial block download: the time it takes for a Bitcoin node to synchronize with the Bitcoin network, as it needs to process all historic transactions and blocks in order to construct the latest UTXO-set: the current state of bitcoin-ownership.\n \nAaron and Sjors explain some of the ways sync-time has been sped up over time. First, sync-time was improved through “Headers First” synchronization, which ensures that new Bitcoin nodes don’t waste time validating (potentially) weaker blockchains. In recent years, sync-time has been improved with “Assume Valid, ” an optional shortcut that lets nodes skip signature verification of older transactions, instead trusting that the Bitcoin Core development process in combination with the resource-expensive nature of mining offers a reliable version of transaction history.\n\nFinally, they explain how the security assumptions underpinning Assume Valid could be extended to allow for the potential future upgrade Assume UTXO to offer new Bitcoin Core users a speedy solution to get up to speed with the Bitcoin network, sacrificing a minimal amount of security during the initial bootstrapping phase."
---
## Introduction

Aaron van Wirdum:

Sjors, this week we are going to create a carbon copy of the Chaincode Podcast.
They had an episode with James O’Beirne on AssumeUTXO, and we are going to make an episode on AssumeUTXO.

Sjors Provoost:

And we are going to follow roughly the same structure.

Aaron van Wirdum:

We're just going to create the same podcast, just with our voices this time.
We're gonna do it step by step.
First step is, Headers First.
That's how they did it, so that's how we're going to do it.

Sjors Provoost:

Right.
And by first step you mean we're going to go back in time and look at some improvements on how to download the blockchain quickly and safely?

## The Problem of Syncing a Bitcoin Node: Headers First

Aaron van Wirdum:

Yeah.
That's basically the problem that we're solving here.
Well, not you and me.
Well, maybe you a bit, but definitely not me, but its the problem of syncing.
So when you turn on your Bitcoin Core node, then the first thing your node's got to do is...
Well, other than connect to the network which we discussed last week.
Then the next thing is it needs to be able to communicate with the network.
It needs to download the blockchain.
It needs to be aware of the state of the network, basically.

Sjors Provoost:

So the most naive way to do that would be to say to other peers, just give me everything you've got.
And then you get gigabytes and gigabytes and gigabytes and terabytes of blocks and headers and random stuff.
And your hard disk is full and you crash.
So that's not the right way to do it.
So I think the initial version of Bitcoin before it was even called Bitcoin Core, it would just ask nodes for a header and then it got a header and it would ask nodes for a block and it would get that block.
And it would ask for the next header and it would just sequentially get all the header, sequentially, get all the blocks.

Aaron van Wirdum:

One header at a time followed by the same block one at a time.

Sjors Provoost:

Yeah, I think so.
I might be wrong on this, but it doesn't really matter for what we're about to explain.

Aaron van Wirdum:

So what the problem with that?

Sjors Provoost:

Well, the problem with that is you don't know if you're following a dead end.
So I might be...
We all know there's a lot of blocks out there but I could give you...
When you start syncing I could give you the first block and then I could just mine the second block and the third block myself at a very low difficulty.
So I could just keep the Bitcoin difficulty at one and just buying a chain with a million blocks in it.
And I would give them to you one by one by one by one, and you would check it and you'd be happy and you would check it and you'd be happy.
And I would send you megabyte size blocks or even bigger with all the secret stuff in it.

Aaron van Wirdum:

Sure.
Just to be clear, even though the difficult is low, that doesn't make it any easier for my nodes to verify the transactions?

Sjors Provoost:

Exactly.

Aaron van Wirdum:

It's still going to cost a lot of computational power?

Sjors Provoost:

So it's very cheap for me to generate a fake chain with very low difficulty.
And I can just keep you busy for a long time.
So one way to get rid of that problem is first ask for headers not the entire block, but just headers.

Aaron van Wirdum:

Just to be clear, this isn't really a problem in itself? Because in the end I would still, as a new node compare blockchains, and then pick the one with the most difficulty.
It's just you need to verify all of the chains first before would make the pick? That's the problem here.

Sjors Provoost:

But I could turn on Amazon and give you a million chains like that.
So it would be very hard for you to find the real one.
So the idea then is you download the headers instead.
So headers are a lot smaller.
So I can give you a bunch of nonsense there, but you can quickly shop between headers and see the total difficulty in it.

Aaron van Wirdum:

Right.
So instead of downloading and verifying all the chains and then picking the one with the most proof of work, I'm first checking out, which chain has got most proof of work.
So I'm basically inverting it, right?

Sjors Provoost:

Yes, exactly.

Aaron van Wirdum:

And then the one with the most proof of work, that's the one I'm actually going to validate.

Sjors Provoost:

Right.
Because so far you just have SPV security.
So you just know which one has the most proof of work, but it could be invalid.
So in that case, you start downloading one block at a time.
Or in fact, because you already have all the headers, you can download lots of blocks at the same time, from different nodes in parallel.
But you have to verify them in sequence.
And then if you run into an invalid block, okay, then you say this header chain might have the most proof of work, but it's not valid.
So I'm going to go to this second most proof of work header chain and ask for the blocks.
It's mostly going to be the same maybe except the last few.

Aaron van Wirdum:

You mentioned SPV security very briefly.
Technically that would be possible, right? Even though Bitcoin Core doesn't do that right now.
It would be possible to bootstrap your nodes get started with SPV security at first.
And then only after you're done validating all of the blocks you got full security?

Sjors Provoost:

Yeah, no, you could, you could.
But I don't think you would know your transaction history because you do need the blocks for that.

Aaron van Wirdum:

But you would still have SPV security and there was a proposal to implement something like this in Bitcoin Core a while ago.

Sjors Provoost:

Yeah, I think so this was by Jonas Schnelli, I think four or five years ago, an attempt to at least start up in SPV mode.
And then I guess if you create a new address from scratch, then you know it's history.
So then when the next block comes in and you see a transaction to that address, then you know that you have a balance.
You can't rescan any old addresses, but you can see anything new that comes in.
Because you're going to download all the real blocks after yeah.
Starting at the present basically.

Aaron van Wirdum:

You're at least sure that more miners think it's a valid transaction or at least they're spending hash power telling you it's a valid transaction.

Sjors Provoost:

Yes.

Aaron van Wirdum:

So even though you don't have full security, it's a little bit better than nothing.

Sjors Provoost:

Right.
And of course it's definitely enough to receive it.
And then just to assume that it's fake, but you can just sit on it for a while.
But in the meantime you would be validating all the older blocks.

Aaron van Wirdum:

Yeah.
But just to be clear, Bitcoin Core doesn't do this right now.

Sjors Provoost:

No, it doesn't.

Aaron van Wirdum:

Right now it's just a trick to avoid having to download all of these fake chains potentially instead only download the chain that has the most proof of work.
That's that's what Headers First is?

Sjors Provoost:

Yeah.

## Assume Valid

Aaron van Wirdum:

Now next step.
So there's a thing called Assume Valid.

Sjors Provoost:

That's right.

Aaron van Wirdum:

What is Assume Valid?

Sjors Provoost:

So Assume Valid is a block hash that is encoded in the software.

Aaron van Wirdum:

Just to be clear, this is actually in Bitcoin Core today?

Sjors Provoost:

Yes.
It's been there for a few years.
So it, it is a hash of a recent block as in recent, before the release.
And a lot of the different Bitcoin Core developers and anybody else who is on Github can see what that hash is.
And they can check for themselves whether that hash is real.
And if you're a new user and you start a Bitcoin Core, it's going to sync all the headers, it's going to get all the blocks.
And if that particular hash is in the chain, then it will not verify the signatures.
So it's not a checkpoint.
The hash does not have to be out there.
But if it's out there, you don't verify any of the signatures up to that point.
So it's a lot it faster to sync that way.
Or a lot less slow, I would say.

Aaron van Wirdum:

Do you still download the signatures?

Sjors Provoost:

You download everything.

Aaron van Wirdum:

You download everything?

Sjors Provoost:

The whole blockchain.

Aaron van Wirdum:

So its just a shortcut for syncing is that you do not verify the signatures up until that point?

Sjors Provoost:

Exactly.

Aaron van Wirdum:

So what you are doing is you're still checking the proof of work.
You're still checking that miners actually produce the blocks by expending energy.
And you're checking that it is the longest chain.
And you're also checking all of the transactions in order to construct the UTXO set, which is the current state of balances.

Sjors Provoost:

Right.
Money cannot come out of nowhere basically.
So you check all that stuff, but you do not check the signatures.

Aaron van Wirdum:

So you're not checking that the valid owner of each coin in any part of history was actually the correct owner.
For that you're trusting essentially on the miners, as well as on the developers side.

Sjors Provoost:

You're fully trusting the developers.
Well, you're trusting that the developers, if they were to put in something that's not real, somebody would notice that.
Because you can see this source code and it's just one line.
And if that has a hash in it that doesn't exist, well, then you should be worried.
And it would be quite weird even then, because it would have to be a chain with more proof of work.
Otherwise you would never see it.
So some evil developer would have to produce a chain with more proof of work than the real thing in order to trick some future user, but risk everybody noticing it.

Aaron van Wirdum:

Yes.
Well that's why I mentioned also the miners.
Like you still got to produce the proof of work, right?

Sjors Provoost:

Yeah, exactly.

Aaron van Wirdum:

So why Sjors would we trust guys like you?

Sjors Provoost:

You don't.
I mean the saying is: don't trust, verify.
But you're relying on that, somebody's done that.
Because don't forget that you're still downloading piece of software from the internet.
Which could have a line of code in there that says, just send all the Bitcoins to me.
So you have to check for sneaky things by the developers in general.
But that particular sneaky thing would be extremely easy to see.
Because it's one place in the code base that has a hash in it and everybody can reproduce it.
And if you don't like this and you don't have to like this, you start Bitcoin from scratch with dash assume valid is zero.
And then it will validate all the signatures.

Aaron van Wirdum:

Exactly.
That's just what I was about to ask.
If you don't want to put this trust in developers, you can still do it yourself?

Sjors Provoost:

Yeah.
But keep in mind, so you're not putting that particular piece of trust in the developers, but you still download the binary file from the internet.
So you are putting trust in the developers.

Aaron van Wirdum:

I mean, that depends, right.
You could check the source code if you really wanted to, and then...

Sjors Provoost:

Yes, you should, and then you see this hash.

Aaron van Wirdum:

Compile into binaries if you want to.

Sjors Provoost:

You can do that and then you'll see this hash and you trust that part of the source code isn't sneaky.
Because you can look at the source code, but there could be some really sneaky obscure C plus plus code in there that you have no idea what it's doing and it's stealing your coins.

Aaron van Wirdum:

You're underestimating my ability to check for very sneaky C plus plus source code.

Sjors Provoost:

Well, that's great.
We need more people like you to make sure that doesn't happen.

Aaron van Wirdum:

I wish that was true.
So this is actually in Bitcoin Core and its been in Bitcoin Core for a while.

Sjors Provoost:

Yeah, I think a couple years.

Aaron van Wirdum:

And apparently everyone's comfortable enough with this.

Sjors Provoost:

I don't know.

Aaron van Wirdum:

Looks like it.

Sjors Provoost:

And I don't know if people use the feature.
They might turn it off.

## Assume UTXO

Aaron van Wirdum:

So now a newer idea, which is based on Assume Valid is James O'Beirne's AssumeUTXO.

Sjors Provoost:

Yes.

Aaron van Wirdum:

So what is the difference? What is AssumeUTXO then?

Sjors Provoost:

Well here, the UTXO set, as we've said a couple times is the collection of coins that exist right now.
So every time you send somebody money that creates a UTXO and it destroys the UTXO that you send from.

Aaron van Wirdum:

It's the current state of balances is how I generally call it.

Sjors Provoost:

Yeah.
Although, yeah...

Aaron van Wirdum:

Yeah.
I know.
Technically, you object to the term balances.

Sjors Provoost:

Well, because balance is something you can add and subtract to, but these UTXOs are destroyed all the time.
So it's like you have a bank account and the bank account is destroyed when you use it.

Aaron van Wirdum:

Sure.

Sjors Provoost:

But in general, the idea is that every time...
The only way you can reconstruct the UTXO set.
So the only way and find out which coins exist right now is to replay everything from scratch.
So you have to take the first block, see which coins it creates, which coins it destroys.
Then the second block, see which coins it destroys, which coins it creates, et cetera, et cetera, et cetera, et cetera.
And that takes a long time and you can only do it sequentially.
You have to start at the beginning.
You have to go to the end.
You cannot do it in parallel because you don't know if block 100 hundred thousand.

Sjors Provoost:

You don't know if it's valid because you need to know what coins existed at one block before it.
So this is annoying because it takes a long ass time to sync the whole blockchain.
So what AssumeUTXO does, is it takes a snapshot of this UTXO set at a certain height, maybe just before the release or a bit older.
And then when your node starts, it starts from that point.
So it skips...
Initially skips the whole history.
It starts from this snapshot and then it just checks the next block and the next block and the next block and the next block until it reaches the tip, the most recent block.
So then you know exactly your balances and you can start using it.
But in the meantime, in the background, it starts at the Genesis block, goes all the way to the snapshot and make sure that the snapshot is correct.
And if the snapshot is not correct, it starts screaming.

Aaron van Wirdum:

I'm assuming it still does the Headers First syncing, right? First it checks out which chain is the longest one.

Sjors Provoost:

In fact it has to, because in order to load the snapshot, it must already have the headers at that point.
So it has to have the headers up until the snapshot before it can even load the snapshot.

Aaron van Wirdum:

Right.
And then with Assume Valid, it still did all of the UTXO set constructing.
It still replayed all of the transactions.
It just didn't check for the signatures.
It just skipped its signature validation.
And now with AssumeUTXO, at least initially it skips all of it.
It skips the transaction replaying as well as obviously, then also the signature checking.
So just takes the UTXO set and from there on out constructs, the blockchain based on the newer blocks that have been found since then.

Sjors Provoost:

Exactly.
And so you're back to where everything started.
As soon as that backlog checking has been done, then you're basically at the same trust as you are now.
However you could...
And this gets into trade offs.
Like, do you really want to check all the history? Because there are a lot of things you can know without checking history.
So there's no plan right now to not check history because that's still a bit controversial.

Aaron van Wirdum:

You mean check history after...

Sjors Provoost:

Before the snapshot.

Aaron van Wirdum:

Yes.
You basically check the snapshot.
Then you check what have happened since the snapshot and once you've constructed the current version of the UTXO set and the current version of the blockchain.
Then you go back to block number one and start to check if your assumption of the UTXO set was actually correct.

Sjors Provoost:

That's right.
And so the question is, could you eventually in the future opt out of doing that? And what are you sacrificing when you do that? And well, some things you're not sacrificing.
So the nice thing is if you start at the snapshot and you create a new address and you receive coins on it and they get into a block, then you kind of know that block is valid.
At least unless there's another chain out there because otherwise like a lot of miners are wasting a lot of proof of work on a chain that's not valid.
Which could be true.

Aaron van Wirdum:

Which could be true.
Which is a trade off.
You're trusting that miners are being honest there, you're trusting that they're not burning resources just to screw with you.

Sjors Provoost:

Not screw with you, screw with everyone.
But there could be some conspiracy where the snapshot is fake and the core developers and the miners collude and create a fake snapshot that has a couple of extra coins in it that all the miners agree that they will approve blocks with that coin in it.
So you could sneak in a hard fork.
That's the scary thing about it, which is why, again, you need people to check whether the snapshot is real.
You can either do it yourself with this back validation or you can go in and...
Or you can rely on the fact that other people are looking at the source code and see this one particular line, which if it contains something ridiculous, there's a problem.
And again, the same story with the headers, that still need to match.
So somebody would have to spend a whole lot of proof of work and get sneaked that fake snapshot in.

Aaron van Wirdum:

So this is not included in Bitcoin Core right now?

Sjors Provoost:

No, in fact, all of this is quite new.
So I think the current version of Bitcoin Core has a way to create a snapshot.
But there's nothing you can do with that snapshot.
And then not the version that's coming out now, but the version that might come out like early next year should have a way to...
Probably will have a way to load a snapshot.

Aaron van Wirdum:

What does load a snapshot mean?

Sjors Provoost:

So this UTXO snapshot, the set of coins is a couple gigabytes and the only way you can get it is to download it from someone.
It's not included in the source code and there's no way to serve it over the peer-to-peer network yet.

Aaron van Wirdum:

The only thing that's included in the source code would be the hash of the UTXO set? Not the UTXO set itself because it's too big.

Sjors Provoost:

Right.
And so initially, maybe that UTXO set is just a torrent that people can host.
It's very easy to check a torrent, because it also has a hash.
Or one use case for that could be say, if you're running a BTCPay server, if you're spinning that up for the first time, it's really, really time consuming to have to download the entire blockchain.
But then you probably want to skip validation of the older stuff.
Because if you're running that server you're probably also running a node somewhere else.
So you can still compare that, that you're actually looking at the same chain.
So that could be a good use case for it.
And then it's nice that the BTCPay server thing just downloads the three gigabyte file and then starts syncing from there, save you like two weeks.
Because all these web servers that are incredibly slow.

Aaron van Wirdum:

So right now, Bitcoin Core can make snapshot of a UTXO set, but it doesn't actually do anything with it?

Sjors Provoost:

Yep.

Aaron van Wirdum:

Then in an upcoming release it's going to be able to download UTXO set?

Sjors Provoost:

No it's going to be able to load a UTXO set that you downloaded.
Somewhere.

Aaron van Wirdum:

And then maybe in the future version after that, then it's going to complete the package and you might have something called Assume UTXO in Bitcoin Core.

Sjors Provoost:

One way such a future could look is the nodes.
Every node that wants to would serve this snapshot.
Probably not automatically because it's pretty big.
It's like couple gigabytes.
But any node that wants to could serve the snapshot and then there's a peer-to-peer protocol to download the snapshot automatically.
And so when you start a new node, it would automatically find the snapshot, use the snapshot, sync to the tip, show you some orange blinking thing, probably.
And then sync from the start to the snapshot and then show you a nice green blinking thing.

Aaron van Wirdum:

Is this controversial at all? The fact that there are some trade offs there, some security trade offs.
Even though they're small and temporary, they're there.
Do you think this is controversial at all?

Sjors Provoost:

I don't know.
I mean, usually with this kind of features, first of all, it's experimental.
So that means you probably need to do something to turn it on.
My guess is, once it's done to the point that I just described, it's probably still going to be off the first time.
And then if people start objecting to it or not, that's sort of the thing you need to see.
I mean, something is controversial when people decide it's controversial.

Aaron van Wirdum:

But that hasn't been decided yet then?

Sjors Provoost:

Not that I know, but there's only a handful of people who actually grasp this feature.
So it might be a bit early.
In the longer run something that's been an ongoing discussion for ages is the idea of committing to the UTXO set inside the blockchain itself, a UTXO commitment.

Aaron van Wirdum:

I've heard of that.

Sjors Provoost:

That certainly is controversial.
I don't think...
I don't know if anybody is opposed to it in principle, but it's certainly controversial depending on how you do it.
Because what you want to prevent is sort of the scenarios we discussed before, right? The scenario where the blockchain is too big to check for everybody and then a bunch of miners and developers decide to give themselves some coins and they get away with it.
Because not enough people verify the entire history.
So that's a risky part of it.

Aaron van Wirdum:

How would that work with embedding? Sorry, it's embedding the UTXO set into the blocks?

Sjors Provoost:

You're not embedding it.
You're embedding a hash into the block.

Aaron van Wirdum:

Sure.

Sjors Provoost:

So every block would contain, I guess in the coinbase transaction a hash of the UTXO set or some other derived thing of the UTXO set.

Aaron van Wirdum:

What's the benefit of that?

Sjors Provoost:

Well then instead of relying on what's in the source code, this hash, you would rely on what's in the blockchain, this hash.
That's I guess, you make it part of consensus and a block is not valid if the hash is not valid.
So you would reject blocks that have an invalid hash rather than reject code that looks fishy.
I think it's a different thing, but there are quite...
There are very different ways that you can put stuff in a block.
It could be straightforward as a hash, but it could also be something a little bit more indirect, something that if you know...

Sjors Provoost:

So if you look at the block and you see this number, you do not know the UTXO set and you can't download the UTXO set using that information.
But instead you have to download...
You have to process the whole blockchain from the Genesis block to make sure that that thing in the blockchain is valid.
But then the question is what is use going to be? There's some tricky trade ups there.
You should ask Peter Todd at some point, because he's thought about that stuff a bit more.

Aaron van Wirdum:

At some point I will.

Sjors Provoost:

All right.

Aaron van Wirdum:

We've gone off the rails.
But I think we covered everything.

Sjors Provoost:

Yeah.
In general, it's one thing that people complain about when they hear about Bitcoin Core.
Its like, "Oh my God, I need to download the whole blockchain." And then you get this tradeovers do you want people to just put up with that? Do you want to make it slightly less annoying?

Aaron van Wirdum:

Yes.
At a trade off.

Sjors Provoost:

And then the smallest possible trade off.
So I think this is a very interesting project, so I'm happy to test it.
That's usually what I do.

Aaron van Wirdum:

Good.

Sjors Provoost:

Test it.
Try to break something and then complain or get up.

Aaron van Wirdum:

All right.
