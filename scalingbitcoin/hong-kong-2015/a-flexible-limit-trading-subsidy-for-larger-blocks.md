---
title: A Flexible Limit Trading Subsidy For Larger Blocks
transcript_by: Bryan Bishop
tags:
  - soft-fork-activation
speakers:
  - Mark Friedenbach
media: https://www.youtube.com/watch?v=fst1IK_mrng&t=4h27m53s
---
slides: <https://scalingbitcoin.org/hongkong2015/presentations/DAY2/3_tweaking_the_chain_2_friedenbach.pdf>

I really want to thank jgarzik for that interesting talk. Who picks what block size? My talk is going to be about a category of dynamic block size proposals that attach the block size limit to the fee in such a way that as there is more demand for block size, through users that want to pay fees, the block size will increase or decrease as necessary. The need for a dynamic block size is so that the block size can increase. A payment network stuck at a too small block size is useless. At the same time, a block that is too large leads to miner centralization, not only in an adversarial case where miners are out t oget us, not only is that an issue, but we might see miner centralization to a group located in one place, which is influenced by big blocks. We are looking for a goldilocks zone where the blocks are large enough to be useful, but not so large that they destroy the network.

Many of the proposals are on a set schedule, according to some curve for max block size limit. The other two are based on miner voting. The schedule falls apart because we can agree that 1 MB is too small. We have no idea what the future is going to bring, let alone 2 years in the future or 4 years in the future. The miner voting proposals are flawed in a few ways. If it is the case that, such as in some proposals, the block size proposla has a miner vote (like [bip105](https://github.com/bitcoin/bips/blob/master/bip-0105.mediawiki)) where it goes up or down based on the block size, but that's defeated because the miners can fill up the blocks with random garbage. At the other side, there's things like bip100 where there is a vote for up/down for whether the block size should increase, and it's just miners making the choice.

First, we have seen from selfish-mining that even if you limit to 80% of the miners have to vote, that's really only 30% of the miners because 30% of the miners can censor other miners and make it look like 80%. So a small 33% able to pick the block size is too low of a threshold. It doesn't matter what the threshold in the BIP says, it's going to be 33% because of selfish-mining. We have seen over the past day that miners do not see it as their role as being the most informed or the proper people to be making this decision. It's a fair criticism that the bitcoin community should be doing it. But how do we achieve that?

The solution is that, the only thing that is available to us are miner votes. So we should make the miner votes based on user fees or any mechanism that users have to signal to miners to comply with user demands. Some of this is repeat, but the last one is important. We have scarce resources available, namely hashpower and block reward, and also bitcoin days destroyed. The blockchain protects as the available for signaling. We have only these mechanisms to play with. It would be nice to have 1 user 1 vote, but we don't have identity because of sybil resistance. It would be nice to have 1 miner 1 vote, but a miner could just send the same thing over and over again to make tons of different votes. So this is why our options are limited.

The proposal itself is quite simple, to increase the block size, a miner can defer the subsidy or some reward, choosing to not claim the full amount otherwise allocated to them. A miner would then choose to take 20% of the reward or something, and as a result they are allowed to create a larger block. Why would they do this? Well they would do this if the fee market would provide more income than they would have through the subsidy. This ties the block size directly to the fee market. Did the blocks go up or down, take the average, and that becomes the new base block size for the new period.

There is one problem here. How do you set what's the price for the fee market? We have so far punted on that. There's a parameter that could be chosen, and then we can decide whether that is too high or too low based on voting in transactions. This is derivative of two separate proposals from Meni Rosenfeld and gmaxwell, but kind of mixed together here. I don't want to steal credit. There was a modification of this by petertodd of a proposal by jgarzik.

Here's a graph before I get to the code, to define how the miner can influence the block size. The vertical axis is an increase or decrease of up to 20% in block size, and horizontal is how much subsidy or block reward that they are giving up or claiming from previously given in order to get a larger max block size. It is non-linear such that at the zero point in the middle, that is to say the base block limit, the marginal cost of increasing is such that when the fees equal subsidy, is when you see increase up or down. And this is configurable with a parameter. It's a non-linear function that becomes more costly as you increase the block size the more you increase. This is desirable because you can look past historically and get into insights from what the mempool was at the time, which tells you how many extra transactions were available at the time. It's pretty cool to get insights like that.

Getting into the code, there's a, it's all implemented. I forgot to push before the talk. This is a flexible block size limit, using fast integer math, no floating points in the square roots. The constant factor chosen was explicitly done so that the cost would range from whatever the cost is to increase the kilobyte at the midpoint it would be 4x that cost at the extreme. So if you want to increase the full amount allowed, like when the mempool transaction fees are increasing 4x their normal amount. This was somewhat arbitrary number picking, there was some simulation in picking these but due to time constraints I am not going to show the simulations in this presentation. There's some room for bike shedding here.

We don't want to have to set the security parameter though. The numbers at the bottom are how much subsidy you're giving up, it shouldn't be set by miner vote or developers, but by users. This determines at what fee value does the block size start to increase, and if you assume a certain fee value, then it determines what the block sizes are going to level out at. We want some way for users to signal whether they pick this value, this steady state block size should go up or down. Since we don't have too many variables to play with, the one that seems to reflect the stakeholders the best is bitcoin days destroyed, which is somewhat obscure value but it is essentially if you have inputs coming into a transaction then the age of those inputs times the value of those transactions is the bitcoin days destroyed. So you are weighting the amount or value of the BTC and how long they have had it. The proposal is that you would adjust the security parameter up or down based on weighted votes from bitcoin days destroyed. You could use two bits from the nsequence proposal of the inputs, to signal up or down vote. Two bits are used because currently the sequence field is only used for two purposes, one is to signal the transaction is final, and the other one is to sometimes soon is as a relative locktime which happens to set these bits to zero. So we take those to mean no vote. If you alternate the bit values of either of these, you could vote up or you could vote down. Over a period, and you would probably vote over a period of two weeks or more because of variance, you would look over that window and find if users are voting up or voting down.

I would like to backtest my data against Rusty's corpus. There should be a draft written in the next couple of days. I have left extra time available for questions.

Q: Can transactions be censored?

A: Yes. If there is a cabal of miners that do not like a vote, there could be a price differential in the price they pay, yes. They are giving up the fees they would have collected. That's a risk, yes. If you are voting against the cabal of miners, then perhaps you have to pay a higher fee. This is unfortunate but not sure what to do.

Q: Why does deferring reward and claiming reward incentivize miners to reflect user preferences?

A: The idea is that we want the-- if there's so much demand that users are willing to pay fees greater than the subsidy that miners would be giving up, then we might as well go with that. Hopefully this is not a suicide pact where there would be so much demand that users would pay to destroy bitcoin. That's why the curve is non-linear. The rewards they get from the fees make up for the subsidy they are foregoing.

Q: We could achieve voting from stakeholders, without running into the problem with sending money, is to pick a blockheight and use bitcoin signatures based on the private key address, using the private key at that blockheight and then weighting votes that way.

A: ......

Q: Do you see this with a hardcap, a hard ceiling?

A: There has to be a hard limit on block size. Even if we got rid of block size, we have to have a hard limit of some kind somewhere. If the security parameter is high enough, you could have a very high limit that is beyond what we think is safe, and fully expect to never hit it until at some point in the future.

Q: I like your proposal. In your proposal, people who own lots of BTC will have advantage?

A: Yes. People who hold BTC for longer period of time have stronger value in the vote.

Q: Because you use BTC for votes, what about giving the miners, ...

A: Giving miners like a certain percentage of vote?

Q: As payment for the votes.

A: The miners, by reflecting the vote accurately, they have to include all transactions that are above whatever their cutoff fee threshold is. So they can receive the maximum reward by not censoring transactions. It's possible to add a miner vote, if that was desirable. I was operating under the assumption that miners did not want that. But if they did, we could add something.

Q: This proposal is probably the best one since it's not a stop-gap.

A: The simplest one is the most straightforward? I am very deeply concerned about entities acting as jgarzik calls "FOMC", people picking numbers out of a hat to decide what level of decentralization or what fees need to be. Bitcoin is meant to be a decentralized system. I am looking for solutions that in some way tie block size solutions to in some way measurement of user demand, which is decentralized and does not have someone playing with parameters. We should have the simplest possible solution, we don't want to screw it up, at the same time, there's a great risk to proposals that set numbers or is a very simple vote that is easily gamed.

Q: You propose a window of 2016 blocks. Visa had an increase.

A: My proposal has a maximum increase of 20% per block. Wallets would have to use replace-by-fee to update the fees available in response to the traffic. Presumably, as the blocks get temporarily full, there would be people upping their fees, and then the upped fees would trigger the bigger blocks.

Q: Did you do any testing about miners growing the blocks to push smaller miners out?

A: Yes, but it depends on what you set the initial parameter to. The ideal parameter should be set to approximately equal to the subsidy. You are trading a significant fraction of subsidy to increase the block size. So right now an order of magnitude increase in fees would be necessary to become greater than the subsidy. So what would have to happen is ... in the foreseeable future, if deployed soon, we would need a much smaller parameter. Fees have a lot more variane than block size. Fees would go in and out of phase of having an effect on block size. So to answer your question finally, did I do simulations? Yes, but it's not necessarily the simulations that would be useful for current block size data, because the transactions we're including right now don't really respond to mempool dynamics of increasing or decreasing fees. Also, the size of fees at the moment are not reflective of the important properties that the proposal is trying to capture.

    21:25 <@maaku> also I didn't have time to go into it but obviously flexcap doesn't work well with CT...

<https://github.com/maaku/bitcoin/tree/flexcap>
