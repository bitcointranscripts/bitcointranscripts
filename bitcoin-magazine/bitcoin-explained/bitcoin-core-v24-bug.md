---
title: "Bitcoin Core v24 Bug"
transcript_by: jeffreyweier via review.btctranscripts.com
media: https://www.youtube.com/watch?v=66W6_AVSxME
tags: ["bitcoin-core"]
speakers: ["Sjors Provoost","Aaron van Wirdum"]
categories: ["podcast"]
date: 2022-12-29
---
## Introduction

Aaron van Wirdum: 00:00:20

Live from Utrecht, this is Bitcoin Explained.
Sjors, welcome back.
I saw you were promoting your book everywhere in the world over the past couple of weeks.
Where did you go?

Sjors Provoost: 00:00:31

Absolutely.
I went to a place called New York, a place called Nashville and a place called Austin and those are all in the United States.

Aaron van Wirdum: 00:00:39

That sounds very exotic.
And you were promoting your book.
Which book is this yours?
Do you want to promote it on our show as well?

Sjors Provoost: 00:00:46

Yeah, in case nobody's heard of it, it is called Bitcoin: A Work in Progress.
And if you want to find it, because of the way that Amazon actually messed up the indexing, so they basically took the colon in the name, Bitcoin: A Work in Progress, and treated that one as a title and the other as a subtitle.
So you want to look for Sjors Bitcoin and then you'll find it.

Aaron van Wirdum: 00:01:08

Great sales pitch.

Sjors Provoost: 00:01:09

Or you can go to btcwip.com and you'll find it too.

Aaron van Wirdum: 00:01:12

So I saw you promoted on Marty Bent's podcast.

Sjors Provoost: 00:01:16

Exactly.
TFTC.
Yeah, that was a bit unplanned because we happen to be in the same building and they said hey do you want to come on the podcast and we could talk about the book so we talked about that.
Tales from the Crypt.

Aaron van Wirdum: 00:01:27

Yeah so that's why there was no Bitcoin Explained episode for the past couple of weeks.
But we're back, our dear new listener, with this Christmas special of Bitcoin Explained.
Actually, I guess by the time this is released, it's not going to be Christmas anymore, but we're recording it.

Sjors Provoost: 00:01:45

Yeah, the last episode of 2022.

Aaron van Wirdum: 00:01:47

Pretty close to Christmas anyways.
Yeah, I guess it kind of depends on how...I'm not 100% sure if our great, super talented editor is actually working between Christmas and New Year's.

Sjors Provoost: 00:02:01

Well, it's the last episode that was recorded in 2022.

Aaron van Wirdum: 00:02:04

Yes, that's for sure.
So we've got a very special episode for you today.
Dear listener, I hope you're strapped in.
This is going to be a major one.
Sjors is going to educate you about the most important development of the year.

Sjors Provoost: 00:02:19

Yes, we have scraped the absolute bottom of the absolute last barrel that we could find after like an hour of brainstorming topics.

Aaron van Wirdum: 00:02:26

We wanted to bring you something before the end of the year, because otherwise you would have had to manage probably five to six weeks without our voice.
And we didn't want to do that to you, the listeners.
So here we are back with an episode about a bug that was in Bitcoin Core 24.0. But, first of all, let's back up a little bit here.
Let's take it seriously.

Sjors Provoost: 00:02:40

It's a serious issue.

## Explanation of Bitcoin release process

Aaron van Wirdum: 00:02:41

We had an episode on Bitcoin Core 24.0. But then the release of Bitcoin Core 24.0 was delayed by quite a bit.
And that was because of a discussion about full RBF, there was an option to switch on full RBF in the Bitcoin Core 24 node.
And that sort of pushed back the actual release of Bitcoin Core 24.
And then finally Bitcoin Core 24 was released, but then it kind of wasn't.

Sjors Provoost: 00:03:27

Yeah, there was a bug in it.
But the release was announced.
But if you went to the website bitcoincore.org, you would actually still find version 23.
So only some advanced users would have been able to download the actual release.

Aaron van Wirdum: 00:03:39

So hang on, if Bitcoin Core 24 is not on bitcoincore.org, is it really released?

Sjors Provoost: 00:03:47

In a sense, yes, because there was a tag made on GitHub, which is signed and there was an announcement so people would be able to download it if they went straight to the FTP download site, where you just see the list of files, but not if you went to the main website because that page takes a little bit longer for people to look at and then that gets released as well.
The page that points to the release.

Aaron van Wirdum: 00:04:09

Wait, so does the page usually refresh automatically to include the latest release?

Sjors Provoost: 00:04:15

No, the website is on GitHub too.
So people make a pull request to add a page that points to the new release and maybe some release notes and other remarks.
And that always takes a few days and within that few days, the bug was found.
And so it was postponed.

Aaron van Wirdum: 00:04:31

Okay, I see.
So there was technically an official Bitcoin Core 24 release, but that release never showed up on bitcoincore.org.
What you do find on bitcoincore.org right now is Bitcoin Core 24.0.1. And this is because there was a bug in the original, technically officially released Bitcoin Core 24 release.
Is that right?

Sjors Provoost: 00:04:56

Yeah, exactly.
And when something like that happens, then the next release can be just called 24.0.1, basically not immediately 24.1. Because it's like a quick enough fix, basically.
Probably nobody's gonna be running the old version.

Aaron van Wirdum: 00:05:12

So first of all, there was a bug in 24, but that was not caught in the release process.
That's why there is the release candidate process, right?

Sjors Provoost: 00:05:29

Yeah, so the idea is the release candidate, you hope that people test it and find bugs.
But of course, not everybody's doing that and not everybody will be testing every single possible feature in every way that they, every way that you can break it.
So that was not found in time.

Aaron van Wirdum: 00:05:43

So a bug was found after it was officially released, but before it was published on the bitcoincore.org website.
Okay, Sjors, what's the bug?
What happened?
What went wrong?

[omitted podcasting 2.0/boosts segment]

## What makes a non-RBF transaction new?

Sjors Provoost: 00:07:10

He or she is paying 10,000 sats and has a question which is related to the topic we talked about earlier, namely RBF.
What makes a non-RBF transaction new to a node and when is it just another version?
Is it easy to consider the new transaction if some of the input UTXO changes.

Aaron van Wirdum: 00:07:33

Sorry can you repeat the question?

Sjors Provoost: 00:07:36

What makes a non-RBF transaction new?

Aaron van Wirdum: 00:07:40

What makes a non-RBF transaction new?
Alright so what makes a transaction new?

Sjors Provoost: 00:07:44

Rather than another version.

Aaron van Wirdum: 00:07:45

Okay yeah.
Do you want to answer that?

Sjors Provoost: 00:07:49

Yeah, so my guess is, it depends on how the node, how your wallet wants to interpret these things.
In essence, a transaction spends outputs.
So if any output is spent by another transaction, then that is a different transaction.

Aaron van Wirdum: 00:08:01

I guess technically on the consensus level, any change to a transaction makes it a new transaction, right?
But there's some nuance here maybe when it comes to relaying.

Sjors Provoost: 00:08:12

What makes it new versus another one?
You could have two, if you have one input and one transaction and then another input and another transaction and those are different transactions, they don't exclude each other but the case we're interested here is when you're replacing a transaction that means that you have another transaction that spends the same input.
Or at least one of the same inputs, so that only one of those two can exist.
And then the question is, what is new and what is old?
Well, part of that just depends on what you saw the first as a node before RBF, which would be like, if I already know a transaction, then whatever else comes in is new.
But that could be different for different nodes because you might receive them in different order.
But whether you call it another version or whether you call it new, it just depends on the interpretation of the wallet, how it wants to display it.
So it could, I think in Bitcoin Core, it'll put a cross through the old one and then just put the new one in its place.

Aaron van Wirdum: 00:09:04

Yeah, I guess this question sort of derives probably from our conversation about these kinds of topics where we're using terms like new and version, but in actual Bitcoin protocol, there's no such distinction, right?

Sjors Provoost: 00:09:21

Yeah, exactly.
At least I think not, because you have the end version field, but I think with RBF, it's just a flag.
It's not a number that goes up.
The only thing that goes up is the fee.
So if a wallet wants to be a little bit smart about it, it could look at which one pays the highest fee.
And then that's sort of the newer one.
That's probably intended as the newer one.
So if you want to make a good wallet UI, you might want to show something that it increased the fee rather than showing two transactions.
But that's really just up to the wallet authors, how they want to interpret what they're seeing on the chain.
The blockchain doesn't really care.
Well, the mempool doesn't really care.
The blockchain definitely doesn't care.

Aaron van Wirdum: 00:09:59

Yeah.
I guess it's just way more binary.
Either a transaction is valid or it's not.
And if it's not, that can be because it's conflicting with the previous transaction.

Sjors Provoost: 00:10:10

Yeah, but then valid in the mempool depends on your mempool policy, right?

Aaron van Wirdum: 00:10:16

All right.
Well, that was maybe a very confusing answer.

Sjors Provoost: 00:10:23

It's a good question.
I would also recommend people, if you have questions, also ask them on Stack Overflow.
Or Stack Exchange because you'll get better answers.

Aaron van Wirdum: 00:10:31

Like I said, I think the question kind of derives from our conversation about it.
And it doesn't really map on the actual Bitcoin protocol.
So that makes it a little bit hard to answer.
But hopefully our attempt is at least worth something.

Sjors Provoost: 00:10:44

How much did they pay for?
10,000 Satoshis.

Aaron van Wirdum: 00:10:49

All right.
Do you think this answer was worth 10,000 Satoshis?

Sjors Provoost: 00:10:52

I think it was worth way more than 10,000 Satoshis.

Aaron van Wirdum: 00:10:56

Okay, cool.

## Explanation of the bug

Aaron van Wirdum: 00:11:57

So then we're back to the main topic, Sjors.
Here you finally get the answer you've been waiting for.
There was a bug in Bitcoin Core 24.
That's why there was a Bitcoin Core 24.0.1 release.
What was this bug?

Sjors Provoost: 00:12:14

Yeah, it was a bit of a foot gun basically.
I don't know if foot gun is the right word.
You could lose a bunch of money.
So in Bitcoin Core when you're sending money you can either let the wallet decide automatically which of your coins to use to send the money or you can manually specify exactly which coins you want to use or some combination of both where you say well I want to pay one Bitcoin to this guy and I want to use this specific 0.3 Bitcoin coin that I have but other than that you figure it out which coins to take from the wallet.

Aaron van Wirdum: 00:12:44

Right, when you're saying coins the technical term here is UTXOs.
I guess people that know that know what you mean anyway.
So yeah, my addition doesn't really help anyone.

Sjors Provoost: 00:12:54

No, that's fine.
So the analogy is you have a wallet and there's a bunch of coins and paper notes in it and you have to pay something and you take one euro coin out of it and you say I definitely want to use this but then you have some other guy going through your wallet and deciding which other coins to use to add up to 10.

Aaron van Wirdum: 00:13:14

Well if you want to use the analogy, sometimes when you're abroad in a country where you don't know which coins are what and you don't want to waste time, you just sort of show all your coins to the merchant and then they'll just pick.

Sjors Provoost: 00:13:24

They'll do the coin selection for you.

Aaron van Wirdum: 00:13:26

Exactly.
That happens sometimes.

Sjors Provoost: 00:13:27

I have done that a few times.

Aaron van Wirdum: 00:13:28

So that would be the analogy here.

Sjors Provoost: 00:13:31

So anyway, there was a bug in that where you would basically select a couple of coins and then due to the bug it would use those coins twice to calculate what was going on.

Aaron van Wirdum: 00:13:54

Ah, wait, so you got a number of coins, UTXOs, and when you're manually selecting them, then for the fee calculation it would falsely assume that you selected them double?

Sjors Provoost: 00:14:08

Yeah, exactly.
And for some reason the net result of that mistake is that you might be paying a very very large fee because you think you're paying say one cent of fees but actually because you've counted this 10 euros twice it somehow includes it twice.
I don't completely understand how it happened but that was basically the nature of the bug.
So you'd be paying a very large fee now fortunately there is a warning system if you pay a really really high fee it will abort but there's another feature in the wallet where you say I want to pay this address and I don't care about the precise amount, I just want to send this coin or this set of coins.
You select the coins that you want to send over.
So this can be useful for privacy.
If you receive your salary or whatever, and that's one coin, essentially, and you want to send only your salary to an exchange and none of the other coins in your wallet, so you select your salary and you send it to the exchange and if you use that feature in combination with this bug you would lose even more money and then the warning system didn't work correctly.
As you notice I'm being a bit vague because the actual bug is not described very well.
That is the actual implication of the bug is not described very well.
The bug itself is described as what was wrong in the code and that's pretty obvious.
So there was a pretty bad way to lose some money.
So don't use 24.0, just use 24.0.1.

## How did the bug get released?

Aaron van Wirdum: 00:15:38

All right.
Well, this sounds like a bug, a glitch.
And I think you mentioned, I'm still going to ask.
So how does this get into the code?
Why is this in there?

Sjors Provoost: 00:15:49

So this is interesting, of course, to look at what exactly went wrong here.
So the bug itself was like one line of code that should not be there.
I think it was a command called break, which jumps out of a loop, and that command was a mistake.
Now how does that get there?
It was part of a refactoring.
So basically refactoring means you take an existing piece of code that may be ugly and you rewrite the same code but prettier in a way that it doesn't change any of the behavior.
And so that's good because better, cleaner, more readable code in the future will lead to fewer bugs.
However, you might make a mistake replicating the original behavior and that's what happened here.
So I think in practice here, there were a bunch of different functions that were responsible for removing.
So if you take these coins that you've manually selected, then it would have to remove those from like another set of coins so that you don't select coins twice, something like that.
And because the coin selection algorithm, it looks through the coins in your wallet it tries to see which coins can I add to this transaction but it shouldn't be adding coins that are already in your transaction so it kind of had to do the subtraction there and that code was doing the subtraction only once.
I think it was only subtracting one coin that you selected, but not all of them.
So this is the kind of bug that you might not see if you only select one coin, you'd only see if you select two coins.
So it's, difficult to run into this.
So the code was doing 12 separate steps to remove these coins.
And with the new version, it would only need two steps to remove the coin.
So it was cleaner, but it had the mistake in there and the mistake was not caught.
It wasn't caught during the code review by the people looking at it.
There were also no tests that failed.
So there was no test where this precise scenario of adding two coins, etc., etc. was there.
Because either could have caught it.
Somebody could have caught it in a review or somebody, some automated test could have caught it, but it didn't.
And so the way that that is fixed is, first you fix the original bug, and second, you add tests that would have caught it, so that at least the same bug could not happen again.
That's pretty much what happened.
And the other reason it wasn't noticed is that it was only in the release and not in the master branch.
So that's an interesting aspect there.

Aaron van Wirdum: 00:18:15

The master branch is the main thing that Bitcoin Core developers work on.
And once in a while, Bitcoin Core developers say, from here on out, this is the new release.
And they keep working on the master branch for new features, and the new release is going to be released.
And somehow this bug was only in the release.

Sjors Provoost: 00:18:30

Yes, exactly.
Because the bug was introduced in this refactor and then after that bug was introduced, the split to the release was made and then somewhat later on master the bug was accidentally fixed.
Not deliberately fixed.
And the way you accidentally fix something is you do another refactor and something and then you actually make another mistake because you're not replicating the original behavior.
Because nobody wanted that original behavior, nobody would have noticed that either.
So it was accidentally fixed on master and that also has to do with the odds of finding it because who is testing Bitcoin Core?
Well, part of it is people running the master branch.
Those are probably other Bitcoin Core developers that are just trying, snapshots off the master branch that, are not supposed to be very safe.
It's supposed to be correct but it's more likely to have bugs.
But because the bug was not in the master branch, nobody testing the master branch would have noticed this.
Only people testing the release branch and that might be a much smaller group of people in practice.
And like we described it's not the easiest thing to trip on.
But if you do trip on it, it's very painful.
So it was definitely worth fixing.

Aaron van Wirdum: 00:19:33

Well, there you have it.
That's why the new release is Bitcoin Core 24.0.1 instead of just Bitcoin Core 24.
You are enlightened, our dear listener.

## Additional bug fixes

Sjors Provoost: 00:19:45

Yes, there are two other bugs in there too, but they're less important and in very different areas.

Aaron van Wirdum: 00:19:50

Oh, that's a kind of a depressing note to close the episode on.

Sjors Provoost: 00:19:54

There's always bugs.
So what happens is after a release, the developers pile up existing bug fixes for a future release.
So, there'll be a version 25.0, which will have the new master branch on it, but there'll also be a version 24.1, 24.2, which will have only sort of bug fixes in it that are important enough to put on the old releases.

Aaron van Wirdum: 00:20:21

Wait, wait, wait, wait.
Are there still bugs in Bitcoin Core 24.0.1 as far as we know right now?

Sjors Provoost: 00:20:25

I don't know.

Aaron van Wirdum: 00:20:26

I thought that's what you said, but maybe I misheard.

Sjors Provoost: 00:20:28

No, the general process is that we'll collect bug fixes over time.
So maybe immediately after release, there is no known bug, or maybe there's a known bug, but there's no fix for it yet.
But then over time, say the next six months or a year, bugs will get fixed.
We'll find out there were bugs in version 24.
And then you can do two things to your users.
You can say, tough, just download version 25 if you want that bug fixed.
But then they have to download all these new changes in version 25, which people don't like.
So there will also be version 24.1, which only fixes the bugs, but doesn't have any of the other new changes.
That's called backporting.

Aaron van Wirdum: 00:21:06

Sjors, I just want you to tell our listeners that Bitcoin Core 24.0.1 is clean and we're ready for the new year.
We're ready for 2023 with Bitcoin Core 24.0.1.

Sjors Provoost: 00:21:20

Well, all I can tell you is that currently there is a milestone called 24.1 and it doesn't have any bugs in it.

Aaron van Wirdum: 00:21:27

There we go end of the episode but thank you for listening to Bitcoin Explained
