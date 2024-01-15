---
title: "Address Relay"
transcript_by: kouloumos via tstbtc v1.0.0 --needs-review
media: https://podcasters.spotify.com/pod/show/chaincode/episodes/Martin-Zumsande-and-Address-Relay---Episode-20-e1if91d
tags: []
speakers: ['Martin Zumsande']
categories: ['podcast']
date: 2022-05-13
---
Speaker 0: 00:00:00

In Adromain you also have this distinction between the new and the tried tables.
So the new tables are for unverified addresses that someone just sent you and you don't know whether they are good, whether there's really a Bitcoin node behind them.
And the tried table is addresses that you've been connected to in the past.
So at some point, at least in the past, you know, they were your peers at some point.

Speaker 1: 00:00:19

Right.
And you also need to make sure that you get some fresh blood in there, so you don't get sequestered into some part of the network.
And then, I don't know, you go on vacation and your node was offline for a week and you come back and nobody's online anymore.
You need to constantly keep hearing about new nodes.
Hi, Jonas.

Speaker 2: 00:00:45

Hey, Murch.
Glad to get you back in the studio before you rush off to London.
And we're gonna be talking to Martin today, huh?

Speaker 1: 00:00:53

Yeah, yeah.
We heard a talk by him yesterday already, so we're kind of prepped.

Speaker 2: 00:00:57

That's better than usual, isn't it?

Speaker 1: 00:00:59

Yeah, yeah, We have a good idea what we'll be talking about already.
We did a few peer-to-peer topics already earlier with Amitie and Peter.
But I think we're going to look at different aspects of peer-to-peer this time.

Speaker 2: 00:01:12

Very good.
Well, Martin's been with us for a couple of weeks.
We finally dragged him in the studio and hope you enjoy the episode.
Welcome to the Chaincode Podcast, Martin.

Speaker 0: 00:01:32

Hi, thank you for having me here.

Speaker 2: 00:01:34

Absolutely.
It's great to have you in the office these last couple of weeks.

## His background

Speaker 2: 00:01:37

So today we want to hear a little bit more about your background, sort of how you got to working on Bitcoin Core, and then some of the things you're working on.
So tell us, where do you come from?

Speaker 0: 00:01:48

Yeah, I'm originally from Germany, and I'm a physicist.
I did my diploma and PhD in physics.

Speaker 2: 00:01:56

And what specifically in physics?
Physics is pretty broad.

Speaker 0: 00:01:58

Yeah, I was doing statistical mechanics for my diploma thesis, like doing mostly simulations already, so a lot of computational work.
And then for my PhD, I worked in the field of systems biology, which is like a mix of physics, math, and biology.
So somehow I tried to apply some physical techniques on problems from biology such as bone remodeling or some signal pathways in the cells.
So that's what I did.
But that's been a long time ago I left science to work in the industry and I worked as a consultant for banks until I found about Bitcoin.

Speaker 2: 00:02:38

Well, having a physicist who's now spent some time at banks, I can see the progression to something like Bitcoin.

## Getting interested in Bitcoin

Speaker 2: 00:02:45

How did you follow up on Bitcoin Core and how did you start working on it?

Speaker 0: 00:02:49

Well, I got interested in this space at first, not so much technical, but trying to understand how Bitcoin works.
There was an essay I read that I liked very much and made me feel like I understood Bitcoin better, which was by also a physicist, I think, Michael Nielsen.
He had a blog post there.
And that was the first time I thought I really understood Bitcoin on a certain level, of course, and went deeper into it.
I wanted to really understand how it works at a lower level, at the lowest level, the level of code.
And I got interested in Bitcoin Core and started contributing the small thing first.
Also, I still had a job at the same time, so I couldn't do this full-time.
So I picked some smaller project, reviewed some PR, participated in the review club, which was great, which also started at the same time when I got interested in Bitcoin, and yeah, here I am.

Speaker 2: 00:03:40

Very good.
I think Waxwing is a physicist, isn't he?
Is Waxwing a physicist?

Speaker 1: 00:03:45

He's a mathematician, I think.

Speaker 2: 00:03:46

Oh, okay, Well.

Speaker 1: 00:03:47

I think he used to be a math teacher.

Speaker 2: 00:03:50

Cool.
Well, we'll edit that part out.
I was wrong about that.

## How to approach P2P

Speaker 2: 00:03:55

So you seem to spend more of your time at Bitcoin Core lately in the P2P area.
So tell us why that area and what's interesting you there.

Speaker 0: 00:04:07

I think I've been interested mostly in P2P from the start.
It's just that I have more time now to work on these problems.
It is the field that interests me most, And mostly because I think it's not only about the code, I'm gonna say in the code, but about the network, like how all these different agents run their own code, some different versions of Bitcoin Core, some other implementations, whatever, they all work together.
And on a systems level, some behavior comes into play that is larger than just the parts.
So it all works together, and it needs to be secured.
There are several ways one could attack Bitcoin Core or the Bitcoin network and making sure that this works well when everyone plays nice together and it's also resistance against attacks.
That is something that I find really interesting.

Speaker 1: 00:04:59

Yeah, I think One of the interesting things is that the credo is never to trust another node for what they tell you, because they might be lying.
So on the one hand, you have to make it work locally and you have to have an emergent behavior across the whole set of participants that is not wasteful, but still gets everybody all the information they need.
I can see the appeal.

Speaker 2: 00:05:26

How do you approach the different trade-offs?
Because when we talked to, We've had Peter on the podcast talking about P2P.
We've had a media on the podcast talking about P2P.
It's seemed very nuanced.
How do you think about those trade-offs and understanding when you pull this lever, something else pops up over there?
And also the history and the context of P2P, because some of it in some cases came out of Peter's head, some of it is deliberate.
There still seems to be some DOS vectors in there.
So how do you think about all that?

Speaker 0: 00:05:57

Well, I think the one thing is to try to really read the code and not read it once, but read it many times and try to find new nuances.
Why is that that way?
If you find something that interests you, and one of the things that you should do if there is something that you don't really understand, but then often you have the urge to say, I'm sure someone has thought about it and I'll maybe think of it another time and let's concentrate on something else for now.
And I think these exactly are the points where most people do the same and where it's interesting to look deeper and really answer the questions you have yourself and until you know or are sure you have a solution.
And sometimes, yeah, you found something that some people haven't thought of before.
And then you maybe create PR to fix this.
And yeah.

Speaker 1: 00:06:42

So you're saying Bitcoin developers are like peer-to-peer nodes.
They don't trust what other people have done?

Speaker 0: 00:06:48

Yeah, I mean you should never really trust the code that it works.
I mean it's not necessarily that someone has written bad code on purpose, but maybe something that used to work once stopped working because of something that was done in another part of the code base and there are many ways that things could go wrong.
And so I think it's always best to check for yourself how the code works and that way you also find ideas of things to change.
I think it's sometimes it's good just to read code and try to make sure you really understand it well.
And that's where you find ideas for ways to improve the code by yourself.
Sometimes better than going into a code section like with the purpose.
I'm going to change this now, because this might lead to changes that are not So great.

## The network is changing

Speaker 1: 00:07:31

Yeah, this actually reminds me of one of the topics that came up at BitDevs this week, where we talked about Jameson Lobs' observation that the network appears to get slower because more and more of the nodes are on home connections and core connections.
So there's fewer slots on IPv4 available for other participants.
So these magic values that were picked, how many peers people or nodes have, might not scale to everybody being on a broadband connection at home.
So it's not only that the code and all the Bitcoin core node around it changes, but also the reality of the network changes.
So it's sort of multivariable emergent behavior.

Speaker 2: 00:08:15

Yeah, it will continue to emerge because we continue to try to encourage people running their nodes on Raspberry Pis in remote locations.
And what may be good for decentralization may not be so great for bootstrapping and initial block download and things like that.

Speaker 0: 00:08:29

Yeah, and some things just happen because people choose different ways to participate in the Bitcoin network.
For example, I just recently was really surprised to see that there are like so many nodes using Tor right now.
So I think there are even if you look at some statistics website, there are bit nodes, there are even more peers in the network that are using Tor than that are using IPv4.
So

Speaker 1: 00:08:51

reachable nodes.

Speaker 0: 00:08:52

Reachable nodes.
And that is something like a very new development.
I don't think it was like this three or four years ago.

Speaker 2: 00:08:57

I feel like that's the Umbral effect.

Speaker 1: 00:09:00

Yeah, Raspi, Blitz and Umbral and a few other of those home node packages are configured to automatically only connect to Tor.
I think it's part of it is that it is not trivial to puncture NAT, local area network and open up the ports.
And if you have a Tor connection, you basically do that automatically.
You are configured to receive from outside.
So I think that might have something to do with it.
And also that people that run Lightning nodes, especially don't want to reveal their IP address.

Speaker 0: 00:09:31

Because It

Speaker 1: 00:09:32

sort of is a hot wallet.

## What's the purpose of the Address Manager (AddrMan)?

Speaker 1: 00:09:33

So Adderman, what's the goal of the address manager?

Speaker 0: 00:09:36

The goal of the address manager, I would say, is to have a good variety of peers to find to connect to.
So you don't want to have all your peers be from the same IP range.
Or you want to have a good variety there.
You also only have a limited amount of addresses you can save.
You don't want to have a system where it can overwhelm you like write up your disk.
So you also need to have like a limited amount.
So you have like a restricted number of addresses that fit there.
And in Adromain you also have this distinction between the new and the tried tables.
So the new tables are for unverified addresses that someone just sent you and you don't know whether they are good, whether there's really a Bitcoin node behind them.
And the tried table is addresses that you've been connected to in the past.
So at some point, at least in the past, you know, they were valid peers and they were your peers at some point.

Speaker 1: 00:10:25

Right.
And you also need to make sure that you get some fresh blood in there.
So you don't get sequestered into some part of the network and then, I don't know, you go on vacation and your node was offline for a week and you come back and nobody's online anymore or things like that.
So you need to constantly keep hearing about new nodes.

Speaker 0: 00:10:43

Yes, and that means that old nodes will be overwritten at some point.
If you haven't heard from them for a long time, they will be like new nodes that have a higher probability of actually being there on the network still.
They will get a preference and the old one might be replaced by them.

## Peering differences to LN nodes

Speaker 2: 00:11:00

I think there's a big difference between something like this and the Lightning Network is that these ephemeral connections between Bitcoin nodes.
I was surprised when I first booted up a node to watch those connections turnover and find them in your logs, as opposed to Lightning, which is much more like you want to establish yourself as a good member of the community and consistent.
And like, unless you're going on chain, those are pretty permanent connections.

Speaker 1: 00:11:21

Right.
Especially since you want to talk about a channel you have with them, you would be permanently peering with those.
But with Bitcoin peers, it's, it's very exchangeable.
You just need somebody that talks to you, right?
So on the one hand, you do want some persistence because you don't want to give an opportunity to an attacker to completely replace all your peers and eclipse you.
But on the other hand, you do want some mixed fruit.
So you keep being well connected to the whole Bitcoin network.

Speaker 0: 00:11:48

And there is one important thing that is different from the Lightning Network in Bitcoin.
You don't want to be the network public.
So you don't want your peers or anyone else to know which nodes you are currently connected to.
Right.
That is something that is, I think in Lightning Network, it's being published, but at least for the public nodes and in Bitcoin Core, this is something that nobody should be able to get this information out of you.

## Ethan Heilman's talk on Network Partitioning Attacks

Speaker 2: 00:12:10

Yeah, I think one of the clearest explanations of the trade-offs here was Ethan Heilman give a talk at the residency and there's a video, we can put that in the show notes, where he talks about just sort of like, I mean, it's really in the context of Eclipse attacks, but he really dives into the new and tried table and the different considerations there.

## Addrman and eclipse attacks

Speaker 2: 00:12:27

And then there's a wiki page on the DevWiki that goes into how that's evolved over the last seven years since that paper came out, seven years?
So anyway, if you're interested in more reading, there's stuff there.

Speaker 0: 00:12:38

Yeah, it's a great article.

Speaker 2: 00:12:39

So we did a couple episodes with Amiti 15 and 16, that was in October.
And then Peter joined for that for episode 16.
We covered a little bit of AdderMan and AdderRelay.
But those are some areas that you're also spending some time into.
So why those areas of the code?

## AddrRelay and the role of node addresses

Speaker 2: 00:12:55

What is interesting there?
And yeah, and why spend so much time?

Speaker 0: 00:12:59

Yeah, I mean, I'm very interested in AdderRelay.
It's different than the other types of relay like blocks where you need proof of work, transactions where you spend some Bitcoin, whereas for an address to relay you don't really have to do any kind of work to relay it.
But we still need those.
Nodes need addresses to find other nodes to connect to.
So it's on the one hand, it's easy to spam the network with addresses.
On the other hand, it's important that Address Realize still works as good as possible so that nodes have a good variety of peers to connect to, that they can find peers quickly and to get all of these different goals and make them work together.
And that is something I find really challenging and interesting.

## Getting connected to the network

Speaker 1: 00:13:38

So maybe we can briefly give an overview of how nodes get addresses in the first place.
If you start with a fresh node, how do you get connected to the network and how do you hear more about other peers in the network after?

Speaker 0: 00:13:51

Yeah, there are different ways of getting addresses.
Like for a new node in the network, they would query the DNS seeds.
Those are like centralized seeds that are run by Bitconners and they will give you a small number of addresses that will help you bootstrap.
They are not meant to be a source of addresses forever but ideally just once when you are new to the network they will give you something to start with and then you build up your own address database and use that in the future.
But for that to be possible you need more ways of relaying addresses to the network and there are two ways I would say.

## Self-announcements

Speaker 0: 00:14:24

One of them is the address gossip relay.
So basically once a day a node will self advertise its address to the network, send it to its peers, and those peers will take it, pick it up, and add it to their address database, but also will relay it a bit further to some of their peers, usually two, sometimes between one or two.
And this helps an address propagate over the network, But there's like a certain system for this, some algorithm in place that makes it sure that it doesn't go on forever.
We don't want to spend the network with a given address.
So this will only work for like 10 minutes or so.
And after that it will stop.
And maybe on the next day we try again, But yeah, that is the gossip relay.
And that is how nodes self-advertisements relate to the network.

## Address spam in summer 2021 and peer distribution

Speaker 2: 00:15:06

So we've seen even within the last year, people try to mess with that.
I know that Peter and Amiti will be feeling over this in their episode, but what did you observe and how are we addressing that going forward?

Speaker 0: 00:15:16

Yeah, actually, that was in last summer, There was suddenly a huge spike in the traffic of addresses being relayed and it was really interesting to see this unravel in real time.
It was some kind of attacker who would use a botnet to spam the network with addresses that were not its own, They were just randomly generated IPv4 addresses.
They had a number of nodes that did that.
They connected to random peers, send them like 5,000 addresses, and disconnected, and did that again to some other peers.
And there were like maybe 30, 40 peers doing this at the same time.
And this was going on for quite a long time, like for two months or so.

Speaker 2: 00:15:49

And what's your theory?
Research, harming the network, what's the motivation?

Speaker 0: 00:15:54

Yeah, I can only speculate because I think it is not known.

Speaker 2: 00:15:58

Could have been you.
You don't have to speculate.
It could have been you.
Yeah.
You seem to know a lot about it.

Speaker 0: 00:16:03

Yeah.
There are different theories.
I mean, the attacker, they might have had the intention to attack the network, to just, they might have had the intention to do harm to the network, make it impossible for new nodes to find peers.
But that's just one theory.
And it's also possible that these were researchers that were people who wanted to analyze the topology of the network because they did this in a very special way.
They didn't send huge chunks of addresses that would only reach the victim that would receive them and the victim wouldn't propagate them any further.
What they did was they split these up into very small packages with up to 10 addresses and they sent a lot of these small packages.
So what this did was this made use of the address propagation algorithm in Bitcoin Core because Bitcoin Core, when it would receive up to 10 addresses in a package, they would distribute them to the peers and send them further along.
So the attackers, they might have had the intention to use this in order to find out how many peers their victim was connected to.
So you can do this.
I mean, you need one attacker node that sends the addresses and you need one detection node that would also connect to the victim and just see how many addresses get relayed to this node.
And you can do the math there and you can figure out this node, our victim node has 100 connections or something.

Speaker 1: 00:17:20

You talked about this yesterday to us already, so I understand I think how it works now.
Every time a node receives an announcement of addresses with up to 10 addresses, For each address separately, they'll randomly pick two peers to forward it to.
So if you send say 500 packages of 10 addresses and a node has a hundred peers, they'll randomly decide for each of those 5,000 addresses which two peers to relay that to.
So now if there's another peer connected to the attack node, this receiver or observer node would probably get some 50 addresses.

## Correction: The peer would not get addresses-divided-by-peers addresses, but 2×addresses-divided-by-peers addresses as the addresses get forwarded to two peers each.

Speaker 1: 00:17:59

If there were only 10 peers connected to the attack node, they'll receive 500.
So the observer will basically get n divided by a number of peers of these randomly generated addresses forwarded.
And that way, while an attacker could measure the peer degree of the node, right?

Speaker 0: 00:18:16

Yes.
The thing that is, it's called in network science, I think it's called degree distribution, which says like how many peers have how many other peers that they are connected to and to make a distribution out of that.
And that is an important measurement to show about the topology of a network and that different ways that peer distributions can be.
And there could be a power law, there could be like very random, like very evenly distributed.
And maybe the attacker just wanted to know how it is for the Bitcoin and peer distributions.

Speaker 2: 00:18:45

Yeah, that's interesting.
I mean, I'm trying to think of the value of that.
One, we mostly see them in Lightning.
You see the Lightning network visualized and sort of cool, and you can understand the interconnectivity and you can see how it grows.
There's also the idea of, there's got to be heuristics associated with nodes that are configuring their peers and not using the defaults.
And so a node that has a thousand connections is some sort of flag as to what it might be.
It might be a spy, it might be a miner, it might be just, there's a reason that it would have more connections.
So I don't know, I'm just sort of thinking about why someone would do this.

Speaker 1: 00:19:18

It could be a fingerprinting.

Speaker 2: 00:19:18

We haven't seen a paper come out yet associated with it, as far as I can tell.

Speaker 0: 00:19:21

I mean, actually, there is a paper, not by the attacker, but by a team in Karlsruhe.
They are a team of researchers there.

## Estimating the Node Degree of Public Peers and Detecting Sybil Peers Based on Address Messages in the Bitcoin P2P Network by Matthias Grundmann

Speaker 0: 00:19:27

And they actually have a note that monitors the whole network and probably put the link there in the show notes.
They also published a paper on archive about this and they were actually in a position because they are connected to most nodes to calculate the degree distributions.
And this is something I think I find really interesting because this is something really positive that can come out of this because the redistribution, it doesn't really reveal privacy because it doesn't say who is connected to who, but it does give a good estimate how the network looks like.
And this is something that Bitcoin developers or researchers can use in simulations of the network, because if we understand how the networks behave, it's much more easier to simulate the dynamics on it in some agent-based model, for example.
And so I think this is something, I don't know if the attacker wanted to know this, but it's definitely something that the Bitcoin research community can make use of.

## Simulating the network

Speaker 2: 00:20:15

I want to hear a little bit more about simulations.
And you've done some simulations for Adderley, but you also have a prior history of science and simulations.
And I'd love to hear sort of how you think about creating simulations and using that past experience.
Is there any crossover to creating simulations for Adderley?
Yeah.
How do you go about it?

Speaker 0: 00:20:33

Yeah, I think there's definitely, I've done a lot of simulations in the past, but it's something I would want to pursue much deeper in the future, because I think for a lot of decision, if we want to change some things, for example, in address relay, change a little thing there, we can say that makes sense locally.
We can understand why it should be good, but we are not really sure what this will do for the network.

Speaker 2: 00:20:54

I mean, there's lots of things.
There's early, there's transaction rebroadcast, there's, you know, the list goes on and on.
It goes back to my original question of how you think about when you pull a lever and something pops up over there.
If you're changing how the network interacts, those variables can cause unintended consequences.
So having simulations to go along with the code review obviously gives you more confidence.

Speaker 0: 00:21:15

Exactly.
And I think it would be great if there was some agreed upon or like widely used simulation framework so that each time I want to simulate something that interests me, like that I know about it, I wouldn't need to worry about creating a realistic degree distribution.
So it would be good to have that out of the box.
Just take one of the realistic scenarios and see how this affects the simulation.

Speaker 2: 00:21:37

Yeah, I know that, you know, Suhas has his simulator.
Gleb has his simulator.
The Carnegie Mellon team.

Speaker 0: 00:21:43

Yes.

Speaker 2: 00:21:43

Obviously, there could be some shared nodes there.

## Requesting addresses from peers

Speaker 2: 00:21:46

So there's a third way that nodes on the network learn about addresses.
And what's that third way?

Speaker 0: 00:21:52

That way is the get other message.
So when a node makes an outgoing connection, not for inbound, just for outgoing ones, we ask them, we send this get other message to them once, and then they will answer this with a huge chunk of addresses, up to a thousand addresses.
And those addresses, they randomly pick from the other man.
And yeah, so that gives, they are not filtered for recency or something.
So they might be a bit older.
They might be, they're also being cached right now.
So with the get utter message, we would only send out one set of thousand addresses to our peers within 24 hours.
So they are something, yeah, a little bit more long living ones.

Speaker 2: 00:22:32

But there's a grab bag there.
You have maybe some junk in there, maybe some stuff that's in the tried table, and maybe some actual connections that the node would be paired with, right?

Speaker 0: 00:22:42

Yeah, but there is not really a selection for this.
We just get random addresses that we just would send away.
In a getAddress response, we would just send random addresses.

Speaker 2: 00:22:53

Do you think it should be preselected?
Yeah, I think it would

Speaker 0: 00:22:55

make sense, because for example, in many nodes, they would have a lot more addresses in the new table than in the tried table.
So that would mean that we're also like in a get other message, we would have a larger percentage of notes on a new table.
And the new tables, they are not really filter for quality.
So I think it might make sense to think about like including a certain percentage of addresses from the try table that we know are quality and are good, and are actually a piece on the Bitcoin Core network, and include them in a get-out-of-response network.

Speaker 2: 00:23:28

And what circumstances would you actually ask for these messages?
So you have the bootstrapping mechanism through DNS seeds, and you have the gossip.
And so it's sort of like that in-between state of, I know about a few, and I'm going to do some connections, and I'll go ask for some samples.
Is that sort of the best?
Is that the best use of...

Speaker 0: 00:23:46

I'd say it's currently being done just once.
When you start a new connection to outbound peer, you just ask them once for this big chunk at the beginning of the connection.
And then never again while the connection lasts.

Speaker 1: 00:24:00

So if you were to restart and reconnect to the same outbound peer again, you would ask again.

Speaker 0: 00:24:06

Yes, but if you do this within 24 hours, you would get the same response because we don't want to be able to make use of this to scrape our Adorama database to be able to see all the nodes that are in there.

Speaker 1: 00:24:20

So and obviously, since we don't trust any of our peers, we're very paranoid.
We add that only to our new table, right?
So we get a big chunk of a thousand new addresses from each outbound connection, add that to our new table.
And if we ever need later some more outbound connections, or with our feeler connection every two minutes, we would try some of the new tables and potentially move them to tried.

Speaker 0: 00:24:44

Exactly.
The distinction between new and tried it makes a lot of sense because whenever we would make an outbound connection we would toss a coin and with a probability of 50% we would pick one address from the new table, just one, whatever it is, or we would pick one from the tried table.
So if our new table was overwhelmed by spam or something, we would still have a 50% chance for each try to pick one from the try table, which is probably not affected by this.
So even if for some reason our new table was junk, we would still have a way to find peers in a reasonable amount of time.
Well, if we have some errors in the try table, if we don't have done we are out of luck.

## Walking through first connection of a node

Speaker 1: 00:25:25

So if you're a completely new node, you would connect to a DNS seed.
How much do you get from a DNS seed?
Is that like just a few connections or is that a thousand?

Speaker 0: 00:25:35

It's just a few.
I think it was reduced at some point in the past recently, but it's under 50 I think.

Speaker 1: 00:25:41

Okay, so I'm a new node, I connect to a DNS seed, I get under 50 addresses from a DNS and they are basically tried addresses.
Right.
And not new addresses.

Speaker 0: 00:25:51

They are tried for the DNS.
So the DNS is internally.
They have a crawler which tries to connect to Bitcoin core nodes and will only give those that actually exist on the network.

Speaker 1: 00:26:03

So we're a little less paranoid towards DNS seeds.
But that's kind of makes sense because we're completely new here and we don't know that we can trust.

Speaker 0: 00:26:10

But we still store these in the new table, in our new table.
So we don't just believe the DNS seed, if they are good, we just put them to tried.

Speaker 1: 00:26:18

And then of course, the node would make eight outbound connections to blocks only connections and a feeler connection would start going through the remaining new and then each outbound connection would give us 1000 new addresses again.
And so very quickly, we would build up some stock of new addresses in our new table.

Speaker 0: 00:26:35

Yes and all the let's say 10 nodes that we connected to when we disconnect them we would also like promote them to the try table because now we have been able to connect to them.

Speaker 1: 00:26:46

Right Although we do not get any new addresses from blocks-only relay connections, right?

Speaker 0: 00:26:51

Right, but I think the block-only connections themselves that we connect to, their address will still be promoted to Trite.

Speaker 1: 00:26:59

Yeah, makes sense.

Speaker 2: 00:27:00

Yeah, I mean, as I listen to this and as I'm sort of catching up on my reading, it just seems so nuanced.

## Coinscope paper

Speaker 2: 00:27:06

Like, getAdder messages were taken advantage of by, in the Coinscope paper, where they used specific timestamps that were proliferated through the network to understand network topology.
And then Gleb added the cached responses, because otherwise you could scrape the Scrape Adderman if you just kept querying.
So it's

Speaker 1: 00:27:24

like- I seem to remember that there was something that made sure that you never share more than 30% or

Speaker 2: 00:27:29

23%- 23%, yes.

Speaker 1: 00:27:32

23% of your address.

Speaker 2: 00:27:34

And Peter doesn't claim full responsibility for that, but I'm sure we can look up the code.

Speaker 0: 00:27:38

I think it was introduced by Peter.
Maybe he found it from somewhere else.

Speaker 2: 00:27:42

That's right.

Speaker 1: 00:27:44

Illuminati.
Cool.
Hopefully that gets cut.

## Being a Bitcoin Core contributor

Speaker 1: 00:27:50

All right.

Speaker 2: 00:27:50

I want to talk a little bit about just what it's like to be a Bitcoin Core contributor and sort of how you think about spending your time, what kind of code review you pick up, how you look for ways to contribute.

Speaker 0: 00:28:02

Yeah, I think there are many different ways of being a Bitcoin Core contributor.
And I think every person has to find a way that works best for them and for their interests.
But what I personally like is I don't want to spend all of my time on projects like the Multi Index Adderman and I want to spend a lot of time on review, reviewing other things because that's the way you learn especially if you're a relatively new contributor.
I think that is important to not get lost in some like esoteric area and spend all your time there, but also get to know other parts of Bitcoin Core better.
And something that I personally really like is just look at the list of issues.
Maybe there's some intermittent failure in some functional tests and just try to see what has happened, try to find a fix, make a small PR there.
And yeah, this can take some time, but it's usually not a huge project.
You can do this like one evening maybe, and yeah, you fix some small bug there.
And that is something I really like.
And you also learned something about some part of the code base that was not familiar to you before.

Speaker 2: 00:29:08

What's the difference between doing this on nights and weekends and having the opportunity to do this full time and making this your regular job?
Like, How does it change your approach or how do you pace yourself?
Or I mean, you're a few months in, so what has that transition been like?

Speaker 0: 00:29:22

Yeah, I think for me personally, before I didn't really have the energy to do large projects because I was just doing this on the side.
So I just did a small review there and a small PR there, like changing smaller things.
Now that I have more time, I'm concentrating on larger things like multi-index project is one of them, but I would also try to review larger PR and more complicated PRs. So recently I've become interested in the indexes and there's a large PR by Russ and I'm currently trying to review that, which is, it takes a lot of time because it's a large change.
And yeah, I want to spend more time on more complicated changes.
We have an

Speaker 2: 00:30:02

Ack Russ t-shirt we have to get in your hands then.
I don't know if we have your size, but cool.
Thank you for sitting down with us and telling us about your days on Bitcoin.

Speaker 0: 00:30:10

Yeah, it was great.
Thank you very much.

Speaker 2: 00:30:25

So, any takeaways from our conversation?

Speaker 1: 00:30:28

I thought that the Adderman spam was really interesting.
The spam attack that was trying to either leverage the exact behavior of Bitcoin Core on what it will relay to learn the node peering distribution, but maybe also just didn't know exactly what was gonna happen and then didn't get all their addresses relayed as wanted.
Right.
That was an interesting thing there.

Speaker 2: 00:30:53

It must have been a government op.
Didn't read the code close enough.

Speaker 1: 00:30:58

I don't know.
And I just find it fascinating how much a little change at the local level changes the global emergent behavior.

Speaker 2: 00:31:06

Yeah, which is why we have our best physicist on the case.
Something happens over here and something else happens over there.

Speaker 1: 00:31:12

So quantum entanglement.

Speaker 2: 00:31:13

That's right.
Yeah, it was great to have Martin in the office these last couple of weeks and yeah, I really enjoyed the conversation with him.
He's a really approachable guy and I mean, he's been working sort of moonlighting on Bitcoin now for a couple years, but really excited to see him working full-time with a grant through Rink.
So very good.
We'll try to get this out soon and get into the studio again probably in the next couple weeks.
