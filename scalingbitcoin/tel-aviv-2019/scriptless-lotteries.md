---
title: Scriptless Bitcoin Lotteries from Oblivious Transfer
transcript_by: Bryan Bishop
tags:
  - cryptography
  - adaptor-signatures
speakers:
  - Lloyd Fournier
---
<https://twitter.com/kanzure/status/1171717583629934593>

# Introduction

I have no affiliations. I'm just some guy. You're trusting a guy to talk about cryptography who got the date wrong. We're doing scriptless bitcoin lotteries from oblivious transfer.

# Lotteries

Imagine a trusted party who conducts lotteries between Alice and Bob. The goal of the lottery protocol is to use a cryptographic protocol without having a lottery trusted party. The idea is that the honest parties have a 1/n chance of winning each time.

# Scriptless

Bitcoin has a way of specifying spending rules on coins. We use a cryptographic protocol to realize the conditions under which the coins can be spent. The conditions can be spent, and somehow the person will be able to magically arrive at a signature. You can use instead of OP\_CHECKMULTISIG a threshold multisig scheme, or you can replace HTLC by using "adaptor" signatures. These two things, you can pretty much replace most of the useful stuff you can do with bitcoin script. I think you can do almost all of lightning, but Andrew who came up with adaptor signatures said no you can't-- timelocks maybe.

Scriptless is interesting because they are more efficient and more private. Also, it's interesting to know what w ecan do and can't be done without script. What do you really need scripts and opcodes for?

<https://bitcointalk.org/index.php?topic=355174.0>

"..I think the multi-party lotter y scheme still rates as the most advanced usage of script yet found in the wild." - mike hearn, this was before lightning but it's still up there.

So what we will be doing today is showing a lottery that doesn't use a script at all.

# Lottery without a trusted third party

You need to fairly generate randomness, no OP\_RANDOM, you need a few other requirements that I am going to skip over apparently.

# Coin tossing

There was a seminal paper in 1981 called "Coin flipping by telephone" but people quickly called it coin tossing instead or something. This was Manuel Blum in 1981. Alice sends a commitment to a coin toss to Bob, Bob sends his coin toss back, Bob checks Alice's result against the commitment. The result is computed against both coin tosses.

# Hash-commitment coin tossing

Here is how the bitcoin version works. Alice chooses a random bit, and she commits to it with a hash function with a long random string or nonce. Bob sends his value, and Alice sends the value. Hopefully, no party aborts. The thing to make note of is that you can get Alice, she learns the output first. There's no way to solve this problem, but you can sprinkle some blockchain to solve some problem, but generally Alice always learns the value first. She might not release the preimage to tell Bob that she lost. So a lottery protocol has to overcome this.

# First attempt at lottery protocols

<https://bitcointalk.org/index.php?topic=277048.0>

Many of the original protocols use collaterla to force both parties to reveal pre-images. Adam Back came up with a more appropriate idea, which is that if some party doesn't do something at some point, then they just lose all the money instead.

# Miller-Bentov 2016

There were quite a few academic papers after that thread, like 4-6 papers or something. There was one that succinctly summarized the idea with the "Zero-collateral lotteries in bitcoin and ethereum" paper. So you both have a fund transaction, you sign into it, but you already have transactions spending from it before you put it on the blockchain. Each transaction acts like a state. The funding goes down; Alice can move it to the next state by revealing her preimage, and then-- so she already has that transaction signed, she needs the value to go to the next state, and then in the next state, Bob can take the money if he reveals a value such that his value and Alice's value can do something interesting. Otherwise, he can't do anything except wait for a timeout where Alice gets the money. There's no collateral in this. It's what we want. The winner just takes out the bitcoin with probability 1/2.

This is probably the simplest hash-commitment lottery protocol. What you can see is that you got these hash preimage reveals, but if we want to make this scriptless; we can replace HTLCs with adaptor signatures normally, but in this case we can't because you're revealing the preimages but you're actually spending the money on a function of the two preimages. It's some predicate on the two preimages determines whether it can be spent, it's two preimages and a predicate. It's a non-trivial use of script, it's interesting that we can do this without any script at all.

# Scriptless lottery through oblivious transfer

We want Alice and Bob to pay into a funding setup transaction, and then we want no script used at all to do this. We're going to change the cryptographic primitive to oblivious transfer instead of coin tossing. Manuel Blum also came up with this idea in 1981. He came up with two ideas for doing random bits. He did coin tossing, and also oblivious transfer.

Oblivious transfer is where Alice transmits 1 of n messages to Bob of Bob's choosing but Alice doesn't learn which one that Alice transmitted. The sender doesn't know which message was sent. The receiver only gets one of the messages. Alice has n messages, Bob chooses one that he wants to learn, Alice doesn't learn which one he learns. That's the basic idea.

You can get a random bit from that. Bob chooses a random bit, Alice chooses a random message, and Bob learns the message according to his bit. He learns the result after Alice sends her bit over, he sends the message he learns back to Alice, and Alice looks and sees hwich message did he choose to learn, and then she picks based on that.

# Oblivious signing

It might not be clear how to go from that to some kind of bitcoin protocol. We're going to do oblivious transfer of signatures. It's not just "messages" arbitrary. It's not quite obvivious transfer, though. If we replaced the messages with just signatures, what would happen is that Alice could just put one message as a signature and the other one is just garbage and then Bob does oblivious transfer and he gets the signature and he thinks everything is fair but Alice knows which message he got because the garbage was the other one. So we have to have some verifiable oblivious transfer, called oblivious signing.

Bob chooses which message he wants signed, and Alice doesn't know which one was signed. We're going to use oblivious signing. We have a fund transaction that we sign last, and we first sign the child transactions. By the way, this is all predicated on having Schnorr signatures and you could probably do it with ECDSA but that's not this talk. You have to sign the transaction scaffold after you choose the key securely. You have to sign all the abort transactions and the lottery winning transactions. For the Bob wins transactions, you have to do oblivious signing, at Bob's choosing, but Alice doesn't know which one he chose her to sign. Then you sign the transactions to fund. Also, these transactions have timeouts where the other party wins. If you have a secure oblivious signing protocol, then each party would win 50% of the time here. So the only options are either Alice wins and Bob timeout loses, or Bob wins and Alice timeout loses or something.

# Adaptor signatures (Poelstra 2017)

I am sure you have seen these before. Here they are in multiplicative notation instead. You have an auxiliary point, this conditional point that you add to the signing algorithm. You multiply the nonce value by this. The s value you get out of the signature is missing the discrete log of the condition. There's Y condition and y the satisfaction of the condition. An important feature is that the signer learns little y once they see the signature. So then you learn little y when you see the signature on the blockchain.

# Oblivious signing again

Alice to give Bob adaptor signatures where Bob only knows the completion for one of them. We need Bob to know a discrete log of some point but only one of some set of points. So a pedersen commitment is given of a certain form; it's impossible to decommit to more than one value without knowing the discrete log of some h with respect to g.

If we can instead fix C to 0 or 1, then the committer can only know the discrete log of T or  TH^(-1). They can only know the discrete log of one of those two.

To put these two ideas together, the idea is that you can only know the decommitment for one pedersen commitment, and adaptor signatures. Bob has a choice, 0 or 1, he generates a random y value, and--- Alice creates two adaptor signatures, one on T and one on TH^(-1) and then sends them over to Bob. He has to verify both of them, that they are all valid adaptor signatures. He verifies both of them, and then he completes one. That's it, that's how we get oblivious signing.

# Security

Security for the sender is that if Bob completes both adaptor signatures, saying that he reveals the completion, or revealing the discrete log of the condition, then we're going to learn the discrete log of T and TH^(-1) which Bob learns-- so the discrete log.. violates that the discrete log is hard, so Alice has that security in that respect.

It's information theoretically impossible for Alice to learn which choice Bob made, it's indistinguishable from random.

I came up with that, I was very happy with myself. I don't invent cryptographic primitives very often. I decided to call it "oblivious signing" and then I googled it and found out that someone else already wrote it up, in 2008 (2006?).

# Two-party oblivious signing

Not so fast! our transaction outputs are locked by joint public keys. Both Alice and Bob have half the public key, so we can't just use that algorithm by itself, we have to change it a bit. I think these changes preserve the security from the slide before.

They both choose joint nonces, we did this already. Along with T, Bob sends his half adaptor signatures for m0 (BobWin0) and m1 (BobWin1) under B0 and B1. Alice calculates the full adaptor signatures and sends them back to Bob. So we've managed to do two party on the joint public keys.

That's it, we did it. Just to recap on this, so now Alice posts the fund transaction, she picks one or picks zero, Bob now if he chose the same bit as Alice he is able to take the money, and otherwise Alice takes it. With 50/50 probability, Alice is going to win the lottery.

# Summary

Lotteries were previously an eample of something that could only be done with non-trivial scripts. But they can actually be done without script, and actually they can be done efficiently without script and still on-chain. Obvliious signing with Schnorr signatures is secure and efficient (at least as it is used here).

Some unsubstantiated claims: you can do lotteries with different odds by doing 1/N oblivious signing rathe rthan 1/2. You can cooperatively complete the lottery in two on-chain transactions. I think you can execute the cooperative protocol in a payment channel, where it's a UTXO in a state of a payment channel, and even do it in a "multi-hop" but that's conjecture. There can be a guy in the middle who has a lottery on his left hand side and a lottery on the right hand side, and he's guaranteed to lose one and win the other and he doesn't know which one and he will be a man in the middle, and you can do that recursively so you can do many hops of that.



