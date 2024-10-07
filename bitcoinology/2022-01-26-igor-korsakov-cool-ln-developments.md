---
title: Cool Lightning Network Developments
transcript_by: kouloumos
tags:
  - lightning
  - client-side-validation
speakers:
  - Igor Korsakov
date: 2022-01-26
media: https://www.youtube.com/watch?v=5pmfNOUQg_s?t=285
---
## Synonym

Igor
Synonym is a company that [John Carvalho](https://twitter.com/bitcoinerrorlog/) started and he is trying to put Web3 inside of Bitcoin. But what it consists of? They're using several things like identities and people hosting their own data.

### AOPP

For identity, the first thing I want to mention is Address Ownership Proof Protocol (AOPP). This is the field that we added in BlueWallet some months ago. I think it was a Switzerland exchange that wanted this, so they sent us a pull request and we merged it ([PR#2915](https://github.com/BlueWallet/BlueWallet/pull/2770), [PR#4431](https://github.com/BlueWallet/BlueWallet/pull/4431)). Basically, the Switzerland exchange for compliance reasons, wants to be able to send out funds only to the addresses users prove they own. The way they do it is they sign an arbitrary message with this private key that's associated with an address, and this is how they prove that they own the address. So the way it works is that the user scans the QR with with his mobile wallets. He scans the QR on the Switzerland's Exchange website and this QR code says "this is the arbitrary data, please sign it with your private key and post the result to this API endpoint". So that's what wallet does. Of course it's asks you if you want to do it, if you want to proceed, this is what you're doing, if you agree with it. If you say yes, yes, yes, in the end, you sign some random data with your private key and you post it to the API endpoint. This is how you prove that you own the address.

One of the ideas of the Web3 is that users can carry their identities with them and always prove that they are who they are. But how can you put it in Bitcoin? This is how you do it, not with this (AOPP), this is just a very specific thing for like some Switzerland exchange, but the general idea is that you sign some message, you prove you own the address and this is going to be your identity which you carry with you across some websites, some forums, some blogs. And since we've got HD wallets, which carry a lot of addresses, we can issue a new identity for each website we visit. I guess it works a little bit differently in Synonym but the idea is still the same. There is no way around this, you still have to sign something with your Bitcoin private keys. You've got the HD wallets, you've got lots of addresses, a lot of identities. This is how you do it.

### Hypercore

Now you own the address, you prove your identity and you want to share your data with some peeps on the interwebs with some blogs, forums. So how do you do it without giving up your privacy or self hosting your data? We know for a fact that people don't want to run servers. We tried that, people just don't do it, not the majority of them. So Synonym took the pretty cool thing which is called [Hypercore](https://hypercore-protocol.org/). The Hypercore is a protocol. I like to think about it as the personal torrents which are friendly for developers. The Hypercore is basically an append only binary log, which involves Merkle trees. The one who started the Hypercore can always prove that this is the data he wrote, and no one can alter it because it's authenticated by some private key. So this is the connection of owning private keys with Hypercore. I as a user can probably prove that I own this address and I can start the Hypercore with the data I own and sync it to other parties. Hypercore is very efficient. Basically acts as a torrent, so you can share it to multiple parties and it gets synced very fast and efficient. In fact, one of the cool demos I saw for hypercore is that some guy started a video streaming through hypercore and shared it to his peeps. Basically, video stream is a stream of bytes, so you can share this binary log to other people and they catch up pretty fast. They read it, they catch up to the top and there are synced. So you can watch the video from real time.

So why not put my personal data in Hypercore. With hypercore you have the ability to not just share data, you can add some more custom rules like, this specific shard or whatever is going to be writable for someone else authenticated by this public key. So these terms are tree like structure, which involves cryptography, which no one can alter, except me or whoever I approved and this is how I'm going to share my data.

It's peer-to-peer. Of course there is no magic, so there are exchanges of peers involved. If you are running the Hypercore by yourself you need a central entity where peers are going to register. This is basically a torrent.

Audience
You said before the problem was you've had various people trying to run a server of their own, they won't keeping it there, right? So presumably, you'd be holding on to a lot of people's data.

Igor
No, no, you're holding your own data, because you're seeding your hypercore. So as a user, it could be even transparent. You don't even know that you're hosting hypercore for your own data. You're sending it to other peers and other peers who want to check out your data, see your blog posts, they just discover you and they stream from you.

Audience
It's still data you got, outside of the address. What we've done is that we confirm the address and then there's data which is user information, right? Where is that held?

Igor
You go to some website, you see other people and if you want to check them out, you connect to them.

Audience
So the site has the information?

Igor
Yes, but not your information, only the information that you--authenticated by your public key--have this information. It's like a fork in the road and you see a sign and this sign says if you go there, you'll get this.

Audience
What's the source of the information? Where is the original data?

Igor
On your own host. No one's gonna host it for you. You're saving it yourself, but it's p2p, when many people join, they can stream from other people, not just from you. But because it's a Merkle tree it's provable that no data was altered when it was delivered to other people. So the p2p peers can verify that it's unaltered and it comes from you originally.

Audience
Do you need to be online the whole time?

Igor
For the initial sync. Once you seeded it, you are good. Well, maybe no one cares about you, you don't have any peers and when you're offline, you cannot seed it. But if you have a network of friends, they can seed your data to each other when you're not around.

Audience
...reputation?

Igor
This is how I understood Synonym, this is what John works on. If I got it correctly there should be reputation involved. I don't know where exactly, but somewhere here.

So this is Hypercore. Hypercore is a pretty cool thing because it wasn't made for Synonym or by Synonym. It's a pretty old product, so you can go and check it out. It's basically torrents friendly for developers. If you need some kind of a sync of binary locks on your host or something, you can try it out and maybe it will work for your own application. So just go and check out Hypercore, it's pretty cool, I tried it.

### Tether

Synonym as a company, [is a Tether-owned company](https://twitter.com/Synonym_to/status/1460781354308808705). Tether is a stable coin, the biggest one. If we could have one shitcoin, one shit token it could be one from Tether and we don't need anything else. It's funny that people are always concerned that Tether is gonna fall once people find out that there is no backing of this Tether. But who cares, dollars isn't backed by anything, british pound isn't backed by anything, like who cares? When all this ends we still use dollars. I think Tether will live long and happy life.

### OMNI

Tether originally runs on OMNI protocol. I think about Tether as a meta coin, they adapt, they survive, they change. If Ethereum dies they don't care. they can run on Solana, if Solana dies they don't care, they can run on whatever. So a bunch of shit coins they can run on all of them. They don't care. But they keep their hand on the pulse so they can check out if it's dying and just migrate. But still, they run on that [OMNI layer](http://www.omnilayer.org/) and that's the original protocol for issuing tokens on Bitcoin blockchain.

The way it works is that someone puts a transaction on Bitcoin blockchain and puts the [OP_RETURN opcode with with some data](https://learnmeabitcoin.com/technical/nulldata). They create an OP_RETURN output with prefix OMNI and the rest is data. And this data is usually very basic operations, like issue token with this ID, move this token if I own it, multisig, batch send for airdrops. It's not UTXO, it's kind of an account based. This specialized software, which they call OMNI daemon, can parse the whole Bitcoin blockchain and check out all those OP_RETURNs with the prefix OMNI, and create accounts map for everyone who issued something, who moved something and basically keep track of all the OMNI tokens that were created and moved and who owns how much. USDT is one of the tokens on OMNI protocol.

This works on the Bitcoin blockchain, so every time you are making a transfer, you're creating a Bitcoin transaction and you can move your USDT or any other tokens.
How do you put it on lightning? That's a good question, right? The way to do that on lightning, is that they have a multisig on OMNI and they trade a state channel with this multisig on OMNI. So they create another Bitcoin transaction where one of the outputs is going to be funding transaction for regular lightning channel. Of course, it's not a regular lightning transaction because it involves locking some OMNI tethers, some USDT.

Audience
So this is just gonna be a normal channel open but it's just gonna have the OP_RETURN for the thing.

Igor
Yeah, but the channel open is not going to recognize by regular LND. Because they had to take the BOLT (the specification) and they called it [OmniBOLT](https://github.com/omnilaboratory/OmniBOLT-spec). So they took the specification of regular lightning channels, they altered it a little bit so it suits working with this OP_RETURN outputs where everything happens. It's not inside the [Bitcoin script](https://learnmeabitcoin.com/technical/script), everything happens inside of Omni multisig. So regular LND cannot work for this.

Audience
...Inaudible...

Igor
Yeah, you have to have collateral. You need to have USDT first to lock it in the channel, kind of like regular Bitcoin when you create lightning channels. So you take your USDT, you create a channel with some counterparty, you fund the channel with your USDT. Of course, there is another output for regular BTC because you cannot fund punishment transactions with USDT on Bitcoin blockchain, you have to have a little bit of BTC for close channel transactions.

Audience
...Inaudible...

Igor
When someone created tether, he just created OP_RETURN on Bitcoin blockchain. He said "With this prefix OMNI, I'm issuing assets with an ID tether-USDT and I'm issuing myself a lot of tethers". This is how tether was created. On Bitcoin blockchain is not backed, so you cannot redeem your USDT on Bitcoin. Well, technically you can because inside of this OMNI specification, there are opcodes for doing trades for DEX. Omni layer actually was a motherland of original DEX, so you could put up offers to sell some of your OMNI tokens through Bitcoin. And other people would pick them up from Bitcoin blockchain and do some trades. I don't think people use it much these days. I don't know, I haven't checked it out.

Audience
Does that mean that anyone who wants to use the Omni Layer, each have to have not LND, but another implementation?

Igor
Yes. They created [OmniBOLT daemon](https://github.com/omnilaboratory/obd). So you have to run OmniBOLT daemon to fund your transactions with tether and after that, it acts pretty much as regular lightning channels. Another cool thing is that they specifically designed the OmniBOLT daemon with the fact that signing keys are not gonna be residing on this daemon. So actually light clients can connect to one OmniBOLT daemon, each keeps his own seed and signing happens on the client only and this (the daemon) acts like some kind of relay, or something like that. I don't know how it works, but they claim they did it. Unlike LND, because in LND it's very hard to extract signing part from the rest of the daemon. That's why people have to carry with them their whole LND when they want to do lightning stuff. So even mobile clients, like Breez wallet, it's essentially whole LND packaged as a mobile app.

Audience
Can [macaroons](https://github.com/lightningnetwork/lnd/blob/master/docs/macaroons.md) help with that? Because you can delegate specific capabilities.

Igor
Yeah, technically you can, but I don't think they finished the support for this in LND. It was an idea years back, but still no one uses it. The idea was that you can issue macaroons like authenticate someone. There are macaroons to create invoice, there are services where you can issue read only macaroons so someone can issue invoice but you cannot lose money in this way. You can only authenticate someone to create invoices on your behalf and you will receive money issuing macaroons like "I want this guy to withdraw 10000 sats", maybe it's supported technically but no one uses it.

So now we have USDT on lightning, this is the plan for Synonym. Any questions? May someone can add something, maybe I missed something.

Audience
What's Synonym exactly?

Igor
Synonym is everything, all of that, having your identity, having your data and having your tokens on Lightning as a single package. John wants to take Web3 and make it Bitcoin friendly. Because you know, Web3 is a term for shitcoiners. They're always Web3, Web3, what's Web3? This is Web3 but now we're trying to put it inside the Bitcoin ecosystem.

Audience
I guess the question is what is Web2 actually?

Igor
I was going to say that. That's my finishing remark. I'm not a big fan of Web3, because I'm not a big fan of Web2. We were supposed to have flying cars and colonies on Mars and instead we have ...inaudible... like Twitter, or TikTok. Yes, I'm not a big fan of Web3 but it's interesting how it unravels, how it unfolds, we'll see what this will lead us to.

Part of Synonym is Slash Tag. Slash Tag is basically a bit more formal definition of the protocol, of how I want to show my identities, my accounts and my data to other people. Last time I checked, it had only contacts and kind of like accounts.

### Synonym compared to Strike

Audience
How is the protocol different from what Strike is doing?

Igor
They do absolutely different stuff. If I got it correct, the way Stripe works is--there's USA, there is Salvador (draws border on whiteboard). USA people, if they move from BTC to USD, it doesn't leave the country. Instead, on this side of the border (Salvador), someone pays with USD the receiver and BTC is used as the transport layer (USA -> Salvador). So there is no lightning, there is no tokens involved in Strike. So if I got it correct, this is how Strike works.

Audience
...Inaudible...

Audience
That central point where is moving from USA to El Salvador, isn't that over lightning?

Igor
It can be lighting, it can be BTC, it can be pigeons with golden coins, it doesn't matter because the real USD doesn't leave USA. Instead, people inside of El Salvador are paid with USD by someone from inside El Salvador. So this is how money-moving services work these days.

Audience
Do you know [Abra](https://www.abra.com/)? They we're going to use Bitcoin basically for remittances. The idea was basically someone would send funds and then they meet someone.

Igor
This is actually quite old idea. Have you ever heard of TransferWise? They rebranded to Wise. They do the same thing. The way they keep the costs low is that if you're sending pounds over the border, no real pounds leave the country, because they pay someone from inside the country and at the destination country someone pays the destination. So no real funds movement across the border happens. This is how Wise works, this is how they keep their fees really low.

Audience
The idea is even older than that, it was called [Hawala](https://en.wikipedia.org/wiki/Hawala), same concept.

Igor
Yeah, same concept. And I think Western Union did the same like 200 years ago. I think there were the same, so someone calls someone far away and says "Look, you have to pay this guy this much".

Audience
I've heard Jack (Mallers) say that somewhere in the protocol there is tethers.

Igor
Well, maybe instead of BTC you can move tether, but it doesn't matter. Still USD doesn't leave USA and USD is paid in El Salvador.

Audience
Maybe it's just that instead of holding USD in their app, they are holding USDT and only when you want to move it in your bank account they convert USDT to USD.

Igor
Well, I'm not a fan of Strike because Strike is kind of a really centralized entity.

Audience
...Inaudible...

Igor
Well anyway, there's no token involved, lightning tokens in Strike. Anyone wants to add something? Maybe someonehere knows more about Synonym than I do, please share.

## RGB

Igor
Next thing on my list is [RGB](https://github.com/LNP-BP/LNPBPs/blob/master/lnpbp-0011.md). RGB is a really interesting concept. Originally Synonym was supposed to run on RGB, but there were problems with RGB so John decided to move from RGB and do this thing with tether and tokens on tether. RGB is kind of like architecture to run smart contracts on BTC completely off chain and reimagine smart contracts.

### Smart contracts on Ethereum

The way smart contracts work on Ethereum is that, Buterin said that we're going to host all the source code on the blockchain. Actually, I was reading Buterin's blog posts from back in the day, I don't know 2014 maybe. At the time he hasn't invented Ethereum yet, but he was writing blog posts about how Bitcoin works. And this is how I learned how Bitcoin works, from his blog post actually, in Python. This idea sparkles in his mind that what if we'll put a whole Turing-complete program inside of this Bitcoin script.

Imagine this is Bitcoin transaction. So there are outputs. And there is a Bitcoin script which is not Turing-complete. And this is where this guy thought maybe we can put the whole program, the really working program in this output. He came up with this idea to Bitcoin Core guys and they turned him down, because this not even doesn't scale, it doesn't scale squared. Because eventually, a shitload of programmers will migrate to this--if it's successful, will migrate--and will host their source code on the blockchain on top of elliptic curve compute verification that will add execution of the scripts on each block, well, this won't fly. And this is what we're seeing with Ethereum, when it's so big and it's so hard to run the node. I think the block time for Ethereum is like 17 seconds. There are blocks that takes like minutes to process all scripts inside of block--like longer than a block time. This is ridiculous.

Audience
Is that happening today? Like minutes for verification?

Igor
Maybe, not with the lightest blocks, but still you can install the Ethereum client and it will choke on some couple of years back data. You'll see like one block gets processed for minutes.

Audience
...Inaudible...

Igor
Well, imagine you're writing shit code in your life and you put on this shit code forever and ever in some block. This is ridiculous, right? Satoshi didn't Turing-complete language inside Bitcoin script, not because he was dump. It was because he anticipated that people will be smart-asses and will try to take advantage of Turing-complete stuff in the blockchain. That's why he didn't do it and that's why Bitcoin Core guys turned down Vitalik when he came to them with this idea, they said it wont scale. But he went ahead anyway and created Ethereum and now we have a smart contract, you create the bytecode of the smart contract, you mine it in a transaction--so you have a transaction with this bytecode. Once it's mined, it gets an address. Now anyone can reference to this smart contract and provide some data and do some computations and alter the state on the Ethereum blockchain.

This is how it works, you keep a lot of code on the blockchain. Each call of this code is another transaction that gets mined and it mutate this global state and the global state is visible to everyone. And a smart contract is visible to everyone. Everyone can see everything.

Audience
I just really want to correct what said earlier, the problem with having a script which is--in quotes--"Turing-complete" is not that you can have a long series of computations because you could impose a cost per step and that's what they are doing in Ethereum. Let it be a long program, let's say it does take quite a while. The problem is that I can pre-compute the block before everyone else knows about it and then publish it to the network and then everyone else has got this massive disadvantage because I'm 2-3-4 minutes ahead of everyone in the block and that's what leads to that centralization.

### Rollups on Ethereum

Igor
So this concept scales very bad. The current consensus on Ethereum world is that "let's create a side-chain"--actually they have several side-chains and those side-chains act as batching for transactions, which is basically rollups. A rollup is a side-chain where you batch several transactions into one transaction. The way they do it now is that they have zero-knowledge rollups and optimistic rollups. Zero-knowledge rollups still publish cryptographic proof that the computation happened. Optimistic rollups, they don't publish anything, they just hope that everything is correct. And some kind of validator, later, will catch the cheater and we'll punish the cheater. That's how it works. That's why optimistic roll ups are more favorable in the Ethereum community because they can process even more, because they don't do shit. They do something in zero-knowledge rollups but not in optimistic rollups.

Audience
THe solely advantage with the optimistic one is that if there is a dispute and somebody says, "Oh, there was a fraud" like one of those 1000 transactions that was actually fraudulent. It means that you have to wait some time, you have to wait for proof to get published. So that means that if you want to take your money off this optimistic, it takes ages, it takes a week.

Igor
Yeah, last time I read it was about one week. So if you have a dispute on optimistic rollups, there is a one week dispute. You don't have a finality of a transaction for a week, right? In Bitcoin you have it in six blocks, in one hour.

Audience
Did [plasma](https://ethereum.org/en/developers/docs/scaling/plasma/) originally was going to be the same?

Igor
I think plasma was not a rollup, I though plasma was a side-chain technology, no?

Audience
...Inaudible..

Igor
Last time I read on plasma, was the fact that it died.

### How RGB runs smart contracts completely off-chain

Igor
Okay, so RGB is totally a different concept from this. RGB says "Okay, guys, look, we have a contract. We don't have to keep this contract public". So if I'm buying a car, it's a contract between me and the seller of the car. We don't have to make it worldwide available. The contract is between me and the seller of the car. So we utilize this concepts of client side validation. It utilizes this concept of single-use-seals, which is a totally new concept in cryptographic world, and Directed Acyclic Graphs (DAGs). Now, let's imagine I'm creating a contract to issue tokens, and I want to _ some tokens to someone. I create a definition of the token, which is called schema in the world of RGB. I shared the schema on client side, I don't commit the schema anywhere. I shared the schema with my peer who I send some tokens, and this is going to be a mutation of a state. I am sharing all that state with my peer. And this peer has it only on client side, he sees that this is a mutation of a state, this is the source of the state, there are cryptographic proofs that this has happened, this was signed by my friend's public key. It happened, and we don't have to commit it to the blockchain. I can send some tokens again, I mutate the state, and this guy can send it somewhere else. So we end up with a graph, we end up with a directed acyclic graph. It's directed because it flows in one direction, so I can send tokens only in this direction. It's acyclic because you cannot make some crazy loop and go back. And it's a graph, so it's a DAG.

It employs client side validation, so every time I mutate the state, I share the new state with my peer who I'm sending tokens to. So this is schema and this is how we keep it off chain. We don't commit anything to blockchain. Well, there is a problem here with double spends. How they prove that there is no double spend here. This is where we employ single-use-seals and some other cryptographic magic, which is newly invented for RGB. Single-use-seals is the new concept in cryptography, it was invented by Peter Todd, I think. If you boil down single-use-seals, it will be, "take a private key sign something and prove to someone that you signed with this private key only once". If I'm taking a message and I am signing it with my private key and I give you this message, and then I signed something with the same private key and give it to you, can I prove that I didn't do this?. In purely cryptographic terms, it's impossible because I can take my private key and sign as many messages as I want. So single-use-seals relies on something else to publish cryptography stuffs so other people can verify. And this is I think the weak spot in this concept because you have to have a storage to publish single-use-seals and have no double spends. We have a whole proof of work, huge machine to prevent double spends on Bitcoin. And he will say, "oh, we'll just use single use seals and assorted" and we're done, we're cool. So this is a weak spot. I think in the early concepts they were supposed to use some IPFS or some distributed file storage for single-use-seals, but now, I don't know what they're doing. They don't use Hypercore, last time I checked, there's no mention of Hypercore in RGB.

Audience
What were you saying earlier? It's like it's possible mathematically. It's kind of true. But there's an exception to that rule because if you have a signature scheme, like a single use signature scheme by which if you publish a second signature on the same key, you reveal your private key. Such signature schemes exists and that could conceivable, in a half kind of way, solve that problem.

Igor
Yeah, but since we use client side validation, we're not sharing it to anyone. You receive tokens, this is a transaction for your eyes only. You have to have some kind of storage for everyone. So everyone could see.

Audience
This is happening off-chain, right? But at some point, you want to sum up everything and publicly broadcast everything that happened.

Igor
They don't need it. Imagine you have a schema for token and this is just a shit token, it's not related to Bitcoin in any way so you don't need to publish it to blockchain. Well, they still use, I think currently RGB is at the stage where you need to publish your single-use-seals or whatever to blockchain. You're not publishing the whole transaction, you're only publishing some cryptographic byproducts of the transaction happened here and here and here. Alone this data is not enough for anything. Just data, but in a combination of client side validation and this data like "I issued some token schema", "I mutated the state to move tokens to my friends here" and "he moved here and here", in combination it works.

Audience
When you say schema, what is that exactly? Because it's not clear to me.

Igor
The schema is whatever you want it to be.

Audience
This is the restrictions you want to put there pretty much.

Igor
Yeah. It can be a token, it can be NFT or something else. The RGB guys are working on different schemas. In fact, they created [RGB-20](https://github.com/LNP-BP/LNPBPs/blob/master/lnpbp-0020.md) as a relation to ERC-20 tokens on Ethereum. And of course, we have Bulletproofs and Pedersen commitments here. So at the point of moving tokens, we don't see amounts, so it's more private than regular tokens. So if I'm this guy (shows a node on the drawn DAG graph), what I need to get is only client data from here, partially from here and this schema, and I can validate that this happened and I indeed receive those tokens. And if I look into Bitcoin blockchain, I can also make sure that no double spends happened and boom, you have smart contracts on Bitcoin. But without this massive computation on Ethereum. Well, it's a bit more complex here than what I just said. Because it might not be very simple transfer, it might be very complex state mutation.

Audience
About the mutation, can you just walk through with some dump example like what a mutation would be? For me is not really clear.

Igor
Basic mutation is that I had 10 tokens and now we changed it and now I have 8 and this guy has 2.

Audience
So every time you update what is between you and me, that's a different mutation.

Igor
Yeah. So different state and this is the graph of states. But because they want something more complex, they created a virtual machine, kind of like Ethereum Virtual Machine, but not the same. They call it [AluVM](https://www.rgbfaq.com/glossary/aluvm) and this virtual machine is going to process the state mutations.

### When RGB

The problem with RGB is that it became a very big, very complex concept. It's in development for several years and we don't see getting into production very soon. People just work on it and work on it. I don't think that they have enough manpower, I think it's [Max Orlovsky](https://github.com/dr-orlovsky) and a couple of other guys that work on it. Right now they have AluVM, which is on its infancy. They want to put this on lightning as well, so they created a brand new Lightning node. They are creating a wallet that can handle all of this, which is called [My citadel](https://github.com/mycitadel). The scope of work is really big, like a lot of stuff to do to make it fly. That's why John from Synonym, he was relying on this initially, but in the end, he decided that this is not getting into production anytime soon so we need to switch to something more realistic something we can deliver. That's why he switched to tokens on Omni Layer. Apparently it's easier to put OMNI tokens inside of lightning than make this flight. And that's RGB.

Audience
What did you specifically like about this? What made you present this one?

Igor
Well, the whole concept is very cool. You have smart contracts that don't have to touch blockchain. They don't have a massive footprint. This schema is not committed to blockchain in Ethereum you would take your big smart contract, compiled into byte code, put it inside a transaction and mine it and it's in a block in the blockchain forever and ever. In Ethereum, everyone can see this smart contract. Everyone can interact with it. Everyone can read it and know what was it about. But in reality, if I want a smart contract, I want it between me and you. No one else should be involved, right? Because it's between me and you,

Audience
And the people involved could see their chain of relevance?

Igor
Yeah, only people involved and every state mutation is not a huge transaction. Because in Ethereum you take arguments for a method that was mined in blockchain, you put it again in a transaction, you mine it, and then the global state mutates in Ethereum. So it takes a lot of data, a lot of computations and in RGB you take it completely off blockchain, you don't use blockchain, only for some validations that no double spends happened, which is quite tiny, like you can use OP_RETURNs for that, which is like 40 bytes per transaction. When in Ethereum like I don't know, each transaction, just mutates token state. I don't know how much is that. It's a lot.

Audience
They are moving to proof of stake so they won't have the...

Igor
I think they're moving to proof of stake but it's unrelated, they still gonna have contracts compiled to bytecode committed to somewhere and each node will have to recomputed each state's mutation in Ethereum. So proof of stake is not even a solution here.

Audience
Is the idea with RGB that any one person can eventually like cash out without affecting everyone else's state in this tree.

Igor
I don't get it.

Audience
...Inaudible...

Igor
There's no collateral involved, there is no collateral. I create a schema, there is no collateral involved. There's no Bitcoin involved.

Audience
...Inaudible...

Igor
The token never leaves the RGB.

Audience
It's only using Bitcoin as a kind of anchor of the cryptographic proof. Ultimately they're trying to achieve cryptographically provable token, not a derivative of Bitcoin.

Igor
Yeah, and I forgot about about that. On top of that, they're working on [Bifrost](https://www.rgbfaq.com/glossary/bifrost), which is going to be a protocol for DEXs on top of RGB. This is where you'll be able to swap your RGB tokens to other RGB tokens or Bitcoin, or use atomic swaps to some other coins in other blockchains. The point is that the whole scope of the project is huge, so we don't see when it will be in production.

Audience
On the tricky point, the single-use-seals point, I just refresed my memory looking at Peter Todd's old blog posts and he was saying that, how you gonna know this seal hasn't been used somewhere else? That's the fundamental problem. You've got a seal, you can show a signature and move it to a new thing but you need to know that hasn't been another signature. And he was saying, he has this thing called Proof-of-Publication Ledger.

Igor
I think the Proof-of-Publication layer is just a general concept, which could be IPFS or in this case, blockchain, the Bitcoin blockchain. I think it was early on, I think you can find it still in the documentation because it wasn't updated. But I think they decided not to do it and just use regular Bitcoin transactions using OP_RETURN as as a proof of publication.

Audience
You have to kind of batch them, right? Each individual seal, that might be millions of them and you can't OP_RETURN all of them.

Unknown
I think that's work in progress. That's why it's still not in production. Single-use-seals is kind of complex concept, I don't completely understand it. I'm not even sure that each state mutation has single-use-seals, I think it's some different cryptography. Single-use-seals definitely used at the schema issuing. You issue a schema, you put a cryptographic proof on the blockchain in the form of single-use-seal. I don't know why. And here is some different magic, some different cryptographic magic, I don't really understand.

Audience
So you can't peg-out into the Bitcoin blockchain. Once you are in this network, there is no pegging-out.

Igor
No pegging-out.

Audience
You start on that network as well. The token is created in that.

Audience
I suppose you can always convert outside of the blockchain and trust in a way.

Igor
Yeah, use atomic swaps maybe or DEX. DAG I think it's another concept which is currently explored by other blockchains, by altcoins. It's a concept that you don't have a block of transactions, the concept of state mutations and creating a graph of everything. I don't know how successful it is in altcoin world, I have to research.

Audience
On this, do you have a level of confidence, do you see it as being feasible?

Igor
Well, it's very interesting concept, but I don't see it flying in this year, to be honest. They're released some stuff. They released a bit of My Citadel, the releasde a bit of lightning implementation, brand new lighting implementation based on rust. So they're releasing something, they're working, but will this whole concept be viable this year? by the end of this year? I don't know. If I'd had to bet, I would bet on Synonym.

I think that's all I wanted to tell you guys.

## LSPs

Audience
What you gonna tell us about LSPs? I wanted to hear about LSPs, or is that another thing?

Igor
Actually LSP is one of the concepts of Synonym, it's a blocktank. The idea is that once the created tokens on OmniBolt it takes a lot of friction to make those tokens fly. It's not like in Ethereum, where you create a smart contract and everyone can use those tokens. In lightning you have to supply liquidity for your own tokens. Iif you trade a token on Omni Layer, you have to supply liquidity and blocktank is their own LSP which is going to supply liquidity for USDT. Say you want to participate in USDT tokens on Lightning Network. What you do is, you announced it and blocktank will create a channel to you so you will get incoming liquidity in USDT on OmniBolt protocol on lightning. Does this makes sense?.

So blocktank. Other people that will want to issue tokens on OmniBolt, they will have to do the same. If I want to create my DOGE token on OmniBolt I will have to maintain my own LSP which is supposedly going to be an open source blocktank. And I'm going to open channels to other people who want to receive DOGE token on OmniBolt Layer 2. What else about LSP? I haven't thought about it much, I am not a fan of LSP concept. Because like Lightning Service Provider, if you're supposed to open channels to everyone and you're aiming to make fees routing to everyone, this leads to centralization. You have to commit a lot of funds to those channels and you are spending funds to open the channel so this could be a lot of money. I don't think it's worth it.

You're opening a channel, you spend fees on opening channel, you're committing capital to a channel, which is dead weight now, and you hope to earn routing fees. How much could it be? I remember channel opening fees for like $15 when the blockchain was clogged. Can I make my $15 back by routing fees in several years? I'm not sure. And I committed capital, if I locked 1 Bitcoin to a customer, if I get 1000 customers per day, do I commit 1000 Bitcoin per day? This is a shitload of money. So I'm not a fan of LSP concept but I don't know a solution around it at the moment.

Audience
A comparison to made is with a custodial service, right? LSP is at least better than custodial service because at least there's a channel being allocated to a specific user. With a custodial service the user never has a channel. Obviously, I agree with you. It's gonna lead to centralization, but perhaps it's better than custodial.

Igor
I don't know, if BlueWallet would have to act as LSP, we onboard 1000 people per day, we would have to commit a lot of capital to channels and I don't think we would ever make it back.

Audience
Maybe once someone has got a channel with a LSP, perhaps acts like a stepping stone to operate the channel themselves? Maybe the channel with the LSP is operated for that customer such user can be transitioned to a channel that the user then operates.

Audience
You can charge the user to put together the fees.

Igor
But that starts sounding like an economy, you have acquisition costs, you have running costs. If you're running open-source, fuck the cost but if you are running as a business you have acquisition costs, running costs, marketing costs, and will the economy converge to a point of being profitable. I don't see it converge to a point of being profitable. As I said openning fees could be $15 per channel per user, and this is a lot money to pay to onboard a user who you don't even know if he is going to use the app. Maybe he just open the app and close and delete it.

Audience
...Inaudible...

Igor
My production LND has problems maintaining 100 channels on 4 cores. How I'm gonna add 1000 more channels per day? Do I need to run a DevOps team?