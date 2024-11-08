---
title: 'Libbitcoin: A practical introduction'
transcript_by: Bryan Bishop
speakers:
  - James Chiang
date: 2019-09-10
aliases:
  - /scalingbitcoin/tel-aviv-2019/edgedevplusplus/libbitcoin
---
or: libbitcoin's bx tool: Constructing a raw transaction

<https://twitter.com/kanzure/status/1171352496247365633>

<https://github.com/libbitcoin/libbitcoin-explorer/wiki/Download-BX>

# Introduction

I am going to talk about libbitcoin. It's an alternative implementation of Bitcoin Core. There's a few alternatives out there, like btcd and then bcoin. Libbitcoin is written in C++ and it's the oldest alternative implementation that is out there. I'd like to show a few examples of what you can do with libbitcoin. I'd like to show how it is designed and give you a sense for its architecture an dalso show some design tradeoffs compared to the original implementation.

My involvement started out with writing on the wiki documenting the different libraries. My journey in bitcoin started with libbitcoin. Since the library is structured in such a modular way, it was actually easy for me to understand the protocol just by reading the details.

# Agenda

I'll talk about libbitcoin and libbitcoin explorer which allows you to do wallet generation, wallet management, key generation, and also serves as a client to the RPC server. Then I'll look at the server itself, and finally the node.

# Introduction to libbitcoin

This is the libbitcoin project. Here's the dependency graph. There's libbitcoin-explorer, libbitcoin-server, -node, -client, -protocol, -network, -database, -consensus, secp256k1, -network, -protocol, -client, -explorer. The lead developer is Eric Voskuil. He's here today. The project was originally initiated by Amir Taaki. It is the oldest alternative implementation to Bitcoin Core. It's not a fork. The codebase is not related, with the exception of libsecp256k1. It of course implements the same protocol, we hope.

# libbitcoin principles

Our primary principles are modularity, legibility, it's designed to be performant. And it's also designed to be scalable.

# Alternative implementations

Why do we need alternative implementations? Eric has a nice writeup about the genetic purity fallacy. The argument usually goes, Bitcoin Core is so complex, that it's impossible to get two separate implementations that behave identically. So therefore we should only have one implementation. But that's not entirely true. For one, there is no way we can have only one true client. Every client can diverge from the previous version, so there can't really just be one true client version or implementation. There are many reasons why a client might diverge from one user to another.

One of the other arguments was about "systemic risk" like protocol divergence. If theoretically you had a more vibrant ecosystem implementation, then the risk of divergence is less because if only 10% of the nodes are experiencing a system partition, that's better than all of the clients failing at the same time because then it would be even more confusing to figure out whether it's a problem worth fixing to average users.

# Explorer demo: HD wallets

libbitcoin-explorer is not just an RPC client that is different from the CLI client found in Bitcoin Core. It actually has a lot of the core library functionality in it. It has wallet commands, transaction commands, and other utilities. They are exposing parts of libbitcoin system library in the explorer tool itself. It also has a few server call methods, chainstate methods, transaction fetch or index, broadcast. It's like a hybrid tool that lets you do different things.

I'll show an example to make this more clear. I'd like to start with HD key generation and derivation. I think Bryan gave an HD wallets talk so I won't go into too much detail. This is the flow of making an HD wallet.

<https://diyhpl.us/wiki/transcripts/scalingbitcoin/tokyo-2018/edgedevplusplus/hierarchical-deterministic-wallets/>

I'm just running a shell script that calls the bx tool, which is installed on my computer locally. This is a jupityr notebook. I'm show Bryan showed a few things from here.

Say you want to restore a wallet. If you want to restore a wallet, you kind of need to know which addresses you generated and which ones received coins. When we restore a wallet, we take the mnemonic and we generate keys. Then we request from the server whether these addresses have a history. From that, we can tell, assuming that these keys are generated and used sequentially, then we can figure out which HD derivation state was of the wallet the last time it was used before recovery. But we won't know if receive addresses were handed out that are not yet used on the network, but still handed out to users.

The next example is constructing a payment channel with bx. A payment channel is just a few transactions with certain output scripts. I'm trying to get this example into the Mastering Lightning book from Andreas Antonopolous. It's a great example for showing how easy it is to create a channel with only a couple lines of code.

# libbitcoin server

In bitcoind, RPC is designed as a local client interface. The server does the signing and everything else. But in libbitcoin, the server is meant to serve as a public index of data on the blockchain. It uses the zeromq messaging framework. It uses the libsodium authentication-encryption scheme. The idea is that zeromq allows us, this is a messaging framework designed for distributed systems and microservices. It allows us to scale the server horizontally quite nicely.

# Client zeromq dealer socket

In this example, I have the zeromq socket at the top, and the zeromq dealer socket on the other side. I want to show what happens when one side is offline or backed up. The client is trying to send messages to the server, and the server is either slow or offline. The zeromq socket then blocks on the client side. Messages don't get lost, but they get blocked. Then the server comes online, and then the send socket on the client side is no longer blocking.

But what if the messages are queueing on the server side because the client is a slow receiver? The messages queue on the server side, the server has to figure out how to manage that or when to drop messages.

What if there are multiple zeromq servers to connect to? The client automatically distributes the requests round-robin style. Every connection to a server has an independent send and receive queue on the client side.

# libbitcoin zeromq router socket

What happens when one client creates a higher load than other clients? There's a fair queueing algorithm in zeromq to make sure that no one client gets an extraordinarily high share of requests and thereby potentially DoSing the service.

Internally, we also use zeromq to distribute work to the workers. You can configure how many server workers you want. That's all configured through zeromq.

Bitcoin Core uses zeromq but only as a subscription service, not to do RPC.

# libbitcoin v4: websockets interface

libbitcoin v4 is not released yet. It's in progress. What's happening here is we're building an HTTP server on top of the zeromq interface. The websocket support, the json/rpc interface, basically just forward the request to the underlying zeromq querying interface. The robustness of this server-client message handling that we saw before is maintained.

# Address index: wallet client

libbitcoin also indexes by address. It was always debated whether Bitcoin Core should have an address index. This is the case in libbitcoin. I actually use this. I was restoring my wallet. I took my mnemonic backup phrase, I generated a derivation path, and for every key I queried the server to see if that key has a history so that I can figure out to which bip32 derivation path I generated keys. This is possible in libbitcoin because of this address index.

# Address index: payment server

Say I'm generating a payment invoice. I want to know when this key in the invoice is appearing in the unconfirmed transaction set. I can subscribe to that address, and I can get a notification when it gets into the mempool and then a second notification once it gets confirmed. This is all possible because we have an address index.

# libbitcoin: network (p2p)

libbitcoin's node includes a nice p2p module. This encapsulates the functionality to maintain connections on the bitcoin p2p network. This doesn't include transaction propagation, but ping-pong and the most basic messaging protocols you need to keep a p2p connection alive. What you see here are the different classes and how they are encapsulated. You can manually configure peers to connect to. There's an inbound session and an outbound session.

# libbitcoin database

libbitcoin implements its own database, interestingly enough. Let's spend a minute talking about how it works. I think it's a neat design. The libbitcoin database is basically just a hashtable that lives in a memory mapped file. You tell the operating system that there's a file that I want the operating system to manage and map to memory. Depending on what parts of the hashtable you want to access, this data may or may not reside in memory.

One point I'd like to show is the ability to write in parallel simply because the only part that is guarded is the allocation. If I have a new transaction or block that comes in, I allocate space for that block, but in a previous allocation I continue to run or write there. This lets us write in parallel to the database. This is useful for block sync where I'm downloading blocks in parallel and these can all be written to the database. The writing stage can be parallelized, which is nice.

# libbitcoin v4: continuous parallel block download

In libbitcoin v3, the initial block download is synchronous. I think Eric has been working on this for over a year now. Since we can parallel-wise store blocks to the libbitcoin database, the continuous parallel block download is a nice optimization. We can request blocks from our peers in parallel, we can drop peers that are slow. Once the blocks are connected, we can do the full contextual validation from the genesis block.

# WIP: libbitcoin v4

Here's the things in v4. There's an HTTP server being implemented by Neill. This includes websockets and JSON-RPC and it's partially compatible with Bitcoin Core. There's also improved initial block download (IBD) (continuous parallel block download), and Neutrino filter support.

Okay, that's my presentation. Thank you Anton for having us. I think it's important that we have alternative implementations, that we know they exist, and that we use them. I think this contributes to a more healthy development environment for bitcoin.

# See also

<https://diyhpl.us/wiki/transcripts/building-on-bitcoin/2018/libbitcoin/>
