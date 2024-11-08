---
title: 'Flare: An Approach to Routing in Lightning Network'
transcript_by: Bryan Bishop
tags:
  - research
  - lightning
  - routing
speakers:
  - Pavel Prihodko
date: 2016-10-08
media: https://www.youtube.com/watch?v=Gzg_u9gHc5Q&t=1680s
---
<https://twitter.com/kanzure/status/784745976170999810>

I will not be as technical as Olaoluwa was. You have nodes that open up payment channels. This scheme is actually developed at the moment in great detail. So how do you find the channels through which to send payments? So we wanted to propose some initial solution to this.

## Routing requirements

It should be source routing because we need the privacy. When a user sends a payment, so the decision of what route to choose should be on the sender side, because if he delegates it to an intermediate node then they don't have the necessity to privacy as much. The other aspect is trustlessness. When the payment is sent from a-- nobody should be able to see who sent it and from where it is going it. The payment should also be quite fast. In minutes, or maybe even seconds for the payment to occur.

## Routing

We wrote a <a href="http://bitfury.com/content/5-white-papers-research/whitepaper_flare_an_approach_to_routing_in_lightning_network_7_7_2016.pdf">whitepaper</a> where you can read more details about Flare.

## Core idea

The state of lightning network can be split into two distinct components. One is payment channels and the other is the total capacity of channels. We assume channels might last for days or weeks. We can think of this information as static. The other kind of information is the status of nodes, whether they are online or not. The distribution of funds in the channel--- the distribution might change.

## Flare design

Proactive part (on schedule) is gathering static information, like store open channels.

Reactive part (on payment request); gather dynamic information, ask funds, fees, status. Find path based on both.

## Proactive part

Obviously if your network is small, there's no problem to just broadcast information so that each node receives the same information. But if the network gets bigger, this decision just doesn't scale. It might work for hundreds or thousands, but if you assume 5000 lightning nodes or the number of bitcoin "SPV" nodes, then this wouldn't work.

So we came up with another idea where each node -- knows about its neighborhood but it also in a way quite similar to the way how DHT works -- it finds some paths through some distance nodes using beacons.

## Beacons

Each node finds a path to nodes whose addresses are closest to the one's claiming to them to be beacons. When someone wants to send money, he will note that a node was looking. If he does not know the path through the nodes he wants to send the money through, but he does know some addresses, there is a likelihood increase that this node knows a node that passes through this one.

## Routing table

((missed this section))

## Reactive

When node E wants to send money to D, E and D find path candidates on the graph of their routing table. You have to find candidates. So then you do some shortest path things. You find various paths short as possible... it's not sufficient to find just one path because we know, because this information needs to be the total capacity of roads, so we may find that on the one path that we can't send the money because of route fund exhaustion. So we need to find as many routes as possible.

## Disjoint paths

There might be some update to this scheme when we want to increase.... not only trying to find the shortest path, but also in poor conditions that this path would resemble the most different path possible. Suppose we introduce some weights penalizing us from taking the usual path.

If no candidates are found E requests tables from nodes whose addresses are closest to D and so on. When several candidates are found, E collects dynamic information on them. If the one is found, E creates HTLC and sends money to D.

## Dynamic data

But how do we know which candidates to check first? Need ranking. The funds on the side of the channel that we want to send-- they are somewhere between zero and ... if we know nothing about the current distribution, then it makes to sense to assume it's uniformly random distribution. One can estimate the probability that a channel would be able to support this, using a probability that a payment will make it through a channel. It's a probability that the channel would be capable to route that payment. It's multiplication of each channel able to process a payment. After we get the probabilities we can start sending probes through the candidates with highest chance of success.

## Implementations

<https://github.com/lightningnetwork/lnd>

<https://github.com/ACINQ/eclair>

## Topology of LN

I wanted to show some test results. Inside Bitfury, we experimented on 100,000 nodes. We have a simulated environment. We discovered that... different graphs; I think they also, run some simulation on 2,500 nodes with lightning client. The tricky thing is that if you want to measure performance then we need some realistic topology for lightning network. The problem is that at the moment nobody knows.


paper <http://bitfury.com/content/5-white-papers-research/whitepaper_flare_an_approach_to_routing_in_lightning_network_7_7_2016.pdf>
