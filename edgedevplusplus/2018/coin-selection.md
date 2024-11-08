---
title: Coin Selection
transcript_by: Bryan Bishop
tags:
  - coin-selection
speakers:
  - Kalle Alm
media: https://www.youtube.com/watch?v=ZMzVIi1lgyw
date: 2018-10-04
aliases:
  - /scalingbitcoin/tokyo-2018/edgedevplusplus/coin-selection
---
<https://twitter.com/kanzure/status/1047708247333859328>

# Introduction

I am going to do a short talk on coin selection. Everyone calls me kalle. In Japanese, my name is kalle. Coin selection, what it is, how it works, and interestingly enough- in the latest version of Bitcoin Core released yesterday, they have changed the coin selection algorithm for the first time since a long time. They are now using something with more scientific rigor behind it (branch-and-bound coin selection), which is good news.

# Concept

The concept behind coin selection is that... you receive bitcoin in transactions, you've heard about this. The bitcoin we hold we refer to them as outpoints, which are (txid, output index). You have the transaction id and then an index inside of that transaction. It's the index in the output list on that transaction. The outpoint is something that we own. Even if we use the same address (which we shouldn't) to receive multiple times, each one will have a different outpoint, even if the transaction is similar to a previous transaction. You never have the same outpoint for two separate UTXOs, even if someone sends you money to the same address in the same transaction multiple times. You still have a distinction between these two outpoints because the first one has a lower index and the other one has a higher index.

When we talk about "balance" in the wallet, is that we're talking about the sum of all of our outputs and all the coins in there. It's like change at the cash register. You have to find the right combination of coins in order to spend the certain amount of money. However, in bitcoin, you can create your own coin face values. You have to create a new coin for yourself as the change output. You send the rest to the receiver and also miner fees.

# Coin selection goals

Ideally, we want to minimize the number of coins we spend at any one time, for several reasons. Every time we "aggregate" coins together, we connect the histories of the two outpoints to one owner. We pay fees based on the transaction fee, and more coins means bigger sizes and thus more fees. By associating coins together, you are actually degrading the privacy of the system.

We're also incentivized to try to find coins so that the input is about the same as the output. If we manage that, then we can skip making a new change output, which means a smaller transaction. This means lower fees.

The process of running this optimization over coins is called "coin selection".

# Branch and bound

A lot of changes in coin selection were deployed in Bitcoin Core v0.17; it's branch-and-bound or otherwise called Murch's algorithm because Murch is the guy who proposed it and one of the developers who worked on it. The old version was called Knapsack solving using subset sum approximation.

If someone is sending you money to the same address more than once, and you spend one of those UTXOs partially with 10 other coins, then you have told the world that these coins belong to the same person. There are ways to identify these same patterns. It degrades privacy. You always want to spend these coins together, or not at all. If you have three coins all corresponding to a single pubkey, then you should use "grouping" and spend all of those coins at the same time.

# Knapsack solver

The knapsack solver was the old implementation. The idea behind the knapsack solver was bruteforcing the coin selection problem. You randomize the set of coins, which is good for privacy so we always want to do that. Then we try coin selection a bunch of times and we try to see how good the result is based on total fees and size, and then the tries are iterated multiple times. For big wallets, this is time intensive. This is what Bitcoin Core was using up until v0.17.

In more detail, coins are selected by shuffling the coins, iterating over the coins, and if the coin value is equal to the target, you return the coin immediately. If the coin value is less than the target, you put it in the "value" list and add its value to the total. Otherwise, if the coin value is less than the smallest previous coin larger than target, then you mark it as "smallestHigher". If the sum of the total == target, then return the "value" list. If the sum is less, and there is a marked coin marked as smallestHigher, then return the marked coin.

You want to find a coin that is as close to the target as possible, but higher. If it's lower then it doesn't meet the payment requirement, but if it's higher then you can break it into change later.

The knapsack solver uses subset sum approximation. You keep repeating over and over again, in this case 1000 times. What we do is, and this is very bruteforce... you go through the coins twice. And include the coins if a random boolean is true, or if this is the second pass and the coin has not been included yet. If the target was reached, then see if the total beats the high score (by being smaller), and keep the solution if so.

All of this is done about 7 times, with different parameters. It prefers not to use recently confirmed or unconfirmed coins, or coins in a long unconfirmed chain. It will try to prefer coins that are confirmed. Stuff like that. It does these various iterations of the same algorithm.

# Branch and bound

The branch-and-bound coin selection algorithm is a little more sophisticated and more efficient. The idea here is to use effective value per UTXO and use efficient search for exact matches. It uses a binary tree to represent un-selected UTXOs. It does a depth-first search. One of the goals is to minimize a waste metric based on cost - long-term expected cost + excess amount.

When you're sending coins, you're not only spending coins and getting money back, but in the future you're going to spend the coins that you're spending back to yourself. You want to see what the long-term versus short-term fees are for those coins, which gives you a better prediction about how wasteful it is to spend in these ways. You might be creating UTXOs that are going to be dust, or spending a future coin might cost you money. So you do this depth-first exhaustive search in branch-and-bound and there's a waste metric and we just try to minimize that waste metric. It's very straightforward.

So there's both long-term and short-term fee rates in this algorithm. The long-term feerate is the minimum expected fee rate in the far future like 1008 blocks in the future. Get the cost of spending a resulting change output. Calculate the fee, the long-term fee, and effective value for all "eligible" inputs. Discard any inputs with a non-positive effective value. The effective value is just the face value minus the fee. Some of them will cost you money to spend, and are not really worth their face value.

Backtrack if we cannot reach target with remaining available value, selected value is out of range, or if we are more wasteful than the best solution. Record and backtrack if within range of hte target. Otherwise, iterate (unless we're already backtracking).

The branch and bound solver is also a bit of a knapsack solver. The previous implementation was more of a random heuristic, and not specifically an optimal knapsack solver.

# Branch and bound: Backtracking

I said it's a binary tree, but really it's a boolean vector that we add true or false to. True means it's enabled, false means it's disabled. This is for UTXOs. So we remove "unset" (false) entries from the current selection until we encounter a "set" (true) entry, or until out of entries. If the current selection list is empty, then we stop looping (all branches have been traversed). Unset the last entry in the list, and the nremove corresponding effective value from current\_value, and remove corresponding waste from current\_waste.

# Branch and bound: recording

Recording is just add the excess value (value - target) to the waste value. If the resulting waste is less than the best waste, then store the current selection as the best selection.

# Branch and bound: termination

If we don't have a selection that works at all, if there is no best selection at all, fail, otherwise return the best selection and convert the bools.

# References

* <http://murch.one/wp-content/uploads/2016/11/erhardt2016coinselection.pdf>
* <http://diyhpl.us/wiki/transcripts/scalingbitcoin/milan/coin-selection/>
