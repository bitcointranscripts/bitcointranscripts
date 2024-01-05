---
title: "Scaling Bitcoin With The Erlay Protocol"
transcript_by: davidgumberg via review.btctranscripts.com
media: https://www.youtube.com/watch?v=Gq6vRnJnbBM
tags: ["p2p","mempool","erlay"]
speakers: ["Sjors Provoost","Aaron van Wirdum"]
categories: ["podcast"]
date: 2021-04-08
---
## Preamble

Aaron van Wirdum: 00:00:07

Live from Utrecht, this is the Van Wirdum Sjorsnado.

Sjors Provoost: 00:00:10

Hello again.

Aaron van Wirdum: 00:00:12

We've done it again, Sjors.

Sjors Provoost: 00:00:14

We've done it again.

Aaron van Wirdum: 00:00:15

We recorded the whole episode without actually recording it.

Sjors Provoost: 00:00:18

Yeah.

Aaron van Wirdum: 00:00:19

So we're going to do the whole thing over.

Sjors Provoost: 00:00:20

It's this thing where you press the button, but you don't press it hard enough.
And you have to check if the red light is blinking.
It is now.


### Sidebar about Podcast 2.0 Sat Streaming

Aaron van Wirdum: 00:00:28

Great. I think you have a bit of news, some exciting news for us.

Sjors Provoost: 00:00:33

That's right. You can now stream your sats to us (Sjors and Aaron).
Yeah, you can. It's very cool.

Aaron van Wirdum: 00:00:41

How does that work?

Sjors Provoost: 00:00:49

The way it works is this standard called Podcasting 2.0.
So for those who don't know, a podcast is essentially just an RSS feed with a bunch of information like the title and a nice picture and for every episode a link to some mp3 file that your podcast player downloads.

But it turns out you can add more stuff to this RSS feed and Adam Curry, the original podcaster, he basically started a project called Podcasting 2.0 which adds a bunch of new fields and one of those new fields is called 'value' and this value field lets you add for example a Lightning node public key to the RSS feed of your podcast.

And then if you have a podcast player that understands this, like a normal podcast player will just ignore it, but a player like in the Breez iOS test flight app, I think also like in the Sphinx app, if they understand it, and they have Lightning available, they'll start streaming sats to you as the people are listening.
And you can suggest a rate, but people can choose it themselves.

Aaron van Wirdum: 00:01:58

So people can either listen for free or they can pay us.

Sjors Provoost: 00:02:01

That's right.

Aaron van Wirdum: 00:02:02

Well, let's see what they choose.

Sjors Provoost: 00:02:04

So not only that, they can listen for free in a really well-functioning app maintained by Apple, or they can use very experimental software and have to deal with Lightning and then pay us.

We'll see which people prefer.

Aaron van Wirdum: 00:02:21

Sounds like we're gonna be stacking sats, Sjors.

Sjors Provoost: 00:02:23

Yeah, I think the last time I checked the node there was zero sats in it, but it's only been live for a couple hours.

### Sidebar about Taproot activation 'coin flip'

Aaron van Wirdum: 00:02:29

The other thing I wanted to mention is people keep pinging me about the coin flip.
Did you hear about the coin flip?

Sjors Provoost: 00:02:34

I did because you just told me in the previous take.
But tell me again.

Aaron van Wirdum: 00:02:38

I'm trying to pretend a little bit like this is an original episode.

Sjors Provoost: 00:02:42

All right.

Aaron van Wirdum: 00:02:43

I'll try that.

So the Speedy Trial discussion was winding down to block height or block time, which we discussed in our episode about Speedy Trial that was about Taproot activation.

Sjors Provoost: 00:02:57

And the difference is basically, at least I find block height a little bit easier to understand, but the existing soft forks so far and BIP9 have all used block time, which is fine.
It's just a little bit more difficult to think about, but in terms of code I don't think it matters that much.

So there's now two pull requests.

Aaron van Wirdum: 00:03:17

Yeah, and it looks like it's going to be the block time one based on a blockchain based coin flip they did.

Sjors Provoost: 00:03:24

That's amazing, even though they can be gamed.

Aaron van Wirdum: 00:03:31

This was mentioned on the IRC chat as well.
But, it would be pretty expensive to game it.

Sjors Provoost: 00:03:37

Well, the future is at stake, right?

Aaron van Wirdum: 00:03:40

The future of Bitcoin is at stake.
If Speedy Trial happens at all... There's been a couple of NACKs by now, so we'll have to see.

This is not what our episode is about.
Our episode Sjors, this episode, episode 34 is about Erlay.

Sjors Provoost: 00:03:56

Erlay.

## Erlay

Aaron van Wirdum: 00:03:58

So [Erlay](https://arxiv.org/abs/1905.10518) is a project, I think it was started at the University of British Columbia, or at least University of British Columbia researchers Gleb Naumenko, Alexandra Fedorova and Ivan Beschastnikh were working on it, as well as Blockstream's Pieter Wuille and Greg Maxwell.

### The problem that Erlay solves

Aaron van Wirdum: 00:04:32

So, Erlay, the problem it solves, Sjors, is that nodes use bandwidth.

Sjors Provoost: 00:04:43

Lots of bandwidth.

Aaron van Wirdum: 00:04:44

Yes, and this is a problem because we want people to be able to run full nodes.
And if full nodes use bandwidth and bandwidth costs money, the more bandwidth means it's more expensive to run a full node, which means fewer people will run full nodes or at least they'll be incentivized not to and it would be good if we could reduce the cost of running a full node.

So it would be good if we could find ways to make it cheaper to run full nodes which means if we could find ways to reduce bandwidth use.

Sjors Provoost: 00:05:21

That's right and we've previously talked about downloading the blockchain as a source of bandwidth use and we talked about some ways to make that smarter.
But, now we're going to talk about the transactions that are not yet in a block, the mempool.

Aaron van Wirdum: 00:05:37

I want to finish (describing) the benefits (first).

Part one is it would be good if we could reduce bandwidth or if people choose to keep using the amount of bandwidth they're currently using, if we could further optimize the efficiency there, then we could have nodes connect to more other nodes.
Which, would in turn benefit network robustness it would counter certain types of attacks like Eclipse attacks.

Sjors Provoost: 00:06:09

Yeah, because we talked about Eclipse attacks in earlier episodes and one of the solutions we already mentioned is: Well, just connect to more peers.
And there is a big downside to that, which we'll explain in a bit in terms of bandwidth use.

Aaron van Wirdum: 00:06:23

So, if we could optimize bandwidth use, that means people can either run a full node more cheaply, or they can connect to more nodes, which counter certain types of attacks, or a bit of both. That's what we're trying to do is reduce bandwidth use.

So you already mentioned this, there's basically two main things that cause bandwidth.
One of them is receiving and forwarding blocks themselves and this is what the blockchain consists of.
And, the other thing is receiving and forwarding transactions.

Sjors Provoost: 00:06:59

That's right. Before they are in the block.

Aaron van Wirdum: 00:07:02

This is how transactions find their way over the network, which ultimately is how they find their way to miners so they know which transactions they can include in blocks.

Sjors Provoost: 00:07:14

Every node has a thing called the mempool, which is where they keep track of transactions that aren't in the block yet and they relay those to their peers.

And you might say, "Well, why would you do that?"

Well, there's some selfish interest in (that) you want to know as soon as somebody's about to send you a transaction, and you want to know as soon as somebody is about to cheat on you on Lightning.
It's nice to know that these transactions might start happening before they're in a block.

But, there's also an altruistic reason: If nobody did this, then transactions would not get to miners, because you'd have to know which nodes are the miners and send it directly to them.
And so, especially because it's altruistic, you want to make it cheap or get a lot of value out of it.

### Transaction relay

Aaron van Wirdum: 00:07:55

So, receiving and sending transactions over the network, not the blocks, the transactions, how does this actually work on the technical level?

Sjors Provoost: 00:08:10

Well, basically you just scream.
That's kind of what it boils down to.
I mean, you hear about a transaction and it's like, "Oh my God, everybody, did you know about this transaction?"

So literally, you might be connected to, I don't know, eight peers outbound or even more inbound.
And if you hear it from your first peer, you will tell all your other peers about it and this is called flooding.

So everybody just gossips the transaction to as many nodes as they can.
This uses an enormous amount of bandwidth, but it's very robust.
It's very likely for a transaction to make it through and it'll make it through very fast.

Aaron van Wirdum: 00:08:42

It's a little bit more nuanced than that because you send transaction IDs first, right?

Sjors Provoost: 00:08:51

Right.
So there is some optimizations because what I just described would be sending the whole transaction and that would use a lot of bandwidth.
But, what you could do instead, and what nodes actually do instead, is sending short ID's, which is just a very short hash of the transaction, not even the normal transaction ID, but something even smaller.

And then when a node receives those, they can say, "I don't know about these ones, tell me more," and then you give the whole transaction.
There's some back and forth and this saves bandwidth, but it's a one-off saving.
Maybe it reduces the total bandwidth by a factor of four, but that's it.

Aaron van Wirdum: 00:09:26

Right.
To make this very explicit, what happens is I receive a transaction ID or a short version of a transaction ID, which is a hash of a transaction or an even shorter version of that.
I check this against all of the transactions I have in my mempool.
If I don't have it yet, then I get back to the node that sent me the ID and I tell them, "Hey, send me this whole transaction. I haven't seen this yet."
This node sends me the whole transaction.

Now I turn to all my other peers and I send them this ID and then some of these peers will get back to me and tell me, "I don't have this transaction either, send it to me as well, please."
And that's how it's forwarded.

Or if they have it already, then I'm not going to send them the whole transaction.
I just send them the ID, they checked it, they already have it, so we're good.

Now, what happens is that this last example where I send out an ID and my peer already has that transaction, that actually happens a lot because they are connected to so many other peers as well, and odds are they already got it from someone else.
So it happens a lot that these transaction IDs are basically sent for nothing, they already had the transaction.

So this is in a way wasted bandwidth, I'm sending this transaction ID to them, they're receiving it, but they already had the whole transaction so I'm sending the ID for no good reason.

Sjors Provoost: 00:10:55

Yeah, and it's good to realize that it's impossible, at least naively impossible, to prevent that waste, but we can get into how much of that waste it is.
But, compared to the most theoretical ideal scenario, which is bad for decentralization reasons, if everybody just downloaded the transactions from a central website that would be the most efficient way to do it in terms of data usage.
But, of course, we don't want to have a central website.

Aaron van Wirdum: 00:11:22

Yeah, I think more than half of all bandwidth that a node is sharing these transaction IDs.
And they ran the numbers at some point and I think about 44% of the total bandwidth use of a node is basically waste, are these transaction IDs that--

Sjors Provoost: 00:11:48

--are telling people what they already know.

Aaron van Wirdum: 00:11:51

Exactly. This 44%, that's what we're gonna try to bring down with Erlay.

### How Erlay works

Aaron van Wirdum: 00:11:59

Erlay, in order to bring that down, uses something called minisketch, right?

Sjors Provoost: 00:12:05

Yeah, it basically does two general things.
One is it still uses this flooding that we just described, and the other is it uses minisketch.

The flooding is reduced, it's only flooding now between publicly reachable nodes.
The general idea is that some nodes can be reached from the internet, their IP is known, and other nodes are probably behind a firewall or they have a privacy setting on and they're not reachable.

But, the idea is that every node that is not reachable will connect to a node that is reachable, or almost everyone unless you do it manually. Because otherwise, how do you connect to the rest of the network?
The idea is that as long as all these reachable nodes have like flood a lot between each other, then at least all the unreachable nodes are just one hop away from all the transaction data.

That's sort of the first step, where you reduce the flooding to a smaller group of people.
And then the second thing you do is, and this is the cool part, is the minisketch.


#### Minisketch

Aaron van Wirdum: 00:13:08

Right, so what's minisketch?

Sjors Provoost: 00:13:10

Okay, so the goal of minisketch is to do set reconciliation.

Aaron van Wirdum: 00:13:14

What is set reconciliation?

Sjors Provoost: 00:13:17

A set is basically just a bag of stuff.
In this case the contents of your mempool, the list of all your transactions, that's a set.
Or, the list of all the short IDs of your transactions is a set or whatever.

I have a mempool, so I have a set, and you have a mempool, so you have a set.
The question is, what is the difference between these sets?
What are the transactions that I have that you don't have, and that you have that I don't have?
That (difference) is probably just a fraction of the mempool.

That challenge in computer science is just called set reconciliation, trying to find out what the difference is and then trying for both of us to get the same set eventually.
So sending the least amount of data over and back.

Aaron van Wirdum: 00:13:58

So one way we could do that is you just send all of the transactions you have in your mempool to me.
I compare all of your transactions to all of my transactions.
I can easily tell the difference and send you the transactions that you didn't have yet and keep the transactions from yours that I didn't have and now the sets are reconciled.

Sjors Provoost: 00:14:20

That is one way to do it that is worse than what we just described with flooding.

Aaron van Wirdum: 00:14:23

Yes, this is a very resource intensive thing to do so we're using something more clever than this.
But, this is the general principle, (and) we're just using something mathematically more clever.

Sjors Provoost: 00:14:35

Exactly.
So the mathematical clever thing is this: 
And this is where we're going to get extremely hand-wavy, because I do not actually know or understand the moon math involved.

Aaron van Wirdum: 00:14:46

God knows I don't either.

Sjors Provoost: 00:14:48

No, that's okay though.

The idea is I take my mempool, the set, and I do some math on it and the end result is a little, maybe one kilobyte object or two kilobyte, or whatever.
Some small object compared to the rest of the mempool.
And you do the same type of operation and you end up with a one kilobyte object.

And now I send you my one kilobyte object.
This is called the sketch.
So I'm sending you my sketch and that's just a tiny thing.

You receive the sketch and now the math says that if the difference between our two mempools was actually less than the size of the sketch, then you can actually figure out exactly which transactions are missing on either side. 

Only then, so if the difference is bigger, then you get gibberish, you don't know anything.
But if the difference is the same or smaller, you can actually reconstruct which transactions I am missing and which transaction you are missing.

Then the procedure is pretty simple, your node will just give me the transactions that it knows I need and it will ask for the transactions that it needs.

Aaron van Wirdum: 00:15:57

So if for some absurd reason, we have completely different mempools, then this won't work very well or at all?

Sjors Provoost: 00:16:05

No, and the good thing of course about the mempool is that because you're syncing it all the time, and because there are rules about highest fee things are more important, it's actually fairly predictable what the mempools of other people are going to look like.
For the most part, it's going to be the same.

Then it's just a matter of finding the right parameters to use with this sketch.
So, (finding) how big you want to make the sketches so that most of the time people will actually find the difference, but not so big that it just wastes more bandwidth than the flooding protocol.
And that's sort of what the paper went into with simulations.

Aaron van Wirdum: 00:16:39

So if it's close enough, then I can figure out which transactions are the difference and we can reconcile just these transactions.

##### Other applications of minisketch

Aaron van Wirdum: 00:16:48

Without getting into the moon math specifically, I know there's been some other examples where this kind of math has been used.

Sjors Provoost: 00:16:58

Yeah, so it's interesting, and I only learned this today, maybe wrong on some of the stuff, but it refers to something called fuzzy matchers, I think was the term.

Aaron van Wirdum: 00:17:08

I think so.

Sjors Provoost: 00:17:10

So it refers to an older paper from, I think 2004 or 2008.

Aaron van Wirdum: 00:17:13

The trick predates Bitcoin, basically.

Sjors Provoost: 00:17:16

Yeah, and I'm sure the general principle is even older.
But, the problem they were trying to solve was, for example, biometric identification.

Aaron van Wirdum: 00:17:26

Fingerprints.

Sjors Provoost: 00:17:27

Yes, so if I wanna go to my moonbase and I wanna enter the moonbase, they want my fingerprint.

Aaron van Wirdum: 00:17:34

Of course.

Sjors Provoost: 00:17:34

But I don't want them to have a database.

Aaron van Wirdum: 00:17:36

Everyone knows you can't get into your moonbase without a fingerprint.

Sjors Provoost: 00:17:40

I don't want them to have a database of my fingerprint.
I don't want them to have a photo of my fingerprint.
But, they're gonna need that, naively speaking, because when I put my finger on the little sensor, it's gonna take a picture and that picture is always gonna be slightly different than what it was before.
So they cannot just store, say, a hash of the image.
They have to store the image itself and then look at it and say, "Well, this is so and so much difference."

Aaron van Wirdum: 00:18:06

The reason it's going to be slightly different than before is basically it's a photo and even if you take a photo of the same object, it's going to be slightly tilted or slightly darker or some pixels are going to be different at least.
So it's going to be similar, but not literally exactly a copy.

Sjors Provoost: 00:18:23

Right, because every single pixel is slightly different and the same really goes with normal passwords.
One typo in your password and it just doesn't work anymore.

Aaron van Wirdum: 00:18:31

So it could work, we could take a picture of your fingerprint and then make a new fingerprint and compare the two.
However, the problem here is that we don't want a database full of fingerprints because people can steal the database and abuse it and rob banks and leave your fingerprints all over there.

Sjors Provoost: 00:18:50

There's another use case where this is an even bigger problem, which is what if I want to put some Bitcoin on a private key that is generated by my fingerprint?

In this case, there is no database, there is just my fingerprint and I want to construct a private key from that fingerprint.
If I take a picture on the device and then take the image and put the image literally on a cold card and that (image) is its entropy, it'll give you a set of private keys.
Then if I repeat that, it'll give me a different set of private keys, so that'd be quite bad.

It would be nice, however, if you could do this in a way, and that's kind of what that original paper described,.
so (that) it would take certain properties of the fingerprint or the iris scan, doesn't really matter what, and then it would create a 'sketch' of your fingerprint.

Aaron van Wirdum: 00:19:40

Right, that's where the term 'sketch' comes from.
It's a mathematical sketch basically.

Sjors Provoost: 00:19:46

Yeah, a mathematical 'sketch' of your fingerprint, which is not the same as a hash but it is some sort of summary of it.
But, if you have that sketch you cannot reconstruct a fingerprint.
It is similar to a hash in that you can't go back.
It's a one-way function but it has a slightly more more useful information than a hash does, and it's very small.

So, what the moonbase does, or what the iPhone would do, is it would store this sketch, and then when you reappear and you put your fingerprint on the sensor, it's now going to make a sketch of this new fingerprint.
And then, because of what we just talked about, if those sketches are similar enough, you can actually reconstruct the difference.
In other words, in the case of the moonbase, you can say, "Hey, I can reconstruct the difference, therefore I think this difference is small enough."
It's the real person, it's the real fingerprint.

Or in the case of the private key, you can actually, because you stored a sketch of the original fingerprint, you can now, using the other fingerprint, essentially your second fingerprint, and this original sketch, so you make a sketch of the new one, you can actually reconstruct the exact sort of image that you would have had the first time around and so you do get the same entropy, and so you can use your fingerprint to store your Bitcoin.

Don't do this, but you could using this methodology.

And, this difference can also be used for mempool comparison.

Aaron van Wirdum: 00:21:09

Yeah, so this trick for comparing fingerprints is the same mathematical trick that we're now using in the context of Bitcoin for set reconciliation in mempools.

Sjors Provoost: 00:21:24

Which will make it more efficient to put your node on the moon and we're a full circle.

#### How Erlay uses minisketch

Aaron van Wirdum: 00:21:31

Okay, how is this actually used in Bitcoin then?
What actually happens?
What's the step-by-step process if we're using set reconciliation?

Sjors Provoost: 00:21:43

Yeah, if this stuff were to be merged in Bitcoin Core, the nice thing is it doesn't change any consensus rules, so it's just something people can use or they can not use it, and you connect to peers and if those peers support this way of handling things, then depending on whether they are public nodes or not, you would either do the original flooding or you would use the sketching and you would keep your mempool synced by using these sketches.

Aaron van Wirdum: 00:22:09

So, instead of constantly sharing every transaction ID you receive with all your peers, now you're also once in a while just sharing a sketch and based on that sharing the transactions that you don't share yet?

Sjors Provoost: 00:22:26

Yeah, and this is so much more efficient that you can have lots and lots of peers with which you are exchanging these sketches, far more than you could if you were using the flooding.

So you use flooding with a subset of your peers or not at all, and you use the sketches otherwise.

And if the sketch somehow fails, there's a little fallback that's [described in the protocol](https://github.com/bitcoin/bips/blob/master/bip-0330.mediawiki#sketch-extension) that says, "Well, if the sketch is too big, you can try something half the [size of the first] sketch again and overlap [that with first sketch]."
So, you can do a second attempt if the difference is just a little bit bigger.

And then if you give up, if it fails again because the difference was too big, great, you just fall back to the original flooding protocol.

So that's kind of what it does.

And there's a [pull request](https://github.com/bitcoin/bitcoin/pull/21515) on it.
There's a [BIP out there.](https://github.com/bitcoin/bips/blob/master/bip-0330.mediawiki)

Aaron van Wirdum: 00:23:06

Yeah, this is it sounds very hypothetical, but this is actually something that's being developed and that could be merged into Bitcoin Core soonish.

Sjors Provoost: 00:23:19

I only briefly looked at the pull request and it looks like most of the things are in there but of course I haven't tested it or or thoroughly reviewed it.
But my guess is it'll happen, or maybe not if there's a huge problem of course, but as far as I'm concerned it sounds pretty good.

Aaron van Wirdum: 00:23:39

Yeah, clear so far.
Anything else?

Sjors Provoost: 00:23:42

I don't think so.
That's all we got.
Alright, so thank you for listening to the Van Wirdum Sjorsnado!

Aaron van Wirdum: 00:24:00

Bye.
