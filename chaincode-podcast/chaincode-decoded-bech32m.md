---
title: 'Chaincode Decoded: Bech32m'
transcript_by: varmur via review.btctranscripts.com
media: https://podcasters.spotify.com/pod/show/chaincode/episodes/Chaincode-Decoded-Bech32m---Episode-11-ev1jnc
tags:
  - bech32
  - segwit
  - taproot
speakers:
  - Mark Erhardt
  - Adam Jonas
summary: This revisits a segment we call Chaincode Decoded. In this episode, we'll learn how to say Bech32 and also what it and Bech32m are.
episode: 11
date: 2021-04-16
additional_resources:
  - title: mailing list post
    url: https://gnusha.org/url/https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2019-November/017443.html
  - title: BIP350
    url: https://github.com/bitcoin/bips/blob/master/bip-0350.mediawiki
  - title: 'Pieter Wuille: New Address Type for SegWit Addresses (presentation)'
    url: https://www.youtube.com/watch?v=NqiN9VFE4CU
  - title: Sipa demo
    url: http://bitcoin.sipa.be/bech32/demo/demo.html
  - title: Bech32 adoption
    url: https://en.bitcoin.it/wiki/Bech32_adoption
  - title: (Some of) the math behind Bech32 addresses
    url: https://medium.com/@MeshCollider/some-of-the-math-behind-bech32-addresses-cf03c7496285
aliases:
  - /chaincode-labs/chaincode-podcast/chaincode-decoded-bech32m/
---
Adam Jonas: 00:00:00

Chaincode podcast is back, welcome to the Chaincode podcast.
I am here with Murch, and we are back.
It's been quite a layoff, but we're back in the studio and happy to be here.

Mark Erhardt: 00:00:16

Very happy.

Adam Jonas: 00:00:17

Today we are going to revisit a segment called "Chaincode decoded" where we're going to be going into Bitcoin fundamentals, and we are going to start with `bech32` and `bech32m`.
Hope you enjoy, happy to be back.

## `Bech32`

Mark Erhardt: 00:00:34

Let's talk about `bech32`.

Adam Jonas: 00:00:37

All right.
What's going on there?
Maybe we'll start with the pronunciation.
Are you sure it's "bech32"?

Mark Erhardt: 00:00:41

The inventor of the name, I think, calls it "bash32".
I've heard various other pronunciations like "beck32" or "bech32".
I don't know, "bech32".

Adam Jonas: 00:00:53

Okay, so "bech32".
Why do we need this new format?

Mark Erhardt: 00:00:57

Previously, we had addresses that were encoded in [`Base58Check`](https://en.bitcoin.it/wiki/Base58Check_encoding).
`Base58Check` uses a character set of 58 characters, and that includes mixed case.
So it's case sensitive and it's just a headache to copy these.
Have you ever tried to dictate an address on the phone or something?

Adam Jonas: 00:01:19

Unfortunately.
Just writing it down is not that fun.

Mark Erhardt: 00:01:22

Yeah, because you have to constantly look twice.
Was it an uppercase, lowercase?
We think of the letter, we don't think of a capitalized or lowercase letter.
Anyway, that was a bit of a headache.
It's nicely compact because you can encode so much information with a big character set, but the mixed case is just a huge downside.
So when SegWit got proposed, a new address standard was proposed with a 32 character set, `bech32`.
One big advantage of that, besides it having much better error detection, was that it would be single case.
So it's either allowed to be lowercase or uppercase, but mixed case is explicitly forbidden.

Adam Jonas: 00:02:08

And so it's 32, which gives you the alphabet, which is 26, plus some numbers.
So what characters are we removing?

Mark Erhardt: 00:02:17

The characters that are forbidden are zero, I think O, L probably. (Correction: characters removed from the set are 1 B I O)

Adam Jonas: 00:02:24

Okay.
We take some out because they can be confusing when you're looking at them visually.

Mark Erhardt: 00:02:28

The ones that look like other things - like "l" looking like "1" or "I", and "O" looking similar to "0" and so forth.
Anyway, it's just 32 characters, which is a multiple of two.

Adam Jonas: 00:02:43

Nice.

Mark Erhardt: 00:02:44

It also can be completely lowercase.
The standard case is just to make the addresses completely lowercase.
Uppercase is explicitly allowed, though, because, for example, when you encode addresses as QR codes, you can use a smaller instruction set to encode uppercase, and the complexity of the QR code goes down a lot, and it's easier to pick it up with a camera and stuff like that.
Especially in QR codes, you actually want to use all uppercase.

## What is the distinction between `Bech32` and native SegWit?

Adam Jonas: 00:03:19

Cool.
So we have this new format, and then what do we do with it?
What's the distinction between native SegWit and `bech32`?

Mark Erhardt: 00:03:26

A lot of people use that interchangeably.
Native SegWit describes a type of output format, whereas `bech32` describes an address encoding.
`Bech32` especially is used for native SegWit v0 outputs, which is Pay-to-Witness-Public-Key-Hash (P2WPKH) and Pay-to-Witness-Script-Hash (P2WSH).
Actually it's also used in other things, I know that Lightning invoices get encoded in `bech32`.
I think there is also a PGP alternative that encodes their pubkeys in `bech32`.
It's basically a public standard and other people have picked it up because there went a lot of work into making a format that has very nice error correction properties.

## Why does Taproot need a new address format?

Adam Jonas: 00:04:11

So why does Taproot need a new address format?

Mark Erhardt: 00:04:13

Aha, excellent question.
The [BIP-173](https://github.com/bitcoin/bips/blob/master/bip-0173.mediawiki), the definition of the `bech32` address format, specified that it should encode all addresses for SegWit v0 through SegWit v16.
You might remember that SegWit introduced versioning for the script language.
Only the script inside of the SegWit scripts gets versioned, in the witness programs.
The first one that got defined was segscript and it was version zero SegWit and it gave us four different new output types.
The wrapped SegWit types, which is a backward compatible format because the witness program gets embedded into a Pay-to-Script-Hash (P2SH) output.
So when you spend it, you first have to prove, look, I know what the original pre-image for that hash was, and now please go over there and solve that witness program.
That works for P2WPKH and for P2WSH.
So either of those can be embedded in a P2SH address, which made it great for forward compatibility, because P2SH rolled out in I think 2012, 2013, and all wallets could send to P2SH addresses, especially because a lot of big exchanges used multisig, so they wanted P2SH, and wallets could support that out of the box.

Now, the other two output types that got introduced were native SegWit outputs, in the sense that they did not have this P2SH wrapper, but they just directly had you resolve the witness program.
The problem was that a lot of wallets obviously didn't know how to deal with the new address format, because the new address standard had just been proposed even slightly after SegWit was proposed.
So in order to be able to pay to an output, you either had to just know what script to put there, or you had to be able to decode the addresses and then generate or find the script from that.
Especially just (the) decoding step that was missing until wallets had `bech32` decoders, right?
So it took a while for a lot of wallets to be able to send to native SegWit outputs.
Since that is a very painful process, in the spec it was specified that it should work out of the box for version 0 through version 16, and you should respect the version that you're given, and then just send to the address that you're given, because nobody would give you addresses that have no meaning on the network, right?
They would just be burning funds and they wouldn't have gotten paid, so they made somebody else pay into the void and that other person could prove to them, "Hey, you gave me that address, you got paid, there's your money.
You can't get it?
Well, that's your mistake, not mine, right?"
Basically it's safe to be able to spend to higher versions of SegWit, and that was the specification.

Now that Taproot became more imminent, people were actually testing whether wallets were ready to pay to Taproot address, which are native SegWit v1 addresses.
They found that not only had a lot of wallets basically curbed any versions but v0 - so they would just say, oh, address invalid, which is sort of safe, maybe a little much hand-holding, but not wrong per se - but much worse, they found that some wallets ignored the version parameter and downgraded the address to v0.
Now let's remember, SegWit is versioned, and the script has meaning within the context of the version.
When you try to send funds to a version one (v1) address and keep the script the same but then label it as a version zero (v0) address, you're actually creating something that is unspendable, you're burning funds.
So this was a very popular wallet service and they were, if given a version one address, they would burn the funds.
They would literally say, oh yeah, it looks good to me, and then create a transaction that burned the funds.

Adam Jonas: 00:09:02

Given that we're talking about wallet services, isn't that on them?
Why is that a protocol issue?

Mark Erhardt: 00:09:07

Yes, it's on them, and they didn't correctly implement the spec.
I guess that would be a valid stance to take to say, well, if you're burning your customers' funds, that's on you.
This service in particular has had a very slow response to SegWit in the first place, and who knows when they'd get around to fixing it.
Until then, there's just a very large portion of all Bitcoin transactions going through that service.
Given that a lot of other services also already had to make minor changes in order to be able to send to v1, just setting it to enabled addresses, or allowing these types of addresses, this change that we're introducing with `bech32m` on the sending side is very minor.
So basically, if you have to touch it already, if you change two lines instead of one line, you'll be fine, but better than burning out a ton of funds.

Adam Jonas: 00:10:06

And I guess the other approach would be standardness, so making anything other than v0 non-standard.

Mark Erhardt: 00:10:14

SegWit v0 addresses are only allowed to have two fixed lengths.
One of them is 42 characters, which is for P2WPKH, and one is 62 characters for P2WSH.
The way that taproot is proposed, it will also just have a 32 byte hash, so they're exactly the same length as P2WSH.
If they were using the same address format, other than the version zero and version one, there's no difference between the space that they're allowed to be in.
By downgrading to v0, they would essentially be creating a valid output type that is to be interpreted as a P2WSH output, but it cannot be resolved as such because there's no script hash that resolves to it, because taproot uses a pubkey.
That's not compatible.
People wanted to prevent that from happening on the one hand, and on the other hand, about a year or two years ago, someone discovered that `bech32` actually had a [length extension mutation weakness](https://gnusha.org/url/https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2019-November/017443.html).

## Bech32 length extension mutation weakness

Mark Erhardt: 00:11:26

You can think of `bech32` addresses as just as a huge polynomial.
The character set, the 32 characters, are just encoding numbers from 0 to 31, and each character position is the factor of one of the polynomial terms.
Now it turns out that because the checksum was using a constant of 1, when you have an address that ends on the character p, which encodes the value 1, you can insert q's or remove q's right in front of the last letter p.
Q encodes the letter zero.
Mathematically, that is equivalent to multiplying all other polynomial terms with another x.
And it turns out that that is another valid `bech32` address.

## Bech32m

Mark Erhardt: 00:12:25

What [`bech32m`](https://github.com/bitcoin/bips/blob/master/bip-0350.mediawiki) does, is it changes the constant in the checksum to something much bigger, which is not part of the 32 character values, and it gets rid of this type of error.

Adam Jonas: 00:12:41

Got it.
Very good, so that's what we're going with going forward.

Mark Erhardt: 00:12:44

Right.
Basically, the only thing you have to do is, oh, if there's a version 1 or higher here in the address now, I have to run a decoder that uses a checksum with this higher new value instead of 1.
(That's) literally the only change people that want to send to this address have to make.

Adam Jonas: 00:13:01

Great.
Any last words on maybe the implementation of `bech32m`?

Mark Erhardt: 00:13:06

You don't have to do anything to continue to be able to send to SegWit v0 outputs because the address format for them doesn't change, and it's also not prone to the length extension mutation because the addresses are limited to two specific lengths.
Now if you implement support for sending to all the new and higher versions, be sure to check that it goes through with all the test cases from the BIP.
There's test cases that make sure that all the `bech32` addresses do not properly resolve to `bech32m` decoders and vice versa, all `bech32m` addresses don't properly resolve to `bech32`.
You should be able to pass all the test cases in the BIP.
That includes being able to send to all higher versions than v1, so that when we roll out, I don't know, `SIGHASH_NOINPUT`  eventually, or other new address formats that might come up in the future, everybody will just be able to send to them and we won't have a multi-year headache where nobody knows whether it's safe to default to native SegWit addresses yet or things like that.

Adam Jonas: 00:14:22

Thanks for a great conversation, Murch.

Mark Erhardt: 00:14:18

Yeah, this one was fun.

Adam Jonas: 00:14:19

And looking forward to the next one.
I think we're going to do mempool next?

Mark Erhardt: 00:14:29

Everybody's been talking about the mempool in the past few months because it's been a bit congested.

Adam Jonas: 00:14:33

It's that bull run.
Everybody's upset about the bull run.

Mark Erhardt: 00:14:36

Price should be going down so I can buy more.

Adam Jonas: 00:14:37

We'll see you next time.
