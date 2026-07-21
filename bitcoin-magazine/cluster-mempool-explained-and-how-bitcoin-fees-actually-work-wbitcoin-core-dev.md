---
title: 'Cluster Mempool Explained & How Bitcoin Fees Actually Work w/Bitcoin Core Dev'
speakers:
  - Pieter Wuille
  - Shinobi
tags:
  - cluster-mempool
  - rbf
  - cpfp
  - fee-estimation
  - transaction-pinning
categories:
  - Mining
  - Transaction Relay Policy
  - Fee Management
date: '2026-02-02'
source_file: https://youtu.be/jSkTsPquAPE?si=La7KLwM1JNht8bOv
media: https://youtu.be/jSkTsPquAPE?si=La7KLwM1JNht8bOv
transcript_by: 0tuedon via tstbtc v1.0.0 --needs-review
summary: Pieter Wuille and Shinobi discuss cluster mempool, now merged into Bitcoin Core for the 31.0 release. The conversation covers why the original mempool had conflicting orderings for mining vs eviction, how cluster mempool solves this by partitioning related transactions into clusters of at most 64 transactions and running an optimal ordering algorithm on those small groups, and how this enables a globally consistent pre-computed total ordering that improves replace-by-fee incentive compatibility, fee estimation, multi-child CPFP, and transaction relay rate limiting. The talk also covers the historical progression of mempool improvements and how optimal ordering within bounded clusters future-proofs the mempool for arbitrary layer 2 use cases like Lightning and Ark.
---

## Why Bitcoin’s Mempool Has Been Broken

Speaker 0: 00:00:06

Hello, everybody.
I'm Shinobi, technical editor at Bitcoin Magazine, joined by Peter Wullie of Chaincode Labs.
So we are here to discuss your latest obsession over the last few years, Cluster Manpool.
This is definitely not the first time We've talked about this.

Speaker 1: 00:00:34

I hope it's among the last times I need to talk about it now that the changes have actually been merged in Bitcoin Core with plan to be in the 31.0 release later this year.

Speaker 0: 00:00:48

I can imagine that's a familiar feeling with you at this point.

Speaker 1: 00:00:53

It's been a long project.
I mean, I've had many big projects over the past few years, but I mean, it's still a big one that it's good to have off my plate.

Speaker 0: 00:01:08

So you and Suha's staff tour kind of conceptualized this, I think, three years ago now, roughly?

Speaker 1: 00:01:16

Yeah, I think it was a discussion we had in the office here in February, 2023, where we're thinking about all the problems that the current Mempel has.
And in fact, I think this was inspired by a talk Suez gave to us here internally, just talking about the problems the Mempel has.
And among them, it's not the only one, but I think it's sort of a nice demonstration of how things are broken.
And that's really the difference between how in the current mining algorithm we use one ordering and when deciding what transactions to remove from the mempool when it fills up and you don't have enough memory anymore, we use a different ordering.

## The Core Problem with Transaction Ordering

Speaker 1: 00:02:16

This was necessitated by the design of the code at the time, but it was still surprising.
So in a bit more detail, when, and jumping ahead, The real problem is that you would hope that the mining algorithm picks the transaction in some order, going from higher fee rate to lower fee rate order, but respecting topology, because of course we can in mempool have dependent transactions where you have you know I pay you in an unconfirmed transaction and then you use those coins and spend them further to pay for something so now we have child transaction and there's logic in there so that if your transaction pays a higher fee rate, these two will be considered together and we'll have that's the child pays for parents concept.
So all of that block mining algorithm in Bitcoin Core today and as it has been since 2015, has taken all of this into account.
So it roughly comes up with a good ordering, not perfect, we'll get into that later, but fairly good, going from higher fee rate to lower fee rate with parents always before their children.
And you would hope that when memory runs out, you start evicting transactions that would be considered last by this order.
The very last, the first thing you want to evict is the last thing you would want to mine.

## Why Eviction Logic Failed Under Load

Speaker 1: 00:04:05

This makes sense.
And that's true in most cases, but you can construct pathological examples of constellations of transactions within a mempool where this is not the case.
And in very extreme cases, in fact, it appeared to be possible.
Suhas discovered this, that the very first thing you evict is the last thing, is the first thing you would you would mine, which is obviously bonkers.
That's not what we want to throw away.
And I don't say that this is the only problem or even the most important one.
Even the most important one, it just is a nice way of showing that what we really want inside is a well-defined single ordering on all transactions.

Speaker 0: 00:05:04

If you want predictability, you want to know this is going to always happen in these conditions.

Speaker 1: 00:05:09

Right.
The real problem, why are these orderings difference?
Well, the reason is roughly that in order to decide what you'd want to mine last, you basically need to run the mining algorithm for like a mempool minus Epsilon sized block and then see what you didn't mine and well if it that that would work But sadly this is computationally infeasible with all the transactions in there.
So and and so well what happens if you're faced with a problem?
Well, we need a fixed ordering, but it is too computationally expensive to do.
Well, what if we could pre-compute things?

## The Limits of Heuristics in Bitcoin Core

Speaker 1: 00:05:57

What if instead of just running the mining algorithm at the time a block template is built, and that's only what a miner would do.
We in fact do it ahead of time.
Whenever a change is made to the mempool, we in fact keep a total ordering on all transactions in the mempool at all times.
And if we have this pre-computed, well, then block building is easy.
You pick from the front, eviction is from the end.
But there are many more examples of parts of the Bitcoin core codebase that in one way or another try to assess with a heuristic that's often incorrect and often inconsistent, is this transaction better than this one?
Say there is a flood of transaction that come into your node, as we've seen a year or two ago, there have been such floods.
There's a rate limiting process that will prevent that flood from being propagated to all your peers and having them be overwhelmed too.
So you need to make a decision which transactions are you going to send first.
Obviously the better one you want to send first.
But it doesn't know that because we can't certainly at that time don't have computationally the time to go determine what things are.
But there are even more examples like for fee rate estimation, it would be nice if fee rate estimation could take CPFP into account.
It can't do that because it would need this information of adjusted goodness or effective fee rate as we call it of transactions.
And so all these problems we realized, in fact, that there's a whole bunch of ways that we're trying to compare quality of transactions with each other inside the code base in many different ways all heuristically and all done independently.
Another one is when fee bumping transactions in the wallets.
There's similar logic there.

## Replace-By-Fee and Incentive Compatibility

Speaker 1: 00:08:18

And we really need to come up with a way to pre-compute this total ordering and if we have that then all these problems become so much simpler.
Oh, the biggest one of all, replace by fee.
If you have a transaction that comes in, that replaces another one, you need to know whether taking this new transaction and evicting all the things it conflicts with is actually an improvement.
There's a bit 125 rules which are so sort of followed still, but they are heuristics and they are imperfect in many ways.
There are ways today that you can replace a transaction with one that is just unambiguously worse and gets accepted.
And similarly, many ways that you can have an unambiguously better transaction come in and will reject it for arbitrary reasons.
Yeah, just difference between like absolute fee and fee rates, looking at size and how that's computed.
So that is one, but that's orthogonal.
So the replacement rules, if we're going into that, sort of boil down into two categories.
One is incentive compatibility in the sense of, does taking this transaction make things better for the mempool, the miner, in terms of fee income.
And there's another set of rules which are about denial of service protection.
So we want when a transaction replaces another one, we sort of charge the new transaction a fee for the cost of having relayed the old transaction which will now not, as we expect it, won't end up in a block anymore.
And so there's an absolute fee increase requirement that comes from there.

Speaker 0: 00:10:14

Yeah, kind of just looking at bandwidth cost.

Speaker 1: 00:10:17

Yes.
This is just to prevent, you know, enabling avenues for an attacker to use the Bitcoin peer-to-peer network as a free relay mechanism.

Speaker 0: 00:10:28

You're effectively at least imposing as much cost on them as relaying nodes is going to pay.
So it's it's not like the nodes aren't being compensated but they're still bearing the cost.

Speaker 1: 00:10:38

Right.
Ideally we'd have the transaction relayers receive the income for relaying transactions but that really doesn't...

Speaker 0: 00:10:50

If you figure that out let me know we can finally replace Bitcoin.

Speaker 1: 00:10:55

I do believe there was a very early research paper called the red balloons paper that tried to do this, but I don't recall how it worked.
In any case, it's just not a practical problem.
Or rather, even if you have a solution for it, it's not a desirable outcome because it just means you will try to bypass the relay network that charges you a fee to relay and send it to miners directly, which is the very opposite of what we want to achieve.
So, replaced by fee rules, you have the incentive compatibility ones and you have the denial of service ones.
We're not touching the denial of service protection rules, but the incentive compatibility ones today are wrong in both ways.

## Why Recomputing the Entire Mempool Is Impossible

Speaker 1: 00:11:41

Like they will accept things that are worse and they will reject many things that are better.
And with sort of a framework of reasoning properly about how good transactions are with respect to each other, this involves a bit more than just ordering them.
Sort of boils down to drawing a diagram of how the fee increases with a size and comparing those diagrams.
But still, the cluster mempool framework in the end is a solution to all these problems at the same time.
And so, all right, we want to impose a total ordering that we can pre-compute, but sadly, already explained, like we can't just run a mempool-sized version of the block building algorithm to determine the full ordering of everything at all times.
And sadly, as things stand today, it's in theory possible to relay a single transaction and completely change the optimal ordering of every transaction in the mempool.
Completely reverse it, for example, we have an example.
Like given this chain of transactions sideways, like parent-child, parent-child, parent-child.
The ordering is like you first mine this, then this, then this, then this.
Now you add one very high fee rate transaction to the end and suddenly it's this, this, this, this, this,

Speaker 0: 00:13:19

this, this.

Speaker 1: 00:13:20

So that's a problem because that means we need to deal with a case of the single transaction is being relayed to you and you need to recompute the ordering of everything in your mempool, however big it is, maybe hundreds of megabytes.
And the solution to this is, well, what if we can just restrict how many transactions can be affected by any given new transaction coming in?
And that's where the term cluster comes from.
So we partition, the idea is to partition the mempool into groups of related transactions.

## Introducing Clusters and the 64-Transaction Limit

Speaker 1: 00:13:54

And this includes parents, children, ancestors, descendants but also descendants of your ancestors and their ancestors and their descendants and so forth.
So anything that can be reached or any two transactions that are related by an arbitrary combination of parent of child of steps, they are considered to be in the same cluster.

Speaker 0: 00:14:20

It's like a family tree, like visually.

Speaker 1: 00:14:24

Yeah, like there's even the slightest relation between them that you think of them as the same.
So it's your parents, your grandparents, your children, your grandchildren, but also your uncles, your nieces, your cousins, your everything.
And the idea is simple.
Instead, so the previous mempool had some resource limitation rules.
The default was that we would impose, among other things, at most 25 ancestors, including the transactions itself, and at most 25 descendants, including the transaction itself.
And this is related directly to the computational cost of the mining algorithm and the eviction algorithm, which needed to operate on these sets of ancestors and set of descendants.
I won't go into the details here.
Anyway, so with this new approach we're replacing them.
Those rules go away completely and they are replaced instead with a rule that clusters can be at most 64 transactions.
Number is a bit bigger, so it does mean that you can build longer chains of transactions than 25.
But of course, it now works both ways.
And so it's not...

Speaker 0: 00:15:49

It's not directionally bound, it's just total size.

Speaker 1: 00:15:52

Yes.
And your family can be at most 64 transactions rather than just your ancestors or just your descendants.
Based, we've done analysis on historical weight of the mempool, it doesn't appear that many transactions would be affected by this new rule and of course it will possibly enable new use cases that weren't possible before.
And so with that, our solution is really partition the mempool into these clusters of at most 64.
We impose a policy rule.
You can't go above that.
If you try to go above, we'll just reject the transaction.
And whenever such a cluster is changed, a new transaction is added to it, some part of it is mined, there's a reorg that conflicts some part out, there's a replacement that conflicts with some part, any change that's made to a cluster, we run effectively the block mining algorithm again, but just on that little cluster of at most 64 transactions.

## How Cluster Mempool Enables Optimal Ordering

Speaker 1: 00:17:04

And because it's so small, this is fast.
And it turns out that really all you need is this ordering within sets of related transactions.
The overall ordering of the mempool is sort of a very simple merge sort of all your clusters.
And this we can do at runtime whenever needed.
But the hard part, the computationally hard part is now restricted to just these groups of 64 transactions.
Whenever a change is made, we just rerun a mining algorithm on it.
It's not a mining algorithm anymore.
It's really just an algorithm for deciding the order of the transactions within it.
Yeah, and of course, once we had that, and we now actually do have that, there's an obvious follow-up question because as I mentioned earlier, the existing logic for deciding transactions at block building time is suboptimal in many ways.
This isn't necessarily a problem, but it's nice if we can do better.
And given that we're only going to be running this algorithm anymore on groups of 64 transactions, we may have the ability to do something far better than what is done today.
As an example, so today you have Child pays for parent, which works.
So you can have a single child that pays for a parent and they will be aggregated and seen as a group, which is what you want.
But what doesn't work is children pays for parent or children pay for parent, grammar.
So if you have two children that both have a higher fee rate than a parent, only the one with the most effects will be considered alone, rather than the combination of the two both bumping the parents together.

Speaker 0: 00:19:19

That's a big problem.

Speaker 1: 00:19:22

I wouldn't say it's a problem because...

Speaker 0: 00:19:24

Well, it's a big blind spot.

Speaker 1: 00:19:25

Yeah, it's just...
I don't think it matters much in practice today because, of course, people aren't relying on use cases that need children pay for parent because it just doesn't work.
But it has been my focus for I guess most of the past two years on and off, done some other things too, but is try to come up with good algorithms for deciding, I have a group of at most 64 transactions, What's the best ordering to mine them in?

## Future-Proofing Bitcoin for New Use Cases

Speaker 0: 00:20:15

And people using Bitcoin.
Bitcoin exists to be an alternative to this institution, but to do that, it needs people to actively maintain it.
If you actually want to hear from developers themselves, how they approach their work and what they choose to work on, go to bitcoinmagazine.com and get yourself a copy of the core issue.
So it's pretty much like you have this whole abstract architecture and new way of ordering things and managing the mempool.
And now it's just, well, now what's the math of how we're going to manage?

Speaker 1: 00:21:18

Yeah it's just a drop-in replacement right when we started this idea of cluster mempool the idea was just to run the existing block mining algorithm on these now groups of 64 transactions ahead of time as opposed to do it on the whole mempool at block building time.
But given that we'll only be running it on groups of 64, maybe we can just do something better or specialize it and in practice we can basically find the optimal ordering always, which is neat.

Speaker 0: 00:21:52

I mean, that's a little more than neat.
I think that's the very good thing long-term for the network to have like an optimal, like most profitable algorithm like that to be open, like anyone has access to it.
Exactly.

Speaker 1: 00:22:06

Because before Optimal, our goal would be to be sufficient to cover all the things that people do on the network practically.
If all that people do is single transaction CPFP bumping, then all you need is an algorithm that can deal well with that.
But what if some use case who knows what crazy, interesting or dumb things people come up with in the future that creates a strong economic incentive to pay for weird things in transactions.
Well, if it's optimal, it's optimal.
There's nothing people can come up with as long as it's restricted to 64 transactions and is still subject to the denial of service protection rules and so on.
But in terms of topologies of related transactions, it doesn't matter what people come up with, we'll always order it the right way.

Speaker 0: 00:23:09

Yeah, so it's essentially future-proof, so that you can continue optimizing it based on new second layers built, new network behaviors or meta protocols or whatever people.

Speaker 1: 00:23:22

You can come up with whatever use case and the algorithm or the behavior of nodes just becomes well if it's better I'll take it if it's not better.
I won't take it And it can discern betterness in any topology of up to 64 transactions.

Speaker 0: 00:23:45

I mean, that sounds like a huge deal, especially for layer twos, and just kind of giving more Predictability or certainty as far as what people are building on top of especially for like reactive layer twos like lightning or arc where you might have to respond to another party's transactions and you need that guarantee you need to know like if I submit this transaction like is this going to out-compete something or replace something.

Speaker 1: 00:24:18

It's true, but I wouldn't say it becomes more predictable because it's predictable in the sense that it's at a very high level, super easy to give you what you need to do.

## Incentives, Miners, and the Long-Term Bitcoin Path

Speaker 1: 00:24:35

You need to make it worth whatever you're doing needs to result in increasing fee income.
And if you can do that, it will take it.
But how that's decided, that's sort of a very high level black box kind of thing where before we had the big 125 rules which were not perfect and deviated from in several ways, but they gave you a list of conditions like, if you satisfy this rule, this rule, this rule, this rule, the replacement will go through.
That's no longer the case.
The rule is, it needs to be better.
Figure it out.
I don't think this is an issue in practice because people really if you're talking about groups of transactions where you or your protocol lightning or whatever layer to have control over all related transactions, there is no issue because you can of course just run the algorithm on it and see if it will be accepted.
As soon as you interact with potentially grieving parties that might try to attach to your group of transactions, like I make an unconfirmed output to a third party, now they can attach arbitrary other things to that and what I might need to do to bump a fee here becomes now dependent on what they're doing.
So It does become, I think, harder to reason about, but it's a far cleaner.
And it actually aligns with the incentive compatibility in the network, where before we had arbitrary rules that weren't actually always the best ones and we shouldn't expect that going forward those rules would be ones that miners keep following.
While this, they hopefully will.

Speaker 0: 00:26:45

I feel like, at least from my perspective, it feels kind of like the latest point in a progression of kind of cleaning up or removing incompatible things in the mempool.
Like the original first scene safe rule, And then when we first implemented RBF it was opt-in, you had to flag it.
But miners were still mining unflagged transactions anyway.
It's kind of been, at least the entire time I've been in this space, people have been slowly cleaning up those things that people just did.

Speaker 1: 00:27:20

Do you remember priority?

Speaker 0: 00:27:22

I don't know how long you had the percentage of the block set aside for zero fee transactions if they were old enough.

Speaker 1: 00:27:29

If they were, yeah, If they had sufficiently high bitcoins, they destroyed per byte, which I guess made sense in very early days because that was a useful prioritization mechanism.
But of course, I mean, that's just not maintainable.

Speaker 0: 00:27:51

Yeah, well, once there was real value and people competing for block space, no rational miner would run that.
Exactly.

Speaker 1: 00:28:00

So yeah, there's been a long sequence of steps in that direction, I think.

Speaker 0: 00:28:07

I mean, it's a necessary thing in the long term.
Like, if we're going to use a system that depends on the incentives of these profit-motivated players, we should be aligned with their incentives or how do you think this is gonna work?

Speaker 1: 00:28:20

Exactly.

Speaker 0: 00:28:21

Well, you know, I think you gave a super stellar breakdown and I think most people watching might actually walk away understanding it.
So I want to thank you all out for that, Peter.

Speaker 1: 00:28:32

Yes, Peter.

Speaker 0: 00:28:34

And I hope you guys all learned something.

Speaker 1: 00:28:37

Bye.
