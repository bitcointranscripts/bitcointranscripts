---
title: 'Chaincode Decoded: Blockchain'
transcript_by: varmur via review.btctranscripts.com
media: https://podcasters.spotify.com/pod/show/chaincode/episodes/Chaincode-Decoded-Blockchain---Episode-14-e11n7tl
tags:
  - mining
speakers:
  - Mark Erhardt
  - Adam Jonas
summary: In this Chaincode Decoded segment we talk about the fundamental role of Bitcoin's blockchain and some of its peculiarities.
episode: 14
date: 2021-05-27
additional_resources:
  - title: Episode 1 with Pieter Wuille
    url: https://podcast.chaincode.com/2020/01/27/pieter-wuille-1.html
  - title: 'Episode 5: The UTXO set'
    url: https://podcast.chaincode.com/2020/02/26/utxos-5.html
  - title: 'Majority is not Enough: Bitcoin Mining is Vulnerable'
    url: https://www.cs.cornell.edu/~ie53/publications/btcProcFC.pdf
  - title: Entropy sources in the block header
    url: https://bitcoin.stackexchange.com/a/96442/5406
  - title: Eschaton block
    url: https://twitter.com/orionwl/status/969903330523865088
aliases:
  - /chaincode-labs/chaincode-podcast/chaincode-decoded-blockchain/
---
## Introduction

Mark Erhardt: 00:00:00

However long it has been since the last block (has) been found, the next block is expected to take 10 minutes.
So if you have been waiting for 10 minutes, or hashing for 10 minutes already, next block is still in about 10 minutes.
Even if it's been an hour, it's going to take 10 minutes until the next block comes.

Adam Jonas: 00:00:28

Welcome to the Chaincode Podcast.
I'm here with Murch.
Today, we are going to talk about blockchain fundamentals.
Let's get to it.

## Purpose of the blockchain

Adam Jonas: 00:00:40

Let's start from the very beginning.
Why do we need a blockchain?

Mark Erhardt: 00:00:46

We have a distributed system, right?
Everybody is in different places, they have latency in between.
We don't have a central coordinator, and we still need to find a way to get together and agree on a single ground truth.
Basically what we are doing is we hold a distributed lottery to elect a single author to write the next block, and we use their perspective of what the next block should be.
By picking just a single author, we now can decide the order of transactions, how they appeared on the network, and have a quasi-central construct that is created distributedly to synchronize with.
By ensuring that everybody gets a blockchain eventually, we get guaranteed propagation of transactions to every participant.
Through the Proof-of-Work scheme, we make the history immutable because every block builds on the previous ones.
We additionally have a way to distribute the money supply.
All of that in a distributed way without having someone decide.

## Mining is a lottery, not a race

Adam Jonas: 00:01:56

And so you use the word lottery and not something like race.
Why isn't it just a race?

Mark Erhardt: 00:02:02

People often describe the work that Bitcoin miners do as solving complicated computation or something like that, but that's not really a good way of describing it.
Essentially, miners use their hardware to participate in a lottery.
Every time they try with a block template (whether it) hashes to a valid block, they buy a ticket for the lottery, and there's a very small chance that a ticket wins.
When the ticket wins, they have found a new valid block, they send it to the network and update everybody to the new state of the network, and the lottery starts over.
Sure, there's complicated math involved in hashing, but it's not complex work that they're doing, they're not solving a riddle, they're buying tickets in a lottery.

Adam Jonas: 00:02:53

Right, so having a lot of hash power doesn't give you the advantage in that you can add it up to be able to go faster than someone else to find (the solution to) this complex problem.
It just gives you more lottery tickets.

Mark Erhardt: 00:03:06

There's often this misconception that there's a stack of work to power through, but that's not the case.
Every single attempt - taking a block template and hashing it to check whether the hash is low enough to constitute a valid block - is completely independent.
There is no progress here.
If you've done 10 hashes already, you're no way ahead from somebody that's just doing their first hash.
This is what makes it (more) a lottery, and not - the fastest miner always wins.
Every single attempt has the same likelihood of winning, and you don't know whether any of the tickets are more likely to win until you try them.

Adam Jonas: 00:03:48

When you say fastest, you mean more hashes per second compared to another miner, like more other hardware that isn't computing as quickly?

Mark Erhardt: 00:03:56

Yeah, exactly.
Optimally, if you ignored latency and all that, basically this would lead to people having the relative chance of winning the next block as the ratio of hashrate they have of the global hashrate.
So that's the optimum.
It's a little less exact because there is latency, and it takes a moment for people to validate the new block when it gets propagated and things like that, but it's pretty good.
Given the long window, the long target block interval of 10 minutes, the latency is actually a very small portion of the overall window in which a new block is tried to (be found).
Interestingly enough, since there is no progress and all of these events are independent, however long it has been since the last block (has) been found, the next block is expected to take 10 minutes.
So if you have been waiting for 10 minutes or hashing for 10 minutes already, next block is still in about 10 minutes.
Even if it's been an hour, it's going to take 10 minutes until the next block comes.

## Why doesn't the same miner always win?

Adam Jonas: 00:05:04

Right, so that does lend itself to the lottery analogy more than the race analogy, and you're not getting to a certain point...
Why doesn't the same miner or the same pool, with the most hashrate just win every time?

Mark Erhardt: 00:05:19

The important points here are everybody works on a unique set of inputs due to having different addresses that they're trying to pay the block reward to, and there's no progress in mining.
So every single block template being hashed, every single hash attempt, is an independent random event with a minuscule chance of succeeding.
If you do a random event generator again and again, eventually you will win.
But you might win after 10 tries, while somebody else has done 5 million tries already.

## What happens if two blocks are found at the same height?

Adam Jonas: 00:05:55

That's just how lotteries work.
So there's this lottery, and the lottery pretty much entitles the pool to not only pay themselves through the reward, but also print the block, which then is distributed to the network.
So what happens if there are two blocks found at the same height and they're competing, what happens to the transactions in those blocks?

Mark Erhardt: 00:06:20

Since there's latency in the system and then a little delay for checking the block, occasionally another miner will find a block at the same time,
or two miners will, and it happens about every two or three weeks.
In that case, each of these miners will have included whatever transactions they thought should be in the next block.
That's usually just the transactions that pay the highest fee rate, they optimize for the biggest fee they can collect in a block, and these two competing blocks have a very large overlap.
I think we've had this question a ton of times on Stack Exchange where somebody asks - "So what happens if a transaction is in one block and then it doesn't become part of the longest chain, but a stale chain tip?"
From the perspective of the competing blocks, the other block doesn't exist.
It's not part of the best chain, it's irrelevant, right?
So they can both have the same transactions in the same block, and any transactions that were not included, they're still in the mempool of the node that accepted the other competing block.
Eventually, one of the two blocks will sire another successor block, and every node will say - "That's the best chain because it has the most work", reorganize back to that chain tip, and all the transactions that were previously confirmed in the competing block, either they're already included in the two competing blocks now, in the new best chain, or they're still in the mempool, so the miners can just pick them in a future block.

Adam Jonas: 00:07:59

Are they reintroduced to the mempool?
Because you would imagine if there's that reorg...
So say there's two blocks, 1A and 1B, and 2A comes from 1A.
The miners that were originally looking at 1B, the transactions included in that, and it no longer becomes a stale block.

Mark Erhardt: 00:08:18

Right, a temporarily embarrassed best chain.

Adam Jonas: 00:08:22

Okay, so the transaction that was in that block is then reintroduced to the mempool?

Mark Erhardt: 00:08:30

Yes.
So operationally, what a bitcoin node does is it actually rolls back to the last shared block between those.
Then, using the reverts (`rev*.dat` files) that are stored for every block, it builds the new blocks from that previous shared ancestor.
I think it does all of this in memory, it doesn't really write back everything to the UTXO set and then take it right out again, because there's such a large overlap usually between two competing blocks.
It just does it in memory.
Basically that's exactly what it does, it goes back, puts everything back in the mempool, then applies the two new blocks.

## The longest reorgs

Adam Jonas: 00:09:11

So there's this assumption that these reorgs are never particularly deep.
In what circumstances have we seen some big reorgs?
What are the longest ones that we've seen in the wild?

Mark Erhardt: 00:09:23

Let's distinguish between natural reorgs and other events that caused a large reorg.
The longest natural reorgs we've seen were four blocks deep, and those last happened in 2012, so some time has passed.

Adam Jonas: 00:09:39

Four doesn't seem that much either.

Mark Erhardt: 00:09:41

Yeah.
Well, it's pretty weird, right?
It means that two miners each found four blocks in a row, without hearing about the other chain, or without accepting the other chain as the best tip up to that point.
I assume that that was a series of very quick blocks each, otherwise, that would just be insane - like a 10 minute block in between and the other miner hasn't heard about it.
Since then, the latency on the network has dropped a lot.
We have header first synchronization, which also means that you don't have to send a whole megabyte of block, but just 80 bytes to announce the new header.
On the one hand, it's not that long, but on the other hand, it still sounds pretty insane.

Adam Jonas: 00:10:27

Then you said there were some maybe unnatural reorgs that had happened in the past.
What are some of those?

Mark Erhardt: 00:10:34

We had a value overflow bug in August 2010, where somebody created 184 billion bitcoins, and obviously that got reorged out.
I think that actually took a patch, and the patch had to get distributed, but then 2010 was really the nascent...

Adam Jonas: 00:10:55

Right in the beginning, yeah.

Mark Erhardt: 00:10:57

Another one that we saw was...
Was it the 0.8 upgrade for Bitcoin where there was a mismatch in the behavior of the LevelDB and Berkeley DB - when that was switched?

Adam Jonas: 00:11:10

It was the number of locks, yeah.
Peter goes over that in his episode, and it was a quirk.

Mark Erhardt: 00:11:20

Basically it was a hard fork.
It was a hard fork that happened to get triggered by a block actually exhibiting the behavior that was different.
I think it was more than 30 blocks that got reorged out.

Adam Jonas: 00:11:30

Yeah, that had to be a coordinated effort to pretty much stop the chain and restart.
There's some debate as to whether that's a hard fork, but it was definitely something.

Mark Erhardt: 00:11:42

It was basically a smaller set of possible valid blocks that got extended to a bigger set.
So, whatever.
We can go into soft forks versus hard forks some other day or episode.
So there were a few instances of three block reorgs and two block reorgs, but all of that hasn't really happened in a very long time.
I think it's been three or four years since even a two block reorg happened.
Nowadays we have a fairly decent propagation on the network, and we see one block reorgs only about every two or three weeks.

## How does the blockchain work?

Adam Jonas: 00:12:16

So this is why we need a blockchain.
How does a blockchain work?

Mark Erhardt: 00:12:18

It's a pretty small data structure, the header has only 80 bytes.
The most important part that makes it a chain is each header commits to the preceding block by including the previous block's hash.
That's 32 bytes right there.
I think most of you had induction in math where you have a proof concept of - "if I can prove it for one item, and can prove if it happens for one item the next item is covered by the same proof, and then it belongs to all items".
It's sort of the same here with the blockchain.
You take the Genesis block, which was a little more arbitrary because it doesn't have a predecessor, and then every single block chains from the Genesis block and points at the previous block, so they're all connected.
You can't stuff anything in between.
You can't change anything back in the history without making everything that follows invalid.

Adam Jonas: 00:13:20

A couple of questions come out of that.
One, how does someone get a Genesis block when they're syncing for the first time?

Mark Erhardt: 00:13:26

The Genesis block is hard-coded in the software.
It's sort of like the anchor point for the whole blockchain.

Adam Jonas: 00:13:33

And two, wouldn't it make sense when one is syncing and getting the whole history, that they can ask a bunch of different nodes out of order and then assemble it locally?
That would be faster, right?

Mark Erhardt: 00:13:46

Sort of, but a lot of the validation work can only be done when you have looked at the previous blocks.
What a node does when it syncs is that it builds the UTXO set.
The blockchain is basically the journal and the UTXO set is the ledger of balances.
To keep track of all the balances, you need to know the previous balances.
Then the current block gives you the change set of the previous balances to the new balances.
To build that, you need them in the right order.
But the idea is a good one, I think you talked about this with Peter already in the first episode, header first synchronization takes advantage exactly of that.
The header itself is only 80 bytes.
The body of the block, which is the transactions and a lot more data, is committed to by a 32 byte Merkle root in the block header.
That ensures that the transactions are kept exactly in that order.
They need to be byte for byte exactly the same, itherwise, the hash is incorrect, and then of course it doesn't fit to the block header.
Yes, you can collect the data from peers to assemble later locally, but generally, you want to check it in order, in order to be able to build one block on the other and to assemble the UTXO set.

Adam Jonas: 00:15:10

Right.
We also did an episode on the UTXO set with John, that was our first Chaincode decoded.
And we also have the Ultra Prune episode with Peter, which we'll link to.

## Why does Bitcoin converge on one chain?

Adam Jonas: 00:15:21

Why does Bitcoin converge on one chain?
You would imagine that miners are competing and often flooding the network with different chains because they want to get the miner reward.
How does the network converge on one?

Mark Erhardt: 00:15:35

Miners spend an actual real-world cost to do mining.
They have to first buy hardware, and then they spend electricity, which cannot be converted back from the Proof-of-Work they've done to perform Proof-of-Work.
So they have a real world cost and they only get paid when they find blocks - blocks that are part of the best chain and mature for at least 100 blocks.

Adam Jonas: 00:16:04

To be clear, we have to probably differentiate between pools and miners because there's not a lot of solo miners out there, so when we're saying they, it's probably pools.
Miners get paid in a different way, which we'll maybe go into in another episode.

Mark Erhardt: 00:16:19

Right, mining pool operators, basically.
When a new block is found, a miner or mining pool operator has the choice.
Do I want to compete with this block and expend energy to have a competing block eventually that may or may not become part of the longest chain?
Or do I want to just accept that somebody else got this block, and then try to get the block reward for the next block?
It turns out that if you try to compete against the whole network that has converged on this new best chain tip, you lose most of the time.
There was a widely regarded [paper](https://www.cs.cornell.edu/~ie53/publications/btcProcFC.pdf) on selfish mining a while ago, and it shows that once you have 33% of the total global hashrate, it can be profitable to do shenanigans in that way.
But if we're assuming that miners and operators do not control that much hashrate, or (are) not interested in playing games, they usually always are incentivized to just continue the best chain they know of, because competing will make them less money.

Adam Jonas: 00:17:27

Makes sense, so that's why miners accept blocks found by other miners because it's just in their best economic interest.

Mark Erhardt: 00:17:34

Right, and this is different to other consensus protocols where you do not have an actual real world cost that you're expending all the time, where you lose money if you're not cooperating with the rest of the network.
So this actual real-world cost is actually one part of the incentives to work for the best of the network.

## Will we always find a new block?

Adam Jonas: 00:17:54

So we have this system where miners are looking for blocks and there's quite a variance in when blocks are actually found.
How can we be sure that there's actually going to be another block found?

Mark Erhardt: 00:18:08

Yeah, especially since they go through the nonce-space in less than a second.
That question comes up quite often, and it's correct, a single ASIC can quickly go through the whole nonce-space, (in) less than a second.
But there's [more entropy sources](https://bitcoin.stackexchange.com/a/96442/5406) in the block header that allow you to increase the space that you're searching for in the next block.
Obviously, the previous block hash is fixed, so is the difficulty statement.
What is not fixed is the version field - 29 bits of the 32 bits are not encumbered by any rules.
Well, they might be interpreted for soft fork activation, but they're available for stuff like [Overt ASICBoost](https://bitcoinops.org/en/topics/asicboost/) or just malleating them generally.
You can vary the timestamp.
You do that every second already naturally, but you can actually do time rolling.
I think it's fallen out of use, but people were doing it more in (the) earlier years of Bitcoin.
You get a fairly large range in which you can pick the timestamp, about one hour in the past and two hours in the future, which gives you another 13 bits of entropy.
Then the nonce has four bytes, so 32 bits.
Of course the Merkle root itself has 256 bits, 32 bytes of entropy.

## Mining pools have disjoint hashing spaces

Mark Erhardt: 00:19:30

I think it's very important to note that every miner is working on a completely unique set of block templates.
Why is that?
When miners try to get paid, they build the first transaction in the block, the coinbase transaction, and it's the only transaction that's allowed to have no inputs.
What it does is it pays out the transaction fees and the block subsidy - the block reward in total - to the miner's address.
When a miner builds a block template, they include their own address as the recipient of the reward in their template.
When they find a valid block, this transaction is included, so each miner pays themselves.
By winning the distributed lottery and becoming the sole author of the block at a specific height, they get to print new money - up to the block subsidy amount - and send it to themselves.
Since they all have separate addresses that they want to pay to, and I think mining pool operators also split up the work-space for the mining pool participants by giving them separate addresses that they work towards, (so) each block template will have a different Merkle root because the coinbase transaction id is different because it pays to a different address.
So the Merkle tree will be different, and the Merkle root will be different, and that makes the block header different.
Throwing the block header into SHA-256, which is pseudo-random - for whatever input it gets, it'll basically generate a random 256 bit digest.
Since they use different addresses, all of these will be unique and everybody works on separate work-space.
So no miner will ever repeat the work of other people.
I've just shown you that it has (approximately) some 330 bits of entropy, which is bigger than 256 bit of the digest space.
So I think we're good, we will be able to find some input.

Adam Jonas: 00:21:36

For a while.

Mark Erhardt: 00:21:38

Yeah, up to the [Eschaton Block](https://bitcoin.stackexchange.com/questions/119223/is-there-a-well-defined-last-block), right?

Adam Jonas: 00:21:41

It's not like Satoshi foresaw that there would be this much hashrate on the network because otherwise the nonce-space would be bigger, right?

Mark Erhardt: 00:21:49

Right, right, right.
But the difficulty and the hashrate grow in tandem, right?
In fact, the hashrate grows and that makes the difficulty rise to meet the new hashrate to reset the interval to roughly 10 minutes.
Unless suddenly overnight, 90% of the hashrate drops off the face of the earth.
Even then, they just need to take about 10 times as long until they find the random block template that happens to hash to a valid block.
Then given that there's a ton of people waiting with their transactions at that point, they'd be incentivized to add more hashrate and it would be settled.

Adam Jonas: 00:22:28

We saw a little bit of this with the Bcash forks and playing around with trying to adjust the hashrate to the difficulty, and it got a little messy on that chain.

Mark Erhardt: 00:22:37

But it was pretty smooth on the Bitcoin side, actually.

Adam Jonas: 00:22:40

Well, the market took care of that for us.
Great.
Well, that was fun.
We'll keep it rolling,
Going back to basics.
Some of these are sourced from Murch's lengthy experience with Stack Exchange.
Thanks for joining us.
