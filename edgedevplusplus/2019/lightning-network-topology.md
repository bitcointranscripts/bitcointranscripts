---
title: Lightning network topology, its creation and maintenance
transcript_by: Bryan Bishop
tags:
  - topology
  - lightning
  - routing
speakers:
  - Carla Kirk-Cohen
media: https://www.youtube.com/watch?v=j2l_Ut4k1qI
date: 2019-09-10
aliases:
  - /scalingbitcoin/tel-aviv-2019/edgedevplusplus/lightning-network-topology
---
# Introduction

Alright. Give me a second to test this. Alright. Antoine has taken you through the routing layer. I'm going to take you through what the lightning network looks like today. This is the current topology of the network and how this came about, and some approaches for maintaining the network and making the graph look like we want it to look.

# Lightning brief overview

There's ideally only two transactions involved in any lightning channel, the commitment transaction and the closure transaction. We want to make sure there's as few opens and closes on the chain as possible. We want to make sure the topology of the network enables routing so that we don't have to constantly keep opening and closing channels to make payments. It's really constraining when you're on the lightning network and you have to open a new channel to make a payment, and you end up clogging the chain anyway.

We open and close channels wisely.

# Public vs private channels

Public channels are known to the network, and announced on the gossip protocol using a channel announcement. This announcement is agreed by both of the nodes in the channel. They intend for people to route through it. This is very different from a private channel, which is not announced to the network. If you have a peer trying to announce a private protocol, you just don't sign the channel info and other clients won't route through it unless there's both signatures.

When we look at the topology of the network, we can only look at the public topology really unless someone else volunteers private data. It's kind of annoying because we want to see the really interesting things in the internet. It may be possible to deduce or infer information about private channels through hints.

There's also personal vs routing nodes. A public node or a routing node would set up some public channels and manage capital well, and hope to earn a lot of fees. Fees are very low in lightning but hopefully one day we can have higher nodes and running these nodes can be incentive-compatible. It would be great if people earned fees for running lightning nodes. I think with intelligent channel creation, you can definitely earn a lot more.

# Path finding and routing

We use source-based routing in the lightning network. However, you have a scarcity of funds. This means there's going to be a lot of failures through LN because nobody knows the funds. However, there is something you can do called a probing attack where you route payments through a specific edge and you fail it with a bad preimage but you route it through with various routes and the minute you hit a range where the payments stop going back to you or failing with a certain range, then you know that's the amount available in the channel. At the moment, it's possible to figure out balances even though we're trying to hide it. It can deanonymize things if you can trace balances through the network.

We optimize for fees and timelocks. There's a channel update message on the network. This is how we figure out how we're going to route.

# Topology matters

The current topology really matters. It affects the ease of path finding, the success of payments, and it influences fees. If you're poorly connected to the network, then you're probably going to be paying more fees. It also is related to the resilience of the network and it opens us up to topology analysis by surveillance companies if we're not careful.

# Topology overview

There's 5600 nodes, about 35218 public channels, and 959 public BTC sitting in those channels. I used the tool LNTopology found on github to run an analysis and figure out what the network looks like. At least the public network.

The diameter is defined as the shortest longest path. The longest path you can take in a network between any two nodes. In lightning, we're limited to 20 hops. We're presently at about 11. So we're well within the limit.

Extent is the other one which is longest shortest path, and this value in the lightning network is 6. This gives you a picture of the extent of the network.

I don't see why someone would want to drive up the diameter of the lightning network, but just creating two nodes and creating a very large chain at the edge of the graph. It would cost you a bit to do this, but again these are worst case metrics possibly produced by nodes not necessarily actual actors in the network.

A graph of the degree distribution shows that there's a small number of nodes with a ton of channels. This is indicative that we have a hub-and-spoke network. There's a collection of hubs. A hub is one big node that has a bunch of connections, and then the smaller nodes connect to the hub and they have fewer connections. This is fairly supported by the assortativity of the graph, which is a value between -1 and 1. This measures the tendency of nodes to connect to nodes with similar degrees. If it's a positive number, it means low degree nodes connect to high degree nodes (or is it the other way around).

# Topology creation

When LN first started out, the topology was achieved through manual connections. People connected with other people they knew. Then in 2017, lnd, one of the three main implementations, added something called autopilot which automates the way in which you connect to nodes. It worked based on preferential attachment where you would become more likely to connect to nodes that already have a lot of channels open and have liquidity. This drove the development of the hub-and-spoke network. At the time, it was intended for autopilot and the original commit said "we probably shouldn't do this but here's a first attempt at this". It has significantly influenced the network topology.

Also another aspect of topology/channel creation is liquidity providers. There are some companies that will open a channel to you, like Biig or Bitrefill, which will accept an out-of-band payment where if you pay them they will open up a channel with you providing liquidity. Only a few people were doing this; a lot of channels got opened up and now lnbig has 20-24% of the liquidity of the lightning network in their channels.

# Network maintenance

Maintenance is an interesting topic. There's a need to distinguish between channel health and network health. If you're running a node, you want to connect to people who are online a lot. If you're connected to offline nodes, then it becomes pretty unreasonable. You want to route and get fees.

Network health is about setting up a topology that is conducive to routing and resists network attacks, regardless of how healthy individual channels are.

Changing topology has a high cost. There would be at least 35,000 transactions on chain if the lightning network all channels were closed. So that's not really reasonable, and it doesn't make sense as a way to scale bitcoin of course. I think we need to open and close channels more wisely.

# Opening channels

The problem with manually opening channels is that people tend to deanonymize themselves and their node metadata. So this is straight deanonymization. People should be responsible for their own privacy, but we should provide a default for less-educated users.

The other issue is that lightning is a payments graph; it's not a social graph. There's really interesting work on the twitter and facebook social graphs but we don't really know what the graphs on lightning will tend to look like. You might not open a channel with your friend, but rather businesses you work with. You will probably perpetuate a hub-and-spoke network anyway because companies tend to have a power law about them.

Second degree preferential attachment is about connecting to nodes that are peers and are connected to the well-connected hubs. This will help receive better positioning in the network, but it's slightly better than just connecting to hubs exclusively.

# Graph metrics

c-lightning is looking at using graph metrics to inform open/close channel decisions. There's two categories: connections that go to the network as a whole, and then the one as you as a channel alone. There's one mode which is randomly connect, and another one that connects in a way to decrease the diameter of the graph. That's interesting because you can close the diameter. But it is a bit gameable, because someone can costlessly create a large diameter for the network. I'm sure we can get around this fairly easily, like have some sanity checks in there.

Another one is "betweenness centrality" which is good for a node that wants to maximize fees. You want to connect to nodes with high betweenness centrality. They tend to sit on a high amount of the shortest paths on the network. If you connect to such a node, then you will probably sit on many of the shortest paths as well.

Also preferential attachment is still an option.

# Node sorting

Another direction which takes a different approach is node scoring. There's something called "buzz scores" which are publicly released scores, but how they do it is not public. But you can make some guesses, like uptime is probably involved. Make sure your nodes are online. I think they do some basic probing to figure out who are the more balanced nodes on the network. I think they run some small probes every 2 weeks and they try to figure out who has more liquidity and they score them well because of this.

Again, this is potentially gameable, if you know what metrics they are using, then you can try to increase your score. But it's hard to see an attack here. You get a good score by behaving well. But maybe you can temporarily increase your performance while you get probed, but not sooner.

I think the mobile app currently uses this scoring list and is publicly available.

# Closing channels

I am pretty interested in closing channels. If you close a channel, you incur an on-chain fee and you potentially lock up your funds in a delay if you unilaterally close. Also, you have the opportunity cost of losing out on future routing fees. All of these are difficult things to think about as a person. I worked on a mainnet lightning integration and we had these channels that weren't doing anything. It's hard to pull the trigger on a channel because you want them to win, but you really have to cut your losses and do another channel somewhere else.

I worked on a system for scoring channels which will hopefully inform autopilot about making a decision when to close a channel. I looked at four dimensions.

Reliability: the uptime of the remote peer in the channel.

Success rate: HTLC success rates that the channel provides, versus the number of failures. Obviously, the failures could be further down the line, but maybe this is connected to a channel that keeps failing and then we should want to close that even though we're not the problem.

Profit/volume: this is based on fees earned and total amount moved through the channel. This needs to be calibrated to how much BTC you have in the channel.

Utility: how much personal use we get from a channel. This isn't particularly important for a routing node, but if you have a channel open and you make a payment every day to buy coffee or a beer or something, you don't want to close the channel just because there's no routing fees because your other options might cost more than running your own node.

# Conclusion

The lightning network seems to have a hub and spoke topology. Topology is really hard to change. It's expensive to change this.
