---
title: 'Bitcoin++ Insider Edition: Super Testnet'
transcript_by: 'mokayaj857 via review.btctranscripts.com'
media: 'https://youtu.be/hv9Ckgeal88'
date: '2025-05-21'
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
# Bitcoin++ Insider Edition: A Conversation with Super Testnet

## Intro

**Speaker 0:** 00:00:00

Hey Super, how's it going?

**Speaker 1:** 00:00:01

So good.

**Speaker 0:** 00:00:02

Welcome to Bitcoin++ Insider Edition. Do you want to explain to the crowd who you are and what you're doing in Austin this week?

**Speaker 1:** 00:00:09

My name is Super Testnet. I'm a Bitcoin developer. I focus on Bitcoin, the Lightning Network. I do a lot of research into alternative Layer 2 solutions, and I'm in Austin this week for Bitcoin++, a Bitcoin conference that just took place, to present one of my projects.

**Speaker 0:** 00:00:27

What project were you talking about?

**Speaker 1:** 00:00:29

It's called `TestNet Generator`. It's a project where you can launch your own Bitcoin testnet and then have as many Bitcoins, or fake Bitcoins, as you like to test with.

**Speaker 0:** 00:00:41

Did anyone get testy during the workshop?

**Speaker 1:** 00:00:43

No, I don't think so. I was really excited that Luke Dashjr came to it.

**Speaker 0:** 00:00:47

That's fun.

**Speaker 1:** 00:00:48

He's a longtime Bitcoin hero for me, and he chose to come to my talk.

**Speaker 0:** 00:00:52

That's really cool. Did you manage to spin up a testnet during your talk?

**Speaker 1:** 00:00:56

Oh, yeah. We did that within the first five minutes.

**Speaker 0:** 00:01:00

Then what did you do the rest of the time?

**Speaker 1:** 00:01:02

I added `CTV` to it. As an illustration of how I code, I had some `CTV` code and added it into the testnet so you can create `CTV` transactions.

**Speaker 0:** 00:01:14

Very cool. So you talked about how Luke Dashjr came to your talk and you were excited he was there. What talks did you go to that you think he might have been excited you were in the audience for?

**Speaker 1:** 00:01:27

Well, I went to his talk, but I don't think he knows me, so maybe not that one. It was also right before mine.

**Speaker 0:** 00:01:38

What was he talking about in that one? Was that his policy changes?

**Speaker 1:** 00:01:41

Yeah, he was demonstrating how to make your own mempool policies. It was pretty cool, because we've been dealing a lot during the conference with new versions of spam on the blockchain. So he gave an illustration of how fast it is to update the mempool to filter out more spam.

**Speaker 0:** 00:01:59

How fast was it?

**Speaker 1:** 00:02:01

He did it within 30 minutes.

**Speaker 0:** 00:02:03

Let's go. When he was talking to me about the talk, because I really wanted him to do that one since I thought it was a cool demonstration of the process for making that kind of code change, he was telling me he wasn't sure he could get it to compile in 30 minutes.

**Speaker 1:** 00:02:18

It did. I remember back when Counterparty first launched, there were new types of spam going on in the network. The Counterparty people were saying things like, "you can't stop us, we can just add new things you can't detect." At the time, Luke made this cool poster. He updated his mempool policy and said, "Look, it took five minutes, I just added a line, and now I've filtered your new type of spam." It reminded me of that. It doesn't take much to actually fight this stuff.

**Speaker 0:** 00:02:46

Right, it just takes a little bit of proactivity. I had a tweet thread after listening to the talks about how, really, one side of the debate...

## Filtering Bitcoin Transactions

**Speaker 0:** 00:02:57

A lot of what we talked about at the conference was this filtering stuff. It felt like more of a theme than I was intending it to be. But there are kind of two positions. One is that we can't fight it, we should let them do it — they're paying for block space. As long as people are paying for whatever data they want included in a transaction, and the transactions aren't spamming the network in terms of sheer number of transactions, that's arbitrarily fine. Then there's the position that Luke and the "Knots" organization hold —

**Speaker 1:** 00:03:38

We call them Nazis.

**Speaker 0:** 00:03:39

The Knots — they're like, well, we should and we can fight it, and here's how we're going to do it. They're digging in and doing their best to prevent this type of data from being written into the blockchain by filtering out those transactions. Where would you say you fall on that spectrum? Are you for continually updating filters so this data doesn't arrive at your node, or should people be allowed to write arbitrary data into the blockchain as long as they're willing to pay for it?

**Speaker 1:** 00:04:11

I'm a fan of the first one. I like to fight the spam and try to eliminate as much of it as possible, increase the cost of producing spam, and generally make their lives harder so that Bitcoin is better money.

**Speaker 0:** 00:04:27

My understanding of this is similar to how things grow in a forest — something grows, a predator comes along and eats it, so it grows spines, and eventually you end up with flowers that are beautiful but you can't touch because they're too poisonous. My worry with constant evolution is that spammers will find new ways to put data into transactions. Is it worth fighting that endless fight, making them more sophisticated and incentivizing them to go around the mempool to get their transactions into blocks?

**Speaker 1:** 00:05:10

I think so. If it's a never-ending battle, there's nothing wrong with having a never-ending resistance against it. Perhaps instead of us getting complacent and saying "we can't fight it," they'll be the ones to get complacent and say "none of our attacks are working."

**Speaker 0:** 00:05:30

I see.

**Speaker 1:** 00:05:31

For a long time that kind of did happen. Back when Counterparty launched, they were doing spam on Bitcoin for a while, but it dropped off because Bitcoiners fought it and they moved to Ethereum. That lasted all the way up until around 2022. So maybe the same thing can happen. If we fight it hard, and succeed at stopping most of their efforts, perhaps they'll move somewhere more accepting and do it there.

**Speaker 0:** 00:06:00

The grass is greener somewhere else.

**Speaker 1:** 00:06:02

And then we get another eight years or so.

**Speaker 0:** 00:06:05

Or out of spite. A lot of these projects that launch spam or arbitrary data onto the network seem to have moments where a bunch of transactions get in — they're buying a lot of block space for a certain period — but then they really fall off. Writing into the blockchain isn't free, it costs money. They're going to run out of sats at some point, right? Why not just let them write it all in, and once they run out of sats, they go elsewhere?

**Speaker 1:** 00:06:35

That's a pretty good solution. I think you can improve it by making it cost them even more money so they run out faster. That's what filters do at the mempool level — they increase the cost of getting transactions to miners. Spammers have to go to private mempools, which typically charge more; they have to download, install, and run special software, and convince miners to do so, which increases costs on miners, who then pass those costs on. It jacks up their prices and makes value destroyers run out of money faster. To me, that's a very good thing.

## OP_RETURN Data Limits

**Speaker 0:** 00:07:10

The `OP_RETURN` data-carrier size limit — should we keep it at 80 bytes, make it smaller, or get rid of it?

**Speaker 1:** 00:07:16

I'd like to reduce it to zero.

**Speaker 0:** 00:07:18

Reduce it to zero — so you want `OP_RETURN`s to basically not exist. Remove them entirely.

**Speaker 1:** 00:07:24

I think it should be possible to create an `OP_RETURN`, but only with zero value and zero data in the script.

**Speaker 0:** 00:07:32

Zero data in the script, no data. Super is a data minimalist, it sounds like. Would you say you're a minimalist in other aspects of your life?

**Speaker 1:** 00:07:45

Some people say that. I'm not going to say that.

**Speaker 0:** 00:07:47

Never mind.

**Speaker 1:** 00:07:48

Some people say that, sure.

## Eternal Battles on Bitcoin

**Speaker 0:** 00:07:51

This kind of war on arbitrary data in the blockchain that you're proposing Bitcoiners engage in — it sounds like an eternal struggle you're signing up for. Do you have any precedent for fights you've been involved in that have dragged on for years, like this one has?

**Speaker 1:** 00:08:17

In the Bitcoin space?

**Speaker 0:** 00:08:19

Sure, or in general.

**Speaker 1:** 00:08:21

The one that comes to mind is the fight against altcoins in general. Trying to persuade people that Bitcoin is better money than altcoins is a battle I've been in since before I even got into Bitcoin. That's a pretty comparable one.

**Speaker 0:** 00:08:45

Do you think this battle against arbitrary data is related to that altcoin fight?

**Speaker 1:** 00:08:55

Related, yeah. A lot of the spam is token data — people creating and launching altcoins, using Bitcoin's blockchain as the data carrier for those. So part of fighting altcoins is also fighting them on Bitcoin's blockchain, which is part of the spam.

**Speaker 0:** 00:09:13

It makes sense, but part of me thinks: if they want to send Bitcoin to Bitcoin miners — buy Bitcoin so they can run their scams on Bitcoin — isn't that good for Bitcoin? Blocks are getting filled up.

**Speaker 1:** 00:09:26

It has some good effects, but also negative ones. I could easily imagine someone synchronizing the blockchain, taking a look at what's on there, and thinking, "it's a bunch of JPEGs and altcoins, there's barely any Bitcoin happening on this network — why would I synchronize this?"

**Speaker 0:** 00:09:44

But those transactions are paying fees to Bitcoin miners. Isn't that Bitcoin?

**Speaker 1:** 00:09:50

The fees are Bitcoin, but —

**Speaker 0:** 00:09:54

Bitcoin's changing hands.

**Speaker 1:** 00:09:55

Some is, yeah. They're paying miners to add data to the blockchain. If they were paying to move data around on some other network, that would be a better use of it. Say someone made an art house and sold art, with the art moved through normal means like email or physical delivery, but the payment happened on Bitcoin — that'd be a great use case, paying for art while moving the data off-chain. But when they do it on-chain, the network is used for something it's not designed for, it's not good at transferring that kind of data, it costs a lot of money, and it imposes a cost on everyone running the network, who just see a bunch of non-Bitcoin stuff on there.

**Speaker 0:** 00:10:48

Where are they going to see it, though? Are they looking through the raw block data?

**Speaker 1:** 00:10:51

Yeah, I think even the fact that when you download it, you see it's 500 gigabytes or more —

**Speaker 0:** 00:10:58

But Bitcoin could easily be full of —

**Speaker 1:** 00:11:02

No problem, I was just going to say it could easily lead someone to wonder what that data is, and if they take any cursory look, they'll see a lot of it is junk.

**Speaker 0:** 00:11:15

Do you think they'd feel differently if they looked and saw it was all people moving Bitcoin around?

**Speaker 1:** 00:11:19

Yeah, I think so. I think that would lead someone to say, "wow, these people really care about this project."

## HODLing vs. Spending Bitcoin

**Speaker 0:** 00:11:26

But if we're all supposed to be HODLing Bitcoin, are we supposed to be sending it to each other?

**Speaker 1:** 00:11:31

I'm a fan of sending Bitcoin to each other, not just hoarding it.

**Speaker 0:** 00:11:34

I don't know, it's like — we have this wonderful thing, a blockchain that permits anyone holding Bitcoin to transact at any point in ten-minute increments. If people who hold Bitcoin aren't sending enough transactions frequently enough, why not let spammers use the block space and send Bitcoin to miners, if no one else is willing to outbid them for it?

**Speaker 1:** 00:12:00

It reminds me of a scene from the film *O Brother, Where Art Thou?* where they run into the guy who sold his soul to the devil so he could learn to play guitar really well.

**Speaker 0:** 00:12:07

Okay.

**Speaker 1:** 00:12:07

They ask him, "why did you sell your soul to the devil?" And he says, "well, I wasn't using it." I don't think "Bitcoiners aren't using it" is a good reason to give up block space to spammers.

**Speaker 0:** 00:12:22

I think that's a perfect argument. I appreciate hearing your thoughts on that — it's an interesting perspective on the current topic.

## BTC++ Conference Recap

**Speaker 0:** 00:12:44

I was a little disappointed the conference didn't spend more time on mining decentralization on the main stages. We had a great talk on `Datum` from Jason Hughes at Ocean — I'm excited to watch the recording. Did you feel like we focused too much on this filtering debate? I kind of felt that way, or do you think it's an important conversation we needed to have as a group?

**Speaker 1:** 00:13:17

I think too much time was spent on it. I would have preferred more focus on mining decentralization and the things you mentioned. Having some space dedicated to filtering would be fine — maybe one talk instead of nine.

**Speaker 0:** 00:13:32

Got it, I didn't realize we had that many talks.

**Speaker 1:** 00:13:36

I don't think it was literally nine, but it felt more prominent than I would have wished.

**Speaker 0:** 00:13:41

Yeah, it definitely got a lot of airtime, but I think it's what people wanted to talk about.

**Speaker 1:** 00:13:48

I agree.

**Speaker 0:** 00:13:49

So that's what we ended up talking about, because that's what it seemed like people wanted. Where are you headed next? What's next for Super Testnet? Will we see you in Riga for the Privacy Edition?

**Speaker 1:** 00:14:00

I'd love to. On the note of privacy, I'll be in Las Vegas later this month — May 5th or 6th, I think — talking on a privacy panel with Seth for Privacy and Andrew Van Weerdum at the Bitcoin Conference in Las Vegas. I'll also be presenting on the privacy advantages of using `CoinPools`. Lots of focus on privacy for me lately.

**Speaker 0:** 00:14:24

Great. Hopefully we'll see you in Riga in August, the 7th and 8th, right ahead of the Baltic HoneyBadger. Sounds like people can catch you in Vegas. Are you participating in the Bitcoin++ Hackathon, the online virtual one this year?

**Speaker 1:** 00:14:42

There's also one happening alongside the Las Vegas event — they do a lot of hackathons. Is that the one you're referring to?

**Speaker 0:** 00:14:48

Yeah, we're helping run it this year — Bitcoin++ is powering the Vegas hackathon.

**Speaker 1:** 00:14:53

I'm not a fan of the hybrid model, and to express that, I'm not participating.

**Speaker 0:** 00:14:59

That makes sense. The hybrid model includes an online component?

**Speaker 1:** 00:15:03

Yeah, it's fine to have an online component, but when there's no in-person component, that's upsetting to me.

**Speaker 0:** 00:15:11

Makes sense. I also prefer in-person components.

**[Speaker 2]:** 00:15:15

This episode is brought to you by BTC++, the premier technical conference series for Bitcoin developers. BTC++ is not your typical Bitcoin conference — it's a world-class gathering of engineers, hackers, and builders focused on the cutting edge of Bitcoin development. From protocol research to Lightning, smart contracts, covenants, privacy tools, and beyond, BTC++ dives deep into the work shaping the future of Bitcoin. Join us for our next event in Riga, Latvia on August 7th and 8th, focused on Bitcoin privacy, and see all upcoming events at btc++.dev.

**Speaker 0:** 00:15:55

We're back for part two of interviewing Super. We had some questions from last time that we didn't get to, so I wanted to dig into those.

## Is Arbitrary Data/Spam Subjective?

**Speaker 0:** 00:16:03

We talked about spam filters and what spam is, and your position was that we should work as hard as possible to prevent spam from getting into blocks, because Bitcoin should be for financial transactions. A good question from our audience: is the idea of "arbitrary data as spam" subjective? Would people just look at Bitcoin and say, "oh, this is definitely spam"?

**Speaker 1:** 00:16:37

I think spam has both a subjective element and an objective element, and I want to talk about a couple of the objective elements for a moment. When Satoshi created Bitcoin, he built very early mempool filters that allowed certain types of transactions and prohibited the rest. The types he permitted were sending to a Bitcoin address, sending straight to a `scriptPubKey`, and sending to a multisig — a list of public keys. Everything else was banned: anything involving more advanced uses of script, anything involving data-carrier functionality. Part of the reason, I think, was that there was no consensus yet on what other transaction types should be allowed.

I think it would be cool to return to a model with a very restricted default set of allowed transactions, where to get something else transmitted, you'd have to make a case for lifting that limit — for example, "this is a Lightning transaction, it uses script in a new way, so we should relax the limits; if it matches a Lightning template, we should allow it into the mempool." That's one objective factor: you can test a transaction against approved criteria, and if it doesn't match, it's prohibited.

Another objective factor is the data-carrier element itself. If a transaction uses `OP_RETURN` to carry a certain number of bytes, or an inscription envelope to carry bytes, that's an objective way of identifying arbitrary data — it's not the minimum number of bytes necessary to send money to an address, since you could have done that without the `OP_RETURN` data or the inscription envelope.

## Transaction Filtering Governance

**Speaker 1:** 00:18:36

So there are objective elements we can test against and filter for.

**Speaker 0:** 00:18:40

There are a lot of directions I could take this, but one is: if you come up with a list of permitted and non-permitted transaction types, you now need a committee deciding what's allowed. That introduces a lot more politics into the process and bureaucracy, since someone has to maintain the allowable list, and when new types emerge, you'd need a patch/change-request process to get them added — Lightning transactions, for example. That seems different from the alternative, where everything is permissible as long as you can pay for it and it fits the protocol outline, minus a few fields where you can put anything you want. That seems more open, anarchic, and capitalist — whoever's willing to pay for block space can have it, regardless of content. How do you balance those two approaches when it comes to governing how strict the filters should be?

**Speaker 1:** 00:19:54

Before I answer, a rhetorical point: to me, sounding more capitalist or more anarchic isn't a good thing — I'd prefer things that sound less anarchic, less capitalist. That said, what you're describing as bureaucracy sounds a lot like the Bitcoin Core BIP review process. When we wanted to add the Lightning Network to Bitcoin, it needed a couple of soft forks. To get those activated, there was a BIP review process — people had to upgrade their nodes to a new software version if they wanted to opt in.

I think it'd be great to have a similar process for expanding the set of transactions allowed at the mempool level. If you had to convince Bitcoin developers your idea is good, they released new software, and other people chose whether to run it, I think we'd see a lot less spam on the network today, because it'd be much harder to get it in. That sounds like a better world to me.

**Speaker 0:** 00:20:52

Makes sense. A better world for everyone sounds like a great idea.

**Speaker 1:** 00:20:58

Yeah, that's neat to me too. But when there are disagreements about which world is better, that's why platforms like this let us have a discussion and try to persuade one another.

**Speaker 0:** 00:21:10

Do you think we necessarily need to agree on which way is better, or can the filtering camp coexist alongside the permissive camp?

**Speaker 1:** 00:21:18

I think they can coexist. I hope an increasing number of people agree with me, and we'll see what happens.

**Speaker 0:** 00:21:26

So we kind of wrapped up the last chat saying we wished the conference had spent less time on filtering and `OP_RETURN`s and data carriers — and then we spent 20 minutes talking about it ourselves.

**Speaker 1:** 00:21:42

More like 30 minutes.

**Speaker 0:** 00:21:43

30 minutes, going on, without talking about anything else. What should we be talking about instead? If we could change the conversation, what would it be?

**Speaker 1:** 00:21:53

I'd like to talk a bit more about privacy, which is something we've mentioned a couple of times.

## Privacy on Bitcoin & Lightning

**Speaker 0:** 00:21:57

Okay, let's do it.

**Speaker 1:** 00:21:58

A lot of my recent projects have focused on improving privacy on Bitcoin. I actually released some code for one today, and I'll likely release more soon — a privacy tool for the Lightning Network. The project is designed to make it easier to increase the number of hops between you and your destination on the Lightning Network, because I think more hops means more privacy. So I'm building a tool for that.

**Speaker 0:** 00:22:33

Increasing the number of hops increases your privacy — that makes sense. I think Rusty had a project in `CoreLightning` adding configuration options to route pathfinding, so if you want more privacy it would favor more hops. There are trade-offs to adding more hops, though, right?

**Speaker 1:** 00:22:50

Yeah, payment reliability falls, and that sucks.

**Speaker 0:** 00:22:56

It's also more expensive?

**Speaker 1:** 00:22:58

Typically, yeah.

**Speaker 0:** 00:22:58

From a cost perspective — is the cheapest way to send a Lightning transaction a direct, peered connection on the Lightning Network?

**Speaker 1:** 00:23:09

It depends. One nice thing about a direct connection is you don't have to pay routing fees.

**Speaker 0:** 00:23:15

So it's basically free.

**Speaker 1:** 00:23:17

It is basically free, but you also have to set up the connection. If you're not making repeated transactions to that peer, it's about 300 bytes to open the channel and maybe 400 bytes to close it.

**Speaker 0:** 00:23:28

So it's more expensive.

**Speaker 1:** 00:23:28

If you're only doing one transaction, you're actually losing money there.

**Speaker 0:** 00:23:32

You'd have been better off just doing an on-chain transaction.

**Speaker 1:** 00:23:34

Or opening a channel with someone you'll more likely make repeat connections to and routing through them.

**Speaker 0:** 00:23:40

Right, makes sense. So other than adding more hops, is there anything else you think improves privacy?

**Speaker 1:** 00:23:50

Decoy public keys. One feature of `BOLT 11` Lightning invoices is that you embed a public key in them. If you're running a routing node, that's enough to find you on the network. If you're not, you also have to specify a routing node you're connected to, or within a couple of hops of, which leaks information about your node. So it's possible to strip that public key from an invoice, replace it with a dummy public key, or replace it with someone else's. I like tools that help people do that so they don't leak data about their node on the Lightning Network.

**Speaker 0:** 00:24:31

Dummy keys are one way to prevent leaking data, that makes sense. What else are you working on, Super?

**Speaker 1:** 00:24:38

It depends on the week — it seems like every week I come up with another project. Last month, I was focused quite a bit on `CoinPools`. I presented my `CoinPool` software at Bitcoin++ in Brazil, and I've made a couple of updates since, but it's not in a great state right now, so I'll have to keep working on it at some point. I also tend to get sick of working on a single project, which is why I look for something else — hopefully I'll get inspired to return to it.

**Speaker 0:** 00:25:12

People can find out more about `CoinPools` by watching your Bitcoin++ talk from Florianópolis, and you'll be talking about it in Vegas in a few weeks too.

**Speaker 1:** 00:25:23

Yep — search "Super Testnet CoinPools" on YouTube and you should find a video. You can also search the Bitcoin++ YouTube channel, and possibly there will be a livestream at the Bitcoin Conference in Las Vegas, where you can find more information.

**Speaker 0:** 00:25:40

Great. Anything else we should cover, Super? What's next for Super Testnet — `CoinPools`, privacy on Lightning?

**Speaker 1:** 00:25:47

I mentioned my presentations in Las Vegas, and I may be in Riga for the privacy conference. We'll see what happens, but I'm looking forward to those, and to continuing work on whatever random projects occur to me.

**Speaker 0:** 00:26:03

More Bitcoin development coming to you soon from Super Testnet. Thanks, Super.

**Speaker 1:** 00:26:09

Thank you, everyone.