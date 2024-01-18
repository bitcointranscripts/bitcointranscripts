---
title: "Building Trustless Bridges"
transcript_by: kouloumos via tstbtc v1.0.0 --needs-review
media: https://www.youtube.com/watch?v=M40yzuv6DNY
tags: []
speakers: ['John Light']
categories: ['conference']
date: 2023-07-06
---
Thank you all for coming to my talk.
As is titled, I'll be talking about how we can build trustless bridges for Bitcoin.
So my name is John Light.
I'm working on a project called Sovereign.
We actually utilize a bridge, the Rootstock-Cowpeg Bridge, because our project was built on a Rootstock side chain.
And we're interested in how we can improve the quality of that bridge.
Currently it's a federated bridge, we would like to upgrade to a trustless bridge.
And this talk will describe one way that we can build a trustless bridge.
So just to kind of introduce this concept, what is a Bitcoin bridge?
So a Bitcoin bridge is a system that enables users to lock stats on the Bitcoin main chain and then receive an equivalent amount of IOUs for stats on some destination system.
And then, perhaps most importantly, It enables the user to burn the IOUs on the destination system in exchange for an equivalent amount of stats on the main chain.
This is also referred to in the literature as a two-way peg, but nowadays most people call these bridges.
So the destination system could be blockchains, it could be tangles or hashgraphs, fediments, state channel networks, centralized or federated databases, really any kind of system for transferring BTC or Sats, however you prefer.
So at a very high level, the bridging process works like this.
Some, a user will take some Sats, they will lock some Sats in a address on the main chain.
There's a bridge system that does some stuff.
And then the user will, on the destination system, they'll get issued an IOU for an equivalent amount of sats, and then they can use those sats in the destination system.
So that's the deposit process.
And then a withdrawal works the same way in reverse.
So the user is going to burn some sats on the IOUs on the destination system.
The bridge is going to do some stuff, and then the user will get some sats unlocked and sent to their mainchain address.
The bridge does some stuff is really where all of the differences between the different bridge designs comes into play and I'll describe what that landscape of the design space looks like currently.
But first I wanna talk about why are we even doing this?
Why would users give up control of their stats to a bridge?
So the first reason is we want to increase transaction throughput.
So Hal Finney said back in the day that Bitcoin itself cannot scale to have every single financial transaction in the world.
There needs to be a secondary level of payment system, which is lighter weight and more efficient.
And so a bridge is like how you get stats into this secondary level that is lighter weight and more efficient.
Howe's intuition there was backed up by empirical data through numerous studies, one of which was created and published by the mining group BitFury.
It's a few years out of date by now, but the basic principle still applies.
They showed that if you increase the block size to 8 megabytes, then within 6 months, like 95% of the nodes are going to get knocked off the network just because they're not powerful enough to keep up with such a large block size limit.
Like I said, this is several years out of date now.
The situation has probably been improved, but the basic idea still holds.
As you increase the block size limit, it becomes more difficult for nodes on the network to keep up unless they are also increasing their computing power at a similar rate, which of course increases the cost, which knocks some people out who just can't afford those increased costs.
So it increases centralization.
The other motivating factor is we want to be able to add new functionality to Bitcoin.

## Why create a bitcoin bridge?

So everyone knows, or at least people who are familiar with Bitscreen's script know that it's kind of limited in its capabilities.
There are only a few primitives that you can combine together to create Bitcoin smart contracts.
People have come up with all kinds of new ideas of things that we could do with blockchains, other than what is already possible with Bitcoin today.
Satoshi Nakamoto referenced this when he was talking about this idea called BitDNS, which is like a precursor to Namecoin.
He said, piling every proof-of-work quorum system in the world into one data set doesn't scale.
Bitcoin and BitDNS can be used separately.
Users shouldn't have to download all or both, use one or the other.
BitDNS users may not want to download everything the next several unrelated networks decide to pile in either.
So he's basically referring to this tension between having a blockchain that has limited expressivity that maybe only supports one or a few small numbers of applications, and then a blockchain that has full expressivity that you can pile all of these different types of applications into a single blockchain.
Do we really want that or do we want to try to firewall these things and have it separation of concerns so that users who are only interested in one application can use one system, and then users who are interested in another application can use some other systems.
So we want solutions to this problem that don't harm the decentralization and the security of the Bitcoin main chain.
And so we've come up with this idea of bridges so that we can increase transaction throughput and add new functionality by transferring SACs to other systems, and those other systems take on the burden of increasing transaction throughput or adding new functionality.
So one way that you could solve this problem is just by piling all of this stuff into the Bitcoin main chain so we could have more transactions per block, more blocks per day, more expressivity, more everything.
But your Raspberry Pi node is not going to be very happy about that.
And eventually, as the BitFury study shows, it'll just get kicked off of the network.
And that is bad for Bitcoin decentralization security, so it doesn't really meet our requirements that we defined in the previous slide.
So what we've done instead is we come up with this way to have the Bitcoin main chain and then some destination system.
And we have this bridge that connects the two so that you can move sats back and forth.
Then you have your Raspberry Pi nodes that are like validating the Bitcoin main chain.
They're super happy because the block size limit can stay small and Bitcoin script stays very simple so they can easily verify Bitcoin transactions.
And then on the destination system, we don't really care what kind of nodes run the destination system if users want to opt into a destination system Where they have to have you know some beefy server thing then you know that's fine like they're free to do that But the main chain users are unaffected.
So let's talk about the different types of bridges that exist or could exist.
But before we do, I want to take a little semantics detour.
There are a couple of jargony terms that I'm gonna use in this talk.
One I've already referenced in the title of the talk, which is trustless.
So what do we mean by trustless?
I'm gonna define trustless as saying that a bridge is trustless if it does not introduce any new trust assumptions compared to holding and transacting or using SAS on the Bitcoin main chain.
And so therefore a trusted bridge is a bridge that introduces one or more new trust assumptions.
I know that there's not currently like a total consensus on what the definition of trustless is, but I think that in this context, I think this is a reasonable definition.
So just keep that definition in mind when I use that term throughout this talk.
I'm also going to use the phrase Layer 2 because this is a conference about Layer 2s.
So I want to be clear about what I mean when I say Layer 2.
There are a few definitions that have been proposed for Layer 2.
Georgios Konstantopoulos says, what makes a Layer 2 special is when Layer 2 security is equal to Layer 1 security.
So he's basically saying Layer 2 is an off-chain system that has ownership security and double spend resistance equal to the main chain.
This definition isn't very satisfying to me.
He actually contradicts himself like in his tweet.
So he says layer two security is equal to layer one security, but then he says, you know, that includes this, you know, it would include a system where you play a fixed duration game where honest players are guaranteed to win, but that's not how Layer 1 works.
There's no fixed duration game when you're holding funds on Layer 1.
So yeah, this kind of is not an internally consistent definition, so I reject it.
Munib Ali from the SACS project has proposed the definition where he basically says Layer 2 is an off-chain system that gets full double-spend resistance from the main chain.
This definition is also not very satisfying because it would actually exclude lightning, which I think is weird.
It also doesn't completely accurately describe his system stacks because after the Nakamoto release stacks will only get full security after I think 100 blocks.
So there's like a caveat there like okay, eventually you get like full double spend resistance from the mainchain.
But anyways, just because it excludes like lightning it just doesn't seem very satisfying to me, so I also reject that definition.
And then there's this third definition where layer two is like any off-chain SAS transfer system.
And there are lots of people who express this kind of viewpoint.
Not Groobles on Twitter says, lightning, Fetimint, and liquid are all layer twos.
This guy, Matt.biff, says like Coinbase is a layer two.
Kali from Cashew says, you know, Opendime is layer two.
Instagib says altcoins are layer twos.
Kali from Cashew says OpenDime is layer 2.
Instant Gibbs says altcoins are layer 2.
Of all the definitions I've mentioned so far, this is probably my favorite because it's at least consistent.
Right, you can say, okay, any off-chain transfer system is a layer two, but it still just doesn't feel very satisfying to me to say like Coinbase is layer two or OpenDiamond is layer two.
So I'm introducing a new definition, which is like a bridge, a layer two bridge, if users can unilaterally redeem their IOUs, like on the destination system, for main chain SATs. That means they don't require any cooperation from any third parties to get their stats out of the system.
And then this redemption process is actually enforced by the main chain consensus rules.
And so therefore, a non-layer 2 bridge is a bridge that does not let users unilaterally redeem their IOUs. For mainchain SaaS, you need some sort of cooperation with a third party to get your money out of the system.
So that's the terminology that I'll be using.
And so I've laid out this quadrant.
On the top, systems that are close to the top are systems where, yeah, systems on the top half are systems where some third parties can steal user funds.
Systems on the bottom half are systems where third parties cannot steal user funds.
Systems on the left hand, I'm calling not layer two systems because third parties can freeze funds, meaning that users cannot actually get their funds out of the system.
And then the systems on the right are all going to be layer two systems because third parties cannot freeze user funds.
Users can always make a transaction on the main chain to get their money out of the bridge.
So the first type of bridge is the classic centralized custodian.
An example of this would be like WBTC on Ethereum or even your centralized exchanges like Mt. Docks or Silk Road or something like that.
So the centralized custodian fully controls the bridge.
They usually just give the users an address, users send their stats to the address, they get an equivalent amount of IOUs like in the custodian's database.
In the case of WBTC, it's like a token on a different blockchain.
But the users trust the centralized custodian absolutely with the security of their funds.
So centralized custodians aren't all bad.

## Centralized custodian

They have some benefits.
They're cheap.
They have really high throughput.
You can have a totally custom execution environment for how you can manipulate your IOUs and transfer them between users.
But of course, they have the obvious downsides of there's a single point of failure.
The compromised custodians can freeze and steal user funds.
There's no kind of internal incentive system keeping them honest, like you just rely on the legal system or reputation or something.
And the users cannot unilaterally redeem their IOUs for Bitcoin.
They have to like ask the custodian, please give me my stats back and maybe this custodian complies, maybe they don't.
So they go up here.
They're like the most trusted, most risky kind of bridge that you could use.
Then there's federated multi-sig.
This is improving the custodial model a bit.
In this case, you don't have one custodian, you have multiple custodians and they have to collaborate together using a multi-state contract in order to control the bridge.
Some quorum of the custodians have to sign off on a transaction in order to effectuate withdrawals from the bridge.

## Federated multisig

Similar to the centralized custodians, they're cheap, they have really high throughput, you can just spin these up as many as you need.
You can have custom execution environments.
For example, you know, Liquid sidechain is like a federated multi-sig.
It has a new type of blockchain with confidential transactions and recursive covenants.
Fetty Mints have like Chami and eCash, Rootstock has EVM contracts, so you get a lot of flexibility from your execution environment.
There's no single point of failure because you have multiple custodians that have to collude to move the funds.
But even still, if that quorum is compromised, then the custodians could freeze or steal the sats that are locked in the bridge.
I see a hand.
You have a question?
Yeah, when you have also like the single point, let's say you have a multisig that requires three sign-offs, and there's three people involved in this transaction.
You have a single, each of those people is a point of failure because if they don't sign off on the transaction, then everything just stays locked.
Yeah, so The question was, if you have a multi-sig, and it's like a three of three, so that means all of the signers have to sign off in order to move funds, then any one signer who decides not to sign could block a transfer.
That is true.
And so you might amend this to say, like, if you have a fault tolerance multi-sig, like a two of three instead of a three of three Yes, there's a there's a safety versus liveness trade-off In that model, but you still in that case You don't you still don't have a centralized a single point of failure in that case.
You have two points of failure.
I've never compromised two though.
Yeah.
Yeah.
Yeah.
I mean, it's better than one, but it's maybe two of three, like marginally better.
But in the case of liquid, it's like 11 of 15, I think.
And in the case of rootstock, it's like seven of 12 or something.
So they generally try to set this N to be very high and then M to be some fault-tolerant subset of that.
But very good point.
Thank you for mentioning.
Federated multisigs, they don't have exogenous honesty incentives.
So again, they're just relying on reputation or the legal system or something to keep them honest.
And there's no unilateral redemption mechanism.
So the users are relying on this federation to like, co-sign transactions in order to so users can get their funds out of the bridge.
So federated multistakes kind of sit like in the middle, I would say, of the spectrum on, you know, can't steal and can't freeze.
If you add HSMs, like hardware security modules, into the mix, then you can actually upgrade this a little bit and say, if you trust the hardware security module device, then they can't steal your funds, but they can still freeze, because they can just unplug the hardware security module from the Internet, so it can't sign anything.
But since the private key is held in this hardware security module that is theoretically inaccessible to the custodian, they can't sign arbitrary transactions.
And that's how the PowPeg in rootstock and the Liquid bridge works on the liquid sidechain.
There's the hash rate escrow.
So in the case of a hash rate escrow, you have like just Paul described in the last talk, you have basically all of the miners in your layer one blockchain are collectively controlling a hash rate escrow smart contract on layer one.
They have to like work together to upvote withdrawals from the bridge.
And so then users can deposit their stats into this hashrate escrow.
The miners will upvote withdrawal requests, and then if there are enough upvotes, the withdrawal will eventually go through and users can get their sats back out of the hash rate escrow.
But once the sats are in the bridge, they can get IOUs on any kind of arbitrary destination system that the miners want to support.
So, the benefits here are, again, they're cheap, they're high throughput.

## Hashrate escrow

Even though an individual sidechain might have relatively low throughput, you can just spin up like an arbitrary large number of sidechains.
They can have custom execution environments.
There's possibly no single point of failure.
It depends on how centralized mining is in your layer one blockchain.
There are endogenous-ish honesty incentives.
So there's not explicitly collateral that gets destroyed or something if the miners are compromised or dishonest.
But the miners do have a large investment in ASICs, and if they attack that hash rate escrow, then maybe the users of layer one will lose confidence in the security of the system, which would destroy the value of the ASICs. But it still has the downside that a compromised hash power majority could freeze and steal locked assets.
So in the case of freezing, they can just refuse to upvote withdrawal requests.
And In the case of stealing, they can upvote withdrawal requests that are actually invalid according to the sidechain rules.
There's no unilateral redemption mechanism per se.
If you were a miner and you had a majority of the hash power, then you could get your own coins out of the system.
But in that case, it wouldn't be a very safe system, because you could take everybody else's coins as well.
So for all the users who don't have a hash power majority, there's no way for them to like unilaterally get their points out of the system.
They have to rely on the miners to upvote their withdrawal requests.
And I see a question.
I mean, just like, does this not apply, if you look at Bitcoin, this applies to any single transfer, right?
I mean, these two negative points, like I trust miners to process my transfer and if it's part of the consensus that, you know, like a drive chain, that you have to process it, you know, you'd have to fork the chain.
So it's kind of the same security model as your normal payments, is it not?
So it's like it's shown as negative, but it's kind of the same security model as the underlying chain.
So maybe it's being overly strict of kind of saying it's an extra risk, I guess.
Maybe in the case of freezing, you could make that case because a majority of miners could just decide not to mine your transaction in a layer 1 block, but they can't arbitrarily steal money.
So they can only double spend funds that they have themselves like spent in the past and typically only in the recent past because the deeper you try to reorg the more expensive it is and the harder it is.
But they can't just like pick an address and say like oh that address has a lot of Bitcoin, I wanna steal that Bitcoin.
But in the case of a hash rate escrow, they can pick any hash rate escrow and say, I want all those coins and just take those coins.
So you're right about the freezing in a way, but the stealing, it is a different trust model.
We'll hold other questions to the end because I've got to blaze through this in like 20 minutes.
So Hashrate escrow also I think sits in this upper left quadrant, although we're getting closer to the can't freeze, can't steal quadrant.
There are collateralized custodians.
In this case, you have either a single custodian or a federation of custodians and they've got some kind of collateral.
And this collateral is usually held on another blockchain like Ethereum or some alt chain.
And they collectively control a multi-sig and if they try to take the user's funds out of the multi-sig without the user's authorizations, then their collateral will actually get slashed, And then some of the systems will actually give the collateral to the user to compensate them.
So some examples would be Interlay or TBTC v1.
I think it was probably the first production implementation of this.
NOMIC is another example.
And these systems, they have high throughput.
You can have a custom execution environment.

## Collateralized custodian

There's endogenous, meaning internal, like honesty incentives because they have this collateral that will get seized or slashed if they get if they were dishonest.
And then you know optionally you could have no single point of failure most of the systems that are designed like this way use multi-sigs of some sort.
But it's more expensive.
You have to, like for every Bitcoin that you put into the system, you usually have to have more than a Bitcoin worth of collateral.
And so it's relatively capital intensive.
And there's still no unilateral redemption mechanism.
Users still have to rely on the custodians to actually make a withdrawal from the multi-sig.
So collateralized custodians are, I put them right there on the edge of like we're almost getting to layer two.
But technically they can still freeze or still use your funds.
There's a system called a state chain and in this system you have the user Alice and Bob who would be a state chain entity.
They create a multi-sig transaction and then for every transaction Alice is going to get a redemption transaction.
Alice can use the redemption transaction to get her coins out of the bridge if Bob is ever uncooperative.
Once she has that redemption transaction, she can safely put funds into the bridge or receive funds on the system.
And then she gets issued some IOUs on the state chain, can transfer them around and eventually get her stats back out on the main chain.
So state chains are cool because they have high throughput.

## Statechain

It's the first system we've talked about that has a unilateral redemption mechanism.
You could optionally have improved privacy with blind signatures.
You could optionally have no single point of failure, because some designs for state chains that use a single state chain entity, some use a federation, which would have no single point of failure if they have a fault tolerant signing policy.
But the downsides are you still don't have a fully custom execution environment, And you have limited spending denominations is actually one of the interesting limitations of the state chain system.
Recipients must be online in order to receive funds because they have to like co-sign and acknowledge the receipt of transactions.
And compromised state chain entities can steal funds from payment recipients.
So this is a somewhat subtle attack, but basically The state chain entity could collude with previous owners of a coin that has been sent to you in order to use the unilateral redemption transaction to withdraw the coin before you notice that this has happened.
So yeah, it's like a subtle attack that they try to solve with hardware security modules, but it is like a fundamental limitation of the state chain model.
So for recipients of state chain transactions, the state chain entity can't freeze user funds because they have the unilateral redemption transaction, but they can steal your funds by colluding with earlier owners of the coins.
For state chain senders, that is people who put coins into the system and then send those coins to somebody else, the state chain entity can't steal those coins.
And if they use a hardware security module and you trust the hardware security module, then they also can't steal.
So this is actually a pretty decent model if you accept those security assumptions.
And then there's the Lightning Network, where Alice is a user and Bob is Alice's channel partner.
They create a multi-sig together with some revocation secrets that enable each party to keep the other honest.
Once they have that set up, they can put funds into the bridge and then transfer coins around the Lightning Network.
And then at any time, if Bob becomes uncooperative, Alice can use her most recent channel state to get her funds out of the system, and then if Bob tries to cheat and close his channel with an earlier channel state, Alice can use the revocation secret to take all of the funds in the channel and kind of penalize Bob for trying to steal from her.
So this is a pretty high security system.
It's also got high throughput.

## Lightning Network

There's no single point of failure because both users can like lead with their funds if the other one's uncooperative.
There's a unilateral redemption capability.
There's internal or endogenous honesty incentives due to the revocation transaction.
But there are some fundamental limitations of this bridge.
Users have limited inbound payment capacity due to the channel liquidity situation.
There's limited onboarding and offboarding capacity because you need to make a layer one transaction to onboard new users and you also need to make a layer one transaction to get your funds out onto layer one to offboard.
Recipients must be online and there's no custom execution environment, like you can only do simple payments.
A dishonest hash power majority can steal sats that are sent to channel partners.
So this is kind of far-fetched, but it's still a theoretical possibility.
Basically the idea is that a hash power majority could collude with Bob and say, go ahead, send the earliest channel state where you had the most money in the channel after you've already sent most of your money to Alice, and we will censor any revocation transactions that Alice or her watchtowers tried to send on layer one.
And they censor the red vacation transaction for the duration of the challenge period and eventually Bob gets all of his money out of the channel even though technically he already sent it to Alice.
So for Lightning's senders, nobody can steal the Sass in the channel, nobody can freeze the Sass in the channel, but for recipients, they're actually trusting the hash power majority not to be colluding with Bob to censor the revocation transaction.
I'm gonna skip the optimistic rollup, which is more like a theoretical bridge that you can't build on Bitcoin today.

## L2 optimistic rollup

And go straight to the last bridge that I wanted to cover which is the L2 validity rollup.
So this is another bridge that like you can't build on Bitcoin today but it is a bridge design that has been proposed and actually implemented on other blockchains.
And the basic idea is that you have this validity rollup operator, Alice, and for every new block that gets created in the destination system, Alice is going to include a validity proof along with the data of the block in a transaction that gets posted to the rollup script on layer 1.
And with that, users can be certain that when they put funds into the bridge, they can always get their money out.
And also that neither Alice nor anyone else is able to steal their money out of the bridge.
So L2 validity roll-ups are nice because they give you a custom execution environment.

## L2 validity rollup

It could support L2 validity roll-up would be a destination system that can support any kind of execution environment.
It could be a Simplicity smart contract or Ethereum, you know, EVM smart contracts or Zcash-style private transactions.
It doesn't matter As long as you can make a validity proof that you can put on L1 and L1 nodes can verify, you can have any kind of execution environment you want.
There's no single point of failure because the user can always get their funds out of the bridge, even if the validity rollup operator is uncooperative.
So it also has a unilateral redemption mechanism that way.
The compromised rollup operator cannot steal Sats that are locked in the bridge because they can't forge validity proofs that convince L1 users that their withdrawal transaction is valid even though it's invalid.
These are cryptographic proofs.
If they don't have the private keys that own the SASS, then they can't withdraw the SASS from the bridge.
And it also has double spend resistance that is equivalent to layer 1.
So this is important because it means that, yeah, if you trust that you're not going to get double spent on layer one because it's so expensive to pre-org a block, then you can also have that same level of trust or assurance on layer two validity rollup.
All of these qualities put together make the layer two validity rollup bridge completely trustless.
There are no new trust assumptions compared to holding or transacting in SACs on Layer 1.
The downsides of this are that there is high throughput, but not unlimited throughput.
Because you have to post the block of every layer 2 validity rollup inside of a layer 1 block, your throughput capacity is limited by your carrying capacity on layer 1.
In the case of Bitcoin, it would be like 4 megabytes per block.
It's also relatively expensive because validity proofs require a high computational capabilities.
It's not as computationally intensive as mining Bitcoin, but it's more computationally expensive than just signing transactions on a multi-sig or something like that.
So validity roll-ups go in the lowest, farthest right quadrant of this where this is totally trustless, like no one can steal or freeze funds, and it's, at least it's, the same trust model, the same security model is like pulling SASS on layer one.
You have about five minutes.
Thank you.

## Ingredients for a trustless bridge

So the ingredients that you need to have a trustless bridge like this and the validity you roll up has all of these ingredients is that layer one needs to know what the rules of the destination system are, or at least needs to know a hash of the rules.
Because with that, we can verify that destination system state updates are valid according to the rules of the system.
And that ensures that People can't, for example, make an invalid withdrawal from the bridge, claiming that they are withdrawing Sats that they own, which they do not actually own.
We need to know what the current canonical state root of the destination system is, so that users can't effectively double-spend the bridge by withdrawing sats that they've already transferred to somebody else.
We need to enforce that a state update must build on the last known canonical state, meaning that the destination system cannot reorganize independently of Bitcoin layer 1.
And This ensures that when a user receives coins on layer 2 or the destination system, that the security of that transaction is equivalent to if they were receiving Bitcoin on layer one.
And finally, we need a strong data availability assurance for state update data.
We need to have at least enough data stored somewhere with a high degree of data availability assurance that we can fully reconstruct the current canonical state of the system.
And the reason why you need this is so that in the case of a validity rollup, like the user needs to know what the current state of the system is so they know how much money they have.
And with that, they can also prove that they own money or stats in the current state of the system, and they can make a withdrawal for that amount of stats.
So they need to know the current state so that they can prove, I own some stats in that state and I want to make a withdrawal from the bridge.
If I had time, I was going to discuss one more, but I'm going to skip that.
I produced a report about Kubernetes rollups that goes into much more detail about their history and how they work and how we can build them on Bitcoin.
It's at Bitcoin roll ups.org if you want to check it out.
And I'm happy to take any questions if you have time for questions.
Thank you.
That was me.
Please come on up to the next one.
Thank you very much.
Thank you.
