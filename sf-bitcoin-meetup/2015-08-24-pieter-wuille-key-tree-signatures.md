---
title: Key Tree Signatures
transcript_by: Michael Folkson
tags:
  - research
  - cryptography
date: 2015-08-24
speakers:
  - Pieter Wuille
media: https://www.youtube.com/watch?v=gcQLWeFmpYg
---
Slides: <https://prezi.com/vsj95ns4ucu3/key-tree-signatures/>

Blog post: <https://blockstream.com/2015/08/24/en-treesignatures/>

## Intro

For those who don’t know me I’m Pieter Wuille. I have been working on Bitcoin Core for a while but this is work I have been doing at Blockstream. Today I will be talking about Key Tree Signatures which is what I have been working on these past few weeks. It is an improvement to the multisig schemes that we want to support. This is an outline of my talk. I’ll first talk about multisig support in Bitcoin, K-of-N threshold, I’ll go into that later. Then I will talk about what if we restrict the problem to just 1-of-N, see if we can improve that. Then alternatively look what if we want just K-of-K where everyone is a signer and improve that. Combine the two approaches that gives us a better K-of-N. Then generalize this into something we are calling Threshold trees and then finally talk about some future work.

## Why multisig?

Multisig, this is the mechanism where you have transactions that need to be signed by several keys in order to unlock some funds. There are different use cases for this. One is multi device security where I create a transaction on my laptop but I am not quite sure about the security of the system so I would like to require a signature by my phone as well so an attacker would need to compromise both my phone and my computer. Another reason for doing this is a low trust escrow. If you require 2-of-3 signatures, one of them is the sender, one is the receiver and a third is an escrow service which gets to sign off on who gets the funds whether the goods were delivered or not. This is an improvement over the traditional escrow system where the escrow just gets the money and can run off with it. This is an escrow who gets decide who gets the money but doesn’t have it themselves. Of course whenever you have shared funds some company holds money that not just a single person should be required to unlock them.

## OP_CHECKMULTISIG properties

In Bitcoin this is implemented using OP_CHECKMULTISIG which gives N public keys and requires K signatures with it where K is between 1 and N. In Bitcoin N in this case is in practice limited to 15 keys due to the restrictions of P2SH, pay-to-script-hash addresses. It has a downside that validation performance if such a CHECKMULTISIG transaction is being used on the blockchain depends on the number of keys. If you do even a 1-of-15 multisig it can require up to 15 signature checks that everyone in the Bitcoin network will have to do. This is a resource constraint which is not nice. The storage size, you need to publish the full public keys and signatures into the blockchain. This is linear in K and N. This means that even if the restriction of these 15 keys was lifted there is really no way of doing thousands of keys involved. The transactions would be huge.

## ACE UP

Gregory Maxwell a while ago [came up](https://diyhpl.us/wiki/transcripts/gmaxwell-bitcoin-selection-cryptography/) with a number of interesting properties that this sort of signature scheme can have. He called it ACE UP. Accountability, composability, efficiency, usability and privacy. I will go over the properties for CHECKMULTISIG in Bitcoin, at the end of the talk I will refer back to them with the new scheme we have constructed. Accountability is the ability to see who signed off to spend the funds. If you have a 1-of-10 signature scheme where anyone in a company can spend the money and suddenly the money disappears you probably want to know who spent it. Composability is if you want to receive money from me but you would like me to send funds not directly to a single key of yours but to a multisig scheme. Now I want to create a more complex transaction that either pays to you with your multisig or to someone else. Can I improve the scheme and combine the two? This is something that traditional Bitcoin multisig cannot do. You cannot do 2-of-3 or another 2-of-3. It has to be represented as a single one. The efficiency, as I said is linear in K and N which is not very good. Usability is pretty nice in CHECKMULTISIG. Someone creates a transaction without signing it, broadcasts it to everyone, everybody signs it, you bring the partially signed transactions together and the result is a fully valid transaction. You don’t really need one round. Then there is the privacy. This is something where CHECKMULTISIG is really bad. Everyone can see all the public keys involved, they can see what the actual policy is. You cannot hide the fact that you are using a 5-of-8 and maybe it is known that you are the only real user of 5-of-8 keys in Bitcoin. Now everybody knows it is you. Let’s talk about how we could potentially improve this.

## Better 1-of-N

First of all let’s restrict the problem to just 1-of-N. If we think about what is a 1-of-N multisig scheme all you need to do here is have a set of public keys, choose one of them, create a signature with it and then prove to the blockchain or your consensus system that the key used was part of this set. There exists a solution, it has already been deployed within Bitcoin to prove membership of a set. It is called a Merkle tree. In Bitcoin it is used to prove to SPV nodes that a particular transaction is part of a block. I will talk about Merkle trees.

## Merkle tree

The idea is you start with a bunch of leaves, in this case keys, you take their hashes, and you combine them pairwise to produce a higher layer of hashes. You start with a layer of 8 possibilities, combine two of them together into the hash of both, this results in 4 hashes. Then you take two of them together to produce two hashes again and you combine those together to create a root hash. Anyone can then prove membership of this root and I will show you how.

## Program

```
Check(root,h3,b3,h2,b2,h1,b1,x):
    if (b1):
        swap(x,h1)
    x = SHA256(x,h1)
    if (b2):
        swap(x,h2)
    x = SHA256(x,h2)
    if (b3):
        swap(x,h3)
    x = SHA256(x,h3)
    return x == root
```

This is a program in pseudo Python style coding. The question is given a root and a leaf, prove to me that that leaf is actually part of the set was that hashed to construct this root. x is the leaf in this code. It takes as input three booleans to determine which direction you are going up and three hashes that are being combined. I will go over it. Say we want to prove that k4 is part of the root, I publish k4. I also publish k3 and a boolean to say k4 is the second here. You combine those two together to recompute D. I also give you C and say it is left of it, hash those together to produce A. Then I publish B and say it is on the right of it, hash them together to get the root and you verify this root matches. You can see that this is three times the same step we are doing. We start with the leaf, combine it with something to produce a higher level hash and repeat this. Not going into the details but this is the program. The question is could we potentially implement such a program to run inside Bitcoin scripting language because we don’t have a native construct in Bitcoin to do so? We can almost.

```
					r,h3,b3,h2,b2,h1,b1,x
SWAP IF			r,h3,b3,h2,b2,h1,x
	SWAP			r,h3,b3,h2,b2,x,h1
CAT SHA256		r,h3,b3,h2,b2,x
SWAP IF			r,h2,b3,h2,x
	SWAP			r,h2,b3,x,h2
CAT SHA256		r,h2,b3,x
SWAP IF			r,h2,x
SWAP			    r,x,h2
CAT SHA256		r,x
EQUALVERIFY
```

This is a literal translation of the program from one side to the other. Unfortunately it requires this CAT operation which is concatenation. This was an operation was disabled in Bitcoin years ago, 2009/10 for fear of DOS potential. However in Elements Alpha, our first technology demo sidechain we reenabled this OP_CAT. This was actually accidentally made a general improvement, I think Patrick did that. Then later realized that this actually enabled the implementation of these Merkle trees. On the right you can see what the stack is. I won’t go through the details but if you are interested you can go through it and see that it actually works out.

We can use this. What someone would do is publish a public key, publish this path along the Merkle tree to prove that it results in a root hash. Then publish a signature with that public key and all you need to do is verify that the Merkle branch results in a hash that is equal to the root and that the signature checks out with this public key. We have combined the checking that the public key is a member of the set and actually doing a signature check with it. This has very nice performance properties because what ends up in the blockchain is just a single signature check. Plus a bunch of hashes. They are much faster to validate than a signature check. This results in logarithmic storage size. Every layer in the tree you add doubles the number of potential keys. You can create something with thousands or hundreds of thousands of keys and only have a few levels in the tree. Why would someone want a 1-of-N scheme? It is not typically something that is being used. One use case is honeypots. If say you have a server farm with 10,000 machines and they all have a wallet. You want to see whether someone breaks in. Perhaps you want to give a certain incentive for an attacker to steal the money that is there. Say I have for my 10,000 machines 10 Bitcoin at my disposal that I don’t care about, that I am willing to lose if that means I can detect an intrusion. In a normal scheme I would need to put 1 millibitcoin on every machine and it is very unlikely that an attacker would find this interesting enough to steal. However, if you have a 1-of-N multisig scheme with 10,000 keys you can share your 10 Bitcoin over the entire set. Every machine would have full access to those same 10 Bitcoin. If a single machine is broken into presumably they steal the whole thing. At the same time because of this accountability property that this also has you would know which machine was stolen. You would give a separate key to each of them.

Q - How many keys? I thought you could only use a certain number of keys with multisignature?

A - In Bitcoin’s CHECKMULTISIG you can but using the approach I have just shown here you can build a Merkle tree with 10,000 keys at the bottom and the tree would only be 14 levels deep. It is a few hundred bytes to do this. This is a logarithmic storage size which this approach has. You only publish a single signature and a single public key and then in logarithmic space you can prove that it is a member of this huge set of 10,000.

Q - How big is the script to do this?

A - It is six operations per level. Six bytes per level plus you would publish one hash per level for the branch and one boolean. 40 bytes that get added per level that ends up in the blockchain. Per signature but you only do one. For now.

## Better K-of-K

The next step. What if instead of just one signer we want everyone to sign? It turns out for this there is also a solution. I will briefly will talk about Schnorr signatures now. They are pretty much ECDSA as they should have been. Unfortunately Schnorr signatures were patented at the time when ECDSA was being standardized so the world on using ECDSA. But ECDSA is pretty much a workaround for the patent that Schnorr had. Schnorr is faster, simpler, it has a stronger security proof, it is provably non-malleable. It supports batch validation, recovery, the properties we would like to see in ECDSA. The patent did run out I think in 2009. There is no reason why Bitcoin couldn’t have used it from the start except ECDSA was the standard so let’s use that. However the reason that Schnorr signatures are interesting, they also support native multiparty signatures.

## Native multiparty signatures

A multiparty signature is a scheme where different participants jointly construct a single signature. This is exactly what we want for this K-of-K. Here is an example with four keys. They would all produce a nonce, which is actually similar to a public key. They would publish their nonces. They would all combine everybody’s nonces into a combined nonce. Everyone takes this nonce and uses it to produce a partial signature. Then in a second round you would merge all these signatures together to produce a joint combined signature. This combined signature is now valid for the sum of the public keys. This really results in an amazingly performant multisignature scheme because what ends up on the blockchain is a single signature check. People don’t even see how many keys were involved. I want to send a transaction to you, you and you. I want you three to sign to unlock it. I would send my coin to the sum of your public keys. In order for you to unlock it you need to collaborate using this two round scheme I gave to produce a signature. None of you need to reveal your private keys to each other. This is K-of-K and it does it in constant size and constant verification time. The only downside is that it requires two rounds because you first need to publish the nonce.

Q - Schnorr signatures, you don’t need to have them in order. You don’t need to know what the order of the keys are, with ECDSA you need to know the order of the keys.

A - With ECDSA you only have a single key. But using a CHECKMULTISIG construction you need to obey the order and the order is irrelevant here, that is true.

## Better K-of-N

To combine these we have one scheme that allows us to produce a Merkle tree to prove membership of a large set. Otherwise we have a mechanism for taking several keys and making it look like a single key. To combine these two you create a Merkle tree where every leaf is one of the potential combinations you want to allow with different public keys.

## Example

For example if I would want to do a 2-of-4 signature this has 6 combinations for 2-of-4 keys. I have listed them here k1,k2 and k1,k3 and so on. You turn this into a Merkle tree where in every leaf you sum up all the involved keys, take a hash of it, work your way up to the Merkle root and you send the coins to a Merkle branch verification plus a single signature check.

## Performance

The performance is still nearly constant validation time because there is only a single actual expensive signature check involved though there may be several levels of hashes which are much faster. The space required for this sort of mechanism, the amount of data this requires on the blockchain is logarithmic in the number of combinations of keys. The signing time is linear because during signing you need to construct a Merkle branch. In order to do so you need to know the entire tree. This is unfortunate as there is a certain overhead to computing the sum of the public keys in each of the leaves.

## Number of combinations

Here is a table of all up to 20-of-20 keys, I don’t know if you can read the numbers of how many combinations exist. For example if I want to do the worst case, a 10-of-20 which is 184,756 combinations. I would construct a Merkle tree with 184,756 leaves each of which is the sum of 10 public keys out of 20. Add them together, work all the way up to compute the root which would in this case 18 levels. You need to iterate through these 184,756 combinations in order to compute the Merkle root or the Merkle branch during signing. In practice that is two seconds.

Q - With this property of summation of public keys with Schnorr what is to stop someone from doing an attack where they forge a key by generating a whole bunch of public keys and finding a way of summing those to the thing they want to do and signing the ones that they generated?

A - Public keys have 256 bit entropy in them. It sounds like you are trying something like a collision attack which would have 2^128 in order to pull off.

Q - There is an attack that your implementation avoids, I don’t know if we will talk about it tonight?

A - I might mention it later. Try not to distract too much.

Up to numbers like this, this is perfectly viable in most use cases at signing time. If you would go up to say 1 billion combinations the signing time or constructing the address requires probably several hours of computation though it is parallelizable too. That is a better K-of-N.

## Threshold trees

We are not actually in this scheme restricted to just doing K-of-N. We are constructing a Merkle tree in which each leaf is some combination of public keys. It is really just a means of describing a particular condition over what public keys we want to allow. There is no reason why this policy is limited to K-of-N. We came up with this idea of using a threshold tree which is a tree structure in which every leaf in the tree is still a public key and every inner node is some combination, n out of the levels below need to be satisfied. OR is the same thing as only one has to be satisfied, AND is all of them have to be satisfied but you could just as well use 2-of-3 or whatever. The description I give here is an OR of an AND and a THRESHOLD of a AND.

`OR(AND(k1,k2,k3), THRESHOLD(2,k4,k5,AND(k6,k7)))`

This just says “Either k1, k2, k3 all sign or 2 out of k4, k5 and a combination of k6 and k7 have to sign. You can construct arbitrarily complex descriptions like this. This is a universal scheme so any monotonic boolean circuit of conditions you would want to allow over sets of public keys can be represented by this. Only AND and OR are sufficient but by adding this threshold ability K-of-N it is much more expressive.

## Implementation

https://github.com/ElementsProject/elements/pull/48

This is implemented. You can look at the source code of it. It is not yet merged into Elements Alpha but we will probably do so soon. You can create such a description of AND and OR and THRESHOLD of different public keys that you want. It will compute the address for it, allow you to send to it, allow signing it, transferring the partially signed transaction for it around and result in a valid transaction. A few interesting implementation details here. All of it works in logarithmic space. Even if you have a description that results in let’s say 1 billion combinations, those 1 billion combinations are never fully materialized in memory. How does it work? It iterates over your description tree to produce one by one the different combinations in a lazy way and then there is a Merkle root and branching algorithm that will consume these to produce a Merkle branch of a Merkle root. It never keeps all of these in memory at the same time. This means that all this code can reasonably run on low power, low memory devices which is something you usually want for multisig schemes. It is tested, at least once.

## Properties

Let’s go back to the ACE UP properties that I mentioned in the beginning. The accountability property, can the participants see who signed off? Yes because it is obvious from the signature, you can see which position in the tree your leaf was. The participants in the transaction know the full tree so they know what it corresponds to. This is the same between CHECKMULTISIG and these tree signatures. Composability is obviously much more powerful. I can take two trees and I can combine in arbitary ways, by construction this is what it does. Efficiency, CHECKMULTISIG has faster signing because you don’t have this iterating through all combinations thing. Though tree signatures have faster verification. This is what we care about in resource constrained blockchain systems. Then there is the usability. It is similar except tree signatures have two combination rounds due to the requirement that people first publish their Schnorr nonces and then combine them together, sign and combine again. The privacy argument, if I want to hide my policy or even better I want to hide who is involved in the transaction, what keys are, the way to do it in all of these schemes is by adding dummy keys to it. In CHECKMULTISIG this is extraordinarily expensive to do because we are only limited to 15 keys entirely. Though in tree signatures I can easily double the number of keys and only add one level to the tree.

## Log-log scale graph for signature size

I will show you some benchmarks. This is a graph that shows the size of the signature as a function of the number of keys involved. For tree signatures the worst case is where K is half of N. 10-of-20, 5-of-10, this results in the maximum number of combinations. Those are the red lines. For CHECKMULTISIG the worst situation is where you have the number minus one. 19-of-20, 9-of-10 and so on. That is the blue line. The dotted lines are CHECKMULTISIG and the full lines are tree signatures. You can see it that there is not a single case where CHECKMULTISIG is better. I do need to point out that this a logarithmic scale in bytes. 100 kilobytes is the largest transaction that can fit in a Bitcoin block. That is the limit. It is also not entirely honest to say the full red line goes up there because the signing time is exponentially related to the size of the signature. The largest one up there would probably require more computation than the universe can do in a reasonable amount of time. It only goes up to around a kilobyte.

## Log-log scale graph for validation time

This is a graph for the validation time of both. CHECKMULTISIG is the dotted line that goes diagonally while the two lines below are tree signatures. In microseconds, it goes up to 0.1 seconds for validation.

Q - Where is the dotted red line?

A - In CHECKMULTISIG the validation time depends on the number of public keys and not on the number of signatures. The dotted blue line and dotted red line coincide. Also the place where the red line visibly goes above the blue line is not interesting because it is infeasible to construct such large signatures.

## Future work

This was threshold trees which is what we have implemented. To briefly say something about future work here. All of this is implemented in Elements Alpha, our sidechain, but we had to use an emulated construct to validate Merkle trees. This is not a native feature in the scripting language. It is slightly inefficient and a side effect of what we can do. It is perfectly possible to create a specific opcode in Bitcoin scripting language or Alpha scripting language, that takes a Merkle branch and validates it. It is interesting to see that this is only a soft fork. That is something that could relatively easily be added to Bitcoin if there was demand for it.

Q - Would it make sense to actually build this in natively so there is pay-to-merkle-root of script hashes instead of pay-to-script-hash?

A - Next point. In addition to native Merkle branch checking to be able to get this to work in Bitcoin we would also need Schnorr signature support. That too is possible with a soft fork and would bring in several other advantages like batch validation. Batch validation is where you take a bunch of signatures and you verify whether all of them are valid or at least one of them is invalid. There is a factor of 2,3 speed up to get over a single validation. It is exactly the thing we want in Bitcoin during block validation.

A next step and this is actually an idea that is much older than all of this work, Merklized Abstract Syntax Trees. We are not really limited to producing a single balanced tree of combinations of keys. We could in fact restructure this scripting language entirely to be tree shaped where you have AND and OR things. You can put “check a locktime”, “check a signature” and all sorts of complex conditions that you can write but structure them as an abstract syntax tree. You have just some expression that defines the condition for spending something using signature checks and whatever. Then turn this expression into a tree, an OR or CHECKSIG A, CHECKSIG B would be a tree like I’ve shown. You put Merklization directly onto this tree. Every node would get a hash associated with it that depends on the hash of the leaves below. This basically allows you to build a huge script of different conditions and only reveal the part of the script that you are actually using to satisfy. That would be the next step. Not something that is easy to do here but I am very interested in working on that. It is like doing P2SH recursively. You pay to a hash that reveals part of a script and part of that is again a hash which reveals a part of a script and so on.

Q - I’d point out that with MAST this big tree of signatures can be this big tree of instructions saying “If this returns TRUE check these three keys.”

A - Turning the actual script into a tree rather than just the keys.

Other work is other efficient signature schemes. The mechanism I have presented here is very good for certain use cases but it is not good for others. You cannot do 50-of-100 due to the combinatorial explosion of combinations. Even though the signature would in theory be small and the validation time would be small it is completely infeasible to sign this. There is other work that Greg refers to in his [talk](https://diyhpl.us/wiki/transcripts/gmaxwell-bitcoin-selection-cryptography/) such as Polysig which is a mechanism that is very efficient for K-of-N where K is really close to N. Or if you don’t care about the accountability property, if you don’t care about seeing who signed there is ring signatures which have similar compact representations.

## Q&A

Q - Once you have calculated a complicated tree is there a way to reuse the root for multiple payments? Is it safe to use it directly or would you want to somehow hide the fact it is going to the same place?

A - Ideally you would never reuse a single key in the first place. If you care about this sort of privacy which you should then it is a non-issue because you are using new keys. However it is true that you could have a single dummy key that does not have a corresponding public key involved and anytime you reuse it you change the dummy so it is not recognizable that it is the same only due to the path being similar.

Q - When you mentioned the other efficient signature schemes what about the one that is like threshold signatures from Princeton? You may have meant that when you said Polysig?

Greg Maxwell: That is referring to the ECDSA stuff. The problem with the existing ECDSA efficient signature schemes is they require many round trips to complete. We think this is less exciting because it makes it very hard to build useful applications out of them. When you have to do round trips multiple times, you have six devices and you have to visit each one six times. If they are in safes you are about to shoot yourself.

A - Tap your phone, tap your phone again, tap your phone again.

Greg Maxwell: But with a ten minute wait as someone else taps their phone.

Q - For the Bitcoin blockchain it is ECDSA but there are other blockchains. Eris can be configured for ed25519 which is Schnorr signature native.

A - I think ed25519 does not support adding public keys together? It has a requirement on a particular bit being set.

Greg Maxwell: This will work in Bitcoin eventually. This is a trivial soft fork. ed25519 breaks hierarchical wallets. It breaks the addition with standard implementations. The curve is fine.

Q - Have there been simulations done to see if you have filled a block with CHECKMULTISIG in maximum case how long the verification would take?

A - You would fail because there is a limit in Bitcoin.

Q - The 100 kilobytes?

A - There is a sigop limit. There is a limit in Bitcoin that limits a single block to at most perform 20,000 signature checking operations. However this is computed in an inefficient way. A 1-of-20 multisig which can go up to 20 signature checks will always be counted as 20. You can only do 1000 maximum size CHECKMULTISIGs in a Bitcoin block.

Q - Why was the cap taken out for… and why are those problems not relevant on a sidechain?

A - Imagine a script, push a byte, DUP CAT DUP CAT DUP CAT, this blows up your memory usage in an exponential way. You take the one byte, you duplicate it, you have two arguments of one byte, you concatenate it together, it is two bytes now. Duplicate two bytes, four bytes. This was a time in Bitcoin when there were several vulnerabilities being discovered and presumably at the time this restriction on disabling the CAT opcode was intended to be temporary except it now requires a hard fork to reenable.

Greg Maxwell: There was an attack that you could cause many petabytes of memory usage in the system, it was a real attack, nobody exploited it but it existed so the opcode was disabled to be sure there was no attack.

A - So the obvious question becomes why did we reenable it because it is side limited? Any CAT that would result in a size over 520 bytes which is the usual size limit for a script in Elements to fail. We reenabled it in a trivial and safe way. People could have done in Bitcoin at the time too but nobody bothered.

Greg Maxwell: It would take work to check to make sure that that fix was sufficient. When you have a production system that is in danger of being damaged by it you don’t want to spend a lot of time to figure out the fix is sufficient.

A - There were no use cases for it as far as I know. This is one of the first use cases for the CAT instruction. We would’ve found others it was enabled.

Q - Could you talk about some of the use cases for having a multisignature contract with many signatures beyond what Bitcoin can currently support?

A - I mentioned one, the 1-of-n, the honeypot. This is not really about that having that many keys, it is just the number of combinations that blows up even with not that many keys. What other use cases would there be for moderately large multisigs? Some mechanism where you need a majority out of a bunch of people to agree and you want them to all have their own keys.

Q - Stock voting. 5000 shareholders and 4000 elect the board?

Q - I did have one client who wanted this implemented. There are people who are willing to pay money for that.

Q - Can you give some examples of where it would be advantageous to use that Merkle tree structure to create a script?

A - It is advantageous whenever you don’t want to reveal the entire script. This is actually something that is pretty useful. Imagine we set up some complex smart contract that pays out using different criteria. This would be a large signature to satisfy presumably. However using this tree structure you can create something that is an OR of either this complex contract or both of us just agree. When we both agree that the rules are satisfied we don’t need to prove to the world that it was satisfied. We just agree. In that case the entire section of the complex smart contract would not end up on the blockchain at all. You would just send to the root hash of the script and you would just reveal the left branch would be a simple 2-of-2 multisig.

Q - The right side which is the complex contract where would that be? On a sidechain?

A - No. This is completely independent of what blockchain technology we are using. The tree is only conceptual. We jointly construct this tree that describes the conditions under which things get spent. Whenever we sign coins away we reveal the part of the tree that we need. The smart contract could just be a complex combination of multisig that does a check locktime. There are various extensions that could be enabled here.

Q - Do you want to talk about the vulnerability that was potentially avoided here?

A - One of the problems involved here is if you have several people distributing their keys. We want to do a 3-of-3 multisig. You give me a key, you give me a key. I say “My key is the sum of the negation of your keys.” What the scheme would do is compute the sum of those three and my key would cancel out your key. In the resulting key only his is left. If my public key is the negation of yours and we create the sum of the three of them which is what we do with leaves of the Merkle tree, A + B - B, it sums up to A and the result is that just Greg can sign for the three of us. The solution is that whenever these nonces are being published, the nonces themselves are being signed by the keys involved. Everyone can see that everyone else actually has the ability to sign for their own public key.

Q - What do you think about the hard fork?

A - I think we should try to avoid controversial hard forks. I think we should work towards to a solution that the entire ecosystem can support.

