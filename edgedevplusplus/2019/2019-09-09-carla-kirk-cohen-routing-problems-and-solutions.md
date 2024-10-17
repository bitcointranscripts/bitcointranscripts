---
title: Routing Problems and Solutions
transcript_by: Caralie Chrisco
tags:
  - lightning
  - routing
speakers:
  - Carla Kirk-Cohen
date: 2019-09-09
media: https://youtu.be/1O-bhcbh9vE
aliases:
  - /'scalingbitcoin/tel-aviv-2019/edgedevplusplus/2019-09-09-carla-kirk-cohen-routing-problems-and-solutions'
---

## Introduction


I'm going to be talking about routing in the Lightning Network now. So I'm going to touch on how it's currently operating, some issues that you run into when you are routing, and then some potential expansions to the spec which are going to address some of these issues.

We ran through the Lightning Network graph: the nodes of vertices, the channels in this graph of edges. And at the moment, nodes need to keep this graph in memory so they can route quickly. If you store it in a database, it's going to slow you down very much. It's storing about 40 Mb, which is acceptable at the current state of the network, but we do expect this to grow. It's also required for routing. If you're a node in the Lightning Network you need to be able to route; that's the reason you joined the Lightning Network and you need to have this graph and all the information it contains so that you can do that.

## Channel announcements

We built the graph up with a set of messages, which are broadcast on the gossip protocol. So the first one that we use is something called channel announcements. A channel announcement is telling the network that a channel exists. There is one per node in the channel, a channel is between two parties at the moment, and so we broadcast two channel announcements. And what you need to do with this is prove that you own one of the keys in a 2-of-2 multisig in the transaction this channel is based on, and that you own one of the IDs of the nodes that this transaction claims to be, these two nodes that have claimed to open a channel with these transactions.

And furthermore, as I touched on earlier, these nodes need to agree on the announcement message. Both nodes need to sign both announcements. This is to make sure that no one broadcasts channels that are supposed to be private.

## Node announcements

The next message that we use is something called a node announcement. This is a bit more sort of miscellaneous; it allows you to add further information to the channel announcements, which contain your node pub key. We only take these into account, according to the spec, if these nodes already have a channel open. There's no point of you keeping track of a node if it doesn't have a channel open--it doesn't serve you at all, it has no purpose, and it's also a potential DoS vector--so (in that case) we just discard these messages and do not forward them in the network.

These messages also indicate nodes' willingness to accept inbound connections, so IPv4 or 6, or Tor addresses, which aren't really related to routing but it does provide you with some additional information.

And finally these announcements have a strictly increasing timestamp. So if we see a timestamp with an old node announcement, a node announcement that we've already seen a newer timestamp for, and we've seen all the timestamps, we assume something is wrong and we disconnect from this node because they shouldn't be behaving like this.

## Channel updates

And finally we look at channel updates. With node announcements and channel announcements we can build what the graph looks like. Channel updates allow us to change the values this graph has. So specifically, you can update your channel policy. This is the fees that you wish to receive for routing over this edge, which is a base fee per every single payment and then a fee paid per Satoshi thereafter.

And that's a bit of a difference to Bitcoin that people don't often realize when they start to look at Lightning, is that your fee does scale with the size of your transaction (meaning the Bitcoin size, not the kilobyte size), so that's a big difference.

This (the channel update) also contains the time-lock information that you wish to accept over this channel and the limits that you'll pay some HTLCs: the minimum amounts, the maximum amounts, and a total number of HTLCs you're willing to route through this channel. And these again are set per node in a channel, so a channel has direction--you can move funds back and forth between the two peers--and each node has the right to determine their own fees in their own time lock according to their risk preference.

These messages can also be used to keep your node alive. If you haven't done anything for two weeks, your tunnel will be pruned from the graph in most implementations, so you can send out one of these to keep alive. However, these messages are currently flooded and they make up a very large portion of network traffic, almost 40% last time I looked, which was about two months ago. This is generally because nodes are flipping online and offline a lot. So every time they come back online they send out a new channel update message to indicate what their current rates are, and this really clogs up the network a lot. It's a bit of an issue at the moment.

One of the first problems and one of the biggest problems we face in routing in the Lightning Network is that of unknown channel balances. We advertise in the channel announcement the capacity but not the balance. If I say I've got two Bitcoin in this channel, it might mean that all of it's on one side, and I can route outwards but I can't receive anything on that channel. It might all be on the other side, meaning that I can receive inwards but I cannot route outwards, or it might be balanced, meaning there is Bitcoin on both sides and I can route in either direction. And when you try to traverse an edge which doesn't have any Bitcoin in the direction that you're moving, you get a temporary channel failure on your payment. So this is when you calculate a route that includes that channel edge but it doesn't actually have any Bitcoin on the side that you're wishing to move across. And this means that your routing attempt will fail. So what a lot of the implementations do is they implement iterative routing. This means that you retry again, so you try to calculate a new route and either exclude that edge entirely from your graph, temporarily--you don't ban them for having unbalanced channels, you just take them out of this specific iteration--or you can intelligently decrement the chances of using that channel in a browsing algorithm. So there is both of those options, but the tradeoff you have here is that you have to run the pathfinding algorithm again, which I think for most implementations is a Dijkstra's algorithm, it's a pretty computationally expensive thing and leads to really bad UX if you're sort of constantly waiting for this route to succeed.

Another option that was brought up on the mailing list recently is to rebalance channels in reaction to these failures. So if you’re a node and you're routing a payment and it arrives and you actually do not have capacity, you can in that moment do what's called just-in-time routing, to make a circular payment back to yourself to make sure you actually have coins on that side. And while this in theory sounds like a really great idea, one of the problems is that you will incur fees making that circular payment back to yourself. You also need to have more than one channel. If it only has one channel you need to have a loop back to yourself to be able to rebalance, and the rebalance itself can fail, which further increases the amount of time the routing will take.

Another problem we have is that people have out-of-date channel updates. This means that you'll have an insufficient fee or time lock for a node, so if a node increases their fee and you have not received that message, then your payment is going to fail. However these updates do take about 10 to 15 minutes to propagate through the whole network because we use this really basic flooding mechanism, so nodes are fairly tolerant of you being out of date. However, a lot of the issue comes in when you restart a node that hasn't been online for a long time, and you get completely bombarded with these channel updates. Generally, if you're a mobile app--which is the kind of node which is open once in a while--you don't want to open it up and have to wait for a whole bunch of things to download and then make a payment. You want to open it up and pay; that's what you opened it up in the first place for.

So there are a few solutions here. The first is to re-query for updates, so when you receive a policy failure you'll know that you've got the fee or the time lock wrong or the number of HTLCs, so you can query for that specific node's update and then get it. However, this still has the issue where you do have to recalculate the route; you still have to get that information and then retry and delay the user experience further.

Another big one would be to have some gossip improvements. The spec has agreed to move to inventory-based gossip, which will be much more efficient in terms of bandwidth. I don't really see any big trade-offs right now; there's a very very basic flooding mechanism in the network, so switching over to inventory would be a really positive thing.

Another future problem for the Lightning Network is that of light client routing. We could see that the memory requirement for the graph grows too big if we end up with a very large network graph. We could face bandwidth constraints on very small nodes that don't want to sync up the whole graph or even parts of the graph. And we could struggle with route computations, so if the amount of computation required to iteratively route, which is a fairly likely situation--given that we do not disclose channel balances--that may become a bit overwhelming for light clients.

Some of the solutions and trade-offs there are here. The first one is to prune the graph, and I think this is pretty low-hanging fruit and there's a lot of space for optimization, especially with the current state of the network, which is a 40-megabyte graph. It is still pretty manageable as-is. So you can do so by removing small channels, already bad channels with nodes that aren't online; you just prune them from your network view and you forget about them. Or, you can use a more heuristics-based approach where you learn the expected neighborhoods where your node is likely to transact. People do have spending habits. Maybe you buy a coffee every day. Maybe you wake up and draw a picture on satoshi's place, if that is your thing. You can train your node to figure out where you're going to be routing. The trade-off here is that unexpected routes will fail, pretty likely, if you are pruning the graph very aggressively. If you suddenly buy your Bitcoin beer at a different place, you're not going to know what that side of the network looks like and you're going to be in trouble.

Another solution that people are starting to look at is the idea of offloading computation. So rather than light clients having to do all of this computation by themselves, they offload that to more resource-intensive clients who do that computation on their behalf in exchange for fees.

## Trampoline routing

So one of the ideas out there at the moment is something called trampoline routing and in this setup you have a light node who stores a subset of the graph including a set of trampoline nodes which I've got up here with three circles. The trampoline node has a much more extensive view of the graph so I've used this big gray bubble to express the Lightning Network because I don't have space on the slide. And so you can offload computation to the trampoline node if you know of the existence of one or two. So if the sender wants to send to recipients your route you need to figure out a route from the sender to the trampoline you then offload computation to the trampoline. You just tell them okay it needs to get to the recipient. then the trampoline is responsible for further pathfinding to the recipient. If this if this routing fails they then communicate that failure back to the trampoline it doesn't go all the way back to the recipient they would have to deal with it and the trampoline tries to route again and if they are successful there's time so you intuitively route and they succeed then they send that success all the way back to the sending node who's made a transaction.

We'll touch a lot in privacy about this. this is more that you're not necessarily gonna have that you don't want to just be opening up a channel with the trampoline. So you'll have a local view of the network. It's maybe got a few trampoline nodes and a few hops between yourself and those trampolines. That's kind of what 's trying to indicate that you will do some routing yourself. It'll just be much less because you're trying to reach this trampoline which will then do the vast majority of the robbing.

Audience Member Speaks.

Carla: No, I don't notice into necessarily okay so this is one of the proposals out there for trampolines is PR six five four on the bolts pacification and the way this works is that you do a regular trampoline regular onion to the trampoline which is that first half in the diagram. and this is the onion packet that looks like so it's got a type version, public key and one thousand three hundred bytes of hop-hop payloads.

And then you put the trampoline onion inside of the hot payload of the original onion in the last hop. The trampoline onion packet looks very similar to the original onion packet however it's got a much shorter hop payloads and you get 400 bytes of payload and these payloads are slightly different so they have the amount they have the node ID they have the time life delay but they also have what's called recipient features and these recipient features indicate what kind of recipient it is so whether or not the recipient supports trampoline or not. This is really important when we get down to routing to your recipient.

Alright so what would multiple trampolines look like if you have a graph set up here where send a wants to send to sender Zed and they aim to achieve this with two trampolines t1 and t2 on the image a would first construct a regular onion which is indicated by the white square which tells be throughout t1 and then inside of that regular onion they would put a trampoline onion which has these two further hops right? So the next hop is t2 which is the trampoline and the next hop is the recipient node which is dead.

So A would send us this onion to whoever has a look at this onion peels off the first layer and sends it to t1. Now he wants a trampoline note so it recognizes that there's a trampoline onion inside of the last half of this onion. So they say okay my next destination is t2 and I need to write to it so it now runs Dijkstra's algorithm or Dever path finding it has to build up a regular onion and that will have all the steps that this packet needs to reach t2 in the network.

It then also takes the remainder of the trampoline onion and puts it back inside of this regular onion. So we created a new onion and now we're going to route it again. This onion goes off on the Lightning Network and each node along the hop peels back the player and routes it onwards until eventually it reaches the second trampoline. This trampoline again understands that there is a trampoline onion packet inside of the regular packet whereas all the other nodes along the hub between t1 and t2 didn't need to know that. They're only concerned with the next hop along the way.

So they just look at the regular onion they see when they need to go and they send it with no problems but t2 gets this trampoline packet and has a look at the next hop in it and it sees the next hop is zed. Zed also got the recipient features set so that it knows it is not a trampoline node. So it now needs to convert this final hop in the network into a regular onion hop rather than putting the onion the trampoline packet back in the onion so it now computes the route to Zed which is just a single hop for a Y to route to Z and then sends a packet onto Y who sends a packet to Zed who receives the payment and observes absolutely no difference.

A problem here is that there is a privacy unique if Z is not a trampoline bug. Because the second trampoline knows that they are not the final destination because they had to convert it to a regular hop. If it was supporting trampoline they would just put that trampoline onion back inside of the regular onion and say could unwrap it and would know what the message was and there wouldn't be any privacy leak.

On that note moving on to some trade offs, the first is this potential privacy leak. If all recipient nerds support trampoline it would be fine and there are some things that we can do to get around this issue but if people aren't supplying trampoline this is a privacy leak for the recipient. However the degree to how bad this is you can debate the curse. We use sauce based routing so the sender already knows who the recipient is. There's just now one more party who knows who the recipient of the other's payment is and that's the final trampoline.

Another trade-off --

Audience Member speaks

Carla: Yeah so just as I understand this type of message, so I signal this feature to be a new feature, a new feature block that you negotiate

Another argument against trampoline routing, which I think is all right, is that if you use a trampoline you're not gonna learn about the network graph. Because when you fail, when you fail to make payments you can discount certain edges and learn where your routing wall and routing badly. I don't personally rate this one very highly as a bad trade-off because if you are using a trampoline you've really chosen to outsource routing. That's the trade-off you've made. If you do want to learn more about the network graph and run more efficiently, then you need to be able to support more of the graph.

Fee estimation is really tricky with this. You can have a lot of trampolines, you can have a lot of hoffstein trampolines and because you don't know what the network looks like you have no idea how many hops there are between your trampoline and your destination. It might be one, it might be 15. You're gonna have to give fees for the 15 cases even if it's actually one. This is bad for senders because it costs you so you're gonna have to have some maximum fee that you said but it's good for incentivizing trampolines. It's good for encouraging people to run these great trampoline nodes where they can clean up on fees because they've got really efficient routing, but nonetheless it is tricky and the final one which is a bit of a nasty one is capacity attack. Much like you do if you want to have pro balances in the network you can look up liquidity in the network by routing a payment through a very long path back to yourself and then just holding it there. At the moment this is limited by the number of hops that you have in an onion packet which is 20. An attacker right now would have to open up channels to do this but they can 20x their liquidity so if I have one Bitcoin I can lock up 20. Since trampoline allows you to create these multiple onions. if you have one Bitcoin you can lock up 60. So it allows that attack to scale a lot more. It's not entirely clear how we're going to address that at the moment. It isn't a tax service which really hasn't been exploited at all in the Lightning Network to my knowledge but if we do move into a sort of a competitive fee market where people are trying to outdo their competitors, locking up their liquidity with trampoline payments would be a good way to go.

## Rendezvous routing

Another way of routing that the SEC is currently looking at is something called rendezvous routing. This offloads commutation in a different way by splitting the pathfinding burden between the sender and the recipient. This also has great privacy improvements. What I would say one of the biggest motive key motivations for this proposal is is that right now when a routes to e a does know who the final node is whereas in rugby be routing also if E is using a private channel the way that you route to a node over a private channel is that they provide you an invoice with a hint. So if the last hop on this route is private it will just provide a hint indicating that they should route to D right? This still does leak your general location in the network graph which isn't great.

What rendezvous routing does is allow you to concatenate routes at a public round every point so say that's C is advertising around a viewpoint so this again will just be a feature that you said because you support this the recipient node e would take a look at C and calculate a route from C to itself and then it will put that route in an onion so regular routing packets. This onion would then go into an invoice potentially or just be communicated out-of-band and provide up to the person creating that send. They will have the ability to see the first hop in this route which is C so then just needs to computer out to see and then they can create an onion which goes to that rendezvous point into which the onion goes to the recipient. Then as we route, we start to unwrap the onion each point so begets the onion and then it's on to C and C knows that it needs to switch ephemeral keys at this point which is really interning relative so they can actually get the smaller rack the smaller onion out of the bigger one and then continue to write on te and some of the trade-offs here is that we lose a bit of spontaneity so if you want to receive on the Lightning Network and you first need a calculator path to yourself it means your invoices are pretty likely to have a bit more of a life a lifetime or lifespan limit so if you produce a route to yourself and then you send that invoice over three weeks later then maybe that route doesn't exist anymore and the invoices damned to fail because the channels don't exist and another one another big one is the trade-off between privacy and cost right so if you're sending to someone and you're using a rendezvous point you don't know where they are. They could be right next to you could have one or two help to get to them but because both of you are routing to this arbitrary point you might end up with ten hops and end up paying a lot of fees. That's kind of an inherent trait. You're not going to get around it if you don't know where if you don't want people to know where you are you're going to be difficult to find however you know this is kind of the sender paying for the recipients privacy which isn't great but yeah that's the way it is.

Yeah thank you. Questions?

## Q&A

Audience Member speaks
Carla: Oh no so if I have a channel open with someone and you're routing in this direction only I only I charge fees because it's my Bitcoin that's that's being potentially locked up okay so it's my liquidity that's being used and then if someone's routing to me then they earn the fees well said

Audience Member Speaks

Carla: At the moment you can do 20 ups and with travel you can do 60 in terms of the timeout it depends on the timeouts that the invoice has and the deltas across the route

Audience Member Speaks

Carla: I don't have any current defaults. I feel like you might.

Audience Member Speaks

Carla: I think some images have six out of six as default yeah yeah so I think I think there's a six block Delta default  in an invitation so long 20 hubs you're looking at a hundred twenty blocks so to 20 hours. Yeah I think that might be the default but then also the person that ends that route might have a minimum timeout, so it could be a lot more and you can control that timeout at the end of the route.

Carla: To my knowledge.

Great. Thank you
