---
title: Socratic Seminar 3
date: 2019-10-14
transcript_by: Bryan Bishop
tags:
  - miniscript
  - taproot
---
<https://www.meetup.com/Austin-Bitcoin-Developers/events/265295570/>

<https://bitdevs.org/2019-09-16-socratic-seminar-96>

We have sort of done two meetups in this format. The idea here is that in NY there's BitDevs which is one of the oldest meetups. This has been going on for five years. They have a format called socratic where they have a talented guy named J who leads them through some topics and they try to get some discussion going on and pull from expertise in the audience. We are facilitators, but not experts, so don't expect us to know everything. Everyone is here to learn. Let's do a round of introductions to say your name and what your role is.

# Miniscript

Let's start with miniscript. I'm not even going to try to explain it. Andrew? What is the problem that miniscript is going to solve? Miniscript is a scheme for writing bitcoin scripts in a structured way. The problem with bitcoin script is that-- a lot of people are unaware that bitcoin has a scripting system. It's possible to do more things than assigning coins to a ke. You can have arbitrary sets of signers, hash preimages which is how lightning HTLCs work, and arbitrary sets of timelocks and you can combine them in whatever ways you want. The scripting system is not really designed to do automated reasoning about. To come up with script, you need to get a bitcoin expert woh will write special purpose code for fee estimation and one-off ad hoc security analysis to convince yourself that the script is doing what you expect it to and won't do things that you don't expect it to.

((switched to an actually usable keyboard))

If your user wants to do all sorts of weird stuff, sucks to be them becaquse you can't support them with your infrastructure because you need to know the one script you're coming up with is the one where you're actually a signer. Without miniscript, this is impossible. Without miniscript, you would need to write the blob at the bottom. The red thing at the top is kind of cool. You take all of the opcodes at the bottom and decode it into the red thing. The thing at the top is a list of spending conditions and how they combine. The stuff at the bottom is a bunch of machine execution opcodes for a stack machine that only incidentally represents spending conditions and operates on opaque data that is sometimes integers sometimes signatures and you should really make sure you're correct. This is normally hard to read because it's hex, or even in this opcode representation it's hard to read. You also get a readability benefit. The big thing is that it has a structured of spending conditions.

Q: Could this be combined with PSBT?

A: PSBT at its core is simple. It's a standardized format for bitcoin transactions. It's tagged output data. PSBT as a protocol defines a whole bunch of roles like the signer like a hardware wallet that inspects the transaction and produces a signature. It's straightforward and doesn't need to understand much. The creator is a tool that takes an unsigned transaction and takes some data. There's a role called an updater which says oh these outputs are mine and here's some script spending them, here's a derivation path for my keys and that's straightforward. The most critical part of PSBT is a finalizer which has the job where for every input it takes all the signatures attached to all the keys, and all the data involved, and assemble that into a complete transaction. It takes structured PSBT data which has data appropriately associated, and then you need to assemble a witness with the right signatures in the optimal order and you insert 1's and 0's to choose different script branches. The job of the finalizer is very complicated. It needs to do a lot of things to build a transaction out of this data. A finalizer is typically something that wallet developers need to write on their own, but miniscript lets you write a fully general finalizer that can work with many different wallets and it can be an off-the-shelf tool that you can get interoperability from. Miniscript encodes as script; your script is already in the PSBT, and miniscript lets you parse the script into this structured thing. You can parse existing scriptsi nto miniscript, do the analysis, and then figure out which keys and signatures you need.

Q: How will this interoperate with taproot?

A: We will basically need to double the size of miniscript for taproot. Miniscript is designed to encode as bitcoin script; taproot has a new version of bitcoin script, with some subtle changes a lot of which were designed to make miniscript easier to implement. Tapscript, which is the script part of taproot, we would need to add a few more opcodes to miniscript like the merkleized pruned branches thing and also the new way of doing multisignature in tapscript.

Q: What are the major differences between miniscript and other attempts at -- like Ivy and Simplicity?

A: Simplicity is in its own category, which is a whole replacement language. Ivy is a good example though. Miniscript is not compiled. It's not about writing in a high level language and trusting that the output matches the input. Miniscript is just an encoding of script, which means that first of all you don't really need to trust that the output matches the input because you can check yourself by stripping off data. Also you can go backwards from the script to the policy. Miniscript is not a higher level language, it's just a better structured version at the same level. This is what script should have been.

WT: How certain are the developers that the consensus is the behavior as you expect?

A: Very certain, for two reasons. On the screen, there's 26 fragments and they are all small and straightforward. And then we didn't use the weird somatics, except OP\_CSV takes a 5 byte number where the other ones take 4 byte numbers.

# Bitcoin optech newsletter

A cool thing is the bitcoin optech newsletter. I am going to skip a few. They made a wallet compatibility matrix. They are pushing for segwit usage. Whaever wallet you're using, you can run through and see what features they supopot. This is useful when choosing an exchange or something like that. They had a 27 week long series where each week's newsletter included a section about segwit, like how to implement it and why to implement it. Anyone curious about segwit would find that useful and go back and scroll through those. They are pretty short reads.

Q: Are there any big surprises in that compatibility matrix like someone not doing so well, or someone doing really well?

A: Not really. One thing that I thought was cool was that sometimes you see things like, Wasabi wallet, they have all the good stuff but the new wallets are like not even bothering to code the legacy stuff which is a little annoying if you want to receive funds on a legacy address on -- like receiving native segwit wrapped. You can send to them, though. They just want you to feel the pain if you're receiving from an old wallet, and force them to upgrade. That's good; I don't blame them.

... a lot of them support pay-to-pubkey-hash which is sort of like the single sig, just using one hardware wallet. ... There's also some weird address length restrictions. Some of them support bech32. Any comments about this or experiences with segwit adoption-- does your wallet use it? Any thoughts about it? Okay, we can keep moving on.

# Notable code changes

Here's one notable code change that I thought was interesting. Nicolas Dorier made btcpay. He has a pull request open to allow a whitelist for bloom filters. If you have a lite client, like on your mobile phone, they have a whitelist feature where you can basically just allow -- it's another way to use your full nodes and talking to lite clients. Any thoughts about this?

Q: Why a bloom filter instead of like asking friends?

A: It was one of the first attempts to do a lite client so that you could run a wallet and verify your transactions without having to have a full blockchain of data. So you would send bloom filters to a full node that supports this feature.

If you know how bloom filters works, it was done back then as a way for lite clients to not synchronize the entire blockchain but it has major drawbacks in both privacy and also security where a bloom filter as an end user is not really a bitcoin user, you're not verifying anything for yourself and trusting that the server you're talking to is telling you the truth and it's not recording all the filters that you ask for... it's basically like giving all your addresses to them. So this kind of wallet has become less and less important over time. The other reason aside from bad for your privacy and security, it was also very bad for bitcoin nodes. It opened the bitcoin full nodes to a trivial DoS attack. Trivial low-bandwidth DoS attack. With extremely low bandwidth, you could cripple most of the nodes around the world. As a result, many people have turned off bloom for many years now, by default. Since then, there's bip158 neutrino which doesn't help with privacy but at least it's not a DoS vector for full nodes. Some people call it controversial because it encourages use of bitcoin without verifying anything for yourself; but some other people would call that a necessary evil. But then you should learn about assumeutxo.... so there's a lot to this story. By having the ability to whitelist or blacklist bloom, I didn't even know that somebody had a pull request for this. It's really good. Bloom is the lowest bandwidth best way for you t oconnect to your own full node preferably over a full node, because you trust yourself to fully index so your phone client using your own full node is also sovereign. But yes, you could just use RPC. If you have bloom enabled, the entire network could be crippled at very low cost.

Q: How did this ever get merged?

A: Do you want the polite answer or not? Some people prioritized user adoption over privacy and security. There's a tradeoff when you do so in a reckless manner, maybe. Bloom is way less bandwidth and faster if you use it in a secure manner to your own node, than neutrino. So it's still useful. I just wouldn't enable it by default, unless you're accepting the risk of your node getting DoSed.

Q: Why haven't we seen a DoS attack? With bip66, there was wide-spread flipping the s value and it was havoc.

A: p2p nodes aren't using bloom to talk to each other. There's a memory exhaustion attack; I think it was fixed before it was public. It was never totally fixed. Bloom was first added in v0.7 or v0.8. Ever since then, they have added more and more mitigations to Core that would reduce the ability to cripple the node but it's never fully protected. The other reason to not use it, especially over the normal unencrypted unauthenticated p2p connections is that there's no way to know that you're being mitm'd. So somebody could trivially intercept that and spy on you, filter you, or lie to you. So that's another reason-- there's many reasons to want- I don't know if it was officially given a number, but bip324 was a replacement for bip150 and bip151 which was encryption and authentication as an option for p2p connections. You generally want that for all kinds of reasons. You should encourage developers working on that as an option for the future of p2p connections.

# Signet

Regtest is a mini version of a network that you can spin up on your computer as a test. Now there's a new signet thing. Has anyone used signet? Could you give a tldr on it?

<https://diyhpl.us/wiki/transcripts/scalingbitcoin/tel-aviv-2019/edgedevplusplus/signet/>

# SNICKER

SNICKER is like this interesting coinjoin proposal. Basically where if you can figure out who owns, given a public key on the bitcoin blockchain, you can prepare a bunch of coinjoins and they might choose to do it. So you send it to them, and they might choose to take you up on it. It could get more popular when taproot hits, because taproot is mostly pay-to-pubkey so the pubkeys will be a little more visible. You don't need to know who owns it, and it's cheaper than the normal coinjoin, and it's no interaction.

Coinjoin is a privacy mechanism in bitcoin where a bunch of people decide to combine transactions and then give a bunch of outputs with all the same amounts and it can hide where your BTC came from. However, you don't know who is the maker of this transaction. SNICKER has some better privacy guarantees and it's cheaper.

# Rapid fire random things

Here's a cool python script that someone made, that can print out a graph of who was mining at a given time. You could make an animation I guess.

Here's a new block explorer I haven't seen before; it does mapping of inputs and outputs. I don't really understand this thing yet, KYCP, but it looks quite interesting. There's some boltzmann analysis to quantify how some privacy measures, I'm not really sure. I tried it once. Know your coin privacy. So kind of the aim of this block explorer is to show how much is visible and revealable on a given transaction. So most of this is focused on your privacy. It makes it easy to go back in time and look. I think it's one of the folks from Samurai. I think it's Chainalysis? No, that's blockchain.info. Ookay, moving on.

This is projectmempool.space which has a bunch of cool graphs, like utilization of the mempool. This is thransactions that are waiting to be confirmed. This is the rate that people are paying to get into the blockchain, graphed over time.

# Bitcoin codebase deep dive

This is doing some analytics on activity in the Bitcoin Core repo. On some days of the week there's a lot of activity, but not on the weekends. Also shows you the number of commits; it's increasing over time generally. Here's the analysis of how long the code stays around I think. I think that's what it is. What is the burndown analysis? It doesn't really make sense though-- so this disappeared immediately?

# Rapid fire again

Chainalysis mentions that most mixed bitcoin are not used for illicit purposes. This was an interesting article in Bitcoin Magazine. Wasabi Wallet has received $250m year-to-date and it's going vertical. So that's cool. Then there's an analysis of this maker market, a successor to silk road. Bitcoin still remains the main mode of payment, and Monero is not. It's the dominant payment method, so that's interesting.

This is a hack on EOS. There was a smart contractu sing an on-chain random number generator based on blockheight, and someone was able to steal an ungodly amount of money out of the smart contract because they were using a blockchain-based RNG. Any comments on this?

Here's some new stuff on the Bitcoin Core GUI. This one allows you to disable private keys for a watchonly wallet. PR 15450. So that's cool. Here's a new GUI for Bitcoin Core using pruning and reducing the amount of historical blocks you store. Also there's a bunch of transcripts from Bitcoin Edge Dev++ conference.

A few of us also went to the optech bitcoin taproot workshop, the publisher of the optech newsletter. It was cool. It was a bunch of python code in jupyter notebooks. You install a version of Bitcoin Core with the taproot bip code running, and you're able to write transactions against that and you can learn how taproot works against that. There's very indepth examples made by the Chaincode Labs residency people. They might be interested in doing a taproot one day seminar or workshop.

# Lightning stuff

The lightning section is kind of small this time. There's a few things I've been reading as well, tangentially related. One thing that I found interesting that Justin kind of touched on which isn't on this list, I'd bring it up anyway, is the discussion on the bitcoin-dev mailing list about the nomenclature about using the word address. I thought it was an interesting point for discussion.

Q: What's wrong with an address?

A: The word "address" encourages address reuse. People think of it as a bank account or mailing address or email address. But really addresses should not be reused. It has problems with security and privacy.

Another issue is that people think coins from addresses, which caused a lot of money loss ever since bitcoin was created there was confusion about that. One thing that we were talking about with Wasabi earlier, is that it forces you to think of each transaction that you receive. They don't let you reuse addresses, and it makes you tag every transaction that you get in. Addresses also obscures what's going on with UTXOs. Every time you receive a transaction, you have to spend that entire output. What Wasabi by thinking of it and bcoin has this in the code at least, thinking of it more like coins. Each time you receive something, it's a coin. To make a new transaction you have to combine coins and make coins. They suggested invoice IDs, payment tokens, bitcoin invoice, address in paranthesis to not confuse people too much. Bitcoin invoice path. Bulla is something someone else talked about. It was an old form of money where you put a thing of value into a clay container and stamp what was in the container on the outside of the clay, and the only way to really redeem it was to break it. It's a similar to a UTXO. You can only spend it by destroying it and making a new UTXO. Nobody would know what a bulla is, though. (Jokingly, maybe Wasabi takes the coins when you do address reuse, as a security service fee.)

Q: What about saying, "send it to this coin" or "this lock"? Someone suggests, "send it to this thing". Unfortunately "lock" sounds too close to block.

UTXOs are really new things when it comes to exchanging money. There's no real analogy. People find this confusing about bitcoin; that it's a script and a lock. Maybe it's better for adoption to make a new name, so that people have something to grasp on to.

# Reconciling on-chain and off-chain with eltoo

I'll try to briefly explain what eltoo is. Does everyone know what lightning is? Okay. Lightning currently uses this script format in bitcoin transactions to create this off-chain mechanism. These are called HTLCs, hashed timelock contracts. It's similar to what we were seeing before, like miniscript, not exactly, it's more complex scripts not just paying to a public key that encodes current conditions. One way that lightning allows for this off-chain protocol is that you have two parties that enter into a multisig contract and they both have to agree unlock it. When you're paying each other, it's just two people, and they basically agree to rebalance the payout of that contract. One of the problems is that what happens when you don't trust the other party. So say the other person takes an older agreed to version of your contract... There's a punishment mechanism, where there's a chance to steal the entire value of the contract.

eltoo is another lightning proposal.. it's confusing, if you talk about naming schemes. Eltoo is another way to do payment channels without having to keep track of every intermediate state. What it does is that the original proposal gives a new way to update the agreement about the state of the channel. Rather than have this penalty mechanism, what it would do instead is it would introduce SIGHASH\_NOINPUT --- and the sighash is the signature hash, and when you're signing to release a UTXO, it's a descriptor on your signature just a byte that says here's what I'm signing in the transaction. It's what you're locking in or committing to. NOINPUT says that you're commiting to a bunch of stuff in the transaction which does not include the input id. In normal circumstances, thsi is very risky because you're allowing anyone to plug in a valid input that would match with your signature and say okay with this input then this transaction is valid. You can sign a transaction and anyone can update the inputs. Thsi is useful for an off-chain protocol like lightning because what we can do is rather than relying on the punishment mechanism where I have to keep track of the states, every time we update we update a number in the transaction and say okay we're moving from state 3 to state 4 but we're not committing to the input.

Q: Can you only react before it gets committed in a block? Or is there a locking?

The underlying mechanism here is that every state update is able to spend the coins from any previous state. So if someone tries to steal by publishing state 2, and state 4 exists, state 4 is able to chain off the original coins like it should, or any of the prior states. Whatever hits the chain, you can publish state 4. The states are sequence numbers. Eltoo uses OP\_CSV and it looks at the sequence number. So the output of state 4 says that anything higher can spend this. OP\_CSV largest size is 4 bytes. Some of it is used for timelock. There's a range of numbers you can use for this mechanism.

What was interesting about this is that, cdecker who is one of the authors of the eltoo paper, makes this mental model connection between eltoo this kind of update mechanism and the utxo mechanism that we already use on-chain. And so he, I don't think he proposed anything concrete, but basically he says, you can re-duplicate bitcoin-like mechanisms using eltoo because if you think about it when we're talking about a UTXO we're talking about a previous state which gets destroyed and we're going to move it on to this new state that we agree to. He suggests that using this mechanism, you can reconcile on-chain and off-chain models with eltoo. So that's pretty cool.

There's also a python implementation of eltoo by Richard Myers who works at gotenna. It's pretty interesting.

Some people are concerned that SIGHASH\_NOINPUT cannot be considered safe because users might be stupid and use it in inappropriate situations. There can be double spending situations that arise if users aren't careful. How much are protocol developers responsible for protecting users from bad wallet designers? I don't think there's a right answer. There's people on two sides of it. This has introduced some more discussions like, should we call it SIGHASH\_NOINPUT\_UNSAFE. Or maybe chaperone signatures where you have to opt-in, and also output tagging which is another way to lock in and be explicit about it. So it's an interesting idea. I don't know if anyone has any input or opinion on how much we should protect dumb users from doing dumb things. It's not even protecting dumb users; it has to be done by wallet designers. A user would have to be opting in to using a wallet that has decided to use this unsafe feature. My personal opinion is use it at your own risk. There's all kinds of ways for wallets to steal your money. But this is not a hypothetical problem; there have been dumb wallet designers in bitcoin as well as shitcoins.

You could do vault-like systems with NOINPUT. There's a concern that people would be too experimental. But again, use it at your own risk.















