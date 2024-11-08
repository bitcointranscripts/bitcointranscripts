---
title: Graphene Set Reconciliation
transcript_by: Bryan Bishop
tags:
  - P2P
speakers:
  - Brian N. Levine
---
Brian N. Levine, College of Information and Computer Sciences, UMass Amherst

This is joint work with some people I work with at UMass, including Gavin Andresen.

The problem I am going to focus on in this presentation is how to relay information to a new block, to a neighbor, that doesn't know about next. This would be on the fast relay network or on the regular p2p network. It's about avoiding a situation where, the naieve situation is to send the entire block data. Alice gives block data to the Bob person. She gives the new block. Bob says i don't know about it yet, why not send it? And then there's... here's the blockheader and here's the full set of transactions that are there. There's really no need to do that.

The reason why we want to do this is that block announcements are faster when they are smaller. It's easier t oget through firewalls with fewer packets. There is less forking in the network when the announcements are faster. And mining gets more efficient and there's more security with higher hashrate and so on. So let's see if we can reduce the amount of data that goes between Alice and Bob. This is not about reducing the size of the blockchain. It's just about Alice and Bob informing each other about new data.

The protocol that I am going to describe, Graphene, is about 1/10th the size of current methods, particularly compact blocks. We are able to get these gains by combining two known solutions from the set reconciliation literature-- bloom filters and IBLTs. You probalby know aboutbloom filters. IBLTs will be described.

Why does this work? We are optimizing the special case that is that everyone needs to know everything all the time. And blocks are comprised of transactions that are probably widely known already. Set reconciliation is where we both have the same information and there's some subset of the data that we want to agree on. We don't want to exchange the data again. Only once.

We have to build graphene up from some other protocols. We are going to start with compact blocks, then go to xthin blocks, and then "Soot" (a fake protocol), and each time I will change some aspect of the protocol to make it more efficient. And then IBLTs and then Graphene.

# Compact blocks

You probalby know about compact blocks from bip152. There are enormous savings in compact blocks. Why would you send the full transactions? You can just send the txids. You don't need to send all 32 bytes of those txids. You can get away with 5 or 6 bytes because the hcances of a mistake are 1 in a trillion, and it's easy to recover from a mistake almost instantly anyway. So if you do this, you go from a 1 megabyte block with maybe 4200 transactions would be expressable in 21 kilobytes. And an 8 MB block is down to about 164 kilobytes. So this is the gold standard that I want to beat in this talk. Here's a full review of how well compact blocks do. It's based on a small python simulation we wrote. It grows linearly- the amount of data exchanged between compact block users is at first small but it grows linearly. This is our point of reference. The top axis, this is in terms of transactions I make the assumption that the size of the block is that many transactions times 256 or something.

# Bloom filters

Can we do better? Yes. We can make use of bloom filters. As I said before, the reason why bloom filters will work is that neighbors have these transactions already and they are probably only missing a few. Alice can use bloom filters based on her mempool or something. In case you don't know, a bloom filter allows you to check whether some item is a member of a set. If you don't know bloom filters, it's an amazingly fantastic data structure you should know.

We make a bit array of seven entries. I am going to insert an element into the bit array. I'll hash my transaction. Let's say there are two hash functions we send it through. I send it through hash function 1 and it tells me-- I send it through the hash function and then i XOR it with the size of the array. That's index 1. Then I set the bit. I send it through the other hash function and I get index 4 and I set that bit. I want to add another element. So I take transaction 2, I send it through hash 1, it says set index 0, and it just so happens to collide with the first transaction and we set index 4 again. So there's some collision there. Now I would like to send this to Bob and he will check whether a certain transaction in his mempool is in this block. He will check against the bloom filter bit field. He will send his transactions through the same hash functions. He arrives at the same values. He checks cell 1 and cell 4 and it appears that yes transaction 1 is in this set. Similarly he might take some transaction 3 which was never a member of the bloom filter, and he might get cell 1 and cell 5 and sees that since cell 5 is zero, there's no way that transaction 3 could have been in that blom filter, and that's a true negative. But false positives are a problem. It might collide with two cells that we already set to 1, and we get a false positive. False negatives are non-possible, that's left as an exercise to the reader.

If you don't want false positives, you have to make the array larger. Bloom filters have this tradeoff. If you need a low false positive rate, you need to make the bloom filter larger. You need to send as few bytes as possible over the network.

# Soot

In xthin blocks, it's previous work that used bloom filters. What we're trying to do is we're going to- Alice is going to say, hey I have a new block. Bob is going to say okay, I want that new block. Here's a bloom filter of everything in my mempool, please send anything you think I don't have, and then she will send the transactions and txids. I am going to put this aside because it's more data than compact blocks itself. There's another way to solve the problem. Assume that Alice will prioritize sending transactions that appear in the block-- what I mean is that Alice will say to Bob, here is an int we have never spoken about, it's in the next block. So Bob just gets notified about that. We don't need bloom filters from Bob anymore. So ... the size of my mempool is m, so Alice says, let me make a bloom filter of all the transactions in this block, and I will set the false positive rate to be 1/m where m is the value that Bob gave.  How many false positives do we expect here, if bob sends every transaction through the bloom filter? It's 1. We expect 1 to happen here. That's not very good by the way because if every time that Alice says to Bob I have a block for you and Bob says here's how many transactions I have here's a bloom filter so that you can filter down... we expect Bob wil include one transaction not in there.. the merkle tree he forms, he wont be able to recreate the block, it will be invalid. To solve this problem, you lower the false positive rate of the bloom filter, make it much larger. So say it's 1/(100 * m). So we only expect this to fail 1% of the time onw. And when it does, we fall back to compact blocks. Seems like an efficient protocol, right? This is the "soot" protocol by the way. It doesn't exist. How much data it sends over hte network is dependent on the size of the mempool, because that's the parameter for the size of the bloom filter. So we're doing a bit better here. Can we do better?

# Invertible bloom lookup tables (IBLTs)

These are not as well known as bloom filters. They are a bit more complicated. There is more functionality in bloom filters than you need for this talk. The basic idea is a generalization of the bloom filter concept. There are set reconciliation data structures in the literature. At a high level, we're not using a bit. We keep count of the numbe rof elements we have happened to insert into each cell. We take an element we want to insert, we get the indices through the hashing, instead of setting the bit to 1, we are going to store a counter. We are handwaving here. There are real details which I am skipping.

Say i have an IBLT of a certain size, I have inserted some transactions or whatever. With IBLTs, unlike bloom filters, if you have 2 of them, and they differ by no more than 15% then you can perform a subtraction operation on them, it's not the normal subtraction operation, and you get the symmetric difference back and you get the elements back. You learn which element was in which IBLT. So you can get the difference. The symmetric difference is 2 in this example. And what's great about this is that the size of the IBLT- and this is counterintuitive-- the size of the IBLT does not depend on the initial list, but only on the symmetric difference that you expect to be able to decode after subtraction.

If I had a million or a trillion elements in those two lists, their sizes would be the same- it doesn't matter, it only matters that they differ by 2 elements. IBLTs can be very small if you can manage that expected difference.

Let's try to apply this in a fourth protocol with IBLTs. We are prioritizing transactions that appear in a lbock if they haven't been sent already. Alice says new block ,Bob says great I don't have that yet pleas esend it. Alice sends an IBLT of all the transactions. Bob says thanks, he doesn't send anything back. Bob says, let me create an IBLT of my mempool, I'll do this subtraction operation which is from the Epstein paper I listed on the slide earlier... And if it decodes, then we're done. What I mean by "if it decodes", the IBLT has to account for this 15% difference. If it can't, then you have to make the IBLT even bigger. So you have to fail and then double it and try again. So really what's going on is that the size of the IBLT is the amount of data we're going to send over the network.. is based on the difference between the mempool and the block. Mempools are not always small. They grow enormously large. This IBLT solution will use an enormous amount of situation in this situation.

In this graph, you see compact blocks in red. Things are great when the mempools are mslal because you don't have much symmetric difference. You can see this green line where the IBLT blows up in size to account for that. The solution fails there.

Can we do better? Yes.

# Graphene

Now you know the problems we're trying to overcome. Expensive to use bloom filters when the mempool is large and the symmetric difference is high. Same with IBLTs. You use a bloom filter to reduce the symmetric difference... then you solve hte problem of letting a couple things go through with an IBLT. The IBLT cleans up the mess. The mess is small. The IBLT itself is also small, as a result. Because bloom filters are probabilistic, although you know the expectation of how many things are going to fail, you don't know which things are going to fail. And it doesn't matter-- the IBLT will recover which ones anyway.

We can set the bloom filter to a false positive rate to 1/size of the mempool. We expect one false positive. The size of an IBLT is based on the size of the expected difference-- say one transaction. That's a tiny IBLT, it's almost nothing. If you read our paper, you can parameterize the false positive rate of the bloom filter, and the IBLT settings, in one equation-- I'm kind of lying here-- but I'm not. The false positive rate is 1/this denominator. The bloom filters have ceiling functions... the work is no different computationally, I'm not hiding a complex computation.

Here's the protocol. Alice says hey I have a new block. Bob says great, here's the size of my mempool. Alice says great, I am going to use this formula from the previous slide, I will create a bloom filter that is the right size such that the size of the bloom filter and IBLT is at its optimal smallest point and hten Bob receives that, he sends lal of his mempool transactions through it, and he builds an IBLT, and then he decodes the difference, he subtracts i from i prime and then he's done. If this doesn't work, then Bob asks for a larger IBLT to account for some weird probabilistic failure. The failures rarely happen- it's 1/1000 rate. If you tune the parameters, it never happens really. These things randomly fail but they don't if you do it right.

So a 1 megabyte block... it has 4000 transactions in it. Compact blocks was doing something like 20 kb. But the graphene solution is doing really well the only disadvantage is that the size increases with the size of the mempool but I have a mempool with 100k transactions and it's not growing that fast at all. If I expand this to larger blocks, you can see that the same scaling properties hold. It's really 1/10th. If the mempools go up beyond that, it wouldn't grow much faster.

Graphene fits in one IP packet. Compact blocks do not. There is no increased time. There's no significant use of storage or CPU. Combines bloom filters and IBLTs. There's a small write-up I made at this URL.

<http://forensics.cs.umass.edu/graphene>

# Q&A

Q: Obviously you are talking about bigger block sizes... hard-fork to... by these results... is this theoretical, or are you expanding the bcash blockchain? They don't have enough transactions to ttest this...

A: This is all just python simulations.

Q: Simulation of what? testnet? bcash testnet? Where is... is this all simulation? Are there a testnet bitcoin where this has been tested?

A: So the question is how did I get these results. This is a python simulation of Alice talking to Bob. I would love for someone to code this up and use this on a real network. Nobody got hurt in the making of this transaction.

Q: How does the receiver expect the order of the transaction? Do they bruteforce it?

A: If you have an order for the merkle tree... then you have a problem because there's no efficient way. In the worst way it's n log n bits to describe the order of something. In the best case there's a known canonical ordering. In that case, these results are small. If you have to have non-canonical ordering, then these results would be higher. That green line would go from 20 to like 80 or 100, still left than half of compact blocks. You are raising the minimum of what it takes to describe a block t osomeone. Graphene at this point is doing its best at its theoretical minimum lower bound on describing a block. It would overwhelm. All of the cost is in specifyin the order, block propagation would be about specifying order.

Q: It's not clear to me why you are trying to find a difference between mempools. Since blocks are fairly specific in size, why not just try to consolidate the top megabytes of the mempool by economic order?

A: Are you asking if I am trying to find a mempool difference?

Q: Seems like you are deriving the IBLT by the mempool..

A: I'm not. The mempools is over.. Sorry, the IBLT is over just the block from Alice's perspective. From Bob's perspective, it's just the transactions in his mempool that goes through the bloom filter. The IBLT tells him which transaction it is.

