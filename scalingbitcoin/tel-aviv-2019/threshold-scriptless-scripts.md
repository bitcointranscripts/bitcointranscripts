---
title: Threshold Scriptless Scripts
transcript_by: Bryan Bishop
tags:
  - research
  - adaptor-signatures
  - threshold-signature
speakers:
  - Omer Shlomovits
---
<https://twitter.com/kanzure/status/1171690582445580288>

## Scriptless scripts

We can write smart contracts in bitcoin today, but there's some limitations. We can do a lot of great things. We can do atomic swaps, multisig, payment channels, etc. There's a cost, though. Transactions become bigger with bigger scripts. Also, it's kind of heavy on the verifiers. The verifiers now need to verify more things. There's also privacy issues because you put your contract publicly on chain.

We want the same functionality but without actually using smart contract scripts. We want to use regular transactions using the primitives of public keys and signatures.

## Agenda

I am going to introduce Scriptless Scripts using Schnorr signatures in the way they were originally described. Schnorr is not yet supported in bitcoin but we're going to describe how to do this with ECDSA which is currently deployed on bitcoin. We'll ask some questions like why is ECDSA different from Schnorr? Once we get done with this, then I want to talk about some known issues with 2p-ECDSA. It's going to be about threshold cryptography and threshold signature are dealing with similar problems. Eventually we will see a big list of experiments that we can do today with using the ECDSA for Scriptless Scripts toolbox ESS. I hope to convince you that this is efficient and secure to do it today.

## Schnorr signatures

Let's first look at Schnorr signatures which is useful for scriptless scripts and we'll compare against ECDSA. So we choose a random k, then we compute R = k * G. We compute the signature as k + the hash of R, P and m.

## Adaptor signatures

For scriptless scripts, there's a shtik. It's adaptor signatures. Basically we're taking a Schnorr signature and we're writing s' which is the addition of this Schnorr signature with the adaptor little p. As it turns out, using this shtik we can --- all the other-- ...

## Scriptless script atomic swap

This is the canonical example of scriptles s scripts. Say you want to trade bitcoin for litecoin on-chain. So the wallet sends some information about the adaptors, and the prime is the signatures in the ... public key.. is not known public key... Using this information, they can't do anything but make sure that the signatures are indeed adaptor signatures. But so now, what you do is send two signatures, two Schnorr signatures to wallet A. Using this signature and his own signature on litecoin, for s-a, wallet can get the coins on litecoin. Publishing s-a will now allow the other counterparty to do this computation and extract a secret and use it to compute on s-a' and he can now get the bitcoin.

There are many more examples beyond atomic swaps. This is just the basic idea of how it works.

There's a list of open questions about this. We will focus on the ECDSA support question. There was a slide from a few years ago that Andrew Poelstra gave in a talk.

## ECDSA scriptless scripts: the hard questions

What's wrong with ECDSA that we needed Schnorr? And we need to understand how to implement with ECDSA because we'll see it's not as simple as using Schnorr signatures.

## ECDSA vs Schnorr signatures

Schnorr signatures are considered more simple than ECDSA. There's a few more differences. One is that as you can see when you compute this s value, in ECDSA we're using this non-linear term where we take the inverse of the nonce, and under the hash function in ECDSA it's just a message but in Schnorr it's also the point out. Eventually the signatures look similar. In Schnorr it's a point, and in ECDSA it's .... a modulo...

ECDSA has no security proof, it's malleable, and not linear. EC-Schnorr is provably secure under ROMDL. Provably non-malleable, and it has linearity property.

So is ECDSA a no go? That slide was from Pieter Wuille.

## ECDSA: no security proof?

ECDSA has been around for many years. The analysis of ECDSA has become better and better. There's a paper "The security of DSA and ECDSA" which proved security but under a different model. In 2003 there was also the generic group model. We're missing something from ECDSA, specifically .... non-algebraic. This is something we're ignoring when we use a generic group model. We can say this is not perfect, but moving forward a few years there's another paper "On the provable security of EC(DSA) signatures". This is more close to reality. Also 2016 bijective random oracle BRO model. This is getting us really close to a very good security proof, we can already make some claims based on this security proof. What we can assume is that the more we use ECDSA then the analysis will become more and more tight.

ECDSA is one of the most widely used signature schemes like in TLS, PGP, S/MIME email, multiple cryptocurrencies, etc. There's also wide standardization in IEEE P13636, ANSI x9.62, FIPS 186-4. It is also subject to massive cryptanalysis efforts.

## ECDSA: malleable?

Malleability means that you can change the signature to get another valid signature on the same message. There's malleability in ECDSA. What the paper I just described showed you, there's ECDSA prime which can eliminate this malleability and it's strongly unforgeable. We define ECDSA prime which fixes it. This is one way to solve malleability. There's bip62 which is doing exactly this, fixing it to ECDSA prime. Using segwit, we kind of also dealing with the transaction malleability which can also effect it. So I would say the malleability is manageable.

## Schnorr signatures: malleability?

For a Schnorr signature, we can prove non-forgeability. But in practice, Schnorr is not as standardized. There are many different variants of Schnorr signatures which have different verification schemes. Bitcoin has bip-scheme and also another blockchain uses a different type of Schnorr signature.  What's the right standard to use for Schnorr signatures?

There's EC-SDSA, EC-SDSA-opt, EC-FFSDSA, EC-Schnorr, and many others.

## Linearity

This is definitely a valid point. There's an inverse of k, this is an issue with ECDSA that does not exist in Schnorr signatures. Given the non-linearity of ECDSA, are scriptless scripts possible? Is it possible but inefficient? Or is it possible with compromising on security? Maybe we need to introduce new security assumptions into the equation?

## Linearity: observation

Threshold ECDSA struggled with the same problem of linearity. It's not surprising that looking at existing solutions for ECDSA scriptless scripts, they are based on threshold ECDSA.

## Scaling Bitcoin 2018

We gave a talk on "Instantiating scriptless 2p-ECDSA". Clasiscally you can replace a multisig with a single sig using 2p-ECDSA. Then there was "[Anonymous multi-hop locks for blockchain scalability and interoperability](https://eprint.iacr.org/2018/472.pdf)". They define scriptless scripts over ECDSA by constructing this adaptor signature from Schnorr but for ECDSA. To do this, they also needed 2p-ECDSA. So it's common to both of these.

Fast secure two-party ECDSA signing (Yehuda Lindell)

## Threshold ECDSA signatures

2p-ECDSA is an instance of threshold ECDSA protocols. Then I'll explain the two-party ECDSA protocol. Is it efficient? Should it be used? How can we build on top of it and others?

Threshold signatures are described as two protocols. It's key generation and signing. We have two parameters m and n. We need first a setup phase where we generate the key. (t,n) threshold signature scheme distributes signing power to n parties such that a threshold of the parties can sign.

## Two-party keygen from Lindell 2017

https://github.com/KZen-networks/multi-party-ecdsa

There's key exchange where at the end both parties agree on some public information, but then there's an ... we need to define or use a different... it adds some specific properties of homomorphism. I'll mention it in a second. It basically uses this.. property... that there's no leakage of x1 and x2.

What can we do with this? Well, we can sign. We basically run another diffie-hellman key exchange to get... and then we do this kind of computation to... this is what I mentioned before. This is specifically.. this kind of... but eventually one party will send... and the other party will do some more computation.. and be able to... such that verification will succeed. We calculate that this is unforgeable so that no single party can forge a signature without having access to both parties at the same time.

## 2p-ECDSA lock using MMSKM18

https://github.com/KZen-networks/multi-hop-locks

This is how to do adaptor signatures in ECDSA. The change is really minimal. When you're generating some random point, instead of using the generator of the elliptic curve, we just use the .... in order to... eventually the adaptor would be s', which is not an addition--- and multiplication. Multiplication is possilbe given you have s' and you need to do the inverse of t. It's similar but different.

## Possible issues

We see it's definitely possible to use ECDSA scriptless scripts because we have ECDSA adaptor signatures and we can build other protocols on top of it.

What about efficiency? We first did this key generation setup. It might be restrictive. There's also signing and this homomorphic computation that we need to consider, and also interaction.

What about securtiy? The protocol is secure, but there's a new cryptograhpic assumption and that might compromise the security.

There's another issue.

It might be bad news. But I want to declare it's not bad news. This is much much bigger than a single protocol. There's so many threshold ECDSA papers since 2017. Ther's also ECDSA and class groups assumption used in CCLTS19. I just want to claim, choose the right protocol for the right use case. There are many ways to try to analyze the differences, and basically it's the work that should be done when you want to use a specific one for a given use case. There are other protocols that are using othe rtypes of security assumptions, and it might be that your system is already making one of the same assumptions so it might be okay to use that assumption.

We can build threshold ECDSA without any new security assumptions on top of ECDSA in a few of these.

What about interaction? There's a setup phase, let's say it's a one time thing.

papers: [L17](https://eprint.iacr.org/2017/552.pdf), [GG18](https://eprint.iacr.org/2019/114.pdf), [LNR18](https://eprint.iacr.org/2018/987.pdf), DKLS18, [DKLS19](https://eprint.iacr.org/2019/523.pdf), [CCLST19](https://www.math.u-bordeaux.fr/~gcastagn/publi/CRYPTO19_2pECDSA_extended.pdf), SA19, [DKOSS19](https://eprint.iacr.org/2019/889.pdf)

params: 2/2, t/n, t/n, 2/n, t/n, 2/2, n/n/, t/n

There's also open-source code for some of these. Some of these results are very new and the code isn't written yet. There was one paper presented a few weeks ago. There's a setup phase. They are assuming class groups which is a different assumption. But the security proof is much more tight. This is an interesting candidate.

## Experiments

I want to just describe a few of the experiments and what we can do with these tools.

With multisig using threshold ECDSA, we get privacy. The transaction looks completely regular. The on-chain cost is the same as a single signature transaction. We can even take it further, there's open-source code links here on the slides: http://github.com/KZen-networks/multi-party-ecdsa.

We can also do a threshold ECDSA wallet. It's possible. There's key derivation in there and so on. github: [gotham-city](https://github.com/KZen-networks/gotham-city) [blockchain-crypto-mpc](https://github.com/unbound-tech/blockchain-crypto-mpc)

Another use case is coinjoin mixer. This is a byproduct. Coinjoin is basically where multiple people agree on inputs and outputs and they add their own inputs and outputs. Chaumian coinjoin can achieve this coordination in a more structured way. It's also possible to structure the way-- it's a coordination game for key generation, each one party can generate a local view and also... so maybe we're... way to get this consensus between parties off-chain that can later be used without a central authority. https://github.com/KZen-networks/ShareLock

Another use case is atomic swaps. We can use scriptless scripts and adaptor signatures. But another construction depends on access structure secret shares can be swapped using "gradual release of secrets". This is not a perfect atomic swap, though. github: [atomic-lock](https://github.com/scriptless-scripts/atomic-swap), [centipede](https://github.com/KZen-networks/centipede/).

Another one is to use a payment channel network. This is the anonymous multi-hop locks paper that was mentioned earlier.

Finally, a few years ago was a "[Efficient zero-knowledge contingent payments in cryptocurrencies without scripts](https://eprint.iacr.org/2016/451.pdf)". They used 2p-ECDSA not the Lindell way but another way. This was a zero-knowledge contingent payment where it's an atomic swap but instead of switching one coin with another, you switch one coin with a proof of some statement. They jointly sign this transaction, and there's a zero-knowledge proof that the solution is encrypted by the signature. You get this information once the signature is broadcasted. This is really interesting and can be done today.

## Research

https://github.com/KZen-networks/white-city/

We're in a good place because this threshold cryptography is in [a standardization process by NIST](https://csrc.nist.gov/Projects/Threshold-Cryptography). There's some underlying assumptions on the network layer, like authenticated secure p2p communication and a broadcast channel. We had one idea of using the blockchain as the broadcast layer. It would be nice to have better accountability, and batch signing and verification.

## Summary

Threshold ECSA based scriptless scripts are practical today. They are possible now, they are practical to use in real life, and they hold strong security gaurantees and the focus of active research in the cryptography community.






