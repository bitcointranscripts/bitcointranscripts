---
title: 'Proof-of-Verification for Proof-of-Work: Miners Must Verify the Signatures on Bitcoin Transactions'
transcript_by: Bryan Bishop
tags:
  - research
  - proof-systems
speakers:
  - Kanta Matsuura
date: 2019-09-12
media: https://www.youtube.com/watch?v=Uh6Ywxrobzw&t=11607s
---
<https://twitter.com/kanzure/status/1172142603007143936>

extended abstract: <http://kmlab.iis.u-tokyo.ac.jp/papers/scaling19-matsuura-final.pdf>

## History lesson

In the 90s, we had some timestamping schemes where things are aggregated into one hash and then it would be publicized later in the newspaper. This scheme was commercialized, in fact. However, the resolution of the trust anchor is very limited. It's one day or half-day at best. When we want to verify, we need to visit the online-offline database maintained by a trusted party to get the merkle inclusion paths. They assume verification or validation is assumed to be infrequent.

## Digital publicizing of super root hash

Later, we tried to digitize the publication case by using TV broadcasting. The resolution was better, but we need to assume that verification is still very infrequent. This still requires a trusted party to operate a database to help figure out merkle paths or merkle roots.

## Avoiding a trusted third party

As you may all know, bitcoin and blockchain is an attempt at avoiding a trusted third party. As a result, we achieve public verifiability. This is good. However, due to the need of the p2p network, the resolution is somewhat intermediary between seconds and days, it's maybe minutes or hours. I would like to point out that "verifiability" does not ensure that someone has really verified it. We just saw, we can verify it.

## Research question

This is my research question.

Are we (any nodes) certain that naother node has really verified the transactions to be included in the block of the current concern? In this talk, we focus on the verification of the signatures on transactions. In order to fully verify the transaction, a node must also confirm that it is not an attempt of double-spending. This aspect is not explicitly considered here. However, it is worth noting that a node must visit the input transactions and confirm the public key correspds ot the recipients of the inputs in order to fully verify the signature.

This proposal is focused on the verification of signatures on transactions.

## Possible stories of the problem

Rushing miners may skip the verification so that they are in a better position in the competition of getting rewards. Signature verification is much more computationally expensive than hashing, and maybe the miner is stupid and doesn't know to be doing transaction validation in parallel. The risk may get more significant if scalability innovation dramatically increases the number of transactions in a block. Colluding nodes may also skip the verification for the purpose of attacks.

## Proposal: Proof-of-verification

The proposal is called proof-of-verification.

Transactions are created the same way. Suppose you verify each transaction. Then, this verification automatically produces a proof-of-verification and anyone can verify these proofs. In theory, there are a wide variety of implementation options. I call this "explicit proof-of-verification" where we just append these proofs to the hash function for mining. Maybe we want to reduce the communication overhead; we could hash all of such proofs of verifications. For "implicit PoV", we just append the proofs to the proof-of-work hashing. This can reduce the communication overhead, but maybe some of you are not happy to see that the hashing of the nonce is now in a different form.

## Schnorr's digital signature scheme

I'd like to revisit another classic, the Schnorr signature scheme. This slide describes key generation in Schnorr signature schemes. Finally, we need to do modular exponentiation of a random number. The verifier of the signature needs to reconstruct the exponentiated parameter r. The proof-of-verification here is the reconstruction of v in signature verification, of r in the signature generation. Therefore, this parameter can be reused as a proof-of-verification.

It should be noted that this modular exponentiation in the signature verification algorithm cannot be pre-computed. This is very important. I use this trick in the "protection of authenticated key-agreement protocols against a denial-of-service attack", 1998. This is also a classic.

## Applicability

In many digital signature schemes like DSA based on the hardness of the discrete logarithm problem, including EC-based implementations, we find such parameters that can be a proof-of-verification. This applies to DL-based multi-signatures as well. For example, in the case of a simple Schnorr multi-signature, the modular exponentiation can be a proof-of-verification. You can find some examples in my extended abstract, which I uploaded to my homepage on the web.

## Computational cost for honest nodes

Are we going to have additional computational cost for honest nodes in this scheme? The answer is a resounding no. When we consider the nodes who generate transactions, there are no changes. The proof-of-overifiation mechanism is just naturally embedded. Nodes who generate a block, have a proprotional increase of component hashing (proportional to the number of the transaction outputs) but much smaller than the total PoW hashing, for both implicit PoV and explicit PoV.

In most of the hash functions that can handle arbitrary length input, they have similar structure to the construction invented by Merkle-Damgard. From this scheme, we can easily increase the computational cost but not necessarily large.

Nodes who are considering whether they agree to the newly reported block: if they are not interested in signature verification but interested only in the verification of the nonce, the use of the implicit PoV increases the computational cost; the node must verify the signature to compute the hash before verifying the validity of the nonce. SPV nodes who do not verify the signatures cannot verify the .....

## Communication overhead

No changes in the case of implicit PoV for communication overhead, however there is a marginal increase for explicit PoV. I'll skip this because of the time constraints here.

We might consider individually verifiable explicit PoV, where we append all the PoVs or the hash of each PoV, etc, if we are willing to accept larger communication overheads. A lite client would just verify some of the PoVs or something, and then if their transactions are fine then maybe they trust the miner.

## Summary

Dishonest nodes may skip the verification of the signatures on transactions. Such behaviors may allow malicious transactions to be included in a new block, and reduce the ...

## Future work

* Advanced experimental evaluation

* Advanced theoretical evaluation, especially the SPV security model

* Proof of full verification: extend PoV so that we can verify someone else has confirmed there are no double spends. Extending PoV so that we can verifyu someone else  has done anti-malware operations on the scripts (like malware detection). Maybe more problems to be considered.



