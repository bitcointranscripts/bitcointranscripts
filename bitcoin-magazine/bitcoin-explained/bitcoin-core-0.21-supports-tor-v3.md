---
title: "Bitcoin Core 0.21 Supports Tor V3"
transcript_by: jeffreyweier via review.btctranscripts.com
media: https://www.youtube.com/watch?v=KRPtbq8_1is
tags: ["bitcoin-core","onion"]
speakers: ["Sjors Provoost","Aaron van Wirdum"]
categories: ["podcast"]
date: 2020-10-15
---
## Introduction

Aaron van Wirdum: 00:00:07

Live from Utrecht, this is the Van Wirdum Sjorsnado.
Sjors, you pointed out to me that Bitcoin Core has an amazing new feature merged into its repository.

Sjors Provoost: 00:00:19

Absolutely, we have bigger onions now.

Aaron van Wirdum: 00:00:24

Right, so I had basically no idea what it meant.
You figured it out.

Sjors Provoost: 00:00:29

I did.

Aaron van Wirdum: 00:00:34

Yeah so let's start at the beginning.
It's about Tor.

Sjors Provoost: 00:00:40

Tor was the big motivator to get everything in there.
Have you ever used Tor or do you know what Tor is?

Aaron van Wirdum: 00:00:51

I have a basic understanding of what Tor is, yes.

Sjors Provoost: 00:00:53

When you see a Tor address it looks quite weird.

Aaron van Wirdum: 00:00:58

Right.

## How does Tor work?

Sjors Provoost: 00:00:58

And so the idea is that it's a public key, essentially, a TOR address.
And that refers to a hidden server somewhere on the internet.
And the way you communicate to that hidden server is not directly because you don't know its IP address but indirectly through the Tor network and you use onion packages for that.
So the idea is that you start from the inside the last hop before the hidden server and you give that hop instructions how to reach the hidden servers and then you write instructions for the second last hop and you give it instructions how to reach the first hop.

Aaron van Wirdum: 00:01:42

Everyone is still using IP addresses it's just you don't know the IP address of the the Tor node you're communicating with instead you're communicating with other Tor nodes and every Tor node communicates with a direct peer so they all everyone only knows the IP address of their direct peer, but they don't know where the message originated or where it ends up.
Plus, they can't read the message because it's encrypted.

Sjors Provoost: 00:02:10
That's right.

Aaron van Wirdum: 00:02:11

And in order to support this, all of these Tor nodes have their own IP address, which is their onion address, and that's what they use to, that's what you're communicating with directly.

## Benefits of running a Bitcoin node behind Tor

Sjors Provoost: 00:02:23

And Bitcoin Core nodes can run behind such a hidden surface.
So everybody can have their Bitcoin node run at a secret location so your IP address remains secret.

Aaron van Wirdum: 00:02:35

What's the practical benefit of that?

Sjors Provoost: 00:02:38

Your IP address remains secret so if you don't want the rest of the world to know that your IP address is running a Bitcoin node, maybe that's useful.

Aaron van Wirdum: 00:02:48

Yeah, and I think it's also because if you're sending transactions from an IP address, then network analyzers can reveal where transactions originated.
Although I guess that's also being solved.
There's other solutions for that as well.

Sjors Provoost: 00:03:03

That's defense in depth.
Ideally your node behaves in a way that it looks indistinguishable from all other nodes.
Your node downloads all the blocks and it downloads all the mempool transactions and you can't tell which wallet is running inside which node, but there's all these sneaky companies that try anyway.
And then they might know that you sent a specific transaction, or then they might know which Bitcoins belong to you, and since your IP address is quite easy to figure out who you are.
It could be nice to have Tor in theory.
But regardless, that's just how it works.

Aaron van Wirdum: 00:03:40

So you can use Bitcoin from behind Tor and I think the thing was that there's a new type of Onion addresses.
There was an update in the Tor protocol.

Sjors Provoost: 00:03:52

That's right.

Aaron van Wirdum: 00:03:52

And that uses new addresses.

Sjors Provoost: 00:03:55

Yes.
So the Tor addresses are now longer, which just makes them more secure.
We don't need to go into why that is, because I don't know why that is.
All we know is that Onion addresses now, in version 3, are a bit longer.
And that means that if you want to keep running a Bitcoin node on Tor, you'll have to use those longer addresses because Tor is centralized and they have decided to eventually get rid of the version 2 addresses.

Aaron van Wirdum: 00:04:23

Okay, but they didn't yet.
So right now version 2 addresses are still usable?

Sjors Provoost: 00:04:27

Yes, I think they've been officially deprecated now and I think in about a year or so, they won't work anymore.

Aaron van Wirdum: 00:04:33

I see.
So anyone who wants to continue using Tor needs to upgrade before next year.

Sjors Provoost: 00:04:42

Something like that.

Aaron van Wirdum: 00:04:42

So that's why Bitcoin would need to be upgraded in order to support this new address.

Sjors Provoost: 00:04:47

Yes.
So then we get to the question of why would this make a difference?
What's wrong with a longer address?
And that has to do with how Bitcoin nodes spread the word about who they are.
Because how do you know which node to connect to?
And the idea there is that nodes can communicate with each other, they send each other lists of known nodes.
So they ask each other, hey, which Bitcoin nodes do you know?
And then they get a list of IP addresses.
And generally those are either IPv4 addresses or IPv6 addresses.
IPv6 is the new kid in town since, 1998 or something.

Aaron van Wirdum: 00:05:26

Right, these are the regular IP addresses.

Sjors Provoost: 00:05:29

Correct.

Aaron van Wirdum: 00:05:30

The IPv6 ones are longer as well, and that's because IPv4 was running out, right?

Sjors Provoost: 00:05:36

Right.
There's only, I think, 4 billion potential IPv4 addresses, whereas there's just enough for every molecule in the universe of IPv6 addresses.

Aaron van Wirdum: 00:05:46

Right.
So Bitcoin nodes keep lists of other Bitcoin nodes and their IP addresses.

Sjors Provoost: 00:05:55

Yes, and the way you would communicate a Tor address is you would piggyback on IPv6 because there is a convention, I think it's used outside of Bitcoin too, where if the IPv6 address starts with a certain prefix, certain characters, certain numbers, then everything that follows is the Tor address because the Tor version 2 address, let me see if I got it right.
An IPv6 address is 16 bytes and a Tor address is only 10 bytes.
So you can hide inside of it.

Aaron van Wirdum: 00:06:27

So Bitcoin nodes keep the IP addresses of other Bitcoin nodes they know, and these are these IPv4 and IPv6, and some of the IPv6 are also the Tor addresses.
And when nodes connect with each other, they share their lists, so everyone has an even more complete list of all of the Bitcoin nodes.
Is this correct?

Sjors Provoost: 00:06:49

That's right, yes.
The problem with Tor version 3 addresses is that they are 32 bytes, which is twice as long as an IPv6 address.

Aaron van Wirdum: 00:06:56

Right, so now you can't hide it inside an IPv6 address.

Sjors Provoost: 00:06:59

No, so nodes have no way to communicate those addresses at the moment.

Aaron van Wirdum: 00:07:04

Right.
So that has been upgraded.

## How does a Bitcoin node gossip addresses?

Sjors Provoost: 00:07:08

Exactly.
So this is not rocket science to solve, but somebody actually needs to do it.
And Wladimir van der Laan wrote a standard a while ago, I think in 2019, that has a new way of communicating, of gossiping addresses.
And the major change is that you can, each message says, this is the type of address I'm going to communicate, and there can be various types, including the new Tor one, but also future ones.
And then it can have different lengths.
So in the future, if a new address format comes along that's too long, that's not going to be a problem.

Aaron van Wirdum: 00:07:44

So that sounds like a pretty straightforward upgrade from my layman's perspective as a non-programmer.

Sjors Provoost: 00:07:52

It is.

Aaron van Wirdum: 00:07:52

But a very important one because we do want to keep using Tor potentially.

Sjors Provoost: 00:07:58

Yeah, and the nice thing is it's a completely new peer-to-peer message.
So old nodes just ignore that message, or if you know it's an old node that you're talking to, you don't use that message.
So newer nodes will know this new message and can communicate all these new address types and older nodes just carry on like nothing happened.

Aaron van Wirdum: 00:08:18

Okay, I have one follow-up question about this sharing of lists and sharing of IP addresses, which is not Tor specific, but how do you actually connect to the first node?
How do you bootstrap to the network?
If you have no list yet of other nodes, then how do you find the first node?
How does this actually work in Bitcoin?

## How does DNS work?

Sjors Provoost: 00:08:44

Yeah, so the bootstrap problem, basically, you've just downloaded Bitcoin Core or some other client and you start it up and now what?
Is it just going to guess random IP addresses?
No.
So it needs to know another node to connect to, at least one, preferably a couple.
The way it tries to do that is using something called DNS seeds.
The internet DNS system is used for websites when you type an address www.google.com.
What your browser does is it asks a DNS server what IP addresses are from that Google domain.

Aaron van Wirdum: 00:09:18

Do you know how many DNS servers there are?

Sjors Provoost: 00:09:22

Lots of them, because if you run a website, your hosting provider will have a DNS server that points to your website, but then your country will have a DNS server that will point to your hosting provider, and your internet provider has a DNS server that points to all these different countries, etc.
So it's very redundant.

Aaron van Wirdum: 00:09:43

We're going very off the trail here, but I do find it interesting.
How do these DNS servers remain in sync?

Sjors Provoost: 00:09:52

So basically, when you have a DNS record, so if you are maintaining a website, you usually have to go into some control panel and type in the IP address of your server and then your domain name and that's stored on the DNS server.
One of the fields you have to fill out is the timeout.
So what you're saying is after 24 hours for example or after one hour you should ask me again.
So when you're visiting a website you're gonna ask your maybe your ISP hey do you know the IP address for this website?
And if it doesn't, it's going to ask the next DNS server up the street, basically, say, do you know it?
And then as soon as it finds a record, it's going to say, is this record still valid or is this expired?
And if it's still valid, it'll use it.
And if it's expired, it'll go up closer and closer to the actual hosting provider.
So it's, it's basically cached.
Does that make sense?
So the easiest would be if you go to a domain like say google.com.
Okay, how do you find the IP address?
Well, you ask Google what the IP address is.
But how do you know what the IP address is for google.com.
You don't know that because that's what you were trying to find out.
So you have to ask somebody else.
And so you ask your internet provider, do you know the way to google.com?
Well, your internet provider might not know that, but it says, I know the way to .com basically, and .com will know the way to google.com.
So that's kind of how it works.
.nl, same, you go to you ask .nl, where is google.nl?

Aaron van Wirdum: 00:11:27

Okay, that makes total sense.

Sjors Provoost: 00:11:30

Ideally they already have this cached, because so many people go to google.com, that if you ask your ISP where is google.com, they'll know, because somebody else asked.
But if they don't know, they'll send you to .com.

Aaron van Wirdum: 00:11:41

Right, so this is where I'm really getting at.
The DNS system is ultimately centralized.
There's a centralization risk there.
Where you're trusting the DNS server.

Sjors Provoost: 00:11:53

And for Bitcoin, we're kind of abusing it.
Because Bitcoin nodes are not websites.
But the idea is that there are a couple of core developers who run DNS seeds, which are essentially DNS servers.
And we're just pretending that, for example, seed.bitcoin.provoost.nl, which is what I'm running, is a website, quote unquote.
And when you ask that website, quote unquote, what its IP address is, you get a whole list of IP addresses.
But those IP addresses are Bitcoin nodes, and every time you ask it, it's going to give you different IP addresses.

Aaron van Wirdum: 00:12:28

Right, so what if someone corrupts you?

## How does Bitcoin maintain a list of nodes?

Sjors Provoost: 00:12:31

Well, one step back.
So this means that the standard infrastructure of the internet, all the internet service providers in the world and all these others are caching exactly where all the Bitcoin nodes are, because they think it's just a website.
So it's kind of nice that you keep all these lists of nodes redundantly stored on the internet.
And there's quite a few protections on the internet, against censorship of DNS.
So you're leveraging all that.
But at the same time, if I and the other people were to lie and run a fake server, we could send you to any node we want.
But that would be very visible.

Aaron van Wirdum: 00:13:06

All right.
And the reason it's visible is because anyone can request these IP addresses from you and then check if they're actually Bitcoin nodes or not, or if you're trying to cheat there.
That's the reason they're visible.

Sjors Provoost: 00:13:16

Exactly.

Aaron van Wirdum: 00:13:17

It would be hard to cheat.

Sjors Provoost: 00:13:20

If you were to cheat like that, very non-randomly, to add to the whole world, it'd be very obvious.

Aaron van Wirdum: 00:13:26

Right.
But what if it happens?
Is there another way to connect to the Bitcoin network at that point?

Sjors Provoost: 00:13:31

If they're lying, it's tricky, but if they're just offline, if all the Bitcoin DNS seeds are not reachable, then inside the Bitcoin Core source code, and also in the thing you download, is a list of IP addresses, as well as a few hidden servers.

Aaron van Wirdum: 00:13:47

That's also Bitcoin nodes.
They're embedded into the source code.
Which nodes are these, or why are these embedded in the source code?

Sjors Provoost: 00:13:57

What happens every six months or so is we ask all the DNS seed maintainers to provide a list of the most reliable nodes.
Just all the nodes sorted by how frequently they're online.
Because your DNS seed tends to track, I've polled this node once and it was online.
So basically what a DNS seed does on its side is it's just a crawler.
The DNS seed goes to a couple of Bitcoin nodes, asks it for all the nodes it knows, keeps a list and just goes to the list, and pings them all.
Then once it's done pinging them all, it's just going to ping them all again, and it keeps track of how often they're online.
So you make a list sorted by reliability, you take that from all the contributors, and that goes into the source code.
That's the fallback.

Aaron van Wirdum: 00:14:48

Interesting.

Sjors Provoost: 00:14:49

But it's only the first time you start your node, at least in theory.
So only the very first time you start your node, you need this.
After that, you keep track of the nodes you know about, you store all these gossip nodes in a file, and you start opening the file and you just try the nodes you know about and only if you run out if it doesn't work you ask to see it again

Aaron van Wirdum: 00:15:10

Yep, and then you keep syncing your list of IP addresses with the new nodes?

Sjors Provoost: 00:15:16

Yeah, exactly.
I think whenever a node connects to you for the first time, that's one of the first things they ask.
Who else do you know?
I think you can even send them unsolicited.
Which is why, if you start a new node, you get inbound connections pretty quickly.
Because you've announced your IP address to other people and they're gossiping it around and these other nodes then start connecting.

Aaron van Wirdum: 00:15:38

Interesting.
So that makes it pretty clear to me.
You bootstrap to the Bitcoin network by first querying DNS records to find other Bitcoin nodes.
You get a list of IP addresses.
You use these to connect to the actual Bitcoin nodes, which could also be Tor nodes at that point.
These you can also query from the DNS records.
At that point you ask about all of the nodes they know and you update your list and from that point on you're also sharing your, the IP addresses you have with other nodes.
So far these were IPv4 and IPv6 and IPv6 had a subset of onion nodes.
And with this upgrade, we'll be ready for a newer version of onion nodes.
That's the story.

Sjors Provoost: 00:16:28

That's about right.

Aaron van Wirdum: 00:16:28

That's our podcast.
Great.

Sjors Provoost: 00:16:30

And one tiny little thing that was recently added is that the Bitcoin node actually can spin up the version three on your node, but that is actually like a five line change.
So that's quite nice.
That'll just work when you start a, I don't know, I think it's version 0.21 if you started up.
If you were running a version 2 node before, it's going to run a version 3 Tor node after.
If you weren't, then you need to read the documentation how to set it up if you want to use it.

Aaron van Wirdum: 00:16:58

Good.

Sjors Provoost: 00:16:59

So, yeah, that's all.
