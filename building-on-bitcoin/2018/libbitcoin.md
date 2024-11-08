---
title: Libbitcoin
transcript_by: Bryan Bishop
speakers:
  - Eric Voskuil
date: 2018-07-04
media: https://www.youtube.com/watch?v=QtB4YUneiEE
---
<https://twitter.com/kanzure/status/1014483126817521665>

This is me. When I first suggested giving a talk here on libbitcoin, ....  one of the pieces of feedback I got was that bitcoin is libbitcoin, what are you building on bitcoin? libbitcoin is actually more. I will also talk about what it is going on underneath. It's an implementation of bitcoin as well.

Most of the talks I give are around cryptoeconomics. Up until recently, libbitcoin hasn't been mature enough to go and promote. This is one of the first talks I've given on libbitcoin actually.

For me, it's important to cover the crypto-economics behind libbitcoin. Building on bitcoin is really more than just building financial tools that use bitcoin, it's really about building on bitcoin. Making something that bitcoin pulls more people in towards bitcoin.

Individual power should be enhanced. Say you have in bitcoin, how you help protect it. If everyone moves off to a centralized system for validation for say mining-- one person has say in everything.We want to build tools that build on bitcoin, not tools that pull people away from bticoin. This is what libbitcoin is all about Helping people build bitcoin stuff, not encouraging people to use a centralized API that really takes that power away from them.

That power is interms of security is expressed by miners and merchants. Miners secure conrfirmations, and merchants secure the rules, and validate in a way that matters

Independent exercise of power implies you're doing it covertly. If you're doing it publicly and someone steps in and says don't do that, and you're orced to comply, you don't have the power-- the person forcing you has the power. When we talk about decentralization of bitcoin and security, you have to wonder and ask yourself, why does decentralization matter? McDonalds is highly decentralized-- they are everywhere, but you can still force them to apply a tax law. Decentralization exists so that people can hide and operate.

The concept of anonymity is the essential element of covert operations. Decentralization is another way that people are allowed to be anonymous. If you are big, you can't hide.

Bitcoin relies on public data that can be verified to achieve anonymity. It doesn't achieve this through encrypted channels in the same way that banking systems works. It works by giving everyone the same copy of the data.

Large operations are inconsistent with anonymity. Big server farms can be taken down-- it's not anonymous if it can be taken down. Decentralizability is important.

Bitcoin requires competitive performance for small operation. Competitive performance-- you have to, at a lwow level, can be competitive at a lwow level... if only large server farms can do bitcoin, then bitcoin is not secure, it's only secure for the few people who do it, as long as they are allowed to do it.

In terms of-- I mentioned mining. The other half of the security model is merchants. if you sell something for bitcoin and you validate that coin, then you are providing security for the system. If that's all done publicly and large-scale, then you don't have that ability, people that can force you have the say.

Are there shortcuts? Non-economic nodes, like just throwing up 10,000 validating nodes on AWS.... that's completely irrelevant and does nothing for the security of the system. Layering does not change the individual node requirements. Everyone still needs to run their own node. Prunnig does not remove the full chain validation requirement unless you want to trust a central authority to ensure the data is valid.

Checkpointing reduces individual power by delegating some part of validation to someone else. The point I am trying to make is that bitcoin requires people to run full nodes, for miners and merchants. You can't get away with not doing it.

In libbitcoin, we're focused on the bitcoin stack right now. It's usable for development. People can build on bitcoin, instead of pulling people away.

Amir Taaki started libbitcoin in 2011. It's the first implementation of bitcoin after Satoshi's implementation. It's taken a while to get mature, but it's been around for quite a while.... There were several main principles-- it needs to beprivate, it needs to be scalable, and it needs to have integrity such that no individual or group should have enough power to coerce users.

In libbitcoin, there is the system, blockchain, build, client, consensus, database, explorer, network, node, protocol, server.

boost is a primary dependency, and libsecp256k1 is another dependency. Otherwise, unless you're doing client-server stuff, there's not many other dependencies. We use zeromq as a client-server protocol stack.

OUr bitcoin server-- we have a node, and then bitcoin server is additional code on top of the node. It provides command line options, configuration settings, you can run bitcoin-server as a single file. There's a library that implements this stuff, so you can take the library and build your own user interface over it. Websockets has been useful for local machine oeprations, we're adding that, open up a browser and talk to the implementation. The client-server interface includes payment subscription, querying, block and transaction broadcast. Usually we think about the RPC interface, this replaces it with a robust client-server interface.

bitcoin-explorer is on the client side. It's an executable you can use to run the node and the server. The client side has administrator tooling. You can talk to the server, do cryptographic primitives, make transactions, run different commands... you can use CurveCP and SOCKS5 (Tor).

My focus here was not to talk about all the things in libbitcoin. We're doing some new interesting things on performance. The performance is important.

libbitcoin is very different from traditioanal full node implementations. There's no transaction memory pool, there's no block memory pool, no signature or script cache, no unspent output store, etc. The store is a small amount of memory-mapped files. You never hit the disk when you're querying. If you're running a high-performance server with a lot of RAM, then the entire store can sit in RAM. The files are arrays and hash tables. So we get constant-time lookup for every single thing we look up in the chain. And we use zeromq, you can use in-process binding--- you can run these queries in-process with the server, or run them over the IPC, or run them over the intenret with CurveCP or something. You can scale your client or your wallet app or your mining app sitting on top of the node away from the box, or you can have it very close, depending on your performance requirements. This is constant time and extremely high performance. I saw yesterday that you can run 200 wallets on Bitcoin Core? That's absurdly low to me. You should be able to run millions. More hardware, more performance, preferably in a linear fashion.

Bitcoin in terms of transaction processing is non-scalable. You can't add more hardware and make bitcoin process more transactions. When it comes to layering, bitcoin is infinitely scalable, you can transfer all the value in a single transaction. Layer is taking advantage of the ability to transfer large amounts of value with small amounts of data without having to increase transaction volume.

When we talk about scalability of the node, we're not talkning about transaction performance, but just internal node oprations like query optimizations or running servers or boxes.

We always index all transactions. In Bitcoin Core, that's a command line option. We always index spent-by.. it could be a huge amount of data but we end up with a data store that is about the same size as Bitcoin Core without its txindex. I don't know what their problem is.

ElectrumX provides an additional index over on top of the bitcoind store. Basically, you let bitcoind sync the entire chain, then you reindex on top of it, it's about an additional 35 gigabytes of data. Our server indexes all that data and it ends up with smaller store.

I don't think you will find any bitcoin node that is faster than libbitcoin. I'd challenge you to find something better. I don't have numbers for across the ecosystem. For syncing, it's really slow. We were doing some prototyping last year about fast initial block download. We fully paralleilized the database and you can write blocks and transactions at the same time from multiple peers. We synced the entire bitcoin mainnet chain in 15 minutes off of a fast network. That's pretty good. A bunch of nodes running on the same LAN. We were relying on checkpoints to skip validation though.If you don't have that, how do you know when to start? It's a hard problem. The solution relied on that, which I saw as a weakness. So I figured there's a way to do this, and it might take a while to implement, and it might have a syncing process that takes a wile-- and we'll do the work and finish it in v4. Initial block download is kind of slow. It's not horrible, but I'd like to see a 10x improvement over bitcoind which is what I've been shooting for for a while. I want to parallelize initial block download and parallelize it to be continuous block download. We don't have a lot of stuff stored in RAM, it goes to disk as we validate, but if something gets reorged, whatever, it always gets the same transactions validated from the disk and so on. We end up building a tree of blockehader metadata as the node starts up. Eventually the tree is current, and then we organize that on to the disk. We have a candidate array, blocks that are potntially going to be confirmed... we do it in parallle... we start downloading. We have a tree of blocks, usualyl a list, once we find the longest branch in the tree, we commit it to disk, and once we're in the current timeframe based on timestamp, we start downloaing in parallel from peers, we use standard deviation to find the fast peers, we weed out the slow peers, we don't have to give priority to the slower peers because we already know the blocks are good we just want to hit the peers that are giving the fastest response. We write all the blocks to disk concurrently, we do the minimum required validation to know that it's expensive data for someone to fake-- it has PoW associated, all the transactions are there, they get flushed to disk at the same time. We don't have to rely on checkpoints, we rely on having the strongest chain with current timeframe and that can change.... you have a candidate chain and the most recent strong known chain. This is also useful when you shutdown your node and come back online a while later. There's a validation chaser that goes and does validation in parallel after you have downloaded. We get to bring in blocks all at the same time, put them on disk all at the same time. We take about 2.5 hours to sync bitcoin mainnet-- and server indexing takes an additional 15 minutes.  I think on the same machine, Bitcoin Core takes about 12 hours.

# See also

<https://diyhpl.us/wiki/transcripts/scalingbitcoin/tel-aviv-2019/edgedevplusplus/libbitcoin/>
