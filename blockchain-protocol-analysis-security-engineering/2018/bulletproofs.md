---
title: Bulletproofs
transcript_by: Bryan Bishop
tags:
  - proof-systems
speakers:
  - Benedikt Bünz
media: https://www.youtube.com/watch?v=gZjDKgR4dw8
---
<https://twitter.com/kanzure/status/958881877896593410>

<http://web.stanford.edu/~buenz/pubs/bulletproofs.pdf>

<https://joinmarket.me/blog/blog/bulletpoints-on-bulletproofs/>

<https://crypto.stanford.edu/bulletproofs>

## Introduction

Good morning everyone. I am Benedikt Bünz and I am going to talk about bulletproofs. This is joint work with myself, Jonathan Bootle, Dan Boneh, Andrew Poelstra, Pieter Wuille, and Greg Maxwell. Bulletproofs are short proofs that we designed originally with the goal of improving confidential transactions but I'll talk about how they have many more applications and how they are short zero-knowledge proofs for arbitrary computations really.

## Bitcoin transactions

Let me start with some motivations. You've probably seen this if you're in this room. This is what a bitcoin transaction looks like, according to blockchain.info and you can see that you can see which outputs are sent to which other outputs and what the amounts are. To know whether a transaction is valid, there's a simple check that you have to check that the input amount is greater than the outputs and that no new money is created. This is the fundamental validity check of any bitcoin transaction. It actually turns out that the difference between the inputs and the outputs is exactly the transaction fee that goes to the miners.

If we think about it, the validity of a bitcoin transaction comes down to three things. The signature has to be correct, which authorizes the bitcoin transaction was sent from some previous output. The second requirement is that the inputs are unspent. The third condition is that the sum of inputs is greater than or equal to the sum of the outputs.

But we can see that bitcoin is neither confidential nor anonymous. By confidentiality I mean that the transaction amounts are hidden and by anonymity I mean that you can't tell who's sending to whom. Though, people assume in public media that bitcoin is anonymous there has been lots of research that this isn't really the case. You can't see who owns a bitcoin address, so it's pseduonymous, but you can see who is transacting to who and more importantly you can also see how much is being sent. Even if you think about popular centralized systems like Venmo even there you can('t?) see who is sending to who. For monetary transactions you don't want to have the amounts public so that you don't have your salary on the blockchain or as a business perhaps buying tires from another company you don't want to say how much you are paying per tire because these are important business secrets. Without this confidentiality, you're making the blockchain less useful for businesses.

## Confidential transactions

To solve this, <a href="http://diyhpl.us/wiki/transcripts/gmaxwell-confidential-transactions/">confidential transactions</a> were <a href="https://people.xiph.org/~greg/confidential_values.txt">proposed by Greg Maxwell a couple years ago</a>. Instead of sending cleartext amounts, we're going to send cryptographic <a href="https://en.wikipedia.org/wiki/Commitment_scheme">commitments</a>. You can imagine these cryptographic commitments like writing down a number and putting a piece of paper on them in a cryptographic way. Or actually it's more like locking it in a box. Why do I lock the paper in the box? The box isn't see-through so you can't tell what the commitment is, you can't tell how much is being sent. But you cannot open it up afterwards to be something different. You can only open it to the amount you committed to.

## Pedersen commitments

So we're going to use these algebraic commitments called pedersen commitments and the question is now if we have these pedersen commitments then how can we check this validity check and check the signatures and that the inputs aren't spent. But how do we check that the sum of outputs isn't greater than the sum of inputs?

It turns out there's actually a second check that we need to do, and it's trivial, we have to check that the outputs are positive. It's possible to commit to a negative number. But here with the pedersen commitment and there's some sort of overflow but basically you have to ensure that the outputs are positive or within some small range.

## Confidential transactions benefits

Confidential transactions were proposed for a few reasons. They are structured like bitcoin transactions. The transaction amounts are hidden using these commitments. The transaction graph is still public and there's this question of how to verify transaction validity. Here comes a beautiful cryptographic tool to the rescue which is these zero-knowledge proofs of knowledge.

## Zero-knowledge proof of knowledge

A zero-knowledge proof of knowledge is basically I can send that Peggy the Prover can say that she has some commitent to a positive number. The verifier can ask "prove it" and then they can do an interactive challenge-response protocol which might span over multiple rounds which convinces... Victor can ask questions which Peggy will only know if the statement is true, e.g. if x is indeed a positive number in this example. But her answers don't reveal anything about what x is. So Victor is convinced that it's positive and that Peggy must know it, but he learns nothing else. This is called a range proof. You can prove that x is in the range 0 to (2^(52) - 1).

## Non-interactive zero knowledge proof of knowledge

In the blockchain scenario, we're even more interested in non-interactive zero knowledge proofs of knowledge. Peggy can just create this proof on her own and then send it to Victor and Victor is convinced that the proof is correct. It's actually a publicly verifiable proof and anyone can convince themselves that it is correct.

## Homomorphic commitment scheme

So how to do a range proof in this regime? What does it mean that a number is in some certain range? One way I could do that is by decompsing the number into 52 bits or it's in the range 0 to 2^52 so there's a bit representation of 52 bits to do this number. Peggy commits to all of the bits of the number and then sends the commitment for each bit to Victor along with a proof and the proof is going to be that each bit is in zero and one and actually bits. These are so-called homomorphic commitments and Victor can very easily verify that we have a commitment to the-- that they add up, that the sum of the commitments is a commitment to the original value that we wanted to do the rangeproof for.

## Linear range proofs

These are linear range proofs. They are based on <a href="http://www.cs.au.dk/~ivan/Sigma.pdf">sigma protocols</a> and they have been.... and this is what Greg Maxwell originally proposed for confidential transactions. There were a bunch of improvements later. For 64-bit range proofs, this is still 4 kilobytes. If I want to say, for example, double the range or the precision of my rangeproof then I would have to double the size of my proof unfortuntely. The nice property that they have is that they don't have a trusted setup.

## Preprocessing SNARKs with trusted setup

<a href="https://eprint.iacr.org/2012/215">Quadratic span programs and succint NIZKs without PCPs</a>

This is 4 kilobytes. Way too large for a transaction. So how to reduce the size of the rangeproof? If you're in the cryptocurrency space, one very popular tool and one actually amazing cryptographic tool are these preprocessing SNARKs with trusted setup from GGPR 2013. These proofs they kind of instead of doing this interactive protocol or having that non-interactive way... the queries are pre-computed and encrypted using a common reference string. In one setup, I'm going to preprocess a bunch of queries, or someone is going to do that, and then using these encrypted queries the prover can compute a short proof and the verifier can very quickly (having precomputed answers) can verify that the proof is correct. Now we have a short proof that is also fast to verify, and it also turns out that the proof is 188 bytes no matter what you're proving. No matter how long the range is, or if you're proving a more complex statement, then you can provide that proof in only 188 bytes which is quite amazing. You need to do the setup, which is relatively slow. But what is more problematic is that if the setup was-- if someone, someone has to do the setup and for example if the setup was done by someone malicious then the setup can be used or the person who maliciously created the setup can create cheating proofs. For example, I could prove that a number is in the range without that being true.

## Additional problems with trusted setup

This problem can be reduced by using multiple people in a <a href="https://en.wikipedia.org/wiki/Secure_multi-party_computation">multi-party computation</a> setup of the trusted setup together. This is exactly <a href="https://petertodd.org/2016/cypherpunk-desert-bus-zcash-trusted-setup-ceremony">what zcash did</a>. But still there's downsides to it. Because-- which I'll go into a second. SNARKs seem like an interesting candidate. They are very short. The verification is nice, it's 10ms. It's not as fast as we would like it to be. But they have this trusted setup, which is pretty bad. The problem with trusted setup is that-- for example, in cryptocurrencies, such as zcash, or for confidential transactions with trusted setup, if the trusted setup was subverted then we would not be able to tell. They are zero knowledge proofs so a prover would be able to create money out of thin air by just creating new kind of new coins freely and creating more money than he has. But the problem is that nobody would be able to tell. It's not like a break of a hash function where it would be much more likely that we could tell something wrong is going on. But if the zcash trusted setup was subverted then there's no real way of knowing that's the case. There would simply be silent inflation. The prover can create more money, sell the coins, and get revenue from that, and it would be quite a terrible situation.

I'm in no way claiming that this is the case... but the problem is that even if there was a fear that the trusted setup was subverted, or if someone is fearmongering and saying hey you didn't run this protocol correctly, there's no way of disproving that statement and saying "no look at this and everything works" or if you look at the assumptions and if you trust the assumptions then you're fine. There's no way of verifying whether the trusted setup was done correctly, unless you participated in it yourself, which is what zcash is <a href="https://z.cash.foundation/blog/powers-of-tau/">currently doing</a>. In the revamp you can participate in the trusted setup yourself, and then you can be sure that you personally haven't cheated and that the trusted setup was correct.

Trusted setup is also expensive. For every new functionality you would need a new trusted setup. If you wanted to change something about the zcash proof system, then you would have to do a new trusted setup and that's what they're doing right now.

## STARKs and computationally-sound proofs

Last year a new tool was introduced at bpase17 called <a href="https://cyber.stanford.edu/sites/default/files/elibensasson.pdf">STARKs</a> (<a href="https://eprint.iacr.org/2018/046">see also</a>). This is Micali 01, Ben-Sasson et al. 2017. This was called STARKs or computationally-sound proofs. They are based on the PCP theorem which are also quite amazing. They are only logarithmic in size, they have fast verification, but they are not very practical especially for this application.

We kept looking for more things that would suite the application to confidential transaction rangeproofs. We found a paper that came out in 2016 by Bootle et al. 2016 from the University College London for log sized proofs for arithmetic circuits. This is an interactive multi-round protocol. There's an interaction going on but you can make this into a non-interactive protocol. This protocol had really short proofs which were logarithmic in size for arbitrary statements but the proving time, the verification time, is linear in the circuits. In SNARKs, the proof size is constant and the verification time is also constant. It doesn't change with the circuit. But here the verification time was linear. But we really more care about the proof size which is much more important in a distributed network for something like a range proof where the transaction has to be sent around the network and network bandwidth is often the bottleneck.

This seemed like an interesting candidate because you had logarithmic proof sizes. But it turned out that in practice for some technical reasons it didn't really work well together. The way that the protoco lwas presented didn't work well with the homomorphic commitments. In practice, the range proof size would not have been much better than even the linear proof.

## Bulletproofs

This is why we improved on the protocol and developed <a href="http://web.stanford.edu/~buenz/pubs/bulletproofs.pdf">bulletproofs</a>, which in general are 3x shorter than the previous proof protocol but you can aso do very efficient proofs on these committed values. You want to prove that a commitment in a certain range, and with bulletproofs this can be done very efficiently. It's also, it can make it non-interactive using this Fiat-Shamir heruistic, and bulletproofs are only based on the discrete logarithm assumption which is one of the most tested assumptions in cryptography. What this means is that you can run it no matter what elliptic curve you're using you can use bulletproofs. There are other cryptosystems like SNARKs where you need to use pairings which only work for certain curves but bulletproofs only rely on discrete logs which any secure elliptic curve also relies upon the discrete log problem being hard.

We designed bulletproofs for range proofs but they also generalize to arbitrary arithmetic circuits. This means that I can prove say I have some computation and I want to prove to you that I've done this computation correctly and I have some secret inputs to this computation. So say I want to tell you that I know secret inputs such that this complex function evaluates to 1. It's a function that is either 1 or 0. And I want to prove to you that I know inputs, secrets to a zcash transaction such that the transaction is valid. This is a function that I could encode in an arithmetic circuit. Bulletproofs also work for that. The proof size for that is, again, logarithmic in the size of- the complexity of that function.

<https://joinmarket.me/blog/blog/bulletpoints-on-bulletproofs/>

## Bulletproofs proof size

<https://www.youtube.com/watch?v=gZjDKgR4dw8&t=17m20s>

What does this mean concretely? Let's look at range proofs. For one range proof using bulletproofs, we can compare it with the old range proofs which were roughly 4 kilobytes for 64 bits of precision. And for us, the proof size is only 672 bytes. SNARKs are constant size and still shorter. The nice thing though is that if I want to prove that multiple ranges are in this same-- multiple commitments are in the same range- then I can use this logarithmic aggregation technique. I can do this much faster htan doing two proofs. It's much easier for me. The proofs are much shorter than two values are in a certain range. So why is this important? If I have a confidential transaction then I am going to have multiple outputs to multiple people. In any standard case I usually have at least two outputs. If I want to prove to you that these two outputs are within the range then I could simply give you a single bulletproof and we can see that we get this nice logarithmic aggregation and the proof size only grows by 64 bytes versus the linear proof which only grows in size. Actually if you extend this and say you have 10 outputs, then it just, it's just a, the differences get quite dramatic. We're still under 10 kb for proof size for bulletproofs, and the linear range proofs would have been 40,000 bytes.

## Coinjoin

10 outputs is not realistic for most transactions. So the question is, now that we know we can get an aggregate or a benefit from having more outputs in a transaction. So how can we incentivize people to create transactions with more outputs? Well, one thing that comes to mind are <a href="https://bitcointalk.org/index.php?topic=279249.0">coinjoin</a> transactions. A coinjoin transaction is where multiple users combine their transactions to have one transaction. This is often done to increase anonymity. It turns out that this also has-- with bulletproofs, we might be able to use this to create shorter transactions for everyone. Smaller transactions for everyone.

The idea is to have multiple provers and they all want to prove that their commitment is within the range. So the question is whether these provers together can they create a proof without revealing their secrets to each other. Of course, they could just tell each other their secrets and then one person just creates a proof. But that's not the idea. You don't want to give up the value you've been working so hard to hide, you don't want to send that value even to the people that you're sending this transaction to. So say Peggy's aren't friends (the verifiers aren't friends) but they want to create one transaction together. They could concatenate it together where each person creates their own proof but this doesn't really help.

## Bulletproofs' multi-party computation (MPC)

We designed a multi-party computation protocol for bulletproofs, which is a protocol that allows you to combine proofs and create one single proof within a few logarithmic number of rounds with very little communication or you could even use less rounds and have a little bit more communication. They can create one proof together without revealing to each other what their secret values are. They won't learn the other parties' which values they are sending but they can still as a group create a single transaction with a single proof. This is how having 10 outputs in a transaction becomes much more realistic and much greater benefits. Coinjoin here is not only helpful for anonymity but also helpful for efficiency which creates an economic incentive to join your transactions together.

## Bulletproofs for confidential transactions and mimblewimble

Let's summarize why bulletproofs for confidential transactions. And by the way, this all also applies to <a href="http://diyhpl.us/wiki/transcripts/realworldcrypto/2018/mimblewimble-and-scriptless-scripts/">mimblewimble</a> which also uses confidential transactions because this is such a big win.

So we have 670 bytes instead of 4 kilobytes range proof (for 64 bit range). With aggregation and bulletproofs, we can put two range proofs in 736 bytes instead of 8 kilobytes. And for 16 range proofs, just to make it sound good-- it's 928 bytes vs. 61 kilobytes. It's a big win.

Doubling the precision adds 64 bytes. The old range proofs used 52 bits only because you know every bit added more linear cost to it linearly. But here it doesn't really matter what precision of range proof you need.

In total, the UTXO set size as a rough estimate we ran some numbers it would now be 17 GB vs the current 160 GB if you use the old range proofs. In mimblewimble, this would be because you can aggregate everything it would be almost the size of the whole blockchain.

There's also this built-in coinjoin protocol for combining confidential transactions.

One of the goals we had originally was to make sure that, and this is a more technical point, but making sure that even if someone was able to break the discrete log assumption perhaps with a quantum computer then there could be proof schemes and commitments where they could only break anonymity. They could reveal how much is being sent but they couldn't break soundness (couldn't create money out of thin air). We think that would have been a much more desirable tradeoff instead of the one that we currently have, which is that even if there's a quantum adversary he wont be able to learn the amounts but he will be able to create money out of thin air which makes the system very unusable. We would have liked to have this tradeoff that you have unconditional or quantum soundness and only computational hiding or computational zero-knowledge. The problem it turns out is that if you just use, theoretically, if you use compression- so we need to represent our bits in something less than the number of bits- there's just fundamentally no way of getting unconditional soundness. If you compress something then you're losing, somewhere you're losing information.

## Bulletproofs proof size for circuits vs. SNARKs/STARKs

<https://www.youtube.com/watch?v=gZjDKgR4dw8&t=25m>

I also said that bulletproofs work for arbitrary arithmetic circuits. For saying I want to prove to you I've done some more complex computation correctly. Let's compare the bulletproofs size versus some other tools that we have in the toolbox.

Again the proof size of SNARKs is just completely unbeatable. But again, they have a trusted setup. We can see again that STARKs, I don't like, don't quote me on the exact numbers because I read them off from a graph from the STARK paper but as an order of magnitude a STARK is at least over 200 kb. Even the smallest STARK is over 200 kb. And also growth is logarithmically with a bigger factor. Versus bulletproofs-- even for gigantic circuits, the proofs stay pretty small.

Over on the right on the graph, there's a circuit with 4 million gates. Why is that interesting? Well, this is the circuit that the original zcash paper had. It was a circuit with 4 million gates. This proves that zcash transaction is correct or the 188 byte SNARK is--- or for bulletproofs it's 1.8 kilobytes, but it's not a completely insane amount of data. For STARKs it's 455 kilobytes. So you if you have a one megabyte block size, then you could fit exactly two zcash transactions in that style into the block, and that of course is quite unusable. zcash is currently working on a bunch of improvements to make their circuits smaller. For them they are working on reducing the prover time. For us this would also be- using bulletproofs- reduce the proof size, again rough estimates but, maybe then it's more on the order of 1.3 kilobytes.

## Bulletproofs not for zcash

Why aren't we saying let's use bulletproofs for zcash? The reason is that the proof verification time is still linear in the statement. The verification time for SNARK is constant. It's 10 milliseconds no matter what you're proving. For bulletproofs, it's growing linear with the statement. I'll show you in a moment that the constants-- and there's a lot of cool tricks we can use to get this down-- it's unfortunately not fast enough to prove something like zcash.

## Comparing proof systems

<https://www.youtube.com/watch?v=gZjDKgR4dw8&t=27m45s>

<table>
<tr><td>Proof system</td><td>Sigma protocol</td><td>SNARKs</td><td>STARKs</td><td>Bulletproofs</td></tr>
<tr><td>proof size</td><td>long</td><td>short</td><td>shortish</td><td>short</td></tr>
<tr><td>prover</td><td>linear</td><td>FFT</td><td>FFT (big memory requirement)</td><td>linear</td></tr>
<tr><td>verifier</td><td>linear</td><td>efficient</td><td>efficient</td><td>linear</td></tr>
<tr><td>trusted setup</td><td>no</td><td>required</td><td>no</td><td>no</td></tr>
<tr><td>practical</td><td>yes</td><td>yes</td><td>not quite</td><td>yes</td></tr>
<tr><td>assumptions</td><td>discrete log</td><td>non-falsifiable</td><td>OWF (quantum secure)</td><td>discrete log</td></tr>
</table>

This is a comparison of different proof systems. We can see that bulletproofs are definitely just superior to sigma protocols, which is a very classical proof system and it's inear. They don't have the trusted setup, they have more reliable assumptions than SNARKs, but again the proof size is linear. The proof size for STARKs only grows logarithmically- for very complex statements it might be okay, but for something like a rangeproof in practice it's just not practical and the prover is extremely expensive for a STARK and it has very expensive memory requirements... I think they ran their system on a 780 GB RAM machine and I think they were only able to work up to you know a certain limit of, there's no way a prover could prove a zcash proof or STARK yet. It's still in the--- STARKs are an amazing breakthrough and really cool work and I'm sure there's a lot more to come there.

## Bulletproofs for solvency proofs

Dagher et al. 2015 <a href="https://eprint.iacr.org/2015/1008">Privacy-preserving proofs of solvency for bitcoin exchanges</a>

What are other applications? Looking at these properties, what are some other interesting applications for bulletproofs? One interesting application could be solvency proofs, such as for cryptocurrency exchanges that want to prove they really do hold some cryptocurrency coins.

This was developed a couple years ago. This was shortly after MtGox went down. An exchange could prove that they have coins instead of saying "trust me" they could give a zero-knowledge proof that they are solvent and the proof would not reveal any information about why they are solvent. It wouldn't reveal anything about customers, such as with addresses they have, or how much they have in total. All of that can stay private. But the exchange could still convince the users that they have as many bitcoin as they claim to have. You can't do this for dollars because dollars are not a cryptocurrency.

I thought this was a neat application. With bulletproofs you can get the solvency proofs down from 18 GB to 62 megabytes so that's a nice improvement.

## Bulletproofs for smart contracts

Another application of bulletproofs is smart contracts. A smart contract, you can write a bulletproof which is a short proof for an arbitrary computation. You don't have a trusted setup. This is pretty nice for a smart contract. It makes it easily adaptable for different computations. This idea of having this proposal or proposal on how to have privacy-preserving smart contracts-- but for each different smart contract, in that paper, you need a new trusted setup. With bulletproofs, this is no longer the case, and the proofs are short and the size doesn't blow up. Verification is linear and it might be too complex for a contract to run and perhaps the contract doesn't have the power to run this computation. For some computations it might, but for others perhaps not.

To work around this, there's a refereed delegation model proposed by Canetti, Riva and Rothblum in 2011 ("<a href="https://eprint.iacr.org/2011/518">Two 1-round protocols for delegation of computation</a>"). This is exactly truebit uses where they say, say I want to verify my proof. I input my proof and the verifications outputs 1 or 0, either it succeeded or not. And then I can send the proof to the smart contract along with, I lay out this verification procedure and I do it step-by-step and I send out the middle value, the middle value of this verification procedure and I kind of commit to that or send it to the smart contract. And then someone else can read the proof, it's publicly verifiable, check it offline on his fast hardware and say there's a mistake it's a faulty proof I don't trust this-- then the challenger can complain to the smart contract and claim the proof is invalid. What they then do is that they run a binary search and say "I think actually the value in the middle is wrong" and then we know that they diverge or disagree on some sort of gate or computation step between the first step and the middle step. And then you run an interactive binary search with the smart contract, and then at the end the smart contract only has to check a single gate in the verification procedure. A single step in the verification procedure, to decide whether the challenger was correct or whether the prover was correct. So this is kind of truebit- they are trying to do this for many different applications but this also works for verifying a bulletproof. The cost is only a logarithmic number of rounds, a logarithmic amount of communications, and the smart contract only has to do 1 small computation (checking 1 gate). So this could be one multiplication or one addition.

## Bulletproofs for verifiable shuffles

Another application of bulletproofs, which is somewhat outside the realm of cryptocurrency but might still be interesting, are for verifiable shuffles. The idea is that you have a bunch of senders, each of them has a bitcoin transaction or an email and they somehow want to shuffle their mails and it's encrypted email maybe and they want another set of encrypted or committed mails or values and they want to output them and the important thing is that there's some sort of shuffling between the input and the output. This is called a mixnet. There, part of this mixnet computation is that you have basically n proofs that here's two lists of committed values and the underlying values I've committed to are exactly the same in the two lists. With bulletproofs, you can have logarithmic size verifiable shuffle and the best previous result was square root.

## Bulletproofs implementation

<https://github.com/bitcoin-core/secp256k1>

Let's talk about some very exciting... note that I haven't yet mentioned a single number for how long a bulletproof verification time takes. I'll do that now. There's some exciting new developments. Andrew Poelstra and with the help of Pieter Wuille and Peter Dettma, went on implemented bulletproofs into libsecp256k1 which is the standard bitcoin cryptography library. They did an amazing job of implementing bulletproofs and they have come up with many improvements. I have also heard that there's a rust implementation. I also have a java implementation which is a lot slower and a lot worse and is not production-ready code. On the other hand, libsecp256k1 is-- this is the code that secures bitcoin itself and it's very excited that bulletproofs is implemented there and can make adoption a lot easier.


## Multi-exponentiation

<a href="http://www0.cs.ucl.ac.uk/staff/J.Bootle/pippenger.pdf">Efficient multi-exponentiation</a> (Bootle)

So what are the highlights of this verification of bulletproofs? What was Andrew able to do? So, one of the core things that they did is if you, this is actually only a part of the protocol, but it's this complex and we written it up- you write these up as interactive protocols between prover and verifier because analyzing them is a lot easier but it has many wrongs and it was complex but it turns out that when you loo at it carefully and you do some tricks and optimizations then you can verify it using one single big multi-exponentiation which is where you have a bunch of generators (say 2n), so for 64 bit range proof you have 128 generators, and then you have a bunch of exponents that I can compute and then I have to do this multi-exponentiation and check whether the result is equal to zero. Why is it helpful to reduce it not just for simplicity or understanding but what are the reasons why it's helpful to reduce it to multi-exponentiation? Well, multi-exponentiation is a very well studied problem and it turns out that the kind of the cryptographic operations the heavyweight operations only grow with N over log(n) so it actually gets better the bigger your statement is. And we can see here that the-- for a range proof, the bulletproofs are actually faster to verify than a SNARK. They are significantly faster. They are almost 2.5x faster, and it grows for even bigger statements. So for 2 rangeproofs, it's 3x faster than the old range proof protocol. They are a lot faster than STARKs. This graph is deceiving-- if you scale this up to bigger computations then SNARKs and STARKs which are either constant time or STARK verification time grows logarithmically at some point it will become faster. This is still within a microsecond though. Verifying a confidential transaction range proof takes about 4 milliseconds. In context, I think verifying an ECDSA signature is 800 microseconds. So it's still a factor of 5x slower... but, I think just yesterday Andrew Poelstra came up with this trick which- I guess- Dan Boneh told me this has been around forever.. a trick for batch verification.

## Batch verification

Bellare, Garray, Rabin <a href="https://cseweb.ucsd.edu/~mihir/papers/batch.pdf">Fast batch verification for modular exponentiation and digital signatures</a>

What if you have two transactions and they have two range proofs? You have this-- you can reduce the verification to this simple multi-exponentiation. But now I have one with- in the first proof, my exponents are x1 to x2n and for the next method it's y1 to y2n. The generators, however, stay the same. What I can do as a verifier I just sample a random scalar alpha and then multiply the first equation times alpha and then add them to the second equation. And for, unless I get very unlikely, and I sample alpha from a large enough space, the only way that this now the sum of the two equations verifies is if the two equations actually held. So, what does that mean concretely? I take an alpha, multiply the first thing by alpha, or exponentiate it by alpha, and then combine the two. Instead of having to do two multi-exponentiations, I still have to do one, and it's of the same size. I only have to operate-- do a little bit more work for the exponents, but it's actually quite efficient. The heavy operations- the heavy exponentiation, it stays the same. I only need to do one exponentiation of a fixed size. This is interesting in bitcoin confidential transactions because it means I have all these transactions in a block and I'm a miner and I want to verify the whole block and I do this trick not just for 2 but all the transactions in the block and then I only need to do one exponentiation. These are preliminary numbers- verifying the first transaction is 4 ms but then verifying each additional transaction is only 200 microseconds of additional proof time, which I think is even faster than verifying an ECDSA signature. Bulletproofs for confidential transactions in terms of verification time has become practical. There's no more reason in terms of time why you wouldn't add confidential transactions to bitcoin. I think this is very exciting new development. And maybe, there's still lots of other problems like the technical difficulties, quantum security, the question of whether you want confidentiality in a transaction, but at the very least technically, now with bulletproofs confidential transactions have become practical.

There will be an updated paper on bulletproofs in a few days.

<https://crypto.stanford.edu/bulletproofs>

## Q&A

Q: From a proof system perspective, is there any case where it's more interesting to choose a sigma protocol? And secondly, can you expand on the applications on bulletproofs for cryptocurrencies could you use this for publicly verifiable secret sharing scheme to prove some constraints on values fulfilled or is there something else?

A: Technically, I can talk about that in more detail in offline, but when you have complex statements on public commitments or public keys... if you're using different bases for your pedersen commitments, then bulletproofs are potentially still interesting. At least in theory, and perhaps specifically, you could apply this to arbitrary applications. It's a general proof system for arithmetic circuits just like SNARKs is a general proof system for arbitrary arithmetic circuits.

<https://joinmarket.me/blog/blog/bulletpoints-on-bulletproofs/>

<https://www.reddit.com/r/Bitcoin/comments/7u67an/video_presentation_bulletproofs_benedikt_b%C3%BCnz/>

<https://www.reddit.com/r/Bitcoin/comments/7cs1zc/bulletproofs_a_radical_improvement_in_the/dps7ju6/?sh=bf6a0eb8&st=JD5Y740U>

<https://github.com/ElementsProject/secp256k1-zkp/pull/16>


