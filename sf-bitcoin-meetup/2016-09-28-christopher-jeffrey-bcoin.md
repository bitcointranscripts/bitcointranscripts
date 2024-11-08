---
title: Bcoin
transcript_by: Michael Folkson
tags:
  - consensus-enforcement
date: 2016-09-28
media: https://www.youtube.com/watch?v=MGm54LZ1T50
---
Bcoin repo: https://github.com/bcoin-org/bcoin

## Intro

Hey everyone. I’m JJ with Purse. Tonight I want to talk to you about full nodes and full node implementations in general. In particular my project and the project we’ve been working on at Purse which is bcoin. A little history about me. I’ve actually given a presentation here before two years ago at the dev meetup. What I gave my talk on two years ago was actually the process of turning bitcoind into a shared object, into a library so you could link to it and call functions directly and call consensus code. It was a very small change, it was a small compile time option. A couple of line change to the config file and I submitted it as a pull request to Bitcoin Core. It rejected unilaterally by everyone. Now I’m here two years later. Since I had no options left, I wanted to do cool Bitcoin things, I wanted to have a cool library, a library that could be a full node. Since I couldn’t use Bitcoin Core I ended up writing my own full node library. Here I am two years later and I am going to present that. Bcoin, what it is, a little history about Bcoin. It was created in 2014 by Fedor Indutny. He’s a lead NodeJS dev. You may have heard of him. He was actually the guy who discovered you could steal a private key from a Heartbleed infected server, he was the first one to actually do that. He is a really smart guy. When he created Bcoin, at that point in history in 2014, I was sort of into cryptocurrency. I had been mining, I tried to mine Bitcoin and it didn’t work. I tried to mine Litecoin and eventually Dogecoin. But I didn’t really understand it. I would look at block explorers and I would see this Merkle root and I would be like “What is that thing? Why is it there? Why is it necessary?” I tried looking at the bitcoind code and I think I looked at it for about two minutes before I was like “This code is horrible. There is no way anything clever or good is in here and I gave up reading it. My friend Fedor created this simple SPV wallet in the browser called Bcoin. I was familiar with Fedor’s code so I thought I’ll take a look at it. I’m interested in cryptocurrency. The first time I read through it and I saw how a transaction verification worked. I think it was the first time I started to understand how Bitcoin worked. It was brilliant. I saw everything. The previous output script is included in the current transaction. The previous transaction ID is included in the current transaction, that affects the sighash, the current transaction ID. That’s brilliant actually. I didn’t see this in the bitcoind code because it was full of all of this s\*\*\*. I can’t read it, it is unreadable. When I saw it expressed in this simple way I was like “It is a brilliant protocol. It is a brilliant way of doing things. It is just implemented horribly.” I became a contributor to Bcoin right away. It was still a simple SPV wallet. Last year I started to rewrite it as a full node. The thing that really pushed me to rewrite it as a full node was for use in purse.io. But it is an open source project and people can use it. I think we do need alternative full node implementations. I am going to step back from Bcoin for a little bit and just talk about alternative full node implementations in general.

bitcoind or Bitcoin Core, it was the first implementation of Bitcoin by Satoshi. It is really old and it is full of a lot of old code. One thing it brings with it is actually a mentality. It brings a lot of baggage. There is this longstanding mentality that it is the only full node and it is impossible to reimplement. There’s a quote from Satoshi himself up here where he says “A second implementation would be a menace to the network.” This is actually a very popular opinion. People are very opposed to alternative implementations. Matt Corallo, as you can see there, very nearly has a mental breakdown describing his opposition to the alternative implementations. Then there is a quote from Peter Todd, he’s Peter Todd. I wouldn’t have him any other way. We have some pushback here. We have a lot of people who think this really isn’t a good idea. While their opinions do have merit I think they are very dismissive. They say it can’t be done and they haven’t really tried to reimplement it. They haven’t waited to see whether an alternative implementation can actually pull this off. They assume it can’t be done. Even Satoshi, if you read the rest of his posts, it is more that he is lazy than anything. He just didn’t want to help maintain an alternative implementation but he doesn’t say it is impossible to reimplement. He just says it is a menace.

I am going to be referring to alternative implementations as menace implementations. There are a few menace implementations out there. These are not all of them but these are the ones are maybe seen as the most production ready. There’s bitcoinj which is written in Java and it is really bad. Then there is btcd which is written in Go and it is fantastic. It is a really good project. Then there is NBitcoin, I actually haven’t played around with it much but it is the .NET stack, it is C\#. It is also really well written. Now there’s Bcoin which is Javascript. There has never really been a full Javascript Bitcoin node. There was BitcoinJS a couple of years ago. They had bitcoinjs-server which would connect to the network and try to validate the blockchain but they ran into a lot of issues with scalability, data management and things like that. The project was abandoned in 2013 but the guys who wrote it are actually really smart. I want to make that clear. The BitcoinJS guys, they do great work, but that project is now unmaintained. There is never really a good thing in Javascript to do Bitcoin with. We can ask ourselves if this opinion is so popular, its really bad to have an alternative implementation why are all these menace implementations popping up? MC8 can answer that. He points to childhood. Childhood is the reason that these menaces are created. Maybe its Bitcoin’s childhood that’s to blame for these menace implementations. Let’s look at Bitcoin’s childhood for a second. Satoshi releases a white paper, we all know that. He releases a working C++ implementation of his protocol. The implementation itself has no tests, no docs and it has global state riddled everywhere. That last part is really important because global state means that it is almost impossible to abstract things out and turn it into a library. If you have global state in the process, it is not unique to one instance. It was meant to be a process, it was not meant to be a library.

## bitcoind shortcomings (or Satoshi was not a programmer)

Here is a list of the bitcoind shortcomings. Global state, we went over that. Very poor coding style. It is already C++. On top of that you have extremely weird code and it is not very readable. It is especially not readable to beginners who want to try to understand Bitcoin. If you have never read the bitcoind code and you go and read the master branch and you can actually understand it, congratulations you are a liar. You didn’t understand it. Nobody is going to understand it. There is a very cumbersome external API especially for notifications.

## Mike Hearn was right

“Whoever Satoshi was, he showed no familiarity with post-1995 software development techniques and that includes a complete lack of any unit tests and therefore a testable codebase. Any modern implementation should do better… You cannot currently build fake chains or inject test messages and get the responses back. Making Core a fully testable codebase is a big job that nobody has really tackled even after five years.” Mike Hearn (2014)

I just want to say Mike Hearn was right on one thing. In 2014 he had this BitcoinXT thing, he wanted to implement this new message on the network layer called `getutxos`. Light nodes, like SPV nodes, don’t usually have access to the full UTXO set. The UTXO set is pretty important because you almost can’t do anything interesting in Bitcoin without the UTXO set. You can’t verify transactions, you can’t see the value that is being redeemed. Wouldn’t it be nice if these light nodes had a way to ask the network for UTXOs. That way they don’t have to maintain an entire blockchain. It sounds good on paper but it is actually a really bad idea because right now there’s no cryptographic proof for UTXOs so you have no idea whether a node is lying to you about values or scripts or anything like that. When this blew up in his face and he didn’t write proper tests for this implementation, it ended up being a DOS vector he was overly defensive about it. He didn’t just admit that he was wrong. He was basically a total a\*\* about it. He said one thing that was totally irrelevant but made perfect sense. It was irrelevant but it was absolutely true. He made a really good point there. I wish more people would point this out. It is a shame I have to quote Mike Hearn here. I wish somebody else said this but I have to say he’s right.

## Nowadays things are better?

That was 2014. Nowadays are things better? What has changed? Tests, there are lots of unit tests and things like that. There’s actually really good docs on the Bitcoin protocol in general. It explains a lot of how it works. There is libbitcoinconsensus. The goal of libbitcoinconsensus is to move a lot of consensus functions out of Bitcoin and into a library so you can just link to it, call these consensus functions and you don’t have to worry about compatibility with consensus. The problem with that is that it is just the scripting system. It only handles a small part of what Bitcoin consensus is. There is a lot of other stuff that you need to check. It is a step in the right direction but in practice it is probably not that useful until more functions get in there. There is a more fleshed out API, more RPC calls, there’s a REST API now. What hasn’t changed is that there is still global state all over the place. There is this insane system of locks you have to use to access the coins. Am I right roasbeef? Code insanity hasn’t changed. Notifications, there is still really not a good way of doing notifications. There is a wallet notifier argument you can pass in which will spawn a child process every single time a transaction comes in. While that’s a really UNIXy way of doing it it is also a really ugly way of doing it. It is really slow and an inefficient way of doing things. There’s some ZeroMQ notifications too. And it is still written in C++ unfortunately. That hasn’t changed.

## Sample bitcoind code

https://youtu.be/MGm54LZ1T50?t=821

If you have a weak stomach you may want to look away. Here’s some sample bitcoind code. This is SegWit code. What this function is doing is it is looking through a coinbase’s output to define the commitment output. The commitment output is a special thing you need with SegWit. There are two problems with this function. One is that if statement is 354 columns. It is wrapped here but it is on a single line. You notice that the for loop doesn’t actually break when it finds the commitment position. That means that every commitment position before it is actually ignored. That’s a weird way to write it. You might want to start backwards and go back and break when you find one. It is not immediately obvious what it is doing to somebody who wants to reimplement this code. I want to clarify. This is Pieter Wuille’s code. I actually love sipa, I love SegWit, it was a lot of fun to implement. I think he’s a really smart guy and a really smart programmer. This is just the example that came to mind when I wanted to show how horrible the bitcoind code is. This is not the only example. I don’t blame Pieter Wuille here, I blame the overall coding style of the project. If you look at Pieter Wuille’s project, libsecp256k1, the code there is brilliant. I think there is some spell that Bitcoin Core has over people that when they contribute to it they just write really ugly code. So let’s make something better. Something more readable, more hackable, more maintainable. How do we do that?

## Hard parts

There are some hard parts to doing this. First is the vastness of Bitcoin. There are a lot of different things happening in Bitcoin. There are a lot of different features. The second is the complexity. Not only are there a lot of different things happening, these things that are happening are actually very complex and very hard to understand. The third thing is data management and scalability. People probably don’t realize how much data management Bitcoin actually is. There are tens of millions of transactions, hundreds of thousands of blocks. It is an insane amount of data. You really, really have to focus on data management. If you work on a Bitcoin full node it will get you interested in databases because you have to find the most optimal solution. The fourth, the really tough guy, is consensus, agreeing on all consensus rules. The fifth thing is transaction relay policy which is sort of like consensus but not as important because you are allowed to get it wrong, if you screw it up a little bit. I have a really cool quote by Al Pacino there.

“You’re not a programmer anymore. You’re a bitcoin dev now. You’re on the other side: whole new ballgame. You can’t learn about it in school… and you can’t have a late start.” (Al Pacino)

It makes sense. You can’t learn about it in school. You can’t learn about Bitcoin in school. You just have to dig into it. I sort of explained vastness and complexity. Let’s start with data management and scalability.

## Data Management: Coins Everywhere

So data management in Bitcoin, there are coins everywhere. When I say coin I mean UTXO. I call UTXOs coins because I think UTXOs are a really ugly acronym and coins makes more sense. Coins are the heart and soul of Bitcoin. There are currently 40 million coins in 11 million unspent transactions. This is a problem. We need to store all these coins. We need to index them in some way. But every key in a database can potentially make another key lookup slower. Coins also generally need to be cached in memory for fast access. They need to be future proof because we don’t want to have a giant migration if we need something else, another piece of data in the transaction. They also need to be compressed. Unlike the actual blocks in the blockchain the UTXO set cannot be pruned. It can be pruned when you’ve spent the coins, you delete those. But you need to maintain a full UTXO set. Blocks you can prune, you only need to keep the last 288 blocks. But the UTXO set, you need the whole thing. It is in our best interest to keep it compressed and keep it as small as possible. If the UTXO set became 80 gigabytes, it will one day, it would be almost pointless to have a full node that is pruned because you still need the UTXO set. Indexing, UTXO ID vs TXID. I was going to explain to you why BitcoinJ is horrible and this is why. There is a UTXO ID thing and it is the hash of the transaction plus the index of the output. That’s the way BitcoinJ indexes coins. That means BitcoinJ has 40 million keys in the database for the UTXO set. The other way to do it is store it by transaction ID. This is a really cool thing about Bitcoin which not too many people know about. This is why I wanted to share it with you. There is a fundamental primitive data structure internally, used in internal implementations of Bitcoin that are sort of a coin serialization. They are very similar to a transaction but they only contain outputs and the version and usually a coinbase flag and some other things. This thing is found everywhere internally in Bitcoin implementations but not many people are familiar with them because they don’t show up on a block explorer. They are not external. That’s the way you store, under the transaction ID but you only store the outputs. You delete the outputs once they are spent. The blockchain when it can’t find an output it just assumes it is double spent. There is another thing that BitcoinJ doesn’t do. There is something called a Coin Viewpoint. This is also an important internal data structure in full nodes. A Coin Viewpoint is a snapshot of the entire state of coins as they pertain to a block. That block could be getting added to the chain or it could be getting disconnected during a re-org. Some of the coins in it could be spent, some of them could be unspent. It is a really necessary thing to have. I wanted to point this out. This is what you need to do if you want to make a full node and BitcoinJ doesn’t do this. If we can get all this data management down what is next?

## Blockchain vs Mempool

It is blockchain and mempool. The blockchain is very neat and organized. Everything comes in in order. It is easy knowing whether a transaction exists or not on the blockchain. If it is not on the blockchain it doesn’t exist. The mempool is in many ways trickier to implement than the blockchain. I call the mempool the Wild West. There are orphan transactions and in those orphan transactions, the transactions they’re redeeming, we actually can’t check whether those transactions exist or not. We can’t check to see whether we simply haven’t seen a transaction before or whether that transaction is just non-existent. It is really weird to deal with. You need to store orphans when they are come in and hope they get resolved eventually. If they don’t you need to drop them out of the mempool. In the mempool malicious transactions are more common. It is not very easy to forge blocks and craft malicious blocks because nodes always verify the headers first. It is very hard to fake, even headers, it requires a lot of effort. But in the mempool it is really easy to forge transactions. The next thing that is hard about the mempool is these transaction relay policies. Like I said they are not consensus rules so you are allowed to get them wrong. But they are still very hard to implement. They are very tricky. Because they are stricter than consensus rules they are easier to get wrong.

## Consensus (Lockstep)

So consensus like Satoshi said, lockstep. In Bitcoin bugs become consensus rules. That is because we’re not Ethereum. It sounds like a joke but I’m dead serious. We don’t roll back history and hard fork because we find a bug in the protocol, much less a bug in a single script. We have integrity, we just live with it. It becomes a consensus rule.

## Example of a consensus edge case

One of my favorite examples of this, just to explain how weird this, something Peter Todd brought to light on the dev mailing list two years ago. This is one of the coolest transactions ever sent. It only exists on the testnet blockchain but the first funding transaction that sends to something, if you look at the first output you can see it is regular 2-of-2 multisig but it has some other stuff before it that is kind of strange. The transaction that redeems from it, Transaction 2, Input 2 is redeeming from Output 1 of Transaction 1. That just looks like a regular multisig input. But if we go back and look at Output 1 from Transaction 1 we notice there is a signature in it. If you look at it closely that signature is actually valid. We have a valid signature for the next transaction in the previous transaction output. If you know how sighashing works you should know that this is logically impossible, sort of a hash collision. It is not possible so what the hell is going on? Why is there a valid signature in the first output?

## Chicken or egg

There is a chicken or egg problem. A signature is basically a hash, like an encrypted hash. How can you have a hash for the next transaction in the previous transaction? In the original Bitcoin implementation, there are different sighash types in Bitcoin. Everyone is used to SIGHASH_ALL but there is also a SIGHASH_SINGLE, sighash types hash the transaction differently when they are creating signatures. So what SIGHASH_SINGLE does is it only signs the output at the current input index for the signature you are creating. But the question is what happens when the input index is actually higher than the number of outputs? As I showed here before, there are two inputs in the second transaction. But there is only one output. So when it does SIGHASH_SINGLE on the second input what happens? This happens. It returns a `1` but this function is returning a `uint256` which is a SHA256 hash. When it returns a `1` it gets cast to `uint256`. This is one case where explicit typing actually hurts you more than it helps you. If you write this in Javascript the code would just throw it but in C++ it actually ruins consensus rules. Because of this, this results in a predictable signature hash of `0100000…`. We actually know what the hash is ahead of time regardless of what the hash of the next transaction is. Even stranger is that there this `FindAndDelete` thing. Whenever a CHECKMULTISIG happens, the way Satoshi originally wrote it, is that `FindAndDelete` gets called on the signature being verified. It goes through the previous output script trying to remove the signature from that previous output script. For a long time people thought that code would never get called and had never been called on the main chain. How could a valid signature be in the previous output script? What is the purpose of this? People were probably right. This should never get called. But because of SIGHASH_SINGLE we can actually have signatures in previous output scripts. They will go back and remove these signatures from the previous output scripts. If you look back at this transaction it is a multisig transaction. There is another regular SIGHASH_ALL signature in the input. When that signature is created you need to take into account that the signature in Output 1 from Transaction 1 is actually going to be dropped from the script when it is signed. That is one thing you need to take into account. All the other signatures need to take that into account. The signature is actually reserialized as it is passed into `FindAndDelete`. You notice it is passed into the `CScript` constructor. It is changed to a single push data. If the signature in the previous output script is not the same push data it won’t get removed. You also need to account for that. You need to get this down byte for byte exactly or you will get forked off the main chain. Some of these opinions that it is impossible to reimplement a full node, like I said very dismissive but they sort of have some merit. This is just insanity. If we can get that right maybe we can move onto transaction relay policy.

## Example Policy Edge Case (the recent rejects problem)

Here is an example policy edge case. Recently it was discovered after SegWit was merged in that witnesses can be mutated. A bad actor on the network can mutate a witness and give a really big witness or an invalid witness and cause validation to fail on some level and get passed into this recent rejects filter thing. A recent rejects filter is a bloom filter that keeps track of all the transactions that have been recently rejected so you don’t re-request them. It tracks by regular transaction ID which is the problem and not witness transaction ID. If somebody mutates the witness it doesn’t change the regular transaction ID. Somebody can take your transaction, alter the witness and your transaction gets added to the recent rejects filter. It effectively censors the transaction until the next block. The recent rejects filter gets reset every block. There is a crappy naive solution in Bitcoin Core right now. Johnson Lau’s solution is `IsBadWitness` which is a good solution. It checks for standardness of the witness vectors and whatnot. But at the end of the day you have to get relay policy right. It is a whole bunch of nonsense and a whole bunch of work. A lot of things you need to focus on getting right. If we can do all of this, if we can get past this and reimplement consensus and policy we now have a framework to actually build a good Bitcoin library on top of.

## Bcoin

That moves me onto Bcoin. I know it is really boring but that is the kind of stuff I have been doing for the past year. I have been obsessed with it. I think I did a good job of reimplementing it and thinking about how to reimplement things. This is Bcoin. These are some code examples. This is what Bcoin looks like when you require it. We can create a blockchain technology for your blockchain app. You notice there is no global state here. You instantiate a new blockchain and you can get the genesis block and whatever. There is no global state so everything there is self contained within that instance of the blockchain object. That is really handy. Bcoin itself only has two required dependencies by default. There is no left pad stuff going on here. You guys are aware of that whole drama? There are only two dependencies. You don’t even need a database. By default Bcoin will actually create this blockchain in memory. You can create hundreds of these things. You can have them on different networks, you can do whatever you want. Syncing the blockchain, you notice you pass the chain into this `pool` object. The `pool` is the peer-to-peer pool, it is the network pool of peers. Then you can start to sync. What is important about this is that these two objects are not by default tied together. You don’t instantiate them together. They are totally separate. You can have a blockchain without a peer-to-peer pool. You can have a peer-to-peer pool without a blockchain. You can actually have a mempool without a peer-to-peer pool. You can have a wallet database without any of that. It is all loose coupling. It all works on its own.

## Loose Coupling-tying these together via proxying events

The way we deal this is that we have all these objects, like peer-to-peer pool and blockchain. They are just all tied together by this full node object that Bcoin has. The full node code in Bcoin is actually very small. It is just a proxying of events and tying all these different objects together. Whenever the `Pool` receives a block it notifies the `Chain`. Whenever the `Pool` receives a transaction it notifies the `Mempool` and so on. You can notify the `Websocket Server`. We have web socket events in this system and it is all very uniform, it is all very clean. It is very easy to reason about.

## Javascript, why?

A lot of people ask this question, why Javascript? First of all I want to say Javascript may not have been a totally conscious decision in Bcoin’s design since it was already written in Javascript when I got involved. I actually think it is a better language than most people probably think it is. It is faster than you think. It is actually pretty damn fast which is surprising because Javascript is such a dynamic language. On benchmarks it can’t compete with say Go, it can maybe come close in select benchmarks. It will beat the hell out of Ruby or Python.

Q - Is this a JS subset?

A - No I’m just talking about Javascript, V8 Javascript.

The other benefit is Javascript is ubiquitous, it is everywhere. Everyone is familiar with it, everybody has seen it at some point. It will run in a browser, on the server, on your laptop, on your phone. No other language platform can lay claim to that except for Javascript. Bcoin actually runs in the browser. You can sync a full node in the browser and it will store the blockchain in IndexedDB and it will do full validation in the browser and maintain a mempool and everything. The drawbacks to Javascript is that there is no 64 bit number types. I think this is one of the biggest problems with Javascript. It is a huge pain in the ass. You need to sort of hack ints into the language. Javascript only has double floats. We have to figure out some way to deal with that. Javascript is only single threaded. You have asynchronous jobs or functions that are asynchronous by default but there is no convenient way to put something on another thread and use it asynchronously. We have to figure out a way to deal with that. A third one is people aren’t used to writing real code in Javascript. They are used to spinning up NodeJS and serving a web page, hitting MongoDB and serving another web page. Then in the browser they are just using Angular and React. It is not even Javascript even more. Not many people actually know Javascript. At least not the kind of Javascript that Bcoin is written in. They are familiar with it but we need to introduce more real code into the ecosystem to get people thinking about Javascript more deeply.

## Solving the drawbacks

We can use a lot of trickery to treat doubles as though they were ints. It is possible. It is time consuming but if you know how ints work and you know how doubles work you can actually make Javascript behave as if it has ints. Precision loss, double floats lose precision at 53 bits. This is actually pretty lucky because `MAX_MONEY` in Bitcoin is only 51 bits. A 51-bit-max plus a 51-bit-max, the highest it can be is 52 bits. We can check for value overflows in consensus code the same way Bitcoin Core does and the same way any consensus implementation would do. We are adding up output values, we just check that the first output value is less than `MAX_MONEY` and we check that the second one we are going to add it to is less than `MAX_MONEY`. We add them together, we check that the result is less than `MAX_MONEY`. That works because we are never going to get a result higher than 52 bits and lose precision, potentially have a bad comparison. Javascript is single threaded, we can solve this by using worker processes in NodeJS and web worker threads in the browser. It actually works pretty well. If you have four cores you can spin up four worker processes in NodeJS and you can verify four transactions at the same time. A block comes in, you can parallelize transaction verification. For the not much real code in JS we need to make Javascript great again. This is what Bcoin is trying to do and this is also what Ryan X Charles at Yours network is trying to do. We are going to make Javascript great again. We need to get some real code back into that ecosystem. It can’t all just be Angular and React and MongoDB, all this BS.

## Example

I would like to show you how some of this works in Bcoin. I am going to go into the NodeJS REPL and I am just going to require Bcoin and do some things with it.

`bcoin = require(‘bcoin’);`

`chain = new bcoin.chain();`

I can instantiate a blockchain just like that and that’s in memory because I haven’t selected a database. If you look here you’ll notice that it is just stored in a read block tree in memory.

`chain.open()`

`chain.db.db.db`

I can just request the genesis block from the chain database.

`chain.db.getBlock(0).then(console.log);`

There we have the genesis block. Like I said we can start up a peer-to-peer pool. We can pass the blockchain into it.

`pool = new bcoin.pool({ chain: chain });`

I am going to bind to their events so we don’t get spammed.

`pool.on(‘error’, function() {});

Now we have this pool thing and it is tied to the chain we can open it.

`pool.open();`

We can start the blockchain, first we connect. When you connect it doesn’t try to sync the blockchain or anything. It just starts requesting transactions and things like that. We don’t really have a mempool so it is not actually relaying transactions but we can request transactions perfectly fine. All these messages will be emitting transaction events on the pool.

`pool.connect();`

`pool.logger.level = 4;`

Now we can start the blockchain sync.

`pool.startSync(); pool.logger.level = 4;`

Apparently we don’t have a good peer here. I don’t have a connection, there it goes. There we are syncing the blockchain. That is all stored in memory, probably not good to sync it too much. I’lll turn these logs off real quick. That’s how easy it is. We can start up transactions.

`bcoin.tx();`

We can create mutable transactions. We can add inputs and outputs.

`bcoin.mtx().addInput(new bcoin.coin()).addOutput({ value: 100 });`

I actually don’t have any funds right here so I can’t show you sending a transaction but I will show you receiving a transaction in a second. I have the main chain synced on here, on Bcoin, so I am going to start that up now.

`bcoin --prefix ~/.bcoin_good/ --no-auth --use-workers`

It is just a simple command line. Here we are. We are on the network. Bcoin, one of its goals is to have a nice API. But another one of its goal is to be compatible with bitcoind. It includes a legacy JSON-RPC system. We can do things like `getblockchaininfo`.

`bcoin rpc getblockchaininfo`

We have the same output we receive from bitcoind. We can do `getpeerinfo`.

`bcoin rpc getpeerinfo`

There is also a new school API aside from just the RPC because we don’t want to clone bitcoind completely because that is what we are trying to get away from. The new school API is accessible through CLI. We can access the primary wallet and we can ask for the balance for example.

`bcoin cli wallet get`

Bcoin’s wallet is a BIP 44 wallet. We can look at that. We can see the address and the token and the current receiving address. One of the things I would like to do just to prove to you guys that this is a real wallet and a real node, I would like to send a transaction to myself. I should have done this on testnet. If someone can actually import that and rescan the chain that quickly I would be very impressed. It will return the mnemonic to you by default if it is not encrypted. It is probably good to encrypt your wallet, I didn’t learn that lesson.

`qrencode “insert_receiveAddress”`

If anyone wants to send me money though, here’s the QR code. Anyone want to send me a tip for having a really good talk? We can watch the events here.

Right there we can see an incoming transaction for 1 wallet and another incoming transaction. Thank you whoever that was. More people want to send me money? All this money is going to get stolen in a second. You can steal back your money if you want. We can look at the history.

`bcoin cli wallet history`

We got three transactions from you guys. That’s pretty good. If anyone wants to steal this, this is the amount of coins you’ll get.

`bcoin cli wallet balance`

I am going to move that out as soon as I stop working on this. That’s Bcoin right now. I hope I have made my point that it is actually pretty easy to use. You can even go into the NodeJS REPL and just create a blockchain.

## Bcoin Features

The other kind of cool thing is right now Bcoin has a lot of features. It is up to date with a lot of the latest BIPs. Versionbits, SegWit, compact block relay. But one of the really cool things it supports that nothing else supports right now is BIP 150 and BIP 151. Those are the peer-to-peer encryption and peer-to-peer auth BIPs. I think they are really necessary for Bitcoin. Bitcoin should ideally have had it from Day 1. Lightning has it from Day 1 but Bitcoin does not so it is great to get that into Bitcoin right now.

Q - Are you proposing features to Bitcoin Core?

A - Not right now. I don’t have any good ideas right now. I am more about reimplementing it in a sane way. But I’ll keep my eyes open.

Q - Do you have more CLI output choices?

A - You want to see more RPC commands? One of the nice features that could be added to Core would be web socket support. At the same time I almost feel like maybe it doesn’t belong there. You would need to decide on a protocol for doing it. Right now Bcoin uses Socket.IO events which is a pretty simple protocol. It would be nice to have something slightly more low level in Bitcoin Core. That would be a pretty nice extension to Bitcoin Core. Maybe more extensions to the REST API too. Right now it is just all RPC where you pass into parameters as a JSON array. It is very annoying to curl it for that reason. It is not very usable on the command line for that reason.

Now that we have a Bitcoin full node in the browser we can also do other cool things like Layer 2 things. Right now Bcoin has the start of a Lightning implementation on top of it, it is called Plasma. It is meant to be lnd compatible. Right now it can connect to the network and do the initial handshake and send a single funding request. But the data management isn’t quite there yet and I hope to get it there in the future because Lightning is very cool and it is very fun to work on.

## Coming soon starring Roasbeef and JJ

This is a movie (Menace II The Network) that me and Roasbeef and going to star in. It is called Menace 2 The Network, it is like a sequel of Menace To Society.  The movie was inspired by Satoshi’s quote.

