---
title: "Bitcoin Core 0.21 Supports Tor V3"
transcript_by: jeffreyweier via review.btctranscripts.com
media: https://www.youtube.com/watch?v=KRPtbq8_1is
tags: ["bitcoin-core","onion"]
speakers: ["Sjors Provoost","Aaron Van Wirdum"]
categories: ["Podcast"]
date: 2020-10-15
---

## Introduction (0:0-00:34)

Aaron: 00:00:07

Live from Utrecht, this is the Van Wirdum Sjorsnado.
Sjors, you pointed out to me that Bitcoin Core has an amazing new feature merged into its repository.

Sjors: 00:00:19

Absolutely, we have bigger onions now.

Aaron: 00:00:22

Bigger onions.

Sjors: 00:00:23

Bigger onions.

Aaron: 00:00:24

Right, so I had basically no idea what it meant.
You figured it out.

Sjors: 00:00:29

I did.

Aaron: 00:00:29

You know everything about this.

Sjors: 00:00:30

Well, I wouldn't say that, but I know a thing or two.
So basically...

Aaron: 00:00:34

Yeah so let's start at the beginning.
It's about Tor.

Sjors: 00:00:37

Well it's also about Tor.

Aaron: 00:00:39

Okay.

Sjors: 00:00:40

But the Tor was kind of the big, I guess the big motivator to get everything in there.
So if you're familiar with...
Have you ever used Tor or do you know what Tor is?
I shouldn't ask those kind of questions.

Aaron: 00:00:51

I have a basic understanding of what Tor is, yes.

Sjors: 00:00:53

Exactly.
And when you see a Tor address, it's this weird little, it looks quite weird.

Aaron: 00:00:58

Right.

## How Tor works (0:58-2:10)

Sjors: 00:00:58

Is that a nice way to say it?
And so the idea is that it's actually a public key, essentially, a TOR address.
And that refers to a hidden service somewhere on the internet.
And the way you communicate to that hidden service is not directly because you don't know its IP address but indirectly through the Tor network and you use onion packages for that.
So the idea is that you start from the inside like the last hop before the hidden service and you give that hop instructions how to reach the hidden servers and then you write instructions for the second last hop and you give it instructions how to reach the first hop.

Aaron: 00:01:42

Sure yeah everyone is still using IP addresses it's just you don't know the IP address of the the Tor node you're communicating with instead you're communicating with other Tor nodes and every Tor node communicates with a direct peer so they all everyone only knows the IP address of their direct peer, but they don't know where the message originated or where it ends up.
Plus, they can't read the message because it's encrypted.

Sjors: 00:02:10

That's right.

Aaron: 00:02:11

And in order to support this, all of these Tor nodes have their own IP address, which is their onion address, and that's what they use to, that's what you're communicating with directly, so to say.

## Benefits of running a Bitcoin node behind Tor (2:23-3:03)

Sjors: 00:02:23

Yeah, and Bitcoin Core nodes can run behind such a hidden surface.
So everybody can have their Bitcoin node run at a secret location so your IP address remains secret.

Aaron: 00:02:35

What's the practical benefit of that?

Sjors: 00:02:38

Well your IP address remains secret so if you don't want the rest of the world to know that your IP address is running a Bitcoin node, maybe that's useful.

Aaron: 00:02:48

Yeah, and I think it's also because if you're sending transactions from an IP address, then network analyzers can reveal where transactions originated.
Although I guess that's also being solved, right?
There's other solutions for that as well.

Sjors: 00:03:03

Well, that's defense in depth, right?
So ideally your node behaves in a way that it looks indistinguishable from all other nodes.
So your node downloads all the blocks and it downloads all the mempool transactions and you can't tell which wallet is running inside which node, but there's all these sneaky companies that try anyway.
And then they might know that you sent a specific transaction, or then they might know which Bitcoins belong to you, and since your IP address is quite easy to figure out who you are.
It could be nice to have Tor in theory.
But regardless, I mean, that's just how it works.

Aaron: 00:03:40

Okay, so you can use Bitcoin from behind Tor and I think the thing was that there's a new type of Onion addresses.
There was an update in the Tor protocol.

Sjors: 00:03:52

That's right.

Aaron: 00:03:52

And that uses new addresses.

Sjors: 00:03:55

Yes.
So the Tor addresses are now longer, essentially, which just makes them more secure.
And I guess we don't need to go into why that is, because I don't know why that is.
All we know is that Onion addresses now, version 3, are a bit longer.
And that means that if you want to run it, keep running a Bitcoin node on Tor, you'll have to use those longer addresses because Tor is centralized and they have decided to eventually get rid of the version 2 addresses.

Aaron: 00:04:23

Okay, but they didn't yet.
So right now version 2 addresses are still usable?

Sjors: 00:04:27

Yes, I think they've been officially deprecated now and I think in about a year or so, they won't work anymore.

Aaron: 00:04:33

I see.
So anyone who wants to continue using Tor needs to upgrade before next year, so to say.

Sjors: 00:04:42

Something like that.

Aaron: 00:04:42

Roughly.
So that's why Bitcoin would need to be upgraded in order to support this new address.

Sjors: 00:04:47

Yes.
So then we get to the question of why would this make a difference?
What's wrong with a longer address?
And that has to do with how Bitcoin nodes spread the word about who they are.
Because how do you know which node to connect to?
And the idea there is that nodes can communicate with each other, they send each other lists of known nodes.
So they ask each other, hey, which Bitcoin nodes do you know?
And then they get a list of IP addresses.
And generally those are either IPv4 addresses or IPv6 addresses.
IPv6 is the new kid in town since, I don't know, 1998 or something.

Aaron: 00:05:26

Right, these are the regular IP addresses.

Sjors: 00:05:29

Correct.

Aaron: 00:05:30

Yeah, the IPv6 ones are longer as well, and that's because IPv4 was running out, right?

Sjors: 00:05:36

Right.
There's only, I think, 4 billion potential IPv4 addresses, whereas there's just enough for every molecule in the universe of IPv6 addresses.

Aaron: 00:05:46

Right.
So there's a list, or Bitcoin nodes keep lists of other Bitcoin nodes and their IP addresses.

Sjors: 00:05:55

Yes, and the way you would communicate a Tor address that way is you would kind of piggyback on IPv6 because there is a convention, I think it's used outside of Bitcoin too, where if the IPv6 address starts with a certain prefix, certain characters, certain numbers, then everything that follows is the Tor address because the Tor version 2 address, let me see if I got it right.
An IPv6 address is 16 bytes and a Tor address is only 10 bytes.
So you can hide inside of it.

Aaron: 00:06:27

So Bitcoin nodes keep the IP addresses of other Bitcoin nodes they know, and these are these IPv4 and IPv6, and some of the IP6 are also the Tor addresses.
And this is what, when nodes connect with each other, they share their lists, so everyone has an even more complete list of all of the Bitcoin nodes.
Is this correct?

Sjors: 00:06:49

That's right, yes.
The problem with Tor version 3 addresses is that they are 32 bytes, which is twice as long as an IPv6 address.

Aaron: 00:06:56

Right, so now you can't hide it inside an IPv6 address.

Sjors: 00:06:59

No, So just nodes have no way to communicate those addresses at the moment.

Aaron: 00:07:04

Right.
So that has been upgraded.

## Discussing how Bitcoin node gossip addresses (7:08-8:19)

Sjors: 00:07:08

Exactly.
So this is not rocket science to solve, but somebody actually needs to do it.
And somebody, Vladimir Vondelan wrote a standard a while ago, I think in 2019, that has a new way of communicating, of gossiping addresses.
And the major change is that you can, each message says, okay, this is the type of address I'm going to communicate, and there can be various types, including the new Tor one, but also future ones.
And then it can have different lengths.
So in the future, if a new address format comes along that's too long, that's not going to be a problem.

Aaron: 00:07:44

Right.
So that sounds like a pretty straightforward upgrade from my layman's perspective as a non-programmer.

Sjors: 00:07:52

It is.

Aaron: 00:07:52

But a very important one because we do want to keep using Tor potentially.

Sjors: 00:07:58

Yeah, and the nice thing is it's a completely new peer-to-peer message.
So I guess old nodes just ignore that message, or if you know it's an old node that you're talking to, you don't use that message.
So newer nodes will know this new message and can communicate all these new address types and older nodes just carry on like nothing happened.

Aaron: 00:08:18

Right.
Okay, I have one follow-up question about this sharing of lists and sharing of IP addresses, which is not Tor specific, I guess, but how do you actually connect to the first node?
How do you bootstrap to the network?
If you have no list yet of other nodes, then how do you find the first node?
How does this actually work in Bitcoin?

## : Explaining how DNS works (8:44-10:40)

Sjors: 00:08:44

Yeah, so the bootstrap problem, basically, you've just downloaded Bitcoin Core or some other client and you start it up and now what?
Is it just going to guess random IP addresses?
No, right?
So it needs to know another node to connect to, at least one, preferably a couple.
The way it tries to do that is using something called DNS seeds.
The internet DNS system is used for websites when you type an address www.google.com.
What your browser does is it asks a DNS server what IP addresses are from that Google domain.

Aaron: 00:09:18

Yep.
How many, do you know how many DNS servers there are?

Sjors: 00:09:22

Lots of them, because basically if you run a website, your hosting provider will have a DNS server that points to your website, but then your country will have a DNS server that will point to your hosting provider, and your internet provider has a DNS server that points to all these different countries, etc.
So it's very redundant.

Aaron: 00:09:43

We're going very off the trail here, but I do find it interesting.
How do these DNS servers remain in sync?

Sjors: 00:09:52

So basically, when you have a DNS record, so if you are maintaining a website, you usually have to go into some control panel and type in the IP address of your server and then your domain name and that's stored on the DNS server.
One of the fields you have to fill out is the timeout.
So what you're saying is after 24 hours for example or after one hour you should ask me again.
So when you're visiting a website you're gonna ask your maybe your ISP hey do you know the IP address for this website?
And if it doesn't, it's going to ask the next DNS server up the street, basically, say, do you know it?
And then as soon as it finds a record, it's going to say, okay, is this record still valid or is this expired?
And if it's still valid, it'll use it.
And if it's expired, it'll go up closer and closer to the actual, to the actual hosting provider.
So it's, it's basically cached.
Does that make sense?
So the easiest would be if you go to a domain like say google.com.
Okay, how do you find the IP address?
Well, you ask Google what the IP address is.
But how do you know what the IP address is for google.com.
You don't know that because that's what you were trying to find out.
So you have to ask somebody else.
And so you ask your internet provider, do you know the way to google.com?
Well, your internet provider might not know that, but it says, well, I know the way to .com basically, and .com will know the way to google.com.
So that's kind of how it works.
.nl, same, you go to you ask .nl, you know, where is google.nl?

Aaron: 00:11:27

Okay, yeah, that makes total sense.

Sjors: 00:11:30

Yeah, and ideally they already have this cached, because so many people go to google.com, that if you ask your ISP where is google.com, they'll know, because somebody else asked.
But if they don't know, they'll send you to .com.

Aaron: 00:11:41

Right, okay, so this is where I'm really getting at.
The DNS system is ultimately centralized, right?

Sjors: 00:11:47

Yes.

Aaron: 00:11:48

There's a centralization risk there.

Sjors: 00:11:50

Absolutely.

Aaron: 00:11:51

Where you're trusting the DNS server.

Sjors: 00:11:53

And for Bitcoin, we're kind of abusing it.

Aaron: 00:11:55

Right.

Sjors: 00:11:56

Because Bitcoin nodes are not websites.
But the idea is that there are a couple of core developers who run DNS seeds, which are essentially DNS servers.
And we're just pretending that, for example, seed.bitcoin.provoost.nl, which is what I'm running, is a website, quote unquote.
And when you ask that website, quote unquote, what its IP address is, you get a whole list of IP addresses.
But those IP addresses are Bitcoin nodes, and every time you ask it, it's going to give you different IP addresses.

Aaron: 00:12:28

Right, so what if someone corrupts you?

## DNS is storing list of bitcoin nodes. (12:30-13:30)

Sjors: 00:12:31

Well, one step back.
So this means that the standard infrastructure of the internet, all the internet service providers in the world and all these others are caching exactly where all the Bitcoin nodes are, because they think it's just a website.

Aaron: 00:12:42

Mm-hmm.


Sjors: 00:12:42

So it's kind of nice that you keep all these lists of nodes redundantly stored on the internet.
And there's quite a few protections on the internet, you know, against censorship of DNS.
So you're leveraging all that.
But at the same time, of course, if I and the other people were to lie and run a fake server, we could send you to any node we want.
But that would be very visible.

Aaron: 00:13:06

All right.
And the reason it's visible is because anyone can request these IP addresses from you and then check if they're actually Bitcoin nodes or not, or if you're trying to cheat there.
That's the reason they're visible.

Sjors: 00:13:16

Yeah, exactly.

Aaron: 00:13:17

It would be hard to cheat.

Sjors: 00:13:20

If you were to cheat like that, like very non-randomly, like to add to the whole world, it'd be very obvious.

Aaron: 00:13:26

Right.
So, but what if it happens?
Like, is there another way to connect to the Bitcoin network at that point?

Sjors: 00:13:31

Well, if they're lying, it's tricky, but if they're just offline, so if all the Bitcoin DNS seeds are not reachable, then inside the Bitcoin Core source code, and also in the thing you download, is a list of IP addresses, as well as a few hidden services.

Aaron: 00:13:47

Right, so that's also Bitcoin nodes.
They're embedded into the source code.

Sjors: 00:13:52

Yeah, so every year

Aaron: 00:13:53

or so we...
Which nodes are these, or why are these embedded in the source code?

Sjors: 00:13:57

Okay, so what happens every six months or so is we ask all the DNS seed maintainers to provide a list of the most reliable nodes.
Just all the nodes sorted by how frequently they're online.
Because your DNS seed tends to track, I've polled this node once and it was online.
So basically what a DNS seed does on its side is it's just a crawler.
So the DNS seed goes to a couple of Bitcoin nodes, asks it for all the nodes it knows, keeps a list and just goes to the list, pings them all.
Then once it's done pinging them all, it's just going to ping them all again, and it keeps track of how often they're online.
So you make a list of that sorted by reliability, you take that from all the contributors, and that goes into the source code.
So that's the fallback.

Aaron: 00:14:48

Interesting.

Sjors: 00:14:49

But it's only the first time you start your node, at least in theory.
So only the very first time you start your node, you need this.

Aaron: 00:14:56

Sure.

Sjors: 00:14:57

After that, you keep track of the nodes you know about, you store all these gossip nodes in a file, and you start opening the file and you just try the nodes you know about and only if you run out if it doesn't work you ask to see it again

Aaron: 00:15:10

Yep, and then you keep syncing your list of IP addresses with the new nodes?

Sjors: 00:15:16

Yeah, exactly.
I think whenever a node connects to you for the first time, that's one of the first things they ask.
Who else do you know?
I think you can even send them unsolicited.

Aaron: 00:15:25

Okay.

Sjors: 00:15:27

Which is why, you know, if you start a new node, you get inbound connections pretty quickly.
Because you've announced your IP address to other people and they're gossiping it around and these other nodes then start connecting.

Aaron: 00:15:38

Interesting.
Okay, so that makes it pretty clear to me.
You bootstrap to the Bitcoin network by first querying DNS records to find other Bitcoin nodes.
You get a list of IP addresses.
You use these to connect to the actual Bitcoin nodes, which could also be Tor nodes at that point, right?
These you can also query from the DNS records.
At that point you ask about all of the nodes they know and you update your list and from that point on you're also sharing your, the IP addresses you have with other nodes.
So far these were IP4 and IP6 and IP6 had a subset of Onion nodes.
And with this upgrade, we'll be ready for a newer version of Onion nodes.
That's the story.

Sjors: 00:16:28

That's about right.

Aaron: 00:16:28

That's our podcast.
Great.

Sjors: 00:16:30

And one tiny little thing that was recently added is that the Bitcoin node actually can spin up the version three on your node, but that is actually like a five line change.
So that's quite nice.
That'll just work TM when you start a, I don't know, I think it's version 0.21 if you started up.
If you were running a version 2 node before, it's going to run a version 3 Tor node after.
If you weren't, then you need to read the documentation how to set it up if you want to use it.

Aaron: 00:16:58

Good.

Sjors: 00:16:59

So, yeah, that's all.

Aaron: 00:17:01

I guess that's it.

Sjors: 00:17:02

All right.

Aaron: 00:17:03

Guys I forgot to mention something.

Sjors: 00:17:05

Oh my god.

Aaron: 00:17:05

I have amazing news.

Sjors: 00:17:07

Tell me.

Aaron: 00:17:08

Actually, Sjors you already know the news.

Sjors: 00:17:09
I know.

Aaron: 00:17:10
Ruben.

Ruben: 00:17:11

What's the news?

Aaron: 00:17:12

The Van Wirdum Sjorsnado has its own feed now.

Ruben: 00:17:14

Wow.

Aaron: 00:17:16

Its own RSS feed and it showed up in my podcast app.

Ruben: 00:17:19

Excellent.

Aaron: 00:17:20

So I'm now subscribed to the the Van Wirdum Sjorsnado.
If you're listening and if you want to hear for all our episodes, then you can subscribe to the Van Wirdum Sjorsnado.

Ruben: 00:17:29

I'll be subscribing for sure.
It's actually exactly what I was asking you guys for, like what I was missing.
I just wanted to be able to subscribe to your podcast specifically.
So great.

Aaron: 00:17:37

So that's two subscribers already, Sjors.
Me and Ruben.

Sjors: 00:17:40

That's excellent.

Aaron: 00:17:42
We're on a roll.

Sjors: 00:17:44
I was already subscribed.
So another related news is that we have had our first swap cast.

Ruben: 00:17:49

Oh yeah, that's true.

Sjors: 00:17:50

Because we actually featured on

Aaron: 00:17:51

the Unhashed podcast.

Ruben: 00:17:54

That's right.
Yeah, so sometimes we're getting technical issues or whatever and unable to record.
And then what we do is we look at other podcasts or something where maybe I appear or one of the other guys and we broadcast that.
So in this case, I came onto your show.
So I asked you guys, maybe we can put that on the Unhashed podcast.
So our Unhashed podcast listeners were also able to listen to the last episode.
And probably, you know, if I don't know, a couple of weeks from now we run into issues again maybe I'll be asking you to air this episode so maybe number two

Sjors: 00:18:25

yeah if you need an extra motivation to check that out we actually re-edited the audio so it's gonna be a little bit better than the original.

Ruben: 00:18:32

That's correct.

Aaron: 00:18:33

Alright I wanted to mention that.

Sjors: 00:18:34

Thank you for listening to the Van Wirdum Sjorsnado.

Aaron: 00:18:37

There you go.
