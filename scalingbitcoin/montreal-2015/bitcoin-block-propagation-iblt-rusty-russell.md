---
title: Bitcoin Block Propagation and IBLT
transcript_by: Bryan Bishop
speakers:
  - Rusty Russell
tags:
  - p2p
  - research
---
This is not what I do. But I was doing it anyway.

The problem is that blocks are transmitted in their entirety. If you have a 1 MB uplink and you're connecting to 8 peers, your first peer will see a 1MB block in about 66.8 seconds. And the last one will get it in 76.4 seconds, because we basically blast out blocks in parallel to our peers. Miners can solve this problem of slow block transmission by centralizing and all using the same pool.

That's not desirable, so it would be nice if we could take advantage of the redundancy in the same block. The worst case is that you create a block that nobody has seen before, but it does help for the normal case. A naieve approach is to send txid which potentially adds some roundtrip latency, so you want to avoid that.

The first approach to this was gavinandresen's O(1) block propagation using an invertible bloom lookup table. I google image searched for IBLT and that's what I got. An invertible bloom lookup table, basically what you do is you take.. you split your transactions into fragments that look like this, a fragment id, an index, and then the actual data. Those of you familiar with bloom tables will know that you take three hash functions, you throw the fragment into your bloom filter there, and then you keep a counter as well as XOR'ing in the data. Then do the same thing with the second fragment.  You do that for all the fragments, you get something like this, which is basically an oversaturated bloom table and useless to everyone.

One side does that ofr the entire block; then the peer gets the equivalent IBLT and then XOR the main parts, you subtract the counters and get the difference, and hopefully that's not oversaturated. You extract the buckets. Buckets with -1: transaction not in block, and you remove that transaction from the IBLT. If the count is 1, then there's an unknown transaction in the block, so extract that. If you end up with an empty IBLT, you then try to form a block out of that. That's IBLT in a nutshell.

There are some minor improvements and optimizations on the original proposal that have been coded up. Use siphash not SHA256 for id (v. fast). Offset index by hash of id (decode ordering). etc.

More interestingly, creating this IBLT is really fast. It's O(number of transactions in the block). There's a twist that we use to make it O(n log n). Pieter Wuille suggested why don't we just this for encoding between peers, rather than the miner setting it up.  You would use this to encode a block for each of your direct peers, potentially differently for each peer.

So the question comes down to scaling. How well does this approach scale? It scales with the differences in mempool with some factor. There's some encoding penalty (1-2.2x) for throwing these transactions into IBLT. It depends on whether they are missing. The differences in mempool scales with transaction rate. As more transactions go through, the more likely you are to have missing transactions in someone else's mempool.

The issue that comes up is that this helps against centralization in one sense, because there's less pressure on miners to collaborate into single pools because they have faster block transmission. But it does put pressure on homogenization, because this approach works best if mempools are identical, which might open the door to things like censorship.

We really wanted a tradeoff. You do need some heuristic about which transactions are going to be in the block. You can't put the entire mempool into the IBLT. So you're going to need some heuristics, but we need a compact heuristic for them to get an idea about the kinds of things they should put into their IBLT. As efficient as possible.

So this is what we came up with. You first send your minimum satoshi per byte or per kilobyte or whatever scale it is. This assumes that miners are profit-maximizing, that if they find a transaction that pays more than some rate, they will include it. And then they include transactions which are below that rate (priority line perhaps), or some that were above the threshold but I didn't include those.

Even if you have 1 million transactions in your mempool, it is still only going to cost 20 bits for each of those 1 million transactions. Those are actually pretty cheap to transmit these.

About six months ago, I hacked up bitcoind to dump mempools every time it receives a transaction and block. I ran a node in Singapore, one in Australia, two in San Francisco one of which is on the relay network. I have up on github, a bitcoin corpus of a week of mempool data for all of these nodes https://github.com/rustyrussell/bitcoin-corpus - if we used 128 byte fragment size, it seems to be the ballpark right size, instead of transmitting everything to everyone else, we send, and this is best case, this is the smallest possible IBLT and still get the data across, we would still get 3% of that. Best possible case is 15.4 MB instead of 482.3 MB.

I got lucky, and there's a streak of "stress testing" on the network, random fluctuations on the network that cause full blocks.

Canonical block ordering; IBLT doesn't encode the order. Gavin suggested that you pick an arbitrary order and you have to keep that order so that you don't have to transmit that information. We could order by fee per kilobyte, if we're picking an arbitrary order anyway. There are a couple things that we could do there. If you had a commitment to the minimal fee value and the number of transactions above or below, it would allow some fee determination for SPV. If you put in the number of transactions or blocks that are dependent, you could SPV prove that the value is correct. A commitment like that would allow a lightweight wallet to have some insight into fee levels for fee estimation reasons, which is really interesting.

There is also the idea of propagating weak blocks (near blocks). If it's 1/20th of the difficulty target, they broadcast that, so you get a series of weak blocks before you get a real block. When you send a block, you encode it by referring to a previous weak block: just encode the differences since then. If you could update and represent whole ranges since the last block, that's more likely to be workable if you had ordered by fee per byte anyway.

We can actually test this without any miner supported changes today. This is my vague plan. We cheat and we send the peer all of the information, we pretend it was in the ordder, and then we tack on the ordering information so that we fcould use it today. And then we guess the minfee. And a protocol like this would have contact with your peers, they would have some feedback about how close it was to their mempool, and you could get information about how convergent the mempools are. A recently rebooted node is going to have a very different mempool. When you receive a block, you look at how different it is; then you add an estimate on that for your IBLT sizes, if it's smaller than the block then you use IBLT, and then there's a 95% chance that they can reconstruct it. You need infinite data to be sure, but you pick 95%- and they could always fall back to a normal to getblock.



