---
title: Basis of Lightning Technology 12
transcript_by: mubarak23 via review.btctranscripts.com
media: https://www.youtube.com/watch?v=LSP0p_IPUIM
tags:
  - offers
speakers:
  - Sjors Provoost
  - Aaron van Wirdum
date: 2021-08-13
episode: 44
summary: |-
  In this episode of The Van Wirdum Sjorsnado, hosts Aaron van Wirdum and Sjors Provoost discuss BOLT 12 (Basis of Lightning Technology 12), a newly proposed Lightning Network specification for “offers”, a type of “meta invoices” designed by c-lightning developer Rusty Russell.

  Where coins on Bitcoin’s base layer are sent to addresses, the Lightning network uses invoices. Invoices communicate the requested amount, node destination, and the hash of a secret which is used for payment routing. This works, but has a number of limitations, Sjors explains, notably that the amount must be bitcoin-denominated (as opposed for fiat denominated), and the invoice can only be used once.

  BOLT 12, which has been implemented in c-ligtning, is a way to essentially refer a payer to the node that is to be paid, in order to request a new invoice. While the BOLT 12 offer can be static and reusable — it always refers to the same node — the payee can generate new invoices on the fly when requested, allowing for much more flexibility, Sjors explains.

  Finally, Aaron and Sjors discuss how the new BOLT 12 messages are communicated over the Lightning Network through an update to the BOLT 7 specification for message relay.
aliases:
  - /bitcoin-magazine/bitcoin-explained/basis-of-lightning-technology-12
---
## Intro

Aaron Van Wirdum: 00:00:09

Live from San Salvador and Utrecht, this is the Van Wirdum Sjorsnado. Hello! Hey Sjors, welcome back.

Sjors Provoost: 00:00:19

Thank you.

Aaron Van Wirdum: 00:00:19 

It's been a while.

Sjors Provoost: 00:00:20

I mean I'm not physically back.

Aaron Van Wirdum: 00:00:24

Yeah, I'm the one who's not physically back. I'm still hanging out in El Salvador checking out what's going on here with the new Bitcoin law.

Sjors Provoost: 00:00:33

Sounds fun.

Aaron Van Wirdum: 00:00:35

So yeah, we're doing another episode remote, which always kind of sucks, but let's make the best out of it.

Sjors Provoost: 00:00:43

Indeed.

Aaron Van Wirdum: 00:00:43

Sure.

Sjors Provoost: 00:00:43

It should be fun.

Aaron Van Wirdum: 00:00:45

Today we're discussing Bolt 12.

Sjors Provoost: 00:00:48

Yes. I forgot to prepare any kind of pun for that, but yes.

Aaron Van Wirdum: 00:00:52

Hey, Bolt itself is a pun. The Lightning developers fixed that one for us.

Sjors Provoost: 00:00:59

Yeah, that's true. All right, it stands for our basis of lightning technology, which is comparable to a BIP, as we've discussed in an earlier episode for a Bitcoin Improvement Protocol. But it's also different from a BIP.

## Basis of Lightning Technology


Aaron Van Wirdum: 00:01:12

The pun obviously being lightning bolt for those listeners that are particularly dense. And yeah, it stands for Basis of Lightning Technology. And like you mentioned, it's like a BIP, but for lightning specifically, right?

Sjors Provoost: 00:01:26

Yeah. And of course, it makes it really hard to Google anything, right? So If you're trying to find out what is a bolt, and then you add bolt lightning, you're just not going to find anything related to the protocol. So, it's really smart.

Aaron Van Wirdum: 00:01:39

Right. So far, there were apparently 11 bolts. Is that right? Yes. So, there's basically 11 specifications of how the Lightning protocol works?

Sjors Provoost: 00:01:52

Yeah, exactly. So that is the distinction between BIPs and BOLTs, I would say. BOLTs are really a specification. So they're a lot more formal in that sense. So, usually what they do is somebody proposes a bolt and then if there's two implementations of different Lightning implementations that support it, then it's ready.

Aaron Van Wirdum: 00:02:18

Right. So, there were 11 so far and there's now a 12th bolt. Or is it a proposed bolt or what's the status of this?

Sjors Provoost: 00:02:26

I think it's proposed because the only implementation is in C Lightning.

Aaron Van Wirdum: 00:02:29

Right. So it would be official if some other implementation adopts the same thing?

Sjors Provoost: 00:02:34

I think so.

Aaron Van Wirdum: 00:02:35

Right, so it's a proposed bolt and it was proposed by Rusty Russell, I think?

Sjors Provoost: 00:02:42

Yes, he actually gave a presentation about this in September 2019 in Berlin at the Lightning Conference there, which was fun.

Aaron Van Wirdum: 00:02:52

Right. So 11 bolts so far, this could be the 12th bolt. So the Lightning specification or the Lightning protocol could be upgraded or expanded, extended. And we're going to explain, you're going to explain mostly. It's going to be mostly you, Sjors, this episode, I think. And everyone knows that if the two of us do a lighting episode. These are usually the best episodes.

Sjors Provoost: 00:03:22

I think we can do an okay job at explaining this one. Hopefully, we'll hear.

Aaron Van Wirdum: 00:03:28

All right, let's see how far we get. So, Bolt 12, what is it? Sjors, Take it away.

Sjors Provoost: 00:03:33

Well, maybe we want to take one step back and talk about Bolt 11 or more generally invoices.

Aaron Van Wirdum: 00:03:40

Right, yes. Because Bolt 12 is essentially a new type of invoice or an extension of how invoices work? Is that the right way to put it?

Sjors Provoost: 00:03:50

Yeah, like a meta invoice, I guess.

Aaron Van Wirdum: 00:03:52

Right. So the Lightning Network, the Lightning Protocol currently uses invoices. So yes, let's first Explain what is a Lightning Invoice? What is this?

Sjors Provoost: 00:04:02

Yeah. So a Lightning Invoice is just a piece of text and it has a computer readable, of course, and it has a couple of things in that text. One is the node that the transaction needs to be sent to. So a node is just a public key. There's usually an amount, like how much satoshis are you expecting. And the interesting ingredient, there the hash of the secret. So the idea is that when you're actually paying an invoice, you're going to get the actual secret rather than the hash of the secret. And that's how this whole chain of HTLCs that we talked about with Joost Jager. That's kind of how they cascade. So those are the three ingredients that are on an invoice. So if you're selling me an apple, you tell me how many Satoshi you want for the apple, the hash or the secret and what your note is, and you can add a bunch of other things to the invoice that are not very important for this conversation. Like a description and some hints on how to route to you.

Aaron Van Wirdum: 00:05:11

Right, yeah. So an invoice is just a piece of data that tells you what my node is, because all nodes on the Lightning Network have their own identifier, which we mentioned is a public key, plus the amount, plus a hash, which is sort of the magic of how the Lightning Network works. So, I communicate this information in an invoice to you and that's how you know how to pay me. That's what an invoice is, right?

Sjors Provoost: 00:05:39

Exactly, and then my wallet would just pay that invoice by sending a bunch of messages and constructing a payment and doing the routing stuff and all that stuff that we talked about earlier.

Aaron Van Wirdum: 00:05:51

Right. So this sounds perfect to me.

## Problems with Lightning


Sjors Provoost: 00:05:54

Yeah, it is. It's amazing and you know, Lightning has been working. So it's not the end of the world.

Aaron Van Wirdum: 00:06:00

So what's the problem? Well, there's a couple of them. Why fix what isn't broken, Sjors?

Sjors Provoost: 00:06:06

There's a couple of problems. So let's say you have an apple in your store and you have this Lightning invoice and you decide to make the Lightning invoice early on. So you want to put it on a sticker and you put the sticker on the apple. The problem is you have to set the amount of satoshis. And so by the time I go to your shop and pick up the apple, maybe the exchange rate, doubled.

Aaron Van Wirdum: 00:06:30

Right.

Sjors Provoost: 00:06:30

The apple is too expensive and you'd have to make a new sticker. So volatility basically is kind of hard to deal with in this way. It's fine if you make the invoice real time, but not if you want to make them in advance and print them out.

Aaron Van Wirdum: 00:06:44

Yeah, we're assuming that a lot of people are not using Bitcoin as a unit of account yet. They're still using some kind of fiat currency as a unit of account, but they want to be paid in Bitcoin. So you want to be paid $1 in Bitcoin for your apple, rather than a fixed amount of satoshis for your apple. And that's hard to do with a static Lightning invoice. You'd have to create the invoice at the moment of sale and you can't make it in advance. So that's one limitation.

Sjors Provoost: 00:07:17

Another one, and there is a workaround for that too - none of these are end-of-the-world problems - is that this hash of the secret that we talked about, you can only use this once. So If you want to have a tattoo on your body with a lightning invoice, that's not a good idea because the first person who pays it, then there's a chance it's going to leak and the mechanism won't work anymore. So then you'd have to print a bunch of QR codes on your skin. If you use the henna tattoos, I guess you can do that. There's also another workaround for this problem of incurring payments.

Aaron Van Wirdum: 00:07:54

I think it's not technically really that it doesn't work. It's just that it's not secure, right? Because the secret needs to be a secret. That's why it's a secret. While if you've used it once, then the secret has been sort of used on the Lightning Network. And therefore, if you create a new invoice with the same hash of a secret, then someone else might know the secret and therefore claim funds that they weren't supposed to claim, right? So that's why every invoice should only be used once. So every secret is only used once. So you can't use the same invoice for different apples. In my apple store, I can't put the same sticker with the same price on every apple because once the first person buys an apple, the secret is gonna be out there and all the other apples. I'm running a big risk of having my apples stolen basically.

Sjors Provoost: 00:08:54

So one solution to that problem that already exists is that instead of making an invoice, you only publish your node identifier and then the customer just basically enters the amount themselves and send it to your node. So you're kind of leaving that to the customer. Of course that's annoying too because then how do you do automatic handling of payments because you're expecting a certain amount? And what if it goes wrong? If the customer types the wrong amount, that's kind of not ideal, but it's possible. And for donations, it's fine, right? For donations, you can have a, I guess, a tattoo with your node identifier on you, and then people can donate you because it's up to them how much they want to send anyway. There are solutions to that. If you Google, for example, keysend.

Aaron Van Wirdum: 00:09:43

We've now mentioned two downsides of the current invoice system. One of them is fiat volatility. The other one is you can't really reuse the same invoices in a secure way. Are there more?

Sjors Provoost: 00:10:00

I mean, that's sort of the main thing.

Aaron Van Wirdum: 00:10:03

Yeah. These are the two.

Sjors Provoost: 00:10:04

Well, the other thing is, but it's not really a downside, an invoice can only be used to receive money. It can't be used to send money. So you can't do a credit invoice.

Aaron Van Wirdum: 00:10:18

Give me a concrete example of this. When would you want to create an invoice to send money?

Sjors Provoost: 00:10:25

A Bitcoin ATM. So if I put $10 into a Bitcoin ATM and I wanted to send me that amount in satoshis over the Lightning Network, then the way that works right now is that, or well there's some other technologies, but what we just described is you as the person using the ATM has to make an invoice for that ATM and then the ATM will pay you if the invoice is what it wants. And that's not ideal. Ideally, what you want to do is you want to give money to the ATM, like a piece of paper, and then it should show you a QR code and you scan that and then it pays you. So it's a credit invoice.

Aaron Van Wirdum: 00:11:03

Right.

Sjors Provoost: 00:11:03

That's what you'd like to see. And there are some workarounds for this. So it's not the end of the world again.

Aaron Van Wirdum: 00:11:09

Right. So the current invoice system, it works for what it needs to do. However, we've now mentioned, three main limitations. One is you can't create the invoice ahead of time, at least if you're pricing stuff in fiat, because of the fiat volatility. The second one is you can't reuse the same invoice because it's not really secure because the secret is exposed after the first time. And the third sort of downside is that you can't create an invoice to send money. Am I saying it right? I think so.

Sjors Provoost: 00:11:41

Yeah. And as far as I know, some or all of these are solved in practice, not at the protocol layer, but at the application layer with something like LNURL. So we can do a whole other podcast going into that. But for now, we're going to talk about a solution at the protocol level, which is called Bolt 12.

Aaron Van Wirdum: 00:12:01

Bolt 12. All right, there we go. Bolt 12, you mentioned, it's like a meta invoice. You can consider it like a layer on top of regular invoices that communicates not just invoice data, but something on top of that, right?

Sjors Provoost: 00:12:20

It doesn't even communicate the invoice. In the apple example, the bold 12 thing, the sticker that you put in your apple, might say, this is an apple. This is the identifier of the apple for the store, maybe has some SKU, some unique number, and this is the lightning node and please go talk to this lightning node. Then what the customer app will do is it scans the QR code, it sees okay this is an apple and I have to talk to this other node, it then calls the other node and says please give me an invoice for this apple and then the node actually gives you an invoice for the apple right then, which you can pay. Which means the Lightning Node for the store can calculate the exchange rate, for example, right at the last moment. And then it's paid as a regular invoice.

Aaron Van Wirdum: 00:13:16

Right. So Bolt 12 is essentially a specification for a protocol of how to contact a specific node, which would be the node you want to pay. And then that node knows how to respond to that request by creating an invoice. Is that right?

Sjors Provoost: 00:13:36

Almost. So, it's not really how to contact a node because that's sort of known how to do that. But it is, or it might actually, I don't know. But it is saying you should contact this node because this node is who can give you the invoice.

## Subscriptions


Aaron Van Wirdum: 00:13:52

So with Bolt 12, you get the info on which node to contact and at that point, an invoice is created. Therefore, we're solving the time problem because the invoice is created at the exact time that you want to make the payment, even though the Bolt 12 meta invoice was stuck on my apple for a while. And we're fixing the secrets problem because the invoice is created uniquely even though the sticker was on my apple for a while. But Sjors, is there more?

Sjors Provoost: 00:14:28

There is more. One thing you can do now is subscriptions. So Bolt 12 has a special way to indicate that this is a subscription. So it can say, please don't ask me just for one invoice, but ask me for an invoice every week or every month. And it can even say, well, the invoice should be $10 every month rather than say 10 satoshis every month.

Aaron Van Wirdum: 00:14:53

Right. So, if you want to buy an apple from me every month, that's the worst example probably.

Sjors Provoost: 00:15:03

Yeah, it's a terrible example.

Aaron Van Wirdum: 00:15:04

If you want to buy an apple from me every month, we can actually automate that.

Sjors Provoost: 00:15:10

Yeah, exactly.

Aaron Van Wirdum: 00:15:13

So Bolt 12 can sort of include that information. It can offer to create an invoice every month, but there's still a lot of work to be done on the wallet side to actually make this happen in reality. Like Bolt12 in itself doesn't solve this, right?

Sjors Provoost: 00:15:35

No, in particular, because if you're talking about sort of an automated payment every month in a different exchange rate even, then that creates a few problems, right? So for example, if let's say it's automatic, you don't want to think about it too much, but then the server side, the recipient, so let's say the Spotify or whatever, they create this invoice every month for $10 based on what they think the exchange rate is. And then your wallet asks for that invoice once a month. So, hey, do you have a new invoice for me? And the server says, yeah, here's one. And then the wallet has to say, well, according to me, it's $10.01. And so then you have to say, okay, what percentage of disagreement is okay? That sort of stuff would need to be worked out and what what does the wallet do if there's not enough balance? Is it nag the user or not? And from mobile wallets it's even more tedious because mobile applications tend to be off in the background. So they have to wake up at the right time to ask for new invoices. So there's definitely work to be done, but at least specifying what the subscription should be, that can be done at the protocol level.

Aaron Van Wirdum: 00:16:46

Bolt 12 enables this. There's still a lot of work to be done behind the screens, but at least now there's a way to sort of start doing that. And there's even more. This is amazing. Sjors.

Sjors Provoost: 00:17:00

This is amazing. Well, we talked about the Bitcoin ATM.

Aaron Van Wirdum: 00:17:04

Yes, that's the problem we haven't solved yet.

Sjors Provoost: 00:17:07

Right. So I put in $10. And now it's solved because the ATM will display a Bolt 12 thing - offer is the technical term - and it will say, take my money, would you like this $10 worth of satoshis? And then my wallet if it understands this, it will create the invoice and give it to the ATM and then the ATM pays it. So there we have the reverse flow. So my wallet creates an invoice and the ATM sends to it.

Aaron Van Wirdum: 00:17:39

Right. So Bolt 12 is a communication layer that allows Lightning nodes to communicate invoices. I think that's the very short way to put it, right?

Sjors Provoost: 00:17:53

Well, except that it is not the communication layer. So that's, I guess, what we need to explain next. It's more of a meta invoice.

Aaron Van Wirdum: 00:18:01

That's exactly what I was getting to, Sjors. You read my mind. Perfect.

Sjors Provoost: 00:18:05

Exactly.

Aaron Van Wirdum: 00:18:06

So if we're creating a new communication layer or new ways for nodes to communicate, how does this actually work? How is this data sent from one Lightning node to another?

## Onion Messages

Sjors Provoost: 00:18:19

Well, it will use an extension, I think, Bolt 7 called Onion Messages. So, the Lightning Network already uses Onion Routing to send payments. As I think we've discussed in earlier episodes what onion routing is. I send a message to the next node or a payment to the next node and then they send it to the node after that, etc. And every node only knows where it came from and the next hop.

Aaron Van Wirdum: 00:18:50

Well, to be more exact, every node knows from which neighboring node it got it and which next node, but it doesn't know where the message started or where the message will end, right? Or what the message is because it's encrypted on every step.

Sjors Provoost: 00:19:05

Yeah, because as you unwrap, as you unpeel the onion, basically, there's a new secret and a new secret and a new secret, and only the final destination will know precisely what was in there. And there's some tricks to make it look the same size. So yeah, you can't see how far along in the route you are. We talked about that with Joost Jager with this crazy postal analogy that didn't work.

Aaron Van Wirdum: 00:19:28

Yeah, I remember. So right now it's already possible to send messages over the Lightning Network, I think. Is this done by using zero Bitcoin payments or no?

Sjors Provoost: 00:19:42

Yeah, either zero Bitcoin payments or very small payments. So what you're basically doing is sending a fake payment or a very small payment. And that's using the usual routing mechanisms that we talked about earlier. And then next to the payment or even the fake payment, there's a message, which is whatever the message you want to send. So this protocol upgrade actually makes that more elegant. Just to be resource intensive especially, because those fake payments...

Aaron Van Wirdum: 00:20:11

Sjors, Sjors, Sjors. I want to make this clear for myself and for our listeners. We just discussed Bolt 12, there's another bolt, Bolt 7. Bolt 7 specifies what we just described, how that currently works. Is that correct or no?

Sjors Provoost: 00:20:31

Yes, exactly. Right. The whole onion routing thing.

Aaron Van Wirdum: 00:20:34

And what we're going to be discussing now is an extension of Bolt 7 to help Bolt 12?

Sjors Provoost: 00:20:41

That's right.

Aaron Van Wirdum: 00:20:42

Right. Okay. So we're going to discuss it.

Sjors Provoost: 00:20:44

And maybe create the future in general because it's pretty cool.

Aaron Van Wirdum: 00:20:47

Is it a proposed change to Bolt 7 or is it already changed? It's a proposed change to Bolt 7. Yeah. Okay, so how would Bolt 7 be changed?

Sjors Provoost: 00:20:57

I think one way to say is it decouples the messaging from the payment side. Because so far when you use this Onion routing messaging in Lightning, you're actually trying to make a payment. But now, this can be separate. So you can actually send a message to any node on the network that supports this. And even ones that you don't have a payment channel with, so it's much easier to come up with a route and it'll just forward it to the final destination.

 
Aaron Van Wirdum: 00:21:30

Right. So right now if you want to send a message over the Lightning Network, you're actually using all the payment routes, which are, you know, the payment channels. Even though it's a zero Bitcoin payment, you're still using the existing payment channels.

Sjors Provoost: 00:21:46

And you're really taxing those channels too, right? You're holding coins in reserve and all sorts of complicated things.

## Deep Dive

Aaron Van Wirdum: 00:25:02

Right. And with this proposed extension to Bolt 7, you wouldn't actually use the payment channels anymore. You just send messages to other Lightning nodes on the network.

Sjors Provoost: 00:25:13

Yeah. And this means that, at least for now, this would be free as in any node will just relay any message that it's getting. Is your rate limited?

Aaron Van Wirdum: 00:25:23

Because so far there was a fee involved, it was just a regular payment channel fee type of fee? 

Sjors Provoost: 00:25:28

 Yeah. So when you make a payment, every hop you have to pay a little bit for. Now if you have a fake payment, you don't end up actually paying, so it is a problem. But if you're making small payments or zero payments, then you are paying all the routes in between for the service of relaying a message. But this new extension does not require that. But the good news is that it is far less resource intensive. Because the node that receives a message and needs to relay it, can do that in one go and then it can forget it ever happened. It doesn't have to track anything. There's no secrets or all that sort of stuff.

Aaron Van Wirdum: 00:26:06

Right. That's the good news. Is there also bad news?

Sjors Provoost: 00:26:10

Well, the bad news is because it's free, it could be DDoSed. So, a node would have to rate limit things like don't send too many messages. And it's not guaranteed to arrive. So when you're sending a message using this Bolt 7 extension, it may arrive. It's like UDP in the network protocol.

Aaron Van Wirdum: 00:26:30

Right. So, if you're currently sending a message over the Lightning Network, you're using the payment channels and you're essentially getting a confirmation that the message actually got to the recipient. While with this new extension, It's not using payment channels and it's just using other nodes and it doesn't require the same level of resources and that kind of stuff, but you're not getting the same level of confirmation. You're not as sure that the message made it to the recipient. Is that right?

Sjors Provoost: 00:27:04

Yeah, that's correct. However, if you want to reply, and you probably want to, if you're asking for an invoice - because you want the invoice - then in your message should be instructions on how to send a message back. So basically you just provide another bunch of onions that can be unpeeled on the way back. So the person you're talking to does not have to know where the message is coming from.

Aaron Van Wirdum: 00:27:29

Yeah, basically the confirmation that the message ended up with the recipient is the fact that you got an invoice back, right?

Sjors Provoost: 00:27:36

That's right. Yeah.

Aaron Van Wirdum: 00:27:38

Right. So, does that cover the proposed extension to Bolt 7?

Sjors Provoost: 00:27:45

I think so. I mean, I'm sure there's all sorts of subtle things that I don't know and we haven't covered, but I think this is the essence.

Aaron Van Wirdum: 00:27:52

If we got the basics, I'm happy. So to reiterate, Sjors, do you want to reiterate? I'm going to reiterate and then you can correct me if I'm wrong. There's a new proposed Bolt 12. It's actually implemented in C Lightning already, I think.

Sjors Provoost: 00:28:13

It's experimental, but yeah.

Aaron Van Wirdum: 00:28:15

But that's the only implementation that has, the only Lightning implementation that has actually included it so far, right? It's not available for mobile wallets or anything like that yet.

Sjors Provoost: 00:28:25

No. 

Aaron Van Wirdum: 00:28:26

Right. This Bolt 12 is an additional communication, a meta invoice is how you described it previously, that tells Lightning Nodes which Lightning Node to connect with or to ask for information about an invoice. This allows for more flexibility on the invoices itself.

Sjors Provoost: 00:28:50

That's right. Or in the case of sending a payment, the Bolt 12 meta invoice basically says who to send the invoice to. So in the case of the Bitcoin ATM, the Bolt 12 thing will tell you, okay, this is the ATM node, please send an invoice to this node and we'll pay it.

Aaron Van Wirdum: 00:29:16

Yeah, and the main problems it solves is it takes care of the fiat volatility. So you can create meta invoices ahead of the time of payment. It takes care of the secret so you can use the same meta invoice for all my apples. And like you said, you can use a meta invoice to determine who's actually paying who. This is all done using a new extension to the Bolt 7 messaging protocol that works on a best effort basis. Is that it? Did I just summarize it?

Sjors Provoost: 00:29:54

I think so. Great.

Aaron Van Wirdum: 00:29:57

Shors, I think we're done then. We did it. We made another episode.

Sjors Provoost: 00:30:02

I think so too, let's hope the recording worked. Thank you for listening to the Van Wirdum Sjorsnado.

Aaron Van Wirdum: 00:30:07

There you go.
