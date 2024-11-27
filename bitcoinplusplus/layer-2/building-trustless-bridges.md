---
title: Building Trustless Bridges
transcript_by: markon1-a via review.btctranscripts.com
media: https://www.youtube.com/watch?v=M40yzuv6DNY
tags:
  - scalability
  - sidechains
  - statechains
speakers:
  - John Light
date: 2023-04-29
summary: Many mechanisms have been created that enable users to lock BTC on the mainchain, transfer a claim on the BTC in some offchain system, and then later redeem the claim and take ownership of the underlying BTC. Colloquially known as "bridges", these mechanisms offer a diverse range of security and usability properties for users to choose from depending on their risk tolerance and cost preferences. This talk will give an overview of the different types of BTC bridges that exist, how they work, and how they can be improved.
---
Thank you all for coming to my talk.
As is titled, I'll be talking about how we can build trustless bridges for Bitcoin.
So my name is John Light.
I'm working on a project called Sovryn.
We actually utilize a bridge, the Rootstock Powpeg Bridge, because our project was built on a Rootstock side chain.
And we're interested in how we can improve the quality of that bridge.
Currently it's a federated bridge, we would like to upgrade to a trustless bridge.
And this talk will describe one way that we can build a trustless bridge.

## What is a Bitcoin bridge

So just to kind of introduce this concept, what is a Bitcoin bridge?
So a Bitcoin bridge is a system that enables users to lock sats on the Bitcoin mainchain and then receive an equivalent amount of IOUs for sats on some destination system.
And then, perhaps most importantly, it enables the user to burn the IOUs on the destination system in exchange for an equivalent amount of sats on the mainchain.
This is also referred to in the literature as a two-way peg, but nowadays most people call these bridges.
So the destination system could be blockchains, it could be tangles or hashgraphs, fedimints, state channel networks, centralized or federated databases, really any kind of system for transferring BTC or sats, however you prefer.
So at a very high level, the bridging process works like this.
A user will take some sats, they will lock some sats in a address on the mainchain.
There's a bridge system that does some stuff.
And then on the destination system, they'll get issued an IOU for an equivalent amount of sats, and then they can use those sats in the destination system.
So that's the deposit process.
And then a withdrawal works the same way in reverse.
So the user is going to burn some sats on the IOUs on the destination system.
The bridge is going to do some stuff, and then the user will get some sats unlocked and sent to their mainchain address.
"The bridge does some stuff" is really where all of the differences between the different bridge designs comes into play and I'll describe what that landscape of the design space looks like currently.

But first I want to talk about why are we even doing this?
Why would users give up control of their sats to a bridge?
So the first reason is we want to increase transaction throughput.
So Hal Finney said back in the day that Bitcoin itself cannot scale to have every single financial transaction in the world.
There needs to be a secondary level of payment system, which is lighter weight and more efficient.
And so a bridge is like how you get sats into this secondary level that is lighter weight and more efficient.
Hal's intuition there was backed up by empirical data through numerous studies, one of which was created and published by the mining group bitc.
It's a few years out of date by now, but the basic principle still applies.
They showed that if you increase the block size to 8 megabytes, then within 6 months, like 95% of the nodes are going to get knocked off the network just because they're not powerful enough to keep up with such a large block size limit.
Like I said, this is several years out of date now.
The situation has probably been improved, but the basic idea still holds.
As you increase the block size limit, it becomes more difficult for nodes on the network to keep up unless they are also increasing their computing power at a similar rate, which of course increases the cost, which knocks some people out who just can't afford those increased costs.
So it increases centralization.
The other motivating factor is we want to be able to add new functionality to Bitcoin.

## Why create a bitcoin bridge?

So everyone knows, or at least people who are familiar with Bitcoin's Script know that it's kind of limited in its capabilities.
There are only a few primitives that you can combine together to create Bitcoin smart contracts.
People have come up with all kinds of new ideas of things that we could do with blockchains, other than what is already possible with Bitcoin today.
Satoshi Nakamoto referenced this when he was talking about this idea called BitDNS, which is like a precursor to Namecoin.
He said, piling every proof-of-work quorum system in the world into one data set doesn't scale.
Bitcoin and BitDNS can be used separately.
Users shouldn't have to download all or both, use one or the other.
BitDNS users may not want to download everything the next several unrelated networks decide to pile in either.
So he's basically referring to this tension between having a blockchain that has limited expressivity that maybe only supports one or a few small numbers of applications, and then a blockchain that has full expressivity that you can pile all of these different types of applications into a single blockchain.
Do we really want that or do we want to try to firewall these things and have it separation of concerns so that users who are only interested in one application can use one system, and then users who are interested in another application can use some other systems.
So we want solutions to this problem that don't harm the decentralization and the security of the Bitcoin mainchain.
And so we've come up with this idea of bridges so that we can increase transaction throughput and add new functionality by transferring sats to other systems, and those other systems take on the burden of increasing transaction throughput or adding new functionality.

So one way that you could solve this problem is just by piling all of this stuff into the Bitcoin mainchain so we could have more transactions per block, more blocks per day, more expressivity, more everything.
But your Raspberry Pi node is not going to be very happy about that.
And eventually, as the BitFury study shows, it'll just get kicked off of the network.
And that is bad for Bitcoin decentralization security, so it doesn't really meet our requirements that we defined in the previous slide.
So what we've done instead is we come up with this way to have the Bitcoin mainchain and then some destination system.
And we have this bridge that connects the two so that you can move sats back and forth.
Then you have your Raspberry Pi nodes that are like validating the Bitcoin mainchain.
They're super happy because the block size limit can stay small and Bitcoin Script stays very simple so they can easily verify Bitcoin transactions.
And then on the destination system, we don't really care what kind of nodes run the destination system if users want to opt into a destination system where they have to have you know some beefy server thing then you know that's fine like they're free to do that.
But the mainchain users are unaffected.

## Categorizing bridges

So let's talk about the different types of bridges that exist or could exist.
But before we do, I want to take a little semantics detour.
There are a couple of jargony terms that I'm going to use in this talk.

### What do we mean by "trustless"?

One I've already referenced in the title of the talk, which is trustless.
So what do we mean by trustless?
I'm going to define trustless as saying that a bridge is trustless if it does not introduce any new trust assumptions compared to holding and transacting or using sats on the Bitcoin mainchain.
And so therefore a trusted bridge is a bridge that introduces one or more new trust assumptions.
I know that there's not currently like a total consensus on what the definition of trustless is, but I think that in this context, I think this is a reasonable definition.
So just keep that definition in mind when I use that term throughout this talk.

### What do we mean by "Layer 2"?

I'm also going to use the phrase Layer 2 because this is a conference about Layer 2s.
So I want to be clear about what I mean when I say Layer 2.
There are a few definitions that have been proposed for Layer 2.
Georgios Konstantopoulos says, "What makes a Layer 2 special is when Layer 2 security is equal to Layer 1 security".
So he's basically saying Layer 2 is an off-chain system that has ownership security and double spend resistance equal to the mainchain.
This definition isn't very satisfying to me.
He actually contradicts himself in his tweet.
So he says Layer 2 security is equal to Layer 1 security, but then he says, that it would include a system where you play a fixed duration game where honest players are guaranteed to win, but that's not how Layer 1 works.
There's no fixed duration game when you're holding funds on Layer 1.
So yeah, this kind of is not an internally consistent definition, so I reject it.

Muneeb Ali from the Stacks project has proposed the definition where he basically says Layer 2 is an off-chain system that gets full double-spend resistance from the mainchain.
This definition is also not very satisfying because it would actually exclude Lightning, which I think is weird.
It also doesn't completely accurately describe his system Stacks because after the Nakamoto release Stacks will only get full security after, I think, 100 blocks.
So there's like a caveat there like okay, eventually you get like full double spend resistance from the mainchain.
But anyways, just because it excludes Lightning it just doesn't seem very satisfying to me, so I also reject that definition.

Then there's this third definition where Layer 2 is any off-chain sats transfer system.
And there are lots of people who express this kind of viewpoint.
Notgrubles on Twitter says, "lightning, fedimint, and liquid are all Layer 2s".
This guy, matt.bit, says "Coinbase is a Layer 2".
Calle from Cashew says, "Opendime is Layer 2".
Instagibbs says "Altcoins are Layer 2".
Of all the definitions I've mentioned so far, this is probably my favorite because at least is consistent.
You can say, "okay, any off-chain transfer system is a Layer 2", but it still just doesn't feel very satisfying to me to say like Coinbase is Layer 2 or Opendime is Layer 2.

So I'm introducing a new definition, which is: A bridge is a Layer 2 bridge, if users can unilaterally redeem their IOUs, like on the destination system, for mainchain sats. That means they don't require any cooperation from any third parties to get their sats out of the system.
And then this redemption process is actually enforced by the mainchain consensus rules.

Therefore, a "non-Layer 2" bridge is a bridge that does not let users unilaterally redeem their IOUs for mainchain sats, you need some sort of cooperation with a third party to get your money out of the system.

So that's the terminology that I'll be using.
And so I've laid out this quadrant (refers to slides).
On the top, systems on the top half are systems where some third parties can steal user funds.
Systems on the bottom half are systems where third parties cannot steal user funds.
Systems on the left hand, I'm calling not Layer 2 systems because third parties can freeze funds, meaning that users cannot actually get their funds out of the system.
And then the systems on the right are all going to be Layer 2 systems because third parties cannot freeze user funds.
Users can always make a transaction on the mainchain to get their money out of the bridge.

## Centralized custodian

So the first type of bridge is the classic centralized custodian.
An example of this would be like WBTC on Ethereum or even your centralized exchanges like Mt. Gox or Silk Road or something like that.
So the centralized custodian fully controls the bridge.
They usually just give the users an address, users send their sats to the address, they get an equivalent amount of IOUs like in the custodian's database.
In the case of WBTC, it's like a token on a different blockchain.
But the users trust the centralized custodian absolutely with the security of their funds.
So centralized custodians aren't all bad.
They have some benefits.
They're cheap.
They have really high throughput.
You can have a totally custom execution environment for how you can manipulate your IOUs and transfer them between users.
But of course, they have the obvious downsides of there's a single point of failure.
The compromised custodians can freeze and steal user funds.
There's no kind of internal incentive system keeping them honest, like you just rely on the legal system or reputation or something.
And the users cannot unilaterally redeem their IOUs for Bitcoin.
They have to like ask the custodian, please give me my sats back and maybe this custodian complies, maybe they don't.
So they go up here.
They're like the most trusted, most risky kind of bridge that you could use.

## Federated multisig

Then there's federated multi-sig.
This is improving the custodial model a bit.
In this case, you don't have one custodian, you have multiple custodians and they have to collaborate together using a multi-sig contract in order to control the bridge.
Some quorum of the custodians have to sign off on a transaction in order to effectuate withdrawals from the bridge.
Similar to the centralized custodians, they're cheap, they have really high throughput, you can just spin these up as many as you need.
You can have custom execution environments.
For example, Liquid sidechai is like a federated multi-sig.
It has a new type of blockchain with confidential transactions and recursive covenants.
Fedimints have like Chamian eCash, Rootstock has EVM contracts, so you get a lot of flexibility from your execution environment.
There's no single point of failure because you have multiple custodians that have to collude to move the funds.
But even still, if that quorum is compromised, then the custodians could freeze or steal the sats that are locked in the bridge.

I see a hand.
Do you have a question?

[Audience]: "Yeah, when you have also like the single point, let's say you have a multi-sig that requires three sign-offs, and there's three people involved in this transaction.
Each of those people is a point of failure because if they don't sign off on the transaction, then everything just stays locked".

Yeah, so the question was, if you have a multi-sig, and it's like a three of three, so that means all of the signers have to sign off in order to move funds, then any one signer who decides not to sign could block a transfer.
That is true.
And so you might amend this to say, like, if you have a fault tolerance multi-sig, like a two of three instead of a three of three. 

[Audience]: "You are balancing out like how much safety do you want in terms of agreement versus how much slacks do you want in terms of assembly dies of whatever".

Yes, there's a safety versus liveness trade-off in that model.
You still don't have a centralized a single point of failure in that case.
You have two points of failure.
I mean, it's better than one, but it's maybe two of three, like marginally better.
But in the case of Liquid, it's like 11 of 15, I think.
And in the case of Rootstock, it's like 7 of 12 or something.
So they generally try to set this `N` to be very high and then `M` to be some fault-tolerant subset of that.
But very good point.
Thank you for mentioning.
Federated multi-sigs, they don't have exogenous honesty incentives.
So again, they're just relying on reputation or the legal system or something to keep them honest.
And there's no unilateral redemption mechanism.
So the users are relying on this federation to like, co-sign transactions in order to so users can get their funds out of the bridge.
So federated multistakes kind of sit like in the middle, I would say, of the spectrum on, you know, can't steal and can't freeze.
If you add HSMs, like hardware security modules, into the mix, then you can actually upgrade this a little bit and say, if you trust the hardware security module device, then they can't steal your funds, but they can still freeze, because they can just unplug the hardware security module from the Internet, so it can't sign anything.
But since the private key is held in this hardware security module that is theoretically inaccessible to the custodian, they can't sign arbitrary transactions.
And that's how the PowPeg in Rootstock and the Liquid bridge works on the Liquid sidechain.

## Hashrate escrow

There's the hashrate escrow.
So in the case of a hashrate escrow, just like how Paul described in the last talk, you have basically all of the miners in your Layer 1 blockchain are collectively controlling a "hashrate escrow" smart contract on Layer 1.
They have to work together to "upvote" withdrawals from the bridge.
Then users can deposit their sats into this hashrate escrow.
The miners will upvote withdrawal requests, and then if there are enough upvotes, the withdrawal will eventually go through and users can get their sats back out of the hashrate escrow.
But once the sats are in the bridge, they can get IOUs on any kind of arbitrary destination system that the miners want to support.

So, the benefits here are, again, they're cheap, they're high throughput.
Even though an individual sidechain might have relatively low throughput, you can just spin up like an arbitrary large number of sidechains.
They can have custom execution environments.
There's possibly no single point of failure.
It depends on how centralized mining is in your Layer 1 blockchain.
There are endogenous-ish honesty incentives.
So there's not explicitly collateral that gets destroyed or something if the miners are compromised or dishonest.
But the miners do have a large investment in ASICs, and if they attack that hashrate escrow, then maybe the users of Layer 1 will lose confidence in the security of the system, which would destroy the value of the ASICs.
But it still has the downside that a compromised hash power majority could freeze and steal locked assets.
So in the case of freezing, they can just refuse to upvote withdrawal requests.
And in the case of stealing, they can upvote withdrawal requests that are actually invalid according to the sidechain rules.
There's no unilateral redemption mechanism per se.
If you were a miner and you had a majority of the hash power, then you could get your own coins out of the system.
But in that case, it wouldn't be a very safe system, because you could take everybody else's coins as well.
So for all the users who don't have a hash power majority, there's no way for them to like unilaterally get their points out of the system.
They have to rely on the miners to upvote their withdrawal requests.
And I see a question.

[Audience]: "Does this not apply, if you look at Bitcoin, this applies to any single transfer, right?
I mean, these two negative points, like I trust miners to process my transfer and if it's part of the consensus that, like a drivechain, that you have to process it, you'd have to fork the chain.
So it's kind of the same security model as your normal payments, is it not?
It's shown as negative, but it's kind of the same security model as the underlying chain.
So maybe it's being overly strict of kind of saying it's an extra risk, I guess."

Maybe in the case of freezing, you could make that case because a majority of miners could just decide not to mine your transaction in a Layer 1 block, but they can't arbitrarily steal money.
So they can only double spend funds that they have themselves like spent in the past and typically only in the recent past because the deeper you try to reorg the more expensive it is and the harder it is.
But they can't just like pick an address and say like, "oh that address has a lot of Bitcoin, I want to steal that Bitcoin".
But in the case of a hashrate escrow, they can pick any hashrate escrow and say, I want all those coins and just take those coins.
So you're right about the freezing in a way, but the stealing, it is a different trust model.
We'll hold other questions to the end because I've got to blaze through this in like 20 minutes.
So hashrate escrow also I think sits in this upper left quadrant, although we're getting closer to the can't freeze, can't steal quadrant.

## Collateralized custodian

There are collateralized custodians.
In this case, you have either a single custodian or a federation of custodians and they've got some kind of collateral.
And this collateral is usually held on another blockchain like Ethereum or some alt-chain.
And they collectively control a multi-sig and if they try to take the user's funds out of the multi-sig without the user's authorizations, then their collateral will actually get slashed, and then some of the systems will actually give the collateral to the user to compensate them.
So some examples would be [Interlay](https://www.interlay.io/) or [tBTC](https://docs.threshold.network/applications/tbtc-v2) v1.
I think it was probably the first production implementation of this.
[NOMIC](https://www.nomic.io/) is another example.
And these systems, they have high throughput.
You can have a custom execution environment.
There's endogenous, meaning internal honesty incentives because they have this collateral that will get seized or slashed if they were dishonest.
Optionally you could have no single point of failure, most of the systems that are designed like this way, use multi-sigs of some sort.
But it's more expensive.
Like for every Bitcoin that you put into the system, you usually have to have more than a Bitcoin worth of collateral.
And so it's relatively capital intensive.
And there's still no unilateral redemption mechanism.
Users still have to rely on the custodians to actually make a withdrawal from the multi-sig.
So collateralized custodians. I put them right there on the edge of like we're almost getting to Layer 2.
But technically they can still freeze or still use your funds.

## Statechain

There's a system called a statechain, and in this system you have the user Alice and Bob who would be a statechain entity.
They create a multi-sig transaction and then for every transaction, Alice is going to get a redemption transaction.
Alice can use the redemption transaction to get her coins out of the bridge if Bob is ever uncooperative.
Once she has that redemption transaction, she can safely put funds into the bridge or receive funds on the system.
And then she gets issued some IOUs on the statechain, can transfer them around and eventually get her sats back out on the mainchain.
So statechains are cool because they have high throughput.
It's the first system we've talked about that has a unilateral redemption mechanism.
You could optionally have improved privacy with blind signatures.
You could optionally have no single point of failure, because some designs for statechains that use a single statechain entity, some use a federation, which would have no single point of failure if they have a fault tolerant signing policy.

But the downsides are you still don't have a fully custom execution environment.
You have limited spending denominations, (which) is actually one of the interesting limitations of the statechain system.
Recipients must be online in order to receive funds because they have to co-sign and acknowledge the receipt of transactions.
Compromised statechain entities can steal funds from payment recipients.
This is a somewhat subtle attack, but basically the statechain entity could collude with previous owners of a coin that has been sent to you in order to use the unilateral redemption transaction to withdraw the coin before you notice that this has happened.
It's like a subtle attack that they try to solve with hardware security modules, but it is like a fundamental limitation of the statechain model.

So for recipients of statechain transactions, the statechain entity can't freeze user funds because they have the unilateral redemption transaction, but they can steal your funds by colluding with earlier owners of the coins.
For statechain senders, that is people who put coins into the system and then send those coins to somebody else, the statechain entity can't steal those coins.
And if they use a hardware security module and you trust the hardware security module, then they also can't steal.
So this is actually a pretty decent model if you accept those security assumptions.

## Lightning Network

Then there's the Lightning Network, where Alice is a user and Bob is Alice's channel partner.
They create a multi-sig together with some revocation secrets that enable each party to keep the other honest.
Once they have that set up, they can put funds into the bridge and then transfer coins around the Lightning Network.
And then at any time, if Bob becomes uncooperative, Alice can use her most recent channel state to get her funds out of the system, and then if Bob tries to cheat and close his channel with an earlier channel state, Alice can use the revocation secret to take all of the funds in the channel and kind of penalize Bob for trying to steal from her.
So this is a pretty high security system.
It's also got high throughput.
There's no single point of failure because both users can like lead with their funds if the other one's uncooperative.
There's a unilateral redemption capability.
There's internal or endogenous honesty incentives due to the revocation transaction.

But there are some fundamental limitations of this bridge.
Users have limited inbound payment capacity due to the channel liquidity situation.
There's limited onboarding and offboarding capacity because you need to make a Layer 1 transaction to onboard new users and you also need to make a Layer 1 transaction to get your funds out onto Layer 1 to offboard.
Recipients must be online and there's no custom execution environment, like you can only do simple payments.

A dishonest hash power majority can steal sats that are sent to channel partners.
So this is kind of far-fetched, but it's still a theoretical possibility.
Basically the idea is that a hash power majority could collude with Bob and say, go ahead, send the earliest channel state where you had the most money in the channel after you've already sent most of your money to Alice, and we will censor any revocation transactions that Alice or her watchtowers tried to send on Layer 1.
And they censor the revocation transaction for the duration of the challenge period and eventually Bob gets all of his money out of the channel even though technically he already sent it to Alice.

So for Lightning's senders, nobody can steal the sats in the channel, nobody can freeze the sats in the channel, but for recipients, they're actually trusting the hash power majority not to be colluding with Bob to censor the revocation transaction.

## L2 optimistic rollup

I'm going to skip the optimistic rollup, which is more like a theoretical bridge that you can't build on Bitcoin today.

## L2 validity rollup

And go straight to the last bridge that I wanted to cover which is the L2 validity rollup.
So this is another bridge that you can't build on Bitcoin today but it is a bridge design that has been proposed and actually implemented on other blockchains.
And the basic idea is that you have this validity rollup operator, Alice, and for every new block that gets created in the destination system, Alice is going to include a validity proof along with the data of the block in a transaction that gets posted to the rollup script on Layer 1.
And with that, users can be certain that when they put funds into the bridge, they can always get their money out.
And also that neither Alice nor anyone else is able to steal their money out of the bridge.

So L2 validity roll-ups are nice because they give you a custom execution environment.
L2 validity roll-up would be a destination system that can support any kind of execution environment.
It could be a Simplicity smart contract or Ethereum, EVM smart contracts or Zcash-style private transactions.
It doesn't matter, as long as you can make a validity proof that you can put on L1 and L1 nodes can verify, you can have any kind of execution environment you want.
There's no single point of failure because the user can always get their funds out of the bridge, even if the validity rollup operator is uncooperative.
So it also has a unilateral redemption mechanism that way.
The compromised rollup operator cannot steal sats that are locked in the bridge because they can't forge validity proofs that convince L1 users that their withdrawal transaction is valid even though it's invalid.
These are cryptographic proofs.
If they don't have the private keys that own the sats, then they can't withdraw the sats from the bridge.
And it also has double spend resistance that is equivalent to Layer 1.
So this is important because it means that, if you trust that you're not going to get double spent on Layer 1 because it's so expensive to re-org a block, then you can also have that same level of trust or assurance on Layer 2 validity rollup.
All of these qualities put together make the Layer 2 validity rollup bridge completely trustless.
There are no new trust assumptions compared to holding or transacting in sats on Layer 1.

The downsides of this are that there is high throughput, but not unlimited throughput.
Because you have to post the block of every Layer 2 validity rollup inside of a Layer 1 block, your throughput capacity is limited by your carrying capacity on Layer 1.
In the case of Bitcoin, it would be like 4 megabytes per block.
It's also relatively expensive because validity proofs require a high computational capabilities.
It's not as computationally intensive as mining Bitcoin, but it's more computationally expensive than just signing transactions on a multi-sig or something like that.
So validity roll-ups go in the lowest, farthest right quadrant of this where this is totally trustless, like no one can steal or freeze funds, and it's the same security model is like holding sats on Layer 1.

## Ingredients for a trustless bridge

The ingredients that you need to have a trustless bridge like this, and the validity you rollup has all of these ingredients, is that Layer 1 needs to know what the rules of the destination system are, or at least needs to know a hash of the rules.
Because with that, we can verify that destination system state updates are valid according to the rules of the system.
And that ensures that people can't, for example, make an invalid withdrawal from the bridge, claiming that they are withdrawing sats that they own, which they do not actually own.

We need to know what the current canonical state root of the destination system is, so that users can't effectively double-spend the bridge by withdrawing sats that they've already transferred to somebody else.

We need to enforce that a state update must build on the last known canonical state, meaning that the destination system cannot re-org independently of Bitcoin Layer 1.
And this ensures that when a user receives coins on Layer 2 or the destination system, that the security of that transaction is equivalent to if they were receiving Bitcoin on Layer 1.

And finally, we need a strong data availability assurance for state update data.
We need to have at least enough data stored somewhere with a high degree of data availability assurance that we can fully reconstruct the current canonical state of the system.
And the reason why you need this is so that in the case of a validity rollup, the user needs to know what the current state of the system is so they know how much money they have.
And with that, they can also prove that they own money or sats in the current state of the system, and they can make a withdrawal for that amount of sats.
So they need to know the current state so that they can prove, I own some sats in that state and I want to make a withdrawal from the bridge.
If I had time, I was going to discuss one more, but I'm going to skip that.
I produced a report about validity rollups that goes into much more detail about their history and how they work and how we can build them on Bitcoin.
It's at [bitcoinrollups.org](https://bitcoinrollups.org/) if you want to check it out.
And I'm happy to take any questions if you have time for questions.
Thank you.
