---
title: 'Shielded CSV Private & Efficient Client Side Validation '
speakers: null
source_file: https://www.youtube.com/watch?v=zpghEIWveJI
media: https://www.youtube.com/watch?v=zpghEIWveJI
date: '2024-11-27'
summary: "The client-side validation approach removes transaction verification\
    \ from the consensus rules. Instead, transaction data posted to the blockchain\
    \ is only interpreted on each individual node (\"client-side\"). This approach\
    \ allows building protocols with very low on-chain size and verification cost,\
    \ while providing strong privacy.\n\nThis talk proposes the client-side validation\
    \ protocol \"zkCSV\" (working title) that, in contrast to existing client-side\
    \ validation protocols, only requires 64 bytes of on-chain space regardless of\
    \ the size of the transaction and is fully private. The protocol's communication\
    \ cost between transaction sender and receiver is independent of the transaction\
    \ history. Furthermore, zkCSV can be instantiated with existing cryptographic\
    \ zk-SNARK primitives.\n\nWith a trust-minimized mechanism like BitVM2 to bridge\
    \ between the blockchain and the client-side validation protocol, zkCSV adds strong\
    \ privacy to Bitcoin and scales Bitcoin to 100 transactions per second. It has\
    \ been described as \"the most useful thing you can do with BitVM2\".\n\nEven\
    \ without a bridge, zkCSV can be used to create a private cryptocurrency pegged\
    \ to bitcoin (for example via the one-way peg) that offers substantial advantage\
    \ over existing private cryptocurrencies. These currencies require users to validate\
    \ all transactions, which contain relatively large and computationally expensive\
    \ Zero-Knowledge proofs. zkCSV, however, only requires the recipient of a transaction\
    \ to download the full transaction data, which results in significant reductions\
    \ in computational and bandwidth costs. Furthermore, zkCSV derives its resistance\
    \ to double-spending from Bitcoin, eliminating the need for its own consensus\
    \ mechanism. Moreover, private cryptocurrencies are not able to hide the transaction\
    \ graph better than zkCSV.\n\n What would an attendee learn from this talk?\n\n\
    - What client-side validation is and what its advantages and limitations are.\n\
    - How it is possible to achieve only 64 bytes on-chain cost using sign-to-contract\
    \ and signature half-aggregation.\n- How zk-SNARKs and in particular proof-carrying\
    \ data schemes are applied to provide strong privacy.\n- That private & efficient\
    \ client-side validation is a largely unexplored framework that has a vast design\
    \ space and potential for innovation, in particular for designs that allow efficient\
    \ layer 2's.\n\n Is there anything folks should read up on before they attend\
    \ this talk?\n\nno\n\n About the Speaker\n\n Social Links\n\n- Github:\_https://github.com/jonasnick\n\
    - Twitter:\_https://x.com/n1ckler\n- Website:\_[https://nickler.ninja](https://nickler.ninja/)\n\
    \n\nTABCONF 6, GitHub link\nhttps://github.com/TABConf/6.tabconf.com/issues/90"
tags: []
categories:
    - Education
transcript_by: 0tuedon via tstbtc v1.0.0 --needs-review
---

Speaker 0: 00:00:18

This is the first session of the day.
Great to see you here nonetheless.
I promoted the session yesterday during the party.
Apparently it worked, so I'm pretty happy about that.
I'm gonna talk about Shielded CSV, our private and efficient client-side validation protocol.
This is joint work with Liam Egan from Alpenlabs and Robin Linus from XeroSync.
If you attended the Socratic panel yesterday, then the first 10 minutes will be very similar, but afterwards we will go deeper into the protocol and also answer some of the questions that came up yesterday.
We start with a summary of the protocol.
Shielded CSV is a transaction protocol to create an L1 on top of a blockchain that allows embedding arbitrary data.
For example, Bitcoin.
And by L1 I mean a system that provides the concept of ownership and transfer of ownership.
We can describe Bitcoin as consisting of two parts.
A layer, what I call layer 0.5, that governs the rules of the blockchain, such as how blocks look like, proof of work, best blockchain, et cetera.
And on top of that, there is some transaction validation protocol that determines how transactions look like and what makes them valid.
Shielded CSV sits on top of layer 0.5 in parallel to an existing transaction validation protocol.
There's some overlap between Shielded and the existing transaction validation because in order to embed data into the blockchain you typically need to make an ordinary transaction.
Shielded CSV inherits the double spending security from the underlying blockchain.
The amount of Data embedded into the blockchain approaches 64 bytes per shielded payment.
Coins and coin proofs which prove validity of the coin are sent directly to the receiver through some one-way communication channel.
And coin proofs are succinct.
In particular, that means that they are constant size regardless of the number of the overall transactions.
Shielded CSV is fully private, which means that coin and coin proof reveal nothing except that the coin is valid.
Okay, our motivation for this is twofold.
First, we believe that Shielded is a more efficient design for private cryptocurrencies because zero knowledge proofs do not end up on the blockchain and they are not verified by all full nodes of the system.
Also Shielded can use an existing blockchain and does not need to create its own.
But our primary motivation is improving Bitcoin's privacy, in which case Shielded would use Bitcoin's blockchain.
But since Shielded is still a separate L1, it requires a bridging mechanism between ordinary Bitcoin and the shielded system, which can be built, for example, with a BitVM type system, but also in principle with a one-way peg or federated peg.
So in order to get a better understanding of the client-side validation paradigm, we start by building a toy CSV protocol.
We have Ivy, the issuer, who wants to issue froge coins.
On the Bitcoin chain, Ivy has an unspent transaction output with two sets and she signs a message, I issue 10 froge coins in transaction one, output one, redeemable for physical frogs.
This creates an additional meaning to Ivy's on-chain UTXO.
Not only does it represent two sets, but also 10 Frogecoins to everyone who's interested in the Frogecoin system.
Now Ivy wants to send Frogecoins to Roy the receiver.
So she creates an off-chain transaction that sends some Frogecoins to Roy.
And To prevent double spending, she creates a corresponding on-chain transaction that commits to the Frogecoin transaction and sends some arbitrary number of sets to Roy.
Roy sees the Bitcoin transaction, but he wants Frogecoins.
So, Ivy sends the entire Frogecoin transaction graph as a proof to Roy.
Roy checks that all transactions are valid, connect to an issuance transaction, and have corresponding on-chain transactions.
While this toy protocol is simplistic, it demonstrates some key aspects of client-side validation protocols.
So this is a table from the white paper comparing RGB, taproot assets, IntMax2 and shielded CSV across three different dimensions.
The blockchain space required per CSV transaction, the size of the proof that is sent to the receiver and the privacy of the system.
The blockchain space required per RGB and taproot asset transaction is the same as in our toy CSV protocol.
It is one Bitcoin transaction with the same number of inputs and outputs as the CSV transaction.
The IntMax2 protocol manages to reduce that to only four to five bytes per payment using an interactive protocol between the senders.
That is pretty remarkable.
In shielded CSV, the space requirement is 64 bytes, regardless of the size of the CSV transaction, which is worse than IntMix2, but does not require an interactive protocol.
So the Bitcoin blockchain with four megawatt unit blocks would support about 100 shielded CSV transactions per second.
The size of RGB and taproot assets coin proofs is similar to the toy CSV protocol.
It is proportional to the transaction history, which is the set of ancestor transactions of the transaction paying the recipient.
In IntMex2 and ShieldedCSV, the proof size is constant.
In RGB, taproot assets and IntMex2, the receiver sees the entire transaction history graph, revealing essentially the same information as Bitcoin transactions.
RGB encrypts amounts and asset types using confidential transactions, which makes transaction graph analysis significantly more difficult.
RGB interpret assets are compatible with the Lightning Network, which can improve privacy of users.
Shielded, on the other hand, is what we call fully private.
A coin proof leaks nothing to the receiver except the validity of the coin.
Okay, so we've built the toy CSV protocol.
How do we get from that to shielded CSV?
And the answer is that we first need to take a step back and better understand what client-side validation actually is.
And the main insight is that transaction validation does not need to be part of the consensus rules.
This idea was actually first published by Peter Todd already in 2013.
He writes, why validation is an optional optimization.
Given only proof of publication and a consensus on the order of transactions, so blockchain, can we make a successful crypto coin system?
Surprisingly, the answer there is yes.
Suppose the rules of Bitcoin allowed blocks to contain invalid transactions, then transactions are only validated client side and they are simply ignored if they are invalid.
So how can we use this insight?
If there's no transaction validation, then we don't need to post the full transaction to the blockchain, right?
So what we can do instead is to derive a short piece of data from the CSV transaction that we call the nullifier.
And we post this nullifier to the blockchain just to prevent double spending.
The nullifier is called nullifier because it nullifies a coin and prevents reuse.
In the toy CSV protocol, the nullifier was essentially a full Bitcoin transaction, which is not short, has a lot of overhead.
In Shielded, the nullifier is 64 bytes of data that is interpreted entirely client-side.
So if we take client-side validation seriously, then we uncover this giant iceberg that goes deeper and deeper and deeper and deeper, but for the rest of the presentation, I wanna focus on just what's above the water.
In particular, how exactly we arrive at 64-byte nullifiers, which is what got me originally hooked on the client-side validation paradigm.
And in the end, I will try to shed some light on how we get constant and private coin proofs.
Okay, let's continue developing our toy protocol.
We first define a few things that we have basically all seen before.
So a client-side validated transaction is similar to a Bitcoin transaction.
It consists of inputs and outputs.
We call transaction outputs coins to distinguish them from other types of outputs that we also have in the system.
They consist of an amount and public key.
And we have the concept of a coin ID to uniquely identify coins.
The coin ID is the transaction hash concatenated with the index of the coin in the transaction.
Transaction inputs contain coin IDs to refer to the coins they are spending.
And the coin proof is the history of transactions connecting a coin to one or more issuance transactions.
So for Sally, the sender, to pay Roy, she sends him coin and coin proof.
Roy verifies that all transactions in the coin proof are valid.
For example, they don't create a larger amount than what they spent, and they do connect to issuance transactions.
So now, the most important slide.
How do we prevent double spending?
We define the nullifier to be a tuple of coin ID and the coin, the coin ID of the coin being spent and the hash of the transaction that spends the coin.
Sally takes this nullifier and writes it to the blockchain.
Roy reads the blockchain and processes all nullifiers contained there.
And while doing that, he maintains a data structure, the nullifier key value store, that stores the nullifiers he has read from the blockchain, and it maps the coin ID of the nullifier to this transaction hash.
Now the crucial rule is that whenever Roy encounters a coin ID that is already in the key value store, he just ignores that nullifier.
So if Alice would try to double spend by posting a nullifier with an already existing coin ID, then Roy would ignore the nullifier when processing a block.
And besides this nullifier ignore rule, we need a second rule.
So first, we need to remember Sally sends coin and coin proof directly to Roy after posting the nullifier to the blockchain.
And Roy maintains the key value store with nullifiers he's read from the blockchain.
And as we've mentioned before, Roy verifies the coin proof, checking all transactions in the coin proof are valid.
And the new rule is that every coin spent in the coin proof must be present in the key value store and the transaction hashes in the coin proof must match what is stored in the key value store.
So this design actually does successfully prevent double spending with a nullifier smaller than an actual Bitcoin transaction.
The nullifier is still quite different than what we actually use in shielded CSV, so I'm going to quickly go over the changes that we make to the nullifier without going into too much detail.
So first, our nullifier has a very big problem, which is that it's completely insecure.
Anyone can nullify any coin if they just know the coin ID.
They just post the coin ID and some transaction hash to the chain.
So we can solve that by adding a signature to the nullifier.
Another problem of our design so far is that we have to post one nullifier per coin that is spent instead of one nullifier per transaction.
So our solution is to introduce accounts, which are a special type of transaction outputs.
So we have two types of transaction outputs, coins and account states.
And having accounts allows us to nullify an account state instead of a coin.
So we only need to post one nullifier per account state update which can then spend an arbitrary number of coins.
Another problem is that in order to post a nullifier to the blockchain, we need to create a dedicated on-chain transaction which has a lot of overhead that we don't really want.
We only care about posting nullifier data to the blockchain.
We don't care about the transaction.
So our solution is to introduce the role of a publisher who collects nullifiers and posts them all at once to the blockchain with just a single transaction.
Publisher is not a permissioned role at all.
Anyone can do that.
Anyone who's able to create Bitcoin transaction can become a publisher.
Okay, so here's a quick summary how we get to 64-byte nullifiers.
So we start with a nullifier consisting of coin ID and transaction hash, which as we mentioned is insecure and requires one nullifier per spent coin.
We introduce accounts, which essentially replaces the coin ID with a nullifier public key.
I don't want to explain that, it would go too far.
We just accept it exists.
It's still insecure because there's no signature.
So we add a Schnorr signature and obtain a secure nullifier consisting of 128 bytes.
Then we use a technique that's known in the Bitcoin space as sign to contract, and essentially this allows us to commit to the transaction hash in the signature such that it does not need to be part of the nullifier explicitly.
Only in the coin proof, the prover needs to show, the coin prover needs to show that they actually committed to the transaction that they're claiming to commit to.
And finally, we define an aggregate nullifier, which is an aggregate nullifier that is created by the publisher.
The publisher uses Schnorr signature half aggregation to essentially compress the 64-byte Schnorr signature into a 32-byte Schnorr signature, and this gives us the final nullifier that is actually proposed in the shielded CSV white paper.
Okay, so we're finishing this section, how nullifiers work, with a diagram that summarizes shielded CSV.
Sally wants to pay Roy.
She creates a transaction that takes her account state, her coins, and generates a new account state and a new coin, or new coins, one of which is for Roy.
She sends the nullifier to the publisher.
That nullifier nullifies her current account state and commits to the transaction she created.
The publisher aggregates nullifiers, publishes an aggregate nullifier to the blockchain.
Roy reads the aggregate nullifiers from the chain, verifies the aggregate signature, and updates his nullifier key value store.
Sally sends coin and coin proof to Roy.
Roy verifies that all transactions in the coin proof are correct and correspond to an entry in the nullifier store.
Okay, we're now going to have a brief look at how shielded coin proofs become succinct and private because in our toy protocol right now, the coin proof consists of all ancestor transaction, so its size grows proportionally to the number of transactions and it reveals the transaction graph to the receiver.
And our solution is to wrap the protocol in a proof-carrying data scheme.
I'm going to talk about that now.
So proof-carrying data is a concept that originally comes from the distributed computing space.
So we have a network of computing nodes, they take some input, produce some output, and what's guaranteed to happen in distributed computing like this?
Bugs.
So the idea is to attach a proof pi to every output that proves that the computation is correct.
And therefore, the output data not only carries the output of the computation, but it carries a proof as well, which presumably is where the name comes from.
What is important is that the proofs do not only prove that the single output was computed correctly, but also that all preceding computation was correct.
So proof pi three proves that pi one and pi two were correct proofs as well.
The size and verification time of these proofs is independent of the graph size, and we can make it zero knowledge for incoming inputs and outputs.
So the proof reveals nothing about the computation graph except that the computation is correct.
And a PCD scheme can be, so PCD is a very abstract thing, but it can be instantiated with recursive SNARKs or so-called folding schemes.
We discuss that in more detail in the paper.
So maybe you can already guess how we can use that in the CSV protocol.
So every node in the computation roughly corresponds to a shielded transaction.
The outputs are either account states or coins.
The local input is the data necessary to prove a correct account state transition.
And the pies are the coin proofs.
So more concretely, in order to create a coin proof, Selly takes her current account state, some coin, and the corresponding proofs, as well as her private input, and creates a new account state and proof, and a new coin, and a coin proof that she sends to Roy.
The proof proves to Roy that all transactions are correct and have been nullified, succinct, and zero knowledge.
And why PCD?
Well, it has turned out to be really helpful in abstracting away the complexity related to the coin proofs, and this allowed us to extend the shielded CSV protocol relatively easily.
So for example, in the actual protocol, a transaction corresponds to multiple nodes in the graph, not just a single one, and that is to allow trustless fee payment to the publisher.
So, we're coming to an end.
What does shielded CSV consist of?
So first, it consists of an instantiation of PCD.
How do we actually get this primitives?
The paper just describes PCD as an abstract primitive and briefly mentions how it could be instantiated.
And the main part of shielded-csv is the definition of what is considered correct computation for the underlying PCD scheme.
So what makes a valid account state transition and which outputs of the transition are valid?
We specify those rules in Rust.
And finally, shield-csv consists of a specification that determines exactly how blocks are processed and how the nullifier key value store is updated.
There's much more in the paper than what we managed to discuss here.
For example, how to deal with blockchain reorgs, how to pay fees to publishers.
The paper gives detailed security definitions of the primitives, for example, of the various types of accumulators, how to do shared T of N accounts similar to T of N multi-sig wallets in the Bitcoin space.
How to do atomic swaps with Bitcoin and with PTLC enabled lightning.
The importance of wallet state and how to manage it.
And the papers specify the nullifier accumulator, much more.
But there are a lot of questions.
This is a new paradigm iceberg.
We just see in front of us what we see and we don't see everything.
But we know some questions are for sure open and one thing that we want to do in the future, would like to do is to have a more complete specification with test vectors.
We need to instantiate the primitives.
As I mentioned, it's not only PCD.
We also have these other things, accumulators, or even hashes, so the question is, what is the most efficient scheme we can use for that?
We want to improve the privacy of Bitcoin, so we need some bridging mechanism.
So someone needs to figure out whether BitVM is actually practical.
We need to figure out how exactly do these communication channels between sender and receiver look like and what implications do they have for the user experience?
Are there other drawbacks of the client-side validation paradigm that we're not aware of?
How do you get the nullifiers exactly from the senders to the publishers?
How to create more efficient time locks?
We specify one way in the paper, but we believe that there's a more efficient way.
How to do payment channels, ideally compatible with Lightning.
How to create light clients.
How to create more powerful smart contracts in the system.
And much more.
All right, that's all I had prepared for today.
You can find the paper, shieldedcsv.org.
It would be great if you would read it.
Much more details in there.
If you have comments, then don't hesitate to write us an email or open an issue on GitHub.
Thank you.

Speaker 1: 00:26:08

Thank you.
Thank you.
Thank you.
Thank you.
Thank you.
Thank you.
Thank you.
Got a question right over here.

Speaker 2: 00:26:22

Hey, Eunice, great talk.
I'm still trying to process how global uniqueness is achieved, so like drilling in on double spending.
It's apparent to me how the nullifier prevents double spending of transactions that have inputs from previous blocks.
How does a verifier conclude that no transaction data within a single block is being double spent, i.e. That that information is globally unique only in that one place.

Speaker 0: 00:26:56

We don't specify exactly how a client would read the block.
But you could imagine that they get the block, parse it as a list of transaction as in Bitcoin, and then they just go from top to bottom, read through the witness part, find the nullifiers, and then whenever they encounter a nullifier, they insert it into the nullifier key value store.
So if there is actually a duplicate nullifier, some duplicate coin ID somewhere later in the block, then the receiver would have already inserted that coin ID into the nullifier store, and then they would ignore this second nullifier completely.
Does that answer the question?
Okay.

Speaker 2: 00:27:45

Is that something that's further discussed in the paper or maybe like would be an addendum or something?
Yeah, the question is, are those specific details included in the paper or maybe something to follow up with and further specify?

Speaker 0: 00:28:01

This is definitely something that someone needs to figure out exactly if they wanted to implement this.
But the paper is more abstract than that, I would say.

Speaker 3: 00:28:14

How does one recognize a nullifier?
Is it like super obvious?
I mean, that could be a censorship problem, or is it like, oh, we're just gonna evaluate every signature on the blockchain, and if it's a, you know, it could be a nullifier, or it could not be, we just store them all?

Speaker 0: 00:28:31

I haven't thought much about it, because, like, I don't know, you could imagine there's some magic bytes somewhere in the witness.
There's these envelopes for inscriptions that I don't know much about for how to inscribe data in the witness part.
I don't know exactly how that would look like.
I guess there are many degrees of freedom how to actually do that, but...
I don't see a way how you would...
You have to store them all forever, right?
Sorry?

Speaker 3: 00:29:01

You have to store them all forever, I'm guessing?

Speaker 0: 00:29:04

Yes, right.

Speaker 3: 00:29:04

So you probably don't want to store every single Schnorr signature, just in case it happens to be a nullifier.

Speaker 0: 00:29:12

Yeah, it's correct.
Ideally you don't want to store garbage, but yeah, not sure how to best prevent that because it's easy for someone to create something that looks like a nullifier but is not one and you have to store it.

Speaker 3: 00:29:25

If you do put a magic byte on it, then there's gonna be some people that are gonna be like, oh, we must censor those things.

Speaker 0: 00:29:31

Right, yeah, but you still need to verify this aggregate signature for the nullifier, so random data will not have a valid aggregate signature.

Speaker 4: 00:29:51

Is there something in the nullifier that binds it to the recipient?
Because what prevents Alice from handing the exact same data to Bob and exact same data to Carol at the same time and they're both referring back to the same nullifier.

Speaker 0: 00:30:09

So I mentioned that, so we have transactions and transaction outputs.
Transaction outputs are accounts or coins, so we care about coins, and coins consist of amounts and public keys.
So the public key would be Alice's public key.
Although it's a little bit different in the shielded protocol because we have this concept of an account ID, which is actually a public key.
And you use that, your public key identifies your account, and in order to create an address, you produce a hiding commitment to that account ID.
So you can produce as many addresses as you want from your account ID, they are unlinkable.
You can post them on your website, whatever, give them to the sender, and then the coin actually does not contain the public key, but rather this hiding commitment.
And then if you want to spend the coin, you need to open it and show this is my account ID that corresponds to my account state, which is also input to the transaction.

Speaker 4: 00:31:22

In a sense, the coin, we have like a parallel chain of digital signatures that's kind of being embedded in the coin history.

Speaker 0: 00:31:38

Can you make the question more precise?

Speaker 4: 00:31:40

Well, like one, the blockchain itself is a chain of digital signatures, right, where you have...but each transaction is signed over to the next public key, which is signed over to the next public key, and so on and so forth.
So it seems like we have this parallel ledger that's being sent alongside, that's being embedded in the primary ledger, I guess the 0.5 layer.

Speaker 0: 00:32:16

Yeah, that's one way to think about it, right?
There exists this transaction graph, this separate transaction graph, but what is important is that no one knows it because there are just these coin proofs and you don't learn about the transaction graph, right?
You just get a proof, the transaction graph is correct, and here's my coin and the coin is correct, but you don't know the transaction graph.
But it exists in some space.

Speaker 5: 00:32:48

Maybe ask Jesse's question again.
So suppose that I double spend.
So I send the same coin to you and I send the same coin to Jesse.
And I or a publisher, I guess, publishes a transaction or a new nullifier for both of those.
Presumably the nullifiers would be distinct.
So at what point would it be noticed?
Like what's?

Speaker 0: 00:33:14

So The nullifier won't, so the nullifier will potentially be distinct.
Remember, it consists of these two parts, coin ID, transaction hash.
The coin IDs will be the same, otherwise they don't spend the same coin.

Speaker 5: 00:33:27

Awesome, the nullifier identifies what I'm spending, but not where it's going.
Go back to the slide.

Speaker 0: 00:33:39

Yeah, let's go to the toy nullifier, not the actual one.
Oh no, this one.
The nullifier contains a transaction hash, and the transaction hash commits to the receiver.
Because the transaction, just like a Bitcoin transaction, the transaction has inputs and outputs, and outputs, there are coins, some outputs are coins, potentially coins contain amounts and a public key or an address, explained earlier.

Speaker 5: 00:34:20

Okay, that helps.

Speaker 6: 00:34:25

Okay, so you're posting a nullifier to the chain with a signature attached.
Is that signature signed with a key that's linked to an identity like account, or is that nullifier scoped, or are you using like a re-randomizable signature scheme like Zcash?

Speaker 0: 00:34:43

It's more simple than that.
So you don't, obviously you don't use the same public key all the time.
This would defeat the purpose.
But what you do in an account state update is you essentially, let's go maybe one Here.
Nullifier public key, I didn't want to mention that.
So what you do in account state update is you commit to your next nullifier public key, which you will use to nullify the next account state.
And then you produce a signature for that nullifier public key.
And you can draw the next nullifier public key essentially at random.
And thereby this is unlinkable.
Yeah, The account system is a bit difficult to, definitely a bit difficult to wrap your head around, but it really helps because then we only have to post one nullifier per transaction to the chain, which is really nice.
All right, so let's give one more big round of applause.
Thank you.

Speaker 1: 00:35:53

Thank you.
