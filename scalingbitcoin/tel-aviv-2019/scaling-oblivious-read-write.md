---
title: 'A Tale of Two Trees: One Writes, and Other Reads, Scaling Oblivious Accesses to Large-Scale Blockchains'
transcript_by: Bryan Bishop
tags:
  - research
  - lightweight-client
  - privacy-enhancements
speakers:
  - Duc V. Le
---
## Introduction

We are trying to get optimized oblivious accesses to large-scale blockchains. This is collaborative work with our colleagues.

## Motivation

As we all know, bitfcoin data has become too large to store in resource-constrained devices. It's like 240 GB. The current solution today is bip37 + Nakamoto's idea for simplified payment verification (SPV) clients which don't run the bitcoin network rules. Resource-constrained clients (thin clients) have to rely on other potentially malicious full clients to obtain transaction information. This leads to some privacy implications. You might connect to some malicious node.

## SPV

Simplified payment verification relies on bloom filters which are probabilistic data structures that allow users to test membership of an item inserted into the bloom filter. The client makes a bloom filter and sends the filter to the full node. Then the thin client is able to request a block from the full node, for all the blocks that match the filter. It sends back the blocks to the client with the transactions.

Unfortunately, there's an attack on this approach. The adversary will be able to correctly guess the addresses belonging to the SPV client.

## Solutions

We need a full node that offers private access to the thin client. The adversary shouldn't be able to learn what the SPV client has just requested. In the crypto community, this is known as uisng a private information retrieval technique. To our understanding, most cryptographic PIR approaches are not scalable. One could use ORAM + trusted hardware to provide a generic PIR solution.

There could be trusted hardware residing on the full node that the mobile client talks with. The trusted hardware will secure the communication channel between the mobile client and the server. It uses oblivious RAM to hide data. The encrypted databank in this case is the blockchain data. I will go into detail about how ORAM works.

## Oblivious RAM

Oblivious RAM is a cryptographic primitive introduced in 1987. The idea is that you use a cryptographic primitive that hides access pattern on encrypted data of a program.

## Tree-based ORAM schemes

This is an example of path-ORAM. There's a client and a server. The server stores the data in an encrypted format. On the client side, there is... the.. the position map tells the client which block resides on which path.. for example, if he's interested in block id 4, by looking at the position map, he knows it resides on path 3 of the tree. In this example, if he wants to retrieve this block, then he will request the server to send over this path to the client. The idea is to hide the data. There must be randomization of the location of the blocks in the data tree. The client will push back the path inot the server. Because they only overlap between path 3 and path 1 is the root node, then the block of... then hopefully it's clear how ORAM works.

All the logics and data structures implemented in the client side are known as ORAM controllers. A tree-based ORAM access can be generalized as a combination of 2 operations, readpath and eviction. The idea of this project is to use ORAM to hide the access patern of the thin client on the blockchain data.

## Trusted execution environment

In this project, we used Intel SGX as a solution for our trusted execution environment. There are two properties here that we are interested in, namely remote attestation, and code isolation where we can set aside trusted memory region known as the enclave making sure no other processes can access this memory region. The idea is to implement ORAM controllers inside an enclave. Use oRAM controller to store and encrypt blockchain data in ORAM structure. The INtel SGX performs ORAM access on behalf of the remote client.

## Challenge: ORAM storage overhead

The first challenge is the ORAM storage overhead. Using ORAM incurs a constant storage blowup, 8x for path-ORAM and 4x for circuit ORAM. Storing bitcoin blockchain into ORAm tree results in 2 TB of blockchain data in a tree structure.

## Solution for storage blow-up

Securing oblivious access to the unspent transaction output set (UTXO set) is sufficient instead of blocks. So the intuition here is that the SGX  should oblivious and securely update UTXOs set, and provide thin clients with oblivious access ot tihs database.

The size of the UTXO database is around 2.8 GB. Therefore, the size of the ORAM tree is about 24 GB and for path-ORAM and  for circuit ORAM it would be about 12 GB which is accessible.

## Challenge: traditional ORAM's lack of concurrency

ORAM access is readpath and eviction operations. Eviction causes some writing on the ORAM tree. If the client sends a request during the eviction process, then the writing will block the client. It will have to wait for the ORAM access to finish. This is bad that in the bitcoin network it generates a new block every 10 minute and the new block can incur 1000 ORAM updates and this can lead to 1-2 minutes of downtime. So basically the ORAM access, writing on the ORAM tree, and if the client tries to access during this update period, then it will not be able to get that from the ORAM tree.

## Solution for concurrency

We introduce two ORAM trees. There's one that is a read-once tree and the original tree to allow non-blocking eviction. The read path performs read on the read tree, and evict performs on the original tree. Then these synchronize once every block interval. The readpath, there's no writing on the tree. We can perform readpath in parallel.

The security of this is that, in the traditional ORAM setting because there's no eviction on the readpath tree, if the client accesses the same path multiple times then ... but in the blockchain setting, an SPV client ... the SPV client should only request once during an interval of 10 minutes. The system synchronizes 2 trees every 10 minutes. The effects that you improve latency from the perspective of the thin clients. We can now perform parallel readpath on the read tree.

## Challenge: Trusted memory region is limited

The size of the trusted memory region (PRM) is limited to 96 MB. Allocating more memory is possible, but performance will suffer. Naive use of ORAM will quickly cause the PRM to run out of memory.

## Solution for limited trusted memory region

We can use a recursive ORAM construction. The idea is to store the position map into another ORAM structure in the untrusted memory region. You can store the position map as a smaller ORAM tree, encrypt it, and it will--- and now you just need to store a smaller position map for the smaller position tree.

## Challenge: Bitcoin address and ORAM ID mapping

How does the SGX know how to translate a bitcoin address into an ORAM block? Naive approach 1 is to use address and do ORAM bid, and position map will be huge. So the other approach is deterministic hashing address into ORAM block, which would mean an adversary can overflow a block.

## Solution for address-ORAM block ID mapping

In the paper, we offer a different way of mapping an address into an ORAM block. It's a different tradeoff between the storage of the ORAM trade and ORAM access. Using PRF OBlockMap to map bitcoin address into ORAM blocks... read the paper for more detail.

## Problems

Even with the mapping, there will still be some problems. This will introduce collisions: this is a standard max load analysis. One can show the ORAM block will have less than a certain number of UTXOs with overwhelming probability. Also, some addresses have more outputs than others, even though address reuse was strongly discouraged from the beginning.

## Output/address distribution

The system decider can pick how many outputs an address can have. We can cover up to 92% of all addresses. Only 8% of the addresses have more than 2 UTXOs.

## Several side-channel attacks against Intel SGX

The system we built is based on top of Oblivate and Zerotrace. Our system inherited standard secure operations from both libraries. Their implementations uses an oblivious access wrapper by using the x86 instruction cmov. From the perspective of a nattacker, this is the same as reading or modifying every byte in memory. Note that this attacker can only observe access patterns.

## Putting things together

We have an overview of the system here in this diagram. The SPV client can do remote attestation with the management enclave. There's a read enclave and an eviction enclave. The only thing that causes an update on the ORAM tree, is the bitcoin network.

## Conclusion

We have developed a system design that supports a large-scale oblivious search on UTXOs while efficiently maintaining the state of the bitcoin UTXO set.

