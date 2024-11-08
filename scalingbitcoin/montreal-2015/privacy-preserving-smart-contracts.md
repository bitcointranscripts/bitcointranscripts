---
title: Privacy-Preserving Smart Contracts
transcript_by: Bryan Bishop
tags:
  - research
  - privacy-enhancements
  - contract-protocols
speakers:
  - Ranjit Kumaresan
date: 2015-09-12
media: https://www.youtube.com/watch?v=gpJrGuZEJsY&t=858s
---
<ranjit@csail.mit.edu>

<http://people.csail.mit.edu/ranjit/>

We have been looking at how much we can support or what limitations we might encounter. There are also efficiency issues and privacy guarantees. And then there are some potential relaxations that will help with removing the fundamental limitations and express the power and make smart contracts more useful.

The point of this talk is off-chain transactions and secure computation. I will also highlight the relationship of secure computation and bitcoin. This integration provides protocols for smart contracts that provide new perspectives on scaling issues.

The agents join the contract. Well-defined set of rules. Most things in every day life and society are just contracts. More philosophically speaking, bitcoin is a contract among miners and users of the system. We will use bitcoin and ethereum for running examples of smart contracts.

* claim-or-refund
* multi-party fair exchange with penalties

Secure computation. This is actually allows a set of distributed parties to run computation on data, and then receive results. The parties are trusting some kind of authority in the default model. The privacy and correctness would of course be placed on trust in the third-party. In the real world, there is no such party to trust. The transformation from the ideal world to the real world are of course done by secure computation protocols. They don't have to trust any party. Secure computation is an active area of research and cryptography. In the last decade it has seen enormous improvements in efficiency.

SNARKs, NIZK (non-interactive zero knowledge proofs), fully homomorphic encryption, obfuscation are all examples of secure computation. They are less efficient than secure computation itself because of the additional restrictions that they each require.

We can receive significant improvements on scaling parameters like number of agents, size of rules, size of data and privacy. Number of agents is decoupled from block size limit. We can also remove on-chain dependence. All of those computations involving rules and data are carried out off-chain. Privacy would be guaranteed of course by the crypto technology.

For stateful contracts, we can get a non-trivial as a result in terms again the privacy, but only in the stronger varaint of bitcoin, .. with example for the poker contract, we need signature verification and arbitrary data. These protocols also need large-numbers of ordered transactions. Solutions like Lightning Network can be of major help.

* A Note on Coin tossing
* Secure Multipartry Computations on Bitcoin
* How to use bitcoin to design fair protocols
* How to use bitcoin to incentivize correct computations
* How to use bitcoin to play decentralized poker
* Hawk: the blockhaain model of cryptography  privacy


Use off-chain crypto for scaling purposes, which is based on secure computation.


