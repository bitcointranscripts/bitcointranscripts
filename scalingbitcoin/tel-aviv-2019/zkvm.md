---
title: 'ZkVM: zero-knowledge virtual machine for fast confidential smart contracts'
transcript_by: Bryan Bishop
tags:
  - proof-systems
  - utreexo
  - musig
speakers:
  - Oleg Andreev
date: 2019-09-11
media: https://www.youtube.com/watch?v=-gdfxNalDIc&t=8538s
---
<https://medium.com/stellar-developers-blog/zkvm-a-new-design-for-fast-confidential-smart-contracts-d1122890d9ae> and <https://twitter.com/oleganza/status/1126612382728372224>

<https://twitter.com/kanzure/status/1171711553512583169>

## Introduction

Okay, welcome. What is zkvm? It's a multi-asset blockchain architecture that combines smart contracts and confidentiality features. It's written in pure rust from top to bottom.

<https://github.com/stellar/slingshot>

## Agenda

I'll explain the good parts, and then I'll explain away the bad parts. Sounds like a good time.

## What does this have to do with bitcoin?

zkvm is a unique combination of the best ideas in the blockchain space. Out of all the diversity of ideas and the various protocols, smart contracts, all these things, we have been picking the best things and trying to combine them into an elegant way. You can think about this as if you were to design bitcoin from scratch, this is all the best ideas of the past few years together.

## zkvm architecture

Uh oh, a blank screen. I guess it's a zero-knowledge presentation. Oh okay, here we go.

We start with a blockchain. A blockchain has transactions. In our case, transactions are programs that manipulate value and send them from inputs to outputs. This is the UTXO model. You can also issue assets. It's a multi-asset blockchain for issued assets.

## Utreexo

<https://diyhpl.us/wiki/transcripts/mit-bitcoin-expo-2019/utreexo/>

<https://diyhpl.us/wiki/transcripts/bitcoin-core-dev-tech/2019-06-06-utreexo/>

<http://diyhpl.us/wiki/transcripts/scalingbitcoin/tel-aviv-2019/edgedevplusplus/accumulators/>

Utreexo is from Tadge Dryja. I am not going to explain how this works too much. There's an excellent paper and videos out there about it. The idea is that you have a bunch of UTXOs that you want to insert into that set and delete from that set. Right now the UTXO set in bitcoin takes about 3 GB of storage, and you can compress all of this into about a kilobyte.

You don't keep the leafs, only the roots of these perfectly binanced binary trees. When you delete, you have to show a merkle inclusion proof which shows reconstruction of the tree. You can show a bunch of insertions and deletions and then reorganize the tree in a normal form. This allows you to show the tree in a compact way.

Storage is basically free now, and this means more nodes can be full nodes. We can package up this whole system as a library and put it in your application and not have to worry about dedicated UTXO storage here. You can dump all the utreexo state on the disk without a problem.

The problem is that every node has to update UTXO proofs. There's extra bandwidth overhead, but negligble with caching.

## Program execution

As I said, a transaction is mostly a program. Unlike bitcoin, you don't have a hierarchical data structure with inputs and outputs and other fields. The programs in bitcoin are localized in the inputs. Instead, there's just one flat program. This was originally done with Txvm which was previous work that we did a few years ago. Zkvm is sort of an evolution of that approach and adding confidentiality.

The other thing is a zero-knowledge proof which is a single aggregated bulletproof in the transaction.

The VM is instantiated per transaction, and discarded after the transaction is processed. So this is still stateless. It has full isolation from the rest of the blockchain state, and then you throw it away. It doesn't interact in a complex manner with some other parts of the blockchain.

So you instantiate the VM and you run the program. This consists of a high-level instruction set that enforces the network rules. You can add additional constraints inside of your contracts and can role your own custom protocols.

This is a stack machine just like in bitcoin. Things are being changed on the stack. While the transaction is being executed, it records two kinds of side effects in two arrays. There's the bulletproof rank-one constraint system. When you execute the instructions on the VM, it automatically arithmetizes the constraints and adds them to the ... but it also applies to any zero-knowledge constraints some contracts might want to have. The constraint system is verifiable in a single aggregated proof.

The changes to the blockchain are recorded separately in a transaction log. Once you have a validated transaction, you take this transaction log and apply it to the blockchain state. This is where you can apply it with utreexo, where you can fail a transaction if the output is already spent or something. But this is pretty cheap, and this allows you to verify transaction in parallels similar to bitcoin.

## Contracts

This is a generalization of what the output is in bitcoin. In bitcoin, the output is effectively a script and value. The script protects the values. You have to satisfy the script in order to unlock the value. This is the same in zkvm, but you have an extended version of what the script predicate can mean. You can store multiple values too, like one value or two values or some pure data parameters that are not money but some strings or numbers. So whenever you try to spend one, you re-evaluate it inside the VM and then have to track with this.

You can take the predicate as a public key and satisfy it with a signature. You can sign the whole transaction or sign a subprogram as a sort of delegation pattern. Once you satisfy this predicate with a signature, it unlocks it and puts it on the stack so you can use them. The predicate can also commit to the program itself. The program takes care of the systems and then decides what to do with them.

## Taproot

<http://diyhpl.us/wiki/transcripts/sf-bitcoin-meetup/2018-07-09-taproot-schnorr-signatures-and-sighash-noinput-oh-my/>

We use taproot. It's the same idea, but implemented in rust. You have a commitment to a key with which you can sign, and you have a commitment to a merkle tree of different program options. You can use both, or use just one. If you want to just sign, you can ignore the second part. If you always want to trigger some pre-arranged program, then you can set k to some unsignable key with some orthogonal generator. You can learn about taproot everywhere else, so we won't dive much more into that.

## zkvm instruction set

It has some pretty high level operations in the zkvm instruction set. There's a few instructions for manipulating items on the stack. A few that manipulate constraints. There's operations to issue and mix values. There's operations for the contracts like unlocking with a signature or program, and you can also create an input or create an output.

It's a pretty small instruction set for the features it gives you. Bitcoin's instruction set is 88 instructions. Ethereum is also pretty big. Miniscript is very small, which is cool. Zkvm is 33 instructions. Miniscript is 26 instructions.

Values are first-class citizens. You don't model them as entries in some virtual database table in the VM, instead the value is the actual tihng. It's a linear type that you can move around, split and merge.

## Cryptography stack

To implement all the cryptography-wrapped constraints, we use a pure rust implementation of curve25519-dalek which is a different curve from bitcoin's secp256k1 curve. The reason why we use curve25519-dalek is because it allows us to parallelize operations and gives us tremendous speed improvements at the level of doing the most basic cryptographic operations. Unfortunately this curve is not a prime order curve like the bitcoin one, so it doesn't immediately give you good options. We built ristretto255 to fix this.

ristretto255 gives you a safe prime order group. Everyone using curve25519-dalek should be using ristretto255.

We built our implementation of bulletproofs covering the rangeproof functionality, using a constraint system API which is currently experimental. It allows you to squeeze the ... into the middle of constructing the constraint system. Some of the weights in your constraint system can actually be random challenges when you commit to some portion of variables first, squeeze the challenge, and then create more variables later. This allows us to have shuffle gadgets implemented in linear time. This is important for the cloak protocol which is a separate small protocol which performs the merge of multiple assets... It's the sum of inputs and the sum of outputs, you can't transfer one asset into another, and htis is fully obfuscating the asset flow within one transaction, and this works on top of bulletproofs. We have custom constraints nad high-level constraints that allow you to build arithmetic expressions and logical expressions out of those. These are automatically arithmetized and compiled on the fly. The constraint API allows you to write custom constraints on the contract.

The interface to the zkvm instruction set... and then on top of that you can build your own protocol, like vaults, payment channels, orderbooks, etc. The cool part is that all of this is in pure rust. It's pretty efficient and the API is nice.

## Constraints

How do the constraints work?

You have the ability to express arithmetic expressions and boolean formulas. These are expressed in a typical Forth-like notation. You can multiply things, add things, check if some things are equal, and then build expressions. Behind the scenes, zkvm doesn't really vcompute anything when this happens. It assembles instead an abstract syntax tree on the fly and then what's on the stack--- high-level constraints and expressions, then when you want to verify it, it takes the root of the syntax tree and arithmetizes it and inserts it into the constraint system. This can be done very fast and it can be done on the fly. Any contract can do this while the contract is being verified.

## Example of custom constraints

Say you want to have a contract that checks that some payment has been made and it has to satisfy some parameter. All the parameters of this formula must be kept confidential. Once it does, it unlocks the value.

We use a pedersen commitment, and use a variable to construct a bunch of constraints and verify them. Once you will make sure the zkvm will make sure the constraints are respected, we will use the borrowed value you're interested in, land make a payment to the address you're required to meet. We do not receive a value and inspect it, instead we just forward it at zero-interest rate and send it to the other.

Negative value is mixed with an actual payment in the cloak. A variable defines a payment constraint with borrow + output. To deal with the negative value, the only way to deal with it is to mix it with others in the cloak. You leave the negative value on the stack, so the user has to find the appropriate amount to compensate when they compute their transaction.

## Linear types + capabilities

This is linear types + capabilities. We can express our requirements in an expressive way. This allows us to avoid bugs like confused deputy problem because we're not doing reflection.

## ZkVM tradeoffs

The VM is not turing complete. It's optimized for financial use cases and to borow from gmaxwell, "blockchain is important" so we try to minimize any computation on-chain. Ideally, you only see some signatures on the chain and maybe a zero-knowledge proof of a single instruction. Occassionally when parties in a payment channel don't cooperate, then maybe they reveal payment conditions and zkvm enforces that. This is explicitly not designed for arbitrary computation.

Even though we have pretty efficient cryptography and compression of the blockchain state, but the amount of data you still have to catch up with is linear. So it's similar to bitcoin, if you want to catch up then you have to get all the blocks. The known ways for us to compress this amount of data, uses entirely different cryptography and more interesting assumptions which we don't use in zkvm.

On the bright side, SVP clients which only have blockheaders and pieces of the UTXO set, and completely discarding and not verifying transactions, which is what they need to keep track of the utreexo proofs. If oyu're a lightclient with a payment channel and you want to watch the status of your channel, whether it's closed forcibly by the counterparty or just update the proofs, you need to transfer O(1) data but this will be reduced than the full transactions so you don't need to verify all transactions.

If you have a trusted sourc,e then there's a standard way to bootstrap via utreexo roots. If you have a trusted root, then you don't have to replay all blocks from the beginning of time.

## Privacy features of zkvm

The asset types, claled flavors, are private. Asset amounts are private. Data parameters are private, and you can always make them explicitly public if you want. Anything that happens within the transaction, if you have one giant cloak instruction, the asset flow is also encrypted.

What's not private are the programs (which are all available in plaintext) and the transaction graph where you can find UTXOs linked together just like in bitcoin.

Taproot reveals only a script or program in the event of dispute and only then a specific branch is revealed. So including the program might not be such a big deal in zkvm.

On the transaction graph, the alternative is to erase the links between inputs and outputs like zcash or monero. They impose some important scalbility tradeoffs. You have to store an ever-growing amount of data, like key images, to prevent double spending. This has nothing to do with cryptography; monero can use ring signatures, and zcash has to use this accumulator. You need to check that the -- is not there. So in the UTXO model, it's important that you can store only the things that you know are not spent. So that's why we don't have any transaction graph obfuscation on layer 1.

But on layer 2, you could use coinjoin. This is the distinction between TLS and tor. TLS gives you data confidentiality between point to point, but if you want extra anonymity then you have to do some extra work which is how tor works. That's the last tradeoff.

## Performance

This thing is fast. We use less than 1 ms per output, up to 1000 tx/sec. This gives us ample room for CPU performance. Custom constraints are relatively cheap. Rangeproofs for output values bear most of the cost. Signatures and custom constraints have 1-5% overhead. Also, this scales with privacy. This is a rare place where the search for better privacy is aligned with performance. Aggregation saves space and time, but also helps with privacy. Proof size is log(n) so the marginal cost goes to zero. Also, you have free storage with utreexo

## Conclusion

We have a small, pure-rust codebase. zkvm + utreexo + blockchain, 7k loc schnorr + musig + keytree + bulletproofs. We have 14k LOC for curve2519 + ristretto255. Assumptions are ECDLP on curve25519, and Keccak (shake128) is a random oracle.

<https://github.com/stellar/slingshot>

<https://github.com/dalek-cryptography/bulletproofs>

<https://ristretto.group/>

