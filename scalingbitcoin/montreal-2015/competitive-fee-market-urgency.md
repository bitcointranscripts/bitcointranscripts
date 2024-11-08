---
title: Competitive Fee Market Urgency
transcript_by: Bryan Bishop
tags:
  - research
  - mining
  - fee-management
speakers:
  - Marshall Long
media: https://www.youtube.com/watch?v=TgjrS-BPWDQ&t=6843s
---
The urgency of a competitive fee market to ensure a scalable future

I am Marshall. I run Firehash. CTO Cryptsy also. Some people have higher cost, some people have lower cost. I think those were some good estimates for true costs. I am going to be talking about why fees are going to be very important very soon. We'll talk about what happens without fees, talk about why bitcoin really isn't free but how we can do things like microtransactions, real microtransactions, talk about the cost and talk about solutions.

So without fees, everyone knows that there's a lack of security. Miners are even today, and I'll go on to show why fees are really negligble for us, even at 10x what the current fees are, we don't care, it's not paying our bills. We'll dig into our own numbers. Even at 100x the fees still don't cut it. As these block halvings continue, we're getting into a really scary place where at the next block halving we have 50% of the hashrate get out. And the 2 week difficulty adjustment it's pretty bad. Everyone says that the fees are enough, well it's not.

((Fees aren't just for paying miners, it's for prioritization.))

This diagram is off of Peter R's paper. I apologize if this was your original equation. It outlines the revenue model where it takes into account propagation time, orphan rates, and this I thought to be almost exactly spot-on with my mining costs and a lot of my colleague's mining costs. Again Peter, walking in, sorry, if this is your equation, sorry. As everyone knows that propagation time can get wakey as block size goes up, then there's an orphan rate problem. We'll just kind of dig into some of the costs that we actually see. And then you'll see why this is important.

These charts are based on the current generation of mining gear. There's about 4 chips coming out for mining soon which will double these numbers. As you can see, the top axis is size of capacity in megawatts, the other axis is mostly revenue. These are true numbers. There's also the price of power every day. There's labor costs, ther'es factored in hardware amortization costs, build out costs, and a few other things like that. As you can see here, at even 3 cents you're not going to be profitable right off the bat, because yes gear is getting cheaper, but electricity is expensive, labor is expensive. Even at 5 megawatts right now you're almost at break-even.

Moving forward this gets a little better with next-generation gear. The actual chips that are coming out are going to be about 0.2 watts per gigahash. This is a nice average. It gets a little bit better. But we're coming to a technology cliff very quickly. Going down in node size helps, but there's not enough room to go down, ew're getting close to Moore's law issues. This is the scary part. Some of these will be released in October, these are based on real numbers, my data set will be online. You start to see this kind of graph where it really depends on your power cost, even if your power cost is almost free. At 3 cents it's pretty much almost free, what my company had to do was make strategic partnerships with government and colocation providers that give us free power in exchange for revenue share. This is why I feel there's a need for a fee market, because if we don't figure it out before summer 2016, these numbers get even worse because all of this is based on 25 BTC per block.

I'll be doing a discussion after lunch about these things. These graphs are from real hard numbers. They can only be fixed I think with a multitude of solutions, like lightning network which would be profitable for us, increased fees, but bitcoin is not free right now anyway. There are some cool things we can do moving on. Block size, everyone wants to talk about it. Block size has diminishing returns, as the block size gets bigger the other transactions don't have as much fee. One thing I find exciting is the idea of sharing mempools between pools, you can push transactions and then pay a monthly fee for free transactions. It does have some centralization problems but we're open to solutions. You can do zero transaction fees on the blockchain, but you can ... yeah I think petertodd is losing his mind right now.

There will be more miners at the Hong Kong event, next summer is going to get real really quickly.
