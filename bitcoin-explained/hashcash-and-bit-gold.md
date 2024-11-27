---
title: Hashcash and Bit Gold
transcript_by: varmur via review.btctranscripts.com
media: https://bitcoinexplainedpodcast.com/@nado/episodes/episode-88-hashcash-and-bit-gold-a5cjn
speakers:
  - Sjors Provoost
  - Aaron van Wirdum
date: 2024-01-03
episode: 88
summary: 'In this episode of Bitcoin, Explained, Aaron and Sjors discuss two electronic cash projects that predate Bitcoin: Adam Back’s Hashcash and Nick Szabo’s Bit Gold. As detailed in Aaron’s new book, The Genesis Book, these systems introduced design element that were later utilized by Satoshi Nakamoto. Aaron and Sjors explain what these elements are, and how they inspired Bitcoin’s design.'
---
Aaron van Wirdum: 00:00:18

Live from Utrecht, this is Bitcoin Explained.
Hey Sjors.

Sjors Provoost: 00:00:21

Yo, yo.

[removed sponsor segment]

## Aaron's book - "The Genesis Book"

Sjors Provoost: 00:01:07

So, Aaron, you wrote a book.

Aaron van Wirdum: 00:01:08

Yeah.
Oh, yes, I did.

Sjors Provoost: 00:01:09

Cool.

Aaron van Wirdum: 00:01:09

At the time of recording, it's almost published.
We're publishing it tomorrow, January 3rd, but that's like midnight actually, UTC.
So in a couple of hours, Sjors, my book will be live.
Yeah, so that's kind of cool.
It is called "The Genesis Book", Sjors, and it tells the prehistory of Bitcoin, the origin story of Bitcoin.
It's the story of the people and projects that inspired Bitcoin.
So, Sjors, to celebrate that, we're going to discuss some of the topics from my book.

Sjors Provoost: 00:01:45

That's right.

Aaron van Wirdum: 00:01:46

So it's kind of for the first time, I think, not really an episode about Bitcoin.
Have we done something about it?

Sjors Provoost: 00:01:54

We've done an episode about Digicash.

Aaron van Wirdum: 00:01:57

Well, no, hang on, we also did the episode about Tornado Cash.
That was actually not about Bitcoin.

Sjors Provoost: 00:02:03

Exactly.

Aaron van Wirdum: 00:02:03

Anyways.

Sjors Provoost: 00:02:05

And we'll still cover things that are very relevant to Bitcoin.

Aaron van Wirdum: 00:02:08

Right, well, my entire book is very relevant to Bitcoin.
Everything in my book is relevant to Bitcoin, Sjors, so of course, also what we're going to discuss.

Sjors Provoost: 00:02:15

Excellent.

Aaron van Wirdum: 00:02:17

Did I mention it's called "The Genesis Book", and you can find it on the Bitcoin Magazine store and Amazon and I don't know where else.

Sjors Provoost: 00:02:23

Sounds good.

Aaron van Wirdum: 00:02:24

I think [thegenesisbook.com](https://thegenesisbook.com) should be live by the time you listen to this, hopefully.

Sjors Provoost: 00:02:32

All right.

Aaron van Wirdum: 00:02:32

You want to know anything more about where you can find my book, Sjors?

Sjors Provoost: 00:02:35

No, but we will put it in the show notes.

Aaron van Wirdum: 00:02:37

Okay, we'll go to the episode then.
I discuss in my book, there are five main digital cash projects that are precursors to Bitcoin in a way.
There are more, and there's a lot more in the book, Sjors.
There's all kinds of background and stories, and colors, and storylines and adventures, and ... okay, I'll stop now.

Sjors Provoost: 00:03:05

Yeah, from what I've been reading, you cover Austrian economic stories, and sort of alternate the digital money story versus the political story.

## Introduction

Aaron van Wirdum: 00:03:16

Anyway, enough with the shilling, let's get to the actual episode.
So there's five electronic cash projects in the book that have a bigger focus than some of the more minor ones.
So the first one of that is e-cash, which was produced by Digicash.
We're not going to talk about that because we already did in episode 52, which was about Fedimint, right?

Sjors Provoost: 00:03:43

Yeah, in episode 52, Fedimint, we start all the way back with how David Chaum's e-cash works, how blinded signatures work, definitely recommended listening.
Then we go all the way to how that's now applied to Fedimint and Cashu.

Aaron van Wirdum: 00:04:00

Yeah, so we're going to skip that one, we're not going to talk about that again.
Instead this episode will be about Hashcash and BitGold.
I don't know how we're going to do this format, usually I'm the one who asks questions.
We'll figure it out, I think.
I have no idea how to do this now.

Sjors Provoost: 00:04:22

Well, you should tell a little bit of the story, and then we'll get to some of the technical juicy bits where I might have some opinions too.

## Hashcash

Aaron van Wirdum: 00:04:31

Okay, cool, yeah.
The first one is [Hashcash](http://www.Hashcash.org/papers/Hashcash.pdf).
The background here is, in the nineties the internet was becoming more popular, and also there was the cypherpunks mailing list.
They had their own mailing list where they were discussing privacy technologies, but also more ideological types of posts, or how to create digital cash and all these kinds of discussions.
A bunch of the cypherpunks were also running remailers, this was sort of the precursor of Tor.
There was a way to send an email anonymously, send an email without the recipients knowing where the email came from.
The problem was that spam was becoming popular around this time as well, the cypherpunk mailing list itself was being spammed, anyone else who had an email address was being spammed, and especially also these remailers were starting to be spammed to the extent that it was becoming burdensome to run one.
So it was potentially an attack on these remailers.
Either it was a spam attack that remailers were being abused for, or maybe it was just an attack on the remailers themselves, as a denial of service type of situation.
So cypherpunks specifically wanted to create digital cash.

Sjors Provoost: 00:05:54

One step back, I think they also wanted to fix the spam problem, right?
With digital cash maybe in the back of their mind.

Aaron van Wirdum: 00:06:02

Sorry, I said digital cash, I meant digital postage, and that's what you're getting.

Sjors Provoost: 00:06:06

Yes, digital postage stamps.
But it might be interesting, something you also mentioned in the book is that there was a worry that if the cypherpunks didn't fix this problem, then governments would step in and they would start dealing with spam.
This would be a problem because if governments have to fight spam, then the way they would probably do that is by de-anonymizing everyone and basically KYC-ing email to the extent of where if there's a spammer, they know who they are.

Aaron van Wirdum: 00:06:36

Yeah, plus the government would then have to make a judgment call about what is spam and (that's) kind of relevant to Bitcoin these days, with the whole Ordinals thing.
But yeah, then governments have to make a judgment call about what is spam, so what actually is legal?
Then by the time they can find a spammer, yeah, that would have to be some sort of identification.

Sjors Provoost: 00:06:54

And they would have to ban anonymous email, which is the kind of thing they were trying to do.

Aaron van Wirdum: 00:07:00

Right, so the cypherpunks didn't like this, and specifically Adam Back didn't like this.
Adam Back was of course one of these cypherpunks, I don't think he needs an introduction to anyone who listens to this podcast.
So Adam Back wanted to come up with digital postage.

Sjors Provoost: 00:07:19

First I think we should go back in time, right?
Because everybody talks about Hashcash and how Adam Back invented that, and he did, but it was not the first time it was invented, as so often happens in history.

Aaron van Wirdum: 00:07:30

I was also considering if I should talk about the other ways they were thinking about digital postage, but I think we should skip that, right?
That's what you can find in the book.

Sjors Provoost: 00:07:40

Exactly.

Aaron van Wirdum: 00:07:41

So shall I hand it to you here?
Actually Adam Back was not the first person to invent digital postage.
He did think he was, he was not aware of the previous proposal, but there was actually another proposal that's a bit older and quite similar to Adam Back's proposal, which was... the names from the top of my head?

Sjors Provoost: 00:08:06

[Dwork and Naor](https://www.wisdom.weizmann.ac.il/~naor/PAPERS/pvp.pdf).

Aaron van Wirdum: 00:08:07

Yeah, I was thinking of their first names, but yeah, their last names were definitely Dwork and Naor, Moni Naor and Cynthia Dwork, I think.

Sjors Provoost: 00:08:14

Yeah, and they did not come from a cypherpunk background.
They came from it with a just, hey, we are people using email and we don't like spam background.

Aaron van Wirdum: 00:08:27

They were from IBM, right, they were computer pros.

Sjors Provoost: 00:08:31

Yeah, they weren't random people, but they were not saying - how can we prevent the government coming into this email world?
It's just, how do we get rid of spam?
Essentially they came up with the idea of introducing Proof-of-Work for email, and they came up with three different work algorithms.

Aaron van Wirdum: 00:08:51

Yeah, and to be clear, the term Proof-of-Work didn't exist yet at this time.

Sjors Provoost: 00:08:55

I don't know exactly what they called it, but something along the lines of like a challenge or...
But basically, they picked three algorithms, and I think one of them boiled down to finding - if you take a number and you wanna figure out which two primes can be multiplied to get to the number.
So let's say you pick the number 100 and you say "tell me which two prime numbers multiply to 100", and you would say "I don't know, because it's 10 times 10", so those are not prime.

Aaron van Wirdum: 00:09:28

Kind of a bad example.

Sjors Provoost: 00:09:30

No it's a fine example but it shows that as soon as you give me the right answer, I can very quickly verify that, yes, these two numbers multiply to this total.
Actually, I think you didn't have to find prime numbers, it's just modulo prime number.

Aaron van Wirdum: 00:09:43

I think the way it works is you have two very big prime numbers, these are factored (multiplied) into another big number, and then the big number can only be produced by two specific prime numbers then, right?

Sjors Provoost: 00:09:56

I think that's RSA, but not what this...

Aaron van Wirdum: 00:10:01

Oh, this works a bit different?

Sjors Provoost: 00:10:02

I think this was much simpler, this was something called modulo a prime number.
So if you take a much smaller number we know the number 13 is prime, right?
So you would say okay here's the number 10, find me two numbers that you can multiply to get the number 10, but you can multiply and then you do modulo 13.
So you can say - this is not very good in math - but if you do 3 times 4 that's 12, so that's not enough.
If you do three times five, that's 15.
(15) Modulo 13 is two, right?
You keep looking for this number that if you go around in circles around this prime number, it gets you the correct result.

Aaron van Wirdum: 00:10:45

Okay, we're getting very into the weeds now, let's get back to the main road.
So they had three ideas.

Sjors Provoost: 00:10:50

Exactly.
So this is one of them and the key part is that it takes a while to find these numbers, but it's very quick to check.
You just multiply modulo and you're done.
They had two other algorithms that I don't want to go into also because I don't know them, but they had an interesting property from them is that you could build an exception into it.
So basically saying, well, if you're the mailing list operator, then you can use this special key and you can bypass the work.
I don't know whether that would be practical or not, but that's sort of what they came up with.

Aaron van Wirdum: 00:11:23

Right, the backdoor function.

Sjors Provoost: 00:11:25

Yeah.

Aaron van Wirdum: 00:11:27

The points being here though, so what Naor and Dwork, the idea they come up with is that whatever calculation you have to make, you have to make it in combination with some data from the email itself.

Sjors Provoost: 00:11:41

Yes, because you can prove that you did a bunch of work, but if that's unrelated to your email, you would just reuse the same work.
So you have to make sure that the work is always a function of the email itself.
Ironically, they discovered the use of hash functions for that, or they knew that you needed hash functions for that part.
So you take the hash of the email, and then you use the hash as the starting point of your challenge.

Aaron van Wirdum: 00:12:05

Oh, they did use the hash for that part?

Sjors Provoost: 00:12:07

Yeah.

Aaron van Wirdum: 00:12:08

Oh, I didn't know that, that's interesting.
We should spell this out for those who haven't realized this.
Naor and Dwork were not using hashes for the Proof-of-Work.
They were using, what's it called?
Is there a better term for what they were (using)?

Sjors Provoost: 00:12:25

They were just using math problems.

Aaron van Wirdum: 00:12:26

Yeah, right.
Now the idea was still very similar to...
Most people that listen sort of know where Proof-of-Work came from, that's why we're sort of skipping some parts, but we should actually spell it out.
So the idea was if you attach a little bit of Proof-of-Work to an email, then (for) most people that want to send an email, that's not really a problem, that's like a couple of seconds of computing time.
However, if you're a spammer that wants to send tens of thousands, or maybe even millions of emails, which you usually have to do to be a profitable spammer, then it becomes so expensive that it's not worth it anymore.
So that's how it's postage.
It's different (from) postage in the sense that you're not buying it from anyone.
Also whoever you're sending the email to is not getting the money or anything like that.
You're proving that you spent some resources, some energy, and that way it's too expensive for a spammer to be a spammer.

Sjors Provoost: 00:13:23

Yes, exactly.

Aaron van Wirdum: 00:13:25

That's what Naor and Dwork essentially came up with.
This was in 1992, but then independently, basically, it was sort of a parallel invention - not exactly parallel, (there was) some time difference, but Adam Back was not aware of this solution, so when they were discussing this problem on the cypherpunks list, they didn't know it was kind of a solved problem, but then he reinvented something very similar.

Sjors Provoost: 00:13:54

Yes, but then using a hash function, SHA-1 in this case, but that doesn't really matter.
The thing is it's not actually better or worse than the design that was made before.

Aaron van Wirdum: 00:14:08

Okay, (can) you explain how it works?

Sjors Provoost: 00:14:10

So you take some aspects of the email, as we said before, and then you add a nonce to it.
A nonce is a number that you pick randomly, doesn't matter what it is, but you have to pick it such that the resulting hash starts with a certain number of zeros.
Notice that in Bitcoin Core, the hash does not only start with a certain numbers of zeros, but has a specific value that it has to stay under, but it's roughly the same idea.

Aaron van Wirdum: 00:14:37

Right, so you would send the email, you include this hash.
Then the recipient would check if there's actually a valid hash in it, if not, the email would just bounce.
I guess that was the same with Naor and Dwork's system.

Sjors Provoost: 00:14:54

Yep, same idea.

Aaron van Wirdum: 00:14:56

Yeah, I didn't spell that out, but same idea, basically.

Sjors Provoost: 00:14:57

Yep, they both have the concept of difficulty, where you can make the hash more or less difficult, depending on what your perceived spam problem is.

Aaron van Wirdum: 00:15:04

Yeah, the recipient or the remailers, which I mentioned earlier, will check - does this have a failed hash?
If not, just reject it, and if so, it's forwarded to whoever it needs to be forwarded to.
So that's basically the idea of Hashcash, right?
Did we forget about anything?
I can tell you that in the early days, there was some adoption of it.
So Apache used, is that how I pronounce it actually?

Sjors Provoost: 00:15:43

I think Apache, yeah, SpamAssassin.

Aaron van Wirdum: 00:15:45

Yeah, they used it in SpamAssassin and Microsoft recreated something very similar.
It was incompatible with different standards, but basically the same idea again.
And then more recently...

Sjors Provoost: 00:15:59

Those two are completely unused right now because SpamAssassin removed it again, and the Microsoft thing doesn't exist anymore.
More recently, as you're getting to, Tor has been using Proof-of-Work.
Again, it's a completely different algorithm, but it is an example of Proof-of-Work being used outside of a cryptocurrency, where it's not used to produce value, it's simply used to prevent spam.
So this concept is still alive and well.

Aaron van Wirdum: 00:16:27

Right.

Sjors Provoost: 00:16:27

Now, one interesting aspect I wanted to talk about...

Aaron van Wirdum: 00:16:33

This is why we're talking about it in a Bitcoin podcast.
Why we're focusing on Hashcash more than the Naor-Dwork concept, right?
Is that where you're getting at?

Sjors Provoost: 00:16:42

Yeah, there's an interesting kind of a historical coincidence, I would almost say.
This is something you pointed out earlier that I think Adam Back was aware of and he pointed it out, which is to say that there are multiple kinds of Proof-of-Work, but in particular, two different kinds are stochastic and non-stochastic Proof-of-Work.
That's a distinction I hadn't really thought about.
The idea here is that with a hash function you may or may not get the right result, and statistically it will take a certain amount of time before you find a solution, but it's random.
Sometimes you find the right solution instantly, other times it takes a very long time.
Whereas with these earlier algorithms, there's a guaranteed time of how long it takes to find the square root, for example, of two numbers.
So I suppose you could maybe make it random, but assuming you use a standard algorithm, it'll take a fixed amount of time to find a solution.

Aaron van Wirdum: 00:17:45

Let me give an analogy that I've used, not in the book but in an article I wrote earlier.
Let's say there's a 100 lottery tickets, and one person buys 40 tickets and another buys 60.
Now the person that has 60 has more chance to win - 60%, but the person that bought 40 still has 40% (chance) to win as well.
While if you take two cyclists and one of them can ride his bike (at) 60 miles an hour and the other (at) 40 miles (an hour), then any time they do a race, the one that can cycle 60 miles an hour will just win, every time.

Sjors Provoost: 00:18:25

Exactly.

Aaron van Wirdum: 00:18:26:

Every time the same cyclist will win.
There's no 40% chance that a 40 mile(s) per hour cyclist will ever win.
It's just not going to happen.

Sjors Provoost: 00:18:35

So if you translate that to the context of Bitcoin mining as it is today, let's say we had picked a non-stochastic form of Proof-of-Work, based on that original paper.
So if Adam Back had known about the original paper and had not bothered to implement something based on a hash function, because there's already a solution out there, then you would have the biggest miner, whoever that is, will just always find the next block first, because they would always find that big prime number or whatever the challenge is.
They would always find it first.

Aaron van Wirdum: 00:19:04

Right.
It will be like that 60 mile cyclist rather than...
Currently Bitcoin mining kind of works like this lottery, but if the biggest miner just always wins, then you can't have Bitcoin like we have it today.

Sjors Provoost: 00:19:16

Of course, we still have some centralization problems in that sense, but this would be centralization on steroids if we did not have hash-based Proof-of-Work.

Aaron van Wirdum: 00:19:23

Yeah, basically Bitcoin wouldn't work, like not as it's designed today.

Sjors Provoost: 00:19:27

Yeah, or maybe we would have figured it out and then changed it, but definitely it would have been not optimal.

Aaron van Wirdum: 00:19:32

Yeah, so what you alluded to, we may have been quite lucky in that sense, that Adam Back wasn't aware of the prior proposal.
He invented this in a way that's actually useful for Bitcoin.

Sjors Provoost: 00:19:45

Exactly, but it's not something he was aware of at the time, or at least he didn't put it in the paper.

Aaron van Wirdum: 00:19:51

As far as I know, and I've discussed it with him, so either my memory is failing me or I'm pretty sure he only realized that after Bitcoin himself.
He only figured that out, so that actually Hashcash specifically only works for Bitcoin.
That was not some sort of pre-planned thing for Mr. Back.

## Nick Szabo on secure benchmark functions

Sjors Provoost: 00:20:09

Yeah, now before we get to the next topic, which is BitGold, we should talk about something that the author of BitGold observed about Proof-of-Work.
That's kind of the bridge I wanted to make.

Aaron van Wirdum: 00:20:23

Yeah that is also the bridge I make in my book, Sjors.

Sjors Provoost: 00:20:26

Excellent.
It's almost like I read it.

Aaron van Wirdum: 00:20:29

At least if we're thinking about the same thing.
So Hashcash or Proof-of-Work, for the first time introduced something, created something akin to digital scarcity, because there is an actual physical cost - energy in the real world required to produce it.

Sjors Provoost: 00:20:55

Yeah.

Aaron van Wirdum: 00:20:56

So rather than just copying numbers, you have to actually invest something, real resources, and that sort of creates something that you could see as digital scarcity, right?
That's what you're getting at.

Sjors Provoost: 00:21:05

That's not where we're getting it, though it is true.
What I'm getting at is, the question is, how do you define Proof-of-Work, or how do you measure it?
How is it different from other cryptography?

Aaron van Wirdum: 00:21:18

This is not a bridge I make in my book, Sjors.
Unless I'm completely confused where you're going.

Sjors Provoost: 00:21:23

It is a new bridge, but basically Nick Szabo wrote an article about something he calls... now I lost the term, that's not smart.

Aaron van Wirdum: 00:21:33

You mean secure benchmark functions?

Sjors Provoost: 00:21:35

Yes, secure benchmark functions.
So here's the thing, we know that with normal public key cryptography for example, and with hash functions like SHA-256, we know that it's easy to verify.
_Easy_ is defined as (it) takes a very short time on a typical computer, and impossible, or it would take forever, effectively, to hack it, to coincidentally go back from the hash to the original, from the public key to the private key which is then called _hard_.
But with Proof-of-Work you're doing something that's a little bit in between.
It is definitely not easy to go back to find a certain number of zeros for example, in the Proof-of-Work in the hash, but it's also not hard - in the sense that it will not take forever.
In fact, you don't want it to take forever because then you cannot make the Proof-of-Work on your email if it would take forever to make the Proof-of-Work.
Then the question is, how do you define that?
How hard is hard enough?
(It) should not be too easy, (it) should not be too hard.
Nick Szabo wrote this article about it, coining of term "secure benchmark function".
Now if you look at the 1992 paper about Proof-of-Work, they were also informally defining it as something that's not too easy, not too hard, somewhere in between.
So, Szabo put it in slightly more mathy terms.
The analogy we could get into is the one-way function, or what it's comparing it with.
So we talked about one-way functions in an earlier episode, where you actually were correct and I was wrong.

Aaron van Wirdum: 00:23:15

So I remember that.

Sjors Provoost: 00:23:18

Good, so keep enjoying that feeling.

Aaron van Wirdum: 00:23:20

Yes.
I think everyone heard that, right?
Can you repeat it one more time?

Sjors Provoost: 00:23:25

Let's just try and explain it correctly, because I don't even remember exactly what I was saying.

Aaron van Wirdum: 00:23:30

Go on.

Sjors Provoost: 00:23:31

A one-way function is a function that is very easy to go in one way, like checking that a hash is correct, but very hard to go the other way, like trying to produce a fake original (pre-image) of a hash.
There are a bunch of one-way functions out there.
One is finding the factors in a big number, or these prime factors as you mentioned with RSA.
Another is the discrete logarithm problem, or that's sort of a more generic one, but that is used for public and private key cryptography, like the elliptic curve.
Then there's cryptographic hash functions like SHA-256, which so far has not been broken.
The problem is there is no mathematical proof that this actually exists.
We think these functions are one-way, and they better be one-way, but it may turn out that some mathematician somewhere proves that they're not, and then you get into the whole `P = NP` stuff that we're not going to get into.
Now, there is a special kind of one-way function called the [trapdoor one-way function](https://en.wikipedia.org/wiki/Trapdoor_function).
That is public key - private key cryptography, where it is very hard to go back, it is very hard to go from a public key to a private key, in fact (it would) take the age of the universe, unless you know the private key.
Then it's trivial.

Aaron van Wirdum: 00:25:03

Yes.

Sjors Provoost: 00:25:04

I think I said it wrong.
It's very hard to fake a signature, for example, but if you know the private key, then it's trivial to make the signature, and that is the trapdoor, the secret passageway through which you can do things.
That was the distinction we wanted to make back then.

Aaron van Wirdum: 00:25:18

There actually is, Sjors, a chapter about this in my book as well.

Sjors Provoost: 00:25:21

Yeah, so then the secure benchmark function has to be less strenuous.
It can't be a one-way function because then you'll never go back.
So if you go to the [Wikipedia article](https://en.wikipedia.org/wiki/One-way_function) about one-way functions, it defines this little thing like, okay, for any blah, blah, blah function that you try a hundred thousand times or whatever, statistically you should almost never find the correct answer.
That's sort of how they defined it.
Then Szabo basically writes a similar formula, but then explaining what this secure benchmark function should look like.

Aaron van Wirdum: 00:25:57

Sjors, are we still just making a bridge?

Sjors Provoost: 00:26:02

Yes, we are.

Aaron van Wirdum: 00:26:03

This is a big bridge you're building here.

Sjors Provoost: 00:26:04

I'm almost done with the bridge.
One thing that is interesting there is that when it comes to these one-way functions, it doesn't matter what hardware you have.
You can have the whole universe and you still cannot crack it.
You can have a Dyson sphere and you can't crack it.
But in the secure benchmark function, the device that you use, the machine that you do things on, actually matters in the math.
You cannot just abstract away the machine, you have to say, okay, what is a realistic computer?
Then you get back to the spam problem.
If a spammer has an ASIC, a modern-day ASIC, and let's say the algorithm was SHA-256 instead of SHA-1, then you as a consumer trying to send an email would have to burn your phone to the ground in order to just send an email, but that guy with the ASIC can just spam a million people because per watt of electricity that you're putting into that ASIC you can just produce enormous amounts of spam, whereas your phone is less efficient so it would just get too hot.
That's why it's very hard to find functions that are easy enough for a phone, hard enough for an ASIC, and he anticipated that problem in that very short paper.

Aaron van Wirdum: 00:27:12

That was Sjors building the Brooklyn Bridge over here, beautiful in its own right.

Sjors Provoost: 00:27:17

Exactly.
That's why he needed, for his BitGold proposal, because he didn't actually build the project, he says make sure it's one of those secure benchmark functions.

## BitGold

Aaron van Wirdum: 00:27:31

Yeah, in my book, I sort of muffle this away in a footnote, and I just call it hashes because it's what we were talking about anyways.
Okay Sjors, let's talk about BitGold.
I don't know if there's much specifically to introduce.
I can tell the whole story about how the cypherpunks want to create digital cash and Nick Szabo was one of them, but let's...

Sjors Provoost: 00:28:04

I think it might be interesting to mention... I think it was like seven points that he describes that this system should do?

Aaron van Wirdum: 00:28:12

Well, that was Adam Back.

Sjors Provoost: 00:28:15

Oh, I thought the BitGold paper also lists like seven properties of the system.

Aaron van Wirdum: 00:28:20

In the BitGold paper? It's been a while since I read it.

Sjors Provoost: 00:28:22

Yeah, maybe you just describe it in general terms.

Aaron van Wirdum: 00:28:27

BitGold itself?
Okay, so we're getting more to the technical side then.

Sjors Provoost: 00:28:32

Yes, what the architecture of the system is and how it should work.

Aaron van Wirdum: 00:28:35

Okay, yeah, I can do that.
Nick Szabo wanted to create digital cash, right?
Hashcash was introduced, so now there was something akin to digital scarcity.
It wasn't real digital scarcity, obviously, or at least not limited because over time it becomes easier and easier to create valid hashes.
There were a number of problems with Hashcash, why you couldn't use it as money, also, of course, you can't pay someone with Hashcash.
It's like a one-time use.

Sjors Provoost: 00:29:03

Yeah, so what you're describing is the inflation problem, right?

Aaron van Wirdum: 00:29:06

Well, that's the one problem, and also you can't transfer it to anyone.
You can't re-spend Hashcash.

Sjors Provoost: 00:29:13

Yeah.

Aaron van Wirdum: 00:29:14

So it wasn't really digital money yet, it was digital postage, essentially.
But it did introduce something akin to the digital scarcity, and this idea inspired, for example, Nick Szabo to propose their own digital currency schemes.
Now, BitGold was never implemented, it was only ever a proposal, but it's still interesting.
The way it works is you start with a candidate string.
The candidate string can be anything, it doesn't really matter, but let's just say a random string of numbers.
Then with a Proof-of-Work or a secure benchmark function, as you just explained, that's how Nick Szabo called it in his paper, I believe.
At least in one of his posts, he very specifically called it that.

Sjors Provoost: 00:30:03

Yeah, I think in the post I read, he just used all of the terms, but then made this benchmark a more specific definition.

Aaron van Wirdum: 00:30:11

Right, exactly.

Sjors Provoost: 00:30:12

But we can just call it Proof-of-Work because that's what it is.

Aaron van Wirdum: 00:30:14

Yeah, let's call it Proof-of-Work.
So there's a candidate string, anyone can use Proof-of-Work to create a new valid hash, essentially.
Now the person who creates this valid hash becomes the owner of this hash.

Sjors Provoost: 00:30:32

So whoever creates it first.

Aaron van Wirdum: 00:30:33

Whoever creates this first, yeah.
I don't think it was specifically defined or specified how this initial ownership would work, but the obvious solution is you hash your public key with it, that would just be an easy way to do it, right?
Anyway, so whoever creates a valid hash using Proof-of-Work on the candidate string gets to own that string, and then the valid hash becomes the new candidate string.
So now everyone can start hashing that to find the next candidate string to find the next valid hash, which then becomes the next candidate string.
Okay, so that's how you own these strings, essentially.
Transferring strings is much like Bitcoin, you sign a message saying, this string now belongs to this public key.
If that message is cryptographically signed with the corresponding private key of whoever was owning it, whatever public key was owning it, then the transfer is valid.
The challenge was - who gets to keep track of who owns what, or perhaps more specifically, how do you prevent double spending?
One person could sign several transactions (to) go to several people.

Sjors Provoost: 00:31:50

And how can you prevent, afterwards multiple people saying that they found it first, right, if the new thing was discovered?

Aaron van Wirdum: 00:31:58

Yes, right, that too.
So there needs to be, consensus on who owns what.
Also other problems are for example, censorship.
Anyways, so double spending, let's just say is the main problem.
Nick Szabo envisaged like a ownership registry.
So there would be a bunch of internet servers, and they would essentially vote on whether or not a transaction is valid or which transaction out of conflicting transactions is valid.

Sjors Provoost: 00:32:31

Yeah.
The key part there is it's at least not a central party that's doing it, but it's somehow decentralized, multiple people are tracking it, everybody can sort of check that it's at least, you know, maybe a bit honest.
I mean, there's certain things you can check because signatures are signatures, you can't forge them.
But if all these public parties keeping records disagree, it's hard to decide which is right.
You can't just count them, for example.

Aaron van Wirdum: 00:32:56

Yeah, well, the first thing you mentioned is interesting about the signatures.
So the problem is essentially that this registry, these servers, they can be corrupted in different ways.
For example, it wasn't Sybil resistant, or at least Nick Szabo hadn't come up with a robust way to make it Sybil resistant.
In other words, one guy could join with 10,000 different servers and just outvote everyone else and double spend everyone, there was no robust way of stopping that.

Sjors Provoost: 00:33:31

Yeah, it's basically all the Proof-of-Stake problems.

Aaron van Wirdum: 00:33:35

It's similar.
It didn't use Proof-of-Stake itself, but yeah, there was nothing at stake in that sense, that's for sure.
Nick Szabo at that time thought a potential mitigation against this is that users themselves can sort of keep an eye of what's going on.
Then let's say the Sybil attack happens, then the honest servers, the honest nodes in this registry system, they can split off.
They can say, no, that's someone's trying to cheat, we're just going to start our own registry.
Then users who are paying attention can see, yep, this registry is honest and this registry is not.
That was supposed to solve that problem, but it doesn't really.
For example, if you're offline, and you come online, and you weren't paying attention, you're a new user or something like that, you were just offline, you were on holiday, who knows?
All of a sudden there's two registries, there's no way to know which one was cheating and which one was not.

Sjors Provoost: 00:34:44

Exactly.
It sounds like you need to be online all the time and you need to download all the transactions.
It's like running your own Bitcoin node, although there wasn't an actual blockchain at the time, well, there may have been, sort of.

Aaron van Wirdum: 00:35:01

Yeah, wait.
The way you're phrasing it now sounds like it would have been a solved problem.

Sjors Provoost: 00:35:06

No, you would.
If you were to implement this system, then it sounds like everybody should just be verifying everything so that there is no third party.

Aaron van Wirdum: 00:35:14

Well, so that's what we're getting later.
But BitGold did not have this idea yet in any case.

Sjors Provoost: 00:35:20

No, no, the idea would be that there would be multiple servers doing this job, but in order to check the servers, the only logical conclusion to me would be that everybody has to check everything.

Aaron van Wirdum: 00:35:33

But you're very smart.

Sjors Provoost: 00:35:34

Well, and I have the benefit of hindsight.

Aaron van Wirdum: 00:35:37

Maybe mostly that.
Or both.
There is a fairly recent analogy we could draw from this non-solution, you could say, which would, for example, be Ethereum Classic and Ethereum, right?
At some point, a valid transfer happened on Ethereum and then that money was stolen back.
Then the people that stole it back said, no, we're the real Ethereum.
At that point, there were two Ethereums, and the actual Ethereum was forced to change its name, while the Ethereum where the theft happened went on, and that's what people today call Ethereum.

Sjors Provoost: 00:36:20

That's one perspective, and the other is that the people who call things Ethereum apparently do not primarily follow what the software says.

Aaron van Wirdum: 00:36:30

That's kind of the point.
So you can debate about this and there's no clear solution.
I still think what I said is correct.
I really mean that, but that's besides the point, the point is you're now expecting users to keep an eye on everything, so it wasn't really a good solution.
However, it was of course very innovative, it had a very innovative idea.
It was a big step into thinking about creating digital cash, specifically digital cash based on Hashcash, that wasn't backed by anything else.

Sjors Provoost: 00:37:03

Yeah, I think one innovation there compared to Digicash, because we talked about that earlier or e-cash.
In e-cash you have a mint, that's the entity that creates coins, and they are also the entity that is essentially the central bank that clears all transactions.
So there is a single point, the entity that issues the coins, that checks all the transactions, that kind of has a monopoly on the transaction log, or maybe not.
Whereas at least the issuance now is completely decentralized because everybody can deliver their Proof-of-Work.
I think that ingredient is there.
The verification, although still a bit hand-wavy, the idea is that it shouldn't be one entity.
I think he also was mentioning RPOW already, but that's something to discuss another time.

Aaron van Wirdum: 00:37:54

He was not mentioning RPOW because RPOW came years later.

Sjors Provoost: 00:37:59

Maybe I read a newer paper.

Aaron van Wirdum: 00:38:01

Yeah, that's probably it then.
Let's for the sake of convenience now imagine that this system would have worked.
Now you can create these strings and you can send them to other people, and there's this registry that keeps track of which public key owns which string.
Now we're getting close to something that looks like money, but there is a second big problem that BitGold was facing, or that it sort of solved?
The second big problem is that over time it becomes cheaper to produce valid hashes, right?

Sjors Provoost: 00:38:39

Yeah.

Aaron van Wirdum: 00:38:40

So at first, because computers just get better and better, it gets faster and faster, so it's easier and easier, cheaper and cheaper to create valid hashes.

Sjors Provoost: 00:38:48

And there's more of them.
That's actually not important that there's more of them, but that it is cheaper, costs fewer kilowatts of energy to do it.

Aaron van Wirdum: 00:38:57

Right, so the problem then is that the money isn't fungible necessarily.
It should be that each currency unit of the same denomination should be worth the same.

Sjors Provoost: 00:39:10

Well, either it's fungible, but in that case, all the money you created in the past is now worthless, so it's fungible, but highly inflationary.
Or it's not fungible, and that's I think the solution that he proposed, is where you value older work more.
So you say because this work was generated 10 years ago on a slower computer, we know that more energy was put into it, therefore we can correct for that.
Then the hope is that the market actually does that.

Aaron van Wirdum: 00:39:41

No, no, the market doesn't have to, if the market doesn't do that, that's even better.

Sjors Provoost: 00:39:45

Then it's highly inflationary.
So you mine your coins in 1999, you have a hundred of these coins, and now a hundred units of work.
Ten years later, somebody makes a hundred units of work in a fraction of a second, so either your hundred units of work are worth nothing in the future, or they are valued because they are old.
Whether the market will pick one of these two, I don't think there's any guarantee.
He does argue that there are some precedent(s), like that older collector items are worth more, a bit like Ordinals, I guess.
But that's not the part of Ordinals that's taking off the most.

Aaron van Wirdum: 00:40:18

Yeah, or like the misprints of certain postage stamps or something were worth more.
Yeah, so indeed he does argue that.
The idea that he proposed was we'll create a market for these strings, for these hashes, and on these markets people can trade them against each other.
So that's how the markets can figure out how much a 2005 hash is worth in relation to a 2015 hash.
So maybe one 2005 hash is worth ten 2015 hashes.
I should note all these hashes are also timestamped, they're made in order.

Sjors Provoost: 00:41:01

You can prove that they are a certain age.

Aaron van Wirdum: 00:41:06

Yeah.
Which is also another chapter in my book, Sjors, where I talk about the invention of timestamping.

Sjors Provoost: 00:41:12

Great.

Aaron van Wirdum: 00:41:13

I won't get on that detour.
So (in) BitGold there's this market for strings and you can figure out how much these strings are worth in relation to each other.
Then Nick Szabo's vision was there will be sort of banks, like in a free banking type of environment, where these banks will collect the different strings and bundle them together into buckets of strings of the same value.

Sjors Provoost: 00:41:39

This was written before the derivatives markets implosion in 2007, right?

Aaron van Wirdum: 00:41:47

Yes, we're in 1998, so yes.

Sjors Provoost: 00:41:50

Yeah, when all these triple A rated buckets and I'm thinking about what happened there.

Aaron van Wirdum: 00:41:54

Right, right, right.
Yeah, has nothing to do with this Sjors, but thanks for that color.
In my example earlier, where one 2005 hash is worth ten 2015 hashes, one bucket could consist of one 2005 hash, and another bucket could consist of ten 2015 hashes.
Now you have buckets of the same value.
These banks would then use these buckets, or these bundles, whatever you want to call them, to issue coins on top, digital coins still.
So for example, every bucket is worth 10,000 coins and these 10,000 coins are issued to people's account(s).
So now you have a digital form of cash that people can pay each other with.

Sjors Provoost: 00:42:41

That is actually Digicash, right, that layer on top?

Aaron van Wirdum: 00:42:45

Yeah, you could use e-cash for that.
I mean, it doesn't have to, it's free banking, you're free to do whatever you want, Sjors.
You could use e-cash for that, if you want to offer privacy to your customers and get customers that way.
But yeah, this was the idea.
So once you have 10,000 coins in my example, you can exchange them for an actual bucket of strings, and then you have the actual bucket, and you can maybe bring them to another bank.
Also because these strings, it's cryptographically provable who owns them, you can also have the proof of reserve type of stuff.
Nick Szabo was already thinking about that kind of stuff to address your 2008 concern, by the way.

Sjors Provoost: 00:43:27

Yeah, yeah, it's a free banking system.

Aaron van Wirdum: 00:43:31

So this was basically the idea of BitGold, did I miss anything?

Sjors Provoost: 00:43:37

Yes, so we talked about inflation and I guess these buckets also address the change problem, right?
Because another issue is that when you had the original e-cash system, you could go to a shop, and you would come with your 10 euros worth of this stuff, and they would immediately go to the bank, redeem it, and give you your change back.
So change wasn't a problem in the original system.
Change is also not a problem in Bitcoin because the transaction itself creates a change.
But in this system these strings don't have change.
So what you could do is somebody could make lots of small little pieces of work and distribute those, just like you would distribute small change, and then you go to a shop and you get these little strings back for your change, but it may be easier to do all this on a second layer and just have big buckets somewhere that don't need to be changed all the time.
Because also it would mean having to track all the movement of all these mini-strings, like tracking the movement of every penny on the planet.

Aaron van Wirdum: 00:44:39

Right, yeah exactly, it's interesting you mentioned that.
Nick Szabo was already thinking about second layer solutions, as are being developed and exist on Bitcoin today.
This was also sort of an original Nick Szabo vision to have different layers for different types of transactions.
So that's, that's BitGold in a nutshell, I think, Sjors.

## Conclusion

Sjors Provoost: 00:45:01

All right, well then I guess I can conclude that Bitcoin fixes this.

Aaron van Wirdum: 00:45:05

Yeah, we're going to make one more Genesis Book shill episode, right?

Sjors Provoost: 00:45:09

I think so, yeah.

Aaron van Wirdum: 00:45:10

Maybe next week or the week after we'll make one on B-money and RPOW.
Cool.

Sjors Provoost: 00:45:16

All right, then, in that case, thank you for listening to Bitcoin.

Aaron van Wirdum: 00:45:19

Explained.
