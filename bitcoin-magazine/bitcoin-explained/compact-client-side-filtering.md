---
title: "Compact Client Side Filtering: Neutrino"
transcript_by: NeroCherubino via review.btctranscripts.com
media: https://www.youtube.com/watch?v=HGrdiwqlKhU
tags: ["spv"]
speakers: ["Sjors Provoost","Aaron van Wirdum"]
categories: ["podcast"]
date: 2021-01-29
---
## Introduction

Aaron van Wirdum: 00:01:34

Live from Utrecht, this is The Van Wirdum Sjorsnado.

Sjors Provoost: 00:01:37

Hello.

Aaron van Wirdum: 00:01:38

Van Wirdum Sjorsnado.
Did I say it right this time?

Sjors Provoost: 00:01:42

I don't know.
We're not going to check again.
This is take number three.
Now you're going to ask me whether I rioted and I'm gonna say no.

Aaron van Wirdum: 00:01:51

You're like psychic.

Sjors Provoost: 00:01:53

Yes.

Aaron van Wirdum: 00:01:54

You're able to predict the future.
Okay, so let's skip all the rioting jokes and all the pronunciation jokes and get to it.

Sjors Provoost: 00:02:02

Yes.

Aaron van Wirdum: 00:02:03

What are we gonna discuss?

Sjors Provoost: 00:02:04

I think we're gonna talk about compact block filters.

Aaron van Wirdum: 00:02:06

Yes aka Neutrino.

## What are Light Clients

Aaron van Wirdum: 00:02:09

These are a new type of filters for light clients so first let's start at the beginning Sjors what are light clients?

Sjors Provoost: 00:02:20

Yeah we should also caveat that by new type, we mean from 2018 or something.

Aaron van Wirdum: 00:02:25

It's not brand new, but it's still fairly new.

Sjors Provoost: 00:02:27

Yeah, we mentioned in the last episode that we were going to talk about that at some point.

Aaron van Wirdum: 00:02:31

Yeah, we did, because we did a Bitcoin Core 21 episode and it's one of the new features in Bitcoin Core 21.

Sjors Provoost: 00:02:38

That's right.

Aaron van Wirdum: 00:02:39

And now we're gonna get more in depth about Neutrino.
So what are light clients?

Sjors Provoost: 00:02:44

So the idea of a light client is that you don't want to download the whole blockchain.
And Satoshi made some remarks about that in the original white paper, how you could avoid downloading the entire blockchain, maybe if you were on a mobile device.

Aaron van Wirdum: 00:02:56

Yeah, you want to be able to use Bitcoin, that is, send and receive Bitcoins, for example, Satoshi's, but you don't want to have to download the entire blockchain, which you normally would have to do in order to know what the current state of balances of UTXOs is, which you need to know in order to know if transactions are valid and so forth.
The downside is it takes about two days, I think nowadays, depending on how fast your computer is, but something like that on a reasonably fast computer.

Sjors Provoost: 00:03:27

Yeah, I think I can do it in five hours.

Aaron van Wirdum: 00:03:30

Yeah, because you've got like a wizard's computer, but normal people would take like two days.
But even on your phones, you couldn't do it in five hours.

Sjors Provoost: 00:03:39

No, on a phone it's horrible.
It's days if not weeks.

Aaron van Wirdum: 00:03:42

Yeah, so that's where light clients come in.
So what are light clients?

Sjors Provoost: 00:03:46

Yeah, so of course there are different ways to do it.
The very lightest of lightest clients would be a custodial wallet, but we don't want to talk about that.
But here, what we're talking about is something that uses SPV, so simplified payment verification.

Aaron van Wirdum: 00:04:00

Oh yeah, so custodial is one way to do it.
The other way is to sort of connect a wallet to a full node, which you're running on some other device.
But what we're going to discuss here is yet another solution, which, yeah, SPV, as you mentioned.

Sjors Provoost: 00:04:15

Yeah, so simplified payment verification, as it says, it is a simple way to verify payments.
And why do you care about that?
Because the real, one of the things you care about when using Bitcoin is that you actually got the coins that you think you have.
That may be something you want to verify.
And there's actually a way to do that, which involves knowing the headers, and the headers are 80 bytes each per block, so it's pretty small.

Aaron van Wirdum: 00:04:39

Yeah, the block headers.

Sjors Provoost: 00:04:40

And then in addition to that, a proof, a Merkle proof that shows that this transaction is actually inside the block.
So if you know what a transaction is and you know that it's in the block, then you know you've received it, assuming that the rest of the block was valid and nobody did any shenanigans with the history, etc.

Aaron van Wirdum: 00:05:01

Yeah, so in a way you're kind of trusting hash power you're trusting that whoever invested all this energy in hash power did so because it would be too expensive to do this while mining an invalid block.

Sjors Provoost: 00:05:19

Exactly, so you're trusting other people to do the verification.
The other thing is that somebody can prove that you did receive a transaction this way, they can give you that proof.
For example, the person who paid you, but also the wallet has a way to fetch it which we'll talk about but it doesn't work the other way around so just because nobody's giving you a proof doesn't mean that you did not receive the transaction you cannot prove that a transaction does not exist.

## Bloom Filters for Light Clients

Aaron van Wirdum: 00:05:44

So let's say I'm running an SPV client and someone told me they paid me, then I want to know if that's really true.
So I would ask you, Sjors, who's running a full node, you could tell me I didn't receive anything, even if I did.
I'm still trusting you in that way.

Sjors Provoost: 00:06:03

Yeah, we can go into a little bit more detail about how that works.
So the naive way would be, okay, if somebody makes a payment to you, then that person should send the proof.
That's possible, but it's not very convenient.
So what instead happens is something called Bloom Filters.
And what your lightweight wallet does is it creates a filter which says, give me all the transactions that relate to this address.
But It doesn't really say which address it is, but there's some magic math going on so that when a node sees a certain address, it'll know that it has to send you a signal.
So for example, it would say, give me all the transactions in which an address starts with an A.
And that's not exactly how it works.
It's mathematically more sophisticated than that.
But you can understand intuitively what the privacy benefit of that is.
Like I'm not telling you that which address I have.
I'm just telling you tell me everything that has an A in it.
And you can configure that.
So you can say well give me every address with ABCDEF.
Some more specific things.
So you get only the transactions you care about.
If you care a bit more about privacy, you ask for a bit more, but it comes at the cost of bandwidth.

Aaron van Wirdum: 00:07:13

So the thing is, your actual addresses are a subset of the addresses you're asking about.

Sjors Provoost: 00:07:19

Exactly.
So in practice, your light wallet sends a message to a full node somewhere on the network, one of its peers, and this full node will then keep an eye on that.
As long as you're connected to it, it will keep an eye on those addresses and it will send you a block, but with only those transactions in it that match.
And each of those transactions will have the correct proof that it actually belongs in the block.

Aaron van Wirdum: 00:07:41

Which the light client is then able to check.
So the light client checks, okay, is this actually the address I cared about or is this a false positive is the block valid as far as hash power goes and then is the transaction valid I guess and if that all checks out then the light client sort of knows fairly sure that it has been paid even though they're still trusting hashpower.

Sjors Provoost: 00:08:04

Yeah, so there's a couple of issues with this and we talked about one already.

Aaron van Wirdum: 00:08:08

Yeah, just to be clear in case any listeners are confused this is not what the rest of the episode is going to be about.
This is like a trick that exists, has been existing for the past, what is it?
Eight years, something like that?

Sjors Provoost: 00:08:21

Yeah.

Aaron van Wirdum: 00:08:22

Probably longer than that.
What we're actually gonna discuss in this improvement on this solution, because there are problems with this solution and that's what Sjors is gonna explain now.
What are the problems with this solution?

### Problems

Sjors Provoost: 00:08:35

Yeah, so one problem is privacy and particularly because you don't want to use too much data, there apparently are quite a few wallets out there that will use the lowest false positive rate possible.
So you can say okay you know do I want lots of false positives so lots of information about other addresses so I have good privacy but you can also set it very low and apparently they use a very low one which means that you're really just telling the full node that you're talking to, okay, this is the address I care about.
And that's a problem because that full node you're talking to might be Chainalysis.

Aaron van Wirdum: 00:09:10

Yeah, and I think it's not just that, I think there's also some additional puzzling the full nodes can do.
Like if he would be interested in this address, he wouldn't be asking about this or with change or something.
I don't know the details.
I just know that this solution, this SPV solution is broken privacy-wise.
I think Nick Jonas broke it a long time ago.
He works for Blockstream now.
And since then, everyone agrees that this is broken privacy-wise.
If you're using SPV in this way, you're essentially giving away all of your addresses to a random node on the Bitcoin network.

Sjors Provoost: 00:09:47

Okay, so that's also bad.

Aaron van Wirdum: 00:09:48

Or several, probably even several nodes.
You're just giving away your privacy.
It's broken.

Sjors Provoost: 00:09:54

Yeah, the other problem is that it's pretty intense on the node that has to do this, that has to provide these filters, because if you're running a full node, now some random node starts talking to you and says, hey, please give me updates about these addresses.
And so you need to do a bunch of CPU use for people, and you're just doing it voluntarily.
And it turns out that that's even exploitable.
If you create a special filter, you can create a lot of CPU load for somebody even though you don't actually care about those transactions.
So you can write especially those Raspberry Pis which is turned into steaming you know.

Aaron van Wirdum: 00:10:29

Yeah, so in this case the the light client, the SPV client, is making the filter for the addresses it cares about plus false positives, gives this filter to a full node on a network, and then this full node has to decipher which addresses the light client is interested in.
This is costing the full node's CPU power.
So it's costly, and the full node isn't earning anything by it, unless it's a spy node, and then we're back to problem one.

## Compact Block Filters

Sjors Provoost: 00:10:59

Well, and that creates a perverse incentive of course, because for normal people there is really no reason to do this other than altruism, but for spy nodes there is a financial motive to do this, so guess who are serving this.
So let's move on to a new approach that was produced, I believe proposed around 2018, maybe 2019.

Aaron van Wirdum: 00:11:18

By Lalu (Rosebeef), Lightning Labs' CTO.

Sjors Provoost: 00:11:30

This is often referred to as Neutrino, but technically Neutrino is an implementation of that.

Aaron van Wirdum: 00:11:36

Of the general idea?

Sjors Provoost: 00:11:37

Yeah, of the idea of compact block filters.
The BIPs you want to look for are BIP 157 and BIP 158.
So, I think we should first talk about high level, what's going on and why it's good.
And then I'll try to do a quick explainer on what it's actually doing at a more nitty gritty technical level, because it's kind of cool, I think.

Aaron van Wirdum: 00:11:58

Sounds good to me.
Start with the high level stuff.

Sjors Provoost: 00:12:01

So the high level stuff, if you're running a full node, you're no longer getting custom filters from the peers that connect to you.
There is only one filter.
Basically what you do as a full node is you process all your blocks and you create an index for every block.
There is a couple kilobytes of information that you need to keep track of.
And you do that once and then peers can ask for it and you just give it to them.
So every peer gets the same information from you.

Aaron van Wirdum: 00:12:27

I think what you're trying to say is with the SPV solution we discussed a minute ago, the light client creates a filter that includes the addresses it cares about plus false positives and in this Neutrino solution or compact block side filters or whatever it was called officially, This is reversed and the full node actually creates the filter.

Sjors Provoost: 00:12:52

That's right and the filter just covers everything.

Aaron van Wirdum: 00:12:55

Everything that's in the block.

Sjors Provoost: 00:12:57

Well, every output script that's in the block And for every input, the output script that corresponds to it, which would be in the previous block that it's spinning from.

Aaron van Wirdum: 00:13:06

So this means that any full node, especially now with Bitcoin Core 21, any full node can create a filter.
And they would all be the same because they're all seeing the same block?

Sjors Provoost: 00:13:17

Yes.
And now on the client side what you do is you connect to any peer and you say give me the filters.
You know you're not giving away any information when you're doing that other than that you're a light client.

Aaron van Wirdum: 00:13:29

The light client just asks for the filter.

Sjors Provoost: 00:13:32

Right and it could you know in theory it could ask multiple peers and make sure that they get the same filter.

Aaron van Wirdum: 00:13:37

Then what does the light client do with the filter?

Sjors Provoost: 00:13:40

So what the light client is going to do is it's going to see it's going to go through its own addresses and it's going to see does the filter match any of those addresses.
So basically you can see for every block you run your addresses through the filter and it'll say yes this block contains transactions pertaining to the filter.

Aaron van Wirdum: 00:14:01

There are still false positives.
So what light clients really do is they put their address through this filter or whatever they actually do technically, you're going to explain it in a minute.
And then a computer is going to tell them yes there might be relevant transactions in this block or no there are definitely no relevant transactions for you in this block.

Sjors Provoost: 00:14:29

Yeah and so this false positive story is as far as I know is not because of privacy, it's just because math can't do better.
This has to do with like, if you want less false positives, then the files that the node need to keep track of need to be bigger.
So if you make the filters really big, then you never get false positives, but then you might as well download the whole block.

Aaron van Wirdum: 00:14:50

So if the computer says no, there are definitely no relevant transactions in this block for you, then the light client just ignores the block.

Sjors Provoost: 00:15:01

Exactly, you can do that.
Assuming the filters are not a lie, it should work.

Aaron van Wirdum: 00:15:07

What if the computer says yes?

Sjors Provoost: 00:15:09

If the computer says yes, you have to download this block.

Aaron van Wirdum: 00:15:11

Then you download the full block.
So even a light client in that case downloads, well, whatever it is, 2 megabytes of data, just downloads the whole block.
And then searches in this block to see if there was actually a transaction pertaining to that client in the block.

Sjors Provoost: 00:15:28

Yeah, so if your wallet is tracking thousands of addresses then maybe you have to download one in a hundred blocks as a false positive even though you haven't done anything right so this depends on how many addresses you're watching you get a little bit more false positives but yeah you have to download a bunch of blocks.

Aaron van Wirdum: 00:15:47

So you actually have to download slightly more data compared to the previous privacy-broken SPV solution.

Sjors Provoost: 00:15:55

But you get much better privacy.

Aaron van Wirdum: 00:15:56

Because now sometimes you need to download a block.

Sjors Provoost: 00:16:00

Yeah

Aaron van Wirdum: 00:16:00

Even sometimes if there's a false positive, so sometimes you download a block for nothing, but sometimes you've got to download a block, but then you get much better privacy.

Sjors Provoost: 00:16:09

Yeah, and you could even be smarter about it.
Like you could request one block per peer so that the only thing each peer knows is that you may care about something in that block which is not a lot of information maybe you fetch them over Tor if you want to be even better so that's kind of nice privacy wise but it reuses a bit more bandwidth

Aaron van Wirdum: 00:16:29

Is that a high level part?

## Downsides

Sjors Provoost: 00:16:31

No so we can also talk about some of the downsides.
So the biggest problem is that the filters can be fake, as in a node can just give you a complete nonsense and then you start asking for blocks.
First of all then it would match at the wrong block, so you wouldn't be able to find the blocks that pertain to you.
Of course, at some point, maybe you can figure that out if you ask multiple peers for their filters and then you start comparing which one is lying.
But that's the kind of worms.
The good news is it is being used by a lot of the, especially Lightning mobile wallets.
And they seem to work, but maybe we still live in this happy time.
So I think we talked about that last time.
Where now everybody's being nice to each other, but maybe one day people are stopping nice to each other and then I don't know what's gonna happen.

Aaron van Wirdum: 00:17:20

Yeah we we spoke about it in the podcast but I think in a different context right?

Sjors Provoost: 00:17:25

Yeah.

Aaron van Wirdum: 00:17:26

Or not.
Well anyways so one problem is that you're a light client, I'm a light client, I'm downloading this filter from you, Sjors, who's running a full node, and then I actually have no idea if this filter is actually a filter or just gibberish.
Is that what you're telling me?

Sjors Provoost: 00:17:42

Yeah, not just gibberish, but just wrong.
Like it has the wrong transactions in it, it will match the wrong things.

Aaron van Wirdum: 00:17:48

Right, and there's no way for me to tell the difference.

Sjors Provoost: 00:17:51

No, and unfortunately, it's also the case that if you download a block, you cannot recreate the filter.
So the only way to create the filter is to download the entire blockchain.
And the reason for that is that the filter contains not just the outputs, because the outputs you know.
If you download a block you know what outputs are in that block.
But it also contains the outputs for every input.
And so that refers to earlier blocks.
So the only way to really check whether it's not lying would be to find a block and then make sure that you find all the blocks for those inputs and it would just be a mess.
So that's unfortunate.

Aaron van Wirdum: 00:18:32

This sounds like a very big downside.
It sounds like if someone would want to attack these kind of light clients.

Sjors Provoost: 00:18:41

Yeah but then you have to maybe compare it to the you know earlier situation that we had with the Bloom filters.
It's kind of also about lying by omission.

Aaron van Wirdum: 00:18:49

That's really the problem.
And it's sort of a DOS factor this time on the client, because the client could be having to download every single block because it doesn't know which one to download.

Aaron van Wirdum: 00:19:00

Is that a high-level part?

## Technical Details

Sjors Provoost: 00:19:02

Yeah, I think in the long run, one of the thoughts is to turn that into a commitment into the block, but that itself is controversial, but that would at least solve this trust problem, because if the filters are committed in a block, then you do know that they're correct, at least you're back to SPV proof.

Aaron van Wirdum: 00:19:18

You're at least back to trusting the hash power.

Sjors Provoost: 00:19:20

Yeah, so then you're at the same trust as you were with the bloom filters, in terms of trusting hash power.
Okay, so let's maybe talk about how this works.

Aaron van Wirdum: 00:19:32

Yeah, you want to get more technical?

Sjors Provoost: 00:19:34

Yeah, so here's the recipe.
If you're serving these filters, what you do is you go through a block, for each block, you take all the output scripts, except `OP_RETURN`, because that's not interesting, And for every input you take all the output scripts it refers to.
And you just put those in a row.
And now, for every item you're going to hash it, there's a special hash function for it.
We talked about hash functions, I think, in another episode.
So now you have these hashes, which are just essentially all semi-random.
Just looks like noise.

Aaron van Wirdum: 00:20:08

Looks like random numbers.

Sjors Provoost: 00:20:10

Yes.
They're deterministically random, so if you take an output script, you will get the same hash.
And then you're going to sort those hashes and you're going to calculate the difference between the hashes.
Because hashes are just big numbers.
So you can subtract, you sort them and then you subtract them.
And it turns out that this is something you can compress with Golomb coding.
And this is just some mathematical trick that I don't understand, but it turns out that if you have a pattern like this, a bunch of sorted random things, you can compress it very efficiently.
And so you do that, and now the client gets this compressed piece of data and what it's going to do is it's going to look at the addresses that it is interested in, the scripts that it is interested in, and it's going to hash its own scripts.
And remember the hashes were sorted so now you can actually check the filter for the first hash and then the second hash and the third hash etc.
And see if you have a match and then you can stop when your hash is higher, is a greater number than the last hash you checked.

Aaron van Wirdum: 00:21:22

I don't understand that at all, but sounds interesting.

Sjors Provoost: 00:21:26

Okay, well that's fine.
It wasn't the best explanation probably, but you can find it on the internet.
But basically, it's kind of cool fancy math that lets you you know very efficiently communicate a lot of information.

Aaron van Wirdum: 00:21:37

Love it.
Okay so that was the high level explanation and then after that the mathematical explanation which I didn't understand but maybe some of our listeners did.

Sjors Provoost: 00:21:48

Probably only if they already understood it.

## Final Thoughts

Aaron van Wirdum: 00:21:51

Next question.
You just mentioned embedding the filters into blocks.
Why is it not already the case?
To just put it bluntly.

Sjors Provoost: 00:22:00

First of all because it's a soft fork and we've talked about (how) soft forks are the kind of things you want to be very careful with.

Aaron van Wirdum: 00:22:07

But also because it's controversial.
Because why is it controversial?

Sjors Provoost: 00:22:10

Well, for, it's probably for several reasons, but one reason would be how easy do you want to make it for people not to verify the whole chain.

Aaron van Wirdum: 00:22:18

Even if you're using this Neutrino solution just like the specific solution which we discussed at first, you're still not getting full security.
You're still trusting hash power as I've mentioned in both cases.
So you're trusting that at least a majority of miners isn't lying to you, essentially.
So then the question is, okay, we can make it very easy to run light clients, but do we actually want to make it very easy for people to run light clients because that way they're all going to trust on miners and maybe that's not such a good idea in the first place.

Sjors Provoost: 00:22:55

Exactly.
And there's kind of two forces where people are drawn to.
On the one hand, you could say, well, if it's difficult to run a light client, maybe more people will run a full node on a good computer.
But there's another attracting force that will just get people to use custodial wallets or some other thing.

Aaron van Wirdum: 00:23:11

Yeah, or not Bitcoin at all.

Sjors Provoost: 00:23:13

Exactly.
And it's hard to say, and in the long run, maybe it's different.
Maybe in the short run, by supporting this, you get lots of mobile adoption of people who at least, you know, use Bitcoin, at least check the headers, rather than check absolutely nothing.
But maybe on the very long run, that doesn't happen.
Now, in the longer run, we have Moore's Law.
So if the block size doesn't increase, and if networks and computers do get better, then maybe in a couple of decades, I think Luke Dashjr did a calculation on it, maybe in a couple of decades, it becomes real practical to run this thing on your phone.

Aaron van Wirdum: 00:23:46

I guess this would also assume Moore's Law holding up, right?

Sjors Provoost: 00:23:51

Yeah, or at least somewhat holds up.
Otherwise it takes even longer.

Aaron van Wirdum: 00:23:56

We could also decrease the block size limit as Luke suggests, and that way it would be shorter that that way we could use full nodes on our phone sooner.

Sjors Provoost: 00:24:07

I don't know if that's worth having a giant civil war over (that) though.

Aaron van Wirdum: 00:23:56

I think only Luke thinks that, well not just Luke there's a couple more people but it's probably not gonna happen.

Sjors Provoost: 00:24:20

So this goes back to our Utreexo episode where we discussed another way to verify blocks that takes less RAM and one particular advantage of that approach is that you could sync a note on your computer and then just have a QR code on your computer because you trust your own computer.
You scan it with your phone and boom, your note on your mobile phone is synced.
So that gets rid of the initial sync problem.
And this Utreexo technique allows you to work with very little RAM, which probably means that you can sync your phone on Wi-Fi and it'll be fast and then maybe you use some of these light client techniques if you're outside doing something.
So when you're outside you make a payment or you receive a payment and you kind of trust it, but when you get home, you can immediately see if something went wrong.

Aaron van Wirdum: 00:25:06

Yeah.
So the episode is short.
Neutrino compact side block filters.
They're new type of light clients that offer more privacy.
They are being used in Lightning wallets, but they're not specifically for Lightning wallets.
Are they used in normal light wallets by now?

Sjors Provoost: 00:25:23

I don't know.

Aaron van Wirdum: 00:25:24

I don't think so.

Sjors Provoost: 00:25:25

I haven't kept track of new normal light wallets, but I guess most of them are Lightning wallets nowadays, the new wallets.
Aren't they?

Aaron van Wirdum: 00:25:33

New wallets, sure, but I think Electrum, they would be interested to maybe implement it as well, but I don't think they have yet.

Sjors Provoost: 00:25:41

That might be worth a brief mention too.
The third solution that people are using is Electrum.

Aaron van Wirdum: 00:25:46

Yeah, that is another sort of in-between solution.

Sjors Provoost: 00:25:49

Yeah, as far as I know Electrum will just say here are my addresses give me transactions and then it will get SPV proofs.
So you get less privacy than Bloom filters but we already discussed that the privacy might be zero, but you do get the same security in terms of proving that these transactions are real.
And the same lying by omission and the same problem with potential spy nodes.
Yeah, I guess that's all we've got here.

Aaron van Wirdum: 00:26:12

I think so.

Sjors Provoost: 00:26:14

In that case, thank you for listening to The Van Wirdum Sjorsnado.

Aaron van Wirdum: 00:26:17

There you go.
