---
title: Silent Payments
transcript_by: nymius via review.btctranscripts.com
media: https://www.youtube.com/watch?v=Cqmk2cZ2IjM
tags:
  - silent-payments
speakers:
  - Christoph Ono
  - Michael Haase
  - Yashraj
  - Josibake
date: 2024-01-31
summary: Silent payments are introduced as a method to enhance Bitcoin transactions' privacy and usability by addressing the issue of address reuse. Unlike traditional methods, silent payments use elliptic curve Diffie-Hellman (ECDH) to generate unique addresses for each transaction without interaction. This preserves user privacy and simplifies the process. Josibake explains the design rationale, technical challenges, and implementation strategies. He emphasizes the need for widespread adoption of sending capabilities and highlights the potential applications in exchanges and other services. The discussion also covers the trade-offs between privacy and computational overhead, proposing solutions to ensure efficient implementation and user education.
aliases:
  - /bitcoin-design/learning-bitcoin-and-design/silent-payments/
---
## Introduction

Christoph Ono: 00:00:02

So welcome everyone.
Super excited to have this call here today.
And we are in Learning Bitcoin and Design call number 16.
Hilariously, we had number 17 this morning, because we move things around time-wise.
But this is number 16 about silent payments.
We have the super expert Josie here, who is willing to talk us through what silent payments are and how they work.
So I'll just hand it over to Josie to kick us off and we can organically feel out where we should take this conversation.
Feel free to kick us off if you'd like to, you can just talk to us for 20 minutes, give an overview, or if you prefer a more conversational format, that works as well.
Hopefully, we have lots of time for everyone to ask questions and get those answered too.

Josibake: 00:01:01

Yeah, for me personally, first I'll preface, you guys got the bait and switch.
I'm not the super expert.
That's Ruben Somsen, who isn't here with us today.
Ruben Somsen was the original author of the silent payment scheme.
I am the super expert sidekick.
I am someone who got really excited about silent payments when I heard about it and then started helping Ruben out.
So how I've been helping is co-authoring the BIP with him.
We've been working on that for a while now, just formalizing the spec, coming up with test vectors for wallet implementations.
I've also been working on a silent payments implementation for Bitcoin Core.
And on the side, looking for other ways with different libraries to help out.
In terms of the format, I much prefer a conversational, more informal way of doing things.
So I'll launch into an overview, but I would encourage anybody who has questions, just feel free to jump in and ask questions.
If I say something that you don't understand, don't wait for later, just interrupt me, because then I feel like we're all using each other's time really efficiently, and make sure that we clear up any gray areas.
I'll launch in with like a high-level overview, but like I said, raise your hand or stop me if something doesn't make sense.

## Background on Silent Payments

Josibake: 00:02:32

Silent payments is kind of the nth iteration of a pretty old idea in Bitcoin, which is stealth addresses.
Maybe you've seen in other places people have a static address which is an account and rather than go through the flow of always handing someone a fresh address, there's these concepts in other cryptocurrencies and other projects of this static payment identifier.
The original idea goes way back to like 2012 or 2014, somewhere around that era, where people were talking about stealth addresses.
The idea of a stealth address is you have a static code and people can send Bitcoin to you using that static code and they can use it over and over again.
It becomes more like a routing number.
If you're a bank, you have a routing number.
Once I have your routing number, I can just send money to you whenever I want without interacting with you to get some code or confirmation.
The thing about stealth addresses is they do this in a way that preserves user privacy.
Not just the user privacy, but the privacy of all the users of Bitcoin.
I'll talk about that more a little bit later.

## Current Challenges with Address Reuse

Josibake: 00:03:45

Today, if one of you wanted to send me Bitcoin, the only way to do it is you'd have to get in contact with me via messaging app or something, and you'd ask me for a fresh address.
I would give you a fresh address and then you would use it.
If the next day you want to send me Bitcoin again, you'd have to get in contact with me again, ask for a fresh address and so on and so forth.
This is a cumbersome process that a lot of us are used to at this point.
But if you're coming from any other, if you're not familiar with Bitcoin, you're used to more of like a Cash App or a Venmo or a PayPal-like experience, where you're like, "Hey, what's your tag or what's your email or what's your identifier? What's your routing number?"
And then once I have that number, I save you as a contact and I can just send stuff to you whenever I want.
That's the user experience that a lot of people are used to.
So it can be very jarring when they come to Bitcoin.
And it's like, "Oh, I have this interactive process where I have to ask for a fresh address."
Because of this friction, people often tend to do the bad thing of just reusing the same address.
You'll see people will post a Bitcoin address in their Twitter profile or their GitHub, or they'll give you an address and instead of reaching out to talk to them again, you might be tempted to just reuse the same address.
There's nothing in Bitcoin that stops you from reusing the same address.

## Privacy Issues with Address Reuse

Josibake: 00:04:58

The problem is that the same address shows up on-chain multiple times.
So now someone from the outside can say, "Ah, whoever owns this address has received X number of payments, holds this much."
They can see the transactions that paid them.
You can now start to cluster a lot of activity.
When enough people do this, you can cluster things.
Exchanges are big offenders here, posting static deposit addresses, and then everybody knows that any transactions to that address are actually someone depositing to an exchange.
It limits the anonymity set of everybody else who's not doing that.
It makes it easier to hurt the privacy of everybody who's using Bitcoin when we have this widespread on-chain address reuse.
It also hurts your own privacy.
If I post an address on my Twitter profile and say, "Hey, if you're happy with the work I'm doing on Bitcoin, send me some Bitcoin."
Anybody can come over to my Twitter profile, just look up that address in an address explorer and see how many times people have donated, what amounts.
If they're a chain analysis firm, they can start to look at those people who donated and start to look at their UTXOs that they spent, which maybe leads to uncovering someone's identity.

## Silent Payments Overview

Josibake: 00:06:04

So we've got all these problems, and yet this is what people are most inclined to do because it's not a normal payment experience that we're used to, having to constantly interact with the person to get fresh payment information.
That's the idea that these stealth addresses are trying to solve.
The idea is very simple.
I'll just talk about silent payments right now and then maybe later we can talk about comparisons to other things that have tried to solve this problem.
With silent payments, I will post this new address format called a silent payment address.
It'll start with `sp1q` instead of `bc1q`.
So it's clear that this is not a regular Bitcoin address.
It's going to be a little bit longer than a regular Bitcoin address.

Yashraj: 00:07:00

So why did we make this decision about making the silent payment address visually recognizable by a regular person?
Can't we simply delegate all of that to the wallet software or something?

Josibake: 00:07:17

Yeah, that's a great question.
Addresses are meant to be this human-readable component for Bitcoin, right?
If we think about what a Bitcoin address is, we've got the `scriptPubKey`, and the `scriptPubKey` is actually what goes into the blockchain, but that's cumbersome.
So we encode `scriptPubKey`s into addresses, and the addresses have this recognizable format to them.
Like, segwit addresses always start with `bc1q` or `bc1p`.
We have SegWit version 0 addresses, which is `bc1q`, and Taproot SegWit version 1, which is `bc1p`.
So just looking at the address as a human, you can be like, "Ah, that's a Taproot address, that's a SegWit address."
They're also a little bit more compact than the full `scriptPubKey`.
The `bech32` and `bech32m` encodings are meant to remove ambiguous characters so that a human can quickly look at an address and verify, "Okay, this looks correct."
Addresses are already this convention meant for humans to use.
The wallet software takes care of decoding the address into the appropriate `scriptPubKey`s that the wallet understands.
With silent payments, we wanted to go the same direction and say we want something that you could show to a human being and they'd be like, "Oh, that's a silent payment address."
It would be very clear that it's not a regular Bitcoin address because we didn't want any confusion of like, "What's a Bitcoin address? What's a silent payment address?"
So the silent payment address is supposed to be something that people will recognize.
The wallet can parse that address and take care of doing the silent payments protocol.

Yashraj: 00:09:03

Another question on that one is if the wallet that I use does not support silent payment addresses, can these addresses be used like a regular address?

Josibake: 00:09:19

Yeah, that's another good question.
This is something that we discussed early on.
There's a whole section on this in the BIP discussion.
We talked about, "What if we use something like BIP 21 to do silent payments? Rather than come up with a new address format, let's just use existing ones."
My argument against doing that is, if a wallet doesn't understand silent payments and then it falls back to just using a static address, that could actually lead to more address reuse on-chain than before.
Currently, someone posts a taproot address and they're like, "Hey, anytime you want to send me Bitcoin, use this address."
This is horrible because of all the privacy concerns.
Then you have someone else who's like, "I don't really like that. I want to use silent payments. I wouldn't have posted just a static Bitcoin address anyways."
So now I'm going to post the silent payment address, so anyone who understands silent payments can send to me.
Anyone who doesn't will just fall back to using a static address, which means we've added one more person who's using a static address.
The whole idea of silent payments is we want to prevent any and all address reuse.
So it didn't make sense to allow this fallback mechanism, which would allow you to do something we're trying to avoid.

## Encouraging Adoption

Josibake: 00:10:39

We decided to tackle that problem differently, similar to how we did with Taproot.
When you launch a new protocol or a new address format, there will be a lot of people that don't understand how to use it.
So we designed the silent payment protocol so that sending and receiving are separate.
You can implement sending without receiving.
You could implement receiving without sending, but that doesn't make sense to me.
You can implement both.
The barrier to implementing sending is meant to be as small as possible.
We'd approach it like, if someone wants to use silent payments, the most important thing is that there are a bunch of wallets that understand how to parse that address format and can send to that address.
If there's one person in the world who wants to use silent payments and nobody else cares, we still need a lot of people who can send to a silent payment address.
So we separated the protocol into send and receive, tried to make sending as simple as possible.
The first phase of developer advocacy for silent payments will be focused on, "Hey, even if you don't care about this, can you support sending to a silent payment address?"
That way, even if your users don't want to use silent payments or they don't care about it, at least when they see a silent payment address in the wild, which is someone who's saying, "Hey, I care about receiving Bitcoin in a more private way with better UX," their wallet is able to send.
Then we can defer the more complicated problem of implementing receiving down the road.
The hope is that by making it as easy as possible to implement sending support, there will be widespread adoption for wallets to send.
The few wallets or people who really care about the receiving part can go build and do those as well.
If we had done the other way where you kind of have to implement the full protocol, it's less likely people would do it and it would slow down adoption.
You'd have this bad experience of trying to scan a silent payment address and it doesn't work.

Christoph Ono: 00:12:43

That's interesting.
The chicken and egg adoption type of problem seems like a common thing.
I remember the same with multi-language recovery phrases, where the first step was just to be able to read them.
Then to have one aspect of it that's easier, that kind of gets things rolling, and then hopefully leads to a full adoption later on.

Josibake: 00:13:07

It's particularly hard in an ecosystem like Bitcoin where you can't just go force people to do stuff.
You have to meet them where they're at and try to make things as easy for them.
A lot of wallets are run by volunteers or people who aren't getting paid, just passion projects.
So when you go and say, "Hey, I made this new protocol," they might respond with, "I don't care about that protocol."
You're asking people to do work to support it.
That's one area where we did try to put a lot of thought into it and learn from history where we've seen that work well or slow things down.

Christoph Ono: 00:13:40

Do you feel like that was a problem with adoption of the previous attempts at this or do you think there were different reasons?

Josibake: 00:13:49

It's hard to say.
When you look back at history, it's difficult to know what was going on at the time.
The previous attempts at solving the address reuse problem don't seem to have gained a lot of traction.
But it's difficult to say why that might be.
One thing is early on, I don't think people really cared that much about address reuse.
As we've seen more adoption and people care more about Bitcoin, we've realized this is really bad.
It doesn't just hurt my privacy, it hurts everyone's privacy.
In the early days when Bitcoin was just fun, I don't think anyone cared about that.
They were just like, "Oh yeah, just reuse the address."
I think Satoshi even had an original pay-to-IP address in Bitcoin, which is the worst possible thing you could do for privacy, but it's nice UX.
I think in previous versions, BIP 47 is the one that has the most traction.
It's a stealth address scheme.
I do wonder if having to implement the full send and receive for BIP 47 to work has limited their adoption.
I don't know if that's something they've experienced or not.
Requiring the full protocol is more work for wallet devs.

## How Silent Payments Work

Josibake: 00:15:09

Maybe someone watching this hasn't quite got the punchline yet.
What are we trying to do here?
I throw my silent payment address up somewhere.
You see that code, your wallet parses that code without interacting with me.
You find this address anywhere.
You could find it printed on a billboard.
You could find it in my GitHub.
The point is it's interactionless.
You don't have to text me or know who I am.
You just say, "Hey, I want to send some money to that address."
Your wallet sends to that address.
By following the silent payments protocol, it generates a guaranteed unique address that's never been used before, and that is only spendable by me.
Then you send money to that freshly generated address.
The next time you want to send money to me again, the whole process repeats with a freshly generated address.
Someone else can come along, use the same code and be guaranteed that they're not going to get an address that you might have previously used because they're also generating their own address fresh.

The way this works and how it's somewhat distinct from previous versions of stealth addresses and how people have tried to solve it, all of the information for generating that specific address is contained within the transaction itself.
To be more specific, you use the private keys of the UTXOs that you want to spend, which are only spendable by you and nobody else.
Use those private keys in that transaction in combination with the public keys in my silent payment address to do something called elliptic curve Diffie-Hellman.
Elliptic curve Diffie-Hellman is where two parties can exchange secret information in public and arrive at the shared secret that only they know.
So you use your private keys in conjunction with my public key to create a Taproot output that has never been created before and can only be created using your inputs that you spend and my silent payment address.
I scan through the transactions and I see the public keys in your inputs just by looking at the blockchain.
I use the private key corresponding to my silent payment address to do the reverse process to identify that this was a payment to me and also have all the data that I need to spend the output.
This means that there's no state, no crossover.
It's not like an `xpub` where if I put an `xpub` publicly and Christoph sends me some money to one and then somebody else simultaneously asks for a fresh address from the `xpub` and it gives me the same one that it gave Christoph because it hasn't registered that Christoph used it yet, you both might send to the same one.
There's no state management or anything like that.
There's also nothing that links any of these multiple payments from you to my silent payment address.

## Privacy Advantages

Josibake: 00:17:58

If you come to my silent payment address, let's say I'm the Signal Foundation, and I post a silent payment address that I want to receive monthly donations for people who want to support Signal, but I don't want to know who they are.
I don't even want to know if they're paying me every month.
Christoph donates on the first of the month in January, then donates on the first of the month in February.
There is no way from looking at those transactions that the Signal Foundation would be able to say, "Ah, these two payments on January and February came from the same person."
Each payment to a silent payment address is completely independent.
They're not groupable by sender in any way.
This is a really nice property for silent payments compared to something like BIP 47, which is more about establishing a payment channel.
You do this notification on-chain with an `OP_RETURN` or they have a few other mechanisms, but whatever the mechanism, you get this notification transaction out there.
That notification transaction sets up a way for the counterparty to be able to derive fresh addresses when they want to send to you from this `xpub`-like thing.
It's basically an `xpub`.
They encode the information you need to do an `xpub` into an operator and you decode it.
The issue with this, when you go back to that Signal Foundation example, they might not know Christoph's identity, but they'll see a payment that came in on the 1st of January and a payment that came in on the 1st of February.
From their wallet's perspective, their wallet can determine, "Ah, these two payments came from the same entity because they're both derived from the same notification that we used to establish this."

## Unique Properties of Silent Payments

Josibake: 00:19:36

These are two distinct areas where silent payments add some new and different properties that I don't think have been done yet with stealth addresses.
Silent payments do really well in privacy that all of these things have done, which is try to limit address reuse and add some additional guarantees of better sender privacy than other protocols.
Another exciting thing to me about silent payments is it's also a user experience improvement.
Privacy is usually more costly and more difficult.
Very rarely is the easiest way to do something also the most private way to do something.
That's a problem for users because some of us really care about privacy, others don't care about privacy and care more about having an easy experience.
Also not understanding that the decisions we make today might hurt our privacy in the future or might hurt the privacy of other people who do care.
So like you may not care about address reuse, but your address reuse hurts my privacy because even if I'm not reusing addresses.

We have to make privacy stuff as easy or easier than doing it the non-private way.
With silent payments, this is really nice because a silent payment transaction will not cost you anything more than a regular Bitcoin transaction.
You don't have to pay for a one-time notification.
You don't have to pay for any extra data in the transaction.
It's just a regular old Bitcoin transaction as if you had just been reusing the same address.
It also doesn't look any different than any other Bitcoin transaction, which is a nice property.
Someone from the outside can't tell that these things are silent payments.
But if you're a user who just does not care about privacy at all, and someone tells you, "Here's a way to send and receive Bitcoin that's a little bit more like a username or a routing number," it kind of Trojan horses the privacy in for them.
They're like, "Oh, yeah, this is easier than asking someone for a fresh address every time and it doesn't cost me anything more than a normal transaction. The user experience seems pretty much the same. Why wouldn't I use this?"
Then we've got people using Bitcoin more privately than they were before.

Christoph Ono: 00:21:53

Come for the static ID, stay for the privacy.

Josibake: 00:21:57

Yeah, right?

## Comparing to BOLT 12 for Lightning

Michael: 00:22:00

Hey, I'm Michael.
By the way, nice to meet you.
So it sounds like it's similar in principle to BOLT 12 for Lightning, right?
It's the same kind of routing number or unique identifier that in the background generates all the magic.
So that's really cool.

Josibake: 00:22:32

Yeah, BOLT 12 is another great example.
I think BOLT 12 is the analogy of this for Lightning.
In Lightning right now, Lightning is even more interactive than in Bitcoin.
If I give you a Bitcoin address, you can send money to it whenever you want.
If I give you a BOLT 11 Lightning invoice, you have to use it right before it expires, before I go offline.
BOLT 12 is handling that there.
My dream would be in the next X years, soon, TM, you would have a BIP 21 style QR code that starts with a BOLT 12 Lightning invoice and falls back to a silent payment address.
From a user experience, you have this static QR code that you could post anywhere, never have to change it.
People who use it will be using Lightning and Bitcoin in a more private way that doesn't have address reuse or any of these interactive go-betweens.
We need to see a lot more adoption before we get to something like that.
But that's the user experience that I'm envisioning, that I think we should be driving towards.
You try to scan a QR code, it tries to do it first with BOLT 12.
If it can't do it with BOLT 12, it falls back to a silent payment address.

Christoph Ono: 00:23:49

Very cool, very cool.
How's everyone doing here?
Everyone's very quiet.
If you have questions, you're welcome to put them in the chat, put them in the document here.
Trying to take some notes.
Feel free to ask anything.

## Trade-offs of Silent Payments

Yashraj: 00:24:07

Yeah.
I think, Josie, that was a very good explanation.
And also you really pointed out very well the benefits of silent payments.
I love that.
People could just listen to the conversation and get a quick summary.
That's awesome.

Josibake: 00:24:26

Yeah, I guess, like you said, I've done a good job of mentioning the benefits of silent payments.
Maybe I should spend a second and talk about some of the trade-offs because there's no such thing as a free lunch.
Ruben and I have not stumbled upon some mystery of the universe that nobody else thought of.
So I'll cover the trade-offs quickly because they are relevant.
If you have something like an `xpub`, an `xpub`, BIP 32, Hierarchically Deterministic Wallet, it allows you to pre-generate private keys and public keys before they've been used.
You know all possible addresses you could hand out in the future at any given time.
`xpub`s have been used as a way of mitigating address reuse in the past, but there are usability problems with that, which silent payments definitely improve on.
One being gap limit scanning.
You're never really sure with an `xpub`, and there's a lot of state management to make sure you're properly keeping track of which addresses you've used before so you don't accidentally hand them out again.
You can really only use an `xpub` per person.
I can't give the same `xpub` to Michael and Christoph because they'll both be choosing the next index to send to me and might step over each other and we end up with a problem.
So that was the idea with `xpub`s and then BIP 47 kind of took this and said, well, let's make an `xpub` per contact.
So we don't have any of that problem and then they manage their state.
So that's one idea there.

The benefit of the `xpub` approach is I can pre-compute these keys and then check for them to see if anybody has sent money to them.
I can do that check using the UTXO set.
The UTXO set says, "These are the `scriptPubKey`s that are currently unspent."
You go to the UTXO set and you're like, "I have these keys, which could be turned into `scriptPubKey`s. Let me see if any of those `scriptPubKey`s currently have any Bitcoin."
That's an easy way for you to scan.
If you want your wallet history, you fall back and scan the whole chain.

## Scanning Challenges with Silent Payments

Josibake: 00:26:30

With silent payments, it's a little different.
You can't pre-generate anything because the sender generates that address.
You have no knowledge of that address until the sender decides to send you money.
The sender generates the address and then uses it in a transaction.
It flips it.
The problem with that is to be aware of that, you need to scan the chain.
You need to be looking for transactions that have `scriptPubKey`s that look like they might have been generated with your silent payment address.
You can also scan the UTXO set.
The trade-off between an `xpub` style way of doing things or a BIP 32 where you pre-generate the addresses and the silent payment one, you have to scan the UTXO set for these outputs that are paying to you.
In order to do that, you need access to the input data of the transaction that created that output.
You don't have to scan the whole chain, but for an `xpub` style way of doing things, all you need is the `xpub` and the `scriptPubKey`s in the UTXO set.
For silent payments, you need the UTXO set and the inputs to the transaction that created that output in the UTXO set.
For full nodes, this is very easy.
They already have full access to the blockchain, all of the transactions, always available to them.
If you're already running a full node, there's not much extra overhead to run silent payments connected to that node.

## Light Client Implementation

Josibake: 00:27:56

For a light client, this is trickier.
They need this input data, which is one single pubkey representing the sum of the pubkeys used in that transaction.
It's about 33 bytes of data per transaction.
For light clients that don't have access to the full chain, they now need access to this 33 bytes per transaction to be able to check whether or not outputs in the UTXO set belong to them.
Tadge gave a talk at Baltic Honeybadger where he said it better than I had been able to express.
In silent payments, we are making the process overall less interactive.
The sender and receiver do not need to interact in order to complete a payment.
In order to facilitate that non-interaction, we're spending more in raw compute.
We have to do more scanning on the node side to find that data and use that data.
This is a great trade-off because of the benefits we get.
But it's worth mentioning.

Yashraj: 00:29:00

Yeah, quickly jumping in on that one.
I think that was a very good one that we have made this trade-off wherein we are replacing interaction and some other things that we used to do with just computing a lot of stuff.
My question leading into that is not a lot of people run full nodes already.
We have a lot of wallet users who are relying on their wallet provider running a full node somewhere else.
So how does this make silent payments harder to use, if at all?
And the second question would be the privacy implication of that.
Right now, I might have a non-custodial wallet that I use and do not regularly have to track my transactions.
But now that I'm using silent payment addresses, my assumption is that they would be the ones who would have to track the blockchain and my keys or something like that.
Is that true?
And if yes, what is the privacy implication of that?

Josibake: 00:30:18

Could you rephrase the first question again real quick?
We'll start there, then maybe jump onto the second one.

Yashraj: 00:30:23

Yeah, yeah.
My first question was regarding the fact that not a lot of people run full nodes already.
When they don't, there are some other trade-offs, like some other downsides.
So what would that be?
Then the second one was just focusing on the privacy aspect of that when it comes to the user and their wallet provider.

Josibake: 00:30:48

This is kind of bigger than just the topic of silent payments.
It's something that I care a lot about and have been doing a lot of thinking about.
Essentially, if you do not run your own full node today, there is no private wallet for you.
It just doesn't exist.
Most wallets out there are using the ElectrumX protocol, which there's Electrs, the original Python one, and everything like that.
The wallet is actually talking to the wallet provider server, and the wallet is querying for specific addresses, saying, "Can you tell me anything about this address?"
There's just no way to do this privately.
It just doesn't exist.
I think there's been some arguments about this in the past, where people have tried to claim that some of these things are private, but they're not.
The server could, you can claim, "Well, they're not doing it."
But if nothing prevents them from doing it, from a privacy threat modeling, you have to assume they're doing it.
You can't just take someone's word like, "Oh, we're not collecting logs."
So any wallet using ElectrumX as a backend is telling ElectrumX every single address that they're interested in.
"Can you tell me anything about this address?"
The server could be logging all of that, keeping track of that information, and you have very limited privacy.
The only private light client wallet protocol that I'm aware of today is BIP 158, which was originally conceived for these lightning nodes that wanted a private way to ask for information about what's spent in a block.
This you can actually use privacy with the trade-off that it takes a little bit more bandwidth.

In the BIP 158 world, full nodes create this compact filter for the whole block and say within this filter we encode every `scriptPubKey` that was spent or created.
Then the light clients ask for these filters and all that the node or the wallet provider learns at that point is a client was interested in this block.
They don't know anything about which addresses they were interested in.
They just know they wanted a block.
The light client gets that block and has this way of testing for existence.
If they have a `scriptPubKey` they want to check, they can test if it exists in that filter.
If it does exist in that filter, they ask for the block, either from the same person or a different node to better preserve their privacy.
They download the full block and have all the information they need to process the transaction they care about.
The nodes don't learn anything about the specific transaction.
This to me is the best that we have right now.
It's not really widely used by wallets.
A lot of people defer to using this Electrum style thing where you're just kind of telling the server, "Hey, this is exactly the transaction and the output that I'm listed in."

TLDR, if you're not running your own node, you're just not running a private light client today for the majority of wallets.
How this matters to silent payments is, as we started talking about silent payments and how we wanted to support light clients, in theory, it would work totally fine for a silent payments user to just hand their scan key to somebody else.
In the silent payments protocol, the address is composed of two keys, a spend key and a scan key.
The scan key is used for finding the transactions.
The spend key is used for spending the transactions.
Your spend key can be in super cold storage, never touches the internet, whatever, and your scan key can be hot online on a full node that either you own or somebody else owns and it's doing the scanning.
If you lose your scan key and give it up to somebody, you lose your privacy.
They can see all the transactions sent to your silent payment address, but they cannot spend them.

In theory, silent payments could also be used in a non-private way where someone gives their scan key to somebody else who's running a full node, either a wallet provider or whatever, and that person does the scanning on behalf of them and just tells them when they find a transaction.
This is very similar to how it works currently with Electrum.
For me, that's not super interesting.
I can't stop anybody from building that, but it's not interesting to me because the whole point of silent payments to me is usability along with privacy.
One of the things that I've been working on and researching is how could we use something like BIP 157 and 158 for supporting silent payments light clients?
I have some proof of concepts and ideas where what you would get from a full node is you would ask them, "For a block, give me all of the tweak data that I need," which is about 33 bytes per transaction that would be a silent payment transaction.
Also give me a BIP 158 filter for this block.
You're asking for two pieces of data.
You take that tweak data, generate the silent payment outputs privately on your device that you're interested to check.
Then you check if they exist in the filter.
If they exist in the filter, you ask another node or the same node for the full block, download the block, and process the transaction.
This way you could have a light client operating privately without needing the full blockchain.

You don't need the full blockchain.
The trade-off you're making is you need more bandwidth.
Instead of Electrum using the least bandwidth, BIP 158 uses a little more for the filters, and then silent payments would use more than that.
At least now, we're giving users the option.
If you want to run a light client and don't want to run a full node, here's an option to use a light client privately with more bandwidth than it would cost you to do it non-privately but less bandwidth than running a full node.

Yashraj: 00:36:42

Quickly jumping on that.
What you just described, this scan key providing that all of that stuff, the user does not explicitly need to do any of this themselves.
The wallet software can do this in the background.

Josibake: 00:37:01

Exactly.
From a user experience standpoint, I'll take BDK as an example.
In BDK, they have this work where they have composable backends.
You want to set up a wallet, you're building with BDK, and then you pick a backend.
I think they're working on compact block filters, BIP 158 as a backend, though it's not ready yet.
But you could say, "I want an Electrum backend. I want an RPC backend. I want it to connect to only my node or a node that I trust, or use one of BIP 158."
From the user's perspective, they don't care or know.
I mean, they should, right?
There's privacy implications for the backend.
But from the user perspective, they don't really know.
If the wallet's well designed from a user experience, they're clueless.
They just open up their wallet and see that it's doing stuff, but they don't know how it's getting that information.
It would be the same here, except that we would expect, if you have an Electrum style wallet versus a BIP 158 style wallet, the user would see more bandwidth consumption.
Maybe the wallet loading screen takes longer, there's more bandwidth.
Part of the UX challenge of silent payments would be explaining that trade-off to the user.
Why is my phone, my mobile phone, Bitcoin wallet operating slower than this other wallet?
Why is this app using more data?
There's a UX challenge of explaining to the user, "You're using more data because you're not giving up your privacy to another node.
You could use less data but then you're giving up all of your privacy."
People do care about that.
Even if they don't, we're allowing them to make that educated trade-off for themselves.

## Background Operations for Mobile Wallets

Michael: 00:38:45

But would they even notice?
One of the points is that you can send asynchronously, right?
You're not even in contact.
So the wallet could in regular intervals scan for incoming transactions and alert you only when it finds something.
It would already be kind of, I don't know how realistic that is or whether that's feasible, but the implications might not be that bad because you're probably a lot of the time not even expecting it, except if you really synchronously interact with the person paying you.

Josibake: 00:39:32

Yeah, I agree.
There are a lot of usage patterns where it wouldn't generally matter.
Having mobile apps do things in the background is very difficult.
People struggle with that.
Another thing is a lot of times people talk about push notifications, like their wallet alerting them of something.
I don't think push notifications can happen in a private way where the user is in control of the thing.
Imagine how most push notifications work.
You have your client connected to some server and that server is doing a bunch of work and things for you.
When that server finds something out, it proactively sends you information as the client.
By the nature of you outsourcing that work to the server, it usually means the server is learning a lot about you.
This comes up with BIP 158 style wallets.
If you have ElectrumX, an Electrs personal server running as your wallet backend, when it finds a transaction, it can proactively send you that notification.
The only way that that server knows to send you the notification is because it knows the transaction, which means you've lost all your privacy to the thing that is sending you the notification.

We kind of have to educate people.
You're going to use stuff more privately, you're not going to have the same user experience as non-private alternatives.
We shouldn't make that our goal.

Maybe there's some really clever way that, you know, I'm not aware of that we can do notifications in a more private way.
But what I imagine would be more the use case is: I have a Bitcoin mobile wallet on my phone and I'm using it on my phone because I don't want to run a full node or I don't have the ability to run a full node.
But I had this Bitcoin wallet that I'm using like somewhat infrequently.
I wouldn't expect that I'm pulling it up and using it every single day.
So I turn it on and I wanna, maybe there's some user initiated action of like, hey, scan for recent payments, or maybe when the app opens, it just starts scanning in the background and it tells you like, hey I'm downloading all of these filters so I can check for payments, you know give me a second and then I'll tell you if there's any new payments.
And this is very similar to like if you run a Bitcoin Core node on your laptop and you shut your laptop off for a couple days and you turn it back on, you open Bitcoin Core and it'll alert you.
Hey, the last synced block I have is this.
The current tip is this.
You know, give me five minutes while I sync the chain up to here.
So I imagine it'd be similar in the wallet.
Then the wallet does its work.
And then while it's doing that, then it's like, ah, hey, by the way, and that time that you were offline, you know, three people paid you and here's your new balance and it's current, you know, up to this block, I'll check again in five minutes or wait for you to tell me to check again.
And the reason I'm using this as an example, I think there's a nice improvement that we could do with silent payments where to minimize the bandwidth that the client needs to download.
When I come online and start scanning again, I don't really want all the blocks since I was last online.
I only want data for transactions that still have unspent outputs.
So if I check on January 1st and I scan and I get all this data, I've checked all these transactions for this block height, and then I go offline and then I come online February 1st again.
And I say, hey, I want to scan for more payments.
The server, whoever's sending me those payments, ideally should just send me information for UTXOs that were created since my last scan.
This is something we sometimes call cut through, transaction cut through.
I really don't need any data for an output that was maybe created on January 2nd and spent on January 10th.
Because clearly it wasn't for me.
If it was spent, it was not for me.
So this is something that I've been kind of playing around with where I don't even think the bandwidth concerns are going to be that bad for us on a payment user if we can come up with a way to implement a protocol like this.
Because now you're taking advantage of the fact that a lot of UTXOs are going to be created and spent before you decide to scan again.
Like if you scanned once a day, I think last time I looked at the numbers, it was like 50% or more of the UTXOs are created and spent in less than a day.
So if you're scanning for once of a day, you're already cutting down on 50% of the data that you need.
So I think we should be totally upfront about this and being like, hey, look, if we're going to build private mobile client experiences, it's going to be really difficult if we expect the exact same level of UX from a non-private mobile wallet.
And we shouldn't make that our goal, right?

We shouldn't be trying to provide a Venmo or Cash App-like experience on something that is fundamentally different in that it has privacy or reduced trust as the things that it values the most.
We need to highlight, "Here are the trade-offs you're making, here's what you're getting for it."
That makes it challenging.
But I'm hopeful that the more we push the boundary and research and prototype things, we may find that the user experience degradation is not as bad as we think it is.
It's always going to be the case that someone using a BIP 158 style backend for their wallet won't get notifications.
They'll have to spend more bandwidth.
But if we can quantify that and say, "Oh, it's 15, 20 MB more per month," to me that seems acceptable compared to, "Here's a wallet you can use non-privately and here's a wallet you can use privately but it's 20 GB per month."

Christoph Ono: 00:45:11

I think it's also important to think about, are you comparing to Venmo, Revolut, Apple-$2,000-iPhone-5G-experience, which is for a lot of people in the world, that's not the point for a lot of this Bitcoin stuff?
Or are you comparing to not even being able to make any payments at all, for which this is an insanely huge improvement or somewhere in between?

## Silent Payments and Backups

Christoph Ono: 00:45:36

I had another question around backups.
Let's say I'm in my wallet, I imported my seed and I click okay, generate one of these addresses for me.
The wallet should probably tell me that, "Cool, you might need more bandwidth now because of this scanning."
And, "Make sure to back this up."
Or, "If you use this wallet in another application, not all transfers might show up if it doesn't support this feature or something."
There's something that people might have to be aware of if they assume that they can put their seed in any place and everything will just be the same because it might just not be because of some choices they made, right?

Josibake: 00:46:22

This is another area where we wanted to be really careful when designing the protocol.
One of the reasons we decided to keep everything within the transaction.
There's no extra data, no `OP_RETURN`s, nothing outside of the transaction itself.
We didn't want the user to have to back up any additional information.
The recommendation in the BIP is we've proposed a new derivation path with the silent payments BIP number.
This is in the same style as BIP 43, BIP 44, and those that have followed.
They say, "If you're using a BIP 32 style seed, whether that be a BIP 39 seed phrase or BIP 32, this derivation path by the constant 352 is reserved for silent payments keys."
I start with my seed phrase, go to the 352 derivation path and generate two private keys, one for my scan key, one for my spend key.
So I don't have to back up anything except for the original seed phrase.
If I import that into another wallet, as long as that wallet supports silent payments, they'll know to check that 352 derivation path the same as how the rest of these derivation path standards work.

The user does need to be aware of, "You've imported this seed phrase that was used for silent payments.
You can scan the UTXO set.
The same as an `xpub`-style wallet.
You scan the UTXO set first and that tells you what your spendable balance is.
If you want your transaction history, the same as a regular old wallet using `xpub`s or something else, now you need to scan the full chain.
That will give you your full wallet history.
We're really trying to keep it as close to an experience as any other wallet is possible.
We don't want the user to have to go around backing up extra information.
One of the nice properties of silent payments is as long as you have access to the Bitcoin blockchain, or as long as you can get access to it, the full chain, you can always recover your full transaction history and your full wallet balance.

In a BIP 32 style world where we have the gap limit and look ahead, there is this complex management of scanning, checking these derivation paths, making sure you're looking far enough ahead with the gap limit to ensure you're recovering all of your money.
Whereas in silent payments, it's like, you look at a transaction, take the inputs of that transaction, do Diffie-Hellman with this private key.
If something doesn't show up in the outputs, it was not a payment to you.
If something shows up in the outputs, you get a match, it was a payment to you, and now you have all the data you need to spend.
It's a trade-off of, yeah, you need to get to the Bitcoin blockchain.
But if you can do that, you have peace of mind knowing that with just this backup from a seed phrase that allows you to generate the scan key, you should be able to find all of your money.

Christoph Ono: 00:49:31

That's great.
Go ahead, Yash.

Yashraj: 00:49:34

When I add a wallet into an application and it checks for addresses sequentially, it's often able to detect all the payments in a few seconds or a couple of minutes.
But if we have silent payment addresses, it would take longer because it has to do more computation, download more data and stuff.

Josibake: 00:50:05

Yeah.

Yashraj: 00:50:06

If I'm checking sequentially, it's really easy, right?
20 addresses, 100 addresses.
But if I'm doing silent payments, it's almost an unbounded number of addresses I have to check for.

Josibake: 00:50:18

When you're checking addresses sequentially, you are relying on that gap limit heuristic.
You're assuming you didn't use more than the look-ahead window.
You really should be checking the whole UTXO set to ensure you have a match.
So it is faster, but it's faster with less peace of mind.
To be doubly sure you're getting all the money from that BIP 32 chain, you should be brute-forcing way ahead on the gap limit, which takes longer.
The fact that it's quick is good.
If you're re-scanning a silent payment address, it is going to take longer because instead of pre-generating stuff and checking, you have to check every unspent Taproot output.
Any unspent Taproot output could be a silent payment to you.
You have to check all of those in one pass.
We haven't benchmarked this yet, but it's not crazy.
We're not talking about crazy orders of magnitude.
If you want wallet history, both wallets will have to scan the full chain.

Yashraj: 00:51:40

Even if it takes longer or needs more data, we could always convey that upfront so the user knows the trade-off and can make a decision based on that.

Josibake: 00:51:54

Yeah, absolutely.
It's always expectation setting.
Another thing worth mentioning with silent payments is there will be a slight increase in the work to do the scanning because this ECDH step is an elliptic curve multiplication, which is somewhat expensive for a wallet to do.
One of the things we're planning to benchmark on the Bitcoin Core one is if we do a wallet rescan.
If today, my descriptor wallet takes two hours to rescan the chain for wallet history, with silent payments, I would expect it to take maybe two hours and 15 minutes or two and a half hours.
It's not going to take much longer, but there is a little bit of extra work in there because of the ECDH step.

Yashraj: 00:52:42

Does that increase the work that wallet providers might have to do because we might have thousands of users using silent payment addresses in the future?
The wallet provider who runs the full node has to do all of this extra work.
Is that just a trade-off?

Josibake: 00:53:06

That's another one I'm interested in looking at.
We're always talking about the non-private scenario here, where the wallet provider is doing the scanning for the user.
We're strictly in non-private territory.
There's no way to do this privately.
Taking BIP 47 as an example, one of the implementations of BIP 47, if a user is not able to run their own node, they will have the wallet provider scan for them because the user will give them the `xpub`s to scan for.
The user loses their privacy to the server to do the scanning for them.
For BIP 47, you have an `xpub` per contact.
If I had opened a payment channel with Christoph, opened a payment channel with Michael, opened a payment channel with you, there are three `xpub`s that the server has to scan for on the server side.
It's the number of users times the number of connections those users have for that `xpub` style scanning.
It blows up pretty quickly, but it's not that bad because they can pre-generate what all of these addresses would be and put them in some sort of database.

On the silent payment side, let's say the server says, "I've got an index for silent payments. Just give me your scan key, I'll do the scanning for you."
Now I've got a million users.
That means the server would have to do a million ECDH steps, a million elliptic curve multiplications to check for all of their users, which is more work than the `xpub` lookup in a database style of doing things.
I think really, the way you push for payment adoption is by investing in these more private light client protocols.
What I was describing earlier with BIP 157 and 158 is nice because it's private, but it also scales better.
One single server computes these indexes and distributes them to clients.
The server does the computation of the index one time, and then gives it to whoever asks for it.
If the server does the work once, it gives it to many clients.
This is a good client-server model.
Then each individual client does a little bit of work relevant to themselves.
If I have a million silent payments users, and they're all using this more private protocol, they'll ask for the filter data from the node a million times.
The node computes it once, gives it to people a million times.
Then you have a million phones each doing their own ECDH calculations to check for payments, which distributes that calculation better, rather than having a single server just chewing through ECDH calculations to support N number of users.

## Current Status and Next Steps

Christoph Ono: 00:56:07

We're at the hour now.
We can still keep chatting if everyone wants to.
But I was wondering, what's the status right now?
What are the next steps?
What are the goals?
Is it to get implementations?
Is it to do more benchmarking, testing, consensus building?
Is this accepted as a solution by the ecosystem?
Or is it possible to tell even?

Josibake: 00:56:36

Great question.
The nice thing about silent payments is it does not require a soft fork.
We don't need anyone to agree or accept it.
It's a wallet protocol.
Anybody interested can feel free to reach out, get in contact, start implementing it.
In terms of status, Ruben Somsen and I are very happy with the state of the BIP.
At least in my head, I'm considering it finalized.
I don't expect any breaking changes to the protocol.
That being said, buyer beware.
This is a BIP that is brand new.
It hasn't been out for multiple years yet.
Six months ago, some people jumped in and were eager, but we had to make a change to a hashing step in the BIP.
Some people were frustrated.
So it is new, but for our purposes, we're saying the BIP is ready to go.
We've spent the last couple weeks adding more test cases to the BIP, so test vectors for wallets to implement.
Anybody is free to take a stab at it.
Start implementing it in your wallet.

I encourage people, if you're interested and want to play around with this, start implementing sending support.
Even better, let's make libraries for sending support that we can start giving to people.
Sending support should be very easy.
Relatively easy compared to the receiving side of it.
You don't need to change anything about your wallet backend for sending support.
If you're a wallet that uses the Electrum protocol, you can send to silent payment addresses.
No problem.
I expect that sending is something you can do without changing much.
If we get enough momentum on the sending side, then the receiving momentum will follow.
That's where we're at.
I'm actively looking for people who want to start implementing sending.
I'm happy to work with people on that.

In terms of the Bitcoin Core implementation, that's still a work in progress.
We need more reviewers in Bitcoin Core because it moves very slowly there.
We're making a big change to the wallet.
But that's where I'll keep putting a lot of my attention, continuing to work on that.
Nobody needs to wait for it to be on Bitcoin Core for people to start using this.
It's nice.
For light clients, we'll need something in Bitcoin Core, whether that be an index or some protocol for distributing the stuff.
We're in the phase now where we've spent a lot of time grinding on the protocol, working out the edge cases, making sure we're happy with it.
Now I'm fully in implementation mode for Bitcoin Core.
I'd be excited to see other people starting to run with it and implement it.
It's ready.

Christoph Ono: 00:59:52

Awesome.
Hey, Yash, sounds like something we could do a side project on the Bitcoin Core app for.

Josibake: 00:59:58

That'd be awesome.
There's a lot of fun design space around silent payments.
I have this dream in my head someday that we'll have like usernames for Bitcoin.
And it kind of feels like we could start thinking about like, what would the UX and design around a username be for something like a silent payment address.
Another thing that I'm really excited in starting to do is reach out to exchanges and talk to them about it, about how exchanges could start doing silent payment support.
Instead of sending to a static address to deposit your money to the exchange, you can now have a silent payment address that's unique to you.
The exchange could allow withdrawing to a silent payment address, which I know today a lot of exchanges, you have to like register a single address and you have to like approve it in your wallet and then you withdraw to that address multiple times.
Again, horrible for privacy.
And then if you wanna change it, you have to go through this like two factor authentication and everything to be like, oh yeah, this is a new address, I'm not a hacker.
Well, if we had sign of payment support, you go to the exchange one time, you register it, hey, this is my sign of payment address, you authorize it, go through all that safety to say, like, this is what I wanna withdraw to.
And now, for the rest of the duration of your account with that exchange, you can always withdraw to that same address and never have to go through this painful process of updating every time.
So there's a lot of things that are just like beyond strictly wallet and user experience that I'm kind of excited to start talking to people about and exploring the design space for.

Yashraj: 01:01:35

I'm super excited about this.
Not just in the Bitcoin Core app, but in the design guide.
If Josie is saying that people can run with it even now and in the Bitcoin Design Guide we have guidance around that, we might save people some effort on the design aspect.
I'm super excited for it.
I want to work on it.
I love this.

Josibake: 01:02:13

That would be awesome.
That's one thing I was hoping to come out of a call like this because it's a fundamentally different user experience.
We don't have this generate fresh address every time.
We have a static QR code, a static address that can be reused.
There's a lot of different ways of thinking that aren't prior art for design.
That'd be really cool to see some guidance for wallet developers.
So we have this clean uniform experience for people.

Christoph Ono: 01:02:50

Let's wrap it up here in a minute, but I just have one question because you mentioned it.
Actual usernames on Bitcoin.
I know that BIP 47 people, they have these Paynyms and it's basically a centralized server, which I don't think that's what we want to shoot for.
Do you think it's possible in any other way?

Josibake: 01:03:09

It's something I've kicked the tires on a little bit.
One idea is, let's say you did have a centralized server that was handing out silent payment addresses.
Let's say I own the domain Josie.com.
Under my well-known directory, I want to put my silent payment address.
You can just hit me at josie.com and your wallet will retrieve the silent payment address and parse it.
Something like that would be really cool.
There's some threat leveling of, "Oh, but someone could get in between and modify the address."
How could we combine something like the silent payment address with our domains, with some way of signing and authenticating that data?
I agree, there are less impressive ways to do it, which is just running a Paynym style thing where, yeah, a centralized server just maps the Paynym to the static code.
But we're leaking a lot of information and we really aren't authenticating any of the data.
In the centralized server handing out silent payment addresses, how do you know the server isn't just replacing every address with their own?

Christoph Ono: 01:04:34

Yeah.

Josibake: 01:04:34

Right?
So I've been thinking about stuff like that.
I don't have any groundbreaking, but it's another one of those areas where I feel like if we just keep kicking the tires on this, there's some interesting ideas.
Someone was like, "We could inscribe stuff."
And I was like, "I want usernames, I don't want them that bad. I don't really want to go that route."
But it's a fun idea that I want to keep playing with.

Christoph Ono: 01:05:02

Yeah, that sounds like what Lightning addresses and Nostr addresses, that type of format basically.
We have both of these that are testing out right now.