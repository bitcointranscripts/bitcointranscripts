---
title: Silent Payments
tags:
  - bitcoin-core
  - silent-payments
date: 2023-04-25
aliases:
  - /bitcoin-core-dev-tech/2023-04-26-silent-payments/
speakers:
  - Josibake
  - Ruben Somsen
---
## BIP Overview

Scanning key and spending key are different: better security.
Silent payment transactions are indistinguishable from transactions with taproot outputs on-chain.

Q: Address labeling, why not create two silent payment addresses?

A: It doubles scanning costs.

Limited to taproot UTXOs (currently about 3% of transactions) but when it increases we should find ways to optimize scanning, even though it currently does not seem to be an issue.

Q: Why no P2PK

A: Limit to most used payment types to keep the implementation simple? No strong opinion.

Q: Do you need txindex?

A: No. It uses undo data to get the prevouts

Q: Can you prune data?

A: Yes, but can only rescan wallet history from unpruned blocks. It should be possible to recover from the UTXO set on a pruned node

## Address encoding

prefix: sp for mainnet and tsp: testnet
'q' char: silent payment v0
64 bytes concat of recipient pubkey Bm || Bscan

## Public Keys

Instead of using a single public key, use all the input public keys that were signed for
Needed to prevent coinjoin input linking (knowing who you're paying to). Also helps with scanning (only one ECDH per transaction).

One way we could do this is to limit to Complex scripts:
    Script contains a pubkey and signature
    Script is valid miniscript

Q: Why not only native segwit inputs and drop support for other types?

A: UTXOs already exist in other types, don't want to require senders to migrate UTXOs to newer versions because it is costly and raises costs to entry and hurts adoption

We want the protocol to be as easy as possible for senders and keep the protocol simple. Sending is simpler than receiving in terms of implementation.

Q: How does ECDH work with MuSig?

A: Should be fine, have not tested.

## Creating outputs

can pay multiple outputs in the same transaction
Most expensive step is ECDH, which only needs to be done once, regardless of the number of outputs

Q: Why support creating outputs to the same recipient in a transaction?

A: For paying the same entity to multiple labels and also in the case of a coinjoin where multiple participants are paying the same silent payment address

Q: Is adding keys together vulnerable to rogue key attacks?

A: Not a problem. All keys have signatures.

Q: Why increment N and not take output index?

A: Don't want to tie it to how the tx is setup -> have to check all the transaction index makes the scanning faster

Spend and scanning keys are derived using BIP32 using m/BIP'/0'k and m/BIP'/1'/k respectively.
Using separate derivation paths for spend and scanning keys allows for better security.
Leaking the scanning key does not leak the spend key and vice versa.

Q: Most wallets don't support exporting private keys

A: We talked to a few hardware wallet manufacturers and so far everyone has said  they would support it. Need to figure out a safe way to do it.

Q: Could use hashed public key as private key for the scan key if private key cannot be exported from wallet.

A: We would rather avoid it, your public key is now secret data. If you leak the public key, you would lose your privacy

You could have a dedicated wallet for silent payments.
Can generate silent payment addresses for change outputs, will not require BIP32 support.
Maybe will support marking the change outputs using labels so that when funds are restored the user can know which outputs are change outputs.

After the SP BIP is published, another BIP for Silent Payment descriptors should be published.

The receiver of an SP payment has a wallet that is tied to a full node for scanning.

Could use the script interpreter to extract the signatures from the script.
May cause issues with newer versions of taproot for nodes serving multiple light clients.
Dropping support for complex scripts may resolve issues but will reduce the anonymity set.

Versioning feature would require scanning transactions for each version.
A single input supporting SP is required in the transaction.

SP could serve as donations but also as a routing number for transactions to transfer funds to ourselves. Could also be used in username protocols

Light client process:

- Node scans the blockchain for potential SP transactions.
- Sums up the pubkeys and sends them to the light client for verification.

## Next steps

- We will update the BIP and submit it to the mailing list.
- We will convert the draft PR into a smaller PR to add support in Core, will follow up with a second PR for adding RPC coverage, etc
