---
title: What is Lightning Network?
transcript_by: masud-abdulkadir via review.btctranscripts.com
media: https://www.youtube.com/watch?v=ZxrXkprwxUM
tags:
  - lightning
speakers:
  - Adam Gibson
date: 2021-12-15
---
## Introduction

Hello everyone.
We're going to sort of soft start now, and this is a new meetup group we've decided to call Bitcoinology.
It's a whimsical name.
It's really intended to convey the idea that we want to discuss Bitcoin not in a super developer technical code way, but we do want to discuss it—how it's used, even what the history and culture of it are, and what are the interesting things as a user and as a sort of Bitcoin person you can learn.
I don't know whether Bitcoinology conveys it properly.
It's intended to be sort of halfway between serious academic stuff on the one hand and, on the other hand, just culture and just enjoyment stuff.
This is the first—it's a test meetup.
We're just seeing how it will go.
We decided that a good topic would be the usage of Lightning, or Lightning Network, as a sort of second layer of Bitcoin.
I'm going to go through what I'm going to do in this talk.
It's basically going to have two halves to this session.
The first half is me giving a talk, a traditional presentation.
You can interrupt with questions if you like that's fine.
If you do, I will have to repeat them—a reminder to myself.
I'm going to explain some of the history behind the Lightning Network and where it came from.
Because if you only know a little bit about Bitcoin and we just established it with a hands-up, most people here know quite a bit about Bitcoin, but some people may be watching or some people in this room right now may don't know that much about it, and they may know even less about Lightning.
I want to give the context, where it comes from, and why it's useful today, and hopefully that will lead into what it's really like to use the Lightning Network today as a payment system, and we're actually going to do that in practice in the second hour.

Let me kick off by, first of all, going to the start of this presentation.
I've called it Lightning Network Make Bitcoin Fun Again, and I hope you'll understand, apart from just the trivial sense, why I say that as we go through the first section.
Part one is how we got here.
This is about the history leading up to the Lightning Network.
By the way, on this first slide, you're not going to be able to see everything perfectly, but I'll try and point out the things you do need to be able to see.
This slide is, I think, interesting.
On the left, you have an Archive.is snapshot of bitcoin.org, which was the place you used to go to always to get your Bitcoin software, and the front page of it was actually a video, which of course doesn't show up on Archive.is now, but it also had these little call-out sections you see on the right: "instant peer-to-peer transactions," "zero or low processing fees." And this was on the Bitcoin.org website as far back as 2012, I'm sure, maybe even earlier, and as late as 2014, they were still saying that, and even later.
And I've written here, "very unwise." Even at the time, myself and I'm sure quite a few other people thought it was quite dubious to be advertising Bitcoin as specifically an instant transaction system and specifically as a zero processing fee transaction system.
And why was it dubious?
Because of its nature, without going into the technical details, Bitcoin is not instant.
It cannot be instant to transfer bitcoin.
In terms of zero processing fees or very low processing fees, that was very true in the very early days of Bitcoin, but even though it was true, everyone knew inevitably that to whatever extent Bitcoin was successful, it inevitably meant that fees would not be zero, and moreover, not only are they not zero nowadays, but they are quite unpredictable, which is maybe even more important than that they're not zero.
This was unfortunate, but it reflected a very strong sort of cultural tendency, if you could call it a culture, in the early days of Bitcoin to think of it as a potential replacement for our normal consumer payment system.
People often talk about cash and digital cash, but what I think a lot of people had in their minds around that time, 2012, 13, 14, is they had in their mind, "Oh, I'm going to go to my local bar, my local pub, and I'm going to infuse them; they're going to accept Bitcoin; they'll be, you know, people made these videos of QR code, exactly what we're going to do today, but they did this eight years ago or whatever," and they were, "Oh, look, the bar is; there was a pub somewhere in London or somewhere in England anyway, accepting Bitcoin this," and it was all, to use the language of the kids nowadays, it was all a bit cringe.
It was a bit cringeworthy because, to me anyway, that's not how it's actually going to work, and why do I say that?
Because I always called it, well, Bitcoin is SWIFT, not Starbucks points.
What I meant by that, if you don't know SWIFT, is that SWIFT is international wire transfers.
It's a very heavy, very serious way of transferring money, but it works all around the world.
It was originally tended to be very apolitical, and you can think of Bitcoin like that or like hard currency in the old Soviet Union.
You can't really think of it as a replacement for Visa because it just doesn't scale to that.
It doesn't have the right privacy properties.
It doesn't have the right consumer experience.
That's why I and quite a few other people were quite negative about this viewpoint.
On the other hand, there were people like this, the most obvious example being Roger Ver and several others; Charlie Shrem was another one, who were very public figures in 2013, very popular and famous, and a lot of the time they were going on the media and they were trying to push this narrative: "Bitcoin is going to be the next Visa." We started talking about transactions per second metrics, and they were always trying to play down the idea that there would be fees and there would be delays.
They all know we can accept unconfirmed transactions and we can just work around it, and even whole companies were built up around this concept that we could make these transactions sort of free and sort of instant, but actually they weren't really, and this whole, well, I suppose the guy at the bottom here perfectly illustrates the end of that period, or the transitionary period, because that was an amazing video, by the way, in 2013 with him sitting on this bouncy ball.
I have no idea to this day why he was sitting on that when they were talking to him, but this is Mark Karpellis; he used to run Mt. Gox or Mt. Gox, and of course, he's another sort of aspect of the problems of those early eras because there was a lot of, you could call it, amateurishness or unprofessionalness in maintaining these very serious exchange websites, and famously, it completely collapsed with millions of dollars lost, or millions of...hundreds of millions, I suppose.
Charlie Shrem was a businessman.
This sign here is typical of that era.
That was an early attempt to say, Look, we can exchange Bitcoin in shops, bars, and other places.
It's perhaps strange for me to put Andreas Antonopoulos on the same slide, but he's just another aspect of those same early days where they were talking about a lot of enthusiasm about Bitcoin as a consumer payment system.
He's more on the developer and engineer side, but to this day, he's still an important figure.
in a different way.

## The Next Few Years...

Let's try and go to the next few years very quickly.
Basically, in 2014 and 2015, the price dropped a lot.
People are losing interest.
I've put here "lost interest." But I thought it was funny to observe that at the same time we were losing interest towards the end of 2014 and the beginning of 2015.
Of course, because we were losing interest, there were a lot fewer transactions on the blockchain.
Because there were a lot fewer transactions on the blockchain, the price of the transactions stayed very low; if anything, it was lower, right?
It was almost a calm before the storm.
Very shortly after that, although you don't really see it on the chart, in 2016 and then 2017, transaction fees really started to rise and eventually spiked hugely at the end of 2017 due to a lot of interest in using Bitcoin.
It perfectly illustrated all the businesses that had built up that were trying to make this consumer payment system; they were all horribly failing in some way or another because the users simply couldn't use the system.
They would try and enter a payment; in mid-2017, it was very typical.
You'd try to enter a payment with Bitcoin for, say, $20, and you'd try to pay a $2 fee, and then it turned out, oops, you have to wait two weeks for that payment to clear because your transaction fee is nowhere near enough.
It really was the crystallization of all the problems that were discussed earlier."

## Lightning Network Paper

What we'll see in the coming years is that something else was going on in the background.
This is January 2016, roughly.
We have these two guys, Taj Dreiger and Joseph Poon, writing a paper called the Lightning Network Paper.
Initially, it was something just in the back quarters because it was just technical people, a few developers here and there, and so on, researchers who were even remotely interested in this.
This paper was written in a strange way.
I don't know how many people...
hands up if you have actually read the Lightning Network Paper, more than a few lines.
Well done! You're obviously very masochistic people, because that paper is not an easy read.
This illustrates, I think, perfectly.
This die is one of the final diagrams.
It just shows you how complicated the structure of what they were describing was.
It was very difficult to understand, and it was based around a couple of little hacks because, actually, Bitcoin's blockchain intrinsically didn't support it.
Before I run on, what on Earth am I talking about, the Lightning Network Paper?
What is the Lightning Network, just for the people who don't know what it is?
It's basically the idea that, given everything I've said in the last 10 minutes, we need a system where we can transfer bitcoin without actually putting it on the Bitcoin blockchain.
Because the Bitcoin blockchain is intrinsically pretty expensive to use, once enough people start using it, Their idea was, let's make transactions of Bitcoin back and forth, not just back and forth between two people, but between anyone in the world and me, and have it not actually touch the blockchain until some later time.
And we'll go into that later.
That was their idea, but to actually make it work was this incredibly complicated byzantine structure.
Part of what made it complicated was something called malleability.
Malleability is just a fancy word for change.
If something's changeable, then it's malleable.
The problem is that intrinsically at that time, transactions on Bitcoin's blockchain were in some sense malleable in that when you created them, you could then create another version of them that was still valid before it got committed.
I know I'm getting a bit technical there, but basically, there was a problem with Bitcoin's blockchain that made it too changeable.
A solution came out called SegWit, but SegWit got all mixed up with something called the block size war.
In 2016, these guys were coming up with this clever new scheme, and some other people were getting excited about it.
Even though it was pretty complicated, they were still excited because we could get these transactions off the blockchain.
A lot of other people were still arguing about, No, no, no, let's make the block sizes bigger because that way we can get more and more transactions on the blockchain.
The argument was about whether we should go off-chain or make the blockchain bigger to support more and more transactions.
Jonathan Beer here wrote a book recently called The Block Size War.
I think about last year sometime.
If you don't know the history of the block size war, it is interesting, but that's not the topic of our talk."


## The Block Size War

As we reach the end of 2016, it turns out a bunch of people are actually starting to develop this thing called the Lightning Network, at least as software.
Nobody's using it yet because this SegWit thing hadn't yet activated, and it was not very realistic to actually build it.
Because it was complicated, as I just explained, it is definitely a complicated system.
I'll talk about these guys in a minute.
Building that software took time.
Even getting up to the first basic version took some time.
You had these companies or projects spring up.
There was Lightning Labs, started by Elizabeth Stark here, along with Loulou, and they built this LND software.
And this software will be behind a lot of the wallets that we're using later today.
Blockstream, which started in 2015 with a whole sort of sidechain business, Rusty Russell, who's originally a Linux developer, and Christian Decker, who did a PhD in Bitcoin, are famously the first Bitcoin PhDs. They were two of the people, and there were some other people who worked on another version of Lightning called C Lightning, and as I said before, Asank worked on Eclair.
You had at least three, and arguably more, different versions of this Lightning software being developed in 2016.
And it got to the point, so by the end of 2016, we had the whole block-size war raging.
And in the background, at the same time, we had these guys putting together a set of protocols and agreements because they had to make all of this complicated software talk to each other, and it was not trivial.
I remember this: I put here the Scaling Bitcoin sign because in Milan in 2016, there was one of a series of Scaling Bitcoin conferences, and one of the things that happened there was that was the first meetup.
All these guys met up in a room.
I remember there was a whole set of 13 or 14 people, developers, and they were there solidly for two days just hashing it out.
What did they come up with?
They came up with what's called nowadays the bolts.

## The Bolts

The bolts are the standards.
They're a bit like RFCs for those of you who are engineers or internet people.
Basically, it describes what the protocol should do, what the protocol must do, and what every piece of software must agree to in order for all these Lightning off-chain payments to work.
And the outcome of all that is that in 2017, the software moves forward; they have something that works, and by the summer of 2017, this historic moment—it's historic, silly in a way—is at room 77 in Berlin.
You have Laulu, one of the engineers I just mentioned, paying for a beer with Lightning.
This is Jorg Platzer, the guy who owns room 77, actually with Testnet Lightning.
He didn't actually use real Bitcoin.
He used TestNet.
There's actually a story behind that, because why did they use it?
Why did they use TestNet?
I wonder if I can ask the audience why they used Testnet Lightning in the middle of 2017 and not main chain Bitcoin Lightning?
Because SegWit hadn't been adopted at that point.
Because SegWit hadn't been adopted at that point, thank you; that's the correct answer.
The weird thing is that on Litecoin, they actually activated this SegWit thing, this thing that fixes malleability, some months earlier.
They were even trying to do this stuff on Litecoin, as well as on, this is confusing, Litecoin Lightning.
They were doing it on Litecoin and on Bitcoin Testnet, but they weren't doing it on Main Chain Bitcoin because 2017 was the end of the block size; it was this massive explosion.
I can't even begin to describe 2017 to you; it was the most crazy year ever from a whole bunch of different angles.
But from one angle, were we finally activating SegWit at the end of August, somebody correct me, or at the beginning of August 2017, in the middle of August, Michael, anyone?
Roughly, whatever, August 2017.
We activated SegWit in the midst of a hundred other things happening, which I'm not going to describe.
But it meant that from the end of 2017, we could finally use this off-chain protocol called Lightning on the Bitcoin Mainnet.

## What is lightning?

Finally, we actually talk about Lightning really being a thing, a real thing.
It was a real thing by, let's say, sometime in January 2018.
I don't remember the exact date.
In the sense that all the developers said to everyone, Look, this is now ready.
We don't think it's really, really ready in the sense that it isn't perfectly safe and it isn't always going to work perfectly, but it is at least ready to try out and experiment.
People started experimenting with lightning very early in 2018.
This graph here, by the way, illustrates roughly the increase in capacity of the Lightning network between May 2018 and May 2019.
At this point, I'm going to start to get a little bit more concrete about what lightning even is.
Because when I say the capacity of the Lightning network, if you didn't know what it was before this talk, you're probably quite confused.
What do I mean by capacity?
The first thing to understand about the Lightning network is that it consists of things called channels.
between pairs of people.
Any two people, such as Alice and Bob, might have a channel between them.
The best analogy to have in your head about what a channel is is probably the abacus analogy.
Most people probably know what an abacus is.
You have a wire, and you have beads that can thread along the wire.
And so there's two ends of the wire.
And suppose we have ten beads; we could have five pushed over to one side and five pushed over to the other side.
Perhaps it's Alice and Bob on the two sides.
Alice can move one bead from her side to Bob's side, going from five to four to six.
It's a way of moving actual Bitcoin from one end of a channel to the other end of the channel without actually making a transaction on the blockchain itself.
Does that make sense of what a channel is?
Then, if you think about the Lightning network as a whole, it's a network of such channels.
There are lots and lots of them.
Actually, nowadays, it's tens of thousands.
And each one of them has a certain amount of bitcoin in it—those beads on that wire.
We're just adding them up on that graph.
And you can see obviously, like any new technology, there are ways of adoption; there's a sudden growth for this, that, and the other.
For example, sometime in the middle of 2018, there was this thing called the Lightning Torch, and it was  Oh, let's try this out.
Let's try sending money to each other using this protocol off the blockchain right across the world, and I think they did it on Twitter.
One person would send 100,000 sats, sats such as satoshis, right, a 100 millionth of a Bitcoin, and then the next person would send 110,000 sats to some other random person; it would go around in a group, and Bitcoin being Bitcoin, of course, eventually the topic arose: well, can I send this to a guy in Iran, and somebody was like, Maybe you shouldn't send it?
This is—that's what it's for, right?
Bitcoin is for the payments you're not allowed to make; they don't want you to make them, and that's what they say, and of course the other thing about it is that it's dangerous.
So I show here an example: payment failed.
In those days, so we're talking about 2018, it was very, very common for payments to fail because the software was trying to talk to each other and it had to agree on a whole bunch of fiddly little details, and it often didn't agree and things went wrong.
It was still very early.
It wasn't very reliable.
You'd get all kinds of errors and failures to route.
But it did get better during that year.
I can speak from experience.
I started using it probably in February or March.
I tried it a little bit, and I tried it a little bit more.
It was getting better.
So we're coming forward to today now.

## Examples

Being reckless with lightning, I want to show you just some obvious, simple examples of how we have been using it, especially in the first few years.
Gambling is an artist's idea, because a lot of it was just having fun with games.
Because, why not?
Because it's things that you couldn't do otherwise.
Here you have a roulette wheel.
Sorry, the picture's terrible, but it's the best I could find because the site's down now.
It was called Lightning Spin.
You had a roulette wheel, and you would put 1,000 sats.
You'd just click a button, get a QR code, and send 1,000 sats, which is $0.50.
And then you would be able to gamble with it.
You say, "I want a five-time multiplier," and if it comes up on the right color, I get the five-time multiplier; otherwise, I lose my money.
Silly, right?
But honestly, if you try it, it's huge fun.
And there are lots of examples of that.
The point is, by doing that otherwise, each time you wanted to make some sort of change in that game, it would have cost you a network fee, which would make sense in a way.

Let's think about how.
Do you remember what he said?
Alex was saying that if you would need to pay, if we didn't have lightning, and you wanted to pay 50 cents to gamble on that, you'd have to pay a network fee every time.
And, of course, that's true.
Another way of saying it is that effectively, you'd end up with a custodial model, right?
Which is that you would, because you couldn't send 50 cents on the bitcoin blockchain for less than one cent as you can with lightning, you would have had to put $20 on with bitcoin and then just leave it and trust the guy owning the site with your money.
It takes away some of the trust you have to put into a service operator because you can make very small payments.

I think this second example is obviously a lot more beautiful to look at, but it also illustrates the point maybe even better.
Because this was called Satoshi's Place, and it actually still exists.
I can still pull up this website.
You can still use it.
You might want to try this later.
What you can do is click on it, and it says to you, "Right, choose your color," and you can start drawing, but every pixel that you put on this picture is going to cost you one satoshi.
Again, one satoshi is about 1,000th of a dollar.
Just to give you a sense, You can start drawing, and you can draw the Mona Lisa, or you can draw a penis, as many people did back in the day.
I can assure you that.
And you can draw anything you like and it costs you one satoshi per pixel.
It's very, very simple.
I actually tried it again yesterday, just to check if it still works.
It works fine.
Am I still there?
No, I don't know.
Anyway, so the point is, this was really fun, and it was really popular for about one month, and I remember, perhaps people here remember, the Bitcoin Lightning Conference in Berlin in 2019, I think it was, where they had a panel, and there were all these very serious people sitting in a panel talking about lightning.
And somebody's drawing a penis above them because, in real time, it's really funny.
But I think that's lovely because that illustrates that point.
Maybe it's not the most useful thing in the world, but it really does illustrate something you couldn't do otherwise.

## LN Markets

Right?
And I like this example; it is much more recent.
This is a site called LN Markets, and all they're doing here is offering you the opportunity to trade futures with leverage, so the degenerate gamblers amongst us, and there are plenty of them, will love this site if they haven't seen it already.
What I really like about it is something called this link here; you can't see it, but it says connect with lnurl.
What it really means is that when you click it, it pulls up a QR code.
And again, you can try this later if you've got the right wallet.
You can scan it, and it will log you in with the public key of your lightning node.
And the beautiful thing about that is that it's pure public-key cryptography, okay?
You're signing with a key, and you're not giving them any credentials—no emails, nothing else at all.
And you can jump in there, and I did this a couple of months ago, and I put in 2,000 sats or 10,000 sats, and I totally degenerately bet 50 or 100 times leverage, and I made 40,000 sats.
Hopefully HMRC is not listening, but if you are, that's only about 20 quid.
Okay, HMRC.
It's completely without any, and what I love about that is that it's so free.
There's nobody collecting my data there.
Okay, because it's just purely the public key.
Now, of course, the public key of your node—well, that's some metadata that could be used, right?
You could discuss that.
But it's a really nice model.
And the same model is used on this website.
It's a relatively newer one again, called Stack and Use, after Hack and Use, of course, but it's the Reddit-style thing where you can upvote or downvote the post, and when you upvote it costs you satoshis.
You know, does it prevent bot farms?
I mean, who knows?
But the idea is cool, and it still uses, I've actually, you know, you can dox me a little bit, that's one of my mobile phones, node keys there.
I can just use that key, and I can.
That's an identity in quotes that I can use on that site.
interesting, I think.

## Spending Lightning

Just a brain dump here of all the different ways I could remember spending lightning.
Basically, buying souvenirs, buying mugs, buying t-shirts, and different kinds of gambling, that Lightning Spin one, Satoshi's Place, and Bitrefill (which I haven't mentioned yet, is really cool where you can actually buy gift cards), you can buy gift cards using Lightning or mainchain Bitcoin.
And it's just really easy.
And what I like about that site is that they've really tried hard.
They've got really good lightning support, and they've got a lot of other features as well, such as address, if anyone knows what that means.

You can do things like pay friends to settle a restaurant bill, and it might seem like a trivial example, but I can tell you I've done that maybe seven, eight, nine, or 10 times at different meetups and conferences.
And of course, what's cool about it is that it actually works, as opposed to in the past, when we could do it with just Bitcoin wallets, and it did work, but we didn't get confirmations.
We were just trusting each other anyway.
It's really cool that now, with lots of different white lightning wallets, we'll see there are several of them.
You can pay each other this, and it settles immediately.
And that's really nice; it works.

You can buy beer and coffee; I've done that at different meetups.
Of course, not in everyday life, but in El Salvador, you can.
A lot of these things are things I would have paid with Bitcoin before, but I'm now paying with Lightning.
I can pay with my VPS through Lightning.
Sometimes you'll find some of these services using BTCPay Server, which is a piece of software that gives a full suite of merchant-accepting payment services using Bitcoin and Lightning.
It's really cool; I recommend it.

Donations—the nice one I think here on this list is podcasters.
It's a new thing.
If anyone's used Breeze, I think there are a couple of other apps that do it.
You can listen to a podcast and pay per minute.
I pay 10 sats per minute when I'm listening to podcasts on the app.
And if I want to, if I hear something I really  I can boost it and give it more sats for that specific timestamp.
Again, that's an example of the whole micro-payment idea in action.
Of course, the final point is that we do tend to still use the Bitcoin main chain for a lot of payments, especially if they're larger than we tend to use them.

## Growth

Okay, we're getting through.
Growth—that's what the network looked like in the end of January 2018 on the left.
It's already pretty complicated, right?
However, there aren't that many nodes; there are just a lot of connections.
Nowadays, if we try to visualize the Lightning Network, it's nearly impossible because you can't.
I mean, so this is some weird AI, machine learning thing that came up with some picture that I don't even really understand.

Why is it so difficult nowadays?
Well, if you look at the actual statistics, you see the number of nodes is increasing pretty rapidly.
And actually, 1ml.com has about, if you look at it right now, about 31k nodes recorded there.
This was something I got from the recent "Mastering the Lightning Network" book that Andreas Antonopoulos and René Picard worked on.
I don't really know exactly how they're getting their numbers compared to theirs, but there's a slight difference, but it doesn't really matter.
Order of magnitude: we're talking about 50k nodes and 100k channels.
and it is growing.
Some things are growing faster than others, which may be interesting as well, but hopefully it's obvious to you because I've talked to you about channels.
Two people share a balance.
Capacity is the sum of what's in Bitcoin in all those channels.
And of course, part of this is, how do we really measure these stats?
That's very hard.
Because what you've got is a decentralized network of people, perhaps Alex and Philippe here have a channel, and then you two have a channel, and you two have a channel, and we're all supposed to talk to each other on this decentralized network and tell each other, at least tell each other what the channels are and how much Bitcoin is in them.
Of course, we could be lying, and then there's the question of, even if I know the total capacity on the channel, how much of it is on the left and how much of it is on the right?
I don't necessarily know that.
It's a very complicated business.
And there's this thing called private channels as well, where you don't advertise them.
It's a very complicated business to talk about analyzing the whole network and getting the full picture.
This is at best an approximation, and I would guess that because of private channels, for example, that number is a significant underestimate.
How much, I couldn't tell you.

## Intermission

It gives you a sense of the network's growth, and it's actually pretty large right now.
Now for an intermission.
By intermission, unfortunately, I do not mean that I stop talking.
That will happen shortly later.
What time are we at right now?
We have everyone.
Okay, we only started, okay?
That's about what I thought, okay?
For this, I'm going to need a table.
I'm sorry.
Basically, what I'm going to explain now is that without using technical jargon or any technical information at all, I really want to explain how a lightning network payment channel works.
The lightning network is now two words.
I'm only going to explain Lightning with this.
I'm not going to explain the network part, which is just as crucially important: even if we can pay each other, how do I pay him when I'm not connected to him?
I'm going to ignore that.
I'm just going to talk about two people trying to pay each other, but without using the bitcoin blockchain directly, to try and save on fees, so it costs less, to try and be instant instead of 10 minutes, and to try and be more private.
There are three advantages to doing it off-chain, right?

What we do is develop some contracts.
Imagine it as Alice and Bob, right?
You won't all be able to see this perfectly, but let's say this is the first contract.
Alice and Bob make a contract where Bob will be the black ink and Alice will be the blue ink.
Keep that in mind: Bob black, Alice blue.
In this particular situation, Bob has $90, Alice has $10, and they're pre-agreeing that because...
he's worrying me.
We're okay.
We're pre-agreeing that because, let's say, Bob actually has $90; he puts it into the pot, and Alice has $10; she puts it into the pot.
That's their actual balance, right?
They make a contract that says, Okay, Bob has 90, Alice has 10, and we both sign it.

These two names at the bottom represent signatures.
They're both signing this contract.
Now, of course, there's one thing weird about what I've written here, which is this one day.
What am I talking about?
What I'm saying is that on this particular version of the contract, Alice's money, Alice's $10, is locked up for one day.
If we go to the blockchain, and I'm representing the blockchain by my robot judge, because after all, the whole point of the blockchain is that it's completely impartial and it's completely algorithmic.
It just decides on the rules, right?
If I show this contract to the blockchain, it'll say, "Yes, okay, Bob gets his $90 because it's signed by both of you guys; that's fine.
Bob gets his $90, Alice gets her $10, but just one thing: you can't settle this contract before the day is up, Alice.
You're not going to get your money straight away." That seems a bit weird, but you'll understand it in a minute.

What we do is make two versions of the same contract.
This second version is the one that Bob makes, or, let's say, is applied to Bob.
This has the same amounts of money and the same signatures, but in this case, it's Bob's money that's locked up.
Bob keeps the one where his money is locked up.
If I sort of put them on two sides, so you're going to be Bob and you're going to be Alice, sorry.
Bob's version of the contract has his money locked for one day.
Alice's version of the contract has her money locked for one day.
And so the whole point of making these contracts, at the moment, does nothing, right?
Because who cares, right?
We already have the money.
The whole point of making those contracts is that we can replace them, or we can try to anyway.
I'll take Alice's version.
This is a new version.

## Intermission (Continued)

In this version of the contract, Alice has $70 and Bob only has $30 because Bob is paying Alice $60 for some expensive socks, right?
Bob's paying Alice $60.
That's why they've changed.
It's 30 on his side and 70 on her side.
Just as before, we lock the money belonging to the person owning this version of the contract, and that's Alice.
Alice's money is locked, Bob's money is locked, and we created a new version of the contract.

Now, have we finished?
Is it the case now that, okay, I've paid you, Alice?
There you go; there's a new version of the contract; it's got $70.
We're done, right?
We can keep doing this; we can keep updating the contract, right?
What's wrong with that?
Right?
What's wrong with that?
There are two different versions of the contract.

Right, yes.
Suppose you take Bob's point of view.
He's looking at this saying, "Okay, we've done that.
I've got these two contracts.
One of them says 90–10, and one says 30-70.
Well, for this one, I've got 90, and for this one, I've only got 30.
I don't care about that one, right?" He's going over here and saying, "Here, give me $90.
Now, I've got my $60 socks.
I've effectively stolen them from Alice, haven't I?
I've basically told him that this is the truth."

And of course, the real issue here, isn't it obvious, is that we didn't tell this guy about this change?
We didn't tell this guy.
That was the whole point of the system, right?
We were trying to avoid the huge fees and delays associated with using this guy.
We want to do it separately on our own, right?
By doing it separately on our own, we've avoided those fees.
But unfortunately, we haven't actually solved the problem because we updated a contract, but we did not invalidate the earlier form.
That's what we do next.

What we do is take out a new contract.
After creating these two new versions of the contract, we also create a rider on the contract, or, what's the word, an extra clause in the contract.
This one says if contract 1a says that 1a is Alice, if contract 1a is executed, I can't read, pay all $100 to Bob.
Alice signs that.
What Bob can do is keep this extra clause.
That's Bob.
Bob can keep the extra clause saying that if Alice ever spends the old version, he is going to be able to take her money.

Now, the opposite.
Bob signs an extra clause on his contract, and it says if I ever execute contract 1b, well, all the money is going to go to Alice.
And Alice can take that.
I know it's a bit complicated, but what I'm trying to illustrate to you is that essentially, it's almost just like a legal wrangling; it's just a legal construction.
What it means is that here's Bob; he's paid his $60 to Alice.

If he decides to be a cheat and tries to use the old version of the contract and walks over here and says, "Give me that," his money's locked for one day, remember?
Maybe Alice went off on a day trip.
He's trying to execute this, and he's hoping she won't get back because if she doesn't get back before one day, this guy's just going to give him the $90 because it says it right there; it says that's what he should do.
And he's not going to argue; he's only going to follow the rules; he's a robot—more of a she, actually.
Sorry, my mistake.

But, however, if Alice gets back before the end of that first day, what happens?
What has Alice got?
She has the extra clause, and she goes over here and says, "Look, you've got this contract here; it says that that's all very well, but I've got this extra contract," and by the way, I'm missing some important technical details here for those of you who know these things; please forgive me for that, but the basic logic is here: well, because that contract exists and this is an extra clause on the contract, it says, if he's trying to execute that, give it all to me.
Well, he's just going to give it all to Alice.
The entire $100 ends up with Alice, right, in that scenario.

Bob would be stupid; at least if he thinks Alice is alive within the next day, he would be stupid to try and execute that contract.
He won, right?
That's the theory, anyway.
And we can keep repeating this process where we just keep updating the contract, a new version of the contract, but also here's a rider or an extra clause to the previous contract, and we just keep doing it over and over and over again.
Every time we do that, we're creating a situation where the other side is incentivized to not cheat us because if they do, they're going to lose all their money in the channel.
Right.
Does that make sense to you as a broad outline of how it works?

## Problems

That's a bad question.
What might be the problem?
I think it's fair to say that there are two obvious problems with this construction, two ways it can go wrong.
Let me put it like that.
What are the two ways this construction can go wrong?

So the first problem is what we call liveness.
Here I use the example of one day, but we would actually use longer periods than one day—two weeks, for example.
If you're not around, somebody might cheat you, and if you just stay offline for a long time, then their cheating could be successful.
In what I just described, this would be executed after one day, two weeks, or whatever it is.
That's the first problem.
This protocol is not like Bitcoin, where you just receive money and forget about it for four years.
That's the first one.

The second one is a bit more subtle, so I'm not sure if people will say what I'm thinking in my head.
What does it have to do with it?
It's to do with that, for sure, 100%.
That's also a liveness thing, right?

Audience: Because of the fact that people lose their money because of the old backups.

That's the same thing again, though.
But that's the other way.
Okay, that's more advanced and important; maybe you can explain that in the second half.
It's a good point.

No, actually, what's in my head?
It's very bad for teachers to say, "What am I thinking, right?" What's in my head is this.
That mechanism relies on both sides, or at least on the particular cheating side having something to lose.
In a situation where one side of the channel has nothing at all, it literally has no cost to them to try and cheat because you can't punish them.
In Lightning, they have a thing called the channel reserve, and the channel reserve is at least an attempt to solve that issue.
But really speaking, Lightning works only really well where you have these relatively balanced channels because of this game-theoretic assumption that we need to be able to punish someone.
This whole process is called LN Penalty nowadays to contrast it with another way of doing Lightning, which I'm not going to get into, which might in the future make this whole thing a bit more smooth, maybe.
All right, so that was my attempt.

## Payment Channels

I don't know if it was 10 minutes, but it was my attempt to explain payment channels in 10 minutes, and the other half of lightning, the network half, I'm not going to explain now, but it's a similarly clever piece of reasoning.
Using wallets.

Audience: I think we can talk a bit about what happens.
Those contracts and stuff—are they actually being used for those channels all the time?

If both parties are being honest and are live and active, you can always replace a complicated contract with a simpler one that just says, Give Alice $10, give Bob $90.
We can avoid some of the nastiness of having complicated contracts displayed on the blockchain.

Audience: The users are separate from the nodes themselves, right?

Well, all I've described there is what's called the Poon Dryja payment channel, technically, because it was the two guys I showed earlier who came up with this idea.
And it's a bidirectional payment channel.
It's the basis of lightning in the sense that each of the two parties in lightning forms these channels, and then we have a network of them.
One person could have lots and lots of channels, I think, which is your point.
Absolutely right.

## Wallets

Wallets.
Let's talk about actually using it, because I think I've done enough theory, haven't I?
These are examples of wallet UIs. Actually, the one on the left is BlueWallet, but it's a bit of a comparison, the exact screen is different, but it doesn't matter.

Basically, what you'll see in most of these is that you'll see an amount.
The amount can be in Satoshis, the amount can be in Bitcoin, the amount can be in dollars, pounds, or whatever.
Okay, they'll vary that.
They may or may not show you a list of your historical transactions.
What they will tend to mostly focus on in what we're doing next is that they have buttons for sending and receiving money.
And very often they'll have a separate button for scanning a QR code, because most of them will allow scanning a QR code to be sent.
But the thing to remember is that this is an interactive process.

What makes this different from Bitcoin is that it's true, and it's almost entirely true that both parties have to be present.
In Bitcoin, the receiver can just be asleep.
But in Lightning, that's not really the case.
Serve is the caveat there.
We're going to send and receive.

And it looks similar to Bitcoin wallets, especially today; it doesn't show you stuff about channels by default.
It used to be the case right at the beginning.
They used to say, "Oh, open your channels and manage your channels." Users don't want to talk about channels.
They just want to talk about sending money and receiving money.
And that's mostly what these wallets tend to do nowadays.

This is actually BlueWallet, Phoenix, and Breeze, but we'll see that later.
This is Muun, which some of you just installed.
This is actually a different one called Zebedee, which is more of an example of a custodial wallet.
Actually, Blue is as well, but complicated.
Custodial means, well, in that case, you're not even holding the private keys yourself.
You're actually letting someone manage the money for you to some extent.
And maybe they're using lightning in the background, but that's not quite the same thing.
We'll talk about those trade-offs later.

## Lightning Wallets

I've shown this one as an example of what happens when you actually try to work with lightning at a sort of deeper level.
If you run a full lightning node and maybe have it connected to your home Raspberry Pi and you have various other models, servers, and what have you, you can start getting involved in managing channels, and oh, let's try and find liquidity, let's try and provide liquidity, and get money for providing liquidity.
There's a whole rabbit hole about how deep you can go with lightning.
But for now, let's just think about using it for sending and receiving payments.
Briefly, I could mention my experience in El Salvador recently.
I'm not sure if anyone—maybe one or two people—was in El Salvador with me, so they know about it.

## Summary

How can I summarize this quickly?
Because I'm running on a little bit too long.
You've got the Bitcoin; it's very much a tale of two cities, the El Salvador experience.
You've got the Bitcoin Beach, a famous project, in a place called El Zonte, literally on the beach, of course.
very small place, very, we could say underdeveloped, few restaurants, few hotels, and basically everyone there has, as a project, started using Bitcoin and also Lightning for payments for various things.
And they tend to use something called the Bitcoin Beach wallet, which is a really strange hybrid.
It's not really like the things I just showed you, which you just installed on your phone.
It's a centralized custodial service by a company called Galloy.
And when you scan their QR codes, maybe later one of you might want to try that one, particularly, you'll see that you actually get sent to a webpage, not to a lightning wallet.
You have to go to a webpage, and the webpage then hosts the lightning payment invoice for this person, even though again, it's custodial.
They themselves are not holding the keys.
It's a good example of how people make trade-offs in the real world.

Audience: Is that just for their business when it comes to tax, or does that help in accounting?

I think it's a complicated question as to why they've gone down that road, but I think it's mostly about the technological difficulty of it, which makes it a lot simpler for a person who doesn't have a detailed technical background or the time to get involved in nodes and whatnot.
I think it's interesting.
I want to move on, but I think it's a good question.
Maybe we can talk about it in the second hour.
Chivo.
I want to mention Chivo; it's very important.
Chivo, this is an example of the better aspect of Chivo, where their ATMs actually successfully give you dollars in return for Bitcoin.
But it's the main chain only at the ATMs. Their mobile wallet is, quite frankly, a complete disaster.
I mean, by all accounts and by my own experience, a complete disaster.
It does not work for lightning anyway.
It has, by default, a US dollar interface.
By the way, guys, you were there.
Correct me if I'm wrong; it has a US dollar interface by default.
You can choose bitcoin, but that will default to main chain bitcoin.
And then, if you look really carefully, it will go to lightning, yes.
I was just going; you didn't finish; let me finish.
In the third option, if you look carefully, there is a button to choose lightning, right?
And perhaps you're going to correct me in saying this, but from what I heard from other people and from myself, it tended to be the case that even if you could get a lightning payment to work, it wouldn't show up on the app.
Did you find it different?

Audience: Yeah.
It works for me all the time.

It works for you every time.
Okay.

Audience: I was thinking about the merchant version.
Yes.
Personal version.
And maybe the merchant one didn't work.

The personal one worked.
Right, that sounds right.
Because I just remembered now, I did pay one person; it was a barista at a coffee place.
I paid his personal Chivo wallet.
Fine, you're exactly right.
But for the merchant one, I tried it a couple of times, and I heard several other people saying that when you're in a restaurant and you try to pay them, your wallet will show that you've paid $10, and their wallet will show nothing.
It was a disaster.
I had to pay twice.
But there have been several other problems in the early days of Chivo, and from what I've heard from people, it's really bad.
And I'm upset about it because I think it's damaged the ordinary Salvadorian's perspective on what bitcoin adoption might be.
I'm not going to mention some of these other things.

## Other Things

This is the Starbucks point of sale, which, in my experience, worked flawlessly every time.
I think it's IBEX; does anyone know?
I don't really care; it's some company that did it.
It's funny, though; they show three different denominations.
They throw dollars, and then they show SATs, S-A-T, and capital, and then they show BTC as well, just in case you get confused.
It's just supposed to help you understand what the price is, I guess.
But anyway, it works absolutely fine with more than one Lightning wallet for me.
Also, McDonald's, of which I'll give an example in a minute.
Just to make pictures, that's Bitcoin, this is my slideshow now, my holiday.
I mean, it's a bit, sorry.
Bitcoin Beach looks really nice in the sunset; cool.
This is Hope House in El Zonte, where you have some guys who drove from Argentina or something; I don't even know the story here.
This is something I just donated to, and that was the new mural by Bit Refill.
It's a very interesting place to have a look at.
But San Salvador was different because they didn't have that Bitcoin Beach wallet thing.
A lot of people were using Chivo, which didn't really work very well with merchants.
But on the other hand, McDonald's, Starbucks, and a few chain restaurants were working fine.
It was all very strange.
And when you talk to the taxi drivers, half of them think it's great, and half of them think it's terrible.
I don't know what that proves.

Video Time! I just thought it might be amusing to finish this off by showing you what it's like to use it.
If my eyesight can actually find it, there it is.
This was a completely serendipitous meeting on the street.
It's already scanned the QR code.

VIDEO: *Difficult to Hear* All we need is a hotspot and 815.
You got it?
Woo! All right, all right, there we go.
Every time I see it, everybody's like Woo! Strict deals, coffee.
I keep on talking about coffee and tea.

This very short video is basically about how I met a guy called Tomer on the street.
He's a local here, actually.
He's a journalist, and he makes videos and stuff.
He and his cameraman guy were talking to this guy who runs a coffee plantation—or owns a coffee plantation, I don't know.
Anyway, he was getting interested in Bitcoin because he was showing them around, and they said they gave him; I think they gave him; I know, they gave him Muun Wallet; he installed it; and I just met them on the street, and I said, "Oh, you're selling coffee; I'll buy coffee with Bitcoin from you." It's a meme, right?
You have to buy coffee with Bitcoin.
You've got it, right?
He goes into the building, comes back out with a bag of coffee, which you can't quite see, but I'm holding it in my hand here, and he says, "$10," and I paid him, and it worked immediately.
Now, I think that's a really cool example of how it can work.
This is how it could be.
It could be the case that we reach a point where everyone can reliably pay each other.
$10.01 I paid for a $10 bag of coffee.
I didn't know him, and he didn't know me.
It worked perfectly in, literally, two or three seconds.
Of course, it's not always going to be great like that, but that was an example where it was really good.

Another example, which is a few seconds longer but also a short video, is this.
I actually just nabbed this from Twitter.
This is why a lot of people here will know him.

Video: *Difficult to Hear We're getting a bit of an order at the company.
We're a couple of minutes late.
It's what you'd expect; it's the normal McDonald's...
that's a bit...
squeeze...
that one's squeezed...
okay, that's water.
Right, paint.
And then that seems to shut down.
And here...
that's a bit of a breakup; we know that's what's going on.
And with Bitcoin, see that?
I'm going to get the seats jacked out.
I'm going to put it here.
Because I'm going to break up.
We know that's not true.
With Bitcoin, see that?
We're going to see that.
Nice one; I'm there.
And I'm going to use my Allen Bits wallet.
Guys,  thanks for the tips, but this is not the Allen Bits tip jar.
I think this is a good excuse to make a payment.
I'm not a tip jar; I mean, it's not bad to make a payment from a tip jar.
There we are.
third big coin.
I wonder what a coffee from McDonald's would be  There you go.
Seven points.
Scare it.
Don't pay it.
Just please.
I want you to copy a copy of McDonald's using Lightning.
I know.
All right, here we go.
Is that 10 points?
Ha, ha, ha, ha, ha, ha, ha.
Scan it.
Double-click it.
It's really slow.
Come on, Lightning.
You can do it.
LN Bits will let.
No, I mean, it's just a little bit slow, but it works fine.
Oh wow, look! It does.
Really?
It works just fine, yeah.
The paper works through.
Yeah.
Wow.
Nice.
Nice.
Thanks to the company.
And thanks for letting me pay for it.
I'll get the LN bits, Chuck.

I mean, that was a bit slower, but in my experience, I used the same thing several times, and it was absolutely fine.
Okay, well, I think I'm more or less done in the first half, so we can.
If anybody has any questions or thoughts, please ask; otherwise, oops, there we go; otherwise, we can move on to actually using it.
Your turn.
This is your turn.

## Liquidity

Audience: Questions.
Between the nodes, you can add liquidity.
What did you mean by that?

The concept of liquidity is really important here.
Basically, when we talked about the payment channels, there was $100 between Alice and Bob, and the money was being moved back and forth.
We can't move more than $100 back and forth because what we do is put that $100 into that channel.
It's fixed there until we decide to close the channel.
Channels are opened for a certain amount of money, and then we have that amount of money in that channel.

Think of it: there are lots of channels with different amounts—one with $50, one with $500, one with $100—all over the place, and we're trying to move money around through these channels.
Sorry, I didn't explain all this, because I didn't want to get too much in the weeds.
Liquidity is something we're talking about, how much money is available to be moved in certain directions through the network.
Is that helping?

Audience: But you said it adds liquidity.
How does it add?

Well, there's multiple answers to that question as well, unfortunately.
One way you might want to add liquidity is by simply opening a new channel for a larger amount.
It is possible to do something called splicing, but that's technical because you can actually take the same channel and increase its size.
Generally speaking, you can't change the size of the channel once you've created it.
You would have to either add a new channel or close the old one and add a new one with more liquidity.

If you're thinking about that example that I showed, what's going on there is that when I talk about providing liquidity, I might have a Lightning node, and I might want to receive a lot of money because I'm a merchant selling goods.
I'm expecting lots of payments, but I might not have a channel with an inbound capacity that is big enough for that.
What I would do is go out onto the market and say to people who can open a channel with me for, let's say, $10,000; that's an extreme example, but open a channel with me for a large amount, and I will pay them a small fee, a small percentage fee, in order to do that, to help me.

Audience: Oh, in order to ensure that the contract thing can't be broken.

Well, just, yeah.
The other person isn't zero on the end of the thing, is that it?

It's just that the problem is that it's limited, right?
It's supposed; here's a classic example.
You are a merchant; you want to sell 10 pairs of socks every day, and let's say it's $500 every day.
You get a channel open, and your first problem is, oh, but I open the channel, I put the money in it, and I need the other guy to put money in it so he can pay me.
I need someone to open a channel for me, so to speak.

There's a directionality here, which is tricky.

Audience: But that's someone's; it's actually, it's actually, it correlates to actual Bitcoin.

That's, but that's the weird thing, because if I ask you to open a channel for me, I'm not asking you to pay me.
There's a subtle difference there, right?
If you open a channel for me for $1,000, it doesn't mean that you've given me $1,000.
What you've done is locked up your $1,000 in that channel.
Now, if I go away, you'll be able to take the money out again, but it's a hassle.
I have to pay you for the time and the annoyance of dealing with that.

Audience: If you want to receive some of those beads, either you need to spend some of those beads to get them to the other side so that they can come back, or someone has to open the channel with beads on their side so they can push beads to you.

Audience: But all the beads correlate one to one with Bitcoin and the blockchain?

The total amount of beads, so to speak, is locked in what we call a multi-signature address.
It's literally an address on the blockchain containing those funds, but it's just that it requires both parties' signatures to move it.
It's locked in the sense that until both of us agree to close the channel and move it out, it will stay there.

Audience: But it's not an inflation of the...

No, it's Bitcoin that already exists, and it's just locked.
It's locked in this subtle sense that it won't go anywhere until both of us agree to move it.
I know that technically, I haven't really covered how it works.
I'm sorry about that.

Audience: Say, for instance, that if the person could potentially win a certain amount, you still have to have liquidity there for what that person could win.
In effect, you open the channel, play the game, and then you separate everything at the end, but you still have to cover what that person could have won, whether they win it or not.
That makes sense.
It's quite obvious.

But let's get on a bit.
Our task now, because we've only got 50 minutes, is to get on.
The first step is that I want everyone to at least have one of these wallets on their phone.
If you're on Android, it means Phoenix Wallet, Muun Wallet, Blue Wallet, or Breeze.
People will help you; lots of people here have lots of experience with this.
If you're on iOS, not Phoenix, because it's not available on iOS, but the other three, those are choices we've made because they're probably the most convenient for these demonstration purposes.

And I want to be able to pay people money—10,000 Satoshis, which is, you know, a few, two or three, I don't know, four pounds—and not just me; maybe a couple of other people will help out as well.
But I want everyone to at least have the experience.
If you've already had this experience, then just help other people.
But I want everyone to have the experience of trying to receive money.
And you can receive it immediately in one of these wallets.
Any questions before we start, or should we just get on with it?
I think we should just get on with it, right?

And then afterwards, you can try paying as well as receiving.
I mean, go ahead.
If whoever's ready to receive 10,000 sats, just say the word.
myself, and certainly Alex as well.
Maybe some other people might also help in making these payments.
And once you've got some money, you can always, of course, pay me some with this QR code.
Oh no, not this QR code.
But no, I'm going to give you an LN address later.
I'll do that later.
Let's receive the money first.
Are you ready?
