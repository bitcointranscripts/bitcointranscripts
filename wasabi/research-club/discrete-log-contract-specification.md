---
title: 'Discrete Log Contract Specification'
transcript_by: 'yousif1997 via review.btctranscripts.com'
media: 'https://www.youtube.com/watch?v=_ZDungWdxzk'
date: '2021-03-23'
tags:
  - 'research'
  - 'dlc'
  - 'coinjoin'
speakers:
  - 'Nadav Kohen'
  - 'Ben Carman'
  - 'Max Hillebrand'
  - 'Shinobi'
categories:
  - 'club'
summary: 'Today''s WRC episode includes Nadav Kohen and Benthecarman discuss the use of Discrete Log Contracts (DLCs) and their potential benefits and challenges. They explain that DLCs can enable various applications such as betting, options contracts, insurance, and synthetic assets. They highlight the advantages of DLCs, including high liquidity and fast trading of futures, especially once implemented on the Lightning Network. However, they also acknowledge that there may still be a need for centralized solutions depending on the specific use case. The speakers delve into the technical aspects of DLCs, including the transition to Schnorr signatures and the privacy implications of using DLCs. They also discuss the role of oracles in DLCs and the potential for coin joints with DLCs. Overall, the speakers provide a detailed overview of DLCs and their potential applications in the cryptocurrency space.'
---

## ## General overview of Discrete Log Contracts (DLC).


Max Hillebrand: 00:00:07

So, everybody, welcome to this episode of the Wasabi Wallet Research Experience.
This is our weekly research call where we talk about all the crazy things happening in the Bitcoin rabbit hole.
We can use them to improve the Bitcoin privacy for many users.
And today we got the usual reckless crew on board, but also two special guests from Suredbits.
We have Nadav Cohen and Ben The Carman.
How are you both?

Ben Carman: 00:00:36

Good, thanks for having us.

Nadav Cohen: 00:00:39

Yeah.

Max Hillebrand: 00:00:44

Really cool, So maybe we can just get going with a quick introduction of what is the very general overview of 'Discrete Log Contract's that you're working on in Surebits.

Ben Carman: 00:00:57

I mean, like the highest level explanation is just, you have a Bitcoin contract or a Bitcoin transaction that's contingent on an `Oracle` or set of `Oracle`s attesting to an outcome.
So you do something basic like betting on the Super Bowl, or something more complex doing like, you know, an options contract on the Bitcoin price.
So, actually like what you're betting on and what the `Oracle` is signing is kind of limitless.
And it's just like what you can build on top of that.


## Uses of DLCs. / Betting. / Options trading. / Insurance. / Synthetic assets. / Any financial contract.

[EB]: 00:01:32

Yeah, I have a question.
First question.
What are, in your opinion, the most obvious uses of this technology?
For example, betting is one that you just mentioned.
What other things can be done with this technology?

Ben Carman: 00:01:53

I mean something that's coming out soon is if you saw Atomic Finance is releasing their options like trading with `DLC`s so that'll be a way where people can buy and sell covered calls directly on Bitcoin without needing to use an exchange, which I think will be pretty cool.
You can also use this for things like insurance or things like, just like basically any existing financial contract that you have, or like something like derivatives, or you can also use it to like hold other assets for like something we did.
So we've like basically created a synthetic dollar by just like having your payout be like you know you start with like $50 worth of Bitcoin and you end with $50 worth of Bitcoin and so you do that without dollars you could do that with Apple stock you can do that with like literally anything so and kind of the possibilities are kind of limitless.
It's just figuring out how to do all these things.
Nadov, do you have anything to add?

Nadav Cohen: 00:03:00

Yeah, I mean I think you hit all the really obvious ones we already know about betting, trading, hedging, and I guess synthetic assets.

## Finding counterparties. / High liquidity, high speed trading. / Cooperative transfers. / Matching engines.

[EB]: 00:03:14

In this case, the contract has two parties, right?
I mean it's two people involved.
In most of the financial contracts there are also two people involved but given there is a high liquidity it's transparent for you.
You don't need to find someone to make up this contract.
There is a system that can find the counterparty for you, right?
That if you want to sell, for example, what you want, sorry, what you have.
Do you think these contracts can replace that kind of, or can be used to build this kind of high liquidity and very fast kind of trading of futures or whatever?

Nadav Cohen: 00:04:12

Yeah, so I think to some extent the answer is yes, especially once we have `DLC`s on Lightning and we can do things like cooperative transfers as well.
And, you know, of course we need some kind of matching mechanism and there are lots of ways to go about approaching that problem.
But I will say, I mean, at the end of the day, I think there will be lots and lots of use cases for `DLC`s. But I expect there will still be some amount of more centralized solutions that people want to use in cases where they're willing to take on, or in the cases where the trade-offs that `DLC`s take don't make sense for them and they wanna use like a centralized third party or something like that.

## NASDAQ execution time vs self-sovereignty assurances.

Ben Carman: 00:05:08

Yeah, like we'll never rival the like NASDAQ execution time but you know, they'll never rival our, you know, self-sovereignty version of it.
So, you know, it's really like what the user wants.

## How will DLCs change when Taproot and Schnorr signatures are available? / ECDSA Adapter-Signatures. / Thousands of signatures per DLC.

[EB]: 00:05:22

Okay, Max, just in case, jump whenever you want.
I can make questions all the day, right?
But now I have another question because this was implemented, this is something that exists today, I know it's available, right?
But it is not using, I think, ``Schnorr`-Signatures’, right?
That first, if that is correct, how can this contract change when that `Taproot` is merged and available for the Bitcoin network.

Ben Carman: 00:06:09

Nadav you can probably answer this better than me, you're very technical.

Nadav Cohen: 00:06:12

All right, Yeah, so right now we're not using `Schnorr` On-Chain.
We're using `ECDSA` `Adapter-Signatures`.
And once we have `Taproot`, then we can use `Schnorr` On-Chain and use `Schnorr` `Adapter-Signatures`, which will be much, much nicer.
They're like nearly three times smaller, much faster to compute, much faster to verify, and since these are like the things that you're building to sign all the Off-Chain transactions like you're dealing with like tens of thousands, sometimes more, of these signatures per `DLC`, at least if you're doing like financial contract stuff or numeric contract stuff I should say. And so.

## Adapter-Signatures are Off-Chain.

Max Hillebrand: 00:07:03

Nadav, one question, you said that the `ECDSA` `Adapter-Signatures` are three times larger, but aren't, like, is this the On-Chain data that's three times larger compared with `Taproot`?

Nadav Cohen: 00:07:13

No, no.
So `Adapter-Signatures` aren't valid On-Chain.
`Adapter-Signatures` are kind of an entirely Off-Chain construct that's very closely related to the On-Chain signature scheme.
Yeah, so actually `Adapter-Signatures` for `ECDSA`, You have your like 65byte like actual signature.
I mean it's not DER encoded but whatever.
And then you have like a 97byte zero-knowledge-proof of discrete-log-equality or PUDL.
And Yeah, so there's kind of extra steps because we're going through `ECDSA`, whereas in `Schnorr` you just have a nice little 64byte `Adapter-Signature`.
And then also all of the computations on those are much faster, or at least significantly faster.
So that's kind of the first nice thing.
And then the other nice thing, though I'm not sure whether or not we will or, you know, when we'll get around to utilizing this, but you can use `Adapter-Signatures` in `Schnorr` with key aggregation, which is just crazy significantly harder in `ECDSA`.
So right now with `ECDSA` `Adapter-Signatures` we are using single signer `ECDSA` `Adapter-Signatures` so that we need like a two-of-two On-Chain, but with `Taproot` that can also just become like a single Pubkey On-Chain.
So long-term for `DLC`s in a taproot future, a `DLC` On-Chain looks like some money moving into one Pubkey and then moving out to two other Pubkeys and that's all there is to it On-Chain there's nothing else that shows up On-Chain.

## Are multisig scripts On-Chain?. / 2-party ECDSA. / Easy to get ECDSA wrong.

Max Hillebrand: 00:09:10

Okay and just to confirm right now you have the `Multi-Sig` script On-Chain?

Nadav Cohen: 00:09:15

Yeah right now it looks like some funds moving into a 2 of 2 and then leaving to 2 outputs.
So it kind of looks like a lightning open close.

Max Hillebrand: 00:09:23

I mean you could use two-party `ECDSA` to compress it to a single Pubkey too.
Why did you not do that for this MVP?

Nadav Cohen: 00:09:32

Because I want to sleep at night.
Yeah, I mean, the dirty secret is that, you know, basically anything you can do with `Schnorr` you can do with `ECDSA`.
It's just very easy to get wrong at every stage.
And it's just a much larger attack surface.
And implementation complexity and getting people to look at that code is very hard and all the other kind of challenges that go with it.
So yeah.

Max Hillebrand: 00:10:07

Yeah.
And Taproot makes it obsolete, so.

Nadav Cohen: 00:10:10

That's right.

Max Hillebrand: 00:10:11

Waste of time.

## DLCs look like Lightning Channels On-Chain.

[EB]: 00:10:15

Okay.
One more.
I think I know the answer but
these contracts are not easy to identify or I think it's not probably possible to identify On-Chain, right?
I mean if there is a transaction that basically I was betting something to Max and Max won the bet, the transaction is not, I cannot say, observing the transaction On-Chain, I cannot say, hey, this is a payment to Max, right?

Ben Carman: 00:10:55

No, not at all.
Like the `Oracle` can't tell you're using them.
Only The only people that could tell is like you and your counterparty.
It's literally just like a 2 of 2 `Multisig`.
So people probably think it's a lightning like channel at first because that's way more common than `DLC`s at the moment.
But yeah, It's like very private in that way.

[EB]: 00:11:19

Exactly, but with taproot, you will not even be able to say this is a two parties, a `Multi-Sig`nature.
It's just a normal transaction, isn't it?
Or am I wrong?

Ben Carman: 00:11:32

No, that's correct.
Yeah, it was like in the like, you know, years from now when we have like full taproot support yeah, it'll look like just you know, like 2 inputs fund this this Pubkey and then this Pubkey sends out to, you know, two other outputs.
And it could be a user wallet, it could be someone consolidating `ETX`s, it could be whatever, it's just, it looks very non-augmented.

Nadav Cohen: 00:11:58

It could be a payment with change.

Ben Carman: 00:12:00

Yeah, it could be a payment with change.
It could be anything.
So it'll be very hard to tell what's going on.

## Can withdrawal payment output be to a 3rd party address? / Multiparty DLC.

Max Hillebrand: 00:12:04

Can it actually be a payment?
Like do you think that the software will be in a way that the withdrawal transaction can be to an arbitrary address, even to a third party who was not involved in the contract in the first place?

Ben Carman: 00:12:17

I don't see why not.
Like you just specify an address for your payout so you could set it to like instead of being it to your own wallet, set it to deposit to like your friend or deposit to an exchange or whatever you want.

Nadav Cohen: 00:12:32

Yeah, and in the future, or so first of all, just to have it outcuts go to, you know, more than two parties is it's quite simple.
I mean it's not implemented or specified right now but totally possible if there was a use case, that wouldn't be a hard thing to add.
And then on top of that, in the future, we'll probably have more multi-party `DLC` stuff available anyway.
So yeah, I think that you can intermingle kind of payments with these things as well.

## Privacy implications of DLCs. / No one but your counterparty knows what is going on.

[EB]: 00:13:07

Well, it's very interesting because you know that we like things that when you cannot say what is going on On-Chain we like it, right, so I was imagining that probably if we have a huge amount of these transactions that you cannot say what is happening, who is paying whom.
It could be useful, I mean it has privacy applications probably.
Have you something in mind, have you discussed these properties before?
I'm sure you did.
Can you share with us your thoughts about this property for privacy?

Ben Carman: 00:14:05

I think it's huge for privacy, just like being able to do financial contracts where no one but your counterparty knows what's going on.
Like today, you know, you have to like go through a financial institution to be able to do really anything and you get KYC'd and all that versus this like completely permissionless and open all you need is like some stats to open up the contract.
So I think that'll, I think like one of the huge things is like today in the world we have like the US financial institution that's like has like all the network effects and money and like if you can't get access to that you kind of get boned in the Traditional finance world but with this like, you know You could be some like guy in Nigeria with just an internet connection and some bitcoin and like have like, you know, all those financial products now.

## How much do I have to trust the Oracle? / Sets of Oracles. / Predefined refund if Oracle does not sign anything. / Impossible for Oracle to lie privately. / Publicly verifiable fraud proofs.

[EB]: 00:14:56

I have a more concrete question.
How much I have to trust on the `Oracle`?

Ben Carman: 00:15:05

I mean it depends.
So you can you don't have to use a single `Oracle`.
You can use multiple.
So like what we released last week was we did like a two of three setup where if two of three `Oracle`s agreed on a average bitcoin price then our contract could execute.
But so you don't need to trust like a single `Oracle` completely but at the end of the day like your `Oracle` or a set of `Oracle`s completely was going to dictate your outcome.
So like if they're all hacked or regulated or go offline, like your contract is screwed and there are ways to like, you could like, since it is just a two of two `Multi-Sig`, you can collaborate with your Counterparty to close it in a different way or we do have like a predefined refund so if the `Oracle` never signs anything you get your money back, but You know the `Oracle` can like you know if you're using a single `Oracle` and they sign the wrong outcome like That's just gonna be what it is and you're kind of screwed there

Nadav Cohen: 00:16:05

Yeah, I will note though so it is true that your contracts that you have open, that the `Oracle`s, if they lie or are corrupted or something like this, if that happens, the `Oracle`s, or sorry, the `Oracle` contracts that were based on that specific event get wrecked.
But the kind of `Oracle` model for `DLC`s has kind of users as entirely private entities and `Oracle`s as entirely public and oblivious entities.
So it has, first of all the nice property that `Oracle`s don't know anything about their users off the bat or at least it's very tricky for them to learn anything about their users and how they're being used and if they're being used in these kinds of things.
Which is nice, you know, I always tell people that when you're dealing with `Oracle`s and trust models in general like privacy is a part of security.
It's just part of a security model.
But then on top of that because `Oracle`s are public entities in `DLC`s there is no real way for them to lie privately.
If you get, you know, if `Oracle` that you're using lies, even if they like say lie privately to your counterparty, you can recover that lie from On-Chain information using the Off-Chain information that you have from the transaction that your counterparty uses.
So at the end of the day you can still construct publicly verifiable fraud proofs that the `Oracle` attested to something that was false or equivocated or something like this.
And so in the future I think that there will be lots of ways for `Oracle`s to essentially you know put their money where their mouth is and stake funds that can be taken away from them if they lie.
Because at the end of the day, and even if that's not the case, you know, just from like a more reputation perspective, like it's impossible for them to lie in private, essentially, is a nice property of `DLC`s.

Max Hillebrand: 00:18:22

Yeah, really cool.

## Funding transactions into DLCs can break common input ownership heuristic. / Chaumian DLC.

Max Hillebrand: 00:18:23

I have one more question on the more On-Chain layer.
So the funding transactions into that, `Discrete Log Script`, has two inputs from, or an input from each user.
So both of those provide.

Nadav Cohen: 00:18:37

At least one.

Max Hillebrand: 00:18:38

Provide at least one in the same transaction.
And the nice thing is this also breaks the common input ownership heuristic.
And it's the same as dual funded Lightning or `Payjoin`.
So this is actually a nice benefit for On-Chain privacy in general.

Ben Carman: 00:18:55

Yeah, I think this is really huge, where you kind of get like a mini `Coinjoin` there, and something that I wrote a while back, but a thing where you could do like, I call it a Chowmian-`DLC` where you could batch a whole bunch of `DLC`s together and then like you have like a basically a whole bunch of inputs going into like a bunch of different `DLC`s all in one giant transaction.
And now you like really break the common input heuristic there.

Max Hillebrand: 00:19:23

Yeah, exactly right.

## Coinjoins with DLCs.

Max Hillebrand: 00:19:24

That's the logically following next question.
I'm curious, maybe Yuval or Nadav have interesting points on the nuances of `Coinjoin`s with `DLC`s.

Ben Carman: 00:19:37

I mean, I think, I think like it's theoretically possible to be able to like have a like similar to like Wasabi's model where you have like a coordinator but instead of this coordinator just giving and passing around details about the coin transaction you guys would also pass around stuff about your `DLC` and the nice thing too with this is the coordinator could actually close the contract for you if they are connected to the `Oracle`.
So there's some like actual `UX` improvements there too where you know you don't need to be online and actually close your own `DLC`.
Yeah, the gist of it is just like, you know, you set up or like you say, I have like 50 participants all doing a contract and then they take one side of the bet and the other, say like half take one side of the bet, half take the other, and then they all register inputs and basically just create a giant `DLC` and then all the payouts go out at the end.
I don't know.

## Non-DLC users on the same Coinjoin. / Mixed pools. / Channel factories.

Max Hillebrand: 00:20:47

Yeah, One note here is that if all of the users of this `Coinjoin` use `DLC`, then it's kind of like a bad fingerprint in terms that you know that for 100% sure this is a `DLC` contract.
Well, if there are other non-`DLC` users in the same `Coinjoin`, then because of `Taproot`, they look the same.
This would be huge, because then you don't know which user is part of the `DLC`, which has to pay join, like amount consolidation.
And that would improve amount analysis massively for everyone I think.

Nadav Cohen: 00:21:24

Yeah I think that's totally doable and we've thought about kind of this where you can just mix pools where you have people who are doing `DLC`s with people who are doing `Coinjoin`s with people who are opening lightning channels or in the more distant future channel factories and all these kinds of things at the end of the day You can always just like save a little bit on fees by throwing everyone's inputs and outputs on the same transaction.
Of course with `DLC`s in particular, there are ways around this where you can kind of have like a multi-stage setup, kind of closer to how they've been working on putting multiple Lightning funding transactions, multiple Lightning channel opens in the same transaction.
You could do something like that with `DLC`s and `Coinjoin`s and all just kind of in one transaction.
But if you wanted to actually mix kind of normal `Coinjoin` users with `DLC` users then there is kind of the, I suppose maybe not for everyone this is a downside, but the downside of like there's a long time between going On-Chain and paying out Because you have to wait for like the `Oracle` event to happen or something like this but you know if someone's mixing coins they don't need to be sending anywhere anytime soon then maybe this isn't a big deal.

## Increase anonymity set.

Max Hillebrand: 00:22:55

It's actually a cool privacy benefit of having time-staggered remixes.
It increases your anonymity too.

Ben Carman: 00:23:04

Yeah I think that could be really big too, because the only downside there is that, at least in today's `Coinjoin`s, you would have to use the same output amount.
So if you're doing like Wasabi, it's like the 0.1 Bitcoin.
But with the stuff you guys are working on with Wabi Sabi, you kind of get rid of.

Max Hillebrand: 00:23:26

Wabi Sabi fixes this.

Ben Carman: 00:23:27

Yeah, Wabi Sabi fixes this.
And then you could do an entire thing where you know you could have any contract really going in on there and Really privately with everyone else's transaction.
That'd be awesome.

Nadav Cohen: 00:23:40

Yeah, and another thing.
I just realized that I forgot to mention that is like a benefit of doing things this kind of way, at least for `DLC` users, is if you have, you can essentially use netting while you're doing this.
So if I have a position open with two different people who are also participating here and there's like some overlap happening, then really all that needs to happen in the more `Coinjoin` looking transaction is kind of the aggregation so I can like recover some collateral or things like this.

## Wabisabi and consolidation of payouts.

Max Hillebrand: 00:24:19

Yeah, especially with WabiSabi that allows for multiple outputs being registered at different values.
Like consolidation of multiple refunds or payouts can be done too.
Maybe.
I mean, therein the nuances of course, like how much information does the coordinator learn?
That's something for you all to figure out, I guess.

Yuval: 00:24:44

As far as I can tell, there shouldn't be any requirement for the coordinator to be involved at all.
There might be added value, like if the coordinator is also helping to mediate this kind of net settlement, like making the actual outputs allocations more efficient, that might be a good reason to involve the coordinator.
But I'm a little bit rusty about `DLC`s, but if I understand correctly, the way that you would do such a thing is two users would just register their funding amounts to a Wabi Sabi `Coinjoin`.
They would negotiate the Off-Chain contract.
And then at the signing phase, Once the transaction ID is already locked in, assuming only `SegWit` inputs are allowed into the transaction, at that point the refund transactions and stuff like that, exactly like a Lightning channel, can be pre-signed before both parties to the `Coinjoin` provide their `Coinjoin` signatures.
So at least in theory, it should already be possible.

Max Hillebrand: 00:26:00

You spoke about the deposit into the `DLC`, but what about the payout and the withdrawal of the `DLC`?

Yuval: 00:26:07

If I understand correctly, once the two of two output is already locked in and funded, the `Oracle` will publish its attestation, I guess, for lack of a better term.
Sorry about that.
And then one of the parties to the transaction will be able to unilaterally spend that.
At that point, especially if it's a`Taproot` output, of course, they could negotiate to just do like a payout transaction that spends that much like `Coin Swap` settlements work.
And equally, they could bilaterally agree to register this output as an input to a subsequent `Coinjoin` if complex scripts are implemented.
Like if you're able to do arbitrary input types and not just `SegWit`, PayToWitness PubKey Hash inputs to `Coinjoin` transactions, then at that point, like, there's no difference, right?
Like, the ownership proof is equivalent to the collaborative spend path.
And Yeah, it's just a matter of the two parties like agreeing who actually uses the credentials to register outputs.
But that's like, there's no theft risk there.

## UX improvement if coordinator automatically uses Oracle signature. / n-of-n outputs. / Obfuscation: wave functions, cancelling noise.

Max Hillebrand: 00:27:46

But to build on top of that because Nadav said that there is this `UX` improvement that the coordinator can automatically take the `Oracle` signature and do initiate the withdrawal transaction but I'm not sure how this would work with `Coinjoin`s in a non-custodial way because you cannot pre-sign the `Coinjoin` transaction because you don't know the `Coinjoin` transaction.
So how would that work?

Ben Carman: 00:28:10

They couldn't close it in a `Coinjoin` transaction for you, but if they had your outcome signatures and they got the `Oracle` signature, they could close it like in the easy case where it's just like a single transaction that just has the output to the winner.
But if you wanted to do like the `Coinjoin` close, you'd have to do that cooperatively with your counterparty.

Nadav Cohen: 00:28:35

So I think another thing to mention, I kind of mentioned that there are two different ways of doing this.
One of them is closer to like the multiple lightning channel openings, which I think is what we're currently discussing, where you have a bunch of inputs and then a bunch of two of two outputs.
But another way of doing this that I think Ben has proposed, which has its own trade-offs, is having a bunch of inputs and then a single n of n output, and then a single transaction spending that n of n output in the end, which closes all of the `DLC`s. And this would be the situation where it would make a lot of sense to have a coordinator be able to just broadcast that mass closing.

Ben Carman: 00:29:25

Something you could also do is, well, maybe not, but you could just have your counterparty's signature be, have the `SigHash` flag for `SigHash` single, so it's only committing to the payout output, and then you could put that output in the `Coinjoin` transaction.
The only problem is though, then if you're using that `SigHash` flag, you're kind of revealing which output is yours.
So maybe that wouldn't be the best, but you're still kind of, you know, at least you're saving on fees that way by sharing all the metadata in the transaction.

Nadav Cohen: 00:30:00

Yeah, and it is important to note that for this end-of-end scheme to work, you do gain some information about the other people in the mix because you know what their outputs would be on `Oracle` Outcomes.
But there are a couple ways to mitigate this.
I don't think this has been well thought out or modeled yet.
But you can, for example, have rather than one output per participant, you can have multiple outputs where essentially if you picture, like, say, the `Oracle` outcome on each party has a payout curve, you can decompose that payout curve into some wave functions or something like that, where each output looks nonsensical, essentially.
And you don't know which aggregation of outputs corresponds to like which entity or things like this.
Or there are a couple other ways of kind of trying to do obfuscation where you can have like canceling noise on multiple outputs.
But again, this hasn't been thought out too well yet.

Ben Carman: 00:31:08

Also, I think another possible way you could do it is, and once you have the `Taproot` thing, we just have like a single key behind the funding output, you could, in the cases where a single party gets all the winnings, you could instead of signing a transaction, upon getting the `Oracle` signature, you could have them just get the other user's private key, and then you could use that to then, so then they could, then they just own the input completely unilaterally, and they could use that to register for a `Coinjoin`, and just like spend it from there, however they see fit.

## Coordination complexity of signing rounds.

Max Hillebrand: 00:31:54

And one of the other constraints that I see is the coordination complexity and how much that increases when like two users need to collaboratively look at the `Coinjoin` and only after they have come to an agreement, sign the `Coinjoin`.
So what do you think?
Will this lead to more failed signing rounds just because the users don't communicate properly?

Nadav Cohen: 00:32:21

So I think, with `DLC`s, you have, you're signing so many things.
I, I don't think that, adding this, this `Coinjoin`ing stuff really has a significant increase in how many things you are signing and validating and such.
It could change like the size of the thing you have to validate before you sign, say, or the thing you have to hash before you sign, rather.
But at the end of the day, even, for example, for the n of n scheme, where they're like, for every possible, or for every relevant possible `Oracle` outcome you have a separate closing transaction for all end parties.
If you were doing just a two-party `DLC` in the usual way You would still have to sign that many things, or at least on the same order of magnitude.
And so you know, I think at least in kind of a coordinated model it's not a big difference, where you have some kind of one party that is communicating with many other parties.
If it's more of like a gossip-based mixing protocol, then this might be significantly harder.

## Speed of signing rounds.

Max Hillebrand: 00:33:46

Maybe a more concrete question.
So if Nadav and I want to fund this `DLC` contract, we register our inputs in the `Coinjoin` that we want to use in the deposit.
In the next round we register our output address, which is one cooperative, or like one of our cooperative `DLC` contracts, and two changes for each Nadav and me.
Then finally, this gets put together by the coordinator, and we go into signing phase.
And now, both Nadav and I have the `Coinjoin` transaction, which we will use to do the pre-signed refunds transactions and all the `DLC` stuff that needs to be done.
And then after all these refunds are signed, then we put our final signature on the `Coinjoin`, like both of us on our own individual `UTXO`s, and register them in signature registration.
Is that roughly correct?

Nadav Cohen: 00:34:46

Yeah, that sounded right to me.

Ben Carman: 00:34:49

Yeah, I think you could, because like with that 'Multi-Oracle' `DLC` that me and Nadav did last week, like it took us like five minutes to sign everything.
We still have some optimizations to do to make that faster.

Nadav Cohen: 00:35:02

And by some he means all.
It will be much faster by the time we're done with it.

Ben Carman: 00:35:07

But it's still like, you know, it's not as fast as like because I think like in wasabi You have like what 20 seconds or something to sign?

Max Hillebrand: 00:35:15

So I think it's a three minutes timeout for the signature basically.

Nadav Cohen: 00:35:19

That'll be good.

Ben Carman: 00:35:20

Okay, so maybe but yeah something you could do like if it was like, you know, if you were pushing on that threshold, because you do need this both parties do need to sign and verify each other's stuff.
So something you could do is just you give each other the refund transaction signatures and once the fine transaction is confirmed or after it's been at least broadcast, then you can start doing your outcome signatures.
So at least that way you're guaranteed to get your money back if something goes wrong.

Nadav Cohen: 00:35:52

I think that has a bunch of free option problems probably.
But yeah.

Ben Carman: 00:35:58

Probably.

Nadav Cohen: 00:35:59

But I do think that if it's a three minute timeout in the future, this isn't going to be a problem.
Like we have lots and lots.

Max Hillebrand: 00:36:08

I'm actually not sure what it will be in the future.

Nadav Cohen: 00:36:09

Okay.

Max Hillebrand: 00:36:10

But I think right now it's three minutes.
Yuval, what are your thoughts on signing period timeout?

Yuval: 00:36:16

So generally I would say it's probably going to be variable.
Like we've been thinking about scenarios like `PSBT` support or hardware wallet support.
And if it's `PSBT` support for like a manual thing, you know, maybe some rounds would even have a signing phase that's on the order of hours for, you know, high value `Coinjoin`s or something like that.
I think that's something that even if the Wasabi coordinator doesn't deviate from the current timeout values and there is demand, I'm sure that some coordinator would come up and offer those round parameters.

Nadav Cohen: 00:37:07

Cool, yeah.
So I mean, `DLC`s require, I assume, at least usually, less time than using a hardware wallet.
So that's good to hear.

## Coordinator rounds determined by the user.

Yuval: 00:37:22

For what it's worth, like one idea we were kind of spitballing is having the, like making all the coordinator rounds basically determinable by the users.
So if there's no round available right now with parameters to your liking, for example, the fee rate might be too low or too high, or you want a `Coinjoin` with a larger minimum input amount or something like that, we still need to think this through.
But it seems reasonable to just support like a specific user asking.
I mean, it's probably not going to be exposed in the front-end directly just because it's a kind of a low-level feature.
But there's no technical reason, and I think no game theoretical reason why the coordinator should not support the ability to just ask for a new round to be created.
So I'm optimistic about these kinds of possibilities opening up.

Max Hillebrand: 00:38:59

Okay, cool.

## Benefits of amount consolidation. / Pay-to-endpoint over Wabisabi. / What information does coordinator need? / What information do the users need?

Max Hillebrand: 00:39:00

Maybe I think one topic just to rehash and to dive deeper is the benefits of the amount consolidation of two users.
Maybe Yuval, if you have some further thoughts on this `Payjoin` similar type of amount consolidation.

Yuval: 00:39:21

So that was kind of implied by the scenario I was describing earlier, just to get everybody on the same page.
The idea behind, So I'm hesitant to call that `Payjoin` just because `Payjoin` kind of implies more.
It implies the steganographic features as well.
So I think like a pay to endpoint over Wabi-Sabi or a credential payment or something like that is perhaps a better term.
But the idea is like let's say Alice wants to pay Bob some amount, she registers inputs greater than that amount and produces in her registration, she requests a credential worth the payment amount and then she just gives that to Bob.
Alternatively, she could ask Bob for a credential request and then she has no opportunity to use it herself, but in either case there's no theft concern.
Bob can then go and use this to register his output for the received amount, or he can consolidate it with his own inputs to get better privacy.
And this is nice because it protects Alice's inputs from Bob's prying eyes and vice versa.
And yeah, it's like that's kind of how you would have to do it anyway for like the simple case.
What I would be kind of like more interested in hearing Ben and Nadav's thoughts, like in the scenario where the coordinator is kind of mediating the bets themselves, especially in a net settlement setting, what kind of information would the coordinator need to know, and what kind of information, like, do the individual users need to exchange in order to get that settlement going because I think that's Kind of the logical continuation of this this type of pay to endpoint approach

Shinobi: 00:41:49

Real quick before the dive and Ben answer that, in a naive case…

Max Hillebrand: 00:42:01

we're losing you.

Shinobi: 00:42:02

This isn't there still some change output from each other?
You're still obscuring things for a third party observer where that payment looks like a single user's change output?

Yuval: 00:42:14

So You were breaking up, but if I think, if I understand correctly, then yes, I mean, you're not disclosing that there even was a payment, and further, you'd be breaking the sort of heuristical assumption that you can partition the transaction into like one set of inputs and outputs per user that's going to balance to zero.
So this is like further helps to break down the common owner input heuristic.
But like, I'm not sure what you meant in the chat by pass on an output credential for unmixed change.
The credentials.

Shinobi: 00:43:07

Well, I'm saying like, if I put my input in there and get my mixed outputs and then give you an unmixed change output, like that will look like I'm just getting my unmixed change back, but I paid you.
And even though we still see that graph between the two of us, like nobody else can interpret that graph correctly.

Yuval: 00:43:29

Yes.
And that is a much simpler scenario because there's no interactivity, there's no pay to endpoint.
All you need to do is give me an address and I register some output with your address.
Like in the pay to endpoint scenario, you do have much better counterparty privacy, because there like the only thing I learn is what credential am I giving you?
I don't learn how you're actually using it.
And Of course you can in theory combine it with your unrelated input credentials which I don't know about.
And then the payment amount is also hidden and never appears in the transaction.
So many privacy benefits.

Ben Carman: 00:44:21

To go back to nothing much as an original question, I think to have the coordinator like be doing like acting as like a watchtower, I think all you'd have to give them is like the `Oracle` that they'll be fetching from to get the signature and then like your actual outcome signatures.
So doing so you kind of reveal what your contract is to the actual coordinator, but you also then get this kind of watchtower thing where they can close it for you and you don't need to be online and make sure you do it, which is huge `UX` improvement.

Nadav Cohen: 00:45:00

Ben, are you talking about the two of two situation where there are a bunch of two of two outputs?

Ben Carman: 00:45:05

Yeah, yeah, I guess if you have like, you know, like a-

Nadav Cohen: 00:45:07

Gotcha, or yeah, I was just gonna mention in that case, a really what you can use generally speaking is a watchtower.
And you know, If coordinators are some kind of watchtower in the future, they can also be used for that purpose.
But you can also just use normal `DLC` enabled watchtowers in the future.
But yeah, go ahead and talk about the n of n case if you want.

Ben Carman: 00:45:29

Yeah.
So if you had like a 50 of 50 like kind of thing, I think you still reveal your, your contract in that way, maybe less.
So

Nadav Cohen: 00:45:42

no, I think you would have to reveal quite a bit, actually, in this case, which is why you need kind of other obfuscation methods.
If I'm not mistaken, all of the contract execution transactions are now like aggregate amongst all 50 peers and they all have to sign the closing transactions for everyone.
And so they see kind of what the output values are.
And so you need to do some obfuscation on them, I think.
Ben, is that right?

Ben Carman: 00:46:10

Yeah, I guess you do get the benefit though, like where the coordinator won't know like which address is going to like which user.
So you do like, they'll know like, you know, this person or this address gets paid out if this, you know, if the price of Bitcoin is 10K or whatever, but they don't know directly like which user registered the payout address.
So you get the benefit of, hiding that, but they still can see like what the payout curve is for each address.

Max Hillebrand: 00:46:39

Yes but you might actually be able to do some amount decomposition of these payout transactions.

Nadav Cohen: 00:46:44

That's right.

Max Hillebrand: 00:46:45

Right so you have one input worth one Bitcoin and to break that down into 0.4 and 0.6, for example, naively said, but of course there's more signing.

Nadav Cohen: 00:46:54

I don't think that it will require necessarily more signing, But I think what happens is that rather than everyone passing around their contract info, the thing that's used, essentially their payout curve for `Oracle`, as what the `Oracle` says is the x-axis and their payout as the y They take their payout curve instead and they break it up into pieces with canceling out noise And register multiple outputs and then passed around these nonsensical noise full payout curves as if they're coming from different people.
And so everyone should have pretty nonsensical, if this works out anyway.
Again, I haven't looked into it deep enough, but everyone should be able to pass around somewhat nonsensical payout curves where each person is actually getting the aggregate of multiple payout curves, but no one else knows what that looks like.
Then hopefully that mitigates things a little bit.
And furthermore, once you have everyone's payout curves, you can construct for yourself deterministically all of the closing transactions that you need to sign and validate signatures of.

Ben Carman: 00:48:18

Okay, yeah, that makes sense.
So like, if you have like, say like 50 users, you'd end up with like 100 or like 200 actual payout outputs but you know there's still 50 users so Some of them are getting multiple.

## Amount decomposition? / Payout curves.

Max Hillebrand: 00:48:32

Yeah, but by the way, we've done a lot, especially Yuval did a lot of research on this amount decomposition.
And currently, like we assume that every user knows the inputs of the users of this current round of `Coinjoin`.
And it seems that's the same case here, right?
Every user knows at least the inputs of this amount.
And then you can already make some privacy, optimized amount organization for the outputs and the payout curves.
It's like, But that benefits from having standard amounts.
So if you would have multiple standard amounts, when users choose some of them, and they choose depending on what other inputs were registered.

Nadav Cohen: 00:49:15

Yeah, and I guess in theory, you could even have, I guess maybe it's easier if everyone always has the same number of outputs, but you could even play with that as like a parameter to mess around with is you could have more outputs on like some `Oracle` outcomes as opposed to others if say you're receiving more or something like this.

Max Hillebrand: 00:49:40

I actually would guess, I'm not sure but I have an intuition that it's better for privacy if it's not sure how many exact outputs you have.
Like if there's an arbitrary, like an ambiguous room between one output or zero outputs, and I don't know, 21 outputs, whatever the maximum value is, that seems to be more private because you then don't know how many siblings each other kind.

Nadav Cohen: 00:50:03

Yeah, so you could have, I guess, payout curves that look noisy and are zero in lots of places and everyone just filters out dust outputs every time or something like this.
Or maybe there's a more sophisticated way of doing that so that you don't actually see that.

Yuval: 00:50:21

I think it's actually orthogonal.
Like if you look at the amounts themselves from purely the `Coinjoin` perspective and you're able to create enough ambiguity between the input amounts and the output amounts, I think it's immaterial what the script semantics of those outputs are.
And whether or not the funds are broken down afterward divided between two counter parties to some bet, that doesn't really matter.
All you learn is that this was split between two people but the bet itself should be like the total amount should not be really like linkable to the the inputs of both users.
Like in this scenario, you can imagine the two counterparties are kind of acting like one user.
The combined, like if you partition the transaction and look at only the subset of inputs and outputs for those two users who are transacting.
If they construct the bet amount, like the bet output amounts, in such a way that there's no way to infer that subset based on all of the like the rest of the transaction it's sufficiently ambiguous and at that point like it's not clear which inputs are going into the bet at all and and therefore it should not be linkable to the specific user.

## Net settlement.

Yuval: 00:52:19

Nadav, could you talk a bit more about the net settlement stuff that you were alluding to before?

Nadav Cohen: 00:52:27

Sure.
Yeah.
So, say, like, I am entering into, say, two `DLC`s, and I'm a little bit over-collateralized because, say there's like some cancelling out, so to speak, in my position, like I'm a bit long here, I'm a bit short here, or something like this, then if in a situation where you have kind of both of those `DLC`s going in in one place, I can essentially have my two counterparties essentially take on that bet somewhat synthetically against each other and like recover some of my own collateral.
If that makes sense.

Yuval: 00:53:17

Do those counterparties need to coordinate or are they only coordinating through you?

Nadav Cohen: 00:53:28

I guess it kind of depends on what the coordinated setup looks like for the actual mixing stuff.

Yuval: 00:53:38

Sorry I shouldn't have used that word.
Like suppose in the non-`Coinjoin` scenario you're doing this kind of thing.
Do the two counterparties that you have, do they need to communicate between them and exchange like `Adapter-Signatures` between them?
Or can they rely on you to transfer the information between them?

Nadav Cohen: 00:54:08

I see.
So yeah, if you want to do netting stuff, you actually do need kind of something like a `Coinjoin` looking thing, because essentially you need like all three parties inputs and outputs and such to be in a single transaction in order to get back your collateral so to speak.
So some amount of coordination does need to happen.
I assume that there are different ways of doing this.
Maybe Ben is more well-versed.

Ben Carman: 00:54:43

I think it'd be up to like the person that's actually benefiting from the netting to be able to figure out how to do it correctly because You know they're it's a sort of over collateralizing that they can take it out.
They'd have to negotiate that with their peers to like change the actual contract to be like to benefit them to get the less collateralized.
At least that's my understanding.
I don't know.
I think didn't Ichiro write the initial paper on it?
He's probably the best one to ask, but he's obviously not here.

Nadav Cohen: 00:55:26

Yeah, I think it's pretty much similar to what you have in mind though, Ben.
Yeah, but I guess short answer is, it's likely easiest if they are coordinating with one another, but there's likely other ways of making things more obfuscated or something.


## ## Q&A.


[EB]: 00:56:02

Okay guys, just in case, we are making questions and comments just to keep the wheel rolling, right?
But anyone can make questions.
In fact, it's good if we call this section Q&A now, right?
Because I think most of the topics are already covered.
In fact, the advanced topics are already covered.
So feel free to raise the hand.
To raise the hand.

## Can you get screwed if you lose stateful data.

Shinobi: 00:56:38

Well, I kind of missed the first 19 minutes or so, but kind of just the general topic of blurring `DLC`s and nesting them into a `Coinjoin`.
I mean, it seems like there's a lot of wins that you can have here, but it does kind of worry me that that implicitly transitions the model of a `Coinjoin` for those users to, you can get screwed or things can go wrong if you lose stateful data, as opposed to it's literally impossible for something to go wrong here.

Nadav Cohen: 00:57:16

So I think an important thing to note is there are kind of two different ways of doing this.
One of which is essentially just having a `Coinjoin` where some of the outputs are like these two of twos that are `DLC` funding outputs themselves.
And you know those two of twos once we have `Taproot` become just single Pubkeys anyway.
And if you are doing things this way, then I don't believe that parties who aren't doing `DLC`s become affected by parties that are doing `DLC`s inside of the same mix if that.

Shinobi: 00:57:52

Well, I mean, they shouldn't in either case, unless I'm missing something.
But it's just kind of like that's an implicit risk, I think, that should be like that that is deserving of like a big morning screen that like things can go wrong if you lose these transactions, you know what I mean?

Ben Carman: 00:58:12

Well, like, I'm still just have like.

Nadav Cohen: 00:58:52

Oh boy, what's happening?

Ben Carman: 00:58:57

I hope someone got an MST out of that.

Shinobi: 00:59:00

That just destroyed my brain.

## Embedded assumptions in having Coinjoin + DLC. / DLC API.

Nadav Cohen: 00:59:02

Yeah.
I guess, Shinobi, can you elaborate on how this is different from just entering into a normal `DLC` in terms of state?

Shinobi: 00:59:12

Well, I just mean, it's like, Kind of putting these two options together implicitly assumes that One piece of software is gonna be capable of both and I just feel like you know Burying a million options like that like something should be explicit about that.
You know what I mean Like there's no difference between a Nami and a `DLC`.

[EB]: 00:59:46

Max, can you fix this?
Do you think?

Max Hillebrand: 01:00:00

Yes, I just said the password.
Yeah.

[EB]: 01:00:16

You

Adam: 01:00:16

should also be able

[EB]: 01:00:18

Yep, just did.
But it comes again.

Max Hillebrand: 01:00:32

It is why we have the password.

Ben Carman: 01:00:35

Yeah.
To get back on topic.

Shinobi: 01:00:37

I love the adults in this space who want to have adult conversations about things.
There's so many of them.

Ben Carman: 01:00:47

Well, to get back to it, there's not too much difference.

Nadav Cohen: 01:00:52

Intermingling maybe, Ben, because right at the end of the day, you could have your mixing black box and your `DLC` black box, and one message needs to be passed from one to the other.
I don't look specifically the one that has the funding `TX` ID in it.
I don't think that there's much else.

Ben Carman: 01:01:14

Yeah, yeah, like All you need is for the `DLC` software is like a funding `TX` ID for everything and then that should be able to handle everything else.
So it wouldn't be a huge complexity issue or anything like that.

Shinobi: 01:01:26

Okay, so you guys are just talking like API hooking two pieces of software together, not like rolling all of this into like the Wasabi UI or anything.

Nadav Cohen: 01:01:35

That's right.
Although that's at least...

Shinobi: 01:01:38

Yeah, then that was a bad question on my part then.

Nadav Cohen: 01:01:41

Got you.
No worries.
But for the N of N mix, then that's kind of its own custom thing but that kind of assumes that everyone involved is doing specific `DLC` stuff.
Yeah, where you're registering two of two outputs, hopefully you can and in the future, you know, just single pubkey outputs.
Then essentially what you'll do is you'll have like a callback where when you get the thing you need to sign before you sign the actual like funding or the mixing transaction, you like go make a call out to the `DLC` API, do all that stuff and then come back and do this last.

Shinobi: 01:02:19

Okay.	
All right, that makes sense then.
I guess ignore Shinobi's bike shedding troll concerns.

## Optimisations for arbitrary amount settlements. / Contract Execution Transactions. / Rounding. / O(lg n) signatures for n outcomes. / Verifiable encryption.

Max Hillebrand: 01:02:46

Maybe a question on some different regard that we did not talk about.
How about optimizations that you used for these arbitrary amounts price settlements?
Can you maybe speak a bit more?

Nadav Cohen: 01:02:59

Sure.
Yeah, so generally speaking, you know, if you're thinking about `DLC`s as like a black box, you think about like there's some set of outcomes, you create a transaction for each of those outcomes that pays out however it's supposed to for that outcome.
And then you generate `Adapter-Signatures`.
But this works great for most betting.
But if you're, say, Doing something where the outcome is a number or you know, there's just a ton of outcomes and they're structured Then you have Kind of this problem, oh! a couple different problems, but mainly the problem is that you have like let's say a hundred thousand possible outcomes or something like this when maybe especially usually it's the case that you only really care about some small subset of those.
And if it's anything above a certain number or below a certain number, then you just have some edge case like, OK, this person gets all the money or something like this.
So what we do is we have the `Oracle`s, numeric `Oracle`s specifically, sign each binary digit, each bit of the outcome individually.
And then we can essentially construct outcomes using digit prefixes instead of the entire list of digits.
So instead of requiring that there's a separate outcome, so to speak, or it's a different outcome for every different number.
You can have, for example, if you ignore the last digit and you just look at all of the digit prefix up to the last digit, then you can have an outcome that corresponds to two possible numbers.
And then if you ignore two digits, that's four possible numbers and so on.
And so you can essentially, for example, say if everything above 100K is just like the same outcome, basically, then what you can do is you can decompose that very very large interval into only logarithmically many CETs essentially, or contract execution transactions.
And so, and then furthermore, we introduced some amount of rounding.
So this is like negotiated, both parties are okay with the amount of rounding that happens And you essentially say round to the nearest hundred Satoshis or the nearest thousand Satoshis or something like this.
And then by doing that you can get more kind of flat pieces which can be compressed by the same mechanism until logarithmically many, you know, `Adapter-Signatures` that you need.
And so in practice what this means is that even relatively complicated, you know, financial contracts on numeric outcomes on prices end up with only, say, a couple thousand `Adapter-Signatures` or cases that you've decomposed it into, rather than having to cover like all 100, 200,000.
And then furthermore, for 'Multi-Oracle' stuff, there's also some fanciness that we do, where essentially you do something similar, where agreement between two `Oracle`s is essentially constitutes like you take one of these digit prefixes from one `Oracle`, and then you construct a digit prefix for the second `Oracle` that covers that same, or what the first `Oracle` said, with, say, some allowed amount of error.
So we even cover cases where you have multiple `Oracle`s and they don't sign exactly the same thing.
They can be like some amount off.
Say if you're for example using like Kraken and Bitfinex and Gemini or something like that as three price `Oracle`s, then you can have it so that so long as any two of them are within $128 of the same BTC USD price or something like this then your contract will execute.
So yeah all sorts of fanciness and stuff happening there And there's some more optimizations that I'm working on that maybe use some like verifiable encryption and stuff like that to try and get the scaling for adding new `Oracle`s down to something more reasonable.
Yeah, I'd be happy to talk more about it of course, but at this point I'm probably just rambling unless someone has questions.

## Can optimisations for DLCs be used to optimise Coinjoins?

Max Hillebrand: 01:08:41

I'm just curious.
Do you think that this is, in any, at all interesting research useful for conjoins?

Nadav Cohen: 01:08:48

Can you say that one more time?

Max Hillebrand: 01:08:51

Do you think that there is some nice similar ideas that we can use to optimize for `Conjoin`s?
In the non-`DLC` case, I mean.
Or is it just complete different research?

Nadav Cohen: 01:09:03

I would think if there is any overlap, it would be in kind of the coordination of the outputs and such.
Because we have some pretty succinct coordination between the two parties on, you know, essentially like the contingent like, you know, if the `Oracle` says any of these things then here are my outputs in all of those cases.
So we have like these nice compressed, essentially like seeds from which you, or you know, contracts from which you derive all of the transaction information.
But I guess for a regular `Coinjoin` you just have one transaction so maybe that's not a big problem.

Ben Carman: 01:09:48

Yeah I think where the most overlap is is honestly like on the Off-Chain side where you're finding counterparties like we've like looked into like different ways we could, you know, have a place to find like a counterparty for the bets you want to make.
And like you could do like, you know, you just have like a central place, like somewhere like a Wasabi coordinator, or you could have something where it's like, join market where it's like, you know, a kind of decentralized kind of thing where you're finding there's no like coordinator to find you counterparties.
So it's, it's a different way to do it.
And we haven't really, there's probably gonna be multiple different ways to do it similar to how the `Coinjoin` landscape is today.
So I think that'll be probably the place where there's the most overlap.

Max Hillebrand: 01:10:36

Yeah, I think the amount of organization might be interesting for you guys.
Like, based on the inputs of other users, how can we optimize the outputs of us?
So to gain more privacy, I think this is like non `Coinjoin` cryptography related things that might be interesting for you.

Nadav Cohen: 01:11:00

Yeah and I guess also you know if we are doing some kind of `DLC` mixing stuff in the future, then also the amount decomposition things might be some overlap there.

## Consensus on fee priority. / Child-pays-for-parent for DLCs. / Replace-by-fee not possible for large Coinjoins or DLCs. / Free credentials.

Max Hillebrand: 01:11:25

One maybe relating question, how do you get consensus on the fee priority for this transaction?

Nadav Cohen: 01:11:35

So currently this is done via, essentially, you know, you can choose whether or not to accept a certain fee rate, But afterwards everything is fee bumpable using child pays for parent where the child is replaced by fee enabled.
So it's yeah.
I guess there's always the, you know, lots of complex ways to handle these kinds of things.
I think right now the dual-funded Lightning Channel proposal just has like the initiator pay all the fees because it's simpler.
But we decided to kind of split the fees between the two parties and then for the fee rate that's in like say the offer message.
And then everything beyond that is done just by fee bumping.
Yeah.

Max Hillebrand: 01:12:36

Yeah, two notes here.
I mean, for somewhat obvious reasons, `RBF` is not possible in large `Coinjoin`s or not reasonable to do because you have to resign, everyone has to resign.

Nadav Cohen: 01:12:45

That's right.
And for `DLC`s, it's not possible either.
It's only the child.
And the child pays for parents.
So like, if you spend your change, then the thing you're using to spend your change is what you would `RBF` with.

Max Hillebrand: 01:12:58

Yeah, yeah, that's smart actually.
But the issue here still is with the size of the `Coinjoin`.
You have to child pay for parent, the entire fee for the `Coinjoin`.

Shinobi: 01:13:09

Well, Max, you could do that out of the change input or output that Wasabi is getting fees in.
Once you implement fee credentials, that could potentially be a thing where users pay for that, air quotes, with the fee credentials, but it's just that single output Wasabi got the mixed fees with that could actually do the `RBF` child-pays-for-parent hybrid if a `Coinjoin` stalling in the mempool?

Max Hillebrand: 01:13:40

Yes, maybe.
Yeah, actually, maybe.
And users can pay at any time, maybe every hour, Wasabi will do an `RBF` of the child to fee bump.
And if there was no fee bumping, free credential being sent in that hour, then it also doesn't do the `RBF`.
Yeah, actually.

Shinobi: 01:14:07

And that would be totally open for any user.
It's not like everybody has to chip in or split it up.
It's just like, if I'm super impatient, take my fee credentials, make that happen faster.

Max Hillebrand: 01:14:24

Plus the user doesn't have to spend his own chain coin right which would reveal his high time preference fingerprints while instead if the coordinator spends his fee output with the `RBF` thing, then we only know that some user in this `Coinjoin` have the high time preference and paid for the fee bunk, but we don't know which one it was.

Yuval: 01:14:44

I don't think that would work because you would need to provide like all of the `RBF` scenarios of which there will be exponentially many in the size of the transaction for every single users.
Like every ordering of users choosing to bump fees should subtract some different amount and then all of those outcomes have to be pre-signed except for...

Shinobi: 01:15:10

Why though?

Max Hillebrand: 01:15:11

I don't know.

Shinobi: 01:15:13

We're not talking about the `Coinjoin` transaction itself.
We're talking about a child transaction with the fee output.

Yuval: 01:15:21

Oh! forget what I said.

Shinobi: 01:15:23

But so it's like that should.

Max Hillebrand: 01:15:24

Yeah It's actually a smart way to do it.

Shinobi: 01:15:27

Yeah that would be super private.
That would allow any user to accelerate the `Coinjoin` without any privacy damage on their part and then three, like that could go to the extreme that wasabi literally burns that entire fee income for that round in two fees, but they're not going to do it unless they redeem tokens and then have the right to spend some reserved `UTXO`s on themselves so that like that's a complete privacy win and should totally balance out on Wasabi’s hunt.

Max Hillebrand: 01:16:00

Yep, because we already got the Bitcoin earlier.
And by the way, maybe even users who are not part of this `Coinjoin` can issue a fee bump.
Because as long as you have fee credentials, Any user can pay it.

Shinobi: 01:16:25

Nadav, you are a whiz kid that inspires genius ideas everywhere you go.

Nadav Cohen: 01:16:30

To be fair, I credit Antoine Riard with all of the fee bumping stuff.
I just read his spec and gave it a review.

Shinobi: 01:16:39

You still inspired something here because you are a Wizkid.

Max Hillebrand: 01:16:50

Yeah, but again, the statement still holds, right?

## Aggregated fee-bumping. / Efficient fee estimation. / Free riders contained within 1 transaction.

Max Hillebrand: 01:16:53

One user has to pay to fee bump the transaction of every user.
And so your SAT per vbyte  is gonna be very small.
But your nominal amount of SAT is still going to be quite large, if you want to make a meaningful difference.

Nadav Cohen: 01:17:09

Yeah, though you could also kind of view it as some kind of crowdfunding for fees scenario, where it'll go through.
Maybe that's not a good analogy, because you also are.
You want these.
There's important things in these, and different people will have different preferences.
But you know in theory you could have multiple people doing fee bumping and the fee bumping would all then kind of get aggregated.
Yeah, some people can always be kind of free riders in that scenario if they don't have too much at stake.

Max Hillebrand: 01:17:48

Yeah, but the nice thing is that the free riders are contained within one transaction, because the alternative approach to efficient fee estimation is what we used before in Wasabi 1.0, but that is not turned off, is to make child pays for parent of unconfirmed `Coinjoin` rounds.
So to allow unconfirmed coins of a `Coinjoin` outputs to remix.
And the coordinator slightly increased each round's fee a little bit, which was efficient to get all `Coinjoin`s confirmed reasonably quickly, reasonably cheap.
But the downside was that if you were the first participant in the first round of `Coinjoin`, like the parents transaction, the first unconfirmed, then you paid very little fees, While you were like at the end of the chain number 15 or something, your fee rate got higher and you don't even get faster confirmation for that because you carry like 14 parents that you still have to confirm.

Nadav Cohen: 01:18:46

Gotcha.

Max Hillebrand: 01:18:48

So with this approach, at least this free value problem stays within one transaction.
And I guess that's as small as it can get.

Shinobi: 01:19:04

I mean, that's perfect though, because that just removes all of the dependency limits in the mempool except for remixing, right?
Because each thing would be its own parallel child pays for parent.
That's what you're saying, right?

Max Hillebrand: 01:19:21

Yeah, exactly.
Each coin is, sorry, each `Coinjoin` transaction is one unconfirmed transaction.
And because the coordinator requires that all inputs to the `Coinjoin` have been confirmed already.
This means that no coin from the unconfirmed `Coinjoin` transaction can be registered in a new `Coinjoin` transaction, and therefore we don't have child pays for parent chains.
Go ahead, Adam. Sorry.

## Perverse incentives for individual users in Wasabi Coinjoins. / Incentivise pro-privacy behaviour. / UTXO days destroyed. / Fidelity bonds in JoinMarket. / Mining fees. / Coordinator fees.

Adam: 01:20:04

I did have a question, but it's a bit different topic.
Is that okay?

Max Hillebrand: 01:20:10

Sure, go ahead.

Adam: 01:20:15

So, I was thinking about the `CBL` things some of you might have seen on Twitter.
And I believe I got to the end of how far I can think about that and I properly went through the issue but it would be really nice if to hear what you guys think about that.
So the start is that there is a perverse incentive for the perverse incentive for the `Coinjoin` fees with the current Wasabi, which is that the more user the `Coinjoin` have, the exponentially more fee is being paid out by the `Coinjoin` rounds, if I'm correct, and there is a perverse incentive for the coordinator to add their own users.
So what do you guys think about this?
And I will not say what I think, just see if we get to the similar conclusions or not.

Yuval: 01:21:39

Do you mean in the context of `DLC`s or `Coinjoin`s in general?

Adam: 01:21:45

No, with current Wasabi `Coinjoin`s, the coordinate fee structure.

Yuval: 01:21:53

I agree 100%.
I think it's a problem and especially In combination with the discount, there's additional perverse incentives for individual users to register specific outputs.
And that can be combined to make sibling by somebody other than the coordinator also are a little bit cheaper.
So it's not just the coordinator.
I think it's perfectly possible to address it.
Like this is why I've been proposing a flat rate, some percentage of mining fee, perhaps, and on top of that, doing some sort of discount model for encouraging pro-privacy behavior.
So for example, bringing in an older input, something which destroys a large number of coin days, this is kind of like fidelity bonds and join market.
Like, you know that that input has not been sibling any of the rounds that were concurrent with this output not being spent, like after it was confirmed this could not have been used, this liquidity could not have been used to `CBL`other rounds.
So it's good to incentivize that kind of behavior as well.

Adam: 01:23:26

All right, so is it a perverse fee incentive?
Yes.
Let's keep it simple and only talk about the coordinator for now.
Does anyone not agree with this or we can move on and everyone agrees?

Shinobi: 01:23:44

With the coordinator, I mean, that's a special unique case because anything that they could do is free.
And that's like the whole problem with the fee schedule and sibling.
You have to balance between on one end, it being so cheap that you can sibble all day long, and on the other end, it being so expensive that people aren't going to remix, which is one of the most important properties of a system like this.
So it's like, If you're talking the fee schedule, I mean, I wouldn't talk about perverse incentives.
I would be talking about where is that middle spot where you accomplish both of those things.
It's not too expensive for people to be remixing, But it's not so cheap that you can just flood the system with liquidity and sibling.

Adam: 01:24:38

We'll get to that because I mean, yeah, sorry, Max, go ahead.

Yuval: 01:24:45

If I may just quickly, an important distinction here is mining fees and coordinator fees are very separate.
So Shinobi, your point stands when coordinator fees dominate over mining fees, but not vice versa.

Shinobi: 01:25:01

Touche.

Max Hillebrand: 01:25:05

Yeah and one other quick thing is that this cheaper remixing for high quality coins, especially when we add a timeout benefit, right, so `UTXO` days destroyed, if that count is high then you get a cheaper coordination or mining fee.
This has similar denial of service protections as Fidelity bonds, though I would say weaker because Fidelity's bonds, you actually cannot spend the coin in this lock-up period, while with this type you could have spent the coin, but because you did not spend it, you get cheaper fees.
So it still improves denials, or increases denial of service costs, just in opportunity costs of not spending these coins.

Shinobi: 01:25:50

Yeah, I mean, I think that's a perfect way to balance that.

## CBL incentives. / Fees for every mix round disincentivise CBL attacks. / Samurai Whirlpool incentives.

Adam: 01:25:57

All right so this is a fair birth incentive.
There is no question about this.
Now, is it a `CBL` incentive?
And I actually did not, I was not able to come to the end of this question.
My conclusion was maybe, but you know what a `CBL` is when most of the participants are actually one entity, right?
So the question is, would this lead to such a situation where most of the participants are one entity?
Is this incentivizes that much so that would happen?
You know what I mean?

Shinobi: 01:26:52

Well, I mean, aside from the coordinator, I don't see how that could be the case if you're paying fees every time.
And I mean If the coordinator wants to `CBL` their mixing pool, all they have to pay is mining fees.
Everything else is free.
But with anybody else, if you're paying fees for every mix round, I don't see how that encourages it.
That's a disincentive.
That's one problem I have with Samurai is their fee schedule incentivizes lots and lots of remixing, but the fact that you only pay once and everything else is free, I could just buy a new `UTXO` on Cash App every day and feed that into `Whirlpool` and just let that `CBL` all day for free.

Ben Carman: 01:27:42

That's something you do to like prevent the coordinator from having like the ability to `CBL` by just only paying mining fees, to just have like half or like a third of the actual coordinator fee just be sent to an operator and burn, or to have it donated to HRF or some fund?

Shinobi: 01:28:05

Well, that's kind of what I think like nothing much was getting at with modeling the mixing fees off of the mining fees so that's that's always balanced the correct way there.
You can correct me if I'm wrong, nothing much.

Yuval: 01:28:21

Yeah, like you could make the flat, the sorry, the coordinator fees either be completely flat, so like some percentage of the amount, regardless of how many other inputs and outputs are in the transaction, regardless of how much liquidity is in the transaction.
That could be like a linear function of the amount or the weight.
And if you make it just a linear function of the weight, well then, you know, it's proportional to the mining fees.
It doesn't really matter like which of these specific scenarios, and it could be like a constant function not necessarily a linear function.

## Where is the equilibrium for coordinator fees? / Linear function of fee rate.

Adam: 01:29:02

All right, all right.
So I didn't fully fleshed out, but I think somehow the, because if you think about it, if there are 99 real users, then it makes sense for the coordinator to join in, to be the hundred one, because 99 people will be paid after another peer, 0.003%, right?
So it makes sense if you're thinking about the big numbers, because then you will get 99,0003%.
But if you're thinking about the small numbers, one, if there is only one user, does it work for the coordinator to get into the round?
And the answer is it doesn't because that's only 1 times 0, 0, 0, 3 percent, and the coordinator will pay more mining fees than how much it would gain fees from that person.
So I think the question here, where is the equilibrium where the Bitcoin fees?
You know. yeah.

Yuval: 01:30:21

the intercept is where I think it's roughly like 20,000 Satoshi's on average in coordinator fees for like a I may be misremembering, but like 0.1 times the number of users times 0.003 I think percent, sorry, so another two zeros.
But like you can calculate the expected value for the coordinator from like or not even expected just the value for the coordinator for that additional user and if the marginal cost in terms of the current mining fees of adding a single input and registering another fake zero point one output is less than that, then there's a clear incentive for the coordinator to do that.
So it's it's just a function of the current fee rate for the transaction.
And because, I mean, you could do this repeatedly, so long as the cost of an additional input and output is less than the figure without multiplying by the number of users, because the total amount paid by the user, that usually sums to several tens of thousands of Satoshis, as long as that increment is greater than the marginal cost of an additional fake user, well, that's a linear function.
So it's the same regardless of how many inputs and outputs were already added.

Adam: 01:31:58

OK, so what's interesting here is that it might seem like there is a severe issue, but it doesn't because it definitely doesn't make sense for one people, two people, three people, five people, ten people, maybe at ten people it starts to make sense for the coordinator.
But you know, there is a line somewhere where it starts to make sense.
And so it doesn't mean that the coordinator is incentivized to take 99 of the existing users or something like that.
It just means even the coordinator participates with more users, it pays more mining fees.
You know what I mean?
Like there must be a line there where it starts to make sense, but maybe it's at 50 people.
I don't know, right?

Yuval: 01:32:55

It's a function of the fee rate.
So at one Satoshi per byte and let's say 100 bytes per fake user, let's say it costs 100 Satoshis to pay the mining fees for another `CBL` user, if you can extract more than 100 Satoshis and coordinator fees from the target user or users, right?
So like the more users you're targeting, the less powerful your `CBL` attack is for de-anonymization, but the more fees you can extract out of those victims.
So there's just a tipping point there, right?
It's just the intercept of two lines.
And it's.

Adam: 01:33:38

Yeah, exactly, exactly, right?
But I'm actually gonna create a graph where you listening this episode, but this means it's not a `CBL` incentive, at least not in the sense that people are using it to be, right?
Because there is no incentive to do it for smaller number of users.
So not the number of users as you're saying it, sure.
But anyway, you know what I mean.
It's not a `CBL` incentive, nothing the `CBL` incentive that where the coordinator is incentivized to be anonymize everyone.
No, it's very far from the case actually.

[R]: 01:34:23

It's a free ride incentive.

Yuval: 01:34:27

Well, no, it's worse than a free ride incentive because the coordinator actually increases its revenue if it does this.
But even if the tipping point, whether or not it makes sense for a `CBL` attack or only for extracting additional fees, that entirely depends on whether or not the mining fee rate is low enough.
And if the minimum rate is like one Satoshi per byte, that's actually not that high.
I think it's usually much higher than that.
I think it's on average more like 10 or 20 at the lowest rate.
So that implies that, yes, Adam, you're correct.
It's not really a direct incentive because an additional fake user would not, the cost would not be covered by the additional fees of just a single user.

## Are there any other incentives for CBL?

Adam: 01:35:26

All right, so now it's worth asking the question that, You know, here is a weak `CBL` incentive or a strange `CBL` incentive, but, you know, there are these incentives for `CBL`.
What do you guys think?
Can you identify some?
So, obviously, it is reputation, the largest `CBL` incentive.
And it is also noticeable when you start to do that.
Do you guys see why?
So for example, we can tell with the current Wasabi that there is no `CBL` happening, or at least not this kind of `CBL`.
Why?
It's because we have 10,000 Bitcoin monthly volume, and the direct way, the known noticeable way to `CBL` it would be if we would be most of the participants of that of the 10,000 bitcoin if we would be bringing in that fresh those are fresh bitcoins not the actual `Coinjoin` volume That's 40,000 But the fresh bitcoins monthly is 10,000.
So in order to `CBL`, unnoticeably, we would have to have like 9,000 Bitcoin or something crazy like that.
But if we would have 5,000 Bitcoin, then the last thing that we would care about is the perverse fees incentive, which at best, it's a couple of bitcoins, not 5,000.
You know what I mean?
It wouldn't make sense in that case.
Do you guys agree or disagree with that?

Yuval: 01:37:32

Mostly agree.
I think it's, you know, you need to actually crunch the numbers and figure out like at fee rate X, this is how much liquidity you would need to create a fake graph of this size in order to make, you know, hide the liquidity.
And you can reduce it to, like, what is the liquidity requirement and what is the marginal cost or profit for the coordinator to do, like, an additional round and parameterize that by how many real users are in the round.

Adam: 01:38:08

We could also execute, okay, let's say we agree, then I say that I wasn't completely correct there because we could also execute a similar attack from less money, you know, from remixing.
Actually, I think that's what you were referring to by liquidity, right?

Yuval: 01:38:28

Yeah.

Adam: 01:38:29

I guess the confirmation or something like that.
Yeah.

Yuval: 01:38:34

It's not just that, it's also like how much in mining fees are you paying to create like a fake graph that does not look like remixing, which is like that's a distinction between fresh and remixed coins, right?

Adam: 01:38:51

Okay.
So, but we also know that, you know, because this what, what the `CBL` would lead to in this case, if we don't have, don't have, if we are not matching the users' money with our own money, with multiplies of the users' money, we would have to have that much.
Then If that's happening, then we would see a very high number of remixes, and it's only 20 to 30%.
So that's not, That actually proves that there is no, This kind of `CBL` which may or may not be `CBL` happening.
Does that make sense?
Is there anything wrong with that?

Yuval: 01:39:43

No, I think that's correct, but I mean you need to take into account the possibility that you mix coins and then you create some sort of fake spending graph and eventually you cycle that back into the mix with, you know, a bunch of fake transactions in between which also costs you mining fees, probably a lot more than the mining fees for the `Coinjoin`, in order to simulate fresh bitcoins that are actually just getting recycled by the coordinator.
That incurs a significant cost and I think it's, you know, If you look at the topology of the actual graph on the blockchain, it should be fairly straightforward to estimate that cost or even just measure it.

Max Hillebrand: 01:40:26

Yeah, but for what it's worth, the dumplings repo only uses one, like you can fool the dumpling repository into thinking it's fresh Bitcoin by just making one transaction.
So fresh Bitcoins are only the actual outputs of the `Coinjoin`s, being inputs of the next `Coinjoin`.
But if there's even one half of a single user transaction in there, it's not considered fresh anymore.
Or, sorry, it is considered fresh.

Yuval: 01:40:52

Yes, and I mean, that, if you are thinking adversarially, then the coordinator probably anticipated that and created, you know, anticipated the scenario where the dumplings repository was updated to take that into account, etc, etc.
You can still reduce that to a cost in mining fees at the bottom line.

Adam: 01:41:20

So anyway, just to sum up, so is it a perverse incentive?
Yes.
Is it a `CBL` incentive?
Not really.
Not in the sense where people are using it, because maybe it would be a big `CBL` incentive, something like that, but not even in the technical sense, because in the technical sense the majority of the users should be controlling the volume.
And is there a `CBL`?
No, there is no `CBL` because it's noticeable, which is a disincentive.
And the final question is that why did we not change that?
It's because, you know, the fee structure is actually pretty fair, because you gain more privacy, you pay more, but that's not the real reason.
The real reason is because the fee structure is not something that, you know, that's the first agreement you have with all your users.
And if you are unilaterally just changing it without a very good reason like wasabi 2.0 which needs change anyway because of the protocol then you know like you're not changing around with the most fundamental parameters

Adam: 01:43:12

That's good music by the way.

[R]: 01:43:21

What music?
I can see someone is sharing their screen again.

Adam: 01:43:33

Yeah, but guys, can you kick him out?

Max Hillebrand: 01:43:38

Trying but doesn't work.

[R]: 01:43:42

Yeah, we need to use a private Jitsi.

Adam: 01:43:47

Then maybe just let the music go for a while and then the live stream.
That would be a nice ending.

[R]: 01:43:58

Yeah.
Yeah, maybe we should end the stream now.

## Closing thoughts.

Adam: 01:44:03

Wasabi research club got hacked.
Tomorrow headlines.
Wasabi wallet got hacked.

Shinobi: 01:44:15

Can't have fun.
Can't be an adult because stupid children.

Adam: 01:44:34

All right, thank you.

Max Hillebrand: 01:44:38

Any closing thoughts that Ben or Nadav want to bring up?

Yuval: 01:44:46

We should set up `DLC` contracts for whether or not there's a `CBL` attack on Wasabi.

Ben Carman: 01:44:52

There we go.
I was going to say thanks for having us, this was fun.
Always down to talk to you guys.
Yeah, thanks.

Yuval: 01:45:03

Thanks for coming.

Adam: 01:45:10

Thank you guys.
It was really, really, you know, just thinking back when we started the Wasabi Research Club as exactly Not exactly more than one year ago then we were just gonna have have some fun reviewing all the privacy papers and putting them on YouTube and hoping that the authors of the privacy paper appear because this is publicity for them and then we can pick their brains and ask our questions and you know, that was fun and then for a long time it was just us basically thinking about all kinds of privacy things.
And it looks like you guys are taking this to a completely new level.
So, I mean, it's really, really awesome to see.
So, congrats for this.

Ben Carman: 01:46:18

Yeah, I mean, you guys are doing awesome here.
I remember when I was in college, just watching all your, like the Snicker one and the, oh dear, and all the different mix net ones that are really interesting.
And yeah, it's crazy what you guys are building now.
It's completely awesome.

Max Hillebrand: 01:46:42

Yeah, and I really like how it's all coming together.
Like I can totally see what we saw, the `Coinjoin`s that open and close `DLC` contracts or lightning channels that then open and close `DLC` contracts.
That's going to be a wild wild world.

[R]: 01:46:57

Yeah, guys, we have again someone sharing their screen.
But yeah, let's end the stream and yeah, I think this was a good episode.

Adam: 01:47:10

You know, I'm listening to this music like three times a day, super simple songs.
My son really loves it.

[R]: 01:47:21

I can't even hear the song, but yeah.