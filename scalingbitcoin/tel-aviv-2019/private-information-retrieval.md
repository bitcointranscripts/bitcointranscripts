---
title: Applying Private Information Retrieval to Lightweight Bitcoin Clients
transcript_by: Bryan Bishop
tags:
  - research
  - lightweight-client
  - privacy-enhancements
date: 2019-09-11
media: https://www.youtube.com/watch?v=YxsjdIl0034&t=8723s
---
## SPV overview

I have to thank the prior speaker. This is basically the same, except this time we're not using SGX. We're looking at bitcoin lightweight clients. You have a lite client with not much space not much computing power, can't store the bitcoin blockchain. All it knows about is the header information. We assume it has the blockheader history. In the header, we can find the merkle tree, and given the merkle tree we can make a merkle proof that a given transaction is included in a block.

The SPV client basically wants to ask this full node whether the client received some coins. We want the full bitcoin node to outsource the relevant transactions so that the client can make new transactions in order to spend those coins in new transactions.

The main criteria is privacy. We don't want to reveal which transactions we're actually interested in, and we don't want to reveal our addresses. There are many attackers that are trying to link our transactions to our real-world identities or other kinds of information in order to deanonymize the payment flows.

## Bloom filters

The traditional use of SPV wallets was to use bloom filters. So in order to protect the user's privacy, a bloom filter is a probabilistic data structure whereby we can insert elements into the bloom filter and then test the membership of a given element against the bloom filter. It works by hashing an address, then you flip the bits to 1 in the bloom filter where this hash matches. You can do this for any arbitrary amount of addresses you would like to insert into this bloomfilter. To test the membership of a particular address, you do the same and check whether the particular bits are actually flipped. Bloom filters allow for false positives. This is a customizable false positives rate. If you know the size of the bloom filter and how many elements you insert into it, you can target a certain false positive rate.

## bip37 bloom filters

bip37 bloom filters are pretty simple. We have an SPV client, it connects to a few full nodes. I think most SPV clients connect to 8 full nodes, depending on config. In this initial connection, it sends the bloom filter to the full nodes. It's an opaque obscure data structure and we hope the full node doesn't know what addresses we have. Then the full node checks transaction relevancy against a bloom filter, and if yes, it forwards the transaction back to the lite client.

The problem is that if the full node is an adversary, then the adversary would be trying to find the true address within the anonymity set of false positives. If you have a false positive rate of 0.1%, and 33 million addresses in the blockchain, then you have 33,000 false positives and you are quite anonymous. It's a probabilistic anonymity.

## Model and privacy measure

We had prior work in 2014. We have an adversary on the full node. We outsource the bloom filter to the node. We bruteforce all the addresses in the blockchain, then we get a total set of all the true positives and false positives. By knowing the groundtruth, we knew which addresses we actually had in the bloomfilter. We can measure privacy objectively by measuring those two. We repeated this by adding more addresses on the SPV client, and this may or may not create new bloom filters.

Our finding was that it was possible to find all the bitcoin addresses. If you get multiple bloom filters for the same person, like if someone restarted their liteclient, or has a lot of addresses, you can actually do an intersection attack between multiple bloomfilters. Aggregation or seed parameters don't keep track of state. If your true positives remain the same, but not your false positives, then it's trivial to outline the false positives and do an attack like that.

## Proposed solution

At the time, the proposal was to pre-generate bitcoin addresses and use a constant-sized filter. There are some benefits to this. You always know the false positive rate of this filter, and there are no intersection attacks possible, and you never outsource filters with the same fake pre-generated bitcoin addresses.

## Private information retrieval

But can we make it better?

We just saw a talk about using SGX. This is an attempt to evaluate the performance of a private information retrieval (PIR) based solution. The previous presenter said PIR is expensive in computation and communication. The basic idea of PIR is that you query a database and the server doesn't learn anything about the query. The simplest version is to download the entire database.

There's information theoretic PIR and then there's computational PIR. In ITPIR, we assume we have multiple servers like multiple full nodes. Lite clients issue queries to the subset of the servers. What we assume is that only a fraction of these are malicious. This is an underlying assumption for ITPIR to actually provide privacy. In the CPIR privacy, it's guaranted by cryptographic means.

These are the two high level proposals in the PIR research literature you can find.

## IT-PIR vs C-PIR

You have a risk of sybil attacks in IT-PIR, and you have an additional trust assumption of honest servers, but IT-PIR has the benefit that if one server is responding with the wrong entry or doesn't have the entry you're looking for, then you can still recover with the answers from the other servers. This is a notion of robust that you don't get in C-PIR. On the other hand, no risk of sybil attacks with C-PIR because there's only one server you're interacting with.

## Hybrid PIR

A hybrid of IT-PIR and C-PIR was proposed in 2014. "The best of both worlds: Combining information-tehorertic and computational PIR by communicable efficiency".

## System overview

PIR servers odwnload the blockchain, constructs PIR databases. For each database, the PIR server creates a description file called manifest file. The blockchain needs to be translated into PIR databases. Then, for each user collects all available block headers from e.g. full node peers. The user fetches the manifest files from the PIR servers to later efficiently query the PIR database. The user executes the PIR-SPV protocol, decodes the PIR responess to servers and then performs SPV validation.

We do a temporal division of the blockchain. We have all-time data, then a monthly data, and a weekly data.

## PIR protocol

The user wants to look up an address. He goes to the PIR manifest. He needs to ask the server to make a query on the address PIR database. This is a query to the first database. Given the blockheight he gets back, he can query the merkle tree database. Once he identifies some transactions that he's interested in, he can finally query the actual raw transaction PIR manifest.

The client performs interpolation search on these manifest PIR files.

## Further improvements

It doesn't seem quite practical yet. Every time the database changes, we need to recompute the PIR databases and transmit new manifest files to the clients. Interpolative search might be able to help skip manifest files. There might be a way to have a more fine granular separation of databases to clean things up.

