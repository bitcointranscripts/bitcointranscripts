---
title: Overview Bitcoin Core Architecture
transcript_by: Bryan Bishop
speakers:
  - James O'Beirne
tags:
  - bitcoin core
media: https://www.youtube.com/watch?v=L_sI_tXmy2U
date: 2018-10-05
aliases:
  - /scalingbitcoin/tokyo-2018/edgedevplusplus/overview-bitcoin-core-architecture
---
<https://twitter.com/kanzure/status/1048098034234445824>

slides: <http://jameso.be/dev++2018/>

# Introduction

Alright guys, how are you guys doing? You guys look tired. Given your brains are probably fried, I am delighted to tell you that this talk will be pretty high level. I am James O'Beirne, I work at Chaincode Labs. I've been working on Bitcoin Core since 2015. I am in New York most of the time.

# Agenda

Today we are going to talk about Bitcoin Core. This will be pretty high-level. We're going to talk about what Bitcoin Core does in a general sense, what its user interfaces are, the concurrency model and how it does things at the same time, we'll talk about regions of code, how storage works, what the various data structures are, and some future work you can keep an eye on.

In this talk, we're going to talk about the concurrency model and how to do things simultanoeusl.y We'll talk about the major subsystems, about storing and access data, and what are some of the major data structures.

# Bitcoin Core

Bitcoin Core does a number of things. It's a validating and relaying node in the p2p network. It passes around blocks and transactions and maintains some notion of validity.

It's also a wallet implementation. It's a GUI and RPC tool for end-users that want to manipulate and work with coins. It's also a working example for people doing wallet implementations. Right now Bitcoin Core has one of the most sophisticated coin selection implementations, and it's a reference implementation for other wallets that want to follow.

Bitcoin Core handles block assembly and submission for miners.

Bitcoin Core provides a programmatic interface for bitcoin applications, like block explorers and others, using the RPC API and CLI.

# Glossing over

I will not be covering: cryptographic implementation details, p2p message protocol, graphical code in qt/, test framework in test/, or exact validation semantics or basically anything detailed. Hopefully you will take the content in this talk and go do some exploration for yourself. This should just be a blueprint for you to go poke around later.

# User interface: p2p

Bitcoin forms a TCP overlay network of nodes passing messages to one another. These are defined in <https://github.com/bitcoin/bitcoin/tree/master/src/protocol.h> including net message types you can look at. That's a succinct summary of the message types nodes can communicate to each other.

You can manually add nodes with the -addnode flag. You can set the number of max connections with -maxconnections and these are MAX\_OUTBOUND\_CONNECTIONS and DEFAULT\_MAX\_PEER\_CONNECTIONS.

DoS protection is very important because it prevents malicious peers from disrupting the network. Simple payment verification (SPV) nodes query full nodes for merkle proofs, so Bitcoin Core provides that.

# User interface: RPC/HTTP

This is an easy way for users to interact programmatically with Bitcoin Core over HTTP. The CLI is actually powered by the RPC interface.

# User interface: QT

Who here has used this? Oh, okay. Interesting.

# User interface: ZeroMQ

The zeromq interface publishes notifications over a socket. I think the bitcoin fee bot and bitcoin twitter confirmations bot are built using this zeromq interface.

# Concurrency model

Let's get into the concurrency model. Bitcoin Core performs a lot of tasks simultaneously and it needs a way to do that. Basically the way it does that is using threads and some shared data structures which are guarded by locks. It's a little deceptive because Bitcoin Core is in some ways literally multithreaded but for many of the important operations, it's not, and you're contending for the locks all at the same time.

A lot of the initialization stuff happens in <https://github.com/bitcoin/bitcoin/tree/master/src/init.cpp>

p2p networking is handled by a single select loop in ThreadSocketHandler under CConman. We may replay select with poll (PR 14336) to avoid file descriptor limits.

All changes to the chainstate are effectively single-threaded thanks to cs\_main. If you have have 3 hours to kill, grep for cs\_main and see the horror.

# Threads

<table>
<tr><td>script verification</td><td>nproc or 16</td><td>ThreadScriptCheck</td></tr>
<tr><td>loading blocks</td><td>1</td><td>ThreadImport</td></tr>
<tr><td>Servicing RPC calls</td><td>4</td><td>ThreadHTTP</td></tr>
<tr><td>load peer addresses from DNS seeds on startup</td><td>1</td><td>ThreadDNSAddressSeed</td></tr>
<tr><td>send and receive messages to and from peers</td><td>1</td><td>ThreadSocketHandler</td></tr>
<tr><td>Initialize network connections</td><td>1</td><td>ThreadOpenConnections()</td></tr>
<tr><td>Process messages from net to net\_processing</td><td>1</td><td>ThreadMessageHandler</td></tr>
<tr><td>Tor control</td><td>1</td><td>TorControlThread</td></tr>
<tr><td>walletnotify</td><td>1</td><td>user-specified</td></tr>
<tr><td>txindex building</td><td>1</td><td>ThreadSync</td></tr>
<tr><td>blocknotify</td><td>1</td><td>user-specified</td></tr>
<tr><td>upnp connectivity</td><td>1</td><td>ThreadMapPort</td></tr>
<tr><td>CScheduler service queue</td><td>1</td><td>CScheduler::serviceQueue</td></tr>
</table>

The ValidationInterface allows the asynchronous decoupling of chainstate events from various responses. Use SingleThreadedSchedulerClient to que responses and exceute them out-of-band. You can use events like UpdateBlockTip and others, and BlockConnected, BlockDisconnected, etc.

# Exercises

Grep for CCriticalSection to find most of the lock definitions and the trace threads, used for whenever threads are spawned.

# Regions

Regions of code are little modules of state and procedures that each do a thing for bitcoin. It's not an official term. It's just subsystems that handle different tasks. Looking at these things should hopefully give us an idea of the different granual ideas of what bitcoin does and where it does them.

<table>
<tr><td>net</td><td>handles socket networking and tracking of peers</td></tr>
<tr><td>net\_processing</td><td>routes p2p messages into validation calls and other response p2p messages</td></tr>
<tr><td>validation</td><td>defines how we update our validated state (chain and mempool)</td></tr>
<tr><td>txmempool</td><td>mempool data structures</td></tr>
<tr><td>coins and txdb</td><td>interface for in-memory view of the UTXO set</td></tr>
<tr><td>script/</td><td>script execution and caching</td></tr>
<tr><td>consensus/</td><td>consensus params and merkle roots and some transaction validation</td></tr>
<tr><td>policy/</td><td>fee estimation and replace-by-fee</td></tr>
<tr><td>indexes/</td><td>peripheral index building (txindex)</td></tr>
<tr><td>wallet/</td><td>wallet database and coin selection and fee bumping</td></tr>
<tr><td>rpc/</td><td>defines the rpc interface</td></tr>
</table>

# Regions: net.h, net.cpp

<https://github.com/bitcoin/bitcoin/tree/master/src/net.h>

<https://github.com/bitcoin/bitcoin/tree/master/src/net.cpp>

net is the bottom of the Bitcoin Core stack. It handles network communication with the p2p network.

# Regions: net\_processing.cpp

<https://github.com/bitcoin/bitcoin/tree/master/src/net_processing.h>

<https://github.com/bitcoin/bitcoin/tree/master/src/net_processing.cpp>

net\_processing adapts the network layer to the chainstate validation layer. It translates network messages into calls for local state changes. "Validation"-specific (information relating to chainstate) data is maintained per-node using CNodeState instances.

Much of this region is ProcessMessage() - a giant conditional for rendering particular network message types to calls deeper into Bitcoin Core, such as BLOCK and HEADERS NetMsgType.

Grep for "Misbehaving" to find all the places where we downrate nodes and peers for giving us invalid blocks or whatever.

# Regions: validation.cpp

<https://github.com/bitcoin/bitcoin/tree/master/src/validation.h>

<https://github.com/bitcoin/bitcoin/tree/master/src/validation.cpp>

validation handles modifying in-memory data structures for chainstate and transactions (mempool) on the basis of certain acceptance rules. It both defines some of these data structures such as CCHainState, mapBlockIndex, as well as procedures for validating them, such as CheckBlock.

Oddly, it also contains some utility functions for marshalling data to and from disk, e.g. ReadBlockFromDisk, FlushStateToDisk, DumpMempool, LoadMempool. This is probalby because validation.cpp is the result of refactoring main.cpp.

Here's a diagram of how validation relates to the other regions here.

# Regions: coins.cpp

<https://github.com/bitcoin/bitcoin/tree/master/src/coins.h>

<https://github.com/bitcoin/bitcoin/tree/master/src/coins.cpp>

<https://github.com/bitcoin/bitcoin/tree/master/src/txdb.h>

<https://github.com/bitcoin/bitcoin/tree/master/src/txdb.cpp>

CCoinsView boils down to getting an unspent coin and seeing if it's unspent. The rest is just implementation detail.

# Regions: dbwrapper.cpp

This is an abstraction around the leveldb database. I'll talk about other storage mechanisms later in the deck. This allows us to obfuscate data, which allows us to avoid spurious anti-virus detection and various things to prevent people from getting in trouble for running a full node with all the arbitrary blockchain data.

# Regions: script/

<https://github.com/bitcoin/bitcoin/tree/master/src/script/>

EvalScript is the script interpreter.

# Regions: consensus/

<https://github.com/bitcoin/bitcoin/tree/master/src/consensus/>

This was an attempt to consolidate a lot of what dictates consensus, but almost everything in bitcoind dictates consensus. It defines the bip9 deployment struct, which is kind of interesting if anyone remembers from 2017.

CValidationState is in there which is a little piece of state that gets passed around in places to accumulate DoS scores.

# Regions: policy/

This is for making assesments about transactions, such as whether a transaction is signaling replace-by-fee. It also has some code for doing fee estimation.

# Regions: interfaces/

This is a newer addition. This is the start of the numeration of all the interfaces in Bitcoin Core. This is part of an effort from ryanofsky to use more formalized messages. Orginally everything was running in one process but maybe one day all of the components will be running in different processes or maybe even separate code repositories. The first step of that is separating things out into different interfaces.

# Regions: indexes/

This is some work by jimpo (Jim Posen). Does anyone not know what the txindex is? It's a quick way to look up from the hash of a transaction into the raw data for the transaction. It's a useful thing to have if you're a block explorer. There's some additional indexes proposed, like marcinja did some work in #14053 to implement an address-to-transactions index. This thing actually makes use of the ValidationInterface construct.

# Regions: wallet/

This does what it says- it's logic for marshalling wallet data to and from disk via BerkeleyDB. Utilities for fee-bumping transactions, does coin selection, RPC interface for the wallet, and some bookkeeping.

# Regions: rpc/

This is where all the definitions for rpc functions live. It's fairly easy to add an RPC, just look at any of them for an example.

# Regions: miner.cpp

<https://github.com/bitcoin/bitcoin/tree/master/src/miner.cpp>

<https://github.com/bitcoin/bitcoin/tree/master/src/miner.h>

This is useful for constructing and generating blocks. getblocktemplate is how you distribute a block template to a mining tool to get everyone coordinated on the same block. And submitblock does what it says.

# Regions: zeromq

I was talking about this earlier.

# Storage

How do we store stuff in Bitcoin Core? Here's a tree of the file structure if you go into your data dir you're going to see a banlist, blocks/, chainstate/, and others.

`$ tree ~/.bitcoin/regtest/`

```
├── banlist.dat
├── blocks
│   ├── blk00000.dat
│   ├── index
│   │   ├── 000005.ldb
│   │   ├── 000006.log
│   │   ├── CURRENT
│   │   ├── LOCK
│   │   └── MANIFEST-000004
│   └── rev00000.dat
├── chainstate
│   ├── 000005.ldb
│   ├── 000006.log
│   ├── CURRENT
│   ├── LOCK
│   └── MANIFEST-000004
├── debug.log
...

├── fee_estimates.dat
├── indexes
│   └── txindex
│       ├── 000003.log
│       ├── CURRENT
│       ├── LOCK
│       └── MANIFEST-000002
├── mempool.dat
├── peers.dat
└── wallets
    ├── db.log
    └── wallet.dat
```

# Storage: .dat files

The .dat files are basically just raw bytes of some serialized data structures. You can checkout serialization here: <https://github.com/bitcoin/bitcoin/tree/master/src/serialize.h>

# A brief digression into serialization

There's a macro called ADD\_SERIALIZE\_METHODS and there's some magic around how these structs are packed into raw bytes.

# Leveldb

Leveldb is a fast, sorted key value store used for a few things in Bitcoin. It allows bulk writes and snapshots. It is bundled wit hthe source tree in src/leveldb/ and maintained in bitcoin-core/leveldb.git repository on github.

Leveldb has the block index, which is the tree of all the valid blocks we've seen. It also handles something called chainstate/, which is really just the UTXO set.
