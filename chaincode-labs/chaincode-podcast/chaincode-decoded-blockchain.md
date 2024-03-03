---
title: "Chaincode Decoded: Blockchain"
transcript_by: kouloumos via tstbtc v1.0.0 --needs-review
media: https://podcasters.spotify.com/pod/show/chaincode/episodes/Chaincode-Decoded-Blockchain---Episode-14-e11n7tl
tags: ['mining']
speakers: ['Mark Erhardt']
categories: ['podcast']
summary: "In this Chaincode Decoded segment we talk about the fundamental role of Bitcoin's blockchain and some of its peculiarities."
episode: 14
date: 2021-05-27
additional_resources:
-   title: Episode 1 with Pieter Wuille
    url: https://podcast.chaincode.com/2020/01/27/pieter-wuille-1.html
-   title: 'Episode 5: The UTXO set'
    url: https://podcast.chaincode.com/2020/02/26/utxos-5.html
-   title: 'Majority is not Enough: Bitcoin Mining is Vulnerable'
    url: https://www.cs.cornell.edu/~ie53/publications/btcProcFC.pdf
-   title: Entropy sources in the block header
    url: https://bitcoin.stackexchange.com/a/96442/5406
-   title: Eschaton block
    url: https://twitter.com/orionwl/status/969903330523865088
---
Speaker 0: 00:00:00

However long it has been since the last block is being found, the next block is expected to take 10 minutes.
So if you have been waiting for 10 minutes or hashing for 10 minutes already, next block is still in about 10 minutes.
Even if it's been an hour, It's going to take 10 minutes until the next platform.

Speaker 1: 00:00:28

Welcome to the Chaincode Podcast.
I'm here with Murch.
Hi there.
Today, we are going to talk about blockchain fundamentals.
Let's get to it.

## Purpose of the blockchain

Speaker 1: 00:00:40

Let's start from the very beginning.
Why do we need a blockchain?

Speaker 0: 00:00:46

So basically, we have a distributed system, right?
Everybody is in different places.
They have latency in between.
We don't have a central coordinator.
And we still need to find a way to get together and agree on a single ground truth.
Basically what we are doing is we hold a distributed lottery to elect a single author to write the next block.
And we use their perspective of what the next block should be.
And By picking just a single author, we now can decide the order of transactions, how they appeared on the network, and have a quasi-central construct that is created distributedly to synchronize with.
And by ensuring that everybody gets a blockchain eventually, we get guaranteed propagation of transactions to every participant.
Through the proof of work scheme, we make the history immutable because every block builds on the previous ones.
And we additionally have a way to distribute the money supply.
All of that in a distributed way without having someone decide.

## Mining is a lottery, not a race

Speaker 1: 00:01:56

And so you use the word lottery and not something like race.
Why isn't it just a race?

Speaker 0: 00:02:02

People often describe the work that Bitcoin miners do as solving complicated computation or something like that, but that's not really a good way of describing it.
Essentially, miners use their hardware to participate in a lottery.
Every time they try to, with a block template, hashes to a valid block, they buy a ticket for the lottery.
And there's a very small chance that a ticket wins.
And when the ticket wins, they have found a new valid block.
They send it to the network and update everybody to the new state of the network.
And the lottery starts over.
Sure, there's complicated math involved in hashing, but it's not complex work that they're doing.
They're not solving a riddle.
They're buying tickets in a lottery.
Right.
So having a lot of hash power doesn't give you the advantage in that you can add it up to be able to go faster than someone else to find this complex problem.
It just gives you more lottery tickets.
There's often this misconception that there's a stack of work to power through, but that's not the case.
Every single attempt at taking a block template and hashing it to check whether the hash is low enough to constitute a valid block is completely independent.
So there is no progress here.
If you've done 10 hashes already, you're no way ahead from somebody that's just doing their first hash.
Basically, this is what makes it a lottery more and why not the fastest miner always wins.
Every single attempt has the same likelihood of winning and you don't know whether any of the tickets are more likely to win until you try them.

Speaker 1: 00:03:48

When you say fastest, you mean more hashes per second compared to another minor, like more other hardware that isn't computing as quickly?

Speaker 0: 00:03:56

Yeah, exactly.
Optimally, if you ignored latency and all that, basically this would lead to people having the relative chance of winning the next block as the ratio of hash rate they have of the global hash rate.
So that's the optimum.
So it's a little less exact that because there is latency and it takes a moment for people to validate the new block when it gets propagated and things like that.
But it's pretty good.
And given the long window, the long target block interval of, well, 10 minutes targeted, the latency is actually a very small portion of the overall window in which a new block is being tried to find.
And interestingly enough, since there is no progress and all of these events are independent, however long it has been since the last block is being found, the next block is expected to take 10 minutes.
So if you have been waiting for 10 minutes or hashing for 10 minutes already, next block is still in about 10 minutes.
Even if it's been an hour, it's going to take 10 minutes until the next block comes.

Speaker 1: 00:05:04

Right, so that does lend itself to the lottery analogy more than the race analogy.
And you're not getting to a certain point.

## Why doesn't the same miner always win?

Speaker 1: 00:05:12

Why doesn't the same miner with, or the same pool, in fact, with the most hash rate just win every time.

Speaker 0: 00:05:19

Right.
So the important points here are everybody works on a unique set of inputs due to having different addresses that they're trying to pay the block reward to.
And there's no progress in mining.
So every single block template being hashed, every single hash attempt is an independent random event with a minuscule chance of succeeding.
So if you do a random event generator again and again, eventually you will win.
But you might win after 10 tries while somebody else has done 5 million tries already.

Speaker 1: 00:05:55

So that's just how lotteries work.
Cool.
So there's this lottery And the lottery pretty much entitles the pool to not only pay themselves through the reward, but also print the block, which then is distributed to the network.

## What happens if two blocks are found at the same height?

Speaker 1: 00:06:12

So what happens if there are two blocks found at the same height and they're competing, what happens to the transactions in those blocks?

Speaker 0: 00:06:20

Since there's latency in the system and then a little delay for checking the block, occasionally another miner will find a block at the same time,
or two miners will, And it happens about every two or three weeks.
So in that case, each of these miners will have included whatever transactions they thought should be in the next block.
That's usually just the transactions that pay the highest fee rate, they optimize for the biggest fee they can collect in a block.
And these two competing blocks have a very large overlap.
I think we've had this question a ton of times on Stack Exchange where somebody asks, So what happens if a transaction is in one block and then it doesn't become part of the longest chain, but a stale chain tip?
Well, from the perspective of the competing blocks, the other block doesn't exist.
It's not part of the best chain.
It's irrelevant, right?
So they can both have the same transactions in the same block, and any transactions that were not included, they're still in the mempool of the node that accepted the other computing block.
Eventually, one of the two blocks will sire another successor block, and every node will say, oh, well, that's the best chain because it has the most work.
Reorganize back to that chain tip and all the transactions that were previously confirmed in the competing block, either they're already included in the two competing blocks now in the new best chain, or they're still in the mempool.
So the miners can just pick them in a future block.

Speaker 1: 00:07:59

Are they reintroduced to the mempool?
Because you would imagine if there's that reorg.
So say there's two blocks, 1A and 1B.
And 2A comes from 1A.
The miners that were originally looking at 1B, the transaction's included in that, and it no longer becomes a stale block.

Speaker 0: 00:08:18

Right.
A temporarily embarrassed best chain.

Speaker 1: 00:08:22

Okay.
And so the transaction that was in that block is then reintroduced to the mempool.

Speaker 0: 00:08:30

Yes.
Okay.
So basically, operationally, what a bitcoin node does is it actually rolls back to the last shared block between those.
And then it using the reverts that are stored for every block, and then it builds the new blocks from that previous shared ancestor.
I think it does all of this in memory.
It doesn't really write back everything to the UTXO set and then take it right out again, because there's such a large overlap usually between two competing blocks.
It just does it in memory.
But basically that's exactly what it does.
It goes back, puts everything back in the mine pool, then applies the two new blocks.

## The longest reorgs

Speaker 1: 00:09:11

And so there's this assumption that these reorgs are never particularly deep.
In what circumstances have we seen some big reorgs?
Maybe, yeah, what are the longest ones that we've seen in the wild?

Speaker 0: 00:09:23

Let's distinguish between natural reorgs and other events that caused a large reorg.
The longest natural reorgs we've seen were four blocks deep.
And those last happened in 2012.
So some time has passed.

Speaker 1: 00:09:39

Four doesn't seem that much either.

Speaker 0: 00:09:41

Yeah.
Well, it's pretty weird, right?
It means that two miners each found four blocks in a row without like hearing about the other chain or without accepting the other chain as the best tip up to that point.
I assume that that was a series of very quick blocks each.
Otherwise, I would just be insane.
Like a 10 minute block in between and the other miner hasn't heard about it.
Since then, the latency on the network has dropped a lot.
We have header first synchronization, which also means that you don't have to send a whole megabyte of block, but just 80 bytes to announce the new header.
On the one hand, it's not that long, but on the other hand, it still sounds pretty insane.

Speaker 1: 00:10:27

Yeah.
And then you said there were some maybe unnatural reworks that had happened in the past.
What are some of those?

Speaker 0: 00:10:34

So we had a value overflow bug in August 2010, where somebody created 184 billion bitcoins.
And obviously that got reorged out.
I think that actually took a patch and the patch had to get distributed.
But then 2010 was really denacent.

Speaker 1: 00:10:55

Right in the beginning, yeah.

Speaker 0: 00:10:57

And another one that we saw was, Was it the 0.8 upgrade for Bitcoin where there was a mismatch in the behavior of the level DB and Berkeley DB when that was switched?

Speaker 1: 00:11:10

It was the number of locks.
Yeah.
So Peter goes over that in his episode And it was a quirk.
Basically it was a hard fork.

Speaker 0: 00:11:20

It was a hard fork that happened to get triggered by a block actually exhibiting the behavior that was different.
I think it was more than 30 blocks that got re-arced out.

Speaker 1: 00:11:30

Yeah, that had to be a coordinated effort to pretty much stop the chain and restart.
There's some debate as to whether that's a hard fork, but it was definitely something.

Speaker 0: 00:11:42

It was basically a smaller set of possible valid blocks that got extended to a bigger set.
So, whatever.
We can go into soft forks versus hard forks some other day.
So there were a few instances of like three block reorgs and two block reorgs, but all of that hasn't really happened in a very long time.
Even two block reorgs haven't, I think, three or four years since a two block reorg happened.
And nowadays, we have a fairly decent propagation on the network, and we see one block reorgs only about every two or three weeks.
So this is why we need a blockchain.

## How does the blockchain work?

Speaker 0: 00:12:18

Like how does a blockchain work?
So it's a pretty small data structure.
Actually, the header has only 80 bytes.
The most important part that makes it a chain is each header commits to the preceding block by including the previous block's hash.
So that's 32 bytes right there.
Now I think most of you had induction in math where you have a proof concept of if I can prove it for one item and can prove if it happens for one item, the next item is covered by the same proof.
And then it belongs to all items.
Well, it's sort of the same here with the blockchain.
You take the Genesis block, which was a little more arbitrary because it doesn't have a predecessor.
And then every single block chains from the genesis block and points at the previous block.
So they're all connected.
You can't stuff anything in between.
You can't change anything back into history without making everything that follows invalid.

Speaker 1: 00:13:20

A couple of questions come out of that.
One, how does someone get a Genesis block when they're syncing for the first time?

Speaker 0: 00:13:26

The Genesis block is hard-coded in the software, right?
It's sort of like the anchor point for the whole blockchain.

Speaker 1: 00:13:33

And two, wouldn't it make sense when one is syncing and sort of getting the whole history that they can ask a bunch of different nodes out of order and then assemble it locally?
That would be faster, right?

Speaker 0: 00:13:46

Sort of, but a lot of the validation work can only be done when you have looked at the previous blocks.
So what a node does when it syncs is that it builds the UTXO set.
So the blockchain is basically the journal and the UTXO set is the ledger of balances.
And to keep track of all the balances, you need to know the previous balances.
Then the current block gives you basically the change set of the previous balances to the new balances.
So to build that, you need them in the right order.
But the idea is a good one.
I think you talked about this with Peter already in the first episode.
But header first synchronization takes advantage exactly of that.
The header itself is only 80 bytes.
And the body of the block, which is the transactions and a lot more data, is committed to by a 32 byte demercal root in the block header.
And that ensures that the transactions are kept exactly in that order.
They need to be byte for byte exactly the same.
Otherwise, the hash is incorrect.
And then, of course, it doesn't fit to the block header.
Yes, you can collect the data from peers to assemble later locally.
But generally, you want to check it in order in order to be able to build one block on the other and to assemble the UTXO set.

Speaker 1: 00:15:10

Right.
So we will go back and we also did an episode on the UTXO set with John.
So that was our first chain code decoded.
And we also have the Ultra Prune episode with Peter, which we'll link to.

## Why does Bitcoin converge on one chain?

Speaker 1: 00:15:21

So why does Bitcoin converge on like one chain?
You would imagine that miners are competing and often flooding the network with different chains because they want to get the miner reward.
How does the network converge on one?

Speaker 0: 00:15:35

So miners spend an actual real-world cost to do mining.
They have to first buy hardware, and then they spend electricity, which cannot be converted back from the proof of work they've done to perform proof of work.
So they have a real world cost and they only get paid when they find blocks.
Blocks that are part of the best chain and mature for at least 100 blocks because current bases only get plant-based rewards.

Speaker 1: 00:16:04

And to be clear, we have to probably differentiate between pools and miners because there's not a lot of solo miners out there.
So when we're saying they, it's probably pools.
Miners get paid in a different way, which we'll maybe go into in another episode.
Right.
Mining pool operators, basically.

Speaker 0: 00:16:22

Basically, when a new block is found, a miner or mining pool operator has the choice, do I want to compete with this block and expend energy to have a competing block eventually that may or may not become part of the longest chain?
Or do I want to just accept that somebody else got this block and then try to get the block reward for the next block?
So it turns out that if you try to compete against a whole network that has converged on this new best chain tip, well, you lose most of the time.
There was a widely regarded paper on selfish mining a while ago, and it shows that once you have like 33% of the total global hash rate, it can be profitable to do shenanigans in that way.
But if we're assuming that miners and operator doesn't control that much hash rate or is not interested in playing games, they usually always are incentivized to just continue the best chain they know of because competing will make them less money.

Speaker 1: 00:17:27

Makes sense.
So that's why miners accept blocks found by other miners because it's just in their best economic interest.

Speaker 0: 00:17:34

Right.
And this is different to other consensus protocols where you do not have an actual real world cost that you're expending all the time, where you lose money if you're not cooperating with the rest of the network.
So this actual real-world cost is actually one part of the incentives to work for the best of the network.

Speaker 1: 00:17:54

So we have this system where miners are looking for blocks and there's quite a variance in when blocks are actually found.

## Will we always find a new block?

Speaker 1: 00:18:05

How can we be sure that there's actually going to be another block found?

Speaker 0: 00:18:08

JOHN MUELLER.
Yeah, especially since they go through the non-space in less than a second.
That question comes up quite often, and it's correct.
A single ASIC can quickly go through the whole non-space, less than a second.
But there's more entropy sources in the block header that allow you to increase the space that you're searching for in the next block.
So obviously, the previous block hash is fixed, so is the difficulty statement.
But what is not fixed is the version field.
29 bits of the 32 bits are actually not encumbered by any rules.
Well, they might be interpreted for soft fork activation, but they're available for stuff like overt ASIC boost or just malleating them generally.
You can vary the timestamp.
You do that every second already naturally, but you can actually do time rolling.
I think it's fallen out of disuse, but people were doing it more in like earlier years of Bitcoin.
And you actually get a fairly large range in which you can pick the timestamp.
So about one hour in the past and two hours in the future, which gives you another 13 bits of entropy.
And then the nonce has four bytes, so 32 bits.
And of course the Merkle root itself has 256 bits, 32 bytes of entropy.

## Mining pools have disjoint hashing spaces

Speaker 0: 00:19:30

I think it's very important to note that every miner is working on a completely unique set of block templates.
And why is that?
Well, when miners try to get paid, they build the first transaction in the block, the coinbase transaction.
And it's the only transaction that's allowed to have no inputs.
What it does is it pays out the transaction fees and the block subsidy to pay out the block reward in total to the miner's address, right?
So when a miner builds a block template, they include their own address as the recipient of the reward in their template.
And when they find a valid block, this transaction is included.
So each miner pays themselves.
And by winning the distributed lottery and becoming the sole author of the block at a specific height, they get to print new money up to the block subsidy amount and send it to themselves.
Since they all have separate addresses that they want to pay to, And I think mining pool operators also split up the workspace for the mining pool participants by giving them separate addresses that they work towards.
Each block template will have a different Merkle root because the coinbase transaction ID is different because it pays to a different address.
So the merkle tree will be different and the merkle root will be different and that makes the block header different.
Throwing the block header into SHA-256, which is pseudo-random, and for whatever input it gets, it'll basically generate a random 256 bit digest.
And since they use different addresses, all of these will be unique and everybody works on separate workspace.
So no miner will ever repeat the work of other people.
I've just shown you that it has like, I don't know, some 330 bits of entropy, which is bigger than 256 bit of the digest space.
So I think we're good.
We will be able to find some input.

Speaker 1: 00:21:36

For a while.

Speaker 0: 00:21:38

Yeah.

Speaker 1: 00:21:41

It's not like Satoshi foresaw that there would be this much hash rate on the network because otherwise the non-space would be bigger, right?

Speaker 0: 00:21:49

Right, right, right.
But the difficulty and the hash rate grow in tandem, right?
In fact, the hash rate grows and that makes the difficulty rise to meet the new hash rate to reset the interval to roughly 10 minutes, right?
Unless suddenly overnight, 90% of the hash rate drops off the face of the earth.
And even then, they just need to take about 10 times as long until they find the random block template that happens to hash to a valid block, then given that there's a ton of people waiting with their transactions at that point, they'd be incentivized to add more hash rate and it would be settled.

Speaker 1: 00:22:28

We saw a little bit of this with the Bcash forks and playing around with trying to adjust the hash rate to the difficulty.
It got a little messy on that chain.

Speaker 0: 00:22:37

But it was pretty smooth on the Bitcoin side, actually.
Yeah.

Speaker 1: 00:22:40

Well, the market took care of that for us.
Great.
Well, that was fun.
Yeah.
We'll keep it rolling.
Going back to basics.
If you have ideas what we should be talking about.
Some of these are sourced from Merch's lengthy experience with Stack Exchange.
But yeah, if you have ideas on other things that you'd like to go into.
All right.
Thanks for joining us.

Speaker 0: 00:23:03

Hot in here.
