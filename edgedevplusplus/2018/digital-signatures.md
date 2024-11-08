---
title: Finite fields, Elliptic curves, ECDSA, Schnorr
transcript_by: Bryan Bishop
tags:
  - cryptography
speakers:
  - John Newbery
media: https://www.youtube.com/watch?v=DcGm_4-ig1o
date: 2018-10-04
aliases:
  - /scalingbitcoin/tokyo-2018/edgedevplusplus/digital-signatures
---
<https://twitter.com/kanzure/status/1047634593619181568>

# Introduction

Thank you to Anton and to everyone at Keio University and Digital Garage. I have an hour to talk about digital signatures, finite fields, ECDSA, Schnorr signatures, there's a lot of ground to cover. I'm going to move quickly and start from a high level.

My name is John. I live in New York. I work at a company called Chaincode Labs. Most of the time, I contribute to Bitcoin Core.

I am going to talk about the concept of electronic coins, finite fields, elliptic curves, and then Schnorr signatures, and then I will touch on ECDSA. I am talking about Schnorr signatures more than ECDSA because Schnorr signatures are easier to understand and easier to reason about and it should give you some intuition about how digital signatures work. I am not going to go into great detail in many of these things. I hope you will have some intuition about how these things come together. You can treat these things as a black box; if you know the properties of how digital signatures work, you don't necessarily need to know how it works under the hood.

# Caveat auditor

I am not a cryptologist. This is only an overview. There will be no formal proofs or mathematical formulas. I'm going to use some terms loosely. For any cryptographers in the room, I am sorry for these, like I might say "zero knowledge" but not mean zero-knowledge proofs.

# Electronic coins

This is a diagram from a document. Does anybody recognize which document? This is from section 2 of the bitcoin whitepaper. An electronic coin is a chain of digital signatures and you can transfer the coin by signing the hash of the previous transaction and the public key of the next owner, and append these together, and then you can verify the chain of ownership.

# Transaction structure

A transaction has at least one input, but possibly many inputs, whic hcontains a reference to the transaction output (txout) that is being spent, and a digital signature proving that the owner of the private key uathorized the transaction. And also a transaction contains some outputs (txouts) which contain the amount, the public key of the recipient. It goes from one public key to the next public key.

# Verifying a transaction

In practice, it's more complex. There's script. But this is a simplified view of how bitcoin works. How do you verify a transaction? Every node on the network checks that the inputs point to an output that exists and has not been spent. It also checks that the outputs do not exceed the amounts of the input. And that each input has a valid signature (valid scriptsig). This is what happens when you verify a transaction.

# Digital signature

Digital signatures are used to transfer ownership of coins. A digital signature proves that hte owner of the coin authorized the transfer- only someone with the private key can sign the transaction (authentication). Nobody can change that transaction once signed, and that's called integrity.

Digital signatures use asymmetric cryptography. There's a public key which is known to everyone, and a corresponding private key which is kept secret. Only someone with a private key can create a valid signature over the message. Everybody can verify that signature. Bitcoin uses a digital signature scheme called ECDSA which goes over an elliptic curve called secp256k1.

ECDSA is a little bit of a hack to get around a patent that was granted to the inventor of the Schnorr signature algorithm. Schnorr signatures are better in every way. In the future, bitcoin might be extended to allow for Schnorr signatures now that the patent has expired.

# Discrete log problem

ECDSA is an application of the discrete log problem. In some systems, it's easy to multiply, but difficult to divide. Multiplication is where you take an element and add it to itself multiple times. But if you give two elements and ask how many times do we have to get the first element to get the second input, that is difficult in some finite fields, and this asymmetry is called the discrete log problem. This is then built into a digital signature scheme.

I am going to talk about cyclic groups. In general there is a generator G. For a given H in the group, what is the scalar x such that xG = H. This xG adding G to itself many times is easy, but given H, it's difficult to work out what x is. In public key cryptography, x is the private key, and H is the public key.

In bitcoin, where we can multiply things but not divide, we use secp256k1 defined over a finite field.

# Finite fields

I am going to briefly talk about finite fields and elliptic curves. All of this can be treated as a black box. You just need to know that things in this blac kbox are easy to multiply but difficult to divide. Really, as long as you have a system where it is easy to multiply but difficult to divide, you can build an asymmetric cryptography scheme over it. You can build a Schnorr signature scheme over another group as long as it has these problems.

A group in mathematics is a set of objects along with a binary operator which we are going to call + here. A binary operator is something that takes two elements from something in the set, and gives you another element from the set. The binary operator has the following properites: closure, which is where you add them together and you get another element in the group. There's an identity property which is that if you add zero to anything you end up with that same element. Every element has an inverse, another required property. If you have an element in the group, there's another element where you use a binary poperator, you end up with zero if you add the inverse element. Also, associtiavity, where (a+b)+c is the same as a+(b+c) and it doesn't matter which order you do those things. Also, some groups have commutative properties-- these are called Abelian groups, and that's if you have a+b then it's the same as b+a. Not all groups hav ethat.

# Cyclic group

A cyclic group is cyclic if there's a generator element. Here we're calling it small g. If every element in the group is g added to itself some number of times, then we call that a cyclic group with the g generator. The integers modulo p for any number p is a cyclic group.

# Fields

A field adds some more structure to a group. A field is a commutative group with a second binary operator x. That second binary operator is also closed, has an identity, has inverses (except for zero), and is associative and commutative.

An example field is the real numbers, with addition and multiplication defined as normal-- that's an infinite field. The rational numbers, if you just take those, with addition and multiplication that's defined as normal. The integers from 0 to (n-1) with addition and multiplication defined modulo n this is known as a finite field.

An interesting field we will talk about is Fp where p is a prime number. This is the integers modulo p. F13 is {0, 1, 2, ... 12}. 4+5 is 9, 8+9 is 17 but we wrap around so mod 13 that's 4.

# Elliptic curves

An elliptic curve is a curve of the form y^2 = x^3 + ax + b. In bitcoin, we use the secp256k1 curve. This is y^2 = x^3 + 7. So a=0 and b=7. If we draw out this curve we end up looking like this.

# Elliptic curves over a finite field

Instead of defining that secp256k1 curve over the reals, we actually define it over a finite field of integers modulo p where p is an enormous number here which is 2^256 - 2^32 - 2^9 - 2^8 - 2^7 - 2^6 - 2^4 - 1. It looks like a random distribution, it's difficult to intuit what it looks like, it looks like a bunch of dots on a page. But it still has some nice properties of what it would look like if it was over the reals.

# Defining a group operation for the elliptic curve

We can define a group operation for points on this curve. We define it as follows. To add two points, if we have a point P and another point on the curve Q, to add them we draw a line and we see where it meets the curve and then we mirror it on the x axis. So here, P + Q equals R. That's a binary operation in the group.

To double a point, to add it to itself, here we double P. We find the tangent of the curve at that point, find where it meets the curve again, and then reflect over the x axis. You can do this every time you use a tangent you'll find the curve at some other point, but I'm not going to prove that.

And the inverse under the group operation is its reflection in in the x axis. If we add P + Q together, we usee that an element plus its inverse-- that's our identity element, that's the only exception where you have a line between two points on the curve it wont meet the curve again.

I'm not going to prove that this is a group operator on this set of points on the curve. I'm just going to claim it.

# Generating a cyclic group

Take any point G on the curve. G is for generator. And I'll add it to itself. And I'll keep adding it to itself until I come back to the same point. Every point I've otuched is a multiple of G. That set of points is a cyclic group. For secp256k1, we use a specific generator point, 55066263022... etc. I'm going to claim but not prove that this cyclic group is easy to add elements to each other or itself multiple times, but hard to divide. If I gave you an element in this group and ask you how many times you need to add G to get to this point, it will be really hard. Nobody has found a way to do this efficiently, as far as I'm aware.

# Discrete log problem for an elliptic curve

This finite field elliptic curve system we're going to claim that multiplication is easy but division is difficult. The private key is scalar x in the range 0 from n-1 where n is the order of the group, it's a 256 bit number. The public key is a point P on the curve where P = xG.

Q: Why are we unable to prove this?

A: People have tried to find an efficient way to break the discrete log problem, and as far as we're aware nobody has succeeded. That's our security model.

If you have x, you can very easily find P which is a public key. It's easy to go from x to P. But the other way is computationally difficult.

# Schnorr signatures

If everything above was alien to you, don't worry. You don't need to know any of that, because you're not a cryptography. Put that in a box and throw the key away-- just know we have a system where it's easy to multiply, but difficult to divide. It doesn't matter what's in that box, we could substitute elliptic curves for something else. We're going to build on these properties and now talk about Schnorr and Schnorr signatures. We're going to start with the Schnorr identification protocol.

If I have a scalar x which is my private key and it corresponds to a public key P, I can prove to you that I know what x is without revealing what x is. I can prove to you this in zero knowledge. I can make a proof but you won't learn anything else.

# Zero-knwoledge proof

A zero-knowledge proof requires three properties: completeness, the proof convinces the verifier. It requires zero-knowledge where the only thing you learn is that I know what x is, no other information is revealed. Also, soundness, which is that the proofs only work if I know the value.

It has three steps for the schnorr identification protocol: it requires a commitment step, where ythe prover picks a nonce scalar k and commits to it by sending K = kG to the verifier. Then you send a challenge- where the verifier sends a challenge scalar e. Then I send a response, which is called s = k + ex. The prover sends the response scalar. Little k is a scalar, it's just a number, e is just a number you have challenged me with, and x is a private key. I've sent you a number.

Why do we have completeness here? The completeness is whether my proof will convince you. You'll be convinced if this identity holds: sG = kg + exG. The verifier is convinced that the prover knows x if the identity equation holds. xG is P. The verifier can do this because he knows s, G, K, e and P. K was sent to the verifier. e because the verifier sent that to the other party. and P is the public key.

Do we have zero-knowledge here? Why do you learn nothing? The transcript of the 3 step protocol is (K, e, s). K is the commitment that I sent you in step one. e is a challenge you sent back to me, and s is a proof or the signature. If someone is watching the protocol and writes down each message going back and forth, it would be (K, e, s) and that is the transcript.

If the verifier colludes with the prover and tells her what e\_fake is, before she provides a K, then she chooses s\_fake randomly and set K\_fake = s\_fake * G - e\_fake * P. So the transcript is then (K\_fake, e\_fake, s\_fake). The transcript looks the same for a fake proof as it does for a real proof. If someone is an impartial watcher from outside and sees this fake proof, they can't tell the difference between the fake proof and the real proof. This fake proof tells you nothing about x. Your simulation proof can be produced without knowledge of x, and your simulation proof is indistinguishable from the real proof. It therefore tells you nothing about it.

What about soundness? If I am able to produce a proof then I must know x. If the prover can reliably produce a proof for any challenge e, then she must know x. How do I prove this or show that Schnorr identification protocol has soundness? Imagine you are able to pause, fast-forward or rewind what the prover is doing. The verifier could "fork" the prover- the verifier could wait for the prover's commitment K, send challenge e\_1 to the prover and receive response s\_1. Then we rewind to the challenge step, send a different e, and then get s2 instead of s1. Just suppose the verifier had this secret power being able to go back in time. The verifier now has s1 and s2 and they could then calculate the value x and then work out the private key just by challenging twice after the same commitment. The verifier has extracted the private key x from the prover. If the verifier can take the private key from the prover, then the prover must have already had the private key. I can't take something from you that you don't already have.

Imagine the prover going through this operation and forking himself and the prover can extract the key from himself. If the prover can create this signature, then he can learn his own private key, so he must know his own private key.

Any questions about that?

# Non-interactive Schnorr identification protocol

How do we turn this into a non-interactive proof such that I can prove to the whole world at the same time that I know x? The only thing that the verifier did is provide a random challenge in one of the steps. The first one was a commitment and then there was a challenge step. If we could replace the verifier but instead use a random oracle that gives us a random number, then we can do away with the verifier. The random oracle simply provides a random number after the commimtent step, then we don't need a verifier. We treat a hash function as a rnadom oracle. After has a special meaning here; the prover can't know the output to a hash function before evaluating it. If they could do that then they could cheat just like colluding with the verifier. "After" means sequentially after. This changes it from an interactive proof to a non-interactive proof, and this is called a Fiat-Shamir transform.

The identification protocol now has 3 steps as before: the prover picks a nonce scalar k, the prover calculates e = H(kG). In bitcoin we use sha256. But any hash function where you can't predict the input given the output. Then the prover computes the scalar s = k + ex. This is the same as before except our e is not provided by an external verifier, but instead created using a random oracle or the hash function. The proof is (s, e). Anyone can verify once again by checking sG = kG + exG. This is the same identity as before.

Any questions about that?

Q: How does the observer know how e was calculated? We're talking about the transform from the interactive proof to the non-interactive proof. The observer can see (s, e) tuples. How does this prove that you know what x is?

A: Good question. You can share big K.

Q: Okay, so big K is known.

# Signature of knowledge over a message

That was a non-interactive identity protocol. You proved to any observer that you know what x is, without revealing x. You can now extend this to creating a signature over a message. Since H is a rnadom oracle or a hash function and it returns different values for whatever you put into it, you can add extra inputs to that H function call, and you get a signature of knowledge over that message.

So e = H(m || kG) where m is the message. The prover calculates s in the normal way, s = k + ex. The verifier checks that the identity holds and that e is indeed H(m || kG). What does this do? That seals the message under the signature. Once that signature is produced, you can't change the message afterwards without knowing the private key x. This gives you message integrity.

And that's a Schnorr signature. It's the same identity but also putting a message into that hash message. Usually that message is going to be a hash of other details that you want to include in the signature.

# ECDSA

I am going to go over this quickly. I'm going to give the identities and the formula. It's a different digital signature algorithm. It also uses the discrete log problem over elliptic curves just like Schnorr. It was developed because Schnorr was encumbered by a patent for many years. ECDSA has non-linear signatures, so this makes threshold and adaptor signatures much more difficult. This makes scriptless scripts more difficult. There is no formal security proof for ECDSA. So that zero-knowledge demonstration from earlier, doesn't exist for ECDSA. Also, ECDSA signatures are malleable. There are many reasons why we would prefer to use Schnorr signatures and maybe in the future bitcoin will implement and deploy Schnorr signatures.

# ECDSA signing

The prover signs a message m as follows: set z as the leftmost bits of H(m) (the hash of a message). He then picks a random nonce scalar k. He sets K = kG and r as the x coordinate of K. So K is a point on the curve and he just picks the x coordinate, and then he sets s as the inverse of k multiplied by (z + rx). The ECDSA signature is the pair (r, s).

# ECDSA verification

The signature can be verified by setting z as the leftmost bits of H(m), and set u = z/s and v = r/s. If the x coordinates of uG + vP is equal to r, then the signature is valid. It's similar in some ways to Schnorr, but it's made just different enough to not be encumbered the patent.

# Further reading

* Borromean ring signatures paper by Greg Maxwell and Andrew Poelstra: <https://github.com/Blockstream/borromean_paper>

* <https://joinmarket.me/blog/blog/from-zero-knowledge-proofs-to-bulletproofs-paper/>

* <https://blog.cryptographyengineering.com/2014/11/27/zero-knowledge-proofs-illustrated-primer/>

* <http://diyhpl.us/wiki/transcripts/sf-bitcoin-meetup/2018-07-09-taproot-schnorr-signatures-and-sighash-noinput-oh-my/>

* <https://diyhpl.us/wiki/transcripts/blockchain-protocol-analysis-security-engineering/2018/schnorr-signatures-for-bitcoin-challenges-opportunities/>


