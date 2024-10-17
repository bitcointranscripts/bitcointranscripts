---
title: Bitcoin Core 0.21.0
transcript_by: Bitc0indad via review.btctranscripts.com
media: https://www.youtube.com/watch?v=kM4912dv39o
tags:
  - bitcoin-core
  - anonymity-networks
  - eclipse-attacks
  - compact-block-filters
  - signet
  - descriptors
speakers:
  - Sjors Provoost
  - Aaron van Wirdum
date: 2021-01-21
episode: 24
aliases:
  - /bitcoin-magazine/bitcoin-explained/bitcoin-core-v0-21
---
##  Intro

Aaron van Wirdum: 00:01:35

Live from Utrecht, this is The Van Wirdum Sjorsnado.
Episode 24, we're going to discuss Bitcoin Core 21.

Sjors Provost: 00:01:46

Hooray.
Well, 0.21.
We're still in the age of the zero point releases.

Aaron van Wirdum: 00:01:51

Yes, which is ending now.

Sjors Provost: 00:01:53

Probably yes.

Aaron van Wirdum: 00:01:54

That's what I understand.
The next one, the 22 will actually be Bitcoin Core 22.

Sjors Provost: 00:01:59

That's what it says in the master branch right now but you know until there's a release somebody could come out and you know change it back all right well anyways it's gonna be yeah 22 will be the next version.

Aaron van Wirdum: 00:02:10

Yeah so this one is still called Bitcoin Core 0.21 and it was released exactly a week ago when we're recording?
No, less than a week ago.
Anyways, last week and we're gonna discuss this new release and the new features in this new release.

Sjors Provost: 00:02:27

Yeah, there's some very cool features in there.

Aaron van Wirdum: 00:02:29

It's a big release.
There's a lot of new stuff in here.

Sjors Provost: 00:02:32

Yeah, and we're going to refer back to some earlier episodes where we talk about either the specific feature or at least the general area that this feature touches.

Aaron van Wirdum: 00:02:40

Yeah, we already discussed some of it.
So what we're going to do for this episode is we're just going to take the release notes and discuss each notable new future point by point for the most interesting ones.

Sjors Provost: 00:02:56

That's right.
And in the show notes you can find the full release notes which are very long.

Aaron van Wirdum: 00:03:01

Let's start.
Are you ready?

Sjors Provost: 00:03:03

I'm ready.

Aaron van Wirdum: 00:03:04

Let's go.
So first points.

## Mempool

Sjors Provost: 00:03:06

Yeah, so the first change, the mempool, right?
It used to be that when you have a Bitcoin Core wallet, you would be broadcasting transactions from your wallet.
And then after 15 seconds or so you would be broadcasting transactions from the wallet and you would just keep broadcasting it to your peers nearby.

Aaron van Wirdum: 00:03:26

Isn't it 15 minutes?

Sjors Provost: 00:03:27

Yeah 15 minutes.
So it would very frequently broadcast its own transactions because the wallet really wants to make sure that the rest of the world hears about its transactions.

Aaron van Wirdum: 00:03:37

Until it's included in a block, of course.

Sjors Provost: 00:03:40

Exactly.
The problem with that is it's not very good for privacy.
Because if you can pinpoint which node is constantly repeating a transaction, then that suggests that that's the node that created it.

Aaron van Wirdum: 00:03:51

Yeah, it makes it very obvious which addresses, which inputs originate from which node, which is bad for privacy, because a node can be tied to an IP address and an IP address to an identity and so forth.

Sjors Provost: 00:04:03

Exactly.
So the long-term goal here, which has not been achieved in this specific change, but we always do little micro steps.

Sjors Provost: 00:04:11

The long-term goal is to get to a place where the node will just treat its own transactions, its own wallet transactions, just like it would transactions from another peer.
So it will not prioritize its own transactions.
And there's some downside to that because you have to keep your wallet open probably a little bit longer to make sure that it does get broadcast.
But yeah, then it would be indistinguishable.
So I think one of the long-term goals is to say, we're going to wait until the wallet transaction fee is close to what it would be for the next block, because you can order transactions by fee.

Aaron van Wirdum: 00:04:45

Yeah, I think what you're trying to say is that right now this rebroadcasting is done blindly while in the future the plan is to actually see if the transaction should have been included in a block by now based on the fees and only if that's not the case will it rebroadcast the transaction and it will do so for any transaction the node has seen not just for its own transactions.

Sjors Provost: 00:05:08

Exactly and this also creates a better separation between because then you know Bitcoin Core is a node which has a mempool and it's a wallet and you know this dealing with mempools should be done by the node, and it shouldn't be done by the wallet.
So there's a lot of process separation going on under the hood there.

Aaron van Wirdum: 00:05:25

Yeah, but this, what we're describing right now, is actually not included in Bitcoin Core 21 right now.
We've seen one micro step towards this in Bitcoin Core 21.

Aaron van Wirdum: 00:05:26

So what is this micro step?

Sjors Provost: 00:05:36

If I understand correctly, the micro step is that it's going to broadcast it once a day instead of every 15 minutes.

Aaron van Wirdum: 00:05:42

I think that's right.
It just does it less often.
So there's a bigger chance it will have been included in a block by then, which means it's never going to rebroadcast.

Sjors Provost: 00:05:52

And you need to spy on a node a lot longer.

Aaron van Wirdum: 00:05:54

Yeah, exactly.
So it's a benefit for privacy.

Sjors Provost: 00:05:58

Yeah, I would say so.

Aaron van Wirdum: 00:05:59

And it's a small step towards a bigger plan.

## Tor Version 3 Support

Aaron van Wirdum: 00:06:02

Okay, next one.
Oh, we should mention as far as the mempool stuff, we've discussed this in episode 19.
That's in more detail for listeners who want to go back a couple of episodes and hear more about this.
Okay, next point is Tor version 3 support.

Sjors Provost: 00:06:20

Yeah, which we talked about in episode 13 in quite a bit of detail.
So the quick version is Tor has been improved, this is version 3, Bitcoin Core now uses that.

Aaron van Wirdum: 00:06:31

That's the very short version.

Aaron van Wirdum: 00:06:33

And I think that's good enough for now.
So yeah, episode 13 for anyone who wants to hear more.

Sjors Provost: 00:06:38

Right, because this also includes a new way to gossip addresses.
So that's, you know, that's actually a bigger change.

Aaron van Wirdum: 00:06:44

I mean, the important thing is that I think a year from now, if I'm recalling correctly, if you want to use Tor in a year from now, you actually do need to have this version 3 support, right?

Sjors Provost: 00:06:57

That's also my understanding, yeah.
Tor is still centralized, So there's somebody in charge who can say, okay, next year, you can no longer use version 2.

Aaron van Wirdum: 00:07:04

Right.
So now Bitcoin Core supports version 3, which means it's compatible with Tor even a year from now.

## Anchors - Eclipse Attacks

Sjors Provost: 00:07:15

Anchors.
It's a new file, but more importantly, we talked in episode 17 and 18 about eclipse attacks, how a node can be sort of isolated from the rest of the network.
And one of the countermeasures that we talked about back then is that when the node restarts it should remember at least some of the nodes it was previously connected to and that's what these anchor connections are.
So before your node shuts down it saves, or I guess it regularly saves, two of the nodes that it's connected to currently, namely nodes that it's only exchanging blocks with, so very low bandwidth.
And then when it starts up, it's going to read that file and it's going to connect to them again.
And we explain a lot more about that in those episodes.

Aaron van Wirdum: 00:07:55

Yeah, I think especially episode 17.
Yeah, both 17 and 18, I think most of this specific change was in episode 17.
So this was included in Bitcoin Core 21 as well.
So Eclipse attacks are now harder to pull off against Bitcoin Core 21 nodes.

## BIP-157 "Neutrino Filters"

Sjors Provost: 00:08:18

The next point is BIP-157, also known as neutrino filters.
We have not talked about that yet, so we can briefly explain it.
There are lots of mobile wallets out there, especially for Lightning, that don't want to download the entire blockchain.

Aaron van Wirdum: 00:08:34

Yeah, or just Lite wallets in general.
They don't have to be mobile, just something that doesn't download and verify the entire blockchain.

Sjors Provost: 00:08:41

Yeah, though I think the number of excuses you have to run a Lite wallet outside of a mobile situation are reduced.

Aaron van Wirdum: 00:08:48

I mean, a lot of people don't feel like waiting for two days for the whole thing to sync.

Sjors Provost: 00:08:53

Yeah, that's true for the initial experience.

Aaron van Wirdum: 00:08:55

I mean it's a bad idea or you know definitely not preferable but that would be the reason.

Sjors Provost: 00:09:01

Yeah, so what these filters do is they instead of you instead of downloading every block you download these filters which are much smaller than a block and then you can take your own list of addresses and run your own list of addresses against that filter And the filter will tell you whether or not there's something in the block pertaining to your addresses.

Aaron van Wirdum: 00:09:20

Yeah, or at least possibly.

Sjors Provost: 00:09:22

Yeah, there can be some false positives.
So you might get a list of a thousand blocks that you need to download, and maybe of those thousand blocks only a hundred actually contain your transactions.
But that's better than downloading all 666,666 plus blocks.

Aaron van Wirdum: 00:09:36

Yes, we made that milestone this week.

Sjors Provost: 00:09:39

Yeah, exactly.

Aaron van Wirdum: 00:09:40

That's why you remember the exact number.

Sjors Provost: 00:09:42

Precisely, it's very hard to remember.
There are lots of trade-offs when it comes to these filters, so I think we should go into that for another episode.
It's not enforced by consensus, so you're kind of trusting that the list is real.
Let's say the list gives you a bunch of nonsense results and you start downloading those blocks and you don't see what you're expecting, well then you know that whoever gave you those filters was lying to you.
But it gets a little complicated.
So we'll talk about that some other time.
But it's there and it was already used in the wild a lot, especially by the mobile lightning wallets.
So far there was only specialized nodes that would serve that, usually running BTCD.
And now, you know, every Bitcoin Core wallet can do it.
Yeah, if you turn it on.

Aaron van Wirdum: 00:10:22

Yeah, so just to be clear, the thing that's new in this Bitcoin Core 21 release, I'm just gonna call it Bitcoin Core 21, Not Bitcoin Core 0.21.
Anyways, what's new here is that I think previous Bitcoin Core release could already create the filter and now in this Bitcoin Core release it can share it over, I guess, the peer-to-peer network, right?

Sjors Provost: 00:10:44

That's correct, yes.

Aaron van Wirdum: 00:10:45

That's what's new.

Sjors Provost: 00:10:46

Yeah, the filter has been around there.
So as usual, you have this filter but you can't really use it.
And now you can use it.
Next one?

Aaron van Wirdum: 00:10:53

Yeah, so we'll get back to this in another episode.
I think this is the short version of it.

## Signet Signup

Next point.

Sjors Provost: 00:11:00

Signet.

Aaron van Wirdum: 00:11:01

Signet.

Sjors Provost: 00:11:01

Which we discussed in episode 10.

Aaron van Wirdum: 00:11:04

Correct.

Sjors Provost: 00:11:04

In great detail.
But the very short version is, it is like testnet, but heavily centralized.
And everybody can make their own if you want to.
And it's awesome.

Aaron van Wirdum: 00:11:16

Yeah, what it does is it creates a Bitcoin blockchain in a way, just like testnet is just sort of a copy of the Bitcoin blockchain.
Same rules and same things apply, it's just there for developers to test new stuff on, to test new software on without the risk of losing coins if there are bugs and these kinds of things.
The problem with the testnet is that because it's so similar to the Bitcoin blockchain it depends on hash power but without any economic incentives to actually keep the way secure or stable in any way.
The testnet can be very insecure or no not as well insecure and more importantly unstable.

Sjors Provost: 00:11:57

Yeah unstable especially because there might not be any blocks and then after 20 minutes there's like lots of blocks.
Yeah.
It's just a mess.
You can have very large reorgs.
It's not fun to develop against it and although when you develop software you should make it very robust, you have to deal with edge cases that really make no sense on the real Bitcoin network.
So you're kind of wasting your time.

Aaron van Wirdum: 00:12:19

Right.
So yeah, SIGNET is like a testnet, except that Bitcoin blocks need a valid signature.
From whoever is running the SIGNET.
And that person is making sure that the test network is somewhat stable.
So it's completely insecure.
This is not how you want to design actual Bitcoin, because it depends on the trusted third party, but because it's just for testing anyways, it's fine.

Sjors Provost: 00:12:45

Yeah, and although there's just two people who can sign it, that doesn't really matter because everybody can make their own SIGNET with their own rules.
And you can have a 15 out of 15 multi-SIG, or you can make it everybody can sign it.
It's probably a bad idea.
But the centralization part is solved by just having as many as you want, and it's worth nothing.

Aaron van Wirdum: 00:13:04

So this was included in Bitcoin Core 21.
What does that mean exactly, to have it included in Bitcoin Core 21?

Sjors Provost: 00:13:11

Well, it means that you can start Bitcoin Core with the `-signet`, just like you can start it with `-testnet` and your icon will have a nice different color and there's a faucet out there that you can go to and you can get signet coins which you get by the dozen, I think, so it's nice.
The other thing that's included is taproot.

Aaron van Wirdum: 00:13:36

Right yeah okay.

Sjors Provost: 00:13:38

And taproot is active on Signet.

Aaron van Wirdum: 00:13:41

Yeah so we now have taproot on Signet.

Sjors Provost: 00:13:43

That's right.

Aaron van Wirdum: 00:13:44

Obviously this is meaningless for regular users, this is just for developers, just for testing their software.

Sjors Provost: 00:13:51

Exactly, but the main plan was to have the taproot code inside of Bitcoin Core, unactivated, but just there so people can find bugs in it and can play with it.

Aaron van Wirdum: 00:13:59

Which is also the case, it's in there now.

Sjors Provost: 00:14:02

Exactly, so it's nice because normally you would have the code of a soft fork in there and you could theoretically play with it but it's not very clear how you would do that but now it's very clear because you can use it on Signet and the nice thing about Signet is that the rules can be changed anytime because there's you know two miners that can centralize decide to just enforce different taproot rules if the taproot spec is changed because it's not final until it's live.

Aaron van Wirdum: 00:14:29

Yeah, well it's kind of final.
The idea is that from here on out, it shouldn't be changed anymore, I think.
That's why it's included in the code in the first place.

Sjors Provost: 00:14:38

Yeah, I think you'd see it as a release candidate.

Sjors Provost: 00:14:41

Because even if taproot activates on mainnet in the future with a new version of Bitcoin Core, this old version of Bitcoin Core won't do anything with that.

Sjors Provost: 00:14:50

So, even if the rules change now, there's no problem with your 0.21 node.
It will not get confused if taproot changes.
Of course, hopefully it doesn't.

Aaron van Wirdum: 00:14:59

But about that, so yeah, the taproot code is included in Bitcoin Core 21.
This also means that probably the next minor version of Bitcoin Core, which would be Bitcoin Core 21.1, well, Bitcoin Core 0.21.1, will have the actual activation logic for taproot.

Sjors Provost: 00:15:22

Hopefully, yeah, if all goes well.

Aaron van Wirdum: 00:15:23

That's kind of the plan, right?

Sjors Provost: 00:15:24

I mean, yeah, I think that's the tradition.
But you know, there's no centralized management team that decides what the plan is.
So it is what may happen.
But yeah, let's just say that's the plan.
That's the thing with an anarchistic system, right?
It's what we did the last time, but nobody can force any of the volunteers and developers to do it again until it's been done.

Aaron van Wirdum: 00:15:47

Isn't it time for you to take charge, Sjors?
I'm assuming that there will be a minor release which has a taproot activation in it.
It's just gonna be my assumption.

Sjors Provost: 00:15:58

I'm optimistic, but I have not followed any of the, we discussed taproot activation possibilities in episode 3 I believe and taproot itself in episode 2 or the other way around.

Sjors Provost: 00:16:09

And I have not followed the news since then when it comes to activation so I guess I'll just see when it activates.

Aaron van Wirdum: 00:16:15

Yeah there's more on that discussion indeed in episode 3 and taproot itself in episode 2.
All right, next point.

## BIP339 "WTXID"

Sjors Provost: 00:16:22

Yeah so we'll jump back in our little queue to BIP339 witness transaction id relay or WTXID so here's the thing a long long time ago before there was SegWit, transactions had a hash.
And this hash represented, you know, the entire transaction.

Aaron van Wirdum: 00:16:43

It was a transaction ID.

Sjors Provost: 00:16:45

Exactly.
But then we created SegWit.
And segwit added data to the transaction but the identifiers that we use for transactions are still based on what is in the transaction minus all the segwit stuff this is because old nodes don't don't see the segwit stuff

Aaron van Wirdum: 00:17:04

Yeah this was kind of why segwit worked to solve malleability because previously the transaction before segwit the transaction had all the transaction details how many bitcoins are involved where they going plus the signature and this was all hashed and this hash was a transaction ID.
However, it turned out that slightly different signatures could all be valid and therefore a signature could be changed in flight for example you send a transaction to the network someone on that network slightly changes the signature the transaction is still valid but all of a sudden the transaction ID changed because the hash changed because the signature changed.
So to solve that, this was a problem for things like Lightning.
So to solve this, SegWit separated the transaction details from the signature and the transaction details were still hashed to create the transaction ID and the signature was put in a separate part of a block, a segwit part of the block, and therefore malleability was solved.

Aaron van Wirdum: 00:18:16

But this meant that the signature was not part of the transaction ID at all.

Sjors Provost: 00:18:17

That's right, and that makes a lot of sense when you, for example, have something like Lightning or any sort of escrow system where you pre-sign a transaction to release coins.
You want to make sure that the transactions go in.
And so The transaction that releases the coins refers to the transaction that puts the coins in there.
So you don't want somebody to be able to change that transaction that goes in, because then you suddenly don't have a release transaction anymore and your coins are held hostage.

Aaron van Wirdum: 00:18:43

So what's this change now?

Sjors Provost: 00:18:44

What this change is, is not about how the consensus works, but it's how transactions are relayed between nodes.
So, when a node talks to another node, it says, hey, here's a bunch of transaction IDs, would you like the whole transaction for this thing?
And that's still referring to this pre-segwit transaction hash, also the on-chain transaction hash.
But this new change lets you gossip these transactions using the witness transaction ID, which does include the signature, I believe.
Now I don't know why that's useful, to be honest, but because I haven't read up on what exactly the BIP is saying.
I'm just saying that you can now gossip transactions based on, including the witness, which I guess could have some benefit.

Aaron van Wirdum: 00:19:27

Do you think this has something to do with potentially sharing a transaction with an invalid signature and therefore...

Sjors Provost: 00:19:41

That's my theory, because I should have read it, but my guess is that indeed you would send another node a transaction hash and they would ask for the transaction and you would give it a fake transaction because you would just add your own signature to it and it would just be nonsense.
And then the other node would say, okay, this transaction is dumb.
I'm just going to ignore that moving forward.
And then another node would give the real one, but this node is now rejecting it because it's already seen it and it thought it was fake.
So you want to prevent that.

Aaron van Wirdum: 00:20:02

Right and that's what this new change might solve is your speculation but neither of us is actually sure because we didn't read the BIP.

Sjors Provost: 00:20:10

That's right.
Read the BIP fellows.

Aaron van Wirdum: 00:20:15

And it's BIP which one is it?
339.

Sjors Provost: 00:20:17

Yes, I also know this was done before taproot because it has some sort of utility there too.

## RPC Changes

Aaron van Wirdum: 00:20:25

Next item is taproot which we've already covered.
So then the next item is a bunch of RPC changes.

Sjors Provost: 00:20:32

That's right.
If you look at the release notes, a lot of changes are about the RPC.
And we're not gonna mention them because they're not that interesting.

Aaron van Wirdum: 00:20:39

RPC stands for Remote Procedure Call?

Sjors Provost: 00:20:42

Yes.

Aaron van Wirdum: 00:20:42

What does that mean actually, Sjors?

Sjors Provost: 00:20:44

It basically means if you're running a Bitcoin node, then you can issue commands to it.
And if you're a desktop user, you would just click on buttons.
But if you're in the command line, well, you would type Bitcoin client, then some command.

Sjors Provost: 00:20:56

But if you are on the network, you probably want to send some JSON to it and get some JSON back from it over the network.
And that's what these RPC calls are for.
So you can send the commands over the network and get a response back.
And if you've built some sort of complicated server, you want to make sure nothing breaks.
And BitConcord is always very careful.
It tries not to make breaking changes in that RPC.
So, for example, a situation you might be in is you run a block explorer of some sort, and you have one little server machine that has a Bitcoin full node on it and we'll get to that actually with the CMQ explanation but I guess we'll transition to that.So you'll have one node that runs Bitcoin core on it and another that runs a database and another that runs the website because usually you know they try to split all these things up so the web server might ask the node questions like what is the current block height or you know what's in your mempool that that's done via RPC That might or it might say send a transaction to this person that's also done via RPC.
So that's all scripts and code so you want to make sure that your code is still doing what you think it's doing when you upgrade the node.
But which brings us to the next point ZeroMQ feature improvement.
So you can read in, if you find this interesting, you can read in the release note exactly what.

Aaron van Wirdum: 00:22:22

Is that one of the RPC changes?

Sjors Provost: 00:22:25

Well ZeroMQ is not actually RPC, but it's also a way to communicate.

Sjors Provost: 00:22:32

So with RPC you have the Bitcoin node is listening and you send a command to it and you get a response back.
That's how RPC works.
But in ZeroMQ it's push-based.
So what you're doing is the Bitcoin Node is constantly broadcasting and you can listen to that broadcast through a channel and so the broadcast could be every new block.
So then you're listening to a certain channel and you get the block as soon as the node sees it.
Or you can listen to transactions or I believe you can even listen to transactions at a certain address.
This might be useful if you have a block explorer with a live page where you're looking at an address and then the notes sees a new transaction on that address, it sends a message to your ZMQ to the web server and the web server sends a WebSocket message to the browser so your browser updates without having to hit the refresh button, something like that.

## Send RPC

Sjors Provost: 00:23:28

There is a new Send RPC by yours truly, which is cool.
It basically, if you want to send coins through the command line, I mean, you can do it with the graphical interface, but if you're, you know, the cool kids want to do it with the command line, it's very tedious.
You know, when the first version of Bitcoin Core came out, but it wasn't even Bitcoin Core.
I think you just had a command called send to address and you gave it an address and an amount and that was it.
And that's still out there.
But the problem is that command got expanded, but it doesn't have all the features you may want.
And at the same time, there were commands to create PSBTs that we talked about in an earlier episode.
Those commands were very powerful.
You could do all sorts of cool things to your transaction, including coin selection, for example, through the command line.
But it was very tedious because if you want to make a PSBT then you have to make it and then sign it and then finalize it and do a bunch of things.
So the problem was you had a very simple way to send coins with the very old Satoshi time RPC methods, just send to an address but you couldn't configure it.
Or you had a super powerful method that was extremely hard to use.
And so the new `send` RPC is easier to use and powerful.

Aaron van Wirdum: 00:24:41

And you made this?

Sjors Provost: 00:24:42

Yes, and it's been improved since.
It's especially useful if you're experimenting with newer features, like hardware wallet integration and stuff.
Then you want to experiment on the command line and then hopefully later do it in the GUI.

Aaron van Wirdum: 00:25:01

How is that going to take a side path?
What's going on with hardware integration, hardware wallet integration?

Sjors Provost: 00:25:07

It's very slow.
So I think I gave a presentation in 2019 or something.

Aaron van Wirdum: 00:25:14

In London?

Sjors Provost: 00:25:15

Yeah and Andrew Chow was on it as well.
And I mean the final picture we thought would be here now, or at least I was hoping for, but it's not.
But a lot of things have been done.
So part of the hardware wallet project was to get PSBT support.
That's pretty much done.
Part of it was descriptor wallets, which we'll get to next.
So that's been done and the thing I've been working on as a work in progress is a expansion of this send command in RPC that will let you talk to a hardware wallet directly from the command line and The second one is a graphical interface around that.
And those pull requests exist, they get a little bit of review, but they're not moving forward very quickly.
Eventually it might happen.

Aaron van Wirdum: 00:25:56

But it's still moving.

Sjors Provost: 00:25:58

It's still moving, and also there are great other solutions out there.
So there's the Spectre open source project which just runs a little web server on your own computer and then it magically talks to the RPC again with these RPC calls that we talked about and it creates wallets and it's very very nice very slick we wouldn't be able to get it that slick.
But if you can get more support inside of Bitcoin Core, it means fewer software that you need to download from places that you then need to trust.

## Experimental Descriptor Wallets and SQLight Support

Sjors Provost: 00:26:28

The next point is called experimental descriptor wallets and SQLite support.
So two things.
So descriptor wallets, I don't think we've talked about that yet.
So the general idea is that when Bitcoin Core started, it was just a single address type, pay to public key.
I think we did discuss that.
And then there was a new address format, pay to public key hash.
And so that was added to the wallet.
And then SegWit came along and pay to script hash came along.
And now there's the wallet is just a giant mess of backwards compatible things.

## The Descriptor Wallet

Sjors Provost: 00:27:02

Code that nobody understands.
And well, Andrew Chow has been at work at cleaning that up.
And one of the things that was added was the idea of the descriptor wallet.
The descriptor is something invented by Sipa.
And the idea there is that you describe what is in the wallet.
So you literally just write out, you start with this master key, and then you take the first derivation, you know, within BIP 42, and you take the second derivation or whatever, and then it's slash star, and then if you write down just those descriptors you can recover your addresses.

Aaron van Wirdum: 00:27:33

Yeah so this could be for example you have a bunch of multi-sig addresses and these are described as multi-sig addresses and then your hardware wallet addresses and then your playing addresses or whatever and these are sort of categorized you can easily categorize your different UTXOs your different coins.

Sjors Provost: 00:27:53

Yeah so for a hardware wallet is a nice example usually a hardware wallet will give you an xpub you know if you plug it in it can spit out an xpub and xpub is a way to derive multiple addresses.
And so a multi-sig address.

Aaron van Wirdum: 00:28:05

We did discuss that in, I think, one of the first episodes.
I don't have the number in front of me.

Sjors Provost: 00:28:12

Yeah, could be.
And basically, You can say, okay, here's a multi-sig address consisting of these three XPUBS and then what you need to do to these XPUBS to get the individual addresses.
So you can describe very complicated wallets.
And if we add mini-script support in the future, you can describe even more wildly complicated wallets that way.

Aaron van Wirdum: 00:28:32

Right.
So what's up with SQLite?

Sjors Provost: 00:28:34

SQLite is a new database format so the wallet itself is just a bunch of records essentially and right now it's sitting in Berkeley DB version 4 which is a 10 year old unmaintained piece of software which you know it's 10 years old and unmaintained so that's a problem and SQLite is a bit more modern it's still being maintained and it's very short so the total code for SQLite is not that large to review, and it is designed to be backwards and forwards compatible in sane ways.
So if a new version of SQLite comes out, you have pretty strong guarantees that it's still going to work.
And that If you save something in the new wallet, it's also going to work in an old version.

Aaron van Wirdum: 00:29:19

Yeah, I was just going to ask that.
So if you upgrade to Bitcoin Core 21, you're...

Sjors Provost: 00:29:27

Nothing happens.

Aaron van Wirdum: 00:29:28

Nothing interesting happens.
Nothing worrisome happens.

Sjors Provost: 00:29:31

No, if you already have a wallet it is not converted to descriptor wallets, it is not converted to SQLite, nothing happens.There are manual commands that if you like to you can do that, but we still consider both of these things somewhat experimental, So you probably don't want to do that.
But the goal in the future is that new wallets will be descriptor wallets and will be stored using the SQLite database.
And then, you know, more far into the future, there'll be an automatic migration tool or like at least some button that says, you know, you probably want to migrate this.
Right.
Then even further into the future when you start it up, it'll say, okay, I'm not going to start up, please migrate the wallet first using this tool or something.
And then later on it's like, please download an older version.
Now, I guess there'll always be a conversion tool because you want to be nice.

Aaron van Wirdum: 00:30:21

I like my backwards compatibility, Sjors.
Please keep that for me.

Sjors Provost: 00:30:25

Yeah, I guess it depends on how horrendous it is to keep all that old code around.
But I guess one thing we might end up doing is write just the code that's necessary to read one of those old Berkeley databases, no longer to be able to write it.
So you wouldn't need the whole library, you know we talked about libraries, we would just need enough to be able to read it.
But that's you know years and years probably.

Aaron van Wirdum: 00:30:48

I think we've made it to our last point.
It's a small one.

Sjors Provost: 00:30:52

Yeah, at the RPC level, you can now specify your fee in Satoshi per byte.

Sjors Provost: 00:30:58

Yeah, so it used to be Satoshi per kilobyte or BTC per kilobyte, some weird unit.

Aaron van Wirdum: 00:31:03

Something no one else used.

Sjors Provost: 00:31:05

Yeah, exactly, because now all the websites will use Satoshi per byte

Sjors Provost: 00:31:10

Yeah, the annoying thing about the standard that it was using before is if you type one because you intended one satoshi per byte, you're actually saying, I don't know, a thousand satoshi per byte, or some really obscene number that would be very expensive if you don't know what you're doing.
There is actually protection against that since a few years.

Aaron van Wirdum: 00:31:29

So that's changed to make it more consistent with the rest of the Bitcoin ecosystem.

Sjors Provost: 00:31:33

Yeah, and that's not yet in the graphical interface, but that's typically the next step.

Aaron van Wirdum: 00:31:38

Right.
So yeah, I noticed there were like 140 contributors to this release, something like that?

Sjors Provost: 00:31:43

Quite possible.

Aaron van Wirdum: 00:31:45

Maybe 130, 140, something around that number.

Sjors Provost: 00:31:48

Because we talked about the highlights, but if you look at the actual release notes and then at the bottom, there are so many super small changes that could be an individual contributor that just comes by.

Aaron van Wirdum: 00:31:59

Yeah, I just wanted to mention thank you to all these 130 or 40 or whatever it was contributors.
Thanks to everyone.
Thanks to you as well, Sjors.

Sjors Provost: 00:32:08

Thank you.

Aaron van Wirdum: 00:32:09

You're one of them.
What else?
How do people upgrade?
What do people do?

Sjors Provost: 00:32:12

Go to bitcoincore.org and download it and then do all the checks to make sure that you've got the real thing.

Aaron van Wirdum: 00:32:19

Yeah, like the signature verification stuff and these kinds of, well, I guess that's the main thing.

Sjors Provost: 00:32:25

Yes, yeah, I think that's it.

Aaron van Wirdum: 00:32:27

Yeah, and nothing else, right?
So Like we mentioned, this Berkeley DB to SQLite, that's unnecessary, you don't need to re-download blocks or anything like that.

Sjors Provost: 00:32:36

As a user, you just download the new version and life continues.

Aaron van Wirdum: 00:32:41

Nice, I like that.
I like life to continue.

Sjors Provost: 00:32:45

Alright, and thank you for listening to The Van Wirdum Sjorsnado.

Aaron van Wirdum: 00:32:48

There you go.
