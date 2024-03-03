---
title: "Chaincode Decoded: Bech32m"
transcript_by: kouloumos via tstbtc v1.0.0 --needs-review
media: https://podcasters.spotify.com/pod/show/chaincode/episodes/Chaincode-Decoded-Bech32m---Episode-11-ev1jnc
tags: ['bech32', 'segwit', 'taproot']
speakers: ['Mark Erhardt']
categories: ['podcast']
summary: "This revisits a segment we call Chaincode Decoded. In this episode, we'll learn how to say Bech32 and also what it and Bech32m are. Enjoy!"
episode: 11
date: 2021-04-16
additional_resources:
-   title: mailing list post
    url: https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2019-November/017443.html
-   title: BIP350
    url: https://github.com/bitcoin/bips/blob/master/bip-0350.mediawiki
-   title: 'Pieter Wuille: New Address Type for SegWit Addresses (presentation)'
    url: https://www.youtube.com/watch?v=NqiN9VFE4CU
-   title: Sipa demo
    url: http://bitcoin.sipa.be/bech32/demo/demo.html
-   title: Bech32 adoption
    url: https://en.bitcoin.it/wiki/Bech32_adoption
-   title: (Some of) the math behind Bech32 addresses
    url: https://medium.com/@MeshCollider/some-of-the-math-behind-bech32-addresses-cf03c7496285
---
Speaker 0: 00:00:00

Chaincode podcast is back.
Welcome back to the Chaincode podcast.
I am here with Merch.
Hey there.
And we are back.
It's been quite a layoff, but we're back in the studio and happy to be here.

Speaker 1: 00:00:16

Very happy.

Speaker 0: 00:00:17

So today we are going to revisit a segment called Chinko decoded where we're going to be going into Bitcoin fundamentals.
And we are going to start with batch 32 and batch 32 M.
Hope you enjoy.
Happy to be back.
Let's talk about batch 32.
All right.
What's going on there?
Maybe we'll start with the pronunciation.
Are you sure it's batch 32?

Speaker 1: 00:00:41

The inventor of the name, I think, calls it bash 32.
I've heard various other pronunciations like Beck 32 or Bech 32.
I don't know, Bech 32.

Speaker 0: 00:00:53

Okay.
So Bech 32.
Why do we need this new format?

Speaker 1: 00:00:57

Previously, we had addresses that were encoded in base 58 check.
Base 58 check uses a character set of 58 characters, and that includes mixed case.
So it's case sensitive and it's just a headache to copy these.
Have you ever tried to dictate an address on the phone or something?

Speaker 0: 00:01:19

Unfortunately, just writing it down is not that fun.

Speaker 1: 00:01:22

Because you have to constantly look twice.
Was it an uppercase, lowercase?
We think of the letter.
We don't think of a capitalized or lowercase letter.
Anyway, that was a bit of a headache.
It's nicely compact because you can encode so much information with a big character set, but the mixed case is just a huge downside.
So when SegWit got proposed, A new address standard was proposed with a 32 character set, bash32.
And one big advantage of that, besides it having much better error detection, was that it would be single case.
So it's either allowed to be lowercase or uppercase, but mixed case is explicitly forbidden.

Speaker 0: 00:02:08

And so it's 32, which gives you the alphabet, which is 26, plus some numbers.
So What characters are we removing?

## Correction: The characters removed from the set are 1 B I O

Speaker 1: 00:02:17

The characters that are forbidden are zero, I think O, L probably.

Speaker 0: 00:02:24

Okay.
We take some out because they can be confusing when you're looking at them visually.

Speaker 1: 00:02:28

The ones that look like other things like L looking like one or I and O looking similar to zero and so forth.
Anyway, it's just 32 characters, which is a multiple of two.
Nice.
It also can be completely lowercase.
The standard case is actually just to make the addresses completely lowercase.
Uppercase is explicitly allowed, though, because, for example, when you encode addresses as QR codes, you can use a smaller instruction set to encode uppercase, and it makes the QR codes just look like the complexity of the QR code goes down a lot and it's easier to pick it up with a camera and stuff like that.
Especially in QR codes, you actually want to use all uppercase.

Speaker 0: 00:03:19

Cool.

## What is the distinction between Bech32 and native SegWit?

Speaker 0: 00:03:19

So we have this new format.
And then what do we do with it?
What's the distinction between native segwit and batch 32?

Speaker 1: 00:03:26

A lot of people use that interchangeably.
So native segwit describes a type of output formats, whereas bash 32 describes an address encoding.
And bash 32 especially is used for native segwit v0 outputs, which is pay to witness public key hash and pay to witness script hash.
And actually it's also used in other things.
I know that Lightning invoices get encoded in Bash 32.
I think there is also a PGP alternative that encodes their pub keys in bash 32.
But it's basically a public standard and other people have picked it up because they went a lot of work into making a format that has very nice error correction properties.

Speaker 0: 00:04:11

So why does Taproot need a new address format?

## Why does Taproot need a new address format?

Speaker 1: 00:04:13

Aha, excellent question.
The BIP-173, the definition of the bash32 address format specified that it should encode all addresses for segwit v0 through segwit v16.
You might remember that SegWit introduced versioning for the script language.
And only the script inside of the SegWit scripts gets versioned in the, in the witness programs.
So the first one that got defined was segscript and it was version zero segwit and it gave us basically four different new address types.
Or I should say output types.
If we're, if we're correct here.
The wrapped segwit types, which is a backward compatible format because the witness program gets embedded into a pay to script hash output.
So when you spend it, you first have to prove, look, I know what the original pre-image for that hash was.
And now please go over there and solve that witness program.
And that works for pay-to-witness public key hash and for pay-to-witness script hash.
So either of those can be embedded in a pay-to-script hash address, which made it great for forward compatibility because basically, Pay2ScriptHash rolled out in I think 2012, 2013, and all wallets could send to Pay2ScriptHash addresses, especially because a lot of big exchanges used multisig, so they wanted pay-to-script hash, and wallets could support that out of the box.
Now, the other two output types that got introduced were native segwit outputs, in the sense that they did not have this pay to script hash wrapper, but they actually just directly had you resolve the witness program.
The problem was that a lot of wallets obviously didn't know how to deal with the new address format because the new address standard had just been proposed even slightly after segwit was proposed.
So in order to be able to pay to an output, you either had to just know what script to put there, or you had to be able to decode the addresses and then generate or find the script from that.
And especially just decoding step that was missing until wallets had batch 32 decoders, right?
So it took a while for a lot of wallets to be able to send to native segwit outputs.
And since that is a very painful process, it was in the spec, well, specified that it should work out of the box for version 0 through version 16, and you should respect the version that you're given, and then just send to the address that you're given, because nobody would give you addresses that have no meaning on the network, right?
They would just be burning funds and they wouldn't have gotten paid.
So they made somebody else pay into the void and that other person could prove to them, hey, you gave me that address, You got paid, there's your money.
You can't get it?
Well, that's your mistake, not mine, right?
So basically, it's safe to be able to spend to higher versions of SegWit.
And that was the specification.
But Now that Taproot became more imminent, people were actually testing whether wallets were ready to pay to Taproot address, which are native SegWit v1 addresses.
And they found that not only had a lot of wallets basically curbed any versions, but v0.
So they would just say, oh, address invalid, which is sort of safe, maybe a little much hand-holding, but not wrong per se.
But Much worse, they found that some wallets ignored the version parameter and downgraded the address to v0.
So now let's remember, SegWit is versioned and the script has meaning within the context of the version.
And now when you try to send funds to a version one address and keep the script the same but then label it as a version zero address, you're actually creating something that is unspendable, you're burning funds.
So this was a very popular wallet service and they were basically, if given a version one address, they would burn the funds.
They would literally say, oh yeah, it looks good to me, and then create a transaction that burned the funds.

Speaker 0: 00:09:02

Given that we're talking about wallet services, isn't that on them?
Like, why is that a protocol issue?

Speaker 1: 00:09:07

Yes, it's on them.
And they basically didn't correctly implement the spec.
I guess that would be a valid stance to take to just say, well, if you're burning your customers' funds, that's on you.
But the service in particular has had a very slow response to SegWit in the first place.
And who knows when they'd get around to fixing it.
Until then, there's just a very large portion of all Bitcoin transactions going through that service.
And given that a lot of other services also already had to make minor changes in order to be able to send to v1, just setting it to enabled addresses or allowing these types of addresses.
This change that we're introducing with batch 32m on the sending side is very minor.
So basically, if you have to touch it already, if you change two lines instead of one line, you'll be fine.
But better than burning out a ton of funds.

Speaker 0: 00:10:06

And I guess the other approach would be standardness.
So making these anything other than v0 non-standard.

Speaker 1: 00:10:14

Segment v0 addresses are actually only allowed to have two fixed lengths.
One of them is 42 characters, which is for pay-to-witness public key hash, and one is 62 characters for pay-to-witness script hash.
The way that taproot is proposed, it will also basically just have a 32 byte hash.
So they're exactly the same length as pay to witness script hash.
There's no way if they were using the same address format, other than the version zero and version one, there's no difference between the space that they're allowed to be in.
By downgrading to v0, they would essentially be creating a valid output type that is to be interpreted as a pay-to-witness script hash output, but it cannot be resolved as such because there's no script hash that resolves to it because taproot uses a pubkey.
That's not compatible.
People wanted to prevent that from happening on the one hand, And on the other hand, about a year or I think two years by now ago, someone discovered that Bash 32 actually had a length extension mutation weakness.

## Bech32 length extension mutation weakness

Speaker 1: 00:11:26

You can think of Bash 32 addresses basically just as a huge polynomial.
The character set, the 32 characters, are just encoding numbers from 0 to 31, and each character position is the factor of one of the polynomial terms.
And now it turns out that because the checksum was using a constant of 1, when you have an address that ends on the character p, which encodes the value 1, you can insert q's or remove q's right in front of the last letter P.
And the Q encodes the letter zero.
Mathematically, that is equivalent to just multiplying all other polynomial terms with another x.
And it turns out that that is another valid bash 32 address.

## Bech32m

Speaker 1: 00:12:25

So what bash 32m does is it changes the constant in the checksum to something much bigger, which is not part of the 32 character values, and it gets rid of this type of error.
Got it.
Very good.
That's what we're going with going forward.
Right.
Basically, The literally only thing you have to do is, oh, if there's a version 1 or higher here in the address now, I have to run a decoder that uses a checksum with this higher new value instead of 1.
Literally, the only change people that want to send to this address have to make.

Speaker 0: 00:13:01

Great.
Any last words on maybe the implementation of Bec32M?

Speaker 1: 00:13:06

You don't have to do anything to continue to be able to send to segwitv0 outputs because the address format for them doesn't change.
And it's also not really prone to the length extension mutation because the addresses are limited to these two specific lengths.
And now if you implement support for sending to all the new and higher versions, be sure to check that it goes through with all the test cases from the BIP.
There's test cases that make sure that all the bash 32 addresses do not properly resolve to bash 32M decoders and vice versa, all Bash 32M addresses don't properly resolve to Bash 32.
You should be able to pass all the test cases in the bib.
That includes being able to send to all higher versions than one, so that when we roll out, I don't know, SIGHASH no input eventually, or other new address formats that might come up in the future, everybody will just be able to send to them and we won't have a multi-year headache where Nobody knows whether it's safe to default to native segwit addresses yet or things like that.

Speaker 0: 00:14:22

Thanks for a great conversation, Murch.
Yeah, this one was fun.
And looking forward to the next one.
I think we're going to do mempool next.

Speaker 1: 00:14:29

Everybody's been talking about the mempool in the past few months because it's been a bit congested.

Speaker 0: 00:14:33

It's that bull run.
Yeah.
Everybody's upset about the bull run.

Speaker 1: 00:14:36

Price should be going down so I can buy more.
We'll see you next time.
