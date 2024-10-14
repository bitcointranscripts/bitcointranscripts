---
title: Lightning privacy
transcript_by: markon1-a via review.btctranscripts.com
media: https://podcasters.spotify.com/pod/show/chaincode/episodes/Sergei-Tikhomirov-and-Lightning-privacy---Episode-19-e1egh3e
date: '2022-02-17'
tags:
  - lightning
  - research
  - security
  - topology
speakers:
  - Sergei Tikhomirov
summary: Postdoc Researcher Sergei joins Murch and Jonas to talk about channel balance probing in Lightning, privacy concerns in general, and the importance of researcher-developer collaboration.
episode: 19
additional_resources:
  - title: Sergei's homepage with links to all prior research
    url: https://s-tikhomirov.github.io/about/
  - title: '"Twitter for your bank account" meme'
    url: https://twitter.com/hdevalence/status/1484413227026960384
  - title: Analysis and Probing of Parallel Channels
    url: https://eprint.iacr.org/2021/384
  - title: StackExchange answer about transaction size limit
    url: https://bitcoin.stackexchange.com/a/35882/31712
  - title: Overview of anti-jamming measures
    url: https://blog.bitmex.com/preventing-channel-jamming/
  - title: On the Difficulty...
    url: https://eprint.iacr.org/2019/328
  - title: An Empirical Analysis
    url: https://arxiv.org/abs/2003.12470
  - title: Counting Down Thunder
    url: https://arxiv.org/abs/2006.12143
  - title: Congestion Attacks
    url: https://arxiv.org/abs/2002.06564
  - title: Cross-layer Deanonymization
    url: https://arxiv.org/abs/2007.00764
  - title: Flood & Loot
    url: https://arxiv.org/abs/2006.08513
  - title: Hijacking Routes
    url: https://arxiv.org/abs/1909.06890
aliases:
  - /chaincode-labs/chaincode-podcast/lightning-privacy/
---
Sergei Tikhomirov: 00:00:00

It reminds me of the conversation about end-to-end encryption, like the companies like Facebook, for example, that try to kind of turn this conversation about privacy from, okay, I want my conversations to be private from Facebook, towards, oh, we're encrypting end-to-end, and no one except you and Facebook knows what you're talking about.
I think we should aim for even more ambitious target to make it private even from the owners or from the operators of this whole garden.
This is what peer-to-peer protocols are about.

Caralie: 00:00:42

Hi everyone, welcome to the Chaincode Podcast.
My name is Caralie and I am very happy to be back sitting here with Jonas and Murch.
Hi guys.

Jonas: 00:00:49

Hey Caralie, welcome back.

Mark Erhardt: 00:00:50

Hey there.

Caralie: 00:00:51

Thank you.
It's been a long time.
Who are you guys talking to today?

Mark Erhardt: 00:00:55

Well, today we're going to talk to Sergei.
He's our new colleague at Chaincode.
He's been doing his PhD and he's been looking at lightning stuff a lot, channel probing especially with the focus on what happens if you have multiple parallel channels between two peers.

Jonas: 00:01:14

So yeah, we'll talk about his research and also just sort of get into the weeds on Lightning and privacy.
And we haven't done a Lightning episode for a while, so it's hard to have an expert back on.

Caralie: 00:01:24

Nice.
Well, I look forward to listening.

Mark Erhardt: 00:01:25

Hi Jonas.

Jonas: 00:01:29

Hey, Murch.

Mark Erhardt: 00:01:29

What are we doing today?

Jonas: 00:01:36

Talking to Sergei.
Sergei.

Sergei Tikhomirov: 00:01:39

Hey, what's up?
Glad to be here.

Jonas: 00:01:40

Tell us a little bit about yourself.
How did you make your way to Chaincode?
What are you doing here?

Sergei Tikhomirov: 00:01:46

I'm doing research now at Chaincode.

## Sergei's background

Sergei Tikhomirov: 00:01:49

I've been interested in Bitcoin for quite a while.
I've done some research at the University of Luxembourg.
I did my PhD on Bitcoin and other related, blockchain-related topics, so to say.
I've done some smart contract research, some Bitcoin peer-to-peer research, and for the past, I would say three years, my main focus has been layer two protocols on Bitcoin, in particular Lightning.
I'm interested in privacy in Lightning, reliability and the related topics, which are kind of entanglement of different trade-offs that we will try during this podcast to untangle a little bit, I hope so.

Jonas: 00:02:22

Yeah, that sounds cool.
Most recently, what kind of work have you been doing in terms of the academic research you've been up to?

Sergei Tikhomirov: 00:02:31

My latest project that I've more or less wrapped up for now, it resulted in a paper called Analysis and Probing of Parallel Channels in the Lightning Network.
And perhaps it's worth taking a step back and explaining just basics of Lightning, and then I will explain what the problem is that we've been focusing on.

## Lightning basics

Sergei Tikhomirov: 00:02:50

So I'm sure many of the listeners are familiar with that, but to put everyone on the same page, I would just say that Lightning is an additional network, an additional protocol on top of Bitcoin that allows for very fast payments and that utilizes Bitcoin scripts in a very clever way to make it very secure with some kind of additional security assumptions.
But I would say they do not diminish security very much.
So the point is that Lightning nodes form a network and Alice can send a payment, not only to Bob, with whom she has a direct channel, that is some coins locked up into a multi-signature account.
But also Alice can send money to Charlie through Bob using what is called multi-hop payments.

## Why LN payments fail

Sergei Tikhomirov: 00:03:38

And this is the essential functionality of Lightning.
But the problem with this approach is that these channels that pairs of nodes may have between each other, they have the capacity, that is, the total number of coins that is locked into the channel.
And also, the two nodes have their respective balances, which is how many coins Alice currently has, how many coins Bob currently has.
And the amount that a particular channel can forward on behalf of someone else depends on the balance on the respective side.
So if Alice has three coins, Bob has seven coins, it means that Alice can only forward up to three coins towards Bob, and Bob can only forward up to seven coins towards Alice.
And the remote node who wants to forward through this channel only knows the total capacity, only knows that there are ten coins in the channel, but doesn't know how they are distributed.
That's why the sending node is never sure whether the payment goes through or not.
If the balance is not enough, the payment is rejected and the sender has to start over, has to select a different path and try a different path.
So this is kind of a reliability issue, but what I've been looking at is the attack that is based on this mechanism, which exploits this mechanism in a sense.
And the attack basically allows revealing balances in remote channels, which is a privacy problem.
And the balances are not announced, they are not broadcast.
So it seems that it could be a good idea to keep them private and maintain a high level of privacy in the Lightning network.

## Why privacy is important

Jonas: 00:05:19

So you've said the word privacy a bunch in that description.
Why do you think that privacy is important?
And maybe as we zoom back a little bit and think about maybe, you also mentioned trade-offs in your intro.
What are the trade-offs between the different layers and what are the trade-offs in terms of how Lightning is constructed?
And where does privacy fit into that compared to the other goals of Lightning?

Sergei Tikhomirov: 00:05:48

So generally speaking, I would say that privacy is a very important property of a money system, which we are trying to develop here with Bitcoin and additional technologies such as Lightning on top of.
Bitcoin, if we don't have privacy, then in the worst case scenario, it means that everyone knows about everyone else's affairs, about everyone else's monetary situation, which is just bad.
And It's bad for business, bad for just human dignity in some cases.
And it opens the door to abuses of power, to discriminating against people based on their transactions.
And this is something that we are trying to avoid and build systems that are resilient to that.
And in terms of Bitcoin, there has been lots of research about Bitcoin privacy since 2013, maybe even earlier.

## Privacy potential of Lightning vs L1 Bitcoin

Sergei Tikhomirov: 00:06:40

People have been writing about clustering transactions and labeling transaction clusters.
And there are huge companies like Chainalysis built on top of this premise that monetize on this expertise and sell basically the service of de-anonymizing users.
Bitcoin privacy on layer one is kind of more or less understood.
We understand what's bad about this and it can be to some extent improved using techniques like mixing, coinjoins and so on.
But with Lightning, we have a different set of tradeoffs, a different system.
I see a huge potential here for privacy because Lightning is a layer two network.
And as I explained before, payments go through a path of nodes from the center to potentially some intermediary nodes and to the receiver.
Nodes outside of this path don't even know that the payment is happening.
There is a contrast here on layer one.
Each transaction is broadcast to everyone and every node validates it and miners include it in a block and all the transactions are stored in perpetuity in this distributed database called the blockchain.
It can be analyzed years and years down the line.
In Lightning, this is not the case.
So first of all, we have this very good baseline for privacy, which is transaction only happens between peers and some intermediary nodes.
But on the other hand, there are some new privacy challenges that layer one doesn't face, such as protecting the balance of the channels.
So on the one hand, nodes do not advertise their balances, and it just seems to me logical that if I run Lightning node, by default, I want to keep my balances private because this is part of my private financial information.
But As it turns out, and as we have, okay, we haven't discovered it, it has been discovered before, we kind of built on top of previous work and I will explain it in a bit, like what exactly does that mean.

## How probing works

Sergei Tikhomirov: 00:08:39

But the probing attack that we've been focusing on allows an adversary to reveal the balance of some remote channel by sending a series of fake payments that we call probes.
And these payments are fake in the sense that in the normal course of operation in Lightning, the receiver first creates some secret, the payment secret, then sends the hash of the secret to the sender.
The sender creates a series of contracts, which are called HTLCs. And then the receiver can reveal the secret and claim the payment, which ensures atomicity.
So this is how this normally works.
But of course, there's no way to tell a hash of some value from just a random string of bits.
And this is exactly what the attacker does.
So the attacker or the prober creates payments targeted at the victim node, just selecting a random value instead of the payment hash.
And of course, such payments cannot succeed, they will fail.
But the question is how exactly they fail.
So there are two scenarios how this payment will fail.
The first one, if it gets through the whole route towards the receiver, and the receiver looks up in the database and says, I don't know the preimage of this hash, something must be wrong, and I reject this payment.
This is one scenario.
And another scenario is if somewhere along the route a balance is insufficient in an intermediary channel.
And then this intermediary node would say, I don't have enough balance to forward this probe, because intermediaries don't know that this is fake, they cannot distinguish between a fake random value and a real hash.
And therefore they will propagate the error back to the sender so that the sender knows that, okay, this channel doesn't have sufficient balance, so I should avoid this channel and choose another route, another path around it.
And the prober distinguishes between these two error cases, between these two error messages, and can therefore understand whether the balance...
There are kind of two scenarios.
Either the attacker connects directly to the target channel, and then the attacker can make the following observations, that the balance in the target channel is either greater than the amount of the probe or less than the amount of the probe.
And repeating this process in a binary search, the attacker can narrow down the range of the estimates to basically arbitrarily low value.
If we don't account for dust limits, don't account for fees, but basically, very precisely, the attacker can learn the balance.
In a more generalized setting, the attacker can do the same thing through a multi-hop path, so the target node would be the last one, but also the attacker will get some information along the way about the intermediary nodes, whether they have sufficient balance or not.
So this is the basics of probing.

## Why is balance discovery bad?

Mark Erhardt: 00:11:34

So what's the problem with being able to find out exactly what the channel balance is?
How does that reduce the privacy?
Because everybody announces their channel already having X amount of balance and whether it's on the left or the right side, how is that an issue for the users?

Sergei Tikhomirov: 00:11:51

First of all, the nodes, when they establish a channel, they do not have to advertise a channel.
This is a voluntary activity.
And when you open up explorers like explorer.async.io or other Lightning explorers that report number of channels and nodes, this only reports the public nodes and channels.
And If I'm a Lightning user, I do not have to announce my channel at all.
But even if I do announce it, that kind of assumes that I want some payments to be routed through me and potentially earn fees from these routing operations.
Still, there is just privacy to my financial situation.
I mean, similarly to Bitcoin on layer one, I wouldn't want some third parties whom I don't know.
I don't know what they're up to.
I don't know what other information they have on me.
I don't want them in general to know the balance of my Bitcoin wallet and to connect my seemingly unrelated addresses to just one identity and link it to some exchange address or something.

## Persistent identities in Lightning

Sergei Tikhomirov: 00:12:56

Another way in which Lightning is, I would say, less private, or at least this is a consideration that we have to make, is that the identities of nodes in Lightning are relatively persistent.
So contrary to Bitcoin nodes, if I establish a Bitcoin node, I exchange some data with other peers, it doesn't matter very much which peers I connect to, as long as I'm not fully eclipsed, as long as I have at least one honest connection to the real Bitcoin network, then by comparing the proof of work, I will know which chain is the heaviest, which chain is valid.
Contrary to that, in Lightning, when I establish a Lightning node, I create an identity, a node ID, and then if I establish a channel to some other node, then this connection is persistent.
We have locked up some coins, and I remember the node ID of my partner, and my partner remembers my node ID.
And on top of that, oftentimes I also advertise my IP address in addition to my node ID or linked together with my node ID, which is also a huge step towards potentially de-anonymizing my node.
This doesn't have to be the case.
It is possible to use Lightning through Tor, and many nodes do establish Tor connections, but not all of them.
And this is something also to think about.

Jonas: 00:14:24

Yeah, I mean, we're certainly getting a little bit off of the topic of probing, but I think the idea of persistent identity versus ephemeral identity is an important one to recognize.
And then based on that, I think that goes back to Mark's question, is if you have a persistent identity and you are trying to establish yourself as a good member of the network, then showing that you have a large balance actually is a helpful way to do that.

Mark Erhardt: 00:14:54

The point that I was actually getting at is, if you are able to track which balances change at what time, and you can pinpoint the channels that were involved in the routed payment.
You can actually de-anonymize who paid whom, what amount.
And I think it'll be hard to keep a probing attack on the network stable to that degree where you can actually do this, but in combination with having a large number of the Lightning nodes, say certain blockchain surveillance companies recently announced that they're now monitoring Lightning network as well, if they have say a third of all nodes on it.
And in addition to having timing attacks when the payment goes through multiple of their nodes where the hash pre-image matches on multiple forwarding hops and the amounts also match.
And then seeing like certain channel balances change due to putting probing attacks out there, they might be able to tell.
The basic privacy assumption of Lightning, where the sender has pretty good anonymity because he is not revealing himself at all when he sends to the receiver, and the receiver having okay anonymity, depending on how many hops he's away because you cannot tell whether payment goes further than then the next forward or not. You might be able to to tell who was the last hop and how much they got and from whom.
That's where I was going.

Jonas: 00:16:35

This is where, again, we start getting into Taproot and some other pieces of revealing more information than you might otherwise.
Like a noob user might imagine, based on reputation alone, that Lightning is much more private.
But essentially this all ends up onchain.
And so when you have a balance that ends up on-chain, the timing and the...
What happens in the black box of sending lightning payments seems like that should be private.
But at the end of the day, it all ends up in a transparent way on the chain.

Mark Erhardt: 00:17:17

Right, although you don't know which side got which part, right?
You see two parts going out, or maybe even they split it in more ways when they close it and splice out at the same time.
And you don't know who got which part, but with a timing attack, or with a probing attack, you're able to...

Jonas: 00:17:36

In the same way you don't know which is the change that you get in the transaction.
I mean, machine learning can probably figure this stuff out.

Mark Erhardt: 00:17:43

To a degree.

## Multi-vector security model and trade-offs

Sergei Tikhomirov: 00:17:45

I mean, this is all a multilayered process.
There is no silver bullet and there is no one fix that we can apply either to Bitcoin or to Lightning and say, okay, now this is private.
Of course, there are multiple attacks and the more attack vectors we leave open, the more information the potential adversary can gather and combine together and so on.
So I think our job as protocol developers and researchers is to come up with ways to fix what can be fixed and what cannot be fixed.
Okay, we have to live with that.
We have to make some trade-offs and I will return to the topic of trade-offs.
I remember that part of the question, but yeah, I would say, sure, channels end up on chain sooner or later, but in the long run, we're all dead.
And if most of the activity is transferred to Lightning, and if channels are open and closed relatively infrequently, then the promise that your activity within this black box would be hidden is quite an important one.
But I would agree that this whole space is just trade-offs on top of trade-offs.
And in particular, if we talk about probing, of course, one can make an argument that if I'm a routing node, if this is my business, I want to earn fees, I want to avoid failures.
I don't want to fail other users' payments.
And therefore, it might make sense for me to advertise my balance in some way, or at least not defend myself against probing deliberately to let other users know that this is exactly how much I can forward so they know what to expect from me and I won't fail payments.
And probably we could envision some addition to the protocol or some additional protocol on top of Lightning that would allow nodes to willingly exchange this information if they want, if they want to give up privacy for the sake of better reliability or something like that.
I mean, who am I to disagree?
Who am I to say this is wrong?
But I think that by default, if users don't actively opt in into that, we should make our best effort to protect their balances and try not to ruin their assumption that Lightning is private or more private than layer one Bitcoin.

## Twitter for your bank account" meme

Mark Erhardt: 00:20:21

I actually find it a little scary.
For a long time we had that meme on Chain for Bitcoin to be a private payment.
And I think that quite a few people...

Sergei Tikhomirov: 00:20:31

I was going to say the meme of that Bitcoin is Twitter for your bank account.
There was a joke recently on Twitter that one of the Zcash developers made this joke on a conference in 2017 or 2018.
But then Twitter rolled out NFT support just recently.
And they have this disclaimer that by logging in into Twitter, you're linking your address to a Twitter account.
So they actually made the joke turn into reality.
This is something that-

Jonas: 00:20:54

We'll have to put it in the show nodes.

## The danger of overestimating Bitcoin's privacy

Mark Erhardt: 00:20:57

Okay, but what I was trying to get at was, it can actually be dangerous for users to assume that there's more privacy than there is.
So I think that maybe got some people into trouble before with onchain payments where they maybe were, I don't know, maybe a more benign example would be some women rights group in a country where that sort of thing is not allowed, receiving donations from abroad and thinking it's super private but it ends up not being as private as they think.
But so not only do we have to try to make it as private as possible, but we also have to be open about where it actually fails these promises so that people don't get misled.

Jonas: 00:21:46

Yeah, and I also think it starts becoming even more dangerous within the walled gardens of wallets and custodial wallets integrating Lightning.
So we have Lightning integration in Cash App now.

## Lightning integrations and walled gardens

Jonas: 00:22:01

And if you can imagine a beginner thinking that, well, I've heard Lightning is private, but I'm using it within this walled garden of Cash App.
It may not have all of the bells and whistles that you think it might.

Sergei Tikhomirov: 00:22:16

It reminds me of the conversation about end-to-end encryption, like the companies like Facebook, for example, at least as far as I can understand it, that try to kind of turn this conversation about privacy from, I want my conversations to be private from Facebook towards, oh, we're encrypting end-to-end, and no one except you and Facebook knows what you're talking about.
And this is kind of the way to put it to make themselves look good.
So the same with the walled gardens.
I mean, I'm not saying that Cash App is deliberately trying to push this narrative, probably they don't, but users may perceive it as, okay, everything is private within this world garden.
But I think we should aim for even more ambitious target to make it private, even from the owners or from the operators of this one garden.
So this is what peer-to-peer protocols are about.

## Lightning Service Providers and LN's centralized topology

Jonas: 00:23:05

Yeah, and I also think terminology becomes important here because as we're sort of pushing the label of lightning service providers versus users, that distinction is important of how you actually interact with lightning.
And I think, you know, I sort of, I stopped going to meetups over COVID.
So I sort of, when I reemerged, I kept hearing people talk about LSPs, but that really wasn't a thing in, early 2020.
Like now that is a way to describe how to interact with Lightning.
But that term wasn't being used all that much in late 2019.

Sergei Tikhomirov: 00:23:49

I think whatever term we use, the network is getting more centralized, or at least it was quite centralized from the beginning, as multiple research papers show the graph coefficients that show the distribution of nodes by their connectivity or by the amount of funds that they hold, the distribution is very uneven.
A very small fraction of nodes actually hold most of the value and are on the paths between the majority of like potential pairs of senders and receivers.
And this is, I mean, we may not like it.
We may have preferred kind of mesh-like topology, everyone connecting to their neighbors or something like that.
But to be fair, I don't believe this is economically viable.
And there are clear economic advantages to having kind of a hub-and-spoke-ish model where Lightning Service Providers or companies that are professional operators in the space, establish large nodes and provide good quality of service, good liquidity, and so on and so forth.
So I think we should be designing the protocol, keeping in mind that this is the likely organic evolution of the network.
It will be conceptualized.

Jonas: 00:25:06

But can't you both have the idea of this hub-and-spoke topology for people that need it, and then also the interconnectivity in a mesh, more private, more beneficial for edge nodes, kind of topology for other channels that you're establishing?

## LNBIG booth in El Salvador

Mark Erhardt: 00:25:25

Yeah, that's sort of the thing that makes me excited about Lightning network is, while there is participants that have invariably a higher balance and more nodes that they're connected with, if they start charging too much fees, the network will route around them because It's a peer-to-peer network where there is no power levels or anything like that.
A scale-free network.

Jonas: 00:25:53

There's some power levels because LNBIG had his...
I don't know.
Their booth in El Salvador is just an LNBIG booth.
I don't really understand what it was advertising.
But when I went to adopting Bitcoin in November, there was just a booth for LNBIG.

Sergei Tikhomirov: 00:26:16

With no one behind the booth because they're anonymous.

Jonas: 00:26:18

I didn't see anybody there.
But it was like there was a banner and it was...
For context, LNBIG is a huge market maker on Lightning.

Sergei Tikhomirov: 00:26:30

I think in 2019, they held 40% of the total capacity of Lightning.

Jonas: 00:26:35

So a lot of Bitcoin.
And now they're sponsoring conferences.

Mark Erhardt: 00:26:39

They basically just got really rich through Bitcoin, presumably, and wanted to give back.
And we're really excited early on already about the Lightning Network, from what I gather.
And for a while when you started a Lightning node, they'd just open a channel to you to give you inbound capacity of like significant amounts.
They changed their behavior since because so many of their channels remained unused.
They've gotten a little more selective.
But yeah, they still have a huge portion of the capacity on the network.

## Potential oligopoly of large nodes

Sergei Tikhomirov: 00:27:13

I just wanted to take a step back and mention the point that you mentioned about large nodes potentially raising the fees and we can always start to run them.
But I would say that my concern would be the opposite.
What if large nodes set very low fees and check the majority of payments and with their economic power and their quasi-monopoly or oligopoly status, they track the majority of payments and then it would become much easier for them to collude in the anonymized users or censor and ban users that they don't like, something of that nature.
I think this is something that we should be thinking about and protecting against.
And while, of course, the protocol is open and the implementations are open source, and of course, technically, you can establish a channel to whoever you want.
But the question is, how practical would it be?
And if most of the liquidity will be locked up in huge LSPs, of course, you could probably route $10 or $100 through your friends.
But if you want to route $1,000, it may not be possible, or it would cost many failed payment attempts or something like that.
The user experience would be potentially worse.
So this is something that we also should be addressing.

## Probing parallel channels

Jonas: 00:28:29

Do you want to circle back to the findings of your paper, since we've gone down a very different path.

Sergei Tikhomirov: 00:28:36

So returning to the probing, so if we agree that probing is a problem, the focus of our paper was the following.
So from the point of view of the attacker, okay, the basic construction has already been described in prior papers and it works well and it has been shown to work, but one complication that lightning topology may present for the attacker is the so-called parallel channels.
So the lightning protocol allows two nodes to share multiple channels between them, each with its own capacity, each with its own balance.
If the attacker wants to know what balance all these individual channels contain, it is, strictly speaking, not possible with the method I described earlier.
Because when the probe is being routed through this multi-channel hop, the node, like the first node on the path, is free to choose any of the parallel channels, whichever has enough balance to forward the probe.
So when the probe returns to the attacker, or rather when the result returns to the attacker, the error happened at the receiver or the error happened previously.
It is not clear which channel was that.
And okay, this is unclear.
But on the other hand, it would also be incorrect to say that the attacker gets no information.
The attacker gets some information, but no one bothered before we did, no one bothered to quantify it and to describe in mathematical terms exactly what the attacker learns in this case and how the attack can be optimized or adapted for the case of parallel channels.
And basically the two observations that we make, or rather, like first of all, in our paper, we introduce a new model that uses a geometrical analogy.
So we suggest correspondence between channels and dimensions.
So if we have a two-channel hop, it is like a two-dimensional space.
It's like a plane, and each point on the plane corresponds to some combination of potential balances in this channel.
So we have three channels, it would be a cube or what is it called, parallelogram, four dimensions, five dimensions and so on.
Of course, most of the examples are two-dimensional, just not to make your head explode.
So the first point is that, okay, the attacker has some area on this surface where, according to the attacker's knowledge, the true balance point may be.
And each probe makes a particular cut in this figure and narrows down the possible search.
So basically it's a generalization of binary search to n-dimensional space.
So we described this model, we have lots of beautiful pictures and diagrams that help you understand what's going on there.
I would say the key insight from that model is that three-dimensional space and higher is different than two and single-dimensional space.
So if we have just one channel, everything happens as I described earlier, we can probe the balance precisely.
If we have two channels, we have like points on a plane, then we can, like if we assume that we can probe the channel from both directions, then according to the geometrical model, we also can narrow down our search, like finally, ultimately, when the attacker does everything that the attacker can do, then we have what is left of this figure is just two points that correspond to the possible permutations of these channels.
So basically in the two-dimensional case the attacker also can learn precisely the two balances.
But what happens in three-dimensional and high-dimensional cases is that the final figure that is left after all the probes have been done and the attacker cannot do anything to learn more information, then still the final figure is some kind of either one-dimensional line or two-dimensional surface or high-dimensional figure.
So long story short, for three channel hops, four channel hops, five channel hops, and so on, it's impossible with this vanilla probing algorithm to learn the balances precisely.

## Combining probing with jamming

Sergei Tikhomirov: 00:33:00

But we suggest a way to fix it for the attacker, namely to combine the probing attack with another attack that also has been known, it just hasn't ever been combined with probing.
And the second attack is called jamming.
I should probably explain what jamming is shortly.
Jamming is a type of denial of service attacks on Lightning channels, and it works roughly as follows.
So as we described previously, the payment normally works in two phases.
So first, there is a series of contracts, which are called HTLCs, hashed time-locked contracts, that are created along the path.
So they are first created, and some coins are locked up in each of the channels, and they are released in one of two scenarios.
Either the receiver reveals the secret and claims the payment, and these contracts are revealed and the balance is moved towards the receiver.
So this is how the payment happens.
Or after some timeout, If the first scenario doesn't happen, then the coins can be taken back by the sender, by the next node, the next node, and so on, so the payment is rolled back.
But the attack is that if the attacker, who wants to block other users' channels, can create, or rather can initiate a payment between two nodes that it controls, and just fails to reveal the secret, then these HTLCs will be stuck for some time until timeouts expire.
And the timeouts can be pretty large on the order of hours or even days.
So this is quite nasty.
And there are two types of probing attack.
One assumes that the attacker has to have similar capacity to the capacity that it wants to block.
So if I want to block one Bitcoin in some channel, I have to have one Bitcoin in my own channel, which is quite expensive.
But the other type of jamming, what is called slot-based jamming, exploits another peculiarity of Lightning that is that at any point in time, like the security assumption and the security guarantee of Lightning is that at any point in time, any of the two counterparties can go on chain and take the latest state of the channel, put it on chain and get their money back, maybe after some timeout.
But if I didn't try to cheat, this is my money, I can take it on chain anytime.
And to make it happen, the transaction that encodes the current state of the channel must be below some limit in terms of buys, so that it fits into the Bitcoin consensus rules or policy rules, propagation rules, and so on.
It must be standard in other way.
And this limits the number of outputs that such transaction might have.
Therefore, it limits the number of so-called hanging HTLCs or in-flight HTLCs that the Lightning channel can have at any one time.
And there is only 483 in-flight payments.

## The limit on in-flight payments

Mark Erhardt: 00:36:10

Is that really limited because of the standardness of transactions?
Because transactions are standard up to 100,000 Vbytes.
So 483 outputs shouldn't be that large.

Sergei Tikhomirov: 00:36:22

Yeah, how many outputs should it be then?
Because I think I read this Bitcoin Stack Exchange answer that explained it this way, like 100 kilo.

Jonas: 00:36:31

Did Murch write the answer?

Sergei Tikhomirov: 00:36:32

I don't remember, that's why I'm asking.

Mark Erhardt: 00:36:34

Probably not.
Most of the lightning stuff was written by Rene.
Okay, so you have a limit of how many HTLCs you can have open per channel.
I think it's more of a sanity limit than an actual standardness limit.
And if you can fill up that whole limit.
Yeah, what can you do then?

Sergei Tikhomirov: 00:36:58

You can essentially block the channel.
So the liquidity will be locked up in this in-flight HTLCs and it cannot be used to forward any other payment until the HTLCs are resolved.
And this is what the attacker in the probing attack can take advantage of.
So if there is a hop that the attacker wants to probe, the attacker can send some jams first and jam basically all channels except for one and then probe the remaining channel.
And this allows the attacker to overcome this dimensionality issue and by probing channels one by one, it's possible to probe them all, at least in our somewhat simplified model, but roughly speaking, this is how it works.

Mark Erhardt: 00:37:50

All right, so your paper describes how you can still find out the balance of the two participants even if they have multiple channels between each other and you do it by jamming the remaining channels and then probing one of the channels for the exact balance and then moving through the channels accordingly to jam and all the others and measure the one that that's there.
So there's been this question that's been at the back of my mind listening to your explanation.
What would happen if every Lightning participant wouldn't allow you to route the full amount of the channel, but basically only ever allow up to the next discrete amount available in their channel.
To make it simple, you make 10%, 20%, 30% and so forth, just 10% steps.
And while your balance is between 51 and 59%, you always limit routing to 50%.
And when it drops below that, you limit routing to 40%.
Wouldn't this inherently limit the amount of information that you can extract with probing?

Sergei Tikhomirov: 00:39:12

Yeah, that's a good idea.
Basically, I think that can be a countermeasure.
I would agree that the probing attack, at least as we have it in our model, and as far as I'm aware, other papers have this as well.
So they assume that if the forwarding node can forward this balance, then it will forward this balance.
Modular fees, like you can try to account for fees, but basically, if technically I can forward this, I will forward this.
A potential countermeasure indeed could be that I will reject some of the payments that technically I could have forwarded.
Yeah, I mean, that could work, but of course it has its own trade-offs, right?
Because if I'm a commercial routing node, it means that I will reject some of the potential revenue from these payments.
And also if the attacker knows which exact pattern does the victim apply, like this rule about 51% to 59% or 50% something like that, then the prober also can, can factor this in into the calculations and extract some information.
But I mean, I don't have a direct answer.

Jonas: 00:40:24

That's to the detriment of the network, right?

Mark Erhardt: 00:40:27

I mean, it reduces the forwarding capacity, but it gets rid of...
So one other thing that comes to mind is probing has a legitimate and a mischievous use.
So legitimate use is you know you are going to route a payment in a moment and you start probing already whether you can find a path that will support your payment and then once you actually get the instruction to make the payment you execute on your already refreshed information and improve your user experience.
Maybe people or users configure their nodes to do this regularly with routes that they use a lot or whatever.
So they keep an up-to-date view of what paths they can use.
That seems like a legitimate use.

## Bad and good probing

Mark Erhardt: 00:41:19

I'm wondering whether if everybody did that, that would lock up a lot of capacity in the network already and reduce the routing capacity for others.
But The mischievous use would be, of course, to try to reduce the financial privacy of everyone and to learn the exact balances of channels and to perhaps even pinpoint who pays whom.
And that certainly would require an amount of probing that if, say, there's multiple different actors that try to probe the whole Lightning network, it would just result in a cacophony of failing payments.
So if we actually discretize our response to this, sure, we limit how much can be routed through us, but we might actually reduce the amount of probing that goes on and therefore make all the noise that comes with people trying to observe us much less and make Lightning more useful.
So here's my counter.

Sergei Tikhomirov: 00:42:26

I mean, it's kind of tricky when we're talking about peer-to-peer network.
I think in terms of we can do this or we can do that, we should always remember that this is a network of independent actors who pursue their own interests as they see them.
It may be purely commercial interests, it may be some malicious interests, or it may be some altruistic behavior.
We don't know.
But what I would say is that the situation when people think they have the privacy, but they can be easily probed, this is undesirable.
And we can kind of separate it into two scenarios for the cases that I want to reveal my, disclose my balance, reveal my privacy, or refuse to have privacy for the sake of reliability versus having as much privacy as possible.
On the other hand, as long as the protocol becomes permissionless, anyone can send payments, right?
And as long as the hash function is not broken and we cannot distinguish between a random number and a hash of some value, the forwarding nodes cannot distinguish between probes and honest payments.
So this is also that, like fundamentally, I don't see how this can be fixed.
And probing or some other activity that involves sending deliberately incorrect or invalid payments, I don't think we can prevent it fully.
However, one potential countermeasure, not directly against probing, but against just unwanted activity in general that has also been discussed, are think, I mean, there are multiple proposals that are often discussed in the context of anti-jamming countermeasures.
But if we make a point that jams and probes are just two subtypes of the type of unwanted traffic on the Lightning Network, we can say that anti-jamming countermeasures may mitigate probing to some extent as well.
And I'm talking about things like upfront payments or things like some kind of reputation-ish systems, which is a dangerous path, I agree, but whatever we think of that, it may merge organically, and maybe we should think about that and how to make it less bad than it would be otherwise.
This long we are saying that a future that I want to avoid for Lightning would be that everything is KYC, everything is like...
To open a channel to a large node, you have to prove who you are.
And the nodes have a very valid justification for that.
They would say, okay, if you don't, if you don't denonymize yourself upfront, then you could attack us, or you can forward some probes or jams or whatever malicious traffic through your node.
And because of the onion routing, we don't know whether it's you, whether it's someone else.
So please be responsible for the traffic that goes through you.
And we only want to open connections to trusted peers.

Jonas: 00:45:44

Yeah, I mean, KYC is a little bit loaded.
KYC is not necessarily showing someone your driver's license.
It can be pseudonymous, like knowing that someone is a good citizen of the network.

Sergei Tikhomirov: 00:45:55

Yeah, probably.
I'm not using this term very precisely, but identifying yourself in some way to even start using the network.

Jonas: 00:46:02

And that's already happening.
That's just node health metrics that are being used across various implementations.

Mark Erhardt: 00:46:09

Uptime, number of channels, total downloads.

Sergei Tikhomirov: 00:46:12

I think there is some kind of distinction between such metrics and something connected to my human identity or some corporate entity that I might establish.
So in terms of the metrics, everything I have to do to become a good citizen by these metrics is just run a node reliably and forward payments and follow the protocol and it's just my regular activity as opposed to disclosing some information that, I don't know, that I cannot withdraw that is not strictly within the bounds of the protocol, that links my protocol behavior to my behavior somewhere outside of the protocol.

Jonas: 00:46:54

Yeah, but you had already talked about sort of this bias towards hub-and-spoke topology.
And so that's going to lend itself to it being less decentralized and less trustless.
So if that's our future, it's for those that care about privacy, trustlessness, decentralization, then that may not be the kind of network you want to participate in, which is sort of going back to my previous point of, is there not a world of both?
Is there not a world of, the public nodes bootstrapping you and getting you to where you need to go in terms of channel connections, but also the world of private connections that maybe is less convenient.

Sergei Tikhomirov: 00:47:47

Yeah, I mean, I don't disagree with that.
I think there will be these two worlds, but I think like, we as protocol developers and researchers should make efforts to like, first of all, incentivize this privacy preserving world to be to be a bigger share of the total?

Jonas: 00:48:05

I agree, but we already have autopilots and things that are opening channels to large liquidity providers, again, for convenience, because we want Lightning to be a good user experience.
And so the more that that's done, the more of a self-fulfilling prophecy hub-and-spoke topology becomes, no?

Sergei Tikhomirov: 00:48:24

Yeah, I mean, again, I agree with that.
But topology is only one part of the question.
It might well be possible that we have a relatively centralized topology by some graph metrics, but still a very private protocol that does some advanced cryptography or something, or splits payments in a clever way and preserves privacy in the end of the day.
So we may have a centralized topology and a high degree of privacy.
I would hope so.

Mark Erhardt: 00:48:49

Yeah, for example, with multi-hub and PTLCs, you can have different relationships and like multi-hop payments that are not correlatable except for like the recipient.

## Hub-and-spoke terminology and aviation analogy

Mark Erhardt: 00:49:01

So I think even if we have, say, a superhighway in the center that is composed of a few supernodes, I don't like hub too much.
Supernode in the sense that a node has a huge balance and a lot of connections.

Jonas: 00:49:20

I'm sorry, why don't you like hub?

Mark Erhardt: 00:49:22

Hub-and-spoke sort of gives the impression that they're inherently different things.

Jonas: 00:49:28

Because they are.

Mark Erhardt: 00:49:29

No, they're not.

Jonas: 00:49:30

But that's what lighting service providers do essentially right now want to be hubs.

Mark Erhardt: 00:49:37

They do not have different privilege levels.
They operate more professionally maybe and they might have more influence or more utility, but inherently they have the same power level in the sense that everybody is using the same software, creating channels the same ways.
So I don't like to have unspoken topology because it gives the sense of there being different types of software that have different privilege levels?

Jonas: 00:50:03

I don't think privilege levels.
I agree with everything else you said, but the different privilege levels, in some ways they do, because they have better connectivity and they're operating in a different way.
That's not privilege levels in terms of access.

Mark Erhardt: 00:50:23

Not from the protocol level.

Sergei Tikhomirov: 00:50:27

The term is also used in aviation.
You have hub airports and smaller airports.
At least the analogy in my mind is similar to airports.
We have all the airports are licensed and planes can land on them, but some are huge hubs.
And if you go from between different parts of the country or the continent, you have to go through one of these big hubs.
And also you can, like, technically, if an emergency happens, the plane can land on some smaller airport.
Yeah, sure, but they are the same in terms of kind of aviation protocol, but they're not the same in terms of actual usage.

Mark Erhardt: 00:50:59

Sure, okay, fine.
Maybe I'm just getting that into the wrong pipe.

Jonas: 00:51:02

We're just quibbling back at you.

Mark Erhardt: 00:51:04

No, no, no, fine.
So one thing we're seeing a little bit already, at least my understanding is that some of the hubs are already limiting channels to have a minimum size so that some users just cannot open channels to hubs because they don't want to tie up that much funds.
And what we see is that people sort of get a multi-level hierarchy now, where there's a medium tier of hubs that connect to the actual hubs, so to speak.
And now they sort of guarantee that the traffic their routing is good.
But these sub networks, I think, that are created that way. If they become important enough, take the role of an actual hub or route around the actual hubs if there's some deficiencies there.
And so inherently it is a scale-free network that is self-healing if there's any shenanigans.
And if we look around how sentiment can be driven by narratives, I think also that hubs that, for example, obviously get sponsored in order to sell information and things like that would just not get routed through.
And maybe to a degree, Lightning could be self-mending.

Sergei Tikhomirov: 00:52:48

Yeah, I mean, I'm not sure how I can comment on that.
There are multiple potential futures.
And what you say is, I mean, I agree with that and it's logical, but no one knows how the future will pan out.

Jonas: 00:52:58

But that's why we have researchers.

Mark Erhardt: 00:52:59

Exactly.

Jonas: 00:53:00

To tell us how the future will look.

Mark Erhardt: 00:53:02

He can just be optimistic.
He can tell me, we don't know.

Jonas: 00:53:06

He can write a simulation and tell you.

## Doing research in Bitcoin and Lightning

Jonas: 00:53:09

Tell us a little bit about what it's like to do research in Lightning and Bitcoin generally.

Sergei Tikhomirov: 00:53:15

Sure.
I mean, this is fascinating.
I think that research, I mean, it's the way of thinking.
It's just scientific methods, so to say.
And it's just about being skeptical and analyzing things and trying to, before rationing and trying to implement something or rush to conclusions, try to understand, like first of all, formulate the problem and try to understand very precisely what it is that you are trying to understand.
Try to invent some metrics, try to come up with some specific questions, what you're trying to prove or disprove, and then try to create a model that describes the reality in some way and let this model help you find the answers.
And in particular in the Lightning and Bitcoin world, I think this is a very interesting and very promising research subject.
So if any of the researchers, including academic researchers, of course, and the universities listening to this podcast.
Please contact me if you don't know where to start and you want to do Bitcoin research.
I think this is a very nice topic because, first of all, it's an intersection of multiple fields.
And whether you are a cryptographer, a mathematician, a computer scientist, or economist, of course, someone closer to financial sciences and more of a social science, the social dynamics are also fascinating.
Bitcoin can offer you everything and everything is intersected and influences like different various parts of the ecosystem influence each other in fascinating ways.
If we focus more on the computer science side of things, and in particular security and privacy side of things that I have been focused on during the past years, this is fascinating because we have this permissionless network launched by some pseudonymous person.

## Why Bitcoin is unique

Sergei Tikhomirov: 00:55:18

No one knows who that is and where they are now.
And now it's evolving as a living organism and it just blows my mind.
I mean, everyone knows that, but just thinking about it, that we all work for and in this ecosystem that no one actually controls.
There is no one on top, there's no organization, there is no single entity that controls it.
And everything just might be a bit chaotic at times, but this is something that we should cherish and preserve.
Because this is a big reason why I'm focused on Bitcoin.
This is what makes Bitcoin unique.
Chaincode, as you might know, of course, is Bitcoin-only and Bitcoin-focused organization.
I'm not strictly a Bitcoin maximalist.
I also have my interest outside of the Bitcoin space, in other like blockchain stuff.
But Bitcoin is absolutely unique in that it has a very clear mission.
It has a very clear vision.
We want to implement basically digitally native money that is apolitical, that doesn't depend on any subjective decisions of any particular person or group of people.
And I think this mission is important.
I think Bitcoin has a very high chance of achieving it, at least to a large extent.
And this is what makes me excited and what makes me want to work on.
And research approach in particular is helpful here to make justified, long-term, focused decisions on protocol development.
So the developers write code and they're brilliant at this, but sometimes it's worth taking a step back and try to read up on the research that has been done even long before Bitcoin has been invented.
What were people thinking about?
Certain cryptographic problems, about some graph theory problems, economic problems, whether these can be applied to Bitcoin and Lightning.
And as long as the Bitcoin development and Lightning development also takes a long-term view, we don't want to just implement something very quickly and pump and dump.
We want to develop protocols that will live for decades or even centuries.
And this is where research is very helpful in making these decisions.

Mark Erhardt: 00:57:45

From a research perspective, I think one of the really interesting things for a lot of the involved fields is you can do research on Bitcoin that will actually get implemented and used.
And that's pretty exciting.

## Researcher-developer collaboration

Sergei Tikhomirov: 00:58:00

I would say on this note that this is what I consider part of my mission here at Chaincode to make researchers and developers talk to each other more because of course we would like to see researchers work on important problems that actual development faces.
And the other way around, the results that researchers achieve, we want to see them implemented into actual real-world systems.
But currently, this is often not the case.
And it seems to me that researchers are somewhat in their own universe, their own world, and they're working on problems that may not always be directly applicable.
And developers, on the other hand, partially because of this first problem, the developers also are not very aware of what's happening in the research field.
So I think it would be very helpful if these two groups of people collaborate more and developers submit valid problems and interesting problems to researchers, and researchers share their interesting and applicable and implementable results to developers.

Mark Erhardt: 00:59:09

You mean we don't need 20 more selfish mining papers?

Jonas: 00:59:12

Or better yet, you can just be Sipa and just do both.
Talk to yourself.
Be fine.

Caralie: 00:59:15

Thank you for joining us, Sergei, and excited to have you on the podcast here and have you at Chaincode.

Sergei Tikhomirov: 00:59:24

Absolutely.
Happy to be here.

Mark Erhardt: 00:59:26

Yeah.
Thanks for that.
It was interesting.

Sergei Tikhomirov: 00:59:29

Thanks a lot for the questions.
It was fun.

Caralie: 00:59:36

Well, that was a fascinating conversation.

Mark Erhardt: 00:59:38

I did like how we got into the weeds a bit here and there and went really beyond what his paper was about and looked a little bit at the broader privacy implications of on-chain and Lightning.

Jonas: 00:59:52

Yeah, I think sometimes when I read these research papers, one thing that strikes me is where did they get the context of whether this was an important problem or how are they thinking about things from a general framework and a wider lens?
And it's nice to talk to a researcher who's here to learn about that.
That's why Sergei's at Chaincode.
So yeah, good episode.
Excited to do more.

Caralie: 01:00:16

Yeah, thanks everyone.
