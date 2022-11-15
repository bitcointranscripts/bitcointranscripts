---
title: Block Building with Clara and Murch - Episode 18
transcript_by: Whisper AI & PyAnnote
categories: ['podcast']
tag: ['Building a valid block 101', 'The current getblocktemplate algorithm', 'Child pays for parent', 'Is there something better?', 'How easy would it be to guess the next block?', 'Do we have a better idea than initially mining an empty block?', 'Empty blocks and SegWit', 'How to improve on the candidate set algorithm e.g., linear programming', 'Why should Bitcoin Core have better block building?', 'How to compare different block building techniques']
---

Chaincode Labs podcast: Block Building with Clara and Murch - Episode 18

SPEAKER_00: is we want the set of miners to be an open set where anybody can enter and exit as they wish and if we now had obvious optimizations that people had to implement to be as competitive as possible that would make it harder for new miners to enter this place

SPEAKER_02: Hey, Merch. Hey, Clara. Hi. Welcome to the ChainCode Podcast. Clara, for you, your first episode. We're so excited to have you here.

SPEAKER_01: Hi. I'm also very excited to be here.

SPEAKER_02: And today we're gonna talk about block building. So maybe you could start us off a little bit about Claire, how did you get the chain code? Like, what are you doing here? What are you spending your time on? Tell us a little bit about yourself.

SPEAKER_01: OK, so my background is in mathematics. I have a PhD in math. I was working on graphs and probability. And during my PhD, I also got really interested in this whole Bitcoin space. And then I decided to pursue it as a postdoc. So I spent some time at Berkeley and at Caltech. But I felt like I need to be in a place where people are really into Bitcoin. And here I am.

SPEAKER_02: So how does a mathematician get into Bitcoin? Because we need more of them.

SPEAKER_01: So I think that there are a lot of really, really fascinating questions inside this space. And as a mathematician, I felt like I want better motivations for the questions I'm answering, and more I think people in applied math might also think this way. So I think people just need to know that there are really cool questions here waiting to be solved.

SPEAKER_02: and what kind of cool questions are you pursuing?

SPEAKER_01: So the block building one that we will discuss later, it's a very clean algorithmical question. It's very similar to knapsack. It's very classical kind of optimization, things that are people were working on for a while. So it has a new context and it's nice to look at it from there. I'm working a lot on the Lightning Network. So there's a lot of economy and other things coming in, but at the end, it falls down to network or graph theory. So there's very, very nice questions that have to do with optimization and evolution of random graphs and similar things.

SPEAKER_02: It sounds like we're gonna have to record another episode We might Okay, so those are the kinds of problems you're currently working on. Yes Okay, so yeah, we'll look forward to to getting that on tape at some point soon Tell me maybe like this specific problem of block building. Why did why were you attracted to this?

SPEAKER_01: We might. Yes. So it's very clear, I think, to anybody that comes from the algorithmic world that what's happening now, it's a straightforward, greedy algorithm. And in most cases, this would not be the optimal solution. So when somebody from math or CS sees a not optimal algorithm happening, it scratches. Got it.

SPEAKER_02: at it and merge. So from a Bitcoin perspective, why does this matter? Why are we spending our time on this?

SPEAKER_00: What you don't want is that there is a huge amount of potential for somebody to do better than everybody else, because that will mean that they can make more money building blocks than other people and can get an undue amount of reward for the same work. So what we want Bitcoin Core to do is to, out of the box, do very well, maybe optimally, but reasonably well, that there is no huge advantage for somebody else to come in and find a proprietary solution that blows everything else out of the water. So one of the reasons to look at block building carefully is to make sure that there is no such hidden potential there.

SPEAKER_02: Oh, that makes sense. It's hard to get miners to upgrade, but it seems like they're probably making their own patches and, you know, try to get, try to get an edge. So running their own custom software is, you know, you'd, you'd.

SPEAKER_00: Bye! think that they'd be super curious to to tickle out the last little bit but on the other hand blocks have been not full and at one Satoshi per byte even if the block is full that's 10 milli Bitcoin in reward right today but you know yeah you're

SPEAKER_02: today. But you know, a year ago, people were all fees were all the rage. Sure.

SPEAKER_00: and in two more years we'll have another halving and in a few more years it'll get into the range of an of a full block at min-relay fee where it's interesting 20 years but so if you already know how blocks are built and what sort of where fees and block subsidy come from that's what we'll cover in the first section sure and you might want to skip that we'll put something into our show

SPEAKER_02: So if you're ready... Well, I'm excited to talk about this actually this one I'm sitting out. So I'm just gonna let you two talk and uh, And then we'll wrap it up.

SPEAKER_01: So, before we talk about building the blocks, we need to understand what are the Lego pieces we're putting into the block, right?

SPEAKER_00: So, blocks contain transactions, blocks are limited in a number of ways, they have to be valid, and they cannot be bigger than 4 million red units.

SPEAKER_01: Now, for example, I do know what are the limits on the block, but what are my options? Where are the transactions? What do I know about the transactions?

SPEAKER_00: Right, after somebody submits a transaction to the network, the transaction gets validated by every node that sees it, and then after validating, they forward it to their peers. To see whether a transaction is valid, a full node will look at what pieces of Bitcoin exist, look at their local copy of the UTXO set, and see that the transaction only spends funds that are still available for spending. And eventually, those unconfirmed transactions will land in the mempool of a miner, and miners will pick from the mempool a block template of unconfirmed transactions that they're trying to build a valid block from.

SPEAKER_01: Cool, so now we know that we have the mempool, it has this unconfirmed transactions, and then we want to build a valid block. So a valid block is of limited size. And we also have some rules into which transactions can go into the block.

SPEAKER_00: Right. So you cannot include invalid transactions. Well, you can, but it makes an invalid block. And transactions have to be in the correct order, right? You cannot spend funds that don't exist yet. So if you, for example, have a transaction that spends funds from another unconfirmed transaction, the parent transaction has to go first to create the outputs that the second transaction then uses in its interest.

SPEAKER_01: Are there other ways that a transaction can be invalid with signatures, obviously?

SPEAKER_00: Right, so it could be just generally malformed. It could spend funds that don't exist, as in like just some made up pieces of Bitcoin. You could have the problem that there's two transactions that spend the same funds, which basically falls under the same rule. The first transaction consumes the existing unspent transaction outputs. And then the second one doesn't have the ability to spend them again. You could have an invalid script or invalid signature, or you could have a transaction that spends the same funds twice in the transaction itself. So if you naively just check that a transaction only spends one set of inputs and no other transaction does, you might miss that you spent the same funds twice. So I don't know the whole set of rules by heart, but there's a bunch.

SPEAKER_01: So. So in this space of block building, I think we'll mostly focus on the limit on the block size, and only spending available UTXOs or existing UTXOs.

SPEAKER_00: maybe one more comment. There's a special transaction that has to be in every block, which is the coin based transaction or the generating transaction. It's the one that goes first in the block and that can collect the transaction fee and create new bitcoins. And after that, a miner may include zero to full block of transactions and they can pick any transactions they want, as long as they follow these rules that they're not spending any funds that don't exist yet and so forth. It's completely up to the miner to pick what they want to include, but generally is the goal of the miner to collect as much money as possible. So we expect miners to build the most profitable block.

SPEAKER_01: Thanks for watching! So how would they do that?

SPEAKER_00: Well, currently we assume that most miners are using Bitcoin Core and Bitcoin Core has a function called getBlockTemplate. getBlockTemplate will look at the full nodes mempool, the queue of unconfirmed transactions and for each transaction in the mempool it has stored the size and fees of all of its ancestors plus itself.

SPEAKER_01: What do you mean by ancestors? Right.

SPEAKER_00: Right. So we had previously mentioned if there are transactions that depend on each other by one transaction first creating a transaction output that another transaction in the queue is spending, they have to go in that order, right? Because the output has to exist before it can be input for another transaction. So any transactions that topologically precedes another transaction, we call them ancestor.

SPEAKER_01: Okay, so for each transaction, we're looking at all of the other transactions we will need to include in the block beforehand for the block to be valid. We sum up the weights of all of these transactions. We sum up the fees of all of these transactions. And from this, we discover how many Satoshi's per bit we will get from this whole per byte.

SPEAKER_00: Or better yet, per V-Byte, because SegWit's been active.

SPEAKER_01: Yes, I quit.

SPEAKER_00: Note that this ancestor set fee rate for the transaction does include all the ancestors and the transaction itself. The observation here is that the transaction with the highest ancestor set fee rate, including that and all of its ancestors, will be the most profitable next step in building a block template.

SPEAKER_01: Given these rules for blocks, there's a current algorithm that gives us a block template, right? How does it work?

SPEAKER_00: Yes, so the call getBlock template, it uses the mempool, which is already a list of all the unconfirmed transactions with its ancestor set information. And then it just looks at which ancestor set will give me the most fees per Vbyte and includes that first. And then it updates all the other transactions that are impacted by this ancestor set getting confirmed, recalculating their ancestor set information and then pops the next one from the top. It does that until nothing fits into the block anymore. Block template is done.

SPEAKER_01: Yeah.

SPEAKER_02: Thanks for watching!

SPEAKER_01: or until the mempool is empty.

SPEAKER_00: Yes. Okay. Sure.

SPEAKER_01: So in general, this is a greedy algorithm. At every step, we look at a transaction, what would we need to put in to have this transaction in the block, what are the dependencies, which was the optimal one looking at its ancestors, put it into the block and then continue with this question. So are we happy with being this greedy?

SPEAKER_00: So this works pretty well, actually. It's also very fast with having pre-calculated all the ancestor sets for the unconfirmed transactions in the mempool already. It has two small things, or maybe not quite so small things, where it does not necessarily find the optimal solution. So A, it's a greedy algorithm and it does not find the optimal block in the sense that it doesn't necessarily fill the last few Vbytes in the block if it just has collected some stuff already and nothing else fits anymore, it won't go back and shuffle the tail end a little more to get the last few satoshis.

SPEAKER_01: Actually... Given the current algorithm, it also motivates some wallet behavior.

SPEAKER_00: As many of our listeners are probably familiar with, there exists a concept called child pays for parent. And this leverages the dependency between a parent transaction and a child transaction that a child paying a high fee rate can only get included once its parent is included because it spends an output that the parent creates. And as we have said before already, you cannot include the child unless all of its inputs exist. So when you have multiple of these situations in parallel, where say one parent has three child transactions that all pay more fees than the parent, you would have three separate ancestor sets that each compete to be the best ancestor set to be included in the block. And you can get now situations where the three children taken together with the parent would have a greater fee rate than what is currently being included in the block, but we would not notice because we evaluate them separately. We noticed that if we could search in the mempool data for constructions where this is the case, we actually can find sometimes constellations in which we change what block template would be built and make blocks more profitable for miners by including these sets of transactions together first.

SPEAKER_01: The current algorithm just looks at child, parent, parents, parent and so on and so forth. So in some sense, it's very one dimensional, right? Just one above the other, above the other.

SPEAKER_00: Well, you can have multiple parents, so it's a DAG or a directed acyclic graph. Yes, it's fairly one-dimensional because you basically just look at a transaction with all of its ancestors.

SPEAKER_01: So in the current algorithm, we're just looking at a transaction and all of its ancestors in what we are suggesting to do. We want to do something slightly more complicated where we look at sets of transactions and all of their ancestors, right? Because we can't put transactions without all of their ancestors set, but our starting point would not be a single transaction, but we could have many transactions.

SPEAKER_00: Essentially, you can think of what we're searching for as an overlap of multiple ancestor sets, right? So if you have a single child that pays for its parent, you would want to combine it with the ancestor set of another child of the same parent. So they need to have some overlap in their ancestry. They need to be connected in the graph in some way. But the overall situation is such that through the shared ancestry, their set fee rate for the whole set of transactions is higher than for any of the individual ancestor sets.

SPEAKER_01: That sounds great, but as we know, one of the main things that we want from a block building algorithm is for it to run quickly.

SPEAKER_00: Yes, so especially in the moment after a new block is found, we want miners to be able to switch over to building the succeeding block as quickly as possible. And miners often build an empty block template intermittently because they don't know for sure which transactions they can include until they have evaluated the parent block. But we want them to be able to switch over as quickly as possible to a full block at the next height.

SPEAKER_01: So let's talk implementation a bit.

SPEAKER_00: As you might imagine, if you have all the ancestor sets for every transaction, you have a very clean list of things that you need to look at. For every single transaction, you just look at all of its ancestors. That's O of n in the size of transactions. To find what we call candidate sets, these overlaps of multiple ancestor sets that could be even more profitable to include, we need to essentially search the power set of graphs of transactions that are connected. So what we do here is we look at one transaction that has a high fee rate, and then we cluster all of the transactions that are connected to it, either via child or parent relationships. I'll be referring to this construct, the maximal set of connected transactions as a cluster. And then in this cluster, we want to find the best subset, best as in the highest set fee rate. Obviously, we can only include sets of transactions for which all the ancestors are included. So we're looking at some overlap of ancestor sets, and we call this a candidate set.

SPEAKER_01: So this candidate sets could be ancestry sets as we've seen in the current algorithm, but because we're allowed to traverse up and down from child to parent to parent back to child, we get a more complicated structure, but to keep the block valid, we need to make sure that at the end, whatever we're trying to put into the block has all of the ancestry.

SPEAKER_00: Exactly. Right. So as you might imagine, this is no longer searchable just in the order of the size of transactions, because now we have to essentially search through the power set of all the transactions in every cluster that explodes very hard in the complexity. And that gets us in trouble with, we want us to run really, really fast. Our idea is, we would continue to quickly build a fairly good block using the ancestor set based block building that we have already, and then we would perhaps in the background have a second process that searches for a more profitable block using these candidate sets that we have been discussing.

SPEAKER_02: Alright.

SPEAKER_01: But of course, we don't actually need to look at the power set of all the transactions, so the first thing we need to remember that a lot of subsets of transactions are just not allowed into the block, so we definitely want to focus our search on subsets that are valid. Even when we focus ourselves only on valid subsets, we can also do things a little bit in a smarter way.

SPEAKER_00: Right. Yeah, there's a few nifty little tricks that we found while we have been writing our research code for this. We start our search in the cluster by a number of initial candidate sets. And since we have them already, we just initialize with the ancestor sets that exist in the cluster, which is for every single transaction in the cluster, we have already a starting set. The next observation we had was, when we have an ancestor set in a cluster that has fee rate x, any leave in the cluster, as in any childless transaction in the cluster that has a lower fee rate than that, can never lead to a better candidate set than this. So if you have a transaction A that pays five Satoshi per byte, that has a child which pays four, you will never get a better candidate set by including this child with four when you already have something that pays five Satoshi per V-Bank.

SPEAKER_01: I think an important point to make is that when we're thinking about fee, we're talking about the effective fee rate. So we're not interested in fee that this transaction would give us. I, again, remind our listeners that we're talking about fee per VBate.

SPEAKER_00: Yes, I might accidentally say fee. I always mean fee rate and always specifically the fee rate of a set of transactions that if we include them together would be the highest across all the unconfirmed transactions still in our mempool. So we have two optimizations so far. One is obviously we don't have to search the whole power set of transactions in the cluster. We can limit ourselves to only searching the valid subsets and we can do that by starting with the ancestor sets in the cluster and then expanding from the ancestor sets by adding additional ancestor sets to that. So specifically if we have a set of transactions say maybe just a single transaction that doesn't have any unconfirmed parents we would add the ancestor sets of each of its children to create new candidate sets to add to our search list and we basically just go through our search list greedily. We first evaluate the candidate sets with the highest fee rates, expand from those again but since we start with all the ancestor sets in the cluster already we can very quickly use the leaf pruning that I mentioned to cut down on transactions that we never have to look at. So every time we find a better candidate set in the cluster by expanding it for example by including a second child for a parent and getting a higher set fee rate we actually reduce the search space at the same time. So very quickly on this cluster we'll find one single best candidate set and have evaluated all possible combinations either by dismissing them or by having actually evaluated them and then we just remember this as the best possible candidate set in a cluster of transactions. Now if we look at a mempool a mempool can have up to 300 megabytes of transactions and we don't really want to traverse all of that immediately really we only want to look at the relevant transactions. So what we do is we sort all the single individual transactions by their fee rates and we only start clustering even on the transactions that have the highest fee rates. So we basically move down from an infinite fee rate and pick the single transaction with the highest fee rate, search for its cluster, look what the best candidate set in that cluster is, check out what the set fee rate for that candidate set is and then we resort the whole cluster into our list of data that we need to look at at the fee rate of the best candidate set in that cluster. Then we use for example a heap for that and we bubble up the next transaction or cluster by highest fee rate and if a transaction bubbles up we cluster it and sort it into the heap as the cluster. If a cluster bubbles up we pick its best candidate set because now we know across all of the mempool this is the set of transaction that has the highest possible fee rate and we can just include it in our block. When we include a candidate set into our block we naturally need to remove it from the cluster and we have to update all the transactions in the cluster to to forget these as unconfirmed ancestors and therefore like have new ancestors had fee rate, ancestor size, ancestor fee and we put them back into our list of single transactions and we only look at them again if any of those single transactions bubble to the top by fee rate before we fill the block. That's a few of our optimizations so far I guess.

SPEAKER_01: Yeah, and I guess that if we would have other precalculations, we could have made things quicker because we're starting now only with the ancestry sets for each transaction, but we could have precalculated such clusters or something like that.

SPEAKER_00: Well, the downside of precalculating all the clusters is that we would have to cluster all the 300 megabytes of mempool potentially when in the end we actually want to only include about one megabyte.

SPEAKER_01: Right, but we get to do it to some extent in our off time. We don't do this when we build the block, and we're in a hurry, so...

SPEAKER_00: Oh. Oh, absolutely, we should be pre-calculating the whole block, actually, not just cluster information. The cluster information is somewhat ephemeral anyway. As soon as you pop the best candidate set out of the cluster, you have to recluster and re-search for the best candidate set. So just pre-calculating the clusters is sure a little benefit, but actually just pre-calculating the whole block template in the background on a loop, say, every time we add new transactions or every minute or so, and then having something at the ready when the user calls get block template would be maybe interesting. Of course, the problem is when a new block gets found and when we want to have a new block template quickly, it might be slow to do all the candidate set search on every cluster and all that. So when it's supposed to be as quick as possible, we should use the ancestor set-based approach and respond with that first.

SPEAKER_01: I wonder how easy it is for us to guess what's the next block we're going to see. So to calculate both the block we want to mine now and the block we will want to mine once we'll hear about the block, because if everybody's using the same algorithm, I know what's going to be in the block I'll see pretty much, so I have a good guess at least.

SPEAKER_00: you have a very good guess but I think especially for transactions that were just broadcast on the network you don't have a good guess whether the miner has it already included in the block template even if the mining pool operator has seen it already they give out templates to all the mining machines only whenever the mining machine has exhausted the template they're working on so even for like 10 20 seconds after the pool operator has built a new block template the machine will maybe still work on traversing the extra non-space for that block for the previous block template so there is a little bit of a latency between a new block template being created and that actually being what mining machines work on so you could be missing some transactions and that not would not be a huge problem you would just not have them in your look-ahead block template but you might also have some transactions that are precious to the miner because say they also have a wallet business on the side and they prioritize the transactions of their customers or they they have an accelerator service and include some transactions that are actually not in the very top of the mempool but maybe would be in the look-ahead block so even if you have the look-ahead block you can't really use it until you've evaluated that it has no conflict with the previously found block.

SPEAKER_01: Do we have a better solution than mining on an empty block in the beginning? Like, should we guess a block and take the risk that it won't be actually valid? Or should we go for an empty block?

SPEAKER_02: Which should we guess about?

SPEAKER_00: I guess at this point, the transaction fees make such a small part of the total block reward. And the total block reward, of course, consists of two parts. There's the block subsidy, which is the newly minted coins, and there are the transaction fees from the transactions included in the block. And we had a period of six and a half months earlier this year, where we did not have an empty mempool. There was always a queue of transactions trying to get confirmed. But since mid-June, roughly, we've had ample block space, mostly because there was a huge shift to more efficient output types getting used. And the hash rate reduction that happened after China banned mining was quickly regenerating. So we had faster blocks for some time, and faster blocks means more block space, of course. So those two things together, I think, led to us essentially having abundant block space all the time, which meant that the fee rates have been very low for the past five months. And whereas in the first half of the year, the reward was about one-sixth transaction fee, in the past half year, it's been more like maybe less than 5%, 2% or 3%. The risk of having an invalid block and losing the newly minted coins is probably going to outweigh the reward of including transactions in the block.

SPEAKER_01: But we can expect sometime in the future, a sharp threshold moment or just a threshold moment as the block reward is having after give or take for years.

SPEAKER_00: One thing that miners could do is that they keep a stash of their own transactions that they don't broadcast to the whole network and only use for their own block templates and The moment that a new block is found They include those the problem is if they always include them in their block templates They would leak because people see what block template they're building So I haven't thought this through enough to make sure that it's a viable idea But I think that empty block mining will will remain a thing What we want to do is to make block validation as quickly as possible and then to make block building as quick as possible So that there's as little delay as possible between a miner hearing about a new block and starting to mine a new full block

SPEAKER_01: I do find the concept of a miner having secret transactions, so to say, that they keep on the side. Where did they hear about these transactions at all?

SPEAKER_00: Oh, I mean, for example, they could have payouts to their pool contributors, or there is one mining pool that was closely associated with a wallet service for a while, it could just be those. But on the other hand, that seems a little far-fetched, because if you have a wallet service, people want to transact, they don't want to wait for that transaction to go through.

SPEAKER_01: So actually as a mining pool, if I want to pay the miners, it does make sense to, instead of mining on an empty block, mining on my rewards, if I'm paying out of previous block rewards, because I know there's not going to be in conflict, these are fresh coin just minted, nobody could have touched them besides me. Do we see this behavior?

SPEAKER_00: I don't think we see that very much. I'm also kind of expecting that given there's very frequent payments of small amounts to people, I would expect that mining pools that eventually adopt lightning as a withdrawal means to their pool contributors. I've taken a lot of time to say that. I expect empty plugs to remain.

SPEAKER_01: Cool. How often do we see empty blocks?

SPEAKER_00: Not that often anymore. We actually saw a fairly sharp decline in empty blocks when SegWit happened, because SegWit required miners to update their software. And for a long time, miners had been running older software, and all the efficiency improvements in the peer-to-peer layer and block building and stuff like that suddenly came to pass in the software upgrade. And we saw two things. We saw especially that there was a lot fewer mini-blockchain forks, where there was latency and or validation was slower, and two mining pools found blocks at the same height. And that was especially because the compact block relay happened between whatever they were running and SegWit, and then I think also a little bit faster block validation and build.

SPEAKER_01: So this is what we have on our plate now, but we already talked a bit about what might happen in the future, but we also have a few thoughts about what else can we do to make block building even better. So there is linear programming solutions that solve, to some extent at least, the other problem we've talked about with blocks.

SPEAKER_00: It's the optimal use of all the available block spaces.

SPEAKER_01: Right. Because sometimes when you're doing greedy things, you, so a very crude example would be I can fit two kilos into my knapsack and thanks for everybody who giggled because they know what's the knapsack problem, so you can put two kilos in your knapsack and you want to put as many items as you, as you want. You have one item who is, who weights a kilo and a half and two items that weight one kilo, so if you're greedy, you take the kilo and a half item and can't fit, and can't fit anything else. And if you're not as greedy, you take, you look at it and say, okay, I can take the two items that weight one kilo each. So this is a problem that our current algorithm does not solve, but by using linear programming techniques could be solved, a downside of these techniques that they have a tendency to be slow, although it's unclear that they have to be, and this is something we definitely would like to look into.

SPEAKER_00: So basically, by running linear programming, we would be able to find out how close to the optimal solution we can get with just a candidate set based approach.

SPEAKER_01: Any other thoughts on the future?

SPEAKER_00: Maybe we should touch on why it's important that Bitcoin core has really good block building. The idea is we want the set of miners to be an open set where anybody can enter and exit as they wish, especially the entering is interesting obviously. And if we now had obvious optimizations that people had to implement to be as competitive as possible, that would make it harder for new miners to enter this place.

SPEAKER_01: So I would like to comment that even if now the mining fees from transactions are not a crucial part in the future, they either will become something important or mining won't make sense. As the block subsidy is going down, the fees become more and more important. And so in the future, this would carry a lot more weight.

SPEAKER_00: Yeah, definitely. Even if we're thinking right now, this week we just crossed 90% of all bitcoins being in circulation. In 2036, it'll be 99%. And I think 2046, it'll be, or 2050, it'll be 99.9%. And as the block subsidy keeps having, even just a regular full block at minimum fee rate, we'll eventually have more fees than new coins. I think that's reached by 2060 with one Satoshi per VBITE and four million white units.

SPEAKER_01: I think this is already something Satoshi mentioned in the white paper.

SPEAKER_00: I mean, that's a far, far future, but we're trying to build a system that lasts for multiple decades, so we have to think about the long-term incentives. So Clara, tell me, we had an idea how we should be measuring whether our candidate set-based approach makes sense and is a good improvement. Can you tell us a little more about that?

SPEAKER_01: So there are a few ways we can compare different block building techniques, one of which is just looking at a certain mempool and then saying which block building algorithm will do better, which is a valid point of view, which we're exploring. But another very interesting thing to look at is what happens if, say, 2% of the miners use our new algorithm while the rest are using the old one. And for this we want to use a simulation, of course, that does the following. So we have snapshots of the mempool and then at any moment we know that a block is built. We're going to flip a coin that tells us are we going to use the old algorithm or the new algorithm. And then we build a block, we update the mempool, there's new transactions coming in, again find a block, flip a coin and decide. Some of the listeners might be familiar with Monte Carlo and things like that, so if this is where your mind went you are absolutely correct. And by doing this we can compare how much can a miner gain when they move to the new algorithm, especially in an environment where the old algorithm is still running. This might also affect the changes, how quickly will the algorithm be taken by the other miners. Because if you can already do much better by being the only one that does it, that's a very nice incentive.

SPEAKER_00: Right. And then there's also the aspect, it's hard to say how it will affect how wallets build transactions when there's new behavior in how blocks are being built. So when we actively search for situations in which multiple children or descendants bump an ancestor together, this might lead, for example, to people crowd sourcing a withdrawal from an exchange with 200 outputs to get it confirmed a little quicker. We wouldn't be discovering that right now at all with ancestor set-based block building, but we would discover that with candidate set-based block building, and then maybe if there's a few two, three, four percent of the miners already using that, people might start to say, all right, I'll ship in and try to spend it already, and together we'll get withdrawal confirmed more quickly, and that would be the incentive for miners to switch over and start using that. And that's the new block building algorithm for miners.

SPEAKER_01: We already see this sort of crowdsourcing behavior in the mempool. So.

SPEAKER_00: We found a few interesting clusters when we were analyzing mempool snapshots. We have this data set where we have, when a new block came in, the node took a snapshot of what was currently in their mempool, and we can then compare what we see in the block and what was available for block building, and that's what we use to build our alternative blockchains in this Monte Carlo approach. And we found some curious clusters already with over 800 transactions where there's a lot of children spending from the same parent and stuff like that. So there is some of that going on already, but currently, of course, mining doesn't exploit that, so people aren't doing it on purpose. It's just people that are, I don't know, withdrawing from a broker, and the broker has such a volume that they pay out to 100 people at the same time, and five of them immediately try to spend it at the same time. But they're competing with each other because it's getting evaluated as five separate child pays for parent attempts, whereas we would be evaluating it as a single descendants pay for ancestor constellation. So we do the Monte Carlo approach. We run that alternative blockchain that we're building a few times with, say, 2% of the miners using our new algorithm already. What do we do then?

SPEAKER_01: What was that? Thanks for watching!

SPEAKER_02: Thanks for watching!

SPEAKER_01: and then we compare how better did the miners that use the new algorithm did comparing to the ones that use the old algorithm. So that's another viewpoint for comparing these two algorithms. Yeah. So we already have some data available. There's more coming up.

SPEAKER_00: Thanks for watching! Yeah, we published a thing about basically comparing one algorithm with another algorithm at a specific height for every block. Now we're doing the, let's build a whole blockchain instead, because that's more fair, because we won't reuse the same transactions again. Say there is a constellation for candidates that should get preferred. We would be including it maybe for multiple blocks in a row if we don't build in a whole alternative block.

SPEAKER_02: Maybe just sort of to wrap things up, I have two questions of listening to that episode. The first one is, if you can get more fees into this current block, doesn't that just pull fees from a future block?

SPEAKER_01: Well, if there aren't a lot of transactions in the mining pool, that is, the whole current mining pool can fit inside of a block, you don't need any sophisticated algorithm. You just need the block to be verifiable and have the transactions in the correct order, and you send it off. It doesn't matter what you're doing. Our algorithm becomes important only when there is actual competition for block space. And in that case, you're assuming there are more and more transactions coming in. So, yes, you're taking the transactions now, but there's going to be more transactions later on for the next block.

SPEAKER_00: So it's it's kind of fun how it works out. We want people to build the best possible blocks and we want for example to have these constellations of multiple children to bump a parent together and it turns out that if a miner does find these constellations they also make more money. So if there's only one miner out of 20 that adopts this they'll make more money than the other 19 and other miners will also adopt this new algorithm.

SPEAKER_02: That's a nice incentive. And then my other question is obviously mining is a cutthroat game. And so when you're talking about the speed of serving these block templates and these optimized blocks, where's the edge of speed versus the optimization of the fees?

SPEAKER_01: So in some cases, you'll find miners even mining empty blocks in the beginning. So you can think about it as a stepped process. You start with an empty block, then you use the quickest algorithm that gives you a good enough block, and then after a while, if you haven't found a block, you look for a better block, and you can think about other algorithms even better than what we're proposing now that are even slower using linear programming or something like that, that will also be like the third block template that you serve if you find that you have enough time.

SPEAKER_02: Yep.

SPEAKER_00: What happens when you run a mining pool is that you don't create one black template and then your miners are working on that for the whole duration until a block is found. You keep updating that as more transactions come in. So you're constantly recomputing the block template anyway. If some of those happen to just have a little more fees a little later after you switch to a new height, I don't think, sure, it might not be mined on in the first half minute or so, but generally, if it's transparent, it'll just snap into place.

SPEAKER_02: sense. So this sounds better in every way. When do we see it in the wild?

SPEAKER_00: When Well...

SPEAKER_02: Thanks for watching!

SPEAKER_00: careful Asking around a little bit what might need to happen for for such an algorithm to get integrated into Bitcoin core seems to indicate that there might be either need to make it run separate and The architectural challenge of that would be easy or if you want to integrate it properly into the Mempool Mempool is such a central part of how everything fits together in Bitcoin core. That would be a pretty invasive change, so I'm a little bearish on the timeline

SPEAKER_02: All right, very good. Well, thank you both for your time. Enjoy the conversation, and we'll look forward to getting Claire around soon again. Thanks.

