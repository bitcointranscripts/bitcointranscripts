---
title: Routing Failures
transcript_by: Andrew Toth and Caralie Chrisco
tags:
  - lightning
  - routing
speakers:
  - Fabrice Drouin
date: 2019-06-25
media: https://youtu.be/z5vEyvc2vrE
aliases:
  - /chaincode-labs/chaincode-residency/2019-06-25-fabrice-drouin-routing-failures/
---
## Introduction

So I'm going to talk about routing failures in lightning. Basically lightning is a network of payment channels and you can pay anyone, you can find a route. In routing in lightning you have two completely different concepts: how to find a route (path finding) and once you have a route how to actually send a payment through the routes to the final destination. This is what Christian showed that's the source routing.

So it's two different parts. When you have the graph, how do you find a route to your destination that is not part of lightning. Path finding is not defined anywhere in the specs. You do what you want, you can compute it yourself, you can ask someone to compute the route for you, but it's not specified in the actual lightning specs. Once you have a route what is specified is how you create onion messages to get the payments to be forwarded to its destination.

##Routing Table

To have a model for this for the graph that you have, we use a routing table that is made up of gossip messages. You have three types of gossip messages. You have node announcements this is a lightning node, you have channel announcements this is lightning channel, and you have channel updates and you have wallet updates for each side of every channel.

Can you tell me why you need two updates, one for each side? What are these updates used for?

Audience Member speaks

Fabian: Yes exactly. So if you have a channel between A and B, A will say, “Okay if you want to route through me using this channel, this is a fee, these are the fees I'm going to ask you to pay for and this is the CLTV Delta I'm going to ask you to use.” If you want route payments using the same channel but through B you would say, okay these are the fees that you need to use and this is the CLTV Delta that you need to use.” So A sets a routing fee when you want to have a route through A and B sets routing fees when you go through B. And it's very possible that you can use a channel on one side only. If all the money is on A side it won't be possible to use it to route payment through B. So you won't have channel updates for this side or you will have one that is disabled. The only information actually needed to create onion payments are channel updates. You don't need channel announcements, you don't need node announcements.

So this has been shown to you already when you receive a payment you peel off your onion layer and it reveals that destination, the next hop, the amount and CLTV that you're supposed to use when you forward the payments.

## Routing Failures

So basically you get this. The node that is relaying a payment as an incoming payment, we call it “upstream” and outgoing payments “downstream” and it's relaying payments. It has an amount and an expiry on the upstream side, and on the destination on the channel that it's supposed to forward the payments to it has also an amount and an expiry. So why do you think the node in blue could fail to route payments? What do you think are potential reasons for failing to route payments?

Audience Member: Not enough fees.

Fabian: Yes, not enough fees.

Audience Member speaks

Fabian: It could also be a failure because the node is not available. There's another one.

Audience Member: CLTV is too small.

Fabian: Yes.

Audience Member: The payment hash is not nice.

So also if you use tricks like these spontaneous payments [inaudible] could be that also. So you have plenty of reasons for payments to fail. It could be because the HTLC is badly formatted, the onion is unreadable. It could be because you have errors on the upstream channel. Like the balance is not enough to move money from one side to the other because there's a problem with the CLTV expiry. It could be because you have problems on the downstream channel because there are balance issues; not enough money to send to the downstream channel because the number of pending payments or the amount that is locked in pending payments is too high.

These are causes for failures, but it could also be because relay fees are not met. Or because the CLTV delta, the delta at the time I want to fix problems downstream it's too short for me. It could also be because the channel doesn't exist. You are using a routing table that is old, the channel has been closed but you don't know it. So you're trying to route through something that doesn't exist anymore. It could be because the node that you're trying to forward payments to is offline. You have many different types of errors that would cause your payments to fail. So in the specs you assign them types. And for certain types that are not fatal errors, for errors where you can actually retry, when you return errors you can attach a channel update.

So the errors we have today are bad onion, which can't read what's in the onion that is attached to an HTLC. You have permanent failures; it's never going to work. You have node failures; the node trying to relay the payments is having problems. And you have update failures. So it's almost right but for example you are using fees that are wrong because you probably have a view of the network that is outdated.

The channel updates used to compute the routes are too old and do not reflect the latest fees that have been set by the node you're trying to relay the payment through. So when you have - for some types of errors the payment is failed and you need to compute a new route and try again. Or some type of errors like update errors, you can actually keep the route you have, apply the new update, so just change the fees you're paying along the routes and try again.

And you can ban channels for a short while when you have temporary errors, or you can just remove channels from your local view of a network when you have permanent errors. But this has an impact on UX because every time you retry it with a few seconds basically to compute new routes and retry the payments. So if your view of the routing table is too old, too outdated, you will get new information as it fails, but it's really bad UX. So there's a compromise to be found between synchronizing everything when you start your lightning node, and I think a good enough routing table that you can start attempting to pay but failing because your updates are too old.

And that's, yeah, that's what we see tomorrow or, in two days when we talk about gossip. How do you efficiently synchronize routing tables? How do you make sure that you have enough information to find routes, and that route you compute is good enough so that your payments will go through and you will not have to retry. And for some of you - if you've been using Eclair for example, a few months ago we would attempt to pay even if the routing table was not really synchronized. And you will see the first payments - very often users will complain that the first payment was slow.

It looks slow, it takes a few seconds and then it's quicker. It's because we're trying to update the routing table and we often fail. The first payments get your dates we needed and try again with the new updates. So it's something you can see. It's in some lightning wallets and it’s bad UX. So we've pushed really hard for changes in aspects to make routing sync more efficient because if you use outdated data you pay the price from a UX point of view. Your payments are slow and that's not good. The idea is you open your wallet and you want to be able to pay in a few seconds. If it takes more than that it’s bad UX. So that's why I think a good view of the network is very important especially for end users and that's why it’s so important to know how to efficiently synchronize routing tables.

There's something that was I think not mentioned by Alex when it comes to incentives, but if you look at this, what do you think the node in the middle needs to know about the network? What kind of routing table does it need to have to forward payments? Does it need to have good information on the network to be able to forward payments? It doesn't need anything.

Right now we have a strange situation where the big nodes like in the middle of that one that do all the related stuff don't really have an incentive to have good routing tables because they don't use them. The only ones you really need a good routing tables are the end users and they're in many ways the weakest nodes in the network. It runs on phones offline, often on small devices, less CPU and less memory and they're the only ones who actually need routing tables. No one in the middle, it doesn't need anything. Which is why trampoline is changing this. If you’re a trampoline node you do need at least a partial view of the routing tables. So the incentive I think I way are fixed by trampoline because for this to work even with the lightning nodes will need to have at least a partial view of the network days up to date that's not the case today.

Audience Member asks a question.

Fabian: I wouldn't say there’s scoring, but I’m pretty sure every implementation is looking at ways to ban peers that misbehave. We've become more and more aggressive. If you send us updates for channels that are being closed after a while we will ban you.

Audience Member: I mean all of us little use use a scoring off of a certain kind it's just the type of signal that we mix in to that score that that changes so we are currently using the CLTV deltas because that's a time it money might be locked up and the fees as a signal into the score and I guess you are also using the same signal. Then you can add additional signals, it’s not an issue.

Audience Member speaks

Audience Member: We don't have an autopilot per se yet. So we use it mostly for choosing a route or prioritizing one channel over another.

Fabian: Yes the same way of heuristics to try basically with if possible we try to find the route that is least expensive as possible for you. We try to use the oldest channel and the ones with the biggest balance because of capacity with the smallest CLTV delta. Well that's just heuristics. But what you’re saying, I think is a bit different.

Every explorer now, every lightning explorer is trying to push their own ranking system, which can be heavily game and basically that's a different story. But that's what [inaudible] was trying to do with lightning beach and [inaudible] ranking information I think others too - but how it's computed is not really open yet.

Audience Member speaks

Fabian: I think what you do locally to ban peers that misbehave, like for example you can do  probing. I think C lightning does that now.

Audience Member: We have plugins that do that.

Fabian: So for probing, you basically create payments with the random payment hash - and it's supposed to fail right away. If it doesn't fail it means something's wrong and eventually someone will detect that nothing is coming back and after a while you would close channels. Because having channels that are not efficient is a waste of money, we believe that as the network grows and channels become bigger nodes will start being more aggressive when it comes to banning misbehaving peers and closing channels that are not used.

Audience Member speaks

Fabian: Maybe not blacklisting but if you have a channel that is never used, you close it.  If every channel where every parent time fails, you close it. We run a fairly big node on mainnet, one of the biggest and we have started being fairly aggressive when it comes to channels that are non efficient or not used because it's a waste of everything. It's a waste of money for us and it's bad for everyone because it makes payments not reliable.

But I will also say that you don't want to have only public channels. Suppose mobile phones are all private channels you would like to have mobile phones connect to because mobile users will mostly likely pay.

Audience Member speaks

Fabian: You want to be as reliable as possible, so that people want to connect to you because they know if they pay through you, it will work.


Audience Member speaks

Fabian: Not today, no.

Audience Member speaks

Without enough channels or nodes with zero fees today, I think we’re going to add more.
