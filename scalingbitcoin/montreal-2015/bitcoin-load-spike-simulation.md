---
title: Bitcoin Load Spike Simulation
transcript_by: Bryan Bishop
tags:
  - research
speakers:
  - Conner Fromknecht
  - Nathan Wilcox
---
Our goal for this project, our rationale of what we're interesting is when many transactions arrive in a short period of time. This could be because of denial of service attacks where few entities are creating a large number of transactions, or many people wanting to create transactions, like a shopping spree. We wanted to answer two questions, how does the temporary spike in transaction rate affect confirmation delay distribution? For a given spike shape, can we change the block size and how would that effect the evolution of the system?

Our simulation is based on ... stoachastic simulation "bitcoin\_load\_spike". Based on bitcoin traffic bulletin #34 simulation. Our mempool model was an infinite FIFO queue (no fees/priority). They are appended to the mempool. We used transactions that were 250 bytes. The main way that our model differs from the bitcoin traffic bulletin is that our block size is variable, we can adjust it, and provide spike profiles, we have this time-varying spike so we can model that in the simulation so that we have different loads during different points in our simulation. We can log the confirmation times for each one of our spikes.

<https://github.com/cfromknecth/bitcoin_load_spike>

<http://hashingit.com/analysis/34-bitcoin-traffic-bulletin>

We varry the poisson distribution rate in that step function.

Traffic Bulletin results: an s-curve showing the cumulative effect of the transactions. You see that across the graph, there is separation increases with the increase in load. The farmost left curve terminates at 380 seconds, at 5 or 6 minutes, which is what you expect from an essentially empty network. The purple plot is about 10k seconds per transaction, so you can see the huge increase just based on the load of the network. On the right, 100% transaction rate means that in this model 3.5 transactions/second, which is proportional to the block size and how large transactions are, another thing to point out is the time scale on the x-axis is logarithmic even though the s-curves all have the same shape, the tails are a lot worse as the loads get high. It could be the case that 20% of transactions have to wait over 3 hours or something like that once the load is high enough. This is the result from bitcoin traffic bulletin that we're trying to extend.

So we don't have results that we felt comfortable sharing because we think we have bugs. So sadly we have this sketch of what we could imagine, hopefully you can tell us if you would like to see these results and whether they would be useful. We wanted a time series plot showing the rate jump up in the square wave. We expect that if we plot the mempool size over time and smooth that, it would look like what you see here. The mempool size would grow over time. And then we we expect the mempool to drain over time after the spike ends. In a fictional universe, that should occur..... How long is that hump? How long does it take the memory pool to drain? We would be interested at each of these arrows to create another distribution plot like the one from the original model.

The original simulation, you fixed the block size based on transaction rate; we can model spikes that are 10's of thousands of times higher, and see the network response to that, instead of just fixing a rate just above the network capacity because then you have an infinite queue that continues to grow.

The next step is to imagine a different block size and see how that changes the length of this curve. So this is something we need further work on, one thing we need to do is more background work. This seems like a fairly simple problem or model that would probably exist elsewhere, and the history of router design evolution and we're not that familiar with queuing theory, this was sort of like a weekend project to discover it for ourselves. There is probably other work that is not specific to bitcoin. There are many firehoses on the net about information about bitcoin.

As for future work, given that the general philosophy or the outcome of the simulation are related to events and queuing theory, it could handle more cases, get more accurate simulations for the bitcoin network. We would like to compare against previous transaction rates to compare how our load spike simulation fits real data that we see in history. And the second way is that we want to expand our simulation to include things like transaction loss, as well as replace-by-fee which is a reorder of transactions in a queue, and fees are not taken into account by the simulator. Expanding on those would give us more accurate results for the simulation.

Queue reordering and things like that, it's my personal interest with this project because there's been a lot of discussion about both of these topics, but some people are focused on for the standard operation of the network how much load can it handle, but there's also the exceptional case of denial-of-service attacks or shopping sprees, and I'm particularly interested in learning more about the mechanics between user behavior and miners, or wallets and miners and full nodes.
