---
title: Replace-by-Fee Bug (CVE-2021-31876)
transcript_by: 0xB10C via review.btctranscripts.com
media: https://www.youtube.com/watch?v=OHx55vjX_Ig
tags:
  - rbf
  - cves
  - bitcoin-core
speakers:
  - Sjors Provoost
  - Aaron van Wirdum
date: 2021-05-21
episode: 38
---
## Intro

Aaron van Wirdum: 00:00:08

Live from Utrecht, Aruba and Utrecht, the Netherlands, this is The Van Wirdum Sjorsnado.

Sjors Provoost: 00:00:15

Hello, welcome, and listeners, sorry for the maybe not perfect sound quality, because we have to make do with the remote recording.

Aaron van Wirdum: 00:00:24

Yeah, for the second time since we're making our show my laptop broke, so here I am on my phone.

Sjors Provoost: 00:00:32

And you decided to use your laptop in a swimming pool which you know you should not do.

Aaron van Wirdum: 00:00:38

No one told me that I shouldn't do that. Okay. Apparently my laptop is not waterproof. Sjors, today we are going to discuss the exotic CVE-2021-31876.

Sjors Provoost: 00:00:57

Cool, is that a spaceship?

Aaron van Wirdum: 00:00:59

That sounds exciting, right? It is apparently a bug. Oh.

## What is a CVE?

This is actually what I'm going to ask you, Sjors. Sjors, CVE, what is a CVE number? What are we talking about here?

Sjors Provoost: 00:01:15

It stands for common vulnerabilities and exposures. It's basically, there's just a big open database of known bugs, security vulnerabilities really, not all bugs. Across all types of software. Pretty much, yeah. So then it starts with the, you know, the year and then some number that indicates, you know, the number, which bug it was in that year. Pretty much anybody can file that, can file such a report and say, hey, I think we found a security vulnerability in this project. And then you can decide how long you want to keep it secret because you want to give people time to fix things. And then it becomes for everybody to see and refer to.

Aaron van Wirdum: 00:02:02

So this was basically bug number 31876. That's the number. This is a bug in Bitcoin Core, right? Yes. Yeah, so obviously to be clear, not all CVE bugs are in Bitcoin Core, but this one is. And that's what we're discussing today.

## What is replace-by-fee?

So Sjors, this bug was discovered in March of this year by Antoine Riard, if I'm pronouncing that correctly.

Sjors Provoost: 00:02:34

You have to ask him.

Aaron van Wirdum: 00:02:38

And it was disclosed about two weeks ago on the bitcoin-dev development list. So what is this bug?

Sjors Provoost: 00:02:46

Yeah, So it relates to an episode we talked about earlier, replaced by fee, RBF. And the idea there is, you know, if you make a transaction, then maybe the fees go up and you want to increase the fee for that transaction because it's not confirmed yet and you can use replace by fee to indicate that you want to do that.

Aaron van Wirdum: 00:03:08

Yeah, so users are sending transactions to the network all the time, anytime they're spending money and all of these transactions end up in people's mempools, including miners mempools, and then miners, when they create a new block, they basically include all those transactions that pay the highest fee until the block is full, essentially, which means that if you're paying a low fee, you might have to wait until the next block. Or if you paid a very low fee, you might have to wait for a very long time. So it could happen that, you know, after you send the transaction, then all of a sudden there's a lot more transactions on the network paying more fees, and you're waiting longer than you plan to wait for your transaction to confirm. And if you include an RBF, replaced by fee, flagging the transaction, that allows you to increase the fee before it's confirmed, which will make it confirm faster.

Sjors Provoost: 00:04:01

That's right. And it should be noted that this is not a consensus rule. So it is not, because it's not happening in the blockchain itself, it's happening on the network. And on the network people can run whatever software they want. So this isn't a guarantee, but it's basically a convention to make it easier to replace your transaction while also having some security that people can't if they don't want to. But we had a whole episode dedicated to that.

## What happens if you have two transactions built on top of each other?

But one of the important aspects of this scheme is what happens if you have two transactions that build on top of each other. What if one of them signals that it can be replaced, but then the child of that transaction says it cannot be replaced? And this is where the bug comes in.

Aaron van Wirdum: 00:04:51

So you're sending funds to me and then I'm sending funds, the same funds essentially to Ruben, before the transaction is confirmed?

Sjors Provoost: 00:04:59

Yeah, and because...

Aaron van Wirdum: 00:05:02

My transaction to Ruben is what's considered a child transaction and your transaction to me the first one is the parent transaction right?

Sjors Provoost: 00:05:09

Yeah and that means that if I put a flag in my transaction to you that says this can be replaced then by definition your transaction can also be replaced, even if you don't indicate it.

Aaron van Wirdum: 00:05:21

So now we know what the parent transaction is and what the child transaction is. So let's get to what the actual bug is in this context.

Sjors Provoost: 00:05:30

Right, so the official rule as it's indicated in the BIP, the Bitcoin Improvement Protocol, is that if the parent transaction signals RBF, then the child transaction should also be RBF. Right. So, in other words, if I indicated that I can replace the transaction, then that means you can also change the transaction. And the bug, and that's what comes in, is that for Bitcoin Core, that's not the case.

Aaron van Wirdum: 00:05:56

So I can increase the fee of my transaction to Ruben If your transaction to me was an RBF transaction, even if my transaction wasn't necessarily an RBF transaction, I can still increase the fee, right?

Sjors Provoost: 00:06:10

Yes, exactly. Except you can't.

Aaron van Wirdum: 00:06:12

That's the official rule. And now the bug is that it turns out that that's not actually what's in the Bitcoin Core code, correct?

Sjors Provoost: 00:06:20

Yeah, exactly. The Bitcoin Core code is not checking that rule.

Aaron van Wirdum: 00:06:23

Right, so this is a bug specifically for the Bitcoin Core client, essentially. Is that the right way to put it?

Sjors Provoost: 00:06:32

Yes.

Aaron van Wirdum: 00:06:32

Right.

## Is this something we need to be concerned about?

So first of all, is this a problem? What kind of, what are we looking at here? Is this something that we need to be concerned about just on, at face value?

Sjors Provoost: 00:06:42

So at first sight, you might think it's not really a problem because if you wanted to be able to use RBF you know in your transaction to Rubin you could have just signaled RBF. So it only becomes a problem in more complicated scenarios especially if you have multi-party systems like Lightning and other second layer kind of ideas where there's two parties involved that can spend a certain transaction. So, you know, so for example, yeah, if there's two parties involved that can spend the same output then those two parties you know they might be able to replace each other's transactions and then this thing can get messy.

Aaron van Wirdum: 00:07:24

Yeah so from what I understand this is a bug in the Bitcoin Core code, but really the only part of the Bitcoin ecosystem that seems to be affected right now is the lightning network the lightning protocol and that's where it gets a little bit complicated, right?

Sjors Provoost: 00:07:46

yeah "a little bit" just to put it mildly.

## HTLCs

So maybe you can try a hand at explaining how can someone exploit this bug on Lightning?

Sjors Provoost: 00:07:57

Yeah, so for that we need to explain very roughly what an HTLC is, A hash time lock contract. And this is when in Lightning you are sending, or not just in Lightning, it's a general mechanism, but in Lightning is what we're talking about here. Let's say, well Let's talk about Alice, Bob and Carol, so it's a bit easy to remember the direction. Let's say Alice is sending one Bitcoin to Carol through Bob. So Alice has a channel with Bob and Bob has a channel with Carol. And the way Lightning lets you safely move one Bitcoin from Alice to Carol is by Alice sending it to Bob and by Bob sending it to Carol. But this is done atomically. So that means that the way Lightning is designed is Alice will only send money to Bob if Bob also sends money to Carol and otherwise nothing happens so this way you don't end up with a situation where Bob is sending money to Carol but Alice is not sending money to Bob because then Bob is very unhappy.

Aaron van Wirdum: 00:09:01

Yeah essentially Carol creates a secret I think that's the way it works, right? Carol creates a secret number and then gives the hash to Alice. And Alice sort of tells Bob, If you tell me the secret that refers to this hash, then I'll give you a Bitcoin. And then Bob can tell Carol the same thing. Bob also tells Carol, if you can tell me the secret of this hash, then you'll get a Bitcoin. And the way this actually works is that there are transactions created that send coins from Bob to Carol and from Alice to Bob that require this secret. So if, am I saying this right? If, let's say, if Bob publishes, hang on, who's publishing what? Sjors, help me out here.

Sjors Provoost: 00:10:01

Yeah, so it basically goes from Carol to Alex back. So Carol publishes the secret, then so Bob, let me do that again. Bob has a transaction that says Carol gets my Bitcoin if she reveals the secret. Right? So what happens then is that Carol reveals the secret and Bob sends the money. And because the secret is revealed, in this case on the blockchain, Alice can see the secret. So Alice can now take the money. Okay, Alice can now send the money.

Aaron van Wirdum: 00:10:36

No, no, no, no, no, no, no, no, no, no. Bob sees the secret and therefore he can claim the money from Alice, right?

Sjors Provoost: 00:10:42

Oh, yeah, exactly. Well, yeah, Alice could also be nice and volunteer the money, but yeah, this is how it works, right? Bob wants the money. So Bob sees the secret that Carol published, takes the money from Alice and Carol is able to take the money from Bob. So this is all good. The thing is though, there's also a condition where there could be a timeout. So if nobody reveals the secret, well you don't want those coins to be stuck forever. So basically if nothing happens then after a while Alice can just take the money back and if nothing happens after a while Bob can take the money back right that's a fallback mechanism there's a timeout there that still make sense

## How can someone exploit this bug in lightning?

Aaron van Wirdum: 00:11:26

All right so that's what HTLCs are. Now let's get to this bug how does this How can this bug be exploited in the context of HTLCs?

Sjors Provoost: 00:11:37

Yeah, so the way you kind of have to understand how it was designed is that if Carol is nice and on time, she will reveal the secret on the blockchain. Right? Sorry, one second. She will reveal the secret on the blockchain, which is just a transaction, and that transaction confirms, because that's what the blockchain does. And that means that the timeout, the alternative transaction, where she can take the money back, well, that can't go anywhere, because once the secret is revealed and that transaction is confirmed, the transaction timeout cannot be there. You would need to re-org the blockchain to be able to use it. Does that still make sense?

Aaron van Wirdum: 00:12:24

Yeah, in the context of Lightning, it doesn't only matter who's paying who, it also matters that the transaction confirms in time. Because if the transaction doesn't confirm in time, the payer can take the money back through the timeout. So that's why that matters.

Sjors Provoost: 00:12:41

So if nothing happens on the blockchain, then after 80 blocks, the timeout transaction can be spent. But if before that moment the secret is revealed then that transaction, then the timeout transaction cannot be spent because yeah it would replace the other one. So that's how it works in theory but the problem is it has to go into the mempool first. And so what Carol can do if she's kind of collaborating with Alice I think although I'm not sure about that part what she can do is she can reveal she can release the transaction with the secret in it but she puts a very low fee on it. And now we have a problem because this transaction is in the mempool, it is revealing the secret, it is claiming the funds, but it's not getting confirmed and it can take a long time. In fact it can take so long that in the meantime there's a timeout even for Alice and so Alice will just issue her a refund transaction. And so now what happens is Alice got her money back and Carol still hasn't paid.

Aaron van Wirdum: 00:13:51

Okay, Sjors, I think you just explained it the wrong way around.

Sjors Provoost: 00:13:54

Yeah, that's possible. We're not sure. We just listened to it in the...

Aaron van Wirdum: 00:13:56

So what happens is Carol publishes the transaction to claim the funds and she actually claims the funds. Now the secret is revealed to Bob who can also claim the funds from Alice. But if this transaction is low on the second transaction where Bob claims the funds, then it's possible that this transaction won't confirm and Alice can later reclaim the funds when the timeout has run out. And now Bob is stuck in the middle without any money because the funds have been claimed from him and he's not actually able to claim any funds back from Alice because Alice basically cancels that transaction. I think that's the exploit, right?

Sjors Provoost: 00:14:47

Yeah, I think so. Let me also say it in one way, right? So Alice basically just claimed the money because she knew the secret, right? Because the secret was revealed. Yep. And she used the normal fee, so that transaction will confirm. Nope. No, no, no, sorry. See, this is really confusing. No, what Alice does is she just, she can wait, right? She has to take the initiative. So she basically issued the refund to take the money back because there was a timeout.

Aaron van Wirdum: 00:15:17

Yeah, Alice has all the time in the world basically. Well, Alice is sort of hoping that the transaction won't confirm so she can claim it back. Alice is ultimately the one paying Carol. So if she can't claim the funds back, then Bob is screwed if he already paid Carol. I think that's sort of the problem here.

Sjors Provoost: 00:15:40

Yeah, so indeed.

Aaron van Wirdum: 00:15:42

Dear Van Wirdum, Sjorsnado listeners, We're sorry for this confusing episode. It doesn't help that we're doing it at the distance. But we're kind of figuring it out ourselves admittedly, but we're pretty sure this is the problem, right Sjors.

## The basic principle

Sjors Provoost: 00:15:57

Yeah, roughly anyway, because whenever you read these mailing list posts, it always turns out to be a one more step more complicated. But I think this is the basic principle where we have a transaction that is in a mempool, but it's not gonna confirm on time and therefore there's another timeout and this allows people to cheat. And normally, the way to prevent that kind of problem or to deal with that kind of problem is with RBF.

## The heart of the problem

Aaron van Wirdum: 00:16:22

Yes, let's just get to the heart of the problem here. The problem indeed is that usually you're able to RBF your transaction, which is important in the context of lightning where we have timeouts type of stuff going on. So if all of a sudden you can't use RBF anymore because there's a bug in Bitcoin Core, now it's getting problematic, more problematic than usual, where usually you can just have patience, it just means your transaction is being a bit slower. Now, all of a sudden, there's a real problem because someone can take your money back if you can't RBF. That's the gist of the problem.

Sjors Provoost: 00:16:58

Right, because normally what Bob would have wanted to do in this case is basically get his refund because he can see that Alice is getting the refund so he should be getting a refund and he would be able to do that because the refund would just pay a higher fee than the other transaction and all would be happy. But basically, because of this RBF glitch here, it might not be that easy.

Aaron van Wirdum: 00:17:28

Okay, well, full disclosure, I'm not sure if we explained it right. I'm sure we explained the bug right. I'm sure we explained the ultimate problem right. I'm not sure if we explained  right. I'm sure we explained the bug right. I'm sure we explained the ultimate problem right. I'm not sure if we explained the HTLC order of things right.

Sjors Provoost: 00:17:43

I think that's correct that we explained it probably wrong.

Aaron van Wirdum: 00:17:46

If we got it wrong, I'm sorry everyone. Better next time, especially if we're live in the same room again. I hope you got something out of it.

## How worried should lightning people be?

Aaron van Wirdum: 00:18:00

Sjors, last part of the episode then. Is there something, how worried should we be? How worried should lightning people be? And is there something fixable?

Sjors Provoost: 00:18:04

I'm not entirely sure how worried lightning people should be because this type of attack was already possible even without this bug, but it was more complicated. And at the same time, Lightning has been developing other solutions around this general problem. So honestly, I don't really know. But the best news here is that this bug is fairly easy to fix. Or at least, you know, it can be fixed because again, it's not a consensus rule. So Bitcoin Core could simply ship a fix for it. And then when people upgrade, the fix is there. And there's also nodes that ignore RBF completely, which means still replace whatever has a higher fee.

Aaron van Wirdum: 00:18:47

Yeah, it shouldn't be a controversial fix, of course.

## Is the bug already fixed?

Is it already fixed as far as you know?

Sjors Provoost: 00:18:52

As far as I know, I don't think so. I haven't checked in a few days. Somebody wrote a test, a functional test for Bitcoin Core to describe the bug. That's always nice because then it's easier to see that it's fixed. But I don't know how easy or hard it is to fix it. But in principle, like, I don't think it would be controversial to fix it. I mean, it would be good for Bitcoin Core to do what the BIP says it should do and we know that I think in btcd which is another implementation it is implemented correctly.

## Closing comments

Aaron van Wirdum: 00:19:26

All right, Sjors, I think this was our worst episode so far. What do you think?

Sjors Provoost: 00:19:30

I don't think so. We have the pilot episode that we never actually released.

Aaron van Wirdum: 00:19:34

Oh yeah, that's definitely the worst one. Well, this is maybe the worst one we're actually going to put online.

Sjors Provoost: 00:19:42

But, hopefully it's enough for people to dig into this rabbit hole and actually understand it.

Aaron van Wirdum: 00:19:47

Better luck next time.

Sjors Provoost: 00:19:48

All right then.

Aaron van Wirdum: 00:19:49

But I think that was the episode for us.

Sjors Provoost: 00:19:51

Yes, well, thank you for listening to The Van Wirdum Sjorsnado.

Aaron van Wirdum: 00:19:55

Sjors, maybe we should compensate with a good pun. Do you have a good pun to compensate this with? No. All right, then we'll end without a pun.

Sjors Provoost: 00:20:05

Sorry about that. All right, until next time.

Aaron van Wirdum: 00:20:08

There you go.
