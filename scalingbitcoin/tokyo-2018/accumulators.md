---
title: A Scalable Drop in Replacement for Merkle Trees
transcript_by: Bryan Bishop
tags:
  - proof-systems
speakers:
  - Benedikt Bünz
media: https://www.youtube.com/watch?v=IMzLa9B1_3E&t=3520
date: 2018-10-06
---
<https://twitter.com/kanzure/status/1048454406755168257>

## Introduction

Hello. Test. Okay. I am going to talk about accumulators for UTXOs. The previous two talks were a great setup for this. This is joint work with Ben Fisch who is also here today and Dan Boneh. I first want to advertise the Stanford Blockchain Conference (formerly known as BPASE) happening at the end of January 2019 at Stanford. Whether you give a talk or not, you should try to attend.

## UTXOs

The UTXO set is a growing problem. We had a talk this morning about dust in the UTXO talk. We have about 60 million UTXOs. The problem is that as we heard in the talk before, the blockchain is quite an inefficient data structure for UTXOs because if I want to download an old block, I need all the blockheaders in between. If I want to download an old transaction and check if it's unspent and I only have the head of the blockchain, then I need to check all the inbetween transactions and check if they spend my transaction or not.

## UTXO commitments

UTXO commitments have been proposed ot solve this. As we just heard, every block gets a commitment to the current state, such as the current UTXO state. The idea here is that the consensus rules would ensure that there's an in fact a correct UTXO commitment in the header. A lite client would be able to check this. If I want to convince a lite client that this is the correct UTXO, then I neede to give him a proof that here it is in the UTXO set commitment. We could use this to turn everyone into a lite client.

## Merkle trees

The classic way to do this is merkle trees. The merkle tree is built like this. I can give you inclusion proofs to prove to you that something is in the UTXO set, and I can do inclusion proofs, it's log(n) hashes, and I can do updates in some cases, everything is log(n).

## Stateless full nodes

I can build a stateless full node that doesn't have to store the full UTXO set. How does this work? When I send a transaction, I would now have to provide a proof that my transaction is spending an unspent coin. Right now the miner checks that a transaction is unspent. But in this design, the user would prove that the coin is unspent. Then, the nice thing is that the miner who just says some storage, can just check that the transaction is unspent. This is intriguing.

## Problems with merkle trees

There's a few problems with that approach. The main problem is that these inclusion proofs if you append them to every transaction is they become quite large. Every transaction would have inclusion proofs. This would be about 160 gigabytes of extra data in the blockchain. You would need to do a lot of expensive checks when verifying the blockchain. When petertodd talks about this, he proposes to use this only for very old transactions. Most transactions should not have to use this technique.

## RSA accumulator

I want to talk about RSA accumulators, which could be a replacement for a merkle tree. We could choose an RSA modulus which is a large number the product of two primes. We also have a hash function mapping an arbitrary element into primes. Then we pick an element out of the group to initialize the accumulator. How do we use this? We might want to add sometihng ot our set. The accumulator is a short commitment to the set. If we want to add something to the accumulator, we raise the accumulator to that value. If we delete something, we take one over the element's root. Here I hash it into the primes, but for the rest of the talk let's assume every element is a prime. It's enforceable.

If I represent here the set of UTXOs, then the state of the accumulator is g to the product of all the elemnets in the set. One nice property is that it doesn't matter when things are added, but the accumulator is completely commutative. It has many other nice properties.

## Accumulator proofs

The inclusion proof is very simple, it's one over x proof of the accumulator. This can be computed using a trapdoor or a secret. We can improve that. Or you have to know the full set. If it was constructed honestly, then you get a cancelation and you get back the A value. There's a security proof that in this RSA group you can't do that operation if x wasn't in the set. I can also do an exclusion proof, which is more complex, and I'll omit the details look them up. It uses the bazooko coefficients. LiLiXue07. You can do very efficient stateless updates. I can efficiently tell you- see which transactions or which things were added or removed from the set and I can update my proof appropriately. In our paper, we have a method for this.

## RSA requires trusted setup?

You might have seen this and said well this is useless it requires a trusted seutp. Who has to do the trusted setup? What does it mean? N is p\*q and the problem is that if anyone knows p and q then they could completely break the scheme and fool you into thinking something is in the accumulator even if it isn't. The efficient delete from this accumulator needs a trapdoor. The classical scheme assumes there's an accumulator manager that does this. Also, you can find Ns in the wild (the Ron Rivest assumption). These are Ns where probably nobody knows the trapdoor, such as RSA puzzles created by Ron Rivest back in the day and he deleted the p and q and if you trust him then you can use that N value. Or there are old companies that are bankrupt now and maybe they have the key in a hardware module and maybe it ogt destroyed when the company went bankrupt and maybe you could use those but that might not be good neough.

## Class groups

Class groups were proposed in BW88 and L12. This is an amazing mathematical object originally developed by Gauss.. it's a class group of quadratic number fields and the idea is that this is a group of unknown order and you don't know how many number of items are in that group. It has properties similar to RSA but does not require trusted setup. The class group elements are a little bit shorter than RSA elements, roughly half the size.

## RSA accumulator state of the art

If you think about the inclusion proof, it's constant size regardless of the number of items in the accumulator. The whole thing is still 3000 bits. This is better than merkle inclusion proofs once the size of the set is greater than 4000 elements. You also have dynamic stateless adds, and you can add things into the accumulator without knowing what else is in there. You can use this for decentralized storage; a fully verifying node doesn't need storage, and users maintain their own UTXOs and inclusion proofs.

The room for improvement here is for aggregate and batch inclusion proofs-- what if I have many proofs, how can I aggregate them? What about stateless deletes, being able to delete without knowing what's in the accumulator? And what about faster verification?

## Aggregate inclusion proofs

Say we have two inclusion proofs for the accumulator. It turns out that we can do something called Shamir's trick to create something else such that it's an inclusion proof for both elements that you wanted to both check. If we can do this for two elements then we can do this for an arbitrary number of items. Allthe inclusion proofs in a block- instead of having one merkle path or one RSA inclusion proof for transaction, you could just use a small one for the whole block. So instead of the 160 gigabytes I talked about before, we're back down to 1.5 kilobytes which you could print out on a single piece of paper.

## Stateless deletion

If I have this trapdoor then I can efficiently delete. But what if we don't have a trapdoor? We changed the model: we assume that every time we want to delete something, I actually have an inclusion proof available. When do I need to delete something from the UTXO set? It's only when it's spent. But when it's spent, the user is providing the inclusion proof anyway. The next value of the accumulator is just equal to the proof; why is this the case? The proof is just g^(u/x) so it divides out the value. Literally the proof divides out the value. We set the accumulator to be the proof. In the blockchain it's a bit different, because we have multiple transactions and multiple inclusion proofs with respect to the same accumulator. We can use the same trick as the slide before, to compute one inclusion proof for all of them, and then that's our update to the accumulator. This is now how we have stateless deletes. This allows us to have BatchDelete function. We can have many proofs with respect to the same accumulator and delete them all at once.

## Too slow?

RSA is kind of slow, it's slower than hshes. 219 updates per second if you use a 2000-bit RSA or something. It's just a little bit slow, especially for full sync, updating the whole blockchain and you need to check all these proofs then the sync is very slow. The aggregation technique reduces the size of the proof, but it doesn't reduce the verification time.

For class groups, there are no benchmarks yet, but they are getting used for verifiable delay functions. Chia announced a competition where you either try to speed up the class group or try to break them and I think it has $100,000 in prizes. We will soon have better information about how useful and how secure these things actually are.

## Wesolowski proof (Wesolowski 2018)

We can use the Wesolowski to reduce the verification time which came up in the verifiable delay function developments.  You can also use proof of exponentiation efficiency here. Exponentiation of G vs 128 bit long division.. it's a gigantic speedup.

## Fast block validation

We can now do fast block validation and verification. Say I'm a miner and I want to compile my blocks. At the current state of the blockchain, the current accumulator state, and I remove a bunch of things with the stateless delete from the accumulator... so this is all the spends removed.. then I add the new transactions to the accumulator, and then I compile the new block, it has the headers still, and th transactions, and a BLS signature maybe so it's a small signature. And then it has these two values, so the half of the next state and the full next state, and this proof of exponentiation. What does a fully-verifying node have to do now? It has to verify the BLS signature which could be very fast, and it has to verify the two proofs of exponentiation which are also insanely fast in practice. You just have to check from there if you add s again you get here, and if you add n you get to the new accumulator state.

## Performance

What are some of the performance numbers? Take these numbers with a huge grain of salt. I did htis on my macbook using standard java libraries. For a merkle tree, an inclusion proof for 64 million things is like 20 hashes, so that's 8.5 microseconds. If I want to verify using this new Wesolowski, it's 0.3 microseconds, it's way faster than a merkle tree. For class groups, we don't know. Are they faster are they slower? The class group is smaller, so they might be faster or slower, it's hard to evaluate without having Pieter Wuille implement this.

## Vector commitments

Vector commitments are similar to accumulators. You could use this with merkle trees. It's a commitment to a vector, and I can open it at a position and tell you the vector at position x has a value and we build a new vector commitment that there were previous vector commitments from RSA but the verifier would require gigabytes of memory or linear size memory and ours basically requires zero size memory so it's efficient that way.

## Short IOPs

There's these zero-knowledge proofs like STARKs... or the class of zero-knowledge proofs called IOPs and at a high level, the prover makes a short commitment to a long proof, and then the verifier asks for some indices and then the prover sends the proofs and the merkle proofs and shows at position x the proof was this value and then the verifier can accept or reject them. The problem is that the merkle ptahs are quite long; we can replace this with vector commitments, and we can aggregate vector commitments and then this is basically like a few kilobytes instead of a bunch of merkle data. This reduces the proof size from... these numbers are from one setting, it's terrible to get concrete numbers here because you have to look at the concrete setting; for one large setting you could reduce the proof size from hundreds to dozens. Asymptotically it removes it as a factor of log(n). It makes the proofs shorter.

## Q&A


