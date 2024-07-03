---
title: "The P2P network"
transcript_by: kouloumos via tstbtc v1.0.0 --needs-review
source_file: https://anchor.fm/s/12fe0620/podcast/play/41966810/https%3A%2F%2Fd3ctxlq1ktw2nl.cloudfront.net%2Fstaging%2F2021-9-18%2F4bec062e-5ccc-96b3-26a2-f406eedee214.mp3
media: https://podcasters.spotify.com/pod/show/chaincode/episodes/Amiti-Uttarwar-and-the-P2P-network---Episode-15-e18v7oq
tags: ['bitcoin-core', 'eclipse-attacks', 'p2p']
speakers: ['Amiti Uttarwar']
categories: ['podcast']
summary: "Amiti returns to the Chaincode office to discuss all things p2p."
episode: 15
date: 2021-10-18
additional_resources:
-   title: 'Searchable #bitcoin-core IRC logs'
    url: http://bitcoin-irc.chaincode.com/bitcoin-core-dev/
-   title: Eclipse Attacks
    url: https://bitcoinops.org/en/topics/eclipse-attacks/
-   title: Altnet
    url: https://github.com/ariard/altnet-proposals
-   title: Transaction download on Bitcoin's p2p network comic
    url: https://github.com/amitiuttarwar/bitcoin-bytes/blob/master/tx-download.jpg
---
Speaker 0: 00:00:00

When you have all of these different components in the system, even a very simple rule can turn into this kind of infinitely complex interactions.
And it's incredibly difficult to wrap your head around at such grand scale.
And that's also something that makes it really cool because that's why it's so important to collaborate.

Speaker 1: 00:00:25

♪♪♪ Hi, I'm Jonas and welcome to the Chaincode Podcast.

Speaker 2: 00:00:41

Hi, I'm Murch.
Welcome back, Murch.

Speaker 1: 00:00:43

It's been a while.
So who are we bringing on as a guest today?

Speaker 2: 00:00:47

We'll have Amity on today.
She's gonna talk with us about peer-to-peer.

Speaker 1: 00:00:51

It's been a while since Amity's last been in the office.
That was 2019 when she was a resident and we're glad to have her back.
So enjoy the episode.
Welcome Amity.
Welcome back to Chaincode.
What is it like to be back at Chaincode?
How have things changed in the last two years?
Nothing's changed in the last two years, I assume.

Speaker 0: 00:01:10

Definitely feels a lot calmer.
I'm the slightest bit less aggro about my interest in learning Bitcoin, but not all that much different.
It just comes and goes, you know.

Speaker 1: 00:01:23

Welcome back and today we are delighted to talk about P2P because it's all of our favorite subjects.

Speaker 0: 00:01:31

Is it?

Speaker 1: 00:01:32

It's gonna be by the end of this episode.
Maybe to start things off, why do you work on P2P?
Why is it interesting?

Speaker 0: 00:01:40

I love P2P.
I find it to be so fascinating.
I think What really compels my interest is the fact that you have a very bounded set of rules that behave logically.

## Why Amiti works on P2P

Speaker 0: 00:01:52

So what a node is doing is a very well-defined programmatic execution of rules that it's been told.
And that we can go look at the code and see.
But then even really simple things when you expand it to a network of nodes that are running all over the world, they're running different versions of Bitcoin Core, they're running alternate clients and you've got potential malicious adversaries, you have potential inadvertent mistakes that could occur, whether in Bitcoin Core or alternative clients, and all sorts of stuff in between.
You even have people who do things that are odd, that have no clear benefit, and then you go, ah, maybe that's academic research, who knows?
And so When you have all of these different components in the system, even a very simple rule can turn into this kind of infinitely complex interactions.
And it's incredibly difficult to wrap your head around at such grand scale.
And that's also something that makes it really cool because that's why it's so important to collaborate.
And in Bitcoin Core, obviously peer review is such a fundamental aspect of our development ecosystem.
And I think it's really cool to constantly have more components that give me clues to understand the thing that is happening.
But I can't see the whole thing.
I can't see exactly who's sending what messages in all between all of the nodes on the Bitcoin network, but I can get lots of clues and enough that I can reason about them and make choices based on different heuristics.
So It's both very bounded and scoped.
There's what a node is doing is so well defined, and yet it's endless and complex.
And I can just sit around thinking about it.
It feels kind of like an intellectual play space for me to try to imagine all of these different Incentives and possibilities and how do we make progress in that land of chaos?

Speaker 1: 00:04:12

Okay, so we get it P2P is cool How do you how do you think about sort of like designing P2P?
Just like off at the top of your head, if you had to just come up with a framework, just out of thin air, how would you be thinking about the design?

## A framework for p2p design

Speaker 0: 00:04:28

Yeah, that's a very good question.
Clearly never thought about this before.
But I'd imagine that you could have five principles.
Just out of thin air.
Yeah, let's just call them that you want the network to be Reliable, timely, accessible, private, and upgradable.

Speaker 1: 00:04:50

Okay, so you're very smart.
But the fact that you came up with those at the top of your head, how did you think of those five characteristics and how did those sort of come to be?

Speaker 0: 00:05:00

Maybe a better answer to your question earlier of what has changed in the last two years of working on Bitcoin is kind of the way that I glean information.
I think there is so much context to all of the choices, all of the code, how the network works.
And it came from Bitcoin Core and all of the things that have been observed within that ecosystem, within the Bitcoin ecosystem, but also prior to that.
So a lot of what I've spent my time doing is trying to better understand how people who are much more experienced than me are approaching these kinds of problems and Something really cool is this is all open source.
So you can just go find out even if it was a decision that was made in 2013 you can go dig it up and sometimes we'll come across these wonderful elaborate comments just left on PRS that go into depth about why this one line of code must be this particular way, or prolific contributors totally fundamentally disagreeing on what we should be valuing.

Speaker 1: 00:06:11

I have a question about that.

## How do we systemize Bitcoin Core knowledge?

Speaker 1: 00:06:12

So as we're sort of systematizing that kind of information, like how do we memorialize that and how do we keep those records and create that web of context so that newcomers like yourself or the next to me can get to those things faster?

Speaker 0: 00:06:30

I would say the first question is, is it important or beneficial to be able to get to those things faster?
Because on one hand, I definitely think there's ways you could speed up sharing context.
And I think that's beneficial to all of us working on the project of how do we share this knowledge and make sure that we're building it up over time amongst a changing set of contributors versus going in circles or losing things that we once understood.
On the other hand I feel like it's so cool that it's all there and the fact that I can access it and I feel like in my personal journey taking that scenic route of getting there has taught me stuff that I can't necessarily quantify and it's hard to know what would be lost if you just tried to like dump all this super technical information in my brain I probably wouldn't have been able to parse it so maybe part of it was that it took me a long time and I say past tense but like it's still taking me a long time.
I heard things today that I have on my list to go dig up history about that are intriguing to me.
So it's kind of a hard question to answer, because we also don't have the ability to just like A-B test what it means to learn a complex system.

Speaker 2: 00:07:53

Also there's just so much by now there is so much content that you can't really read it all Like no single person can understand all the design decisions that were made in Bitcoin anymore, especially if you count Lightning Network as well.

Speaker 0: 00:08:09

Definitely there's too much content, but then I think that relates to the question of how do you surface the nuggets of wisdom that are the shiniest?
Are they just needles in the haystack?
Or can you just say here it all is?
I think there's some in between.
Having searchable IRC logs is really cool.
Really helpful.

## Searchable #bitcoin-core IRC logs

Speaker 1: 00:08:34

We now have searchable IRC logs.
Speaking of taking the scenic route, we took the scenic route around the design goals.
You mind if we go back and sort of talk about how you arrived at those things and how they what the interaction between them might be.

Speaker 0: 00:08:52

Yeah absolutely and I can dig into breaking them down and what I mean by these words because they're just words that are attempts to capture larger ideas.

Speaker 1: 00:09:03

They all sound great.
Like, everybody wants reliability, timeliness, accessibility, privacy, upgradability.
Like, I'll take them all.
So No trade-offs, right?

Speaker 0: 00:09:16

No trade-offs, if you can somehow do them all.
As I was trying to navigate this world, I wanted something succinct that I could refer back to.
And then in the process of making that, realized that this is a convenient tool to try to communicate with others the things that I value and am striving for.
So the first three, reliable, timely, and accessible, as features of network, I think are important for any successful peer-to-peer network.
What I mean by reliable is that if you submit a valid message to the network, it will eventually be delivered to all other nodes that are participating on the network.
So you get a message in, it'll go everywhere.
That's reliability if you can predict that with confidence.
What I mean by timely is how long it takes to get there.
And looking at Bitcoin, the timeliness of each message has very different goals and constraints that we strive for.
So for example with transactions, it's important that people get transactions quickly in relation to how long it took for a block to be mined.
But when you say that blocks need to be arriving quickly, those are two very different time scales.
Transactions can take like several seconds, tens of seconds, whereas blocks, there's been so much work to reduce any latency.
And in transactions, we actually use that latency for other benefits, which we can dig into more.
But the second thing is that you have a network, so you can send a message, and then it's timely, so that message actually gets where it's going in a reasonable amount of time.
And then the third is that the network is accessible.
That node operators actually have the ability to participate.
Like, that's great if that's there, but if you can't get on it, what does it matter?
And I think every project is going to have to define that for themselves.
And in Bitcoin, at a very technical level, what I mean by saying accessible is minimizing the resource requirement that is necessary to run a node.
Everything from that to being able to connect to honest nodes when you start up and being able to bootstrap and find peers and there's also I think censorship resistance can come into here Like no node can prevent another node from participating in the network, which is a fundamental premise that we are constantly thinking about in the day-to-day decisions that we are making.
And so I've kind of like loosely summed this all up as the term accessible.
Like you have to be able to use the network.
And so these three values, I think, to different extents or in different ways, any successful peer-to-peer network needs to have.
But I think we have two additional ones in Bitcoin that we really value.
The next one is privacy.
And that, you know, probably is not a hard sell for people listening to a Bitcoin podcast.
It's money.
And if you want to use money freely, it has to be private.
And the last one is upgradability.
And what I mean there, that actually is a very hard one to achieve technically.
But what I mean there is giving users choice.
If you have phone software or any app you run, most technology in this day and age at some point they'll just be like, listen, upgrade your phone or I will do it for you, or maybe it'll just stop working.
You don't really as a user have a lot of choice in what version or how the rules changed at some point You just have to hit accept or like maybe you can delete the app or get a new phone or whatever But projects aren't prioritizing that Whereas in Bitcoin we really prioritize that anyone who participates in the system, if they have bought into a specific set of rules at a time, then they should always be able to continue using Bitcoin with that rule set.
So even if others adopt more or less whatever rules then they shouldn't be forced to do anything different.
They can literally go into a cave, come out and spend their Bitcoin ten years later.
And so that's a very challenging thing to to value and to design around.
Obviously there are tons of conversation about soft forks versus hard forks and blah blah blah blah blah.
But I think there's a core value here that we want everyone to be empowered regardless of how you're interacting with the system.
And that also goes to how we develop of people have choice of their level of involvement.

Speaker 1: 00:14:12

Are these in order in any way?
So you grouped the top three as in any peer-to-peer network.
Do you order these in terms of priority or in terms of what the PV network needs?
Because otherwise I could come up some really good acronyms here.
You are Pat is how I remember this or maybe rat up Rat up.

Speaker 0: 00:14:32

I do think you are Pat is a little friendlier.

Speaker 1: 00:14:35

Okay, I like rat up or rat PU.
You've covered some of these designs.

Speaker 0: 00:14:38

Wait, up art.

Speaker 1: 00:14:40

That doesn't speak to me.
Art up.

## Forward compatibility and upgradability

Speaker 2: 00:14:47

What I really hear when you say that you want upgradability, you talked a lot about forward compatibility, but is there also an aspect of the people that go into the cave for 10 years and they come back and want to spend their coins, but the people that are staying there and constantly tinkering and thinking about new use cases, they want to introduce new rules or new features.
Isn't that also a big part of upgradability?

Speaker 0: 00:15:17

Yeah, definitely.
That's kind of the contention of how do you have both.
I don't think it makes sense to say, okay, Bitcoin Core is done.
Let's just stop now.
And also Bitcoin's done, you know, let's just, We're good.
I'm definitely not advocating for that.
I mean most of the features that we want are in some way or another Related to the other goals and even if they're not I'd figure out a way, you know At least in my mind.

Speaker 2: 00:15:46

So Bitcoin is inevitable.
You've heard it here first.

Speaker 1: 00:15:51

So you've covered these design goals and then maybe you could talk about how these actually work in practice.
How does the rubber hit the road on these concepts?

Speaker 0: 00:15:59

So maybe we can dig into a couple of different examples.

## Partition resisitence

Speaker 0: 00:16:03

One that I find interesting is a threat to reliability is that if there's any partitions in the network then your message cannot make it to all other participants ever, you know?
And so partition resistance is something that we think a lot about in P2P as a very core principle.
And digging into that, it's been surprising to me to realize the depth of thought that contributors have had.
Like, okay, there's one class of malicious attackers are trying to isolate this specific node so that they can do something weird.
Eclipse attacks.
Now they are under, well, not control, but like they're subject to your lens of seeing the whole network.

Speaker 1: 00:16:51

Yeah, maybe you can describe what an eclipse attack is.
I don't think we've covered that.

Speaker 0: 00:16:55

Really?

## Eclipse Attacks

Speaker 0: 00:16:55

Well, an eclipse attack is essentially where A node believes that they're connected to multiple participants on the network and thus getting a view of the activity on the network.
But really, they're connected only to one adversarial entity.
So they might have multiple connections, they might be going to different IP addresses, but they're all controlled by one entity that's collaborating with each other.
So now their view of the world has been eclipsed.
And because proof of work is so cool, there's still, it's not quite game over, it's just very close.
So this attacker can't, it would still be extremely challenging to fake blocks because you still have to have valid proof of work and that's not trivial at this stage of the, you know, of the hash rate and stuff.
And so that isn't a trivial attack that they can do, but they can still do other clever attacks.
Obviously privacy is going to be totally lost and they can try to mislead into having double spends based on kind of kidnapping transactions or selectively revealing what transactions this entity sees.

Speaker 1: 00:18:11

And I think with the, you know, prevalence of lightning, you also need to be careful about sort of the view of lightning justice transactions and things like that.

Speaker 0: 00:18:20

Yeah, yeah.
The whole threat model definitely changes when you bring in the incentives of lightning and in other cases where one transaction wouldn't have been very lucrative to suppress in Lightning, it could be.

Speaker 1: 00:18:35

Yeah.
I think that also maybe in addition to that, thinking about eclipsing mining nodes is another sort of issue of wasting hash power, like.

Speaker 2: 00:18:47

Reducing the global hash rate in order to make it difficult to go down for yourself There's the selfish mining attack sort of angle.

Speaker 0: 00:18:55

That's I mean, so another attack that you could do that involves a partition but might not be as specific would be like say you were able to partition all of China off of the rest of the world so now the hash rate has been super broken up and it's much easier to to do hash rate oriented attacks because you now have like half as much that you're trying to compete with just by creating a partition.

Speaker 1: 00:19:23

And that also be like thinking of like a state level kind of issue.
Yeah.
Well, rejoining the network, reconciling.

Speaker 0: 00:19:32

Absolutely.

Speaker 2: 00:19:33

Well, slow down here, right?
There's no hash rate in China anymore.

Speaker 0: 00:19:36

Oh I can't keep up.
But there's actually things like what if there is a crazy natural disaster and the internet pipes that are at the bottom of the oceans like, you know, disconnect.
I mean, I think it's cool that there's a whole ecosystem of people solving it.
Like, apparently there's satellites that will solve this or I don't really know what's going on there.

Speaker 2: 00:20:00

I believe I've been told that there's also a radio transmitted like a radio source for the blockchain here in New York.

Speaker 0: 00:20:07

Nice.

Speaker 2: 00:20:08

So yeah, you can receive it via satellite feed from for example, the Blockstream satellite.
It will broadcast not only the latest blocks, but the whole blockchain every 24 hours.

Speaker 0: 00:20:20

Nice.

Speaker 2: 00:20:20

And I've seen reports of like ham radio transfer transactions, but also I think on some radio frequencies the latest blocks are being broadcast.

Speaker 1: 00:20:30

Yeah, I mean,

## Altnet

Speaker 1: 00:20:31

this is why Antoine is going after the alt net kind of stuff Is that having different transport layers allows us to be a little bit more flexible, maybe a podcast for another day What's actually being passed around the network like we've talked about these high-level You know words, but what's what's actually going across the wire?

Speaker 0: 00:20:52

Yeah, so there's plenty of P2P messages.

## Messages sent across the wire

Speaker 0: 00:20:55

Some of them are kind of operational, like, hey, this is how we establish a connection.
We'll do this specific dance to make sure that we're compatible and you're listening to the rules of the Bitcoin network.
But the three main things that bring about complexity and thus are the most interesting are addresses, transactions, and blocks.
So blocks are hopefully pretty evident why those are important.
Obviously they have transactions in them, but when I say transactions, what I mean are the unconfirmed ones that haven't been mined yet.
So that's important to get to miners and enlightening for different reasons, but to get around the network so that they can make it into a block.
And then addresses are, we have something called an adder message and essentially what this contains is just to clarify yeah ip addresses because we also use it for the invoice address yeah exactly exactly so what I mean by addresses here are the location of where the nodes are, those IP addresses, versus wallet addresses or like the 5,000 other types of addresses we have in this world.
So these adder messages are related back to partition and I mean a lot of things of just how do you find other other people that you can talk to and so these three are very complex because when we go back to the design goals for each type of this message we can look at what makes them very challenging to achieve these goals for.
For example, transactions, as we mentioned, we want them to be timely and get to all of the other peers and saturate the network within, you know, no more than like a minute or two.
And at the same time, we don't want bandwidth requirements to be insane because then the cost of the hardware for running a node would go up so high that at some point if the network scales enough, then you know there's only a handful of people in the world or maybe organizations that are able to afford the hardware requirements.
That's the accessibility goal.
So we need to do clever tricks to figure out how do you get this out, but you don't want to just spam everyone.
And that's getting really into that is the nuances that I spend my days thinking about.
Similarly, it's when you think of transactions and you want them to be private, but then you also want them to get out to the network.
That's kind of a ridiculous concept.
You're like, hey everyone, there's this transaction, but maybe it's not mine.
How do you pull that off?" So that's another tricky contention that you have to work with and find solutions that aren't necessarily making compromises but are improving both at the same time.
Those are some examples of what makes transactions hard.
And we can look at blocks and addresses through a similar lens.

Speaker 1: 00:24:07

It sounds like as you dive deeper and explain the world of P2P, it's pretty fast.
There's a lot of nuance, there's a lot of trade-offs, and there's a lot of, I move a lever here and something pops up way over there.

Speaker 0: 00:24:22

Oh my god, yeah.

Speaker 1: 00:24:23

And so in that world of interesting things, what's most interesting to you?
What are you working on?

## AddrRelay and AddrMan

Speaker 0: 00:24:31

Well, what's really captivated my interest right now has been Adder Relay, and specifically right now is Adder Man, which is the address manager, which is keeping track of all these IP addresses that you're getting from the network.
But generally I do think add or relay is an area that's so hard to comprehend that we don't have a great shared understanding of how it works, what design goals are.

Speaker 1: 00:25:00

Can you maybe start from the top?
So yeah, I'm breaking down add a relay to be address relay, which means that I'm relaying addresses via my node.
To what end?
Where those come from?
How do they get to me?
Like, can you talk a little bit about that?
That?

Speaker 0: 00:25:15

Yeah I can.
Say I start a brand new Bitcoin node and I'm like great I need friends.

## Bootstrapping, DNS seeds and address announcements

Speaker 0: 00:25:25

Who do I talk to?
Who knows how to speak Bitcoin?
So we have some bootstrapping mechanisms.
Namely one of the biggest ones is DNS seats.
And so that's a set of destinations that are hard-coded that you can hit and they will return information about active nodes on the network.
And then with that information I can go and try to connect to a bunch of those nodes.
We don't want that to be the only way that we learn about nodes or other nodes learn about us, you know, in turn, because it's essentially a more centralized solution.
If someone was an attacker and was able to give you false addresses, then they can get you into an eclipse situation.
So we have a lot, lot more types of mechanisms.
There are some that can be inputted by users, but the main automatic ones come down to self-announcing your own address and then it trickling through the network.
And then also when you connect to peers, sending them a get adder message, which just says, hey, send me a bunch of addresses, please.
So those are the two main ongoing mechanisms for automatic address relay.
But the things that make it challenging are that unlike transactions or blocks, addresses don't have evidence of work and in order to verify it I have to do a lot more than what you have to do to tell it to me.
So to break that down a little bit, you send me an IP address, say you say it's 1111, then I can look at that number and say, well, that's an invalid range or that's a valid range, but I don't know if there's actually a Bitcoin node there.
The only way I can figure out if there's a legitimate Bitcoin node there is by trying to connect to this IP address, seeing if they respond and do the version handshake and then disconnecting, And then I can say, great, it's a good one.

## DoS issues

Speaker 1: 00:27:32

So that sounds like it's lends itself to a denial of services, asymmetric work based on just applying a string, right?

Speaker 0: 00:27:40

Yeah.
So if, if we did a very naive, like, great, you sent me an address.
Now I will tell everybody and everyone will tell everybody and we just kept doing that.
First off, if you can kind of imagine the visual, if there was no end to it, you would just have a whole network of nodes that are just constantly firing.
It would be like neurons or something, which means it could be infinite.
So if we just trivially did that, it would immediately be a bandwidth DOS.
But then you also need heuristics of how do you get it out enough?
Because if you tried to verify everything, it would essentially be a CPU DOS.
Like in order to send out one address, I had to spend enough compute power to like try to open a connection via TCP, blah, blah, blah, blah, blah.
It would be a CPU DOS, or no addresses would go anywhere.
So how do you balance those extremes and have something reasonable where nodes can hear about addresses but also don't get super spammed.

Speaker 1: 00:28:49

And so we're talking about an Adder Relay right now.
Maybe talk about AdderMan, sort of pivot into specifically, like what's the purpose of AdderMan?
How can it go wrong?

## Address Manager

Speaker 0: 00:28:59

Yeah, I mean, that's a great segue because that's the main way that we are able to protect ourselves, but also participate in this relay of addresses.
So Adderman stands for address manager.
And essentially what it does is stores all of these IP addresses.
But there's a lot of cleverness in the design to make sure you're not, again, if you stored everything then that would be a memory DOS.
So How do you store it?
How do you make sure that a malicious or inadvertent identity can't bias your adder man?
Or how do you make sure that the noise doesn't outweigh the work that you have done?
It seeks to answer those sorts of questions.
So at a high level, the way it does that is it breaks down the storage component into two different tables, the new table and the tried table.

## New table and tried table

Speaker 0: 00:30:00

So the new table is where the addresses initially go, and that would probably be quite full most of the time after you've started up a node and have been running it for a while.
The tried table is what you're protecting.
Those are the ones that are saying I've connected to a node there, I believe it to be good, and I want to be able to refer back to it in the future for when I'm seeking peers.

Speaker 1: 00:30:27

Just to double click on that, the tried table is it gets moved from the new by opening a connection and therefore you verify that it's a Bitcoin node somewhere.
You don't know if it's good or bad, but it's something.

Speaker 0: 00:30:41

It's doing the dance.

Speaker 1: 00:30:42

And then you file that away for future use.

Speaker 0: 00:30:45

Yeah, and then of course like it could go offline it could have Successfully done the version handshake, but then not know what a block is or you know there are things that could go wrong for sure, but we store it as a likely candidate versus you know this random set of numbers that was sent to us in the IP address.

Speaker 1: 00:31:08

I think there's two things you said in there that I just want to hear you explain.
You said you say do the dance.
Can you tell me a little bit more about said dance?

Speaker 0: 00:31:19

Yeah, well, there's a couple layers.
Like in order to open a connection, there's layers that are totally outside of Bitcoin.

## The Bitcoin network “dance”

Speaker 0: 00:31:26

Like running a TCP connection, there's going to be a different sort of version handshake.
But then at the Bitcoin level we also have a version handshake and that's essentially if you and I were trying to connect to each other we would send each other a version message and that would have some metadata about what I'm running, what services I offer, that sort of stuff.
And then you would send me yours and then when I receive it, I would send you a Verac.
And when you receive mine, you'd send me a Verac.
So there is super oversimplified.

Speaker 1: 00:32:04

There's a lot of detail to the dance one should make a video and superimpose this on top of like peacocks putting up their tail and like doing this dance the hen does the dance back and then the peacock does more.

Speaker 0: 00:32:17

Yes, a projack.

Speaker 1: 00:32:18

Someone should get on that.

Speaker 0: 00:32:20

What are you up to, Jordan?

## Transaction download on Bitcoin’s p2p network comic

Speaker 0: 00:32:22

I do have a comic that illustrates the version handshake and there are little like boxy nodes.

Speaker 1: 00:32:30

Put in the show notes.

Speaker 0: 00:32:33

Really animating Bitcoin P2P is something that I really hope exists in the world soon.

Speaker 2: 00:32:40

You mentioned earlier, there is no proof of work attached to an address announcement.

## Addresses and proof of work

Speaker 2: 00:32:45

Why not?
Like if you self-announce your node, if you were required to attach some modicum of proof of work, then your address announcement would be relayed with that proof of work.
That might make it slightly bigger, but might make it harder to spam as well.

Speaker 0: 00:33:05

I mean, you'd have to think it through of what kind and what it, like making sure it's not easy to hack or just cause I provided it once, like say I gave it to you and I self-announced and I did this proof of work thing and then you were an honest node and you forwarded it on, but if you were a malicious node, what if you just kept it and then kept sending it over and over and over again.
How does that work?
So then maybe you solve that with a time limit, but then you're on a decentralized network and oh my God, time on a decentralized network is very hard, very, very hard.
So then what do you do there?
And I don't think it's impossible.
I think it would just have to be like flushed out.
I mean, it's also a strange incentive, right?
Because there's this asymmetry between inbound connections and outbound connections.

## Inbound and outbound connections

Speaker 0: 00:34:00

If you start a Bitcoin Core node, then you automatically will make eight outbound full relay connections and two outbound block relay only connections.
And some of them will enable inbound connections.
So in order to have an outbound, you need someone who is accepting inbounds that has open slots that you can connect to.
That's the only way to get onto the network and participate in it.
Having inbound slots is more optional.
Obviously, it would require more resources to support and mainly the Challenging thing is when there's all these custom firewalls that different routers different Nats different all these rules that are outside what Bitcoin application has the ability to access.
And so although the application comes with, yes, enable inbounds by default, I think the vast majority of users have to go do some additional configuration.
They may or may not realize, may not be willing to do, like who knows.
So there's an intrinsic asymmetry between the types of connections.
And it's also easier for attackers to create lots of inbound connections.
Whereas if you connected to them, they'd just have to be like sitting around and get lucky.
So there's a lot of differences between inbounds and outbounds.

## Block relay only connections and full connections

Speaker 0: 00:35:28

Going back to those three different kinds of things, transaction, addresses, and blocks, Each one of them has specific different ways that they can be used to reduce privacy.
So addresses, you could do some like triangulation of sending fake addresses and then having different connections on the network and then observing where those addresses show up because of the way relay works.
There's also other things you could do.
You could have a node there and see who learns about it, et cetera.
Transactions, you could do things like have double spends that you send one side of the network and another to the other side fast enough, and then you start probing and seeing which transaction does this node have, And that way you can learn who each node is more connected to and kind of like the distribution of nodes on the graph.
That's one example.
But there's just so many more of ways that these different pieces of information can be utilized to reduce privacy.
Blocks are the hardest thing to fake because proof of work.
So in order to use them to reduce privacy, that means you need to make a bunch of blocks and that's by definition difficult.
So blocks are the most crucial component of not having a partition on the network.
If everybody has the chain's tip, that's a better worst case than if people have different chain tips or operating on different forks or versions.
So blocks are the most crucial and They're the hardest to fake.
So having block relay only connections do not relay transactions.
They do not relay addresses.
And so are going to be a lot harder for a third party to figure out heuristics in order to observe that this connection is present.
And can just intrinsically by creating a more saturated network graph, increase the guarantees of the network, and it can have that saturation without compromising on the amount of resources too much, because just relaying blocks is much, much easier than validating transactions, than checking addresses, than allocating all the resources required to do that work.
So there's a few different reasons, and I think it's very cool, because when we say that there's contention between having privacy as well as reliability, BlockRelay connections are innovation that increased the guarantee of both, which I think is extremely clever.

Speaker 1: 00:38:20

That's interesting.

Speaker 0: 00:38:22

I Think so.

Speaker 1: 00:38:23

Are there other things you're thinking about how to man as you continue to do this monk like study of Understanding things that were decided ten years ago and now have survived all sorts of adversarial attacks and that's amazing.

Speaker 0: 00:38:39

I mean, so many things.

Speaker 1: 00:38:42

Give us one to sign off on.
What's your favorite thing you've learned about Adderman in the last month?

Speaker 0: 00:38:47

The thing that pleases me is getting to know it.
It's fun to go into a component and it just feel terrifying and murky and overwhelming and then you just kind of keep nicking away at learning it and I really enjoy that process.
It actually reminds me a lot of backpacking, where I'll do a lot of off-trail stuff, and when you come to a campsite that's kind of in the middle of literally nowhere, no humans in sight, it can be so terrifying to just be in random mountains and there's a tendency to stay really close to wherever you've set up your tent.
But then as the night passes and the next morning or however long you're there for, you start getting more familiar.
You have to go to the river to get water, you might just get interested by something, go on a hike, and you get to know this whole little corner and it becomes super homey, even though you're kind of in the middle of nowhere.
And I feel very similarly about Bitcoin where I'll come in and just be like, oh my god What is happening here?
Why do I like this and then Slowly nick away at it and It becomes comfortable and it becomes fun to get to know something intimately, you know Your radius has expanded quite a bit glad to have you back glad to have her in the office It's great to be here.

Speaker 1: 00:40:11

All right, I think that wraps it up for today All right.
So what do you think that much?

Speaker 2: 00:40:16

Very interesting the five principles sound very straightforward But then when you dive a little deeper, there's a lot to unpack there You always have trade-offs.

Speaker 1: 00:40:26

You can't just get all of five of them for someone who's in the weeds of P2P it is sort of hard to go high level and also talk about the details and so I think Amini did a pretty good job of sort of giving us an outline but I know she really wanted to talk about things that were over her head.
I also think that, and I mentioned this during the episode, you pull one lever over here and something else pops up over there and the trade-offs and the nuances of this system are quite complex.
So I appreciate that people are thinking very deeply about this and keeping us safe out there.
We'll be putting up some show notes and hopefully be doing more episodes soon.
We apologize for the long layoff, but hope you enjoyed it.
