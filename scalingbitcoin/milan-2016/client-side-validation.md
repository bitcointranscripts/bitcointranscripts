---
title: Progress on Scaling via Client-Side Validation
transcript_by: Bryan Bishop
tags:
  - client-side-validation
speakers:
  - Peter Todd
date: 2016-10-09
media: https://www.youtube.com/watch?v=uO-1rQbdZuk&t=6198s
---
<https://twitter.com/kanzure/status/785121442602029056>

<http://diyhpl.us/wiki/transcripts/scalingbitcoin/milan/breaking-the-chain/>

Let's start with what isn't client-side validation. I am going to call this the miner-side approach. Here's some smart contract code. In this example, it's Chronos which is a timestamping contract. What you have here is a contract that stores in ethereum state consensus some hashes as they are received, they are timestamped. And ultimately at some point in the future you could go and ask the ethereum state machine, you know, did you go and get this hash? And you know, this is typical of a lot of these applications. It raises a lot of questions about who has the data. Do we need everyone to have the data?

In comparison, client-side validation of data is actually the mainstream thing that happens. This example is my bank. When you ask what's going on under the hood, well my web browser starts off with a root-of-trust and it receives signatures from a server that I don't trust originally. I check the signatures of course. Then I download the rest of the website. This is pretty typical. There's no shared consensus, it's all done client-side. This is pretty much how most crypto is implemented. Ethereum's "let's put it all into the consensus state approach" is something I think we have done a little bit too much of in the blockchain world.

If we're going to talk about what do we have in our toolbox to do these kinds of client-side protocols, it's actually fairly simple. Your basic primitives are signatures. This is pretty much everything that crytpo relies on anyway. We have proof-of-existence where we use a series of hash operations. Yesterday we heard about timestamping in general. I wont cover that in too much detail. And then there's proof-of-publication, which is a bit of an odd term. Whereas timestamp is proving that a particular message existed for a certain time, in proof-of-publication I am proving that some message was added to some set of messages. Proving that if someone else wanted to, they could find that the message existed (or didn't) or was available, rather.

In opentimestamps, which is my timestamping solution, the key takeaway is if you ask yourself how much data do you need for the whole world to have consensus? Well it's basically just the blockheaders from bitcoin. This is a solved problem. There is probably going to be a lot of bikeshedding about the structure of the proofs, but it's clear to me how this will look. Another case study is blockstack using a proof-of-publication. I know the blockstack engineers will yell at me for oversimplifying, but basically it takes the blockchain starting at some point in the past, and reads through it, and because everything is in consensus about what data you are applying to, being the blockstack consensus algorithm, we can guarantee we can get the same results. If I register domain names or something, what we're doing is publishing part of the data relevant to that operation to the chain. This guarantees that everyone else receives that data. The proof-of-publication guarantees that they can read it. Their consensus algorithm will run through it and hopefully get the same results. There are some caveats, which will be mentioned in a moment. Counterparty and mastercoin are other applications of this doing it in slightly different ways. It's a valid approach and it does work.

Could we do this in bitcoin? We actually hear people say that miners are validating blocks. Well, if miners are validating blocks, then what is your full node doing? It's also validating blocks. If miners didn't violate blocks, then what would your full node do? Well, it would validate blocks. What if we changed the bitcoin protocol rules and say well you have this proof-of-work thing, and you have this consensus about most-work chain, we'll keep that part. But we'll say that what's in that chain can be anything. Your full node will not reject a block under any circumstance regardless of what's in it. We'll say, well, maybe ... ultimately the content of the block we will not reject under any basis. However, if I want to send you money, the full node will go through the blockchain and reject stuff that doesn't follow the protocol. If we're running the same software on both sides and there hasn't been a bit flip or something like that, you and I will come to consensus. When I send money, you will receive it, and vice versa. I mean, that works.

So really you can say that miners validate and it's an optimization. It has some interesting social effects about what is the valid definition of bitcoin. If we had this rule, then I could also create litecoin and coexist on the same system. It raises social questions, but not technical questions. This can pretty clearly work--- except for paying miners, that's a more complex question.

Well what's so hard about the double spend problem? I like to use the analogy of where's waldos. You have this big pile of block space, and you want to go find waldo. And it's easy to find him, but it does take work to go find another waldo. It's easy to point out waldos. It's consensus over what's in this space; you can imagine a hash tree or a merkle tree being made up of this. But ultimately our ability to be in consensus is limited by our ability to scan through and deal with this space, which doesn't scale too well. We run into problems when we try to apply standard database techniques. Any standard database engineers will say well 10 different servers, shard it or whatever. Some of them will complain to you about consensus. In theory, it would be very simple. If you're seeing only one shards of the chain, then it's difficult to determine if a double spend has happened. The solution to that could be well why don't we assign different coins to different shards? Why not make that a rule? And we can easily code this in the definition of a coin. Well a coin exists in this part of the chain, and I would argue that in a system like this, be it 4 chains or some crazy binary tree, I should be able to go prove to you that my coin is valid by showing you that it was created, it existed at some point, and maybe at when it was spent it was reassigned to another chain. At each step, I should be able to prove this to you.

I call this an transaction history proof. We don't need anyone else to validate it. We just need that consensus. I don't have enough time to talk about how we will get that consensus. Assume for a second that we do get that. In that scenario we have another interesting property, if we have a scheme where some miners mine the shards. If our protocol rules say that any block is valid, then this could potentially scale. What's hard about this system is that both those blocks are invalid because they needed to trust that other people were doing their job. However in a truly sharded system, it's the client's responsibility to validate and ensure rules were followed.

We want to take coins in at one transaction, combine them, spend them and split them, just like we do in bitcoin right now. If you look at the bitcoin transaction graph, you get this quasi exponential blow-up. If you pay me, and I go back in history, pretty soon my coin is dependent on every other coin in existence. If I go back in time and invalidate one of those transactions-- if the rule is that every transaction in history must be valid, then my coins are invalid unless I give you all the data. If you happen to have fiber internet to the home and maybe fiber with cell phones... but we want to do better than that.

We can linearize that history. What we're doing here is we're relaxing our rules a little. We're saying rather than guaranteeing inflation hasn't happened, we're guaranteeing it probabilistically instead. You could imagine if you have a transaction with 2 inputs. You could pick one of the inputs at random, as a rule. And if one input is valid, then we prove it. And if it's not valid then the transaction is invalid. So how do the numbers work out? If we have fake inputs, and we work out the math, we can solve the expected return for trying to fake something. The long story short is that you end up with-- creating a fake input to a transaction- your'e jus tas likely to destroy the real inputs. You can create a system where you must commit to in advance to spending the coin, and there is a certain probability of it being picked; if the false input is picked, then you have destroyed real money on the real inputs.

Well, now the question is of course, what do you use to go pick this? There's some wokr on modeling the blockchain as a random beacon that nobody can influence. There are some papers on this, go look at it. "Using bitcoin blockchain as a random beacon" is a title of a paper on this subject, for example. There are reasonable approaches here that could work. I did some simulation on this; what you're ooking here is that, if you pick a random input in bitcoin, and follow it back, how long does a proof end up being? Well, I went and looked. Essentially nearly every transaction terminates in a coin creating out thin air at a coinbase transaction in about 2000 steps. This is basically based on the inflation rate of bitcoin. Put another way, this would be in terms of blocks. So this graph here, I'm saying what block number did I end up when I went back in history to create this proof in my simulation work? This graph is more linear, and I'm not sure why yet. I'm going to have to do more research on the properties of this kind of transaction graph. With bitcoin inflation rate, which is actually kind of high, in actual real world data, we're terminating in at most under 3,000 blocks.

Well how much data do you need for a proof of publication system? The amount of data to show that a transaction hasn't been spent is osomething probably on the order of revealing a 128 bit key. So that's maybe 16 bytes, maybe some overhead depending on the exact mechanism you use... so this could be a 100 byte proof per block to maybe 1 kilobyte per block. So this is 30 to 350 megs of proof. So for me to give you a coin, I'm giving you that many megabytes worth of data. It kinda sucks, but it's plausible that I could transfer you a gigabyte of data to give you a coin. What's interesting is that if you can shard the underlying proof-of-publication layer is that we have something that scales in a big way. I'm provin with you with data that nobody else needs to see; that's where the gigabytes are coming from. Most of the transaction graph can be completely discarded.

Of course there's one caveat here, which is that defining protocols is tough. In bitcoin since we have miners attesting to what consensus is, it's easy to tell when the consensus has failed like when one person is using a slightly different version of the protocol than someone else. In a proof-of-publication system, it's not necessarily true that you would notice that. To give an example, consider the not entirely readable ethereum protocol spec in their yellow paper. This is probably the best attempt at specifying consensus.... well when the DAO hack happened, they ended up specifying things with links in a medium.com blog post. Ultimately it needs to be easier to specify protocols so that we can write in a language designed for this for what's a valid transaction. You would probably have 10 different implementations for moving the data around. But we need to agree on what's valid and what isn't. I would not be surprised if apologies to Blockstack that if they run into these problems too. I know Counterparty and Mastercoin have had these problems. It's going to be a tough problem to solve. Thank you. Questions?

# Q&A

Q: Miners let anything into a block. What about transaction fees?

A: In practice you would give someone a proof saying here's a transaction, it's not valid yet, but if you put it into a block it would be valid and you can skim off the top of the transaction.

Q: It seems confusing to me-- right now we have this scarce resource of block size. In your case it would be unlimited because it wouldn't matter. So I'm wondering if that's a correct understanding. Is it totally uncapped? Spam response is on the sender of the coin?

A: I didn't specify in this talk what the proof-of-publication layer would look like. I've done some work in my treechains vision I guess it wasn't a full proposal. There are tradeoffs here. My suspicion is that this is a fundamental tradeoff. Priority would be paid for by fees in that kind of system. Equally I could imagine where instead of one chain, we have ten chains that are equal, and somewhat loosely coupled. And then we have a much bigger block size but the miners have to go and process less data. I think there's room to explore implementation details here.

Q: If you shard the blockchain, then how can I pay from one of these shards to another shard? Does this work? Are they pegged?

A: It does work. It's because when I give you money, I'm proving you the validity of it, across different shards. For example, if I start out in the red shard, and I'm proving to you that the coin is not spent for some part of history and that when it was spent it was committed to a different place. For that next part of history, it would be the same type of proof for that other shard. Even if someone is mining one particular shard doesn't have the full history, they are just proving the history was published and it cannot be rewritten. I can still prove that data to you by giving it to you as a client. That's the key difference there.

Q: You're entangling randomness over time. You have a complex system where everything is being intertangled by these proofs such that you can't reproduce those without that time?

A: I'm not sure I would say it like that. I think the idea about reproductions is interesting. In these systems, very little of the data needs to be public. If you have a transaction and the definition of a valid spend is that you publish the signature for some hash, nobody else needs to know what the signature means. You can conceive of a system where signatures go into a blockchain and they are encrypted. So when I prove to you that I have not spent the utxo already, I give you a decryption key, and you scan through it and test-decrypt all data, and then when the actual spend happens, you decrypt it, check the signature, and you're done. Everybody else doens't know what's going on. This is similar to Adam Back's committed transactions. In Adam's transactions, it's a fungibility issue where yes it will eventually get revealed.

Q: When you mention DEX, do you have a more expanded explanation of that?

A: DEX is also a drug. You could probably buy it on Silk Road. If you look at Christopher Allen's work, it's probably <http://weboftrust.info/> to find DEX. I can't point you to fully running source code.

Q: In this system, would the shards be running the same protocol?

A: Not a problem. But also not a part of this talk.

Q: For linearization of the proof, you need a public random source. So you want to take that from blocks in the future?

A: That's a tricky engineering question. If you look at the paper I mentioned, essentially what it's doing is finding how expensive it is to influence the result of that random beacon. And if you can... suppose you had full ability to influence that. You could make money out of thin air. So you need to tightly put bounds on how much mining power it would take to throw away blocks that would otherwise contribute to value, in comparison to influencing the value. A simple way to understand this is to think of the blocks being used as input to a random block and you can put bounds on how much you can move the final values. But this is a research question.

Q: You can influence the randomness at a certain cost. And if you need to flip 1 bit to make a valid proof into an invalid proof then this might....

A: With the random walk suggestion, you would need many blocks in a row to make an invalid proof into a valid proof. Or you could have this so that you-- mining is what lets you create coins out of thin air. You institutionalize the fraud.

Q: Even before I spend my coin, I could test my proof goes through with that randomness and depending on that I either spend it or not spend it. Or maybe I send it to my self, and then spend it in the next iteration because the randomness is different?

A: This is similar to fiat-shamir transform where you bound how much you can influence this simply because hash functions act like pseudorandom number generator. It holds promise.

Q: Is it an accurate or oversimplification-- value hashcash.. present proof that I possess a fraction of htis hashcash, and use a proof-of-publication mechanism?

A: I would agree with nearly all of that. I didn't mention what would lead to the creation. But chances are it would be hashcash by making every block worth so much. There are ways to do this like in treechains for example. You could use this for a centrally issued token for example with some initial issuance.

# References

<https://petertodd.org/2016/closed-seal-sets-and-truth-lists-for-privacy>

<https://petertodd.org/2016/state-machine-consensus-building-blocks>

<https://petertodd.org/2016/delayed-txo-commitments>

<https://petertodd.org/2015/why-scaling-bitcoin-with-sharding-is-very-hard>

<https://petertodd.org/2014/setting-the-record-proof-of-publication>

<https://bitcoincore.org/logs/2016-05-zurich-meeting-notes.html>
