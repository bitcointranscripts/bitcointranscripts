---
title: CoinShuffle
transcript_by: realdezzy via review.btctranscripts.com
media: https://www.youtube.com/watch?v=dVZDeEfSdcI
tags:
  - research
  - coinjoin
speakers:
  - Aviv Milner
  - Adam Fiscor
  - Lucas Ontivero
  - Max Hillebrand
date: 2020-01-20
summary: CoinShuffle is a decentralized coinjoin protocol that aims to address the privacy and centralization issues of traditional coinjoins. Participants can anonymously submit their addresses in a process that uses encryption to prevent linking the addresses to specific individuals. The addresses are then shuffled using secure multi-party computation, creating coinjoin outputs that include inputs from all participants. CoinShuffle eliminates the need for a central coordinator and is resilient to denial of service attacks. However, the decryption process is sequential and the time cost increases with the number of participants. The protocol also has measures to handle misbehaving participants and failed rounds. Additionally, alternative approaches such as using mixnets and integrating with other infrastructures like the Lightning Network are discussed. Overall, CoinShuffle provides a viable solution for decentralized and coordinated coinjoins, but the performance is dependent on the number of participants. Further we discuss the importance of integrating second layer technologies like the Lightning Network in a private way and the challenges of achieving efficiency in coin mixing. They propose steps to improve the space efficiency of coin mixing and finding algorithms that perform well in simulations. They also explore the trade-off between space efficiency and privacy, suggesting that higher coin denominations could be more efficient and private. They discuss the idea of using existing data to simulate mixing transactions and score mixes based on real-world data. They also mention the possibility of using the knapsack algorithm for scoring and discuss the challenge of arranging inputs and outputs in a trustless manner. The speakers plan to explore different mixing networks and techniques, such as cache fusion, to improve coordination and trustlessness.
aliases:
  - /wasabi/research-club/coinshuffle/
---
## Introduction to CoinShuffle

Aviv Milner: 00:00:00

Today we're talking about CoinShuffle, practical decentralized coin mixing for Bitcoin.
So, let's get started.
So we're looking at a 2014 paper by Ruffing, Moreno-Sanchez, and Kate.
Everything is obviously posted on GitHub.
Here is the paper itself.

Last week, just a reminder, we talked about SNICKER CoinJoin, and the summary was that we can have a non-interactive CoinJoin between two participants if the proposer, if one of the two participants assumes likely UTXOs, tweaks a revealed public key with a Diffie-Hellman shared secret, and then takes this partially signed Bitcoin transaction and broadcasts it to a public forum where the other participants may sign it when they see it.
So essentially we talked about non-interactive CoinJoins.

So far we've talked about Knapsack CoinJoins, SNICKER, today's CoinShuffle, and then next week's will be decided at the end of this call.
You can find out everything on our Wasabi Research Club github.

Okay, so we're going to reintroduce last week's topic, which is the problem with current CoinJoins.
So the problem that we talked about last week, we're talking about this week as well, is that they require coordination.
So last week it was more about interactivity, this week it's about coordination.
So coordination is potentially a problem because of things like privacy or the fact that the coordinator becomes a central point of failure.
So the question today is gonna be, can we create CoinJoins without coordination?
Just like last time, we talked about what it would take to create a CoinJoin and really it comes down to knowing the inputs, the outputs and the signatures.
Now if we think deeply about this, it's not just about knowing inputs, outputs, and signatures.
You know, inputs and outputs, change outputs, aren't necessarily anonymous, so participants can declare their inputs and declare their change outputs.
But we also have to find out all of the participants' mixed outputs, so their anonymous outputs.
And we need to find this out without having them reveal the link between their outputs and the fact that they belong in the CoinJoin.

So if we look at how Wasabi does this with a coordinator, well, Wasabi uses what's called secure multi-party computation, or essentially just Schnorr signatures, Schnorrian blind signing of outputs in order to allow for outputs to be anonymously submitted.
So users, for example, will register their inputs and they'll have a blinded output signed by the server, at which point later they will submit the unblinded output to the coordinator and the coordinator doesn't know who is the person that submitted the output, only that that person is valid because the coordinator did a blind signing of the output.
Okay, so CoinShuffle in summary is just Wasabi without the coordinator.
So using Dissent protocol for communicating anonymous outputs by participants, and we'll look at that briefly and then, there are no questions so far, right?
Or comments?

Lucas Ontivero: 00:03:43

No.

## CoinShuffle breakdown and illustration

Aviv Milner: 00:03:45

Okay.
So, CoinShuffle.
So we can imagine six participants.
In particular, we want to imagine an ordered set of six participants.
So we'll have that the left, the red individual is the first, and the last participant is the purple, and there's all the participants in-between.
Just for the purpose of illustration, it's easier if they're colorful.
Essentially what we want to do is that these participants, they want to submit their inputs, they want to submit their change outputs, but they also want to submit a blinded output, an output that no one, that is completely anonymous to the rest of the participants.
And they want to do this without a coordinator that is essentially controlling how this goes.
So essentially what you have here is what the CoinJoin will look like at the end, is it should look like a bunch of inputs from all six participants, some change outputs and some outputs that are equal size that we don't know who they belong to.
So we have six ordered participants and we have an anonymous CoinJoin output.
So it's trivial to get the change outputs done and the inputs done because those can be linked together And participants don't have to hide the fact that they are the ones submitting that information.
Now we're going to see how a participant, in this case, is going to anonymously submit an anonymous output.
So in this case what we have is we have the first participant is the red participant.
So if you look at this colorful little blob in the very middle is the red address.
Okay, that's like the unencrypted red address is right in the center there.
And then what the red participants going to do is that person is going to encrypt that red address against purple's public key and take that encrypted data and encrypt it against blue's public key and so forth and then that data is encrypted against green's public key and so forth and so what you have and this is familiar to some of you, it's like an onion, right?
So it's a layered encryption.
So it's encrypted against purple, blue, green, yellow, orange.
So then red will take this blob and pass it to the next person in line, which in this case is orange, right?
Now orange will decrypt one layer because orange, it holds the orange public key.
So orange can decrypt the layer from red's address and simultaneously add orange's address, also encrypted in the same onion scheme being encrypted first against the purple key, then the blue, then the green, and then lastly, the yellow.
And now that Orange has two blobs to pass on to the next individual, Orange is gonna shuffle them.
So, you know, just like this.
And again, Yellow now is going to submit his own address, unwrap the two layers of Yellow on the orange and the red.
And then again, encrypt everything so that it's layered against the next three participants and shuffle and send over to the next layer.
And so, you know, things repeat over and over again.
And finally, what happens is that purple, who's the last individual has all of the addresses and can decode all of them, but has no idea who they belong to.
So from the perspective of purple, only purple address is known to be to belong to it.
Every other address belongs to someone else and it's not clear who.
So from orange's perspective, you know, only the orange address is known.
The other five addresses are completely a mystery.
And from yellow, it's the same idea.
And from red.

Adam Fiscor: 00:07:38

Can you just go back because I think it's incorrect.
Yes go back like two more or something.
Yes, so you see, right now, yellow only has three outputs.
Three onion encrypted stuff, but actually it's everyone broadcast.
Oh, okay, sorry.
Go ahead.
I know it's incorrect, but I can't explain it.
I will come back to it.

Aviv Milner: 00:08:26

Yeah, so it definitely can be incorrect.
I don't claim that I'm 100 percent, but I think the idea overall, or the aim is so that all participants in an ordered fashion can submit their addresses and not have the address linked to them.
And it's done exactly in this sort of way.

Adam Fiscor: 00:08:52

I got it.

Lucas Ontivero: 00:08:54

I think what Aviv is telling us is correct, because that's the same that I understood when I read the paper.
Everyone, I mean, you decrypt the previous participants with your private key because the message was encrypted with your public key because previously there is an announcement phase where all the participants share their public keys.
So in this order, you create this onion layers, right?
And is that how Aviv is telling us now?
I think it's correct.

Adam Fiscor: 00:09:41

Okay, so let me explain what is incorrect about this.
Is that, as you said, first announcement, announcing the public key.
So everyone here, Aviv, Igor, Lucas, Max, O, I don't know if you want pseudonym or real name, Sorry, Rafael and me.
So everyone announces his own public key and everyone has to think of a message or an output, a Bitcoin address.
And we have to encrypt that Bitcoin address.
Everyone has to encrypt it in a specific order.
So first to Aviv, then to Igor, then to Lucas and so on.
And then we broadcast all the encrypted messages.
So that's how you can shuffle them.
That's what is shuffled.

Lucas Ontivero: 00:10:45

Well, no.
No. What I understood is what Aviv is saying.
It is in order, yes, and the message is passing one by one and everybody decrypts the coins with their public keys, shuffles the encrypted addresses, yes, and pass that to the next one.
So, in the end, the latest one, the latest participant, the one in the final step, can finally decrypt all the addresses, except of course, the one that belong to him.

Adam Fiscor: 00:11:46

Ok so i think it's correct and there might be only a misunderstanding.
Aviv can you go back to red?
At this point, go to the next one.
At this point, Orange only has two or has all the encrypted messages.

Aviv Milner: 00:12:15

Only two.

Adam Fiscor: 00:12:18

No, that's what's incorrect.
Orange has all the encrypted messages.
Everyone encrypts their message in a specific order and broadcasts all the messages.
Red starts decrypting the layer, the upper layer of the messages and shuffles it.
Then orange starts decrypting his layer and shuffles.
So all the messages, right?
Everyone has all the messages all the encrypted messages that's the point.

Aviv Milner: 00:12:56

It actually seems like what Adam is saying makes a lot of sense So there's no reason why everyone couldn't submit all of their addresses like the way Red did it.

Adam Fiscor: 00:13:16

And that's how you can put it into a peer-to-peer network where everyone broadcasts every message.
It's not really passing along.
Maybe it can be, but it's not really passing around the messages from peer-to-peer, but broadcasts all the messages for everyone all the time.

Aviv Milner: 00:13:39

I did think that it was sequential in that red had to communicate to orange and orange had to communicate to yellow and yellow had to communicate to green.
And that it wasn't like, I mean, I guess you could do it publicly because you can keep announcing everything and only the right person can decrypt that layer.
But I did think that it was sequential.

Adam Fiscor: 00:14:06

I mean, just think about it.
What if red, because in this case red doesn't shuffle anything, then red cannot make sure that the things are shuffled correctly.
Right, orange can only partially make sure that two thing is shuffled.
Now I actually wrote code for it, so I'm pretty sure what I'm saying.
Anyway, can we agree in this or someone would like to have objection?

Aviv Milner: 00:14:40

I'm very happy to concede this because I think that the points is the same, that the goal is the same, is that these peers want to essentially mix these outputs and not have connection between who submitted what, right?

Adam Fiscor: 00:14:56

All right, let's move on then.

Aviv Milner: 00:15:14

So the summary is here as well, but the summary of what happened is that six participants got together and are essentially submitting their anonymous addresses outputs in such a way where when Purple finally opens all six addresses, Purple can't link those addresses to any of the past participants.
And it's done with like onion-layered encryption and shuffling.
So those outputs are shuffled across participants.
Adam says that all six addresses are shuffled with every single step, and that could very well be the case.
But at the end, you have six addresses that are unlinked.
So here is the, in the paper it's explained.
So you can see in the top right, Alice has this layered encryption and she passes off to Bob who decrypts, who passes it off to Charlie, decrypts and you can see this sort of mixed network.
Yeah and on the bottom left you have a CoinJoin that's been signed, on the bottom right you have a CoinJoin that's not been signed because someone tampered with the addresses and added an invalid address to the CoinJoin.
So the big thing to talk about with CoinJoin...

Adam Fiscor: 00:16:54

Sorry Aviv, can I show my code that maybe you understand it better based on that?
I am sharing my screen, right?

Aviv Milner: 00:17:23

Okay.

Adam Fiscor: 00:17:24

Do you see it?

Max Hillebrand: 00:17:27

Yeah.

Adam Fiscor: 00:17:28

Okay, then it's a problem because it's not in the video, just like last time I had to cut it out.
And anyway, very quickly, then we have Oli's, Bob and Satoshi, and everyone broadcasts their public keys.
I run this and it's going to be, this comes out.
So everyone broadcasts their public key And then these onions, these are the encrypted messages, encrypted for everyone.
And then everyone starts to decrypt their messages one by one.
Everyone starts to decrypt all the messages, all the layers, and at the end we get a script like a Bitcoin script, right?
That's the Bitcoin address it's just `scriptPubKey` and not Bitcoin address so anyway if you see that yeah it works okay I don't want to ruin the video with this so go ahead.

Aviv Milner: 00:18:51

Okay well pretty much at the end here, the big concern, right, when you consider getting rid of a central coordinator and instead having peers doing this process themselves is the time it will take and the computation it will take from the peers.
So in the CoinShuffle paper, they took participants and set them up on a local network and then on a global network with a certain amount of latency from one side of the network to the other side of the network.
And here you can see the time it takes.
So if you look at the local network, where there's almost no latency, it looks like a linear increase in the time it takes.
With 50 participants, you have 30 seconds, 40 seconds of time it takes for, essentially the participants to do the entire dance from start to finish.
And then with the global network, you can see that the time it takes is much, much more because every single individual needs to hear the latest state and then decrypt that situation and then pass it on to the next individual who will, who needs to then, so it is sequential whether individuals are talking directly to each other or in public broadcasting to everyone, it's still the case that these onions have to be decrypted in a sequential way.
So the more participants you have, the more time it takes.
And on the right, there is the average processing time per node.
And We also have descent, which is what this is based on.
They also did a similar test of the shuffle time for 44 nodes with varying size.
Here, it's one megabyte of data, of encrypted data that's being shuffled over 44 nodes.
You can see it takes several minutes, so 15 minutes by 44 nodes.
And over here it was three minutes by 40 or 50 participants.
So yeah, in summary, rather than have a secure multi-party computation with a coordinator, CoinShuffle aims to solve the problem of constructing a CoinJoin with just participants themselves.
Using the Dissent messaging protocol, CoinShuffle participants shuffle their anonymous outputs until all outputs are made available to all participants without a link from any participant to an output.
And the biggest drawback is the time cost as the number of participants grows and then the advantage is that there's no coordinator to attack, do a denial of service.
That's pretty much what I think needs to be said about this so yeah we'll leave it at that.

## Questions

Adam Fiscor: 00:21:52

Thank you Aviv.
Let's continue with questions and discussions and then ideas and at the later on topic for next week.
So yeah, who has questions?

Lucas Ontivero: 00:22:11

I have a comment.
Well, first of all, I think I don't know what your implementation is based on.
Probably it's in a new version that we don't know.
But I understood the same that Aviv explained to us.
And in fact, there is a very simplified version or very simplified explanation in BitcoinTalk about it by Tim, one of the creators of this scheme.
I understand the same whatever I read it but anyway that's one point.

Adam Fiscor: 00:22:57

If red doesn't have all the onions then who's gonna decrypt his onions for other people?

Lucas Ontivero: 00:23:17

No Alice in this case the red, doesn't decrypt, he only encrypts the output, right?
Encrypts the output with all the public keys of the other participants in order.
So the next one, in this case the orange one, decrypts with his public key.
It remove one layer, yes, and just encrypt everything again.
The latest layer is the yellow one, right?
So yellow, decrypt remove that layer, mix those addresses and encrypt again with, yes, this is what Aviv is doing.
So in the end, all the addresses has only one layer of encryption that is the one belonging to that guy, the purple, I think.
Okay, so purple decrypts all the addresses, yes, except the one that belongs to him, and performs just the latest shuffle and broadcasts that list of outputs to everyone.
So, after that, the next step is creating the transaction so nobody knows what output belong to the rest.

Adam Fiscor: 00:25:12

I see okay maybe then I don't know it.
I didn't understand it properly then.
Because of course both schemes work.
I mean, I know that my scheme is working.
And now that you explained what you're doing, it seems to me that's working too.
And that results in less encryption and decryption.
So less network messages, maybe it's faster.
So, yeah, okay.
Yeah, I think you're right.
All right.

### Idea for a change on this scheme

Lucas Ontivero: 00:26:00

I have an idea here for this scheme, because if in the first phase, I mean in the announcement phase, participants could announce their public keys and also how much money they want to participate with, for example Alice can say this is my public key and I want to participate with one Bitcoin, Bob, this is my public key and I want to participate with 0.83 bitcoins.

Adam Fiscor: 00:26:37

They have to announce their inputs with their public keys.

Lucas Ontivero: 00:26:42

Yes, but my idea is changing the protocol just a bit, right?
Because if everybody knows the public keys and the amounts that other participants want to participate with, then what participants can do is creating the outputs, not only the addresses but also the amount of that addresses using the snapshots, right?
Because remember that was one of the ideas that the latest proposal that was never published by, I don't remember the name of the guy that was with us in the Knapsack episode.
He said, there is a new version that I never published that is the participants only need to know the amounts of the other participants so they can split their outputs in such a way that they can create a Knapsack transaction, right?
So in that way, we could encrypt more than one address but also the amount.
So you don't need to shuffle, right?
Because the idea of, oh, well, yes, you need to shuffle.
So you can shuffle, but in the end, what the purple guy will receive is a lot of output transactions, yes, with not only the script, but also the amount, and that will be a Knapsack transaction.
So it could be used for unequal outputs too, using what we learned in the first episode

Adam Fiscor: 00:28:40

I think that's a very important idea that's a good job Lucas seriously.

Lucas Ontivero: 00:28:49

Thank you.

Adam Fiscor: 00:28:53

So, anyone have questions or should I go with mine?
Okay, Aviv.

Max Hillebrand: 00:29:00

One general question.
Okay, go ahead, Aviv.

Aviv Milner: 00:29:10

No, you ask your question first.

### How to defend against sybil attacks

Max Hillebrand: 00:29:16

Okay, it was a general question about denial of service or other sybil attacks.
I mean we can use a central coordinator to ban UTXOs and we have a fee to have economic disincentives to sybil attacks, but there are no signatures in coinbase.
So how can we defend against sybil attacks?

Aviv Milner: 00:29:38

So that's a really great question.
It's addressed in the paper and in the protocol itself.
So the phases, you know, there's the first phase is the announcement phase, then there's the shuffling phase.
What happens later is that if after the shuffling phase, if you get to an undesired outcome, namely, the addresses that are appearing are not belonging to all the participants.
You know, someone added two addresses or someone didn't shuffle correctly.
There is a way to go through the blame phase where essentially all the participants reenact what they did and you can tell if someone did something bad.
So you can do blame but that also takes time and it's arguable that it's easier to attack this sort of system than a Wasabi coordinator.

Adam Fiscor: 00:30:36

Can I rephrase your answer?
It was correct.
I just want maybe easier to say this way that if someone misbehaves that obviously everyone detects it because the final CoinJoin doesn't happen.
So everyone just exposes all the actions that they take except their outputs, except their Bitcoin addresses.
So, and the protocol can run, because If you give out all the actions that you take during the run of the protocol to everyone that, hey, here is my private key, for example, I signed my messages with this, then you can tell exactly who misbehaved and you can rule him out and you can run the protocol with the remaining honest participants.
This is something that was a little bit unhelpful.

Lucas Ontivero: 00:31:40

I have a comment Because that's right, in fact there is some advanced techniques in the other paper, I think it is the CoinShuffle++ that I'm not familiar with yet.
But listen, sybil attacks are hard to prevent in conjoin, right?
It's really hard, right?
Now because in this case, for example, if you are one guy that participated with multiple identities, let's say.
Imagine I am red and you are orange, yellow, light blue, and blah, blah, blah.
So there is nothing I can do.
Yes, but denial of service attacks can be, I mean, I think it's a naive alternative but it works pretty well.
That is, okay, someone didn't sign the transaction, right?
It is easy to see, to know that.
So, you can just ban that coin, as we do, and try again.
Sooner or later, That guy will run out of money and probably is not the best, right?

Adam Fiscor: 00:33:06

That doesn't work, Lucas.

Lucas Ontivero: 00:33:08

Why?

Adam Fiscor: 00:33:10

Let's think about what if Purple just switches one of the addresses of the outputs.
Max, I cannot hear anything, sorry.

Lucas Ontivero: 00:33:57

Max, do you have some software or feature that mutes you when you are not speaking or something like that because I see that you are muting and unmuting and in high frequency.

Adam Fiscor: 00:34:22

Anyway, Lucas, can you reply to my question?

Lucas Ontivero: 00:34:28

Sorry, I didn't hear your question.
Can you repeat please?

### How dishonest participants are figured out/punished

Adam Fiscor: 00:34:35

What if purple, the last one, changes the address, changes let's say red's address to his own address, then it's going to be red who doesn't sign.
So you cannot really ban red, right?

Lucas Ontivero: 00:34:53

No, wait, but I can see the transaction, right?
The final CoinJoin transaction has, in this case, one, two, three, four, five, six.
There are six participants.
Let's say there are six inputs too, just to simplify, and there is one missing signature.
So someone didn't sign, right?
So in that case, we can ban that coin so you can participate again but not with the same coin.

Aviv Milner: 00:35:32

So in this protocol unfortunately you can't apply the same banning heuristics as with Wasabi.
So with Wasabi you can ban the coin that did not sign.
In this protocol, if you end up with an unsigned CoinJoin, there are two reasons.
Either someone is not signing on purpose, in which case you can ban the coin they did not sign or someone did the protocol wrong.
In the case Adam gave, Purple is the last person with all of the addresses and Purple dumps Red's address and adds two of Purple's addresses to the mixed outputs.
So how do you know that happened?

Lucas Ontivero: 00:36:22

Sorry, yes, I understand now.

Aviv Milner: 00:36:27

So what you have to do in that case, it's actually quite unfortunate, is that every person has to reveal to the entire group what information they received and what they encrypted and what they decrypted.
And by doing this, the guilty party will be revealed.
But the annoying part is that this also takes several minutes of everyone sort of presenting what they have.
And then you have to recursively go through and see which person you know tampered with the information and if you can waste three minutes of time then you know arguably it's a privy to DOS attack.

Lucas Ontivero: 00:37:19

Yes, it's clear now.
Yes, sorry, it was a silly question.
But anyway, remember what Adam Gibson tell us, right?
The denial of service attacks is because someone wants to prevent this from happening and there is not incentive because you cannot steal money.
So if there is a denial of service attack, I mean there are no incentives at the beginning at least for this kind of attacks.
So, A naive implementation can work at the beginning of that list.
I mean an implementation that doesn't implement any denial of service attacks prevention mechanism.

Aviv Milner: 00:38:17

So the point is that with this protocol, you do have a blame phase and you can point out the guilty party, it's just it takes additional time.
So all I'm going to say is that looking at the trade-offs of this protocol, as soon as we start talking about large number of participants, more than 50, we're going to have pretty severe problems with latency.
And I think there's an issue where the longer it takes for a round to happen, the more likely someone is to lose connection or be a part of the problem.
So I think it's just not practical to do CoinJoins this way.

## Difference between CoinShuffle and Wasabi

Adam Fiscor: 00:39:00

One more thing that's interesting in this is that here, the DOS protection, so here the CoinJoin happens between the honest participants.
In Wasabi, We always forget the state.
We take down the required anonymity set, but anyone can register to that, not only those who were already registered in the previous failing round.
I'm not sure which direction is the good, but this might be something that we can consider later on.
Any thoughts on this?

Aviv Milner: 00:39:47

Can you say that again?
I don't think I understood.

Adam Fiscor: 00:39:51

Sorry.
Yeah, I was not clear enough.
So here, if a round fails, then the next round is going to happen between the participants without the malicious party.
In Wasabi, if a round fails, then the next round, the anonymity set required anonymity set will be lowered, but Wasabi doesn't make sure that those people who were in the failing previous round, the honest people from the failing previous round will mix.
Do you understand the difference?
It's a subtle nuanced one but it's somewhat important.

Aviv Milner: 00:40:45

I want to say yes but I honestly don't think I understood.

Adam Fiscor: 00:40:51

Okay, so there is a round Wasabi CoinJoin, Wasabi or CoinShuffle doesn't matter the round fails what happens in CoinShuffle?
The same participants will CoinJoin.
It is CoinShuffle.
In Wasabi it's not the same participants.
Wasabi just lowers the required number with the number of malicious participants but still in that round anyone can register.

Aviv Milner: 00:41:32

Okay so two things about that then.
So firstly, CoinShuffle, if a CoinShuffle round fails, it goes through the blame phase, it points out someone to blame, and then it does a CoinJoin, another CoinShuffle without that participant that's what I understood.

Adam Fiscor: 00:41:53

Yes, exactly.

Aviv Milner: 00:41:53

And in terms of Wasabi, I thought Wasabi was you know if a CoinJoin fails It's because someone didn't sign and that one coin that didn't sign is banned for example and all the coins try again minus that one coin.
So I guess I'm confused on both issues.

Adam Fiscor: 00:42:15

You are right except the end that not all the coins who already registered it's not those who are redoing the exact same failing round without the malicious person but it's a completely new round anyone can come the malicious person is banned but any new coin can come in, in CoinShuffle new coin cannot come in okay

Aviv Milner: 00:42:52

okay so that that I had that I understand and I didn't know that was the case and it's a bit, yeah, it's a very small detail but yeah, I guess it's important.

Adam Fiscor: 00:43:09

All right, next question.
What is secure multiparty computation?

Aviv Milner: 00:43:21

Is that for me?
Because I can just read a Wikipedia definition.

Adam Fiscor: 00:43:24

No, it's a question for the author.
Next time when Coinshuffle++ will be.
Okay, so one more thing that Since we are comparing it to Wasabi, there is a comment.
Or actually it's not even a comment.
Anyway, I'm just going to read it.
I'm not sure if it's from the paper or it's a comment from BitcoinTalks.
So, Maxwell sketches a modification to the CoinJoin protocol using blind signatures to avoid the problem of a centralized mix learning the relation between input and output addresses.
This is the Chaumian CoinJoin, just saying, and yes, it's in the paper now, I know.
This protocol employs the Anonymous Communication Network, TOR, as a building block to provide unlinkability.
In contrast, Coinshuffle provides full resistance against traffic correlation attacks by using a decentralized high latency mix network run only by the participants.
So that's an important point here too, right?
That Wasabi relies on new TOR identities, Coinshuffle does not.
It's doing a mix.
You could even f**king mix without TOR, just on the clear net, right?
It would still work.

Aviv Milner: 00:45:06

That seems pretty important and I definitely missed it.

Max Hillebrand: 00:45:10

But actually, I mean I was giggling when I read the paper and the shout out to Zerolink.
But then the question that I have is I mean we could also do ZeroLink not on Tor but on a mixnet would that work too?

Adam Fiscor: 00:45:26

Bear in mind that all the CoinShuffle implementations are actually using a server and you know in theory you can use just a bulletin board server where participants are posting their messages but they are actually using for coordination and host protection and things like that I think.
So yes, you can say that CoinShuffle is wasabi without TOR and you know what I mean.
So yes, definitely, but then you will call it CoinShuffle because CoinShuffle is using a mixnet, that's the thing about it.

Aviv Milner: 00:46:23

Well, I guess the important thing to note is that CoinShuffle doesn't make any claims about how we structure CoinJoins, rather just how we communicate, right?

Lucas Ontivero: 00:46:36

Okay, sorry.
Anyway, I understand what you say.

## Combining Knapsack with CoinShuffle

Max Hillebrand: 00:46:40

We kind of spoke about this already.
Maybe a bit further to discuss how we can combine Knapsack with this.
So I'm not sure I understood the conversation we had earlier.
So would it be that we first do a communication round with CoinShuffle and then we get this CoinJoin transaction and then we apply Knapsack to this CoinJoin transaction or how exactly would that work?

Lucas Ontivero: 00:47:21

Well, Knapsack works by splitting the outputs depending on the amount of the other participants, right?
So, if you know how much the other participants are participating with, you can split your output in such a way that after the process, I mean, you do exactly the same that Aviv explained us, but in the end, the purple guy will decrypt all the outputs, right?
And those outputs, when you analyze those outputs, there will be more than one trivial mapping to the inputs, right?
So, it is basically a knapsack transaction.
Is it clear?

Adam Fiscor: 00:48:30

Wouldn't that lead to like spam in the chain?
Too many UTXOs or would there be like some kind of minimal amount?
Minimum amount for one UTXO.

Aviv Milner: 00:48:46

That's the trade off with the knapsack is that, yeah, the better the knapsack, the more UTXOs you need.

Lucas Ontivero: 00:49:01

Okay, going back to the comment, to what Adam said, yeah, I mean, it is possible to use the same technology that in DC networks, I mean, using XOR, using the XOR of XORing all the messages with all the public keys of all the participants.
And in that case, we could remove Tor.
The only problem is that we still will be able to see the IP addresses.
Something that we thought we cannot do.
So, the server will not be able to know who message belongs to whom, right?
But the IP address is still there.

Adam Fiscor: 00:50:00

Oh, that's a very good point because in Wasabi the server doesn't know that if someone registers to the CoinJoin, did he used Wasabi before or not.
The server doesn't know because it's on a new Tor stream.
But with CoinShuffle, if you don't use Tor, then you can tell that which participants, which person participated in which CoinJoins.
So now you can correlate.
So you actually have to use TOR for CoinShuffle.

Lucas Ontivero: 00:50:47

Yes, that's my point.

Adam Fiscor: 00:50:53

Okay, I only have one discussion thing or rather interesting thing regarding CoinShuffle is that, I don't know if you guys knew it, but on BitcoinTalk the very first page of conversation was about a replay attack And then Tim Ruffing noted that the thing about encryption schemes is that all secure encryption schemes always use randomness for encryption to make sure that encrypting the same message twice does not yield the same ciphertext.
The odd randomness is built in the encryption algorithm itself.
One does not have to add randomness manually to a message before giving it to the algorithm.
Try it, take an encryption tool and try to encrypt the same message twice.
So anyway, it's just good to know.
So do you guys have any presentations, questions, discussions, ideas?
Or should I move on to something more interesting?

Lucas Ontivero: 00:52:24

I have no idea or question just something that we could have in mind that could improve our CoinJoin transaction is researching if is there any way to identify the offender in order to remove it and create a new conjoin without that attacker, that could be great.
I think it's not possible, but it could be good to, if we can say, okay, someone didn't sign, provide proof of something, just to avoid creating a new round again.
So that would be really good.

## Wasabi Research Club roadmap

Adam Fiscor: 00:53:17

I think it's possible, I think it can be done and not even hard, but I'm not sure it makes sense, because Then what's the attack?
The attack is that the sybil comes, the malicious sybil comes and tries to...
I don't know.
It's an interesting question to explore definitely.
All right.
So, before we would get into the next topic, I want to talk about something, is that what direction should this research club take.
Now I want to talk about just an idea of how should we, how can we make, What's the most, what's the best thing to research in Bitcoin privacy?
And I have a small roadmap-ish thing and we could adjust the researches to that later on.
Right now we will, of course, as we discussed, we will go through the CoinShuffle line, but after that.
So please, opinion, It's something that I've been thinking about for a year now and it's getting more and more solid based on the opinions, but I would like to hear yours too and adjust it.

So this is the roadmap to Bitcoin privacy.
Very first thing to do is to figure out the most block space efficient way of mixing coins.
Second thing to do is to figure out how to send money in a mix instead of mixing to yourself.
The third thing to do is after these things are figured out, we have to figure out how to do it trustlessly.
Fourth thing to do is figure out how to do it in a decentralized way, which I am not interested in, but for completeness, this is something that people might be interested in.
And the fifth thing to do is figure out how to integrate other infrastructures into this new mixing technology that's just being researched.
What are these infrastructures?
Those are relevant.
Light clients, how to do it with a light client, how to do it on mobile, how to do it with hardware wallets, and are there any ways to integrate it to the lightning network somehow and rolling to the lightning network or something like this.
So figure out the most block space efficient way of mixing, figure out how to send in a mix instead of mixing to self, figure out how to do it trustlessly.
This three step is what the Wasabi Research Club should be about.
The integrations and later things are, I don't know, it's 10 years down the line or 20.
So do you guys agree that This is a logical sequence of research that we could take later on when we learn more things.

Aviv Milner: 00:57:30

I definetly agree.
It might be a good idea to start talking about how we would measure efficiency in a CoinJoin, against the block space that it's consuming.
I've been thinking a lot, I don't know if we have time right now to talk about like the perfect...

Adam Fiscor: 00:57:54

This would be my next topic to be honest, that I have sub steps for the very first step.
So I don't know, should I say the sub steps or do you want to say what you are saying right now?

Aviv Milner: 00:58:11

Yeah, I mean, I'll just say what I've been thinking about because you know we're all thinking about privacy right now.
When I think about the perfect privacy on Bitcoin given what Bitcoin allows barring layer two solutions, To me that perfect solution is essentially, you know, every block contains one transaction and all inputs and outputs from all transactions are collapsed into a single transaction.
And then there are some optimization happening where people are breaking down their inputs and they have common outputs of similar size and then there's knapsacking and all sorts of fancy stuff.
But the idea is that the asymptote of privacy, the best place privacy can go, this is an intuition, I could be completely wrong about this, is just every single block is just these massive transactions, that's where I think things would be going.
And so that kinda points to what Adam was saying about how to figure out how to send in a CoinJoin as well, because that means that if you can receive and send and mix all in one CoinJoin, then all transactions could be CoinJoins in the future.

Adam Fiscor: 00:59:31

So yeah, we will probably never get there or not probably we definitely never get there but it's it's a good idea to take imagine what could be the perfect at the best that that's possible and start to work backwards from there.
Yeah, that's good.
Do you guys see the logic between these three steps?
That most efficient way of mixing, send in a mix and then do it trustlessly.
Does it make sense?
I really would like some feedback.

Max Hillebrand: 01:00:25

Yes, I think that's a nice idea.
Especially though also, as you mentioned later, with other technologies like for example Lightning Network, I think an important aspect here is to integrate getting into second layers and out of in a private way.
So doing, you know, CoinJoins into a Lightning Channel factory, for example, or doing hyper loops, you know, atomic swaps out of the Lightning Network in a CoinJoin.
But this somewhat goes together with sending and receiving within a CoinJoin.
Though not just into a single public key, but more advanced second layer script.

Adam Fiscor: 01:01:04

So the reason is why the Lightning Network integration is at the very very end, because everything depends on the CoinJoin scheme.
So first you really have to figure out how to do on-chain transactions and then you can move on to Lightning Network.
Anyway, the very first step is figure out the most block space efficient way of mixing coins and This is my thinking.
There are two steps here.
First, we have to figure out how to score mixes and second, since finding the maximum score based on the set of inputs is computationally infeasible, an algorithm must be found that performs the best in multiple simulations.

## Privacy vs Space efficiency

Lucas Ontivero: 01:01:58

Okay, sorry, you asked for feedback.
I not totally agree, because I know that your goal has been your goal for probably years, right?
I mean, finding the most space efficient way to make this, to build this conjoin transactions, but I will say that our goal should be the most private way to create the conjoin transactions, (which) probably it is more expensive.
But I think the first filter or the first goal should be to maximize the privacy, even when probably it's not the most space efficient solution.
Just that.

Adam Fiscor: 01:02:57

That is obvious what provides the most privacy.
If you know the common greatest divisor, you have a set of inputs, you get the common greatest divisor of them and every output gets that, right?
Or let's say one Satoshi, but rather the common greatest divisor.
So that provides the best privacy.
But this is an optimization problem.
The best privacy while not wasting that much block space so you know

Lucas Ontivero: 01:03:41

Yes that's clear it's exactly the same that I thought when you say it is obvious.
Yes, it is obvious.
But I mean, we have to have like a minimum requirement, right?
We cannot worsen the privacy level that we have now.

The problem is it's not easy to know what our users want, right?
They sometimes want to be able to mix more money and faster.
Sometimes they want to be able to participate with less money, it's not easy, yes?
So probably it could be more efficient, space efficient to mix higher coins, right?
For example, instead of now we are using 0.1, 0.2, 0.4, of course it would be more private to split all in 0.1 coins, right?
But I don't know if trying to achieve a more space efficient solution, if that will not require to mix bigger coins I mean to have bigger outputs.

Adam Fiscor: 01:05:31

We are on the same page here, Lucas.
I understand what you're saying.

Adam Fiscor: 01:05:40

I just have a roadmap to how to get there.
My idea is that we take the existing data, the existing Wasabi data of what happened with Wasabi, what amounts people are coming in a mix, or just existing blockchain data.
The point is that you build a software that makes this simulation.
And when I say the first step is how to score mixes, what I actually mean is to figure out how to score a chain of mix.

Step one figure out how to score one mix and Step two figure out how to score a chain of mix based on real world world data simulation.
So right now we are just scoring, we are not really mixing, we put some naive mixing algorithm and we try to figure out, we see a transaction chain of, mixed transaction chain, and we try to figure out how the hell should we score that mix.
And then we say, okay, let's use Knapsack for that.
And we run Knapsack for the exact same data that we run our previous naive mix and then we compare our scores that hey, did Knapsack score better or the previous naive mix score better.
Does that make sense for you?

Lucas Ontivero: 01:07:22

Yes, it makes sense.
It is backtesting basically with different algorithm.
The only thing that we have to have in mind probably is that given we mix 0.1 at a time, yes, basically, yes, people with a lot of money, I don't know, probably 1000 bitcoins, it's not currently mixing with with wasabi probably, yes, because it will take if they want to make it right, it will take a lot.
So probably what we see in our conjoin transactions, that information is already constrained by our outputs, right?
That's just what's a common.

Adam Fiscor: 01:08:21

That's something we have to figure out implementation time that Should we take the wasabi real-world data or should we look at instead wasabi mixed data instead?
Should we look at the input amounts on the blockchain just randomly.
Yeah that's a methodology issue and that's something to figure out.
And now going back to the Wasabi Research Club, because this is the first step that we should think about how to arrange the inputs and the outputs and we went down the path of CoinShuffle, I think we can use it for our advantage because the thing is even after we figure out how to arrange the inputs and the outputs, we have to figure out how to do it in a trustless way and it's like, it's a really hard problem.
But that's when the CoinShuffle line of research comes in.
And at the end of that line of research there is CashFusion, which is probably solving this problem, and which is something that I wouldn't take as it is, but I would really love to know the techniques that they are using.
So we can go through the CoinShuffle line of research, which is with this CoinShuffle now.
Next time as Lucas suggested we do something about the mixed networks and Tim Ruffing, the author of CoinShuffle, suggested to look into the dining cryptographers networks.
It's a paper.
And then of course, CoinShuffle++ and then CashFusion.
And after we look into CashFusion, which our hope is that it either solves our problem or provides or armors us with the necessary tools to tackle later the trustlessness problem.
Then we can move on to CoinJoin analysis and after the CoinShuffler things we can move on to CoinJoin analysis stuff like CoinJoin Sudoku, Boltzmann, maybe Knapsack code or whatever.
So we drop the coordination issue, we get into the subset sum issue.
What we started with Knapsack, that's my idea.
So and at that point we could actually start to research how to arrange the amounts, how to score the mixes, right?
That's the first one.
So, this is my long-term idea.

Aviv Milner: 01:11:35

I have an intuition about scoring mixes that it will be quite hard to do this and you know I know that we can apply some basic heuristics you know for example take the volume and multiply by the number of participants or this or that, but it's just not trivial thinking about how to score a mix, especially because if we decide, you know, some function accurately consumes a transaction and gives a good score whatever function we decide will shape the direction of the mixing in the future so I think that this will be quite a tough thing to not just present a function to score mix but also to justify why this function is the best approximation.

Adam Fiscor: 01:12:27

I think Knapsack is perfect, the Knapsack paper is a perfect basis for that.
Because what they did there is they counted the likelihood between inputs and outputs to belong together.
But they also counted the likelihood between inputs and inputs and outputs and outputs.
And if you adopt those numbers, somehow just weigh it with the block space used and you apply the whole concept to a mix of transact, to a chain of mixed transactions instead of just a single mix, then that might work.
I don't know.
I think that could work like that.

Aviv Milner: 01:13:20

Is it feasible to calculate the subset sum of a large CoinJoin efficiently?
Can we do that?

Adam Fiscor: 01:13:31

Not at all.
It's five inputs, five outputs that could be done.
Six, I don't think so.

Aviv Milner: 01:13:42

Okay, so.

Max Hillebrand: 01:13:44

We have constraints here, yes.

Adam Fiscor: 01:13:57

So The CoinShuffle line at the end with CashFusion, is this good for the next three weeks?
So next, dining cryptographer networks, then CoinShuffle++, then CashFusion.
And then we can move on to the first step.

Lucas Ontivero: 01:14:22

I agree.

Max Hillebrand: 01:14:25

Yes I think that's good but maybe in this slide how about increasing the frequency Because I have more capacity to maybe do a I don't know two calls a week for example

Lucas Ontivero: 01:14:45

It takes time to read the papers and think about it.
It's not so easy.