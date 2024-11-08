---
title: Future of SPV Technology
transcript_by: Bryan Bishop
tags:
  - lightweight-client
---
<https://docs.google.com/document/d/1t0bSZj5b66xBdW7xrjHlcvfqYAbTaQDB4-_T0Jvs3T4/edit#heading=h.5lm45oa6kuri>

issues with current SPV wallets

Existing clients and their status

* bitcoinj
* electrum
**    they are doing SPV proofs
**    bloom filters

utxo commitments need to get in
need to pick which type of utxo commitments

Number of nodes to connect to for more SPV clients

1 header from each peer to verify that we are all getting the same thing
what block does each peer think is the best?
very cheap to poll a huge number of peers

“commit to a bad block”

* is SPV completely broken? privacy failures with bloom filters
* commit to a bloom filter, only ask for the transactions you want
* you can use pynchon gate and riposte for messaging (like anonymous remailers)

what’s the benefit of the SPV model over the electrum model?

why would a node want to communicate with SPV nodes at all?

off-chain contracts for SPV, pay per query

storageless full-nodes (full verification, but no blockchain storage)

make each node have random fraction of utxo set

bitcoinxt getutxos does not have proof, sybil insecure

spents vs unspent - use unspent, otherwise super large

* order by fee per byte is for block header somewhere, not utxo set commitments
* for commitments to occur, need order
* soft-fork, but not for headers
* utxo commitments don’t have to be in the blockheader
**    miners must only optionally include it
**    if they don’t include it, it’s fine

how to order utxo data before merkleizing it

take historical utxo set, then make updates in same way as everyone else
rules for when to merge the tree updates

headers should have a commitment to other headers in the coinbase transaction output

* utxo commitment - tree, leafs should be sorted by outpoints
**   reduce resource requirements for tree updates
**   also maintain a set of tree update deltas
**   large pile of tree update deltas should be merged into the actual tree

SPV fee estimation
    worried about high fees, not low fees (assuming replace-by-fee)

SPV handling of lightning network and payment channels
    might require utxo set commitments

what’s the purpose or use case of SPV

who funds spv wallet development? does anyone? who might?

lower infrastructure requirements, don’t have to run giant third pirty central server


riposte - private information retrieval, reversal of pynchon gate model


Bitcoin Core should have an SPV implementation
there’s a branch for SPV
start a full-node, throttles verification
why should this be a separate protocol, should be default part of protocol

Summary points

* utxo commitments need to happen, soft-fork
* headers should have a commitment to other headers in the coinbase transaction output
* updatable utxo commitment trees for spv and other reasons
* there should be a SPV implementation in core
* talk to more SPV clients, 1000s of connections
* fee estimation - should you do anything at all?
* lightning network + spv for your phone or other low-powered devices
* argue for spv development for low infrastructure requirements
* pay per query for SPV
* bloom filters don’t work in SPV, denial-of-service problems, need private information retrieval protocol like riposte
