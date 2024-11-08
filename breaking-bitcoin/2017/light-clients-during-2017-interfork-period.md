---
title: Light Clients During 2017 Interfork Period
transcript_by: Bryan Bishop
tags:
  - lightweight-client
  - segwit
  - soft-fork-activation
speakers:
  - Thomas Voegtlin
date: 2017-09-09
media: https://www.youtube.com/watch?v=eCE2OzKIab8&t=5h9m
---
<https://twitter.com/kanzure/status/1005617123287289857>

Next up is Thomas.

## Introduction

Alright. Hello everyone. Thank you for having me. I'm the developer of the Electrum wallet. I started this project in 2011. I'm going to talk about lite clients and the implication of the 2017 hard-fork. We might be in the middle of two forks at the moment.

So we have segwit and we are very happy about that. ((applause)) This graph was taken from Pieter Wuille's website. It has lasted almost a year and during that year we didn't know whether we would get segwit eventually. There was this phased transition where miners started signaling for segwit just before the UASF deadline. I still don't really understand what happened but I'm trying to investigate that and explain what I do understand.

So where are we now? Are we in the middle of two forks (segwit2x)? Why did miners activate? What are they running currently? I haven't checked recently of the number of miners that are signaling for segwit2x. I think it's pretty high. Will there be a hard-fork in November? That's the question.

## What is bitcoin

When you talk about forks, there's also the question of what is bitcoin. That is the existential question. Is it the chain with the most proof-of-work no matter what? For some people the answer is yes. This is an answer from Gavin Andresen. He said that if bcash has more hashrate then it would be bitcoin to him. I guess consensus rules go out first, in the code, for the bitcoin client. But not for everybody. If we want to change consensus rules then we have to decide what we define as bitcoin.

This way of thinking, of deciding that bitcoin is the chain that has the most hashrate reminds me of this other question: what gives value to bitcoin? Does bitcoin have value because it is difficult to mine? Or does the market value of bitcoin drive the hashrate and the difficulty? For me, it's the second one. I guess that's the case for most developers. If you ask this question to a miner, then they might have a different perspective, because a miner will spend money to mint bitcoin and then they will sell it- and they don't want to sell at a loss. This perspective is different for miners, in other words.

This difference of perspective is interesting to understand the motivation behind hard-forks and the decision about what is bitcoin and which chain is bitcoin.

## Hard-forks and soft-forks

Hashrate matters during a hard-fork. There's a distinction between soft-fork and hard-forks. A soft-fork is a fork where the consensus rules become more strict. A hard-fork is-- it's not correct to say that the consensus rules are relaxed. Rather, a hard-fork is a fork that is not soft, in the sense that if you do a hard-fork then you may do a strict relaxing of the rules and in that case your hard-fork is reversible like BU bit you can change the rules so much that some are relaxed but others aren't, which is also a hard-fork.

In the case of a soft-fork, if the miners following the soft-fork... a majority of hashrate.. then the other branches of France.. then that's why it is safe to do a soft-fork. But it could also happen without a majority of hashrate, the two branches will exist if the miners that follow the fork do no thave 51% percent. This was the idea of the UASF proposal: initiate a fork regardless of the hashing power just by users and then see how much following comes from the miners. So that's why soft-forks are easier. In a hard-fork, unless it's reversible, you will end up with two chains. If the forking chain has a very strong majority, then it can allocate a portion of its hashrate to undo the blocks of the smaller chain. This was the threat agitated by some miners a few months ago.

## Relationship between hashrate and price

The other thing that is important is feedback through market price. The price creates the hashrate. This is my opinion. But not enough hashrate, can also kill the price. If the branch that forks sees one block per day then there's no market and if there's no market then no miners are going to follow on that branch. This could happen with segwit2x. So the normal regime is tha tthe price creates the hashrate, but the fact that the hashrate can kill the price is not a normal situation, it's more like a boundary condition.

## Segwit UASF activation

Why did segwit activate? Did UASF work as a deterrent? Or was it just segwit2x that worked and are we in segwit2x? How does deterrence work in that case? This is the idea that the losing branch of a soft-fork are going to be... so if you're mining on a branch that is under risk of being orphaned, then you might lose everything in the end even though you are successfully mining blocks. As a miner, you have to wait 100 blocks in order to have maturations of the coins that you have mined. So this threat of getting your funds is actually a strong deterrent for miners unless of course the soft-fork has a very very small minority of the hashrate.

## Replay protection

Then there's replay protection. BCH implemented that with a new sighash type. In segwit2x, there will not be replay protection. The difference is that with BCH, I'll just quote.... but most of the people in BCH did not see bitcoin as the main bitcoin, they just wanted to try a new proposal. But if you are forking because you believe your coin is the true bitcoin, then you have no reason to implement replay protection. It's a game of chicken. You should not expect replay protection in a hard-fork proposal motivated by the belief that it will be the true version of bitcoin.

## Light clients

Light clients do not see full blocks. They just get the blockheaders. They can filter the blocks using a bloom filter. They can also get a list of the transactions from electrum servers. These are two different ways of performing SPV. When you get this information, you can download the merkle proof of your transaction and you can check that your transactions are in the blockchain.

Because light clients cannot see the full blocks, they cannot verify the consensus rules. They cannot detect violations of consensus rules. They might try to infer the size of the blocks from the size of the merkle branches- which was proposed by luke-jr some time ago I think. In general, this is not reliable. The blocks in BCH are in general are one megabyte today.

So light clients are vulnerable in the case of a fork because of that. And also because they tend to follow the longest chain. This exposes the users to a hostile takeover by the miners.

## SPV and forks

They follow the longest chain because it's another thing about SPV--- SPV is not about bloom filters, and SPV does not say you have to follow the longest chain. Following the longest chain is what most implementations do, because it's easy, but if there's a fork then you might want to do things differently.

The full node follows the longest valid chain, because that's the consensus rule, and it includes validation of all the other rules. For an SPV client it might be interesting to validate all the chains that we hear of. And this gets back to the initial question, do we define bitcoin as the longest chain? I spoke recently with a SPV wallet developer that told me "for my wallet, bitcoin will be the longest chain because this is how I believe it should be".

## Fork detection

With electrum we did it differently. In order to prepare for the UASF, we implemented fork detection. We cannot detect violations of consensus rules. At least not in the general case. We could try to infer the size of the block from the merkle branches, but this is not a generic mechanism, and it would be useful maybe only once if ever. We can do better.

We can detect consensus failure or the fact that the electrum servers which are bitcoin nodes are not on the same blockchain. So what we do is we download and validate multiple chains and this new feature of electrum was out in version 2.9. So instead of a chain of blockheaders, we have a tree of blockheaders, and we validate the chains that we hear about and are validating the bitcoin rules, and we check the difficulty on all of them.

## UASF

This fork detection has been implemented in order to prepare for UASF with the belief that if UASF starts with less than 50% of the hashing rate would result in a chain split. Like I said, I do believe that we have to give users a freedom of choice because feedback through markets is an important component of deterrence that I mentioned. Miners can only be deterred if markets are working properly, and markets will only work properly if bitcoin users have a choice of which chain they are on and where they spend their coins.

With this feedback through the market, miners will allocate hashrate according to how much they get paid by the market. In the end, if the UASF coin is worth more than the other one, then it should have more than 50% of the hashrate, and it's a self-fulfilling prophecy at that point, isn't it?

## Fork detection GUI

The following is how it works in the electrum GUI for fork detection. They get a dialog where you can see if there's a fork. This screenshot was taken shortly after the BCH fork. It shows that some of the nodes are on the main chain and some of the nodes are on the bcash chain. As an SPV client, we do not know which chain is the main one. We have not implemented anything for the user, for the client to actually detect that, because we what we publish is the first letters of the hash of the block where the split occurs and we expect people to check this hash with different sources. We do not have technically another way to know unless of course we trust nodes not to lie, and we don't want to trust nodes. We don't want the electrum clients to trust servers.

## Coin splitting

There's a way that you can split coins if you use electrum in this context. In my way, the best way is to use RBF. You should create a transaction that can be replaced, and you propagate it on both chains. Of course, this has been designed for the case where a user has been exposed to a fork without replay protection. We expect that your transaction will be replayed on both chains, and you should propagate it on both chains. Once this happens, at some point it will be mined on one of the chains. If it's not already mined simultaneously, in most of the cases--- this will not happen- you will burn the fee on the other chain. Once they are both confirmed, they will have different txid vlaues and you will split your coins.

Well, that was the theory. What actually happened?

## What the fork?

Segwit did not split the blockchain. It was activated by the miners at the last minute. And then bcash showed up at the same time. It did it with incompatible headers, which are SPV-friendly, because SPV clients are not going to accept those headers. I showed you a screenshot of electrum following the two chains- this was in the first few blocks after the fork, before the new rules settled in. The bcash headers were still acceptable for the bitcoin validation rules but as soon as they started to have modifications-- as soon as the modification of the difficulty rules in bcash became activated in practice, then .... Sorry? As soon as this EDA was used, this chain was no longer valid for electrum, and the nodes did not connect to that anymore. Bcash was SPV-friendly because SPV clients were protected from it after the EDA set in. It also had replay protection so that users could not spend bitcoin on both chains unless they really wanted to.

The problem was that-- we were communicating about this fork detection thing, and users thought that they would be able to spend on both chains in any kind of fork. But this is not the case. This tool was designed to protect users from a fork that does not have replay protection, e.g. a hostile fork. Since we do not support altcoins, electron cash was born.

## The future is bright

We have segwit. Maybe there will be segwit2x in November. But this time we will be ready. If segwit2x has no replay protection, and it has the same difficulty rules as bitcoin, which is the case at the moment, then this fork detection we have in electrum will be useful.

Okay, thank you.

<https://www.youtube.com/watch?v=eCE2OzKIab8&t=5h28m27s>
