---
title: "Hashcash and Bit Gold"
transcript_by: kouloumos via tstbtc v1.0.0 --needs-review
media: https://bitcoinexplainedpodcast.com/@nado/episodes/episode-88-hashcash-and-bit-gold-a5cjn
tags: []
speakers: ['Sjors Provoost', 'Aaron van Wirdum']
categories: ['podcast']
date: 2024-01-03
---
Speaker 0: 00:00:18

Live from Utrecht, this is Bitcoin Explained.
Hey Sjoerds.
Yo, yo.
Are you going to do the jingle again?

Speaker 1: 00:00:26

I am not, but I know now that you are the best ad reader, so please read the ad.

Speaker 0: 00:00:45

Hardware stuff.
Shors, do you know what else they have?
They have the OpenDime, they have the BlockClock, I think, right?

Speaker 1: 00:00:51

Zetskart.

Speaker 0: 00:00:52

Zetskart.
They got everything you need.
What a coincidence.
That's our sponsor, CoinKite.
All right, Shors.
That was my read.
Hey, that's an improvement compared to last week, I think.
Probably.
What do you think?
We're getting there.

Speaker 1: 00:01:07

So, Aaron, you wrote a book.

Speaker 0: 00:01:08

Yeah.
Oh, yes, I did.
Cool.
It's, well, at the time of recording, it's almost published.
So we're publishing it tomorrow, January 3rd, but that's like midnight actually, UTC.
So it's like one hour time.
So in a couple of hours, Jors, my book will be live.
Yeah.
So that's

Speaker 2: 00:01:26

kind of cool.

Speaker 0: 00:01:26

So that's kind of cool.
It is called the Genesis book Shorts, And it tells the prehistory of Bitcoin, the origin story of Bitcoin.
It's the story of the people and projects that inspired Bitcoin.
So, of course, to celebrate that, we're going to discuss some of the topics from my book.

Speaker 1: 00:01:45

That's right.

Speaker 0: 00:01:46

So it's actually kind of for the first time, I think, not really an episode about Bitcoin.
Have we done something about it?

Speaker 1: 00:01:54

We've done an episode about DigiCash.

Speaker 2: 00:01:57

Well, no, hang on.
We also did the episode about the Tornado Cash.
That was actually

Speaker 0: 00:02:01

not about Bitcoin, kind of.

Speaker 1: 00:02:03

Exactly.

Speaker 0: 00:02:03

Anyways.

Speaker 1: 00:02:05

And we'll still cover things that are very relevant to Bitcoin.
Right.

Speaker 0: 00:02:08

Well, my entire book is very relevant to Bitcoin.
Everything in my book is relevant to Bitcoin, of course.
So of course, also what we're going to discuss.
Excellent.
Did I mention it's called the Genesis book and you can find it on the Bitcoin magazine store and Amazon and I don't know where else.

Speaker 1: 00:02:23

Sounds good.

Speaker 0: 00:02:24

I think, the, I, I, I'm, the Genesis book.com should be live by the time you listen to this, hopefully.

Speaker 1: 00:02:32

All right.

Speaker 0: 00:02:32

You want to know anything more about where you can find my bookshores?

Speaker 1: 00:02:35

No, but we will put it in the show notes.

Speaker 0: 00:02:37

Okay, we'll go to the episode then.
So yeah, we're going to discuss.
So okay.
I discuss in my book, there are sort of five main digital cash projects that are sort of precursors to Bitcoin in a way.
There are more, and there's also a lot more in the bookshores.
There's all kinds of background and stories and colors and storylines and adventures.

Speaker 1: 00:03:05

Yeah, from what I've been reading, you cover Austrian economic stories and sort of alternate the digital money story versus the political story.

Speaker 0: 00:03:16

Anyway, enough with the shilling.
Let's get to the actual episode.
So there's five electronic cash projects in the book that sort of have a bigger focus than some of the more minor ones.
So the first one of that is eCache, which was produced by DigiCache.
We're not going to talk about that because we kind of already did in episode 52, which was about, what was it about?
Fetiment, right?

Speaker 1: 00:03:43

Yeah.
In episode 52, Fetiment, we start all the way back with how David Chomps' E-cash works, how Blinded Signatures work, definitely recommended listening.
And then we go all the way to how that's now applied to, well, Pediment and Cashew.

Speaker 0: 00:04:00

Yeah, so to sort of, we're going to skip that one.
We're not, we're not going to talk about that again.
So instead this episode will be about Hashcash and Bitworld.
And I think this will be sort of, I don't know how we're going to do this format, which because usually I'm kind of the one who asks questions and We just still do that and I don't know.
We'll figure it out, I think.
Well, no, actually, I have no idea how to do this now.

Speaker 1: 00:04:22

Well, you should tell a little bit of the story and then we'll get to some of the technical juicy bits where I might have some opinions too.

Speaker 0: 00:04:31

Okay, cool.
Yeah.
So the first one is HashCash.
So the background here is, so in the nineties, the internet was becoming more popular and also there was the Cypherpunks mailing list.
And they had, first of all, they had their own mailing list where they were discussing privacy technologies, but also more ideological types of posts or how to create digital cash, of course, and all these kinds of discussions.
And they were also, a bunch of the cypherpunks were running remailers.
So this was sort of the precursor of Tor.
There was a way to send an email anonymously, send an email without the recipients knowing where the email came from.
The problem was that spam was becoming popular around this time as well.
So the Cypherpunk mailing list itself was being spammed.
Anyone else who had an email address was being spammed.
And especially also these remails or remailers were starting to be spammed to the extent that it was becoming burdensome to run one.
So it was potentially an attack on these remailers.
Either it was a spam attack that remailers were being abused for, or maybe it was just an attack on the remailers themselves, as sort of a denial of service type of situation.
So people wanted to create, Cypherpunks specifically wanted to create digital cash.

Speaker 1: 00:05:54

And I think, well, one step back, I think they also, they wanted to fix the spam problem, right?
With digital cash maybe in the back of their mind.

Speaker 0: 00:06:02

Sorry, I said digital cash, I meant digital postage, and that's what you're getting.

Speaker 1: 00:06:06

Yes, digital postage stamps.
But it might be interesting, something you also mentioned in the book is that there was a worry that if the cypherpunks didn't fix this problem, then governments would step in and they would start dealing with spam.
And this would be a problem because then you would get, if governments have to fight spam, then the way they would probably do that is by de-anonymizing everyone and basically KYC-ing email to the extent of where if there's a spammer, they know who they are.

Speaker 0: 00:06:36

Yeah.
Plus the government would then have to make a judgment call about what is spam and what kind of relevant to Bitcoin these days, actually with the whole ordinal thing.
But yeah, then governments have to make a judgment call about what is spam.
So what actually is legal?
And then by the time they can find a spammer, yeah, that would have to be some sort of identification.

Speaker 1: 00:06:54

And they would have to ban anonymous email, which is, you know, the kind of thing they were trying to do.

Speaker 0: 00:07:00

Right.
So the cypherpunks didn't like this and specifically Adam Back didn't like this.
Adam Back was of course one of these cypherpunks.
I don't think he needs an introduction to anyone who listens to this podcast.
So Adam Back wanted to come up with digital postage.
Maybe should I…

Speaker 1: 00:07:19

First I think we should go back in time, right?
Because everybody talks about HashCash and how Adam Beck invented that.
And he did, but it was not the first time it was invented as often happens in history.

Speaker 0: 00:07:30

Yeah.
I was also considering if I should talk about the other ways they were thinking about digital postage, but I think we should skip that.
Right.
That's what you can find in the book.

Speaker 1: 00:07:40

Exactly.

Speaker 0: 00:07:41

Okay.
So yeah.
Okay.
So shall I hand it to you here?
Because yes, so actually Adam Beck was not the first person to invent digital postage.
He did think he was, like he was not aware of the previous proposal, but there was actually another proposal that's a bit older and quite similar to Adam Back's proposal, which was the names from the top of my head.

Speaker 1: 00:08:06

Duerck and Naur.

Speaker 0: 00:08:07

Yeah, I was thinking of their first name, but yeah, their last names were definitely Duerck and Naur, Moni Naur and Cynthia Duerck, I think.

Speaker 1: 00:08:14

Yeah, and They did not come from a cypherpunk background.
They came from it with a just, hey, we are people using email and we don't like spam background.
And so they- – Well,

Speaker 0: 00:08:27

they were for IBM, right?
They were computer pros.
–

Speaker 1: 00:08:31

Yeah, they weren't random people, but they were not saying, how can we prevent the government coming into this email world?
It's just like, how do we get rid of spam?
And so they invented, essentially They came up with the idea of introducing proof of work for email, and they came up with three different work algorithms.

Speaker 0: 00:08:51

Yeah, and to be clear, the term proof of work didn't exist yet at this time.

Speaker 1: 00:08:55

I don't know exactly what they call it, but something along the lines of like a challenge or… But basically, they picked three algorithms, and I think one of them boiled down to finding, if you take a number and you wanna figure out which two primes are necessary, can be multiplied to get to the number.
So let's say you pick the number 100 and you say tell me which two prime numbers multiply to 100 and you would say I don't know because it's 10 times 10 so that's not those are not prime.

Speaker 0: 00:09:28

Kind of a bad example.

Speaker 1: 00:09:30

No it's a fine example but it shows that as soon as you give me the right answer, I can very quickly verify that, yes, these two numbers multiply to this total.

Speaker 0: 00:09:38

Actually, I

Speaker 1: 00:09:38

think you didn't have to find prime numbers, it's just modular prime number.

Speaker 0: 00:09:43

I think the way it works is you have two very big prime numbers, these are factored into another big number, and then the big number can only be produced by two specific prime numbers then, right?

Speaker 1: 00:09:56

I think that's RSA, but not what this here.
Oh, this

Speaker 0: 00:10:01

works a bit different?
I think

Speaker 1: 00:10:02

this was much simpler.
This was something called modulo a prime number.
So if you take a much smaller number we know the number 13 is prime, right?
And so you would say okay here's the number 10.
Find me two numbers that you can multiply to get the number 10, but you can multiply and then you do modulo 13.
So you can say this is not very good in math, but if you do 3 times 4 that's 12, So that's not enough.
If you do three times five, that's 15.
Modulo 13 is two, right?
So you can do et cetera, et cetera.
You keep looking for this number that if you go around in circles around this prime number, it gets you the correct result.

Speaker 0: 00:10:45

Okay, we're getting very into the weeds now.
Let's get back to the main road.
So they had three ideas.

Speaker 1: 00:10:50

Exactly.
So this is one of them and the key part is that it takes a while to find these numbers, but it's very quick to check.
You just multiply modulo and you're done.
And they had two other algorithms that I don't want to go into also because I don't know them, but they had an interesting property from them is that you could build an exception into it.
So basically saying, well, if you're the mailing list operator, then you can use this special key and you can bypass the work.
I don't know whether that would be practical or not, but that's sort of what they came up with.

Speaker 0: 00:11:23

Right, the backdoor function.

Speaker 1: 00:11:25

Yeah.

Speaker 0: 00:11:27

The points being here though, so was Nowr and Dwork also, like what they, the idea they come up with is that whatever calculation you have to make, you have to make it in combination with some data from the email itself.

Speaker 1: 00:11:41

Yes, because you can prove that you did a bunch of work, but if that's unrelated to your email, you would just reuse the same work.
So you have to make sure that the work is always a function of the email itself.
And ironically, they discovered the use of hash functions for that, or they knew that you needed hash functions for that part.
So you take the hash of the email, and then you use the hash as the starting point of your challenge.

Speaker 0: 00:12:05

Oh, they did use the hash for that part?
Yeah.
Oh, I didn't know that.
That's interesting.
Yeah, so because we should maybe spell this out for those who haven't realized this.
So Naor and Dwork were not using hashes for the proof of work.
They were using, what's it called?
Is there a better term for what they were?
They were

Speaker 1: 00:12:25

just using math problems.

Speaker 0: 00:12:26

Yeah, right.
Now the idea was still very similar to, I mean, I think most people that listen sort of know where proof of work came from, that's why we're sort of skipping some parts maybe, but we should actually spell it out.
So the idea was if you attach a little bit of proof of work to an email, Then most people that want to send an email, that's not really a problem.
That's like a couple of seconds of computing time.
However, if you're a spammer that wants to send tens of thousands, or maybe even millions of emails, which you usually have to do to be a profitable spammer, then it becomes so expensive that it's not worth it anymore.
So that's how it's postage.
So it's different in postage in the sense that you're not buying it from anyone.
And also whoever you're sending the email to is not getting the money or anything like that.
It's just, you're proving that you spend some resources, some energy, and that way it's too expensive for a spammer to be a spammer.

Speaker 1: 00:13:23

Yes, exactly.

Speaker 0: 00:13:25

Okay.
So that's what's now or and Dwork essentially came up with.
This was in 1992, but then independently, basically, it was sort of a parallel invention.
Not exactly parallel, though, you know, some time difference, but Attenbach was not aware of this solution.
So when they were discussing this problem on the Cypherpunks list, they didn't know it was actually kind of a solved problem.
But then he reinvented something very similar.

Speaker 1: 00:13:54

Yes, but then using a hash function, SHA-1 in this case, but that doesn't really matter.
And The thing is, it's not actually better or worse than the design that was made before.

Speaker 0: 00:14:08

Okay, explain how it works.

Speaker 1: 00:14:10

So you basically take some aspects of the email, as we said before, And then you add a nonce to it.
A nonce is a number that you pick randomly, doesn't matter what it is.
But you have to pick it such that the resulting hash starts with a certain number of zeros.
Right.
Notice that in Bitcoin Core, the hash does not only start with a number, certain numbers of zeros, but actually has a specific value that it has to stay under, but it's roughly the same idea.

Speaker 0: 00:14:37

Right, so then, yeah, you would send the email, you include this hash, and then the recipient would check if there's actually a valid hash in it.
If not, the email would just bounce.
Exactly.
So I guess that was the same with Nowrintworks system.
I didn't

Speaker 1: 00:14:54

spell that.

Speaker 0: 00:14:54

Yeah, I didn't spell that out, but same idea, basically.

Speaker 1: 00:14:57

Yep, they both have the concept of difficulty, essentially, where you can make the hash more or less difficult, depending on what your perceived spam problem is.

Speaker 0: 00:15:04

Yeah.
So anyways, the recipient will then say, or in the case of the remailers, right, which I mentioned earlier, the remailer will check, does this have a failed hash?
If not, just reject it.
And if so, it's forwarded to whoever it needs to be forwarded to.
So that's basically the idea of HashCash, right?
Did we forget about anything?
Yeah.
So that's HashCash.
I think that you, well, I can tell you that in the early days, there was some adoption of it.
So Apache used, is that how I pronounce it actually?

Speaker 1: 00:15:43

I think Apache, yeah.
Spam Assassin.

Speaker 0: 00:15:45

Yeah, they used it in Spam Assassin and Microsoft recreated something very similar.
Like it was incompatible with, you know, different standards, but basically the same idea again.
And then more recently…

Speaker 1: 00:15:59

And those two are completely unused right now because Spam Assassin removed it again and the Microsoft thing doesn't exist anymore.
More recently, as you're getting to, Tor is being used in proof-of-work.
So again, it's a completely different algorithm, but it is an example of proof-of-work being used outside of a cryptocurrency.
So where it's not used to produce value, it's simply to prevent spam.
So this concept is still alive and well.

Speaker 0: 00:16:27

Right.

Speaker 1: 00:16:27

Now, one interesting aspect I wanted to talk about…

Speaker 0: 00:16:33

This is why we're talking about it in a Bitcoin podcast.
Why we're focusing on Hashcash more than the NowrDwork concept, right?
Is that where you're getting at?

Speaker 1: 00:16:42

Yeah, well, there's an interesting kind of a historical coincidence, I would almost say.
And this is something you pointed out earlier that I think Adam Beck was aware of and he pointed it out, which is to say that there are two kinds of, well, there are multiple kinds of proof-of-work, but in particular two different kinds are stochastic and non-stochastic proof-of-work.
And that's a distinction I hadn't really thought about.
But the idea here is that you, with a hash function, you may or may not get the right result and it will take us, statistically will take a certain amount of time before you find a solution, but it's random.
So sometimes you find the right solution instantly, other times it takes a very long time.
Whereas with these earlier algorithms, There's a sort of a guaranteed time of how long it takes to find the square root, for example, of two numbers.
So I suppose you could maybe make it random, but assuming you use a standard algorithm, it'll take a fixed amount of time to find a solution.
And you might think-

Speaker 0: 00:17:46

let me give an analogy that I've used, not in the book, actually, I think, but in an article I wrote earlier, it's kind of the difference between, let's say there's a hundred lottery tickets and one person buys 40 tickets and another buys 60.
So now the person that has 60 has more chance to win 60%.
But the person that bought 40 still has 40% to win as well.
While if you take, you know, two cyclists and one of them can ride his bike 60 miles an hour and the other 40 miles, then any time they do a race, the one that can cycle 60 miles an hour will just win like every time.
Exactly.
There's no, there's every time the same cyclist will win.
There's no 40% chance that a 40 mile per hour cyclist will ever win.
It's just not going to happen.

Speaker 1: 00:18:35

And so if you translate that to the context of Bitcoin mining as it is today, let's say we had picked a non-stochastic form of proof of work based on that original paper.
So basically if Adam Beck had known about the original paper and had not bothered to implement something based on a hash function, because there's already a solution out there, then you would have the biggest miner, whoever that is, will just always find the next block first because they would always find that big prime number or whatever the challenge is.
They would always find it first.

Speaker 0: 00:19:04

Right.
It will be like that 60 mile cyclist rather than like currently Bitcoin mining kind of works like this lottery.
But if the biggest miner just always wins, then you can't have Bitcoin like we have it today.

Speaker 1: 00:19:16

And of course, we still have some centralization problems in that sense, but this would be centralization on steroids if we did not have hash-based proof of work.

Speaker 0: 00:19:23

Yeah, basically Bitcoin wouldn't work, like not as it's designed today.

Speaker 1: 00:19:27

Yeah, or maybe we would have figured it out and then changed it, but definitely would have been not optimal.

Speaker 0: 00:19:32

Yeah.
So essentially, what you alluded to, like we may have been quite lucky in that sense that Atomback wasn't aware of the prior proposal.
So he invented this in a way that's actually useful for Bitcoin.

Speaker 1: 00:19:45

Exactly.
But it's not something he was aware of at the time.
Or at least he didn't put it in the paper.

Speaker 0: 00:19:51

As far as I know, and I've discussed it with him, so either my memory is failing me, but I'm pretty sure he only realized that after Bitcoin himself.
He only figured that out, so that actually Hashkai specifically only works for Bitcoin.
Yeah, no, that was not some sort of pre-planned thing for Mr. Back.

Speaker 1: 00:20:09

Yeah, now before we get to the next topic, which is Bitgold, we should talk about something that the author of Bitcoin observed about proof-of-work.
That's kind of the bridge I wanted to make.

Speaker 0: 00:20:23

Yeah, well, that is also the bridge I make in my bookshorts.

Speaker 1: 00:20:26

Excellent.
Yes.
It's almost like I read it.

Speaker 0: 00:20:29

I mean, I think, at least if we're thinking about the same thing.
So yeah, you mean, so hash cash or proof of work essentially for the first time brought something aching to digital scarcity, created something, introduced something aching to digital scarcity Because there is an actual cost of physical cost energy in the real world required to produce it.
Yeah.
So rather than just copying numbers, you have to actually invest something, real resources, and that sort of creates something that you could see as digital scarcity, right?
That's what you're getting at.

Speaker 1: 00:21:05

That's not where we're getting it, though it is true.
Oh. What I'm getting at is that the question is how do you define proof of work, or how do you measure it?
How is it different from other cryptography?

Speaker 0: 00:21:18

This is not a bridge I make in my book, Jors.
Unless I'm completely confused where you're going.

Speaker 1: 00:21:23

It is a new bridge, but basically Nick Szabo wrote an article about something he calls now I lost the term, that's not smart.

Speaker 0: 00:21:33

You mean secure benchmark functions?

Speaker 1: 00:21:35

Yes, secure benchmark functions.
So here's the thing we know that with normal public key cryptography for example and with hash functions like SHA256 We know that it's easy to verify and easy is then defined as like just takes like a very short time on a typical computer and impossible or like you know it would take forever effectively to hack it, to coincidentally go back from the hash to the original from the public key to the private key which is then called hard.
But with proof-of-work you're doing something that's a little bit in between.
It is definitely not easy to go back to find a certain number of zeros, for example, in the proof-of-work in the hash, but it's also not hard in the sense that it will not take forever.
In fact, you don't want it to take forever because then you cannot, you know, make the proof-of-work on your email if it would take forever to make the proof-of-work.
So then the question is, how do you sort of define that?
How hard is hard enough?
Should not be too easy, should not be too hard.
And Nick Szabo wrote this paper, well this article about it basically, the coining of term secure benchmark function.
Now if you look at the 1992 paper about proof-of-work, they were also informally defining it as something that's not too easy, not too hard.
So, what in between?
So, Sabo put it in slightly more mathy terms.
And the analogy we could get into, I guess, is the one-way function, or what it's comparing it with.
So we talked about one-way functions in an earlier episode, where you actually were correct and I was wrong.
So I

Speaker 0: 00:23:16

remember that.
Good.

Speaker 1: 00:23:18

So keep enjoying that feeling.

Speaker 0: 00:23:20

Yes.
I think everyone heard that, right?
Can you repeat it one more time?

Speaker 1: 00:23:25

So let's just try and explain it correctly, because I don't even remember exactly what I was saying.

Speaker 0: 00:23:30

Go

Speaker 1: 00:23:31

on.
A one-way function is a function that is very easy to go in one way, like checking that a hash is correct, but very hard to go the other way.
She's like trying to produce a fake hash, no, a fake original, basically.
And there are a bunch of one-way functions out there.
One is finding the factors in a big number, or these prime factors as you mentioned with RSA.
Another is a discrete logarithm problem, or that's sort of a more generic one, but that is used for public and private key cryptography, like the elliptic curve.
And then there's cryptographic hash functions like SHA-256, which so far has not been broken.

Speaker 2: 00:24:21

The

Speaker 1: 00:24:22

problem is there is no mathematical proof that this actually exists.
So we think these functions are one-way, and They better be one-way, but it may turn out that some mathematician somewhere proves that they're not.
And then you get into the whole P is NP stuff that we're not going to get into.
Now, there is a special kind of one-way function called the Trapdoor One-Way Function.
That is public key, private key cryptography, where it is very hard to go back, it is very hard to go from a public key to a private key, in fact like, you know, take the age of the universe, unless you know the private key.
Then it's trivial.

Speaker 0: 00:25:03

Yes.

Speaker 1: 00:25:04

I think I said it wrong, it's like, it's very hard to fake a signature, for example, but if you know the private key, then it's trivial to make the signature.
And that is the trapdoor, the secret passageway through which you can do things.
So that was the distinction we wanted to make back then.

Speaker 0: 00:25:18

There actually is, sure, a chapter about this in my book as well.

Speaker 1: 00:25:21

Yeah, so then the secure benchmark function has to be less strenuous.
It can't be a one-way function because then you'll never go back.
So if you go to the Wikipedia article about one-way functions, it defines this little thing like, okay, for any blah, blah, blah function that you try a hundred thousand times or whatever, statistically you should almost never find the correct answer.
That's sort of how they defined it.
And then Szabo basically writes a similar formula, but then explaining what this secure benchmark function should look like.
And

Speaker 0: 00:25:58

the...
Sure, Are we still just making a bridge?

Speaker 1: 00:26:02

Yes, we are.
This is

Speaker 0: 00:26:03

a big bridge you're building here.

Speaker 2: 00:26:04

I'm almost

Speaker 1: 00:26:04

done with the bridge.
One thing that is interesting there is that when it comes to these one-way functions, it doesn't matter what hardware you have.
They just seem like you can have the whole universe and you still cannot crack it.
You can have a Dyson and you can't crack it.
But in the secure benchmark function, the device that you use, the machine that you do things on, actually matters in the math.
You cannot just abstract away the machine.
You have to say, okay, what is a realistic computer?
Because, and then you get back to the spam problem.
If a spammer has an ASIC, a modern-day ASIC, and let's say the algorithm was SHA-256 instead of SHA-1, well then you as a consumer trying to send an email would have to burn your phone to the ground in order to just send an email, but that guy with the ASIC can just spam a million people because per watt of electricity that you're putting into that ASIC you can just produce enormous amounts of spam, whereas your phone is less efficient so it would just get too hot.
And so that's why it's very hard to find functions that are hard enough, like that are easy enough for a phone, hard enough for an ASIC.
And he kind of anticipated that problem in that very short paper.

Speaker 0: 00:27:12

That was Shor's building, the Brooklyn Bridge over here.
Beautiful in its own right.

Speaker 1: 00:27:17

Exactly.
And that's why he needed, for his Bitgold proposal, he says like, yeah, make sure you, you know, whatever you do, because he didn't actually build the project, make sure it's one of those secure benchmark functions.

Speaker 0: 00:27:31

Yes.
Okay.
Yeah, in my book, I sort of muffle this way in a footnote, and I just call it hashes because Okay.
So, let's talk about bit goals.
I don't know if there's much specifically to introduce unless I you know, I can tell the whole story about how the cypherpunks want to create digital cash and the example was one of them, but let's At some point.

Speaker 1: 00:28:04

I think it might be interesting to mention the, I think it was like seven points that he describes that this system should

Speaker 0: 00:28:12

do.
Well, that was Adam Back.

Speaker 1: 00:28:15

Oh, I thought the BitGold paper also lists like seven properties of the system.
Basically like it has to be

Speaker 0: 00:28:20

in the BitGold paper.

Speaker 1: 00:28:22

Yeah.
Or at least it's

Speaker 0: 00:28:23

been a while since I read it.

Speaker 2: 00:28:24

Well,

Speaker 1: 00:28:24

maybe you just describe it in general terms.

Speaker 0: 00:28:27

BitGold itself.
Okay.
So we're getting more to the technical side then.

Speaker 1: 00:28:32

Yes.
What the architecture of the system is and how it should work.

Speaker 0: 00:28:35

Okay.
Yeah, I can do that.
Okay.
So basically Nick Szabo wants to create digital cash, right?
Hash cash was introduced.
So now there was something aching to digital scarcity.
Now It wasn't real digital scarcity, obviously, or at least it was at least not limited because over time it becomes easier and easier to create valid hashes.
There were a number of problems with hashcash, why you couldn't use it as money.
Also, of course, you can't pay someone with hashcash.
It's like a one-time use.

Speaker 1: 00:29:03

Yeah.
So what you're describing is the inflation problem, right?

Speaker 0: 00:29:06

Well, that's the one problem.
And also you can't transfer it to anyone.
Like you can't re-spend hashcash.
Yeah.
Right.
So it wasn't really digital money yet.
It was digital postage, essentially.
But it did introduce something aching to the digital scarcity.
And this idea inspired, for example, Nick Szabo to propose their own digital currency schemes.
Now, Bitgold was never implemented.
It was only ever a proposal, but it's still interesting.
So the way it works is you start with a candidate string.
The candidate string can be anything, I guess.
It doesn't really matter, but let's just say a random string of numbers.
And then with a proof of work or a secure benchmark function, as you just explained, that's how Nixarbo called it in his paper, I believe.
At least in one of his posts, he very specifically

Speaker 2: 00:30:03

called it that.

Speaker 0: 00:30:03

Yeah, I think in

Speaker 1: 00:30:04

the post I read, he just used all of the terms, but then made this benchmark a more specific definition.

Speaker 0: 00:30:11

Right, exactly.

Speaker 1: 00:30:12

But we can just call it proof of work because that's what it is.

Speaker 0: 00:30:14

Yeah, let's call it proof of work.
So you use proof of work.
So there's a candidate string.
Anyone can use proof of work to create a new valid hash, essentially.
Now the person who creates this valid hash becomes the owner of this hash.

Speaker 1: 00:30:32

So whoever creates it first.
Yeah.

Speaker 0: 00:30:33

Whoever creates this first.
Yeah.
I don't think it was specifically defined or specified how this initial ownership would work, but the obvious solution is you hash your public key with it.
And that would just be an easy way to do it, right?
Anyway, so whoever creates a valid hash using Proof-of-Work on the candidate string gets to own that string, and then the valid hash becomes the new candidate string.
So now everyone can start hashing that to find the next candidate string, which then, to find the next valid hash, which then becomes the next candidate string.
Okay, so that's how you own these strings, essentially.
Transferring strings is much like Bitcoin.
You sign a message saying, this string now belongs to this public key.
And if that message is cryptographically signed with the corresponding private key of whoever was owning it, whatever public key was owning it, then the transfer is valid.
The challenge was who gets to keep track of who owns what, or perhaps more specifically, how do you prevent double spending?
One person could sign one transaction or several transactions go to several people.

Speaker 1: 00:31:50

And how can you prevent, you know, afterwards multiple people saying that they found it first, right?
If the new thing was discovered.

Speaker 0: 00:31:58

Yes, right.
Yes, that too.
So there needs to be, you know, consensus on who owns what.
Also smaller, well, other problems are like, for example, censorship.
Anyways, so double spending, let's just say is the main problem.
And Xabo envisaged like a ownership registry.
So there would be a bunch of internet servers and they would essentially vote on whether or not a transaction is valid or which transaction out of conflicting transaction is valid.
Now.

Speaker 1: 00:32:31

Yeah.
So the, the key part there is it's at least it's not a central party that's doing it, but it's somehow decentralized, multiple people are tracking it, everybody can sort of check that it's at least, you know, maybe a bit honest.
I mean, there's certain things you can check because signatures are signatures, you can't forge them.
But if all these public parties keeping records either disagree, it's hard to decide which is right.
You can't just count them, for example.

Speaker 0: 00:32:56

Yeah, well, the first thing you mentioned is kind of interesting about the signatures.
So if...
Okay, wait.
So the problem is essentially that this registered, this pop, this registry, these servers, they can be corrupted in different ways.
So for example, it wasn't stable resistant, or at least an example hadn't come up with a robust way to make it civil resistant.
In other words, one guy could join with 10,000 different servers and just outvote everyone else and double spend everyone.
Like there was no robust way of stopping that.

Speaker 1: 00:33:31

Yeah, it's basically all the proof of stake problems.

Speaker 0: 00:33:35

It's similar.
Yeah, it didn't use proof of stake itself, but yeah, there was nothing at stake in that sense.
That's for sure.
Now, Nixzabo at that time thought a potential sort of mitigation against this is that users themselves can sort of keep an eye of what's going on.
And then if there's, let's say the civil attack happens, and then the honest servers, the honest nodes in this registry system, they can split off.
They can say, no, that's actually someone's trying to cheat.
We're just going to start our own registry.
And then users who are paying attention can sort of see, yep, this registry is honest and this registry is not.
And that was supposed to sort of solve that problem, but it doesn't really.
Like for example, if you're offline and you come in line and you weren't paying attention, so to say, you're a new user or something like that, you were just offline, you were on holiday, who knows?
And all of a sudden there's two registries, there's no way to know which one was cheating and which one was not.

Speaker 1: 00:34:44

Exactly.
It sounds like you need to be online all the time and you need to download all the transactions.
And then you can sort of, it's like running your own Bitcoin node, although there wasn't an actual blockchain at the time.
Well, there may have been, sort of.

Speaker 0: 00:35:01

Yeah, wait.
The way you're phrasing it now sounds like it would have been a solved problem.

Speaker 1: 00:35:06

No, you would.
If you were to implement this system, then it sounds like everybody should just be verifying everything so that there is no third party.

Speaker 0: 00:35:14

Well, so that's what we're getting later, sure.
But Bitgold did not have this idea yet in any case.

Speaker 1: 00:35:20

No, no.
The idea would be that there would be multiple servers doing this job basically.
But in order to check the servers, the only logical conclusion to me would be that everybody has to check everything.

Speaker 0: 00:35:33

But you're very smart.

Speaker 1: 00:35:34

Well, and I have the benefit of hindsight.

Speaker 0: 00:35:37

Maybe mostly that or both.
Well actually, so there is a fairly recent sort of analogy we could draw from this sort of non-solution, you could say, which would, for example, be Ethereum Classic and Ethereum, right?
At some point, a valid transfer happened on Ethereum and then that money was stolen back.
And then the people that stole it back said, no, we're the real Ethereum.
And at that point, there were two Ethereums, and the actual Ethereum was forced to change its name, while the Ethereum where the theft happens went on, and that's what people today call Ethereum.

Speaker 1: 00:36:20

I mean, that's one perspective, and the other is that, you know, the people who call things Ethereum apparently, you know, do not primarily follow what the software says.

Speaker 0: 00:36:30

That's kind of the point.
So you can debate about this and there's no clear solution.
And I mean, I still think what I said is correct.
Like I really mean that, but that's sort of besides the point, the point is you're now expecting users to keep an eye on everything.
So it wasn't really a good solution.
However, it was of course very innovative.
It had a very innovative idea of how you could sort of, you know, it was a big step into thinking about creating digital cash, specifically digital cash based on Hash Cash that wasn't backed by anything else.

Speaker 1: 00:37:03

Yeah, I think one innovation there compared to DigiCash, because we talked about that earlier or eCash.
In eCash you have a mint, that's the entity that creates coins, and they are also the entity that is essentially the central bank that clears all transactions.
So there is a single point, the entity that issues the coins, that checks all the transactions, that kind of has a monopoly on the transaction log, or maybe not.
Whereas at least the issuance now is completely decentralized because everybody can deliver their proof of work.
I think that ingredient is there.
And the verification, although still a bit hand-wavy, at least the idea is that it shouldn't be one entity.
And I think he also was mentioning RPOW already, but that's something to discuss another time.

Speaker 0: 00:37:54

He was not mentioning RPOW because RPOW came years later.

Speaker 1: 00:37:59

Maybe I read a newer paper.

Speaker 0: 00:38:01

Yeah, that's probably it then.
Where were we?
Okay, yeah.
So we saw, okay, let's for the sake of convenience now imagine that this system would have worked.
So now you can create these strings and you can send them to other people.
And there's this registry that keeps track of which public key owns which string.
Now we're getting close to something that looks like money, but there is a second big problem that Bitgold was facing with or that it sort of solved.
So the second big problem is that it over time becomes cheaper to produce valid hashes, right?
Yeah.
So at first, because computers just get better and better, it gets faster and faster, so it's easier and easier to cheaper and cheaper to create valid hashes.

Speaker 1: 00:38:48

And there's more of them.
Well, that's actually not important that there's more of them, but that it is cheaper, yes, costs fewer kilowatts of energy to do it.

Speaker 0: 00:38:57

Right.
So the problem then is that the money isn't fungible necessarily.
Like it should be that each currency unit is worth the same or each currency unit of the same denomination should be worth the same.

Speaker 1: 00:39:10

Well, either it's fungible, but in that case, all the money you created in the past is now worthless.
So it's fungible, but highly inflationary.
Or it's not fungible where you, and that's I think the solution that he proposed, is where you value older work more.
So you say because this work was generated 10 years ago on a slower computer, we know that more energy was put into it, therefore we can correct for that.
And then the hope is that the market actually does that.

Speaker 0: 00:39:41

No, no, the market doesn't have to.
If the market doesn't do that, that's even better.
Then

Speaker 1: 00:39:45

it's highly inflationary.
So you mine your coins in 1999, you have a hundred of these coins, and now a hundred units of work.
And now ten years later, somebody makes a hundred units of work in a fraction of a second.
So either your hundred units of work are worth nothing in the future, or they are valued because they are old.
But whether the market will pick one of these two, I don't think there's any guarantee.
He does argue that there are some precedent, like that older collector items are worth more, a bit like ordinals, I guess.
But that's not the part of Ordinalis that's taking off the most.

Speaker 0: 00:40:18

Yeah, or like I think the misprints of certain postage stamps or something were worth more.
Yeah, anyways, yeah, so indeed he does argue that.
So the idea that he proposed was we'll create a market for these strings, for these hashes.
And on these markets, people can trade them against each other.

Speaker 2: 00:40:39

So

Speaker 0: 00:40:40

that's how the markets can figure out how much is a, you know, 2005 hash worth in relation to a 2015 hash.
So maybe one 2005 hash is worth 10 2015 hashes.
I should note all these hashes are also timestamped.
Like first of all, they're of course made in order.

Speaker 1: 00:41:01

You can prove that they are a certain age.
Yeah.

Speaker 0: 00:41:06

Yeah.
Which is also another chapter in my book, Chores, where I talk about the invention of timestamping.

Speaker 1: 00:41:12

Great.

Speaker 0: 00:41:13

But I won't get on that detour.
So Bitgold, yeah, so there's this market for strings and you can figure out how much these strings are worth in relation to each other.
Then Nick Szabo's vision was there will be sort of banks, like in a free banking type of environment, where these banks will collect the different strings and sort of bundle them together into, you know, buckets of strings of the same value.

Speaker 1: 00:41:39

This was written before the derivatives markets implosion in 2007, right?

Speaker 0: 00:41:47

Yes, we're in 1998, So yes.

Speaker 1: 00:41:50

Yeah, when all these triple A rated buckets and I'm thinking about what happened

Speaker 0: 00:41:53

there.
Right, right, right.
Yeah, has nothing to do with this short, but thanks for that color.
So in my example earlier, where one 2005 hash is worth 10 2015 hashes, one bucket could consist of one 2005 hash and another bucket could consist of 10 2015 hashes.
So now you have back buckets of the same value.
And these banks would then use these buckets or these bundles, whatever you want to call them, to issue coins on top of digital coins still.
So for example, every bucket is worth 10,000 coins and these 10,000 coins are issued to people's account.
So now you have sort of a digital form of cash that people can pay each other with.

Speaker 1: 00:42:41

And once someone would be, that is actually digi cash, right?
That layer on top.

Speaker 0: 00:42:45

Yeah.
You could use e-cash for that.
Yeah.
I mean, it doesn't have to like in a free it's free banking.
You're free to do whatever you want.
Sure.

Speaker 2: 00:42:50

Yep.
But Yeah, you could use e-cash for that.
Yeah.
I mean, it doesn't have to like in a free it's free banking.
You're free to do whatever you want.
Sure.
Yep.

Speaker 0: 00:42:51

But yeah, you could use e-cash for that.
If you want to offer privacy to your customers and, you know, get customers that way.
But yeah, this was the idea.
So once you have 10,000 coins in my example, you can exchange them for an actual bucket of strings, and then you have the actual bucket and you can maybe bring them to another bank or, and also because this is all like these strings, it's cryptographically provable Who owns them, you can also have like the proof of reserve type of stuff.
Like Nick Zabo was already thinking about that kind of stuff to address your 2008 concern, by the way.

Speaker 1: 00:43:27

Yeah.
Yeah.
It's a free banking system.

Speaker 0: 00:43:31

So this is how, yeah, this was basically the idea of Bitgold.
Did I miss anything?

Speaker 1: 00:43:37

Yes, so we talked about inflation and I guess this sort of these buckets also address the change problem, right?
Because another issue is that when you had the original e-cash system you could go to a shop and you would come with your 10 euros worth of this stuff and they would immediately go to the bank, essentially redeem it and give you your change back.
So change wasn't a problem in the original system.
Change is also not a problem in Bitcoin because the transaction itself creates a change.
But in this system these strings don't have change so what you could do is somebody could make lots of small little pieces of work and distribute those just like you would distribute small change and then you go to a shop and you get these little strings back for your change but it may be easier to do all this on a second layer and just have big buckets somewhere that don't need to be changed all the time.
Because also it would mean having to track all the movement of all these mini-strings.

Speaker 2: 00:44:35

Like

Speaker 1: 00:44:35

tracking the movement of every penny on the planet essentially.

Speaker 0: 00:44:39

Right, yeah exactly.
It's interesting you mentioned that.
Nixzabo was already thinking about second layer solutions, you know, as are being developed and exist on Bitcoin today.
This was also sort of an original Nixabo fission to have different layers for different types of transactions.
Yes.
So that's, that's Bitgold in a nutshell, I think, Jors.

Speaker 1: 00:45:01

All right.
Well then I guess I can conclude Bitcoin fixes this.

Speaker 0: 00:45:05

Yeah.
Well, we're going to make one more Genesis Book Chill episode, right?

Speaker 1: 00:45:09

I think so.
Yeah.

Speaker 0: 00:45:10

Maybe next week or the week after we'll make one on B-money and ARPAO.
Cool.

Speaker 1: 00:45:16

All right, then.
In that case, thank you for listening to Bitcoin Explains.
