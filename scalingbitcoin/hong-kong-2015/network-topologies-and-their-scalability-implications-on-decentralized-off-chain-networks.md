---
title: Network Topologies and their scalability implications on decentralized off-chain networks
transcript_by: Bryan Bishop
tags:
  - lightning
speakers:
  - Joseph Poon
date: 2015-12-07
media: https://www.youtube.com/watch?v=fst1IK_mrng&t=1h29m38s
---
slides: <https://scalingbitcoin.org/hongkong2015/presentations/DAY2/1_layer2_3_poon.pdf>

LN transactions are real Bitcoin transactions. These are real zero-confirmation transactions. What's interesting is that the original idea behind Bitcoin was solving the double-spending problem. When you move off-chain and off-block, you sort of have this opposite situation where you use double-spends to your advantage, spending from the same output, except you have this global consensus of block but you have this local ordering that you use through this lightning system of penalties through which you can update the balances between two people. Through this system, there is no delegation of custody to a third-party, you don't put your money into some exchange or whatever.

By having a network of these payment channels, you can do atomic payments across these channels. This is functionally instant, like within a few seconds at most. If everyone is in the same room, you could probably do this in milliseconds, and this enables micropayments because you can update the state way more frequently than you can hit the blockchain.

Yesterday it seemed like a lot of people were talking about the idea of block size and what it really means. What got lost is what happens to Bitcoin long-term. What happens when the subsidy goes to zero long-term? Transaction fees could pay for miners. That's the idea, right? There might be alternative proposals, but most people in the room think that as block reward goes down from 25 to 12.5 all the way down close to 0, that as transaction volume go up, transaction fees could go up in aggregate, and that's how we will get security. If you are a miner, and you are a mining pool or whatever, the costs are dependent in your income is dependent on what the other miners are willing to do. If you are not willing to mine a low-value transaction, the other miner next door might be willing to. As a result, everyone is going to be willing to mine whatever they can. If you have gigabyte blocks, you are going to want to include as many transactions as possible as long as there is minimal orphan risk. If you have no constraints, fees will approach zero. The larger the block size is, the less aggregate fee the miner can get.

In the opposite direction, if you reduce block size to 100 kilobytes, fees might go up. The fees might be too large for all possible payments. Bitcoin today could probably pay for a cup of coffee, you could probably pay a 5 to 10 cents fee, and you could probably wait around for the transaction to happen. You could do it, it wouldn't be fun, but you could do it. With 100 kilobyte blocks, you probably couldn't use Bitcoin today. It would probably be more for long-term storage. When you have this dual tension when you need to enforce the security of the network, and the ability to use the system to store and withdraw, you are going to be reaching this local maximum. The long-term value of lightning is solving this long-term mining incentive, which is sort of at odds with each other.

When the fees start getting high, lightning still works. With higher fees to pay for mining security, we still need to make micropayments and payments. You can have extremely small blocks but everyone just moves it to a third-party custodian. You as a miner still don't make money because everyone moved to Coinbase or whatever, there would be no transactions there. With lightning, these are real bitcoin transactions. You are going to be making periodic on-chain payments, it's just significantly fewer. With a larger population, you can make real bitcoin payments. It enables a system using net settlement with many uses.

In long-term, this enables high security and high-volume transactions. This is the narrative that we need to think about when it comes to the block size debate. A lot of the issue is intrinsically linked to issues related to long-term viability of the incentive structures.

However, with lightning, we also need to think about desirable network topology. The core promise of bitcoin is decentralized payments. It would be sad if this had to become Visa or Mastercard or Unionpay. We all want the network to be decentralized. But I think the primary criteria should be more nuanced. You can say you want something, but you have to understand whether it will happen in an adversarial system, where businesses want to centralize the topology of the system. I think node incentive really matters with this. You need to understand the causes of centralization in order to design a good system.

This presentation is asking a system: are there significant network effects in having a hub-and-spoke model where there are intermedaries routing all the payments? Do the hubs provide significantly more value? Are there significant netowrk effects where if you are a hub operating another node, starts to become non-cost-competitive, so everyone wants to operate with that single entity... are they going to do that?

I think you can't stop highly-connected peers. There are power-law distributions. Highly connected networks are cheap and a function of transaction fees. Connectivity is cheap and it's easy for everyone to be connected to everyone within some low measure of degrees.

Is it more efficient to organize near single hub? How do you bootstrap a distributed system like this? How you bootstrap will have long-term effects on the topology of the system. Bram Cohen brought this to our attention. If you have a channel open, and you can pay over lightning; if you have a channel open and you can pay over lightning, it will be cheap and fast and instant you should do it. If someone is 2 hops away from you, do it. But on lightning day 1, how are you going to deploy? You're going to release a single hub? That's kind of messy.

However, another way to do it, and in my view a better way, is if you have no channels open, and you want to get on the lightning network. Then you just open a channel with someone, anyone, open a channel for 0.1 BTC or whatever for the initial payment that you wanted to make. Say you want to pay someone 0.01 BTC, then put 0.1 BTC in the channel maybe. They can continue to make payments in the future. Everyone, whatever they have currently, that's great, they can close out the channel whatever- even in the future. If Bob wants to send more money in the future, that's great. If Bob wants to route through me, great. If you can't route to someone, you just open up a channel with them. So the transactions might be higher early on, but that's fine because they are cheap right now. This will optimize for a very decentralized network. This makes bootstrapping easy.

We can bootstrap the Lightning Network by defaulting to opening channels instead of making regular bitcoin transactions.

What you're really doing is matching on-chain scalability with the transaction fee costs. As transaction fees get more expensive, you will want to be more efficient. You have this very very wide connectivity. That way, everywhere first and foremost is a dumb channel. Lightning is a nice bonus where it's preferred but not necessary, and that's a good short-term view of this, to encourage decentralization.

However, there is this incentive for people to say "well, let's operate a hub and dominate the network, no problem". Well, I think it's improbable that this will happen. You're not going to have one Visa. I think it's very very unlikely. It's borderline impossible. A huge factor of that deals with, in a hub and spoke model, you are going to have low velocity, which means the amount of funds transferred over something. The velocity of the US dollar is the funds moving back and forth depending on the money supply, and in this case, the money supply is locked up in channels. Functionally, if you have a system where you want to be a big guy, that means you are willing to have a lot of people connecting to you, you don't really know whether they are going ot transact with you. In the previous model, people are directly doing trade with each other. So you know they are having some measure of volume, and if you're not actually transacting, then you wouldn't be connected. In this hub model, you would opportunistically open channels iwth everyone, well you're going to have money that is essentially locked up and dead. As a hub, you need to put up a lot of money. So you need to put up a lot of money because if you presume, let's say you are Alice, you have a 1 BTC channel open, and let's say the hub has no money, they're like hey open channels with me, I am going to dominate the market as a hub or whatever, if you are Bob and Carol and whoever, and the hub isn't putting up any money into the new channels, how can Alice send money to Bob or Carol? When they want to send money to Bob or Alice, well with Carol, the hub's balance is zero and Carol's balance is high. The only way to push funds, in the hub topology, is if the hub puts up money. Then Alice would be able to push through the hub to Carol. This way it works. Money can flow when there's a star topology, but the center of the star has to put up a lot of money. As a hub, you need to put up a lot of money. And in that case, you need to deal with the issues of time value of money and velocity. When you have this topology, and you have this star topology, in this topology, let's say Alice doesn't do any more transactions and she goes on vacation and says whatever I'm doing other stuff, who cares... the hub just has a lot of money locked up. The velocity is incredibly low in this channel. What does your time value look like? The hub can only mitigate this by charging a monthly fee. But Alice might as well go do something else, instead of paying that monthly fee. And she might as well just connect directly to whoever she is transacting with. Money flows much more easily in that model.

It's unclear how things will play out. I think a single hub is unlikely. I think you would need to put up a lot of money. When you do that, you don't have enough BTC to just operate under this model. There are still cases where highly-connected star topologies would make sense, but I don't think there will be only one. Additionally, you wouldn't really know whether you know you are going to be a hub. There's no way to know whether you are routing from outside the star topology. Additionally, accepting more channel requests means less money velocity, so it might counter the network effects.

There are greater on-chain efficiencies, but higher off-chain costs, related to time value of money. We need to account for that there's implications for information leakage, so you might want to connect to more nodes and route that way.

Q: That was pretty interesting. One question I did have about what you mentioned in the beginning, about the over-arching of where Bitcoin should be in the long-term. What are your thoughts on, if miner rewards go to zero, and transaction fees don't go up-- what if miners are paid only by US dollar appreciation of BTC? So price should increase assuming the usage of bitcoin and demand will sort of static.

A: That's a possibility, but how many people do you see today mining at a loss?

Q: The price is where it is today, because miners are selling 50 BTC per block. If they can only sell 25 BTC per block, that it would maybe double. The price might appreciate.

A: That's a possibility. It's much better if it's still working if it's straight up zero. Yes it does take time to go down over time. The relative portion of block rewards to fees, fees are a larger portion. So I think for the security model of Bitcoin, I would expect fees would have to work in a more robust way.

Q: Suppose you have a network topology where in a part of the network there are two hubs in the same network subgraph. Now it is their primary business model to route other people's moneys. So they notice they have a bunch of links between each other, then they just try to merge together and they free up that money and can use it for other things. So isn't that sort of a centralizing force?

A: Not necessarily. If you have a system where users are willing to offer negative fees to free up money in different directions; the viewpoint is that there's a lot of traffic between these two large hubs, and when you have a lot of traffic between two large hubs, the assumption is a lot of directional flow, which would require a large balance. It would be ideal to minimize the directional flow between two hubs, and you can do this with rebalancing. The rebalancing needs to be robust to improve decentralization. If there was no rebalancing, then yes there are incentives along those lines.

Q: Will you assume that for the hub-and-spoke model, there's BTC locked up. But can those hubs close the channels? So how quickly can they close channels. So I don't see this is a factor that breaks it.

A: Say they close the channels and the users go somewhere else. If you are a large entity, it's presumpting an economic incentive where you are optimizing for your time value or whatever, when you're doing that, you are already selecting for transactions that are preferential and optimal in the network. Like when your users tend to transact with automotive users or something, so there's greater use of capital efficiency in that space. Someone in retail joins your network, incredibly low velocity, you kick them out. That's already a network segregating system where you already have clumps of money on the graph. I think that will happen, we're both in agreement. If the channels you're connected with aren't a good use of funds, yeah you should close that channel, and I think this creates a more decentralized graph.

Q: How do you incentivize the network to get the ideal network topology? How does it naturally happen?

A: Bootstrapping?

Q: How does it get to an optimal state? It may not be centrally planned, right?

A: Well, what would it look like if you have this design? If you design it where everyone optimistically connects to everyone early on, then you can bias towards decentralization even more.

Q: Each time the direction of payment changes. You have to reduce the lock time?

A: No. There was a paper (duplex payment channels). That one operates in that fashion. But in lightning, that's not the case. You don't actually need to reduce the locktime. With CSV, you can functionally run these with infinite time. You can leave them open for many years, if necessary.

Q: Open channel, then when your funds are being locked and so on, then you close the channel, and then reopen later. So the capital could be allocated in the most efficient manner. In the example you were giving,

A: Ah you mean the hub is poor?

Q: It's a matter of capital allocation. Faster channels would be more efficient than big channels. They still have to close and reopen channels.

A: Yes, I think that's similar to the other argument where money is locked up, and you just close up. And then reopen later? By doing that, as a function, I think that's a decentralizing force. I don't think the hub model will work. I think you will have somewhat supernodes, but I don't think you will have a centralizing hub, because you will kick off users. And that helps with decentralization. Yeah, it's not profitable to be a hub, that makes it decentralized, yeah. If you have this type of model, you're going to face the same problem where it is going to be deeply unprofitable use of allocation of capital. It's going to be biased towards a system where you are going to want to connect to people within your supply chain and your geographic area, to keep track of velocity of money and time value of money and so on.

Other lightning presentation from same day: <http://diyhpl.us/wiki/transcripts/scalingbitcoin/hong-kong/overview-of-bips-necessary-for-lightning/>
