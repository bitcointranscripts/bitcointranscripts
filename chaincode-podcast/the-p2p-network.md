---
title: The P2P network
transcript_by: varmur via review.btctranscripts.com
media: https://podcasters.spotify.com/pod/show/chaincode/episodes/Amiti-Uttarwar-and-the-P2P-network---Episode-15-e18v7oq
tags:
  - bitcoin-core
  - eclipse-attacks
  - p2p
speakers:
  - Amiti Uttarwar
date: 2021-10-18
episode: 15
summary: 'In this episode of the Chaincode Podcast, Amiti Uttarwar discusses the intricacies of peer-to-peer (P2P) networks in Bitcoin with hosts Adam Jonas and Mark Erhardt. Amiti explains her fascination with P2P due to its logical yet complex interactions across the global network of nodes. She outlines five key principles for designing effective P2P networks: reliability, timeliness, accessibility, privacy, and upgradeability. The conversation delves into specific challenges, such as Eclipse attacks, address relay, and the role of the address manager (AddrMan) in maintaining network integrity. Amiti also highlights the delicate balance between ensuring privacy and achieving network reliability. Overall, the discussion emphasizes the importance of continuous collaboration and innovation in Bitcoin''s P2P network development.'
additional_resources:
  - title: 'Searchable #bitcoin-core IRC logs'
    url: http://bitcoin-irc.chaincode.com/bitcoin-core-dev/
  - title: Eclipse Attacks
    url: https://bitcoinops.org/en/topics/eclipse-attacks/
  - title: Altnet
    url: https://github.com/ariard/altnet-proposals
  - title: Transaction download on Bitcoin's p2p network comic
    url: https://github.com/amitiuttarwar/bitcoin-bytes/blob/master/tx-download.jpg
aliases:
  - /chaincode-labs/chaincode-podcast/the-p2p-network/
---
Amiti Uttarwar: 00:00:00

When you have all of these different components in the system, even a very simple rule can turn into infinitely complex interactions, and it's incredibly difficult to wrap your head around at such grand scale.
That's also something that makes it really cool because that's why it's so important to collaborate.

## Introduction

Adam Jonas: 00:00:25

Hi, I'm Jonas, and welcome to the Chaincode Podcast.

Mark Erhardt: 00:00:41

Hi, I'm Murch.

Adam Jonas: 00:00:43

Welcome back, Murch, it's been a while.
So who are we bringing on as a guest today?

Mark Erhardt: 00:00:47

We'll have Amiti on today.
She's going to talk with us about peer-to-peer.

Adam Jonas: 00:00:51

It's been a while since Amiti's last been in the office, that was 2019 when she was a resident and we're glad to have her back, so enjoy the episode.
Welcome Amiti, welcome back to Chaincode.
What is it like to be back at Chaincode?
How have things changed in the last two years?
Nothing's changed in the last two years, I assume.

Amiti Uttarwar: 00:01:10

Definitely feels a lot calmer.
I'm the slightest bit less aggro about my interest in learning Bitcoin, but not all that much different.
It just comes and goes, you know.

Adam Jonas: 00:01:23

Welcome back and today we are delighted to talk about P2P because it's all of our favorite subjects.

Amiti Uttarwar: 00:01:31

Is it?

## Why Amiti works on P2P

Adam Jonas: 00:01:32

It's gonna be by the end of this episode.
Maybe to start things off, why do you work on P2P?
Why is it interesting?

Amiti Uttarwar: 00:01:40

I love P2P.
I find it to be so fascinating.
I think what really compels my interest is the fact that you have a very bounded set of rules that behave logically.
So what a node is doing is a very well-defined programmatic execution of rules that it's been told, and that we can go look at the code and see.

But then even really simple things, when you expand it to a network of nodes that are running all over the world, they're running different versions of Bitcoin Core, they're running alternate clients and you've got potential malicious adversaries, you have potential inadvertent mistakes that could occur, whether in Bitcoin Core or alternative clients, and all sorts of stuff in between.
You even have people who do things that are odd, that have no clear benefit, and then you go, ah, maybe that's academic research, who knows?

So when you have all of these different components in the system, even a very simple rule can turn into infinitely complex interactions.
It's incredibly difficult to wrap your head around at such grand scale.
That's also something that makes it really cool because that's why it's so important to collaborate, and in Bitcoin Core, obviously peer review is such a fundamental aspect of our development ecosystem.
I think it's really cool to constantly have more components that give me clues to understand the thing that is happening, but I can't see the whole thing.
I can't see exactly who's sending what messages between all of the nodes on the Bitcoin network, but I can get lots of clues, and enough that I can reason about them, and make choices based on different heuristics.
So it's both very bounded and scoped, what a node is doing is so well defined, and yet it's endless and complex.
I can just sit around thinking about it (laughs).
It feels like an intellectual play space for me to try to imagine all of these different incentives and possibilities, and how do we make progress in that land of chaos?

Adam Jonas: 00:04:12

Okay, so we get it, P2P is cool.
How do you think about designing P2P?
Just like off the top of your head, if you had to just come up with a framework, just out of thin air, how would you be thinking about the design?

## A framework for P2P design

Amiti Uttarwar: 00:04:28

Yeah, that's a very good question, clearly never thought about this before.
But I'd imagine that you could have five principles (laughter).

Adam Jonas: 00:04:39

Just out of thin air.

Amiti Uttarwar: 00:04:41

Yeah, let's just call them - that you want the network to be reliable, timely, accessible, private, and upgradable.

Adam Jonas: 00:04:50

Okay, so you're very smart (Amiti's laughter).
But the fact that you came up with those at the top of your head, how did you think of those five characteristics and how did those come to be?

Amiti Uttarwar: 00:05:00

Maybe a better answer to your question earlier of what has changed in the last two years of working on Bitcoin is the way that I glean information.
I think there is so much context to all of the choices, all of the code, how the network works, and it came from Bitcoin Core and all of the things that have been observed within that ecosystem, within the Bitcoin ecosystem, but also prior to that.
So a lot of what I've spent my time doing is trying to better understand how people who are much more experienced than me are approaching these kinds of problems.
Something really cool is this is all open source, so you can just go find out.
Even if it was a decision that was made in 2013 you can go dig it up, and sometimes we'll come across these wonderful elaborate comments just left on PRs that go into depth about why this one line of code must be this particular way, or prolific contributors totally fundamentally disagreeing on what we should be valuing.

## How do we systemize Bitcoin Core knowledge?

Adam Jonas: 00:06:11

I have a question about that, so as we're systematizing that kind of information, how do we memorialize that, and how do we keep those records and create that web of context so that newcomers like yourself, or the next Amiti, can get to those things faster?

Amiti Uttarwar: 00:06:30

I would say the first question is - is it important or beneficial to be able to get to those things faster?
Because on one hand, I definitely think there's ways you could speed up sharing context, and I think that's beneficial to all of us working on the project of how do we share this knowledge and make sure that we're building it up over time, amongst a changing set of contributors, versus going in circles or losing things that we once understood.

On the other hand I feel like it's so cool that it's all there and the fact that I can access it.
I feel like in my personal journey, taking that scenic route of getting there has taught me stuff that I can't necessarily quantify, and it's hard to know what would be lost if you just tried to dump all this super technical information in my brain.
I probably wouldn't have been able to parse it.

So maybe part of it was that it took me a long time, and I say past tense but it's still taking me a long time.
I heard things today that I have on my list to go dig up history about that are intriguing to me.
So it's kind of a hard question to answer, because we also don't have the ability to just like A-B test what it means to learn a complex system.

Mark Erhardt: 00:07:53

Also there's just so much by now, there is so much content, that you can't really read it all.
No single person can understand all the design decisions that were made in Bitcoin anymore, especially if you count the Lightning Network as well.

### Searchable #bitcoin-core IRC logs

Amiti Uttarwar: 00:08:09

Definitely there's too much content, but then I think that relates to the question of how do you surface the nuggets of wisdom that are the shiniest?
Are they just needles in the haystack, or can you just say here it all is?
I think there's some in between.
Having searchable IRC logs is really cool, really helpful.

Adam Jonas: 00:08:34

We now have searchable IRC logs.
Speaking of taking the scenic route, we took the scenic route around the design goals (Amiti's laughter).
You mind if we go back and talk about how you arrived at those things, and what the interaction between them might be?

Amiti Uttarwar: 00:08:52

Yeah absolutely, and I can dig into breaking them down and what I mean by these words, because they're just words that are attempts to capture larger ideas.

Adam Jonas: 00:09:03

They all sound great (laughter).
Like, everybody wants reliability, timeliness, accessibility, privacy, upgradeability.
Like, I'll take them all.
So no trade-offs, right?

Amiti Uttarwar: 00:09:16

No trade-offs (laughs), if you can somehow do them all.
As I was trying to navigate this world, I wanted something succinct that I could refer back to.
In the process of making that, I realized that this is a convenient tool to try to communicate with others the things that I value and am striving for.
So the first three, reliable, timely, and accessible, as features of a network, I think are important for any successful peer-to-peer network.

What I mean by reliable is that if you submit a valid message to the network, it will eventually be delivered to all other nodes that are participating on the network.
So you get a message in, it'll go everywhere.
That's reliability if you can predict that with confidence.

What I mean by timely is how long it takes to get there.
Looking at Bitcoin, the timeliness of each message has very different goals and constraints that we strive for.
For example with transactions, it's important that people get transactions quickly in relation to how long it took for a block to be mined.
But when you say that blocks need to be arriving quickly, those are two very different time scales.
Transactions can take several seconds, tens of seconds, whereas blocks, there's been so much work to reduce any latency.
In transactions, we actually use that latency for other benefits, which we can dig into more.
The second thing is that you have a network, so you can send a message, and then it's timely, so that message actually gets where it's going in a reasonable amount of time.

Then the third is that the network is accessible, that node operators actually have the ability to participate.
Like, that's great if that's there, but if you can't get on it, what does it matter?
I think every project is going to have to define that for themselves.
In Bitcoin, at a very technical level, what I mean by saying accessible is minimizing the resource requirement that is necessary to run a node.
Everything from that to being able to connect to honest nodes when you start up, and being able to bootstrap and find peers.
There's also censorship resistance that can come into here, like no node can prevent another node from participating in the network, which is a fundamental premise that we are constantly thinking about in the day-to-day decisions that we are making.
So I've loosely summed this all up as the term accessible, you have to be able to use the network.

So these three values, I think, to different extents or in different ways, any successful peer-to-peer network needs to have.
But I think we have two additional ones in Bitcoin that we really value.
The next one is privacy.
That probably is not a hard sell for people listening to a Bitcoin podcast.
It's money, and if you want to use money freely, it has to be private.

The last one is upgradeability.
What I mean there, that actually is a very hard one to achieve technically, but what I mean there is giving users choice.
If you have phone software or any app you run, most technology in this day and age at some point they'll just be like, listen, upgrade your phone or I will do it for you, or maybe it'll just stop working.
As a user you don't really have a lot of choice in what version or how the rules changed, at some point you just have to hit accept.
Maybe you can delete the app or get a new phone or whatever, but projects aren't prioritizing that.

Whereas in Bitcoin we really prioritize that anyone who participates in the system, if they have bought into a specific set of rules at a time, then they should always be able to continue using Bitcoin with that rule set.
So even if others adopt more or less rules then they shouldn't be forced to do anything different.
They can literally go into a cave, come out and spend their Bitcoin ten years later.
So that's a very challenging thing to value and to design around.
Obviously there are tons of conversation about soft forks versus hard forks and blah blah blah.
But I think there's a core value here that we want everyone to be empowered regardless of how you're interacting with the system.
That also goes to how we develop, people have choice of their level of involvement.

Adam Jonas: 00:14:12

Are these in order in any way?
So you grouped the top three as in any peer-to-peer network.
Do you order these in terms of priority or in terms of what the P2P network needs?
Because otherwise I could come up some really good acronyms here.
"U R PAT" is how I remember this,  or maybe "RAT UP."

Amiti Uttarwar: 00:14:32

I do think "U R PAT" is a little friendlier.

Adam Jonas: 00:14:35

Okay, I like "RATUP". Or "RAT P U."
You've covered some of these designs...

Amiti Uttarwar: 00:14:38

Wait. "UP ART."

Adam Jonas: 00:14:40

Mmm... that doesn't speak to me (laughter).

## Forward compatibility and upgradeability

Mark Erhardt: 00:14:47

What I really hear when you say that you want upgradeability, you talked a lot about forward compatibility, but is there also an aspect of... the people that go into the cave for 10 years and they come back and want to spend their coins, but the people that are staying there and constantly tinkering and thinking about new use cases, they want to introduce new rules or new features.
Isn't that also a big part of upgradeability?

Amiti Uttarwar: 00:15:17

Yeah, definitely.
That's the contention of how do you have both?
I don't think it makes sense to say, okay, Bitcoin Core is done.
Let's just stop now.
Also Bitcoin's done, you know, let's just, we're good (laughter).
I'm definitely not advocating for that.
I mean most of the features that we want are in some way or another related to the other goals, and even if they're not I'd figure out a way,  at least in my mind.

Mark Erhardt: 00:15:46

Bitcoin is inevitable.
You've heard it here first.

Adam Jonas: 00:15:51

So you've covered these design goals and then maybe you could talk about how these actually work in practice.
How does the rubber hit the road on these concepts?

## Partition resistance

Amiti Uttarwar: 00:15:59

So maybe we can dig into a couple of different examples.
One that I find interesting that is a threat to reliability, is that if there's any partitions in the network then your message cannot make it to all other participants. Ever.
So partition resistance is something that we think a lot about in P2P as a very core principle.
Digging into that, it's been surprising to me to realize the depth of thought that contributors have had.
Like, there's one class of malicious attackers are trying to isolate this specific node so that they can do something weird - Eclipse attacks.
Now they are under, not control, but they're subject to your lens of seeing the whole network.

## Eclipse Attacks

Adam Jonas: 00:16:51

Yeah, maybe you can describe what an [Eclipse attack](https://bitcoinops.org/en/topics/eclipse-attacks/) is.
I don't think we've covered that.

Amiti Uttarwar: 00:16:55

An eclipse attack is essentially where a node believes that they're connected to multiple participants on the network, and thus getting a view of the activity on the network, but really they're connected only to one adversarial entity.
So they might have multiple connections, they might be going to different IP addresses, but they're all controlled by one entity that's collaborating with each other.
So now their view of the world has been eclipsed.
Because Proof-of-Work is so cool, it's not quite game over, it's just very close.
It would still be extremely challenging to fake blocks because you still have to have valid Proof-of-Work, and that's not trivial at this stage of the hash rate and stuff.
So that isn't a trivial attack that they can do, but they can still do other clever attacks.
Obviously privacy is going to be totally lost, and they can try to mislead into having double spends based on kidnapping transactions, or selectively revealing what transactions this entity sees.

Adam Jonas: 00:18:11

I think with the prevalence of Lightning, you also need to be careful about the view of Lightning justice transactions and things like that.

Amiti Uttarwar: 00:18:20

Yeah, yeah.
The whole threat model definitely changes when you bring in the incentives of Lightning, and in other cases where one transaction wouldn't have been very lucrative to suppress, in Lightning it could be.

Adam Jonas: 00:18:35

Yeah.
I think that in addition to that, thinking about eclipsing mining nodes is another issue of wasting hash power, like...

Mark Erhardt: 00:18:47

Reducing the global hash rate in order to make the difficulty go down for yourself.

Adam Jonas: 00:18:53

There's the selfish mining attack angle.

Amiti Uttarwar: 00:18:55

Another attack that you could do that involves a partition but might not be as specific, would be - say you were able to partition all of China off of the rest of the world, so now the hash rate has been super broken up and it's much easier to do hash rate oriented attacks, because you now have half as much that you're trying to compete with just by creating a partition.

Adam Jonas: 00:19:23

And that is like a state level kind of issue.
Well, rejoining the network, reconciling.

Amiti Uttarwar: 00:19:32

Absolutely.

Mark Erhardt: 00:19:33

Well, slow down here, right?
There's no hash rate in China anymore.

Amiti Uttarwar: 00:19:36

Oh I can't keep up (laughs).
But there's actually things, like what if there is a crazy natural disaster and the internet pipes that are at the bottom of the oceans disconnect?
I think it's cool that there's a whole ecosystem of people solving it.
Apparently there's satellites that will solve this, or I don't really know what's going on there.

Mark Erhardt: 00:20:00

I believe I've been told that there's also a radio transmitted source for the blockchain here in New York.

Amiti Uttarwar: 00:20:07

Nice.

Mark Erhardt: 00:20:08

So yeah, you can receive it via satellite feed, from for example the Blockstream satellite.
It will broadcast not only the latest blocks, but the whole blockchain every 24 hours.

Amiti Uttarwar: 00:20:20

Nice.

Mark Erhardt: 00:20:20

I've seen reports of ham radio transfer of transactions, but also on some radio frequencies the latest blocks are being broadcast.

## AltNet

Adam Jonas: 00:20:30

Yeah, I mean, this is why Antoine is going after the [`AltNet`](https://github.com/ariard/altnet-proposals) kind of stuff.
Is that having different transport layers allows us to be a little bit more flexible, maybe a podcast for another day.
What's actually being passed around the network?
We've talked about these high level words, but what's actually going across the wire?

## Messages sent across the wire

Amiti Uttarwar: 00:20:52

Yeah, so there's plenty of P2P messages.
Some of them are operational, like this is how we establish a connection.
We'll do this specific dance to make sure that we're compatible and you're listening to the rules of the Bitcoin network.
But the three main things that bring about complexity and thus are the most interesting are addresses, transactions, and blocks.

Blocks are hopefully pretty evident why those are important.
Obviously they have transactions in them, but when I say transactions, what I mean are the unconfirmed ones that haven't been mined yet.
So that's important to get to miners, and enlightening for different reasons, but to get around the network so that they can make it into a block.

Then addresses are - we have something called an `addr` message and essentially what this contains is...

Mark Erhardt: 00:21:50

Just to clarify - IP addresses, because we also use it for the invoice address.

Amiti Uttarwar: 00:21:57

Yeah exactly, exactly.
So what I mean by addresses here are the location of where the nodes are, those IP addresses, versus wallet addresses or like the 5,000 other types of addresses we have in this world.

So these [`addr` messages](https://btcinformation.org/en/developer-reference#addr) are related back to partition... just how do you find other other people that you can talk to?
These three are very complex, because when we go back to the design goals for each type of this message, we can look at what makes them very challenging to achieve these goals for.
For example, transactions, as we mentioned, we want them to be timely and get to all of the other peers and saturate the network within no more than a minute or two.
At the same time, we don't want bandwidth requirements to be insane because then the cost of the hardware for running a node would go up so high, that at some point if the network scales enough, then there's only a handful of people in the world, or maybe organizations, that are able to afford the hardware requirements.
That's the accessibility goal.

So we need to do clever tricks to figure out - how do you get this out, but you don't want to just spam everyone.
Getting really into the nuances of that is what I spend my days thinking about.
Similarly, when you think of transactions and you want them to be private, but then you also want them to get out to the network.
That's kind of a ridiculous concept.
You're like, hey everyone, there's this transaction, but maybe it's not mine.
How do you pull that off?

So that's another tricky contention that you have to work with, and find solutions that aren't necessarily making compromises, but are improving both at the same time.
Those are some examples of what makes transactions hard, and we can look at blocks and addresses through a similar lens.

Adam Jonas: 00:24:07

It sounds like as you dive deeper and explain the world of P2P, it's pretty vast.
There's a lot of nuance, there's a lot of trade-offs, and there's a lot of - I move a lever here and something pops up way over there.

Amiti Uttarwar: 00:24:22

Oh my god, yeah.

Adam Jonas: 00:24:23

So in that world of interesting things, what's most interesting to you?
What are you working on?

## AddrRelay and AddrMan

Amiti Uttarwar: 00:24:31

Well, what's really captivated my interest right now has been `AddrRelay`, and specifically right now is `AddrMan`, which is the address manager, which is keeping track of all these IP addresses that you're getting from the network.
But generally I do think `AddrRelay` is an area that's so hard to comprehend that we don't have a great shared understanding of how it works, what design goals are...

Adam Jonas: 00:25:00

Can you maybe start from the top?
'm breaking down `AddrRelay` to be address relay, which means that I'm relaying addresses via my node.
To what end?
Where do those come from?
How do they get to me?
Can you talk a little bit about that?

### Bootstrapping, DNS seeds and address announcements

Amiti Uttarwar: 00:25:15

Yeah I can (Laughs).
Say I start a brand new Bitcoin node, great.
I need friends.
Who do I talk to?
Who knows how to speak Bitcoin?

So we have some bootstrapping mechanisms.
Namely one of the biggest ones is DNS seeds.
That's a set of destinations that are hard-coded that you can hit, and they will return information about active nodes on the network.
With that information I can go and try to connect to a bunch of those nodes.

We don't want that to be the only way that we learn about nodes or other nodes to learn about us, because it's essentially a more centralized solution.
If someone was an attacker and was able to give you false addresses, then they can get you into an eclipse situation.
So we have a lot, lot more types of mechanisms.

There are some that can be inputted by users, but the main automatic ones come down to self-announcing your own address, and then it trickling through the network.
Then also when you connect to peers, sending them a `getAddr` message, which just says - hey, send me a bunch of addresses, please.

So those are the two main ongoing mechanisms for automatic address relay.
But the things that make it challenging are that unlike transactions or blocks, addresses don't have evidence of work, and in order to verify it I have to do a lot more than what you have to do to tell it to me.
So to break that down a little bit, you send me an IP address, say you say it's `1.1.1.1`, then I can look at that number and say, well, that's an invalid range or that's a valid range, but I don't know if there's actually a Bitcoin node there.
The only way I can figure out if there's a legitimate Bitcoin node there is by trying to connect to this IP address, seeing if they respond and do the version handshake and then disconnecting, and then I can say - great, it's a good one.

### DoS issues

Adam Jonas: 00:27:32

So that sounds like it's lends itself to a denial of service, asymmetric work based on just applying a string, right?

Amiti Uttarwar: 00:27:40

Yeah.
So if we did a very naive... like you sent me an address, now I will tell everybody, and everyone will tell everybody, and we just kept doing that.
First off, if you can imagine the visual, if there was no end to it, you would just have a whole network of nodes that are just constantly firing.
It would be like neurons or something, which means it could be infinite.
So if we just trivially did that, it would immediately be a bandwidth DoS.
But then you also need heuristics of how do you get it out enough?
Because if you tried to verify everything, it would essentially be a CPU DoS.
In order to send out one address, I had to spend enough compute power to try to open a connection via TCP, blah, blah, blah, it would be a CPU DoS, or no addresses would go anywhere.
So how do you balance those extremes and have something reasonable where nodes can hear about addresses but also don't get super spammed.

Adam Jonas: 00:28:49

And so we're talking about `AddrRelay` right now.
Maybe talk about `AddrMan`, pivot into specifically, like what's the purpose of `AddrMan`?
How can it go wrong?

### Address Manager

Amiti Uttarwar: 00:28:59

Yeah, I mean, that's a great segue because that's the main way that we are able to protect ourselves, but also participate in this relay of addresses.

`AddrMan` stands for address manager.
Essentially what it does is stores all of these IP addresses.
But there's a lot of cleverness in the design to make sure you're not... again, if you stored everything then that would be a memory DoS.
So how do you store it?
How do you make sure that a malicious or inadvertent identity can't bias your `AddrMan`?
How do you make sure that the noise doesn't outweigh the work that you have done?
It seeks to answer those sorts of questions.
At a high level, the way it does that is it breaks down the storage component into two different tables, the new table and the tried table.

#### New table and tried table

Amiti Uttarwar: 00:30:00

So the new table is where the addresses initially go, and that would probably be quite full most of the time after you've started up a node and have been running it for a while.
The tried table is what you're protecting.
Those are the ones that are saying - I've connected to a node there, I believe it to be good, and I want to be able to refer back to it in the future for when I'm seeking peers.

Adam Jonas: 00:30:27

Just to double click on that, the tried table is - it gets moved from the new (table) by opening a connection, and therefore you verify that it's a Bitcoin node somewhere.
You don't know if it's a good or a bad Bitcoin node, but it's something.

Amiti Uttarwar: 00:30:41

It's doing the dance.

Adam Jonas: 00:30:42

Then you file that away for future use.

Amiti Uttarwar: 00:30:45

Yeah, and then of course it could go offline, it could have successfully done the version handshake but then not know what a block is, there are things that could go wrong for sure, but we store it as a likely candidate versus this random set of numbers that was sent to us in the IP address.

### The Bitcoin network “dance”

Adam Jonas: 00:31:08

I think there's two things you said in there that I just want to hear you explain.
You said - do the dance? (Amiti's laughter)
Can you tell me a little bit more about said dance?

Amiti Uttarwar: 00:31:19

Yeah, well, there's a couple of layers.
In order to open a connection, there are layers that are totally outside of Bitcoin, like running a TCP connection, there's going to be a different sort of version handshake.
Then at the Bitcoin level we also have a version handshake, and that's essentially if you and I were trying to connect to each other, we would send each other a version message, and that would have some metadata about what I'm running, what services I offer, that sort of stuff.
Then you would send me yours, and then when I receive it, I would send you a [`VerAck`](https://developer.bitcoin.org/reference/p2p_networking.html#verack), and when you receive mine, you'd send me a `VerAck`.
So there it is, super oversimplified... there's a lot of detail to the dance.

Adam Jonas: 00:32:04

Someone should make a video and superimpose this on top of like peacocks putting up their tail, and doing this dance (Murch's laughter), and the peahen does the dance back, and then the peacock does more.

Amiti Uttarwar: 00:32:17

Yes, a projack[unclear].

Adam Jonas: 00:32:18

Someone should get on that (laughter).

Amiti Uttarwar: 00:32:20

What are you up to, Jonas?

#### Transaction download on Bitcoin’s p2p network comic

Amiti Uttarwar: 00:32:22

I do have a [comic that illustrates](https://github.com/amitiuttarwar/bitcoin-bytes/blob/master/tx-download.jpg) the version handshake and there are little like... boxy nodes.

Adam Jonas: 00:32:30

Put in the show notes (laughter).

Amiti Uttarwar: 00:32:33

Really animating Bitcoin P2P is something that I really hope exists in the world soon.

## Addresses and Proof-of-Work

Mark Erhardt: 00:32:40

You mentioned earlier, there is no Proof-of-Work attached to an address announcement.
Why not?
Like if you self-announce your node, if you were required to attach some modicum of Proof-of-Work, then your address announcement would be relayed with that Proof-of-Work.
That might make it slightly bigger, but might make it harder to spam as well.

Amiti Uttarwar: 00:33:05

You'd have to think it through, making sure it's not easy to hack.

Say I self-announced, and I did this Proof-of-Work thing, and then you were an honest node and you forwarded it on, but if you were a malicious node, what if you just kept it, and then kept sending it over and over and over again.
How does that work?
So then maybe you solve that with a time limit, but then you're on a decentralized network and oh my God, time on a decentralized network is very hard.
Very, very hard.
So then what do you do there?
I don't think it's impossible, I think it would just have to be fleshed out.
I mean, it's also a strange incentive, right?
Because there's this asymmetry between inbound connections and outbound connections.

## Inbound and outbound connections

Amiti Uttarwar: 00:34:00

If you start a Bitcoin Core node, then you automatically will make eight outbound full relay connections, and two outbound block relay only connections, and some of them will enable inbound connections.
So in order to have an outbound, you need someone who is accepting inbounds that has open slots that you can connect to.
That's the only way to get onto the network and participate in it.

Having inbound slots is more optional.
Obviously, it would require more resources to support, and mainly the challenging thing is when there's all these custom firewalls that different routers different NATS... all these rules that are outside what the Bitcoin application has the ability to access.
So although the application comes with enabled inbounds by default, I think the vast majority of users have to go do some additional configuration.
They may or may not realize, may not be willing to do, like who knows?
So there's an intrinsic asymmetry between the types of connections.
It's also easier for attackers to create lots of inbound connections.
Whereas if you connected to them, they'd just have to be sitting around and get lucky.
So there's a lot of differences between inbounds and outbounds.

## Block relay only connections and full connections

Amiti Uttarwar: 00:35:28

Going back to those three different kinds of things - transactions, addresses, and blocks - each one of them has specific different ways that they can be used to reduce privacy.

Addresses, you could do some triangulation of sending fake addresses, and then having different connections on the network, and then observing where those addresses show up because of the way relay works.
There's also other things you could do.
You could have a node there and see who learns about it, et cetera.

Transactions, you could do things like have double spends that you send one to one side of the network, and another to the other side, fast enough, and then you start probing and seeing which transaction does this node have, and that way you can learn who each node is more connected to, and the distribution of nodes on the graph.
That's one example.
But there's just so many more ways that these different pieces of information can be utilized to reduce privacy.

Blocks are the hardest thing to fake because of Proof-of-Work.
In order to use them to reduce privacy, that means you need to make a bunch of blocks, and that's by definition difficult.
So blocks are the most crucial component of not having a partition on the network.
If everybody has the chain's tip, that's a better worst case than if people have different chain tips, or operating on different forks or versions.
So blocks are the most crucial and they're the hardest to fake.
So having block relay only connections, they do not relay transactions, they do not relay addresses, they are going to be a lot harder for a third party to figure out heuristics in order to observe that this connection is present, and can just intrinsically by creating a more saturated network graph, increase the guarantees of the network, and it can have that saturation without compromising on the amount of resources too much, because just relaying blocks is much, much easier than validating transactions, than checking addresses, than allocating all the resources required to do that work.

So there's a few different reasons, and I think it's very cool, because when we say that there's contention between having privacy as well as reliability, block relay connections are an innovation that increased the guarantee of both, which I think is extremely clever.

Adam Jonas: 00:38:20

That's interesting.

Amiti Uttarwar: 00:38:22

I think so.

Adam Jonas: 00:38:23

Are there other things you're thinking about `AddrMan` as you continue to do this monk like study of understanding things that were decided ten years ago, and now have survived all sorts of adversarial attacks, and that's amazing.

Amiti Uttarwar: 00:38:39

I mean, so many things. (Laughter)

Adam Jonas: 00:38:42

Give us one to sign off on.
What's your favorite thing you've learned about `AddrMan` in the last month?

Amiti Uttarwar: 00:38:47

The thing that pleases me is getting to know it.
It's fun to go into a component, and it just feels terrifying and murky and overwhelming, and then you just keep nicking away at learning it, and I really enjoy that process.
It actually reminds me a lot of backpacking, where I'll do a lot of off-trail stuff, and when you come to a campsite that's in the middle of literally nowhere, no humans in sight, it can be so terrifying to just be in random mountains and there's a tendency to stay really close to wherever you've set up your tent.

But then as the night passes, and the next morning, or however long you're there for, you start getting more familiar.
You have to go to the river to get water, you might just get interested by something, go on a hike, and you get to know this whole little corner and it becomes super homey, even though you're kind of in the middle of nowhere.

I feel very similarly about Bitcoin, where I'll come in and just be like, oh my god what is happening here, why do I like this?
Then slowly nick away at it, and it becomes comfortable, and it becomes fun to get to know something intimately.

Adam Jonas: 00:40:07

Your radius has expanded quite a bit.
Glad to have you back, glad to have her in the office.

Amiti Uttarwar: 00:40:11

It's great to be here.

Adam Jonas: 00:40:12

All right, I think that wraps it up for today!
So what do you think of that Murch?

Mark Erhardt: 00:40:16

Very interesting.
The five principles sound very straightforward, but then when you dive a little deeper, there's a lot to unpack there.
You always have trade-offs.
You can't just get all of five of them.

Adam Jonas: 00:40:30

For someone who's in the weeds of P2P, it is hard to go high level and also talk about the details, and so I think Amiti did a pretty good job of giving us an outline, but I know she really wanted to talk about things that were over our heads.
I also think that, and I mentioned this during the episode, you pull one lever over here and something else pops up over there and the trade-offs and the nuances of this system are quite complex.
So I appreciate that people are thinking very deeply about this and keeping us safe out there.
We'll be putting up some show notes and hopefully be doing more episodes soon.
We apologize for the long layoff, but hope you enjoyed it.
