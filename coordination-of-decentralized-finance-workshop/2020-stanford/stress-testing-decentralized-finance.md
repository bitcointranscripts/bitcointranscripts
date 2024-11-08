---
title: Stress Testing Decentralized Finance
transcript_by: Bryan Bishop
tags:
  - security-problems
  - altcoins
speakers:
  - Tarun Chitra
date: 2020-02-18
---
<https://twitter.com/kanzure/status/1229844754990370816>

## Introduction

More quantitatively, I think coming up with stress tests is akin to Bryan's question.... stress testing is something that people in this space kind of do, and I'm going to talk about what that looks like and what an actuarial analysis should look like.

I'm going to go through three examples of where an actuarial analysis shows certain weaknesses that need to be monitored and understood. They are going to be more on the scifi end of cryptocurrency. We'll end with an attack that has happened twice in the last 72 hours. Even the normal media is covering some of these attacks. We'll start with some things that seem scifi, but people are definitely taking advantage of this.

## Background

I worked in high-frequency trading for a while, built ASICs and did some algebraic geometry. I started a company that attempts to do more rigorous statistical stress tests.

## DeFi stress testing via three vignettes

The first one is that proof-of-stake has fundamentally disconnected economics from proof-of-work. It's intuitive, but understanding why is important. One of the main reasons is that the monetary policy in a PoS netwokr and how it emits block rewards is tied to competitive on-chain activities, whereas in proof-of-work this is less true.

The second thing we'll talk about is on-chain lending which you can see in this figure has grown quite a bit. It's a way of doing decentralized spec lending and decentralized block-finance.

Then finally, how does smart contract code interact with incentives? This is an attack that has happened recently that we will talk about.

## Monetary policies in proof-of-stake systems

Let's start with a thought experiment. Imagine you have a proof-of-stake asset that is securing a smart contract platform. There's an on-chain lending platform. The contract allows the user to borrow and lend the underlying staking asset, algorithmically determine interest rates, and at least 50% of the users are rational and profit-maximizing. There are some potentially altruistic entities, some that might be byzantine, and most users don't have antithy towards the network.

What happens if the interest rate for the on-chain lending rate is higher than what the proof-of-stake market is offering? If you're rational, eventually you will move all your staked assets into the lending. It doesn't make sense otherwise. So how would an on-chain lending vehicle have a higher interest rate than the staking itself? Well the simple way it happens is say the price crashes for an asset relative to some currency, the demand to short the asset will go up, and this will increase borrowing demand so the interest rate for lending goes up. In these volatile conditions, you can easily have this phenomena, and we have seen this in practice where interest rates go higher than lending rates.

The monetary policy of the staking network has to accomodate these alternative sources of yield. Capital stakes can be cannabolized. BlockFi and others-- the contract will keep lending, nobody can stop it once it is deployed.

Proof-of-stake networks look more like central banks than proof-of-work. They have to adjust their monetary policy based on lending activity. When people are reallocating from staked assets to lent assets, that's equivalent to the overnight lending that central banks do.

Proof-of-stake networks don't need external assets. You need an extremely liquid hashrate derivatives market to do the same thing for bitcoin, and for bitcoin that doesn't exist.

Stress testing involves understanding network demand and the risk preferences of the evaluators and participants of the system. One thing key to this is that deflationary monetary policies is devastating to proof-of-stake systems, and this is not true for proof-of-work systems.

## Market risks of on-chain lending

Let's consider on-chain lending risk. On-chain lending itself can kind of cause capital flight or bank run from proof-of-stake. So what about the lending mechanism itself? How does it keep synchronized and adjust to market prices?

Let's talk about the biggest on-chain lender, which is Compound. This number I pulled is wrong- I think it has gone up since the ETH price went up a lot this morning. Basically, the way these work is they-- you have three principal agents... one is lenders who lock tokens into a smart contract with a pool of assets, the other side is borrowers that post collateral into the contract and then borrow against that contract. Lenders receive continuously paid interest. There's a p2p lending pool, if there's a default then everyone splits the risk of loss based on their share in the pool. The interesting thing is, where does the demand come from? It comes from people who are long ETH and want dollar liquidity so they want to borrow stablecoins. This is how things bootstrap themselves. This is a smart contract, and there's no way to stop this- unless there's an admin key. In Compound, there will soon be no admin key.

The way this works is that there's a curve which is algorithmic game theory- called a scoring rule- that provides you with an interest rate for borrowers and lenders as a function of demand and quantity. So you define the net demand divided by total supply to be the utilization rate. You can think of that as what percentage of the total money supply that this contract can touch is due to demand, and if it's very high then you have a higher interest rate, and if it's very low then you don't have a high interest rate. Compound's whitepaper and implementation differ in what curve they use.

## On-chain lending and liquidators

So how does this contract handle defaults? What happens when someone doesn't pay back their loan, they're not paying interest? This is all over-collateralized secured lending. This is like a home equity loan. Say your home is valued at $1m, and you're allowed to borrow some percentage against that like 40% or 75%. If the price of ETH goes down so much, my loan is in default and under water and now the contract is holding net liability. So what these contracts do is they operate something like a foreclosure auction on your assets. These liquidators buy the collateral at a discount from the smart contract, and then they have bought the liability. So the question is, how much of a discount does the smart contract have to do? Compound does this with three different monetary policy: they're a fixed-incentive one, Maker has an auction with reserve prices, and DiDx is a blend of those two. In some cases, it's a fixed price and in some cases an auction.

So why do liquidators by this collateral? If in theory they knew how much slippage or how much market transaction fees they will pay, then they will make a profit because if it's greater than they can pay for, then they get some percent of the collateral. But this depends on market risk. This smart contract now has exogenous risk factors like market prices crashing. Are liquidators really going to enter the foreclosure auctions? In an incident like 2008, nobody is going to come and buy it. This is the type of risk that is not caught by a security audit or formal verification. It's about things exogenous to the contract. Having volatility, that's not knowable to the contract itself...

The worst case is a deflationary spiral. Say ethereum prices crash. Liquidators buy up all the collateral, and they all sell all the collateral immediately, causing ETH to crash and causing more loans to go into default. So you get into this spiral where you keep selling and you can't get out.

## Modeling liquidation risk

If you were to make an actuarial risk score or something statistically rigorous, how? You need to model market prices. What's the colatteral factor? The second thing to model is slippage. If you have ever done any trading, it's how much impact am I causing in the market when I'm trading? Are people going to frontrun me? Slippage is a way of measuring how much cost am I paying for people knowing about what I am doing. Then model agent risk preferences- like buying at a discount and selling at an exchange, there's some risk to that because what if I don't win the collateral auction and I can't sell fast enough. So modeling the risk preferences of liquidators who are really risky and enter each auction, or some don't enter because they don't think they can profit with some probability above some threshold.

In bitcoin, fee sniping is quite- because it's, slower, and because bigger blocks, and CPFP and replace-by-fee, the fee sniping is significantly less complex stategy wise than ethereum. This is actually good for bitcoin users. In ethereum, the frontrunning behavior makes it hard for certain types of transactions to succeed. But you do have to model this thing where people will try to frontrun these auctions for collateral.

A really important part here is that, running these stress tests on mathematical models that are supposed to approximate the contract, don't really work. One of the reasons for this is that your model is never going to replicate the crazy exit conditions. There are many non-analytic edge cases, like say you're modeling the price of the contract by some Neto process.... well, the contract is represented as fixed-point arithmetic, your Neto process is going to overflow at some point, so how do you handle that when it happens or what the contract does when it happens? Because that might be the time when the arbitrage is largest. Also, the contract logic doesn't match the whitepaper description. You really have to understand the smart contract and bytecode and post-compilation code can give you very different outcomes than what you might expect from static analysis. There's gas optimization, fee optimization, and static analysis view of the world doesn't exactly tell you everything.

In normal trading, what do you do? You have 100s of exchanges, each has different latency, each has different wire format. You do specialized Monte Carlo. The way to do this is to backtest plus you add in this multi-agent model of people competing for these auctions and people competing for lending and so on.

## Simulation results

We did this simulation, large-scale simulation with thousands of borrowers. We ran millions of simulations. For ethereum's maximum volatility, kind of the current Compound system can handle significantly more debt than it currently has, but if the volatility goes up by 50% then you start to see a huge increase in undercollateralized debt ratio. These phase transition boundaries between no-defaults and tons-of-defaults is very common in trading strategies, you always see this stuff. Your high-level model might not work with this. On the left, we have thousands of competing liquidators and these are their expected profits under different volatility conditions. There's certain volatility conditions where income is quite smooth, it's basically increasing almost linearly, whereas in these very volatile conditions you have the same where you keep missing auctions and then you evenually run on.

## Interoperable financial incentives

The thing that has gotten popular press coverage... was written by Matt Levine earlier today. Matt Levine, this Bloomberg writer, has a great quote: "It is not original to me, but one thing that I think and write a lot is that cryptocurrency enthusiasts keep re-learning hte lessons that regularo finance learned decades ago, and that you can see a lot of financial history replaying itslef, sped up, by observing cryptocurrency.". In proof-of-stake and DeFi, there's a lot of ways to go wrong and not get the desired economic outcomes.

## Flash loans

What's a novel attack that you can't do in normal finance? We got this crazy thing this week: flash loans. Flash loans are something that is basically the following. There's a lending pool like Compound, and I can say hey Compound I promise you that when I borrow $5 million, I'm executing this code on it and then I'm going to return $5 million. So if the code I executes runs into a halting condition like running out of gas or someone frontruns me, then the loan won't go through and I pay it back immediately. It's like being able to go to the bank, get $10 million, and say here's exactly what I will do and if I'm in a condition where I can't do those things, you get the money back in a single transaction. That's what a flash loan is.

This is what Matt Levine's article was about.

This lets everyone do the George Soros attack. This is a very famous trade from 1992 involving Soros buying out a currency to make sure the central bank couldn't rebalance relative to something it was pegging against, and then eventually they capitulated and started printing more money. So you borrow a gigantic loan at no cost basically, you spend x% of your loan on a short position, and then you spend some of the remaining amount of your loan to manipulate an oracle that provides a short against which your loan is marked at. This happens a lot in normal trading. This is a funny thing that some people are saying it's novel, but no this happens with central banks like when they announce an increase in rates but then there's a huge amount of open market operations where someone is selling unreasonable amounts of eurodollar contracts for the next quarter... usually central banks will do open market operations to mitigate the impact of their announcement.

This flash loan crash happened twice this week. There's thousands of people trying to replicate this right now. These lending pools have hundreds of millions of dollars in them. You can scale your strategy by quite a bit doing this.

## Risk mitigation

So we have heard about chains of defaults and it's turtles all the way down. What can we do about it? Well, first we need a better threat model and not do the crypto threat model about everyone honest and everyone byzantine and no one in the middle exists- that's not true. If you read a lot of proof-of-stake papers, the participants involved have probably never traded or don't understand financial markets, they think it looks like proof-of-work and you get the same security. But proof-of-stake has really crazy capital costs from lending and derivatives. You have to choose parameters correctly, which is hard. That's where you need simulation-based tooling.

The other thing you need is continuous mechanism monitoring. Every time market changes come through, you should be updating default probabilities and what's the risk in the system. It's a continuous thing that changes the market. Because you have so many different actors, you really have to make sure you monitor all of them.

<https://gauntlet.network/>

## Q&A

Q: Mempool sniping- anyone monitoring this?

A: People are definitely doing this. Gas price auctions, on average costing 1 cent, evnetually you see some where for $10k.

Q: So what about comparing opportunities across contracts?

A: It's quite suboptimal. The first attack netted a profit of like $375k. But it was highly suboptimal. In fact, if you chose different parameters for how much you split amount used vs oracle manipulation use, the optimum was around $1 million. So there's kind of a-- I think this space has people starting to do it, but it's not as sophisticated as normal trading.

It's important to not assume that the attacker won't have money. They might have arbitrary amounts of money.

Q: So it's not illegal to do this?

A: Well, the admin key might mean they can boot out the user, but they wouldn't be able to do this if it was fully decentralized. But this might count as market manipulation. I think it's weird because they interjected in the market. Otherwise it would have been more like someone having a successful trade. Then BZX would collapse. Well, the lenders are subsidizing this. When it gets defaulted on... the lent pool is used for the short, so if it doesn't get paid back then it's defaulted on it. It's a little like insurance and re-insurance with weirder securitization.

## Group discussion

We spent a bunch of time comparing governance in proof-of-stake and DeFi arguing that proof-of-stake governance is frought with difficulties because stakeholders, because it's already a complex situation where the majority of capital owners are not the validators and it's unclear if the delegators are aligned with stakeholder views on proof-of-stake. We compare DeFi governance which has been more successful; it has a lot more votes, partly because it relies on traders with financial incentives. They go and vote, on interest rates, because they have more direct incentive on that, but on proof-of-stake it's unclear when to vote on new features.

We also talked about staking derivatives and how all these complex things are just ways to prevent lending activity and other capital flight type of things from removing network security. I think that's pretty much it. We spent a lot of time on those two pieces. We were comparing and contrasting, like if we go from 2017 to now, the vision that was sold then is quite different from what the current reality looks like.

Q: I didn't realize validators in PoS systems were staking money from venture capital funds. That seems like a big incentive issue, because the purpose of staking is to disincentivize improper transaction validation. I know we touched on it a little bit, but I'd love to hear your thoughts on that.

A: Once you have Binance or Coinbase as the main validator, then they can start censoring transactions once they have enough stake aggregated to them.

Q: If I am a validator and not staking the money myself, maybe I don't care if I screw over the VC fund's staked transactions? Or maybe I misbehave in my staking validation, and my funds...... it's really a principal agent problem.

A: ... there's proportional slashing, where you have to put up a bond proportional to the number of users you're delegating for, which disincentives you as a pool operator from doing double spending or something. This is a proportional slashing cosmos proposal. There are certainly disincentives and bad incentives there, and designing things around those is important. The key is to make sure the slashing probability... the expected returns from slashing is strictly negative, for the validator and the person whose assets they are validating for, at all time.

Q: But the delegator and validator enter outside of the chain agreement, about how the liability of the slashing gets shifted? In that case, validators might still have incentive where they say basically in any circumstance if slashing you still carry the VC costs. So it's the same thing, as a highly leveraged transaction.

A: Yeah, I guess the difference is that on-chain contracts can be enforced by consensus. In newer staking networks, the staking primitive is represented as a smart contract itself. The consensus mechanism is upgradeable in the sense that the contract can be upgraded. The addres can point to another contract that points to another contract that replicates interest rate models.

These transcripts are <a href="https://twitter.com/ChristopherA/status/1228763593782394880">sponsored</a> by <a href="https://blockchaincommons.com/">Blockchain Commons</a>.


Tweet: Transcript: "Stress testing decentralized finance" https://diyhpl.us/wiki/transcripts/coordination-of-decentralized-finance-workshop/2020-stanford/stress-testing-decentralized-finance/ @tarunchitra @CBRStanford #SBC20
