---
title: AssumeUTXO
transcript_by: varmur via review.btctranscripts.com
media: https://www.youtube.com/watch?v=knBHvzKsIOY
tags:
  - assumeutxo
  - bitcoin-core
speakers:
  - James O'Beirne
date: 2020-02-13
episode: 4
summary: Next in the studio, we caught James O'Beirne, who until recently was a co-worker of ours at Chaincode. We talked to James about his experience at the Chaincode residency, his most recent project AssumeUTXO and how he champions and effects change in Bitcoin Core.
aliases:
  - /chaincode-labs/chaincode-podcast/assumeutxo/
---
James O'Beirne: 00:00:00

Bitcoin is a very complex piece of software and it's very difficult to review for correctness.
Even people who are really experienced with the code base still have a really hard time determining, in some cases, whether a change is safe or not.

## Introduction

John Newberry: 00:00:25

Hi Jonas.
Hi Caralie.

Caralie: 00:00:27

Hi guys.

John Newberry: 00:00:29

We have Caralie in the studio.
Caralie is our producer and she's been helping us with the episodes.

Caralie: 00:00:34

Yeah, it's been a lot of fun.
It's been really great working with you guys and getting to meet all of the wonderful guests that you guys have had on.

John Newberry: 00:00:41

Great to have you here.

Caralie: 00:00:42

Thank you.
Who do you guys have up next?

John Newberry: 00:00:46

Well, this week we talked to James O'Beirne who until very recently was a co-worker here at Chaincode Labs.
I first met James a couple of years ago, back in 2017, 2018 at a conference in Stanford and then a meetup in San Francisco.
It was obvious from when I met him that he was very passionate about Bitcoin and enthusiastic.
He was so enthusiastic I think he applied the very first day that we opened applications for the residency in 2018.
So he came to the residency in 2018 and then went on to join Chaincode and he's been a friend and a co-worker for the last two years.

Caralie: 00:01:22

I love that.
What did you guys talk about?

Adam Jonas: 00:01:24

We talked a little bit about how he decides the projects that he works on, and his most recent project which is `AssumeUTXO`.
Then we talked a little bit about how he advocates and affects changes in Bitcoin Core.

John Newberry: 00:01:36

We really love talking to James and we hope you enjoy the episode.
We'll be back at the end.

Hi James.
Welcome to the podcast.

James O'Beirne: 00:01:50

Thanks, it's great to be here in our conference room (laughter).

Adam Jonas: 00:01:55

Well thanks for making the trip.
We're going to talk about a few different things today.
We're going to talk about what you're currently working on.
We're going to talk about the vision quest that brought you here today.
So maybe why don't you go back to not the beginning, but the start of the new beginning, to Chaincode.

## 2018 residency

James O'Beirne: 00:02:13

Sure thing.
I came to Chaincode in the winter of 2018, I think it was February 1st.
I had been talking to John previously, because we had collaborated to some extent on a few things in the repo, and I had met him in California at a conference out there and had told him that I'd like to apply to the [residency](https://medium.com/@ChaincodeLabs/chaincode-residency-2018-26cd8a65d5f7).
So he encouraged me to do so, I did that, and somehow got in.
So I showed up in New York during the winter of 2018 and started the residency, which was a lot of fun.
Through that, got acquainted with Chaincode and that led to a full-time position.

Adam Jonas: 00:03:10

That was also the crypto winter of 2018, I believe.

James O'Beirne: 00:03:13

Correct.

John Newberry: 00:03:13

Oh yeah, we were coming off that hot 2017 bull run.

James O'Beirne: 00:03:19

Yeah, yeah, mixed emotions.
But it was a really great time.
The residents were all awesome, and the sessions that we had were really interesting because it was a smallish group, it was maybe 15 total, I think, maybe a bit more than that.

John Newberry: 00:03:41

It was two sessions of two weeks and six or seven in each, I think.

James O'Beirne: 00:03:47

Oh, is it that small in terms of people there?
Okay.

John Newberry: 00:03:49

Pretty small.
Yeah.
Select, exclusive.

James O'Beirne: 00:03:54

Yeah, no, everybody there was great, and so we had some really great sessions.
Very interactive, very Socratic.
It was a lot, it was intense.
First and foremost, I think of myself as a carpenter, but instead of wood, it's software.
So at a certain point, I kind of tuned out and was just ready to start coding, but it was awesome.

One of the things that I think about a lot when working on Bitcoin is that it's really easy to get hung up on how many smart people are here and you can get in your own head about like what can I actually contribute?
It's a really easy rabbit hole to spiral down because there are incredibly talented people working on Bitcoin.
But what you've got to realize is that there are different kinds of smart, everybody has different skill sets.
I kind of like putting one foot in front of the other, and having consistent engineering hygiene, and trying lots of things and iterating quickly.
That makes me really good at some things, it makes me really not good at other things.
I think what's cool about development of Bitcoin is that there is actually space for a lot of different approaches.

## Choosing what to work on

Adam Jonas: 00:05:21

As a carpenter starts to think about what he's going to build, how do you decide what to work on and what kind of angle you're going to take on a project like this?

James O'Beirne: 00:05:33

I think before you know anything, you just have to jump in and start doing things.
I don't mean necessarily opening PRs and things of that nature, but I think cloning the source code and then playing around with it, making modifications to it, is really important just to get to know the code base, watching the way that reviews work.
Fundamentally, it's all about where the bottlenecks are, whether that's in terms of a feature set, or the performance, or resource usage or vulnerabilities.
Everything is kind of like looking at what the lowest hanging fruit is and then going from there.

So I came in not necessarily knowing what I was going to work on.
I came in having made a change to the LevelDB wrapper that we use and having worked on the test suite a little bit, but I think there were a whole lot of dimensions of Bitcoin Core that I just wasn't familiar with.
I think the first thing I started to work on was the fork detection framework.

## Fork detection framework

James O'Beirne: 00:06:55

The idea there is that we want to have some kind of logging, or alert system, if Bitcoin sees a heavy work fork that's been going on and hasn't been resolved because that means that your node might have been partitioned somehow.
Nominally we have ways of doing this, but they're kind of broken, and they're still kind of broken.
That has to do with balancing considerations around DoS and the way that we do the bookkeeping around header validity.
So anyway, I had started to work on that but that was kind of stalling and it didn't look like it was going anywhere.
Frankly, it's a cool project and it was a good way of getting introduced to Bitcoin Core in a formal way, but I think the marginal utility of that is low.
So I started thinking about what really mattered to me, in terms of where did I think the important work was in Core.

## Initial block download (IBD)

James O'Beirne: 00:08:06

That naturally led to the duration of the initial block download because I think that's kind of a sticking point for a lot of people who want to participate in consensus, and want to run a node that they transact with, because that's really the only way that you reify the rules that you're using Bitcoin under.
So it's an important thing to...

Adam Jonas: 00:08:31

I'd like to challenge that a little bit.

James O'Beirne: 00:08:33

Sure.

Adam Jonas: 00:08:34

Don't you think if someone has set up the hardware or just gotten their ducks in a row to actually participate, that they're just going to wait for whatever it takes to do the initial block download?
The speed of which... I mean I hear the phone instance, and I hear just usage or outdated hardware, or whatever the case may be, we want to enfranchise as many people as possible.
But if you've set it up and you've started the process, can't you just wait a little bit longer?
Is that really an area of optimization that we need?

James O'Beirne: 00:09:11

Yeah, you certainly can, and that's the right question to be asking.
In my experience, there are a lot of people who are on the margin there.
For example, I have a friend who is a very diligent user of Bitcoin and he's very privacy conscious, but every time he's gone to download the chain and use Bitcoin QT, he gets kind of hamstrung and he's stuck waiting days and he's turning his laptop on and off.
So subsequently, that kind of user is pushed towards using something like say Electrum, which has a different security model than Bitcoin QT.
So yeah, I think there are a lot of hobbyist users out there who are going to buy, say, a Raspberry Pi and set it up and wait the four or five days or whatever that it takes to sync.

But I think appealing to those users who are maybe casual users of Bitcoin or maybe more than that, but they're deciding between getting the whole blockchain or using Bitcoin under a different security model, and that's kind of on the margin.
So I think those are important people to go after.

The other thing to keep in mind is that the blockchain is just going to keep growing.
There's linear growth there, and I think there has to come a point where we say, okay, we have to stem this somehow, because if we want this to keep going on forever, IBD time can't scale with forever.
So we needed to truncate somehow.

John Newberry: 00:11:01

Okay, so let's talk about [IBD, initial block download](https://btcinformation.org/en/glossary/initial-block-download).
What is a node doing when you switch it on for the first time?

James O'Beirne: 00:11:10

Well, I think the first thing it does is check to see if it's got any data, and if it doesn't, then it tries to find peers.
If it doesn't know any peers right off the bat, it'll consult these [DNS seeds](https://stackoverflow.com/questions/41673073/how-does-the-bitcoin-client-determine-the-first-ip-address-to-connect) that are run by various people and it'll get a random set of peers.

It'll connect to those peers and it'll ask them, I think, what the best block that they know about is.
Is that right?
So in doing that, your node then gets the headers chain, which is basically an abbreviated version of the blockchain.
That's the vital information, the vital metadata about blocks without the transaction data itself.
Once it has all that, it figures out what the most work valid headers chain is, and then starts the initial block download process, which is where it's actually obtaining the data in the blocks, the full blocks themselves, reassembling the blockchain, which basically amounts to building a few indexes, the most important of which is the [UTXO set](https://btcinformation.org/en/glossary/unspent-transaction-output), which is its own data structure.

## UTXO set

James O'Beirne: 00:12:33

At the end of all that, you end up with this set of unspent coins, which you can then use to decide whether an incoming block is valid or invalid.
That whole process takes, at the moment, anywhere from four hours, if you've got a really good internet connection and really good hardware, to an unbounded amount of time, depending on your hardware and bandwidth.

John Newberry: 00:13:00

Okay, so you start by getting this headers chain, which is the block headers, and that contains the Proof-of-Work, so just from that small amount of data, 80 bytes per block, you can figure out which chain has the most work.
At this point you're not validating transactions, so you don't know whether it's a valid chain, but you know that it's got the most work.

Then you go back and download the blocks.
As you're downloading blocks, you're validating them and building this UTXO set, which is a set of coins, a set of unspent transactions.
So that takes a long time.
It takes a long time to download that data.
There's IO there because you're writing to disk, and there's computation there because you're validating the signatures.
The blockchain is getting bigger all the time, so if you do this in a year's time, it will take longer.
So what are some of the strategies that we've had so far before us?
We're going to talk about `AssumeUTXO`, but before we get there, what are some of the strategies that we've had to make this take less time?

## Parallelized signature validation

James O'Beirne: 00:14:06

Yep.
So the first I'm aware of, and correct me if there's something we did before this, but the signature verification that we have to do for each block, you can to some extent [parallelize](https://github.com/bitcoin/bitcoin/pull/2060) that.
So one of the things that we do is we have a thread pool of signature verification processes, so that gets parallelized.

## `assumevalid`

James O'Beirne: 00:14:36

Another thing that we do is called [`assumevalid`](https://bitcoincore.org/en/2017/03/08/release-0.14.0/#assumed-valid-blocks), and I actually didn't know about this until I came to the Chaincode residency.
I was taken aback when I learned about it, as I think most people are and should be because it's a very unintuitive idea, and it should kind of raise the hair on your back if you're a dyed in the wool Bitcoiner, and you're like, hey, wait a second, how does this thing actually work?

So what `assumevalid` does is there is a block hash hard-coded in the source code.
If your Bitcoin client sees a headers chain that contains that block hash, it will assume that all of the signatures in all of the blocks underneath the block designated by that hash are valid.
So it'll skip signature verification.
Traditionally signature verification is the most costly part of initial block downloads, so that saves you quite a bit of time.

So the natural question is, how does this not somehow dilute the security model of Bitcoin?
You're trusting the developers, I think would be the catchphrase.
The reality is that this works because... Bitcoin source code is the trust model, right?
That's what you're trusting when you run Bitcoin, the source code that your binary is built from.

Basically, when you're evaluating a change to Bitcoin, that's obviously going to affect consensus in one way or another, that change could potentially be doing anything.
It could be short-circuiting some kind of validation that might permit the spend of a certain coin that doesn't exist, it could be doing any number of things.
All `assumevalid` does is it makes part of the review process a sort of commonly agreed upon attestation that the software has previously validated this particular chain.
It doesn't really dictate what the right chain is, because let's say there's a massive reorg where somebody secretly forked, started working on a fork at some point before that `assumevalid` mark, that alternate fictional chain could still potentially overtake the chain that's been deemed `assumevalid`.
It's just basically Bitcoin users coming together and saying, hey, look, yeah, this is the chain that we've all previously validated, we know it's valid, and it gets reviewed like any other piece of the code.

### Different than checkpoints

John Newberry: 00:17:31

So this is [different from checkpoints](https://en.bitcoin.it/wiki/Bitcoin_Core_0.11_(ch_5):_Initial_Block_Download#Checkpoints), a hard-coded checkpoint in the source code, because if there's a competing chain with more work, you can reorg to that chain and you'll get into consensus with that longer, more work chain.

James O'Beirne: 00:17:50

Yep.

John Newberry: 00:17:51

Whereas with a checkpoint, it precludes that.
A checkpoint would hard-code the exact chain that you would have to follow.

James O'Beirne: 00:17:57

Right, right.
So that really is the developers of the software dictating what the only allowable chain is.
Whereas this is sort of a public attestation that, hey, we've all previously validated this chain, we know it's valid.
This kind of change is interesting because when you think about it, from a threat model standpoint, it's a nice thing to have because Bitcoin is a very complex piece of software and it's very difficult to review for correctness.
Even people who are really experienced with the code base still have a really hard time determining, in some cases, whether a change is safe or not.
So when you kind of crystallize your security assumptions in a place where almost everybody can review it...

### Updating `assumevalid` value in the code

James O'Beirne: 00:18:51

So for example, the way that we [update the `assumevalid` value](https://github.com/bitcoin/bitcoin/pull/9484), ([0.19](https://github.com/bitcoin/bitcoin/pull/17002), [0.18])(https://github.com/bitcoin/bitcoin/pull/15429), because we do that typically with every release, is somebody will post a modification of that value, and then a number of people will chime in on the pull request and say, yeah, so I used the node that I previously provisioned with the initial block download process, and I ran this RPC command, and it told me that this hash that you mentioned in the source code is actually in my chain.
So I agree to this.
That's something that you don't have to be an expert in C++ to be able to do, you don't even necessarily need to be a software engineer to do that.
So the use of this technique allows you to get way more widespread review over a pretty security critical change.

Adam Jonas: 00:19:51

Do you find non-software engineers actually contributing though?
That assumption seems to work if actually other people are doing it.

James O'Beirne: 00:20:03

Yeah, I think not enough people are at the moment, but you definitely do see people in the Bitcoin community who are not involved in this sort of day-to-day development of Bitcoin Core who pay attention to those pull requests.
They'll chime in and they'll say, yeah, I ran this RPC command and this matches up.

So it really brings more people into the fold than otherwise would be on something where many, many people should be paying attention.
Because I could post a pull request tomorrow that claims to be some kind of optimization to the UTXO set, and it could contain some vulnerability.
The number of people who are currently able to find that vulnerability is very, very limited relative to the number of people who can run an RPC command and say, no, no, no, this doesn't match up with what I have.

John Newberry: 00:20:55

Yeah, and it should also be noted for the mountain men who, sorry, and mountain women (laughter), we don't preclude any people who live on mountains, but you can switch off this feature and validate every signature from Genesis to the tip.

James O'Beirne: 00:21:12

Yeah, exactly, very important.

## Assume UTXO

Adam Jonas: 00:21:15

So does that mean we're going to transition to `AssumeUTXO` ([GitHub issue](https://github.com/bitcoin/bitcoin/issues/15605), [proposal](https://github.com/jamesob/assumeutxo-docs/tree/2019-04-proposal/proposal), [talk](https://www.youtube.com/watch?v=PoEoG6sP1hw)), and how you arrived at that solution?

James O'Beirne: 00:21:20

Yeah, we can do that.
I was very concerned with this IBD thing, and I thought, how cool would it be if we could cut that time down substantially?
Even maybe cut it down enough so that you could at some point run it on these really underpowered devices and devices with not great internet connectivity.
So I spent a little bit of time tinkering with doing small things, like trying to make logging asynchronous and just these little optimizations.
I thought even if I eke out 10% to 15% reduction of the time, it's not going to make a big dent.

So what are some of the bigger ideas that might help me get this time down?
I think I first heard Alex Morcos mention this, but the idea of using some kind of a UTXO snapshot to bootstrap a node came up at some point, and I thought, oh, that's an interesting idea.
I don't think it'll necessarily work or be acceptable from a security standpoint, but it sounds like it'll be fun to implement, and I was looking for an excuse to get to know the code base better anyway.
So I said, okay, well, I'll come up a little prototype and just see how it works.
And so I did that.
Throughout the course of doing that, I became increasingly convinced that this was basically just the spiritual continuation of `assumevalid`.

So the idea of this is that, like `assumevalid`, you could hard code the hash of the UTXO set at a certain point in time, at a certain block height.
If you hard code that expected value there, you can then have the user upload a serialized version of the UTXO set that hashes to that value.
You can then initialize all the data structures in Bitcoin that are necessary for operation based upon that snapshot.
Then in the background, you can do the regular old initial block download.
But meanwhile, you're able to transact as sort of a fully validating node.
You can see incoming blocks, and you can judge their validity, and send transactions.

So I implemented this and found that, in terms of the security model, it didn't really differ from `assumevalid` and shopped it around to a few people.
To my surprise, the conclusion was, yeah, this looks pretty good.
On top of that, in the preliminary testing I did, the results were great in terms of trimming down the IBD time.
I think the latest numbers are something like an hour and a half from start to finish to get up and running on my computer.
So pretty good results so far.

John Newberry: 00:24:44

Okay, so let's just dig in a bit into how it's different from `assumevalid`, and why you get that significant performance improvement, or lower time to sync to the tip.
With `assumevalid`, you get the headers chain, you download all the blocks, and then you're building this UTXO set, but you're not validating signatures as you build up to the `assumevalid` block.
That building of the UTXO set itself is quite expensive.
Maybe you can talk a little bit about why that is, and the coins cache, and flushing to disk and that kind of thing.
Whereas with `AssumeUTXO`, you don't need to build that UTXO set, you get a snapshot.
So you just fast forward through the first 500,000 - 600,000 blocks, whatever it is, the height of the assumed UTXO block.
So maybe just a bit about where you're saving time when you do this?

## Platform and memory considerations

James O'Beirne: 00:25:44

The UTXO set is, other than maybe bandwidth and signature validation, probably the biggest bottleneck in doing initial block download.
We never defined what the set itself is, but it's a mapping of outpoint, which is the transaction ID and index, and then valued by the unspent coin itself, which you can find at that outpoint location.
We reference this thing when we're validating incoming blocks because we want to obviously verify that the coins being spent in the block are valid spends.
Then we want to actually update the set with the new unspent coins that are made available by that block.

This gets tricky because the UTXO set is about three and a half gigs right now, and on some platforms that can fit into memory, so access to that set is very fast.
On other platforms, we're limited by memory, and so we have to write out part of that to cached disk and selectively page in and out the parts that we're using at the moment into working memory.
So depending on your platform, it can get really expensive to do operations on this set when it gets big.
That's indeed where a lot of the time is spent when you're doing initial block download on, say, a machine that has 2 gigs of memory and maybe an old spinning disk.
You spend a lot of time flushing the in-memory coins down to disk and then reading coins that you haven't found in your in-memory part of the cache from disk.
So with `AssumeUTXO`, when you're given this serialized snapshot, and you can just load it in from a certain point in the height, a certain point in the chain, you've foregone doing a lot of disk writes and reads.

## Criticisms

Adam Jonas: 00:27:56

What criticisms have you received thus far?

James O'Beirne: 00:28:01

I think a lot of people read it and they are initially very skeptical, which I completely understand because I was skeptical, and you should be skeptical.
It seems like a too good to be true kind of thing.

The tricky part is that conceptually, it's much easier to sneak in, say, an illegitimate unspent coin than with `assumevalid`.
So for example, if you could convince someone to accept an `AssumeUTXO` hash that they had constructed specifically, it's very easy for an attacker to then serialize a modified version of the UTXO set that matches that hash, and then basically convince someone to accept an illegitimate spend.
Oh, and I guess it's worth noting an important part of the proposal is that unlike in `assumevalid`, you cannot specify the `AssumeUTXO` hashes through the command line, and this is a pretty intentional.
I think that would just be a huge foot gun because then you could pre-format the `bitcoind` command and trick somebody that way.

Okay, short of the malicious command line that you might give somebody, what you would have to do is modify the source code somehow to accept that malicious `AssumeUTXO` value.
The thing to keep in mind is that if you can modify somebody's binary, then you're cooked in the first place.
Because if you can modify their binary, it's much easier to just add some little conditional into the coins cache code that accepts their spend, or does any variety of things.
So in actuality, this doesn't open the potential for any attacks because we're still relying on the threat model of not being able to have your binary modified.

John Newberry: 00:30:03

I think there's a maybe more philosophical, subtle argument against, which is kind of a slippery slope argument that we want validation to be quick and IBD to be quick, and taking a shortcut like this is kind of kicking the can.
If people come to rely on this as the only way to validate the full chain, we might get ourselves into a position where it actually is impossible to fully validate the full chain.
Ethereum might be there at this point already...

Adam Jonas: 00:30:38

The fastest way to do the IBD is to just not validate at all (chuckle).
Super fast.

James O'Beirne: 00:30:43

Yeah, that's a good line of thinking.
I think the thing is that when we introduced pruning, we kind of went through this.
Obviously, if you run a pruned node, that means that you only keep around a certain number of the most recent blocks.
Obviously, if we don't want to use disk space, then everybody should run a pruning node, and at that point, nobody's serving blocks.

I guess this is a little bit different in the sense that, yeah, if everybody's starting in `AssumeUTXO` mode, and not back validating the chain, which is a sort of mandatory part of the current proposal...
Yeah, it's worth pointing out that if you are using `AssumeUTXO` in its current incarnation, you're doing a background validation from scratch.
So I think that kind of alleviates that concern, but there are people who argue that if you're willing to buy into the `AssumeUTXO` security model before you have done the back validation, then why even do the back validation?
There are a lot of people who have thought a lot about this and still sort of hold that opinion, but I think the nice thing is that if we all agree that that's the case, then it's a pretty simple matter to make the background validation optional or disabled at some point, but for now, we can be conservative and still do that.

## Championing a big change in Bitcoin Core

Adam Jonas: 00:32:16

So we were covering the arc of your Chaincode journey, and I guess I'd be wondering, what is it like to champion something that's such a big change and just so different?
What can you do yourself, and what do you need others to do to get something like this into Bitcoin Core?

James O'Beirne: 00:32:35

Initially, I didn't really think about this as a big change, but in hindsight, I guess it is.
I think the best thing you can do is just to try and be very communicative, try at every opportunity to provide motivation for why this is a good thing, why it makes sense.
I have taken the approach of trying to break this change up into a number of small constituent PRs, and just get those steadily merged so that the notion of progress doesn't become this binary thing about whether the giant PR is merged or not, you can have some incremental progress.
I think everybody feels a little bit better about that.
But yeah, I think in Bitcoin development, one of the really hard parts of it is socializing your work.
It's definitely difficult given the slow pace of development, which is of course merited, but I think effective communication and just being very clear about your motivations and demonstrating why it's worthwhile change...

Adam Jonas: 00:33:48

Just to be clear to the listeners, how did you go about socializing this?
You did a work in progress or a draft implementation and you started carving off pieces, or you did a draft up front, how did you get it out?

James O'Beirne: 00:34:04

Yeah, so I did the draft implementation, and that was the first artifact I had.
I spent a little bit of time polishing that up and making the commits work semantically, and I posted that along with a pretty lengthy description.
After that, maybe a few weeks after that, I let it hang out for a little bit.
I then made a mailing list post and solicited feedback from the Bitcoin dev mailing list.
I used that feedback to then build what in hindsight probably should have just been a BIP, but it was a frequently asked questions document that I posted on GitHub.
I asked a few people to review that, and some of that feedback I actually posted in the same repo as the frequently asked questions document.
After that, I started proposing parts of that big draft PR.
While that was going on, I guess I did some more informal stumping, I went on a few podcasts and you blackmailed me into doing a few talks, which I should thank you for.

Adam Jonas: 00:35:22

All done, yeah.

James O'Beirne: 00:35:25

So, yeah, it's a multifaceted thing and kind of any way you can shill your change, it's probably good.

John Newberry: 00:35:35

Thanks, James.

Adam Jonas: 00:35:36

Thanks, James.

James O'Beirne: 00:35:37

Thank you guys.

## Wrap up

John Newberry: 00:35:43

Okay, I really enjoyed that talk.
What did you think, Jonas?

Adam Jonas: 00:35:46

Yeah, I really liked the conversation about IBD and the `assumevalid` conversation, those were my two highlights.

John Newberry: 00:35:52

And we're certainly going to miss James here in the office.

Caralie: 00:35:55

Yeah, it was great that you guys got to sit down with him before he took off for his next adventure.

John Newberry: 00:35:59

Good luck, James.
We'll see you here.

Caralie: 00:36:01

Good luck, James! Bye!
