---
title: Private Broadcast
tags:
  - bitcoin-core
date: 2026-10-13
---
## Status and goals

The discussion opened with an acknowledgment that private broadcast’s introduction in version 31 could have gone better. The feature had since been labeled experimental, and its privacy claims softened to describe best-effort protection. Participants reported that version 32 addressed several leaks, while acknowledging that others might remain.

The immediate questions were what to target for version 33 and what would justify removing the experimental designation. The main areas of work were:

- Defining the threat model and intended privacy guarantees.
- Separating broadcast behavior from the node’s other state.
- Supporting wallet transactions, including child-pays-for-parent (CPFP) and package-related behavior.
- Reconsidering how broadcast peers are discovered.

The central disagreement concerned whether to continue improving the existing implementation or adopt a more isolated broadcaster with a deliberately narrow interface and state machine.

## What should private broadcast protect against?

Participants distinguished between defeating straightforward transaction-origin monitoring, such as the model associated with LinkingLion, and resisting an adversary who actively probes a node and follows related transactions over time.

The existing implementation was described as an improvement against the simpler model. Stronger concerns involved an attacker combining observations across multiple broadcasts to associate a transaction—or a series of transactions—with a particular node.

The proposed primary goal was to prevent an observer from linking the sender’s IP address to a transaction through network-level probing. A secondary goal was to prevent one broadcast job from affecting another in ways that expose information.

This was not presented as a promise of complete anonymity or Sybil resistance. Participants acknowledged that some inter-job correlation might remain. However, they disagreed about which residual leaks were acceptable and whether the proposed design’s threat model and specification were sufficiently settled.

A recurring comparison was broadcasting through a public transaction-submission service over Tor. Proponents of isolation wanted a similarly narrow separation from the user’s node, but with more reliable delivery and without relying on a single submission service. The comparison was an architectural benchmark, not a claim that either approach offered unconditional privacy.

## Mempool feedback, retries, and active probing

The current design uses the transaction’s arrival in the local mempool as feedback that it has propagated, allowing private broadcast to stop retrying. Participants described this as effectively having two roles: one component sends the transaction, while the ordinary node listens for it to return.

That feedback helps with reliability, but it also connects observable broadcast behavior to local node state.

An attacker could potentially influence whether a candidate node has seen a transaction and then watch for subsequent broadcast attempts. Across related transactions, the presence or absence of retries could help eliminate candidate nodes and narrow down the sender.

The timing matters. A retry shortly after the initial attempt could provide a stronger signal than one many hours later. Participants suggested that longer delays would weaken the probe, but noted the competing needs of users who start a node, send a transaction, and do not leave it running for long.

Several approaches were discussed:

| Approach | Motivation and trade-off |
|---|---|
| Retry based on mempool feedback | Helps detect apparent propagation failure, but exposes behavior dependent on local state. |
| Make a fixed number of attempts on a predetermined schedule | Removes that feedback dependency, at the cost of continuing attempts even after successful propagation. |
| Increase the initial number of broadcast connections | Could reduce reliance on later retries, but does not by itself settle questions about timing or correlation. |
| Space retries farther apart | May weaken probing signals, but makes recovery slower and is less useful for short-lived sessions. |

An alternative implementation was described as making six attempts, including fallback behavior, regardless of the observed outcome.

Not everyone thought removing feedback was worth the trade-off. One argument was that propagation could be measured and that the existing approach appeared to work well. The counterargument was that privacy should come from a design that avoids shared state, rather than from repeatedly finding and patching individual leaks.

Ordinary broadcast was also used as a comparison: it does not provide a definitive success acknowledgment either. Private broadcast nevertheless needs some strategy for peers that simply accept and discard a transaction.

## An isolated broadcaster

The main architectural proposal was to move broadcast logic out of the existing network-processing machinery and into a narrowly scoped component.

The proposed component would have:

- A strict state machine that responds only to expected message sequences.
- A separate list of connection targets for each broadcast job.
- Retry behavior that does not depend on the ordinary node’s mempool.
- Minimal interaction with other node state.

Proponents argued that this would make the privacy properties easier to reason about. Any later connection to node state could then be introduced deliberately, with its information leakage assessed explicitly.

The implementation was described as a library with a command-line tool that performs one job and exits, alongside an integration that queues jobs inside the node. It did not necessarily require a separate process. The exact boundaries remained open.

There was interest in making this a replacement behind the existing `sendrawtransaction` interface, rather than requiring users to adopt a new RPC. Supporters considered a version 33 target feasible, but no delivery commitment or final design was established.

## Peer discovery without shared address state

Removing dependence on the ordinary node’s address manager, `addrman`, was the other major part of the isolation proposal.

The concern was that address information can itself carry a fingerprint. An attacker could introduce distinctive address information and later look for behavior connecting the broadcaster to the node that received it.

A separate `addrman` instance was suggested. Critics worried that collecting, maintaining, and selecting addresses would recreate much of a miniature node, along with the complexity and privacy problems the isolated design was intended to avoid.

The alternative tool used fixed onion peers and DNS seeds, with DNS resolution performed through Tor. Testing suggested discovery could add around 15 seconds to a broadcast, sometimes less. Some considered that acceptable; background discovery was mentioned as a possible optimization, though it would introduce more complexity.

The main objections and open questions were:

- **Fixed peers become stale.** As releases age, the implementation could increasingly depend on fallback discovery through Tor exits.
- **Release-specific peer lists may fingerprint the client.** Fixed onion seeds associated with particular versions were identified as something that might need to be removed.
- **Greater reliance on DNS seeds was contentious.** Some preferred ordinary peer-to-peer address discovery, while others prioritized the smaller state and interaction surface of a simpler mechanism.
- **I2P support was unresolved.** Participants questioned whether an equivalent to Tor’s remote-resolution mechanism existed and whether obtaining addresses from an I2P peer would be necessary.

The discussion also revisited the public-submission-service analogy. A narrow interface can reduce opportunities for fingerprinting, but concentrating interactions with one party has its own risks if a fingerprint remains.

No peer-discovery approach was selected. Proponents of the isolated design favored beginning with a small, understandable mechanism and adding complexity only where justified.

## Wallet integration, CPFP, and packages

Wallet support was a major practical goal. Participants wanted private broadcast to be available to ordinary wallet users, including for rebroadcasting, rather than only through selected transaction-submission RPCs.

The alternative implementation supported single transactions and one-parent-one-child (1p1c) cases. Broader wallet integration required deciding how the wallet would pass transaction dependencies to the broadcaster.

One proposal was for the wallet to use an interface analogous to `submitpackage`, supplying the relevant transactions together. For a transaction in a larger cluster, that could mean supplying the entire relevant package.

However, participants noted that general package relay was not available. Passing a list to the broadcaster would not automatically provide a protocol capable of sending it as a package. The broadcaster might instead need to remain connected and answer requests for the supplied transactions.

For opportunistic 1p1c relay, the discussed behavior was to begin with the child and wait for the peer to request the parent. This requires keeping the connection open long enough for the request-and-response sequence.

The privacy concern was whether different local mempool contents would cause different externally visible behavior—for example, changing whether the broadcaster offers a parent. Participants argued that the procedure should remain consistent regardless of the broadcasting node’s mempool state. The wallet would determine which transactions the broadcaster was authorized to reveal.

## Asynchronous broadcast and wallet accounting

Wallet accounting creates another dependency on the local mempool.

Participants described the wallet’s success condition as requiring the transaction to exist in the local mempool. Otherwise, balance reporting can become misleading, with a zero balance cited as a possible symptom.

Private broadcast cannot assume that a transaction will return through the network quickly or synchronously. It may usually happen promptly, but delivery can be delayed or fail. A broadcast job completing or timing out therefore does not necessarily mean the transaction is already available locally in the form the wallet expects.

This left an integration problem: how to preserve correct wallet behavior without making the private broadcaster’s observable decisions depend on the mempool.

Keeping local resubmission was mentioned in discussing the interface, but the notes do not establish a final solution.

## When should the experimental label be removed?

Participants disagreed about what the experimental designation should mean.

One position was that private broadcast should work throughout the wallet before it was considered non-experimental. Differences between RPCs were seen as confusing, although remaining opt-in would mitigate that concern.

Another position was that wallet integration could be added later as an extension. Under this view, the experimental label primarily signals that the interface or feature may change substantially; removing it creates a stronger expectation that the feature will remain available.

A privacy-focused criterion was also proposed: remove the label once the implementation adequately protects against linking client identity to transactions through network-level probing.

Isolation was presented as a way to reach that goal, but participants still wanted further scrutiny of the specification and acknowledged residual correlation risks. Neither the criterion nor removal of the label was agreed.

## Why integrate it into Bitcoin Core?

The discussion closed by considering why the broadcaster needed to be part of `bitcoind` rather than only a standalone tool.

The argument for integration was reach: `sendrawtransaction` is already widely used infrastructure. Making private broadcast available through a configuration option could encourage adoption and make transaction-origin inference harder for network observers.

Both forms were considered possible: a shared implementation wrapped by a command-line tool and by the node. The node integration was described as the primary target, with little or no change required to the existing RPC interface.

## Outstanding decisions

The discussion left several concrete questions unresolved:

- What active-probing and cross-transaction attacks must the feature resist?
- Should retries be independent of mempool feedback, and on what schedule?
- How should broadcast peers be discovered without sharing identifying node state?
- How should the design support both Tor and I2P?
- How should wallet accounting and transaction dependencies interact with an asynchronous broadcaster?
- What evidence and functionality would justify removing the experimental designation?

The main proposed direction was stronger isolation from mempool, address-manager, and network-processing state. Supporters viewed that as a more defensible foundation for privacy; the remaining debate concerned its reliability, discovery mechanisms, wallet integration, and the guarantees it could actually support.