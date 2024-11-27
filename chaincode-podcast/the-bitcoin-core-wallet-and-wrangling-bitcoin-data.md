---
title: The Bitcoin Core wallet and wrangling bitcoin data
transcript_by: varmur via review.btctranscripts.com
media: https://podcasters.spotify.com/pod/show/chaincode/episodes/Josibake--the-Bitcoin-Core-wallet-and-wrangling-bitcoin-data---episode-24-e1piaje
tags:
  - bitcoin-core
  - signature-aggregation
  - wallet
speakers:
  - Josibake
summary: In this conversation, Adam Jonas and Mark Erhardt discuss their work with Josie Baker on Bitcoin data analysis, focusing on mempool data collection and Bitcoin Core wallet improvements. Josie explains his work in standardizing and cleaning mempool data to create a comprehensive, open-source dataset. This dataset will facilitate research and development in areas such as fee estimation and transaction propagation. They also delve into Bitcoin Core wallet enhancements, including privacy improvements and efficient coin selection methods. The conversation highlights the importance of reproducibility, empirical analysis, and open-source collaboration in advancing Bitcoin technology. Josie’s efforts emphasize the value of making Bitcoin data accessible and fostering a community of contributors in the Bitcoin development ecosystem.
episode: 24
date: 2022-10-21
aliases:
  - /chaincode-labs/chaincode-podcast/the-bitcoin-core-wallet-and-wrangling-bitcoin-data/
---
## Introduction

Adam Jonas: 00:00:00

Hey Murch!

Mark Erhardt: 00:00:01

Yo, what's up?

Adam Jonas: 00:00:02

We are back, as promised.
We're really following through this time.
We have Josie Baker in the office this week, and we're going to hear about what he's up to.

Mark Erhardt: 00:00:11

Yeah, we've been working with him on some mempool data stuff, and I've also worked with him closely on some Bitcoin Core wallet privacy improvements and that's fun stuff.

Adam Jonas: 00:00:19

Sounds like you already know all the answers, but I'm going to find out what you all are up to, and so hope you enjoy.
Welcome, Josie.
We tried to get you in the studio last time, but too busy.

Josibake: 00:00:35

We were very productive last time.
Many things had to be talked about, discussed, brainstormed.

Adam Jonas: 00:00:40

So tell us about the kind of work you've been doing now.
How long have you been doing this Bitcoin thing for?

Josibake: 00:00:45

I want to say I've passed the year mark, so about a year and a half.
I would consider the start the Chaincode seminar, which would have been the 2021 online seminar that I participated in, almost two years.
In terms of what I've been up to, lots of data analysis stuff.
So working with mempool data, mostly collecting data that people were wise enough to start collecting years ago and just were kind of sitting on and taking that, standardizing it, putting it all together, cleaning it a little bit, and working with one of Chaincode's own, Clara, on a research paper, analyzing that data.
The real goal for me is to then open source it and make it available for other people to use and hopefully find utility and interesting things from it.

## Analyzing historical transaction data

Adam Jonas: 00:01:25

Super cool.
Let's start with the project itself and then maybe you can talk more generally about data and what you like to do with Bitcoin data?

Josibake: 00:01:32

Yeah, so the project itself started with, we wanted to look at transactions and we didn't really want to look at anything in particular.
We just wanted to start looking at and analyzing transactions.
Some ideas we threw out there were - is there anything in fee behavior or transaction construction that leads to wallet fingerprints, and is that something that we can make people aware of?
Is there anything we can learn about fees and transactions and offer improvements?
That led into some wallet work where we looked at historical transactions, we applied some chain analysis heuristics to them and saw 30% of all transactions fit one of the heuristics pretty easily.

So we're like, okay, that seems like something we should address, and that led to work in Core, which we can talk a little bit about later.
As we were looking at this, one of the things that kept coming up was - okay, we have all this stuff on the blockchain, and everybody can analyze it, but what we don't have is the mempool.
Then someone would be like - "Oh, I have some mempool data, and it's for this month or this week, and it's in this format."
And then someone else would be like - "Oh, I think I have some too, but it has a bug or an issue, or it's a totally different format and I'm missing..."
So I started to reach out to people who I knew were interested in collecting this stuff and ask - "How much do you have, and can I have it, and are you interested in collecting it?"
So we got some from Christian Decker, who had been collecting it for a long time.
Basically his node was logging every time a transaction entered the mempool, I think all the way back to 2012, and it was maybe the basis of [one of his earlier papers](https://www.researchgate.net/publication/261434466_Information_propagation_in_the_Bitcoin_network) about propagation to the network.

Mark Erhardt: 00:02:52

Transaction propagation.

Josibake: 00:02:53

Yeah, it's actually block propagation.

Mark Erhardt: 00:02:55

Oh, yeah, right.

Josibake: 00:02:56

I thought it was about transaction propagation.

Mark Erhardt: 00:02:58

He had figures for both, I think, but the block propagation is more important.
Because we do have no transaction propagation guarantees, we have block propagation guarantees.
So one of those numbers is a lot more reliable than the other.

Josibake: 00:03:10

Yeah.
So anyways, we got the data from him.
There were some gaps in it where we would find periods of a day, a week, or an hour where all of a sudden all the transactions are in the ledger, but none of them are in his logs, which indicates maybe the node was down or not collecting.
So I started reaching out to other people and being like - "I heard you had some mempool data," and then taking all of that together and trying to build more comprehensive... the goal being for every transaction we see in the ledger, I also have a log of when it entered the mempool so we can say - this is when the transaction was first seen and this was when it was eventually mined.
So we have that from like 2017 onward where it's about 99.5% coverage, where 99.5% of the transactions in the ledger we also have a record in the mempool.
What I'm working on now is cleaning that, standardizing it, documenting it, and then writing a pipeline so we can just keep it running and continue collecting and then make that available to people, which I think is super exciting.
I think there's implications for doing research, backtesting assumptions and things like that, and there's also historical nuggets that are pretty interesting that you can go back in time and see weird things that happened.

### Creating a publicly available dataset

Adam Jonas: 00:04:12

So you have all this data, you've done a project with it.

Josibake: 00:04:16

Yep, in the works, we're finishing a paper.

Adam Jonas: 00:04:19

Cool.
So what's next?

Josibake: 00:04:20

The next thing is just making it available for other people.
I think one of the things about data analysis type work, the first most important thing to do is just start collecting it and putting it somewhere where other people can access it.
I don't even have to conceive of all the possible uses for it.
I just have to make it available and try to reduce the work that other people have to do to use it.
So if I've already done the cleaning, if I've already found edge cases, if I've already standardized the data, and then you can just come and get a clean data set that has a transaction and a timestamp and you don't have to fix the timestamps or standardize anything, you're much more productive, and then we can just see what comes from it.

Mark Erhardt: 00:04:51

It makes it much easier for people to reproduce, because very often there's data produced and people make some conclusions or assertions and nobody can reproduce them.

Josibake: 00:05:02

Then yeah, you can't really trust what comes from it.
I also think consistency is also super important.
If you do some work and you make a mistake, and then I have some data and I make a mistake in mine, it becomes a lot harder to reason through the conclusions and then compare conclusions.
If we all start from the same dataset and that dataset has a mistake in it, at least we've all made the same mistake, and it becomes easier to either find it, or fix it when we discover, okay, we were calculating this wrong and now everybody needs to fix stuff.
So consistency and reproducibility I think are super important.

Adam Jonas: 00:05:29

Do you think these data sets exist behind closed doors in academia or in chain analysis?

Josibake: 00:05:35

Absolutely.
Absolutely.
I can't believe we were the first four or five people to be like - "I'm going to start collecting mempool metrics."
So I think that's what I'm excited about, I'm sure people have been using this, but doing the work to make it available to everyone.
The open source philosophy, something I care about just in general, and I think could be super useful for Bitcoin.
I think there's implications for people who want to build fee estimation stuff, or we want to start reasoning about what the future looks like as the subsidy decreases, and now we have a data set to work and play with, and not everybody needs to go out and pay for it, or do the work to collect it themselves.
So I'm hoping it's a high leverage project.

Adam Jonas: 00:06:11

You have a data group coming together that seems to be interested in Bitcoin data analysis and Bitcoin data engineering.
So tell us a little bit about how that came together and what you all are thinking about.

Josibake: 00:06:21

It happened very organically, which was kind of cool.
My background before Bitcoin was data science and data engineering.
When I first started contributing to Bitcoin, I was drawn towards the more data-y stuff because I could provide immediate value while learning some of the other Bitcoin stuff and software engineering.
So got started there, and then as you start to reach out and talk to people, you find people in other corners who have been doing data stuff, and then they get excited, they're like - "Oh, here's somebody else who cares about data."
And we just started to work together.
So most recently we were in the Azores and finally got a bunch of these people who've been doing data stuff.
All the people that I ended up collecting mempool logs from, we were all there and we had a chat and was like, why don't we formalize this and let's make a group where we can start to chat more and collaborate.
I think there's an interest in it.

Usually with data stuff, you just keep collecting it and hoping that someone's going to be interested, and it feels like the time is right.
I think the big thing we want to do is start collecting lots of different data, agreeing on standard best practices and how to clean it, enrich it, store it, and make it more discoverable so that people have one place to go to. So many people can be feeding into it, and collecting this data and using it independently, but we're collating it all to be like, if you're interested in data, before you go out and collect it on your own, why not see if we're collecting it here and we're also willing to reach out and help you on these types of projects.

### What could it be used for?

Adam Jonas: 00:07:36

What are you hoping the outcome will be?

Josibake: 00:07:38

More empirical analysis and empirically driven development.
Like doing chain analysis and finding things where it's like, okay, let's quantify how big a problem is.
Let's see if we can fix it and then analyze the result.
I think there's kind of two ways to approaching software development, and you can do a combination of both.
Some people analyze it purely from theory and they think through how everything works and like, okay, this is the right thing to fix, and that's great.

There's other people who are like, let's just look at the data in the system, let's analyze how the system is working and try to find opportunities for improvement.
They might be opportunities that people were already aware of, but at least now we can quantify it - if we were to fix this, this is the impact.
That helps us prioritize these things.
It might also help us discover things that nobody had thought about before.
Like, that's odd, let's keep pulling at that thread, oh, we found this whole thing nobody thought about and now we can fix it and address it.
So that's kind of my goal.
I also think there's a storytelling aspect with data.
We can find interesting anomalies in history and make people aware of them, and that makes Bitcoin interesting.
It makes the whole thing kind of like, what happened in 2020 or 2021 when all the miners shot offline?
Okay, let's tell a story in data about that.

Adam Jonas: 00:08:40

Given your brush with academia, what more can be done there?

Josibake: 00:08:43

Academics love data.
And they don't like collecting it.
And they don't like cleaning it.
So build it and they will come.

Adam Jonas: 00:08:48

Yeah, I hope so.
Those are all ambitious and worthwhile goals, hopefully it happens.

Josibake: 00:08:54

Yeah, so Bitcoin may or may not be gold, but data is gold.
So that's one thing.

## Bitcoin Core wallet

Josibake: 00:08:58

Other things, I really like the Bitcoin Core wallet.

Adam Jonas: 00:09:01

You both like the wallet.
So let me ask the question, why the Bitcoin Core wallet?
Why don't you just slap on some JavaScript and turn into something pretty?

Josibake: 00:09:09

First problem is that you said JavaScript.

Mark Erhardt: 00:09:11

There are quite a few people that use the Bitcoin Core wallet, either because they don't want to trust any other projects, or they've always used it, or they are power users and find the RPC interface that allows them to do things that they can't do with other wallets.
So we have a very odd set of users about whom we don't know a lot.

Adam Jonas: 00:09:32

There were a couple of studies.
There's an MIT-sponsored study and then a Spiral-sponsored study on Bitcoin Core wallet users.
Achow helped design the survey that went out.

Josibake: 00:09:41

I think that can be directionally useful, but there's probably a lot that's not understood there.

Mark Erhardt: 00:09:46

One of the things that I would be interested in would be to get updated numbers on how many transactions we think might have been created by Bitcoin Core, which we should be able to find out via various fingerprints of things that only Bitcoin Core wallets do.

### Why have a wallet in Bitcoin Core?

Mark Erhardt: 00:09:59

What really excites me about the project is that it is sort of a showcasing of what you can do with wallets.
A lot of wallets focus on just usability and some on privacy, but there's very little of exploration of all the possibilities and the toolkit, the things that you can do with it is usually not as broad, which can be an overburdened API and it can make it hard for people to find out what all you can do.
But we do do some stuff that no other wallet does, I think.

Josibake: 00:10:30

Yeah, I think that's a great summary.
The Bitcoin Core wallet should be a very feature-rich wallet like, here's everything that's possible with Bitcoin, and here's examples that other wallets can follow, best practices.

Adam Jonas: 00:10:41

Like a reference implementation, maybe?

Josibake: 00:10:43

Yeah, a reference implementation, where have I heard that before?
I also think there's an accessibility component, we want to remove barriers for people using Bitcoin.
We want people to run their own node.
We want them to custody their own funds.
We want all of these things so we kind of owe it to them to make it easy to do.
Now for technical people I think we're fine downloading a software stack, we'll get some software from here, get some software from here, and then we're gonna stitch it all together and we know how to audit the supply chain of these different softwares that we're putting onto our computer, but for a non-technical user, that's daunting.

It's like, okay, you wanna use Bitcoin?
All right, well, here's all the phone wallets you first got to look at and figure out who to trust.
Then you got to run a node.
So you got to either download it from Core, or you got to go get one of these nodes in a box, or go to a custodial solution.
I think it's really important that there is a place that you can go download Bitcoin software.
I can download it, I can finish [IBD](https://btcinformation.org/en/glossary/initial-block-download), and I can start using it.
I think that's one of the things that the Bitcoin Core wallet provides.
You download the node, you use the node, you have a wallet, it all works right out of the box.
There are some, not guarantees, but you know that the builds are reproducible.
You know that there's been a lot of thought into the dependencies, into the security, and to me it should be a very accessible option for people.
If you get more specialized and you want to start stitching together different wallet software, you're totally free to do that, but we need this base offering for people.

Adam Jonas: 00:11:58

How do you think about how the wallet, which you two spend a lot of time on...

Josibake: 00:12:03

I use it.
I've forced myself, I use Bitcoin Core wallet to kind of like...

Adam Jonas: 00:12:09

A power user, one might say.

Josibake: 00:12:10

More to like eat my own dog food, if I get frustrated with the wallet, I can at least talk to people or try to fix it.

Adam Jonas: 00:12:16

But my question was the separation between wallet and GUI because a lot of novice users in particular, they will be interacting with the wallet through the GUI, which is not something that either of you spend a ton of time on.

Josibake: 00:12:26

I also use the GUI.

Adam Jonas: 00:12:28

I'm not saying spend a ton of time on in terms of using, I'm saying, based on your commit history.

### Separation of GUI from wallet

Adam Jonas: 00:12:33

You spend more time with the wallet and less time on the GUI, but there is a coupling there.

Mark Erhardt: 00:12:37

So where we certainly do not excel is UX.
There's a ton of things that happen in the Bitcoin Core wallet that don't happen elsewhere.
But I don't think that we necessarily, for example, make the cheapest or most private transaction.
I think that we have some privacy features that no other wallet has, but a wallet that will 100% focus on privacy will operate differently than Bitcoin Core.
It's more of a one size fits all and showcasing of what you can do, than the best wallet out there.

Adam Jonas: 00:13:05

Right, it's a well-rounded wallet.

Josibake: 00:13:06

That's what it should be, right?
I think there needs to be a wallet out there that does that.
Then you start with the well-rounded wallet and you have pretty good privacy, pretty good efficiency, pretty good security.
Then as you continue on your Bitcoin journey, you can go and have a 100% privacy focused wallet.

Adam Jonas: 00:13:22

Probably the best security you do particularly well.

Mark Erhardt: 00:13:24

I think that generally running a wallet on a computer has different threat profiles than one that is coupled with a hardware token, or like multi-sig out of the box where you generally have a two of three multi-sig setup and things like that are huge security improvements that are hard to replicate just with one piece of software.

Josibake: 00:13:45

Yeah, I would agree with that.

## Only use one input type when building transaction

Adam Jonas: 00:13:44

We started talking about this because you like the wallet.
What are you doing on the wallet?

Josibake: 00:13:49

Yeah, so one of the things I started with, I mentioned at the beginning.
We were doing this analysis of transactions and I'll probably get the name wrong, but there's the different script type heuristic where if all my inputs are `bech32` and then I'm paying to a Pay-to-Script-Hash output, and then I see a change output that is also `bech32`, it's pretty reasonable to guess that the `bech32` is the change output.

Mark Erhardt: 00:14:14

[Same input heuristic](https://en.bitcoin.it/wiki/Common-input-ownership_heuristic).

Josibake: 00:14:15

Yes, same input heuristic and pay to different script type outputs.

Mark Erhardt: 00:14:17

So you have a transaction with two wrapped SegWit inputs and one wrapped SegWit output, one native SegWit output.
What do you think happened here?
The idea is, if the input scripts match one of the outputs, that's the change output and the other one is the payment.

Josibake: 00:14:32

As we were doing this analysis, I was curious, how often does this happen and how many times could I just tag transactions and guess?
I think off the top of my head, the number was like 30% of transactions, we could make a reasonable guess as to the change output.

Mark Erhardt: 00:14:44

Just from this one heuristic...

Josibake: 00:14:45

Just from one heuristic that is extremely cheap to compute, you don't need to be throwing stuff into complicated databases or anything, you just look at the transaction.
Then that started the discussion, then there was a PR [(PR #24584 in Bitcoin Core)](https://github.com/bitcoin/bitcoin/pull/24584) in core for just matching the payment output type when you generate change, which I thought was a great improvement.

But as we started talking about it more and discussing some of the trade-offs, it was like - well, okay, if my wallet is native SegWit by default, and then I start accumulating these Pay-to-Script-Hash (P2SH) outputs in the wallet because I'm paying a lot of P2SH people, when those P2SH outputs are then combined with the native SegWit UTXOs on my wallet, you just have to look at the next hop and be like, okay, you improve the privacy for this one transaction, I can figure it out in the next one.
Since everything's on an immutable ledger that's going to last for thousands of years, if at any point in the future that privacy is ruined, it's a waste of effort or time to even do it in the first place.

There's differing opinions on this, but I agree with that, you need to solve it, it can't be a temporary thing.
So that got me thinking about coin selection and well, why don't we just try to spend same type UTXOs together?
Like if my wallet has some native SegWit and some P2SH that I've acquired through matching change outputs, and in the future I'm gonna pay a P2SH or anything really, group those UTXOs together, and it breaks this heuristic of being able to look at the next hop.
It started as what seemed like a simple idea, and then got deep into the weeds of the wallet and coin selection, and I learned a ton about it and I had a lot of fun and we were able to also quantify the improvement.

So in parallel, Achow had been working on a wallet simulation script, a framework, whatever you want to call it, and we started using that to be like, all right, let's make a change to coin selection.
Let's see how often this new logic would get triggered or not triggered.
Let's measure the waste metric.
Let's measure all these other things and ensure that we're not increasing the fees that a user would pay over time, et cetera.
We had a few people provide us anonymous wallet histories, and we grouped this into different scenarios.
Like you're this type of wallet, that type of wallet.
I think that was really fun too, we identified a problem by looking at data, then we quantified with data, we're actually solving the problem.
What we ended up finding with this, it did improve the privacy and it improved the efficiency or the cost.
What we mean by that is - over time, what's the total amount you would pay in fees?
It was like a 5% reduction in the total amount of fees you would pay over time, while also breaking this heuristic and improving the privacy.
So that's one of those rare win-wins, like it's cheaper and it's more private.
Where usually it's like, it's more private, but it's gonna cost a lot, or it's really cheap, but it's not private.

Adam Jonas: 00:17:08

You just make all the change outputs Pay-to-Taproot outputs, and then you can get your "When Taproot".

Josibake: 00:17:13

I'm not gonna touch that.

## How is working on the wallet?

Adam Jonas: 00:17:15

There seems to be some momentum in the wallet, there's like a working group.

Josibake: 00:17:18

I think it's a great place to cut your teeth on Core.
You're not doing anything with consensus, which is already like a load off.
I think it's easier to jump in, it's a localized problem.
The wallet has one job, one function, and it's a pretty well scoped function.
The wallet has a ton of work that can be done, there's a nice backlog.
So you come in and like, oh, okay, there's plenty of stuff to do here.
You can do something that is important that users will actually use.
There's kind of that connection of like, oh, if I made a change to coin selection, and so now anyone who uses Bitcoin Core is using my change to coin selection, that's cool, you feel very connected to the work you're doing.
So it's important work.

But for me, at least, and I don't want to speak for others, it was less stressful.
I felt like I could get into the wallet and start to work, play with stuff.
I also feel like the wallet is very testable.
It's perhaps more testable than peer to peer, like some of these network wide things that until you see it in the wild, it's hard to know what's going to happen, whereas with the wallet, we can scope it and test it, we can simulate and run scenarios.

Mark Erhardt: 00:18:15

It does have emergent behavior in the sense that your coin selection choices at this time will affect your UTXO pool for the future transactions, and you want to try to spend more of your UTXOs at low fees.
You want to compose a good UTXO pool so that you can find more changeless transactions.
You want to have enough UTXOs that you have reasonable financial privacy when you create transactions, but few enough that you don't have huge future costs if the fees just continue going up.
So there's this emergent behavior to it, but you can actually just run simulation scenarios, how the UTXO pool and the wallet will change over time with different strategies.
So it's fairly testable in the sense that you control all the moving pieces, and you can make some reasonable or less reasonable assumptions about how the fee rates change, what sort of transactions are being built and things like that.

Josibake: 00:19:04

I think everything he just mentioned is why the wallet is interesting.
There's tons of topics that I think are understudied and have real implication.
One of the fundamental things in Bitcoin is a transaction, and a transaction is created by a wallet.
There's tons of things that go beyond just the privacy and spending money and stuff like that and the emergent behavior that will affect the network.
Also, as we build layer two, there's interest in, okay, the wallet coin selection, these things might be making certain decisions and how it creates UTXOs in the wallet and the UTXO pool in your wallet, and what implications does that have for funding transactions for higher layers.
So again, there's a lot of cool topics that are both Bitcoin-y and computer science-y, and it's a nice sandbox within to work with.
You can test things, you can simulate things, and I think it's cool too.
You have a connection to the users.

## Cross-input signature aggregation

Adam Jonas: 00:19:48

Another thing that you seem to have been investigating is [cross-input signature aggregation](https://bitcoinops.org/en/topics/cross-input-signature-aggregation/).

Josibake: 00:19:55

My background is math.
I found computer science and the tech world through math.
So I've always had a deep intrigue and love of cryptography, and wanting to get better at it and know more about it.
I'm also very interested in privacy, and efficiency, and these types of things.

So I heard about cross-input signature aggregation like a year and a half ago, and the first time I heard about it, I was like, this is super cool, I want to learn more about this.
Then I got busy doing other stuff and it was still in the back of my mind.
So coming into this year, as I'm wrapping up the data project and thinking about, okay, what do I want to work on next?
I think that's what I want to spend some time on.
Both in educating myself, like how does it work, learning more about the cryptography, and also helping the people who have been working on it as like doing research, playing with implementations, proving use cases, because I think it's a really exciting (feature) for Bitcoin.

### Catching up on history

Adam Jonas: 00:20:39

So catch us up a little bit on the history, because originally this was all going to be part of the Taproot soft fork.
It was split out, but who's been working on it?
How long has it been talked about?
Is it today?

Josibake: 00:20:48

It's not a new idea for sure.
Long long ago in Bitcoin, we knew there would be a world in the future where we had [Schnorr signatures](https://bitcoinops.org/en/topics/schnorr-signatures/), and once we had Schnorr signatures, all these other things become possible, and cross-input signature aggregation was one of those things.

Then as Shnorr Signatures became a reality for Bitcoin through Taproot, then it was like, okay, well, let's just do all the Shnorr signature-y things at once.
Then some other people were like, that's a bad idea, we should break this out.
There was some discussions about - this is big enough on its own, we don't want to slow down Taproot.
We want to have more time to make sure it doesn't break other things in Bitcoin, that we fully understand the design space of it, so let's separate it out and let's just do Taproot, because Taproot is a necessary building block for it.
I think that was a really good decision.

So now the people that I'm aware of that have been working on it, there's Jonas Nick, I think Tim Ruffing, those are both people that I've heard talk about it.

Adam Jonas: 00:21:37

The usual Blockstream suspects.

### Writing the BIP with Hacspec

Josibake: 00:21:38

Those are the ones that I'm most aware of, but I'm sure there's others.
Just because I'm not aware of it doesn't mean that they're not doing important work.
I think one of the things that also made me decide to spend some effort and time on this was there was a draft BIP that was proposed recently for a scheme for [half-aggregation of Schnorr signatures](https://bitcoinops.org/en/newsletters/2022/07/13/#half-aggregation-of-bip340-signatures) like Taproot.
I think they even referenced the BIP number.
There's kind of something concrete to work with.

There were some decisions made in that BIP, and I'm going to butcher the names or get them wrong, but they spent some time to write the specification in something called [Hacspec](https://hacspec.org/), which is this Rust-like language that you can define a cryptographic scheme in, and then you can run these proof validators on it to get proofs of validity, proofs of security, and things like that.

It might be the first one that's doing this in Bitcoin Core, but you get all this power right out of the box.
I'm like, okay, we're writing it in this, so then we get these guarantees of security, and we can write test vectors and other things.
So it's a cool area to work, and a lot of tooling is already there.
When I see people putting effort into something, it feels like, okay, there's some momentum here.
I don't want to come and spend a bunch of time on something because I think it's cool, and there's no momentum behind it, and then six months later, it's like, well yeah I learned a lot about this thing that's never going to happen.
So when I'm deciding what to work on, I look for momentum and I feel there's some momentum there.

### Thoughts on shipping cross-input signature aggregation separately

Adam Jonas: 00:22:47

So a couple questions.
One is, Murch, you were shaking your head when Josie said why it was a good decision to split it out.
Why?

Mark Erhardt: 00:22:54

I was shaking my head because there's a few different arguments in both directions.
So on the one hand, when Taproot was pretty much done, what we ship now as Taproot, cross-input signature aggregation very much was still in the design phase.
So it was just at a very different level of preparedness and that's why it got taken out and delayed.
Also Taproot was starting to size up to a pretty substantial soft fork already and in itself is introducing a bunch of extension possibilities, a new output format, a new signature type.
Adding to that, instead of treating inputs as separate things on transactions to have a single signature per all the Shnorr capable signatures on a transaction, and then having mixed output types on the transaction and some of their signatures can be aggregated.
It was a very orthogonal thing to most of the other things that were shipped with Taproot.

The very interesting thing if we had been able to ship cross-input signature aggregation with Taproot would have been that it would have given a financial incentive for people to do multi-party transactions, where multiple users get together to provide multiple inputs to the transaction and create outputs together.
It would have broken the same ownership heuristic that we've talked about a little bit already, where most blockchain analytics approaches assume that any inputs spent on a transaction are owned by the same entity, and now once you aggregate signatures it becomes cheaper to build transactions with other parties than by yourself.
So I strongly believe that Pay-to-Taproot will be the dominant output type in five to seven years.
If we had shipped it with cross-input signature aggregation, we would have shipped a privacy improvement that is financially attractive.
You would not need to say, oh, I'm doing this for privacy, no, I'm doing this because it's cheaper.

Josibake: 00:24:40

It's a really important point.
Privacy and some of these other things like cost and usability are usually very much on opposite ends for each other.
You have to choose one or the other and you have to make a compromise.
Once in a while, something comes along that's like, why not both?
Really, I think the only way you'll have a reasonable degree of privacy is if there's an economic incentive to do it.
Because most people don't care until the privacy is broken, until the privacy has been exploited, and at that point it's too late.
So if you want people to have privacy, even if they don't care about it now, they don't understand why it's important, then you make it economically attractive for them to do so.
To me that's a very rare moment and it's exciting.

Mark Erhardt: 00:25:15

You have to make it the default choice and people are gonna opt out if it's more expensive still sometimes.
So it has to be the default choice and cheaper.
That would have been the exciting thing that we could have shipped here.
But it was, as I said, years away from being shipped and I think Taproot shipped at a good time, so maybe if we do get another output type in the future, maybe based on Pay-to-Contract and similar to the Taproot outputs right now we will ship it with that.

Adam Jonas: 00:25:43

Yeah, just as a counterpoint, it does seem like soft forks are becoming increasingly difficult to get community consensus on.
So every time you ship a soft fork, it might be a little bit harder. Seemingly soft forks haven't been parallelized much, so it might not be in line, for example.

Josibake: 00:26:02

I think it's a good point and also a separate discussion, but I don't think that should reason... all the points about cross-input signature aggregation being a very big design space that needs its own special attention.
We shouldn't decide how seriously we're going to research and test and vet something based on whether or not it will be easier to soft fork or not.
That's my opinion.
I think you should give something its proper due diligence and then talk about activating it.

Adam Jonas: 00:26:25

I'm just playing devil's advocate here.
Now that Bitcoin is mainstream, putting in more privacy features seems like you're pushing water uphill a bit, like you're sort of picking a fight with the powers that be as opposed to if you got this in five years ago.

Mark Erhardt: 00:26:37

Yeah I think that as more regulated entities enter the space and have opinions on the space, I think it might get more scrutiny to have a privacy improvement.

Adam Jonas: 00:26:46

Given that the largest pool is now in the United States, it just becomes more complicated.

Mark Erhardt: 00:26:51

So one of the big problems with shipping cross-input signature aggregation at a later date is that it cannot be combined with Pay-to-Taproots.
It is spec incompatible to change how the signatures work on Pay-to-Taproot.
So an old node will not accept a cross-input signature aggregation transaction, so that would be a hard fork to add it to the existing Pay-to-Taproot outputs.
So we'll have to get people yet again to update their default output types, and as we've seen with SegWit, native SegWit adoption is five years in.
Now we have 70% to 80% of the transactions use SegWit and something like 45% of the inputs are native SegWit.
But it'll be another five to seven years or so until that is the case for Pay-to-Taproot, and once we push out another output type, it'll take forever again.

Adam Jonas: 00:27:37

And so what are the problems with it that are currently being reasoned through?

Josibake: 00:27:40

Ask me in six months.

Adam Jonas: 00:27:41

Okay.

Josibake: 00:27:41

But that's kind of the point of why I want to spend some time on it.
When you say like, oh, I'm going to spend time researching something, a very viable and likely outcome when you take on something in a research capacity is, okay, I learned that this is not a good idea.
That's valuable input, and that's valuable to tell other people, okay, I spent some time looking into this and here's everything that I learned and yada yada.
And now I've updated my opinion on it, I'm not excited about it anymore.
Sometimes people forget that.
Sometimes you need people to research something and take an idea as far as you can take it, to convince yourself it's a bad idea, or to convince yourself it's a good idea.
Ideally, when you go into it, you're kind of a blank slate and be like, this seems really cool to me, It seems promising, but let's see if there are show stopping problems or if it's feasible or not, or if the risks outweigh the benefits.

## Onboarding to Bitcoin development

Adam Jonas: 00:28:22

You're a social guy, you seem to like people.
Tell us how you're working with your buddies and dragging more people into Bitcoin development.

Josibake: 00:28:30

Getting more people involved in Bitcoin development is super important.
It's something that I care a lot about.
I want to see developers in the pipeline.
I think it takes a while to fully understand Bitcoin and be making meaningful contributions, and if that's true, you need a pipeline of people learning and growing in their knowledge.

Adam Jonas: 00:28:45

How long do you think it takes?

Josibake: 00:28:47

For me, I think it's three years, that's the number I set for myself.
I said, okay, I want to get into Bitcoin development.
The first year, I'm not going to do anything useful, I'm going to learn a lot.
The second year, maybe I'm starting to do some more impactful and useful things.
Then the third year is like really like, okay, I'm making valuable contributions to Core.

Adam Jonas: 00:29:04

2023 is gonna be a big year.

Josibake : 00:29:05

It's gonna be a big year.

Josibake: 00:29:07

Big things coming.
Stamp it.
But I don't think that's unique to Bitcoin, right?
I think that happens in the software development industry too.
You come in and you start learning a new tech stack or a new technology and you're not really doing anything useful.
Of course there's outliers, but initially you're not really doing anything useful, you're doing the grunt work that other people don't want to do.
You're learning a lot.
Second year, you're kind of owning a project, something's kind of your own thing, or you're working with other people.
Then the third, or if we didn't want to talk years, now you're like staff or principal.
Now you're really doing big things, you're an important person or a respected voice in the space.

I think that's true for Bitcoin.
So then let's keep the pipeline primed, let's keep people learning and growing.
That's how I found Bitcoin, doing the Chaincode seminar, and I thought it was fantastic.
So something I've tried to do is get as much leverage out of that as I can.
So I took the seminar curriculum and I got some friends together.

### Running the seminar with friends

Josibake: 00:29:52

I had a bunch of friends asking me about like, oh, like you just did a career change, you're working on Bitcoin and they all had their own independent questions.
So like this person would ask me a question, then another friend would ask me the exact same question, and I was like, look, why don't we all just get together, we'll meet once a week, and here's this nice curriculum of material that we can read in the meantime.
I pretty much just forked and copied the Chaincode seminar format, and we went much slower.

It was much more like we all knew each other, so it was more fun and enjoyable.
If people got busy, we were like, oh, let's just meet next week, or, hey I didn't really understand this week, let's read it again.
Are there any additional resources?
So it was a fun, slowed down version that I feel like we got a lot more out of, and it was enjoyable.
Everybody learned a lot and everybody said they enjoyed it, and then a few of them actually went on to join the official Chaincode seminar cohorts.
So that's something I would encourage a lot of people to do.

If you work in Bitcoin, or you know a lot about it, and you have people talking to you and asking you questions or people who are also software engineers and they're interested and they don't know where to start, just use the material.
It's all for free.
The benefit to Chaincode then, you can provide recommendations as you go through and be like...

Adam Jonas: 00:30:54

You don't need to benefit Chaincode.
I think the idea of putting effort into that is that people do their own thing.
I'd love it if the community updated that content on its own.
So in a parallel, Bitcoin transcripts is also something that we're involved with, and some guy showed up, cares a lot about it, he's now the maintainer of Bitcoin transcripts.
So that's great if someone else takes it over, and I think something similar here would be awesome.

### Giving back to open source

Josibake: 00:31:16

I agree.
I think the broader point is when you use open source materials, always look for a way to give back.
That's just how we keep open source alive in a healthy community.
If everyone becomes takers, people get burnout, people leave.
So if you're going to use a free resource, try to find a way to give back to that and improve it for the next person who's gonna use it.
So as we went through the material, we would notice where a link was dead or maybe that wording could be changed, or  I found this other great resource.
I was constantly telling them, hey, just open up a pull request, add it to the repo, tell someone about it.

We did a lot too where we got a lot more hands on.
We forked Bitcoin Core, we kind of basically just created our own little private network, and we were mining with CPUs, and going through simulated soft fork upgrades, and that was cool for me to see the excitement when you get really hands on with it, and you learn by doing.
So out of that I had some ideas of, what are some ways we could make that more of a teaching tool, a very hands-on experience.

So the main point is, use these free resources.
But as you use them, be mindful of - how can I give back and make this more useful?
But yeah, I thought it was a great experience.
It was also a way to kind of, if you get annoyed with your friends all asking you the same question from five different places, just get them all together on a video call once a week and make them read all that stuff.
Do your homework.

Adam Jonas: 00:32:22

Well, thank you for coming in and sharing what you're up to.

Josibake: 00:32:26

Thank you for having me.

## Conclusion

Adam Jonas: 00:32:33

You two have been doing quite a bit of collaboration together it sounds like.
But it was good for me to find out what's going on.

Mark Erhardt: 00:32:39

Cool, glad to hear it.

Adam Jonas: 00:32:40

I liked the cross-input signature aggregation conversation.
It's something that continues to be in the back of my mind after it was split out from Taproot.
It seems like it's just such a win.
Gotta get it in.

Mark Erhardt: 00:32:52

Yeah, it'll still take quite some work.
I think it'll be interesting to see how we can even put it in because we'll need a new output type and that new output type should be financially incentivized.
We want people in the long term to converge on one output type, for privacy.

Adam Jonas: 00:33:08

Do you think that there's enough use cases for Taproot without this?

Mark Erhardt: 00:33:12

Oh, yeah.
I think it's very obvious that Taproot will be used a lot for multi-sig stuff.
I think that there's very powerful things you can do with single-sig that you can't do without other output types, just via the script path fallbacks and the tweaks.
I mean, you can tweak ECDSA signatures too, but it's more baked in the Pay-to-Taproot output.
Between those things, I see that Pay-to-Taproot will be the standard and default output very soon.

Adam Jonas: 00:33:38

Yeah.
I just feel like cross-input signature aggregation would have been such an immediate win.
I feel like the community would have picked up on it really fast.

Mark Erhardt: 00:33:46

Yeah.
So if you have any cool data stuff to do, you should totally reach out to Josie.

Adam Jonas: 00:33:51

The thing I like about him, and he's only been doing this for a couple of years, the guy's a giver.
He doesn't just take, he's really mindful about people who have been generous to him, and giving back to the community, and we didn't talk about his climb to funding or anything like that but he's just very cognizant of how he can be helpful immediately and how he can pitch in.
So, it's great!

Mark Erhardt: 00:34:10

Well, it was a fun conversation.

Adam Jonas: 00:34:12

Cool.
I hope you enjoyed this one as much as we did, and we're gonna keep trying to put these out, so hopefully we'll be speaking with you soon.
