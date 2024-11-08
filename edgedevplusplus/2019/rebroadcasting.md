---
title: Rebroadcast logic in Core
transcript_by: Bryan Bishop
tags:
  - bitcoin-core
speakers:
  - Amiti Uttarwar
date: 2019-09-09
aliases:
  - /scalingbitcoin/tel-aviv-2019/edgedevplusplus/rebroadcasting
---
<https://twitter.com/kanzure/status/1171042478088232960>

## Introduction

Hi, my name is Amiti. Thank you for having me here today. I wanted to talk with you about rebroadcasting logic in Bitcoin Core. For some context, I've been working on improving it this summer. I wanted to tell you all about it.

## What is rebroadcasting?

We all know what a broadcast is. It's hwen we send an INV message out to our peers and we let them know about a new transaction. Sometimes we rebroadcast and send an INV for the same transaction.

Sometimes these transactions might not be in other people's mempools, and there's several reasons why that might happen. It might be related to a failure in the first broadcast. The transaction could have expired from the mempool because it's been around for 2 weeks and there's that default time limit. The transaction may have been evicted from the mempool because of the competitive fee rate market and maybe you had a low fee rate transaction and the other ones had high fee rates and got in there and kicked yours out. There might be network failures, reorgs, transactions might not always be in everyone's mempool. You want them to be in there so that it can get confirmed and sent to a miner.

You rebroadcast because you want your transactions to be propagated and get mined into a block and be confirmed.

## Why do it?

Something to consider.

## How does it currently work?

The logic is presently: once per block, a node rebroadcasts all of its unconfirmed wallet transactions. Every time a node sees a new block come in, it looks at what transactions it has that are still not confirmed and then tries to rebroadcast it and send INV messages to its peer.

This is really bad for privacy.

The node will only rebroadcast if it was the source of that transaction. So if an adversary has a couple of connections open to your node and is paying attention, it's a dead giveaway if it sees another INV message for the same transaction and it can infer that you're the source wallet.

Rebroadcasting is kind of aggressive. It doesn't consider what should be confirmed. If you made a low fee rate transaction, and you were targeting a one day block confirmation target, then between now and that transaction being picked up by a block, then every single time a new block comes in, your node would say oh no my transaction wasn't confirmed in that maybe my peers don't have it, let me tell them about the transaction. But really, that was intentional, which was why you set the low fee rate.

Q: How does your wallet distinguish your transactions from other transactions?

A: Say the first node generates a transaction and told the second node about it. The second node has it in its mempool. The first node decides to rebroadcast that transaction to the second node. The second node would not continue to propagate that, it would just say "I'm good, I have that transaction". Thus it would also not be rebroadcasting it.

Q: It can't conclude that it was in A's mempool.

A: You already received it from that node.

## Dust attack

This leaves a vulnerability called a dust attack.

Nodes define my transactions to be ones where any of its addresses are involved. The way an adversary would take advantage of this is that it would send dust to many different addresses totally at random. Then the node will begin rebroadcasting the transactions where it was receiving this dust amount. So the attacker can then figure out, ah, these addresses belonged to these nodes. That's not great. Let's do better.

## Let's do better

The point of rebroadcasting is to make sure your transactions make it to miner mempools and make it into a block. Can we also maintain privacy or at least improve it? Right now it's pretty bad so I think we can improve it. The proposal that I'm putting together is based on, first, all nodes will rebroadcast not just the ones with wallets enabled. We're revealing less information now. We'll reduce pointless rebroadcasting; we'll add some logic to identify which transactions should have been mined. Third, ew will have decoy transactions. We'll apply logic across all transactions, and this way you will rebroadcast transactions that weren't originated from you.

## What has been mined?

In trying to answer this question of what should have been mined, that's kind of interesting. I thought about looking at the block and identifying the minimum fee rate of any transactions in that block. Sounds great, until you realize there's a handy RPC method called prioritizetransaction which allows miners to apply a private priority independent of a fee rate. By looking at the block, you can't identify with certainty whether the transaction was included because of the fee rate or because of this independent private priority mechanism.

## My mempool

Another way is to compare your own mempool and the latest block and look at the delta of what wasn't included. You construct your expectations of what would be in a block, based on your local mempool. Then you process the new block, and remove the transactions from your mempool that were confirmed, then you have the delta remaining between the expected and the actual and you could rebroadcast those. This seems undesirable because it adds latency to the block acceptance flow where that processing time is important.

The tradeoff of this-- of not having it perfectly precise, is that we would send extra INV messages. This is a hit to bandwidth, but they are quite small. It seems like an acceptable tradeoff between bandwidth and privacy.

## Implementation

On a poisson timer, approximately once per hour, rebroadcast selected transactions. Criteria for transactions is to use CreateNewBlock and mimic the way the miner would form a block. We limit to 3/4 max block weight because we want to leave room for the case where miners uses private prioritize and would discard other transactions. Also, we're going to apply a recency filter and say the transactions must be older than 30 minutes in order to be rebroadcast. So let's look at the top of the mempool, and if they have been around for a while then maybe the miners don't know about it and they need to be rebroadcast. So we get these transactions, we add them to the inv transactions to send, and then they are relayed to your peers just as all transactions are.

In the current implementation, the wallet directly rebroadcasts transactions which is a layer violation. I'd like to pull out the rebroadcast functionality into the node and it's a better division of responsibility. All nodes will rebroadcast, and all transactions can be treated the same. This makes for cleaner code and gives stronger privacy guarantees.

## Wallet resubmit

With this new division of responsibility, the mempool can drop the wallet transaction because of the reasons we talked about like expiry, eviction, unclean restart. The wallet's responsibility is to make sure the local mempool knows about its transaction. Exactly once a day, the wallet attempts to resubmit the transaction to a mempool. It can send it once a day to its local mempool because it's no longer a privacy leak. The mempool will make sure that transactions it knows about are propagated to the network in a reasonable way using this new rebroadcast logic.

This does leave room for an important edge case. The use case is that if you create a transaction with relay disabled, and you submit it to your mempool locally, in the current implementation it would rely on the rebroadcast in order for an iniitial successful broadcast. This can be problematic with my proposed changes for a low fee rate transaction. The way it would go is, you would disable p2p, you would create a transaction with a low fee rate and a several day confirmation target. You inspect it in your mempool, you think it's good to go, then you enable relay back on. With the new rebroadcast logic, it might be several days until that transaction is actually at  the top of the mempool and you would expect it to be confirmed, or it might be a short window of time before that would occur. You don't need your node online that much or to rely on the fact that the node will be online at that exact time to get the first broadcast out. In order to solve that, I introduced a set called setUnbroadcastTxIds to the mempool. This can keep track of whether the first relay was successful for transactions submitted, either via the wallet or by RPC. It's hard to define whether the relay was successful. The way I've done so is that if one peer asks for a getdata for that transaction, then we call it sufficient. We keep track of the unbroadcasted transactions and we include them in the rebroadcast set. That gives the privacy of the timer, but it also makes sure that the transaction makes it out.

## Conclusion

I wanted to give a shout out to functional tests. A lot of my time was spent writing functional tests. But I was surprised to learn so much about bitcoin by doing that. Mocktime for example. I'd have all these failures, and I learned about sendmessages thread and getdata and transaction time intervals and just from reading the logs-- this line, this line has taught me so much about bitcoin the "combine\_logs.py" trick. Tests are never glamorous to write, but I had a lot of fun.

I would like to persist the unbroadcast set to mempool.dat so that this can survive node restarts. I'm really curious to see what the bandwidth looks like on the network and see if it looks reasonable. I also have some follow-up pull requests like test framework improvements.

## Open questions

There's a few open questions I have around this.

Are there any significant privacy implications for nodes that have varied mempool expiry settings? If a node has expiration set to not be the standard two weeks, or be set to less than that, and the wallet resubmits its transaction to the mempool and then the node rebroadcasts more quickly than expected. How much of a privacy leak is that? I find this question interesting and I haven't quite resolved yet.

There's an interplay between software upgrades and policy changes. If a node has software and then there's not consensus changes but policy changes, as in a different view of the mempool, then what can happen with rebroadcasting transactions that used to be valid but would no longer be considered for a block no longer actually mined to be removed from the mempool, is that this transaction can kind of stick around forever. This is already a viable problem because it just takes one node to rebroadcast, but having stronger rebroadcast logic means this might occur more and nodes with older software might have mempools with transactions that can't be mined, which is not what we desire.

## Thank you

I just want to say thank you to a lot of people. I've gotten a lot of feedback and support.

## References

<https://github.com/bitcoin/bitcoin/pull/16698>

