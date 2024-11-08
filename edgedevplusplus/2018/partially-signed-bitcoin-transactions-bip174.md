---
title: Partially Signed Bitcoin Transactions (BIP174)
transcript_by: Bryan Bishop
tags:
  - psbt
speakers:
  - Greg Sanders
media: https://www.youtube.com/watch?v=iJR9Lg1jyJg
date: 2018-10-04
aliases:
  - /scalingbitcoin/tokyo-2018/edgedevplusplus/partially-signed-bitcoin-transactions-bip174
---
<https://twitter.com/kanzure/status/1047730297242935296>

## Introduction

Bryan briefly mentioned partially-signed bitcoin transactions (PSBT). I can give more depth on this. There's history and motivation, a background of why this is important, what these things are doing. What is the software doing?

## History and motivation

Historically, there was no standard for this. Armory had its own format. Bitcoin Core had network-serialized transactions. This ensures fragmentation and it's incomplete and bad that there was no standard. For segwit, a transaction to a legacy node looks like a zero-input transaction, which is a way to flag it as a segwit transaction. This sometimes gets software confused, even segwit wallet software. It sometimes think it's a legacy transaction with zero inputs. There has to be a better way. This incongruity also increases the workload of developers to support various things such as hardware wallets or external signers, such as wallets that don't have the keys local.

A couple months ago, we had Andrew Chow at Blockstream (who is also a Bitcoin Core developer and Armory maintainer) work on this. Over some years, he got some feedback and finalized something as bip174. It's been just released in Bitcoin Core v0.17. It's all there. Armory and various hardware wallets are also supporting it. The coinkite cold card wallet basically just takes a PSBT file, signs it, and hands it back to the user. There are other libraries that now have support for it, including rust-bitcoin and others.

## Transaction signature validity

In general, if you're a transaction signing program and you are given a transaction to sign, and you have no additional information, it's hard to reason about what is this transaction and what it's doing. A hardware wallet has no memory available for the most part, it has no sense of the UTXO set values, and it is not usually running consensus rules. In Bitcoin Core previously, and ledger wallets, or trezor wallets, you had to feed the previous transactions or the previous inputs or at least the whole output information for segwit inputs, into the hardware wallet. Wallet needs to have all the previous transaction data.

Beside that, the previous transaction data isn't sufficient. If you're signing p2sh or p2wsh, then the signer might not know the script- they might just have the hash of the script and not have the redeemScript. Bryan mentioned logic like "I'll sign anything that gives me more money" but how do you figure that out? PSBT can help solve this.

Also, you need key paths. You need to feed this data to the hardware wallet somehow.

All these details come together as crucial for anything working remotely well. Each signer has different hardware and different signers and there's no good solutions. Custody solutions today are haphazard and they only work with maybe one or two different kinds of setups.

## PSBT fields

I'll go over some of the data fields. It's encoded in base64. It's engineer-readable, maybe not human readable. The fields are key-value maps. They carry all the information necessary for the signer to reason about the transaction, and to solve it in the sense of how to sign for it, and then sign for it. Eventually, finalize the transaction and make it completely signed instead of partially-signed.

There's a "global type" field, and there's currently only one, whic his the unsigned transaction itself. It's the raw unsigned transaction itself. It should not carry any witness data in this form. These are all kept blank.

And then there's "per-input types" that start at index 0 and move onwards. There's non-witness UTXOs where you have to include the entire transaction because you take the entire transaction, you get the txid to hash it, and then you check it's actually the same and it matches, and it's the hash of the transaction. For a segwit UTXO, you can work it around a little bit and only give it the serialized output itself, just part of a transaction. This is due to the fact that signature hashes in segwit include the value under the sighash. If I claim it's 3 BTC, then when the hardware wallet wants to sign, it says well this is 3 BTC and then verifiers will check this. If I lied to you and it's actually 4, then it will be an invalid transaction.

There's also "partial signature" as part of per-input types; it includes a key and signature value. There's also a sighash type which is an advisory thing; the default is SIGHASH\_ALL where you hash the entire transaction and sign that. There's other sighash types as well, which other people have talked about today.

Also there's "redeem scripts", which is recursively evaluated.

There's also "witness script", and "bip32 derivation path" for each input. It can be any number of them; the key is the public key, and the value is the master fingerprint and an index array of indices that get you there. The master fingerprint is part of the extended pubkey that you were told about earlier. It just lets you identify it, no cryptographic guarantees.

## PSBT RPCs in Bitcoin Core

There's combinepsbt, decodepsbt, finalizepsbt, createpsbt, converttopsbt, walletcreatefundedpsbt, walletprocesspsbt. Once it's created, you can process it. walletprocesspsbt is where you hand it to another wallet and if it knows something about an input and an output it could fill it out and optionally sign it and then pass it off to the next machine. Once it's all done and all the partial signatures are finalized, there's finalizepsbt where you can then get the network-serialized transaction the thing you actually submit to the network. decodepsbt is useful for debugging and introspection.

## References

* <https://github.com/bitcoin/bips/blob/master/bip-0174.mediawiki>
* <https://github.com/achow101/HWI>




