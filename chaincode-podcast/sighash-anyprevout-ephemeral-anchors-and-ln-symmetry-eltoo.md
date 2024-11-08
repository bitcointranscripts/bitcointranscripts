---
title: SIGHASH_ANYPREVOUT, ephemeral anchors and LN symmetry (ELTOO)
transcript_by: stackeduary via review.btctranscripts.com
media: https://podcasters.spotify.com/pod/show/chaincode/episodes/Greg-Sanders--SIGHASH_ANYPREVOUT--ephemeral-anchors-and-LN-symmetry-ELTOO---Episode-29-e1v1dc3
date: '2023-02-15'
tags:
  - eltoo
  - ephemeral-anchors
  - package-relay
  - rbf
  - sighash-anyprevout
speakers:
  - Greg Sanders
summary: Greg Sanders joins us to discuss ANYPREVOUT, ephemeral anchors and LN symmetry (a.k.a. ELTOO).
episode: 29
additional_resources:
  - title: 'Package relay'
    url: 'https://bitcoinops.org/en/topics/package-relay/'
  - title: 'Pinning attacks'
    url: 'https://bitcoinops.org/en/topics/transaction-pinning/'
  - title: 'BIP125'
    url: 'https://github.com/bitcoin/bips/blob/master/bip-0125.mediawiki'
  - title: 'T-Bast''s pinning attack summary'
    url: 'https://github.com/t-bast/lightning-docs/blob/master/pinning-attacks.md'
  - title: 'Package relay RBF'
    url: 'https://gnusha.org/url/https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-September/019464.html'
  - title: 'PR'
    url: 'https://github.com/bitcoin/bitcoin/pull/26265'
  - title: 'Daric: A Storage Efficient Payment Channel With Penalization Mechanism'
    url: 'https://eprint.iacr.org/2022/1295'
  - title: 'Two-party eltoo w/ punishment by AJ Towns'
    url: 'https://gnusha.org/url/https://lists.linuxfoundation.org/pipermail/lightning-dev/2022-December/003788.html'
  - title: 'BIP118'
    url: 'https://github.com/bitcoin/bips/blob/master/bip-0118.mediawiki'
  - title: 'SIGHASH_NOINPUT'
    url: 'https://github.com/bitcoin/bips/commit/98b7238f68d17f0e01275dd32075078702225356?short_path=2f8c560#diff-2f8c560480095b9f314d3a7e17cf7048a10f9a15b391acaf2c96412d5b4d4b9c'
  - title: 'Ephemeral anchors'
    url: 'https://bitcoinops.org/en/topics/ephemeral-anchors/'
  - title: 'op_2 email by Luke'
    url: 'https://gnusha.org/url/https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2018-May/015945.html'
---
Greg: 00:00:00

With `ANYPREVOUT`, I don’t want to champion it right now from an activation perspective.
I think the community is pretty split right now on what to do, but we can build the knowledge and build up the tooling.

Murch: 00:00:18

Hey Jonas.

Jonas: 00:00:19

Hey Murch.
We are back in the studio for a productive podcasting week.
We have @instagibbs (Greg Sanders).
So what should we talk to him about?

Murch: 00:00:28

He’s been looking a lot at mempool policy improvements.
I think we’re going to talk about v3 transactions, package relay, his recent work on ephemeral anchors, and then how that all hopefully compounds to us getting LN-Symmetry eventually.

Jonas: 00:00:46

Yeah, LN-Symmetry, otherwise known as Eltoo.
He’s championing to get rid of Eltoo and call it something better, more descriptive.

Murch: 00:00:54

He has my axe.

Jonas: 00:00:55

All right, cool.
Enjoy the episode.

Murch: 00:01:03

Good morning.

Jonas: 00:01:05

Hey Greg.

Greg 00:01:06

Morning.

Jonas: 00:01:06

Welcome.
Should we be calling you Greg or instagibbs?

Greg 00:01:11

Either is fine.
Greg’s fine.

Jonas: 00:01:13

Greg.
Okay, welcome, Greg.
Nice to have you in the office for a couple days here.
Today we are going to talk about some of your work, some of the things you’re thinking about.
You’ve been around Bitcoin for quite a long time.
Coming in, dipping out, come back in, doing some different things.

Murch: 00:01:28

Second round, around the block.

Greg: 00:01:30

I’ve been in the industry the whole time, but, my open source contribution comes in and out depending on what my interests are at the time, pretty much.

Jonas: 00:01:37

What are your interests these days?
What are you thinking about?

Greg: 00:01:40

These days, I’ve been focusing on a couple of things, but it focuses mostly around mempool policy and also Eltoo, the application of `ANYPREVOUT`.

Murch: 00:01:50

You mean LN-Symmetry, right?

Greg: 00:01:52

That’s right.
I’m rebranding it right now.
It’s called LN-Symmetry instead of LN-Penalty, which means you can use `ANYPREVOUT` to have a symmetrical channel state for Lightning Network channels.

Jonas: 00:02:05

Yeah, we’re going to dive into all of those things.

## Package relay

Jonas: 00:02:07

Let’s start with package relay and work up from there.

Greg: 00:02:10

There’s been this idea for many years that the peer-to-peer transaction layer, you want to be able to propose a set of transactions at the same time to a node.
For example, one transaction could be too low fee, but you can spend an output at a higher fee and do child pays for parent.
So this works today if the parent transaction, is the fee is beefy enough to get in the mempool on its own, but maybe not enough to get mined in a reasonable amount of time.
But it doesn’t work if the fee is too low.
So for example, if you wanted a transaction that’s zero fee, maybe you don’t know what the fee is going to be, or you’re basically doing a smart contract, for example, like Eltoo, you can’t actually siphon off any fees.
So you need to somehow pay for the fees.
There’s a few concepts of how to do it with consensus changes or smart `SIGHASH` changes.
But to do it in a policy way, it seems to make sense to have this package of proposals that you pass around the network.

Jonas: 00:03:10

How might this relate to some other terms that we’ve heard in terms of pinning attacks and things like that?

## Pinning attacks

Greg: 00:03:16

CPFP, child pays for parent, it actually can cause and mitigate pinning.
Because if you have a shared transaction, like a commitment transaction, a Lightning network with your counterparty, they go to chain with a too low fee version and then they spin off their own child pays for parent that’s actually not good enough.
Then if you want to RBF that, it’s actually very expensive.
And so that’s one version.
There’s many pinning attacks.
If you want to know what a pinning attack is, read BIP 125 and look at all the rules and say, how could I make this more difficult to actually robustly fee bump a transaction?
That’s pretty much what I do.
There’s been a lot of people thinking about it, working on it, and then recently, so the last couple years or so, Gloria Zhao has been working on package relay as a concept.
She was thinking initially, I think, more on the how do we gossip these, how do we put these in the mempool, but a drop-in replacement for single transaction relay, in a sense.
But then she realized that there’s all these pinning attacks.
She was talking to people who said, well, there’s a pin here, pin there.
Package relay by itself was insufficient for robust fee management.

Jonas: 00:04:31

The mempool has become a crossroads for layer one and layer two in terms of discussions.
It’s also a problem.

Greg: 00:04:41

It’s hard.

Jonas: 00:04:42

It’s hard.
Are we thinking, given that you’re thinking so much about mempool policy, about a pretty big rewrite in terms of how it works?
Are we thinking about mitigation steps on DOS vectors that are currently there?
How do you approach it?

## Mempool policy

Greg: 00:04:57

The current mempool policy is very DOS aware because we want to make sure that denial of service is expensive at least.
In an ideal sense, the denial of service would be someone spamming the chain with high fees.
They’re just outbidding everyone.
That’s kind of like the so-called ideal case, where they’re paying for the DOS, so the attack is limited until they run out of funds eventually, which we saw in 2017 or something.

## Stuffing the mempool - 2017

Greg: 00:05:23

We had that crazy months-long backlog.
Mempool was full, completely full for months.
Whoever that was ran out of money pretty much because of the…

Jonas: 00:05:32

That was a malicious attack?

Greg: 00:05:34

I think so.
At the time I wasn’t convinced but it’s pretty obvious.
The volume is just crazy even compared to today.

Murch: 00:05:40

I think there was some research on how all those outputs got spent later and it’s been a while since I read this, but they could tie it together.
So it definitely looked like there was at least one entity that was stalking the mempool.

Jonas: 00:05:56

This was like block-sized war stuff.

Greg: 00:05:59

I’m not a conspiracy theorist, but also it doesn’t have to be a conspiracy.
It could be one guy just cranking out.
They have some Bitcoin to burn, they wanna make a point, they do that.
It was so bad that transactions were being dropped from the mempool permanently.
I know a guy who held onto a copy, and then months later just dumped like hundreds of megabytes of other people’s transactions from the mempool.

Murch: 00:06:19

I noticed.

Greg: 00:06:21

Yes.
So that’s a little fun history that we haven’t seen since because things have been mostly clearing out in a weekly fashion.

Murch: 00:06:30

Turns out a bunch of people were not aware that when stuff drops from the mempool, that it could come back because it’s still a valid transaction.
And they didn’t invalidate those old versions.
And they paid some people twice when this cache of old transactions got resubmitted.

Greg: 00:06:49

That might have been a digression.
Back to the kind of architecture.
So it’s very DOS aware, but there’s also actual users.
So there’s wallets and there’s smart contracts.
And I think they’re actually closer than some people let on from a sense of as a wallet, I’d want to robustly fee-bump, but right now there’s all these issues with it.
So for example, the Bitcoin Core wallet, it’s kind of a self-made limitation, but I’ve seen this in a number of other places where I’d say, well, if one of the outputs has already been spent, I don’t wanna double spend that parent transaction, because it could be very expensive.
Or I’m not sure how to calculate the right amount, so on and so forth.

Murch: 00:07:22

Also just you don’t want to surprise the counterparty.

Greg: 00:07:26

Yeah.
TXID stability and stuff like that, which is also another concern.
Custodians or payment processors don’t want to cycle TXIDs on people and because people don’t understand it.

Murch: 00:07:39

A lot of software tracks by TXID instead of by payments.

Greg: 00:07:42

I mean even informationally.
A customer says, "Oh I’m seeing this transaction coming and I’m getting paid, then disappears," they freak out.
They say, "Where’d my money go?".
This is a real problem.
I was just talking to someone yesterday.

Murch: 00:07:53

It’s a customer support problem.
Expensive.

## Rewrite mempool or make the problem simpler

Greg: 00:07:57

So the question is, how do we fix this?
So there’s the big architectural override of how the mempool works.
Should we rewrite everything?
Okay, do something really, really smart, maybe DOS resistant.
I think there’s just the design space is so huge.
I think it’s like a decade of work in some ways.
Or we make the problem simpler.
And so this is kind of the direction that a few people were thinking, I think Suhas, TheBlueMatt and others, but hadn’t really written down a proposal.
And so Gloria and myself and a few others started thinking about how to make something that would work today with, in the short term I would call it, with minor changes to, for example, the Lightning Network could use it with minor changes, versus something that would be bigger or more disruptive.

## Package relay RBF A.K.A. v3

Greg: 00:08:42

Gloria has the package relay work and then on top she calls it package RBF proposal, also known as v3 proposal.
Or you pick a new version, Bitcoin transaction version three, and you say, okay, I’m opting into a simpler topology of unconfirmed transactions.
The mempool's policy is like a handshake agreement: okay, you wanna make a parent transaction and you might wanna fee bump it and we’re gonna let you do that.
So you have one parent transaction and up to one child transaction.
So it’s a parent-child relationship and the child is limited in size.
The package size of two, which fixes some pinnings.
Go read those rules.
And then limiting the child to a certain size, which fixes rule number three, which is the common one people point out, which is you have to replace all the total fee of all the children you knock out of the mempool, which can be prohibitively expensive.
And even if the child is not going to be mined in the next two weeks.
It’s just absolute fee considerations.

Murch: 00:09:49

Or yeah, in the old style, up to 100 transactions can be replaced, and of course, the total size of all that.

Greg: 00:09:56

Yeah, so that’s BIP rule five, I think.
It’s up to 100 transactions.
That’s all fixed with here because you can only knock down two times the number of inputs that you double spend.

Murch: 00:10:06

And if the confusion is not enough, BIP 125 does not actually fully align with what’s implemented in Bitcoin Core.

Greg: 00:10:13

That's right.
So Gloria did some great work communicating not only what the...she’s done some great talks you should go look up, but also documentation about what are the design decisions of the mempool as today, descriptively.
And then also some prescriptive notions.
So in the Bitcoin Core repo, you can see that there’s these Markdown files that have a great explanation of why things are the way they are.
Because when I was interested in mempool policy in 2017 or so, it’s just kind of a spooky science.
It’s witchcraft a little bit.
Why is this here?
Why is this code here?
Who really knows?
If I cornered Suhas in a room, I could probably get an answer out of him.
But systematizing that knowledge and getting it down and communicated to the wider dev community, at least, was very important.
And that’s what she did.
So they’re right.
So that’s the v3 package RBF, which says, I can RBF this parent efficiently.

Murch: 00:11:05

Right.
So to recap, there’s one transaction and it has to be a version 3 Bitcoin transaction so there’s versions all over Bitcoin we’re not talking about one SegWit versions or block versions.

Greg: 00:11:18

There’s two standard ones today: version 1 and version 2.
Version zero is never standard interestingly enough.
And you could have negative numbers too, but those are not standard either.

Murch: 00:11:27

So for example version 2 is required if you want to use CheckSequenceVerify.

Greg: 00:11:30

That's right, relative timelocks.
That’s why and anything above two is also in consensus.
Anything two or above has relative time locks, so that’s the natural.
Next number is three.
It has no additional consensus meaning, but from a policy perspective you can open up a new door perhaps.

Murch: 00:11:46

Right, so you would label your transaction as v3 and then your node would only permit a single child up to a thousand vbytes I think.

Greg: 00:11:56

Yeah, it’s an arbitrary number but so in the worst case the attacker can do almost 101 kilobytes.
So let’s call it a hundred to round it off.
So really you’re looking at about a 100X reduction, the rule three damage they can do if you think of it that way.

Murch: 00:12:12

And no additional children which makes the whole pinning topology more difficult.

Greg: 00:12:16

And the child must also be v3.
And v3 is implicitly replaceable at all times.
So even if there’s no full RBF in the network, there’s a problem with signaling inheritance with BIP 125.
So even if the parent, like version 2 today, if the parent opts in to replacement, the child doesn’t have to.
It’s kind of a loophole in some ways, and so you had to fix that loophole as well.

Murch: 00:12:41

So they’re always signaling replaceability by being v3?

Greg: 00:12:46

Yeah, so it’s simpler topology.
Based on this topology, we don’t know any major pinning vectors for this one because it’s easy to reason about.
And the hope is that if you have it there, then wallets can opt into this new regime, where it’s a simple way of doing fee replacement for smart contract proposals, vaults, things like that.

Murch: 00:13:08

So now we have this proposal out there and how are we going to use that?

Greg: 00:13:13

The canonical example I guess would be something like the Lightning Network with commitment transactions.
So it’s the challenge-response regime of Lightning Network where you need to be able to quickly get the last state on-chain if you need to go to chain.
The attacker today with the Lightning Network, if the mempool is full, they can take a transaction and then put a really large child or many children, low fee, and then stick it in the mempool and then it makes it inefficient, I guess uneconomical to replace essentially.
So the counterparty is burning your fee, your funds pretty much.
So that would be one.
Another is batch payments.
Today it’s when you’re doing batched payouts to many customers for example, it’s unknown if your customers are gonna sweep their funds doing something stupid.
So it’s very hard to consistently RBF a transaction.
So theoretically you could use that for RBFing if they’re okay with the TXID changing in this example.
I also call it a RBF carve-out.
This policy is a carve-out for RBF behavior, replaced by fee behavior.

Jonas: 00:14:17

Cool.
Tangently related to that is a proposal to reduce the standard transaction size.
And so what?

## Reducing the standard transaction size to 65 bytes PR

Greg: 00:14:25

Yeah, that’s actually, I think it’s, is that in 24?

Murch: 00:14:29

Yeah, was it?

Greg: 00:14:30

It’s already merged into master in Bitcoin Core.
So yeah, it’s fairly tangential, but one thing I was looking at, and I noticed that I interact with this problem every three years, and then I forget I did, but there was a security issue with SPV proofs in Bitcoin because of the way Satoshi designed the Merkle tree proof.
And essentially, it’s a way of, if some miner had some hash, if some attacker had mining hash power, they could make a fake proof and then trick someone who doesn’t fully validate the chain.
And this means transactions of size 64 bytes could theoretically make a fake proof possible.
So because it’s just the size of the two leaves when you’re doing 32 bytes plus 32 bytes, 64.
It makes it look like an inner part of this Merkle tree, but it’s actually a leaf.
It’s actually a transaction.
It’s not a TXID, it’s a transaction.

Murch: 00:15:25

So you could pass off TXID as being part of a Merkle tree where it’s actually not.

Greg: 00:15:32

Yeah, things like tap trees, they’re not vulnerable just because it’s a common mistake in Merkle trees and Satoshi fell onto this one.
But it was secretly found and reported.
So Bitcoin Core instituted a restriction that anything less than 82 bytes, I believe.

Murch: 00:15:50

You worked on it.
Why are you looking at me?

Greg: 00:15:52

I didn’t make this patch.
It’s 82 bytes, because it’s saying, OK, if you have a SegWit input and a pay to witness pubkey output, which is one of the smaller outputs.
How big would this transaction be?
And they said, OK, we’re going to do this.
Anything smaller than this will not be relayed on the network because it costs too much to allocate memory or something.
They just made up an excuse, which covered the 64 byte case.
And this is witness stripped, meaning non-witness data.
And that’s why 82, that number, shows up, not 100 and whatever, Mr. Bitcoin calculator, Murch.

Murch: 00:16:28

So if you take off the witness data from a native SegWit transaction, the output is 36 bytes.
The empty script against one is 41 together plus 31 for the output is 72 and then 10 for the header is 82.
Yes.

Greg: 00:16:48

So that’s the number made up.
So it had some idea of legitimacy, but it was just hiding another issue.
And then after it was revealed, I made sure to add a comment to the code base.
So I found it very confusing.
So there’s this comment there.
And then I started running into this use case where they have small UTXOs. People just want to burn them to fees to clean up the UTXO set, but you’d actually an `OP_RETURN` output.
So you did this 82 math, and that’s assuming is it 22 bytes in the script pubkey?
It’s a push zero byte push 20.

Murch: 00:17:20

Eight for the amount, one for the length of the script and then 20.

Greg: 00:17:24

And to make an `OP_RETURN`, the most compact `OP_RETURN`, you only need one byte, the `OP_RETURN` itself.
You don’t even need a data push.
It’s provably unspendable.
So that saves you 21 bytes in burning and maybe that’s the difference in cleaning it up or something like that.
You could also do batched cleanup of UTXOs to make it bigger.
But I’ve seen a few different developers talking about this, the async people, Peter Todd.
And then also I had some other work I was thinking about building on top of v3 package, RBF proposal, where it’d also make more sense too.
So the debate came down to, well should we disallow 64 bytes exactly or anything less than 64?
Or what should the range be?

Murch: 00:18:08

Less or equal, yeah.

Greg: 00:18:08

Yeah, less or equal.
And what should the range be?
I had my opinion, people had other opinions.
And for now, this release, the 24, 25, I’m not sure, Bitcoin Core release, it’s going to start becoming standard to spend down to 65 bytes.

Murch: 00:18:24

So for example, if you have an `OP_RETURN` output or an `OP_TRUE` output, you could now have a transaction that is 65 bytes, but you’d actually have to stuff it with a few more bytes of…

Greg: 00:18:35

You’ll stuff `OP_RETURN` with four bytes or something like that.
Which is still a pretty good improvement.
And it’s also just easier to read the code.
It’s not as easy as disallowing 64 only, but that’s a quibbling for me, I guess.

Jonas: 00:18:52

Let’s get back to the main thread, which is our march towards Eltoo.
So the next…

Murch: 00:18:58

LN-Symmetry.

Jonas: 00:19:00

Oh, sorry.
LN-Symmetry.
Is Eltoo truly dead as a term?

Greg: 00:19:04

No. No one’s carrying it except for me, so I can pick whatever I want.

## March to LN-Symmetry

Greg: 00:19:07

I see.

Murch: 00:19:08

The problem really is that the term is such a naming clash.

Greg: 00:19:13

It sure is.
And for context, I say LN-Penalty to refer to the current scheme.
Lightning Network with penalty.
And I specifically mean the BOLTs that are in today and that flavor of...

Murch: 00:19:23

I’ve heard that before.
I think that’s somewhat established now.

Greg: 00:19:26

I’m just putting it out there.
When I say LN-Penalty, I mean look at the BOLTs today, what’s deployed today, essentially.

Murch: 00:19:32

Yeah, the whole thing with punishment transactions.

Greg: 00:19:34

Punishment transactions and even the way the transactions are structured.

Murch: 00:19:38

Yeah, the commitment transactions are built.

Jonas: 00:19:41

So let me ask you a question.
The asymmetry in the penalty mechanism is a deterrent?

Greg: 00:19:46

Yes.

Jonas: 00:19:47

Are we going to have something similar in Eltoo?

Greg: 00:19:49

So this is where I was saying, I’m calling that LN-Symmetry, and then there’s LN-Penalty.
So I call our own penalty this way, it’s transaction structured.
You can also do any, so for Eltoo you need `ANYPREVOUT` which is essentially omitting the previous output so you can they say rebind, but when I implement it ends up being you just bind.
You only bind at the last second.
You pick your UTXO at the last second that you’re trying to spend based on the state update of the channel, that’s hit the chain.
With `ANYPREVOUT`, there’s actually a number of flavors of architectures you can pick.
So there’s one called DARIC, D-A-R-I-C.
It’s got a paper, it’s well written, it’s got a nice table.
It’s actually very consumable to an engineer.
That uses `ANYPREVOUT`, maintains penalties, but they restructure the transactions to be, in my opinion, simpler and superior to the current architecture, even beyond APO.
Just the way the transaction structure’s cleaner.
It removes things like second stage transactions for HTLCs, all this pre-signing of other stuff, and it brings down watchtower state and node state down to O(1), using `ANYPREVOUT` specifically to reduce the state.
That has 100% penalties like LN today, LN-penalty.
Then LN-Symmetry has no penalty mechanism because it’s what I also call vanilla Eltoo, which is just, you just have a series of state updates and then once the dust settles, the settlement comes out, and money just flows out.

Murch: 00:21:27

I feel that, yes, it doesn’t have an explicit punishment, but you do have to bring your own fees.
So you do have to pay money in order to broadcast in the old state.
And strictly speaking, if you assume that either a watchtower or the counterparty is active, then eventually it will settle on the last state, so you are just strictly initiating by paying.
However, the other party has to pay for the update, so you’re paying the same amount.

Jonas: 00:21:55

That seems like it’s worth a try.

Greg: 00:21:58

It only is worth a try if you know your counterparty is going to be offline and not come back in a reasonable time, in my opinion.

Murch: 00:22:03

I mean the other party has to pay for the second update.

Greg: 00:22:07

Yeah.

Murch: 00:22:07

So you pay the same if you broadcast the old or the new.

Greg: 00:22:10

Yes.

Murch: 00:22:11

But you do burn your reputation too.

Greg: 00:22:12

If you have to go on a unilateral close, the incentive is to pick whatever is nicest for you.
Now, there’s the other one.
If you know you have the last version, it means you can get your funds out faster.
Because if the counterparty comes online, they reset the clock.
So there’s a little bit there, but maybe you’ll go for the thing with the biggest balance or something.
That’s true.

Jonas: 00:22:35

Yeah, rolling the dice or putting in a pinning attack or...

Greg: 00:22:41

I suspect economic arguments to stay online, stay cooperative, and then if you’re not cooperative, there’ll be defaults.
I don’t know if people would make defaults to try to cheat.
It’ll be interesting to see.

Murch: 00:22:55

People also see when you do a unilateral close, and I think they might be able to find out which side initiated it or both parties in the channel might just be tainted.

Greg: 00:23:08

In the LN-Symmetry case, it’s completely symmetric and adding asymmetry just...

Murch: 00:23:15

A lot of people say we still need a punishment.
Otherwise, how can we ever make sure that people collaborate and are nice?
But honestly, if you look around, there’s no unilateral closes that go awry.

Greg: 00:23:29

The incentives are going on-chain when you could have gotten mutual close or stay online is obviously worse.
So the question is, what is incentivizing?
My argument is that keep your node online.
And I don’t think people are going to close on you.
I just don’t think so.

Murch: 00:23:45

As long as it stays symmetric, it’s of course much cleaner and easier to build and the watchtowers are simpler and smaller.

Greg: 00:23:51

There’s other architectures too, kind of in the middle, where you can opt in to a certain amount of fees.
They can do fractional fees.
So Anthony Towns has some write-ups on this.

Murch: 00:24:01

That was interesting with…

Greg: 00:24:03

I believe it all works.
And so you have this kind of different flavors.
I think I’ve been implementing the Eltoo, the LN-Symmetry version of it.
And I’ve proven out and written a spec for it.
So I think `ANYPREVOUT` fits pretty much any of these buckets and a lot of these same tricks that we’ve developed for LN-Symmetry can be reapplied.
So for example, reducing the state machine for committing to updates.
In Lightning network today it’s one and a half round trips.
And it’s actually asymmetrical in updates too.
So you’re sending each other updates all the time, and eventually you converge if you stop proposing updates.
But there’s a possibility that it just continues to diverge.
And from a spec perspective and a reasoning perspective, it’s really tough to think about, I think.
My work on LN-Symmetry has been much simpler to think about.
There’s exactly one set of state and the same would be with DARIC and Anthony Towns version 2.
There is some asymmetric state, but you don’t have to do asymmetric updates if that makes sense.

Murch: 00:25:07

Right.
I think.

Greg: 00:25:08

You take a leader, they propose updates and you rotate.

Murch: 00:25:11

The gist of AJ’s thing was that the payout for the commitment transaction is bigger than the input.
So when you go for closing it, you have to provide more funds in order to have sufficient funds to create the outputs, and that’s asymmetric.
So the closer has to pay more.

Greg: 00:25:30

Since the state’s asymmetrical, you can also just reduce the amount of output.
So the cheat path decrements the cheaters amount by as many Satoshis as you want.
Of course, you have to agree on this amount.
It could be an interesting threading the needle situation where people want a little bit of penalty but not a lot, because I know a number of people with big money that don’t wanna put big money in a Lightning channel because it’s just super scary.
Like an honest mistake can be 100% loss.
It’s really scary.

Jonas: 00:26:03

`ANYPREVOUT` isn’t the first proposal to make Eltoo happen.
So it started with `SIGHASH_NOINPUT`.
Yes.
And that seemed to be.

Greg: 00:26:13

Yes, there’s `SIGHASH_NOINPUT`.
That was Christian Decker.

## BIP118 - SIGHASH_ANYPREVOUT

Greg: 00:26:17

Was it a full BIP?

Jonas: 00:26:18

I think AJ was running with that.

Greg: 00:26:20

So AJ also did his own `ANYPREVOUT`, and then it was separate, and then they combined.
So at some point, they combined the concepts.
And this is BIP 118, which hasn’t changed in a while.
Seems pretty static.
Well, the text has changed.
The actual format hasn’t.
And it’s built on Taproot.

Murch: 00:26:39

And it’s very comprehensively described on <anyprevout.xyz>.

Greg: 00:26:45

I think that website’s going away.
Fiatjaf says he’s letting the website expire, the certs or something, or the domain or something.
It was just two days ago.
So it’s Taproot only and only in tapscript spends.
So it’s kind of a mild incentive to say, hey, don’t try to use this for normal transactions because this rebinding thing is pretty powerful, meaning kind of dangerous, and you don’t want to use it for everyday spends because this would mean address reuse can end up in losses pretty much.

Murch: 00:27:13

Although as far as I understand APO also makes you commit to a specific amount.
So any UTXO that has the same script...

Greg: 00:27:22

There’s two amounts.
Sorry, there’s two versions of the flag.

Murch: 00:27:25

There’s `ANYPREVOUT_ANYAMOUNT` and there’s `ANYPREVOUT`.

Greg: 00:27:28

`ANYPREVOUTANYSCRIPT`, which also allows any amount.
And this doesn’t commit to the script that it’s signing for.
And then there’s just `ANYPREVOUT`.
These are two versions of it.
I ended up using, I think, `ANYPREVOUTANYSCRIPT` only, because the reattaching over scripts is pretty important for my use case.

Jonas: 00:27:50

And it seems like `ANYPREVOUT` was marching towards next in line, but it sort of got caught up in the Covenant kerfuffle as well.
As a champion of the soft fork, how are you thinking about the sequencing or not?
Or anything to do with it?

Greg: 00:28:05

That’s a loaded question.
As a champion, are you talking about yourself?
I’m not the champion.

Jonas: 00:28:09

So I’m no champion.

## Softfork and activation history

Greg: 00:28:11

Currently I’m championing soft forks is really hard.
Historically, I went through the history and I’m trying to think of the last soft work that was primarily championed by its author.
And it’s like CHECKLOCKTIMEVERIFY, I think with Peter Todd, I think is the last one.
Because CHECKSEQUENCEVERIFY was written by Mark Friedenbach.
He left the effort, and then BtcDrak took it over and dragged across the finish line.
We have SegWit, which is a little different.
Everyone and their mom wanted it, but you know, so Peter...

Jonas: 00:28:43

Not everyone.
Everyone that’s still around.

Greg: 00:28:47

Everyone that didn’t want a schism already for other reasons.
Let’s just be honest.
There’s a reason, it’s a different community.
And then just showed the truth, that it’s just different communities and it needed a split.
I’m glad that people ended up just splitting off in the end because we don’t have to be married to each other if we don’t want to work together.
Bitcoin’s about working together.
So SegWit was like written by Pieter Wuille, but I don’t think he really championed an activation.
I think he allowed a BIP9 activation to get merged and then he didn’t lift a finger when it was floundering because he’s like, "I’m okay waiting years to get it" is pretty much his response, which I think is a valid response to it.
And then with Taproot, he literally did nothing to drag it across the finish line aside from make sure it’s high quality, high quality tests, things like that.
And we relied on other contributors to take up that.
So I’ve made this axiom that I think the author should be different from the champion because it’s too much self-investment, I would say.
And also it’s a signal, if you’re championing your own proposal, correct signal, but it’s a signal that the uptake’s not there, the mind share.
So Jeremy Rubin with `OP_CHECKTEMPLATEVERIFY`, it’s got good stuff, and I’ll circle back to what I like about it, the effort, but it seemed to be too much on Jeremy’s shoulders to champion it.
Other people would look at it, some people would say, yeah, it’s good, and then go back to their day job and not lift a finger to help, and that ultimately hurt it.
There’s a bit of a renewal in that space with `OP_VAULT`, because it’s kind of a superset of behavior, so maybe we’ll get to revisit that behavior.

Murch: 00:30:18

I think that for a few of those soft fork proposals there were also just a bunch more authors, so it felt like there was more mind share already.

Greg: 00:30:25

Yeah, of course.
I guess if you have 50 authors, but that’s kind of crowding the boat.
But essentially having more than one person really active in evangelizing the tech and getting the use cases out there.
Now what I really liked about `OP_CHECKTEMPLATEVERIFY` was all the tooling being built to prove it out.
And so that’s part of the effort here is with `ANYPREVOUT`, I don’t want to champion it right now from an activation perspective.
I think the community is pretty split right now on what to do.
But we can build the knowledge and build up the tooling.
And also, side note, I’m going to eventually when I get this stuff all merged.
And there’s a lot of preparatory work to get there, a lot of quality of life improvements for Core Lightning right now.
But once I get there, then I can port this over to the Liquid Network, which already has the crazy covenant, powerful covenants, and I’ll essentially do an `ANYPREVOUT` widget.
So use introspection to emulate `ANYPREVOUT` and launch it there.
So it’s simple.

Murch: 00:31:21

So with Core Lightning on the Liquid Lightning Network, you’ll be able to test LN-Symmetry there.

Greg: 00:31:30

Yeah, still have to get package relay and all that, all the stuff, but it’s like a roadmap to getting something that’s usable and simpler.

Jonas: 00:31:37

We’re not going to use Litecoin as our activation playground anymore?

Greg: 00:31:41

No.

Murch: 00:31:43

They’re finally doing their own thing.

Greg: 00:31:45

Yeah, they are doing their own thing, actually.

Murch: 00:31:47

MimbleWimble extension block.

Jonas: 00:31:49

Oh, boy.

Greg: 00:31:50

Yep, they’re off on their own, which is great.

Jonas: 00:31:53

The sequence of events is package relay, underway.
Then we have APO, underway.

Murch: 00:32:01

Sort of.

Greg: 00:32:02

Tooling, specs, building on top, proving it out.

Jonas: 00:32:05

Okay.
And then we have LN-Symmetry underway.

Greg: 00:32:10

Yeah.
So building LN-Symmetry is kind of a necessary preparatory step.
Proving out that it actually does what we want.

## Ephemeral anchors

Greg: 00:32:18

At the beginning I was I started doing research on it and I ran into, how are we gonna pay for fees for this?
Because these update transactions, they can’t have fees, because you’re contesting who has the money.
And there’s no penalty to draw from.
There could be any number of updates, so how do you not siphon off the channel funds while you’re doing these updates, while you’re doing this channel response period?

Murch: 00:32:40

So since any update can bind to any predecessor, the amount of money that is available has to be the same for every transaction so that you can still pay out the same amount.
So linking them all together cannot leak money.
So since there’s no fees, there’s no money left for fees because nothing is going anywhere else, you have to bring your own fee?

Greg: 00:33:01

So, Murch could say, well, why can’t you just use `SIGHASH_SINGLE`?
So it’s one input, one output, and then using `SIGHASH_SINGLE`, you can attach on your own inputs and outputs as fees, bring your own fees.
Well, then you get back to this pinning issue, because every update could be pinned 100x or something like that.

Murch: 00:33:18

With `SIGHASH_SINGLE` any...

Greg: 00:33:21

And so the classic example also even without the spam attack, they could, your counterparty can bundle the attack, can stick yours along with a bunch of other people’s attach a fee to it and say, somebody has to pony up all the funds to bump this transaction.
It’s a bundling like grief attack.
So that’s no good.
And so I was thinking of more robust ways of doing this.
And this is where I came up with the idea of ephemeral anchors, which is, I’ll dive into this now.
So in channels today and Lightning network, you have this anchor output, which is some, it’s like 330 Satoshis, kind of a useless amount, just to make it relayable.
And so maybe someone will clean it up in the future.

Murch: 00:34:02

And do you need one or two of them?

Greg: 00:34:04

Today you need two, because you can’t collaboratively double spend each other safely.
There’s key material and you need to be able to spend your own independently to fee bump when necessary.

Murch: 00:34:19

So every single time there’s a unilateral close, at least one of those anchor outputs hangs around.

Greg: 00:34:25

Yeah, it hangs around.
There’s a time lock, like 16 blocks or something.
So once it sits there for 16 blocks, then it becomes an anyone-can-spend type thing.
But if fees are high, it’s not gonna get swept.
Or if the pre-image is not known, that sort of thing, it could happen.
But also it’s the siphoning off.
So you’re siphoning off this value with this anchor output.
That’s a no-go.
So I need a zero value anchor, but a zero value anchor means you have a zero value output sitting in the UTXO set, which is also no-win.
But we have package relay in this mystical new world that I’m trying to build with other people of course, but this Eltoo world.
So perhaps we can use package relay and say, OK, if you propose a package and a transaction has a dusty-looking output, allow it, if and only if it gets spent in the same package.
So in this v3 context, this is simpler to think about, does the parent have an output that’s dust?
That’s OK, as long as it’s spent by the child.
There’s additional rules on here.
I actually mark the output by using the opcode `OP_2`, which is one more than `OP_TRUE`, because everyone uses `OP_TRUE` for testing.
So it just breaks like a million tests.
So I’ll just pick the next one.
That was actually a Luke Jr. idea in 2017.
I found old emails talking about this kind of similar idea.
So it’s an OP, it’s a script of `OP_TRUE`, which means no key material needed and no witness data needed to spend it.

Murch: 00:35:49

It resolves the stack to true automatically because there’s only a value that is…

Greg: 00:35:53

It's truthy.
And the script interpreter says, is this truthy?
And then it says, yeah, this is truthy and then it’s successful to spend.
So it’s watermarked that way.
So it says, if you have an output like that, it must be spent, and you can only have one of them.
So each parent transaction can have one of those.
It means the parent has to be zero fee for mempool policy DOS reasons.
There’s a lot of complexity here.

Murch: 00:36:17

Right, if the parent had more fees, it could get mined by itself.
And then dust output would hang around.

Greg: 00:36:25

That’s right.
Also, if the child is evicted for RBF and doesn’t spend the parent, so like the child gets evicted and the parent’s alone, we wanna make sure the parent is not mined by itself.
Yeah, that’s the other one.
So there’s a couple ways of doing this.
So zero fee ensures that it’ll hang around by itself and the miner won’t pick it up, or if certain set of patches happen, it can get evicted too, in a clean up pretty much.
Say, oh, you’re zero fee, get out of here.
And you have this one parent one child topology, and it must be spent.
Therefore, it’s like a mutex lock for spending an output on the parent.
So if someone is spending a child, someone’s spending an output from the parent, you can RBF that spend no matter where it is.
And so I think this is very powerful for when it comes to, let’s go back to Lightning Network today.
If we had ephemeral anchors, we’d make two keyed anchors of 330 bytes become one zero value anchor that doesn’t require any key material.
And then these outputs, let’s see, certain outputs in the LN-Penalty case would work.
Let’s say the two remote output, which is, let’s say Alice and Bob are in a channel.
Alice goes to chain with her version.
Alice went to chain with her commitment transaction.
Bob can immediately sweep.
If it’s the correct, let’s just say it’s the last one, Bob can immediately take their balance, their remaining balance, non-HTLC balance.
They can just immediately spend it.
But that’s not true today in the mempool because it has a time lock and things like that.
So you can’t actually child pays for parent using that output.

Murch: 00:37:56

Well the counterparty can, but Alice cannot.

Greg: 00:37:58

No, they’re all time locked with one lock CSV because of pinning.
Because you can’t spend the anchor then.
So if they’re allowed to spend in the mempool…

Murch: 00:38:06

Oh, because the anchor output is the only one that can be spent.
And now we have one anchor output that can be used by anyone.

Greg: 00:38:12

Yeah, so in all these outputs we can drop this one block CSV relative time lock.
They all have them because of this pinning issue, except for the anchor.
The anchors do not.
So we can drop all these concepts.
We can go back to more composable scripts, Miniscript-compatible scripts.
These things are not Miniscript-compatible because you’re adding these random locks everywhere.
It also helps with things like splicing, where you say, I want to splice out to an arbitrary destination.
But you can’t really prove to the other person necessarily that it has a one block CSV to stop pinning.
And maybe it’s a Coinbase address.
And they’re not going to hand you one of these.
They’re just gonna give you, pay to witness pubkey or pay to Taproot or something.
So from a composability’s perspective, you can take this, if we rework it, then you could have a channel with one anchor, no value draining out of it.
All the outputs are immediately spendable, well, some are not because of the challenge response period, but the immediately spendable ones can be used for child pays for parent to bring fees up by itself.
And also things like splicing and you can splice into a new funding output versus, and not have to prove that there’s a time lock in there.
You don’t have to tell your counterpart anything, you just send them funds here and it ends up being some other smart contract.
So I think it’s really powerful from a composability perspective as well.
I could talk about one more, it’s the motivations for ephemeral anchors from a use case perspective.
So one of the kind of use cases that really stuck out to me is that with ephemeral anchors, you can completely partition your custodied funds, so the funds inside a smart contract or inside a set of keys, versus the fee Bitcoin.
The Bitcoin you’re paying for fees.
These are two separate concepts.
In a personal wallet, if you just pull out a wallet, you’re generally commingling them and it’s okay because you’re a person, you’re just one person.
You’re not an LLC even necessarily, but from a custody perspective or from accounting perspective, it’s kind of a nightmare.
For example, I worked at BitMEX for about two years, and there’s very strict accounting about where Satoshis go.
Once Satoshis are off, alarms start going off.
It’s like, hey, where’d this go?
And you have to account for it, which makes accounting for fees really tricky.
You either make it kind of hacky or you kind of lie to the system, hey, there’s not that many Satoshis here, and then you secretly use them for fees because from an engineering perspective, you just want to use them in the correct engineering way, not from an accounting perspective.
An ephemeral anchor means a custody provider can do a batch payout, put an ephemeral anchor on there, and then the wallet ops team can run a different wallet which grabs that fully signed transaction and attaches their own inputs to the child pays for parent setup.
You have clear separation, clear delineation of user and engineering slush funds.

Jonas: 00:40:58

You lose that pop-up that’s in an exchange that says, this is why you’re paying fees.

Greg: 00:41:05

Yeah.

Jonas: 00:41:06
5

It’s like essentially the company would pick up the fees for you.

Greg: 00:41:09

Yeah.
And that’s the natural thing.
It’s really terrible when you have to tell a user to pick fees.
So BitMEX did do that for Bitcoin.
I’m not sure if they’re doing it anymore.
I can’t be a user as a US citizen.
But it was pretty awful because of this restraint, which was very prescient in some way, they were built in the aftermath of Mt. Gox.
But because of this, and this lack of engineering flexibility from a relay perspective, you had to have a slider and say, "how many Satoshis do you want to send as a fee?" You don’t even know how big the transaction is going to be.
So essentially having an engineering wallet ops slush fund for fees, I think that works much cleaner.

Jonas: 00:41:46

And it incentivizes them to get the fees right, as opposed to overpaying.

Greg: 00:41:52

They target, say, fees are sort of like this, and they set it static.
And then if they make money, it goes in the pile, on the fee pool pile.
If it drains, you expense it or whatever.

Jonas: 00:42:03

Yeah, as I’m listening to this, it strikes me that you have this long timeline with a lot of different features, and there’s a sequence to making sure that a bunch have to get in before you’re able to do the next stop in the sequence.
But it also seems like each of these features in isolation is a value add.

Greg: 00:42:23

Yes, definitely.

Jonas: 00:42:23

And so package relay, this has been talked about for a very long time.
It’s on its way.

Greg: 00:42:28

At least 2013 or something.
As long as I’ve been in the space.

Jonas: 00:42:30

It’s on its way.
Ephemeral Anchors seems quite valuable just on its own.
Is that the case for `ANYPREVOUT` as well?

Greg: 00:42:40

As a consensus change, the bar is so high.
It can’t just be a nice thing to have or a really nice cleanup, but everyone has to agree because you’re encumbering other people with logic.
Even if they run like Libbitcoin or BTCD, everyone has to sync up on what this is and everyone has to...if we find out that something’s wrong with v3 or whatever, we can always change it in the future.
With consensus change, you can’t really.
Once people put money in, you can’t just freeze that pattern.
So the stakes are just much higher, I would just say.

Jonas: 00:43:15

But I guess I haven’t heard of `ANYPREVOUT` being championed outside of Eltoo.

Greg: 00:43:23

Yeah, that’s another, that’s a great question.
I was just talking about this yesterday.

## Is ANYPREVOUT useful outside of LN-Symmetry?

Greg: 00:43:27

I was like, `ANYPREVOUT` is pretty powerful, but only has a few use cases where it really hits a home run, I would say.
Maybe that’s big enough.
Maybe it’s just the biggest home run.
One grand slam or something.
But it’s also possible that, it depends on your theory of what a soft fork should do.
I think it makes things like channels simpler to reason about and build, whether you like penalties or not.
So I think for that, I think it gets a nice big green check mark, but it doesn’t wax your car, doesn’t make faults exactly.
You can do some kind of like CTV emulation, some parts of it, but it’s not a superset or it’s not a…

Murch: 00:44:07

It’s bigger and less powerful or something.

Greg: 00:44:09

Yeah, they’re intersecting circles in a Venn diagram, so to speak.
So it can do some things that are interesting that are byproducts, like with `ANYPREVOUTANYSCRIPT` because you’re emitting your own script you can stick that you’re signing for you can stick the signature in the script it’s like self-referential and say this transaction must look like this and can only commit to the shape of the outputs and the n-lock time and n-sequence, things like that.
So it does some quirky things like that.
But if we really like that, maybe we should have CTV, or maybe we should have `OP_VAULT`.
So that’s an open discussion.
And then this is where all the contention is.
It’s not all the contention, but of the who’s next questions, this is a big one.
Should we be aiming really small, missing small, you know, doing the key killer product releases, so to speak, and then focus on the future, maybe more systematically, or I don’t know what the solution is here.
But I’m really focused on, there’s a pile of things to improve today’s consensus regime, so I’m kind of focused on that for now.

Jonas: 00:45:19

But you’re going to stay away from activation?

Greg: 00:45:21

For now, yeah.

Jonas: 00:45:23

That is a seemingly a pretty big open question.

Greg: 00:45:25

I don’t know how much of this is Twitter psyop or whatever, but people seem pretty contentious about it.
They’re like mad that people are making new releases of Bitcoin Core almost.
"Why do you need to work on it?" I think these people have no idea what they’re talking about because they don’t understand how security works or build systems work or anything like that.

Murch: 00:45:44

Or that software just also ages in the context of what operating systems...chips and so forth.

Greg: 00:45:53

Like build systems.
Try building something that hasn’t been touched in 10 years.

Murch: 00:45:57

Yeah, exactly.

Greg: 00:45:57

Kind of a headache.
So I have to wonder how much of this is just Twitter nonsense or is real.
In the dev community, I think it’s a little less contentious in some ways.
People have their preferences, but they understand the pluses and minuses of those a little better.
So it’s a little more respectful, I’d say.

Jonas: 00:46:15

But Eltoo seems to be, sorry, LN-Symmetry seems to be supported across the board.

Greg: 00:46:22

Some people still like penalties.
Now I still think, well, maybe we should just look at getting `ANYPREVOUT` and do DARIC.
Because I think it’s like a wonderful cleanup to the current protocol.
If you had DARIC plus ephemeral anchors and stuff, I could make you a very nice set of BOLTs.
I have BOLT specs that seems very nice and shorter.
And watchtowers are much easier, that sort of thing.
So I think there’s still some choices to be made.
But maybe there’s enough to start.
I need feedback from people.
When I talk to people, I say, I’m really excited about Eltoo or LN-Symmetry or these kind of setups.
But they’re all busy doing their own thing, and they’re busy trying to stay away from politics.
I totally get that.

Jonas: 00:47:01

DARIC is not something I’ve actually heard of, and so why is that not more, not allowed in the discussion?

Greg: 00:47:06

It’s an academic paper, and they didn’t do much to spread it in the dev community, but it’s pretty straightforward.
It’s a well-written paper.
I think Shinobi pointed it out to me.
There was a predecessor called generalized payment channels, which was kind of, I’m not gonna say garbage, but impractical.
And then it was like, DARIC was like a successor that was a much more practical instantiation.
And actually it seems like they understand the problem space, the engineering problem space, much better somehow, even though they’re academics.
So kudos to them.

Jonas: 00:47:36

Cool.
Well, it was really great having you.
This was a good talk.

Greg: 00:47:39

I enjoyed it.
Thanks for having me on.

Murch: 00:47:40

Yeah, thanks for coming in.

Jonas: 00:47:51

He is very articulate about those subjects.
That was a good episode.

Murch: 00:47:56

I think I might have led him astray a few times and we got a little bit in on different branches in the conversation.

Jonas: 00:48:03

That’s what this is all about.

Murch: 00:48:04

But now you can totally talk to all your friends about APO and LN-Symmetry.

Jonas: 00:48:10

That’s right you know all the acronyms and you’re gonna be a hit at the parties.
Okay hope you enjoyed the episode we’ll try to get another one out soon.
Bye.