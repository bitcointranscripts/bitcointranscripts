---
title: Package Relay Primer
tags:
  - bitcoin-core
  - package-relay
  - p2p
date: 2023-04-25
aliases:
  - /bitcoin-core-dev-tech/2023-04-25-package-relay-primer/
speakers:
  - Gloria Zhao
---
Slides: <https://docs.google.com/presentation/d/12YPlmmaCiNNL83b3FDmYwa7FKHP7yD0krzkEzM-tkTM>

## Problems

## CPFP Doesn’t Work When Mempool Min Feerate Rises

Bad for users who want to use CPFP and L2s, but also a glaring limitation in our ability to assess transaction incentive compatibility

## Pinning

- being able to feebump transaction is a pinning concern
- counterpart can intentionally censor your transactions, and in L2 that can mean stealing your money because you didn’t meet the timelock

### Pinning examples

1. ANYONECANPAY -> anyonecanpin: add input that comes from huge unconfirmed low-fee rate tx -> absolute feerate needs to increase, so you're paying more fees for the tx to confirm slower
2. shared descendant limit can be monopolized
   1. descendant limit is 25 txs, so someone else can fill up that limit
   1. we have a carve-out for CPFP already to try and mitigate that
3. RBF Rule 3 is gameable
   1. replacement fees must > all descendants, and they may be large, low feerate -> expensive

- most L2s have pinning problems, so we need to fix that

## Get rid of txid-based relay

- we want to avoid txid based relay
  - can't deduplicate txid and wtxid that correspond to the same tx
  - can't deduplicate txs that only differ in witness
- we still require txid-based relay for orphans, because txs specify prevouts by txid -> so we don't know which wtxid to request

## Definitions

- pinning attack: a censorship attack on relay/mempool level, abusing policy
  - avoid getting into mempools
  - staying in mempool but never getting mined
  - a pinning attack is NOT paying more to get mined (even though it might be an attacker doing it, that's just a fee-based market)

- package: any list of transactions that can be represented as a connected DAG
- ancestor package: a package of 1 tx and its (unconfirmed) ancestors
- Descendant package: (fill in from slides)
- Package relay: relaying and validating packages together
- Sender-initiated: a node proactively announces packages they think their peers should download and validate together
  - in initial proposal: suggested announcing a child with all of its parents if assumed that peer does not have parents yet (e.g. becausee parents are toow low fee)
- Receiver-initiated: nodes can request packages when they recognize they're missing something

## Why is there so much mempool code?

- Peers are not trusted to provide correct information.

## Sub-projects and problems they solve

- Package CPFP: mempool logic to allow descendants to allow for ancestors. Accept packages, allow a child to bump a parent past mempool min feerate. Solves "CPFP doesn't work when mempools are full problem"
- P2P Package Relay: additional protocol msgs to request, provide, download package information on p2p network.
- Package RBF: also allow a child to pay for parent's conflicts (treat as 1 aggregated tx). However, painful pinning attacks still exist.
- v3 policy: for things that want robust RBF
  - make it feasible for them to be 0-fee without introducing dos vectors
- ephemeral anchors (built on top of v3) which allows anchors to be 0-value, which allows us to remove need for CPFP carve-out

## Progress so far

- we have:
  - package cpfp
- open:
  - v3
  - [#29633](https://github.com/bitcoin/bitcoin/pulls/29633) (looking for review)
  - [#27463](https://github.com/bitcoin/bitcoin/issues/27463): overview of package relay
    - also have a full branch for package relay

## Open questions exist

- how to make orphanage robust enough, currently 3 different approaches
- make a new mempool.dat file?
- do we want splice in/out to be covered by package relay/v3?
  - yes, but need to look into whether current approach is sufficient

## Walking through the BIP

- `ancpkginfo` provides a transaction's ancestors
- `getpkgtxns` allows the receiver to request any subset of the announced txs
- shows how Package Relay fixes CPFP. does not rely on feefilters as long as you don't reject a
  package because it contains a low fee tx.

Should there be a limit on the number of transactions in getpkgtxns? Should there be a limit on the
number of transactions in ancpkginfo?

- we already bound the network message size (to 4M bytes of payload)
- Could we ever generate a message that exceeds the limit?

`pkgtxns` should use the same order as `getpkgtxns`

`ancpkginfo` SHOULD sort topologically and include all unconfirmed ancestors and the tx itself.
However we cannot enforce this without matching chainstate.

The combined hash is lexicographic, so the same set of transactinos will always have the same identifier

`sendpackages` should perhaps specify how big an ancestor package would get accepted
alternatively, it should be left up to the receiver to deal with ancestor packages that are too large.

Looking for a different term for `pchCommand`

Q: How far is the pullrequest?

A: Tracking issue: <https://github.com/bitcoin/bitcoin/issues/27463>
some of the earlier pieces are opened as PRs. persisting ancestor sets over restarts, p2p messages to negotiate package relay, handling orphans more reliably. There are
about 5 more functional milestones to the whole project. One or two milestones per release seems reasonable.

Orphan handling should be made more robust, e.g. we request parent information from any peer that announced an orphan, and prefer outbound peers as the source.

Q: Could the P2P changes maybe all be activated on Signet together for testing?

A: Yes, there is a branch with the whole implementation already.
Unclear who needs it for testing, signet has a workaround (pseudo ephemeral anchors uses
prioritisetransaction) in the absence of package relay.

Mempool, Validation, Policy could be opened for merging in parallel to Orphan handling since different reviewers would be required.

The activation of the package relay feature would set a config option to default false which only would get set to true at the end of the last milestone.

Q: How does this interact with V3?

A: V3 would follow the activation of package relay.

Going into the Milestones:

## Milestone 1

1. "Don’t allow anything below min relay feerate (#26933)" was merged today. We generally don’t allow transactions with an individual feerate below minRelayTxFee, but V3 will permit 0-fee txs as the parent, and CPFP can be used to get past the dynamic mempool minimum feerate.

2. "Persist CPFP’d transactinos across restarts (#27476)" Loading mempool.dat does not enforce minimum feerate on loading, but afterwards trims the mempool to the permitted size.

- lots of discussion on importance and viability of the approach, PR to be deprioritized in the stack of work.
- possibly just amend the mempool.dat format that can store package relationships
- Just don’t modify `TrimToSize()`

3. validate package transactions with their in-package ancestor sets (#26711)

- want to be able to handle something more complicated than single-parent-single-child
- Allow any ancestor package
- Be lenient on what you’re provided with, e.g. take valid subsets of the package instead of rejecting the whole package if a part is inacceptable.
- find largest permitted subset
  – We defer Package RBF for the moment

## Milestone 2

- Orphanage is currently limited to 100 txs, up to 400 kB each
- Problem: Peer can churn orphanage by sending a ton of orphans
- Problem: does not effectively protect memory
- We randomly evict when orphanage overflows, but we might not be anywhere close to the theoretical max

Idea 1: only protect one package per peer, or have a huge potential upper limit

- terrible performance, tons of packages are gonna be dropped

Idea 2: Hard limit globally to a number of bytes, when you go over limit, evict things from peer that has sent more than 2*maxTxSize

Idea 3: Token bucket per peer to limit exposure to bad packages

Idea 2 gets the most positive feedback.

## Milestone 3

Add TxPackageTracker

Interface vision. This will be more interesting to discuss when looking at the code.

Rejection Caching

We need to continue downloading ancestor package information because someone could give you invalid information that could be superseded by correct information.
However, by keeping track of what we have gotten before, we would notice when we are offered the same invalid package or something that depends on something that was relayed previously.
