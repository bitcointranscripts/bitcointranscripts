---
title: "Silent Payments"
transcript_by: nymius via review.btctranscripts.com
media: https://www.youtube.com/watch?v=Cqmk2cZ2IjM
tags: ["silent-payments","privacy","privacy-enhancements","transaction-origin-privacy"]
speakers: ["Josibake"]
categories: ["club"]
date: 2024-02-06
---
Christoph Ono: 00:00:02

So welcome everyone.
Super excited to have this call here today.
And we are in Learning Bitcoin and Design call number 16.
Hilariously, we had number 17 this morning, because we move things around time wise.
But this is number 16 about silent payments.
And we have the super expert Josie here, who is willing to talk us through what silent payments are and how they work.
And so I'll just hand it over to Josie to kick us off and we can just organically, kind of feel out where we should take this conversation.
And so feel free to kick us off if you'd like to, you can just talk to us for 20 minutes, give an overview, or if you prefer a more conversational format that works as well.
And hopefully we have lots of time for everyone to ask questions and get those answered too.

Josie Baker: 00:01:01

Yeah, for me personally, first I'll preface, you guys got the bait and switch.
I'm not the super expert.
That's Ruben Somsen, who isn't here with us today.
Ruben Somsen was the original author of the silent payment scheme.
I am the super expert sidekick.
I am someone who got really excited about silent payments when I heard about it and then started helping Ruben out.
So how I've been helping is co-authoring the BIP with him.
So we've been working on that for a while now, just formalizing the spec, coming up with test vectors for wallet implementations.
And then I've also been working on a silent payments implementation for Bitcoin Core.
And then also just on the side as well, looking for other ways with different libraries to help out.
In terms of the format, I much prefer a conversational, more informal way of doing things.
So I'll launch into an overview, but I would encourage anybody who has questions, just feel free to jump in and ask questions.
If I say something that you don't understand, don't wait for later, just interrupt me, because then I feel like we're all using each other's time really efficiently, and make sure that we clear up any gray areas.
But I'll launch in with like a high-level overview, but like I said, raise your hand or stop me if something doesn't make sense.
But I guess to start, silent payments is kind of the nth iteration of a pretty old idea in Bitcoin, which is stealth addresses.
And then maybe something that you might have seen, you know, in other places you'll see people like in Ethereum for example they have a static address which is an account and you rather than go through this flow of always handing someone a fresh address, there's these concepts in other cryptocurrencies and other projects of this static payment identifier.
So the original idea I think goes way back to like 2012 or 2014, somewhere around that era, where people were talking about stealth addresses.
And the idea of a stealth address is you have a static code and people can send Bitcoin to you using that static code and they can use it over and over and over again.
So it becomes more like a routing number.
Like if you're a bank, you have a routing number.
Once I have your routing number, I can just send money to you whenever I want without interacting with you to get some code or confirmation.
The thing about stealth addresses is they do this in a way that preserves the user privacy.
Not just the user privacy, but the privacy of all the users of Bitcoin.
I'll talk about that maybe more a little bit later.
So today, if one of you guys wanted to send me Bitcoin, the only way to do it is you'd have to get in contact with me via messaging app or something, and you'd ask me for a fresh address.
And I would give you a fresh address and then you would use it.
And then if the next day you want to send me Bitcoin again, you'd have to get in contact with me again, ask for a fresh address and so on and so forth.
This is a cumbersome process that I think a lot of us are used to at this point.
But if you're coming from any other, you know, if you're not familiar with Bitcoin, you're used to more of like a Cash App or a Venmo or a PayPal-like experience, where you're like, hey, what's your tag or what's your email or what's your, you know, identifier?
What's your routing number?
And then once I have that number, I save you as a contact and I can just send stuff to you whenever I want.
That's the user experience that a lot of people are used to.
So it can be very jarring when they come to Bitcoin.
And it's like, oh, I have this interactive process where I have to ask for a fresh address.
And because of this friction, people often tend to do the bad thing of just reusing the same address.
So you'll see people will post a Bitcoin address in their Twitter profile or their GitHub, or they'll give you an address and then instead of reaching out to talk to them again, you might be tempted to just reuse the same address.
And there's nothing in Bitcoin that stops you from reusing the same address.
But the problem is that same address shows up on chain multiple times.
So now someone from the outside can say, ah, whoever owns this address has received X number of payments, holds this much.
They can see the transactions that paid them.
And you can now start to cluster a lot of activity.
And when enough people do this, when you can cluster things, so like exchanges are big offenders here we'll post static deposit addresses and then everybody knows that any transactions to that address are actually someone depositing to an exchange it limits the anonimity set of everybody else who's not doing that.
So it makes it easier to kind of hurt the privacy of everybody who's using Bitcoin when we have this widespread on-chain address reuse.
It also hurts your own privacy.
So if I post an address on my Twitter profile and say, look, hey, If you're happy with the work I'm doing on Bitcoin, send me some Bitcoin.
Anybody can come over to my Twitter profile, just look up that address in an address explorer and see how many times people have donated, what amounts.
If they're a chain analysis firm, they can start to look at those people who donated and start to look at their UTXOs that they spent, which maybe leads to uncovering someone's identity.
So, we've got all these problems, and yet this is what people are most inclined to do because it's not a really normal payment experience that we're used to of having to constantly interact with the person to get fresh payment information.
So that's kind of the idea that these stealth addresses are trying to solve or this, you know, these group of solutions and the idea is very very simple.
I'll just talk about silent payments right now and then maybe later we can talk about comparisons to other things that have tried to solve this problem.
But with silent payments, I will post this new address format called a silent payment address.
It'll start with `sp1q` instead of `bc1q`.
So it's clear that, okay, this is not like a regular Bitcoin address.
And then it's going to be a little bit longer than like a regular Bitcoin address.
Go ahead.
There's a hand up there from Yash.
Yeah.

Yash: 00:07:00

So why did we make this decision about making the silent payment address visually recognizable by a regular person?
Can't we simply delegate all of that to the wallet software or something?

Josie Baker: 00:07:17

Yeah, that's a great question.
So already, addresses are meant to kind of be this human readable component for Bitcoin, right?
Because if we think about what a Bitcoin address is, we've got the script pubkey, and the script pubkey is actually what goes into the blockchain, but that's cumbersome.
So we encode script pubkeys into addresses, and the addresses have this recognizable format to them.
So like, segwit addresses always start with the `bc1q` or `bc1p`, right?
So we have SegWit version 0 addresses, which is our `bc1q`, and then we have Taproot SegWit version 1, which is `bc1p`.
So just looking at the address as a human, you can be like, ah, that's a Taproot address, so that's a SegWit address.
They're also a little bit more compact than the full script pubkey.
The `bech32` and `bech32m` encodings are meant to remove ambiguous characters, so that a human can quickly look at an address and verify, okay, this looks correct.
Addresses are already kind of this convention of, these are meant for humans to be using.
And then the wallet software is what takes care of decoding the address into the appropriate script pubkeys that the wallet understands.
So with silent payments, we wanted to go the same direction and say we want something that you could show to a human being and they'd be like, oh, that's a silent payment address.
And it would be very clear that it's not a regular Bitcoin address because we didn't want any confusion of like, what's a Bitcoin address?
What's a silent payment address?
So to kind of go off that same design, the silent payment address is supposed to be something that people will recognize.
And then the wallet can parse that address and take care of actually doing the silent payments protocol.

Yash: 00:09:03

Yeah.
Another question on that one is like if the wallet that I use does not support silent payment addresses, can these addresses be used like a regular address?

Josie Baker: 00:09:19

Yeah, that's another good question.
This is something that we discussed early on.
There's a whole section on this in the BIP discussion, where we talk about, okay, what if we use something like BIP 21 to do silent payments?
Like rather than come up with a new address format, let's just use existing ones.
My argument against doing that is, I don't think, if a wallet doesn't understand silent payments and then it falls back to just using a static address, that could actually lead to more address reuse on chain than before.
Because currently someone posts just a taproot address and they're like, hey, you know, anytime you want to send me Bitcoin, use this address.
And this is horrible because of all the privacy concerns.
And then you have someone else who's like, I don't really like that.
I want to use silent payments.
And I wouldn't have posted just a static Bitcoin address anyways.
So now I'm going to post the silent payment address, so anyone who understands silent payments can send to me.
And anyone who doesn't will just fall back to using a static address, which then means we've added one more person who's using a static address.
So the whole idea of silent payments is we want to prevent any and all address reuse.
So it didn't really make sense to allow this fallback mechanism, which would allow you to do something which we're trying to avoid.
We kind of decided to tackle that problem a little bit differently, similar to how we did with Taproot, where obviously when you launch a new protocol or a new address format, there's going to be a lot of people that don't understand how to use it.
So we designed the silent payment protocol such that sending and receiving are separate.
So you can implement sending without receiving, you could implement receiving without sending, but that doesn't really make sense to me, or you can implement both.
And the barrier to implementing sending is meant to be as small as possible.
So rather how we'd approach it is, look, if someone wants to use silent payments, the most important thing is that there are a bunch of wallets out there that understand how to parse that address format and can send to that address.
If there's one person in the world who wants to use silent payments and nobody else cares, we still need a lot of people who can send to a silent payment address.
So we separated the protocol into send and receive, tried to make sending as simple as possible and as silent payments, like the first phase of, I guess, developer advocacy of reaching out to wallets and talking to them about this new protocol will be focused on, hey, even if you don't care about this, can you support sending to a silent payment address?
So that way, even if your users don't want to use silent payments or they don't care about it, at least when they see a silent payment address in the wild, which is someone who's saying, hey, I do care about receiving Bitcoin in a more private way with like better UX, then their wallet is able to send.
And then, you know, we can defer the much the more complicated problem of implementing receiving down the road.
So the hope is that by making it as easy as possible to implement sending support, there will be widespread adoption for wallets to send and then the few wallets or people who really care about the receiving part can go build and do those as well.
If we had done the other way where you kind of have to implement the full protocol, I think it's less likely that people would do it and it would slow down adoption a lot.
You'd have this bad experience of like you try to scan a silent payment address and it doesn't work.

Christoph Ono: 00:12:43

That's interesting.
The chicken and egg adoption type of problem seems like a common thing.
I also remember the same with multi-language recovery phrases, where the first step was just to be able to read them.
And then to have one aspect of it that's easier, that kind of gets things rolling, and then hopefully leads to a full adoption then later on.

Josie Baker: 00:13:07

It's particularly hard in an ecosystem like Bitcoin where you know you can't just go force people to do stuff you have to really meet them where they're at and and try to make things as easy for, I mean, a lot of wallets are run by volunteers or people who aren't getting paid, it's just passion projects.
So when you go and you're like, hey, I made this new protocol, I don't care about that protocol.
Like, you're asking people to do work to support it.
So that's one area where we did try to put a lot of thought into it and learn from history where we've seen that work well or slow things down.

Christoph Ono: 00:13:40

Do you feel like that was a problem with adoption of the previous attempts at this or do you think there were different reasons?

Josie Baker: 00:13:49

It's hard to say.
I mean, always when you look back at history, it's difficult to know what was going on at the time.
I think the previous attempts at kind of solving the address reuse problem, they don't seem to have gained a lot of traction.
But it's difficult to say, you know, why that might be.
You know, one thing is early on, I don't think people really cared that much about address reuse.
It's something that as we've, as we've seen more adoption, and people have cared more about Bitcoin, we've kind of started to realize, hey, this is actually really, really bad.
And it doesn't just hurt my privacy, it hurts everyone's privacy.
But in the early days when Bitcoin was just fun, I don't think anyone really cared about that.
They were just like, oh, yeah, just reuse the address.
I think Satoshi even had like an original pay to IP address in Bitcoin, which like if you're a privacy person, it's just like the worst possible thing you could do.
But it's, you know, pretty nice UX.
So I think in previous versions, BIP 47 is kind of the one that has the most traction, it's like a stealth address scheme.
I do wonder if having to implement the full send and receive for BIP 47 to work has limited their adoption.
I don't know if that's something they've experienced or not.
I know it's in requiring the full protocol like that, it is more work for wallet devs.
So maybe just to kind of wrap up, because we're starting to use BIP 47 and refer to other things and aware, maybe someone watching this hasn't quite got the punchline yet of like, what are we trying to do here?
So I throw my silent payment address up somewhere.
You see that code, your wallet parses that code without interacting with me, right?
You find this address anywhere.
You could find it printed on a billboard.
You could find it in my GitHub.
The point is it's interactionless.
You don't have to text me or know who I am.
You just be like, hey, I want to send some money to that address.
Your wallet then sends to that address.
And by following the silent payments protocol, it generates a guaranteed unique address that's never been used before, and that is only spendable by me.
And then you send money to that freshly generated address, and then the next time you want to send money to me again, the whole process repeats a freshly generated address.
Someone else can come along, use the same code and be guaranteed that they're not going to get an address that you might have previously used because they're also generating their own address fresh.
And the way that this works and the way it's somewhat distinct from previous versions of self-addresses and how people have tried to solve it, all of the information for generating that specific address is contained within the transaction itself.
So to be more specific, you use the private keys of the UTXOs that you want to spend, which are only spendable by you and nobody else, use those private keys in that transaction in combination with the public keys in my silent payment address to do something called elliptic curve Diffie-Hellman.
Elliptic curve Diffie-Hellman is where two parties can exchange secret information in public and arrive at the shared secret that only they know.
So you use your private keys in conjunction with my public key to create a Taproot output that has never been created before and can only be created using your inputs that you spend and my silent payment address and then I scan through the transactions and I see the public keys in your inputs just by looking at the blockchain and I use the private key corresponding to my silent payment address to do the reverse process to identify that this was a payment to me and also have all the data that I need to spend the output.
So this means that there's no state, no crossover.
It's not like an X pub where like if I put an X pub publicly and Christoph sends me some money to one and then somebody else like simultaneously asks for a fresh address from the X pub and it gives me the same one that it gave Christoph because it hasn't registered that Christoph used it yet, then you guys both might send to the same one.
There's no state management or anything like that.
And there's also nothing that links any of these multiple payments from you to my silent payment address.
So if you come to my silent payment address, let's say I'm the Signal Foundation, and I post a silent payment address that I want to receive monthly donations for people who want to support Signal, but I don't want to know who they are I don't even want to know if they're paying me every month so Christoph goes and he donates on the first of the month in January and then he goes and joins on the first of the month in February, there is no way from looking at those transactions that the Signal Foundation would be able to say, ah, these two payments on January and February came from the same person.
Each payment to a silent payment address is completely independent.
They're not groupable by sender in any way.
So I think this is like a really nice property for silent payments compared to something like BIP 47 where it's BIP 47 is more about establishing a payment channel.
So you you do this notification on-chain with an `OP_RETURN` or they have a few other mechanisms, but whatever the mechanism, you get this notification transaction out there and that notification transaction sets up a way for the counterparty to be able to derive fresh addresses when they want to send to you from this like `xpub` like thing.
It's basically an `xpub`.
They encode the information you need to do an `xpub` into an operator and you decode it.
The issue with this, when you go back to that like Signal Foundation example I just gave.
They might not know Christoph's identity, but they'll see a payment that came in on the 1st of January and a payment that came in on the 1st of February.
And from their wallet's perspective, their wallet can determine, ah, these two payments came from the same entity because they're both derived from the same notification that we use to establish this.
I think these are two distinct areas where silent payments adds some new and different properties that I don't think have been done yet with the stealth addresses.
This is one area where I think silent payments does really well in the privacy that all of these things have done, which is try to limit address reuse and then add some additional guarantees of there's better sender privacy than other protocols.
Another thing that I like about, an exciting thing to me about silent payments, is it's also a user experience improvement.
Privacy is usually more costly and more difficult.
Very rarely is it the easiest way to do something is also the most private way to do something.
That's a problem for users because some of us really care about privacy, others of us don't care about privacy and we care just more about having an easy experience as we use something, while also not understanding that the decisions we make today might hurt our privacy in the future or might hurt the privacy of other people who do care.
So like you may not care about address reuse, but your address reuse hurts my privacy because even if I'm not reusing addresses.
So one thing we really have to do for privacy stuff is we have to make it as easy or more easy than doing it the non-private way.
So with silent payments this is really nice because a silent payment transaction will not cost you anything more than a regular Bitcoin transaction.
You don't have to pay for this one-time notification.
You don't have to pay for any extra data in the transaction.
It's just a regular old Bitcoin transaction as if you had just been reusing the same address.
It also doesn't look any different than any other Bitcoin transaction, which is a nice property that, you know, someone from the outside can't tell that these things are silent payments.
But if you're a user who just does not care about privacy at all, and then someone tells you like, hey, here's this way to send and receive Bitcoin that's a little bit more like a username or a routing number, I think it kind of Trojan horses the privacy in for them were like oh, yeah this is like much easier than asking someone for a fresh address every time and it doesn't cost me anything more than what I would do to do a normal transaction user experience seems pretty much the same __"why wouldn't I use this?"__ and then we've got people using bitcoin more privately than they were before

Christoph Ono: 00:21:53

Come for the static ID stay for the privacy.

Josie Baker: 00:21:57

Yeah, right I mean, it sounds like.

Michael: 00:22:00

Hey, I'm Michael. By the way, nice to meet you.
So it sounds like it's similar in principle to BOLT 12 for Lightning, right?
So it's, I mean, it's the same kind of routing number or unique identifier that in the background then generates kind of all the magic happens in the background.
So that's really cool.

Josie Baker: 00:22:32

Yeah, BOLT 12 is another great example.
I think BOLT 12 is the analogy of this for Lightning, where in Lightning right now, Lightning is even more interactive than in Bitcoin, where, you know, if I give you a Bitcoin address, you can send money to it whenever you want.
If I give you a BOLT 11 Lightning invoice, you got to use it right before it expires, before I go offline, and so BOLT 12 is kind of handling that there.
So my dream would be, you know, in the next X years, soon, TM, you would have a BIP 21 style QR code that starts with a BOLT 12 lightning invoice and falls back to a silent payment address.
And from a user experience, you have this static QR code that you could post anywhere, never have to change it, and people who use it will be using Lightning and Bitcoin in a more private way that doesn't have address reuse or any of these, you know, kind of interactive go-betweens.
I think we need to see a lot more adoption before we get to something like that.
But like that's kind of the user experience that I'm envisioning, that I think we should be driving towards.
You know, you try to scan a QR code, it tries to do it first with BOLT 12.
If it can't do it with BOLT 12, it falls back to a silent payment address.

Christoph Ono: 00:23:49

Very cool, Very cool.
How's everyone doing here?
Everyone's very quiet.
If you have questions, you're welcome to put them in the chat, put them in the document here.
Trying to take some notes.
Feel free to ask anything.

Yash: 00:24:07

Yeah.
I think, Josie, that was a very good explanation.
And also you like really pointed out very well like what are the benefits of silent payments.
I love that.
Yeah, so I think people could just listen to the conversation and like get like a quick summary.
That's awesome.

Josie Baker: 00:24:26

Yeah, I guess, like you said, I think I've done a good job of mentioning the benefits of silent payments, maybe I should spend a second and talk about some of the trade-offs because there's no such thing as a free lunch.
Ruben and I have not stumbled upon some mystery of the universe that nobody else thought of.
So I think I'll cover the trade-offs really quickly because I think it is relevant.
So if you have something like an `xpub`, an `xpub`, BIP 32, Hierarchically Deterministic Wallet, it allows you to pre-generate private keys and public keys before they've been used.
And so you kind of know all possible addresses that you could hand out in the future at any given time.
And `xpub`s have been used as a way of mitigating address reuse in the past, but I think there are usability problems with that, that silent payments definitely improves on, one being like gap limit scanning.
You're never really sure with an `xpub`, and there's also a lot of state management to make sure that you're properly keeping track of which addresses you've used before so you don't accidentally hand them out again.
And you can really only use like an `xpub` per person.
I can't give the same `xpub` to Michael and Christoph because then they're both going to be choosing the next index to send to me and might step over each other and then we end up in a problem.
So that was the idea with `xpub`s and then BIP 47 kind of took this and said, well, let's make an `xpub` per contact.
So we don't have any of that problem and then they manage their state.
So that's one idea there.
But the benefit of the `xpub` approach is I can pre-compute these keys and then I can check for them to see if anybody has sent money to them.
And I can do that check just kind of using the UTXO set.
Like the UTXO set says, hey, these are the script pubkeys that are currently unspent.
And then you go to the UTXO set and you're like, oh, well, I have these keys, which could be turned into script pubkeys.
Let me see if any of those script pubkeys currently have any Bitcoin.
And that's kind of an easy way for you to scan.
And if you want your wallet history, you've got to fall back and scan the whole chain.
Right.
With silent payments, it's a little different in that you can't pre-generate anything because the sender is actually going to generate that address.
You have no knowledge of that address until the sender actually decides to send you money.
The sender generates the address and then uses it in a transaction.
So it kind of flips it.
The problem with that is to be aware of that, you need to scan the chain.
You need to be looking for transactions that have script pubkeys, that look like they might've been generated with your silent payment address.
So you can also scan the UTXO set, right?
Where the trade-off I would say between like an `xpub` style way of doing things or a BIP 32 where you pre-generate the addresses and the silent payment one, you have to scan the UTXO set for these outputs that are paying to you.
And in order to do that, you need access to the input data of the transaction that was to create that.
So it's you don't quite have to scan the whole chain but let's say for you know like a an `xpub` style way of doing things all you need is the `xpub` and the script pubkeys in the UTXO set.
For silent payments, you need the UTXO set and the inputs to the transaction that created that output in the UTXO set.
So for full nodes, this is very easy.
They already have full access to the blockchain, all of the transactions, So it's always available to them.
I would say that if you're already running a full node, there's not much extra overhead to run silent payments connected to that node.
For a light client, this is a little more tricky.
Now they need this input data, which without getting too deep into the weeds, that input data is really just one single pubkey, which represents the sum of the pubkeys used in that transaction.
So it's about 33 bytes of data per transaction.
So some light client that doesn't have access to the full chain now needs access to this 33 bytes per transaction to be able to check whether or not outputs in the UTXO set belong to them.
So there was a really good talk that Taj gave at Baltic Honeybadger where I think he said it better than I had been able to express is, in silent payments, we are making the process overall less interactive.
The sender and receiver do not need to interact in order to complete a payment.
And in order to facilitate that non-interaction, we're spending more in just raw compute.
We have to do more scanning on the node side to find that data and do that and use that data.
To me, I think this is a great trade-off because of the benefits we get.
But I think it's worth mentioning.

Yash: 00:29:00

Yeah, Quickly jumping in on that one.
Yeah, so I think that was a very good one that we have made this trade out wherein we are replacing interaction and some other things that we used to do with just computing a lot of stuff.
But my question leading into that is then not a lot of people run full nodes already and we have a lot of wallet users who are relying on their wallet provider running a full node somewhere else.
And so does this, so how does this make silent payments like harder to use if at all?
And the second question would be like, what is the privacy implication of that?
Because like right now, I might have a non-custodial wallet that I use who do not regularly have to track my transactions and all of that.
But now that I'm using silent payment addresses, my assumption, and I might be wrong, is that they would be the ones who would have to track the blockchain and my keys or something like that.
Is that true?
And if yes, what is the privacy implication of that?

Josie Baker: 00:30:18

So could you rephrase the first question again real quick?
And we'll start there, then maybe jump on to the second one.

Yash: 00:30:23

Yeah, yeah.
So I think my first question was regarding the fact that not a lot of people run full nodes already.
And so when they don't, there are some other trade-offs, like some other downsides.
So what would that be?
And then the second one was just focusing on the privacy aspect of that when it comes to the user and their wallet provider.

Josie Baker: 00:30:48

So I think, you know, this is kind of bigger than just the topic of silent payments.
And it's something that I care a lot about and have been doing a lot of thinking about is essentially, if you do not run your own full node today, there is no private wallet for you.
It just doesn't exist.
I think most of the wallets out there are using the Electrum X protocol, which there's Electrs, there's the original Python one and everything like that, which is where the wallet is actually talking to the wallet provider server, and the wallet is querying for specific addresses.
And saying, hey, can you tell me anything about this address?
There's just no way to do this privately.
It just doesn't exist.
And I think there's been some arguments about this in the past, where people have tried to claim that some of these things are private, but they're not.
The server could, now you can claim, okay, well, they're not doing it.
But if nothing prevents them from doing it, from a privacy threat modeling, you kind of have to assume they're doing it.
You can't just take someone's word like, oh, we're not collecting logs.
So any wallet that's using ElectrumX as a backend is just telling ElectrumX every single address that they're interested in.
Can you tell me anything about this address?
Can you tell me anything about this address?
And so that server could be logging all of that, keeping track of that information, and now you have very limited privacy.
I think really the only private light client wallet protocol that I'm aware of today is BIP 158, which was originally kind of conceived for these lightning nodes that wanted kind of a private way to ask for information about what's spent in a block.
And this you can actually use privacy with the tradeoff that it takes a little bit more bandwidth.
So in the BIP 158 world, full nodes kind of create this compact filter for the whole block and they say within this filter we encode every script pubkey that was spent or created and then the light clients ask for these filters and all that the node or the wallet provider learns at that point is okay a client was interested in this block, but they don't know anything about which addresses they were interested in or anything like that.
They just know they wanted a block.
The light client then gets that block and they have this way of testing for existence.
So if they have a script pubkey they want to check, they can test if it exists in that filter.
If it does exist in that filter, then they ask for the block, either from the same person or a different node to better preserve their privacy.
They download the full block and then they have all the information they need to process the transaction they care about.
And the nodes don't learn anything about the specific transaction.
So this to me is like, this is really the best that we have right now.
And it's not really widely used by wallets.
And I think a lot of people defer to using this Electrum style thing where you're just kind of telling the server, hey, this is exactly the transaction and the output that I'm listed in.
So TLDR, to kind of go back to the original, if you're not running your own node, you're just not running a private light client today for the majority of wallets.
How this kind of matters to silent payments is, as we started talking about silent payments and in how we wanted to support light clients, in theory, it would work totally fine for a silent payments user to just hand their scan key to somebody else.
You just be like, hey, so maybe it was worth mentioning.
In the silent payments protocol, the address is composed of two keys, a spend key and a scan key.
The scan key is used for finding the transactions.
The spend key is used for spending the transactions.
So your spend key can be in some super cold storage, never touches the internet, whatever, and your scan key can be hot online on a full node that either you own or somebody else owns and it's doing the scanning.
And if you lose your scan key and give it up to somebody, you lose your privacy.
They can see all the transactions that have been sent to your silent payment address, they cannot spend them.
So in theory, silent payments could also be used in a non-private way where someone just gives their scan key to somebody else who's running a full node, either a wallet provider or whatever, and that person does the scanning on behalf of them and then just tells them when they find a transaction.
This is very similar to how it works currently with Electrum.
For me, that's not super interesting.
I can't stop anybody from building that, but that's not interesting to me because the whole point of silent payments to me is like usability along with privacy.
So one of the things that I've been working on and researching is, how could we use something like BIP 157 and 158 for supporting silent payments light clients?
So I have some proof of concepts and some ideas there where what you would get from a full node is you would ask them, hey for a block give me all of the tweak data that I need which is going to be about 33 bytes per transaction that would be a silent payment transaction.
And also give me a BIP 158 filter for this block.
You're asking for two pieces of data.
You take that tweak data, you generate the silent payment outputs privately on your device that you're interested to check.
And then you check if they exist in the filter.
If they exist in the filter, you ask another node or the same node for the full block, you download the block, you process the transaction.
And so this way you could have a light client that is operating completely privately without needing, well not completely, more privately, right?
There's still privacy implications with BIP 158, but about as private as you can get today.
You're scanning for transactions in a light client.
You don't need the full blockchain.
The tradeoff you're making here is you do need more bandwidth.
Right.
So instead of Electrum uses the least bandwidth, I think.
BIP 158 uses a little bit more for the filters, and then silent payments would use more than that.
So it's kind of like, at least now, I think we're giving users the option of, like, hey, if you want to run a light client, you don't want to run a full node, here's an option for you to use a light client privately with more bandwidth than it would cost you to do it non-privately but less bandwidth than it would cost you to run a full node.

Yash: 00:36:42

Yeah quickly I'm jumping on that. So, what you just described like this can keep providing that all of that stuff so the user does not explicitly need to do any of this themselves right the wallet software can do this in the background.

Josie Baker: 00:37:01

Exactly yeah you know from a user experience standpoint you know I'll take BDK as an example.
In BDK, they have this work where they have like composable backends where, you know, you want to set up a wallet, you're building with BDK, and then you pick a backend.
And I think they're working on compact block filters, BIP 158 as a backend, though it's not ready yet.
But you could say like, hey, I want an Electrum backend.
I want an RPC backend.
Like I want it to connect to only my node or a node that I trust, or use one of BIP 158.
From the user's perspective, they don't care or know.
I mean, they should, right?
There's privacy implications for the backend.
But from the user perspective, they don't really know.
If the wallet's really well designed from a user experience, they're clueless.
They just open up their wallet and they see that their wallet is doing stuff, but they don't really know how it's getting that information.
And it would be the same here, except that we would expect, like, if you have an Electrum style wallet versus a BIP 158 style wallet, the user would see more bandwidth consumption.
Maybe the wallet, like the loading screen takes longer, there's more bandwidth.
And so I think part of the UX challenge of silent payments would be explaining that trade off to the user.
Right.
Like why?
Why is my phone, why is my mobile phone, you know, Bitcoin wallet operating slower than, you know, like this other wallet or, you know, why is this app using more data?
And I think there's kind of a UX challenge there of explaining to the user, well, yeah, like you're using more data because you're not giving up your privacy to another node.
You could use less data but then you're just giving up all of your privacy and I think people do care about that and even if they don't then we're allowing them to kind of make that educated trade-off for themselves.

Michael: 00:38:45

So but would they even notice?
I mean, one of the points is that you can send asynchronously, right?
So you're not even in contact.
So that wallet could kind of in regular intervals scan for incoming transactions and it would alert you only when you you know when it found something so then then it would all already be kind of I don't know how realistic that is or or whether that's feasible but the implications might not even be that bad because you're probably a lot of the time you're not even expecting it, except if you really synchronously interact with the person paying you.

Josie Baker: 00:39:32

Yeah, I agree.
I mean, I think there's a lot of usage patterns where it wouldn't generally matter.
I would say though, like having mobile apps do things in the background is very difficult.
I think this is something that people struggle with.
The other thing is a lot of times people talk about push notifications, right?
Like their wallet alerting them of something.
And I just, I don't think push notifications can happen in a private and kind of like, where the user is kind of in control of the thing, right?
Because if you imagine how most push notifications work, you have your client which is connected to some server and that server is doing a bunch of work and things for you and when that server finds something out, it proactively sends you information as the client.
But by the nature of you outsourcing that work to the server, it usually means that the server is learning a lot about you.
So this kind of comes up sometimes with BIP 158 style wallets.
If you have ElectrumX, you know, an Electrs personal server running as your wallet backend, when it finds a transaction, it can proactively send you that notification.
The only way that that server knows to send you the notification is because it knows the transaction, which means you've lost all your privacy to the thing that is sending you the notification.
So I think this is another way where we kind of have to educate people of like, you're going to use stuff more privately, you're not going to have the same user experience as maybe non-private alternatives.
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
We shouldn't be trying to provide a Venmo or Cash App like experience on something that is just fundamentally different in that it has privacy or reduced trust as kind of the things that it values the most.
So we need to kind of highlight like, hey, here are the trade-offs you're making, here's what you're getting for it.
And so that makes it challenging.
But I'm also hopeful that like the more we push the boundary and research these and kind of like actual prototype things, we may find that the user experience degradation is really not as bad as we think it is.
I think it's always going to be the case that someone who's using a BIP 158 style back-end for their wallet, they're not going to get notifications.
They are going to have to spend more bandwidth.
But if we can quantify that and be like, oh, yeah, it's 15, 20 Mb more per month.
To me, that seems like a very acceptable thing versus like, hey, here's a wallet that you can use non-privately and here's a wallet that you can use privately but it's like 20 Gb per month.

Christoph Ono: 00:45:11

Yeah, I think it's also important to think about that.
Are you comparing to, you know, Venmo, Revolut, Apple-$2,000-iPhone-5G-experience, which is for a lot of people in the world, that's not the point for a lot of this Bitcoin stuff?
Or are you comparing to not even be able to make any payments at all, for which this is an insanely huge improvement or somewhere in between.
I had another question around backups.
So let's say I'm in my wallet, I imported my seed and I click okay, generate one of these addresses for me.
The wallet should probably tell me that, cool, you might need more bandwidth now because of this scanning, maybe.
And make sure to back this up, or if you use this wallet in another application that not all transfers might show up if it doesn't support this feature or something.
There's something that people might have to be aware of if they assume that they can put their seed in any place and everything will just be the same because it might just not be because of some choices they made, right?

Josie Baker: 00:46:22

Yeah, this is another area where we wanted to be really careful when designing the protocol.
So, one of the reasons we decided to keep everything within the transaction.
There's no extra data.
There's no `OP_RETURNS`.
There's no anything outside of the transaction itself as we didn't want the user to have to back up any additional information.
So what the recommendation currently is on the BIP is we've proposed a new derivation path with the silent payments BIP number.
So this is very in the same style as BIP 43, BIP 44, and like those that have followed, where they say, hey, look, if you're using a BIP 32 style seed, whether that be a BIP 39 seed phrase or BIP 32, this derivation path by the constant 352, this is reserved for silent payments keys.
So I start with my seed phrase, I go to the 352 derivation path and I generate two private keys, one for my scan key, one for my spend key.
So I don't have to back up anything except for the original seed phrase.
And if I import that into another wallet, so long as that wallet supports sign of payments, they'll know to check that 352 derivation path the same as how the rest of these derivation path standards work.
Now, what the user does need to be aware of is, hey, so you've imported this seed phrase that was used for silent payments.
You can scan the UTXO set.
Again, same as an `xpub`-style wallet.
You scan the UTXO set first and that tells you what your spendable balance is.
And then if you want your transaction history again, same as like a regular old wallet that's using `xpub`s or something else.
Now you need to scan the full chain and that will give you your full wallet history.
So I think we're really trying to keep it as close to an experience as any other wallet is possible.
And we don't want the user to have to go around backing up extra information.
I think one of the nice properties of silent payments is as long as you have access to the Bitcoin blockchain, or as long as you can get access to it, the full chain, you can always recover your full transaction history and your full wallet balance.
Where I'm not trying to FUD BIP 32 or anything like that, but when you go into a BIP 32 style world where we have like the gap limit and look ahead, there is kind of this complex management of, you know, you're scanning, **but you're scanning**.
You need to check these derivation paths, you need to make sure you're looking far enough ahead with the gap limit to make sure that you're actually recovering all of your money.
Whereas in silent payments, it's like, hey, you look at a transaction, you take the inputs of that transaction, you do Diffie-Hellman with this private key.
If something doesn't show up in the outputs, this was not a payment to you.
If something does show up in the outputs, you get a match, then this was a payment to you, and now you have all the data you need to spend.
So it's kind of like, again, that trade-off of, yeah, you need to be able to get to the Bitcoin blockchain.
But if you can do that, then you kind of have this peace of mind knowing that with just this backup from a seed phrase that allows you to generate the scan key, you should be able to find all of your money.

Christoph Ono: 00:49:31

That's great.
Go ahead, Yash.

Yash: 00:49:34

Sorry, so I on this one, like so when I'm when I just add a wallet into an application and it checks for addresses sequentially, it is like often able to detect all the payments in a few seconds or a couple of minutes.
But if we have silent payment addresses, it would take longer because it has to do a lot more computation, a lot more downloading data and stuff.

Josie Baker: 00:50:05

Yeah.

Yash: 00:50:06

So if I'm checking sequentially, it's like really easy, right?
20 addresses, 100 addresses.
But if I'm doing silent payments, it's like almost an unbounded number of addresses that I have to check for?

Josie Baker: 00:50:18

I think when you're checking addresses sequentially, you are relying on that gap limit heuristic, right?
You're kind of like assuming you didn't use more than the look ahead window and everything like that.
And so I think what you really should be doing is kind of checking the whole UTXO set to see if you have a match.
So like I think it is faster, But for me, it's faster with less peace of mind, because really what I should do to be doubly sure that I'm getting all of the money from that BIP 32 chain is I should be brute forcing way ahead on the gap limit, which is going to take a lot longer.
So the fact that it's quick is good.
And if you're scanning, if you're re-scanning, let's say you import a silent payment address and you're scanning the UTXO set, you are, it is going to take longer because now instead of pre-generating stuff and checking, you're going to check every unspent taproot output, right?
Because any unspent taproot output could be a silent payment to you.
So you're gonna have to check all of those in one pass.
We haven't benchmarked this yet, but it's not crazy, right?
We're not talking about crazy orders of magnitude.
If you want wallet history, then both wallets.
There is no fast way for an `xpub` wallet to recover a wallet history or a sound payment wallet.
You are going to have to scan the full chain.

Yash: 00:51:40

Yeah, and I think even if it takes longer or needs more data, we could always convey that up front so the user can know that this is the trade-off and they can make the decision based on that, I guess.

Josie Baker: 00:51:54

Yeah, absolutely.
I think it's always expectation setting.
Another thing worth mentioning with silent payments, there is going to be a slight increase in the work to do the scanning because this ECDH step is an elliptic curve multiplication, which can be a somewhat expensive step for a wallet to do.
So I think that's one of the things that we're planning to benchmark on the Bitcoin Core one is if we do a wallet rescan.
Let's say today I have like my descriptor wallet set up and I decide to rescan the chain to look for wallet history that might take two hours.
With silent in payments, I would expect it's probably going to take maybe like 2 hours and 15 minutes or 2 hours and a half.
I don't think it's going to take much longer, but there is a little bit of extra work in there because of the ECDH step.

Yash: 00:52:42

Yeah, does that increase the work that the wallet providers might have to do because like now we we might have in the future it might have thousands of users using silent payment addresses and now for each of those users the wallet provider who does the full node has to do all of this extra work.
And so that is just like a trade-off.

Josie Baker: 00:53:06

Yeah, that's another one that I'm interested to look at.
So again, we're always talking about the non-private scenario here, right?
Like if the wallet provider is doing the scanning for the user, we're strictly in non-private territory.
There's no way to do this privately.
So taking BIP 47 as an example, one of the implementations of BIP 47, if a user is not able to run their own node, then they will have the wallet provider scan for them because the user will give them the `xpub`s to scan for.
So the user is now losing their privacy to the server to do the scanning for them.
And for BIP 47, you have like a, I think an `xpub` per contact.
So if I had opened a payment channel with Christoph, opened a payment channel with Michael, opened a payment channel with you, now there's three `xpub`s that that server is gonna have to scan for on the server side.
So I think of it as the number of users times the number of connections those users have for that `xpub` style scanning as a wallet provider, which blows up pretty quickly.
But I think it's still not that bad because they can pre-generate what all of these addresses would be and put them in some sort of database.
On the silent payment side, and again, this is something where I'm like, I wouldn't recommend that people build it this way, but let's just say the server said, hey look, I've got an index for silent payments, just give me your scan key, I'll do the scanning for you, and now I've got a million users.
That does mean that that server would have to do a million ECDH steps, so a million elliptic curve multiplications to check for all of their users, which is going to be more work than the `xpub` lookup in a database style of doing things.
I think really, the way you push for payment adoption is I think we keep investing in these more private light client protocols because you know what I was describing earlier with BIP 157 and 158 it's another one of these nice ones that I think it's private, but it also scales better right because one single server computes these indexes and distributes them to clients.
The server does the computation of the index one time, and then they give it to whoever asked for it.
If the server does the work once, it gives it to many clients.
So this is like a good client-server model.
Then each individual client does a little bit of work relevant to themselves.
So, if I have a million silent payments users, and they're all using this more private protocol, they'll ask for the filter data from the node a million times.
So the node would compute it once, give it to people a million times, and then you have a million phones each doing their own ECDH calculations to check for payments, which distributes that calculation a lot better, rather than having a single server just chewing through ECDH calculations to support N number of users.

Christoph Ono: 00:56:07

We're at the hour now.
We can still keep chatting if everyone wants to.
But I was also wondering then, what's the status right now?
What are the next steps?
What are the goals?
Is it to get implementations?
Is it to do more of this benchmarking, testing, consensus building?
Is this accepted as a solution by the ecosystem?
Or is it possible to tell even?

Josie Baker: 00:56:36

Great, great question.
The nice thing about silent payments is it does not require a soft fork.
So we don't really need anyone to like agree or accept it, right?
It's a wallet protocol.
So I would say you know anybody who's interested feel free to reach out get in contact if you want to implement it.
I would say in terms of status Ruben Somsen and I are very happy with the state of the BIP.
I think the BIP, at least in my head, I'm considering it finalized.
I don't expect that we're going to make any breaking changes to the protocol.
Now, that being said, buyer beware.
This is a BIP that is brand new.
It hasn't been out for multiple years yet.
I know six months ago, some people jumped in and were really eager, and then we had to make a change to a hashing step in the BIP.
Some people were a little frustrated so it is you know it is new but I think you know for our purposes we're kind of saying like look the BIP is ready to go we've been spending the last couple weeks myself and another contributor we've been working on adding more test cases to the bit, so test vectors for wallets to implement.
At that point, anybody is free to take a stab at it.
Start implementing it in your wallet.
I would really encourage people, if you're interested and want to play around with this, start implementing sending support.
Even better, let's make libraries for sending support that we can start giving to people.
Sending support should be very easy, right?
I mean, relatively.
It should be relatively easy compared to the receiving side of it.
And you're not really, like to do sending support, you don't need to change anything about your wallet back end whatsoever.
If you're a wallet that uses the Electrum protocol, you can send to silent payment addresses.
No problem.
You know, there's I expect that sending is that thing that you can do without really changing much.
If we get enough momentum on the sending side, then I think the receiving momentum will follow.
So that's kind of where we're at.
I'm actively looking for people who want to start implementing sending, I'm happy to work with people on that.
In terms of the Bitcoin Core implementation, that's still a work in progress.
You know, we need more reviewers in Bitcoin Core because it moves very slowly there and we're kind of making a pretty big change to the wallet.
But that's where I'll keep putting a lot of my attention, just continuing to work and get that.
But I don't think, you know, nobody needs to wait for it to be on Bitcoin Core for people to start using this.
You know, obviously it's nice.
And I think for light clients, we're going to have to have something in Bitcoin Core, whether that be an index or some protocol for distributing the stuff.
But yeah, I think we're in the phase now where we've spent a lot of time grinding on the protocol, working out the edge cases, making sure that we're happy with it.
Now I'm fully in implementation mode for Bitcoin Core and I'd be excited to see other people starting to run with it and implement it.
I guess it's ready.

Christoph Ono: 00:59:52

It's awesome.
Hey, Yash, sounds like something we could do a side project on the Bitcoin Core app for.

Josie Baker: 00:59:58

Yeah, I think that'd be awesome.
Yeah, and I think there's a lot of fun, you know, to me, there's a lot of fun design space around silent payments, right?
It's not just, you know, I have this dream in my head someday that we'll have like usernames for Bitcoin.
And it kind of feels like, yeah, we could start thinking about like, what would the UX and design around a username be for something like a silent payment address.
Another thing that I'm really excited in starting to do is reach out to exchanges and talk to them about it, about how exchanges could start doing silent payment support.
Instead of sending to a static address to deposit your money to the exchange, you can now have a silent payment address that's unique to you.
The exchange could allow withdrawing to a silent payment address, which I know today a lot of exchanges, you have to like register a single address and you have to like approve it in your wallet and then you withdraw to that address multiple times.
Again, horrible for privacy.
And then if you wanna change it, you have to go through this like two factor authentication and everything to be like, oh yeah, this is a new address, I'm not a hacker.
Well, if we had sign of payment support, you go to the exchange one time, you register it, hey, this is my sign of payment address, you authorize it, go through all that safety to say, like, this is what I wanna withdraw to.
And now, for the rest of the duration of your account with that exchange, you can always withdraw to that same address and never have to go through this painful process of updating every time.
So there's a lot of things that are just like beyond strictly wallet and user experience that I'm kind of excited to start talking to people about and exploring the design space for.

Yash: 01:01:35

Yeah, I'm super excited about this.
And I'm Christoph like not just in the Bitcoin Core app, but in the design guide that we have, I think if like Josie saying that people can can run with it even right now and if in the Bitcoin Design Guide we have some sort of guidance around that and we might say people who want to implement this, we could save people some effort on the design aspect of it.
Yeah, so I'm super excited for it.
Want to work on it.
Yeah.
I love this.

Josie Baker: 01:02:13

That would be awesome.
Like that was one thing I was really hoping to come out of a call like this because it's a fundamentally different user experience, right?
You don't have this like generate fresh address every time you have a static QR code, a static address that can be reused for the duration of the wallet.
So there's a lot of like different ways of thinking that I think maybe aren't, you know, there isn't prior art on for design.
So that I mean, that'd be really cool to see some guidance come out for wallet developers.
So we have this kind of like clean uniform experience for people.

Christoph Ono: 01:02:50

Let's wrap it up here in a minute, but I just have one question because you mentioned it.
Actual usernames on Bitcoin.
I know that BIP 47 people, they have these Paynyms and it's basically a centralized server, which I don't think that's what we want to shoot for.
Do you think it's possible in any other way?
I mean,

Josie Baker: 01:03:09

it's yeah, it's something I've kicked the tires on a little bit.
You know, one idea is, let's say you did have a centralized server that was handing out silent payment addresses.
So like I say, I want some username at domain.com and then the domain just returns.
Like let's say I own the domain Josie, josie.com.
Under my well-known directory, I want to put my silent payment address.
Now you can just hit me at josie.com and your wallet will retrieve the sign of payment address and parse it.
Something like that would be really cool.
There's obviously some threat leveling of like, oh, but someone could get in between and modify the address or whatever.
So I've been thinking a little bit about this of like, how could we combine something like the silent payment address with our domains, with some way of signing and authenticating that data?
I do agree, there's some less impressive ways to do it, which is just running a Paynym style thing where like, yeah, centralized server just maps the Paynym to the static code, but we're leaking a lot of information and we really aren't authenticating any of the data.
Like in the centralized server handing out silent payment addresses, how do you know the server isn't just replacing every address with their own?

Christoph Ono: 01:04:34

Yeah.

Josie Baker: 01:04:34

Right?
So I've been thinking about stuff like that.
I don't have any groundbreaking, but it's another one of those areas where I'm like, I feel like if we just keep kicking the tires on this, there's some interesting ideas.
Someone was like, yo, we could like inscribe stuff, you know, we could have like, and I was like, you know, like, I want usernames, I don't want them that bad.
Like, I don't really want to go that route.
But it's a fun idea that I want to keep playing with.
Yeah.

Christoph Ono: 01:05:02

Yeah, that sounds like what Lightning addresses and Nostr addresses, that type of format basically.
Which, I guess we have to, we have both of these that are testing out right now.