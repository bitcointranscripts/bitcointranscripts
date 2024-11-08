---
title: Scripts (general & simple)
transcript_by: Bryan Bishop
tags:
  - scripts-addresses
speakers:
  - John Newbery
media: https://www.youtube.com/watch?v=np-SCwkqVy4
date: 2018-10-04
aliases:
  - /scalingbitcoin/tokyo-2018/edgedevplusplus/scripts-general-and-simple
---
<https://twitter.com/kanzure/status/1047679223115083777>

## Introduction

I am going to talk about why we have scripts in bitcoin. I'll give some examples and the design philosophy. I am not going to talk about the semantics of bitcoin script, though. Why do we have bitcoin script? I'll show how to lock and unlock coins. I'll talk about pay-to-pubkey, multisig, and computing vs verification in the blockchain.

## Why have script at all?

In my first talk, I talked about digital signatures to transfer coins from one person to another. So why did Satoshi add script? With a chain of digital signatures allows a digital coin to be transferred from one person to another. What if I want my coin to be spendable when 2-of-3 people sign? It might be an escrow or some cold wallet service. How do I do that? What if I want my coin to be spendable when someone presents a secret, like the preimage to a hash digest?

Instead of creating lots of special transaction types, Satoshi added a generic scripting language to bitcoin. It specifies encumberances or conditions for spending coins. It wasn't mentioned in the whitepaper at all. It might be that Script was added quite late of the bitcoin source code. Early versions of script were really ugly-- like anyone could spend anyone's coins, which was a bug. So maybe the implementation was rushed.

## What is script?

In bitcoin, a contract is a "predicate". It takes some inputs, and the outputs are either true or false. The inputs are the transaction and some additional data provided by the person spending the coin. It returns true or false. If it retunrs True, then the transaction is valid, or false, the transaction is invalid.

Contracts are implemented in bitcoin as programs written in a programming language called Bitcoin script. It's an unfortunate name but there it is. It's a stack-based language. Every operation either pushes elements onto the stack or acts on the elements in the stack in some way. At the end of execution, if the stack is non-empty and the top element is non-zero, then it returns true, otherwise the script is evaluated as false.

## Locking and unlocking coins

How do we lock coins with a condition or unlock it? A coin is locked with conditions under which it can be spent. The locking conditions are encoded with a scriptpubkey. The unlocking proof is encoded in something called a scriptSig.

Ealry versions of bitcoin concatenated scriptsig and scriptpubkey and then ran the combined script. If it evaluated to true, it was a valid spend. But unfortunately that's broken, and if you do that, anyone can spend anyone's coins. Once you know how script works, you can figure out how to spend anyone's coins. In v0.3.8, this was changed or fixed by running the scripts separately, first run the scriptsig, leave the results on the stack, and then run the scriptpubkey script.

Note that the scriptsig doesn't need to be a script; it can just provide stuff on the stack. It could just provide data.

## Example locking conditoin: pay-to-pubkey (p2pk)

The simplest scriptsig is called "pay-to-pubkey" (p2pk). The condition for spending a p2pk output is signing a message with the private key corresponding to the given public key. The message that the spender must sign is a part of the transaction that spends the output. We talked about how digital signatures work in the first talk, so this is just a digital signature over the transaction for parts of that transaction. Incidentally, this is why it's called scriptpubkey: it contains a pubkey, and the scriptsig is called scriptsig because it contains a signature.

## Multisig

Multisig is another type of locking condition. You use this when you want to encumber your coins with k-of-n parties signing it. The condition for spending a multisig coin is that you must sign it with k-out-of-n pubkeys given the script. The message we sign is the same for each of the pubkeys, it's a part of the transaction you're spending.

## Pay-to-pubkeyhash (p2pkh)

In pay-to-pubkeyhash (p2pkh), the scriptpubkey is the hash digest of the public key. The conditions for spending a p2pkh is providing a public key that hashes to that digest, and a signature of a message with that private key that corresponds to the given public key.

Any questions so far? Does it all kind of make sense?

## Pay-to-scripthash (p2sh)

Pay-to-scripthash (p2sh) locks an output with the hash digest of some arbitrary script. You provide the hash digest of that arbitrary script. The spending conditions is that you have to provide that script (called the redeemScript) and you also have to provide the data required t osatisfy the locking conditions on that script.

## Why p2sh?

Why did we do this? The scriptpubkeys for p2sh are a small, uniform size. It's 32-bytes plus filler. The sender doesn't need to know the spending conditions for what they're sending- it's none of their business. The merchant shouldn't have to tell each customer what the multisig conditions are that the merchant wants to apply. It's a privacy issue. The receiver is the one that specifies the conditions inside the redeemScript. And, in p2sh, this can be encoded in the bitcoin address format for p2sh.

## Pay-to-witness-pubkeyhash (p2wpkh) and pay-to-witness-scripthash (p2wsh)

Segwit bip141 introduced two new kinds of locking scripts. Key difference is that the data required t osatisfy the conditions is carried in a separate structure called the "witness", which is not covered by the txid. This is what fixes malleability.

## Pay-to-pubkey (p2pk) (stack example)

I'm just going to show you what it looks like on the stack when we're executing those scripts. Pay-to-public-key is the easiest, most straightforward output type. The scriptpubkey contains the public key (33 bytes for compressed keys), and the OP\_CHECKSIG opcode (1 byte). The scriptsig contains just a signature, which is 71-72 bytes.

Before execution, you have your scriptsig provided by your sender, and you have your scriptpubkey which has the pubkey and the OP\_CHECKSIG operation. You execute the scriptsig, and it's just a data element, so it's put on the stack. Next, you execute the scriptpubkey. The first element is pubkey, so that's a data element, it's pushed to the stack and the stack now looks like (pubkey, sig). OP\_CHECKSIG looks at the two elements on the stack and verifies that the signature is a true signature for the given pubkey. The stack is then left with a value "1", which evaluates to True.

## Multisig again (stack view)

For a k-of-n multisig, the scriptpubkey contains the number k (how many people need to sign) as one byte usually, and then all n public keys (this is 33 bytes each if we're using compressed pubkeys, or 65 bytes for uncompressed pubkeys), and then the number n (1 byte) for the number of total keys, and then OP\_CHECKMULTISIG (which is 1 byte). The scriptsig needs to include a dummy 0 byte because there's an off-by-one error, and then the corresponding signatures.

## Computing vs verifying

I'm going to talk about something kind of philosophical about computation and verification on the blockchain. A contract is a predicate. It takes inputs and it outputs either true or false. Bitcoin nodes are only interested in whether the contract evaluates to true. We're not interested in how it gets to true; just that the output is true and not false. Bitcoin does this using Bitcoin script, which is an interpreted language, and it's executed by every node. So we're doing a computation on every node, but it's only really interested in verification of the output, it doesn't really matter how we get there as long as it's all correct.

Adding more computation workload to contract execution does not scale in a blockchain. Verification is much easier and more scalable than computation, especially if we have things like aggregate signatures or batch validation for multiple signatures. If we had every contract just some arbitrary program in some turing complete language, then that makes for a non-scalable blockchain. At the limit, a blockchain could use zero-knowledge proofs instead of script execution. At the margin, there are lots of technologies that can improve scalability by only committing minimal data to the blockchain. If you can provide a proof that the conditions have been met, then that is much more efficient and scalable.

## Scaling contracts

What are some examples of this? Only reveal the spending conditions at time of spend, like in p2sh, is good for scaling because the spending conditions don't need to be stored by every node before that coin gets spent. This is also true for p2wsh. The utxo set kept by every node doesn't need to store the spending conditions of every coin.

We can batch multiple payments into one on-chain commitment, like in layer 2 such as lightning network. A single on-chain transaction can be a single proof of the final transaction state for tens of thousands of off-chain lightning transactions.

We could create a script where we only reveal the branch of the contract that was executed, using things like merkleized abstract syntax trees (MASTs) or taproot. We don't have that yet, but we hope to get that in bitcoin in the near future.

In the best case where everyone agrees, instead of showing a big script, just broadcast a single threshold signature and taproot and graftroot are examples of doing this. If you have a single signature, then you can batch validate that with all the other signatures in the block for example and that's really quick.

You can combine multiple signatures int oa single signature, which is easily done with Schnorr signatures and threshold signatures. Also, you can use adaptor signatures and scriptless scripts to embed the conditions into the signatures themselves.

## Privacy and fungibility

Usually, scalability improves also mean better privacy for people transacting. Transactions look more uniform and similar, which is also great for fungibility.

## Conclusion

A bitcoin output can be locked with a contract. A contract is a predicate- it takes the transaction and additional data provided by the spender and returns true or false. Bitcoin uses Bitcoin script to encode contracts and the witness data. The witness data is additional data you provide to prove you can spend or have fulfilled the conditions of the contract. Script is a stack-based language that executes on all nodes. A blockchain is for verifying, not computing. We happen to use computing in script, but all we're really interested in are, are the conditions met? And that's verification.

