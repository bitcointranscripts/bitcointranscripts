---
title: Compact Multi-Signatures For Smaller Blockchains
transcript_by: Bryan Bishop
tags:
  - research
  - threshold-signature
  - bls-signatures
speakers:
  - Dan Boneh
date: 2018-10-06
media: https://www.youtube.com/watch?v=IMzLa9B1_3E&t=1610
---
Dan Boneh (Stanford University), Manu Drijvers and Gregory Neven (DFINITY)

paper: <https://eprint.iacr.org/2018/483.pdf>

<https://twitter.com/kanzure/status/1048441176024469504>

## Introduction

Hi. Thanks a lot for coming in after lunch. This slot is often known as "the slot of death". Some of us are jetlagged, this is the perfect time to doze off and only wake up at the end of the talk. I'll try to prevent that from happening. I think the best way to do that is to start about what this talk can do for you. This talk is going to be about signature schemes that allow signatures to be compressed in size, which will save space on the bitcoin blockchain and allow more transactions to get in the blockchain.

You guys all know what bitcoin transactions look like. There are inputs and outputs. You can use the p2pkh scheme, where the input is pointing to a previous UTXO. It's a pretty simple system.

## What multisigs can do for you

We have two multisig schemes, one that requires pairing and another that just uses classical discrete log. It can compress multiple signatures into a single signature. It's one element and one exponent in the discrete logarithm scheme. In the pairing scheme, you can compress those signatures even further and just use one signature for the entire block and all its transactions, which is one group element in size.

Doing some of these changes would break the basics of bitcoin because you could not verify individual inputs anymore. This may be hard to introduce. In the short-term, it has some application to something called multisig address. There's some confusion about multisignature and multisig.

## Multisig address

A multisig address is where the output contains a hash of a script that specifies a list of public keys and a threshold for the number of the public keys. Any input that wants to spend the coins from that output has to provide some threshold number of signatures from those public keys, and possibly denote which of those keys are being used, and thereby authorize the transaction.

## What multisignatures can do for you

We have many schemes for you in the paper. For the special case of n-of-n multisig schemes, where all the signers have to sign and agree, there we can use either a pairing based scheme or a discrete log based scheme. What they allow you to do is compress all of htose public keys into a single aggregate public key which is only one group element in size. It can also compress all the signatures to a single group element in size for the pairing scheme, or one group element and an exponent in the discrete logarithm scenario.

## What aggregate multi-signatures can do for you

You can aggregate across transactions and within transactions, to get a single signature for the whole block.

## What accountable-subgroup multisigs can do for you

What about any threshold that you want to use other than n-of-n? We also have a solution for that. This is maybe the more novel scheme we offer, if we were talking at a crypto conference, by which I mean cryptography (there, I said it). I would focus on this one. It's a use case that could be interesting. There are workarounds for doing k-of-n. I'll show some detail on tihs later. One of the schemes we have is called "accountable-subgroup multisig scheme", what it allows you to do is to compress all the pubkeys into a single aggregate pubkey for all of them. For any subset s of the signers, and--- any of the subset of signers, and the signature would be just two group elements large, irrespective of the number of signers and also who signed will be accountable and it will be clear. You will know who has signed. We're looking at a threshold scheme here, and you could have some other schemes where certain keys have more weight than others. This is pretty cool, and it's independent of the group s of signers, you get a short signatures. By specifying the group of people who can sign, this can be done succinctly, and you could write a list of indices in a sorted list of the public keys, or take an n bit string and set the bits of certain signers to 1 if they are participating, it could be t log(n) or n bits, whichever is smaller.

## Partially-aggregate ASM

This is only partial: only one of the groups can be aggregated, one group element per signature will be necessary per transaction here.

## Witness size per block

This has been taken from our paper, we are going to present our paper at Asiacrypt later this year. There's a lot of parameters to take into account. How many inputs are there in a transaction? What kind of thresholds are we using? How many transactions are there in a lbock? This is for some typical parameters. The main numbers to look at right here ar for the discrete log scheme and our pairing scheme. Under current circumstances, our schemes can allow you to save 1 megabyte of space per block on the blockchain which is nothing to sneeze at.

## This talk

I am going ot start off by giving some more background on discrete logarithms and pairings, then we will talk about BLS signatures and rogue-key attacks. The problem of using BLS signatures in a straightforward way for multisignatures. Then I will be ready to discuss secure multi-signature schemes with key aggregation, and accountable-subgroup multisignatures.

## Background on discrete logarithms and pairings

Most of you will know this. Discrete logarithms (DL) and computaitonal diffie-hellman (CDH). Given a group element X, you have to come up with an x that is the discrete logarithm of this X with respect to your generator P. This is assumed to be computationally hard. There's also the computational diffie-hellman (CDH) problem, where it is hard to come up with an element C which is the product of the two discrete logs a and b.

Pairings are curves with a special property that there are a pair of groups g1 and g2, and a function e which is the pairing with a bilinearity property where if you pair two elements from the two groups then you have their discrete logs written explicitly here: anything in the multiplier can be taken into the exponent of the pairing, and can be used as a multiplier on the other side. You get some funny properties from this, where you can move multipliers from one side to the other in the pairing.

There's also a variant of the CDH problem called co-CDH. We use another one called psi-co-CDH. For certain curves, psi-co-CDH is efficiently computable and then this becomes co-CDH assumption. But in typical type 3 curves which are considered most secure today, this function is not computable, so it has to be an assumption that even in the presence of an oracle this problem remains hard.

## BLS signatures and rogue-key attacks

These cannot be used in a standard way to build multisig schemes. Suppose you have a hash function that maps messages into the generator in group 2... You multiply it with a secret key.... As a signer, you take a hash of the message, and you multiply it with your secret key. If we have bilinear maps, by verifying it against the pairing of the public key with the hash of the message, the sk can go on top and back in front here, and therefore this equality would have to hold for the signature to be valid.

## Composing BLS signatures

This signature scheme is pretty cool and has many uses. You can compose signatures, compress signatures, and it seems really straightforward how you can do this because you can simply add up all the signatures. If you want to verify this, you can do this by verifying this product of pairings right here.

* Boldyreva 2003
* Boneh-GLS 2003

There's a rogue key attack here. If you know someone else's public key, and you choose as your own pubkey something for which you don't know the secret key, but you take the group public key to be something where you know the discrete log, then you can break the multisig scheme. But, we oculd insist that all the messages being signed are different. This is what the 2003 BLS paper does, and then you can't aggregate pubkeys anymore. Another alternative is including proof-of-knowledge in your public key, but your public keys will grow. Another alternative is to do smarter key aggregation.

This borrows something from the MuSig paper. We prove that this technique also works for BLS signatures. So you have this exponent that are different for all the public keys, you take the full set of public keys, the aggregate public key is then computed as a weighted average over all of those public keys. It's not in the paper, but we realized you could do slightly better by optimizing this and taking the first exponent to be 1, and then all the other exponents are multiplied to be different from 1, and this saves you a little bit on computation and this might matter for small n. Combining is then adding keys together and then you apply those coefficients on it. Verification is done identical to standard BLS signature. You have an aggregate public key here, and it just takes two pairings in order to verify this.

## Multi-signatures from pairings (MSP)

This is provably secure under co-CDH in the random oracle model.

## Aggregate multi-signatures from pairings (AMSP)

You have to be careful; you have to get the aggregate public key into the hash in order to sign. Aggregate is just summing up the keys, and the verificatoin is a product of the pairings here.

## Interactive multi-signatures from discrete log (MSDL)

I'll go a little bit faster here. From discrete logs, take the Schnorr scheme and turn it into a multisig scheme. Doing this is delicate. There's a first version in the paper from Maxwell-PSW 2018 v2. It had a slight flaw in the proof originally but then it was fixed. At the same time we had the same scheme in our paper. It's 3 rounds of Schnorr multisignatures with a 3rd round used for provable security. Verification is the same as for Schnorr signature so that works out really well.

## Accountable-subgroup multisignatures

This is addressing the use case of k-of-n. This is like normal multisig for different groups of k, and hash those into a merkle tree so the different aggregate or subsets enter the root here and then when you prove a certain subgroup then you should show the mekrle path and then a multisig under that root. That works if k-of-n chooses... is not too large, but it stops working when it becomes very large. Using our accountable subgroup multisig scheme, you can also do this when t and n are of arbitrary size. For 50 signers out of 100, you can never generate this merkle tree with our new scheme you could actually do this. The only thing is that you need one round of interactive setup for the key generation. What you end up with is an aggregate pubkey for the full group in one group element, and the signature takes two group elements plus a description of the size of the set of the signers that participated.

## Our ASM scheme

I am going to skip describing how our scheme actually works. There's an interaction requirement. Signers can sign non-interactively after that. It's secure under the co-CDH assumption, and you could evne further aggregate this if you want to.

## Proofs of possession (PoPs)

Pubkeys get larger and they get into the blockchain. There might be cases where proof-of-possession scheme might be useful to you.

## Conclusion

What multisigs can give you is savings in the witness length when using these schemes. Going for n-of-n multisig addresses, you can use 144 bytes if you use the pairings version or 96 bytes in the MSDL case. In k-of-n multisig, it's 32 bytes plus k, or n/8 B + 192 bytes for ASM. It would be great to see this adopted but I'm sure there's plenty of practical, technical and political arguments not to do so. If we could help with any of those, then we would be very happy to do so.

