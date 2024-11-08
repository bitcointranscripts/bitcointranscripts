---
title: Scalable and Accountable Timestamping
transcript_by: Bryan Bishop
tags:
  - proof-systems
speakers:
  - Riccardo Casatta
---
slides <https://scalingbitcoin.org/milan2016/presentations/D1%20-%20A%20-%20Riccardo.pdf>

<https://twitter.com/kanzure/status/784773221610586112>

Hi everybody. I attended Montreal and Hong Kong. It's a pleasurable to be here in Milan giving a talk about scaling bitcoin. I am going to be talking about scalable and accountable timestamping. Why timestamping at this conference? Then I will talk about aggregating timestamps. Also there needs to be a timestamping proof format. I will describe two of the formats for this purpose, including opentimestamps and chainpoint.

## Why timestamps at Scaling Bitcoin?

I want to to clarify what is a timestamp. A timestamp proves that a message existed prior to some point in time. That's all it proves. This chart shows the number of OP\_RETURN transactions. This is often used for timestamping. It's a log scale. In 2015, there was a big increase in the number of transactions using this. In 2016, it's about 4000 transactions/day or about 2% of the capacity of the network. It's almost impossible to say how many timestamps are done. This is good for privacy. But a good guess would be to correlate it with the number of transactions........

OP\_RETURN utilization: coinspark, open assets, colu, eternity wall, omni layer, .... about 50% seem to be timestamping and the other 50% are relying on other properties than blockchain. So we have 2000 transactions/day doing timestamping, then. We just need 200 transactions/day for global timestamping needs. This is less cost. This is like 0.1% of total block space.

## One-certificate-one-transaction

This is one of the proposals for certificates in the blockchain. It's a certificate. No, sorry. The first input is the key of the issuer. The first output represents the recipient of the certificate. The second output is the pubkey. And then the hash of the certificate. With this solution, everyone can check all certificates emitted by one authority. The certificates that someone owns. Also the certificates can be revoked, by spending the revocation key. With this solution, we have one-to-one mapping between certificates and issuing on the blockchain.

So say 3000 degrees/year * 40 exams/year * 40,000 universities. So that means we need 80 megabyte blocks just for degree certificates in the blockchain. So let's see if we can do better with aggregation.

## Aggregating timestamps

Everyone in the room should be able to recognize the bitcoin block header data structure. We build a merkle tree. We hash every transaction, and then we get a merkle root right inside of the bitcoin block header, and we just get another... which is the timestamp... and basically there is a list of data, and with the same technique we build a merkle root of timestamping data to be timestamped. This merkle root is written inside of a single transaction that is inside of the merkle root of the bitcoin block header.

How do we prove that some data belongs in that merkle tree? So we have the yellow data for example, and we need the information on the green squares, and everything in light bue is from the hashing data. And so, basically, the timestamping property is that-- directly the hsah of the public key. The transaction. But we can see that we achieve many timestamps for a single bitcoin transaction.

So the number of ... in this.. is log of the ... so the proof does not grow with the amount of data to be timestamped. You're not preventing double spending. This solution does not cover this aspect. We are obtaining scalability exactly because we are only doing timestamping here.

There is some technique here like hashchain on top of the merkle trees. It's complex. I'm putting hashchain here for reference. It would require another presentation about this. So coming back to the initial claim, we said that we just need 20 transactions/day for timestamping needs. So it's about one transaction per block. While it's true that a single timestamp would be dangerous because we need to trust the timestamper to do his job, but the worst thing that could happen is that the timestamper is not doing its job, so you could see that happening and just do the job yourself.

We can theoretically rely on a single global timestamper. We only need about 200 transactions/day. This scenario requires a common tool for replication and a standard format.

## Timestamping proof formats

Let's start with opentimestamps, which was proposed and implemented by petertodd. The basic idea of the format is that if you can create a path from the data, if you can create a path of commitment operations from the data we want to timestamp to a merkle root in a bitcoin blockheader, you are testing the documenting is committing to the block, or the block is committing to that document rather. And this means you cannot change the data without changing the merkle root of the bitcoin block, which would be a highly expensive operation.

The format also supports intermediate states to accomodate the nature of the blockchain timstamps which are not real time. When a client asks for a timestamp, it gives one immediately returned within a few seconds while the server waits to aggregate for the whole second of receivables. It then hands the client the state and commitment operations. When requested, the server will produce the proof in the other state. The client doesn't need to rely on the server after this point.

Another feature is that this... so the same proof would contain multiple attestation. This way you can spot different timestamping chains or different providers. All of this can be in the same opentimestamps proof. There are multiple reasons to include multiple attestation, such as showing coherency, or providing validation cross-checking, or preventing failure, or not requiring trust in a single timestamping system.

Also the following operations is supported-- say different hash operations in the commitment operations or the merkle tree, with a different hash function for the block header commitments.

Also, opentimestamps has git integration. Git has a extra space for extra data, for example to sign commits with PGP signatures. How do we verify a signature for an expired or revoked key? Well there's only the keys signing them... so you can look at timestamps of the commits to see if the keys were valid during the time that the keys were active. On github, there was recently a bug where both pgp and timestamps would be considered an invalid signature. However, they fixed this the other day and it now says it's a valid signature, although they don't seem to be checking timestamps yet.

<https://petertodd.org/2016/opentimestamps-announcement>

<https://petertodd.org/2016/opentimestamps-git-integration>

## Chainpoint

Chainpoint describes a merkle tree where the chainpoint proof is in JSON. It contains information to go from the data to the hash of the transaction timestamped that contains the timestamping information. Basically, it contains data that is in the red circle. We can see that this operation is supported by receipt and tools provided to verify receipts, and supported anchor ties. We have bitcoin and ethereum. A single receipt and a single type of hash... so this.... so if we, we can put together two receipts because we are doing JSON-LD, to create something we have seen before. .. for the same data. The target hash is the same. So we use this receipt, if the initial packet is in common between the two receipts, then we have some redundancy in the proof, but it's just initial compact. But in some cases, like we have seen before, we have the hash in the bitcoin blockchain merkle tree, is different from the timestamp merkle tree, it's difficult to represent using this system.

For the comparison of the size of proofs for opentimestamp versus chainpoint using json, as we can see the json is not that big of a deal. We can use msgpack for json serialization format. Testing compression is not very interesting. We can have gzip with better results, and most of the time msgpack + gzip is slightly better. Apart from size comparison, the point of the binary format of opentimestamps was to give a format with an atomic interpretation that you can either parse the data or you could do nothing with it. And that's exactly what we want.

<img src="https://imgs.xkcd.com/comics/standards_2x.png" />

