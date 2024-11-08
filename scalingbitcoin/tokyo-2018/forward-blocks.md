---
title: 'Forward Blocks: On-chain/Settlement Capacity Increases Without the Hard-fork'
transcript_by: Bryan Bishop
speakers:
  - Mark Friedenbach
---
paper: <http://freico.in/forward-blocks-scalingbitcoin-paper.pdf>

slides: <http://freico.in/forward-blocks-scalingbitcoin-slides.pdf>

<https://twitter.com/kanzure/status/1048416249791668225>

# Introduction

I know that we're running late in this session so I'll try to keep this fast and get everyone to lunch. I have presented at Scaling Bitcoin four times now so I won't dwell on the introduction. I wanted to talk about scaling bitcoin directly on chain in a way that is compatible with all existing node deployments.

# Goals

The goals that went into designing this proposal is that we are we want to be able to scale the bitcoin blockchain on chain in a way that an upgraded node will still be able to see the new transactions that occurred, even if there's some delay in receiving them. There are some highlights listed here on this slide that I think this can be done as a soft-fork to bitcoin and it dovetails int osome other useful additions to the bitcoin protocol. At best, this talk is a high-level summary. I posted to the IRC group for this workshop both the paper describing this technique and the slides. I encourage you to look at those links and look at it yourself.

# Definitions

First of all, everyone should know what a soft-fork is- it constrains what kind of block is valid. I am looking at forwards-compatible soft-forks, where a node which does not upgrade still has utility in being able to access the network and is not coercively forced to upgrade. No mandatory upgrades. There can be flag days, but it shouldn't block off access for old nodes.

# A note on centralization risks

I want to talk about centralization risks of a proposal like this. I break up centralization risk into two categories- one is the cost of validation, how difficult it is to process blocks coming in on the wire as you hear about them. Without introducing pairing crypto, you can't really reduce the cost of validation. You scale up linearly in size, then you scale up cost. The other thing we're concerned about is censorship resistance, which is your ability to get a transaction on the chain, which has a non-linear relationship with block size and interblock interval. We will try to trade off our deisgn in such a way that even if we increase cost of validation, we're going to make a smallest as possible decrease in censorship resistance.

# Dual proof-of-work

I was not thinking about scaling bitcoin originally, but instead a dual proof-of-work change where you introduce a new proof-of-work with a soft-fork. The first idea was add an additional proof-of-work algorithm. I am not proposing this, but it's a good place to start and thinking about this.

Suppose that you want to transition from an old PoW to a new PoW. You need both sets of miners to commit to where they want their reward for their block to go to, and you transition in proportion from the old to the new. Initially none of the fees and subsidy go to the new miners, but eventually it transitions over. If you do this slowly enough then the effect this has on mining income is comparable to just natural variance. It will be small enough that the bitcoin difficulty adjustment algorithm will adjust it; it has to be at least 3 years or greater. After that period of time, you would expect that the difficulty of a lbock from the perspective of old miners would be more, and they would all be difficulty 1 blocks.

# New proof-of-work, or merge mining?

I am not advocating for switching to other crazy PoWs. The change could be merge-mining, which is technically a change in your PoW, where you are evaluating something else. Either approach is possible, I don't make a recommendation either way.

# Forced hard-forks

The hard-fork bitcoin research group has a number of proposals they have been working on, and the one considered most safe is called "forced hard-fork" and some people call it an "evil fork" because while it's not a flag day hard-fork, you're cutting off access to the blockchain after the point of activation and suddenly the blocks are empty and you have to upgrade your node to see the extension block content. That's a good starting point for how I am going to construct my proposal.

What we do is we want to fix the two issues or couple issues that come up; you're able to increase the size of the extension block arbitrarily, but because those transactions are not visible to prior nodes, then typically these proposals might include a bunch of other changes like fixing bitcoin script. We're excluding those. We're envisioning that the extension block will only contain that the bitcoin transactions that would have occurred in bitcoin, even hypothetically if the hard-fork had not happened.

As we grow the size of the extension block, we end up relaying the transactions that get confirmed there on to the original network. So, there's a delay between when a transaction gets confirmed in the extension block and when it gets visible to the old nodes. The old nodes view of the block is not empty blocks, but instead transactions that were getting confirmed in the extension blocks from a long time ago.

We can use the timewarp bug to shrink the block interval. The idea is we call this a forward blockchain. This is a reference to forwarders in the military where forward observers of mobile infantry units scout the path ahead.

# Two chains, two separate ways to scale

There's two chains. There's the forward blockchain which scales by large blocks on a higher interval; there's a compatibility chain.

# Some annoying loose ends

If you're paying astute attention, there's some things that don't work. You can't repay the coinbases on the forward blockchain; you need to figure out how to fix this, get this out of the compatibility blockchain without replaying the blockchain. I've developed an approach for that. This slide just shows that we're not ignoring some of the problems here.

# Cross-chain header commitments

Instead of one block subject two proof-of-works, we'll fork after the point of activation and the forward blockchain will confirm blocks and the compatibility blockchain by some magic mechanism will observe those transactions and start adding them in sequence in the same order. The magic here is that the compatibility chain commits to the blockheaders that the miner knows about, when a block header reaches 100 confirmations then it becomes locked in. Even if a more-work chain is shown in terms of blockheaders, it will not reorg that forward block commitment. Vice versa, same thing happesn on the forward blockchain and both chains develop knowledge about what the tip is on the other blockchain. Once there's 100 confirmations, both consider the block to be locked in. When the compatibility chain locks in a forward-block header, they add all the transactions into the transaction processing queue, and then every block going forward has to include those transactions. It also adds the coinbase outputs of the forward block to an output payout queue and it's a requirement of the compatibility chain that the coinbases rewards are paid out from that queue. So the miner on the compatibility chain no longer selects transactions to include, nor do they select what happens to the coins that were generated by the block- they have to pick transactions from the queue, and outputs from the coinbase payout queue.

# One coinbase shared by two chains

In the opposite direction, when the forward blockchain confirms a block with 100 depth from the compatibility chain, the coinbase of that block gets entered into the UTXO set of the forward block. So now we have full transaction compatibility, even with coinbase mixing of values, you're sourcing from the compatibility chain which everyone sees even an un-upgraded node. You use the compatibility coinbase to synchronize payments based on the state of multiple chains is a common pattern we will reuse.

# Initial parameters of the forward blockchain

I am going to talk about how to restrain growth in a reasonable way. The forward blockchain has a target block interval of 15min, and I'll explain why. It's basically because it gives us a boost against centralization, using censorship resistance, and you have to increase the initial maximum weight to compesnate for 15minutes. We can also expand this with flexcap, which I presented at Scaling Bitcoin Hong Kong but now there's charts and graphs and equations. You allow the forward block miner to pick a higher or lower proof-of-work target and in doing so they are forced to increase or decrease the size of the block they are generating. Theyt are trading off subsidy and fee for having a block easier to find; this doesn't effect how you are sorting priority of blocks in terms of a lesser block in this context is still counting for the same amount of work. Every adjustment period, about 3 weeks, you adjust the base amount to an average of the past however many blocks you're considering.

The main takeaway from this graph is that it's non-linear, it's quadratic. It's easy to calculate, and for a given distribution of transaction fee in the mempool, there's a specific value that will make the most sense to use. That value swill cluster in its distribution near zero. If your mempools are empty, you go down the lefthand side of the chart and you can decrease your difficulty by 25% and reduce your block by 75%. Alternatively if you have areally full mempool, you can go to the right and increase your difficulty into a larger block as a result. It's responsive to demand +/- 25%.

# Timewarping the compatibility chain

I am going to talk about the mechanism for timewarping the compatibility chain. Read the slides later. It's basically that you have the timestamp field of the block be set by consensus, if there are transactions in the queue to be processed. The way in which it's set is you set it to the absolute minimum value if there are transactions still to be processed, unless the next transaction has some locktime keeping it from being confirmed, in which case you jump to whatever. At the very last block in the adjustment interval, you specify a value for the timestamp which is derived by running the difficulty adjustment algorithm in reverse: you know how much you want to adjust up/down in hashrate or the warp factor, which is the ratio of the forward block to the maximum compatibility block size, so you want to get an expectation every 600 second, run the difficulty adjustment algorithm in reverse, and that's your timestamp. You use timewarp, but you constrain it to satisfy the needs of the forward blockchain.

# Eliminate the "halvening" with a continuous subsidy curve

One of the things we can do is get rid of the halvening- I know there's mixed opinions on this. There's no reason that the bitcoin price should double when the subsidy drops in half. We can set a new subsidy schedule in the forward blocks, so long as it's roughly similar to the already existing subsidy schedule. The easiest thing to do is to just linearize it. You effectively make a series of short flat lines, so that the subsidy is continuous instead of having some shocks every few years.

# Multiple forward blockchains

Before we talk about the maximum limits, let's talk about mitigating decreases in censorship resistance. One of the methods is sharding. I am talking about database sharding, not the cryptocurrency sharding. Set your expectations at the door there. If we can have one forward blockchain, we could just as easily have 30, and source transactions from them separately such that each shard has its own UTXO set, and transactions are required to source its input from a single shard only. Stuff in one shard is not connected to what happens in other shards. There needs to be a way to transfer between shards, and there's some synchronization requirements, and it's the same mechanism we used earlier for the coinbase rules. You could use a native segwit output can be prefixed with a value indicating the destination shard identifier. This makes it unspendable on the forward blockchain. The nops would not be usable on bitcoin. These prefixed ouptuts are added ot the coinbase payout queue verbatim, and the value is claimed by the compatibility block miner and added ot the carry-forward balance. When it gets locked in on the compatibility chain, that output is added to the coinbase payout queue. When it finally does confirm the transaction, the "anyonecanspend" shard destination output is spent by the compatibility lbock miner and added into a fund that does the coinbase payouts. If you transfer between shards, you end up having to force corodination with a compatibility chain which requires an activation period so it's the usual process of syncing state nad it takes time. You cannot spend from anything that requires coinbase maturation because you don't know what the output is going to be ahead of time.

# The high end of scaling limits

So what does this give us? I said the number 28 shards, which was chosen in part because that's the max number of single byte that can be used in prefix bytes and in bitcoin script. But it's also the minimum that you could use for what you might think are a minimum for shard parameters-- some might think 32, a hundred might be reasonable, but other than that, you might get two shards coming in at once and because they overlap it would hog down your resources and cause them to take longer to validate and you get this cascade of too many shards coming in. I think the cutoff will be between 30 and 100. In this setup, you would have shards coming in about every 30 seconds in expectations. In each individual shardchain, it would be 15 minutes between shard blocks. They can each be up to 768 megaweight in size, and this gives you 14.336 gigaweight allowed of transactions to be processed every 10 minutes, which is about 11tx/person/day for everyone in the world currently alive. To prevent denial of service from premature growth, it is recommended that a gain limiter of +0.78125% peradjustment period to be applied, which results in a maximum growth of +14.5%/year. You constrain with a gain limiter the amount that you can adjust up or down, and there's a long series of digits there, it's a power of 2 percent you can move up or down on the adjustment period in the forward blockchain. This growth limit assumes that the mempool setup is that you're doing +25% blocks every single time, which is very unlikely. I'll note that these numbers are less than what is providing in bip103 which was a very conservative scaling proposal. As long as you have this limiter at the end, it grows very slowly.

# generalized ledger transfer mechanism

I am going to skip these last two slides, which show how to use the coinbase payout mechanism to implement confidential transactions, sidechains, and transaction expiry. I want those, and they would be good to add. If a transaction had its outputs expiring, it could get.. something.. coinbase payout queue. With that, I would go to questions. Thank you.

# Q&A

Q: What is the sharding?

A: In my shards, transactions only source inputs from one shard. Each shard is a separate consensus system. There's a mechanism for moving value between shards.

Q: Are these the same miners?

A: It has to be separate proofs-of-work for each shards. With traditional merged-mining, if you find a block it satsifies the others. You can reuse the haswork of a miner, but maybe it only solves for one shard but not another. Come find me at lunch.

Q: Does a soft-fork to fix the timewarp bug kill this proposal?

A: I had a discussion about fixing this off list, because there were exploits mentioned in that discussion. But it depends on what the soft-fork really does. In the timewarp domain, you limit how much you do in that. I had the flexcap gain limited to something like no more than 17% per period. You can do that kind of limitation in the timewarp bug fix. If you fix the timewarp bug in that way, then this would still work.

<https://www.reddit.com/r/Bitcoin/comments/9lqw2z/forward_blocks_a_proposal_to_increase_onchain/>
