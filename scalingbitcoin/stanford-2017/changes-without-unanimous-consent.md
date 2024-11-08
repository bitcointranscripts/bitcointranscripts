---
title: Changes Without Unanimous Consent
transcript_by: Bryan Bishop
tags:
  - soft-fork-activation
speakers:
  - Anthony Towns
---
I want to talk about dealing with consensus changes without so-called consensus. I am using consensus in terms of the social aspect, not in terms of the software algorithm consensus for databases. "Consensus changes without consensus". If you don't consensus on consensus, then some people are going to follow one chain and another another chain.

If you have unanimous consensus, then new upgrades work just fine. Developers write software, miners run the same stuff, and then there are no splits because PoW builds on other blocks and we're all happy and the economy is all in agreement as well and everyone wins. If everyone doesn't agree, you have a bit of a problem. You can have different sorts of disagreements. I would say that the disagreements are going to be more likely as bitcoin scales and grows, for a variety of reasons. Once bitcoin becomes big enough that governments buy in, then governments are going to have different goals to decide upon. There might be incompatible goals and disagreements, where disagreements don't have compromise, and then it ends up in chain split. This might mean segwit2x vs bitcoin cash or whatever.

We can have more subtle reasons for disagreements, like people who might not understand the impact of a change is going to be. So maybe some people think segwit2x or 4 MB is going to kill bitcoin and they're wrong-- they are still going to disagree on accepting those changes and even if they are wrong, their disagremeent can still cause a chain split and things like that. You can also have improvements that make bitcoin better for some people but some others worse off. The Bitcoin Core project tries to avoid that sort of thing but even then it's not always right. An example of this is ASICBOOST, and segwit makes ASICBOOST worse and some people are going to object about that as they did. Maybe you should only do improvements where everyone is benefiting- and perhaps it's impossible to do upgrades once there's too many people in the ecosystem.

As bitcoin grows, you get more developres maybe some of those developers are hopeless and they enter more bugs or something. Maybe you have more developers finding bugs in proposals and if you have a proposal that nobody knows about any bugs perhaps they accept it but once they find out about bugs they would reject it. And perhaps you hae strategic disagreements where you want to pretend to be against a disagreement where you establish a compromise and say please give me this change so that I can make a compromise and go ahead. And if you have those incentives to disagree, then you get more disagreements as well.

I contend that disagreements aren't going to go away-- we can't get everyone in the same room and give them nice treats and coffee and come to agreement. No, I think we will continue to have disagreements and those disagreements will result in a split.

Splitting is cheap. If you look at the Bitcoin Gold stuff, that's not $100's of millions of dollars to split a $100B economy. It's a few lines of code on github and a few press releases and a few developers spending time. Lots of people can do that. It's not a big ask. The cost is low the benefits high then stuff like that is going to happen. The problem is that the costs are kind of external... if the people who don't want splits, people invested in bitcoin and maybe they have lots of software that expects bitcoin to continue with its rules, their costs might be high and they have to change code, websites, legal agreements, etc. But it's someone else choosing to split the chain, and these companies have to react to it. So you can't really say Bitcoin is great as is, Satoshi was wonderful let's not make any changes, let's not do Bitcoin Script 2.0, let's not do signature aggregation what we have is great let's leave it... well someone can come along and say that's great, here's a new client with support for all the new things and a new proof-of-work and everyone gets free coins. One way or another, splits are kind of inevitable in that sense.

Uncontroversial changes are fine. There are a bunch of ways to do them. We have done uncontroversial soft-forks and they work fine. You can do a simple uncontroversial emergency hard-fork-- that might have been done in secret. You can do uncontroversial hard-fork and burry it for ages so that in 3 years we have 2 MB blocks or something. Or, you can have other approaches.

You can have contentious hard-forks and it ends up with a split. You can do a really quick hard-fork that doesn't necessarily work so great. Anyone who doesn't upgrade will be with a split and people won't be able to upgrade. You can have a contentious user-activated soft-fork where even if miners don't really support it, users activate it and you end up with a split.

So the argument is that splits are going to happen and you kind of want to deal with them.

## Decision makers

Who are the decision makers here? Developers, miners, users, regulators? Is it someone else? I don't think Core developers have a chance of making decisions here. In Linux, there's Linus. But in Bitcoin Core, you're not going to get that answer. Maybe different cryptocurrency implementations are going to have a developer lead, that's fine, but not in bitcoin.

Miners can make decisions especially if everyone wants to defer to what miners do. But I don't think most people want to defer to miners anymore. I don't think that miners are going to make decisions. But I might get proven wrong in a week or so.

Nodes enforce the rules but they are too easy to fire up replacements to actually give you a meaningful decision. So that leaves the economy and the market as the decider. I hope people are in favor of this. They are provide-- they are the reason why the miners, developers and nodes are operating. They are behind the developers in two senses. A lot of developers are interested in the philosophical reasons of bitcoin and that is going to help the economy in the first place, to make it free, more reliable, or make everyone rich in aggregate. If they are not in it for the philosophy then they are in it for the money and the economy is the one that ends up providing paychecks. I don't think you can run a bitcoin miner without getting some sort of immediate benefit from bitcoin, and it's up to the economy to buy and sell bitcoin to do that. And the nodes are also easy for the economy to fire up.

The way that the economy does things is that they buy and sell bitcoin for goods and services. They are the ones... the economy's power as such is that it sets a price for bitcoin in terms of US dollars.

## Changes

Someone proposes a consensus change like segwit to increase the block size, or bitcoin script 2.0, something that nodes will enforce and something that miners will hopefully check. There are two choices that everyone will make- either adopt the change or keep with the old rules. I am using n for the nobody changes situation, e for the eerybody changes situation, and s for the situation where there is a chain split. The hypothetical value of the original chain with old rules is a, new rules is b, and the other one is the greek letter. This is the expected probability and value of these things happening on the chain and sort of equation.

If you have that model, then you want to work out the values. If the highest expected value of bitcoin is a, and a > b, then choose a, and if b is going to be in more value then you want everyone to adopt the new rules. Maybe segwit is the example, maybe the new rules are going to increase the market price somehow. Does that make sense? I hope so.

## Trading coins

You want to find out these values. As a person you might not know, but perhaps the economy knows. The way that the economy expresses this knowledge is by assigning values. The way they do this is by having a market and trading these potential coins. So there are three sorts of way doing this for either coins that are-- unconditional, like what Bitfinex is offering for segwit2x. You buy a token if the chain with .... if the segwit2x chain continues on it's worth something, and you can also have options for refunds, like offers to buy segwit2x coins for 7:3 or whatever it is today, from Adam Back, and a refund if there's no split. And then there's a third case where actiation doesn't happen. All 3 of these can generate different prices.

We don't have enough equations to work out the unconditional values. All of the markets combined will only kind of give you conditional values. If you look at those values, like the bitfinex price of segwit2x you can't actually tell if that's a low price because the segwit2x coins might not be valuable, or it's because the market is saying that everyone is going to back off from the segwit2x thing and it's not going to happen at all. You can fix this by having a US dollar prediction market but then you have to do it in US dollars you can't do it decentralized on chain because you have correlation problems.

## Price discovery

If you don't have price discovery, before the split happens, you can get shocks in the price. In the Bitcoin Cash split, the price rose immdiately after by about 5%. That makes sense if people weren't able to move.

If you have a split, then there are many costs and they are mostly externalities. If you are kind enough to keep the proof-of-work, unlike Bitcoin Cash and Bitcoin Gold, then you can kind of estimate what the cost of split is going to be. It's expensive, maybe not crazy expensive, and again that only applies if you have the same proof-of-work.

## Making splits not horrible

So how do we make splits not horrible? We have 10 minutes. So this is a mini-talk. You want to have replay protection. You want your transactions for bitcoin only going to bitcoin and segwit2x only going to segwit2x, and don't give them unexpected bonuses tha tyou don't get to claim your value from. I argue that the main reason why segwit2x doesn't have replay protection is because implementing it would socially imply that they are not the real bitcoin. Bitcoin Cash implemented replay protection but they were an obvious fork. If Bitcoin Core isn't implementing replay protection, then why should segwit2x implement it? We want replay protection in place and forks this way and forks that way, everyone gets replay protection for free.

The obvious way to do this is to have transactions commit to a block in the history. After the split, say that block 500,000 is going to be such and such which has the segwit2x or the non-segwit2x forking block in its history. There's a bip115 that proposes how to do this, a new opcode to specify a blockhash. It makes double spends a little bit easier to deal with if you are doing zero-confirmation stuff. The downside is that it requires two transactions to split the coin. The first one has a scriptSig with a checksig and it has to evaluate that against what the block is.

Instead, I am proposing that we use the sighash signature stuff. Instead of a special opcode, we ould have an extra bit in the sighash, and an extra two bytes to specify how far back the block is that you're committing to. So if you want to specify 120 blocks ago you had this particular block, you put 120 in the signature. You set the locktimes, so that you have something absolute to compare it against, and then you just add the hash of the block to the hash that you're calculating when you're doing the signature.

You need to know the hiehgt of the chainsplit and the hash of the block that is forking. You can get replay protection, and you commit to the block. If you want to do both sides, you need to follow both chains and do those transactions. You get wipeout protection because you know the particular blockheight; you can do a checkpoint and not allow reorgs. You can do that with SPV and lite clients.

bip115 has the provisio that it only does a year's worth of blocks or so such that you don't need to maintain too many blocks, even for a SPV client yoyu can just ignore everything but the last year's worth of blocks and still securely validate scriptSigs. Also, signatures can be self-contained.

One of the drawbacks potentially with bip115 as specified is that a transaction if it commits to the blockheight or blockhash of whatever the current hash.. if that block gets orphaned then your transaction is invalidated, so if someone is trying to spend it as a zero-confirmation then their transaction tree is also invalidated, so you can add a consensus rule to block this situation as well.

So that seems to be great for replay protection but it doesn't lead to the price discovery. The betting with roger talk from yesterday, that replay protection is not sufficient for that.

## Tying transactions to soft-fork activation status (BIP commitments)

The other proposal, which is more complex, instead of committing to a particular block, you can commit to the activation status of the bip, using pretty much the same approach. Specify a versionbit, have a sighash flag to indicate that, it does require that any forks have a versionbit that you can indicate. Bitcoin Core has to set it to active or inactive. You could argue bip102 is segwit2x or something, so that's reasonably feasible in this situation to use a versionbit. The big challenge with this is that it potentially makes every upgrade a hard-fork. So your version 19 comes out with some user acceptance soft-fork and maybe everyone agrees it's a great thing and it's not controersial and then it gets activate.d You make a transaction that insists that it's activated.. and what do people running old ersions see, do they see the transaction as valid or invalid? Is the soft-fork activated or not? So this adds the complication that you have to track the implicit status of a soft-fork.. if you see a block wit ha unch of signatures saying that the soft-fork is activated, then you have to assume it's activated.

Miners could still confuse things, they could fit into a lbock and say that every bit is activated, and then they exhaust the space of bits. And then you exhaust the resources there... But you can add some complexity and say implementations need to update with some kind of regularity and once the newer version is expected to come out, they can't know whether their thing is inactive. In the 3, 6, or 12 months, then the implementation is... and no other bits can be activated and we're good.

Unknown bits would be rejected by all current versions of software. New bits would be allowed by software updates. They just need a delay of 6 months or so, between publication and activation. And of course hard-forks can change any rule they want.

The caveat is that ... for the two refund contracts, you need a refund in the event that a chain split hasn't happened. Perhaps you use discreet log contracts or cryptographic proof that there is another chain to a merkle transaction with a merkle path to the transaction that shows that the BIP is active or something. You need similar opcodes for this and it would take a fair bit of space. You could arrange ransom payments so that if someone tries to cheat and both blockchains have a reasonable amount of value then perhaps cheating becomes profitable, but at least within that tradeoff you don't need a trusted exchange to do this kind of trading.
