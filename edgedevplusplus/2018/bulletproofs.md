---
title: Bulletproofs
transcript_by: Bryan Bishop
tags:
  - cryptography
speakers:
  - Kalle Alm
media: https://www.youtube.com/watch?v=YslQUkiEMXc
date: 2018-10-04
aliases:
  - /scalingbitcoin/tokyo-2018/edgedevplusplus/bulletproofs
summary: Overview of Bullet Proofs - a new zero-knowledge cryptographical solution for confidential transactions
---
# Bulletproofs

<https://twitter.com/kanzure/status/1047740138824945664>

# Introduction

Is there anyone here who doesn't know what bulletproofs are? I will not get to all of my slides today. I'll take a top-down approach about bulletproofs. I'll talk about what they are, how they work, and then go into the rabbit hole and go from there. It will start dark and then get brighter as we go. As you leave here, you may not know what bulletproofs are. But you're going to have the tools to figure it out. That's the goal here today. I think you guys are pretty tired. My voice is dying, too. So things are not great. But we will be doing some fun things here. I'll do the proofs and stuff we're doing.

I wrote a tool for the purpose of learning bulletproofs, called aside. It's very narrow purpose, but it could be helpful in these situations. If you have sage math, I recommend that instead. People asked me why I wasn't using sagemath; well, I didn't know about sage math.

# Acknowledgements

Most of what I'm talking about today is based on Adam Gibson's (waxwing's) blog post "from zero (knowledge) to bulletproofs which is about 45 pages long. The bulletproofs paper is also about 45 pages long, which is interesting. Adam wrote down how he learned about bulletproofs, and I'll go through that, and then how I saw that. So you'll be seeing how I saw someone seeing how bulletproofs work.

<https://joinmarket.me/blog/blog/from-zero-knowledge-proofs-to-bulletproofs-paper/>

# Agenda

The agenda includes bulletproofs top-down, then math stuff, then zero-knowledge proofs.

# A problem that bulletproofs address

Fungibility is a necessary property of sound money. If two separate one dollar bills were worth different amounts of money, then the dollar would be useless as a currency. In the same way, in bitcoin, if I had two coins that were both worth 1 BTC face value but they were worth something different on the market then that's really bad. Money doesn't work that way.

Bitcoin has a problem because it's not very private. It's one of the least private currencies in existence. We can all check where all the coins are. It's all there on the blockchain. The problem is that you can deanonymize users on the blockchain, and this reduces fungibility. One solution is called [confidential transactions](http://diyhpl.us/wiki/transcripts/gmaxwell-confidential-transactions/).

In confidential transactions, you can hide the amounts using something called a range proof and homomorphic commitments. One way that you can do analysis and deanonymization on blockchains is by looking at the values and seeing how much people are sending to who and when. But if you can hide the values, then you can gain a lot of privacy.

The problem, though, is that confidential transactions are pretty huge. They are several kilobytes in size. You would be spending 10x more fees to spend a confidential transaction on the bitcoin network today if it was a deployed and activated feature.

However, bulletproofs can shrink the confidential transactions and do a bunch of other cool things.

# What bulletproofs really are

Roughly speaking, bulletproofs are zero-knowledge proofs of faithful execution of arithmetic circuits.

# The general idea

You can use the replace inner-product argument to reduce the overall communication by a factor of 3. This eliminates the need ofr implementing commitment opening algorithm as a part of the verification circuit. It's some fancy schmancy multiparty stuff. It also helpful specifics like range proofs.

We're going to talk about the inner product argument.

For coinjoin or multiparty and as the people go up, you end up paying less money to be more private and be more secure. This is a pretty good privacy feature.

There's also some specifics in the bulletproofs paper itself, like talking about range proofs, which is another part of confidential transactions. As you can see, there's lots to cover here.

# General idea behind that

Bootle's 2016 paper was actually building on a 2009 Groth paper. It improves the communication complexity from square root proportional to .... and the general idea behind that is the 1991 Pedersen commitments paper. You can tweak the pedersen commitments to give a public coin, a zero-knowledge argument, for the satisfiability of a binary circuit with N gates that require communicating order sqrt(N) group elements.

* Bootle 2016 <https://eprint.iacr.org/2016/263.pdf>
* Groth 2009 <http://www0.cs.ucl.ac.uk/staff/J.Groth/MatrixZK.pdf>
* Pedersen 1991 <https://www.cs.cornell.edu/courses/cs754/2001fa/129.PDF>

# What are bulletproofs?

Bulletproofs are an optimization of confidential transactions, which makes confidential transactions practical for bitcoin transactions. Also, bulletproofs are an optimization of coinjoins (even with yourself) which makes them even more practical. Also, bulletproofs are a significant advancement towards better fungibility in bitcoin.

# Mathsies

Before we get into the fun part, we're going to go to the bottom part and talk about some math. There's tedious pages and pages and pages of math. It's straightforward. It's a long road. Terminology can also be scary. Don't let terminology scare you. But this is all very simple to understand if you do the work.

# A note on curve points

A scalar is a regular number, not on a curve, not an x and y coordinate. It's a huge number, like 32 byte huge. It could be that big. Say we have two scalars a and b. We just take a number and use it as a private key. If you take the number "2" and use that as your private key, that would be bad. But if you have a 32 byte value, or 256 bits, that's pretty good if you have entropy. And you multiply it by G, the generator, it turns that number into a curve point.

We can use the scalars as private keys: aG is the public key for the private key a. We can combine them to form a new private key (don't do this at home) aG + bG is the public key for the private key (a + b). You can take two public keys and you can add them together. If you add them together, you get a third. We can also subtract one from another: aG - bG is the pubkey for (a - b). We can add pubkeys together. You might think this could mean you could do multisig, but this is broken when you do it with someone you don't trust because they could negate your key by saying their key is just the opposite of your key or something.

# NUMS number

NUMS just means, nothing up my sleeve. In particular, if P is our NUMS number, I don't know the x in the equation x * G = P. NUMS numbers are super simple to make, e.g. using a hash function like by doing H(G || i) can be G\_i for the vector of generators G where G is the "regular" generator.

You can prove it's a NUMS number for something like "my name is kallewoof" because you don't know the private key that corresponds to that, or it would be incredibly unlikely for you to already know that private key.

# Dot product, inner product

Dot product and inner product are the same thing. For a = (a1, a2, ... an) and b similarly, the dot product of a and b can be calculated. Simlarly, with hadamard product between a b, ie.. the elements are pairwise multiplied but no summation occurs.

# To hide a value

Say we have a value x which is a secret and we want to hide it. We start by saying x is our secret value. Now we can do x * G to get our public key if you want. G here is a generator. In bitcoin, we have one single generator. But here we will have lots of generators. Basically all of them are public and known to everyone. They're usually denoted using capital letters, like H, G and bold H for vectors of generators, etc.

# Hiding vs binding

A commitment scheme is "hiding" if a commitment C does not reveal the value it commits to, and the scheme is "binding" if after committing to C(m), you can't change your mind and open it as a commitment to a different message m2. It is proven that no commitment scheme can be perfectly hiding _and_ perfectly binding. This has been proven.

Hiding is related to zero knowledgeness. Binding is related to knowledge soundness.

# Generalizing 1 + 2 = 3

In the equation 1 + 2 = 3, there's variables, an operation, and equivalence.... if this is a commitment, then this would be perfectly binding because I can't suddenly change any of this because you know all of the details and can verify it. But it's completely not hiding at all, because you know what it is, it's not good for privacy.

But we could do something like x + 2x = 3x. This is actually perfectly hiding, I think. It's very nearly perfectly hiding. But it's completely unbinding because I can set x to be whatever I want and it would still be valid. So it's not binding at all.

If I did x + 2x = 3, then we're back to square one. It's perfectly binding again, but it's also not hiding because you can simply solve for x.

x + 2x = y is interesting but it's not helpful at all. We can keep going and try x + ax = bx, and then find out that a is b - 1 which isn't helpful here.

We can say something + something is something again... but that's too abstract. But if I say that I have something, and I know what it is, but I add it to something else, and then I subtract a third thing from it, and I claim this is zero. I commit this to zero. This is actually useful, even if you don't know anything about those values. If I can do that, then I can also say the first two values equal the second value. That's pretty close to a confidential transaction. I can hide the value here, maybe. So if I say the inputs are the inputs on the left hand side and they add up on the left hand side, and you take all the outputs on the right hand side, then even not knowing anything about the values, I know that the transaction is not overspending. So that's useful.

There's a problem though, which is negative values. I can create money by hiding negative values and only spending the positive values. So there's no range check in this example yet. We don't know if we're overflowing or underflowing.r.

# Pedersen commitments in elliptic curve form

A pedersen commitment is an information-theoretically hiding commitment scheme, which is binding under the discrete logarithm assumption. Opening a commitment means revealing the v value in C = rH + vG. So that's a commitment. G and H are generators. v is the hidden value.

# Recap

Generators are pre-defined, public nothing-up-my-sleeve numbers. E.g., secp256k1 curve G: x * G = public key P for private key x.

Commitments: hides and/or blinds some other value.

# Pedersen commitments again

There's a homomorphism here. "A structure preserving map between two algebraic structures of the same type". For example, f(x + y) = f(x) + f(y). Pedersen commitments have a homomorphism as well.

# Dramatization of zero-knowledge proofs

I don't actually know the power rangers. They seemed appropriate for this. If we dramatize zero-knowledge proofs, we can get the following.

P: the prover. She proves that she knows stuff. Some call her Peggy.

V: the verifier, he verifies that hte prover knows what they claim to know.

E: the extractor; a torturer; makes P spit out secrets, aka an emulator.

S: the simulator; conjurer of tricks; a bold liar who tricks the verifier in various ways.

O: the oracle; knows stuff no one else knows.

Most people write these as P, V, E, S and O.

# Zero-knowledge proofs criteria

A zero-knowledge proof must have completeness (an honest prover must succeed in convincing the verifier), it must have zero-knowledgeness (the verifier must learn nothing about the secret from the proof), and knowledge soundness (the prover must not be able to convince the verifier unless the prover actually knows the secret).

# Transcripts

A transcript here is just a list of stuff that the prover and verifier tell each other. Interaction between prover and verifier is called a transcript. The order is crucial, for example, the verifier does not reveal certain values to the prover before the prover sends a value, and so on.

# Schnorr identity protocol

Schnorr identity protocol is a simple example of a zero-knowledge proof scheme. John Newbery presented on this earlier today. You have a secret value x, you have a commitment Q which is xG. The transcript is (R, e, s). THe prover sends R = kG to the verifier. The verifier sends random value e. The prover sends s = k + ex to the verifier. Then the verifier verifies sG =? R + eQ.

This is an example of a sigma protocol. The prover sends something, the verifier sends something back, and then the prover sends something back. This is why it's called a sigma protocol. I don't even know why they call it that. Are they trying to confuse me? But anyway.

# Completeness

Given a prover with a correct opening to a commitment C, does it always validate? With the Schnorr identity protocol, Q is the commitment to x, and if the prover knows x, there is nothing in the calculation s = k + ex that the prover cannot do, and the verifier will thus receive a valid solution for sG = R + eQ.

I'll give you an example of a zero-knowledge proof that might be retarded but it will help you understand it. The transcript will be (R, e, z) where x is Hash(z). I'm proving knowledge about x here. x is the private key. But this zero-knowledge proof requires you to send me the preimage of x as a hash-value. So we need to have the z value be qual to the inverted hash of x. We can't prove anything, even if you have x, you can't prove it.

If you can't prove that you have x even if you have x, then the zero-knowledge proof is broken.

# Zero-knowledgeness

Does the verifier learn anything about the secret after convincing the verifier that they know x, have they learned anything about x? In the case where the verifier already knows x, we have seen that already. What if they don't know x? Now we are going to talk about the simulator, the conjurer of tricks. The simulator is going to take control of the verifier's execution environment and we're going to do time leaps by creating the transcript and doing it out of order.

The simulator first sets s and e to random values, and then they set R = sG - eQ and then they set the transcript to (R, e, s) and the verifier says sure and it checks the value and says it worked. But the simulator doesn't know the secret, and yet they can still make a proof for it.

By changing the order of the transcript, I can create something that looks identical to a real proof, even though it's fake. You wouldn't be able to tell which is which. They look exactly the same. Because they look exactly the same, and the only thing I did to make a fake one was to change the order, it follows that you don't learn anything about the secret. All I did was change the order and proved to you something that was not the case. Changing the order does not create information, right?

There's a slight note about the distribution here. Don't create zero-knowledge proofs without knowing this caveat.

Any questions about zero-knowledgeness or completeness? Okay.

# Knowledge soundness

This is complementary nad opposite to proving zero knowledgeness. Remember the extractor? Say he takes control of the prover and tortures him or her in various ways. So what we do is that the idea is to manipulate the prover somehow so that he spits out the secret information (the witness). If we succeed, the prover must know the secret information. The extractor "debugs" the prover. He can start, stopl, rewind, and copy the states of the prover however the extractor would wish.

In the Schnorr identity protocol case, the question is wheter does the prover actually prove that he knows x or could he somehow fake it? The transcript was (R, e, s) where s = k + ex and R = kG. Extractor runs the prover up until after the first step in the transcript. He saves the state, just like a video game he can save and reload later. He runs to the end. He can get back a random value s1... this is one round, he does this two times. Instead of going back to the beginning, he restores the state and runs it until the end again, to produce e2 which is random, and s2 which is k + e2x. We can now solve for x.

By just doing this twice, I can get your private key. Isn't that great? How did I get the private key? This isn't normal. It's the most common error in cryptography, where you reuse the ephemeral key or the nonce. If k1 and k2 were different, then we would have more unknowns than equations.

This proves knowledge soundness for the Schnorr identity protocol.

# Summary

You can prove zeroknowledgeness by manipulating the verifier such that they believe the proof, even though the proof is invalid.

You can prove knowledge soundness by manipulating the prover into revealing the secret to us.

# Vector pedersen commitments

I only have 5 minutes left. You take the pedersen commitment and you can extend it to take a vector of that. Here, G is a vector of generators. When you have vectors together like this, it's implied that there's a dot product in between.

We also generate a set of commitments for each of our m vectors of dimension N where N is not equal to m2. Have we revealed anything by showing the commitents to the world? The answer is no. The commitments are stil lperfectly hiding and they aren't perfectly binding, under the discrete log assumption.

So we have a zero-knowledge protocol for vectors.

# References

* bulletproofs paper: <https://eprint.iacr.org/2017/1066.pdf>
* <https://joinmarket.me/static/FromZK2BPs_v1.pdf>
* <https://joinmarket.me/blog/blog/from-zero-knowledge-proofs-to-bulletproofs-paper/>
* <https://diyhpl.us/wiki/transcripts/2018-02-02-andrew-poelstra-bulletproofs/>
* <https://diyhpl.us/wiki/transcripts/blockchain-protocol-analysis-security-engineering/2018/bulletproofs/>

