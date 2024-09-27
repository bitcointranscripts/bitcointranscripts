---
title: "Making Bitcoin More Private with CISA"
transcript_by: kouloumos via tstbtc v1.0.0 --needs-review
media: https://www.youtube.com/watch?v=HvI7NPI_Pk0
tags: ['cisa']
speakers: ['Fabian Jahr', 'Jameson Lopp', 'Craig Raw']
date: 2024-08-29
summary: "Delve into the world of Cross-Input Signature Aggregation (CISA) with our expert panel from Sparrow Wallet, Bitcoin Core, and Casa. This discussion illuminates how CISA could revolutionize Bitcoin transactions by enhancing privacy and reducing fees. Uncover the technical aspects of half and full signature aggregation and understand their potential impact on the Bitcoin network."
---
Speaker 0: 00:00:01

So there's one person on the stage here that is not up there.
Why?

Speaker 1: 00:00:07

Hi, everyone.
My name is Nifi.
I'm going to be moderating this panel today.
We're here to talk about CISA, I think, cross input signature aggregation.
And joining me today on the stage, I have Jameson Lopp from Casa, Craig Rau of Sparrow Wallet and Fabien Yarr of Brink.
So welcome them to the stage.
Really appreciate it.
Yeah.
Great.
So we're excited to be talking to you guys about this.
I think it'd be great maybe to start off hearing a little bit more about who's on our panel today.
So if panelists, you could tell the audience about the project that you're working on and what your first, like where you first heard about SISA from, if that makes sense.
So Craig, do you want to start?

Speaker 2: 00:00:55

So I built Sparrow Wallet.
It's a security and privacy focused wallet.
The first time I heard about Caesar was really from you know other privacy activists in the Bitcoin space who were talking about you know how they were really hoping that this cross-input signature aggregation was going to be shipped as part of the taproot upgrade and Obviously, we know that that didn't happen so when you know you're looking at things from a privacy point of view you want to do things like create multi-party transactions and as we will hear, cross-input signature aggregation really provides an interesting basis for being able to do that on a more economic, with more economic benefits.
So that was the first time that I kind of really started to look at it was from the privacy angle.

Speaker 0: 00:01:54

Yeah, I primarily work on Bitcoin Core and I can't really remember a specific time when I heard about it for the first time.
Like the time between the SecWit Soft fork and the Taproot Soft fork was really when I got very, got deeper into Bitcoin and like started contributing to Bitcoin Core and somehow it was always there.
And I only, when I started researching on Caesar and going deeper into it over the last couple of months I saw also that yeah historically it was a topic that was brought up and that was discussed to be part of the Taproot soft fork, but then at some point it was cut basically to keep the scope smaller.

## Remembering the Past and Discovering Cisa

Speaker 0: 00:02:40

And so I guess at some point around that time I saw it and then it was removed and I never really paid much mind to it around the time.
And when I reviewed the Taproot soft fork, it was not in there.
So I kind of forgot about it for probably one or two years.
And then, yeah, but it kept popping up on Taproot.
Also, like Craig said, more privacy minded people.
And that triggered me to look deeper into it.

Speaker 3: 00:03:09

I'm Jameson Lopp.
I work on Kasa, where we help people get into highly distributed, secure, multi-signature self-custody setups.
And I could be misremembering, because it's been several years, but I think the first time that I heard about Sisa was an Andrew Polstra talk.
And I mostly remember being blown away by the vision that he painted of basically a future in which we were all financially incentivized to participate in coin join transactions for everything that we transacted and basically you know breaking a lot of the potential for chain surveillance to be watching everything that we're doing because, you know, I think if we're all honest with each other, Bitcoin has some pretty poor privacy characteristics.

Speaker 1: 00:04:03

That's a great point.
Wow, yeah, okay, so I think now that we've kind of have like an intro into how each of you came to hear about it and maybe some of the things that you thought were important or cool when you first heard about it, Maybe we could take a little bit of time to explain a little bit more what CISA is and what those letters stand for.
Does anyone have a good explanation of how it works?

Speaker 0: 00:04:29

I can start off.
So it's really already all in the name.
Cross-input signature aggregation.
So if you think of a Bitcoin transaction as it looks today, you have sometimes one but often multiple inputs and with each of the input usually a signature is associated.
And what the linearity property of Schnorr signatures allows you to do is to aggregate these signatures.
And you can aggregate them across the different inputs that you have in a transaction.
And so that means that in the future we could have transactions that have multiple inputs.

## Cross Input Signature Aggregation

Speaker 0: 00:05:09

If you think specifically about transactions that have a lot of inputs like coinjoins for example as we just mentioned, these could have just one signature then.
And depending on what technique you use, these can be just as big as one single signature before.
And of course, that saves a lot of space, both on chain and also in terms of the fees, because you take up less space in a block.
That is the general idea.

Speaker 1: 00:05:35

I have a quick question about that.
So whenever you say you can do cross-input signature aggregation, so like on a transaction, usually you'll have a couple of things called inputs, and each of those inputs will have a signature on it, right?
So kind of the general idea is that on that same one signature, instead of having a couple of them, you kind of be able to roll them all up and just have a single signature.
Is that a good summary of What you're explaining?

Speaker 2: 00:06:02

Yeah, I would say so.
Yeah, so there's two major ways to do this.
The one is what we call a half signature aggregation, or half ag as we abbreviate it.
And that's basically where you don't have any kind of need for an interactive process.
So anybody can take all of the signatures that appear currently for every input in a transaction and they can aggregate them into one.
Now the size of that one is unfortunately not the size of a normal signature, it's a slightly bigger one.
In fact that size is determined by the number of inputs that you have.
So that's one way to do it.
And then there's a more comprehensive way to do it, which is called full signature aggregation.
And that gets you a really much more compact signature, which is the aggregate of all of the other ones.
Unfortunately, the downside of that is that you have to do this interaction while you sign.
And the problem with that is that interaction is always contains a lot of complexity.
So unless you own all of the inputs you are going to have to interact with all of your everyone else who's adding an input to that transaction.
And that creates, obviously, a much more difficult process in terms of signing.
And as a result, we generally, at least I personally, am more excited about the kind of half signature aggregation because it's just so much easier to do and gets you a lot of the benefits, even though it's not quite as efficient.

Speaker 1: 00:07:39

Cool, so it sounds like we're taking signature data and it's all the same signature data in like a single transaction, right?

## Various Approaches to Signature Aggregation

Speaker 1: 00:07:46

You wouldn't have multiple transactions that you're doing, it's like on a single transaction level.

Speaker 3: 00:07:50

Well there's also full block aggregation, right?
Okay.
This is going really far down the rabbit hole and I think that it's not even something that is on the table.
Because there's too many additional edge cases, I guess, that come up, especially when you start thinking about like reorganizations of the blockchain.
And my understanding is you would basically have to have like this other mem pool to keep track of things that, you know, were not sufficiently buried enough in the blockchain that they could be reorganized, because if there was a reorg, it would not be as simple as how we do reorgs right now, where we just take every transaction out and put it back into the mempool and start over again.

Speaker 1: 00:08:33

Right, cool.
So it sounds like you're saying there's a couple of different ways we could do signature aggregation.
We could do it at the transaction level, there's a proposal to be able to do it at the block level, but again, there's some tradeoffs there.
So one of the nice things if you were able to take basically signature aggregation at the block level would mean that you take all the signatures anywhere in any transaction inside a block.
And for that, you'd create maybe a single signature object.
Maybe it's not exactly a signature, but something similar to that.
Why is one reason that you would want to even do this?
It sounds complicated, but.

Speaker 3: 00:09:07

Yeah, well, so there's the privacy characteristics improvements.
But also, I think it's interesting whenever we're talking about incentivizing people economically.
So if anyone was around and paying attention in 2016, 2017, when we were talking about segregated witness, there was this concept of a witness discount.
It was basically put in place to help incentivize people to help rebalance the cost between creating a UTXO and spending a UTXO.

## Incentivizing Participation in Coin Joins

Speaker 3: 00:09:45

Basically, you run into some problems where if you're receiving a lot of transactions, you're basically creating a lot of unspent transaction outputs in your wallet, it becomes problematic if at some point in the far future you want to go spend them and perhaps the fee rates in the market for block space have gone up a lot, it can become insanely expensive to spend your own money and this inevitably catches a lot of people by surprise if they haven't been through a full market cycle before.
So I think that this is another potential interesting aspect of aggregation is that once again we would be pushing the balance forward a bit to help incentivize people to you know clean up their UTXOs because we're not we're not penalizing them as much by making it really expensive to do so.

Speaker 0: 00:10:37

And maybe to expand on that, so there is a financial incentive then for people to participate in coin joins and that gives them additional privacy And the nice effect of that also is that hopefully this would lead to also like wider adoption of CoinJoin, which means that when more people are CoinJoin, that's a higher anonymity set that benefits everyone that is after this anonymity property, but also everyone that participates in this coin join can also use this as a plausible deniability, even if they are doing it primarily for the privacy aspect, but they can also always say like, hey, I'm saving fees here.
So that's my primary motivation.
And hopefully a further trickle-down effect would be that when people are more asking for this, when this becomes more widestream adopted, then also more and more wallets adopt this.
Easier to use wallets, complexity gets hidden and it becomes more of a mainstream feature.

Speaker 3: 00:11:36

Yeah, I mean we have to think about the incentives, right?
I consider myself a cypherpunk, I'm a big privacy advocate, I would assume we all are, but the reality of the situation is, and this is pessimistic, most people don't care about privacy or they don't care until it's too late, and so we can stand up here and we can talk about how awesome it is to have really strong privacy and why you should be using all of these insane tools that are very niche right now.
But if we actually want people to adopt privacy tools, we need to give them the financial incentive to do so.

## Privacy Tools and Cost Savings in Bitcoin Transactions

Speaker 3: 00:12:16

It should not be a situation where the average person should be going out and basically asking their wallet providers or other software developers to, you know, please bake in additional privacy tools and protections into the software.
Really it should be, why are you making me spend more of my money to use Bitcoin when you could be using this technology that, you know, it happens to enhance privacy, but it's actually saving me money.

Speaker 2: 00:12:45

Yeah, so you might be wondering at this stage what are the savings actually look like and it turns out that if you apply what I was describing earlier, this half signature aggregation technique, you can fit about 20% more average size transactions into a block.
So you can immediately think that that's going to reduce the average fee level for any point in time people submitting transactions to the mempool to be included in a block, you can now fit 20% more average-sized transactions into that block.
That obviously is a big advantage.
Now the actual effect on a particular transaction because of the witness discount that Jameson mentioned earlier is actually less.
So there you've got like a seven to eight percent.
But remember that the average fee rate is going to be lower because again, we're fitting more transactions into a block, which just means there's less pressure on block space.
So that's how I would encourage you to think about it from the start.
Like, for me, the efficiency in terms of block space is a good reason to do this anyway, regardless of whether we get privacy benefits, it's almost like the privacy benefits come along for the ride.
We actually have this really restricted data space in the blockchain, and if we can apply a fairly simple and low-risk form of compression I think it's a serious thing to think about.

Speaker 1: 00:14:12

I think you know now that we've sort of talked about how great this is we're gonna get more transactions in a block we're gonna save money we're gonna get better privacy I'd be really interested to hear why it didn't make it into Taproot originally.
Like, is there any opposition to this proposal?
What was it about Taproot or the Taproot process where this proposal didn't quite make it over the line?

Speaker 0: 00:14:40

So I mean, I was not in the room when this...

Speaker 3: 00:14:45

I don't think any of us were in the room.

## Pushback and Perceptions of Soft Forks

Speaker 0: 00:14:49

But I've read all of the transcripts that were available from when these things were discussed.
And from what I can say, I think there was no direct opposition or so.
I think the primary motivator was to keep Taproot manageable in terms of review effort and just keep the scope smaller.
The only thing that I could see really in between the lines, what Craig already kind of mentioned is that if you just look at the pure fee savings numbers and the numbers of weight units that you save, if you just throw that over to somebody that it's for half aggregation in the single digits, then people are often a bit disappointed as a first reaction and you have to really discuss it and fill it a bit more with this understanding and I think that made it also have turned off some people and like why maybe also developers felt like this would be the easiest thing to chop off but that people wouldn't miss as much.

Speaker 2: 00:15:53

Yeah so I mean I think you know in terms of the whatever pushback I have heard so far is what Fabian was saying that it doesn't do enough.
You know, I think that there's a general perception that, you know, we can only ever push for one soft fork at a time, so all the soft forks have to compete to be the one, which is an interesting point of view.

Speaker 3: 00:16:17

It's interesting because I was in the room in Hong Kong when Peter Wille announced that we were changing the flagging system so that we could do like 32 soft forks in parallel.
And of course, we have not yet taken advantage of that.

Speaker 2: 00:16:33

Yeah, so we're in a very different space from that now.
I think something to bear in mind, if you're thinking about it from that point of view, is that, and I heard Brandon Black actually, who was here earlier today talking about Opcad, is that I think Caesar is probably the most low-risk soft fork that we could imagine.
And I'm talking here about the well-understood half signature aggregate form of it.
You know, it's really from a security model point of view, the cryptographers tell us that there is no risk effectively or very low risk to doing this.
It really takes very well understood properties of Schnorr, which is really just adding these signatures up and uses that.

## The Limited Potential of Signature Compression

Speaker 2: 00:17:18

So in terms of risk of doing the soft fork it's not really enabling other things that Bitcoin can do.
It's not going to be some kind of ungranted, it's really just compressing.
And if you think about it, compression is a fairly bounded area.
You're not going to suddenly have people developing all kinds of perhaps unwanted things on top of Bitcoin just because you have compressed the signature size down.
So maybe it opens up the space for other soft forks if we do a soft fork which has such a low risk to it that it actually gets across the line.

Speaker 3: 00:17:57

I think it's also worth noting that this is by no means the only signature aggregation scheme that's even happening in Bitcoin, right?
Is that like with the taproot soft fork a few years ago, we did get the theoretical ability to do Schnorr signatures.
But that has been an ongoing process, right?
So as far as I'm aware off the top of my head, there's a pretty limited amount of adoption of Schnorr so far because I think Music, Music 2, is the main production-ready standard that people are using.
And that can only do an N of N, like a two of two or a three of three type of scheme, so it's kind of limited in its flexibility.
And I care about this a lot, operating a multi-signature self-custody wallet, We're waiting for the further evolution of threshold signature schemes like Frost that can do more arbitrary, K of N type of multi-sig.
And That evolution, that research is still ongoing.
We're continuing to see new iterations of Frost come out.
And so we do expect that we will start to see more adoption of aggregated signatures across the ecosystem.
But the ultimate end goal would be something where there's only one signature per block.

Speaker 1: 00:19:22

The final form of SIGAG as we go all the way to the block level.
Cool, so we only have a few minutes left.
Maybe we can spend a little bit of time talking about, okay, so we almost had it, we didn't get it.
What would it take, what's left from here to get it to the point where we could soft fork it in?

Speaker 0: 00:19:45

There's still quite a few things to hammer out in terms of all of the details, like defining a spec.

## Signature Aggregation and Getting Involved

Speaker 0: 00:19:53

So for the half-arc, there's a BIP draft, but it's not a pull request on BIP repository, but there's just minor to-dos like test vectors there that are open however for the full aggregation we still need to develop the signature scheme, so that requires quite a bit of effort from people reversed in cryptography and specifically on the side of the interactivity and We will also want to have a security proof for that scheme that comes out on the other hand and that means people with Very specific talents and an experience in that area will also be needed in process so so these I think are the big to-dos that we have and Yeah The people that can do this stuff need to come together and work on it.
Personally, I spend quite a bit of time on it right now.
But maybe something to everyone watching this or in the audience, if you want to get involved, let us know.

Speaker 3: 00:21:01

Call your local developer and demand signature aggregation today.

Speaker 2: 00:21:05

Yeah, and just to that point, Fabian has developed a great site where you can learn more.
So, you know, if the concepts that we've talked about here today make sense, if you want to understand them better.
If you go to sizeresearch.org, that's C-I-S-A research dot org, you know you can really learn much more about it.
It's very easy to read, It's not going to be overly technical.
And I think it gives a good grounding in these things.
And then, largely the way that soft forks happen is that people need to express views about them, and ultimately we need to develop some form of rough consensus around whether we want to do it or not.
So as far as I'm aware, this is the first panel we've had which talks about it.
It is still, even though it's an old concept and it's a simple concept, We don't really have a lot of discussion about it right now.
So talk about it.
Try and develop an understanding of what it is that it's trying to do, and see whether you want to have it in Bitcoin or not.

Speaker 3: 00:22:17

I don't know.

Speaker 1: 00:22:17

Do You You
