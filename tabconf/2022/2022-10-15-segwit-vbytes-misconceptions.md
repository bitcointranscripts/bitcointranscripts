---
title: 'Weighing transactions: The witness discount'
transcript_by: Bryan Bishop
tags:
  - segwit
  - fee-management
speakers:
  - Mark Erhardt
date: 2022-10-15
---
You've already heard from someone that this presentation will be more interactive. I probably won't get through all of my material. If you have questions during the talk, please feel free to raise your hand and we can cover it right away. I'm going to try to walk you through a transaction serialization for both a non-segwit transaction and a segwit transaction. By the end of the talk, I hope you understand how the transaction weight is calculated and how the witness discount works. At the end, we might look at a few different output types at the end.

## Before segwit

Before segwit activated, a transaction would look like this: it would have at least one input and one output. This here is a p2pkh input and this transaction has 4 outputs, one is a wrapped segwit, one is a legacy output, it doesn't matter too much for now. Hopefully you have seen this kind of transaction before.

## Transaction serialization

Under the hood, this looks a little more detailed. If you serialize or look at the serialization of a transaction, as colored by yogh.io, you can see that all of this data is encoded into a hex string and this hex string is covered here by the different functions.

We will first look at the metadata of the transaction. A transaction has a "transaction header" which consists of a 4-byte version field, the input counter which tells you how many inputs there will be in a transaction, the output counter which does the same for outputs, and a 4-byte locktime field.

If anybody has been following the recent announcement of v3 transactions, this is the transaction version field here. As we can see here, the 1 is at the front because the value is little-endian not big-endian.

After looking at the transaction header, we will look at the inputs.

## Input serialization

If we spend a transaction input, the very first thing we have to do is tell the world which UTXO we are spending. To uniquely identify a UTXO, we use an outpoint which is a txid and the position in the output list of that transaction. This txid is in dark blue on my slide. This is the parent transaction of that UTXO. As computer scientists, we start counting at 0.

To spend that UTXO, we have to satisfy the condition script that was encoded in that UTXO. We do that with an input script. "Input script" can have a variable length depending on what kind of condition script we're trying to satisfy, so therefore we have to encode into the input area the length of the input script and this is called the input script length.

After that value, you insert the input script. For a p2pkh input, it's a well-known script. To satisfy a p2pkh script, the funds are locked to the hash of a public key. We have to show the public key, then hash it and show that it matches what was stored in the output and after that provide a signature that matches the public key.

The last field of the input is the "sequence". Using this we can indicate that the transaction is replaceable. If any one input on the transaction is lower than the maximum value, then the transaction is non-final and can be replaced. You only need to specify it on one input. That's sufficient to make a transaction non-final. What happens if this field is lower than maximum value minus 1? Then we're dealing with locktimes. I won't dwell too much on that.

## Output serialization

In this example transaction, we have four outputs. I have highlighted one of them. The first thing we have in the output is the "amount" which is the number of satoshis that we're signing over to this condition script that we're locking funds to. An output creates a new UTXO and a UTXO has a certain number of sats allocated to it. Then it has a locking script or condition script that codifies the conditions under which these sats can be spent.

Q: What is the largest amount you can do in a transaction?

A: The amount field is 8 bytes and I believe that is sufficient to store more than 21 million bitcoin.

Q: Why integers?

A: Some people might know already, but we never use floats or doubles in protocol development. The native unit in the bitcoin protocol is sats. We have an integer number of satoshis we're assigning here. We do not use an integer number of bitcoin because floats are bad and they can cause rounding errors which we don't want to use in financial protocols.

So we have an 8-byte field to encode the amount. It's also little-endian. We have an output script here which has an output script length followed by an output script. This is a P2SH (pay-to-scripthash) script in this case. The hashes in p2sh are 20 bytes. It's a hash160.

## Native segwit

I should clarify what native segwit is. A lot of people refer to the first type of native segwit output just as "native segwit". You might be familira with P2WPKH. These are addresses starting with pc1q. These are the 0th version of native segwit outputs. Recently we had a soft-fork in November 2021 almost a year ago which introduced another new output type called pay-to-taproot (P2TR) which is also a native segwit output. It's the native segwit v1 output and these addresess start with bc1p. "p" encodes 1 in bech32. My example will be a pay-to-taproot output.

Q: What about wrapped segwit because that's two different output types?

A: Wrapped segwit is a little bit of a hybrid because wrapped segwit was made to be backward-compatible by satisfying the rules of P2SH but the witness part is all the same as native segwit. In the witness section of wrapped segwit, you would have exactly the same witness stack as in native segwit. We will get into that in a bit.

Between wrapped and native segwit, the difference is a forwarding script that says look at the witness and that's how we can satisfy the spending conditions. Nested is different. We're also not doing nested segwit outputs for native taproot, that was only a v0 thing. Now that people can hopefully build native segwit outputs, we will leave them behind.

## Native segwit v1

Here is the very first pay-to-taproot transaction that was ever spent on the blockchain. The message was "I like Schnorr sigs and I cannot lie". This is a bc1p address that indicates it's a P2TR output and it's also spending change to a P2TR output. Let's look at its serialization.

It looks similar to our previous example except we have a lot more orange in here. All the orange here is the witness bytes here. You will see that there are a few other differences. For example, the input script length here is now 0 and that's because we no longer have an input script on native segwit inputs. Instead, we provide the data to satisfy the spending conditions in the witness. All the native segwit inputs, you can always recognize them because their input script length is 0.

Let's look at the witness data. Who here remembers what we should have directly after the version here is a non-segwit output? Yes, the number of inputs. In the very first sentence, I said a transaction must always have at least one input and one output. If a non-segwit node that is not familiar with the native segwit format, and gets a transaction with 0 here, what will he do with that transaction? It's invalid, it's dropped and he bans his peer for giving him this bullshit. What we put here for the marker and the flag is, is just hey this is a new format and old people or old nodes shouldn't even read this and you got this by accident. Don't parse this. Then, the flag indicates that the transaction has a witness section which is inserted after the outputs before the locktime.

Q: What do you mean by invalid? I thought mempool had standardness. There's also non-standardness where the transaction is still valid. Is this a relay policy?

A: .. this representation of the transaction appears invalid because non-segwit nodes of which there are basically none on the network anymore, because the last non-segwit version was 0.12 and that is 10 versions ago so about 5 years ago and the lifecycle is that we maintain versions for like 2 years. So this is mostly hypothetical to explain how it worked back then, not an active problem any more. I'll take your question in 2 slides. I do mean invalid. If we get this representation of a transaction to a non-segwit node, then they will think it is crap.

Q: It happens to be the case with segwit it's bizarre that a unique situation where as I understand it the old segwit nodes talking to a non-segwit it will construct a different transaction vector and different block. It won't have these times. There's an isomorphism between this transaction and a valid non-segwit transaction. The non-valid thing is very confusing.

A: There is a different representation of the transaction that the non-segwit node will be able to parse. They don't need the witness data because of how the soft-fork worked and they wouldn't understand the witness data anyway.

So this indicates tihs is a segwit output. Why don't we have a count of witness stacks? Well, because every input has to have a witness stack in a segwit transaction. In this tx, we have only a single input so we have a single witness stack to satisfy that input. So the first thing we have is a number of witness items, and then the length in this case the first and only witness item.

## Block space in segwit

Before segwit, we had a block size limit of 1 megabyte. We just counted the raw bytes of all the data in a block and that had to be at most 1 million and otherwise the block was invalid. With segwit we introduced a weight limit for blockspace which is 4 million weight units. Since we only give the non-witness data to old nodes, they only see this green part up here which is always smaller than 1 megabyte. But for nodes that speak segwit, we also give them the witness data so that we can exceed 1 megabyte now. In August we had a new biggest block which was 2.77 megabytes.

The segwit nodes see the complete transaction. Often there was this misunderstanding that the witness is not part of the transaction or not part of the block or things like that. The segwit node sees the full segwit transaction. For the nodes that don't understand segwit, what we give them is the transaction without the witness data. This should look very familiar. It has a version, input counter, the outpoint telling what UTXO is being spent so it can be deleted from the UTXO set, we have an input string script which happens to be of length 0, and then a sequence, and then the output scripts and the locktime. All the parts are the same as pre-segwit for non-segwit nodes but they have a reduced security model because the non-segwit nodes can't actually validate the signature. We strip out the witness marker and witness section and just hand them the stripped transaction. This is smaller than the full transaction which lets us stick to the 1 megabyte block limit that the old nodes continue to enforce and it also has reduced security because the pre-segwit nodes don't get the input condition scripts to show that someone was authorized.

## txid

How do we have the same txid between segwit and non-segwit nodes? Well, segwit introduced another change which is that we calculate txid for segwit transactions only from the stripped transactions. We use this as input to calculate the txid which is just a hash of the tx data. This also allows us to do things like lightning because in lightning we need to build a refund transaction that spends the output here before it is signed. You don't want to give the channel partner the funding transaction that is fully signed because then they can make sure the money goes there even without agreeing on the downstream future transactions. We have to agree on the downstream transactions like the refunding transaction before putting the commitment funding money at risk.

Segwit nodes and non-segwit nodes therefore always have the same txid for the same transactions even though they have different representations.

There is also a wtxid witness txid. In order to commit to the full transaction that the segwit nodes see, we need a commitment to the full complete transaction. If we were only committing to the script transaction, then someone can strip out the signature and put them in a block and it would be invalid in a new block. We use the stripped transaction to take the txid, that's what we commit to in the merkle root of the block, and that's what we can build a child transaction on top of. That's what makes transaction malleability go away. But then, for the segwit nodes, to make sure that they actually have the complete transaction, we also have a witness commitment in the coinbase which commits to the wtxid values which are built from the complete transaction.

Q: If you have a transaction with multiple inputs, is there something in the witness data that delineates finishing and starting that different data?

A: There is not, no. How does that work? We have an input counter up here that tells us how many witness stacks there will be. Every input needs a witness stack. The legacy input type will have a witness stack of length 0. The second witness stack will have data for our example transaction using P2TR for example. ..... We don't really have to tell how many witness stacks there will be.

## Transaction weight

For transaction weight we multiply 4 by the non-witness data and one time the witness data. That's the transaction weight when these two values are added. To get the stripped transaction, we count each byte of the non-witness data 4 times, and then the witness data is counted once. These coefficients were selected because they felt good.

What about a transaction with no witness data? We have only non-witness data and we count that 4x, and we have a limit of 4 million weight units and before that we had a limit of 1 million bytes. If we count all the non-witness data 4x, that's the same size: we multiply it by 4 and the limit is 4 times higher. For non-segwit transactions, this continues to be backwards compatible and completely correct for old nodes because old nodes don't see witness data. The proportion of the 4 million weight units of a block is bigger than the non-witness data of 1 million bytes. Whenever we have segwit transactions, they will always fit into a stripped block and a stripped block will always fit into the 1 megabyte limit.

Q: I heard that there is a proposal to remove the witness discount. Could you elaborate on that?

A: There were some people speculating about whether removing the witness discount in the long-term would be able to be soft-forked into the protocol. My argument I made is that if you always count the cost of witness data as non-witness data, then that's strictly smaller than the- it would use less of the available block space than the current rules so we should be able to soft-fork that in. What that would do is if we had cross-input signature aggregation (transactions having multiple inputs but only one signature) then that would make it more attractive to use signature aggregation because it would remove more costs from transactions and also decrease the available blockspace which some people find good because we apparently already have too much blockspace already. I don't subscribe to that, but I found it to be an interesting hypothetical scenario to consider. It could be a good way to incentivize adoption of signature aggregation if we ever got that.

Q: The legacy signatures are not discounted, right?

A: Legacy signatures are counted as non-witness data. They are in the input scripts. A non-segwit transaction has to provide the witness data, so to speak, the script arguments to satisfy the condition script are provided in the input script. Here is a p2pkh input, and it provides a pubkey and a signature and with the output script the output script duplicates the pubkey, hashes it and checks that it matches the hash in the previous output and checks if the signature fits the pubkey. The pubkey and signature are in the input script and are therefore not considered witness data and they are therefore counted 4x.

Q: Why are you not discussing the most important feature of the witness discount? It produces an incentive to create larger transactions that are undercharged on fees. I thought you were going to talk about the rampant misconception that these transactions are smaller or more efficiently encoded.

A: Fine. I'll go to the next slide.

## Different output types

I will now enumerate all possible output types.

Segwit is a block size increase in that it allows to have more data in a block. But it is also sort of a, it doesn't really make transactions smaller at least not for wrapped segwit transactions. P2SH-P2WPKH is wrapped segwit single sig. Only script arguments are discounted in the witness section. P2TR has the biggest output size of the four types on this slide. In the raw byte length, a transaction with 2 inputs and 2 outputs of P2PKH which is the legacy type is basically the same size as a native segwit v0 single sig input. They are not significantly smaller. But, in the amount of block space that they consume due to the discount, the native segwit is 68 vbytes whereas the P2PKH input is 148 so it's almost 2x as big. P2TR is actually the smallest bytesize out of these. All together it's only 312 bytes, so it's about 20% smaller than native segwit and P2PKH. I agree in parts that for the older segwit types they are not a bandwidth improvement. But P2TR is actually smaller.
