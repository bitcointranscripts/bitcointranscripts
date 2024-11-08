---
title: 'Cross-Chain Swaps: Atomically Swapping Coins for Privacy or Cross-Blockchain Trades'
transcript_by: Bryan Bishop
tags:
  - privacy-enhancements
  - coinjoin
  - coinswap
speakers:
  - Ethan Heilman
  - Nicolas Dorier
media: https://www.youtube.com/watch?v=NedW6AhImKg
date: 2018-10-05
aliases:
  - /scalingbitcoin/tokyo-2018/edgedevplusplus/cross-chain-swaps
summary: Ethan and Nicolas describe atomic cross-chain swaps - a protocol where two parties can exchange coins as a single operation. The exchange does not require any trusted third party and neither of the parties involved can cheat each other. They describe how this can be used on a single blockchain as a privacy protocol or “cross-chain” as a trading protocol.
---
<https://twitter.com/kanzure/status/1048017311431413760>

## Introduction

We are Ethan Heilman and Nicolas Dorier. Ethan is from Boston University. Nicolas is from DG Lab and working on NBitcoin. Today we're going to be talking with you about atomic swaps for privacy and for cross-blockchain swaps. When we say atomic swaps, what do we mean? At a very high level, the idea is that it enables Alice and Bob to trade some cryptocurrency. But they shouldn't be able to cheat each other. The good part about being able to not cheat each other is that the trade is atomic. So it either goes through completely or not at all, but never partially. If it went through partially then one person would get the other party's money but the other party wouldn't get money; so it's really important to have atomicity in this type of trade. We want to be able to do this without having a trusted third-party. Usually, there's a custodian that does the swap for the two traders, which ensures fairness. However, with blockchain, we can do this without a trusted third-party. The blockchain acts as the third-party. As I said before, either the trades occur or both parties get their coins back. We assume the parties are malicious and they will do all sorts of crafty things to try to cheat each other. This protocol should work in the presence of malicious participants.

## Use cases: cross-blockchain trades and privacy

The first use case is a cross-chain atomic swap, which is an atomic swap in which someone has one cryptocurrency and the other party has a different cryptocurrency asset. It could be Alice and Bob and bitcoin and litecoin. Alice sends Bob litecoin and Bob sends Alice bitcoin.

Another use case is using atomic swaps for privacy. This is useful for obfuscating a coin's transaction graph. Alice and Bob each exchange with each other 1 BTC so that the origin of the coins is not so easily determined by someone analyzing the blockchain graph data. This can increase the fungibility of bitcoin and makes it a better form of money. Alice and Bob trade bitcoin UTXOs of the same face value to increase privacy. This is identical to the cross-chain swap but it's a same-chain swap.

## Atomic swaps within the same blockchain

Let's look at a very simple atomic swap, within the same blockchain. There has to be a protocol for Alice and Bob to find each other, which has its own privacy implications of course. They have to find each other and then agree on the amounts that they are going to be using in the atomic swap. You could use two commitment transactions and then a third transaction where the swap is performed. You could also pre-sign the swap transaction thanks to segwit and the loss of txid malleability. The third transaction is where the swap occurs, but it is signed first, before the commitment transactions are funded or broadcasted. Notice that this is atomic, and it satisfies the atomicity requirement.

This is a simple form of a coinjoin.

* <https://diyhpl.us/wiki/transcripts/scalingbitcoin/milan/joinmarket/>
* <https://diyhpl.us/wiki/transcripts/building-on-bitcoin/2018/coinjoinxt/>

## Non-atomic cross-blockchain trade

Let's look at a non-atomic cross-blockchain trade. This is broken. Alice asks Bob hey do you want to trade some litecoin for bitcoin. Bob says yes. Alice posts a transaction on the litecoin blockchain which sends litecoin to Bob. Now Bob has litecoin and bitcoin. If he's an honest participant, he would then post a bitcoin transaction on the bitcoin blockchain giving Alice the agreed amount of bitcoin. Unfortunately this is not atomic. Alice cannot cheat Bob in this setting, so it's fine if Alice is untrustd. However, if Bob is malicious, Bob can cheat Alice by not posting the bitcoin transaction. He can get the litecoin from Alice and not give any bitcoin to Alice.

The way to prevent this is to use hashlocks. You might be familiar with HTLCs (hash timelock contracts). That's what we're going to use here.

## Hashlocking funds

A hashlock is a requirement you place on funds such that to spend the transaction output you have to provide a value X such that the Hash(X) = Y. You have to use a hash function where it's hard to discover the preimage given the hash.

A simple example of a hashlock is that Alice chooses a random value X and hashes it to get Y. Alice then creates and a posts a transaction which is locked under two conditions: (1) it needs a signature from Bob, and the second condition is that the input that spends it must also provide an X such that Hash(X) = Y. So if Bob learns the value X, then Bob can spend transaction 1 outputs by using Bob's secret key to generate a signature and also providing the X value. We can use this to make an atomic cross-chain trade. The idea here is that Alice is going to choose a random value X and hashes it to get Y and she is going to post transaction 1. She is not going to tell anyone what X is at this point, she keeps it as a secret. Bob waits for transaction 1 to be confirmed, and then posts transaction 2. At this point, Bob doesn't know what X is. But he knows that if he learns the value X then he can claim money from the outputs of transaction 1. Bob knows this is safe to do becaus ethe only way that Alice can take money out of transaction 2 is by revealing X, and if Bob learns X, then he gains the ability to get money out of transaction 1. So Alice waits for transaction 2 to be confirmed, and then posts transaction 3 which reveals X. This grants Bob the ability to get his money because he now has the preimage. He can get his litecoin now. This is the simplest version of an atomic swap. Alice has swapped litecoin for bitcoin, and Bob has swapped bitcoin for litecoin. They use a hash preimage to make sure that the transaction is atomic.

Alice could give the preimage to Bob, but Alice wants her coins. She wants to post the transaction at some point. Conceivably, she could give it to Bob and maybe she's not sure what output she wants to spend it to, so she gives the value to X and then later in 2 hours she decides she wants to spend the money over here and then post this transaction. But we're assuming these are mutually untrusting parties. Alice only releases the value to get the money. She could tell Bob about the value, though. Often when we build these protocols, if this was happening in a payment channel, Alice wouldn't have to show Bob the transaction instead she just shows the preimage and then she can post the transaction at her leisure. Great question.

Notice that if Alice doesn't spend this money, then Bob can't claim the litecoin from transaction 1. What happens if Alice or Bob... or what happens if Alice goes away and she never proceeds? Bob's money is then locked forever. That's not great for Bob. You could blame Alice because she set this up and then went away. Bob was trying to make a trade, and now his funds are locked basically forever.

So we need to add an additional condition called a timelock. This will allow for the funds to be refunded after some time has passed. Timelocks are an additional condition that say that after a period of time has passed, both parties can take their money out of these commitment transactions if the protocol hasn't been completed by some future time limit.

This timelock protocol is known as the TierNolan atomic trade protocol.

## Full TierNolan atomic trade protocol

Bitcoin has two different kinds of timelocks. It has three, actually. We're going to talk about two of them. There's checklocktimeverify and checksequenceverify. In this talk, we're only going to talk about checklocktimeverify. And checksequenceverify allows you to do relative timelocks, relative to when the transaction is posted. And checklocktimeverify allows you to do absolute timelocks, so it's based on a specific blockheight or a specific timestamp.

Something to note about the TierNolan protocol is that Alice can go last. Alice has the ability to decide whether the trade happens. So you could imagine Alice could say look at-- if the timelock is 3 days, Alice could look at the market and then decide whether the trade is going to make her money. You have to be careful about who you are trading with. They can't steal your money, but Alice could choose to adversarially have your trade happen or not happen.

## Full TierNolan atomic trade protocol: timing

I am going to show this with blockheight. You want the timelocks to probably do blockheight or blocktime which is the timestamp inside the block. Blockheight is fairly risky to do for different blockchains because the mining levels may increase or decrease in unexpected ways, and it's really important that Alice's refund happens after Bob's refund. If Alice's refund happens before Bob's refund then it's no longer safe, and Alice can cheat Bob in that case. So to keep these in sync, it makes more sense to use blocktime than to use blockheight ofr the timelock restriction.

## Full TierNolan atomic swap protocol (again)

I attempted an implementation of the atomic swap protocol a few years ago. It was two blockchains based on bitcoin. It could be BTC and LTC for example. The process was the following. There was Bob that was giving his public key to Alice. Then Alice from this created an offer to Bob that said okay let's swap this amount of bitcoin against this amount of litecoin. Here is my hash and my public keys. Most people get enough informatoin to create the transactions from that in the way that Ethan presented to you. There's an offer transaction that gets signed by Alice and on the other side there is a Bob transaction signed by Bob. The scripts are either Bob signs with a secret that only Alice knows, and then maybe a timeout.

<http://bitcoin.ninja/checkscript>

## Privacy

We will discuss two protocols. One is a simple coinjoin, and the other is Maxwell's coinswap. In a simple two-party coinjoin, this is the version of that protocol requiring new public keys. As long as the inputs have the same amounts, you shouldn't be able to tell which output belongs to Alice and which output belongs to Bob. The probability of you guessing correctly is 1/2, basically a conflip.

## Private atomic swaps (Maxwell's coinswap)

<https://bitcointalk.org/index.php?topic=321228.0>

Imagine that Alice and Bob put their coins into a 2-of-2 multisig output. The coins are controlled by Bob's public key and Alice's public key. They both sign transactions that say if the value X is revealed then this can be spent by Alice and if the value X is revealed then Bob can spend these outputs over here. Alice then releases transaction 6 but notice that these haven't been confirmed yet. These are off-chain transactions. Alice can construct the transaction privately but not send to Bob. If one of the parties defected and try to go to the blockchain, Alice can post the transaction but she doesn't have to construct it and send it to Bob for Bob to learn the value X.

## Using payment channels

You could take Maxwell's coinswaps and generalize it to payment channels. As before, everything is locked up into 2-of-2 multisigs. They perform the protocol that I just showed you for coinswap. Rather than posting the final transactions on the blockchain, they could just perform another coinswap by transmitting some more coins. They could in real time decide they are going to trade 2 LTC for 2 BTC or 4 LTC for 1 BTC and keep a running tally and then finally close out the last state. You could use this to perform more than one trade, once you setup the 2-of-2 multisig transactions.

## Privacy summary

Maxwell's coinswap makes cross-chain atomic swaps indistinguishable from four multisig transactions on different blockchains, although they might be able to correlate by price, timing, network information. They are strictly more private than if you were to expose the information or use other atomic swap protocols.

There are some privacy-focused atomic swap protocols like Barber's fair exchange (XIM) and [tumblebit](https://diyhpl.us/wiki/transcripts/scalingbitcoin/milan/tumblebit/), which uses signatures in a way where you can't link the preimages together.

## References

* <https://diyhpl.us/wiki/transcripts/bitcoin-core-dev-tech/2018-03-05-cross-curve-atomic-swaps/>
* <http://diyhpl.us/wiki/transcripts/layer2-summit/2018/scriptless-scripts/>
* <http://diyhpl.us/wiki/transcripts/building-on-bitcoin/2018/blind-signatures-and-scriptless-scripts/>
