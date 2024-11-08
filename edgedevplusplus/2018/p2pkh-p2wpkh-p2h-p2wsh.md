---
title: P2PKH, P2WPKH, P2SH, P2WSH
transcript_by: Bryan Bishop
tags:
  - scripts-addresses
speakers:
  - Greg Sanders
media: https://www.youtube.com/watch?v=nrYOMjVmqi8
date: 2018-10-04
aliases:
  - /scalingbitcoin/tokyo-2018/edgedevplusplus/p2pkh-p2wpkh-p2h-p2wsh
---
<https://twitter.com/kanzure/status/1047697572444270592>

## Introduction

This is going to be a bit of a re-tread I think. I am going to be talking about common bitcoin script templates used in bitcoin today.

Addresses do not exist on the blockchain. But scripts do. You've heard about p2pk, p2pkh, p2sh, and others. I'm going to go over these anyway.

## Pay-to-pubkey (p2pk)

This was the first type. It had no address format actually. Nodes connected to each other over IP address, with no authentication. You got the script directly from the receiver. The only vestiges of this in Bitcoin Core are in Bitcoin Core RPC when you run "generate" in regtest mode. The witness is empty, the scriptSig is a 71 or 72 byte signature, and the scriptpubkey is a 33 or 65-byte pubkey followed by OP\_CHECKSIG.

The signature is DER-encoded.

## Pay-to-pubkeyhash (p2pkh)

It uses base58 encoding, and addresses correspond to specific scripts, there are no addresses on the blockchain itslef. This introduces the idea of using a hash in the scriptpubkey to hide the full pubkey (and UTXO entry), at the cost of the scriptsig size. This is not consensus-special, it was just a new template that the ecosystem had to adopt, but it did not require a soft-fork or hard-fork.

## Pay-to-scripthash (p2sh)

This is the second address type that was standardized. It starts with a "3" in the address. The key insight is that the receiver is in charge of the spending policy, and should pay for increased script size. Previously with bare multisig, the sender would pay for all this upfront cost. The UTXO size was much larger in bare multisig. p2sh supports arbitrary scripts within this, up to a 550 byte push element. Due to the way it's designed, it can be at most an n-of-15 multisig. You're limited to n-of-15 multisig script. This is specifically non-segwit, by the way. It's legacy p2sh.

It runs in two stages: normal script execution, then recursively runs again on de-serialized script.

## Pay-to-witness-pubkeyhash (p2wpkh)

The bech32 address starts with "bc1". It requires segwit bip141. bech32 encoding is longer but easier to transcribe, more robust against errors, and even has error correction potential. The script evaluation is implicitly converted to something identical to p2pkh. The witness has a signature and a pubkey. The scriptsig is empty. The scriptpubkey is the 0 byte followed by 20-byte pubkey hash. So this is implicitly converted to pay-to-pubkeyhash (p2pkh). There's a couple of script changes here, mostly sighash changes for the transaction digest algorithm in bip143 or something.

## Pay-to-witness-scripthash (p2wsh)

For this example I'm doing another 1-of-2 multisig example. The witness is (0, signature1, 1, pubkey1, pubkey2, 2, OP\_CHECKMULTISIG). The scriptSig is empty. The scriptPubKey is (0, 32-byte scripthash).

So, p2wsh is a segwit address type replacement for p2sh. 32-byte hash, since p2sh's 80-bits of security was deemed insecure in the near future. 80 bits is considered insecure since there are already existing computational networks that do much more computation than that in production today, so it's considered insecure.

There's another nested loop evaluation in there, it's messy but it allows for backwards-compatibility. This is mentioned in the bip141 spec.

## References

https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki

https://github.com/bitcoin/bips/blob/master/bip-0143.mediawiki

btcdeb

bitcoin script wiki






