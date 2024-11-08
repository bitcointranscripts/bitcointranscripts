---
title: Mechanism Design
transcript_by: Bryan Bishop
tags:
  - mining
  - incentives
speakers:
  - Matt Weinberg
---
-- Disclaimer --
1.  These are unpaid transcriptions, performed in real-time and in-person during the actual source presentation. Due to personal time constraints they are usually not reviewed against the source material once published. Errors are possible. If the original author/speaker or anyone else finds errors of substance, please email me at kanzure@gmail.com for corrections.

2.  I sometimes add annotations to the transcription text. These will always be denoted by a standard editor's note in parenthesis brackets ((like this)), or in a numbered footnote. I welcome feedback and discussion of these as well.
--/Disclaimer --

A mechanism designer's view of cryptocurrencies

Matt Weinberg (Princeton University)

We're going to go ahead and get started. This is the session on economics of mining. I put this session together at the last minute because I'm interested in the economic incentives behind these mining protocols. When we say mining, we might have other membership methods in mind other than just PoW. I would like to introduce Weinberg and he will give a talk about mechanism design as it applies to cryptocurrencies.

# Introduction

I have no idea how broad the audience is here, but I assume it's much broader than I am used to. I am trying to get a sense of what I'm going to get through this talk. The main points are the following. The focus should be on the design of cryptocurrency protocols. My background is in mechanism design, which means the entire talk will focus on design of cryptocurrencies.

I am going to be talking about deviations htat don't interfere with consensus; consensus is still going to work, but whoever launches the attack will get money that others wouldn't get. This is a long-term concern because it's an indirect threat to consensus even if the individual attack doesn't disrupt consensus immediatley.

The other distinction I would like to make is the kind of stuff that will come up in this talk, you will see stylized models and say hey that's missing some aspect of the model. That's intended, and that's by design. The point of this kind of research is to understand one aspect at a time really well. The point of the research I am going to talk about is not to design a working perfect implementation full, but to understand one part at a time and give advice ot people better at designing and engineering protocols. Everything you're going to see, the model is going to be missing something, but that's intended.

I want to represent my research community in economics and computation. We are different from the other research communities here. Obviously I am just one person in this community and I am not officially speaking on behalf of this community. These are just my opinions.

# Strategic attack

Imagine you're participating in something like Nakamoto consensus. There are some things you can't do, like forging transactions without breaking digital signatures. You can't retroactively change the contents of blocks without finding collisions in cryptographic hash functions. Just using cryptography, we can prove that unless you break cryptography, you can't do these things.

Using Nakamoto consensus as an example, when you create a block you can point to any block you want as a previous block it doesn't need to be the previous blokc. Also, you can hide blocks, selectively propagate them, and when you're including transactions you don't need to make it a full block, and you can include whatever set of transactions you want. It's not that we need cryptography to be better to resolve these problems, there's no hope of cryptography addressing these problems. You need to incentivize miners to behave in a certain way. You can't just force them to do it with cryptography.

I am not going to be talking about eclipse attacks, network partition attacks, or any problems with latency which you usually see in distributed computing. I just want to isolate one thing at a time.

# Outline

I'll try to give a brief overview of several topics. I'm happy to offline talk forever about any of these topics. The sampling of topics is biased towards my own research because that's what I know best and can present better. I won't read through the list, but these are representative topics.

Kiayias/Koutsoupias/Kyropoloou,/Teselekousins 2016 in defining a mining game, selfish mining, and a bunch of others slide went by too fast.

# A blockchain mining game

I am going to present a mathematical model and then make some true statements. I wnat to show you the process of writing an EC paper. I want to create a game and claim that it does a good job of capturing miner incentives when they incent..... when you create a node, you can add a directed edge to any node in your graph. You don't have to follow the longest chain, but you can point to whatever block you want. In any timestep, you can broadcast any of the nodes you have created or you are aware of, but you don't have to broadcast them to the peers there's nothing forcing you to do that. The payoff is that, the payoff is that the limit of steps as it goes to infinity of fraction of blocks in the longest chain created by m. This is a description of the game.

Some important points about this. That's the game. What are the modeling assumptions I made going in? Which ones do I consider significant and not significant? One thing I did is that I said timesteps are discrete and every timestep someone is finding a block. We all know that's not how PoW works, it's instead found by an exponential distribution. I'm abstracting that away and saying I don't think it matters for the model. I also abstracted away broadcasting. When I define the payoffs, I want to note that this is assuming that the players are trying to maximize the bitcoin they get per unit time. It also assumes the transaction fees are zero.

For things like abstracting the exponential time defined blocks, it makes the math and model easier to analyze and write it down. But I don't think it effects the qualitative conclusions you can draw from the model. Mathematically it's a little bit different but it seems like I am going to get the same conclusions. Also, for abstracting away point-to-point communication and latency and yes you should care about latency for distributed computing but from the perspective of incentives I don't think latency plays a huge role. For the last assumption, this one I think is different... when I say that I'm assuming that players are trying to maximize their BTC per unit time and no transaction fees, I think that's significant. It assumes that the bitcoin/USD exchange rate is what economists would call exogeneous. If I'm mining, I'm not affecting the value of bitcoin and I'm just maximizing the amount of bitcoin I am getting. But I think this assumption could be legitimately challenged. I don't think it's a huge deal to say that transaction fees are zero when they are really very small; or it might be an issue to say the transaction fees are zero when you are incented entirely by transaction fees.

I think having a valuable insight into designing incentive-compatible cryptocurrencies, but I also think future work should examine when exchange rates are indogenous instead of endogenous, and when the transaction fees are the entirety of the incentive.

If there are no questions on parsing this model, then I will state some results.

Q: So you said some parties on the last point, that they are omaximizing the number of bitcoin you get. But in this model, they maximize relative bitcoin they get compared to the other parts of the network.

A: This is bitcoin per unit time. In bitcoin, there is difficulty adjustment. The longer chain grows by 2048 blocks every 2 weeks. So if you're using some strategy that makes a lot of blocks or they aren't in the longest chain, or you can cause other people to make blocks that aren't in the longest chain, then you effect the time it takes for others to make new blocks. The length of the longest chain is proportional to time. If you want to maximize bitcoin per unit time, you want to maximize the blocks in the longest chain per the size of the longest chain. So that's what I'm claiming here.

Q: You qualified the exogenous assumption, but I still want to double click on it. Fundamentally, if I succeed in attacking bitcoin or ethereum network slightly, then you ... can compute whether it was worthwhile to mount this attack and how much it cost. If I really succeed, then the real protection is that I am going to hurt myself and devalue the coin to such an extent that I don't get to extract any real value. This is inherent in any model.

A: I think that's an example of, I'm not the right person to answer that question. The question was that there's a difference between effecting the currency a little bit or the exchange rate, versus something where you do so much selfish mining that the currency is now worthless. I would say that mechanism design is not the right way to approach that. Classical distributed systems are already doing a good job of thinking about those problems.

# Longest chain protocol

Let me give some quick sanity stuff. If you want to do a sanity check if you want to confirm what the model is, this is what the longest chain protocol would be in that language. In Nakamoto's first paper, there was some intuition that if all of the miners followed the longest protocol, ... then it is to follow the longest chain protocol. That's the reasonable conclusion that most people drew and believed for a long time. There was even this correct random walk analysis in the paper, that said there's a specific strategy that wont work if you have less than some chunk of the computational power. This is roughly around the time that got me interested in cryptocurrency was this big result from Eyal/Sirer 2014 that said there's a selfish mining attack where you can take 1/3rd of the hashrate. If everyone else is following the longest-chain protocol then you can do better than that yourself if you don't follow it.

So the main idea is that when you create a block, you should hide it. Myabe you get lucky and you mine two rounds in a row; now that you have this private chain of length 2 you can use this to guarantee you are in the longest chain and cancel other blocks that other miners are creating. You might get unlucky, and maybe you don't mine in the next round and you lose out and that's bad. But it turns out that the expected gain is more than the expected loss when you have more than 1/3rd hashrate. If you are able to predict the future better, and you knew that your next round is more accurate or more likely, then oyu mitigate the expected loss. The second one I want to emphasize is that the expected loss comes from losing the rewards in the block you're creating, and both of these things will come up when I dash through other stuff.

There was some follow-up work to selfish mining 2016. There was SSZ 2016 and KKKT 2016. With 30%, you can make the same claim-- if every other miner is using longest chain in this game and you have less than some amount of mining power, then oyur best -- is to use longest chain. So it mitigates some of the damage caused by selfish mining.

According to one of the coauthors, selfish mining hasn't been detected on bitcoin but it has been detected on smaller altcoins. Why is it the case that it hasn't been detected on bitcoin? One reason might be that no single miner has more than 30% of the hashrate. There might be periods of time where that was false for bitcoin. My best guess is that the dollar to bitcoin exchange rate is not indogenous... or maybe selfish mining would hurt the value of bitcoin and they didn't do it. Or maybe it would discourage someone with 40% of the hashrate to selfish mine, but what would happen if a miner would be able to short sell bitcoin? Currently you can't do something like that because LedgerX doesn't exist, but in the future that might change. The value of this research is to understand why it is the case on one currency you see it and on bitcoin you don't? And if should things change in the fuutre, what should you be looking out for?

# Transaction fees

I don't think I have enough time to go through everything that I wanted to say. I'm going to state a few results of block reward vs transaction fees. It's a hotly debated topic. One result that might not be super clear since I didn't get to build up the model, but in the case where transaction fees become dominant instead of block rewards as the incentive, this was work of Carlsten/Kalodner/Narayanan 2016. We showed that the incentive issues are way more complex for transaction fees than block rewards. The rough intuition is that when you're rewarded by transaction fees, it's possible that you're going to mine a block that wasn't worth all that much, so if you happen to mine it, then you might as well hide it and try to selfish mine because the cost is low. The incentives are very different, and that's one reason why.

# Proof-of-stake

One last point about the difference between PoS and PoW. Where is the source of randomness coming from? For PoW, I think about somehow there's this magic external source of randomness which has nice properties, which is that who happens to be the next miner to invert the hash function. It turns out it's hard to get that kind of pure randomness using the cryptocurrency as a source of randomness. The main result I want to take away here is that, I mentioned that if somehow your randomness had the property that you could predict in the future how accurately you are to be the next miner, then you could do selfish mining even better. So you can withhold your block if there's a way to know you're likely to be the next winning miner. There's a thoerem that says any ... is more vulnerable to selfish mining than the PoS counterparts.

# Economics of bitcoin mining

If a miner has a electricity costs 20% lower, then either it is not profitable for the competitor to not mine, or .... some other option that the slide moved too fast.

# Takeaways

The fact that people are here means that people understand incentives are important. They should not replace classic distributed systems naalysis, but we should also do mechanism design style analysis. Our community tends to focus on consulting vs engineering. We try to write one paper that understands one aspect very well; what this means is that every paper has something unrealistic about the model but that's by design because we need to understand that one aspect really well.

We should think of the goal of this research as, we should think about new protocols before they are deployed, or circumstances bfeore they are changed. Maybe for a given-- for a specific protocol and time, of course doing specific analysis that that protocol at that time is going to be more useful.






