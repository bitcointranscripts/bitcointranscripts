---
title: SNICKER
transcript_by: kouloumos via tstbtc v1.0.0 --needs-review
media: https://www.youtube.com/watch?v=S0C-50QTteA
tags:
  - research
  - coinjoin
speakers:
  - Adam Gibson
date: 2020-01-13
summary: |-
  In today's episode Adam Gibson discusses various aspects of the SNICKER protocol. He introduces the concept of non-interactive coinjoin and how SNICKER aims to address the privacy and coordination issues of current coinjoin systems. He explains the process of constructing a transaction in the SNICKER protocol, including the use of shared secrets, diffie-hellman key exchange, and the role of participants in signing and validating the transaction. He also explores the potential improvements and future developments of SNICKER, such as competitive proposals and encryption methods. Overall, this section provides a comprehensive overview of the SNICKER protocol and its potential applications in improving the privacy and efficiency of Bitcoin transactions.
  Later on the discussions revolve around the efficiency and privacy of retrieving proposals from a receiver, the potential usefulness of SNICKER outside of mobile devices, the implementation of SNICKER as a proof-of-concept, analyzing different blockchain transactions, and expressing gratitude for the insightful presentation and interest in future sessions. There is also a focus on investigating different protocols like CashShuffle and CoinShuffle, as well as the possibility of implementing CoinJoin. The participants express their interest in exploring these topics further in future discussions.
aliases:
  - /wasabi/research-club/snicker/
---
Speaker 0: 00:00:01

All right guys, welcome to week two.
This week we're talking about Snigger, simple non-interactive coin drawing with keys for encryption reused.
I'm going to allow myself 15 minutes to go through the paper like we did last week and then we'll open it to discussion.
We're very lucky that Adam Gibson, the author of this BIP proposal is here so he's going to answer questions and correct anything that I've said that might be wrong.
Okay, so this is where you can find more about this.
We're taking it from GitHub, so the link is here.
The PowerPoint will be uploaded somewhere.
I'll make sure that happens.

## Last week - Knapsack Coinjoin

Speaker 0: 00:00:40

Okay, last week, just a quick reminder, we did an AppSack CoinJoin, and our summary was that we can mix with arbitrary values if we do a tactical partition of outputs, breaking them down further to make more possible interpretations of a coin joint transaction.

## Wasabi Research Club

Speaker 0: 00:01:00

So last week was Knapsack, this week is Snicker, next week we will discuss at the end of this video.
And you can always find out what we're doing at the Wasabi Research Club link.

## Problem with current CoinJoins

Speaker 0: 00:01:11

Okay, so what's the problem that's being addressed with current coinjoins?
The entire concept around Snicker, if I understand it correctly, is that we're trying to deal with the fact that the Coinjoins are interactive.
If you're familiar with how Wasabi or JoinMarket or any Coinjoin system works, you have all these participants that need to coordinate together.
Typically, this coordination requires a coordinator.
And even if the coordinator takes special precautions to use you know blind signatures and TOR and all these things there's still some amount of privacy that's being leaked because of the coordinator.
It's also very difficult to coordinate as you know with Wasabi if you have a hundred participants there can be all sorts of issues with coordination.
And the coordination is fragile to attack because now there's a central point of failure.
So if someone really wanted to hurt a particular mixing protocol, they could just attack the server that's doing the coordination with a denial of service attack, for example.
So this is the question we're going to ask today, which is, could a coin join be done without coordination?
So on the right, we see a typical coin join that something like Wasabi would do.
You have these inputs, you have these outputs, and you have these mixed green outputs that could belong to any of the participants.
And when you think about what it is, it's fundamentally consists of three things that need to be allocated from every participant, which is an input, an output, and a signature.
So those three things we're going to address in this paper.

## Inputs

Speaker 0: 00:02:33

So part one, inputs.
So I'm directly now reading from the Snicker version zero and version one.
So how can we figure out an input for a coin join?
Well a proposer in this scheme, because we'll have two people, a proposer and a receiver.
They obviously know their own input because they're the ones that's interested in mixing but they don't know the input of a potential CoinJoin buddy.
Because we're not using coordination, there's no people that are waiting in line to do this.
So one way we can deal with this is that the proposer simply guesses which UTXO on the blockchain might most likely be interested.
So maybe there's 10,000 UTXOs that fit the right specifications, and now this proposer that's trying to do an uncoordinated coin join is going to guess which of those might be interested in doing a coin join.
So maybe the UTXO that they look for are ones that are part of a joint market transaction or that are just at random or maybe a coin join that comes from a previous sneaker transaction.
You know, later on a sneaker gets more adopted.
So here on our left we have our orange UTXO.
We are the proposer in this case and we're looking out in the world and we see all of these possible UTXOs that could be our inputs.
And really what we're doing is we're just essentially just randomly selecting one that meets the criteria which is that it's smaller than our UTXO, in this case 21, so 20 works.
We're just constructing the coin join ourselves.
So if we're orange, then black is some other person.
This is what it's going to look like here.
So obviously we're going to match the value with the value of the UTXO we're selecting and then we're going to have some change for ourselves.
So So far, that's what it looks like.
And we could continue doing this over and over again for any number of UTXOs. We simply select a UTXO from a pool, put it on the input side, create the transaction, fill everything in.
So that covers inputs.
So with inputs, we're just gonna guess.
With outputs, well, a proposer knows their own address and they know their own unused addresses, right?
So every time we create transactions we use fresh addresses.
But how will a proposer figure out a fresh address that belongs to another party that isn't participating in the same transaction?
This is actually I think the most interesting and clever part of Snicker.
So we're going to try to answer this question.
So there's the question of, you know, when I take this 19 Bitcoin UTXO input that I found on the blockchain and I construct this transaction myself, what am I going to fill in for the address of the person that I'm trying

Speaker 1: 00:05:09

to coin join with?

Speaker 0: 00:05:11

I can't communicate with that person directly, there's no back and forth, this isn't coordinated.
So there's an obvious solution, which is just copy the same address used by that UTXO.
So if that UTXO is using an address with a public key, you know, X, just reuse the same public key.
Well, obviously that's not very smart because that exactly points out to the public that the unwinding of the coin joint.
So that's a very simple working solution, but it's obviously it doesn't do anything privacy wise.
So there's a smart solution is that we can use an address that is tweaked from the public key of the UTXO by a common shared secret between parties.
All right, so what we're gonna do is we're gonna take the public key that we know our mystery user has, which is on the left here, the input of 19.
We're gonna take that public key and we're going to tweak it with a common shared secret.
And here I think we have to take, oh wait, just, yeah.
So all we know about the mystery UTXO is that it possesses a private key to the public key that holds the funds.
But it's important to understand in this model that the public key isn't explicitly written in a UTXO.
When you send money to someone, you only make a commitment to the hash of their public key.
So what that means is that we can only know a public key to an address if that address has spent funds from it in the past.
So this is where the idea of address reuse comes in.
So really we're looking for an address that has a coin, that has a UTXO, and an address that's previously spent another UTXO from it, and thus reveal its public key.
So, But how will we tweak the public key of the receiver with a shared secret?
So this is the really the coolest part and I think it's the only time we need to take a brief aside in terms of math.

## Elliptic Curve Primitives, Diffie Hellman

Speaker 0: 00:07:12

So we're going to just quickly cover some stuff that you can not worry about if you don't care.
But the way that elliptic curve math works is that on our first line here, we have some private key P, and it's associated with a public key P when run through the elliptic curve with generated point G.
And a different person's public key, private key might be K, and it has a public key of capital K.
And as it turns out, you can do addition of private keys because private keys are just numbers, a number of times you run through the elliptic curve.
And so this allows us to do something really cool which is called the Diffie-Hellman Key Exchange where we can essentially, if two people each have a public key, then they can apply their private key against the other person's public key to create a common shared secret.
So that's pretty much the only thing you need to know and some people will know this because it's very basic cryptography.
Other people will probably not be able to appreciate it.
So what we're gonna do is we're going to take the receiver's public key and then create a shared secret, Divi Hellman shared secret between our public key as a proposer and their public key.
And what we end up getting is a point on the elliptic curve, and I believe that that is then later hashed in the specification, but the point is that there's a shared secret.
And so now the output that I'm sending the funds to isn't the same address but rather the same address tweaked such a way that anyone in the outside world has no idea that that tweaked address corresponds to the the input address.
Only the two participants know this shared secret between each other.
Okay, so so far we have selected a bunch of candidate UTXOs for the inputs and specifically with reused addresses.
Then we've created a recipient address with a Divi Helmand tweak value C.
The last part is what about signatures, right?

## Signatures

Speaker 0: 00:09:26

Because we know that when we have a coin join, we need all the participants to sign and validate that everything makes sense.
So in this case what we're going to do is the proposer is going to sign their own input, creating a PSBT, a partially signed Bitcoin transaction, and they need to make that partially signed Bitcoin transaction available to the receiver.
And the way that you can do this, it's very open to different ideas, but essentially it can be a public message board, it could be some public server, it could be directly peer to peer where The proposer is just sending out these PSBT's to many many people.
And so the idea here is that We have this input of 21 on the left and we're taking all these valid UTXOs that might possibly work and we're creating all of these partially signed Bitcoin transactions where we are signing only our own input.
And then we're essentially propagating these partially signed Bitcoin transactions all around.
So we're broadcasting them maybe to a message board, maybe to our peers, however it's done and hoping that someone picks it up and signs off on the transaction and then themselves broadcasts it to the network, to the Bitcoin network.
Right?
So a receiver can verify the contents of the PSBT and validate that the Diffie-Hellman tweaked public key matches what they have, the receiver can then choose to sign or not sign.
There's an important point to note that it would be not safe to just broadcast these PSBTs without encrypting them because a malicious listener could essentially track down these PSBT's and record them and then if any of these PSBT's got signed they could essentially unwind the coin join that's happening.
So a simple solution is just encrypt the PSBT against the public key of the other party that you're dealing with.
So now all you have is these blobs of encrypted data and essentially a single public key that can decrypt it.
And very little is revealed about what's going on there.
So in version zero, the summary is a proposer selects potential UTXOs from reused addresses.
Proposer then constructs outputs by tweaking the receiver's public key with a Diffie-Hellman key exchange.
Then the proposer broadcasts an encrypted PSP key to a public forum or to peers directly and then receiver can decrypt and sign and broadcast.
So some really cool things to observe here, the two takeaways of what makes this protocol cool is firstly, well I would say secondly, but firstly that Snicker is a deterministic protocol.
Everything is on-chain and if a user is restoring their wallet and their wallet is Snicker compatible then their wallet should have no problem in figuring out the tweaked public keys created from Snicker transactions.
So there's no need to store persistent data.
This is different than a Lightning protocol where data needs to be stored.
And if you don't have that data stored somewhere, your 24 words is not gonna be able to find that data for you.
And the most important thing, the whole point of the snicker protocol is that it's non-interactive.
So some people don't understand what the word non-interactive means.
In this case, what we're saying is that the receiver only participates the very, very last stage, having had no prior interactions with the proposer.
So it's minimally interactive.
The minimum interaction you can have is signing a transaction, and that's what we're talking about here.
If you compare with the Wasabi protocol right now, you have many, many interactions where you have people registering their inputs, then you have people registering, you know, blinded outputs and then registering their change and then back and forth and back and forth.
In this case, we only have one interaction at the very, very end.
The proposer is doing a lot of work, for sure, by propagating a lot of transactions and by doing a lot of figuring out in terms of guessing addresses and public keys and potential UTXOs, but the receiver is doing very little here.

## SNICKER V. 1

Speaker 0: 00:14:01

So Snicker version 1 has a simple addition, which is how can we implement Snicker without requiring address reuse?
That is, without requiring the receiver to reveal their public key.
And this is also quite clever, which is that, well, what if the proposer could just guess the co-ownership of a used address as a UTXO sitting in unused addresses?
So, a simple way of saying that is, if you look over here on the right, on the right, we have an output of value 10.
And that is a UTXO that we think is snicker compatible with us.
So we're a proposer, we look at output 10, we see that has a lot of potential but we don't know the public key to that output.
But what we observe is that the transaction where it comes from has one input and two outputs and it looks like output of value 10 is the change.
So what we can say is that input of 19 is also change, is also belong to the same owner.
Thus, that public key probably is in that public private key pair is is the same person who has the public private key pair of the output of 10 which is still unspent.
So essentially what we're doing is we're trying to not only randomly guess a valid UTXO that works with us, but also some ancestor that's revealed its public key that we can then use to create the transaction.
So this is what it looks like.
On the right, you have your input of 21.
I select the output of value 10, I create my CoinJoin transaction and the black output 10 on the very far right uses the public key from input 9, 19 way on the left.
So I'm not using the same address but a past address because that past address has revealed its public key.

## SNICKER Summary

Speaker 0: 00:15:58

So Snicker in summary is non-interactive coin joins are possible between two participants by leveraging either reused addresses or you know guessing co-ownership and a public board for posting PSBTs or some form of communication and I think that is it that's everything so yeah Adam can jump in with Adam Gibson can jump in with any thoughts.

Speaker 2: 00:16:25

Thank you, Aviva.
I want to just quickly outline the schedule for today.
So first of all, Adam Gibson, whenever you want to leave, just say so and leave, don't feel pressured to stay here.
Second, I want to, very first thing, I want you guys to say questions that only the author can answer so we can get over that and then we can do questions and then we can do discussions on topics and then we can do new ideas this snicker gave us and finally discuss what the next week's paper should be.
So One question, does anyone else have a presentation?
All right, seems like no one.
So first, Abib's presentation.
Adam, what was your impression?
What do you think?
Do you want to correct something?

Speaker 3: 00:17:40

No, I want to say it's very clear, really high quality.
So congratulations on an excellent piece of work there.
The I was I was looking for mistakes.
I think there might have been one equation in the only math slide that was wrong.
But it's such a trivial point that I won't even mention everything else is.
I mean, seriously, you explained it very clearly.
I guess you didn't explain every detail, but I think you explained most of what's in the BIP.
Yeah, no, it was very good.
So I think it's more a case of if people here have things coming out of that that they still don't understand and myself and Aviv or anyone else can try and explain it.

Speaker 2: 00:18:26

Anyone has anything to add to the presentation?
Adam, don't forget to mute yourself sometimes.
Sorry, yeah,

Speaker 3: 00:18:42

I was just having a stretch.

Speaker 2: 00:18:44

Okay, how about questions to the author that only the author can answer.

Speaker 1: 00:18:52

I mean in general I think when I first got to know Snickers I thought it was just for interest re-use, but especially we're reading a bit now, This is especially powerful for example with change analysis.
So if we have a coin that is being spent, then the public key is revealed.
And in most transactions, the change coin will be from the same owner than the input.
So just by having a regular spending transaction, Adam, how likely do you think is it that we can find a successful proposal for a Snickers, you know, if we do change heuristics and other stuff?

Speaker 3: 00:19:30

Yes, so a couple of points on that.
The first point is, there's a kind of ironic beauty in this scenario, which is that specifically in the case where there is bad UTXO privacy management, That is the case where this is possible, right?
Because if you know which is the change, then you know which one is right.
You can do a coin join, snicker coin join coming out of it.
That's a kind of a quip and a joke.
But the more serious point is it doesn't really matter.
I mean, think of it this way.
A typical transaction has a spending output and a change output.
And that's kind of also somewhat true with coin joins, where you just have multiple people together and you still have like one out and one chain, one coin join out, one change out.
And if you don't know, let's say in a typical spending transaction, which one's the spend and which one's the change, then you can just make a proposal for both.
It's not a big deal.
I mean, this will naturally lead on to the more important practical question of how do we handle lots of proposals.
But I don't think at first it seems like an important question.
But if you think about it, it kind of isn't right.
This is very opportunistic.
Yeah, that's what I think.

Speaker 2: 00:20:44

So two of you know if Coinjoins, if they are if they are not recognized that they are snicker coin joins, then they look like normal transactions.

Speaker 3: 00:20:59

Sorry, yeah, That's kind of a different point, isn't it?
Which is there's this question that Aviv correctly handled in the presentation, which is like, how do you identify candidates for this process?
If you're trying to kind of bootstrap or seed the process, then you might want to be taking, you might want to be proposing coin joins on UTXOs, which are not themselves coin join UTXOs. So they could be ordinary wallet spending transactions.
That's a bit tricky, but if you're going to try and do it, obviously you have the fundamental issue of which one is the change, because I need to know if I'm going to use Snicker version one, then I need to know which one is the change so that I can map it to the input of the transaction and get a public key.

Speaker 1: 00:21:48

So if

Speaker 3: 00:21:48

you're going to do that, then you just might have to try twice instead of once, because a typical spending transaction only has two outputs, right?
It doesn't have like a hundred.
If you're talking about a CoinJoin transaction and you're taking UTXOs from that, then it's a different story, right?
But generally speaking, that's going to be somewhat easier.
And then the kind of third case is if you want to build a Snicker transaction from a previous Snicker transaction.
And that again, like the CoinJoin case is easy because it's very easy to analyze that transaction in terms of which one is the change.
Right.

Speaker 2: 00:22:19

Any more questions for Daltor?

Speaker 3: 00:22:23

I have

Speaker 0: 00:22:24

a few, but if anyone else wants to interrupt me feel free.
One thing I would like to ask is how you see things going forward with this.
So you have proposers that are scanning the blockchain.
Ideally you would have wallets that are snicker compliant.
Wallets that are snicker compliant and so they would they would connect to this like message board or repository of snicker PSBT's.

Speaker 3: 00:23:03

Encrypted proposals yeah.

Speaker 0: 00:23:06

Okay Do you want to talk a bit about incentives?
Because I don't know if you said anything about that in the paper, but How do you see incentives playing out in terms of people profiting off of these transactions?

Speaker 3: 00:23:23

Yeah, I didn't talk about it much, but I did briefly mention it, I think, in the future improvement section.
I was just sort of waffling a little bit about, you know, under what circumstances might you be able to do this to actually do payments and anyway, but forget that.
Your question is obviously very relevant, incentives.
I think it's a slightly unclear point to me, but I'm hoping that it's one of those situations where the market figures it out for you.
So essentially, you've got a degree of freedom in the proposal that you make.
So in your nice presentation, you clearly showed what the transaction looks like.
You have two inputs, one from each party, and you have two equal sized outputs, and then one change output for the receiving party.
Now, even in that simplest model, that's the model that exists in the proposal, it obviously is possible to tweak like who is paying the Bitcoin transaction fee in that and maybe further, one party might actually receive additional funds depending on some details.
One party might be the proposer, and it might be the receiver.
And I can see arguments for both.
The most natural, my suspicion is that this would start off with a kind of proposers making proposals which receivers do receive money from.
But it could easily be imagined as going the other way only because proposers have more work to do than receivers.
And then thirdly, as I was just mentioning at the start there, we could imagine a slightly different model of Snicker where somebody wants to spend money in a coin join and actually forced a receiver to take a specific sized output that would require four outputs instead of three.
And that's not actually included in the BIP, it's just something I was thinking about as a future possible improvement.
And the reason I find that fascinating, because I could imagine this scenario where like, imagine you wanted to pay someone one BTC and you wanted to do it with slightly better privacy, but you were willing to sort of wait a little while.
But if you sweeten the pot significantly, you might find that putting out 100 proposals, you immediately get one of them snapped up.
And all the receivers are in a race to get that money.
So it could actually create a very bizarrely fast process, even though it's totally non-interactive.

Speaker 1: 00:25:59

You know, Adam, kind of jumping upon this point, what if we add one round of interaction?
So Alice proposes, let's make a transaction that then Bob downloads and decrypts and sees, but Bob actually wants to do an equal value or like a different equal value to pay one specific amount and then Bob creates the second proposal adjusted to his needs and Decrypts the two Alice's puppy and publishes back to the bulletin

Speaker 3: 00:26:29

That's interesting, you know, maybe I mean it it's almost it's almost the case that you can't stop him, right?
I don't actually think that there's...
It's almost not needed to change anything in the proposal for that to happen, right?

Speaker 1: 00:26:45

No, no, it would just be client-side, a second-speaker proposal, but to already two peers who have already established some form of communication beforehand.

Speaker 3: 00:26:54

I suppose what that suggestion, that's a very interesting suggestion, I suppose what it throws up is the point which isn't really clear, which is to what extent are these roles separated, the proposer and the receiver, and to what extent should they be separated.
Now I originally had in mind a quite asymmetric scenario because I felt and I think this is true really that the proposer because of needing a significant amount of blockchain scanning skills and access to the ability to scan blockchain to find candidates, The proposer's job is significantly more difficult than the receiver.
And I was specifically trying to advertise the idea that the receiver side of this protocol is something that could be implemented in mobile wallets pretty easily.
But I think if you try to make the two parties symmetrical in their abilities, And you say that any Snicker-enabled wallet is able to do both sides.
That would be cool, but I am afraid that it imposes slightly larger computation and etc.
Costs and, you know, development costs on, let's say, a mobile wallet that wanted to implement the proposal.
So I'm quite keen to defend the idea that people could be receiver only and it could be nice and simple.
But that doesn't, of course, set aside the possibility that the souped up professional grade wallet is able to do both sides and is able to do what you just said, which is that they could even because they're constantly listening for proposals, like they ping out a proposal and they get get get one back on the same UTXO.
That's that's really kind of clever.
I like that.
Thank you.

Speaker 2: 00:28:32

All right.
My question.
Snickers.
Interactive coin join with keys for encryption reused.
Explain it.

Speaker 3: 00:28:42

Yeah.
Well, the S.
Well, it's funny when I was in, what was it, Amsterdam, and I was explaining this to Roastbeef, and he said, that's a backronym, isn't it?
I said, you're absolutely right, it's a very backronym.
You know what backronym means?
No?
Backronym?
No. Okay, backronym is just like, you know, acronym is the word in English that refers to the case where you give the initials of something like PSBT is an acronym starting with A.
So there's this kind of joke word backronym, which is where You think up the name and then you choose the words to make it fit that acronym.
So so basically I was trying to find a memorable word for non.
The origin of this was in thinking about the idea of non interactive coin join generally.
That There have been various ideas proposed in the past, and none of them quite really worked for making CoinJoin non-interactive.
The S is just to make it work.
It's just the backronym, Snicker Simple.
But the keys for encryption reused, I think, does actually make sense, right?
Because you, I mean, maybe if it wasn't a backronym, it would have been keys reused for encryption.
But it does make sense, right?
Because you either take a reused address, so you have a key, a public key there that you're reusing for encryption, or you're taking a key from a previous transaction and reusing it for encryption.
By the way, this brings up a point that is sometimes discussed in this protocol, is to what extent is the encryption part necessary?
I personally think it is either completely necessary or it's very, very desirable.
But it's a kind of an interesting thought experiment to imagine how all this would work if the PSBTs or the anyway, the signatures on transactions were just broadcast onto the message board in the clear.
I think it's not really desirable.
So I think the encryption part, although it's sort of a little bit extra complexity.
It's kind of necessary.
Yeah.

Speaker 2: 00:30:52

All right, thank you.
Questions for the author or should we get on general questions?
Okay, general questions.

Speaker 4: 00:31:00

No, I have a question.
Sorry.
Because, well, before that, thanks Adam for joining us.
My question is, for example, we have this machine, the Wasabi coin join machine that knows the inputs, right?
And the change address for every single participant.
And if you were working with Wasabi, and you know that, and you have this thing, what would you do?
For example, could you create a proposal for every change output?
Or how can we take advantage of this that we already have here to implement Snicker easier or more effective.
I don't know.

Speaker 3: 00:32:11

Sure.
Sure.
I don't know.
I'm kind of hoping that you're going to explain this to me a bit more, because I remember that the reason I wrote the draft BIP was because you had a thread on your GitHub.
And I thought, oh, people are interested in the idea of doing this.
And I wanted to make sure that there was some kind of clearly defined protocol written somewhere so that if people like you want to discuss it, you at least have something concrete to discuss.
Now, how would the Wasabi scenario, how would it change this?
I don't actually know for sure.
In the naive sense, okay, when we have a Wasabi coin join, we have a large transaction with a lot of outputs.
We could try to propose, I don't know who we is in the sentence, but we could try to propose Snicker coin joins on the change outputs.
But to do that, we would need to use the version one of Snicker.
In other words, because there's no address reuse, we would need a public key to work with.
So I don't know whether you're going to make proposals on input keys from deposit.
Does that make sense?
You don't have the x pubs, do you?

Speaker 0: 00:33:30

This is great.
Because inputs are usually quite linkable to change.
It's not always 100% clear, but in most cases, you can quickly find...

Speaker 3: 00:33:42

Yeah, yeah.
Yeah, yeah, that's true.
But that's not actually addressing the point, is it, if you think about it?
Because what you remember in version 1 the point is you have to find the what am I trying to say you've got the yeah yeah yeah yeah you're right yeah that's that's all you need yeah yeah yeah it Because it's a big coin join and you can generally link inputs to outputs, that addresses the problem.
Yeah, you're right.

Speaker 1: 00:34:08

Another cool thing with the Wasabi architecture is that the participants of the coin join, they receive both the coin join transaction as well as the blog very swiftly so they could the those peers that actually communicate in the zero link coin join itself could then do a snicker coin join very very quickly afterwards to get the property also for their for their changeout that maybe even was in the same block

Speaker 3: 00:34:35

yeah but I mean

Speaker 1: 00:34:36

but well

Speaker 3: 00:34:37

first of all yes I agree with everything everyone said I was never really clear though Why you find this?
This interesting specifically now Wasabi sense.
I think it's just generally interesting for everyone, somewhat.
But I thought the really obvious, like, best use case for this was like a mobile wallet that wanted some extra privacy feature, but didn't want to have to implement a massive, you know, a big coordinated over a network and to a server or not to a server, whatever.
No, they didn't want something too complicated, but they just wanted something that very passively over a long period would add more coin joins.
Isn't it the case with something like Wasabi that you have, the guy's there, right?
He's connected up to the server and he's done his mixing and he's got his on sets and what have you.
And if he's got change outputs that he's not happy with, he can just put it through another round of mixing, can't you?

Speaker 4: 00:35:33

Yes, yes, you are absolutely right.
We are trying to do research alternatives to provide new privacy features and the receiver is more or less clear to me how to do it and it's easy to do in a mobile wallet, yes, but the proposer has to do more job and we can do that.
I mean, I think we can provide, because I think, for example, the Electrum team was saying that, well, they maybe could implement the receiver part.
And I think many people can do that because it's probably easier.
So we can do the proposer, I think.
And that will be great because you need a proposal.
Someone has to get it.
So that's why.
And this doesn't have to generate revenue for us.
It's just We want to be the best wallet, just that.

Speaker 3: 00:36:47

Right, I see what you mean.
Yeah.
So when you say we can be the proposer, are you saying, would it be something like the client, like they've got a desktop wallet, desktop Wasabi wallet, are they going to be effectively making requests to Wasabi servers to scan?
Oh, no, they have their own Bitcoin core.
They might have their own bitcoin core right how would they get these scanning results to find proposals how would that work

Speaker 1: 00:37:17

Either it's Bitcoin Core running or you use the blocks that you already have downloaded because we have mobile.

Speaker 0: 00:37:24

He's asking where the proposals would come from and I'm guessing the answer is either from the coordinator or in Wasabi there would be like it would point to a public, you know, repository or where these proposals are being maintained.

Speaker 3: 00:37:46

I guess the client just needs a list of candidates.
The thing that's kind of somewhat intensive is to get candidate UTXOs, isn't it?
Because once you've got a candidate UTXO, You could act as proposal and construct a proposal pretty easily on it's not really more complicated than the receiver, is it?
Yeah, I think so.
And then you just you just encrypt it and you just put it wherever the bulletin was.
Wasabi could also maintain a bulletin board that would be nice and easy for you.
Because it's just going to be a bunch of binary blobs.

Speaker 0: 00:38:20

So hypothetically, Wasabi could be snicker compliant and then not deal with the proposals at all, but just tell everyone it's snicker compliant and then maybe have a place where people can post their proposals and people should just know you should only target UTXOs from recent Wasabi coin joins in particular the change outputs.
That would make it easier for proposers.

Speaker 3: 00:38:48

Yeah, you could restrict it like that.
That would certainly make things a bit easier to handle.
Yeah.

Speaker 2: 00:38:56

Can you talk about taproot?

Speaker 3: 00:39:00

Oh, yeah.
Yeah.
Thanks for reminding me.
I forgot about that.
It's just one small detail, but it's very simple and elegant, which is that if we, you know, obviously these things take time, don't they?
But if everyone switched to taproot, then there would be no discussion about version 0 and version 1.
There would just be a version 2 for taproot, which is because the taproot exposes the public key directly in the UTXO, then there would be no need to make an inference or to worry about reused addresses.
I actually forgot that and David Harding told me after I'd written the thing.
Yeah.

Speaker 1: 00:39:36

Here, Adam, quick question.
What if, I mean, the taproot pubkey is a tweaked pubkey, right?

Speaker 3: 00:39:41

Yeah, yeah, but it doesn't matter.

Speaker 1: 00:39:43

It's just a twice tweaked pubkey.

Speaker 3: 00:39:47

Yeah, I mean, it's kind of abstract, isn't it?
But if you think about it, like the taproot public key is, you know, notionally tweaked with the script, but if you're just creating just vanilla taproot segwit version one outputs, you're just, that's irrelevant, because you're just going to know the private key anyway.
So I mean, yeah, you're right in theory that if you, no, but actually you make a fair point because if I go in as a proposer and look on the blockchain and I find all the taproot outputs, I never know which ones are actually like tweaks with an actual script and which ones are just like a public key and there's no scripts behind it, no Merkle root, you know.
But you're right, so in some like abstract sense it's like a tweak of a tweak but that doesn't change anything.

Speaker 1: 00:40:34

Right you just take the two tweaking factors to the original private key and...

Speaker 3: 00:40:39

Yeah but you think about it doesn't it's not never really going to work like that in practice is it because if if it's an ordinary taproot output and it's not like some weird multisig in which case this is never going to work or I don't even want to think about it.
Then you're just going to be the person who owns it is just going to be signing on the full key, just like they do usually, you know, because usually even in multisig taproot, you're signing on the main key, the key pass spending, because you just override the contract, you know.
I'm waffling now, ignore me.
Anyway, there's no issue, there's no issue, it's fine.

Speaker 4: 00:41:13

Yes, that's great.
I didn't have that in mind.
You know, if we implement tabroot2, all the outputs of our coinjoin transactions could be candidates for sneakers, because it is clear it's people that wants to gain privacy.
So they are natural candidates.

Speaker 3: 00:41:42

Yeah, it's interesting that you look at it like this, that you think of it more in terms of like we could be proposers because I think the sales pitch I've tried to like get people to see this is that the sales pitch of this is the ability to have coin joins without doing anything at all.
That's how I tried to sell it to people.
I don't think let's not forget in all this discussion.
The huge weakness of the idea is it's just two party coin joins.
Right.
And so you've got to be looking at it in a certain way.
And I think it's in a way, it's almost the opposite of Wasabi.
I was on a podcast a few weeks back and I said, this is what I said.
It's like, think of it as like a spectrum.
Wasabi is really on one end and this is on the other end because Wasabi is very tightly coordinated, very tightly coupled.
Like everyone gets together and it's got advanced cryptography to make sure the privacy still works, but it is tightly coupled.
And it means that, you know, as long as people are willing to get together and do it, it works right.
Whereas this is exactly the opposite.
This is like the ultimate laziness of CoinJoin.
It's like, I really don't give a shit.
I'm just running a wallet and on my phone and I switch it on every day or two.
Because that's the thing, right?
This system could work even if you don't switch your wallet on very often because it could just when you switch it on, it could download the latest proposals for your key.
Oh, by the way, we didn't mention that indexing keys.
OK, I'll stop waffling, but there is a whole area which we haven't discussed, which is like this whole issue of how do you deal with a huge number of proposals?

Speaker 2: 00:43:16

I want to get into that.
And specifically the spam issue.

Speaker 3: 00:43:20

Yeah, let's talk about that.

Speaker 2: 00:43:21

And I will have a surprise idea for you that brings together toproot and spam issue.
So can you talk about...
Well yeah go ahead.

Speaker 3: 00:43:38

No no I want you to talk.
Please go ahead.
Yeah, sure.

Speaker 2: 00:43:43

So you had a couple of ideas how to prevent the spam issue.
And I'm most interested in the hashcash one.
That's why I should first discuss the non-hashcash ones.
So first, someone could pay some money to, I don't know, Bern or a central coordinator or something like that, but probably Bern in order to make a proposal.
So, how would you do that?
How would you?

Speaker 3: 00:44:17

Yeah, it would have to be a central like that.
So in that scenario, you've got, this is what was in my head.
You've got a bulletin board server.
I was planning to do this, but I've just never got around to it.
Just to set it up as a kind of a proof of concept, just set up a Tor hidden service.
And all it does is receives encrypted blobs as proposals.
And then anyone, let's say with a joint market wallet, some code in there that just pings that URL, that Tor hidden service URL, and just downloads anything that connected to a particular key.
So you'd index it by public key, just because it's a little bit easier.
So the proposal would attach in public, the public key for that proposal, which is not a privacy loss because that's on the blockchain anyway, and it's only a proposal.
It's not the receiver doing it.
So the receiver would just take all of it and just maybe for maximal privacy and then just read the proposals for his public key.
In that scenario, we know there will be a particular hidden service and they could just say, well, look, you can't make a proposal unless you...
So if it's a payment to a burn address, they could say, to make a thousand proposals, you have to...
Or you get 1000 proposals per, I don't know, one unit of Bitcoin sent to the burn address and you have to sign the key, it'd be a bit of a mess and more to the point, it would be a kind of extra centralization factor.
But it would be one way to prevent the obvious problem that if you send encrypted proposals, there could be a billion of them and nobody has any idea whether they're valid or not.

Speaker 0: 00:45:56

I'm confused why this is a problem because Firstly, the encrypted blobs have the corresponding public key, so most people don't have to look through blobs that don't relate to them.
But also, why isn't the hashcash solution of just forcing encrypted blobs to have a unique hash work.

Speaker 3: 00:46:20

Well, I think Nopara is going to come on to that.
Yeah.

Speaker 2: 00:46:24

So the rest of the ideas, except with the exception of the hashcash, is all about paying some money, the fidelity bonds, the paying with Lightning Network, those are all about paying money, right?

Speaker 3: 00:46:37

Well, the Lightning would be paying but let's be clear about fidelity bonds, right?
It's not quite the same because you don't actually pay the money.
You just lock it, right?
So You lock the money and you sign for it and it's provably locked for some period of time.
So you lose the time value of the money, but you don't actually lose the money.
So it's fiddly and that would be even probably even more complicated than just a payment, right?
Well, it would be more complicated.
It would be inconvenient for users, for proposers to have to lock up their money.
But, and also then you have to worry about the privacy implications.
This is one of the problems I have with all these proposals is when we're trying to create a very tight privacy system, we're not exposing like network information, trying to get better privacy for our coins.
But if we then have to make payment of our coins, we have to start worrying about the privacy of those payments.
And it's like almost infinite regress because now I'm going to have to coin join my my fidelity bonds and my and my payments, as well as the coin join that I'm actually coin joining and God, what a mess.
I don't really like any of those proposals, but I don't think they're necessarily wrong.
They could work.
I mean, after all, Lightning has some privacy.
So.

Speaker 2: 00:47:52

Awesome.
So let's go on to the last one or the first one, whichever point you go.
Hashcash.
The idea of hashcash is that you make some computation and you prove that you made that computation in order to make an action.
So it would not be like, well, an attacker would have to get a lot of resources or bots or something like that in order to attack this system and whenever they stop the attack, the system is back online.
So that's the idea of hashcash, which is as you you phrased it, you phorophrased it in beat message or in other systems, it's sort of kind of worked, right?

Speaker 1: 00:48:45

Do you want to

Speaker 2: 00:48:45

say anything to it or?

Speaker 3: 00:48:49

No, I just think it's an interesting idea but I'm just about whether it could be effective or I'm not sure.
I'm just not sure to be honest.

Speaker 0: 00:48:59

Sorry, I just realized it probably wouldn't be effective because the proposer has to issue so many of these proposals.
So if you toggle it so that every proposal costs, you know, five seconds of computation, then it's probably going to hurt people who are legitimate.

Speaker 3: 00:49:22

Yeah, it is.
But think of it this way, right?
In the original proposal of HashCash for junk mail, the scenario there is that the attacker wants to make...
Yeah, so in that case, the attacker probably wants to send tens of thousands of emails, and maybe has a 1% or 0.1% conversion rate.
So it's quite heavily skewed in favor of the honest participant, because an honest email user doesn't need to send thousands of emails, maybe just a few.
So that's why Hash Cash made sense.
Now here we've got a kind of gray area that I don't really know the truth of.
Like what is the ratio?
Like if you're an attacker, first of all, why are you even attacking the system?
There's no monetary incentive in attacking it.
So it must be like a kind of a somebody wants to kill the system.
Right.
So since we can't really measure their economic incentive, I mean, how how What's the scaling factor that we need to create to make it feasible for the honest user, but infeasible for the attacker?
And also part of that equation is how many proposals do you need to make as a proposer?
Do you need to make tens of thousands?
Do you need to make 100?
Do you need to make 10?
I have no idea.
It's really it's really all up in the air.

Speaker 1: 00:50:36

How about this?
So you know a proposer will most likely do several proposals especially when the coins that he proposes for are being spent right because And then what might be possible is that if these proposals are encrypted, that the proposer can prove that the encrypted block was from a now spent output.
And if he can provide the proof that this encrypted message is no longer needed, then he has the right to add a new encrypted block or maybe even two of them to post the next two things.
And as soon as these proposals become obsolete, he can upload the next one.

Speaker 3: 00:51:15

Yeah, I thought about this and also I remember maybe it was Matt Corralo or somebody who thought about this and suggesting like zero knowledge proofs of certain properties of the encrypted data.
I don't actually think it works at all.
The reason I say that is because fundamentally, You can't know if a proposal is valid unless you have full consensus access to Bitcoin.
Because if I'm an attacker and all I want to do is create a fake proposal, then it may be even as simple as just tweaking one tiny, like one byte in the UTXO input string, you know, like the 32 byte UTXO input.
And I don't think that there's a way that zero knowledge proofs can actually address that.
I mean, I'm completely putting aside the problem that you've got of SHA-2, proving properties of data under SHA-2 is already very complicated.
But even that wouldn't be enough.
You need, I don't know, I think it doesn't work.
That's what I'm saying.

Speaker 4: 00:52:21

I have an idea, because there can be more than just one bulletin board.
So we, for example, in Wasabi, in our coordinator, we could have one and search for candidates, yes, for example with that because it's simpler and post proposals to our own bulletin board where nobody else has access to write, to post proposals.
So in that case, we don't need any mechanism for spam protection or anything like that because we are the only ones that post proposals there.
Well, a mobile wallet can query our bulletin board, for example, and others too.
So I think in our case, we could do something like that.
It could be very simple.

Speaker 3: 00:53:25

Yeah, I think that's one of the first of, like I listed four or five ways you could try and handle this.
One way is you could just restrict access fundamentally just as a fixed set of people who could make proposals but obviously that's that's a less interesting proposal at scale because we want proposals from you know various parties we don't really want...

Speaker 4: 00:53:44

Well yes, oh sorry, but you know we can have for example our own bulletin board and other people can have another one.
And there can be just one that synchronize, that consolidate all the proposals in one big, main or central repository.
It could be, I don't know.
I mean, how to scale that is, I think probably, I don't know really.
Probably it's a different problem, probably it's not.
But it could work.

Speaker 3: 00:54:24

Yeah, I think it can definitely work.
It's just a question of how far we can go in making it as kind of as effective and broad as possible.

Speaker 2: 00:54:35

Okay, guys, here you go.
Pay to endpoint.

Speaker 3: 00:54:40

Yeah.

Speaker 2: 00:54:42

What's the largest problem of pay to endpoint or rather, what do I think is the largest problem of pay to end point is that it disrupts existing user workflow.
What can we do about it?
What do we want?
We want someone to give me an address and then I could even send money to that address or based on that address I could establish peer to peer encrypted communication between the someone who is giving me the address.
Right?
If we could solve this, that would be great.

Speaker 4: 00:55:29

One comment just about that.
You know Tor provides what is called something like ephemeral hidden services or something like that, that can be created on the fly, I mean without a Tor config file.
So you can open, for example, Wasabi and create and publish an endpoint as a heightened service without any configuration file or anything like that.
So you just need to to know the the onion address of your peer.

Speaker 2: 00:56:15

That's important but there is a more fundamental issue here and it turns out it's the exact same issue that Snicker has.
Is that how do you send an encrypted message to someone based on only the Bitcoin address right you can't do that you can't get the public key out of the Bitcoin address unless it's a top-root output so now you can create an encrypted message from the Bitcoin address that someone sent to you and that message would include your TOR endpoint and you could broadcast that to a peer-to-peer network and they would get in communication with you.
So the problem is solved.
What's the only problem left?
Is the spam attack.
And how could we, I wouldn't dare to say solve the spam attack, but definitely improve a lot on it with hashcash that's a straightforward application to that so what do you think about that

Speaker 3: 00:57:28

so you're basically saying bit message was the answer all along We basically need a peer-to-peer messaging network that's encrypted and has hashcash.
So we should have stuck with bit message.

Speaker 2: 00:57:42

But the problem was that you cannot, You don't want to ruin the user workflow, right?
It wouldn't ruin anything because someone would give you an address and if there is no answer to your encrypted message, then you just send the money.
So the user

Speaker 3: 00:58:02

might not

Speaker 2: 00:58:02

notice anything that, hey, a pay to end point transaction happened.
The user would have no idea about that.
It just give you an address and send you a transaction and you know.

Speaker 3: 00:58:15

But wait, are you saying that as far as you're concerned, this problem is solved by hashcash?
Is that what you're saying?

Speaker 2: 00:58:23

The encrypting message problem is solved by top root.
And this one issue, I wouldn't dare to say solve, but definitely improved with hashcash or at least a try.
It's worth a try, you know.

Speaker 3: 00:58:43

But I think the reason that hashcash made sense with bit message was because bit message was like email where all you were trying to do was prevent.
Yeah, no, it's almost the same, but it's not quite the same somehow.

Speaker 2: 00:58:58

All you are trying to do is prevent many messages, many fake messages to go out to the network.

Speaker 3: 00:59:08

Yeah, but...

Speaker 2: 00:59:10

Yeah, but not sure if it works that way, right?
Because there are millions of other ways that Atacar can figure out to get that much computation.
For that you would ask what's good in it for Atacar.
And not really because the transaction is still happening but without a payment point.

Speaker 3: 00:59:31

Yes, I think that's actually quite a strong argument.
And there is

Speaker 2: 00:59:35

a limited time frame that, well, if there is a, if you don't find, if Nova replies to your encrypted message within 10 seconds, maybe that's how long a user can tolerate or maybe that's that's too much already.
But if you don't find an encrypted, if you don't find a communication, then you just send a normal message.

Speaker 3: 01:00:04

I think for payments where people can't tolerate a 10 second wait, and then they should they should be using Lightning anyway.
It would be a smaller payment, generally a retail payment.

Speaker 2: 01:00:17

Anyway, I threw this idea out there.
We can move on to Snicker more specifically.

Speaker 3: 01:00:23

No, I think we've covered a lot of it.

Speaker 1: 01:00:28

One thing that I was so curious about how to best and privately retrieve proposals from a receiver.
And I thought because we, or maybe, there are already the public keys exposed, right, together with the encrypted data.
So I thought would roll on rice filters similar to block filters at 3.58, would that make sense here?

Speaker 3: 01:00:52

I'm, If you're asking me, I'm actually not, I haven't really studied that area yet, but intuitively from like a vague idea of what it's doing, it should be the same problem.
So I suspect a similar solution will apply.
Yes.
I mean, obviously, the naive thing to do is to download everything.
That way, it's like it's like running a Bitcoin core node where you just download everything.
And obviously, the equally naive in the other direction is just to only take the data for your public key, which would reveal something about you, even though, you know, tour, blah, blah, blah.
But it would reveal something.
So, yeah, the kind of probably the smart way is to have some kind of filter that would intelligently download data in such a way that people couldn't.
Because it would be a bit like Bitcoin blocks, right?
Because if you imagine you had a mobile phone wallet, you turn it on.
Let's say you turn it on every morning for whatever reason.
You probably don't.
Let's say you do.
Then you'd want to download the data since the previous time you logged on, which would be a chunk of encrypted proposals.
And like you say, we probably would want some kind of filter to be smart about it.
Yeah.

Speaker 2: 01:02:02

So I only have two more topics left.
One is just a statement that I think it's uncontroversial but I will ask.
So I think the most efficient way working on Snicker should be actually after Toproot gets on the Bitcoin network.
So before that it's kind of a hack, but after Toproot gets there it's a more cleaner solution.
Anyone has anything to add to that?
Okay, the next thing is, this is kind of silly too because I know the answer but I just want to ask it.
That you know, Schnorr signature aggregation which results in aggregating the signatures is a notoriously interactive process, while Snicker is a notoriously noninteractive process.
So

Speaker 3: 01:03:07

can

Speaker 2: 01:03:07

you elaborate on that?

Speaker 3: 01:03:12

Well, yeah, but the thing about Schnorr's signature aggregation is there's different, like, what's the word, different scenarios where you use it, right?
If we're talking about multi-sig, then we're talking about mu-sig, and that is a three round interactive protocol as currently set up.
But that wouldn't, I mean, that doesn't really apply to this because this is like coin join between different parties.
But if we were talking about signature aggregation cross inputs, then as far as I know, there isn't even a proposal for that yet, if I remember right.
So I'm not sure what I could say about it.
I suppose we could imagine a future where that was happening and where therefore there would be a problem in doing this kind of protocol because the signature, but the thing is, if the signature aggregation cross inputs requires interactivity, that statement only really applies when more than one input is, when the inputs are not all owned by the same party.
So it only applies to CoinJoin.
And so it might mean that you couldn't make a Snicker coin join that, like other coin joins, had the nice property of reducing the size of the transaction and therefore being more economical.
So it might make Snicker a lot less attractive.
I guess that's what you had in mind, is it?

Speaker 2: 01:04:47

Yes.
But on the other hand, if you actually assume interactivity, then you can assume that every wallet will implement the signature aggregation and if snicker wouldn't implement it then it would just mean that's a Snicker transaction because that's...

Speaker 3: 01:05:08

Yeah, yeah, yeah, yeah.
It would mark it out as just different.
Yeah, but...

Speaker 2: 01:05:11

Yeah, but it doesn't matter because as you said, it applies if...
So if you pass around the transaction between participants, it's not a problem.
It's a problem when you just want to pass back the signature to the server.
No, because you have to pass around the signature.
But it's two participants, it's not a problem.
Anyway, that was for me all and go ahead guys, anyone has anything to ask, discuss?

Speaker 0: 01:05:48

I guess I'll say something maybe controversial or non-controversial.
I don't see Snicker being useful outside of the mobile devices like what Adam was saying.
I'm trying to wrap my head around different use cases, but it feels like it's really for the mobile devices.

Speaker 3: 01:06:12

I mean, maybe the only, I tend to agree, but maybe the counter argument might be, especially if Wasabi users, because I'm thinking about Wasabi specifically because of where we are.
Maybe if Wasabi users saw a value in having this kind of opposite to what Lucas was saying, because I almost think like the Wasabi users might want to do it between themselves and not involve the Wasabi server at all.
Because I think the Wasabi model is pretty strong, but there is a theoretical weakness of, you know, the server may be sort of sibling and stuff like that.
Maybe that's a bit silly, I don't know.
But but I just think maybe you could imagine because of Wasabi Coinjoin, like a joy market coin has the property of being a very but certain things have happened.
You might find it useful to sort of do extra coin joins pulling off the edge.
Or maybe that's not a good example.

Speaker 0: 01:07:15

There's also something about small coin joins that's very unappealing, which is that they're very inefficient.

Speaker 3: 01:07:21

Right, that's a good point.

Speaker 0: 01:07:23

Per byte, it's always better to have as many people as possible.

Speaker 3: 01:07:28

So yeah, it's sometimes easy to forget in 2020 or whatever, because fees are so cheap nowadays, but

Speaker 1: 01:07:36

only a couple of years ago it was just a bit

Speaker 3: 01:07:38

of a nightmare doing coinjoins.
It's a good point.

Speaker 1: 01:07:44

Well, You know, as I would agree that Wasabi is probably a bit too heavy software to do the receiving of these.
As Lukas said earlier, it might really be a good opportunity for WasabiCoin to be able to propose Snickers transactions and then that then other wallets, like mobile wallets, can do these rounds based on Wasabi users proposing them.
So that might actually be quite interesting how the Wasabi actually contributes to the proposing.

Speaker 3: 01:08:14

Yeah, you have a selling point there, don't you?
Because if I, as a receiver, get a proposal from a Wasabi output, then I can inherit partially some of the anonymity set, some of it.

Speaker 1: 01:08:31

Yeah, that's actually a great point that I didn't think about here.

Speaker 3: 01:08:38

It'll depend on the details, but it could be a thing.

Speaker 2: 01:08:46

All right, any more topics for someone?
Or we should move on to deciding what should be the next topic, next week's topic.
So yeah, go ahead if you have something.

Speaker 1: 01:09:02

Maybe Adam, specifically for, how do you want to do this with JoinMarket?
Do you have any implementation ideas specifically?

Speaker 3: 01:09:10

Oh yeah, so, well it's a bit stuck, because I wrote a PR for it, for just only the receiver side, about three, four months ago.
But a bunch of other stuff got in the way.
And then I realized I didn't really have a good PSPT library yet that I could use.
But that was just me.
What I really wanted to do was I wanted to write the receiver side into the into the joint market software and then set up a test server for a bulletin board.
And then obviously, it would have to make proposals.
But it would just be like me or like one or two people making proposals initially just to try it out, you know.
Because I'm more interested in just like having it, getting it tried out at this point.
After having at least a proposal is written now.
So it's there's some kind of like standardized format for it.
Once that's decided, then I was hoping there would be a proof of concept, but I haven't really finished.
So, you know, you know how it goes.

Speaker 2: 01:10:21

All right.
Anyone has anything left on Sneaker?

Speaker 1: 01:10:28

No, just my opinion is, you know, Max, for example, is a big fan of atomic swaps

Speaker 4: 01:10:33

and I think for example that sneakers is it is probably easier for us and it is it could be good if we can do something because we have this wallet that we have a server we can find a candidate on our server yes and we can have do the hard work and so okay but anyway it's just the hard work.
I disagree.
Ok, but anyway, it's just another opinion.
I think It could be possible.
I mean, we have the infrastructure too, we can have our bulletin board.
I like it.
Just that.

Speaker 2: 01:11:29

I believe there are other alternatives that could be more easier or more flexible to implement.
Just being a coinjoint taker in every transaction, pay to endpoints, so you would implement Tor communication between people and that would help a lot in salaries, giving out salaries too, because it's like,

Speaker 1: 01:12:03

could you give me an address?
Yes, it is the address.
Yes,

Speaker 2: 01:12:07

you know, whatever.
So but anyway, my point is that the very first issue that what Aviv said is that two of two coin joints are really inefficient so

Speaker 3: 01:12:22

good point

Speaker 0: 01:12:25

yeah

Speaker 3: 01:12:28

okay

Speaker 2: 01:12:31

so ideas for next week

Speaker 0: 01:12:35

I'm gonna politely ask recommend something which is the I think it's coin shuffle or cash shuffle.
The reason why I'm so motivated to learn and read about that is because apparently Bitcoin.com, Bitcoin Cash wallet is going to implement it for their mobile devices.
And so it's already in production or very close to production.
So I'd really like to investigate that.

Speaker 2: 01:13:04

I've read the CoinShuffle and CoinShuffle++ papers and they are very...
I don't disagree.
I just want to say that if we go with cash shuffle, then let's just start with cash shuffle paper.
Not cash shuffle plus plus, not value shuffle.
What?
Ah, sorry, sorry.
Coin shuffle, I'm talking about coin shuffle.
So let's start with the coin shuffle paper and then go one by one on the things.
Okay, so coin shuffle, one idea.
Another idea?
Okay, I have a couple.
I have a couple.

Speaker 4: 01:13:55

You know, for me coin shuffle is also something that we have to take a look at I've read the coin shuffle and coin shuffle plus plus papers, they are very interesting but the problem is I think we will never implement something like that.
So, I don't know if...
Yes, it is good to know more but I don't know if if we will gain some

Speaker 2: 01:14:26

Opinion on on sneaker that I think we will never implement it, but it just brought me two insights about top root and hashcash that I value a lot you know and we did not really start to work on the new mixing We just trying to learn more because there is a lot to learn, you know So, yes Then I have ideas.
I have a couple of things.
I just I just see it then one is coin join Sudoku Which is which is analyzing coin join transactions.
It was actually analyzing blockchain info transactions.
That's interesting.
Another one is Boltzmann from, you guys might know Boltzmann from Lowrent at somewhere.
I think that's an interesting thing to take a look at.
Another thing is Knapsack code because the guy just gave us a codebase that would be really interesting in light of that we know now how Knapsack was analyzing the transactions, how the Knapsack paper was analyzing the transactions.
So I think that blog post would be really interesting.
So let's do the vote.
Who is voting for CoinShuffle?

Speaker 4: 01:16:33

Okay, I'm voting for Coinshopper.

Speaker 0: 01:16:35

Yeah, me too.

Speaker 2: 01:16:37

Ok, Coinshopper 2, 3,

Speaker 4: 01:16:43

4.
Wait, just one more point, sorry, 4.
Next time, instead of Coinshopper++, for example, we can go directly to the Dining Cryptographers problem and the DC networks, instead of jumping directly to the to the coin shuffle plus plus because it's it's not so easy to to catch the first

Speaker 2: 01:17:17

okay so we have four votes to coin shuffle and Dining cryptographer DC nets Dining cryptographer networks Who's voting for that?
I I vote one.
Who else?
Lucas of course

Speaker 4: 01:17:38

No, but not for the next one the next was only concha from probably should yes exactly

Speaker 2: 01:17:48

okay all right so coin joins sudoku I vote one you can vote for multiple things by the way sorry okay

Speaker 0: 01:18:01

Sorry, I'm not working with that

Speaker 1: 01:18:03

as well.

Speaker 2: 01:18:03

The Sudoku.
Okay.
Boltzmann.
I vote one.

Speaker 1: 01:18:12

May I have a vote, Peter?
Yeah, would be cool.

Speaker 4: 01:18:17

Yes, I vote for that too.

Speaker 2: 01:18:21

For Knapsack code, I vote one.
And the last one is the Cash fusion analysis amount analysis is very similar to Sorry, I didn't hear it.
Can you repeat it max?
You're voting to this okay, that's Two votes Looks like no one else is voting.
So we have CoinShuffle and Boltzmann with four votes.
How should we decide on that?

Speaker 4: 01:19:13

Whoever- With a coin.

Speaker 3: 01:19:18

Yeah.
Vote on the blockchain.

Speaker 2: 01:19:24

Sorry?
Oh

Speaker 4: 01:19:25

yeah, you can vote.

Speaker 0: 01:19:27

Okay.
Adam, why don't you break the tab?

Speaker 3: 01:19:33

What, is it me?
I don't know.
I don't.
I think, yes, it's a huge amount of stuff, you know.
No, I don't really know.
I'll let you figure it out.

Speaker 2: 01:19:47

All right, so, okay, let's do this.
Our bot, we do the coin shuffle, but that means for the next 5 weeks we are full because CoinShuffle, DCNets, CoinShuffle++ ValueShuffle, CashShuffle, CashFusion I don't know But yeah

Speaker 4: 01:20:13

Oh well, I have more If Adam one day can help us again, it would be great to have something about better commitments, ring signatures, confidential transactions.
Adam actually wrote

Speaker 3: 01:20:30

a...
Don't forget, to do CoinShuffle++ you also need to learn how to factorize Polynomials over finite fields, so that'll be a nice short session as well

Speaker 1: 01:20:45

weekly like a daily let's do it yeah

Speaker 0: 01:20:53

let's

Speaker 2: 01:20:59

do it coin shuffle

Speaker 4: 01:21:00

next week

Speaker 1: 01:21:00

anyone has

Speaker 2: 01:21:01

anything to say talk about what did you think about this episode, Adam, how you liked it?

Speaker 3: 01:21:10

Oh, sorry, you're asking me?
Yeah, that was great.
Yeah, that was, I was very useful, actually.
I like the presentation.

Speaker 1: 01:21:22

All

Speaker 2: 01:21:22

right.
Thank you, guys and See you next week.
I hope we have an attendance like this

Speaker 1: 01:21:39

Thank you very much Adam for joining us, it was very very helpful and insightful.
Keep

Speaker 3: 01:21:43

it up.

Speaker 0: 01:21:43

Yes, Thank you.

Speaker 1: 01:21:45

Thank you all.

Speaker 2: 01:21:47

Thank you guys and don't forget to like and subscribe.
