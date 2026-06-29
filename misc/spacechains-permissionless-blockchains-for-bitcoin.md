---
title: 'Spacechains – Permissionless Blockchains for Bitcoin'
transcript_by: 'muchai254 via review.btctranscripts.com'
media: 'https://www.youtube.com/watch?v=N2ow4Q34Jeg'
date: '2020-12-13'
tags:
  - 'sidechains'
  - 'covenants'
  - 'sighash-anyprevout'
  - 'op-checktemplateverify'
  - 'eltoo'
  - 'rbf'
speakers:
  - 'Ruben Somsen'
categories:
  - 'Contract Protocols'
  - 'Soft Forks'
  - 'Mining'
source_file: 'https://www.youtube.com/watch?v=N2ow4Q34Jeg'
summary: "Ruben Somsen presents Spacechains, a design for permissionless, trustless secondary blockchains that extend the Bitcoin ecosystem without creating competing altcoins. The design combines two primitives: Blind Merged Mining (BMM) and the Perpetual One-Way Peg (P1WP).\nBMM lets anyone produce a spacechain block by winning a fee-bidding auction for a single, unique slot in the Bitcoin chain, requiring only one Bitcoin transaction per block. It is built from a pre-generated sequence of covenant transactions linked by a one-block relative timelock, using SIGHASH_ANYPREVOUT (or alternatively OP_CHECKTEMPLATEVERIFY) to avoid the circular-reference problem of self-referencing signatures, with users bidding via SIGHASH_ANYONECANPAY + SIGHASH_SINGLE and RBF. This fully decouples spacechain mining from Bitcoin miners, who simply select the highest-fee bid, preserving censorship resistance and inheriting Bitcoin's difficulty and reorg properties.\nP1WP lets users burn BTC for an equivalent amount of \"spacecoins,\" a one-way peg that preserves the 21M cap and gives the token a single, non-speculative purpose: paying spacechain fees."
---

## Intro

Ruben Somsen: 00:00:01

Hi, welcome to my presentation about spacechains.
Spacechains are a combination of two ideas, one being the `Blind Merged Mining` and the other one being the `Perpetual One-way Peg`.
I'm going to go through both of them and the combined concept is what I call spacechains.

## Key Points

Ruben Somsen: 00:00:18

So the key points are we're going to create some kind of blockchain, but we're going to do it by outsourcing mining to the Bitcoin blockchain with only a single transaction per block, meaning that there's not going to be a lot of overhead on the Bitcoin blockchain.
It's going to be a trustless chain, multiple trustless chains, as many chains as you like, that can be created permissionlessly and they essentially serve the Bitcoin ecosystem.
There's not going to be a competing coin, there's no altcoin, no shenanigans like that.
It's going to function in a way that does not require a speculative asset.
So this is hopefully going to open a door to more permissionless innovation, where essentially anyone can create blockchains that serve the Bitcoin ecosystem.
So the main thing, the one caveat that needs to be said is that this is not a `two-way peg`.
So this is not going to be a system where you take your Bitcoin, you move to a spacechain, and then you do your thing there and you move back.
That is not going to be possible.
So you might be thinking now, is this a `sidechain`?
Well, that's a good question.
I think depending on who you ask, the answer may be yes or maybe no.
So I decided to answer this a little bit more in an indirect way and describing basically what part of a sidechain, kind of the sidechain idea it does hit on.
So obviously, the one it doesn't hit on is there's no trustless `two-way peg`.
But the things it does do is it allows permissionless chain creation without another speculative asset.
And really it serves the Bitcoin ecosystem.
And I think that is one of the, at least half of the dream of what kind of the sidechain idea was all about.
When the paper original released in 2014, at least that was what I was dreaming of, having all these different chains where I could just move your Bitcoins back and forth.
And now, okay, you can't quite move your Bitcoins back and forth, but we still have lots of different chains that somehow serve Bitcoin.

## What is a blockchain

Ruben Somsen: 00:02:22

So to kind of go through what a spacechain is exactly, I want to start very simple, but with a deceptively simple question, which is what is a blockchain?
And I think when you hear this question you might think it's simple but I think it's actually a difficult question to answer.
So the way I want to answer this question is that it's an open database essentially but it's an open database that is rate limited by sacrifice.
And in the case of Bitcoin, obviously, the sacrifice is proof-of-work.
And the nice thing about Bitcoin is obviously that, essentially, anyone can create a block.
If too many blocks come in at the same time or within a certain time frame, the difficulty goes up.
So this naturally rate limits how many blocks can be created and this sort of makes sure that even though it's an open database that anybody can add data to, there's never going to be too much data.
There's only going to be roughly two megabytes every 10 minutes.
So the interesting thing is that the resulting scarcity, at least in the way Bitcoin did it, can be tokenized.
Because there can only be one block every 10 minutes.
If you add a block reward there and you create, say, 25 bitcoins every 10 minutes and then, you know, after a couple of years, 12.5, 6.25, etc.
That's the way Bitcoin issues new tokens.
And then once you have tokens, the system is kind of bootstrapped, right?
We have a scarce token that everybody can use.
But the one interesting thing that I think is quite underappreciated is that Satoshi Nakamoto came up with a way to do mining or leave it to other people to do mining.
And the importance of that cannot be understated.
You don't have to take your transaction and put it into your block yourself and mine it.
But what you can do is you can just add a fee and anyone can take it.
You send it over through the P2P network and anyone can take those transactions, put them into a block, and claim the fee for themselves if they're successful.
And that's a non-interactive process.
And that is really one of the key things that makes Bitcoin work.
And maybe it looks obvious in hindsight, but I don't think it was that obvious.
And it turns out that this is quite a key feature to kind of recreate yet another blockchain, you need to have a feature like this.
So roughly what we're trying to do here is we're trying to create yet another blockchain or multiple blockchains.
But we want to skip the tokenization step.
We don't want to create yet another Bitcoin competitor, yet another altcoin, but everything else we need.
We need an open database that's rate limited by sacrifice, and we need some way to outsource the mining where we just send our transaction and somebody else puts into a block for us.
So these two features are basically what we're going to try and recreate.

## Creating blockchains - Blind Merged Mining (BMM)

Ruben Somsen: 00:05:07

So first, creating a blockchain, how do you do that?
Well, the mechanism I'm using here is called `Blind Merged Mining`.
And essentially, you use BTC, you use the Bitcoin blockchain, or you use the Bitcoins to sort of simulate or emulate mining.
And what you do, like with Bitcoin, you have proof-of-work, and that's a way to show that you sacrificed something, provably.
But now that we have Bitcoin, we can do it in other ways, right?
We can say, okay, well, maybe I burn a Bitcoin, or maybe I lock up my Bitcoins, or maybe I waste a bunch of block space on the Bitcoin blockchain, which is a terrible idea, don't do that, but it works.
Or, and this is my personal way I think this should be going, is through something called fee-bidding.
So fee bidding is, in my opinion, the better of these options, although they all can work to some extent.
And the reason for that is that it's very space efficient and it's fully incentive compatible, where if somebody tries to censor you, it essentially works the same way Bitcoin works, where it's costly to censor somebody.
And in terms of space efficiency, as I already told you, what we're going to get it down to is one transaction per block.
So there's also regular `Merged Mining`, and I have to specify that this is actually better than regular `Merged Mining`, because with regular `Merged Mining`, what you need is you need Bitcoin miners to essentially participate and run the software and create blocks for you.
And here in this system, what I want to do is anybody can create a block and anybody can propose it to the miners.
And the miners just take whatever pays them the most, basically, in Bitcoin fees here.
So how that works out is that the mining is completely separated from the Bitcoin miners.
Anybody can do it.
And the Bitcoin miners just do their usual thing, where they just take the transaction with the highest fees.
We'll get into more detail about how that works later.
Just to give you a rough preview of what's going to happen, I'm going to give you a simplistic overview and then I'm going to go into the actual details, the technical details.
Either way, you'll get your answers.

## Fee-bidding BMM

Ruben Somsen: 00:07:20

Fee bidding, Blind Merged mining.
What's that all about?
Well you can at a high level imagine there being a unique location for a blockchain hash in the Bitcoin blockchain.
There's only one location.
If you want to utilize it, you'll have to outbid others for it.
So anybody can bid for this unique location by offering Bitcoin fees to the Bitcoin miners and whoever pays the highest fee gets their hash included.
So it's an auction and the auction winner gets the block and therefore gets the block on this other spacechain that they have created, presumably through this Blind Merged mining process.
So the original idea, as far as I know, is from Paul Sztorc.
And he basically, the way he had envisioned it, it requires a soft fork.
And what I've come up with here is a way to kind of avoid having to do at least a specialized soft fork.
So you don't need a soft fork that literally is only in order to enable Blind Merged mining.
You can even do it without a soft fork, but there are some sacrifices and we'll get into that later on.
But this kind of means essentially that now since there's no longer a specific soft fork required, it's kind of inevitable.
This is going to happen.
So just to give you a better idea, let me show you with some pictures.
Imagine the Bitcoin blockchain and this little pink blob is this unique location that people have to bid for.
It's a hash and the hash refers to a spacechain block.
The way consensus works is just the next Bitcoin block comes in and then there's also another spacechain hash in there and referring to a spacechain block.
What's important to note here is that this blockchain can fork separately from the Bitcoin blockchain.
So how that works is as follows.
Here for instance another block 2 is found block 2b and it's mining on top of block 1a.
So now you have a fork, both are length two, but we don't know which the winner is.
And the winner is simply determined by literally which is the longest chain.
So once another block is found, now we know the winner, 2a is orphaned and 2b is essentially the winner.
Of course, this could change again, but assuming consensus just moves forward, this is now the state of the network.
So, one way of looking at this, and I think it's an important abstraction, is to say that this is essentially like a single use seal.
And a single-use seal is a concept or an abstraction, an idea that was thought of by Peter Todd, where it's essentially the idea is that every UTXO on the Bitcoin blockchain is like a little box that you can open once, you can take out the content, you can put it in other boxes, but it's single-use, right?
You can only open the box once.
And here we have kind of a similar concept, except that the box is not opened by whoever holds some kind of private key, but it's a box that literally can be used or closing the seal in this case of the analogy by whoever pays the most to the Bitcoin miners and Bitcoin fees.
The reason I want to point that out is because right now, I'm using this for Blind Merged mining, but that's not necessarily the only use case.
There are other ways in which this can be used as well, and I'll leave that to your imagination.

## Equivalent to PoW, except...

Ruben Somsen: 00:10:42

Roughly speaking, this process of having this unique hash and having people bid for it is roughly analogous to proof-of-work, except there are a few changes, a few differences.
And they're relatively minor.
So first there's no difficulty issue you might've noticed.
But it's not entirely true.
Difficulty is actually inherited from Bitcoin.
Because the Bitcoin blockchain ensures that can only be one unique hash every 10 minutes.
So this is essentially how the difficulty works out.
And all the fees that go to the Bitcoin miners, they're also turned into proof-of-work.
So they are part of the difficulty algorithm, essentially.
So there is no difficulty in the Blind Merged mining side on the spacechain, but there is an actual kind of difficulty that is inherited from the Bitcoin blockchain.
So the second thing is, well, the highest bidder always finds the block.
And that is somewhat different.
It's kind of like, how would I say it?
It's like hashing power is just like anybody can mine with any kind of CPU, for instance, where it's relatively easy to go to Amazon and rent a bunch of hash power you can just take over blockchain.
It's kind of like that, where as long as you're willing to pay the most money, you get to create the block.
But it is still competitive.
So in that sense, it still works.
And the interesting thing is that every user is essentially a miner, as long as they have some bitcoins and are willing to pay some bitcoins to create a block.
So it creates a very competitive ecosystem.
So forks are possible, but they play out sequentially.
As we saw in a couple of previous slides, essentially, if you remember block 2a, block 2b, when block 2b is created, block 2a is not being built on top of.
It's not possible because there's only one unique hash where a block can be put.
So even during a `reorg`, let's say you want a hundred block reorg, that means that the chain basically stands still for a hundred blocks.
And that's actually a good thing because it makes the `reorg` more difficult.
I think of like low proof of work blockchains, where out of nowhere, suddenly 100 blocks can appear and be the longest chain and you're just screwed, right?
Like there's suddenly there's a `reorg`.
And here at the very least, you see it coming.
You can respond by trying to build on top of the currently longest chain by paying higher fees, et cetera.
So I think game theory wise, it actually works out a little better in favor of having consensus move forward.
So this is also kind of funny thing, but the minority soft fork, or even a minority hard fork that is trying to utilize the same unique spot can't survive because the only blockchain that will appear is the one that pays the most money, the most fees to the Bitcoin miners.
So if you have two blockchains that are trying to compete for the same spot, the highest paying one simply wins.
This can be good or bad depending on how you look at it.
There's always a way to hard fork out of it by just picking a different unique spot.
It has to be a unique spot, but there can be multiple.
And finally, this also needs to be pointed out, is that you have to validate the parents, right?
Or the parents, even, if you have a spacechain inside of a spacechain.
And the reason for this is that the parents is basically where the fees are being paid.
And there's actually one more step that I'll get into later that makes a spacechain a spacechain, which is the perpetual one-way peg and that requires also the parents to be validated.
So the main thing that is preserved here is the censorship resistance.
Miners lose income if they try to censor anything.
If they don't want to put your Blind Merged mine spacechain block into the blockchain, they can do so, but if you're the highest paying person, they are losing fees.
If they're losing fees, they're not competitive against other Bitcoin miners.
So it works out exactly the same in that sense.

## Paying for Block Space

Ruben Somsen: 00:14:36

So that brings me to paying for block space.
Okay, so we've got this blockchain now and we have a mechanism, Blind Merged mining, to create these blocks.
But now we still need a way to pay people, to pay miners to put your transaction in, right?
We don't have a token yet.
Similar to what I was saying about Bitcoin and where that was quite the innovation that you could use your Bitcoins to pay fees.
How do we pay fees here?
So what are our options?
Well, the simple but rather silly solution would be to create an altcoin right and as I said earlier, we don't want to do that.
So that's a no-go 
A cool but way too complicated idea, maybe someone can think of some way of doing this properly, but it is, I can tell you it's quite difficult, is `pay out of band`, where you essentially maybe pay over the Lightning Network or something along those lines, and then your transaction, you know, you pay the miner and the miner adds the transaction.
But the problem with this is that it's very difficult to make it so that these two are kind of synchronous, right, where there are multiple miners and now how do you know which one to pay?
How do you know that after you pay them, they actually put your transaction into the block?
And these are all problems.
So long story short, it is at least as to my current knowledge, too difficult to make this happen and not really practical.
So that brings me to the third and final solution, which is burning your Bitcoins.
And this is actually an old idea that I kind of like brought back to life.
And it turns out that it works better than you might expect.
So let's get into that.
But before, I just want to say that because we don't have a new token being created, we don't have a block subsidy.
So the reorg incentives are different than how it works out with Bitcoin, right?
With Bitcoin, we still have a block subsidy, but once that goes down to zero, now the reorg incentives are a little different.
So we basically run into that problem sooner here.
And that's important to point out.
It's not a trivial problem to really ensure that the blockchain moves forward, but it is definitely a solvable problem.
So at the very least, it's not a showstopper.
Okay, so the burning Bitcoin part, which I call the perpetual one-way peg.
One-way peg meaning as opposed to two-way peg, you can move your Bitcoins to this other chain, but one-way so you can never move back, which is why it's a burn, right?
You destroy your coins and you get some spacechain tokens.
And it's perpetual, meaning that you can always do this.

## Perpetual One-Way Peg (P1WP)

Ruben Somsen: 00:17:19

So for every Bitcoin you burn, get a spacecoin.
This preserves the 21 million limit, essentially.
So that's great.
There's not, you know, seeing the whole spacechain plus Bitcoin ecosystem still preserve the 21 million limits I think is a very important aspect of this right where there is literally no inflation.
So this is important to note as well which is that Bitcoin is always the superior asset it's absolutely not a competitor If you move from Bitcoin to some kind of spacechain, now you're stuck in a spacechain.
You can't go back.
But if you just hold your Bitcoin so you do nothing, you can always move to a spacechain later.
So that's always the superior option.
There is really very little incentive to actually burn your Bitcoins and move over.
But there are some which I'll get into.
The token essentially has only one use case and that's what I wanted to say, which is that you only use it to pay for block space.
That's literally the only use case.
So the way that works out is that you essentially, you burn a few Bitcoins or Satoshis, whatever, get some space Satoshis, spacecoin Satoshis, and those are the only thing you use to pay for fees, pay for block space.
And I'd say the most important thing here is that there's really no meaningful speculation you can do with this token.
It's never going to be worth more than a Bitcoin, so why would you speculate on it?
Why would you move over to this chain more than you actually need?
So what's most likely going to happen is that you're just gonna see roughly how much block space demand there is.
So let's say there's I don't know one Bitcoin worth of block space in terms of fees every couple of blocks or something like that, then there really will be only one Bitcoin burned in total and that will be sufficient to pay for all the fees for everyone essentially on this chain.
And it's going to be kind of a loop, right?
Where the Blind Merged mined, spacechain miners, they get the fees and they sell the fees again and you can use them again, et cetera.
So that's kind of where you have your, you know, either through the Lightning network or whatever, when you need some spacecoins to pay for fees, you just buy them or you just hold a little amount, like $5 or $10 or whatever, depending on how popular the spacechain is and how high the fees are.
So that actually, because it's so uninteresting to speculate on this token, it actually creates a lot of stability for the token.
Where the only way the token kind of loses value is there's a lot of demand for block space, and then demand for block space goes down again.
Then the token goes down in value a little bit, but even that's not too important or too problematic because you're not supposed to be holding a lot of these coins, right?
So maybe you had 10 bucks worth of the spacechain coin.
And then okay, now you have five bucks.
Okay, yeah, it sucks.
It's not great.
But you can still utilize the chain for its utility.
Nothing is really lost except for like a little bit of value, which was not supposed to be worth much in the first place.
Fernando Nieto, or Nieto, I'm not sure how to pronounce it, he wrote an article which is called Soft pegged sidechains, where he goes into some more details, and I also post in the comment section.
So if you're interested in kind of topic of how to maintain the peg stability at least somewhat you can you can find more information there 
So and this is important to note.
There's a real limitation here, right?
Like this is not a token where you're gonna store your value It literally cannot act as a Store of Value.
You'd be crazy to move in a million dollars into a spacechain and expect to get your value back somehow when you sell the token to a third party.
That's never going to happen.
Really, so that is the one limitation where the only use cases for these chains are things that do not require you to have a Store of Value on there, or decentralized Store of Value I should say.
So that might raise the question, well what are these chains good for if you can't store value?
Well, we're going to get into that.

## Why Burning Bitcoin Is Not a Problem

Ruben Somsen: 00:21:34

But first, I want to mention that I think a lot of people have this feeling where, wait a second, you're asking me to burn my Bitcoins?
That really feels bad, man.
I don't want to burn my Bitcoins.
And yes, I understand the feeling, but it really isn't bad is all I can say.
It's a feeling and you should get over it because it's not logical and I'm going to explain why.
So first, the alternatives are worse, right?
You could have some competing altcoin if you prefer, and then you don't have to burn your Bitcoins, but now you have to sell your Bitcoins to get the altcoin.
Is that better?
I don't think so, because that's not a chain you want to use, right?
You don't want to use Ethereum, you don't want to use Dash or whatever.
You want kind of the value and ecosystem to be with Bitcoin.
And that's really kind of a key thing here that this whole idea is trying to accomplish where it's supposed to build the Bitcoin ecosystem, not create competitors for Bitcoin.
You could also have some kind of trusted IOU token.
You know, You could have used the Tether chain or something, and I have an example of that later on in the presentation.
But that runs into the issue of that you're trusting an entity, right?
And that's the whole thing we're trying to avoid here.
We're trying to be trustless.
So these are not better alternatives.
There really isn't an alternative, actually.
This is really as good as it gets in terms of avoiding these much more massive problems.
So second thing that unfortunately isn't obvious to everybody who hears this, but you don't have to burn your bitcoins.
Somebody has to burn their bitcoins.
And then once that happened, they can sell those tokens, those spacecoins to you.
So you can buy them from somebody who already has spacecoins or buy them from spacechain miners who receive them whenever they create a block, and that can be sufficient.
So it's not necessarily that everybody burns some Bitcoins.
It just needs to happen to a certain degree so there are some tokens on this chain, and then that's sufficient.
And so this is something I mentioned already, but it's good to repeat it, which you really only need to burn as much as there's block space demand, right?
There's one Bitcoin demand, one Bitcoin worth of demand, basically, then only one Bitcoin needs to be burned, that would be sufficient, there's going to be some friction in the system where obviously you're not gonna get, you know, you create a block and then the miners get the spacecoins and then they sell them on the market again and the next block appears.
Maybe it's possible to get to create really efficient markets where that happens instantly, I don't know.
But my guess is that, you know, there's going to be a little bit of friction there and people are going to hold on to some of these spacecoins a little bit, but not to a massive degree.
And finally, it's just good.
I mean, what this means is that other people are going to be burning their Bitcoins, which means your bitcoins are going to be worth more because they're more scarce now.
So really, it's good for Bitcoin, right?
If half the bitcoins disappear tomorrow, it means your Bitcoins should be worth twice as much.
And that is how that works.
So really, there is no downside here.
You don't have to burn your Bitcoin.
Somebody else can do it.
There doesn't have to be a lot of Bitcoin's burned.
And if Bitcoins are burned, I'm not complaining.
I think it's great.
More Bitcoins for me, basically, in terms of relative value.

## Use Cases

Ruben Somsen: 00:24:48

So that brings me to the use cases, and that's not an unimportant thing, right?
So, so far I've talked about this.
Okay, so we've got a blockchain, but it can't store value.
There's no two-way peg.
So what the hell is this good for?
And that's a really good question that maybe I should have answered a little sooner, but I'm answering it now.
And I think the main use case, or at least the one that I think connects to the most people is essentially colored coins.
You could have colored coins with privacy features or something like that.
So asset issuance.
So once you have this chain where tokens can be created, and these tokens can be anything, they can be rare Pepe's, they can be whatever if you wanna do security tokens or something, I'm not a big fan, but sure, go ahead.
You can even create a token that is a federated two-way peg where it actually represents Bitcoins.
But obviously there's a trust involved there where whoever issued the token is actually promising you that you're going to get a Bitcoin for the token, similar to the Liquid network.
But, you know, it's possible.
And people can use it in that way, where you kind of have a hybrid of people issuing tokens on this trustless decentralized chain.
And then the tokens themselves might not be fully trustless, but that's up to you to decide whether or not you want to hold that token.
And of course, it can have privacy features.
It could be a Mimblewimble chain even, or it could be like Liquid where it has confidential transactions.
You could do decentralized DNS, and this would essentially replace Namecoin, where with Namecoin, you basically have the functionality of decentralized DNS.
But I think the existence of a speculative asset inside of a chain such as Namecoin is a problem.
And you're not to say that Namecoin had a better solution back then, like we didn't have a better solution to the problem.
So it's completely understandable that they created an altcoin.
But I think for today, looking at that, the altcoin only adds friction, right?
It only adds pumps and dumps, meaning that your coin might go heavily up, heavily down in value.
And you don't really want that, right?
You just want to utilize the chain.
You just want to tap DNS.
So the existence of the speculative token, I think is complete negative.
And we can get rid of that essentially and reissue something like Namecoin, take out the speculative assets and replace it with the perpetual one-way peg and use Blind Merged mining.
So even all the mining fees kind of go to the Bitcoin network as well, which also helps Bitcoin to become more resilient.
So then the third use case, and I think this one is a bit of a stretch but it might be possible I'm yeah I'm not sure it's weird which is low value payments right 
So essentially think of you know kind of the Bitcoin cash dream right where the idea was well we want our low value payments on the blockchain.
Blocks should never be full, transactions should always be cheap.
So you could do that, provided everybody is willing to hold like five to ten dollars worth of these spacecoins.
You know, not a lot of value.
You don't really care whether it goes down in value a whole lot, and then you use that to create small transactions, but on-chain, on a bigger blockchain that you don't have to use if you don't want, right?
It's an opt-in chain.
So it really provides kind of the Bitcoin cash use case.
The only thing that's questionable is whether the token really holds any value.
So you'd have to think, like, okay, let's say if you're receiving a lot of these microtransactions after a while, you have like 100 bucks of them, well, you better cash them out quickly, right?
Because it's not really a place where you just want to keep gathering and suddenly you have like thousands of these tokens because by the time you want to sell them and a bunch of people want to sell them, then the value might go down.
So you got to be careful there.
But I do think it works at least to a lesser degree for maybe really small payments as long as blocks are not full.
And you can maybe experiment a little bit with more dangerous chains that have way too big block sizes.
And then finally, you can have DAOs, you can have DeFi, you can have DEXs. I'm going to give a more specific example of what kind of use case you can have there.
But for DAOs, for instance, I know Bisq has a sort of like a colored coin DAO that's currently operating on top of the Bitcoin blockchain.
I think that's going to be a problem.
When Bitcoin blocks become fuller than they are now and transaction fees go up, something like that just can't exist efficiently in the Bitcoin blockchain.
And we'll have to move.
And I think this is kind of the place where we have to move.
And then the DeFi, the DEX stuff is kind of like the Ethereum use case or like the stuff that they're doing.
Some of that, I think, can be tied to Bitcoin through these chains and we'll get into that later.
So that brings me to the technical details.
So from this point on it's going to get a little bit more difficult to follow.
Hopefully you can still kind of follow everything.
I'll try to keep it as straightforward as possible.
At the end of the presentation, I'll give you a couple more use case examples, a little bit more practical.
Please stick around for that.

## Under the hood

Ruben Somsen: 00:29:57

Under the hood, first a few technical things, and then I'll show some pictures, so bear with me.
Essentially, what we're creating is a sequence of transactions.
They're enforced by a covenant and there's a relative lock time of one block.
So you just have a bunch of transactions and one transaction per block can get into the blockchain.
We use `SIGHASH_ANYONECANPAY` plus `SIGHASH_SINGLE`.
What this does is that we have this kind of input and outputs that marks the covenant and then we have other inputs and outputs that come from users that they can add.
And they add them to pay for fees, and they add them to add their blockchain spacechain hash, basically attach it to this transaction.
It's RBF enabled, and that means that anyone can pay for inclusion.
So you have to basically outbid each other.
And that's how we get the fee bidding.
And yeah, so the spacechain block hash can be committed in the added output, but we can do this through basically the equivalent of the taproot commitment.
It doesn't have to be exactly the same, although it could be.
And what that does is that basically even the hash doesn't appear on the Bitcoin blockchain.
So that saves another 32 bytes.
It's not absolutely necessary.
You can also just use an OP_RETURN, but it's more efficient.

## Covenant Transaction Structure

Ruben Somsen: 00:31:18

So there will be even more details later, but here are some pictures.
Imagine a transaction here with a covenant input, a covenant output, and we'll get into the details of the covenant later.

## A user adds their input/output (RBF bidding)

Ruben Somsen: 00:31:28

The user adds their inputs and outputs, and through RBF bidding, essentially, this determines who gets at their input and outputs.
So let's say you put one Bitcoin as a user input and then 0.95 as a user output, that means you paid 0.05 Bitcoin as a fee.
Then somebody else comes along and they pay 0.06, which is higher.
Therefore, your transaction doesn't get in, but the other guy's transaction does get in.
The highest one, let's say 0.06, gets mined into a block.
Now, with the user output, they reveal their taproot commitments to the peer-to-peer network of the spacechain, including the whole block itself, and that's basically how the spacechain block comes into existence.
In the spacechain block, there is a user coinbase, which is where they aggregate their spacechain fees so they get all the fees on the spacechain and that that decides basically how much they're willing to pay on the Bitcoin side.
So in this case, 0.06 Bitcoin means that on a spacechain, they should have received roughly the equivalent of that.
So once the next block is created, it's exactly the same thing.
Same covenant.
The covenant is also connected.
So the covenant output is the covenant input for the next transaction, and everything else is exactly the same.
So it just repeats over and over.

## How to do the covenant

Ruben Somsen: 00:32:56

So that brings us to the question to how to do the covenant.
So there are a couple of ways of doing it.
So one way would be kind of a trusted setup and this would use Child Pays For Parent.
The nice thing is that this trusted setup works today.
I say trusted in quotes, because basically what it is, is where you have the covenant input and outputs.
You could just have a private key and you could put a signature there and you could then after you created a bunch of signatures and all of these transactions like 10,000 or a million of these transactions you just throw away the private key with which you created this sequence of transactions, then assuming you really did throw away the key, it is as good as a covenant.
But that's where the problem is.
You don't know if the key was thrown away.
Well, the nice thing is it doesn't matter a whole lot.
It's not a good thing and there are better ways of doing it.
But if you want to do it without a soft fork, then that will be the way.
The downside is that, let's say, that person didn't throw away the key.
They can then basically fork this sequence of transactions.
And what that means is that the chain just halts.
Nobody loses money, there's not going to be any reorgs or something weird like that.
The chain halts and then a hard fork has to occur to restart the chain.
It's not terrible, preferably this doesn't happen, but nobody loses any money essentially.
So that's why I think it's acceptable to do it like kind of as a first step.
But we can do better.
So one of the better ways would be `OP_CHECKTEMPLATEVERIFY `.
This would also require Child Pays For Parent, RBF as well by the way, both of these, but Child Pays For Parent as well.
And while that is one way of doing it, and this is a Jeremy Rubin's idea.
So this is a soft fork that is kind of in the works that may or may not come to Bitcoin.
I think this is absolutely a perfectly fine way of doing it, but my preference goes to using `SIGHASH_ANYPREVOUT`.
`SIGHASH_ANYPREVOUT` is actually a soft fork that is, I think, maybe slightly more likely to make it into Bitcoin or might come to Bitcoin sooner than `OP_CHECKTEMPLATEVERIFY`, but who knows.
And it's actually intended for kind of improving the Lightning Network through something called `eltoo`.
And It actually turns out that for this specific covenant that I'm trying to create, it is slightly more flexible than `OP_CHECKTEMPLATEVERIFY`.
So `OP_CHECKTEMPLATEVERIFY` and `SIGHASH_ANYPREVOUT` turns out they can do roughly the same thing.
`OP_CHECKTEMPLATEVERIFY` is usually the cleaner way of doing it.
But in this case, I think there's an argument to be made for `SIGHASH_ANYPREVOUT` because basically the transactions become a little smaller and things are a little bit more flexible and we'll see that in a minute.
So I'm going to go and take you through the `SIGHASH_ANYPREVOUT` method of creating this covenant.

## Pubkey Spend Transaction (nothing special)

Ruben Somsen: 00:35:49

So I'm starting really simple here.
And I guess I should note this `SIGHASH_ANYPREVOUT` was not intended to do the covenant, but it just turned out that it happens to enable this.
So it's actually kind of cool.
And this is something that Anthony Towns taught me.
So yeah, I'll take you through it, kind of how it works.
So imagine just a regular output, a very simple one where there's a pubkey and a CHECKSIG
So the way to spend this would be with a signature, right?
So when you spend it, you just put the signature in the input script and the signature signs the transaction signing and the transaction it's creating and the previous transaction is trying to spend, essentially.
So what happens if we take the signature and we just move it, right?
We just move it to the output script.
So there is a problem here.
This doesn't actually work if you just do this.
And why doesn't it work?
Well, there is a circular reference here, right?
As I told you, the signature is signing two things, and basically the red bars you see here is what it's signing.
So it signs a new transaction, but it also signs itself.
That becomes a circular reference.
The signature itself is signing the signature, and that doesn't work.
The way to solve this is, well, that's exactly what `SIGHASH_ANYPREVOUT` does.

## Covenant Transaction with anyprevout

Ruben Somsen: 00:37:16

What `SIGHASH_ANYPREVOUT` does is it allows you to skip signing a transaction ID.
You're not signing the actual transaction that you're spending, you're just assuming that they fit.
With this, we've basically solved the issue, the circular reference.
And now it actually works out, where you already have the signature of the next transaction in the previous transaction.
And that makes it a covenant.
So now that it's a covenant, we don't really need K there.
We can just replace it by G.
G is the generator.
It's just basically your private key is one.
That's what it means.
So there is no real private key there, but in order to stay compatible with how Bitcoin works, we do need to have a key there.
So the key is just private key one.
Great.
This makes creating the signature really easy because it's basically just a hash plus one.
There's no calculation needed at all.
Yeah, this just works essentially.

## Sequence of transactions (pre-generated)

Ruben Somsen: 00:38:15

We just create a sequence of transactions like this with the signature already in the outputs.
That means that it's already determined what the next transaction is going to be, and that's how the sequence is created.

## Users Add Input/Output via Anyprevout (RBF Bidding)

Ruben Somsen: 00:38:30

And from this point on, we add the user input and user output.
And the nice thing is that the `SIGHASH_ANYPREVOUT` does two things.
Because the TXID is not signed, it also means that the TXID doesn't change when a user adds their input and output, or rather it does change, but it doesn't matter.
It doesn't invalidate the signature.
That works out perfectly.
Here, it's important to note that the user input does sign the entire transaction and doesn't do a `SIGHASH_ANYPREVOUT` or something like that.
The reason for that is, well, yeah, I'm not sure if that matters specifically, but what you need is you need to make sure that the entire sequence of transactions can be replayed so that people who were bidding but didn't get into the blockchain then still get into the blockchain, but in a way that's not actually a valid block.
So that's not possible because the entire transaction is signed.
So the TXID at that point for at least the user input and output is basically determined and cannot change.
So this prevents further malleability.
So the spacechain hash is basically the change output so you can think of like a taproot output where instead of taproot commitment there's also a spacechain hash that needs to be revealed at some at some point and this basically lowers the the burden or moves the burden of revealing a hash onto the spacechain side and makes the impact on the Bitcoin blockchain as minimum as possible.

## Minimum Viable Spacechain

Ruben Somsen: 00:39:58

So, that brings me to describing what essentially would be a minimum viable spacechain.
So if you wanted to create a spacechain, what's the minimum amount of work you could do to get it to work today?
So I would say you take the Bitcoin code base, and you introduce some minor changes, relatively minor.
The first change you have to make is the proof-of-work.
You take the proof of work and you just keep it, but you just make it so that any amount of proof-of-work is valid.
Nobody actually has to do any proof-of-work to create a valid hash.
It's just difficulty set to zero.
So then on the Coinbase reward side, you have to do two things.
One is the regular thing you always do, which is you just take the spacechain fees, which is fine, right?
There's a token in this instead of Bitcoin, it's spacecoin.
If there are fees, they go into the Coinbase.
That's absolutely fine.
But then the second thing you have to do is you have to take however many Bitcoins were burned on the Bitcoin blockchain.
And the way this works is that you would just introduce that into this transaction structure here, where you add another output with an OP_RETURN.
OP_RETURN doubles as a way of burning Bitcoins.
And however many Bitcoins were burned inside of this transaction, yeah, they basically become a Coinbase reward on the side of the spacechain.
And then since we're using the OP_RETURN for burning anyway, and it's a little bit easier so you don't have to reveal the hash, although you might as well do the hash reveal thing, it just makes things more complicated.
We're talking about an MVS, a minimum viable spacechain here.
You just use OP_RETURN to put a 32-byte hash there.
Not the most efficient thing, but it's the simplest way of doing it, essentially.
And then finally, since we don't really want to wait for soft forks, and that's something we've seen, right?
Soft forks are taking quite a long time to activate.
So instead of waiting for them, I suggest we just use the trusted setup today.
Even though it's not perfect, it's good enough.
The worst case scenario is that the chain halts and has to be hard forked to be restarted.
But it's not terrible, and it only happens if the person who created the sequence of transactions doesn't throw away their private key, which I think is also, there's not a whole lot of gain there to keep the private key.
So it can be acceptable.
It's not ideal, but if we want to get started today, that's how we have to do it.
So for this reason, I think it's good to show you what this kind of like trusted setup method looks like.
So this is what it looks like.
I'm not going to get into detail, but essentially, instead of having one transaction in the Bitcoin blockchain, you now need two transactions.
The second one, Child Pays For Parent, the first one and the second one can be RBF'd.
That's roughly how it works.
So it's the same thing, it's just more transactions.

## USDT DEX Spacechain

Ruben Somsen: 00:42:55

So that brings me to kind of a more, I guess, elaborate example, right?
So I've given you an example here of a minimum viable chain, but that's sort of boring.
So let me give you a little bit more of a spicy example.
So this will be a USD Tether or whatever, whoever wants to issue USD, can be anyone, kind of a DEX Spacechain.
So the first thing to note is that, and this is something kind of interesting that Sjors Provoost actually mentioned to me, and yeah, I hadn't really realized until he pointed it out, but if you have a spacechain that is specialized in existing for the use of one single token, like USD Tether, then you don't actually need to perpetual one-way peg.
Right, it's not perfect in the sense that, okay, so you have this token that's not trustless, so the whole chain is kind of not entirely trustless, but you still have this...
The way the blockchain moves forward is still completely...
That part is trustless.
So there's still a benefit to doing that.
So in the case of having a USD Tether chain, which is really exclusively for that purpose, you don't need the perpetual one-way peg, you just issue USD Tether and you use that to pay for fees to to the miners of this chain.
So then one thing you can do is you can create a Bitcoin derivatives covenant and this can be done trustlessly without an oracle and the reason for that is that, as I mentioned before, you, if you run the spacechain, you also have to run the Bitcoin blockchain.
And what that means is that you can have consensus in the spacechain, be dependent on what happens in the Bitcoin blockchain.
And that's really nice, because that allows us to kind of do something along the lines of a semi, like an atomic swap that is semi-native, but only halfway because it's only on the Bitcoin side.
And this allows us to create sort of a, you know, it's not quite a two-way peg, but it's a way to have a something that is like the value of Bitcoin inside of this USD Tether chain.
So I'll get into the exact details in a second.
So then once we have this USD Tether and we have these Bitcoin derivatives, at that point you can swap them out, you can just trade with those, you can create special trading contracts like what they do in Ethereum or something like that.
All that stuff.
So the Bitcoin derivatives covenant, what does it look like?
So here you can imagine a contract.
So this is going to be a transaction, right?
A contract representing, let's say one Bitcoin.
And for the current example, let's say one Bitcoin equals $20,000.
So Alice, who is basically the contract facilitator, and normally should receive a fee for that, but we're leaving it out for simplicity, she puts in half a Bitcoin worth of USD Tether, so 10k.
And then Bob, who actually wants to have this contract, he wants to have the Bitcoin, so he's the one paying the fee, he puts in 20k.
And 20k is exactly what one Bitcoin is worth.
So on the output side, there's 30k in total, obviously.
So the question is, who gets the 30k and when?
So the first condition is if Bob receives one Bitcoin on the Bitcoin blockchain and remember like I said this can be verified right.
The space chain is aware of what happens on the Bitcoin blockchain.
So if this actually happened and Bob received the Bitcoin, then Alice can claim the full 30K.
So she gets her 10K back and the 20K that was originally the price of the Bitcoin.
So the second way in which this can end up is there's a timeout.
So Bob never received his one Bitcoin and nothing happened and Alice was just lazy and did nothing.
Then Bob can get both the 10K, which is essentially collateral, plus the 20K he put in originally.
So he's 10K richer, essentially, depending on what the Bitcoin price is, but that's what the collateral is for, to kind of have enough there that even with a price swing of 50%, you're still fine.
So the third thing you could do, which kind of makes it more of a token, is that you can create a covenant out of it, right?
Where you can allow Bob to swap out.
So everything in the contract stays the same, but everywhere where you see Bob, now it says Carol, for instance.
So Bob can sell this contract worth one Bitcoin because he's going to get one Bitcoin towards the end of the contract.
He can sell it to Carol, and then everywhere where it says Bob, it now says Carol.
So that essentially tokenizes this contract.
Yeah and so one thing he can do is he can even sell it back to Alice right and then there's never Alice never actually has to give a Bitcoin because Alice just holds the entire contract at that point.
So because of that, it doesn't have to end up that Alice even gives a Bitcoin to Bob.
You can end up by just settling, which is kind of like the cooperative close in a Lightning Network, right, where you don't really want everything to play out.
You just want to agree that if it plays out, you know how it's going to play out.
So you just pay each other and you're done with it.
So one last caveat that I have to point out here is that there's a race condition, which is that Bob can transfer the covenant to Carol while Alice is paying Bob one Bitcoin.
And in order to prevent that, you actually need Alice to be able to first disable the covenant, whether you want to do that temporarily or not, that's a design detail.
And then at that point, then you give the Bitcoin.
And that ensures that this race condition doesn't occur.
So that's kind of a cool way of, even though it's not a real Bitcoin, it's still like Bitcoin, and some people call that a sidechain.
I don't think it should be called a sidechain when something like that happens, but you could call it that.
So it gives you a glimpse into kind of what is possible, and there's probably far more than I thought of that is possible because you can create any chain you want, and that's really awesome.

## Potential Future

Ruben Somsen: 00:49:03

Just to give you a potential future idea of where this could potentially be headed, and obviously I don't know, but this is what I imagine would be good for Bitcoin.
You have the Bitcoin blockchain, roughly two megabytes.
I know it's like 4,000 weight units or something like that, but roughly two megabytes worth of data.
So then you have a spacechain, which let's say utilizes the exact same code as Bitcoin does.
Reason for that being that we want people to feel secure in using that chain.
And then from that chain, you create your other chains.
And this is essentially to minimize the amount of Bitcoin space you use.
And maybe you create a big blockchain like we talked about with 32 megabytes worth of data or something like that.
And what you have here is on the Bitcoin blockchain there is only one transaction per block, right?
And that creates the spacechain.
And then from that spacechain, we have the exact same construction creating the big block spacechain.
So it's very efficient in terms of how much Bitcoin space you're utilizing here.
So then maybe you have a confidential assets spacechain, which maybe make it a little bit bigger because, I don't know, we feel like that's good enough.
In this chain, you can create your own assets.
They can be confidential, so you don't really see the history of it.
Somebody could issue a federated two-way peg on there if they feel so inclined, et cetera.
So then we maybe have to use the Tether chain that I just described, where you have some sort of DEX thing, allowing people to basically use USDT Tether to move in and out of fiat without using an exchange.
Then we might have some kind of experimental sidechain technology that does something weird where there's actually one chain that connects to some other chain, a bunch of other chains maybe in a way that doesn't require you to validate all the chains, only the chains you're interested in, but still somehow you have some two-way peg between them.
I may or may not be working on an idea like that, but that will be for another presentation.
And then maybe finally, you will have some kind of DNS chain where maybe it's like a .com or something where you store your URLs and you sell them onwards to other people.
And what you can do is you can kind of like, you can chain these chains.
And as I said earlier, what happens is that the children always have to validate the parents.
So DNS number three is kind of, you have to validate DNS number two and DNS number one and the spacechain in the middle and the Bitcoin blockchain, all of that.
So it becomes kind of like a lower tier DNS, essentially.
So you can think of maybe there's DNS all the way to the end that only Bitcoiners use or something.
And then DNS number one is maybe like the .com of DNS, something like that.
Whether that makes sense to tier it like that, I don't know, but I just wanted to show it as an example.
So that brings me to the end of the presentation.
So in summary, spacechains enable new blockchains that serve the Bitcoin ecosystem.
Hopefully I've convinced you of that.
And this is really something.
So I guess maybe it's good to end on a note and say that the way I look at Bitcoin is that it's a resource that is really scarce.
We have one block coming in every 10 minutes, it's only a couple of megabytes, not a lot of data can get in there, and we have to find ways to do more with that space, without just putting everything in a single blockchain, or without just adding trust to third parties.
So even though this kind of system with these blockchains, there are some limitations, I think it's a novel set of trade-offs where it is completely trustless, but it has some use limitations such as there not being a two-way peg and things like that.
But I think it's really where we have to go as an ecosystem.
And if not today, then maybe five or 10 years from now, I think having chains like this just makes sense, right?
Where it's completely trustless and you can move to them and you can do your colored coins there.
You know, take RGB, for example.
I think it's a really cool project, but it still utilizes the Bitcoin blockchain directly.
And as block space becomes more scarce, I think those kinds of use cases become priced out.
Right?
Where here you can create a, you know, let's say USD Tether blockchain, where you can still have cheap fees because you can even create 10 USD Tether blockchains if you wanted.
As opposed to doing USD Tether as a colored coin on the Bitcoin blockchain, where if you want to move your USD Tether, you have to pay really high fees because the Bitcoin block space is so scarce.
So that's roughly kind of my thinking.
My feeling is that we have to move towards things like this.
And that's also what motivates me to work on this.
So yeah, that concludes my presentation.
Thank you very much for listening.
If you're interested in talking more about this or just discussing it with me or whatever, please join me on Telegram at a channel I created called t.me/spacechains.
So you can go there, you can chat with me and other people who are interested in this on Telegram and maybe we can discuss kind of what this potential future for Bitcoin might look like.
Thank you.

