---
title: Abstract Thinking About Consensus Systems
transcript_by: Bryan Bishop
tags:
  - consensus-enforcement
speakers:
  - Luke Dashjr
media: https://www.youtube.com/watch?v=INku7GsxhXY
date: 2018-10-05
aliases:
  - /scalingbitcoin/tokyo-2018/edgedevplusplus/abstract-thinking-about-consensus-systems
---
<https://twitter.com/kanzure/status/1048039485550690304>

slides: <https://drive.google.com/file/d/1LiGzgFXMI2zq8o9skErLcO3ET2YeQbyx/view?usp=sharing>

## Serialization

Blocks are usually thought of as a serialized data stream. But really these are only true on the network serialization or over the network. A different implementation of bitcoin could in theory use a different format. The format is only used on the network and the disk, not the consensus protocol. The format could actually be completely different.

Each block is identified by a single cryptographic hash and it commits to various abstract information. To verify the block, one must compute the correct hash. The block data allows you to compute the correct hash independent of what format that data is stored in. It's all the same as long as the commitments are calculated correctly.

There's some information required to compute the blockhash. There's a block version, a timestamp, difficulty, arbitrary data called the nonce. Note that there's no previous blockhash or merkle root. Those are mid-states that don't need to be stored.

Format-independence extends to transactions as well. They are a format of sequenced bytes indicating a transfer, but really this could be formatted in any way, as long as the commitment is correctly calculated. Suppose there was a new memo field, but you wanted to make it part of the consensus rules. In segwit, the signature was moved to a new witness field. The old field must be treated as empty for validation. By requiring it to be empty, it was effectively deleted. In segwit, the commitment algorithm was modified with the new witness field and some other changes. With a soft-fork, we can add a consensus rule that the transaction is only valid if the witness field validates correctly. Also, the commitment algorithm is modified where it commits to the generation transaction's output.

## Objects vs serialisation thereof

Often when developers think of blocks, they think of a header followed by a bunch of data representing transactions.
Usually that works fine, but it's not quite accurate, and can occasionally result in some subtle, unconscious assumptions that might make things more difficult than they need to be.

In reality, blocks in this format are only ever used two places: over the network, when a node is doing the initial blockchain synchronisation, and storing the block on the disk.
But neither of these are part of the consensus itself, and an implementation of Bitcoin could very well use a completely different format if desired without necessarily breaking compatibility with the rest of the community.

So what actually constitutes a block? Each block is identified by a single cryptographic hash.
That hash commits to various abstract information.
No matter how the block is stored or transmitted over the network, to verify the block, one must compute the correct hash.
Therefore, the block itself is comprised of the information required for computing the correct hash, independently of what format that information is stored in.

## Commitment algorithm

What information is needed to compute the block hash?
First, we have the block version (which is actually a can of worms, but let's not get into that now).
We also have the timestamp, difficulty, and an arbitrary 32 bits called the "nonce".
These simple fields are called the block header, and are committed to simply by adding them into a SHA256 hash in a well-defined manner.
But the block hash also commits to more information using two more complicated algorithms, call a block chain and a merkle tree, which provide extra functionality not relevant to this topic.
Despite the additional complexity and mid-calculation hashes, at the end of the day, these are both still just committing to information.

## Abstract transactions, and extending them

This extends to the transactions as well.
One is tempted to just see a transaction as a sequence of formatted bytes indicating a transfer, but in reality, the transaction can be represented any way an implementer likes, so long as the commitment is correctly calculated when it is mined into a block.
There are also two additional commitments needed for transactions: the transaction id, which must be calculated when spending an output created by such a transaction, and the signatures, which are calculated using an asymmetric digital signature to prove this transaction has permission to consume its inputs. But these similarly are commitments to the abstract information making up a transaction.

Since the serialisation of transactions and blocks is not relevant to the consensus system itself, let's disregard it, and use JSON instead to look at them.
<slide>

A nice property of looking at this in JSON, is that it becomes obvious that we can add new keys without disrupting anything.
For example, we could add a "memo" field.
<slide>
Since the block does not commit to this memo field, however, it does not need to be processed by other nodes to validate the block.
That makes sense, since other nodes really don't care about the memo.
But if your counterparty does, you can send it to them using any common network protocol.

## Adding consensus-critical fields to transactions

However, what if you want to use this field in new rules?
For example, let's look at Segwit.
The infamous problem with unintended malleability was a result of the transaction id committing to more information than the digital signature.
Specifically, the transaction id committed to the "signature" field, while the signature obviously could not commit to itself.
The solution was to add a new field, called the "witness", and move the signature there, while requiring the old "signature" field to be empty.
By requiring the old field to be empty, it is effectively deleted, as its commitment becomes a constant.
<slide>
So now we have replaced the "signature" field with a new "witness" field.
None of the block, the transaction id, nor the signature commit to this new field, so like the "memo" field, it can be ignored by other nodes.
But with a softfork, we can add a consensus rule that a block is only valid if the "witness" fields all verify correctly.
Now, nodes must receive and validate the "witness" field even without any commitment to it.

## Extending the block commitment

Unfortunately, without a commitment to the new information, an attacker can use a valid block hash to trigger the more CPU-time consuming signature validations for a block that is invalid because the final witness fails due to corruption.
So, to avoid denial of service attacks, we need to have the block hash commit to any field used for validation.

Since existing nodes already calculate the block's commitment in a specific way that does not include this new "witness" field, we need to extend the current commitment algorithm somehow.
How can we do this? By reusing an arbitrary 256-bit piece of information already committed to, to commit to a new commitment hash instead.

Transaction outputs, including as part of the block reward, each have scripts determining the conditions under which they can be spent.
These outputs also are allowed to have a value of zero bitcoins.
For Segwit, we chose to increment the output count, and commit to the new information in a merkle tree as if it were 256 bits of output script data.
Now, old nodes can be told of this fake "output" so they still calculate the correct block hash, whereas new nodes can implement the revised commitment algorithm.

As a result, we have cleanly replaced the "signature" field with a new "witness" field, without breaking backward compatibility, or even with any ugly hacks.

## Block size vs weight

Now, going back to the distinction between the abstract information and serialisation thereof...
Years ago, the infamous block size limit was introduced.
This was in fact the first and only consensus rule that dealt directly with the disk serialisation of the block headers and new transactions.
A lot of discussion can be found about what this block size limit should or shouldn't be, but the real question that should have been asked is why such a concept existed in the first place.
Disk space has never been a particularly limiting factor for nodes.
Bandwidth has, but it is only one of many factors.
Arguably the most expensive factor is the unspent transaction output (also known as "UTXO") database, which must be kept in quickly-accessible memory, but isn't related to block sizes at all.
Therefore, while clearly there must be some resource limit, it doesn't really make sense to have it be based on network serialisation bytes.

One particularly harmful shortcoming of this limit, is the difference in byte sizes between signatures and public keys.
For Bitcoin, the typical size of a public key script, included when creating a new UTXO entry, is approximately one fourth the size of the typical signature needed to remove the entry.
That means that it effectively costed four times more to reduce the burden of the UTXO set, than it did to increase the burden:
a huge conflict between the burden of the system and usage incentives.

Due to the way Segwit moved the signatures out of the existing block commitment, into a new commitment, old nodes would no longer see the signatures nor count their size toward the block size limit.
This created an opportunity to rebalance the limit to match the actual burdens on the network.
It therefore replaced with a byte limit with an abstract "weight limit".
The weight limit was four times larger, and data serialised for old nodes would count toward the new limit as four weight units per byte, thus avoiding violating their enforced size limit.
But instead of counting signatures at the same weight, since the “witness” field is new, we can count it at a lower weight.
Existing fields, on the other hand, can only be counted at a greater relative weight in a softfork.
