---
title: 'BIP: OP_SECURETHEBAG'
transcript_by: Bryan Bishop
tags:
  - research
  - op_checktemplateverify
speakers:
  - Jeremy Rubin
date: 2019-09-11
media: https://www.youtube.com/watch?v=YxsjdIl0034&t=2453s
---
<https://twitter.com/kanzure/status/1171750965478854656>

## Introduction

Thank you for the introduction. Today I am going to talk to you about OP\_SECURETHEBAG. It's research that I have been working on for the last couple years. I think it's very exciting and hopefully it will have a big compact. I have a lot of slides.

## Why are we here?

We are here for scaling bitcoin. The goal we have is to scale bitcoin. What is scaling, though? We have talks on networking, privacy, talks on all sorts of different things but they are all trying to relate to something fundamental, which is increasing transaction throughput. That is the most important goal in my opinion. If it's not serving that goal, then it doesn't relate to scaling bitcoin. What about privacy, what about more private transactions per second? It all relates back to transaction throughput.

## Scaling tradeoffs

Scaling has many tradeoffs with latency, cost, layerization complexity, censorship resistance, privacy, redundancy, you're probably going to have to give something up.

## Acceptable tradeoffs

What are the acceptable tradeoffs? Block size increases. Everyone loves them, right. The advantages is that you can get more transactions, it's simple, done, you get it. But there's a lot of disadvantages, like centralization pressure, bandwidth requirement increases, and also it's a hard-fork and now you need to get everyone to agree. Block size increases, maybe not.

Lightning network is great, you get some low latency, less on-chain storage, more transactions. The disadvantages are that you have interactivity, high collaterialization requirements, and there's fees, and it's not particularly reorg safe. It might be dangerous depending on reorg conditions.

Is there something that we can get that gets all the advantages and is completely free of tradeoffs?

## Intuition building

Let's build some intuition on how that might be possible. Normally, you are free to spend a UTXO in any way. You can spend in any way you want. In a committed UTXO, you can only spend it one way. That one way is determined by what the script is. If you want to spend it some other way, it's invalid. This is a little bit of an analogy to a certified cheque. You go to the bank, the cheque says who is going to get the money, and that's it they get the money. It's not like a normal cheque where it can bounce. You know how it is going to be resolved, in the same way that you know how a UTXO will be resolved when you spend it.

## Batching

Batching is old-news tech but it is just now getting deployed inside exchanges. The idea has been around for a while. You have a set of payments that you're going to make, but you're going to do a bunch of transactions and they are all yours so why not add them all up? It will save you signatures and change and fees, it's generally a good idea if you're doing a high volume of transactions.

## Intuition building: two phase payments

What if you make a batch payment, and then instead of directly creating all the outputs, we add one intermediate committed outputs. It says, in the next step, we will create all the outputs. What this does is it allows us to put these transactions in different blocks. When block space gets cheaper, you do the work later and reveal.

This is what the basis for OP\_SECURETHEBAG is.

## Multi phase payments

Let's say this is 10 MB of outputs. You can't do that inside a single block right now. So you can take it and put it into a list. Instead of pop and expand, it's done in two phases, and this gives you an idea on the amount of bandwidth in a block. It competes less in the fee market. It kind of sucks to be at the end of this list, though. Say you have 30 hops along this list, you have to wait for everyone else to clear before you can get your payment out.

## Tree payments

What if instead of doing a list, we do a tree. This is a flexible operation. Essentially you only have to do log(n) work to get your payment out, which is usually pretty small for whatever number of transactions you're doing.

## Receiving tree payments

Okay, so someone pays you, and they say here's a single output and you're going to be able to get a transaction out of it at some point. So we have a tree here, and you're going to receive a payment in that tree, and the only information you care about as a receiver is this log(n) inclusion path in this tree. You only care about you getting yours; you're able to prune out the information. As long as you retain this path, you're able to get your money.

What's cool about how this works is that it's not n log(n). When the next person comes along, it's amortized for them. You get to save the work you've done collaboratively. If you sum up the layers of the trees, you get... and so on and so forth. What this means is that the overall work is going to be just 2n transactions compared to having 2n outputs. The total amount of extra stuff is not that much.

There's a neat property when you use this a certain way. The information on those nodes is deterministic. In the original batch, we took it and deterministically transformed it into this tree. From the leaf nodes of the tree, we can recompute what that would be. If you're running a pruned node, you can erase the extra information as soon as you learn one of the expansion steps. The actual storage requirements are relatively low.

## Four options

There are four options on what's availbel today: you can have covenants with OP\_COV, you have pubkey recovery, and pre-signed transactions and OP\_SECURETHEBAG.

## OP\_COV

OP\_COV is some pattern-matching based covenant where it interprets the output you're creating. This is really powerful and therefore bad because you can create malicious covenants that can infect everything. It's just been out for a number of years and nobody has made a serious effort to get it into bitcoin.

## Pre-signed transaction multisig

This one actually works, but if you have 100k people in this tree, then you need to do multiparty ECDSA with 100,000 people and there will be denial of service issues when someone goes offline which will happen. Another issue is that you can't prove or guarantee to a third-party. You can't prove to a receiving party. Also, you can't evne prove to yourself, you have to delete the key after you sign with it and be non-circumventible, but maybe someone leaked it out of your memory. The last category is pubkey recovery like CHECKSIGFROMSTACK and ANYPREVOUT/NOINPUT but I don't think it's the way to go forward. The issue is that fundamentally that keys should be keys and signatures should be signatures. As soon as they are meaning some other thing, I think it's an abstraction violation, and it doesn't even work when you start hashing the pubkey into the message which is generally considered best practice for digital signature algorithms

## OP\_SECURETHEBAG

OP\_SECURETHEBAG is a multi-byte opcode. It takes its argument from itself rather than from the stack. In OP\_SECURETHEBAG, you include a hash which commits to all the details inside a transaction that will be used except for the COutPoints. You commit to everything else. If you know a particular COutPoint and you know it's OP\_SECURETHEBAG of some hash, then you can fill in exactly what transaction will occur and what the txid will be for tha ttransaction.

This structure means that you can't pass any information into this, and this eliminates any possibility of recursion. You can prove that you're using the fuel or doing a destructuring argument for the proof and no recursion is possible.

There's no extension to bitcoin that will come later tha twasn't going to enable recursion; that plus this will enable recurison--- which is not true for some of the pubkey recovery options like I mentioned before.

Multiple inputs are allowed, but it's not recommended.

It could be deployed inside of taproot's tapscript.

## Implementation process

There's a draft BIP, with experimental code out there. There's experimental Bitcoin Core wallet support in progress. Minor BIP options are in flux like pushless multibyte opcode versus alternatives.

## Impact

Is this going to be better? Big warning, this is simulated results. If you go read my simulator, it might convince you that OP\_SECURETHEBAG is going to have a pretty big impact on how we use the blockchain.

This is the master graph and it shows you why OP\_SECURETHEBAG is so great. What's going on is that I did a simulation with 50% adoption meaning 50% of all transactions are going into OP\_SECURETHEBAG tree. What I did was, I did two spikes in volume. So this is the average transaction volume that is the max that can be confirmed. If you're doing transactions at this rate, you will have constantly full rates assuming they are all accepted. After this other point, this mempool is never going to clear out when we get that second spike.

Having run the simulation, what are the results. What we see instead is that, bear in mind this is powers of 2 on the vertical and powers of 10 on the horizontal. We see the mempool is 10x smaller when using OP\_SECURETHEBAG. We also see this red line represents the things we have now backlogged using OP\_SECURETHEBAG. They are fully confirmed and committed to, but you don't have an output you can directly spend from. It takes some time to clear those out when the spike goes down. We can see the mempool is basically empty for this entire period. Our mempool clears out significantly faster than without OP\_SECURETHEBAG. Before, OP\_SECURETHEBAG the mempool would never go back down because the mempool is saturated and things are added at least as fast as we can confirm transactions. You only have to do log(n) transactions, which are guessable once you know the leaf nodes. The extra fee required to prioritize pulling out one of those coins is basically constant because of that.

I also did another adoption simulation. Even if only one business adopts OP\_SECURETHEBAG, then they will have a massive benefit. Many tefchnologies need a lot of adoption in order to make an impact. But actually, this has a big impact for everyone regardless of how many people adopt it.

## Summary: OP\_SECURETHEBAG is like a transaction bypass capacitor

OP\_SECURETHEBAG smooths out the transaction backlog. You'll be able to get confirmations earlier, but spending will be more delayed. It soaks up excess transactions, and releases them later like a sponge. The private benefit is large even with small adoption. The private use will benefit the entire public. There's also reorg safety, by default doing lots of withdrawals is not reorg safe unless you're clever. With OP\_SECURETHEBAG, if it gets reorged out, you get a really big win-- it's secured by the anchor of when the original OP\_SECURETHEBAG payment was made. It's locking the coins to be spent in the way you specified. OP\_SECURETHEBAG helps you not get double spent.

## What's the catch?

I made a claim that there's no tradeoff. Let me present one more piece of information to prove that there's no tradeoff if you accept an assumption. Normally, multi-radix congestion controlled transactions... you can expand on a transaction and its children all at once, or you can do a binary tree. The claim that is probably true is that, given there's O(1) overhead in amortized work per input, and O(n) overall work, and without OP\_SECURETHEBAG the batch thing is O(n) also. In the worst case, we're not doing asymptotic work or something, this isn't like n^2 thing. Worst case, it's O(n) more work. The idea is that you can defer and wait for asymptotically chaeaper blockspace then it's going to be a constant amount more expensive. Smaller size verification of interiro node transactions compared to normal transactions (no signatures). The interior nodes are prunable, and they have some sort of optimal tree structure not just leaf nodes all at the end. You can apply some of these htings recursively across the tree. I think the expected overhead is just constant. If you're doing a transaction with more than a few outputs, it's always better to use OP\_SECURETHEBAG especially if you're a business and reliability is a concerned.

## Advanced topics in OP\_SECURETHEBAG

If you're doing inter-business traffic, where businesses are doing managed cashflow, they can manage the money and pay their other obligations. This makes liquidity between busisnesses is really quick.

Instead of doing payments, you can open up channels. This is called ball lightning. You can create as many channels as you wnat, and they can be connected in whatever topology you want.

You can unroll looped programs into finite steps with OP\_SECURETHEBAG. You can compile this into a finite form where you have a run limit such as a million years, and then you can compile this into a set of transactions using OP\_SECURETHEBAG to enforce the transitions between steps without requiring pre-signed transactions.

Smart vaults: you can have a program that moves at a certain pace, and it can move a cold coin to hot storage, and once in hot storage you can send it to cold storage or after some timelock you can spend it to a customer. This is a failsafe design and all of the components are isolated from each other.

You can have non-interactive channels.

You can have coordination free decentralized mining pool payouts.

## Summary

OP\_SECURETHEBAG is great and it's the best thing ever. I'm going to skip about deployment. We could wait to deploy this, fees are low right now, but that's kind of like waiting to go to the doctor until you get cancer. Also, things are slow in bitcoin and if ew want this to happen then we need to think about it now. This is going to make hte long-term prospects of the fee market healthier.

## Options

This could be a tapscript extension, but since taproot is going to take a long time then maybe make it a custom opcode and deploy it sooner.

## Next steps

I could use help like sponsoring me as a researcher, or help review the BIP, or work on the implementation, or integrate OP\_SECURETHEBAG on the product, chime in on the bitcoin-dev mailing list, or tweet about it and ask questions.

<https://docs.google.com/presentation/d/1r-pUj-k-K7IQuufSUepVmjDFOZUKeUBB338ribwECk0/edit#slide=id.g5986436661_0_0>

