---
title: FROST
transcript_by: Michael Folkson
tags:
  - threshold-signature
speakers:
  - Chelsea Komlo
  - Elizabeth Crites
date: 2022-08-07
media: https://youtu.be/tWopcFzSTas?t=11604
---
Location: Zcon 3

FROST paper: <https://eprint.iacr.org/2020/852.pdf>

Sydney Socratic on FROST: <https://btctranscripts.com/sydney-bitcoin-meetup/2022-03-29-socratic-seminar/>

## Introduction

Elizabeth Crites (EC): My name is Elizabeth Crites, I’m a postdoc at the University of Edinburgh.

Chelsea Komlo (CK): I’m Chelsea Komlo, I’m at the University of Waterloo and I’m also a Principal Researcher at the Zcash Foundation. Today we will be giving you research updates on FROST.

## What is FROST? (Chelsea Komlo)

You might not know what FROST is and that’s totally ok. What FROST is is a flexible round optimized Schnorr Threshold Signature Scheme. FROST was designed by myself and my collaborator Ian Goldberg in 2020. FROST is actually two things. First FROST introduces a distributed key generation (DKG) protocol which later we’ve come to know as PedPop. Second FROST introduced a 2 round threshold signing protocol which is concurrently secure. This is what FROST is known for because it was really the first in its kind. Threshold signatures before FROST were either 3 round or they were insecure when signing sessions were performed concurrently. This is the first of its kind in the literature. What is interesting to this community is that FROST was designed with the Zcash ecosystem in mind. We had people come and gather requirements from the Zcash community and presented those requirements to us. That’s where FROST emerged from. But now it is being adopted as an industry standard. We designed something for this ecosystem but it turned out to be a problem that needed to be solved at large.

## What are Threshold Signatures?

I’ve been talking a lot assuming you know what threshold signatures are but you actually might not. Let’s see what those are very quickly. A threshold signature scheme is a public, private scheme. Like any public, private scheme there is a public key that’s used for verification but unlike single party signatures the signing key is actually partitioned amongst some set of signers. Here I am showing you a 2-of-3 example. What that means is you actually only need some subset of signers to participate in order to issue a signature. That’s nice because say one of the signers takes off on their motorbike into the mountains you can still have some set of signers be able to issue a signature. What is interesting about this is signers sign using only their secret share. The full secret is never reconstructed.

## Uses for Threshold Signatures

You might say this is really interesting magical cryptography, where would we actually need threshold signatures? There’s actually a lot of places where you might want them. First and foremost banks and exchanges are very interested in threshold signatures. Also cryptocurrency wallets are also interested, you might want to take your signing key and partition it among many devices. Then finally for trust authorities you might want to partition trust among many authorities as opposed to a single authority.

## Where was FROST last year?

I presented FROST at Zcon last year so this is a reoccurring topic and something we’ve been working on at the foundation for quite a while. Last year when I presented FROST we had published the paper, I will refer to that original variant of FROST as FROST1 going forward, and I also presented FROST to NIST. NIST was having a workshop on standardizing threshold signatures, I presented FROST there and gotten good feedback. Finally we had started a IETF draft on FROST because there is so much interest outside of the Zcash ecosystem so we decided write it up in a generalized way.

## Where is FROST now?

Now let’s look at where FROST is today at this Zcon. I have checked on GitHub and there are at least 5 public implementations of FROST. There are probably more private implementations but there is not just our implementation, other people have implemented it as well. We have an optimized FROST2 that Liz will be talking about in a little bit. We have additional security proofs. What is nice about this is we wrote a security proof but there is now independent security proofs validating our result of the security of FROST. Our IETF draft is almost done, we are starting to request feedback and we are hoping to wrap this up quite soon. There are other protocols (e.g. [ROAST](https://medium.com/blockstream/roast-robust-asynchronous-schnorr-threshold-signatures-ddda55a07d1b)) that are starting to build on FROST as a building block. I’ll talk about this in a bit but this is one example of some research that is taking FROST as a building block and incorporating it into higher level protocols. What is interesting is PedPop is being used in the context of other threshold signatures. I know PedPop is being used in the context of threshold BLS for example. Currently at the foundation we are working on unlinkable FROST. I’ll talk about this later but we are taking FROST and incorporating it for the privacy guarantees that the Zcash protocol provides. Then finally the gold standard for cryptography is that FROST is being used practically. Coinbase published a [blog post](https://blog.coinbase.com/frost-flexible-round-optimized-schnorr-threshold-signatures-b2e950164ee1) where they talked about their use of FROST and I’ve talked to many other practitioners who are deploying FROST today. That’s the most important validation we can have. I’ll pass it off to Liz.

## Introduction (Elizabeth Crites)

I’d like to take this opportunity now to discuss some of the details about how we uncovered a more efficient version of FROST called FROST2 and how we proved its security. In addition to FROST we also proved the security of a range of multiparty Schnorr schemes. We proved some multisignatures in which all n parties are required to sign the message and also some threshold signatures like FROST2 where some threshold is required. This is joint work with Chelsea and Mary Maller.

## (Single Party) Schnorr Signature Scheme

Before we get into multiparty Schnorr I just want to recap how regular single party Schnorr works. Alice here is going to sign a message, the first thing she does is generate her key. She samples her secret key (`sk`) uniformly at random from a field and her public key is the generator raised to this secret key. In order to sign a message `m` she is going to sample a nonce, she samples this little `r` value uniformly at random from the field and again raises that value using the generator. The nonce I will refer to as this `R`. She then forms a hash value including the following: it includes her public key, the message she’s signing and her nonce. The output is this value `c`. She forms part of the signature `z` using the little value `r` plus this hash value `c` times her secret key `sk`. The full signature consists of her nonce `R` and the little value `z`.

The verifier can check the signature as follows. First it computes the hash value `c` taking as input the key `PK`, the message `m` and the nonce `R` and checks this verification equation.

`R . (PK)^c = g^z`

You can tell that this looks exactly like the equation for `z` if you took some generator `g` and raised it to that value. The verifier then outputs accept if this equation holds.

## Attempt: Multi-Party Schnorr

Now let’s make an attempt to build a multiparty Schnorr signature scheme. I’m going to have a few simplifications here. In particular I’m only going to consider 3 signing parties and all 3 of them are going to be required to sign. This is the multisignature setting. I’m also going to include a combiner, this is just for simplicity. This combiner is not trusted, it just makes things a little bit cleaner. The attempt would be how about everybody just generates a regular standard single party Schnorr. They form their nonce as before, each party has this value `R` and they send it to the combiner. The combiner can take the public keys and multiply them together to form the aggregate public key representing the 3 parties. We are going to include proofs of possession throughout this talk. Everybody is going to prove knowledge of their secret key and that is how you can multiply the keys together without any kind of rogue key attack. The combiner also creates an aggregate nonce which is the multiplication of each party’s individual nonce. Then the combiner computes this hash of the aggregate key, the message to be signed and the aggregate nonce. Sends this value to all of the parties and they compute their standard single party Schnorr, just as before. They send these values `z` to the combiner and the combiner just adds them up. The final signature consists of the aggregate nonce and the aggregate value `z`. Critically this verifies exactly like single party Schnorr. You take as input the aggregate key and the aggregate nonce and it looks exactly like standard single party Schnorr. This is important too because in the threshold setting you won’t be able to tell which signers actually signed the message. That’s really important for privacy. Also here with the simplification for multisignatures, for a threshold scheme you would have a key which is output by the distributed key generation protocol and also some Lagrange coefficients thrown in. But this is the simplest thing for us to analyze. The problem is that this is completely broken. There has been a long line of work starting by the original paper by Schnorr who proposed this ROS problem.

## ROS Attack

[ROS](https://eprint.iacr.org/2020/945.pdf) stands for Random inhomogeneities in a Overdetermined Solvable system of linear equations. Never mind that, you can basically think of this attack as a birthday attack or a solution to a k sum problem. The problem was stated in the original Schnorr paper. In 2019 Drijvers et al actually show how to break the unforgeability of the scheme I just showed you along with a range of other multisignatures, threshold signatures and blind signatures. This has a confirmed polynomial time attack which was discovered by Benhamouda et al in 2020. Critically this attack relies on the concurrent setting. What I mean by that is an adversary can potentially open many signing sessions at once. Prior schemes sometimes limited the notion of security to sequential security in order to not be susceptible to this attack. Every signing session would be open and completely closed before moving to the next one. But we are interested in having a system that is secure in this concurrent setting. The trick works like this. The adversary opens multiple signing sessions and they see the nonces of the honest parties first. Recall on the last slide everybody sends their nonces right away. The adversary can wait, see what everybody else’s nonces are and then produce theirs in a clever way. Then they are able to use this to forge a signature.

## Fix 1: 3 rounds

One way to fix this is to add a round. This is a commitment round. The parties will compute a commitment to their nonce first which is just the hash of their nonce value. They send these commitments to the combiner, the combiner sends these commitments back. Again I’m using a combiner but we could have some kind of broadcast where everyone is sending these values to one another. Then at that point they reveal their nonce. Critically an adversary has already had to commit to their nonce so they can’t do this clever trick of using the other nonces they’ve seen. Here again the combiner computes the aggregate public key and aggregate nonce, multiplying everything together and sends the value `c` to each of the parties. Then they compute it just like regular Schnorr. The verification is exactly the same.

## How to Prove Schnorr Assuming Schnorr

<https://eprint.iacr.org/2021/1375.pdf>

This is one of the contributions we made in this work. Consider a 3 round multisignature SimpleMuSig which includes proofs of possession of the keys. And also a 3 round threshold signature SimpleTSig which incorporates the PedPoP distributed key generation protocol that was part of FROST. The main observation that was made in the work that produced FROST was you don’t need 3 rounds, you can get 2 rounds but you have to do something clever.

## Fix 2: 2 Nonces (“FROST”)

I’m calling it FROST in quotations because I am considering the multisignature setting not threshold but the idea is the same. Instead of sending a single nonce you send 2 nonces and each nonce is computed exactly as before `g^r` and `g^s` for some random values. They send these nonces directly to the combiner and the combiner multiplies the keys as usual. But there’s also this additional hash value `a`. The hash takes as input the index of the signer `j`, the aggregate public key `PK`, the message `m` and the set of all the parties’  nonces `R_j` and `S_j`. This is another way to commit to those nonce values because they are all being hashed. You can’t manipulate your nonce value after the fact. Now the aggregate nonce is computed as the product of the `R` values times the `S` values raised to the signer specific hash. The reason that you need 2 nonces, if you had just 1 raised to this hash you could just basically multiply it out. This non-linearity is really critical. From here the combiner computes the hash value `c` as usual, sends it to the parties and then they compute their `z` values as follows:

`z_j = r_j + a.s_j +c.sk_j`

Then they send their value `z` and everything is like before.

`z = z_1 + z_2 + z_3`

`sigma = (R,z)`

`Verify (PK, sigma, m)`

`c = H(PK, m, R)`

`R. PK^c = g^z`

## Fix 3: 2 Nonces (“FROST2”)

The observation that we made for our optimization is that the hash value doesn’t need to be computed individually per signer. You can actually use a single hash value. Here I’ve highlighted it in red. The hash value takes as input the aggregate key, the message and the set of nonces to prevent those ROS attacks. But it doesn’t need to take as input the signer index. What that means is that there is a single hash value. This reduces the number of exponentiations required for signing from `t` in a threshold case to just 1.

This is the second set of contributions we make in this work. We introduce an optimized 2 round multisig called SpeedyMuSig which incorporates the proofs of possession. And also the optimized version of FROST called FROST2 which we proved secure together with the PedPoP distributed key generation protocol. The reason we were able to uncover this optimization was actually a function of the way we were trying to prove the original FROST scheme. This is a new proving framework that we are introducing here in this work. I am going to talk a little bit about how we were able to prove FROST2 secure.

## Proving the Security of Multi-Party Schnorr

Basically these proofs are made difficult by the fact that they are complex interactions involving multiple parties. Then there is also the aspect of trying to extract some kind of solution to some hard problem. For our security reduction we consider the two moving parts. The first one being that you have to simulate honest users to the adversary but you also have to extract a solution from the adversary’s responses to some hard problem. Our idea was to separate these two parts and consider the multi-party aspects separate from the extraction.

This is a high level overview of how our framework looks. We have our 3 round multi party signatures on the left which are SimpleTSig and SimpleMuSig and then the 2 round FROST2 and SpeedyMuSig on the right. These are multi party schemes. We consider an intermediate level of assumptions which helps to separate these two components. The Schnorr assumption just says regular Schnorr signatures are unforgeable. We know this to be true under the discrete logarithm assumption, there are many versions of that proof. But critically that is a single party level so we can actually prove multiparty as a reduction to single party and then use the standard proof from single party Schnorr to discrete log. For the case of the 2 round schemes we have a similar single party intermediate assumption called the Bischnorr assumption. It is a little bit more complex but the same idea holds. You have the multiparty schemes reducing to the single party and then from the single party you are trying to extract the solution to the One More Discrete Logarithm assumption. This is a slightly stronger assumption. In particular the 3 round schemes are interesting from a theoretical standpoint because they only rely on discrete log. Whereas the 2 round schemes require this slightly stronger assumption.

## Stronger Security for Non-Interactive Threshold Signatures (Chelsea Komlo)

<https://eprint.iacr.org/2022/833.pdf>

We did a bunch of work looking at the security of FROST but also other people have done similar work and come to similar conclusions. This is incredibly great. In science we like to have results validated by independent groups. I am going to highlight some recent research that came out this year. It is going to be presented at Crypto in a couple of weeks along with our work. At Crypto this is a merge with the work that Liz just talked about. I’m going to summarize what their work is now. This is a paper called Stronger Security for Non-Interactive Threshold Signatures by Mihir Bellare, Stefano Tessaro and Chenzhi Zhu. What is neat about this work is they actually give a hierarchy of notions of unforgeability for threshold signatures. Prior to this paper there is a standard notion of unforgeability where you assume an adversary controls, depending on the protocol, `t-1` corrupted players and there is some number of honest players. What this paper does is it takes that notion and makes that the base notion and creates stronger notions of security. What is cool is they give proofs of unforgeability for FROST1 and FROST2 but they actually show that FROST1 and FROST2 are fulfilling even stronger notions of security than what our proofs showed. That is the first great news that came out of this paper. But something that is also very interesting is they show that FROST2 actually has a slightly lower notion of security than FROST1. Both are actually stronger than what was originally claimed but there is a slight difference between the two and I am going to talk about what the slight difference is now. In short the difference between the two is that FROST2 is malleable with respect to the signing set whereas FROST1 is not. What do I mean by this malleability of the signing set?

<https://youtu.be/tWopcFzSTas?t=12913>

As I said before you have some number of honest parties, in this case 2. And you have some number of corrupted parties, also in this case 2. Let’s assume we are talking about a 2-of-4 scheme. In FROST2 what will happen is all of the players will publish their commitments. Let’s say here they believe that they are starting their signing protocol with signers 1,2 and 3. The honest players are saying “We are going to sign with players 1,2 and 3”. What the corrupt player will do is it will choose its commitments with respect to the commitments of the honest players. Critically it is able to negate the commitments of some of the players and what this evaluates to is a group commitment that is only with respect to the commitments of one of the honest players. In short they choose their commitments so they can knock out player 2 and then the group commitment evaluates to only the commitment of the first honest player. You might say how does this impact security? The honest players can’t actually detect that this attack is happening. They will receive the challenge, they will perform signing as before, they will publish their signature shares and then the group signature is actually with respect to players 1, 3 and 4. If you are going to take away anything from this slide, there is a lot of math and symbols and whatever, the most important points from this slide are that players 1 and 2 who are honest think they are contributing to signing but the signature represents contributions from players 1,3 and 4. This is what I mean by malleability of signers in FROST2.

## Signing Set Malleability

You might say “Does this matter?”, this is actually a new notion for threshold signatures. In the threshold signatures before no one actually considered this notion. It is a new notion and it is interesting to think about. You might say “Is this actually needed in practice?” We talked about this as well and the conclusion we came to is we don’t know. This might be an application specific requirement. The IETF draft that we’ve been working on, we had it changed to the optimization of FROST2 but now we changed it back to FROST1 because we didn’t want to exclude any use case that applications might have. We came to the conclusion that maybe it is, maybe it is not, but we don’t want to exclude any kind of use case. But for applications that are performance critical and don’t really care about this malleability of signers FROST2 may be still be of interest. I want to highlight this here because there is this performance versus malleability trade-off between FROST1 and FROST2. It depends on your application which one may be best for you.

## FROST and robustness

I am going to switch gears now and talk about robustness. Robustness means a lot of things in cryptography. I know there are other notions of robustness in cryptography. What I am talking about here is robustness for threshold signatures or MPC in general, it means the protocol succeeds as long as at least some number of players participate honestly. Here we are talking about a threshold number of players. The reason why I am talking about this is because FROST is not robust. When we designed FROST we explicitly said “We are going to optimize for 2 rounds for a non-robust protocol”. That’s an explicit trade-off that we made. Looking at this example to the right, let’s say you have a 2-of-3 scheme where you have 2 signers required and 3 total. If you have 3 signers contribute to this signature but 1 signer contributes garbage you have to throw away that signature, it won’t validate. It is a correctness issue actually. If you have this case you have to rerun the protocol. What is nice is FROST does fulfil the notion of identifiable abort. What identifiable abort means is that if someone does contribute garbage you can identify the player that did and you can kick them out. It is not so bad. Someone either maliciously or not maliciously contributed garbage, let’s exclude them, figure out what happened. We can still hopefully sign using the remaining number of players but there is a performance trade-off with that.

## ROAST

Paper: <https://eprint.iacr.org/2022/550.pdf>

Blog post: <https://blog.blockstream.com/roast-robust-asynchronous-schnorr-threshold-signatures/>

The reason why I’m talking about all of this is because there is some other recent work that’s called ROAST. What ROAST is is a wrapper protocol for Schnorr threshold signatures but they use FROST as the canonical example. Basically at a high level what ROAST is is a wrapper protocol that makes schemes like FROST robust. I know I have talked to people who would like this type of mechanism so I’m highlighting it because I know in practice that this is something people would like to use. In short you can have 3 players, one of them might contribute garbage and you can still have a signature output at the end. The reason why this is interesting research is because there is a trivial solution of where you would need to maintain n choose t concurrent sessions but this protocol actually reduces that number to `n-t+1`. If `n` and `t` are small it is quite cheap to run this protocol.

## What’s Next: Unlinkable FROST

Finally I want to highlight some ongoing research that we’re doing right now. In the Zcash protocol there is the requirement for unlinkability of signatures and public keys. This is currently being fulfilled by… DSA. For rerandomizable DSA you are able to randomize signatures and public keys so that on the blockchain you are not able to link them between signers. This is very easy to do in a single party setting and it is harder to do in a threshold setting for different privacy and security trade-offs. This is ongoing research. We have a candidate scheme which I think is going to be talked about later in the engineering update. I’m looking at the proof of security right now so we’ll have some more news towards the end of the year. But this is what is coming up and something we feel confident about being able to design for the Zcash protocol. Also importantly as we’ve been doing this work there have been a lot of discussion about what kinds of security or privacy cases we should consider. Do we need to consider signers being able to disclose information so that these signatures can be targeted on the blockchain? How much do you trust the signers? How much do you trust the coordinator? There are a lot of questions and we would love to hear from you, the kind of use cases you would like to target within this setting for a threshold setting specifically.

## What do you need?

I want to conclude by saying that we’ve done a lot of work the last 2 years, a lot has been going on, we’ve been really busy, it has been a blur. I hope you can see how much has come out of this and really how this research that we have done within the Zcash community has benefited the larger ecosystem. That is something we are really proud of and we are proud that the research we’ve done has further implications from ourselves. We are wrapping up a lot of this work right now, we are hoping to have unlinkability work done soon. The security of FROST is now closed. It is well understood. We are wrapping up the IETF work. Now we are starting to look at what’s next. FROST started within this community by saying “Here are the problems we have. Please help us, let’s try to find a solution to them”. So I want to put out a call to you to say “Are there other things that we haven’t considered?” Have you tried using FROST in some settings and found that it doesn’t maybe fit exactly with where you are trying to use it for different privacy or security use cases. If that’s the case come and talk to us. We also do other work besides multisignatures. We are interested in other research problems you might have. We are looking for things to do or things to work on and new problems. Please come and talk to us about your problems and what you’d like to see from the ecosystem overall. That’s all.

## Q&A

Q - What other ecosystems are deploying or interested in FROST?

A - I know there is an [implementation](https://github.com/ElementsProject/secp256k1-zkp/pull/138) of FROST specifically for Bitcoin. There has been interest in writing a BIP for FROST. Someone from Monero has popped up and talked about using FROST in that setting. That’s the blockchain settings but there are other wallets. It is considered in any setting where you might need an efficient threshold scheme.

Q - How does FROST compare technically with MuSig?

A - There was the original MuSig scheme that was the one I went over in my first slide. That was broken. It was followed up by the MuSig2 scheme. Our SpeedyMuSig is exactly MuSig2 with proofs of possession.

