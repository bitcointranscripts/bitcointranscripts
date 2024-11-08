---
title: Security Aspects of Lightning Network Routing
transcript_by: Bryan Bishop
tags:
  - routing
  - lightning
  - lnd
  - security
speakers:
  - Joost Jager
media: https://www.youtube.com/watch?v=Q9w9VCOrego
---
D146 D0F6 8939 4362 68FA 9A13 0E26 BB61 B76C 4D3A

<https://twitter.com/kanzure/status/1137740282139676672>

## Introduction

Together with my colleagues I am building lnd. It's one of the implementations of lightning. In routing, there's the sender of the payment, the intermediate routing nodes that forward payments, and a receiver. I would like to scope this down to looking at security just from the perspective of the sender.

## Goals of LN

Why are we doing all of this? The thing we're looking to get to is a mobile app where you scan a QR code, you confirm the payment, you can have a slight delay no problem but you want the payment to be sent successfully every single time within seconds. There's nothing much more to it. Ideally you want a short delay. The payment speed is determined by the speed of nodes and network connections and routing path length. I will give a brief overview of how intermediate nodes get paid.

## Delayed failed payments

Sometimes you see a spinner and it keeps spinning and then after one minute it shows you that the payment timed out. This means one or multiple attempts have been made to make the payment. In the end, the payment didn't happen. All the routes tried didn't work out. There's sometimes a timeout of like one minute and then you give up, and you didn't pay. However, what could also happen is that you get the screen not after one minute but after days. What happens if you have a long route is that you lock your HTLC to a large number of blocks like 100s and if somewhere along the route then some node might not cooperate and hold on to the HTLC and during that whole time you don't know what happened; did the payment arrive at the sender or has it not arrived yet? This is difficult to explain to people because they expect the payment to work immediately or go directly and they don't expect this in-between state for a long time. A malicious node along the path can deny and delay payments from the neighbor node. So a bad node can fail any payment. On the way back, a bad actor can decide to delay as long as possible.

## Delayed successful payments

If it always failed, then it wouldn't be a big deal because you could get your money back. But a node can delay your settlement, and after a few days of waiting you can get a new payment sent notification. You could accidentally pay twice because maybe the recipient sent you another payment request in the mean time that you also paid. In this situation, you have to rely on the receiver to be friendly and to return your payment. He can delay on the way there or on the way back, like the sender might not learn that the payment went through in time before he makes another payment even if it really did go through. He could learn through another channel but LN can be arbitrarily delayed.

## Defense

We can defend against this. We look for the lowest cost route, we attempt a payment. If it succeeds, everything is fine. If it fails, we take information out of the failure and feed it into a system that manages reputation of nodes. This is not centralized, it happens on each individual lightning node. This information about node reputation is fed back into the next attempt to find a route. So we learn things from previous attempts to improve future payment attempts. It's really important to get the node reputation registry as good as you can, because it can help you avoid bad nodes from the past or help you settle a payment more quickly than otherwise. You could use a whitelist from someone you trust feeding it into your reputation system to find routes.

I'd like to do this in a more decentralized way though. You should be able to make your own observations when you make payments and extract useful information out of this.

## Updating node reputation: interpret outcomes

Say you get a payment quickly, or after a few days. In each case, you want to ideally pinpoint the exact node that failed our payment. You want to learn some information from this. There's a hodl invoice problem where a receiving node can wait to cause it; the problem is that it is hard to distinguish between intermediate nodes that cause delay versus receivers that are causing delay in this process. If it was a slow payment, we want to know what is the source of the delay. As a sender, we know when we sent a payment and when we got the success message back so we can measure the time between there. But we don't know if that duration is not to our liking then which node actually caused the delay or it could even be multiple nodes. In case of failure, we have the same questions: which nodes caused the delay? Which nodes accidentally failed the payments? These could be different nodes, one node failed and another node delayed the payment. Failure reason and source node may be unavailable, but that information should be communicated to us.

## Failure source identification

A node that fails a payment does encrypt(HMAC || reason)) so that the other nodes can't read what they are forwarding back to the sender. They make an onion packet on the way back and the sender of the payment is unwrapping the onion at the end of the chain, and discovering why the payment failed and sees an HMAC that authenticates the source of the error.

A channel might have a balance and it could be insufficient to carry the payment. This would be a temporary channel failure. It encrypts it, then it goes through the onion layers of further encryption for each hop, and the original user can decrypt everything and can blame a certain user for not having a channel balanced and they will be penalized or not used or something.

It's not always that simple though. If the error is "fee\_insufficient" then it means that a node didn't receive enough fees. In lightning, every node charges a fee to forward a payment. That's the basis of a routing node. They advertise the fee they would like to use. So a node might take too much fee and not pay the remaining nodes. In this case, the forwarding node can blame the next node-- but if we see the fee insufficient, it might be the signer of the node or it might be one node before that could be the real source of the problem.

There's also the "invalid\_onion" case, where it means that someone forwards information and says it's invalid and I don't have the keys to create an error message to send back to the sender. So in that case, the intermediate node signs a message saying there's an invalid onion problem on behalf of C because C doesn't have the keys to do this. So what should the originating node think about this situation? In this type of error, the originating node needs to take into account that it could be either of those two nodes that are to blame.

There's also "final\_expiry\_too\_soon" case. In LN, these HTLCs get forwarded and they have different timelocks. The final node might have a timelock requirement of 10; so when it arrives to him, it should have at least 10 blocks left on the blockchain before it expires, and if it doesn't then he sends an error back. Any node along the way could have introduced a delay. It's hard to say who took much time to forward it.

Failure source identification-- unknown case, where the failing node just sends back random bytes, and it's propagated to the originating node. It starts to look for a matching HMAC and it will never find it. So the last node is able to make the payment fail without the originating node being able to know which node in the route did this.

## Consequences

* Bad nodes have opportunities to fail and/or delay a pamyent without the sender being able to identify them easily.
* Routing nodes seeking to optimize profit could use this to "downgrade" errors to minimize penalization.
* Why so many failure messages and variants?
* Node fingerprinting

Using a "fee insufficient" error can spread the failure or penalization to multiple nodes. So a smart node would probably try to spread the blame around. It could in fact choose a different error to minimize penalization.

## Penalization rules

So what nodes and what routes to penalize? Some solutions include well, let's just accept this as a limitation. Some routes we won't try even if they might work for us, and we just accept this. It considers how many alternatives there; maybe we can penalize aggressively and still get away with it? Maybe there's more advanced penalization algorithms, like "triangulation" of bad nodes similar to "Master mind" where you guess four colors and you get some information about which colors were in the right position and you use that to create the best next guess. Another option is to expand the protocol with additional info that allows us to identify which node is failing or delaying the payment.

It's important to note that currently the lightning network is reasonably friendly, there's not that many nodes that are deliberately trying to frustrate payments but we're not sure how the network is going to develop. But we should consider how to prepare for more adversarial conditions on the network.

## Extended failure message requirements

We currently have a few features like previous hops have data obfuscated, and hops do not learn their position in the payment path. It's compatible with older nodes, ideally. In the future we might be able to have the error source identified as a pair of nodes. We would like to be able to identify a pair of nodes that could be blamed for the delay. If you have just a pair of nodes, that could be enough information. This idea is called penalization with node pairs.

We could also add timestamp information in the failure messages.  You would do encrypt(HMAC || timestamp || reason), and then do onions on top of this. One problem with this is that the node can observe the size of the path and then compute how far they are in the path, which is a possible link. We might be able to do a format that has padding or something.

We would also penalize nodes that fail HMAC and also its predecessor node. Usually the chain of HMACs in the failure message, we're able to narrow down the cause of the failure to a pair of nodes. This fits the requirements for a new style of message.

For timing information, we can add timestamps at every hop. What it would look like is, this is really technical, here's the three hops for the channel id used. Every hop adds timestamp information in the return packets. You can then penalize node pairs where time difference is reported.

For the settle path, the same new protocol can be applied. A message can be made in which we add timestamps similar for the failure path. All the errors that we see, like delays or failures on the successful payment or a failed payment, will be attributable to a single node pair and this information can be used to apply penalty to nodes. There's still some crypto work needed to determine the exact format. There's some options here but with some slight tradeoffs, but doesn't look bad.

## Reputation

In the future, what can we do with this? There can be a reputation model. The step is to update the model with the pair penalization information. There's a reputation model for the nodes you use. Bring it into a system that is able to control path finding for further attempts in the future. There are different ways to do this, like giving a node a unitless score where every node starts with 100 points and if something goes wrong we subtract some points. This is difficult to reason about because we're not sure what the scores really mean. We could use a machine learning model behind it, and do something like an optimal score based on previous history seen. You could also do a probability system in lnd; we tried to represent node reputations in ways that can be reasoned about. We express a probability about our next payment along this channel succeeding. We multiply the probabilities to get the probability of the whole route succeeding. We feed this into path finding to find the best route. This is no longer the best route in terms of price but also in terms of cost, success and the cost. There's also a "virtual attempt cost"- the cost of an attempt that you don't pay, but what is it worth for you to make one attempt less to make this payment? Senders gradually make their probabilistic reputation models more aggressive over time, and by doing this the network as a whole will become better over time. This might over time change the graph because right now penalties aren't that hard so routing nodes can get away with a lot of unbalanced channels or being offline. If we change this, then a routing node might think twice about accepting a perfect channel from a node that it's not sure will in the end serve well for forwarding payments. So you lose an incentive to connect indiscriminately to many nodes and use many channels. The graph might actually shrink overall.

## Probing

By making payments, you can learn something about the network and the graph like which nodes to use. Probing is a way to artificially gain more information about this. With probing, you send a payment to a receiver and you do it such that the payment hash to which the HTLCs is locked is unknown to the receiver. So when they receive it at the end, they are forced to cancel it because they don't know what the preimage is. You gain information about the intermediate nodes along the path. This doesn't bear the risk of making a payment; your money might get locked up for some time, and you could use a different amount like a much smaller amount to do an initial test of some route and use the outcome of this to feed into your reputation model and use it to improve your experience for future payments that benefits from the information that was observed while doing the probes.

## Persistent storage and sharing

We would like in lnd to start to persist this data. Right now it's only kept in active memory. We want these observations we make about payments to be stored on disk and we also want to store this in the most basic form possible which allows us afterwards to change parameters or even change hte model. it's possible to share data with others, and merge datasets for greater view of the network. But there's issues with authentication, privacy and gaming the system.

## Conclusions

Reputation management is important for reliable lightning payments. The current protocol contains gaps around bad node identification. The gaps seem to be somewhat fixable. The sender's reputation management strategies can shape the network and the long-term shape of the network. There are some possibilities of sharing reputational data between nodes so that nodes don't always need to be bootstrapped.
