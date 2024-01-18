---
title: "The Block 1,983,702 Problem"
transcript_by: kouloumos via tstbtc v1.0.0 --needs-review
media: https://bitcoinexplainedpodcast.com/@nado/episodes/episode-87-the-block-1-983-702-problem-s7s3j
tags: []
speakers: ['Sjors Provoost', 'Aaron van Wirdum']
categories: ['podcast']
date: 2023-12-21
---
Speaker 0: 00:00:19

Live from Utrecht, this is Bitcoin Explained.
Hey Sjors.

Speaker 1: 00:00:24

So last time I read the sponsor and it was a complete disaster.
So this time you're going to do it.
As the song goes, Aaron reads ads, Aaron reads ads, Aaron reads ads.

Speaker 0: 00:00:36

Nice.
I forgot all about the jingle.
You haven't read any toots, what's it called?
Boost.
You haven't read any Boost for

Speaker 1: 00:00:46

a while.
What's going on with that?
No, we might do that later again.
Because we've gone this hyper-commercialized entity now with sponsors and stuff.

Speaker 0: 00:00:52

True, yeah.
Shors, do you know who our sponsor is?
It's CoinKite.
And they produce the cold card.
You know what I love about the cold card?
Besides the fact that they are our sponsor, Sjoerds.
I love that they're Bitcoin only.
I love that they're a hardware wallet.
It's secure.
It's for your Bitcoin.
It's to store your Bitcoin on.
How long is our read, Sjoerds?
Did I get there yet?
I think you're good.
The cold card is great, get it.
That's right.
Shors, today we're discussing a very niche bug that I had never heard of, but apparently there's a bug in the Bitcoin protocol.

Speaker 1: 00:01:31

Well, there was a bug in the Bitcoin protocol.

Speaker 0: 00:01:35

Right, but there's still a problem.

Speaker 1: 00:01:38

There was a bug, then there was no bug, then there was a bug, then there was no bug.
There's still a problem, but not a bug.

Speaker 0: 00:01:45

Right, okay, I see.
So there was a bug, now there's no bug, but there's still a problem which is not a bug.
Well, it's

Speaker 1: 00:01:52

kind of a bug, but it's not like a dangerous bug like the original thing.

Speaker 0: 00:01:55

Sounds pretty buggy.
Anyway, so it's called the 1,983,702 problem.
Did I say it right even?
The block 1,983,702 problem.

Speaker 1: 00:02:11

Yeah, that sounds good.
Or the block 198,3702 problem.

Speaker 0: 00:02:14

Right.
So this will be a problem in.

Speaker 1: 00:02:18

Yeah, there's another term you could use is the BIP34 does not imply BIP30 problem.

Speaker 0: 00:02:27

I don't know which one is worse.
They're both pretty bad.

Speaker 1: 00:02:30

Okay, cool.

Speaker 0: 00:02:31

So this will be a problem in block, well, again, 1,900,000 something.

Speaker 1: 00:02:38

Yeah, which is like a couple decades from now.

Speaker 0: 00:02:40

Yes, like 22 years from now, my sort of napkin math told me.

Speaker 1: 00:02:44

And to be clear, It's a problem, it's not like bad.

Speaker 0: 00:02:49

Right.
Okay, but it is something that needs to be solved eventually, in some way or another.

Speaker 1: 00:02:55

It's better if we solve it, yeah.
But it's not like the 2106 problem, which, like in the year 2106, the whole blockchain simply stops.
That's definitely a problem.

Speaker 0: 00:03:05

Right, this is not a problem that's going to require a consensus change.

Speaker 1: 00:03:09

No, ideally it would.
But not a hard fork.

Speaker 0: 00:03:12

Right, okay.
How did you find about it?
Like I said, I'd never heard of this.
Is this just something you, this is your hobby you look for very niche things that no one else has heard about?

Speaker 1: 00:03:23

Well we sometimes need to scrape the bottle of the barrel for episodes titles, but in this case I was trying to understand a bug in StratMV2, something I'm working on recently, and had something to do with the Coinbase transactions and whether or not it has a witness.
Turns out it does have a witness, or at least it can have a witness, which I didn't know, and That's why I kept banging my head against it.
But as I was trying to understand how the code works, I was reading the code comments and I came across this like almost full page story about this problem.

Speaker 0: 00:03:57

Okay, I'm gonna just call it the 1,900,000 problem because I don't wanna read it in full every time.
So the 1 million 900,000 problem, we'll start at the beginning.
So you mentioned there was a bug.
It all started with a bug, right?
And this has been a bug in Bitcoin since the beginning?

Speaker 1: 00:04:18

Yes.

Speaker 0: 00:04:19

Like it's an OG Satoshi bug?

Speaker 1: 00:04:21

Exactly, an OG Satoshi bug, which is that it was possible for two identical transactions to exist, or more than one basically, identical transactions to exist in sequence.

Speaker 0: 00:04:33

It was or wasn't?

Speaker 1: 00:04:35

It was possible.

Speaker 0: 00:04:35

It was possible.

Speaker 1: 00:04:37

And this was creating a problem because, well, when the transaction exists twice, then the original one essentially just disappears.
This has to do with how transactions work.

Speaker 0: 00:04:51

Yeah, let's halt here for a second.
So how do you get two identical transactions?

Speaker 1: 00:04:56

Same hash.
So the same hash means it's the same content.
So it's the same inputs, the same outputs.
And so typically you would expect this in a Coinbase transaction in the early days, because a Coinbase transaction doesn't have any inputs, or maybe it is the name of your pool, which would be the same if you were mining multiple blocks.
And then the outputs might be the address that you're paying yourself to, which might also be the same of your pool.
So if you mined in the early days two blocks to the same address and with the same pool name and you were like, I guess that,

Speaker 0: 00:05:30

yeah.
That makes sense.
So you're a pool in the early days, you have your Bitcoin address, one blah blah blah blah blah, because that was the early addresses, and you're mining new coins, so there's no inputs, and you just, these new 50 coins are sent to this one blah blah blah address.
And if that happens twice, if you say you mine two blocks in a row, it's going to be the exact same transaction.

Speaker 1: 00:05:54

Yeah, however, it also would have to be the same amount.
So this would be either a block with no transactions in it, so no fees.
So the Coinbase amount would be exactly 50 Bitcoin back in the day, or it would be coincidentally the exact same total fees.
The thing is, it only happened twice.

Speaker 0: 00:06:14

Especially In the early days, there were still a lot of transactions that didn't pay any fee, I guess.
Or there was a fixed fee for a while.

Speaker 1: 00:06:20

Probably a fixed fee.
So then maybe if you had...
I don't know.
I didn't look at those specific blocks.

Speaker 0: 00:06:24

Right.
Anyways, that is the most likely reason why that would happen.
Is it plausible that it could happen in any other circumstance to identical transactions?

Speaker 1: 00:06:36

Well, it could happen as a child of the coin.
So if the Coinbase transactions are identical, then you could make another transaction.
Basically, you could just replay another transaction from the past that spends that Coinbase transaction.
So the whole history of that Coinbase could be repeated.
So if somebody mines a block and then they send it to the Pirate Bay and they download a movie, you could redo all that history.

Speaker 0: 00:07:00

Yeah, It would just have to start from the same coinbase transaction that's already identical.
That's the only way you can get more identical transactions.
Exactly.
You start from there, yeah.

Speaker 1: 00:07:09

Or if you break SHA-256.

Speaker 0: 00:07:12

Which is also an episode we recorded at some point, I think.

Speaker 1: 00:07:17

I don't think anybody broke SHA-256, but we did talk about hashes in general.

Speaker 0: 00:07:21

We talked about what it means to break it, I think.
Anyways, I'm going on to tangents here.
Okay, so that's how you can get identical transaction IDs. And so you said it's possible, so why is it a bug if it's possible?
Because I thought you were gonna say it's impossible, but you said it's possible.
Why is it a bug then?

Speaker 1: 00:07:42

It's possible, it was possible to be exact, but the bug is that it creates problems for you, especially for you as the recipient of that transaction.

Speaker 0: 00:07:52

Right, so the miner in this case?

Speaker 1: 00:07:53

Yeah, so the miner mines, say, 50 Bitcoin and doesn't spend it, and then a week later, he mines 50 Bitcoin and also doesn't spend it.
Now he's like, oh, I've got 100 Bitcoins, how am I gonna spend this?
Oh, I'm gonna make a transaction and this transaction points to a previous transaction, that's what a transaction is to do.
So you would point to the original Coinbase transaction by its hash and then also by the position of the output in the Coinbase transaction.
But then the question is, which one do you mean?
And the Bitcoin Core software would simply look at the most recent one and would spend that.
And There was only one entry, so it would just be overwritten.
So the original coins would be gone.

Speaker 0: 00:08:42

Okay, you have to explain this, I think.
Why would the original...
So you say Bitcoin Core would just take the most recent one.
So why wouldn't the older one just also still exist for next time you want to spend?

Speaker 1: 00:08:53

Well, so Bitcoin Core keeps track of a list of outputs that exist.
Basically, the transaction hash and the identifier.
So if you add another one that is the same, it would just overwrite it.

Speaker 0: 00:09:05

Oh, sorry, do you just mean the UTXO set here?

Speaker 1: 00:09:08

Yeah, although I think at the time the UTXO set worked a little different than it does now.
But I think essentially it was the same thing.
It's just a list of coins that exist.
So it's a transaction hash and an identifier and whatever script you need to spend it.
And so if you were to create the transaction again, that would just be the same entry in the database.
So the database would think there's only one.

Speaker 0: 00:09:29

Okay, so not both transactions would be included in this database.
It would just be considered as the same transaction, so there's only one.
So then if you spend it, both are gone because they overlap.

Speaker 1: 00:09:41

Because you deleted one entry.
So this can lead to quite strange situations.
For example, let's say you mine a transaction once and then a couple blocks later you mine it again and then you spend it and so then it disappeared, right?
That's one way, but let's say you mine one transaction.
Sorry, yeah, let's do it again.
You mine one transaction, you mine a couple other blocks, and then you mine the transaction again.
Now, if there's a reorg, the blockchain undoes your most recent block, and then creates some other blocks.
That means that your transaction has now disappeared

Speaker 0: 00:10:27

from your

Speaker 1: 00:10:28

point of view.

Speaker 0: 00:10:29

Yeah, yeah, Yeah, okay, I get it.
So, oh yeah.
So, yeah, let me try to re-explain that, even though it was kind of clear to me, but maybe if I re-explain that might help one other person out there.
So, yeah, you're creating a blockchain, obviously, and then The first Coinbase transaction is included in block three, and then the next one is included in block seven.
But then there's another block seven, and that's the blockchain that the network goes with.
That becomes the longest chain.
So now your second Coinbase transaction is deleted from your UTXO set, basically, or your database, and it's not like the one before that is not like automatically restored either.
So now you lost both.

Speaker 1: 00:11:12

Yeah, you lost both.
However, somebody else who just starts up a new blockchain, a Bitcoin blockchain, will never see the original second block.
So they will only see the first block in which you do get the coinbase.
And as far as they're concerned, it's still there.
So now you have a consensus failure.
Because part of the network believes that a coin exists and the other does not and that will explode as soon as somebody tries to spend it.

Speaker 0: 00:11:33

Yeah, or to put it a little bit more accurately, maybe...
I mean, I think you're saying it technically accurately, but the more normie way of saying it is there's no consensus on who owns which coins.

Speaker 1: 00:11:44

Well, yeah, There's no consensus on who owns that, on whether that specific coin exists.

Speaker 0: 00:11:48

Not so much who owns it.
Well, that's a technical way of saying it, right?

Speaker 1: 00:11:51

Well, it's not about who owns it, it's that it exists or not.
So you can spend a coin that doesn't exist.
It's not about not satisfying the script, but it's just about the coin not existing.

Speaker 0: 00:12:01

Yeah, you're right actually.
In the real case, some nodes would actually think the coins don't exist at all anymore because yes, I see what you're saying.
Yeah, you're right.
Anyways, the important part is that the UTXO set or what, Sorry, why do you not call it the UTXO set?
Did you say back in the day was-

Speaker 1: 00:12:18

So this is the part I'm a little vague on, but initially the concept that we call the UTXO set, so a list of coins that exist, is not something that Satoshi invented as such.
I think we'll cover that again maybe in a future episode.
But this idea of having a database of which coin exists and you just add and remove coins from it, I think at the time it was not like that.
It was just a list of all transactions that were still relevant or something like that.
It was less efficient.
So, I think in 2018 or 2017, it was refactored into what we would now consider the UTXO set.

Speaker 0: 00:12:58

Okay.
So, let's just...
But this

Speaker 1: 00:13:00

less efficient implementation had the same problem.
The modern UTXO set would definitely have this problem.
And my understanding is the original one had two, even though it stored more data than we do now.

Speaker 0: 00:13:10

Anyways, the key point here being that the ownership records that every node holds would start to diverge.
And if that starts to happen, that is a consensus failure.
That you could get to a place where you try spending coins and it confirms on your end and it doesn't confirm on the other end and networks start to, it's chaos.
Like that's, so that's potentially, that was a potential actual risk with this OG Satoshi bug.

Speaker 1: 00:13:35

Yeah, and as far as I know, what did happen was there were two instances of these duplicate coinbases.
Basically miners losing 50 BTC.
But I don't think there were cases of also re-orcs on top of that that would have created this mess.
But maybe there was and nobody noticed it.
Because the mess would not have been...
Well, I think we would have noticed it now, yeah.

Speaker 0: 00:13:58

Probably right.
That would have been very unlucky as well.
Like, you've got to have an exact re-orc exactly on that block where this exact block happened.

Speaker 1: 00:14:07

Yeah, and because as far as we can tell it only happened twice, it might have happened more often in chains that never survived.

Speaker 0: 00:14:14

Well, no, then we would have the problem, right?

Speaker 1: 00:14:17

Well maybe we are

Speaker 0: 00:14:18

the surviving

Speaker 1: 00:14:19

chain where that didn't happen, but there may have been other chains where it did happen and it didn't survive.

Speaker 0: 00:14:23

Well we would have probably heard it then at some point, don't you think?
Because then there would have been nodes with these different transaction records, UTXO, set, whatever you want to

Speaker 1: 00:14:32

call it.
Yeah, but I mean, if this was long enough ago, maybe they just restarted the computer and just didn't care, but probably didn't happen.
Fair.
All

Speaker 0: 00:14:40

right.
So this was the, again, this was the OG Satoshi bug.
And This bug was fixed.

Speaker 1: 00:14:47

Exactly.
And this is where BIP30 comes in.
This was introduced in 2012.
What BIP30 does is very simple.
It says there shall never be two transactions with the same hash at the same time.

Speaker 0: 00:15:01

At the same time?

Speaker 1: 00:15:02

At the same time.
As in, if you create a transaction right now, it's not allowed to already exist in the UTXO set.

Speaker 0: 00:15:08

Okay, but it's just an invalid transaction.
So if the same thing would happen, if the miner would create this Coinbase transaction where he pays himself to the same address.
The Bitcoin network nodes, my node, your node, would just say, this is not valid, you just wasted your energy, we're going to wait for a valid block.
Exactly.
Right.

Speaker 1: 00:15:27

Now, let's say they do that, they make a coinbase,

Speaker 0: 00:15:32

then they spend it, then they can make

Speaker 1: 00:15:34

the same coinbase again.
That's no problem.
So BIP30 does allow that.
Right, okay.
So that was great and that worked.
The only problem is that this rule is a bit difficult to check, because it means that whenever you get a new block, for every transaction in that block, you have to make sure that it doesn't already exist, the transaction itself.
So right now, whenever you check a block, you go through every transaction and you check that all its inputs exist, so it's spending from something that exists, but you do not check if the transaction itself exists, or at least you don't now because of what we'll discuss.
But with Bit.30, you would have to do that.
You'd have to do an extra check for every transaction.
Like, hey, now that I've checked that all the inputs are valid, or whichever sequence we're going to do, does this transaction exist?

Speaker 0: 00:16:25

Right.
So that was the case in 2012, for a brief while, at least, after BIP30 was deployed.
And this sounds like it's an especially annoying or burdensome check because it's so unlikely that it's necessary, especially for all non-coinbase transactions.
But just technically...

Speaker 1: 00:16:44

It's completely unnecessary in the sense that no miner would be this stupid, but of course if you don't check then they would be.

Speaker 0: 00:16:50

You have to check, but it's burdensome.

Speaker 1: 00:16:52

But it wastes some resources.
I don't know how much, if it's like 1% or 10%, but it's annoying.

Speaker 0: 00:17:00

And also just in general, you want miners to be able to check the validity of new blocks or all nodes.

Speaker 1: 00:17:07

You want

Speaker 0: 00:17:07

them to be able to check for the as soon as possible.

Speaker 1: 00:17:10

Yeah, so every second you can shave off the checking time is better.
So, bit 34 was introduced, which made this process more efficient.

Speaker 0: 00:17:18

When was this?

Speaker 1: 00:17:18

Same year, just a half a year later.
That is to say...

Speaker 0: 00:17:21

And was this introduced especially because, before the reason we just mentioned?
Yes.
Okay, so it was like a performance improvement.

Speaker 1: 00:17:29

I think so.
So, the little background is that BIP30 was a relatively simple software that could be deployed very quickly because they realized the problem and they wanted to fix it as quickly as possible so nobody would deliberately exploit it.
BIP-34 was something that was deployed a bit more carefully, very much like the BIP9 style soft fork.
So there was some signaling involved, block version number went up and you had like so many percent of the miners had to signal it, et cetera, et cetera.
So BIP34 was a more thorough solution, but it was also deployed more carefully.
So what does BIP34 do?
Well, it makes sure that, well, that was the idea, that the Coinbase transaction is unique by definition by adding the block height to it.
So every Coinbase transaction must start with the block height.
And because it must start with the block height, it's going to be different than previous transactions which had a different block height, or previous Coinbase transactions had a different block height, so you won't have the duplicates.
That is to say moving forward, you don't have to duplicate.

Speaker 0: 00:18:33

Yeah, okay, yeah, this makes sense.
This way every Coinbase necessarily is unique, like every Coinbase transaction necessarily is unique because it's in a new block that has new block height.
And therefore every transaction that comes from, that's spent from that coin is also unique.
So now every transaction has to be unique.
Yes.
Okay, yeah, makes sense.
Yeah.
Good solution, Shorts, I like it.
Who came up with this?

Speaker 1: 00:18:58

I think it was...
I'm not sure.

Speaker 0: 00:19:02

Well, whoever came up with it, congratulations.
Thank you.

Speaker 1: 00:19:05

I think it was...

Speaker 0: 00:19:06

However, I guess there's another problem you're going to mention about this solution or not.

Speaker 1: 00:19:10

I think the original one was Pieter Wuyle and the second one was Russell O'Connor.

Speaker 0: 00:19:15

Right.
Okay.
However, so I guess this is why we're making

Speaker 1: 00:19:18

this episode.
No, Gavin Andresen.

Speaker 0: 00:19:19

Gavin Andresen.
I could have guessed.
Gavin, you messed up.

Speaker 1: 00:19:25

Well, I don't know.
I mean, it's just he's the author, so it doesn't mean that he came up

Speaker 0: 00:19:29

with it.
It was a joke, but maybe it's a kind of a sensitive joke at this point in time.
Sure, go on.
Because there is a problem.
It introduced a problem.

Speaker 1: 00:19:42

Yes.
Well, actually, it did not introduce a problem.
So just having this rule is fine.

Speaker 0: 00:19:49

Okay.
However...
Good job, Gavin.
However...

Speaker 1: 00:19:52

Oh. Exactly.
So Gavin, whatever it was, he didn't do anything wrong.

Speaker 0: 00:19:55

Okay.

Speaker 1: 00:19:56

However, then in 2015, somebody tried to be smart and said, hey, we have this BIP 34, which means that we don't need to check for BIP 30 anymore.
We can make it faster.
So perhaps I said before in the episode, oh this was the reason the performance thing was the reason to introduce it.
Maybe not.
Maybe they did it because it was just a more elegant solution and it would prevent mistakes.
But then a couple of years later, somebody realized, hey, we can actually make this faster by not checking BIP30 anymore.
Because we know that the blocks must be unique, right?

Speaker 0: 00:20:31

Yeah, like I explained just now.
I immediately got it.
Why did it take these Bitcore core developers so long, George?

Speaker 1: 00:20:37

I don't know.
So in 2015, that optimization was merged.
And Well, then in 2018, so three years later, somebody realized, oh, oops,

Speaker 0: 00:20:53

that doesn't actually work.
Wait, wait, wait, sorry, I lost the plot.
Where are we now?
What's the year?

Speaker 1: 00:20:57

Well, the year of the fix is 2018, but I guess the year of the realization was late 2017.
So somewhere, I think it was October 2017, but this wasn't documented, but it kind of follows.
Somebody realized, oh wait a minute, there are exceptions to this convenient rule.
Remember that the rule of BIP-34 is that you put the height of the block at the beginning of the coinbase.
So block number one would have height number one, etc.
But that rule only applies starting with block, I don't know, 200,000 something.

Speaker 0: 00:21:36

It started being applied in 2012.

Speaker 1: 00:21:39

Yeah, and it started being applied from height number 220,000 or something like that.
So then the question, and so from there on this rule is correct, but the problem is, and that's what people realize, is that it doesn't apply earlier.
The rule wasn't active earlier.
So what is actually in those earlier Coinbase transactions?
Might there be numbers in those earlier Coinbase transactions, numbers that could represent a block height?
The answer is yes.
There were numbers in there.
So there were older Coinbase transactions that had numbers in there that represented blocks that might occur in the future.

Speaker 0: 00:22:12

Okay, I know what you're saying, but you don't, The word represent is confusing here.
There were just numbers in there and they could be interpreted as blocks from the future.

Speaker 1: 00:22:21

Yeah, either it was a very smart miner that foresaw that this problem was going to happen.

Speaker 0: 00:22:25

Like let's say, like there could have been an early miner that for whatever reason put the number a million in the Coinbase.

Speaker 1: 00:22:34

Yeah, so as the episode suggests, some miner put the number 1,983,702 in the Coinbase.

Speaker 0: 00:22:41

Right.
They

Speaker 1: 00:22:42

didn't actually put that number in there, they were probably just writing their name, and the name, if you map it into how a computer reads it, might have looked like a big number.

Speaker 0: 00:22:50

Right.
So, that's...
Okay.
So, there was a block in, like, say 2009, that starts with the number 1,900,000 something.
So, by the time we actually get to block number 1,900,000, and that number has to be put in the Coinbase, there's a risk that it was a pretty, that's not gonna happen, right?
Normally this would not happen,

Speaker 1: 00:23:16

But in theory, somebody could put, would have to put the same number in it.

Speaker 0: 00:23:21

Yes.

Speaker 1: 00:23:22

And then could, if they wanted to, wouldn't happen accidentally, make the rest of the Coinbase identical to that original transaction.

Speaker 0: 00:23:29

Right.
So, yeah, so it would just have to spend the same amount of...
Well, no, because there's 50 coins in the original Coinbase.

Speaker 1: 00:23:37

Much more.
So, Merge looked at this specific transaction, and it turns out that that was a very lucky block.
So, not only did it get a 50 Bitcoin Coinbase subsidy, which modern blocks don't get, it also got, I think, 50 or so BTC in fees.

Speaker 0: 00:23:55

That's good.

Speaker 1: 00:23:56

Yeah, so that's a very nice little block in the past.
So if you wanted to reproduce this, your Coinbase transaction would have to create about 107 Bitcoin.
It would have to spend 107 Bitcoin.
That is only allowed if there is 107 Bitcoin worth of fees in that block.
So that's never going to happen accidentally.
The other thing that has to

Speaker 0: 00:24:16

happen is that the attacker would have to actually probably pay these fees himself and then burn it in this block.

Speaker 1: 00:24:22

Yes, because he cannot send it to some arbitrary destination.
He has to reproduce the original Coinbase transaction, which means that his 107 Bitcoin has to go to the original owner of that Coinbase transaction.
And so maybe this miner, you know, was frozen and wakes up and decides that this is a fun joke because he can just get the 107 Bitcoin back after doing this.
But the other problem is it would have to be a non-SegWit block, because there was no SegWit back then, and SegWit adds something to the Coinbase.
Well, you can't add that to the Coinbase, because then it would be a different block.
So that means all the fees would have to be in non-SegWit transactions.
There's all sorts of problems with this attack.

Speaker 0: 00:25:05

One problem

Speaker 1: 00:25:05

I can think about is that the next miner might be like, hey, there's a lot of fees in that original block, let me reorg it and mine it myself.
But anyway, so but this could be done.
And then you would have an identical transaction.

Speaker 0: 00:25:18

Hang on, hang on.
Maybe first finish your sentence.

Speaker 1: 00:25:21

So if the attacker did that, they would have an identical transaction.
And this is what people realized back in 2017, 2018.
That's bad because that is a BIP-30 violation.
But we are not checking BIP-30 anymore.
So we should check BIP-30 again.
That's the solution, basically.
But it was a realization, like, oh, if we don't fix this, let me, you know, they would have to look at all the other numbers that were in all the transactions and see if this could happen earlier.

Speaker 0: 00:25:50

Okay, also, there could still be nodes that are checking BIP-30, right, in theory?

Speaker 1: 00:25:54

Yeah, that could be very old nodes.

Speaker 0: 00:25:55

Which could be sort of its own problem.

Speaker 1: 00:25:57

All the nodes from before 2015 would check BIP-30, and they would not approve this walk if this attacker did that.

Speaker 0: 00:26:06

Let me sort of cut down, shortcut to, okay, so let's say an actual, let's say just, you know, the classical example, like a state-level attacker that does want to burn a hundred bitcoins just to fuck with Bitcoin.

Speaker 1: 00:26:20

It doesn't have to be a state level attacker like a hundred Bitcoin is there's a lot of money but it's not a state level money.

Speaker 0: 00:26:26

Well hang on we're talking in 20 years from now Sjoerds.
That's enough to buy North America.

Speaker 1: 00:26:31

Sure okay.

Speaker 0: 00:26:33

So a state level attacker wants to do this, what's the actual specific consequence?
Would he also have to do the re-org thing?

Speaker 1: 00:26:45

Well, okay.
So, the question is, first of all, you want to...

Speaker 0: 00:26:47

What's the actual risk?

Speaker 1: 00:26:48

Well, the first risk, and again, this has been fixed, but if it had not been fixed, the first risk is that they could violate bit 30.
And that means that if you had a node from before 2015, it would not accept the block.
New nodes would accept the block.
So you get a chain split.
And of course, you know, the majority of people would probably be on the modern nodes because you wouldn't be running 25 year old software, but it's still not healthy.

Speaker 0: 00:27:11

I mean, I'm pretty lazy with upgrading, to be honest.

Speaker 1: 00:27:13

Yeah, Well, your computer will force you to, probably.
The other thing is, then you could have shenanigans.
You could be talking about this reorg scenario.
I don't know if that's useful for the attacker or just shoots himself in the foot.
But there may be other weird things that you can do.
Like it's not part of the...
It shouldn't happen, basically.
So you can try and reason about it, but you just want to prevent that from happening.

Speaker 0: 00:27:39

Okay, so we've got 22 years more or less to do something about this problem.

Speaker 1: 00:27:44

Yeah, We didn't wait that long.

Speaker 0: 00:27:46

What are we going to do?
Oh, it's solved already?

Speaker 1: 00:27:48

Yes, in 2018, once they realized this problem was solved, and the solution is very simple, as of block 1,983,702, we just checked BIP-30 again.

Speaker 0: 00:28:01

Oh, we're back to checking BIP-30 with all these inefficiencies?

Speaker 1: 00:28:05

Yes.
We won't now, but we will check it from that block onward.

Speaker 0: 00:28:09

Oh okay yeah that makes sense.

Speaker 1: 00:28:11

Which means we have 30 years to actually solve the problem but if we don't solve the problem we'll just check BIP30.

Speaker 0: 00:28:16

Right okay so in 20 years, so my Bitcoin Core node, well, I haven't upgraded my...
Your Bitcoin Core node today, if you don't upgrade it, will still start checking for BIP-30 in 20 years from now?

Speaker 1: 00:28:31

That's right.

Speaker 0: 00:28:32

Oh, okay, interesting.

Speaker 1: 00:28:33

So, will your node probably, unless you didn't upgrade before 2018?

Speaker 0: 00:28:38

I'm not sure.
No, probably I did.
Yeah, no, I did upgrade since 2018.
There are

Speaker 1: 00:28:42

so many security vulnerabilities in old Bitcoin nodes that this is the last of your problems.

Speaker 0: 00:28:47

I might be like three versions behind, but not that bad.

Speaker 1: 00:28:50

That's probably not too bad.
But it gets more exciting than that because 1,983,702 is not the only block where this happens, it was an earlier block where it didn't happen but it could have or it could not have.

Speaker 0: 00:29:06

Wait sorry, there was?

Speaker 1: 00:29:08

There is block 490,897.

Speaker 0: 00:29:11

Are we talking about the future or the past?

Speaker 1: 00:29:13

The past.

Speaker 0: 00:29:14

Okay, what about it?

Speaker 1: 00:29:15

So this block was another one of those numbers that if you look at the all the coinbase transactions and you just find what number is in there, there were a couple of numbers in there.
I think one number was so low like 200,000 it was before BIP34 was activated so it wasn't a problem because it was referring to something in the same era.
But the next number was 490,897, which was in October 2017.
And that block, if it wasn't for some lucky circumstances, could have already exposed this bug that we just talked about.
So we wouldn't have had 30 years.
No, we had two weeks, basically.
At least the people who discovered this issue discovered it about two weeks before that block.

Speaker 0: 00:30:01

Interesting.

Speaker 1: 00:30:01

So this is like the asteroid coming towards the earth and NASA says oh we found an asteroid coming towards the earth but don't worry it's going to miss us by like at least a distance between here and the moon.
It's fine.
The only thing is we found out like two hours ago so if it had not missed us we would be dead and we would not have noticed it.

Speaker 0: 00:30:17

Right, right, right.

Speaker 1: 00:30:18

So this is one of those cases where yes, the bug isn't actually harmful, but if it had been harmful, there would have been only two weeks to deal with it.

Speaker 0: 00:30:26

Well, I mean, the bug could have been harmful if someone wants to exploit it.

Speaker 1: 00:30:31

No. So basically, by looking at the original transaction, they could see that it was not possible to exploit this.
And the reason is because that Coinbase, yes, you could duplicate it, but it was already spent.
And so you then need to reproduce the transactions that spent the Coinbase.
And that is impossible because one of those transactions was spending another Coinbase.
And that other Coinbase had a number in it, it's like 5 billion or some insane number.
And we can never get to block 5 billion, at least not in the current code, right?
Because it stops in 2106.

Speaker 0: 00:31:06

I see.

Speaker 1: 00:31:06

And then you have a hard fork.
So with a hard fork, you can fix everything basically though.
Anything after block 6 million or so is you don't have to worry about it.
So that was good, but it was a close call.

Speaker 0: 00:31:18

With a hard fork you can fix anything.
You can code shorts on that.

Speaker 1: 00:31:23

I'm not saying you're not introducing

Speaker 0: 00:31:24

a new problem.
Are you pushing for a hard fork?

Speaker 1: 00:31:27

No, you can just wait until 2006.
Right.
2106.

Speaker 0: 00:31:30

Anyways, okay, we had a near miss in 2017.
That turned out to not be a real problem.
Now we got 20 years to either fix this problem or just ignore it because it's kind of already fixed.
Anything else?

Speaker 1: 00:31:46

Yes, so the fix was shipped in 2018.
It just basically says, okay, from this block, gonna check bit 30.
So anybody running a modern node doesn't have to worry too much.
Except on testnet, I think on testnet, I think on testnet, it's already checking bit 30 now.
But who cares about TestNet?
Because TestNet had the same kind of problem.

Speaker 0: 00:32:11

Yeah.

Speaker 1: 00:32:12

And it was fixed in the same way.

Speaker 0: 00:32:14

Okay.

Speaker 1: 00:32:14

And I think in TestNet there was another block like that in block 2,200,000 or something like that.

Speaker 0: 00:32:21

I don't care about testnet.

Speaker 1: 00:32:22

Testnet is already at block 2,500,000.
So I think it's already checking pip 30.

Speaker 0: 00:32:26

Okay.

Speaker 1: 00:32:27

And there's a little code comment saying like, oh, I'm sure somebody will fix it before then.

Speaker 0: 00:32:32

Oh, I was going to ask, are there others?
So we got 20 years, are there other solutions?
Like, is this just it, or do we have other ways out of this conundrum that we find ourselves in?

Speaker 1: 00:32:41

So ideally, you want to have something in every block that we know was not in those blocks before BIP34 activated.
And there's a bunch of candidates that were mentioned back in the day, but one candidate that I saw on Twitter, I think it was Kelvin Kim that said it, but I don't know if he came up with it or heard it from somebody else.
And that is to basically make SegWit mandatory.
And why?
Right now...

Speaker 0: 00:33:11

Wait, wait.

Speaker 1: 00:33:13

SegWit commitments...

Speaker 0: 00:33:14

SegWit for every transaction mandatory?

Speaker 1: 00:33:16

No, just say for every block.

Speaker 0: 00:33:18

For every Coinbase transaction?
Yes.
Yeah, okay, that makes sense.

Speaker 1: 00:33:21

So every block has to commit to SegWit, has to include the SegWit commitment.
The SegWit commitment is an up-return that refers to the tree of SegWit transactions.

Speaker 0: 00:33:30

Oh, wait, so are you just, oh.

Speaker 1: 00:33:33

So the transactions in the block don't have to be segwit.

Speaker 0: 00:33:36

Oh, so what you're saying is there could still be a block mine that has zero segwit transactions.
But as soon as there's one segwit transaction in a block, you need the segwit thing in the Coinbase and therefore the transaction ID is different.

Speaker 1: 00:33:48

Yeah, and so right now, every time there is a SegWit block, yes, that's happened automatically.

Speaker 0: 00:33:53

Okay, has there

Speaker 1: 00:33:53

been...
But empty blocks or blocks with no SegWit transactions do not commit to SegWit.
But definitely empty blocks don't.
However, they can, they just don't.
Because they don't have to.
So the change would be to say,

Speaker 0: 00:34:04

okay, you have to...
Let me ask this question real quick.
So, because I was going to ask, has there been any block mined that doesn't include any segwit transactions?

Speaker 1: 00:34:14

Since

Speaker 0: 00:34:14

segwit is out and that would be empty blocks.

Speaker 1: 00:34:16

Yes.

Speaker 0: 00:34:16

Right.
Yeah.
Makes sense.

Speaker 1: 00:34:17

Okay, go on.
So basically, you know, the difficulty then would just be, okay, when you propose an empty block, which you have to do as a miner sometimes, very briefly, just make sure that it's a segwit block.
So that would be a fairly simple soft fork.

Speaker 0: 00:34:32

But

Speaker 1: 00:34:32

there are other ideas out there.

Speaker 0: 00:34:35

It's probably still like, you know, in the sort of Puritan Bitcoin conservative, you know, which is a good philosophy, It's still kind of a cost to miners, which you're imposing on miners, like now they have to do something extra.
Like it might still be controversial, I don't know.
What do you think?

Speaker 1: 00:34:54

I don't know if it's a cost to miners because if they use Bitcoin Core to create the block templates, Bitcoin Core would just do it for them.

Speaker 0: 00:35:01

Well, the cost I'm referring to is you have to upgrade your Bitcoin Core node once in a while.
It's not backwards compatible is what I'm basically saying.

Speaker 1: 00:35:10

Not for the miners, no, but that's always true for Soft Forks.
Well, no, it's not always true for Soft Forks.
Generally soft forks are done in such a way that if you only mine standard transactions, then you're going to be fine.
But for this case, yes, miners would have to do something, just like they had in the first time it was introduced.
So yeah, it's not entirely innocent.

Speaker 0: 00:35:31

It seems to me like a very plausible or reasonable solution.
I'm just pointing out that even that might have some pushback.

Speaker 1: 00:35:37

Yeah, and the other solutions have this same, I think, have the same property, is that every miner would have to do it, or they might lose a block if they mine an empty block.

Speaker 0: 00:35:44

Right.

Speaker 1: 00:35:45

So I think another one was, okay, we just add the block height again, but we add it to a different field, like the lock time of the Coinbase transaction.

Speaker 0: 00:35:54

Because lock time wasn't activated back in?

Speaker 1: 00:35:57

Lock time wasn't used.
As far as I know, again, you'd have to run a script and check.

Speaker 0: 00:36:01

Well, LockTime was introduced in 2015, right?

Speaker 1: 00:36:05

It's possible, but the field might, the field with the numbers were there.
They didn't have any meaning, right?
So you still have to check that they weren't used.
But that's easy.
I think this SegWit thing is the simplest one.
The other option is we can buy ourselves another 20 years or so to block 3,808,179.

Speaker 0: 00:36:27

How?

Speaker 1: 00:36:27

Well, we would have to very carefully study block 1,983,702.
Well not this block, but the original block that created it.
And that Coinbase has been spent so it can already be recreated but you have to look at all the descendants.
So this thing was spent to like around 10 different addresses and those could spend and those could spend.
And if you can show that for every transaction descending from it, it was also using a Coinbase transaction that cannot be duplicated, maybe you can prove that it, you know, you could write a proof that it can never happen, gives you another 20 years.
I think that's a stupid exercise compared to the simple software.

Speaker 0: 00:37:04

Well, you didn't figure it out for this podcast, if that's the case or not?

Speaker 1: 00:37:07

I did ask it on Stack Overflow in a comment somewhere, but no, I did not.

Speaker 0: 00:37:11

Sure, do you even do?
What do you do for this podcast?
Nothing.

Speaker 1: 00:37:16

Moving on.
I did actually run a script to check that there are no upreturn transactions before BIP324 activated.

Speaker 0: 00:37:26

Wait, sorry, can you repeat that just for me?

Speaker 1: 00:37:28

There were no upreturn transactions in the Coinbase before BIP324 activated.

Speaker 0: 00:37:33

You did actually check that?

Speaker 1: 00:37:35

Yes.

Speaker 0: 00:37:35

Okay.

Speaker 1: 00:37:35

Which means that you don't even have to commit to SegWit, you just have to put Upperturn in a Coinbase transaction.
That will be the rule.
But of course, it's easier to just say SegWit.

Speaker 0: 00:37:46

Okay.
So far, I think we agree SegWit is the most reasonable, low effort kind of way of doing this.
I guess you could do Taproot as well, maybe, or no?
Does it make sense?
No, just SegWit.
Taproot is just a subset.
I'm just thinking out loud.

Speaker 1: 00:38:00

You want to keep it simple?
So the funny thing is there was in 2019 a proposal...
I'm just

Speaker 0: 00:38:04

thinking of soft forks that were introduced after 2015 to make me sound smart.
But yeah, SegWit is the obvious thing here.
Go on.

Speaker 1: 00:38:12

Yeah, so there was a great consensus cleanup proposal back in 2019 by Matt Corallo, Blue Matt, which contained a bunch of these very small fixes, kind of similar to this one, but not actually this one.

Speaker 0: 00:38:27

A fix for this specific problem?

Speaker 1: 00:38:29

Yeah, it was not in there.
So why

Speaker 0: 00:38:32

do you even bring it up?

Speaker 1: 00:38:33

Because I was curious whether the great consensus cleanup

Speaker 0: 00:38:35

would

Speaker 1: 00:38:36

clean this up.

Speaker 0: 00:38:36

Right, and it doesn't.

Speaker 1: 00:38:38

But it would if you were to revive that proposal you should clean this up too.

Speaker 0: 00:38:42

Okay.

Speaker 1: 00:38:42

Because it also fixes the time warp attack and other things that we've discussed in other episodes.

Speaker 0: 00:38:47

Sure, yeah.
Okay.

Speaker 1: 00:38:51

That's all I have.

Speaker 0: 00:38:52

Yeah, well, I mean, sounds to me like SegWit is the easy way to go, and also...

Speaker 1: 00:38:57

We have a few decades

Speaker 0: 00:38:58

to figure this out.
We can think about it a while.
All right, thanks, Jors.

Speaker 1: 00:39:02

All right, and thank you for listening to Bitcoin.
Explained.
