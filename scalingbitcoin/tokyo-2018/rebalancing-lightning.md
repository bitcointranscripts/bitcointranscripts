---
title: 'Rebalancing in the Lightning Network: Analysis and Implications'
transcript_by: Bryan Bishop
tags:
  - lightning
  - fee-management
speakers:
  - Sebastián Reca
date: 2018-10-07
media: https://www.youtube.com/watch?v=nwSuctrzV7Y&t=637s
---
<https://twitter.com/kanzure/status/1048753406628655105>

## Introduction

This talk is going to be about rebalancing in the lightning network. I'll talk about the implications and about running a lightning node.

## Financial costs

In the lightning network, routing nodes will incur in financial costs by having their money locked inside channels. They can't use that money elsewhere. They incur a financial cost to doing this activity, at least an opportunity cost. To recover this, they can charge a fee every time they route a payment. If there are more or less payments, they are not paying more or less opportunity cost. It only depends on amount of money locked and how long it is locked. They have a choice about how to set the fees.

I'll give some examples about how these can be prorated into these fees. If N is the total amount of money locked, and r is the annual interest rate, the financial costs are N * r. There are some strategies. You can treat all payments equally, and P ius the expected number of payments in a year, and your fee can be (N * r)/P, and then you can penalize payments. Alternatively, you could take into the account the size of the payments routing over your node. Suppose you expect A to be the expected amount of BTC routed per year, you can do the fees = (z * N * r)/P where z is the payment amount. THis penalizes big payments, whereas the other one penalized small payments.

The more payments (or money) routed through your node, the cheaper the fees can be. Your node will also be more competitive in that case. This means you're probably to get more payments for routing and then you will become even more competitive.

## Channel exhaustion

The question of the financial cost is that you want to route a lot of payments and earn a lot of fees. Financial costs are not the only costs you will have. I will review how balances are updated in the lightning network, to introduce the next type of cost you will have. Suppose you have locked up some bitcoin in a lightning channel. Also, Alice and Bob could be connected to other nodes. There's routing that occurs in this example topology for the lightning network. You can get into a situation where one side of the channel is exhausted, which will cause you to miss payments, and then you will need to charge even higher fees. Also, Bob gets overfunded if Alice side has been exhausted.

## Rebalancing: splicing

Rebalancing is increasing our balance in some way in order to route more payments. You could close your channels and then re-open them with more funds. You can do splicing, with closing and reopening again with more money in one single transaction. Even with that optimization, rebalancing by splicing costs money because you have to broadcast a transaction, pay fees, and wait for confirmation times.

## Rebalancing: circular payments

This is another way of rebalancing channels. If Alice and Bob happen to be connected by another path, we can make a payment to ourself like this and then we can get our channel rebalanced. This strategy is very good in some sense because it's completely off-chain. You also don't have to wait for confirmation times. But still, it's not completely free, and you're going to pay the lightning fees because every hop in the path will charge you some fees, and the longer the path the more you're going to pay for this. When you perform splicing or circular payments, you're only limited by the amount of money you have. In the case of circular payments, you're limited by the balance of other nodes, and the longer the path, the more limited you're going to be. The other difference is how they affect the network routing capacity of the network as a whole. If you assume atomic multi-path payments, then you can see that here in this example. By doing the circular payment, we're not changing the network capacity as a whoel. But if we do splicing or closing/opening channels, then we're changing the routing capacity.

## Rebalancing problems

Rebalancing channels costs money. Optimizaiton problem: how to route the largest amount of money (or payments) while minimizing the rebalancing costs? I want to capture more payments and earn more fees. Both strategies will co-exist in the network. Splicing is more expensive because you have to pay on-chain fees. No matter which strategy you pick, rebalancing is going to cost you some money.

The rebalancing problem can be divided into three smaller problems: prediction of payments, who is going to send a lot of payments or receive a lot of payments? If some nodes receive more money relative to other nodes, then you would put money there in advance to route the upcoming payments and earn those fees. The other problem is optimization of money distribution. Once you have these predictions, then you have to find a way of distributing your money in your channels so that you can route the largest amount of payments or the largest amount of money.

For optimizaiton of money distribution for 2 nodes, Branzei, Segal-Halevi and Zohar answer this question for the case where 2 peer nodes transact following a random process, one node makes the next payment with probability p and the other one with probably 1 - ip. All payments of equal size. You can then derive a formula and obtain the optimal distribution of money. This problem gets harder if you add more node sand the distribution of money and amounts gets more complex.

Finally, you have the actual rebalancing problem. You have optimal distribution of money problem, and then you have to choose when to move your money from one channel to another and this involve bitcoin fees or LN fees. So this is the rebalancing problem.

## Simulation model

Now that we have some understanding of the rebalancing problem, I'm going to talk about rebalancing costs, which was based on a simulation model where we're a LN routing node and we're connected to other nodes, we have some amount of money available, we're connected to a set of peer nodes that are transacting with each other following a random process in which they follow a payment rate matrix where the probability of node i making the next payment to j is made by a payment rate matrix. And, the payment amounts follow a certain given distribution as part of the input.

How does the amount of money locked impact the need for rebalancing?

How does rebalancing costs add to the total costs of having a routing node? What is the optimal amount of money we must lock inside a node in order to be the most competitive? The rebalancing costs decrease linearly it's the inverse of amount of money locked and the financial costs increases linearly with the amount of money locked so you get this optimal amount of money where your node becomes the most competitive.

How does the bitcoin fees impact the lightning network fees?

## Conclusions

All routing nodes in the LN will face the rebalancing problem and its costs. Routing nodes will be economically incentivized to correctly predict payments weather. Linear fees make sense in the LN. The optimal amont of money to be locked inside channels will grow with the bitcoin fees. Lightning fees will grow with bitcoin fees.
