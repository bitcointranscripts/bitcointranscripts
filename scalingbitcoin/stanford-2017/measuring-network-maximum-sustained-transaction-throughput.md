---
title: Measuring maximum sustained transaction throughput on a global network of Bitcoin nodes
transcript_by: Bryan Bishop
tags:
  - p2p
speakers:
  - Andrew Stone
date: 2017-11-04
media: https://www.youtube.com/watch?v=LDF8bOEqXt4&t=3981s
---
Andrew Stone, Bitcoin Unlimited

We are 25 minutes behind schedule.

We have the rest of the team wathcing remotely. I think the motivation for this project is clear. Transaction volume on the bitcoin network could be growing exponentially except that there is a limit on the number of confirmed transactions. Transaction fees have increased and confirmation times are not reliable, and bitcoin is unusable for some applications.

Some people want to see the max blokc size limit lifted. Some people worry that p2p electronic cash will be eliminated if changes occur or don't occur. Bitcoin is highly scalable because users can be their own banks, verify their own transactions and send payments to any other user without going through any miners. All of this technology is already available to the world's human inhabitants.

The scaling concerns are related to network nodes because those nodes must process every single transaction. If you imagine those 4 billion people I mentioned earlier each making one transaction per day, that makes out to 50k transactions per second. We can't forget about network nodes because they play a critical role in securing bitcoin.

I was interested in 50k/sec number. Is this easy to achieve? Is it physically impossible? Maybe somewhere in between. It seems to be controversial. We wanted to measure the maximum sustained throughput on standard off-the-shelf client software already out there and see how close we would be to achieving that number.

## Gigablock testnet

We built a gigablock testnet. As of October 2017, it has 18 nodes. Our standard hardware spec is 4 core machine with 30 megabit/second internet. 16 GB RAM and a solid state hard drive. Typically we are only mining with 4 to 6 of those nodes. The rest are hosting python scripts which are generating a bunch of 2-input 2-output transactions and broadcasting them to the local bitcoind instance.

The generators can generate about 2000 transactions/second sustained. So for the past 2 months we were doing some ramp tests. We plot time on the horizontal axis , and transactions per second on the vertical axis. This makes a ramp. We ran this profile on October 25th. We ran the generators until we got to 500 tx/sec a few hours later, with a ramp.

If I plug in the rate for successfully submitted transactions, I get this purple curve here. We kept up well. Where things get interesting is if he look at the rate where a particular node was able to emit transactions into its mempool. All of the nodes or all the miners had similar charts. So we see that when the throughput rate was low, below about 100 tx/sec, the mempools of all the nodes are keeping up with the overall transaction generation rate.

However, when we cross 100 tx/sec, the mempools begin to lag behind. We identified bottleneck number one. 100 tx/sec, is mempool acceptance bottleneck. We can learn some interesting things about block propagation here as well.

There are probalby 40-50 blocks solved during this ramp. When we loo kat them, we see that the mempools were 99% similar, so it works really well, we were able to compress the block by a factor of 3. But by the time we get to this point over here, the transactions in node A's mempool are quite different from the transactions in node B's mempool. The xthin compression doesn't get you much savings. So you're propagating blocks in full at this time. And then we see this collapsing behavior of the network.

What was the root cause of this? We can gain insight into this question by looking at the generation rate versus the CPU load. If I plot the data, I get this scatter plot. What we see is that when we hit the bottleneck zone at 100 tx/sec, we are only using about 25% of the CPU power. If I plot the 8 and 16 core machines-- which we hit those blottlenecks at....

Well, I can hear Thomas Zander yelling the answers over the internet right now. It's a single-threaded process. We're encounter problems as soon as we max out the node. So we should parallelize the mempool acceptance, and then we can do 1000 tx/sec, and bursts to 10k tx/sec.

What does a ramp test look like with the mempool acceptance bottleneck removed? We see now that our mempool acceptance rate keeps up good. The rate that transactions are actually committed to the blockchain- there's a new bottleneck. We did a few ramps. We were never able to sustain more than 500 tx/sec into the blockchain.

To under that bottleneck, it helps to examine the xthin block propagation. I am plotting block size on horizontal, and propagation time on vertical axis. If I look at the data for all the blocks propagated on our test network in the past 2 weeks, I get this scatter plot here. This is a log-log chart, so I'm looking at several orders of magnitude of depth. The color is the level of compression indicated. Green is good. 100 MB propagates with only 3 MB block information. Some of those points are red- that's when xthin fails for whatever reason and we propagate the blocks as full block data all at once.

Since we have the data, let's do some statistics on this data. We can fit it to a linear model for block propagation time as follo. Tau is our propagation time. Q is our block size, and tau naught is our inherent coefficient (the anti-block time), and ... the block propagation impedance in seconds. If I perform a least square best fit to this scatter plot, I get the following coefficients. If I plot the resulting curve, I get this. It's a linear model. I thought it was an interesting coincidence that according to the regression, ... block time to propagate..

If you want to think of this in transactions per second, you can look at this axis up here. It sheds some light into being able to commit only 500 tx/sec in the blockchain. When you get into the highl evels of throughput, the propagation of the block becomes commensurate with the time that.... Andrew wrote a paper a couple years ago, the time that the blocks and try to come to consensus, is ... a time.. in terms of.. getting data into the blockchain. We believe this is the second bottleneck propagation time is commensuare with block time, and improving xthin or protocol would probably help us scale to a higher level.

An interesting sidenote is that the propagation time did not depend on the network bandwidth for the given nodes. If you calculate the bits per second they are actually propagated when the next block is sent. It's 500 kbits/second. It's vastly smaller than the pipes connecting the nodes. We're limited by the software, not by the size of the pipes connecting to them.

My last slide before I turn it over to Andrew.... regressions and interpolations. We found that CPU load and amount of bandwidth consumed on the network scaled linearly with the transaction throughput. This allowed us to solve for regression coefficients for those two terms. Interpolating for our bottleneck, we can say that running a node at 100 tx/sec means that you are maxing out 1 core worth of CPU power and you're sustaining 3 megabits/second on your internet. At these levels, we get these numbers, and at your global adoption levels of 50k tx/sec, you get these numbers here. If you put Bitcoin Unlimited on a 500 core machine and try to get 50k tx/second, you're not going to get that. This is assuming you are going to rewrite the code and take advantage of parallelization opportunities. These are the empirical regression coefficients-- we can improve these numbers by a factor of 5 by doing more work on code.

In terms of memory and disk IO, one weakness of our experiment is that we are running with a utxo set size of approximately the same set size of bitcoin's current utxo set. If we have 1000 tx/sec, the bitcoin utxo set size is going to be significantly better. I don't think my numbers for memory or disk IO are particularly relevant. But we will be doing a utxo set stress test and maybe we can present that at scalingbitcoin next year.

I thought it was interesting that the bottlenecks we found were not related to the protocol or the infrastructure but they were bottlenecks in the implementation, namely inefficiencies in the Satoshi codebase. My hunch is that we can achieve VISA-level on standard midgrade machine on a bunch of work done to make better software.

[SNIP...]

Andrew

## Mempool magic

Thanks. I did two types of optimization to achieve the number. The first one is parallelization and secondly just raw optimization of the code. If you look at this slide, this is what the original code did. I think you guys can take a look. Sorry if this ... might be more appropriate for people wh have looked at the code, sometimes you have to dive into the details. There was a socket receive thread and a message receive thread. And then send to the mempool which would do other work like midblocks and stuff. I focused only on transaction acceptance. It looks more complex, but it's probalby 95% the same actual code, it's just a reorganization.

We have a socket receive thread at the top, which is the same as in the original code. And then that sends its message to a message handling thread (4-8 of those about). And these message handling threads do the normal block commitance and stuff because I didn't optimize that yet. If it's a transaction that has come in, instead of handling it directly, I put it into an incoming transaction queue. There are 4-8 transaction validation threads that run and commit the ... when they, if a transaction is accepted then they actually don't commit the transaction to the mempool right away, they put it on a mempool commit queue and then a mempool ... actually commits it to the mempool.

The reason why I separated the last two in this way was so that the mempool is actually essentially a read-only database while the transaction validation threads are running. So all of these transaction validation threads can run simultaneously without having to deal with locking. Some people might ask, what happens then, obviously, when you have a double spend? And the answer is that it's tricky, but we keep a bloom filter or bloom-like filter of all the inputs of the transactions that are in-processing. If there's a conflict, then that transaction is shuttled off to a "try later" queue and then periodically when the mempool commit thread runs, then these try-later transactions are put back into the incoming transaction queue. This ensures that any transaction conflicts are handled and there's no incorrectness in the algorithm.

Obviously this, architecture assumes that, we don't have a lot of conflicting transactions. They are transactions-- unonfirmed transactions spending another one within 5 seconds or so. I think that's a reasonable assumption because what we're trying to do here is handle a whole world of people spending bitcoin, not individuals spending lots of bitcoin. Hop to the next slide.

One more thing to say is that after I separated out those threads, I got almost no additional parallelization and the reason why is that the original code is doing a lot of locking. People who use the code are doing cs\_main locks which are used almost everywhere. So I needed more fine-grained locking. I switched a lot of the major states, the locks on major states to a shared mutex where you have simultaneous readers but only a single writer. All my transaction commit threads can take read locks on the mempool, and then periodically, every few seconds, the writer thread comes in and all the readers stop, the writer commits to the database. This was actually the majority of the code changes was in the locking strategy. The reason why is because the standard template library in C doesn't allow recursive sharing mutexes, they haven't implemented them. We use recursive mutexes. I had to de-recurse the mutexes before writing shared mutexes.

Here are some venn diagrams of the simultaneity of the threads. You can see.... so... here.. this is the receive thread for the socket. It runs simultaneously. Not that interesting. What's more interesting is that the transaction validation thread can run simultaneously with itself, and also with the message handling. But not at the same time as the mempool commit. As we were saying, one thing I haven't looked at yet, is making the block processing simultaneous with the transaction commitment, that's work to be done.

Running out of time. Let me just move on to the optimizations that I did. There were a lot of optimizations to be done. I don't want to go over them all. I want to throw out this slide so that you can quickly look at them. A lot of this stuff doesn't matter when you have a 1 megabyte block. We had a transaction n squared processing in the blocks in all the Satoshi clients, but it was easy enough to fix. One to give an idea for optimizations, the most interesting one was this fast bloom filter. Let me hop forward and talk about this.

In one of the previous talks today you learned about a bloom filter. I don't have to go over that. One interesting thing about the bloom filter is that it has to execute a bunch of hash functions over the data. Running hash functions is very time consuming. So this bloom filter was I thought it was going to be fast or a faster way to determine which transactions had input conflicts. Turns out it wasn't. When examining the algorithm, I realized we don't need to run a hash filter to do a bloom filter in our particular situation because the txid is already essentially a hash of the transaction so it's... cryptographically random data. So why should we re-hash the hashed data? So from this observation comes the fast filter idea where we select arbitarry bits out of a txid and use that as the hashes for a bloom filter. And you know, if you use like power of 2 buffer size, things go even faster. And then, probably someone will say, this isn't a good idea because well an attacker can look at your txid and select or create specific txids that conflict with yours. But there's an easy solution to that, which is that each node, and this is one possible solution, which is that each node can choose arbitrary bits out of txid and that will stop any attacker. That's the sort of optimization that we did.

Since I am not even running the hashes in the bloom filter, this fast filter runs probably orders of magnitude faster. We didn't even test it. And that's it.

## Q&A

Q: How do I validate transactions if it's a gigablock?

A: You use SPV.

Q: How secure is that?

A: I don't think this is a talk about SPV. We're looking forward. We don't assume you are going to run a 5 year old computer. We're not going to use 1 gigabyte blocks tomorrow. The fact is that a relatively inexpensive computer can do it today.

Q: ....

A: Can you repeat the question? I didn't catch what you said.

Q: ....

A: Right.

Q: ... and you may want to re-spend... and I think.. 55% of the transactions... 0 ancestors.. So 45% have some ancestors or descendants? Was that in your case?

A: The transaction generators are python scripts which are managing their own wallets. We are not using the bitcoind wallets. If you try to generate 2k tx/sec with bitcoind wallet, you'll get 20 transactions/second really.

Q: .. parallelize acceptance... have all the non-descendants...

A: Actually, you know, because we had relatively few.. you know.. computers. We bumped the number of ancestors way up, maybe 3-4x more times than is normal.



