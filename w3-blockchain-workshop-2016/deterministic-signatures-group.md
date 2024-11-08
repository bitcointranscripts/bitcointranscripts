---
title: Deterministic Signatures Group
transcript_by: Bryan Bishop
tags:
  - threshold-signature
---
Deterministic expressions (group)

So please give your name and organization and what would you like to hear in the next twenty or thirty minutes.

ECDSA threshold signatures. Signature systems. Multisig predicate expressions.

- new crypto systems
- build pipeline things, gitian things
- git signatures
- interop
- smart signatures
- "crypto conditions"
- ECDSA threshold signatures

<https://github.com/WebOfTrustInfo/ID2020DesignWorkshop/blob/master/topics-and-advance-readings/DexPredicatesForSmarterSigs.md>

<http://diyhpl.us/wiki/transcripts/w3-blockchain-workshop-2016/christopher-allen/>

<http://diyhpl.us/wiki/transcripts/w3-blockchain-workshop-2016/petertodd-dex/>

<https://petertodd.org/2016/talks-dex-arnhem-dev-workshop>

<http://web.archive.org/web/20220119164821/http://www.weboftrust.info/downloads/smart-signatures.pdf>

Probably what people are least familiar with is crypto conditions. I am going to say a tiny bit about it. Rather than a more flexible language, it's more of a struct that basically it's a structure in which you can put a bunch of isgnatures in a variety of ways such that you evaluate the struct so it's more of a, it's similar to DEX except there's a few features it doesn't have, like it doesn't evaluate external inputs, like "is equal to some value you pass in". It's a formalized language for encoding an expression of a signature or crypto operations or pretty much the same thing. It's an entirely deterministic way to pass around this stuff so that it doesn't matter what language or platform, the result is always going to be the same, it's an essential primitive for the interledger thing, we think of it as a provable event, you need to prove the event happened, you prove it by providing a signature that fulfills that condition.

There was one thing that interledger did differently. You had some prefixes in a fashion such that you could rapidly interpret that you can't do this part of the tree. There were bitmasks upfront. It would specify what operations are going to be used, so you don't have to unpack the whole thing to be able to decide whether you can evaluate.

Would the bitmask overconstrain it? I mean, look at the multihash people, that explodes in size. So if we have 8 bits, will we have a collision there? The thinking in interledger here was that if you, it's flexible, so you can add new bits and new flags and say here's a new operation, and by default if you don't know what that flag means, then you don't know what that flag means. This registry getting big is the concern, of all these operations you have to maintain.

If there's a huge fragmentations operations, it's going to create a fragmentation of support, and the chances are that if you're passing around a condition, fewer and fewer people will support it. The network and system users will start to get fragmented as you increase the number of capabilities required. It's highly likely that most people will support all the common basic ones. There's a good argument for keeping this to hashes at first, and then later introducing more common stuff. You have to balance this with future flexibility.

Could it be served, my next question is, could that be served by a a global, get a hint that, individual substructures have the hints so that you can find the one you can do? You have a prefix, which has a condition, then you have a bitmask, and in this condition there are a bunch of operations being used. Perhaps this should be combined into a versioning notion? There is a version bit, but you could use that to offer different structural features, rather than purely would you be able to evaluate a specific signature type.

So, to you, it's, we talked about needing to have some kinds of hints for typing and other stuff. Is there something we could put upfront somehow that allows a hint as to what operands are inside? My thinking with this stuff is that, at most, you really only want to have, you definitely want to have the actual expression language be as simple as possible. Avoid having to bump the version. As an example, at the level that all the data is hashed, you could only .... you could try to support as few crypto primitives as possible, and after that the particular use case you might have, might have a standard, if I'm going to sign an email then maybe I will have a standard for which parameters would be passed into an email predicate expression. This would be separate from the actual evaluation engine. We wouldn't want to have to bump the version on that thing too often.

Let's say you have a CHECKSIG as an opcode, then it basically receives a multi sig, the thing that Juan has been working on, a signature that has some kind of, on the signature a pre-pended type. And, that's a Schnorr signature, and another one would be a DSA, RSA, ECDSA of all those different things. Is it better that checksig could look at the value and just check the sig, or is it better that it's CHECKSIG ECDSA? Well, you might end up writing an expression that explicitly does an ECDSA CHECKSIG, because you need to gain compatibility with another scheme, interface with a piece of hardware of another type of signature. Given that, and the fact that regex is fast especially compared to crypto, if an opcode is CHECKSIG RSA, that means you just do a regex on there, and then you do the CHECKSIG...

I could write an expression that did the thing that ... and then calls ECC CHECKSIG or RSA CHECKSIG or whatever, and package that up as a self-contained expression. We can take something like DEX and wrap it in an encoding format. So you can save yourself the regex operation and just have a prefix format with bitmasks. So then you would have a bitmask for all the opcodes. In the encoding format you could optimize pretty heavily. You looked at crypto conditions much earlier, right? It wasn't as flexible, but there were some other clunkiness that I think you were worried about?

Is there a subset of DEX that we could say, doesn't necessarily require full interpreter to do, but would allow us to encode something as a proto-DEX that something could run? OP_NOPs? You could define something as a DEX expression, and implement that as a hard-coded thing. You could go and build up an expression which actually compiles straight to code.

One of the crypto conditions objectives was legacy. The classic problem is that a bank has a bunch of signatures that are RSA and from a legacy system, on a 5-year old HSM that they are using. They might have an OR to a more efficient EC system, but they might want it to be an AND. They start with an OR condition and they say starting in 2018, we're going to start putting ANDs in there, and in 2020 we are going to eliminate RSA but still have all the artifacts of that. But have the artifacts be inspected in the future.

More complex parsing tasks wont be possible. If you try to write an XML parser in DEX, literally the number of operations that you will need to be able to do to express something from an XML expression, there might be no way to express that in a language like DEX, and if you did that anyway, and if you had up to 100 million different computations. SSL, wayback when, we didn't actually in the reference implementation parse ASM.1, the ASN.1 was so constrained in early certificates that we basically, in effect, hard-coded hte reading and did not parse.

Yes you could do that with DEX. You know that the thing you are taking in might be this data structure, you could check that the bytes are in the right place, and we have met the subset of this complex standard, and maybe someone spits out a signature in a wrong format, and the system fails.

What's key for us is that you never have a false positive. In interledger, you set up all these transfers which are on hold, so if a ledger has said great I have setup a transfer in the middle of this chain and I will be able to evaluate thisc condition, and then the evaluator comes back and says sorry can't evaluate, then that's a failure. It's esesntial to the protocol that if you say you can evaluate the fulfillment that you can actually validate the fulfillment. Before you, you're looking at the conditions, this is what the fulfillment will look like, and when I get it, I will be able to evaluate.

Crypto conditionals doesn't do pruning, it doesn't have a merkle tree type of concept within it. You could represent a crypto condition in some basic DEX code as long as we avoid certain operators that are more complex. And put some sort of prefix field in it to give the hint that's necessary. All of the things could be represented.

Why does the system know what the time is? It's a time oracle. DEX .5, which might meet crypto onditions requirements, but does not have tree pruning or oracles, but meets hteir needs, it would be conformant and a DEX 1.0 could read it.

Signature validation might be more interesting if you have roots of trust. Because of how the pruned stuff works, you can emulate a traditional PKI with a root of trust. But you could also emulate a web-of-trust, but you could also emulate new structures that are not Certificate Authority design. Web-of-trust becomes a UI level thing where it's never going to be reasonable to write a DEX expression that has a trust metric on its own. I can use the expression to evaluate all the web-of-trust signatures. Which ones to trust? You're constructing one of these expressions saying, as the author, I have these requirements. And then I pass it to you, and you have to meet these requirements to do this.

I might go and trust different people than you do, so there's no way to come up with a common expression that we will both use. The idea of PKI si that you would agree because you agree with the root. But in web-of-trust you don't agree on the root.

We have been talking about mail and messages, but it's basically a proof. With hyperledger, ideally, and talking about the hyperledger ideal and not the current implementations, you should be able to plug in different consensus mechanisms and different business mechanisms, and what they would all have in common is that they can send proofs to each other, and then you need a deterministic system for shared proofs. In the current hyperledger fabric project, is not that this. Their architecture is not compatible with that. How do you get atomicity across both systems, and they both have to agree on the same proof evaluation, and you need an absolutely deterministic condition to define the condition and this is where crypto conditions comes from. The protocol coud potentially be something like multi-protocol ideal like IPFS has made, where as long as you both support the format, it could be DEX, crypto conditions, or it could be a hash.

My thinking in how DEX is designed, comes mostly from Bitcoin Core, which is that writing code that evaluates these expressions however they are done whether through more complex systems or a script or something, is difficult because you and I have two different implementations, we're going to be both duplicating work. I would rather do duplicate work on something simple, and then just pass around code, like the Java virtual machine concept. In interledger, your receiver defines a secret, they provide the hash back as part of the condition, and then this releases all the payments. Can you do hash locks in this? Yes. You could write a DEX expression that returns true if you provide the preimage to the hash. The absolute most simple example is a hash lock.

In interledger, we are debating whether crypto conditions are even necessary. It's highly likely that 99% of transactions that hashlocks are enough. Something more complex might occur in a more atomic way. What if we gave you a very well defined hash lock as DEX where we say we're not going to change that, you don't have to actually create an interpreter for DEX, because we're giving you a standard. If you see something that doesn't look like a hash lock, just say you don't support it. The right way to do this is to come up with a format that can evolve without breaking all of the old implementations and then start really simple because of the fragmentation problem. So you want everyone to say they support hashlock.

There is one issue with hashlock which requires that the system can enforce publication. There are systems that cannot do that. In interledger, the hash lock creator requirement that sender and receiver can communicate. If you as a sender want to blindly send and know that the receiver will get the money, you have to have at least their public key. In early bitcoin there were early standard bitcoin transaction. In the early stage, what if we say here's some pretty standard things that will meet your needs and some other needs, and then you don't necessarily have to have us to have a final DEX functional language for you to be able to start parsing this and using it.

The power of the language you could still achieve with limited primtiives, just PKI hashes and the ability to OR and AND them together, you can already do a whole bunch of cool stuff without having to require complex implementations. Once you nail down the design, the actual implementation is going to be simple to do.

If you have an interface layer between what the string signature is, and what the rest of your code does. When I go check the signature, first I check that it declares various fields, like I made the claim that the message body had this hash, or the subject line had this hash, then you could pair this with your application's internal representation of an email or a payment. I don't think you can get away from this. If I have an email client and I have some code that I, I need to put... in the condition itself, you define a way to evaluate inputs, while you're trying to fulfill the condition. This is what is emerging with the json-ld thing.

In bitcoin, the signature hash algorithm takes in a transaction and does some validation, it's a canonical transaction and some sort of normalization, and then w. . SignatureHash or transaction signature digest algorithm as jl2012 called it. Bitcoin Core didn't make this a standard of the

We have a language that has expressions evaluating to true or false. In the smae way that something can say that there's an RSA signature here, just replace it with a DEX thing and it has an RSA signature in it. But, that, are there languages per se that W3C has defined? Are there data formats? W3C tends to be at a higher different level. There are data ontologies, sparql and query languages that fit within W3C before. Would this be something that W3C would consider to be better with IETF? With crypto conditions, even though most of the stuff was in W3C community, then it seems more likely to be a fit for IETF instead. IETF for protocols and W3 for application layers. IETF has HTTP and W3C has HTML. But there's of course a grey area.

Interledger needs this, like crypto conditions, and DEX is talking about it in the future of json-ld signatures because of verified credentials people. IETF has some baggage in the sense that they are wanting to, they are avoiding anything that has to do with RDF or acyclic graphs or any of that. I'm not sure I can get that through. IETF is also maybe avoiding the build system use-cases as part of that.

You should be ready with action items at 12:45. I hope you had a productive discussion and that everyone spoke.

There are a variety of protocols that exist today that have a field that say "it's a signature". In many cases you can drop in a DEX, because just like a signature it evaluates to true or false. It would have a lot of compatibility with existing protocols to say that version 0 is a signature, version 1 is a smart signature and allows for a richer level of complexity. It's an abstraction layer on signatures, to make multiple signatures look like a single signature. For interledger it's for legacy payment systems where they only have single signature support, but they put this abstraction layer upfront and maybe for a while it's still the old signature, but then maybe over time they support an OR system or something, and over time they can migrate to better crypto systems.

This is not about identity, it's about a cryptographic primitive. Instead of at the application layer you need to pick which signature you're using, you just say this is what the signature is. This could also be backwards-compatible with old signature systems.... PGP would be an example. Some of these things ignore data at the end of what they parse. PGP is an example of htis where you can take two PGP signatures and concatenate them and git doesn't even notice.

What does this need from standards? Interledger wrote a standard, but we need to look at the DEX things and some of their features. We could add these as optional, or debate whether they are needed. Maybe standardize this, as an encoding format for a lambda expression language where the opcodes are all crypto algorithms basically. That's basically what we're standardizing. There are two examples of that, and we should probably come towards something that we could standardize on. The lazy option is, encoding format with a prefix that says what follows is DEX and what follows is an interledger crypto conditional.

When you do this as a simple language, then you can have, you could review the implementation of the language especially since this is a functional composable language, it's easy to do a security review of the language with a structure you know they might have 10 or 1000s different ways that people take that structure of an RSA signature and interpret it through a variety of different things. It allows a greater level of security because it allows it to be more easily reviewed in the longrun.

The motivation for not going to a turing complete language was the security complexity and security evaluation. A lambda expression based language, or something. This DEX is not actually really turing complete. You have effectively done the same thing. It's in some sense a structure that can have a reference to another structure in it, and you can recursively apply rules. My structure might be, there's an AND structure and two other structures and AND it with two other structures.

In terms of standardization, it's important that it does not compromise the determinism of the system. I haven't thought about it hard enough because I only just saw the presentation. What is the impact of external inputs? How do you manage the deterministic nature of those? There might be something wrong with how you check the signature against an external thing, and maybe the part we screwed up with is in the browser we had some memory where we check the URL against the signature, I'd be much rather to screw up there rather than something more fundamental.

What next? The key output right now that cryptoconditions and DEX can probably figure out how to work on. 17th July there will be a conference in Berlin.  Stefan will be there, he is the brains of crypto conditionals.
