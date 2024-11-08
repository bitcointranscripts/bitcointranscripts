---
title: Payment Points
transcript_by: tvpeter via review.btctranscripts.com
media: https://www.youtube.com/watch?v=Y2mTjCldRAU
speakers:
  - Nadav Kohen
tags:
  - ptlc
date: 2020-03-30
episode: 7
aliases:
  - /chaincode-labs/chaincode-podcast/payment-points/
---
Nadav Kohen: 00:00:00

Right now in the Lightning Network, if I were to make a payment every single hop along that route, they would know that they're on the same route, because every single HTLC uses the same hash. It's a bad privacy leak. It's actually a much worse privacy leak now that we have multi-path payments, because every single path along your multi-path payment uses the same hash as well.

## Intro

Caralie Chrisco: 00:00:37

Hi everyone, welcome to the Chaincode Podcast. I'm Caralie and I am sitting here with John. Hi John.

John Newbery: 00:00:43

Hi Caralie, how are you?

Caralie Chrisco: 00:00:44

I am okay. I'm sad that Jonas is not joining us, but it is due to the current circumstances in the world.

John Newbery: 00:00:51

Yeah, Jonas is sheltering at home just like all of us.

Caralie Chrisco: 00:00:54

But we still wanted to go ahead and introduce this episode where you guys chat with Nadav Cohen.

John Newbery: 00:00:58

That's right, we talked to Nadav, who works at ShortBits with Chris Stewart. And ShortBits is a really interesting company. They are using the Lightning Network to monetize APIs and data streams. And Nadav writes a really, really interesting blog at shortbits.com/blog, where he writes about the technology behind the Lightning Network, discrete log contracts, payment points. And so we wanted to talk to Nadav about payment points specifically, which is a potential upgrade to the Lightning Network, which we could get after Schnorr signatures are activated. So we talked to Nadav about that technology, about the advantages that it has over HTLCs, and about some of the really interesting use cases.

John Newbery:

Hey Nadav.

Nadav Kohen:

Hey

John Newbery:

Welcome

Nadav Kohen:

Thanks for having me.

Adam Jonas: 00:01:48

So today we're going to talk about payment points. And we're really excited about this. Can you maybe start off by explaining a little bit about an HTLC and how Lightning uses HTLC and then we'll take it from there.

## HTLCs

Nadav Kohen: 00:02:03

Totally. So HTLC stands for Hash Time Lock Contract, and it refers to the Bitcoin contract in which it has kind of two spending cases. One of them is a hash lock, and the other one is a time lock. So if I set up an HTLC pointed at you or spent to you, that means that if you reveal the preimage to the hash that is in that HTLC, then you can claim those funds. But if after a timeout you don't do that, I can kind of claw those funds back. So it has a hash lock on one side kind of to you and a time lock on the other side to me. And whoever claims those funds gets them. So how they're used in Lightning is if I want to pay Carol through Bob, then I would set up an HTLC to Bob that says if he reveals the preimage to a hash that Carol knows, then he can claim my funds, and then I tell him where Carol is, and he goes and sets up the same HTLC to Carol. And then Carol, who gave me the invoice for this payment, generated this hash, knows the preimage, she can claim her funds, and now that she's claimed her funds, she must have revealed the preimage to that hash to Bob, and so Bob now knows the preimage and he can claim his funds. And so, HTLCs are what the Lightning Network uses to make routing atomic between payment hops.

John Newbery:

So what do you mean by atomic?

Nadav Kohen:

By atomic I mean that no node on the network along a route is at risk of losing funds without being paid. Meaning if their funds get claimed, they must learn the hash preimage, which must mean that they have the ability to claim the funds pointed at them. So it's what makes everything risk-free in the sense that either the entire payment route will happen or it won't, which is kind of what makes it one thing or atomic.

John Newbery:

Right, it can't be cut up.

Nadav Kohen:

Unlike real atoms.

## Timelocks

John Newbery: 00:04:15

That's right. And what about the time lock component of that? So as you go along the path, something happen with the times.

Nadav Kohen: 00:04:20

So if, for example, your counterparty, or the counterparty of any routing node along the route disappears or is just not responding, then you have all of these payments kind of set up, and on Lightning you always have to be ready for the case where your commitment transaction ends up on chain. So essentially, in order for things to be safe and secure and not trusting, you have to make sure that everything is working as if it's on the blockchain. And so if we're on the blockchain, and I have this HTLC set up, and the hash lock is never going to be claimed, meaning the the payment has essentially failed, but I'm on chain, then you want to be able to get your funds back, seeing as things are atomic, every single HTLC along this route will have failed. And so if you're not on chain, you can just get rid of that HTLC without using any kind of timeout, assuming that the parties are cooperating. But if you're on chain or if the parties aren't cooperating, meaning you have to go on-chain, then you can just wait out that time lock and then claim your funds back.

## HTLC drawbacks

Adam Jonas: 00:05:39

So HTLCs have some drawbacks. Can you tell us about that?

Nadav Kohen: 00:05:42

Yeah. So right now on the Lightning Network, if I were to make a payment that was routed, every single hop along that route would know that, if they talked to each other, they would know that they're on the same route because every single HTLC uses the same hash. And so you're essentially putting a rubber stamp on inside each layer of the onion that kind of correlates that payment along that route. So it's a bad privacy leak. It's actually a much worse privacy leak now that we have multi-path payments, because every single path along your multi-path payment uses the same hash as well. And so people can try and find out where you are based on intersections between paths and things like this.

## Wormhole attack presented in *Anonymous Multi-Hop Locks for Blockchain Scalability and Interoperability

Nadav Kohen: 00:06:34

And then it also has the drawback that if you have two nodes, which could be the same person running those two nodes, or it could be two different people who are just cooperating, and they realize that they're on the same path, they can perform something called a wormhole attack, where rather than revealing the preimage, or so let's, I'll give some names so that I'm not being too hand wavy, say that Mark and Mallory, both malicious, are on two nodes along a route, not neighbors, but just two nodes along a route where Alice is paying Bob someone external to them. And they see that they're on the same route because they've set up HTLCs with the same hash. And now Mark is going, is further along the route and he's going to learn the preimage. And now rather than claiming the funds pointing at him using that preimage, he directly tells Mallory, not on the Lightning Network, just however they're communicating, what the preimage is. And she claims her funds using that preimage, and you kind of have just skipped over all of the intermediate notes between Mark and Mallory. And presumably, I mean, if they're the same person behind them, they don't care that Mark didn't get paid. They still ended up getting the money that they were owed. And if they're different people, maybe they have some backdoor deal where they pay each other. But essentially what's happened here is that they've stolen the fees of all of the nodes in between them, because the difference between what Mark would have made and what Mallory did make is those fees. Not only have they been able to steal all those fees, which are kind of the payment for the use of the liquidity of the nodes in between, but also if Mark wants to, he cannot fail the payment. He can just like hold on to it, and all of the nodes in between them will have in-flight HTLCs indefinitely until, well not indefinitely, until the time lock occurs, and that's when the payment actually will fail. So you can kind of hold their funds hostage to the worst case scenario. And it's completely undetectable because to them it just looks like the payment never happened and that the payment failed. And so there's not really any mitigation against this. And also you're economically like incentivized to perform these attacks because you get paid to do so.

John Newbery:

But Alice and Bob don't care about this, right?

Nadav Kohen:

Alice and Bob don't care about this, this is correct. This is something that only affects routing nodes.

Adam Jonas:

And it sort of seems like it's a more efficient route. I mean, at the end.

Nadav Kohen:

It is a more efficient route. Yeah, but I would say the main problem is definitely the privacy leakage that happens with HTLCs, but then also it can be problematic that people are incentivized to kind of steal fees from people in between and hold their funds hostage. Although they're not incentivized to do that, it doesn't matter to them.

Adam Jonas: 00:09:45

Are there other solutions that could improve this?

## Point time lock contracts (PTLCs)

Nadav Kohen: 00:09:49

Yeah, so there are these things called PTLCs, which are point time lock contracts. These are essentially the same as HTLCs, except for instead of the hash lock we have a point lock so instead of saying reveal the preimage to this hash we say reveal the scalar to this point which is analogous to you know saying reveal the private key to this public key. Except for I try to say scalar and point, because private and public, normally you shouldn't be giving people your private keys. But it's OK to give people scalars to points that aren't being used as keys most of the time. Yeah, but so essentially, in Bitcoin script, there isn't actually a way to compute the point to a number. But there is some math magic you can do with adapter signatures. On Schnorr, it's very easy to do adapter signatures. On ECDSA, it's quite a bit harder. But using adapter signatures, you can essentially enforce point locks in kind of like not a strictly on-chain sense. And yeah, you can create PTLCs and then you do everything else on Lightning exactly the same. But rather than having the contracts be set up in a way where you're revealing preimages to hashes, you reveal scalars to points. And the reason that this helps us is because with hashes, you're destroying a lot of useful, non-sensitive information about your preimage. So you can't do anything with a hash of something. Whereas when you have a point of a scalar, certainly you get no useful information about the scalar, or at least no sensitive information about the scalar. Because if that were the case, public-heap cryptography would be kind of screwed. But you still get some nice properties, specifically an additive property, where if I have two scalars and I add them together and then find out what the point is, that gives me the same result as if I took the two points corresponding to those scalars and added those two points together. And so what we do on the Lightning Network with PTLCs is we add a random nonce to every single hop. And that completely decorrelates them because every single kind of PTLC uses a random point. Well, yeah, just a random looking point, I guess I should say. And then so everyone kind of adds this tweak on the way forward. And then when a preimage is, or a scalar is revealed to you, then you subtract your tweak on the way back. And so this has a couple nice properties. A, it decorrelates all of the payments. No two people can know that they're on the same route, at least not nearly as easily, because there's no linking information other than amount and distance and all the usual things you have to worry about with the Lightning Network. And then also, you have the nice property that only the sender learns the true preimage. That is, the preimage to that invoice.

## Proof of payment

Nadav Kohen: 00:13:15

So in a lot of Lightning applications today and probably in the future, we have this thing called proof of payment, which we essentially treat the hash preimage as a proof of payment since it's received atomically with a payment being completed successfully. Only if your funds are claimed do you learn the preimage to this hash. And then you can use that preimage as kind of a receipt in various senses. You can use it as a literal receipt if you're doing accounting. You can also use it at the application layer as kind of like a lock on the payment. So for example, at SharedBits, we have APIs where you buy data from us over the Lightning Network. And how you do it is you ask for it. We give it to you encrypted with the payment hash preimage. And then once the payment is completed, you now have the preimage. And so you can decrypt that data if and only if we receive your payment.

John Newbery: 00:14:15

And that's a really nice model because it's kind of stateless from your side, right?

Nadav Kohen: 00:14:18

Totally. Yeah. So if we go down and our lightning node is still up or something like that, like if our API goes down or something like this, if you pay, you get the data. It doesn't really depend on anything external. But the issue with this right now in the world of HTLCs is that every single hop along the route gets your proof of payment. So they can go to a website and be like, I paid that invoice, even though you were the person who actually lost funds during that Lightning transaction.

John Newbery: 00:14:51

And there are potential attacks if the invoice does not have an amount? Someone on the route could somehow.

## Invoiceless transactions

Nadav Kohen: 00:15:01

Yeah, I think this is a somewhat separate issue. I think this isn't solved by PTLCs. Invoiceless transactions on the lightning network are quite tricky. In part because the person receiving doesn't inherently know how much they are supposed to be receiving. So the hop before them could take a super huge fee or something like this that they aren't supposed to. And I believe there are mitigations against these things. You can put information inside the TLV of the onion or something like that. But I don't know that that's been standardized. But yeah, I think that with HTLCs, The main problem is just it's yet another concern. On the application layer, if you want to use the hash preimage, you have to mix in someone's pub key, which means you need to get someone's pub key, these kinds of things. And So with PTLCs, this is kind of solved, because since there's a tweak along every hop along the way that gets added on the way forward and subtracted on the way back, only the original sender of the payment learns the preimage. And it can be really used without as much hesitation as a receipt that can be used to make things atomic with the lightning payment.

John Newbery: 00:16:27

Can we make things a little bit more basic and go back to HTLCs? So Alice, Bob, Charlie, in a payment route, Alice is paying Charlie. Who chooses the preimage and the hash and how do those get communicated and how is that different for PTLCs?

## Hashes, preimages, and HTLC mechanics

Nadav Kohen: 00:16:43

So in general today on the Lightning Network, the person getting paid, so in this case that would be Charlie, generates the invoice and puts it somewhere or sends it to Alice, not on the Lightning Network. And then Alice is then the person who sets up the payment. She decides what the route is, she decides to go through Bob and computes the fees and all of these kinds of things. She constructs the onion, which is the message that gets sent through the Lightning Network.

John Newbery: 00:17:14

And that invoice that Charlie created has the preimage?

Nadav Kohen: 00:17:17

It has the hash. The hash of the preimage, yes. So the payment hash is going to be inside the invoice, which Charlie created, and Charlie keeps somewhere the preimage to that hash. And then Alice goes ahead and sets up an HTLC to Bob, and Bob peels his onion and sees that he's supposed to then set up a payment to Charlie with the same hash. Bob does not know that Alice originated the payment. Alice could just be another hop on the route. And Bob also doesn't know that Charlie is the last person on the route. Likewise, Charlie doesn't actually know that Alice is the person paying him necessarily. He just knows that he has been paid for this invoice. So those are some nice privacy properties that we have.

John Newbery:

And very briefly, the onion.

Nadav Kohen:

Yes, the onion. So essentially, how you keep things nice and private while doing routing over the Lightning Network is, The person who is initiating the payment, in this case Alice, generates an onion and what you do is you kind of go backwards, starting at the end of the route, and you create the message that you want to give the last person, and you encrypt it with your shared key to them, with their keys essentially, And then you take that message. And so now that it's encrypted, only they can read it. Then you write your message kind of like on the outside of that to the next person. And you encrypt that. And you keep adding layers, which is why we call it an onion. And so as you pass this onion, people kind of like peel back one layer,

## Onion analogy

read what they can, and then they can't read anything more because it's encrypted and then they pass it on.

John Newbery: 00:19:02

And the bit that was added just for them tells them where they pass it on.

Nadav Kohen: 00:19:03

Yeah, exactly. And onion's not the best analogy because the onion doesn't actually lose size when you peel it. It just like gets more garbled, so to speak. All onions are the same size. So peeling is kind of like you take off a layer, and then you add on a fake layer on the inside, or something weird like that. I don't know exactly how it would be a good analogy.

## PTLC mechanics

John Newbery: 00:19:30

We don't have a vegetable that looks like that.

Nadav Kohen:

Yeah.

John Newbery:

OK, so that is HTLCs. PTLCs, same onion?.

Nadav Kohen: 00:19:35

Same onion. Same routing. Same routing.

John Newbery:

Charlie is going to create the secret just as before and create an invoice.

Nadav Kohen:

And so he puts the point in the invoice rather than the hash. And then Alice now generates the onion and when she generates the onion there is an extra step for Alice and what that extra step is is for each hop along the route and she computed that route she generates a random number a random scalar and then computes the points to those scalars. And then in the onion, she kind of has an additive tweak on each of those hops. And in the onion, which is a personalized message to just that one hop, she also tells each person what their scalar tweak is. And so because they need to subtract it on the way back. And so then in the protocol, everyone adds their point on the way forward. So if someone, if my tweak is like capital B, if Bob's tweak is capital B, and he has received a PTLC pointing at him with the point A, then he would set up a PTLC with the point A plus B moving forward. And then when he receives the preimage, like lowercase A plus B, he subtracts lowercase B and reveals lowercase A to the person in front of him. So everything is the same as HTLCs in the process, except for these additive tweaks on the way forward and subtractive on the way back.

John Newbery: 00:21:04

And so for the routing nodes, it's basically the same, except that the commitment and the reveal is a point in the scalar. But for Alice, for the payer, she's the only one who gets that original secret.

Nadav Kohen: 00:21:19

Exactly. She's the only one who gets the original secret. And then as far as the process goes, she has to generate all of the tweaks. And I forgot to mention, she also, the extra wrinkle that's different from HTLC is that she reveals the sum of all of the tweaks to the last person, Charlie in this case, because Charlie needs to be able to satisfy his PTLC and his PTLC is going to be the sum of all the tweaks plus his point. And so he knows the preimage to his point, and he needs to be given the preimage to the sum of all the tweaks. But that's just done in the onion, as you'd expect.

Adam Jonas: 00:21:55

And so it sounds like this is just superior in every dimension.

Nadav Kohen: 00:22:00

Yes. So not only does it give you payment decorrelation and protection against wormhole attacks, but also you can do all sorts of other fancy stuff with it, which I assume we'll be talking about shortly.

## Why don’t we use PTLCs today?

Adam Jonas: 00:22:14

Yeah, I mean, before we get to that, why hasn't this been pushed harder? It sounds like, just looking it up, it looks like it's been around for a while. Given the issues that we currently know about HTLCs, why wouldn't we go to PTLCs now and figure out how to do it better in the future.

Nadav Kohen: 00:22:36

Yeah. So first thing to note is that in order to implement PTLCs, as opposed to HTLCs, you need to implement some stuff that is not already available in Bitcoin script. So HTLCs are just native to Bitcoin script. They're currently implemented using stuff available in the base layer. Whereas to implement PTLCs, we need to either introduce signature system that has nice adapter signatures, which is the plan with BIP Schnorr. But we could also implement adapter signatures for ECDSA. But we just don't currently have any nice, well-tested libraries for doing this. I've kind of asked around people who I know who are working on LibSec P, and it sounds like they find it interesting, but they also think like Schnorr is better. It's better not just in that we're getting it and everyone will be using it, but also that Schnorr adapter signatures have better security guarantees than ECDSA adapter signatures. They give you a bigger anonymity set. They do lots of other things in superior ways to ECDSA adapter signatures. And so I guess short answer is no one has ever gotten around to implementing ECDSA adapter signatures in a nice, tested library. And part of that is Lightning is relatively new, and HTLCs have not been the biggest issue that has been kind of the active field of work in Lightning. We're working on various liquidity issues, atomic multipath payments, rendezvous routing, trampoline routing, all these kinds of other issues. And this payment points has kind of taken the back seat because we know that Schnorr is coming to fix it. And so.

Adam Jonas: 00:24:52

And you think that's the sentiment? Is Schnorr arrives and this is a drop-in solution?

Nadav Kohen: 00:24:53

That's what I understand of it. And I know that I'm going to be pushing to make sure that we're implementing PTLCs, hopefully before Schnorr even hits the base layer for Lightning. But yeah, I think I saw in March of 2017, there was an email post by Andrew Polstra showing how to do lightning channels using PTLCs in Schnorr. And so I think We know what we want to do, but we're just kind of waiting for Schnoor to hit base layer before we go ahead and implement this.

Adam Jonas:

So all those, that magical timeline sort of unfolds, and then What else could we do? What does this unlock?

## Improving proof of payment

Nadav Kohen: 00:25:47

Yeah. It unlocks quite a few pretty cool things. Most of them have to do with the additive property of points. You can add more things in. And then there's some other fancy point stuff you can do, but I'll get to that probably in a second. So I think the first really cool thing that you get is there are a lot of proposals going around right now, some of which are already implemented on the Lightning Network, such as multi-path payments. Another example is invoiceless payments, which are also known as spontaneous payments. I think those are implemented on LND right now, but I could be wrong. And both of these have an issue when using HTLCs, that since the sender has to do some of the work in constructing the payment hash, it turns out that since we're using hashes, they have to do all of the work. There's no input that you get from the last person, and so you already know the preimage as the sender. So this isn't actually an issue. You don't have any problems in terms of the atomicity or security of completing a lightning payment. If the sender, the person who initiates the payment, knows the preimage, because they never reveal it to anyone. And so it would be an issue if someone along the route knows the preimage early. But if the person who is initiating the payment knows the preimage, it doesn't actually have any adverse effects. So for example, How a spontaneous payment works is, say, we have Alice, Bob, and Charlie again. Alice, without an invoice, creates a payment. She generates the preimage. She generates the hash from that preimage. She sets up the onion in the same way. And then in the innermost part of the onion, the part that only Charlie can read, she writes down what the preimage is. So now this gets passed forward, peeled, peeled, peeled. Charlie gets it. He's like, oh, a payment. What's this? Opens it up, sees that the preimage is written inside, and then he can go turn back to Bob and claim that payment. And this is how that works, but it has the issue that you have no proof of payment because Alice has learned nothing by having... She knows that Bob has... She knew the preimage to begin with, So she can't use it as a proof of payment. And the same is true for multi-path payments right now. The sender generates the preimage that they then get revealed to them at the end. And there's some other proposals. Stuck-less payments would require the sender do some work in these payments that are called stuck list payments, and that would mean that they would have no proof of payment in that scheme either. And just generally, there are a decent number of cool things we can do on Lightning if we're willing to sacrifice proof of payment, which is sad for us at SharedBits where we're trying to use the proof of payment as a way to create lightning paywalls and stuff like this. So all of this is easily solved with payment points by just adding the stuff that needs to be generated by the sender plus stuff that is known and generated by the receiver. And then so as an example, with like an atomic multi-path payment, rather than having the sender generate all of the preimage and then just having it so that the preimage gets discovered by the receiver when all of the paths are set up. You can do all of that but then also to each of these paths add a point that is generated by the receiver And so then the receiver still learns what the point generated by the sender was, or what the scalar, sorry, generated by the sender was. And then they can just add that scalar to the one they know, and then reveal that. And then when that gets back to the sender, the sender learns kind of the sum and they know their part so they subtract it away and they can use the other part as proof of payment. So essentially just add the receiver's point to anything and you get free proof of payment for everything. So that's kind of the simplest non-magical math thing you can get using PTLCs instead of HTLCs. Trying to pick which one to do next. Do you have a favorite?

John Newbery:

Well, you mentioned something there called stuckless payments. Yes. That's intriguing.

## Stuckless payments

Nadav Kohen:

Yeah, so stuckless payments are, is a proposal where rather than, so currently kind of the situation I described, you have a payment setup phase immediately followed by a payment kind of completion phase. I forget what the actual name for it is in Stuckless Payments, but that's what we have. And the proposal is to add an update phase. So rather than having, so say, think about it in terms of spontaneous payments for HTLCs, because you can't have proof of payment with HTLCs. So if I have a spontaneous payment, but where Alice doesn't write the preimage inside the onion, and instead tells Charlie what Tor address to go ping and ask for it. And so essentially, the idea here is that if my payment gets stuck during setup, I can safely retry another payment because the actual preimage only gets revealed to the person, to the receiver of the payment once. So since the sender knows the preimage and just tells Charlie, Alice tells Charlie where to go ask her for the preimage. And she can set up as many routes and try as many payments simultaneously or in sequence as she wants with Charlie. And the first one Charlie receives, he's going to go ask her for it, and she's going to reveal it to him. And she's, by the way, I should have mentioned, she's using different preimages for each of these payments she's setting up. Otherwise, that would kind of defeat the purpose. So yeah, anyway, the first one, Charlie receives, he goes and asks for the preimage, and Alice makes a note of this and makes sure not to reveal any of the other preimages to him. So Charlie should just fail the rest of the payments. And so, upsides and downsides to this proposal. The only downside is that Charlie has to go find Alice via some other means. There have been some proposals that he uses an alternative route to just send a message over the Lightning Network or various other things that use the Lightning Network. Or you can just post something on Tor and go out of band. But however it happens, if we have that extra round trip available to us, then what we can do is we can have Alice kind of retry or set up simultaneously as many payments as she wants and have only one of them be completed. And it also is nice and interoperable with atomic multi-path payments, so she can retry sub-payments in an AMP. And yeah, I think probably how this will actually manifest is you try a payment and you wait a second or two and if it's still not done, you just try again on a different route to try and improve kind of the payment experience on Lightning. And another cool thing to mention about it is that only the receiving and sending nodes need to have the feature implemented. All of the routing nodes, To them it just looks like a normal payment that either fails or succeeds. And so this can be like an odd feature bite or feature bit on, no I guess byte, an odd feature byte on Lightning, meaning that not everyone has to have it implemented in order for everyone to coexist and do their thing.

John Newbery:

So how do PTLCs play into this?

Nadav Kohen:

So PTLCs just add proof of payment to the scheme. So if you do the scheme using HTLCs, Alice must generate the preimage entirely rather than just a part of the preimage, as she would in PTLCs. So with PTLCs, you can, because right, if you're trying to do, If this becomes like the norm on the Lightning Network, where all payments are stuckless payments, or even a majority, or many payments are stuckless payments, it would be a real shame if we just like got rid of proof of payment entirely on the Lightning Network. And with PTLCs, we don't have to.

John Newbery: 00:35:01

And what happens to all of those failed payments?

## Spam on Lightning

Nadav Kohen: 00:35:02

They act like normal failed payments on the lightning network. So they kind of propagate backwards from their point of failure with failure messages kind of going backwards on the onion, essentially. And everyone just gets their funds back and if anyone tries to hold off on that, then you go on chain and use the time lock. But normally, payments just pretty quickly fail. You update and remove that HTLC from your commitment transaction. Yeah. And Not to downplay the fact that right now on the Lightning Network, it is very spammable. Please don't, but you could spam it in lots of different ways. You could pay yourself and hold onto those and fail those. Essentially because of the routed nature of the Lightning Network, your cost to hold up other people's money and just lock it up, you get a 20x multiplier on your funds. You can just take a long route to yourself and hold up a little bit of your funds and the same amount of 19 other people's funds and channels. So I know that there are people working on the spam problem and I think it's really important, but we don't have too much spam on the Lightning Network right now, luckily.


John Newbery: 00:36:33

Let's keep it that way.

Nadav Kohen: 00:36:34

Yeah, for a little bit, until we figure it out.

Adam Jonas: 00:36:41

Let's talk about a few other things. Tell me about escrow contracts or Schnorr signatures or anything else that you're excited about.

## Selling Signatures and Schnorr signatures off the main chain

Nadav Kohen: 00:36:49

Totally. Schnorr signatures, although they aren't on main chain right now, can still be used off of the main chain in things like discrete log contracts. And also, I just realized, since payment points, so if we implemented payment points today, meaning like ECDSA adapter signatures, we could still use Schnorr signatures off-chain. And so that's what I'll describe here. So Schnorr signatures have this nice property that, well, first of all, for those who don't know, Schnorr signatures, like, the resulting signature is a scalar. It's just a number. And so for any number, you can compute a point on an elliptic curve. And so if you take the signature times g, or you take the point of the signature, essentially the public key, if you treated the signature as a private key, If you take that point, you can actually compute that point from the signer's public keys without knowing anything about the signature. And so what this means is that you can, on a PTLC Lightning Network, pay someone for a valid digital Schnorr signature of a specific message in a completely trustless fashion. You can, from their public keys, compute the point associated with that signature, and then make that signature, or make the scalar behind that point, which is the signature, your proof of payment. And so you can trustlessly pay people for their signatures. So for example, when I mentioned earlier that at SharedBits, we are encrypting data with the payment hash preimage, that requires that you trust SharedBits, that we're not just giving you garbage. And if you wanted to pay us right now over HTLCs for a specific piece of data, you could not, without some very heavy zero-knowledge proofs, verify before completing that payment that we indeed were giving you the encryption key for that or the decryption key for that. Whereas once we have payment points you can trustlessly pay people for their signatures of specific messages. And you can actually, you can go kind of a step further, so I can add these points whose preimages are signatures to anything else.

## Contingent payments

So you can make contingent payments where the payment is contingent on the receiver learning of a signature. So an example of this would be, say I have an oracle some place that will be signing a specific message if Bitcoin is over 10K at the end of this weekend or something like that. And say I want to pay you 10K Satoshis if this happens. Just as like, oh, woohoo, it happened. So I get a point from you, which will be my proof of payment. And then I compute from the Oracle's public keys the point that would be associated with their signature, the point whose preimage is their signature of, like, moon or whatever message they decide to sign. And then I add these two points together and I use that as the point in my PTLC. And now you won't be able to claim this payment unless the Oracle signs this message. And so if they do, then you just add that signature to your preimage, and you get kind of the sum preimage, which is the one you need to claim this PTLC. And I will see that my funds have gone and at the same time get the signature from the oracle as part of my kind of payment completion, as well as a proof of payment from you. And you can kind of just do this generally. Like you can add as many SIGs together as you want. They can be oracles. They can be like other parties involved in multi-party schemes. But you can make contingent payments on signatures being revealed. And the really cool thing with all of this payment point stuff is like everything is interoperable. Like you can have stuckless AMPs in which I'm doing like a multi-party thing that's using payment points, that's using like signature revealing as part of it and stuff like that.

## Escrow contracts

So there's all sorts of kind of like interoperable things, which brings me to the next thing you can do with payment points, which is these escrow contracts. So something of a similar flavor to kind of these signature contingent payments, but somewhat different in how they work and kind of what the trust and execution model is. So say that Alice wants to pay Bob if Bob cleans her house, or something like, there's some thing in probably the real world. It doesn't have to be in the real world, but let's say it is. And so they both agree to some third party, which we call an escrow, say like Aaron, who they both trust to report truthfully whether or not Bob has cleaned Alice's house. Now, they don't actually contact Erin necessarily, or they don't have to tell Erin what she's being used for, or just generally there's a nice kind of privacy layer here. And so what they do is they take a signature from Erin, because they know her public keys, and they compute a point for a signature from Erin. And then they, so essentially what we want here is we want a payment to go through if Bob and Alice or Bob and Aaron agree that this payment should go through. So either Alice can say, you cleaned my house well. Here you go. And the payment should go through. Or if Alice isn't there or Alice is not cooperating, then they can go to their mediator, Aaron. And Aaron, along with Bob, can help this payment go through. And so how we do this is we take Bob's point and we add it to, we want a point whose preimage can be computed by either Alice or Aaron. So, so far we've just been talking about how you can add points together and that essentially acts like an AND logically. And it turns out that using some fancy math, you can usually create these OR points. There are a couple different ways of doing this. One of them is verifiable secret sharing. Another way of doing this is through verifiable encryption, which is probably what you would do in this case. So what that means is you have Aaron's public keys, so you can encrypt things that only she can decrypt. And so what you do beforehand is Alice will verifiably encrypt, meaning encryption plus some simple zero knowledge proofs that you're following the rules of the encryption. And so Alice verifiably encrypts her preimage, her scalar, using Aaron's public key. And then she gives this encrypted value over to Bob. So now if Alice agrees, she just reveals the scalar directly to Bob if Bob has cleaned her house. And now, A plus B, Bob has the preimage he needs to claim this payment. But if Alice isn't agreeing, Bob can go without Alice's permission to Erin, give her this encrypted value. And if Erin agrees that Bob has cleaned Alice's house then Aaron can decrypt this value and give it to Bob and this value is the preimage that Alice generated. So you can do these kinds of OR schemes and in general these points with what are called monotonic access structures. That's just an access structure is just like, what are all the sets of people who can collaboratively compute the preimage to this point? And so a monotonic access structure is just all of the access structures made up of ANDs and ORs. And so I'm not too comfortable claiming you can get all of these with all of the different constraints on privacy and all these other things. But you can usually find a way, sometimes more complicated than others, to create ORs as well as ANDs. And so, and as I mentioned, all of these things are kind of composable. So you could have it like be this escrow or this oracle and this person or whatever else. And you can make all of these kinds of interesting contingent payments. And contingent payments is just another way of saying contracts, right? Like a smart contract is really just a contingent payment where the execution can happen in various ways.

## Atomic multiparty setup and payment renegotiation

In this case, you can always kind of abstract your execution to someone signing off that the execution did something or something like that. We're not kind of just confined to Aaron said Bob cleaned Alice's house. Aaron could also say that the result of running this program with these inputs, like this arbitrary program, is like this output or whatever, and she can sign that message. And then you can use that in a contract. And so you can get these pretty general contracts just from having payment points lying around. And everything to everyone not involved in these payments looks like a normal lightning payment just like it does right now with HTLCs. Yeah and you can do even more with payment points that I'm not even talking about right now. I won't get into how these work because they're quite complicated but I claim and I have yet to write it up too formally, it's on a mailing list post somewhere, that you can do atomic multi-payment setup. So you can set up multiple of these contingent payments in various directions between a ton of parties, and you can have all of the setup kind of happen atomically so that you don't have a problem of, like, I set up a payment to you, and you haven't set up one to me yet. And then you can also do payment renegotiation, where you cancel out-ish one payment while setting up another one under different circumstances. So this came out of work dealing with like, you have a discrete log contract set up using payment points on Lightning and you want to sell your position to someone else and you can do that using Lightning. And you can't do that on-chain, which is cool.

John Newbery: 00:47:56

Cool, well, maybe we can have you back on the podcast once that's on.

Nadav Kohen: 00:48:00

I'm working on a blog posts as we speak. So those should be out soonish at sharedbits.com/blog

## ETA of payment points

John Newbery: 00:48:06

We will include that link in the show notes. OK, just to wrap up, when payment points?

Nadav Kohen: 00:48:12

When payment points. When Schnorr? Hopefully very soon after that. I'm very hopeful that the closer Schnorr gets, the more people take time aside from their busy lightning developer lives to go look at my fancy theoretical not useful right now payment point write ups and stuff like this, get super excited and then go implement it. So that would be great.

John Newbery:

Cool. Well, thank you so much.

## Outro

Caralie Chrisco: 00:48:55

We hope you enjoyed that episode.

John Newbery: 00:48:57

Well, I really did. We had a great conversation with Nadav and I think payment points are fascinating, especially the use cases that they open up.

Caralie Chrisco: 00:49:06

Speaking of fascinating, if you are looking to level up your knowledge on Bitcoin Core or the Lightning Network, go to residency.chaincode.com/resources. And we have plenty of study groups, we have our curriculum up there, and it would be a great way for you to dig into the material in this time of isolation.

John Newbery: 00:49:31

Bye.
