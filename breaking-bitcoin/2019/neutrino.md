---
title: Neutrino, Good and Bad
transcript_by: Bryan Bishop
tags:
  - compact-block-filters
speakers:
  - Jimmy Song
media: https://www.youtube.com/watch?v=ABPOYFw9zAQ
---
... 228C D70C FAA6 17E3 2679 E455
## Introduction

I want to start this talk with a question for the audience. How many of you have a mobile wallet on your phone right now? How many know the security model that the wallets are using? Okay, how many of you trust those security assumptions? Okay, less of you. I am going to talk about Neutrino. In order to talk about it, let's talk about before Neutrino.

## Simplified payment verification

Let's start with simplified payment verification. There are in fact other models and many of your wallets use sometihng else. SPV was described by Satoshi in the bitcoin whitepaper. Once you have a merkle root, it's possible to verify that a transaction is in there. This wasn't implemented until bip37 which was the first time you could do SPV. The thing about bip37 is that it requires server-side filtering. For every client that connects, the server has to do some processing and server-side filtering. It's hard to get the UTXO set using SPV. If you are trying to recover a wallet using bip37, you have to figure out, what is a reasonable last block before my wallet was created? From that block on, you have to go and register a bloom filter and request the filter blocks from the server. Basically you have to keep track of that. It could be a long time, especially if your wallet is old. Very few wallets actually use SPV. If you're not using Breadwallet, pretty much other wallet uses some sort of centralized server. That's what you're using or trusting with your money if you're using a non-Breadwallet mobile wallet.

The client creates a bloom filter. It registers the bloom filter with the server. The server has to process all the transactions in a block through that filter. This is the key bad thing about bip37. On a per bloom filter basis, or per block filter request, it has to calculate all of this. There's a lot of work for the server to do. Once the server figures out which ones fit that filter, and the filter by the way if you don't know is the superset of the interesting transactions for the light client. That's a way to sort of preserve some amount of privacy without downloading the entire block. At that point, the light client has some kind of proof of inclusion and it knows the transaction was in the block and they can verify this because the transaction was in the merkle tree and the merkle root is in the blockheader. Here is how a merkle tree inclusion proof works.

## What's wrong with SPV?

There's a bunch of things wrong with this. For the light client, even if you create a very good superset of your transactions, the server still knows something about what transactions or addresses you might be interested in. So that's a privacy leak. The light client can also get fooled by the server by a transaction omission attack. They can give you proofs of inclusion but they can also just lie to you and tell you the transaction wasn't included, and you have no way to know unless you're checking against different servers- you only need one honest server, but it leaves you vulnerable to an isolation attack. There's a further problem- CVE-2017-12842 which is essentially what you can do is you can fake another transaction within one of the nodes at the bottom of the merkle tree. It turns out that this is more expensive than creating a legitimate proof-of-work and that's an even better way to fool an SPV client.

For the server, the bad thing is that there's a denial of service vulnerability because the client dictates what the server should do. The amount of work the server does scales linearly with the number of bloom filters registered by clients. This is a denial of service vulnerability.

bip37 doesn't really work unless we generally all trust each other. You're forced to trust each other, and both sides are vulnerable.

## Neutrino

What does neutrino do? For the client, what we want is privacy and some sort of sufficient proof that some transaction is in a block, and you want to as best as possible eliminate the omission attack. You don't want lies or omissions to effect you. For the server, you want to reomve the denial of service vector and reduce total computations. Another nice thing would be reduced storage overhead. One of the other problems with bip37 is that you need txindex on because for any spending transaction you need to know the previous transaction's output or the scriptpubkey related to it so that you can run it through that filter. You need to keep that, if you're going to serve up bip37 requests or respond to those requests. Some mutual goals include minimizing trust, minimizing transmission and minimizing calculation as much as possible. With bip37 you kind of have to trust each other, you have to transmit a lot of data, and the server in particular does a lot of computation.

Neutrino servers have a deterministic filter that they calculate on a per-block basis. Instead of having to scale linearly with respect to however many light clients are connected to it, instead you can just calculate one universal filter per block. You can sort of think of it like metadata about the blocks and specifically the UTXOs that were involved. The light client requests a filter for any of the blocks it gets. When requested, the server already has a pre-calculated filter. There is no additional calculation required by the server. The light client at that point checks the filter and sees if any of its own transactions or more specifically scriptpubkey are matching. At that point if there's a match then the client requests the entire block from the server, and then the client can look through all of the transactions and identify their UTXOs or their payment or whatever they need to do.

## Main benefits of bip158 over bip37

The server is less DoS-able because it doesn't have to scale linearly with the number of inbound connections. Also, you don't need txindex. On a per block basis you can calculate all of your filters while you're downloading the blocks yourself. You can keep them around and send them whenever convenient or whenever it's requested.

The client gets to preserve privacy because you're downloading entire blocks. The server does know something about you, which is that when you request a block and maybe timing information. It might suspect that you had a transaction in the block. This is a much larger superset than provided by the bloom filter in bip37. Also, less trust is required: you don't need to trust the server is giving you something, because the filters are essentially deterministic.

The main disadvantage of bip158 is that it requires more bandwidth. The client filter is roughly 20 kb for a 1.4 megabyte block. You need to download this for every single block, and check that against whatever addresses you're looking at. It does require more bandwidth on both sides, but this is a nice tradeoff because you do get some good properties from this.

We know when someone is lying, at least to some degree. There's one lie-by-omission attack we haven't talked about yet. But for the most part you can kind of tell that someone is lying.

## Remaining vulnerabilities in bip158

Lie of omission is still possible because the server can still send you a bad filter. They can send you a filter and say this is the actual filter for this particular block, but there's no way to really very that filter, and it's not committed by the miners in the blockheader or coinbase. There's a concept of filter headers and a chain of these headers but there's no real way to tell other than asking everybody and see if anyone gives you something different. But again, you might be suffering from an isolation attack and maybe you don't know. This particular problem can be fixed with a filter commitment in the coinbase of every block, like in an OP\_RETURN or something. We have to be careful with this because if we have a filter commitment then it would be a soft-fork. The thing about a soft-fork is that it takes a hard-fork to undo; if this is a feature that doesn't get used, then what do we do? One of the clever things the Core developers have thought about is making the commitment soft-fork expire after 3 years. If it gets used, then you would extend the lifetime in some way that makes sense.

The other problem is a bad block attack. This is expensive because you need sufficient proof-of-work. This is like saying okay your transaction was included, I did pay you in that particular block and the client might believe that they got paid. There's no way to know that there's a longer chain because probably they are isolated. This is not necessarily a problem with Neutrino-- this is more of a problem with light clients in general. The deep reason is because light clients really can't verify all of the consensus rules. You need to be able to run a full node in order to verify all the consensus rules. This is a fundamental limitation of light clients. It's not something you can prevent, it's just something inherent to lite clients. You can either make everyone a full node, thus fixing this, but at that point you have all of the drawbacks of running full nodes like bandwidth consumption and all the CPU cost and all this other stuff.

## Alternatives

So we're at a security conference and unfortunately this is the reality of a lot of security things... Nobody really appreciates security until something breaks, and then they tell you that you didn't do a good enough job. There are in fact alternatives to Neutrino.

You could do something with a trusted setup, like you have a node that you completely trust and you communicate from your mobile wallet to that trusted node. As long as you have good encrypted communication or some method of communicating that you find secure, then you can do everything you need to do on a mobile wallet. I think this is the model that electrum uses if you setup your own electrum server on the other side, you just trust the electrum server to tell you all the right answers, in which case you don't need Neutrino you can just use straight communication in fact you might even store all your UTXOs on the server.

You could also trust a third-party, which is how most mobile wallets work. Mycellium wallets always callback to the mycelium servers and as long as you trust them that's fine, but otherwise it's a privacy problem and it kind of sucks. This is another solution.

The third way is that you could trust some combination of third-party, like a majority rules kind of thing where you connect to a bunch of others. This is compatible with Neutrino. Request from multiple servers and check their responses and have some contingency plan for what happens when you get disagreement.

## Summary

To summarize all of this, Neutrino is a strict improvement over bip37 except in bandwidth. You still need to run a full node, because it's possible for servers to deceive you even if at some amount of cost including creating some kind of proof-of-work. Lite clients have this fundamental vulnerability that they can't check all the consensus rules, which opens us up to some level of attack like Bitcoin2x for example. If these servers go in different directions, you have no idea what consensus rules they are following. This is why it's so important to run a full node. This makes it so that you know which consensus rules it is following.
