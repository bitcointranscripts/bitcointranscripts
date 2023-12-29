---
title: "OP_RETURN"
transcript_by: realdezzy via review.btctranscripts.com
media: https://www.youtube.com/watch?v=NYj80OGlWGg
tags: ["script"]
speakers: ["Sjors Provoost","Aaron van Wirdum"]
categories: ["podcast"]
date: 2022-07-15
---
## Intro

Aaron van Wirdum: 00:00:19

Live from Utrecht, this is Bitcoin Explained.
Hey Sjors.

Sjors Provoost: 00:00:24

What's up?

Aaron van Wirdum: 00:00:25

How exciting.
Two weeks ago you told me that maybe you would go to Bitcoin Amsterdam.

Sjors Provoost: 00:00:31

Yes.

Aaron van Wirdum: 00:00:31

And now you're a speaker.

Sjors Provoost: 00:00:33

I'm a panelist, probably not a real speaker.

Aaron van Wirdum: 00:00:37

That counts that that's a speaker in my book Sjors.

Sjors Provoost: 00:00:40

Sounds good.

Aaron van Wirdum: 00:00:41

How exciting.
Sjors today we're gonna discuss we're gonna discuss a blog post by BitMax Research.

Sjors Provoost: 00:00:48

That's right.

Aaron van Wirdum: 00:00:48

Which is about the OP_RETURN Wars.
So exactly, very nice clickbait title.
Do you remember what the name of the blog post is?
Was it was it just the OP_RETURN Wars?

## OP_RETURN War

Sjors Provoost: 00:01:00

It's called the OP_RETURN wars of 2014, Dapps versus Bitcoin transactions.
And it's a slightly clickbaity title because well it was only called wars by certain other people.
But

Aaron van Wirdum: 00:01:14

wasn't it referred to as the OP_RETURN wars previously in your memory?

Sjors Provoost: 00:01:18

Yeah, but some people object that the OP_RETURN wars have been sort of that term was phrased by people trying to launch various coins and trying to make Bitcoin developers look bad.
Not everybody likes the term.

Aaron van Wirdum: 00:01:31

Okay, fair enough.
Okay, so let's start at the beginning.
This has been, we've discussed this in some of our episodes here and there before, I think, but first of all, Sjors, what is OP_RETURN?


## What is OP_RETURN

Sjors Provoost: 00:01:44

So When OP_RETURN appears in a transaction, so in a script, then as soon as that happens, the script is invalid.
And so a nice example, and so the most practical form to use that would be that your entire script starts with OP_RETURN, and then it follows whatever you want to put there, for example, some random text.
Because when a script is invalid, you know it's not going to run, and that means that nobody can ever spend it.
Because no matter what you do, it's always going to be invalid.

Aaron van Wirdum: 00:02:14

Right, but that to me sounds like the transaction would be invalid.

Sjors Provoost: 00:02:18

Oh, no, no, no.
It's an output of a transaction.
So if you're sending to an OP_RETURN transaction, so if you're sending, if your address, quote unquote, so the script on the blockchain is in OP_RETURN followed by anything, then whoever tries to spend it will find that their transaction is invalid.

Aaron van Wirdum: 00:02:34

Right.
Okay.
So you can send to an OP_RETURN.
It's just provably unspendable.
You can't spend anything from an OP_RETURN.

Sjors Provoost: 00:02:42

Exactly.

Aaron van Wirdum: 00:02:42

From an output that has OP_RETURN in it.

Sjors Provoost: 00:02:45

Yes.
And because it's provably unspendable, that allows software that processes the Bitcoin blockchain to make some optimizations, it can basically just pretend that those coins don't exist.
But whether they really exist or not is kind of in the eye of the beholder.
They're there, but it's impossible to spend them.

## How long has OP_RETURN been around

Aaron van Wirdum: 00:03:01

Right.
And OP_RETURN has always been in Bitcoin?
Has it always been a function in Bitcoin?
Has it always been possible?

Sjors Provoost: 00:03:09

As far as I know, yes.
And so that means it's also been always been possible to put anything you want after the OP_RETURN code.

Aaron van Wirdum: 00:03:17

Right, so you could always create a transaction with OP_RETURN.
However, and now we'll get to this in a second, I think originally transactions that spent from an OP_RETURN, no wait, transactions that spent to, wait now I'm confused.

Sjors Provoost: 00:03:30

Yeah, as far as I know, originally, if you created a transaction that spends to an OP_RETURN, then nodes generally will not relay that transaction.
They would simply ignore it.
However, if they saw it in a block, they would be fine with it.
So that's called standardness.
In this case, it's not standard.
So standard transactions are transactions of a specific shape and form.
Those are automatically relayed.
And that's partially to prevent people shooting themselves in the foot by creating a transaction that's just wrong.
And there's probably some other reasons that we can get into in another podcast.

Aaron van Wirdum: 00:04:04

Right.
Yeah.
So, yeah.
So, an OP_RETURN was always possible, but Bitcoin nodes generally just wouldn't forward it to other nodes.

Sjors Provoost: 00:04:13

That's right.

Aaron van Wirdum: 00:04:13

So, it's very hard to get it into an actual block.

Sjors Provoost: 00:04:16

Yeah.
You'd have to talk to a miner.

Aaron van Wirdum: 00:04:18

Yeah, and then the miner would have to put it into a block, because I assume that mining software also by default just wouldn't include it in blocks, right?

Sjors Provoost: 00:04:27

Yeah, so either you would have to know which node is a miner, And then maybe that miner is configured that they do consider it standard, but more likely, the miner would have to manually include it through some process.

## OP_RETURN Node acceptance and Standardness

Aaron van Wirdum: 00:04:40

Right.
So at some point, and this is what the blog post is about, at some point, it was decided that nodes, that Bitcoin nodes, Bitcoin Core nodes specifically, although back then it wasn't even called Bitcoin Core yet, they would actually start forwarding some OP_RETURN transactions, right?
So why was that?

Sjors Provoost: 00:05:01

Yeah.
So in roughly the end of 2013 or the beginning of 2014, there was a release of Bitcoin Core that would let you that if there was less than 40 bytes or 40 bytes or less after the OP_RETURN message, it would be standard.
So you would relay those.
And then later on, as we'll discuss, it was increased to 80 bytes.
And so the reason is, it was kind of, I think one of the analogies that was used, or many analogies used, I'll stick to the, let's say the friendly ones, is this idea of People were breaking windows all the time because they're trying to get inside of a house and it was nice to just leave the window open, basically.
So it was actually a form, it was meant as a form of damage control.

Aaron van Wirdum: 00:05:42

Well, before we get to the analogy, or Well, now you've given the analogy, but what is it an analogy for?
What are we actually talking about?

Sjors Provoost: 00:05:49

What is the actual damage, right?
Why were people breaking windows?
So basically, people were trying to put things on the blockchain that are not transactions, that are not moving money, but that are sharing information.
And one example of that, which I'll shamelessly plug, you can also find in my book, is to put the Bitcoin white paper inside the blockchain.
And the way they would do that is to create a transaction that sends money to a multi-sig address and that multi-sig address would have three keys but those keys you know would not actually be keys because a public key would you know be a nice piece of data but they wouldn't be actual keys and it turns out that if you add up all these fake keys you can reconstruct a Bitcoin white paper.
Now, the problem with that is that for nodes who are looking at the blockchain, those transactions look like they're real.
They look like they're really sending money to somebody and that somebody apparently is a multi-sig owner.
And this is where the problem comes in.
Nodes don't only need to relay those transactions and store them in the blockchain, they also need to keep track of this thing called the UTXO set.
So there's a set, usually kept in memory if at all possible, of every coin that currently exists.
So when you create a transaction, you're spending a coin, so those coins no longer exist, and you're creating new coins, and those coins do exist.
That's what you need to keep track of.
And so this white paper and this other stuff that was put in that way has to be kept track of by nodes.
Even today, even though nobody will ever spend it, you still have to keep track of it.
And so the solution is to use OP_RETURN.
Now you can still put that kind of data on the blockchain if you wanted to, but nodes don't have to keep track of it because they know it is not spendable.

Aaron van Wirdum: 00:07:36

Right.
So to go one step back or to tackle that step by step.
So originally if you wanted to include data in the blockchain, could be any type of data, You gave the Bitcoin white paper as an example.
Then what people would originally do is basically break down the Bitcoin white paper into data and then create public keys that aren't actually public keys because there are no private keys for them.
And these public keys would just include the data that is the Bitcoin white paper, right?

Sjors Provoost: 00:08:04

Yes.

## Keeping unnecessary data off the UTXO set

Aaron van Wirdum: 00:08:05

Right.
So, and then that's transmitted over the Bitcoin network.
Everyone verifies these as transactions.
It's included in the blockchain and then it's also included in the UTXO set.
Now, with OP_RETURN, it's still included in the blockchain.
Yes.
However, it's not included in the UTXO set.
That's the real difference there, right?
Yeah, exactly.
Notes just know these coins are provably unspendable, so we don't have to store these in the UTXO set.


Sjors Provoost: 00:09:33

Yes, so it saves some time because now when you know you still have to download the blockchain, you still have to check every block, that does not change.
But the difference is that this little database that you're keeping of the UTXO set, that no longer has to grow.
And you can also normally throw away old blocks.
So if you have a small hard drive, you can always toss out the old blocks, but you can never toss out anything from the UTXO set.

Aaron van Wirdum: 00:09:54

Yeah, so the two main benefits are, first of all, storage, especially for pruned nodes that don't store the entire blockchain, because they now have a benefit because they have a smaller UTXO set.
And the other one is computational.
When a new transaction comes in, there's a smaller UTXO set to check the new transaction against.

Sjors Provoost: 00:10:13

Yeah.
So I guess a better way to say that is it's saving you, potentially saving you memory.
So ideally you want to keep the entire UTXO set in RAM.
Now that's already not possible these days.
I guess back when this discussion was happening, the UTXO set may have been much smaller, maybe a few hundred megabytes.
Now it is over 10 gigabytes.
So for now most people unless you have like you know 20 gigabytes of RAM you're probably not holding it in RAM anyway.
But it is nice if you can keep the UTXO set in RAM all the time it's much faster.
And we did an episode about that.
It is episode 15 in which we explain a mechanism that could solve this problem called U3XO.
And that would remove the need to keep the UTXO set in RAM, but it comes at the expense of some trade-offs.
And we just explain those there.

Aaron van Wirdum: 00:11:02

Okay, let's stick to the OP_RETURN for now.
People were storing data in the blockchain.
This came at a cost for people that were running full nodes.
And so at some point, developers figured, okay, look guys, if you're going to store data in the blockchain anyways, then please use OP_RETURN.
And that way, there's a smaller cost to all nodes.

Sjors Provoost: 00:11:27

Yeah, but there was a second request too, I would say, because this limit of 40 bytes.

Aaron van Wirdum: 00:11:32

Yeah, I was going to get there.
So OP_RETURN was always in the protocol, but it was basically useless because nodes wouldn't forward OP_RETURN transactions.
Then Bitcoin developers said, all right guys, you're going to store data anyways.
So we'll allow, we'll effectively enable OP_RETURN.
But then the next debate was about the size of the OP_RETURN messages.

## The OP_RETURN message size debate

Sjors Provoost: 00:11:55

Yeah, exactly.
So one number you could have used for that size was to say, okay, how big can these multi-sig transactions be?
And I think that was 172 bytes so you could have said okay we're just gonna make OP_RETURN 172 bytes because in that case there is really no reason to use these multi-sig keys anymore because you might as well use OP_RETURN but there was a simultaneous I guess movement or desire to not make the blockchain unnecessarily big.


Sjors Provoost: 00:12:22

I think it's useful to look at that in perspective.
So right now there is a fee market.
So that means that if you're putting a lot of data onto the blockchain, it's going to be very expensive for you to do that.
Or at least there's a mechanism to make sure that, you know, useful stuff goes on the blockchain more easily than useless stuff, depending on if you define useful by how much you're willing to pay for it.
But back then, blocks were super small.
They were maybe 10 kilobytes or 100 kilobytes, I don't know where they were in 2014.
And that meant that this OP_RETURN data could just make blocks really big for the time that happened.
And we've done an episode in the past where we looked at, I think it's episode number 55, where we looked at old node software and see how that old node software would perform under the current block sizes.
And it turns out that very old node software, especially from say 2012, would not have been able to keep up with actual one megabyte blocks,or at least not very easily.
So back then it was actually necessary to keep blocks small, basically from a more altruistic point of view.
And that's what a lot of the discussion was about, like what is good behavior on the blockchain.

Aaron van Wirdum: 00:13:27

So why was, so the first limit that was set, well initially the limit was zero, initially OP_RETURN was effectively impossible, but then the limit was increased to 40 and why why was it increased to 40 okay

Sjors Provoost: 00:13:43

so the idea behind 40 is that it allows you to put a hash in there, a typical hash using normal cryptography like SHA-256 is 32 bytes.
So this allows you to put a 32 byte hash on the blockchain and then a few extra bytes to do, I don't know, some metadata for that hash.
Now there were some protocols out there that wanted 80 bytes.

Aaron van Wirdum: 00:14:06

Yeah, Counterparty in specific.
This is what sort of this blog post that is the reason we're making this podcast.
That's the main example that's given.
It's basically about the counterparty protocol.

Sjors Provoost: 00:14:17

Yeah, so I don't know for sure if the increase to 80 bytes was only for counterparty or whether there was another protocol that needed it.
But basically there was some back and forth and I guess people decided to just allow 80 bytes.
But really 40 should be enough for most things, but it requires a little bit more work for those protocols.
So if you look at something like, as far as i know..

Aaron van Wirdum: 00:14:38

The reason 40 is enough is what you're saying is because really the only data you ever need to include in the blockchain really is a hash.
Because then you anchor any other data you want to anchor in and that's really all you ever need to do.

Sjors Provoost: 00:14:52

Yeah, so if you're building some sort of other protocol and we talked about open timestamps in an earlier episode, we talked about other things.
Generally that protocol has its own software and that software should take care of its own data.
It should have its own peer-to-peer network essentially.
It should send its own data around.
Maybe that data is a blockchain, maybe that data is something else.
But that's more complicated to implement because now you have to build your own peer-to-peer network And so a lot of these protocols back in the day and very likely Counterparty as well preferred to just shove everything onto the Bitcoin blockchain and not have to deal with that complexity.
And so that was some of the discussion about.
But Counterparty was using the multi-sig solution in the beginning.
So they were putting data on the blockchain anyway.
And so yeah, I guess then it makes more sense to say, okay, let's just increase the OP_RETURN limit to 80 bytes.
So they stopped doing that.

Aaron van Wirdum: 00:15:44

So At first it was increased to 40, this was in 2014 and the argument there, as we explained, or as you explained, is that you really only need 40 because you can just include a hash.
But then people, you said a counterparty project, it was using more than 40 for whatever they want to do.
So essentially Bitcoin developers conceded and said, all right, well, if you're going to do it anyways, here's 80, here, have fun with it, with your 80.

Sjors Provoost: 00:16:13

I think that's how it went, But there may have been other projects there too that needed 80 for some reason.
Now there is some confusion because if you look at the original proposal, so the original release that had the 40 byte limit, there was also a pre-release.
So with Bitcoin, or Bitcoin Core anyway nowadays, What happens is when you make changes they go into a pull request on GitHub and then once they're approved they get merged and they end up in this master branch and this master branch sort of a working copy which is not released but anybody can run it so there was a time when there was a limit of 80, if you were using that master branch of Bitcoin.
But generally that's not considered final software, it could have bugs in it, et cetera.
So before that release came out, it was reduced to 40.
Does that make sense?
So there was a limit of 80, but only in unreleased software.
Then there was a limit of 40 in the release software.
And then much later, there was another limit of 80.
And so some of the fight, war, whatever you want to call it, seems to be about that.

Aaron van Wirdum: 00:17:14

They announced 80.

Sjors Provoost: 00:17:15

Where It was sort of seen as a revoking of the 80, but that was never really released.

Aaron van Wirdum: 00:17:21

Right.
Got it.
It was never 80, but it was announced to be 80, and then it was brought back to 40.
And I think that's what threw some people off.

Sjors Provoost: 00:17:29

So I think what happened is there was this upper turn thing was introduced in the code and they just picked 80 as the first number then there was, I think Jeff Garzik put it on the mailing list saying hey we should probably talk about that and then people said okay let's make it 40 and that was what went into the release.
So and then there's you can find newer discussions where people said oh you know we told you about Counterparty and then I think Greg Maxwell would say no you didn't you told us after basically this release and then we increased it but you know so that's a whole fight about what was the sequence of events there.

Aaron van Wirdum: 00:18:04

So and right now the limit is 80?
Yeah and there was a minor maybe mistake in the blog post where it said that currently the limit is 83 but you you say it's just 80 right?

Sjors Provoost: 00:18:16

So the the amount of data you can put on it is 80.
However, the size of the output, so what the script on the blockchain would look like, is 83.
And the reason is because you have one byte that says OP_RETURN, then you have another byte that says, I'm going to give you a bunch of data now and then another byte that says how much data so that that would be 80 bytes for example and then the data itself so that in total that's 83 and there's some some weird edge cases where you could have like one OP_RETURN and then say I'm gonna and then you could say I'm gonna give you five bytes of data and now I'm gonna give you another five bytes of data.
So there's ways of grouping your data.
There's just very subtle implementation details, but as long as you stay below the 83 bytes for the whole script you're fine.

Aaron van Wirdum: 00:19:03

Right.
Now one thing you already alluded to is that back then, back when this discussion was happening, I think people were really looking at the Bitcoin blockchain as sort of a shared resource.
And they weren't thinking about it as much, it seemed like, like we would today as a market.
So today, in general, I think we have more of this idea that whoever is willing to pay the highest fees gets into the block.

Aaron van Wirdum: 00:19:34

And we have a block size limit to protect nodes, essentially, to protect users from having to store too much data.
And back then, people weren't really thinking about fee markets yet.
There were no fee markets yet.
So it was really just considered a shared resource.
Now from today's perspective, don't you think it would make more sense to just remove any OP_RETURN limit and just say whoever wants to pay for it will pay or put differently would you say that maybe the people that were making that argument what was it eight years ago maybe you were right that it should have just been allowed and whoever pays pays

Sjors Provoost: 00:20:14

I'm not sure So one of the things is that the fees that you're paying go to miners, they don't go to node operators.
So every node operator is still somewhat altruistically running these things.
So you'd still want to see what do you want node operators to do for you?
Do you want them to store your your bible?
Or do you only want to do payments?
So you could still have that argument that even if somebody was willing to pay a very high rate, a very high fee to miners to include lots of OP_RETURN data, you could argue well, but they're not paying the node operators to store that OP_RETURN data and people are not running nodes to publish the Bible or whatever.

Aaron van Wirdum: 00:20:52

But they don't have to store the data.
Though they still need to verify it once.

Sjors Provoost: 00:20:56

Yeah, they still need to process it.
So, but yeah, the burden is a bit lower, especially when you use OP_RETURN and it's much better than the alternatives.
On the other hand, there's also now things like RGB and things like OpenTimestamps, various other projects that show that you can just use a single hash or even not a hash at all because from a privacy point of view, things like tweaked signatures, tweaked public keys or tweaked signatures are even a more privacy-friendly way to put data on the blockchain, which also makes them indistinguishable from regular transactions.
That one thing, that means that you can't stop it, whatever you do in the protocol.
But it also means that by using the protocol in that way, even though you're using it for something that's not moving money around, you are helping the people that are moving money around because you're creating a bigger anonymity set for everybody else.
Because you're just creating a bunch of noise between all the transactions.

## Should the size limits remain?

Aaron van Wirdum: 00:21:48

Right.
Well, that could also be considered an argument for removing the limit.
It's like you say, if you can create it anyways and no one can even see that you're just creating data that's non-transaction data essentially.

Sjors Provoost: 00:22:01

You can't see it if you're not using OP_RETURN.
So those protocols that use tweaked signatures don't use OP_RETURN at all.

Aaron van Wirdum: 00:22:09

Well, that's what I mean.
So at that point, why don't we just say, okay, people can put data on the blockchain and we can stop them.
We might as well just make it easy and have it done in such a way that it doesn't impact the UTXO set.

Sjors Provoost: 00:22:24

But then it's actually hurting privacy because if people start using OP_RETURN for their data instead of these more privacy-friendly ways, then they're just hurting their own privacy.
But as far as I know there's nobody currently with a serious proposal of why they would need bigger OP_RETURN messages.
I think Bitcoin SV is experimenting with very, very, very, very large OP_RETURN messages and like has 99.999999% of their chain with OP_RETURN data.
So I don't know how I would feel about it, but so far I don't think it's a relevant question.

Aaron van Wirdum: 00:23:00

So the general idea behind, and I think this is what you mentioned when you said some people don't like the term OP_RETURN wars, is that this part of Bitcoin's history is sort of considered by Vitalik decided to launch Ethereum.

Sjors Provoost: 00:23:15

Yeah, but that makes very little sense because he could have used, if he needed OP_RETURN, then he could have done the same thing with OPMULTISIG.
So I don't think that particular thing would have made the difference.
It's not possible to run Ethereum on top of Bitcoin with or without OP_RETURN.

Aaron van Wirdum: 00:23:36

And the other thing anyone can do, of course, is just fork Bitcoin Core and allow for bigger OP_RETURN messages, since it's not a consensus rule.

Sjors Provoost: 00:23:44

So you know, maybe The lesson from that discussion was that Bitcoin was clearly not going the way of allowing everything and everyone to do complicated things on the blockchain.
And that may have been a realization point for him to say, okay, if Bitcoin is not going that direction, I'll try my own project.

Aaron van Wirdum: 00:24:00

Yeah, I think that's sort of the argument or that's also the argument sort of presented in this blog post that it was a cultural thing that the Bitcoin culture at that time was not very accommodating to non-transaction data on the blockchain and that's why Vitalik decided to start his own blockchain.

Sjors Provoost: 00:24:19

Perhaps, might also have something to do with being able to make money.
But of course the nice thing about having a new chain is you know you can do whatever you want so it does give you a lot of creative freedom.
That's the more optimistic interpretation of it.

Aaron van Wirdum: 00:24:31

Yes, they can clearly do whatever they want.
We cover everything about OP_RETURN?

Sjors Provoost: 00:24:36

I think so.
Well, it might be fun to mention there was an incident in 2019, a project called VariBlock, Which I believe has Jeff Garzik as their advisor.
And at some point there was a lot of increase in the number of OP_RETURN transactions, not the size of them, just the sheer number of them.
To the point where they were starting to compete, you know, they had to pay some pretty high fees to compete with regular transactions And it was interesting to watch and there was kind of a worry that this would just mean that, you know, OP_RETURN transactions are the buyer of last resort and every block from now on will be full.

Aaron van Wirdum: 00:25:11

That was basically an altcoin that used Bitcoin's proof of work as its security?

Sjors Provoost: 00:25:18

Yeah, I believe so.
I think roughly what the idea was is that people on that altcoin would create candidate blocks basically and the hash of those candidate blocks would be on the Bitcoin chain and then whoever paid the highest fee on the Bitcoin chain would be the winning block on that chain.
So you'd have lots and lots of Bitcoin transactions, each with a hash that could represent the future block and then whichever has the highest fee would win.
So it would be a nice way to give money to Bitcoin miners.
But last time I checked on a coin market cap, it said market data is untracked.
So it sounds like that's not going very well.

Aaron van Wirdum: 00:25:50

It doesn't sound very good, Sjors.

Sjors Provoost: 00:25:51

But who knows.

Aaron van Wirdum: 00:25:52

Okay, I think that's it, or not.

Sjors Provoost: 00:25:55

Yep, that's all I got.
Great.
Thank you for listening.
