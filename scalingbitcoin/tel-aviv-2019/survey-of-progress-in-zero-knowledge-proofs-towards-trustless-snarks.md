---
title: 'A Survey of Progress in Succinct Zero Knowledge Proofs: Towards Trustless SNARKs'
transcript_by: Bryan Bishop
tags:
  - proof-systems
speakers:
  - Ben Fisch
date: 2019-09-11
media: https://www.youtube.com/watch?v=-gdfxNalDIc&t=1752s
---
<https://twitter.com/kanzure/status/1171683484382957568>

## Introduction

I am going to be giving a survey of recent progress into succinct zero-knowledge proofs. I'll survey recent developments, but I'm going to start with what zero-knowledge proofs are. This is towards SNARKs without trusted setup. I want to help you get up to date on what's happening on with SNARKs. There's an explosion of manuscripts and it's hard to keep track.

One theme is the emergence of polynomial commitment schemes which is an efficient tool for building transparent SNARKs without trusted setup.

At the end, I will announce a new trustless polynomial commitment schemes based on fresh work that we will be posting with my coauthors Benedikt Benz and the others in a few days.  The result of this work is the ability to build trustless SNARKs.

## Zero-knowledge SNARKs

It's a zero-knowledge succinct non-interactive argument of knowledge. The relevance of SNARKs is both a scaling technique both for verification and also it's a privacy tool. When you're doing zero-knowledge proofs on large statements, then SNARKs are what allow you to produce a small proof on the blockchain even if you're proving a large statement. Right now, anonymous transactions on zcash---- without doing trusted setup would be nice.

So what is a SNARK? It is a non-interactive proof. When a prover sends just one message to a verifier, it then proves abstractly anything which is a relation that can be computed by a polynomial sized-- in other words, an efficient circuit in class NP. If I have a witness with a statement saying here's an encrypted confidential transaction and here's the secret information you would need to verify this information in the clear, then you could verify my proof instead that if you had the vital information then you could verify that my statement is true.

Succinctness is that the proof size is small, so polylogarithmic, in the size of the circuit that computes this statement in the first place. If they have a long amount of secret information, instead of sending it in the clear, they can just prove the statement. Efficiency is about the verification time. The verifier doing only a small amount of work to verify is an important goal.

Knowledge extraction says informally that basically if the prover succeeds in convincing the verifier of this statement, then the verifier knows that there is extra information that makes the statement true. This is a very strong security property that implies more. It shows that the prover actually knows the secret information that makes this information true.

Zero-knowledge says that basically the interaction or the proof doesn't reveal anything about that secret information.

## Transparent setup

Sitting on the side, there's been this setup procedure at the top of my diagram. It's there because some SNARKs in fact all efficient SNARKs today really involve some kind of setup of public parameters.

The setup is called transparent if it involves no secrets. Anyone can verify the setup was done correctly. It's publicly verifiable.

Another thing to talk about is pre-processing SNARKs. Maybe the verifier needs to in order to be able to trust the system in a trustless way, then for any given circuit that is being proved, it needs to at one time do a large amount of work to verify that some preprocessing was done correctly but then later when verifying multiple instances of the same statement it would not need to do so much work. So we still get an efficient verification.

## Genesis: PCP theorem

Let's now talk about where SNARKs began.

In the beginning, there was nothing. Then there was the PCP theorem. It's one of the crown jewels of computer science. In the hebrew year 750, I think, in 1990, Ben Fisch was born. 1990 BFL. There was also the first version of the PCP theorem which says that any exponentially long proof can be proved with only polynomial long information. Any polynomial sized proof can actually be checked only at a constant number of locations usually a log(n) amount of randomness.

The PCP theorem says that basically anything that I would want to prove to you, I could give to you, and if you had random access to that proof-- you have oracle access to the proof and you're reading a single bit of a proof is just a O(1) operation, then you only have to do a constant amount of work to verify this proof and you only need to lookup a constant amount of locations.

## CS proofs

CS proofs were computationally-sound proofs, the first step towards SNARKs. The idea was to commit to this PCP proof with a merkle tree. Then when the verifier wants to look up some location in the proof, then the prover can simply give merkle inclusion proofs that they are reading the correct location. They would give a merkle proof to show the correctness of the version.

This can be made non-interactive using the Fiat-Shamir transform. The interactive version would be the prover sends the merkle tree root and then the verifier sends random challenges of where they want to check the proof. The prover would provide merkle inclusion proofs for the query location. But this can be made non-interactive by using a hash applied to the first messages in the interactive version.

## Cryptographic compilation

This paradigm will appear over and over again. We can look at all constructions of SNARKs as taking an information theoretic proof system and adding some kind of cryptographic compiler of that in order to turn it into something with the properties of a SNARK. We can apply merkle trees and random oracle hashes and fiat-shamir transform in order to turn this thing into a SNARK.

## Linear PCP

Are there other kinds of PCP theorems that might provide more power other than checking individual locations of the proof? PCP is actually a function. So the prover would send to the verifier a vector, and let's say the verifier has the ability to make queries that return inner products of that vector with that query. This is called a linear PCP.

Indeed, one of the stepping stones towards efficient SNARKs was a result in 2007 by Ishai and Ostrovsky showed a linear homomorphic encryption version and gave this quadratic proving time. It wasn't a merkle tree construction, it used a more powerful technique called linear homomorphic encryption to turn it into a SNARK. Unfortunately this initial work had linear verification time and quadratic proving time.

## QAPs and GDPR

It was a stepping stone towards GDPR and QAPs.

* GGPR 2013
* Quadratic arithmetic program instnatiation of linar PCP
* Lipmaa13, BCIOP13, BCTV14, CFH.....

## QAPs (GGPR)

There's QAP-based linear PCPs. It's exactly following this idea of designing an information theoretic protocol where the verifier makes inner product queries to some vector that the prover has. This is compiled using something called linear-only encoding. Because of the properties of QAP, they are able to get down to log(n) proving time and linear verification time.

## R1CS example

There's a bunch of polynomial matrices and the witness, the secret witness-- of the first witness- the input. You just need to show that the circuit will be satisfied if this constraint equation is satisfied. You can see that it's basically matrix vector operations except for H(x) times Z(x). THese are matrices of polynomials, so it's not toally linear.

But this is converted into a linear PCP by changing a random point, evaluating the polynomials at the random point, and then you get the matrices, and then basically just five inner product queries and doing some quadratic checks on the result. This is what the R1CS linear PCP looks like.

## R1CS preprocessing SNARK

Push the secret queries normally made by the verifier into some preprocessing step. Like this hidden random that was chosen by a trusted seutp; it's compiled int oa SNARK by using linear encoding to force the prover to apply those queries to the witness factor that they commit to. This approach appears to fnudamentally require this trusted non-universal setup.

Non-universal means that for every circuit when the queries change, you have to do a new trusted setup to push everything into the preprocessor.

## Interactive oracle proofs

Going back to the original Mckaley proofs based on classical PCPs, there was interesting work going on making tha tapproach of these weaker PCPs more practical. The problem was that the original PCPs were beautiful in theory but not in practice. We introduced the notion of interactive oracle proofs simultaneously by BCS16 and RRR16.

They noticed that you can get a lot more powerful if you allow interaction, like multiple rounds of interaction, and in every round the prover would send some PCP or proof oracle that the verifier just is able to check with random access to a few locations.

If you were to apply cryptographic compilation techniques to that, then you get a multi-round public protocol involving merkle trees and that can be compiled into a SNARK as we saw before. Multiple rounds allows for greater efficiency. Another nice thing is that these weaker PCPs, the compilation techniques are also very basic using hash functions and merkle trees compared to linear PCPs which involve more heavyweight cryptography. They tend to be not as efficient in proof size, but more efficient in operations and work being done.

## STARK, Aurora

Two state of the art results in this line of work are STARKs and Aurora. Each of these have seen further developments since they were introduced. STARKs work for uniform programs or many repetitions of a small program done many times over. Aurora is more for general circuits. Both have log squared sized proofs. STARKs has linear verification but only for uniform programs, which Aurora has as well, but unfortunately Aurora has linear verification time so it's not a SNARK under all definitions yet.

## Interactive linear PCPs?

What about allowing interaction for the more powerful PCPs like the linear PCPs? QAP was not really interactive. What if we allow multiple rounds of interaction where there are multiple rounds of challenges from the verifier, and each round the prover is sending -- proof to the vector, that the prover can then make linear queries to. We call these linear interactive oracle proofs. Linear IOPs.

## Polynomial interactive oracle proofs

One special case is a polynomial interactive oracle. It's a polynomial PCP where the--- the information theoretic protocol sends polynomials, the verifier wouldn't have to read the whole polynomial, but would receive oracle access for evaluating that polynomial at some point. If you want to read queries like, the coordinate query like in calssical PCPs, there's a generic reduction that replaces the coordinate query with a 2 round polynomial IOP.

Polynomial IOPs sit between point PCPs which are short, and linear PCPs. The polynomial can be represented as a short PCP as well. There's actually a lot of the modern work in point PCPs you know, use polynomials as well in the way that they actually work.

## Polynomial interactive oracle proof compilation

The recent general paradigm is compiling polynomial IOPs using something calling a polynomial commitment scheme. The process to take a polynomial IOP-- every time the prover would send a polynomial to the verifier, he sends instead a polynomial commitment, and this is applied to the compiler to turn this into an interactive argument that doesn't involve these oracles. Then it can be compiled into a SNARK using the fiat-shamir trick.

## Polynomial commitment scheme

KZG 2010

There's a setup, commitment and opening. The key new thing is an interactive protocol that allows you to prove that the polynomial is evaluated at some point is equal to some claimed value.

The efficiency requirement is that this interactive protocol should have communication which is sublinear in the size of the polynomial otherwise you could just send the polynomial. And the commitment should be small, like constant size or a single proof element. It would also be nice if the interactive protocol is a public coin, which  could then be transformed into a non-interactive protocol.

You shouldn't be able to open the polynomial at two different points. Argument of knowledge would be nice as well, showing that you have validated the polynomial correctly, then you actually know the polynomial.

## Transparent setup

The transparent setup would be just as before, probably some setup that doesn't have secrets. PRevious construction form Kate te al form bilinear groups had a trusted setup. That has to be done by some trusted party.

## Sonic: Polynomial interactive oracle proofs for NP

The underlying result in the Sonic paper is that it shows how you do a polynomial interactive oracle proof for any NP computation that makes just one bivariate query and three univariate queries of the degree size of the circuit polynomials, and it's two rounds. This can be transformed into a five round polynomial IOP, with 24 overall univariate queries. If you apply the Kate commitment scheme out of the box, then you get a SNARK with a one-time setup and it can be compiled in the way I described previously to turn this information theoretic interactive polynomial protocol into a something and then can be transformed into a SNARK.

## Sonic: Uniform circuits

...

## Sonic: Universal setup

It gives you universal setup and ... processing time per circuit.

## Sum-check

A lot of the other work is based on the sum-check protocol from LFKN 1990. It's a classic protocol from the 1990s. Don't worry about the details. You can think of this protocol as a polynomial IOP as well, because every round the prover sends the polynomials and the verifier does a few checks, and at the end evaluates the polynomial at a random value. You can look at these polynomial PCP oracles, and making some oracle queries.

## GKR interactive proof

This GKR interactive proof works by defining a polynomial at each level of the circuit which basically just says, ... if this is an addition gate then ... just add the input gates, add the two gates, if you have a multiply gate then you multiply. It has a recursive definition of what a polynomial... encodes each layer of the circuit. Then each of these can be replaced with a sum-check protocol which is done kind of recursively. What you end up with is O(d log|C|) where d is the depth of the circuit, which can be done efficiently if you have a low-depth circuit. The queries are on low degree polynomials, i.e. you can read the polynomials entirely in the clear. This has to do with the way that it was defined- polynomials turn out to be low-degree polynomials and you don't need the machinery I discussed before.

This GKR isn't zero-knowledge, XZZPS 2019 tried to make it zero-knowledge by adding some small random masking protocols ((polynomials)). These end up involving polynomial commitments because you get larger degree polynomials than normal.

Hyrax 2017 WTsTW has .... so it's not really..

Finally, Spartan and Clover and BFL..... BTVW 14 and BFL 91... Spartan used, you can represent the satisfiability of an arithmetic circuit using this sum over all values in this boolean hypercube of this polynomial g. So what you get from Spartan is a thoerem that there exists a polynomial IOP that involves a logarithmic number of rounds, but really just 3 queries to the log C variate polynomial oracle, and one query to each 3 log C variate polynomial roacles. For uniform circuits, only three queries to a log C variable polynomial. Using previous work, this can be done with square root sized proofs and linear proof of time.

## Recent comparison

I took this straight out of Libra which was a comparison of different sizes reported in XZZPS 2019. You can see the most efficient SNARKs which require a trusted setup, smaller than a kilobyte, to the ones based on classical IOPs which are closer to the 400 kilobyte range, as well as things in the middle.

## Transparent setup polynomial commitment schemes

We have a polynomial commitment schemes from groups of unknown order. We instantitate this with class groups, and we get traqnsparent setup and a few other nice properties. If you apply it with Sonic, we get what you call Supersonic. It's a trustless setup SNARK with log n proof size and log n verification, quasi-linear prover time + preprocessing. It's 24 kb proof size for 1 million gate circuits. Further optimizations are possible. It's not as good as using libsnark, but it's currently better than the state of the art for the other trustless setups.

Alan will be talking about this next week at Starkware Sessions. Thank you.

