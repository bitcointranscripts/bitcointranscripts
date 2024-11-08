---
title: Improving SPV Client Validation and Security with Fraud Proofs
transcript_by: Bryan Bishop
tags:
  - research
  - lightweight-client
speakers:
  - Mustafa Al-Bassam
date: 2018-10-06
media: https://www.youtube.com/watch?v=IMzLa9B1_3E&t=1610
---
paper: <https://arxiv.org/pdf/1809.09044.pdf>

<https://twitter.com/kanzure/status/1048446183004233731>

## Introduction

I am going to be talking about fraud proofs.  It allows lite clients to have a leve lof security of almost the level of a full node. Before I describe fraud proofs, how about we talk about motivations.

## Motivations

There's a large tradeoff between blockchain decentralization and how much on-chain throughput you can get. The more transactions you have on the chain, the more resources you need to validate the chain. If the blockchain is fast becoming big, then in theory more users will want SPV nodes or lite clients. I use the terms interchangeably. Instead of running full nodes.

The problem with SPV nodes is that they will gladly accept invalid blocks from miners. They just check the accumulated PoW rule and they do nothing to validate that the transactions in the block are valid. They make a very large assumption that the majority of the consensus is honest. This is different from how full nodes work in bitcoin. If everyone was running an SPV node instead of a full node, then malicious miners could collude together to create money out of thin air. The only thing that the 51% attack can do right now is double spend transactions; they can't insert invalid transactions at the moment. But with SPV clients only, then they would be able to do that.

How could we make it possible for these non-fully-validating nodes, these SPV nodes, to reject invalid blocks so that we don't have to trust miners? That's essentially what fraud proofs aim to do.

## Fraud proofs

This talk is based on the fraud proofs paper we released last week. This is a joint project with Vitalik and some other coauthors. The basic idea of fraud proofs is that you have a lite client and a full node and SPV nodes only download the block headers of the blockchain, they don't download transaction data except merkle proofs of certain transactions relevant to them. Full nodes download everything.

With a fraud proof system, if a full node downloads a block and detects an invalid transaction, they could in theory send a proof to that SPV node that the block has an invalid transaction and then the SPV node could verify the proof and reject that block permanently. The problem with this is what if the miner only sends the blockheaders to the SPV client but doesn't actually publish the transaction data? In that case, it would be impossible for the full node to generate a fraud proof that the transactions are invalid because they don't know what the transactions are. You can end up in a situation where SPV nodes are accepting invalid blocks because nobody can generate a fraud proof for them.

## Earlier discussions on fraud proofs

The original bitcoin whitepaper briefly mentions the concept of "alerts" or fraud proofs. The idea of "alerts" (separate from the alert system) is that nodes could send warnings to SPV nodes that some block is invalid and this would prompt the SPV client to re-download the entire block and validate the transactions. In practice, this doesn't work because a full node could tell the SPV node to download all the blocks and you would have no way to find out if it is valid or not without downloading the blocks yourself and checking. In the worst case scneario, the efficiency of running this kind of SPV node requires the same kind of resources as running a full node.

gmaxwell and petertodd have take nthis idea further by proposing "compact fraud proofs" where you wouldn't just alert lite clients about invalidity, but you would also prove that it's invalid and then you verify the proof. However, this requires a different fraud proof for each of the different ways to violate bitcoin rules. One fraud proof type for double spending, and one for block size, and so on.

We are going to simplify this down to all one fraud proofs.

gmaxwell has also discussed on IRC using erasure coding for data avialability with a scheme using "designated source" with PoW rate-limiting. His scheme relies on a designated source and rate limiting.

## Generalizing the blockchain as a state transition system

Let's talk about creating a fraud proof of the system with a single fraud proof. W eneed to generalize the blockchain as a state transition system. Every single transaction in the blockchain basically just reads or modifies the state of the blockchain. We have this state transition function. It takes the current state of the blockchain and the transaction you want to apply, and it retunrs a new state or if the transaction is invalid then it returns an error.

Our goal is to find a way to prove these invalid state transitions to lite clients. We need a way to represent efficiently the entire status of the blockchain as a merkle root in a merkle tree. We could store this as a key-value store. If we imagine this store state as a key-value store, in the case of bitcoin, all the keys would be basically UTXO ids. But all the values would be a boolean that represents if the transaction is unspent or otherwise, or if it doesn't exist or is already spent. We also need non-membership proofs so tha tyou can prove that some UTXO does not exist in the state.

## Representing the entire state as a merkle root using a sparse merkle tree

We can use a sparse merkle tree to do this, which is all the rage lately. A sprase merkle tree is a merkle tree with an insanely large number of leaves. If you want to be able to represent every possible sha256 hash as a key, then this sparse merkle tree would need 2^256 leaves. And you might be wondering how is that possible to generate that? And it turns out it's quick to generate that because the vast majority of the leaves in this tree will be basically be 0, which is the default value in the tree. Because of the vast majority of the leaves in the tree are 0, then that means the vast majority of intermediate nodes in the tree will also be zero. You don't need to recompute every node in the tree; you already know the vast majority of the leafs in the tree will be zero. Merkle proofs will be O(log(n)) like in a regular merkle tree. To access key K in the tree, you access the Hash(K)th item.

We can thus represent the entire state of the blockchain as a single merkle root, including all UTXOs. You can append this merkle root to the end of each block. A sparse mekrle tree is not the only way to represent a key-value store, you could also use a patricia tree.

Now that we have the merkle root as a state, you could imagine the blockchain as a state root transition system. Instead of transitioning the state, you transition the merkle root of the state. You redefine the transition function and create a transitionRoot function that takes stateRoot, transaction and witness as inputs to this new function. It will take in some transaction and also witnesses, and returns the new state tree of the blockchain or an error. A witness of a transaction is simply the set of the mekrle proofs for the state root of the block that basically shows you all the parts of the state that the transaction accesses or reads. Using these witnesses, you can recompute the entire state root of the tree. All you need are the merkle proofs of the parts of the state that the transaction accesses, and you can figure out the new merkle root if you only modify that part of the tree. This allows you to find out the new state of the blockchain without requiring the entire state of the blockchain.

What we can do with this is that we can do an execution trace in every block. We need to include the post-state root of the transactions in the block (every few transactions). W einclude the new state root after every single transition in the block. If you execute the transactions each, we can include the state root after every single transaction. This gives you an execution trace of the block. You don't actually have to include it after every transaction, you could also do it after every few transactions if you want to.

The fraud proof would now consist of this, the pre-state root for the transaction, the transaction itself, the state root, all of the merkle proofs for the witnesses, and the transaction itself, and a few other itesm. A full node would send a lite client all of this data and that lite client can execute this function and if it finds out that after executing this state transition function is different from the per-state root in the block, then this means the fraud proof is correct and the block can be rejected.

You don't have to include the state root after every transaction; this saves block space but the fraud proof gets bigger.

## The data availability problem

If the data isn't available, then the fraud proof can't be generated. You could use erasure coding to solve this. It's a technique that lets you take some number of pieces of data, extend it to 2x the size, doubling the data, and then if you lose some parts of the data, then you can recover the whole data from some subset number of pieces, and in fact the pieces don't need to be consecutive parts of the data. It doesn't matter the ordering of the pieces, as long as you have the right number of them.

## Naive data availability scheme

You might require a miner to commit with the merkle root of the erasure coded version of the block data. If you do that, it means that for the miner to hide any piece of the block, they have to hide half of the block. Because if they hide just one piece here, then that piece can be recovered from the rest of the pieces. However, if they hide a bit more than half of the data, then the block cannot be recovered. Using this, you can build a sampling based availability scheme. It's no longer 100% availability problem, now it's a 50% availability problem. A client can randomly sample different pieces of the block. If you assume the miner has hidden 50% of the block or slightly more because they don't want the block data to be recovered, then there's a chance that the client will land on an unavailable piece, then the block is rejected. Clients would then gossip pieces to full nodes for recovery of the data.

The problem is what happens if the miner incorrectly generates the erasure code? You have no way of recovering the data. The lite client would have to download the entire block and re-generate the erasure code to see if it's correct or not, but that's going back to square one. We want lite clients to not have to download the full block.

## Multidimensional erasure coding

Here, we're using three-dimensional erasure coding for simplicity but you could take it to higher dimensions. So if you use this, you have the original-- you have ot arrange all of the original data in the block into a square, and then you extend that data, and extend the square.... these columns and rows are extended individually using the erasure coding.  The fraud proof would be limited to a column or row. If any row or column is incorrectly generated, a fraud proof that the code is incorrectly generated is limited to that specific row or column, that's O(sqrt(blocksize)). Miner has to hide roughly 25% of the square to hide any pieces.

What is the probability of a client landing on at least one of the available piece if the miner has hidden 25% of the square (if sampling without replacement)? 60% after 3 samplings; 99% after 15 samplings. After 15 samplings, there's only a 1% chance that the miner can fool a user into thinking that a block is available when it's unavailable. On average, miners would have to do 100x more PoW in order to generate that invalid block. But you could also have a high probability if you do more samplings.

## Selective releasing of pieces

What if a miner only releases pieces as clients ask for them? Remember, the moment that a miner releases 25% of the square, then a full node can recover the whole data. A miner might want to fool as many clients as possible without releasing 25% of the square. So they might want to release just under 25% of the square. What that would mean is that the miner could always pass the sampling challenge the first couple of hundred or thousand of lite clients. The exact number of that depends on ohw many samples each client makes... the exact number of how many clients can be fooled depends on how many samples they make each (s) and how wide the square (k), and whether the miner doesn't drop the connection to many of the connecting nodes that are making these sampling requests.

## Preventing selective releasing of pieces

We can prevent this by assuming an enhanced network model. Clients send requests anonymously. The order in which requests are received by the network are uniformly random (clients sampled are interleaved). For example, using a mixnet. This would mean that a miner would have the same probability of fooling all client,s including the first ones to ask for samples. The requests are unlinkable to the clients.

## Block validity security assumptions comparison

Let's compare the scheme to the assumptions that SPV nodes and full nodes make. An SPV client assumes 51% of the hashrate is being honest. SPV clients with fraud proofs ohave to assume there's at least one honest full node in connected network graph, that the maximum network delay to receive proofs (e.g. 5 minutes), and a minimum number of lite clients (few hundreds).

## Conclusions

It's quite efficient in the space, a state fraud proof would be quite small. Our computations are also efficient, taking a few milliseconds. The link to the full paper is here. I'll take questions now, thank you.

<https://github.com/musalbas/smt>
