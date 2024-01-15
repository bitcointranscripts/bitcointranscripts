---
title: "Block Building"
transcript_by: kouloumos via tstbtc v1.0.0 --needs-review
media: https://podcasters.spotify.com/pod/show/chaincode/episodes/Block-Building-with-Clara-and-Murch---Episode-18-e1dmitu
tags: ['research']
speakers: ['Clara Shikhelman', 'Mark Erhardt']
categories: ['podcast']
date: 2022-02-01
---
Speaker 0: 00:00:00

The idea is we want the set of miners to be an open set where anybody can enter and exit as they wish.
And if we now had obvious optimizations that people had to implement to be as competitive as possible, That would make it harder for new miners to enter this place.
Hey, Murch.

Speaker 1: 00:00:32

Hey,

Speaker 2: 00:00:35

Clara.

Speaker 1: 00:00:38

Hi. Welcome to the Chaincode Podcast.
Clara, for you, your first episode.
We're so excited to have you here.

Speaker 2: 00:00:43

I'm also very excited to be here.
And

Speaker 1: 00:00:46

today we're going to talk about block building.
So maybe you could start us off a little bit about, Claire, how did you get to Chaincode?
Like, what are you doing here?
What are you spending your time on?
Tell us a little bit about yourself.

Speaker 2: 00:00:57

Okay.
So my background is in mathematics.
I have a PhD in math.
I was working on graphs and probability.
And during my PhD, also got really interested in this whole Bitcoin space.
And then I decided to pursue it as a postdoc.
So I spent some time at Berkeley and at Caltech, but I felt like I need to be in a place where people are really into Bitcoin.
And here I am.

Speaker 1: 00:01:30

So how does a mathematician get into Bitcoin?
Because we need more of them.

Speaker 2: 00:01:35

So I think that there are a lot of really, really fascinating questions inside the space.
And as a mathematician, I felt like I want better motivations for the questions I'm answering.
And more, I think people in applied math might also think this way.
So I think people just need to know that There are really cool questions here waiting to be solved.

Speaker 1: 00:02:04

And what kind of cool questions are you pursuing?

Speaker 2: 00:02:06

So the block building one that we will discuss later, it's a very clean algorithmical question.
It's very similar to knapsack.
It's very classical kind of optimization, things that people were working on for a while.
So it has a new context and it's nice to look at it from there.
I'm working a lot on the lightning network.
So there's a lot of economy and other things coming in, but at the end it boils down to network or graph theory.
So there's very, very nice questions that have to do with optimization and evolution of random graphs and similar things.

Speaker 1: 00:02:54

It sounds like we're going to have to record another episode.

Speaker 2: 00:02:58

We might.

Speaker 1: 00:02:59

OK, so those are the kinds of problems you're currently working on?

Speaker 2: 00:03:02

Yes.

Speaker 1: 00:03:04

Okay.
So yeah, we'll look forward to getting that on tape at some point soon.
Tell me maybe like this specific problem of block building.
Why were you attracted to this?

Speaker 2: 00:03:12

So It's very clear, I think, to anybody that comes from the algorithmic world that what's happening now, it's a straightforward, greedy algorithm.
And In most cases, this would not be the optimal solution.
So when somebody from math or CS sees a not optimal algorithm happening, it scratches.

Speaker 1: 00:03:46

Got it.
And merge.
So from a Bitcoin perspective, why does this matter?
Why are we spending our time on this?

Speaker 3: 00:03:52

So what you don't want is that there is a huge amount of potential for somebody to do better than everybody else, Because that will mean that they can make more money building blocks than other people and can get an undue amount of reward for the same work.
So what we want Bitcoin Core to do is to out of the box do very well, maybe optimally, but reasonably well, that there is no huge advantage for somebody else to come in and Find a proprietary solution that that blows everything else out of the water.
So One of the reasons to look at block building carefully is to make sure that there is no such hidden potential there.

Speaker 1: 00:04:37

That makes sense.
It's hard to get miners to upgrade but it seems like they probably make their own patches and you know try to get an edge.
So writing their own custom software is, you know.

Speaker 3: 00:04:48

You'd think that they'd be super curious to tickle out the last little bit.
But on the other hand, blocks have been not full.
And at one satoshi per byte, Even if the block is full, that's 10 milli Bitcoin in reward.
Right?

Speaker 1: 00:05:04

Today, but you know, a year ago, people were all, fees were all the rage.

Speaker 3: 00:05:09

Sure.
And in two more years, we'll have another halving.
And in a few more years, it'll get into the range of a full block at min relay fee where it's interesting.
I mean, for 20 years.
So if you already know how blocks are built and where fees and block subsidy come from, That's what we'll cover in the first section.
Sure.
And you might want to skip that, we'll put something into our show.

Speaker 1: 00:05:35

Well, I'm excited to talk about this.
Actually, this one I'm sitting out, so I'm just gonna let you two talk, and then we'll wrap it up.

## Building a valid block 101

Speaker 2: 00:05:47

So, before we talk about building the blocks, we need to understand what are the Lego pieces we're putting into the block, right?

Speaker 0: 00:05:57

So blocks contain transactions.
Blocks are limited in a number of ways.
They have to be valid, and they cannot be bigger than 4 million write units.

Speaker 2: 00:06:09

Now, for example, I do know what are the limits on the block, but what are my options?
Where are the transactions?
What do I know about the transactions?

Speaker 0: 00:06:19

Right.
After somebody submits a transaction to the network, the transaction gets validated by every node that sees it.
And then after validating, they forward it to their peers.
So to see whether a transaction is valid, a full node will look at what pieces of Bitcoin exist, look at their local copy of the UTXO set, and see that the transaction only spends funds that are still available for spending.
And eventually those unconfirmed transactions will land in the mempool of a miner and miners will pick from the mempool a block template of unconfirmed transactions that they're trying to build a valid block from.

Speaker 2: 00:07:04

Cool.
So now we know that we have the mempool, it has this unconfirmed transactions, and then we want to build a valid block.
So a valid block is of limited size, and we also have some rules into which transactions can go into the block.

Speaker 0: 00:07:25

Right, so you cannot include invalid transactions.
Well, you can, but it makes an invalid block.
And transactions have to be in the correct order, right?
You cannot spend funds that don't exist yet.
So if you, for example, have a transaction that spends funds from another unconfirmed transaction, the parent transaction has to go first to create the outputs that the second transaction then uses in its input.

Speaker 2: 00:07:51

Are there other ways that the transaction can be invalid?
Well signatures obviously.

Speaker 0: 00:07:58

Right, so it could be just generally malformed.
It could spend funds that don't exist, as in like just some made-up pieces of Bitcoin.
You could have the problem that there's two transactions that spend the same funds, which basically falls under the same rule.
The first transaction consumes the existing unspent transaction output, and then the second one doesn't have the ability to spend them again.
You could have an invalid script or invalid signature, or you could have a transaction that spends the same funds twice in the transaction itself.
So if you naively just check that a transaction only spends one set of inputs and no other transaction does, you might miss that you spent the same funds twice.
So I don't know the whole set of rules by heart, but there's a bunch of them.

Speaker 2: 00:08:49

So, in this space of block building, I think we'll mostly focus on the limit on the block size and only spending available UTXOs or existing UTXOs.

Speaker 0: 00:09:04

Maybe one more comment.
There's a special transaction that has to be in every block, which is the coinbase transaction or the generating transaction.
It's the one that goes first in the block and that can collect a transaction fee and create new bitcoins.
And after that, a miner may include zero to a full block of transactions, and they can pick any transactions they want, as long as they follow these rules that They're not spending any funds that don't exist yet and so forth.
It's completely up to the miner to pick what they want to include, but generally is the goal of the miner to collect as much money as possible.
So we expect miners to build the most profitable block.

Speaker 2: 00:09:46

So how would they do that?

Speaker 0: 00:09:48

Well, currently we assume that most miners are using Bitcoin Core and Bitcoin Core has a function called get block template.
Get block template will look at the full nodes mempool, the queue of unconfirmed transactions.
And for each transaction in the mempool, it has stored the size and fees of all of its ancestors plus itself.

Speaker 2: 00:10:14

What do you mean by ancestors?

Speaker 0: 00:10:17

Right.
So we had previously mentioned, if there are transactions that depend on each other by one transaction first creating a transaction output that another transaction in the queue is spending they have to go in that order, right?
Because the output has to exist before it can be an input for another transaction.
So any transactions that topologically precedes another transaction, we call an ancestor.

Speaker 2: 00:10:44

Okay, so For each transaction, we're looking at all of the other transactions we will need to include in the block beforehand for the block to be valid.
We sum up the weights of all of these transactions, we sum up the fees of all of these transactions, and from this we discover how many satoshis per bit we will get from this whole...

Speaker 3: 00:11:07

Per byte.

Speaker 0: 00:11:08

Per byte.
Or better yet, per Vbyte.
Because Segwit's been active.

Speaker 2: 00:11:14

Yay Segwit!

Speaker 0: 00:11:16

Right.
Note that this ancestor set fee rate for the transaction does include all the ancestors and the transaction itself.
The observation here is that the transaction with the highest ancestor set fee rate, including that and all of its ancestors will be the most profitable next step in building a block template.

## The current getblocktemplate algorithm

Speaker 2: 00:11:38

Given these rules for blocks, there is a current algorithm that gives us a block template, right?
How does it work?

Speaker 0: 00:11:49

Yes, so the call get block template, it uses the mempool, which is already a list of all the unconfirmed transactions with its ancestor set information.
And then it just looks at which ancestor set will give me the most fees per VBYTE and includes that first.
And then it updates all the other transactions that are impacted by this ancestor set getting confirmed, recalculating their ancestor set information, and then pops the next one from the top.
It does that until nothing fits into the block anymore, block template is done.

Speaker 2: 00:12:26

Or until the mempool is empty.

Speaker 0: 00:12:28

Yes.
Okay.

Speaker 2: 00:12:30

So in general this is a greedy algorithm.
At every step, we look at a transaction, what would we need to put in to have this transaction in the block, what are the dependencies, we choose the optimal one, looking at its ancestors, put it into the block, and then continue with this question.
So, are we happy with being this greedy?

Speaker 0: 00:12:58

So, this works pretty well, actually.
It's also very fast with having pre-calculated all the ancestor sets for the unconfirmed transactions in the mempool already.
It has two small things, or maybe not quite so small things, where it does not necessarily find the optimal solution.
So A, it's a greedy algorithm and it does not find the optimal block in the sense that it doesn't necessarily fill the last few vbytes in the block.
If it just has collected some stuff already and nothing else fits anymore, it won't go back and shuffle the tail end a little more to get the last few satoshis.

## Child pays for parent

Speaker 2: 00:13:37

Given the current algorithm, it also motivates some wallet behavior.

Speaker 0: 00:13:45

As many of our listeners are probably familiar with, there exists a concept called child pays for parent.
And this leverages the dependency between a parent transaction and a child transaction that a child paying a high fee rate can only get included once its parent is included, because it spends an output that the parent creates and as we have said before already, you cannot include the child unless all of its inputs exist.
So when you have multiple of these situations in parallel, where say one parent has three child transactions that all pay more fees than the parent, you would have three separate ancestor sets that each compete to be the best ancestor set to be included in the block.
And you can get now situations where the three children taken together with the parent would have a greater fee rate than what is currently being included in the block, but we would not notice because we evaluate them separately.
We noticed that if we could search in the mempool data for constructions where this is the case, we actually can find sometimes constellations in which we change what block template would be built and make blocks more profitable for miners by including these sets of transactions together first.

Speaker 2: 00:15:12

The current algorithm just looks at child, parent, parent's parent, and so on and so forth.
So in some sense it's very one-dimensional, right?
Just one above the other above the other.

Speaker 0: 00:15:28

Well, you can have multiple parents.
So it's a DAG or a Directed Acyclic Graph.
Yes, it's fairly one-dimensional because you basically just look at a transaction with all of its ancestors.

Speaker 2: 00:15:41

So in the current algorithm, we're just looking at a transaction and all of its ancestors.

## Is there something better?

Speaker 2: 00:15:47

In what we are suggesting to do, we want to do something slightly more complicated where we look at sets of transactions and all of their ancestors, right?
Because we can't put transactions without all of their ancestor set, but our starting point would not be a single transaction, but we could have many transactions.

Speaker 0: 00:16:14

Essentially, you can think of what we're searching for as an overlap of multiple ancestor sets, right?
So if you have a single child that pays for its parent, you would want to combine it with the ancestor set of another child of the same parent.
So they need to have some overlap in their ancestry, they need to be connected in the graph in some way, but the overall situation is such that through the shared ancestry their set fee rate for the whole set of transactions is higher than for any of the individual ancestor sets.

Speaker 2: 00:16:49

That sounds great, but as we know, one of the main things that we want from a block building algorithm is for it to run quickly.

Speaker 0: 00:17:01

Yes, so especially in the moment after a new block is found, we want miners to be able to switch over to building the succeeding block as quickly as possible.
And miners often build an empty block template intermittently because they don't know for sure which transactions they can include until they have evaluated the parent block.
But we want them to be able to switch over as quickly as possible to a full block at the next height.

Speaker 2: 00:17:29

So let's talk implementation a bit.

Speaker 0: 00:17:32

As you might imagine, if you have all the ancestor sets for every transaction, you have a very clean list of things that you need to look at.
For every single transaction, you just look at all of its ancestors.
That's O of N in the size of transactions.
To find what we call candidate sets, these overlaps of multiple ancestor sets that could be even more profitable to include, we need to essentially search the power set of graphs of transactions that are connected.
So what we do here is we look at one transaction that has a high fee rate and then we cluster all of the transactions that are connected to it either via child or parent relationships.
I'll be referring to this construct, the maximal set of connected transactions as a cluster.
And then in this cluster, we want to find the best subset, best as in the highest set fee rate.
Obviously, we can only include sets of transactions for which all the ancestors are included.
So we're looking at some overlap of ancestor sets and we call this a candidate set.

Speaker 2: 00:18:44

So this candidate sets could be ancestor sets as we've seen in the current algorithm, but because we're allowed to traverse up and down from child to parent to parent back to child, we get a more complicated structure.
But to keep the block valid, we need to make sure that at the end, whatever we're trying to put into the block has all of the ancestry.

Speaker 0: 00:19:11

Exactly.
Right.
So, as you might imagine, This is no longer searchable just in the order of the size of transactions, because now we have to essentially search through the power set of all the transactions in every cluster.
That explodes very hard in the complexity, and that gets us in trouble with, we want us to run really, really fast.
Our idea is we would continue to quickly build a fairly good block using the ancestor set based block building that we have already.
And then we would perhaps in the background have a second process that searches for a more profitable block using these candidate sets that we have been discussing.

Speaker 2: 00:19:57

But of course we don't actually need to look at the power set of all the transactions.
So the first thing we need to remember that a lot of subsets of transactions are just not allowed into the block.
So we definitely want to focus our search on subsets that are valid.
Even when we focus ourselves only on valid subsets, we can also do things a little bit in a smarter way.

Speaker 0: 00:20:29

Right, yeah, There's a few nifty little tricks that we found while we have been writing our research code for this.
We start our search in the cluster by a number of initial candidate sets, and since we have them already, we just initialize with the ancestor sets that exist in the cluster, which is for every single transaction in the cluster, we have already a starting set.
The next observation we had was when we have an ancestor set in a cluster that has fee rate x, any leave in the cluster, as in any childless transaction in the cluster, that has a lower fee rate than that, can never lead to a better candidate set than this.
So, if you have a transaction A that pays 5 satoshi per byte, that has a child which pays 4, you will never get a better candidate set by including this child with 4 when you already have something that pays 5 satoshi per byte.

Speaker 2: 00:21:30

I think an important point to make is that when we're thinking about fee, we're talking about effective fee rate.
So we're not interested in fee that this transaction would give us.
I again remind our listeners that we're talking about fee per vbyte?

Speaker 0: 00:21:48

Yes, I might accidentally say fee, I always mean fee rate, and always specifically the fee rate of a set of transactions that if we include them together would be the highest across all the unconfirmed transactions still in our mempool.
So we have two optimizations so far.
One is, obviously we don't have to search the whole power set of transactions in the cluster.
We can limit ourselves to only searching the valid subsets.
And we can do that by starting with the ancestor sets in the cluster, and then expanding from the ancestor sets by adding additional ancestor sets to that.
So specifically, if we have a set of transactions, maybe just a single transaction that doesn't have any unconfirmed parents, we would add the ancestor sets of each of its children to create new candidate sets to add to our search list.
And we basically just go through our search list greedily.
We first evaluate the candidate sets with the highest fee rates, expand from those again.
But since we start with all the ancestor sets in the cluster already, we can very quickly use the leaf pruning that I mentioned to cut down on transactions that we never have to look at.
So every time we find a better candidate set in the cluster by expanding it, for example, by including a second child for a parent and getting a higher set fee rate, we actually reduce the search space at the same time.
So very quickly on this cluster we'll find one single best candidate set and have evaluated all possible combinations, either by dismissing them or by having actually evaluated them.
And then we just remember this as the best possible candidate set in a cluster of transactions.
Now, if we look at a mempool, a mempool can have up to 300 megabytes of transactions, and we don't really want to traverse all of that immediately.
Really we only want to look at the relevant transactions.
So what we do is we sort all the single individual transactions by their fee rates, and we only start clustering even on the transactions that have the highest fee rates.
So we basically move down from an infinite fee rate and pick the single transaction with the highest fee rate, search for its cluster, look what the best candidate set in that cluster is, check out what the set fee rate for that candidate set is, and then we resort the whole cluster into our list of data that we need to look at, at the fee rate of the best candidate set in that cluster.
Then we use for example a heap for that and we bubble up the next transaction or cluster by highest fee rate.
And if a transaction bubbles up, we cluster it and sort it into the heap as the cluster.
If a cluster bubbles up, we pick its best candidate set because now we know across all of the mempool, this is the set of transactions that has the highest possible fee rate, and we can just include it in our block.
When we include a candidate set into our block, we naturally need to remove it from the cluster, and we have to update all the transactions in the cluster to forget these as unconfirmed ancestors, and therefore like have new ancestors set fee rate, ancestor size, ancestor fee, and we put them back into our list of single transactions.
And we only look at them again if any of those single transactions bubble to the top by fee rate before we fill the block.
And that's a few of our optimizations so far, I guess.

Speaker 2: 00:25:45

Yeah, and I guess that if we would have other pre-calculations, we could have made things quicker.
Because we're starting now only with the Ancestry sets for each transaction, but we could have pre-calculated such clusters or something like that.

Speaker 0: 00:26:05

Well, the downside of pre-calculating all the clusters is that we would have to cluster all the 300 megabytes of mempool potentially, when in the end we actually want to only include about one megabyte.

Speaker 2: 00:26:18

Right, but we get to do it to some extent in our off time.
We don't do this when we build the block and we're in a hurry.

Speaker 0: 00:26:26

Oh absolutely, we should be pre-calculating the whole block Actually, not just cluster information.
The cluster information is somewhat ephemeral anyway.
As soon as you pop the best candidate set out of the cluster, you have to recluster and research for the best candidate set, right?
So Just pre-calculating the clusters is sure a little benefit, but actually just pre-calculating the whole block template in the background on a loop, say every time we add new transactions or every minute or so, and then having something at the ready when the user calls getBlockTemplate would be maybe interesting.
Of course the problem is when a new block gets found and when we want to have a new block template quickly, it might be slow to do all the candidate set search on every cluster and all that.

## How easy would it be to guess the next block?

Speaker 0: 00:27:20

So we should, when it's supposed to be as quick as possible, we should use the ancestor set based approach and respond with that first.

Speaker 2: 00:27:31

I wonder how easy it is for us to guess what's the next block we're going to see.
So to calculate both the block we want to mine now and the block we will want to mine once we'll hear about the block.
Because if everybody's using the same algorithm, I know what's going to be in the block I'll see pretty much.
So I have a good guess at least.

Speaker 0: 00:27:55

You have a very good guess, but I think especially for transactions that were just broadcast on the network, you don't have a good guess whether the miner has it already included in the block template.
Even if the mining pool operator has seen it already, they give out templates to all the mining machines only whenever the mining machine has exhausted the template they're working on.
So even for like 10-20 seconds after the pool operator has built a new block template, the machine will maybe still work on traversing the extra non-space for that block, for the previous block template.

Speaker 3: 00:28:35

So there is a little

Speaker 0: 00:28:36

bit of a latency between a new block template being created and that actually being what mining machines work on, so you could be missing some transactions and that would not be a huge problem.
You would just not have them in your look ahead block template.
But you might also have some transactions that are precious to the miner, because say they also have a wallet business on the side and they prioritize the transactions of their customers or they have an accelerator service and include some transactions that are actually not in the very top of the mempool but maybe would be in the lookahead block.
So even if you have the lookahead block, you can't really use it until you've evaluated that it has no conflicts with the previously found block.

## Do we have a better idea than initially mining an empty block?

Speaker 2: 00:29:27

Do we have a better solution than mining on an empty block in the beginning?
Should we guess a block and take the risk that it won't be actually valid or should we go for an empty block?

Speaker 0: 00:29:42

I guess at this point the transaction fees make such a small part of the total block reward.
And the total block reward of course consists of two parts.
There's the block subsidy, which is the newly minted coins, and there are the transaction fees from the transactions included in the block.
And we had a period of six and a half months earlier this year where we did not have an empty mempool.
There was always a queue of transactions trying to get confirmed.
But since mid-June roughly, we've had ample block space, mostly because there was a huge shift to more efficient output types getting used, and the hash rate reduction that happened after China banned mining was quickly regenerating, so we had faster blocks for some time, and faster blocks means more block space, of course.
So those two things together, I think, led to us essentially having abundant block space all the time, which meant that the fee rates have been very low for the past five months.
And whereas in the first half of the year, the reward was about one-sixth transaction fee, in the past half year it's been more like maybe less than 5%, 2 or 3%.
The risk of having an invalid block and losing the newly minted coins is probably going to outweigh the reward of including transactions in the block.

Speaker 2: 00:31:14

But we can expect sometime in the future a sharp threshold moment or just a threshold moment as the block reward is having after, give or take, four years.

Speaker 0: 00:31:29

One thing that miners could do is that they keep a stash of their own transactions that they don't broadcast to the whole network and only use for their own block templates and the moment that a new block is found they include those.
The problem is if they always include them in their block templates, they would leak because people see what block template they're building.
So I haven't thought this through enough to make sure that it's a viable idea, but I think that empty block mining will remain a thing.
What we want to do is to make block validation as quickly as possible, and then to make block building as quick as possible so that there's as little delay as possible between a miner hearing about a new block and starting to mine a new full block.

Speaker 2: 00:32:18

I do find the concept of a miner having secret transactions, so to say, that they keep on the side.
Where did they hear about these transactions at all?

Speaker 0: 00:32:30

Oh, I mean, for example, they could have payouts to their pool contributors or there is one mining pool that was closely associated with a wallet service for a while.
You could just beat those.
But on the other hand, That seems a little far-fetched because if you have a wallet service, people want to transact.
They don't want to wait for that transaction to go through.

Speaker 2: 00:32:54

So actually as a mining pool, if I want to pay the miners, It does make sense to, instead of mining on an empty block, mining on my rewards if I'm paying out of previous block rewards, because I know there's not going to be a conflict.
These are fresh coin, just minted.
Nobody could have touched them besides me.
Do we see this behavior?

Speaker 0: 00:33:19

I don't think we see that very much.
I'm also kind of expecting that given there's very frequent payments of small amounts to people, I would expect that mining pools would eventually adopt lightning as a withdrawal means to their pool contributors.
I've taken a lot of time to say that.
I expect empty blocks to remain nothing.

Speaker 2: 00:33:44

Cool.

## Empty blocks and SegWit

Speaker 2: 00:33:45

How often do we see empty blocks?

Speaker 0: 00:33:47

Not that often anymore.
We actually saw a fairly sharp decline in empty blocks when SegWit happened, because SegWit required miners to update their software.
And for a long time, miners had been running older software, and all the efficiency improvements in the peer-to-peer layer and block building and stuff like that suddenly came to pass in the software upgrade.
And we saw two things.
We saw especially that there was a lot fewer mini blockchain forks where there was latency and or validation was slower and two mining pools found blocks at the same height And that was especially because the compact block relay happened between whatever they were running and SegWit.
And then I think also a little bit faster block validation and build.

Speaker 2: 00:34:45

So this is what we have on our plate now, but we're already talked a bit about what might happen in the future, but We also have a few thoughts about What else can we do to make block building even better?

## How to improve on the candidate set algorithm e.g., linear programming

Speaker 2: 00:35:02

So there is linear programming solutions that solve, to some extent at least, the other problem we've talked about with blocks.

Speaker 0: 00:35:18

The optimal use of all the available block space.

Speaker 2: 00:35:21

Right, because sometimes when you're doing greedy things, you, so a very crude example would be, I can fit two kilos into my knapsack.
And thanks for everybody who giggled because they know what's the knapsack problem.
So you can put two kilos in your knapsack and you want to put as many items as you want.
You have one item who weights a kilo and a half and two items that weight one kilo.
So if you're greedy, you take the kilo and a half item and can't fit anything else.
If you're not as greedy, you look at it and say, okay, I can take the two items that weight one kilo each.
So this is a problem that our current algorithm does not solve, but by using linear programming techniques could be solved.
Downside of this techniques that they have a tendency to be slow, although it's unclear that they have to be, and this is something we definitely would like to look into.

Speaker 0: 00:36:42

So basically by running linear programming we would be able to find out how close to the optimal solution we can get with just a candidate set-based approach.

Speaker 2: 00:36:55

Any other thoughts on the future?

## Why should Bitcoin Core have better block building?

Speaker 0: 00:36:58

Maybe we should touch on why it's important that Bitcoin Core has really good block building.
The idea is we want the set of miners to be an open set where anybody can enter and exit as they wish, especially the entering is interesting obviously, and if we now had obvious optimizations that people had to implement to be as competitive as possible, that would make it harder for new miners to enter this place.

Speaker 2: 00:37:32

So I would like to comment that even if now the mining fees from transactions are not a crucial part, in the future they either will become something important or mining won't make sense.
As the block subsidy is going down, the fees become more and more important.
And so in the future, this would carry a lot more weight.

Speaker 0: 00:38:01

Yeah, definitely.
Even if we're thinking right now, this week we just crossed 90% of all bitcoins being in circulation.
In 2036 it'll be 99%.
In, I think, 2046 it'll be, or 2050, it'll be 99.9. And as the block subsidy keeps halving, even just a regular full block at minimum fee rate will eventually have more fees than new coins.
I think that's reached by 2060 with one Satoshi per VBITE and four million white units.

Speaker 2: 00:38:38

I think this is already something Satoshi mentioned in the white paper.

Speaker 0: 00:38:44

I mean that's a far, far future but we're trying to build a system that lasts for multiple decades.
So we have to think about the long-term incentives.

## How to compare different block building techniques

Speaker 0: 00:38:55

So Clara, tell me, we had an idea how we should be measuring whether our candidate set-based approach makes sense and is a good improvement.
Can you tell us a little more about that?

Speaker 2: 00:39:09

So there are a few ways we can compare different block building techniques, one of which is just looking at a certain mempool and then saying which block building algorithm will do better, which is a valid point of view, which we're exploring.
But another very interesting thing to look at is what happens if, say, 2% of the miners use our new algorithm while the rest are using the old one.
And for this we want to use a simulation, of course, that does the following.
So we have snapshots of the mempool.
And then at any moment we know that a block is built.
We're going to flip a coin that tells us are we going to use the old algorithm or the new algorithm.
And then a block, we build a block, we update the mempool, there's new transactions coming in, again find a block, flip a coin, and decide.
Some of the listeners might be familiar with Monte Carlo and things like that, so if this is where your mind went, you are absolutely correct.
And by doing this, we can compare how much can a miner gain when they move to the new algorithm, especially in an environment where the old algorithm is still running.
This might also affect the changes, how quickly will the algorithm be taken by the other miners, because If you can already do much better by being the only one that does it, that's a very nice incentive.

Speaker 0: 00:41:06

Right, and then there's also the aspect, it's hard to say how it will affect how wallets build transactions when there's new behavior in how blocks are being built.
So when we actively search for situations in which multiple children or descendants bump an ancestor together, this might lead, for example, to people crowdsourcing a withdrawal from an exchange with 200 outputs to get it confirmed a little quicker.
We wouldn't be discovering that right now at all with ancestor set-based block building, but we would discover that with candidate set-based block building, and then maybe if there's a few, two, three, four percent of the miners already using that, people might start to say, all right, I'll chip in and try to spend it already and together we'll get withdrawal confirmed more quickly.
And that would be the incentive for miners to switch over and start using the new block building algorithm for mining.

Speaker 2: 00:42:08

We already see this sort of crowdsourcing behavior in the mempool.
So

Speaker 0: 00:42:15

We found a few interesting clusters when we were analyzing mempool snapshots.
We have this data set where we have when a new block came in, the node took a snapshot of what was currently in their mempool and we can then compare what we see in the block and what was available for block building and that's what we use to build our alternative blockchains in this Monte Carlo approach and We found some curious clusters already with over 800 transactions where there's a lot of children spending from the same parent and stuff like that.
So there is some of that going on already, but currently of course mining doesn't exploit that so people aren't doing it on purpose.
It's just people that are, I don't know, withdrawing from a broker and the broker has such a volume that they pay out to a hundred people at the same time and five of them are immediately try to spend it at the same time but they're competing with each other because it's getting evaluated as five separate child pays for parent attempts whereas we would be evaluating it as a single descendants pay for ancestor constellation.
So we do the Monte Carlo approach, we run that alternative blockchain that we're building a few times with say 2% of t miners using our new algorithm already.
What do we do then?

Speaker 2: 00:43:37

And then we compare how better did the miners that use the new algorithm did comparing to the ones that use the old algorithm.
So that's another viewpoint for comparing these two algorithms.
So we already have some data available, there's more coming up.

Speaker 0: 00:44:01

Yeah, we published a thing about basically comparing one algorithm with another algorithm at a specific height for every block.
Now we're doing the let's build a whole blockchain instead because that's more fair because we won't reuse the same transactions again.
Say there's a constellation for a candidate site that should get preferred, we would be including it maybe for multiple blocks in a row if we don't build in a whole alternative blockchain.

Speaker 1: 00:44:33

Maybe just sort of to wrap things up, I have two questions of listening to that episode.
The first one is, if you can get more fees into this current block, doesn't that just pull fees from a future block?

Speaker 2: 00:44:45

Well, if there aren't a lot of transactions in the mining pool, that is the whole current mining pool can fit inside of a block, you don't need any sophisticated algorithm.
You just need the block to be verifiable and have the transactions in the correct order, and you send it off.
It doesn't matter what you're doing.
Our algorithm becomes important only when you want, only when there is actual competition for block space.
And in that case, you're assuming there are more and more transactions coming in.
So yes, you're taking the transactions now, but there's going to be more transactions later on for the next block.

Speaker 3: 00:45:27

So it's kind of fun how it works out.
We want people to build the best possible blocks and we want for example to have these constellations of multiple children to bump a parent together and it turns out that if a minor does find these constellations they also make more money.
So if there's only one miner out of 20 that adopts this, they'll make more money than the other 19, and other miners will also adopt this new algorithm.

Speaker 0: 00:45:58

That's a

Speaker 1: 00:45:58

nice incentive.
And then my other question is, obviously, mining is a cutthroat game.
And so when you're talking about the speed of serving these block templates and these optimized blocks, where's the edge of speed versus the optimization of the fees?

Speaker 2: 00:46:18

So in some cases, you'll find miners even mining empty blocks in the beginning.
So you can think about it as a stepped process.
You start with an empty block, then you use the quickest algorithm that gives you a good enough block.
And then after a while, if you haven't found a block, you look for a better block.
And you can think about other algorithms even better than what we're proposing now that are even slower using linear programming or something like that, that would also be like the third block template that you serve if you find that you have enough time.

Speaker 3: 00:46:57

What happens when you run a mining pool is that you don't create one black template and then your miners are working on that for the whole duration until the block is found.
You keep updating that as more transactions come in.
So you're constantly re-computing the block template anyway.
If some of those happen to just have a little more fees a little later after you switch to a new height.
I don't think sure it might not be mined on in the first half minute or so but generally if it's transparent it'll just snap into place.

Speaker 1: 00:47:32

Makes sense.
So this sounds better in every way.
When do we see it in the wild?

Speaker 3: 00:47:39

Well, careful asking around a little bit what might need to happen for such an algorithm to get integrated into Bitcoin Core seems to indicate that there might be either a need to make it run separate and The architectural challenge of that would be easy, or if you want to integrate it properly into the mempool.
Mempool is such a central part of how everything fits together in Bitcoin Core, that would be a pretty invasive change.
So I'm a little bearish on the timeline okay

Speaker 1: 00:48:22

all right very good well thank you both for your time enjoy the conversation and we'll look forward to getting Claire on soon again thanks

Speaker 3: 00:48:30

Thanks.
Thanks.

Speaker 2: 00:48:45

You
