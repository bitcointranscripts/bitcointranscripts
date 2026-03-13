---
title: 'Shielded CSV Private & Efficient Client Side Validation'
transcript_by: 'Garvit-77 via review.btctranscripts.com'
media: 'https://www.youtube.com/watch?v=zpghEIWveJI'
date: '2024-11-27'
tags: []
speakers:
  - 'Jonas Nick'
categories:
  - 'Shielded CSV'
source_file: 'https://www.youtube.com/watch?v=zpghEIWveJI'
summary: "The client-side validation approach removes transaction verification from the consensus rules. Instead, transaction data posted to the blockchain is only interpreted on each individual node (\"client-side\"). This approach allows building protocols with very low on-chain size and verification cost, while providing strong privacy.\n\nThis talk proposes the client-side validation protocol \"zkCSV\" (working title) that, in contrast to existing client-side validation protocols, only requires 64 bytes of on-chain space regardless of the size of the transaction and is fully private. The protocol's communication cost between transaction sender and receiver is independent of the transaction history. Furthermore, zkCSV can be instantiated with existing cryptographic zk-SNARK primitives.\n\nWith a trust-minimized mechanism like BitVM2 to bridge between the blockchain and the client-side validation protocol, zkCSV adds strong privacy to Bitcoin and scales Bitcoin to 100 transactions per second. It has been described as \"the most useful thing you can do with BitVM2\".\n\nEven without a bridge, zkCSV can be used to create a private cryptocurrency pegged to bitcoin (for example via the one-way peg) that offers substantial advantage over existing private cryptocurrencies. These currencies require users to validate all transactions, which contain relatively large and computationally expensive Zero-Knowledge proofs. zkCSV, however, only requires the recipient of a transaction to download the full transaction data, which results in significant reductions in computational and bandwidth costs. Furthermore, zkCSV derives its resistance to double-spending from Bitcoin, eliminating the need for its own consensus mechanism. Moreover, private cryptocurrencies are not able to hide the transaction graph better than zkCSV.\n\n What would an attendee learn from this talk?\n\n- What client-side validation is and what its advantages and limitations are.\n- How it is possible to achieve only 64 bytes on-chain cost using sign-to-contract and signature half-aggregation.\n- How zk-SNARKs and in particular proof-carrying data schemes are applied to provide strong privacy.\n- That private & efficient client-side validation is a largely unexplored framework that has a vast design space and potential for innovation, in particular for designs that allow efficient layer 2's.\n\n Is there anything folks should read up on before they attend this talk?\n\nno\n\n About the Speaker\n\n Social Links\n\n- Github:\_https://github.com/jonasnick\n- Twitter:\_https://x.com/n1ckler\n- Website:\_[https://nickler.ninja](https://nickler.ninja/)\n\n\nTABCONF 6, GitHub link\nhttps://github.com/TABConf/6.tabconf.com/issues/90"
---
**Jonas Nick** 00:00:18

This is the first session of the day.
I'm gonna talk about `Shielded CSV`, our private and efficient client-side validation protocol. This is joint work with Liam Egan from `Alpen labs` and Robin Linus from `ZeroSync`. If you attended the Socratic panel yesterday, then the first 10 minutes will be very similar, but afterwards we will go deeper into the protocol and also answer some of the questions that came up yesterday.
We start with a summary of the protocol. `Shielded CSV` is a transaction protocol to create an L1 on top of a blockchain that allows embedding arbitrary data.
For example, Bitcoin and by L1 I mean a system that provides the concept of ownership and transfer of ownership.
We can describe Bitcoin as consisting of two parts.
A layer, what I call layer 0.5, that governs the rules of the blockchain, such as how blocks look like, proof of work, best blockchain, etc and on top of that, there is some transaction validation protocol that determines how transactions look like and what makes them valid.`Shielded CSV` sits on top of layer 0.5 in parallel to an existing transaction validation protocol. There's some overlap between Shielded and the existing transaction validation because in order to embed data into the blockchain you typically need to make an ordinary transaction.
`Shielded CSV` inherits the double spending security from the underlying blockchain, the amount of Data embedded into the blockchain approaches 64 bytes per shielded payment. Coins and coin proofs which prove validity of the coin are sent directly to the receiver through some one-way communication channel and coin proofs are succinct. In particular, that means that they are constant size regardless of the number of the overall transactions.
`Shielded CSV` is fully private, which means that coin and coin proof reveal nothing except that the coin is valid.

### Motivation for Sheilded csv

Our motivation for this is twofold.
First, we believe that Shielded is a more efficient design for private cryptocurrencies because zero knowledge proofs do not end up on the blockchain and they are not verified by all full nodes of the system. Also Shielded can use an existing blockchain and does not need to create its own. Our primary motivation is **improving Bitcoin's privacy**, in that case Shielded would use Bitcoin's blockchain.
Since Shielded is still a separate L1, it requires a bridging mechanism between ordinary Bitcoin and the shielded system, which can be built, for example, with a BitVM type system, but also in principle with a one-way peg or federated peg.

So in order to get a better understanding of the client-side validation paradigm, we start by building a toy `CSV protocol`.
We have Ivy, the issuer, who wants to issue froge coins. On the Bitcoin chain, Ivy has an unspent transaction output with two sats and she signs a message, *"I issue 10 froge coins in transaction 1, output 1, redeemable for physical frogs"*. This creates an additional meaning to Ivy's on-chain UTXO, not only does it represent two sats, but also 10 Frogecoins to everyone who's interested in the Frogecoin system. Now Ivy wants to send Frogecoins to Roy the receiver. So she creates an off-chain transaction that sends some Frogecoins to Roy and To prevent double spending, she creates a corresponding on-chain transaction that commits to the Frogecoin transaction and sends some arbitrary number of sats to Roy. Roy sees the Bitcoin transaction, but he wants Frogecoins. So, Ivy sends the entire Frogecoin transaction graph as a proof to Roy, Roy checks that all transactions are valid, connect to an issuance transaction, and have corresponding on-chain transactions.

### Client-side Validation and System Comparison

<!-- needs a image for comparison  -->
While this toy protocol is simplistic, it demonstrates some key aspects of client-side validation protocols. This table from the white paper compares `RGB`, `Taproot Assets`, ``intmax2``, and `Shielded CSV` across three dimensions: blockchain space per CSV transaction, proof size sent to the receiver, and system privacy.

The blockchain space required per RGB and Taproot Assets transaction is the same as in our toy `CSV protocol`. It is one Bitcoin transaction with the same number of inputs and outputs as the `CSV transaction`. The `intmax2` protocol reduces that to only four to five bytes per payment using an interactive protocol between senders. That is remarkable.
In `Shielded CSV`, the space requirement is 64 bytes per transaction, regardless of the size of the `CSV transaction`. This is worse than `intmax2` in terms of space, but it does not require an interactive protocol with four-megaweight-unit blocks, the Bitcoin blockchain would support about 100 `Shielded CSV` transactions per second.
The size of `RGB` and `Taproot-Assets` `coin proofs` is similar to the toy ``CSV protocol``. It is proportional to the transaction history, meaning the set of ancestor transactions of the transaction paying the recipient. In `intmax2` and `Shielded CSV`, the proof size is constant. In `RGB`, `Taproot-Assets`, and `intmax2`, the receiver sees the entire transaction history graph, revealing essentially the same information as Bitcoin transactions. 
`RGB` encrypts amounts and asset types using Confidential Transactions, which makes transaction graph analysis significantly more difficult. `RGB-issued` assets are compatible with the Lightning Network, which can improve user privacy. `Shielded CSV`, on the other hand, is fully private. A coin proof leaks nothing to the receiver except the validity of the coin. 

### From Toy CSV to `Shielded CSV` 

We have built the toy `CSV protocol`.
How do we get from that to `Shielded CSV`?
We first need to better understand what client-side validation actually is. The main insight is that transaction validation does not need to be part of the consensus rules. This idea was first published by Peter Todd in 2013. He wrote, "Why validation is an optional optimization." Given only proof of publication and consensus on transaction ordering, meaning a blockchain, can we build a successful cryptocurrency system? Surprisingly, the answer is yes.

Suppose Bitcoin allowed blocks to contain invalid transactions. Transactions would then be validated client-side and ignored if invalid. If there is no transaction validation in consensus, we do not need to post full transactions to the blockchain instead, we derive a short piece of data from the CSV transaction called the nullifier. We post this nullifier to the blockchain solely to prevent double spending. It is called a nullifier because it nullifies a coin and prevents reuse. In the toy `CSV protocol`, the nullifier was essentially a full Bitcoin transaction, which is not short and has significant overhead.
In `Shielded CSV`, the nullifier is 64 bytes interpreted entirely client-side. If we take client-side validation seriously, we uncover a much deeper paradigm. For the remainder, we focus on what is above the surface. In particular, we explain how we arrive at 64-byte nullifiers and how we achieve constant and private coin proofs.

### Client-Side Validated Transactions

A client-side validated transaction is similar to a Bitcoin transaction. It consists of inputs and outputs. We call transaction outputs coins to distinguish them from other output types.
A coin consists of an amount and a public key. We define a coin ID as the transaction hash concatenated with the output index.
Transaction inputs contain coin IDs referencing the coins being spent. A coin proof is the history of transactions connecting a coin to one or more issuance transactions.
When Sally pays Roy, she sends him the coin and its coin proof. Roy verifies that all transactions in the coin proof are valid, for example, he checks that they do not create more value than they consume and that they connect to issuance transactions. 

### Preventing Double Spending with Nullifiers 

To prevent double spending, we define the nullifier as a tuple of the coin ID and the hash of the transaction spending the coin. Sally writes this nullifier to the blockchain. Roy reads the blockchain and processes all nullifiers. He maintains a key-value store mapping coin IDs to transaction hashes. 
If Roy encounters a coin ID already in the store, he ignores the new nullifier. If Alice attempts to double spend by posting a nullifier with an existing coin ID, Roy ignores it.
In addition to the ignore rule, we add another rule. Sally sends the coin and coin proof directly to Roy after posting the nullifier. Roy verifies the coin proof. Every spent coin in the coin proof must be present in the key-value store. The transaction hashes in the coin proof must match the stored hashes.This prevents double spending using a nullifier smaller than a full Bitcoin transaction.

### Securing and Compressing Nullifiers

The initial nullifier design is insecure. Anyone who knows a `coin ID` can post a nullifier. We fix this by adding a `Schnorr signature`. Another issue is requiring one nullifier per spent coin. We introduce accounts, which are special transaction outputs. We now nullify an account state instead of individual coins. This allows one nullifier per account state update.
Another issue is the need for a dedicated on-chain transaction to post each nullifier. We introduce a publisher role.

A publisher collects nullifiers and posts them together in one Bitcoin transaction. Anyone capable of creating a Bitcoin transaction can act as a publisher. We begin with a nullifier consisting of coin ID and transaction hash. We introduce accounts, replacing coin ID with a nullifier public key. We add a `Schnorr signature`, producing a 128-byte nullifier. Using sign-to-contract, we commit to the transaction hash within the signature, removing the need to include it explicitly. Finally, the publisher aggregates signatures using Schnorr half-aggregation. This compresses the signature from 64 bytes to 32 bytes.
This results in the final 64-byte aggregate nullifier used in `Shielded CSV`.

## `Shielded CSV` Workflow

Sally creates a transaction consuming her account state and coins. It produces a new account state and new coins, including one for Roy. She sends the nullifier to the publisher.
The nullifier nullifies her previous account state and commits to her transaction. The publisher aggregates nullifiers and publishes an aggregate nullifier on-chain.
Roy reads aggregate nullifiers, verifies the aggregate signature, and updates his store. Sally sends Roy the coin and coin proof.
Roy verifies that all transactions in the coin proof are correct and correspond to entries in the store.
Succinct and Private Coin Proofs via Proof-Carrying Data

In the toy protocol, a coin proof contains all ancestor transactions. Its size grows with transaction history and reveals the transaction graph. The solution is Proof-Carrying Data (PCD).
In distributed computing, nodes take input and produce output. Bugs are inevitable. PCD attaches a proof π to each output proving correctness. Each proof verifies not only local computation but all preceding computation. The proof size and verification time are independent of graph size. It can be made zero knowledge. The proof reveals nothing except correctness.
PCD can be instantiated using recursive SNARKs or folding schemes. In `Shielded CSV`, each node corresponds to a shielded transaction. Outputs are account states or coins. Local inputs prove valid account state transitions. The π values are the coin proofs. To create a coin proof, Sally takes her account state, coins, proofs, and private input. She generates a new account state, new proof, and a new coin with proof for Roy. The proof shows all transactions are valid and nullified, succinctly and zero knowledge. In the full protocol, a transaction corresponds to multiple nodes to allow trustless fee payment to the publisher.

## Components and Open Questions

`Shielded CSV` consists of an instantiation of PCD.
- It defines correct computation rules for account state transitions in Rust.
- It specifies how blocks are processed and how the nullifier store is updated.
The paper also addresses blockchain reorgs, publisher fee payment, accumulators, shared T-of-N accounts, atomic swaps with Bitcoin and PTLC-enabled Lightning, wallet state management, and nullifier accumulators.

Open questions remain.

- We need a complete specification & test vectors.
- We must instantiate primitives such as PCD, accumulators, and hash functions efficiently.
- We need bridging mechanisms to Bitcoin and to evaluate BitVM practicality.
- We must define sender-receiver communication channels and understand UX implications.
- We must examine drawbacks of client-side validation paradigm.
- We need mechanisms for nullifier propagation to publishers(mempool).
- We seek more efficient timelocks, payment channels compatible with Lightning, light clients, and more expressive smart contracts.

You can find the paper at [shieldedcsv.org](https://shieldedcsv.org). Please read it and provide feedback via email or GitHub issues.
Thank you.

**Audience** 00:26:22

Hey, Jonas, great talk.
I'm still trying to process how global uniqueness is achieved, drilling in on double spending?
It's apparent to me how the nullifier prevents double spending of transactions that have inputs from previous blocks. How does a verifier conclude that no transaction data within a single block is being double spent, i.e. that information is globally unique only in that one place.

**Jonas Nick** 00:26:56

We don't specify exactly how a client would read the block but you could imagine that they get the block, parse it as a list of transaction as in Bitcoin, and then they just go from top to bottom, read through the witness part, find the nullifiers, and then whenever they encounter a nullifier, they insert it into the nullifier key value store. So if there is actually a duplicate nullifier, some duplicate coin ID somewhere later in the block, then the receiver would have already inserted that coin ID into the nullifier store, and then they would ignore this second nullifier completely.

**Audience** 00:27:45

Are those specific details included in the paper or maybe something to follow up with and further specify?

**Jonas Nick** 00:28:01

This is definitely something that someone needs to figure out exactly if they wanted to implement this. But the paper is more abstract than that.

**Audience** 00:28:14

How does one recognize a nullifier? Is it super obvious?
That could be a censorship problem, or is it like, oh, we're just gonna evaluate every signature on the blockchain, and if it's a nullifier, or it could not be, we just store them all?

**Jonas Nick** 00:28:31

I haven't thought much about it, because, like, I don't know, you could imagine there's some magic bytes somewhere in the witness. There's these envelopes for inscriptions that I don't know much about for how to inscribe data in the witness part. I don't know exactly how that would look like. I guess there are many degrees of freedom how to actually do that, but I don't see a way how you would.

**Audience** 00:29:03
You have to store them all forever, right?

**Jonas Nick** 00:29:04

Yes, right.

**Audience** 00:29:04

So you probably don't want to store every single Schnorr signature, just in case it happens to be a nullifier.

**Jonas Nick** 00:29:12

Yeah, it's correct. Ideally you don't want to store garbage, but yeah, not sure how to best prevent that because it's easy for someone to create something that looks like a nullifier but is not one and you have to store it.

**Audience** 00:29:25

If you do put a magic byte on it, then there's gonna be some people that are gonna be like, oh, we must censor those things.

**Jonas Nick** 00:29:31

Right, yeah, but you still need to verify this aggregate signature for the nullifier, so random data will not have a valid aggregate signature.

**Audience** 00:29:51

Is there something in the nullifier that binds it to the recipient?
Because what prevents Alice from handing the exact same data to Bob and exact same data to Carol at the same time and they're both referring back to the same nullifier.

**Jonas Nick** 00:30:09

So I mentioned that, so we have transactions and transaction outputs. Transaction outputs are accounts or coins, so we care about coins, and coins consist of amounts and public keys, the public key would be Alice's public key.
Although it's a little bit different in the shielded protocol because we have this concept of an account ID, which is actually a public key and you use that, your public key identifies your account, and in order to create an address, you produce a hiding commitment to that account ID. So you can produce as many addresses as you want from your account ID, they are unlinkable.
You can post them on your website give them to the sender, and then the coin actually does not contain the public key, but rather this hiding commitment and if you want to spend the coin, you need to open it and show this is my account ID that corresponds to my account state, which is also input to the transaction.

**Audience** 00:31:40

Well, the blockchain itself is a chain of digital signatures, right? but each transaction is signed over to the next public key, which is signed over to the next public key, and so on and so forth.
So it seems like we have this parallel ledger that's being sent alongside, that's being embedded in the primary ledger, I guess the 0.5 layer.

**Jonas Nick** 00:32:16

Yeah, that's one way to think about it, There exists this transaction graph, this separate transaction graph, but what is important is that no one knows it because there are just these coin proofs and you don't learn about the transaction graph, You just get a proof, the transaction graph is correct, and here's my coin and the coin is correct, but you don't know the transaction graph, but it exists in some space.

**Audience** 00:32:48

So suppose that I double spend. So I send the same coin to you and I send the same coin to Jesse and I or a publisher, I guess, publishes a transaction or a new nullifier for both of those.
Presumably the nullifiers would be distinct. So at what point would it be noticed?

**Jonas Nick** 00:33:14

The nullifier won't, the nullifier will potentially be distinct. Remember, it consists of these two parts, coin ID, transaction hash. The coin IDs will be the same, otherwise they don't spend the same coin.

**Audience** 00:33:27

The nullifier identifies what I'm spending, but not where it's going.

**Jonas Nick** 00:33:39

The nullifier contains a transaction hash, and the transaction hash commits to the receiver because the transaction, just like a Bitcoin transaction, the transaction has inputs and outputs, and outputs, there are coins, some outputs are coins, potentially coins contain amounts and a public key or an address, explained earlier.

**Audience** 00:34:20

Okay.

**Audience** 00:34:25

You're posting a nullifier to the chain with a signature attached is that signature signed with a key that's linked to an identity like account, or is that nullifier scoped, or are you using like a re-randomizable signature scheme like Zcash?

**Jonas Nick** 00:34:43

It's more simple than that, obviously you don't use the same public key all the time, this would defeat the purpose.
So what you do in account state update is you commit to your next nullifier public key, which you will use to nullify the next account state and then you produce a signature for that nullifier public key and you can draw the next nullifier public key essentially at random, thereby this is unlinkable.
The account system is a bit difficult to wrap your head around, but it really helps because then we only have to post one nullifier per transaction to the chain, which is really nice.
Thank you.
