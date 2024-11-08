---
title: Bitcoin Peer-to-Peer Network and Mempool
transcript_by: Caralie Chrisco
tags:
  - p2p
  - transaction-relay-policy
media: https://youtu.be/eVerdR2hOMw
speakers:
  - John Newbery
aliases:
  - /scalingbitcoin/stanford-2017/edgeplusplus/p2p-john-newberry
summary: John Newbery covers the primitives and functionality that comprises Bitcoin peer-to-peer network. This includes types of nodes that comprise the network, message format, control messages, transaction and block propagation, mempool, fee estimation, compact blocks etc.
---
Slides: <https://johnnewbery.com/presentation/2017/11/02/dev-plus-plus-stanford/p2p.pdf> & <https://johnnewbery.com/presentation/2017/11/02/dev-plus-plus-stanford/mempool.pdf>


## Intro

John: So far today, we've talked about transactions and blocks and the blockchain. Those are the fundamental building blocks of Bitcoin. Those are the data structures that we use. On a more practical level, how does a Bitcoin network actually function? How do we transmit these transactions and blocks around? Well, the answer to that is a peer-to-peer network, which is what I'm going to talk about now.

I'll give you a brief overview of what the P2P network is. I'll talk about different kinds of nodes on that network. There are different nodes. I'll talk about the message format. I'll talk about control messages, transaction propagation, and finally, block propagation.

## P2P

So what is the peer-to-peer network? It's how transactions and blocks are propagated from your node across to the other nodes in a Bitcoin network. It's a completely flat open peer-to-peer network. There's no authentication. There are no special control master nodes or anything like that. Each node on the network is a peer, and it needs to be resistant to attack because it's open, right? There's no wall between Bitcoin and the rest of the world. Bitcoin must be resistant to things like denial of service attacks, Sybil attacks, and so on.

So what kind of messages make up the peer-to-peer network? What kind of message do we send? VERSION, VERACK, ADDR, GETADDR, INV, GETDATA, GETBLOCKS, GETHEADERS, TX, BLOCK, HEADERS, PING, PONG. Lots of different messages. We'll go over some of those in this session.

How do we connect to that network? Initially, we connect to something called a seed node. A seed node will tell us about other nodes on the network using the ADDR message. The ADDR is telling us about the address of other nodes that we can reach on the network, and your Bitcoin Core node will connect to up to eight outbound connections, outbound (full) peers. [NOTE: since this talk, [two block-only relay connections have been added](https://github.com/bitcoin/bitcoin/pull/15759)]

Other implementations may do something different, but for Bitcoin Core, it's 8, and you may or may not accept an inbound as an option you can set. So your outbound nodes, they're the important ones. They're what you're relying on. Inbound could be anything. So far, so good?

So it's a completely open network. You could connect to something that's complete garbage, right? You don't know what you're connecting to. So if you connect to a node that misbehaves, they need to be removed somehow. They waste our system resources. They take up slots that could be used for honest nodes, and those things are bad. So if they're wasting our system resources after leaving us open to denial of service attacks, they might blow up our memory usage or a network usage, or disk usage. If they're taking up slots that could be used for honest peers, that leaves us open to a Sybil attack or an eclipse attack. If, in fact, we're surrounded by dishonest nodes, we can't get the actual state of the network.

Let's talk about what bad behavior might involve. It might be invalid transactions or blocks. That's pretty easy for us to see. Because we validate everything we see, if a peer sends us an invalid transaction, we can see that instantly. They might send us unconnected blocks. They might send us blocks that don't connect to our chain. Which, in some cases, that's valid. We might be missing some blocks in a chain, and they're telling us about what's at the tip. But you know if they keep sending us unconnected blocks, maybe they're feeding us a false chain. Something that's valid, but it's not the actual true most work chain. They could stall. They could be attacking us somehow by using up our slots and sending us information really slowly, so we don't get the most recent blocks, or it takes us a long time to reach the tip.

They could send us things called non-standard transactions. There are two types of rules in Bitcoin. There are consensus rules. Something invalid by consensus is just completely invalid. Standardness is more about how we propagate transactions before they get in a block, and transactions can be non-standard, which means by default, we won't propagate them around, but a peer might send us a bunch of non-standard transactions.

Audience Member asks a question (inaudible)

John: An empty transaction? An empty block? No. Anything in a block is standard. Standardness only applies to transactions outside blocks. There'd be things like, before CSV (CHECKSEQUENCEVERIFY) was activated, we might make using that opcode non-standard, so those transactions don't get propagated around, and then when CSV is activated, it becomes standard. It's a way of managing soft forks, and we had non-standard rules for SegWit as well. We might just get malformed messages. We might get something that is actually complete garbage.

So what do we do about that? We have a few options. We might just ignore that, right? Just drop the message and continue. Stay connected to the peer. Don't take any action. We could disconnect the peer immediately if it's something bad. We could ban the peer. That's slightly stronger. That's where we disconnect them and make sure they don't reconnect within 24 hours. Or we can apply DoS points. We might apply 10 DoS points if they do something bad. When their DoS score reaches 100, we ban them. This stuff is always changing within Bitcoin Core. It's not optimal right now. We can do better, but these are the kind of options we have.

Any questions about that?

Audience Member asks a question (inaudible)

John: So the question was, how does a DoS score work?

It's a bit of a mess, to be honest. By default, if a peer reaches 100 points, we ban them, and we'll give them 10 points if they feed us 10 unconnected blocks. I think that's right.

Audience Member: So, a node can rack up ban points for misbehavior?

John: Right. Then you'll be banned after you reach 100, and that lasts 24 hours.

Audience Member: A node's behavior doesn't propagate throughout the network, right?

John: Yeah, this is our node making decisions about its peers. I won't go into that in any more detail, but that's kind of a high level.

## Types of Nodes

Let's talk about different types of nodes on the network. The gold standard is a full node, otherwise known as a fully validating node. That's because it validates all of the rules, all of the consensus rules of Bitcoin. It receives blocks as they're mined and propagated. It verifies the validity of those blocks. It verifies that all of the transactions in that block are valid and are spending unspent outputs, and it enforces the consensus rules of the Bitcoin network. To do that, it needs to keep a collection of all of the unspent outputs. That's the set of information that we're interested in. It's the most secure and the most private way to use Bitcoin. If you use your own full node, you're validating the rules. You're making sure that there's no extra inflation, there are no double spends. It's also the most private because you're not telling anyone about your addresses or your public keys.

## Pruned node

There's the concept of a pruned node. This was introduced in v10 or v12, I think. A pruned node is a full node. It's still validating all of the rules of the Bitcoin network. The only difference is it's discarding old blocks after it's validated them. That saves on disk space. It's got to retain a bit of history, up to two days. I think two days minimum and the undo data that I told you about. If there's a reorg, even if a day reorg, that would be a really large reorg, it can still do that. It propagates the new blocks. It sees, but it can't serve old blocks to peers. When you turn your node on for the first time, you need to download all of the blocks in the blockchain. That's called initial block download. If you connect to a full node that doesn't prune, you can download all of the old blocks. If you connect to a pruned node, obviously, they can't serve you those old blocks because it has pruned them away. In terms of security, it's as secure as a full node. It is a full node, right? It's validating all of the rules is making sure the miners aren't increasing inflation. It's making sure that there aren't double spends. It's a full node, but it's just saving a bit of disk space.

Audience Member: Do you know that the node is pruned?

John: Yes. You don't know they're pruned. You know that it can't serve your blocks because in its version message, it doesn't send you a service bit node network. I'll talk about version and service bits later, but you know that you can't get blocks from it.

Audience Member: Is this considered the implementation from the white paper where Satoshi considers saving disk space?

John: Kind of. I haven't read that chapter recently in the white paper.

Audience Member: (inaudible)

John: That is slightly different. A full node has two types of data. It has the blocks as they were serialized, which it's storing on its disk, and that will be up to 200 GB at this point, and it has a set of unspent transaction outputs. What you need in order to enforce the rules of the network is that set, the UTXO set. The archive of blocks is basically dead data. You don't use it for validation, and if you remove that and you just have the UTXO set, you can still validate all of the rules. So that UTXO set does not include spent outputs. Those spent outputs have already been removed. I'm sorry I don't have that white paper and chapter 7 in my head, but it sounds slightly different. Any other question about pruning?

## Archival Nodes

I'm going to talk about archival nodes. All I mean by that is, it's a full block that stores the entire history. It's like an archive, and it can serve blocks to its peers on the network. Unlike a pruned node, which can't serve all blocks, an archival node can serve you any block in the history. That's signaled using your NODE_NETWORK service bits in the version handshake. That should answer your question.

## SPV Nodes

Next are SPV nodes. SPV nodes only download the block headers and information about specific transactions. When I say information, I mean the Merkle proof of that transaction was included in a block. So they can validate proof of work because that's included in the headers, but they can't validate other network rules. They can't detect an invalid transaction has been included in the block and can't verify the money supply. So if all of the nodes on the network were using this system, except the miners who are mining, the miners could inflate money. No one would be checking them. They can verify the inclusion of transactions, and they can't verify exclusion. We don't have that kind of proof. They can use something called bloom filters to preserve a bit of privacy. They're not great. A bloom filter is my SPV node talking to a full node and saying, "I am interested in this set of transactions or this set of addresses, but I'm not going to tell you exactly what addresses." With that kind of filter, you'll always get the transactions you're interested in if the full node is honest. But the full node can't fingerprint exactly what your address is. They're not great. There are better systems out there, but this is what we have right now, in the peer-to-peer network.

A few other node options in Bitcoin Core. `-blocksonly`, does what you'd imagine. It's a full node that doesn't propagate transactions outside of blocks. It's still validating all of the rules or the full consensus rules, but it's just not propagating those transactions outside a block.

`-nolisten` means that you won't accept incoming, inbound connections. You'll make outbound, but you won't listen for inbound connections. You can connect over Tor. That preserves a bit of privacy, perhaps using the `-onion` option, you can connect over a proxy. Then the concept for `-whitelist` which is you connecting to a node. You'll never disconnect or ban them, and you'll always propagate transactions to them. Any questions?
`
Audience Member: I think there was an article about Jameson Lopp about how many SPV nodes a full-node can serve?

John: There must be some limit on the number of inbound connections. I don't know it off the top of my head. Maybe someone else knows?

Audience Member: The total is 125.

John: 125 total connections. So you can have up to eight outbound. Those are the peers that you care about. Then they're important to you. You're expecting to get information from, and the total for outbound plus inbound is 125 apparently.

Audience Member speaks (inaudible)

John: I'm not sure this is like a canonical definition, but what I mean when I say this, it's a full node because it's validating all of the rules, but it's not a pruned node. It''s serving up old blocks to peers.

Audience Member: Any full-node that is not pruned is archival?

John: If it's serving blocks to its peers, yes. So pruned is a kind of full node. Archival is also a kind of full node.

Audience Member: Do archival nodes advertise as some kind of a system of record? What is the point of the status there?

John: Again, I'm just using this word archival in a vague sense. What I mean is, it will serve old blocks. And a node signals that it can serve old blocks using the NODE_NETWORK service bit in the version handshake. So when you connect to it for the first time, it will say I have node network, which means I will serve you blocks. Any other questions?

## Message Format

Let's talk quickly about the message format. Peer-to-peer messages have a header and a payload. The head is 24 bytes long. It's a fixed length, and it's got certain fields. Fixed fields. In fixed fields. It's got magic at the front. That's just 4 bytes, 4 fixed bytes saying that this is a message on the Bitcoin network. For the main net, it is f9beb4d9. It's just what Satoshi chose to identify messages for the Bitcoin main net. Testnet has a different 4 bytes leading. Litecoin has a different 4-byte magic. Bitcoin cash has the same magic, but they claim they're going to change to a different magic. 2x tries to pretend it's Bitcoin...

After the 4 bytes of magic, you have 12 bytes of a command name. That's ASCII, just saying what the command in the payload is. For example, ADDR for address message, INV for inventory version. So if you just parse out those 12 bytes, it'll just be ASCII for what the command is. Then you got a payload size of 4 bytes on how long the payload is, in bytes. That limits the size of the payload at 32 MB and then a checksum that was added in a later version, which is a double sha-256 of the payload. That's kind of a lousy network checksum, but that's what it is. So that's your 24 bytes, and then you have a payload, which is up to 32 MB, and each command has its own defined format. So that's what it looks like -- four bytes of magic, command Payload size, checksum, then the body or the payload.

So here's an example header. Those first four bytes are always the same network magic. Then you have the command name. So if you can read ASCII, you can see that hex76 is V, 65 is e, and so on. For VERACK, the payload size is always zero. There's no payload for VERACK. Then a checksum, which is SHA256(SHA256) of the empty string because the payload is zero.

Does that make sense? Pretty simple format.

## Message types

There are two really kinds of messages on the network. There are control messages, and there are inventory or data messages. Let's look at the most important control messages, and probably the most important is a version, version VERACK handshake. Every new connection on the network starts with this handshake. I connect to a peer. I send him a version. He sends me a VERACK. He sends me his version. I send him a VERACK. That's a handshake. It's used by nodes to exchange information about themselves.

What's inside a version message? There's a version it's four bytes. It's the highest version that the transmitting node can connect to, right? It's usually your version. Then there are these service bits, and that's a bitfield of the services that your transmitting node supports. So one of those services is NODE_NETWORK that says, "I can send out blocks." I'm a full node that can send blocks and transactions. There's a NODE_WITNESS, which says, "I understand what SegWit is, and I can send you witness blocks and witness transactions," and so on. Then there's a timestamp. So timestamp tells the receiving node this is what I view the time as. Nodes on the network take account of what their peers think the time is in certain circumstances.

Then there's a bunch of addr_recv. The transmitting node is saying, "I think that you support these services." "I think this is what your IP addresses and your port is," and then the addr_trans services. That's the transmitting nodes saying, "these are the services that I support, and this is what I think my address is." So that addr_trans services should be the same as the services field. Then there's a nonce, eight bytes of randomness to ensure that a node isn't connecting to itself. There's a user agent, which for Bitcoin Core is Satoshi, and then the version because Bitcoin Core is the descendant of the Satoshi client. Then there's a start_height, which is saying this is the height of my tip. This is how far through the blockchain I've advanced, and then there's this relay bool which is saying, send me INVs or transactions.

So that's what we send out when we first connect to a peer. Any questions about that?

Audience Member: If you are a node that is not accepting inbound connections, how do you received information about blocks and transactions?

John: You connect to outbound connections.

Audience Member: You are receiving from the outbound?

John: Both. You'll transmit to inbound and outbound.

Audience Member: What's the purpose of the random number?

John: To make sure you don't accidentally connect to yourself. It's weird. I don't know the history of that one. Apparently, it's to stop you from connecting to yourself.

Audience Member: What's the difference between message and transaction?

John: A transaction is a way of transferring value on the Bitcoin network. A message is a network envelope of data that you're sending to a peer.

Audience Member: Could the message contain a transaction?

John: Yes, the message could contain a transaction. I'll talk about how transactions are sent using those messages.

Just quickly spinning through the other control messages. VERACK as a response to a version, It's acknowledging that it's received that version head message. ADDR is how we gossip information about the network. So if I'm connected to some peers, I'll send out an ADDR saying these are the peers I've connected to, is how we build out our view of the peer-to-peer network. GETADDR is requesting information about additional peers. PING/PONG confirming connectivity, so I send out a ping, I expect a pong in response. Then there are these FILTERLOADs. These are for setting up the bloom filters that I told you about for the SPV nodes. I think that's it. There might be a few others, send_headers, send_compact.

To answer your question, how do we propagate a transaction across this network? Well, new transactions are announced with an INV message. That stands for inventory, which means we have new inventory to share. That contains a transaction ID. That's the hash of the transaction, excluding the witness, which is the unique identifier for that transaction. INVs can also be used to propagate blocks, but that's not so common these days. Originally, that's how blocks were propagated, but not so anymore. If the receiving node wants that transaction, if it hasn't seen it before, it sends a GETDATA saying, "Yep, send me that transaction." And then the announcing node will send a TX message, so it looks like that. Pretty simple. The transmitting node sends an INV, the receiving node wants that transaction, so it sends a GETDATA, and the transmitting node sends a TX. Make sense? Pretty easy.

## Block Propagation

That's transaction blocks. How do we propagate those? Initially, they were propagating the same way as transactions INV-GETDATA-BLOCK. In v0.10.0,  we introduced what's called headers first syncing. In v0.12.0, we introduced SENDHEADERS. V0.13.0, introduced compact blocks. V0.14.0, high bandwidth compact blocks, and all of this is an effort to make block propagation faster and more efficient. Block propagation is really important. The faster blocks propagate across the network, the lower the stale block rate, and the more healthy the system runs. Transactions, it doesn't matter if they get delayed a bit, but blocks really need to get across the network more quickly. That's why there's a parallel network called FIBRE, that Matt Corallo maintains as a way of transmitting and propagating blocks really fast -- speed of light fast.

So let's talk about some of those block propagation methods. Headers-first is where the transmitting block sends an INV for the block hash just like normal, but the receiving node sends a GETHEADERS and GETDATA in response. So it's saying, send me the headers and also send me the block. This is good because that INV could include a block that doesn't connect to our tip. It might be like a reorg going back to somewhere else in the chain. And the GETHEADERS is saying send me all the headers back to where I know about in the chain. The transmitting node sends the headers connecting the tip to the receiving node's best block and the block. So it looks a bit like that. The transmitting node sends an INV, and the receiving node says, "yep, I want those headers, I want that data," and the transmitting node sends the headers and the block.

John: Any questions about SENDHEADERS? SENDHEADERS was the next step along, and that was a new control message in v12, protocol version 70012. It's sent immediately after the VERSION  handshake. So you do your VERSION handshake with your peer, and then you say SENDHEADERS. It indicates that I want you to send me headers without sending the INV first. That saves us one round-trip, saves us the INV-GETHEADERS round trip, and that's formally defined in BIP 130, if you want to look up the definition. So after v12 that's what it looks like. So in the headers, the receiving node sends back a GETDATA and the transmitting node sends a block.

## Compact blocks

What about compact blocks? Compact blocks reduce even more than the round-trip time the bandwidth for propagating blocks, and it relies on this observation that if you're on the peer-to-peer network and you're receiving transactions and blocks when you receive the block, you've probably seen most of the transactions in that block already because you saw them when they entered your mempool. You saw them when they were propagated around before they got in a block. It's enabled in a similar way to SENDHEADERS. There's a SENDCMPCT message similar to SENDHEADERS sent immediately after the VERSION handshake, and it's defined in BIP 152.

So there are two modes. There's low bandwidth, with the same number of messages as headers first block syncing, but that saves a bit on the number of transactions that are sent in the compact block. Then there's a high bandwidth, which is for very quickly propagating blocks around the network. After your VERSION handshake, you'll tell your peer, "Hey, I'm interested in compact blocks," and when he receives a block, he'll send you the compact block headers, the shortids, and you'll say GETBLOCK. I'll talk about what those mean.

The compact block includes the header, the 80 bytes as normal, and it has shortids for the transactions, so those are 6-byte identifiers for the transaction saying, "I'm including these transactions, which I think you already have. I think you've already seen these transactions so I'm not going to send you the full serialized transaction. I'm just going to tell you this transaction was included in the block, and then the receiving node from those shortids reconstructs a block based on transactions in its mempool. If it doesn't have any, if there are some transactions missing from its mempool, it says "give me the remaining transactions" as in the GETBLOCK TXN method, and the BLOCKTXN will send those remaining transactions.

That was peer-to-peer. Any questions about peer-to-peer? That was really quick, so there's lots of detail that I skipped over.

Audience Member: What is the difference between FIBRE and this?

John: The FIBRE network sends blocks really quickly between miners. So the idea is to reduce that stale rate of blocks that don't become part of the main chain, and it uses forward error correction. It sends blocks over UDP. I don't know the technical details, but it's just a really fast way of transmitting blocks.

Audience member: Is that over the network?

John: You'd need to download and compile the FIBRE client, but I believe you can just connect to it. Again, I don't know a great deal about FIBRE.

Audience member: Is there anything being done to mitigate latency and getting around the Great Firewall of China?

John: FIBRE, I think FIBRE would do that. Probably. Again it's not something I know a great deal about.

## Mempool

I'm going to talk about a mempool. So I'm going to have to rush a bit to get through this. I'm going to talk about what a mempool is. I'm going to talk about limiting and eviction in the mempool and then like this grab bag of topics about things that connect to the mempool. Replace-by-fee, signature caching, script caching. Going to talk a little bit more about compact blocks, and then I'll touch on fee estimation. All of those topics down there somehow interact with the mempool in some way.

So what's a mempool? It's a node's view of all of the transactions which haven't yet been included in a block, unconfirmed transactions. Transactions are propagated around the network using that INV GETDATA transaction, and if you receive a transaction message with the transaction in it, you validate that, verify that it's a valid transaction, and then you accept it into your mempool. Then miners have their mempool on their nodes, and they select transactions from that mempool to include in the next block based on the fee rate. That's how they choose the best fee-paying transactions. So often, when people talk about the mempool, they talk about "the mempool." There's no such thing. A mempool is something that is on your node. Your node's mempool might be slightly different from your peers. Depending on what order you saw transactions in, but we want them to be roughly the same. You know if you've got a node on the network that's been there for a long time, we'd like you to have some kind of view of what other nodes are seeing, what transactions they're seeing. Nodes verify the validity of transactions before they go into the mempool. They verify that they are consensus valid. They'll also verify, they'll check them against standard-ness rules, which is something I mentioned before. Double spends are not allowed. If you have two conflicting transactions, the one that arrived first is the one that will stay in your mempool. Transaction chains are allowed, so you're allowed to spend from an unconfirmed transaction. You can have a chain of ancestors and descendants in your mempool. I think the default is 25 deep.

Audience Member: Miners will be providing different packages to allow, for example, for transactions for higher fees?

John: Perhaps. I'm going to talk about replace-by-fee later. But this isn't consensus.

Audience Member: I mean replace-by-fee as long as it's not a double spend attack.

John: They can do that. It's not consensus. What they include in their block is up to them as long as it's valid. But this is the Bitcoin Core, and most implementations will accept the first transaction they see. They won't allow double spends from that.

How do we limit the mempool, and why do we need to? Well, a node's mempool is a private resource. Its memory on your computer and external parties could potentially abuse that resource.

They could send you loads of transactions and fill up your mempool and potentially make your computer fall over. So we need somehow to prevent that from happening. We need to limit how much resources an external party can use on our system. There are a few ways we do that.

We expire old transactions. If a transaction has been in your mempool for longer than 14 days, it's probably not going to get included in the block. It's been sitting around getting stale. Miners haven't included it for 1,000 blocks, so we age it out. We also limit the size. The default maximum mempool size is 300 megabytes. Once we reach 300 megabytes, we won't allow new transactions in, or rather, we will start evicting the low fee-paying transactions from our mempool. Because a mempool should be about transactions which will eventually get into a block and so it makes sense to evict the low fee-paying ones first because miners probably won't include those.

The fee rate calculation is done based on a package, and when we say package, we mean a collection of transactions, parents and descendants, and ancestors. If we have a chain of unconfirmed transactions, we'll look at the fee rate for that entire package of transactions because that's what the miner is optimizing for. So if we have a transaction with a very low fee and a child with a very high fee, then a miner might include both. They need to include the ancestor because otherwise, the child is not valid. So they look at the fee rate for the entire package, and that's what we do in our mempool as well.

There's another dimension to this. There's something called FEEFILTER, and that's my node saying to my peer, I'm no longer interested in transactions paying lower than this fee rate because I won't accept it to my mempool. So I say, "I'm not interested in transactions to pay less than five Satoshi's per byte because my mempool won't accept them anyway," and that's defined in BIP 133. Any questions about that?

## Replace-by-Fee

Replace-by-fee is a way of unsticking your transaction. Say you send a transaction out to Bitcoin with a low fee or with a certain level of fee and the fee rate on blocks goes up, miners probably won't include your transaction because there are better paying transactions out there, and so it kind of gets stuck in this limbo in the mempool. Replaced by fee is a way of unsticking it. We replace the old transaction with a new version with a higher transaction fee. Like I said earlier, a miner can choose to include any version of a transaction. The mempool is not consensus critical. The mempool is not canonical. A miner couldn't choose which transaction they include, but as I said, most nodes won't allow transactions to be replaced in the mempool, in general. That's kind of the general rule.

So in BIP 125, we implemented this new feature called OPT_IN REPLACE-BY-FEE. That is saying, "I'm sending this transaction, but I'm going to allow it to be replaced later by a higher paying fee." It's basically allowing a double spend of your transaction or a replacement of your transaction to get into the mempool, but it's opt-in. You signal that you'll allow it, and you opt-in using the sequence number in one of the transaction inputs. Sequence number was the last field in that input that Jimmy talked about earlier, and you signal with a certain value in there. You're saying, "I'm happy for this transaction to be replaced later if a higher fee paying transaction replaces it."

So if the sequence number is less than 0xfffffffe, then the transaction is "replaceable." Again, none of this is consensus. This is just nodes doing what we expect them to do. Any transaction could be included in the block, but this is me signaling explicitly, saying, "I'm happy for this transaction to be replaced in the mempool." Make sense?

There are a few conditions attached to that. Replace-by-fee could potentially be a DoS vector. There's a limit to how many transactions I can send because there's a limit to the amount of money I have, and if I don't include enough fee, these transactions won't be included or won't be propagated. RBF could be used, and I could send a transaction, and I can bump the fee up a little bit, and bump it up a bit more, like saturate the network that way.

So there are conditions attached to replace-by-fee. The first condition is it has to have this sequence number lower than that. The replacement needs to have a higher fee. I can't replace it by a lower fee, so I need to keep bumping up the fee. The replacement doesn't contain any new unconfirmed inputs, and the replacement pays for its own bandwidth. So the delta between the old transaction and new transaction needs to be at least some level, some number of Satoshi per byte, 500 Satoshi, or something like that. The replacement does not replace more than 100 transactions. Any questions about RBF?

## Signature Caching

Next, I'm going to talk about signature caching. There are a few signatures, I don't know if you recognize any of those signatures. As I said earlier, transactions, in general, are seen twice if you're a fully connected node on the Bitcoin network. You'll see them once when they're broadcast by the signing user and sent across the network. And then you'll see them the second time when they're included in a block. So obviously, there's an optimization here. Rather than fully validate a transaction twice, you can partially cache the result of that transaction the first time. So when you see it in a block, you don't have to do all of that transaction validation again. It means that block propagation is a lot faster because you don't need to fully validate all of the transactions in the block.

Signature validation, that ECDSA stuff that Jimmy talked about earlier where you're validating an ECDSA signature that's really expensive. You've got to do a lot of elliptic curve additions, and it takes a long, long time, a lot of computing power. So, each transaction input usually includes at least one signature. Instead of evaluating those signatures twice just keep a cache of those signature validations evaluations and that was added in a Bitcoin Core quite a long time ago 0.7.

## Script Caching

There's a new, better version of script caching. Instead of just caching the signature validation,  in script caching we cache the validity of the entire script in input. Because a Bitcoin script is context-free, if it's true now it'll be true forever, independent of any contextual information. So we cache the validity of the entire script sig evaluation, and that was added in 0.15, which came out in July.

Audience Member: Does script caching make signature caching obsolete?

John: More-or-less. Signature cashing is still in there as kind of an edge case, DoS protection, but this would kind of make most of that redundant. This stuff really does improve block validation times like orders of magnitude.

So why don't we just cache the entire transaction? Well, because transactions are contextual, right? The validity of a transaction depends on dates outside the transaction. A transaction could be valid in one block but invalid in a different block. For example, lock time is some kind of contextual validity for a transaction. So we can't just cache the entire validity of the transaction. Any questions about that before we move on?

So why am I talking about this now? Because obviously, this requires a mempool. It requires that you've seen a transaction before you see the block, so that's how it links back into the mempool. And you get more benefit from this the longer you've been online. As your cache fills up by seeing more transactions, by the time the block arrives, you would have seen a higher percentage of those transactions in the block. So the longer you're online, the better this cache will be functioning. Obviously, a `-blocksonly` node will not benefit from this. It's like front-loading the validation of a block because you're partially validating a block before you even see it. You're validating the transactions in that block before you even receive it.

## Compact blocks

A bit more about compact blocks, and again this will link into mempool somehow. Compact block saves propagation, bandwidth, and time as I said earlier. The way it does that is it doesn't include all of the raw transactions, the serialized transactions when it transmits a block. That's defined in BIP 152. It was introduced in, I think, in version 12 or 13. There's low bandwidth that will save on block propagation bandwidth but not necessarily on time.  And in high bandwidth, which is what really saves on block propagation time.

Why is this interesting in terms of the mempool? Well, we receive a compact block that doesn't contain all of the full transactions. The way that works is a transmitting node thinks, "this receiving node already has these transactions in its mempool. It's already seen them, so I don't need to include them in a block. It refers to transactions by a shortid. That's a 6-byte digest using this kind of this SipHash-2-4 algorithm, and then the receiving node will take those shortids and see if they map to transactions in its mempool and try and reconstruct that block itself. You're saving a little bandwidth, and potentially, you're saving time. If you're missing any transactions, if there are any gaps in your mempool, you can send a GETBLOCKTXN back saying, "I've got some gaps. Can you help me fill them in?" So that requires a mempool, right? It requires that you've got this collection of transactions already in your mempool. Any questions?

## Fee Estimation

In Bitcoin, your transactions all have fees. You're in some kind of competition with other users of the system to get your transaction into a block. The way you differentiate yourself from other transactions, the way you induce miners to include your transaction in a block, is to include a big fee -- an appropriate fee for how urgent your need is. That's how miners choose which transaction to include, and the prevailing fee rate can change quite a lot. We've seen this recently. We've seen it go up quite a bit and then down, then up. It depends on a lot of factors, but it comes down to how much demand there is for the supply of block space. So estimating how much fee you need is quite difficult. It's a dynamic system. What you do or what some people do affects what other people do. The past is not necessarily indicative of what will happen in the future. It's an estimate.

So we could use a mempool for this. We could look at a snapshot of the mempool and say these are the outstanding unconfirmed transactions. These are what I'm competing against. But there are problems with that. The expected time to wait for a block is always ten minutes. So if the last block was nine minutes ago, the expected time for the next block is not one minute. It's another ten minutes as a function of the Poisson distribution.

You don't know what's going to arrive in the next ten minutes. It doesn't account for "lucky" and "unlucky" runs. So you might have like three blocks in the space of five minutes, which would empty out the mempool and reduce the amount of fee required or you might have an unlucky run, where there are 30 minutes without a block, the mempool fills up and you need more fee to get into the block. Just looking at a snapshot does not give you that kind of depth of information, and again there's no such thing as the mempool. You don't know exactly; you have an incomplete view of the outstanding transactions.

So you can use recent blocks, and looking at recent blocks gives you an idea of how much fee was required to be included in the block. But again, there are problems with this in that it is trivially gameable by miners. The miner could stuff the block with private, high fee-paying transactions, and everyone looking at that on the network might think to themselves, "oh, I need to include a really high fee because the last broker only had high fees." So you need a bit more information than that.

So what we do in Bitcoin Core is we look at recent blocks, and we look at the mempool, and we track how long transactions stayed in the mempool, and what fee they required based on time and fee. That requires you to have a mempool. It requires you to have this historical view of what was coming into the mempool and what was included in blocks, so you need a large sample. You need recent transactions, and the longer you've been online, the longer you've seen the mempool, the better estimate you can make for fees. So that's another aspect of the mempool we use.

Thank you very much.
