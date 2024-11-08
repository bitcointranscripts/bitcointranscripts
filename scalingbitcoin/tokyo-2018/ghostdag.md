---
title: The GHOSTDAG protocol
transcript_by: Bryan Bishop
tags:
  - research
speakers:
  - Aviv Zohar
media: https://www.youtube.com/watch?v=3Hksieg5GdM&t=1807s
---
paper: <https://eprint.iacr.org/2018/104.pdf>

## Introduction

This is joint work with Yonatan. I am going to talk about a DAG-based protocol to scale on-chain. The reason why I like this protocol is because it's a very simple generalization of the longest-chain protocol that we all know and love. It gives some insight into what the role of proof-of-work is in these protocols. I'll start with an overview of bitcoin protocol because I want to contrast against it.

## Bitcoin's consensus protocol

The behavior of the honest miners is that you mine for tips on the longest chain, and you're supposed to publish your blocks immediately. These are the requirement ofr bitcoin miners. We make some security assumptions of this protocol, which is that most of the hashrate is honest players that are following these rules. There's another assumption that says that block propagation takes much less time than the time that it takes to create or validate blocks. As long as we have these two sasumptions and correct behvaior, then what we can do as validators or as onlookers on the system, we can look at the longest chain, we can take all the transactions on the longest chain and we're guaranteed at high probability that transactions that are located there will not be switched out.

This is basically the main bitcoin protocol. The problem is that block propagation fails at scale. You could either have larger blocks or you could increase the block size, which makes block propagation slower which breaks the inequality. Or you can reduce the time between blocks, making the system faster, which also breaks this inequality. What we're aiming to do here is get rid of the block propagation assumption or weaken it in some way, and we want the rest to kind of remain.

The changes we're going to make to the protocol is that instead of looking at the tips of the longest chain, we're going to use a directed acyclic graph (DAG). It's still mining, still proof-of-work protocol. We still ask miners to publish their blocks as quickly as possible, and we still need a high amount of honest hashrate. Instead of picking the longest chain, it's pick the longest k-cluster. I'll talk about that in a moment.

What we're going to have is a transaction set with high probability does not change. We're going to have the same types of guarantees that bitcoin gives us, that the probability of being double-spent reduces exponentially as you wait for more confirmations.

## What you can get

Security will no longer break at higher throughput if instantiated correctly, but there's really no free lunch in these things. Latency of course, increases. There is a tradeoff that you can't avoid in consensus protocols between throughput and latency. It's very hard to get around it. This is the case here as well. You'll have to wait longer for a confirmation, but that's better than the system completely losing security. We don't solve other consensus problems like how to store the entire blockchain, how to improve validation time, how to bootstrap and sync the entire data structure... you've heard a lot of talks during this workshop on ways to do that, and these can all be combined with ghostdag. We're just looking at the consensus layer here.

## From chain to DAG

I want to talk about the interesting change here, which is moving from chains to directed acyclic graphs (DAGs). You can imagine a classical miner in the bitcoin protocol faced with a blockchain where he looks at all the blocks he's heard of, and he's supposed to mine on top of the longest chain and he has to go and look for which is the best chain to work on. In DAGs, you say don't make a choice, just tell us about all the tips that you know about, of blocks that you have seen that don't have any extension yet. Our goal once we have this DAG data structure is to get an ordering of these blocks. If we have that order, it doesn't change, it remains the same as the DAG grows. Every time we get two conflicting transactions, we check the ordering, and ew always accept the first one and the second one is the one that is rejected or ignored because it's double spending.

## Terminology

I want to establish some basic terminology. With regards to a block x that is somewhere in the DAG, we can talk about all the blocks that x has referenced directly or indirectly as the "past" of x. We can think about these as blocks that have been received by the node that created block x by the time of creation becaus ethe creator includes a hash of the previous blocks. He has had to have seen that information, and these include hashes of predecessor blocks and so on.

The blocks that point to x are actually in its future, and we know they were crfeated after x because they include its hash and had to know its hash and thus that required x to already exist.

This makes up a past cone and a future cone. It's similar to light cones in relativity. You can talk about blocks known to x or blocks that have been influenced by x. The blocks that are neither in the past or the future are in the "anticone" of x. They were blocks created in parallel; we don't know if they came first or later. We have to basically figure out how to order those blocks.

## What do honest blocks look like?

If these two blocks are in the anticone of each other and we can't order them, this only happens if they are created roughly at the same time. You need to remember that the behavior of honest nodes is to point at their latest tips and broadcast their blocks quickly. If they were created at different times, an honest miner would have pointed to that block and included it as an ancestor. They must have been included at roughly the same time and the miners hadn't heard about it. But suppose we had an oracle that told us here are the blocks that were created by honest participants... we would see some blocks that are in each other's anticone that can't be ordered; but only a few of these will happen. There are some other blocks that have maybe very large anticones, we odn't know how to order them and these are actually attacker blocks. If someone told me which blocks are which, which we don't really know. This motivates our definition of a k-cluster, which is the main notion in the protocol.

## k-cluster

A k-cluster is a set of blocks c such that each block looks honest.. each blocks in the set has a small anticone from within the set. They look like a well-behaved set of block and they don't have large anticones with respect to the set itself. I can talk about a 1-cluster because every block in it has at most one block in its anticone within the set. Here's an example of a 2-cluster, and it's 2-cluste rbecause this block has 2 blocks in its anticone within this set. I could not add another block and still keep the property of the 2-block. A 0-cluster is basically a set of blocks with no blocks in their anticone, which is otherwise known as a blockchain or just a chain. You can always parameterize a DAGchain protocol with k=0 and get a longest-chain protocol with a linear blockchain consensus protocol.

## phantom protocol

The first version of the protocol is the phantom protocol. It basically says look at the DAG that you've got, the miners have built it, they have pointed it at some recent tips, they have pointed at some data structures. Instead of taking the longest chain, we'll take the maximal weight k-cluster in the DAG, whichever is largest. Then we do a topological sort on it in some canonical way (past-dependent only) such that every node that sees the same set would get the same order. That's it, we're done.

This set that we choose will contain most of the honest blocks. Almost all of them, if k was set well. It will remain the same, it does not change as the DAG grows. If you're in the k-cluster and you've been ordered in some way, the ordering will not shift. This is exactly what we need for a transaction set to be accepted and remains in consensus.

There's a slight problem with the protocol I've just described: we have this step of finding the maximal k cluster in the DAG, which is a NP hard problem. If you know your computer science, that's not a good idea for a protocol, you'd have to run in exponential time to find the set that is best.

## GHOSTDAG

So our solution is ghostdag (the name is a result of Ethan Heilman because of the movie Ghost Dog). The solution is to use a greedy algorithm to get a large k-cluster. It's not going to be the largest one, but it will be good enough. In the paper, we prove all the properties we've otld you about with respect to that greedy algorithm. In some sense, the k-cluster is a group that is suspected of being the honest nodes. When we look for the largest k-cluster, we do this because we have the assumption that the honest miners are the majority of miners in the network and they would produce a large set of blocks that look nice with respect to each other with small anticones, and the greedy algorithm does well on detecting them.

The idea of ghostdag is that we construct the k-cluster that we're building, sequentially by slowly going through the DAG and inheriting the heaviest k-cluster from its predecessor block by block and augmenting it with extra block. What you do is add blocks to this k-cluster that you have inherited from your predecessor block, and you keep adding blocks until you break the property of the k-cluster and then you stop. You want to maintain the k-cluster property.

Now we can proceed with the DAG to the next block. We have a 7-block k-cluster here, and a 5-block k-cluster that was constructed over here, so now how we decide on the k-cluster for this DAG? So we take the largest one, which is the 7 k-cluster, and we add a block. So now we have an 8-block k-cluster. This happens to be the largest one in this graph. So what do we do now? We have this large k-cluster. We basically just order them, in some topological sort which is canonical. Topological sort is where we assign each block an order in the sequence and we have to respect the links--- if you point to a predecessor, it has to have a smaller number in sequence than you. Ties have to be broken in some canonical way during topological sorting, such as by hash. Any way would work, as long as it's consistent.

## Intuition for resilience to double spends

Suppose you have these blocks created by honest miners. But the attacker wants to double spend a transaction. One thing the miner could do is insert a block that is a double spend and the way he does it is he points to thes eblocks and it looks like a well-behaved block that gets into the k-cluster. So there's a double spend in those two blocks. What I would claim is that this is not a successful attack because this intruder block is really well-behaved; it points to recent blocks, created right after them, and it was published right after, and it was referenced by the blocks created just after the attack block. So this transaction set was made public to the network, and people saw it, they saw the double spending, and the blocks get sorted and ordered in the topological ordering. So only one of the blocks will have the successful spend, and the other one will have an ignorable second transactoin which was trying to double spend.

## Comments

Extra data structures can allow for handling anticones and getting an extra-efficient implementation. Topological order can also be "inherited" from "heaviest" predecessor, which can also be efficient. And lastly, something to talk about is something our reviewers found interesting. If you think about the block reward, you can give every block in the k-cluster a block reward, which adds resilience to the selfish mining problem.

Selfish mining attacks are based on an attempt to push one of the blocks off the chain and deny rewards to honest participants. To push a block off of the k-cluster, yo uwould have to try to increase the anticone and build stuff in the parallel to it, but get into the k-cluster and push an honest block out. Because k is larger than zero in the bitcoin blockchain case it's k=0 but in ghostdag it's larger k, you're going to have to wait larger to increase the anticone size for the block you're attacking against. You need to build more blocks as an attacker, and thus you are going to be losing block races more often. It's a handwavy answer as to why, but selfish mining becomes more difficult.
