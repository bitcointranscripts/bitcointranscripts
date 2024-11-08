---
title: Verifiable Delay Functions
transcript_by: Bryan Bishop
tags:
  - cryptography
speakers:
  - Dan Boneh
date: 2019-02-03
media: https://www.youtube.com/watch?v=dN-1q8c50q0
---
<https://twitter.com/kanzure/status/1152586087912673280>

## Introduction

I'll give an overview of VDFs and make sure that we're on the same page. I want to make sure everyone knows what it is that we're talking about.

The goal of a VDF is to slow things down. The question is, how do we slow things down in a verifiable way?

## What is a VDF?

I won't give a precise definition, look at the manuscripts. A VDF is basically a function that is supposed to take T steps to evaluate, even if the honest party has polynomial parallelism. You shouldn't be able to speed up the evaluation in that scenario. Also, the output should be easily verified with efficiency.

There's a setup, evaluation and verification algorithm. The setup takes a security parameter lambda, a time bound T, and produces public parameters pp and we'll talk about the setup procedure later today which might involve multi-party computation steps. That's the setup.

The evaluation function takes (pp, x) and produces an output y and a proof. This should take T steps even if you have a parallel computer. Parallelism should not speed up the computation.

The verification algorithm takes (pp, x, y, and the proof) and it tells you quickly whether or not y is a correct evaluation of the VDF.

## Security properties of verifiable delay functions

There are two security properties.

The first one is uniqueness. It's crucial that these things are unique. Given a particular value x, there should be only one value y that convinces the verifier. If he can construct a y and a proof and a y prime and another proof that convinces the verifier in both cases, then it must be that y and y prime are equal. It's okay to have different proofs for the same y value, but it shouldn't be able to convince the verifier that there are two valid y values.

The second property is the "epsilon-sequentiality" property which is that, even if the adversary has a parallel machine, in particular polynomially-many processors, then the adversary runs in time time(A)<(1-epsilon)T a little bit less than T, even such an adversary can't distinguish the output of the VDF from a random value. So unless you spend time T, then the output of the VDF (the output of Eval(pp, X)) should look completely random.  We call this epsilon-sequentiality because the sequentiality is parameterized by epsilon here. We'd like to achieve sequentiality for the smallest possible value of epsilon.

Alright, that's as formal as I am going to get. I hope this is clear enough for everybody.

## Applications: lotteries

So what do we need verifiable delay functions for? Well there's the question of lotteries. You want to generate verifiable randomness in the real world. Is there a way to verifiable generate randomness?

## Broken method for generating randomness: distributed generation

This is sort of crypto 101. If you want to have n parties generate a random value.... the beacon chain has a random beacon in it. This is a dumb way to do this, nobody should use the following. We have participants, everyone posts a random value to the bulletin board, and the output is just the XOR of all the values. This looks rnadom but it's completely broken, because the last participant Zoey can choose her value so that she controls the final random value.

There have been many attempts to fix this problem, like commit-and-reveal. The problem with commit-and-reveal is that people might refuse to reveal. Why can't you just ignore their commitment if they refuse to reveal and only XOR the values of the people that opened the commitment? That's insecure. You can't just ignore the values that weren't opened because if 20 people collude then they could choose to not open any subset of 20 of them, and in doing so, they get 2^20 possibilities for controlling the final output. Commit-and-reveal is insecure if you ignore the values that were not opened.

Q: ...

A: Yeah, but now it's a game between how many players you have colluding... yeah, potentially. I don't know. For bit flipping, we know that this is not possible in a fixed number of rounds, but this is not bit flipping. This is just randomness, which you can't do in constant rounds. Okay, but anyhow. Commit-and-round--- these two rounds are problematic, we'd like to do things in a single round. Just post and you're done, nobody needs to come back and do anything else to get the randomness.

So this basic mechanism doesn't work. So what to do instead?

## Solution: slow things down with a VDF

There's a beautiful idea that says do what we were going to do before, but now we hash the outputs that everyone contributed. This isn't enough to ensure randomness, because the last participant can grind and get a hash that she likes. But instead what we're going to do is introduce a verifiable delay function.

We're going to introduce a verifiable delay function and the output will be the output of the computation. Nobody needs to come back, and the VDF guarantees the properties. Why does this work and produce unbiasable randomness?

Well, mechanically let's talk about how this works. Everyone starts submitting their randomness at noon, and then at a certain time, that's the participants in the protocol. The VDF is going to be longer than the submission window time. The sequentiality property of the VDF ensures the last participant can't try lots of inputs to the protocol because they can't compute the output of the VDFs because it will take her more than the submission time to compute it. We need to make sure it really takes her more than that amount of time, even if she has gallium-arcinide ASICs and the latest tech. It really needs to be the case that she can't predict the outputs in the submission window.

You guys have looked into gallium-arsanide technologies, right? It's not just ASICs. A lot of money is going to be at stake here. With a lot of money, you can build lots of fancy technologies. All of that has to be taken into account.

Q: ...

A: If it takes 10 minutes to submit, then you want it to take 1000 minutes to break the VDF. That's 1000 minutes for the honest party, yes, that's what I mean.

Q: ...

A: Yeah, good.

Alright, sounds good. Yes?

Q: ...

A: Oh, yes, yes, absolutely. Absolutely, absolutely. Yeah, yeah. Justin was saying that ... ethereum would likely set the parameter for the VDF to be 100x. So if you need a delay of 10 minutes, you set the parameter to be 100x, so 10 times 10 minutes, for the honest guys. There's capital D and then there's epsilon. That's the property of the protocol, yeah. So we're good.

Alrigtht, very good.

Sequentiality ensures that the last participant can't bias the output because she can't choose a value because it takes her too long to grind. And uniqueness ensures that there's no ambiguity about the output. Once the output is produced, people can't go back and say oh no the randomness should have been something else.

It's very interesting. Joe makes this nice point that if you remove any one of these requirements, then constructing VDFs becomes easy. The sequentiality and uniqueness requirements makes VDF difficult.

So that's why they are useful. Let's walk through a few constructions we can consider.

There's a great paper on proof-of-sequential work. It's just hash functions and robust graphs. It's using known techniques, yes. We don't need to have multiple VDF workshops on uniqueness, because we already know how to make VDFs if we remove uniqueness.

I have to be careful with my words at this conference.

## Constructions: easy with a hardware enclave

The first construction that comes to mind is a hardware enclave. If we had hardware enclaves, then constructing VDFs is quite easy.

What is a hardware enclave? We can store cryptographic keys inside the enclave, and we use those keys to generate the VDF. So the public parameters would be the signature for our public key scheme. So pk is public. When the input comes in, the enclave enforces a time delay, and when it's done, it produces some MAC or PRF of the input X and it also signs the output and proves that the VDF was computed correctly by the hardware. If we had a hardware enclave, then VDF construction is quite easy. But if you ever steal the HMAC secret key, then it goes out the window and everyone can compute these instantly.

You can't imagine how many people come in and ask me how can we use hardware assumptions for consensus. I think it's a terrible idea. If there's a lot of money riding on the security of these consensus protocols, well with enough money any hardware enclave can be broken. That's my position. It's fine for privacy and protecting data, but for consensus where breaking consensus means loss of money that's where it becomes dangerous.

That's the first approach that comes to mind. Seems like there's consensus on the main points.

## A construction from hash functions

You could build a verifiable delay function from hash functions. What you can do is you can build the VDF in the most natural way, which is where the public parameters are a parameters for a SNARK and the VDF is defined as a hash chain where evaluating sha256 repeatedly is going to take time T. But how do you verify the output was computed correctly? That's where SNARKs come in. But it turns out this is difficult to get to work correctly. The proof pi is a SNARK that the hashchain was computed correctly. Computing the SNARK takes more time than computing the chain, so you have to do something to counteract that. There was a paper by myself and Benedikt and others to show how to do this well, so that you can generate the proof fast enough. The verification would be a verification of a SNARK proof.

## Permutation polynomials

We also have ideas about building verifiable delay functions from permutation polynomials, and somehow that hasn't taken off yet, but that might be a future direction. Permutation polynomials is a polynomial that is a permutation of a finite field. It's such that for any two points x and y in the field the polynomial f(x) is not going to be equal to f(y). The property that this construction uses is the fact that finding roots of a polynomial-- the input x is going to be the image of the polynomial, and the value of the VDF would be a y value such that f(y) is equal to x. The input to the VDF is a value x, and the value is to find an input to the polynomial such that when you evaluate that input at the polynomial, it evaluates to the given value x. We want to find a f(y) that is equal to x. We want to find the roots of the polynomial f - x, can we find the root of that polynomial? Because it's a permutation polynomial, we know it has a unique set of roots. If it's easy to evaluate, like a sparse polynomial, then checking the roots were computed correctly is eas,y just evaluate and see if you get zero. Finding roots of polynomials the practical way to do it is by a GCP computation which is inherently sequential. That's the idea there. So the question is, are there good permutation polynomials for which there are no shortcuts and the best way to find the roots is by GCP computations? It's another valid direction for construction of VDFs. But the research challenge is, are there good permutation polynomials that are easy to evaluate- like sparse polynomials or they have short ... or the best way to find the root of the polynomial is GCP computation and no other shortcuts?

## An algebraic construction

An algebraic construction is the one that we're all excited about. The algebraic construction starts from a finite cyclic group G which has (1, g, g^2, g^3, ...) and the assumption is that the group G has an unknown order, and nobody knows how many elements are in the group. The public parameters are going to be some hash function into the group. The way we define the evaluation of the VDF is basically, take your input x, hash it on to the group, then raise the result to 2^T and that's inherently requires T squarings. This has been used for proofs of time, timelock puzzles, Rivest-Shamir... no.. RSW. This kind of function has been used quite a bit.

But how do you verify the output is correct? There was some beautiful work of Pietrzak'18 and Wesolowski'18 really beautiful protocols that allow you to quickly verify that the function was computed correctly. You can read the papers to see how the protocols work. It's proof of correct exponentiation. We wrote a [survey paper](https://eprint.iacr.org/2018/712) on this also. We will hear later today about hybrid schemes that combine the two proofs to make proof generation a little bit faster than we have today.

That's the algebraic construction. There's one issue here. The complexity assumption is that the group has unknown order. What does it mean? Why do we need the group to have unknown order? If the group has known order, like order D, then evaluation becomes trivial because I could compute 2^T mod D and then I would raise H(x) to that power but that's a very small power. If I knew the order of the group, I could accelerate it from T squarings to logarithmic time. So this group has to have unknown order.

Q: Rather than hashing into the whole group, you hash into a 64-bit space?

A: So the requirement is just that you see, you shouldn't be able to find three images in the hash function, say, that multiply to one another. You shouldn't be able to find x1, x2, x3 such that H(x1)\*H(x2)==H(x3) otherwise you would be able to trivially get the evaluation of the VDF. The hash function needs to be resistant to these multiplicative collisions. 256 bits is on the border of what's secure there, so I would suggest hashing even more than 256 bits. We really in principle need to worry about those multiplicative collisions.

The issue is that-- there's another attack, not just multiplicative collisions. Imagine H(x) mapped to a number that happened to be a product of only small primes. It happens to be 3\*5\*7 and you could precompute the VDF at 3, 5 and 7 and that would let you quickly evaluate the VDF at a number H(x) that happens to be a product of a small prime. So it's important that H(x) is not only a product of a small prime. So 256 bits is definitely not enough. You would need, to avoid these ... you would probably need the output to be a thousand bits or so. But that's okay, we know how to do that. You need a hash function that outputs more than 256 bits.

## Finite groups of unknown order: RSA group

So the challenge is: how do we generate groups of unknown order? Nobody should know the order of the group. VDF would be insecure if we can compute the order of the group. What are the candidate groups?

The RSA group comes to mind. You generate two integers, p and q, and you multiply them and the order of the group is unknown unless you can factor the modulus. Anyone who knows the factorization can know the order of the group, so we would need to construct this in a way where nobody knows the factorization. This requires a trusted setup. You could also choose a random large enough n, but n would have to be something like 40,000 bits so that the factorization is unknown. I think it's 30-40,000. We can talk about whether it's safe to go below that. If you choose a random number, it would have to be quite large for the factorization to be unknown. We would like to generate a 20000 or 4000 bit value for which nobody knows the factorization.

The problem with the RSA group is that you require a trusted setup. How do you run a protocol that generates a RSA group, such that everyone is convinced that the RSA modulus is a factor of two large primes, and nobody knows the factorization? We'll have a group discussion later today about this.

So we talked about RSA groups. The issue is the trusted setup procedure.

## Finite groups of unknown order: class group of an imaginary quadratic order

The other group that has unknown order is a class group of an imaginary quadratic order. I won't define what this is. But the amazing thing about this is that this group is specified by a prime. So literally you just choose a prime that happens to be 3 mod 4 and boom you have a group defined by this prime. The amazing thing is that if the prime is large enough, like 1000 bits, then nobody knows how to calculate the order of that group. It's just the best algorithm that we have for calculating the order of the group runs in subexponential time. You can't run the algorithm to calculate the order of the group.

This is a remarkable group because you pick a prime, you get a group of unknown order, and you can use it for a VDF... The benefit is that there's no setup, but the problem is that the operation in that class group is relatively slower than in the RSA group. To be honest, we don't know how much slower.

I talked with Bram Cohen yesterday and he said from the competition he ran, the implementations they have are much better than the initial implementations. So now maybe the performance differences between RSA operations and class group operations it used to be like a factor of 20, and it seems to be reduced to a factor of 5 now. We still don't know the answer there though.

The issue is that we don't know how much it can be parallelized, it could be that the class group operation itself can be parallelized. Justin, you had another comment? Yeah, nobody has ever done this. We don't know what the ASIC performance would be for a class group.

How parallelizable is the class group operations? We would like to basically understand and extract all the parallelism we can out of the group operations so that we know how long would it take to actually run.

Class groups were proposed in cryptography back in the 1990s but they have never been deployed. There's a lot of interesting work to be done here. For RSA I agree that a lot more is known. Since these groups are so easy to generate, you can switch these groups every few minutes. For RSA the large parameters means you have to pick them such that they aren't breakable in 50 years. But for a class group, we just have to generate a parameter large enough to not be broken in like a minute because they are so cheap to generate. In principle, maybe you can shrink the parameters such that it becomes faster than the RSA operation.

What do we do about attacks on RSA groups or class groups? Look, class groups, computing the size of a class group- this is a very fundamental question in algebraic number theory. A lot of people have worked on coming up with better algorithms for this. They run in time L 1/2, whereas factoring runs in time L 1/3rd. This is not a new problem, and it has been studied quite a bit. It's a very fundamental problem.

Class groups have no setup, but there's a slow group operation (meaning slow verification).

Chia is going to be using this. We need to come up with a number to say whta is the right modulus size to use.

## Open problems

Problem 1: are there other groups of unknown orders? The goal is no setup and there should be efficient group operations. Class groups have a slow parallelizable group operation, and the RSA group has trusted setup. Maybe there's a group that is a better choice.

Problem 2: These algebraic VDF constructions are not post-quantum secure. I don't know if we need to worry about that now. My calculations sohw that it is 30 years away. Why is not post-quantum secure? Shor's algorithm can efficiently compute groups, it's good at finding the order of groups. No group of unknown order will be secure against a quantum attack; the whole algebraic approach is inherently not post-quantum secure. Is there a way to do post-quantum VDFs efficiently? We could go back to the hash-based VDFs, but that requires recursive SNARKs. Is there a simple VDF that will also remain secure in the presence of a quantum adversary?
