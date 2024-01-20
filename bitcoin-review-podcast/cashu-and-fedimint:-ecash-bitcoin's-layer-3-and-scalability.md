---
title: "Cashu & Fedimint: ecash, Bitcoin's layer 3 & scalability"
transcript_by: satstacker21 via review.btctranscripts.com
media: https://www.youtube.com/watch?v=-nzVYVcdk9M
tags: ["ecash"]
speakers: ["Calle","Eric Sirion","Rijndael","Matt Odell"]
categories: ["podcast"]
date: 2023-04-13
---

## Introduction

00:00:02

Everything else versus Bitcoin essentially gets spent and dies.

00:00:05

I want to be able

00:00:06

to have reactive security and I think OpVault is today the most straightforward, easiest to use way to do that.

00:00:13

I will not be insulted by a clockmaker.

00:00:21

Overall these kind of ways to make the network easier to both build on and interact with, I think is a really big deal.

00:00:27

If Bitcoin existed when we started Twitter, We would not have to go down the ad model path.
I mean, as simple as that.

00:00:33

Integrating Lightning into a social network is the killer app.

NVK: 00:00:37

Hello and welcome to the Bitcoin.Review podcast, where we explore developments and projects with the people who actually make them happen.
The show is supported by Pod 2.0 SatStreaming and CoinKite.
If you're a new listener, I'm NVK.
I run CoinKite, where we've been helping people secure their Bitcoins for over a decade.
We make the coldcard and fun products like the Block Clock.
You can find more information about it on coinKite.com.
If you haven't had your brain completely destroyed by the segregated witness episode, I hope that the e-cash episode will finalize.
It's going to be fatality of your brain on this one.
So I have with me a really good group of folks, two of them who are working on the biggest projects, who are deploying E-cash out there in the world.
So

## Guest introductions

welcome Calle.

Calle: 00:01:33

Hey there, NVK, hey everyone, Thanks for having me.

NVK: 00:01:36

Hey, so which project do you work on?

Calle: 00:01:39

Oh, it's called Cashu, as you say, or I say Cashu, which is a Chaumian eCash system built on top of Lightning, basically for Bitcoin Lightning.
Yeah.

NVK: 00:01:50

Very cool.
Mr. Eric.

Eric: 00:01:53

Hey guys.
Thanks for having me.

NVK: 00:01:56

What's the name of the project you're working on?

Eric: 00:01:58

Yeah, I'm working on Fedimint, which is a federated e-cash protocol on top of Bitcoin with connectivity via Lightning.

NVK: 00:02:06

Nice.
Rijndael, thanks for coming back, sir.

Rijndael: 00:02:11

Hey, good morning.
Good to see everybody.

NVK: 00:02:13

And Mr. Odell.

Odell: 00:02:16

Very excited for this conversation.

NVK: 00:02:18

I can tell by your tone.

Odell: 00:02:21

It's an early one.

NVK: 00:02:24

I am racked.
I actually didn't sleep.
It's very rare that
I don't sleep.
And last night was brutal.
I think it was just hot.
So yeah, third cup of coffee might get me going on this.

Odell: 00:02:36

Had a very whiskey-fueled Easter.

NVK: 00:02:39

That's nice.

Calle: 00:02:40

Yeah, very nice.
For me, it's almost evening, so I've been already having a couple of beers today.

NVK: 00:02:45

Oh, look at that.
I bet Odell was having the whiskey during Easter because he was trying to tell people that the banking system is gonna collapse and family does not want to hear about it.

Odell: 00:02:57 

Guilty.

## Chaumian ecash origins

Alright guys let's let's, let's start at the signal here.
Who cares about our personal lives?
So e-cash, very old tech, Mr. Mr. Chaumian invented this in the eighties.
Right.
And, it was kind of like interesting, but you know, it was not viable, right?
I mean, every project that tried to employ it sort of failed and I have an opinion about this.
Well, I might as well give it.
It's because Bitcoin didn't exist.
So you didn't have a source of truth.
You didn't have a way to peg in and peg out.
You didn't have a way of interacting as an on and off ramp with a system that's digital without digital money, right?
So like match made in heaven, This thing is now actually usable.
It's super cool.
Very well proven technology, very well studied.
But then comes Eric and Calle and like take this thing to a whole other level And because of Bitcoin, because of Lightning.
And I hope we can sort of explore this in depth here.
So who's going to volunteer to give a little bit of a technical primer of what is eCash, what is eCash now, and sort of like where we're at on how you guys are exploring it.

Calle: 00:04:26

So I'm going to try it here.
First of all, maybe just a comment on what you said.
I'm not so sure that DigiCash, which is the company by David Chaum, who invented this whole thing in 1982, DigiCash, the company was founded eight years later.
So 89 or 90 or something.
So there was a pretty long gap between those two events.
And DigiCash itself tried to be viable for almost a decade, but I think active it was for maximum five years or so.
And when you look back on the reasons why it failed, It's not usually because the fiat system was so prohibitive.
So that's also my take.
I share the take with you that e-cash needs Bitcoin to really shine.
But when you look back, the reasons why DigiCash itself failed was literally poor management.
So there were insanely huge deals on the table.
There was Deutsche Bank was interested, but that wasn't even the biggest one, I think.
Microsoft- 

Rijndael: 00:05:26

Do you know Microsoft want to put it in Windows or something?

Calle: 00:05:28

It's insane.
They wanted to put a DigiCash wallet into every Windows 95 installation, but David Chaum then wanted too big of a share of the income there, or the money generated, so Microsoft pulled out.

NVK: 00:05:43

He has a history of expecting a little too much and wanting too much of a set of things.

Calle: 00:05:47

And the third one is Visa.
Visa offered them 40 million back in the 90s.
That was still real money, right?
And he just said, no, I want double of it just in the last couple of days or so.
So the deal also failed.
So my way of seeing, looking at this is DigiCash then crashed or was, you know, just a closed shop.
And then a couple of years later, PayPal and credit cards on the internet really blew up.
So I think...

NVK: 00:06:16

How convenient.

Calle: 00:06:17

Yeah, I think so.
If things would have gone a little bit more different back in the 90s, I think the default online payment experience today could have been, without Bitcoin and everything before, could have been perfectly private e-cash on the fiat system.
That is technically possible.
I know regulatory problems then started with, you know, everything that's happened later.
But it's just, I mean, it's unimaginable today to build e-cash on fiat, I think.

NVK: 00:06:43

You know, just as a small tangent on that, like, you know, yes, it was technically possible, but can you imagine if it was just a little bit successful, the regulators would have come crashing on it.

Calle: 00:06:55

Yeah it's true but that's what also people said about Bitcoin so you know once something spreads

NVK: 00:07:00

a bit.
But you could stop eCash on Windows right you could stop eCash on Visa and there is no digital on and off ramp without the Fiat system.
You know, like it's one of those things that like, yes, it was kind of possible technically speaking, but you would have been killed it.
At least in my opinion, it would be killed because.
Too easy, like, you know, Liberty Reserve, Bitgold, like every other Bitcoin sort of pre pre digital cash that pre Bitcoin that was attempted, we got killed when it got more attention, right?

Odell: 00:07:35

The banks are the choke point.
It's the banks.

NVK: 00:07:38

That's right.

Rijndael: 00:07:39

Yes.
Well, and importantly, like traditionally, e-cash relies on a central issuer.
So even if you have transactional privacy, that's still where you're going to apply all of your regulatory controls.

NVK: 00:07:51

There is somebody to jail.

Calle: 00:07:53

Yeah, exactly.
So sorry for the tangent, but let's...

NVK: 00:07:57

No, no, it's good.
It's good.
We need to sort of give people like, you know, why's and the who's and go for it.

## ecash integration with monetary networks

Calle: 00:08:04

So how it works, right?
E-cash works the way I thought when I first learned of Bitcoin, how I thought it works, but then I learned that it's not the way it is.
So in Bitcoin, you have the blockchain that is somewhere out there in the network.
What you hold is your keys and you construct transactions that you then submit into the network and eventually they get mined and that becomes a Bitcoin transaction, right?
So in Bitcoin, you hold keys and then you make transactions.
With eCash, it's very different from this setup.
What you actually hold are digital pieces of data that represents the money itself.
It's not a key to the money but it is the money in the system and you hold it literally on your hard drive on your mobile phone and when you want to pay someone you take a little bit of the data and you send it over the wire to someone else.
And then they receive it by sending it once to the mint, destroying it and getting a new one.
That is how you prevent the double spend, basically.
So the whole setup of how eCash is built is very different from all the blockchain stuff that we've seen later.
And yeah, it seems it's a good fit to combine this with the blockchain.
It seems, you know, once we have Bitcoin, we can build on top of it.
But yeah, that's a very high level overview of the dynamics.

Eric: 00:09:14

Yeah, Fun fact, when you say it would be good to combine with a blockchain, people actually tried it.
And I think that was the original Zerocoin protocol paper that came out that implemented eCash on Bitcoin.
And then it turns out, yeah, Bitcoiners don't really like having some moon math running on their blockchain.
So they continue development and that's where Zcash came from originally.

NVK: 00:09:43

You know, I think David tried to launch his own shitcoin as well, I think was maybe like 2016, around that time.
I forgot the name of his shitcoin.

Eric: 00:09:56

Yeah.
I mean, the incentives are just very strong to do that.
So.


NVK: 00:10:00

Is it called Terra or something like that?
Anyways, you know, after Bitcoin, a lot of projects try to do e-cash sort of blockchain, e-cash things that sort of, Hey, how can we just stick one thing on the other?
But at least to me, the true advantage here is Bitcoin really provided the on and off ramp to the mint that you wouldn't otherwise, right?
I mean, like, you know, Visa is just sort of like paper, Right?
Like you can't, like Visa is not like an actual token that you can sort of bring back and forth between your mint and a person.
So you need, you need like a provable money token, which is Bitcoin, right?
That you can then use with this other decentralized thing.

Rijndael: 00:10:54

Yeah, like you want both common money for people to settle in and out of the mint with, but I think you also want a common neutral money for mints to settle with each other with.
Because one of the problems that every ecosystem runs into is kind of this like cold boot, like bootstrapping problem of, You know, nobody wants to use your money if there aren't goods and services that accept it and nobody wants to build like marketplaces if nobody's using the money.
And so if you have, if you just went off and made your own Chaumian mint that's like NVK cash or something, And the only thing that people can buy-

NVK: 00:11:32

Any day now

Rijndael: 00:11:33

With it is sats cards.
Any day now?
Yeah, any day now.
The only thing that people can use is, you know, Sats cards and it derives its value from the future ability to buy Sats cards with it.
That's going to have very limited utility and not a lot of people are going to use it.
If you can have, you know, NVK cash, but it's redeemable for Bitcoin, then that's a lot more valuable because like now you get to lean on the network effects of Bitcoin.

NVK: 00:11:57

Well, I mean, any money network is only as valuable as your capacity of getting in and out of it.
If you can't trade the tokens, right, for something else, it's a problem.
And, you know, as you've learned from PotatoCoin, which was really a guy in Russia trying to use potatoes, and he actually got the whole village to use potatoes to buy and sell.
And then he got to, he went to jail.
Like I mean, you know, the Russians, it got so successful that he got arrested.
And I don't know what came to the guy after that, but this is, this is the importance of this on and off ramp.

Eric: 00:12:33

But I think it's not only being on and off ramp.
Like Bitcoin is the first money that can be programmed, right?

NVK: 00:12:40

Yes.

Eric: 00:12:40

And that kind of allows a lot of permissionless innovation.
And I think that's what we're seeing here.
Like Bitcoin gave us permissionless monetary innovation and Lightning made it scalable.
For only Bitcoin, these e-cashmints would still be kind of isolated because they always have to go on chain to switch between them and to settle between them.
But with Lightning, we now have a superpower.
We have an instant settlement network between different kinds of e-cashmints even.
It doesn't even have to be e-cashmint.
Calle can be using Cashu, I can be using FediMint, and we can transact with each other.
While some third party runs their own Lightning Node in a fully self-controlled manner.
And they can still transact with us.
That's what freedom of transaction is really about like, and permissionless innovation.

NVK: 00:13:33

I want to get into scalability soon because, you know, Lightning scales only to a certain extent and I find that the eCash solutions are a huge deal because they can scale us to the 8 billion people after that.
We'll get there, but

## Technicals of ecash

who wants to explain e-cash technically?
Like, you know, let's give a proper explanation of what's actually going on under the hood.

Calle: 00:13:59

OK, I can jump in again.
So an e-cash system is a closed system.
You can basically imagine it lives inside this network of Bitcoin nodes.
There is this e-cash system.
And now this e-cash system gives out tokens that you can trade inside of the system, right?
It's inside money, outside money kind of thing.
So the way it works in Cashu, and I guess also like I'm gonna just explain it how it works in Cashu and Eric, you jump in whenever you need to correct me anything that is related to Fedimint.
So if you want the e-cash from Mint, you would ask them and hey, Mint, I want to have e-cash and mint would say basically, yeah, pay this Lightning invoice and if you pay this Lightning invoice, you give me your Bitcoin and I will give you e-cash in return basically that you can redeem later for this Bitcoin back.
So you get the e-cash.
Now the important part is the mint gives a blind signature on a piece of data that you gave to the mint before.
So what you as a wallet do basically is you generate random data, could be random, could be also committing to something else, but let's make it simple.
You take random data and you blind it with a blinding factor it's called, and then you send this blinded message to the mint and the mint now signs this blind message what you get is a blind signature.
It sends you back the blind signature and because you were the person who blinded this initial secret you can unblind this blind signature what you get is a signature on your original message.
The fact, you know, the important bit is the mint has never seen your original message, but it can verify the signature that it just gave you when you later show it.
Now, this disblinded signature and the secret message, sorry, the unblinded signature and the secret message together is the e-cash.
So when you put them together, you can treat it as a piece of money and it's a piece of data and that you can now send around basically in a network.
And you know, for the privacy, which makes this whole system extremely private is if I send e-cash now to Rijndael, and then Rijndael goes back to the mint and says, hey, mint, look, I have now this piece of e-cash that is worth half a Bitcoin.
I want it to be paid out onto the Bitcoin network again.
The mint doesn't know that this e-cash that Rijndael just redeemed back was the one that I actually created when I painted.
Basically there is no way to link the peg in to the peg out.
And with that, also all the transactions happening internal in the system are basically not traceable.
That gives it this fantastic privacy properties.

NVK: 00:16:20

So, you know, like you could say this, like, you know, like your mint, it mints out a bunch of say tokens with, you know, let's ignore the part that the other person gave a signature first.
OK, So essentially you have a bucket where all the mint tokens go in.
Anyone can take this token, trade with each other, as long as they're still the same kind within the same network.
Nobody knows who traded with who and how much those were worth.
That's like one of the best sort of anonymity sets that you get for using this technology within the same mint, with each other using the same token.

Calle: 00:17:01

I need to maybe correct here, at least in the signature scheme that Cashu uses, the mint knows the volume happening at each point in time.
I'm not sure if that's also the case.

NVK: 00:17:09

Well, and there is also your latest release with the news that we can get to in a bit.
But the key here is, if we just go back to like normal people here, you have now a money that as long as you're using with each other for the same kind of money and not going back to Bitcoin or Lightning, right?
Like you have like a nearly perfect anonymity set.
Right.
Like it's beautiful.
Like you really can't know who they are, how much they transacted.
But if you trust the mint, you know that there is a certain level of the distribution, right.
Of those tokens, right.
You know, the cap, you know, the volume of money that's in there.
Now, what prevents a mint from just creating a bunch of money, devaluing everybody's money in the current solutions?

Odell: 00:18:02

Before we get there, I mean, I think it's just really important to just why is why is this tech interesting?
Why?
Why should this tech be interesting to Bitcoiners?
And the reason is, is because no matter, you know, how strong our principles are about using Bitcoin as freedom money or using Bitcoin in a sovereign self-custody way, users ultimately want convenience and they want low cost.
And as a result, what we see is many, many users using custodial lightning wallets that give them no privacy, and that they have to trust with both custody of their coins and with their privacy.
So we see we see wallets like Wallet of Satoshi that are extremely successful.
So how can we improve that trust model if that's going to be the result of people using Bitcoin anyway?
And I think that is a key aspect that people miss.

Eric: 00:18:57

Yeah, and also like just if we have to trust someone, then we want to move this trust assumption more local to the people, like move it into their communities instead of to some random third party on a different continent.
Like that's one of the bigger problems I think generally with a third party custody, like that you don't have any reason to actually trust this other party.
And this problem is to some degree removed when you trust someone in your community.

NVK: 00:19:28

You know who to punch.
That's my sort of easy way of explaining it.

Calle: 00:19:33

Yes, so...

NVK: 00:19:34

Yeah, go ahead, Calle.

Calle: 00:19:36

Maybe also, you know, on top of the privacy that we just discussed, within the system itself, so you can do payments that are not correlated to each other, basically to the individual users.
Funny, fun fact, a mint itself doesn't have the concept of a user or the concept of a wallet.
It doesn't need to basically.
Like compared to regular custodial solutions where you would have a database with IDs, you know, Calle ID, NVK ID sends Bitcoin back and forth.
You would have to track that.
A mint itself doesn't even have the concept of a user or a wallet.
It basically just takes in Bitcoin, gives out e-cash, takes in e-cash and gives out Bitcoin.
That's the two main functions.
So even although, you know, not even, but on top of the privacy that you get by transacting inside the Mint, you also get a privacy by pegging out of the Mint because, you know, just it follows from that, that if you then tell the Mint, you know, I don't want this e-cash anymore.
I want to have it on my Lightning or my Lightning wallet.
You just give it some e-cash and the Mint doesn't know who you are.
So basically you can come in, then you are completely blind.
You're completely, you know, anonymous.
And then even on your way out, the Mint still doesn't know who you are, basically.
So there is no entering a password or whatever, signing in with some kind of ID.

Rijndael: 00:20:54

Yeah, there's kind of two anonymity sets at play here.
There's like the anonymity set of the users of the mint.
And so inside the mint, the mint operator can't tell who's trading with whom.
Because as Callie mentioned earlier, there isn't this big replicated ledger that everybody shares.
Instead it's your coins are what you have on your computer or in your phone.
And if I want to pay Odell, I hand him a blob of data.
He goes to the Mint to redeem it for a new blob of data.
So there's a database interaction there.
But just because Odell and I are trading doesn't mean that NVK and Calle need to update their local copies, right?
So it's more private.
It also scales more naturally with how we usually build computers and databases and networks.
So you have kind of good privacy inside the Mint.
But then also when you're interacting with the Mint from the broader, either layer one, Bitcoin or Lightning Network, all of the users of the Mint kind of ride on common rails in and out of the Mint.
And so to an outside observer, if you have a Mint with a thousand people inside of it, they can't distinguish individual transactions going from outside of the Mint to individual users inside the Mint, which is pretty cool.

Eric: 00:22:08

Yeah, it's a little bit more nuanced with Lightning still, unfortunately.
Sure.
Because currently in Lightning, we don't have a good way of providing privacy for the recipient, for example.
Like when I'm sending a transaction to someone from a mint, the mint might still learn to whom I actually send it.
I'm really looking forward to blinded paths for that, which are a fake part of Bolt 12, but also being explored independently now.
And that would fix the problem, I think.
And also there's this really interesting invention, I think, by Fiatjaf And I think Antoine, like the guy behind Simple Bitcoin Wallet, where they do the routing client side and only tell the Mint, or like they would be telling the Mint to forward the Onion message, or like the Onion payment, but they have already done the routing client side.
And that would be super interesting to implement, I think both for cashu and for fedimint.

Calle: 00:23:06

So you're probably referring to hosted channels there?

Eric: 00:23:09

Yes, exactly.
Hosted channels with eCash would be very powerful.

Calle: 00:23:12

Exactly.
Absolutely.
I also see a way there to improve it.

## Supply and auditability

NVK: 00:23:17

So where does the money come from?
Right?
Like how do people know the supply of the mint and that they're not being they're not being, what's the word?
Debased.
Debased.

Eric: 00:23:31

That has been all the rage on Twitter the last few days, I feel.

NVK: 00:23:36

No, I mean, like we know, right?
But like, how do we explain the different options of trade-offs that you can have, right?
Because there's a few different ways of going about this too, right?
Not every e-cash network or mint is the same.
There is different options.
So let's start sort of exploring maybe some of them.

Eric: 00:23:56

Yeah, so in my opinion, with all the research I've done, you cannot really have such an auditability without either reducing the privacy of the system or without introducing a zero-knowledge proofs where the users that are spending e-cash notes have to essentially prove that their node, that their spending is part of the issued set of E-cash nodes.
Like if you do either of these, you can totally have auditability in the E-cash system.
But for example, the ZKP route, if we wanted to keep the privacy and just add on some zero-knowledge proof, then that would mean the users would need to know about all the issued e-cash notes in existence again to produce these proofs, at least as far as I'm aware, like you might be able to build some multi-party computation protocol between the mint and the user where they can get some help in constructing these zero knowledge proofs.
But in the end, that would make for a much more complicated system, which is much closer to z-cash.
I think it would be close to z-cash, kind of.

NVK: 00:25:05

Yeah.
Okay.
So I think this is the important part for people to realize is that, you know, Bitcoin has the UTXO set that's public and kept by everyone and does not have blinded signatures because accounting for the money supply is Bitcoin's trade-off, right?
Like it's the most important feature that Bitcoin has.
It's kind of the whole point.
Now that whole point comes with privacy trade-offs.
Bitcoin will never have perfect privacy.
And that's the reason why we need this other second layers and third layers.
I'm, By the way, I'm putting ecash in a third layer.
So that, you know, you can find these other trade-offs based on different amounts and sort of like, you can have like a nice rainbow of trade-offs to pick depending on what you're trying to do as a user participating in this network and trying to make payments.

Calle: 00:26:06

Yeah.
So, I mean, we already have this problem in Lightning itself.
So it's very easy to prove how much money you have on chain, right?
You publish a proof of reserve.
Everyone has been doing it who runs an exchange these days, basically.
But even on Lightning, Wallet of Satoshi, let's take it as an example again, cannot prove that they have the Bitcoin that they say they have.
Like, let's imagine we know every user's balance somehow.
We tally it all up and we know it's this amount of Bitcoin.
Now we go to Wallet of Satoshi and say, prove us that you have this Bitcoin.
They can only point to their channels and say, look at these channels, but in these channels we don't know what their balance on their side is basically.
So we have this kind of problem there already.

Eric: 00:26:48

Yeah.
At least you would need the cooperation of the channel peer to sign a message essentially that states the current balance because of like the problem of

Calle: 00:26:56

all channel peers.

Eric: 00:26:57

Yeah.
Yeah.
Yeah.
Of all channel peers to have a sum of all these channels.

Rijndael: 00:27:01

Well, and it's an instantaneous, like, balanced snapshot, right?
You'd have to continuously roll

## Is ecash the third layer of Bitcoin?
it.

NVK: 00:27:07

I saw some faces when I mentioned a third layer.
Yeah,

Calle: 00:27:12

we can go into it later.

NVK: 00:27:13

Yeah, no, and I think it's important because and I guess I'll explain why.
At least I see it that way.
So Lightning is still sort of moving UTXOs, right?
It's just choosing when, but it's still sort of using a Bitcoin UTXO, while eCash, not really.
So I kind of feel like the third layer is sort of like is leveraging Bitcoin, but it's no longer Bitcoin.
While Lightning is Bitcoin, but kind of not sometimes.

Calle: 00:27:41

I don't know.
I want to be extremely pedantic about this.

NVK: 00:27:44

Please do.
It's a good one to argue about.

Calle: 00:27:46

If you say it doesn't have to be Bitcoin and then it can be layer 3, basically, why not layer 5?
Right.
I would ask you why it's not layer 76 then.

NVK: 00:27:55

Well, it could be if you have another two layers of e-cash.

Calle: 00:27:58

Yeah, what is that?
Is that the web interface to use the e-cash?
And is that the mail envelope in which I send my e-cash in an SD card.
It becomes quickly, it really dilutes the definition.
So for me, I am extremely pedantic about it.
I invite everyone listening to be as pedantic as I am.
To be a layer of Bitcoin, two main things have to be met is first, you have no other way of measuring the money.
So it must be denominated in Bitcoin, whatever this new layer is.
And second, in case of a conflict, you must be able to almost always fall back to the layer below in case of conflict without having to ask anyone's permission.
In Lightning we have this, right?
So if your channel partner cheats on you, then you just say, no, here's a punishment, you go back to on-chain, you have your money.
Now, for me, a layer three, let's say it would be built on top of Lightning, would have to obey to this rule as well.
So that means in case I don't, I don't know, you don't honor my e-cash, I would have to have some kind of mechanism to get my money on Lightning, at least on Lightning without having to ask you nicely whether you want to cooperate or not.

NVK: 00:29:08

I think for me, the layer three is no longer Bitcoin.
I feel like the layer two is where we have that rule set that you described.
Right.
So you have to go in and out.
You have to be essentially clearable to UTXOs. Right.
Now, layer three is something that is leveraging Bitcoin.
It's leveraging Bitcoin's truth, but it's not necessarily like it doesn't have to be Bitcoin.
I guess that's sort of like where we differ.
Like we differ.
And I think like many other things are going to come that are not necessarily payment channels.
So Lightning, right.
That could also serve in the layer two place, which are redeemable for Bitcoin.
But I think layer three is where the, you know, the loosey goosey sort of like whatever is connecting to Bitcoin, let's put it this way, somehow lives.
And that's sort of like a very sort of broad space, right?
I mean, maybe Visa decides to like, you know, use Lightning ins and outs somehow.
And, you know, to me that's them using Bitcoin that to me is layer three.
So yeah, I mean, I share, I agree with your explanation.
I just don't think that that's the actual layer.
Let's put it this way.

Eric: 00:30:24

Yeah, also from a FediMint perspective, like this layering discussion is even more complicated.
I think Cashu builds directly on Lightning, right?
You don't even deal with on-chain Bitcoin right now.
But with FedMint, the federation holds on-chain Bitcoin.
And then through some elaborate protocol, we incentivize some external third party that cannot cheat the users to make Lightning payments for them.
So if you were to think about it, like does it build on Bitcoin or does it build on Lightning?
You cannot really tell which one it is.
So maybe your layer three definition would be much easier for us to deal with because it's much looser.
Everything is a layer 3 essentially.

NVK: 00:31:09

Yeah, anything that sort of goes in and out of Bitcoin to me is like layer 3.
It's like, it's just, you know, you're really just floating on the top of it.
Like you're just leveraging it.

Calle: 00:31:17

Anything goes man.
That's right.

Rijndael: 00:31:20

I mean, I'm going to argue that it's actually not a layer of Bitcoin at all.
Right.
Because like in my mind, layer two is you take Bitcoin transactions and you apply some other protocol for how you compose these Bitcoin transactions together, right?
So like Lightning, you have this extra layer of networking and extra layer of semantics on top of like, how do we update a particular shape of a Bitcoin transaction?
So a layer three would be, let's take a layer two like Lightning and apply some extra protocol on top of it for how we compose particular Lightning payments together, for example.
I would say that these ECash systems that have Lightning compatibility are separate systems that have lightning compatibility, use lightning to move money in and out of them.
But, you know, a Cashu mint is not itself composed out of lightning.

NVK: 00:32:08

You know, the best way I like to sort of like make it very simple for people to understand second layer is that you're using essentially zero confirmations in a way, right?
Sure, the parties may be confirmed, whatever, but like, but you're not leveraging a on-chain transaction for finality yet.
Right?
So that's why It's like a softer, you get all their benefits, many of them.
Right.
But you're not truly relying on that on-chain transaction for your transactions, for your trade, not your transaction, for your trades finality.

Rijndael: 00:32:44

Yeah.
I think all Bitcoin scaling solutions ultimately involve how do we not publish this on-chain transaction until as far in the future as possible.

NVK: 00:32:55

How do they not take four megabytes?

Rijndael: 00:32:57

Yeah, exactly.
And then the trade-offs are just What guarantees do you get between when somebody hands you the sandwich and when the transaction actually goes on chain?
And with Lightning, that's one set of tradeoffs.
With eCash, it's a different set of tradeoffs.
With Liquid, it's a different set of tradeoffs.
And It's what do you do between exchange of goods and actual transaction finality on Bitcoin.

NVK: 00:33:19

Calle, before we move on to something that I want to explore, I want to give you the final word on the pedantic version of the layers.
You get the final word.

Calle: 00:33:29

So, yeah, I just as I said, I think we need very, very strict definitions here because people start just making up these words and advertise their projects or whatever.
There's so much bullshit going on just because we don't have these words fixed.
So if you hear stuff like that, be a bit cautious.

## Cashu

NVK: 00:33:48

Thank you.
So I think this is a good place for us to start exploring the two implementations of eCash that actually have users and are sort of like playing around.
And so Calle, why don't you start like explaining to us what like Cashu is, and then maybe we have Eric explaining what FeDI is, or FediMint, and then we can discuss some of the trade-offs and some of the differences.
That could be a good launching point for people to understand this a little bit better?

Calle: 00:34:18

Yeah, so Cashu is basically, the idea of Cashu itself is to be a simple to implement protocol that allows you, if you run a custodial service, to just take out all the legacy custodial stuff with the database where your users are stored and stuff.
You just rip it out and you replace it with a protocol like Cashu.
And so we're trying to build this protocol that is extremely easy to implement and that allows you to take Bitcoin from your users in and give them e-cash out.
And so this works quite easy.
You can, for example, just, I'm gonna make one example of where this might be useful, is you have an API endpoint, for example, and it gives weather data, let's say.
And your business model relies on, you have to ask your users, pay me this lightning invoice, and then you have 500 requests.
You can make 500 requests and I will give you weather data 500 times, right?
So what you need to do is you have this database of user IDs and it says 500 requests for this users and then you tell it this database.
Now, I imagine Cashu as something that you can take out the system and replace it with this eCash and say, you pay me this invoice and I will give you e-cash in return.
I don't remember how many requests you have.
You get the e-cash.
Now, when you want to make a request to this API endpoint, you include a little bit of e-cash in your request.
So basically, like back in the days, you write a letter and you would put in the stamp for the response into the letter, basically.
That's basically how I imagine it.
Allows you to build these very, very simple applications where you can just replace the custodial management of funds with an e-cash management.

NVK: 00:36:07

So you would say like in a real world scenario, I like your one time you gave this explanation, say for example you have a school and you want to essentially provide a way for people to pay each other.
Maybe it's to like buy and sell the books around and, you know, use the cafeteria and, you know, that sort of like a small money network.
Right.
And maybe they're not like, you know, rich enough to have Bitcoin, right?
So you could use, the school could be the mint and then have its own monetary system that does go in and out of Bitcoin with lightning.
That's how we get in there.

Calle: 00:36:44

Yeah, exactly.
And I deliberately chose this API example just to not make it a physical community.
But obviously, I mean, there are digital communities, I don't know, a Telegram channel or fans on the Internet or something.
But there are these physical communities as well, like a school, like a village, like a conference hall or something where you would want to have this internal money system.

NVK: 00:37:06

Would you say that this would be great for a poker website, trying to do poker chips very fast in an accountable and private way?
So it's much better than using a database, but still a single point of failure, right?
That this single issue or the single person to punch.

Calle: 00:37:22

Exactly.



NVK: 00:37:24

It would be terrible for a dark market, right?
Because the dark market now has a single point of failure and there is no enforcement on how to clear this back to Bitcoin if there is a failure there because it's e-cash.
Yeah, it's just sort of like two kind of digital examples of this to me is a great way for websites to replace a database of tokens.

Calle: 00:37:46

Yes, absolutely.
And I'm not even sure about the dark market.
So I think there are dark markets out there that have a balance.
So you basically pay the dark market, then you have a balance on a sheet, and then you buy the goods and it gets subtracted from your database entry and added to the seller.

NVK: 00:38:04

Oh, nowadays it could be unpasteurized milk, dark market, right?
I mean, like you don't have to go far.

Calle: 00:38:08

Exactly.

NVK: 00:38:10

So or vaccine papers.

## Fedimint

So, Erik, do you want to now, like, explain to us a bit about FediMint and what's sort of like, what is it, what the goal is and like the more complicated stuff you can do with it.

Eric: 00:38:24

Yeah.
So fundamentally, I think both projects started with the same insight, kind of, that eCash is a really powerful system to build transaction systems and that we can now build such a system on Bitcoin because Bitcoin allows permissionless innovation.
But the difference between Cashu and FediMint lies in the fact that with Cashu, you still have a single point of failure.
So it's much easier for someone who runs such a system to run away with the money and rug pull all the users or being pressured by a third parties to do so.
And for Fedimint what we achieve is we split the trust or multiple people.
Like when I speak about a federated system, it means there are N people, let's say four people, and as long as T of them, in the case of four, it would be three, as long as three of four people are honest, the system keeps running according to the protocol.
And then once more people go bad or become malicious, then at first the system stops working.
And in the worst case, if let's say three out of four of these people become malicious, then they could actually steal the money.
And what allows you to do is in a community where you have some relatively high level of like trust, but not ultimate trust.
There's probably for most people only one person they trust ultimately, which is themselves, or maybe not even that.
In that case, you can take some really high trustworthy people out of your local community and they become your Lightning service provider, essentially.
And they issue you these e-cash notes.
You can redeem them with them, pay Lightning invoices or pay internal invoices between each other if you're in the same community.
And that gives you this really scalable system to use Bitcoin in a world where hyperbitcoinization happens essentially, because people did the calculations.
It's infeasible.
First of all, on the technical level, it's infeasible to onboard 8 billion people onto Lightning.
It would take years and we couldn't do anything else during that time.
So that doesn't really work at least as of now.
And the second point is we already see it.
Matt mentioned that most people using Lightning do so in a somewhat custodial way.
Like a lot of people are using Wallet of Satoshi.
Like the slightly better alternative is a Bitcoin beach wallet where they already have this community custody concept in place, but it still allows these operators to see everything that's going on.
And like an interesting observation there is the closer you move the trust, like for example, If you have your neighbors operate your lightning node for you, then you really don't want them to know what you're spending your money on.
So that's why the privacy aspect, at least in my opinion, is even more important when we are talking about these localized systems.
It's not that bad, at least in a social context, if some random Coinbase employee knows that you have bought some porn magazine, but it's really bad if your conservative neighbor knows that, who is running your local e-cash mint.

Rijndael: 00:41:47

Yeah.
I think there's been this thing that we've talked about for a couple of years about the way that Bitcoin is going to scale, not only in terms of technically, but also in terms of like usability is that you'll have your neighborhood Bitcoiner who runs like the Uncle Jim lightning node, and then like all your friends and family use your node.
And, you know, do you really want that person like knowing everything that you're spending your money on and like all of- 

NVK: 00:42:11

We have nothing to hide.

Rijndael: 00:42:13

Yeah, right, exactly.
And so, you know, something like Cashu or FediMint is a strict upgrade for that system.
And if you think about, you know, other things like I use Stacker News, right, to like upvote posts or I use the Fountain Podcast app, It would be better if even though that's a custodial system, if I had some privacy about what things I'm exchanging my stats for or who I'm sending money to in those systems.
So I think a lot of people look at something like cashu or fedimint and say, Oh, like, you know, I'll keep my Bitcoin in Bitcoin.
You know, thank you very much.
And like, this isn't a replacement for lightning.
This isn't a replacement for Bitcoin.
This is a upgrade to custodial systems that people are already going to use, both for usability and privacy perspectives.

Eric: 00:43:05

I think Second Use is actually a perfect example because to have true freedom of speech and freedom of expression, you need some level of privacy.
Otherwise, there can be all sorts of crew pressure and social phenomena that you won't actually use your freedom of speech.
So having some private way of like, what do you do on second use?
It's essentially you upload posts that you think are insightful, like without that you don't get the true signal.
You get what people think is acceptable.
And yeah, so integrating some sort of ecosystem there would be really powerful.

NVK: 00:43:41

So let's get a little bit more in there.
Like, how does Fedimint actually work?
And how are you, you mentioned that you guys are going to use a base layer somehow and, and it is federated.
So like, why don't you explain to us a little bit of like, how, how you actually accomplishing these things technically?

Eric: 00:44:00

Yes.
So basically what a Fedimint Federation is, it's a group of people that run consensus algorithms between each other.
It's a lot like Bitcoin, but since we only have a limited set of people that participate, we can use, not proof of work, but some other Byzantine fault tolerance algorithms.
I don't have to go into that, but essentially what they lead to...

NVK: 00:44:22

Oh, please do.
This is the podcast to do it.

Rijndael: 00:44:26

Yeah.
Are you guys still using Honeybadger BFT?

Eric: 00:44:28

Yeah, we're currently still using Honeybadger, but we have some Bitcoin intern actually, who wants to explore different BFT algorithms that are a bit more efficient and that scale better to larger federations.

Calle: 00:44:42

But Eric, why don't you really explain that to us?
Because I think it's very interesting.
What you achieved is insane, by the way.
It's an insane achievement.
I must say that because it also kind of replaces some of the federated sidechain ideas that are, you know, you can have a sidechain without a blockchain kind of way, innovation that I think of it.
So why don't you explain to us the Honey Badger BFT algorithm that you need to have this federated signing of eCash?

## Federated signing and sovling the double spend problem

Eric: 00:45:10

So maybe I start with stating why we even need that.
Like the fundamental problem we have with any federated system is if Alice has some money and wants to pay Bob, then we would send this transaction to all the federation members, right?
Like Alice would create a transaction, sending money to Bob and giving it to all the four Federation members.
But that's the happy case.
Like that's if Alice is actually honest.
But what happens if Alice in one transaction pays Bob and in the different transaction pays Charlie and then gives these two transactions to two different sets of Federation guardians, like these people running the Federation, then what do we do?
We have a conflict there.
And to solve this conflict, essentially what we do is we create deterministic ordering of these transactions.
So a BFT consensus algorithm is everyone, like each of the four guardians in the federation can contribute transactions to the consensus.
And then at the end of it, a subset of these transactions is chosen, put into a deterministic order, and then you just process these transactions.
And for example, if Alice wants to double spend, then the first transaction goes through, and the second one is canceled, because we know it was already spent.

Calle: 00:46:28

So if I can ask a question, and You can correct me, but because I think this is the real point here, is when you have a system where you have, let's say, a three out of five, right?
You need three confirmations and the two you don't need.
So you have this e-cash and now you want to spend it and you only show it to three of them and two others never see it.
And when you do this like three times, you can double spend an eCash node because you can pay it, you know, to show it only a subset first and then rotate and show it to the next subset and rotate to a next subset.
And what you end up with is at the end an e-cash note that you have shown to one subset, but also have spent to another subset.
So that is the problem that you need to solve, basically.

Eric: 00:47:13

Yeah, like in the e-cash case, that's the specific problem there that you can actually create money out of thin air.
If you have this, it's called equivocation in the literature, telling different sets of the system participants, different truths.
And to prevent equivocation, you equivocally use consenus protocols to make sure everyone's on the same page.

Rijndael: 00:47:34

Well, and something that I think is really important to think about, especially like a lot of people from different backgrounds listen to this podcast.
There's a really classic article I think came out of Sun Microsystems, there's a Wikipedia page about it now called Fallacies of Distributed Computing.
I think everybody should go and read it.
Basically what it comes down to is that computers and networks are a lot crappier than we like to imagine that they are.
And you can have arbitrary network partitions, you can have arbitrary latency between two links in a network without it impacting the entire network.
And any time you have a distributed system where lots of nodes all have to come to agreement on the same answer, you have to account for these things.
And you have to deal with the fact that like in a five node federation, maybe all the nodes can talk to four of them, but then like two of your nodes can't talk to each other.
And you can't tell the difference between a failure from just networks sucking and from somebody attacking your network.
There's a whole list of these things.
It's called fallacies of distributed computing.
You know, people should go and read it.
But it's important that, you know, your system can deal with just intermittent network issues, as well as active attempts to double spend.
The way that Bitcoin handles that is through proof of work and Nakamoto consensus.
But since something like Fedimint has a different operational footprint, they have to handle it differently and they can make different tradeoffs.
And right now they're using a algorithm called Honeybadger BFT to do that.

NVK: 00:49:04

So just sort of like simplifying this, like the way you're finding, the way you're proving that it was not double spent essentially is by bundling in a deterministic transaction.
And because it's deterministic, you can't cheat.
So that gets canceled if somebody else tries to double spend in a different round or rotation.

Eric: 00:49:31

Okay.
So like what the BFT contenders gives you is like, first of all, everyone gets the same transactions, like everyone gets the same output each round.
That's like the most important thing.
And secondly, when there are multiple rounds happening after each other, you also get the deterministic ordering of these transactions.
So you cannot connect to two of the guardians and tell them, hey, I want to first submit this transaction paying Bob, and then the transactions paying Charlie, and the second one fails because I'm double spending and like giving these transactions in a different order to the other two peers.

NVK: 00:50:09

So it's the order, sorry.

Eric: 00:50:10

Yeah.
Like, I mean, the order is important because it determines like which one gets canceled, right?

Rijndael: 00:50:16

Right.

Eric: 00:50:16

And, but also it doesn't work without everyone having the same view on the outcome, right?

NVK: 00:50:22

Okay.
So you've sort of put together a great way of, of having a better, I wouldn't call it a proof, but a better assurance that you have not created or paid, double paid somebody, right?
You have not double spent.

Eric: 00:50:39

The cool thing about the BFT consensus on Fediment is that after you have achieved BFT consensus, you can pretty much think about the system as if it was a completely centralized one.
Because after that point, if all your further operations are deterministic, like just deterministically applying functions on top of the output from the consensus, then don't really have to think about it being a distributed system all that much anymore.
Like there's still some special cryptography you need.
And we can get into that because that's like one of the bigger challenges that I faced with FediMint.
But the cool thing is after you have consensus on which transactions happened in which order, it's not a not really distributed system anymore you're thinking of.
And that makes it much easier conceptually.

## Fedimint tradeoffs

NVK: 00:51:26

So please do go in there because, you know, if this was perfect, right, we wouldn't need proof of work.
So there is some trade-offs that are made.

Eric: 00:51:35

Right, right.

NVK: 00:51:36

And that's, I think it's important part for us to get into.

Eric: 00:51:39

I think we can get us out of the way rather quickly because like proof of work was enormous innovation because these BFT algorithms or BFT consensus algorithms, they only worked for a known sets of participants up to the point where Bitcoin was invented.
It was an unsolved problem how you can have an open set of these participants and consensus systems without totally failing.
And Bitcoin solved that through proof of work.
And with Federation, you have just a different problem.
You know the people that are participating.
So you can use algorithms that are more efficient, I'd say, that have lower latency, like Bitcoin has the 10 minute block time, with FediMint we go down to like a second or a little bit more than a second.

Calle: 00:52:26

But do you think it is fair to say, because I'm really bullish on FediMint in that regard, so since for example, the liquid sidechain I think uses a similar consensus algorithm among the guardians of the sidechain to come to a consensus of the new state of the sidechain, right?
But What they did there is basically to have the blockchain and Bitcoin, then we have these guardians holding money from that blockchain in a multisig and processing on the side something that is again a blockchain.
I see FediMint, and please correct me if I'm wrong, as a way to get rid of the sidechain and have very, very similar properties.
Basically, you can still have this multi-sig where you put the money in, but instead of just rolling over a state over and over again in a block versus block versus block, you can even have scripts and all the other features of a sidechain inside this much more anonymous and completely differently built system, an e-cash system.

Eric: 00:53:24

That's actually gets into how Fedimint got started.
Like when Liquid was released, I saw it and it was amazing because it didn't occur to me you could have this multi-sig wallet with some BFT consensus running between all the Guardian nodes and then implement anything you want on top of that.
And it would be somewhere between a centralized solution and a fully decentralized one.
It gives you this trade-off.
But I was thinking, why is this even a blockchain?
Because the guardians could cheat at any point in time.
They could just run away with the money if they were malicious and you could see it, but you couldn't really do anything about it.
And at the time I was also learning about client signatures and cryptography in general, and was like, okay, if we could build such an old Chaumian ecosystem in a federated way, that would be so awesome.
Like we'd still have the multi-sig wallet that keeps the Bitcoin, but then instead of having another blockchain, which is like a really inefficient data structure in many ways, that has to be validated by clients.
We just issue these e-cash notes and people can use them to pay each other.
At that point, I wasn't really aware of how to integrate with Lightning later on.
But it would be a really private way to transact inside your community.

Calle: 00:54:44

So looking at Cashu and Fedimint, I, every day more, I think that shit coins probably don't need their blockchains either.

Eric: 00:54:52

We made them irrelevant.

NVK: 00:54:54

They never did.
I mean, you know, they would have been better in Pulsegrass, but you can have like, you can have signed roles.
So anyways, so, okay.
So let's, let's explore this a little bit more.
So like, this is good, right?
Like we're trying to get to here is like, it's why do we need this?
Because we're explaining the actual technical trade-offs of like Bitcoin efficiencies and inefficiencies versus this, right, and we've explored Cashu, which is a simpler sort of version of this, right.

## How does the federation work?
So how does the federation works on Fedimint?

Eric: 00:55:28

Okay, so for federated e-cash, like Fedimint has grown into kind of a federated application framework by now, but for the federated eCash use case, we have two sides.
Like on one side, we have a multi-sig wallet, which keeps the Bitcoin on chain.
And on the other side, we have eCash Mint, which issues threshold signed eCash notes.
So instead of using a blind signature scheme, we're using a threshold blind signature scheme where a certain number of the guardians has to cooperate to issue these signatures.
So you're still generating your random number as a client, you're still blinding it and giving the blind random number to the federation, but then the federation engages in a multi-party computation protocol that generates a blind signature for the nonce.
The particular protocol used is like special BLS blind signatures, like based on pairing cryptography.
It's a pretty straightforward protocol actually compared to other ones, because it's only like one round.
Every Guardian generates the blind signature share, they exchange them, then they get combined.
And as long as we have T out of N of the signature shares, we get a combined planned signature and that's sent back to the client who can use the blinding key to unblind it.
And now they have like the random number, which we most of the time call a nonce and the signature and the nonce signature pair is the e-cash note, which you can now just spend like a Calle already explained.

Rijndael: 00:57:05

So, sorry, that's really interesting.
I didn't realize that you guys were doing MPC for computing the blinding factor.

Eric: 00:57:10

I mean, it's, it's no, not applying factor.

Rijndael: 00:57:14

Okay

Eric: 00:57:14

I mean, you can, a few, a blind signature generation on the server side is kind of MPC.
I mean, in the end, it's just generating the signature shares and combining them.

NVK: 00:57:25

Would there be any advantage really of doing MPC for the blinding factor?

Eric: 00:57:30

No, not really.

NVK: 00:57:31

No, Right.
Yeah.

Eric: 00:57:32

I mean, maybe in the future,

## Fedimint denominations problem

like one thing we haven't gone into really yet is like the biggest problem I have with FediMint right now and that Calle probably has with cashu here is that we need different denominations for our e-cash notes.
We could have like e-cash notes that are always worth like one satoshi and that would scale horribly because suddenly you'd need like millions of e-cash notes just to pay like a few milli bitcoin.

Calle: 00:58:01

Megabytes of e-cash notes.

Eric: 00:58:04

That doesn't really scale.
So what we'd probably like is e-cash notes that commit to the amount they represent and commit to it in a blind way where we can have proof that when you have a transaction, that the input eCash notes have the same value in total as the output eCash notes, like a lot, like confidential transactions on Liquid.

NVK: 00:58:26

You know, I hear a denomination on the tokens that I'm like, oh, those are sats cards with e-cash tokens on them that then could be redeemed, right?
Because like, all you have to promise is that you're keeping it secret.

Eric: 00:58:40

Right.

NVK: 00:58:41

That could be a funny thing.

## How is a federation formed?
Okay, so How is a mint formed and how are the federated, like each, like the actors of the federation chosen?
How do I go about starting a federation on Fedimint?

Eric: 00:58:58

So there are two parts to it.
Like The one that's closest to what I'm working on each day is the technical part, where we assume we already have a set of people, like for example, four people.
And then we just run the Fedimint daemon.
It opens a port where it can connect to WebUI.
Then you have to exchange some, like essentially, your IP addresses and your ports that you're running on.
You have your group of friends.
You all know each other's telegram or signal handles.
You just exchange this information.
And then FediMint engages in something that's called a distributed key generation protocol where all the keys necessary for issuing these planned e-cash notes are generated.

NVK: 00:59:43

How do you prove, How do you prove that I'm not generating, say, three keys on my local system, pretending to be three different systems?
Because, like, let's say we're all unknown to each other, right?
Yeah.
And, say, Matt is going to be one key, Calle is going to be a key, Eric's going to be a key, Rijndael is going to be a key.
And I'm going to pretend that there's another five guys you guys don't know about.
Okay.
And I'm going to just, and I'm going to add them all and I'm going to be their sock on Telegram.
Right.
And I'm going to pretend I'm all of them and I'm going to cyborg this network now.
How do we prevent that from happening?

Eric: 01:00:19

Like that's a problem that cannot be solved in the technical realm.
Like there we have to go into the social realm and get different solutions.
Like when we're talking about like big online communities, then it's much harder to really guarantee that.
And you probably have to go by activity.
Like if someone is not really active, then I guess they have a higher likelihood of being a sock puppet.

NVK: 01:00:44

So What you're describing is that this is a limitation of FediMint, right?
Like you have to have a certain threshold of trust with the parties that you're entering into a federation with.

Eric: 01:00:57

Yes.
And that's what,

Rijndael: 01:00:59

well, If you want to have a civil resistant open set of validators, then you add proof of work.
Yes.
Like that's essentially Bitcoin.

NVK: 01:01:08

Exactly.
Yeah.

Calle: 01:01:09

Don't reinvent Bitcoin.
Don't reinvent Bitcoin.

NVK: 01:01:12

That's right.
So we're degrading, right, that a non-anticipable defense mechanisms that Bitcoin have, right?
So that it can coordinate truly being a non so that we can have this efficiency, right?
And jumping to a non-proof of work Algo as a federation.

Eric: 01:01:33

But like, that's also why one of the most promising use cases is communities, like physical communities where you actually know the people that-

NVK: 01:01:43

You know who to punch.

Eric: 01:01:44

Yeah, exactly.

NVK: 01:01:46

I know, seriously.
It's, yeah, it's this best feature of the protocol.
So you know who to punch when the money disappears. Proof of punch.

Eric: 01:01:53

Proof of punch.
Yeah.
And so that's why a lot of focus is currently on communities that A, have a need for some sort of Bitcoin banking system, and secondly, that have this tight social connection still.
In the West, we often lack that, But for example, in the global South, it's mostly still intact.
Like their local communities where you have a whole village that essentially knows each other.
And like if they're like four village elders or like four, probably not elders because they need to run some good little computer software, but four people that enjoy high trust in their community, then yeah, you can spin up a FediMint.


NVK: 01:02:39

Well, I mean, it's better than being a single signer, right?

Eric: 01:02:42

Yeah, exactly.

Odell: 01:02:42

The elders kids.

NVK: 01:02:44

That's right.
So you have like three people, right?
Ideally or something like that.
Minimum, you'd say like at least three people to start somewhere with a little bit of a better sort of a single point of failure resistance.

Eric: 01:02:57

We generally, actually, we generally require like four people or seven people.
Like it's a little bit different than with Bitcoin multisig.

NVK: 01:03:05

Why is it four instead of three?
I'm curious.

Eric: 01:03:08

Yeah, there is actually a theoretical proof for asynchronous Byzantine fault tolerant consensus algorithms that if F is the number of maximum malicious peers and N is the number of total peers, then N has to be greater than three times F, like greater.
So it's at least three times F plus one.

NVK: 01:03:34

Okay.
So

Eric: 01:03:35

you cannot have any better algorithm if it should work in asynchronous network conditions.
So that's why we went with that.
And it gives us the best reliability and like the, it makes it the most bulletproof essentially.

## Comparing Fedimint to liquid



NVK: 01:03:49

So, you know, one of my biggest criticisms of Liquid when it came out was the fact that you couldn't bootstrap a federation, a competing federation, which in my view, killed the project.
And you ended up with just sort of, you know, exchanges are using it right now, but they use it between each other and sort of like, it's not like, they're just using it like as, as, as, as they could have used just Pulsegrasp, right?
Like, so a huge part of having non-proof of work systems is its replicability in terms of competing groups, chains, right?
For lack of, it's not a chain, but competing pools.
So you know, I found that like when, you know, you guys launched the project, I'm like, okay, well, this is great.
They're already starting it right, at least that part, right?
So, sorry guys, one second here.

Eric: 01:04:40

I think that's also a central point of Fedimint that we don't aim to have like this one federation to rule them all, but rather deploy a lot of these small federations in their local communities so that there's no systemic risk to Bitcoin, essentially.

Odell: 01:04:59

And to take that thought a step further, the Fedimint project, and I would say maybe Chaumian Mints in general, rides or dies on how easy it is to roll up these servers whether that's a single SIG server or if that's a federation server like that needs to be as easy as possible.
Otherwise there will not be competition.

NVK: 01:05:21

Sorry, my kids were ringing the bell.
I thought it was a delivery that's important.
So another issue was, you know, producing, implementing a liquid HSM is not a simple task.
It's very hard code to write that was also not open.
Right.
What I'm seeing here now is you have similar systems in terms of purpose that offer like a substantial improvement in easiness of implementing, deploying and it seems like an evolution of that protocol in terms of like, not technically they're different, but in terms of like better sets of trade-offs and better efficiencies, because again, it's not a blockchain, while Liquid is.
And I think you guys are doing that like right.
Is this how you guys thought this through?
Is it like the one button deploy, mint one button deploy, pull kind of the idea?

Eric: 01:06:18

Yes, we are working a lot on making it as simple as possible.
And I think later this year, we will also try to integrate with some of the node packages that are out there.
So people have even easier time setting it up.
Currently it's still under heavy development, so it doesn't make as much sense to do that yet.
But we already have a really convenient web interface.
And yeah, it's really just five minutes setting it up.
Like over the last months, I did a bunch of workshops showing people how to set up FediMint.
And yeah, it's after a while I got into like a habit where I could do it in like five minutes essentially and then you have a federation running.
And regarding your comments about Liquid, like I have huge respect for the people who built it because they were first movers.
They had to essentially find out a lot of things for the first time and FediMint has profited enormously from these learnings.
So for example the HSMs, they are really good for some really long tail events, like for some really complicated hacks that someone could try to pull off, but they also make it really hard to iterate on the code.
Like it makes it so much harder to upgrade the system that uses HSMs. So for Fediment, for now, we are saying like, no, we don't do HSMs. Like we keep it simple and we want to iterate.
We want to get people to play with it rather than building like the perfect thing that's maybe ready in 10 years.
Like that's the trade-off too.

## Ease of use setting up a mint

Calle: 01:07:55

Yeah regarding the ease of setting it up that Matt just made, I think that is a very critical point actually and also something that I learned actually a lot from Ben Ark himself, the creator of LNbits.
LNbits is very influential in that sense that it allows, You know, the dream of being an Uncle Jim, literally just a couple of clicks.
So you have your lightning node and then you set up this magic piece of software that allows you to infinitely generate wallets and give them around in your subnet basically, or in your community, family, whatever.

NVK: 01:08:30

With trade-offs.

Calle: 01:08:31

With trade-offs, Obviously with trade-offs, but his argument was always, and that is something that I very much agree with, is that if you make it easy enough to deploy this on a wide range of locations on the planet, it becomes impossible to kill.
And I think that is the strength of ease.
So something that often in developing software, people also tend to forget, you know, that adding features makes it powerful, but making it extremely easy to use and to set up gives it a completely different power, which is that many people will be able to adopt it, which makes it resilient against attacks and so on.

Rijndael: 01:09:09

Yeah, it also, I think it's really important for the customers or the users of a particular mint to have a credible, easy exit path.
Right, like if I set up a Cashu mint or a feta mint with like my local community or like my local BitDevs community, and then I start, you know, abusing the members of my mint by withholding withdrawals or by putting sauce on my steak or whatever the thing is.
If anybody else in the community can click two buttons inside of LNbits and spin up a new mint and say, Hey, everybody, you should leave that mint and you can leave over lightning.
If you should leave that mint over lightning and come to my mint that I just set up in five minutes, then you know, the, the pressure is on me as a mint operator to behave in a trustworthy way because like there's marginal switching costs for all of the members of my mint.
If it's very expensive or very hard for people to run competing mints, then I end up with like a natural monopoly because nobody's gonna compete with me.

## Running a federation/setting up a mint


NVK: 01:10:14

What's the security requirements and thresholds for you to run, to be a member of the Federation?
Like, can you just use your general purpose, like everyday computer, or like, do you need the proper HSM for this?
Like what's the security threshold here?

Eric: 01:10:33

For FedElement, you don't really need any special hardware.
Like you can just use a normal-

Rijndael: 01:10:38

Can I run it on my computer?
What happens if I get hacked?


Eric: 01:10:41

That's why we have this threshold.
Like if only you get hacked, That's not a problem.

NVK: 01:10:45

Is it easy to rotate the keys?

Eric: 01:10:48

Not yet, but it can be made rather easy.
Like you just run the distributed key generation algorithm again, and then you just move all the funds to the new federation.
That's in theory, not a big deal.
It's more of an engineering challenge.
So we haven't gotten to it yet.

NVK: 01:11:03

But it's huge.
Yeah.
It's huge because it's super low barrier of entry, right?
It means I can run a shitty digital ocean VPS where my signing is done on a certain threshold that I policy that I put there.

Rijndael: 01:11:16

I don't know if this is still the case, but like a year ago, the bootstrapping script that came with Fedimint would run, I think it was four nodes, and then one of them was like actively crappy.
And it like would, Like that was a way of exercising the...

NVK: 01:11:32

So it was a Windows machine?

Rijndael: 01:11:34

Yeah.
Anyway, so like you can see the BFT doing the right thing.
Like that's why you have three out of four.

Odell: 01:11:41

First of all, I mean, I think at least in the beginning, most people will be running it on, you know, different cloud server instances, particularly because I mean, Tor is fucking unreliable.
So if you're running it at home, you're exposing your IP address of the federated server.
But to what Rijndael said, I think it's an important point to mention, There's two different aspects here, right?
It needs to be easy for people to run these servers so that we have competition.
That's more on the open source Fedimint protocol or on Cashu's protocol, right?
Like anyone should be able to run the servers.
But then, in terms of switching costs, that's going to be a front-end problem to solve.
There's going to be many different front-ends.
One of the front-ends is being maintained and shipped by Fedi, Eric's company.
There'll be many different front-ends, But what's kind of cool about how they're looking at it is this idea of easily connecting to multiple different Fedimints from one front end.
And then as a result of that, you kind of can imagine a drop down menu where you have all these different Fedimints that you're connected to in the same front end.
And then you can easily switch between them.
Ideally, like one or two button presses, like exit this fediment to this fediment, and you can just move between.
You can constantly rebalance if one is for like spending cash or one is for larger savings or something like that.

NVK: 01:13:06

Would you say that would be similar to like how Cashu does with LNBits?
You just kind of go there, you just add an IP, click and boom.

Eric: 01:13:15

Just to clarify, I co-founded Fedi with Obi and Justin Moon, but day to day, I'm mostly staying on the FediMint side as a lead maintainer there and try to stay out of the commercial side to be as impartial as possible because we want to see multiple implementations, multiple front ends for the Fedimint and to see it grow as an ecosystem.
Because I mentioned it a few times, like Fedimint isn't just federated e-cash, it's like a federated application building platform.

NVK: 01:13:45

That's normally how a lot of these protocols die is because you have a company that's a little too closed, even though it's open source, but they are a little bit too closed on how it gets deployed because, you know, they want that sort of like moat and fair advantage on starting out, which is fair, you know, you got to pay bills, but they end up just getting a little too harsh on that.
Like, like Liquid did, you know, Blockstream did with Liquid.
And then, you know, there's no competing, there's nobody else interested in using somebody else's platform instead of a protocol, and then it kind of goes nowhere.
So props to you guys for sort of like choosing this sort of like, let's get this idea, this open protocol out, and then sort of like monetize through like, you know, just being very good at it and, you know, having a lot of great ideas.

Eric: 01:14:35

Yes.
And maybe to Matt's point, like I have some insights into the app development, obviously.
And one interesting thing that's being discussed there is if you have a community that's growing and that's becoming kind of too big for the threshold that was chosen, like let's say we have a three out of four community and then more and more people join it and it becomes kind of risky.
And the app would determine that using some factors, then it would kind of nudge people to start their own communities.
And you can join multiple federations.
That's totally possible and it's encouraged to do so.
So over time we could have like one federation as a start and then these many, many smaller federations spinning off from that just over time by naturally more and more people being attracted and then like becoming a worse risk trade off and then comes feasible.
Like if you have enough users, then you can actually spin out like a smaller federation for a smaller sub-community.
Right?

NVK: 01:15:42

Yeah.
Rijndael, I think you wanted to say something.

Rijndael: 01:15:44

Yeah.
I was going to say to exactly what Eric's talking about or Matt said a few minutes ago, there's a Cashu wallet called NutStash.
I think it was done by Gandalf21.

NVK: 01:15:56

I love the naming.
It's just absolutely brilliant, Brandy.
It's everything I love about that thing.

Rijndael: 01:16:02

And what's cool about Nutstash is it's a wallet interface that's compatible with the Cashu protocol.
And you can actually add multiple mints to it.
And then you can like one click shift money between these different mints.
And what it's doing is it's doing like a lightning payment from mint A to mint B, but the user experience is I have 500 Satoshis in mint A and I want to split it between mint A and B.
So I just sort of shift my money from one to the other and it does a redemption and payment on one and then like a receive and mint on the other.
But, you know, because these things are connected to each other over lighting, it's a really smooth experience.

Calle: 01:16:46

Yeah, it's fantastic.
Nutstash is amazing.
You can check it out on Nutstash.app and it's made by a developer called Gandlaf21.
He's an amazing guy.
But I just, you know, to comment on what we just said and how this influenced the cashu development itself.
This openness really had an impact on what the apps look like today.
So first when we started working on it, we made everything in the open.
All the API endpoints, everything was discussed with everyone who was interested in how to make it more efficient and so on.
But it became very immediately clear that if you make it super easy to spin up a mint, which is in Cashu three clicks in LN bits, and if you do it with the Python thing, It takes you two minutes to install and just boom, you are mint basically.
So it turns out that if you increase the number of mints just suddenly, then the wallets, all of them become less usable if they don't support multiple mints.
It just becomes boring.
You know, you're just part of this mini mint that someone has put up there and you can basically only pay these 15 autists in that same mint or something.
So it's not fun to use it.
So just the availability of mints and I've looked it up on lnbits on the demo server which is one custodial demo server that you should not use, but already people have made more than 300 different mints on there because it's click, click, and then you have a mint, right?
It shares Lightning Node with all the other mints, but it's a true e-cash mint.
So all of the Cashu apps basically have multi-mint support now.
You have Cashu.me, you have the Python client, there is a Golang client.
All of them need to because otherwise the UX becomes just unbearable, basically.

## The open source movement

NVK: 01:18:26

I think the last few years sort of like gave us this a little bit more clarity on this sort of like the open source meme or open source sort of like movement.
I think things were a little bit convoluted, a little bit sort of like heated for, for many decades.
And I think it created a lot of confusion and sort of like made things a little too black and white for people.
So people chose to sort of go one way or go the other way and hate each other and all those things.
So I think what's been happening because of Bitcoin really is that we're starting to realize that there is this better space where, you know, we're all like protocol maximalists for the fossiness of it.
Like it has to be essentially public domain, right?
It's not even GPL.
It's like literally public domain.
That's the protocol.
So it never becomes a platform.
And the people who invent them often find that is in their interest, their self-interest to bootstrap those protocols with open clients, open servers, and things that foster the adoption of that protocol.
And then they'll go and they'll try to find moats and values and businesses where the value add is at, right?
So they will build specialty clients that may be open, closed, who cares, right?
And this creates this sort of like healthy place where the creators find a direct source of revenue from their creation, but they don't hinder society from fully benefiting from the creation too.
After Nostr came out, you know, like you're finding this sort of like extremely amazing snowballing of this model happening where, because we used to, we used to have right, this sort of like the foundation owns the protocol.
And then there is a company to the side that owns the implementation.
But it was never sort of like clean thinking, right?
There was never sort of like nobody fully understood like where one starts, the other one ends.
And I think this clarity is really starting to snowball now.
And it's giving us this like ultra fast pace.
I mean, I'm seeing this on Nostr, I'm seeing this on Lightning.
And Bitcoin took like, you know, over 10 years for this to be clear.
I don't know.
I just felt like this was like a, it's a super interesting thing because I'm seeing it again and it's exciting because it pushes people to really innovate much faster because they also know they're going to have a way to eat after.
It's a very cool place to be in.

Rijndael: 01:20:57

Yeah, I have a very strong opinion on this.
I think something else that's happened in the last decade is the old way to monetize your open source project was to provide like either pro serve for setting up the server or whatever the backend was or to provide like extra bits.
And then you had the three big cloud providers basically strip mine open source by saying like we're going to host MongoDB as a giant scale out service and completely eat the business model of like hosting MongoDB as a service.
And now Mongo has no way of making money.
And so I think that the incentives used to be to make a really good piece of open source software but make it kind of hard to deploy so that you would pay people to come and deploy it for you.
And that yeah, And then Amazon made that a one click operation and completely destroyed that business.
So now the thing to do is let's make it as easy as possible to deploy and customize these things.
And then the value add is custom clients, custom data, custom integrations.
And that it turns out is actually better for the community because people can iterate on top of it faster.

NVK: 01:22:08

It's amazing, right?
That you could find this incentive alignment out of all this mass where like, you know, open source people eat and it's not Microsoft and Amazon who make money out of GPL, which has always been my beef.
It's like you have this evil corps.
They make all the money out of all the public domain.
That that, anyways, that's, that's pretty cool.

Eric: 01:22:28

Yeah.
And Bitcoin also gives us a way of rewarding the people that built the software, like value for value, essentially.
Like if you're building a Lightning wallet, why don't you include some, let's say, opt-out functionality that just sends a small donation, depending on the usage of the app, to the creator at the end of the month.
Like, why not?
We can do it now.
Like it was totally infeasible for most of the open source history, but now we do have the tools.

NVK: 01:22:55

Well, it's because we were never able to send a Mili Satoshi in terms of dollar terms.

Eric: 01:23:02

Yeah, exactly.
Now we have the tools.

NVK: 01:23:04

Now we do.
But I also think that we now have more customers, right?
Where we didn't before.
Before the customer was the product too.
So you only really had Twitter as the customer of your technology, not the Twitter users as the customer of your technology.
Right on Nostr, your customers are both the users and the applications using your stuff, right?
It's just, it's a more broad thing.
We don't know how this plays out either.
It's just an exciting new dynamic that's fairly new.
And I think people are not paying attention to it.

Eric: 01:23:36

Yeah, I think there's an ongoing cycle kind of in computing.
First, you move the business logic to the server and then you move it back to the client then you move it back to the server.
And currently we are moving a lot of our business logic back to the clients because we have enough computing power and it brings us certain benefits like censorship resistance and scalability and like a lot of good things.
That allows us to not have the central server as our customer, but the actual user.

## Proof of reserves in ecash

NVK: 01:24:04

Calle, I think you had a good, not a segue, but a fun pivot here, which is proof of reserves.

Calle: 01:24:14

Yeah.
So maybe if you allow me to go one step back again, because I'm going to get to Proofs Reserve immediately after that.
So the two big problems of e-cash are, in my view, maybe there are more, the two big problems are its custodial.
So you leave your Bitcoin with someone, they can take it away from you.
And the other one is, it's hard to audit.
So it's hard to figure out whether someone prints more e-cash than they have Bitcoin, basically.
So as we've heard before, Fedimint really improves the first problem a lot by just federating the Bitcoin and the signing process into multiple servers.
I think that also comes with the cost of implementation and so on.
So in cashu we don't do that.
It's just a single SIG server.
That means that if one server rugs you, your money is gone.
So that is the problem number one.
And the second problem is this proof of reserve, but actually the problem is proof of liabilities.
But because proof of reserve is solved these days, it's on-chain proof of reserve, you can do it.
We also alluded before proof of reserve is not really possible with Lightning, but there are ways around that.
But for an e-cash project or a protocol or a mint, you would have to figure out somehow how you can prove whether the liabilities of the mint equal the proof of reserve or at least are smaller than that.
So we've been thinking about this for a long time and just how do you make that for your Cashu.
I just want people to know that the mint didn't print any money out of thin air.
And usually, you know, Eric has summarized two attempts on this and I would actually like his opinion on this because you said before you think it's impossible.
I think now it's possible since a couple of days, basically.
We found a new way of approaching this.
So here's how it goes.
In Cashu, a mint does two operations.
It first gives you out the e-cash.
These are the blind signatures that's giving out.
And then there's a second operation which is burning the e-cash.
When you spend it again, you redeem it and you reveal the secret.
So there's essentially each mint, the minimum mint design for each e-cash project is it needs a list of spent secrets.
It's a list that grows, right, for all the money so you can record it in a database that says this note has been spent once, I'm not gonna honor it again, that's how you prevent the double spending.
So when we built Cashu it became pretty clear immediately that this will, over a long period of time, if you have thousands and millions of users, this would grow.
It's a list that will grow forever and ever, and you have to keep the list forever because you don't know when someone with a very old e-cash note will just appear and try to spend it.
So one solution that came up to that was, let's introduce key epochs.
A very simple solution is that we have one set of private keys for the mint that is valid for one year, let's say, and then after one year, we make a cut, and then we rotate the keys to a new set of private keys.
And then we slowly rotate all the ecashu from the old epoch to the new epoch.
And then once all the ecashu is redeemed from the old epoch, we can just prune it from the database and keep going on with the new key epoch basically.
So for scalability reasons we've come up with this rotation of keys initially.
Now it turns out that you can use this same mechanism to build a proof of liability system and the way it could work is that the Mint now publishes these two lists that it has.
So there is a list of all the blind signatures it gave out and then there is a list of all the secrets that it redeemed.
These are two different lists and usually they are kept inside the Mint.
No one is interested in them.
But now in this new scheme, the Mint could publish these reports, let's say once a month.
It would publish a whole list of money I gave out to everyone and the whole list of money I redeemed by everyone.
And you could tally it all up.
And the end result would be how much money is in all the wallets out there.
So if you have all the issued money minus all the redeemed money, that is the open balance of this mint basically.
So you would publicly open these, publish these lists and now here comes the kicker, a user that has a wallet now could basically, once these lists, these reports are published, could go back and check whether the money that I ever owned is included in this list or not.
So basically what you can say is that the Mint will try to make its liabilities, this first list, as small as possible and it will try to fake redeems as much as it can.
That's dishonest Mint.
But with this, when you force the Mint to publish this, you as a user can basically prove that the mint hasn't included the e-cash that it gave you into this list.
So basically, one month later after this is published, you could come and show to the world, I hold e-cash from this mint, but the mint didn't include it in its proof of liabilities report basically.
That's how you catch the mint.
Now, you know, someone listening might now notice, wait, this is flawed because how do you know that all the e-cash that you gave out will also be redeemed or the mint could just, you know, pretend to be a user and just produce fake burns.
It could just fake redemptions basically to keep its liabilities low.
But that's where the rotation part comes in.
Basically, if you force the mint to rotate the keys every few months or so, you close the time window in which new e-cash can be produced.
So basically, if you say the mint doesn't produce e-cash notes from this old epoch anymore, then it cannot fake an arbitrary amount of redemptions because people will just appear out of nowhere and someone will say, wait, you faked some redemptions, you say that the key epoch is closed, you pretend as if it's closed, but it's actually not.
I still hold money from that key epoch basically.
So that's how you catch a mint producing fake money, basically.
And I'm super stoked on this because the key point of this was this time window, actually, that I didn't think about, that you need this predefined time in which you close the key epoch round.
And once you have that, you just suddenly have this public way of auditing the mint and it may be that if you want to try to catch the mint at lying you need to reveal your privacy you know the unlinkability of e-cash gets broken for the person who wants to catch the mint lying.
But I think it's a like basically it's a that's a very fair price to pay.
Everyone would pay that price to reveal their privacy once to catch the mint at inflating the supply without telling everyone.

NVK: 01:31:15

How do you enforce the epoch?

Calle: 01:31:17

You wouldn't enforce it.
You would just control it socially, basically.
The mint would commit publicly that it will rotate the epoch every 12 months or so, or every month.

NVK: 01:31:27

But how is time counted?
Like, how do you not cheat time?

Calle: 01:31:31

I mean, I would obviously do it with a block time and not real time, but...

NVK: 01:31:35

Yeah, I was just trying to understand that.

Calle: 01:31:37

And you would obviously also, I think without saying it goes, you would publish these lists and open timestamp them as well onto the Bitcoin blockchain, because you don't need a blockchain, you just need a timestamp of your documents.
But so that way you can also make sure that no one has went back and just manipulated the list after releasing a notorious one.

NVK: 01:31:58

Is the trade off that at the public review time, everybody goes to jail kind of thing?
Or what's the anonymity set left there?

Calle: 01:32:08

So if you, that is true, if you make this epoch too small, it becomes bad for the privacy because now you have a pool of users that is maybe, you know, if it's only one day long, for example, then that means that only the people who use the e-cash in that single day are the anonymity set.
So you want to make it long enough such that the anonymity is still great, but you want to also keep it short enough so that you can actually catch the mint fast enough when they're trying to inflate the supply.
Right?
So you need to wait at least this one epoch until you can catch the mint after the epoch.

NVK: 01:32:40

You know, I'm imagining sort of like a Girls Gone Wild situation here where they're all on stage and they all just lift their shirts at the same time.

Calle: 01:32:48

Exactly.
But yeah, so a single user would be enough to catch them in that line.
So the mint would pretend this epoch is now cleared and I've paid you all back.
But then someone just single user would be enough to say, no, I can prove that you did not and then something fishy is going on.

Eric: 01:33:03

And you don't even have to reveal the blinding key or lose your privacy, actually.
Like I think having a public spend list is enough because if your e-cash note isn't included in the public spend list, but it's still validly signed, then you know and like this old mint or this old epoch doesn't have any money left in it.
Then, well, obviously there was inflation somewhere.
And I think that the really cool thing that didn't occur to me about this scheme is that you can actually prove it.
Like this automated bank run kind of idea has been floating around for a while, I think, at least in the FediMint land.
But actually being able to prove that your mint was cheating by publishing this spend book.
That's really cool.
Because otherwise you would just notice, okay, well, I cannot get my money out of the mint every few months or so, when it happens.

Calle: 01:33:58

And so this simple proof library, and it's actually simple, I think, you know, You would have to read it to maybe really understand.
If you just listen to it right now, it might be a bit confusing, but it's actually a simple one.
And what's fascinating to me, so I've been thinking about this only in the last 72 hours, it starts causing more and more ideas in my brain, which is actually that once you introduce a proof of liability, then you get away, you suddenly, so many other problems go away.
For example, in cashu, the single-sig problem in cashu that someone could just run away with your money, it basically gets fixed by this proof of liabilities because now a cash mint, what it could do is just keep a very tiny float of the money in the e-cash mint itself, in the lightning node, and the majority of the fund can just go to on-chain.
That's why you want them to be able to proof of reserve anyway.
And then you can just do a multi-sig and suddenly you have just unstealable money with a single-sig e-cash server that can just spend very fast only the balance on the Lightning.

NVK: 01:35:03

Could you transfer this proof of liability for somebody else to assume the mint from that checkpoint?

Calle: 01:35:10

You need to repeat the question.
I didn't get it.
Like, how do you, what do you transfer?

NVK: 01:35:15

So you now have this proof of liability, right?
When you essentially do the review.
Can another mint assume that and now be the new mint?

Calle: 01:35:25

So you would sign the reports

NVK: 01:35:29

with somebody else.

Calle: 01:35:30

Yeah, with your private keys of the mint, basically.
So you should be able to verify that this mint, that the report is literally from the mint that gave out the e-cash, but that should be easy to solve.


Rijndael: 01:35:40

So one of the things that's also really interesting about this scheme is if you imagine a world where you have a single SIG issuer, right, like in Cashu, a way that they could inflate the money supply or double spend is that, you know, I'm the mint, but I'm also a user, I buy a sandwich from Odell, he goes and burns the token at the mint to get a new token.
And I say, yep, I've written down that that token's been burned.
And then I just erase that entry.
And now I go and hand the same token to NVK to buy a sats card.
And I can just like continuously double spend this same token because I'm getting value for it, but I also control the ledger.
And what's interesting is if you publish the spend list, and if you timestamp it with something like open timestamps, then clients could periodically download a snapshot of the spend list.
And if I receive a token that's on the spend list, then I just reject it.
And I don't vend the good or service.
So there's this thing where You might not want to do that in line with every transaction or something, but the possibility of people maintaining a synchronized snapshot of the spend list might be enough to deter that abuse from the Mint.

Eric: 01:36:58

I think that case is actually not really what the Mint would do because they already have the key.
They can print arbitrary e-cash.
Like, they don't have to double spend like that.

Rijndael: 01:37:08

Sure.

Eric: 01:37:09

Yeah.
But it's really interesting that you can prove that the Mint was cheating because then like even if only you are stuck on the old Mint Epoch and everyone else has migrated over, you can at least warn them that this Mint went fractional reserve.
Like what you're doing is when you're migrating between epochs, you're staging a bank run more or less.
And now instead of only knowing for yourself that the mint was fractional reserve, you can prove it to other people that will then hopefully be wise enough to take your money off that mint.
And also in regards to the option where you would keep a lot of the money in a multi-sig offline wallet in a single-sig Mint.
That only really helps you if you don't allow arbitrary amounts of money coming out from the multi-sig into the hot wallet of the mint each epoch, like you need to limit it kind of.
And that would also limit users that want to get out of the mint, which might be kind of problematic or like it's a trade-off.

NVK: 01:38:12

But it's often all you need is like one bank run to happen in one place to sort of inform how people should go about the other places that are similar within that human sort of time span.
Right.
So if one bank goes bad, everybody goes check their shit.

Rijndael: 01:38:27

Yeah.
My Mint doesn't have a solvency problem.
It has a liquidity problem.

Calle: 01:38:32

Exactly.
I mean, that would be a question of how to manage capital as efficiently as possible, right?
So in my experience, when you look at, you know, if you look at a system where money flows in and out, the float is on the order of a percent or so.
People just leave it sitting there for most of the time, basically, in every kind of bank account or a Bitcoin wallet or whatever it is.
So there you have the tradeoff between, because lightning, again, is not auditable money, right?
So you have to make this trade-off to say, I want to, let's say, have 98% of the funds on an auditable multi-sig wallet that no one can run away with.
And I'm OK with having 2% of the funds in a hot Lightning wallet that I cannot audit as well.
Basically I could spend it without anyone noticing it.
At the same time, you have to then calculate against whether that is enough to have a good UX for people suddenly wanting to make a bank run without having to wait for new funds to appear on the Lightning Node or something.

## Onchain vs lightning mints

NVK: 01:39:35

So would it be stupid to sort of, you know, for a mint that has less velocity needs to just do it on-chain?
I mean, you know, you can have a much smaller Taproot multi-sig there that, so it's like, you know, you're still using last block space, but it's still on chain, right?
And you can do it with thresholds, well, eventually, and have something that like maybe has less, so less velocity, but more accountability.
That could be interesting.

Eric: 01:40:09

Also one comment to like the idea of the multi-sig.
Like I think If you go all the way, then eventually you end up at Fedimint actually.
Because what we are doing is we have all the money in the multisig and we are also threshold issuing these e-cash notes because that's still the weak point in, I think, the single sig e-cash, but multisig Bitcoin scheme.
You don't really have an audit.
That's not what you do there.
It's more of attestation.
Like you attest at the point in time when everyone switched over, there were enough funds, but in between you don't know anything about that.
Like between these attestation points, the single issuer of the Mint could totally go and print all the money they want and you cannot prove anything about it.
And during that time, if they generate a lot of outflow, you couldn't really determine if that outflow is natural from users or if the mint has gone bad.

NVK: 01:41:05

So could you redeem to Base Layer instead of redeeming to Lightning?

Calle: 01:41:10

Yeah, I think, I mean, as Eric said, I think that is how Fedimint basically works.
It is the primarily the funds are stored in a multi-sig, but the Lightning functionality is another participant in the network that does a swap into the Lightning network.

NVK: 01:41:26

Because Lightning is multi-sig, so that's the part that I was missing there.

Eric: 01:41:29

Like Lightning is really hard to federate, actually.
And also you might not even want to federate it because managing a Lightning Node involves a lot of choices and federations aren't good at making choices on their own.
How you do it typically is you would make a proposal and people vote on it, it's much too slow to manage the Lightning Node with that.
So instead, what we are doing is we have this external party which runs the Lightning Node, which can make payments on behalf of users and receive payments on behalf of users in an atomic way.
So they cannot cheat.
All they can do is at worst, they can doss the user, like they can not provide their service, but they cannot take the money.
Like it's all atomic, atomically linked by the pre-image that's travels through lightning network and their spot contracts being executed in Fedimint.
So that's how we couple the single-sig Lightning Node to the multi-sig.

## Auditability and proof of liabilities

Fedimint.

Calle: 01:42:22

I want to get back to your point where you said that the Mint can basically, you know, between these attestation periods, which are, you know, these key epochs, when you roll over funds from one key to another, that inside these epochs everything could go wrong.
And I mean, not everything quite, there is still a limit, I guess, because it depends on how often you release these reports, for example.
But You're right in a sense, but I don't think that it's actually an issue because for Fedimint, it makes sense because you're focusing on community custody where the chance of being stolen maybe is the primary problem that you need to solve basically.
But I think for a large custodian, for example, or a bank, I think the problem is more the fact that they could inflate the supply without anyone noticing.
I don't think that It's very likely that wallets of Satoshi would just run away with the money and nothing could, I mean, there is still, you know, you could still punch them by following up on them in the physical world.
But catching a mint, just inflate the supply 1% a year, 2% a year, that's much more problematic in a big setup like a whole bank, for example.
So I'm extremely fascinated of the solution or just the possibility because I myself, I don't know of any other system where you can actually audit the liabilities basically publicly.
I mean, even if it's not applicable to cashu or Fedimint or whatever, if the scheme alone is interesting by itself, because show me a bank where you can audit their liabilities or a exchange.
I mean, all of the exchange releases.

NVK: 01:44:07

Oh, it's by design.

Calle: 01:44:08

They all release proof of reserves, but it's not worth anything if you don't also release a proof of liabilities.
But how do you check the liabilities?
I mean, how do you check that there is not some Kraken user out there who has a very big number on their balance, basically, although there is no Bitcoin backing it up in this proof of reserve?
That's a problem.
And I see, I mean, If this whole thing works, we have to implement and see what are the trade-offs.
But I'm just really bullish just on the possibility of introducing a liability check, public liability check for custodial entities.
Very cool.

Eric: 01:44:41

Definitely, it helps a lot.
I fully agree there.
It's just what I want to point out is it's not a full auditability solution.
It's like periodic attestation.
And that's totally a breakthrough.

NVK: 01:44:52

Well, it's a huge upgrade.

Eric: 01:44:54

Yeah, definitely.

Rijndael: 01:44:55

And probably like the whole theme for all of the e-cash stuff is that it's not a silver bullet.
It's a huge upgrade.

Rijndael: 01:45:02

better trade-offs than what we have.

## Fedipools

NVK: 01:45:04

So guys, there's just one more thing that I wanted to get it in.
I mean, maybe we get into some other things, but like this one, I definitely wanted to get in before the two hour mark, which is something that kind of caught my attention like extra to Fedimint, which was Fedipools.
Do you guys want to like touch a little bit on that?
It's like it's a super interesting idea.
And that kind of like got my brain spinning a little bit for like, oh, holy shit.
So like, you know, this is not just like a banking sort of solution here, right?
Like there is all of these other interesting sort of programmatic things that he can do that can start solving like some real problems that we have like how do pools pay small tiny amounts of Bitcoin to their miners in a more private way.
So anyway, so like who wants to sort of like explain what Fedipool is and why that's even possible to do with Fedimint?

Eric: 01:45:59

Yeah, So maybe I should start and then Odell can correct me if I'm misrepresenting anything anywhere.
But to my understanding, Fedipool as a concept solves a different dimension of the mining pool problem.
There's already a Stratum V2, which solves the block template construction problem, that we decentralize that again so that miners themselves can propose their own block templates so the pools cannot censor transactions.

NVK: 01:46:29

He improves it.
I wouldn't say he fixes it.

Eric: 01:46:32

Yeah.
Okay.
Yeah.
And then there's the second axis where we want to improve that miners cannot be cheated out of their money because like pools have to take custody of the block reward and then split it up.
And that's what Fedipool in my opinion solves.

Odell: 01:46:46

Yes.
So I mean, if I was going to just from a high level here, and I might as well while I'm speaking now, just say that I'm dropping in five minutes, and this has been a fantastic conversation.
Unfortunately, I have to leave early.
The cool part about Fedimints is it mitigates and reduces a lot of the risks we see with custodial wallets.
And once you start to talk about custodial wallets, where do we see issues with custodial wallets and central points of failure in Bitcoin?
We see it on exchanges, we see it on custodial wallets like Wallet of Satoshi.
Those are obvious areas of target for for Fedimints to improve that trust dynamic.
And then of course, we also see it with mining pools.
Mining pools operate custodial wallets for their miners, the individual miners that connect to mining pools.
There's a lot of trust there with the mining pool operators.
Now Stratum V2 is an extremely promising protocol improvement.
Fedipools is complementary to Stratum V2.
So what we'd like to see, or at least what I would like to see personally, is essentially a Fedipool implementation that also includes Stratum V2 and the benefits that come with Stratum V2, but instead of having a single SIG custodial wallet that we see with mining pools currently, you would have a multi-sig federated wallet that also comes with the Chaumian eCash privacy benefits for the individual miners.
There's an interesting thing there specifically with job negotiation, this idea that instead of the currently mining pool operators are choosing which UTXOs are included in a block, Stratum V2 kind of tries to flip that on the head and allow individual miners to run their own nodes and propose which transactions are going to be included in a block to try and reduce that censorship risk.
Fedipool, you could actually, but the big complaint that we see there is most miners are not gonna run their own nodes, they're not gonna be well-connected nodes, they're not gonna be constructing their own blocks, there's a lot of friction there.
In a Fedipool, we could have a kind of hybrid model where the people that are running the federation servers, let's say it's seven individual miners and the quorum is a five of seven or something like that.
Those seven individual miners that are running the Federation servers could also be doing the job negotiation and choosing which transactions are included in a block.
So then the smaller miners that are part of that Fedipool, instead of imagining all the smaller miners all running their own nodes and doing this job negotiation and the latency that gets included with that whole process and whatnot, they could just kind of delegate who they want to do the transaction selection to those Federation members.
So you could have like seven different members in a pool, basically all proposing block templates, proposing which transactions are included, and then a bunch of individual miners then choosing which of those seven they trust with the job construction.
And so then all of a sudden, you have competition within a pool on who is constructing the transaction rather than having to completely leave the pool and go and switch to a different pool because you like how they choose the transaction.
So you actually have this cool little competition, a game theory dynamic that happens internal within the pool.
Does that make sense?

NVK: 01:50:00

That was great.

Eric: 01:50:02

Yeah.
Yeah.
And I just want to add, like, we shouldn't stop at Fedipools.
Like there's so many other applications that we could federate.
And as Matt mentioned, like everything essentially that takes custody of your Bitcoin and then allows you to do something smarter with it that can be implemented as the FediMint module.
And if there are hackers out there that are listening, please come and build modules.
It would be awesome.
And we just finished like a big materialization effort.
And now it's much, much easier to just implement your own applications on Fedimint.

NVK: 01:50:42

Very cool guys.

Odell: 01:50:43

Now I have to drop.
This conversation was great.
Appreciate you all.
Cheers.

Eric: 01:50:48

Cheers.

NVK: 01:50:49

Any final thoughts, Matt?

Odell: 01:50:51

I did a full write up on Fedipool on my blog, DiscreetLog.com.
Check it out.

NVK: 01:50:57

Awesome.
That was great.

Rijndael: 01:50:58

Thank you.
Thank you for joining us.

Odell: 01:50:59

Thanks.

Rijndael: 01:51:01

All right.
Now that Matt's gone, let's get into the real talk about privacy. I'm just kidding.

NVK: 01:51:06

Well, you have nothing to hide, so.

## Scriptable ecash01:59:36 Nostr + ecash

Rijndael: 01:51:08

That's right.

NVK: 01:51:09

So, guys, I mean, like we covered quite a bit.
I still have a little bit of time.
Is there like any other technical aspects that you think like people maybe miss?
We're going to get to Nostr in a second too, but I find that like oftentimes people sort of like restrain from doing the brain dump of some of the technical parts.
And there's a lot of people there who appreciate that.
So is there anything else that maybe we should talk about?
I think Calle, he's doing like hand raising there, like there's no tomorrow.
So Calle, go for it.

Calle: 01:51:43

So I think what's also an interesting point is to talk about scriptable e-cash, because I think that it also goes into direction of what I tried to say before, why I think FediMint is a killer of Liquid.
It's not a killer.
I mean, I love Liquid, Don't get me wrong, but it's something that achieves something very similar because it allows scripting.
So what you can do with eCash is, you know, usually if you have a scripting language on a blockchain, you would have all the participants verifying the blocks, execute all the scripts, and then see if the scripts are valid or not.
And if they are valid, then the transaction is valid, right?
So how do you achieve something similar with eCash?
And it turns out that in the very beginning when I tried to explain how it works I said that at least that's how it works in Cashu.
I imagine it's similar in FediMint but please correct me there as well.
In the beginning I said you generate the secret and then you blind the secret and you send it to the mint and then the mint signs the secret.
Now what if that secret is not just a random number, but it's actually a, for example, script hash?
It could be like we know with pay to script hash, there's a whole script that you want to have executed, and then you take a hash of the script and now it looks like a random number and you let that to be signed from the mint basically and say, please sign me this random looking number.
The mint doesn't know that there's a whole script behind it, it just signs the number and get it back.
Now, when you, and that's the idea how it works in Cashu today, is when you then want to spend this special piece of e-cash that is not generated from a random number but from actually a script hash, then You can only spend it when you send it to the Mint, and then the Mint will ask, give me the script for this eCash as well.
I will honor your eCash only if you can give me a script that it was committed to with this random secret, and if the script is valid, obviously.
If the script doesn't run through, I'm going to unread.
And that sounds super simple because now you just, instead of redeeming eCash directly, you just also supply script to redeem the eCash.
And the Mint now has a state machine, runs the script in Cashu's case, it's literally Bitcoin script.
So you can use Bitcoin script to script your e-cash.
The Mint then just puts the script into its virtual state machine, runs the script, and if the script says true, then the e-cash is valid, basically.
Once you introduce this, basically a whole new universe opens up what you can build.
You can build smart contracts out of it, I don't know, trade atomically between one person and another.
You can now make an atomic swap between e-cash and Lightning Or a shitcoin and e-cash and basically all the things that you can do on a blockchain, but without anyone having to run every script.
Basically, you just have this one server or a federation in the case of Fedmint that needs to execute the script and says, yep, this is okay.
I can honor this e-cash transaction.

Eric: 01:54:47

Yeah.

Rijndael: 01:54:48

Well, in your case, your eCash token is committing to Bitcoin script, because that's what was available in the library that you used.
But it doesn't have to be that way, right?
It could be that, you know, your e-cash issuer executes whatever script semantics or whatever VM you like.
So you could build whatever crazy smart contracting system that includes external data.
Maybe you want to have an e-cash where every transaction is like the settling of a bet or a financial transaction that relies on external pricing oracles, like whatever you want.

Calle: 01:55:26

Or maybe you can make an e-cash mint that is basically an exchange.
So It's literally only for an exchange for people to trade one shitcoin against another shitcoin, for example, but atomically using e-cash.
Could be.

Eric: 01:55:37

Yeah.
Yeah.
So it actually, to some degree, it works really similarly in Fedimint.
Like we don't randomly generate our nonces because in the federated model, it's actually necessary to have a key in there that can sign the transaction.
Because we have this weird little problem that when we create an e-cash transaction that takes some e-cash notes as input and issues new ones as output, then if you submit it to a malicious guardian, then they could just take the e-cash note from the input side and attach it to a transaction of their own that pays themselves.
So we already need the public key in there to sign the transaction.
So this rebinding attack cannot happen.
That's also why you generally always want a public key in a Bitcoin script, because if you only had, for example, a hash and then you need to reveal a pre-image, Anyone could just take this input and attach it to their own transaction.
And it's totally imaginable that we extend this public key with a taproot-like construction that can also commit to a bunch of scripts.
And to be honest, I think the scripting system of Bitcoin is probably one of the things that people would really like to fix if they could.
And so I wouldn't go to Bitcoin script for that.
But one really interesting idea that a friend of mine is working on is simplicity.
And I think he will be talking about it at Bitcoin++ in Austin next month, how to integrate Fedmint with simplicity and how to have scriptable E-cash notes.
And that opens so many new possibilities.
It's amazing.
And you have a formally verifiable scripting language without the weird semantics of Bitcoin script and some of the privacy of e-cash notes.
That would be just mind-blowing.

Rijndael: 01:57:32

Yeah, that's really cool for a bunch of reasons.
I mean, it's really cool for Fediment users, but I think it's also really cool for Bitcoin users, because one of the problems that I think we historically have when weighing new soft forks or new opcodes is you have this like chicken and egg solution where we're like, we don't want to add new features to Bitcoin if it's not actually useful or if there's not market demand or if there's not software support for it.
But like, how do you go and build those things if it's not available in Bitcoin?
And so that's where the idea of like the Bitcoin Inquisition subnet comes in, or a lot of times people say, Oh, go add it to liquid first.
We'll test it on liquid and then we'll add it to Bitcoin.
It'd be really cool if like you could go and build interesting smart contracts in simplicity on top of Fedimint, like show that there's demand, work out all of the conceptual ideas, and then that makes it more obvious whether or not we should have something like simplicity.

NVK: 01:58:23

Well, I mean, you know, there's also the problem that like elements is like 80,000 diff.
You never get merged.
I mean, like, realistically speaking, right?

Eric: 01:58:31

I think the problem with having that on eCash is that it's too different from Bitcoin already.
So what I think would be the solution here where Fedimint definitely can help is making SIGNETS deployable as a Bitcoin sidechain to everyone, like make it available to everyone to deploy SIGNET sidechains.
Just take any fork of Bitcoin Core, set up a fediment with a module that can sign SIGNET blocks, and just let them try out all the crazy software features they want.
That's like something I really want to see because then we could test out OpCTV, we could test out Simplicity, all the things in parallel, like without having to press implement it in elements, which.

NVK: 01:59:20

Whatever makes the conversation of drive chains go away is worth

Calle: 01:59:25

pursuing.
Yeah.

NVK: 01:59:26

Yeah.
Like anything really.
I mean, same for a Tail Emissions, like whatever makes it go away as a conversation, I'll take it.

Calle: 01:59:34

That's good.

NVK: 01:59:36

So, I guess like the last thing before I close this up, maybe like we should touch a little bit on Nostr and eCash because it does seem to have a little bit of a match made in heaven kind of situation there, very similar to Lightning and Nostr.
I think the velocity of eCash being used on Nostr could be better than using Lightning, perhaps.
So I think it's maybe worth exploring there a little bit.

Calle: 02:00:00

So the nice thing about eCash, and that's the different thing, that's what in the UX perspective really sets it apart from Lightning, is that Lightning is a pull-based system.
You have to generate an invoice first, and then the invoice has to communicate to the sender, and then it can be paid.
Whereas eCash is a push-based system.
So you take your money and you throw it to the receiver and they need to catch it somehow.
That changes a lot of things, like just from the possibilities of what apps you can build.
And for a push-based system, right now in cashu you most of the time when you have a cashu transaction, so you either scan something that looks like a lightning invoice and then the cashu transaction happens in the background that's again pull-based, or you take this piece of text and you send it to someone on Twitter or on Telegram or Signal, whatever, to any text transport basically.
But for these text transport systems you need identity, you need to know the receiver somehow and send it to the Twitter handler or whatever.
And I think Nostr really fixes this.
So Nostr, I think Nostr for me personally, it's more interesting for the other stuff, you know, it's notes and other stuff transmitted over relays.
I'm really bullish on the other stuff, basically.
And the other stuff will be, and already we're seeing this, will be machines talking to each other.
So you have software talking to software over Nostr, not people talking to people over Nostr.
And one of the ways that already you can use in Nutstash has a NOSTR client built into the wallet.
The Cashu nutshell, that is the Python command line interface, also has NOSTR built in.
What you can do with these is basically you just say, Cashu send and then the amount and then add a Nostr pubkey or NIP5 identifier or whatever.
It takes the e-cash and just wraps it into a Nostr DM and sends it over to the user.
So the UX becomes you open your wallet and then suddenly it makes bing And you see a DM just arrived in your wallet and you got some eCash that you redeem immediately.

NVK: 02:02:05

So I guess like two sort of very like high level things.
Do you think it would be worth changing Zaps to support like eCash tokens?
Because right now one of the issues is Zaps that you can't even prove so you can do washing, right?
You can't prove that the receiver sent a real Lightning transaction.
Is there no point in making Zaps with tokens?

Calle: 02:02:29

I'm not sure.
I think the Zaps are, I mean, they're super popular, but they're not in line that much with how LNURL actually works, although it uses LNURL in the background.
And at the same time, the reason why Zaps mean anything is because it's hard to run a lightning node, right?
If it were super easy to run a lightning node, everyone would just fake ZAPS as much as they want, and it would lose its meaning.
So basically, I think, like, although I love it so much, just being very honest about it, I think ZAPS itself is built on a foundation of sand somehow.
It will go down as things become more easy to use.

NVK: 02:03:07

Oh, I think somebody is just going to figure out a way of adding a proof to the other end before the client.
So you're still going to rely on the clients to display it truthfully, right?
But technically you could add a proof to the other side.

Calle: 02:03:20

Yes, but nothing hinders you from just spinning up infinitely many identities and zapping yourself all day long, basically.

NVK: 02:03:27

And no, no, you could make it.
Yeah, I guess.
Yeah.
So Well, then maybe with Cashu it's true.
I mean, you could have it so that the mint validates that.

Calle: 02:03:35

Yes.
In that case, you have the same problem that you can pay yourself all the time.
So I think that that's it comes back to what we had earlier.
If you have an anonymous system, then only Bitcoin fixes this basically.

NVK: 02:03:47

That's right.

Calle: 02:03:48

So you need some kind of proof of work or something to get rid of fake identities.

## Naming ecash units of account

NVK: 02:03:53

So where, like aside from just sending like Cashu or FediMints, I mean, is there a name yet for your unit of account, at least for the, on the Fedimint side for like how to describe it.
I know people would just choose whatever they want, but.

Eric: 02:04:07

I think there shouldn't be actually.
I think maybe FMPTC, that's what we use in some documentation, but in my opinion, E-cash should never be used directly.
Like I think it's an anti-pattern to actually send e-cash in most cases.
Maybe it makes sense for such push payments, but the problem is you lose your compatibility with the rest of the Bitcoin ecosystem.
Ideally, what I imagine for Fedimint is that all interactions will be violating invoices.
That way, it doesn't matter if the other side is on a Fedimint, on Cashu or on something completely different.
And like we avoid this monoculture essentially.
Like otherwise what happens if like one of these projects becomes too big and we now have our custom way of transferring money.

NVK: 02:04:56

Yeah, no, no, but like, you know, I'm just referring to sort of like the general term, right?
Because unfortunately we can't use the word crypto anymore for cryptography.
That's gone.
We can't use the word token anymore because, you know, it's going to just feel like it's a shit coin, right?
So I feel like when people who are not as technical are sort of like discussing this and discussing ideas and maybe what they want to invent as companies that add value add and whatever.
They often need a term, right, to describe it so that it really represents, you know, this e-cash token.
Yeah.

Eric: 02:05:31

Like we call it e-cash notes generally.

Calle: 02:05:34

Yeah, maybe notes like a bank note because it really also gives you the impression of a piece of money that you can hand around.

Eric: 02:05:42

We've also switched over the years multiple times.
Like We started with coins and we went to tokens and it was apparently too shitcoiny and now we are at notes.

NVK: 02:05:50

So yeah, because coin implies blockchain, you know, unfortunately.
Yeah.

Rijndael: 02:05:54

And for Cashu, you can say nuts.

NVK: 02:05:56

Yeah, I know.

Calle: 02:05:57

Yeah, we also say nuts sometimes.

NVK: 02:05:59

See, like The job that he did with all the semantics around Cashu, I think really made e-cash like happen in the minds of people in the last year.
People started to understand it because you created all the little metaphors and all the little terms that people needed to describe the ideas.
Right.
So that's why I was asking.
So like notes is a great one.
I'm going to start using that.

## ecash integration and intercompatability


Calle: 02:06:26

But can I come back to Eric, what you said about using eCash directly instead of Lightning invoices?
I have to think more about this.
I think I agree if you're talking about user-facing Lightning wallets, right?
So in the best case, a cashu wallet, also a FediMint wallet, right?
The user doesn't even know what they're using.
They're just, you know, they get used to using a Lightning wallet here and then they switch over to a Fedimint Lightning wallet and they just keep using it and get this perfect privacy for free basically on top of it.

Eric: 02:06:56

Exactly
Exactly

Calle: 02:06:56

So I get completely where you're coming from.
But still it's very worth exploring how if you strip away the Lightning stuff from it, still what it enables you.
For example, just, you know, including ecashu in a Nostr dm.
It could be including ecashu in a HTTP request or it would be, you know, putting ecashu into onions when you do onion routing.
Ecashu, layer by layer, you could pay a Tor relay, for example, and each Tor relay can just take out some eCash from the relay, from the layer that you wrapped.
So there are many, many things that are still completely unexplored because we didn't have this digital representation of money being able to send around.
I think we will still see people experimenting with bare e-cash without wrapping it around the lightning UX.

NVK: 02:07:43

I mean, I'm perfectly fine with that.
Like, especially when you're talking about, say, for example, the, I'm not sure how I feel, but this is the best example, but, Stacker News, which to me really just reminds me of poker websites, like any gambling site, right?
Where like, you know, people sending bare notes would be way more beneficial than people using Lightning to send those notes because you're only losing efficiency by using Lightning in this instance, right?
You're not gaining anything.
If anything, you're actually losing privacy.
So might as well sort of just send us notes around as we're, we're doing our gambling on the table, right?
And then the lightning in this case would be just used for clearing.

Eric: 02:08:29

Yeah, I think you got a point there.
The problem that I foresee in the future is that there will be many incompatible E-cash systems.
So maybe one thing we should take from that is that we might want to work on like a standard, how to represent e-cash in a way that can tell the application like what kind of e-cash is this?
Is this Fediment e-cash?
Is this Cashu e-cash?
Is this some random third-party e-cash?

Rijndael: 02:08:58

Are you thinking of doing like a BIP21 style like URI where you have like a URI that has whatever the lowest common denominator is, whether that's a layer one address or a lightning invoice or something.
And then you have some optional fields that are like, Here's the Cashu note, here's the fedimint note, whatever.
And you have tolerant readers that can read it and say, okay, this is the version of it that I support.
So I'm going to use this particular layer.
Is that what you're thinking or something else?

Eric: 02:09:32

Not necessarily.
The problem is a lot of these protocols won't be compatible necessarily.
So I think compatibility can at best be achieved on the client layer or on the recipient side.
So for example, if I only have Fedimint eCash from my mint, then I would encode in the eCash node, which mint it's from and which version of Fedimint it uses.
And then I can send it to a Cashu wallet.
And if the Cashu wallet kind of has a stub FediMint client that can at least redeem the FediMint e-cash note and then transfer it via Lightning invoice to the Cashu instance that the user's actually on, then we would have some minimal sort of interoperability at least, otherwise, like we would end up with totally separate ecosystems that cannot talk to each other.
And I think that would be a very sad state of things.

NVK: 02:10:25

I have different opinions on that, but I mean, it's great, But I think it's also nice when things don't necessarily talk to each other because we could always go back to Bitcoin to find like a deeper sort of more higher value consensus.
So I think people get too preoccupied with trying to make things compatible.
Like, you know, one of my biggest beefs with Lightning is the fact that we had 50 different payment channels, papers, and we ended up with just sort of like one that took kind of like almost too long to ship because everybody was trying to make everything compatible where we could have had three different lightning systems.
They were very completely incompatible.
They clear with Bitcoin, but they could have had different, very, very different trade-offs with very different powerful futures.
Right.
So I feel like sometimes like people, because we have Bitcoin and that's the only reason we can afford to try things that are not necessarily compatible in the other layers, like layer three.
But, but I think like, I mean, there's a million other questions and things we could talk about, but I think This is a very good point for us to sort of like close up without sort of getting too much in the weeds.
And I think it would be great to maybe do another one where we explore like a few different ideas and maybe in a few weeks or a few months, we're going to have like some more examples in real world of things happening, especially if a Moon stops snoozing in ships.
So guys, listen, thank you so much.
This was awesome.
Any final thoughts?
Rijndael?

## Final thoughts

Rijndael: 02:11:58

I'd say people should go and play with these systems.
Like the Fedimint repo is really well documented and it's gotten a lot more organized in the last year or so.
So go check out Fedimint and also play with Cashu.
Like I think three of the mints on the LNbits test server were just from like me messing around and you know, you can take 10 cents worth of lightning and make a shitload of e-cash on CashU and just like play with it and send it to yourself, send it to other people on Nostr.
I feel like just playing with this stuff is sometimes the fastest way to get some intuition around it and what it can do.
So definitely go play with it.


Calle: 02:12:40

Yeah, on that, just reach out to me.
I mean, I know there are people who want to get started building on Bitcoin and whatever project interests you, if it's FediMint, if it's Cashu, if it's another Bitcoin-based project, independent of what we have just talked about today, we need more Bitcoiners.
Literally, this is your moment.
Dive in, start with stupid things, just have fun, and you will find things that interest you.
And if you want to play with Cashu, please look at it.
It's extremely simple.
You can build a JavaScript application doing e-cash stuff in literally a couple of hours or so.
So look at the documentation on Cashu.space.
If you have any questions, Calle BTC, that's me.
I will hold your hands and show you the way, the nut.
I will show you the nut.

NVK: 02:13:23

Yeah, Calle, where can people find your nuts?

Calle: 02:13:26

My nuts are usually positioned on Nostr or on Twitter, on the Calle BTC, but that's the last thing I'll say.

NVK: 02:13:34

Thank you.
Eric, any final thoughts?

Eric: 02:13:37

Yeah.
So if people want to learn more about Fedimint, visit Fedimint.org.
We have some great explainers there or look it up on github.com slash Fedimint slash Fedimint.
I think we went into a lot of interesting topics today.
So thanks for having me and yeah, looking forward to working together with everyone, especially with Cashu.
Like the project has always led to some new insights.
Like I think by working together, we can build something much stronger.
So yeah.

NVK: 02:14:08

Well, thank you guys.
And I think any mobile dev out there, please, somebody, please make a Cashu Fedi, like an e-cash wallet that has proper integrations with Lightning like as an actual app, because I think what's missing right now is like a very, very friendly way for you to just like send and receive that does not involve a web.
I think that would be super, super cool.
And I think you can probably find monetization to that, like not too far from now, you're going to be ahead of everybody.
I think it's going to be a very common thing the same way, lightning while it's exploded.
So, I guess with that, I mean, again, thank you so much.
This was absolutely awesome.
We're going to do more of this stuff about layer three at some point soon.
We're going to put layer three on the name of the episode until Calle's nuts explode.
So thank you.
Thank you so much, guys.
You have a great day.

Calle: 02:15:09

Amazing.
Thank you for having us.

Eric: 02:15:11

Thank you.
Have a great day.

NVK: 02:15:16

Thanks for listening.
For more resources, check the show notes.
We put a lot of effort into them.
And remember, we don't have a crystal ball, so let us know about your project.
Visit bitcoin.review to find out how to get in touch.
