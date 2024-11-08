---
title: Lightning Overview, Channel Factories, Discreet Log Contracts
transcript_by: Bryan Bishop
tags:
  - lightning
speakers:
  - Tadge Dryja
media: https://www.youtube.com/watch?v=6J5jd7wf6aI
date: 2018-10-05
aliases:
  - /scalingbitcoin/tokyo-2018/edgedevplusplus/lightning-network
---
<https://twitter.com/kanzure/status/1048039589837852672>

# Introduction

I have quite a while to speak. I hope it's not too boring. I'll have an intermission half way through. It's not going to be two hours. It will be more like 80 minutes or something. We are going to talk about payment channels, unidirectional payment channels, lightning channels, homomorphic keys, hash trees, watchtowers, discreet log contracts, oracles, anticipated signatures, DLCS within channels, etc.

I am Tadge Dryja. I work at MIT Digital Currency Initiative. It's a cool place. A few bitcoin developers work there. I wrote the lightning network whitepaper with Joseph Poon more than 3 years ago. I have no control over the lightning network. I'm not really working on it that much anymore. Other people are working on crazy stuff, that's really cool. I'm not even really working on discreet log contracts, instead I've been working on cryptographic accumulators for bitcoin and I've been working on that for a few months.

I am not going to talk about multi-hop payments because that was covered in a previous talk. I will talk about the basic structure of payment channels, though.

# Why payment channels?

It's kind of complex: why do any of this? Why not just use bitcoin? That's a legitimate question. There's a lot of weird conspiracy theories- a lot of people hate lightning network, and that's fine you're welcome to not use it. Even at MIT, an incoming freshman was telling me how lightning was a conspiracy by big banks to take over bitcoin. But really? I ride a bicycle to work. Where's my buy out..? Anyway, the real reason is scalability. Every transaction in bitcoin has to be stored by all nodes.

Satoshi posted on Halloween 2008, almost 10 years ago. He said he's been working on a new electronic cash system that's fully peer-to-peer (p2p) with no trusted third party. The first public reply was this person James A. Donald who said we very much need this system but the way I understand your proposal, it does not seem to scale to the required size. It was pretty interesting. He was right on the ball. So yeah, how do we scale this?

# 1-way channel

One way to think about bitcoin or the blockchain is that it's one wifi access point for the whole world. That doesn't scale very well. If you've been to big conferences, sometimes with 100s of people, wifi is pretty slow. You're all sharing the same transmission band for that medium. Similarly with the blockchain: you guys are all sharing the same blockchain and you compete for the scarce resources. In other networks, you break the network into hierarchies and you have routers and switches and you go between different points that way. If you're browsing the internet, then someone else doesn't see it. In the case of wifi, I can listen in. People might not be aware of that, and yes there's TLS and stuff, but if you're making DNS requests in this room then I can listen in on your wifi data and see that. Similarly with bitcoin, you can see the bitcoin data. So what about splitting it up?

# Payment channels

Let's make payment channels. Two people put some funds into a regular UTXO and they can move the funds between each other without updating tha UTXO. Who owns the UTXO changes, but it doesn't have to be broadcasted to the blockchain. There was an idea that was pretty old, before lightning, and these are incremental payment channels which are one-way channels. Transactions in bitcoin have a "lock time" field and you can say this transaction is only valid after a certain blockheight or after a certain time.

The idea is this channel is just a multisig output, a 2-of-2 multisig signature requirement. Normally multisig is friendly multisig where I have maybe three keys and I need two keys of them to spend or I do them with a friend or there's an exchange company. But this is more like adversarial multisig where we're worried about someone trying to steal our money. The simplest way is to have a funding transaction. Your input is Alice's money and she has UTXOs from her wallet and she gives 1 transaction input, and she sends 10 BTC to an Alice-Bob 2-of-2 multisig. That's pretty risky, because if Alice sends it, Bob can disappear and Alice would not be able to access her coins. Before Alice broadcasts that, she can specify that she wants a refund transaction with a locktime set in the future. This refund transaction has an input which has the funding transaction's txid and index, and it has Bob's signature on it. Bob signs the refund transaction before the commitment/funding transaction is broadcasted. Alice then can put 10 BTC into the funding transaction knowing that there's this safety of the refunding transaction. There's some small loss for Alice in time and some small fees but this is a small cost compared to having no backup plan at all. Also there's a timelock and the channel has to be closed before that because otherwise the refund transaction will no longer be valid.

This is restricted and this channel is one direction. Alice can keep paying Bob and Bob can't spend money back to Alice. The other restriction is that there's a set time period. Even though Bob knows he has those coins... in a week, there's a transaction which is locked and can't be broadcast but in a week it will be valid and Alice can use the refund transaction later. Before the end of the timeout, Bob needs to broadcast the most recent state or something. As soon as Bob gets the latest transaction, he can delete the earlier state. He never really needs to store the old ones because he would rather have more money.

# 1-way channel outcomes

Bob keeps getting half-signed transactions with more money going to him. The old transactions are useless and he deletes them. He needs to broadcast a new transaction before the refund transaction becomes valid. The refund transaction needs to be built before the commitment or funding transaction. You could use OP\_CHECKLOCKTIMEVERIFY to get around these problems... but basically segwit is what really enabled this to work.

# Lightning channels

* [Lightning network overview](https://diyhpl.us/wiki/transcripts/layer2-summit/2018/lightning-overview/)
* [Hardening lightning network](https://diyhpl.us/wiki/transcripts/blockchain-protocol-analysis-security-engineering/2018/hardening-lightning/)
* [Bootstrapping lightning network](https://diyhpl.us/wiki/transcripts/building-on-bitcoin/2018/bootstrapping-lightning-network/)
* [lightning network paper](https://lightning.network/lightning-network-paper.pdf)
* [The future of lightning (2018)](https://diyhpl.us/wiki/transcripts/baltic-honeybadger/2018/the-future-of-lightning/)
* [lightnig-rfc.git](https://github.com/lightningnetwork/lightning-rfc)
* [mit-dci/lit.git](https://github.com/mit-dci/lit)
* [c-lightning.git](https://github.com/ElementsProject/lightning)

The goal of lightning is to make bi-directional payment channels that can stay open indefinitely. How can you do this? How do you make a refund transaction? If it's time-based then you have a limited time duration. How do you revoke old states from earlier in the channel? How do you get rid of that?

There's some new timing-based opcodes that got put into bitcoin that helped us. One that is really big is OP\_CHECKSEQUENCEVERIFY which is sort of confusing and it doesn't sound like it has anything to do with timing. But it's a relative timelock opcode. Your input has to be at least this old in order to spend it. The timelock field on a transaction itself says that this transaction is valid "after Friday" or something. OP\_CHECKSEQUENCEVERIFY says this output is valid after it's 3 days old; it doesn't specify an absolute time, just a relative time. This is really important and useful. You might not know when the transaction is going to be confirmed in a block. You could specify number of block or number of seconds; and you say once this output has been confirmed, you can spend it after it has 1000 confirmations. How many confirmations does this output need before it's allowed to be spent?

Also, since it's an opcode, you can mix it with ohter things. You could say if you have key A and sign you can spend immediately, and if you have key B then you can sign but you have to wait at least a day or something. This is a useful opcode that we needed to make lightning network a reality.

# Revoke based on timing

What you can do, and the way you can provably credibly delete a transaction is that... how can you do that? You can use timing. You use OP\_CHECKSEQUENCEVERIFY and use 2-of-2 multisig which can happen immediately, or you can have this other key and then you have to wait 100 blocks. This is a little confusing because the keys you use here might not be used by Alice and Bob; they are just new public keys. So there's 2-of-2 multisig: if these two keys sign together then this coin can be spent immediately. However, if this other key signs, then it can also spend, but it needs at least 100 confirmations. This allows timing windows where in one condition there's an immediate spend but otherwise there's a delay.

So who generates these different keys for the revocation transactions? You make revocation transactions. You create a transaction which spends the funding amount output from early on in the protocol. Instead of directly spending to Alice and Bob in the revocation transaction, you make it more complex. Bob creates this transaction, signs it, and sends it to Alice. This is what sits on Alice's computer. The transaction that sits on Alice's computer does send Alice her coins and Bob his coins. But the rule is that Alice can sign and get these coins after 100 blocks, or Alice's revocable key and Bob's public key can sign together immediately to spend these Alice coins. And then Bob's coins just go directly to Bob, the same way as before. This transaction is held by Alice. A mirror image transaction is held by Bob, it's symmetrical but it's not the same exact transaction. It's sort of the same, it's the same template at least, except it's Alice and Bob flipped.

So the transactions are revealed, in order to revoke. Either party broadcasts and has to wait. Alice gives Bob the AliceR private key. Bob gives Alice the BobR private key. Now if they broadcast the counterparty can take all the funds while they wait.

# Add and delete states

So that's how you keep updating lightning channels. You create the initial state. The parties create the second state where Alice sends coins to Bob or the other way around. They create the new state but before it's a credible payment they have to revoke the previous state. Both parties reveal the private key that they were using to make it a valid transactoin. Once they revoke it, they don't want to broadcast it, because they know they will lose all their money because their counterparty can immediately spend all of the outputs because they had been given the private key. It's just toxic data at that point.

# Two-party indefinite payment channels

Now you have two-party, indefinite channels based on the construction I have described. You still need to create a channel to pay. You need one transaction to open the channel, one transaction to clos ethe channel, and potentially two transactions to close the channel in rare circumstances like adversarial circumstances. Cooperative closes are more convenient, they are faster, and nobody has to ever know that this was a channel. It will just look like a 2-of-2 multisig that spends to two regular addresses and nobody will be able to tell it was a channel so that's pretty cool.

# HTLCs

I am not going into depth about multi-path payments where Alice has a channel with Bob and Bob has a channel with Carol. Without opening a channel to Carol, Alice can pay Carol via Bob. This is with hashed timelock contracts (HTLCs). You know the preimage of a hash or you have some key and you have to wait some amount of time using OP\_CHECKLOCKTIMEVERIFY. Broadcasting this, if you want to spend this part of the script, if you want to spend with keyA, you have to reveal the preimage and then everyone can see it because it goes on the blockchain. This allows anyone else to collect the funds in a similar output script. This is very similar to the atomic swaps that were just talked about in Ethan's presentation.

You could make some optimizations. When we're talking about revocation keys where it was Bob's public key and a signature from this other key that Alice makes each state and reveals the private key, then you could make this into a hash preimage instead of a new key. In this script for the revocation transaction, instead of having Alice signs and Bob has this recovable 2-of-2... how about Alice signs and knows the preimage and Bob does a hash each time? Instead of a 70 byte signature, you get a 20 byte preimage. That's better. There was some talk about fancy Schnorr stuff and I'll go way into that soon. But you could add keys together. B + C = R. What's the private key for R? It's the sum of the private keys. If you take two public keys, add them, then the private key for that new key will be the sum of the private keys. This is easy and straightforward to do in the code. It's not super useful in ECDSA because you need to know little b and little c in order to sign in those cases. But in the cases we're dealing with here, one party does know both private keys. One party makes a 2-of-2 multisig transaction where they know both keys. So revealing something? This works.

# Reduced script

The reduced script is just KeyD or keyA and time passes. Or another key can sign at any point. The opcodes if you want to do that in script is OP\_IF keyR OP\_ELSE delay OP\_CHECKSEQUENCEVERIFY OP\_DROP KeyA OP\_ENDIF OP\_CHECKSIG. In reality there's a few other things in the real script to make it safer. Anyway, this allows you to revoke.

# Reveal key, revoke state

When you make all of these states in the lightning network channels, you need to keep track of all of the old secrets. Maybe you're paying per frame for the video you're watching. You need to store all of these old private keys. This is 32 bytes per key. You don't know which old state he might try to broadcast when cheating you later. Instead, you can build a hash tree where you can store log(n) secrets. I call this elkrem. It's a cheesy play on words: it's a merkle tree but backwards, with the arrows reversed. Often you come up with stuff and then later realize someone came up with that 20 years ago; it's called GGM and it was created 20 years ago. Anyway, you have a root, and you come up with a random number for the root. If you want to send, then you can to go left you can append the zero and then get the 2... but if you want to go right then you append a 1, and hash it, and get it. Left child, append a 0 and hash, and right child append a 1 and hash. Instead of trying to compute a parent, I can compute children by concatenating and computing and going left/right and down. So you have a sender that knows the root and can compute pretty quickly any hash in the tree, and you have a receiver that starts getting things. Once the receiver receives a later state, he can delete the previous state because he doesn't need those anymore and you can re-derive the original secrets. You only need to store log(n) secrets to protect against billions of different old states. That's kind of a fun trick.

# Watchtowers

Another idea is watchtowers... you have these output scripts, like KeyD || KeyA and time. KeyD is sort of the wrong or bad key. If this execution happens, then something went wrong. If you're spending with KeyD then that means someone had broadcasted a previous state going against the contract. That means someone is trying to take all the coins. A transaction spending KeyD is called a "justice transaction". Justice delayed is justice denied, especially in lightning channels because you need to be online. If you don't take it with your KeyD and the time elapses, then your counterparty can take the coins and they have then won and successfully committed fraud.

The idea of a watchtower is that you can create these justice transactions and grab all the coins as soon as you learn the private key for keyD because you know what the txid is, you will know how much money will be in it. It will be an invalid transaction because the inputs don't exist yet. You're spending something that hasn't been broadcast yet. But if that transaction gets broadcasted, then anyone could fill in those transaction details and your justice transaction will become valid. You can hand your justice transaction to a watchtower and say hey watch for something and if it occurs then fill in this transaction. You're trusting the watchtower to be online, and they can't take your money, in fact they can't even figure out which channel you were participating on. If the adversarial case occurs then the watchtower will see the details about the channel. But if everything works out okay then you can ask the watchtower to please delete the data and they don't need it anymore.

The watchtower could collude to not broadcast the justice transaction. So a good mitigation is to give your justice transactions to a bunch of different watchtowers, and to your friends, and then if anyone is online and watching then you're safe. But yes, there's no assurance that they will stay online and do this protocol. You still have privacy, though. And really you can run your own server and not use a watchtower at all. But it's a backup thing and you're trusting it will stay online.

Let's do a quick intermission and then I'll talk about discreet log contracts.

# Discreet log contracts

* <https://diyhpl.us/wiki/transcripts/discreet-log-contracts/>
* [discreet log contracts paper](https://adiabat.github.io/dlc.pdf)
* <https://github.com/mit-dci/dlcspec>
* <https://github.com/mit-dci/dlcoracle>
* <https://github.com/mit-dci/dlc-oracle-nodejs>
* <https://github.com/mit-dci/dlc-oracle-go>

Most of finance seems to be about bets. They don't call it betting. It's conditional or contingent payments. Whether it's insurance or some other type of trade or bet, there's contingencies about who pays whom. It's payments conditional on some external data. In this example, say Alice and Bob bet on tomorrow's weather. If it rains, Alice gets 1 BTC. If it's sunny, then Bob gets 1 BTC. The problem is that the bitcoin blockchain does not have an OP\_WEATHER and now we have to soft-fork in OP\_WEATHER and know what the weather is in. But wait, the bitcoin blockchain doesn't know about the weather. How could it? It just knows bitcoin stuff.

Lightning network is a simple script, enforcing the most recent transaction. That's a smart contract. It's an internal-only smart contract; all the data and keys are generated by the channel itself. There's no outside information coming in. This is clean and easy to implement. But if you want some kind of external data to come into the system such as the weather then you're going to need something called an "oracle", a mechanism by which the real world can get into bitcoin.

One mechanism where real world gets into bitcoin is mining, where you have to expend electricity to get new coins. But the rest of bitcoin can operate without real-world data going in. The simplest way to do an oracle would be a 2-of-3 multisig contract. You could also do 2-of-2 where there's no oracle at all and Alice and Bob just go into 2-of-2 and they just agree that if it's rainy then someone gets coins or someone else gets the coins in the case of sunny. If they are friends then this works, but bitcoin is the currency of enemies. 2-of-2 would make this based on trusting your counterparty. Wealthy players can just wait out the poor players, too, and negotiate and say instead of 1 BTC how about you get 0.8 BTC or something. So maybe they just wait a few years and give up until the other party agrees to get only 0.8 BTC or something.

You could use an escrow scheme like 2-of-3 and there's some companies that do that I think. This is the multisig oracle construction. There's 3 keys: Alice, Bob, and Olivia. If Alice and Bob are chill, then they can both sign without contacting Olivia. If Alice and Bob fight or are unresponsive, one of them can ask Olivia to sign. The problem is that the participants can bribe Olivia since Olivia was already part of this 2-of-3 multisig. Alice can influence the multisig oracle to say the wrong thing and get paid for doing this.

2-of-3 multisig oracles are interactive. Not only do they see every contract, they decide the outcome of every contract, individually. They can equivocate: Olivia could sign "it's raining" in one contract and sign "it's sunny" on another contract at the same time. How are you going to know? Maybe people will publish this but it's difficult to discover this. It would be better if the oracle couldn't equivocate and had to stick to a single answer. It would be better if the oracle had no idea that the contract exists. That would be really cool, but how do you do this?

Well, remember the revokable transaction technique. We're going to use the same exact scripts as regular lightning network channels. But before I get into these details, I am going to talk about elliptic curve math operations. Some of this should be kind of familiar like multiplying by G (the generator).... in elliptic curve signing, you've got two types. Lowercase letters are scalars and uppercase are often points on the curve. What are the operations we can do? Scalars are regular numbers, sometimes modulo some prime number. You can add, subtract, multiply, divide these scalars. They are just big numbers. It's efficient to add, subtract, multiply, and divide. And then you have these curve points. You can add them, by drawing a line between them and see where else that line intersects the curve. You can also subtract them- you can negate them, and you just flip it over the x axis. You can add, subtract, that works, it's a bit slower but a computer can do it quickly. But what you can't do is multiplication and division. There's no notion of A * B. Multiplication is not defined, and similarly, division is not defined either. You cannot add a point and a scalar, that's a type error like in programming languages. Multiplying by G is sort of casting a scalar to a point. You can multiply a curve point by a scalar. Adding points and scalars is undefined. Point times scalar is OK; repeat the tangent doubling process. Division by scalars is also possible. You can pretty efficiently multiply a curve point by a scalar; but this is the biggest CPU cost for verification in bitcoin. So you can add, multiply, divide scalars, and you can take curve points and multiply them by scalars and divide. So you pick some random point G, and we call that the generator. That's a point that we all agree on and there's nothing particularly special about it. It loops back to itself- if you multiply G by itself enough times eventually you get back to G. It takes a long time though. You can add pubkeys: sum of the private keys gives sum of the public keys. Fun stuff ensues from this. Since you can't divide points, you can't get a scalar back out. You can also add pubkeys.

In discreet log contracts, we use this to make a non-interactive oracle. In lightning, we reveal private keys and then add them up in order to revoke a state. But in discreet log contracts, the oracle reveals a private key, which allows a key to be broadcast.

# Schnorr signatures

Real quick about Schnorr signatures-- it's sort of on your shirt. I don't know what D is on your shirt. It's sort of like a modified or fancified Schnorr signature on your t-shirts. It's pretty similar. Anyway the straightforward way is that you have a public key A = aG. You also make a key pair that exists only for this signing process, so a nonce k which is random, and you call R = kG it's the public key version of k. This is usually called the nonce for the signature. To sign, you compute s = k - H(m, R)a. The nice thing about this is that it's all scalars, there's no curve point operations. You take k, which you made up, and you take the hash of (m, R) and this gives you 32 bytes and you multiply it by your private key which is also quick, and then you subtract that from k. And your signature is just (r, s). For someone to verify, they will have to do some elliptic curve operations. If you multiply both sides of this equation by G< you get another equation. These terms are all known to the verifier. To verify, you ask whether sG is equal to kG - H(m, R)aG. So this is how you do a Schnorr signature.

# Fixed-R signature

You switch the signature around a little bit for discreet log contracts. You can only sign once using this different construction. The pubkey can be A but you could also have a pubkey (A, R). Previously the signature was (R, s) but you could have pubkey (A, R) and the signature can be just (s).

# k-collision

Say I sign twice with the same R and the same a value. What this means is that there is going to be signature 1 and signature 2. The k value will be the same each time. If I use the same key and the same message then that's fine. But if I have two different messages, then I have s1 and s2 that differ only in this hash, the coefficient of a. What the verifier can then go do is that they don't know k or little a, but they do know s1 and s2. If s1 - s2 = k - H(m1, R)a - k + H(m2, R)a = (H(m2, R) - H(m1, R))a and then you can compute the value of a by using a = (s1 - s2) / (H(m2, R) - H(m1, R)). So now you can solve for a. This is pretty bad. Fun fact, this is what brought down the Playstation 3 code signing. This is how I learned about this. Sony always used the same k value. k was random looking but it was always the same. So then anyone could play pirated games on the Sony Playstation3 console. I think a bitcoin wallet had a problem with nonce reuse. Watch out for nonce reuse. Generally, we use RFC6979, which makes k a function of the private key and the message. If you take the hash of the message and little a, and use that for k, then that's safe. If you sign with a new message, then you get a different k.

# Anticipated signature

What can we do here with this new redefined Schnorr signature? It might seem worse: you can only sign once. But for this oracle signing about the weather, being able to sign only once might be a feature not a bug. So we ask the oracle to pick a k nonce, multiply it by G, give us R today. If you sign two things, then you could get the private key, and you could ask the oracle to put some money on that private key on the blockchain so that there's a fidelity bond on the line. Given the "pubkey" (A, R) and a message m, you can't compute s (the signature) due to the elliptic curve discrete log problem. However, you can compute sG = R - H(m, R)A. You can compute sG. Normally this is only done for verification. sG is a point on the curve. You don't know the scalar, you don't know s. But you do know sG. This is just a keypair like any other public-private key.

# Signatures as private keys

It's an unknown scalar, but you know what it is times the generator point. Hmm, this sounds like a keypair. Use this for a third party oracle to sign messages, revealing a private key. That signature is a private key that you can use to spend money. Olivia's signature is a private key. sG is a public key. Mix with Alice and Bob's public keys.

In lightning network, states are added sequentially, and validity is enforced by revealing private keys to previous states.

In discreet log contracts, you create all the states at the same time. You don't know which will happen, but you create all of them upfront. Which one is valid is determined by which signature the oracle produces. The oracle is essentially endorsing one of the states. In discreet log contracts, you don't have to worry about going offline for a month and losing money or whatever. But when you come online, you have to broadcast two transactions at the same time. That's the only timing constraint you have. You sweep the output as soon as you make it.

# Discreet log contracts within channels

You can do a lot of cool things with discreet log contracts. If the parties are cooperating then you can make these contracts within lightning channels. You can use "nested contracts". You can use multiple discreet log contracts per lightning channel. This is a good use case for SIGHASH\_NOINPUT where you would use SIGHASH\_NOINPUT for the subcontract discreet log for these signatures because then you're not referencing the txid of this output, just the key, and then when the txid changes that's not a big deal. TXID of the parent changes, but the discreet log contract can stay the same and you don't have to resign.

# Discreet log contract use cases

Currency futures, stocks, commodities, sports, insurance. It's fairly general- it can be any kind of smart contract where you are making a contingent payment based on some event. There's a bunch of "stablecoins" out there like tether which are kind of sketchy and they are not cryptographically secure. With discreet log contracts, you would still be dependent on an oracle to publish the right price, but this seems better than asking someone to hold on to millions of dollars for you. You can have a contract related to the price of bitcoin and depending on the price you get more or less bitcoin. You can do a contract where you have a fixed dollar value of BTC, and the other side is someone who wants super volatile bitcoin price action.

# Current state of the software

Lightning network: there are many people working on different implementations. I've been trying to keep up, but there's a lot. There's ACINQ, Lightning Labs, Rusty's stuff, my stuff (lit). Discreet log contracts- there's MIT DCI doing lit, DG and CryptoGarage, and others. Lots of interesting problems are remaining.
