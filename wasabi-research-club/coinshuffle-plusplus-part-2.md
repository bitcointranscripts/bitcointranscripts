---
title: Coinshuffle++ (Part 2)
transcript_by: kouloumos via tstbtc v1.0.0 --needs-review
media: https://www.youtube.com/watch?v=bCZFAqB3bnU
tags:
  - research
  - coinjoin
  - privacy-enhancements
  - cryptography
speakers:
  - Tim Ruffing
date: 2020-02-11
summary: In today's episode Tim Ruffing explores the concept of disruption in the Coinshuffle++ protocol and how it can be detected. He explains that the protocol passively observes messages and their outcomes, without knowing which message belongs to each participant. The speaker also discusses the practicality of blocking someone from the protocol, mentioning the role of network setting and the potential power of an attacker. Additionally, Ruffing highlights the importance of multiple communication rounds, protocols for key exchange, and the need for peers to verify if the protocol has been disrupted. Further Tim explains the concept of introducing another broadcast round in Coinshuffle++ to avoid disruption. By replacing one broadcast with another, the protocol ensures that if one message is disrupted, all messages are disrupted. This eliminates the need for a broadcast round to check for disruption, as participants can simply look at the list of messages and determine if their own message is there or not. This approach provides a guarantee of message integrity without additional broadcasts. Ruffing also addresses the limitations of Coinshuffle++, such as the lack of privacy in transactions with unequal inputs and the inability to pay while mixing. He discusses potential solutions for the anonymity of payments and emphasizes the benefits of Coinshuffle++ for coin shuffling. The timing and trust aspects of the protocol are also discussed, with a mention of potential delays and the need to trust other peers. Overall, Coinshuffle++ offers improvements in message integrity and coin mixing, but there is room for further development in addressing certain limitations and ensuring robust anonymity.
aliases:
  - /wasabi/research-club/coinshuffle-plusplus-part-2/
---
Speaker 0: 00:00:00

Yeah.
All

Speaker 1: 00:00:02

right, guys, we're here with Tim Ruffing, one of the authors of the Coinshuffle++ paper to talk about privacy.
So this PowerPoint and the presentation, Tim will do that himself and I'll just sit back.

Speaker 0: 00:00:22

Yeah, hey.
I'm sorry if this will look weird now, but I had to send my slides to Arif to share the screen, so I can't click through the slides he needs to do it, so It could be a little bit weird.
Maybe just pop up a few things on the slide, please.
Maybe maybe like actually the entire slide until we are the next thing.

## How Bitcoin transactions work.

Speaker 0: 00:01:00

Yeah, so this is, you all know how Bitcoin works, but this is just to show you a little bit how I throw things here.
So we have a transaction right and Alice on the left and she has a key and you have maybe some pizza dealer on the right and and again Alice's change address which is address C here and then this transaction is valid if A signs it and this checkmark thing is basically the signature very well and then we send it to the Bitcoin network and the transaction is validated and so on.
So I think this is all the things that we need here.

## Main privacy issues.

Speaker 0: 00:01:39

And also here, I mean I included those slides because I had them anyway, but I don't need to tell you that privacy is important, right?
And that we have a lot of privacy issues, for example, the amounts are public just by looking at the blockchain.
And yeah, even worse, you can link addresses to each other just by looking at the links on the blockchain.
So maybe go to the next thing.
Yeah, there are a lot of links here and you can link addresses here.
You know that stuff.

## Transaction graph analysis.

Speaker 0: 00:02:23

Then you can continue with larger tools and you'll know that stuff.
And it's huge.
And now we have even companies that do that stuff.
That de-anonymize you for profit actually.

## Big picture of privacy technologies.

Speaker 0: 00:02:45

So, improving privacy.
And here I have some picture with some privacy technologies.
This is just to show you where where CoinShuffle stands in this big picture.
In this big picture.
So, yeah, so actually I could basically put CoinJoin instead here probably and it would still be a valid picture.
The basic idea here is that with CoinJoin or CoinShuffle or CoinMixing in general, also TumbleBit is in the same category, we can't do so much in terms of privacy, but we are pretty compatible with Bitcoin because it works currently in Bitcoin.
Of course, if you want more privacy, you can have fancy zero-knowledge proofs and other technologies like zero-cash or whatever.
But this will never be integrated in Bitcoin, I guess.
And then there's something in the middle, maybe, that I can briefly mention in the end here, which is value shuffle.
If you can have amount of privacy in Bitcoin by adding something like confidential transactions, then mixing suddenly gets better and you can have better privacy even with mixing.
This will be very useful.

## Coin mixing.

Speaker 0: 00:04:19

Okay, this is a coin join seminar.
So again, we can quickly go over the slide because I don't need to explain you how mixing works.
We do it via a multi-input, multi-output transaction that you all know as a coin join.
Now the interesting thing here is, if you want to do this transaction, here Alice, Bob and Carol need to come up with a new list of, with a fresh list of output addresses, C prime, A prime, B prime, in a way that should, nobody can tell which of these new addresses belongs to which user.
And the way we're going to do this is a peer-to-peer mixing protocol.
And in this talk, our peer-to-peer mixing protocol is CoinShop++.

## Peer-to-peer mixing.

Speaker 0: 00:05:15

So, what's peer-to-peer mixing?
If you look at it as a primitive, it's a protocol where you have a number of participants.
In this example, we have four participants.
They all have an input message.
Here the input messages are A' B' C' D' and like in our coin mixing example, this would be the output addresses that appear on the right-hand side of the coinjoin transaction.
And now what peer-to-peer mixing gives you is output is the thing on the right side.
It's basically a shuffled list of those input messages, such that no one can tell which message belongs to which user.
But the messages will all be public.
Next.

## P2P trust model. / Anonymity Set in the presence of adversaries.

Speaker 0: 00:06:16

Right, and the trust model we want to have here is really a peer-to-peer trust model, which means that there are no, there's no mutual trust, so the peers don't trust each other, it is a random strangers on the internet, or it should be the case for CoinJoin and there are no third-party routers.
What I mean by that is we don't rely on anything like Tor to provide anonymity.
So in this example here now, look at the left-hand side.
Alice and Dave could be malicious and this means for anonymity that the anonymity set remains the set of honest users.
So Bob and Carol still have an anonymity among each other.
Of course now they only have an anonymity set of two because they can't have anonymity together with the attacker, right?
Just not possible.
Next.
Because exactly, we have those links here.
So if the attacker controls Alice, then the attacker knows that a prime is Alice's address and the attacker controls Dave, then he knows that d prime is Dave's address.
So yeah, we can't provide anonymity with those two addresses.
But as I said, like Bob and Carol still get an anonymity set of two in this example.

## Termination in the presence of malicious users.

Speaker 0: 00:07:44

Another property that we want to have next to anonymity is termination.
This simply means the protocol terminates in the presence of malicious users, which means that there shouldn't be users that can stop honest users from finishing the protocol.
The only thing we assume here is what I mentioned last week in the informal discussion about Crunchyroll++ already.
For termination, we assume that there is a bonded board.
What do we mean by that?
It's basically a server in the middle where we all connect to, and the server handles the broadcast for us.
And because we are in this peer-to-peer trust model, we don't really trust the server for anonymity, but we trust it for termination.
In practice, this means that if the server is malicious or just broken, then the peers won't be able to finish the protocol, but nothing bad happens.
They could just switch to a different server.
However, no matter how malicious the server is, the server can't break anonymity.

## How does CoinShuffle++ work? / DC-net (Chaum, CRYPTO '88).

Speaker 0: 00:09:00

So how does CoinShark V++ actually work?
It's based on a DC-net, which basically stands for Dining Cryptographers Network.
And Dining Cryptographers network is a weird name for the following actually rather simple concept.
Say we have again three users now and Assume these three users have pairwise shared keys and the keys are the numbers on the triangle here.
So, for example, Alice has a shared key with Carol.
That's the number one, the red one key here.
And yeah, and every pair has a shared key of one bit.
And now Alice on the top, she also has a message.
The message is the bold thing.
She has a one bit message which is also one.
Now what Alice does is, Alice takes her message, the one, and adds up, this is the thing in the parentheses, the two keys shared with the other parties, the blue key and the red key.
And we get one plus one plus one, And if we work in the bit field or basically you can think of XOR instead of plus, then the result here is just a one.
And then Alice will broadcast this one.
And Now Bob and Carol do the same.
Also Bob has a message which is a zero here.
Bob adds the two other keys and broadcasts the result and Carol does the same.
And now, the cool thing now is if we add those three messages up that have been broadcast, which is 1 plus 1 plus 0, then this basically means that we have...
Yeah, so if I expand it, we have just this result and now we see that every key has been added twice, which is kind of clear because it has been added by both sides of the of every of those connections basically.
So that means that all the keys here cancel out And we are left with the sum of the messages here, which is one plus one plus zero.
Yes, and the last zero should be bold.
So If we add those together, we get zero.
And zero is indeed the sum of the messages that the users had in mind.

## DC-nets in practice.

Speaker 0: 00:12:08

So the interesting thing here is now that this gives the users some form of anonymity in this very simple setting.
So, now we know what the sum of the input messages is, but we don't know who contributed what part to this sum.
This is a form of anonymity, basically.
This was kind of a very simple and awkward example because in practice, we don't want to, Okay, I should follow the slides.
In practice, first of all, if you want to do this in practice, we need to obtain shared symmetric keys.
This is not hard because we can just do a cryptographic key exchange.
This is kind of standard.
We can do the Fahami key exchange, for example.
But functionality-wise, What we want to do in practice is we don't want to send just one bit message, we want to send longer messages, for example, with common choices.
This is also not too hard to do.
Now I've shown you an example with the bit field, which is the field which is 0 and 1 basically as a mathematical field.
What we can also do if you want to send larger messages is encode them as larger integers and use larger finite fields to transmute them.
But most importantly, I think what we've seen in the example is that people compute the sum of their messages, but if you want to do peer-to-peer mixing, we don't want the sum of the messages of the people, but we want the entire set, right?
So We want a list of the messages, not a sum.
Now what a lot of these proposals and practice do, and I think you've looked into that two weeks ago in the seminar here, is try to use some slots reservation.
For example, in this picture here we would have three slots because we have three users and assume there is a magic way such that every user gets a slot in an anonymous way.
So Alice here, the first user, she has the middle slot, the second slot.
Bob has the first slot and Cavill has the third slot.
And now, for example, Bob will transmit his message in the first slot and two.
And now basically what we could do here is we could run a dcnet in every of those three slots and next.
Three slots and next.
And then Alice, yeah, so forgot to say that Alice in the slots where people don't have assignments, they just send zeros, right?
So if you look at the first slot, we add the zeros which are basically just some form of padding, I could say, and Bob's message.
Then we would have the messages.

## Slot assignment.

Speaker 0: 00:15:49

But the problem here is, we could have the messages back, but the problem here is that this needs this, what I call magic now, this needs an anonymous slot assignment.
So in order to make this work, we already need some protocol that provides anonymity in some sense.
And this is where most of these proposals to use slot reservation actually fail in practice, because it's a chicken and egg problem.
You need, in order to get an anonymity here, you need another anonymous sub-protocol that gives you a slot assignment.
And because this is hard, those protocols in the literature do the various tricks that mostly are not great because they can fail in practice.
So for example, what they often do is that you guess a slot randomly.
Say we have a thousand slots available and there are three users, and then every user guesses a random slot.
And this kind of works in practice, but it's pretty annoying because now instead of running 3 ADC nets, we need to run a thousand 3C nets.
So we need a lot more communication.
And Moreover, even like with a thousand, it could be that Alice and Bob both select the same slot and then, let's say they both select slot N, then in slot N we would have not m1 or m2, but we actually would have m1 plus m2.
And this is just not the result that we want.
So this is not great.

## Alphabetic ordering of public keys for slot assignment.

Speaker 0: 00:17:46

What we do instead is based on an idea that's pretty old already.
It appeared shortly after the CEMENTS and the idea is...

Speaker 2: 00:18:05

Before you go into, can I have a question?

Speaker 0: 00:18:07

Sure, yeah,

Speaker 2: 00:18:08

go ahead.
So why wouldn't a slot assignment work in, since everyone knows about everyone, why wouldn't the slot assignment just be decided based on alphabetical ordering of each other of everyone's public keys right

Speaker 1: 00:18:31

you because Because the whole point is we don't want to know who is who is

Speaker 0: 00:18:35

right So I mean functionally yes but like The problem is we we also like the peers here want anonymity even against each other, right?
So like if everybody in the shuffling knows that like if Alice knows that Bob has the first slot, then Bob can't get the anonymity because whatever message appears in the first slot it will be Bob's.

Speaker 2: 00:19:05

Yes, makes sense.
Thank you.

## Why are finite fields needed?

Speaker 1: 00:19:07

Can I ask one question?
Why are finite fields needed?
If you can do a DC net for one bit, can't you do it for 10 bits or any arbitrary number of bits?
Just have shared keys that are M bits long and-

Speaker 0: 00:19:25

Just by, you mean just by using XOR instead of finite fields?

Speaker 1: 00:19:30

That's right.

Speaker 0: 00:19:36

In general, you can do this with these DNETs and this is what people usually do.
The reason why you need finite fields is exactly on the slide I'm talking about now.
So this will be clear in a minute, I hope.

## Slot reservation. / Multiple messages (BB, EC'89).

Speaker 0: 00:19:57

So what we do instead of this slot reservation thing is actually it's abusing a method that has been proposed to the slot reservation but we have been using it to send the messages directly So what we do is we have something we could call slots.
It's not really slots, something like slots.
But yeah, maybe it's easiest to think of n slots here.
We have n users and we have n slots.
But instead of sending the message in only in one slot and sending zeros and all the other things Does here instead is she takes her message and one Sends it in the first slot And now she she will send m1 squared in the second slot.
She will send m1 to the three in the third slot and so on up to M1 to the end.

## Why doesn't Alice lose anonymity on broadcast of m_1 in slot 1?

Speaker 1: 00:21:03

Tim, could you explain why she doesn't lose anonymity when she, in the first slot, when she broadcasts M1?

Speaker 0: 00:21:14

Because, maybe click next?
Because everybody will do the same.
So also Bob will send M2 in the first slot and M2 square in the second slot and so on.
So everybody sends the same in the same slot.
Does this make sense?

Speaker 1: 00:21:37

So if Bob hears M1 and M3, can't he know that M1 comes from user 1 and M3 comes from user 3?

Speaker 0: 00:21:51

Ah, yeah I think the thing that you're missing here is that we are still doing a DC net in all of those slots.
So we still have the shared keys in here.
They're not in this picture, because here on the slide, I wrote just what the, basically what the input messages to the DCnet will be in every slot.
But just as the example we've seen in the beginning with just single bits, in every of those slots we run a DCnet with the shared keys added.
So Alice will not, in the first slot, not simply broadcast M1, but she will send M1 plus shared key with Bob, plus shared key with Carol, and so on, plus shed key with user N.
So only after we have obtained all the rows in the first slot in the first column here, these keys will cancel out.
So just by looking at Alice's broadcast on the network, you can't tell that M1 is in there.
Does this make sense?

Speaker 1: 00:23:21

Yes, so sorry follow-up question.
So doesn't M1 interfere with M2 when they're canceling out?

Speaker 0: 00:23:28

Yes, yes and I will come to that now.
Maybe click next.

## Sum of messages over finite-fields. / Power sums.

Speaker 0: 00:23:41

Yes, so you said m1 will interfere with m2 here and that's kind of true.
What we will have if we have all those messages in the...
Maybe let's look at the first slot.
If you have all the broadcasts in the first slot, all the keys will cancel out.
This is still true, but still like everybody basically send this first slot.
So we won't get a single message there, but what we will get is the sum of all those messages.
And in the second slot, in the second column, we will get the sum of the squares and so on up to the last slot.
Does this make sense so far?

Speaker 1: 00:24:31

When we're doing sums, are we doing sums over a finite field or XOR sums?

Speaker 0: 00:24:37

Yes, we're doing sums over finite fields.
I think this is...
Thanks for reminding me.
I think this is now the...
Not yet, but like...
Yeah, we maybe click next.
Sorry.
Now, not yet, but like, yeah, maybe click next.
Sorry.

Speaker 2: 00:25:03

I'm very curious what you do with those sums.

Speaker 0: 00:25:08

Yes, and sorry, I don't have slides for exactly the thing.
But, well, now I don't see the slides anymore.
I have to click.
So, okay, now we have those power sums.
And now I think we could go into that in detail, maybe later, if you're really interested.
And I don't have slides for this, but I really think it's not super important.
The thing is here is that if you have this list of the sums here, of those power sums, Then you can compute the messages again.
And just in information, theoretically, this, I mean, this is not a proper explanation, but at least if you look at the number of bits here, that makes sense, right?
We have n messages altogether because we have n users.
And let's say every message has b bits.
So, if you have the list of the power sums here, we have n times p bits and n times p bits is is the same amount of information and because we used to use a proper encoding like this or some thing is just one encoding of a list of messages you can decode it back and get the messages back but for this to work we need finite field arithmetic and that's why we do sums and finite fields instead of just XOR.
This wouldn't work if you used XOR.

## Disruption.

Speaker 0: 00:27:15

And okay, now the problem in the big problem in DCNets is that they can be disrupted, which basically means if there's one malicious user, let's say your Bob is malicious, what Bob could do is instead of sending m2 and m2 squared and so on and following this nice algebraic structure that you're supposed to follow, Bob could just send bullshit in every slot, for example, like random values or anything else that he wants, right?
And now the problem is if we now want to sum up in the slots, of course we can sum up, we get some sums, but like those sums will be again bullshit.
And yeah, even worse, because we are doing like n DCNets here, or a DCNet in every of the n slots.
Bob here says fully anonymous, right?
Because this was the core property of the DCnet that we can compute the sum of the messages and we can do this here in every slot, but we don't know who contributed what part to that sum.
So we can't tell who contributed bullshit.
We just see in the end that, okay, we don't get any messages back, like our decoding procedure doesn't work.
But then we don't know what to do.
So What do we do then?
Well, in case of disruption, break anonymity.

## Why Coinshuffle++ works. / Flowchart of CoinShuffle

Speaker 0: 00:29:07

And, well, this may sound like a bad idea, but let me explain why this actually works.
And to understand why this makes sense, we need to have a look at the flowchart of the coin shuffle run.
So the first thing we do, like everybody generates the fresh Bitcoin interest, this is gonna be the output in the coin transaction on the right side and it will be our message in the peer-to-peer mixing protocol.
Then, peers do key exchanges.
They run the VHelm and key exchanger.
I don't need to explain you how it works.
Just it makes sure that every pair of users will have a shared key that they need for the DCnet.
Okay, then we run the actual DC net and then we would run it in slots as I've just shown you.
And then now If we would proceed like I've shown you on the previous slide, and actually this is not the real, this will not be the final flowchart of CronShuffle++, We will come to that later, but bear with me for the moment.
If we would do what we've seen on the last slide, we need to somehow, we need to check if our run has been disrupted.
The problem is, namely, that it could be that the run is disrupted for, Well, how should I say this in the best way?
And so, if you get the output, the only thing you can do now is to see if your own message is there, right?
Like If you're Alice, you get those power sums in the end, or if you hope that they are power sums, you try to decode the list of messages, and then you have a candidate result for the protocol.
The only thing you can do now is you can look at if your own message is there, which basically means that no one disrupted your message.

## Validating Bitcoin addresses instead of messages.

Speaker 2: 00:31:54

Can you, instead of looking at your message, although it doesn't matter, that's good, But instead of looking at your message, can you just check if these are Bitcoin addresses or bullshit?

Speaker 0: 00:32:13

You mean You could have some redundancy in there.

Speaker 2: 00:32:20

Yeah, but it doesn't matter because checking if your message is there is just as easy as anything else.
Yeah.

Speaker 0: 00:32:29

Let me think about this for a moment.

Speaker 2: 00:32:37

The question if bullshit can be constructed in a way that still valid Bitcoin addresses.

Speaker 0: 00:32:47

Yes, yeah this is the problem so I can't, I don't have this on the slides, but what could happen is that, like in the example Bob was the malicious guy, right?
So let's say Bob sends his messages last.
Then basically Bob sees all the other messages.
Bob sees all the other rows in a sense.
And he sees all the other messages.
He sees the list of all the other messages that the others want to send.
And then he could, it's not clear from the slide here but then you could construct a special form of bullshit message in a sense that only disrupts for example Alice's message and not the other messages.
Okay.

Speaker 2: 00:33:56

No, not okay, because then everyone would be able to check if Alice's message is a Bitcoin address, valid Bitcoin address or not.

Speaker 0: 00:34:08

No, no, okay.
So, what Bob sees is, Bob sees just a list of the other messages.
He doesn't know which message belongs to which user.
So he sees somehow that M1 is there, which is Alice's message, but he doesn't know that it belongs to Alice.
But now, because he knows M1, he could send bullshit such that m1 is disrupted, is basically replaced by a random message or a message of his choice even and the other messages are not.

Speaker 2: 00:34:40

Yes,

Speaker 0: 00:34:41

okay.
So, he could selectively disrupt messages even though he doesn't know to which users those messages belong.

Speaker 2: 00:34:53

Makes sense.
Thank you.
So he could swap Alice's address.
Right.
Swap a random address to his own address and

Speaker 0: 00:35:02

for example, yeah, yeah, and That's why We we would need so Love Okay What I was saying before is that the only thing Alice now at the end of the DZNet round, what she can do is she can look at the set of messages of the results of the protocol and see if her old message is there, right?
But she doesn't know if the other messages are all there.
She will see some messages there, but she doesn't know if, for example, if Kevil's message has been replaced or not.
And the important thing at this step here is that, however, we all, like all the peers in the protocol need to agree whether disruption has happened or not because if it has not if there was no disruption then like this is the case we see now on the slides and then they will go ahead and create a contract transaction and hopefully sign it.
However, if one of them, like if one was disrupted, then what they want to do is They want to reveal the key exchange sequence, which is basically a standard de-anonymization step.
Basically, it means that we all agree, like all the peers in the protocol agree that we give up this round, we give up anonymity in this round.
And we discard the addresses that we generated at the beginning.
We need to give me a moment to convince you that this is not a bad idea.
Why can we discard those?
Well, I mean, these are just, so far these are just random Bitcoin addresses, right?
We have never told anybody to send us money there and we will never do it again in the future.
So it's not a problem at all to throw those away.
But now because given the key exchange secrets, everybody can compute the shared keys for everybody.
Which means that Alice now knows the shared keys that Bob has, not only with her, she knew that one before because it's a shared key.
But now she knows also the shared key that Bob had with Carol, that Bob had with Dave and so on.
So now basically everything is public in this run.
So everybody can just look at everybody's messages and then all the honest guys will now figure out that what Bob sent didn't make sense, it didn't fit this algebraic structure.
Basically, they look at Bob's broadcasts in his second row, in a sense, and subtract all the shared keys that he had with the other peers, which are public now.
And then they look at the result and see, the result should be in the first slot M2, in the second slot M2 square and so on.
And they just can check now if Bob's messages follow this algebraic structure.
And yeah, they figure out that Bob's messages don't follow the structure so they know Bob was actually malicious they can kick him out and start from scratch this is make sense so far?
Yes, it's clear for me.

Speaker 1: 00:38:56

And then if no one signs a particular transaction, that's pretty trivial to find who is the missing signature.

Speaker 0: 00:39:03

Right, right.
Exactly, that's the case now.
Next, maybe.
Then, okay, yeah, if everybody decides, okay, great, success.
But if not, we can again, or maybe actually that arrow could be wrong here.
And in that case, we don't need to discard the addresses.
Now we better do okay, we better do.
But the important thing is here like yeah if if somebody refuses to sign here Then we know that this guy is malicious or at least offline and we can exclude him.
However, this is not okay, this is trivial to implement them, but we actually need to be careful for this case as well, because the protocol somehow needs to make sure that if we reach that point where we think that there was no disruption, then there was really no disruption.
To make sure that we are excluding the right guy here.
But the protocol actually has this property.
So it can't be the case that everybody thinks that there was no disruption, but actually Alice's message was disrupted.
So she will naturally refuse to sign because she would lose money by sending it to a wrong address on the coin drive.
But everybody else will think that she actually needs to sign the transaction.
The protocol also makes sure that this contact.
Yeah.
Okay, and this is the basic idea how we provide anonymity and termination at the same time by basically cleverly giving up anonymity in case that the protocol is disrupted.
Then we can, because then we gave up anonymity for the single run, we can figure out who was malicious and then we can kick him out.

## "Fresh" vs. "Fixed" input messages.

Speaker 0: 00:41:30

Side topic, are fresh messages needed?
So what I told you now is basically the entire idea of the protocol is this.
Why this works with giving up anonymity is because we have those kind of fresh Bitcoin keys, right?
We can throw them away and nothing bad happens, not for our money and not for our anonymity.
Well, then everybody knows that I wanted to use this address, but I never used it in fact.
So I can give up anonymity for this one and this works because we can generate addresses and we can discard them generate new ones and so on but what if we want to send messages that are kind of fixed that are not random Bitcoin addresses and maybe use this protocol beyond Bitcoin, for example, to leak confidential documents.
Like such a confidential document as on the slide here, I would call this a fixed message.
And it turns out that this is not possible.

## Features of P2P mixing protocols.

Speaker 0: 00:42:41

So if we look at features of peer-to-peer mixing protocols, I've already told you they should provide anonymity, they should provide termination.
And now if we add support for fixed messages as a third property, and CurrentJava++ provides anonymity and termination, great.
So if we add support for fixed messages, support for fixed messages.
Next.
Then we can ask is there a protocol in the intersection of all these circuits in the middle and

## Define termination.

Speaker 2: 00:43:20

what the termination mean

Speaker 0: 00:43:26

termination means that the protocol terminates, even if there are malicious peers inside.

Speaker 2: 00:43:34

So not termination would mean if there are malicious peers then the protocol just doesn't.

Speaker 0: 00:43:46

It doesn't finish.
So, or it aborts.

Speaker 1: 00:43:53

Yeah, in the

Speaker 2: 00:43:53

example of Wasabi.
Termination is.
It doesn't finish.

Speaker 0: 00:43:55

Or it aborts.

Speaker 2: 00:43:55

So it's like termination is...

Speaker 0: 00:43:59

Maybe it should have been called successful termination, right?
So you can imagine that a protocol that doesn't provide termination basically, for example, it tries to start mixing with the DCnet and then it notices, oh, there was disruption and then, well, it fails, just aborts.

Speaker 2: 00:44:21

Okay, so if it aborts, if it notices that there was disruption, then that would mean termination is not ensured.

Speaker 0: 00:44:31

Right, okay.

## Wasabi does not guarantee termination.

Speaker 1: 00:44:35

Yeah, so I think Adam, like currently Wasabi does not guarantee termination, right?
Because if a coin join doesn't happen, wasabi bans a coin and then reopens the round and more malicious people could enter the round.
But one way to make it guaranteed to terminate is to only allow the same participants and then exclude them so that it converges to a smaller and smaller number.

Speaker 0: 00:45:08

I see.

Speaker 2: 00:45:10

Isn't determination is to basically being able to identify the malicious party?

Speaker 1: 00:45:17

No, no.
In this case I'm saying specifically given F malicious peers, can you tell me when Wasabi will do a coin join?
And in the case of CoinShuffle++ the answer is 4 plus 2 F rounds.
And in the case of Wasabi, it's just when we've banned enough people and there are no more malicious peers and we don't know when that will be.

Speaker 0: 00:45:44

So There's half a pound of the number of UTXOs in the chain.
But it's pretty large.

Speaker 2: 00:45:55

So but wait, let's go back to termination.
You just said that if the round aborts, then that means that it aborts in a way that you cannot figure out who was the malicious one.

Speaker 1: 00:46:17

I think termination in this case means that it's successful, that eventually there's a coin join.

Speaker 0: 00:46:24

Yeah, I think, Adam, what you're mixing up here is when I say anonymity and termination here, in particular termination, I look at the entire protocol.
So like the entire protocol provides termination and it does so by like the inner working is that it tries to run once and if it sees that this run doesn't work then it restarts.

Speaker 2: 00:46:59

Okay, so that's...

Speaker 0: 00:47:01

But like when I say termination I look at the like the entire protocol in the black box as a black box.
It doesn't matter what it does internally.

## Is identifying the malicious peer a requirement for termination. / Dissent (CCS'10).

Speaker 2: 00:47:11

Yeah, sorry for hanging on it, but I think it's important.
So does that mean it could still be possible to provide anonymity with fixed messages if successful termination of the entire protocol is not a requirement?
But what is the requirement is actually to being able to identify the malicious peer.

Speaker 0: 00:47:43

So Maybe let's finish the slide and come back to this question.
Maybe it's answered, then maybe not.
So what could be interesting is to have a protocol in the middle that has all those three properties, But it turns out that this is not possible.
Interestingly, there was a protocol called descent at CCS10 That was supposed to be in the middle and has all the properties, but it turns out it doesn't provide an anonymity.
If you would code it exactly like it's written in the paper, it would provide termination and fixed messages and lose anonymity.
Does this answer your question or not?

Speaker 2: 00:48:45

No, no, my point was that if you can identify the malicious peer, then it doesn't really matter if termination happens or not of this protocol rounds because you could...
Yeah, but...

Speaker 0: 00:49:04

Okay, sorry, go ahead.

Speaker 2: 00:49:09

That was pretty much it.

Speaker 0: 00:49:11

Okay, again, when I say termination, I don't talk about...
I don't mean termination of a protocol run, of a run that can be aborted.
I mean termination of the entire thing, like the entire thing with a big loop.

Speaker 2: 00:49:33

So, okay.
So, if you can identify the malicious peer, but you don't exclude it, but create, but you have to create a completely new protocol and from that you exclude it that would mean that it is a terminating protocol.
Okay fine, let's

Speaker 0: 00:50:00

go.
Okay.

## CoinShuffle++ is a circular protocol.

Speaker 1: 00:50:04

Just to clarify, Coinshuffle++ is a circular protocol.
It has four, it has six rounds, six steps, and then four of them are repeated every time someone disrupts, right?

Speaker 0: 00:50:19

Yes.
Yes.
And that's why I look at the entire thing, like with the circular thing in It provides termination.
I think this is all I wanted to say here.

## Anonymity attack on Dissent Protocol.

Speaker 0: 00:50:39

I can actually show you how this anonymity attack on this end works.
I don't need to tell you a lot about this end but I think it can still be instructive.
The only thing I think you need to know is that like the three points on top here, this end proceeds in broadcast rounds and The outcome of the protocol is revealed to all the users in the last broadcast and also a network attacker sees the outcome of the protocol in the last broadcast.
An outcome is to remind you what is the output over, what is the outcome over P2P mixing protocols, just a list of shuffled messages.
Now let's say we have Alice, Bob and Carol, and they all have their fixed messages, their documents, and Bob is the honest guy here, and we are the network attacker.
Now, what we do is, We just let the users run the protocol.
We listen to the messages as a network attacker and we only interfere with it in the last broadcast of the first run, basically.
So what we do is we block Bob's message.
Because we're a network attacker, we can do this.
But we still see his message.
If we see it, we just don't forward it to the others.
Which means that we as a network attacker, we learn the list of messages that people wanted to send.
These are the three documents here on the right hand side.
This is the right hand side here and on the slide is the view of the attacker.
So here we see what's going on.
We see the list of messages, but we don't know yet which message belongs to which user.
But okay, now we brought Bob.
So now what happens is, because we blocked Bob's last messages and the protocol is supposed to provide termination.
The other remaining parties like Alice and Carol, they need to somehow start from scratch, right?
And they do a second run of the protocol.
And now because Bob is not in the protocol anymore, they kicked him out because he appeared to be malicious to the other two parties.
Bob's message won't be there in the second run.
So now what the attacker can do is he just looks at the outcome of the first run and the second run and compares them and he will just notice that the missing protocol, the missing message is the one, the gray one with a confidential mark on it.
Because he knows that he blocked Bob, he knows that this is the message from Bob.
Does this make sense?

Speaker 2: 00:54:03

Probably.
Okay, feel free to ask.
Sorry I was just blanking out.
It wasn't really a good explanation.

Speaker 1: 00:54:14

Okay.
So, I guess I just don't understand how descent works well enough, like why there would be multiple rounds.
But isn't it the case that Bob's message is XORed with the two adjacent Diffie-Hellman shared secrets?
So How is it that you can figure out Bob's message?

Speaker 0: 00:54:43

Okay, I think there are multiple things here.
So, yes, I didn't explain to you how this works.
It works differently from a DCnet.
So basically, it's a little bit like or it's pretty similar to the contra of the one that you also discussed.
But my point here is that it doesn't really matter, right?
So the attack that I show here would equally be true if we would try to run, if we would try to use fixed messages in CoinShuffle itself.
And this would be exactly the same issue.
So it doesn't depend on really how the protocol looks like.
But in the end of the protocol, at some point you need to reveal the messages, right?
So what the attacker here does is in the first run, like he just looks at the protocol passively until the last round.
So basically he observes all the messages of all the people and then she just he just sees the outcome of the protocol which is the list of messages and so far there's nothing wrong with it because he doesn't learn which message belongs to the chooser

## How practical is it to block an adversary from the protocol.

Speaker 1: 00:56:14

this might be a dumb question but how practical is it to block someone from the protocol, mid protocol?

Speaker 0: 00:56:23

I think this really depends on the network setting.
Like usually if you write protocols, you want them to be secure against network attackers and we actually assume that network attackers can do much more.
They can not only block messages, they can also replace them, duplicate them and all the stuff.
Of course you can ask how realistic that in practice is.
Usually we abstract away from this question, just say like look the attacker is super powerful because we don't know how powerful he actually is.
Now, if you look at coin shuffle or descent specifically, I told you in the beginning that we assume that we have this bulletin board in the middle that handles all broadcasts.
And the reason why we do this actually is to have better efficiency.
And Now it's getting interesting.
So because we didn't want to trust this bulletin board in the middle of the server in the middle for anonymity.
But if you think of the server in the middle being the malicious network attacker, Then suddenly it's very, very easy to block messages, right?
You just don't forward them.
Like think of, I think last week I mentioned the simple example of my RST server, just as an example of a server that broadcasts your messages to everybody else.
So basically in this setting, if you have the server, you can always claim more.
Look, I didn't.
Bob didn't send the message.
He's offline.
So in this setting it's super realistic to do this attack.
If you're the server in the middle.
Yeah, okay.
Efficiency and...
There we go, next.

## Broadcast rounds.

Speaker 0: 00:58:38

Okay, now this is the flowchart again that we've seen And now the title of the slide says naïve.
Why naïve?
Because this is actually not the truth.
Here I need to re-explain something that I think I started this explanation on one of the previous slides.
And actually, because I was confused on the slides, which slide we are.
Okay, let's count communication rounds.
And communication rounds are here, broadcasts.
So we need one broadcast for the key exchange.
This is the symbol here.
Then we need one broadcast to run the actual DCNets.

Speaker 1: 00:59:32

And now,

Speaker 0: 00:59:36

because now is the crucial part, because we all need to, like all the peers now need to agree on whether the protocol has been disrupted or not.
I told you this example where you can selectively disrupt messages from peers.
So to avoid this, in a naive way, we would need another broadcast here just to check that we all agree on whether there was disruption or not because as I explained to you earlier the only thing you can do is you can look at this on the output of the protocol and see if his own message is there but he doesn't know if the messages of the others are there.
So to make sure that we all agree whether there was disruption or not, we would need another broadcast from here.
And this is the broadcast that basically belongs to the disruption box.
And then once we all know whether there has been disruption or not, we need one more broadcast either to broadcast the signatures on the contract transaction or to reveal the key exchange secrets depending on which way we go now.
Okay now in Coinshovel++, so sorry can you go back one step?
Yes.
So, if you look at this now, if you count the broadcasts, these are basically four broadcasts in every run, right?
No matter which way we go.
Now what we do instead in CoinShop++ is we want to avoid this broadcast at the disrupted box here.
And how do we do that?
Next, by introducing another broadcast here.
So, So far, this doesn't make a lot of sense, right?
Because we still have four broadcasts per run.
We replace one broadcast by another broadcast.
But let me explain to you why this makes sense.
Next.
Ah, okay.
Let me first tell you what we actually do.
So what we do here is like this first broadcast that we introduced now is basically a commitment, cryptographic commitment to the DCnet vector.
By vector I mean just the rows that the peers send in the DCnet.
So we first send the commitment, next.
And then we send the actual DCnet contents, the actual rows.
So Why do we do this?
The idea is, basic idea is that now we get this following relationship.
Now by doing this, we get the guarantee that if there is one honest user whose message is disrupted, then all of the messages are disrupted.
And the other way around.
This basically means that now, instead of needing a broadcast round, to check with the others if there has been disruption, what we now can do instead is really just looking at our own output.
So you look at the list of messages and see if your own message is there.
You know if your own message is there, then all the other messages are there.
And equally, you know if your own message is not there, then also the other messages are not there.
And the rest on the slide was just formal stuff, not interesting here.
So now let's look at an example.
Go back please.

## Example execution.

Speaker 0: 01:04:17

So if we would now have a protocol with runs, let's say we have a first run of the protocol and now every box is a broadcast.
So we have four broadcasts.
And remember that the DCnet round is now in the third position.
Because we first send the key exchange, then the second thing is we commit to the DCnet vectors, to the DCnet messages, Then we send the actual DCNET message, the third round.
This is what I mean when I write DC.
And then in the end, we either send the signatures around or we reveal the key exchange messages.
And now let's assume like okay this first run is disrupted.
Next.
And remember disruption happens in the DCNet round.
So somebody sent bullshit in the DCnet round, this round is disrupted, the run is disrupted, then we would start the second run and would need another four rounds if you go back again.
Sorry.
So, this is the naive thing.
And now, next, what we do in Conjava++ is we actually want to pipeline these runs and to reduce the number of overall rounds.
So now the idea is basically, we run two rounds of the first one, and then we already start a second run.
It's not clear yet if you will need it or not.
But in case the first run is disrupted, then we can just switch to the second run.
Which is the example here, right?
And then maybe the second run actually is not disrupted.
And okay, we have started already a third run just in case and then okay, but the second one works, it runs through so we can just support the third one.
This is how we pipeline this and Now look at this red line here.
This is how the information flow is basically from the first one to the second one.
Because the first one, remember the first one was disrupted, right?
So after the fourth message, after the last message in the first run, only then we learn who is the malicious party, because this is where we reveal the secrets.
And note now this, you can see this from the red line now, this is exactly the point in time that is still, so it's still okay to exclude the malicious guy now for the second run, because now the malicious guy that excluded the first run can't disrupt the second run, because we managed to exclude him from the second run before we reached the DC thing, before we reached the DC message phase.
Does this make sense?
Please ask if this is unclear.

Speaker 1: 01:07:42

Makes sense to me.

Speaker 0: 01:07:45

Great.
And this is the reason why we wanted to push the DCNET round to the third broadcast instead of the second.
So This was the thing I've shown you on the previous slides, right?
In the naive version, we run key exchange, then already the CNET, and then we need to check with the others if disruption happened.
Then the DCnet round would be in the, the DCnet message would be in the second round.
But here what we act, what we here do is to this commitments to the DCnet And then sending the DCnet only in the third round, we move the DCnet to the third round and we make this interleaving of two here possible.
Yeah, and now if you count the number of rounds, if you have F malicious users, then we need 4 plus 2 F broadcast rounds.
And this is better than previous work, which was the original cold travel, which was just all of NF rounds.
So much slower.

## Practical evaluation of CoinShuffle++.

Speaker 0: 01:09:04

Yeah, and now we can evaluate this and practice with the with the basically the setup that I mentioned here on the slide and compare this to the to the previous protocol coin shuffle And at least in this setting, Coinshuffle++ is much, much better than Coinshuffle, as you can see on the graph.
So Yeah, for example, for usually a number of you point out on the paper is 50 notes there.
We are still below 10 seconds in this setting.
And then coin shuffle, the original coin shuffle was like almost three minutes in the setting.
Next.
Yep, next.
Next.
Next.
Okay.

## Handling unequal inputs.

Speaker 0: 01:10:00

And then just, I think this is maybe should have been called limitations of coin zone actually for this audience here.
But you're probably aware that handling unequal inputs is a very naive form, is a very bad idea, right?
Because if you do a transaction like it's on the slide here, then everybody could just, every external observer even could just tell that Bob, like the one point, can you go back?
Sorry.
Yeah, so if everybody who looks at this transaction can just tell that B and B prime belong together, there's no privacy if you do a naive coin join with unequal inputs.
And we all know Adam has much better suggestions to do this.
But this is still an obvious limitation of coin drawings.
Okay and also this is more subtle what we what we also can't do in coin shuffle++ is the following.
So actually you don't want to mix your money, right?
You want to also to pay with your money.
So, I hope you could have the idea to do a payment.

Speaker 2: 01:11:36

You can or cannot do this?

Speaker 0: 01:11:39

You cannot.
And I will tell you why.
So Bob could have the nice idea to have a payment in the coin join here, like there's a pizza restaurant with address R and he sends 0.1 Bitcoin to the pizza restaurant and then he sends the remaining 0.9 Bitcoin back to E-Prime, which is his change address.
And now like if you're just an external server you you look at this transaction I mean of course you can you can see that 0.1 and 0.9 belong together But you couldn't tell whether they both belong to A, B or C.
However, the reason why it doesn't work is more subtle.
Now look at what would be the messages that we have to send to the peer-to-peer mixing protocol.
Like in the normal coin shuffle plus plus run, we would just send the output address, which is r and b prime here.
Now Bob would basically have two messages in the peer-to-peer mixing protocol, one for R and one for B'.
And now these messages are not just the symbol, the addresses, because he also needs to send the amounts there, right?
Because the amounts are not implicit anymore.
In the previous example where everybody has one Bitcoin, the amounts are not messages that need to be mixed.
But here they would need to be mixed.
So Bob basically sends two messages and one of the messages is the pair r, 0.1. And the reason why this doesn't work is now that the 0.1 is a fixed message.
It's nothing that you can discard and throw a new random one, right?
It just doesn't work.

Speaker 2: 01:14:02

Because does that matter?
What really matters is that the output address is changed.
So it's like the message is not not the zero point one.
The message is or zero point one.
If you next you message or to 0.1 because Robert gave you many addresses.

Speaker 0: 01:14:27

Yeah, but I think like I had this we had this side topic, right?
Is a fresh message is actually necessary?
Can we do mixed, sorry, can we do fixed messages?
And the reason why the answer was no, the reason was that anonymity is broken.
So functionally you're right, you can just like if the first run is disrupted you could abort it and then restart with R2 and 0.1. But then it could be that there is an attacker and anonymity.

Speaker 2: 01:15:13

I'm sorry, can you repeat that?
Repeat that?

## Mixing and paying simultaneously.

Speaker 0: 01:15:22

I had a few slides under the title, side topic are fresh messages necessary, right?
Where I showed the attack on this end, for example.

Speaker 2: 01:15:38

But the message is fresh.
It's just one component of the message is fixed.

Speaker 0: 01:15:44

Okay.
But the attack basically applies to also messages where one component is fixed.
You really lose anonymity in this setting.

Speaker 1: 01:16:00

Also how would you pay someone, like typically you only have one address?

Speaker 0: 01:16:08

Yeah, typically only can you repeat?

Speaker 1: 01:16:12

Typically you only get one address when you have to pay someone So you have to also...

Speaker 0: 01:16:17

Yeah, okay.
Yeah, this is what I like.
If I write a paper, I would call this an engineering challenge and put it aside.
Yes, of course, then you need to...
But you're right.
And so what I'm saying is you're right.
In practice, you need to solve the problem.
It's just that it's kind of doable, but you need recipient support and this would be another drawback, even if it would be possible.
Either, like if you do a coinjoin with 50 parties, then either you ask the pizza restaurant to give you 49 addresses, which is ugly but works.
And what you have something like PIP 32 and public derivation and so on, where like the restaurant would give you one master public key and you can just derive an arbitrary number of actual addresses from it.

Speaker 2: 01:17:21

So just to reiterate on the problem here is that when you expose your messages, then of course you don't expose the Bitcoin addresses, but what you expose is that you want to send 0.1 and 0.9 and then what you could do with that is that, well I guess this send failed because the peers were very malicious so I'm just going to send one Bitcoin in in the failing round but you know you could you could assume honesty and and if honesty yes then I mean it's not very robust but you can...

Speaker 0: 01:18:13

Yeah, no but I see what you're saying.
Let me repeat to make sure I get the right thing.
So what you're saying is basically you be optimistic, try to like the first run, try to do the payment.
And then, but if this first run fails, then go back to simple mixing without paying.

Speaker 2: 01:18:38

Yes.

Speaker 0: 01:18:40

Yeah, this, you're right, this principle would work.
It's a good question how robust this is in practice, but in principle you could do this.

Speaker 2: 01:18:54

All right, thank you.

Speaker 0: 01:18:56

Okay, and now this is the final word here on the slides, I think.
So, I hinted that this already, Like if we are in a system where we have confidential transactions, which is a cryptographic technique to hide the amounts on the transactions, like the amounts are not in plain, stored in plain, but are in homomorphic commitments and cryptographic commitments.
Then suddenly those amounts, because they are in commitments, These are not fixed messages anymore.
This can be re-randomized basically.
So you can take a commitment and like you can commit to the same amount twice and those commitments look totally independent of each other.
Then this problem with the fixed message goes away and then you suddenly can mix and pay simultaneously.
And also like an addendum protocol you need for this is value shuffle, which is full op fork.
And also you, of course, get rid of the previous problem that you can't mix unequal amounts, then you can also mix equal amounts and suddenly mixing is so much nicer and better.
If you could hide the amounts, but I think this is also not used in this seminar here.

Speaker 2: 01:20:32

I have one more theoretical and less practical talk that you know what does really termination mean here?
Termination means that everyone signs, but that's not really what termination is.
Termination is that successful broadcast happens.
So now there is the issue with double spends.

Speaker 0: 01:21:01

Yeah, right.

Speaker 2: 01:21:02

Yeah, so we detect the double spends and then we have to run the whole protocol again.
What if you are a miner then everyone has to be online until confirmation.

Speaker 1: 01:21:18

Sorry but isn't a double spend the same as not signing the CoinJoin at the end round?

Speaker 0: 01:21:25

The problem is just that you don't figure it out so quickly, right?
So and you don't know, right?
As I've shown you on the slides, basically, the protocol is finished as soon as you get the signatures on the coinjoin message, the content of the action from everybody else, then you have a signed coinjoin.
Then if naively then you think like the protocol is finished, I just need to broadcast the transaction to the network now and then it runs through.
But yeah, like in reality, people could double spend maybe a minute later or so.
Not sure how realistic a minute is.
If you're a miner, yes.

## Double-spend attack.

Speaker 2: 01:22:13

The smartest way to be double spend here would be that you divide the network, like one half of it knows about the correct transaction, the other half of it doesn't know about the correct transaction.
So The peers cannot really agree if the protocol was disrupted or not.

Speaker 0: 01:22:38

Have you seen this in Wasabi?
Has this happened?
I mean, I think it's a problem with every CoinJoin thing, right?

Speaker 2: 01:22:48

So, I mean, if I broadcast two transactions, like to six and six peers at the exact same time, then they are propagating on the network in a way that the manpool splits and then a miner has to come to decide which one was actually the real transaction.

Speaker 0: 01:23:16

Right, no, I mean my question was if you have seen this attack in Wasabi or somewhere else.

Speaker 2: 01:23:24

I did see double-spent Wasabi coin joins like maybe a year ago.
I could not figure out what was that.

Speaker 0: 01:23:36

Okay.
I always wondered how relevant that is in practice.
I mean, like if you, Of course you can do this attack, but it's really pointless for the attacker.
I don't know.
It's just super annoying.

Speaker 2: 01:23:59

Yeah, it's like, you know, other schemes those are working in practice don't even ensure denial of service protection right and this is like a new level of theoretical attacks.
So it's an engineering challenge, as you would put it.

Speaker 0: 01:24:23

Yeah, I mean, I would at least say it's not the end of the world.
But like, Even if people do this attack actively, what you can do is wait for another minute or so.
If you haven't seen a conflicting transaction for a minute, well, okay.
And actually, the peers can also then relay the transactions, right?
Like if one of the peers on the protocol sees a conflicting transaction, you could relay it to the others and basically have proof that there's a double-span.
Ah, okay, okay, yes.

Speaker 2: 01:25:05

My point would be, but you wouldn't see because the nodes don't broadcast to you, but yeah, you can relay to the others.

Speaker 0: 01:25:13

But it's kind of, from a running time perspective, kind of annoying.
Right now I told you, okay, like in a nice network setting, this protocol takes below 10 seconds, and then I tell you, no, you need to wait another 20 seconds just to make sure there's no double spam.

Speaker 2: 01:25:33

I mean if others relay a transaction like that, a conflicting transaction, then would that, I mean you would have to trust the other peers that they are not lying about the conflict in terms oh no because they can only the transaction those are theirs so they would be the the the the guys who are disrupting around so yeah never mind

Speaker 0: 01:26:01

I think like I think you could just assume that like if this transaction exists and it's signed that's already bad enough right

Speaker 1: 01:26:16

okay guys no one you stop the video in about five minutes.
Just a heads up.

Speaker 2: 01:26:22

Okay.
All right.

Speaker 0: 01:26:26

Yeah, it took long.

## CoinShuffle++ with arbitrary numbers of malicious users.

Speaker 1: 01:26:31

So maybe I'll ask a question if that's okay.
Tim, in the slide...

Speaker 0: 01:26:44

Yep.
Well, you can...
Usually you ask the speaker to go back to the slide, but you can go back to the slide.

Speaker 1: 01:26:55

So can you talk a bit more about how this would look like depending on how many malicious peers there are?

Speaker 0: 01:27:05

That's a good question.
So this basically assumes no malicious users, which basically means four rounds, right?
And you know, you know the protocol, protocol needs four plus two F rounds if you have F malicious users.
So you can already, like, you're just using this number, you could just scale the graph a little bit.
The problem is that this is not entirely the right answer because here when I say there are no malicious users, that also here means that they are all pretty responsive, right?
So this is a synchronous protocol, so At some point, I need to decide when somebody is offline.
I need some kind of timeout.
And now, in this setting here, basically, we don't need a timeout because we assume everybody is offline.
