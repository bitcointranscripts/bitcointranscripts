---
title: ZK on Bitcoin
date: 2024-11-20
---

## Crash Course

- Satoshi: _"If a solution was found [to do ZK with Bitcoin], a much better implementation of Bitcoin would be possible."_

### What's Possible

- **On-chain:** 12 bytes per transaction in some systems.
- **Off-chain:** Any L2 protocol like ARK, coinpools, channel factories.
- **Privacy:** ZCash CISA, ring signatures, shielded CSV (64 bytes on-chain transactions).
- **Developer Freedom:** No more soft forks—just use ZK verification to build anything (e.g., L2s, vaults, streaming payments, subscriptions).

### Key Question

- **ZK vs ZK-SNARKS** (we’ll get there).

### What is ZK?

- **Paper from the 1980s:** Introduced 2-party protocol with prover & verifier to prove the correctness of a statement. Proof reveals only if the statement is true without revealing any data.
- **Technical Meaning:** Proof reveals only the truth of a statement.
- **Colloquial Usage:** Succinctly proving a computation was done correctly, whether or not data is revealed ("verifiable computation").
  - Prove you ran a program correctly to a verifier, prove long computation with very quick (a few ms) proof to verify.
  - Example: "Is a given UTXO set valid as of block height `n` from specific version of Bitcoin Core?"
    - Proof can be verified in a few milliseconds. I.e. start up a node with equivalent security to a full node.

### ZK in Practice

![ZK in practice](https://raw.githubusercontent.com/bitcointranscripts/media/refs/heads/main/bitcoin-research-week-2024/zk-on-bitcoin/zk-in-practice.jpg)

- **SNARKS (Succinct Non-Interactive Argument of Knowledge):**
  - Witness (e.g., `f(x) = y`).
  - Proof much smaller than witness size.
- **STARKS:**
  - Subcategory of SNARKs.
  - Transparent (no trusted setup), hash-based, quantum-resistant.
- **Applications:**
  - Chainstate proof with Incremental Verifiable Computation (IVC).
  - Chain of independent verifications.
  - Complexity of verifier depends on proof system.
  - ZK-VM to verify anything written in Rust (verifier implemented once).

### Use Cases

1. **Privacy:** Keeps witness private (doesn’t need to be provided at all).
2. **Scalability.**

### Tradeoffs

- Size, post-quantum security, and speed of prover.
- Typical construction:
  - One big fast proof → Prove the SNARK with one big slow proof.
  - Prover is fast and proof is small.
  - Program → **STARK → Groth16**
    - STARK: Fast `O(n)`.
    - Groth16: Slow `O(log2n)`.

## ZK on Bitcoin

- ZK proofs in Bitcoin script (not proving Bitcoin stuff like zkSync).
- Example: Using BitVM (optimistic with fraud proofs).
  - **BitVM 1:** Permissioned.
  - **BitVM 2:** Permissionless but relies on initial parties for coin retrieval (punished if they don’t cooperate).
  - Covenants could address fixed amounts.
    - ZK enables covenants, and covenants enable ZK.
    - `CTV` would enable the presigning ceremony of BitVM but doesn’t address the optimistic/fraud-proof part of the protocol.

### Use Cases & Requirements

![ZK comparison](https://raw.githubusercontent.com/bitcointranscripts/media/refs/heads/main/bitcoin-research-week-2024/zk-on-bitcoin/comparison-table.jpg)

1. **ZK Rollups:**

   - Needs ZK verification **and** recursive covenants.
   - Examples:
     - `OP_CAT` (verifier needs 2–3 MB).
     - GSR (includes `CAT` + other opcodes to make verifier more efficient).
     - Even a 32bit MULT would be bigger than one tx
   - Recursive covenant required to carry state of rollup from one transition to the next and move the coins from one state to the next.
   - Is there a minimal set of TX introspection opcodes to get the recursive?
     - Big inputs to SNARK can be parsed inside the SNARK
   - Alpen labs uses liquid introspection opcodes - there are many. Introspection implies recursive covenants, CTV is too weak, and can not reason about inputs which is necessary.

2. **Shielded CSV (Client-Side Verification):**

   - Needs a bridge.
   - Needs chain introspection to detect nullifiers in the chain (e.g., `OP_BLOCKHASH`).
   - Without introspection:
     - It makes assumptions about the attackers hash rate.
     - Alternatives: Nullifiers consumed by UTXO or sent to bridge "contract"/accumulator.
   - Non-optimistic protocol needs `OP_CAT` + `OP_MUL` (or GSR) to verify SNARK on chain.

3. **ZCash-Style Protocol on Bitcoin:**

   - Needs new address type.
   - Needs new tx field? Could fit in `OP_RETURN`.
   - Might need something like an extension block.

4. **Sidechains:**

   - Needs light client for the sidechain in bitcoin.
   - Has its own consensus mechanism.
   - Also needs recursive covenant.

5. **Zero Knowledge Contingent Payments:**
   - Requires knowledge of the solution when setting up the contract. So order of things is the backwards.
   - Does **not** require recursive covenants.

## Observations

- Covenants imply ZKP, ZKP implies covenants and `OP_CAT` gets you both?.
- ZKP doesn't give you introspection.
- Is there set of opcodes that just lets you do the math in script “probably” fit a Groth16 verifier into a bitcoin script?
  - `OP_MUL` to make the verifier more efficient without enabling recursive covenants.
- Culturally bitcoin people are uncomfortable with pairings because they usually require trusted setup.
- Pairing opcode makes Groth verifier way smaller, but requires picking a curve.

## Side Effects

- `OP_CAT` + `OP_MUL` Could enable tokens on-chain without client-side (e.g., [CAT protocol](https://catprotocol.org/)).
  - CATVM: Exit without permission (unlike BitVM).
- Vaults
- Verifier for other schemes like BLS or lattice-based.
- Replicate `OP_CHECKSIGFROMSTACK` which gets you LN-symmetry.

## Future Directions

- Does any of this help with fee-pinning problems?
- Could `OP_TXHASH` and BigInt math be used instead of `OP_CAT`?
- Does Bitcoin PIPEs simplify everything?
