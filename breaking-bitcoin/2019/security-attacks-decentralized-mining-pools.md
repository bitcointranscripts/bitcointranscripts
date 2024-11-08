---
title: Security and Attacks on Decentralized Mining Pools
transcript_by: Bryan Bishop
tags:
  - security-problems
  - research
  - mining
speakers:
  - Alexei Zamyatin
media: https://www.youtube.com/watch?v=NWG7HZVT00M
---
<https://twitter.com/kanzure/status/1137373752038240262>

## Introduction

Hi, I am Alexei. I am a research student at Imperial College London and I will be talking about the security of decentralized mining pools.

## Motivation

The motivation behind this talk is straightforward. I think we can all agree that to some extent the hashrate in bitcoin has seen some centralization around large mining pools, which undermines the base properties of censorship resistance in bitcoin which I think bitcoin solves in a nice matter. Miners who join these giant pools have no cryptographic or real guarantee that they will receive fair payouts. They still have to put in some minimal level of trust.

"A deep dive into bitcoin mining pools: An empirical analysis of mining shares" 2019

## Decentralization

While bitcoin doesn't have severe problems around centralization with a single mining pool, altcoins have another story. Small cryptocurrencies often suffer from centralization. Take a look at namecoin and we see that a single entity was able to maintain the hashrate for prolonged periods, which is kind of a problem I hope we can all agree on this.

## Goals of decentralized mining pools

Censorship resistance is an important factor. We should try to give decisions about which transactions to include should be to the miners in the pool and not up to the pool operator. The assumption is that if you have sufficient numbers of honest miners then at some point your transaction will be included into the blockchain. With fewer pools, it's easier to censor transactions. Also, we want miners to be able to verify that payouts are being done fairly and that no single miner in the pool is trying to defraud them.

The challenge is that we must reach agreement on reward distribution. In centralized pools, we have a single leader that decides who receives how much reward. Usually a single miner cannot verify if someone is defrauding you because they don't have information about the other shares. There's some overhead in the decentralized scheme, due to multiple verifications requirement. We want the overhead to be minimal.

## p2pool

p2pool was the first decentralized mining pool proposed and launched in 2011. p2pool uses a separate sharechain (FIFO queue) of bitcoin blocks that are chained together. The more weak blocks you can include in the sharechain, the higher the fraction of the reward you will receive once the pool finds a block. The interesting thing about this is that the rest of the network doesn't have to see these weak blocks. All you notice is that blocks mined by p2pool have large coinbase transactions that do a lot of payouts. This is how miners participate in the pool; by specifically including the correct payout structure.

Miners compete to put blocks into this bounded queue of blocks. The duration of a p2p pool... the scheme was PPLNS (about 3 days) so based on the blocks from the last 3 days. p2pool struggled with difficulty adjustment, which is adjusted based on the overall hashrate of the pool. The idea was that one share would be found every 30 seconds. But we can't have miners decide which difficulty they choose for their shares. A cool that we have in p2pool is specifically since there's so many blockchains around there that try to introduce smart contracts, p2pool doesn't need that. The only requirement is that the block interval not be too low otherwise you have subsecond for the share broadcast and you're actually running Nakamoto consensus on the sharechain so that has to be kept in check.

## Share difficulty handling

We need to be able to solve the difficulty adjustment. The sharechain must define the minimum difficulty. As a miner, I want to introduce as many shares as possible. I can choose a low difficulty and then spam the chain. Even if we say that heavier blocks outweigh small blocks, it will still cause lots of forking and reorgs. That's destabaliziation. So what if we take a statifc difficulty target pegged to the bitcoin difficulty target? The problem with this is that you can do this and it's fine for a while but the structure of your pool changes over time. It's a consensus rule of the sharechain so changing it requires a fork.

p2pool implemented dynamic difficulty adjustment just like in Nakamoto consensus. You look at the number of shares mined, and then you adjust the difficulty based on the number of shares expected. In a centralized pool, if you're a small miner you would be happy if a large miner joins because that reduces the variance of your payouts. But in p2pool, a large miner increases the overall difficulty threshold and a small miner would no longer be able to include any more shares in the sharechain. So then p2pool now has to separate into pools for small, medium and large miners.

## Block size and latency issues

By broadcasting shares in sharechain, you have to broadcast shares every 30 seconds in addition to bitcoin blocks and transactions. Miners with low bandwidth have problems with this. The original p2pool code had a transaction size limit. If we look at some historical data, on average p2pool blocks were smaller than other blocks at the time. We also see that p2pool blocks only have 61% of the expected block size. A discussion was had on github, and two networks were created for p2pool- one network for miners with a lot of bandwidth and one with low bandwidth.

## Selfish mining and 51% attacks on the p2pool sharechain

Even a small miner with no real impact on the bitcoin security, can still attack p2pool sharechain. Say p2pool has 10% of the bitcoin hashrate and a miner comes along with 4-6%. They could start selfish mining on the p2pool sharechain and defraud the other miners. He can fork out the sharechain blocks. You can try to mitigate this by imposing bounds on how many sharechain blocks you can fork out. But p2pool miners could detect this quickly and try to ban him. In the long-term, if someone persisted with this attack, people would just leave the pool as the pool becomes unusable. Theoretically, there are some large miners that probably don't like p2pools existing.

## Temporary dishonest majority

Let's assume that p2pool controls 30% of the overall bitcoin hashrate. Then an attacker comes along with 21% of the overall bitcoin hashrate. The attacker can try to convince p2pool to join his attack and this would gain a temporary majority of the hashrate. So the miner does a selfish mining attack on the sharechain as well as the bitcoin blockchain. There's a secret attacker chain that he doesn't broadcast until he's ready. He can easily outpace the p2pool sharechain and override the work of the p2pool miners. At first, the attacker keeps it secret. Eventually say the miner finds a mainchain block, and maybe he wants to continue selfish mining so that he can do better in the long-run. In the normal selfish mining attack, the strategy is that--broadcast the block and trigger a race and hope that you win the race. But the attacker scenario is different; he broadcasts the sharechain to p2pool as well. In normal selfish mining, if the attacker has better connectivity than the honest miner then he will win the race because he can broadcast it to the network more quickly. But p2pool will extend the longer sharechain, so they might temporarily join on the attack. This way, the attacker together with p2pool would very likely win the race. For this attack, we assume miners on the p2pool pool broadcast blocks received over sharechain to bitcoin. Hence the attacker keeps sharechain blocks secret from the beginning.  If this assumption is not the case, then the attack becomes even more effective because p2pool may join the attacker chain from the start.

Another observation we can make is that in the scenario where the attacker is paying out p2pool... if we now assume p2pool miners were economically rational and were willing to be bribed to do this attack to increase their profits, this might be enough to convince them to join the attack. Last year in Lisbon I mentioned that say there's a p2pool that controls 72% of the hashrate... this would in the long run incentives everyone to join p2pool; p2pool blocks are worth more to p2pool miners than normal bitcoin blocks because this is where they get paid out, so they have an incentive to prefer p2pool blocks.

## p2pool today

The p2pool codebase is no longer actively maintained. There's lots of forks, with weird things that probably break p2pool mechanics. Why did p2pool work, or why is it no longer active? I believe that- it seems that the overhead of p2pool was not worth the effort for a lot of miners, plus the issues with reduced block size, and an interesting observation that was made was that some miners decided to join p2pool but did not want to run their own p2pool node, so they connected to trusted p2pool nodes which is against the whole idea of decentralized mining.

## Smartpool (Luu et al, 2017)

Smartpool was proposed in 2017. It uses a smart contract to verify shares probabilistically and claculates reward distribution. It has an interesting verification mechanism for shares, which could be applied in theory to p2pool. Say we have a smart contract, a miner wants to join the pool, he checks the contract, he specifies the contract address as the recipient of the payment. The miner will mine shares locally. However, instead of broadcasting each share and sending to the contract, he constructs an augmented merkle tree where the leaves are the shares. You can look at the 2017 Smartpool paper. You can't include duplicates because it will give a sorting error; so we know a miner can only include a share in the tree once. The miner sends the root of this tree to the pool. The contract says I will randomly select a few branches you need to prove to me. The idea is that if you play this game for a long enough time, the incentive to misbehave is not there. The expected reward for honest behavior and dishonest behavior is about the same. The risk that you face of being detected due to manipulation is higher than the value of the gain. After submitting the proofs, the contract then can send a payment to the new address.

One interesting thing that this gives us is that miners can now select the difficulties of their shares themselves, and specify this when submitting the claim. The contract can adjust the calculation based on the difficulty that the shares were generating.

The caveat is that this needs a smart contract, and a bias-resistant random seed maybe from the blockheader but we know that can be biased especially since we're the miners in this scenario.

## Practical challenges

In smartpool, the idea is that you submit the claims at irregular intervals. You don't really know the state of each miners at the time you find a block. Also, to submit your claims and to accept your payments you need an on-chain transaction. Essentially, you might have to wait for your pool to mine a block i nthe first place, and if it's irregular then your miners will have to wait for these blocks in order to claim their payments which is kind of unpractical. Some of you may be asking how this is applicable to bitcoin. In the paper, they talk about verifying bitcoin proof-of-work in ethereum and then do cross-chain atomic swaps or something.

## Security issues

The smart contract in smartpool cannot verify transaction validity. This means that as a large miner I can submit blocks that are otherwise valid but they have invalid transactions. This launches an undetected block withholding attack, and if someone accuses me then I can say here's the blocks. If I never give you the invalid transactions, which only I have, then... yeah.

Fork handling is not discussed in the paper either. Compared to p2pool, in p2pool we keep submitting the shares after each block. In smartpool, submissions happen at irregular intervals. So it's possible multiple blocks have been found between submissions. The contract would have to check each share and know for each share what is the last block it should have extended. It's tricky. I couldn't actually find this part of the verification in p2pool. If it's not there, then the pool could sponsor selfish mining attacks.

Finally, smart contracts like Smartpool which verify proof-of-work allow us to construct quite nasty bribing attacks. We have a paper coming out in the next one or two weeks where we show how to construct bribing attacks where the bribers have all the risk and the miners have none. If you'r ewilling to attack another chain, you will be incentivized to participate, and these attacks work cross-chain and you won't be able to detect this without monitoring all of the smart contract capable blockchains.

## Summary

Something that I am interested in looking at is combining p2pool with the probabilistic verification of Smartpool. The p2pool miners broadcast share lcaims and proofs, then you verify this locally and update your structure. In theory this would allow miners to specify variable difficulty for their mining activity, maybe have less overhead. But how to combine this with PPLNS?

Obviously something that is more viable than anything proposed previously is that centralized pools allow miners to choose their own transactions; I think betterhash is pretty interesting. Check out the betterhash proposal.

Thanks a lot.
