---
title: The Block 1, 983, 702 Problem
transcript_by: sahil-tgs via review.btctranscripts.com
media: https://bitcoinexplainedpodcast.com/@nado/episodes/episode-87-the-block-1-983-702-problem-s7s3j
tags:
  - bitcoin-core
  - security-problems
speakers:
  - Sjors Provoost
  - Aaron van Wirdum
date: 2023-12-21
episode: 87
summary: |-
  The episode from "Bitcoin Explained" podcast, hosted by Aaron van Wirdum and Sjors Provoost, discusses a complex issue in the Bitcoin protocol known as the "Block 1, 983, 702 Problem." The dialogue delves into the historical bug in Bitcoin's protocol that allowed for the existence of duplicate transactions, leading to potential consensus failure and the loss of Bitcoin for miners. This problem, stemming from an "OG Satoshi bug, " has been partially addressed over time through various Bitcoin Improvement Proposals (BIPs), specifically BIP30 and BIP34, which aimed to prevent duplicate transactions by ensuring unique coinbase transactions in each block.

  However, a subsequent realization highlighted a loophole: early blocks (pre-BIP34) could contain numerical sequences in their coinbase transactions that might accidentally be replicated in future blocks, posing a potential risk of creating duplicate transactions again. This issue, dubbed the "Block 1, 983, 702 Problem, " could theoretically allow an attacker to exploit this loophole, though it would require significant resources and specific conditions to be feasible.

  To mitigate this risk, a temporary fix was implemented in 2018, deciding to reinstate BIP30 checks from block 1, 983, 702 onwards, giving the Bitcoin community time to find a more permanent solution. Several potential fixes are discussed, including making SegWit mandatory for all blocks, which would inherently prevent the duplication issue by ensuring a unique identifier in each block that was not present in pre-BIP34 blocks.

  Throughout the conversation, Provoost and van Wirdum explore the technical nuances of the problem, the historical context of its discovery, and the implications for Bitcoin's security and consensus mechanism. They emphasize the importance of proactive problem-solving in the Bitcoin community while acknowledging the complexities involved in implementing changes to the protocol.
---
## Introduction

Aaron van Wirdum: 00:00:19

Live from Utrecht, this is Bitcoin Explained.
Hey Sjors.

[omitted sponsors segment]

Aaron van Wirdum: 00:01:20

Sjors, today we're discussing a very niche bug that I had never heard of, but apparently there's a bug in the Bitcoin protocol.

Sjors Provoost: 00:01:31

Well, there was a bug in the Bitcoin protocol.

Aaron van Wirdum: 00:01:35

But there's still a problem.

Sjors Provoost: 00:01:38

There was a bug, then there was no bug, then there was a bug, then there was no bug.
There's still a problem, but not a bug.

Aaron van Wirdum: 00:01:45

Okay, I see.
So, there was a bug, now there's no bug, but there's still a problem which is not a bug.

Sjors Provoost: 00:01:51

Well, it's kind of a bug, but it's not like a dangerous bug like the original thing.

## Explaining the Bug and Its Implications

Aaron van Wirdum: 00:01:55

Sounds pretty buggy.
Anyway, so it's called the "1,983,702" problem.
Did I say it right even?
The block "1,983,702" problem.

Sjors Provoost: 00:02:11

Yeah, that sounds good.
Or the block "1,983,702" problem.

Aaron van Wirdum: 00:02:14

So, this will be a problem in.

Sjors Provoost: 00:02:18

Yeah, there's another term you could use is the BIP34 does not imply BIP30 problem.

Aaron van Wirdum: 00:02:27

I don't know which one is worse.
They're both pretty bad.

Sjors Provoost: 00:02:30

Okay, cool.

Aaron van Wirdum: 00:02:31

So, this will be a problem in block, well, again, 1,900,000 something.

Sjors Provoost: 00:02:38

Yeah, which is like a couple decades from now.

Aaron van Wirdum: 00:02:40

Yes, like 22 years from now, my sort of napkin math told me.

Sjors Provoost: 00:02:44

And to be clear, It's a problem, it's not like bad.

Aaron van Wirdum: 00:02:49

Okay, but it is something that needs to be solved eventually, in some way or another.

Sjors Provoost: 00:02:55

It's better if we solve it, yeah.
But it's not like the 2106 problem, which, like in the year 2106, the whole blockchain simply stops.
That's definitely a problem.

Aaron van Wirdum: 00:03:05

Is this not a problem that's going to require a consensus change?

Sjors Provoost: 00:03:09

No, ideally it would.
But not a hard fork.

Aaron van Wirdum: 00:03:12

Okay.
How did you find about it?
Like I said, I'd never heard of this.
Is this just something you, this is your hobby you look for very niche things that no one else has heard about?

Sjors Provoost: 00:03:23

Well, we sometimes need to scrape the bottle of the barrel for episodes titles, but in this case, I was trying to understand a bug in Stratum V2, something I'm working on recently, and had something to do with the coinbase transactions and whether or not it has a witness.
Turns out it does have a witness, or at least it can have a witness, which I didn't know, and That's why I kept banging my head against it.
But as I was trying to understand how the code works, I was reading the code comments, and I came across this like almost full-page story about this problem.

Aaron van Wirdum: 00:03:57

Okay, I'm gonna just call it the "1,900,000" problem because I don't wanna read it in full every time.
So, the 1 million 900,000 problem, we'll start at the beginning.
So, you mentioned there was a bug.
It all started with a bug, right?
And this has been a bug in Bitcoin since the beginning?

Sjors Provoost: 00:04:18

Yes.

Aaron van Wirdum: 00:04:19

Like it's an OG Satoshi bug?

Sjors Provoost: 00:04:21

Exactly, an OG Satoshi bug, which is that it was possible for two identical transactions to exist, or more than one basically, identical transactions to exist in sequence.

Aaron van Wirdum: 00:04:33

It was or wasn't?

Sjors Provoost: 00:04:35

It was possible.
And this was creating a problem because, well, when the transaction exists twice, then the original one essentially just disappears.
This has to do with how transactions work.

Aaron van Wirdum: 00:04:51

Yeah, let's halt here for a second.
So how do you get two identical transactions?

Sjors Provoost: 00:04:56

Same hash.
So, the same hash means it's the same content.
So, it's the same inputs, the same outputs.
And so typically you would expect this in a coinbase transaction in the early days, because a coinbase transaction doesn't have any inputs, or maybe it is the name of your pool, which would be the same if you were mining multiple blocks.
And then the outputs might be the address that you're paying yourself to, which might also be the same of your pool.
So, if you mined in the early days two blocks to the same address and with the same pool name and you were like, I guess that...

Aaron van Wirdum: 00:05:30

yeah.
That makes sense.
So, you're a pool in the early days, you have your Bitcoin address, one blah blah blah blah blah, because that was the early addresses, and you're mining new coins, so there's no inputs, and you just, these new 50 coins are sent to this one blah blah blah address.
And if that happens twice, if you say you mine two blocks in a row, it's going to be the exact same transaction.

Sjors Provoost: 00:05:54

Yeah, however, it also would have to be the same amount, right?
So, this would be either a block with no transactions in it, so no fees.
So the coinbase amount would be exactly 50 Bitcoin back in the day, or it would be coincidentally the exact same total fees.
The thing is, it only happened twice.

Aaron van Wirdum: 00:06:14

Especially In the early days, there were still a lot of transactions that didn't pay any fee, I guess.
Or there was a fixed fee for a while.

Sjors Provoost: 00:06:20

Probably a fixed fee.
So then maybe if you had...
I don't know.
I didn't look at those specific blocks.

Aaron van Wirdum: 00:06:24

Anyways, that is the most likely reason why that would happen.
Is it plausible that it could happen in any other circumstance to identical transactions?

Sjors Provoost: 00:06:36

Well, it could happen as a child of the coin.
So if the coinbase transactions are identical, then you could make another transaction.
Basically, you could just replay another transaction from the past that spends that coinbase transaction.
So the whole history of that coinbase could be repeated.
So if somebody mines a block and then they send it to the Pirate Bay and they download a movie, you could redo all that history.

Aaron van Wirdum: 00:07:00

Yeah, It would just have to start from the same coinbase transaction that's already identical.
That's the only way you can get more identical transactions.
You start from there, yeah.

Sjors Provoost: 00:07:09

Exactly.

Or if you break SHA-256.

Aaron van Wirdum: 00:07:12

Which is also an episode we recorded at some point, I think.

Sjors Provoost: 00:07:17

I don't think anybody broke SHA-256, but we did talk about hashes in general.

Aaron van Wirdum: 00:07:21

We talked about what it means to break it, I think.
Anyways, I'm going on to tangents here.
Okay, so that's how you can get identical transaction IDs. And so you said it's possible, so why is it a bug if it's possible?
Because I thought you were gonna say it's impossible, but you said it's possible.
Why is it a bug then?

Sjors Provoost: 00:07:42

It's possible, it was possible to be exact, but the bug is that it creates problems for you, especially for you as the recipient of that transaction.

Aaron van Wirdum: 00:07:52

So the miner in this case?

Sjors Provoost: 00:07:53

Yeah, so the miner mines, say, 50 Bitcoin and doesn't spend it, and then a week later, he mines 50 Bitcoin and also doesn't spend it.
Now he's like, oh, I've got 100 Bitcoins, how am I gonna spend this?
Oh, I'm gonna make a transaction and this transaction points to a previous transaction, that's what a transaction is to do.
So you would point to the original coinbase transaction by its hash and then also by the position of the output in the coinbase transaction.
But then the question is, which one do you mean?
And the Bitcoin Core software would simply look at the most recent one and would spend that.
And There was only one entry, so it would just be overwritten.
So the original coins would be gone.

Aaron van Wirdum: 00:08:42

Okay, you have to explain this, I think.
Why would the original...
So you say Bitcoin Core would just take the most recent one.
So why wouldn't the older one just also still exist for next time you want to spend?

Sjors Provoost: 00:08:53

Well, so Bitcoin Core keeps track of a list of outputs that exist.
Basically, the transaction hash and the identifier.
So if you add another one that is the same, it would just overwrite it.

Aaron van Wirdum: 00:09:05

Oh, sorry, do you just mean the UTXO set here?

Sjors Provoost: 00:09:08

Yeah, although I think at the time the UTXO set worked a little different than it does now.
But I think essentially it was the same thing.
It's just a list of coins that exist.
So it's a transaction hash and an identifier and whatever script you need to spend it.
And so if you were to create the transaction again, that would just be the same entry in the database.
So the database would think there's only one.

Aaron van Wirdum: 00:09:29

Okay, so not both transactions would be included in this database.
It would just be considered as the same transaction, so there's only one.
So then if you spend it, both are gone because they overlap.

Sjors Provoost: 00:09:41

Because you deleted one entry.
So this can lead to quite strange situations.
For example, let's say you mine a transaction once and then a couple blocks later you mine it again and then you spend it and so then it disappeared, right?
That's one way, but let's say you mine one transaction,
you mine a couple other blocks, and then you mine the transaction again.
Now, if there's a re-org, the blockchain undoes your most recent block, and then creates some other blocks.
That means that your transaction has now disappeared from your point of view.

Aaron van Wirdum: 00:10:29

Yeah, okay, I get it.
So, let me try to re-explain that, even though it was kind of clear to me, but maybe if I re-explain that might help one other person out there.
So, yeah, you're creating a blockchain, obviously, and then the first coinbase transaction is included in block three, and then the next one is included in block seven.
But then there's another block seven, and that's the blockchain that the network goes with.
That becomes the longest chain.
So now your second coinbase transaction is deleted from your UTXO set, basically, or your database, and it's not like the one before that is not like automatically restored either.
So now you lost both.

Sjors Provoost: 00:11:12

Yeah, you lost both.
However, somebody else who just starts up a new blockchain, a Bitcoin blockchain, will never see the original second block.
So they will only see the first block in which you do get the coinbase.
And as far as they're concerned, it's still there.
So now you have a consensus failure.
Because part of the network believes that a coin exists and the other does not and that will explode as soon as somebody tries to spend it.

Aaron van Wirdum: 00:11:33

Yeah, or to put it a little bit more accurately, maybe...
I mean, I think you're saying it technically accurately, but the more normie way of saying it is there's no consensus on who owns which coins.

Sjors Provoost: 00:11:44

Well, yeah, There's no consensus on who owns that, on whether that specific coin exists.

Aaron van Wirdum: 00:11:48

Not so much who owns it.
Well, that's a technical way of saying it, right?

Sjors Provoost: 00:11:51

Well, it's not about who owns it, it's that it exists or not.
So you can spend a coin that doesn't exist.
It's not about not satisfying the script, but it's just about the coin not existing.

Aaron van Wirdum: 00:12:01

Yeah, you're right actually.
In the real case, some nodes would actually think the coins don't exist at all anymore because yes, I see what you're saying.
Yeah, you're right.
Anyways, the important part is that the UTXO set or what, Sorry, why do you not call it the UTXO set?

Sjors Provoost: 00:12:17

Did you say back in the day was- So this is the part I'm a little vague on, but initially the concept that we call the UTXO set, so a list of coins that exist, is not something that Satoshi invented as such.
I think we'll cover that again maybe in a future episode.
But this idea of having a database of which coin exists and you just add and remove coins from it, I think at the time it was not like that.
It was just a list of all transactions that were still relevant or something like that.
It was less efficient.
So, I think in 2018 or 2017, it was refactored into what we would now consider the UTXO set.

Aaron van Wirdum: 00:12:58

Okay.

Sjors Provoost: 00:12:59

But this less efficient implementation had the same problem.
The modern UTXO set would definitely have this problem.
And my understanding is the original one had two, even though it stored more data than we do now.

Aaron van Wirdum: 00:13:10

Anyways, the key point here being that the ownership records that every node holds would start to diverge.
And if that starts to happen, that is a consensus failure.
That you could get to a place where you try spending coins and it confirms on your end and it doesn't confirm on the other end and networks start to, it's chaos.
Like that's, so that's potentially, that was a potential actual risk with this OG Satoshi bug.

Sjors Provoost: 00:13:35

Yeah, and as far as I know, what did happen was there were two instances of these duplicate coinbases.
Basically miners losing 50 BTC.
But I don't think there were cases of also re-org on top of that that would have created this mess.
But maybe there was and nobody noticed it.
Because the mess would not have been...
Well, I think we would have noticed it now, yeah.

Aaron van Wirdum: 00:13:58

Probably right.
That would have been very unlucky as well.
Like, you've got to have an exact re-org exactly on that block where this exact block happened.

Sjors Provoost: 00:14:07

Yeah, and because as far as we can tell it only happened twice, it might have happened more often in chains that never survived.

Aaron van Wirdum: 00:14:14

Well, no, then we would have the problem, right?

Sjors Provoost: 00:14:17

Well maybe we are the surviving chain where that didn't happen, but there may have been other chains where it did happen and it didn't survive.

Aaron van Wirdum: 00:14:23

Well we would have probably heard it then at some point, don't you think?
Because then there would have been nodes with these different transaction records, UTXO, set, whatever you want to call it.

Sjors Provoost: 00:14:32

Yeah, but I mean, if this was long enough ago, maybe they just restarted the computer and just didn't care, but probably didn't happen.
Fair.

Aaron van Wirdum: 00:14:40

All right.
So this was the OG Satoshi bug.
And This bug was fixed.

## Addressing the Bug: BIP30's Role

Sjors Provoost: 00:14:47

Exactly.
And this is where BIP30 comes in.
This was introduced in 2012.
What BIP30 does is very simple.
It says there shall never be two transactions with the same hash at the same time.

Aaron van Wirdum: 00:15:01

At the same time?

Sjors Provoost: 00:15:02

At the same time.
As in, if you create a transaction right now, it's not allowed to already exist in the UTXO set.

Aaron van Wirdum: 00:15:08

Okay, but it's just an invalid transaction.
So if the same thing would happen, if the miner would create this coinbase transaction where he pays himself to the same address.
The Bitcoin network nodes, my node, your node, would just say, this is not valid, you just wasted your energy, we're going to wait for a valid block.

Sjors Provoost: 00:15:25

Exactly.
Now, let's say they do that, they make a coinbase, then they spend it, then they can make the same coinbase again.
That's no problem.
So BIP30 does allow that.
So that was great and that worked.
The only problem is that this rule is a bit difficult to check, because it means that whenever you get a new block, for every transaction in that block, you have to make sure that it doesn't already exist, the transaction itself.
So right now, whenever you check a block, you go through every transaction and you check that all its inputs exist, so it's spending from something that exists, but you do not check if the transaction itself exists, or at least you don't now because of what we'll discuss.
But with BIP30, you would have to do that.
You'd have to do an extra check for every transaction.
Like, hey, now that I've checked that all the inputs are valid, or whichever sequence we're going to do, does this transaction exist?

Aaron van Wirdum: 00:16:25

So that was the case in 2012, for a brief while, at least, after BIP30 was deployed.
And this sounds like it's an especially annoying or burdensome check because it's so unlikely that it's necessary, especially for all non-coinbase transactions.
But just technically...

Sjors Provoost: 00:16:44

It's completely unnecessary in the sense that no miner would be this stupid, but of course if you don't check then they would be.

Aaron van Wirdum: 00:16:50

You have to check, but it's burdensome.

Sjors Provoost: 00:16:52

But it wastes some resources.
I don't know how much, if it's like 1% or 10%, but it's annoying.

Aaron van Wirdum: 00:17:00

And also, in general, you want miners and all nodes to be able to check the validity of new blocks as soon as possible.

## Efficiency and BIP34: A Solution with Caveats

Sjors Provoost: 00:17:10

Yeah, so every second you can shave off, the checking time is better.
So, BIP34 was introduced, which made this process more efficient.

Aaron van Wirdum: 00:17:18

When was this?

Sjors Provoost: 00:17:20

Same year, just half a year later.
That is to say...

Aaron van Wirdum: 00:17:21

And was this introduced especially because, before the reason we just mentioned?
Yes.
Okay, so it was like a performance improvement.

Sjors Provoost: 00:17:29

I think so.
So, the little background is that BIP30 was a relatively simple software that could be deployed very quickly because they realized the problem and they wanted to fix it as quickly as possible so nobody would deliberately exploit it.
BIP34 was something that was deployed a bit more carefully, very much like the BIP9 style soft fork.
So there was some signaling involved, block version number went up and you had like so many percent of the miners had to signal it, et cetera, et cetera.
So BIP34 was a more thorough solution, but it was also deployed more carefully.
So what does BIP34 do?
Well, it makes sure that, well, that was the idea, that the coinbase transaction is unique by definition by adding the block height to it.
So every coinbase transaction must start with the block height.
And because it must start with the block height, it's going to be different than previous transactions which had a different block height, or previous coinbase transactions had a different block height, so you won't have the duplicates.
That is to say moving forward, you don't have to duplicate.

Aaron van Wirdum: 00:18:33

Yeah, okay, yeah, this makes sense.
This way every coinbase necessarily is unique, like every coinbase transaction necessarily is unique because it's in a new block that has new block height.
And therefore every transaction that is spent from that coin is also unique.
So now every transaction has to be unique.

Sjors Provoost: 00:17:52

Yes.

Aaron van Wirdum: 00:18:53
Okay, yeah, makes sense.
Good solution, Sjors, I like it.
Who came up with this?

Sjors Provoost: 00:18:58

I think it was...
I'm not sure.

Aaron van Wirdum: 00:19:02

Well, whoever came up with it, congratulations.
Thank you.

Sjors Provoost: 00:19:05

I think it was...

Aaron van Wirdum: 00:19:06

However, I guess there's another problem you're going to mention about this solution or not.

Sjors Provoost: 00:19:10

I think the original one was Peter Wuille and the second one was Russell O'Connor.

Aaron van Wirdum: 00:19:15

However, so I guess this is why we're making this episode.

Sjors Provoost: 00:19:18

No, Gavin Andresen.

Aaron van Wirdum: 00:19:19

Gavin Andresen.
I could have guessed.
Gavin, you messed up.

Sjors Provoost: 00:19:25

Well, I don't know.
I mean, it's just he's the author, so it doesn't mean that he came up with it.

Aaron van Wirdum: 00:19:30

It was a joke, but maybe it's a kind of a sensitive joke at this point in time.
Sjors, go on.
Because there is a problem.
It introduced a problem.

Sjors Provoost: 00:19:42

Yes.
Well, actually, it did not introduce a problem.
So just having this rule is fine.

Aaron van Wirdum: 00:19:49

Okay.
Good job, Gavin.


Sjors Provoost: 00:19:52

However...
So Gavin, whatever it was, he didn't do anything wrong.

Aaron van Wirdum: 00:19:55

Okay.

Sjors Provoost: 00:19:56

However, then in 2015, somebody tried to be smart and said, hey, we have this BIP34, which means that we don't need to check for BIP30 anymore.
We can make it faster.
So perhaps I said before in the episode, oh this was the reason the performance thing was the reason to introduce it.
Maybe not.
Maybe they did it because it was just a more elegant solution and it would prevent mistakes.
But then a couple of years later, somebody realized, hey, we can actually make this faster by not checking BIP30 anymore.
Because we know that the blocks must be unique, right?

Aaron van Wirdum: 00:20:31

Yeah, like I explained just now.
I immediately got it.
Why did it take these Bitcoin core developers so long, Sjors?

Sjors Provoost: 00:20:37

I don't know.
So, in 2015, that optimization was merged.
And well, then in 2018, so three years later, somebody realized, oh, oops!
that doesn't actually work.

## The Unforeseen Consequences of Optimizations

Aaron van Wirdum: 00:20:53

Wait, wait, wait, sorry, I lost the plot.
Where are we now?
What's the year?

Sjors Provoost: 00:20:57

Well, the year of the fix is 2018, but I guess the year of the realization was late 2017.
So somewhere, I think it was October 2017, but this wasn't documented, but it kind of follows.
Somebody realized, oh wait a minute, there are exceptions to this convenient rule.
Remember that the rule of BIP34 is that you put the height of the block at the beginning of the coinbase.
So block number one would have height number one, etc.
But that rule only applies starting with block, I don't know, 200,000 something.

Aaron van Wirdum: 00:21:36

It started being applied in 2012.

Sjors Provoost: 00:21:39

Yeah, and it started being applied from height number 220,000 or something like that.
So then the question, and so from there on this rule is correct, but the problem is, and that's what people realize, is that it doesn't apply earlier.
The rule wasn't active earlier.
So what is actually in those earlier coinbase transactions?
Might there be numbers in those earlier coinbase transactions, numbers that could represent a block height?
The answer is yes.
There were numbers in there.
So there were older coinbase transactions that had numbers in there that represented blocks that might occur in the future.

Aaron van Wirdum: 00:22:12

Okay, I know what you're saying, but you don't, The word represent is confusing here.
There were just numbers in there and they could be interpreted as blocks from the future.

Sjors Provoost: 00:22:21

Yeah, either it was a very smart miner that foresaw that this problem was going to happen.

Aaron van Wirdum: 00:22:25

For instance, there could have been an early miner who, for whatever reason, placed the number one million in the coinbase.

Sjors Provoost: 00:22:34

Yeah, so as the episode suggests, some miner put the number 1,983,702 in the coinbase.
They didn't actually put that number in there, they were probably just writing their name, and the name, if you map it into how a computer reads it, might have looked like a big number.

Aaron van Wirdum: 00:22:50

So, there was a block in, like, say 2009, that starts with the number 1,900,000 something.
So, by the time we actually get to block number 1,900,000, and that number has to be put in the coinbase, there's a risk that it was a pretty, that's not gonna happen, right?

Sjors Provoost: 00:23:16

Normally this would not happen,
But in theory, somebody would have to put the same number in it.

Aaron van Wirdum: 00:23:21

Yes.

Sjors Provoost: 00:23:22

And then could, if they wanted to, wouldn't happen accidentally, make the rest of the coinbase identical to that original transaction.

Aaron van Wirdum: 00:23:29

So, yeah, so it would just have to spend the same amount of...
Well, no, because there's 50 coins in the original coinbase.

Sjors Provoost: 00:23:37

Much more.
So, Merge looked at this specific transaction, and it turns out that that was a very lucky block.
So, not only did it get a 50 Bitcoin coinbase subsidy, which modern blocks don't get, it also got, I think, 50 or so BTC in fees.

Aaron van Wirdum: 00:23:55

That's good.

Sjors Provoost: 00:23:56

Yeah, so that's a very nice little block in the past.
So if you wanted to reproduce this, your coinbase transaction would have to create about 107 Bitcoin.
It would have to spend 107 Bitcoin.
That is only allowed if there is 107 Bitcoin worth of fees in that block.
So that's never going to happen accidentally.

Aaron van Wirdum: 00:24:15

The other thing that has to happen is that the attacker would have to actually probably pay these fees himself and then burn it in this block.

Sjors Provoost: 00:24:22

Yes, because he cannot send it to some arbitrary destination.
He has to reproduce the original coinbase transaction, which means that his 107 Bitcoin has to go to the original owner of that coinbase transaction.
And so maybe this miner, you know, was frozen and wakes up and decides that this is a fun joke because he can just get the 107 Bitcoin back after doing this.
But the other problem is it would have to be a non-SegWit block, because there was no SegWit back then, and SegWit adds something to the coinbase.
Well, you can't add that to the coinbase, because then it would be a different block.
So that means all the fees would have to be in non-SegWit transactions.
There's all sorts of problems with this attack.
One problem I can think about is that the next miner might be like, hey, there's a lot of fees in that original block, let me reorg it and mine it myself.
But anyway, so but this could be done.
And then you would have an identical transaction.

Aaron van Wirdum: 00:25:18

Hang on, hang on.
Maybe first finish your sentence.

Sjors Provoost: 00:25:21

So if the attacker did that, they would have an identical transaction.
And this is what people realized back in 2017, 2018.
That's bad because that is a BIP30 violation.
But we are not checking BIP30 anymore.
So we should check BIP30 again.
That's the solution, basically.
But it was a realization, like, oh, if we don't fix this, let me, you know, they would have to look at all the other numbers that were in all the transactions and see if this could happen earlier.

Aaron van Wirdum: 00:25:50

Okay, also, there could still be nodes that are checking BIP30, right, in theory?

Sjors Provoost: 00:25:54

Yeah, that could be very old nodes.

Aaron van Wirdum: 00:25:55

Which could be sort of its own problem.

Sjors Provoost: 00:25:57

All the nodes from before 2015 would check BIP-30, and they would not approve this walk if this attacker did that.

Aaron van Wirdum: 00:26:06

Let me sort of cut down, shortcut to, okay, so let's say an actual, let's say just, you know, the classical example, like a state-level attacker that does want to burn a hundred bitcoins just to fuck with Bitcoin.

Sjors Provoost: 00:26:20

It doesn't have to be a state level attacker like a hundred Bitcoin is there's a lot of money but it's not a state level money.

Aaron van Wirdum: 00:26:26

Well hang on we're talking in 20 years from now Sjors.
That's enough to buy North America.

Sjors Provoost: 00:26:31

Sure okay.

Aaron van Wirdum: 00:26:33

So a state level attacker wants to do this, what's the actual specific consequence?
Would he also have to do the re-org thing?

Sjors Provoost: 00:26:45

Well, okay.
So, the question is, first of all, you want to...

Aaron van Wirdum: 00:26:47

What's the actual risk?

Sjors Provoost: 00:26:48

Well, the first risk, and again, this has been fixed, but if it had not been fixed, the first risk is that they could violate BIP30.
And that means that if you had a node from before 2015, it would not accept the block.
New nodes would accept the block.
So you get a chain split.
And of course, you know, the majority of people would probably be on the modern nodes because you wouldn't be running 25 year old software, but it's still not healthy.

Aaron van Wirdum: 00:27:11

I mean, I'm pretty lazy with upgrading, to be honest.

Sjors Provoost: 00:27:13

Yeah, Well, your computer will force you to, probably.
The other thing is, then you could have shenanigans.
You could be talking about this reorg scenario.
I don't know if that's useful for the attacker or just shoots himself in the foot.
But there may be other weird things that you can do.
Like it's not part of the...
It shouldn't happen, basically.
So you can try and reason about it, but you just want to prevent that from happening.

Aaron van Wirdum: 00:27:39

Okay, so we've got 22 years more or less to do something about this problem.

Sjors Provoost: 00:27:44

Yeah, We didn't wait that long.

Aaron van Wirdum: 00:27:46

What are we going to do?
Oh, it's solved already?

Sjors Provoost: 00:27:48

Yes, in 2018, once they realized this problem was solved, and the solution is straightforward. As of block 1,983,702, we simply started checking BIP30 again.

## Averting a Potential Crisis: The Fix and Its Implications

Aaron van Wirdum: 00:28:01

Oh, so we're back to checking BIP30 with all these inefficiencies?

Sjors Provoost: 00:28:05

Yes.
We won't now, but we will check it from that block onward.

Aaron van Wirdum: 00:28:09

Oh okay. Yeah, that makes sense.

Sjors Provoost: 00:28:11

Which means we have 30 years to actually solve the problem but if we don't solve the problem we'll just check BIP30.

Aaron van Wirdum: 00:28:16

So, in 20 years, if you haven't upgraded your Bitcoin Core node...
Your Bitcoin Core node today, if left unupgraded, will still begin checking for BIP30 two decades from now?

Sjors Provoost: 00:28:31

That's right.

Aaron van Wirdum: 00:28:32

Oh, okay, interesting.

Sjors Provoost: 00:28:33

So, your node will likely do so unless you haven't upgraded since before 2018, right?

Aaron van Wirdum: 00:28:38

I'm not sure.
No, probably I did.
Yeah, I did upgrade since 2018.

Sjors Provoost: 00:28:41

There are so many security vulnerabilities in old Bitcoin nodes that this is the last of your problems.

Aaron van Wirdum: 00:28:47

I might be like three versions behind, but it's not that bad.

Sjors Provoost: 00:28:50

That's probably not too bad.
But it gets more exciting than that because 1,983,702 is not the only block where this happens, it was an earlier block where it didn't happen but it could have or it could not have.

Aaron van Wirdum: 00:29:06

Wait sorry, there was?

Sjors Provoost: 00:29:08

There is block 490,897.

Aaron van Wirdum: 00:29:11

Are we talking about the future or the past?

Sjors Provoost: 00:29:13

The past.

Aaron van Wirdum: 00:29:14

Okay, what about it?

Sjors Provoost: 00:29:15

So this block was another one of those numbers that if you look at the all the coinbase transactions and you just find what number is in there, there were a couple of numbers in there.
I think one number was so low like 200,000 it was before BIP34 was activated so it wasn't a problem because it was referring to something in the same era.
But the next number was 490,897, which was in October 2017.
And that block, if it wasn't for some lucky circumstances, could have already exposed this bug that we just talked about.
So we wouldn't have had 30 years.
No, we had two weeks, basically.
At least the people who discovered this issue discovered it about two weeks before that block.

Aaron van Wirdum: 00:30:01

Interesting.

Sjors Provoost: 00:30:01

So, this is like an asteroid heading toward Earth, and NASA says, "Oh, we found an asteroid coming toward Earth, but don't worry, it's going to miss us by at least the distance between here and the moon."
It's fine.
The only thing is we found out like two hours ago so if it had not missed us we would be dead and we would not have noticed it.
So this is one of those cases where yes, the bug isn't actually harmful, but if it had been harmful, there would have been only two weeks to deal with it.

Aaron van Wirdum: 00:30:26

Well, I mean, the bug could have been harmful if someone wants to exploit it.

Sjors Provoost: 00:30:31

No. So basically, by looking at the original transaction, they could see that it was not possible to exploit this.
And the reason is because that coinbase, yes, you could duplicate it, but it was already spent.
And so you then need to reproduce the transactions that spent the coinbase.
And that is impossible because one of those transactions was spending another coinbase.
And that other coinbase had a number in it, it's like 5 billion or some insane number.
And we can never get to block 5 billion, at least not in the current code, right?
Because it stops in 2106.

Aaron van Wirdum: 00:31:06

I see.

Sjors Provoost: 00:31:06

And then you have a hard fork.
So with a hard fork, you can fix everything basically though.
Anything after block 6 million or so is you don't have to worry about it.
So that was good, but it was a close call.

Aaron van Wirdum: 00:31:18

With a hard fork you can fix anything.
You can code shorts on that.

Sjors Provoost: 00:31:23

I'm not saying you're not introducing a new problem.

Aaron van Wirdum: 00:31:25

Are you pushing for a hard fork?

Sjors Provoost: 00:31:27

No, you can just wait until 2106.

Aaron van Wirdum: 00:31:30

Anyways, okay, we had a near miss in 2017.
That turned out to not be a real problem.
Now we got 20 years to either fix this problem or just ignore it because it's kind of already fixed.
Anything else?

Sjors Provoost: 00:31:46

Yes, so the fix was shipped in 2018.
It just basically says, okay, from this block, gonna check BIP30.
So anybody running a modern node doesn't have to worry too much.
Except on TestNet.,I think on TestNet, it's already checking BIP30 now.
But who cares about TestNet.?
Because TestNet had the same kind of problem.

Aaron van Wirdum: 00:32:11

Yeah.

Sjors Provoost: 00:32:12

And it was fixed in the same way.

Aaron van Wirdum: 00:32:14

Okay.

Sjors Provoost: 00:32:14

And I think in TestNet there was another block like that in block 2,200,000 or something like that.

Aaron van Wirdum: 00:32:21

I don't care about TestNet..

Sjors Provoost: 00:32:22

Testnet is already at block 2,500,000.
So I think it's already checking BIP30.

Aaron van Wirdum: 00:32:26

Okay.

Sjors Provoost: 00:32:27

And there's a little code comment saying like, "Oh, I'm sure somebody will fix it before then."

Aaron van Wirdum: 00:32:32

Oh, I was going to ask, are there others?
So we got 20 years, are there other solutions?
Like, is this just it, or do we have other ways out of this conundrum that we find ourselves in?

## Future Proofing Bitcoin Against Similar Issues

Sjors Provoost: 00:32:41

So ideally, you want to have something in every block that we know was not in those blocks before BIP34 activated.
And there's a bunch of candidates that were mentioned back in the day, but one candidate that I saw on Twitter, I think it was Calvin Kim that said it, but I don't know if he came up with it or heard it from somebody else.
And that is to basically make SegWit mandatory.
And why?
Right now...

Aaron van Wirdum: 00:33:14

SegWit for every transaction mandatory?

Sjors Provoost: 00:33:16

No, just say for every block.

Aaron van Wirdum: 00:33:18

For every coinbase transaction?

Sjors Provoost: 00:33:21

Yes.
So every block has to commit to SegWit, has to include the SegWit commitment.
The SegWit commitment is an `OP_RETURN` that refers to the tree of SegWit transactions.

Aaron van Wirdum: 00:33:30

Oh, wait, so are you just, oh.

Sjors Provoost: 00:33:33

So the transactions in the block don't have to be segwit.

Aaron van Wirdum: 00:33:36

Oh, so what you're saying is there could still be a block mine that has zero segwit transactions.
But as soon as there's one segwit transaction in a block, you need the segwit thing in the coinbase and therefore the transaction ID is different.

Sjors Provoost: 00:33:48

Yeah, and so right now, every time there is a SegWit block, yes, that's happened automatically.

Aaron van Wirdum: 00:33:53

Okay, has there been...

Sjors Provoost: 00:33:53

But empty blocks or blocks with no SegWit transactions do not commit to SegWit.
But definitely empty blocks don't.
However, they can, they just don't.
Because they don't have to.
So the change would be to say,

Aaron van Wirdum: 00:34:04

Let me ask this question real quick.
So, because I was going to ask, has there been any block mined that doesn't include any segwit transactions?
Since segwit is out and that would be empty blocks.

Sjors Provoost: 00:34:16

Yes.

Aaron van Wirdum: 00:34:16

Yeah.
Makes sense.
Okay, go on.

Sjors Provoost: 00:34:17


So basically, you know, the difficulty then would just be, okay, when you propose an empty block, which you have to do as a miner sometimes, very briefly, just make sure that it's a segwit block.
So that would be a fairly simple soft fork.
But there are other ideas out there.

Aaron van Wirdum: 00:34:35

It's probably still like, you know, in the sort of Puritan Bitcoin conservative, you know, which is a good philosophy, It's still kind of a cost to miners, which you're imposing on miners, like now they have to do something extra.
Like it might still be controversial, I don't know.
What do you think?

Sjors Provoost: 00:34:54

I don't know if it's a cost to miners because if they use Bitcoin Core to create the block templates, Bitcoin Core would just do it for them.

Aaron van Wirdum: 00:35:01

Well, the cost I'm referring to is you have to upgrade your Bitcoin Core node once in a while.
It's not backwards compatible is what I'm basically saying.

Sjors Provoost: 00:35:10

Not for the miners, no, but that's always true for Soft Forks.
Well, no, it's not always true for Soft Forks.
Generally soft forks are done in such a way that if you only mine standard transactions, then you're going to be fine.
But for this case, yes, miners would have to do something, just like they had in the first time it was introduced.
So yeah, it's not entirely innocent.

Aaron van Wirdum: 00:35:31

It seems to me like a very plausible or reasonable solution.
I'm just pointing out that even that might have some pushback.

Sjors Provoost: 00:35:37

Yeah, and the other solutions have this same, I think, have the same property, is that every miner would have to do it, or they might lose a block if they mine an empty block.
So I think another one was, okay, we just add the block height again, but we add it to a different field, like the lock time of the coinbase transaction.

Aaron van Wirdum: 00:35:54

Because lock time wasn't activated back in?

Sjors Provoost: 00:35:57

Lock time wasn't used.
As far as I know, again, you'd have to run a script and check.

Aaron van Wirdum: 00:36:01

Well, LockTime was introduced in 2015, right?

Sjors Provoost: 00:36:05

It's possible, but the field might, the field with the numbers were there.
They didn't have any meaning, right?
So you still have to check that they weren't used.
But that's easy.
I think this SegWit thing is the simplest one.
The other option is we can buy ourselves another 20 years or so to block 3,808,179.

Aaron van Wirdum: 00:36:27

How?

Sjors Provoost: 00:36:27

Well, we would have to very carefully study block 1,983,702.
Well not this block, but the original block that created it.
And that coinbase has been spent so it can already be recreated but you have to look at all the descendants.
So this thing was spent to like around 10 different addresses and those could spend and those could spend.
And if you can show that for every transaction descending from it, it was also using a coinbase transaction that cannot be duplicated, maybe you can prove that it, you know, you could write a proof that it can never happen, gives you another 20 years.
I think that's a stupid exercise compared to the simple soft fork.

Aaron van Wirdum: 00:37:04

Well, you didn't figure it out for this podcast, if that's the case or not?

Sjors Provoost: 00:37:07

I did ask it on Stack Overflow in a comment somewhere, but no, I did not.

Aaron van Wirdum: 00:37:11

Sure, do you even do?
What do you do for this podcast?


Sjors Provoost: 00:37:16

Nothing.
Moving on.
I did actually run a script to check that there are no `OP_RETURN` transactions before BIP324 activated.

Aaron van Wirdum: 00:37:26

Wait, sorry, can you repeat that just for me?

Sjors Provoost: 00:37:28

There were no `OP_RETURN` transactions in the coinbase before BIP324 activated.

Aaron van Wirdum: 00:37:33

You did actually check that?

Sjors Provoost: 00:37:35

Yes.

Aaron van Wirdum: 00:37:35

Okay.

Sjors Provoost: 00:37:35

Which means that you don't even have to commit to SegWit; you just have to put `OP_RETURN` in a coinbase transaction.
That will be the rule.
But of course, it's easier to just say SegWit.

Aaron van Wirdum: 00:37:46

Okay.
So far, I think we agree SegWit is the most reasonable, low effort kind of way of doing this.
I guess you could do Taproot as well, maybe, or no?
Does it make sense?
No, just SegWit.
I'm just thinking out loud.

Sjors Provoost: 00:38:00

You want to keep it simple?
So the funny thing is there was in 2019 a proposal...

Aaron van Wirdum: 00:38:04

I'm just thinking of soft forks that were introduced after 2015 to make me sound smart.
But yeah, SegWit is the obvious thing here.
Go on.

Sjors Provoost: 00:38:12

Yeah, so there was a great consensus cleanup proposal back in 2019 by Matt Corallo, BlueMatt, which contained a bunch of these very small fixes, kind of similar to this one, but not actually this one.

Aaron van Wirdum: 00:38:27

A fix for this specific problem?

Sjors Provoost: 00:38:29

Yeah, it was not in there.

Aaron van Wirdum: 00:38:31

So why do you even bring it up?

Sjors Provoost: 00:38:33

Because I was curious whether the great consensus cleanup would clean this up.

Aaron van Wirdum: 00:38:36

Right, and it doesn't.

Sjors Provoost: 00:38:38

But it would if you were to revive that proposal you should clean this up too.

Aaron van Wirdum: 00:38:42

Okay.

Sjors Provoost: 00:38:42

Because it also fixes the time warp attack and other things that we've discussed in other episodes.

Aaron van Wirdum: 00:38:47

Sure, yeah.
Okay.

Sjors Provoost: 00:38:51

That's all I have.

Aaron van Wirdum: 00:38:52

Yeah, well, I mean, sounds to me like SegWit is the easy way to go, and also...

Sjors Provoost: 00:38:57

We have a few decades to figure this out.

Aaron van Wirdum: 00:39:00

We can think about it a while.
All right, thanks, Sjors.

Sjors Provoost: 00:39:02

All right and thank you for listening to Bitcoin.

Aaron van Wirdum: 00:39:05

Explained.
