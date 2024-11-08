---
title: Schnorr Signatures for Bitcoin
transcript_by: Bryan Bishop
tags:
  - schnorr-signatures
speakers:
  - Pieter Wuille
date: 2016-10-10
media: https://www.youtube.com/watch?v=_Z0ID-0DOnc&feature=youtu.be&t=2297
---
Slides: URL expired

Pieter Wuille presentation on Schnorr at BPASE 2018: https://diyhpl.us/wiki/transcripts/blockchain-protocol-analysis-security-engineering/2018/schnorr-signatures-for-bitcoin-challenges-opportunities/

Transcript completed by: Bryan Bishop
Edited by: Michael Folkson

## Intro

Today I will be talking about Schnorr signatures for Bitcoin. I want to say a few things in advance. One is even though this is a talk about cryptography and in particular new cryptography I don't consider myself to be a cryptographer. Most of the work I will be talking about is a result of talking to a lot of smart people for a long time. These are things we have been talking about for a long time. Many issues have come up, and I'm glad it has taken a while. You will see why. So Schnorr signatures for Bitcoin, I will first talk about Schnorr signatures and then for Bitcoin.

## Schnorr signatures

Schnorr signatures are a cryptographic scheme. That’s the formula.

`Q = x * G`

`sig = (R,s) = (k * G, k - H(R|M))`

I don't think I will discuss the details here. I will first talk about the history of how we got to the situation we are today with ECDSA in Bitcoin and then talk about the advantages that Schnorr signatures could and would have, how to standardize that and then go through applications that they could have and show that the problem is harder than swapping one for the other.

## History

So history, Schnorr signatures were originally proposed in 1988 by Claus-Peter Schnorr who patented his invention. The nice thing about Schnorr signatures is that they are remarkably simple. It is much simpler than ECDSA, even. It works on any group in which the discrete logarithm problem is hard.

At the time it was proposed for integer multiplication of modular groups. These days we apply it to elliptic curve crypto. However, in 1993, a standard for signatures based on this type of cryptography was standardized. However they didn't use the Schnorr system presumably because it was patented. Instead, DSA was standardized, presumably to avoid some of the patents. Schnorr claimed for a long time that DSA infringed on his own patents.

In 2005, when elliptic curve cryptography was being standardized people built on top of DSA rather than Schnorr signatures that had advantages. They could equally be applied to elliptic curves. In 2008 Schnorr’s patent expires. In 2009 Bitcoin appears and uses ECDSA because it is the only standardized elliptic curve signature system. In 2011, ed25519 was [proposed](https://ed25519.cr.yp.to/ed25519-20110926.pdf) and standardized by Daniel J Bernstein which is effectively a Schnorr like signature system on top of an elliptic curve group. It is not exactly the same but it is very close. What I want you to take away from this is Schnorr signatures are not an established standard. ECDSA is documented and it exactly specifies all the math that has to happen, exactly how signatures are serialized, how the public keys are serialized, exactly what each bit means. This is not the case for Schnorr which is more of a general idea of how to build a signature system. What I am going to try to convince you is that we need a standard for Schnorr signatures not an existing one.

## Advantages

What are some of the advantages that Schnorr has over ECDSA? One is that it is provably secure under standard assumptions, a random oracle model and that the discrete logarithm problem is hard.
ECDSA does not have any proof. Its security is based on people trying to break it and failing. For Schnorr we know that if the random oracle model is an assumption we can make and the discrete logarithm problem is hard then we can 100 percent prove it is secure. It is also provably non-malleable. This is not so much a problem anymore in Bitcoin as we hopefully soon have Segregated Witness plus a low s policy that prevents the known malleability of ECDSA. But there is no proof that there is no other malleability in ECDSA. In Schnorr we know it is impossible. It also supports batch validation which means if you have a group of public key, message signature pairs rather than just a single one, you can verify whether all of them are valid or not all of them are valid at once at a higher speed than each of them individually. This is exactly what we want for Bitcoin blocks because they are big batches of signatures to validate. Last but definitely not least is native k-of-k multisignatures. The idea is that in Schnorr you can take a bunch of keys together and have a single signature that proves all of them signed. And more which I will talk about later.

## Applications of Schnorr signatures

What are some of the applications? First can we take Schnorr as a drop-in replacement for ECDSA as it exists in Bitcoin? And can we apply it to multisig signatures? And I will talk about transaction wide signature aggregation. My goal here is to come up with a single standard that fits all of the applications so we don’t have to worry about what can be used where and when.

So first, the drop-in replacement question. The security proof of Schnorr signatures says that they are existentially unforgeable under the assumptions I mentioned before.

What this means is that if there is a fixed chosen public key in advance it is impossible to create a signature for that key without having the key for any message even messages that an attacker can choose. This sounds great, it is exactly what we want. It turns out it is not exactly what we want. It doesn’t say anything about keys you haven’t chosen in advance. It turns out if you take Schnorr signatures naively and apply it to an elliptic curve group it has a really annoying interaction with BIP 32 when used with public derivation. If you know a master public key and you see any signature below it you can transmute that signature into a valid signature for any other key under that master key. This is a very unexpected result that is not necessarily a problem under standard assumptions. But we should really test our assumptions. This nice proof of existential unforgeability but we need to test whether that is the only thing we want.

Thankfully there is a known and standard solution for this. It is a normal recommendation. Inside a Schnorr signature there is the hash function, the H in the formula. You have the public key under the hash. Or in other words the message you are signing is not just the message but is a concatenation of the public key and the message. This problem disappears. This is a good idea for other reasons too. A downside of doing this is you can’t naive key recovery. Key recovery is the trick where if I give you a signature and a message you can derive what the public key was that would’ve signed this. This is something that naive Schnorr supports and is cool but we don’t actually need it.

## Multisig

Multisigning is the big advantage that Schnorr has and the whole reason we want this. A group of people can jointly create a signature that is valid for the sum of their keys. In the slide here, you see U1, U2 and U3 are the users. How this mechanism works, there is a two round interaction scheme where first they all come up with a nonce k1, k2, k3. They compute a corresponding public point R1, R2, R3. They communicate those to each other and add them up to get an overall R value. Everybody knows this overall R value and signs using this nonce with their own key resulting in a s1, s2, s3. Then you combine all the s values into a final s which is a signature that will be valid for the sum of their public keys. This is nice for k-of-k multisig because now I can say “You, you and you all need to sign. You all give me your public keys. We will add them up together. We compute an address for it. Any money sent now all three need to sign because there is no way to come up with a signature otherwise.” It goes even further. I am not going to go into the details here. I gave a [presentation](https://www.youtube.com/watch?v=gcQLWeFmpYg) on this about a year ago at SF Bitcoin Devs. Even if you don’t have a k-of-k situation but any other policy of what combination of keys that can sign, all you need is a Merkle tree verification in your scripting language plus this ability for Schnorr signatures to add up. You build a tree where every node leaf in the tree is a combination of keys that can sign. You hash them together and the root is now your address. When signing you reveal the path plus the leaf and then a signature with it. The nice thing is that this is approximately O(1). It is O(log (n)) but in practical cases it is pretty much constant. Even if you want to do hundreds of keys. This is really great.

## Cancellation

Unfortunately there is a very big problem with this. Again this is challenging our assumptions. As I told you, you can create a signature with a group of people together that is valid for the sum of your public keys. So you two want to create a multisig address together. You say “My key is Q1” but your actual key is Q2. You don’t say “My key is Q2” you say “My key is Q2 - Q1”. He subtracts the other guy’s key from it. I add them together but the result is now just his key. This would mean that he can sign for both of them while everybody is assuming that we have created an address that actually requires a signature with both. This is the cancellation problem. You can choose your keys in such a way that other people’s keys get cancelled out. The reason this is not usually problem is because all your keys are chosen in advance before the scheme even starts. But in Bitcoin we just have addresses. We don’t have fixed keys in advance. It would be very annoying to go assume that we now need to send around signatures on every address to prove that we actually own it. That would be one solution. It is relatively annoying. This was for a long time a problem that we didn’t know how to solve. Until we discovered there is actually a trick that seems to make things work.

## Delinearize

Before signing everybody multiplies their private key with the hash of their public key. This is not a problem. The result is now that instead of adding the keys together it’s the sum of the keys multiplied by their own hashes. The formula is down there.

`Q = H(Q1)*Q1 + H(Q2)*Q2 + H(Q3)*Q3` (Wagner)

It is slightly harder to sign and slightly harder to verify but all the other properties remain. I started working on a proof that this was secure and I thought I found one. But what I found a proof for was that the exact same cancellation property where there is one user and the other one cancels out the first one is in fact impossible under this scheme.

In particular if you had an algorithm to figure out what the resulting private key after cancellation was under 2 user scenario you could use the same algorithm to break Schnorr signatures themselves. We assume this is hard. People have studied this.

Unfortunately after talking to Adam and Greg and some other people at Blockstream it turned out that we couldn’t extend this proof to the more generic case of proving that no signatures were possible. Then Greg Maxwell came up with an attack which only applies in the case when there are multiple adversaries, multiple people who can each choose their keys and can together cancel out the first one. There is a really cute algorithm called Wagner’s algorithm which would completely break this in no time. So we need another solution.

Instead of just multiplying each key with the hash of itself we multiply it with a hash based on itself and all other keys that are being used. So now an attacker cannot invent any key in this scheme anymore because any key being added to the scheme would change this commitment and break the linearity property that you could use to derive. We have a sketch for a proof that this is actually secure. Unfortunately it would be highly inefficient for <a href="https://diyhpl.us/wiki/transcripts/sf-bitcoin-meetup/2015-08-24-pieter-wuille-key-tree-signatures/">key tree signatures</a>. If you have a key tree with a million combinations, now for each of those million combinations you would need to do elliptic curve cryptography to derive what the leaf is because each of them would need an individual multiplier. This would kill the performance of key trees completely by several orders of magnitude. Thankfully it is not actually needed to commit to the exact set of keys that signs. It is sufficient to commit to a superset of it. To break this scenario an attacker has to be able to choose their own key and not pick one from the set. We believe this is secure. As I said I am not a cryptographer. If people are willing to help prove this I would be very grateful.

## Aggregation

[This](https://bitcointalk.org/index.php?topic=1377298.0) is something that Greg Maxwell came up with after this problem of multiple adversaries in a multi-signing problem was solved or at least we thought we had a solution. We can do much more. We can do aggregation over all signatures in a single transaction. This is a case where you are trying to protect against the situation where you don’t know what all the signers are in advance. You reveal them on the fly. You still have all public keys, we are not aggregating the public keys in this case, we are only aggregating all the signatures. The verifier would take all the public keys that are seen in a transaction, combine them using the formula we have and do a single validation. This doesn’t have the largest performance advantages. It does have the batch validation property. We do get a factor of 2 or 3 speedup. Here is a nice graph of the current Bitcoin blockchain. The blue line is the current block size that is increasing as you can see. The purple line is what if we were able to strip out all signatures which is something that we could do with OWAS or BLS. We can go even further with Mimblewimble. This is shorter term thinking. The green line is a result of if all transactions in Bitcoin history would have used signature aggregation from the start. As you can see it is like a 20 percent reduction in the block size. That is not groundbreaking but what it does have is it finally gives the financial incentive for coinjoin because now the cost you bear in a coinjoin for the space occupied by signatures is shared by all the participants. The more participants you have, it doesn’t matter, there is still going to be only a single signature that you produce for the whole thing. The cost for this signature is shared. It is a small advantage but I think these subtle incentives actually matter especially with fee markets rising.

## Bringing this to Bitcoin

So how do we bring this to Bitcoin? The easiest is we do OP_SCHNORR instead of OP_CHECKSIGVERIFY. With the SegWit script versioning we could define a new version number. CHECKSIGVERIFY from now on means Schnorr CHECKSIGVERIFY. This has a downside. It can only do k-of-k and there is a single signature for every key. We could do better and make an alternative to OP_CHECKMULTISIG, OP_MULTISCHNORR I guess which has multiple public keys but still only a single signature. This would be a huge advantage for larger multisig constructions which are very expensive and large right now in Bitcoin. If we had the above plus a Merkle check or Merklized Abstract Syntax Tree (MAST) or any of those we can pretty much reduce every input to just a single signature. Choose some combination of keys and provide a single signature with it. If we go as far as doing signature aggregation we can do pretty much anything with just a single signature for the entire transaction.

## Signature aggregation

How would signature aggregation would in practice? On the left are signatures, on the right is the redeem script or the scriptPubKey or the witness script or whatever you want to call it. Signatures right now contain the actual ECDSA signature with concatenated to it the sighash type. We just change the meaning of a CHECKSIG operator to either take only a sighash type or take a signature and a sighash type. During the execution of a script we just say “I don’t know the signature for this one. It succeeds.” We add all the signatures, all the pubkeys and all the messages that get seen during validation of an entire transaction onto a stack. In the end we do the aggregation operation and verify a single signature with it. This is an operation that can be done in one go. This is where the 2-3x factor speed advantage comes from. After SegWit this would be a relatively easy thing to do.

## Future work

We definitely need to do academic write ups about this delinearization scheme. I don't know of much in the literature about this exact case. Waiting for SegWit to roll out because we need script versioning. And we need to write a BIP.

Thank you.

## Q&A

Q - The size of the serialization, would it be a fixed size?

A - Yes we don’t need to follow an existing standard that prescribes a ridiculously inefficient signature serialization scheme. We just pick one that is 64 bytes.

Q - With signature aggregation we only have one signature for the whole transaction. That is only where we have one type of sighash? If we have several?

A - It is in fact compatible with multiple sighash types but it is not compatible with not all signers being online at the same time. There is a solution for this. I didn’t want to go into the details. You can basically add an extra byte to define several registers. The group of signers that are online at the same time sign in this register but there is maybe a second register. You lose the benefits of the complete aggregation but it still works.

## References

Schnorr signatures in Bitcoin
https://bitcoincore.org/logs/2016-05-zurich-meeting-notes.html

Schnorr signatures and BLS signatures
http://diyhpl.us/wiki/transcripts/2016-july-bitcoin-developers-miners-meeting/dan-boneh/

Tree signatures
https://bitcoinmagazine.com/articles/blockstreams-pieter-wuille-proposes-tree-signatures-improved-flexible-multisig-bitcoin-transactions-1440624296

libsecp256k1
https://github.com/bitcoin-core/secp256k1

https://github.com/WebOfTrustInfo/rebooting-the-web-of-trust/blob/master/topics-and-advance-readings/Schnorr-Signatures--An-Overview.md

https://bitcoincore.org/en/2017/03/23/schnorr-signature-aggregation/

