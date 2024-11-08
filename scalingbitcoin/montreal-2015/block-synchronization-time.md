---
title: Initial Block Synchronization is Quadratic Time Complexity
transcript_by: Bryan Bishop
speakers:
  - Patrick Strateman
date: 2015-09-13
media: http://youtube.com/watch?v=TgjrS-BPWDQ&t=2h02m06s
---
slides: <http://strateman.ninja/initial_block_synchronization.pdf>

Block synchronization is how nodes join the market. New nodes download the blockchain and validate everything. This is how the security of the network works. Who is responsible for doing this? Everyone must be doing a full block synchronization. If you are not doing this, you're not on the bitcoin network. As a simple hypothesis, the block size growth is related to initial block synchronization as a simple function of the integral. There's a number of runtime complexities that are described here. Right now the actual network looks like this, it's roughly linear growth. This means that initial block synchronization is roughly quadratic time complexity right now, which looks like this. That's what we have today. That's not growth. This is on my very fast desktop machine, synchronizing from a peer that is on the LAN. This is on a raspberry pi 2, that's about 4 or 5 days of synchronizing and it didn't finish. It took another 4 or 5 days to finish for about 8 days total. These are rough simulation numbers. If the blockchain continues to grow linearly, but the total cost is dropping 20% annually, as you can see that's probably fine as long as you assume that we get a 20% annual capacity improvement. This is 20% growth in blockchain size and in capacity- again probably fine. But if we overshoot it, it's not okay. 20% annual increase in block size, but a 10% increase in capacity results in a huge blowup of total costs to synchronize, roughly 16x in about 10 or 20 years, at which point nobody can join the network. Oops, only the old nodes that were running the entire time can be synchronized. Okay, that's it.
