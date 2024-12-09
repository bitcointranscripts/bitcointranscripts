---
title: Silent Payments and Payjoin
date: 2024-11-20
---

## Why combine Silent Payments and Payjoin?

- Silent Payments (SP) are non-interactive, while Payjoin (PJ) is interactive. Both aim to improve privacy.
- SP is **stateless**, which means no synchronization or complicated state management.
- One SP wallet can be used for multiple protocols, allowing the receiver to use one wallet and multiple addresses without increasing scan cost (unlike xpub and the gap limit problem).

### How can SP help PJ?

- Ensure SP works with PJ/ CJ (CoinJoin).
- Without this, stateful address reuse avoidance is the only way to do it.

## Does Blinding / Batch Proof make sense?

- Overload PSBT to absorb multiparty transactions/PJ.
- How important is it to update the PSBT spec? Or should it be a new spec or BIP? This is a potential bikeshedding issue.

## Blinding of Silent Payments

- All inputs are used to create a DH (Diffie-Hellman) point. If multiple users are involved, it leads to interactivity.
- Need to use blind DH protocol. This involves interacting ("hey do a DH with this point") with all the input keys, but the final transaction hides this interaction.
- DLEQ (Discrete Log Equality) is also needed for validation.
- Currently, DH blinding has been punted since it's not relevant for single-party transactions, but for multiparty transactions, blind DH is necessary.

### Similar Issues in Confidential Transactions (CT) in Elements

- Blinding is needed in CT. "PSET" (Partially Signed Elements Transaction) has a blinder.
- Need to figure out output ownership—unfortunately, outputs are not blinded, which risks losing anonymity.
- The receiver of the output doesn't need to participate, but the creator does need to claim the output during the transaction process.

### Multiparty Blinding

- Multiparty blinding **works**, but it requires more rounds.
- Unsolved issue: If two people in a CoinJoin want to send to the same SP address, the proof is reusable between them, so can re-use & fool them.

## Potential Solution: Wabisabi

- Could keyed verification credentials and messages to construct transactions help?
- Messages authorizing transaction construction would not directly affect the transaction itself.
- Proofs for outputs differ between users, and parties would evaluate the event log and come to the same state.

- This does not require anonymous credentials, and could work with ring signatures, as long as there’s a stable reference to the keys.
- If this works, blinding could occur without worrying about address collisions for multiparty transaction constructions.
- This might require a new BIP or PSBT v3.

- What makes it breaking and must be v3 instead of v2?
  - Need to collect inputs before you can make outputs.
  - Can't change inputs once you dervie outputs.
  - Construction process is very different, as in normal PSBT you can build in different orders.
  - Should be safe if signer is rational but feels brittle.

## Full Signature Aggregation in Bitcoin

- Signature aggregation could lead to better privacy, similar to transaction aggregation, where the transaction is not modifiable after signing.

## Data Model for Bitcoin

- A better model is to treat the block as one large collection of inputs and outputs, with no real horizontal lines between transactions.
- Package relay, custer mempool, these are all "chunks" of blocks, a groupings of inputs and outputs.
- The data model for Bitcoin should focus on the block itself as the primary unit, with everything else being a chunk. That's the way to go for aggregation / privacy / scalability.
- splitting off ephemeral anchors; block chunk can also be smaller than a tx. TXID containing witnesses was clearly a bug. Ephemeral anchors give us a way around that bug. Big tension between tx graph and useful things.
- All the chainalisys stuff is based on tx graph; we need to get rid of that and go to block.
- Limiting case: weak block protocol. I want these outputs to exist, willing to destroy these.

## Looking at Libbitcoin

- Remove forced ordering, get rid of blocks, do checks in parallel.
- Optimizing IBD over latency.
- The UTXO model is a great model, don't move away from it. But UTXO shouldn't have to do per transaction.
- Utreexo works like this, it doesn't look at txs, just blocks. A block is a bunch of deletes and adds, it can get cut-through automatically. It's really nice to be able to do one read and one big write for all the I/O for the block.

## Final Thoughts on Mempool and Blockspace

- The mempool can be altruistic—you can get blocks faster if you've got everything in mempool.
- Competitive fee markets result in more RBF (Replace-by-Fee). So the mempool/p2p data to block data ratio goes up, potentially leading to a preference for blocks-only in the future? Maybe not, the bandwidth used seems so low.
- Fee market: people pay 10X higher to get top of block.
- The world is getting more bandwidth and more CPU.
- Don't use blockspace for things you can use CPU or bandwidth for.

## Final 10-Minute Discussion

- DLEQ and PSBT BIP
- Adding new fields and relaxing signer rules could feel like a hardfork, but it might also be an extension of the existing BIP.
- Adding a new phase? achow101 doesn't want to add stuff to current BIP.
- Payjoin needs a notification mechanism and must allow cut-through to replace proposed outputs with their own outputs, requiring more rounds of communication.
- In SP, the sender has control over final outputs. If the receiver wants to send to others, the final round must be controlled by the receiver to avoid griefing by the sender. Punt for now; wait for multiparty protocol.

- Simple Start:

  - SP from the receiver's view.
  - Sender does Payjoin (doesn't know about SP).
  - Don't need a new BIP.

- Informational BIP on how to construct PSBTs to make sure their valid. Anon credential. PSBT lattice is miniPSBT.
- We didn't really join SP and PJ. But that's ok, this is bigger. If we just focus on joining SP and PJ; we need to join all the things. SP and everything; larger PSBT standard for txs.

- R5N Distributed Hash Table
- BIP 322 proof to post hot keys for messaging.
- Consensus on Adam Gibson curve tree (Zcash Orchard)
- hash-to-curve for current time to avoid equivocation.
- BIP 77 directory for key management.
