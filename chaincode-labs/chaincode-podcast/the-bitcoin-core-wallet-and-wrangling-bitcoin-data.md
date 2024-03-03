---
title: "The Bitcoin Core wallet and wrangling bitcoin data"
transcript_by: kouloumos via tstbtc v1.0.0 --needs-review
media: https://podcasters.spotify.com/pod/show/chaincode/episodes/Josibake--the-Bitcoin-Core-wallet-and-wrangling-bitcoin-data---episode-24-e1piaje
tags: ['bitcoin-core', 'signature-aggregation', 'wallet']
speakers: ['Josibake']
categories: ['podcast']
summary: "Josibake joins us to talk about his work on the Bitcoin Core wallet, bitcoin data and onboarding to bitcoin development."
episode: 24
date: 2022-10-21
---
Speaker 0: 00:00:00

Hey, Merch! Yo, what's up?
We are back, as promised.
Great.
We're really following through this time.
We have Josie Baker in the office this week, and we're going to hear about what he's up to.

Speaker 1: 00:00:11

Yeah, we've been working with him on some mempool data stuff, And I've also worked with him closely on some Bitcoin Core wallet privacy improvements and that's fun stuff.

Speaker 0: 00:00:19

Sounds like you already know all the answers, but I'm going to find out what you all are up to.
And so hope you enjoy.
Welcome, Josie.
We tried to get you in the studio last time, but too busy.

Speaker 2: 00:00:35

We were very productive last time.
Many things had to be talked about, discussed, brainstormed.

Speaker 0: 00:00:40

So tell us about sort of the kind of work you've been doing now.
How long have you been doing this Bitcoin thing for?

Speaker 2: 00:00:45

I want to say I've passed the year mark, so about a year and a half.
I would consider the start the Chaincode seminar, which would have been maybe the 2021.
Yeah, so it would have been the 2020 online seminar that I participated in.
Almost two years.
Incredible.
In terms of what I've been up to, lots of data analysis stuff.
So working with mempool data, mostly collecting data that people were wise enough to start collecting years ago and just were kind of sitting on and taking that, standardizing it, putting it all together, cleaning it a little bit, and working with one of Chaincode's own, Clara, on a research paper, analyzing that data.
The real goal for me is to then open source it and make it available for other people to use and hopefully find utility and interesting things from it.

## Analyzing historical transaction data

Speaker 0: 00:01:25

Super cool.
Let's start with the project itself and then maybe you can talk more generally about data and what you like to do with Bitcoin data?

Speaker 2: 00:01:32

Yeah, so the project itself started with, we wanted to look at transactions and we didn't really want to look at anything in particular.
We just wanted to start looking and analyzing transactions.
Some ideas we threw out there were, is there anything in fee behavior or transaction construction that leads to wallet fingerprints?
And is that something that we can make people aware of?
Is there anything we can learn about fees and transactions and offer improvements?
That led into some wallet work where we looked at historical transactions, we applied some chain analysis heuristics to them and saw 30% of all transactions fit one of the heuristics pretty easily.
And so we're like, okay, that seems like something we should address.
And that led to work in core, which we can talk a little bit about later.
But as we were looking at this, one of the things that kept coming up was, okay, well, we have all this stuff on the blockchain, and everybody can analyze it.
But what we don't have is the mempool.
And then someone would be like, oh, I have some mempool data, and it's like for this month or this week, and it's in this format.
And then someone else would be like, oh, I think I have some too, but it has a bug or an issue, or it's a totally different format and I'm missing.
So I started to reach out to people who I knew were interested in collect this stuff and be like, how much do you have and can I have it and are you interested in collecting it?
And so we got some from Christian Decker, who had been collecting it for a long time.
Basically his node was logging every time a transaction entered the mempool, I think all the way back to 2012.
And it was maybe the basis of one of his earlier papers about propagation to the network.

Speaker 1: 00:02:52

Transaction propagation.

Speaker 2: 00:02:53

Yeah, it's actually block propagation.

Speaker 1: 00:02:55

Oh, yeah, right.

Speaker 2: 00:02:56

I thought it was about transaction propagation.

Speaker 1: 00:02:58

And then he had figures for both, I think, but the block propagation is more important.
Because we do have no transaction propagation guarantees.
We have block propagation guarantees.
So one of those numbers is a lot more reliable than the other.

Speaker 2: 00:03:10

Yeah.
So anyways, we got the data from him.
There were some gaps in it where, you know, we would find periods of like a day or a week or an hour where all of a sudden all the transactions are in the ledger, but none of them are in his logs, which indicates maybe the node was down or not collecting.
So I started reaching out to other people and being like, I heard you had some mempool data and heard you had some mempool data and then taking all of that together and trying to build like a more comprehensive, the goal being like for every transaction we see in the ledger, I also have a log of when it entered the mempool so we can say this is when the transaction was first seen and this was when it was eventually mined.
So we have that from like 2017 onward where it's like 99.5% coverage, where 99.5% of the transactions in the ledger, we also have a record in the mempool.
And what I'm working on now is cleaning that, standardizing it, documenting it, and then writing a pipeline so we can just keep it running and continue collecting and then make that available to people, which I think is super exciting.
I think there's implications for doing research, backtesting assumptions and things like that.
And there's also just historical nuggets that are pretty interesting that you can go back in time and see weird things that happened.

## Creating a publicly available dataset

Speaker 0: 00:04:12

So you have all this data, You've done a project with it.

Speaker 2: 00:04:16

Yep.
In the works.
We're finishing a paper.

Speaker 0: 00:04:19

Cool.
So what's next?

Speaker 2: 00:04:20

The next thing is just making it available for other people.
I think one of the things about data analysis type work, the first most important thing to do is just start collecting it and putting it somewhere where other people can access it.
I don't even have to conceive of all the possible uses for it.
I just have to make it available and try to reduce the work that other people have to do to use it.
So if I've already done the cleaning, if I've already found edge cases, if I've already standardized the data, and then you can just come and get a clean data set that has a transaction and a timestamp and you don't have to fix the timestamps or standardize anything, you're much more productive and then we can kind of just see what comes from it.

Speaker 1: 00:04:51

It makes it much easier for people to reproduce because very often there's data produced and people make some conclusions or assertions and nobody can reproduce them.

Speaker 2: 00:05:02

Then yeah, you can't really trust what comes from it.
I also think consistency is also super important.
If you do some work and you make a mistake and then I have some data and I make a mistake in mine, it becomes a lot harder to reason through the conclusions and then compare conclusions.
If we all start from the same dataset and that dataset has a mistake in it, at least we've all made the same mistake and it becomes easier to either find it or fix it when we discover, okay, we were calculating this wrong and now everybody needs to fix stuff.
So like consistency and reproducibility I think are super important.

Speaker 0: 00:05:29

Do you think these data sets exist behind closed doors in academia or in chain analysis?

Speaker 2: 00:05:35

Absolutely.
I can't believe we were the first couple, four or five people to be like, I'm going to start collecting mempool metrics.
And so I think that's what I'm excited about is I'm sure people have been using this, but doing the work to make it available to everyone.
I mean, the open source philosophy, something I care about just in general, and I think could be super useful for Bitcoin.
I think there's implications for like people who want to build fee estimation stuff, or we want to start kind of reasoning about what the future looks like as the subsidy decreases.
And now we have a data set to kind of work and play with and not everybody needs to go out and pay for it or do the work to collect it themselves.
So I'm hoping it's a high leverage project.

Speaker 0: 00:06:11

So you have a data group coming together that seems to be interested in Bitcoin data analysis and Bitcoin data engineering.
So tell us a little bit about how that came together and what you all are thinking about.

Speaker 2: 00:06:21

It happened very organically, which was kind of cool.
So my background before Bitcoin was data science and data engineering.
When I first started contributing to Bitcoin, I was kind of drawn towards the more data-y stuff because I could provide immediate value while learning some of the other Bitcoin stuff and software engineering.
So got started there, and then as you just start to reach out and talk to people, you find people in other corners who have been doing data stuff, and then they get excited.
They're like, oh, here's somebody else who cares about data.
And we just kind of started to work together.
So most recently we were in the Azores and finally got a bunch of these people who've been doing data stuff.
Like all the people that I ended up collecting mempool logs from, we were all there and we had a chat and was like, why, yeah, why don't we kind of formalize this and let's make a group where we can start to chat more and collaborate.
And I think there's an interest in it.
And usually with data stuff, you just keep collecting it and hoping that someone's going to be interested.
And it feels like the time is right.
I think the big thing we want to do is start collecting lots of different data, agreeing on standard best practices and how to clean it, enrich it, store it, and make it more discoverable so that people kind of have one place to go to.

## What could it be used for?

Speaker 2: 00:07:22

So many people can be feeding into it and collecting this data and using it independently, but we're kind of collating it all to be like, if you're interested in data, before you go out and collect it on your own, why not see if we're collecting it here and we're also willing to reach out and help you on these types of projects And what are you hoping the outcome will be more empirical analysis and I would say empirically driven development Like doing chain analysis and finding things where It's like, okay, let's quantify how big a problem is.
Let's see if we can fix it and then analyze the result.
I think there's kind of two ways to approaching software development.
And you can do a combination of both.
Some people kind of analyze it purely from theory and they think through how everything works and like, okay, this is the right thing to fix.
And that's great.
There's other people who are like, let's just kind of look at the data in the system, let's analyze how the system is working and try to find opportunities for improvement and they might be opportunities that people were already aware of, but at least now we can quantify it.
If we were to fix this, this is the impact.
And that helps us prioritize these things.
It might also help us discover things that nobody had thought about before.
Like, that's odd.
Let's keep pulling at that thread.
Oh, we found this whole thing nobody thought about and now we can fix it and address it.
So that's kind of my goal.
I also think there's a storytelling aspect with data.
We can find interesting anomalies in history and kind of make people aware of them.
And that makes Bitcoin interesting.
It makes the whole thing kind of like, what happened in 2020 or 2021 when all the miners shot off line?
Okay, let's tell a story in data about that.

Speaker 0: 00:08:40

Given your brush with academia, what more can be done there?

Speaker 2: 00:08:43

Academics love data, and they don't like collecting it.
And they don't like cleaning it.
So build it and they will come.

Speaker 0: 00:08:48

Yeah, I hope so.
I mean, I guess those are all ambitious and worthwhile goals.
Just hopefully it happens.

Speaker 2: 00:08:54

Yeah, so Bitcoin may or may not be gold, but data is gold.
So that's one thing.

## Bitcoin Core wallet

Speaker 2: 00:08:58

Other things, I really like the Bitcoin Core wallet.

Speaker 0: 00:09:01

So you both like the wallet.
And so let me ask the question, why the Bitcoin Core wallet?
Why don't you just slap on some JavaScript and turn into something pretty?

Speaker 2: 00:09:09

First problem is that you said JavaScript.

Speaker 1: 00:09:11

There are quite a few people that use the Bitcoin Core wallet, either because they don't want to trust any other projects, or they've always used it, or their power users can find the RPC interface that allows them to do things that they can't do with other wallets.
So we have a very odd set of users above whom we don't know a lot.

Speaker 0: 00:09:32

There were a couple of studies.
There's an MIT-sponsored study and then a Spiral-sponsored study on Bitcoin Core wallet users.
HL helped design the survey that went out.

Speaker 2: 00:09:41

I think that can be directionally useful, but there's probably a lot that's not understood there.
Totally.

Speaker 1: 00:09:46

One of the things that I would be interested in would be to get updated numbers on how many transactions we think might have been created by Bitcoin Core, which we should be able to find out via various fingerprints of things that only Bitcoin Core wallets do.

## Why have a wallet in Bitcoin Core?

Speaker 1: 00:09:59

And What really excites me about the project is that it is sort of a showcasing of what you can do with wallets.
And a lot of wallets focus on just usability and some on privacy, but there's very little of just exploration of all the possibilities and the toolkit, the things that you can do with it is usually not as broad, which can be an overburdened API and it can make it hard for people to find out what all you can do.
But we do do some stuff that no other wallet does, I think.

Speaker 2: 00:10:30

Yeah, I think that's a great summary.
Like the Bitcoin Core wallet should be a very feature-rich wallet of like, here's everything that's possible with Bitcoin.
And here's examples that other wallets can follow, best practices.

Speaker 0: 00:10:41

Like a reference implementation, maybe?

Speaker 2: 00:10:43

Yeah, a reference implementation.
Where have I heard that before?
I also think there's an accessibility component of like we want to remove barriers For people using Bitcoin.
We want people to run their own node.
We want them to custody their own funds We want all of these things so we kind of owe it to them to make it easy to do now for technical people I think we're fine downloading a software stack, we'll get some software from here, get some software from here, and then we're gonna stitch it all together and we know kind of how to audit the supply chain of these different softwares that we're putting onto our computer.
But for a non-technical user, that's daunting.
To be like, okay, you wanna use Bitcoin?
All right, well, here's all the phone wallets you first gotta look at and figure out who to trust.
And then you got to run a node.
So you got to either, you know, download it from core or you got to go get one of these nodes in a box or go to a custodial solution.
And I think it's really important that there is a place that you can go download Bitcoin software.
I can download it.
I can finish IBD and I can start using it.
I think that's one of the things that the Bitcoin Core wallet provides.
You download the node, you use the node, you have a wallet, it all works right out of the box.
There are some, not guarantees, but you know that the builds are reproducible.
You know that there's been a lot of thought into the dependencies, into the security, and to me it should be a very accessible option for people.
If you get more specialized and you want to start stitching together different wallet software, you're totally free to do that, but we need kind of this base offering for people.

Speaker 0: 00:11:58

And how do you think about how the wallet, which you two spend a lot of time on.

Speaker 2: 00:12:03

I use it.
I've forced myself, like all of my, I use Bitcoin Core wallet to kind of like...
A power user, one might say.
More to like eat my own dog food.
And like, if I get frustrated with the wallet, I can at least talk to people or try to fix it.

Speaker 0: 00:12:16

But my question was the separation between wallet and GUI because a lot of novice users in particular, they will be interacting with the wallet through the GUI, which is not something that either of you spend a ton of time on.

Speaker 2: 00:12:26

I also use the GUI.

Speaker 0: 00:12:28

I'm not saying spend a ton of time on in terms of using, I'm saying, based on your commit history.

## Separation of GUI from wallet

Speaker 0: 00:12:33

You spend more time with the wallet and less time on the GUI, but there is a coupling there.

Speaker 1: 00:12:37

So where we certainly do not excel is UX.
And there's a ton of things that happen in the Bitcoin Core wallet that don't happen elsewhere.
But I don't think that we necessarily, for example, make the cheapest or most private transaction.
I think that we have some privacy features that no other wallet has, but a wallet that will 100% focus on privacy will operate differently than Bitcoin Core.
It's more of a one size fits all and showcasing of what you can do, then the best wallet out there.
Right.

Speaker 0: 00:13:05

It's a well-rounded wallet.

Speaker 2: 00:13:06

And that's what it should be, right?
And I think there needs to be a wallet out there that does that.
And then you start with the well-rounded wallet and you know, you have pretty good privacy, pretty good efficiency, pretty good security.
And then as you continue on your Bitcoin journey, you can go and have a 100% privacy focused wallet.

Speaker 0: 00:13:22

Probably the best security you do particularly well.

Speaker 1: 00:13:24

I think that generally running a wallet on a computer has different threat profiles than say one that is coupled with a hardware token or like multi-sig out of the box where you Generally have a two or three multi-sig setup and things like that are Huge security improvements that are hard to replicate just with one piece of software.

## Only use one input type when building transaction

Speaker 0: 00:13:44

I would agree with that So we started talking about this because you like the wallet.
What are you doing on the wallet?

Speaker 2: 00:13:49

Yeah, so one of the things I started with, I mentioned at the beginning, so we were doing this analysis of transactions and I'll probably get the name wrong, but there's the different script type heuristic where If all my inputs are batch 32 and then I'm paying to pay to script hash output And then I see a change output that is also batch 32 Pretty reasonable to guess that the batch 32 is the change output.
Same input heuristic Yes, same input heuristic and pay to different script type outputs.

Speaker 1: 00:14:17

So you have a transaction with two wrapped segwit inputs and one wrapped segwit output, one native segwit output.
What do you think happened here?
So the idea is of course, if the input scripts match one of the outputs, that's the change output and the other one is the payment.

Speaker 2: 00:14:32

As we were doing this analysis, I was curious, like how often does this happen and how many times could I just tag transactions and guess?
And I think off the top of my head, I think the number was like 30% of transactions.
We could make a reasonable guess as to the change output,
which just from this one heuristic, that is extremely cheap to compute.
Like you don't need to be throwing stuff into complicated databases or anything.
You just kind of look at the transaction.
So then that kind of started the discussion.
And then there was a PR in core for just matching the payment output type when you generate change, which I thought was a great improvement.
But as we started talking about it more and discussing some of the trade-offs, it was like, well, okay, if my wallet is native segwit by default, and then I start accumulating these pay-to-script hash outputs in the wallet because I'm paying a lot of pay-to-script hash people, when those pay-to-script hash outputs are then combined with the native segwit UTXOs on my wallet, you just kind of have to look at the next hop and be like, okay, you improve the privacy for this one transaction.
I can figure it out in the next one.
And since everything's on an immutable ledger, that's going to last for thousands of years.
If at any point in the future, that privacy is ruined, it's kind of like a waste of effort or time to even do it in the first place.
And there's differing opinions on this, but I kind of agree with that.
Like you need to solve it.
Like it can't be a temporary thing.
So then that kind of got me thinking about like coin selection and well, why don't we just try to spend same type UTXOs together?
Like if my wallet has some native segwit and my wallet has some pay to script hash that I've acquired through matching change outputs And then in the future I'm gonna pay a pay to script hash or anything really group those UTXOs together and it breaks this heuristic of being able to kind Of look at the next hop It started as what seemed like kind of a simple idea and then got deep into the weeds of the wallet and coin selection and I learned a ton about it and I had a lot of fun and we were able to also quantify the improvement.
So we in parallel, H.I. Had been working on a wallet simulation script, a framework, whatever you want to call it.
And we started using that to be like, all right, let's make a change to coin selection.
Let's see how often this new logic would get triggered or not triggered.
Let's measure the waste metric.
Let's measure all these other things and ensure that we're not increasing the fees that a user would pay over time, et cetera.
And we had a few people provide us anonymous wallet histories.
And we grouped this into different scenarios.
Like you're this type of water, that type of wallet.
I think that was really fun too, of like, we identified a problem by looking at data.
Then we quantified with data.
We're actually solving the problem.
And what we ended up finding with this, it did improve the privacy and it improved the efficiency or the cost.
What we mean by that is over time, what's the total amount you would pay in fees?
And it was like a 5% reduction in the total amount of fees you would pay over time while also breaking this heuristic and improving the privacy.
So that's kind of like one of those rare win-wins, like it's cheaper and it's more private.
Where usually it's like, it's more private, but it's gonna cost a lot, or it's really cheap, but it's not private.

Speaker 0: 00:17:08

You just make all the change outputs, pay to tap root outputs, and then you can get your win tap root.

Speaker 2: 00:17:13

I'm not gonna touch that.

## How is working on the wallet?

Speaker 0: 00:17:15

So there seems to be some momentum in the wallet.
There's like a working group.

Speaker 2: 00:17:18

I think it's a great place to cut your teeth on core.
Like you're not doing anything with consensus, which is kind of already like a load off and I think it's easier to kind of jump in.
It's kind of a localized problem.
Like the wallet has one job, one function, and it's pretty well scoped function.
The wallet has a ton of work that can be done.
There's like a nice backlog.
So you come in and like, oh, okay, there's plenty of stuff to do here.
And you can do something that is important that users will actually use.
Like There's kind of that connection of like, oh, if I made a change to coin selection, and so now anyone who uses Bitcoin Core is using my change to coin selection, that's cool.
You feel very connected to the work you're doing.
So it's important work.
But for me, at least, and I don't want to speak for others, it was less stressful.
I felt like I could get into the wallet and start to work, play with stuff.
I also feel like the wallet is very testable.
It's perhaps more testable than like peer to peer, like some of these network wide things that are like, until you see it in the wild, it's hard to know what's going to happen.
Whereas with the wallet, we can kind of like scope it and test it.
We can simulate and run scenarios.

Speaker 1: 00:18:15

It does have emergent behavior in the sense that your coin selection choices at this time will affect your UTXO pool for the future transactions and you want to try to spend more of your UTXOs at low fees.
You want to compose a good UTXO pool so that you can find more changeless transactions.
You want to have enough UTXOs that you have reasonable financial privacy when you create transactions, but few enough that you don't have huge future costs if the fees just continue going up.
And so there's this emergent behavior to it, but you can actually just basically run simulation scenarios, how the UTXO pool and the wallet will change over time with different strategies.
So it's fairly testable in the sense that you control all the moving pieces and you can make some reasonable or less reasonable assumptions about how the fee rates change, what sort of transactions are being built and things like that.

Speaker 2: 00:19:04

And I think everything he just mentioned is why the wallet is interesting.
There's tons of topics that I think are understudied and have real implication.
One of the fundamental things in Bitcoin is a transaction and a transaction is created by a wallet.
There's tons of things that go beyond just the privacy and spending money and stuff like that and like the emergent behavior that will affect the network.
I think there's also, as we build layer two, is there's interest in, okay, the wallet point selection, these things might be making certain decisions and how it creates UTXOs in the wallet and the UTXO pool in your wallet, and what implications does that have for funding transactions for higher layers.
So again, there's a lot of cool topics that are both Bitcoin-y and computer science-y, and it's a nice sandbox within to work.
You can test things, you can simulate things, And I think it's cool too.
You have a connection to the users.

## Cross-input signature aggregation

Speaker 0: 00:19:48

So another thing that you seem to have been investigating is cross-input signature aggregation.

Speaker 2: 00:19:55

So my background is math.
And so I kind of found computer science and the tech world through math.
So I've always had a deep intrigue and love of cryptography and wanting to kind of get better at it and know more about it.
I'm also very interested in privacy and efficiency and these types of things.
So I heard about cross-input signature aggregation like a year and a half ago and it was the first time I heard about it, I was like, this is super cool.
Like, I want to learn more about this.
Then I got busy doing other stuff and it was kind of still in the back of my mind.
And so coming into this year, as I'm wrapping up the data project and thinking about, okay, what do I want to work on next?
I think that's kind of what I want to spend some time on.
Both in educating myself, like how does it work?
Learning more about the cryptography and also helping the people who have been working on it as like doing research, playing with implementations, proving use cases, because I think it's a really exciting for Bitcoin.

## Catching up on history

Speaker 0: 00:20:39

So catch us up a little bit on the history, because originally this was all going to be part of the Taproot software.
It was split out, but who's been working on it?
How long has it been talked about?
Is it today?

Speaker 2: 00:20:48

It's not a new idea for sure.
It was kind of like this long, long ago in Bitcoin, we knew there would be a world in the future where we had Schnorr signatures.
And once we had Schnorr signatures, all these other things become possible.
And I think cross input signature aggregation was one of those things.
But then as Snore Signatures became a reality for Bitcoin through Taproot, then it was like, okay, well, let's just do all the Snore Signatory things at once.
And then some other people were like, that's a bad idea.
Like we should break this out.
And I think there was some discussions about this is big enough on its own.
We don't want to slow down Taproot.
And we want to have more time to make sure it doesn't break other things in Bitcoin, that we fully understand the design space of it.
So let's separate it out and let's just do Taproot because Taproot is a necessary building block for it.
I think that was a really good decision.
So now the people that I'm aware of that have been working on it, there's Jonas Nick, I think Tim Ruffing, those are both people that I've heard talk about it.
The usual Blockstream suspects.
Those are the ones that I'm most aware of, but I'm sure there's others, you know, just because I'm not aware of it doesn't mean that they're not doing important work.
I think One of the things that also made me decide to spend some effort and time on this was there was a draft BIP that was proposed recently for a scheme for half-aggregation of Schnorr signatures like taproot.
I think they even referenced the BIP number.
But there's kind of something concrete to work with.

## Writing the BIP with Hackspec

Speaker 2: 00:22:00

And there were some decisions made in that BIP, and I'm going to butcher the names or get them wrong, but they spent some time to write the specification in something called HackSpec, which is this Rust-like language that you can define a cryptographic scheme in this, and then you can run these proof validators on it to get proofs of validity, proofs of security, and things like that.
It might be the first one that's doing this in Bitcoin Core, but you get all this power right out of the box.
I'm like, okay, we're writing it in this, so then we get these guarantees of security, and we can write test vectors and other things.
So it's a cool area to work, and a lot of tooling is already there.
When I see people putting effort into something, it feels like, okay, there's some momentum here.
I don't want to come and spend a bunch of time on something because I think it's cool and there's no momentum behind it.
And then six months later, it's like, well, yeah, I learned a lot about this thing that's never going to happen.
So I kind of, when I'm deciding what to work on, I look for momentum and I feel there's some momentum there.

Speaker 0: 00:22:47

So a couple questions.

## Thoughts on shipping cross-input signature aggregation separately

Speaker 0: 00:22:48

One is, Murch, you were shaking your head when Josie said why.
It was a good decision to split it out.
Why?

Speaker 1: 00:22:54

I was shaking my head because there's a few different arguments in both directions.
So on the one hand, when Taproot was pretty much done, what we ship now as Taproot, cross-input signature aggregation very much was still in the design phase.
So it was just at a very different level of preparedness and that's why it got taken out and delayed.
Also Taproot was starting to size up to a pretty substantial soft fork already and in itself is introducing a bunch of extension possibilities, a new output format, a new signature type.
Adding to that, instead of treating inputs as separate things on transactions to have a single signature per all the Schnur capable signatures on a transaction and then like having mixed output types on the transaction and some of their signatures can be aggregated.
It was a very orthogonal thing to most of the other things that were shipped with Taproot.
The very interesting thing if we had been able to ship cross-input signature aggregation with Taproot, would have been that it would have given a financial incentive for people to do multi-party transactions, where multiple users get together to provide multiple inputs to the transaction and create outputs together.
And it would have broken the same ownership heuristic that we've talked about this a little bit already where most blockchain analytics approaches assume that any inputs spent on a transaction are owned by the same entity and now once you aggregate signatures it becomes cheaper to build transactions with other parties than by yourself.
So I strongly believe that pay-to-tab route will be the dominant output type in five to seven years.
And if we had shipped it with cross-input signature aggregation, we would have shipped a privacy improvement that is financially attractive.
You would not need to say, oh, I'm doing this for privacy.
No, I'm doing this because it's cheaper.

Speaker 2: 00:24:40

It's a really important point.
Privacy and some of these other things like cost and usability are usually very much on opposite ends for each other.
You have to choose one or the other and you have to make a compromise.
Once in a while, something comes along that's like, why not both?
And really, I think the only way you'll have a reasonable degree of privacy is if there's an economic incentive to do it.
Because most people don't care until the privacy is broken, until the privacy has been exploited, and at that point it's too late.
So if you want people to have privacy, even if they don't care about it now, they don't understand why it's important, then you make it economically attractive for them to do so.
To me that's a very rare moment and it's exciting.

Speaker 1: 00:25:15

You have to make it the default choice and people are gonna opt out if it's more expensive still sometimes.
So it has to be the default choice and cheaper.
That would have been the exciting thing that we could have shipped here.
But it was, as I said, years away from being shipped and I think Taproot shipped at a good time so maybe if we do get another output type in the future maybe based on pay-to-contract and similar to the Taproot outputs right now we will ship it with that.

Speaker 0: 00:25:43

Yeah I guess, you know, just as a counterpoint, it does seem like soft forks are becoming increasingly difficult to get community consensus on.
And so every time you ship a soft fork, it might be a little bit harder or it might be, you know, not seemingly soft forks haven't been parallelized much.
So it might not be in line, for example.

Speaker 2: 00:26:02

I think it's a good point and also a separate discussion, but I don't think that should reason like all the points about cross input signature aggregation being a very big design space that kind of needs its own special attention.
We shouldn't decide how seriously we're going to research and test and vet something based on whether or not it will be easier to soft fork or not.
That's my opinion.
I think you should give something its proper due diligence and then talk about activating it.

Speaker 0: 00:26:25

I'm just playing devil's advocate here.
Now that Bitcoin is mainstream, putting in more privacy features seems like you're pushing water uphill a bit like you're sort of picking a fight with the powers that be as opposed to if you got this in five years ago.

Speaker 1: 00:26:37

Yeah I think that as more regulated entity entered the space and have opinions on the space I think it might get more scrutiny to have a privacy improvement.

Speaker 0: 00:26:46

And given that the largest tool is now in the United States, it just becomes more complicated.

Speaker 1: 00:26:51

So one of the big problems with shipping cross-input signature aggregation at a later date is that it cannot be combined with pay-to-type routes.
It is spec incompatible to change how the signatures work on pay-to-type route because it's spec'd how.
So an old node will not accept a cross-input signature aggregation transaction.
So that would be a hard fork to add it to the existing pay-to-type route outputs.
So we'll have to get people yet again to update their default output types.
And as we've seen with SegWit, native SegWit adoption is five years in.
Now we have 70% of the transactions or 80% of the transactions use SegWit and something like 45% of the inputs are native SegWit.
But it'll be another five to seven years or so until that is the case for pay-to-tap route.
And once we push out another output type, it'll take forever again.

Speaker 0: 00:27:37

And so what are the problems with it that are currently being reasoned through?

Speaker 2: 00:27:40

Ask me in six months.

Speaker 0: 00:27:41

Okay.

Speaker 2: 00:27:41

But that's kind of the point of like why I want to spend some time on it.
Like when you say like, oh, I'm going to spend time researching something.
A very viable and likely outcome when you take on something in a research capacity is, okay, I learned that this is not a good idea and that's valuable input and that's valuable to tell other people, okay, I spent some time looking into this and here's everything that I learned and yada yada.
And now I've updated my opinion on it.
I'm not excited about it anymore.
And I think sometimes people forget that.
Sometimes you need people to research something and take an idea as far as you can take it to convince yourself it's a bad idea or to convince yourself it's a good idea.
Ideally, when you go into it, you're kind of a blank slate and be like, this seems really cool to me, It seems promising, but let's see if there are show stopping problems or if it's feasible or not, or if the risks outweigh the benefits.

Speaker 0: 00:28:22

You're a social guy.
You seem to like people.
Tell us how you're working with your buddies and dragging more people into Bitcoin development.

Speaker 2: 00:28:30

Getting more people involved in Bitcoin development is super important.
It's something that I care a lot about.

## Onboarding to Bitcoin development

Speaker 2: 00:28:35

I want to see developers in the pipeline.
I think it takes a while to fully understand Bitcoin and be making meaningful contributions.
And if that's true, you need a pipeline of people learning and growing in their knowledge.

Speaker 0: 00:28:45

How long do you think it takes?

Speaker 2: 00:28:47

For me, I think it's three years.
That's the number I set for myself.
I said, okay, I want to get into Bitcoin development.
And the first year, I'm not going to do anything useful.
I'm going to learn a lot.
The second year, maybe I'm starting to like do some more impactful and useful things.
And then the third year is like really like, okay, I'm making valuable contributions to core.

Speaker 0: 00:29:04

2023 is gonna be a big year.
It's gonna be a big year.
Big things coming.

Speaker 2: 00:29:07

Stamp it.
But I don't think that's unique to Bitcoin, right?
I think that happens in the software development industry too.
Like you come in and you start learning a new tech stack or a new technology and you're not really doing anything useful.
And of course there's outliers, but initially you're not really doing anything useful.
You're doing kind of the grunt work that other people don't want to do.
You're learning a lot.
Second year, you're kind of like owning a project.
Something's kind of your own thing, or you're working with other people.
And then the third, or If we didn't want to talk years, now you're like staff or principal.
Now you're like really doing big things.
You're an important person or a respected voice in the space.
And I think that's true for Bitcoin.
So then let's keep the pipeline primed.
Let's keep people learning and growing.
And that's how I found Bitcoin doing the Chaincode seminar.
And I thought it was fantastic.
So something I've tried to do is get as much leverage out of that as I can.
So I took the seminar curriculum and I got some friends together.

## Running the seminar with friends

Speaker 2: 00:29:52

And really it was like I had a bunch of friends asking me about like, oh, like you just did a career change, you're working on Bitcoin and they all had their own independent questions.
So like this person would ask me a question, then another friend would ask me the exact same question.
And I was like, look, why don't we all just get together?
We'll meet once a week.
And here's this nice curriculum of material that we can read in the meantime.
And I pretty much just forked and copied the chain code seminar form.
And we went much slower.
It was much more like we all kind of knew each other.
So it was more fun and enjoyable.
If people got busy, we were like, oh, let's just meet next week.
Or, hey, I didn't really understand this week.
Let's read it again.
Or is there any additional resources?
So it was kind of a fun, slowed down version that I feel like we got a lot more out of.
And it was enjoyable.
Everybody learned a lot and everybody said they enjoyed it.
And then a few of them actually went on to join the official Chaincode seminar cohorts.
So that's something I would encourage a lot of people to do.
Like if you work in Bitcoin or you know a lot about it and you have people talking to you and asking you questions or people who are also software engineers and they're interested and they don't know where to start, just use the material.
It's all for free.
And the benefit to Chaincode then, you can provide recommendations as you go through and be like,

Speaker 0: 00:30:54

you don't need to benefit Chaincode.
I think the idea of putting effort into that is that people do their own thing.
I'd love it if the community updated that content on its own.
So in a parallel, Bitcoin transcripts is also something that we're involved with.
And some guy showed up, cares a lot about it.
He's now like the maintainer of Bitcoin transcripts.
So that's great if someone else takes it over.
And I think something similar here would be awesome.

Speaker 2: 00:31:16

I agree.
I think the broader point is when you use open source materials, always look for a way to give back.

## Giving back to open source

Speaker 2: 00:31:22

Like that's just how we keep open source alive in a healthy community.
If everyone becomes takers, people get burnout, people leave.
So if you're going to use a free resource, try to find a way to give back to that and improve it for the next person who's gonna use it.
So as we went through the material, we would notice where like a link was dead or maybe that wording could be changed.
Oh, I found this other great resource.
And I was constantly telling them like, hey, just open up a pull request, add it to the repo, tell someone about it.
We did a lot too where we got a lot more hands on.
We forked Bitcoin Core, we kind of basically just created our own little private network and we were mining with CPUs and going through simulated software upgrades and that was cool for me to see the excitement when you get really hands on with it and you kind of learn by doing.
So out of that I kind of had some ideas of, what are some ways we could make that more of a teaching tool?
A very hands-on experience.
So the main point is, use these free resources.
But as you use them, be mindful of, how can I give back and make this more useful?
But yeah, I thought it was a great experience.
It was also a way to kind of, if you get annoyed with your friends all asking you the same question from five different places, just get them all together on a video call once a week and make them read all that stuff.
Do your homework.

Speaker 0: 00:32:22

Well, thank you for coming in and sharing what you're up to.

Speaker 2: 00:32:26

Thank you for having me.

Speaker 0: 00:32:33

You two have been doing quite a bit of collaboration together it sounds like.
But it was good for me to find out what's going on.

Speaker 1: 00:32:39

Cool, glad to hear it.

Speaker 0: 00:32:40

I like the cross-input signature aggregation conversation.
It's something that continues to be in the back of my mind is given sort of after it was split out from taproot.
It seems like it's just such a win.
Gotta get it in.

Speaker 1: 00:32:52

Yeah, it'll still take quite some work.
I think it'll be interesting to see how we can even put it in because we'll need a new output type and that new output type should be financially incentivized.
And so we want people in the long term to converge on one output type, right, for privacy.

Speaker 0: 00:33:08

Do you think that there's enough use cases for taproot without this?

Speaker 1: 00:33:12

Oh, yeah.
Yeah.
I think it's very obvious that taproot will be used a lot for multi-sig stuff.
I think that there's very powerful things you can do with single-sig that you can't do without other output types, just via the script path fallbacks and the tweaks.
I mean, you can tweak ECGSA signatures too, but it's more baked in the pay-to-taproot output.
And between those things, I see that pay-to-type route will be just standard and default output for this one.

Speaker 0: 00:33:38

Yeah.
I just feel like cross input signature aggregation would have been just such an immediate win.
I feel like the community would have picked up on it really fast.

Speaker 1: 00:33:46

Yeah.
So if you have any cool data stuff to do, you should totally reach out to Josie.

Speaker 0: 00:33:51

The thing I like about him, and he's only been doing this for a couple of years, the guy's a giver.
He doesn't just take, he's really mindful about people who have been generous to him and giving back to the community and we didn't talk about his climb to funding or anything like that but he's just very cognizant of how he can be helpful immediately and how he can pitch in so it's great.

Speaker 1: 00:34:10

Well it was a fun conversation.

Speaker 0: 00:34:12

Cool so I hope you enjoyed this one as much as we did and we're gonna keep trying to put these out so hopefully we'll be speaking with You
