---
title: Discrete Log Contract Specification
transcript_by: kouloumos via tstbtc v1.0.0 --needs-review
media: https://www.youtube.com/watch?v=_ZDungWdxzk
tags:
  - research
  - dlc
  - coinjoin
speakers:
  - Nadav Kohen
  - Ben Carman
date: 2021-03-23
summary: Today's WRC episode includes Nadav Kohen and Benthecarman discuss the use of Discrete Log Contracts (DLCs) and their potential benefits and challenges. They explain that DLCs can enable various applications such as betting, options contracts, insurance, and synthetic assets. They highlight the advantages of DLCs, including high liquidity and fast trading of futures, especially once implemented on the Lightning Network. However, they also acknowledge that there may still be a need for centralized solutions depending on the specific use case. The speakers delve into the technical aspects of DLCs, including the transition to Schnorr signatures and the privacy implications of using DLCs. They also discuss the role of oracles in DLCs and the potential for coin joints with DLCs. Overall, the speakers provide a detailed overview of DLCs and their potential applications in the cryptocurrency space.
aliases:
  - /wasabi/research-club/discrete-log-contract-specification/
---
## General overview of Discrete Log Contracts (DLC).

Speaker 0: 00:00:07

So, everybody, welcome to this episode of the Wasabi Wallet Research Experience.
This is our weekly research call where we talk about all the crazy things happening in the Bitcoin rabbit hole.
We can use them to improve the Bitcoin privacy for many users.
And today we got the usual reckless crew on board, but also two special guests from short bits.
We have Nadav Cohen and Ben DeCarmen.
How are you both?

Speaker 1: 00:00:36

Doing good, thanks for having us.

Speaker 2: 00:00:39

Yeah.

Speaker 0: 00:00:44

You have a really cool, So maybe we can just get going with a quick introduction of what is the very general overview of discrete log contracts that you're working on, the Jervis.

Speaker 1: 00:00:57

I mean, like the highest level explanation is just, you have a Bitcoin contract or a Bitcoin transaction that's contingent on an Oracle or set of Oracles attesting to an outcome.
So you do something basic like betting on the Super Bowl, or something more complex doing like, you know, an options contract on the Bitcoin price.
So, actually like what you're betting on and what the Oracle is signing is kind of limitless.
And it's just like what you can build on top of that.

Speaker 3: 00:01:32

Yeah, I have a question.

## Uses of DLCs. / Betting. / Options trading. / Insurance. / Synthetic assets. / Any financial contract.

Speaker 3: 00:01:33

First question.
What are, in your opinion, the most obvious uses of this technology?
For example, betting is one that you just mentioned.
What other things can be done with this technology?

Speaker 1: 00:01:53

I mean something that's coming out soon is if you saw Atomic Finance is releasing their options like trading with DLCs so that'll be a way where people can buy and sell covered calls directly on Bitcoin without needing to use an exchange, which I think will be pretty cool.
You can also use this for things like insurance or things like, just like basically any existing financial contract that you have, or like something like derivatives, or you can also use it to like hold other assets for like something we did.
So we've like basically created a synthetic dollar by just like having your payout be like you know you start with like $50 worth of Bitcoin and you end with $50 worth of Bitcoin and so you do that without dollars you could do that with Apple stock you can do that with like literally anything so and kind of the possibilities are kind of limitless.
It's just figuring out how to do all these things.
Nadov, do you have anything to add?

Speaker 4: 00:03:00

Yeah, I mean I think you hit all the really obvious ones we already know about betting, trading, hedging, and I guess synthetic assets.

## Finding counterparties. / High liquidity, high speed trading. / Cooperative transfers. / Matching engines.

Speaker 3: 00:03:14

In this case, the contract has two parties, right?
I mean it's two people involved.
In most of the financial contracts there are also two people involved but given there is a high liquidity it's transparent for you.
You don't need to find someone to make up this contract.
There is a system that can find the counterparty for you, right?
That if you want to sell, for example, what you want, sorry, what you have.
Do you think these contracts can replace that kind of, or can be used to build this kind of high liquidity and very fast kind of trading of futures or whatever?

Speaker 4: 00:04:12

Yeah, so I think to some extent the answer is yes, especially once we have DLCs on Lightning and we can do things like cooperative transfers as well.
And, you know, of course we need some kind of matching mechanism and there are lots of ways to go about approaching that problem.
But I will say, I mean, at the end of the day, I think there will be lots and lots of use cases for DLCs. But I expect there will still be some amount of more centralized solutions that people want to use in cases where they're willing to take on, or in the cases where the trade-offs that DLCs take don't make sense for them and they wanna use like a centralized third party or something like that.

## NASDAQ execution time vs self-sovereignty assurances.

Speaker 1: 00:05:08

Yeah, like we'll never rival the like NASDAQ execution time but you know, they'll never rival our, you know, self-sovereignty version of it.
So, you know, it's really like what the user wants.

## How will DLCs change when Taproot and Schnorr signatures are available? / ECDSA adapter signatures. / Thousands of signatures per DLC.

Speaker 3: 00:05:22

Okay, Max, just in case, jump whenever you want.
I can make questions all the day, right?
But now I have another question because this was implemented, this is something that exists today, I know it's available, right?
But it is not using, I think, it's not signatures, it's North signatures, right?
Just that first, if that is correct, how can this contract change when that truth is merged and available for the Bitcoin network.

Speaker 1: 00:06:09

And you can probably answer this first, I mean you're very technical.

Speaker 4: 00:06:12

All right, Yeah, so right now we're not using Schnorr on Chain.
We're using ECDSA adapter signatures.
And once we have Taproot, then we can use Schnorr on Chain and use Schnorr adapter signatures, which will be much, much nicer.
They're like nearly three times smaller, much faster to compute, much faster to verify, and since these are like the things that you're building to sign all the off-chain transactions like you're dealing with like tens of thousands, sometimes more, of these signatures per DLC, at least if you're doing like financial contract stuff or numeric contract stuff I should say.

## Adapter signatures are off-chain.

Speaker 0: 00:07:03

One question, you said that the ECDSA adapter signatures are three times larger, but aren't, like, is this the on-chain data that's three times larger compared to Capra?

Speaker 4: 00:07:13

No, no.
So adapter signatures aren't valid on-chain.
Adapter signatures are kind of an entirely off-chain construct that's very closely related to the on-chain signature scheme.
Yeah, so actually adapter signatures for ECDSA, You have your like 65 byte like actual signature.
I mean it's not DER encoded but whatever.
And then you have like a 97 byte zero knowledge proof of discrete log equality or PUDL.
And Yeah, so there's kind of extra steps because we're going through ECDSA, whereas in Schnorr you just have a nice little 64-byte adapter signature.
And then also all of the computations on those are much faster, or at least significantly faster.
So that's kind of the first nice thing.
And then the other nice thing, though I'm not sure whether or not we will or, you know, when we'll get around to utilizing this, but you can use adapter signatures in Schnorr with key aggregation, which is just crazy significantly harder in ECDSA.
So right now with ECDSA adapter signatures we are using single signer ECDSA adapter signatures so that we need like a two-of-two on-chain, but with taproot that can also just become like a single pubkey on-chain.
So long-term for DLCs in a taproot future, a DLC on-chain looks like some money moving into one pubkey and then moving out to two other pub keys and that's all there is to it on chain there's nothing else that shows up on chain.

## Are multisig scripts on-chain?. / 2-party ECDSA. / Easy to get ECDSA wrong.

Speaker 0: 00:09:10

Okay and just to confirm right now you have the multi-sig script on chain?

Speaker 4: 00:09:15

Yeah right now it looks like some funds moving into a 2 of 2 and then leaving to 2 outputs.
So it kind of looks like a lightning open close.

Speaker 0: 00:09:23

I mean you could use two-party ECDSA to compress it to a single POPkey too.
Why did you not do that for this MVP?

Speaker 4: 00:09:32

Because I want to sleep at night.
Yeah, I mean, the dirty secret is that, you know, basically anything you can do with Schnorr you can do with ECDSA.
It's just very easy to get wrong at every stage.
And it's just a much larger attack surface.
And implementation complexity and getting people to look at that code is very hard and all the other kind of challenges that go with it.
So yeah.

Speaker 0: 00:10:07

Yeah.
And Taproot makes it obsolete, so.

Speaker 4: 00:10:10

That's right.

## DLCs look like Lightning Channels on-chain.

Speaker 3: 00:10:14

Waste of time.
Okay.
One more.

Speaker 1: 00:10:17

I think I know the answer but

Speaker 3: 00:10:20

these contracts are not easy to identify or I think it's not probably possible to identify on-chain, right?
I mean if there is a transaction that basically I was betting something to Max and Max won the bet, the transaction is not, I cannot say, observing the transaction on chain, I cannot say, hey, this is a payment to Max, right?

Speaker 1: 00:10:55

No, not at all.
Like the Oracle can't tell you're using them.
Only The only people that could tell is like you and your counterparty.
It's literally just like a 202 multisig.
So people probably think it's a lightning like channel at first because that's way more common than DLCs at the moment.
But yeah, It's like very private in that way.

Speaker 3: 00:11:19

Exactly, but with taproot, you will not even be able to say this is a two parties, a multi-signature.
It's just a normal transaction, isn't it?
Or am I wrong?

Speaker 1: 00:11:32

No, that's correct.
Yeah, it was like in the like, you know, years from now when we have like full taproot support yeah, it'll look like just you know, like to like to inputs fun this this pubkey and then pubkey sends out to other outputs.
And it could be a user wallet, it could be someone consolidating ETXs, it could be whatever, it's just, it looks very non-augmented.

Speaker 5: 00:11:58

It could be a

Speaker 4: 00:11:59

payment with change.

Speaker 1: 00:12:00

Yeah, it could be a payment with change.
It could be anything.
So it'll be very hard to tell what's going on.

## Can withdrawal payment output be to a 3rd party address? / Multiparty DLC.

Speaker 0: 00:12:04

Can it actually be a payment?
Like do you think that the software will be in a way that the withdrawal transaction can be to an arbitrary address, even to a third party who was not involved in the contract in the first place?

Speaker 1: 00:12:17

I don't see why not.
Like you just specify an address for your payout so you could set it to like instead of being it to your own wallet, set it to deposit to like your friend or deposit to an exchange or whatever you want.

Speaker 4: 00:12:32

Yeah, and in the future, or so first of all, just to have it outputs go to you know more than two parties is it's quite simple.
I mean it's not implemented or specified right now but totally possible if there was a use case, that wouldn't be a hard thing to add.
And then on top of that, in the future, we'll probably have more multi-party DLC stuff available anyway.
So yeah, I think that you can intermingle kind of payments with these things as well.

## Privacy implications of DLCs. / No one but your counterparty knows what is going on.

Speaker 3: 00:13:07

Well, it's very interesting because you know that we like things that when you cannot say what is going on on chain but we like it right so I was imagining that probably if we have a huge amount of these transactions that you cannot say what is happening, who is paying whom.
It could be useful, I mean it has privacy applications probably.
Have you something in mind, have you discussed these properties before?
I'm sure you did.
Can you share with us your thoughts about this property for privacy?

Speaker 1: 00:14:05

I think it's huge for privacy, just like being able to do financial contracts where no one but your counterparty knows what's going on.
Like today, you know, you have to like go through a financial institution to be able to do really anything and you get KYC'd and all that versus this like completely permissionless and open all you need is like some stats to open up the contract.
So I think that'll I think like one of the huge things is like Today in the world we have like the US financial institution that's like has like all the network effects and money and like if you can't get access to that you kind of get boned in the Traditional finance world but with this like, you know You could be some like guy in Nigeria with just an internet connection and some Bitcoin and like have like you know all those financial products now.

## How much do I have to trust the oracle? / Sets of oracles. / Predefined refund if oracle does not sign anything. / Impossible for oracle to lie privately. / Publicly verifiable fraud proofs.

Speaker 3: 00:14:56

I have a more concrete question.
How much I have to trust on the Oracle?

Speaker 1: 00:15:05

I mean it depends.
So you can you don't have to use a single Oracle.
You can use multiple.
So like what we released last week was we did like a two of three setup where if two of three oracles agreed on a average bitcoin price then our contract could execute.
But so you don't need to trust like a single oracle completely but at the end of the day like your oracle or a set of oracles completely was going to dictate your outcome.
So like if they're all hacked or regulated or go offline, like your contract is screwed and there are ways to like, you could like, since it is just a two of two multi-sig, you can collaborate with your Counterparty to close it in a different way or we do have like a predefined refund so if the Oracle never signs anything you get your money back, but You know the Oracle can like you know if you're using a single Oracle and they sign the wrong outcome like That's just gonna be what it is and you're kind of screwed there

Speaker 4: 00:16:05

Yeah, I will note though so it is true that your contracts that you have open, that the oracles, if they lie or are corrupted or something like this, if that happens, the oracles, or sorry, the Oracle contracts that were based on that specific event get wrecked.
But the kind of Oracle model for DLCs has kind of users as entirely private entities and oracles as entirely public and oblivious entities.
So it has first of all the nice property that oracles don't know anything about their users off the bat or at least it's very tricky for them to learn anything about their users and how they're being used and if they're being used in these kinds of things.
Which is nice, you know, I always tell people that when you're dealing with oracles and trust models in general like privacy is a part of security.
It's just part of a security model.
But then on top of that because oracles are public entities in DLCs there is no real way for them to lie privately.
If you get, you know, if Oracle that you're using lies, even if they like say lie privately to your counterparty, you can recover that lie from on-chain information using the off-chain information that you have from the transaction that your counterparty uses.
So at the end of the day you can still construct publicly verifiable fraud proofs that the oracle attested to something that was false or equivocated or something like this.
And so in the future I think that there will be lots of ways for oracles to essentially you know put their money where their mouth is and stake funds that can be taken away from them if they lie.
Because at the end of the day, and even if that's not the case, you know, just from like a more reputation perspective, like it's impossible for them to lie in private, essentially, is a nice property of DLCs.

Speaker 0: 00:18:22

Yeah, really cool.

## Funding transactions into DLCs can break common input ownership heuristic. / Chaumian DLC.

Speaker 0: 00:18:22

I have one more question on the more on-chain layer.
So the funding transactions into that, this block script, has two inputs from, or an input from each user.
So both of those provide at least one in the same transaction.
And the nice thing is this also breaks the common input ownership heuristic.
And it's the same as dual funded Lightning or Payjoin.
So this is actually a nice benefit for launching privacy in general.

Speaker 1: 00:18:55

Yeah, I think this is really huge, where you kind of get like a mini coin join there, and something that I wrote a while back, but a thing where you could do like, I call it a chowmian DLC where you could batch a whole bunch of DLCs together and then like you have like a basically a whole bunch of inputs going into like a bunch of different DLCs all in one giant transaction.
And now you really break the common input heuristic there.

Speaker 0: 00:19:23

Yeah, exactly right.

## Coinjoins with DLCs.

Speaker 0: 00:19:24

That's the logically following next question.
I'm curious, maybe Yuval or Nadav have interesting points on the nuances of coin joins with DLCs.

Speaker 1: 00:19:37

I mean, I think, I think like it's theoretically possible to be able to like have a like similar to like Wasabi's model where you have like a coordinator but instead of this coordinator just giving and passing around details about the coin transaction you guys would also pass around stuff about your DLC and the nice thing too with this is the coordinator could actually close the contract for you if they are connected to the Oracle.
So there's some like actual UX improvements there too where you know you don't need to be online and actually close your own DLC.
Yeah, the gist of it is just like, you know, you set up or like you say, I have like 50 participants all doing a contract and then they take one side of the bet and the other, say like half take one side of the bet, half take the other, and then they all register inputs and basically just create a giant DLC and then all the payouts go out at the end.

Speaker 3: 00:20:46

I don't know.

## Non-DLC users on the same Coinjoin. / Mixed pools. / Channel factories.

Speaker 0: 00:20:47

Yeah, One note here is that if all of the users of this coin join use DLC, then it's kind of like a bad fingerprint in terms that you know that for 100% sure this is a DLC contract.
Well,

Speaker 3: 00:21:01

if there

Speaker 0: 00:21:01

are other non-DLC users in the same coin join, then because of taproot, they look the same.
This would be huge, because then you don't know which user is part of the DLC, which has to pay join, like amount consolidation.
And that would improve amount analysis massively for everyone I

Speaker 3: 00:21:24

think.

Speaker 4: 00:21:24

Yeah I think that that's totally doable and we've thought about kind of this where you can just mix pools where you have people who are doing DLCs with people who are doing coin joins with people who are opening lightning channels or in the more distant future channel factories and all these kinds of things at the end of the day You can always just like save a little bit on fees by throwing everyone's inputs and outputs on the same transaction.
Of course with DLCs in particular, there are ways around this where you can kind of have like a multi-stage setup, kind of closer to how they've been working on putting multiple Lightning funding transactions, multiple Lightning channel opens in the same transaction.
You could do something like that with DLCs and Coin joins and all just kind of in one transaction.
But if you wanted to actually mix kind of normal coin join users with DLC users then there is kind of the, I suppose maybe not for everyone this is a downside, but the downside of like there's a long time between Going on chain and paying out Because you have to wait for like the Oracle event to happen or something like this but you know if someone's mixing coins they don't need to be sending anywhere anytime soon then maybe this isn't a big deal.

## Increase anonymity set.

Speaker 0: 00:22:55

It's actually a cool privacy benefit of having time-staggered remixes.
It increases your analogue too.

Speaker 1: 00:23:04

Yeah I think that could be really big too, because the only downside there is that, at least in today's coin joins, you would have to use the same output amount.
So if you're doing like Wasabi, it's like the .1 Bitcoin.
But with the stuff you guys are working on with Wabi Sabi, you kind of get rid of it.

Speaker 0: 00:23:26

Wabi Sabi fixes this.

Speaker 1: 00:23:27

Yeah, Wabi Sabi fixes this.
And then you could do an entire thing where you know you could have any contract really going in on there and Really privately with everyone else's transaction.
That'd be awesome.

Speaker 4: 00:23:40

Yeah, and another thing.
I just realized that I forgot to mention that is like a benefit of doing things this kind of way, at least for DLC users, is if you have, you can essentially use netting while you're doing this.
So if I have a position open with two different people who are also participating here and there's like some overlap happening, then really all that needs to happen in the more coin join looking transaction is kind of the aggregation so I can like recover some collateral or things like this.

## Wabisabi and consolidation of payouts.

Speaker 0: 00:24:19

Yeah, especially with WabiSabi that allows for multiple outputs being registered at different values.
Like consolidation of multiple refunds or payouts can be done too.
Maybe.
I mean, therein the nuances of course, like how much information does the coordinator learn?
That's something for you all to figure out, I guess.

Speaker 6: 00:24:44

As far as I can tell, there shouldn't be any requirement for the coordinator to be involved at all.
There might be added value, like if the coordinator is also helping to mediate this kind of net settlement, like making the actual outputs allocations more efficient, that might be a good reason to involve the coordinator.
But I'm a little bit rusty about DLCs, but if I understand correctly, the way that you would do such a thing is two users would just register their funding amounts to a Wabi Sabi CoinJoin.
They would negotiate the off-chain contract.
And then at the signing phase, Once the transaction ID is already locked in, assuming only SegWit inputs are allowed into the transaction, at that point the refund transactions and stuff like that, exactly like a Lightning channel, can be pre-signed before both parties to the CoinJoin provide their CoinJoin signatures.
So at least in theory, it should already be possible.

Speaker 0: 00:26:00

You spoke about the deposit into the DLC, but what about the payout and the withdrawal of the DLC?

Speaker 6: 00:26:07

If I understand correctly, once the two of two output is already locked in and funded, the oracle will publish its attestation, I guess, for lack of a better term.
Sorry about that.
And then one of the parties to the transaction will be able to unilaterally spend that.
At that point, especially if it's a taproot output, of course, they could negotiate to just do like a payout transaction that spends that much like coin swap settlements work.
And equally, they could bilaterally agree to register this output as an input to a subsequent coin join if complex scripts are implemented.
Like if you're able to do arbitrary input types and not just SegWit, PayToWitness, PubKey, Hash inputs to coin join transactions, then at that point, like, there's no difference, right?
Like, the ownership proof is equivalent to the collaborative spend path.
And Yeah, it's just a matter of the two parties like agreeing who actually uses the credentials to register outputs.
But that's like, there's no theft risk there.

## UX improvement if coordinator automatically uses oracle signature. / n-of-n outputs. / Obfuscation: wave functions, cancelling noise.

Speaker 0: 00:27:46

But to build on top of that because Nadav said that there is this UX improvement that the coordinator can automatically take the Oracle signature and do initiate the withdrawal transaction but I'm not sure how this would work with Coinjoins in a non-custodial way because you cannot pre-sign the CoinJoin transaction because you don't know the CoinJoin transaction.
So how would that work?

Speaker 1: 00:28:10

They couldn't close it in a CoinJoin transaction for you, but if they had your outcome signatures and they got the Oracle signature, they could close it in the easy case where it's just like a single transaction that just has the output to the winner.
But if you wanted to do like the coin join close, you'd have to do that cooperatively with your counterparty.

Speaker 4: 00:28:35

So I think another thing to mention, I kind of mentioned that there are two different ways of doing this.
One of them is closer to like the multiple lightning channel openings, which I think is what we're currently discussing, where you have a bunch of inputs and then a bunch of two of two outputs.
But another way of doing this that I think Ben has proposed, which has its own trade-offs, is having a bunch of inputs and then a single n of n output, and then a single transaction spending that n of n output in the end, which closes all of the DLCs. And this would be the situation where it would make a lot of sense to have a coordinator be able to just broadcast that mass closing.

Speaker 1: 00:29:25

Something you could also do is, well, maybe not, but you could just have your counterparty's signature be, have the SIGCHASH flag for SIGCHASH single, so it's only committing to the payout output, and then you could put that output in the coin join transaction.
The only problem is though, then if you're using that SIGCHAS flag, you're kind of revealing which output is yours.
So maybe that wouldn't be the best, but you're still kind of, you know, at least you're saving on fees that way by sharing all the metadata in the transaction.

Speaker 4: 00:30:00

Yeah, and it is important to note that for this end-of-end scheme to work, you do gain some information about the other people in the mix because you know what their outputs would be on Oracle Outcomes.
But there are a couple ways to mitigate this.
I don't think this has been well thought out or modeled yet.
But you can, for example, have rather than one output per participant, you can have multiple outputs where essentially if you picture, like, say, the oracle outcome on each party has a payout curve, you can decompose that payout curve into some wave functions or something like that, where each output looks nonsensical, essentially.
And you don't know which aggregation of outputs corresponds to like which entity or things like this.
Or there are a couple other ways of kind of trying to do obfuscation where you can have like canceling noise on multiple outputs.
But again, this hasn't been thought out too well yet.

Speaker 1: 00:31:08

Also, I think another possible way you could do it is, and once you have the taproot thing, we just have like a single key behind the funding output, you could, in the cases where a single party gets all the winnings, you could instead of signing a transaction, upon getting the Oracle signature, you could have them just get the other user's private key, and then you could use that to then, so then they could, then they just own the input completely unilaterally, and they could use that to register for a coin join, and just like spend it from there, however they see fit.

## Coordination complexity of signing rounds.

Speaker 0: 00:31:54

And one of the other constraints that I see is the coordination complexity and how much that increases when two users need to collaboratively look at the CoinJoin and only after they have come to an agreement, sign the CoinJoin.
So what do you think?
Will this lead to more failed signing rounds just because the users don't communicate properly?

Speaker 4: 00:32:21

So I think, with DLCs, you have, you're signing so many things.
I, I don't think that, adding this, this coin joining stuff really has a significant increase in how many things you are signing and validating and such.
It could change like the size of the thing you have to validate before you sign, say, or the thing you have to hash before you sign, rather.
But at the end of the day, even, for example, for the end of end scheme, where they're like, for every possible, or for every relevant possible oracle outcome you have a separate closing transaction for all end parties.
If you were doing just a two-party DLC in the usual way You would still have to sign that many things, or at least on the same order of magnitude.
And so you know, I think at least in kind of a coordinated model it's not a big difference, where you have some kind of one party that is communicating with many other parties.
If it's more of a gossip-based mixing protocol, then this might be significantly harder.

Speaker 0: 00:33:46

Maybe a more concrete question.

## Speed of signing rounds.

Speaker 0: 00:33:47

So if Nadav and I want to fund this DLC contract, we register our inputs in the coin join that we want to use in the deposit.
In the next round we register our output address, which is one cooperative, like one of our cooperative DLC contracts, and two changes for each of us.
Then finally, this gets put together by the coordinator, and we go into signing phase.
And now, Botlanoff and I have the CoinJoin transaction, which we will use to do the pre-signed refund transactions and all the DLC stuff that needs to be done.
And then after all these refunds are signed, then we put our final signature on the current join, like both of us on our own individual UTXOs, and register them in signature registration.
Is that roughly correct?

Speaker 4: 00:34:46

Yeah, that sounded right to me.

Speaker 1: 00:34:49

Yeah, I think you could, because like with that multi-oracle DLC that Mean Adopted last week, like it took us like five minutes to sign everything.
We still have some optimizations to do to make that faster.

Speaker 4: 00:35:02

And by some he means all.
It will be much faster by the time we're done with it.

Speaker 1: 00:35:07

But it's still like, you know, it's not as fast as like because I think like in wasabi You have like what 20 seconds or something to sign?

Speaker 0: 00:35:15

So I think it's a three minutes timeout for the signature

Speaker 1: 00:35:20

Okay, so maybe but yeah something you could do like if it was like, you know, if you were pushing on that threshold, because you do need this, both parties do need to sign and verify each other's stuff.
So something you could do is just give each other the refund transaction signatures and then once the fine transaction is confirmed or after it's been at least broadcast, then you can start doing your outcome signatures.
So at least that way you're guaranteed to get your money back if something goes wrong.

Speaker 4: 00:35:52

I think that has a bunch of free option problems probably.
But yeah.
But I do think that if it's a three minute timeout in the future, this isn't going to be a problem.
Like we have lots of- I'm actually not sure

Speaker 0: 00:36:08

what it will be in the future.
I think right now it's three minutes.
Jubal, what are your thoughts on signing period timeout?

Speaker 6: 00:36:16

So generally I would say it's probably going to be variable.
Like we've been thinking about scenarios like PSBT support or hardware wallet support.
And if it's PSBT support for like a manual thing, you know, maybe some rounds would even have a signing phase that's on the order of hours for, you know, high value coin joins or something like that.
I think that's something that even if the Wasabi coordinator doesn't deviate from the current timeout values and there is demand, I'm sure that some coordinator would come up and offer those round parameters.

Speaker 4: 00:37:07

Cool, yeah.
So I mean, DLCs require, I assume, at least usually, less time than using a hardware wallet.
So that's good to hear.

## Coordinator rounds determined by the user.

Speaker 6: 00:37:22

For what it's worth, like one idea we were kind of spitballing is having the, like making all the coordinator rounds basically determinable by the users.
So if there's no round available right now with parameters to your liking, for example, the fee rate might be too low or too high, or you want to coin join with a larger minimum input amount or something like that, we still need to think this through.
But it seems reasonable to just support a specific user asking.
I mean, it's probably not going to be exposed in the front end directly just because it's a kind of a low-level feature.
But there's no technical reason, and I think no game theoretical reason why the coordinator should not support the ability to just ask for a new round to be created.
So I'm optimistic about these kinds of possibilities opening up.

Speaker 0: 00:38:59

Okay, cool.

## Benefits of amount consolidation. / Pay-to-endpoint over Wabisabi. / What information does coordinator need? / What information do the users need?

Speaker 0: 00:39:00

Maybe I think one topic just to rehash and to dive deeper is the benefits of the amount consolidation of two users.
Maybe Yuval, if you have some further thoughts on this page join similar type of amount consolidation.

Speaker 6: 00:39:21

So that was kind of implied by the scenario I was describing earlier, just to get everybody on the same page.
The idea behind, So I'm hesitant to call that pay join just because pay join kind of implies more.
It implies the steganographic features as well.
So I think like a pay to endpoint over Wabi-Tabi or a credential payment or something like that is perhaps a better term.
But the idea is like let's say Alice wants to pay Bob some amount, she registers inputs greater than that amount and produces in her registration, she requests a credential worth the payment amount and then she just gives that to Bob.
Alternatively, she could ask Bob for a credential request and then she has no opportunity to use it herself, but in either case there's no theft concern.
Bob can then go and use this to register his output for the received amount, or he can consolidate it with his own inputs to get better privacy.
And this is nice because it protects Alice's inputs from Bob's prying eyes and vice versa.
And

Speaker 0: 00:40:47

yeah,

Speaker 6: 00:40:51

that's kind of how you would have to do it anyway for like a simple case.
What I would be kind of like more interested in hearing Ben and Nadav's thoughts, like in the scenario where the coordinator is kind of mediating the bets themselves, especially in a net settlement setting, what kind of information would the coordinator need to know, and what kind of information, like, do the individual users need to exchange in order to to get next element going because I think that's Kind of the logical continuation of this this type of pay to endpoint approach

Speaker 2: 00:41:49

Real quick before the dive and Ben answer that, in a naive case,

Speaker 0: 00:42:01

we're losing you.

Speaker 2: 00:42:02

Isn't there still some change output from each other?
You're still obscuring things for a third party observer where that payment looks like a single user's change output?

Speaker 6: 00:42:14

So You were breaking up, but if I think, if I understand correctly, yes, I mean, you're not disclosing that there even was a payment, and further, you'd be breaking the sort of heuristical assumption that you can partition the transaction into like one set of inputs and outputs per user that's going to balance to zero.
So that this is like further helps to break down the common owner input heuristic.
But like, I'm not sure what you meant in the chat by pass on an output credential for unmixed change.

Speaker 3: 00:43:06

The credential-

Speaker 2: 00:43:07

I'm saying like, if I put my input in there and get my mixed outputs and then give you an unmixed change output, like that will look like I'm just getting my unmixed change back, but I paid you.
And even though we still see that graph between the two of us, like nobody else can interpret that graph correctly.

Speaker 6: 00:43:29

Yes.
And that is a much simpler scenario because there's no interactivity, there's no pay to endpoint.
All you need to do is give me an address and I register some output with your address.
Like in the pay to endpoint scenario, you do have much better counterparty privacy, because the only thing I learn is what credential am I giving you?
I don't learn how you're actually using it.
And Of course you can in theory combine it with your unrelated input credentials which I don't know about.
And then the payment amount is also hidden and never appears in the transaction.
So many privacy benefits.
To

Speaker 1: 00:44:21

go back to nothing much as an original question, I think to have the coordinator like be doing like acting as like a watchtower, I think all you'd have to give them is like the Oracle that they'll be fetching from to get the signature and then like your actual outcome signatures.
So doing so you kind of reveal what your contract is to the actual coordinator, but you also then get this kind of watchtower thing where they can close it for you and you don't need to be online and make sure you do it, which is huge UX improvement.

Speaker 4: 00:45:00

Ben, are you talking about the two of two situation where there are a bunch of two of two outputs?

Speaker 1: 00:45:05

Yeah, yeah, I guess if you have like, you know, like a-

Speaker 4: 00:45:07

Gotcha, or yeah, I was just gonna mention in that case, really what you can use generally speaking is a watchtower.
And you know, If coordinators are some kind of watchtower in the future, they can also be used for that purpose.
But you can also just use normal DLC enabled watchtowers in the future.
But yeah, go ahead and talk about the end of end case if you want.

Speaker 1: 00:45:29

Yeah.
So if you had like a 50 of 50 like kind of thing, I think you still reveal your, your contract in that way, maybe less.
So

Speaker 4: 00:45:42

no, I think you would have to reveal quite a bit, actually, in this case, which is why you need kind of other obfuscation methods.
If I'm not mistaken, all of the contract execution transactions are now like aggregate amongst all 50 peers and they all have to sign the closing transactions for everyone.
And so they see kind of what the output values are.
And so you need to do some obfuscation on them, I think.
Ben, is that right?

Speaker 1: 00:46:10

Yeah, I guess you do get the benefit though, like where the coordinator won't know like which address is going to like which user.
So you do like, they'll know like, you know, this person or this address gets paid out if this, you know, the price of Bitcoin is 10K or whatever, but they don't know directly like which user registered the payout address.
So you get the benefit of, you know, hiding that, but they still can see like what the payout curve is for each address.

Speaker 0: 00:46:39

Yes but you might actually be able to do some amount decomposition of these payout transactions.

Speaker 4: 00:46:44

That's right.

Speaker 0: 00:46:45

Right so you have one input worth one Bitcoin and to break that down into 0.4 and 0.6, for example, naively said, but of course there's more signing.

Speaker 4: 00:46:54

What you do, I don't think that it will require necessarily more signing, But I think what happens is that rather than everyone passing around their contract info, the thing that's used, essentially their payout curve for Oracle, as what the Oracle says is the x-axis and their payout as the y They take their payout curve instead and they break it up into pieces with canceling out noise And register multiple outputs and then passed around these nonsensical noise full payout curves as if they're coming from different people.
And so everyone should have pretty nonsensical, if this works out anyway.
Again, I haven't looked into it deep enough, but everyone should be able to pass around somewhat nonsensical payout curves where each person is actually getting the aggregate of multiple payout curves, but no one else knows what that looks like.
Then hopefully that mitigates things a little bit.
And furthermore, once you have everyone's payout curves, you can construct for yourself deterministically all of the closing transactions that you need to sign and validate signatures of.

Speaker 1: 00:48:18

Okay, yeah, that makes sense.
So like, if you have like, say like 50 users, you'd end up with like 100 or like 200 actual payout outputs but you know there's still 50 users so Some of them are getting multiple.

## Amount decomposition? / Payout curves.

Speaker 0: 00:48:32

Yeah, but by the way, we've done a lot, especially Yuval did a lot of research on this amount decomposition.
And currently, like we assume that every user knows the inputs of the users of this current round of CoinJoin.
And it seems that's the same case here, right?
Every user knows at least the inputs of this amount.
And then you can already make some privacy, optimize the model organization for the outputs and the payout curves.
It's like, But that benefits from having standard amounts.
So if you would have multiple standard amounts, when users choose some of them, and they choose depending on what other inputs were registered.

Speaker 4: 00:49:15

Yeah, and I guess in theory, you could even have, I guess maybe it's easier if everyone always has the same number of outputs, but you could even play with that as like a parameter to mess around with is you could have more outputs on like some Oracle outcomes as opposed to others if say you're receiving more or something like this.

Speaker 0: 00:49:40

I actually would guess, I'm not sure but I have an intuition that it's better for privacy if it's not sure how many exact outputs you have.
Like if there's an arbit, like an ambiguous room between one output or zero outputs, and I don't know, 21 outputs, whatever the maximum value is, that seems to be more private because you then don't know how many siblings each other kind.

Speaker 4: 00:50:03

Yeah, so you could have, I guess, payout curves that look noisy and are zero in lots of places and everyone just filters out dust outputs every time or something like this.
Or maybe there's a more sophisticated way of doing that so that you don't actually see that.

Speaker 6: 00:50:21

I think it's actually orthogonal.
Like if you look at the amounts themselves from purely the CoinJoin perspective and you're able to create enough ambiguity between the input amounts and the output amounts, I think it's immaterial what the script semantics of those outputs are.
And whether or not the funds are broken down after they're divided between two counter parties to some bet, that doesn't really matter.
All you learn is that this was split between two people but the bet itself should be like the total amount should not be really like linkable to the the inputs of both users.
Like in this scenario, you can imagine the two counterparties are kind of acting like one user.
The combined, like if you partition the transaction and look at only the subset of inputs and outputs for those two users who are transacting.
If they construct the bet amount, like the bet output amounts, in such a way that there's no way to infer that subset based on all of the like the rest of the transaction it's sufficiently ambiguous and at that point like it's not clear Which inputs are going into the bed at all and and therefore it should not be linkable to the specific user I'm not up.

## Net settlement.

Speaker 6: 00:52:19

Could you talk a bit more about the net settlement stuff that you were alluding to before?

Speaker 4: 00:52:27

Sure.
Yeah.
So, say, like, I am entering into, say, two DLCs, and I'm a little bit over-collateralized because, say there's like some cancelling out, so to speak, in my position, like I'm a bit long here, I'm a bit short here, or something like this, then if in a situation where you have kind of both of those DLCs going in in one place, I can essentially have my two counterparties essentially take on that bet somewhat synthetically against each other and like recover some of my own collateral.
If that makes sense.

Speaker 6: 00:53:17

Do those counterparties need to coordinate or are they only coordinating through you?

Speaker 4: 00:53:28

I guess it kind of depends on what the coordinated setup looks like for the actual mixing stuff.

Speaker 6: 00:53:38

Sorry I shouldn't have used that word.
Like suppose in the non-coinjoin scenario you're doing this kind of thing.
Do the two counterparties that you have, do they need to communicate between them and exchange like adapter signatures between them?
Or can they rely on you to transfer the information between them?

Speaker 4: 00:54:08

I see.
So yeah, if you want to do netting stuff, you actually do need kind of something like a coin join looking thing, because essentially you need like all three parties inputs and outputs and such to be in a single transaction in order to get back your collateral so to speak.
So some amount of coordination does need to happen.
I assume that there are different ways of doing this.
Maybe Ben is more well-versed.

Speaker 1: 00:54:43

I think it'd be up to like the person that's actually benefiting from the netting to be able to figure out how to do it correctly because You know they're it's a sort of over collateralizing that they can take it out.
They'd have to negotiate that with their peers to like change the actual contract to be like to benefit them to get the less collateralized.
At least that's my understanding.
I don't know.
I think then Ichiro write the initial paper on it?
He's probably the best one to ask, but he's obviously not here.

Speaker 4: 00:55:26

Yeah, I think it's pretty much similar to what you have in mind though, Ben.
Yeah, but I guess short answer is, it's likely easiest if they are coordinating with one another, but there's likely other ways of making things more obfuscated or something.

## Q&A.

Speaker 3: 00:56:02

Okay guys, just in case, we are making questions and comments just to keep the wheel rolling, right?
But anyone can make questions.
In fact, it's good if we call this section Q&A now, right?
Because I think most of the topics are already covered.
In fact, the advanced topics are already covered.
So feel free to raise the hand.
To raise the hand.

## Can you get screwed if you lose stateful data.

Speaker 2: 00:56:38

Well, I kind of missed the first 19 minutes or so, but kind of just the general topic of blurring DLCs and nesting them into a coin join.
I mean, it seems like there's a lot of wins that you can have here, but it does kind of worry me that that implicitly transitions the model of a coin join for those users to, you can get screwed or things can go wrong if you lose stateful data, as opposed to it's literally impossible for something to go wrong here.

Speaker 4: 00:57:16

So I think an important thing to note is there are kind of two different ways of doing this.
One of which is essentially just having a coin join where some of the outputs are like these two of twos that are DLC funding outputs themselves.
And you know those two of twos once we have taproot become just single pub keys anyway.
And if you are doing things this way, then I don't believe that parties who aren't doing DLCs become affected by parties that are doing DLCs inside of the same mix?

Speaker 2: 00:57:52

Well, I mean, they shouldn't in either case, unless I'm missing something.
But it's just kind of like that's an implicit risk, I think, that should be like that that is deserving of like a big morning screen that like things can go wrong.
If you lose these transactions, you know what I mean?
Well, like, I'm still just have like things can go wrong if you lose these transactions, you know what I mean?
Well, I'm still just have like, things can go wrong if you lose these transactions.

Speaker 4: 00:58:52

Oh boy, what's happening?

Speaker 1: 00:58:57

I hope someone got

Speaker 4: 00:58:58

an MST out of that.

Speaker 2: 00:59:00

That just destroyed my brain.

Speaker 4: 00:59:02

Yeah.

## Embedded assumptions in having Coinjoin + DLC. / DLC API.

Speaker 4: 00:59:04

I guess, Shinobu, can you elaborate on how this is different from just entering into a normal DLC in terms of state?

Speaker 2: 00:59:12

Well, I just mean, it's like, Kind of putting these two options together implicitly assumes that One piece of software is gonna be capable of both and I just feel like you know Burying a million options like that like something should be explicit about that.
You know, I mean Like there's no difference between a Nami and a DLC.

Speaker 3: 00:59:46

Max, can you fix this?
Do you think?

Speaker 0: 01:00:00

Yes, I just said the password.
Yeah.

Speaker 3: 01:00:16

You

Speaker 5: 01:00:16

should also be able

Speaker 3: 01:00:18

to kick out.
Yep, just did.

Speaker 0: 01:00:32

It is where we have the password.

Speaker 1: 01:00:35

Yeah.
To get back on top

Speaker 5: 01:00:37

of it.
I love

Speaker 2: 01:00:37

the adults in this space who want to have adult conversations about things.
There's so many of them.

Speaker 1: 01:00:47

Well, to get back to it, there's not too much difference.

Speaker 4: 01:00:52

Intermingling maybe, Ben, because right at the end of the day, you could have your mixing black box and your DLC black box, and one message needs to be passed from one to the other.
I don't look specifically the one that has the funding TX ID in it.
I don't think that there's much else.

Speaker 1: 01:01:14

Yeah, yeah, like All you need is for the DLC software is like a funding TXID for everything and then that should be able to handle everything else.
So it wouldn't be a huge complexity issue or anything like that.

Speaker 2: 01:01:26

Okay, so you guys are just talking like API hooking two pieces of software together, not like rolling all of this into like the Wasabi UI or anything.

Speaker 4: 01:01:35

That's right.
Although

Speaker 2: 01:01:38

that's at least...
Yeah, that was a bad question on my part then.

Speaker 4: 01:01:41

Got you.
No worries.
But for the N of N mix, then that's kind of its own custom thing but that kind of assumes that everyone involved is doing specific DLC stuff.
Yeah, where you're registering two of two outputs, hopefully you can and in the future, you know, just single pubkey outputs.
Then essentially what you'll do is you'll have like a callback where when you get the thing you need to sign before you sign the actual like funding or the mixing transaction, you like go make a call out to the DLC API, do all that stuff and then come back and do this last.

Speaker 2: 01:02:19

Okay.
All right, that makes sense then.
I guess ignore Shinobi's bike shedding troll concerns.

Speaker 0: 01:02:46

Maybe a question on some different regard that we did not talk about.

## Optimisations for arbitrary amount settlements. / Contract Execution Transactions. / Rounding. / O(lg n) signatures for n outcomes. / Verifiable encryption.

Speaker 0: 01:02:49

How about optimizations that you used for these arbitrary amount price settlements?
Can you maybe speak a bit more?

Speaker 1: 01:02:59

Sure.

Speaker 4: 01:03:01

Yeah, so generally speaking, you know, if you're thinking about DLCs as like a black box, you think about like there's some set of outcomes, you create a transaction for each of those outcomes that pays out however it's supposed to for that outcome.
And then you generate adapter signatures.
But this works great for most betting.
But if you're, say, Doing something where the outcome is a number or you know, there's just a ton of outcomes and they're structured Then you have Kind of this problem a couple different problems, but mainly the problem is that you have like let's say a hundred thousand possible outcomes or something like this when maybe especially usually it's the case that you only really care about some small subset of those.
And if it's anything above a certain number or below a certain number, then you just have some edge case like, OK, this person gets all the money or something like this.
So what we do is we have the oracles, numeric oracles specifically, sign each binary digit, each bit of the outcome individually.
And then we can essentially construct outcomes using digit prefixes instead of the entire list of digits.
So instead of requiring that there's a separate outcome, so to speak, or it's a different outcome for every different number.
You can have, for example, if you ignore the last digit and you just look at all of the digit prefix up to the last digit, then you can have an outcome that corresponds to two possible numbers.
And then if you ignore two digits, that's four possible numbers and so on.
And so you can essentially, for example, say if everything above 100K is just like the same outcome, basically, then what you can do is you can decompose that very, very large interval into only logarithmically many CETs essentially, or contract execution transactions.
And so, and then furthermore, we introduced some amount of rounding.
So this is like negotiated, both parties are okay with the amount of rounding that happens And you essentially say round to the nearest hundred Satoshis or the nearest thousand Satoshis or something like this.
And then by doing that you can get more kind of flat pieces which can be compressed by the same mechanism until logarithmically many, you know, adapter signatures that you need.
And so in practice what this means is that even relatively complicated, you know, financial contracts on numeric outcomes on prices end up with only, say, a couple thousand adapter signatures or cases that you've decomposed it into, rather than having to cover all 100, 200,000.
And then furthermore, for multi-oracle stuff, there's also some fanciness that we do, where essentially you do something similar, where agreement between two oracles is essentially constitutes like you take one of these digit prefixes from one oracle, and then you construct a digit prefix for the second oracle that covers that same, or what the first oracle said, with, say, some allowed amount of error.
So we even cover cases where you have multiple oracles and they don't sign exactly the same thing.
They can be like some amount off.
Say if you're for example using like Kraken and Bitfinex and Gemini or something like that as three price oracles, then you can have it so that so long as any two of them are within $128 of the same BTC USD price or something like this then your contract will execute.
So yeah all sorts of fanciness and stuff happening there And there's some more optimizations that I'm working on that maybe use some like verifiable encryption and stuff like that to try and get the scaling for adding new oracles down to something more reasonable.
Yeah, I'd be happy to talk more about it of course, but at this point I'm probably just rambling unless someone has questions.

## Can optimisations for DLCs be used to optimise coinjoins?

Speaker 0: 01:08:41

I'm just curious.
Do you think that this is, in any, at all interesting research useful for conjoins?

Speaker 4: 01:08:48

Can you say that one more time?

Speaker 0: 01:08:51

Do you think that there is some nice similar ideas that we can use to optimize for conjoins?
In the non-DLC case, I mean.
Or is it just complete different research?

Speaker 4: 01:09:03

I would think if there is any overlap, it would be in kind of the coordination of the outputs and such.
Because we have some pretty succinct coordination between the two parties on, you know, essentially like the contingent like, you know, if the Oracle says any of these things then here are my outputs in all of those cases.
So we have like these nice compressed, essentially like seeds from which you, or

Speaker 3: 01:09:37

you

Speaker 4: 01:09:37

know, contracts from which you derive all of the transaction information.
But I guess for a regular coin join you just have one transaction so maybe that's not a big problem.

Speaker 1: 01:09:48

Yeah I think where the most overlap is is honestly like on the off-chain side where you're finding counterparties like like we've like looked into like different ways we could you know have a place to find like a counterparty for the bets you want to make.
And like you could do like, you know, you just have like a central place, like somewhere like a Wasabi coordinator, or you could have something where it's like, join market where it's like, you know, a kind of decentralized kind of thing where you're finding there's no like coordinator to find you counterparties.
So it's, it's a different way to do it.
And we haven't really, there's probably gonna be multiple different ways to do it similar to how the CoinJoin landscape is today.
So I think that'll be probably the place where there's the most overlap.

Speaker 0: 01:10:36

Yeah, I think the amount of organization might be interesting for you guys.
Like, based on the inputs of other users, how can we optimize the outputs of us?
So to gain more privacy, I think this is like non coin join cryptography related things that might be interesting for you.

Speaker 4: 01:11:00

Yeah and I guess also you know if we are doing some kind of DLC mixing stuff in the future, then also the amount decomposition things might be some overlap there.

## Consensus on fee priority. / Child-pays-for-parent for DLCs. / Replace-by-fee not possible for large coinjoins or DLCs. / Free credentials.

Speaker 0: 01:11:25

One maybe relating question, how do you get consensus on fee priority for this transaction?

Speaker 4: 01:11:35

So currently this is done via, essentially, you know, you can choose whether or not to accept a certain fee rate, But afterwards everything is fee bumpable using child pays for parent where the child is replaced by fee enabled.
So it's yeah.
I guess there's always the, you know, lots of complex ways to handle these kinds of things.
I think right now the dual-funded Lightning Channel proposal just has like the initiator pay all the fees because it's simpler.
But we decided to kind of split the fees between the two parties and then for the fee rate that's in like say the offer message.
And then everything beyond that is done just by fee bumping.
Yeah.

Speaker 0: 01:12:36

Yeah, two notes here.
I mean, for somewhat obvious reasons, RBF is not possible in large coin joins or not reasonable to do because you have to resign, everyone has to resign.

Speaker 4: 01:12:45

That's right.
And for DLCs, it's not possible either.
It's only the child.
And the child pays for parents.
So like, if you spend your change, then the thing you're using to spend your change is what you would RBF with.

Speaker 0: 01:12:58

Yeah, yeah, that's smart.
But the issue here still is with the size of the coin joint.
You have to child pay for parent, the entire fee for the coin joint.

Speaker 2: 01:13:09

Well, Max, you could do that out of the change input or output that Wasabi is getting fees in.
Once you implement fee credentials, that could potentially be a thing where users pay for that, air quotes, with the fee credentials, but it's just that single output Wasabi got the mixed fees with that could actually do the RBF child-pays-for-parent hybrid if a coin joins stalling in the mempool?

Speaker 0: 01:13:40

Yes, maybe.
Yeah, actually, maybe.
And users can pay at any time, maybe every hour, Wasabi will do an RBF of the child to fee bump.
And if there was no fee bumping, free credential being sent in that hour, then it also doesn't do the RBF.
Yeah, actually.

Speaker 2: 01:14:07

And that would be totally open for any user.
It's not like everybody has to chip in or split it up.
It's just like, if I'm super impatient, take my fee credentials, make that happen faster.

Speaker 0: 01:14:24

Plus the user doesn't have to spend his own chain coin right which would reveal his high time preference fingerprints while instead if the coordinator spends his fee output with the RBF thing, then we only know that some user in this coin join have the high time preference and paid for the fee bunk, but we don't know which one it was.

Speaker 6: 01:14:44

I don't think that would work because you would need to provide like all of the RBF scenarios of which there will be exponentially many in the size of the transaction for every single users.
Like every ordering of users choosing to bump fees should subtract some different amount and then all of those outcomes have to be pre-signed except for...
Why though?

Speaker 5: 01:15:11

I don't know.

Speaker 2: 01:15:13

We're not talking about the CoinJoin transaction itself.
We're talking about a child transaction with the Z-output.

Speaker 6: 01:15:21

I forgot what I said.

Speaker 2: 01:15:23

But so it's like

Speaker 4: 01:15:24

that, that should

Speaker 2: 01:15:27

be super private.
That would allow any user to accelerate the coin join without any privacy damage on their part and then three, like that could go to the extreme that wasabi literally burns that entire fee income for that round in two fees, but they're not going to do it unless they redeem tokens and then have the right to spend some reserved UTXOs on themselves so that like that's a complete privacy win and should totally balance out on WasabiSun.

Speaker 0: 01:16:00

Yep, because we already got the Vicon earlier.
And by the way, maybe even users who are not part of this CoinJoin can issue a fee bump.
Because as long as you have long-lived fee credentials, Any user can pay it.

Speaker 2: 01:16:25

Nadav, you are a whiz kid that inspires genius ideas everywhere you go.

Speaker 4: 01:16:30

To be fair, I credit Antoine Riard with all of the fee bumping stuff.
I just read his spec and gave it a review.

Speaker 2: 01:16:39

You still inspired something here because you are a Wizkid.

Speaker 0: 01:16:50

Yeah, but again, the statement still holds, right?

## Aggregated fee-bumping. / Efficient fee estimation. / Free riders contained within 1 transaction.

Speaker 0: 01:16:53

One user has to pay to fee bump the transaction of every user.
And so your SAT per divide is going to be very small.
But your nominal amount of SAT is still going to be quite large, if you want to make a meaningful difference.

Speaker 4: 01:17:09

Yeah, though you could also kind of view it as some kind of crowdfunding for fees scenario, where it'll go through.
Maybe that's not a good analogy, because you also are.
You want these.
There's important things in these, and different people will have different preferences.
But you know in theory you could have multiple people doing fee bumping and the fee bumping would all then kind of get aggregated.
Yeah, some people can always be kind of free riders in that scenario if they don't have too much at stake.

Speaker 0: 01:17:48

Yeah, but the nice thing is that the free riders are contained within one transaction, because the alternative approach to efficient fee estimation is what we used before in Wasabi 1.0, but that is not turned off, is to make child pays for parent of unconfirmed coin join rounds.
So to allow unconfirmed coins of a coin join outputs to remix.
And the coordinator slightly increased each round's fee a little bit, which was efficient to get all coin joins confirmed reasonably quickly, reasonably cheap.
But the downside was that if you were the first participant in the first round of coin join, like the parents transaction, the first unconfirmed, then you paid very little fees, While you were like at the end of the chain number 15 or something, your fee rate got higher and you don't even get faster confirmation for that because you carry like 14 parents that you still have to confirm.

Speaker 4: 01:18:46

Gotcha.

Speaker 0: 01:18:48

So with this approach, at least this free value problem stays within one transaction.
And I guess that's as small as it can get.

Speaker 2: 01:19:04

I mean, that's perfect though, because that just removes all of the dependency limits in the mempool except for remixing, right?
Because each thing would be its own parallel child pays for parent.
That's what you're saying, right?

Speaker 0: 01:19:21

Yeah, exactly.
Each coin is, sorry, each coin join transaction is one unconfirmed transaction.
And because the coordinator requires that all inputs to the coin join have been confirmed already.
This means that no coin from the unconfirmed coin join transaction can be registered in a new coin join transaction, and therefore we don't have child-based repairing chains.
We. Go ahead, Adam.

Speaker 3: 01:19:54

Sorry.

## Perverse incentives for individual users in Wasabi coinjoins. / Incentivise pro-privacy behaviour. / UTXO days destroyed. / Fidelity bonds in JoinMarket. / Mining fees. / Coordinator fees.

Speaker 5: 01:20:04

I did have a question, but it's a bit different topic.
Is that okay?

Speaker 0: 01:20:10

Sure, go ahead.
So,

Speaker 5: 01:20:15

I was thinking about the CBL things some of you might have seen on Twitter.
And I believe I got to the end of how far I can think about that and I properly went through the issue but it would be really nice if to hear what you guys think about that.
So the start is that there is a perverse incentive for the perverse incentive for the coin join fees with the current Wasabi, which is that the more user the coin join has, the exponentially more fee is being paid out by the Queen-join rounds, if I'm correct, and there is a fervorous incentive for the coordinator to add their own users.
So what do you guys think about this?
And I will not say what I think, just see if we get to the similar conclusions or not.

Speaker 2: 01:21:39

Do you

Speaker 6: 01:21:40

mean in the context of DLCs or coinjoins in general?

Speaker 5: 01:21:45

No, with current Wasabi coinjoins, the coordinate of the structure.

Speaker 6: 01:21:53

I agree 100%.
I think it's a problem and especially In combination with the discount, there's additional perverse incentives for individual users to register specific outputs.
And that can be combined to make sibling by somebody other than the coordinator also are a little bit cheaper.
So it's not just the coordinator.
I think it's perfectly possible to address it.
Like this is why I've been proposing a flat rate, some percentage of mining fee, perhaps, and on top of that, doing some sort of discount model for encouraging pro-privacy behavior.
So for example, bringing in an older input, something which destroys a large number of coin days, this is kind of like fidelity bonds and join market.
Like, you know that that input has not been sibling any of the rounds that were concurrent with this output not being spent, like after it was confirmed this could not have been used, this liquidity could not have been used to civil other rounds.
So it's good to incentivize that kind of behavior as well.

Speaker 5: 01:23:26

All right, so is it a perverse fee incentive?
Yes.
Let's keep it simple and only talk about the coordinator for now.
Does anyone not agree with this or we can move on and everyone agrees?

Speaker 2: 01:23:44

No problem.
With the coordinator, I mean, that's a special unique case because anything that they could do is free.
And that's like the whole problem with the fee schedule and sibling.
You have to balance between on one end, it being so cheap that you can sibble all day long, and on the other end, it being so expensive that people aren't going to remix, which is one of the most important properties of a system like this.
So it's like, If you're talking the fee schedule, I mean, I wouldn't talk about perverse incentives.
I would be talking about where is that middle spot where you accomplish both of those things.
It's not too expensive for people to be remixing, But it's not so cheap that you can just flood the system with liquidity and sibilant.

Speaker 6: 01:24:36

I know.

Speaker 5: 01:24:38

We'll get to that because I mean, yeah, sorry, Max, go ahead.

Speaker 6: 01:24:45

If I may just quickly, an important distinction here is mining fees and coordinator fees are very separate.
So Shinobi, your point stands when coordinator fees dominate over mining fees, but not vice versa.
Touche.

Speaker 2: 01:25:01

Versa.
Touche.

Speaker 0: 01:25:05

Yeah and one other quick thing is that this cheaper remixing for high quality coins, especially when we add a timeout benefit, right, so UTXO days destroyed, if that count is high then you get a cheaper coordination or mining fee.
This has similar denial of service protections as Fidelity bonds, though I would say weaker because Fidelity's bonds, you actually cannot spend the coin in this lock-up period, while with this type you could have spent the coin, but because you did not spend it, you get cheaper fees.
So it still improves denials, or increases denial of service costs, just in opportunity costs of not spending these coins.

Speaker 1: 01:25:50

Yeah, I

Speaker 2: 01:25:51

mean, I think that's a perfect way to balance that.

## Sybil incentives. / Fees for every mix round disincentivise Sybil attacks. / Samurai Whirlpool incentives.

Speaker 5: 01:25:57

All right so this is a fair birth incentive.
There is no question about this.
Now, is it a Sibyl incentive?
And I actually did not, I was not not able to come to the end of this question.
My conclusion was maybe, but you know what a Sibila is when most of the participants are actually one entity, right?
So the question is, would this lead to such a situation where most of the participants are one entity?
Is this incentivizes that much so that would happen?
You know what I mean?

Speaker 2: 01:26:52

Well, I mean, aside from the coordinator, I don't see how that could be the case if you're paying fees every time.
And I mean If the coordinator wants to sibyl their mixing pool, all they have to pay is mining fees.
Everything else is free.
But with anybody else, if you're paying fees for every mix round, I don't see how that encourages it.
That's a disincentive.
That's one problem I have with Samurai is their fee schedule incentivizes lots and lots of remixing, but the fact that you only pay once and everything else is free, I could just buy a new UTXO on Cash App every day and feed that into Whirlpool and just let that Sybil all day for free.

Speaker 1: 01:27:42

That's something you do to like prevent the coordinator from having like the ability to Sybil by just only paying mining fees, to just have like half or like a third of the actual coordinator fee just be sent to an operator and burn, or to have it donated to HRF or some fund?

Speaker 2: 01:28:05

Well, that's kind of what I think like NothingMuch was getting at with modeling the mixing fees off of the mining fees so that's that's always balanced the correct way there.
You can correct me if I'm wrong, nothing much.

Speaker 6: 01:28:21

Yeah, like you could make the flat, the sorry, the coordinator fees either be completely flat, so like some percentage of the amount, regardless of how many other inputs and outputs are in the transaction, regardless of how much liquidity is in the transaction.
That could be like a linear function of the amount or the weight.
And if you make it just a linear function of the weight, well then, you know, it's proportional to the mining fees.
It doesn't really matter like which of these specific scenarios, and it could be like a constant function not necessarily a linear function.

## Where is the equilibrium for coordinator fees? / Linear function of fee rate.

Speaker 5: 01:29:02

All right, all right.
So I didn't fully fleshed out, but I think somehow the, because if you think about it, if there are 99 real users, then it makes sense for the coordinator to join in, to be the hundred one, because 99 people will be paid after another peer, 0.003%, right?
So it makes sense if you're thinking about the big numbers, because then you will get 99,0003%.
But if you're thinking about the small numbers, one, if there is only one user, does it work for the coordinator to get into the round?
And the answer is it doesn't because that's only 1 times 0, 0, 0, 3 percent, and the coordinator will pay more mining fees than how much it would gain fees from that person.
So I think the question here, where is the equilibrium where the Bitcoin fees?

Speaker 6: 01:30:20

You know,

Speaker 5: 01:30:21

yeah,

Speaker 6: 01:30:21

the intercept is where I think it's roughly like 20,000 Satoshi's on average in coordinator fees for like a I may be misremembering, but like 0.1 times the number of users times 0.03 I think percent, sorry, so another two zeros.
But like you can calculate the expected value for the coordinator from like or not even expected just the value for the coordinator for that additional user and if the marginal cost in terms of the current mining fees of adding a single input and registering another fake zero point one output is less than that, then there's a clear incentive for the coordinator to do that.
So it's it's just a function of the current fee rate for the transaction.
And because, I mean, you could do this repeatedly, so long as the cost of an additional input and output is less than the figure without multiplying by the number of users, because the total amount paid by the user, that usually sums to several tens of thousands of Satoshis, as long as that increment is greater than the marginal cost of an additional fake user, well, that's a linear function.
So it's the same regardless of how many inputs and outputs were already added.

Speaker 5: 01:31:58

OK, so what's interesting here is that it might seem like there is a severe issue, but it doesn't because it definitely doesn't make sense for one people, two people, three people, five people, ten people, maybe at ten people it starts to make sense for the coordinator.
But you know, there is a line somewhere where it starts to make sense.
And so it doesn't mean that the coordinator is incentivized to take 99 of the existing users or something like that.
It just means even the coordinator participates with more users, it pays more mining fees.
You know what I mean?
Like there

Speaker 0: 01:32:48

must be a

Speaker 5: 01:32:49

line there where it starts to make sense, but maybe it's at 50 people.
I don't know, right?

Speaker 6: 01:32:55

It's a function of the fee rate.
So at one Satoshi per byte and let's say 100 bytes per fake user, let's say it costs 100 Satoshis to pay the mining fees for another Sybil user, if you can extract more than 100 Satoshis and coordinator fees from the target user or users, right?
So like the more users you're targeting, the less powerful your Sybil attack is for de-anonymization, but the more fees you can extract out of those victims.
So there's just a tipping point there, right?
It's just the intercept of two lines.

Speaker 3: 01:33:37

And it's-

Speaker 5: 01:33:38

Yeah, exactly, exactly, right?
But I'm actually gonna create a graph where you listening this episode, but this means it's not a civil incentive, at least not in the sense that people are using it to be, right?
Because there is no incentive to do it for smaller number of users.
So not the number of users as you're saying it, sure.
But anyway, you know what I mean.
It's not a Sibylle incentive, nothing the Sibylle incentive that where the coordinator is incentivized to be anonymized every month.
No, it's very far from the case actually.
It's a free ride incentive.

Speaker 6: 01:34:27

Well, no, it's worse than a free ride incentive because the coordinator actually increases its revenue if it does this.
But even if the tipping point, whether or not it makes sense for a Sibyl attack or only for extracting additional fees, that entirely depends on whether or not the mining fee rate is low enough.
And if the minimum rate is like one Satoshi per byte, that's actually not that high.
I think it's usually much higher than that.
I think it's on average more like 10 or 20 at the lowest rate.
So that implies that, yes, Adam, you're correct.
It's not really a direct incentive because an additional fake user would not, the cost would not be covered by the additional fees of just a single user.

## Are there any other incentives for Sybil?

Speaker 5: 01:35:26

All right, so now it's worth asking the question that, You know, here is a weak Sibyl incentive or a strange Sibyl incentive, but, you know, there are these incentives for Sibyl.
What do you guys think?
Can you identify some?
So, obviously, it is reputation, the largest civil incentive.
And it is also noticeable when you start to do that.
Do you guys see why?
So for example, we can tell with the current Wasabi that there is no CBL happening, or at least not this kind of CBL.
Why?
It's because we have 10,000 Bitcoin monthly volume, and the direct way, the known noticeable way to CBL it would be if we would be most of the participants of that of the 10,000 between if we would be bringing in that fresh those are fresh bitcoins not the actual coin join volume That's 40,000 But the fresh bitcoins monthly is 10,000.
So in order to CBL, unnoticeably, we would have to have like 9,000 Bitcoin or something crazy like that.
But if we would have 5,000 Bitcoin, then the last thing that we would care about is the perverse fee incentive, which at best, it's a couple of bitcoins, not 5,000.
You know what I mean?
It wouldn't make sense in that case.
Do you guys agree or disagree with that?

Speaker 6: 01:37:32

Mostly agree.
I think it's, you know, you need to actually crunch the numbers and figure out like at fee rate X, this is how much liquidity you would need to create a fake graph of this size in order to make, you know, hide the liquidity.
And you can reduce it to, like, what is the liquidity requirement and what is the marginal cost or profit for the coordinator to do, like, an additional round and parameterize that by how many real users are in the round.

Speaker 5: 01:38:08

We could also execute, okay, let's say we agree, then I say that I wasn't completely correct there because we could also execute a similar attack from less money, you know, from remixing.
Actually, I think that's what you were referring to by liquidity, right?

Speaker 3: 01:38:28

I

Speaker 5: 01:38:28

guess the confirmation or something like that.
Yeah.

Speaker 6: 01:38:34

It's not just that, it's also like how much in mining fees are you paying to create like a fake graph that does not look like remixing, which is like that's a distinction between fresh and remixed coins, right?

Speaker 5: 01:38:51

Okay.
So, but we also know that, you know, because this what, what the CBL would lead to in this case, if we don't have, don't have, if we are not matching the users' money with our own money, with multiplies of the users' money, we would have to have that much.
Then If that's happening, then we would see a very high number of remixes, and it's only 20 to 30%.
So that's not...
That actually proves that there is no...
This kind of CBL which may or may not be CBL happening.
Does that make sense?
Is there anything wrong with that?

Speaker 6: 01:39:43

No, I think that's correct, but I mean you need to take into account the possibility that you mix coins and then you create some sort of fake spending graph and eventually you cycle that back into the mix with, you know, a bunch of fake transactions in between which also costs you mining fees, probably a lot more than the mining fees for the coin join, in order to simulate fresh bitcoins that are actually just getting recycled by the coordinator.
That incurs a significant cost and I think it's, you know, If you look at the topology of the actual graph on the blockchain, it should be fairly straightforward to estimate that cost or even just measure it.

Speaker 0: 01:40:26

Yeah, but for what it's worth, the dumplings repo only uses one, like you can fool the dumpling repository into thinking it's fresh Bitcoin by just making one transaction.
So fresh Bitcoins are only the actual outputs of the coin joins, being inputs of the next coin join.
But if there's even one half of a single user transaction in there, it's not considered fresh anymore.
Or, sorry, it is considered fresh.

Speaker 6: 01:40:52

Yes, and I mean, that, if you are thinking adversarially, then the coordinator probably anticipated that and created, you know, anticipated the scenario where the dumplings repository was updated to take that into account, etc, etc.
You can still reduce that to a cost in mining fees at the bottom line.

Speaker 5: 01:41:20

So anyway, just to sum up, so is it a perverse incentive?
Yes.
Is it a civilian incentive?
Not really.
Not in the sense where people are using it, because maybe it would be a big CBL incentive, something like that, but not even in the technical sense, because in the technical sense the majority of the users should be controlling the volume.
And is there a CBL?
No, there is no CBL because it's noticeable, which is a disincentive.
And the final question is that why did we not change that?
It's because, you know, the fee structure is actually pretty fair, because you gain more privacy, you pay more, but that's not the real reason.
The real reason is because the fee structure is not something that, you know, that's the first agreement you have with all your users.
And if you are unilaterally just changing it without a very good reason like wasabi 2.0 which needs change anyway because of the protocol then you know like you're not changing around with the most fundamental parameters

Speaker 3: 01:43:00

That's good music by the way.
What

Speaker 5: 01:43:11

music?

Speaker 3: 01:43:16

What

Speaker 5: 01:43:21

music?
I can see someone is sharing their screen again.
Yeah, but guys, can you kick him out?

Speaker 0: 01:43:38

Trying but doesn't work.

Speaker 5: 01:43:42

Yeah, we need to use a private Jitsi.
Then maybe just let the music go for a while and then the live stream.
That would be a nice ending.
Yeah.
Yeah, maybe we should end the stream now.

## Closing thoughts.

Speaker 5: 01:44:03

Wasabi research club get hacked.
Tomorrow headlines.
Wasabi wallet get

Speaker 2: 01:44:15

hacked.
Can't have fun.
Can't be an adult because stupid children.

Speaker 5: 01:44:34

All right, thank you.

Speaker 0: 01:44:38

Any closing thoughts that Ben or Nadav want to bring up?

Speaker 6: 01:44:46

We should set up DLC contracts for whether or not there's a civil attack on Wasami.

Speaker 1: 01:44:52

There we go.
I was going to say thanks for having us, this was fun.
Always down to talk to you guys.
Yeah, thanks.

Speaker 3: 01:45:03

Thanks for coming.

Speaker 6: 01:45:03

Yeah, but thanks.
Thanks for coming.

Speaker 5: 01:45:10

Thank you guys.
It was really, really, you know, just thinking back when we started the Wasabi Research Club as exactly Not exactly more than one year ago then we were just gonna have have some fun reviewing all the privacy papers and putting them on YouTube and hoping that the authors of the privacy paper appear because this is publicity for them and then we can pick their brains and ask our questions and you know, that was fun and then for a long time it was just us basically thinking about all kinds of privacy things.
And it looks like you guys are taking this to a completely new level.
So, I mean, it's really, really awesome to see.
So, congrats for this.

Speaker 1: 01:46:18

Yeah, I mean, you guys are doing awesome here.
I remember when I was in college, just watching all your, like the Snicker one and the, oh dear, and all the different mix net ones that are really interesting.
And yeah, it's crazy what you guys are building now.
It's completely awesome.

Speaker 0: 01:46:42

Yeah, and I really like how it's all coming together.
Like I can totally see what we saw, the coin joints that open and close DLC contracts or lightning channels that then open and close DLC contracts.
That's going to be a wild, wild world.

Speaker 5: 01:46:57

Yeah, guys, we have again someone sharing their screen.
But yeah, let's end the stream and yeah, I think this was a good episode.
You know, I'm listening to this music like three times a day, super simple songs.
My son really loves it.
I can't even hear the song, but yeah.
