---
title: "SIGHASH_ANYPREVOUT, ephemeral anchors and LN symmetry (ELTOO)"
transcript_by: kouloumos via tstbtc v1.0.0 --needs-review
media: https://podcasters.spotify.com/pod/show/chaincode/episodes/Greg-Sanders--SIGHASH_ANYPREVOUT--ephemeral-anchors-and-LN-symmetry-ELTOO---Episode-29-e1v1dc3
tags: ['eltoo', 'ephemeral-anchors', 'package-relay', 'rbf', 'sighash-anyprevout']
speakers: ['Greg Sanders']
categories: ['podcast']
summary: "Greg Sanders joins us to discuss ANYPREVOUT, ephemeral anchors and LN symmetry (a.k.a. ELTOO)."
episode: 29
date: 2023-02-15
additional_resources:
-   title: Package relay
    url: https://bitcoinops.org/en/topics/package-relay/
-   title: Pinning attacks
    url: https://bitcoinops.org/en/topics/transaction-pinning/
-   title: BIP125
    url: https://github.com/bitcoin/bips/blob/master/bip-0125.mediawiki
-   title: T-Bast's pinning attack summary
    url: https://github.com/t-bast/lightning-docs/blob/master/pinning-attacks.md
-   title: Package relay RBF
    url: https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-September/019464.html
-   title: PR
    url: https://github.com/bitcoin/bitcoin/pull/26265
-   title: 'Daric: A Storage Efficient Payment Channel With Penalization Mechanism'
    url: https://eprint.iacr.org/2022/1295
-   title: Two-party eltoo w/ punishment by AJ Towns
    url: https://lists.linuxfoundation.org/pipermail/lightning-dev/2022-December/003788.html
-   title: BIP118
    url: https://github.com/bitcoin/bips/blob/master/bip-0118.mediawiki
-   title: SIGHASH_NOINPUT
    url: https://github.com/bitcoin/bips/commit/98b7238f68d17f0e01275dd32075078702225356?short_path=2f8c560#diff-2f8c560480095b9f314d3a7e17cf7048a10f9a15b391acaf2c96412d5b4d4b9c
-   title: Ephemeral anchors
    url: https://bitcoinops.org/en/topics/ephemeral-anchors/
-   title: op_2 email by Luke
    url: https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2018-May/015945.html
---
Speaker 0: 00:00:00

With any PrevOut, I don't want to champion it right now from an activation perspective.
I think the community is pretty split right now on what to do, but we can build the knowledge and build up the tooling.

Speaker 1: 00:00:18

Hey Jonas.

Speaker 2: 00:00:19

Hey Merch.
We are back in the studio for a productive podcasting week.
We have InstaGibbs Greg Sanders.
So what should we talk to him about?

Speaker 1: 00:00:28

He's been looking a lot at mempool policy improvements.
And I think we're going to talk about v3 transactions, package relay, his recent work on ephemeral anchors, and then how that all hopefully compounds to us getting LN symmetry eventually.

Speaker 2: 00:00:46

Yeah, LN symmetry, otherwise known as L2.
I guess he's, he's championing to get rid of L2 and call it something better, more descriptive.

Speaker 1: 00:00:54

He has my axe.

Speaker 2: 00:00:55

All right, cool.
Enjoy the episode.

Speaker 0: 00:01:03

Good morning.
Hey Greg.
Morning.

Speaker 2: 00:01:06

Welcome.
Should we be calling you Greg or Instagibs?
Either is fine.
Greg's fine.
Greg.
Okay.
Yeah.
Welcome, Greg.
Glad to be here.
Nice to have you in the office for a couple days here.
Today we are going to talk about some of your work, some of the things you're thinking about.
You've been around Bitcoin for quite a long time.
Coming in, dipping out, come back in, doing some different things.

Speaker 1: 00:01:28

Second round, I round the block.

Speaker 0: 00:01:30

I've been in the industry the whole time, but, yeah, my open source contribution comes in and out depending on what my interests are at the time, pretty much.

Speaker 2: 00:01:37

What are your interests these days?
What are you thinking about?

Speaker 0: 00:01:40

These days, I've been focusing on a couple of things, but it focuses mostly around mempool policy and also L2, the application of Anyprevout.

Speaker 1: 00:01:50

You mean LN Symmetry, right?
That's right.

Speaker 0: 00:01:52

I'm rebranding it right now.
It's called LN Symmetry instead of LN Penalty, which means you can use Anyprevout to basically have a symmetrical channel state for Lightning Network channels.

Speaker 2: 00:02:05

Yeah, we're going to dive into all of those things.

## Package relay

Speaker 2: 00:02:07

Let's start with package relay and work up from there.

Speaker 0: 00:02:10

Right.
So there's been this idea for many years that the peer-to-peer transaction layer, you basically want to be able to Propose a set of transactions at the same time to a node for example one transaction could be too low fee But you can spend an output at a higher fee and do child pays for parent.
So this works today if the parent transaction is the fee is beefy enough to get in the mempool on its own But maybe not enough to get mined in a in a reasonable amount of time But it doesn't work if the fees too low.
So for example If you wanted a transaction that's zero fee, maybe you don't know what the fee is going to be, or you're basically done in a smart contract.
For example, like L2, you can't actually siphon off any fees.
So you need to somehow pay for the fees.
There's a few concepts of how to do it with consensus changes or smart SIGHASH changes.
But to do it in a policy way, it seems to make sense to have this package of proposals that you pass around the network.

Speaker 2: 00:03:10

How might this relate to some other terms that we've heard in terms of pinning attacks and things like that?

## Pinning attacks

Speaker 0: 00:03:16

Cpfp, Child Pays for Parent, it actually can cause and mitigate pinning.
Because basically, if you have a shared transaction, like a commitment transaction, a Lightning network with your counterparty, they go to chain with a too low fee version and then they spin off their own telepage for parent that's actually not good enough then if you want to RBF that it's actually very expensive and so that's one version there's many pinning attacks basically if you want to know what a pinning attack is read BIP 125 and look at all the rules and say, how could I make this more difficult to actually robustly fee bump a transaction?
That's pretty much what I do.
But there's been a lot of people thinking about it, working on it, and then recently, so the last couple years or so, Gloria Zhao has been working on package relay as a concept.
And then she was thinking initially, I think, more on the how do we gossip these, how do we put these in the mempool, but basically kind of a drop-in replacement for single transaction relay, in a sense.
But then she realized that, wait, there's all these pinning attacks.
She was talking to people who said, well, there's a pin here, pin there.
And it just, Package Relay by itself was insufficient, I guess, to the point, for robust fee management, pretty much.

Speaker 2: 00:04:31

So the mempool is now sort of become a crossroads for layer one and layer two in terms of discussions.
It's also, it's a problem.

Speaker 0: 00:04:41

It's hard.

Speaker 2: 00:04:42

It's hard.
And so like, are we thinking, given that you're thinking so much about mempool policy, are we thinking about a pretty big rewrite in terms of how it works?
Are we thinking about mitigation steps on DOS vectors that are currently there?

## Mempool policy

Speaker 2: 00:04:55

How do you approach it?

Speaker 0: 00:04:57

The current mempool policy is very DOS aware, Because we want to make sure that to now services expensive at least right in an ideal sense The denial of service would be someone spamming the chain with high fees, right?
They're just outbidding everyone That's kind of like the so-called ideal case where they're paying for the DOS, you know and so the attack is limited until they run out of, basically they'll run out of funds eventually, which we saw in 2017 or something.

## Stuffing the mempool - 2017

Speaker 0: 00:05:23

We had that crazy, you know, backlog, months-long backlog.
Mempool was full, completely full for months.
Whoever that was ran out of money pretty much because of the...

Speaker 2: 00:05:32

That was a malicious attack?

Speaker 0: 00:05:34

I think so.
At the time I wasn't convinced but it's pretty obvious like the volume is just crazy even compared to today.

Speaker 1: 00:05:40

I think there was some research on how all those outputs got spent later and it's been a while since I read this, but they could tie it together.
So it definitely looked like there was at least one entity that was stalking the mempool.

Speaker 2: 00:05:56

This was like block-sized war stuff.

Speaker 0: 00:05:59

I'm not a conspiracy theorist, but also it doesn't have to be a conspiracy, right?
It could be one guy just cranking out, you know, they have some Bitcoin to burn, they wanna make a point, they do that.
It was so bad that transactions were being dropped from the mempool like permanently.
And I know a guy who held onto a copy, and then months later just dumped like hundreds of megabytes of other people's transactions.

Speaker 1: 00:06:19

I noticed.

Speaker 0: 00:06:21

Yes.
So that's a little fun history that we haven't seen since because things have been mostly clearing out in a, you know, weekly fashion.

Speaker 1: 00:06:30

Turns out a bunch of people were not aware that when stuff drops from the mempool, that it could come back because it's still a valid transaction.
And they didn't invalidate those old versions.
And they paid some people twice when this cache of old transactions got resubmitted.

Speaker 0: 00:06:49

That might have been a digression.
Back to the kind of architecture.
So it's very DOS aware, but there's also like actual users, right?
So there's wallets and there's smart contracts.
And I think they're actually closer than some people let on from a sense of as a wallet, I'd want to robustly V-bump, but right now there's all these issues with it, right?
So for example, the Bitcoin Core wallet, it's kind of a self-made limitation, but I've seen this in a number of other places where I'd say, well, if one of the outputs has already been spent, I don't wanna double spend that parent transaction, because it could be very expensive or I'm not sure how to calculate the right amount, you know, so on and so forth.

Speaker 1: 00:07:22

Also just you don't want to surprise the counterparty.

Speaker 0: 00:07:26

Yeah.
TXID stability and stuff like that, which is also another concern like custodians or payment processors don't want to cycle TX IDs on people and because people don't understand it so it's yeah we have software tracks by TX ID instead of by payments I mean even informationally right a customer says like oh I'm seeing this transaction coming and I'm getting paid, then disappears, they freak out.
They say, where'd my money go?
This is like a real problem.
I was just talking to someone yesterday.

Speaker 1: 00:07:53

It's a customer support problem.
Expensive.

## Rewrite mempool or make the problem simpler

Speaker 0: 00:07:57

So the question is, how do we fix this?
So there's the big architectural override of how the mempool works.
Should we rewrite everything?
Okay, do something really, really smart, maybe DOS resistant.
I think there's just the design space is so huge, right?
I'm talking I think it's like a decade of work in some ways, right?
Or we make the problem simpler And so this is kind of the direction that a few people were thinking, I think Sue Haas, Blumat and others, but hadn't really written down like a proposal.
And so Gloria and myself and a few others kind of started thinking about how to make something that would work today with, in the short term I would call it, with minor changes to, for example, the Lightning Network could use it with minor changes versus something that would be bigger or more disruptive.

## Package relay RBF A.K.A. V3

Speaker 0: 00:08:42

And so Gloria has the package relay work and then on top she calls it package RBF proposal, also known as V3 proposal, or basically you pick a new version, Bitcoin transaction version three, and you basically say, okay, I'm opting into a simpler topology of unconfirmed transactions.
And so the mempools policy is basically, it's like a handshake agreement.
Okay, you wanna make a parent transaction and you might wanna fee bump it and we're gonna let you do that.
So basically you have one parent transaction and up to one child transaction.
So it's a parent child relationship and the child is limited in size, which fixes.
So basically the package size of two, which fixes some pinnings, go read those rules.
And then limiting the child to a certain size, which fixes rule number three, which is the common one people point out, which is basically you have to replace all the total fee of all the children you knock out of the mempool, which can be prohibitively expensive, and even if the child is not going to be mined in the next two weeks, right?
It's just absolute fee considerations.

Speaker 1: 00:09:49

Or yeah, in the old style, up to 100 transactions can be replaced, and of course, the total size of all that.

Speaker 0: 00:09:56

Yeah, so that's BIP, that's rule five, I think.
It's up to 100 transactions.
That's all fixed with here because you can only knock down two times the number of inputs that you double spend.

Speaker 1: 00:10:06

And if the confusion is not enough, BIP 125 does not actually fully align with what's implemented in Bitcoin Core.

Speaker 0: 00:10:13

So yeah, so Gloria did some Great work communicating not only what the, like she's done some great talks you should go look up, but also documentation about what are the design decisions of the mempool as today, descriptively, and then also some like prescriptive notions.
So in the beacon core repo, you can see that there's these Markdown files that have a great explanation of like why things are the way they are.
Because when I was like interested in mempool policy in 2017 or so, it's just kind of a spooky science.
You know, it's it's witchcraft a little bit like why is this here?
Why is this code here?
Who really knows, right?
I mean, if I cornered Suhas in a room, I could probably get an answer out of him.
But really systematizing that knowledge and getting it down and communicated to the wider dev community, at least, was very important.
And that's what she did.
So they're right.
So that's the v3 package RBF.
So basically says, I can RBF this parent efficiently, right?

Speaker 1: 00:11:05

Right.
So to recap, there's one transaction and it has to be a version 3 Bitcoin transaction so there's versions all over Bitcoin we're not talking about one segwit versions.

Speaker 0: 00:11:18

There's two standard ones today version one version two version zero is never standard Interestingly enough and you could have negative numbers too, but those are not standard either So for example version two is required if you want to use check sequence verify,
right relative time locks And so that's why and anything above two is also in consensus.
Anything two or above has relative time locks, so that's the natural.
Next number is three.
It has no additional consensus meaning, but from a policy perspective you can open up a new door perhaps.

Speaker 1: 00:11:46

Right, so you would label your transaction as V3 and then your node would only permit a single child up to a thousand Vbytes I think.

Speaker 0: 00:11:56

Yeah, it's an arbitrary number but so in the worst case the attacker can do almost 101 kilobytes so let's call it a hundred to round it off so really you're looking at about a hundred X reduction the rule three kind of damage they can do if you think of it that way.

Speaker 1: 00:12:12

And no additional children which makes the whole pinning topology.

Speaker 0: 00:12:16

And the child must also be v3 and v3 is implicitly replaceable at all times.
So even if there's no full RBF in the network, there's a problem with signaling inheritance with BIP 125.
So even if the parent, like version 2 today, if the parent opts in to replacement, the child doesn't have to.
It's kind of a loophole in some ways, and so you had to fix that loophole as well.

Speaker 1: 00:12:41

So basically, they're always signaling replaceability by being v3?

Speaker 0: 00:12:46

Yeah, so it's simpler topology.
We don't, based on this topology, we don't know any major pinning vectors for this one because it's easy to reason about.
And basically the hope is that if you have it there, then wallets can have, can opt into this new regime where it's a simple way of doing fee replacement for smart contract proposals, vaults, things like that.

Speaker 1: 00:13:08

So now we have this proposal out there and how are we going to use that?

Speaker 0: 00:13:13

Well so I mean the canonical example I guess would be something like the Lightning Network with commitment transactions.
So it's the kind of challenge response regime of Lightning Network where you need to be able to quickly get the last state on chain if you need to go to chain, right?
The attacker today with the Lightning Network, if the mempool is full, they can take a transaction and then basically put a really large child or many children low fee and then stick it in the mempool and then it makes it inefficient, I guess uneconomical to replace essentially.
So you're just burning their, the counterparty is burning your fee, your funds pretty much.
So that would be one.
Another is batch payments.
Today it's when you're doing batched payouts to like many customers for example, it's unknown if your customers are gonna sweep their funds doing something stupid.
So it's very hard to consistently RBF a transaction.
So theoretically you could use that for RBFing if they're okay with the TXID changing in this example.
I also call it a RBF carve-out.
This policy is like a carve-out for RBF behavior replaced by fee behavior.

Speaker 2: 00:14:17

Cool.
Tangently related to that is a proposal to reduce the standard transaction size.
And so what?

## Reducing the standard transaction size to 65 bytes PR

Speaker 0: 00:14:25

Yeah, that's actually, I think it's, is that in 24?
Yeah, was it?
It's already merged into master in Bitcoin Core.
So yeah, it's fairly tangential, but one thing I was looking at, and I noticed that I interact with this problem every three years, and then I forget I did, but there was a security issue with SPV proofs in Bitcoin because of the way Satoshi designed the Merkle tree proof.
And essentially, basically it's a way of, if some miner had some hash, if some attacker had mining hash power, they could make a fake proof and then trick someone who doesn't fully validate the chain.
And this basically means transactions of size 64 bytes could theoretically make a fake proof possible.
So because it's just the size of the two leaves when you're doing 32 bytes plus 32 bytes, 64, It makes it look like an inner part of this Merkle tree, but it's actually a leaf.
It's actually a transaction.
It's not a TXID, it's a transaction.

Speaker 1: 00:15:25

So you could pass off TXID as being part of a Merkle tree where it's actually not.

Speaker 0: 00:15:32

Yeah, so things like tap trees, they're not vulnerable just because it's like a common mistake in Merkle trees and Satoshi fell into this one.
But anyways, so there's this, it was kind of secretly found and reported.
So Bitcoin Core instituted a restriction that anything less than 82 bytes, I believe.

Speaker 1: 00:15:50

You worked on it.
Why are you looking at me?

Speaker 0: 00:15:52

I didn't make this patch.
It's like 82 bytes, because it's saying, OK, if you have a SegWit input and a pay to witness pubkey output, which is like one of the smaller outputs.
How big would this transaction be?
And they said, OK, we're going to do this.
Anything smaller than this will not be relayed on the network because it costs too much to allocate memory or something.
They just made up an excuse, which covered the 64 byte case.
And this is witness stripped, meaning non-witness data.
And that's why 82, that number, shows up, not 100 and whatever, Mr. Bitcoin calculator.

Speaker 1: 00:16:28

So if you take off the witness data from a native SegWit transaction, The out point is 36 bytes.
The empty script against one is 41 together plus 31 for the output is 72 and then 10 for the header is 82.
Yes.

Speaker 0: 00:16:48

So that's the number made up.
So it had some idea of legitimacy, but it was just hiding another issue.
And then after it was revealed, I made sure to add a comment to the code base.
So I felt very confusing.
So there's this comment there.
And then I was like, I started running into this like use case where they have small UTXOs People just want to burn them to fees to clean up the UTXO set, but you'd actually an op return output So you did this 82 math, right and that's assuming is it 22 bytes in the script pubkey?
It's a push zero byte push 20.

Speaker 1: 00:17:20

Eight for the amount, one for the length of the script and then 20.

Speaker 0: 00:17:24

And to make an operturn, the most compact operturn, you only need one byte, the operturn itself.
You don't even need a data push.
It's provably unspendable.
So that saves you 21 bytes in burning and maybe that's the difference in cleaning it up or something like that.
You could also do batched cleanup of UTXOs to make it bigger.
But it was just kind of like, I've seen this, a few different developers talking about async people, Peter Todd, and then also I had some other work I was thinking about building on top of V3 package, RBF proposal, where it'd also make more sense too.
So basically the debate came down to, well should we disallow 64 bytes exactly or anything less than 64?
Or what should the range?

Speaker 1: 00:18:08

Less or equal, yeah.

Speaker 0: 00:18:08

Yeah, less or equal.
And what should the range be?
And basically, I had my opinion, people had other opinions.
And for now, this release, the 24, 25, I'm not sure, Bitcoin Core release, it's going to start becoming standard to spend down to 65 bytes.

Speaker 1: 00:18:24

So for example, if you have an OP return output or an OP true output, you could now have a transaction that is 65 bytes, but you'd actually have to stuff it with a few more bytes of...

Speaker 0: 00:18:35

You'll stuff op return with like four bytes or something like that, yeah.
So which is still a pretty good improvement.
Yeah, and it's also just easier to read the code.
It's not as easy as disallowing 64 only, but that's a quibbling for me, I guess.

Speaker 2: 00:18:52

So let's get back to the main thread, which is our march towards L2.
So the next...

Speaker 1: 00:18:58

L1 symmetry.
Oh, sorry.

Speaker 2: 00:19:00

L1 symmetry.
Is L2 truly dead as a term?

Speaker 0: 00:19:04

No. No one's carrying it except for me, so I can pick whatever I want.

## March to LN symmetry

Speaker 0: 00:19:07

I see.

Speaker 1: 00:19:08

The problem really is that the term is such a naming clash.

Speaker 0: 00:19:13

It sure is.
And for context, I say LN penalty to refer to the current scheme.
Lightning Network with penalty.
And I specifically mean the bolts that are in today and that flavor of.

Speaker 1: 00:19:23

I've heard that before.
I think that's somewhat established now.

Speaker 0: 00:19:26

Yeah, so I'm just putting it out there.
When I say LN penalty, I mean look at the bolts today, what's deployed today, essentially.

Speaker 1: 00:19:32

Yeah, the whole thing with punishment transactions.

Speaker 0: 00:19:34

Punishment transactions and even the way the transactions are structured.

Speaker 1: 00:19:38

Yeah, the commitment transactions are built.

Speaker 2: 00:19:41

So let me ask you a question.
The asymmetry in the penalty mechanism is a deterrent.

Speaker 0: 00:19:46

Yes.

Speaker 2: 00:19:47

Are we going to have something similar in L2?

Speaker 0: 00:19:49

So this is where I was saying, I'm calling that LN symmetry, and then there's LN penalty.
So I call our own penalty this way, it's transaction structured.
You can also do any, so for L2 you need any prev out which is essentially omitting the previous output so you can they say rebind but when I implement it ends up being you just bind you never you only bind at the last second you say like you pick your UTXO at the last second that you're trying to spend based on the state update of the channel, right, that's hit the chain.
Where was I going with that?
Oh, so there's, with any PrevOut, there's actually a number of flavors of architectures you can pick.
So there's one called Dark, D-A-R-I-C.
It's got a paper, it's well written, it's got a nice table.
It's actually very consumable to an engineer.
That uses any prev out, maintains penalties, but they restructure the transactions to be, in my opinion, simpler and superior to the current architecture, even beyond APL.
Just the way the transaction structure's cleaner.
It removes things like second stage transactions for HTLCs, all this pre-signing of other stuff, and it brings down watchtower state and node state down to O of one, using any private specifically, right?
To reduce the state.
And then there's, that has 100% penalties like Ellen today, Ellen penalty.
Then Ellen symmetry has no penalty mechanism because it's what I also call vanilla L2, which is just kind of, you just have a series of state updates and then once the dust settles, the settlement comes out, and money just kind of flows out, right?

Speaker 1: 00:21:27

I kind of feel that, yes, it doesn't have an explicit punishment, but you do have to bring your own fees, right?
So you do have to pay money in order to broadcast in the old state.
And strictly speaking, if you assume that either a watchtower or the counterparty is active, then eventually it will settle on the last state, so you are just strictly initiating by paying.
However, the other party has to pay for the update, so you're paying the same amount.

Speaker 2: 00:21:55

That seems like it's worth a try, right?

Speaker 0: 00:21:58

It only is worth a try if you know your counterparty is going to be offline and not come back in a reasonable time, in my opinion.

Speaker 1: 00:22:03

I mean the other party has to pay for the second update.
Yeah.
So you pay the same if you broadcast the old or the new.
But you do burn your reputation too.

Speaker 0: 00:22:12

If you have to go on a unilateral close, The incentive is to pick whatever is nicest for you.
Now there's the other one.
If you know you have the last version, it means you can get your funds out faster.
Like, because if the counterparty comes online, they reset the clock.
So there's like a little bit of there, but maybe you'll go for the thing with the biggest balance or something, right?
That's true.

Speaker 2: 00:22:35

Yeah, and I mean, rolling the dice or having a, you know, putting in a pitting attack or like.

Speaker 0: 00:22:41

I suspect economic arguments for, It's basically economic arguments to stay online, stay cooperative, and then if you're not cooperative, there'll be defaults.
I don't know if people would make defaults to try to cheat.
It'll be interesting to see.

Speaker 1: 00:22:55

People also see when you do a unilateral close, and I think they might be able to find out which side initiated it or both parties in the channel might just be tainted In the Alon symmetry case, it's a symmetric and adding asymmetry just yeah so a lot of people say we still need a punishment.
Otherwise, how can we ever make sure that people collaborate and are nice?
But honestly, if you look around, there's no unilateral closes that go awry.

Speaker 0: 00:23:29

The incentives are Going on chain when you could have gotten mutual close or stay online is obviously worse.
So the question is, what is incentivizing?
My argument is that keep your node online.
And I don't think people are going to close on you.

Speaker 1: 00:23:43

I just don't think so.
As long as it stays symmetric, it's of course much cleaner and easier to build and the watchtowers are simpler and smaller.

Speaker 0: 00:23:51

There's other architectures too, kind of in the middle, where you can opt in to a certain amount of fees.
They can do fractional fees.
So Anthony Towns has some write-ups on this.

Speaker 1: 00:24:01

That was interesting with...

Speaker 0: 00:24:03

I believe it all works.
And so you have this kind of different flavors.
So I think I've been implementing the L2, the LN symmetry version of it.
And I've proven out and written a spec for it, a bolt for it.
And so I think any prev out fits pretty much any of these buckets and a lot of these same tricks that we've developed for OnSymmetry can be reapplied.
So for example reducing the State machine for committing to updates right and like network today it's one and a half round trips.
And basically, it's actually asymmetrical in updates too.
So you're basically sending each other updates all the time, and eventually you converge if you stop proposing updates.
But there's a possibility that it just continues to diverge.
And from a spec perspective and a reasoning perspective, it's really tough to think about, I think.
My work on LN symmetry has been much simpler to think about, right?
There's exactly one set of state and the same would be with DARIC and Anthony Towns version 2.
Basically, it's there is some asymmetric state, but you don't have to do asymmetric updates if that makes sense.

Speaker 1: 00:25:07

Right.
I think.

Speaker 0: 00:25:08

You take a leader, they propose updates and you rotate.

Speaker 1: 00:25:11

The gist of AJ's thing was that the payout for the commitment transaction is bigger than the input.
So when you go for closing it, you have to provide more funds in order to have sufficient funds to create the outputs, and that's asymmetric.
So the closer basically has to pay more.

Speaker 0: 00:25:30

Since the state's asymmetrical, you can also just reduce the amount of output.
So the cheat path just decrements the cheaters amount by as many Satoshis as you want.
Of course, you have to agree on this amount.
It could be an interesting threading the needle situation where people want a little bit of penalty but not a lot, because I know a number of people with big money that don't wanna put big money in a latent channel because it's just super scary.
Like an honest mistake can be 100% lost.
It's really scary.

Speaker 2: 00:26:03

And so, Anyprevout isn't the first proposal to make L2 happen.
So it started with Sikash no input.
Yes.
And that seemed to be.

Speaker 0: 00:26:13

Yes, there's Sikash no input.
That was Christian Decker.

## BIP118 - SIGHASH_ANYPREVOUT

Speaker 0: 00:26:17

Was it a full BIP?

Speaker 2: 00:26:18

I think AJ was running with that.

Speaker 0: 00:26:20

So AJ also did his own Anyprevout, and then it was separate, and then they basically combined.
So at some point, they combined the concepts.
And this is BIP 118, which hasn't changed in a while.
Seems pretty static.
Well, the text has changed.
The actual format hasn't.
And it's built on Taproot.

Speaker 1: 00:26:39

And it's very comprehensively described on anyprevote.xyz.

Speaker 0: 00:26:45

I think that website's going away.
Vyatjov says he's letting the website expire, the certs or something, or the domain or something.
It was just like two days ago.
But yeah, so it's taproot only and only in tap script spends.
So basically it's kind of a mild incentive to say, hey, don't try to use this for normal transactions right because this rebinding thing is pretty powerful meaning kind of dangerous and you don't want to use it for everyday spends because this would mean like address reuse can end up in losses pretty much.

Speaker 1: 00:27:13

Although as far as I understand APO also makes you commit to a specific amount, right?
So any UTXO that has the same script or there's two amounts.

Speaker 0: 00:27:23

Sorry, there's two versions of the flag.

Speaker 1: 00:27:25

There's any prevout any amount and there's any prevout.

Speaker 0: 00:27:28

Any prevout any script, which also allows any amount.
And this doesn't commit to the script that it's signing for.
And then there's just anyprevouts.
These are two versions of it.
I ended up using, I think, anyprevout-anyscript only, because the reattaching over scripts is pretty important for my use case.

Speaker 2: 00:27:50

And it seems like AnyprevOut was marching towards next in line, but it sort of got caught up in the Covenant kerfuffle as well.
And so how does the, I mean, as a champion of the soft fork, like how are you thinking about the sequencing or not?
Or anything to do with it?

Speaker 0: 00:28:05

That's a loaded question.
As a champion, are you talking about yourself?
I'm not the champion.

Speaker 2: 00:28:09

So I'm no champion.

## Softfork and activation history

Speaker 0: 00:28:11

Currently I'm, you know, championing soft works is really hard.
Historically, I went through the history and I'm trying to think of the last soft work that was primarily championed by its author.
And it's like check lock time verify, I think with Peter Todd, I think this is the last one.
Because check sequence verify was written by Mark Friedenbach.
He left the effort, and then BTC DRAC took it over and dragged across the finish line.
We have Segwit, which is a little different.
Everyone and their mom wanted it, but you know, so Peter.

Speaker 2: 00:28:43

Not everyone.
Everyone that's still around.

Speaker 0: 00:28:47

Everyone that didn't want a schism already for other reasons.
To be, let's just be honest, right?
There's a reason, it's a different community, right?
And then just showed the truth, that It's just different communities and it needed a split I mean I'm glad that people ended up just splitting off in the end because we don't have to be married to each other, right?
If we don't want to work together.
Bitcoin's about working together.
So Segwit was like written by Peter Woola, but I don't think he really championed an activation.
I think he allowed like a BIP9 activation to get merged and then he didn't lift a finger when it was floundering because he's like you know I'm okay waiting years to get it it's pretty much his response which I think is a valid response to it and then with taproot he literally did nothing to drag across the finish line aside from make sure it's high quality high quality tests things like that and it we relied on other contributors to take up that.
So I think I've made this axiom, I guess, is I think the author should be different from the champion because it's kind of this self-invested, it's too much self-investment, I would say.
And also it's a signal, if you're championing your own proposal, correct signal, but it's a signal that the uptake's not there, the mind share.
So Jeremy Rubin with Check Template Verify, it's got good stuff, and I'll circle back to what I like about it, the effort, but it seemed to be kind of too much on Jeremy's shoulders to champion it.
You know, other people would look at it, some people would say, yeah, it's good, and then go back to their day job and not lift a finger to help, and that ultimately hurt it, right?
There's a bit of a renewal in that space with OpVault, because it's kind of a super set of behavior, so maybe we'll get to revisit that behavior.

Speaker 1: 00:30:18

I think that for a few of those soft fork proposals there were also just a bunch more authors, so it felt like there was more mind share already.

Speaker 0: 00:30:25

Yeah, of course.
I guess if you have 50 authors, but that's kind of crowding the boat.
But essentially having more than one person really active in evangelizing the tech and getting the use cases out there.
Now what I really liked about Check, Tell, Make, Verify was all the tooling being built to prove it out, right?
And so that's part of the effort here is with any prev out, I don't want to champion it right now from an activation perspective.
I think the community is pretty split right now on what to do.
But we can build the knowledge and build up the tooling.
And also, side note, basically, I'm going to eventually when I get this stuff all merged.
And there's a lot of preparatory work to get there, a lot of quality of life improvements for Core Lightning right now.
But once I get there, then I can port this over to the Liquid Network, which already has the crazy covenant, powerful covenants, and I'll essentially do an Anyprevout widget.
So use introspection to emulate Anyprevout and launch it there.
So it's simple.

Speaker 1: 00:31:21

So with Core Lightning on the Liquid Lightning Network, you'll be able to test already LN symmetry there.

Speaker 0: 00:31:30

Yeah, still have to get package relay and all that, all the stuff, but it's like a roadmap to getting something that's usable and simpler.

Speaker 2: 00:31:37

We're not going to use Litecoin as our activation playground anymore?

Speaker 1: 00:31:43

They're finally doing their own thing.

Speaker 0: 00:31:45

Yeah, they are doing their own thing, actually.

Speaker 1: 00:31:47

Mimblewimble extension block.

Speaker 2: 00:31:49

Oh, boy.

Speaker 0: 00:31:50

Yep, they're off on their own, which is great.

Speaker 2: 00:31:53

The sequence of events is package relay, underway.
Then we have APO, underway.

Speaker 0: 00:32:01

Sort of.
Tooling, specs, building on top, proving it out.

Speaker 2: 00:32:05

Okay.
And then we have LN symmetry underway.

Speaker 0: 00:32:10

Yeah.
So building LN symmetry is a, is kind of a necessary preparatory step, right?
Proving out that it actually does what we want.

## Ephemeral anchors

Speaker 0: 00:32:18

At the beginning I was I started doing research on it and I basically ran to well how are we gonna pay for fees for this because these update transactions they they can't have fees because you're contesting who has the money and there's no penalty to draw from.
There could be any number of updates, so how do you not siphon off the channel funds while you're doing these updates, while you're doing this channel response period?

Speaker 1: 00:32:40

So since any update can bind to any predecessor, the amount of money that is available has to be the same for every transaction so that you can still pay out the same amount.
So linking them all together cannot leak money.
So since there's no fees, there's no money left for fees because nothing is going anywhere else, you have to bring your own fee?

Speaker 0: 00:33:01

So, merch could say, well, why can't you just use Sighash single, right, so it's one input, one output, and then using Sighash single, you can attach on your own inputs and outputs as fees, bring your own fees.
Well, then you get back to this pinning issue, because every update could be pinned 100x or something like that.

Speaker 1: 00:33:18

With SikHash single any any muggle can come in.

Speaker 0: 00:33:21

And so the classic example also even without the spam attack, they could, your counterparty can bundle the attack, can stick yours along with a bunch of other people's attach a fee to it and say, somebody has to pony up all the funds to bump this transaction.
It's a bundling like grief attack.
And so basically that's no good.
And so I was thinking of more robust ways of doing this.
And this is where I came up with the idea of ephemeral anchors, which is, I'll dive into this now.
So in channels today and lightning network, you have this anchor output, which is some, it's like 330 Satoshis, kind of a useless amount, just to make it relayable.
And so maybe someone will clean it up in the future.

Speaker 1: 00:34:02

And do you need one or two of them?

Speaker 0: 00:34:04

Today you need two, because you can't collaboratively double spend each other safely.
There's key material and you need to be able to basically spend your own independently to fee bump when necessary.

Speaker 1: 00:34:19

So basically every single time there's a unilateral close, at least one of those anchor outputs hangs around.

Speaker 0: 00:34:25

Yeah, it hangs around.
There's a, a time lock, like 16 blocks or something.
So once it sits there for 16 blocks, then it becomes an anyone can spend type thing.
But if fees are high, it's not gonna get swept.
And or if the pre-image is not known, that sort of thing, it could happen.
But also it's the siphoning off.
So you're siphoning off this value with this anchor output.
That's a no go, right?
So I need a zero value anchor, but a zero value anchor means you have a zero value output sitting in the UTXO set Which is also no win, all right But we have package relay in this mystical new world that I'm trying to build with other people, of course But this L2 world So perhaps we can use package relay and say, OK, if you propose a package and a transaction has a dusty looking output, allow it, if and only if it gets spent in the same package.
So in this V3 context, this is more simpler to think about.
Does the parent have an output that's dust?
That's OK, as long as it's spent by the child.
There's additional rules on here.
I actually mark the output by using the opcode OP2, which is one more than OPTRUE, because everyone uses OPTRUE for testing.
So it just breaks like a million tests.
So I'll just pick the next one.
That was actually a Luke Jr. Idea in 2017.
I found old emails talking about this kind of similar idea.
So it's an OP, it's a script of OPTRUE, which means no key material needed and no witness data needed to spend it.

Speaker 1: 00:35:49

It resolves to stack to true automatically because there's only a value that is...

Speaker 0: 00:35:55

And the script interpreter says like, is this truthy?
And then it says, yeah, this is truthy and then it's successful to spend.
So it's watermarked that way.
So it says, if you have an output like that, it must be spent, and you can only have one of them.
So each parent transaction can have one of those.
It means the parent has to be zero fee for mempool policy DOS reasons.
There's a lot of complexity here.

Speaker 1: 00:36:17

Right, if the parent had more fees, it could get mined by itself, right?
That's right.
And then dust output would hang around.

Speaker 0: 00:36:25

Also, if the child is evicted for RBF and doesn't spend the parent, so like the child gets evicted and the parent's alone, we wanna make sure the parent does not mind by itself.
Yeah, that's the other one.
So there's a couple ways of doing this.
So zero fee ensures that it'll hang around by itself and the minor won't pick it up, or if certain set of patches happen, it can get evicted too, in a clean up pretty much.
Say, oh, you're zero fee, get out of here, right?
And basically, you have this one parent, one child topology, and it must be spent.
Therefore, it's like a mutex lock for spending an output on the parent.
So if someone is spending a child, someone's spending an output from the parent, you can RBF that spend no matter where it is.
And so I think this is very powerful for when it comes to, let's go back to Lightning Network today.
If we had ephemeral anchors, we'd make two keyed anchors of 330 bytes, become one zero value anchor that doesn't require any key material.
And then these outputs, let's see certain outputs in the LN penalty case would work.
Let's say the two remote output, which is, let's say Alice and Bob are in a channel.
Alice goes to chain with her version.
Alice went to chain with her commitment transaction.
Bob can immediately sweep.
If it's the correct, let's just say it's the last one, Bob can immediately take their balance, their remaining balance, non-HTLC balance.
They can just immediately spend it.
But that's not true today in the mempool because it has a time lock and things like that.
So you can't actually child pays for parent using that output.

Speaker 1: 00:37:56

Well the counterparty can, but Alice cannot.

Speaker 0: 00:37:58

No, they're all time locked with one lock CSV because of pinning.
Because you can't spend the anchor then, right?
So if they're allowed to spend in the mempool...

Speaker 1: 00:38:06

Oh, because the anchor output is the only one that can be spent.
And now we have one anchor output that can be used by anyone.

Speaker 0: 00:38:12

Yeah, so in all these outputs we can drop this one block CSV relative time lock.
They all have them because of this pinning issue, except for the anchor.
The anchors do not.
So we can drop all these concepts.
We can go back to more composable scripts, mini script compatible scripts.
These things are not mini script compatible because you're adding these random locks everywhere.
It also helps with things like splicing, where you say, I want to splice out to an arbitrary destination.
But you can't really prove to the other person necessarily that it has a one block CSV to stop pinning.
And maybe it's like a Coinbase address, right?
And they're not going to hand you one of these.
They're just gonna give you, you know, pay to witness pubkey or pay to taproot or something, right?
So from a composability's perspective, you can like take this, if we rework it, then you could have a channel with one anchor, no value draining out of it.
All the outputs are immediately spendable, well, within the, some are not because of the challenge response period, but the immediately spendable ones can be used for child pays for parent to bring fees up by itself.
And also things like splicing and you can splice into a new funding output versus, and not have to like prove that there's a time lock in there and stuff.
You don't have to tell your counterpart anything, you just send them funding funds here and it ends up being some other smart contract, right?
So I think it's really powerful from a composability perspective as well.
I could talk about one more, it's the motivations for ephemeral anchors from a use case perspective.
So one of the kind of use cases that really stuck out to me is that with ephemeral anchors, you can completely partition your custodied funds, so the funds inside a smart contract or inside a set of keys, right, versus the fee Bitcoin, right?
The Bitcoin you're paying for fees.
These are like two separate concepts Yeah, we comb and in a personal wallet.
Like if you just pull out a wallet You're generally called commingling them and it's okay because you're a person you're just one person You're not an LLC even necessarily but from a custody perspective or from accounting perspective.
It's kind of a nightmare for example I worked at BitMEX for about two years, and basically there's very strict accounting about where Satoshi's go.
Once Satoshi's off, alarms start going off, right?
It's like, hey, Where'd this go?
And you have to account for it, which makes accounting for fees really tricky.
You either make it kind of hacky or you kind of sort of lie to the system, hey, there's not that many Satoshis here, and then you secretly use them for fees because from an engineering perspective, you just want to use them in the correct engineering way, not from an accounting perspective.
An ephemeral anchor means a custody provider can do a batch payout, put an ephemeral anchor on there, and then the wallet ops team can run a different wallet which grabs that fully signed transaction and attaches their own inputs to the child pays for parent setup.
Basically, you have clear separation, clear delineation of user and engineering slash funds.

Speaker 2: 00:40:58

You lose that pop-up that's in an exchange that says, this is why you're paying fees.
Yeah.
It's like essentially the company would pick up the fees for you.

Speaker 0: 00:41:09

Yeah.
And that's the natural thing.
It's really terrible when you have to tell a user to pick fees.
So BitMEX did do that for Bitcoin.
I'm not sure if they're doing it anymore.
I can't be a user as a US citizen.
But it was pretty awful because like, yeah, you're forcing, because of this restraint, which was very, you know, it's prescient in some way, they were built in the aftermath of Mt. Gox.
But because of this, and this lack of engineering flexibility from a relay perspective, you had to have a slider and say, how many Satoshis do you want to send as a fee?
You don't even know how big the transaction is going to be.
So essentially having an engineering wallet ops slush fund for fees, I think that works much cleaner.

Speaker 2: 00:41:46

And it incentivizes them to get the fees right, as opposed to the overpaying.

Speaker 0: 00:41:52

They basically target, say, fees are sort of like this, and they set it static.
And then basically, if they make money, it goes in the pile, on the fee pool pile.
If it drains, you expense it or whatever.

Speaker 2: 00:42:03

Yeah, as I'm listening to this, it strikes me that you have this long timeline with a lot of different features, and there's a sequence to making sure that a bunch have to get in before you're able to do the next stop in the sequence.
But it also seems like each of these features in isolation is a value add.
And so package relay, this has been talked about for a very long time.
It's on its way.

Speaker 0: 00:42:28

At least 2013 or something.

Speaker 2: 00:42:30

As long as I've been in the space.
It's on its way.
Ephemeral Anchors seems quite valuable just on its own.
Is that the case for any private out as well?

Speaker 0: 00:42:40

As a consensus change, the bar is so high.
It can't just be a nice thing to have or a really nice cleanup, but everyone has to agree Because you're encumbering other people with logic.
You know, even if they run like Libitcoin or whatever, right?
BTCD, everyone has to sync up on what this is and everyone has to, you know, if we, If we find out that something's wrong with v3 or whatever, we can always change it in the future.
With consensus change, you can't really.
Once people put money in, you can't just freeze that pattern.
So the stakes are just much higher, I would just say.

Speaker 2: 00:43:15

But I guess I haven't heard of any Prevout being championed outside of L2 or outside of L1.

Speaker 0: 00:43:23

Yeah, that's another, that's a good, it's a great question.
I was just talking about this yesterday.

## Is ANYPREVOUT useful outside of LN symmetry?

Speaker 0: 00:43:27

I was like, any Prevout has, It's pretty powerful, but only has a few use cases where it really hits a home run, I would say.
Maybe that's big enough, right?
Maybe it's just the biggest home run, right?
One grand slam or something.
But it's also possible that, it depends on your theory of what a soft fork should do, right?
I think it makes things like channels simpler to reason about and build, whether you like penalties or not.
So I think for that, I think it gets a nice big green check mark, but it doesn't wax your car, doesn't make faults exactly.
You can do some kind of like CTV emulation, some parts of it, but it's not a superset or it's not a...

Speaker 1: 00:44:07

It's bigger and less powerful or something.

Speaker 0: 00:44:09

Yeah, it's the, you know, they're intersecting circles in an event diagram, so to speak.
So it can do some things that are interesting that are like by byproducts like you can get you can basically with any private any script because you're emitting your own script you can stick that you're signing for you can stick the signature in the script it's like self-referential and say this transaction must be look like this and it only come in basically you can commit to the shape of the outputs and the n-lock time and n-sequence, things like that.
So it does some quirky things like that.
But if we really like that, maybe we should have CTV, or maybe we should have op-vault.
So that's like an open discussion.
And then this is where all the contention is, right?
It's not all the contention, but of the who's next questions, this is a big one, right?
Should we be aiming really small, missing small, you know, doing the kind of key killer product releases, so to speak, and then focus on the future, maybe more systematically, or I don't know what the solution is here.
But I mean, I'm really focused on, there's like a pile of things to improve today's consensus regime, So I'm kind of focused on that for now.

Speaker 2: 00:45:19

But you're going to stay away from activation?

Speaker 0: 00:45:21

For now, yeah.
Yeah, I mean,

Speaker 2: 00:45:23

that is a seemingly a pretty big open question.

Speaker 0: 00:45:25

I mean, I don't know how much of this is Twitter psyop or whatever, but people seem pretty contentious about it.
They're like mad that people are making new releases of Bitcoin Core almost, right?
Like, just why do you need to work on it?
I think these people don't have no idea what they're talking about because they don't understand how security works or build systems work or anything like that.

Speaker 1: 00:45:44

Or that software just also ages in the context of what operating systems.

Speaker 0: 00:45:49

Yeah, that's I mean like build chips and so forth.

Speaker 1: 00:45:52

Yeah.
Software's just not.

Speaker 0: 00:45:53

Try building something that hasn't been touched in 10 years, you know.

Speaker 1: 00:45:57

Yeah, exactly.

Speaker 0: 00:45:57

Kind of a headache.
So I have to wonder how much of this is just like Twitter nonsense or is real.
I mean, in the dev community, I think it's a little less contentious in some ways.
People have their preferences, but they understand the pluses and minuses of those a little better.
So it's a little more respectful, I'd say.

Speaker 2: 00:46:15

But L2 seems to be, sorry, L and symmetry seems to be supported across the board.

Speaker 0: 00:46:22

Some people still like penalties.
Now I still think, well, maybe we should just look at getting any prev out and do dark, right?
Because I think it's like a wonderful cleanup to the current protocol.
If you had dark plus femoral anchors and stuff, I could make you a very nice set of bolts.
I have bolt specs that seems very nice and shorter.
And watchtowers are much easier, that sort of thing.
So I think there's still some choices to be made.
But maybe there's enough to start.
I need feedback from people.
When I talk to people, I say, I'm really excited about L2 or L1 symmetry or these kind of setups.
But they're all busy doing their own thing, and they're busy trying to stay away from politics.
I totally get that.

Speaker 2: 00:47:01

Darg is not something I've actually heard of, and so why is that not more, not allowed in the discussion?

Speaker 0: 00:47:06

It's an academic paper, and they didn't do much to spread it in the dev community, but it's pretty straightforward.
It's a well-written paper.
I think Shinobi pointed it out to me.
There was a predecessor called generalized payment channels, which was kind of, I'm not gonna say garbage, but impractical.
And then it was like, Dark was like a successor that was a much more practical instantiation.
And actually it seems like they understand the problem space, the engineering problem space, much better somehow, even though they're academics.
So kudos to them.

Speaker 2: 00:47:36

Cool.
Well, it was really great having you.
This was a good talk.

Speaker 0: 00:47:39

I enjoyed it.
Thanks for having me on.

Speaker 1: 00:47:40

Yeah, thanks for coming in.

Speaker 2: 00:47:51

He is very articulate about those subjects.
I like that was a good episode.

Speaker 1: 00:47:56

I think I might have led him astray a few times and we got a little bit in on different branches in the conversation.

Speaker 2: 00:48:03

That's what this is all about.

Speaker 1: 00:48:04

But now you can totally talk to all your friends about APOL and then so much fear.

Speaker 2: 00:48:10

That's right you know all the acronyms and you're gonna be a hit at the parties.
Okay hope you enjoyed the episode we'll try to get another one out soon.
Bye.
Crap, crap in here.
You
