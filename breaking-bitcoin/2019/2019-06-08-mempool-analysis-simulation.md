---
title: Mempool Analysis & Simulation
transcript_by: Bryan Bishop
speakers:
  - Kalle Alm
tags:
  - transaction-relay-policy
  - developer-tools
date: 2019-06-08
media: https://www.youtube.com/watch?v=Mznn1uVyTUQ
---
<https://twitter.com/kanzure/status/1137342023063744512>

slides: <https://breaking-bitcoin.com/docs/slides/2019/mempoolAnalysis.pdf>

## Introduction

Fun fact: I don't think anyone knows this fact, but antpool is a miner and antpool is not mining replace-by-fee transactions. What I mean by that is that if you do a replace-by-fee transaction, they will ignore the second high fee transaction. There are cases where transactions are RBF-bumped to increase the fee to make it mined faster, so you RBF bump it, and then you have people spending the unconfirmed RBF version and then have a chain of transactions but then the original transaction is mined and not the other chained transactions. So that's interesting.

I am going to talk about simulating the mempool and how that is useful and also analysis techniques.

## Agenda

It's very simple: I am going to start with why, then what, and how I did that, and then so what.

## Why mempool analysis

Back a few years ago, I was doing a presentation on scaling stuff where I was saying we could use the mempool to get better estimation of fee rates. After I went off to implement that, I realized that wait I don't actually have a good way to compare parameters to figure out what is the optimal way to do this. You don't want to have something where you have a transaction that never gets confirmed and you have to keep RBF bumping it... we want some kind of analysis for fee estimation reasons. Originally I had patched Bitcoin Core to in real-time look at the mempool. To get one day worth of data, you would have to wait one day which was not very fast.

Another thing is that right now we're losing data. We only know when a transaction was mined, not when it appeared. We don't know much about transactions that were invalidated, when a second transaction replaces the first one there's often no way to find the original transaction. I wanted a way to record the mempool and be able to play back that recording and to be able to do various analysis on that.

## Why record and playback the mempool?

Ther's a loss of information like timestamps, blocks and transactions. There's no good answer to "what happened at time x". We don't know, was the mempool full? How many transactions were circulating at that time? If a transaction wasn't mined, then when did it get out of the mempool? When the mempool gets full, it starts pushing transactions out. This could be useful for fee estimation as well, but there's no recordings of that. Having a tool to help store mempool data would help us see what information we can get out of that. Also questions like is it spam or not spam? What portions of transactions are mined by miners? Without this tool, we don't know that. We could make statements about which transactions we knew about or didn't know about, and which ones miners introduced before we knew them.

There's a tool called MFF that helps do this.

## A new tool for mempool analysis

Mempool File Format helps logs time of re-entry, exit, confirmation and invalidation. You can always get transaction data out of the log. When the block is mined, it stores the block. When a block is unmined, the tool points this out and says it was no longer there. You can seek through this log file on a block by block basis or by blockheight. If you want to find transaction X that is an O(n) operation and it's not very optimal. This is a very specific kind of format, which solves a specific task and it's very bad in most other cases.

There's a library implementation of this as well called libbcq, which was built on top of a database format called CDBQ.

Light clients download blocks and store nothing. You have pruned full nodes which download all blocks and recent transactions, and keep recent confirmed blocks and unconfirmed transactions. Full nodes store all confirmed blocks and unconfirmed transactions. With MFF enabled, all blocks and recent transactions are downloaded, and all blocks, unconfirmed + invalidated transactions are preserved while also retaining the order in which they appeared. Note that in pruned nodes and full nodes, we lose information about unconfirmed transactions that disappear or never get into the blockchain.

## MFF so far

I have a bunch of zeromq dumps. It stores it to a big text file. I have a tiny mempool example and a bigger mempool. Creating these from zeromq dumps takes a long time. In my bigger mempool zeromq dump, it takes about 15 MB/day to store all of this data including all the blocks and all the transactions. There's about 31.8 million entries, and 55,101 invalidated transactions.

It's Bitcoin Core with MFF enabled. If we ever hit another mempool explosion, we will be able to see much better how did things behave and how can we do things to alleviate those problems whether from Bitcoin Core or other wallets. If you have a smaller mempool, you get more data, and that's simply because it has to start throwing things out.

## CQDB

CQDB is a funny way of saying "sequential database". It's a database, it's a seekable sequential database, both a library and spec. Then there's BCQ which is bitcoin CQ (specialization of CQ for bitcoin). There's also a Bitcoin Core patch and hopefully more in the future.

CQDB is a light-weight, space and memory efficient sequential database. It's append-only. It is restricted to chronological order. A tricky thing here is that when you store this data, it's just written once and then it's never changed again. In order to keep some kind of reference to the inside of a cluster like where is block X you have to have a header and the header is written into the next cluster here. Clusters are stored as blocks of header+data pairs.

You serialize objects once, then use references to point back at their byte position. The reader does not have to have any data in memory. If you only have room for ten transactions, then you could throw everything else out and keep 10. When you want to learn about another transaction beyond those 10, you can go back and read the data by looking at the reference for where to seek to.

## BCQ

BCQ is a CQDB where each segment corresponds to a block in the blockchain. Objects in this case are transactions. Say you write a transaction into cluster 3, starting at byte position 10000. You write that in. Later when you want to reference it, like in block 30000, then you say yeah transaction 10000 written as a varint it's actually not a varint.. then if you don't know this transaction then you can take the bytes and seek back 20000 bytes and go to the transaction and deserialize the transaction there. It also writes the segment input information into the header so you can seek to that segment if you wanted to.

<https://github.com/kallewoof/bitcoin/tree/libbcq>

## btc.com output splitting transaction

This transaction looks weird to me. All the inputs are from outputs with the same scriptpubkey, and all the outputs have the same scriptpubkey. I asked them what they were doing, and btc.com said they were splitting outputs for faster payous. They are doing this because if they don't do this, they run out of outputs for paying users. This still doesn't explain why you would have a bunch of inputs on the same transaction, but that's what they are saying anyway...

## What is it good for?

It's good for education to learn how bitcoin works, see the flow of a transaction being fee-bumped or RBF-bumped. It's useful for scientific purposes, like writing better algorithms for fee estimation and things like that.

<https://github.com/kallewoof/mff>

<https://github.com/kallewoof/cqdb>
