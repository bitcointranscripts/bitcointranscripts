---
title: SIGHASH_NOINPUT (BIP118)
transcript_by: Bryan Bishop
tags:
  - bitcoin-core
speakers:
  - Bryan Bishop
media: https://www.youtube.com/watch?v=nNKP6lxo1RA
date: 2018-10-04
aliases:
  - /scalingbitcoin/tokyo-2018/edgedevplusplus/sighash-noinput
---
SIGHASH\_NOINPUT (BIP118)

<https://twitter.com/kanzure/status/1049510702384173057>

Hi, my name is Bryan, I'm going to be talking about SIGHASH NOINPUT. It was something that I was asked to speak about. It is currently not deployed, but it is an active proposal.

So, just really brief about who I am.  I have a software development background. I just left LedgerX last week, so that is an exciting change in my life.  Also, I contribute to bitcoin core, usually as code review.

In order to talk about what the SIGHASH\_NOINPUT proposal is, I'm going to talk about SIGHASH flags.  To talk about SIGHASH flags, this goes back to how a transaction is structured.  The data structure for a bitcoin transaction. In script sigs where you have a signature for proving that you have authorization to spend a coin these signatures are constructed in a certain way and there is a single byte appended to a signature that specifies in what way the transaction was signed. So there is a few SIGHASH flags that are implemented and have been deployed since the beginning. The most common one that I use is SIGHASH\_ALL, that means sign everything except for the scriptsigs.  There are some others as well like, SIGHASH\_ANYONECANPAY, where you only sign a current input and everything else in the transaction is not considered part of the signature, it is not covered under the commitment.

So, there have been many proposed improvements for these SIGHASH types where you say well maybe you only want to sign certain aspects of the transaction, and you could say, I'm interested in spending these coins under these conditions, but I'm also not interested in these other details which we are going to ignore. And so many different SIGHASH flags have been proposed for how to do this including SIGHASH\_NOINPUT, but also others such as. Basically imagine masking out different parts of the transaction.  So any part of the data in the transaction that you can imagine there has been a proposal for a SIGHASH flag for either considering it super important or completely irrelevant in that you are fine with any sort of alternatives being proposed on the network without causing your signature to become invalid.

So specifically SIGHASH\_NOINPUT, the way that this works, the idea is that you don't actually care what specific input is being provided, you don't care what the transaction id is that provides the input into the transaction, however you do care about the amount. Very early on in 2015 this was actually proposed as a malleability fix before SegWit was proposed as a malleability fix, the problem was that SIGHASH\_NOINPUT was actually somewhat dangerous, especially in the context of a malleability fix. So it was not selected by the community, and then we got SegWit.

There is a proposal, [bip118](https://github.com/bitcoin/bips/blob/master/bip-0118.mediawiki), written by Christian Decker.

Alright well this is a bunch of text, about something called application specific pubkeys, which is basically the malleability fix because it is actually quite dangerous. And this is because any input can be swapped into the transaction as long as it has a valid signature and the signature with SIGHASH\_NOINPUT says you do not actually care about which input it is as long as the amount is correct.

Specifically, SIGHASH\_NOINPUT has received attention because the lightning developers would like to use it for something called watchtowers.  And I believe there is either a lightning talk today or tomorrow and that will make more sense, essentially you want to be able to broadcast certain transactions to enforce the rules of the lightning protocol.  I already mentioned the malleability fix. There is also another lightning network proposal called eltoo which is very confusing because the name is ambiguous and refers to layer 2 or "L2" but it's not spelled that way.  I think it was supposed to be a pun but it is really just confusing.

So, there were two other SIGHASH\_NOINPUT proposals. One was for an opcode, and there was also one from I think Johnson Lau for either script v2 or SIGHASH v2, I think that is possibly using a bit mask approach, at the very least a bitmask sighash type was implemented for Elements project.  And that is the overview of SIGHASH\_NOINPUT. I will be back later for other talks.
