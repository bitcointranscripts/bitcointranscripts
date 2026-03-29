---
title: 'Post Quantum CISA: Signature Aggregation for Bitcoin’s Future'
transcript_by: 'Garvit-77 via review.btctranscripts.com'
media: 'https://www.youtube.com/watch?v=cqjo3rmd6hY'
date: '2025-10-30'
tags:
  - 'cisa'
  - 'quantum-resistance'
  - 'taproot'
  - 'musig'
  - 'op-checktemplateverify'
  - 'schnorr-signatures'
speakers:
  - 'Tadge Dryja'
categories:
  - 'Scripts and Addresses'
  - 'Soft Forks'
  - 'Security Enhancements'
source_file: 'https://www.youtube.com/watch?v=cqjo3rmd6hY'
summary: "This talk introduces a novel approach to cross-input signature aggregation (CISA) designed to work with post-quantum (hash-based) signature schemes, addressing one of Bitcoin's most pressing scalability concerns in a post-quantum world.\n\nThe speaker begins by explaining elliptic curve CISA: in a Bitcoin transaction with multiple inputs from the same wallet, each input currently requires its own signature. CISA allows these to be combined into a single aggregate signature, saving block space. However, with EC signatures at ~64 bytes and the 75% witness discount, the savings are only ~8% in vbytes - modest enough that CISA hasn't been prioritized for a soft fork.\n\nPost-quantum signatures change the calculus dramatically. Schemes like SPhInXs Plus produce signatures of ~4 kilobytes - roughly 50x larger than EC signatures. If Bitcoin ever needs to migrate to post-quantum cryptography, transaction throughput could drop to around 2% of current capacity. In this context, aggregation becomes critical: two inputs aggregated would yield ~50% space savings, three inputs ~60% or more.\n\nThe fundamental challenge is that all existing EC aggregation techniques (MuSig2, FROST, half-aggregation, etc.) rely on elliptic curve math that simply does not apply to hash-based or lattice-based signatures.\n\nThe speaker proposes a new opcode (informally called OpCSIV) that sidesteps this problem entirely. Instead of cryptographically combining signatures, inputs can point to other inputs. One input provides a full signature (covering the entire transaction via SIGHASH_ALL), while other inputs include a hash-based pointer - the outpoint (TXID + index) of the signing input - baked into their taproot tree at address creation time. The opcode verifies that the referenced outpoint is being spent in the same transaction, effectively delegating signing authority without any new cryptographic primitives.\n\nKey design details include: an input index field for O(n) rather than O(n²) lookup complexity; a random nonce for privacy blinding to prevent chain analysis of uncommitted taproot branches; and the constraint that the \"lead\" UTXO must exist before the \"follower\" address is generated. No cycles are possible since outpoints are unique, and there are no replay attack vectors.\n\nWallet integration requires careful design: wallets should embed pointers to currently owned UTXOs in new address taproot trees (limited to ~10 for recovery feasibility), while always retaining a primary signing path so no UTXO becomes unspendable. The approach works best with sequential address generation rather than bulk address pre-generation, and is particularly beneficial for exchanges performing frequent UTXO consolidations.\n\nThe speaker notes that this opcode would be pointless today given small EC signatures, but would be highly valuable if Bitcoin ever transitions to post-quantum signatures."
---
## Introduction to CISA

**Tadge Dryja:** 00:00:00

So I'm going to talk about `post-quantum signature aggregation` and I think the talk will probably not take all 30 minutes, and so we'll have time for questions and stuff, discussion at the end, the sort of layout intro, I'm going to talk about `Elliptic curve cross-input signature aggregation`, `post quantum` or `post elliptic curve signatures` and aggregation, a new potential opcode(`op_civ`) and wallet usage.
Okay, so people have probably heard about `EliCurCroInpSigAgg`, I think people call it SIGAG or EC, I don't know Cross-input signature aggregation.
It's an idea that has existed, around 2018-17, people were talking about it a little bit after SegWit it was like, oh once we do SegWit then we should also do signature aggregation, we can do Schnorr signatures and I think when people were talking about changing to taproot, this was one of the ideas of maybe the taproot software would also have signature aggregation built into it or something like that.
The basic idea is, if you have a typical transaction, we'll have a couple inputs, a couple outputs, right?
Alice is paying Bob and Alice has, let's say, a bunch of `UTXOs` in her wallet and she needs to add up to these three UTXOs to send some money to Bob then she has a change output. So let's say she has input 3, 7, and 8, all three of those UTXOs sign. They create a digital signature and you put the signature in that input. It's kind of inefficient if you think about it, right? Because they're all the same person, it's all the same wallet, you're signing three times, you're attaching these three signatures, every node out there verifies this three independent signatures, Kind of silly.
Why don't we just sign once? Right?
So instead of having three signatures you just have two signatures, And this one signature, right, signature 3, it covers everything. Right? it's not like this signature only covers input 3 and you can malleate or change input 7 and 8, when you do sig hash all, you sign the entire thing, you basically hash all the inputs, all the outputs, you sign the whole thing. So if signature 3 is signing, input 7 and input 8 are stuck there, right?
If you try to change input 7 or input 8, the signature is no longer valid, it seems you can just sign once, right? Problem there.
It's actually not risky for Alice. The problem is, Alice can just point to Carol's input and say, yeah, that's my input. Those are my bitcoins. I'm signing with input three for inputs three, seven, and four. But four is not even Alice's. Right?
It's a totally different key, someone else's money.
It's not just that you have no proof that all three inputs are from the same wallet, right?
So you do need all three of these inputs to sort of sign off on being in the transaction and sign off individually on the outputs, the way `Elliptic Curve crosses input signature aggregation` or `EliCurCroInpSigAgg`, with two inputs you know, A and B, both inputs need to point to the outputs. How do you do that with one signature, though ?Right ?.
Input B needs to sort of sign off on signature A without signing, So the way it works, and this is a huge simplification, is you add the signatures and with elliptic curve properties, you can do this. It's basically **`sig A + sig B`** and that plus symbol is doing a lot of work.
There's many papers and many equations but you can do this, you can sort of combine these signatures in a way where they both need to be signing the same things and if they're not the addition doesn't work.

## Benefits and limitations of CISA

So what are the benefits here? A lot of the benefit is space and verification time as well to some extent, it's not like I have 10 inputs, I aggregate into one signature, okay now the verifier only needs to verify one thing. There's some scaling that does add additional work to the verifier per input but you do save a lot of space, right? And this is interactive aggregation, right? It's not.
There's another idea of non-interactive aggregation, which is like a miner or someone in the mempool, like let's say you see two transactions in your mempool and you say, well, I'm going to aggregate these two signatures Right?
There's like Alice signed her transaction, Bob signed his transaction. I'm going to smush these signatures together and then relay it to my peer and say, well, here's two transactions and I smushed the signature together for you. That, as far as we know, is not really possible with `secp256k1`.
It is possible with some other fancy stuff like `BLS curves` and that would be really cool because then you could aggregate the whole block but this is what I'm talking about is just interactive signature aggregation. It **saves space** I think the problem, one of the this is purely my opinion is one of the reasons it hasn't had as much, you know, work behind it and as much like, oh we really need to get this into Bitcoin, is it doesn't save that much space, right?
The elliptic curve signature is around 64 bytes, slightly higher with pre-traproot, but you know around and so you already have this 75% witness discount, right? So if it's in a witness field it counts as 75% less.
So the 64 real bytes turns into 16 vBytes, for the average transaction, it's around 8% savings in terms of vBytes and there's nice statistics from this Blockstream research. There were people working on cross-input aggregation. I don't want to dismiss it, right?
Because if you're long term and Bitcoin's worth already trillions of dollars and people are using this, an 8% savings on fees could be billions of dollars over the course of years. So I think it's super important and really cool research but at the same time, it's like, well, 8% isn't huge, right? it doesn't seem to be the first thing we have to work on here for scalability and space saving.
So in my opinion, that's maybe why it hasn't had as much drive to get into Bitcoin, now there's a little quantum leap.

### Post-Quantum Signatures need CISA

This people, yeah, there's been talks about quantum signatures a bit, so there's post quantum signatures and I don't, even really like the term quantum. So like, my personal opinion is like, I'm not very worried about quantum computers. I actually think both of these things are unlikely, but it's probably more likely that there will be some kind of regular old computer algorithmic deficiency in the elliptic curves we're using than a quantum computer comes and runs Shor's algorithms, both I think aren't gonna happen, I'm not worried about either, but it's like who knows like someday someone would be like yeah Pollard's Row, we got a better way to do Pollard's Row and you know find private keys from public keys on these elliptic curves and there's a paper and people like oh shoot and you know maybe it starts as like a small speed up but it's like hey this is getting you know getting sketchy we should move to a different you know totally possible that we have to move to different signature algorithms, regardless of whether there's a quantum computer or not. I don't think it'll happen, But just in case, it's good to be prepared and so there's different signature algorithms that do not rely on elliptic curves and elliptic curves are broken by Shor's algorithm if you have a quantum computer.
The main downside is they're a lot larger, they're like 50 times larger, like 4KB~ is the size for the Sphinx Plus.
You can get it lower, so there's that's another interesting part of research is it doesn't really need to be 4KB, could we maybe 3KB? Maybe we can whittle it down to 2k, but that's what we're starting with and I don't see any way you get it down to anywhere close to 64 bytes. So how bad would that be if we had to switch?
You're down to 2% of the throughput rate that you had, So if people thought 1 megabyte blocks were small, now you've got like 50k or something, or less, yeah, so 20k. You're really restricted in how many transactions you can do and that's really bad. So signature aggregation would be amazing if you can do it with post-quantum or hash-based signatures because even with the witness discount, these things are going to be 1 kilovbyte and you'd have instead of 8% savings, even a transaction with just 2 inputs would have something like 50% savings. Three inputs you're getting a 60 something. So, very large savings in terms of how many vbytes you're saving here and, these post quantum signatures, if you did switch, maybe you'd also need to crank up the witness discount. That's a whole other argument I don't want to get into but a way to aggregate these would be really powerful.
So let's do it, Let's aggregate Sphinx Plus signatures, So let's look at how they aggregate the elliptic curve signatures and it's a kind of curve.
But even if you know what all these things and I don't endorse exponential notation I like the multiple anyway but what can you multiply hashes right that's what this big pie thing means you multiply stuff can you I guess you can multiply them? Modulo what? Modulo 2 of the 256? What's the generator point for SHA-256? Is there one? I don't, like, none of this fits, right? None of the techniques that people have been working on for years of all these cool things like frost and roast and music too and signature aggregation, half aggregation. None of this applies at all to hash based signatures.
Lattice signatures as well, although Some people are like, hey, maybe there's a way to do aggregation with lattices. I'm pretty skeptical because I do want to say that with elliptic curve signature aggregation, I remember this in like 2018, everyone thought it was going to be easy, it was like, you just add the signatures. You add the pub keys, add the points, add the R points, add the S, it all works and then it was like many years. There's a reason it's called Music 2, Music 1 didn't work well. Anyway, it was a lot harder than we thought and so I think with a lattice thing where, oh, there's hints that it may be possible.
If it's easy, just add, translates into five plus years of hard work, then it may be possible, it's like, yeah, that's gonna be decades. Anyway, so none of these things fit with hash-based signatures or lattice. Is there another way?

## New Aggregation Variation for Post-Quantum

So, and this is what I came up, I don't know, there's maybe better ways. We don't actually need to add the signatures or combine signatures, right?
What we need is you want the inputs to point to the outputs and so if you think about like `OP_CTV`, if you're `OP_CTV` is object template verify, where you basically take the whole shape of a transaction and put that in an output, that counts, right? That's quantum secure because it's just hash based and you're sort of committing to a whole other set of outputs in a quantum secure way, It's just hash based.
It is sort of like a signature in that sense. It works but it's very inflexible, right? You need to know what you're going to do in order to put that into your output. So it's not really usable for normal transactions because you don't know when you like when you generate an address you don't know where you're going to send money received at that address right?
You're like okay here's a new address give me a Bitcoin, now I need to spend it. Well, if I have to decide where I'm going to spend it, even if I possibly, if I can enumerate, it's like, well, I know I'm going to send it to these three different places and then I could put it into three different little `OP_CTV` outputs in the taproot tree. So you could do that, but that's very restrictive, right?
You generally are like, I want to have the Bitcoin and I want to be able to send it anywhere after the fact.
So the basic idea is that inputs point to other inputs. The idea is if one input signs, all the other inputs can sort of point to that input and say, that guy's signature, now we just need to know about inputs instead of outputs at address creation time, which is doable. So when you're creating an address, you may know other inputs that are going to be spent at the same time in the same transaction. So here's the basic idea.
This is a fully signed Bitcoin transaction, three signatures, three inputs, you take two of the signatures away, and then you put these little pointers.
You say well instead of a signature here in this input I'm going to put a pointer to the first input, input 0, input 3 and same here. These other two inputs I'm spending in this transaction point to the input that has an actual full signature. So how do these pointers work? How does input 2 point to input 0 without signing?
Input, what we do is input 0's out point, so it's, these words are hard, the out point is the term for like the UTXO label, It's just TXID index. So when you create a transaction, it's got a TXID and then let's say this transaction has two outputs and so you'd say, this TXID 0 is this UTXO. This txid 1 is this utxo. So that's called an outpoint.
So the idea is you bake the outpoint of input 0 into input 2's taproot tree and that means input 0's UTXO needs to exist before input 2's address is generated and the way you enforce this is a simplified version, I'll go to the actual version in one more slide, but basically you just have an opcode that takes in an outpoint and says, okay, is this outpoint also being spent in this transaction? If so, great.
You know, success, if not, fail Transaction, you know, is invalid.
That's basically it. It's a real simple opcode, right? You do need to do a couple things.
You don't need to, but the actual thing I'm going to propose, and I wanted to like write up this for the mailing list before this talk, but it didn't quite happen, but I will post these slides and make a mailing list post probably maybe on the airplane back. You want to put two extra things, this input index and this nonce, so the idea is the input index is where in the current transaction that's being validated to look for this output index txid and the nonce is discarded but it's just a random number you can put there and it gets discarded has no consensus meaning for blinding. I'll talk about these two.
The input index is where to look in the transaction. So for example, if we're here, this, you know, Alice input 7, so input 1 in the transaction, would say 0, whatever this out point is, and then some random number because it's like, look in position 0 for Alice input 3, if you don't have this, technically it's O($n^{2}$), because if you have 1,000 inputs and they're all saying, hey, look for these other inputs, then it's technically like each time you add an input, it adds how hard it is to search, So technically $n^{2}$, so you put this, it's like two bytes, whatever, you put that in there and then the nonce, there is a potential privacy leak here, right?
If your addresses are sort of pointing to the other UTXOs that you own, if you use a new key each time, just from looking at the address, you can't tell. That's blinding enough but once you spend it, people are like, okay, I know that key. Let me try to grind through and see what other things he was committing to in this tap tree and so if potentially, you know, that could be used for chain analysis, you know, try to try to de-anonymize addresses. In this case, you're already de-anonymized. You're sort of already saying, yes, these inputs are linked, right? These are the same software or entity or coordinating entity but you might have other things that you didn't link that are committed to, and so you want to blind those. So you put this, you know, 16 random bytes or whatever.
It shouldn't probably be random, it should probably be something like the hash of your private key and that out point that you're committing to, because then it's easier to regenerate after the fact. Yeah, so when you're using it, you'd put these elements in the actual taproot tree.
So you'd have your main key, let's say it's a post quantum pubkey at the top of, I guess if you're using BIP 360, there's not really a top, but somewhere high in the tree, here's your normal signature thing, and then you have some branches down here that have commitments to other UTXOs that you already have, then the input index, you leave empty, so you push that onto the stack when you're spending. So you decide, Once you build your transaction, you start signing it by putting these little indices.
Yeah, so this seems to work. It would save a lot of space. It's pretty simple. Implementation's pretty straightforward, it's probably like 20, 30 lines. 

## Wallet Usage and Implementation Details

The part that's a little complicated is wallets, so the idea is when you're a wallet you have a bunch of UTXOs or you start out with none.
The first time you're making a new address in a new wallet you can't use any of this, right? You just here's a new address I'm gonna use a full signature, full pub key but once you're using this, once you've made a second address and you already have a UTXO, you can point to that. You can say, okay, this wallet takes that UTXO information, puts it in the tap tree. Yeah, wallets should take all asterisks currently owned UTXOs and put them in the tree along with a post-quantum pubkey. You want to make this deterministic, you want to have a forwarder to do this, It does kind of complicate wallet recovery.
So if you've just got a seed phrase and you're using this, you can generate all your addresses but a lot of your addresses will commit to UTXOs and so now you're like, let me generate the first hundred addresses and then, on address 0, I see a UTXO. Well, maybe address 1 committed to that, maybe it didn't. Now I have two different potential addresses there.
Technically O($2{n}$), which is very bad. So you would definitely for larger wallets, you know if you have hundreds of UTXOs, you can't do all of them, right? You should limit it to 10 or something.
Then you've got like a thousand X slowdown for wallet recovery, which is probably fine but yeah, I don't know, do exchanges and people with thousands of UTXOs really care about wallet recovery from a seed phrase? Maybe, I don't know but yeah, so it's doable, but you would need a bit of thought into how you design the wallets for this. Yeah, so the thing is, this would work fine today, you could make this opcode and put it into taproot.
It's probably pointless, because signatures are so small right now. They're 64 bytes and the minimum space to use this would be a bit more, it would be more like 70-ish. So it doesn't get you anything.
I guess it's a little faster to verify, because the verification nodes just look for another input and don't have to do an easy operation. It doesn't save any space but it is much smaller than any known post-quantum signatures. There's some that are in the hundreds of bytes, but the ones that I think people are talking about and looking at as the most likely thing that we would have to use in Bitcoin would be like hash-based, because we're already depending on hash, like the security of hashes for Bitcoin. So yeah, going from three or four kilobytes of this is great.
One of the things you sort of worry about is, well, what about replays? You're not signing. Once you reveal this kind of commitment, could it be replayed? And it's not using keys or addresses.
So one of the things, an alternative you could think of is like, what if your address commits to another address? In this pub key, you say, well, if this other pubkey is signing, that's okay. That counts as my signature.
That would also potentially work, but that would open yourself up to replay attacks, so this doesn't have any replay problems because you're pointing to individual UTXOs. There's no way to make cycles. You couldn't have a transaction with five inputs and they're all using `op_civ` because that would imply a hash cycle. That would mean like, I've got your hash in me, I've got your hash in me, I've got your hash in me.
It's like, wait, that's not supposed to happen with hash functions, it doesn't work well with address reuse. If you just keep reusing the same address forever, well, you can't use this, which is kind of a plus, I think.
It is a little tricky in that if you generate many addresses at once, right? If you're like, I want to generate 100 addresses right now, and then I want to give those all to different people, then yeah, this doesn't really help right ?
Because your UTXOs are all going to be independent, so it works better if you're like making an address, receiving, sending, making address, that kind of thing and you can't really use XPUBs and give it to people. I'm not sure you can do that anyway with post quantum pubkeys. So I'm not sure that's a deal breaker either, but the idea of giving someone a smaller thing and they can just derive a lot of pubkeys from that. Maybe there's ways, but yeah, it's a little tricky.
So those are some of the downsides , no cycles because they're all unique, but yeah, that's pretty much it.
It would work with any signature algorithm. It could do with elliptic curve but kind of pointless, but Sphinx once, lattice, whatever. Yeah, so I think that's probably it.
I'm not like advocating like, oh we need to soft-fork this in or any quantum stuff, but it's just sort of like looking at all these quantum signatures and you're like oh there are a lot of problems here and it's like well if you're going you know if you do end up in a situation where you need to use this I think an opcode like this or maybe someone has a better idea, but something like this would help a lot, right? Because then it becomes very signature heavy.
The witnesses are like 90% of the whole block and it's like, oh, getting down the size with this would be great.
So yeah, thanks for listening. I guess we have a couple of minutes for questions, if people have any but yeah, if you tell me why it won't work or if you have a better way, then great.
Thanks.

**Audience 1:** 00:22:33

Amazing work, Good stuff, Looks pretty cool.
This only works if you, so this is on the transaction level and it would only work for the one wallet right like for integrating aggregating signatures for multiple UTXOs in the same wallet, correct?

**Tadge Dryja:** 00:22:54

Yeah, yeah.

**Audience 1:** 00:22:55

So this doesn't really scale Bitcoin in a way that, say, BLS block-wide signature aggregation would.

**Tadge Dryja:** 00:23:00

No, no, I mean, there's no reason to use it now. It only helps, it sort of like makes transition to post-quantum less horrible.

**Audience 1:** 00:23:09

This could maybe like be good for maybe exchanges?

**Tadge Dryja:** 00:23:12

Yeah, they could save a lot of space, you know, because presumably they have a lot of UTXOs and they're doing a lot of consolidation transactions a lot, so that they would be, when they're the primary, they would save a lot.

Speaker 2: 00:23:23

Okay, the other thing I just want to make sure maybe you can draw your attention to someday is isogeny-based PQC, because it's basically like an elliptic curve is in higher dimensions, you can do things like SIDH and other things, and it might be possible to, it might be more powerful than this, but pretty good work so far.

**Tadge Dryja:** 00:23:46

Cool, thanks.
Thank you.
Oh, and on that, yeah, like CoinJoin is another thing where it's like, you can commit to an input if it's multi-sig, as long as you have one of the keys in there, or, you know, so there's ways to do it, but it's not like, oh, this is awesome, we should use it now anyway. It's more of a, well, if you're stuck going to hash-based signatures, this helps. But today, you don't need it.

**Audience 2:** 00:24:10

How does the rest of the blockchain understand that Alice input 3 and the signature there is good for Alice input 7?

**Tadge Dryja:** 00:24:23

So signature 3 still covers, you know, you're using SIGHASHALL, that doesn't change. So it still covers input 7 and 8. So this signature does sign off on this whole thing happening.

**Audience 2:** 00:24:35

I understand that, but the input 7, you're saying input 7 is using a redirection that is not a signature.
So how does the rest of the blockchain understand that the read let's let's say I Pull in an input that isn't mine What what fails?

**Tadge Dryja:** 00:24:58

Okay, so if you if Alice input 7 doesn't have basically Alice input 7 that address has Alice input 3s UTXO label baked into it if AliceInput7 doesn't have, basically AliceInput7, that address, has AliceInput3's UTXO label baked into it and so it takes, yeah, it's in the taproot tree, right?
So the idea is like, down on the left somewhere, there is a this, like opciv with the txid and index of alicin put3.
And so even if that exists, people aren't gonna know where it is, you know, only the wallet can sort of prove that and show it to the world.
And if it's someone else's address, that hash-based pointer doesn't exist at all, and so you can't show it.

**Audience 2:** 00:25:38

And so that's one branch of the tree, Okay, so I understand.
So AliceInput7 is created, so it's revealing that part of the tree, which is what Alice input 3 in quotes means.

**Tadge Dryja:** 00:25:59

Yeah, it's got the hash of Alice input 3 in it.

**Audience 2:**

Got it.

**Tadge Dryja:**

Yeah, I should make I should have made a little tree where it's like, here's your regular pubkey, and then down here you put your `opciv` clauses.

**Audience 3**: 00:26:09

Yeah, thanks for this great nerd snipe and one thing I was thinking about while you were still talking, for the really, really large wallets, do we run into maximum depth limits of tap trees and also for maybe for efficiency reasons we want to limit the number of UTXOs we commit to and then it becomes a very very interesting problem in which order you have to spend your UTXOs otherwise you make some of them unspendable.

**Tadge Dryja:** 00:26:40

So you would never make it unspendable? So like yes, that's why I sort of put this asterisk, What is the optimal way to do this? I don't know.
I think like yeah restrict it to like pointing to ten because you don't need to point to that many. You only need to reveal one.
So you you don't need to like commit to hundreds because it does complicate also transaction construction where you're like oh I want to minimize my transaction size to minimize fees and like now what you do it's already hard right it's a subset sum problem so it's already like I need to pick all these things to get to the right amount but now you add this constraint of like some of them point to others and so they get free signatures and some of them don't so yeah it's kind of a mess but I would not encourage anyone to say I'm gonna only put OP_CIV spends I'm gonna always have my main signing pub key at the top and then these are options.
So I never get stuck where, I spent all these other inputs, I can't spend this one because the only way I spend this one is alongside these others. So I mean, you could, but don't.
But yeah, but the wallet design and transaction design, that's the complex part. It's not, I don't worry too much because it's like it's complex to optimize right?
If you do it in like a pretty you know oh we'll just brute force we'll just do it like the simple way. It'll work, and worst case, you don't get the space savings you could with the optimal way but yeah, it is like, how should you do this? And that would be a fun thing to work.
Cool. Any other?
Good. Well, next is Floresta stuff, right?
Thanks, everyone.