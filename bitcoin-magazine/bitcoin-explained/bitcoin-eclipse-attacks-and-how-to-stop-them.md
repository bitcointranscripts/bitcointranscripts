---
title: "Bitcoin Eclipse Attacks And How To Stop Them"
transcript_by: NeroCherubino via review.btctranscripts.com
media: https://www.youtube.com/watch?v=UK9Yykf2aA4
tags: ["attacks"]
speakers: ["Sjors Provoost","Aaron Van Wirdum"]
categories: ["podcast"]
date: 2020-11-13
---

##Music

Van Wirdum: 00:00:07

Live from Utrecht, this is The Van Wirdum Provoostnado.

Provoost: 00:00:10

Hello.

Van Wirdum: 00:00:11

Hi Sjors.
What's up?
How are you enjoying the election drama?

Provoost: 00:00:16

Oh, thoroughly, yes.

Van Wirdum: 00:00:17

Be careful what you say because you're definitely gonna trigger half of our audience.

Provoost: 00:00:23

The US has great export products, great cheeseburgers, Frappuccinos, nice people, laptops and great movies, good entertainment.

Van Wirdum: 00:00:32

Oh boy, okay, well let's just skip that.
You wanted to make a pun about eclipse.

Provoost: 00:00:38

Yes.
The next solar eclipse is scheduled for December 14th 2020 and it's going to be in Latin America.

Van Wirdum: 00:00:47

Great.
So, let's talk more about Eclipses.
For this entire episode.
We're actually going to do something slightly...
This is the first time we're doing this, I guess, right?
We're going to discuss a white paper, a paper.

Provoost: 00:01:01

Yeah, we're going to discuss a paper about eclipse attacks yes and the paper come up with a better pun so that's all you got from us it's the paper eclipse attacks on bitcoins peer-to-peer network by Ethan Hellman, Allison Kandler, Aviv Zohar and Sharon Goldberg from Boston University and Hebrew University, MSR Israel.
That's right and it was published in 2015.

Van Wirdum: 00:01:26

Yeah, so it's a little while ago.
We're discussing this because the new Bitcoin Core release will include a new method to prevent Eclipse attacks?

Provoost: 00:01:36

That's right.
And it's actually something that was suggested in that paper.
So to give you an idea about the speed of Bitcoin development, sometimes somebody writes a paper in 2015 and then over the years improvements are made based on that paper and that's still happening

Van Wirdum: 00:01:49

Yeah, but this is not the first improvement based on this paper This is one of them and this is just the reason we're doing an episode about it now, correct A lot of things have already been done.
So shows what are eclipse attacks?

Provoost: 00:02:00

So an eclipse attack is when your node is only seeing your enemy, basically, your attacker.
You know, your node has connections that it makes to the outside world, and there are people who connect to your node.
And if all those connections are to some evil person, then you think you're talking to the whole world, but you're actually only talking to one person.
So that person is eclipsing your view of the world.

Van Wirdum: 00:02:21

Exactly, yeah.
Bitcoin is a peer-to-peer network, so it consists of peers that talk with each other.
And I think an average regular node connects to how many peers?

Provoost: 00:02:30

Usually a node connects to connects to eight peers outbound and it can have up to 117 inbound.
That's changed maybe a little bit but that's the idea.

Van Wirdum: 00:02:40

Right so then the idea is if you control all outbound or inbound nodes?
Both okay so if you control both all inbound and outbound nodes of someone else then you can basically lie to them and they have no other connection to the network am I saying that right

Provoost: 00:02:57

That's right so basically you you know you connect to all these nodes because you want to ask them for new transactions and for new blocks and they'll spontaneously give you new transactions and new blocks.
And so if you're only talking to one person eventually, then that person can decide not to give you certain transactions and not to give you certain blocks.
Now they cannot make fake things entirely, right?
They can't fake signatures because you're still checking all the consensus rules.

Van Wirdum: 00:03:23

Sure, but what can they do then?
What's the risk?
Let's say I'm attacked like this.
I'm subject to an Eclipse attack.

Provoost: 00:03:32

The easiest thing, and it's I guess less relevant now because people are more aware of that risk in general, is they can do a double spend attack on you.
So let's say you're expecting money from somebody, you're expecting coins from somebody, and you see this transaction appear in your mempool, so in your memory, but it's not yet in a block and you're happy.
But now it turns out that this person is actually sending you that transaction over the wire, but to the outside world he's sending a very different transaction and so then a new block arrives but you're not going to see that block.
He's sending a conflicting transaction is what you mean he's sending the same coins to someone else to himself probably and so you think you've got this unconfirmed transaction and it's going towards you and you're not seeing any new blocks, but you think, okay, I guess, you know, this is good.
It's mine.

Van Wirdum: 00:04:24

I wouldn't think that's yours.

Provoost: 00:04:25

No, so nowadays people know that accepting zero confirmation transactions is a very bad idea and for all sorts of reasons.
But this is the easiest thing you can do when you can basically hide what's happening.
You can tell this person one thing, that you paid them, and tell other people another thing.

Van Wirdum: 00:04:39

Right, so what if I don't trust Zeroconf?

Provoost: 00:04:43

So if you do wait for a confirmation, they can still attack you using an Eclipse attack, but it's going to get a lot more expensive.
So they'll have to produce a block, basically, a valid block.
And then they give you that block, and it includes the transaction, so you think it's confirmed.
But the outside world is also producing blocks, the normal miners, and they're hiding those normal blocks from you.
So now in the outside world, that transaction never happened because there's a longer chain that's not paying you, and you've just accepted their one block or maybe multiple blocks.
The attack is more expensive as they have to produce more blocks.

Van Wirdum: 00:05:21

Yeah, so the idea is if you're a miner and you want to launch this attack on someone, but you only control 10% of hash power, then usually it wouldn't work because even the blocks you produce with the fake transaction will just be orphans away.
But if you also have an Eclipse attack, then it could actually work because the person you're attacking doesn't see the competing chain.

Provoost: 00:05:45

Yes, and this of course, you know, reminds us why it's important for Bitcoin to be somewhat expensive, because it's really expensive to produce blocks like that.
Back in 2015 this would have been cheaper.
But another thing you can do is because now you think, okay, so they're only going to attack me if the cost of making this fake block is lower than the amount of money they're scamming you for.
So unless

Van Wirdum: 00:06:06

You're buying...
Which is very unlikely.

Provoost: 00:06:07

Right, unless you're buying Teslas or all these fancy cars all the time, you don't have to worry about this, you think.
But it turns out they can do something else, which is they can actually try to split miners.
So they're trying to scam you, but they're also scamming the miners at the same time, basically making miners not see each other's blocks.
And then you might have one miner producing the block the attacker wants and one miner producing the block that goes to you.
And the miners don't even know that this is going on and they're wasting a giant amount of money and the attacker just robs you of $100.
So there's a lot of economic damage, but they still scam you.

Van Wirdum: 00:06:50

So basically, let's say there are two miners on the network, just to simplify things, then you launch an Eclipse attack on one of them, plus you launch an Eclipse attack on me.
Then you can have this one miner produce blocks and he doesn't see the blocks of his competitor and you send these blocks of the miner you're attacking to me and therefore we're on sort of a separate network, which could be a minority network.
So the miner is wasting money, and I'm being cheated with fake transactions at the same time.

Provoost: 00:07:24

Yes, but the attacker still makes money.
So, yes, it's important that the attacker doesn't necessarily have to produce the blocks themselves in order to profit from an Eclipse attack.
Now, the good news, or I don't know if it's good news, but mining is still somewhat centralized.
There's specialized networks that connect miners, so this is quite difficult to do.

Van Wirdum: 00:07:42

Yeah, like we don't want to rely on that.
Relay networks and these kinds of things.

Provoost: 00:07:45

Exactly.
But we don't want to rely on that of course.
Ideally, you know, it should be impossible to eclipse anyone.

Van Wirdum: 00:07:52

Right, so luckily it's getting harder over time because we're getting more solutions to make it harder.

Provoost: 00:08:00

Exactly, nodes are becoming a little bit hardened.
So I guess in order to understand that we should explain how this paper proposes that one does an eclipse attack.

Van Wirdum: 00:08:08

Right, I almost forgot about that.
How do you actually do it?

Provoost: 00:08:14

Well how did you used to?
The idea that you, there's a couple of ingredients that you need here.
One is that what nodes are doing, when they start, they try to find other peers.
And I think we talked about that before a little bit when we talked about DNS seeds.

Van Wirdum: 00:08:32

A couple episodes ago.

Provoost: 00:08:33

Yeah, but basically, you know, when a node has been running for a while, it has a list of addresses that it got from other peers and it stores them in a file.
And when the node restarts, it looks at this file for all the addresses it's heard of and it starts randomly connecting to them.
And the idea here is that you try to pollute this file as an attacker.
You try to give the node a lot of new addresses that you control or that just don't exist.
That's fine, too.
And you you kind of try to exploit the way that this Node picks the addresses that's sort of at a high level what happens.
And so basically the The node divides the addresses in buckets It basically looks at the IP address and find some patterns in it like the starting letters of the IP address or deciding numbers of the IP address
and I guess buckets are just a different word for lists

Provoost: 00:09:29

Yes, yeah separate lists and then when it's starting up it just tries to you know, pick things from different buckets.
It's still get confused by the details.
It doesn't really matter.
But there's basically a way that it does that, and you can exploit that mechanism because the mechanism has or had a bias in it.
For one thing, it tried to take very recent items from the, so if you've learned about an address recently, it would be slightly more likely to use that.
And so you could exploit that.
But the idea is you give the node, you start up a whole bunch of attack nodes and you just feed IP addresses.
You connect to the victim node so you can occupy all the inbound connections.
That's easy.
And then you give it a lot of nonsense addresses and a lot of real addresses that are you.
So every time it makes a connection, it either fails because there's nothing there or it connects to you.
And eventually it only connects to you.

Van Wirdum: 00:10:25

Right, so if I would have to simplify this probably by a lot, then let's say I have a thousand real IP addresses of other nodes, and then you feed me, I don't know, 10 gazillion fake IP addresses or IP addresses that are yours, and then my nodes start to pick IP addresses, then the odds are I'm just going to pick IP addresses that are either fake or yours, and I'm not going to pick any of the real ones because I'm only picking so many IP addresses.

Provoost: 00:10:53

Yeah, and so part of the trick here is that you have a list of IP addresses that you know already, but every time you learn new ones, you start throwing away the old ones you already knew.

Van Wirdum: 00:11:03

So it's even worse than the sort of random example I gave.

Provoost: 00:11:07

Well, that's the problem.
You can just keep giving somebody new addresses and then eventually they won't remember any of their old addresses.
So the paper runs a simulation to see how difficult it is to actually overflow all these buckets.
Because maybe it might be possible in theory, but maybe it's just too much work.
And the paper shows that it's actually not too much work.
I think it's a matter of days that you can flood it.

Van Wirdum: 00:11:32

Okay, so it's going to take a couple of days to basically fill the buckets, the lists of another node's IP addresses with all of your own IP addresses and fake IP addresses.
Yep.
What then?

Provoost: 00:11:44

So then, the node is still not really, you know, The node still has connections, still has outbound connections to the real world.
So the question is how can you get rid of those connections?
And the trick there is you try to make the node crash in whatever way you can make a node crash.

Van Wirdum: 00:12:01

What are some ways you can make a node crash?

Provoost: 00:12:03

Well there are hopefully no ways to make a node crash but this is why it's extremely important to make sure you as a developer you don't write code that can make a node crash because it is an important ingredient in these type of attacks and in other attacks.
So whenever there is a bug that allows Bitcoin Core to crash, it's a pretty serious one.
But you can overload, somehow overload its RAM usage.
There's been lots of problems like that.
But when it crashes and it starts again, hopefully, usually automatically, if you've configured a server correctly.
And when it starts automatically, or when it starts, it's gonna look at that file of peers it knows, and it's gonna try and connect to them.
So it's gonna look in all these buckets, and it's only gonna find the attacker.
And then the attacker also makes sure that it's connecting to you.
So all your inbound connections are full.
And then you're just only talking to the attacker.
So that's what you need.

Van Wirdum: 00:13:01

And then the Eclipse attack is in play.

Provoost: 00:13:04

Exactly.

Van Wirdum: 00:13:05

So now are we gonna solve it?

Provoost: 00:13:08

Yeah, so what are we gonna do about it?

Van Wirdum: 00:13:10

What are we gonna do about it, Sjoerd?

Provoost: 00:13:12

So, as we already said, it is a numbers game.
You need to give a lot of spam addresses to this node to fill up all the buckets and make sure that it only connects to you.
So one very simple solution is just to have more buckets.
Another is, you know, what we said, these more recent peers that you are biased towards.
One thing you can do is to not have that bias.

Van Wirdum: 00:13:35

Or reverse that bias.

Provoost: 00:13:38

Well, then you just attack it in some opposite way.
Whenever there's a bias that gives you something that you can attack.

Van Wirdum: 00:13:45

I would imagine it's harder to attack the reversed version of that bias if you prioritize IP addresses you already knew then it's harder for an attacker to attack you right?

Provoost: 00:13:56

Yes but if you prioritize old IP addresses that you knew a long time ago then they might not be there anymore.
So you're constantly fail to connect.
So there's a trade-off there.
If you've recently heard about the IP address, it's probably still out there.
So there's a bit of a trade-off, but there is one mitigation that's sort of related to this, which is that If you hear of a new address and you want to replace that, you want to put that in the bucket and therefore take something else out of the bucket, first you check the address that's already in the bucket, you connect to it, you see if it's still out there.
If it's still out there, you don't replace it.
So that's called a feeler connection.
So what I think a couple of years ago was merged was basically Bitcoin Core every now and then looks at that bucket, quickly connects to a node, sees if it's real, and remembers that, and then disconnects.

Van Wirdum: 00:14:46

So that is prioritizing older addresses just in a smarter way.

Provoost: 00:14:51

Exactly.

Van Wirdum: 00:14:53

And this was merged.
And what about the previous one I didn't ask about?
Is that one merged using more buckets?

Provoost: 00:14:57

I don't think using more buckets was merged.
Basically the paper has about 10 suggestions and some of them have been merged.
Some of them even before the paper came out because obviously it was an exploitable vulnerability.
And some of them much later.
Another thing you can do, and that is actually what has been merged a few weeks ago.

Van Wirdum: 00:15:18

Which will be in the next Bitcoin Core release?

Provoost: 00:15:20

Hopefully.
Is that when you restart, you try to remember some of the last connections you had.
And so that's what it's doing basically.
It remembers, I think, two connections.
Namely two connections that it only exchanges blocks with, and it tries to reconnect to those.
But not too often, because there's trade-offs everywhere.
But apparently, it's not a good idea to always try to reconnect to the same nodes again when you restart.
Because for all you know, the reason you crashed in the first place is because one of those nodes was evil.
Right?

Van Wirdum: 00:15:54

Yeah, the idea is that as you explained before, you need to crash a node for a node to start up again and find, well, all of the attack IP addresses in this case, this attack would be countered because you're just connecting to some of the same IP addresses you were already connected to.

Provoost: 00:16:09

But now...

Van Wirdum: 00:16:11

With the trade-off that maybe the one you connected to was also the one that crashed you, so you might be crashed again.

Provoost: 00:16:16

Yes, but you exactly yeah and I think one of the mitigations for that is that you only try this once so you connect to the one you were connected to last but if that goes wrong again you don't do it again.
Now another thing you can do is not have more buckets but have more connections, more outbound connections.
Because the more outbound connections you have, the more likely you are to be connecting to honest nodes.

Van Wirdum: 00:16:40

Yeah, the harder it is for an attacker to control all of the IP addresses you're connected to.

Provoost: 00:16:45

Yeah, and you may ask yourself, why wouldn't you do that?
Why not just have as many connections as possible?

Van Wirdum: 00:16:51

Why not have as many connections as possible, Sjoerd?

Provoost: 00:16:54

That's an excellent question.

Van Wirdum: 00:16:55

Thank you.

Provoost: 00:16:56

The problem is that you're exchanging a lot of data, and especially the transactions that are in a mempool, that is very data intense, like gigabytes and gigabytes and gigabytes.
So you can't just add more connections without also increasing bandwidth use.
And there are some new proposals that we'll probably discuss in future episodes that will reduce the bandwidth needed to do these mempool synchronizations and then you can have you know more connections so there's an incentive to make this data exchange more efficient.

Van Wirdum: 00:17:27

Plus there's the solution that some of the connections you connect to you don't share mempool stuff you only connect blocks.

Provoost: 00:17:34

That's right.

Van Wirdum: 00:17:34

I guess that's also one of the solutions mentioned in the paper, isn't it?

Provoost: 00:17:37

I believe it is.

Van Wirdum: 00:17:38

But we sort of already spoiled it in the previous solution.

Provoost: 00:17:41

We may have.
So one of the ways to have more connections, to have the upside of more connections without the downside of more bandwidth is to only exchange blocks with those extra connections because that happens much less frequently and it still costs a little bit of extra bandwidth but much less and this again you know reminds us that you need to wait for confirmations, because those connections will tell you about new blocks.
They won't tell you about new stuff in the mempool, but that's fine if you wait for confirmations.

Van Wirdum: 00:18:11

Is there more?

Provoost: 00:18:12

Well, I mean, you can always use the Blockstream satellite or something like that as another source of data.
Of course, that's not a universal solution, but it is a reason.

Van Wirdum: 00:18:21

It is almost, I think.

Provoost: 00:18:23

Well, I mean, specifically, you would be trusting Blockstream.
But there is an incentive for Bitcoin blocks to be broadcast in general over satellite or AM or from multiple sources so it's more difficult to clip someone because you'd have to eclipse the whole planet right if if if the signal is coming from a satellite you want to eclipse somebody who's listening to that satellite and you either have to blow up the satellite connection to them or blow up the satellite itself which everybody would notice and it'd be in the news and you'd say hey there's probably something going on here.

Van Wirdum: 00:18:55

Sure.

Provoost: 00:18:57

Let's see any other mitigations?

Van Wirdum: 00:18:59

I like your adversarial mindset though that you that you do recognize that that's actually a risk, that someone blows up the satellite.

Provoost: 00:19:07

Well, I mean, you don't actually physically have to blow it up, I guess.
You can just tell people to stop broadcasting to it.
One more solution is to have more nodes, basically, that other people don't know are yours.
So if you have multiple nodes that you're using for whatever your service is, and you make sure that the outside world doesn't know all of them, then they might try to eclipse one of them, but they forgot to eclipse the other ones.

Van Wirdum: 00:19:34

Sounds like a good idea to me, Sjoers.
But there were like ten solutions in the paper.

Provoost: 00:19:38

Yeah, there were.

Van Wirdum: 00:19:40

But we didn't cover them all then.

Provoost: 00:19:41

No, we didn't, because in order to cover them all, you would have to describe the attack in much more detail, to the point that even though I've read this paper probably two or three times over the past few years, I don't understand all the details.
Especially these buckets, the way they are filled is rather tedious.

Van Wirdum: 00:19:58

Right, fair enough.
So yeah, I guess we'll put the paper in the show notes, right?

Provoost: 00:20:02

Yes, and there's a website that links to some of the solutions that have been implemented.
Although I think the website itself is out of date now.

Van Wirdum: 00:20:09

What's the website?

Provoost: 00:20:10

Well, we'll put it in the show notes because that's not easy to spell out.

Van Wirdum: 00:20:14

Anything else?

Provoost: 00:20:15

No. 

Van Wirdum: 00:20:16

Was this our episode on Eclipse attacks?

Provoost: 00:20:17

I think so.

Van Wirdum: 00:20:18

Nice.

Provoost: 00:20:18

That's all I've got.
Thank you for listening to the Event Weirdum Shorts NATO.

Van Wirdum: 00:20:22

There you go.

##Music
