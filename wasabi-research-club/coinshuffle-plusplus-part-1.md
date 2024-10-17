---
title: CoinShuffle++ (Part 1)
transcript_by: Musab1258 via review.btctranscripts.com
media: https://www.youtube.com/watch?v=srkY1mYI0IQ
date: '2020-02-04'
tags:
  - research
  - coinjoin
  - privacy-enhancements
  - cryptography
speakers:
  - Tim Ruffing
  - Adam Ficsor
  - Lucas Ontivero
  - Raphael
  - Max Hillebrand
summary: 'In today''s episode Tim Ruffing introduces the CoinShuffle++ protocol and explains its key components. He describes how the protocol uses power sums and polynomial roots to ensure secure messaging between participants. The protocol consists of four stages: Dimi Hellman key exchange, commitment, DC net, and confirmation. The protocol handles malicious peers by revealing secret keys and excluding them in the next round. Ruffing also highlights the scalability of the CoinShuffle++ protocol, as it can accommodate a large number of participants and complete the process in a relatively short time. The use of dice mix enhances the efficiency of the protocol compared to its predecessor, CoinShuffle. Futher Tim dives into the challenges of implementing CoinShuffle++, a decentralized protocol for coinjoining cryptocurrencies. He highlights the issues caused by varying internet connection speeds and round communication, leading to slower performance. Ruffing also discusses concerns about the negotiation process and cryptography affecting communication speed. Additionally, he acknowledges the complexity of the topic and expresses a desire to simplify it for wider understanding and implementation. Overall, Ruffing emphasizes the importance of maintaining privacy in peer-to-peer transactions and the potential of cryptography in various applications.'
aliases:
  - /wasabi/research-club/coinshuffle-plusplus-part-1/
---
## Intro

Max Hillebrand: 00:00:00

Now, excellent.
Okay, so let's go through it.
CoinShuffle++, peer-to-peer mixing and unlinkable Bitcoin transactions.
This is the paper we're talking about.
It's unclear if the authors are going to be able to join us.
If not, they'll join us next week, hopefully.
Yes, two weeks ago we talked about CoinShuffle, which was the predecessor to CoinShuffle++.
CoinShuffle dealt with the issue of removing the coordinator, doing fully decentralized coinjoins.
But the way that CoinShuffle did it was they would shuffle addresses by onion encrypting them and essentially mixing the addresses as the encrypted addresses are passed across all the peers.
As they are passed across peers, they would be decrypted and then further shuffled.
And we talked about why this is a poor design choice because it doesn't scale very well.
And so as an example, we looked at Electron Cash, which had only five participants in total doing CoinJoin.

## Weekly recap

Max Hillebrand: 00:01:16

So here's where we are in the Wasabi Research Club.
Next week we'll likely do CoinShuffle++ again with the authors.
So I just wanted to quickly run through the DC-network.
So the DC-network was a problem posed by Chaum in 1998 and the idea is that three cryptographers are sitting at a table and they want to anonymously convey whether or not they paid the bill.
So one thing we notice about the dining cryptographers protocol is that it allows for anonymous communication among honest peers and only honest peers.
We'll see why in a second.
And it's completely resistant to traffic analysis, which is in contrast to something like the Tor network.
So one more time, three cryptographers sitting at a table, they need to communicate whether or not they paid for dinner.
So if they didn't pay for dinner, you can think of this as a zero, and if they did, you can think of this as a 1.
At the end of this protocol we want to essentially know whether someone in this table paid for dinner or not.

## The cryptographers at dinner (DC-nets, Chaum)

Max Hillebrand: 00:02:26

So here's how Chaum proposed to do this protocol anonymously.
Every single user is going to look to their right and create a hidden secret.
Just a simple zero or one will suffice and we'll do this for all participants until there are three secrets.
Each secret is only known by two participants and what everyone is going to do is they're going to XOR their secrets.
XOR is just simply asking is the secret on your left different from the secret on your right?
If it is that's a one, if it's not that's a zero.
And so every single participant XORs their value, as you can see here, and they speak out loud the value to the remaining participants.
So you can see here that the orange participant has a one as a shared secret on both sides, so his message is 0.
The green has a 1 on one side and a 0, so his message is 1, and so forth.
And there's only one additional thing we need to do for this protocol to work, which is if you, in fact, are the person that wants to convey that you paid for dinner, therefore someone paid for dinner, you just XOR the value 1 with whatever you have which is a fancy way of saying whatever value you have, you negate that value, you flip the bid.
So in this case what we'll do if no one paid for dinner, then they'll simply say the values they have.
The sum of those values will always be even and all participants know because the sum of the value is even that no one at the table paid so likely an NSA member paid.
But if you are the payer in this case we'll look at Orange.
Orange did pay for the bill.
Orange is going to flip the bit.
Originally, orange was supposed to declare a zero, but now orange is declaring a one.
And so the sum is an odd number.
If the sum is odd, then it means that it was one of the individuals at the table that was in fact the payer, and that's good.
And we know as well that this works because if you look from the perspective of Yellow who did not pay the bill, yellow does not know the secret, the shared secret between green and orange.
And so, yellow doesn't know whether it was green or whether it was orange that in fact paid the bill given the public messages.
And so, all yellow knows that the sum is 3 and that someone must have paid.
Okay, was it either of them?
It's unclear to know.
So the other question we had was why is it always even?
Why is it that even if we have 800 of these people at a dinner table and if every person only has two shared secrets with someone on their left and someone on their right, why is it that the XOR is always even if we sum the XOR values across all participants?
And the reason is quite simple.
All participants either have a zero or a one to their left and to their right.
If they have a different value, then they message 1.
And if they have the same value, they message 0.
And Because it's in a circle, the value must always come back to the original starting point.
So for this reason, if one participant goes from a 0 to a 1, then someone else will have to go from a 1 to a 0.
And that's why it's always even.
And this is the same no matter what kind of setup you have, whether you have many participants or just a few.

## Message collision in DC-networks

Max Hillebrand: 00:06:08

So there are two problems we have to discuss because those are the key reasons why we don't use DC-nets in any practical applications.
And it's the key thing that's solved in CoinShuffle++.
Namely, number one is the collision of messages.
So the only way this protocol works is if only one person speaks at a time or nobody speaks.
So if for example, let's suppose that Green actually paid for half of the bill and Orange also paid for half.
And so what they're doing is they both negate their bid when they speak out loud.
Well, unfortunately that doesn't work.
What happens there is that the values get negated and the entire table gets an even sum.
And so, Unfortunately, Yellow, who is the only person not in the loop that doesn't know the secret, wrongly believes that the NSA paid, which is not the case.
So the big thing to understand here is that when you do a round of a DC-net, you cannot have more than one person say a message.
If more than one person says a message, it actually garbles up both messages.
So that's a pretty big problem.

## Malicious actors in DC-networks

Max Hillebrand: 00:07:28

So further, we have to talk about kicking disruptors.
Something that a malicious entity can do, in this case, Orange is a malicious entity, is simply not obey the protocol.
So, for example, reveal random messages, or messages that are not XORs of what you have, or possibly even the opposite of the XOR that you have, purposefully garbling all the other messages.
The problem in this case is that if orange does something evil, like in this case here, green really did pay for the meal, orange did not pay, but orange is saying as though he paid.
The problem here is that there's no way to find out who the disruptor is in an efficient way.
So in other words, orange can disrupt indefinitely this protocol from happening and that's pretty unfortunate.
So yeah, so who disrupted the message?
It's unclear.
Okay, so yeah, in this case yellow is just unaware of what's going on because yellow doesn't know whether it was green or orange that disrupted the message.

## CoinShuffle++ / DiceMix protocol / 4 + 2f rounds

Max Hillebrand: 00:08:41

So now we're going to talk about CoinShuffle++.
So in the paper, four things are discussed.
First, the paper discusses how peer-to-peer mixing is really a natural generalization of DC-networks.
This is because when you have a peer-to-peer mixing strategy in Bitcoin, we essentially have a bunch of peers that need to anonymously post an address for the mixing.
And then they present, number two, the DiceMix protocol, which solves the two issues I brought up with DC-nets, namely collisions and with malicious peers.
And what's really fascinating about this protocol is that it works in only `4 + 2f` rounds, where `f` is the number of malicious peers.
So given no malicious peers, the entire protocol will end in just four rounds.
And then we have CoinShuffler++ which applies DiceMix to Bitcoin transactions to create decentralized and anonymous Coinjoins.
And lastly, the panel presents internal tiers and peer-to-peer mixing protocols.
We're picking up some noise from...

Adam Ficsor: 00:09:56

I think, yes, one of the authors actually appeared.
Oh, okay.
So just a quick recap.
We usually have a Hangout link.

Tim Ruffing: 00:10:09

Yeah, it's just straight to your email.

Adam Ficsor: 00:10:12

Yeah, so we're going to do CoinShuffle++ again next week.
It's quite difficult so I think two weeks is good.

Tim Ruffing: 00:10:23

Okay, makes sense.

Adam Ficsor: 00:10:27

Oh, and don't forget to unmute yourself when you're talking.
Yep.
Okay.
Alright, Hillebrand you can continue.

Max Hillebrand: 00:10:36

Okay, so Tim Ruffing is here which is pretty exciting.
So now we're talking about CoinShuffle++ because we covered DC-networks.
So DiceMix requires only `4 + 2f` rounds in the presence of `f` malicious peers.
Okay, So I have to come clean and say that I did not fully understand how and why this protocol works, but Essentially the idea is that users are, as opposed to using messages that are XORed together, these DC-nets messages will be power sums.
And so then the messages are extracted by finding the roots of the polynomial.
So I played around with this myself quite a bit, and I tried to replicate this and look at the code for hints, but I struggled quite a bit.
But yeah, that's where I'm at.
So the idea is intentional collisions with this protocol.
And so the entire thing goes in four stages.
Firstly, a Diffie–Hellman key exchange between participants.
Then the commitment phase, where participants are committing what their message is going to be.
And then there's the DC-nets phase, where the participants are using power sums over a finite field to construct their own secure message.
And then there's the confirmation phase, which is the end of a successful mix where messages are made available and all participants have the same anonymous messages.

## Malicious actors in DiceMix

Max Hillebrand: 00:12:53

The way that DiceMix handles malicious peers is by having ephemeral keys and by having participants reveal their secret key and reveal paths that allows everyone to see who in fact is the malicious peer to then exclude them in the next round.
So That's how that's dealt with.

## Example of DiceMix round

Max Hillebrand: 00:13:17

So here's an example of these communication rounds.
So if you look at the first run, number one, you have the key exchange, then you have the commitment phase, then you have the DC-net.
And because the protocol could not arrive at the confirmation phase, the secret keys are revealed and then the pads are revealed, allowing malicious participants to be excluded.
The protocol continues over and over again until finally it reaches the confirmation part of the protocol.
This is Probably the most interesting thing about this protocol, which is that it scales really, really well with more participants.
So, in the original CoinShuffle protocol, there was a sequential bit of work where users had to decrypt and shuffle addresses and then pass them to the next peer in order.
And so because it was sequential, it did not scale very well whereas this here can happen at the same time.
The only thing that causes it to scale worse as time goes on is that you have more complexity when it comes to factorization of the polynomial.
And that's what's visible here in the green.
So yeah, so 100 peers can essentially get through the protocol in just over 20 seconds, which is pretty impressive.
So yeah, by using DiceMix instead of the original DC-net, we can achieve guaranteed finality of the message protocol in `4 + 2f` rounds, where users anonymously post their equal output fresh addresses.
Collisions and disruptions are both effectively dealt with.
Protocol scales efficiently, and the authors claim that it's a substantial improvement to CoinShuffle, which required users to pass encrypted messages sequentially.
So, yeah, that's pretty much it.
I wasn't 100% sure about some parts, but hopefully we can ask questions now.

## Knapsack and unequal amounts

Adam Ficsor: 00:15:41

Okay I want to start with something of a segwit.
It's the most exciting thing probably that Lucas, when we were talking about CoinShuffle, not CoinShuffle++, you figured out how to do it with unequal amounts with the third Knapsack algorithm that's not in the paper.
Can you elaborate on that and Tim may be able to reflect on that idea?

Lucas Ontivero: 00:16:15

Okay, yes, well, my idea was that in the Knapsack paper, it details how an equal output CoinJoin transaction can be built, right?
So, talking with the author of that paper, he said, well, there is one of my proposals that is not in the paper, is that another protocol where you only need to know how much the rest of participants want to participate with, I mean the amount, so the outputs can be splited with this Knapsack algorithm and then the participants and not a central server who can create this unequal output without any interaction.
So they only need to know how much the rest of participants are going to participate with.
So my idea was in the CoinShuffle protocol, if we know how much the rest are going to mix.
Every participant knowing that can split the outputs, right?
And the rest is exactly the same.
I mean, they can just create this onion layers of encryption with the public keys of the rest and the rest of participants do exactly the same.
I mean, they just receive the addresses, in this case are the outputs because if the address plus the amount, I mean, let's call it the output.
And of course they don't know what the outputs are, they just shuffle those outputs.
Because otherwise, in the final CoinJoin transaction if they don't shuffle the outputs you know the first outputs belong to this guy, this other outputs belong to the next one so they shuffle in the same way exactly the same way so the the last participant, the one who finally decrypts the layer of encryption, the last layer of encryption, only sees a lot of outputs and all are unequal outputs.
So I don't know if that makes sense for Tim.

Tim Ruffing: 00:19:34


Yeah, I'm not sure if I got the entire idea, to be honest.
I mean, I looked at the Knapsack paper once, but this is really like years ago or so.

## What is required to determine input amounts?

Tim Ruffing: 00:19:57

It would be interesting to know what exactly is required to come up with the amounts here.
So you basically, you simply know, What you said is that you just need to know the mixing amounts of all the others.

Lucas Ontivero: 00:20:27

Yes.

Tim Ruffing: 00:20:28

Isn't that already something that like the peers in the CoinJoin probably don't want to tell each other?

Adam Ficsor: 00:20:40

It is the inputs, right?
So isn't that already just told everyone what the inputs are?

Tim Ruffing: 00:20:48

Well, okay.
Yeah.
I mean, if they're going to mix the full amount and the input, yes, it's public anyway.
Okay.

## Fixed messages

Tim Ruffing: 00:21:00

But actually, there's a second problem.
So the problem with using amounts in general within something like CoinShuffle, And I think here it really doesn't matter if this is now CoinShuffle or CoinShuffle++.
It's actually in the, CoinShuffle++ paper, but it applies to normal CoinShuffle as well.
So, CoinShuffle basically works by the idea that you use fresh addresses for your mixing.
Like you take a new address, you input it to the mixing protocol.
And again, it doesn't matter now if this is CoinShuffle or CoinShuffle++.
And In the end, you can basically, if something goes wrong, you can de-anonymize this round and throw away your new address because it has never been used, right?
So it's never been used to receive money.
It will never be used in the future.
So it's okay to de-anonymize this round.
Then you, by de-anonymizing, you can figure out who's malicious and kick them off.
And then you can restart without the malicious guys.

Adam Ficsor: 00:22:36

Yes, so your point is that the amount cannot be fresh.

Tim Ruffing: 00:22:41

Right, yeah.
So this is the point.
Like the amount is something that I call "fix".
I think this is the term we use in the paper also.
There's a simple attack once you use fixed messages.
So, let's for example, say we all use, let's say, CoinShuffle for mixing not a fresh Bitcoin address, but some real, I don't know, document, text file.
Everybody has a text file.
Now, what you can do is you can disrupt the first round by basically disrupting the last message of all participants in the sense that you as the attacker on the network, you learn the output of the protocol.
It means you learn the set of all text files.
You don't know yet which file belongs to whom, right?
Because it's so far we are anonymous, but you learn the set of all text files.
And what I can, but what happens is because I disrupt the last run by just simply blocking it on the last round.
So if I simply by blocking it on the network, all the other guys have to restart because they think I'm offline or something.
And then I can block.
So again, assuming I'm the network attacker, I can block some honest users messages on the network.
So This means that the second round also won't finish because there's another guy appears to be awful now.
And now the remaining participants still need to restart from scratch.
They kick out the honest peer that I blocked, they kick him out too.
And now afterwards, let's say the remaining peers that are still on the protocol now managed to finish the protocol.
And now let's say in the beginning we had five people including me.
So I went offline in the first run, then I blocked somebody in the second run.
So there were three participants left now and they have three text files.
And I learned at the beginning all the five text files.
So now I can just look at the two that are missing now in the final output.
And I know one of them is mine.
So I know the other one is from the guy I blocked.
Not sure if this was understandable.
Actually, I can, next week I can bring some slides if I'm here.

Adam Ficsor: 00:26:07

That would be fantastic.

Tim Ruffing: 00:26:09

And show them, because anyway, I have slides for a lot of stuff in CoinShuffle.
But yeah, I think this is a generic attack and this works whenever I can.
I can basically make participants be offline, maybe because I'm a network attacker or blocking their messages.
And it's actually pretty annoying in CoinShuffle because, I mean, in the paper we say it's peer to peer.
What we mean by that, it's basically peer-to-peer on the, if you look at the transaction that's generated, right?
Because in the end, it's basically CoinJoined.
That if you want to do this efficiently, you want to run it over a server, or what you call a bottom board, which is simply responsible for broadcasting messages.
And we don't trust it otherwise.
That's the idea here.
But as soon as everybody connects to a bulletin board, you can maybe just think of my RC server, untrusted RC server.
What we of course trust the server for is that it doesn't exclude people arbitrary from the protocol, right?
It could say, okay, look, this is always Tim.
I don't want Tim to have anonymity, so I exclude him always.
And I think that's in the normal CoinShuffle, that wouldn't be a big issue because, well, I mean, if the server doesn't like me, I can yell at it and use another one.
But like if you use fixed messages and the attack that I mentioned earlier comes into play, then that's pretty annoying because like If I send all my broadcasts via the server, it's very easy for the server to block my messages.
The server just needs to pretend that I went offline.

Adam Ficsor: 00:28:18

Yeah, it makes perfect sense, actually.

Lucas Ontivero: 00:28:24

For me too.
I mean, obviously the problem is that we need to kick the bad participants out.
That's why my idea will not work.

Tim Ruffing: 00:28:42

It's also, by the way, if you, I'm not sure if this is on some future agenda, maybe it is.
I guess people also heard of value shuffle, which is basically assuming, like assuming they have confidential transactions where we can hide the amounts, then this is basically the combination of CoinShuffle++ and confidential transactions.
And there suddenly it works with mixing amounts because there the amounts are in commitments, which you can recreate and which are re-randomizable.
Like if you commit to the same value twice, it will result in a different commitment.
That's why those messages as inputs to the mixing protocol are not fixed in that sense anymore.
But okay, it's just a remark.
Like, as long as we don't have CC.

Lucas Ontivero: 00:29:39

Yes, value shuffle was or is in the agenda.
It was, the idea was for the next week, but the next week we will continue with CoinShuffle++.

Adam Ficsor: 00:29:52

Lukas, CashFusion is in the agenda.

Tim Ruffing: 00:29:59

Oh, okay.
I'm glad, because I didn't see it on the GitHub page.
Yeah, whatever.
Just a remark.
Okay.

Adam Ficsor: 00:30:14

All right.
Yes.

Tim Ruffing: 00:30:19

On the other hand, like, so this is very, very early stuff, but there are also, so what would be interesting is to have something, okay, let me start differently.

## Generic attacks

Tim Ruffing: 00:30:33

So I think the attack that I hear mentioned is so generic that it applies to pretty much every anonymity system you can think of, right?
Like even if I sent...
At least every system where I don't trust my peers.
And actually, this is how it's written in the paper.
So I was thinking, and I'm just currently working on this with Pedro again, Pedro Moreno-Sanchez.
We're looking into relaxations of this model where you maybe have a few trusted servers, but in the sense that, I don't know, maybe there are 20 servers and you only need to trust one of them to be anonymous.
And maybe it's possible to avoid this attack in such a setting because the attack relies on the fact that people can stop the protocol from completing.
And it's maybe interesting to see if we can get around this using some trust that may be acceptable for some users.
I don't know.
However, now that I say it again, I think it's pretty hard for...
I think what I just said makes only a little bit sense because we were looking at other settings.
I think if you really have CoinJoin in mind, That won't really work because in CoinJoin in the end I can always refuse to sign the contract transaction.

Adam Ficsor: 00:32:55

Yes, for example if you would want to use value shuffle then It doesn't matter because at the end you can always choose.

Tim Ruffing: 00:33:07

Even if I somehow use whatever servers to avoid that I simply go offline during the actual mixing and they can somehow continue the protocol.
The rest of the people can continue the protocol without me.
I still won't sign at the end.
So, yeah.
Of course, now you can say, look, I can do more weird stuff and do secret sharing with 20 servers but it's probably not what I wanted to do.

Adam Ficsor: 00:33:40

I have another question.
I have a lot but this is important and then let other people speak that.

## How to understand CoinShuffle++

Adam Ficsor: 00:33:47

Since we are doing this next week too, what would you suggest, how would someone go and understand CoinShuffle++?
In what steps you would do?
Would you first look at the pseudocode and then move upwards and downwards of the paper?
Or yeah, what would be a good way to understand it?
Because I have to admit too, I did not fully understand, but I really tried.

Tim Ruffing: 00:34:20

Okay, yeah.
Let me think about this.
I don't think it's a good way to look at the pseudocode.
I mean, the pseudocode in the paper is very detailed, but I think in that sense, it's too detailed to really understand the protocol from that one.
The reason why we wrote so detailed pseudocode is that in CoinShuffle, it was rather in the original CoinShuffle paper, the description of the protocol was pretty high level.
And some people tried to implement it and screwed up.
So that's why we prefer to give the full truth, even though it's hardly readable.
In the hope that if somebody really translates it from the paper without having too much background in crypto doesn't screw up entirely.
As I said, I can bring slides and try to explain it in the way I would explain, but I think if you understand how a DC-net works, which I think you looked at last week, then I would approach CoinShuffle++ simply as a way to set up a DC-net?
And then if you look at the steps, As we also seen on your slides here, well, what do we need for DC-Net?
We need shared symmetric keys.
Okay, so in the beginning we do key exchange.
Then we need to run the actual DC-net.
And here it is, this trick with the power sums is actually not too essential for a high level understanding of the protocol.
It's simply a way to encode messages.
And it's a clever way because it always works independently of collisions.
But it doesn't give you anonymity or anything like the entire anonymity is provided by the DC-net basically.
So it's just a different encoding of things that we sent through the DC-net.
But it doesn't have in any sense an unlimited limit.
It's just makes sure that we can get the messages, that we can extract the messages later without having any DC-net collisions where some people where they have could be slots, for example, and some people send in the same slot and then you get the extra of the messages and you can't get the extra message back.

Adam Ficsor: 00:37:44

Thank you.

Max Hillebrand: 00:37:45

Yeah.

## Base case: 4-bit message and 3 participants

Max Hillebrand: 00:37:46

So this is exactly what I want to sort of replicate and I think Adam is probably thinking the same thing.
You know, I would like to see that I understand the protocol with like, let's say a four bit message and three participants.
Yeah.
That I could do myself and I was really struggling to do that.
So maybe you can next week in the slides you can show something of that nature or sort of walk through step by step because I wasn't entirely clear.

Tim Ruffing: 00:38:25

Okay, yeah.
Yeah, I can try to do that.

Adam Ficsor: 00:38:33

That's perfect.
I personally, until I don't code something I don't understand.
And I coded all the papers that we were discussing so far, so I thought I have a good understanding.
But this one, I couldn't.
I was trying to go through the pseudocode.
But you have some functions, those are very cryptographic functions and it's not just, right, you have the building blocks, the sign message, verify message, it's just normal cryptography.
But then you have some much stranger cryptography like the Diffie–Hellman key exchange, which I'm not sure what the inputs and outputs should be.
So yeah, that's where I got stuck personally.

Tim Ruffing: 00:39:31

Okay.
Yeah.
So To be honest, there is a reason why I never wrote an implementation of this and I still want to do, but I never managed.
And I think Not because it's not possible, but it's just because it's a very large project.
Even though it's already simplified from the first CoinShuffle.
So actually, When we were writing the second paper, the CoinShuffle++, people contacted us because they were interested in doing an implementation of the other one.
And we even told them, look, I think the new protocol is actually easier.
It's better in every aspect.
Just throw away what you've written so far and start from scratch.
Of course, they weren't happy with the suggestion and didn't take it.

## Implementation differences in CoinShuffle and CoinShuffle++

Adam Ficsor: 00:40:28

So what do you think is the reason?

Tim Ruffing: 00:40:32

The reason for why...

Adam Ficsor: 00:40:37

Why CoinShuffle got implemented like three or four times, I don't know, but CoinShuffle++ did not.

Tim Ruffing: 00:40:45

Oh, that's an interesting question.
I don't know, to be honest.
I mean, the story that I just mentioned, okay, I mean, there was the case that, like, just the new thing wasn't out yet, so they couldn't know about it.
For the other instances, I think just the plus plus paper didn't get so much attention.
There are also some papers that cite the first version and not the second version, which is kind of okay.
Depending on how many citations you want to have in your paper, this is perfectly appropriate.
But at some times, I feel just people overlook the new version.
Also, maybe because we didn't like the title, which is not super clever, because it's called, it doesn't have CoinShuffle++ in the title, right?
So if we would have put that into the title, then I guess it would show up in Google CoinShuffle.
I don't know.
I'm just randomly guessing here.
It's an interesting question.
Randomly guessing here.
So it's an interesting question.
Another reason why really people prefer CoinShuffle++ is, I think this is something that only really was very clear to us when we worked on the plus plus version is that actually kicking people.
So in the normal CoinShuffle, it's easy to deal with cases where people send wrong messages and A lot of the work in the protocol is figuring out who sent wrong messages and kicked them out.
It's however, in this structure where you like the first peer sends to the second one and the second one sends to the third and so on.
In such a structure, it's much harder to deal with peers that appear offline.
Like what if the third guy doesn't receive a message or claims that it doesn't receive a message from the second guy, who's to blame, right?
The second or the third?
And how do you agree on now should we kick out the third or the second one?
And I think if you have a closer look at this, what you really want in the end is again, something like a broadcast channel, which we then in CoinShuffle++ have anyway, because we describe it like this.
And then you have just a server, this untrusted ISC server in the middle that has to find a decision over whether some peers send a message or not.
But then at least it's the same decision for everybody.
So you have to kind of have this broadcast functionality built in.
And of course, now you could go back to CoinShuffle and implement it via the same way.
So instead of letting the first peer send to the second one, the second to the third and so on, it's just everybody sends to the ISC server in the middle.

Yes, you could do this, of course, but then it kind of wastes communication, right?
Because like the only advantage of the normal CoinShuffle protocol would be that you don't need this broadcast in a sense because you only need to talk to the next guy but yeah as I just explained I think this is not really an advantage.

## Broadcast protocol for CoinShuffle / Complexity in CoinShuffle

Adam Ficsor: 00:44:56

Interestingly I misunderstood CoinShuffle at the first time and I implemented a broadcast protocol.
I implemented it in a broadcast way, not in a one-guy talks to the next guy.

Tim Ruffing: 00:45:12

That's interesting.

Adam Ficsor: 00:45:15

It worked.

Tim Ruffing: 00:45:17

Yeah.
I think like, assuming that you have the protocols, I think then crypto-wise, the first protocol is a little bit easier because this layered encryption doesn't have, yeah, it's just encryption, right?
There's no weird process.

Adam Ficsor: 00:45:38

It's just encryption.
I think it's a layered encryption.

Tim Ruffing: 00:45:43

Yeah.
On the other hand, another thing that we figured out when we were looking at the second version is a lot of complexity in CoinShuffle 1 is about getting the cases right when something goes wrong.
Then you have a lot of potential additional messages that peers need to send.
And then you have a huge, basically a case of sanction on just to figure out who is to blame.
And This is also something that is easier in CoinShuffle++.
I actually don't know if we wrote it like that in the paper, but I think we did a general insight.
There was that.
Anyway, the, the method there is that, if you abort around, which basically means you want to de-anonymize the round entirely, but what you do is you reveal the secret from your key exchange, which basically is the only secret information you have in this round, except for your Bitcoin signing key.
Okay, you obviously shouldn't reveal that one.
But like from the mixing itself, the Diffie-Hellman secret is the only secret in the protocol.
This means that as soon as you reveal your secret, what you send is entirely deterministic.
And this makes it very easy to implement the blaming procedure that should figure out who misbehaved because now what you can do is I learn your secret now.
So, and I know your message by looking at the protocol.
So what I can do is just replay your entire protocol messages, re-compute them and just compare them bit by bit to what you actually sent.
And if you send something else, well, then you misbehave.
We can just do this for every peer.
So It's much easier to implement than having this huge case distinction.

Adam Ficsor: 00:48:27

Lucas, Hillebrand, Raphael, do you have something to discuss, questions?


## Complexity in the communication layer / Why not use Tor?


Lucas Ontivero: 00:48:34

I have a question.
Because when we have been studying this ideas and discussing this idea we started with CoinShuffle then just jumping directly to CoinShuffle++, we reviewed the DC-network.
And what I see is that a big part of the complexity of this protocol is about the communication layer, how we communicate with others.
So why are...
Sorry, I don't remember the paper in detail.
Sorry, probably everything is there.
But, why do you think that's the best mechanism instead of using something like Tor, for example, what could simplify the protocol a bit.

Adam Ficsor: 00:49:39

Do you mean using Tor as the protocol or the Tor network as the built thing.

Lucas Ontivero: 00:49:51

Because we are discussing how to, I mean, if you have a man for an encryption key, a shared key, right?
How to broadcast, how to blah, blah.
I think that could be simplified by just communicating with the rest of the peers through Tor, for example.
I mean, why are we using DC-networks?

Tim Ruffing: 00:50:28

Yeah, so I think What you're saying makes perfect sense.
And I think if you like, there's a trade off.
And I think there's a reason why like the existing point of implementations and Adam's implementation, I think it's the one that should be mentioned here actually works by leveraging Tor because then suddenly the protocol becomes much easier.
I mean of course to organize CoinJoin it's not just using Tor.
You need more, like for example like signatures.
But the entire thing becomes way simpler.
The reason why we wrote this paper is that we think it's interesting to have a protocol where you don't rely on Tor.
Mainly because it gives you a stronger anonymity guarantees, right?
Tor is optimized for different settings.
So in anonymous communication, there's always a trade off between multiple efficiency and security dimensions.
Something like a DC-net is pretty slow compared to Tor, but it's fully anonymous.
Like by observing the network, you can't tell anything.
Whereas in Tor, they optimize for low latency, which is very important if you look at websites, because you don't want to wait forever.
But in Tor you have two anonymity drawbacks, right?
So if you first you trust your Tor nodes, and of course you don't trust them fully, right?
There's a distributor trust.
For example, like if your guard node and your exit node work together, they have a good chance of deanonymizing you.
And the same is true for a tech that just listens to the network but can do end-to-end timing correlation.
And I think the reason why Tor made this straight up is what I said, like they want low latency because it should be usable for web browsing.
But here actually I think we are in a different setting.
And we can actually have stronger anonymity by something like a DC-net.

Lucas Ontivero: 00:53:38

Okay, I have another question and again, sorry, I couldn't read the paper.
I don't remember.

## How does the protocol prevent learning of IP addresses of participants?

Lucas Ontivero: 00:53:47

But in this case, the message is clear, it's encrypted, right?
So nobody can read that.
But how is the communication, the communication mechanism, how is it that it prevents learning the IP addresses of the participants?

Tim Ruffing: 00:54:13

Oh, it doesn't.
That's a simple answer.
Okay, sorry.

Lucas Ontivero: 00:54:22

Please, let me check if I understand correctly.
In CoinShuffle, at least, you only communicate with the next guy, so in that case only one participant knows about your IP.
In this case, is it the same or not?

Tim Ruffing: 00:54:47

I think this depends on how you implement it, but let me explain it in a different way maybe first.
So I think when we talk about anonymity and what we actually talk about is unlinkability.
Shouldn't be able to link pieces of data together in the sense that they belong to the same guy.
And now we have unlinkability on different layers here.
So what CoinShuffle is, or CoinShuffle++ is supposed to give you is unlinkability between your input address in the CoinJoin and your output address in the CoinJoin.
Now, what you're asking about is unlinkability between the input address in your CoinJoin and your IP address?
And that's another relevant question, but it's a different question.
Now, because you mentioned Tor, Tor kind of gives you some unlinkability between your IP address and whatever data you send, right?
So it also in a sense, it hides your IP address.
That's why actually in the paper, we say if you care about the second form of unlinkability of not being able to link network identifiers such as IP addresses to your messages, If you care about this too, and probably you care, right, because if you care about privacy, you probably care about privacy on all layers, then you should actually use Tor to run DiceMix or to run CoinShuffle++.
Which is another reason why the implementation with the idea of a server in the middle and plant signatures and where we send over Tor has an advantage because there we use Tor for two different aspects and we only need it once.
But like if you would run CoinShuffle++ without Tor, which I think was the second part of your question, then it really depends on really how you organize your network.
Like if you run it as you propose in the paper with a server in the middle, that's only trusted for basically doing the broadcast, right?
And you don't trust it for anonymity or for, let's really say, for unlinkability between inputs and outputs in the mixing.
Then it's just the case that everybody connects to the server, right?
So the only guy that learns your IP addresses in the end is that server.
Of course you don't want to trust it, but it's better than sharing your IP address with everybody, right?
So I think like the basic guarantee of CoinShuffle++ is always there, also if you run it without Tor.
If you additionally want to hide IP addresses, then it's a good idea to run it over Tor or some other anonymity network.

## How does the 20 second benchmark change with Tor?

Adam Ficsor: 00:58:34

Since we are at this topic, you have the second benchmark there in the paper.
So how would it change with Tor?

Tim Ruffing: 00:58:44

That's a Good question.
I don't know.
I mean, certainly slower, of course, but it's an interesting question.
I hope it's not too much, but I mean, to figure out, I think we need to test it.
I mean, my hope is that it wouldn't be terrible because I think bandwidth-wise, Tor is mostly okay-ish nowadays.
And one of the advantages of the protocol is that it has a constant number of rounds.
So like latency-wise, Yeah, it's not so important to have super low latency because you have only four rounds.
I think The most annoying thing about Tor would be that in the experiment, in the paper, we assumed that everybody connects to this middle node, this broadcast server in the middle, and they all have the same bandwidth to the middle node, which is the optimal setting.
And because the protocol is synchronized, so for every round, you need to wait for the last message from everybody.
And basically the portal net is the slowest peer.
And then if you imagine like 50 peers connecting via Tor, then they probably have just already by the, not only because their internet connection has different bandwidths, Just by a random selection of four routers, they will have different bandwidths.
And then we have to wait for the slowest one of the four rounds.

## 2 minute timeouts in Wasabi

Adam Ficsor: 01:00:46

I can actually tell exactly how much is this lowest peer is going to be because in Wasabi we encountered the same issue and some runs were failing and we were not suspecting DOS attack.
And then we started logging that the peers, those are replying with the message too late.
And it turns out we had to elevate the timeouts to two minutes.
I still have no idea why it had to be that large, why they are replying so late.
But some, the slowest peers are replying in fucking two minutes.
So it's not very encouraging.

Tim Ruffing: 01:01:43

Yeah, two minutes is very long.
If they're not malicious, then doing it is potentially late.

Adam Ficsor: 01:01:56

But don't take this as face value that much because another thing that we realized is when they have to query the whole transaction, which is, I don't know, a kilobyte or maybe a kilobyte, then they are replying slower than when they have to query just some small random data, which is interesting because it should not be the case because the issue with Tor is the communication rounds and not the amount of data.
So, there is that.
Maybe it's one minute, I don't think half a minute, but yeah.

## Using new negotiations. / Tor streams

Lucas Ontivero: 01:02:45

Sorry, just a quick thing.
I suspect that the problem is we are using a new circuit.
A new circuit means a new negotiation.
And all, a lot of cryptography and handshake with the entry point and finding a hidden service directory to make, it is like a DNS for hidden services, right?
And all that negotiation, sometimes really fast and sometimes really slow because in fact it has to query a directory authority or something like that.
So it's really heavy, the creation of a new circuit.
Once the circuit is done, well, the communication is quite decent, the performance, I mean, the bandwidth.

Adam Ficsor: 01:03:49

Actually, we are using new streams that's a little bit different.
And those streams are already built up.
And actually, because I wrote tests for it, when a stream is not built up yet, then Tor is going to just put it in an already used stream So it doesn't want to ruin our performance Anyway, we are going out of the topic.
Raphael, do you have something?

Raphael: 01:04:34

Not really.
Just thinking about all the stuff you've been talking about.

Adam Ficsor: 01:04:43

Yes?

## When 1 round fails

Max Hillebrand: 01:04:45

Yeah, if one of the rounds fails, all of the participants have to reveal their messages, correct?

Tim Ruffing: 01:05:00

Right.

Max Hillebrand: 01:05:02

In the presence of a malicious party.
So I'm just thinking practically speaking, it would mean that if we're working with a wallet and it reveals its addresses, those addresses can never be used again, right?

Tim Ruffing: 01:05:26

Right, I think that's one of the fundamental ideas, that you really use a trust that you never basically used before and then if you know you throw it away you will also never use it in the future.

Max Hillebrand: 01:05:42

Okay that's pretty clear.

## Would Wasabi be safer if it used a CoinShuffle model?

Max Hillebrand: 01:05:45

So are you familiar I mean this might be very rude, but are you well familiar with ZeroLink and how Wasabi is working?

Tim Ruffing: 01:06:00

I'm not sure.
I know a little bit.
Maybe just explain what you want to say and we can see if I can follow.

Max Hillebrand: 01:06:11

I'm just curious if from where you're from your research, if you think that Wasabi would be more secure, safer or better if it was using a CoinShuffle++ model.
Because right now, Wasabi uses a server that does a blind signing of secret outputs.

Tim Ruffing: 01:06:40

Right.

Max Hillebrand: 01:06:44

This is similar to what we've talked about, but yeah.

Tim Ruffing: 01:06:48

I think ignoring all other trade-offs, I think such a model would be preferable really because it provides a stronger form of anonymity and it doesn't rely on Tor.
So, but as I said, there are trade-offs and I still hope that it's possible to implement CoinShuffle++ in a meaningful way.
And assuming we have such an implementation and assuming somehow that's at some point in the future, we will really do it because I still want to do it.
The question is really like how would it perform in practice because four rounds of course is the optimal case and it's kind of nice.
But if you have peers dropping off for whatever reason, you add rounds and you have to restart.
And now if Adam is telling me, okay, like even with Wasabi or with zero link, we already have like timeouts of two minutes.
Yeah.
It's larger than I expected to be honest.
But I think it's something that really we should look into.
Because I said, I think like from a privacy point of view, it's actually the stronger model.
Also, not relying on Tor gives you the advantage that Some people may not be able to use Tor for various reasons and here they still get a meaningful anonymity guarantee.
Whereas if you really rely on Tor, Either you can run it or you cannot.

## CashShuffle vs CoinShuffle

Max Hillebrand: 01:09:04

At one point your co-authors mentioned CashShuffle and he said that it was not a correct representation of CoinShuffle.
I'm just curious if you know anything about that and why that was the case.

Tim Ruffing: 01:09:23

Which of my authors was talking about?

Max Hillebrand: 01:09:27

It was Pedro.

Tim Ruffing: 01:09:31

Okay.
Yeah.
I can't say for sure what he was referring to, but when CashShuffle came out, I had a look at the implementation and I found multiple pretty severe flaws.
Of course, then it was still a GitHub project in the early days and not really used.
I think they fixed these flaws.
At least they told me and actually I reported them on GitHub.
As far as I know, now people have looked at the implementation and it seems better, but I've never looked at it again.
I mean, in the beginning, because the flaws were so heavy, I actually warned people about this on Twitter and thought like, look, this is broken.
Then various people yelled at me for doing this.
So what I heard is that they really improved, but I seriously, I've never looked at it again.
So I don't know if they really improved.

Adam Ficsor: 01:10:59

Just to be sure, they implemented CoinShuffle, not CoinShuffle++.

Tim Ruffing: 01:11:04

Right, they implemented CoinShuffle.
This was another, this was one of the mentioned instances where it also, It also looks a little bit suspicious, right?
Because I think, I mean, I told you, maybe it's a little bit harder to find the plus plus version.
But I think if you, if you, before you start such a project, at least that's the way I would do it.
I would first do a lot of research on the background and try, like, look at various trade-offs and different approaches.
And I think, like, if you do that work, you should find CoinShuffle++.
And I think this was also a reason why it looked to me a little bit like, okay, they didn't really spend time thinking about what they actually want.

Adam Ficsor: 01:12:04

I can give you an alternative why CoinShuffle is being implemented, not CoinShuffle++.

Tim Ruffing: 01:12:10

Yeah tell me.

Adam Ficsor: 01:12:16

It's because, for me, when I looked at the CoinShuffle paper, I was like, oh fuck I get it.
I got the basic idea right away I can just work out everything from there by myself Even if I don't read the paper very carefully.
With CoinShuffle++ I was reading it very carefully, but I still don't get the essence.

Max Hillebrand: 01:12:44

Yeah, I have to concede as well that I'm gonna try again for another week and I might email you personally or your co-authors but I didn't understand the idea either.

Tim Ruffing: 01:12:57

Okay, I guess that's also partially our responsibility, right?
Because like if you write a paper, the goal is that people understand it.
Yeah.

## CoinShuffle vs DC-net

Adam Ficsor: 01:13:13

So it would be a DC-net, right?
But you have previous and later phrases which guarantees some properties of the DC-net that in the original DC-net protocol, it's not guaranteed.
Is that a good way to think about it?

Tim Ruffing: 01:13:31

I think that's a good way to think about it.
Yeah.
Maybe one thing I can add here, but now, of course there's not a danger that this even confuses you more.
I hope not.
There is actually, maybe I can put a link here.
Okay, I'm putting the link here, but really don't want to say don't look at it, but this is really like not explained in a proper way.
So please don't look at it if you want to understand it's a bunch of or anything.
But actually, because like the protocol is pretty involved, I also worked on a simpler version of it, which basically raises it to `4 + 3f` rounds, but it's conceptually simpler and closer to original DC-nets.
But this is totally not ready and the pseudocode there is basically, there's just a little bit of text and a long pseudocode.
I think the pseudocode is not even consistent when it's there.
So it's really work in progress.
And If you look at it, don't try to understand it, because I think you won't understand it just because it's broken the way it's written there.
But I just want to point out that, yeah, like even when I thought about implementing this, I wondered how this can be simplified because it's the protocol is pretty complex.

Adam Ficsor: 01:15:28

That's great.
Thank you.

Tim Ruffing: 01:15:32

So when I think like earlier I mentioned that I was looking into some other models with Pedro recently and I think one of the things he also wants to do is drive this a little bit further to get a simpler, a little bit simpler protocol.
Which also would be computationally a little bit faster at the expense of adding around.

Max Hillebrand: 01:16:05

So can you clarify the link you sent us?
I actually happened to have read this entire thing as well, as well as the pseudocode.
It didn't help that much in understanding.

Tim Ruffing: 01:16:19

I think that's what I'm saying.
Like, I think it doesn't help at all.
It's more like my personal notes than anything ready to be understood.

Adam Ficsor: 01:16:35

All right.
Thank you.

Tim Ruffing: 01:16:39

Yeah, It's already interesting for me.
Like if you look at the paper and no one really understands it, maybe we also have to make it more accessible to people.

## Using the pseudocode and building blocks to understand CoinShuffle++

Adam Ficsor: 01:16:56

My idea is that I'm going to just jump right to the pseudocode and try to code it.
Well, jump right to the building blocks, try to code the building blocks, and then back to the pseudocode, and then hope for the best.

Tim Ruffing: 01:17:17

I think one of the annoying things that always appeared with this is that, I think like when I take time to look at this again, What always bothers me is really that you also need some broadcast layer to do this.
And I always had this on my mind when I was trying to implement it, but I guess I should just forget about this for a moment and really write the crypto part of it and forget about networking.
And then, I mean, because it's really like a layered thing, right?
It's a different layer.

## Do you think a p2p network using Hashcash is a flawed idea? / Bitmessage

Adam Ficsor: 01:18:13

Do you think a simple peer-to-peer network that's using Hashcash could work or is just a flawed idea from the beginning, like bit message, right?

Tim Ruffing: 01:18:26

I think that's too much because it's, I guess, too slow.
I think like something similar to serial link comes already close, right?
Like something where people can connect wire to, I mean, they wouldn't have to, but they can.
And it's a kind of a central point that helps organizing.
And also, I think you have the same problem, right?
You need to find peers to mix with in the first place, right?
I think that's one of the other hard problems that's ignored in all the mixing papers I've written.

## Conclusion

Adam Ficsor: 01:19:40

I'm sorry, I was just taking a note for myself.
So I don't know if you guys have anything but regarding the organization, Hillebrand you said you will record this conversation, did you?

Max Hillebrand: 01:19:56

Yes, It's recorded.

Adam Ficsor: 01:20:02

I cannot hear you.
Is it only me?

Max Hillebrand: 01:20:06

It's recorded.
Hello?

Tim Ruffing: 01:20:11

Yes, I can hear you a bit.

Lucas Ontivero: 01:20:21

We can hear you.
Adam?
Adam?
Okay, it seems Adam is here.

Adam Ficsor: 01:20:30

Sorry, I'm here for some reason.
I couldn't hear anything.
Would you repeat that?

Max Hillebrand: 01:20:37

It's recorded.
So yeah, if there are no further questions, I think we should probably let Tim get back to his work.
So are there any other questions?

Adam Ficsor: 01:20:52

Yes, so because we said in the beginning that it's not going to be recorded, it's going to be just a warm up.
Does anyone have any objections on publishing this?

Lucas Ontivero: 01:21:04

I think it's great material.
I think we should publish it.

Tim Ruffing: 01:21:12

No, when it's published, then I really have a public commitment that I'll be there next week and have slides right so maybe you should do it.

Adam Ficsor: 01:21:26

You can cut out that part.
It's okay.
I'm good.
All right then I don't know do you guys have any topics?

Lucas Ontivero: 01:21:42

No, I just have a comment.

## Decentralised p2p communication is required

Lucas Ontivero: 01:21:43

Because, you know, a decentralized protocol for CoinJoining bitcoins is great.
And if you don't need to use Tor it's even better, right?
The problem is that if we use some kind of bulletin board, a centralized one, then probably we need to use Tor to hit that server.
So it's a pity.
I think the decentralized, the peer-to-peer communication is required.
Otherwise, all the benefits, I think, go away.

Max Hillebrand: 01:22:28

Yeah, I was thinking a similar thing.
The advantage is that people wouldn't have to close their Tor circuit.
They could keep their Tor circuit open for the entire round.

Tim Ruffing: 01:22:47

I think there are two things, right?
Yes, I agree, I would love to have a protocol that's fully decentralized.
I think no one figured it out so far.
Yeah, at least here the advantage would be that as you say, like you don't need to rely on multiple Tor circuits.
But if you think in the end you really want to connect Tor to the central point, and then you can really ask the question like, okay, is it worth all the hassle then?

Adam Ficsor: 01:23:29

Oh, there is one more thing, Tim, you remember the CoinJoin meetup?

Tim Ruffing: 01:23:39

Tell me.

Adam Ficsor: 01:23:41

Do you remember the CoinJoin meetup?

Tim Ruffing: 01:23:43

Yeah, sure, but I don't remember that one other point.

Adam Ficsor: 01:23:51

Because I didn't say.
My point is that one of the problems with pay to endpoints or it's quite a general problem that how do you establish connection between one party and another without breaking the existing user workflow.
And there might be a way at least with Taproot, the public key is going to be exposed in the address.

Tim Ruffing: 01:24:25

Oh yeah okay you mean you can do some form of SNICKER?

Adam Ficsor: 01:24:29

Yes, so now what we can do is that when you give me your Bitcoin address to pay you money then I can encrypt a message to your public key and then broadcast it to the network you are listening to that message and then you decrypt that message - only you can decrypt it - and then that message actually contains my Monero endpoint, and we actually have a peer-to-peer communication between the two of us.
Then the user doesn't even know that it's not a normal Bitcoin transaction.
And then you can do pay to endpoint, merge avoidance, even a lightning transaction in the background.
So I think that's exciting anyway.

Lucas Ontivero: 01:25:29

Oh, that's great.
And in fact, a kind of Bustapay or something like that could be possible too.
I mean, the two parties can join for payment.

Adam Ficsor: 01:25:44

Yes.

Tim Ruffing: 01:25:49

I agree.
I think one of the hard things is really like establishing initial connections and then I think if you figure that out clearly then you can do a lot of stuff.

Adam Ficsor: 01:26:08

Yeah exactly and you don't even have to...
That Bitcoin address as far as I understand the cryptography can be reused for any other purpose because you are just encrypting a message that can be decrypted by whoever owns the private key.
So based on that message that you encrypt, It's a question.
You cannot figure out which Bitcoin address you are encrypting a message to.
Is that correct?

Tim Ruffing: 01:26:42

There are encryption schemes where you just from the encrypted message, you don't see for which public key it's encrypted.

Adam Ficsor: 01:26:52

Yeah.
Is that what's being used in Taproot?

Tim Ruffing: 01:27:00

Well, yeah.
So I mean, Taproot doesn't use encryption, right?
But like,

Adam Ficsor: 01:27:05

Okay.
Elliptic curve, right?

Tim Ruffing: 01:27:07

Right.
So, the public keys are elliptic curve keys, and there are elliptic curve encryption schemes where you can't tell for which public key ciphertext is.
So that exists.
I think you still need to do something because now, well, it depends.
Depends on how many messages you get, right?
Because if you can't easily tell from the message that it's for you, you need to try to decrypt every message just to figure out if it's for you and this can be expensive.

Adam Ficsor: 01:27:53

Yes, exactly, but it's not a problem because you know when the message is coming.
So at that point of time, you start listening to that.

Tim Ruffing: 01:28:04

You're right, it's actually easier as for example in Monero, they have a similar model, right?
Basically, you have to look at every transaction on the blockchain and try to receive it, because you don't know if it's a transaction for you or not.
But here it's a little bit different, right?
Because you only need to listen at that point in time.
It's a good point.

Adam Ficsor: 01:28:34

Anyway, we'll get back to this idea after Taproot is deployed.

Tim Ruffing: 01:28:39

Right, yeah.
Ten years later?
No.

Adam Ficsor: 01:28:42

You know what's interesting?
In your CoinShuffle paper, or CoinShuffle++ paper, I don't know.
In one of the paper, I think the CoinShuffle 2014, even that was talking about Segwit.
