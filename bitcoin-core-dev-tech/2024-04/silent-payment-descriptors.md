---
title: Silent Payment Descriptors
tags:
  - bitcoin-core
  - descriptors
  - silent-payments
date: 2024-04-09
---
Silent payments properties:

- two ECDH with each scan key
- cost of scanning increases with number of scan keys
- multiple address = tweak spend key with label

We wouldn’t wanna flip that because then the spend key would be common, reducing anonymity and adding extra  scanning work

BIP352 recommends NOT using with xpubs, it’s really difficult to have same public key with different chain codes.

Use case question: with silent payments, let's say I make a legacy wallet and want to use one of my existing pubkeys and just combine it with a scan key, is that something that someone could make up. The scan and spend keys are not intrinsically tied, same as key and chaincode (no derivation between them)

We need a more narrow set, if you combine these two keys together, they make a set.

It is limiting but the use cases we eliminate are slim.

Whats’ referenced in the BIP?

- If you want multiple silent payment addressees, and you want anonymity, you need multiple silent payment WALLETS
- 1 address per wallet
- 1 scan key per wallet
- you can have multiple spend keys per wallet (using labels)

The work that wallet has to do is known, constant.

Alternatives reintroduce gap limit (don’t know how deep to scan to find all funds, etc) we don’t want any state: scan chain, guaranteed to find funds.

So, 

1 silent payment address per hd key

1 descriptor is one address

Weird alternatives like multiple silent payment addresses per wallet, stop it from happening by not mentioning it.

Remember:

A descriptor is not an address

Descriptors leak privacy (no need to hide “scan” data in descriptor)

Data overview:

address: scan public key, spend public key

watch-only:  scan private key, spend public key

spend: scan private key, spend private key

Let’s call it "scan entropy" so it doesn’t get confused with private keys, and also it will be included in “public” stuff like descriptors for watch-only wallets.

Maybe hex-encoded the data or something to make it distinct from private keys which must be kept secret?

Motivation behind BIP352 recommendation to use HD wallet (with m/352’/0 path) was so someone can start using silent payments with an existing wallet

In descriptor land we can have arbitrary restrictions

"if you use a silent payment descriptor, you can not use an xpub"

Is that a good idea?

Is it possible to derive one key from the other?

There was a lot of back and forth about this writing BIP352

They do it in Monero: view key is hash of spend key

But we think they should just be independent

Can chaincode in xpub be the scan key?

Descriptor format is starting to emerge…

sp(sppub....)

sp(spprv....)

It would be xpub-like but it would not allow derivation like bip32 xpub

sppub =  scan entropy + spend public key

spprv =  scan entropy + spend private key

We can add another key expression like with musig?

Use one derivation instead of two, where the chaincode is actually the scan entorpy

Could have an sp() expression that transforms xpub into sppub

That’s not in line with deriving them individually though

BIP352 specifies ECDH protocol, does not specify the key derivation. You just need 2 keys, we don't care where they come from. So maybe new descriptor BIP specifies that it comes from chaincode, it’s ok to update BIP352 for this.

Ok say there is going to be derivation where xpub -> sppub

What if you derive scan key and spend keys independently? Are you screwed? Or how do you make a descriptor from that? What if you generate an xpub from dice?

Allow user to pass in key expressions to descriptor, like:

sp(xpub) or we can also allow sp(512 bits)

Use case: Use my two existing private keys to make a silent payment wallet

We could create a new function xpub(64 bytes) then sp(xpub(64 bytes))

Break it down, this is just about encodings… just the essential data

2 things we need to approach:

1. What is wallet giving user (RPC listdescriptors)

2. What can user give wallet to reconstruct (RPC importdescriptors)

Silent payment address is already done.

listdescriptors, what does wallet give me?

sp(sppub...)

or with private keys sp(spprv...)

importdescriptors, what is allowed?

same as listdescriptors

but also… sp(sppub(64 bytes in hex)) ?

Do we expect other wallets to implement all this as well? (yes.)

So, the canonical format is sppub... The recommended format for export is sppub...

However, an allowed use case for *import- is to construct a pair of keys where they are split.

Like, we can take any key expression! sp(keyexpression1, keyexpression2)

We must enforce that the scan key MUST be private key

The wallet user NEVER has any need for scan public key (that goes in the address, just for sender)

How do we parse a descriptor for output in bitcoin core?

When we parse it, then toString() you get back what you parsed.

If you do getdescriptorinfo of sp(sppub...) you’d get sp(sppub...) and that’s confusing, but we already have this behavior where you get a normalized private key in getdescriptorinfo – its just confusing, not really bad.

So we can mandate sppub and give people tools to generate it from whatever else they have.

getdescriptorinfo is unrelated to anything we store in wallet DB.

We normalize the descriptor and the checksum of ORIGINAL string.

We don’t give back original string because it might include private keys.

We never want to return a private key unless explicitly asked.

NEXT FEATURE!

We could also export descriptor to include *found- 32 byte tweaks needed at spend time.

(but you need the UTXO to spend from anyway)

That is a nice to have, to export list of tweaks so another wallet that doesn't know about silent payments can import something.

This out of scope for descriptors.

Use case: import wallet from backup without having to scan chain to *find- funds.

You can backup a descriptor along with all found outputs so an external wallet just gets computed scriptpubkeys. Bitcoin Core cant even use that anyway…

We can have a separate index for tweaks-per-utxo.

This is useless in bitcoin core wallet, we can not just scan UTXO set, our wallet requires the full previous transaction to spend an output.

Dropping this discussion as out of scope and not needed, for now.

OK, THE SPECIFICATION!

Define these two new data strings, similar to xpub and xprv but bech32m encoded:

"sppub1" + 32 byte scan entropy + 33 bytes spend public key

"spprv1" + 32 byte scan entropy + 0x00 + 32 bytes spend private key

- note bech32m recommended character limits because it affects error detection guarantees

The proposed descriptors format:

1.

sp(xpub.../with derivation)

sp(xprv.../with derivation)

This uses the chaincode as scan entropy and private key (or public key) as spend key.

This is okay for importing but we never want to give this to a user because it is not what an xpub is.

2.

sp(KEY1, KEY2)

KEY1 = key expression that MUST be private key (scan entropy must be private)

KEY2 = key expression that can be either public or private (public or private key for spending)

example: sp(xpub…/352h/0h, xpuv…/352h/0h)

3.

sp(sppub...)

sp(spprv...)

We always return this from bitcoin core RPC

SOoooooo, do we need both xpub and sppub? Yes, so that we have something to give the user that is not confusing.

4.

Maybe we need a function f(xpub) -> spub then we only need sp(f(xpub)) and sp(sppub)

Discussion results: Let’s only support 2 and 3
