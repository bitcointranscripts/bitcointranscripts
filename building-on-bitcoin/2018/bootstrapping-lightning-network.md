---
title: 'Bootstrapping LN: What have we learned?'
transcript_by: Bryan Bishop
tags:
  - lightning
speakers:
  - Fabrice Drouin
date: 2018-07-04
---
<https://twitter.com/kanzure/status/1014531050503065601>

My name is Fabrice Drouin. I work with ACINQ. We are a comapny working on printing LN. I am going to talk about what happens, what was the process of bootstrapping and developing lightning and what happened on mainnet.

# Timeline

Who doesn't know what lightning is? And who has used lightning? Okay, almost everyone. It's an evolution on the idea of payment channels. I think it's from 2011 actually. The first big step for lightning was the lightning network paper published in 2015 by Drja.

Rusty Russell published a series of article in 2015 about how to go from an interesting concept to something that could be implemented.

Lightning started basically as indepdndent innovations in 2015 and in 2016 something really important happened in Milan. We decided to go for an open-source process or RFC-like process. Instead of having lightning driven by a group of a specific company, lightning is first a process to build an open-source specification. Anyone just with the specs can implement lightning. It's very important because I do believe lightning got a lot of interest because of that structure and the fact that there was not one single company behind it. There is no ICO, no token. It's an open-source specification that is very detailed. It has everything you need to implement it yourself. Each company is building their own implementation. Other people working on lightning implementations- at least two of them, one in Japan, and someone working on a python implementation.  And one is being made at MIT, which is lit. This structure is particularly successful. The open spec and organization is important.

The specs reached v1 in December. Right now, you have all 3 major implementations are live on mainnet as of April 2018.

# Basis of lightning technology

<https://github.com/lightningnetwork/lightning-rfc>

... you can have a good idea of how it works just by looking at the specs.

# Lightning overview

You can have one transaction to open a lightning channel. It's publsihed on the blockchain. Each party, Alice and Bob, exchange messages and updates... it's a valid bitcoin transaction but it's not published. You can update the valid bitcoin transaction which you don't publish. You update bitcoin transactions, but you don't publish.

The closing transactions- suppose you are happy with the balance on your channel. Alice and Bob can agree on the final transaction and get their money back on the blockchain. You update a transaction that splits how to spend the money.

# How do payments work?

Most of you have tried this. It looks like bitcoin. You have a QR code and you scan it. You have a destination and payment hash. It creates a packet and it gets forwarded to the nodes on the route. Basically it works using preimages. For those of you have used lightning, this can realistically happen within one or two seconds. You get instant payments, and you don't have to worry about confirmations. Also it can work with small amounts.

# Phase 1: testnet

Our first phase was to test on testnet. We were able to validate the transport layers, encryption stuff the way we use transactions. We were able to iron out compatibility issues. We were able to validate implementation choices because... something I forgot to mention, it's very important, it's possible to have different implementations. For bitcoin, it's still an open question as to whether it's good to have multiple bitcoin implementations. Clients must always reach the same results all the time. However, lightning is different and what happens is more like tradiational client-server communication. The exchange you have with your peers has no impact on the rest of the network. It's easy to have multiple implementations, and if something doesn't work, it's easy to upgrade. There are no global consensus issues like in bitcoin. It's not like changing a wheel on a moving car. It's very easy and we do it all the time.

There is a block explorer. There's y'alls. You can buy articles for micropayments and you can read stuff.

We also saw on testnet... a lot of bugs went unreported. A lot of nodes were unreliable. Many of them were never reachable in the first place. Some users forgot to open ports, so you couldn't reach the nodes in the first place. So, testnet for lightning is much less reliable than lightning on mainnet. Most of then odes on testnet... they are offline most of the time. It's a bit frustrating. It was time for us to take the training wheels off.

# Reckless at last: Lightning on mainnet

All of the main implementations were running on mainnet on April. Who bought stickers on lightning? Okay, quite a lot of people in the audience.

We saw some operational issues. None of them were very important. All of the money is on one side, for example. Lack of symmetry in payment capacity was an issue we knew about. if Alice opens a channel to SQUEEKYCLEAN, a lightning node, and Bob opens a channel between.... so can Alice pays Bob?  Alice and Bob might have all their funds on their side of the channel, thus they cannot pay each other.

Dual funding was proposed too late to make it into the specs.

Reanchor is where you replace the funding transaction with something else. This could work with channel factories where closing a channel also opens up a new one.

You could use PUSH and create channels with funds on both sides. Unfortunately this requires an external setup.

# Onchain fee management

We spoke about fees in the previous talk. The biggest operational issue we had on LN mainnet was fee management, for on-chain fee management. The idea is to have transactions that are signed but not published. It means that the fees are going to be static while the on-chain fees are fluctuating.

If the fee rate is fluctuating then it means that you are going to be closing channels often.

# Fee estimation

In the specs, 1000 / 4 = 253. Our fee rate is in satoshi/kiloweight. Estimators and wallets use fee rate in satoshi/kilobyte. Bitcoin Core relay fees are in satoshi per virtual byte (vbyte). What the heck is a vbyte?

What if there was a way to remove fee management from LN? The first thing that comes to mind is using child-pays-for-parent (CPFP). This wouldn't work because you have to produce the transaction in the first place.

However, with eltoo, fee management can be moved out of the protocol. There's a nice solution coming soon.

# Mobile LN nodes

Another challenge for us was how to build mobile nodes. To be really used by people, you need mobile LN wallets. It's hard to do. You basically have two options- you either do remote control, so your wallet is remote control for a node running somewhere else either in a cloud or at home... it's an option used by zap wallet I think. It's the easiest option, but there's security issues. What it means is that you have a node somewhere that accepts incoming requests to send money... so it could be hacked. It's a bit of a problem. There are people working on this.

We'd rather work on having "real" mobile LN nodes. There are many different issues. The first issue is that you need to find a framework that you can use on Android or iOS. You don't want to write anything from scratch on these systems. It's not so easy- there are limitations on what you can use on Android or iOS and there are very few frameworks that actually work everywhere.

A mobile node is going to be offline most of the time. You need to wait on the blockchain. You need to watch the blockchain and watch if the other guy is going to cheat. How are you going to do that if you are offline?

You also need to check that some transaction exists on the blockchain. And you need to validate channels.

How do you synchronize the routing table? If you are offline, you miss the routing table updates. That's a problem for offline nodes.

We are using scala and it runs on the JVM so it works on Android. But there's no way it can run on iOS right now.

# Blockchain monitoring

You could either delegate monitoring to someone else using a watchtower, or you do it on the device.

Delegation to watchtowers is not practical today because the idea of watchtowers is that they don't learn anything about what you are doing, and they don't even know which channels they are watching, and it's not easy and it's a lot of data you have to store. It's a problem for the watchtower concept. Its data set grows and it doesn't know when to prune it.

On device is possible, but you would require very long timeout. Someone could cheat whenever, so you wwould probably need a one week timeout on your phone. You would have to wait 1 week before you get your money back if the other party cheats-- and it might take a qwhile.

Another option is that send only is limited... if you just want to receive, you don't have to care. You can be offline for weeks and you're safe.

Chanenls don't have to be announced. You don't have to be part of the routing table. This has been the default for Android eclair wallet for months now.

Send-only mode is limited, obviously. But that's how it's implemented. It's easy to implement and it doesn't clog the routing table.

# More on mobile LN nodes

Send-only mode helps but you need to do closing transactions and watch the funding transaction.

We watch the output script. But it would be nice to watch for specific transaction IDs. Right now we use electrum servers, we are looking at neutrino bip157 bip158 client-side filtering.

# Routing table management

Again, routing on LN is now done by having everyone know the entire routing table. So you send updates to the routing table to your peers and you keep an updated routing table at all times. This is fine when you're online because your routing table is always up to date. When you're offline, it's a problem. There's a better synchronization mechanism in the specs where you just query for the channels you're missing and there are even better long-term solutions with invertible bloom lookup tables. For those of you using eclair, you might notice that when you start it for the first time after being offline for a few days, for about 30 seconds it doesn't work well--i t's because of the synchronization issue with the routing table. We're working to make it faster, but for now you have to wait 20-30 seconds.

# Watchtowers

The idea of watchtowers is that you delegate blockchain monitoring to a third-party and you don't want them to see much about what you're doing. There are different ideas about how to do this. One of the ideas is to encrypt what you want to publish, and use a ... committed transaction... as... it can use the last 16 bytes as an encryption key to decrypt what you told the watchtower. This is elegant, but there's no incentive to do that. It's not very practical, and I don't think we will see that kind of watchtower. If you remove the constraints where they don't know what they are watching, then other things open up. But this opens you up to a new attack vector.

It would be nice if watchtowers.... what if there was a way to make sure that only the last state is valid, withotu having to remember something about all the previous states? eltoo is also good news for watchtowers. It will help.

# Routing again

You might have heard that LN doesn't do any routing. You might have heard this is an impossible problem to solve.... or that it will work, but as it grows, it will become impractical to work with the type of routing we have today.

There are two concepts that are getting mixed up. One high level concept is, how do you find routes between nodes in the network? There is also another low-level one which is how do you build and forward packets along that route?

LN defines precisely the message and format and encryption to use to forward and build packets to your destination. It's onion routing (relayer only learns about nodes just before and just after them). In source routing, sender chooses the route.

LN does not precisely define how you find routes between nodes. This is good because we can now do upgrades about finding better routes or whatever.

Onion routing has good privacy properties.

However, all the hops know the preimage. We have ways of blinding the preimage so that it would change at each type. Hash decorrelation will become harder with LN.

One thing that has been hard is that-- if you're the second hop and the second to the last hop, then you will know what's going on, because you're connected to the destination and to the center. But how do you know you're the second node or the second to last node? So I don't think it's as big of a problem.

# More routing table management

Everyone has to know the entire routing table. Nodes keep an up-to-date copy of it. It works well with a few thousand nodes. Civilization is growing, and you can start and synchronize quickly now, but we know that this will not work with a few million nodes.

What if I told you that not every channel has to be announced? When you look at explorers, and you see nodes, you don't see everything. It's impossible to check for this.

Only channels that relay payments have to be announced. Not even all of them, you can have several channels between 2 peers, announce only one of them but still use the others ("channel override").

Terminal nodes are nodes that send or receive payments but do not relay them, and don't need to be added to the routing table.

You can build hidden networks of unnannounced channels. You can exchange information about channels or about node information, but you don't have to publish it. You can build virtual hidden lightning networks that nobody knows about. This is already possible today.

Not all channels have to be announced. There could be millions of them. It's how it works today.

# Capacity issues

It's true. There are capacity issues. The big reason is that users open small channels. Why do they do that? It's because we told them to.
