---
title: Bitcoin Core 22.0 Explained
transcript_by: satstacker21 via review.btctranscripts.com
media: https://www.youtube.com/watch?v=xm3BjAKjCXM
tags:
  - bitcoin-core
  - hwi
  - anonymity-networks
  - bech32
speakers:
  - Sjors Provoost
  - Aaron van Wirdum
date: 2021-09-13
episode: 45
aliases:
  - /bitcoin-magazine/bitcoin-explained/bitcoin-core-v22-explained
---
## Intro

Aaron: 00:00:20

Welcome to Bitcoin Explained, the podcast with the most boring name in Bitcoin.
Hey Sjors.

Sjors: 00:00:27

What's up?
What's with the new name?

Aaron: 00:00:29

So We've rebranded our podcast.
What do you think?

Sjors: 00:00:33

Well, I think, you know, especially if you read it correctly, Bitcoin, explained.
I think it's an amazing name.
I think the problem was that a lot of people have no idea what the hell a Van Weerdam Shores Nado is.

Aaron: 00:00:46

Apparently, no one had any idea what Van Weerdam and Shoresnado means or even how to pronounce it so we decided to go for a new name.

Sjors: 00:00:54

Though I think if people listen to it long enough they'll know how to pronounce it but I think the problem is people who are not listening don't know how to pronounce it.

Aaron: 00:01:02

So from now on, we're Bitcoin, Explained.
Why is the comma so important for you?

Sjors: 00:01:07

It makes it sound more profound.
So if you just say, oh, I'm going to explain Bitcoin, whereas Bitcoin, Explained, you know, really says, okay, now You truly understand it.

Aaron: 00:01:16

Very profound.
So the first episode, we're just going to keep counting.
So this is episode 45 of Bitcoin Explained, previously known as Defend William Shures NATO.
And we're going to start off with the new Bitcoin Core release, Bitcoin Core 22.

Sjors: 00:01:33

That's right.

Aaron: 00:01:34

From now on it's not 0.22 anymore, it's just Bitcoin Core 22, right?

Sjors: 00:01:40

Yeah, highly undemocratically decided at some point to just change the numbering because people were asking when is version 1 coming of Bitcoin?
And we're like yeah we're just gonna skip it because it's always bad luck when you do that.

Aaron: 00:01:53

Right so from now on it's does this mean we're not in beta anymore Sjors?
Is that the big announcement?

Sjors: 00:01:59

No I think it means nothing I think it just means that we stopped having this zero prefix.

Aaron: 00:02:05

Basically, Bitcoin Core changed the name for the same reasons that we did, just to avoid annoying questions and make it more clear.
Is that it?

Sjors: 00:02:14

I guess.
I wasn't really there at the decision.
It just happened and nobody wanted to undo it.
So there we are.

Aaron: 00:02:22

Got it.
Well, at the point that we're recording this, the new Bitcoin Core release has not actually been released yet.
Bitcoin Core 22 has not actually been released yet.
But by the time this episode is released, then maybe Bitcoin Core 22 is released as well.
And otherwise, it will be released very soon, right?

Sjors: 00:02:41

That's right.
There's now a third release candidate out.

Aaron: 00:02:44

So that means basically any day now, at the point of recording at least.
And maybe, like I said, maybe it's out by the time this episode is released.
So anyways, we're going to highlight some of the improvements compared to Bitcoin core 21 essentially and bitcoin core 21.1. Was there a bitcoin core 21.2 as well?
I don't think so.

Sjors: 00:03:09

I think there's one in progress.

Aaron: 00:03:11

Right exactly yeah there's one coming as well.
So we're gonna give a short overview of the most notable changes, right?

Sjors: 00:03:22

Yeah, exactly.
So usually the last version digit, those changes are very small.
They're usually bug fixes and those kind of things.
So the release we're talking about now is a big one.

Aaron: 00:03:32

They're either very small or they're a protocol upgrade.

Sjors: 00:03:36

Right.
So in this case, it's a bit more complicated because it's small fixes and taproot that go into 0.21.1 and also probably in 0.21.2.

## Hardware Wallet Support in the GUI

Aaron: 00:03:47

So let's get to Bitcoin Core 22.
That's what the episode is about.
I think the main, the most notable change, the biggest change, and I think you'll agree with that because you worked on it, so you're biased, is hardware wallet support, the HWI, right?

Sjors: 00:04:06

I think that's a pretty cool change.
I don't know if it's the biggest change.
I'm definitely very happy with it.
Yeah, so basically if you download Bitcoin Core 22 and then also download HWI, which we talked about in episode 30, which is just a Python script that connects to all sorts of different hardware wallets essentially using their drivers.
Then I think you just have to change one setting which is to tell it where you put the HWI script and then once you've done that you just insert your hardware wallet you say to Bitcoin core give me a new wallet and it'll say "oh do you want to use a trezor, ledger whatever you've just inserted" and it'll just work to him like any other wallet except that your wallet your hardware device will now show on screen "hey do you want to prove this transaction" so that's pretty cool I think.

Aaron: 00:05:01

Right, but am I understanding you correctly that it does not work out of the box?
You can't only download Bitcoin Core 22, you also need to download the HWI.

Sjors: 00:05:11

Correct.

Aaron: 00:05:12

Which is a separate software package.

Sjors: 00:05:14

Yeah, It's a Python library and you know because it contains all the stuff from the hardware manufacturers and it communicates with USB so it is potentially a can of worms and so we don't want to put it in Bitcoin Core for everybody.
Maybe one day will be but I think it'll be a while because just including USB drivers into Bitcoin Core sounds a bit scary.

Aaron: 00:05:35

Right.
So for now it's like an add-on.

Sjors: 00:05:38

Yes.
But like I said, pretty easy to install.
You download it, put it somewhere, point to it, and that's it.

Aaron: 00:05:44

Hardware wallets were already supported by Bitcoin Core though, right?

Sjors: 00:05:48

Indirectly, yes.
You could use HWI already, but you had to use it from the command line yourself.
And actually HWI also came with a graphical tool, so you could actually use it somewhat you know reasonably, but I think this is much easier now.
It's just right into the Bitcoin Core interface.

### Bitcoin Core Interface

Aaron: 00:06:08

Yeah, no one uses the command line, sure.
So only a couple of Bitcoin Core developers themselves use that stuff.
Regular people.

Sjors: 00:06:16

A surprising number of Bitcoin Core developers use the graphical interface too and it's especially because coin selection is just a lot easier to do if you want to decide which coins you want to spend using a graphical interface you just click on them whereas with a command line it's horrible, you have to copy paste the transaction hash and the identifier, etc.

### Which Hardware Wallets are Supported

Aaron: 00:06:37

Right.
So, which hardware wallets are supported?

Sjors: 00:06:41

Off the top of my head, whatever HWI supports.
So, that is the Trezor, the Ledger, the KeepKey, Coldcard.
I don't know.

Aaron: 00:06:55

Maybe some more.

Sjors: 00:06:57

Yeah, I was just opening the support matrix.
There's a whole list of it.
Bitbox.

Aaron: 00:07:04

Okay.
Is that the only hardware wallet related change in the Bitcoin Core 22?

Sjors: 00:07:11

I mean, that's a big enough one, right?
And I'm sure in next versions, there'll be some more incremental improvements, like being able to bump the fee for example would be nice, that sort of stuff.
Multi-sig would be very nice if it was possible to do that directly.

Aaron: 00:07:26

Yeah, and for now I think it's just one hardware wallet per Bitcoin Core wallet, right?
You can't do two out of three or that kind of nifty stuff yet.

Sjors: 00:07:37

No, exactly.
Multi-signature support is not there yet.
And that just is a whole can of worms in general, right?
Multi-signature support with Bitcoin Core is still not very easy.
It does, it's all possible, but it's, it requires some manual work.

Aaron: 00:07:51

Let me think.
Should we say something else about hardware wallets?
Or is that about it?
But there is also RPC.

Sjors: 00:08:00

No, right?
But yes, that is indeed that you can do it via the GUI or the command line.
I don't know how important it is to do that.

Aaron: 00:08:09

Right, so hardware wallet integration into Bitcoin Core has been a long process, has been an incremental process And now for the first time with Bitcoin Core 22, we have hardware wallet support in the GUI, which basically means we for the first time have hardware wallet support for regular users.

Sjors: 00:08:26

Yeah, exactly.
I think it's still marked experimental.

Aaron: 00:08:29

Great.

## I2P Search

Aaron: 00:11:56

Next up, I2P.
What is I2P?

Sjors: 00:12:01

I don't know.
There's a lot of articles on the internet that say what is the difference between I2P and Tor and then those articles start by saying many people ask what the difference is between I2P and Tor and then they proceed in some really convoluted language.
But basically, it is a Tor-like system that is somehow different.
But the good news is that Bitcoin Core can now use it.

Aaron: 00:12:24

Exactly.
It's a privacy layer on top of the internet, a lot like Tor.
Tor uses onion routing, so messages are encrypted and routed across different users that all have a sort of encryption step on the way.
And therefore you gain privacy.
I2P is similar and the differences are pretty subtle.
It seems that I2P has a more distributed way of mapping the network.
I don't think either of us knows the details of how that works exactly, but it's more distributed than with Tor.
And somehow, I2P is more dedicated to...
What's it called?

Sjors: 00:13:20

Well, it's internal, so it's more difficult to get out of I2P, whereas in Tor, it's very easy to use the original internet in addition to dedicated darknet, or not darknet, but onion sites.

Aaron: 00:13:33

Yeah, that's what I was going to say.
I2P is more dedicated to hidden services.
So if you stay within the network I2P is sort of specialized for that, where Tor is more usable if you want to you know send stuff to the regular internet to the web.

Sjors: 00:13:52

That's what we've read in random Google searches, so we wouldn't know.

Aaron: 00:13:57

These appear to be the subtle differences.
So what does this have to do with Bitcoin Core?

Sjors: 00:14:00

Well, so this kind of ties back into an earlier episode.
So first of all, Bitcoin Core 22 supports that network.
So if you are interested in using it, you can.

Aaron: 00:14:11

Yeah, so you can now connect to the Bitcoin network through I2P.

Sjors: 00:14:15

Yeah, and so what we talked about in episode 13, back when it was still called the Van Wirdum Sjorsnado, what we talked about then is that Bitcoin Core added support for Tor version 3.
And the other aspect we talked about then was more generally how does Bitcoin Core tell other nodes which nodes to consider.
So there's basically a message where you can say, hey, here's a bunch of addresses for other nodes.
And what we explained in an episode is that there's now a new message that makes it easier to announce nodes of various kinds to other nodes including to say okay here's a list of Tor version 3 nodes or here's a list of IPv6 nodes or here's a list of I2P nodes.
And this mechanism is now more generic, which means that in the future if other networks like this come about, some other anonymity network, maybe internet over the lightning network, who knows, it'll be much easier to add support for that, because we'll have a way to gossip those nodes around.

## Tor Version 3

Aaron: 00:15:23

Speaking of these kinds of topics, you already mentioned Tor version 3.
Tor version 2 has now been fully deprecated, right?

Sjors: 00:15:33

Yeah, it was essentially already the case because in the previous version of Bitcoin Core, if it started up, it would immediately switch to Tor v3 and would just not use your Tor v2 settings.
But you could still go back if you did something manually.
And now I think all that code has been stripped out because I think Tor version 2 is more or less shut down.
Because remember, Tor is centralized in that way.
There's somebody out there that can say, okay, this thing no longer works.

Aaron: 00:16:01

Right.
Yeah.
We've discussed this in one of the previous Bitcoin Core release episodes, I think, where the switch from Tor version 2 to version 3 was happening.

Sjors: 00:16:12

Yeah, we did that in the same episode, episode 13.

## Taproot 

Aaron: 00:16:15

Right, got it.
All right, so these are two changes we've mentioned, hardware wallet and I2P support.
You've also mentioned at the start of this episode this difference between major releases and minor releases, where minor releases are usually either bug fixes or they include protocol upgrades.
Now, the last minor release did include a protocol upgrade, namely Taproot, which also means that this is the first major Bitcoin Core release that has taproot support.
Yep.
And we can find this taproot support in a couple of places in this upgrade, right?

Sjors: 00:16:51

Yeah.
Of course, the most important part is all the taproot consensus stuff is in here.
Obviously, the activation code, the speedy trial, all that sort of stuff.

Aaron: 00:17:01

If you haven't upgraded the minor release yet, Taproot is going to activate in November, so this would be a good opportunity to actually upgrade if you want to enforce the new Taproot rules, which you should do if you want to, you know get the maximum security that a full node promises to offer.

Sjors: 00:17:18

Yeah, but the good news is that if you, you know, if you really, really liked version, say 0.21.0, and you don't want to change too much, then you could just go to 0.21.1 and you'll enforce taproot.
But as we'll talk about now, I think version 22 has a few more things on top of this, the consensus enforcement.

Aaron: 00:17:39

Yes.
So what does Bitcoin Core 22 include taproot wise?

Sjors: 00:17:44

Well, it includes some very rudimentary support for wallet, taproot wallets.
Basically you're just a single public key type of wallet, which doesn't make taproot that interesting.
And slightly more generic things where you can have one private one yeah one key per taproot branch so remember in taproot you have a main key and you also have scripts that are sitting in a tree.
And so there's now support for those scripts in a tree.
However, as far as I understand it, those scripts can only be of the super simple type, namely a public key.

Aaron: 00:18:27

Right.

Sjors: 00:18:28

So, they're not very interesting yet, but this is how it goes with Bitcoin Core.
We add little increments at a time.

Aaron: 00:18:35

Yes, we've mentioned that a couple of times.
Bitcoin Core is improved slowly but surely.
Every half year there's a new release, so it's not necessarily that all the taproot stuff comes at the same time.
It's just step by step.
And now the first step is to have very basic taproot support, which essentially comes down to taproot support for regular transactions.
Yeah.
So none of the fancy smart contract stuff, but you can use a Taproot type of address and transaction to receive funds.

Sjors: 00:19:07

Yeah, in principle, but again, it's not even on by default.
You actually have to manually make it happen.
So probably for version 23, it'll automatically do the Taproot things.

Aaron: 00:19:19

Yeah.
I think another way to put it short, if you, if you agree with me, is that there's no actual benefit yet in using Taproot in this Bitcoin Core release, but it's possible to use it for sort of regular transactions, right?

Sjors: 00:19:31

Yeah, exactly.
So you can if you really know what you're doing.
And other than that, it's probably useful to have it in there anyway for people who want to test things on signet or testnet or you know that sort of stuff.
Because we want other developers to keep working on Taproot.

### Taproot descriptors

Aaron: 00:19:44

Yeah, so this was basically Taproot addresses we were discussing.
A little bit deeper under the hood, you have the taproot descriptors.
What are taproot descriptors?

Sjors: 00:19:55

Yes, so a descriptor is a way to say I want to generate a series of addresses, basically.
So instead of saying, okay, our wallet is one address, you say, okay, our wallet starts with the root private key, and then it does a bunch of BIP32 style derivations, and then it says, okay, give me the address number 15 or 16 or 17.
And descriptors allow you to describe that.
And now they also let you do that for Taproot.

Aaron: 00:20:25

I think descriptors also allow you to sort of categorize your funds into specific types of funds, right?
So you can say, these are all my Taproot funds, locked in Taproot stuff, and these are all my Multisig funds, like the Multisig stuff, sorry, Multisig addresses.
And the descriptors sort of let you label these, right?

Sjors: 00:20:48

Yeah, because they describe in a sort of a human readable form, what your addresses are, how to get to your addresses.
Yeah.
You can say, I have one descriptor for my SegWit addresses.
I have one descriptor for my Taproot addresses.

Aaron: 00:21:00

Yeah.
So now there's a Taproot descriptor.
So that's another sort of small step in the Taproot process for Bitcoin Core.

Sjors: 00:21:07

Well, in fact, that is what the wallet has support for.
So you can add Taproot descriptors to the wallet now, but you have to do it yourself.

Aaron: 00:21:15

Right.
So, hardware wallet support in the GUI, I2P support, Taproot.

Sjors: 00:21:23

The other thing is there's a little safety measure there.
Well, two things.
So there's a little safety measure there that you cannot add Taproot to a wallet on mainnet before it activates.
Just to make sure you don't have people sent to your taproot address before it activates because then you lose all the coins.
And the other thing is that there's now some...

Aaron: 00:21:45

Wait, wait, Wait, why would you lose the coins?
It just means you can't spend the coins, right?

Sjors: 00:21:48

No, if you're receiving money on a Taproot address before Taproot activates, then that's anyone can spend.
So yeah, that's a bad idea.
So this is a little basically anti-food gun measure.

Aaron: 00:22:03

Got it.

### Support for bech32 Addresses

Sjors: 00:22:04

And the other upgrade is that there's now some support for BECH32M.
We talked about, I think, BECH32 addresses in general and that for Taproot there's a small change to it.
The episode 28 we talked about addresses.

Aaron: 00:22:21

I remember that.

Sjors: 00:22:22

And that's, yeah, so to the human eye, they'll look identical.
They start with "BC1", but there's some subtle changes in the checksum that you can safely ignore, but it does have to be built.

Aaron: 00:22:34

Right.
That's also included in this release and also related to Taproot.

Sjors: 00:22:39

Exactly.

Aaron: 00:22:40

All right.
Was that all Taproot?

Sjors: 00:22:42

I think so.

## Update to `testmempoolaccept` RPC

Aaron: 00:25:25

So yeah, hardware wallet support, I2P, Taproot.
And then The fourth notable change that we're going to discuss is there's an update to `testmempoolaccept`.
Or is `testmempoolaccept` newly included?

Sjors: 00:25:43

No, `testmempoolaccept` has been around.
So `testmempoolaccept` is an RPC method.
The RPC is a way to programmatically talk to a node, maybe from a Python script or just manually.
And what `testmempoolaccept` does is it takes a transaction, and it says, yeah, If you were to broadcast this transaction, it would be valid.
Or it would say, no, this transaction is invalid because the signature is wrong.
So it's just a way to check if a transaction is correct before actually sending it.
And one of the things I believe it checks against is whether the fee is high enough to even make it into your mempool, because your mempool might be very full and if it's too low it'll say no fee is not high enough.
But one of the restrictions that comes with that, and we talked about this in episode 19, about package relay and other things.
One of the restrictions is that it evaluates these transactions one at a time.
So you might have one transaction that pays a very low fee and then the next transaction actually spends that first transaction and pays a huge fee but you won't get through because the first transaction is immediately tossed away.
And so the longer-term goal that we talked about in this episode is that these transactions can be analyzed as a package in various places so by the mempool itself and in the peer-to-peer messaging protocol.
And so this adds a tiny, tiny, tiny step, which is that now you can give this command multiple transactions.
It's still going to evaluate them one by one.
But again, this is baby steps.

Aaron: 00:27:20

Yeah, if I have to jog my memory, the point here was that for some protocols like the Lightning Network, you might need to use a trick called child pays for parent, which means that you create a new transaction that has a high enough fee to essentially pay for a previous transaction.
That a transaction is sort of stuck in the mempool or whatever.
Well, that's where it will be stuck.
To speed it up, you create a new transaction that spends the same funds, include an extra high transaction there, and that's how you sort of get them both unstuck.
That's how you get the first transaction unstuck, which you sometimes actually really need to do with some, you might be in a rush, in a hurry to actually do that in context of protocols of the Lightning Network, because sometimes you actually need transactions to confirm before some kind of time lock runs out.
And then the problem is that while this works for getting a transaction actually included in a block, it doesn't necessarily work for getting a transaction into a mempool.
Sometimes you need to get a transaction unstuck, but that transaction doesn't even make it into the mempool, which means you also can't get it unstuck with child pays for parent (CPFP).
And then the solution there would be to have the network to broadcast packages of transactions over a network.
So in the same way that a package of transactions can sort of be confirmed by a miner all at once because the miner calculates the total fee, that sort of same calculation, the total fee calculation, would come to apply for what regular nodes put in the mempool.
That's sort of the long-term upgrade that's being worked on, and this is a very small step in that process, right?

Sjors: 00:29:17

Yeah, and for Lightning, it's a way to reduce fees, right?
Because right now when you, well, to reduce fees in some cases.
So right now with Lightning, you have to pre-sign a transaction, which means you have to decide in advance what the fee is going to be for that transaction.
And so these fees have to be taken some sort of worst case scenario into account.
Whereas with this change, eventually the hope is that you just set no fee on it, on the conflicting, on the backup transaction that you have in Lightning, and you just send it on the blockchain and then some, you know, whoever really needs this transaction will just pay the extra fee that is needed right then as a child pays for a parent.
So it's a useful feature, but yeah, there's some problems with relay when the mempool is very full.

Aaron: 00:30:07

Got it.
Yeah, that makes sense.
So this `testmempoolaccept` is a small step in improving that process.
Another incremental improvement.

Sjors: 00:30:17

Exactly.

Aaron: 00:30:18

Alright, so one more to go, Sjors.

## Update to `addmultisigaddress` RPC

Sjors: 00:30:21

Maybe two actually.
I have some other amount.
One small one is `addmultisigaddress`.
I think we talked about that.
Well, basically the multi-signature support inside the RPC.
You can now use it for 20 public keys instead of 16.
Which is something that SegWit supports.

Aaron: 00:30:43

Right.
This is for Bitcore Core users that want to receive a transaction, right now you can create a multi-sig, but it's limited to 16 public keys, is that right?

Sjors: 00:30:57

Yeah, and I think the reason is that the legacy addresses could only do 16 P2SH and SegWit can do 20, but the Bitcoin Core couldn't support it yet.

Aaron: 00:31:08

Right.
So now Bitcoin Core users can receive transactions on 20 key multisigs.

Sjors: 00:31:15

Yeah, it's not a consensus change.
None of the rules changed.
It's just that the Bitcoin Core wallet can now do a little bit more.

Aaron: 00:31:21

Yeah, it was always possible according to the consensus rules, but not according to Bitcoin Core yet, until now.

## Support for NAT-PMP

Sjors: 00:31:27

Yeah.
So another thing we can mention that is, I think, fun is support for NAT-PMP.
Basically when you have a router like if you're running a node at home and you usually have a router that will cause your node to not listen to anything else.
Your node can connect outbound but other nodes can't connect to you because they can't see you.
And the way you solve that is by opening a port on the router, forwarding that port to your node.
Which you can do manually, like you go to 192.168.0.2 and then you log in and you say port forwarding and you say send port 8333 to this device that runs my node.
But nobody wants to do that.
So there are libraries that are often used by games and by programs like BitTorrent and all these things that will do it for you automatically.
That will just, you know, from your computer ping your router and say please route this port to me.
And that was done using UPnP, but apparently that's very insecure and very bad, so it was turned off by default in Bitcoin Core, so nobody was using it.
And now there's another library called NAT-PMP that apparently is a bit safer, a bit easier, and that's now added.
So if you open Bitcoin Core in the settings in the GUI there's a button that says NAT-PMP.
I think you can click on it and it'll try and then it'll try to open the port on the router to listen.
I don't know if it gives any useful feedback, if it doesn't work.
I haven't tried it.
I don't think it works on my router.

Aaron: 00:33:11

And then other than that, what we haven't mentioned, of course, every Bitcoin Core upgrade has a ton of smaller improvements.
Bug fixes, these kinds of things.
But I think we agree that these were, what we've mentioned now, were the six most notable changes in this new Bitcoin core release.

Sjors: 00:33:30

Yeah, there's one meta change I think we forgot to mention, which is not inside the build itself, but is that the deterministic builds for this release are being made using GUIX for the first time.

Aaron: 00:33:43

Right, yeah, I do think we've mentioned that, but maybe you can explain real quick what that is.

Sjors: 00:33:48

Well, I think we talked about, I think we talked about reproducibility in an earlier episode, why open source matters, episode 21.
We talked about, it's important for Bitcoin Core to be open source but also that the thing you're downloading from bitcoincore.org is actually related to that source that's out there.
Because we could just say hey look at this beautiful source code and then give you some binary that's just ransomware.
We spent the whole episode 21 explaining how to prevent that and GUIX is a new project, relatively new, that makes that process of verifiability better.
We're now using that for the release.

Aaron: 00:34:34

Great.

Sjors: 00:34:35

Yeah I think that's that's basically it.

Aaron: 00:34:38

Yeah so the main changes were hardware wallet hardware wallet supported in the GUI, I2P support, first release to have taproot which includes receiving very basic taproot transactions, `testmempoolaccept` was updated as an incremental step towards package relay.

Sjors: 00:34:58

I mean, I don't even know if you want to call it the main changes, it's the changes we discussed and that are maybe the most visible and make sense.
But you know, I can list a few other things.
There's a `CoinStatsIndex`, which has been on my to-do list for a long time to see.
UTXO snapshots., we talked about UTXO snapshots, I think, along another episode and there's another little piece of progress in there.
Yeah, hundreds of things.

Aaron: 00:35:28

Extended multi-sig support is what I forgot to mention.
NAT-PMP.
It's amazing.

Sjors: 00:35:34

It's awesome.
It's going to be available in a store near you.
Oh no, it's free.

Aaron: 00:35:38

Oh, even better.

Sjors: 00:35:40

All right.
I think that's all, right?

Aaron: 00:35:42

Yeah, that's it for me, Sjors.

Sjors: 00:35:44

Okay, then thank you for listening to Bitcoin Explained, formerly known as the Van Wirdum Sjorsnado.

Aaron: 00:35:50

There you go.
