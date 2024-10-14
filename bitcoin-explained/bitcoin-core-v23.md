---
title: Bitcoin Core 23.0
transcript_by: edilmedeiros via review.btctranscripts.com
media: https://www.youtube.com/watch?v=bMMG91sJXpM
tags:
  - bitcoin-core
speakers:
  - Sjors Provoost
  - Aaron van Wirdum
date: 2022-04-24
episode: 56
aliases:
  - /bitcoin-magazine/bitcoin-explained/bitcoin-core-v23
---
## Intro

Aaron van Wirdum: 00:00:20

Live from Utrecht, this is Bitcoin Explained.
Sjors, are we still making a bi-weekly podcast?

Sjors Provoost: 00:00:28

I mean, it depends on what you mean by bi.
It's more like a feeling, right?

Aaron van Wirdum: 00:00:32

We make a podcast when we feel about it these days.
Is that the rule?

Sjors Provoost: 00:00:36

No, it's also when we're not traveling or sick or whatever.

Aaron van Wirdum: 00:00:40

Or we don't have a good idea for a podcast.
This is a good moment actually to maybe make a call to our audience.
We will take requests for topics, or at least we will consider requests for topics.
If any of our listeners have good ideas of things that they want to have explained by us, just let us know on Twitter, and we will consider it.
All right.
So, the last one was, I guess, a month ago.
I don't know when this one will be published because I think our editor is now traveling.
He's in Amsterdam.

Sjors Provoost: 00:01:12

Oh, okay.

Aaron van Wirdum: 00:01:12

He's coming to our meetup tonight.
We're recording this on Wednesday, what is it?

Sjors Provoost: 00:01:17

Wednesday, 20th of April.

Aaron van Wirdum: 00:01:19

And that will be the biggest meetup in all of Europe in Amsterdam tonight, Sjors.
Isn't that exciting?
We recently discovered that it's probably the biggest one in Europe, so now that's our main marketing push.

Sjors Provoost: 00:01:31

Interesting.
I guess that's because there's nothing happening in Prague at the moment?
Because they have pretty big meetups.

Aaron van Wirdum: 00:01:36

We didn't fact-check it, but I think it's the biggest one in Europe.

Sjors Provoost: 00:01:42

But you mean the biggest Bitcoin meetup, which then meets some narrow definition of Bitcoiner or Bitcoin.

Aaron van Wirdum: 00:01:49

Just the biggest Bitcoin meetup we know of.
I don't think we're doing very narrow definitions.

Sjors Provoost: 00:01:54

There's Bitcoin Wednesday, which has nothing to do with Bitcoin.

Aaron van Wirdum: 00:01:58

Right.
Yeah, that's also in Amsterdam.
I mean, is that bigger than ours?

Sjors Provoost: 00:02:02

I don't know.

Aaron van Wirdum: 00:02:03

Who knows?

Sjors Provoost: 00:02:03

Could be.

Aaron van Wirdum: 00:02:04

All right, let's get to the actual meat of this episode.
We are going to discuss Bitcoin Core 23, and we'll probably have this published on the day that it is released because that's what we're going to be discussing.

Sjors Provoost: 00:02:19

That's always a bit of a risky statement because it can take a while before it gets released.
But hopefully, it'll be at the same time.

Aaron van Wirdum: 00:02:25

At the time we're recording this, we're on release candidate 5.
I don't think there have been many Bitcoin Core releases that required more than five release candidates, right?

Sjors Provoost: 00:02:34

Indeed.

## Bitcoin Core Release Candidates

Aaron van Wirdum: 00:02:35

This is not in the show notes, but maybe that's a good starting point.
Sjors, what is actually a release candidate?

Sjors Provoost: 00:02:43

It's a candidate for a release, to put it simply.
It's a way for the Bitcoin Core developers or any software project to allow experienced users to test the software.

Aaron van Wirdum: 00:02:58

Right, and what are they testing it for?

Sjors Provoost: 00:03:00

Well, they're testing something that's going to be as close to the final version as possible.
In fact, the very last release candidate is eventually copied and called the actual release.

Aaron van Wirdum: 00:03:08

In this case, release candidate 5.
I think they're basically guys like you, Bitcoin Core developers and other expert users maybe, they're sort of trying out the software, looking for bugs.

Sjors Provoost: 00:03:24

Yeah, exactly, or changes that are not correctly documented.
For example, if you're running a Bitcoin ATM or something, and you're relying on a Bitcoin Core node to do all sorts of automated stuff, then you would test the new release candidate to make sure that all the automated stuff you were relying on still works and there's not some subtle change that causes your ATM to send free money to its users.

Aaron van Wirdum: 00:03:44

Right.
That lasts for about a week, and then, if no issues are found, the latest release candidate is essentially rebranded to whatever the new Bitcoin Core release is.

Sjors Provoost: 00:03:54

An actual new release is made, but it has the same code.
The only thing that changes then is the version number.

Aaron van Wirdum: 00:04:02

Okay.
So Bitcoin Core 23, that's where we're at.
For those who don't know, Bitcoin Core releases a new version roughly every six months.
And the new Bitcoin Core release will basically include whatever was ready at that time.
Bitcoin Core doesn't wait for specific futures; once every six months, whatever's ready is in there.

Sjors Provoost: 00:04:26

Yeah, that's right.

## Bitcoin Core choice of communication ports

Aaron van Wirdum: 00:04:27

Okay, so we're going to discuss some of the most notable changes.
Let's begin.
Sjors, we're going to begin with something about ports?

Sjors Provoost: 00:04:45

Yes.
As you may or may not know, Bitcoin Core listens to other nodes, if it's on a public network, on port 8333.

Aaron van Wirdum: 00:04:52

By listening, you basically mean communicating with, right?
Or what's more?

Sjors Provoost: 00:04:59

Listening means that it is listening to the outside world.
So you can actually connect to it if you're in the outside world.
A node could also just be on the internet but not listen to anyone in the world.
So you might not know where it is, and even if you send a message to it, it won't hear you.

Aaron van Wirdum: 00:05:12

Right, so if I'm running a Bitcoin Core node and it's a listening node, which is like a setting?

Sjors Provoost: 00:05:17

It's actually the default.
However, in your home situation, it won't listen by default.
That's not because of a setting in Bitcoin Core, but other reasons we'll probably get into.

Aaron van Wirdum: 00:05:26

We'll get into that in a bit.
But essentially, if I'm running a Bitcoin Core listening node- let's just call it that for now- and you're also running a node, and you want to communicate with my node, then you're going to connect with my node on port 8333, right?
So far so good?

Sjors Provoost: 00:05:44

That's right.

Aaron van Wirdum: 00:05:45

Okay, so what is a port?
What does this actually mean?

Sjors Provoost: 00:05:49

A port is part of the TCP protocol, the TCP/IP protocol, basically.
The idea is an IP address is where the computer is.
That's what it tells you.
The port is actually just a thing inside of the messages that you're sending to it.
The internet uses packages, and these packages have a certain structure.
The beginning of the package says which port you want to communicate on.
It's just a convention, a kind of a way to talk to different services on the same machine.
One server on the Internet might run a web server, an email server, and a Bitcoin node.
One convention you'll use is if you want to talk to the web server, talk to port 80 or port 443.
If you want to talk to the FTP server, talk to port 21.
If you want to talk to the Bitcoin node, talk to port 8333.
So it's like if you're sending somebody a letter and you write down the number of the office they're in.

Aaron van Wirdum: 00:06:51

Or the name, in that case.
There are several people living on the same address, and then the name actually specifies who it's for.

Sjors Provoost: 00:06:59

Yeah, maybe, too.
These are conventions.
IP addresses are a scarce resource; they're distributed across the world.
So, there are some centralization involved there.
But when it comes to ports, there are standards and conventions out there, but your machine decides what it does on which port because nobody on the outside can tell you what to do.
It's just a very bad idea to use the wrong port.

Aaron van Wirdum: 00:07:21

When your computer connects with my computer, it tells my computer I'm going to use port 8333, which is just a conventional specification of something we chose.
And at that point, my computer knows he wants to connect to Bitcoin Core, right?

## Port Filtering

Sjors Provoost: 00:07:38

Yes, because Bitcoin Core told your computer that it wants to listen on that port.

Aaron van Wirdum: 00:07:42

That's the convention, but there's a problem with this?

Sjors Provoost: 00:07:49

Yeah.
One thing is that internet providers and others can filter the internet traffic.
One way you can filter the internet traffic is by looking at which port a package is going to.
It's very easy to see; it's at the start of each package.
And you usually have to check that anyway for other reasons.
One thing an internet provider could do is to say "we don't like Bitcoin, let's just block port 8333 specifically".

Aaron van Wirdum: 00:08:13

So, in a Bitcoin-hostile future, where perhaps Bitcoin is banned, and ISPs want to stop people from using Bitcoin, this would be one way for them to do it.

Sjors Provoost: 00:08:25

Yes, this would be the easiest, the lowest-hanging fruit way to do it.
It's certainly not a very effective way to do it, but it's one start.
Certainly not the only thing they can do.

Aaron van Wirdum: 00:08:35

And the reason it's not very effective is because we have the option to use different ports.

Sjors Provoost:

Exactly.
That's the cat and mouse game.
If they make that move, then the second move is we start using other ports.
But in order to prepare for that situation, one of the changes that are in the new version is that Bitcoin nodes will connect to other nodes that have a different port.

Aaron van Wirdum: 00:08:59

So they don't do that now?

Sjors Provoost: 00:09:00

They will do it if you tell it to, but one thing we talked about in the earlier episode is that your node keeps a list of other nodes that it could connect to, and from that list, it tends to pick nodes that have port 8333 and only if that fails after a long time, then it'll try other ports.
That's the preference that's being removed now.
It'll just try any other node, regardless of what port it has, which means that if we move to a future where nodes are listening on different ports, it's going to be less friction.

Aaron van Wirdum: 00:09:30

So, right now, you're running a node.
By default, your node will try to connect to other nodes and prioritize port 8333 nodes.
So, if I'm running a node on another port, and everyone is like you, then I will just not have any inbound connections from other nodes because everyone's ignoring me because I'm not using 8333.
Is that right?

Sjors Provoost: 00:09:52

Yeah.

Aaron van Wirdum: 00:09:53

And this is changing now.
This changes in the new Bitcoin Core, where you won't prioritize 8333.
You'll connect to whatever node.

Sjors Provoost: 00:10:03

Yeah, exactly.
There is, I think, a list of ports that we don't connect to because it could be perceived as an attack.
But I think that list is pretty short.

Aaron van Wirdum: 00:10:13

So this is basically preparing for a potential dystopian future where Bitcoin is very much...

Sjors Provoost: 00:10:19

Bitcoin is always preparing for a potentially dystopian future.

Aaron van Wirdum: 00:10:22

And it should, yeah.
But just to clarify that for the listener.

Sjors Provoost: 00:10:26

Yeah, but also, to clarify this, this is not going to make a difference.
It's just one chess move, and the countermove is pretty obvious.
There are all sorts of ways for internet providers to see that you're running a Bitcoin node, not just the port you're on.
But that's the easiest way, and, you know, enemies are lazy.

## CJDNS

Aaron van Wirdum: 00:10:43

Okay, well, so that covers that change, correct?

Sjors Provoost: 00:10:46

Yeah.

Aaron van Wirdum: 00:10:47

All right.
Let's move on to the next point.
CJDNS.

Sjors Provoost: 00:10:58

I have no idea what it really is, to be honest.
It's in the list of Tor and I2P that we talked about.
It's not a complete replacement of these things, but it's sort of similar-ish.

Aaron van Wirdum: 00:11:11

It's some kind of anonymity network that you can use if you want to use the internet more privately.

Sjors Provoost: 00:11:17

Exactly.
If you know what that is, now you can use it with Bitcoin Core.
I think that will be the first step to put it.

Aaron van Wirdum: 00:11:25

So, Bitcoin Core has included support for CJDNS.

Sjors Provoost: 00:11:30

That's right.
A couple of episodes ago, we talked about the address gossip messages.
We discussed how we used to be able to communicate IPv4 addresses, IPv6 addresses, and Tor v2 addresses, and how it wasn't possible to communicate Tor V3 addresses because they were too long.
They come up with a new standard called address message format number two, which allows you to send addresses of very different sizes and easily add new networks to that.
This is just one of the new networks that's added to it.
You can just use it, you can also gossip them around and things like that.

Aaron van Wirdum: 00:12:08

Details about CJDNS itself is not something that we can provide to the listener.
That's outside of my expertise, and I think outside of yours as well.

Sjors Provoost: 00:12:22

Yeah.

Aaron van Wirdum: 00:12:23

Okay.
Bitcoin Core supports a new privacy or is it new?
Do you know if it's new?

Sjors Provoost: 00:12:28

I don't think it's new.

Aaron van Wirdum: 00:12:29

It just supports an additional privacy network if you want to use it.
Great.
I like it.

Sjors Provoost: 00:12:38

Next.

## RBF transactions and fee estimation algorithm

Aaron van Wirdum:

There's an upgrade in the fee estimation algorithm in Bitcoin Core.
Whenever you want to make a transaction, Bitcoin Core has the option to increase or decrease the fee depending on how fast you want your transaction to confirm, which depends on how many transactions are in the mempool or how high the fees were in recent blocks.
I think these are some of the inputs.

Sjors Provoost: 00:13:09

It looks at how high fees were in recent blocks, but it also checks how long it took before it first saw it in the mempool and when it was in a block.
I'm not exactly sure.

Aaron van Wirdum: 00:13:22

That has been upgraded to include RBF, replaced by fee transactions.
Is that right?

Sjors Provoost: 00:13:29

You could call it an upgrade.
Initially, it would just consider all transactions in the mempool.
When RBF was introduced, it was decided to ignore those RBF fee bumps.
A fee bump is when you increase the fee of an existing transaction.
In the beginning developers were not sure whether miners would actually play along with that game, actually replace the transactions.
Because they weren't sure about that, it was a bit risky to take those fees into account because you didn't know if those fees actually mattered or not.
But they do, and more people are using RBF.
Now, the fee estimation takes into account the fees of the transactions whose fee was bumped.

Aaron van Wirdum: 00:14:12

To be very clear, the fees and RBF transactions we're talking about here are essentially other people's RBF transactions.
To reiterate that really quickly, RBF, you send a transaction, and it's taking longer to confirm than you anticipated, or for some reason, you're in more of a rush all of a sudden.
You have the option to resend the same transaction to the network but include a higher fee this time.
The newer transaction should override the older transaction, the miners should pick that one because it has a higher fee, essentially.

Sjors Provoost: 00:14:51

Exactly.

Aaron van Wirdum: 00:14:53

Then the transactions that are going to be confirmed in blocks essentially have higher fees now if all miners will adopt or accept these RBF transactions.
Therefore, your own transaction, if you're going to send it, would also require a bit of a higher fee, and that's now taken into account.

Sjors Provoost: 00:15:11

Yeah.
The one nuance there is not necessarily that fees will actually go up, because people will make more conservative estimates and then increase them.
So effectively fees might be lower.
But you have to take them into account.
You have to look at what transactions actually go into the block.

Aaron van Wirdum: 00:15:28

Let's say I want to have my transaction confirmed within 24 hours.
Now that RBF transactions from other people are taken into account, should this mean that my fee estimation will be slightly higher now?

Sjors Provoost: 00:15:48

That's what I thought yesterday too, but now I think that's not actually true.
Because RBF transactions, what it's saying is it's now including transactions that have been fee bumped.
But I don't know if it previously excluded those transactions or excluded transactions that were using the RBF flag but were not fee-bumped.

Aaron van Wirdum: 00:16:08

I don't get that at all.

Sjors Provoost: 00:16:13

There's three kinds of transactions.
There's transactions that don't use RBF at all.
There's transactions that set the RBF flag but don't bump the fee.
And there's transactions that now have a higher fee.
The transactions that now have a higher fee are always higher than the ones that don't.
So yeah, I guess you're right.
It would increase the fee estimate slightly.

Aaron van Wirdum: 00:16:33

It would have to, right?
There's no way it can be lower if it's going to take into account RBF transactions.
It might stay the same in some cases.
It's either the same or higher.

Sjors Provoost: 00:16:44

It depends.
If it was discounting all RBF transactions, regardless of whether the fee was bumped or not, then it's different.
Because if the algorithm was only looking at transactions that don't have the RBF flag at all, and now it's also looking at transactions that do have the RBF flag, those might be all systematically lower.

Aaron van Wirdum: 00:17:00

That would be a strange policy if that was the case.

Sjors Provoost: 00:17:05

It may be, but that would be a good reason to revert it.
We should have read the pull request a bit better.
You can do so yourself.

Aaron van Wirdum: 00:17:11

In either case, that's a detail.
The important thing is that RBF transactions are now taken into account for fee estimation.
To summarize that in one sentence, fee estimation should be a bit better now.

## User-space Statistically Defined Tracing (USDT)

Sjors Provoost: 00:17:28

Let's talk about Tether.

Aaron van Wirdum: 00:17:28

Sjors, do you want to talk about Tether?

Sjors Provoost:

Yeah, is it actually Tether?
USDC?

Aaron van Wirdum:

Oh, you know, that's another one, right?
Tether should be USDT or something like that.

Sjors Provoost: 00:17:44

Well, Anyway, oh, it is USDT.
I actually just wrote it wrong in the show notes.
Yeah, it's USDT, but it doesn't stand for tether.
It stands for user-space statically defined tracing for Bitcoin Core.

Aaron van Wirdum: 00:17:55

Aha, it's only now that I understand your pun.
I made a pun in the show notes.
That's great.
We're back to puns.
We need more puns in our show but make the pun again because maybe people didn't get it.

Sjors Provoost: 00:18:08

No, that's fine.
They can re-listen to the episode.
And I ruined it anyway.
The basic idea here is that I don't really understand the basic idea.
Tracepoints are tools that developers can use, but also people who want to monitor their own nodes can use to get really fine-grade statistics out of their nodes.
For example, you can ask your node for things.
You can call the node RPC and ask for the list of blocks or peers you have.
There's RPC call for that.
You can also read log files, and that tells you something.
This (USDT) is just another way to get more detailed information.
One of the details you can get is every message that every node ever sends to you.
All of your peers keep sending you all sorts of messages, and now there's a better tool that you can use to track those messages in a database.

Aaron van Wirdum: 00:19:01

Let's break this down a little bit.
This sounds like something useful for developers specifically, right?
Or is this something users are gonna use for some reason?

Sjors Provoost: 00:19:15

I would say developers, but also say researchers.
Jameson Lopp, for example, when he does all these analyses of whatever's going on, he could use this, or security researchers might find this interesting because they could run a bunch of nodes and check all the message traffic that's coming at those nodes and maybe identify attacks by something subtle.
We talked about an attack on the Bitcoin peer-to-peer network a few episodes ago, where people were announcing fake nodes.
That's something you probably wouldn't be able to detect if you just start your Bitcoin Core GUI; it doesn't get hot or scream at you.
Yet, there is an attack going on.
These kinds of tools would make it much easier to see that this attack is going on.

Aaron van Wirdum: 00:19:59

One small step back, just for my own understanding and the listeners' as well, since they're listening, hopefully.

Sjors Provoost: 00:20:07

That's why we explain things.

Aaron van Wirdum: 00:20:08

First of all, you just mentioned log files.
A log file basically keeps track of every action your Bitcoin Core node does.

Sjors Provoost: 00:20:19

Depending on how you configure it, you can tell it to keep track of quite a lot of detail, yes.
But it's just a long text file, and each line starts with the timestamp, and then it says, "Okay, this happened, okay, this happened"
If you want to process that data, it can be quite tedious.

Aaron van Wirdum: 00:20:34

Right.

Sjors Provoost: 00:20:35

And not everything goes into the log file either.

Aaron van Wirdum: 00:20:37

Okay.
But this was already possible.

Sjors Provoost:

Yes.

Aaron van Wirdum:

Now we're talking about user-space statistically defined tracing.
I'm trying to understand you, it's like a more specific type of log file, it tracks more specific things?

Sjors Provoost: 00:20:57

That's what I understand, too, but I don't completely understand it either.
I guess it really ties better into the operating system, and it's a way to communicate this information in a more structured way than just a text file.

Aaron van Wirdum: 00:21:09

The example you gave was something related to the peer-to-peer network.
You give it a very specific instruction.
You don't have to log everything.
You just log whatever other nodes are communicating with you or whatever data other nodes are sending to you.
Bitcoin Core now has the option to keep track of that in a way that's easy to understand by other types of software, perhaps.

Sjors Provoost: 00:21:35

Yeah, exactly.

Aaron van Wirdum: 00:21:36

As you mentioned, (is is) useful for developers, useful for researchers, not something a regular user will use in general.

Sjors Provoost: 00:21:45

No, I don't think so.

Aaron van Wirdum: 00:21:47

Okay.
That's pretty clear to me.
Next point, Sjors.
Are you ready?

Sjors Provoost: 00:22:03

Yeah, I'm ready.

## Bech32

Aaron van Wirdum: 00:22:05

Bech32.
How do I pronounce Bech?
Is that how I pronounce it?
That's probably a very Dutch way of pronouncing it.

Sjors Provoost: 00:22:12

Yeah, I would say Bech32, but others say Bech32.

Aaron van Wirdum: 00:22:16

B-E-C-H-3-2.
Bech32.
I forgot why this is in the show notes.
Well, I'm sure you remember.

Sjors Provoost: 00:22:27

As you may remember, the Bech32 checksum has some nice properties.
One of them is that it allows you to locate where your typos are.

Aaron van Wirdum: 00:22:34

Bech32 is a type of address?

Sjors Provoost:

Yep.

Aaron van Wirdum:

We did a previous episode on addresses.
Sjors, which episode is that?

Sjors Provoost: 00:22:47

Yes, we addressed this.
I think it was probably episode two or something.

Aaron van Wirdum: 00:22:52

It was very early, yes.

Sjors Provoost: 00:22:53

One of the things we explained is that this new address format that starts with "BC1" will have the nice property that if you make a typo in it, you can actually find out where it was due to mathematical magic.
That was already possible in theory but it wasn't supported in practice.
Now, Bitcoin Core will let you do it, at least if you use the command line in this release, and then maybe in a future release, there's already some work for that, you can do it in the GUI.

Aaron van Wirdum: 00:23:21

If someone, for some reason,would type out an address instead of just copy-paste and then make a typo, then your Bitcoin Core client would tell you, "There's a typo in it, and it's there"
That's basically what will happen.

Sjors Provoost: 00:23:38

There's some discussion about up to what point that's safe because there could be situations where you make too many typos.
Then, it might think you actually meant another address, and it might actually help you accidentally change the address into a different address, which is even worse than the address not working.

Aaron van Wirdum: 00:23:58

It's like autocorrect in that sense.

Sjors Provoost: 00:24:01

But if you're using the command line, then you should know what you're doing.
So it's easier to introduce these features there.

## Wallet Support for Taproot

Aaron van Wirdum: 00:25:08

Nice.
All right.
Next point.
We're getting there.
Two or three more to go, right?
Wallet support for Taproot.

Sjors Provoost: 00:25:20

That's right.
I think, more precisely, new wallets will support Taproot.
If you create a new wallet, it will have Taproot support.
It won't use it by default, but you can.
The other change is a little drop-down menu where the checkbox used to be for Bech32.
Now, there will be a drop-down menu where you can choose.
It still uses SegWit by default, but you can actually select taproot as well.

Aaron van Wirdum: 00:25:48

What exactly does that mean?
What does it mean to use taproot in this context?

Sjors Provoost: 00:25:52

You'll get an address that starts with "BC1P" instead of "BC1Q".
It's a taproot single signature pay-to-public key.

Aaron van Wirdum: 00:26:01

It doesn't mean you're automatically using all the fancy multisig options and timelock options hidden in this tree.
It's still a regular single-key transaction, but you are using a Taproot address.

Sjors Provoost: 00:26:18

Which has almost no benefit, but you can do it.

Aaron van Wirdum: 00:26:22

It has a little bit of benefit for yourself.
The point, in this case, is that anyone monitoring the blockchain won't be able to tell if it was, in fact, just a single-key transaction or maybe there was a fancy script hidden behind it.
That's one of the nice things about Taproot.
It looks the same.

Sjors Provoost: 00:26:40

That's right.

Aaron van Wirdum: 00:26:41

We're working towards this future.
That's part of the vision of Taproot: where every transaction looks the same, and people won't know what kind of transaction is really hidden behind it.

Sjors Provoost: 00:26:57

The transition phase is always a bit risky.
Now, how many wallets can actually do this?
There are not that many, so it might actually tell people that you're using Bitcoin Core, but yeah, that's something to think about.
But it's not the default yet.
The other reason it's not the default is because some wallets cannot send to a taproot address.

Aaron van Wirdum: 00:27:15

In the short term, in the transition phase, you're arguably a bit worse off privacy-wise, but then once people migrate to this new standard, everyone should benefit.
That's basically the short version of the story here.


## Wallet support for freezing coins

Aaron van Wirdum: 00:27:29

Okay.
So we're heading in that direction.
We're moving to the next point.
You can now freeze coins in your wallets.

Sjors Provoost: 00:27:43

It was already possible when you're using the Bitcoin Core GUI to send coins.
You have something called manual coin selection that you can turn on if you like to actually decide which specific coins you want to spend.
It'll give you a nice, well, nice depending on who you ask, graphical display of which coins you have, and you can select boxes and choose which coins to use.
It also has the opposite feature where you could say "I don't care which coin to use but don't use this one and this one" because they come from some bad source that I don't want to mix with my other coins.

Aaron van Wirdum: 00:28:16

Well, that's the new thing, right?

Sjors Provoost: 00:28:19

No, it was already there.
The problem is you have to do it every time you want to make a new transaction.
It didn't remember it.
At least not between startups of the Bitcoin Core.

Aaron van Wirdum: 00:28:31

You're saying coins, which is also what I often use.
It's easier to understand it.
Technically, they're UTXOs, of course.
They're the fractions of Bitcoin you received over time in your wallet.
It was always possible, if you make a transaction, that you tell your Bitcoin Core wallet, "I want to use these fractions to create a new transaction".
Or, like you said, don't use these fractions to create my new transaction.
Now, you can basically tell your node, "Don't use these fractions until I tell you otherwise".

Sjors Provoost: 00:29:12

That's right.

Aaron van Wirdum: 00:29:13

For the rest of time.

Sjors Provoost: 00:29:14

Yeah, exactly.
It remembers it.
And that can be nice for a couple of reasons.
Maybe your wallet has lots of coins from KYC-free places, but it has one coin that you got from Coinbase.
And you just never want to use that coin from Coinbase because then Coinbase can tell all your other coins as they're probably spying on you.
You can basically mark that coin as toxic until you decide to spend it, and it remembers that.
it can also be (useful) if you have something like a dust attack.
Somebody like an analytics companyight be sending very small amounts of dust to Bitcoin addresses that it knows about.
Then it's hoping that your wallet will automatically grab those coins and combine them with the other coins in your wallet, therefore revealing that you own both the old address and the new address.
Now, you can disable those two if you see this attack.
It's pretty advanced stuff, but it's nice that it works.

Aaron van Wirdum: 00:30:13

So, freezing is like a manual thing, you click a button, now they're frozen?
And then, is unfreezing also a manual thing?
Or could you also say, don't use them for a year, and after a year, they're automatic?

Sjors Provoost: 00:30:26

No, it's not that advanced.
You just select it, and you deselect it.

Aaron van Wirdum: 00:30:30

Right.

## Bonus Item: C compiler bugfix

Sjors Provoost: 00:30:32

We have a bonus item.

Aaron van Wirdum: 00:30:34

Exciting.
This is very exciting.
A bonus item.
Sjors, I cannot wait to hear what the bonus item is.

Sjors Provoost: 00:30:39

As we mentioned, there were multiple release candidates, and then there was release candidate number four, and somebody on Windows found a bug.
It was a very obscure bug.
It's like if I go to this screen and then this other screen, and I wait a few seconds, my node crashes.
This is something many people would not even test because when there's a new release you generally test things that are new in that release.
But in this case, somebody was just testing existing functionality and ran into this crash, and people investigated it, and it turned out to be some really obscure Windows-only bug in the C compiler that Bitcoin Core is using.
So, people actually had to fix a C compiler in order to get to fix Bitcoin Core.
And that took another couple of weeks.

Aaron van Wirdum: 00:31:26

The C compiler, that's not even part of Bitcoin Core.
That's just a separate program in Windows that will compile your code into binaries, right?

Sjors Provoost: 00:31:35

Yeah, or a program on Linux that will compile your code so that it runs on Windows.

Aaron van Wirdum: 00:31:42

Right.
There was a bug in that separate piece of software, the compiler, and therefore a bug pops up in Bitcoin Core.

Sjors Provoost: 00:31:51

Yeah, but only in Windows and only in that specific place.
It was very lucky that people even ran into it.
I mean, that specific bug wasn't the end of the world.
It's very annoying, but if there's a bug in a compiler that can cause things to crash, you don't want to think about what other things that bug could cause.
So, it's better to just deal with it.

Aaron van Wirdum: 00:32:09

We've also made an episode about this, Sjors.
Which episode was that?

Sjors Provoost: 00:32:14

In the episode about GUIX, where we talked about dependencies and the dependency circus.

Aaron van Wirdum: 00:32:20

Here, we have a concrete example of a dependency that has a bug and, therefore, causing problems in Bitcoin Core.
So, how was this solved?
Is this solved?

Sjors Provoost: 00:32:30

Yeah, I believe it's solved.
There's two things usually that happen at the same time.
One is, once you figure out what it is, you go to the developers of this dependency project, so the compiler people probably, and you tell them this is broken and here's how you can fix it.
Then, they will put that into their normal flow and eventually they'll release an update where it's fixed.
But you may not want to wait for that.
So, there's something called patches where in Bitcoin Core there's a bunch of these small snippets of code that, before Bitcoin Core is compiled, it first patches whatever needs to be patched, and then it compiles.
So basically, Bitcoin Core creates a little patch that fixes the compiler before it builds Bitcoin Core.

Aaron van Wirdum: 00:33:12

Who creates these patches?
Bitcoin Core developers, actually?

Sjors Provoost: 00:33:15

Whoever fixes the original issue.
It could be a Bitcoin Core developer that fixes the issue for the compiler people.
It could be the compiler people that fix the issue themselves, but they haven't published the new binary for the fix yet.
So then, you would just copy-paste their fix.
It doesn't really matter who does it.

Aaron van Wirdum: 00:33:34

But in this case, do you know who created the patch by any chance?

Sjors Provoost: 00:33:38

Probably Fanquake, but I'm not sure.

Aaron van Wirdum: 00:33:40

So someone created this patch, (and) fixed the upstream problem, or is it downstream?
Is it upstream or downstream?

Sjors Provoost: 00:33:50

I think it's upstream.
I would say upstream.

Aaron van Wirdum: 00:33:51

Yeah, it has to be upstream.
So someone fixes the upstream problem, and now Bitcoin Core should be compiled without the bug.
That's release candidate five.
We're testing that now while we're recording this podcast.

Sjors Provoost: 00:34:07

Hopefully, nothing else is broken, and then it can be released.

Aaron van Wirdum: 00:34:11

Great.
Where do people find this software if they want to download it?

Sjors Provoost: 00:34:15

If they want to test a release candidate, they should go to the Bitcoin developer email list, where there's an announcement that says, "Hey, you can download the release candidate here".
If you just want to wait for the real thing, it'll show up on bitcoincore.org eventually.

Aaron van Wirdum: 00:34:31

All right, great.
I think that covers it, Sjors.

Sjors Provoost: 00:34:33

Cool.
Well, thank you for listening to Bitcoin Explained.
