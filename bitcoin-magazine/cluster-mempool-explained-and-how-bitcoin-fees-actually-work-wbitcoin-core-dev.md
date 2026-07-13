---
title: 'Cluster Mempool Explained & How Bitcoin Fees Actually Work w/Bitcoin Core Dev'
transcript_by: 'satoshiplanet via review.btctranscripts.com'
media: 'https://youtu.be/jSkTsPquAPE?si=La7KLwM1JNht8bOv'
date: '2026-02-02'
tags:
  - 'cluster-mempool'
  - 'rbf'
  - 'cpfp'
  - 'fee-estimation'
  - 'transaction-pinning'
speakers:
  - 'Pieter Wuille'
  - 'Shinobi'
categories:
  - 'Mining'
  - 'Transaction Relay Policy'
  - 'Fee Management'
source_file: 'https://youtu.be/jSkTsPquAPE?si=La7KLwM1JNht8bOv'
summary: 'Pieter Wuille and Shinobi discuss cluster mempool, now merged into Bitcoin Core for the 31.0 release. The conversation covers why the original mempool had conflicting orderings for mining vs eviction, how cluster mempool solves this by partitioning related transactions into clusters of at most 64 transactions and running an optimal ordering algorithm on those small groups, and how this enables a globally consistent pre-computed total ordering that improves replace-by-fee incentive compatibility, fee estimation, multi-child CPFP, and transaction relay rate limiting. The talk also covers the historical progression of mempool improvements and how optimal ordering within bounded clusters future-proofs the mempool for arbitrary layer 2 use cases like Lightning and Ark.'
---

## Why Bitcoin’s Mempool Has Been Broken

# Cluster Mempool Explained & How Bitcoin Fees Actually Work

**Guest:** Peter Wuille (`Chaincode Labs`)

**Host:** Shinobi (`Bitcoin Magazine`)

Recorded: 2026

---

## Introduction

**Shinobi (00:00:00)**

Well, everybody.

I'm Shinobi, technical editor at `Bitcoin Magazine`, joined by Peter Wuille of `Chaincode Labs`.

So we're here to discuss your latest obsession over the last few years: `cluster mempool`.

This is definitely not the first time we've talked about this.

**Peter Wuille (00:00:34)**

I hope it's among the last times I need to talk about it.

Now that the changes have actually been merged into `Bitcoin Core`, with plans for them to be included in the `31.0` release later this year.

**Shinobi (00:00:48)**

I can imagine that's a familiar feeling for you at this point.

**Peter Wuille (00:00:53)**

It's been a long project.

I've had many big projects over the past few years, but it's still a big one, and it's good to have it off my plate.

**Shinobi (00:01:08)**

So you and Suhas Daftuar kind of conceptualized this, I think, about three years ago now?

**Peter Wuille (00:01:16)**

Yeah.

I think it started from a discussion we had here in the office in February 2023.

We were thinking about all the problems the current `mempool` has.

In fact, I think it was inspired by a talk Suhas gave internally, discussing the problems with the `mempool`.

This isn't the only one, but it's a nice demonstration of how things are broken.

The issue is that the current mining algorithm uses one ordering, while the eviction algorithm—the one that decides which transactions to remove when the `mempool` fills up and memory runs out—uses a different ordering.

---

## The Core Problem with Transaction Ordering

**Peter Wuille (00:02:16)**

That was necessitated by the design of the code at the time, but it was still surprising.

The real problem is that you'd hope the mining algorithm selects transactions in descending `feerate` order while respecting topology.

Of course, the `mempool` can contain dependent transactions.

I might pay you in an unconfirmed transaction, and then you immediately spend those coins in another transaction.

Now we have a child transaction, and there's logic that evaluates both together if the child pays a higher `feerate`.

That's the `Child Pays For Parent (CPFP)` concept.

The block-building algorithm in `Bitcoin Core` has taken all of this into account since 2015.

It comes up with a fairly good ordering—not perfect, and we'll get into that later—but generally from higher `feerate` to lower `feerate`, with parents always appearing before their children.

Ideally, when memory runs out, you would evict transactions in exactly the reverse order.

The first thing you evict should be the very last thing you would want to mine.

---

## Why Eviction Logic Failed Under Load

**Peter Wuille (00:04:05)**

That makes sense.

And that's true in most cases.

However, you can construct pathological transaction constellations inside the `mempool` where it isn't true.

In very extreme cases, Suhas discovered that the first thing you evict can actually be the first thing you would mine.

Which is obviously bonkers.

That's clearly not what we want to throw away.

I'm not saying this is the only problem, or even the most important one.

It's simply a very good demonstration that what we really want internally is a single, well-defined ordering across all transactions.

**Shinobi (00:05:04)**

If you want predictability, you want to know that the same thing will always happen under the same conditions.

**Peter Wuille (00:05:09)**

Right.

The real question is: why are those orderings different?

The answer is that, in order to determine what should be mined last, you'd effectively have to run the mining algorithm over a block that's almost the size of the entire `mempool`, and then see what was left out.

That would work.

Unfortunately, it's computationally infeasible.

So the obvious question became: what if we could precompute it?

## The Limits of Heuristics in `Bitcoin Core`

**Peter Wuille (00:05:57)**

What if, instead of running the mining algorithm only when a block template is built—which is all a miner normally does—we ran it ahead of time?

Whenever a change is made to the `mempool`, we maintain a complete ordering of every transaction at all times.

If that ordering is already precomputed, block building becomes trivial.

You simply select transactions from the front of the list, while eviction happens from the back.

But there are many more places throughout the `Bitcoin Core` codebase where we try to determine—using heuristics that are often incorrect and inconsistent—whether one transaction is better than another.

Suppose a flood of transactions reaches your node, as we've seen happen in the past.

There's a rate-limiting mechanism that prevents every transaction from immediately being relayed to all of your peers and overwhelming the network.

That means you have to decide which transactions to relay first.

Naturally, you want to relay the better transactions first.

The problem is that the node doesn't actually know which ones are better, because determining that accurately would be computationally too expensive at that moment.

There are more examples.

For `feerate` estimation, it would be useful if the estimator could take `CPFP` into account.

Today it can't, because it lacks information about the adjusted goodness—or effective `feerate`—of transactions.

We eventually realized that there are many different places throughout the codebase where we're independently trying to compare the quality of transactions using different heuristic approaches.

Another example is fee bumping inside wallets.

There's similar logic there as well.

---

## `Replace-By-Fee` and Incentive Compatibility

**Speaker 1 (00:08:18)**

What we really need is a way to precompute a total ordering.

Once we have that, all of these problems become dramatically simpler.

Probably the biggest example is `Replace-By-Fee` (`RBF`).

When a replacement transaction arrives, the node has to determine whether accepting the new transaction—and evicting every conflicting transaction—is actually an improvement.

Today that decision is governed primarily by `BIP 125`.

Those rules are still followed, but they're heuristic and imperfect.

There are situations today where you can replace a transaction with one that's objectively worse, and it will still be accepted.

Likewise, there are objectively better replacement transactions that get rejected for arbitrary reasons.

**Speaker 0 (00:09:32)**

Yeah.

It's basically the difference between looking at absolute fees versus `feerates`, taking transaction size into account and how all of that is calculated.

**Speaker 1 (00:09:41)**

Right.

That's one aspect of it, but it's orthogonal.

If we look at the replacement rules themselves, they really fall into two categories.

The first is incentive compatibility.

Does accepting this new transaction improve the `mempool` and increase miner revenue?

The second category is denial-of-service protection.

When a transaction replaces another one, we effectively charge the new transaction for the bandwidth and relay cost that nodes already spent propagating the original transaction, which we now expect won't be mined.

That's why there's an absolute fee increase requirement.

---

**Speaker 0 (00:10:14)**

Right.

It's basically accounting for bandwidth costs.

**Speaker 1 (00:10:17)**

Exactly.

The goal is to prevent attackers from using the Bitcoin peer-to-peer network as a free relay service.

**Speaker 0 (00:10:28)**

You're effectively forcing them to pay at least as much as the relay network has already spent forwarding the transaction.

The nodes aren't literally being compensated, but the attacker is at least bearing the cost.

**Speaker 1 (00:10:38)**

Right.

Ideally, transaction relay itself would be economically compensated.

But that really doesn't...

**Speaker 0 (00:10:50)**

If you figure that one out, let me know.

We can finally replace Bitcoin.

**Speaker 1 (00:10:55)**

I believe there was a very early research paper—the "Red Balloons" paper—that tried to solve this problem, although I don't remember the details.

In any case, even if such a solution exists, it's probably undesirable.

If relaying transactions carried direct fees, people would simply bypass the public relay network and submit transactions directly to miners.

That's exactly the opposite of what we want.

So the `Replace-By-Fee` rules consist of two separate parts.

One deals with incentive compatibility.

The other deals with denial-of-service protection.

We're not changing the denial-of-service rules.

But the incentive compatibility rules we have today are wrong in both directions.

They sometimes accept objectively worse transactions, and they sometimes reject objectively better ones.

With a proper framework for comparing transaction quality—which involves more than simply ordering transactions and instead compares how fees grow relative to transaction size—we can solve all of these problems within the `cluster mempool` framework.

## Why the Current Mempool Cannot Maintain a Global Ordering

**Speaker 1 (00:11:41)**

The current incentive compatibility rules will sometimes accept transactions that are objectively worse, and they'll reject many that are objectively better.

A proper framework for reasoning about transaction quality requires more than simply ordering transactions.

It really comes down to comparing diagrams that describe how fees increase relative to transaction size.

The `cluster mempool` framework ultimately solves all of these problems simultaneously.

So we wanted to impose a total ordering that could be precomputed.

But, as I explained earlier, we can't simply run a `mempool`-sized version of the block-building algorithm every time the `mempool` changes.

Unfortunately, with the current design, it's theoretically possible for a single newly relayed transaction to completely change the optimal ordering of every transaction already in the `mempool`.

It can even reverse the entire ordering.

Imagine a chain of dependent transactions: parent, child, parent, child, parent, child.

Initially, the optimal mining order is simply the first transaction, then the second, then the third, and so on.

Now imagine adding a single transaction with a very high `feerate` at the end of that chain.

Suddenly, the optimal ordering changes completely.

**Speaker 0 (00:13:19)**

Everything gets reordered.

**Speaker 1 (00:13:20)**

Exactly.

That's a problem because it means that every time a single transaction is received, you potentially have to recompute the ordering of an entire `mempool` that could contain hundreds of megabytes of transactions.

The solution is to restrict how many transactions any new transaction can affect.

That's where the term `cluster` comes from.

The idea is to partition the `mempool` into groups of related transactions.

---

## Introducing `Clusters` and the 64-Transaction Limit

**Speaker 1 (00:13:54)**

Those relationships include parents, children, ancestors, descendants, descendants of ancestors, ancestors of descendants, and every other indirect relationship.

If two transactions can be connected through any sequence of parent-child relationships, they belong to the same `cluster`.

**Speaker 0 (00:14:20)**

So it's basically like a family tree.

**Speaker 1 (00:14:24)**

Exactly.

If there's even the slightest relationship between two transactions, you treat them as members of the same family.

Parents, grandparents, children, grandchildren, uncles, cousins—everything belongs to the same `cluster`.

Previously, the `mempool` enforced several resource limits.

By default, a transaction could have at most 25 ancestors—including itself—and at most 25 descendants—including itself.

Those limits existed because the mining and eviction algorithms had to repeatedly process ancestor and descendant sets, and the computational cost grew quickly.

I won't go into the implementation details.

With the new design, those limits disappear completely.

Instead, they're replaced with a single rule:

A `cluster` may contain at most **64 transactions**.

The limit is larger than before, so longer transaction chains become possible.

But the rule now applies to the entire family rather than independently to ancestors and descendants.

**Speaker 0 (00:15:49)**

So it isn't directionally limited anymore.

It's simply limited by the total size of the family.

**Speaker 1 (00:15:52)**

Exactly.

Your entire family can contain at most 64 transactions instead of separately limiting ancestors and descendants.

We've analyzed historical `mempool` data, and it appears that very few existing transaction patterns would be affected by this new policy.

At the same time, it enables transaction structures that weren't previously possible.

So the overall idea is straightforward.

We partition the `mempool` into `clusters` of at most 64 transactions.

That becomes a policy rule.

If a new transaction would cause a `cluster` to exceed 64 transactions, the node simply rejects it.

Whenever anything changes within a `cluster`—a transaction is added, transactions are mined, a `reorg` occurs, or a replacement transaction modifies the graph—we rerun the ordering algorithm.

But we only rerun it for that single `cluster`.

Since every `cluster` contains at most 64 transactions, the computation remains fast.


## How `Cluster Mempool` Enables Optimal Ordering

**Speaker 1 (00:17:04)**

Because each `cluster` is so small, recomputing the ordering is fast.

In practice, all we really need is the ordering within each group of related transactions.

The overall ordering of the `mempool` is then just a simple merge of all those individual cluster orderings.

That merge can be performed whenever it's needed.

The computationally expensive part has now been reduced to groups of at most 64 transactions.

Whenever a `cluster` changes, we rerun the ordering algorithm only for that `cluster`.

At this point it's no longer really a mining algorithm.

It's simply an algorithm that determines the optimal ordering of transactions within a `cluster`.

Once we had that, the obvious next question was whether we could improve the algorithm itself.

As I mentioned earlier, the existing block-building algorithm is suboptimal in several ways.

That isn't necessarily a serious problem today, but if we're already recomputing orderings only for groups of 64 transactions, we have enough computational headroom to do something much better.

Take `Child Pays For Parent` (`CPFP`) as an example.

The current implementation works correctly when a single child transaction increases the effective `feerate` of its parent.

Those two transactions are evaluated together, exactly as intended.

What it doesn't handle correctly is multiple children paying for the same parent.

Suppose a parent has two children, both paying higher `feerates`.

The current algorithm considers only whichever child has the greatest effect.

It doesn't evaluate the combined effect of both children increasing the parent's effective `feerate` together.

**Speaker 0 (00:19:19)**

That's a pretty big blind spot.

**Speaker 1 (00:19:22)**

I wouldn't necessarily call it a problem.

**Speaker 0 (00:19:24)**

Maybe "blind spot" is the better way to put it.

**Speaker 1 (00:19:25)**

Exactly.

I don't think it matters very much in practice today, because people don't design applications that rely on something the network doesn't support.

But for the last couple of years, on and off, that's been one of my main areas of research.

The question has been:

Given a `cluster` containing at most 64 transactions, how do we determine the optimal order in which to mine them?

---

## Future-Proofing Bitcoin for New Use Cases

**Speaker 0 (00:20:15)**

People use Bitcoin because they want an alternative monetary system.

But for Bitcoin to remain that alternative, people have to continue maintaining and improving it.

If you want to hear directly from developers about how they approach these problems and why they choose to work on them, go to `bitcoinmagazine.com` and pick up a copy of the *Core Issue*.

So, if I understand correctly, you've built this entirely new architecture for organizing and ordering the `mempool`.

Now the remaining question becomes:

What's the mathematics behind deciding the optimal ordering?

**Speaker 1 (00:21:18)**

Exactly.

When we first proposed `cluster mempool`, the goal was simply to take the existing block-building algorithm and run it ahead of time on groups of 64 transactions instead of on the entire `mempool` during block construction.

But once we realized we'd only ever be working with groups of at most 64 transactions, it became obvious that we could do something much better.

In practice, we can now almost always compute the optimal ordering.

And that's pretty neat.

**Speaker 0 (00:21:52)**

I'd say that's considerably more than "pretty neat."

From a long-term perspective, having an open, optimal, profit-maximizing algorithm that anyone can use seems like a huge improvement for the network.

**Speaker 1 (00:22:06)**

Exactly.

Originally our goal wasn't necessarily mathematical optimality.

It was simply to handle every transaction pattern that people actually use.

If all anyone ever does is ordinary `CPFP` fee bumping, then you only need an algorithm that handles that case correctly.

But nobody knows what kinds of applications, protocols, or economic incentives people may invent in the future.

They might discover entirely new transaction topologies.

If the algorithm is genuinely optimal, then it doesn't matter.

As long as everything stays within the 64-transaction `cluster` limit—and continues to satisfy the denial-of-service policy rules—it will always compute the correct ordering.

Whatever future use case people invent, the algorithm will still choose the economically optimal ordering.

## Incentives, `Layer 2`, and the Long-Term Evolution of Bitcoin

**Speaker 0 (00:23:09)**

So it's essentially future-proof.

It gives you the flexibility to continue optimizing the system as new `Layer 2` protocols, network behaviors, or metaprotocols emerge.

**Speaker 1 (00:23:22)**

Exactly.

Whatever new use case someone invents, the behavior of the node simply becomes:

"If it's better, I'll accept it. If it isn't, I won't."

The algorithm can determine which transaction package is better regardless of its topology, provided it remains within the 64-transaction `cluster` limit.

**Speaker 0 (00:23:45)**

That sounds like a huge improvement, especially for `Layer 2` protocols.

It provides much stronger guarantees for systems like the `Lightning Network`, `Ark`, or other reactive protocols, where participants may have to respond quickly to another party's transactions.

They need confidence that, if they broadcast a transaction, it will actually outcompete or replace the transaction it's intended to replace.

**Speaker 1 (00:24:18)**

That's true.

Although I wouldn't necessarily describe it as becoming more predictable.

It's predictable in a different sense.

At a very high level, the rule becomes extremely simple.

---

## Incentive Compatibility Instead of Rule-Based Heuristics

**Speaker 1 (00:24:35)**

Whatever you're trying to do must increase fee revenue.

If it does, the node will accept it.

How that decision is reached becomes something of a black box.

Previously we had the `BIP 125` replacement rules.

They weren't perfect, but they gave users a checklist.

If your replacement transaction satisfied rule one, rule two, rule three, and so on, it would probably be accepted.

That isn't really true anymore.

The new rule is much simpler:

Make the transaction package better.

Figure out how to do that.

In practice, I don't think this creates difficulties.

If you're working with a transaction package entirely under your own control—for example, within the `Lightning Network` or another `Layer 2` protocol—you can simply run the same algorithm yourself and verify whether the replacement will succeed.

Things become more interesting when another party can attach transactions to yours.

Suppose I create an unconfirmed output that belongs to someone else.

That person can now attach arbitrary descendant transactions.

If I later need to increase the fee of my original transaction, what I have to do now depends on the additional transactions they've attached.

That certainly makes reasoning about replacements more complicated.

But it's also a much cleaner model.

Most importantly, it aligns transaction relay with the actual economic incentives of the network.

Previously we relied on arbitrary heuristic rules that weren't always economically correct.

There was never any guarantee that miners would continue following those rules forever.

With this framework, the incentives themselves naturally lead everyone toward the same behavior.

---

**Speaker 0 (00:26:45)**

From my perspective, this feels like the latest step in a long process of cleaning up historical inconsistencies in the `mempool`.

Originally there was the `First-Seen-Safe` rule.

Then `Replace-By-Fee` was introduced as an opt-in feature, where transactions had to explicitly signal that they could be replaced.

But miners were already replacing transactions that weren't even signaling `RBF`.

Throughout the entire time I've been involved with Bitcoin, we've gradually been removing assumptions that were never really enforced by miner incentives.

**Speaker 1 (00:27:20)**

Do you remember transaction priority?

**Speaker 0 (00:27:22)**

Back when a percentage of every block was reserved for zero-fee transactions, provided they'd accumulated enough priority.

**Speaker 1 (00:27:29)**

Exactly.

If a transaction had destroyed enough coin age per byte, it could be included without paying fees.

That probably made sense in Bitcoin's earliest years.

At the time, it was a reasonable prioritization mechanism.

But it simply wasn't sustainable.

**Speaker 0 (00:27:51)**

Once block space became genuinely scarce and valuable, no rational miner would continue following that policy.

**Speaker 1 (00:28:00)**

Exactly.

Over the years we've taken many small steps in this same direction.

---

## Closing Thoughts

**Speaker 0 (00:28:07)**

It's a necessary evolution.

If Bitcoin depends on economically rational participants acting in their own self-interest, then the protocol should align itself with those incentives.

Otherwise, why would we expect the system to function correctly over the long term?

**Speaker 1 (00:28:20)**

Exactly.

**Speaker 0 (00:28:21)**

I think you've given an outstanding explanation.

Hopefully most people watching will actually come away understanding what `cluster mempool` is.

So thanks very much for taking the time, Peter.

**Speaker 1 (00:28:32)**

My pleasure.

**Speaker 0 (00:28:34)**

And I hope all of you learned something.

Thanks for watching.

**Speaker 1 (00:28:37)**

Bye.