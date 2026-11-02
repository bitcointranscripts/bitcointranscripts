---
title: Wallet Rebroadcasting
tags:
  - bitcoin-core
date: 2026-10-12
---

## Scope of the discussion

There are two parts to this discussion.

One is specifically about private broadcast and what I think is unexpected behavior. Interactions between wallet rebroadcasting and private broadcast raised the question of whether wallet rebroadcasting makes sense at all, particularly in the context of private broadcast.

There are two questions:

- In the long term, what should we do about rebroadcasting?
- In the short term, should we mitigate this unexpected interaction with private broadcast?

## Current rebroadcasting behavior

To summarize: Bitcoin Core rebroadcasts, every 12–36 hours, transactions with inputs or outputs that the wallet is interested in. It sends announcements to existing peers to which it has not already announced those transactions.

This depends on per-peer transaction inventory tracking. That state can disappear over time, potentially after restarts, and is lost after reconnecting.

It is reasonable to expect an adversary to make connections of different durations.

When you first broadcast a transaction, do you broadcast it to all peers?

Yes: anyone who has not already sent it to you, or to whom you have not already sent it.

For rebroadcasting, you also send it to everyone, subject to that filtering.

## Privacy risks for senders and recipients

There is a longstanding issue here for recipients. You can deanonymize people by sending money to outputs their wallets are interested in and waiting for them to rebroadcast the transaction.

For private broadcast, the relevant issue is that the wallet’s rebroadcast pool will contain these privately broadcast transactions.

The simplest case is an adversary maintaining one long-lived connection while also making shorter-lived connections to the same node. If you see the same node announce a transaction once and then announce it again later, even though the transaction never left the mempool, that is a strong signal that the node is associated with the transaction’s origin. There are more ambiguous cases, but there is a range of possible observations.

Rebroadcasting exists because users expect eventual confirmation. That is not a realistic expectation.

You cannot promise that feerates will fall enough for rebroadcasting to help. You already need a way to inform users that a transaction has failed to confirm.

In my view, the problem rebroadcasting solves is very rare under current mempool conditions. It only solves it some of the time, and I do not think there is a way to do it while preserving privacy.

It can cause real harm to users. On one side, your transaction might not confirm. On the other, you might reveal its origin. Those risks are asymmetric.

Having the wallet check these arguments is also a layering violation. Some version of the rule should be that you cannot combine rebroadcasting with private broadcasting. In the long term, we should remove wallet rebroadcasting.

It is also a footgun if you use third-party broadcasting: you can still be probed this way. In the medium term, we should heavily mitigate or remove it.

## Wallet accounting and user expectations

Should the wallet be aware of this? Changing it potentially breaks a number of things. The wallet sometimes errs on the side of telling users they do not have money when a transaction is neither in the mempool nor in the blockchain.

One reason we have rebroadcasting is that, if a transaction is neither confirmed nor in the mempool, the wallet can treat its inputs as spent without treating its outputs as created. Putting the transaction back into the mempool addressed that.

That is a user-experience problem. It is not a good reason to rebroadcast.

Yes, but the behavior is still misleading and unintuitive, especially when there are conflicting transactions.

We should not depend on mempool contents to calculate the wallet balance.

## Using private broadcast for rebroadcasting

Why can’t we use private broadcast for wallet rebroadcasting?

Not all users have Tor.

But we are talking about users who are using private broadcast.

That is not simple enough to backport.

There are also concerns related to package relay. One useful property of rebroadcasting is that, with child-pays-for-parent (CPFP), it can help low-fee parents near the bottom of the mempool get confirmed.

With private broadcast, we lose that behavior. If you broadcast a low-fee parent and then broadcast its child, the receiving peer may not accept them. There is no orphan fetching in private broadcast.

Could we send a package through private broadcast?

Yes.

Rebroadcasting has some bad behavior, but it is still useful.

Would coupling rebroadcasting with private broadcast fix all these issues?

No. Rebroadcasting is a mempool concern; private broadcast is not.

We need to treat all transactions as eligible for rebroadcasting, not just the wallet’s own transactions.

## General mempool rebroadcasting

These problems have been known for a long time. There was an effort to implement rebroadcasting more generally.

The idea was to track how many blocks had appeared in which you expected a mempool transaction to be included, but it was not. After some threshold, you would probabilistically rebroadcast it. This would apply indiscriminately, rather than only to wallet transactions. There were other issues, and that work became stale.

One thing wallet rebroadcasting does is reintroduce a transaction after it has fallen out of everyone’s mempool. General mempool rebroadcasting does not achieve that.

If a transaction falls out of your mempool and your wallet resubmits it, is that a leak?

Possibly, but it is more ambiguous.

In that case, the transaction leaves the mempool and the wallet resubmits it. From there, it is treated like other unconfirmed transactions. There is still some signal.

Are we still conceptually interested in general rebroadcasting? When miners do not behave as expected, or mine transactions that are not in your mempool, that undermines the heuristic. It causes extra rebroadcasting and could create a denial-of-service issue.

Cluster mempool makes this easier because you can compute the mining score cheaply.

## Template sharing

The `sendtemplate` proposal touches on this. The proposal is to send the top 8 million weight units of your mempool. The receiving peer could accept transactions it would have included in its own mempool, as well as some it might otherwise not have.

How is that different from rebroadcasting the top of the mempool?

You keep a sketch, compare it with the previous one, and send incremental updates.

But how is it different semantically, rather than mechanically? It is equivalent to rebroadcasting.

The argument is that we should eliminate special treatment of the wallet’s own transactions. The assumption would be that, as long as at least one connected node has a large enough mempool to retain your transaction, it will get rebroadcast.

But we also have expiry.

That is a separate issue. Transactions expire two weeks after you first learn about them. A recently raised concern is that, because of packages, you might expire something that is about to be mined.

## Mempool expiry

Why do we have expiry?

You want to be able to evict transactions so that the mempool remains functional under certain circumstances. Perhaps we need a better heuristic.

Expiry predates replace-by-fee (RBF). It used to be shorter, very close to the rebroadcast timer.

If your fees are too low and peers do not want to relay your transaction, that is effectively equivalent to censorship from your perspective. For example, a transaction admitted under your low minimum relay feerate might otherwise never propagate or confirm.

The strongest argument might be that we should make expiry much longer. But there could be something we have not considered that allows a node’s mempool to fill up over time with transactions that will never confirm.

If we remove expiry, rebroadcasting might not be useful. Resubmission makes sense, but rebroadcasting does not.

## Broadcast failures and mempool privacy

What happens if you click “Send” when you have no connections? A locktime/block race is another broadcast issue.

We should not allow sending when there are no connections.

In adversarial scenarios, is rebroadcasting effectively the same as resubmitting to the mempool?

Then should we avoid resubmission too? Does it make any difference?

There is a fundamental conflict between effective transaction broadcasting and keeping the relevant transaction pool private. [The source notes are unclear on the precise distinction being made here.] I do not think we should try to eliminate all mempool-related leaks.

That was the first approach to private broadcast. There were too many leaks. Assume the mempool is an open book.

Expiry does not make sense anymore. Rebroadcasting is useful when the mempool is full and fees spike; in that situation, there is no solution other than resubmission.

## Resubmission versus rebroadcasting

To be clear, resubmission means putting the transaction into your own mempool without announcing it to anyone.

Submitting a transaction to your own mempool is still a signal: a sufficiently powerful observer can infer that you are close to its source. That is inevitable.

This is a special case. In other circumstances, a node does not add a transaction to its mempool without broadcasting it.

Here, “submit to mempool” means adding the transaction without putting it into the broadcast path or announcing it with an `inv`. One existing case is wallet loading.

Rebroadcasting means putting the transaction in your mempool and telling everyone, “Do you want it?”

In that sense, resubmission is passive, while rebroadcasting is active.

The current behavior broadcasts the transaction regardless of whether it is already in your mempool.

There is an open pull request that would change this: if the transaction is already in your mempool, do not rebroadcast it; if it is absent, rebroadcast it.

As I understand it, there are three levels of behavior today:

| Behavior | Mempool handling | Announcement behavior |
|---|---|---|
| Resubmission on startup | Add the transaction to the mempool. | Do not broadcast it. |
| Submission when absent | Add the transaction if it is not already present. | Broadcast it when newly added. |
| Unconditional rebroadcasting | Add the transaction if needed. | Broadcast it even if it was already present. |

The suggestion is to remove the third behavior entirely.

## Active attacks using transaction replacement

That does not protect against an active attacker who tries to remove the transaction from the mempool.

Consider a test case: an attacker evicts the original transaction by creating a conflicting transaction that also spends another, unrelated output. The attacker then replaces that conflicting transaction by spending the unrelated output again. The original transaction can now be inserted again.

An attacker could use this to trigger rebroadcasting.

Because we rebroadcast transactions we receive, an attacker can use this to learn who owns an address. The target is the recipient, not the sender. Simply running a wallet passively for 12 hours can expose you to this.

That is worse because the attacker chooses the fee and timing. This was also raised as one reason to retain expiry.

Do not try to solve RBF cycling through this change. It is a qualitatively different problem.

We should not resubmit transactions that were replaced through RBF. We can track that.

The mempool notifications tell us when a transaction has been replaced, so the wallet can flag those transactions as replaced and avoid rebroadcasting them.

We might attempt to rebroadcast the replacement if it is in the wallet, but that needs to be checked.

Unless it has been abandoned.

We try transactions in the order in which they were added to the wallet.

That is worse!

## Longer-term changes and confirmation expectations

It seems we could feel reasonably comfortable removing rebroadcasting if we had something like `sendtemplate` and removed expiry. Removing expiry alone would not be sufficient, but with those changes there seems to be little downside.

There are still questions about how template sharing handles this. I do not think users should be so confident that an unconfirmed transaction will eventually confirm.

Without that expectation, are we effectively building around the assumption that a transaction is “cancelled” if it falls out of your mempool?

Consider a transaction with a middling feerate. If mempool demand is bursty, the dynamic minimum fee could rise and evict it. The transaction could become eligible to return shortly afterward, but fail to get back into the mempool in time.

`sendtemplate` would solve that problem if the wallet resubmitted the transaction to the mempool.

We also resubmit transactions when loading the wallet. Perhaps that is useful, though maybe less so with `persistmempool`.

There is the question of resubmission itself. Separately, who knows if or when `sendtemplate` will be merged? What do we do in the meantime?

Can we mitigate the most obvious problems?

## Proposed near-term mitigation

We should reduce wallet rebroadcasting to resubmission, still running on a timer if necessary. That would be an unambiguous improvement.

Resubmission would still reveal a signal, just as initial submission does. Doing it twice is worse than doing it once, and this change would not eliminate that.

We would need to quantify how much information is revealed. But this is a straightforward improvement. Once we have it, template sharing does not change much about that remaining signal.