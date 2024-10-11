---
title: Sydney Socratic Seminar
transcript_by: Michael Folkson
tags:
  - package-relay
date: 2021-11-02
---
The conversation has been anonymized by default to protect the identities of the participants. Those who have expressed a preference for their comments to be attributed are attributed. If you were a participant and would like your comments to be attributed please get in touch.

Agenda: <https://github.com/bitcoin-sydney/socratic/blob/master/README.md#2021-11>

Package Mempool Accept and Package RBF: <https://gnusha.org/url/https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-September/019464.html>

With illustrations: <https://gist.github.com/glozow/dc4e9d5c5b14ade7cdfac40f43adb18a>

## Intro

I think the best thing for me to do is go through Gloria’s [mailing list post](https://gnusha.org/url/https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-September/019464.html). We’ll go through the package relay acceptance rules and look at how they differ from the existing BIP 125 rules which we had a whole [Socratic](https://btctranscripts.com/sydney-bitcoin-meetup/2021-07-06-socratic-seminar/) about a few months ago with Antoine Riard. Gloria can interject whenever she feels like talking about anything in particular. We are going to go through this excellent mailing list post that Gloria made with all these awesome pictures. We’ll talk about how the package relay rules may differ from [BIP 125](https://github.com/bitcoin/bips/blob/master/bip-0125.mediawiki) replace-by-fee rules. These are the existing rules you apply when you get a transaction to see if you are going to include it in your mempool or not and whether you are going to pass it onto other nodes. With packages, which are single transactions relaying multiple transactions you need variations in these rules. They are really carefully thought out here and explained. A really valuable post. Let’s start going through them.

## Existing package rules

<https://gist.github.com/glozow/dc4e9d5c5b14ade7cdfac40f43adb18a#existing-package-rules>

As we already talked about Bitcoin already has these packages in Bitcoin Core as data structures but they are just not put over the network. That is correct?

Yeah they only exist within your mempool. We don’t think about packages until they are already in our mempool. We want to be able to validate them and relay them.

The reason packages already exist, one of the reasons would be child-pays-for-parent?

Yeah exactly. A small correction, BIP 125 is just replace-by-fee rules which is one of many mempool validation rules.

They are the rules you use to decide whether to replace if there is a conflict between the transactions coming in.

Right.

So the existing package rules, there is this `MAX_PACKAGE_COUNT`. This is the hard limit of the number of transactions you can have in a package. You have also got the `MAX_PACKAGE_SIZE`. BIP 125 has a [rule](https://github.com/bitcoin/bips/blob/master/bip-0125.mediawiki#implementation-details) about not evicting more than 100 transactions. This is another constraint about how big sets of descendants can be. You have this `MAX_PACKAGE_SIZE`. In our existing mempool logic if you are adding an individual transaction you are not allowed to create chains of more than 25, an ancestor and descendant limit. A transaction with all of its ancestors or all of its descendants cannot exceed a count of 25 or 101 kilo virtual bytes. This naturally informs these package limits. If you have a package that is bigger than this it is going to be exceeding the mempool limits. It is a very natural bound.

Is it possible to put the logic together, the RBF rule of not evicting more than 100, is it possible to still have 99 be evicted with the `MAX_PACKAGE_COUNT` at 25 or is it like 25 is the real limit?

You can be conflicting with 100 different transactions that are independent in the mempool.

They are orthogonal basically.

Yeah.

To clarify, is this when you try to replace multiple transactions? Can you walk me through an example as to when the 100 transaction limit can occur?

Let’s say you are trying to validate a transaction and it has 100 inputs. Each of those inputs is also spent by a transaction in your mempool. But those transactions in your mempool are not related.

You have multiple conflicting transactions? Or are you replacing multiple transactions with a single transaction?

Yes. I think people get confused because they think of there only being one original transaction. They are like “It is not going to have more than 25 descendants so how can you hit 100?” But you can be conflicting with many independent transactions.

One transaction can spend 10 different inputs. Each of those inputs can have a package of 25 associated with it.

[This](https://gist.github.com/glozow/dc4e9d5c5b14ade7cdfac40f43adb18a#existing-package-rules) is what the rules look like and how they would affect the relay. The basic one (1A), you’ve got 24 descendants, then you try to package with 2 more in it, doesn’t work. 13 with a package with 2 more in it is fine (1B).

Basically package validation is hard because you are trying to prevent DoS attacks. If you have even just a package of 2 transactions the number of possibilities for interconnectivity with the mempool just gets more and more complex the more transactions you have. The reason why we have ancestor or descendant limits, also known as package limits confusingly, within the mempool is so we can limit the potential CPU time we are spending spinning around trying to find everything that we need to evict or everything that we need to update in case we get a block or we get a conflicting transaction, a replacement or whatever. But because it is really complex with packages we have to do one of two things. Either we very intensively compute all the different relationships before we admit it to our mempool, which can take a long time, or we use heuristics such as the one in [21800](https://github.com/bitcoin/bitcoin/pull/21800) where we assume that the package is very highly connected. But we have to be careful about the way that we construct these heuristics because if it is too loose or too imperfect then we might accidentally create a pinning vector. That’s what this section is about.

“The union of their descendants and the ancestor is considered”. What does that mean?

When we are looking at one transaction it is very easy to calculate what the ancestors in the mempool are. But with packages they might be interconnected, they might share ancestors. So what we do is we take the union of every transaction in the package’s ancestors and that needs to meet the ancestor count. This works for a package of several parents and one child because the union of their ancestors is the ancestor count of the child in the package. The fact that the packages only include a child and its parents, that’s the rule. Is that already in the logic or is that part of the change here?

That’s part of the proposed change. This section is just existing rules that were added in previous PRs earlier this year.

So the union just means you get every single descendant. When you are looking at a package does the package have to have to all the ancestors in it or if some of the ancestors are in the mempool, is that ok?

Yeah this is mempool ancestors.

Some of them can be omitted from the package if they are already in your mempool, that is normal.

Yeah that’s normal.

Which ones are the interesting ones here? In 2A, there is this ancestor with two branches each with 12 in it. There is a package with A and B as the nth child of those branches but A and B aren’t connected to each other at all. Can a package have totally unrelated transactions to each other?

Not in this proposal. But when I wrote the code for ancestor descendant limits since arbitrary packages were allowed I needed to create a heuristic that would work for arbitrary packages and never underestimate the amount of ancestors/descendants. It is supposed to work for arbitrary packages but the heuristic calculates the exact amount for the packages I am trying to restrict us to in this proposal which is child with parents.

The plan is only to allow these child with parents to be broadcast?

Yeah.

The third row is probably more indicative of what we would actually see. In 3A there are two parents, the child is in pink, there is only one layer of parents. There are not parents of parents in the package?

Yes. That’s a restriction, that’s intentional.

## Proposed changes

<https://gist.github.com/glozow/dc4e9d5c5b14ade7cdfac40f43adb18a#existing-package-rules>

Here are the proposed changes. There is multi-parent, one child, two generations in them. They may contain already in mempool transactions and they can also refer to transactions that are already in your mempool. This picture demonstrates things that stick to that rule. One interesting one is D, although there are only parents of P4 in D, P2 is a parent of the parents. There are parents of parents, it is just that they all must be parents of the child.

Right.

In the previous diagram C what do the dots imply?

It is just shorthand for 1 through 24. It means there is P1, P2, P3 etc all the way to P24.

At each individual layer of those parents there are another 24 of them. The second dot implies another parent.

They are also arrows. P25 is spending all of them.

Ok, understood.

## Fee-Related Checks Use Package Feerate

<https://gist.github.com/glozow/dc4e9d5c5b14ade7cdfac40f43adb18a#fee-related-checks-use-package-feerate>

Without conflicts you need to check that the transactions have a good enough fee. The min relay tx fee which is usually 1 sat per byte. But now we have packages and one of the points of package relay is so that this may not apply to transactions individually and could rather apply to the whole package. The point of this is Lightning where you want to do child-pays-for-parent, you don’t have to include fees on each transaction but rather you can bump the fee exclusively with fees of another transaction, a child. You can have a transaction with zero fee that is relayed as long as it is part of a package where the total fee rate of the package is above the min relay tx fee. Am I right there?

Yes.

The section is rationale for using the package fee rate after deduplication. A lot of the thinking around the package fee rate is you want to make sure that your policy is incentive compatible. For example if you had a package where the child pays lower fees than the parents then you want your behavior to reflect what would be most economically rational. And also you don’t want to allow the child to be paying for things twice. It should be able to boost the fee rate but you don’t want people to be able to cheat. F and G are the examples where if you use the package fee rate before deduplication you might end up using the same fees to pay for more than one thing.

This notation here means this is replacing this one. P1 is replacing M1 in F and P2 is replacing M2 in F. The question we are considering here is should this package here in the light orange replace these light blue ones. If these two were not in the mempool this would be a fine package to include. But these are in the mempool and so should we be able to remove them and replace them with P3 that has a nice juicy 600 sat fee. The answer is no. It adds 200 sats but it is adding 300 virtual bytes. The rule is you need at least 1 sat per byte over the existing ones that are there, the min relay tx fee over the ones that are already there in order to replace them. Even if the fee is a little bit better it is not good enough. It has to be 1 sat per byte better and it is not here.

Exactly.

In G1 we are fine. We have 100 sats and 100 virtual bytes and that is fine. There is 1 sat per byte more so we evict it and add P1.

G2 is an interesting one. When you get a package you remove the thing from the package that is already in the mempool. What is the rationale for that?

You are essentially de-duplicating. If it is already in your mempool you don’t need to be checking it again and you shouldn’t use its fees again.

That’s the key point. After de-duplicating here you can see that this adds 200 vbytes and 100 sats. The point is although this package includes P1 we can just include P1 without P3 and P2. If P1 is already in our mempool we can say “Let’s just include that”.

You definitely shouldn’t include its fees. For example here if you included P1 then you would think “I have enough fees to replace M2”. It would look like you are adding 300 sats and 300 vbytes which would be enough. But you already used M1’s fees to pay for the replacement of that other one in diagram G1. You used those fees already so you shouldn’t be trying to use them again.

Let’s say M1 didn’t exist. Let’s consider G2 in isolation. MP1 is P1, it is the same one. It is irrelevant whether MP1 is in the mempool already, you just want to consider it in isolation. In other words replacing M2 only depends on P2 and P3. Is that the right way to think about it?

Yes. If MP1 isn’t already in the mempool you need it in order to validate P3.

The fees of MP1 do not matter in the case of considering whether to add this package of P3 and P2.

If it is not already in your mempool then it is fine to use its fees. But if it is already in your mempool then you definitely shouldn’t because it already used its fees to pay for something.

That’s interesting. Isn’t the point of it to have the best transactions in the mempool? Regardless of what is already in your mempool shouldn’t you just choose the transaction set that is the best? Or are you saying that rule is not as important as keeping packages together? Packages should be excluded or included as a whole.

The goal is to have the most incentive compatible transactions. This is later in the document but you will consider P1 individually and you’ll do that before you try to validate as a package. You’ll pick whatever is best. You can pick just one package or some subset of it if that turns out to be more economical.

You are going to add things individually and then when something doesn’t get added as an individual then you start to consider the package at that point?

Exactly.

What you are talking about here only applies after you’ve done the individual adding. You are not lowering the quality of the mempool in any way.

No never.

I receive a package and if there is some zero fee transaction I skip that and after adding each transaction one by one then do you check the zero fee transactions with respect to the whole package?

You have a package and it has transaction A, B and C. A has a zero fee?

G2 is a pretty good example, a good structure. You would try adding P1 first, that’s fine. Then you would try adding P2, it says “That is not going to work”. You can’t add P3 because you don’t have P2. Then you start considering P2 and P3 as a group.

## Package RBF

<https://gist.github.com/glozow/dc4e9d5c5b14ade7cdfac40f43adb18a#package-rbf>

This is package RBF which is the modification of the [BIP 125 rules](https://github.com/bitcoin/bips/blob/master/bip-0125.mediawiki#implementation-details). The first one, does this use the same signaling mechanism as BIP 125?

Yes.

Just before we go into RBF. With the mempool it is either in the mempool or it is not. There is no intermediate state. Let’s say a package successfully got into the mempool and then the mempool became aware of another transaction so that the package was no longer the most incentive compatible option. Does it then ditch that package? Or should it perhaps hold it in an intermediate state in case things change again?

If you accept the package to your mempool and then you see a conflicting package?

Yeah. Or a transaction that conflicts with the package but it is offering more fees than the package in entirety.

Then you’ll validate that new package the same way you validated the original package. If it pays significantly more fees then it can replace whatever transactions it conflicts with in the mempool.

Is there an edge case here sometimes where the mempool ditches some transactions, perhaps a whole package but then things change again with the introduction of a new transaction added to that package but you’ve thrown away the initial package?

We want to keep our mempool in a consistent state. We don’t want conflicting transactions in our mempool.

To me it seems like you might want like a second mempool while things are still in flux where you dump things there that you don’t think should be in the mempool but then if things change with the introduction of a new transaction then perhaps you bring it back. Obviously once you’ve ditched it from the mempool if you want to get it back you have to go and ask your peers for it.

Not necessarily. We have various caches for transactions that we’ve evicted from our mempool.

We keep them around for a decent amount of time?

For reconstructing compact blocks for example.

So the intermediate state is a cache.

A little bit but it is not part of the mempool. That’s why we have rules that say “If you want to replace a transaction in the mempool it has to be a significantly higher fee”. We are going to keep the best one.

You would never go to that cache to get things out of it? To put it back in the mempool?

No. You could end up re-requesting things.

When would you re-request something?

In this scenario you evicted something and then later you get a really high fee child of it for example. You already threw it out of your mempool and you like “Missing inputs. I need this transaction.” You need to re-request it from your peers.

You could use the cache instead of re-requesting it?

You could theoretically.

Ok so the signaling. I guess this means that everything that is RBF’ed has the signaling in it. It is set with the sequence number. Here is a new rule, New Unconfirmed Inputs (Rule 2). A package may include new unconfirmed inputs but the ancestor fee rate of the child must be as high as the ancestor fee rates of every transaction being replaced. This is contrary to BIP 125 which states “The replacement transaction may only include an unconfirmed input if the input was included in one of the original transactions”. The original BIP 125 was written mostly for wallets who want to bump their fee. When you bump a fee you are going to spend the same inputs, you may add another one, but you are mostly going to spend the same inputs or lower the value of one of your outputs, usually your change output to get more fees. This package rule is more sophisticated than this because we are not dealing with just simple wallets anymore, we are dealing with Layer 2 protocols which need to use child-pays-for-parent. I guess that’s the main motivation.

Yes. Not to knock RBF as it was originally implemented but they were constrained by what the mempool data structure was able to provide them at the time. We have a better mempool now so we are able to have more intelligent rules around RBF.

What does it mean, ancestor fee rate? We have this structure, this package that has children and parents. The child has a fee rate, including the child you can figure out the fee rate of the child in so far as its parent is replacing something in the mempool. You have to look at every single thing you are evicting and see if the ancestor fee rate to the parent that it is replacing double spending the one that is in the mempool is higher than the one that was in the mempool. I don’t know if that is a coherent way of saying it.

Your replacement needs to be a better candidate for mining.

That sounds better. What do you have to consider to figure out that fee rate? Is it a fixed value per package or is it more it is different value when you are comparing it to the transaction you are maybe evicting?

An ancestor score is the total modified fees of this transaction and all of its unconfirmed ancestors divided by the total virtual size of that transaction and all of its unconfirmed ancestors. Essentially you just need to go look at the mempool and calculate all of its ancestors. Get the sum total, divide it and you compare that to the ancestor score of each mempool entry that you are trying to replace. Luckily now that we have more information in our mempool data structure that information is actually cached in each mempool entry.

Is it every unconfirmed ancestor or every new one that you are adding?

Every unconfirmed ancestor.

The rationale makes sense. The purpose of BIP 125 Rule 2 is to ensure that the replacement transaction has a higher ancestor score than the original ones. Example H shows that a new unconfirmed input can lower the ancestor score of the replacement transaction. If we only consider P1 by itself it looks better than that one. But this one needs M2 to be in the mempool whereas before this one would be low priority in the mempool, this one is high priority. P1 shouldn’t get in there without considering the fact that it is attached to M2.

I’ll leave the more complicated examples here. It did take me quite a long time to get to the bottom of them.

It is better with pictures though I hope.

So much better. I wouldn’t even attempt to do it without the pictures.

From an engineering perspective the reviewers are probably really happy to have these pictures.

The next one is the Absolute Fee Rule (Rule 3) which also exists in BIP 125. The package must increase the absolute fee of the mempool i.e. the total fees of the package must be higher than the absolute fees of the mempool transactions it replaces. This differs from BIP 125 Rule 3, it has the bonus now. You can have a transaction with a zero absolute fee and it can still get into a block because the rule is applied to the package now.

Feerate (Rule 4), we already went through that a bit originally. The package must pay for its own bandwidth. You need a 1 sat per vbyte improvement over whatever you are replacing. It must be higher than the replaced transactions by at least that much.

Total Number of Replaced Transactions (Rule 5) states the package cannot replace more than 100 mempool transactions.

The final bit of this is to talk about why you add individual submission, we’ve gone through that a little bit.

## Q&A

One thing that did change, Rule 2, “The replacement transaction may only include an unconfirmed input if that input was included in one of the original transactions”. Wasn’t there also a rule where BIP 125 had to have everything confirmed? In Bitcoin Core [PR 6871](https://github.com/bitcoin/bitcoin/pull/6871) there is a comment in main.cpp “We don’t want to accept replacements that require low feerate junk to be mined first. Ideally we’d keep track of the ancestor feerates and make the decision based on that but for now requiring all new inputs to be confirmed works.”

That is rule 2, if there are any additional inputs they need to be confirmed.

Or they already need to be in the transaction.

Yes.

Does that rule apply to non-packages going forward if you were to implement package relay? This proposal is not yet about the peer-to-peer layer…

I have a confession. I’ll admit this is also bundling in my desire to change our RBF logic. Essentially when RBF was first implemented I said they had a lot of limitations. Rule 2 is an ugly hack or a very bad heuristic. I want to change that but there are always a lot of people nit picking about what to do about BIP 125. You never get anywhere. I was like “We can bundle this in with package RBF and since these rules are better we can gradually introduce them for individual transaction RBF”. That’s my ulterior motive.

We have to do this rule. When you are writing a wallet you have to go “Is it confirmed. I can’t use that thing in the mempool, it is already there”. Different logic to when you are normally constructing a transaction. You have to have this context of am I doing a RBF? It is just bad. That may not apply initially, is that what you are saying?

I have a [PR](https://github.com/bitcoin/bitcoin/pull/23121) open to do this for individual but it has been thousands of words of arguing about disclosing to the mailing list and BIP 125. It is an ugly fight.

I agree with you changing that because it sucks to have that in the wallet. Can I hack my new transactions to be in a package through the RPC? Can we make sure that I get my original transaction into a package so that the package rules apply instead and we can delete that code?

I would imagine that package relay will be mostly a peer-to-peer thing and not really need to be considered in wallets. Ideally you and your peers, you are sending fee rate filters to each other. If you can see that your peer is going to package validate in order to accept this low fee parent, high fee child then you construct a package for them. You just let them know “Hey make sure you package validate this because it is below your fee filter but the package fee rate meets your fee filter”. I don’t think there’s a hack you can do where you always submit packages rather than individual transactions because the concept of package relay is really more node to node than something that clients or wallets should need to think about. You should just broadcast your transaction and it just works. The P2P layer understands how to relay transactions. That’s my design philosophy for this. The whole thing is wallets shouldn’t need to care about all this stuff.

Shouldn’t they need to care in the case of when they are doing a child-pays-for-parent in a very specific way? Is the broadcast RPC API going to allow you to broadcast your zero sat commitment transaction if you are doing Lightning and the follow-up child-pays-for-parent fee paying transaction?

There’s that. The wallet shouldn’t be telling the node what to relay on the P2P network.

Not that but you can broadcast multiple transactions at the same time.

Yes of course. There would be a client interface where you submit multiple transactions together and let your mempool handle that.

Couldn’t you make the argument that if your node knows the other node is not going to accept this by the old RBF rules they can just say “You need to use the package thing”. I don’t know if that would make sense. There’s no hack really so let’s fix it.

Just fix it.

## Zero satoshi outputs in packages

For my spacechain proposal one of the things I would like to see is the possibility of spending zero satoshi outputs. It looks like maybe with package relay there might be a possibility to do that. The problem with zero satoshi outputs is you need to abide by the dust limit. If you don’t abide by the dust limit then you might create an output that is uneconomical to spend. We want to guarantee that zero satoshi outputs by the relay rules are not accepted. But if you have a package then you can construct it in such a way that you can guarantee that the zero satoshi output is being spent within the same package. You could argue that it is ugly because of this, it is essentially a hack to use an output as an anchor to do child-pays-for-parent. My thinking is if you create a transaction that has zero satoshi outputs and that transaction itself has either a fee that is zero or a fee that is at least lower than the child that is paying for it then if you send that out as a package it will never be the case that the child gets evicted and the parent stays in the mempool. That is what you don’t want. You don’t want the child to be evicted and the zero satoshi output still being in the mempool. If the fee rate of the child is higher then I think you guarantee that either they both get evicted or neither get evicted.

I am wondering why zero satoshi outputs? Why not just a normal output? Essentially you are trying to create artificial relationships between transactions? I don’t think that zero fee outputs is the best way to achieve that. You can do what exists now where you spend a normal amount output.

The issue that I have here is that the person who is creating the output with the dust limit is not the person that is going to get that money. I have this transaction structure where one person has to create a tonne of these outputs ahead of time and they are never going to be able to reclaim that money. If they can create satoshi outputs it means it doesn’t cost them anything. I would have to go into more detail to explain why that is the case but it is spacechain design where one person pre-signs a bunch of transactions with a bunch of ideally zero satoshi outputs. If instead they have to create dust limit outputs, it is one transaction per block. You have to create years worth of these transactions. It ends up being hundreds of thousands of dollars just in order to create these outputs. That is what I am trying to avoid here. I do agree that it is like an anchor for trying to bump the fee of a specific transaction. It is a bit of a hack, I would agree with you there. But it does seem to fit very neatly within the package relay structure at the very least.

I think that if it costs someone nothing to create all of these outputs then it also costs an attacker nothing to create all of these outputs. I would argue that if someone wants to take up block space and ask the network to relay their transactions they should be paying.

I agree with that. What I am saying is that the child will have to pay for it. The network should not relay it unless there is a child that is spending a zero satoshi output and paying for its fees. You no longer have this issue, the whole reason for the dust limit is to pay for when it gets spent. If you spend it as a package then you don’t have that issue. The child has to pay for it.

It is still imposing a cost on the network right? It has to propagate this output with no fee? It is imposing a cost on the network even if it isn’t getting into people’s mempools.

Any amount of data that enters the blockchain is a cost for people.

It is only being paid for if that child comes. If that child doesn’t come then it hasn’t been paid for.

If the child doesn’t come it doesn’t enter into the mempool, it doesn’t enter into a block. It is a zero satoshi transaction with a zero satoshi per vbyte fee rate and it has a zero satoshi output. This will never enter the mempool, this will never enter a blockchain unless some miner for some reason mines it. They can always do that but it is not going to be relayed. The only way you can get this transaction to enter the Bitcoin blockchain is to create a child that spends from the zero satoshi output, you send it as a package, the package as a whole needs to be accepted according to all the rules we’ve just discussed.

I don’t understand why it isn’t just one transaction. You are creating a dummy output that you are going to spend immediately, why don’t you just make it one transaction?

We are going to have to go into the whole spacechain design to explain it properly. There is one person who ahead of time creates a bunch of these transactions, that person is then out of the game. You are not supposed to cooperate with them anymore. The person who creates the initial transaction with the zero satoshi output is different to the person who is going to bump it. They are not going to be able to communicate with each other or cooperate with each other. It is supposed to be non-interactive.

I think the reason we want a dust limit is to prevent UTXO bloat. That’s why we have the standardness rule. There is absolutely no way that you can guarantee that that child will be created. You said it would only be included in a block if the child is there. We have no control over that. The miner chooses the transactions. As a node operator with a mempool I personally don’t want to be relaying transactions that create zero satoshi outputs. I don’t want to contribute to bloating the UTXO set. You can’t get around that rule, the miner chooses, the miner has discretion over what transactions go into the block.

I fully agree with that. The point here is that you are not creating a zero satoshi output, you are spending it right away in the same block. Otherwise the miner should not accept it.

You are not enforcing that.

The miner can always choose to ignore any rules. A miner can always create a zero satoshi output if it wants.

Of course it can. The point I’m making is I don’t want to relay those transactions to miners. That’s my choice as a node operator, I choose to enforce the standardness rules. When you are talking about packages all you are talking about is what goes into the mempool. There is no control over what the miners eventually choose to include in a block.

The miner will only receive it as a package. There wouldn’t be a scenario where the miner received that transaction with a zero satoshi output. You wouldn’t consider it if it wasn’t a package.

I think a lot of people who develop applications on top of Bitcoin have this misconception about the P2P network. My application will force the P2P thing to do this. It doesn’t work that way.

The bytes of that second transaction could get dropped. There is no guarantee that both transactions reach the miner. The first transaction could reach the miner and the second one not.

What you are looking for is a consensus enforced rule where the child transaction must be mined with the parent transaction.

No it is what I am specifically trying to avoid. You make it in such a way so that it is never economical to mine the parent without the child. That doesn’t mean it cannot be mined, a miner can do anything. The goal that I am trying to reach is that it is always a fee rate to consider the parent with the child as opposed to just the parent.

You are not listening to what people are saying. There is one point where yes it is highly likely that both transactions will reach the miner but there is the possibility where the second transaction gets dropped in which case there will be a zero fee output that is sent across the network and reached the miner which is what we want to avoid. The second point is yes a miner can create a zero fee output but we don’t want to be relaying that across the network. If a miner wants to create a transaction and include it in a block they are free to do that. What we don’t want to do is relay something across the network so that a miner considers including it in a block.

You have the child and you have the parent. The parent has the zero satoshi output. If you were to send that over the network to someone else then it should be rejected. Nobody should accept that transaction. But if it comes with a child that spends the zero satoshi output then it should be accepted.

You are assuming that they definitely 100 percent always arrive at exactly the same time. Nothing can guarantee that they arrive at exactly the same time. One transaction could be received milliseconds after the first one.

You are waiting for the entire package.

From what I understand your application wishes to be able to create zero satoshi outputs. That is a rule that our policy does not relay. You are saying that our policy should create an exception to this rule in packages to allow your application to be able to create and spend zero satoshi outputs. You are saying this is reasonable because in incentive compatible cases the zero satoshi output will never appear in the UTXO set.

If I am wrong about that then I agree this should not happen to clarify.

I understand what you are saying could be reasonable. But I don’t think I would ever want to create the possibility of relaying transactions that could add zero satoshi outputs to the UTXO set.

If there is a scenario here where a zero satoshi output gets created and gets mined and doesn’t get spent in the same block then I agree we should not do this. My argument is that we can make it such that that will never happen by creating the incentives correctly.

Just because something is incentive incompatible doesn’t mean that it will never happen. The only way to ensure that it will never happen is if you made it a consensus rule.

Now we are talking again about the fact that theoretically miners can mine a zero satoshi output if they wanted because it is not a consensus rule to not do that.

You are asking us to change our policy which I wouldn’t do.

If the policy ended up creating zero satoshi outputs, yes. But I am saying that we can do this in such a way that the policy doesn’t create zero satoshi outputs.

It is incentive incompatible to create zero satoshi outputs. You can’t guarantee.

You are asking the network to take a probabilistic cost at the very least.

Zero satoshi outputs are consensus valid but they are non-standard so all Bitcoin Core nodes on the Bitcoin network will not relay a transaction that creates a zero satoshi output because it is bad practice and bloats the UTXO set. Since it is not a consensus rule it is fine but you are asking us to make that standard and allow relaying transactions that create zero satoshi outputs. You are saying that they are never going to end up in the UTXO set but that is not a consensus rule so it is not guaranteed. Therefore we are not going to remove this policy.

You could have zero satoshi outputs in the UTXO set with or without the policy. The question is do you have more than you otherwise would have?

I’m saying you should relay zero satoshi outputs only if they are relayed in a way that they are immediately being spent. Can you explain why making this change makes it more likely that a zero satoshi output gets created?

Right now if you want to create a zero satoshi output and have it be mined you have to submit it directly to miners. In this scenario you can create it and submit this transaction to any Bitcoin Core node, you attach this child, that makes it incentive compatible to include the child, but that doesn’t mean miners will necessarily include the child. You are increasing the number of ways that someone can introduce a zero satoshi output, it is bad practice. People shouldn’t be using Bitcoin Core this way.

The conversation continued afterwards.

I believe your point (or at least one of them) was that the transactions could still arrive separately so then the parent might arrive first and now there’s a zero satoshi output transaction in the mempool that might get mined. Is that accurate?

Right. Currently it would not get relayed and would not make its way into nodes’ mempools. To ensure that desired behavior is not relaxed in a future package world you need to guarantee that the transactions are received instantaneously and verified together immediately. These guarantees are impossible. Hence you are arguing for a relaxation even though in the ideal cases (with guarantees) it wouldn’t be a relaxation.

In reality there can be a delay between receiving 2 transactions in a package. And it takes time to process/validate both transactions.

So at the very least you are arguing for relaying a zero satoshi output transaction and not discarding it immediately in case the child comes soon after. That is a relaxation from current mempool behavior (and introduces complexity).

The whole idea behind package relay is that you do evaluate the entire package as a whole. For instance you could have a parent that pays zero sats per byte and a parent that pays for itself and the child. If what you said was true then the same issue would apply here. The zero sat per byte transaction could get mined even though it is not economical. But what happens instead is that the package as a whole is evaluated and the entire thing enters the mempool instead of one at a time. Note I am not currently talking about zero satoshi outputs yet.

I think the idea is that even in a future package world every transaction will still pay the minimum relay fee. So a transaction will be relayed and hence can be assessed both individually or as part of a package by a mempool.

“The parent(s) in the package can have zero fees but be paid for by the child”

I don’t think that should be the case then and I see the equivalence you’re making. You’re saying zero fee is fine so zero output should also be fine.

Essentially yes (assuming we can ensure that zero satoshi outputs don’t get mined without being immediately spent).

Should definitely be min relay fee but I don’t know why that is zero.

Note I am still of the opinion that the zero satoshi per byte transaction won’t enter the mempool, it seems we disagree there.

If you are asking the network to relay it it should meet the min relay fee in my opinion.

The idea is that the package as a whole meets the min relay fee.

Seems too relaxed to me.

You’re basically treating the package as a single transaction.

But the transaction could be assessed individually ignoring the package. Otherwise you’re forced to hold onto it waiting for the child to arrive.

If you assess it individually then it simply fails to enter the mempool because the zero satoshi per byte transaction doesn’t meet the relay fee rules.

So you need to guarantee that the child gets there before the parent. Which is impossible.

You’ll just have to wait for the full package to arrive and evaluate that. It is no different than waiting for a full transaction to arrive before you can evaluate it.

Parent arrives, rejected by mempool. Child arrives, mempool requests parent from peers (who might not have it either as they rejected it too).

If the child arrives alone it should just be rejected, it has no parent.

So you have to guarantee they arrive at exactly the same time. Which is impossible.

It is not impossible. It is just a package. Peer A says to Peer B “I have a package for you.” Peer B receives it and when it fully arrives it starts evaluating it.

Otherwise it would be a DoS vector. Sending transactions which have no parents.

Much better to have parent pay min relay fee and potentially make it into the mempool regardless of any package it may be a part of.

Isn’t that how Bitcoin works today without package relay?

We are getting into internet packet reliability now of which I assume neither of us are experts on. I would guess the larger the package the more likely the package doesn’t arrive all in one piece at exactly the same time. 2 transactions would be less reliable than 1. 10 would be even worse.

I’m not an expert but you generally send a hash of what you intend to send so you can know whether the package fully arrived or not.

So the package just gets treated as a very large transaction. And a package of 10 transactions gets treated as a monster transaction.

There are limits of course but essentially yes. And there are also situations where the package does get only half accepted, mainly when the feerate of a parent is higher than the parent and child combined.

We already have limits on the size of the transaction. We are essentially extending those limits by a multiple of whatever the max package size is. Sounds like caching is going to be the biggest challenge here then. We hope that the transaction size limit we currently have is unnecessarily restrictive. Because if it isn’t we’re just about to multiply it by the max package size.

I believe the package cannot be bigger than the maximum transaction size (100kb?).

So your question is if zero fee transactions are fine why not zero outputs too. We are already relaxing the min relay fee requirement when in a package, why not also the non-zero output requirement (when in a package)? You’re getting the relay of the transaction for free, why not the relay of an extra zero output?

There are a few differences that do matter. I actually came up with a scenario that could be problematic which kills my own idea. Parent P1 (0 sats per byte) has 2 outputs, one is zero satoshis. Child C1 spends the zero satoshi output for a combined fee rate of 1 satoshi per vbyte and they enter the mempool as a package. Child C2 spends the other output of P1 with a really high feerate and enters the mempool. Fees rise and child C1 falls out of the mempool leaving the zero satoshi output unspent.

Let’s say P1 and C1 have a combined feerate of 5 satoshis per vbyte and enter the mempool first. Then later C2 enters the mempool. Fees rise to 20 satoshis per vbyte and C1 leaves the mempool. Now P1 and C2 get mined and the zero satoshi output remains unspent. You could maybe come up with complicated rules to prevent this but superficially it seems like it’ll get too complicated.

This enlarges the UTXO set permanently? Standard argument against dust.

Yeah. Under no circumstances do we want the the zero satoshi output to get mined without being spent. You could come up with a soft fork for that but at that point there are probably better things you can do instead (e.g. the soft fork could be that the zero satoshi output is only spendable in the same block, otherwise it becomes unspendable and doesn’t enter the UTXO set).

So I guess this shouldn’t be done but for different reasons than discussed before? Though in similar ball park. It sneaks into a block in this edge case.

Right, seems like it. Unless there is a straightforward fix for the problem I just outlined I don’t think it should be done.

