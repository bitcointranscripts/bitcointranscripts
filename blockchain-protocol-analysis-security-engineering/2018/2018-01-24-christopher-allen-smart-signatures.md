---
title: 'Smart Signatures: Experiments in Authorization'
transcript_by: Michael Folkson
tags:
  - cryptography
  - simplicity
date: 2018-01-24
speakers:
  - Christopher Allen
media: https://www.youtube.com/watch?v=E9sbWKbfyJU
---
Slides: https://www.slideshare.net/ChristopherA/smart-signaturesexperiments-in-authentication-stanford-bpase-2018-final

## Intro

Good afternoon. My name is Christopher Allen, I am with Blockstream and today I wanted to give you an introduction to something that isn’t about consensus, isn’t about proof of stake and other things. I want to pop up a level. I want to talk about smart signatures. These are a number of experiments in authorization.

## Digital Signatures

First we need to recap, what is a digital signature? It demonstrates the validity of a message. It was invented in 1976, the year before Star Wars came out. It was patented in 1980 and the patent expired. It was made practical by Rivest, Shamir and Adleman in the RSA algorithm and became part of the standards world in 1988 using the X.509 Digital Signature Standard. The fundamental architecture of digital signatures has not significantly changed in over 40 years.

## Traditional Digital Signatures

The traditional digital signature, it validates the message by canonicalizing it. It hashes it and encrypts it with a private key and it validates it with a public key. These are then embodied in various certificate data formats, the most popular of which is that original one, ASN.1 which is a data format standard from the 1970s I believe originally, and the X.509. These certificate are then signed in turn by hierarchies of certificates and finally confirmed by a trust policy. This is where things often break down.

## The Trust Policy

What are trust policies? Right now our trust policies are defined by a certificate authority or actually in reality by the app, a browser or the operating system. The trust policy is not defined by the signer who basically signs these things, nor the verifier who is trying to determine that things are all correct. Is the intent of the signer fully expressed? I’m not sure. Does the verifier understand the intent of the signer? Probably not. Does the CA or app understand the trust requirements of the verifier? This is the thing that I think is most important. No I do not believe so.

## New Kinds of Signatures

Another challenge for traditional digital signatures is that modern crypto is allowing a lot more new forms. We have multisignatures being talked about tomorrow in Pieter Wuille’s and Andrew Poelstra’s talk. We have ring signatures by Monero, by our own products at Blockstream. Blind signatures of different forms, aggregated signatures, confidential signatures etc. The traditional digital signature data formats have had very difficult times adapting to these new forms.

## Traditional Authorization

So we have to look at the root. What is the traditional digital signature doing? What is its core use? Its core use is for authorization. Basically a trust policy ensures that the conditions have been met for a particular task. Have we gone through and authorized this party to have access to this website or whatever? The traditional digital signature authenticates that a specific party signed a message and then certifies that the signing party is authorized to do the task. That is the real challenge. Is the signing party actually authorized to do that task? I think we can do better.

## Smart Signatures

This is where we come up with this concept of smart signatures. Its core use is also for authorization except instead we are using scripts. A smart signature has additional parties that can be authorized. The parties can offer delegation services, you can say that somebody else now has the privilege to be able to do this. We want to be able to support AND and OR expressions. We want a lot more kinds of conditions.

Fundamentally the difference between a traditional digital signature and a smart signature is that the trust policy is not interpreted by a CA or in code executed by an app, browser or OS. Instead the trust policy is embedded by the signer into the signature itself. This concept was come up with at the Rebooting Web of Trust in the fall of 2015. Some of the contributors early on include Greg Maxwell, Pieter Wuille, Ryan Shea, Joseph Bonneau, Joseph Poon, Tyler Close etc.

## Our Inspiration

Our inspiration was the Bitcoin transaction signature because it works. It uses a stateless predicate language, sometimes known as Script. The script is created by the signer and it is based on the signer’s trust policy. Thus can support ANDs and OR and multisigs, various complex things like timelocks and puzzles and even other scripts. There are many, many use cases.

## Use Case: Multifactor Expressions

What are some of the use cases? Clearly the most important one right now is multifactor expressions. We want N of N signatures, M of N signatures, we want the logical ANDs and ORs. There may be other elements we want to be able to include. Biometric signatures, proof of hardware control etc.

## Use Case: Signature Delegation

We want to support signature delegation. We want to be able to delegate to another party and we want to limit that delegation. We want maybe to say that somebody can use it for a month, for only purchases and purchases not more than 5K dollars. We also potentially want to have the ability to permanently pass control to someone else in case usage of a key ceases. This could be because of an employment change or because of some significant scenario like disaster or death.

## Use Case: Multiple Combinations

We want to be able to combine these in multiple and interesting ways. For instance in a development release or a continuous integration toolchain it might have at the top level a multifactor 3-of-5 signature. One of those 5 signatures has authorized their assistant to be able to do the signing for the development release because he is on leave. Another signer has a very strong security policy that requires 2-of-2 keys to be applied to the signature where one of those keys is stored on a hardware token.

## Use Case: Transactional Support

Finally we want to be able to support transactions because that is one of the primary uses for authorization. Signatures are often part of a larger process. They can prove that specific transactional states exist before they proceed. We want to be able to test against various oracles. For instance we want to be able to say “No more than 5K has already been spent this month” which means it needs to know how much has already been spent by other authorizations in the history of the smart signature. There may be other uses such as provenance, a piece of art requires a transactional history in order for you to be able to purchase it.

## Requirements

Looking at a lot of these different usage scenarios we have come up with some requirements for smart signatures. I will divide them into two big categories. There are requirements around the language and then there are the requirements around the system.

## Requirement: Composable

The first requirement is composability. A smart signature language should be something that allows you to take simple behavior, small things, well described, well understood and build them into more complex ones. We really need to have simple data structures, stacks, lists etc. The reason why we have both of those requirements is that the constrained set of operations allows us to do sufficient security review to understand what is actually going on, that errors are not being encountered. Our inspirations around composable languages are Forth, Scheme, Haskell etc.

## Requirement: Inspectable

The second requirement is inspectability. This is really about the programmer, the developer. We want the script to be understood by a qualified programmer. We want those elements of the signature script to be brought out and exemplified so the developer can actually know this is what it is going to do and how it is going to function. In the end the programmer has to evaluate is this going to do the business function that I want to have authorized.

## Requirement: Provable

A third language requirement is we want it to be provable. A smart signature language should be formally analyzable to prove correctness and it should support a variety of expert tools to discover hidden bugs. Those are the three language requirements.

## Requirement: Deterministic

We have three system requirements. The system as a whole needs to be deterministic. The script should always produce the same result even on a different OS or hardware. I might even add if in the future there is a new version of the script language it should still function.

## Requirement: Bounded

The second system requirement is that it should be bounded. Execution should not exceed the appropriate CPU or memory limitations. The script size should be minimal in order to limit bandwidth and storage costs. To go back to the previous requirement, in order to do this bounding those bounds need to be deterministic. These all interact with each other.

## Requirement: Efficient

Finally there is a requirement of efficiency. We are not putting in requirements on the difficulty for creating signatures. In fact if it takes several seconds or even longer to create a signature that is acceptable. We are really concerned about efficiency, the cost of verifying should be extremely low. These are all of the primary requirements that we want to have in any smart signature system.

## A Challenge: Privacy?

I do want to add in something we were considering as a seventh requirement which is privacy. There is always a trade-off between flexibility of a sophisticated smart signature and the privacy that it offers because every time you do a signature it is revealing information about the signers. That is certainly a lesson that we have learned from Bitcoin. Smart signature functionality may allow for correlation. In some scenarios that can be bad. In particular in transactional scenarios it reduces substitutability and thus it can break fungibility and various bearer aspects of authorizations. I don’t consider privacy to be a requirement but it is something that you should carefully consider. Some advice, limit sharing of the smart signatures themselves, execute them offchain as much as possible. If you and I have a contract then we don’t need everybody else to see it unless there is a problem. Be transparent and very deliberate in your privacy design. Think about privacy as one of your considerations.

## Experiments: Bitcoin Script

There have been a number of experiments in this area. Obviously the most successful experiment is Bitcoin. It is securing billions of dollars worth of transactions. Bitcoin Script itself is a Forth like language in that it is stack based. It is well tested, well trusted but obviously has some limited capabilities. This is a good thing from a security review perspective if it is going to secure these billions of dollars. We have to be very careful about what we put in it. There are some things coming out, MAST, Schnorr and other improvements that will continue to help Bitcoin. It is a great starting place because we have demonstrated the deterministic aspects. We have demonstrated that that is possible. We have demonstrated that it is bounded, we have demonstrated that it is efficient. What we have not demonstrated is that Bitcoin Script is very composable, being able to combine scripts in various ways is hard. It is definitely not very inspectable. Most people can’t look at a Bitcoin script and say they know what is going on. It is not at this point provable, we cannot have a formal proof of Bitcoin script.

## Experiments: Ivy

There have been some experiments to extend Bitcoin Script. The most notable is [Ivy](https://docs.ivylang.org/bitcoin/) from chain.com. It compiles to Bitcoin Script but it has a much easier syntax. It adds named variables, it adds static types. This makes it an inspectable version of Bitcoin Script. Other than that it has the same limitations that Bitcoin Script does, mainly that it is not provable.

## Experiments: Dex

The first attempt to take smart signature requirements and come up with a language for it was the Deterministic Predicate Expressions [language](https://petertodd.org/2016/state-machine-consensus-building-blocks) by Peter Todd. In it he discusses a Scheme-like lambda calculus that is really optimized for hash trees which among other things allows for partial proofs which I think is kind of cool. I can give you a long Dex predicate that you may only be able to solve a small part of it. You can collapse that to a hash, give it to the next party who is able to take a different part of it and collapse it to a hash. Bring it back to me and I can prove that the particular authorization is allowed without necessarily knowing all the other aspects. It is specifically designed to support state machines and systems that need state machines. It is composable, it is deterministic, efficient and bounded. I am not quite sure about its inspectability or provability. It is strongly typed and with some additional work is probably provable.

## Experiments: Simplicity

One of the most interesting experiments in smart signatures is Russell O’Connor’s [Simplicity](https://blockstream.com/simplicity.pdf) which is from my company, Blockstream. It is a sequent calculus which a lot of people may not be familiar with, which offers finitary functions with bounded complexity. It allows you to create scripts that are very solidly understood. It already has a formally provable semantic and scripts that are written in Simplicity can be provable via the tool called Coq. Of all the different experiments right now it is the most provable, deterministic bounded, efficient, composable. Where it is challenging is that it is not very inspectable at this point. Maybe as it evolves we will create higher level things that allow us to do it but I can’t look at a Simplicity script and have an intuitive feeling “Here is the expression of the intent of the author of this script and what it is going to do.” You are going to hear a lot more about this in a session tomorrow where Russell (O’Connor) is going to [talk](https://diyhpl.us/wiki/transcripts/blockchain-protocol-analysis-security-engineering/2018/2018-01-25-russell-oconnor-simplicity/) more about Simplicity.

## Experiments: Sigma State

Another experiment is [Sigma State](https://github.com/ScorexFoundation/sigmastate-interpreter) by Alexander Chepurnoy. It uses sigma protocols which is a class of digital signatures and crypto systems that are optimized for ZK proofs. Some interesting things about it is that it supports natively ring and threshold signatures. It is different than a lot of the other languages. In order to support hopefully ultimately provability it does have strong types and some other features. It looks like it is reasonably inspectable, composable, should be able to be deterministic and efficient. At this point he doesn’t have a formal proof of the language itself so the path to provability is still to be determined. I personally have some questions about the boundedness of it. It is supposed to be non-Turing complete but there may be some accidental Turingisms in there.

## Experiments: Michelson

[Michelson](https://tezos.gitlab.io/whitedoc/michelson.html) is the next experiment that I am finding interesting. It is by Tezos. It is in the Bitcoin family of being stack based but it is using OCaml as its language mechanism. It is very strongly typed, it is composable, inspectable and efficient. At this point there are not strong proofs for it but I believe that it is provable and is likely bounded and deterministic in the same way that Bitcoin is. There are no formal proofs of that at this point.

## Experiments: Crypto Conditions

This is radically different. This is not a script but this is another approach of addressing the constraints problem. Crypto Conditions is not a language, it is a JSON description of a number of keys. This allows you to do a very deterministic boolean algebra. The advantage of this particular technique, it is very easy to test does this code properly express the intent of the user because it is all deterministic boolean. We can test the hell out of it and get a real thing but it has no flexibility at all. It either fits into the JSON format or it doesn’t. It is bounded, it is efficient, it is deterministic. I find JSON a little bit hard to read but that is ok. It is in the questionable category. It is explicitly not composable. There are no composable elements of it and I don’t know how to prove it either. I can test it but I can’t necessarily prove it.

## Experiments: Status

What is the status of these various experiments? Obviously Bitcoin Script is fully integrated in Bitcoin but at this point there is no standalone version. You can’t take the Bitcoin Script interpreter and use it. There is an open source project from kallewoof which is called [btcdeb](https://github.com/kallewoof/btcdeb) which is a Bitcoin debugger. I notice that the latest version of it adds MAST in one of the branches. People can begin to experiment with extending Bitcoin Script. Ivy has a full white paper and a full script playground available where you can try out various Ivy functions. There is even now a Ivy to btcdeb branch going on right now so you can actually debug Ivy. Dex, Peter Todd has written a blog post about it and done a couple of presentations but at this point there is no white paper and as far as I know there is no implementation. It is interesting as one of the first attempts in this area but there is not a lot you can do with it at the moment. Simplicity which is again going to be talked about Russell tomorrow, the white paper is available, I have seen some people try to do some things based on the white paper but there isn’t any public code yet. It is coming but it is not available. Sigma State, the white paper is supposed to be out next month. I don’t have all the details. There is no public code out but he has been working on some. Hopefully we will know more about the state next month. Michelson has a white paper, has a script playground, you can definitely do some things with Michelson now. Finally Crypto Conditions, it is part of the Interledger reference release and they are in the process of standardizing Crypto Conditions.

## Watching: Smarm

I am watching some other efforts. These aren’t necessarily experiments. Smarm, Christopher Lemmer Webber has been designing Scheme like language that is maybe going to be on top of Simplicity when Simplicity comes out. It allows some of the Scheme composability and those elements at the top but compiles to Simplicity. It can also compile to native code so it is an interesting effort. At this point we only have a requirements document for that but presuming the requirements are met it would be composable, inspectable, deterministic. Can the proofs move up from Simplicity to it? At this point there is no formal description for that so I don’t know yet. It is at least an interesting project worth watching.

## Watching: Frozen Realms

[Frozen Realms](https://github.com/tc39/proposal-ses), this is part of the ECMCA, the Javascript community. It is by Miller, Morningstar and Patino. It is a safe subset of Javascript with limited primordials, it may compile to WASM. I just think there are some interesting things we may be able to learn from this language. It is certainly composable and inspectable in the same way Javascript is. Will it ever able to be provable? I’m not sure. Finally it is a Turing complete language so boundedness is always going to be a challenge for Turing complete languages. You can do it with gas and other mechanisms but you can’t prove it.

## Watching: Bamboo/EVM

In the Ethereum community there is a high level language called [Bamboo](https://github.com/pirapira/bamboo). It is Javascript like, like Solidity and such but it very much tries to call out the explicit state transitions which is one of the classic bugs that happens when you are doing Ethereum contracts. It tries to avoid reentrancy. I am very interested in it from an inspectability point of view. Are they allowing the programmer to more explicitly understand the various reentrancy issues that you have with any kind of asynchronous script. That is why I am watching Bamboo. Not on there, I have not studied the KEVM which is also trying to do provability of the EVM layer of Ethereum.

## Open Questions

The community that is beginning to work on these, we have a number of open questions. One area is the area of context. In Bitcoin the context is the previous transaction. You start with the previous transaction, you have a script and then it executes. With smart signatures we want to be able to refer to things. We want to look at a transaction and go “It is 5000 dollars but the script says you can’t do 5000 dollars.” Those messages might be lists, they might be trees or they may even be very complex acyclic graphs. How does the script refer to the contents of the message that it is signing? There is also runtime context? What is the time, what is it being executed by, what information needs to be passed and is available to the script while it is executing from the runtime? If you think about it from Bitcoin’s perspective we know the block height. There are a variety of different things that can be passed to the script that allows it to do its functionality. When we start talking about stuff that is outside the message, the external process state, Bitcoin script does not have access to the whole blockchain. It can’t know that that particular set of keys was used in another transaction elsewhere. It can only know that it wasn’t used with the prior transaction. How do we handle external process states? This leads to this larger problem of oracles. Anytime you have this asynchronous state we end up in much more complex territory. How do we preserve the execution boundaries when we’re in these asynchronous states? In the same way we have constrained Script to be predicate expressions what are the simplest minimal viable product oracles that are out there? Obviously we need a time oracle, we may want some Bitcoin price oracles etc. How do those work, how do we want to assure them etc? There was a big long discussion by the smart signature team around revocation. Revocation turns out to be a really hard problem. I think originally Pieter Wuille and Peter Todd were both saying that it should be able to be in the primary script. You can have the revocation as an AND type of operator inside the script. I think we are all in rough consensus that likely revocation cannot be done directly within in a signature script. How are we going to do revocation? Do we want some kind of proof of non-revocation as another script? We are not really clear here. Clearly one of the answers is to make the scripts very short lived. Maybe a day, a month or whatever. That way you don’t necessarily need to do revocation.

There is another system security architecture than what is popular today called object capabilities. How many people here are familiar with the concept of object capabilities? It is a very minority architecture. It has been in development for over ten years. It has some very interesting properties. It turns out that ocap and various Least Authority architectures may really benefit from smart signatures. If we are going to add that as another use case we need to understand their requirements more. It may enable some of the types of things that they wish to be able to do that can significantly increase the security of our systems. Another open question is the cryptographic primitives. What do we want to include in our smart signature system. If we look at Bitcoin a lot of the underlying operators were deprecated because they caused various kinds of challenges. They could allow an attacker to do a denial of service by using up a lot of memory etc. Do we want to offer some cryptographic primitives? I am personally interested in the script being able to directly derive HD keys. I think that would be a very useful primitive. Andrew Poelstra has been talking at various conferences about scriptless scripts where we are embedding into a single signature multiple signatures in a form that resembles simple script operations. Can we leverage that? That gives some privacy, it may give us some other capabilities. Then there is this line between the smart signature and the smart contract. A smart signature is a predicate script. It is returning TRUE or FALSE. Is there some value in some non-predicate scripts where we are providing TRUE and FALSE and maybe a hash or something of that nature. There are some interesting open questions there. Then of course all of these experiments are not Turing complete. They are very much exploring the efficient and bounded side of things by not attempting to be fully Turing complete. But where is the line between a smart signature contract and a true smart contract? Is Turing the only difference between the two? Are there a lot of things we can do without becoming fully Turing complete? Unknown at this point.

## References

https://github.com/WebOfTrustInfo/rwot1-sf/blob/master/final-documents/smart-signatures.pdf

https://github.com/WebOfTrustInfo/rwot2-id2020/blob/master/final-documents/smarter-signatures.pdf

References, the most recent paper is Smarter Signatures. That will get you the paper that was published last spring. You can obviously look at the tag \#SmartSignatures in Twitter and you will see other discussions about it.

## Are you a Language Geek? Come to the next Rebooting Web of Trust

But we are evolving it. The concept came up at the first Rebooting the Web of Trust. We are going to have our sixth Rebooting the Web of Trust in Santa Barbara in a few weeks, March 6th - 8th 2018. If you are a language geek and this is something that really gets you excited. You go “That experiment is BS.” I want you to come to this event and tell us what is wrong and help us fix it. I would like to really begin to explore some of these use cases, these requirements and actually begin to have some more solid demos of what the future of smart signatures is.

## Christopher Allen

My name is Christopher Allen and you can reach me at ChristopherA@Blockstream.com

## Q&A

Q - It is still early in terms of experiments so you don’t want to have a standard but is it possible to have a kind of extension to X.509 certificate to include smart signature language constructs including the data structure and syntax?

A - There has been some exploration of how we can extend existing digital signatures with some of these scripts. To a certain extent you can just put in the signature field, the script and all of the predicate expression. I am more interested in what is happening in the W3C. There is something called the Verifiable Credentials, Verifiable Claims community. They are using a special form of JSON that is a graph JSON, it is called JSON LD. It can be signed as a graph signature which is I think very intriguing. I am more expecting that the innovation in this space will evolve in the JSON LD signatures area rather than the X.509.

Q - This signer’s policy is kind of like a self sovereign identity. The holder of the key can decide the policy. uPort, Consensys, they have a decentralized identity focus group. Are you guys talking?

A - I coined the term “self sovereign identity” and Rebooting the Web of Trust is where the decentralized identifier spec was first bootstrapped. The decentralized identifier spec allows multiple blockchains to create decentralized identifiers that can be used for a variety of purposes including self sovereign identity. On Ethereum there is uPort, there is a Bitcoin version of it, there is BigchainDB. There is a public but permissioned blockchain called Sovereign which is also using DIDs. We are meeting every Tuesday morning to try to move that forward in the W3C.

Q - A smart signature is a predicate language but you showed Simplicity and I thought that Simplicity was more than that?

A - Simplicity is more than that. To be clear it is not Turing complete. It unwinds all the loops and all the different aspects of it so you can have a complete expression. I think for what most people want to use it for right now is for things like provable predicate scripts. Clearly it can be used for more than just a predicate. Again it has the same open questions. When we start hitting various levels, once we start talking about asynchronously having scripts talk to each other we run into all the problems that we already know about from the Ethereum world of reentrancy and things of that nature. There is still a lot of work to do.

Q - What is the relationship between your work and the Sovereign Foundation?

A - I am not part of the Sovereign Foundation. They are part of the Rebooting Web of Trust community. They are one of the many different people that cooperated at Rebooting the Web of Trust to incubate the DID standard. Then last June the W3C gave permission to move forward as a work item. It is not on a standards track right now. It is in the first stage. We had a big meeting last week to try to reconcile the last draft. Hopefully this year we will be moving to standards track where it will become a potential international standard.

