---
title: "Mempool Ancestors and Descendants"
transcript_by: kouloumos via tstbtc v1.0.0 --needs-review
media: https://podcasters.spotify.com/pod/show/bitcoinbrink/episodes/Mempool-Ancestors-and-Descendants-e1ald5e
tags: ['cpfp']
speakers: ['John Newbery', 'Gloria Zhao']
summary: "John and Gloria continue their discussion of Bitcoin's mempool by explaining parent, child, ancestor and descendant transactions."
date: 2021-11-24
additional_resources:
  - title: Child pays for parent
    url: https://bitcoinops.org/en/topics/cpfp/
  - title: https://brink.dev/
    url: https://brink.dev/
---
## Parent and child transactions

Speaker 0: 00:00:00

Hi John.

Speaker 1: 00:00:01

Hi Gloria.

Speaker 0: 00:00:02

Feel like talking about mempool ancestors and descendants today?

Speaker 1: 00:00:06

Yeah, let's do it.

Speaker 0: 00:00:06

All right.
Let's define ancestors and descendants first.
Or maybe let's define parents and children first.

Speaker 1: 00:00:13

Okay.
So in Bitcoin, when you have a transaction, you have the person or the owner spending the coin, sending it to someone who's receiving it.
And we define that relationship by the sender puts a public key or a hash of a public key in the output and the person receiving it, when they come to spend it again, they put a signature into the input.
That goes all the way back to the white paper where Satoshi says, we define an electronic coin as a chain of digital signatures.
Each owner transfers the coin to the next by digitally signing a hash of the previous transaction on the public key of the next owner and adding these to the end of the coin.
So Toshi's talking about a chain actually is a bit more complex than that because it's more like a graph because a transaction can have multiple inputs and multiple outputs.
Right.
So your transaction has outputs and then when you come to spend those outputs, they become inputs in the next transaction.
And we define that relationship as one transaction spending the outputs created by the previous transaction as a child-parent relationship.
So the transaction spending the output is the child and the transaction that's created in the first place is the parent.

Speaker 0: 00:01:26

Right.
And one parent can fund many children and many parents can be consolidated into one child.

Speaker 1: 00:01:33

Yeah, exactly.
So the blockchain is simply a kind of a transcript or a log of everything that's happened before and it contains all of the transactions.
And those transactions have this structure which in computer science we call a graph and more specifically a directed graph because we have that direction relationship and even more specifically a...

Speaker 0: 00:01:53

Directed acyclic graph.

Speaker 1: 00:01:56

Exactly.
Exactly.
Because a transaction cannot be its own parent or its own ancestor.
So we talked about parent-children there.
We can extend that relationship and talk about a parent of a parent being an ancestor.
So all parents and all parents of parents and all parents of parents of parents are ancestors and descendants in the opposite direction.
So a child is a descendant, a child is a child and so on.

Speaker 0: 00:02:18

And why is this relevant in a mempool?

Speaker 1: 00:02:22

Good question.

## Relevance of ancestors and descendants to the mempool

Speaker 1: 00:02:23

Well, so far we've been talking about this kind of abstract idea of ancestors and descendants and it's all a little bit academic and maybe doesn't seem that interesting.
And in the blockchain, it's not really that interesting.
It's just kind of historic artifact.
All we care about is the set of unspent outputs.
But in the mempool, we do care about it a lot because unlike the blockchain, which is basically finalized and static, You know, there can be reorgs, but as you go deeper into the blockchain, that's all fixed.
The mempool is very different.
It's always changing.
It's very dynamic.
Things are being added, things are being removed.
And so we need to care about the shape and the properties of this graph when we're adding and removing things.

Speaker 0: 00:03:03

Yeah.
So we always want the mempool to have the best candidates for inclusion in the block by fee.

Speaker 1: 00:03:09

That's right.

Speaker 0: 00:03:10

And transactions leave the mempool two ways, either they're mine, included in block, or we're evicting them in favor of a different transaction to be added to the mempool.

Speaker 1: 00:03:22

Well, there are more ways than that, actually.

Speaker 0: 00:03:24

Or they're expired or conflicted.

Speaker 1: 00:03:27

Exactly.
So there's several ways that a transaction can leave the mempool, and there's a couple of ways it can enter the mempool.
So maybe we should kind of enumerate those.
The most obvious way for a transaction to enter the mempool is that you receive it from a peer on the peer-to-peer network.
You validate that transaction, all of the outputs that it's spending exist, it's a valid transaction and you pop it in your mempool and send it to your peers.

Speaker 0: 00:03:50

Or it can come from your clients.

Speaker 1: 00:03:52

Or it can come from a local application, yep, your wallet or some other RPC client, yep.

Speaker 0: 00:03:57

Right.
And it can leave either because it is invalid or you don't want it anymore or it goes into a block, essentially.

Speaker 1: 00:04:07

I'm not sure I'd agree with the first one.
If it's invalid, it would never be put into the mempool.

Speaker 0: 00:04:11

Invalid as in like it got conflicted because of transaction to block, for example.

## Reasons transactions leave the mempool

Speaker 1: 00:04:16

Right, So let's enumerate those ways that it can leave the mempool.
The most obvious is that it gets included in a block.
So the mempool is this holding area for transactions that might get included in a block, and then you receive a block and hey presto, it actually does have that transaction.
You don't need to keep it in your mempool anymore.
Closely linked to that is you might get a block that contains a conflicting transaction.
So you've got transaction A in your mempool, you receive a block, it's called A2, that spends the same outputs and that's now part of the blockchain and A is no longer valid.
I think that's what you were referring to earlier.
That's called a conflict or it conflicts with something in a block and we have to remove that from the mempool.
Next up we have eviction.
So we remove transactions from the mempool for a couple of reasons.
One is the mempool's got too full and we remove the transactions that have the lowest fee rate or more specifically the lowest ancestor fee rate, descendant fee rate.
Descendant fee rate.
Descendant fee rate, that's right, because they're the least likely to be useful for a miner in future.
So as we shed transactions from the mempool, we remove those ones first.
Another reason we remove transactions from the mempool is if they've been hanging around for too long.
So if a transaction's been in the mempool for two weeks, we will expire it.

Speaker 0: 00:05:31

Do we do that even when we're not full?

Speaker 1: 00:05:33

Yep.
And what else?
We might replace it.
So bit 125, replace by fee, defines some policy rules that we would use where if we receive a transaction on the peer-to-peer network that conflicts with a transaction in the mempool or some transactions in the mempool, we may replace those transactions with a new one if it meets certain criteria.

Speaker 0: 00:05:55

Someone asked me if there's a way for a node operator to manually remove a transaction from the mempool.

Speaker 1: 00:06:01

There is not.

Speaker 0: 00:06:02

I think there's a way that you could do it if you prioritised negative max money.
It would get evicted the next time you did any kind of mempool trimming.

Speaker 1: 00:06:15

Okay, yep.

Speaker 0: 00:06:16

Oh, if it's full.
If it's not full, I think it might still stay.

Speaker 1: 00:06:19

Yeah.
Assuming the mempool's full, it removes stuff from the bottom.
And so deprioritizing a transaction would send it to the bottom.

Speaker 0: 00:06:26

Yeah.
And you could, in the Bitcoin core wallet, abandon transaction and then it'll stop rebroadcasting it.
And then it would naturally, hopefully, come out of the mempool.

Speaker 1: 00:06:36

Potentially but what you need to keep in mind is that your mempool is not necessarily reflective of the rest of the network's mempool.
So once it's out, once a transaction has been broadcast to your peers and they've transitively broadcast it to their peers and it's gone out into the network, it's going to be there forever more unless it gets conflicted with something that's included in the blockchain.
Yeah.
Okay.

## Block construction considerations for miners

Speaker 1: 00:06:58

So those are ways that transactions can be removed from the mempool.
And then maybe we should mention when a miner is creating a block, they're selecting transactions from the mempool.
So they're not removing them yet because they haven't been put in the block.
But when they're constructing that block, they will choose transactions from the mempool based on the ancestor fee rate, because they're trying to maximize the amount of fee that they put in their block.

Speaker 0: 00:07:20

Should we break that down?
Why exactly it's ancestor fee rate and not descendant or base?

Speaker 1: 00:07:25

So transactions in the mempool can spend outputs of transactions in the blockchain, But you can also have, like we talked about, children and descendants.
So you could have transactions in the mempool spending the outputs of other transactions in the mempool.
So you have this directed graph, which is all the transactions that have ever existed included in the blockchain.
And then right at the edge of that, the very top or the bottom, depending on how you're looking at it, you have some unspent transaction outputs, UTXOs, and then you have your graph of transactions in the mempool that kind of extends the graph of confirmed transactions.
So when a miner is looking at which transactions to include, they want to include ones which have high fee, but those transactions with high fee might have ancestors in the mempool, they might be spending the outputs of other transactions, they're dependent on other transactions in the mempool.
And those other transactions have low fee.
So to include the transaction with high fee, you also need to include first the transaction with low fee, because the blockchain has to be ordered.
You can't spend a transaction output that does not yet exist.

Speaker 0: 00:08:30

Exactly.

Speaker 1: 00:08:31

So that's how a miner looks at the transactions in the mempool and decides which ones to include in a block.
They look at the ancestor fee rate because to get the descendant, they need to include all of the ancestors first.
And so this is where we come back to the graph theory because this is quite a difficult problem to solve optimally.
We have heuristics for selecting what we think is a very good block, but if we wanted to exhaustively search the space of all potential blocks, that would be a very computationally intensive task.
So we have these heuristics that kind of range over that graph and try and find a good set of transactions to maximize the fee.
And so we need the graph to have some structure and be able to tractably walk over that graph.

Speaker 0: 00:09:18

Yeah, and when you're a miner and you're constructing a block template, you care about the speed at which you construct that template more than the extra 100 megabytes to store that ancestor and descendant data, because you want to get started on the next block as soon as possible.

Speaker 1: 00:09:35

Exactly.
Yeah.
So you mentioned that ancestor and descendant data.
So the mempool is not simply just a pool of transactions.
We also include some metadata And that metadata is things like the ancestor fee rates of a transaction.

Speaker 0: 00:09:49

Yeah.
And iterators to said parents and children.
I think if you have a mempool with 300 megabytes of storage available, Only about one fourth of that is the raw transaction data itself and the rest is metadata.
And a lot of people are really surprised to hear that, but it is important information that needs to be stored because we're preferring to use space instead of time.

Speaker 1: 00:10:18

Right.
And going back, why do miners care about the time it takes to construct a block?
Because all of that time that they spend constructing a block is wasted time.
So if it's a 10 minute interblock interval, and so 600 seconds, and it takes them six seconds to construct a block.
That's 1% of revenue that they are just leaving on the table.

Speaker 0: 00:10:39

Yeah, exactly.

Speaker 1: 00:10:41

And not 1% of profit.
It's a much higher percentage of profit because obviously they have their overheads and their profit margin is pretty slim anyway.
So these small increments really count to the miners.

Speaker 0: 00:10:52

And is that why sometimes we see empty blocks?

Speaker 1: 00:10:55

That is why we sometimes see empty blocks because...

Speaker 0: 00:10:58

One possible reason.

Speaker 1: 00:10:59

It's one possible reason.
So if a miner receives a block at the tip, they might start doing work immediately before validating that block, before updating their mempool to remove the transactions in their block, in that block.
So they can start work without doing the computation of constructing a block.

Speaker 0: 00:11:17

Yeah, but they still want a block with transactions because of the fees.

Speaker 1: 00:11:22

They prefer to, yeah, that's an incentive.

Speaker 0: 00:11:24

Yeah.

Speaker 1: 00:11:24

So they might start mining with an empty block and then update the template.
Yeah.
As they've done that computational work.

Speaker 0: 00:11:31

But they essentially have to start all over again, searching the non-space.

Speaker 1: 00:11:35

Well every single hash is starting all over again.
You don't make any progress.
So it doesn't make any difference that they've already done some work.
Every time you hash something you're starting from scratch.
You're no closer.

## Full node performance considerations

Speaker 1: 00:11:46

Okay, so we have this graph and we care about performance as you search through it.
Miners care about performance, but also other full nodes on the network care about performance because they are also doing updates to their mempool.
So for example, a bit 125 replacement transaction might push out a bunch of transactions from the mempool.
You might have a chain of transactions, A, B, C, D, E, and then A2 conflicts with A, and so you then need to remove B, C, D, E as well as removing A, because say now they depend on something that's no longer in the mempool.

Speaker 0: 00:12:21

Exactly.
They're invalid.

Speaker 1: 00:12:23

Yeah, they're invalid in that mempool if A2 is in there.

Speaker 0: 00:12:27

This sounds like a good time to talk about why we evict by descendant score rather than ancestor score.

Speaker 1: 00:12:35

Okay, that's a good thing to talk about.
So why do we do that?

Speaker 0: 00:12:38

Well, intuitively it seems like, okay, we want to mine by ancestor score, so why don't we also evict by ancestor score?
But you can have a low ancestor score yet a very high fee child, for example.
So like the most concrete example would be ABC is a chain where C spends B and B spends A, and A has a very low fee.
I don't know, maybe B has a medium fee and C has an extremely high fee.
So C has a very high ancestor score.

Speaker 1: 00:13:15

And A has a very low ancestor score because it's not spending any unspent, unconfirmed transactions.

Speaker 0: 00:13:22

But A has a very high descendant score.

Speaker 1: 00:13:25

Exactly, right.

Speaker 0: 00:13:27

So we don't want to evict this chain, essentially.
Then you can imagine D, which spends C, but has a very low fee.
And we can take D off the chain because we don't need it to mine any of the other transactions.
We only need A and B in order to get C.

Speaker 1: 00:13:46

Right.
So we care about the performance of these algorithms, both in selecting transactions to include in a block and also updating the mempool when you have conflicting transactions or replacement transactions or anything moving that graph, changing the contents of the mempool.
And so to make that tractable, we have limits on the size of that graph.
Specifically those limits are in terms of the ancestor count and ancestor size, and descendant count and descendant size.
So for a transaction to be put in the mempool, it can't have more than 25 ancestors, including itself, so 24 true ancestors.
And the sum of the sizes of itself and the ancestors can be no greater than 101 kilobytes.
And by adding that transaction to the mempool, it can't make any of the existing transactions in the mempool have descendants or packages of descendants that exceed those same limits, 25 and 101.
And so that limits the size of packages and families of transactions in the mempool.

Speaker 0: 00:14:54

Right.
And these are default limits.
You can configure them as a node operator to be whatever you want, but 25 and 101 kilobytes is the default.

Speaker 1: 00:15:06

Yeah.
And that's generally enough for most people.
There might be circumstances where services or exchanges are doing a batch withdrawal and they have lots of customers withdrawing Bitcoin to their private addresses at the same time, they would need to be wary of those limits because they could run into those if they're creating large transactions and those customers are then using those unconfirmed outputs in their transactions.

Speaker 0: 00:15:30

Right.
Yeah.
I've heard of enterprise wallets doing a big fee bump where say they have like 30 customers, outgoing transactions floating in the mempool and they want to add some urgency to that.
So they try to go and fee bump all 30 of them and then they hit the too long mempool chain error.
They're like, what's going on?
But also if you were to increase the limit on your own node, that doesn't necessarily mean that it'll propagate to other nodes.

Speaker 1: 00:15:59

Right.

Speaker 0: 00:16:00

Because their mempools will reject because they have that limit as well.

Speaker 1: 00:16:04

Right.
And that's the thing about policy that to some extent it doesn't matter too much what your own policy is.
It matters what the rest of the network's policy is in terms of transaction propagation.

## Child pays for parent and missing inputs

Speaker 1: 00:16:14

Yeah.
So you have these concepts of ancestors and descendants.
We talked about ancestor fee rate.
So if you have transaction A with a low fee rate and B with a high fee rate, B is incentivizing the miner to include A and B.
And that is used in a technique called Child Pays for Parent.
So if I have a transaction that is unconfirmed in the mempool, it's got a low fee, but I really want it to be confirmed, I can spend one of the outputs in a transaction with a very high fee rate and the miner would then be incentivized to include transaction A and B.
But sometimes that doesn't work because A itself has a fee rate that's too low to get into the mempool.

Speaker 0: 00:16:52

Oh, we're getting into this.

Speaker 1: 00:16:53

We're getting into this.

Speaker 0: 00:16:54

This is like my favorite topic to talk about.

Speaker 1: 00:16:58

Okay, well, let's talk about it a bit then.
So imagine I have a transaction A, I want to spend some of A, but it has a very low fee rate, let's say one satoshi per byte.
And the mempool, network mempools are congested and they've been expiring or evicting transactions from the bottom of their mempool and they won't accept transactions below five satoshis per byte.
So I want A to be included.
I've created now a new transaction B with 100 satoshis per byte.
So I've done child pays for parent.
And then what happens?

Speaker 0: 00:17:29

You get the error for A saying, sorry, this doesn't meet the minimum mempool fee requirement.
And you're like, wait, wait, wait, but what about B?
And it'll say missing inputs because it's spending something that it doesn't know about.
It's like, I did tell you about A and you rejected it, But here, basically you want the node to validate A and B together.

Speaker 1: 00:17:50

Right.
So the way into the mempool, it's a narrow door.
Only one transaction can go through at a time and they need to be assessed serially.
So A comes up, doesn't have the entry fee, gets told to go away.
B comes up and is told, well, you're spending outputs that don't exist.

Speaker 0: 00:18:05

Yeah.
And someone asked me a very good question of like, oh, why don't we look at the transaction candidates in order of their fee rate?
And the answer to that is, well, you don't know the fee rate until you have all of the information.
So in Bitcoin transactions, you don't include the amount in the inputs.
You only include the amount in the outputs.
So the way to calculate a fee amount is you need to find the total inputs and then the total outputs and you subtract them.
But you don't know the input amounts until you go and look up the outputs that they're spending.
And therefore you have to validate transactions in order of like parents before children.
You can't go in order of fee because you don't know until you do it that way.

Speaker 1: 00:18:52

Okay.
So how can you fix that?

Speaker 0: 00:18:54

Well, maybe we can widen the door and let in multiple transactions at a time.

Speaker 1: 00:18:59

That Sounds like a great idea.

Speaker 0: 00:19:01

Yeah.
What about just two at a time?

Speaker 1: 00:19:03

Two at a time.
OK.
Well, let's talk about that next time.

Speaker 0: 00:19:06

Oh, OK.

Speaker 1: 00:19:06

There's a little teaser for the next episode.
All right.
Thanks, Gloria.

Speaker 0: 00:19:10

Thanks, John.
Bye.
