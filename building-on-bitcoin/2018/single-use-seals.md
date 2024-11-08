---
title: Single Use Seals
transcript_by: Bryan Bishop
tags:
  - proof-systems
speakers:
  - Peter Todd
date: 2018-07-03
media: https://www.youtube.com/watch?v=1U-1xkhJeEo
---
<https://twitter.com/kanzure/status/1014168068447195136>

I am going to talk about single use seals and ways to use them. They are a concept of building consensus applications and things that need consensus. I want to mention why that matters. What problem are we trying to solve? Imagine my cell phone and I open up my banking app or the banking app or lightning app... I want to make sure that what I see on my screen is the same as what you see on your screen. We're trying to achieve consensus. For a given state, everyone in possession of it, needs to see the same thing.

In traditional cryptography, this problem is not solved. Signatures are just math. You can sign a message multiple times, and different messages.

So what isn't like this? In shipping, you have anti-camper single-use seal. This means you have a shipping container. Suppose you're in Canada and sending it to Lisbon. When you get this container, there's going to be this seal on it, with a certain number, and when you get that container you should verify the number matches. The guarantee here is that these physical seals there should only exist one for any particular number. No number reuse. In practice, I'm sure that guarantee isn't exactly correct. The other part ofit is that you should not be able to open and close a seal again.

We can take this concept and apply it digitally. Imagine we had some kind of construct for generation, closing, and verifying. Generation would involve associating it with a pubkey or pubkey script or some other form of authentication. You could close it over a message with a signature which validates that message, producing a witness w. And finally verify, which anyone can run, to verify a given message, a witness, and a given seal. This all sounds like a signature, but, what if we add a property where you can't run close twice? What if this was a one time deal? The guarantee we're talking about is that it's secure if there does not exist for two distinct messages, two witnesses that both pass Verify. This is just like a pubkey but we have this guarantee that you can only sign once.

Obviously, we can't do this with math. It's a stateful thing. But if we had this guarantee, what could we build with it?

Well, you could build a blockchain, a chain of blocks. The property you have is that you have a series of blocks associated with a seal. Provided that you start with the same genesis as me, you can validate the witnesses and seals and verify that whatever data you have is going to be the same data that I have. You might be missing stuff at the end, but anything that you do have, is going to be the same as what I have. This is what bitcoin is trying to do in the first place. Same could be done with software versioning-- if we are both running version 1 of a software, and you are running version 1 too, then I want to make sure we're running the same deterministic build as you, and not the backdoored version from the NSA or whatever.

pub struct Seal {
pub txid:sha256dhash,
pub idx: u32,
}

We can use bitcoin as a single use seal. The seal is the txid and a given output number, an outpoint. We can get some code to serialize this and so on. The important thing is that our witness is the transaction spending it, and a blockheight. If you get a little more fancy, then maybe you get a SPV proof saying that the transaction exists.

You validate it, here's one possible way, the important thing is tyhat you come up with some scheme. You have an outpoint, you commit to the message, you do OP_RETURN and commit to the message, there are many variations on this.

This would mean that our blockchain would look like-- what's the target, what's the link (the witness and target), and then a chain which is a target (a genesis) and a list of links. Each one commits to the next seal and we can repeat this indefinitely.

You do have this problem, though, with scalability. Where you're reusing bitcoin transactions. Like with colored coins, every state change, every seal closed, is one bitcoin transaction. Can we do better?

For bitcoin itself, do you actually need blocks to be verified by miners? What if we just agreed on what's in blocks and we re-ran the consensus algorithm ourselves. As long as we run the same algorithms, we can come to consensus. I had this realization a few years ago. My proposal for single-use seals is along the same lines.

Say we had some publication layer, divided into blocks, and we have a new definition of seal which is that it's a pubkey and an initial block. To verify, we take each subsequent block, and we run CheckSig. We can interpret each message as a signature. If the signature verifies or passes, then we say that it's a valid signature and thus the seal is closed. The first signature that is valid is the one that is closing it.

So how do you agree on what the blockchain actually is? We can create a blockchain with a bunch of single-use seals. This is a two-layer system. Imagine taking bitcoin and setting up a sub-blockchain of this proof-of-publication ledger and every bitcoin transaction spent commits to the next block in that ledger. All the data is off the chain, and not on bitcoin itself. So anyone copying the bitcoin chain can't see that data. And this potentially scales. We could imagine, well, why don't we check against multiple messages in this. The first one that is valid is the one that wins.

This leads to a question: can we improve on this even more? What if we had a few billion seals? What if every one was holding the state of every piece of property and parcel in the United States? Well, we would index them.

With a merkle tree, you can take a lot of data and hash it again. But you can also do an indexed merkle tree. If we have a key, and given this tip of the tree, give me the messages associated with it. If we agree on the tip, and everything is hashed, then you and I will come to the same conclusion.

Suppose that I have a seal and you have a different seal... we don't need to have the same data to come to conclusion about the seals. I only need the part of the tree that refers to my seal. This is essentially like SPV proofs where we take a merkle tree and we extract one path from it. Same concept here, we can take a merkle tree with potentially billions of items in it. We can have one path per one seal. My seal might start with bit 1 and yours might start with bit 0 and our merkle path, at the top, will diverge, and we will have completely different data to prove our seals.

How does this scale? For this type of scheme, we need to be able to go prove that each-- we need the transaction outputs for each block... you can imagine maybe 1200 bytes for SPV proof that the transaction outputs are real, plus the transaction itself. If we're talking about 4 billion tiems or seals being closed in every update in each block, there should be 32 levels... so that signature at the end too... and whoever happens to be publishing for that thing. This adds up to be about 3 kb per non-inclusion proof. When this block was created, a vaid signature for my seal's pubkey was not published. And we have to go show that and prove that bit of data was what was committed to, and that ends up being 3 kb. In a real-world sysstem, maybe 12 blocks per day, 3 kb per block, so if I want to prove to you the state of the seal is about 13 MB per seal per year.

Is this practical? The simple answer is sure, why not. 13 megs is trivial. With property titles, and I want to convince that you I owned the house, and i've sold the house to you and I want to prove this and give it to you, I need to give you 13 MB per year of historical data when I owned the house. Or maybe I'm doing something with tokens that represent gold and maybe Tether's certainly existing bank accounts... I could convince you this is true by giving you data that shows that the seal is data. It's only a subset of the total data, thus the system scales.

What's the trust model here? Our definition of proof-of-publication seal.... look at verification. What if you had used the ledger that is now out of operation? Or what if it refuses to give you that data? Well, that's censorship risk. If you don't have the data to prove that you own that house, then you can't convince me of that. So if the ledger doesn't give you that data, you're screwed. On the other hand, can the ledger lie about who owns that seal? Well, they don't have the private key, they can't fake a signature. Bitcoin prevents them from preventing multiple different ledgers because transactions can only be spent once. They can censor you, but they can't lie about the state of the ledger.

The other thing a person could go do, imagine a system where you don't like the given ledger operator. You can close the seal in a way that says you're switching to another ledger operator or some other bitcoin blockchain. Once you have done this, you have the data to prove the status of that token or set of seals, without the involvement of the ledger. Once you have the data, you don't have to go trust them. You could also use a m-of-n seal scheme where they are published on different ledgers. If I had more time, you could go look up my twitter feed, it may offer a solution to the censorship issue. Thank you.

Q&A

Q: So someone is responsible for giving you non-inclusion proofs? How does that work? How much data does that require? And in the non-nefarious case, what does that protocol work?

A: Great questions.

Q: ... tangle...

A: I am building a system that makes the assumption that you have a way to avoid double spending in the first place. I am assuming bitcoin or something like that which can prevent a double spend. Once I have that bootstrap, I can build a bigger system built on, say, bitcoin and provide those guarantees in a more scalable way. Without that base layer, I can't provide any useful guarantees. Maybe some other data structure could work, sure.
