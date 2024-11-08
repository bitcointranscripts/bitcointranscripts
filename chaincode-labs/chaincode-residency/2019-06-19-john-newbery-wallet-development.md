---
title: Wallet Development in Bitcoin Core
transcript_by: Michael Folkson
speakers:
  - John Newbery
tags:
  - wallet
  - bitcoin-core
date: 2019-06-19
media: https://www.youtube.com/watch?v=j0V8elTzYAA
---
Location: Chaincode Labs 2019 Residency

Slides: <https://residency.chaincode.com/presentations/bitcoin/Wallet_Development.pdf>

## Intro

I am going to talk to you about wallets. As for the previous presentation I have all of the links in this document which I will share with you. First of all why should we care about wallets? Kind of boring right? You’ve had all this fun stuff about peer-to-peer and consensus. Wallets are just on the edge. Maybe you’re not even interested in Bitcoin Core. Maybe you want to work on Lightning. I’m going to talk about the Core wallet for a hour. I think you should care about wallets because its the way that humans interact with it. It doesn’t matter about all this consensus stuff and the nodes doing peer-to-peer stuff if we don’t have a way of using the network. Wallets are the way that we interact. Even if you’re not interested in developing wallets the way we think about wallets informs the decisions we make about the peer-to-peer network. For example who is familiar with the Taproot assumption? What is the Taproot assumption?

Audience member: If you have a lot of branches there is always a branch with an agreement with all the parties making the contract. You can aggregate the root key and all the other branches will be dependent on it.

So no matter how complex your scripts are theoretically you could get all the counterparties together to co-sign. They should be able to aggregate their keys and make a single signature. The way they do that is not part of consensus. It is in the wallet. The decision we make about the Taproot design depends on the fact that we can do that even though it is not part of consensus. Enough example is SIGHASH_ANYPREVOUT. Who is familiar with that? Or SIGHASH_NOINPUT? What is that?

Audience member: It doesn’t the sign the input so you can reassign transactions to different compatible transactions instead of just one.

We can integrate that into Bitcoin Core. We have a high level design. But a lot of the discussion is around how we can make that safe. How we can make sure people don’t shoot themselves in the foot? That’s a consideration around wallets and how people interact with the network. What I’m trying to say is even if you don’t care about wallets, even if you don’t care about Bitcoin Core you should care about wallet design and design considerations.

## Fair notice

Fair notice, unapologetically I am going to talk about the Bitcoin Core wallet because I don’t know any other wallets. Sorry if you don’t care about Bitcoin Core. This presentation may contain traces of C++. Sorry if you don’t know C++ but I will try to make it understandable.

## What are a wallet’s functions?

What is a wallet? What are the functions of a wallet? I didn’t get as many as you. I have key management, transaction construction and persistence. What do I mean by those things?

## Key management

Key management identifies your own transactions. If you have a wallet you want to know when you get paid or when you pay someone. You need to generate new addresses either for handing out to people for payments or generating new keys for change outputs. And you need to determine how to sign transactions.

## Transaction construction

Under transaction construction I had you need to be able parse addresses and turn them into txOuts. You need to select coins from your wallet. UTXOs that you own you need to choose which ones to use as inputs to your transaction. You need to sign them and then you need to broadcast them. Advanced features like CPFP, RBF, batching, mixing, coinjoin, payjoin, whatever advanced features you might want to use.

## Persistence

Then persistence. You need to have some kind of permanent storage to store your keys. But also to store your coins so you don’t need to rescan the blockchain every time you start your wallet. Store your transaction history because you might be interested in payments that have come in and coins that you’ve spent. And metadata. Things like labels, how far you’ve scanned through the blockchain and so on. From a high level that is what I’m going to talk about today. There’s also a number of other things the wallet is doing but this is really the core of what a wallet needs to do.

Q - Can you distinguish between a node that’s running with the UI versus command line?

A - The wallet is not interacting with the peer-to-peer network. You have your node and the wallet is behind the node.

Q - When you launch the UI it is not running the actual node?

A - The UI is running the node.

Q - But it’s a separate process?

A - It is the same process. It is a different component. There is a well defined interface between Qt which is the GUI, and the node. When you run Qt it is running everything the same except you also have the user interface.

## Agenda

Before we dive in I am going to do a quick glossary of terms and objects in the wallet you will need to know about. I am going to talk about initialization of the wallet and the interfaces into the wallet. When looking at a new codebase these are probably the best places to start. To see how it starts up and see how you can interact with it from outside. I am going to talk about code management. Where this code lives, where the files are. Key management, transaction construction, persistence and then future directions for the wallet.

## Glossary

What is a pubkey in Bitcoin?

Audience member: Something you can use to sign transactions.

You do need to a pubkey to receive funds. What is the pubkey itself?

Audience member: A point in the elliptic curve.

A point on the secp256k1 curve. In Bitcoin Core we have this object, we have this class `CPubKey` which is an encapsulated point on that secp curve. What comes with the pubkey? A private key. What is a private key?

Audience member: Hopefully a huge number.

It is a scalar. A private key kept secret and used to sign. It is a scalar in the secp256k1 group. In Bitcoin Core that is a class called `CKey`. That’s in `src/key.h`. Next up we have this thing called `CKeyID` which is the HASH160 of that public key. That’s the hash used to create a pubkey hash. That’s also how we identify the keys in the wallet. That is a uint160. It is a 160 bit number and the class is `CKeyID` a reference to a `CKey`.

`RIPEMD160(SHA256(pubkey))`

This is the hash used to create a P2PKH or P2WPKH address.

Then finally `CTxDestination` and that’s a script template with a specific destination. That’s stored as a variant variable. That can be any one of these types: `CNoDestination`, `CKeyID` a P2PKH, `CScriptID` a P2SH, `WitnessV0ScriptHash` a P2WSH, `WitnessV0KeyHash`, `WitnessUnknown` for a future SegWit version. When we look at an output you try to match a template type to it. We say this is a KeyID or a WitnessV0 ScriptID. As we are receiving transactions and parsing them we want to be able to identify what kind of output it is. That’s where the matching happens.

Q - That’s not the full list of everything you can send in Bitcoin. It just the list of what the wallet can send to?

A - Or the wallet can see yeah. You can send to any arbitrary script. This is templating script types.

Q - This is part of the transaction output? Or the transaction output is passed into this structure?

A - Each transaction output has a scriptPubKey. And that scriptPubKey can be any kind of script in the Bitcoin scripting language. But the ones we recognize in the wallet and that we use in the wallet all fit under these templates. And multisig. I didn’t have multisig on there.

Q - P2PK is completely removed?

A - I’m not sure.

## Initialization and interfaces

Let’s talk about initialization and interfaces. It is really exciting. The wallet component is initialized through the WalletInitInterface. That lives in src/walletinitinterface.h. It is just a interface class called `WalletInitInterface` with four methods and a deconstructor. `HasWalletSupport()` `AddWalletOptions()` `ParameterInteraction()` and `Construct()`. This init interface is for starting up the wallet component. For builds with wallet the interface is overridden in src/wallet/init.cpp. It is called `WalletInit`. It inherits from `WalletInitInterface` and it implements those virtual interfaces. For `--disable-wallet` builds this WalletInitInterface is defined in src/dummywallet.cpp. You have this `DummyWalletInit`. It inherits from the `WalletInitInterface` and all of these methods are basically just null. They return true or don’t do anything at all. Those interface methods are called during node initialization. In src/wallet/init.cpp you get this global `g_wallet_init_interface`. It calls `Construct` or parameter interaction or whatever. The reason why we have this dummy class is it means that we don’t have a bunch of if defs all over the initiation function. This is the same call whether it is a build without the wallet or a build with the wallet. It is just without the wallet this would be a dummy interface and with the wallet it will actually construct the wallet component.

Q - There is only one user in that sense for that interface?

A - Yes.

Q - When the source code was initially written this was the entry point and all the code was built into it and extracted to create the daemon?

A - It was all mixed together. There was no separation at all. There was wallet code within main.cpp. No calling into wallet code, wallet calling into…

Q - You couldn’t run one without the other?

A - I don’t think so. I don’t know when disable wallet was introduced but I imagine the initial version didn’t have that.

Q - The separation into this wallet interface seems to be recent, 2017. This is the direction we are going into where pieces of the code get broken up into interfaces and components?

A - Yes

Q - And even separate classes so that if there is some vulnerability in your wallet process it can’t get to your node or the other way round. Especially the networking code is kind of scary. If there is some problem with the networking code hopefully that cannot get to your wallet code. I think that is the idea of process separation. And having things on different machines.

Q - Or even different VM. We have a peer-to-peer stack. We may run a VM connected with a IPC to a wallet.

Q - You run a node on some device somewhere but you have a graphical interface on your computer.

A - We’ll get onto that a bit later.

Q - Why is there an interface specifically for the init part of the wallet interface? If we build with `disable-wallet` you would think the entire wallet interface would need to be included.

A - This `WalletInitInterface` is defined in the node. Then the wallet code inherits from there and implements that interface. Or if you build without a wallet then the node code implements that interface as a dummy.

Q - There is probably some interface between the RPC calls and the wallet that would also be dummied out because it is rebuilding without the wallet. But that’s not part of the `WalletInitInterface`. That’s a separate interface. We’ll get onto that.

## Loading

We’ve constructed the wallet component. Now we are going to load the actual wallets. `WalletInit::Construct()` adds this client interface for the wallet and the node then tells the wallet to load/start/stop through the `ChainClient` interface. This src/interfaces/ directory contains all of those interface definitions between the node and the wallet and between the GUI and the node. `ChainClient`and that is telling it to do various things like `load` `start` `flush` `stop`. This is loading individual wallets. Most of the methods in that interface call through to functions in src/wallet/load.cpp. As you can probably imagine this file contains all of the loading code. Verifying the wallets, making sure that the wallet files are not corrupt, loading the wallets, starting the wallets, flushing them, stopping them, unloading them.

## Node <-> Wallet Interface

The node holds a `WalletImpl` interface to call functions on the wallet. The wallet holds a `ChainImpl` interface to call functions on the node. Again those are defined in src/interfaces/. This `WalletImpl` has methods like `lock()` `unlock()` `changeWalletPassphrase()` `backupWallet()`, `getPubKey()`. This is used by the GUI. The GUI connects to the node and calls wallet functions through this interface. Then if the wallet needs to call functions on the node it uses this interface `Chain`. That has things like `findBlock` `findCoins` `hasDescendantsInMempool` `checkChainLimits` `isReadyToBroadcast`. Anything the wallet needs to know is called through this interface class.

Q - Why would the node need to call into the wallet?

A - It is only for the GUI. The GUI doesn’t connect directly to the wallet.

Q - Notifications?

A - It is not notifications. This is just for the GUI. `WalletImpl` is just for the GUI connecting through the node to the wallet.

Q - The wallet never calls through the RPC path to the node? It is a direct interface.

A - Yes. The wallet does not call RPC functions in the node.

Q - For separating the wallets, this interface…

A - This interface is what would be used. Instead of it being a functional call interface it would be an interprocess call. It would use the same methods.

Q - The GUI could call the wallets directly rather than calling through the nodes, those types of trade-offs. I guess this was just done to make it easier.

A - Yes

This might make things easier. You have your node and your wallet. You have the GUI which calls through the node into the wallet using that `WalletImpl` interface. The wallet calls into the node using the `ChainImpl`  interface. I haven’t mentioned this yet but within that `ChainImpl` there is a notifications handler. That is for all the transactions coming into the mempool, you need to be notified. Or when a block comes in and is connected you need to be notified. That happens through that notifications handler `Notifications HandlerImpl`.

Q - The wallet has an implicit dependency on the node. It is not standalone.

A - No

Q - That is permanent. The node is where the consensus is. The wallet needs to know what consensus is in order to do anything meaningful. Unless you say let’s make a generic wallet that other implementations could use. I don’t see Bitcoin Core doing that. That doesn’t make a lot of sense.

A - Let’s park discussion of what happens in the future until the end. Let’s talk about how it is now and then we can get into future potential.

Q - The notifications handler element, is that in addition to the validation interface or is it…

A - It is the validation interface. I’ll go back and explain it.

I wanted to put this diagram up because people were getting a bit lost I think. This is what it looks like. There is one way for the GUI to call into the wallet which is this. There is one way for the wallet to call into the node which is this. And there’s one way for the wallet to get notifications which is this. Then obviously there’s a RPC directly into the…

Q - The GUI gets notifications about changes from the node or through that wallet interface as well?

A - I am not entirely sure about that.

Q - I think that bounces around a few times from what I’ve seen, the notifications that end up in the GUI. But I also don’t remember how.

Q - How does the GUI get updated from the notifications from either the wallet or node about changes from the network, transactions, blocks, stuff like that?

Q - Right now the GUI is implementing the notification interface…

A - No it is not a notification interface. It does have some interface to get notifications. I don’t know right now.

Q - Is the RPC talking directly to the wallet and not through the `WalletImpl`?

A - It is not talking through the `WalletImpl`. It is talking directly to the wallet through the RPC server.  During initialization the RPC gets up to the wallet.

Q - There are a few calls to register the RPCs on the RPC servers.

Q - The chain object is a separate object. It is not part of the node.

A - This `ChainImpl` is an implementation of the Chain interface. All of the chain state and mempool stuff lives here in the node.

Q - There is also the node implementation interface.

A - Yes but we are not going to talk about that.

The node has the `WalletImpl` interface to talk to the wallet. The wallet has the `ChainImpl` to talk to the node. Then the third piece is the node notifies the wallet about new transactions and blocks through the `CValidationInterface`. This `CValidationInterface` is in /src/validationinterface.h and this is an interface for any interested party to register for notifications for changes to chain state.

Q - This might be a basic C++ question but I see here you have virtual functions and before you didn’t have. They were also virtual?

Q - They were virtual as well. Here you don’t have to override, there you have to.

A - We never instantiate an object of this class. We also inherit from this class. That’s why these methods are overridden.

Q - When it is equal to zero what does that mean?

A - It is not defined. There is no definition for that.

Q - If it is zero you have to provide overrides for all of them. If you inherit this class that we have on the screen you don’t have to provide overrides for all of the functions.

That’s the interface. This is validationinterface.h. It has got good comments on what all those methods are. Then this `NotificationsHandlerImpl`  is inheriting from that interface and overriding the functions that it is interested in. The functions that the wallet is interested in in that `CValidationInterface` is `TransactionAddedToMempool`. Obviously your wallet wants to know whenever a transaction is added to the mempool in case that is a transaction that it is interested in. `TransactionRemovedFromMempool` when a block is connected, when a block is disconnected, when the blockchain tip is updated and when the chain state is flushed.

Q - We have all these handlers that are queued up. Let’s say a new blockchain tip occurs. All these handlers are called, they are called in sequence. Why? If I have ten subscribers, there’s one event. Why is it important that these ten handlers are called in sequence in that queue? Why can’t they be called concurrently?

A - Because we only have one thread. Some of these are asynchronous and some of these are synchronous.

Q - Every subscriber to validation events could have its own stack of events on its own thread.

Q - Every subscriber has one handler or multiple. They will then register these handlers and when they register it they have to register in sequence. They have spots. When the event is called, the signal is called, these are executed one by one by whatever thread is calling the signal.

Q - You need every component to see the same consistent view. The events have to be in order but not between the different components.

A - You could potentially do something like that. The way it is implemented in Bitcoin Core is that some of these are synchronous. `ChainStateFlushed` is the main thread, the message handler thread, will call those callback functions directly. The background thread methods will be called on the scheduler. We only have one of each. Potentially you could make it multithreaded but we’re not optimizing for having like 50 wallets in parallel.

Q - If I’m a miner and there is a new blockchain tip I want to make sure that my handler for the block template is on the top of that stack.

A - You’re probably not going to be running multiple wallets on that same node. It seems like an over optimization to try to make that multithreaded.

## Why?!

At this point you might be thinking why? Why all this weird indirection?

Audience member: It is modularized, it is good.

Audience member: If you have different processes you may use unique tricks to read only some part of your policies. In your file system they would not be the same policies as your chain process.

There are are no functional calls between the node and the wallet. A well defined interface is easier for us to reason about. It means if we make changes to wallet code we are pretty sure we are not making changes to consensus code. Whereas if there are functions calling into each other across that boundary then it makes much more difficult for us to reason about those changes. Individual components could be tested in isolation. You could potentially build the wallet library and test it. We don’t but you could. And in future we could separate the wallet into a separate process which would be good for security because you wouldn’t have your private keys living in the same memory space as the networking code. Then potentially we could open that API up, make it public and other people could make wallets that plug into a Bitcoin Core node. That would be way in the future. This is all pretty recent. These interfaces only got merged maybe 3 to 6 months ago. We now have nice contained wallet code. It is a lot friendlier to work with.

Q - Before that it was…

A - It was just functional calls. The node was making functional calls into the wallet. The wallet was making functional calls into the node.

## Code Management

I am going to run through code management. Let’s have a look at the wallet directory.

`ls -1 src/wallet`

In src/wallet there are a few files. A test directory for unit tests. There is not much in there. It is not huge.

## Code layout

We have coinselection.cpp and coinselection.h which is the branch and bound coin selection algorithm. We have crypter.cpp and crypter.h which is the code for encrypting the wallet’s private keys. walletdb.cpp and db.cpp and the header files, that’s interfacing into the wallet’s BerkeleyDB for persistent storage. init.cpp for initializing the wallet module. And load.cpp for loading up individual wallets. rpcwallet.cpp and rpcdump.cpp for the wallet’s RPC methods. wallettool.cpp is a standalone wallet util. And wallet.cpp is everything else. And then some tests. If we look at the line counts. coincontrol.cpp is pretty small. coinselection.cpp is 300 lines of code, crypter.cpp is 300 lines of code. db.cpp and walletdb.cpp together are maybe 1500 - 3000 lines. feebumper.cpp is for bumping fees, that is another 300 lines. feebumper, crypter, coinselection, coincontrol, these are all pretty small self contained functions. In fact coincontrol is just an object. fees, init, load, all pretty small. psbtwallet.cpp is pretty small, that is for the partially signed Bitcoin transaction format. RPC code is pretty big. That is maybe 6000 lines of code. That is the main interface to the wallet from the command line. wallet.cpp is 4500 lines, that is where the bulk of the logic is. wallettool.cpp, a standalone tool, is like 150 lines, nothing there. Then walletutil.cpp is just utility functions.

Q - For encrypting is there a common encryption library or does it reuse some of the crypto libraries? Does it have its own thing?

A - I’m not sure.

Q - I think it is with CAS, sipa’s implementation of CAS like all the encryption of the wallet stuff.

A - It is just encrypting the private keys.

Q - I think you need to add also keystartup.h and keys.h.

A - There is other code that the wallet is calling which is not in this directory. `IsMine`, the signing interface, that’s in src/script. Maybe I should include some other files here.

Q - What about wallet descriptors?

A - We don’t have script descriptors in the wallet yet, not fully implemented. What we use right now is a function called `IsMine` and a signing provider. Those are both in src/script.

Q - Except for import where you can add all the descriptors. They are translated to the old style of the wallet.

Q - The wallet file wallet.cpp, do you think there is more things that should be extracted out eventually or is it pretty good as it is?

A - Potentially we could extract more out. It used to be that everything was in wallet.cpp.

Q - This might be too early but I’ve noticed that there is a lot of activity around `IsMine`. Some general context?

A - I’ll talk about that later.

Q - wallet.h is gluing the other parts together?

A - .h is the header file. That will contain all the declarations for the classes and functions. Then the implementation of those classes and functions will be in the .cpp
