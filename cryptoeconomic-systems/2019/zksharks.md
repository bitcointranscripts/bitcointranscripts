---
title: ZkSHARKS
transcript_by: Bryan Bishop
tags:
  - proof-systems
speakers:
  - Madars Virza
media: https://www.youtube.com/watch?v=u3Mn27on03A
---
## Introduction

Indeed I am Madars Virza. I am going to talk about SHARKs. I am going to be talking about zero-knowledge SHARKs. It's actually something serious and it's related to non-interactive zero-knowledge proofs.

## Non-interactive zero knowledge proofs

zkproofs are protocols between two parties, a prover and a verifier. Both prover and verifier know a public input, but only the prover knows a secret input as a witness. The prover wants to convince the verifier that some relationship holds between the public input and the secret witness. This might seem very abstract, but it's actually extremely useful.

These properties are typically formalized by completeness--- meaning that true statements have proof, and soundness--- false statements do not. Finally, there is the property of zeroknowledge. The verifier learns nothing about the secret witness beyond what is implied by the membership language. This is usually how non-interactive zero-knowledge works.

But what I have told you is a lie. There is a theorem that this is impossible for interesting languages like NP languages, without any help at least. It becomes possible if you allow yourself some kind of common reference string (CRS). There is a one-time trusted setup that outputs a reference string. This reference string can be used many times by the prover and the verifier and prove the statements respectively.

## Deploying non-interactive zero-knowledge systems

So you have provers and verifiers that are geographically distributed. The question is, who generates the CRS? If it's generated maliciously, then the security properties break down. It's usually done in a cetralized setting. Maybe it's in your IT department that generates the CRS. If you want to use decentralized applications for your proof systems, then we better find out some way to generate a CRS.

The good news is that for many proof systems, the CRS is actually random. Many proof systems have a random CRS. Many things look random like sun spots, stock market, or heuristics like sha256(0) or sha256(1). So we could instantiate bulletproofs by using a CRS but we're going to get it from sha256 or something.

But there's also bad news: the most efficient proof systems have complex common reference strings that are not exactly random.

## Non-interactive zero-knowledge landscape

On the one hand there's NIZKs and non-pairing-based SNARKs like bulletproofs, STARKs, Hyrax, Aurora, Spartan, etc. Then there are pairing-based SNARKs like PGHR13, Goth16, Libra, Sonic, for which the CRS is complex and it reasons about the computation template and does tests based on this. In practice, the ones without any kind of secret setup tend to have slow verification (as statement grows) and/or large proofs. Bulletproofs are really nice for small statements like rangeproofs, but if you want to prove things about a million gate circuit then verification would take like a second. But STARKs are great but they have proofs that are 100s of kilobytes.

With the computation template and complex CRS have quick verification and very small proofs in the range of 100s of bytes. Given that efficiency is desirable, maybe there's a way to get around the trusted setup.

## Ideal world

In an ideal world, we would have someone trusted like maybe your IT department does it. But in a real world, we're going to have many participants each of which contributes a share to the trapdoor of the setup. Then out comes the common reference string as a result. You would want the ideal world setup and real world setups to be the same. This can actually be achieved.

The good part about this is that the constructions only require single point of success. It's not a single point of failure as in many systems, but rather we only need at least one participant to be honest and then the CRS has really been setup correctly. Collusion is probably likely to happen if certain individuals are in a room generating the setup like Putin and Trump and Snowden and Hillary or something.

## Are ceremonies secure?

Are these ceremonies secure? Is the trapdoor secure? I don't think anyone seriously thinks that 50 or 100 people ceremony had participants compromised or colluding. At the same time, there's an epistemological question like why should I believe that those 100 participants even existed? Do I know? In a hundred years, it becomes a myth. Did it really happen? Do I know anyone who participated? In 100 years, will anyone remember the prominent cryptographers from 2019? Maybe I should accept slower verification, or lower efficiency? Does it matter?

There are scenarios where efficiency does matter. Sometimes the propagation speed and verification speed do matter. The propagation speed is dependent on how fast they can verify the transactions. There are also other participants in the system like miners or block producers. They need to get transactions fast and include them in blocks. Even more so, you need to verify the previous block to decide what to mine on top of. So verification is a security risk, there are incidents where people were doing SPV mining and they figured signature verification was too expensive so they turned it off or something. Ideally we would like miners to not do that.

## zkSHARK: zero-knowledge succinct hybrid argument of knowledge

zkSHARKs have short proofs that can be verified in one of two ways. There's prudent verification which is asymptotically slow, comparable to bulletproofs, but do not require any kind of trusted setup. Then there's optimistic verification which is fast (comparable to pairing-based SNARKs), but it relies on a trusted setup ceremony. During transaction propagation, the idea is to optimistically verify the transactions. Miners would then do prudent verification. They would verify provisionally using the optimistic mode, and then later before proof-of-work they do the slow verification.

## What happens if prudent verification fails?

What happens if optimistic verification passes, but prudent verification fails? This can be detected in real-time. You can immediately see that this pair of transactions, where the prudent proof didn't verify but the optimistic one did, is a fraud proof. This is irrefutable proof that something fishy is going on with the setup. Once you see this, you revoke the setup parameters. In zkSHARKs, you can recover soundness by prudently verifying and then you recover efficiency by redoing the setup. The good part about zkSHARKs is that the optimistic proofs can be generated by anyone without the original sender or original witness. In 100 years, we might not remember who the greatest cryptographers of our era, but maybe their new guys can be the participants of this system, and they would be able to refresh all the old proofs.

## A (broken) generic SHARK construction

Someone might think, well, isn't this the same as concatenating in parallel an existing proof system without setup like bulletproofs and a typical snark like Groth16? Well let's see. Say this is a standard proof system where someone produces a proof and someone verifies it. I am going to construct a snark for a fixed language and construct a NIZK for that fixed language. Maybe this SNARK proof can serve as my optimistic proof, but it can't. Optimistic proofs should be refreshable without knowing the witness. Those proofs, if I want to refresh them, then I necessarily need to know the witness to run the SNARK prover. So SHARK is not just two proofs yanked together side by side.

## A generic SHARK construction

Say I have a fixed language... then I construct a SNARK for the langauge that the NIZK verifier proving that the NIZK verifier was satisfied. My SNARK proof reasons about NIZK verification and it doesn't need to know the witness because my NIZK verifier doesn't need to know the witness. So if you give me any two proof systems one with trusted setup and one without, then you can get a SHARK.

That's nice, but it's not too excited from an efficiency perspective. You could do it, but it is going to be challenging to get an efficient SHARK out of it. But say I took bulletproofs and a NIZK and Groth16 SNARKs. Well, my prover starts by reasoning about a circuit of some size. Bulletproofs prover, well, it does some operations and the bulletproofs verifier actually does security parameter times the security circuit size group operations and then it needs to embed this bulletproof verifier. While we get some speedup with mod exponentiation and what not, your SNARK verifier is going to take up ... and if your security parameter is 256, then the constants are pretty accurate here, it's likely not going to be efficient.

## Efficient SHARK construct

We can get a lean SHARK by working directly. We first start by making a NIZK for R1CS which is basically a language for arithmetic circuits with bilinear gates. We do this by presenting a new technique for linear PCPs (LPCPs) in a prudent mode proof system for a public coin NIZK. In order to do this, we also produce an optimized variant of bulletproofs inner product argument. Our proof system is tailored so that-- it has an "algebraic heart" so we don't need to do generic embedding into a SNARK prover, instead we can construct a special SNARK that only knows how to make statements about our NIZK verifier. It's a special-purpose SNARK, and we introduce encoded polynomial delegation to achieve a special purpose SNARK and avoid the lambda squared blow-up in the construction. And that's our SHARK.

While you're waiting for the eprint, you can watch this other talk with more details.

<https://youtube.com/watch?v=OP8ydUxAVt4>



