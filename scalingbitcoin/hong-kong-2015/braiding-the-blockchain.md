---
title: Braiding The Blockchain
transcript_by: Bryan Bishop
tags:
  - mining
speakers:
  - Bob McElrath
media: https://www.youtube.com/watch?v=fst1IK_mrng&feature=youtu.be&t=2h17m20s
---
Bob McElrath (bsm117532)

slides: <https://scalingbitcoin.org/hongkong2015/presentations/DAY2/2_breaking_the_chain_1_mcelrath.pdf>

I work for SolidX in New York. I am here to tell you about some modifications to the blockchain. All the things we heard yesterday about the block size, come down to the existence of orphans. The reason why we have these problems are orphans. These are consequences of physics and resources. This is not a fundamental property in Bitcoin. ((Transcripter's note: basically, only sharding can make local bandwidth less of an issue. Block size limit is not only for the orphan rate.))

An orphan is when two miners don't know about the existence of other blocks. Someone cannot propagate their block fast enough. Any time you have multiple writers, Bitcoin has no locks. No matter what we do with IBLT or weak blocks, we will still have this problem. We don't have to deprive a miner from profit.

What if the orphan block has no double spending? What if it contains a duplicate transaction? It's not a double-spend. It's a spend of the same UTXO. It's not a problem if we see the same thing twice. If this new block contains no conflicting transactions and, why not just call it a sibling instead of an orphan? We can allow a miner to be paid for this sibling block.

We have two chaintips, we don't know which one to follow, some miner in the future needs to tie them together and make a single changetip, to indicate that there's no conflict. The miner will assert that there is no transaction conflict in the entire subset of all the blocks. If you want to get rid of orphans, blocks must have multiple parents. Let's say there was a double-spend in this new block, then this forms a new chaintip, we have to evaluate the amount of work in B and C, and pick which one to work on top of. When there is a double spend, we must pick one.

A block can have multiple parents. This adds lots of complexity. This is a directed acyclic graph. That's the name of the data structure. What if we just take blocks and we throw them out as fast as we can, let them have multiple parents, could we make sense of this mess? Can we evaluate the amount of work? Can we track changetips in a DAG chain? In many ways, it's a linked list data structure. You cannot add something to the end of the tip with another person adding at the same time. So let's move to a more complex data structure.

The consequences of this linked list blockchain model includes orphan risk. DAG allows blocks with multiple parents. Blocks have parents. There are nodes and edges. Edges have direction. Points from children to parents. All of the links only go one way, that's what directed means. There are no cycles. This is cryptographically impossible to do cycles here. If we break the hash function, we have other problems. It's not a line, it's a graph.

DAGs can be partially-ordered in linear time. I can order the success of transactions in linear time. We have to make one more transaction relative to a general DAG. I am going to call this a braid.

I have drawn a graph at the top. A braid is a directed acyclic graph with none of the red links up there. Each block can have multiple parents. A block cannot name its own grandparent as its parent. So no incest. Mommy and grandpa can't have babies because that's gross. I am going to call the analog of a Bitcoin block something called a "bead". This is not a blockchain, so new data structure names. A sibling is a bead that cannot be partial ordered relative to their pairs. And incest is a parent that is simultaneously an ancestor of another parent. I cannot name anything back to the genesis block as a parent. I can already order the DAG using the parent information itself. Adding information about a grandparent doesn't add any new information that I didn't already have.

This is not a straight DAG, it's a slight restriction on a DAG. I am going to add an incentive. I am going to explicitly incentivize quickly transmitting blocks. Satoshi with Bitcoin did the opposite with the blockchain data structure. He slowed this down because of the problem of people simultaneously transmitting blocks. I am going to remove block time altogether. The GHOST paper adds another way to make blocks faster, by taking into account work in another block. GHOST blocks can contain double spends. If I am an attacker and trying to make a double-spend, I can mitigate my losses on the double-side of things. I require parents must not contain conflicting transactions, just like Bitcoin but unlike GHOST.

Per node, the bead time and block time and bead target difficulty and size are all decided per node. I am assuming this data structure is a smaller faster layer below Bitcoin, and we are going to checkpoint this data structure into blocks in order to have compatibility with old bitcoind nodes. There are many ways to get this into Bitcoin. I am not going to go into detail about this or the p2p layer. That's your job, not mine. This is a longer-term project than some of the other proposals you have heard so far.

Finally, I am going to publish these beads ex post facto just like Bitcoin does. Bitcoin-ng in a more traditional computer science way they elect a leader which dictates which transactions come next, but if I can find the leader hten I can ddos the leader. With bitcoin or this braid proposal, you have to ddos all miners off the network to shut the network down.

Here's a slightly more complex example of what happens when you have a fork. Suppose you have beads that have a double-spend between each other. Miners are going to have to choose which bead to work on. You cannot use both of those as parents. So you have to evaluate which one has more work. A consequence of the no grandparent rule (no incest), the graphs have no triangles, a triangle is explicitly naming a grandparent. These graphs have four-sided figures or higher because of that.

The beads that we mine on top of have to reference only one side of the double-spend. We have to take the subset of beads that point back to either A or B and we have to evaluate the amount of work in this subset. We have to evaluate how much work was done in that sub DAG in that sub group of transactions.

That's the basic structure. Okay, so how do you incentivize miners? You can't do what you do in Bitcoin. One of the consequences of Bitcoin is that, you have this rule that you can't spend a coinbase transaction per 100 blocks. This is about making the UTXO set too large in the event of reorg. Because of the size of the earth and people do generate these siblings, then how do you cdecide who to allocate coins to until you can see both of the siblings? Instead of not allowing people to spend coins in, and letting miners create the coinbase, don't let them. We should calculate the coinbase 100 blocks later, rather than calculating it first and not being able to spend it.

The consensus of this system, the changetip, is caused by the profit-maximizing behavior of the miners. This is what causes the whole thing to work. We need to think whether we have the consensus model right. Otherwise you will have a selfish-mining attack. I am going to propose something in a couple slides. Let's all do some analysis in the coming days and coming years and figure out if we have the right thing with this braid.

Miners are going ot individually choose the target. The only limiting factor is CPU and bandwidth. Signatures is CPU-bound, and network is bandwidth-bound. I am going to define two quantities here. One is sibling. The sibling is an analog to Bitcoin orphans. It's a bead that cannot be ordered to come before or after my own bead, using only the DAG's partial order. The time is across the horizontal axis. Siblings are defined per braid tip. You don't care about siblings with double-spends. Siblings must not have conflicting transactions. They must have a single set of UTXOs. Siblings may contain duplicate transactions. We could use IBLT, but we're likely to have blocks with identical transactions, so we will allow that. Each sibling can be weighted a work-weighted fraction of the transaction fee. If you have two siblings and each are at the same difficulty then evenly split the transaction fee.

There is also a cohort difficulty. Cohort is group of people about the same age, like classmates in school. It's the work of other miners in the same mining period. It's all of the beads between my youngest parent and oldest child. I want to look at the youngest parent, in other words, miners in this model would have to retarget their mining often, and look at the latest bead that they have seen. If a miner sits for an hour and mines on the same thing, this does not create a fast network. If we want to look at the oldest child, which says someone else came along and put more transactions on it, then a miner should publish a bead quickly in order to get miners to mine on top of it quickly. So maybe the miner was trying to steal fees by becoming everyone's sibling. We are going to disincentivize this by this quantity, or the children arrive late because of withheld blocks. The cohort difficulty will incentivize fast block transmission.

Here is a diagram of what this looks like. This is a sub-braid. On the left hand side we have A. And then a group of beads here. Siblings are relative to a particular bead. So I am asking what are the siblings of B? If any of G or B or D, eqriqieqrklewqlekqrfasdkfa... you can imagine taking B and G and D, and moving them horizontally and you can't tell which one came first which is why they are siblings.

The youngest parent to B is C, the oldest child is F, only one parent one child in this example, but everyone in that subset there which is D and E and B, which is included in its cohort. For a quiz, think to yourself, what are the siblings of G and the cohort of G, anyone want to shout it out? Siblings of G are C, D, E, F and B. Siblings of D are B and G. Its cohort is B and D.

Here is my proposed miner incentive formula. This is a graph. There are many ways to redefine interesting quantities on this graph that we could explicitly incentivize or disincentivize. The first term is transaction fees, the other one is reward. Proportional to difficulty, the quantity di n the denominator is cohort difficulty, cohort is a better word I renamed it. I am summing over transactions that are in among my siblings.

Rather than having 25 BTC, I could mine at 1/2 difficulty and get 1/2 BTC twice as often. This is probably valuable to smaller miners. The difficulty-weighted split of fees, bigger miners get more money than smaller miners. This causes us to incentivize and optimize the p2p topology to quickly propagate blocks. We are explicitly incentivizing the work between the youngest parent and oldest child, so we want to transmit thing quickly. The p2p topology in bitcoin is quite random right now, and could be optimized.

This means that smaller miners could mine without joining funds. I am pulling [p2pool](https://github.com/forrestv/p2pool) (( [http://p2pool.in/](http://p2pool.in/) )) into bitcoin itself. Optimizing the p2p topology makes censorship much more easy. Bitcoin has a linear, you just add up in each one, this is simplistic. Which braid has more work?

Getting rid of orphans forces the braid structure. Transaction volume is limited by bandwidth and CPU. Confirmation time can be much faster, we can throw out blocks as fast as possible, and we can do it as much as we can propagate blocks, which is limited by the size of the planet. We don't have to solve the NP-complete traveling salesman problem. Miner income can become much more smooth and more predictable. There are many ways to insert this into Bitcoin, and I am sure we will discuss this in the future. Smaller miners don't have huge pools, which is miner decentralization.

Q: You say miners can choose their own difficulty. Is there a limit on not doing empty blocks? It comes to mind that they can produce infinite difficulty blocks and mess with the network.

A: How to get this into bitcoin is a good question. Should there be a minimum difficulty floor is what you are asking?

Q: Many low-difficulty empty blocks would be a problem.

A: Possibly. I have not done that explicitly yet.

Q: Selfish mining?

A: Selfish mining happens because of orphans. It doesn't work here. ((Er, there are orphans. And there are incentives about not including transactions.))

Q: Orphan risk?

A: Yes, you have branches.

Q: What is the difference?

A: Fees are split evenly. There's no difference. Each miner has to choose which one to mine on. Satoshi's analysis baout 51% is correct for this, but not for bitcoin due to selfish mining.

Q: Am I right to say, I should mine an ...

A: Why?

Q: Because there can't be any...

A: If you want to get some transaction fees, ...

Q: ..

A: It would be zero. No split.

Q: ...

A: The reaosn why consensus works in Bitcoin is because miners are forced to choose which branch to take. If you throw out one block with a conflicting transaction, you see someone mining on another chain. You don't lose 25 BTC, you throw out a block at low difficulty, you lose 0.1 BTC not 25 BTC. That choice is very important. We have to force miners to pick one.

Q: Conflicting transactions?

A: Someone could publish a whole bunch of conflicting transactions? And lots of new changetips? Someone can do that in bitcoin too. The only one that matters are the ones that get mined. We could switch to a model where we get rid of p2p relay, and we mine everything. Throwing out transactions for free is not a problem. Only when they get mined, then I have to evaluate which one is what. It's an attack, but it's also an attack in Bitcoin. It's not something new.

Q: If there is a split or fork or orphan, how do you pick which of the two braids to mine?

A: Miner utilization is 100%. Miner utilization goes down if there are double-spends. We want miners to choose. That's their job. Their job is to pick one, and create a chain of consensus.
