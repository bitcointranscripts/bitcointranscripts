---
title: A secp256k1 break? (quantum)
tags:
  - bitcoin-core
  - libsecp256k1
  - quantum
date: 2025-10-21
---

A secp256k1 break? (quantum)

Goal: thinking over recent months about the quantum problem

Multiple approaches, Standardizes schemes.

## Hash based

Already relying on collision resistance. Emergency case, ideally don't introduce
new cryptographic assumptions. Hash based signature schemes rely on the same
assumptions that Bitcoin has now.

The drawback to hashbased is we lose a lot of features like multisignatures.
Lattice-based you can retain some of that. The smallest lattice signature size
is 1.7kb.

### Sphincs+

NIST standardized: Sphincs+

Optimized for size (preferred) and one for signing time.

Standardizes security levels:

<table>
  <tr>
   <td>Security level
   </td>
   <td>classical
   </td>
   <td>quantum
   </td>
  </tr>
  <tr>
   <td>1
   </td>
   <td>128 bits
   </td>
   <td>64 bits (2^64 grover iterations)
<p>
The number of sequential operations a classical computer can do in 10 years
   </td>
  </tr>
  <tr>
   <td>3
   </td>
   <td>256 bits
   </td>
   <td>128 bits
   </td>
  </tr>
  <tr>
   <td>5
   </td>
   <td>Not covered
   </td>
   <td>Not covered
   </td>
  </tr>
</table>

Higher security levels have higher signature sizes.

Leaning toward security level 1.

Shor's attack against DL requires on the order of 2^28 gates

Sphincs+

Size optimized, security level 1: 7.8kb (schnorr 64 bytes)

Since standardization, some optimizations have happened:

Sphincs+C (extra 700-1000 hashes to grind during signing, but verification is
better): 6.3kb signature sizes

Can you do more signing grinding to trade off on size? Yes but it becomes not
worth it.

With the same blocksize, block verification time would be the same.

You can parallelize parts of the signature verification.

S+ has no state requirements.

Number of signatures possible before degrading vs size of signature S+C?

2^64 signatures, then security degrades.

If you drop to 2^40 signatures 4.3kb

2^20 signatures: 3.1kb (~1m)

Does lightning need to move to post-quantum given the economics? Batch attacks
can be dangerous.

Issues

No public derivation. No “efficient” watch-only wallet.

### Stateful sigs

Problem with state? Backups and hardware wallet interplay.

One Time Signature (OTS): generate keypair, only allow to produce a single
signature ever. Otherwise, can be forged.  Ex.: lamport, winternitz

Extended merkle signature scheme (XMSS): generate multiple OTS keypairs, build a
merkle tree, and the root is the public key. First time you sign, signature for
the first OTS, merkle proof. Next time use the second tree entry.

One OTS: 256 byte signature size

Another approach is to build an unbalanced merkle tree. First signature:
288bytes. Second, a bit more. The problem is it is still stateful.

### Both stateless and stateful approach

Public key built with a Sphincs+ and unbalanced (XMSS), sort of like how taproot
has 2 ways to spend. Also outputs the secret key and the seed.

Winterniz OTS with +C optimization would be the OTS scheme for XMSS.

Sign using the unbalanced merkle tree XMSS. Assumes that HWW can keep state
securely.

How to restore? Take the seed, when restoring, always using S+ to sign moving
forward (larger signatures) XMSS can no longer be used. Issues with running in a
VM, or restoring a disk backup.

For Bitcoin Core, you can do things like TPM to store state.

Discussion about multiple XMSS branches for multiple restores.

Point made that if you need to restore and use the fallback S+ branch, people
will probably just send to a new wallet to use the smaller XMSS.

Esoteric ideas for multisig. Similar esoteric ideas for saving some bytes.

Discussion of parameterizing some of the size vs signing value vs # of
signatures for different use cases. Lightning (many signatures) vs onchain
(few).

Deploying? Could add opcodes now for schemes now, and allow them in tapscript.
Keep using schnorr now, and have a sphincs+ fallback.