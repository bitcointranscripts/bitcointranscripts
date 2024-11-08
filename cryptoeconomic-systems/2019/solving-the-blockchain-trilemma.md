---
title: Solving The Blockchain Trilemma
transcript_by: Bryan Bishop
speakers:
  - Sreeram Kannan
  - David Tse
  - Pramod Viswanath
---
-- Disclaimer --
1.  These are unpaid transcriptions, performed in real-time and in-person during the actual source presentation. Due to personal time constraints they are usually not reviewed against the source material once published. Errors are possible. If the original author/speaker or anyone else finds errors of substance, please email me at kanzure@gmail.com for corrections.

2.  I sometimes add annotations to the transcription text. These will always be denoted by a standard editor's note in parenthesis brackets ((like this)), or in a numbered footnote. I welcome feedback and discussion of these as well.
--/Disclaimer --

Solving the blockchain trilemma

Sreeram Kannan, David Tse, Pramod Viswanath

We want to solve the blockchain trilemma. This is the result of collaboration over the last year between the three of us and many more people.

# Blockchain trilemma

What is the blockchain trilemma? Why should we be interested? Trust is a basic primitive in our society.

Platforms that deliver trust on scale, essentially run the modern economy. Youtube, Apple iTunes, Amazon, they are all marketplaces that provide centralized trust at scale. The main friction with these platforms is that they are  centralized. The three points of the triangle are trust, scale and democratization.

If you look at the edge between democratization and scale, this is in fact not new-- there are services like bittorrent which accounts for a large volume of internet traffic. But due to the inability to figure out incentives, they were replaced by other centralized services.

If you look at the other edge here, it's services that provide democratization and trust like bitcoin and ethereum. It's a breakthrough in decentralized trust, but they are not scalable.

# The promise

There are many potential applications that can actually be run on a decentralized trustless platform. This could include payments, exchanges, gaming, social networks, internet of things, or prediction markets. Our core blockchain infrastructure is unable to support the scale required for every potential transaction conceivable. There are some projects trying to close that gap, and there's still a huge amount of progress required.

# The blockchain trilemma

This lets us phrase the key topic of this session, which is the blockchain trilemma which was popularized by Vitalik Buterin of ethereum. The three axis are decentralization, security and scalability. The trilemma asserts that it's impossible to get all three at the same time. No platform can be decentralized, secure and scalable. And indeed, this is one----  this comes from the experience of trying to build these platforms. Bitcoin and ethereum are decentralized and secure but not scalable. Then there are others like EOS, Tron and Ripple that are secure and scalable but not decentralized. Is there a way to get all 3 at the same time?

# The three axes in detail

What do each of these axes really mean? Unless we define it, we cannot achieve it.

Decentralization means that any read-write access to the blockchain is controlled by some distributed mechanism like the amount of compute power you have or the amount of stake you have, like proof-of-work or proof-of-stake.

Security means that you should be able to defend against adversaries that are adaptive to the public state. To be sure that you can comply with adaptive adversaries and incentive compatible.

What does scalability mean? There are two aspects of scalability. You want bandwidth efficiency, and if you provide more bandwidth then your throughput should go up. So this has vertical scaling: the throughput scales with the amount of resources per node scaling. There's another type of scaling, which is horizontal scaling which is where as we get more and more nodes in the network then the performance should improve with a fixed set of resources per node, so that's horizontal scaling and computational efficiency. Each node can process 1000 transactions/second, but you have thousands of these nodes, so you should be able to process millions of transactions.

The main question is, can we get all of these efficiencies, while preserving the other properties? Scaling, decentralization and security. So that's the main goal.

# The blockchain trilemma is solved

Our main claim is that we have an algorithm or protocol that achieves all these three properties called Trifecta. You can have a new platform which is decentralized, secure and achieves very high throughput. For example, in our implementations, we are already able to have 250,000 transactions/second. I'll let David Tse talk about vertical scaling.

# Prism: Vertical scaling to physical limits

<https://diyhpl.us/wiki/transcripts/scalingbitcoin/tel-aviv-2019/prism/>

When we started to think about this, we focused on vertical scaling which is where you have a fixed number of nodes and you want to scale your performance up to the physical resource limits imposed by the network. It turns out that our solution to this problem gives a very strong hint on how to do horizontal scaling as well. I'll spend some time talking about the vertical scaling solution, and then explain how this can be extended to achieve horizontal scaling. This protocol that was invented to solve vertical scaling is called Prism and it will appear in the November London security ACM conference.

# Physical limits

First let's talk about physical limits. There's two types of physical limits. One is that you have a distributed network, and this network is connected together by pipes that have bandwidth limits and capacity limits. That's one example of a limit. So there's a network capacity. On the other hand, there's another limit, which is how long does information take to propagate through the netowrk mostly through multiple hops. There's a speed of light propagation delay. These two numbers impose a certain limit.

When we started this research, we thought that any protocol can have a point in this two-dimensional figure: transaction throughput on the x-axis and confirmation latency on the y-axis. The network capacity imposes a limit on how much transaction throughput you can get, which limits how much you can push through. Transactions need to be exchanged between nodes. On the other hand, propagation delay places a lower bound on how much latency you can get.

One question we had was, is there a way to find a protocol that goes from where bitcoin sits, as close to the point where transaction throughput and speed of light propagation delay are at their limits. I claim that we have found one. Knowing that, we claim that the protocol we found is a very natural generalization of Nakamoto longest-chain protocol which was the first blockchain protocol.

# Longest chain rule

Our protocol is a generalization of longest-chain. Let me explain how this works. Blocks are generated by miners and they get appended to the longest chain. The blocks play two roles: each block contains transactions, and two, and this is subtle, is that blocks actually vote for each other. As blocks get deeper in the chain, after a while they get confirmed. You're waiting for blocks to get confirmed. Each block appended is implicitly voting for the blocks coming before it or whatever it references. The probability of reversal goes down as the longer you have to wait. So here we can see latency and throughput is controlled by one parameter, which is the rate at which blocks are mined.

A very natural solution to improve throughput and the latency is simply to increase the mining rate, so that you can get confirmations faster and your throughput is also higher. But as we all know, when we do that, then forking occurs. And forking is a problem because forking decreases the effective amount of work you accumulate on the longest chain, and makes you vulnerable to attack. The more forking you get, the lower your security is.

So the punch line is, to summarize this diagram, is that forking reduces security. This picture is an example of why the blockchain trilemma is difficult. As we try to scale the throughput for example, we give up on the security. So in this picture, there seems to some potentially fundamental tradeoff between security and scalability which might be one reason why the trilemma is difficult to solve.

We discovered that this tradeoff is not fundamental, but specific to the longest-chain protocol. So we changed the protocol so that this tradeoff disappears. We started with the longest chain again, and then what we realized is that actually these blocks in the longest-chain protocol are doing two different things: they are carrying transactions and they are confirming previous blocks. Our goal is to decouple these two important roles from the longest chain so that we can independently scale the two different mechanisms.

Let me start by trying to figure out how to reduce my latency. Our way of doing it is the following. Instead of having one type of block, we have two types of blocks. We have green blocks and blue blocks in this diagram. The blue block is organized into many chains, like in our implementation 1000 chains. All the clients maintain the entire structure. These chains are the ones that vote for the green blocks, which at this moment, carries the transactions. So transactions are in the green blocks. Blue blocks are voting. Because there's so many chains, the voting rate is much faster than before, about 1000 times faster. So therefore you can confirm transactions faster. That's the intuition.

This allows us to speed up the latency much faster than bitcoin. But as you can see, the throughput is still low because we need to maintain a nice green structure os that the mining rate on the green structure is still very low. In the blue structure, each chain has a low mining rate. The transaction rate is still low in this example-- so we applied the decoupling principle one more time.

So we have a third type of block, called transaction blocks. These blocks focus on carrying transactions. The green blocks no longer carry transactions. Their only goal is to win the lottery. When they win the lottery, then they refer to a bunch of transaction blocks. When a green block is mined, they include the hashes of a bunch of transaction blocks they see. When they win the lottery, their transaction blocks will be carried into the ledger. So now we can see that we can scale up the transaction throughput without compromising on the security of the data structure.

The main point of this picture is the following: security is maintained by the right-hand side. Scalability is achieved on the left-hand side. Why? Because on the left-hand side, now I can start generating many many transaction blocks until I have saturated my physical limits. So that's how we achieved vertical scalability and security. So we have broken the longest-chain tradeoff between security and stability by having a data structure that decouples the two.

# Security theorems

This is a very nice picture. After 70 pages of calculation, we converted them into security theorems. We find that most of these security papers are at least 60-70 pages so we thought we would need comparable length for credibility. The first theorem is that Prism is secure and we haven't compromised security. So for adversary power less than 50%, Prism is secure. However, our throughput is much higher. Our throughput can scale--- it's the network throughput limit times the amount of honest power in the network. An adversary can still do DDoS. Third, our latency we can achieve is the following-- it's of the order of D (the propagation delay, the lowest you can get) plus a term which depends on the probability guarantee of 1/epsilon which is a typical security parameter in these theorems, divided by m which is the number of voter chains. So in the picture I had, there was 10 voting chains, the implementation is 1000 voting chains, and you can choose a large value for m. Each of these voting blocks is small; they only contain a hash and a pointer to a proposal. So it's very small. Basically what you can do is make m very large so that the latency is very insensitive to epsilon.

# Reliable confirmation via unreliable votes

The rough comparison is that, we have achieved reliable confirmation via unreliable votes. On the left hand side is the longest chain protocol where you have to wait for many votes so that an adversary cannot propose an adversarial block that has as many votes as you do. But here, we don't have to wait as long, because we have many many voter trees. As long as they 2 deep, then it's very hard for you to change many votes because to change votes, you fork many of these trees and even though each one is unreliable and it's easy to fork off, to fork off 500 of them is very hard. If the reversal probability is 0.35 for each change, to reverse 500 chains is extremely difficult compared to the problem of reversing just one chain.

# Rust implementation

As I mentioned, we implemented this. Here are some results. We used 4-regular topology of 100 EC2 c5d.4xlarge instances, 120ms delay, 400 Mbps bandwidth per link. This is up on the arxiv paper, <https://arxiv.org/abs/1810.08092> and see this diagram.

# Horizontal scaling

So we talked about vertical scaling: for a given node, fixed number of nodes, you increase scaling by having more resources on each node. The second part of scaling is horizontal scaling. My name is Pramod Viswanath and I am a colleague of Andrew Miller and part of this collaboration. So if I go back to these axes, we're focusing on scaling on horizontal scaling which is where we fix each node's capabilities. The resources per nodes is kept constant, but the number of nodes is increasing. We would like the performance improvement to improve as you add more nodes. If you double the number of nodes, you would like to have double the throughput and that's linear horizontal scaling of course.

In blockchain, this is usually called sharding. What this means is that if you have more nodes, your performance just increases. The resources are computation efficiency, storage efficiency, and communication efficiency. These resources are kept constant.

Why is sharding hard? The key phrase is how blockchains are designed, which is this notion of full replication. All nodes in the system maintain the entire state of the blockchain and participate in validating the state. All the nodes maintain state and validate all state updates. If you have more nodes, then that doesn't change because they are all doing the same work. What improves is security. If you double the number of nodes, your security increases. But throughput didn't change, so you're not scaling in that sense.

One way to do this is that if you double the number of nodes, you could say half the nodes should maintain one part of the ledger and the other half should maintain another part of the ledger. This scales, in a way, because now you have half the number of nodes.

The key question is, can you scale the throughput while also increasing the security? Arguably, if you double the number of nodes, you want to double the throughput and double the security.

# Sharding: randomized node allocations

One way to do sharding is randomized node allocations where there is an outside-the-blockchain algorithm or sometimes inside, that allocates nodes to two different shards in this example the left and the right or purple and blue. Each node only maintains their part of the ledger. Once in a while, this rotates and you re-allocate nodes to shards and redo this. There's always a tradeoff between how often you do this, because every time you reset you have to bootstrap and do some work to catch up. This is considered a solution because now at least you would think you could maintain half the storage but at the same time ... security.. but there's some problems here.

The first problem is that there has to be a way in which you allocate a node to a shard. So you need to identify the node. So you need an identity associated with the node in order to allocate it. This is different from blockchains where you don't need a continuous identity in order to participate in the network.

Another aspect is that it's true that you're randomly shuffling and re-allocating nodes, and that might protect against adaptive adversaries where they come in and they stay that way. But you can think about a more powerful adversary, an adaptive adversary, where maybe they are adversarial but at some point they might go and-- after they have been assigned to the nodes. One way to think about it is that you know which node you have been allocated to, ... there could be collusion among the nodes in the shard to corrupt that part of the ledger. This is another vulnerability. Even if you are shuffling the nodes, it's still vulnerable because after allocating you can still pick up the nodes. So it is insecure against adaptive adversaries. Shuffling is not okay if the adversary can attack.

Even if you allocate just randomly, the fact is that if you want to have many shards then you only have a few nodes per shard and it wont be proportional. So if you have 10 shard nodes, it's not like an adversary maintains the same number of nodes in every shard simply because the numbers are smaller. So if you want to maintain the proportion, then you should really have a limited number of shards. So the third problem is that you really need to have large shard sizes to have proportional representation of diversity.

This is the core of the trilemma, which is that your efficiency decreases inversely while security--- security decreases inversely with the number of shards, and efficiency increases linearly. So how do you solve this if you want both throughput and security while keeping track of resources or being efficinet in storage, compute and communication?

# Efficient computational/validation scaling

The key is to maintain efficiency on all of them. Let's try to say that, there's three things- storage, compute and communication. Computation and storage are separate. Let's say that everybody in the chain maintains the ledger; so it's not scaling. From the storage perspective, there's the same amount of replication. I would like everyone to be able to validate. A block comes in, and it's not yet validated, and anyone who gets the blue node, can ask a random fraction of the network to ask the network to validate if that new block is fine. Everybody has the ledger, everyone has the full state of the network, so they can do the validation for you. If you ask enough people, and there should be-- and your network shouldn't be under an eclipse attack-- but this is our way of scaling compute without having everyone to validate. Only the nodes that are asked, validate and send it back.

# Storage: polyshard

If different groups have their own shard, how do you ensure that the adversary I would like to be able to scale security? Even if the adversary is specifically focusing on one of the shards, that shard is still secure. The only way is if that information in that shard is also contained somewhere else. The idea of a shard means that you have divided it atomically. But the way to think about it is to have pieces of the data spread everywhere. You use something like a fountain code and mix it up. It might not seem obvious how this might work. Even if a fraction of a shard has been taken over by the adversary, the data is still there in some coded way in other parts. It's not immediately obvious how to do validation, but we have a protocol called polyshard which allows storage and security to scale, but only for some limited notions of what functions you can validate. You would like to be able to validate and ... in a distributed way, so you can evaluate low degree polynomials of functions which are-- if you have the goal of -- something like a turing complete computation, then this is not the kind of approach you would like to take.

# Computation and storage efficiency

There's clean ways to do computation: everyone has the state, so they can validate randomly. If you want to store efficiently, it's not immediately obvious, but we've worked on that. But what about doing both of them at the same time? We've talked about the trilemma.

Trifecta principle 1: Self allocation. I don't want to be able to have an outsider agent to do this node allocation. I want nodes to be able to self-allocate which shard they pick and just stay there. This will allow you to avoid the identity problem I mentioned earlier. You maintain only your part of the ledger.

Trifecta principle 2: No separate chains. To scale security, there needs to be commonality. The commonality here with respect to the talk that David just gave, are the proposal blocks and the voting chains. That's where the security was coming from, they are relatively lightweight and just pointers and hashes. All of these blocks link back, the security is driven by the core central chain or in the context of Prism it's the proposal blocks and the associated order blocks.

The issue there though is how does compute or validation work at any one of these shards? If every node needs to validate, then they need to know the state of the network. Each shard has its own part though. So it's not really feasible. So we take the principle one step further where what we agree on is not that the stack of transactions is valid and no double spending, instead we agree on an ordered list of transactions instead. All the nodes agree on an ordered list.

A shard can be entirely---- but it is still secure. They are all driving from this common aspect which is a proposal in the voting chains. Also, besides consistency, there is liveness: Trifecta is live when there is at least 1 honest miner in a shard. Consistency is: Trifecta is consitsent evne when there is ....

We say that the Trifecta computation is efficient and so is the storage. They only maintain their own shards, and they only agree on an ordered list of transactions.

# Communication-efficient scaling

If every nodes does not even receive the block, is it possible to secure that block? How is it possible to secure what I'm hearing if I don't hear what is happening in the rest of the world? If a tree falls in a forest and nobody is around to hear it, does it make a sound? We don't really solve the entire trilemma.

# Coded merkle tree

Sreeram Kannan

A coded merkle tree solves communication efficiency. So we just heard how horizontal scaling works in terms of computation efficiency and storage efficiency. Here we will look at communication efficiency.

# Communication scaling in sharding

Different nodes belong in different shards. Suppose there was a new block in the blue shard in this diagram. Now the rest of the nodes need to be convinced that the data is available, that the blue shard is available to at least one honest node. In the sharding scheme, we were writing in hashes of the block. So suppose that you write in a hash of a blue block into the core chain, and the data is not available. Nobody has the blue block. Then, the whole protocol stops. You cannot execute the shard beyond that particular position. So it's very important to understand communication efficiency. In particular, data availability. How do you convince in a given shard, I have a block, and I want to convince other nodes that the block is available.

Availability is different from invalidity. Let's say a transaction is invalid. It's not temporally fluctuating, but availability is temporally fluctuating. If you pin him down and say there's no block, the adversary might release the block later.

So we're going to make a mapping in constructing a blockchain like in bitcoin, there's a notion of a full node and a lite node. What we're going to think of is, think of the blue shard nodes, as full nodes, and think of the remaining shard nodes (out-of-shard nodes) as the lite nodes. The light nodes want to be sure that the block is available to at least one honest full node in the respective shard.

So we have a full node and a lite node, and the lite node doesn't store the block but it only stores the headers of the blocks in the other shards. The data availability problem is that when you receive a header, you want to make sure that at least one honest node has this block.

The notion of at least one honest node having a block seems tricky. How do you know that a node is honest or not? This is where you assume that at least one full node you're connected to is honest. You might be connected to 20 nodes, and at least one is honest. You're not assuming a majority is honest, but only that at least one is honest.

How are you going to convince yourself that the block is available? The most obvious solution is to download the block. But this is communication inefficient. If every node in every shard needs to download every block from all the other shards, then communication is inefficient.

One idea is to randomly sample blocks. Think of a block as being made of many distinct chunks like they could be transactions but they could be partitioned into symbols. So you randomly sample some fraction of these chunks.  If you get the chunks you were looking for, then you believe the block is available. But the adversary could hide one chunk out of n chunks, and n might be 1 million, and you have to sample a lot to really expose the adversary. So it doesn't work. If only one symbol is hidden, it takes a lot of sampling to expose that.

How do we get around this?

This idea is to use erasure codes. Can we use fountain codes or erasure codes. What do codes do? They try to correct for errors and erasures for missing symbols. Can we try to use coding theory to compensate for this problem? Here's the main idea. You take the symbols in the block and then you somehow encode them to form an error correction code. So in this example, the chunks are now m1, m2, m3, and also m1+m2 and m1+m3 and so on. So now what you do is, the lite node samples coded chunks from the block. Constant number of samples is sufficient. What happens when you sample coded chunks is, if the adversary hid less than half the block, if the adversary hid less than half the block, then the remaining half of the block is sufficient to decode the other half of the block. That's the main property of an error correcting code. If some chunks are missing, you can still reconstruct the whole block.

Rather than checking that an honest node has the entire block, we can check that the honest node has half the block. If you have half the block, you can use the error construction strategy to reconstruct the other half of the block. So now an adversary cannot hide one symbol because if you hid one symbol then you can reconstruct it from the other error correction data.

So we started with a data availability problem. We have to assert that at least 1 honest node has 1/2 the block. If the node has hidden more than half the block, then you would easily find that. You know at least one node has half the block, which means one node can decode the full block. So at least one node has the entire block.

But there's one issue with this.

The node making the block, which is in our case a blue shard node, making the block-- may not fully comply to your required erasure code. For example, here, what it has done here is taken m1 and instead of m1 replace it by m1 prime when it created the merkle root or header. When it created the commitment, it used inconsistent symbols which don't apply to the erasure code. This is called incorrect encoding. A node with incorrect erasure coding can potentially bypass our detection mechanism.

To deal with this, we have a coding-fraud proof mechanism. A full node which has now decoded half the block tries to construct the rest of the block, but detects that if you try to reconstruct it, it doesn't add up to the merkle root that was committed by the node. This becomes a fraud proof that the full node can prove to other nodes.

By randomly sampling a few chunks, we immediately know that at least one node has half the block. So either that node can decode the entire block, or it can prove to you that the block was incorrectly erasure coded based on the merkle tree root commitment. This fraud proof is unchanging with respect to time.

Our main idea of communication scaling is to use erasure codes to reduce the data availability problem into a coding problem.

# Our contributions

The main claim is that we have a new algorithm for erasure coding-- it's not just a regular erasure code, it's a new algorithm called a Coded Merkle Tree. A merkle tree is a mechanism to commit to a bunch of data, but a coded merkle tree is very similar to a merkle tree in that it has hierarchy but it has erasure encoding embedded in the various layers. With a coded merkle tree, we can achieve not only the few bits that you download, but also if you look at the third column here it's called the coding-fraud proof size. The size of the proof to prove fraud is actually small compared to other codes. There was another code constructed by Vitalik Buterin and others called "Fraud and data availability proofs" paper in 2018.

I am not going to explain the construction of our erasure code, but I do want to point out that the coded merkle tree looks like a merkle tree but at each level there is coding and interleaving in order to construct...




