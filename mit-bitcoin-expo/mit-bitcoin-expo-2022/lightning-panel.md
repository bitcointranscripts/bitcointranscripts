---
title: Lightning Panel
transcript_by: markon1-a via review.btctranscripts.com
media: https://www.youtube.com/watch?v=hlTfA42b_uI
tags:
  - lightning
  - taproot
  - ptlc
  - htlc
speakers:
  - Jeremy Rubin
  - Rene Pickhardt
  - Lisa Neigut
  - Jonathan Harvey Buschel
date: 2022-07-05
summary: The discussion primarily revolved around the Lightning Network, a scaling solution for Bitcoin designed to enable faster, decentralized transactions. Rene Pickhardt and Lisa Neigut shared their insights, highlighting Lightning's potential as a peer-to-peer electronic cash system and a future payment infrastructure. They emphasized its efficiency for frequent transactions between trusted parties but noted challenges in its current infrastructure, such as the need for continuous online operation and the risk of losing funds if a node is compromised. The panelists discussed the scalability of the network, indicating that while millions could use it self-sovereignly, larger-scale adoption would likely involve centralized service providers. The conversation also touched on the impact of Taproot on privacy and channel efficiency, and the technical intricacies of maintaining state and preventing fraud within the network.
---
## What is Lightning

Jeremy Rubin: 00:00:07

I was hoping that we can have our panelists, and maybe we'll start with Rene.
Just introduce themselves quickly, and also answer the question, what is Lightning to you?
And I mean that sort of in the long run.
Lightning is a thing today, but what is the philosophical Lightning to you?

Rene Pickhardt: 00:00:26

So I'm Rene Pickardt, a researcher and developer for the Lightning Network.
And for me personally, the Lightning Network is the means to really create this peer-to-peer electronic cash system so to use Bitcoin in a decentralized way and fast way.

Lisa Neigut: 00:00:45

Cool, hey everyone I am Lisa Neigut.
 I work at Blockstream on Core Lightning, which is a implementation of Lightning.
I see Lightning as probably Bitcoin scaling, like the thing that's going to scale Bitcoin.
I'm going like totally get this wrong.
It's cool.
I see it as like payment rails of the future.
I think it's like definitely the way to scale the number of people that are able to make Bitcoin transactions.
I also see it as being the most decentralized L2 that exists today, which is cool.

## When does it make sense to use Lightning? 

Jeremy Rubin: 00:01:27

Okay, and then we'll hopefully get Jonathan in here in a second.
But Jonathan is also a fellow MIT Bitcoin Club person.
He was, I believe, the second president of the club and hosted the expo and currently works at Lightning Labs.
Where is Jonathan EOM is a little bit of a meme around MIT, so we're looking for Jonathan.
So one question I have is, I don't have any Lightning channels and I'm okay.
So when do I actually want to use Lightning?
When am I going to be like, I better use Lightning right now?

Rene Pickhardt: 00:02:16

I mean, I use Lightning whenever I want to pay people with Bitcoin, because for me personally the user experience is just much better than waiting for on-chain confirmations, choosing my fee rate that I'm willing to pay.
I mean I remember once in a while I had to wait like two months to get a Bitcoin transaction confirmed.
With Lightning I usually know this much faster.

Lisa Neigut: 00:02:45

Yeah so I mean I think the thing about Lightning is Lightning makes a lot of sense when you're trying to make repeated number of payments, I think, between a number of parties, right?
And so Lightning is really scaling in the sense that you've got a certain number of channel parties, maybe channel parties isn't the right term there, but that are kind of all embedded in this network.
And the idea is that it's a bunch of people that are transacting between each other over kind of an extended period of time.
So I think Lightning channels to some extent like express relationships of commerce between parties that have set up basically like sort of long running infrastructure to help manage that to some extent.
I think kind of what I'm hinting at here in terms of like, when does lightning make sense is if you're just going to pay someone one time, it doesn't make sense to open a Lightning channel to do that to a large extent, just because of the way the infrastructure is set up.
Well, okay, sort of depends on a lot of things here.
But I think a lot of times you're not going to see a lot of return on the Lightning payment stuff until you start getting into more congestion on the main network, so it'll be cheaper, or you're doing a lot of transacting with Bitcoin, at which point it can drive down the cost of the transacting you're doing.

Jeremy Rubin: 00:04:21

Okay, so I'm convinced, and I'm going to take all my Bitcoin and put them into Lightning channels, because you sold me.
And then the year is, 2042 or something like that.
And then everybody's doing everything in Lightning, blocks are full.
There's a fee market, and when am I not going to be able to use Lightning, and what circumstances will it make sense for me to do on-chain transactions as an individual?

Rene Pickhardt: 00:04:55

Okay, so first of all about convincing you, maybe you don't want to put all your Bitcoin into a Lightning node.

Jeremy Rubin: 00:05:01

Too late, I did it.

Rene Pickhardt: 00:05:03

Yeah, so I mean, one of the known downsides of the Lightning network protocol is that you cannot really operate a Lightning node in a cold storage fashion.
You have to really be online all the time.
Your keys are on an online or hot wallet, so there's a certain risk if your computer or your note gets compromised that you are screwed basically, you have a bolting accident or whatever the lingo is, right?
So you may not want to use all your Bitcoins on the Lightning Network.
The other situation that you addressed was the question of congestion on the Blockchain, if I understand you correctly.
And here I would argue that yes, the block space is something that relates to the security of the Lightning Network, because eventually if I have a conflict, I want to resolve this on the Bitcoin network.
But on the other hand, if there is so much congestion on the blockchain, I cannot do on-chain transactions anyway, right?
So we have to find the sweet spot of what fees we can pay.
I think there's no developments with anchor outputs that you can basically really make sure that your transaction goes in, but you might have to pay a certain premium.

Jeremy Rubin: 00:06:19

Got you.
So how many people are actually using Lightning today, or how many channels are there?
Like, I don't care about people, just like how much usage is there under some metric?

Lisa Neigut: 00:06:31

That's a great question.
I do not know the answer to that question.
Maybe Rene?

Rene Pickhardt: 00:06:38

I don't know the exact number right now, but I think we have something like 70,000 channels that we see on Gossip.
Those are the announced channels.
There are quite some services that don't announce the channels to the Gossip Network because they are represented by nodes that do not really want to engage into routing.
So yeah, that's currently the number, I guess.

Jeremy Rubin: 00:06:59

Okay, and could we do like 140,000 announced channels?

Rene Pickhardt: 00:07:05

Yeah, I don't think this would be a problem.
So basically, whenever you want to announce a channel, you basically have in the channel announcement message, give a pointer to the blockchain transaction or to the Bitcoin transaction in the blockchain.
So you can open as many channels theoretically as there are Bitcoin transactions per day possible on the Bitcoin network.
Of course, you then have to wonder about what will happen if channels closes, how much congestion do they put on the blockchain.

## What are the estimated maximum channels that can be on Lightning?

Jeremy Rubin: 00:07:36

So what is that maximum number if you just had to throw out a number if you saw this many announced channels, you'd be like, this seems like enough or the maximum.

Rene Pickhardt: 00:07:51

I mean, if I recall the numbers correctly, we currently see something like 300,000 Bitcoin transactions being processed per day.
So this is the theoretical maximum number of channels.
I mean, maybe on a byte level you could make this a little bit more efficient or not, but yeah, something around this order of magnitude.

Lisa Neigut: 00:08:11

Yeah, I think one thing that maybe we should talk about here is visibility into transactions that are happening on the Lightning Network, right?
I feel like you're asking for numbers of how many people are transacting with Lightning, right?
Like what's the total number of people that are using the network?
I think that the answer to that is really hard to get and part of the reason for that is how decentralized these payments are, right?
So the idea with the Lightning Network is that you can remove the transactions that you're making with Bitcoin off-chain.
That means that there's no public ledger of all of the transactions that you've made.
Instead, every time you make a transaction, you send it through a series of channels, like a series of tubes, and the record of that transaction is rather ephemeral, right?
Because there's no written record of that transaction that happens that's publicly visible that someone can go and count.
Only the parties that were involved in the routing of that transaction would even know that it happened.
So it's possible that there's like thousands of people and payments that are being processed by Lightning, but because of how decentralized it is, there's no single person or view of the network that will ever be able to give you a good, number of the amount of transactions that are currently happening on Lightning.

Jeremy Rubin: 00:09:43

Yeah, I think I'm more trying to get a sense of what's the maximum that we could do, and if we're going to hit a wall with that, as opposed to how many people are actually doing it.
I do believe it seems to be a lot of people, but do we hit some sort of obstacle of, well, so many people fit into a train car, so that the T, local Boston subway, probably you can only get a couple hundred people per 10 minutes or something.

Lisa Neigut: 00:10:12

Right.
Okay.
So when we're talking about theoretical maximum limits of the system, right?
Okay, so I think there's a couple interesting things to look at here.
The one that I like to think about is in terms of liquidity and Lightning.
So the way that Lightning works is that in order to have a balance to transact, you have to commit Bitcoin to basically a contract that is on chain, and the creation of that contract basically grants you like X units of Bitcoin that you can then transact with over the Lightning Network, right?
So theoretically, the maximum amount of credits that could be transacted over the Lightning Network at any one point in time would be 21 million worth of Bitcoin, that's assuming all the Bitcoin has been mined, like subtracting out all the amount that's been lost, et cetera.
So like, theoretical maximum in terms of amount of liquidity that's available on Lightning is going to be the total amount of Bitcoin that's been locked into the Lightning network, right?
So unless we're like locking all of the Bitcoin that exists into Lightning, at some point, that's going to be like the maximum total value of exchange that can happen at any one point in time.

Rene Pickhardt: 00:11:33

May I add one thing to that?
So when you look at routing on the Lightning Network, it's highly unreliable in the sense of it's a probabilistic process.
And the likelihood for payment to be successful depends on the size of the payment in comparison to the channel.
So if you imagine now everybody is using the Lightning Network in the world, I think you have something like 300,000 Satoshis of liquidity that every node on average can provide.
And obviously the Bitcoin is not uniformly distributed.
So, but if you see this, the question now is how large can the payments actually be?
Because, I mean, you need to have at least two channels, so you need to split these Satoshis.
Yeah, and then if the payment is going to be too large, you're going to have problems.
Right, so I think there are actually limitations just because Bitcoin is scarce.

Jeremy Rubin: 00:12:31

So I guess just asking very concretely, because I think that for my benefit and also for the audience's, are we talking a billion people that can do it?
Are we talking like 100 million people?
Are we talking about 10 million people?
1 million?
How many people actually could operationally, Lightning would be something they're using?

Lisa Neigut: 00:12:55

That's a really hard question to answer because I think it depends on what you count as Lightning users.
So we just saw a great presentation by Andre Neves about the Lightning address stuff, and a lot of the projects that he was showing that adopted it are what I would call custodial Lightning services.
I wish, I don't know if that's so much, correct me if I'm wrong, but my point is that all of the users of those networks are probably using Lightning to do their transactions, but they're probably using channels that someone else is using and managing.

Jeremy Rubin: 00:13:35

Well, do you count that?
That's sort of where I started the panel is like, what is your definition of this?
Is that in your definition of the Lightning Network?

Lisa Neigut: 00:13:43

I see.
Let's see.
I'm like kind of like a big tent-like person.
I would say that at the end of the day, the value of that transaction is being settled in Bitcoin using the Lightning Network, right?
The number of parties that are involved in that transaction is not merely peer-to-peer at that point, right?
It's kind of like having two financial institutions transacting on your behalf at that point, and the medium that they're using to transfer the value just so happens to be Bitcoin over the Lightning network.
So to some extent, that relationship that you have between a Lightning service provider, I think that's what they're calling themselves, I mean, you're transacting over Lightning, but you're asking someone else to effectuate that exchange over Lightning on your behalf, right?

Jeremy Rubin: 00:14:37

Okay, so I'm going to kick it up to Jonathan for a second, who's looking down on all of us now.
So blessed.
So Jonathan, we started off by just kind of asking everybody, philosophically, what is Lightning to you?
If you were to be transported 100 years into the future, and you saw people doing something, and you're like, that's lightning, versus maybe the implementation of it today being a different concept.
And then answering that same question of like, how many people do you think we can get, onboarded into that current vision?

Jonathan Harvey Buschel: 00:15:11

Sure.
So, I mean, this is the basic protocol that we want to use to move, mostly Bitcoin around right now.
So I'd say it's like on the same plane as, email, which kind of maybe didn't go the way we expected or the way it was intended, where there's a bunch of variety of services running email servers.
And there's kind of some open network.
I think with Lightning, we have a better shot at that just in terms of how teams have worked on the protocol and how easy it is to participate in currently.
But I think at the base, it's just a non-custodial, trust-minimized way to move some value around.
It doesn't have to be just Bitcoin.
We just happen to have implemented it here.
So I'm not sure if that answers your question.
But to look also at the scaling side of things, I think I wanted to add on to what Rene mentioned of like there are these bottlenecks in the network, right?
For every Lightning node running, they need to keep up with the state of the network.
And if we're, multiplying the number of nodes by like 10X, probably not everybody's going to be running a server in their house, right?
Not everybody does that right now.
You can buy some cheap computer and like put it in your basement and pull it off now but as the network grows like maybe that isn't something that's feasible but I would still say that you're using Lightning if you like have ownership of your funds if the service you're using is non-custodial and it may be that you know I'm running this server in my basement, and I've got all my friends that happen to be using that.
Or maybe we have some shared ownership of some node running in the cloud.
But still, we have nice guarantees about the security of our funds and what's actually happening with that node.

Jeremy Rubin: 00:17:08

Okay, so Rene, can I push you to just give me one word answer, a number?
And we're not going to hold you to it.
I just want to know, when I'm thinking about this, are we going to get to a number?

Rene Pickhardt: 00:17:23

So you won't get that number from me, but I will give you a better answer.
So, the question you're asking indirectly, as I understand it, is can we onboard 7 billion people to the Lightning Network?
And my answer would be not 7 billion people in the world want to be onboarded directly to the Lightning Network, right?
Take email as an example.
We just had a presentation about Lightning Address that is, like, to some sense similar to the user experience of email.
But many people are using web mail where they trust a certain service provider because they just don't want that.
The beauty about Lightning Network is everybody can join it if they want to take the hustle.
And I think in that respect, we should probably be able to onboard a million or maybe even 10 million self-sovereign users.
Of course, as Jonathan just said, there are limitations also to Gossip.
There are many things that we need to work on.
But I think from the Bitcoin network perspective, I mean, that is like a really hard constraint, right?
I mean, everything else is how Lightning is currently designed, but the Bitcoin blockchain really gives a bottleneck.
I think we can go there.
And my feeling is that should be sufficient to those people who really want to be self-sovereign.
That's at least my perspective.

Jeremy Rubin: 00:18:42

All right, cool.
Yeah, I think that's helpful context.
And I think part of what I'm hearing is that you could be wrong.
Like if we went to 100 million channels operating independently from there, it's not even necessarily that there would be some sort of big security risk or something.
It's more that it would just sort of structurally not be possible to assemble a network like that given the constraint of how many Satoshis are available.

Lisa Neigut: 00:19:17

Yeah, I mean, if we kind of take what Jonathan was saying, that he thinks that Lightning doesn't necessarily a Bitcoin-centric project.
So I think it's like, there's two questions here, right?
Is Lightning Bitcoin scaling solution and is that its sole purpose?
Or is Lightning a technology of how to transfer value in a very decentralized manner that can have other types of value locked into it that it's then transacting.
If it's just Bitcoin, then how many Satoshis, how many transactions to open channels can you fit into a block?
That's important because it's like, okay, there's like X billion people that want to open a Lightning channel because that's the only way they can get onboarded onto the network.
How many blocks would it take to get X billion channel opens done given the current constraints of the Bitcoin Layer 1, right?
I feel like this is a question that comes up a lot with Lightning.
Again, that assumes that those X billion people aren't using centralized service providers that are managing those channels for them, but rather that they're all self-sovereign and basically running their own Lightning infrastructure, et cetera.
So those are all questions that are useful and important for asking when you're looking at Lightning as a way to scale the number of Bitcoin transactions per second that can happen.
I think that if you kind of take Lightning and look at it as a view is what Jonathan, suggested, and that Lightning is a technology for contracting and for building payment networks that are decentralized and hopefully more anonymized, then if it's decoupled from the L1 in terms of the value you're transacting, and I'm not saying that there's plans to make that happen or anything anytime soon, but then I think these questions suddenly become a lot murkier and it's kind of a bigger, like, okay, is Lightning the technology and standard set of how you transact value over more generalized forms of cryptocurrency contracts or is it just the Bitcoin one?

## Lightning and the role of Taproot

Jeremy Rubin: 00:21:35

Cool, yeah, so I guess as we're kind of looking at where things are evolving to support more of that vision, who here has heard of Taproot?
Raise your hand, all right.
So we got a lot of people who've heard of Taproot.
If you haven't, Taproot is a recently activated new feature for Bitcoin.
And a lot of what I've seen online suggests that, like, Taproot fixes a lot of these things, and Taproot is really good.
So what's going on with Taproot and the Lightning Network, and how might this thing that has been activated, but doesn't necessarily mean it's deployed yet, how might that change the shape of what's possible?

Jonathan Harvey Buschel: 00:22:15

I could give some answers here.
So I think one thing that Taproot can fix, assuming it's widely deployed, is the privacy of channel openings.
So we have this on-chain footprint when we open a channel and we close the channel, and we have these scripts in there, right, to give some guarantees about refunds and making sure that we're like locking up the funds for the channel correctly and then exiting correctly.
And right now that is very obvious, right?
If you look on chain, you can find, you know, channel opens and closes.
But we can hide them by using a taproot transaction.
And then we get on-train transactions that look a lot like, other on-train transactions, assuming other wallets adopt Taproot, which they probably would.
So that's something nice.
Another benefit for Taproot is that we have this whole, like other way to embed information now in transactions and in channel updates.
So with this protocol, Taro to embed asset information in the taproot tree.
And the nice thing about that is that this doesn't impose a cost to people who aren't using it or to people who aren't participating.
And I'd be looking forward to see actually what other protocols come out that are embedding data in that tree or make good use of that.
I think right now we're still at the point where base libraries and implementations are adding support for Taproot.
And that will be done soon.
But then you also have to figure out how to upgrade the network, right?
So right now, we have a bunch of channels out there.
And ideally, we don't close every single channel and then reopen it with a Taproot funding transaction.
That would be a lot of strain on the network.
So there are some proposals as well to figure out a better way to upgrade the channel types so that we can better support Taproot use in channels overall.

Lisa Neigut: 00:24:22

I think to kind of build on one of the cool things about, so taproot in terms of privacy, I think the on-chain footprint part, it's actually only, I would say, like maybe 30% of helping hide where your channels are on the network.
There's a whole other thing that we'll have to fix that Taproot doesn't solve before we can improve that measurably at all, really.
However, moving over to Taproot in terms of privacy is good for decorrelating payment paths through the network.
So right now, if for some reason you had multiple nodes on the network and a payment got sent through multiple hops on the network, the data that you use to basically lock those funds into escrow as it moves across the network can be correlated.
By moving over to Taproot, I believe we're able to move over to something called PTLCs instead of HTLCs, which is a point time locked instead of hash

Rene Pickhardt: 00:25:24

time locked.

Jeremy Rubin: 00:25:24

What is an HTLC?
Can you start there?
I don't know what it is.

Lisa Neigut: 00:25:28

Yeah, hang on, let me finish this thought really fast, and then we can loop back around to what an HTLC is.
But the general idea then is with Taproot, you'd be able to use tweaks to use unique identifiers per hop, such that if for some reason someone's running multiple nodes, or your payment looped through the same node multiple times before reaching its destination, you wouldn't be able to correlate it to any other particular hop that it made, so to speak.
Yeah, okay, so what is a HTLC?
Rene, do you want to take this one?

## HTLC

Rene Pickhardt: 00:26:06

Sure.
I mean, HTLC is basically a contract that allows to make a conditional payment in condition with time constraints.
So what I do is if I want to forward a payment to you, I offer you an HTLC, which is a contract, and if you can provide a certain secret, then you can reclaim the payment, and after a certain time has passed, I can basically cancel it, and I can spend the output if you hadn't provided the secret in this time.
And the reason why this is useful is we use this to ensure that a payment is being routed atomically across the network because everybody is committing to the same payment hash.
And this is exactly what Lisa was talking about, that currently we can correlate these things.
And remember I said before that the payment process is a probabilistic process, right?
So when I want to send a payment via Lisa to you, Jeremy, it might very well be that there's not enough liquidity in the channel between Lisa and you.
So then I have to find another route to you, right?
And a lot of people might be aware about the payment at some point in time.
Yep.

Jeremy Rubin: 00:27:09

So like, if we're just like on stage and I wanna hand a quarter, which you know, we're using analog, fiat money, analog energy.
So if we want to use our analog energy and I hand a little lump of metal, what you're kind of saying is I don't let it go, but Lisa's holding onto it and then she hands you a piece, and then she lets go at the same time that I let go.
Is that sort of what you're explaining?

Rene Pickhardt: 00:27:37

Yeah, exactly.
So that's the idea, right?
I mean, if we go back to the example of the quarter, I mean, usually in the physical world, what would happen is you would give the quarter to Lisa and ask her to forward it, right?
Because, yeah, and then of course she could run with it.

Jeremy Rubin: 00:27:51

Yeah, I don't trust Lisa.

Rene Pickhardt: 00:27:52

Yeah, so that's why you keep your hand on it, and she has to have a second quarter that she gives to me, and she has to prove to you that she let go, and this is exactly how the secret of the hash is being released in the hash time lock contract.

## Difference between HTLC and PTLC

Jeremy Rubin: 00:28:06

And so when we go from HTLCs to PTLCs, like what's concretely changing under the hood?

Lisa Neigut: 00:28:14

Yeah, so I just wanted to like kind of maybe reiterate what you guys just said there's kind of this two phases of sending payments, right?
There's a commitment phase and there's a settlement phase. Commitment phase requires there to be like a hash which is like an identifier of that payment. Which also acts as a secret that gets committed to at every channel.
So if there's a channel between me and Jeremy, we would commit to that hash, we'd allocate funds, put them in escrow, and it's basically locked with that hash, so to speak, in a contract, such that the only way that we could get the money out is via a secret that matches that hash or through a timeout, basically, the money would exit escrow.
So there's two paths for money in a channel to exit escrow after it's been placed into it.
And that's what the HTLC kind of stands for.
It's the two ways that you can exit escrow.
It's either with a time lock, so it times out, or a hash.
So the same hash gets committed to in the contracts of the channel on every single channel that that payment touches, right?
And then as Rene was explaining, if at some point as the payment is being locked into channels, or basically committed to escrow in each of the channels as it makes its way in the commitment phase, so to speak, of a payment.
If it fails at some point, then those basically have to be rolled back, those commitments have to be rolled back along the chain.
And then you retry and you have to use the same hash.
That's just the way the payments work right now.
You have to use the same hash when you retry it because that's how the person you're paying is going to be able to effectuate the settlement after the contracts have been.
So you commit, the payment makes it all the way to the node that's able to furnish, we call it pre-image, but basically the unlock that will pull those funds out of escrow and each of the channels that it's been committed to.
So basically, you can't use a different thing on payment reattempts.
So to some extent, depending on what visibility and how many parties you're exposing that to, to some extent it exposes your intent of that identifier to make a payment, right?
So, PTLC is the ability that at every hop that you make, and I don't know enough about the proposal.
I think Andrew Poelstra was the first one to propose it.
I'm going to get that name wrong.
The cool thing about it is it allows you to have a separate identifier for every contract that you commit the funds to in escrow.
So every escrow key to unlock those funds is unique across every channel contract, so to speak, that the funds get escrowed in.

Jeremy Rubin: 00:31:20

So I'm a pretty disorganized guy, and it sounds like what you're telling me is before I had to keep track of a lot of stuff, and now I've got to keep track of even more stuff.
How much stuff are we talking about keeping track of, and what sort of stuff do I keep around and not lose, like my phone and keys and stuff?

Rene Pickhardt: 00:31:40

So there is this kind of like famous node coming on the Lightning Network currently that is called zero fee routing.
Because this person basically made the claim that for various reasons it might be useful to just have zero fees at all in routing.

Jeremy Rubin: 00:31:57

Well you got zero base fee on your shirt, is that your node?

Rene Pickhardt: 00:32:00

No, no, no, no, zero base fee is a different thing, right?
There is the fee rate and there is the base fee.
But what this person did is basically, the person said, well, I charge for people to open channels with them, right?
So I provide them liquidity, so there they're actually paying me.
But while I'm routing the payments, I'm not charging anything anymore.
And of course what this person does, it just undercuts the market, because currently most implementations make their routing decisions based on fees.
And the reason why I'm telling this story is this guy recently made a tweet of saying, my channel database is growing at like five to something gigabyte per day.
Yeah, so that's a lot of stuff.

Jeremy Rubin: 00:32:38

So, and that's a five gigabytes that he has to keep around forever?
Or when can he like delete it?

Rene Pickhardt: 00:32:45

When the channel closes, of course he can delete some of the stuff, because then he doesn't have to remember anything anymore.
But as we just discussed before, if we want to onboard a lot of people on the Lightning Network, we do not want to open and close channels all the time.
So yeah.

Lisa Neigut: 00:33:00

I think, is this the thing that we call toxic waste?
I think that's the topic of the Lightning topic.

Jeremy Rubin: 00:33:07

Yeah, maybe, I'm just trying to figure out, like if I go to Best Buy, I could buy a terabyte or two for 100 bucks, so am I going earn 100 bucks for, is this guy making a hundred bucks a day?
Because then maybe he can just go to Best Buy.
I might have a coupon.

Rene Pickhardt: 00:33:22

So, I don't know his financials, but I know that he takes something like initially 2,000 PPM to open a channel.
So that's like 0.2% of the liquidity in the channel and he guarantees the channel to be open for one or two months, I think. I think he recently increased the prices and changed something.
I don't know but yeah,

Lisa Neigut: 00:33:42

I think we're conflating a bunch of different topics here all at once. So maybe we should like.

Jeremy Rubin: 00:33:47

You want to break it down a little bit?
What's going on, where are we off the rails?

## Cost of opening and closing a channel

Lisa Neigut: 00:33:51

Yeah, so we were talking about how expensive is it to open a channel, and what helps cover that cost of opening a channel, right?
Which you guys brought up a node that's pretty famous on the Lightning Network called Zero-Fee Routing, which famously doesn't charge any money to route payments through it, right?
So the big question with his node tends to be, okay, if he's not charging money to route payments, opening and closing channels has a physical, like real world Bitcoin cost in the Layer 1, you have to pay an on-chain fee to open and close a channel.
So if this node is not routing, is like not making any money by moving money, like moving Bitcoin across the channels that he's opened, is he just net losing Bitcoin every time he opens and closes a channel, I think is one part of it.
That's distinct from the toxic waste part that we were talking about a little bit earlier, which is that has to do with the amount of state that your lightning node individually needs to keep track of and on disk and for how long for all of these payments that happen and why that is, et cetera.

Jeremy Rubin: 00:35:04

Got you, so I guess if I could restate it, there's no amount of money that would make me not lose my keys every time I'm at home and I put my keys somewhere.
So there's a question of how much money would you pay to solve this problem?
And there's a question of like can people actually solve this problem?

Lisa Neigut: 00:35:20

Wait, okay, so can you restate the question about the keys thing?
I don't quite follow.

Jeremy Rubin: 00:35:24

I just mean like you know like you go home and then you like you know lose track of your stuff or like, you get a you know in this context a database corruption. And so there's really a question of things that economically might be in your interest to pay for and things that are just like, even if they're in your economic interest, might be operationally hard for you to do, like not losing your belongings.

Lisa Neigut: 00:35:44

Yeah, I feel like This is yet a third kind of topic with Lightning stuff.
Yeah, which gets into the, what do you call it, like recovery of funds or like, I have funds that are committed to lightning channels.
You know, with Bitcoin, I know if I lose my keys, I'm in a lot of trouble.
On Lightning, what is the equivalent of losing your keys for Lightning, right?
Like that's kind of like, I feel like what you're asking.

Jeremy Rubin: 00:36:10

Yeah, I think a bit.
And then, you know, the follow up is like, is there anything we can do about that?
But start with whatever.
Because earlier I was convinced that I wanted to put all my Bitcoin into channels, now I'm not so sure, so how might we rectify that?

Lisa Neigut: 00:36:25

Right, I see.
And so you're not sure you want to put all your money into channels because of the cost of deploying it?

Jeremy Rubin: 00:36:31

Well now I heard I've got to go and buy a five gigabyte thumb drive every day.

Lisa Neigut: 00:36:34

I see.

## Risks and tradeoffs

Jeremy Rubin: 00:36:34

And you know also that if I lose that then I'm going to lose all my money.
So like now I'm like I'm a little bit more skeptical.
So like how might we get around those problems?

Lisa Neigut: 00:36:43

Yeah so I think some of the some of what kind of Jeremy's talking about is this kind of the construction of the way that Lightning works is you have your money locked into channels, right?
So one general class of, okay, what do I need to remember?
What kind of state am I storing?
Is the first most basic step is, okay, who do I have channels with?
Let's pretend the private key material that you use to update the contracts that make Lightning channels, right?
Like the Bitcoin transactions.
So you have a key that signs those.
Okay, let's say you've got that.
You know how to store keys.
You've successfully stored this key.
Your Lightning node goes down.
All of the data on your Lightning Node is wiped, right?
Okay, first thing you probably need to figure out and would be good information is to know which peers you had contracts with, right?
The way that Lightning contracts work today is that they're two of two signed contracts, which means you basically enter into a Bitcoin transaction agreement with another peer, that there is an output on the Bitcoin blockchain that both of you must create signatures in order to spend that output.
So any transaction that spends this output on the Bitcoin network, that is Lightning channel.
That output in the transaction set that must be signed by two parties, and those are your channel peers, right?
Okay, so you still have your key, but you don't know who you have any channels with, you're in a lot of trouble, because you don't know who to go back and ask, hey, I need you to sign something for me, right?
So even if you could magically recreate all of the transactions that you had signed, or that maybe you know, for some reason, you know what all of your outputs are, so you've backed up what keys are, and you've backed up what all the out points are, unless you can figure out what the other party of that two of two was to sign those outputs so you can get your funds back, you're kind of out of luck, right?
So that's kind of, I think, the first layer of information that you need to remember about a Lightning thing, right?
So your funds are out there, but there's another party and you need to remember who that is because if you lose all your stuff then.

Jeremy Rubin: 00:39:01

That one sounds kind of fundamental.
Like there's nothing we can do to make that better.

Lisa Neigut: 00:39:05

I don't think so, yeah.
I mean if you just not lose your stuff in the first place, that would be pretty good.
But yeah.

Jonathan Harvey Buschel: 00:39:14

So there are alternate channel constructions, right?
So right now we have like the original kind of paper from Tadge and Joseph that the amount of state and like toxic waste we need to keep, right, is linear in how many updates we do, right?
So the reason that that zero fee node probably has so much state to keep track of is like for every payment that is routed through them, for every channel update, they need to store that kind of indefinitely until they close the channel.
And there are alternate constructions like L2 where the amount of data that you'd need to store is kind of static, right?
So you just store basically the latest state and I think some extra information and you would be able to get kind of the same security guarantees there.
I think that's an upgrade that isn't deployable right now.
It's still kind of far down the road, but that would help a lot in terms of what you need to store and not reducing what could be forgotten, but at least kind of the risk and the resource requirements.
And that also would be helpful for thinking about like clients, what can I do with some device that's like my phone or something that's intermittently online or that doesn't have a lot of storage, can I participate?
I think that's also helpful in that respect.

Lisa Neigut: 00:40:34

So I think what Jonathan was talking about then is like, after you know who your channels are, there's a whole other set of information you need to save, which becomes this toxic waste thing, right?
I don't know.
I mean, I don't know if Jonathan's going to answer.

Jeremy Rubin: 00:40:49

So it sounds like a little bit of what you're saying is like, if I am going to a bar and I'm going out like drinking with a friend, I would just need to remember who bought the last round.
I don't need to remember the history of all of our drinking sessions, because I'm already drinking, I'm not going to remember.
I might write down in my wallet on one business card who got the last round, but I'm not going to keep a record of every time we went drinking.

Lisa Neigut: 00:41:11

Yeah, so let's talk about why that is, though.
Yeah, so like Jonathan mentioned, the current construction uses, I think they're called Poon-Dryja channels, is the technical name of the current implement protocol that channels use.
And the way that it works is that every time you update the current state of the money in a Lightning contract between the two parties, you kind of have to remember almost every previous state and also in order to invalidate, so you have state updates on this contract, right, and the state that you're updating is the amount of balance of who owns what between the two parties in that channel.
Every time you update that state, the way that you prevent your channel party from publishing an older state such that they can't roll back time basically to a state where maybe they had all the money in the channel and then they paid it to you over like 10 updates, so you're now at the 10th update, but then they go back and publish the first update such that now they have all the money again and that's what's officially on record on chain and so they spent money but didn't actually spend the money because they were able to get it back on Layer 1.
The way that the Poon-Dryja channel construction helps prevent this problem is by issuing something that we call a revocation key is the technical name for it, that kind of makes each of those past transaction states sort of like toxic waste for the other party, such that if they ever publish an older state, that is what gets committed to chain, and that the other party then has this key that allows them to take all of the money that was originally locked into the two-party contract, so to speak.
So, the waste is toxic in the sense that you can't get rid of it.
If you accidentally forget what the most recent state was and publish an older state to chain, it exposes you to complete and total loss because your channel peer is able to take all that money out of the channel for themselves.
So then if you do have this database backup, like total loss that we're talking about, even if you are able to figure out who your peers are, in order to continue using that contract and not have to do an emergency shutdown or whatever, you basically can't because you don't know what the current state is, so you don't have any information that you can then keep advancing it.
Also, you're at a lot of risk at that point at your channel partner publishing a past date that you don't have the ability to revoke the keys from, etc.

## Summary

Jeremy Rubin: 00:43:50

Okay, so I think unfortunately we're basically almost out of time here, as if somebody can tell me if that's the case.
Yeah, so we're going to wrap up.
I guess just sort of trying to summarize and synthesize from everything that I'm hearing is that Lightning as it is today, we're gonna be able to get to maybe a million, maybe 10 million people or something like that who are able to self-sovereignly host themselves, maybe a lot more, who are gonna be able to use services that are maybe of good reputation, and those services themselves will be completely self-hosted, and maybe that's a way of bringing in a lot more people.
Unfortunately, it's difficult with what we have today to actually run one of these services at large scale and might require a lot of storage.
You're at a very competitive marketplace where your competitors are willing to do the work you're trying to do for money for free.
And so that might be very, very tight and competitive if you're trying to make money out of it.
If you're just trying to send your own payments, maybe that's a better experience.
But there's a lot of exciting research that is going to maybe make the operation of that much better for the 10 million people that we could support.
And then in the future, maybe we're gonna focus on growing beyond that.
Would you say that that's like a summary of where Lightning is at today?

Rene Pickhardt: 00:45:05

Yeah.
Maybe.
Yeah, I mean, it's work in progress.
I think that's the important thing to note here, right?
There's still room for improvement, how I usually say.

Jeremy Rubin: 00:45:16

All right, cool.
Well, give a big thanks to our panelists.
