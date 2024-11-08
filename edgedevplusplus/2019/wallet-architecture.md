---
title: Wallet Architecture in Bitcoin Core
transcript_by: Bryan Bishop
tags:
  - bip32
  - wallet
  - bitcoin-core
speakers:
  - John Newbery
date: 2019-09-09
aliases:
  - /scalingbitcoin/tel-aviv-2019/edgedevplusplus/wallet-architecture
---
<https://twitter.com/kanzure/status/1171018684816605185>

## Introduction

Thanks Bryan for talking about HD wallets. I am going to be talking about wallet architecture in Bitcoin Core. Alright. Who am I? I work on Bitcoin Core. I've been writing code on Bitcoin Core for about 3 years. Lately I have been working on the wallet. I work for Chaincode Labs which is why I get to work on Bitcoin Core. We are a small research lab in New York. There's also the residency program that we run. We just finished our last residency recently.

I also work on Bitcoin Optech which is a project to help open communications between the open-source community in bitcoin and bitcoin businesses. We have a weekly newsletter. If you're not subscribed to that, then I recommend going to bitcoinops.org and doing that.

<https://www.johnnewbery.com/walletdev/>

<https://gist.github.com/jnewbery/93f89b6062d7af932d92204fa04ebe70>

## Why do we care about wallet development?

Who here cares about bitcoin protocol development? If you haven't put your hand up, you're probably in the wrong room. Who here runs a bitcoin wallet? The bitcoin network consists of transactions and blocks. We're interested, as people, in addresses and ownership of coins. In the bitcoin protocol, there's no such thing as ownership, balances or addresses. All there is, are UTXO state transitions. Wallets are an abstraction on top of this that gives us the concept of addresses, balances and the concept of ownership. So it's how we as people use bitcoin.

Wallet development informs protocol development. If you think about recent proposals to change bitcoin, like taproot, sighash noinput or sighash anyprevout-- these are all informed by what wallets can do. Taproot-- who here has heard of taproot? Okay, most of you. One of the central design decisions in taproot, the taproot assumption is that, for contracts, if all parties agree to that contract and the conditions are fulfilled, then they can sign a single signature. Well that depends on MuSig. But that's not part of the bitcoin protocol, it depends on the wallet. Same with SIGHASH\_NOINPUT. A lot of the discussion around NOINPUT is about how to make protocol changes safe for wallets.

My reason for thinking that wallets are important is tha tif you want to know about the bitcoin protocol and be a bitcoin protocol developer then you need to be a wallet developer.

## What are a wallet's functions?

People aren't often sure what is meant by the word "wallet". What does a wallet do? It first of all manages your keys. With private keys, you can sign transactions. With private keys, you can create public keys that you can use to give out. The wallet needs to be able to manage those keys somehow. The wallet also needs to be able to construct transactions. If I want to create a transaction and broadcast it, my wallet does that for me. Also, a wallet needs persistence. People using bitcoin need state to persist for months or years. You probably want to save your wallet state to disk, and a wallet does that. Wallets tend to have user interfaces and advanced interfaces like coinjoin or lightning or it might interface with a hardware wallet.

I am going to only talk about key management, transaction construction, and persistence.

## Key management

What do I mean by key management? If I have private keys, I need to be able to identify which transaction outputs on the blockchain belong to me. My wallet might be watching the chain. How do I figure out which transaction outputs I should care about?

I also need key management to generate new addresses. Also, I need to determine how to sign a transaction when I want to spend a coin.

## Transaction construction

I need to parse addresses and turn them into a scriptpubkey in a transaction output. My wallet does that for me. I also need to do fee estimation and my wallet does that for me. I also need to do coin selection, picking which coins to spend. I need to sign inputs, and then send it out to the network. Well, maybe I want to batch payments, or use replace-by-fee (RBF) or child-pays-for-parent (CPFP).

## Wallet persistence

Well, I want persistence because if I lose my keys I lose my coins. I want to be able to spend UTXOs/coins. Also, I'm interested in storing my transaction history- the whole thing, all the credits and debits. Also, there's metadata I want to store as well, like labels. How far the wallet should scan into the blockchain. The birthdate of a key generation event is useful so that I know not to look for earlier transactions before that date.

## Agenda

I'll go over a quick glossary, and then talk about interfaces of the Bitcoin Core wallet. When I'm talking about a software component, I find it's helpful to talk about edges and how it interacts with other things. I can talk about how the code is managed. Then there's key management, transaction construct, persistence, and finally what might happen in the Bitcoin Core wallet in the future.

## Glossary

In Bitcoin Core, CPubKey is a public key. It's a point on the secp256k1 curve. It's what we use to create outputs. So I want someone to send me coins, so I give them an address generated from my public key. Also, this is used to verify signatures.

There's also a CKey, and that's a private key. In bitcoin, a private key is a scalar. It's used to sign transactions.

CKeyID is a key identifier. It's RIPEMD160(SHA256(pubkey)). This is a hash digest of the public key. This is used in pay-to-pubkeyhash p2pkh and pay-to-witness-pubkeyhash p2wpkh.

CTxDestination - a txout script template with a specific destination. There could be no destination, or a TX\_PUBKEYHASH destination, or CScriptID for TX\_SCRIPTHASH definition (P2SH). And so on. These are templates. When my wallet watches the blockchain, it tries to fit all of the transactions to match one of these templates to see if it recognizes anything.

There's a GUI, the node which connects out to the bitcoin blockchain, and then there's a wallet. There's interfaces between the wallet and the node, like the ChainImpl. The wallet and the node-- that's called WalletImpl. There's notifications passing between these different components.

WalletImpl is the node-wallet interface. The wallet holds a ChainImpl interface to call functions on the node for things like submitting things to the mempool or blockchain processing. The node notifies the walle tabout new transactions and blocks through the NotificationHandlerImpl interface. This is an implementation of CValidationInterface. This is how the wallet hears about transactions added to the mempool, or if a block is connected or disconnected, it's all sent out over the CValidationInterface.

Why all of this separation? It didn't use to be this way. It all used to be in the same file basically. There were direct function calls between the wallet and the node. This is no longer true. In the past year, it's been separated out. A well-defined interface is easier for us to reason about. There are now no functional calls between the node and the wallet. By doing it with separate interfaces, the wallet and the node can be tested in isolation from each other. Future work might separate the wallet into a different process so that it has its own memory. If your node gets compromised, then you're not necessarily leaking the memory of the wallet. There's also the possibility of different wallet implementations getting plugged into your node implementation in the future.

Here's src/wallet/ in the Bitcoin Core code base.

## Code layout

coinselection.cpp|h is the coin selection algorithm, branch-and-bound.

crypter.cpp|h - for encrypting the wallet's private keys

walletdb.cpp|h - interface to wallet's database for persistent storage

init.cpp - initializing the wallet module

load.cpp|h - loading/starting/stopping individual wallets

rpc\*.cpp|h - wallet's RPC interface

wallettool.cpp|h - a standalone wallet tool binary that you can run offline

wallet.cpp|h - EVERYTHING ELSE

It used to be that wallet.cpp had evertyhing but we've split it up over the years to make it more modular. But there's still a lot still in that wallet.cpp file.

Also, there's a subdirectory for tests.

If I do a line count on all of the files, the big files are wallet.cpp with 4534 lines, and a lot of the RPC files have a lot of user documentation and boiler plate code but there's still a lot of code in there. All the other files are quite small.

The RPC server is running in the same process as the node. There's a PR to separate it into a different process. At least some people would like to see that.

## Key management

I talked about key management, transaction construction, and persistence. Let's get into those for a bit, and then we can have a discussion.

One of the things that wallets need to do is identify which transaction outputs the wallet cares about. CValidationInterface notifies the wallet of new transactions and blocks. The wallet needs to decide which transactions are of interest to the wallet. This same interface does zeromq interface, net processing, and other activities. This gets fired off, we go into the wallet, and the wallet uses SyncTransaction and AddToWalletIfInvolvingMe().

IsMine() is where the magic happens. IsMine() is where I decide whether the transaction output is mine. It does that by matching the output template against our private key and whether the private key can be matched with the output template. There's some problems with this. Pattern matching is very complex, and it's not very efficient. It's trying to match different patterns on every single transaction output. It's not selective-- if I only want to receive coins to a P2WPKH output, I would also pay to --- we can't select whether it's one or the other at the moment. The solution to this is to use wallet descriptors or output descriptors. It's currently a pull request in Bitcoin Core to change the IsMine logic to match on the key output script type instead of the pattern matching.

## Generating keys

Originally, Bitcoin Core just generated a bag of keys. Fine. Is there a problem with that? Yeah, backup is a problem. Imagine that I want someone to send me bitcoin. I generate a new private key, create an address, give it to them, they send coins, and my node crashes before I make a backup prior. If I don't have a backup of that new private key, then those coins are gone forever.

The solution to this is keypool which was added by Satoshi in 2010. This caches ahead. It creates 100 cached private keys and then you back that up. When a new key is needed, you draw from the keypool and then top-up the keypool. This needs to be backed up as well, if you go beyond 100 cached private keys used since the last time you backed up.

Yes, the wallet checks all outputs and matches those. You could ask the sender to give you the bitcoin address, which is actually how the early version of Bitcoin Core worked with pay over IP address.

Q: What about connecting to hardware wallet devices? Which part communicates with the hardware wallets?

A: So, there is a separate project called HWI (hardware wallet interface). That's not part of Bitcoin Core itself. It's contained under the bitcoincoreorg but it's a separate project. It's a python executable that communicates using the RPC interface with the wallet.

Q: Does it swap out the wallet portion? Is there a separate wrapper?

A: It's a small separate program here that talks both to a hardware wallet and also the Bitcoin Core wallet here. The terminology is confusing here. I'd call this a wallet, and the Ledger or Trezor is a key signing device. The hardware wallet doesn't implement this software wallet really. The public keys are stored in the software wallet as watchonly and the private keys are in the hardware device.

## HD wallets

You now know exactly what HD wallets are and how it worked. It was only in 2016 that a minimal implementation of HD wallets was added to Bitcoin Core so pretty late compared to bip32. The way it works is that a new HD seed is set on the first time the wallet is run or after upgrading from a non-HD wallet. The good thing about HD wallets is that the backup problem no longer exists. If you restore an old backup, you don't lose the future keys because you fcan generate them deterministically from the seed. However, you might not know how far to look ahead and that's called the lookahead problem or gap limit. You're generating the public keys in this HD chain, but you can re-generate them later from an old backup.

For HD wallets, new keys are derived using the bip32 HMAC derivation scheme. For non-HD wallets, we use strong randomness to generate new keys or top up the keypool. In both cases, we test the new key by signing and verifying a message because the last thing you want is some crazy cosmic ray to cause a bit flip error which might happen. And we also save the key to the database before using it, and flushing it to the disk before using it.

Q: Is this standard practice and...

A: It should be. I don't know, I haven't looked at the source code of other wallet implementations.

Q: Can I import a bip32 key to just have a watchonly wallet?

A: Yes. That's also an example of what HWI is doing. It imports the keys as watchonly keys in the Bitcoin Core wallet and keeps the signing keys somewhere else.

Q: There's just one part, one time fresh entropy injection.

A: Correct, that's the seed.

Q: So if in the past, if I use a bad random number generator, then it's game over. But the 100 key pool with freshly generated entropy, it could have been compromised in the past--- so how do I compare these two?

A: Potentially. But if your random entropy generation is compromised at some point in the past, it might still be compromised now. I compare your argument to saying, well, I should have a separate hardware wallet for every single one of my UTXOs. Maybe. But that seems inefficient and very difficult to manage, and you'll probably lose some of them trying to manage all of those different things.

Q: ...

A: Yes. It's a single seed where everything is derived from.

I am going to rush a bit.

## Constructing transactions

When I want to construct a transaction, I take the public key and convert it to a scriptpublickey. As a user, we do that through the RPC or GUI. The RPC commands are sendtoaddress, sendmany, createrawtransaction, decoderawtransaction, fundrawtransaction, and signrawtransaction, and also submitrawtransaction for broadcasting.

So how do I do that? I put an address into my wallet, the wallet decodes it into a CDestination. Other parameters can be added for adding finer controls. I could signal that this transaction as bip125 replace-by-fee, or what fees I want to attach and so on. The wallet creates the transaction with CreateTransaction.

When creating the transaction, we need to estimate the fee. In Bitcoin Core, we're watching transactions come into the mempool and see how long it takes them to get into a block. So from that we can infer what fee rate we need to reach a certain amount of time to get a confirmation. This is in GetMinimumFeeRate and estimateSmartFee interface.

Q: What if I want to send just 1 satoshi for the whole transaction? Is that possible?

A: A fee of 1 satoshi for the whole transaction, is it possible? In the p2p network, no, because there's a minimum fee rate to relay transactions which is 1 satoshi per byte. You can create it, but your peers won't relay it. If you had a friendly miner, you could talk with them and give it to them directly. The fee is implicit, though. It's whatever the sum of the inputs is less the sum of the outputs.

Q: So the fee rate is a float?

A: We don't use any floats for amounts of bitcoin. You can think of it as a fraction though; it's the amount of satoshis divided by the number of bytes.

Q: How do we calculate the balance of the wallets, without the node needing to track all the wallets? Can I explain the algorithm for calculating wallet balance?

A: I'll do that in a moment. Let's talk later.

Q: What is the mempool?

A: We better talk about that later.

Once we have the fee rate, we do coin selection. This is the CWallet::SelectCoins() function. We prefer coins with more confirmations. The logic for selecting which UTXOs is in coinselection.cpp and it uses branch-and-bound based on a paper by Murch, implemented 2 years ago. If it fails, then it falls back to an old knapsack solver. There's also manual coin selection possible using CCoinControl.

There are some coin selection issues regarding privacy. If you have multiple outputs to the same address, then someone might infer that you're the same person you were previously. There's some coin selection preferences in the algorithm to not break your privacy.

Signing is almost the last step in CreateTransaction(). The CWallet is an implementation of the SigningProvider interface. The signing logic for SigningProvider is all in src/script/sign.cpp.

## Persistence

Bitcoin Core wallet uses berkeley db for storage. bdb is a key-value store. db.cpp is for the low-level interaction with bdb. walletdb.cpp is for higher-level database read/write/erase operations. The object serialization is in wallet.h and walletdb.h and there's additional deserialization logic in walletdb.cpp -- it's all a bit scattered, that serialization stuff.

Q: .. encryption ...

A: We don't encrypt the entire thing; we only encrypt the private keys.

## Future wallet directions

The pattern matching for identifying which transactions are you is inefficient and it will be replaced by script descriptor based wallets. There will also be better hardware wallet integration. There's a tool in the Bitcoin Core github organization that integrates with hardware wallets. Tighter integratoin in the Bitcoin Core wallet itself in the future is probably going to happen. Also, we would like to improve the wallet-node interface so tha tother wallet implementations can connect to the Bitcoin Core full node. We're interested in process separation, re-implementation of the wallet in rust, and different backend storage is interesting to think about.

## Questions

Q: When you sign a transaction--- does Bitcoin Core do anything clever to, see how big the---

A: Yes, we use a dummy key to check the size of the transaction if it was signed.

Q: So there's a signature that is done in fundrawtransaction?

A: Yes, I think that's in fundrawtransactoin. It's a dummy signature.

Q: ...

A: When I talk about wallets, in this presentation, I'm talking about this Bitcoin Core wallet which manages keys and persists transactions and data. You can outsource signing to a hardware device. But the consumer hardware wallets don't really implement all of the features of this Bitcoin Core software wallet-- they usually only implement signing.

Q: Fee estimation?

A: I can point you to a blog post that I wrote. We log transactions as they come into the mempool, and we see how long it takes for them to confirm. We use those datapoints for fee estimation. We need a full node with a mempool in order to be able to do fee estimation.

Q: Are there any... dependencies... supply chain attacks?

A: We use leveldb for storing the UTXO set. We use Qt for the GUI. How do we protect against supply chain security issues? Well, we try to minimize code changes and minimize dependencies. Guix, gitian.

Q: ...

A: It's a lot larger than it was a year ago. We have some good momentum on wallet development. Do other people agree that in order to be a good protocol developer to be a good wallet developer? Sipa is a pretty good protocol developer, and he also implemented miniscript. Ajtowns thinks a lot about wallets a lot. There's quite a few developers working on wallets. It's pretty healthy.

Q: When the wallet gets its own process, is the benefit of the wallet different now? Would you recommend using the Bitcoin Core wallet in the future at that point?

A: Yeah. I don't know. I haven't worked on other wallets. This is the one I know best. I'm really not in the business of recommending other wallet implementations. I think one potential benefit of moving it into a separate process with an API would be competition and competitive pressures. Other wallet developers would be able to implement other wallets backed by a full node. Running a full node is the best possible solution for your privacy.

Q: Who is the typical user of the Bitcoin Core wallet? It doesn't seem to be the enterprises.

A: It's a very good question. Do users actually exist of this thing? I don't know. Does anyone here use a Bitcoin Core wallet? At least 10 people. Alright. It would be really useful to know that and know who's using it. It would also serve purpose as a reference implementation wallet.

## See also

<http://diyhpl.us/wiki/transcripts/scalingbitcoin/tokyo-2018/edgedevplusplus/overview-bitcoin-core-architecture/>

