---
title: On the Security and Performance of Proof of Work Blockchains
transcript_by: Bryan Bishop
tags:
  - research
  - security-problems
  - security-enhancements
  - ethereum
speakers:
  - Arthur Gervais
date: 2016-10-09
media: https://www.youtube.com/watch?v=_Z0ID-0DOnc&t=8857s
---
<https://twitter.com/kanzure/status/785066988532068352>

As most of you might know, in bitcoin and blockchains, the information is very important. Every node should receive the blocks in the network. Increase latency and risk network partition. If individual peers do not get the information, they could be victims of selfish mining and so on. Multiple blockchains has been proposed, multiple reparameterizations like litecoin, dogecoin, ethereum and others. One of the key changes they did was the block interval time. Bitcoin has 10 minutes. Litecoin has 2.5 minutes. Dogecoin has 1 minute. One common misunderstanding is that-- ethereum uses the GHOST rule for its blockchain. For the difficulty calculation, it uses the longest chain. From a security perspective, we argue it's exactly the same as bitcoin. These are basically blockchains that we see out there and we would like to understand better how to compare these.

If you have a faster block generation time, you get faster payments. If you get a bigger block size, you have more payments you can push through the blockchain. To give you some numbers, we have the medium block propagation time of about 8.7 seconds. This has been measured for several years now. For litecoin, it's under 1 second slightly, and for ethereum it's about half a second. There's a strong correlation to block size. There's also propagation time.

In this talk, I would like to show you two things that we have been working on. First it's a quantified framework that allows us to compare the security provisions of these different blockchain and to see which is more secure. We analyze two pillars of blockchain security, one is double spending and the other one is .... and in ordr to have the adversary model be strong, we pick the best strategy. Number of secure confirmations to a merchant, and this depends on the transaction value that the merchant is accepting. Based on our analyzer, we can also increase the throughput without penalizing the security. The second contribution is an open-source bitcoin blockchain simulator and any re-parameterization of bitcoin. It scales to thousands of nodes. It's open-source and documented.

As most of you know, a blockchain is a chain of blocks. At times, miners might find competing blocks (stale blocks). Stale blocks should be treated as lost effort. The honest network is trying to sync, and there are inefficiencies here. To an adversary that is mining at the same time on its private chain, it would not have the same inefficiencies as the honest network. The adversary can outrun the honest network there.

((Stale block rates for different blockchains goes here))

Double spending is a process where an adversary tries to fraud a merchant. Let's assume here that the merchant accepts a one block confirmation transaction. An adversary will mine another transaction in another block and publish the secret chain in order to publish the double spend.

Selfish mining, proposed by Eyal and Sirer. This is a technique where instead of publishing a block, you keep it private. You only release a block to compete with other miners. This forces other miners to perform wasteful computations because they don't know you're already ahead. The adversary loses block rewards because they are basically gambling that some of his blocks might not be accepted.

Selfish mining and double spending are two different attacks. One observation we have is that in selfish mining you increase your relative rewards, and this might not necessarily be a rational strategy. If the difficulty of the blockchain is constant, in particular. And in double spending, it's a rational economic actor.

Qualitatively, this is easy to explain and everyone knows that if we make blockchain generation faster, we have more payments available and less security. If we make blockchain bigger, we have low propagation of blocks, and this slows down everything. What are the results of these reparameterizations?

We propose a framework with two components. The first one is a proof of blockchain, it's instantiated with different consensus parameters like block interval time and network parameters. It uses as an output the state of the blockchain, block propagation times and throughput. On the right side we have a security model, we input security parameters such as the adversarial mining rate, and then it gives out the optimal adversarial strategy and security characteristics.

Let's look at the proof-of-work blockchain. It can be any real deployed network that we have today out there. It can also be a simulated blockchain. We implemented a simulator. Our simulator kept different consensus and network layer parameters. The network consensus parameters are mining power distribution, for example. Geographic distribution of miners and nodes. About 70% of the miners are now in Asia-Pacific these days. You can play around with these geographic parameters. We also allow to change the number of connections of the miners and so on. We support the normal getdata block push, accept headers propagation mechanism, and we also implemented Matt Corallo network and also block propagation improvements, and a test case for a torrent-like approach for block propagation.

The security model on the other side is a model where we captured optimal adversarial strategies for selfish mining and double spending, separatey. This is based on markov decision process. The input to our security models are the following points, like hte adversarial mining power proportions, we get its input from the blockchain and we get the stale rate to quantify the inefficiency of the blockchain. We capture the connectivity and bandwidth of the adversary. W also take into account the impact of eclipse attacks, and a few other things.

Markov decision process is an extension of markov chains. We add actions. We have a state space and an action space. The adversary has 3 blocks that he is mining in secret, so selfish mining. He has a secret chain. Honest network has 1 block. So the state is 3:1 because 3 blocks for the adversary and 1 block for the honest chain. If the adversary chooses to publish his blocks, we call this an override action because he's overriding the honest chain and he gets a reward of 2 blok rewards. If the honest network adopts the chain, then the state changes to 1:1 because the network has adopted it. Refer to our paper that has the full details on the MVP.

So what about our findings? Regarding comparison between for example ethereum and bitcoin; how does the security compare? Ethereum has a stale block rate of 6.8% and bitcoin has 0.41% stale block rate. Ethereum has smaller block rewards and a higher stale block rate. Given our model, we find that for double spending and with an adversary with 30% hashrate, we need 37 block confirmations in ethereum in order to match the security of 6 block confirmations in bitcoin. This is 12.4 minutes versus 60 minutes on average. Litecoin would require 28, and dogecoin would require 47 block confirmations.

How can we increase the throughput? Based on our simulator, we find that if we set the block size to 1 megabyte and 1 minute block interval, we do not penalize block propagation. The security is not substantially impacted. You can go to roughly 7 tps to 60 tps without sacrificing security.

What about selfish mining? We consider selfish mining under constant difficulty-- this is a limitation of our work. If you consider a 30% selfihs miner with mining 209 blocks, instead of 300. Under our optimal strategy, the adversary gets less blocks. So it increases the relative shares of blocks, but gives you a less absolute block portion.

What about the influence of stale block rate on selfish mining? The higher the stale block rate, the higher the relative revenue. We have two hashrates-- one with 10% and one with 30% for two adversaries.

What about double spending? We can see that the probability-- profitability of the adversary depends highly on the transaction value. As we consider a rational adversary, an economically rational adversary, and therefore we quantify the resilience using a minimum double spend value, so if the double spending is profitable then the adversary will choose to double spend, and if not then he will honestly mine. So this is a threshold that tells you when double spending is more profitable than honest mining. So we again have two adversaries, one with 10% hashrate and one with 30% hashrate. Everything below is safe, and everything above the adversary has an incentive to double spend. From this data, we can basically quantify how many confirmations we need. For six confirmations in bitcoin, we are quite safe, with a transation of say 100k, until the adversary has about 30% of hashrate.

Double spending in bitcoin vs ethereum. I gave you some data points at the beginning, but this is the whole picture. On the x-axis, you can see the adversarial mining power. On the other axis, you can see double spending in block reward. On the right y-axis, you can see the double spending in US dollars. So different blockhains have different block rewards in US dollars. So first let's look at the first...not the dotted lines. You can see the blue and the red ones is bitcoin and ethereum with 6 block confirmations. They are pretty similar. Ethereum uses uniform tie breaking, once a node gets two blocks, it will choose uniformly one of them to continue the chain on, rather than the first seen block. So ethereum is slightly less secure here. If we look at the dotted lines which are translated to US dollar value, we can see that for 6 confirmations of ethereum and 6 confirmations of bitcoin, bitcoin is at all times more secure than ethereum. If you look at ethereum the green dotted line at 12 confirmations and bitcoin with 6 confirmations, you can see there's an intersection at about 11-12% adversarial hashrate. So these two blockchains have the same security at that point. At 11% of the hashrate, bitcoin and ethereum at 6 and respectively 12 block confirmations. It depends on the adversary.

We propose a quantitative framework to compare blockchains. We need to quantify these to propose better systems. Selfish mining is not always rational, and double spending is an economically rational strategy.

# Q&A

Q: Just curious if you've tried to do any work extending your analysis to look at blockchain structures like bitcoin-ng or bizcoin. How do these effect those alternative structures?

A: We have not included that. We only looked at reparameterizations. Bitcoin-ng is quite different. We don't capture that.

Q: For selfish-mining, you were assuming a constant difficulty. I thought the idea was that you push the difficulty down and then you get more proportion.

A: As I said, this is a limitation of our work. We don't consider difficulty changes in our security model. In bitcoin, if you were doing a double spending. The difficulty adjusts every few weeks. So if you were double spending, so the double spend will happen within 2 weeks. So constant difficulty is realistic. However, in ethereum, the difficulty is adjusted every block.

Q: Great simulation effort. I made a simulation environment in 2014. TCP packet disordering and delay is difficult.

A: We do not simulate congestion control for TCP. What we do however measure and simulate is the individual bandwidth in different nodes and the difference in upload and download in latency, across the world. So this is captured.

# References

<https://arthurgervais.github.io/Bitcoin-Simulation/index.html>

paper <https://eprint.iacr.org/2016/555.pdf>
