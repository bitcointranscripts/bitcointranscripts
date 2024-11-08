---
title: CoinjoinXT and other techniques for deniable transfers
transcript_by: Bryan Bishop
tags:
  - privacy-enhancements
  - coinjoin
speakers:
  - Adam Gibson
date: 2018-07-03
media: https://www.youtube.com/watch?v=YS0MksuMl9k
---
<https://twitter.com/kanzure/status/1014197088979226625>

<https://joinmarket.me/blog/blog/coinjoinxt/>

## Introduction

My talk today is about what I'm calling CoinjoinXT which is kind of a new proposal. I wouldn't say it's a new technology, but perhaps a new combination of technologies. My name is Adam Gibson. Yes, another Adam, sorry about that. I have been working on privacy tech for the last number of years, mostly on joinmarket. Today's talk is not about joinmarket, but it is about coinjoin.

I want to first talk about fungibility in bitcoin. It's a huge topic. Then I will introduce a topic called CoinJoinXT, which yes is sort of a joke name, and then we can talk about CoinJoin Unlimited, which is another joke. That idea is an extension of CoinjoinXT. It's kind of interesting to look at the extension. There is a blog post about this talk.

<https://joinmarket.me/blog/blog/coinjoinxt>

## Motivation

There is a general perspective that bitcoin is perfectly traceable. The entire history of a coin is not entirely traceable but people think it's traceable. There is an intrinsic fungibility of bitcoin. Note that I am not saying perfect fungibility. It's a different thing. Imagine gold jewlery-- if you have several pieces of gold jewlery, it's melted down, and it's a bunch of gold atoms, and they are all the same and perfectly fungible, but then when you recast that gold into new pieces of jewelery, then you can't tell which output or which piece of gold jwleery ocorresponds to which original piece.

In bitcoin transactions, if you have multiple inputs and outputs, you can't say that bitcoins from output one corresponds to bitcoins in output two. It's not just difficulty of calculation, it's simply that no such correlation exists.

## Coinjoin

I want to straight away talk about coinjoin and how it's used today. This is an example of how coinjoin is used today-- it's an example of a joinmarket coinjoin transaction. If you have good eyesight, you will be able to see that there are several exactly-equal sized outputs. The idea of coinjoin as it's been used so far, or in earlier wallets like dark and so on... the idea was to use same-size outputs so that it's not possible to distinguish any of the exactly-equal sized outputs at least at the level of the transaction. There's no analysis you can do on the transaction to distinguish those outputs because they are exactly the same amount. That's how we use coinjoin today.

What I want to do in this talk is to distinguish between that approach to using what fungibility exists in bitcoin and amplifying it with that method... and distinguishing that with deniability, which means... here, what we have is a fixed pattern where it's easy to identify that these transactions are of a certain type, there's been work by guys at Princeton in blocksci to write an algorithm to identify coinjoin transactions on the blockchain.

Instead, what about deniability? I want to explain how this works, and to do that, I want to talk about blockchain analysis first.

## Blockchain analysis

I'm not really sure if blockchain analysis started with the merklejohn paper in 2013. It was called like, a fist full of bitcoins, and it was an interesting paper to read. They set the foundation for how can you look at the blockchain and try to make correlations between UTXOs or outputs on the blockchain. They came up with some heuristics which were probabilistic assumptions. I'll use the word heuristic though.

If there are multiple inputs in a transaction, then they are all owned by the same party. This  assumption is violated in a coinjoin transaction.

Their second heuristic was kind of vague that, maybe we can identify the change addresses according to a certain rule. I am not going to talk about this one.

Most of blockchain analysis today is based on that idea, they build clusters based on the idea that whenever two UTXOs are used as inputs to the same transaction then they should be considered co-owned and you should be able to grow large clusters by applying that rule. This is based on things like walletexplorer.com and you can see wallet clusters in public, and certainly blockchain analysis companies exist. They seem to be successful businesses and they seem to make money not just through wallet clustering but also other data as well.

I want to add some other heuristics or assumptions that Idon't think people think about and they should.

Heuristic 0 is that each UTXo is unilaterally controlled. You assume that it's owned by one party. Even back in the day, it actually could have been owned by multiple parties using Shamir's secret sharing. There's also recently the possibility of ECDSA two-party pubkey approaches. That's an assumption even if it's a natural one. The heuristic 3 here, this is the weird one: when we identify two parties, we assume that, when the coin is transferred from one party to the other then we assume that's a payment. If Alice pays Bob, tautologically, Alice pays Bob. But there's something wrong in there.

I am going to break all of these heuristics where none of them are valid. That's the goal at least.

## CoinjoinXT

The idea is that you sign the last transaction first. Segwit is the foundation of this technique. We have transaction id malleability fixed. We can prepare a transaction, such as a funding transaction, and then we can instead of signing it or broadcasting it, we can gets its txid and use that to construct refunds, locktimes, or proposed transaction graphs (PTGs). We can prepare all of these sets of transactions and not broadcast them. We need to both have some control over transactions in the set. We only sign the funding transaction at the end, making the whole thing atomic. The entire set of transactions will only occur if we both agree, or you can do things like "if at least one of us wants them to go through then they will all go through".

We can create transactions using the proposed transaction graph, but make payments out individually to Alice or Bob and thus violate heuristic 3. An individual transaction might pay coins to Alice but it may not be a payment. This is something that can contribute to deniability.

This construction is limited because it all starts with a single transaction up here. It could be a tree, rather than a chain, but it's still got one unique entrypoint on to the blockchain. If we're trying to make life more difficult for blockchain analysis, then that's a limited model.

## Promise UTXOs and unilaterally-controlled coins to improve the proposed transaction graph

We can extend this model where we add a promise. This is a promise UTXO here. The idea is that instead of only having one entrypoint into the graph of transactions here (which are co-controlled and pre-signed by the two parties), we can have other entry points, where Alice adds another UTXO from her own wallet, of whatever size, and we call that a promise UTXO. In a sense, it breaks the atomicity of the structure. If Alice and Bob agree to broadcast the transaction and Alice double spends A1 before we reach tx3 then it may not go through... so we've broken the atomicity if we allow unilaterally-controlled UTXOs to enter into the graph at some point in the middle. We need to use a refund transaction with a timelock before that transaction goes through. It's a tradeoff. By adding these promise UTXOs, you're able to add many origins to the graph.

We can make these graphs in any structure we like. So we have two different promise UTXOs here, and there's a huge design space we could be exploring here. There are some dual-control UTXOs. Every time there's a promise, there has to be a backout transaction that is timelocked on the previous transaction.

Other features to bear in mind-- we have been looking at Alice and Bob but this works just as well for n-of-m and 2-of-2.

The other thing to observe is that I gave Alice some equal-sized outputs. There's another kind of variable in the design space here, if you choose to use equal-sized outputs, you get that intrinsic fungibility but you lose deniability a little bit because you can no longer pretend this isn't mixing activity going on. It's possible for equal-sized outputs to not be coinjoined, but people might say generally they are.

The other thing I will mention before I move on, what about practicality of this? I want you to understand that while it looks complex, it's actually not more interactive than simple coinjoin. The interaction between the two parties is simple-- they are just sending keys and so on, but they are only agreeing upfront on the template of the graph. It doesn't require more interactivity. Coinjoin is interactive, but not cross-block interactive where you wait for confirmations. So, that's still true here, even though it might seem more complex.

These dual-control UTXOs, like 2-of-2 multisig between Alice and Bob on some of those coins... At the moment, if we use those, it's a negative for deniability in that they are identifiable as that particular kind of pay-to-witness scripthash or 2-of-2 multisig or whatever... But we're aware that we hope, we hope that there's a Schnorr multisig option that might hide n-of-m keys into 1-of-1 key with the same anonymity set. And there's also ECDSA multisig stuff  that some guys have gone into recently.

There's quite significant problems with using this approach if your intention is "deniability". If you want to make structure of transactions that don't look like coinjoins but are coinjoins, then you might still suffer from amount correlation. In one of the early versions of joinmarket, you could work out a set of inputs corresponding to a certain set of the outputs, due to the way that the output amounts were determined. If we avoid using equal sized outputs, then Alice's outputs added up are going to add up to Alice's inputs. This is not payment- it's her mixing coins with Bob in theory. It doesn't work well if you can do subset sum analysis and look at the sums to find out who owns what. If you look at subset sum, theoretically it's exponential time, but in the weeds, subset sum is practically realistic in general. Maybe it would be difficult in this case because the boundaries aren't clear to the attacker so maybe the blockchain analyst is bad at finding the correct set of transactions but maybe he's able to find that correct subgraph of the blockchain with subset sum analysis.

## Coinjoin Unlimited

You can tweak this and use lightning to make subset sum analysis not work. We still have a set of transactions we negotiate upfront. And then we sign the funding transaction. Well, Alice has 2 inputs, Bob has 2 inputs, they each got 1 output, and there's a third output, which is a dual-funded lightning channel. The usual thing would be to look at sets of inputs and try to add them up, ... but I've marked in blue is that... these ... they are trying to figure out if this input or whatever belongs to Alice or Bob, and he has to figure out the lightning funding transaction as well... He wouldn't initially know that it's lightning, but maybe after it's closed he would. He doesn't actually know the initial channel balance between the two parties. So he can't make a subset that corresponds to any of the inputs elsewhere. Subset sum analysis doesn't work in this situation. Once the lightning channel closes, then these two numbers are exposed on to the blockchain with the closing balances. If the closing balances are the same as the starting balances and you never used the lightning channel, then subset sum analysis can work again, and the transaction analyst can do their analysis with the blockchain again and find the subgraph. But the whole point of lightning network is that you can make payments to other parties. If you leave the channel open for a while and use it, then your balances can significantly change, and then it would be such that there's never any case where subset sum can work. This is a way of trying to get the lightning network's inherit privacy by HTLC paths and so on, to get that to bleed back int othe main chain.

This has limitations, obviously, like the amount of bitcoin you can send on lightning channels. If you look at the inputs and find the amounts are amount much larger than lightning can handle, then you are asymptotically falling back into the coinjoin analysis model. For large amounts of money, lightning is a dubious security model, so maybe we can use equal-sized intrinsic fungibility coinjoins. Moving between large and small, maybe CoinjoinXT with lightning could be interesting. There's a large design space here.

gpg: 4668 9728 A9F6 4B39 1FA8 71B7 B3AE 09F1 E9A3 197A

## Q&A

Q: Does this work with replace-by-fee?

A: You can pre-sign as many transactions as you want, including fee bumping transactions.

Q: What about submarine swaps?

A: I haven't considered that.

Q: Can you use SIGHASH\_NOINPUT?

A: How does that work?

Q: Presumably Alice can name a different UTXO in the future.

A: How do you deal with malicious counterparties? Here the malicious counterparty basically wastes Bob's time or annoys him.

He has to use a refund... but, making it easier so that you can use different coins in your promise, maybe.

Q: What about releasing a private key? Or what about timezone differences for each transaction in the chain?

A: That's kind of orthogonal,... the difficult thing about coinjoin is coordination and getting everyone together to do this whole thing.
