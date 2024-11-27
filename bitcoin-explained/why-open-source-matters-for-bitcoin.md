---
title: Why Open Source Matters For Bitcoin
transcript_by: Sjors, edilmedeiros
media: https://www.youtube.com/watch?v=_qdhc5WLd2A
tags:
  - bitcoin-core
  - reproducible-builds
speakers:
  - Sjors Provoost
  - Aaron van Wirdum
date: 2020-12-18
episode: 21
summary: |-
  In this episode of "The Van Wirdum Sjorsnado, " hosts Aaron van Wirdum and Sjors Provoost discussed why it matters that Bitcoin software is open source and why even open-source software doesn't necessarily solve all software-specific trust issues.

  In theory, the fact that most Bitcoin nodes, wallets and applications are open source should ensure that developers can’t include malicious code in the programs: anyone can inspect the source code for malware. In practice, however, the number of people with enough expertise to do this is limited, while the reliance of some Bitcoin projects on external code libraries (“dependencies”) makes it even harder.

  Furthermore, even if the open-source code is sound, this doesn’t guarantee that the binaries (computer code) really correspond with the open-source code. Van Wirdum and Provoost explain how this risk is largely mitigated in Bitcoin through a process called Gitian building, where several Bitcoin Core developers sign the binaries if, and only if, they all produced the exact same binaries from the same source code. This requires special compiler software.

  Finally, the hosts discuss Guix, a relatively new project that goes above and beyond the Gitian process to minimize the level of trust required to turn source code into binaries — including trust in the compiler itself.
---
## Intro

Aaron van Wirdum:

Live from Utrecht, this is the Van Wirdum Sjorsnado.

Sjors Provoost:

Hello.

Aaron van Wirdum:

This episode, we're going to discuss open source?

Sjors Provoost:

Yes.

Aaron van Wirdum:

I'm just going to skip over the whole price thing.
We're going to discuss open source and why it's useful, or free software and why it's useful.
Are you on the free software train or on the open source train?

Sjors Provoost:

I'm on every train.
I like trains, but tell me-

## Open source philosophy

Aaron van Wirdum:

I can tell you the difference because a lot of people don't know this.
There isn't a lot of difference except for a philosophical difference.
So the idea is that Richard Stallman, he founded the free software movement.
And the idea there was if software is closed source, then there is a power relationship between developers and users, because users don't know what software they are running.
And we'll get to this in a bit, I guess.
Well, I can explain this very briefly right now.
The reason is, and you know this, but I'm explaining it to our listeners, the reason is that the actual software you're running on your computer are binaries.
They're ones and zeros.
That's the stuff computers can read.
While humans, when they write software, they write computer code, and the two aren't the same thing.
So when you're running closed software, you're just running the binaries and you are not exactly sure what your computer's actually doing.
So what your computer could be doing, for example, is spy on you.
If the developer puts a malware into the closed software, then your computer could spy on you, or I don't know, could do all sorts of stuff that you don't actually want the software to do.
So you have to trust the developer in that sense.
You have to trust the developer that he didn't include malware into your binaries, into your software.
So Richard Stallman, he didn't like this idea.
That wasn't his vision for the future, so he started the free software movement where the source code had to be available so people could actually check what they were running on their computer.
So in that sense, there wasn't a power relationship anymore.
They didn't need to trust their developer.
So, free in that context means freedom.
It doesn't mean free as in free beer.

Sjors Provoost:

So in Dutch we have the word, vrijheid, which means freedom and gratis which means free beer.
So, we can intuitively understand this.

Aaron van Wirdum:

We actually have two different words for that.

Sjors Provoost:

And I'm sure German has 27 words for it.

Aaron van Wirdum:

Probably.
Where was I?
So, that was Stallman's vision.
Then I think in the early nineties, there was a difference.
I can't remember the guy who wrote it, but there was this paper about the cathedral and the bazzar, the bazzar and the cathedral, something like that, It was like a Linux contributor.
And he explained the benefits of free software as it was just called until then from a different perspective where he explained how free software could actually provide high quality code.
Because there's a lot of people checking the code, enough eyeballs make all box shallow, that's the saying.
So he came up with a more sort of pragmatic reason why free software was a good idea.
This convinced the Netscape people to turn Netscape, the internal browser, into an open source project.
I'm calling it open source now, and that was Firefox.
And I'm calling it open source now because this group of people, they sort of rebranded free software to open source to more accentuate these different benefits.
So they weren't necessarily proposing, or they weren't in favor of open sourcing software for this philosophical freedom reasons that Stallman was advertising, that he was promoting, but more this pragmatic attitude.
So, that's where the difference between free software and open source stems from.

Sjors Provoost:

There's also a difference between freeware because, of course, that was a term that was going around too, but freeware could still be closed source.

Aaron van Wirdum:

I don't know.
I do know that basically every free software project is also an open software project.
There are very subtle differences for some of the licenses, but it's basically the same thing, just explained with different philosophies.

Sjors Provoost:

All right.
Well, in our case we're going to be quite pragmatic, so the terminology is less important.

Aaron van Wirdum:

You want to just go with open source?

Sjors Provoost:

Yes.

Aaron van Wirdum:

So we're just going to discuss open source.
Okay.
So Bitcoin is an open source project?

Sjors Provoost:

Yes.

## Why open source is important for Bitcoin

Aaron van Wirdum:

Why is that very important in the context of Bitcoin, Sjors?

Sjors Provoost:

Well, imagine you are trying to use Bitcoin and you install a computer program and it gives you an address, and then turns out there's some code in there that just steals your Bitcoin.
That would be bad.

Aaron van Wirdum:

That would be bad.

Sjors Provoost:

So at minimum you want to know what code you're actually about to send your pension to.

Aaron van Wirdum:

Yep.
Well, this is actually...
I just gave you the spying example of Stallman, but this would obviously be another great example where you don't want to trust the developers to not steal your coins.
You want-

Sjors Provoost:

It's a very extreme example.
It makes it very clear why you really need the maximum transparency of what the hell is running on your machine.

Aaron van Wirdum:

Exactly.

Sjors Provoost:

And we're going to go down that rabbit hole a little bit.

Aaron van Wirdum:

Yeah.
Because it's not that easy.

Sjors Provoost:

No, it's not.

Aaron van Wirdum:

It would be nice if it was that easy, but it's actually a lot harder than it sounds to make sure that the code on your computer is actually doing what you want it to do.

Sjors Provoost:

Yeah.
Because one thing is you want whatever Bitcoin code is running to be open source so you can see what it is.
But most computer programs, as we talked about in the first episode, use libraries or dependencies, use some other piece of software, that in turn uses some other piece of software, that in turn uses some other piece of software.

## The Importance of Open Source in Bitcoin

Aaron van Wirdum:

I want to take this one step at a time.
First step, so the code of Bitcoin, it's open source.
It's hosted on the GitHub repository?

Sjors Provoost:

Yeah, it's a GIT repository, which is also hosted on GitHub.

Aaron van Wirdum:

Right, okay.
Sorry.
Thanks for that correction.
So it's on GitHub, so anyone with the skills can look at this source code and check that it does what it's supposed to do.
So, Sjors-

Sjors Provoost:

In addition, everybody who has that skill can compile it themselves rather than downloading it.

Aaron van Wirdum:

Right.
First question, Sjors, because I actually cannot read this at all, how many people do you think can actually read this?

Sjors Provoost:

Well, that depends on what you mean by actually read.
How many people are computer literate in general?
Probably many, many tens of millions in the world.
How many can roughly read what a C program is doing?
I guess, again, several million, tens of millions probably.
But the number of people who can actually understand what the Bitcoin software is doing is probably a lot smaller.
And the number of people who actually do in addition to being able to, is in the dozens.
And then even then it's hyper-specialized.
So somebody might know everything about pier-to-pier networking code and have never looked at some other part of the code.

Aaron van Wirdum:

So, this sounds like a small number.
Why is it so small?
And can it be bigger?
How could we make this bigger in the future?

Sjors Provoost:

Well, one thing is you can make the source code more clean, more readable.
So then there are just more people who can read it, because it's just better.

Aaron van Wirdum:

So why isn't that the case right now, for example?

Sjors Provoost:

Well, it's better than it was, but when Satoshi wrote it, everything was one file with God knows how many lines of code in it.
And that's very, very, very hard to reason about.

Aaron van Wirdum:

For the non-programmers, reason about means-

Sjors Provoost:

Just you're looking at the code and you see, okay, there's a function called make a private key.
Okay.
What does that function do?
Oh, call in this other function.
Where's that other function?
Oh, it's 20,000 lines up in the same file.
Let me scroll 20,000 lines up, have a look at that code, and it's calling something else.

Aaron van Wirdum:

Reason-

Sjors Provoost:

Oh, but it's not calling something.
It's referring to a variable.
Oh, but this variable can be accessed in 15 different places at the same time somewhere in this file.

Aaron van Wirdum:

Reason about means understand what the hell is going on.

Sjors Provoost:

Yes.

Aaron van Wirdum:

Right.
Okay.
So there's not that many, but hopefully, it's improving or it's getting easier, but that's the work in progress and it's still pretty hard.

Sjors Provoost:

Getting a little bit of help from all these altcoins, which are cloning the Bitcoin code.
Not all altcoins are, but many are.
And they're cloning it and they're working on it, and they might occasionally find bucks, too.
Or at least they're looking at it.

Aaron van Wirdum:

Right.
Okay.
So let's say I trust that this process where a bunch of people can look at it, and I trust that they're not all cheating and this process is working.
At that point, I can download the binaries from Bitcoincore.org and I should be totally fine.
Right?

Sjors Provoost:

No.

Aaron van Wirdum:

Oh, what's the next problem?

## Deterministic Builds

Sjors Provoost:

Well, there's a lot of problems.
First of all, who says Bitcoincore.org is run by the same people you just mentioned?
It might not be.
Well, okay, maybe you can still prove that.
But then maybe the site is hacked, or the site isn't hacked, but the DNS is hacked.
There's lots of reasons why the thing you download is not the thing you think you're downloading.
It's called malware.
So one thing that open source projects almost always do is publish a checksum, which is basically saying when you download this thing and you run this script on it, it should have the following checksum.
That's one thing you can do, but then can you trust the checksum that you downloaded?
I don't know, because whoever hacked the site might have also hacked the checksum.
So then what you do is you sign the checksum.
So, for example, a well-known person, in this case, Wladimir van der Laan, he signs the checksum with a signature, with a key, with a PGP key that's publicly known.
It's been the same for 10 years.
So then at least you have something to check.

Aaron van Wirdum:

Okay.
So how does Wladimir know that the binaries he got actually reflects the open source code from the GIT?

Sjors Provoost:

Well, he knows, because he did it.
So, he took the source code.
He ran a command and he got the binary.

Aaron van Wirdum:

And by he ran a command, you mean he put it through some other piece of software that produces binaries from the open source software?

Sjors Provoost:

Yeah.
A compiler and a bunch of other tools.
So, that's great.
But then the question is how do you know?

Aaron van Wirdum:

Right.

Sjors Provoost:

And here it gets a little bit more complicated.
Ideally, what you do is you run the same command and you also compile it, and then hopefully, you get the same result.
And sometimes that works with some project, but as a project got really complicated, it often doesn't work because it can depend on some very specific details on your computer system what the exact binary file is going to be.
So for example, the software uses libraries and those libraries are living on your system.
So we talked about that in one of the first episodes about libraries in general.
These libraries might live in your system and these libraries get updated all the time.
And maybe you updated two months ago and Wladimir is very accurate and he updated yesterday.
And so the final product contains a different version of a library.
And if you only change one letter in a computer program, then boom, your checksum doesn't work anymore.
So that's one of the things that can go wrong.

Aaron van Wirdum:

Hang on.
One step at a time.
Why do I even need to care that my checksum matches whatever Wladimir signed if I compiled it myself?

Sjors Provoost:

If all you want is to compile it yourself, you don't care.

Aaron van Wirdum:

Right.

Sjors Provoost:

But basically what this whole mechanism relies on is that some people check, and that if some people find a problem, they're going to sound the alarm bell.
And so your security model depends on hoping that somebody will do this checking for you because you didn't compile it yourself.

Aaron van Wirdum:

Right.
Everyone who compiles this software should compile into the same checksum because that's how we know everyone's running the same software and no one's being fed malicious software, for example.

Sjors Provoost:

Yeah.
So you, as somebody who wants to make sure that no shenanigan is going on, you go to Bitcoincore.org, you download the binary, you just put it in a nice place, and then you compile it yourself, and you say, "Hey, is this the same?" If not, you go on Twitter and on the news media and you say, "Hey, there's malware on this website."
However, that is not trivial because, for example, these libraries that might be slightly different.
So you get a different checksum, even though there are no shenanigans going on.
It's just your computer is different.

Aaron van Wirdum:

Right.
So if I compile the Bitcoin core software on my MacBook and you compile it on your MacBook, they could still compile into different binaries?

Sjors Provoost:

Yes, because there might be some subtle differences.
And it's not just libraries.
It can even be the time of your computer.
So, because as you-

Aaron van Wirdum:

The clock.

Sjors Provoost:

Find stuff, there's some random output that contains a timestamp, maybe a log.
And if the log is included in the final product, then there's a different timestamp in your version than in my version because we didn't compile it exactly at the same time.
And so, that's a problem.

Aaron van Wirdum:

Right.
So somehow we need to make sure that the same source code compiles into the exact same binaries.

Sjors Provoost:

Yeah, at least if your goal is to verify that nothing went wrong, right?
Because normally if you're just using it yourself, you don't care about that.
So this phenomena is called deterministic builds.
So deterministic really just implies given a source, you're going to get the same binary.
And if you change one letter in the source, you're going to get a different binary, but everybody will get the same, basically, if they make the same change.

Aaron van Wirdum:

So how's this done?

Sjors Provoost:

So, this is difficult.
And the current way that Bitcoin Core is doing this is called Gitean.
And just to sum that up, it's basically you take a Ubuntu machine, could be a virtual machine or could be a real machine.
And you just take a very specific Ubuntu version, I think, that you download.
And many people in the world have seen that version, so you trust it.
And then inside that machine, you build another virtual machine.
And inside that virtual machine, there are all sorts of little changes made to make sure that that machine is identical for everyone who builds this thing.
So I think it uses a fake time and all the files are in the same place and all the libraries are the exact same versions, et cetera.
And then you build Bitcoin Core, and then you look at the checksums inside that virtual machine.

Aaron van Wirdum:

Right.
So it's kind of like running a computer within your actual computer-

Sjors Provoost:

Within a computer.

Aaron van Wirdum:

And everyone's sort of running the same computer within the computer, in their actual computer.
And therefore, the software they're compiling into binaries in the computer in the computer is resulting in the exact same binaries.

Sjors Provoost:

That's right.

Aaron van Wirdum:

This is turned into a checksum.
And if the checksums match, then the developers sign because they can all verify that, yep, it all worked out and this is the correct checksum.
And you can trust this because we're not all going to cheat on you.
Unless they are, but at least-

Sjors Provoost:

But we can catch them.

Aaron van Wirdum:

Yeah.

Sjors Provoost:

Anybody has the opportunity to see that there's a shenanigan going on.

Aaron van Wirdum:

Anyone can follow this process and catch that something.

Sjors Provoost:

Yeah, in theory.
In practice, it's a pain.
It's a huge pain to get the system working.
There's not many open source projects that use this.
As far as I know Bitcoin Core and Tor do, maybe a few others, but not a lot.

Aaron van Wirdum:

Maybe some other cryptocurrencies.

Sjors Provoost:

Some, but a lot of them, even if they've cloned Bitcoin Core, they've stopped doing this process because it's too much work.

Aaron van Wirdum:

Right.
So far so good.

## The Problem with Dependencies

Sjors Provoost:

So, it's great, but there is another problem because the rabbit hole is deeper.
And there's actually two different problems, but they're kind of the same.
So, let's start with the first thing.
Let's say you have read every single line of code in Bitcoin Core and you can say, okay, I've read every single line in there.
I understand every single line of it.
It's just like when you read the Facebook terms and conditions, but then it turns out the Facebook terms and conditions point to some other document.
Like, for example, I don't know, the United States law, all of it.
So, with phrases like as defined in law.
Now you have a problem, because Bitcoin Core uses all sorts of other things.
And so you have to inspect those things, too.

Aaron van Wirdum:

Dependencies, these are called.

Sjors Provoost:

Because the dependencies could also be stealing your coins, so they should be open source, too.
And-

Aaron van Wirdum:

Bitcoin Core doesn't use that many dependencies anymore, right?

Sjors Provoost:

Exactly.
So one of the constraints when working on Bitcoin Core is to try and keep the number of dependencies as small as possible, and also not update them all the time.
Because, of course, the people who maintain those dependencies know that Bitcoin Core is using it.
Right?
So you need to be somewhat on your toes to make sure that those projects are being scrutinized, too.

Aaron van Wirdum:

So let's say some dependency is corrupted.
What could that mean for Bitcoin?
Could they-

Sjors Provoost:

Oh-

Aaron van Wirdum:

Go on.

Sjors Provoost:

Yeah, if some dependency is corrupted, it could steal your coins, basically.

Aaron van Wirdum:

Right, that bad.

Sjors Provoost:

Yeah, that's your worst case.

Aaron van Wirdum:

Okay.

Sjors Provoost:

And this actually it happened at least in another project called Copay, which is, I think it's a library for wallets in general used by BitPay, but by other companies, too.
And it's written in a different programming language, but the general idea is the same.
They have a piece of software that's open source.
Everybody can review it.
But it uses dependencies, and those dependencies use dependencies, and those and those and those and those.
And in this case, they were using NPM, the Node Package Manager and Node.js, and that package manager is basically a very large open source community.
And they've very much focused on making very modular packages.
So I think there's an individual package for addition or multiplication or fairly trivial packages.
And every single package links to a place on GitHub, so it's all open source.
And every package could have its own maintainer who can release updates whenever they want.
And so now you have a problem, because you might be pulling in 10,000 dependencies without even realizing it.
Because you only pull in maybe five dependencies, but those each pull in 50 dependencies, and those each pull in another 50 dependencies.

Aaron van Wirdum:

And if any of these is corrupted, it could, at least theoretically, include coin stealing malware.

Sjors Provoost:

Yeah.
And so, it depends.
There are some ways in theory that you can try to avoid that by encapsulating by saying, okay, this piece of code, I'm going to run that code.
I don't trust it, but I'm going to put it in some place where it cannot do anything other than that I want it to do.
But with JavaScript, which is what they're using, at least at the time, this is two years ago, that was very difficult to do.
So any JavaScript that is run can do anything in the entire browser.
So in this case with the Copay wallet, there would be private keys somewhere inside the browser.
And a piece of malware could just say window dot, blah, blah, blah, blah, blah dot steal coins, basically.

Aaron van Wirdum:

And this actually happened or-

Sjors Provoost:

Well, somebody wrote that malware.
I don't think it was exploited in the wild.
I think it was detected.

Aaron van Wirdum:

Someone, because I vaguely remember this, but someone actually got this kind of malware into the Copay wallets basically, into the Copay library.
This was actually done.

Sjors Provoost:

In a dependency of a dependency of a dependency.
So what they did is they found some random, far away dependency deep down in the tree that's actually used by millions of projects, and that dependency was no longer maintained.
So somebody wrote it, everybody uses it, and then the guy or girl no longer maintained it.
And so the attackers sent an email to that previous maintainer saying, "Hey, I really love your project.
I care about this.
Maybe I can take over from you." And so he got the keys to the kingdom and he was able to publish updates.
And so then he published an update that contained some malware, some coin-stealing code, that was specifically designed to attack Copay wallets or that general library.
And what it did was, well, first of all, he hid it.
So, it's open source, but if you release an update, you can do different versions.
So you can do a minor update saying, "Oh, this is just a small change," and you can do major updates.
And most software will constrain these updates.
So it'll automatically update for you, but only for minor updates.
It won't automatically upgrade a major upgrade.
So what the attacker did is he made a minor update, and then immediately afterwards made a major update, which undid the attack.
So if you looked at the most recent version of the code, there would not be any attack code in there.
So anybody inspecting the open source would say, okay, this is fine.
But if you looked at the specific minor version that was being used, then it was there.
So, you don't only have to review the most recent source code, you have to review the source code specific version that you're using for all of your dependencies.
It's completely impossible.

Aaron van Wirdum:

Right.
So Copay was open source, but because of these dependencies and the dependencies on those dependencies, it's still not going to solve your problems.

Sjors Provoost:

No, and it was very, very subtle, right?

Aaron van Wirdum:

Right.

Sjors Provoost:

Because I guess it was found by somebody very, very carefully looking for this sort of stuff, because it's very hard to stumble into it.
And it was even made that it wouldn't reveal itself early.
Because what you want to do as an attacker is you want to look for a very big bounty and then take that.
Because as soon as you start stealing coins, if you only steal one satoshi and the person losing that one satoshi notices it, they're going to sound the alarm bell and then people are going to start looking where the malware is, knowing that it exists, and they're going to find it.
So basically, it had a condition in there that says there has to be at least a couple of Bitcoin in there and only then am I going to attack.
And I guess that never happened, fortunately, because they caught it on time.
But this is the risk.

Aaron van Wirdum:

So what's the solution?
Just not depend on dependencies?

Sjors Provoost:

Pretty much.
I think there are now, over the last couple of years, there's some companies that will screen as a service that might actually go through all these dependencies.
But what you really want to do is you want to have very few dependencies, and especially you want to stay away from things that have nested dependencies.
So in the case of Bitcoin Core, it's not too bad.
It has, I think, about 10 dependencies that do not have a bunch of nested dependencies.
So, it's not a big tree.
It's relatively shallow.
So you'd have to go after those dependencies directly to attack.
So, that's good news.

## Gitean 

Aaron van Wirdum:

Okay, Sjors.
I think that part is clear.
Now I have another question for you.
I think you have a vague idea where I'm going, because we already discussed exactly where we're going.
We just discussed how you have deterministic builds and how different developers are all using this Gitean building thing to get the exact same binaries and sign all of that.
Now, here's my next question.
What if the Gitean building process itself is corrupted somehow?
Is that possible?

Sjors Provoost:

Yeah.
Or specifically, Gitean uses Ubuntu, and what if somebody says, "Hey, this Bitcoin project's pretty cool.
This Ubuntu project's pretty cool.
Let me contribute some source to Ubuntu." And now when everybody runs their Gitean builder which includes Ubuntu, there is a compiler on Ubuntu and maybe that compiler is modified to, if it compiles Bitcoin Core, it actually adds some code to steal coins.
It would be very, very scary.
So it still have deterministic builds because everybody would be using the same malware to build it.

Aaron van Wirdum:

I guess that's a dependency in itself then, right?
That's like a dependency for Ubuntu, or am I saying that right?

Sjors Provoost:

Yeah, I guess there's two kinds of dependencies.
One is the dependency you are actively running that's inside the binary that you're shipping to your customers.
But the other dependency, and that's a real can of worms, are all the tools that you're using to produce the binary and even to download the binary, but yeah.

Aaron van Wirdum:

So if the tools you use to build Bitcoin Core is corrupt, then you still have a problem because all of the developers are getting to solve the same binaries from their Gitean process, but if that's corrupted...
Anyways, I think our listeners get it.
So what's the-

Sjors Provoost:

Right.
So what you're hoping is that the people who are maintaining all these compilers and all the other things know what they're doing and would never let any such back door through.
But that would be boring, so how do we get more paranoid?

Aaron van Wirdum:

How do we get more paranoid?
How do we solve this problem?

## GUIX 

Sjors Provoost:

Well, the key there is to make everything open source and everything a deterministic build.
So not just Bitcoin is an deterministic build, but every dependency of Bitcoin is a deterministic build, and every tool that is used to build Bitcoin is a deterministic build, including the compiler.
And this is where we introduce GUIX.
This is a project Carl Dong has been working on and has given several talks on that.
We'll probably link to in the show notes.

Aaron van Wirdum:

Yeah, Carl Dong, he's with Chaincode Labs, right?

Sjors Provoost:

Yeah.

Aaron van Wirdum:

Yeah.
So the trick then, it's a difficult trick.
Well, it sounds very difficult to me because you need a compiler that itself needs to be compiled as well, because the compiler is also software.
So if you want to-

Sjors Provoost:

Yeah, so this is turtles all the way down.

Aaron van Wirdum:

Exactly.

Sjors Provoost:

So the ambition of GUIX is roughly as follows.
You start with about, I think it's 150 bytes, of actual machine code.
So that is binary code that you must trust, but it's only 150 bytes, and the whole world can study it and put it on a temple wall or something like that.
But from that 150 bytes, all you need to do now is read source and compile source.
So how do you do that because there's no compiler yet, right?
So this 150 bytes is able to bootstrap.
It is able to read something.
That's all it can do, basically, and produce a little bit more code.
So it reads some something and then it builds up a very simple compiler.
And once it has the very simple compiler, that very simple compiler reads another piece of source, which then builds a slightly more complicated compiler.
And then that slightly more complicated compiler builds another compiler.
And this goes on for quite a while, I think, until eventually, you have the modern C compiler that we all know and love, which is itself, of course, open source, right?
All compilers have this fundamental problem that who compiles the compiler?

Aaron van Wirdum:

It sounds pretty fascinating.
So it's like a-

Sjors Provoost:

It is turtles all the way down, but there's actually a bottom.

Aaron van Wirdum:

Yeah.
It's a-

Sjors Provoost:

It's not turtles all the way down.

Aaron van Wirdum:

It's a C that builds a compiler that builds compilers.

Sjors Provoost:

Yeah.
So all the compilers and sub-compilers are all open source.
It's just that C that is not sourced, that has to be a binary.
Because you have to start with the binary somewhere.
But you can literally just type it.

Aaron van Wirdum:

And this is a work in progress.
This isn't used or finished yet, right?

Sjors Provoost:

I think it's a work in progress, but it is also working.
I believe we can now use this for Bitcoin Core, because I recently did it as well.
Tried to just hit the commands blindly, and it was producing actual Bitcoin Core binaries that could be run and that are not turtles all the way down.
I think it doesn't start at the very bottom.
So I still had problems going from the bootstrap, but that's where it's going.

Aaron van Wirdum:

So do one of these compilers build like the Gitean thing?
Is it the same thing or is it-

Sjors Provoost:

It's not building Gitean itself, but it's a similar principle.
So the idea is it can build, I think the idea eventually, is that it can build a whole operating system.
So then your virtual machine or your physical machine would be running a operating system that you've built from scratch.
But in this case, I think it just builds the compiler tools.
And once those compiled tools are there, it can just start building Bitcoin Core as it would otherwise do.
Similar to Gitean as in it has to make sure that there are no timestamps in there and it doesn't use anything else from your computer.
So it solves two things, right?
It has no untrusted dependencies.
It's not using random libraries.
It's always using the same versions of libraries, which means that everybody can produce the same result.

Aaron van Wirdum:

Interesting.
Okay.
So these 115 bites, were they 115?

Sjors Provoost:

I don't know.
I think it was a 150.

Aaron van Wirdum:

Just a small-

Sjors Provoost:

But they're pretty small.

Aaron van Wirdum:

So do we still need to trust these?
Or, I don't know how big the leap of trust is there.

Sjors Provoost:

Well, you can read them.
There's machine code.
As far as I know, it's machine code that can parse a hexadecimal piece of text.
And then I guess it parses the hexadecimal piece of text and that piece of text is another piece of machine code, I guess, which is then run.
So it's still open source in the sense that the binary is the source.
But machine code can be read, right?
It's very, very tedious to read it.

Aaron van Wirdum:

Wait, these 115 bytes, they're source code or they're binaries?

Sjors Provoost:

No, they're binaries, but you can read a binary.
It's not fundamentally impossible to read a binary.
It's just very difficult to read a binary if it's big.

Aaron van Wirdum:

I see.

Sjors Provoost:

But if the binary is tiny, then it's just a set of machine instructions.
Because what happens when you run a program is the CPU just looks at the first two bytes or whatever, and it says what's the instruction?
And then the instruction says, okay, create a variable.
And the next instruction says set this variable to two.
And then the next instruction says add five to the variable.
And the fourth instruction says restart the computer or something like that.
So if it's just 150 bytes, you can look at every single byte and see what the computer instruction is in there, and you can still reason about it.

Aaron van Wirdum:

I see.

Sjors Provoost:

And I believe the only thing it does is it just has a small program that's able to open a file and read that file and then execute that file.

Aaron van Wirdum:

Interesting.

Sjors Provoost:

And then slowly you try to get to a point where it's human readable.
So the very low level compilers, the very simple compilers, might have code that's not very easy to read, but still very short.
And then very quickly you get very nice, elegant programming languages that you can read.
But something like Rust, in order to build Rust, you need to build compilers that can compile Rust.
In order to make it build a Rust compiler, you probably need a C compiler.
So, yeah.

Aaron van Wirdum:

Yeah, this sounds super fascinating to me, the fact that this is possible.

Sjors Provoost:

And then at least you have this ginormous spider web of code.
All of it is code and you know that it produces a binary, and then you just need lots and lots of people to review every single piece of code in there and be very conservative about updating any of it.
Because if you update any of it, well, it could be malware again.

Aaron van Wirdum:

Right.

Sjors Provoost:

And most people are used to automatically updating the computer.

Aaron van Wirdum:

Well, so this is how we're going to make Bitcoin truly trustless, essentially?

Sjors Provoost:

Well, turtles really all the way down because you're still running it on a piece of hardware.

Aaron van Wirdum:

Ah, true, yeah, of course.
That's a whole other-

Sjors Provoost:

So trusted hardware-

Aaron van Wirdum:

Nightmare.

## Open source hardware

Sjors Provoost:

Open source hardware is another movement that are trying to get rid of all these weird chips on your computer that are doing arbitrary things.
You have no idea what it is doing.

Aaron van Wirdum:

Do we want to give a shout out to walletscrutiny.com?

Sjors Provoost:

Yeah.
So walletscrutiny.com is a website that looks at various wallets, whether they are open source at all-

Aaron van Wirdum:

And a lot of them aren't.
That's pretty scary.
There's dozens of wallets that aren't even open source.

Sjors Provoost:

Yeah.
So the only way to verify those wallets would be to inspect the binaries, which there are tools to make that also slightly less painful than it sounds.
So if there's some very obvious code in those wallets that says steal coins, somebody will probably still find it.
But it's not good.
And then you have wallets that have source published, but if you have that source and you want to make sure that the binary they give you in the play store is the same, it's not that easy.
Sometimes they don't offer any feature functionalities for it.
Sometimes they do, but it doesn't work because it hasn't been maintained, because not a lot of-

Aaron van Wirdum:

How would you make that?
How would you check that?
What's the process there?
How do you make sure that-

Sjors Provoost:

So Wallet Scrutiny actually, for some wallets, for example, ABCore, which is a full note on Android, it's a bit of a toy project, but it's very cool, on the site they just have 20 lines of code that you run in a terminal.
Get this thing from GitHub, get these Android libraries, build this project, and then compare the checksums.
And they show, if you execute these commands, you get the exact result.

Aaron van Wirdum:

So the app you're downloading on your Android phone, you can check the checksum for it?

Sjors Provoost:

Yeah.
I think so, but I don't think they've done it for iOS yet.
And I don't even know if you can do it with iOS.

Aaron van Wirdum:

Right.

Sjors Provoost:

So for computers, for normal computer programs, you might need something like Gitean, which is very tedious and I don't think a lot of people are going to do it.

Aaron van Wirdum:

Yeah, so Wallet Scrutiny-

Sjors Provoost:

Web applications are, again, a different possibility.
I once worked on that, and I think I once got a web application to be a deterministic build and you could actually run a command and it would do it.
But if you don't maintain that, it's going to break.
Because all the Node.js tooling and all that stuff is not designed to make reproducible builds too easy.

Aaron van Wirdum:

So, okay.
So walletscrutiny.com, it's a project by [Leo Van der Schlepp 00:33:36] and it categorizes wallets into custodial, not even open source, so not custodial, but also not open source, which is probably even worse than custodial.
I don't know what you think.

Sjors Provoost:

Depends if you know who it is.

Aaron van Wirdum:

Yeah, I guess.

Sjors Provoost:

If some random person, the only way you can find out who they are is to ask Apple, and then Apple says, "Oh, sorry.
That was some random BVI thing.
We have no idea."

Aaron van Wirdum:

Yeah, anyway, so custodial, non-custodial and also not open source, and then there's non-custodial but at least open source.
And then there's the category non-custodial, open source, and deterministically buildable, which are only a few wallets.
That's sort of the category you want to be in, but that's only a handful.

Sjors Provoost:

And I think the site only covers Android wallets.

Aaron van Wirdum:

Right.
Okay.
Sjors, does that cover our episode?
Is that it?

Sjors Provoost:

I think so.
I think we've opened quite a few cans of worms, and you folks can think about that during the Christmas holidays.

Aaron van Wirdum:

Yeah.
We're taking a break.
There will not be any episode over, well, until the new year.

Sjors Provoost:

Yeah, probably.

Aaron van Wirdum:

Sjors, see you in the new year.

Sjors Provoost:

Yes.

Aaron van Wirdum:

Have have a good Christmas.

Sjors Provoost:

Thank you.
Thank you for listening to the Van Wirdum Sjorsnado.

Aaron van Wirdum:

There you go.

