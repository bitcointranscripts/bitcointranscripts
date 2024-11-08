---
title: 'Playing With Fire: Adjusting Bitcoin Block Subsidy'
transcript_by: Bryan Bishop
tags:
  - mining
speakers:
  - Anthony Towns
media: https://www.youtube.com/watch?v=y8hJ0VTPE34&t=13s
---
slides: <https://github.com/ajtowns/sc-btc-2018>

<https://twitter.com/kanzure/status/1048401029148991488>

## Introduction

First an apology about the title. I saw some comments on twitter after the talk was announced and they were speculating that I was going to break the 21 million coin limit. But that's not the case. Rusty has a civil war thesis: the third era will start with the civil war, the mathematics of this situation seem einevitable. As the miners and businesses with large transaction volume will both decide to reintroduce inflation so that you don't have to pay fees, fees just magically happen. And if you want to increase the subsidy limit, that will involve a fight. This is not a pro-inflation talk. This idea is not endorsed by Xapo, my employer. The fact that I work for a company involved in the 2x nonsense, I hope that will not taint the interpretation of this. I send patches to Bitcoin Core, but Bitcoin Core doesn't endorse this or anything else. And this idea is also not endorsed by me, and I would just like people to think about it.

## Does bitcoin use too much energy?

I don't want to get into flame wars, so I'm going to talk about bitcoin using too much energy.... subsidizing blocks with brand new money has two benefits: (1) a decentralized initial distribution of the currency vs a pre-mine or an auction, and this is much more fair than the alternatives. (2) Subsidizing payment for proof-of-work security vs transaction fees. These days, the main reason for the subsidy is that we're subsidizing the proof-of-work security and the prevention of reorgs and double spends.

When people say that bitcoin uses too much energy, that's like people saying that as far as proof-of-work is concerned, bitcoin is too secure. By saying bitcoin should use less energy, you're basically saying that you want bitcoin to be less secure. That's what you're saying. If you want it to be less secure, you have to say I'm going to be taking more risk, is that going to be a visible amount of risk, or absolutely trivial?

Why might you even think bitcoin uses too much energy? Let's turn to anecdotes and random stories that people have. The mainstream media pays attention to how much energy is getting used and people get concerned about that. Is that a strong indication of a problem, or is it just journalists making scary stories to get clicks? Another factor is that if you look at the bitcoin industry, a lot of the profits are made by mining hardware manufacturers. Is that because there's a lot of money going into it, or because it's a real essential value add?

Over the past 8 months, while the bitcoin price has decreased from $20k to $6k, we have had a 7x increase in difficulty. Does a 7x increase in PoW indicate a "bear market"? If the price is flat, there's no huge investment going into bitcoin, then why is the security going up?

Another factor is that blockchains with smaller PoW are not getting attacked. Why are we spending so much on PoW if the small ones aren't getting attacked? Some of them are getting attacked, but not all of them. Not even testnet is being constnatly attacked; Bitcoin Gold got attacked. It's not as trivial as testnet, but it's still significantly smaller than bitcoin.

## Maths

Can we analyze this in some objective way? Anecdotes are okay for getting introduced to the idea, but at an academic conference we would like to be more objective. The way to measure this might be the hashrate or the difficulty score, or electricity in kWh/year or gigawatts, or in the value or money measured in US dollars or real dollar terms. I am going to be using US dollars for this, not bitcoin or yen or Argentinian whatever. The idea behind US dollars is that the inflation level in real-terms is relatively constant.

Here is the bitcoin difficulty graph on a difficulty axis. It goes up. There's not much else you can say from it. Here's a log graph of the block subsidy on a log graph. You can see the drop at the first halvening here, and the drop at the second halvening here. Otherwise you see huge peaks as the market price goes up and down. The problem with this is is that it tells us what you're paying for, but not what you get in terms of security. The spikes upwards are miners getting free profits.

I like to look at hashrate vs value, an objective graph of the difficulty, the price and the reward schedule to say how many dollars of revenue does a miner get per terahash of hashrate. On a log scale, again, it gives a graph like this. Because miners get more efficient, the number terahashes you can do per dollar goes up over time. It's one of those graphs that goes up and towards the right. You can counter this by looking at the performance of individual miner hardware. As new mining hardware gets released, the amount of hashing you have to do to get one dollar of revenue still keeps going up. The nice thing about this graph is objective, it's not about speculating about what miners have deployed. All the numbers are objective from public data.

ONe of the nice things from that graph is that you can see that as the economic theory says, that miners will essentially eat away at their own profits. If there's more money to be made from mining then they will do more mining until there's no more to be done. The rates for kWh there was $0.16 each. That might seem expensive, but the fact is that, it includes opex costs (cooling, staffing, etc) and capex not just opex, and it includes expected profits, and it needs to cover risk that difficulty will rise faster than expected, and mining isn't a completely efficient market. My guess is that the breakdown is 4c is electricity only, the rest on the slide.

## Predictions

From that structured analysis, can we make predictions? We need to make assumptions about the market price, miner efficiency, and electricity costs. My assumptions on market price, take them for what you will. I will assume that bitcoin is going to succeed and will scale up. I'm trying to be as conservative as possible, which is really not very conservative. I've done a log-log curve fit as a low support of prices. It still gives pretty high valuations, maybe they are lower than what you expect, maybe they are not. In particular, the current value is much lower than the current.....

I also have some assumptions about terahashes/USD and miner efficiency. I also have one for miner efficiency. I also have one about energy costs and electricity costs. You'll note that it goes down very low; that might not be reasonable.

So, those are the assumptions. Going from just the price estimate, we can work out what the reward is going to be valued at over a long period. What this graph shows is that within the kind of an error of a log-log scale of course, that the reward is going to stay high and constant over a matter of decades. We're not going to have the inflation reward in real terms drop-off for quite a while actually. The reason for that is really simple... the reward halves every 4 years, but the price estimates we have doubles faster than every 4 years. So there's no shock there if you're expecting bitcoin prices to appreciate. Those little shocks every time you're using a halvening look a lot worse if you're not using a log scale, so let's just use a log scale.

You can see that the energy use keeps going up, even if the reward stays flat. The price of electricity is going to keep going down, so if you have the same amount of money then you're going to use more electricity. At the top of the graph is 10% of the enitre US energy usage, which I predict is decades out for bitcoin.

Again, these are shaky assumptions. Garbage in, garbage out. We started from shakey assumptions. We don't get to "bitcoin mining on track to consume all of the world's energy by 2020", a lovely headline from Newsweek. I don't think that's the case. 10% of the US energy usage by 2050 might be more realistic. But that's today's energy usage.

## Reducing energy usage

Can we do anything about that and would it be worthwhile? When the price of bitcoin goes up, lower the reward to compensate. If there's less money going into more mining hardware, then we're going to get less energy usage. Obviously we can't get the bitcoin consensus code to look at the market price to figure that out; but we can approximate it by looking at difficulty because if the price goes up the difficulty goes up as people deploy more miners. This is an indirect measurement of course. There is no "recursion" problem here, provided that miners can predict the drop in the reward, and one other factor.

A speciifc example that could work out okay: a concrete example is, cut the reward by 20% every time difficulty doubles. This is easy to calculate reward given block height and difficulty, consistent behavior no matter when the rule gets put in place, and exponential formula makes the math work out fairly nicely. This only applies once difficulty is above 10e12. This can be calculated from the data in the blockheader, too.

If you run this, then you see that the difficulty drops a little bit. The value of the reward in US dollars drops fairly substantially, a bit over a factor of 10. It causes the actual reward in dollars to decline a little bit over time rather than staying flat. Depsite difficulty increase, we're assuming miner efficiency going up and the cost of energy going down.

This is still more efficient than the existing banking system. The other thing is that it still leaves the energy usage flat over time rather than decreasing, which kind of leaves the security at the same level, which is probably a good thing.

## Implementation

Doing this could be a soft-fork. Reducing the block reard is a soft-fork. Limit what miners can claim based on the difficulty, and require them to burn the rest to an OP\_RETURN address. Can we keep the reward? It would seem wasteful not to. The approach I'm thinking of is "pay it forward", where have a miner's "savings trust" UTXO that miners pay into and eventually they can withdraw from it. Instead of burning the reward completely, you pay the reward from the coinbase into the savings UTXO and someday you take fees from it and supplement the coinbase reward. The consensus rules specify the amounts that each block can "withdraw" and must "deposit". If they can avoid paying in but always withdraw then that's not of much use.

Each coinbase spends burned rewards to a scritpubkey "100 OP\_CSV". Each block contains a "savings transaction". Inputs are the previous block's savings transaction output, and the coinbase burn output from 100 blocks ago. Consensus rules validate that the coinbase burn is at least some appropriate value, soft-forkable up. A few other proposed consensus rules.

This approach has a variety of potential uses, such as smoothing the halvening schedule and flattening out the halvening schedule, instead of having abrupt disruptions. You can have it gradually reduce by paying into the savings transaction over 5,000 blocks or 50,000 blocks and then after the next 50k blocks after the reward halves, withdraw from it to smooth it out. I think Mark is going to talk about this in a few talks.

If you have an actual fee market, instead of the entire subsidy coming from inflation, then every now and then you might have fees from lots of transactions such as due to ocnsumer behavior. But perhaps on the weekend oyu will have lower transaction volume, and you can use this approach to smooth out the fee rate so that mining at any particular time of day has the same profitability.

This could also be used as a cost mechanism for allowing temporary increases in the blockweight limit.

## Other approaches

There are plenty of other approaches. Maybe we don't even need an approach, maybe the invisible hand of the market will solve everything for us, who knows.

## Other benefits

Some people claim that halving the reward will force the price to double, as a result of supply/demand. Even if it doesn't exactly double, then demand still goes up. Perhaps that's a good reason to lower the inflation rate in general anyway, thus we have less money going to miners, maybe the same demand means the market price goes up. Maybe if the people on twitter are right, then let's halve the reward each day for the next few weeks, and we could double the price every 8 minutes.

## Conclusions

My assumptions are kind of terrible, perhaps you can provide better ones. How robust are the predictions with different assumptions? What is the likely impact on parts of the industry in real terms? Can we really implement this and make it work, and get the formulas right? I am not going to push this any further than this talk.
