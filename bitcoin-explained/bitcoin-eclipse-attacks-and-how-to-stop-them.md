---
title: "Bitcoin Eclipse Attacks And How To Stop Them"
transcript_by: Sjors, edilmedeiros, NeroCherubino
media: https://www.youtube.com/watch?v=UK9Yykf2aA4
tags: ["bitcoin-core", "eclipse-attacks"]
speakers: ["Sjors Provoost","Aaron van Wirdum"]
categories: ["podcast"]
date: 2020-11-13
episode: 17
---
Sjors Provoost:

Yeah, we're going to discuss a paper about eclipse attacks.
Couldn't come up with a better pun.
So apologies.

Aaron van Wirdum:

That's all you got from us.
It's the paper Eclipse Attacks on Bitcoin's Peer-to-Peer Network by Ethan Heilman, Alison Kendler, Aviv Zohar, and Sharon Goldberg from Boston University and Hebrew University MSR Israel.

Sjors Provoost:

That's right and it was published in 2015.

Aaron van Wirdum:

So it's a little while ago.
We're discussing this because the new Bitcoin Core release will include a new method to prevent eclipse attacks?

Sjors Provoost:

That's right and it's actually something that was suggested in that paper.
So to give you an idea about the speed of Bitcoin development, sometimes somebody writes a paper in 2015 and then over the years, improvements are made based on that paper and that's still happening.

Aaron van Wirdum:

Yeah, but this is not the first improvement based on this paper.
This is one of them and this is just the reason we're doing an episode about it now.

Sjors Provoost:

Correct.
A lot of things have already been done.

## What are eclipse attacks

Aaron van Wirdum:

So Sjors, what are eclipse attacks?

Sjors Provoost:

So an eclipse attack is when your node is only seeing your enemy, basically.
Your attacker.
Your node has connections that it makes to the outside world and there are people who connect to your node.
And if all those connections are to some evil person, then you think you're talking to the whole world, but you're actually only talking to one person so that person is eclipsing your view of the world.

Aaron van Wirdum:

Bitcoin is a peer-to-peer network so it consists of peers that talk with each other and I think an average, regular nodes connects to how many peers?

Sjors Provoost:

Usually a node connects to eight peers outbound.
And it can have up to 117 inbound.
That's changed maybe a little bit, but that's the idea.

Aaron van Wirdum:

Right, so then the idea is if you control all outbound or inbound nodes.

Sjors Provoost:

Both.

Aaron van Wirdum:

So if you control both all inbound and outbound nodes of someone else, then you can basically lie to them and they have no other connection to the network.
Am I saying that right?

Sjors Provoost:

That's right.
So basically you connect to all these nodes because you want to ask them for new transactions and for new blocks and they'll spontaneously give you new transactions and new blocks.
And so if you're only talking to one person eventually, then that person can decide not to give you certain transactions and not to give you certain blocks.
Now they cannot make fake things entirely, right? 
They can't fake signatures because you're still checking all the consensus rules.

Aaron van Wirdum:

Sure.
But what can do then? 
What's the risk, let's say I'm attacked like this.
I'm subject to an eclipse attack.

Sjors Provoost:

The easiest thing and that's I guess, less relevant now because people are more aware of that risk in general, is they can do a double spend attack on you.
So let's say you're expecting money from somebody, you're expecting coins from somebody and you see this transaction appear in your Mempool, so in your memory, but it's not yet in a block and you're happy.
But now it turns out that this person is actually sending you that transaction over the wire, but to the outside world, he's sending a very different transaction.
And so then a new block arrives, but you're not going to see that block.

Aaron van Wirdum:

He's sending a conflicting transaction is what you mean.
He's sending the same coins to someone else?

Sjors Provoost:

Yeah to himself probably.
And so you think you've got this unconfirmed transaction and it's going towards you and you're not seeing any new blocks, but you think, okay, I guess, this is good.
It's mine.

Aaron van Wirdum:

I wouldn't think that Sjors.

Sjors Provoost:

No.
So nowadays people know that accepting zero confirmation transactions is a very bad idea and for all sorts of reasons, but this is the easiest thing you can do when you can basically hide what's happening.
You can tell this person one thing that you paid them and tell other people another thing.

Aaron van Wirdum:

Right, so what if I don't trust zero conf?

Sjors Provoost:

So if you do wait for a confirmation, they can still attack you using an eclipse attack, but it's going to get a lot more expensive.
So they'll have to produce a block basically.
A valid block.

And then they give you that block and it includes the transaction so you think it's confirmed but the outside world is also producing blocks, the normal miners.
And they're hiding those normal blocks from you.
So now in the outside world, that transaction never happened because there's a longer chain that's not paying you and you've just accepted there one block or maybe multiple blocks.
The attack is more expensive as they have to produce more blocks.

Aaron van Wirdum:

So the idea is if you are a miner and you want to launch this attack on someone, but you only control 10% of hash power, then usually it wouldn't work because even the blocks you produce with the fake transaction will just be orphans away.
But if you also have an eclipse attack, then it could actually work because the person you're attacking, doesn't see the competing chain.

Sjors Provoost:

Yes.
And this of course reminds us why it's important for Bitcoin to be somewhat expensive because it's really expensive to produce blocks like that.
Back in 2015, this would've been cheaper.
But another thing you can do is because now you think, okay, so they're only going to attack me if the cost of making this fake block is lower than the amount of money they're scamming you for.
So unless you-

Aaron van Wirdum:

Which is very unlikely.

Sjors Provoost:

Right.
Unless you're buying Teslas or all these fancy cars all the time, you don't have to worry about this, you think.
But it turns out they can do something else, which is they can actually try to split miners.
So they're trying to scam you, but they're also scamming to miners at the same time, basically making miners, not see each other's blocks.
And then you might have one miner producing the block attacker ones and one miner producing the block that goes to you.
And the miners don't even know that this is going on and they're wasting a giant amount of money and the attacker just robs you of a $100.
So there's a lot of economic damage, but they still scam you.

Aaron van Wirdum:

Right, so basically let's say there are two miners on network just to simplify things.
Then you launch an eclipse attack on one of them plus you launch an eclipse attack on me then you can have this one miner produced blocks and he doesn't see the blocks of his competitor and you send these blocks of the miner you're attacking to me and therefore we're on sort of a separate network, which could be a minority network so the miner is wasting money and I'm being cheated with fake transactions at the same time.

Sjors Provoost:

Yes but the attacker still makes money.
So yeah, it's important that the attacker doesn't necessarily have to produce the blocks themselves in order to profit from an eclipse attack.

Now, the good news, or I don't know if it's good news, but mining is still somewhat centralized, there's specialized networks that connect miners so this is quite difficult to do.
We don't want to rely on that.

Aaron van Wirdum:

Relay networks and these kinds of things.

Sjors Provoost:

Exactly.
But we don't want to rely on that of course.
Ideally, it should be impossible to eclipse anyone.

Aaron van Wirdum:

So luckily it's getting harder over time because we're getting more solutions to make it harder.

Sjors Provoost:

Exactly.
Nodes are becoming a little bit hardened.
So I guess in order to understand that, we should explain how this paper proposes that one does an eclipse attack.

Aaron van Wirdum:

Oh yeah.
I almost forgot about that.
How do you actually do it?

Sjors Provoost:

Well, how did you used to?
The idea that you...
There's a couple of ingredients that you need here.
One is that what nodes are doing when they start, they try to find other peers and I think we talked about that before a little bit when we talked about DNS seeds.

Aaron van Wirdum:

Couple of episodes ago.

Sjors Provoost:

Yeah.
But basically, when a node has been running for a while, it has a list of addresses that it got from other peers and it's stores them in a file.
And when the node restarts, it looks at this file for all the addresses it heard of, and it starts randomly connecting to them.
And the idea here is that you try to pollute this file as an attacker.
You try to give the node a lot of new addresses that you control.
Or that just don't exist.
That's fine too.
And you kind of try to exploit the way that this node picks the addresses.
That's sort of at a high level, what happens.
And so basically the node divides the addresses in buckets, it basically looks at the IP address and finds some patterns in it, like the starting letters of the IP address or deciding numbers of the IP address and it divides them across buckets that way.

Aaron van Wirdum:

And I guess buckets are just a different word for lists.

Sjors Provoost:

Yes.
Separate lists.
And then when it's starting up, it just tries to pick things from different buckets.

It's still get confused by the details.
It doesn't really matter, but there's basically a way that it does that and you can exploit that mechanism because the mechanism has, or had a bias in it.
For one thing, it tried to take very recent items from the...
So if you've learned about an address recently it would be slightly more likely to use that.
And so you could exploit that, but the idea is you give the node...
You start up a whole bunch of attack nodes.
And you just feed IP addresses.
You connect to the victim node.
So you can occupy all the inbound connections, that's easy.

And then you give it a lot of nonsense addresses and a lot of real addresses that are you.
And every time it makes a connection, it either fails because there's nothing there or it connects to you and eventually it only connects to you.

Aaron van Wirdum:

So if I would have to simplify this probably by a lot, then let's say I have a thousand real IP addresses of other nodes and then you feed me, I don't know, 10 gazillion fake IP addresses or IP addresses that are yours, and then my nodes start to pick IP addresses, then the odds are, I'm just going to pick IP addresses that are either fake or yours and I'm not going to pick any of the real ones because I'm only picking so many IP addresses.

Sjors Provoost:

Yeah.
And so part of the trick here is that you have a list of IP addresses that you know already, but every time you learn new ones you start throwing away the old ones you already knew.

Aaron van Wirdum:

Right.
So it's even worse than the sort of random example I gave.

Sjors Provoost:

Yeah.
Well, that's the problem.
You can just keep giving somebody new addresses and then eventually they won't remember any of their old addresses.
So the paper runs a simulation to see how difficult it is to actually overflow all these buckets.
Because maybe, it might be possible in theory, but maybe it's just too much work and the paper show said it's actually not too much work.
I think it's like a matter of days that you can flood it.

Aaron van Wirdum:

So it's going to take a couple of days to basically fill the buckets, the lists of another node's IP addresses with all of your own IP addresses and fake IP addresses?

Sjors Provoost:

Yep.

Aaron van Wirdum:

What then?

Sjors Provoost:

Then, the node still has connections, still has outbound connections to the real world so the question is, how can you get rid of those connections? 
And the trick there is you try to make the node crash in whatever way you can make a node crash.

Aaron van Wirdum:

What are some ways you can make a node crash?

Sjors Provoost:

Well, there are hopefully no ways to make a node crash.

Aaron van Wirdum:

Oh.

Sjors Provoost:

But this is why it's extremely important to make sure you, as a developer, you don't write code that can make a node crash, because it is an important ingredient in these type of attacks, and in other attacks.

So whenever there is a bug that allows Bitcoin Core to crash, it's a pretty serious one.
But you can somehow overload its RAM usage, there's been lots of problems like that, but when it crashes and it starts again, hopefully, usually automatically if you've configured a server correctly and when it starts automatically,or when it starts, it's going to look at that file of peers it knows, and it's going to try and connect to them.
So it's going to look in all these buckets and it's only going to find the attacker.
And then the attacker also makes sure that it's connecting to you.
So all your inbound connections are full and then you're just only talking to the attacker.
So that's what you need.

Aaron van Wirdum:

And then the eclipse attack is in play.

Sjors Provoost:

Exactly.

Aaron van Wirdum:

So now are we going to solve it?

Sjors Provoost:

Yeah.
So what are we going to do about it?

Aaron van Wirdum:

What are we going to do about it Sjors?

## Approach to solve eclipse attacks

Sjors Provoost:

So as we already said, it is a numbers game.
You need to give a lot of spam addresses to this node to fill up all the buckets and make sure that it only connects to you.
So one very simple solution is just to have more buckets.
Another is, what we said, these more recent peers that you are biased towards.
One thing you can do is to not have that bias.

Aaron van Wirdum:

Right.
Or reverse that bias?

Sjors Provoost:

Well, then you just attack it in some opposite way.
Whenever there's a bias that gives you something that you can attack.

Aaron van Wirdum:

I would imagine it's harder to attack the reversed version of that bias if you prioritize IP addresses, you already knew, then it's harder for an attacker to attack you, right?

Sjors Provoost:

Yes.
But if you prioritize old IP addresses that you knew a long time ago, then they might not be there anymore.
So you're constantly failed to connect.
So there's a trade-off there.
If you've recently heard about the IP address, it's probably still out there.
So there's a bit of a trade-off, but there is one mitigation that's sort of related to this, which is that if you hear of a new address and you want to replace that, you want to put that in the bucket and therefore take something else out of the bucket, first, you check the address that's already in the bucket.
You connect to it, you see if it's still out there.
If it's still out there, you don't replace it.
So that's called the feeler connection.
So what I think a couple years ago, was merged was basically Bitcoin Core every now and then looks at that bucket, quickly connects to a node, sees if it's real and remembers that and then disconnects.

Aaron van Wirdum:

So that is prioritizing all the addresses just in a smarter way.

Sjors Provoost:

Exactly.

Aaron van Wirdum:

And this was merged.
And what about the previous one?
I didn't ask, but is that one merged using more buckets?

Sjors Provoost:

I don't think so.
I don't think using more buckets was merged.
Basically the paper has about 10 suggestions and some of them have been merged.
Some of them even before the paper came out, because obviously it was an exploitable vulnerability
And some of them much later.
Another thing you can do, and that is actually what has been merged a few weeks ago.

Aaron van Wirdum:

Which will be in the next Bitcoin Core release.

Sjors Provoost:

Hopefully.
Is that when you restart, you try to remember some of the last connections you had and so that's what it's doing, basically.
It remembers, I thinkm two connections, namely two connections that it only exchanges blocks with.
And it tries to reconnect to those, but not too often because there's straight offs everywhere, but apparently it's not a good idea to always try to reconnect to the same nodes again when you restart because for all you know, the reason you crashed in the first place is because one of those nodes was evil.

Aaron van Wirdum:

Yeah, the idea is that, as you explained before, you need to crash a node for a node to start up again and find, well, all of that attack IP address in this case.
This attack would be countered because you're just connected to some of the same IP addresses you were already connected to.

Sjors Provoost:

Yeah.
But not-

Aaron van Wirdum:

With the trade-off that maybe the one you connected to was also the one that crashed you, so you might be crashed again.

Sjors Provoost:

Exactly, and I think one of the mitigations for that is that you only try this once so you connect to the one you were connected to last, but if that goes wrong again, you don't do it again.

Now another thing you can do is not have more buckets, but have more connections, more outbound connections.
Because the more outbound connections you have, the more likely you are to be connecting to honest nodes.

Aaron van Wirdum:

Yeah, the harder it is for an attacker to control all of the IP addresses you're connected to.

Sjors Provoost:

Yeah, and you may ask yourself why wouldn't you do that?
Why not just have as many connections as possible?

Aaron van Wirdum:

Why not have as many connections as possible Sjors?

Sjors Provoost:

That's an excellent question.

Aaron van Wirdum:

Thank you.

Sjors Provoost:

The problem is that you're exchanging a lot of data and especially the transactions that are in a mempool.
That is very data intense.
Like gigabytes and gigabytes and gigabytes.
So you can't just add more connections without also increasing bandwidth use.
And there are some new proposals that we'll probably discuss in future episodes that will reduce the bandwidth needed to do these mempool synchronizations and then you can have more connections.
So there's an incentive to make this data exchange more efficient.

Aaron van Wirdum:

Plus there's the solution that some of the connections you connect to, you don't share mempool stuff, you only connect blocks.

Sjors Provoost:

That's right.

Aaron van Wirdum:

I guess that's also one of the solutions mentioned in the paper isn't it?

Sjors Provoost:

I believe it is.

Aaron van Wirdum:

But we sort of already spoiled it in the previous solution.

Sjors Provoost:

We may have.
So one of the ways to have more connections, to have the upside of more connections without the downside of more bandwidth is to only exchange blocks with those extra connections, because that happens much less frequently.

Aaron van Wirdum:

It still costs a little bit of an extra bandwidth.
But much less, not nearly as much.

Sjors Provoost:

And this, again reminds us that you need to wait for confirmations because those extra connections will tell you about new blocks.
They won't tell you about new stuff in the mempool, but that's fine if you wait for confirmations.

Aaron van Wirdum:

Is there more?

Sjors Provoost:

Well, I mean, you can always use the Blockstream satellite or something like that as another source of data.
Of course that's not a universal solution, but it is a really-

Aaron van Wirdum:

It is almost, I think.

Sjors Provoost:

Well, you would be trusting Blockstream.

Aaron van Wirdum:

Yes.

Sjors Provoost:

But there is an incentive for Bitcoin blocks to be broadcast in general, over satellite or AM, or from multiple sources so it's more difficult to eclipse someone because you'd have to eclipse the whole planet.
If the signal is coming from a satellite, you want to eclipse somebody who's listening to that satellite and you either have to blow up the satellite connection to them or blow up the satellite itself, which everybody would notice and it'd be in the news and you'd say, "Hey, there's probably something going on here."

Aaron van Wirdum:

Sure.

Sjors Provoost:

Let's see, any other mitigations?

Aaron van Wirdum:

I like your adversarial mindset though, that you do recognize that that's actually a risk that someone blows up the satellite.

Sjors Provoost:

Well, I mean, you don't actually physically have to blow it up, I guess.
You can just tell people to stop broadcasting to it.
One more solution is to have more nodes, basically, that other people don't know are yours.
So if you have multiple nodes that you're using for whatever your service is, and you make sure that the outside world doesn't know all of them, then they might try to eclipse one of them, but they forgot to eclipse the other ones.

Aaron van Wirdum:

That sounds like a good idea to me Sjors.
But there were like 10 solutions in the paper.

Sjors Provoost:

Yeah, there were.

Aaron van Wirdum:

But we didn't cover them all then?

Sjors Provoost:

No, we didn't because in order to cover them all, you would have to describe the attack in much more detail.
To the point that even though I've read this paper probably two or three times over the past few years, I don't understand all the details, especially these buckets, the way they're filled is rather tedious.

Aaron van Wirdum:

Fair enough.
So yeah, I guess we'll put the paper in the show notes, right?

Sjors Provoost:

Yes, and there's a website that links to some of the solutions that have been implemented.
Although I think the website itself is out of date now.

Aaron van Wirdum:

What's the website?

Sjors Provoost:

Well, we'll put it in the show notes because that's not easy to spell out.

Aaron van Wirdum:

Anything else?

Sjors Provoost: 00:20:15

No. 

Aaron van Wirdum: 00:20:16

Was this our episode on Eclipse attacks?

Sjors Provoost: 00:20:17

I think so.

Aaron Van Wirdum: 00:20:18

Nice.

Sjors Provoost: 00:20:18

That's all I've got.
Thank you for listening to the the van Wirdum Sjorsnado.

Aaron Van Wirdum: 00:20:22

There you go.