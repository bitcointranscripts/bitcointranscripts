---
title: Elastic Block Caps
transcript_by: Bryan Bishop
tags:
  - research
  - fee-management
speakers:
  - Meni Rosenfeld
---
## Introduction

Thank you everyone. I am from the Israeli Bitcoin Association. I will start by describing the problem.

## The problem

The problem is variable transaction fees. The transaction fees shot up. There's a lot of fluctuation. To understand why this is a problem, let's go back to the basics.

## Block size limit

We can have big blocks or small blocks. Each one has advantages and disadvantages. One of the benefits of small blocks is that it's easier to run a node. There's two metrics for how to run a node. There's lower peak throughput, and lowe raverage/aggregate throughput. The main scalability problem is initial block download. Every node from now until eternity will have to download all the transactions if they want to fully verify the blockchain or in other words run the bitcoin protocol. Even if the network has an ability to use a higher max throughput, we still want the average to be as low as possible and we will save up on those costs. This is why the average throughput is the main performance metric.

I want to see how we can keep this fixed, while improving the other performance metrics.

## Mining gap

Assuming negligble inflation, if blocks are big enough to fit all transactions, then after a block is found, the mempool is empty, and there's no gain from mining honestly. Miners could stop mining and hten do a reorg to take the transactions. This is an actual risk to the network. It's not just that it's harder to run a node, it's also that it's a risk for the network if blocks are too big in the low-subsidy environment in the future.

## Varying network load

Too big and too small is relative. Hgh load means blocks are too small, and there's excessive fees with low usability. If we have low load, then there will be blocks that are too big, enough room for everyone, so fees nosedive. Transactions are included cheaply, not respecting externalities, and then there's the reduced miner payment and security, and then the mining gap I described earlier. When the fees are variable, there's difficulty planning personal economic activity, and difficulty planning network upgrades. Perhaps you personally plan to do an on-chain transaction in the future, but if the fees are too variable, then you can't economically plan for paying for your transactions.

If sometimes we need big blocks, and sometimes we need small blocks, then the obvious solution is why not both?

## Elastic block caps

The basic idea is that we have a variable block size. When the network load is high, we have a higher limit. When the network load is lower, then the limit is lower. Same aggregate throughput, and lower fee variability. The end result is that fees will depend on the load but they won't change as much. If we tweak the parameters right, ew can get the same aggregate throughput while reducing fee volatility.

## Related work

There's a lot of related proposals-- similar ideas like dynamic block limit, flexcaps, excessive size penalty, 2013 Nicolas van Saberhagen, CryptoNote, Monero, 2015-- Greg Maxwell, Mark Friedenbach, and myself. I won't go into all the details, but I will propose a new variant that I think works better than the previous proposals.

## What this proposal is not

This flexcap proposal is not a fire-and-forget long-term block size adjustment. This is not a solution to that problem. It's not based on voting, and it's not based on the actual size of previous blocks. The idea is that this proposal is elastic, not plastic.

The physical analogy should help build intuition here. Something is elastic when you apply force and it changes shape, and when you stop applying shape it returns to the original shape. Plastic is like playhdo, where when you stop applying force it remains in the same shape. A lot of the block size proposals have been plastic, not elastic, or things like bigger block sizes that get bigger without bound.

If the limit keeps getting pushed up when there's high load, then there's no limit that has any handle on the externalities or what hardware resources we need to run a node. I don't know of great metrics to solve this long-term problem, but whatever they are, they aren't elastic.

## Network load metrics

Number of transactions is not a reliable load metric. A trillion floating transactions at 0.1 sat/vByte is spam, not load. Load is when users are actually willing to pay and still can't get in. A good load metric is block inclusion threshold is equal to the minimal block fee rate.

What is the fee threshold for inclusion? What fee does the user need to pay to get his transaction included in the block. When the user needs to pay a high fee, then the network is loaded. At each block, I look at what is the minimum fee rate inside this block, and whatever it is, that's our measure for load.

## Elastic block cap

For each block, we look at the smallest fee rate inside of a block. We define some function where the block limit is some function of the smallest fee rate. We have a lot of flexibility with this, it has lower and upper bounds. I think the best option is a simple hyperbolic function using this formula on the slide.

((Isn't this vulnerable to a miner mining a single block with a super-high fee rate and then stuffing the next block with a billion gigabytes of data?))

This system is not much different from the current system.

## Gameability

How is this gameable. I do believe it's almost not gameable at all. If the miner tries to put in his own fake transactions with the fee that is higher than the minimum, it doesn't help him in any way. If he puts a lower fee, then it just helps himself, it just reduces his allowed block size limit. If he puts a higher than minimum transaction, then it doesn't change the minimum. There is no benefit from out-of-band payments. If a miner tries to include a transaction that has a low public fee, but the user pays the miner out of band. It's possible to do reverse out-of-band payments, where the user puts in a high public fee, but gets a rebate from the miner. We can also look at the 0.1% quantile, and this allows the miner to .. the block space without effect to his size limit.

Q: Miner makes a block with a single transaction with a super high fee that pays himself. Then he stuffs the next block with a hundred terabytes of data.

## Simulation methodology

To get some understanding of how well this method works, I made a simulation. I use brownian motion with restoring force as the definition of the transaction rate function. Each transaction has a random value. Each transaction has random priority, desired dstiance from the tip. Fee is chosen to match desired depth. Discarded if higher than the value.

## Simulation results

There's a baseline result and then a result for the elastic case. The average fee for the elastic case got a little bit lower than for baseline. The graphs look similar, not much of a qualitative difference, but there is in terms of fees.

## Results

By implementing elastic block caps with a modest range, fee variance can be reduced by 30%, while maintaining the same average fee and throughput. Standard deviation was reduced by 16%. It's measurable, I think the cost of doing this is rather low, we can get some reduction in the variance of the fees. If we want more reduction, we could make the bloc ksmaller or choose a different function. It's a goo dstarting point.

## Older ideas

My original idea in 2015 was to make a penalty based on block size. The miner pays a penalty if the blocks are too big. I don't really believe in that concept any more for several reason. First, it's functionally equivalent to ... for whatever else.. we can find an equivalent penalty function in the .. so it's not... The reason why I like the penalty in the first place it's because it's more free market, so the miner can do whatever he wants as long as he pays for it.  But this is more complex to implement and reason about, and it messes with inflation because miners need to lock coins that he would have mined and they get paid to future miners. So that's messy.

## The problem with proportional penalty

There are some other ideas that came out. Some of them had a common theme which was proportionality. They had a penalty that was in some way proportional to the value of the block. If you do that, it just doesn't work and doesn't adapt the block size limit to the network load. If the fees are higher, then the block size limit will be higher. So we want to maximize the total fees divided by the difficulty.  This is in balance to some constant scaling factor, it will not depend on load of the network but other details about how the mempool works and that is not what we want.

## Deployment

I think this elastic block caps suggestion is simple enough for me to implement. I am willing to support implementation efforts, but I think other people are better suited to do the implementation. Changing this is a consensus change. If we want to lower the block size, this is a soft-fork. If we want to increase the block size, this is a hard-fork. I suggest that sometime whenever we get around to doing a soft-fork, we just reduce L from 4 to 3.5 and it doesn't change a lot, but it does help us figure out how this system works instead of in a simulation. Later, we can do a hard-fork to increase the U value. Long-term, the hard-fork should include a growth schedule like 20% growth per year. Size growth to match hardware improvements and network growth using my magic crystal ball to foresee the future. If it's too small, then we hard-fork again and if it's too big, then we do a soft-fork. When we do a hard-fork, we should set a mechanism that increases the parameters by 20% per year or something. This should more or less match Moore's law which we all know applies to literally everything.


