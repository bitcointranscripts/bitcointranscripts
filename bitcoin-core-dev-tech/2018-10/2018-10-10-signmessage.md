---
title: Signmessage
transcript_by: Bryan Bishop
tags:
  - generic-signmessage
speakers:
  - Kalle Alm
date: 2018-10-10
aliases:
  - /bitcoin-core-dev-tech/2018-10-10-signmessage/
---
kallewoof and others

<https://twitter.com/kanzure/status/1049834659306061829>

I am trying to make a new signmessage to do other things. Just use the signature system inside bitcoin to sign a message. Sign a message that someone wants. You can use proof-of-funds or whatever.

You could just have a signature and it's a signature inside of a package and it's small and easy. Another option is to have a .. that is invalid somehow. You do a transaction with some input, where the txid is the message hash or something. We could have OP\_MESSAGEONLY, which is that if you run into that in a signature for a transaction then you immediately fail, and if it's a message then you ignore it. You can have a signmessage pubkey and a spend pubkey and they are separate.

You might have a shared wallet and those UTXOs might represent funds that someone else owns. The complication of proving funds available are what do you do about cold wallets vs hot wallets? Do you use the same UTXOs to prove those funds?

Greg Sanders wants to have use a fork id for signmessage or proof-of-funds and then just use that whenever signing, which means it would be invalid on bitcoin. Make sure that altcoins don't use this too; but what happens when they go ahead and do that? Maybe any fork id means it's a signmessage and all the replay protection goes out the window ((laughter)).

People are asking for a simple extension for signmessage that works with segwit. Turning it into a new transaction type or whatever seems like something worth solving but a different problem. For those who just want to be able to sign a message with an address, having all this complication about well okay I'm expecting a signature from you and you're giving me a signature of a transaction but it has 100 inputs and it's doing other things. What is my verifier supposed to do with that? The API gets really complicated. You're compsing all the complexity of what a transaction can do in a simple message verification feature.

What do people want this for? proof of funds, auditing, airdrops, ...?

For just signing a message with a segwit address, there's already an electrum/trezor thing which is adding a flag to the existing signature. It's just an extension of the existing signature scheme. We could do that. It just seems hacky, though. It's not easily extended to any future change.

You could take the existing script system but the sighash or instead of ECDSA signatures with a suffix that indicates what to hash, any place where a signature is expected you sign the message with that public key. And the message gets some prefix to make sure it doesn't accidentally collide with some transaction or something. Just like a prefix like "bitcoin message:" plus the message. You don't need to include the message in the signature. It's just a scriptsig and a script witness.

The reason why people want the transaction version of this is that then you can get mimblewimble whatever later.. maybe I should throw out the proof-of-funds stuff and keep the signmessage part. Are people signing an address to prove? Are they using this as a PGP replacement, or to prove funds? Sometimes they precommit to a contract before being paid, which isn't very common, but that's what it does.

In confidential transactions, they have a blinding key, and-- they do some decryption. I don't think it's related to this.

I use signmessage to sign wallet entries in my wallet. I do this for proof-of-funds to show that any entry in my wallet is something that I actually control.

This is bip322.
