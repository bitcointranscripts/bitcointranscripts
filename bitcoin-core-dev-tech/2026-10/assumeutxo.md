---
title: AssumeUTXO
tags:
  - bitcoin-core
date: 2026-10-12
---

Below is a thematic summary of both sessions, consolidating arguments while preserving the substantive disagreements. 

***

## Scope of the discussion

The first session asked whether AssumeUTXO was achieving its goals, what prevented users from realizing its benefits, and whether its implementation complexity was justified. The framing was itself contentious: some participants questioned whether calling it a potentially failed experiment prejudged the discussion.

The second session returned to those questions with four possible directions:

| Direction | Proposed approach |
|---|---|
| Remove AssumeUTXO | Remove the feature entirely. |
| Continue with the current design | Retain background validation and proceed with peer-to-peer snapshot distribution. |
| Retain snapshot bootstrapping only | Keep snapshot loading but remove automatic background validation. |
| Refactor the implementation | Preserve background validation while simplifying or separating it from the active chainstate. |

The central disagreement was not simply whether snapshots were useful. It concerned what validation guarantees a snapshot-bootstrapped node should eventually provide, whether the current architecture was necessary to deliver them, and how much complexity those guarantees justified.

## What should AssumeUTXO accomplish?

Participants described several distinct goals that were sometimes being treated as interchangeable:

- Make a node usable sooner.
- Provide a supported alternative to copying a chainstate or data directory.
- Allow a node to become usable quickly and subsequently validate the historical chain.
- Support users who ultimately want an archival node.
- Make bootstrapping accessible without manually locating and downloading snapshots.

These goals imply different requirements. A snapshot mechanism can provide faster startup without necessarily requiring automatic historical validation. Conversely, users who want eventual independent validation or an archival node need a path beyond loading a snapshot.

There was interest in retaining snapshot loading even among those critical of the current design. However, participants questioned whether the speedup was compelling enough. One comparison was with `prunedassumevalid`, which was described as completing initial block download (IBD) in roughly three hours on a performant machine—potentially in the same broad range as snapshot bootstrapping. Snapshot startup itself was reported to take around two hours on a good machine in some circumstances.

Those figures were not treated as settled benchmarks. Participants also identified implementation inefficiencies, including syncing blocks while loading the snapshot, that could obscure the approach’s potential.

## Background validation and the trust model

The strongest proposal for simplification was to retain snapshot loading while removing background validation.

Its proponents argued that users already rely on the snapshot before historical validation finishes. If they wait for validation to finish before using the node, much of the bootstrap benefit disappears. If they use it immediately, a later validation failure cannot undo decisions already made.

From this perspective, background validation was characterized less as immediate protection for the individual user and more as an expensive check on the snapshot commitment distributed with the software. The intermediate state—usable, but not yet independently validated back through history—was also considered difficult to explain.

Others argued that eventual validation is a meaningful guarantee, even if it does not eliminate the initial assumption. Removing it would lower the default level of validation. It also has benefits beyond the individual user: participants wanted more nodes to validate historical blocks and, where retained, make them available to others.

There was disagreement about how firmly background validation had originally been agreed upon. Some described it as integral to the original idea; others said it had never had firm consensus. The notes do not resolve that historical dispute.

The broader question remained: **should snapshot bootstrapping temporarily defer historical validation, or should it be an explicitly different operating mode that may never perform it?**

## Independent checking of snapshot commitments

A separate proposal was to have nodes performing ordinary IBD check the AssumeUTXO commitment when they reach the relevant height.

Instead of ignoring that commitment, a node would flush and hash its UTXO set, compare the result with the expected value, and report a mismatch. This was compared with the public checking practices surrounding AssumeValid and reproducible Guix builds.

The proposal had two separable parts:

- Add independent checking during ordinary IBD.
- Rely on that broader checking as a reason to remove background validation from snapshot-bootstrapped nodes.

Participants could support the first without accepting the second.

The check would apply to nodes passing through the relevant height; it would not retroactively reconstruct an earlier UTXO set for nodes already beyond it. Its cost was described as relatively modest, although no benchmark was established.

Important details remained open. Should a mismatch produce a warning or abort the node? How would users learn that other nodes had found a problem? No formal reporting protocol or centralized channel was proposed: the expectation was that people would publicly report discrepancies.

This approach would therefore distribute verification across independently syncing nodes, rather than give every snapshot user their own eventual historical check.

## How much complexity comes from multiple chainstates?

Critics of the current implementation argued that concurrent chainstates affect much more than snapshot loading. They cited:

- Locking problems, race conditions, and difficult loading states.
- Reorganization handling and situations with unclear recovery paths.
- Cache resizing, copying, and limits on preallocating resources.
- Resources multiplied per chainstate, including a cited example of eight prevout-fetching threads per chainstate.
- Complications involving block indexes, missing undo data, and block availability.
- Extra work when changing IBD, database compaction, or write-amplification behavior.
- Additional RPCs, documentation, and user-facing state.

Their concern was that validation code repeatedly has to account for two chainstates, making otherwise independent improvements harder to implement and review. Outstanding work was said to be collected in issue #32377, with concern that relevant pull requests were not receiving enough review.

Others disputed the scale of the problem. They argued that these were not necessarily the largest sources of complexity or bugs in the codebase, and that some separations introduced for AssumeUTXO were architecturally useful in their own right.

In particular, separating chainstate management from an individual chainstate was not universally considered a mistake. Removing concurrent chainstates would not automatically justify merging those responsibilities again.

Several participants wanted a concrete removal patch before accepting claims of substantial simplification. The first session ended with a stated intention to open a pull request removing background validation and multiple snapshot checkpoints so that the effects could be assessed.

## Could background validation be retained in a simpler form?

Round 2 put more emphasis on alternatives to either keeping the implementation unchanged or deleting background validation.

One proposal was to validate historical blocks using a simpler UTXO view rather than another fully featured chainstate. This could avoid duplicating functionality needed by the active chain, although the suggestion that historical validation need not handle reorganizations was challenged: the snapshot’s base block could itself become stale.

Other possibilities included:

- Running historical validation in a separate context or process.
- Syncing into another directory while continuing to use the snapshot-bootstrapped node.
- Coordinating the two through inter-process communication.
- Providing a specialized command-line mode for a later independent sync.

Such separation might also help users move from a pruned node toward an archival one. The objection was that this could merely relocate the complexity, or create a new workflow users could already approximate with a separate sync.

Kernel work provided another reason to examine the architecture. Participants distinguished the ability to operate on multiple chainstates from a large manager object coordinating them inside the kernel. Some argued that this coordination belonged in the node instead.

Earlier simplification work, including PR #30214, was cited as a starting point. Draft or near-ready prototypes were mentioned, but the discussion did not establish that any proposed refactor would deliver the expected reduction in complexity.

## Snapshot distribution, usability, and adoption

Draft PR #35054, concerning peer-to-peer UTXO snapshot sharing, brought the broader design questions back into focus.

Some participants considered distribution a separate issue: objections to AssumeUTXO’s existing architecture should not automatically become objections to the P2P implementation. Others felt the intended future of the feature needed to be clearer before adding another major component.

Manual snapshot acquisition, including downloading through torrents, was identified as a barrier. P2P distribution could make bootstrapping more compelling, but participants cautioned against assuming that it was the missing ingredient that would produce adoption.

Other usability concerns included slow snapshot loading, competition with block synchronization, and the need for a straightforward graphical interface—described as a button in Qt—rather than a manual procedure.

Comparisons with shipping a prebuilt chainstate or data directory exposed differing priorities. Some wanted AssumeUTXO to compete directly with that convenience. Others emphasized that Bitcoin Core’s value also lies in its validation practices, review processes, and the trust those processes support.

The discussion repeatedly returned to a product question: **if AssumeUTXO did not already exist, which version of it would participants want to add today?**

## Other validation models and configuration choices

Several alternatives were raised without being resolved.

`prunedassumevalid` and SwiftSync-related approaches were discussed as potentially faster or simpler ways to sync or check that a reconstructed UTXO set matches a snapshot. Participants questioned what guarantee such a check provides when historical scripts are not checked, and whether these combinations correspond to understandable user workflows.

Another suggestion was to rely temporarily on the most-work chain for early transaction visibility, followed by background validation. Critics argued that this introduced a different trust model, closer to SPV, and potentially a larger systemic risk. Any temporary assumption, they argued, should be precisely defined rather than described loosely as trusting miners.

Possible user-facing configurations included full synchronization or archival operation on one hand, and a cheaper, pruned AssumeUTXO mode on the other. Another proposal was to trade the complexity of background validation for P2P snapshot distribution and connect that to a lighter validation mode.

Participants also considered allowing background validation to be paused or disabled, perhaps eventually disabling it by default. This could meet some users’ immediate needs or reveal demand for the feature, but it would not remove the underlying code or documentation burden.

Finally, retaining only the newest snapshot commitment was proposed as a simplification. The counterargument was that older commitments support serving snapshots to different client versions; the actual complexity saved remained unclear.

## Outcome and unresolved questions

Neither session selected a direction. Snapshot bootstrapping continued to attract interest, but there was no agreement to remove AssumeUTXO, remove background validation, or proceed unchanged.

The main avenues for further work were:

- Add independent checking of snapshot commitments during ordinary IBD.
- Produce concrete patches demonstrating the effects of removing background validation.
- Compare those patches with refactors that preserve validation in a simpler or separate context.
- Address snapshot-loading performance and usability.
- Clarify which guarantees and user workflows P2P snapshot distribution is intended to support.

The central unresolved trade-off was between **a simpler snapshot-based bootstrap with explicitly limited validation guarantees** and **a bootstrap process that automatically progresses toward independent historical validation**. Participants disagreed both about the value of that progression and about whether its current implementation cost was inherent or could be substantially reduced.