---
title: Package Relay BIP, implementation, V3, and package RBF proposals
transcript_by: Gloria Zhao
tags:
  - package-relay
  - bitcoin-core
date: 2022-10-11
aliases:
  - /bitcoin-core-dev-tech/2022-10-11-package-relay/
---
Notes on Package Relay BIP, implementation, V3, and package RBF proposals from Core Dev in Atlanta.

Also at <https://gist.github.com/glozow/8469dc9c3a003c7046033a92dd504329>.

# Ancestor Package Relay BIP

* BIP updated to be receiver-initiated ancestor packages only.
* Sender-initiated vs receiver-initiated package relay.
    * Receiver-intiated package relay enables a node to ask for more information when they suspect they are missing something (i.e. to resolve orphans). Sender-initiated package relay should, theoretically, save a round trip by notifying the receiver ahead of time that "hey, this is going to be a package, so make sure you download and submit these transactions together." As with any proactive communication, there is a chance that the node already knows this information, so this network bandwidth was wasted.
    * The logic used to decide _when_ to announce a package proactively determines whether it is a net increase or decrease for overall bandwidth usage. However, it's difficult to design anything to save bandwidth without any idea of what its bandwidth usage actually looks like in practice. We'll want to design the sender-initiated protocol carefully, and inform the design decisions using data collected from the mainnet p2p network. However, there is no historical transaction data to use because the goal is to enable currently-rejected transactions to propagate. For now, hold off on sender-initiated, deploy receiver-initiated package relay, observe its usage and figure out where we can save a round trip, and then introduce a well-researched sender-initiated package relay protocol.
* Reliance on BIP133 and p2p communication about fees/feerates.
    * We've updated our mempool acceptance policy's idea of minimum feerate, but not the way we send BIP133 fee filters. What if our fee filter is 1sat/vB and there's a CPFP of a 0sat/vB parent with a 1sat/vB child? That's not incentive-compatible to accept, but the peer will still send us the child. Can't easily fix this; we can't just send ancestor feerate or something.
    * Should BIP133 support be part of the negotiation? It isn't a strict requirement as the package would still propagate even if the receiver wasn't sending fee filters. The only issue is potentially downloading the child twice if the receiver isn't sending fee filters; the onus is then on the receiver to not send a "sendpackages" message. Bitcoin Core already supports BIP133.
    * Another discussion about including fee information in package information. The information cannot be trusted - the package should still be downloaded and verified. To get full feerate, you also need to know topology, individual size, and individual fees for all the transactions. Same conclusion that it's unnecessary.
    * General brainstorming about differences in node policies: would it make sense to have peers provide feedback on which transactions they rejected/accepted and use that information to allocate bandwidth / decide whether to relay?
* The use of partial blocks for package relay.
    * Partial blocks refers to a potential protocol message from miners to announce just-below-difficulty-threshold compact blocks (similar to mining pool shares but much less frequent), providing a sketch what transactions they are including in their blocks. Nodes can use this to pre-download and accept these transactions, ignoring policy rules since they are extremely likely to confirm and already have work on them.
    * Discussion was active but deferred*. This can be considered orthogonal to the package relay proposal, since it did not address the main motivations of the BIP (propagating packages to miners in the first place, orphan fetching, and reducing txid-based relay).
* Will polish the updated BIP and post.

# P2P Implementation
* Deduplication of rejected transactions to ensure we don't re-download invalid transactions but also don't accidentally censor things.
    * Splits our rejections cache (m_recent_rejects bloom filter) into fee-related rejection and non-fee-related rejection filters. Anything that fails for fee reasons (including mempool min fee and fee-related RBF) goes into the fee-related rejection filter, and everything else into the other one.
    * For packages and sub-packages that fail, add the transaction group by hashing the wtxids of each of the transactions, sorted lexicographically. Ensure that each group is itself an ancestor package. When a package is partially submitted, exclude the transactions that ended up in the mempool.
    * Upon receiving ancpkginfo, if an exact match is found in the fee-related rejections filter, don't request tx data. If any of the wtxids are found in the non-fee-related rejections filter, don't request tx data.
* Tradeoffs between bandwidth and memory requirements when downloading transaction data from peers.
    * Intuitively, it doesn't make sense to re-download transactions we already have in the orphan pool (currently bounded to 100 transactions to avoid an oom vulnerability), but that is a cross-peer data structure and currently makes no per-peer allowances. It is trivial for somebody to churn the orphan pool by sending lots of orphans, so an attack could render package relay useless.
    * What would it look like to guarantee that we store 1 package per peer? Implementation shouldn't be difficult, but this means a memory requirement of up to 101KvB (400KB serialized) per peer. With 125 peers, that's a 50MB requirement. This is acceptable because the per-peer memory requirement is small and everyone understands that resource usage scales with the number of connections.
    * Preserve at least 1 package of transaction data per peer, and limit to 1 in-flight package relay per peer. Similarly throttle package information requests.
    * Even with de-duplication, it possible to get O(n^2) download if a transaction chain is tx_1 ... tx_25 (tx_i spends tx_i-1), where tx_1 is 0-fee, tx_2-tx_24 are 1sat/vB (just above the node's fee filter), and tx25 pays for all of them? Each one will be rejected, then downloaded again when grouped with another "ancpkginfo." Solution: when announcing transactions to a package relay peer, only announce ones that don't have unconfirmed descendants.

# V3 transactions and package RBF
* Extremely simple, seems to work for LN. Makes mempool people happy because it also might let us get rid of carve-out and limits the size of connected components in mempool.
* Standardness of a transaction changes depending on chainstate. In the event of a reorg where transactions are re-added to the mempool, it's possible to need to evict V3 transactions in order to enforce its rules. Is this okay? Yes. We have other policies that necessitate the same thing, e.g. descendant limits.
* Package RBF only allowed for V3 transactions. Is it to ensure the ancestor feerate rule is incentive-compatible? The current rule is not 100% guaranteed so.
    * Imagine the original transaction, A, has a child B and co-parent C (i.e. B spends from A and C). C also has another child, D. B is one of the original transactions and thus its ancestor feerate must be lower than the package's. However, this may be an underestimation because D can bump C without B's help.
    * This is resolved if V3 transactions can only have V3 ancestors.
    * Is there ever a need to use a V3 descendant for both V3 *and* non-V3 transactions? Seems like no. There isn't any benefit to use a V3 transaction to bump a non-V3 LN Penalty commitment tx, since the pinning protections are not available. Ok then we can add this rule.
* So the new rules would be:
    * If a V3 transaction spends unconfirmed inputs, those transactions must also be V3.
    * When the directly-conflicting transactions are V3 (which means all original transactions are V3), apply the ancestor feerate rule.
    * Package RBF is only allowed when replacement transactions are V3.
    * Ancestor feerate rule is incentive-compatible when original and replacements are V3.
