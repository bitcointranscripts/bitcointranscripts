---
title: Secure Fountain Architecture
transcript_by: Bryan Bishop
tags:
  - security
speakers:
  - Swanand Kadhe
---
A secure fountain architecture for slashing storage costs in blockchains

Swanand Kadhe (UC Berkeley)

<https://twitter.com/kanzure/status/1172158545577594880>

paper: <https://arxiv.org/abs/1906.12140>

# Introduction

I know this is the last formal talk of the day so thank you so much for being here. This is joint work with my collaborators.

# Is storage really an issue for bitcoin?

Bitcoin's blockchain size is only 238 GB. So why is storage important? But blockchain size is a growing problem. It's always going to go up. If you do some back of the envelope calculations, then the growth rate is roughly 1 block per 10 minutes so roughly 1 MB per 10 minutes. This is about 52,560 MB/year at full blocks.  This is about 144 MB/day. So then the user has to figure out, do I upload this to the cloud? Do I trust the cloud?

# Scaling bitcoin

How can we reduce the storage costs for nodes without reducing the security properties of bitcoin and blockchain in general? We need to take a deeper look into the bitcoin ecosystem. There are archival nodes, lite nodes and pruned nodes.

The archival full nodes are the most secure way to join bitcoin. They download the entire history and validate all of the history and they store the entire blockchain. If you are an archival full node, then you also help bootstrapping the new nodes by giving them the history.

The other extreme are the thin light clients. These nodes are the SPV clients and you can think of them as the most economical way to join the bitcoin system, by ignoring some of the bitcoin rules. They only download the blockheaders. But the issue is that you need to rely on full nodes, since you don't validate any transactions. So there are security and privacy issues.

In between, there are pruned nodes. This is a third type of node. The pruned nodes are essentially bitcoin's solution to storage bloat. The pruned node starts as a full node, but then deletes the history and only stores the UTXO set and the last few blocks. Individually they are almost as secure as full nodes. This has a fixed storage overhead, which is great.

The concern with pruned nodes is how do they interact with network health. If you are an archival full node, you are helping the new nodes to bootstrap because they can download the history and you're also preserving the history. What if every user tomorrow runs a pruned node or SPV client? Well, then we lose the history and it's not possible for a new node to join the system.

We want to come up with ways where we can store the history in a more decentralized way where each node has low storage costs but we're not giving up on any decentralization or security property.

# Challenges

The first challenge is security. There might be some malicious nodes that are adversarial. The second challenge is decentralization, where full nodes must perform their computations without relying on others. The other one is low computation cost, and also the next one is low bootstrap cost. The number of nodes that the new node is contacting should be small.

# Tradeoff

There is a fundamental tradeoff between storage savings vs bootstrapping cost. As you reduce the storage requirements on each node, you increase the amount of work that each new node needs to pay in bootstrapping. We want to devise a scheme that has a very small bootstrapping cost.

# Decentralization via random sampling

When the blockchain grows by k blocks, randomly store s blocks out of k. Keep doing this as time goes on. Suppose for every 10,000 blocks I am only storing 10 blocks, so this is 1000 fold savings. This is good because the storage costs have gone down. In fact, this is used in sharding for ripple. But the problem is that this has prohibitive bootstrapping cost for new nodes. You have to communicate with a large number of nodes to find the last block.

# Erasure coding: Random linear codes

One proposal last year was to use random linear codes. Split every block into k fragments, and compute s coded fragments using random linear coding. This is a well known technique in data backup and archival. See Perard et al 2018, Dai et al 2018. The main issue here is that it's not possible to detect the malicious nodes. Also, recovering the block involves matrix inversion which requires O(k^2) computation. This has a small bootstrap cost, though.

# Erasure coding: Reed-Solomon codes

Here, what changes is how we are taking the linear combinations. Now we are doing it in a specific way, dictated by a Reed-Solomon code. Indeed, there is manageable bootstrap cost, and good storage savings of k/s. Reed-Solomon codes are error-correcting codes, and malicious coded fragments can be corrected which is great.

Unfortunately, the finite field size should grow with the size of the network, which gives this a prohibitive computation cost.

See Raman-Varshney 2018, Li et al 2018 (polyshard).

# SeF: A secure fountain architecture using fountain codes

We are essentially using secure fountain codes to distribute the blockchain history between multiple nodes. We envision that storage-constrained nodes are called droplet nodes here. They only store a small amount of data. When a new node joins the system, it contacts some subset of droplets and downloads the data. You should be able to retrieve the blockchain in the presence of malicious users. Once you retrieve the blockchain, you can act as a full node, but you also encode it and turn yourself into a new droplet. Droplet nodes will slowly replace full archival nodes.

# SeF encoding

In the current epoch (the time required for the blockchain to grow by k blocks), when the blockchain grows by k blocks, encode the k blocks into s droplets using a fountain code. The storage savings are k/s, so if k=1000 and s=10, then you have 1000x savings.

# Fountain codes

In fountain codes, they take a set of packets and encode them into potentially infinite number of droplets. It goes to the bucket and the decoder is able to recover blocks from all the droplets. That's the high level idea.

# Luby-transform (LT) codes

One of the first and well-known fountain codes is luby-transform codes. Basically blocks get XORed together.

# Peeling decoding

Collect an arbitrary subset of droplets of sufficient size. Peeling decoder recovers original source symbols.

Luby 2002 designed a robust soliton degree distribution that guarantees successful recovery.

# SeF: Luby-transform (LT) encoder

In SeF, we are going to use the luby-transform (LT) encoder as-is. So we use a robust Soliton degree distribution proposed by Luby. Once you decide how many blocks you are going to xor, you randomly choose 3 blocks, and you ... then you store that. You also store the header data from the blockchain.

An important property of fountain codes is that they are rateless codes, meaning it's possible to keep constructing droplets without knowing what any other node is doing. This is important for scalability because every node can now create its own droplets without knowing anything about the rest of the network. This helps with decentralization and also scalability of the system.

# SeF peeling decoder

For retrieving the blockchain history, we want to decode the blockchain. We can't use the peeling decoder as-is, because of malicious block providers. They might be giving you some garbage, which gets used in the decoding, and then there's error propagation and it ends up happening that you decode entirely garbage. So we need to deal with it.

We're going to leverage the hashchain structure and merkle roots to cleverly deal with the malicious nodes.

Fountain codes were originally designed for a different task. Here, we're using them for blockchain. Our first step in decoding is to obtain the longest valid header chain. We're acting as an SPV client or lite client. I can verify that this is the correct chain because of the PoW difficulty. Once we have the right chain, I am going to download some droplets from droplet nodes. Then we can create this graph where we can see each droplet is a XOR of some of this other data. Out of these droplet nodes, some of them are going to be malicious meaning that this droplet was claimed to be a XOR of block 3 and 6 but it can actually be some arbitrary data. But we don't know that; once you XOR the blocks, you lose all the semantic information. For a new node, you don't know which are malicious blocks and which are legitimate blocks. So we need to actually detect that.

To do that, we're going to essentially use the header chain as side information to detect bad blocks. So we start in the standard way of the peeling decode,r then we need to pick a singleton block that is not XORed with anything, and let's compare its header with the header in the headerchain. If the headers match, then we take the payload of this block which is supposed to be transactions, and then compute the merkle root and see if the merkle root matches the one stored in the headerchain. If both of them match, then we're going to accept that block. But if they don't match, then it must be a malicious block and we're essentially going to delete it.n

Malicious droplets are detected only when they become a singleton. Peeling is crucial in detecting malicious droplets.

# Threat model

The threat model is that some arbitrary set of nodes are adversarial and are giving you garbage data. We're assuming that there are at least a certain number of honest nodes, and the adversary is oblivious and cannot observe storage contents of the network and then choose to who to attack. In this model, we can show that if a malicious droplet becomes a singleton, it is rejected. OBlivious adversary cannot influence probability of decoding failure for honest droplets.

# Comparison with existing solutions

....

# Numerical results

....

# Tackling block size variability

One thing we can do is adaptive zeor-padding, while computing bit-wise XOR, a node zero-pads the blocks to the largest block among the d blocks.

Block concatenation is a natural way to reduce variance in block size, to first concatenate blocks to form superblocks and then XOR superblocks and that encoding. Then ew can have the blocks almost equal size and we can save a lot.

# Experimental results

...

# Conclusion

We presented a secure fountain code architecture for reducing blockchain storage costs by orders of magnitude without compromising security of the network. This can be directly applied on top of bitcoin, without requiring a soft-fork or hard-fork.

# Future work

* How to dynamically change epoch length k?

* How to reduce decoding complexity to be linear in k?
