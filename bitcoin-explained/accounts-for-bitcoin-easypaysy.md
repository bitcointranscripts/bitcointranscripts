---
title: Accounts for Bitcoin, Easypaysy!
transcript_by: tijuan1 via review.btctranscripts.com
media: https://www.youtube.com/watch?v=AyjU0EJZjR8
speakers:
  - Sjors Provoost
  - Aaron van Wirdum
tags:
  - silent-payments
date: 2020-10-02
episode: 11
summary: In this episode Sjors and Aaron discuss Jose Femenias' Easypaysy proposal, an account system for Bitcoin, on Bitcoin
aliases:
  - /bitcoin-magazine/bitcoin-explained/accounts-for-bitcoin-easypaysy
---
## Intro

Aaron: 00:01:10

Sjors how do you like reusing addresses?

Sjors: 00:01:13

I love reusing addresses, it's amazing.

Aaron: 00:01:16

It's so convenient isn't it

Sjors: 00:01:18

It just makes you feel like you know your exchange if you're sending them money they know everything about you and they like that right?

Aaron: 00:01:26

It's so convenient, it's so easy, nothing to complain about here.

Sjors: 00:01:30

Absolutely.

Aaron: 00:01:31

So that was our episode.

Sjors: 00:01:33

Thank you for listening.

Aaron: 00:01:34

Okay, actually, I think everyone will know reusing addresses is a horrible idea.

Sjors: 00:01:39

Absolutely.

Aaron: 00:01:39

You're giving away all your privacy.
I guess that's the main problem, right?
You're just giving away your privacy.
I guess In the long run, there's maybe some sort of quantum risk, but we mostly care about privacy.
You're giving away your own privacy, and also you're compromising the privacy of everyone you're interacting with.
Because if you give away your privacy, that means everyone who's paying you, blockchain analysts can figure out that they're paying you and the other way around if you're paying people.
So it's compromising everyone's privacy.
While it's very convenient, it's something we shouldn't be doing, is it, Sjors?

Sjors: 00:02:17

Exactly.
That's why most wallets have a button called get new address and some good wallets will actually automatically make a new address whenever you even click on receive.
Some wallets don't.

Aaron: 00:02:30

All right, so that works.
We need to generate a new address for each payment we receive.
However, Sjors, this is a little bit inconvenient as well, isn't it?

Sjors: 00:02:38

It can be.

## Why accounts would be useful intro to Easypaysy

Aaron: 00:02:39

So, here's the solution.
We need an account system for Bitcoin.
Or at least, it's possible to create an account system on Bitcoin and it could be useful.

Sjors: 00:02:49

I think the the word account has some negative connotations, but it'd be nice if you knew one thing about the other party and then you can keep sending the money while automatically using a new address.
I think that's what we want.

Aaron: 00:03:05

So, Jose Femenias Canuelo, that's probably a severe mispronunciation of his name, but Spanish developer Jose Femenias Canuelo, he also believes so.
He believes Bitcoin would benefit from an account system.
It's called Easypaysy, which is short for Easy Payment System, I think.
Easypaysy, and that's what we're going to discuss today.

Sjors: 00:03:33

All right.

Aaron: 00:03:33

It's pretty clever and we'll get to possible downsides later, but let's first just explain how it works.

Sjors: 00:03:41

How does it work?
Because this time you're going to explain how this thing works.

## what is Easypaysy?

Aaron: 00:03:44

I'm going to do most of the explaining this time.
All right, so to generate an account, one of the clever things about this proposal is that it uses nothing outside of the Bitcoin blockchain itself, necessarily.
There's options to that, but we can do it all without any outside of blockchain thing.

Sjors: 00:04:06

By "thing" you don't mean wallets, but you mean there's no communication protocol, you don't have to run a server to communicate with the other person?

Aaron: 00:04:14

Exactly, we generate the account on the Bitcoin blockchain itself, and people can find the account on the Bitcoin blockchain itself.

Sjors: 00:04:22

Okay, so how do I generate an account?

Aaron: 00:04:24

An account is basically a transaction.
That's in this proposal what an account is.
And this transaction consists of one input, so one address where coins are sent from, but this one input is a multi-sig input, so it has two public keys.
It also has one output, which is one `OP_RETURN` output.

Sjors: 00:04:52

So you're sending some money from a multisig address that you control yourself to...

Aaron: 00:04:59

No input.
You're basically sending no money but you do need to pay a fee.
That's the only money that's involved in this transaction.
You're not actually spending anything to anyone, but you need a little bit of funds to have it confirmed.
The input does need to send some money, which is the fee, and then the output receives nothing.

Sjors: 00:05:17

And so the reason why we need a 2 of 2 multisig is...

Aaron: 00:05:22

There's two public keys in there.
These are basically your public keys at this point.
When you're making this transaction, you're announcing to the world, these are my two public keys.
One public key is your identity public key or...
One of them is for communication anyways.
I forget, there's a term for it, which I'm, which is slipping my mind right now, but one of them is for communication.
If you want to send me some kind of message, you use this public key, which I think is the first of the two - it's just an order.
The first one is for communication, and then the second one is for value.
I think the main reason there's two is that one is even more important than the other.
If you lose your communication key, that's a problem, but at least you're not losing money.
If you lose the value key, you're actually losing money.
What you can do is you can put the value key in cold storage in a safe, somewhere secure while you can still talk with people, communicate with people.
That way even if your computer is compromised and only your communication is compromised you still keep your funds.
That's why there's two basically.

Sjors: 00:06:35

It might be worth reminding the listener that so what you're doing here is you're funding your own or like putting a trivial amount in your own multi-sig address and then immediately spending from that multi-sig address and the reason you have to do the latter is because you reveal the keys when you're spending not when you're receiving.
So in order for the rest of the world to see what your keys are you have to spend from it.

Aaron: 00:06:58

That's a good addition indeed when you're spending to...
Well anyway no need to repeat you're right.
Okay so

Sjors: 00:07:05

Then the `OP_RETURN` message that's in the outputs of this transaction can communicate any other piece of information to the world.

Aaron: 00:07:12

You can basically communicate text in this output.
The text we're communicating here is a JSON message, and it includes the instructions for how to pay to this account.
That's the main thing it includes.

Sjors: 00:07:26

I doubt it's actually JSON.

Aaron: 00:07:29

I thought it was JSON.

Sjors: 00:07:30

It's some sort of serialized format, probably, that you can convert to JSON.
Because otherwise it would be very inefficient.

Aaron: 00:07:37

What Jose told me is it's a small JSON document.
You think that's probably a simplification?

Sjors: 00:07:44

Well I don't know I didn't read it in that level of detail.
There's only 80 bytes available in `OP_RETURN`.
You could use those 80 bytes to write ASCII characters, with an opening bracket and colons and all this stuff.
But you can also agree on a serialization format that could put way more information in a smaller space.

Aaron: 00:08:03

But you don't need to communicate a lot of data, you just need to tell people which kinds of transactions you're accepting on this account.

Sjors: 00:08:11

Sure, you can do it inefficient if there's not much data, but if you want more data you can do it more efficiently.

Aaron: 00:08:16

Okay, fair enough.
Anyway, so there's three ways of receiving funds on these accounts.
The first way is not recommended.
It's to receive payments on your value publicly.
So now we're back to reusing addresses.
We don't actually want that, but it's an option.

Sjors: 00:08:35

It's even worse than that, I guess, because you're announcing, "hey, this is where the money is going" to the whole world.
And then it's reusing addresses with everyone that you receive money from, plus everyone you're not even receiving money from.

Aaron: 00:08:49

It's bad.
It's in there because it's just an option for people to use.
You can choose not to use it, but if we're making this protocol, that was Jose's reasoning, we might as well include it for people who do want to use it.
It's a little bit like donation addresses.
Some people do use a donation address, which is just one address they post on a website somewhere, and anyone can pay to this address.
While it's not ideal, it's an option for people that insist on compromising their privacy.

Sjors: 00:09:21

Okay, what's the other option?

Aaron: 00:09:23

Okay, so the one I just described, that's type zero.
And then type one is the next option, which uses the communication key basically to request an address.

Sjors: 00:09:43

Okay, how do you request an address?

Aaron: 00:09:44

There's different ways of doing it.
You can do it through mail.
This is not specified in the protocol.

Sjors: 00:09:50

Okay, so this is where you do need some back and forth communication.

Aaron: 00:09:52

Yes, this one is interactive.
You can request it through email or maybe signal or maybe some other, maybe snail mail, however you want.

Sjors: 00:10:02

But this to me sounds like what we're already doing, where giving people unique addresses.

Aaron: 00:10:06

This is pretty similar to that indeed.
This is just one of the options in the account system.
It's not all groundbreaking.

Sjors: 00:10:13

Tell me about this groundbreaking third option, before I fall asleep.
No, just kidding.
Keep going.

Aaron: 00:10:19

One of the interesting things here, I would argue, is that you're still signing it with your communication key to sort of prove that it's you who's requesting the payment, which can come in handy later on.
That was type one.

Then type two, this closely resembles stealth addresses.
This is where it gets a little bit more complicated.
This is where the sender of the transaction takes the recipients, so the account holders value key, and the sender himself generates a public key and a private key.
He uses his key pair in combination with the recipients, the account holders public key to generate a new key pair.
And then he sends the funds to the public key or to the address that corresponds to this newly generated key pair.
So the money is going there.
In this transaction, he also includes another `OP_RETURN` in which the public key is included.
The public key he generated himself and with this public key, the account holder can use this public key to regenerate the new key pair and thereby he can spend the funds.


The way this works, if you're an account holder, is you need to know that this transaction happened.
There's two ways of figuring that out.
One of them is that the sender just tells you like, "hey, I sent you some money, look at that transaction and you can use it with the information in `OP_RETURN` to generate a private key which you can use to spend the money".
Or the account holder just needs to scan the blockchain to see if there are any transactions with an `OP_RETURN` in there and if there is see if there's information in there that he can use to generate this new key pair that actually matches and that actually lets him spend the coins.
In which case he just finds money on the blockchain basically so he knows he's been paid.
This is a little bit of a hassle of course, because it requires scanning of the blockchain and all of that.
It's relatively private, because even though the value key was revealed in his account, this new money isn't sent to anything that anyone can link to the account by just looking at the blockchain.
It's sent to a completely new address, which even the recipients, the account holder, didn't know at first and had to figure out.
Therefore, it does offer nice privacy features.

Sjors: 00:12:57

I'd say that's quite nice.
The privacy gotcha there that I would think about is that when you as the recipient you first publish you know your identifier, your account...

Aaron: 00:13:08

Let's first explain that and then you get to the privacy gotcha.
Like what the identifier is?

Sjors: 00:13:16

Oh what the identifier is, yeah sure you can do that.

Aaron: 00:13:19

So how do people find your account?
As mentioned, it's just a transaction.
It's a Bitcoin transaction that's going to be included in the blockchain.
So the place where it is included in the blockchain, that is the identifier.

Sjors: 00:13:32

For example, the block height plus the place in the block.

Aaron: 00:13:35

That's exactly what it is.
Not for example, that's exactly what it is.
So the block height is, I don't know, 578331.
I'm just making something up.

Sjors: 00:13:47

You're one of those old schoolers that still remembers blocks in the 500,000 range.

Aaron: 00:13:52

No, I think that's what I used in my article when I wrote this.
That's why it's still sort of stuck in my head.
I didn't use this exact number, but somewhere in the 500k range, I think.
And then it's like the 738th in the blockchain and then the actual account identifier is, if I'm recalling correctly, it starts with the actual blockchain.
If it's Bitcoin, it's like BTC at 500, whatever number I just used in the 500k range, dot and then 700, whichever one I just used, and then I think there's a slash and there's a checksum.
Then you have this identifier, which is based on the place in the blockchain.
There are ways where you can revert.
That's not the right word.

Sjors: 00:14:45

I think what you were going to say is it's going to convert to some nice mnemonic style.
So a couple of words like "rabbit, big, fish".

Aaron: 00:14:54

Exactly.
Right now I was unable to remember the exact numbers I used, but if I would have used a mnemonic in the first place, "Rabbit, fish", I already forgot.

Sjors: 00:15:03

Yeah, "rabbit, big, fish".

Aaron: 00:15:04

Whatever it was.
That's much easier to remember.

Sjors: 00:15:07

That makes sense.

Aaron: 00:15:08

Then you can remember it and you can tell people and you don't forget.
It's much easier to remember.

Sjors: 00:15:13

And you can go on TV and say, remember "rabbit, big, fish".
Then people can send money to "rabbit, big, fish".
And maybe that's slightly easier than giving them an address, though I'm a little skeptical whether that short name is such a big deal.
But this is kind of where we get the privacy gotcha and also the stealth address part.

Aaron: 00:15:31

Let's hear it.

Sjors: 00:15:32

The first time you're using this as a recipient, you're going to create an account, you're going to put a transaction on the blockchain.
If then later on you receive coins, we're going to assume you use this third methodology, the nice privacy thing, it's going to arrive on different addresses.
So that's very nice.
But, if you're stupid, or if your wallet is stupid, it's going to combine coins that, you know, are related to that first transaction.
The first transaction itself is not spendable because it's an `OP_RETURN`, but maybe it comes from another coin.

Aaron: 00:16:04

Sure.

Sjors: 00:16:05

And now you start combining coins and somebody can link your identity to everything you received.
So you still need to be very wary of this cluster analysis risk.
A new wallet could avoid that and warn you about it.

Aaron: 00:16:17

No, that's true.
You have coins in your wallet which you're going to use to pay the fee.
You probably have more in your wallet than just the fees, so you have change and it's then sort of linked to your account.
And then after which the coins can be linked to even the coins you received privately.
And that's something to be aware of, sure.

Sjors: 00:16:40

So I think it's this initial step where you have to announce something on the blockchain that creates this liability almost.
Now for some parties that's actually kind of a feature or at least they can manage it.
If you're an exchange, you know what you're doing, you're not gonna make those privacy mistakes.
And one of the cool things is that you can, you can, you know, add a DNS record is one of the suggestions so that people can verify that, hey, this DNS record matches this big fish thing.
And that's a nice way to double check.
I could imagine hardware wallets could also embed some of these well-known codes so that if you're sending to Kraken or whatever, your hardware wallet could say, oh yeah that's actually an address that belongs to that exchange, at least the last time we we updated the firmware to know these accounts.
It's kind of nice against clipboard attacks and that sort of stuff.
But that's for these schemes in general.
I don't think you need to have this announcement into blockchain specifically.
So if you go to stealth addresses, which I believe is BIP47, mechanism there was slightly different, though I might remember it incorrectly.
But the idea there is that you generate a payment code, which is longer, but it's not something you have to put on the blockchain.
And so you can give that code to somebody else, and that's your identity, but that identity is not tied to anything in the blockchain.
And then you do the same magic trick with somebody takes their own key and adds it and does a bunch of math and then sends it to an address.
And then I think there is an announcement on the blockchain, but it's done by the sender.

Aaron: 00:18:15

It's always done by the sender.
At least the payment is...
Oh, there's a separate announcement from the payment?

## Explaining Stealth Address Identities

Sjors: 00:18:21

So in the scheme we just talked about in Easypaysy, it's the recipient who has to announce their identity on the blockchain, essentially once.
But then when you want to send to them, there's some back and forth.
But here in the stealth addresses scheme, it is the sender that needs to make an announcement on the blockchain saying, to a standard address, hey, so they get a payment code and they send one transaction to a standardized address, which is always the same thing, as a handshake.
And then using the handshake, that's how you come up with the unique addresses that you're actually going to use.
So the recipient will watch the handshake address and every time it sees a transaction on the handshake address it then knows what other addresses it should be watching.

Aaron: 00:19:07

Okay so that does require more blockchain transactions then.

Sjors: 00:19:12

I don't know about the number of blockchain transactions, maybe a little bit, but the nice thing is that it's the senders that are sort of sacrificing their privacy, but only really to the recipient and they're doing that anyway, because they're paying the recipient, rather than the recipient revealing it, you know, lowering its privacy.
But I don't think it's a huge deal and all of these schemes you can choose to just do more off-chain.
You can just have an identifier that you send via email and yeah it's not as short, that's a downside, but it's just a public key in that case and you can do fun things with it.

Aaron: 00:19:48

You want to get into the benefits of this system

## Debating Use Cases for Easypaysy

Sjors: 00:19:51

We did some benefits and some downsides.
I would like to remind the listeners of a chicken-egg problem that was brought up by the infamous ZmnSCPxj.

Aaron: 00:20:04

Z-Man.

Sjors: 00:20:05

Z-Man, or as the Canadians say, Zetman.
If you're a new Bitcoin user and you want to use this system, you don't have coins to send anywhere.
So that's a problem, but there might be ways around it, especially if you're buying coins from an exchange, maybe they can help you set it up.

Aaron: 00:20:23

I want to get into more benefits, Sjors.

Sjors: 00:20:25

Okay.

Aaron: 00:20:26

I think we skipped over the benefits a little bit.

Sjors: 00:20:28

I mentioned a few, but give me more.

Aaron: 00:20:30

Recurring payments.
Did we mention that one?

Sjors: 00:20:32

No, we haven't mentioned that, that's a good one.

Aaron: 00:20:34

So recurring payments, so you want to pay rent every month, so your landlord would have to generate a new address every month and, wait, why is this a problem?

Sjors: 00:20:46

You could say it's annoying for the landlord to have to send you an email with an address every month.

Aaron: 00:20:51

Exactly.

Sjors: 00:20:52

And then it's nice if you can generate, if you can predict these addresses yourself.
But I would immediately say there's a downside to that, because if, let's say my landlord has this magic box that he receives his Bitcoin on and then his magic box breaks but he can't give you a phone call to say "hey yo don't send me any more Bitcoins" then your rent just goes into the ether.

Aaron: 00:21:18

He can call you, right?
He knows where you live.

Sjors: 00:21:22

He does know where you live.

Aaron: 00:21:24

He probably does.
He can ring the bell.

Sjors: 00:21:25

But maybe the postal service is down because of some election issue.
So, you know, it can be tricky.
And more generally, let's say you are a very sophisticated recipient of these Bitcoins, maybe you are a landlord and initially you just have a you know you have one tenant that pays rent that way and you just use your little hardware wallet and you generate these addresses that way.
All is good and well then you have lots of customers and you have a lot of money.
Maybe you want to set up a multi-sig cold storage.
Oh but now you have to tell all your clients or your renters to basically use this new payment code.
So it's nice if you can just give a new address every month then the customer doesn't have to care how you generate that address.
You can do it yourself.
You can have all the sophisticated address generation methods you want.

Aaron: 00:22:15

Sure but here's the thing I think your argument doesn't hold up because I think the idea is that if you're the landlord, you can request payment each month.
You just send a message, hey, pay me.
And then your wallets can be programmed to allow this once a month for up to whatever your pay is.
That way your wallet doesn't need to know all of the addresses into the future.
It just needs to know, okay, it's okay to pay this amount to this account each month, whenever they request it.

Sjors: 00:22:46

But then we really don't need anything in this scheme.
Because now what you're talking about is saying okay, our landlord has some sort of public key identifier that you somehow trust, maybe trust on first use.
It could be a PGP key or it could be some other, just a Bitcoin key, that your wallet and then there's a protocol where your wallet, where they can request payments from you.
Whether that's push-based or pull-based, maybe your wallet is running and it's pulling the landlord's server every day to say, "hey do you have an invoice for me, do you have an invoice for me?".
And then based on some rules you automatically pay it.

Sjors: 00:23:21

I don't think this scheme makes that easier.
The biggest complication there is just the okay what does the server look like that you're going to ping what's expected from a wallet should it ping every day, every week, every month, what if it doesn't?
So that is an interesting problem to solve but I think that's almost perpendicular to this.

Aaron: 00:23:39

Okay then I think the other big benefit is non-repudiation.

Sjors: 00:23:44

Tell me what is repudiation and what is non-repudiation?

## Aaron explaining what non-repudiation is

Aaron: 00:23:47

So I don't know what repudiation is, but I can perfectly explain what non-repudiation is.
So I guess repudiation will be the opposite of that.
It means that once you've paid someone, you can prove that you've paid someone.

Sjors: 00:24:02

Okay.

Aaron: 00:24:02

So you make some sort of order, I don't know, you order to buy a laptop or a teakettle, I'm just pointing at stuff on your desk right now.

Sjors: 00:24:13

A teapot.

Aaron: 00:24:15

That's what it is.
That's what you're ordering and then the seller receives the money and after it doesn't ship the order and then when you complain, he says, hey, I never received any money.
I don't know what you're talking about.
I don't know who you are.
Go away.
At that point, now with Bitcoin, once you've sent it to a regular Bitcoin address, you have no way to prove that you actually did pay this guy.

Sjors: 00:24:38

Depending on how you got the address, right?

Aaron: 00:24:41

I guess, I guess.

Sjors: 00:24:42

If you got the address on a website, and then...

Aaron: 00:24:44

But I want to solve it on the Bitcoin blockchain.
So now we're solving it on the Bitcoin blockchain.

Sjors: 00:24:49

But you want to do everything on the blockchain.
You sound like an Ethereum person.
I'm trying to make you a...

Aaron: 00:24:54

Just hear me out because I want to finish my story.
At this point, normally when you're just sending an address, that guy can just ignore you and claim that he never received a payment.
Now, thanks to the brilliance of non-repudiation, I can take it to court and I can prove to court, look, this is his account.
Look, I actually made a payment to this account, I can prove it, he signed it with his communication key or this is his stealth address, I can prove it in all sorts of ways and at that point there's no way for him to deny that he got the payment.
So now the judge can order him to finally give me that laptop or tea kettle.

Sjors: 00:25:36

Right, or less radical, you can use it in your accounting software.
So there's a little bit of an extra check.
That payments actually happened where you think they happened.

Aaron: 00:25:43

So you do agree there's a benefit now?

Sjors: 00:25:45

I think in general there's a benefit of having receipts essentially.
And basically when you receive an invoice, you really need to have some evidence that you really got that invoice.
So normally if you send an invoice by PDF or via email, it should have the address in it.
And that email should be signed by something, maybe just the standard email DKIM whatever stuff.
And then the proof of payment really is just that address now has money.
But okay, so that's all cool.
Great.

Aaron: 00:26:16

But there's more.
There's more.

Sjors: 00:26:18

Tell me.

Aaron: 00:26:18

Okay.
So actually I got an email from Jose earlier this month.
There's updates to the protocol.

Sjors: 00:26:23

Because just for the listener, this protocol was announced in December.
Then there were some distractions in the world and I guess.

Aaron: 00:26:30

Oh, last December?

Sjors: 00:26:31

Now he's back on it.

Aaron: 00:26:34

I'm going to read the updates to you.

Sjors: 00:26:37

Okay.

## Updates to the Easypaysy Protocol

Aaron: 00:26:38

Okay.
Update A.
Vertical simplification.
Interactive payments: most of the scaling solutions, and a few other minor things will be left out of the first implementation of the protocol.

Sjors: 00:26:50

Okay, we didn't really talk about the relations to Lightning because that's even more complicated, but what was the first bit again?

Aaron: 00:26:56

So interactive payments, that's going to be left out.

Sjors: 00:26:59

And interactive payments, was that the second method you were talking about?

Aaron: 00:27:01

I think so.

Sjors: 00:27:02

Okay, so we already dropped that and now he's dropped it.

Aaron: 00:27:06

Cool.
Okay.
(Update) B: leaner and more powerful transactions.
Do you know what IOC transactions are?

Sjors: 00:27:14

I think that was the cryptographic protocol we were talking about.

Aaron: 00:27:19

Stealth one?

Sjors: 00:27:20

The stealthy address.

Aaron: 00:27:22

Okay okay so IOC transactions don't need the `OP_RETURN` anymore so easypaysy transactions can be as lean as any regular Bitcoin transaction now.

Sjors: 00:27:33

Okay, that sounds good for privacy too.
Like not having these these upper turn things everywhere.
Okay.

Aaron: 00:27:40

(Update) C: Support for SPV wallets.
There is a new discovery mechanism that allows for simple support for SPV wallets.

Sjors: 00:27:48

Because we didn't really touch on that, but if you need to monitor the blockchain, that's a little bit more difficult for lightweight wallets to do than for full-fledged wallets.

Aaron: 00:27:56

So apparently that's solved.

Sjors: 00:27:58

Okay, great.

Aaron: 00:27:59

(Update) D: The business model.
As a side effect, the discovery mechanism needed to support SPV wallets opens up the door to having a business model for Easypaysy, since it will now generate revenue for investors and wallet developers.

Sjors: 00:28:14

I thought it was an open protocol.

Aaron: 00:28:16

None of this is really explained in the email or maybe if I would take the effort and read the PDF.
That's maybe for another time.

Sjors: 00:28:24

Let's stick to the main technical points here.
I mean everybody, you know people, usually you have a business that adds, contributes to the ecosystem with a standard or with some code and they might have their own plan for how to monetize that which doesn't have to be a problem.

Aaron: 00:28:38

That's all I have Sjors.
You don't sound very impressed.

Sjors: 00:28:43

I mean...

Aaron: 00:28:43

you sound mildly...

Sjors: 00:28:45

I was around in the BIP47 days, and there's still only I think one wallet that sort of supports it.

Aaron: 00:28:51

Which is Samurai?

Sjors: 00:28:53

So I do think we need something like this.
So in that sense, I am happy that people are working on trying to figure out a good standard for some sort of identity, not in the KYC sense, but in the sense that I know that I'm actually paying this shop that I think I'm paying and some sort of way to make address reuse really hard.
Although I think part of that is already solved.
I think projects like BTCPay Server have made it ridiculously easy for at least for shops to just never use the same address.
Exchanges should just never use the same address, otherwise they're just completely incompetent.
One thing that might be worth noting is there's a development in Lightning by Rusty, who's proposed a system where normally with Lightning you scan an invoice, that's a QR code somewhere, and you pay it.
That's it.
But this proposal would basically have a QR code where if you scan it, you ping the node, then you get an invoice and you pay it.
That might sound trivial, but it means that you can stick a QR code on an orange in the supermarket and like multiple people can buy an orange basically and get a unique invoice for it.
And you can adjust the price real time rather than having everything fixed.
Because if you put an actual Lightning invoice on an orange, then after a week the price might be completely wrong.
So in this case your orange is more like an identifier that says, hey go to this lightning node and ask me about the price of the orange.
And that sort of solves a lot of these problems too.
So you can have fixed identities.
The orange could have an identity or it's probably the supermarket that sells the orange.
And So you get sort of the same thing.
You can also do recurring payments and all these cool things.

Aaron: 00:30:37

With an orange?

Sjors: 00:30:38

With an orange, yes.
But the thing is, I think there should also be systems like this for just regular Bitcoin transactions.

Aaron: 00:30:48

What you're saying is it's basically solved for Lightning or there's a very, but..

Sjors: 00:30:53

It's not solved for Lightning, but it is easier to solve for Lightning, because Lightning you have to have a running node anyway.

Aaron: 00:30:58

And that's one of the critiques that I've heard of this solution as well, that why focus on on-chain, let's just move this type of stuff to Lightning.

Sjors: 00:31:09

You could for smaller payments, but I don't want to pay my rent with Lightning.

Aaron: 00:31:12

Exactly, what you're saying is, no, no, it would actually be good to have it on-chain as well.
It's just you're not necessarily convinced that Easypaysy is the way to go.

Sjors: 00:31:21

No, but I'm not saying there's any other specific way to go.
My guess is because there's so many different ways to go and not a lot of people are enthusiastic about building it, it's gonna be in a bike shedding-ish state for many more years.
So my hope is that on Lightning we'll get all this sorted out more quickly and then maybe whatever happens on Lightning can inspire on chain.
Or for that matter maybe you just run your Lightning Node software and let it hand out some on-chain addresses when needed.
So Lightning might be the default, but for big payments you do use on-chain, but you use all the Lightning protocol stuff, including the encryption and the routing and the 24-7 server to take care of generating on-chain addresses and verifying payments.
Something like that.
That's all I have.

Aaron: 00:32:15

I'm through.
All right.
I was just thinking of that XRCP or whatever XKCD cartoon about standards.

Sjors: 00:32:26

Oh yeah, let's make another standard.

Aaron: 00:32:28

Yes.
All right.
Anyways.

Sjors: 00:32:31

Should we close it out?

Aaron: 00:32:32

Let's do that.

Sjors: 00:32:33

All right, everybody.
Thank you for listening to The Van Wirdum Sjorsnado.

Aaron: 00:32:38

There you go.
