---
title: PSBT v3
date: 2024-11-20
---

## Things (tx construction) that need interaction:

- SP
- Musig / FROST
- Payjoin / Cut Through
- CISA
- Splicing / LN / Liquid Ads
- Atomic Swaps
- Coinjoins
- DLCs
- CT / Bulletproofs
- Presigned RBF
- BIP322
- WIF / Descriptors
- Covenants

## BIP 370 Modifiability

[Link to BIP370](https://github.com/bitcoin/bips/blob/master/bip-0370.mediawiki)

- Modifiable is very specific, not future-proof. Need more bits?
- Roles: Need more roles?

## PSBT Overview

- **Unchained Split Custody**: Frustration with PSBT's generality—no clear action plan. It's a vague framework.
- **Don't want to make it more generic** because it would become harder to use.

### PSBTv0

- PSBTv0 is for multiple signers. Inputs and outputs come before signing.
- BIP370 also discusses building and signing.

PSBT is overloaded: it encompasses both construction and signing.

## Common PSBT Issues

- People violate PSBT rules regularly.
- PSBT is somewhat trusted—not private keys but privacy-related issues, DDoS, griefing.

### Usage Questions:

- Which fields should you delete?
- Do you want to show your BIP32 path to peers?

## PSBTv3 Possibilities

- What if PSBTv3 has totally new rules, and there’s a separate BIP for signing, plus another BIP for silent payments?
- Focus should be on composability.

### Challenges:

- PSBT is very hard to use. Roles don’t map or fit well. PRs have been open for years.
- Serialization format is okay, but the rest is difficult.

## Key Concepts in PSBT Usage

- **SP Wallets**: May not use BIP32, making some fields pointless.
- Make the BIPs identifiable in the PSBT itself, so it says “hey, I’m using BIP8426” and other computers can recognize it.

## Abuse of PSBT

- **WIF (Wallet Import/Export)**: A mess. Can I export a UTXO with a private key and shove it into a descriptor/PSBT? Kinda, but it’s messy.
- SP needs key export, but all we have is WIF.

### PSBTv0 - "Joined Semi Lattice"

- Rules about how to combine operations. This results in an explosion of error types.
- Fields need rules for aggregation as part of their definition.

## Transaction Weight and Signing Issues

- **Tx weight**: Affects all fields.
- **Taproot signing**: Fees are unknown, and the last signer determines them. This is very relevant to SP BIP discussions.
- **Fee rate**: Never defined in any PSBT BIP. Truck allows ephemeral anchors that can change fee rates.

PSBT is about a single transaction, but the ecosystem involves many transactions and chunks.

- Multiple PSBTs concatenated should work. Don’t make truck transactions impossible with PSBT; multi-transaction PSBTs are needed.
- Actually getting rid of tx is hard fork in blocks. But P2P you can do "chunks", we already have with TRUC, could do partial.
- Need to be aware of dependency tree in some protocols.

### SIGHASH Types:

- **SIGHASH_ALL**: Commits to everything.
- **SIGHASH_NONE**: Need to know exactly what you're signing (nothing?).

## PSBT in Exodus Wallet

- Exodus wallet uses PSBT for data transport between the server and the client (client holds keys). Same with bitkey. The server wants to learn as little as possible about the client.
- PSBT isn’t used universally. Want a standard so people can switch clients.

You should be able to serialize and deserialize. Should merging be possible?

- **Trivial merge**: Union of all fields, but redundancy could be an issue. Tx inputs are unique, no problem. Tx outputs can be equivalent, harder to sort.

## PSBT Serialization Format

Everyone uses Electrum and shoves extra JSON.  
People don't use PSBT. Example code / implementation is in C++ and ancient.  
BDK does use it, in Rust.

Want a serialization format for all these uses.

- **Not a transport protocol**, just a serialization format.
- Descriptors have string serialization, but a binary format is preferred.

Descriptor vs PSBT:

- Descriptor turns into PSBT but can’t be a real PSBT because it lacks outputs.

## PSBT BIP

- **New PSBT BIP**: Just a serialization standard.
- Then you can do signing. Different BIP, has roles: signature aggregator role vs signer role.
- Enumerating all requirements for single signer.

PSBT BIP doesn't really say what roles should _do_.
PSBTv0 offers little diagrams (e.g., for coinjoin), but super minimal example.

## What Fits Into PSBTv3?

- **Splicing**: Kinda, but LN never sends transactions over the wire, though it could.
- **Coinjoin**: Not really. Coinjoin transactions cannot be built in the open as it exposes privacy.
- **Silent Payment BIP**: Should define roles for PSBTs that others can understand. Include BIP-specific fields.

Anyone can construct a transaction from PSBT fields (e.g., 20 fields).

### Printable PSBT

- **isPrintable()**: Checks for core 20 fields. Once populated, fields shouldn’t change, but maybe they could—so people can back out.
- Silent Payment (SP) knows there will be an output but can’t sign until that’s been there.
- If **isPrintable()** can downgrade into a PSBTv0.

## Downgrading and Stable TxID

- PSBTv3 could allow downgrading to v0 for stable txid.
- **YGMI**: Missing, can't calculate a txid, has an explicit field that this doesn't have a txid yet, or will change.
- **StableTxid**: has txid but not signed / witness. txid won't change, also explicit.
- **FullySigned**: Indicates that the transaction has full signatures in the actual witness field. (before that it's in another field in the serialization)

## Combining PSBTs

- Define standard ways to combine fields, then can have a generic combiner.
- Concatenated PSBTs do need to be combined.
- `PSBT.Merge(PSBT)`, `PSBT.Reserialize()`, `PSBT.Extract(field)`.
- Informational BIP on construction phase, out of scope for serialization definition.

Define minimum combining role for locktimes.

- For merging, ensure keys are equal, or it fails.
- Trying to e.g. take the maximum of locktimes is too scary / too specific, that can be protocol specific and not in the BIP.

## Closing

- This could be a new BIP, like v1 or v3? Kind of a reduction of things in v2.
- Don’t want to interfere with other BIP
- A bare nLocktime can be a PSBT (chunk). No inputs = OK. No outputs = OK.
