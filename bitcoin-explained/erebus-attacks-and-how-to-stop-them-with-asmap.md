---
title: Erebus Attacks And How To Stop Them With ASMAP
transcript_by: adamjonas via review.btctranscripts.com
media: https://www.youtube.com/watch?v=I2ZmAPI3ebQ
tags:
  - security-enhancements
  - security-problems
speakers:
  - Sjors Provoost
  - Aaron van Wirdum
date: 2020-11-19
episode: 18
aliases:
  - /bitcoin-magazine/bitcoin-explained/erebus-attacks-and-how-to-stop-them-with-asmap
---
Aaron van Wirdum: 00:00:07

Live from Utrecht, this is The Van Wirdum Sjorsnado.

Sjors Provoost: 00:00:10

Hello!

Aaron van Wirdum: 00:00:10

Hey Sjors. What's up? We got a market cap all time high, did you celebrate?

Sjors Provoost: 00:00:14

No, I did not because it's just dilution.

Aaron van Wirdum: 00:00:16

What do you mean?

Sjors Provoost: 00:00:17

I mean somebody's making more Bitcoin. So it's fun that the market cap goes up, but it doesn't matter unless you...

Aaron van Wirdum: 00:00:23

It doesn't benefit you personally. That's the only thing you're concerned about.

Sjors Provoost: 00:00:27

Exactly. I'm very selfish.

Aaron van Wirdum: 00:00:28

Got it. Sjors, we're making a follow-up episode this time.

Sjors Provoost: 00:00:31

That's right.

Aaron van Wirdum: 00:00:32

I think this is our first follow-up episode? It's very possible.

Sjors Provoost: 00:00:35

Possibly. But everything is connected.

Aaron van Wirdum: 00:00:38

Very true. Last week we discussed eclipse attacks and this week we're going to discuss another type of eclipse attack. Yeah. Last week we discussed a paper by Ethan Heilman et al and this week we're discussing a paper by...

Sjors Provoost: 00:00:53

people whose name I unfortunately cannot pronounce but from the University of Singapore, from Korea University and from the Japan Advanced Institute of Science and Technology. It was published quite a few years later than the previous paper.

Aaron van Wirdum: 00:01:05

Yes, and what's the paper? What's the name of the paper? What's it called? What are we discussing exactly?

Sjors Provoost: 00:01:09

We are discussing the Erebus attack... I have no idea how to pronounce it.

Aaron van Wirdum: 00:01:15

Let's recap Eclipse attacks very briefly. Yeah. You go for it.

Sjors Provoost: 00:01:20

So, if you're a node and you think you're talking to the rest of the Bitcoin network may actually be just a single entity that is pretending to be all the other nodes that you're talking to and so that node is eclipsing your view of the Bitcoin network.

Aaron van Wirdum: 00:01:32

Yeah, so that node could potentially shield transactions or blocks from you, maybe even create fake blocks or blocks that are not included in the longest blockchain.

Sjors Provoost: 00:01:43

Exactly. Not fake blocks, but definitely blocks that are not in the longest chain. So you might think you've seen something confirmed and then suddenly there's a reorg that you didn't know about.

Aaron van Wirdum: 00:01:52

That's fake in my book, Sjors.

Sjors Provoost: 00:01:54

Well, fake could...

Aaron van Wirdum: 00:01:55

be false...

Sjors Provoost: 00:01:56

...signatures and because you're still checking all the proof of work and all the rules.

Aaron van Wirdum: 00:02:00

In my book, it's fake, Sjors.

Sjors Provoost: 00:02:01

Okay, are Bitcoin Cash Blocks are real?

Aaron van Wirdum: 00:02:05

These are very fake.

Sjors Provoost: 00:02:06

Okay.

Aaron van Wirdum: 00:02:07

So one of the solutions, for those who want more details, just listen to our previous episode, the one we did last week. One of the solutions we discussed are like IP buckets, where you categorize other nodes in different buckets with IPs that suggest they are behind different ISPs.

Sjors Provoost: 00:02:26

Right, right. That's been in there from the beginning, these IP buckets, but that is one of the general defenses against Eclipse attacks. So you look at the four digit, four number IP address, and you look at the first two numbers and usually you assume that's going to be different internet providers. So if you have some diversity there, that's good. And there's a bunch of other things that were done to make the original attacks more difficult.

Aaron van Wirdum: 00:02:46

Right. So, but this paper, the one we're discussing this week, actually introduced, proposed, I don't know what the right word is to use here.

Sjors Provoost: 00:02:55

Revealed.

Aaron van Wirdum: 00:02:56

Revealed a new type of Eclipse attack.

Sjors Provoost: 00:02:59

That's right. So basically one where you can fake a lot of those initial IP addresses rather than just one or two.

Aaron van Wirdum: 00:03:08

Right. I think you described it as with this Eclipse attack because it is take two. You already described it in other words. You said this is like faking the internet...

Sjors Provoost: 00:03:17

...it's like faking the internet or it's faking part of the internet

Aaron van Wirdum: 00:03:20

...you're faking part of the internet for one specific node yes let's just what is the internet

Sjors Provoost: 00:03:26

what is the internet...

Aaron van Wirdum: 00:03:28

think to understand this attack we need to understand the internet

Sjors Provoost: 00:03:31

it's a group of computers it'll it has an amazing potential well basically

Aaron van Wirdum: 00:03:35

It's gonna be very big one day, maybe.

Sjors Provoost: 00:03:36

Yeah, the internet consists of building blocks and those are called autonomous systems. An autonomous system could be an internet provider, it could be Google. Usually it's one legal entity and it owns a whole bunch of IP addresses. And when you send something from one place on the internet to another place of the internet, the package goes from one autonomous system to the next autonomous system to the next autonomous system, from your provider to Google to some other place on the internet.

Aaron van Wirdum: 00:04:04

Right. So, if I am a node and I want to connect to a diverse part of the internet, I want to connect to nodes on diverse areas of the internet. Yes. Then surely if I connect to nodes in different autonomous systems, then all my problems are solved.

Sjors Provoost: 00:04:25

Well, that would definitely be a big improvement over just connecting to different IP prefixes, Right? Because Amazon has a lot of them, but you're not really there yet. And that's what the faking the internet comes in. Because when your package goes from your autonomous system to the next autonomous system to the next one, you don't know what's happening after the first step. So the first autonomous system in line can actually fake everything behind it. Right.

Aaron van Wirdum: 00:04:52

So one autonomous system could be like a bottleneck for a whole part of the internet behind it.

Sjors Provoost: 00:05:00

Correct.

Aaron van Wirdum: 00:05:01

Can you give an example of this?

Sjors Provoost: 00:05:02

Yeah, so if we look at it geographically, it's a slight oversimplification, but if you're in Europe and you want to connect to New Zealand, then it's going to go through Australia. And so Australia can basically fake anything going to and coming from New Zealand. Not entirely true because I think there's another cable, but let's pretend there isn't.

Aaron van Wirdum: 00:05:20

Yeah, we're simplifying a bit. So there are bottlenecks and...

Sjors Provoost: 00:05:24

We could say Indonesia could be faking everything that's happening in Australia and New Zealand.

Aaron van Wirdum: 00:05:28

Yeah, so let's say For example, that I am a node, I'm still a node, and I want to connect to diverse parts of the internet. So I'm going to pick Indonesia and Australia and New Zealand because they're very different parts of the internet. But then actually...

Sjors Provoost: 00:05:46

Actually, it might only be connected to some evil person in Indonesia that's fooling you.

Aaron van Wirdum: 00:05:51

That's acting as a bottleneck for the other parts and that's faking the other parts. So then I'm still susceptible to an eclipse attack by the Indonesian guy.

Sjors Provoost: 00:06:01

Yes, well of course not some random Indonesian guy, it would have to be whoever is in control of the Indonesian internet.

Aaron van Wirdum: 00:06:07

Which in Indonesia is probably some random guy.

Sjors Provoost: 00:06:10

It's very possible.

Aaron van Wirdum: 00:06:11

I may be insulting our Indonesian listeners now.

Sjors Provoost: 00:06:15

It's also important to understand that the internet isn't very geographical in that sense. So, for example, there is a cable company in the Netherlands called Ziggo. And if you look at how the internet is constructed from there, the Netherlands Ziggo and the UK Ziggo and the Austrian Ziggo are all behind the same thing called Aorta. Whereas the Dutch KPN is not. So in a sense Dutch and English and Austrian Ziggo customers are less diverse than Dutch and Dutch KPN and Ziggo customers that might be living right next to each other.

Aaron van Wirdum: 00:06:52

Right, interesting. So anyways, I'm a node, I think I'm being smart, I'm connecting to different parts of the internet, different autonomous systems, but actually I can still be tricked. Yeah. Sjorss, how can we possibly know where all of these bottlenecks are?

Sjors Provoost: 00:07:07

Well, first of all, I think we should recap a little bit that how this attack would work, because just faking it is not enough. You need to do the same thing as we explained in the previous episode. So you need to make sure that the person, the node you're attacking, is only going to connect to parts of the internet that are behind you. But the nice thing is that, rather than only giving it your IP address and IP addresses you control, you can give that victim node IP addresses from all over the world. So a much more diverse seeming range of IP addresses.

Aaron van Wirdum: 00:07:37

But the...

Sjors Provoost: 00:07:37

...rest of the attack works the same. You spam them, you wait for them to connect only to you, or to things that are behind you, and then maybe you reset them, if you can get them to crash, or you just wait.

Aaron van Wirdum: 00:07:49

Yeah, we took all of these precautions that we described last week, but then now our smart random Indonesian guy, attacker, he's aware of all of these solutions, So he can still trick us.

Sjors Provoost: 00:08:01

Yeah, because he can fake a much larger chunk of the internet this time. So then the question is that you ask is, what can we do about

Aaron van Wirdum: 00:08:07

it? Bottlenecks, where are they? How do we know?

Sjors Provoost: 00:08:09

Yeah, so the nice thing is there's no official map of the internet, but the internet is a very decentralized thing. Everybody kind of plugs in on their end of the world. But there are people who are trying to make these maps. And in particular, there's an organization called RIPE, or I-A-I-P-E, I don't know how they prefer to be pronounced. And they coordinate the internet in Europe, Middle East, and the former Soviet Union.

Aaron van Wirdum: 00:08:33

Who or what are they? Is it like a non-profit or how should I think about this?

Sjors Provoost: 00:08:38

I think there's some sort of unofficial internet owning non-profit. I mean, what do you mean by non-profit, right?

Aaron van Wirdum: 00:08:47

I don't know, I'm just asking questions because I have no idea what RIPE is.

Sjors Provoost: 00:08:52

Yeah, neither do I.

Aaron van Wirdum: 00:08:53

Okay, internet people. They're making the map for us.

Sjors Provoost: 00:08:56

Exactly. Well, so they do all sorts of useful things and one of the projects they do is making maps. So basically the way they do that is they have a bunch of very large autonomous systems that are sort of connecting to lots of lots of different providers... over the world and they ask them to basically ping everything on the internet and construct routing tables to that point. So they keep track of where the packages go and how they come back. And then they publish that. Basically, every month there's a giant file that you can download that says okay this is the way from me to this place this is the way from the for me to this other place and yeah everybody can download that and play with that

Aaron van Wirdum: 00:09:41

so it's like an unofficial road map for the internet which they're making

Sjors Provoost: 00:09:45

exactly

Aaron van Wirdum: 00:09:46

Which has got colorful lines and map of the world. Is that how I should see it?

Sjors Provoost: 00:09:51

Yeah, exactly. But it's not a complete map, right? It's just a map from those vantage points. So from like 20 different places, you can see thousands of other different places.

Aaron van Wirdum: 00:10:01

So like Europe and Eurasia is that what you mentioned?

Sjors Provoost: 00:10:04

Well again, it's not...

Aaron van Wirdum: 00:10:05

Or they're making it for the entire world? Yeah. What are the disadvantaged places? This organization

Sjors Provoost: 00:10:08

works for Europe and etc but they're doing this for the whole world so they're they are mapping from South America and from Australia and from Singapore and from the Netherlands and from all these places.

Aaron van Wirdum: 00:10:17

Right, so this is a big map. This is like a couple gigabytes.

Sjors Provoost: 00:10:20

Yes.

Aaron van Wirdum: 00:10:21

So you start your Bitcoin node and you download a couple gigabytes.

Sjors Provoost: 00:10:26

Right, because we like downloading gigabytes and then you process it. No, Thankfully there is another project actually can download this map for you called [AsmapRS](https://github.com/rrybarczyk/asmap-rs) by Gleb Naumenko and someone whose first name I don't know called Rybarczyk. And what they do is two things. One they download this map and the other is they process the map. Because now you have all these routes on the internet but the question you really want to ask is where are the shadows or where are the bottlenecks put a different way and so what it does is it looks at all the lines from A to B and it says okay if there's a line from A to B to C and there's a line from E to B to C then you say well all lines go to C they all go to B or in the example we gave before all routes to New Zealand all go through Indonesia. So what we're gonna do is we're gonna consider, we're gonna consider that as if it is Indonesia. So it's a way to compress the internet basically, just hide everything that's behind something else.

Aaron van Wirdum: 00:11:28

Right, yeah. So RIPE made this map and then Gleb Naumenko and Ms. Rybarczyk, they mapped out the bottlenecks, which is not four gigabytes, which is a much smaller file.

Sjors Provoost: 00:11:39

Yeah, I think they compressed it down to eight megabytes.

Aaron van Wirdum: 00:11:43

And do they update this frequently? Because you mentioned RIPE publish a new map every month or so is this also something that's being updated?

Sjors Provoost: 00:11:50

Well and even that's somewhat decentralized because RIPE is pointing to 10 different or I think 16 different organizations that are producing maps in the same format at whatever frequency they choose to.

Aaron van Wirdum: 00:12:02

I see. Some of

Sjors Provoost: 00:12:02

them do it every month, some of them haven't done it in 10 years.

Aaron van Wirdum: 00:12:05

Right, and are Gleb Nuenoko and Mr. Rybarczyk also updating their bottleneck?

Sjors Provoost: 00:12:10

No, they're doing nothing, because they published code that you can run.

Aaron van Wirdum: 00:12:13

Oh, I see. Yeah. Oh, they made software that maps out the bottlenecks. Exactly. I see.

Sjors Provoost: 00:12:18

It just downloads those files, whatever the most recent version is, and processes it.

Aaron van Wirdum: 00:12:22

Right.

Sjors Provoost: 00:12:23

And then there's another script written by Pieter Wuille, Sipa, and it takes that map and it compresses it down to one megabyte using some sort of bitmap magical compression.

Aaron van Wirdum: 00:12:35

Right, and that's included into Bitcoin Core?

Sjors Provoost: 00:12:39

Well, no. Bitcoin Core can use it, but it is not included. It's one of those things where Bitcoin Core makes an improvement, but doesn't completely finish it because they want people to try it out. So the idea is in the future to include it in Bitcoin Core if there are no objections and problems with it.

Aaron van Wirdum: 00:12:55

Okay wait so what's included now exactly?

Sjors Provoost: 00:12:57

Right now in Bitcoin Core it can use this file if you give it to it.

Aaron van Wirdum: 00:13:02

Okay, so you gotta separately use that software that Gleb Nomenko and Mr. Rybaczek wrote?

Sjors Provoost: 00:13:09

And the software that Sipa wrote? Yes, to download and process it. And it's just like two commands. But the idea is of course that eventually that'll be in Bitcoin Core, you don't have to do anything, it'll just work. But you can use that software to check that what is it, the thing that is in Bitcoin Core is not a lie. Because you don't want the Bitcoin Core developers to lie about what the internet looks like. So it's, you know, a problem is auditability. So can you, given those original files, reproduce the same thing? Can everybody reproduce the same thing?

Aaron van Wirdum: 00:13:36

Right. Okay, now we've done this, we've implemented this, we've included this in our version of Bitcoin Core.

Sjors Provoost: 00:13:43

Yep, and basically what that changes is the way the buckets are organized.

Aaron van Wirdum: 00:13:46

Okay.

Sjors Provoost: 00:13:47

So we talked about buckets, right? You look at an IP address and you take the first two numbers and you try to make sure the buckets all have different of these prefixes. And the only difference is now you do that with these autonomous systems, but not just with the autonomous systems but with the ones that we've said only Indonesia rather than we don't consider Indonesia, Australia and New Zealand separate we we only consider Indonesia we keep that diverse

Aaron van Wirdum: 00:14:12

so right

Sjors Provoost: 00:14:13

you have a diverse set of things that are not behind something else

Aaron van Wirdum: 00:14:16

yes so this makes even this evil Indonesian random genius unable to launch Eclipse attacks on us, because we're connecting to different parts of the internet behind different bottlenecks.

Sjors Provoost: 00:14:31

I would not say unable but it's at least it's another like pain.

Aaron van Wirdum: 00:14:35

We're making his life harder and harder.

Sjors Provoost: 00:14:37

Yes we are but we're not making it impossible and for that I think you would need an even more sophisticated map of the internet and like making sure that you're not your eight buckets are not still behind your eight connections are still not you know behind the same thing

Aaron van Wirdum: 00:14:53

right so what's this solution called

Sjors Provoost: 00:14:55

s map

Aaron van Wirdum: 00:14:55

and this was included in the last version of Bitcoin core

Sjors Provoost: 00:14:58

yeah the ability to use a map has been included in the last version and I guess in some future it'll just work.

Aaron van Wirdum: 00:15:03

And it's still a work in progress, it's being developed further and further.

Sjors Provoost: 00:15:07

I mean, you know, Sipa is very busy with Taproot and stuff, so I'm not sure about the progress, but yeah.

Aaron van Wirdum: 00:15:15

Sipa can work on several things at once. He can. And probably literally at once, I mean with like several laptops and doing it all.

Sjors Provoost: 00:15:23

And his clones. Yes. Exactly. But everybody can contribute on that stuff, right? And we're contributing by explaining it.

Aaron van Wirdum: 00:15:30

That's being generous, sure.

Sjors Provoost: 00:15:33

I like to be generous to myself.

Aaron van Wirdum: 00:15:34

Okay, well, it's clear to me.

Sjors Provoost: 00:15:36

Okay, excellent.

Aaron van Wirdum: 00:15:37

Did this cover the paper by the Singaporean, Japanese researchers? Yeah, I think so.

Sjors Provoost: 00:15:43

Because they said it was hard to solve and it's been solved. Nice. All right. So, thank you for listening to The Van Wirdum Sjorsnado.

Aaron van Wirdum: 00:15:50

There you go. Bye.
