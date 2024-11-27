---
title: "Bitcoin Core 27.0"
transcript_by: kouloumos via tstbtc v1.0.0 --needs-review
media: https://bitcoinexplainedpodcast.com/@nado/episodes/episode-92-bitcoin-core-27-0-c4wla
tags: ['bitcoin-core']
speakers: []
summary: "In this episode of Bitcoin, Explained, Aaron and Sjors explain what new features are included in the upcoming Bitcoin Core 27.0 release."
episode: 92
date: 2024-04-10
additional_resources:
  - title: https://github.com/bitcoin-core/bitcoin-devwiki/wiki/27.0-Release-Candidate-Testing-Guide
    url: https://github.com/bitcoin-core/bitcoin-devwiki/wiki/27.0-Release-Candidate-Testing-Guide
  - title: CoinKite
    url: https://store.coinkite.com/promo/BITCOINEXPLAINED
  - title: https://bitcoinexplainedpodcast.com/
    url: https://bitcoinexplainedpodcast.com/
---
Speaker 0: 00:00:16

Live from Utrecht, this is Bitcoin Explained.
Hey Sjoerd.

Speaker 1: 00:00:20

Hello.

Speaker 0: 00:00:21

First of all, I'd like to thank our sponsor CoinKite, the creator of the OpenDime as well.
That's right.
Are we going to get sued if we only mention the Opendime, Sjoerds?
No. Are we contractually obligated to mention the Gold Card or can we just riff off the Opendime this episode?

Speaker 1: 00:00:41

If you want to riff on the Opendime for the great memories it brought us.

Speaker 0: 00:00:46

The Opendime is pretty cool.
I still have a few.

Speaker 1: 00:00:49

What is an open time?

Speaker 0: 00:00:50

It's like a USB stick, kind of small stick.
You put it, you stick it on your computer, you put some Bitcoin on it, you hand it to someone, very cypherpunk technology, off-chain, no one needs to know anything.
And then that person can check that the Bitcoin are really on there and they can take the Bitcoin off only once.
You have to sort of destroy the thing to get the coin off.

Speaker 1: 00:01:12

Yeah, so you can see whether it was spent or not.
You actually have to break it.
Right.

Speaker 0: 00:01:16

Very cool.
So we're making another episode about another Bitcoin Core release.
I feel like one every four episodes we make now is about a Bitcoin Core release.

Speaker 1: 00:01:28

Yeah, those are a bit of our lazy episodes.

Speaker 0: 00:01:32

Well, also we don't make as much episodes.
Or is Bitcoin Core making more Bitcoin Core releases?

Speaker 1: 00:01:37

No, I can, however, tell you that Bitcoin Core version 27.0 will be the best Bitcoin node ever.

Speaker 0: 00:01:45

Nice.
So, Bitcoin Core 27.
As we're recording this, it's in release phase, what is it, release candidate one?

Speaker 1: 00:01:55

Yes, exactly.
So people who would like to test it, they can.

Speaker 0: 00:01:59

For any new listeners, Sjoerd, what does it mean that there's a new BitConcord release?

Speaker 1: 00:02:04

It kind of means nothing, because in BitConcord there is a new release roughly every six months, regardless of what is finished.
So whatever is finished goes into the release, what is not finished does not go into the release.
It is not, yeah, that special, I guess.

Speaker 0: 00:02:20

We should next time just ask Stijn, our editor, to just cut this from the previous episode so you don't have to repeat.

Speaker 1: 00:02:27

To see that I'm answering the question inconsistently.

Speaker 0: 00:02:30

So yeah, every half year there's a bit of a core release, whatever is ready by then goes into the release, whatever is not, is not.

Speaker 1: 00:02:37

Yeah, though one thing that I believe was observed is that the release started drifting a bit.
So, you know, maybe it was in January on one year, and then the next year it was in February, and the next year was in March, and the next year...
So this release is a relatively short one to try and reset the schedule a bit.

Speaker 0: 00:02:53

I see.
Okay, so when was the previous one?
Do you know this?

Speaker 1: 00:02:57

I think it was in November, maybe?
It should be every six months.

Speaker 0: 00:03:01

That's six months ago.
Okay, so release candidate one, what does that mean?
Also for new listeners?

Speaker 1: 00:03:08

Yeah, so what happens is there's a couple of phases to the release.
The first phase is the so-called bug fix time.
So there's a master branch where all the changes go that Bitcoin Core makes and everything in the master branch should be bug free, but sometimes it's not.
And the idea is that a few weeks before the branch off point, which I'll explain in a bit.
People stop merging, or maintainers stop merging things, their features and try to merge only somewhat more conservative bug fixes, typo changes, that sort of stuff, to make sure that there are, you know, to reduce the chance of having any bugs on that master branch in the first place.
And then what happens is this branch off, which is where a separate Git branch is created, where all the changes, which only has bug fixes.
So to understand what that means is there is still the master branch and people are still developing on that, but anything that goes onto the master branch will not go into the release.

Speaker 0: 00:04:10

Wait, but I was asking about the release process, basically.
We're in release candidate one?
We'll get there.
Oh, okay.

Speaker 1: 00:04:18

I was going a little bit back there.

Speaker 0: 00:04:19

Okay, go.

Speaker 1: 00:04:20

So, yeah, so the master branch people can continue to have fun there, that's going to be for the next release.
Meanwhile, there is this separate branch for the release, which has only maybe very minor bug fixes.
And then once, and then to that branch are added a few things to change the version number and then that is turned into a release candidate and that release candidate is first let's say people tested a little bit who are developers and then once that's done, there's a binary release that people can download and test that.

Speaker 0: 00:04:57

So what do we have now?
Where are we?
Do we have a binary release?

Speaker 1: 00:05:02

Yes, there's a binary release for release candidate one.

Speaker 0: 00:05:04

Okay, so how many release candidates are there going to be?

Speaker 1: 00:05:07

Well, so what happens then is for about two weeks people can test it, and then if they don't find any bugs, then we essentially make the same binary and call it the final version.
It's not technically the same binary, we talked about hashes before, the version number is in the binary, so different version number means a different hash, but other than the version number it should be identical.

Speaker 0: 00:05:28

Okay, so the current release candidate could potentially be the next Bitcoin Core 27, but maybe bugs are found, then the bugs are fixed, and then there will be another release candidate, and then that could be the next Bitcoin Core 27.

Speaker 1: 00:05:38

So whenever a bug is fixed, it is first fixed on the master branch, so it also applies to future releases, and then it's backported, as it's called, to the release branch.
And that means that the same fix that was applied to the master branch, then also applied to the release branch, that's extra work.
So ideally, that should not happen too often.
Hence the need to not have bugs in the Massive Ranch.

Speaker 0: 00:06:03

Right.
Anyways, as soon as there's no bugs in the release candidate, we have a new Bitcoin Core release, which in this case will be Bitcoin Core 27.

Speaker 1: 00:06:10

Exactly.

Speaker 0: 00:06:11

And we are going to discuss some of the highlights of this new Bitcoin Core release.
Why should people download it?
Why should people care?
Why, dear listener, do you want to use Bitcoin Core 27?
Schors will explain it all today.

Speaker 1: 00:06:25

Exactly.
Well, first of all, there's something that's not in Bitcoin Core version 27.

Speaker 0: 00:06:31

Yeah, something was jacked out, Libitcoin consensus, which has nothing to do with Libitcoin.

Speaker 1: 00:06:38

Yeah although I think I should say it's not removed it's deprecated which means that this is your last warning it's going to go away 28.

Speaker 0: 00:06:48

Okay and I wait so it's still so that okay just explain what it is.

Speaker 1: 00:06:52

Yeah so deprecation is always a warning, like this thing is going to go away the next time.
So sometimes if you use a feature that's deprecated, it will tell you, hey, this feature is deprecated.
Sometimes you even have to actively set a configuration to use a deprecated feature.
So the first time you try to use it, it says no.
And then you make a change to the configuration, it says, okay, I'll do it, but it's gonna go away next time.
So, you know, be careful there.

Speaker 0: 00:07:18

You've been warned.

Speaker 1: 00:07:18

Yeah so this this thing goes away.

Speaker 0: 00:07:20

So what is this thing?
And why is it going away?

Speaker 1: 00:07:24

So in the early days there was a demand to have or a desire to have the core functionality of Bitcoin Core, so the part that checks the consensus rules, to somehow split that off from the rest so that other people can make their own node software or do other things and don't care about all the whistles and bells that are in Bitcoin Core.
So they don't want a GUI, they don't want...

Speaker 0: 00:07:49

So in other words, that would basically be the rules that define which blocks are valid, right?
That's really the core consensus rules?

Speaker 1: 00:07:57

Well, yeah, the question is, what is exactly the core consensus rules?
That's an open question still.
But at the time, this library, this libBitcoin consensus, was limited to, I believe, things that can check signatures.
It wasn't even fully checking a block, it could just verify individual transactions and signatures.
Okay.
So it was a very limited subset of what we consider the validity.

Speaker 0: 00:08:22

Okay, but that's because it wasn't finished yet?

Speaker 1: 00:08:26

Yeah, it was a work in progress.
It was the first attempt, but it wasn't finished and it's quite difficult to maintain.

Speaker 0: 00:08:33

So why it wasn't finished?
What's hard to maintain about it?

Speaker 1: 00:08:39

Not really.
It was just a pain in the ass.
And now we have the kernel project, which tries it again and uses a different approach.

Speaker 0: 00:08:47

Right.
I mean, from what I understand or what I remember, at least years ago when I heard about this, the bigger core, at least as it was then and probably still, or at least as Satoshi released, it was kind of spaghetti goat, spaghetti coat where everything sort of refers to everything else and some of it was consensus and some of it was not.
So it was very hard to sort of derive from that mess what actually was consensus.
And that sort of was the big challenge to getting this done.
So it sounds like this project was started, I think especially Jorge Timon was working on this.
And it sounds like he kind of went away and probably people sort of stopped caring about this project.
And now Bitcoin Core, DevSet, Let's just get rid of this thing.
Let's start over.
Let's start fresh.

Speaker 1: 00:09:34

Yeah, I think so.
And I think it was also getting in the way of some other refactoring cleanup projects.

Speaker 0: 00:09:38

Right.
And this Bitcoin kernel you just mentioned, have we talked about this on the podcast?

Speaker 1: 00:09:43

We've mentioned it a couple of times.
The TLDR is it's an attempt again to take the essence of Bitcoin Core and make it available for other software.
Now there's still an open question of what should and should not be part of the kernel.
For example, does the mempool belong to the kernel or just blocks?
And we've seen that even network rules impact consensus.
We've seen that very clearly with an episode we did about a BTCD bug, no lib.
Yeah, I think it was a BTCD bug, Yeah, for using with LND, where a block was sent and it was rejected, but it wasn't rejected based on the consensus rules, it was rejected based on a network rule saying that the block had too many, I don't know what it was.

Speaker 0: 00:10:27

Yeah.
We have an episode about it.
Okay.
Anyways, Libitcoin consensus is deprecated.
Yes.

Speaker 1: 00:10:35

So, as a user, you will not notice this at all.
Right.

Speaker 0: 00:10:40

Okay, let's move to something that you might use as a user, might notice as a user.
Actually, I don't think the next one is going to be noticeable by a user either.

Speaker 1: 00:10:50

No, it might be.
It might be.

Speaker 0: 00:10:52

Okay.
This is about the mempool.

Speaker 1: 00:10:56

Yeah, to be precise, it's about saving the mempool.

Speaker 0: 00:10:59

About saving the mempools.
Well, your mempool.
Yeah.
Saving the mempool.
Saving my mempool.
How are we going to save my mempool?

Speaker 1: 00:11:08

Yeah, so Bitcoin Core, when it's running, it receives new transactions.
It holds onto those, usually in memory.
And then at some point you shut Bitcoin Core down.

Speaker 0: 00:11:18

This is before they're included in a block.

Speaker 1: 00:11:20

Yes, exactly.
And then either if a block arrives, they go out of the mempool because now they're in a block, or if you shut down Bitcoin Core but the transaction is still not in a block, it's going to remember it by saving it to disk.
And then next time you start Bitcoin Core, it loads it from disk.
Otherwise you'd have to wait for somebody else to announce it again to you, which is not ideal.

Speaker 0: 00:11:39

Well, or it's in a block, right, by then?
Yeah.
I mean, there's no real, what's actually the point now that I ask this question?
Like, why should I care as a regular user that my mempool is cleared?

Speaker 1: 00:11:51

Well, we did an episode about why the mempool is useful in general.
You know, it helps with things like block relay.
It makes it quicker for you to verify a new block because you already verified those transactions before.
So then when you restart BitConcord it helps you to verify all those new blocks that you're going to catch up with with that mempool that you still had.

Speaker 0: 00:12:12

Right okay so yeah I have a BitConcord node and the mempool if when I shut down my computer, my entire mempool is just saved on disk and then I start the computer again and Bitcoin Core starts up and it remembers what was in the mempool.
Exactly.
Okay, so what's the problem?

Speaker 1: 00:12:30

The problem is that there, you might have a virus scanner and that virus scanner is looking for suspicious files.
And if some joker puts a transaction, creates a transaction and then puts one of this operator and spam, you know, inscriptions, whatever it is in there, they could put something in that looks like a virus.

Speaker 0: 00:12:51

And-
What is a virus or not?

Speaker 1: 00:12:53

Well, that's a philosophical question.
Is a photo of a virus a virus?
I don't think so, because it's not gonna replicate or do any harm.

Speaker 0: 00:13:00

Okay.

Speaker 1: 00:13:00

Right?
So it's more like a picture of a virus, I guess.

Speaker 0: 00:13:03

Okay.

Speaker 1: 00:13:03

It might be the exact same code.
It's just, it's not that your node is suddenly going to run the virus and destroy itself, but the virus scanner doesn't understand that.
So it sees something that looks like a virus and says, I'm going to put this in quarantine now.
And then puts your whole mempool in quarantine and now when you start to node again, it's not going to break, it's just going to say, oh, I guess you don't have a mempool yet, let me make a new one.
Uh-huh.
That's not ideal because we just explained why we saved this thing in the first place.

Speaker 0: 00:13:34

Can't say I feel very stressed about this problem, but sure, go on.

Speaker 1: 00:13:38

No, this is why this problem has not been fixed for the past 10 years.
We do the same thing for blocks that are stored on disk.
Well, what we'll do, we'll explain in a bit, but we have the same problem for blocks, I think that actually did happen in like 10 years ago, some joker put something in a block that looked like a virus.

Speaker 0: 00:13:56

It's better to solve the problem.

Speaker 1: 00:13:58

Yeah, because if your node, if your blocks are thrown into the, you know, are killed by the virus scanner, then your node doesn't work anymore.
Right.
So that's more important.

Speaker 0: 00:14:06

Yes.
And so transactions, yeah, okay, so what's the solution here?
What are we trying to do?

Speaker 1: 00:14:14

The solution here is to basically fool the virus scanner by encrypting the file.
Now encrypting sounds very fancy, it's not the strongest encryption ever, but it is using XOR basically.

Speaker 0: 00:14:31

What's XOR?

Speaker 1: 00:14:33

XOR, well I guess the easiest way to explain it is like a one-time pad.
So, and this is one of the oldest forms of encryption that exists.
You take a text that you want to encrypt, like the word hello, and then you add to it a set of random letters, that's the easiest way to see it, that you've agreed to before.
So you and I wanna communicate, we exchange a long piece of paper with lots of letters on it, and then we say whenever we write a letter to each other, we both start with that piece of paper and we add the letter on that piece of paper to every letter that we write.
Or I add the letter and you subtract it.
And that way...

Speaker 0: 00:15:15

Wait, So this sounds like the Caesar cipher.
Do you know what this is?

Speaker 1: 00:15:19

No, it's much, much more secure.

Speaker 0: 00:15:21

Oh, it is more secure than that?

Speaker 1: 00:15:23

Yeah, I think the Caesar cipher was, well, it was this, I don't, actually, I don't know, it might be similar.

Speaker 0: 00:15:28

The Caesar cipher, which I describe in the Genesis book.

Speaker 1: 00:15:33

Oh, yes, you wrote a book.

Speaker 0: 00:15:35

It's basically, you take the word hello and then you do like plus five and then for each letter, you replace the letter in hello for like the fifth next letter in the alphabet.

Speaker 1: 00:15:48

Yeah, but if you do it just plus five for every letter, that's a bit easy to crack.

Speaker 0: 00:15:52

I mean, it is, but that's the Caesar Cipher.

Speaker 1: 00:15:54

So this cipher means every character gets, you add a different letter or a different number to every character.
And that number is random every time.
So you have a page with completely random numbers that you created with dice throwing, whatever it is.
Number is zero to 26, right?
Or zero to 25.
And when I'm writing the letter, I'm writing you the message, I'm adding a different number to every letter of my message and you have to keep track of where I am and then you can subtract the same number.
And then you burn the piece of paper that we used as a cipher.
So that means Anybody who intercepts the communication midway can no longer decipher it.

Speaker 0: 00:16:35

Anyway, so the mempool is encrypted.

Speaker 1: 00:16:38

Using roughly that technique, except a very insecure version of it, because the entire thing is only like eight characters long, and it just repeats the same eight characters, which is insecure.
And also at the start of the file, the cipher is actually revealed.
So it is totally insecure, because it's not the goal to be secure, it's the goal to fool the virus scanner.

Speaker 0: 00:16:57

Yep.
Okay, that's it?
Mempool upgrade?

Speaker 1: 00:17:01

Yeah, and so the little thing there is that means you can't downgrade, because older versions of the node, if you wanted to go back to an old version, won't understand the mempool file.
But they'll just start a new one, so it's not a big deal.

Speaker 0: 00:17:15

Okay, next one.
BIP324, we made an episode on that.
That's network encryption.
And that's now on by default.
So it was already an option in the previous Bitcoin Core release?
Yep.
Maybe even the one before that?
No, probably the previous one, I think.

Speaker 1: 00:17:37

I think the previous one or the one before it, it was made default.
No, it was...
It was available, you could turn it on.
Yeah.
And now it's on by default.

Speaker 0: 00:17:45

Right, okay.
Quick reminder of what it was again?
Episode 77.
No, sure.
What is it?

Speaker 1: 00:17:53

Sten can just paste it.
No, that's fine.
The idea is that you and I have a connection and instead of sending everything in plain text, we encrypt everything.

Speaker 0: 00:18:06

Yep.
Okay, I mean, I guess actually, yeah, that's good enough.
If you do want to know more, we may have a short on it.

Speaker 1: 00:18:11

Which starts with the Diffie-Hellman key exchange, which you have described in your book.

Speaker 0: 00:18:16

Oh, thanks, you're plugging it as well.

Speaker 1: 00:18:17

And then you use a stream cipher which is essentially a one-time pad where this piece of paper that we talked about we have we know that given the key exchange we did we know what the what that page has to look like so We don't have to give each other a piece of paper with the cipher on it.
We both construct the same cipher, but it's the same cryptographic idea.
So that's pretty cool.
It's on by default.
This does not mean that all your connections are now encrypted by default.
The devil is in the details here.
When you connect to a new node, you will try this encryption only if you think the other side supports it.
And we talked in a very, very early episode about DNS seeds, probably episode 2.
Oh wow.
Where, you know, the way nodes bootstrap is they get a list of other nodes and then they call those other nodes and say, hey, do you know about other nodes?
And you keep a list of which nodes exist in the network.
But you don't just keep track of which nodes exist and their IP addresses, you also check which features they support.
And one of those features can be that they support is encrypted communication.
So only if through the gossip circuit you heard that this node supports encryption, then you're going to try it.
Otherwise you're not.
And so this would be probably a future change.
If we know that this works, then we might just try an encrypted connection all the time and fall back to unencrypted if it doesn't work.
So now this is, even though it's on by default, it's still a bit conservative.

Speaker 0: 00:19:53

Right.
Okay, so so far we talked about something that was removed, something that's a very niche problem.

Speaker 1: 00:20:02

Not niche if you use Windows.
But.

Speaker 0: 00:20:07

No, I think you're, we're not there yet.

Speaker 1: 00:20:10

Okay.

Speaker 0: 00:20:12

I said so far we've talked about something that was removed.
Something that solves a weird virus thing.

Speaker 1: 00:20:21

Yeah, but that may not be a weird problem.
If somebody does this, then it's gonna affect everybody who runs a virus scanner, like not just a few people.

Speaker 0: 00:20:28

I'm not impressed, Shorts.
Where are my soft forks?
Where's, where are my, Does this make number go up?
I don't think so.

Speaker 1: 00:20:37

This is finally fixed lightning.

Speaker 0: 00:20:39

Yes, please.
Okay, moving on to the next one.
Network adjusted timer moves.

Speaker 1: 00:20:44

Speaking of unimportant problems.
Yeah, so there is this rule that says, if you see a new block, that it cannot be from the future.
Well, it cannot be for more than two hours in the future.
So there's a little grace period there.
Question is, what is two hours in the future?
What if your clock is wrong?
You might be wrong about that.

Speaker 0: 00:21:05

Wait, let me repeat that for those that don't know and didn't quite follow.
Yeah, you find a new block or someone sends you a new block.
The block has a time in it.
And then one of the things you do to check if the block is valid is to check that it wasn't mined in the future or in the past I guess right?

Speaker 1: 00:21:24

No the past is fine because you might be catching up on old blocks.

Speaker 0: 00:21:27

Okay yeah it's not mined in the future and the future means two hours or more into the future.

Speaker 1: 00:21:32

Yeah, now there are limitations to the past by the way, but that is relative to earlier blocks, right?
You cannot go, blocks can't go back in time.

Speaker 0: 00:21:38

Right.

Speaker 1: 00:21:38

But yeah, you cannot accept the block that's from the future.

Speaker 0: 00:21:43

Right, now we're talking about blocks in the future.
Yeah.
They can't be binded in the future, which is two hours in the future.
And now what you said is how do you define what is the future?
Well, usually use a clock and I guess that's what you're getting at.

Speaker 1: 00:21:55

And so I think it was Satoshi or maybe one of the earlier contributors who thought, well, what if your clock is wrong?
You might be rejecting blocks, even though they're valid because your clock is wrong, not the miners clock.
And the solution to that was to, when you connect to other peers, you ask them, Hey, what time is it?
What time is it?
What time is it?
You know, Not that long ago, that's a question you would ask people on the street.
Yeah.
The amazing.

Speaker 0: 00:22:20

Do you have the time?

Speaker 1: 00:22:21

Yeah, exactly.
Nowadays, well, we stopped doing that as humans and Bitcoin Core stops doing that now too.
Well, not entirely, but it's, it doesn't do anything with it anymore.
That's the change.
Because the problem is what if your peers are lying to you about the clock?
That's not ideal.
And also, you know, I think most computers nowadays get their clocks set by a network, you know, get the time from the network, from their internet provider or from some other source.
And so my thinking is that they're generally either very accurate to within the second or they are completely wrong because.
Yeah, it's 1900.
Yeah, I've had one of these cheap computers where you, where like the little battery is dead, so when you turn it on, the clock is back at the second zero, which is January 1st 1970.

Speaker 0: 00:23:14

Is that it?

Speaker 1: 00:23:15

That's typically the year zero for a computer.
Okay, so yeah, so now I think it will still warn you, like, hey, this block seems to be, yeah.
No, I think it'll warn you saying, hey, your peers think the time is different than I think it is, but that's it.
It's just gonna work, it's gonna use its own clock.

Speaker 0: 00:23:36

Do you think that in the future when religion is just displaced, we'll actually use 1970 as the year zero?
You think future humans will think that way, Sjoerd?

Speaker 1: 00:23:47

Do you think that when we invent something better than a QWERTY keyboard, we'll actually use it?
I'm still holding my breath.

Speaker 0: 00:23:54

I'm not going to hold my breath for that one.

Speaker 1: 00:23:56

I don't think we're going to change this.

Speaker 0: 00:23:58

Okay.
Because the QWERTY keyboard is not going to change?

Speaker 1: 00:24:04

If we don't change the QWERTY keyboard with obvious productivity benefits why would we replace the calendar system which you know doesn't matter.
Never?
I'm sure at some point people will be like, oh, it's the year 370, 225, 695.
Yeah, that gets a little tedious.
But maybe they'll just not count the thousands or something like that.

Speaker 0: 00:24:30

Or we change it to 1971.
That's what Bitcoiners will agree with.

Speaker 1: 00:24:36

That will be the rounding error in 300 million years.

Speaker 0: 00:24:41

Next point.

Speaker 1: 00:24:46

Another amazing problem.

Speaker 0: 00:24:49

External signing for Windows disabled.
Oh yeah.
This is about hardware wallets.

Speaker 1: 00:24:55

Yes, so there is a feature in Bitcoin Core where you can connect a hardware wallet to your USB port and then you have to install HWI.

Speaker 0: 00:25:02

Some people think that Bitcoin itself will be used as a clock source.
What do you think of that?
That annoys me.
That's philosophical.
Because Bitcoin is not a clock.

Speaker 1: 00:25:12

Bitcoin nodes use a clock, A trusted clock even.

Speaker 0: 00:25:17

You measure the time in blocks nowadays.

Speaker 1: 00:25:20

No, you do not.
Why not?
Because your node checks the blocks to see that their times are valid.

Speaker 0: 00:25:28

I guess that's what we were just talking about.
Yeah, exactly.
Okay, moving on to hardware wallets.
I won't interrupt you anymore.

Speaker 1: 00:25:34

Yeah, so there is a tool called HWI.
We have talked about that in the past.
It's a separate thing you download.
You tell Bitcoin Core where it is, and then you can use hardware wallets right from the GUI as simple as like create new wallet, SSO, which you like to use your cold card if you connected it?

Speaker 0: 00:25:51

Good choice.

Speaker 1: 00:25:53

And it'll import the keys, you can send with it, it'll just work, it's pretty cool.
However, Windows support has always been a bit iffy.
It's been disabled a few times, it's been enabled a few times.

Speaker 0: 00:26:03

What's iffy about it, why is it iffy?
Ah, Windows is just painful.
Hard to program for, like what's the problem?

Speaker 1: 00:26:12

Yeah, I think it would just, either it was broken in Windows or the support for Windows broke something else that we needed.

Speaker 0: 00:26:20

So this is a Windows only problem.

Speaker 1: 00:26:22

So I think it's been, yes, and it's been, we removed support for it I think a year ago, wasn't mentioned in the release notes, nobody complained about it.
Then it was added back, which I think was also not mentioned in the release notes.
Nobody was excited about it.
Now it's removed again, which is mentioned in the release notes, and it should be back again in the next version.

Speaker 0: 00:26:42

Okay, so if...

Speaker 1: 00:26:42

I think nobody's going to care about it.

Speaker 0: 00:26:45

If you have a hardware wallet and you're using Windows and you have a Bitcoin Core node where you use the wallet with the hardware wallet, then you shouldn't upgrade.
And you're using HWI as a tool?

Speaker 1: 00:26:58

Because there's other tools, right?
There's Sparrow Wallet and there's Spectre.
Those will work around the problem.
So it's only under those very specific circumstances that it would cause a problem for you.

Speaker 0: 00:27:07

Okay, and you think that's basically no one is using it that way?

Speaker 1: 00:27:11

Well based on the fact that nobody complained the last time it was removed.

Speaker 0: 00:27:16

Yeah but most people aren't gonna, they don't even know where to find you.

Speaker 1: 00:27:20

But they know where to complain.

Speaker 0: 00:27:22

Do they?
What's the service number for Bitcoin Core?
X.com.
That's true.

Speaker 1: 00:27:30

This would have gone viral if somebody was bothered by this.

Speaker 0: 00:27:32

Clearly.

Speaker 1: 00:27:34

Anyway, yeah.
So, yeah, if you do need this, yeah, then I guess don't upgrade to 28.
To 27.0, wait for 28.0. It'll be fixed again, probably.

Speaker 0: 00:27:43

Okay.
The last part, we have one more, and that one is actually kind of interesting, I think.
So this is about UTXO selection in the wallet and there's a new algorithm, as I understand it, called CoinGrinder.
Is it a new algorithm?
Yes.
Right.
So this is about you want to send coins from your wallet and then your wallet has to decide which coins to use.
And there's like a way to determine which UTXOs, which coins it's going to use.
So what's new about CoinGrinder?

Speaker 1: 00:28:15

Yeah.
So a little bit of a background on coin selection.
The initial coin selection that was built in was using something called the knapsack algorithm, which I guess is what it sounds like.
You have a bag and you want to put a bunch of stones in it from different sizes and then the question is how do you optimally, what's the maximum number of stones you can fix fit into the bag or a problem like that?
If you only put the big stones in, then you have a lots of room left.
If you only put the small stones in, then it's not efficient either, so.

Speaker 0: 00:28:43

The analogy here would be a lot of room left is a lot of change, right?
But that's not really a problem.

Speaker 1: 00:28:48

Yeah, I don't know.
Well, the problem is if you, in this case, if you use lots of very small coins, then you're paying lots of fees because every coin you put into a transaction increases the fees.
And that general problem is the knapsack problem, if my computer science understanding is correct, and that's unsolvable, there's no perfect solution, you can just approximately solve it.

Speaker 0: 00:29:10

It's one of these hard problems, right?
Yes.

Speaker 1: 00:29:13

So There were other algorithms, branch and bound was one.
I don't actually know exactly how it works.
But it boils down to it tries to find a reasonable set of coins to put into the bag to spend with, but not necessarily the cheapest one.

Speaker 0: 00:29:28

Branch and bound try to optimize for not having any change, I think, right?

Speaker 1: 00:29:35

I think, yeah, that's as little waste as possible.
So I think we do want to have change.
Well, I think either it tries to find a coin that just spends it directly, that's nice, if you don't need change at all.
But otherwise, if you do have change, then you don't want to have the absolute minimum amount of change.

Speaker 0: 00:29:56

You don't?
I mean, it's just one.
No, because of privacy.
Change is also one UTXO, right?

Speaker 1: 00:30:00

Yeah, but for privacy reasons, you don't want to reveal which side is change.
And so it deliberately spends a bit more and creates higher change.

Speaker 0: 00:30:09

Oh, I remember that.
Yeah, we mentioned that in an earlier episode.

Speaker 1: 00:30:12

I don't know if that is actually dependent on the algorithm used, whether you use Knapsack or branch and bound or this other one.
It might just be something that we do anyway.
And then there's a different algorithm to find coins based on that choice.
I don't actually know that much about coin selection.
Should ask Merge, he wrote a whole thesis on it.
And he also designed this algorithm.

Speaker 0: 00:30:29

It's kind of a science of its own.

Speaker 1: 00:30:31

Yeah, there's all sorts of trade-offs, right?
For privacy reasons, you want to maybe have a bit more change than you really need.
But also, there's a time preference element here where the cheapest transaction right now, So using the fewest coins as possible.
That's great now, but in the long run it's going to create lots of very small coins in your wallet and then eventually you have to pay.
So normally the wallet does not try to find the very cheapest transaction, it tries to also act in your own long term interest.
However, and this is where the new algorithm, CoinGrinder, comes in, if fees are very high, which in this case is defined as more than 30 cents per byte, but you can change that, then it's going to find the cheapest way to spend it.
So it's going to ignore the future, it's going to say, okay, right now fees are high, hopefully they'll go down again in the future.
I'm just going to do whatever is cheap because otherwise...

Speaker 0: 00:31:27

I can make this payment with using only one UTXO, So that's what I'm going to do because that's the cheapest way.

Speaker 1: 00:31:32

Yeah, because there were situations where fees were 600 sats per byte and the Bitcoin Core wallet was like, oh, let me spend 25 coins now.
And then you were paying, I don't know, hundreds of dollars in fees.

Speaker 0: 00:31:43

Right.
Okay, so it does that if fees are 30 VBytes per...
30 SATs per VByte or more.
But you say you can adjust that manually?

Speaker 1: 00:31:55

Yeah, I believe there's a setting.
It's specified in the readme.

Speaker 0: 00:31:58

It's not just an algorithmically changing thing, but for now...

Speaker 1: 00:32:02

No, I guess the problem is what is high depends on the exchange rate and also depends on the long-term fee rates.
Because if fees will never go below 30, then you should really not use this algorithm even at 30.
It's really designed for spikes.

Speaker 0: 00:32:21

But what is a spike?
Well, I mean, there's probably some way, Mert, if you're listening, we need an algorithm to algorithmically adjust your algorithm.

Speaker 1: 00:32:32

Yeah, well, one of the problems is that if you're not running your node all the time, you don't necessarily know what the fee rates are historically, because if you only look at what's in blocks, you could be fooled by the miners into thinking fees are higher than they are.
So it's a very tricky problem.

Speaker 0: 00:32:48

Yeah.
Anyway, so that's in Bitcoin Core 27 now.

Speaker 1: 00:32:52

That's right.

Speaker 0: 00:32:53

So if fees go up, then this will sort of click on in the same way that everything in your home, Shor's clicks on automatically.
Exactly.
For those that don't know that, Shorz doesn't like touching things, so he has everything automated.

Speaker 1: 00:33:09

And then you spend more time maintaining it.

Speaker 0: 00:33:12

It's like dog from Back to the Future, where feeding the dog is automated.
Exactly.
I think that's it for our episode, right?

Speaker 1: 00:33:25

Yeah, I think we should mention there is a testing guide.
Hopefully we'll remember to put that in the show notes.
Which takes you by the hand and explains if you wanted to test this new version, ideally with fake coins, testnet coins, signet coins.
It'll tell you how to do that.
And that's nice because we prefer it when people find bugs before the release is final.
So help is welcome.

Speaker 0: 00:33:47

Okay, one other quick question.
I also saw, so there's also new releases like 26.1. I saw, what is it, what's the point of that?

Speaker 1: 00:33:57

Yeah, so let's say you're really passionate about the Bitcoin consensus.
And well, in this case, that doesn't matter because it's still in there, but let's say it's removed.

Speaker 0: 00:34:07

Or you're very passionate about using hardware wallets on Bitcoin Core with the thing on Windows.

Speaker 1: 00:34:13

Yes, exactly.
If that's your passion, you can use an older, instead of only using the old release, which probably has bugs in it, there is a 0.1, 0.2, et cetera, that only fixes bugs in that earlier release, but doesn't add any of the new features.

Speaker 0: 00:34:31

Okay, there's a new alt release.

Speaker 1: 00:34:33

Yeah, so this is quite typical in software development.
You have a major version that's released and then there'll be back ports for older versions.
So something like Python, you might have version Python 3.7.9, but also 3.6.12 and 3.5.11, whatever it is.
So this is indeed to not force you into using the latest and greatest version but also not saying oh well if you use the old version you can have all the bugs in it.
It's a bit subjective what goes into these backport releases.
Of course, it could, yeah, usually the more relevant bugs.
Anyways,

Speaker 0: 00:35:16

you should just get Bitcoin Core 27.
Get up to date, get the newest, the shiny release soon to be found on BitcoinCore.org or wherever you find Bitcoin nodes.

Speaker 1: 00:35:29

Thank you for listening to Bitcoin?
Explain.
