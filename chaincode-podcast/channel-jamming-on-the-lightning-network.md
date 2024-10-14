---
title: Channel Jamming on the Lightning Network
transcript_by: mvuk via review.btctranscripts.com
media: https://podcasters.spotify.com/pod/show/chaincode/episodes/Clara-Shikhelman-and-Sergei-Tikhomirov-and-Channel-Jamming-on-the-Lightning-Network---Episode-25-e1r78n4
date: '2022-11-23'
tags:
  - lightning
  - research
  - ux
  - watchtowers
speakers:
  - Clara Shikhelman
  - Sergei Tikhomirov
summary: Clara and Sergei stop by to chat about their recent proposal on mitigating jamming attacks in the Lightning Network. We talk unconditional fees, local reputation, the impact on decentralization and UX, and the state of Lightning in general.
episode: 25
additional_resources:
  - title: recent proposal
    url: https://research.chaincode.com/2022/11/15/unjamming-lightning/
  - title: Spamming the Lightning Network
    url: https://github.com/t-bast/lightning-docs/blob/master/spam-prevention.md
  - title: Preventing Channel Jamming
    url: https://blog.bitmex.com/preventing-channel-jamming/
  - title: 'Bitcoin Optech: Channel jamming attacks'
    url: https://bitcoinops.org/en/topics/channel-jamming-attacks/
  - title: The impacts of channel jamming
    url: https://jamming-dev.github.io/book/1-impacts.html
  - title: 'Bitcoin problems: Channel balance probing'
    url: https://bitcoinproblems.org/problems/channel-balance-probing.html
aliases:
  - /chaincode-labs/chaincode-podcast/channel-jamming-on-the-lightning-network/
---
Clara Shikhelman: 00:00:00

We identify the problem, we identify what would be a good solution, and then we go over the tools that are available for us over the Lightning Network.

Adam Jonas: 00:00:15

Hello, Murch.

Mark Erhardt: 00:00:16

Hi, Jonas.

Adam Jonas: 00:00:16

Back in the saddle again.
We are talking to Sergey and Clara today about their recent work on Jamming.

Mark Erhardt: 00:00:23

They have a paper forthcoming.

Adam Jonas: 00:00:25

We've seen some recent attacks on Lightning.
What's your general opinion about the Lightning network and its future stability?

Mark Erhardt: 00:00:32

I remain very optimistic.
Sounds like all of our problems are mostly engineering problems.
I stick to Rusty's opinion.
It'll take 20 years to bootstrap a new protocol.
We're only five years, seven years in, something like that.
So there's a little room there still but it's working already pretty well and we know of course of a bunch of ways how it breaks and is just not completely engineered out.
One of them is jamming.
Jamming is just a DOS vector on the network because a lot of the resources are provided for free still.
So when you have a channel, let's say we have a channel, we by default usually allow up to 483 slots in parallel for HTLCs. That means we can have 483 payments being forwarded in either direction in total.
And I think that's related to how big a transaction can be when we settle the channel on chain.
So either the slots are exhausted or the complete capacity of the channel is tied up in forwarding payments.
So you can jam up a channel by using up all the liquid capacity, or you can tie it up by using up all the slots.

Adam Jonas: 00:01:43

Got it.
So I think what's cool is that we have some solutions that are being proposed.
Some of the solutions sound super simple.

Mark Erhardt: 00:01:50

There was a big paper write-up by Gleb and Antoine a few months ago.
I looked a little bit at that, mostly just a summary.
It seems like after talking about the problem for years, people are getting a little more concrete trying to systematically suss out what exactly the good behavior is, what needs to be curbed.
Fees have been a large part of the conversation so far, and I think people have been very allergic, but also talking about reputation.

Adam Jonas: 00:02:20

These things really change the dynamics of how Lightning works currently.

Mark Erhardt: 00:02:24

You have to learn anyway.
When you're sending yourself, you learn which channels worked in a payment attempt.
And then if a channel was sent back a message that the capacity is exhausted in that direction, you remember that for a bit and you don't try that channel again, because you're just wasting everybody's resources.
But there's really the question of how do you make people pay for that?
Because right now everybody's just forwarding all the messages for free and if the payment fails it just falls back for everyone and their money was still tied up for the time. They still invested the bandwidth to forward the payments, but they only have opportunity costs and no earnings.
So there have to be ways to offset the service that is being provided by payment attempts.

Adam Jonas: 00:03:09

Yeah, that makes sense.
Well, we are bringing our heaviest academic hitters to talk about this problem.
And so looking forward to this conversation.
Hope you enjoy it too.

Sergey, Clara, thank you for joining us in the illustrious Chaincode Studio.
We are here to talk about channel jamming.

Clara Shikhelman: 00:03:32

Thank you for having us and thank you for choosing this topic.

Adam Jonas: 00:03:35

Let's start at the beginning.
What is channel jamming?

## What is jamming and why is it free?

Clara Shikhelman: 00:03:38

Channel jamming is using the resources in a channel, locking them up and rendering the channel useless for a short time.
The two resources you can use are either the liquidity available in the channel, that is the amount of Bitcoin that can be sent to the other node, And the other thing is the slots.
So there is a limit to the number of HTLCs or number of in-flight transactions that can be over the channel.
This limit comes from layer 2 issues, but the point is there is a limited amount you can forward, there is a limited number of transactions you can forward, and if you're forwarding a transaction and it is not resolved, this slot or this liquidity is locked and no one else can use it until you release it.

Sergei Tikhomirov: 00:04:37

I would like to like add a little bit on top of that.
So if you think of a route Alice to Bob to Charlie, so when Alice forwards a payment to Charlie through Bob, Bob has to put some trust into Alice.
So Alice essentially says, hey Bob, I wanna use some of the resources of your channel to get my payment to Charlie, but I cannot tell you exactly how long it will take and for how long your resources will be occupied.
So if I'm honest, I just want to get my payment across.
It probably will be a few seconds but I may be an attacker and I may be in like this malicious relationship with Charlie.
Charlie may be my collaborator in this attack and we may just hold the payment and hold your channel resources for a very long time and you have no way to know in advance.
So this is the problem.

Clara Shikhelman: 00:05:19

The magic of jamming for now is that you don't pay for failed transactions.
So you can send this transaction, lock up the resources, and then it fails because either the person receiving it is somebody that is working with you or you're just sending something random and taking up slots and liquidity and you don't need to pay anything you can keep doing that and doing that.

Mark Erhardt: 00:05:44

It's like a DOS vulnerability that allows a griefer to freely spend network resources, well not freely, They lock up their own liquidity too, but the price is extremely low because they don't have a permanent price.

Adam Jonas: 00:05:56

Let's sort of go back a little bit further than that and just talk about the general state of the Lightning Network.
Its general robustness versus things like channel jamming.
Matt Corallo gave a talk at TabConf about Lightning being very broken, but also has silver lining in that we can fix these things.
How fixable are a lot of these solutions and How optimistic or pessimistic are we about the health and future of the Lightning Network?

Clara Shikhelman: 00:06:20

So jamming now is pretty fixable.
We talked with the developer community and we got very good responses, so this is probably solvable.
There are other challenges in the Lightning Network that require more and more attention.

Adam Jonas: 00:06:36

So you've been working on channel jamming for the last few months, and we'd love to hear how you came upon this kind of project, and sort of how you got started, and where are you today?

## How our jamming project started

Sergei Tikhomirov: 00:06:48

So this project kind of grew somewhat organically from my previous line of research, which was channel-balanced probing in Lightning.
You can listen about that in the previous episode that we did in February, I believe.
This is a related issue that Lightning Network experiences, Not more of a privacy, but more of a denial of service type of attack.
And we've been thinking about how to address this.
There have been multiple proposals floating around, including all types of different fee structures or reputation schemes.
And we have been trying to come up with a systematic approach and think carefully about, okay, what are the pros and cons of different types of solutions?
What do we actually want from a solution?
And try to list all the, or at least the most important aspects that a solution should have in our opinion, and then go step-by-step and construct a solution, keeping among other things, we think it's very important to keep the simplicity of implementation in mind, because we aspire to come up with something practical, something that can be implemented in some reasonable amount of time, and not just be delayed once and once again for 10 years.
So hopefully we have achieved some result along these lines.

## Prior work on jamming

Mark Erhardt: 00:07:52

How does this relate to prior work?
We know that some other developers wrote up a big piece about channel jamming.
I think how does yours compare to that or how does it relate to it?

Clara Shikhelman: 00:08:04

First of all, we used a lot of prior work.
The first thing we looked at was Gleb Naumenko's blog post about jamming.
It was a very good systemization of knowledge work with other ideas, either his or things that were around the community.
So we definitely, you know, standing on the shoulders of giants, to use the cliche.
So we did read other works that people did.
We used a lot of it.
So our solution at the end is a combination of ideas that were floating around the community.
It was really great working on this because it was such a mature subject that was waiting to be resolved.

Sergei Tikhomirov: 00:08:47

There was lots of different proposals on the mailing list, on the blogs and whatnot.
And I guess the issue that we've been trying to address, compared or in contrast to these proposals, is to come up with something very practical and something that we hope is kind of thought out.
Because lots of the ideas that have been floating around, it was just some developer came up with an idea, wrote up a blog post and it goes along the lines of, okay, we could do something like this.
And there are like a few replies, okay, we could do something like that.
And then it kind of sits there for three years.
We hope that something more practical will come up of our results of our paper a bit faster and we hope that it's more kind of practical and we focus on the practicality as a very important design goal.

Clara Shikhelman: 00:09:35

Spoiler alert towards when we'll talk about the solution It ended up that we probably should be thinking about jamming into different styles.
And then to resolve each style, you need a different solution that was discussed in the community.

Adam Jonas: 00:09:41

Let's get into that.
So let's go into a few more details about how to deal with jamming in the future and what your research was like and then what solutions you arrived to.

## The desired properties of a solution

Sergei Tikhomirov: 00:09:50

So if we're talking about the method or the approach that we've taken, is that we've identified what we refer to as the framework in our work, where basically we have written down a few conceptually simple ideas, but we think they're important.
What do you want to strive for?
Even generically, taking a more broad view rather than just lighting, if we just talk about such decentralized financial networks in general, because there are lots of commonalities among these types of systems, there obviously are lots of attacks.
So what should we be thinking about?
What should we prioritize when we are coming up with some kind of contra measure?
Of course, it should be effective, as in it should do something to solve the problem, maybe even if not completely, but at least make it less desirable for an attacker to perform this.
But also we should think about user experience because we are targeting, hopefully, common people who will be sending their everyday payments, so it shouldn't be too difficult to understand.
We should think about security and privacy, be careful as to not introduce some new attack vectors while fixing older attack vectors, not reveal some private information about the participants, at least not to much greater extent as it used to be in the previous version of the protocol and so on.
So we list basically five or six such desirable properties and then we go in more concrete into the details of the Lightning Network in particular.
We list some design decisions or some questions that we ask ourselves, narrowing down our search.
So thinking about fees, what questions do we ask ourselves when constructing a fee scheme?
Who pays to whom?
In which currency?
Under which conditions?
To which amounts?
And we classify the proposals that have been floating around according to these categories, and then we say we prefer this type of solution to that type of solution, and so on.
And then we narrow down our search more and more until we come up with what eventually will end up in the solution section of the paper.
And then we do a similar thing in the second part of the solution, which is the reputation system.
Again, how can reputation systems be constructed to begin with?
Who assigns the reputation based on what criteria?
How these reputation scores may be increased or decreased?
And do nodes have to agree on what everyone else's reputation is or not?
And then again, answering these questions based on our priorities listed above, we come up with some solution that we think is reasonable and practical.
So this is the approach that we've taken.

Clara Shikhelman: 00:11:58

I think the TLDR is we identify the problem, we identify what would be a good solution, and then we go over the tools that are available for us over the Lightning Network.
So for example, the problem jamming, what we want from a solution is solve it, be easily implementable, and so on.
And the tools that we have are the reputation of our nodes in the network, or the fees that we're charging to forward payments.

Mark Erhardt: 00:12:27

Like throttling certain users, If a channel sends you a lot of requests, you would probably slow them down at some point?

## Reputation

Clara Shikhelman: 00:12:35

So not exactly, and we would love to dive into the reputation.
So in the reputation, each node assigns a reputation to its neighbors, that is, to other nodes they have a channel with.
Now, everybody starts with a low reputation, because I don't know anybody.
And then, for example, if Sergey keeps forwarding good HTLCs to me, and a good HTLC, it means that it pays a fee and it resolves quickly.
With time and with enough fees I start thinking, okay this Sergei, he seems to be doing good business, I already got this nice amount of fees from him, I think I can trust him.
For other nodes, I don't know them, I don't trust them.
Now, every time somebody sends me an HTLC, I first of all ask, is it from a trusted node?
And second of all, does this trusted node tell me that this HTLC is okay?
If this is from a good node that says this HTLC is a good HTLC, I will forward this using all of the liquidity I have and all of the slots.
But if I get an HTLC from somebody I don't know, or like a new peer, or from somebody I trust but is not willing to vouch for the HTLC, I will only allow a limited quota of slots and liquidity.
So anybody just opening a channel to me or forwarding HTLCs Cannot jam all of my slots and all of the liquidity in my channels 

## Centralization concerns

Adam Jonas: 00:14:11

Doesn't that have a centralizing effect? This sounds a little bit similar to the way that autopilot routing what is designed as in I choose people who the network is already familiar with and therefore if you're a business and you run a well-maintained node and you have been up for a long time, then you're going to have an obvious advantage against new nodes who are just coming online.

Mark Erhardt: 00:14:35

It feels more like a web of trust to me.
So you don't go to a third-party source and find nodes that have been vouched for by the network, but you build your own local reputation.

Adam Jonas: 00:14:47

I'm not arguing with that part, it just sort of seems like let's imagine this is implemented today and it doesn't really matter from a reputation standpoint what the network has done for the last five years.
But starting today, reputation matters.
And so you build this graph as to who's trustworthy and who's untrustworthy.
You can imagine that a year from now I come online and I want to get into your web of trust.
And so there is an inherent disadvantage to trying to enter the network a year from now than today.

Clara Shikhelman: 00:15:20

So I do want to point out that you don't rank the whole network.
The only people that you give a reputation are your neighbors.

Adam Jonas: 00:15:28

Neighbors or peers?

Clara Shikhelman: 00:15:30

Nodes you have a channel with.

Adam Jonas: 00:15:31

Right, okay.

Clara Shikhelman: 00:15:32

Yeah, anybody that you don't have a channel with, you don't assign them any reputation.
But it is true that coming into the network becomes slightly more difficult because you need to build a reputation inside of it.
But I think this is a reasonable price to pay before allowing somebody to use all of your resources.

Sergei Tikhomirov: 00:15:52

I just wanted to make a clarification also that we are not assigning scores to nodes.
I mean, we assign reputation to peers, but then eventually the decision whether to consider a payment good or bad, is localized on the payment.
So we are ranking each payment and the reputation score of the peer is one ingredient that comes into this.
We're not trying to rank everyone globally and permanently.

Adam Jonas: 00:16:12

I could also imagine an extension of this is that someone outsources their trust.
So you could imagine that, let's say, Clara's been up and running for a year now, and I come online, and I don't want to start from the beginning, and therefore I borrow her graph, or I use a lightning service provider who's bootstrapping a new node, borrows a graph from another place.
All I'm saying is like by creating reputation, you are creating a footprint as to who's trustworthy and who's untrustworthy, and you just don't know what the long-term effects of that might be.

Mark Erhardt: 00:16:42

I mean, borrowing a graph sort of gets the wrong picture for me in my head.
You might be asking, oh, can this one peer be a good peer for me?
Because somebody else says, oh, yeah, I know them.
Well, I've been working with them for a year.
So you might open one channel with that peer, but you're not borrowing the whole graph, especially since it's only scores for their neighbors.

Clara Shikhelman: 00:17:07

Exactly, so you can't really borrow a graph.
The only place where reputation comes into play is when a neighbor is offering you an HTLC and you need to decide whether to forward it or not.
You also, because of the onion structure in the lightning network, you don't know where this came from.
You just know this comes from this direct neighbor and you can rank other nodes in the graph as much as you want, but you don't know that it came from them.

Adam Jonas: 00:17:33

I guess, again, I'm just pushing back on this because I want to understand, can something like this end up on 1ML and therefore be scraped and people use that to make their own form, their own future decisions?

Clara Shikhelman: 00:17:44

So there is now some global reputation websites on the Lightning Network, which I am, to say the least, not a huge fan, but you can't stop people from doing this.
And I think because this is something very local, I think it's much less dangerous than the other things we see floating around.
I do want to emphasize that if you're starting a business as a routing node, it will be more difficult to compete with nodes that already established themselves and have some trust.
That being said, I think it's a small price to pay to protect the network from different attacks.

Mark Erhardt: 00:18:23

I mean, it also sounds like it would be very reasonable to make a meatspace business connection to someone and say, look, I'm bootstrapping my business.
I'd like you to open a channel with me, and you know who I am.
Maybe that can allow you to initialize my trust connection a little higher.
Like nothing prevents that, right?

Clara Shikhelman: 00:18:42

Yeah.
And also for small users just joining for some everyday kind of moving money and things like that, you would probably never need a high reputation.
You won't need a lot of slots and you won't need a lot of liquidity.
So you can live your happy life sending a bit of money from time to time.
Nobody suspects you as a jammer, you never need like the huge liquidity or take up a lot of slots or things like that.
So at least for the small users just hanging out and sending some money, I don't think they would even feel this change coming in.

Adam Jonas: 00:19:17

Cool.
So besides reputation, what other ideas do you have to help solve this problem?

## Unconditional fees

Sergei Tikhomirov: 00:19:23

The fees.

It has been discussed a lot in the Lightning community, and the key word here is upfront fees.
We use a somewhat more generic term, unconditional fees, because strictly speaking, they can be paid upfront or they can be paid like in the end of the payment cycle but doesn't matter very much.
So the general idea is that currently jamming is essentially free as we've discussed previously because only successful payments pay the fees as the difference between what a routing node forwards and what it has received from the upstream peer.
And because jams always fail, they don't pay anything.
So this makes jamming very cheap because the jammer only pays for channel establishment, some capital lockup costs potentially, but not actual money.
So we suggest to change that, and we've considered multiple proposals that have been suggested.
We think we have come up with the most simple and practical idea, which is basically just pay upfront a little bit or pay unconditionally a little bit.
We've also inherited the same structure of the fee amount.
So currently the success case fee is composed of the base fee and some amount proportional to the amount of the payment.
So we suggest doing basically the same thing with the unconditional part.
But as we show in our calculations and our simulations, this unconditional part can be rather small compared to the success case fee.
And the way I think about this is that a channel usually has hundreds of slots, so there is a magic number 483, which is the maximum number of slots one channel might have, which means the maximum number of in-flight payments that can be at the same time in the channel.
So if a jammer wants to jam a channel, the jammer has to send hundreds of payments every few seconds.
So now we're in the world of quick jamming.
Slow jamming has been addressed by reputation.
Now we're in the world of quick jamming, where an attacker tries to send jams that are difficult to detect because they mimic the behavior of honest payments.
Because honest payments also fail with some probability, and the jammer just pretends, oh, it was just an honest payment.
And because of the onion routing we don't know where the payments come from, so we cannot connect them to the same jammer.
So what do we do?
So the solution, or what we propose, is to charge a small fee.
And because the jammer is sending hundreds of jams every, say, few seconds, for the jammer it would be noticeable, whereas for the honest users, it will be barely noticeable.
And as a scenario for our simulations, we have shown how high can these fee coefficients be in order for a routing node to essentially not notice the difference between the attack case and the honest case.
So imagine a routing node that has been earning some honest fee revenue from some flow of honest payments.
And then we have some assumptions about what is the distribution of amounts of these honest payments, how frequent they come through.
So we have some amount of satoshis per minute that the honest node has been earning.
So then if we impose an unconditional fee on every gem, then the routing node would be earning also some amount of revenue even under the attack.
So we calculate that it's sufficient to have the failure case payment as low as 2%, or it depends on the assumption about the honest payment flow, but the kind of number that we put into the abstract or something is 2% paid up front.
And this already will fully compensate the routing node for the damage that the jamming caused.
From the point of view of the routing node, it would be kind of all right.

Mark Erhardt: 00:22:34

Just to be clear, 2% of the final fee, not 2% of the sent amount, right?

Sergei Tikhomirov: 00:22:39

Yeah, it's not 2% of the amount.
It's like we had payment of 100 Satoshis, the success case fee is one Satoshi, and the conditional fee would be 0.02 satoshi, something like that.

Adam Jonas: 00:22:50

And you think that that's enough?

Clara Shikhelman: 00:22:51

It's enough for the routing node to be compensated.
So it doesn't, for the attacker, maybe they're okay with paying that.
So we can't assume that there is some limit on the funds of the attacker.
But what we can take care of is that a routing node or a node that relies on fees, which are nodes that would suffer from jamming, will be compensated.
So when it comes to their revenue, they're like, okay, either business as usual or I'm being jammed.
Like the money keeps flowing and sure.
Why not?

Mark Erhardt: 00:23:23

What would be the mechanism by which the unconditional fees are delivered?

## How are unconditional fees delivered?

Clara Shikhelman: 00:23:28

So with HTLCs, usually you lock some money and then you say, okay, if the payment resolves successfully, the money goes to the peer downstream.
And then if it fails, all of the money releases back to the peer, which was upstream in the payment.
Now, thanks to Sergi Delgado, we have a really nice POC showing that by changing two lines of code instead of in a resolution, either all of the money goes downstream or upstream, we have a resolution where if something fails, not all of the money goes back upstream.
There's like a small amount that goes downstream.
This is the unconditional fee.

Mark Erhardt: 00:24:14

They've been talking about upfront fees and whatever other fees for years and you can actually just resolve it in rolling back to HTLC asymmetrically.

## UX implications

Clara Shikhelman: 00:24:24

I don't know that the problem that people were facing or the main challenge was the implementation.
I think there was a lot of worry of how much do we need to charge for this to be meaningful and there's also the UX problem because it's going to be not trivial to either explain to people that are going to pay for a failed service, or to hide this inside of the wallet, to create the wallet in a way that, at the end, users are happy.

I'll be happy to elaborate on this a bit, because I think the UX is the most interesting problem when it comes to upfront fees.

Adam Jonas: 00:25:02

Yeah, go ahead.

Clara Shikhelman: 00:25:02

So the thing is, the upfront fees are very small, but still it's unpleasant to pay for something if the payment fails.
So we're thinking about two kinds of users.
There's the one user that understands the Lightning Network, knows what's a jamming attack, and then they go, okay, so this is really such a small amount that sometimes I'm being charged, or whatever.
But then we have the user that hardly knows what's the Lightning Network, never heard about jamming, never wants to know anything about jamming.
So to them, wallets would oftentimes resend the payments if they fail.
And then we can tell them, OK, so the maximum amount of fees you're going to pay is going to be X.
And you calculate this X based on, I don't know, you need five attempts to guarantee a success of 99.9999% and then you're like, okay, this is going to be maximum this.
And more often than not, the fees are going to be less than that.
And explaining to somebody you ended up paying less than you planned to pay, this is usually something which is easier to do.

Mark Erhardt: 00:26:10

So basically you ask the user to upfront give you a budget how much the payment can take, and you overestimate a little bit the cost that it would take to get the payment through and you use a little bit of that for the unconditional fees and the multiple attempts that you might take until your payment goes through.
The rest goes to the regular fees for making all the HTLCs be compensated.
Yeah, it makes sense to me.

Clara Shikhelman: 00:26:35

And again, the unconditional fee is going to be such a small percentage from the total fee that it's not going to be meaningful anyway.

Mark Erhardt: 00:26:43

I've also heard that the number of attempts on the Lightning Network to get payments through has drastically shrunk in the last couple of years.
So 2020, I think people were just getting payments through occasionally and had to at least try 10, 20 times and with various improvements of how paths I found, how people learn about the graph from previous attempts, it's gotten much better.

Adam Jonas: 00:27:07

So how hard is this to turn from paper to fixing things?

## Moving research results towards implementation

Clara Shikhelman: 00:27:13

Well give us a few weeks and Let's see what the community says and if somebody is taking this up.
I think one of the challenges is going to be that everybody in the Lightning Network community is very busy doing very important things.
For example, getting better routing, getting more success.
So working on these kinds of things is always tricky because it's not happening now.
We just want to take care of something before it happens.
So we are doing some work and we feel that people in the community are enthusiastic about it and interested in this.
We just need to hope and push them a bit to make sure this will actually go through sometime soon.

Sergei Tikhomirov: 00:27:55

As far as I understand the intermediary step that must happen between the paper and the actual code being written is spec.
So someone should write up what concrete fields in Lightning messages should change, because obviously if we need payments being endorsed, there must be some additional fields, something must encode its length and value and whatever, very low-level details that are necessary for it to be adopted.
And while conceptually, I think it's quite simple what we propose, there are lots of low-level details must be figured out to implement everything securely.
And another point that I want to make is that while fees do require quite a bit of protocol modification In different aspects like peer-to-peer messages and nodes exchanging version messages and saying I support this, I don't support that, the reputation part can be thought of as quite localized.
It doesn't require much network communication and it allows for more experimentation on individual node levels.
So I won't be surprised if it turns out that professional nodes already do something of this nature.
In any case, this provides a framework for nodes to experiment and set the parameters according to their risk preferences.
Do they want to trade off and accept more high risk payments expecting higher expected fee revenue at the risk that some of these payments may turn out to be jams.
So it's up to individual nodes to decide and potentially this part won't require that broad of a developer consensus but still it would require some.

Mark Erhardt: 00:29:14

So Does this also help a little bit with probing maybe?
Because with probing too we had or have the problem that it's essentially free.

## Effects on balance probing

Sergei Tikhomirov: 00:29:22

Yeah, this also addresses or has some impact on the probing problem because the probing attack as well as the jamming attack is based on the fact that the attacker is sending lots of like quote-unquote fake payments or like payments that don't carry economic value but instead are crafted in a way as to for the attacker to gain some information in the case of probing or to bother people and block their channels in the case of jamming.
So if we put some cost onto sending these fake payments then the attack would be discouraged at least to some extent.
It's not absolute.
And also it must be noted here that not everyone thinks that probing is bad per se, because as far as I understand, in the developer community, when people talk about probing in Lightning, What they mean is that wallets save information that they got from the network while they were trying to make unsuccessful payment attempts.
They know which channels fail and they remember their balance estimate for some remote channels which is useful for payment delivery.
But I think that there is a distinction there.
I don't think it's bad.
If you're trying to send a payment and you remember the result that you got back, it's kind of okay.
It would be stupid not to do that.
But a different thing is to actively send fake payments to collect this information, especially when it doesn't even concern your immediate interests in sending the payments.
You're just trying to probe the network and see everyone's balances.
That can be considered an attack.

## Lightning as a messaging network

Mark Erhardt: 00:30:37

Of course.
Also there was a big discussion last year about Onion messages.
There was a big blog post that dove into whether or not the Lightning Network will become a messaging system.
And one of the concerns there too was that it's free and that the burden or the cost is basically externalized on the whole network.
Is this cheap enough that onion messages can happen but maybe it's still expensive enough that it's not going to flood the network too much?
Or would it have to be more expensive to interact with that as well?

Clara Shikhelman: 00:31:08

So I think this is the point to say that what I say represents only my views and so on.
But no, the Lightning Network should not be a messaging network.
But also, yeah, the upfront fees will mean that you need to pay something to send a message, and I don't think anybody is into that.
So in one sense, this means that this would be a pushback against the Lightning network as a messaging platform.
But I don't see this as a bad thing.

Mark Erhardt: 00:31:36

I meant it as a good thing because obviously there's a cost associated with a lot of onion message routing and this would give you a knob to say how much you charge for forwarding.

Clara Shikhelman: 00:31:48

If somebody wants to pay to send messages over the lightning, sure.

Sergei Tikhomirov: 00:31:53

I agree here that messaging is not the primary use case.
Lots of engineering work is being done to address this use case that we all think about as payments, so carrying messages that carry some economic value and economic meaning.
And kind of downgrading this into simple message exchange is kind of, I mean, the whole protocol becomes kind of an overkill at least in my opinion.
But of course if people are ready to pay for it, then who are we to prevent them if they pay the market price.
Somewhat reminds me of Bitcoin OP_RETURN stuff and putting things into outputs, but on layer one you kind of burden everyone else for eternity to store this data, which is kind of not very friendly if we're thinking about peer-to-peer ethics, so to say.
In Lightning, it's a bit better because you only burden the nodes in the route whose resources you occupy while your message is being passed through.
But still, I think this is not the intended use and we shouldn't optimize for it.
Maybe we shouldn't actively discourage this, but we shouldn't make decisions to make it easier.

Adam Jonas: 00:32:49

Does this play at all with the rise of watchtowers and the uses of watchtowers?

## Effects on watchtowers

Sergei Tikhomirov: 00:32:54

There is some similarity in the question of watchtower incentivization and our proposal, especially the fee aspect.
In the watchtower, as far as I understand the watchtower debate, there is a question of how to incentivize watchtowers So on the one hand we want watchtowers to be incentivized to get the money if they're doing the job. On the other hand we want to prevent the watchtowers from taking the money or taking the prepayment and just not doing their jobs or question of how to link the payment or how to link the fee being paid to the fact of a tower doing its job is kind of an...
Probably I shouldn't say it's an open question because it's kind of clear how to implement this, it's been implemented as far as I understand.
So there are certain similarities in this two-part structure where we have some fee paid up front that provides some initial incentivization for the actor that we want to perform some action, be it routing a payment or watching the chain and disputing the chain.
And then the rest of the payment, the rest of the fee is conditional.
It depends on whether the service has actually been provided.
So there might be some similarities and there might be some cross-pollination between these problems.

Clara Shikhelman: 00:33:56

I also want to comment that with watchtowers, the less spam you have, the less difficult is the work of the watchtower because they just need to keep less information.
So having a cleaner network is going to be useful for that also.

Mark Erhardt: 00:34:10

Have you gotten any in-house review so far?

## Reviews and feedback so far

Clara Shikhelman: 00:34:14

Yeah, Carla that just joined Chaincode and I hope will appear on the podcast sometime soon, was of great help.
In general, I expect that, at least personally, the Lightning Network research flow is going to be oh so much easier now that I can just like pop my head and ask like, "BOLT7, what exactly?", and things like that.
So yeah, that was really great.
I think we named some people in the thanks section in the paper and there were a lot of people that gave very, very valuable comments.

## Future research ideas

Adam Jonas: 00:34:47

So what's next?
Future work?
What happens after this?
You said you're waiting on some reaction from the developer community.
Are there other proposals you plan on putting forward?
Yeah, what happens in terms of future work on this?

Sergei Tikhomirov: 00:34:59

Yeah, so maybe we should list a few ideas that we list in the future work section in the paper and that have been floating around and that we don't directly include into our solution but we think may be worth exploring and if there are some researchers listening they may take this as a topic of their next paper or research project.
For example, the idea that has been proposed is, can we make the amounts of the fees that are being paid proportional to the time that it actually took the payment to resolve?
So speaking from the kind of generic economic standpoint, if I provide some resources, it's kind of natural to take the fee proportional to the amount of resources that are being occupied.
But it's not obvious how to implement this because we lack a trusted time source, or at least a trusted time source with enough precision.
We could look at the Bitcoin blocks.
Maybe it could be a solution, but Ideally we would like something with a second precision, it's not obvious what could we use.
Maybe we can introduce additional trust assumptions and peers, I don't know, trusting each other on the time.
So if Alice says this completed in seven seconds, Bob said it completed in 10 seconds, they could come to some kind of agreement.
But again, it's an open question.
Would be nice to achieve this.
It would allow us not only to fairly price the jamming HTLCs, but also account for the fact that there are protocols based on Lightning or similar ideas that use the HTLCs that are held for a long time as a natural part of their protocol, such as discrete log contracts that resolve one way or the other depending on what the oracle says, so they are kept in flight until the oracle says what actually happened in the real world, or some kind of swaps where on-chain funds being swapped for off-chain funds, and again the HTLC in the Lightning is being held until the on-chain funds are sent the way they should be sent.
So it would be nice to price these fairly proportional to the time it is actually being held for but again it's a research topic.

Mark Erhardt: 00:36:45

Would it perhaps be possible to at least price the amount of time that the timeout is?
Because you can make your HTLC shorter or longer in the get-go, so if you're requesting your HTLC to have a very long timeout period, you might need to pay more upfront fee.

Sergei Tikhomirov: 00:37:01

That could be part of the solution, yes.
So if you declare that my HTLC can only take up to one hour, it's cheaper.
If I declare it can take up to 10 hours, it will be more expensive.
Yeah, that makes sense.

Clara Shikhelman: 00:37:12

Although in general, I think that If the amount of time that you're willing to accept is an hour or something like that, you can already reject saying, okay, this HTLC for two weeks, like I'm not going to even touch it or something like that.

## Privacy-preserving reputation

Sergei Tikhomirov: 00:37:25

Yeah.
We've also list as a potential future research idea, exploring something along the lines of reputation.
And again, in the ideal world, wouldn't it be nice to allow the sender to prove or to test some kind of proof to the payment that will prove that the reputation of the sender is good enough without revealing who the sender is?
Something zero-knowledge proves, Maybe some cryptography can help us.
We haven't explored very deeply this direction, but again, for someone who is interested and well versed in cryptography and interested in this problem, this might be part of the solution.
Another thing that we list regarding the fee schemes, A few more complex fee schemes have been proposed.
The keywords are bidirectional fees or refundable fees, fees that are being paid upstream or downstream depending on some conditions.
Again, there can be some more research work here to classify or to come up with some rigorous framework, how to classify the solutions, how to analyze them from the game theoretical point of view, who pays whom, under what conditions, and what's the final payoffs, and can we make these ideas distill some implementable and practical proposal out of that.
So it's also its potential future research direction.

Adam Jonas: 00:38:33

What was it like to do this kind of academic research on something that was mostly developer griping for many years?
Like how do you pick something like this up?
How do you formalize it?
Like what is the academic process look like and how does that differ from the mailing list blitz and sniping from the sidelines?

Clara Shikhelman: 00:38:51

So I think a lot of things that were added to the paper, the motivation was from time to time, like, okay, we're going to send it to a conference, there's going to be a reviewer, A reviewer is going to read this and they are going to catch us.
So with the knowledge that there are going to be people that are focused on reading this paper, just to look for a way to not accept it to a conference, this gives you a lot of motivation because sometimes in mailing lists people go through an idea and look at it, but they're not against you. Which is not a bad thing, but I feel that there's something rough in the academic world that makes you be very, very careful, write things properly, check things properly.
So I think it's good.

Adam Jonas: 00:39:39

But do you think that the reviewers that are actually gonna be reading this paper for that conference are gonna understand the value that you're providing or the nuance in which you did this?

Clara Shikhelman: 00:39:48

That's always on us.
That's why there's an introduction.
In the introduction, we explain why did we choose this problem, why is it interesting.
It's a very general framework that we used here, can be used in other solutions.
So it's really up to us to convince them that this is, first of all, an important problem, an interesting problem, and that this is a good solution.

Sergei Tikhomirov: 00:40:10

We don't expect reviewers to be hardcore Bitcoiners and be, you know, like, 100% convinced that Bitcoin is important and bringing the humanity forward.
But if they are computer scientists who understand the value of a scientific approach, we hope that we've convinced them that this problem is important enough and interesting enough and the solution is innovative and substantial as to present some value in the academic world as well, but of course being practical to the Bitcoin implementers world too.
So we hope we found this balance.

Clara Shikhelman: 00:40:39

And I think there are people that build their whole career by breaking things.
So before we build something, it's good to give it to people that enjoy breaking it and see if we got something completely wrong.
It's good to know now than in like three years or something like that.

Adam Jonas: 00:40:58

Cool.
Any final words, any thoughts, next steps, next projects?

Clara Shikhelman: 00:41:02

I'm working on a few things that have to do with the basics of the Lightning Network.
There's a paper that is already out that has to do with the costs of channels, decisions, when should you go to the Lightning Network, when should you stay on chain.
The second part of this work is coming out where we discuss the implications on the topology of the Lightning Network.
So all the things you're worried about centralization with this solution, somewhere at the back of my mind, I'm like, oh no, the centralization problem is just centralization is so much cheaper.
There are some projects also in the Lightning Network space about how to push back from centralization, how to motivate people to do things slightly better.
Yeah.

Adam Jonas: 00:41:46

Well, thank you for joining us and telling us all things jamming.
There's a movie from the 80s called Spaceballs and in it there is a reference to someone throwing jam at their communications and it comes through the antenna onto the screen and he takes it off the screen and looks at it and says, we've been jammed.

[Movie Clip Audio:] "Sir, the radar, sir, it appears to be jammed".

So it's a little hard to get that out of your head once it's in your head.
I'll put a link in the show notes so that you know what I'm talking about.
Thank you.

Sergei Tikhomirov: 00:42:17

Thank you.

Clara Shikhelman: 00:42:24

Thank you.

Adam Jonas: 00:42:25

All right, Murch, do you think we're going to solve channel jamming?

Mark Erhardt: 00:42:29

I think this sounds much more hopeful than I had anticipated in advance.
This idea of folding back an HTLC asymmetrically and some fees just always staying with the forwarder, that seems the kind of simple and brilliant that was missing to just have a way of encumbering each attempt with a very, very small cost.
Sort of like the Tobin tax.
It's not enough to really restrict any economic behavior, but it is enough to restrict the high frequency useless stuff.

Adam Jonas: 00:43:00

What's the Tobin tax?

Mark Erhardt: 00:43:02

Somebody suggested a Mr. Tobin, I presume, many years back, 20, 30 years ago, a way of getting high frequency trading not to be done as much and causing these booms and busts because the algorithmic trading just shoots itself into a specific corner.
You would put in extremely small, like less than maybe a thousandth of a basis point on each trade, and it would be enough for these extremely fast strategies to be encumbered by cost.
So people would still do arbitrage if there's really a gap, but they wouldn't be moving pennies back and forth in order to just make use of the frequency.

Adam Jonas: 00:43:41

So Tobin tax for lightning sounds amazing.
So to speak.
Any other thoughts?

Mark Erhardt: 00:43:45

Well, nice to have some people from the office on.
We should get a few more people on.

Adam Jonas: 00:43:51

Yeah, we're gonna get some more people on, you know, promises promises.
But we're working on it, we got our best people on it.
Thanks for listening and we'll see you next time.