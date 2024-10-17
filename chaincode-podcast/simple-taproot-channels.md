---
title: Simple Taproot Channels
transcript_by: TheFrayy via review.btctranscripts.com
media: https://podcasters.spotify.com/pod/show/chaincode/episodes/Elle-Mouton--Oliver-Gugger-and-Simple-Taproot-Channels---Episode-33-e2724sl
date: '2023-07-15'
tags:
  - anchor-outputs
  - cpfp-carve-out
  - ptlc
  - simple-taproot-channels
  - taproot
speakers:
  - Elle Mouton
  - Oliver Gugger
summary: Elle Mouton and Oliver Gugger explained the transition from 2-of-2 Pay-to-Witness-Script-Hash funding outputs to MuSig2 key funding outputs in Taproot channels. This upgrade aims to enhance privacy and chain space savings. The spec for Taproot channels, proposed by Roasbeef, is nearing completion with notable progress from LND and LDK implementations. The podcast also delved into potential updates to the gossip protocol, distinguishing between Gossip 1.5 and 2.0. Gossip 2.0 proposes tying proofs to node announcements rather than individual channels, significantly boosting privacy. The discussion extended to PTLCs (Point Time-Locked Contracts), which promise enhanced privacy and security but require further adoption and development. The iterative approach to these upgrades emphasizes gradual implementation to mitigate risks and ensure stability
episode: 33
additional_resources:
  - title: CPFP carve-out
    url: https://bitcoinops.org/en/topics/cpfp-carve-out/
  - title: Anchor Outputs
    url: https://bitcoinops.org/en/topics/anchor-outputs/
  - title: PTLCs
    url: https://bitcoinops.org/en/topics/ptlc/
aliases:
  - /chaincode-labs/chaincode-podcast/simple-taproot-channels/
---
## Introduction

Elle Mouton: 00:00:00

Then we get to Gossip 2.0, which is the bigger jump here, which would be instead of tying a UTXO proof to every channel, you instead tie a proof to every node announcement.

Adam Jonas: 00:00:15

Okay.

Adam Jonas: 00:00:19

It's a good week for podcasting.

Mark Erhardt: 00:00:21

Oh yes.
We have a lot of people to talk to.

Adam Jonas: 00:00:25

We'll see how many we can wrangle.
But first two are going to be Elle and Oli.
And what are we going to talk about with them?

Mark Erhardt: 00:00:33

So someone told us that there might be some movement on Taproot channels.
And given that there is a spec meeting happening, We wanted to hear about what the proposed spec changes are, how taproot channels work, how that fits into PTLCs, what upgrade paths might exist to get there.
So we're asking the people that are writing the spec.

Adam Jonas: 00:00:58

Cool.
I hope you enjoy the episode.

Mark Erhardt: 00:01:07

Hey Jonas, welcome back.

Adam Jonas: 00:01:08

Thank you.

Adam Jonas: 00:01:09

It's been a while, but we have two great guests today.
Welcome to Chaincode, It's great to have you here.
And I'm excited to talk about Simple Taproot channels.

Oliver Gugger: 00:01:18

Thank you for having us.

Elle Mouton: 00:01:19

Yeah, really, really excited to be here.

Adam Jonas: 00:01:21

Great.
So where do we start?
Maybe tell us about what they are.

Elle Mouton: 00:01:24

Oli, you want to take this one?

Oliver Gugger: 00:01:26

Sure.

## Simple Taproot Channels Overview

Oliver Gugger: 00:01:27

So yeah, you might've all heard of Taproot having been activated quite a while ago.
So everyone's asking, Hey, when do we get all these cool privacy benefits out of Taproot transactions and simple Taproot channels with the emphasis on simple, because that's just the first step towards getting there.
And basically what they do is just replace the funding output, which so far has been a 2-of-2 Pay-to-Witness-Script-Hash funding output with MuSig2, still 2-of-2 signature, but it's a MuSig2 key funding output.
And while we're doing that, it's also changing up some of the scripts to get some of the benefits in chain space savings and privacy benefits.

Mark Erhardt: 00:02:24

All right, so to recap, Taproot's been out for about one and a half years And Lightning Wallets can probably already send to Taproot outputs and probably receive Taproot outputs onchain.
But now we're going to make the funding output, the UTXO that the channel is built upon, Taproot as well.
Which means that we can have something that looks like a single-sig output using MuSig and we, well, yes.
So you said that we're also going to see some changes in the scripts.
That sounds like something that is the business of all Lightning implementations.
What's the status there?
Can you maybe walk us a little through that?

Elle Mouton: 00:03:08

I mean, just the status of the of the spec.
Yeah.
OK, well, so the one and only Roasbeef proposed the spec about a year ago, I think now, and like has gotten really good feedback from kind of all parties.
And I think, so the LND implementation is pretty close to being done, and I think LDK, but I'm not sure, has also made quite a bit of progress.
The spec is not merged yet, but hopefully with the spec meeting coming up, we can make some progress there and get it merged.
But all parties seem to be pretty happy with how it's turned out.

Mark Erhardt: 00:03:43

All right, so The spec is, so a lot of people are in New York right now for the Lightning Summit, and I assume that this is going to be a big topic here.
And so you're saying that the spec is probably going to make progress in the next couple weeks or so?

Elle Mouton: 00:04:01

Yeah, I think so.
Like if we could get to interrupt testing in like the next few weeks, that would be amazing.

Mark Erhardt: 00:04:06

Super cool.

Oliver Gugger: 00:04:07

Yeah, there were a couple of review rounds on the spec and while implementing our version or while Lalo implemented our version, we found out some things that we changed in the spec.
And so far there hasn't been a lot of controversy.
So maybe it could be finalized pretty soon.

Mark Erhardt: 00:04:29

That sounds very cool.

## Changes to the scripts in Taproot Channels

Mark Erhardt: 00:04:30

So basically the benefits would include that if a unannounced channel gets closed for somebody that doesn't have more information about that transaction, if there are no unsettled HTLCs or PTLCs attached, it will look just like a single-sig payment.
That's one of the privacy benefits that we talked about.

Oliver Gugger: 00:04:54

For the cooperative case.

Mark Erhardt: 00:04:55

For the cooperative success case, right?
Yes.
So how about we talk a little bit what the other outputs, the more revealing outputs might look like on such transactions.

Elle Mouton: 00:05:07

Yeah, first of all, one great benefit is a lot of the outputs have multiple branches, right?
So that's a great thing about Taproot is we can just like put things in multiple branches and we only reveal the branch that gets spent.
So in majority of the cases, even in a forced close, it's going to be a smaller onchain footprint.

Mark Erhardt: 00:05:24

So you're talking about having different leaf scripts in the taproot tree?

Elle Mouton: 00:05:28

Yes, exactly.
So do you want me to go in detail of what each output looks like?

Mark Erhardt: 00:05:34

Knock yourself out.

Elle Mouton: 00:05:36

Okay, so just to quickly recap, taproot in general, you've got this key spend path, and you can put a bunch of scripts in a tree as well.
And the key spend path is great because you've got all these scripts, but if you don't need to, you just sign for the one key and you don't have to reveal any of the scripts.
So that's really nice.
And we do get to take advantage of that a little bit in simple taproot channels, but not as much as you would hope.
So I don't know where you were.

Mark Erhardt: 00:06:06

In the keypath spend, we get to benefit from that in what case.
So let's remind ourselves when we have multi-hub payments, we create a smart contract that locks in funds.
There's two locks right now with the HTLCs. There's a hashlock and a timelock.
Also, why am I explaining this lightning stuff to you people?
But in the case, well, in the best case, of course, the payment goes through and it gets folded back into the main balance of the channel.
But in a failure case where some party disappears or the contract times out, either the receiving party needs to get the funds or the sending party needs to get the funds.
And those two cases, one makes use of the hashlock, one makes use of the timelock.
In which case would we be able to make use of the keypath spend?

Elle Mouton: 00:07:00

Okay.
So it also depends on which commitment we're talking about, if it's my commitment or your commitment.
And the important thing to remember is that any output on my commitment that goes to me needs to be locked by at least one CSV because of the anchor, if you're using anchor outputs, which simple taproot channels does do.
So to preserve the whole, what's it called?
CPFP carve out rule.
Any output needs to be locked by one CSV, which requires a script.
So mostly we get to make use of this on any output that goes to you.
So like, for example, if I have got an incoming HTLC to me, then it has to have a revocation path to you.
That doesn't need to be locked by CSV.
So that can be the keypath spend.

Mark Erhardt: 00:07:43

Right.
So the idea would be you are unilaterally closing the channel.
All funds that go to you must be locked in some way because if you are broadcasting an old state, if you could spend any of the money immediately, you might steal money because the HTLC doesn't exist on a newer commitment transaction or the channel balance has changed.
So all funds that go to you in your commitment transaction need to be locked, right?

Elle Mouton: 00:08:09

Yes, I actually, and I just realized I kind of mixed it up a little bit.
Even outputs that go to you need to be locked by one CSV on my commitment transaction for the CPFP carve out.

## Refresher on CPFP carve-out and Anchor Outputs

Mark Erhardt: 00:08:19

Wait, can you explain the CPFP carve out in that context?

Elle Mouton: 00:08:22

OK, cool.
So, Simple Taproot Channels uses anchor outputs.
And the reason for that is if we need to force close, then we can use the anchors to CPFP, so child pays for parents, the transaction, so it gets in.

Mark Erhardt: 00:08:37

Right, so the anchor output is basically a dummy output that has little value and that is spendable by both parties so that you only need one.

Elle Mouton: 00:08:45

So, no, there's two.

Mark Erhardt: 00:08:46

No, There's two?
There's two.
I'm already in ephemeral anchors world.

Elle Mouton: 00:08:52

We wish we could be there already.
So there has to be, there's one that only you can use and there's one that only I can use and the whole idea is that, So there's one output that you can use to CPFP the thing.
And even if you try and like pin the transaction, like basically hitting all the mempool limits, right.
To prevent me from getting it in, then the CPFP carve out rule allows this like one more that's yours, that doesn't have a timelock, always needs to have, well, it doesn't have like the big timelock, still needs to have a one block CSV time block.
So, and just to kind of come back to the start of the question is even that output can't make use of the keypath spend.

Mark Erhardt: 00:09:31

Right, because it has to be check sequence, verify locked.
And thus you cannot just use a tweak because tweaks cannot cater to lock times or it can not express lock times.
So just to recap in case we need to cut together, The transaction has one output for each party on the channel to spend the capacity back to them.
One output for each HTLC in flight either one direction or the other.
And two anchor outputs, one for either party, that can be spent in order to CPFP the transaction.
And there's a carve-out on transactions, so even if the send-in limit is hit and the wait limit is hit, you can bump your transaction using the second anchor output.

## Why Anchor Outputs need to use script path spends

Mark Erhardt: 00:10:23

So my follow-up question would be, why are there two anchor outputs and does that mean that one of them lives forever?

Elle Mouton: 00:10:30

Okay, so the reason there are two is so that we have this CPFP carve out ability, right?
So you have the ability to spend even if I'm trying to pin you and the other way around.
So no, they don't live forever.
And this is like a really cool thing that was thought of even in the current implementation of anchor channels, which basically says you're allowed to spend it for 16 blocks and then it becomes an anyone can spend.
Which is really cool, because then you get these people who just try and sweep all the anchors.
And so we have to, and that was like a big thing in the simple tapper channel proposal, so we have to keep this ability so that we don't litter the UTXO set.
Because it's like 330 satoshis.

Mark Erhardt: 00:11:08

Oh, okay.
So the anchor output does have a minimum balance to make it non-DUST, and that makes it Interesting to sweep at minimum fee rate.
Right, okay.
I was wondering who does the garbage collection and how.
Who is doing the garbage collection?
I guess miners probably?

Oliver Gugger: 00:11:27

Someone does.
We see that the current anchor outputs are being swept.
It has led to some issues in LND where the wallet then also still tries to sweep it, even though it had been swept, but, I think we fixed those.
Yeah.
So someone does, not sure who.

Elle Mouton: 00:11:48

But yeah, that was a really cool, like, interesting, we almost, like, I think Ali, I think you spotted this, that we like almost lost that ability, like, with the design of the simple Taproot outputs, because, so we like, we have this anchor output, we can use the keypath spend because it's like, it only needs your pub key, right?
So awesome, that's the keypath.
And then it's got this anyone can spend thing.
But if that third party wants to come in and spend it, they need to provide the internal key.
And how do they know the internal key?
Okay, well, they would know your internal key if you spend the two remotes because then you provide it.

Mark Erhardt: 00:12:24

So if you use another leaf script, you would provide the internal key.

Oliver Gugger: 00:12:31

If you would spend another output on the transaction that would use the same key, then the world can learn from that spend what the other key was.

Mark Erhardt: 00:12:41

Right.
It's the something block that reveals all the...

Elle Mouton: 00:12:46

Oh, the control block.
Oh, yeah.

Mark Erhardt: 00:12:47

Thank you.
The control block.
Through the control block, you reveal the internal key, but only if another leaf script is used.

Elle Mouton: 00:12:54

Exactly.

Mark Erhardt: 00:12:56

So how do you learn it after?
Oh, is that why we cannot use the keypath?

Elle Mouton: 00:13:02

Exactly.
So the two remotes is really easy because there's only one script, right?
So it's basically people who want to spend the anchor just need to wait till the remote party spends it, they'll learn the key, it's fine.
The problem is on the two local, because you've got two paths.
One is to me after timelock, the other one is revocation path to you, right, if I'm cheating.
And then so we originally had the revocation path as the key spend, because it's like, that's a nice benefit, But then if it does, if that gets spent, then you could have this anchor just left over forever.
So we had to make, we had to get rid of the key, the key spend path in the to local.
And unfortunately we had to put the revocation path in the script and like just stuff the to local key there.
So it doesn't even do anything.
You just pop it on and drop it.

Mark Erhardt: 00:13:47

Would it perhaps be possible to encode it in some way in the other outputs that get spent?
Like once one of the balance outputs gets spent that it's locked to a combination of the, I'm thinking of Silent Payments right now because they're doing a very cool thing of generating a new unique key from the inputs.
And I'm just thinking maybe there's a nifty way of encoding it in some fashion.

Oliver Gugger: 00:14:16

Maybe I mean, there were a couple of ideas floating around.
Maybe someone will come up with a clever idea this week.
I mean, it is not really nice to just put these 33 bytes onchain or 32, I'm not sure which including 32.
Yeah, okay.

Mark Erhardt: 00:14:37

Yeah, especially for an anchor output, which is kind of...

Elle Mouton: 00:14:40

Yeah, but it's like, I think it's really cool that we were like, hey, we wanna make this decision so that we don't end up unintentionally littering the UTXO.
Sure.

Mark Erhardt: 00:14:50

I think that's more important.
No, no, I agree that that is the priority.
We don't want to litter the UTXO.
I'm currently writing an article for the Optech newsletter exactly on that topic, how we are protective of global resources in the network.
But yeah, so I agree on the priorities here.
I am just wondering, especially for an anchor output that of which always only at most one of the two will be spent, It feels kind of sad if it's extra large.
Anyway, getting a little bit.

Elle Mouton: 00:15:19

The anchor itself won't be extra large.

Mark Erhardt: 00:15:22

Well, the spending of the anchor will require an additional 33 bytes to have a script path spend instead of a keypath spend.
Yeah, anyway, also it's only temporary, right?
We're hopefully getting v3 transactions and ephemeral anchors and then you can have a single anchor for both parties.
Maybe, hopefully.
For that, maybe check out our next podcast.
If everything goes well.

## Other goals of Simple Taproot Channels

Adam Jonas: 00:15:52

I just wanted to sort of bring us back to base and talk about, you know, we've talked about the privacy piece.
What else, Like, why else are we pushing for this?
What's the, what's the high level goals?

Oliver Gugger: 00:16:04

So basically it's setting us up for the next step, which would be the, some changes to the gossip protocol.
And then the pen, the ultimate, upgrade will be, to PTLC, which requires, tap roots, funding outputs, But because that last step is such a big step, we're doing it incrementally just to reduce the complexity of each step and gain some experience
Figure out all these complications such as we discussed before.
Yeah, because doing it, everything in one step is big thing.

## Why do PTLCs need Taproot funding outputs?

Mark Erhardt: 00:16:43

Sorry, I have a follow up question there.
My understanding was that PTLCs requires both parties in the channel to be able to understand taproot, but why does it need a taproot funding output?
Wouldn't it also be able to have a PTLC output on a pay-to-witness script hash anchor?
Sorry, funding output?

Elle Mouton: 00:17:03

You technically could, but remember that, so PTLCs, importantly, the whole route needs to be,

Mark Erhardt: 00:17:09

PTLC.
You basically just use whether a channel is a taproot channel as a signal, whether both peers know taproot?

Elle Mouton: 00:17:16

Yes.

Mark Erhardt: 00:17:17

Oh, okay.

Oliver Gugger: 00:17:17

Okay.
And I'm not very up to date on PTLC, so this might be wrong, but I thought that, some information in the funding key, like the nonces used, are also used in, in some of the adaptor signature set up for the PTLCs in order for the revocation stuff to become a bit more deterministic.
So I think that's why we need, but this could be wrong.

Mark Erhardt: 00:17:47

Okay.
So it's part of the arcane details of how exactly PTLCs are going to work under the hood.

Oliver Gugger: 00:17:53

Yeah.
That might be another episode.

Elle Mouton: 00:17:55

I think there's going to be a lot of discussion on that in the next, in the follow up week.

Mark Erhardt: 00:17:59

Right.
So to recap, we're only talking about making the funding output paid to Taproot and PTLCs is future music right now.

## Potential updates for the gossip protocol

Mark Erhardt: 00:18:11

And so you mentioned gossip might change.
Can you give us an overview of what the proposed changes to the gossip are?
I heard some things about how we would love to get away from actually revealing what the funding outputs are.
I think that's what you're talking about, right?

Elle Mouton: 00:18:28

Yeah, so This is like a very big open space for discussion still.
So I can just talk around it kind of.
But basically, so this is also why simple type of channels is initially just for unannounced channels because the gossip layer isn't updated yet.
And why do we need to update the gossip layer?
Because currently the channel announcement message, you know, I get the two keys in this message, I go and reconstruct the P2WSH output.
I go look onchain, I'm like this definitely looks like a Lightning channel, I'm going to trust it, I'm going to pop it in my graph and I'm going to use it.
So that whole proof completely changes now, right?
So we have to redo that as the first thing.
So nodes need to know how to verify that a channel is like a taproot-looking channel.
And then there's this whole discussion of like, so the gossip 1.5 kind of proposal is just doing that, right?
So it works exactly as is today, basically just that we now, the nodes need to go verify this music output.

Mark Erhardt: 00:19:26

So basically just look up, is there a P2TR output that fits this transaction output out point.
Yes.

Elle Mouton: 00:19:35

And you still tie each channel that you want to announce to a UTXO chain.

Mark Erhardt: 00:19:40

Right.
So you would still continue to announce public channels with a specific UTXO.
And of course that would sort of deny some of the privacy benefits of moving to pay-to-tab route, which makes all outputs look, all MuSig outputs look like single-sig outputs and if we could get away with not announcing the funding output explicitly, that would make Lightning way more private, right?

Elle Mouton: 00:20:09

Absolutely, absolutely.
So that's like the, then we get to Gossip 2.0, which is like the bigger jump here, which is, would be instead of tying a UTXO proof to every channel, you instead tie a proof to every node announcement.
So you just say, hey, I own a channel, like I definitely own this UTXO, I'm showing you, I'm like, you know, I got it straight from the exchange.
I don't like this is my KYC to like show that I've got capital.
And then we come up with a multiplier, let's say 10x.
And then that's so let's say I have a proof I have one Bitcoin, one Bitcoin output, 10x.
So now it gives me the ability to advertise 10 Bitcoin worth of channels.
Right.
And then I can give a channel announcement and you kind of just, you don't need to, you don't go verify it onchain.
You just, you know, I've already proved, I've already like,

Mark Erhardt: 00:20:54

you've already verified the commitment to this one Bitcoin and you know that this node has sort of some credibility for up to an amount that they can announce.
Then you have to keep track though how many channels have been announced by specific nodes, right?

Elle Mouton: 00:21:11

Yes, and you have to know is it, you know, if I'm opening a channel with Ali, Is it coming off of my balance?
Is it coming off of his balance?

Mark Erhardt: 00:21:18

So you still have to announce whether the channel is opened by one or the other party?

Elle Mouton: 00:21:24

Yes.

Mark Erhardt: 00:21:24

So that you know who to deduct it from, like their allowance?

Elle Mouton: 00:21:28

Yes.
And then there's other complexities such as like, I've got this allowance for 10 Bitcoin worth of channels, and now I want to open more.
Now what do I do?
Do nodes assume that the other ones are closed?
Because now nodes can't go look onchain to see if the channel's closed, right?
So that is different now.

Mark Erhardt: 00:21:45

I kind of, maybe I'm jumping too far, but I kind of wonder that sort of also enables people to have credit based channels, right?
That must be part of the discussion, right?

Elle Mouton: 00:21:56

Absolutely.
So I could be like, Hey guys, I can, you know, you can use my UTXO as proof and then you can like.

Mark Erhardt: 00:22:02

Sure, sure.
But I mean, a, that channel, the channel partner would also have to agree that the channel is based on credit and there's no actual UTXO.
Yes.
The risk is only, as far as I understood, I looked into this a while back.
The risk is only that of the two channel participants, because of course they also have an ephemeral HTLC and when a payment times out, the onchain settlement would be interrupted at that point, right?
So, but yeah, so is that, is that a big part of whether it's gossip 1.5 or 2.0 that you're going to, or is that settled meanwhile?

Elle Mouton: 00:22:43

I think this part is still very much open for discussion.
Yeah.

Mark Erhardt: 00:22:46

Okay, interesting.

Elle Mouton: 00:22:46

And like it also, you know, I think route finding and stuff becomes a little bit weird because you no longer know exactly what capacities lie where.
And these things are still open for...

Mark Erhardt: 00:22:58

Oh yeah, channel capacities were set by the output, the funding output.
But wouldn't you announce a channel for a specific amount as well now?

Elle Mouton: 00:23:07

Absolutely, right?
And then if you do lie, if you say it's a one Bitcoin channel and it's actually like hundreds of channels, like things are gonna fail, right?
So you're gonna, and then people will adapt.

Mark Erhardt: 00:23:16

Right, but you could announce a one Bitcoin channel if you have 1.1 for privacy reasons.
If you have a higher capacity than you announce that will work, right?

Elle Mouton: 00:23:26

Sorry, can you say that again?

Mark Erhardt: 00:23:28

So let's say we are getting now the privacy benefit of having this unrelated UTXO as the credit-establishing funding output, not funding output, but we still need an actual funding output if we set up a legit channel.
So let's say we had a unique amount of satoshis in that funding output with like eight digits per session.
If we announce that, people might look at the UTXO set, find a specific UTXO of that amount and they're like, ah, that fits the time of the channel announcement, that must be it.
So I could go and say, if I, for example, have 115 Satoshis more than one Bitcoin, I announce one Bitcoin instead for privacy purposes and announcing a smaller capacity should work, right?
Maybe I'm getting too much in the mood.

Elle Mouton: 00:24:15

I mean, you can also just open one public one and then many private ones and then hide it that way.
But you would definitely fuzz the output amounts.

Mark Erhardt: 00:24:25

Paul Matzko Right, sure.
Okay, so we talked a little bit about Gossip 1.5, 2.0. This is also part of what people will talk about in the next couple of weeks?

Elle Mouton: 00:24:33

Definitely, because it's a big change, right?
Changing the gossip layer and 2.0, we get way more privacy benefits, but it is a big jump.

Adam Jonas: 00:24:42

And what are you most concerned about, I guess, in terms of that big jump?

Elle Mouton: 00:24:45

I guess, first of all, taking long, because there's just so many different changes.
And so then it takes just way longer for users to get those benefits.
And you know, big changes means more bugs and more testing and it just takes long.
Right.
So yeah.

Mark Erhardt: 00:25:01

On the other hand, if the 1.5 solution gets rolled out, that might be a good enough provisional solution and live forever, right?

Elle Mouton: 00:25:08

Yeah, so that is, that is.

Mark Erhardt: 00:25:09

So you never get the privacy benefits maybe?

Elle Mouton: 00:25:11

But you get to test things, you get to like iterate faster, you get, we can get PTLCs maybe a bit faster than if we were to wait for the big proposal.
So yeah, there's pros and cons.

## PTLCs

Mark Erhardt: 00:25:22

So PTLCs, we touched on them a little bit, but you said that it is based on needing pay to taproot funding outputs first.
Then also PTLCs can only be used if all hops along a route are support PTLCs. The benefit, of course, is that it becomes more private because it's harder to tie.
For example, back when a surveillance is multiple participants in a long chain of hops, because now it's not just a single pre-image, but every hop has a different pre-image.
What's the timeline for this?
This is super cool.
We've been hearing a lot about it for what, three years now?

Elle Mouton: 00:26:08

I don't know.
So there's been a few kind of, there was initially like a big bang proposal.
I think from AJ Towns with Taproot channels and that immediately included PTLCs. I think T-Best also gave an updated proposal of that.
So I think again, like in the next few weeks, we'll hear more about that.
People are currently just focusing on getting the Taproot channels out first, but you know, two weeks TM.

Mark Erhardt: 00:26:34

Yeah.
Okay.
But people are just as excited about that.

Elle Mouton: 00:26:37

Oh, I think so.

Oliver Gugger: 00:26:38

And it's not just all the protocol updates that are needed and all the scripts that change.
It's also, yeah, I would even say new cryptography that we haven't used in Lightning before with adaptor signatures and all of that.
So, I mean, it's probably not that big of a deal to implement because it's all just elliptic curve cryptography, but because it's a new thing, it could still be that we find some issue with the cryptography protocol or leak of information or whatever.
So It's just quite a big step on all of them.

## Iterative approach or big push?

Adam Jonas: 00:27:18

But I think philosophically, and not being as involved with the Lightning community, what is sort of the approach in terms of iterative small changes and working towards a larger goal, or larger changes and getting them out and seeing what the bugs might be.
The many steps, as Murch alluded to, mean that you may not get to that end point for a really long time, if at all.
And as the system grows and more money gets put into the system, the stakes get higher.
So if you know where you're going, why not just rip off the bandaid now as opposed to doing half measures?

Elle Mouton: 00:27:53

I mean, it just seems like so far when each big proposal we've seen in Lightning, we just keep discussing it for years on end.
And so I think initially I would have said, yes, do the big thing now.
Because if you do the iterative thing, you always have to keep one foot in the legacy world and one in the new.

Oliver Gugger: 00:28:11

It's just hard to be backward compatible, forward compatible, feature flags, feature negotiation.

Adam Jonas: 00:28:17

Lightning is move fast and break things.
Isn't that why we have different layers?
Isn't that the idea?
Is that all the fun, cool people are on Lightning and all the stodgy old timers are on Bitcoin?

Oliver Gugger: 00:28:28

Breaking things might mean it doesn't break Bitcoin as on layer one, but it could still be a forced close in a high fee environment, which isn't funny.
So I mean, I agree we can move faster than on layer one, but it's still people's money on the line.

Elle Mouton: 00:28:48

Exactly.
And I think it's a lot of people's first introduction to using Bitcoin and you don't want that to scare them off, right?
It's got to work.

Mark Erhardt: 00:28:58

It's also hard to see how going to PTLCs is going to have a good bang for the buck quickly.
Because only once many nodes have updated and have created new channels based on taproot outputs, you would actually start being able to send multi-hop payments, because only when all hops have it, you can, right?
So, I mean, sure, you need to get it out there in order for people to be ready for it.

Adam Jonas: 00:29:24

I would imagine that for lightning service providers, though, they would be the first upgrade, and that's where the majority of the, you know, the Starbucks payments will go through, right?

Mark Erhardt: 00:29:34

Right, sure.
And they're short, not many hops, right?
So in the direct vicinity of Lightning Service providers, probably the upgrade speed would be faster.
But if you get the taproot funding outputs first, then the software update to enable PTLCs would also immediately have already that infrastructure of taproot channels that could use it.

Oliver Gugger: 00:29:57

Yeah.
I mean, the other thing, so first coming back to, if we do small incremental steps, we might never get to the end.
I personally don't believe that because the benefits are so clear.
We do want to get there, but might not want to go there as quickly as possible and risk all the bugs.
So I think doing small steps isn't a risk of never getting there.
And also the small steps, that's what I also mentioned, is if you can agree on something, why not go ahead with that thing and then discuss all the other nuances along the way?

Adam Jonas: 00:30:32

If it's providing value.
This is something we see in other projects as well, is that you're sort of working towards an end goal and everybody seems to concept act the end goal.
And so you start, and you start merging in these smaller chunks and then people start having doubts as to what the end goal is.
Maybe this isn't the right approach.
You're stuck in this in-between state.
If you can live in that in-between state and it does deliver value, That makes sense.
But if it's not, and you're sort of just now stuck with one foot in the old world and one foot in the new world, but the new world isn't quite delivering the vision that you hoped for.

Elle Mouton: 00:31:11

But isn't that better than having gone full into the new world?
Because you learned early and then you can like you can make other changes.

Adam Jonas: 00:31:18

I think it depends.
I think you're I think you're I mean, these are all tradeoffs, right?
So you're trading one problem for another and you're uncovering what those problems are and adapting accordingly.

Mark Erhardt: 00:31:26

Right.
But as long as each step provides value on itself, I think you're moving towards a better world, right?

Oliver Gugger: 00:31:33

Yeah.
And, and for us, this, this first step of doing taproot channels, even if they're simple taproot channels is onchain, we already have what we require for PTLCs.
And one thing that we need to mention here is that there's also proposal for dynamic commitment.
So basically you can upgrade a channel in flight without needing to close it.
So if we have simple taproot channels and they're already quite widespread, then the upgrade to PTLC channels would be like an online upgrade.
Right.
So both nodes come up, they take the channel online.
Oh, you also speak PTLC.
Oh yeah, me too.
Cool.
Should we upgrade the channel?
Done.
No onchain footprint.
Right?

Mark Erhardt: 00:32:18

And that would be communicated by a flag then?

Oliver Gugger: 00:32:21

Yeah.
Feature flag.

Elle Mouton: 00:32:23

Yeah.
Yeah.
You'd have to communicate to the rest of the network as well.

Mark Erhardt: 00:32:26

I need to know whether they can send a PTLC.
Yeah.

Oliver Gugger: 00:32:29

So yeah, there are upgrade paths and, and yeah, just getting this first step out is important.
Then we can see where we go from there.

Mark Erhardt: 00:32:40

Super cool.
What have we missed?
Is that, I think we covered what we set out originally to do.
Do you have things that you want to add that we missed?

Elle Mouton: 00:32:52

I mean, this would fit into earlier in, but I don't know if you wanted to talk about the brute force ability of recovery and stuff.
And then it can maybe be edited in earlier in the podcast.

Oliver Gugger: 00:33:04

Doesn't need to be edited in early.

## Recoverability of channel funds and brute force closures

Oliver Gugger: 00:33:06

Yeah, just one thing that, I noticed during review is that, the right original spec had for the two remote outputs.
So basically if I go onchain with force closed and my, my remote party can, can spend it immediately.
Use the internal key for the internal key, use the MuSig2 to funding key of, which is the same as in the funding output because we thought, yeah, we're never going to agree on spending through that.
So it could just be a point that is never going to be used.
But one thing I noticed while writing Chantools, which is a utility that helps people recover funds is that a lot of people don't really do have their channel backup files.
So they cannot sweep funds even if the remote party closed and they would be accessible.
So with the previous channel formats, you had at least the ability to kind of brute force your way to get that.
So basically go through all the keys that you have in your wallet and see if any of them has some funds.
But if now we have an internal key with a key that is derived from something that the other party contributed to, then we can never brute force that, right?
So that's another reason why the two remote output is a bit more complicated or not.
No, it's not more complicated, but it now uses a so-called nums key, nothing up my sleeve key, which is basically a public key that is provably unspendable and it's well known.
So everyone knows what the key is.
So that's basically the internal key.
It can never be spent through that path.
But then the CSV one scripts that we have in there is, is basically allows us to, to brute force this again, if someone doesn't have their channel backup.

Mark Erhardt: 00:35:05

Okay, so the internal key always is the same and it is, so that will reveal onchain of course that you're recovering from an incomplete HTLC.

Oliver Gugger: 00:35:16

Not HTLC, just the channel balance, the two remote.

Mark Erhardt: 00:35:20

Yeah.
Right.
Okay.

Oliver Gugger: 00:35:21

So, but that would have been the case before.

Mark Erhardt: 00:35:23

So this is the commitment transaction output to one of the two remote commitment output and It cannot be spent on the keypath, but it can only be spent on the script path.
So it makes the force close a little uglier to recover from, but no, we already publicly visible anyway, right?

Oliver Gugger: 00:35:43

Yeah.
We already have the same script today, right?
We just don't have an internal key.
So it basically looks the same on taproot.
Like the script path that you spend is the same as today.
It's just an internal key that is a well-known key now.

Mark Erhardt: 00:36:02

Cool.
I have the impression that lunch may have arrived.
Yeah thank you very much, thanks for coming on. 

Adam Jonas: 00:36:21

All right Murch what'd you learn?

Mark Erhardt: 00:36:22

I feel pretty caught up again on how Lightning is going to work.
Pretty excited about Taproot channels coming to pass.
Definitely need to get the pay-to-Taproot outputs up on the chain.
We've got real rookie numbers going on so far.
And yeah, it's all these privacy benefits and upgrades and cost savings that we've been talking about for years that we're supposed to get from Taproot, and they're coming now.

Adam Jonas: 00:36:52

Yeah, it does sound like we're getting pretty close to delivering some of this stuff.
So yeah, thanks to Elle and Oli for coming in.
And we don't get them in the office very often, so it was nice to have them.
Cool, see you next time.