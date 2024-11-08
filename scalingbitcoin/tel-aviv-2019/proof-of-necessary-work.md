---
title: 'Proof of necessary work: Succinct state verification with fairness guarantees'
transcript_by: Bryan Bishop
tags:
  - research
  - proof-systems
speakers:
  - Assimakis Kattis
---
## Introduction

I am going to show you proof of necessary work today. We use proof of work in a prototype. This is joint work with my collaborators.

## Problems

We wanted to tackle the problem of bitcoin blockchain size increases. Every 10 minutes, a block is added to the blockchain and the blockchain grows linearly in size over time. Initial block download increases over time.

## Proof of necessary work

We use proof-of-work to verify transactions. We allow lite clients to verify state with minimal processing. We generare proofs "for free" through PoW. To bundle this in, we can generate proofs for free by leveraging the fact that proof-of-work currently is sort of very computationally intensive.

## Design challenge

There are some important results from theoretical computer science. We can create small succinct proofs from any NP statement. Such proofs can verify previous proofs efficiently. Also, you can use recursive SNARKs. This is really important because we can use this idea, we can have our proof verify the previous proof so that the previous block was correct, and the current transactions in the system. This means we're immediately going to have a proof from genesis up to this point that-- sort of a proof that the whole state is correct.

So what we want is the proof that verifies correctness of the chain, small enough to enter the blockchain (succinctness) and can be checked with very minimal resources.

We use recursive SNARKs which are a specific instantiation of incremental verifiable computation.

## Proofs of state validity

We feel it's natural that incrementally verifiable computation fits into bitcoin.  .... The miner has to keep all of the state, but it's the miner so we're fine with this large memory requirement. We use a merkle root, and the previous proof, and the verifier is going to have to do a cheap computation to check that indeed this is actually correct. We do this throughout every single block, and we attach these proofs to the block.

## Prototype design

We designed a prototype that is account-based and has simple payment functionality. We wanted to establish a proof-of-concept, so there's no UTXOs, no scripts, and there's none of the hunky transaction types. We just wanted to double check that this thing is something we can get numbers for and that they would be feasible. So we did this, and we got some numbers here.

We did our benchmark on AWS ra5.2xlarge with 8 cores and 64 GB RAM.

We're using libsnark and rank-1 constraint systems. It takes about 2 minutes to process these 25 transactions on this benchmark using sort of IVC prototype from a few years ago. I'm not an expert on what's the most cutting edge way of doing IVC. But the idea is that even on a system like this, we're still within the realm of feasibility. Our proofs of the whole system and state sort of, the correctness, is only a couple hundred bytes. We thought that was the demonstration that this is definitely something that could be instantiated.

## What did we achieve?

Our prototype produces block headers of <500 bytes in size, for any number of transactions per block.  The number of transactions doesn't change what the proof size is. It doesn't matter how many transactions there are in the block, you still get a small blockheader. Stateless clients can just take this proof and immediately verify it almost instantaneously.

We could optimize this to get something like 100 transactions/block using something like libsnark, which is a couple of orders of magnitude slower than some of the new stuff coming out. However, the problem is that proofs take a very long time to generate. We would like to incentivize people to make these proofs, and the natural idea is to make the proof-of-work do it.

## PoW from proof generation

We're going to follow Nakamoto consensus in bitcoin. We're going to add a random nonce to the proof on every single iteration. The miners can randomly sample this, and this will change pi or the proof. The nonce is randomly sampled, changing pi. Probability of success is exponentially distributed. The problem with this approach is that when you're doing double-sha256, you can't really split the sha256 up into different parts and compute them once and then churn on the rest. With SNARKs or these proofs, that is something you could definitely do. So this process favors large scale. A large miner will be able to calculate the proof at the beginning, change the nonce, and then only change the parts that effect the nonce. I drew some diagrams to try to demonstrate this.

## Modeling proof generation

I want to give a high-level idea of what the model is here. We need to ensure by predicate (proof) is hard to solve in general. We model this using a hardness oracle O. The oracle is going to be providing the miner with the hard computation. The number of times that the miner queries the oracle is sort of the number of hard computations that they have to do. We want, every single time they make a new proof, we want them to not be able to reuse previous information, and they must query the oracle the same amount of time always. We don't want the prover to reuse any previous information, if we want the same model as double-sha256. In current succinct SNARK implementations, the oracle provides access to modular exponentiation in some prime order group G. This reduces to harndess in the generic group model.

## Formalizing the model

We formalize the model with the notion of epsilon hardness. A large prover only gets an epsilon advantage from previous computation when generating proofs. A definition of epsilon-hardness is provided in the paper.

## Committing to the nonce

We commit to the nonce in the proof. If the nonce is random, then changing any of the inputs without really changing this nonce, is going to lead to an invalid configuration. This really prevents any previous work from being reused. Say you try it with a nonce, you're out of luck, you try again. The nonce is going to change a lot of things inside the proof, so your previous computation is useless. The end result is that we want the miner to compute the whole proof from scratch.

## Adding nonce to state

In the account based model we use, we store state in a merkle tree, the leaves are accounts. For every transaction, we have to check old merkle paths, compute new merkle paths, and check that signatures and amounts are valid. The idea here is that we want to link the state and nonce through a 'seed' parameter. It's some function that is unpredictable, we hash all of them, and we get some value. The end result is that altering any part of the input is going to lead to something that is required, and we are going to formally check this. This is unpredictable by the cryptographic hash function. This is sort of the value we're trying to go to plug into the rest of the proof to make it impossible for an adversarial miner to excervate.

## Creating hard predicates

The problem is that this only requires access to state. An adversary can reuse work as p doesn't alter the vast majority of computation. So the goal is to alter the predicate to embed it into the proof.

Strawman: insert n in every updated leaf. New merkle paths then change unpredictably as a function of the nonce. If we could inject our nonce in all of the merkle paths, then we would be done. The problem is that we only alter half of them. This gives an epsilon of about 1/2.

The new idea is to modify hash function by 'cloaking' it with p. The design challenge is to modify our hash function to use p 'almost everywhere', while outputting the same result as before. We want to take this hash function, make it output exactly the same thing on the output, but all the intermediate steps should be a function of this row which should be computationally unpredictable.

We do the cloaking with a pedersen hash. This leverages some specific properties of Pedersen, namely the homomorphic properties. This doesn't add a lot of constraints into the proof system; it doesn't make the proof substantially larger. We do need to verify that this is an actual input; and this adds a linear amount of constraints, which can increase the proving time of our circuit.

## Putting it all together

We demonstrate how to cloak predicates with a nonce n, making information reuse impossible. What's the theoretical limits for this? For a 20 transaction predicate, there's like 6 million constraints, which means we lower bound our epsilon by 20% per block in our predicate when the implementing the previous ideas without optimization. It's the predicate of the whole block; we can use the cloaking technique for the rest of the computation namely things like the signatures, we use Schnorr, and some of the other stuff. That's really not that important, it is important I just don't go into it here because it's not the majority of the computation. We think it's promising that we can put epsilon down so low that we can have a negligble overhead for large miners.

## Proof chains

Proof chains from bitcoin-ng a few years ago are a similar idea. Discarding previous profos is wasteful, so can we do better? It's easy to extend this and get some throughput, like "Proof Chains" where we require miners to build on top of previous proofs up to some largest level, until they find one that satisfies the difficulty, then they publish it all on the chain and this means that some previous verification can be ... while keeping all the nice properties from Nakamoto consensus.

## Related work

An ideal proof system would require verifier succinctness (for efficient IVC), also be trustless (no trusted seutp), and also be quantum resistant. Recent work is rapidly approaching these capabilities. Since our modification are on the predicate layer, such improvements are complemetnary to our approach. Our work uses IVC as a completely black box. As long as you can use Pedersen, we can switch into any proof systems that have the same guarantees.

## Future work

We would like to generalize this to arbitrary proof system. We want to be watermarking some of these systems. We also want to design cloaking properties for other (faster) hash functions. We would also like to extend to full bitcoin functionality, which might require a soft-fork.

