---
title: Schnorr Signatures and Libsecp256k1
transcript_by: Sjors, edilmedeiros
media: https://www.youtube.com/watch?v=RUhI0R4FMEo
tags:
  - libsecp256k1
  - schnorr-signatures
speakers:
  - Sjors Provoost
  - Aaron van Wirdum
date: 2021-09-18
episode: 9
summary: In the episode of The Van Wirdum Sjorsnado, Aaron and Sjors discuss what the libsecp256k1 library is, why it matters for Bitcoin, and what it means that Schnorr signature support was merged.
---
Aaron Van Wirdum: 00:03:59

We're going to discuss libsecp25, it's a long name.

Sjors Provoost:

Libsecp256k1.

Aaron van Wirdum:

Thank you.
Why are we going to discuss it? We are going to discuss it because BIP 340 support was merged into libsecp256k1 this week.

Sjors Provoost:

What was merged?

Aaron van Wirdum:

Shut up.

Sjors Provoost:

Schnorr was added.

Aaron van Wirdum:

Okay yeah, so Schnorr, exactly.
Thank you for actually making it clear for our listener.
Oh, I misunderstood your question, yeah.
Schnorr was added.
So libsecp256k1 is a library.

Sjors Provoost:

That's right.

Aaron van Wirdum:

And we're going to explain what this library actually is or why it exists or what it does.
And the reason we're going to explain that is because I actually didn't know that much about it.
It's one of these things for me that I heard about and I kind of know what it is, but I never really got into it to any sort of serious extent.
Okay, libraries first of all.
Let's start with libraries.

Sjors Provoost:

Let's talk about libraries.

## Software Libraries

Aaron van Wirdum:

There's a thing called software libraries.
And I'll just let you explain what a software library is, first of all.
So for any programmer that's listening, this is probably going to be very noobish for you, but for people like me this is actually kind of interesting.

Sjors Provoost:

The easiest way to explain the library is it's a reusable piece of software.
So yeah, for example OpenSSL is a library we'll talk about.
It is a piece of software that lets you do all sorts of cryptographic operations from creating random numbers to signing stuff with every curve under the sun.
But it's not an actual program, it doesn't really do anything by itself, but other programs can use a library to do whatever they want without having to rewrite that stuff.

Aaron van Wirdum:

Or I assume you can take part of the library, not necessarily the whole library, but get a specific.

Sjors Provoost:

You take the entire library but you use a subset of it.

## OpenSSL

Aaron van Wirdum:

Exactly, yes.
So Bitcoin was at some point in the past relying on OpenSSL.

Sjors Provoost:

Yeah, until actually very recently, a few months ago.
But for less and less and less stuff.
So in the beginning, OpenSSL was used for all the things.
In particular, the reason it was needed is because Satoshi picked a cryptographic curve, the libsecp256k1 curve because it was pretty and OpenSSL had support for it.
So he did not have to write all this cryptographic functionality, which of course you never want to do yourself because it's very dangerous to write your own cryptographic stuff.
And this is also a reason why he didn't use Schnorr because there was no library for it.
There were other reasons, but this was a reason, a very practical reason.

Aaron van Wirdum:

So just to be clear, when you say Bitcoin Core Satoshi used this library, the OpenSSL library, like how does a software program actually use a library?

Sjors Provoost:

You just Google on Stack Overflow how to use OpenSSL and then you just look at the examples.

Aaron van Wirdum:

Let me rephrase the question.
Where is the library?

Sjors Provoost:

Oh, the library is included in the software package when you download it.
And the binary file contains some of the Bitcoin Core specific stuff, and then a whole bunch of libraries, and that's what makes it so big, around 20 megabytes.

Aaron van Wirdum:

Right, so when you download Bitcoin Core, the software, Bitcoin Core 20 is the newest one I guess, then you actually download, when in this case now OpenSSL anymore, but for Bitcoin 19 you actually downloaded a whole OpenSSL library.

Sjors Provoost:

Yeah, that's correct.

Aaron van Wirdum:

And then it's hosted on your computer from that point on, just you have the library on your computer, your real computer.

Sjors Provoost:

Right.
Now there is two ways to go about that.
You can have a library sitting on your computer already, and then software can say, "Let me just see if I can find that library and I'll use that." Then your download gets smaller.
But the problem is that libraries change and so you don't want to be surprised about what's on the computer, especially with cryptographic stuff.
And even if you include in the download, you can be surprised by what happens to the library because somebody else is maintaining that library and if you're not paying attention to what that other person is doing, they might break something very bad.

Aaron van Wirdum:

So in the case of, let's stick to Bitcoin Core 19.

Sjors Provoost:

Well, in this case maybe take an older one because I think it was Bitcoin Core 0.8 or something.

Aaron van Wirdum:

Let's take Bitcoin Core, I don't know where you're going with this, but lets take that one.
So someone else is maintaining this library?

Sjors Provoost:

Yeah.

Aaron van Wirdum:

Bitcoin Core developers are maintaining Bitcoin?

Sjors Provoost:

Yeah.

Aaron van Wirdum:

They write something in the code, they use some part of the library, you download the library from the Bitcoin Core code, the part of the library is used, and then the Bitcoin Core developers may not have noticed some change that happened to the library and all of the sudden the stuff they wanted Bitcoin Core to do isn't actually doing what they wanted Bitcoin Core to do because the library wasn't doing what they thought it would do because someone else was maintaining the library.
Is that a correct summary?

Sjors Provoost:

Yeah, that's right.
And to clarify what specifically happened here...

Aaron van Wirdum:

You picked Bitcoin Core 8 because there was a specific example you wanted to go to.

Sjors Provoost:

Yeah, I might be wrong about the number because Bitcoin Core 8 had a different problem.
But sort of around that time, there was another bug in OpenSSL that I believe was unrelated to the problem that happened.
But they basically had to upgrade OpenSSL because the old version was simply not safe.
But unbeknownst to the Core devs, there was another change in OpenSSL when they upgraded.
And in particular, this was about when you see a signature, do you consider it valid or not? And the original version of OpenSSL was pretty relaxed, so it would accept signatures as valid even if they did not meet the exact spec.
And they wouldn't be signed by somebody else, so it wasn't about stealing funds, but it was just you could be a little bit sloppy about maybe you add a byte to the signature or maybe not.
So the notation could be a bit sloppy.
And the new version was very picky.
Now, if you use Bitcoin software to create a transaction, that was not a problem, because any Bitcoin transaction was signed very strictly according to the protocol.
But if you are now validating these transactions, if you use old software and you would see a sloppy version that was made with some other piece of software, the old software would be fine, the new software would say it's invalid.
So all of a sudden you have an accidental soft fork.

Aaron van Wirdum:

Right.
And that's what actually happened.
That's the BIP 66 one? Is that what we're talking about here?

Sjors Provoost:

Correct.
BIP 66 was introduced because people became aware of this problem, at least some of the developers became aware of this problem.
So they knew there was an accidental software time bomb basically in the code, and so they proposed BIP 66 saying, "Oh, by the way, we should be more strict about what these signatures look like," without saying, "Oh, by the way, there's a bug in OpenSSL so we better do this now."

Aaron van Wirdum:

Oh, it was like a secret bug fix of the problem with OpenSSL?

Sjors Provoost:

Yes.

Aaron van Wirdum:

I don't think I knew that, okay.

Sjors Provoost:

OpenSSL essentially improved itself by becoming more strict, but that made it a consensus change because what's consensus code it's also whatever your libraries are doing.
So basically OpenSSL introduced a soft fork but without saying, "Oh, there's no deployment date in the OpenSSL update," it just randomly happened.

Aaron van Wirdum:

Right, so that's a great example of why a dependency because that's the official term is a problem.

Sjors Provoost:

Yeah, exactly.

Aaron van Wirdum:

This is a good example of that.
And there have been more problems with OpenSSL I think.

Sjors Provoost:

I mean, OpenSSL is famous for its vulnerabilities, and you know the main big reason behind that is that these libraries are used by everyone for decades, but they're only maintained by like one guy in Germany who doesn't get funded.
It's just like cURL is another famous example of that, it's a library that downloads files, cURL it's used everywhere, it's probably used in the space shuttle.
But there's just one guy that maintains it and nobody's helping.
And it's not good when the entire internet relies on it.
And in the case of OpenSSL, yeah there have been plenty of bugs and it's very easy to make mistakes with cryptographic code.
And it's written in C, so you forget a semicolon, whoops, now you're skipping a line.
So one of the bugs that was called Heartbleed.

Aaron van Wirdum:

Yeah, that was fairly recent, a couple years ago.

Sjors Provoost:

Yeah, a couple years ago.
I think it was a missing colon or literally just one character mistake that allowed you to log into any computer on the internet.

Aaron van Wirdum:

Effected everything.

## Libsecp256k1 Origins

Sjors Provoost:

Without a password.
That's the sort of severity.
And something like that in Bitcoin of course could mean, "Oh, now we have a problem, everybody can just steal all the money." At the same time, Pieter Wuille was working on a library.

Aaron van Wirdum:

For our American and English listeners, that's Peter Wuley or however they want to pronounce it.

Sjors Provoost:

Yeah, or sipa or sippa.

Aaron van Wirdum:

Pieter Wuille, go on.

Sjors Provoost:

He was working on a library, so a piece of software, that was specifically designed to create and verify Bitcoin signatures.
And his original motivation was just to do it faster than OpenSSL.

Aaron van Wirdum:

Okay, so it wasn't a security motivation, it was just a performance improvement motivation.

Sjors Provoost:

Exactly, he explains this in a podcast he did with Chaincode, so if you Google that, or it might be in the show notes.
Basically, he wanted to make it, I think about four times faster and he could try and modify the OpenSSL code itself, but apparently it's such a nightmare to change any of that code and also the OpenSSL code is very generic, it has to support all different kinds of cryptography.
So it's more difficult, if you want to change anything you have to be very abstract in all the things you do.
So it's just like when you write a law, you can't just say, "John can't go to the supermarket," you have to say something like, "Well, anybody over 20 centimeters in size cannot go to the supermarket." So it's very difficult to write these abstract documents.
So he basically wrote it from scratch, specifically for that curve, and it was added to Bitcoin Core I think pretty early, but just to verify signatures, and then later on also to create signatures.
And that coincided with the security vulnerability.
But I don't think it was the cause of it, it was sort of around the same time.
It was like, "Okay, we've had this near miss, we could have had a serious problem, let's not use OpenSSL for that critical stuff anymore."

Aaron van Wirdum:

Yeah, so then the goal was to get rid of that dependent, now I forget the word.

Sjors Provoost:

Yeah, to get rid of the dependency.

Aaron van Wirdum:

Dependency.

Sjors Provoost:

Exactly.

Aaron van Wirdum:

And writes a whole new cryptographic software library for Bitcoin.

Sjors Provoost:

Right.
It's just the curve.

Aaron van Wirdum:

Just eliptic curve, just the thing that's used for signatures.

Sjors Provoost:

Yeah, because there's other cryptographic code in the Bitcoin Core code base.
For example, SHA-256 is in there and a few other curves.
And I think those were originally also from OpenSSL.
Those things are a little bit less scary, you can implement SHA-256 in a day if you're bored in any programming language.

Aaron van Wirdum:

Does it still use libraries for that though or was that rewritten?

Sjors Provoost:

No, so SHA-256, as far as I know, is directly in the code.
So it's just copy pasted from somewhere and then improved.

Aaron van Wirdum:

Right, got it.
So libsecp256, am I saying that right?

Sjors Provoost:

Libsecp256k1.

Aaron van Wirdum:

Thank you, that was meant as a performance improvement, then it was pivoted to actually be a new library for Bitcoin or at least sort of Bitcoin specific library to get rid of this dependency? You mentioned this before, but isn't that also a risk? Like rolling your own crypto?

Sjors Provoost:

Absolutely, absolutely.
So the fact that this thing was reviewed by a lot of people, a lot of good cryptographers before adding it, and I think it was also compared against OpenSSL in terms of using the same tests.
But yeah, at some point you have to take that risk because the other one is just waiting for OpenSSL to explode.

Aaron van Wirdum:

Plus it was Pieter Wuille, so can't really go wrong with that.

Sjors Provoost:

Well, you'll want to have proof of wuille.
But a lot of very smart people looked at it, probably the same people who would also look at OpenSSL.
So that's good, but you don't want to make a habit of this, and in fact they do constantly make very small tweaks to that library to make it a little bit faster, but you want to be very careful with that.

Aaron van Wirdum:

Okay, so that's the library.
Bitcoin has its own library now.
Is this used by any other programs?

Sjors Provoost:

But keep in mind is turtles all the way down, because OpenSSL is also just written by people.
So everything is an implementation at some point.

Aaron van Wirdum:

Sure.

Sjors Provoost:

Okay, so your question?

## Other uses of libsecp256k1

Aaron van Wirdum:

I guess my first question would be, is this library used by anything other than Bitcoin?

Sjors Provoost:

Yes, so this library is, I just heard it on a podcast with Vitalik, it's also used by Ethereum and a whole bunch of other cryptocurrencies.
Basically any cryptocurrencies that uses the secp256k1 elliptic curve, which is just a nice mathematical object.

Aaron van Wirdum:

Right mostly cryptocurrencies though, only cryptocurrencies.
It's pretty cryptocurrency specific, at least.

Sjors Provoost:

Yeah, I'm not aware of any non-cryptocurrency project that uses it.
It could.
It's just a library that allows you to sign stuff, sign messages and verify the signature on a message.
So you could write an encrypted chat application that uses this curve if you wanted to, but I don't know, I guess the encrypted chat applications out there might have their own curve that they use for their thing, I don't know what Signal uses, but they could.

Aaron van Wirdum:

Okay, so that's libsecp256k1, I keep having to pronounce this.

Sjors Provoost:

Yeah, we'll just splice it in the audio later.

Aaron van Wirdum:

I'll just call it libsec.
Is there anything else that's called libsec that would confuse people?

Sjors Provoost:

Libsecp.

Aaron van Wirdum:

Libsecp, okay.
So libsecp.
Is that everything we need to know about libsecp?

Sjors Provoost:

I think so.

## Schnorr Signatures

Aaron van Wirdum:

Yeah, so BIP 340 was merged, which is Schnorr.

Sjors Provoost:

Exactly.

Aaron van Wirdum:

This has been in development for a long time as well I think for years.
So this is also a new implementation, so this is the first time Schnorr has been included in any library because you just mentioned that it wasn't-

Sjors Provoost:

I don't know about any library, but at least at the time when Bitcoin was created, there was no library for Schnorr or at least it wasn't in OpenSSL, which is a widely tested library.
You wouldn't just want to randomly download, "Oh look, somebody implemented Schnorr." 
So what happened is, I think Satoshi was aware of Schnorr but there was a patent on it and there was no implementation, so it was kind of both of these things.
Because I think the patent was actually expired in 2008.

Aaron van Wirdum:

Yeah, I think it just lapsed or something, yeah.

Sjors Provoost:

But either way, you don't just want to write this stuff from scratch.
And if you try and develop a world changing thing, you don't want to then spend three years just implementing the cryptography, given how long it takes to really do this.
But actually Schnorr is simpler, and I think we may have explained this in an earlier episode.

Aaron van Wirdum:

You mean simpler than?

Sjors Provoost:

Than ECDSA.

Aaron van Wirdum:

Which is the elliptic curve algorithm, that Bitcoin currency currently uses.

Sjors Provoost:

Right, and which the libsecp library implements.
But the thing is, you have the same elliptic curve but then in order to make a signature, you have to do slightly different calculations with it.
So that also means that the change for Schnorr is not as complicated as, say the initial version of libsecp was.
The initial version of libsecp had to implement the curve, all the operations you can do in a curve like addition and multiplication, and then implement the signature algorithm of ECDSA.
But in order to do Schnorr, you just need to do the signature algorithm for Schnorr, you don't have to do all the math, the basic foundational math.
So it's not a huge change, it's not like adding a whole new curve to it.
It would be much more difficult to add, say, a different elliptical curve or even a completely different kind of curve than it is to change just from ECDSA to Schnorr, it's a different way of signing, and in fact a simpler way of signing.

Aaron van Wirdum:

Okay.
So this was implemented, again, by Pieter Wuille, I assume, well I know, right?

Sjors Provoost:

The spec was written by him, I think he also wrote most of the implementation, but there's a lot of people on top of that.

Aaron van Wirdum:

There's others, sure.
And it was merged this week.
So what does that mean exactly, where does this get us?

Sjors Provoost:

So what that means is there now is an updated version of this library, but nobody's using that library yet.
And another change is that Bitcoin Core was changed I think a few days ago to include that new version of the library.
To include it, not to actually use it in any way.

Aaron van Wirdum:

So the first major release of Bitcoin Core, when you download that you'll download the library that includes Schnorr.

Sjors Provoost:

Exactly, because the usual process is stuff gets merged into the master branch in GitHub and every six months or so we say, "Okay, let's stop at this point and release whatever is in there," and so next time that'll include the Schnorr code.
Yeah, it'll be in there, it might not do anything.
It might have a few tests that try it, if you don't run the tests you're not going to run it.

Aaron van Wirdum:

Yeah, the next Bitcoin Core release is not going to use Schnorr yet, is your prediction here.
That's your bold prediction?

Sjors Provoost:

I would say it would be extremely reckless if it did.
But there are projects that use it, certain Bcash coin uses Schnorr, I believe.

Aaron van Wirdum:

Oh yeah, I think so.

Sjors Provoost:

But the actual spec for Schnorr was changed a little bit, so I don't know if they're going to change along with it or not.
Not a huge change.

Aaron van Wirdum:

So anyways, it's going to include a library next time you download it.
You're downloading this but it doesn't actually do anything probably, or not anything too important.
But that would be a next step then.
Like I want to excite our audience.
We're getting somewhere, right?

Sjors Provoost:

Yeah, we are.

Aaron van Wirdum:

That's the plan, right?

Sjors Provoost:

So the idea here, of course, is to have Schnorr as part of taproot.
So the entire taproot thing, there are already pull requests that describe what it's supposed to do, not completely finished but pretty far along.
So maybe they'll go in the next version, so not in the upcoming one but the next one.
What I would imagine happens is that it get added not to Mainnet, probably not even to Testnet, but to this new thing called Signet, which is a whole new type of way to do Testnet, which we can do another episode about.
But basically, it'll go in as some innocent ways, so maybe there's just tests for it, tests for everything taproot related, and then anybody who knows how to compile code can just flip a switch and try it on their own machine, but it won't be on Mainnet or probably not even on Testnet.
And then maybe next version, this stuff takes time.

Aaron van Wirdum:

Isn't that exciting our audience? Got to pump it, got to pump this coin Sjors.

Sjors Provoost:

I'm pumping low time preference.
This stuff takes a long, long time.
But basically you add all the code in it, so everything is in there but you don't activate it yet, and then the next time you decide on activation mechanisms, and even those mechanisms might take a while.

Aaron van Wirdum:

That's a whole debate on its own, which we did an episode about, right, if I'm not misremembering?

Sjors Provoost:

Yes.

Aaron van Wirdum:

So, that's what a library is.
That's what a libsecp256k1 library specifically.
Now you also know what Schnorr is, actually we didn't even get into what Schnorr is.
Did we do that in a previous episode?

Sjors Provoost:

I can briefly recap.

Aaron van Wirdum:

Sure, go for it.

Sjors Provoost:

So it's simpler.

Aaron van Wirdum:

What's Schnorr actually Sjors?

Sjors Provoost:

So what happened is there was this patent on this very simple system called Schnorr by a person called Schnorr, and it was very nice, it was a good way to make electronic signatures, but there was a patent on it.
So people came up with a way to convolute the design, make it more complicated, such that it would no longer fall under the patent.
So when the lawyers said, "Okay, this looks obscure enough," so they were just adding numbers to it and abstracting things, just making it more complicated.
And then it didn't violate the patent and so they shipped it.
But now we ended up with this horrible thing that is basically proof of lawyer, convoluted mess, and now that the patent's expired we just go right back to the original design, which is much better.
And mainly it's better because you can add signatures much more easily, and adding signatures is very nice.

Aaron van Wirdum:

Yeah, you can perform math on it.

Sjors Provoost:

Yeah, you could perform math on the original one, you'd be able to publish papers just on the ability to add two numbers.

Aaron van Wirdum:

Right.
Yeah, so for the layman listener, performing math on it just means you can do cool mathematical tricks like add numbers to both the signature or both publicly key and the private key and then it still adds up and still works or you can add signatures or all that kind of cool stuff.

Sjors Provoost:

Yeah, which in the end translates to more privacy and less block space usage, so it's all good.
