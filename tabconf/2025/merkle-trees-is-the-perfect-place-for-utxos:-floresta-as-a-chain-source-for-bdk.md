---
title: 'Merkle Trees is the Perfect Place for UTXOs: Floresta as a Chain Source for BDK'
transcript_by: 'RazorBest via review.btctranscripts.com'
media: 'https://www.youtube.com/watch?v=KHQFxNoRmpo'
date: '2025-10-31'
tags:
  - 'tabconf'
  - 'bitcoin'
  - '2025'
  - 'tabconf 7'
  - 'technology'
  - 'conference'
  - 'atlanta'
  - 'bdk-floresta'
  - 'BDK'
  - 'Bitcoin development'
  - 'Bitcoin wallet'
  - 'Floresta'
  - 'Utreexo'
  - 'trustless wallet'
  - 'developer'
  - 'merkle'
speakers:
  - 'Luis Schwab'
categories:
  - 'Science & Technology'
source_file: 'https://www.youtube.com/watch?v=KHQFxNoRmpo'
summary: "📌 Learn more about this talk on GitHub: ⭐️🐙\nhttps://github.com/TABConf/7.tabconf.com/issues/33\n\n🌱🧰 Explore bdk-floresta\nA work in progress BDK chain source crate that uses floresta-chain + floresta-wire to run a local, trustless node and wallet directly on your device 📲🧱\nPerfect for mobile and low spec setups ⚡️\n\n🧠 What this talk covers\n🌳 Utreexo 101\nMerkle proofs, validation, and bridge nodes\n🔍 How Floresta leverages Utreexo and how it differs from utreexod\n🏗️ A clear BDK architecture overview\n🎬 Live demo\nCreating and syncing a wallet using the crate ✅\n\n🎯 If you’re a dev or a Bitcoin enthusiast who wants lightweight, self contained wallets that can run anywhere, this one’s for you 🛠️🟠\n\n⚡️🛠️⚡️🛠️⚡️🛠️⚡️🛠️⚡️🛠️⚡️🛠️⚡️🛠️⚡️🛠️⚡️🛠️⚡️🛠️⚡️🛠️⚡️🛠️⚡️🛠️⚡️🛠️\n\n🟠 TABConf is a technical Bitcoin conference built for builders. We bring protocol + application devs together to collaborate, debate, and push Bitcoin forward. 🧠🔧\n\n🎥 On this channel you’ll find:\n🗣️ Full talks • 🧑‍🏫 workshops • 🧩 panels\n🛠️ Builder Days sessions • 🔍 deep dives on:\n🧱 Bitcoin Core • ⚡️ Lightning • 🕵️ privacy • 🔐 security • 🧰 the tooling teams ship with\n\n🎟️ TABConf 8 tickets are on sale now!\n🗓️ Oct 12–15, 2026 • 📍 Atlanta, GA\n🏛️ Georgia Tech Exhibition Hall\n\n🎫 TABConf 8 Tickets\n🟠 Pay with Bitcoin: https://checkout.opennode.com/p/7d51f71f-f3e6-4159-bbfa-3a231d14e5b8\n\n💳 Pay with Stripe: https://buy.stripe.com/00w4gzapSf0o4ubg2mdQQ0b\n\n🌐 TABConf Website\nhttps://tabconf.com\n\n🔗 All links hub\nhttps://linktr.ee/tabconf\n\n🫂 TABConf Community\n💬 Discord: https://discord.gg/TRaX8M7amU\n\n🐦 Follow us on X\nhttps://x.com/tabconf\n\n🎧 Subscribe to the TABConf Podcast\n🍎 Apple Podcasts: https://podcasts.apple.com/us/podcast/tabconf-sessions/id1867836916\n\n🟢 Spotify: https://open.spotify.com/show/11Ram7ccTjBeiwhYoDVtF4?si=ec8bab9fdc2945cd\n\n⛲️ Fountain: https://fountain.fm/show/fqYiANm1II8INYOodXaj\n\n⭐️ Star us on GitHub\n🐙 https://github.com/TABConf"
---

Speaker 0: 00:00:00

Hello guys, today I'm here to talk about Merkle trees, Floresta and BDK.
I'm Luis, I'm a grantee from Bitcoin Dev Kit, based out of Brazil.
So a little overview on BDK.
We are a library with a set of crates for building `Layer 1` Bitcoin applications, mainly wallets, but you can build anything that touches on-chain.
We care about blocks, transactions and how to retrieve them.

We have a few crates on BDK.
We have our main crate, the `bdk_wallet`, which is a fully-fledged wallet implementation, batteries included.
We have `bdk_core`, which has the core types and structures that we build everything on top of.
We have `bdk_chain`, which indexes relevant chain data to the wallet's SPKs.
We have the `file_store`, which is a file database for testing and development.
We have the `testenv` crate, which is a set of utilities to make integrated testing.
We have the `Electrum` client, which connects to an `Electrum` server, the `Esplora` client that connects to an `Esplora` server.
And `Kyoto`, which is a chain-source crate that uses compact block filters for data retrieval.

The `bdk_wallet` crate implements the wallet structure.
It tracks indexes and updates `scriptPubKeys` from the descriptor.
These updates need to come from somewhere, either a Bitcoin node, `Esplora` or `Electrum`.
This is an issue, because most people don't really want to run a server or don't know how to run a server, so they just have to trust whatever data they get and there's not much they can do about it.
These servers are a big honeypot for malicious actors like states and ISPs, because they can correlate your IP with chain data such as transactions, addresses, balances and things like that.

Now we get to the issue of the` UTXO` set.
`UTXO` represents an unspent transaction output, a coin that can be spent.
Everybody on the network needs to be aware of everybody else's coins in order to validate transactions.
So if you want Bitcoin to scale on `Layer 1`, we're going to have a lot more coins than we have now.
Because Bitcoin is very small, very few people use it, so if you want to scale this to the entire world we need to figure out a way to make this scale.
We can see on this graph that the `UTXO` set is ever increasing.
It has doubled since the last two years.
It would be great if we could figure out a way to compress that.
And we can with `Utreexo`.
`UTreexo` is a scheme that manages to compress the `UTXO` set into a compact representation using a dynamic hash accumulator.
It does that by arranging all the `UTXOs` in the set as leaves in a Merkle tree, hashing them and storing only the roots.
We can compress 11 gigabytes of the `UTXO` set into just a few hashes.
Since we compressed the `UTXO` set, we're not aware of its entirety.
So we need a way to prove that a coin is present in the set without knowing the entire set.
So we have inclusion proofs.
Let's say I want to prove that the coin `C` is in the set.
For that I need to prove hashes `H(D)`, `H(AB)` and `H(EFGH)`.
You can check this inclusion proof against your own accumulator state and verify that the coin is indeed present in the set.

`UTreexo` introduces some new network topology to the Bitcoin network.
We have full nodes, which are just regular Bitcoin core nodes.
We have a bridge node, which is responsible for generating and providing all the proofs.
So instead of just storing the accumulator hashes, it stores all the trees.
So that's a bit heavy, a few tens of kilobytes on `mainnet`.
We have compact state nodes, which are nodes that only store the Merkle root hashes.
And the bridges provide proofs to compact state nodes.

`Floresta` is a Rust implementation of a compact state node.
It's a lightweight node that can run on a phone or even a Raspberry Pi.
It has a reusable set of crates that can be used as dependencies for other projects such as `bdk_floresta`.
So now we have Floresta as a chain source for BDK.
Why?
I think BDK has a lot of users, many users, many projects use BDK to implement wallets.
So it would be great if they could have a drop-in replacement that has local, trustless on-device validation, because making API calls with financial information is bad for privacy.


`bdk_floresta` will spawn a `Floresta` node on the background, and then it exposes a subscriber that emits wallet updates that can then be applied by the wallet.
Currently, as the project stands, we only have block-by-block synchronization, which is as the node receives a new block, it's applied by the wallet, which takes some time.
But soon we're going to have compact block filters implemented, which will be able to do a backwards full scan very fast.
Spawning a node is pretty simple.
We create some configuration for the node like network and data directory, user agents and things like that.
Then you build a node with the configuration.
And then you just have to get the updates from the node.
So you get a lock on the the wallet, you create a subscriber from the node, you spawn a process that will listen to new events and then you match against the event type.
Currently, we only have block events, so the wallet applies the event.

I made a demo on `signet`, so let's see if it's going to work on this network.
So it spawns a node, fetches some peers from DNS.
Downloads the headers from peers.
We need to get some more bridges up.
It's trying to connect to a `Utreexo` peer, a bridge to get proofs to validate the blocks.
Yeah, it just spawns a task with `Tokyo`.
There are a few in Brazil, some in the US.
We need more.
That's a problem because there's so few bridges that the chance of finding a bridge via P2P discovery is very low.

Speaker 1: 00:10:59

So you need more people to run bridges and then we'll get the peer-to-peer discovery better.
Do you do preferential peering?

Speaker 0: 00:11:10

Yeah.

Speaker 0: 00:11:19

It seems that we're having a lack of bridges here.

Speaker 1: 00:11:23

And those bridges are developed where?
Does `Floresta` develop a bridge as well or is that a completely separate piece of software?

Speaker 0: 00:11:33

So `Floresta` is a compact-state node, so it only keeps the stubs from the roots.
There is another project that's a bridge from Calvin Kim, which is `Utreexod`.
So this is what people are running pretty much.

Speaker 1: 00:11:49

I see.
And `Utreexod` is only the bridge?
Or they also have a compact node?

Speaker 0: 00:11:58

I think they can run as a compact as well.
I'm not sure.

Speaker 1: 00:12:26

I had a question about the privacy trade-offs point that you were making.
So typically you might be connecting to some kind of external `Esplora` instance or something.
But with this, are you going to be connecting to a very small set of these bridge nodes, and is there any difference in the kind of information we're asking for?

Speaker 0: 00:13:00

You only really need bridges during `IBD`.
After `IBD` you can connect to other Compact State nodes, and they will have proof for new blocks and transactions.
You only need a bridge for `IBD`.
But you behave on the network like a normal node.

Speaker 2: 00:13:24

I'd just like to add that the difference here is that you are a regular node doing regular node stuff.
You're just downloading blocks and transactions, address, like any node would already do.
So you are just a node rather than "This is my address - give me transactions".
So it's pretty different.
You're just a node doing node stuff, but with people knowing you are a `Utreexo` node, but that doesn't give much away.
It's just like "Hey, I do `Utreexo`, nice to meet you!".
But you're not saying "Here's my address - what are my transactions"?

Speaker 0: 00:14:11

Exactly, so if you broadcast a transaction via an `Esplora` server, the server knows the transaction is yours.
It can correlate with your IP.
If you're using embedded nodes, it can be anybody's transaction.
You just relay the transaction.
There's a big privacy gain there.
Yeah, it seems we're not gonna have this demo working today.

Speaker 4: 00:14:42

Can I follow up on what you just said before?
Did you say that you don't need the bridge?
I thought you said that the bridge makes the proofs for every new block that comes along.

Speaker 0: 00:14:52

`Utreexo` works like this.
If you want to spend a `UTXO`, you have to attach an inclusion proof of that `UTXO` in the set.
So let's say I am a Compact State node, like `Floresta`, and I want to spend a UTXO.
I need to have the inclusion proof of that with me.
So I create a transaction, sign it normally, attach the proof and broadcast it.

Since we're not going to have any demo work, I'm gonna do a walkthrough on the code.
This is the example I'm running.
We have a descriptor, which I deposited some Bitcoin to it.
We create a `BDK` wallet, set the descriptors, set the network.
We can do `assumevalid` which means you don't do a script validation for blocks before this one, so that goes a little faster.
You create the node config, you have to set the network, set the data directory and some other fields if you want.
Then you create the node, you spawn a node with the config, with the `assumevalid`, attach the wallet, build.
Here I connect some bridges manually, but apparently that's not working.
Then you create a wallet subscriber so you can listen to new wallet updates from the node.
Then you spawn a task for receiving these updates.
And then you can match the update variant and apply it to the wallet.
So in this case it's a block, so `BDK` already has an API to apply the block directly, so we don't have to do anything.
But in the future we're going to have wallet updates from the compact block filters.
Here we have the implementation of the node.
We have config, we have the chain state, we have a handle to interact with the node.
We have some `SIGINT` tasks, we have a signal to stop the node.
We have the wallet, and we have the subscriber which is just an `UnboundedReceivere`.
Here we have some methods to interact with the node like shutting it down.
This checks if the node should stop.
This connects a peer.
This connects a peer.
This gets some info about the peer.
Here we have the implementation of the block subscriber.
Here we can flush the chain to disk.
Here we have the builder for the node.
We have to configure all of these things.
This project is still in its infancy.
We still have a lot of work to do both on `Floresta` and on` BDK`, so I have one foot on each project doing some stuff.
We want to couple the nodes better with the wallet so we can have a shard persistence layer.
We have some stuff to change on `bdk_chain` as well.
I think that's pretty much it if you guys have any questions.

Speaker 5: 00:19:24

I'd like to ask how an ordinary pleb who's not a coder might be able to run a `Utreexo` node?

Speaker 0: 00:19:41

You don't really need to know how to code, you can like just clone the repository and install the binary and that's it.

Speaker 5: 00:19:52

Actually I'm thinking about the bridge node.

Speaker 0: 00:19:55

Yeah.

Speaker 5: 00:19:56

Because it looks like we need to get a lot more of those out in the wild.

Speaker 0: 00:20:00

Yeah.
You probably need a VPS to run the bridge.
People need to be able to access it.

Speaker 3: 00:20:16

Okay.
Thanks.

Speaker 6: 00:20:34

I have two questions.
My first one is: how heavy are these bridge nodes?
Could I just potentially run it alongside my Bitcoin node or could it ship on a `Start9`?
They're heavy.

Speaker 0: 00:20:47

They're kind of heavy.
They use up a few tens of gigabytes of RAM because they need to keep the whole forest in RAM.

Speaker 6: 00:20:59

Interesting So that might be hard to just ship on an `Umbrel` or something, where people can just click play.

Speaker 0: 00:21:07

i don't know.
I don't think that's very feasible.
It's very hungry.

Speaker 6: 00:21:11

I saw the presentation yesterday on having it on mobile, or two days ago.
So yeah, that was great.
Looking forward to seeing it in BDK.
And my second question is, how many people are working on `Floresta` on the project?
And how's that going?
Are you looking for contributors?

Speaker 0: 00:21:30

There's like five people.
Five, six people.

Speaker 6: 00:21:39

Awesome.
Thank you.

Speaker 7: 00:21:53

Hi, can you explain how compact block filters integrate with that?
Has it something to do that it can also fetch the relevant information from normal Bitcoin nodes and not only from `Floresta` nodes?

Speaker 0: 00:22:09

The way it's implemented at this moment, we can only get wallet updates from new blocks that the node verifies and receives.
But the problem is, if I have a wallet that has transactions in the past, I cannot really sync them very fast.
So if you have compact block filters, compact block filters work with bloom filters.
So we make requests to many peers with this filter and we get the transactions details that we care about.

Speaker 7: 00:22:51

So only during `IBD` you do compact block filter?


Speaker 0: 00:22:55

No, we do compact block filters after `IBD`.
But `Floresta` can also skip `IBD`.
So in this case, the only way to get updates from the past is to do compact block filters.

Speaker 7: 00:23:10

Thanks!
