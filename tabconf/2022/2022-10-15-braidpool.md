---
title: Braidpool
transcript_by: Bryan Bishop
tags:
  - mining
speakers:
  - Bob McElrath
date: 2022-10-15
---
## Introduction

I am going to talk today about Braidpool which is a decentralized mining pool. I hope some of you were in the mining panel earlier today in particular p2pool which this is a successor to. I gave a talk a long time ago about a directed acyclic graph blockchain.

## Braidpool

Braidpool is a proposal for a decentralized mining pool which uses a merge-mined DAG with Nakamoto-like consensus to track shares. This was the most straightforward way I could find to apply the ideas of Nakamoto consensus to DAGs. It guarantees all miners get paid through this merge-mined alternative blockchain. It uses a quorum of miners and a large multisig (using FROST, ROAST or MuSig2) to sign coinbase payments or settlement transactions. Our ability to use that for large multisigs makes this possible now. It tracks owed funds through a "UTXO Set" which is actually a set of transactions (Unspent Hasher Payment Output). It targets constant variance among participants. Each ones have different targets, but we want to achieve the same blockrate for all miners. It also allows sending of shares which enables hashrate futures and options. This could be a terahash coin and you could send it to someone and get paid for your shares immediately or do futures and options on it.

## Outline

There are four different broad categories to talk about. I posted on twitter a while back about "general considerations" of these categories. You have to define what the shares are or the weak blocks, and then you need a braid consensus mechanism and I choose that because it's closest to bitcoin in spirit. You need a way to aggregate coinbases into a rolling transaction which is the payout update and then you have to sign something that actually pays everyone.

## Shares

In a decentralized mining pool, a "share" is a weak block: a full, actual bitcoin block that doesn't mean the bitcoin difficulty necessarily. You start with a bitcoin block, it doesn't meet the bitcoin difficulty target necessarily. This is the thing I have to communicate to all the other people in the pool: I'm working on this and if I had gotten a block with this, then you would have gotten paid. I am following the rules and you would have gotten paid had I won the block, and same for you to me if we are both participating in the pool. The payout transaction is a rolling aggregation of past payouts. There's some metadat and uncommitted metadata also in there.

## Share commitments

You have to commit to a couple things. There is an OP\_RETURN in the coinbase that commits to some metadata. It describes who mined it, what the payout address is for that miner, it has all the other metadata necessary to communicate with this miner. You need the IP address of the miner. Once you mine a block, you become a member of the FROST quorum for signing payouts so you need communication with that miner going forward.

## Share metadata

This block of metadata is hashed and committed to in the coinbase metadata. It's committed to in the blockheader and the coinbase has two outputs one is the OP\_RETURN that says braidpool and this commitment, and the other is an address. This address is a very large multisig address using FROST and Schnorr signatures.

Finally there's a little bit of uncommitted metadata as well. The point of using a DAG is that we want to run the blockrate as fast as we can and we want to make blocks as fast as we can. The problem with this is latency. We need a DAG so that we can multiple block producers at the same time. We need a good resolution timestamp. Bitcoin's timestamp field is poor, and miners sometimes roll it anyway. If I want to structure the measure of the graph, you need millisecond precision. When you give a blockheader to a miner, they often go away and compute for seconds or even minutes. Once it comes back, that timestamp is now 10 seconds out of date. With the DAG, I want to measure the latency of the network. In bitcoin, orphans are a measurement of how latent the block is.

The orphan rate itself and the presence of higher-order structures in the DAG are measurements of latency. To do that, though, we need better timestamps. I have added uncommitted metadata block which contains timestamps of the time it was broadcasted. There's also witness timestamp: when I mine a block, I also mention when I saw the parent blocks. This allows me to measure the latency of the network.

## Share value

Each share has a value. Many payment systems have been come up with for shares by pools like PPS which is pay-per-share. In other words, the pool describes a fixed price and you get a fixed amount per share that they pay you from a general fund. A decentralized mining pool, though, does not have an extra source of funds and the only funds come from the coinbase. So you take all the fees, all the coinbase rewards, and you proportionally allocate it based on how much work was done.

Well, how much actual work was done? In the same difficulty adjustment window, each block has a certain amount of work. In a DAG, it's a little more fuzzy. What happens when I get a graph structure that has a diamond in it? Is that the same amount of work as if I had put those serially? Can I just add them together? The answer is yes, if no orphans are generated.

Within a diamond structure like that, you have to ask what is the likelihood that an orphan was demonstrated? This equation on my slide is weighting the amount of work by the likelihood that an orphan was generated in the case that you had more than one block in a graph like this.

You can sum work, if you have linear blocks. If I have a diamond graph, how much work is that actually? It's a little bit non-trivial to figure out. This is just a Poisson distribution and it's the probability that I have two or more blocks in the time window in which these blocks appeared. These are DAG blocks that could have been bitcoin blocks.

## Share tally

The shares are the measure of work. They are a statistical measure of the amount of sha256d calculations performed. How much is that worth? That is actually known at the end of a difficulty adjustment window at the end of every 2016 blocks. At that time, you know how many blocks were mined by the pool and what the difficulty was. That sets the share price. Until that time, we don't actually know. So therefore we pay out every 2 weeks, instead of every block. So the pool will hold off until the price is known. The number of shares per price is changing, per difficulty adjust window. This allows us to make futures on hashrate and options and other derivatives on hashrate.

This is enabled by being able to send shares to a new address.

## Consensus (braid)

I need a consensus. This is an accounting system. I need to count how many shares each miner contributed and add them all up. Moving to a DAG allows you to get much faster block rate. DAG means that blocks have multiple parents. A block can refer to multiple parents. Acyclic means it's cryptographically impossible to decycle (it would require breaking a hash function). It's non-linear, meaning there's no height. It turns out that a DAG can be ordered in linear time. A DAG can be partially ordered in linear time.

We have to make a slight restriction on a general DAG. The restriction is that I cannot name any of my other ancestors as a parent. I am calling that a braid.

## Cohort

I have another talk about cohorts. A "cohort" is a graph cut, it's a grouping of the blocks in the DAG that can be total ordered. WIthin each of these colors here, the graph structure doesn't tell me in which order they appeared. Anything within one color block could be before or after any other item in the same color block. But when you see a color change, it means that everything to the right of it is a child of everything to the left. This is full consensus where everyone agrees; in times between, someone hasn't received some information, and we don't have full consensus.

## Cohort vs difficulty

This allows me to do some interesting things. It allows me to define a difficulty adjustment algorithm. Look at the cohort time on the vertical axis, versus target difficulty. As you can see, the cohort time goes up if I allow too many blocks to be produced at the same time the time to form global consensus goes up and that's because I have to have a quiescent period in the network where no blocks are produced and everyone receives everything. That's when you get global consensus, and that happens less likely by the Poisson distribution as the block rate goes up.

## Difficulty adjustment

There's a happy medium where you have the most often consensus points. There's a formula for this that allows us to define the zero parameter of the retargeting algorithm. For any given period of time, I can measure the number of cohorts, number of blocks in the cohort, the amount of time to form the cohort, and I can figure out what the block rate should be to achieve the most often number of consensus points.

## Miner-selected difficulty

Now that I know how many blocks I want to see and at what rate, I now want miners to select their own difficulty. The purpose of a mining pool, in principle, is to reduce variance. It would be nice if everyone had the same variance but bigger miners have less variance than smaller miners. The purpose of the project is to reduce everyone's variance. If we allow a miner to choose their own variance, they can create more or less blocks as long as it is in the window of difficulty. The software will choose difficulty such that all miners have the same variance. This is not enforced by consensus, you can go and change it, but there's no good reason to do that.

If everyone was mining on braidpool, you get to the lowest possible variance given the 10 minute bitcoin block time.

## Embedded braidpools

Miners even smaller than that can be grouped into a subpool. Instead of having the pool manage coinbases, I can copy everything about braidpool and do it again but this time instead of managing coinbases you can manage outputs in a parent pool. By having two braidpools like this, even smaller miners can operate on this other braidpool and allow arbitrarily small miners to continue operating with minimal variance.

## Conflict resolution

Braidpool will have a transaction system where it has a double spend problem. If you have two transactions that conflict with each other, then which one do you take? We're going to keep all transactions and all blocks. Bitcoin discards blocks in the form of orphans. It's the asymmetry of profit between orphans and main chain blocks that causes selfish mining. So we keep all blocks and transactions to resolve selfish mining in braidpool. But what happens if there's a transaction conflict?

I call it a simple sum of descendant work. I tried a bunch of algorithms but this one seems to work: sum all the descendants regardless of graph structure. The problem with graph structure is that it's manipulable and doesn't cost anything to manipulate the graph. What I want to know is how much work was added on top of a particular transaction, and that's the one I choose, and that's Nakamoto consensus. I sum all descendants, relative to graph structure, using the work which is the same as the share value.

This is only important within a cohort. I don't need the whole chain, I only need to look within the cohort to see what the work weight is. Anything further down the chain than that applies to all of its ancestors.

In the event of a tie, use the smaller hash for choosing which chain to mine on. Adding a transaction system will be a v2 system for braidpool; I want to get it working and distributing funds first before I start adding complex features.

## Payout update

How do we pay everyone? Every block produces a coinbase. I will roll up these coinbases. In addition to every coinbase in every block, there will be a transaction that consumes a coinbase from a previous block, adds it to a rolling sum, and rolls it forward. This is similar to the eltoo protocol which was published a while ago.

Here you have a transaction that has an "update" phase and a "settlement" phase. The update phase is the one we put into every block. In addition to this coinbase, there's this payout update that-- it's one output that has all the outputs from the pool. From that, it has a taproot spend that has the settlement transaction and that's what guarantees everyone gets paid.

I call this taproot payment the UHPO. This is the analog of the UTXO set.

## Settlement transaction: Unspent hasher payment output (UHPO)

This can be divided into multiple transactions if it gets too large, if necessary. The purpose of braidpool is to manage this one big transaction and that's the account that everyone shares. We have to sign and broadcast this in the event that braidpool is shutdown. But really this is an optimistic protocol; we never want to have to send this transaction, but if something goes wrong then we could and everyone can get paid. There are other ways to withdraw from the pool without having to broadcast this transaction.

## Payout signing

Next, we need to sign the payout - both the rolling update as well as the UHPO transaction so it could be broadcast if necessary. In the output, you need two keys: an update pubkey and a settlement pubkey. These keys are generated using the distributed keygen phase of FROST or ROAST. ROAST is basically parallelizable FROST. Within that, we need DKG (distributed key generation), and each one holds a share of the private key and together they generate a public key. The public key goes into the coinbase output. They do this for twice- once for the update key and once for the settlement pubkey.

It's really the advent of FROST and ROAST that we can do this. Within a 2 week window, we could have a bunch of different miners that can participate in making these blocks. So we might need to do a very large multisig because of how big that window is. FROST((?)) can do up to 50 signers before it falls down; we will probably have to combine MuSig and FROST in some clever way.

After a bitcoin block is found, it kicks off a signing ceremony. We don't sign in advance, we sign afterwards. This signing ceremony can happen out-of-band and off-chain.

## Derivatives and instant payout

One of the goals with this is to enable instant payout of shares. If you have a pool, the pool holds on to your funds and you sometimes withdraw your funds. One of the things people worked on for a while is using lightning channels to achieve instant payout. We can do that here, and the way it works is that you find a counterparty, you send them your shares and they send you bitcoin. This can be done by atomic swap or by lightning.

With the decentralized mining pools today, these are the entities buying shares. They also assume a risk management role. In commodity markets, Citadel does analysis like what should the price of futures and options be, and then they do market making and trading on those markets. Pools are currently kind of doing that. My goal with this work is that the pools actually use this because it gives them new options for risk management and they can do derivatives and allows them to reduce their variance to a level they couldn't reach natively.

These kinds of hashrate derivative instruments will be on the centralized markets or either private contracts. I am not building a DEX here. But by having shares as a transferable instrument, that's all that's needed for centralized exchanges to build markets for these instruments.

## Timeline

I am working with Kulpreet Singh on this and I invite others to work with us on this. I am using Jesse Posner's [FROST code from libsecp256k1-zkp](https://github.com/ElementsProject/secp256k1-zkp/pull/138). One of the targets we want to hit soon is latency optimization. We need to be able to send the blocks as fast as possible. BlueMatt talked a little bit about relay networks, like ones using fountain codes to send blocks around very quickly which will be needed to optimize braidpool like the bead braid and get the number of blocks on the DAG to be very fast.

## Conclusion

Now that we have [FROST](https://btctranscripts.com/bitcoin-core-dev-tech/2022-10-11-frost/) and [ROAST](https://btctranscripts.com/tabconf/2022/2022-10-14-roast/), and my prior DAG work, we can put this all together to get this better decentralized mining pool. This is kind of a straightforward evolution of p2pool which put the tally of who's owed into a coinbase transaction, but here in braidpool we keep this outside the coinbase. There's also a proposal from Chris Belcher that uses semi-trusted hubs for lightning to pay everyone. My goal would be to get existing pools to run atop Braidpool, and to have them use stratum v2 as well.
