---
title: 'Coinjoin Done Right: the onchain offchain mix (and anti-Sybil with RIDDLE)'
transcript_by: delcin-raj via review.btctranscripts.com
media: https://www.youtube.com/watch?v=khmLiM9xhwk
tags:
  - coinjoin
  - adaptor-signatures
  - timelocks
  - ptlc
speakers:
  - Adam Gibson
date: 2022-12-10
---
NOTE: Slides of the talk can be found [here](https://github.com/delcin-raj/btc_transcripts_materials/blob/main/cdmx2022.pdf)

## Introduction

My name's Adam Gibson, also known as waxwing on the internet.
Though the title might suggest that I have the solution to the problem of implementing CoinJoin, it's not exactly true.
It's a clickbait.
I haven't, but I suppose what I can say in a more serious way is that I'm proposing what I consider to be a meaningfully different alternative way of looking at the concept of CoinJoin and therefore at the concept of on-chain privacy because the conversation nowadays about on-chain privacy tends to be dominated by CoinJoin.

What is the right on-chain privacy model?
Max (Hillebrand) this morning [has given you an excellent sort of whirlwind tour](https://www.youtube.com/watch?v=dF8sNwp7XiY) of all the most basic and important concepts - the ground zero of on-chain privacy - thinking about change outputs, thinking about address reuse, etc.
Of course, we saw at the end of that an example of one of the most developed ideas that exists today about how to do CoinJoin, which is Wasabi, or Wabi Sabi or Wasabi 2.0.

An outline of what I'm gonna talk about, I'm mostly gonna focus on those first three:
- Do we need CoinJoin, why do we need it
- what are the problems with it
- and then my proposed alternative solution, which is "CoinJoin done right"

## The need for CoinJoin

### Hard Money

#### Onchain is the industrial layer

What I've thought about this stuff for I guess 10 years now, is that I don't see on-chain Bitcoin as a consumer payments network, and I think anyone who thinks it is just misunderstood it, and that could even include Satoshi - shock horror - who talked about vending machines.

I think it's just not the right characterization of what the system actually is.
It's more like a hard money system, which means I've sometimes used the phrase, "SWIFT not Starbucks points".

#### Bitcoin is financial Uranium

I've sometimes said to people, Bitcoin is financial plutonium or uranium, which is my way of saying, this is dangerous stuff.
If you're an engineer and you know what you're doing, then you probably will be okay.
If you're not, you need to be very, very careful.
Because there are things about it that are not obvious.
There are things about it that are very inconvenient.
If you let your impatience get the better of you, you've got a very good chance of losing your money or perhaps not losing your money and then just having very bad privacy as well which is obviously the topic of this conference.

#### Buying and Selling bitcoin on a CEX (Centralized Exchange) is like financial anthrax

I jokingly point out that if Bitcoin is financial plutonium, then buying and selling on a CEX is financial anthrax.
And my point there is that if you're a nuclear engineer, you can handle plutonium correctly, you know the procedures, but if you're handling anthrax on a daily basis, eventually you're gonna die, okay?
So please avoid the centralized exchanges.
This is not the right time to make that comment because everyone's, I should have been putting Sam Bankman-Fried there, of course, but I'm old, so there we go.

#### Lightning vs Onchain payments

The purpose of the section is just to emphasize that point.
We're dealing with something that's difficult to do.
Handling On-chain Bitcoin is difficult.
I know it certainly wasn't accepted to say that back in the day.
It's more accepted nowadays.
I think people get it.
Partly because a second layer exists.

And to come back to my point, for consumer payments network prefer lightning over on-chain Bitcoin.
You know, at least it makes an effort doing that, being usable as a consumer payments network.
But on-chain activity, fundamentally, I would argue, and this is maybe a little bit of a hot take on this slide, you know, is a kind of a political act.
Just even using on-chain Bitcoin at all, let alone using CoinJoin, which I think is definitely a political act.
And I've had many private conversations, including with people in this room and many other sort of Bitcoin users, who confide in me that they want to be virtuous and use CoinJoin like they're told to use CoinJoin, but actually they don't do it at all because they're really scared, and I don't blame them.
Why wouldn't you be scared, you hear stories about the Coins getting blocked all the time.
So, you got to be sensible about these things.
If this is money that actually matters to you, and it's not just a toy, then you've gotta be quite careful about what you're doing.
So I know that's a whole can of worms I'm deliberately gonna not unpack right now, but let's consider that framework that we're talking about a serious form of hard money which has a political component to using it.
On the other hand if we're talking about something like lightning we could say it's not a political act.
Maybe that's a weird thing to say, like if I make a payment with on-chain Bitcoin it's a political act, if I make a payment with lightning it's not.
I can't 100% defend that position but maybe it gets your brain thinking about these issues.


### Why is Privacy Hard

Blockchains are inherently public.
We, as the on-chain privacy community, are, in some sense, trying to do something ridiculous and impossible which is to make something which is inherently public be not public.
And of course projects like Monero and Zcash extend this further, right?
They say, you know what?
The very design of Bitcoin is not good enough for that, we need a design that is properly intrinsically private but I think embedded in that they end up with sort of paradoxical situations and I remember in building on Bitcoin in 2018 I was on a panel and I said, you know, Zcash is great and all, but what if there's a bug which causes inflation?
Nobody will know.
And then six months later, it came out that there was a bug which caused inflation, which nobody knew about, and which they had hidden for an entire year, so for six months before I was on that panel.
So that was a kind of amusing experience for me.
But I think Peter Todd at the back of the room here is one of many people who pointed out before the event, and of course he was involved in the creation of Zcash, that this is a fundamental kind of failure mode you have in such a system which is unavoidable no matter how good your cryptography is claimed to be.
Because the problem is not like is the cryptography sound.
The problem is in the flow from the brain of an academic to a paper, to an engineer, to another engineer, mistakes get made in building these systems. They are intrinsically very difficult to build.
So that's why I say the DNA of blockchains is to be public and trying to make them not public, you kind of tie yourself up in knots a little bit.
I won't go through this text (referring to slide#5).
You can read it later if you care.
I end with a lightning payment as an apolitical act, as my sort of little punchline there.

#### Attack on Zcash

This graph (referring to slide#6) shows an attack that recently happened on Zcash in which somebody spammed their blockchain with five transactions per block, created in a way that it filled up the entire block.
Due to the privacy argument that oh, we should have a fixed transaction fee independent of the size of the transaction, which is just insane.
And anyway, so at the end of the day, they were just spamming the block.

(Additional context:
Zcash uses UTXO model and provides shielded transactions where inputs and outputs are obfuscated.
So the attacker was able to create hundreds of outputs using a very small fixed amount of fee and it
resulted in the blockchain size growing from 31GB to 100GB from mid June to October of 2022.)

And then I'm saying that oh look, the history of Zcash, that is so to speak the nullifiers, which are a bit like key images, which I'll talk about later.
They have to accumulate infinitely because you've essentially got a state that can only increase in size because you can never delete state because you're deliberately obscuring the fact that a particular coin has been spent.
So that's a kind of simplified summary of what's going on there.
And I'm kind of like obfuscating the fact that that's not really the same thing on the graph and in the text, but they are kind of related.
Like the more state you create in Zcash, the more of an issue it is that there's this infinite history which you can never prune.
Maybe this is unfair, maybe the cryptographers are gonna come up with clever ways to deal with that.
I'm not sure, I really don't know.
But there's certainly big problems with taking this approach to privacy.
But it is an obvious approach to privacy.
Let's not be a Maxis who think that anything which isn't Bitcoin is the devil.
We should at least look at these systems.
And I have looked at some aspects of some of these systems.
I find them very interesting.

## Problems with CoinJoin

CoinJoin, as I said earlier, is the way we're tending to do things.
Let's even forget about JoinMarket for a minute.
Let's just say Wasabi, or let's just say Samurai.
People have this idea that make every spend a CoinJoin is somehow the ideal.
If I said I don't think we should make every spender CoinJoin, would you agree with me?
And if so, what's your thinking?
Put it this way, does anyone agree, no, I have to put it this way around, does anyone disagree with this statement, and if so, why?

### Bigger Transactions

[Peter Todd]: "I'll give a huge disagreement.
I would say it's okay that some users, like my OpenTimestamps transactions, have technical reasons where CoinJoin just are a nuisance.
And we shouldn't hate on the people who have reasonable reasons like that.
But they certainly are a niche."

I'm just curious why, I mean, I can see a reason why you'd say we don't need CoinJoin for OpenTimestamps, but why would it be a nuisance?

[Peter Todd]: "Well, because it makes transactions bigger, which makes the proofs bigger.

That's a good reason, yeah.

[Peter Todd]: "Also, because I update the tip of the Merkle tree for all the timestamps every single block, how exactly you'd implement that with CoinJoin?
It's not really clear how you do it."

So it's technically difficult, right?
I think the most important point coming out of that is just the size question, right?
Most ways of doing CoinJoin are going to increase the amount of space we use on the blockchain.

### Centrally coordinated smooth experience. Can't choose amount

Chris Belcher and I in JoinMarket in the early days and many other people of course realized that CoinJoin is cool and all, but you can't have everyone doing equal output sized CoinJoins all the time.

[Audience]: "I would guess also that when you're CoinJoining, you sadly are beholden to the best practices of the other people involved in the round.
And if everyone is just CoinJoining by default with no regard paid for the actual necessity of their own privacy, they might just recombine everything after.
I mean if everything is a CoinJoin, I don't know what that really looks like, but if you're not going to act in a way that preserves privacy and you're CoinJoining with people that actually need it, you might hurt them inadvertently."

Yeah that's a very important point about the fragility or brittleness of these collaborative transactions, as people tend to call them nowadays, is that you can't assert the quality of privacy you get because it depends on not only behavior before, which you can read on the blockchain, but behavior after of your counterparties.
So that's a very problematic aspect.
There's obviously lots of answers to that, this is debatable, but I wanted to illustrate what I think is how it's working today, which is that people are using CoinJoin mostly in these systems.
I mean, Wasabi 2.0 already sort of invalidates some of the things I'm saying here, but in the centrally coordinated model, the idea is that you have to agree on an amount, and that's not very true with RB2, well it kind of is and isn't with RB2, but let's just say, because you're having a central coordinator, who gets to decide what the amount is, so therefore, generally speaking, you have what they call fixed denominations.
If you have fixed denominations, you're gonna get a smoother experience because the central coordinator can handle a lot of the nonsense.
But the inability to choose an amount causes problems like "toxic change".

### Market based, not smooth experience on-chain fee watermark

On the other hand, if you go the other extreme like JoinMarket tried to do, you have a market based system.
You have to handle a lot of problems yourself as a user that otherwise would have been handled by the coordinator, such as Sybil Attacks, or things similar to Sybil Attacks, I won't go into details.
And it makes the experience a lot less smooth.
It also has a much bigger problem, which is an on-chain fee watermark.
So if the fees are being paid from certain participants in the collaborative transaction to another participant because that participant is offering liquidity as a service, it means there's gonna be a discrepancy in the, I'm not going into details, I'm just giving you like the high level idea that, for example, the inputs of one party might be, have more fee deducted from them than the inputs of other parties, which might make it easy for you to identify the inputs of the person who was paying for the service, as opposed to the people who were offering the service and getting paid.
I mentioned this recently in a post on Mastodon, but it suddenly occurred to me, because I listened to a podcast by Sjors Provoost and Aaron van Wirdum about the recent case of Alexey Pertsev, who was imprisoned in the Netherlands, and not yet charged, I believe, but imprisoned for multiple months for being a coder for Tornado Cash, or being part of the Tornado Cash team.
And while we don't know the full details, it apparently is the case that the basis of the prosecutions keeping him in prison is mostly around the existence of a token called TORN or something, which, well, is not directly inside the sort of tornado cash contract execution.
It's inside like some relaying process, and why do you have to relay transactions into the tornado cash process?
It turns out, it's precisely because of on-chain fees, because if you do this anonymity process in their contract naively, the fact that you're paying a fee in Ethereum for the execution of the contract kind of somehow gives away who you were to begin with.
So it's exactly the same issue.
We often find ourselves stumbling if we try to make properly decentralized, properly trustless versions of these cooperative or collaborative transactions for privacy.
We stumble over the fact that there's a fee that has to be paid and if it's being paid directly on-chain, then we come back to that, the DNA of blockchains is to be public, right?
Which means that you have a big problem.

### Economically incentivised vis CISA (Cross input Signature Aggregation)

That's part of what I'm gonna try and solve in the remainder of my talk.
Okay, in the remainder of my talk, it's gonna get very technical from now on, so I apologize in advance for people about that.
I'm not gonna get into the question of economic incentive via cross-input signature aggregation.
I defer you to Jonas Nick who actually worked out the numbers.
I just want to say that economic incentive for CoinJoin via cross input signature aggregation is a bit of a red herring.
A, because the actual amount of fee savings is quite minor as according to the tables [here](https://github.com/BlockstreamResearch/cross-input-aggregation/blob/master/savings.org), 
but also because cross input signature aggregation incentivizes transaction batching but a batched CoinJoin doesn't incentivize a specifically privacy-preserving CoinJoin.
And I'll let you just figure out that on your own later.

## Steganographic Decentralized Market-based CoinJoin (SDMC)

## Steganographic

So I wanna introduce a new concept, which isn't actually new.
I think I first talked about this in, I'd already mentioned Lisbon in 2018, so it's four years ago now, more than four years ago.
But I only introduced the basic concept here, and I think it's developed significantly, at least in my head, maybe not in actual code.
So can we make CoinJoins or things like CoinJoins, let's say collaborative privacy enhancing transactions that are steganographic and if you're not familiar with that term it just means they're CoinJoin that don't look like CoinJoin so they're not obvious.
Coinswap for example has a steganographic property a little bit because you don't see an obvious pattern.
You can't immediately recognize it on the blockchain, so steganographic is decentralized.
I think that the central points of failure is a big issue which we will continue to stumble against in this field.

## Market-Based

Market based because markets solve a coordination problem.
So as was already mentioned this morning, the only really big advantage of JoinMarket is that one person can choose the denomination themselves.
Because they're still kind of CoinJoin, but they also kind of aren't.
So what the heck am I talking about?

## CoinJoinXT (basic idea)

(refer slide#9)

So start with the basic idea.
CoinJoin XT, now the XT is just like a meme.
It was funny four years ago, it's not funny anymore.
But never mind.
So you can just think of it as extended CoinJoin, okay, because that's the the non-meme aspect.
Yeah, okay maybe it wasn't funny for years ago either.

Basically the idea comes from, how did SegWit change Bitcoin?
I'm not going to put this to the audience because you could answer that 10 ways, but the most important thing is lightning.
Anyone here who knows lightning probably knows that why SegWit was important for lightning is it allowed you to pre-sign a transaction using an input that wasn't yet confirmed because you know the `txid`, the transaction id of the transaction before it's on the blockchain, and why did that change in segwit?
Why did segwit allow us to pre sign transactions?

[Audience]: "To go over the transaction malleability which meant you couldn't fool the other party."

And what caused transaction malleability?

[Audience]: "The witness data being a part of the transaction rather than being separate."

And why would it malleate?
Why would that witness data malleate?

[Audience]: "Because you can change trivially.
I can't remember exactly what you can change about it, but you can create a new valid transaction that does the same thing, but with a different signature."

The idea is that, I guess it's kind of important for something else that comes up later is that, we sometimes forget that when we sign something with ECDSA or with Schnorr, we can always make a new signature with a new nonce, same private key, we can make effectively an infinite number of signatures.
So that fact meant that Lightning didn't work without SegWit, but now the witness is outside the transaction ID, you can't malleate it, so you can pre-sign transactions.
The idea here is just to exploit the same thing, but instead in Lightning, you create multiple versions of the same transaction, and they kind of, one overwrites the other with a punishment mechanism.

Here (referring to slide#9), I originally called this on-chain contracting.
Well, let's just have a bunch of transactions and they are all gonna go on-chain.
So the idea here is, there's a funding UTXO (F) between Alice and Bob that gets negotiated in such a way that Bob should recevie a payout at the end.
Then the two parties agree on a sequence of transactions (TX1, TX2, TX3, TX4) which are all linked by at least one connecting UTXO, which all has to be multi-sig.
And they're both gonna have to sign, pre-sign every one of these transactions first before they co-sign the funding transaction.
And that means that at the end of that process, they can both be assured, if at least one of them wants to broadcast all of these transactions, they will definitely all go through because the connectors, the inputs are multi-sigs which can't be reneged on by the counterparty.
Why does this matter for CoinJoin?
Well it means that after TX1, Bob can get a payout in TX1 without Alice also being paid something.
So in a way, Alice is lost out at this point, but all of these (TX2, TX3, TX4) are pre-signed and they can't go anywhere else.
So the idea is to break heuristics by the fact that if an analyst, a chain surveillance expert is looking at this transaction, they'll see a payment out there that might look like an ordinary payment.
We will see below that it depends on the details.

Another thing that might help you understand it is, suppose instead of just a pure sequence, we had an extra UTXO contributed by one of the counterparties inside of TX3.
Let m_{23} be a multi-sig from TX2 -> TX3, but there's another UTXO (A1) contributed by Alice to TX3.

Is that safe? Is it still the case that we can be sure that TX4 will get broadcast?
If this UTXO (A1) is only controlled by Alice, now remember, none of these have been broadcast yet.
We sign TX1, we sign TX2, we sign TX3, we sign TX4, and only finally do we sign this funding UTXO (F), or let's say create a transaction (say T) that pays into that funding UTXO, yeah?
And then that transaction (T) is on-chain.
So UTXO (F) exists, but all of this is just pre-signed by both parties, it's not on the blockchain yet.
So is it safe to just contribute another UTXO? 

[Audience]: "No, because Alice could double spend the money."

Right, so Alice could have given you a signature signing TX3 on UTXO A1, but could 10 minutes later spend UTXO A1 somewhere else.
So that's not safe.
So whenever we have something like that, we call that a promise UTXO.
It's a promise.
It's not a guarantee.
So we need to create time-locked back out refunds, paying out of the transaction before it to make sure that if she does that, we can still get our money back.
Does that make sense?
So notice here, we started with a 1 and 1 (initially deposited amount by A and B), so Alice contributed 1, so at this point (TX2), Alice should get paid back 1, but Bob should only get paid back 0.5 because he had an output in TX1.
Any questions about this structure because this will be extended in a minute.

[Audience]: "Can Alice add that output after the first transaction was signed already?
Or in other words, can we update the chain after we started it?"

I never thought about that.
What do you think?
So hang on a minute.
So, no?
because we're signing here(m_{34}).
What does this arrow(m_{34}) represent?
It represents a UTXO out of TX3 paying into TX4.
What kind of UTXO is that?
Promise UTXO.
It's a multi-sig on a specific TX ID, right?
So we couldn't like, unless you maybe SIGHASH Single or some dark arts that I don't understand, I don't think anyone ever used anyway.
No, basically I'd always envisioned this as frozen in time at the point where you finally, the distinguishing decision is to sign the transaction that pays into that (funding UTXO F).
Yeah, it has to be that way around.
Yeah, anyway that's the basic idea.

[Audience]: "So this is a chain of pre-signed transactions but just like with Lightning we can update."

Right, this is what I was saying at the start, is that Lightning is about, I whimsically called it vertical contracting as opposed to horizontal contracting, because Lightning updates and of course intrinsically updating is kind of stupid, right, because that doesn't guarantee the previous one doesn't exist anymore but the idea is there's a punishment mechanism or an L2 mechanism.
None of that here this is just flat; everything is signed up front and it's unlocked at the moment when you sign the funding UTXO.

[Audience]: "But if both parties collaborate honestly then they could."

Oh yeah! Of course that just goes without saying right, I mean, I'm just trying to design something that's safe from the other side cheating.
Obviously I've put two here, obviously it could be ten people as well, by the way.
This is designed for an N of N multi-sig thing.
So I don't mind spending time on this because after all I'm sure most people either haven't heard of this or didn't really look into it.
So if there are other questions about this structure, I don't mind.
I wanna like make it way more complicated.

Yeah, so how can I summarize it? if you don't want to get lost in the details.
I want to summarize it by saying everything's pre-signed and the reason it's all locked in is precisely because the transfer of funds is on a multi-sig controlled by all parties?
Otherwise it wouldn't be safe, right?

This is a very bare bones illustration, but for example in TX1 there's an extra payout to one of the parties.
So naively you look at it and think, well this isn't safe because Bob's getting a whole load of money before Alice got anything.
But that's why everything has to be frozen and locked at the start.
And by achieving that goal it means we can break the typical heuristics because it doesn't look right.
That looks like there's an actual payment there.

## The Kitchen Sink (extended idea)

(refer slide#10)

I call this the kitchen sink, so I'm extending this idea a bit, all right?
So green is multisig between the parties, here it's also only two, well it's only two in the multisig.
So here (1st node) we have both Alice and Carol funding the multisig initially.
But the idea is we could also embed two other types of event inside this network.
I'm showing it as a very bare bones straight line (almost linear structure of the whole graph), but imagine it could also branch off.
It works.
It's the same principle.
The first thing we embed is a PayJoin.
Okay, let me describe the scenario.
The scenario is Alice wants to make a simple payment to Bob, who is not around.
She wants to pay Bob 1 BTC.
And Carol wants to pay David 2 BTC, but he is around, he's online, and they agree to PayJoin it.
Because that's better for privacy, right?
So where's the PayJoin represented in the diagram?
It's represented by the 3rd node.
It's clear because there's a D there (David).
He's receiving 2.5, but he's also contributing 0.5 into that specific transaction.
What kind of UTXO is the 0.5 from David?
It's a promise UTXO (red arrow), that's right.
But What's the negative about a promise UTXO?
It's not part of a multi-sig, it's coming from outside of the tree, so to speak, or the line.
What's the danger?
Why is it red for danger?
Somebody could double-spend it and break the rest of the chain.
So what do we have to do to address that danger?

[Audience]: "Lock it somewhere in the chain."

Well David's just like gonna...
He's happy to accept a payment of 2 BTC from Carol, but he just wants to do a PayJoin with it, maybe he's got BTC pay server, he doesn't want to do all this rubbish, you know.
He doesn't care about the rest of the tree, what do we do?

[Audience]: "I mean with PayJoin you have a pre-signed single user transaction."

Yeah, but that wouldn't help stop the double spend problem we're talking about.
Remember it's delayed, right?

[Audience]: "But if it's a high fee?
He could double spend it with a high fee."

No, don't do that.
That's wrong, that's terrible.
Well, it's on the diagram.

### TimeLock to mitigate double spending

Timelock back out, right?
Like in the previous diagram, if you have a promise UTXO, you have to put some kind of back out before it to make sure that if the guy double spends it, then at the very least we can assure that the people involved in this CoinJoinXT structure are going to get back the money that they had to start with, they don't lose any money.
Now of course that's not quite good enough because would you go to all this trouble and then just have somebody just, that's annoying right?
Well you can address that with several ways.
For example here (2.5_D red line) it's kind of addressed by the fact he's receiving money.
Like he probably doesn't want to double spend that because this gives him 2 BTC.
So if he double spends it, he's not gonna get the 2 BTC.
So I think that's a pretty good incentive.
Other ways it could be incented is, if the promise UTXO is coming from one of the parties who funded, they could actually have a penalty in the timelock back out.
But I mean, maybe that's a detail.
What else is going on here apart from these two payments?

### Channel Splice

What's going on at the bottom (last node)?
I think this is the really important part.
This is the main thing I wanted to tell you actually.
So what's going on at the bottom is there's actually a channel splice.
Now I'm not sure if technically this is really possible, almost certainly not today.
But I think theoretically it makes sense.
If Alice and Carol agree to do this, they could splice in an amount at the end of this chain into a channel.
They could also open a dual funded channel.
It's the same thing, maybe one of them's more practical than the other.
Now why would we want to do this?
Imagine they've got this channel input here(0.04_{AC}), the new channel (0.09_{AC}), the now spliced-in channel has a larger capacity, and they also get their change outputs from the whole process starting from their original.
If you work out the numbers, that's how much they get back, yeah?
What might be the advantage, and this is a bit of a difficult question, but I'm sure somebody in the room could figure it out.
Why might it be really cool to put a splice into a channel at the end of this construction?
Why might that be valuable?
I mean we could just have, because in fact Carol is owed 1.4 BTC at this stage and Alice is owed 1.1 BTC, So they could just simply be paid 1.1 and 1.4 and everything would be normal.
They've made their payments, they've gone through this structure, but why might it be useful to add in a splice into a channel?

[Audience]: "It's like similar to a PayJoin, where you're hiding the amount each user receives."

Yeah, it's hiding, it's making, I'll just go straight to the point, because you're basically 100% correct, is that it breaks subset sum analysis, I want to put it like that.

## Subset Sum Analysis

### Overview

Now what's subset sum analysis?
It's the basic idea that in a transaction, if it's collaborative, if Alice is basically paying herself in the transaction and Bob is basically paying himself in the transaction, then you can kind of, like the shared coin thing, you can break, figure out these inputs add up to these outputs, these inputs add up to these outputs, and the whole thing ended up being more or less pointless, yeah?
At least from a privacy perspective.
Now, doing this, I mean, arguably the payjoin might have already screwed up a little bit, but that's more complicated.
But this is really clear.
So let me go on to the advantages in a minute.

### How to subset sum analyse?

Let's talk about the subset sum.
So that structure had four inputs.
What do I mean by inputs?
Any arrow that goes into a node in the diagram is considered an input, any outward arrow is considered output.
So there are six outputs.

If you wanted to do subset sum analysis, you're looking for subsets of the inputs and subsets of the outputs.
Now in mathematics that's called a power set.
It's basically the set of all subsets which ingeniously can be calculated by considering that each item is either in a subset or not in a subset, which means the number of subsets of `n` is `2^n - 1` if you don't include the empty set.
So `2^4 * 2^6 = 2^10`.
So you have about 1,000 possibilities, a little bit less, but about a thousand possibilities here.
And basically none of them work.

In other words, you can't find groups of the inputs add up to the same number as groups of the outputs.
By splicing a chunk of the money into a channel and dividing that money betweeen the two participants in a way that is hidden on chain, you no longer have a subset sum solution.

[Audience]: "This means you have to have either a PayJoin or a splice or both?"

I'll be more specific.
You have to have a payment from one of the participants to another one of the participants, but I'm not sure if that's enough, but that's definitely a necessary, I'm not sure if it's a sufficient condition to break subset sum analysis.
But it's funny because the Lightning Channel one is like a weird twist on that idea where it's not that there's a payment, it's just like that, there's a split in one of the UTXOs which isn't exposed.
I guess that's a fundamentally different thing to a payment interparticipant.
But if you have, PayJoin has interparticipant payment, which is why, as you said correctly and I incorrectly corrected you yesterday, a PayJoin does break subset sum.
A PayJoin does break it because it's an inter-participant payment.
The same principle will definitely apply, but also a lightning channel can do the same thing because it's splitting funds without it being exposed on-chain.

[Audience]: "And so is there a qualitative difference between there's one inter-participatory payment versus two?"

Yeah, I was thinking about this the last couple of days.
I haven't really figured it out yet.
I think that's a really interesting question, like could we get 10 people operating in this kind of structure, and just have two of them paying each other, and everyone else's stuff, subsets.
I think trivially no, right, because let's say you've got A, B, C, D, right, and A's paying himself, and B's paying himself, now C is paying D, so A and B, clearly their amounts will add up, right, so you won't have broken subsets on for A and B.
It seems trivially that that's not.
I think there's a lot of little twists on this.

[Audience]: "So the knapsack paper gives the sub-transaction model, the sub-transaction mapping model.
And in there, they assume the sub-transactions map to zero.
They don't model fees.
If you generalize this and parametrize it by some delta, they make a tolerance.
Yeah, they make a useful distinction between derived sub-transaction mappings and non-derived sub-transaction mappings.
So we can think of the non-derived ones as elementary.
They're actually finer grained, whereas the coarser grained ones don't add additional information."

Oh you mean like building multiple into a bigger one.

[Audience]: "The trivial partition of everything together is always a valid solution.
And then the question is, so qualitatively, are you breaking the assumption that a single sub-transaction belongs to a single user?
That's one aspect of it.
And you can still divide into sub-transactions, it's just that the set of users that that sub-transaction is attributed to is more than one entity.
And secondly, there's the question of the tolerance of the amount.
So both the fees complicate this a little bit, but specifically the PayJoin aspect or any sort of internal transfer within the transaction means that the adversary must have additional information?"

Exactly! That's my point of confusion with PayJoin is if you're looking at it thinking Oh that might be a PayJoin then you come up with two solutions.
But if you have no idea you just look there's no solution.

[Audience]: "Yeah and even if you have a solution the solution might attribute that part of the solution to two entities or more, right?
So you have this, I think that's the important qualitative distinction."

Okay, thanks.
So clearly this is quite a thorny and very interesting topic.
I don't want to say it's like, oh, it's too complicated.
It's actually really interesting to start thinking about this.

## Advantages

But I do want to come back and talk about, why Am I even proposing such a weird design as that?
Well, I guess I should ask you.
I mean, maybe you just saw my slides, but what do you think might be the advantage?
All this, it seems like a lot of hassle, right?
Well, certainly in this way, it is a lot of hassle.
There's multiple things going on.
There's four people involved.
One of them's not around, but two of them are having to negotiate a bunch of multi-sig addresses.
Can anybody explain to me why this might be an interesting model?
It's nice to have the diagram (Kitchen Sink) for this part, isn't it?
Like if we look, for example, at transaction at node 3, well, what does it have?
It has two inputs and two outputs.
That's not very unusual, right?
That is, in fact, almost the most common structure, yeah?
Anything between one and three, maybe four inputs and two outputs.
Vast majority of transactions are like that because that's what a payment looks like.
So that's nice.
Now obviously most of them have that kind of structure, but they're not all exactly the same.
Like this one (node 5) has three outputs, which is a little unusual, but it's not very unusual.
So it's a world of difference from what we're thinking about equal output CoinJoin, whether it be JoinMarket, Wasabi, or Samurai, or anything else.
That's the first point.
What are the other possible advantages to this structure?

[Audience]: "You don't even know when the tree starts or stops."

Excellent, yeah.
Excuse me for the low quality here, but this was Like the picture (Transaction graph) I used to illustrate the start of my blog post about this topic.
This is a bit more advanced than the blog, but you know, it's the same thing.
So you know, there's some things happening in a bunch of transactions that are connected, but they're just part of this huge transaction graph on the blockchain.
How is the blockchain analyst gonna know where to start?
It's a huge, it's a completely different world from equal output CoinJoin.
So that's probably the biggest advantage.

So, every transaction could be possibly interpreted as an ordinary spend, with the caveat that since many of these inputs are multi-sig, We need them to be not traditional multi-sig, not `OP_CHECKSIGADD` in taproot, but specifically musig style multi-sig, or at least aggregated multi-sig.
So that's kind of a big limitation, but it's possible today.
The transaction negotiation can happen right at the start.
Now that is not an advantage over equal output CoinJoin.
A CoinJoin traditionally involves a bunch of negotiation, signing and broadcast, right?
Coinswaps and other Steganographic solutions that are similar to CoinSwap often involve what I call cross-block interactivity.
Because you have to fund, and only when you're sure the funding event has occurred correctly can you then complete the protocol to complete a private CoinSwap.
That's not really true with like a general atomic swap construct, may be debatable.
But you know, a proper private CoinSwap, it's kind of a cross-block interactivity you have to worry about, is that embedded deep enough in the chain, because if it's not and it gets re-org'd, then theoretically I can lose some money in a CoinSwap.
But this has the property, even though it's very complicated, there's a lot of signatures, a lot of keys, you can do all of it at one shot, and once you're finished, you never have to talk to your counterparty again.
Because if they go offline, you've got all the pre-signed transactions.
Maybe that's not, I didn't really have enough time.
Musig2 is required, or musig anyway, or theoretically ECDSA with two-party computation (ECDSA-2P).
Anything that hides, to me it's important to hide the fact that they're the multi-sig connectors between each of these transactions, otherwise they don't look like ordinary spends.
And the last point is the point that we just said, the subgraph is not distinguishable.

## How subset sum analysis can fail?

(refer slide#14)

Okay, we talked about subset sum analysis.
I'd also like to point out that subset sum analysis can fail in three ways, maybe.
There are multiple subset sum solutions, we discussed this a little bit.
Sometimes, especially with larger transactions, not so much here, but with larger transactions, there might be multiple different subsets that add up to the same value on the other side.
That's a brittle thing, and I think nothing much explained in great detail yesterday why it's brittle, we shouldn't rely on that, but it exists.
The analyst cannot find the subgraph, that's the fantastic thing about this construct.
There is an inter-participant payment, such as in PayJoin, that can break subset sum as well.
I guess I should have added the lightning as a separate one because it's not really the same thing as an inter-participant payment.
In fact, it's just not.
So there's a fourth one on that list, which is lightning or, I guess, any second layer commitment of funds.
Arguably, the second is the most important (The analyst cannot find the subgraph).
I think that's true.

## Disadvantages

All right.
Some practical disadvantages of doing that.

### All at once? Timelocks but ...

First of all, you're gonna have to time lock.
I'm claiming that when we look at this sequence of transactions that we pre-sign, we're gonna have to put timelocks on them.
Why do we have to put timelocks on them?
In other words, delay them.

Why should we delay the transactions?
Because if not, if it's like 10 of them, and they all go on-chain at once, then at least theoretically, somebody who's watching is gonna say, oh look, that's, well, in the future as well, not just at the time.
So, you know, timing correlation, it would be a bit crappy if we just broadcast them all at once.
You could do that in an initial phase, just testing the idea out, but I think if you want a properly mature system using that, you're gonna have to have delays.
That's not very practical, is it?
An associated problem is, that means you're gonna have to hold those pre-signed transactions and not lose them.
Because if you lose them, you could lose money.
So you're gonna have to treat those pre-signed transactions as like private keys.
Well, not private keys, but you treat them as importantly as money that, it represents money for you.
So I claim that because of that, it might mean we do kinda need to make a model, or at least some incentive model to get people to take part because I'm not just going to arbitrarily help you out to do one of those things and it takes me like six hours and I've got to hang on to and I've got to sign all this.
Pay me some money please, yeah.
So I think we do probably do need a market model at least a little bit for that to work.

[Audience]: "Sorry, aren't the timelocks a fingerprint as well?"

Good question, but I think not because we're going to join the anonymity set of Electrum and Core and other wallets like JoinMarket who put the most recent block or the most recent block minus three or whatever it is, you know.

[Audience]: "So we would just have to broadcast the transaction as soon as the time block expires.
If we wait a long time..."

Yeah, it would be a little bit bad, a little bit late, but I mean that's not gonna be a big deal.
You're gonna have to stay online, right, to broadcast them at those times.
Well yeah, that's a fair point, that they could end up being a little bit delayed and therefore theoretically they look weird.
Fair point, Yeah, depending on if you're online or not.

### Offchain onchain privacy bleed is cool but ...

Off-chain, on-chain privacy bleed is cool.
Do people follow what I'm talking about there?
That was a bit of a weird phrase I used there.
So I was saying, remember at the end of the process, we spliced in some money into a channel in order to break subset sum?
That's cool, that's off-chain to on-chain privacy bleed is what I call it, right?
Because the privacy embedded in committing money into the channel gets bled through into the on-chain because the subset sum gets broken.
It's cool, But it doesn't really work if the amount of money you put off chain is .0001 BTC, and the amount of money you're putting on-chain is 10 BTC.
Because that is just a tiny delta in the subset sum analysis.
Nothing much, just mention tolerance.
You can put a little delta value in your subset sum and get more solutions.
And obviously it's gonna come out.
So I'm thinking like, I don't know, top of my head like 10%, maybe if the off-chain is like 10% of the on-chain, it's okay.
Maybe if the off-chain is only like 1%, maybe it's not okay.

[Audience]: "Do you have to include the eventual?"

Ah, good question, good question.
I remember thinking about this, yeah.
Let's go back to the slide (Kitchen Sink) so we can explain it.
So we had, remember, a splice in node 5.
I mean, even better with splice, but let's say it was funding a channel, dual funding a channel, you know, and Alice put in .02 and Carol put in .03, and then a month later, they close the channel and it's 0.
Well, but the nice thing is even if they do that, we don't know for sure that they didn't have payments going through the channel in the meantime.
So I think the worst case would be, you put the money into a Lightning channel, then you immediately remove it, then it's kind of stupid because you can just assume that they didn't have any payments in the meantime routed through it or payments they made.
Yeah, so but in the general case, you can reasonably say that as long as that channel is long living, we could plausibly assume some amount of TXs went through it.
But very good question, I had the same question myself.

## Markets and Fees

So now, I know we're all hungry, and probably tired as well.
Yeah, and that's why I'm now gonna give you a really dense piece of mathematics.
[laughs]
So in order to have this, I mentioned I think we need a market for this because there's delays and so we have a coordination issue because people don't really want to do it.
Well today we have kind of liquidity markets.
I can't remember when I found these years ago (referring to slide#16).
The [JoinMarket orderbook](https://nixbitcoin.org/orderbook/) is a market.
You know, this is some lightning terminal thing, whatever.
There are liquidity markets, there's liquidity ads, there's all these markets, right?
So we're used to the idea that we can like advertise to request liquidity and offer a payment for that service of liquidity.

### Onchain fees

#### The problem

(refer slide#17)

The problem here is, as I mentioned, on-chain fees and CoinJoin in JoinMarket are a real problem.
So like you do a simple CoinJoin on JoinMarket, you're exposing almost certainly your input value because you're paying a fee to the makers and that fee is deducted.
When you look at the subset sum analysis, you're trying, oh, that's the input size, that's the output size, the difference is the fee.
Oh, he obviously paid a fee.
So unfortunately, a single CoinJoin in JoinMarket doesn't give you what you would really want.
What you would really want is that the receiver of the funds doesn't know where they came from, right?
Or at least that's one thing you would want.
You don't really get that, because this is on-chain fee thing.
So we want this fee to be off-chain, but that's a bit tricky.
And I'm gonna propose a way to solve that problem, make the fee be off-chain so nobody sees it.
I suppose you could either take that approach that some people take of making everyone contribute equally to the mining fee, or you could embed it in this as well.
I think both make sense, don't they?
Let's say it includes mining fee, just for simplicity, all right?
Because it's just another number to add into the fee at the end of the day.
I mean, I know there's different ways of doing it.

#### The solution? - offchain fees

(refer slide#18)

So crudely, my proposed solution is this.
So if you don't understand all the mathematics, maybe you can understand the basic flow.
There's a construct called a hodl invoice, maybe it's a stupid name, but the general idea is like the sender constructs the payment hash, and then the receiver constructs, or They construct the invoice such that when, like the example given is pizza delivery, right?
So when you deliver the pizza, or the merchant delivers the pizza, they can request the pre-image from the payer to unlock the invoice.
So there's more of like an atomicity between the sender receiving the goods for the payment and the payment actually being enacted.
So you kind of set up the route.
You set up the HTLCs and everything, but they don't get unlocked until that moment when the sender reveals the preimage.
So the idea here is that the taker sends, let's say, an elliptic curve point.
Now, this requires PTLC.
So bad news.
This particular part of my presentation requires something that doesn't exist yet, unlike musig2, which theoretically does.
But this requires PTLC, because you have to pay to a point, right?
And then you set up the HTLCs.
When the maker does what is required of him, which is to say sends all the signatures and all the transactions and the multi-sigs that I've just shown you, then the taker will broadcast the transactions, thus revealing his signature, and the trick of it is that his revealing signature will be able to be matched up with the adaptor signature or signature adaptor that the taker produced originally on his partial Schnorr signature in the multi-sig.
And so what that results in is that the maker receives the pre-image for the invoice atomically with the broadcast of the funding transaction.
I'm gonna expand on that because when I first came up with this idea, I thought, well, that's cool, and then I realized there's actually a really big problem with it.

[Audience]: "If you don't have, PTLCs on Lightning Network, couldn't you just do a PTLC on-chain?"

I don't know what you mean.

[Audience]: "Like if you just do a point time lock contract literally on a non-chain payment."

We were trying to create off-chain fees to avoid having a fingerprint on-chain.
The fundamental goal here is an off-chain fee.
Okay, but other than that, your idea is excellent.
It just doesn't actually solve the problem I'm trying to solve.
It solves another problem.
But a good point though.

#### Why the solution doesn't work

(refer slide#19)

So let me first explain why it doesn't work.
What I've just said doesn't actually work.
And the reason it doesn't work is because we have more than one maker.
If we had only one maker, it would work fine.
This works fine in a two-party sense.
You could imagine each maker setting up the invoice to an elliptic curve point Q plus some offset that they choose and then the taker will send the adaptor signature, and I don't really have time to explain adaptor signatures I'm sure a lot of people have heard of it and a lot of people don't really understand it because it's not something that people talk about much.
But the basic idea is you can swap a signature for a secret value.
If I can boil it down to one thing, it's that.
You can swap a signature for a secret value.
So the taker sends this adaptor signature, which is verifiably corresponding to their funding transaction multisig.
And once the maker sees that, he knows that when the signature is broadcast on-chain, he'll be able to subtract his partial signature in the multi-sig and subtract the adaptor signature he was sent and get the corresponding secret Q.
So I'm not gonna explain all the notation here, because I haven't got time.
`Tilde(~)` means aggregated value.
`sigma_t` means taker.
`x` is the private key.
So this is like a Schnorr signature, but with part of the nonce missing.

The part that's missing is the Q.
So basically, he gets the secret value Q once the transaction is broadcast on-chain.
So it's atomic, it's trustless.

Now why doesn't that work?
Well, it does work if there's only one maker.
Yeah, he uses Q to settle the Lightning invoice.
If there's multiple makers, it doesn't work because what's broadcast on-chain is the total signature sigma.
If you have three people making a musig, they're gonna have three partial signatures.
So each maker's gonna see the total.
Well, I did this the wrong way around.
He's not gonna be able to subtract his partial signature and the other maker's partial signature to get the taker's partial signature unless the other maker cooperates with him, which is certainly possible, but it's not something you can depend on, because the other maker could be colluding with the taker.
So fundamentally, it doesn't work, but it does because I figured it out.
Because I actually wrote a blog post years ago, just completely off the top of my head, I thought, I had no idea, it didn't seem remotely practical, but I thought you can kind of do this adaptor signature trick with multiple people at the same time.

#### A working solution

(refer slide#21)

Imagine two makers, we're gonna make a musig, three of three musig, we have an aggregated P, `P_{agg}`, we each have our own nonce, we use three round musig and not musig2, because it's a bit simpler to analyze in this case, but I think it would work the other way as well.
Three-round musig, we're gonna send commitments to our nonce values in the first round.
We're also gonna send commitments to our adaptor secret values.
So the trick here is everyone has their own adaptor secret, not just one person.
We're going to send commitments to the adaptor values: adaptor secret points `Q_i`, and the nonces `R_i`.
Then they get revealed.
Then we find the aggregated nonce.
We've got the aggregated nonce, the aggregated key, and the trick is that let's say if you're index two, you make your Lightning Invoice payment hash, which is actually a point, payment point, be the sum of the adaptor points of the other two parties.
And if you're index three, if you're the other maker at index three, you'll make your payment point for your Lightning invoice be the sum of the adaptor points of the other two people.
So what I realized is that you can't make this take and make a distinction in this construction, actually, because everyone could be colluding against you.
You have to make it so that you use basically everyone else apart from you as your counterparty.
And linearity makes that work.

(refer slide#22)

So each party makes their own adaptor.
So everyone has to send an adaptor to everyone else, which is corresponding to their own adaptor secret `Q_i`.
And they all share those around.
And adaptors are verifiable.
So each person can verify that the adaptor signatures from all the other parties are correct.
When everyone's satisfied, any one person in the group can send their partial signature first.
So if index three sends his partial signature first, it looks like that: `σ_3 = k_3 + q_3 + H(P_{agg} ||R + Q_1 + Q_2 + Q_3 ||m)x_{agg,3}`.
Notice it refers to all of the adaptors, but he only includes his own secret there.
And then, I guess you'll just have to trust me, because it would be way too complicated to explain.
But basically, any person will be able to subtract their own full partial signature, which is to say their partial signature, which is not including an adaptor, and then subtract the adaptor signatures from the other parties.
And the result will be the sum of the adaptor secrets, which are not theirs.
And that's what they already decided was the pre-image for their Lightning invoice.
Should I really have done a presentation about this?

[Audience]: "It's kind of cool because you're sort of changing into two-party, I mean, it's still a multi-party, right?
But it's sort of changing the math and stuff so there's a two-party thing, right?

Yeah, I remember when I had this idea, I ran it by Andrew Poelstra on IRC, and he was like, yeah, that's really cool.
And I realized that this is unfairly linear signatures for the win, you know?
It's the linearity that makes it work, because without that linearity you couldn't do that.
But you're exactly right, it pretends that everyone else is one counterparty by adding them all up.

The only caveat I'll say is, when you do stuff like this in cryptography, you have to be really careful, because the thing is, what happens if somebody tries to adversarially create their adaptor point?
I should try and write a paper about it or something because I believe if you, just like in three round musig, what they do is they commit to all the `R` points up front, and that allows them to then just simply use the linearity and add them without worrying that the other party has subtracted something weird and like, you know.
But I think the same thing would apply with these adaptor secrets.
If you just send hashes to them up front, there's no possible way somebody could manipulate their `Q` values to screw you over.
I believe that's right.
I hate that that's on a video, because if I'm wrong I'm going to look like an idiot.
[Audience]: [Inaudible]
This being three round, I think, is not problematic at all, because we're already gonna have multiple rounds of sharing keys and sharing signatures on transactions.
Whereas, you know, why does musig2 exist?
It was a huge feat of engineering, but it existed because they had specific use cases in mind where boiling it down to two or even only one round of interaction was actually very important, such as certain hardware wallet scenarios.
But if you don't care about that, like I don't, I'm just like right now, I'm writing three-round musig in Python, and it's easy, right?
Because it's not that complicated.
I mean, you just have to make sure you aggregate the keys properly, because you have key subtraction attacks both on the keys and on the nonces, so you have to be careful about that.

[Audience]: "What if two of the makers collaborate?"

The fact that if you commit to the inputs to the adaptor up front, which is to say the adaptor point and the nonce, then it's impossible for you to manipulate those values based on the other person's values.
So you're thinking, if the two makers' `Q` values were somehow manipulated.
Yeah, it's possible, that's why I really... I'm not quite sure, I'll have to think about that.
I'll think about that one, that's an interesting point.
I don't know, I don't think there's an issue there, but I couldn't tell you for sure.
I'm not sure what you would, anyway, let's not get into that now, because I don't have an answer.

## SDMC - the sales pitch

(refere slide#24)

So sales, let me just summarize what I'm saying here.
Sales pitch, because you know, I'm a terrible salesman, and I admit it, but sometimes you want to sell something a little bit.
A market solution to coordination; I think most people in this room at least sort of agree that that is like the right way to solve coordination, yeah?
Obviously you can use central coordinators.
Obviously there's advantages, but markets are cool.

No on-chain footprint; that refers to this PTLC construction, which unfortunately we can't do today, and anyway, how practical is it, you know, setting up this lighting invoice in advance?
I mean, you know, lighting payments fail, So I don't exactly know what we do about that.
Any ideas?
I mean, we atomically set up this invoice and then you try and pay it and then...

[Audience]: "The failure would be before the route reaches the receiver.
And the HODL invoice only goes into effect when the receiver receives the route."

Oh yeah, you've already set it up.
That's true.
If you weren't able to route it to start with, then it wouldn't.
Yeah, I am completely clueless about this stuff, but I know that things like hodl invoices are a bit of a problem in Lightning, right?
Because you're locking things up, and there's a question of how, but that closely ties into my other area of interest, which is how do we allow people to get paid appropriately for the actual resources being used, which includes time and not just money, right?
So I think that's a whole other discussion, but a good point, I wasn't thinking clearly, there's not really an issue with the routing thing because you've already done it.
We could still fail though, right?
We could still fail, I mean, after the event.
There's a timeout, yeah, that's another thing.
So, I mean, certainly this whole idea of the off-chain payment of fees is, I won't say, it's partly speculative, but I think it kind of makes sense, at least in broad outline.

The steganographic, I hope by now everyone understands what we're talking about, a lot of these things look like payments, and you can't distinguish the whole set on the blockchain.
It's maybe a sci-fi, but if people actually start using stuff like this, chain analysis would be really, really hard.
Another element, you've got like 10 transactions in a list, but what if they're all like Electrum style transactions?
You know, what if they're all using the same wallet fingerprints?
So I think part of it should be randomized wallet fingerprints, because you don't want them all to have anything about them that look the same, otherwise, I mean It'll still be hard for them, but they might be able to figure out.

And last one is just a minor thing, is just the fact that you can do the whole negotiation right at the start, which I think is a very important property.
That's my sales pitch for SDMC, which is a thing.

## Q&A

Yeah, maybe questions now.
I'll stop there.

[Audience]: I was just curious, sorry if we already covered this, but is there a way to lock the makers into a fee rate?
Is that designed?

[Adam Gibson]: You mean the Bitcoin network fee rate?

[Audience]: Yeah, I was just imagining, like, if I'm a maker, I could, like, publish the transaction that allows me to get the pre-image, but at a really low fee so it never gets mined.

[Adam Gibson]: The transaction that allows you to get the pre-image is the funding transaction which is a multi-sig so both parties are signing off on that.

[Audience]: And the taker publishes it, right?

[Adam Gibson]: Anyone can publish it, it's a multi-sig so whoever finishes first, I mean whoever wants it to go.
Let's say all the transactions after the funding get signed in advance, and they're all based on a multi-sig, once all of those are signed in advance, that means everyone's agreed, and so they both co-sign the funding transaction which kicks it off.
I've forgotten the question now.

[Audience]: Oh, I was just talking about fee rates.
It sounds like what you're saying is that they're only signing it once they see the fee rates.
There's no concern like that.

[Adam Gibson]: Well, they'd have to agree on the fee rates to sign it, I think is what I'm saying.

[Audience]: What happens if the fee rate changes between when you've signed, pre-signed all the transactions?

[Adam Gibson]: Yeah, now that's a good question.
Somebody asked that back in the day about CoinJoinXT.
They said, what about fee rates?
There's pre-signing multiple versions, which is not unreasonable, although I...
Ugh, that's a lot of data, but I don't think it will be that hard, maybe.
Depends where you're talking, I suppose.
Multiple fee rates is one reasonable solution if you can't come up with a better one.
Can anyone come up with a better one?
So we pre-sign all these transactions, and then suddenly the mempool just spikes.

[Audience]: Child pays for parent, presumably in another coin...

[Adam Gibson]: Yeah, we could do that, right.
Especially if it was just like a one line thing.
It would be particularly easy, just the last one.

Now I think that's an important practical point which I kind of glossed over, but I don't think it should stop it from working.
But it does connect to another point, which is this whole thing about timing.
Will people be comfortable with doing these kind of structures that take hours?
Now, I showed a kind of a paradise version where everything's perfect and somebody gets to do a PayJoin, somebody gets to splice into a channel, somebody gets a payment.
Bob might have to wait six hours for that payment, because I don't want to broadcast all those transactions right at once, so are we really gonna have external payments in those structures?
Maybe not, maybe mostly it'll be more like what CoinJoin is today, where a lot of people are getting together and maybe there's a market, some people get paid a fee.
That's why I was really keen on the idea of designing an off-chain fee element to it.
In theory you could apply that same idea to JoinMarket, it's just unfortunate we don't have PTLCs yet.
They're very powerful and this is a very good example to me of why they're powerful.
People talk about breaking the correlation in the route which is great and everything.
But this, you can swap signatures for secrets, it's really powerful.

[Audience]: And contrarily to single transaction CoinJoin there's a backup problem as well.

[Adam Gibson]: Well yeah One of the disadvantages we listed was you have to treat these pre-signed transactions as well as money.
Not necessarily as secrets.
But that's the other thing.
They're not secret even though they are money.
So you could have like a watchtower kind of design.
Now, there wouldn't literally be a watchtower because it's not watching, it's just somebody could be doing that job on your behalf if you could trust them with your privacy.
But other than that, I mean at the end of the day storing some transactions isn't that much harder than storing some private keys and it's only very temporary.
So it's definitely a problem but it's not I think a great...

[Audience]: There's just no hierarchical deterministic way of backing it up contrarily with keys, right?

[Adam Gibson]: True, yeah, good point, yeah.
That's worse than keys for sure, yeah
It's more difficult, you do have to store that data, but only for a short period, to be fair.

[Audience]: Did you compare the block size, block space?

[Adam Gibson]: Oh, thank you for mentioning that because I forgot to mention it.
I think one of the other advantages of this construction is that I think, now this is a really tricky point.
We talked both yesterday and today about k-anonymity, the idea of measuring anonymity quantitatively, saying there's this number of people who have the same role or action in this event and therefore there's a K anonymity of 10 or 100 or something.
It doesn't apply, in my opinion, at least not in any way that I understand, to a steganographic style of privacy preserving technology.
I mean, you could argue with like a CoinSwap, at least the naive form of CoinSwap involves equal amounts.
So even if the transactions are disconnected, they have a fingerprint that tells you that they're connected somehow, and therefore you can start saying there's N people doing these swaps.
But here, you don't have any idea.
If the blockchain analyst can't even find it, and then if somehow he finds certain parts of it, how does he decide how many people are involved?
It's tricky, I'm sure there are certain cases you could show of this kind of structure where actually the privacy isn't that good but I think generally speaking I could argue that in the limit it has the anonymity set of the entire blockchain.
In the limit because it's trying to behave exactly like the rest of the blockchain.
But that's only in the limit, that's not in reality.
Why did I say that?
You actually asked a slightly different question but I thought it was connected.
You said...

[Audience]: My other question would have been how to quantify privacy which you answered but the other question is how does it compare block space wise?

[Adam Gibson]: Yeah, efficiency of block space.
Do you see why I think it's connected right?
Because if you need a quantitative measure like 100, you need to have a lot of people, well debatable.
I know you've got a lot of very sophisticated ideas about efficiency within your construction of block space usage.
But in principle, this might apply to CoinSwap, but I think it certainly applies to this construction.
But I would argue it's very efficient in block space, because you get a quality of anonymity which is difficult to measure, but which arguably is much higher for per unit of transaction.
It's difficult to compare.

[Adam Gibson]: I'm just gonna pretend the anonymity set is the whole blockchain and somebody's gonna have to tell me why it isn't.

[Audience]: Yeah, so like in this case the anonymity set would be potentially huge, like whatever time window of value-compatible transactions.
But then there's three very difficult open questions.
Okay, so this model assumes the adversary can assign a probability for guessing, and what probability it assigns is debatable.
Tacitly, this perspective assumes that the adversary is truth-seeking and rational, which might not be the case.
We have very good evidence to believe that chain analytics companies are in the profit of selling narratives. And finally, there's no answer for the entropic model, at least as in the paper that I was referencing, assumes a single point of origin.
And even that is prohibitively expensive to actually calculate in most situations.
We don't need to calculate it.
We really want lower bounds on the entropy.
That's good enough.
But nonetheless, the entropy that you would have to calculate for this is like a joint entropy over the power set of all potential points of origin, and that's an exponentially sized object.
It's very difficult questions.

[Adam Gibson]: Yeah, which is great, right?
It's so difficult.
That's great.
Well, I agree.
It would be nice if we could have a really clean model that said there's a specific lower bound of entropy or some even simpler model of k-anonymity set.
All I'm trying to do in this is trying to expand what I think is already trivially existent, which I think Max mentioned earlier this morning.
Bitcoin is intrinsically fungible, it's just not very fungible at all in practice.
It's really, really difficult to get any real practical fungibility, but intrinsically it's completely fungible.
So this is trying to expand on the real intrinsic nature.

[Audience]: One thing that I think is kind of cool about this sort of thing, and this is like sort of maybe more of a social commentary than anything like necessarily technical.
I think CoinJoin in general are like this idea where Bitcoiners have to come together, so like you have to work together as a team to like keep your privacy, which is kind of cool.
This it seems like is a little more, your teams can be like a little smaller size, so to speak, than in larger CoinJoin.

[Adam Gibson]: That's a good point I didn't really mention.
I showed these examples with two people just because it's easier to draw the diagram.
You can do this with 10.
I was talking, I think, to NoPara the other week about what happened if we try to do Wasabi with more people using a CoinJoinXT structure.
And one of the things that I wrote in my response to him, and he agreed with me, was this is so fragile though.
If you try to do 100 people with this kind of structure, well yeah, sure we've got back out, so we're definitely gonna hit the back out path, right?
Because one person out of 100 is gonna screw something up before you, well that's if you use promise.
I suppose you could argue that, anyway it's a complicated question.
The point is that with largest numbers of people, let's say 100 people, right?
We're gonna pre-sign all these transactions, and then we're gonna have 100 of 100 multisig starting the whole thing off, right?
Obviously, the most likely thing is that somebody's gonna fail to respond somewhere during this signing process and the whole thing doesn't even start.
We've just lost time.
But the real question is this (pointing to the red promise arrow on the kitchen sink slide), right?
If you use a structure with a realistic chance of something going wrong, like a promise you take, or like a malicious adversary is just like wants to jam the process.
If they're there, they're gonna block everything that comes after that promise, and everyone else is gonna have to fall back to the timelock, so I feel like very large sets of people can do this fine, but it's more limited.
Because without these alternative inputs, this structure is less kind of impressive, I feel like.
Because if it only has one entry point, it's more plausible to me, intuitively, that there'll be ways to identify it as such.
Maybe that's just a bit too vague.
But I agree with your original point, which is we can do this with smaller groups of people and get a real effect, which is what I had in my mind, like three, four people.

[Audience]: What's the privacy punishment for the fallback timelocked?

[Adam Gibson]: Yeah, good question.
That's a good question.
How much do we lose in terms of the fallback?
It seems to me debatable.
Thinking about only small groups, it makes it a bit kind of easy, right?
Because then this might have like two or three outputs and then it wouldn't look strange so we could just dump everything out in one transaction.
We could theoretically make the timelocks themselves be trees if we need to make them less, but that's kind of annoying, so probably wouldn't do that.
So I think that's a good example where if you had a lot of people it might be worse, because if you want the timelock to be one payout for everyone, it will look very, very distinct.
That's a good point which I hadn't thought about, yeah.
There's definitely trade-offs with using large numbers of people with this, which in practice you would probably avoid by using small groups, I think.

[Audience]: So If the adversary knows that a certain tree is a CoinJoinXT, then the anonymity set is just the fresh Bitcoin that entered the tree in that time period?

[Adam Gibson]: The anonymity set of what though?
One specific output?
It's really slippery isn't it?
But it's a good point to consider, we should definitely consider that, but I think it's.

[Audience]: Like the point I'm trying to make is that if the adversary doesn't know that this is CoinJoinXT, yes, the anonymity set is huge.
But just like with PayJoin, right?
But if he does know this is CoinJoinXT, then it seems it decreases the anonymity sets.

[Adam Gibson]: Well, it must, by definition.
He knows more information, right?
I'm not sure how easy to quantify it but should therefore be a fairly tractable problem.
At least it would reduce it more to existing blockchain analysis on more normal flows I guess which may or may not be easy depending on the structure.
I mean, this is a very simple structure.
I think we can make, well, we can make lots of structures.

[Audience]: Is there an optimal structure?

[Adam Gibson]: I think I'm a bit too lazy to actually try and do this analysis.
Because that kind of analysis is hard.
I don't know, I prefer thinking about long equations with sigmas in them.
I don't like that kind of, yeah, it's hard.