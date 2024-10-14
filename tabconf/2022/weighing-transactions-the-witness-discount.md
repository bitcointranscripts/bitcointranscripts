---
title: Weighing Transactions, The Witness Discount
transcript_by: philmartin2525 via review.btctranscripts.com
media: https://www.youtube.com/watch?v=xmvxR0FTrVE
tags:
  - segwit
speakers:
  - Mark Erhardt
date: 2022-10-14
---
## In this talk

Mark Erhardt: 0:00:25

I'm going to try to walk with you through a transaction serialization, the Bitcoin transaction serialization.
And we'll try to understand a non-SegWit transaction and then a SegWit transaction to compare it to.
And I hope by the end of this talk, you understand how the transaction weight is calculated and how the witness discount works.
And if we get to it, we may take a look at a few different output types in the end as well.

## Transaction components before segwit

Mark Erhardt: 0:00:59

So before a SegWit activated, a transaction would look like this (refers to slide#2).
Generally, every transaction has to have at least one input and at least one output.
And so you see here, I hope you can see it, but this is a pay-to-pubkey-hash input with a 1 in the address.
And this transaction has four outputs.
One is a wrapped SegWit, one is a native SegWit legacy.
Doesn't matter too much for now.
So you've hopefully all seen this before for some of your transactions.
And now under the hood, this looks a little more detailed.

## Transaction serialization

Mark Erhardt: 0:01:42

So if you serialize or look at the serialization of a transaction, here nicely colored by [yogh.io](https://yogh.io), you can see that all of these informations are encoded in a string of hex.
And this hex is colored here by the different functions.
So I'll walk you through what we're looking at here.

### Tx serialization: "Header"

Mark Erhardt: 0:02:12

At first, we're going to look at the metadata of the transaction.
So a transaction has something that I like to call the transaction header.
It consists of the version, which is a four-byte field, the input counter, which tells you how many inputs there will be in the transaction, the output counter, which does the same for outputs, and a lock time field, which is also four bytes.
If anybody has been following the recent announcement of the v3 transactions, this is the TX version field that we're talking about, and this would be a three.
Also, as you can see, for example, here, the one is in the front, because it's little endian.
Damn, Satoshi.
So we've looked at the header.
And again, if you have any questions, just get my attention, and we'll get you a mic.

### Tx serialization: Input

Mark Erhardt: 0:03:12

Now we'll look at the inputs.
So if we spend a transaction input, the very first thing that we need to do is we have to tell the world which UTXO we're spending.
And to uniquely identify a UTXO, what we use is the so-called outpoint.
The outpoint consists of a TXID and the position in the output list of that transaction.
I just picked this transaction randomly from mempool.space last week.
So I don't know who this is or anything like that.
But this TXID in dark blue up here gives us what the parent transaction of that UTXO was.
And this light blue here, all zero, is the position in the output list.
As computer scientists, we start counting at zero.
So all zeros here, the eight zeros, are the first output or first entry in the output list.
OK, so now to spend that UTXO, we have to satisfy the condition script that was encoded in that UTXO.
And we do that with an input script.
So first, because input scripts can have a variable length, depending on what sort of condition script we're trying to satisfy, we have to tell how long the script is.
This is this red field here, "6a".
I'm not going to calculate in my head right now what that is.
I think 106, but yeah.
And then the light blue here is the input script.
So in this case, for a pay-to-pubkey-hash input, anybody got guesses what that contains?
So first, to satisfy a pay-to-pubkey-hash, the funds are locked to the hash of a public key.
So we have to show the public key, then hash it, and show that it matches what was stored in the output.
And then after that, provide a signature that matches the public key.
So all of that is in this light blue stuff.
And then finally, the last field of the input is the sequence.
Does anybody know what we use sequences for?
For example, we can indicate that a transaction is replaceable if any one input on a transaction is lower than the maximum value.
This is the maximum value.
The transaction is non-final and can be replaced.
And that's a BIP 125 RBF, right?
You only need to specify it on one input.
That is sufficient to make the whole transaction non-final.
What happens if this field is lower than maximum minus 1?
Then we're dealing with lock times.
All right, I don't want to dwell too much on that, because otherwise we'll not get to other stuff.
Let's look at the outputs next.

### Tx serialization: Outputs

Mark Erhardt: 0:06:26

Here, we had the output counter from the header before.
We have four outputs on a transaction.
And I've highlighted one of them.
There's three more underneath.
But the first thing that we have in the output is this yellow field, which I've titled "amount".
This is the number of satoshis that we're signing over to this condition script that we're locking up funds to.
So an output creates a new UTXO.
A UTXO has a certain number of satoshis that are allocated to it.
And then it has a locking script, or output script, or condition script that codifies the conditions under which this can be spent.
The largest amount we can put into a transaction, the amount field is eight bytes.
And I believe that is sufficient to store more than 21 million Bitcoin.
Some people might know already, but we never use floats, or doubles, or any sort of behind comma numbers in all of protocol development.
The native unit in all of the protocol is satoshis.
So we have here an integer amount of satoshis that we're assigning to an output.
We do not have a number of Bitcoins or anything like that, because floats are bad.
Floats make rounding errors and things like that.
We don't want that in protocol development where people need to come to the same result, right?
So we have an eight byte field to encode the amount.
It's also little endian, as you can see, because this would be a shit ton of Bitcoin otherwise.
And then we have an output script here.
And the output script is "17" long.
That is 23.
Does anybody know what that is (referring to slide)?
Well, we can look it up, right?
So that was a pay-to-script hash script, right?
So, the hash in pay-to-script hash is 20 bytes.
It's a hash 160.
And, well, I'll get to that later.
I have a slide on all the different scripts for all the output types if we get there.
So what you see here is an amount, the length of the output script.
The output script encodes the rules under which the money can be spent.
And then three more times because there's four outputs on this transaction.

## Terminology: native segwit

Mark Erhardt: 0:09:23

I've been told that I should really clarify what native segwit is.
And I guess this slide is a little raw because I made it 10 minutes ago.
A lot of people refer to the first type of native segwit outputs just as native segwit.
You might be familiar with pay-to-witness-public-key-hash or pay-to-witness-script-hash.
It's the addresses that start with "BC1Q".
And those are native segwit V0, the first or the zeroth version of native segwit outputs.
And recently we had a soft fork in November, well, not quite that recently, almost a year ago, which introduced another new output type called pay-to-taproot.
And pay-to-taproot is also a native segwit output.
And it's the native segwit V1 output.
And these addresses start with "BC1P" because "Q" encodes zero in bash 32 and "P" encodes one in bash 32.
So, all of the native segwit outputs encode a witness program after a version in the output.
So if I talk about native segwit output, this applies to all of these, but my example will be a pay-to-taproot transaction, just to clarify.
Any questions on that so far?
All right, cool, yeah?

Audience member 1: 0:10:53

What's the difference between the ones you've written and the ones that you've talked about, wrapped segwit?
That's like two different outputs, right?

Mark Erhardt: 0:11:02

Yeah, so wrapped segwit is a little bit of a hybrid because wrapped segwit was made to be backward compatible by satisfying the rules of pay-to-script-hash.
But the witness part is all the same as with native segwit.
So, in the witness section for a wrapped segwit output, you'll have exactly the same witness stack as in native segwit.
But we'll get a little more to that.
So, the big difference between wrapped and native segwit is that you have a forwarding script in the input script that says, hey, look at the witness.
That's where we actually provide the data to satisfy the spending conditions.
Did that explain your question or satisfy your question?

Audience Member 1: 0:11:51

Yeah, it makes it easier to start over than native segwit.

Mark Erhardt: 0:12:01

Yeah, nested is different.
And we're also not doing nested segwit outputs for pay-to-taproot where that was only a v0 thing.
Now that people hopefully can build native segwit outputs and we will leave that behind us, hopefully.

## First Taproot transaction: native segwit v1

Mark Erhardt: 0:12:16

All right, let's look at our second transaction.
So, I brought to you the very first pay-to-taproot transaction that was ever spent on the blockchain.
You will recognize here that Bitbug42 left us an op return message.
"I like schnorsex and cannot lie."
And I hope, I'm not sure if you can read this, but this is a bc1p address, which indicates that we're spending a pay-to-taproot output and it's also sending the change to a taproot output here.

### Native segwit transaction

Mark Erhardt: 0:12:47

So, let's look at the serialization of that.
Looks very much like our previous example, except that we have a lot more orange in here.
And all the orange here is the witness bytes and we will look at them a little more in detail.
And you will see that there's also a few other differences.
For example, the input script length here is now zero.
And that is because we no longer have an input script on native segwit inputs.
Instead, we provide the data to satisfy the spending conditions in the witness.
So, all the native segwit outputs, you can always recognize a native segwit input on having an input script length of zero.

### Native segwit transaction: Witness data

Mark Erhardt: 0:13:36

All right, let's look at the witness data.
Who remembers what we should have directly after diversion here usually in a non-segwit transaction?
The number of inputs.
So, in the very first sentences I said, a transaction must always have one input at least and one output at least.
So, if a non-segwit node, a node that is not familiar with the segwit format, gets a transaction that has a zero here, what do you think will he do with that transaction?
Well, that's invalid.
He drops it and bans his peer for giving him this bullshit, right?
So, what we put here with the marker and the flag is that, is a, hey, this is a new format and old people shouldn't, like old nodes shouldn't even read this.
You got this by accident.
Don't parse this.
And then the flag indicates this transaction has a witness section.
The witness section is inserted after the outputs before the lock time.
I saw a question there.

Audience Member 2: 0:14:51

What exactly do you mean when you say invalid?
Is it like, there's like a standard, standard is the physical functionality and a non-standard is versus the physical valid?

Mark Erhardt: 0:15:06

Right, okay, so the question is whether I mean that this transaction appears actually to be invalid for old nodes.
And yes, this representation of that transaction appears invalid because non-segwit nodes, of which there are basically none on the network anymore because the last client that was non-segwit was, I think, 0.12 and that is 10 versions ago, so about five years ago.
And the life cycle is like, we maintain them for two years.
So this is mostly hypothetical and to explain how that worked back then, not an active problem anymore.
But to make, well, actually, can I take your question like two slides, because I'm gonna get to that.

Audience Member 2: 0:15:55

But right now, you're saying invalid, you really mean invalid?

Mrk Erhardt: 0:15:58

Yes, I do mean invalid.
If we give this representation of the transaction to a non-segwit node, they will think that it's crap.

Paul Sztorc: 0:16:14

I was gonna maybe try to say that it happens to be the case with segwit, it's very bizarre that very unique situation where, as I understand it, the old segwit nodes, if they talk, if a segwit node talks to a non-segwit node, it will construct a completely different like transaction vector and a completely different block and everything, and it will not have any of this invalid type of thing.
So there's a one-to-one correspondence, there's an isomorphous correspondence between this transaction and a different transaction that is valid and is a non-segwit.
So the non-valid thing is very confusing, is, you know, I can understand anyone would be confused by that, because it's very confusing.

Mark Erhardt: 0:16:52

I'm gonna get more into the details of that and hopefully make it clear by then.
And there is a different representation of the transaction that the non-segwit node will be able to parse and will make them achieve the same UTXO set in the long run.
They do not get the witness data because they don't understand the witness data.
So basically, we're talking a protocol that, or speaking a protocol that they don't understand, and to protect them from getting that, we made it in a way that they will not accept it.
All right, so I talked a little bit about marker and flag, which indicate A, this is a segwit transaction, B, this transaction has a witness section.
And now, why don't we have a count of witness stacks?
Well, because every input has to have a witness stack in a segwit transaction.
So by having the input counter, we know how many witness stacks there will be.
In this transaction, we had only a single input.
So we have a single witness stack to satisfy the input.
And the first thing that we have is a number of witness items.
And then the length of, in this case, the first witness item and only witness item, which is "40", which is 64.
And this makes that a signature.
And yes, in a pay-to-taproot key path spend, we only have a signature in the witness stack.
All right, so this is our first pay-to-taproot input ever.

## Segwit

Mark Erhardt: 0:18:25

And how does that affect us?
Well, before segwit, we had a block size limit of one megabyte.
We just counted the raw bytes of all the data in a block, and that had to be smaller than one million, or up to one million, and otherwise the block was invalid.
With segwit, we introduced a new limit for block space.
We introduced a weight limit.
And the weight limit is four million weight units.
And since we only give the non-witness data to old nodes, they only see this green part up here, which is always smaller than one megabyte.
But for people, or nodes, I should say, that speak segwit, we also give them the witness data.
So we can exceed the one megabyte now.
And recently in August, we actually had a new biggest block, which was 2.77 megabytes.

### What a segwit node sees

Mark Erhardt: 0:19:22

So how does that work?
What a segwit node sees is the complete transaction.
And I want to clarify at this point, often there was this misunderstanding that the witness is not part of the transaction, or the witness is not part of the block, or things like that.
You can see how this orange part down here is very much part of the transaction, and before the lock time.
And this is the full segwit transaction.
This is what nodes exchange on the network, gossip about, and use to verify that everybody followed all the rules.

### What a non-segwit node sees: Stripped Transaction

Mark Erhardt: 0:19:58

And for the nodes that don't understand segwit, what we gave them is the transaction without the witness data.
And that should look very familiar, right?
There's the version, there's the input counter, we have the outpoint telling it what UTXO is being spent, so that they can delete it from their UTXO set.
We have an input script, which happens to be of length zero, and then a sequence.
And then we have two outputs with amounts and output scripts, right?
And finally, a lock time.
So all of the parts are exactly the same as before segwit for non-segwit nodes.
But they have a reduced security model because they can't actually validate the signature, right?
They don't see the signature at all.
And we strip out the witness marker and the witness section, and just hand them the stripped transaction.
And this is a smaller than the full transaction, which makes us still stick to the one megabyte block limit that the old nodes were enforcing and are enforcing.
And also, it has this reduced security because they don't actually get the inputs for the condition script to show that somebody actually signed for this.

Audience: 0:21:23

How do we have the same TXID between non-segwit node and segwit nodes?

Mark Erhardt: 0:21:29

Well, segwit introduced another change, which was that we calculate the TXID for segwit transactions only from the stripped transaction.
So we use this as the input to calculate the TXID, which is just the hash of the transaction data.
And this is also, by the way, what allows us to do things like Lightning.
Because in Lightning, we need to build a refund transaction that spends the output here before it is signed, right?
You don't want to give the channel partner the funding transaction that is fully signed because then they could just make sure that the money goes there already.
We want to show them the unsigned transaction, but we still need to agree on the TXID so that they can sign the refund transaction to us first before we send the funding transaction and put money at risk, right?
So in segwit transactions, we calculate the TXID from the stripped size.
And non-segwit nodes and segwit nodes, therefore, always have the same TXIDs for the same transactions, even though they have different representations and non-segwit nodes only see part of it.

Audience: 0:22:42

Is there any other ID?

Mark Erhardt: 0:22:45

Yes, there's also a witness TXID.
So in order to commit to the full transaction that segwit nodes see, we do have to have an identifier or a commitment to the full complete transaction, right?
If we were only committed to the stripped transaction, then somebody could take out the signature, put it in their block, and it would look the same, but would be invalid, and make a block invalid without changing the Merkle root, right?
So actually, we use the stripped transaction to take the TXID.
That's what we commit to in the Merkle root of the block.
That's what we can build a child transaction on top of.
That's what makes transaction malleability go away, if you've been around and heard about that.
But then for the segwit nodes, to make sure that they actually have the complete transaction, we have also a witness commitment in the coinbase, which commits to all the witness TXID, and the witness TXIDs are built from the complete transaction.

Audience Member 3: 0:24:06

If you got a transaction with multiple inputs, is there something in the witness data that delineates where that witness for one finishes and the next one starts?

Mark Erhardt: 0:24:15

That's an excellent question, and I should have really used a transaction with two inputs, but no, there is not.
And how does that work?
Well, we have an input counter up here already that tells us how many witness stacks there will be, because every input has to have a witness stack.
If you have a legacy input and a pay-to-taproot input, for example, the legacy input will have a witness stack of length zero.
It'll just say, hey, here's my witness stack.
I have zero witness items.
Thanks, man.
And then the second witness stack will have the pay-to-taproot witness stuff.
Let's say if we had a pay-to-public-key-hash input, a legacy input here before, this one would be two, and we would just expect two witness stacks.
The first one would say zero here, and then we'd know, okay, we've completely parsed that witness stack because it's just length zero, zero items.
And then we'd get to the second one, and it tells us again how many witness items to be, then tells us the length of each witness item, gives us the witness item data.
So we don't really have to tell how many witness items, or sorry, witness stacks there will be.
Okay, so we've talked about what a segwit node sees, what a non-segwit node sees.

### Transaction WEIGHT

Mark Erhardt: 0:25:37

So where is that mystical transaction weight coming in from?
Well, we take four times the non-segwit data, and one times the witness data, and add that up, and that is the transaction weight.
So we know now how we get the stripped transaction, right?
Just remove all the witness data, and we count each byte of the non-witness data four times, and then the witness data is counted once.

Audience: 0:26:11

Why these two coefficients?

Mark Erhardt: 0:26:17

They were basically arbitrarily picked because they felt good.

So what happens if we have a transaction that does not have any witness data?
We have only non-witness data, we count that four times, and we have a limit of four million weight units now, and before that we had one million bytes.
So if we count all the non-witness data four times, that is the same size, right?
We multiply it by four, and the limit is four times higher.
So for non-segwit transactions, this continues to be backwards compatible and completely correct for old nodes.

What happens when we have witness data?
Well, old nodes don't see the witness data, and this is strictly less than, the proportion of the block weight, the four million weight units, is bigger than the non-witness data of one million bytes.
So whenever we have any segwit transactions, they will always fit into the strip block, and the strip block will always be less than one megabyte.
And that's how old nodes that don't understand segwit could follow along and still arrive at the same UTXO set because they knew which UTXOs to remove from the set and to create, and would always get a valid block because there was a block that was spending stuff, was creating new outputs, had the same TXIDs, and was backwards compatible.

## Q&A

If there's more questions, let's do questions first.
Otherwise, I'll have a look at this table.

Audience Member 4: 0:28:23

I don't know, maybe that is too detailed now, but I heard now the last days there is a proposal to remove the witness discount.
I think I even heard it from you on an evening dinner.
So maybe you could elaborate a bit.
I think that is interesting for others as well.
What is the motivation behind that?
Thanks.

Mark Erhardt: 0:28:40

So there is, there were some people speculating on whether or not removing the witness discount in the long term would be able to be soft forked in.
And the argument that they made was that if you always count all the witness data at the same cost as non-witness data, so if here was also a 4X, that's strictly smaller than the current, it would use less of the available block space than the current rules, so we could soft fork that in.
And what that would do is, if we had a cross-input signature aggregation, aka when we can have transactions where we have multiple inputs but only one signature, then that would make it more attractive to use aggregation because it would remove more cost from the transaction.
And it would also decrease the block space, the available block space, which some people find good because we apparently have too much block space already.
I do not subscribe to that hypothetical scenario.
Maybe when we do a cross-input signature aggregation proposal, that would actually be attractive to economically incentivize adoption, but I think it's pretty speculative and far out there still.

Audience Member 5: 0:30:13

The legacy signatures are not discounted, right?

Mark Erhardt: 0:30:17

Legacy signatures are counted as non-witness data.
They're in the input script.
Let's remind ourselves, just a sec, here.
So a non-SegWit transaction has to provide the witness data, so to speak, the script arguments to satisfy the condition script are provided in the input script.
So this is a pay-to-public-key hash input, and what it does is it provides a pubkey and a signature, and then with the output script, the output script duplicates the pubkey, hashes it, checks that that matches the hash that was in the previous output, and then checks whether the signature fits the pubkey.
And the pubkey and signature are in the input script here, so they're non-witness data and counted for X.

Audience Member 6: 0:31:27

Why are you not discussing the most important feature of the witness discount, which is that it produces many bad incentives, certain transactions are larger and consume more bytes, and yet they are undercharged on fees, and yet there's a rampant misconception.
When I saw the title of your talk, I thought you were gonna talk about the rampant misconception that these transactions are somehow smaller or more efficiently encoded when the reverse is the truth.
Most important thing that you were supposed to say in this whole talk, and I've been waiting patiently for you to get to that slide.

Mark Erhardt: 0:32:01

Fine, I'll go to the next slide, which I have right here.
Segwit is a block size increase in that it allows to have more data in the block.
But it doesn't really make transactions smaller, at least not for wrapped segwit.
So in this table, what you see is pay-to-pubkey-hash, which is just legacy single sig, pay-to-script-hash, pay to witness public key hash, which is wrapped segwit single sig, native segwit single sig, and pay-to-taproot.
For the transaction header, those are the same, except for the lower three, since they require segwit transactions, we need to have the marker and the flag, right?
We talked about that.
And output-wise, this is all non-witness data, right?
The outputs are never discounted, only script arguments are discounted in the witness section.
So you will see, for example, that pay-to-taproot has the biggest output of those four types, right?
On the input, however, with the forwarding script that you need to wrap the pay-to-script-hash, pay to witness public key hash input, basically, in the input script, you just have a redirect that says, hey, I look like a pay-to-script-hash output, but really, you want to look at the witness section.
And that costs us an actual 24-bytes increase.
So in the raw byte length, actually, the pay-to-pubkey-hash input is, or a transaction with two inputs and two outputs of pay-to-pubkey-hash, which is the legacy type, is basically the same size as a native segwit v0 single sig input.
They are not significantly smaller.
But in the amount of block space that they consume due to the discount, the native segwit is 68 vbytes, where the pay-to-pubkey-hash input is 148.
So it's almost twice as big, right?
Pay-to-taproot is actually, though, the smallest byte size out of these.
Altogether, it's only 312, so it's a solid 20% smaller than native segwit and pay-to-pubkey-hash.
So I agree in parts.
For the older segwit types, they are not a bandwidth improvement.
Pay-to-taproot is actually smaller.
All right, I think that's all the time I got, and thank you for coming to my talk.
Thank you.
