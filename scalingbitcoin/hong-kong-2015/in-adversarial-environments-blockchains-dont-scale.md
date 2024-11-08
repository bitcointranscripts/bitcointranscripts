---
title: In Adversarial Environments Blockchains Dont Scale
transcript_by: Bryan Bishop
tags:
  - security
  - incentives
speakers:
  - Peter Todd
media: https://www.youtube.com/watch?v=ivgxcEOyWNs&t=30m35s
---
slides: <https://scalingbitcoin.org/hongkong2015/presentations/DAY1/2_security_and_incentives_2_todd.pdf>

That was a very useful talk (on [security assumptions](http://diyhpl.us/wiki/transcripts/scalingbitcoin/hong-kong/security-assumptions/)), thank you Andrew.

I am going to start by talking about nitty-gritty applications where adversarial thinking is useful for incentives for decentralization. In an environment where everyone has the data, we are kind of limited as to what we can do. When we talk about scale, I am talking about 5 or 10 orders of magnitude. Do we have a system that has fundamentally different scaling characteristics?

Before the United States learns about China's new block, they are going to find another block. Who is going to win the tie? Depending on how the hashrate is distributed, it will be China and then eventually both sides will come to consensus. This is pretty well known feature of Bitcoin. This is how the system works. There's a big catch though. When you talk about failure modes and incentives, you might ask well, what percentage of hashing power does the Chinese side need for them to come out ahead? For them to earn more money than the other side? You can do the math on this.

It turns out to be about 30% which is really interesting, because then you could ask if you are behind the Great Firewall, and I don't have a better internet connection to the rest of the world, do I have an incentive to improve the situation? It's not clear that you do in many scenarios, which means that if I am not in China, then how do I add to the decentralization of bitcoin? What's the long-term progression of this?

It could be a scenario such that when you bump up to these limits, hashing power is going to be in one place because that's what's most profitable. Matt Corallo's relay network is a good example of using compression techniques to compress blocks, pre-replicate blocks and transaction data, rather than sending the whole new block, then you send just a few bytes. In Bitcoin, you have to think adversarially. If I am the miner in China, then perhaps it is to my advantage that the relay network doesn't work. If I am not thinking about the harm to the bitcoin price, but rather just how much money I am going to make this month or next week, I don't necessarily want the relay network to work because that helps my competitors.

In other environments, this would work really well. But in adversarial environments, this might fail. The distribution of hashpower is currently fairly lopsided. We are in a situation where it is really easy to get miner consolidation. I am not too worried about the mining pool graph, and I would be more concerned if it didn't change too often. I think this one in my slide is from September.

Well how are we going to scale this? Bitcoin is just a big unspent coin database. As with most computer science, I can put a tree on it. I can find every coin by its unique identifier. When I go spend a coin, I'm updating an entry in the database. This looks like most database applications, like customer databases or personal databases. This all works very well, if the items in my database gets too big, I can start sharding it, I can split up the key space in this case, if there are other servers running it, I just go to the server responsible for that keyspace and I do whatever I need and so on. This is a really valid scenario. But what's interesting is asking, why is this hard in Bitcoin?

This comes down to what are we using Bitcoin for? Well, transactions. You can get consistency and rollback in databases. In bitcoin, the transaction graph is the most important thing. As we build blocks, we create coins, spend them, and create new coins. Sometimes coins are merged together, sometimes they are split apart. And the system progress. Now if you want to shard that database and split it across that key space, then obviously this could work. When I go to make a transaction, I would go to the part of the bitcoin ecosystem that holds my coin, I would say please spend it, here's my authorization, in a standard system this would work really well.

The problem is that Bitcoin has tihs issue where the data in the database depends on (inaudible). If I have a single invalid transaction, that very first red bitcoin, its act on the rest of the bitcoin is invalid. My definition of a blockchain is everything in it is valid, so if that one is invalid, then if I try to split up that database, then I'm trusting other people to do the right thing. I am trusting, in an adversarial environment, other miners to not create fake money.

I have done some work for banks and fintech and advising them about their architecture. When they go look at blockchains, even though they are in an environment where they have law on their side, everyone knows each other, when something goes wrong they can call each other up, the smarter clients are actually pretty terrified of blockchains. Even in this benign environment, when something goes wrong, it's not clear how to rollback. When a counterparty at another bank screwed up and now there's a million dollars of fake money, it's not easy to fix. If you look at how banking works now, even though they could have technologically done blockchains for a long time, they don't. They use systems where they have bank accounts where they transact with each other. All of it is localized, if something goes wrong, it's localized. Bitcoin doesn't have htis property, because we have transactions. This makes traditional thinking very difficult.

In adversarial environments, I can't scale this by splitting this up. We need better technology. What solutions do we have?

Lightning is a great example of a system that helps scalability by limiting the trust you are involved with. The lightning system, if I am going to send money through another node, yes there's trust involved, but it's piece-wise trust, if it's broken then I wait for timeouts to trigger and get my money back. The whole system isn't "infected" by these mistakes. Mistakes don't build on each other. You can always verify the consensus blockchain.

Longer-term, it would be nice if we could find ways to scale blockchains. I am not going to present this as a fully solved problem, but one of the ideas that has been out in this space is well maybe miners shouldn't validate. But then you would allow invalid transactions.. So then I am building on a part of the blockchain, and then I am harmed or something. Well, if I am going to give you money, why not give you a proof that all of the transactions and all of the data in that transaction can be split up, and corresponds to real money? In this kind of system, it's certainly inconvenient to trust miners to ensure you have money, but if I have the correct data then I could convince you that the money is real.

The most naive way to do this requires quasi-exponential scaling, and then you would have high-rates of mixing. Once, gmaxwell did some work on this and looked at how much coins are mixed. Going back six months, every coin is mixed with every other coin. We have a trick up our sleeve. We can linearize this history. I am sure the snarks guy are going to laugh at me about this, but that's okay. This is simple in comparison.

If I have a yellow coin in the transaction graph history, if I ensure all the inputs to that coin have actually been spent and recorded irrevocably, and pick one of those inputs at random, I can put myself in a position where probabilistically I can get away with creating fake coins, where one input goes in and the other input doesn't exist, and half the time I would create money out of thin air, and the other half of the time I have destroyed my money. It would be possible to go from crazy O exponential blow-up, to linear type of proof, where the amount of data I have to give you is linear in the amount of history. If coins are getting created on occassion, then newly created coins have no history. If the proof crunches through, the proof gets shorteend when there's new coins. This gets close to O(1) scaling.

When you go to clever math with snarks, this becomes very easy, and potentially in the future we can go scale this way. Given how hard validation is in an adversarial environment, why don't we let someone else do that validation? The person who cares about this should do their own validation. This is maybe 5 years out. We do have some hope here.

My proposal is simple. We should wait and see. We should not make hastey steps to go and push bitcoin down into a new trust model. If we do a block size increase, we should do something small, something within the same region that bitcoin operates in right now, and then see what happens in a few years.

Q: What if instead of history of transactions, you had checkpoints on balances, then you could shard more or less...

A: That's a great idea, I proposed it to fintech clients. This was my work called proofchains. Those checkpoints, if some trusted entity were doing those, in a banking environment it's certainly easy to setup checkpoints, but in a decentralized environment it's not clear how to do this. If we went down this path, for a while it would certainly work, but this becomes a target for censorship and seizure. Whoever has the authority, whoever wants to go after them and shut them down, maybe go on Reddit and elect a new leader.. that's probably enough to de-stabilize the system if done consistently. SNARKs and recursive SNARKs could compute the checkpoints for you, but I wouldn't want to just sign-off and say yeah sure on that.

Q: You were talking about relay network, and one question is, wouldn't China be fighting the rest of the world, not just the United States?

A: In my diagram, I am pretending geopolitics are much simpler. China currently has enough hashrate majority to pull this off. They have at least 60% of the hashrate I think. The attack I mentioned needs only 30%. That attack happens naturally in environments without a block size limit. It's to my incentive to let people go through and get transactions through. Without that block size limit, there's no clear definition of what spam is. If I am the guy with the most hashing power, then .... try to even it out to the greatest degree possible. ((stream problems))

Q: If I prove all the inputs are valid, but how do you prove inputs have not been spent? Proving the non-existence of a spending input.

A: One way to think about these systems is to think in terms of proof-of-publication. I prove to you, as part of spending money, that I have published that spend so that everyone who wants to get that information can get it. Simultaneously, I have proved that nobody else including myself has publshed a spend of that transaction. And you limit where that transaction could have been published. A simplistic model in my treechains concept, I could just give you a part of the blockchain. I could give you a compact proof that no transaction exists that would have validly spent that coin, from the time it was created to the time it was spent. I think there are ptoential solutions there.

Q: When are you going to write the treechains bip?

A: Does anyone want to hire me? This is all very far out. This is not going to happen overnight. I think we will see lightning deployed before treechains.

Q: Client-only validation, and miners would have to care about fees right?

A: That's one of the hard things to solve. Recursive SNARKs makes this easy so that when you go pay a miner to mine your transaction, you could have a compact proof that the money is real. If you don't use SNARKs, and instead use simpler math, you would have to give someone like 10 megabytes of data to prove that the transaction is real. I am interested to see what people come up with there.

Q: I want to understand the linear coin history proposal. It sounds like colored coin validation where you tracing specific coins. For that to work, is it the case that a transaction could be valid if it has invalid inputs?

A: Yes, that's exactly it. What's interesting about a system like this is that you could use this for privacy, where you deliberately create an invalid transaction knowing that you will get away with it sometime. One good thing about encouraging this is institutionalizing the "fraud", to create a system more robust, we exercise the code that handles that case. If I am not giving you that data, then I have very good privacy. If I have two coins, and I go and ignore simply one of them, and do some magic to create a fake proof, when I do get away with that fake proof, now I don't have to go prove to you where that other money comes from. This is where privacy and scalability meet each other. You can't have scaling where everyone has all the data.

Q: What do you think about using miners not to verify each other? I think bitcoin-ng uses something where you put anything into the blockchain, then produce proofs of invalid transactions, then you resolve disputes or something.

A: That's been brought up in bitcoin for a while now. Satoshi talked about this in SPV clients, where they would receive alerts from their peers about invalid blocks. It's not a bad idea. It's a different security model from current Bitcoin, where you are relying on the existence of a flood-fill network where you are expecting to have a good chance of receiving a notification of invalidity. That assumption of a flood network is often not true. If you come over to my apartment, and I was feeling mean, I might setup a wifi access point to limit your ability to hear the bitcoin network, maybe I will filter out the fraud proofs. If I am large miner, maybe I will run enough nodes on the network such that if you connect randomly, you are less likely to connect to an honest node. I think the big worry is what socially happens if you don't detect fraud immediately? Given the rate of mixing in the Bitcoin economy, if you find out a few days later that a block was invalid, do you rollback? Do you invalidate millions of dollars of bitcoin? The reality would have to be that we accept it and people would sometimes get away with fraud? That could potentially destabilize an economy if fraud gets in like that, we don't have a good idea of what that would lead to.

Q: There are two ways to do mining. You can build mining equipment. China way is like BTCC, raising money from each other, then using bitcoin to make .. then mining. There are two different ways. The Chinese way is more friendly to Bitcoin community, not like our people wanting to make a lot of hashrate and destroy the system. Everyone wants to protect the system. Every Chinese mining pool wants to protect the system. We want to come here to know, do you have a suggestion or a solution? Your suggestion is to wait for a few years, then we do something? But we want more better way, we want more communication, what better idea do you have? Don't wait ? Are there better ideas tha tdon't involve waiting?

A: I was in China last week. An interesting story I heard about is that there were multiple occasisons when China hashing operations had loaned their hashrate to each other, as good neighbors. Not getting any money in return. Loaning lots of equipment. As a United States developer, that lets me sleep well in night that we have a big community that behave a lot more altruistically than our assumptions. We cannot rely on these assumptions. We need to design a system that still works in the face of an adversary. That very friendly, very helpful, very good mining community might not exist in the future. Who knows why. Maybe some Western company makes chips 10x faster. Maybe the government of China now restricts the internet in a way that we can't usefully use? I still want a system that is resiliant. To the best of my knowledge, I cannot get the scale we want at the scale we want, without taking risks that are unacceptable. My caution is predicated on how I think we can very rapidly deploy systems, such as lightning and payment channels, and even changetip, and situations where they work in a way that is less risky to the whole ecosystem. I think we're better off if we take that cautious approach, given how many billions of dollars.






