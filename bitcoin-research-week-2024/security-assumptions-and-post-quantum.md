---
title: Security Assumptions and Post-Quantum
date: 2024-11-19
---

Bitcoin security is based on SHA256 and the discrete log assumption:

- GPG keys are used to sign hashes of Bitcoin Core or commits.
- There was an alert key.
- Some offchain protocols use OMDL (a stronger assumption).

Correctness proofs:

- Correct, but there are losses in proofs.
- You shouldn't use Schnorr on secp256k1 if you only trust the ROM.
- If a system only has a proof:
  - There's an alternative model.
    - **0 testing assumption**: Assume your hash function receives a polynomial and doesn’t output a root of the polynomial.

In silent payments:

- They use ECDH but don’t hash the result; this should have a proof.

Cultural notes:

- There’s a lot of culture: a wrong proof might be accepted if the loss doesn’t "count."
- The secp256k1 curve is pretty straightforward.

Multiparty ECDSA:

- Dismissed in Bitcoin space due to the Paillier cryptoassumption (related to RSA).

Crypto assumptions:

- Some assumptions are stable (e.g., discrete log), but RSA and pairing curves have weakened.
- Quantum computers (QC) break the discrete log.
  - Collisions in QC are not better than classical computers.
  - (Second-) preimage in QC requires square root work using Grover’s algorithm.

Post-quantum cryptography (PQ):

- Two categories:
  1. **Based on hashes.**
  2. **Others:**
     - Lattices.
     - Isogenies (recently broken).
     - Codes (stable since the 1960s but require megabytes of data).
- Is QC even a problem?
  - Opinion: It will completely destroy Bitcoin, so it’s not worth worrying about.
  - We should present a technical solution to signatures at least.

### QROM and Bitcoin Mining

- ROM works well with quantum computers, but instantiation with a hash function isn’t satisfactory anymore.
- In QROM, you can query a hash function on a superposition of states.
- Can prove knowledge of BIP39 keys if QC becomes relevant.

### Post-Quantum Solutions

- Best to have a scheme ready now.
- Hash-based signatures should be easy to implement.
- Bandwidth isn’t currently a problem (not the bottleneck for IBD).

NIST standards:

- FAEST: 5kB signatures.
- SPHINCS.
- There’s a BIP for post-quantum signatures.

Idea:

- Put a Lamport public key in the taproot tree + reserve an OP code for it.
  - Soft-fork out key path spend.
  - But then what?

Concerns:

- Transition to PQ could be very fast.
- We should **not** trust the government to help with the PQ transition.
- Currently, no good PQ signature scheme exists.
- NIST is continuing to standardize PQ signatures.

Using SNARK:

- Can aggregate all signatures in a block.
- A 40MB PQ block might take as long to verify as a 4MB block today.

Other notes:

- Bandwidth is increasing worldwide (including in sub-Saharan Africa).
- There’s a recent post-quantum BIP, but details are scarce.
- The timewarp attack still exists.
- QC attacks on signatures wouldn’t necessarily break Bitcoin’s social contract.

### Outcomes

- Shared understanding of what could and should be done.
  - Commit to a public key in the taproot tree and an opcode:
    ```
    <Schnorr pk> <CHECKSIGVERIFY> <Lamport public key> <OP_NOP42>
    ```
    - This doesn’t work because there are no NOPs in Tapscript for redefining—just a real NOP.

Lamport signatures:

- With Lamport sigs, you could potentially implement covenants (humorously noted as "lol").
