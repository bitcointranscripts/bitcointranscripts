---
title: 'Bitcoin++ Insider Edition: Super Testnet'
transcript_by: 'mokayaj857 via review.btctranscripts.com'
media: 'https://youtu.be/hv9Ckgeal88'
date: '2025-05-15'
tags:
  - 'mempool'
  - 'privacy'
  - 'lightning'
  - 'routing'
  - 'btcplusplus'
speakers:
  - 'Super Testnet'
  - 'niftynei'
categories:
  - 'security-enhancements'
source_file: 'https://youtu.be/hv9Ckgeal88'
summary: "In this Bitcoin++ Insider Edition interview, niftynei sits down with developer Super Testnet at the Bitcoin++ Austin conference to discuss the ongoing debate around transaction filtering and arbitrary data on the Bitcoin blockchain. Super Testnet advocates for aggressive mempool filtering to raise the cost of spam — including reducing the OP_RETURN data carrier limit to zero bytes — arguing that Bitcoin's block space should be reserved for financial transactions and that sustained resistance can push spammers onto other networks, much as it did after the Counterparty era. He frames both the spam fight and the broader altcoin debate as part of the same effort to preserve Bitcoin as sound money, and draws a parallel to Satoshi's original restrictive mempool design as a model worth revisiting.\n\nThe second half shifts to privacy improvements on the Lightning Network, where Super Testnet describes his current project to increase the number of routing hops between sender and destination as a straightforward privacy gain, and explains the use of decoy public keys in BOLT 11 invoices to avoid leaking node identity. He also briefly recaps his CoinPool work from Bitcoin++ Florianopolis, noting its potential to improve both privacy and scalability for Lightning users, before previewing upcoming talks on coin pools and privacy at the Bitcoin Conference in Las Vegas."
---

## Intro

niftynei:00:00:00

Hey Super, how's it going?

**Super Testnet:** 00:00:01

So good.

niftynei: 00:00:02

Welcome to Bitcoin++ Insider Edition.
Do you want to explain to the crowd who you are and what you're doing in Austin this week?

**Super Testnet:** 00:00:09

My name is Super Testnet, I'm a Bitcoin developer.
I focus on Bitcoin, the Lightning Network.
I do a lot of research into alternative Layer 2 solutions and I'm in Austin this week to come to Bitcoin++, which was a Bitcoin conference she just held, and present about one of my projects.

niftynei: 00:00:27

What project were you talking about?

**Super Testnet:** 00:00:29

It's called `Testnet Generator`.
It is a project where you can launch your own Bitcoin testnet and then have as many Bitcoins as you like, or fake Bitcoins, to test with.

niftynei: 00:00:41

Did anyone get testy during the workshop?

**Super Testnet:** 00:00:43

No, I don't think so.
I was really excited that Luke Dashjr came to it.

niftynei: 00:00:47

That was exciting.
That's fun, yeah.

**Super Testnet:** 00:00:48

He's a long time Bitcoin hero for me and he chose to come to my talk.

niftynei: 00:00:52

That's really cool, yeah.
Did you manage to spin up a test network during your talk?

**Super Testnet:** 00:00:56

Oh, yeah.
We did that within the first five minutes.
Very cool.

niftynei: 00:01:00

Then what did you do the rest of the time?

**Super Testnet:** 00:01:02

I added `CTV` to it.
So I went through how I, as an illustration of how I code, I had some `CTV` code and I added it into the testnet so you can create `CTV` transactions.

niftynei: 00:01:14

Very cool.
Cool.
Very cool.
So you talked about how Luke Dashjr came to your talk and you were excited that he was there.
What talks did you go to that you think they might have been really excited that you were in the audience for?

**Super Testnet:** 00:01:27

Well, I went to his talks, but I don't think he...
He probably doesn't know me, so maybe not that one.
This was also right before mine.
Let's see.

niftynei: 00:01:38

What was he talking about in that one?
Was that his policy changes?

**Super Testnet:** 00:01:41

Yeah, he was doing how to make your own mempool policies.
It was pretty cool, because we've been dealing a lot during the conference with new versions of spam on the blockchain.
So he was just like, let's just do an illustration of how fast it is to update the mempool to filter out more spam.

niftynei: 00:01:59

How fast was it?

**Super Testnet:** 00:02:01

He did it within 30 minutes.

niftynei: 00:02:03

Let's go.
Okay, yeah.
When he was talking to me about the talk, because I really wanted him to do that one, because I thought it was a cool demonstration of what the process is for making that kind of code change, he was telling me that he wasn't sure he could get it to compile in 30 minutes.

**Super Testnet:** 00:02:18

It did.
Yeah, I remember back when Counterparty first launched, there was new types of spam going on in the network back then.
And the Counterparty people were saying, like, you can't stop us, we can just add new things that you can't detect.
And at the time, he made this cool post where he was like, he updated his mempool policy, and he was like, look, it took five minutes.
I just added a line, and now I filtered your new type of spam.
And it reminded me of that.
It was like, it doesn't take much to actually fight this stuff.

niftynei: 00:02:46

Right, it just takes a little bit of proactivity.
I mean, so when you say fight this stuff, I had a tweet thread after listening to the talks about how really one side of the debate...

## Filtering Bitcoin Transactions

niftynei:00:02:57

A lot of stuff that we talked about at the conference was this filtering stuff.
I felt like that was more of a theme than I was intending it to be.
But one of the things I feel like there's kind of two positions.
One is that we can't fight it.
We should let them do it.
They're paying for block space.
So it's, you know, in terms of letting people pay for whatever data they want to get into a transaction, that's arbitrarily fine as long as they're paying for it and the transactions aren't spamming the network necessarily with number of transactions, if that makes sense.
And then there's, I think, the position that Luke and the Knots organization, for better or worse, I don't know if you call that Knots organization.

**Super Testnet:** 00:03:38

We call them Nazis.

niftynei: 00:03:39

Nazis.
OK, yeah.
The Knots, they're like, well, we should and we can fight it.
And here's how we're going to do it.
And we're digging in and going to do our best to prevent this type of data being written into the blockchain by filtering out transactions included.
Where would you say that you fall on that spectrum?
Are you like, we should continually update our filters and try to make it such that this data doesn't arrive at your node or is it, you know, we should let people write arbitrary data into the blockchain as long as they're willing to pay for it?

**Super Testnet:** 00:04:11

I'm a fan of the first one.
I like to fight the spam and try to eliminate as much of it as possible, increase the cost of production of spam and generally just make their lives harder so that Bitcoin is better money.

niftynei: 00:04:27

You think that like.
Like, yeah, do you think that filtering stuff out is a...
I mean, okay, so my understanding of this, though, is you know how when things are growing in the forest, they grow one thing and then a little predator comes along and eats it, and so then it grows spines and then you end up with flowers that are beautiful but you can't touch them because they're too poisonous or something.
Is there something, do you think, like my worry with like the constant evolution is that spammers are going to find new ways to put data into transactions.
Is it worth fighting the endless fight to make them more sophisticated and incentivize them to go around the mempool to get their transactions into blocks?

**Super Testnet:** 00:05:10

I think so.
Yeah, I think if it's a never-ending battle, there's nothing wrong with having a never ending resistance against it.
Perhaps instead of us being the ones to get complacent and just say, well, we can't fight it.
Perhaps they will be the ones to get complicit and just say, well, none of our attacks are working.

niftynei: 00:05:30

I see.

**Super Testnet:** 00:05:31

Yeah, I think for a long time that kind of did happen.
Like they're back when Counterparty launched, they were doing spam on Bitcoin for a while, but it kind of dropped off because Bitcoiners fought it and they moved to Ethereum.
And that lasted for, I don't know, all the way up until 2022 or so.
So I think maybe the same thing can happen.
If we fight it really hard, and if we succeed at stopping most of their efforts, then perhaps they will move to somewhere where it's more accepted and do it there.

niftynei: 00:06:00

Like, hey, the grass is greener somewhere else.

**Super Testnet:** 00:06:02

And then we get another eight years or whatever of...

niftynei: 00:06:05

Or spite.
Yeah.
I mean, a lot of these projects that seem to launch like spam stuff on the network or putting arbitrary data in seem to like have moments where they have like a bunch of transactions that get in, like they're buying a bunch of block space at a certain period of time, but then after that it seems like they really fall off.
I mean, you know, writing stuff into the blockchain isn't free, it costs money.
They're gonna run out of sats at some point, right?
Like why not just let them write it all in and then when they run out of sats go somewhere else?

**Super Testnet:** 00:06:35

That's a pretty good solution.
I think you can improve that solution by making it cost them even more money so that they run out faster.
And that's what I think filters do at the mempool level.
They increase the cost of getting this to miners.
They have to go to private mempools which typically charge more, they have to download and install and run special software and convince miners to do so and that increases costs on miners and they have to pass on those costs.
It makes it harder and jacks up their prices and makes the value destroyers run out of money faster.
To me, that's a very good thing.

## OP_RETURN Data Limits

niftynei: 00:07:10

So, the `OP_RETURN` data carrier size limit, should we keep it at 80 bytes, make it smaller, get rid of it.

**Super Testnet:** 00:07:16

I'd like to reduce it to zero.

niftynei: 00:07:18

Reduce it to zero.
So you want it such that `OP_RETURN`s don't exist basically.
Remove the `OP_RETURN`.

**Super Testnet:** 00:07:24

I think having it so that you can create an `OP_RETURN` but only if it has zero value.
Zero data in the script.

niftynei:00:07:32

Zero data push.
Okay.
No data.
Super is a data minimalist it sounds like.
Would you say you're a minimalist in other aspects of your life?

**Super Testnet:** 00:07:45

Some people say that.
niftynei: 00:07:47
I'm not going to say that.


Never mind.
Sure.


## Eternal Battles on Bitcoin

niftynei: 00:07:51

So I mean, this kind of like war on arbitrary data in the blockchain that you're proposing that the Bitcoiners engage in.
Have you engaged in any other sort of like fight you feel like that's like — I mean that's like an internal eternal war that you're sort of signing up for.
Isn't it easier to like, well I was going to say, do you have any precedents of fights that you feel like you've been involved in for a long time that have like dragged on for years like this one has.

**Super Testnet:** 00:08:17

In the Bitcoin space?

niftynei: 00:08:19

Sure, or in general.

**Super Testnet:** 00:08:21

The one that comes to mind is the fight against altcoins in general.
So like trying to persuade people that Bitcoin is a better money than altcoins is a battle that I've been in since pretty much since I actually since before I got into Bitcoin.
And yeah, that's — I think that's that's a pretty comparable one.

niftynei: 00:08:45

Altcoins.
So I mean, and do you think that this battle against arbitrary data is like related to the altcoin?
Spamcoin?
Altcoin?
I'm sorry.
I don't know what you call it.

**Super Testnet:** 00:08:55

Related, yeah.
A lot of the spam is token data.
So it's people creating, launching, and then using altcoins with Bitcoin's blockchain as the data carrier for those.
And so part of fighting altcoins is also fighting them on Bitcoin's blockchain, which is part of the spam.

niftynei: 00:09:13

Yeah, it makes sense.
I know, part of me is like, but if they want to send Bitcoin to Bitcoin miners, like buy Bitcoin so they can run their scams on Bitcoin, isn't that good for Bitcoin?
Blocks are getting filled up.

**Super Testnet:** 00:09:26

It has some good effects, but it also has negative effects.
I could easily imagine encouraging someone to synchronize the blockchain and then they, you know, take a look at what's on there and they're like, it's a bunch of JPEGs and altcoins and like there's barely any Bitcoin happening on this network.
Why would I synchronize this?

niftynei: 00:09:44

Well, you say there's barely any Bitcoin happening, but those transactions are paying fees to Bitcoin miners, right?
Is that not Bitcoin?

**Super Testnet:** 00:09:50

The fees are.
The fees are paying Bitcoin, but it's...

niftynei: 00:09:54

Bitcoin's changing hands.

**Super Testnet:** 00:09:55

Some is, yeah.
They're paying miners in order to add data to the blockchain.
And I think if they were paying to move data around on some other network, that would be a better use of it.
Like let's say that someone made some kind of art house and then they sold art and the art was moved through normal means like email or physical delivery, but just the payment happened on Bitcoin.
I think that'd be a great use case of Bitcoin to just pay for art and say, let's move this off-chain.
But when they do it on-chain, it makes it so that the network is being used for something it's not designed for, it's not good at transferring that kind of data, costs a lot of money, and it imposes a cost on all the people who are trying to run the network, and they just see a bunch of stuff that's not Bitcoin on there.

niftynei: 00:10:48

Where are they going to see it though?
Are they looking through the block data?

**Super Testnet:** 00:10:51

Yeah, I think even the fact that when you download it, you see it's 500 gigabytes or more.

niftynei: 00:10:58

But Bitcoin could be easily full of, I'm sorry.

**Super Testnet:** 00:11:02

No problem, I was just going to say it could easily lead someone to wonder what is that data and if they do any cursory look at it, they'll see that a lot of it is junk.

niftynei:00:11:15

Do you think they would feel differently if they looked at it and saw it was all people moving Bitcoin around?

**Super Testnet:** 00:11:19

Yeah, I think so.
I think that would be a good reason to say, wow, these people really care about this project.

niftynei: 00:11:25

I see.

## HODLing vs. Spending Bitcoin

niftynei: 00:11:26

But if we're all supposed to be hodling Bitcoin, who's supposed to be sending Bitcoin to each other.

**Super Testnet:** 00:11:31

I'm a fan of sending Bitcoin to each other and not just hodling it.

niftynei: 00:11:34

Yeah, I don't know, it's like one of those, it's like, well, okay, we have this wonderful thing which is a blockchain which permits anyone who holds Bitcoin to transact at any point in time in ten minute increments, right?
And if people who hold Bitcoin aren't sending enough transactions frequently enough, why not let the spammers use up the block space and send Bitcoin to miners if other people aren't willing to outbid them for the space?

**Super Testnet:** 00:12:00

It reminds me of a scene from the film O Brother Where Art Thou?
Where they run into the guy who sold his soul to the devil so that he could learn to play the guitar really good.

niftynei: 00:12:07

Okay.

**Super Testnet:** 00:12:07

And they say, well, why did you sell your soul to the devil?
And he says, well, I wasn't using it.
It's like, I don't think there's a good reason to give up block space to spammers is because Bitcoiners aren't using it.

niftynei: 00:12:22

I think that's a perfect argument.
Yeah.
Great.
Is there any other like, so I think that, I think that makes sense from a perspective of, yeah, okay.
I like, I appreciate hearing your thoughts on that.
I think that's an interesting perspective on the current topic.

## BTC++ Conference Recap

niftynei: 00:12:44

I was a little disappointed at the conference that we didn't spend more time talking about mining decentralization on the main stages.
I had a bunch of talks I think that kind of went around this.
We had a great talk from `DATUM` about `DATUM` from Jason Hughes at OCEAN.
I'm really excited about watching the recording on that one.
Did you feel like we focused too much on this filtering debate?
Because I kind of felt that way.
Or do you think it's an important conversation that is one that maybe we needed to spend time on as a group?

**Super Testnet:** 00:13:17

I think too much time was spent on it.
I would have preferred to see more of a focus on mining decentralization and the things you mentioned.
Also, I think having some space dedicated to it would be fine.
Maybe one talk instead of nine.

niftynei: 00:13:32

Okay, got it.
I didn't realize we had that many talks.

**Super Testnet:** 00:13:36

I don't think you had nine talks, but it did seem more prominent than I would have wished.

niftynei: 00:13:41

Yeah, I think it definitely got a lot more airtime.
But I think it's kind of one of those things like, I think it's what people wanted to talk about.

**Super Testnet:** 00:13:48

I agree.

niftynei: 00:13:49

And so that's what we ended up talking about because that was what it seemed like people wanted to talk about.
Cool.
Where are you headed next?
What's next for Super Testnet?
Are we going to see you in Riga for the Privacy Edition?

**Super Testnet:** 00:14:00

I'd love to.
On the note of privacy, I will be in Las Vegas later this month, May 26th I think, 5th or 6th.
I will be talking on a privacy panel with Seth for Privacy and Aaron van Wirdum at the Bitcoin conference in Las Vegas.
And then I will also be doing a presentation about the privacy advantages of using coin pools.
So lots of focus on privacy for me lately.

niftynei:00:14:24

Okay, great.
Well, hopefully we'll see you in Riga then in August, the 7th and 8th right ahead of the Baltic Honeybadger.
Sounds like people can catch you in Vegas.
Are you going to be participating in the Bitcoin++ Hackathon online virtual one for Bitcoin++ this year?

**Super Testnet:** 00:14:42

For Bitcoin++, there's also one happening with the Las Vegas thing.
They do a lot of hackathons.
Is that the one you're referring to?

niftynei: 00:14:48

Yeah, we're helping run it this year.
So Bitcoin++ is powering the Vegas hackathon this year.

**Super Testnet:** 00:14:53

I'm not a fan of the chosen model and in order to express that I'm not participating.

niftynei: 00:14:59

Okay, that makes sense.
And the chosen model that we're doing is the online?

**Super Testnet:** 00:15:03

Yeah, well, it's fine to have an online component, but when you have no in-person component, that seems...
That's upsetting to me.

niftynei: 00:15:11

Makes sense.
Yeah, I also prefer in-person components.

**[Ad Read]:** 00:15:15

This episode is brought to you by BTC++, the premier technical conference series for Bitcoin developers.
BTC++ is not your typical Bitcoin conference.
It's a world-class gathering of engineers, hackers, and builders focused on the cutting edge of Bitcoin development.
From protocol research to lightning, smart contracts, covenants, privacy tools and beyond, BTC++ dives deep into the work that's shaping the future of Bitcoin.
Join us for our next event in Riga, Latvia on August 7th and 8th, focused on Bitcoin privacy, and see all our upcoming events across the globe at btc++.dev.

niftynei:00:15:55

We're back for part two of interviewing Super.
Super, we had some questions from last time that we didn't get answered, so I wanted to get into it.

## Is Arbitrary Data/Spam Subjective?

niftynei:00:16:03

We talked a little bit about spam filters and what spam is and you were very much we should work as hard as possible to prevent spam from getting into transactions because — or into blocks really — because Bitcoin should be for financial transactions.
Good question though that came from our audience is that, is that idea of arbitrary data like spam subjective?
Like if people look at Bitcoin, are people gonna be like, oh, this is definitely spam?

**Super Testnet:** 00:16:37

I think that spam has a subjective element and an objective element.
And I want to talk about a couple of the objective elements for a moment.
Walton, do you want to take the tablet?
Yeah, I think spam has subjective and objective elements and I want to talk about the objective elements for just a moment.
So when Satoshi created Bitcoin, he had very early mempool filters that he created allowed certain type of transactions and actually prohibited in the mempool the rest.
So types of transactions he did permit were where you're just sending to a Bitcoin address, he allowed you to send just straight to a `scriptPubKey`, and he allowed you to send to a multisig which was a list of public keys, and he banned everything else.
Anything that involved more advanced uses of script, anything that involved data carrier stuff, it was all prohibited.
And I think part of the reason I think he did that was because there was no consensus yet on what other types of transactions should be allowed.
I think it would be cool to go back to a model where there's a very restricted set of transactions that are allowed by default in the mempool, and if you want to get something else transmitted, you have to make a case for lifting that limit and saying, this type of transaction should also be done.
Like for example, this is a Lightning transaction, it uses script in a new way, so we should relax the limits.
If it meets a Lightning template, we should allow that into the mempool.
So that's one objective factor is you can actually see whether it matches certain criteria that are approved.
And then if it doesn't, then it's prohibited.
Another one is just the data carrier elements themselves.
If a transaction uses `OP_RETURN` to carry a certain amount of bytes, or if it uses an inscription envelope to carry a certain amount of bytes, that's an objective way of telling this is just arbitrary data.
It's not the least amount of bytes necessary in order to accomplish the goal of sending money into an address because you could have done that without including an `OP_RETURN` that has data or without including an inscription envelope.

## Transaction Filtering Governance

**Super Testnet:** 00:18:36

So there are objective elements that I think we can test against and filter for.

niftynei: 00:18:40

I mean, yeah, there's a lot of different directions I think I could take this, but I think one of them is like, okay, so if you come up with a list of transactions of what's permissive and what isn't, now all of a sudden you need a committee that's saying, okay, this is allowed and this isn't allowed.
And so all of a sudden you introduce, I think, a lot more politics into the process.
You need a lot more bureaucracy because you need someone who's saying this is the list of allowable transactions and this is the not allowable and when new types come out you have to go through like a patch change request process to get it added to the allowable list like lightning transactions for example.
Whereas that seems a little bit different from the other side, which is like everything and anything is permissible that you can pay for.
It fits the protocol outline, minus these few fields where you can put anything you want in it.
That seems more open and anarchic and capitalist in terms of whoever is willing to pay for the block data can have it, it doesn't matter what they want to put in it.
How do you balance those kind of two requirements in terms of governance of making the decision to make the filters more strict?

**Super Testnet:** 00:19:54

Before I do that, I just make a rhetorical point.
To me, sounding more capitalist and more anarchic are not good things.
I would like things that sound less anarchic, less capitalist.
That said, having a bureaucracy, I think that sounds a lot like the Bitcoin Core BIP review process.
Like when we wanted to add Lightning Network to Bitcoin, it needed a couple of soft forks.
And in order to get those activated, there was a BIP review process.
People had to upgrade their nodes to a new software version if they wanted to do that, if they wanted to opt in to these soft forks.
I think it'd be cool to have a similar process for expanding the set of transactions allowed at the mempool.
If you had to convince people who develop Bitcoin that your idea is a good idea, and then they had to release new software, and then other people had to choose whether they want to run it or not, I think that we would see a lot less spam on the network today because it'd just be a lot more difficult to get it in.
And that sounds like a better world to me.

niftynei: 00:20:52

Cool, makes sense.
Better world for everyone sounds like a great idea.

**Super Testnet:** 00:20:58

Yeah, that's neat to me too.
But when there are disagreements about which world is better, I think that's why platforms like this allow us to have a discussion and persuade one another.

niftynei: 00:21:10

Do you think we necessarily need to all agree which way is better?
Or can the filtering camp exist alongside the permissive camp?

**Super Testnet:** 00:21:18

I think they can coexist.
I hope that an increasing number of people agree with me, and we'll see what happens.

niftynei: 00:21:26

Okay, yeah.
So we kind of wrapped up the last chat, and at the end of it we said, man, we just talked about, like we wish that at the conference we would have talked about things other than filtering and `OP_RETURN`s and data carriers, and then we spent 20 minutes talking about it ourselves.

**Super Testnet:** 00:21:42

Yeah, no, like 30 minutes.

niftynei: 00:21:43

No, 30 minutes, going on 30 minutes without talking about it.
What should we be talking about if not that?
Like if we could change the conversation to something else, what should we change it to?

**Super Testnet:** 00:21:53

I'd like to talk a little bit more about privacy, which is another thing we mentioned a couple times.

## Privacy on Bitcoin & Lightning

niftynei: 00:21:57

Okay, yeah.

**Super Testnet:** 00:21:58

So a lot of my recent projects have focused on improving privacy on Bitcoin.
And one of the things that I'm currently, well, I just released some code for it today and I'll be hopefully doing a little bit more later, is a privacy tool for the Lightning Network.
So, my current project is designed to make it so that you can increase more easily the number of hops between you and your destination on the Lightning Network because I think that increasing the number of hops increases your level of privacy.
So I'm making a tool for that.

niftynei:00:22:33

Increasing the number of hops increases your privacy.
That makes sense.
I think Rusty had a project in Core Lightning and he's trying to add to some of the configurations in route pathfinding so that it would optimize — if you're trying to be more private, it would add more hops.
There's trade-offs to adding more hops though, right?

**Super Testnet:** 00:22:50

Yeah, payment reliability falls and that sucks.

niftynei: 00:22:56

It's also more expensive, right?

**Super Testnet:** 00:22:58

Yeah, typically.

niftynei: 00:22:58

From a cost perspective,
is the cheapest way to send a Bitcoin a Lightning transaction?
Wait... is it that the cheapest way to send a Bitcoin transaction is between someone you're directly peered to on the Lightning Network?

**Super Testnet:** 00:23:09

I think it depends.
At least one nice thing about that is you don't have to pay routing fees if you have a direct connection to someone.

niftynei: 00:23:15

Yeah, it's basically free.

**Super Testnet:** 00:23:17

It is basically free, but you also have to set up the connection.
And if you're not going to be making repeated transactions to them, then it's about 300 bytes to set it up, maybe 400 bytes to close the connection.

niftynei:00:23:28

It's more expensive.

**Super Testnet:** 00:23:28

If you only do one transaction, you're actually losing money there.

niftynei: 00:23:32

You would have been better just doing an on-chain transaction.

**Super Testnet:** 00:23:34

Or opening up a channel with someone who you will more likely make repeat connections to and then routing through them.

niftynei: 00:23:40

Right, makes sense.
Yeah, yeah, yeah.
Cool, so other than adding more, so you said adding more hops, is there anything else you think improves privacy?

**Super Testnet:** 00:23:50

Decoy public keys.
So one feature of the way Lightning invoice, `BOLT11` invoices work is that you put a public key in them and if you're running a routing node, then that's enough to find you on the network, to find your node.
If you're not running a routing node, then you also have to specify a routing node that you're connected to, or it's within a couple of hops of you.
And this leaks information about your node on the network.
So getting that public key out of an invoice is possible.
It's possible to replace it with a dummy public key.
It's possible to replace it with someone else's public key.
I like tools that assist people with doing that so they don't leak data about their node on the Lightning Network.

niftynei: 00:24:31

Dummy keys are one way to prevent leaking data.
That makes sense.
Yeah.
Cool.
What else are you working on, Super?

**Super Testnet:** 00:24:38

Well, it kind of depends on the week.
It seems like every week I come up with another project.
Last month, one thing that I was focused on quite a bit was CoinPools.
So I presented my CoinPool software at Bitcoin++ in Brazil.
And I have done a couple of updates to it since then, but it's not in a better state right now.
So I have to keep working on it at some point.
But the other thing is I get sick of working on projects, and I got sick of working on the CoinPool thing, which is why I look for something else.
So hopefully at some point I will get inspired to work on it again.

**niftynei:** 00:25:12

And so people can find out more about CoinPools by watching your Bitcoin++ talk from Florianópolis.
And you'll be talking about it in Vegas, it sounds like, in a few weeks.
Very cool.

**Super Testnet:** 00:25:23

Yep, so you can, if you go to YouTube and search for Super Testnet Coin Pools, you should find a video on there.
And you can also search the Bitcoin++ YouTube channel and eventually possibly, I don't know if they'll be live streamed at the Bitcoin conference in Las Vegas, but if so, you can also find information there.

**niftynei:** 00:25:40

Great.
Anything else we should talk about, Super?
What's next for Super Testnet?
Coin pools, privacy on Lightning?

**Super Testnet:** 00:25:47

Yeah, I mentioned my presentations in Las Vegas.
Perhaps I'll be in Riga for the privacy conference there, so we'll see what happens, but I'm looking forward to doing those things.
Continuing to work on random projects that occur to me as they occur.

**niftynei:** 00:26:03

More Bitcoin development coming to you soon from Super Testnet to yours.
All right.
Thanks, Super.

**Super Testnet:** 00:26:09

Thank you, everyone.