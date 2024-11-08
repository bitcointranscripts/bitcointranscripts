---
title: Bitcoin Satellite Network
transcript_by: Bryan Bishop
speakers:
  - Adam Back
date: 2019-05-11
media: https://youtu.be/tJOI2i6h3HM
---
# Bitcoin in Spaaace!

I am going to be talking about the bitcoin satellite service that Blockstream has been offering for a few years now. I am going to talk about what it does and why that's interesting to users.

# Satellite infrastructure

There are 4 satellites, 2 uplinks with base stations sending data up to the satellites, and then 5 transponders. It's covering both Asia and Australia with one satellite with two transponders. Telstar 18v was launched by SpaceX late last year. It uses a 9m (30 ft) uplink dish. Blockstream is leasing fractional bandwidth on commercial satellites. You can negotiate with them to lease bandwidth, and that's what we did, at least enough bandwidth to provide the satellite service.

The uplinks are operated by Blockstream. We have two uplink sites. The picture on the right is the 9m dish which is the uplink for the pacific region.

# User equipment

The whole design is setup to minimize user equipment costs. On the left you can see the satellite dish setup using a 45cm dish, and a software-defined radio card. The picture on the right is of a ... so it's a 64-bit ARM CPU processor. That's the minimal specification it takes to run the software. It costs about $40 to buy that equipment.

# How it works

It might sound high-tech. But satellites are actually relatively dumb. We leased bandwidth on 4 satellites with 5 coverage zones. We have two dedicated Blockstream owned uplink sites. Satellites are dumb and all the intelligence is on the ground. We use a bitcoin node at the uplink, with low latency FIBRE network. We use forward error correction, and 4x block retransmit per 24 hour period. We use an SDR that does analog-to-digital conversion, and signal procesing is in arm64 processors.

# What do you use this satellite service for?

It has an interesting number of use cases. This is cheap privacy- it's passive broadcast, nobody knows you're using it. You can receive information and nobody knows that you were the one that were interested in that data. It saves bandwidth, it's about 10 gigabytes/month. IP addresses are often translatable. It also enables more global bitcoin access, and provides network split resilience. A bitcoin full node uses more than 10 gigabytes per month, and with satellite you can .... it also emerges cost in emerging markets. It also enables bitcoin mining.

Also, the internet itself can suffer from political disruptions and also other network disruptions. So having a satellite downlink can provide some more resiliency for users around the world. This helps protect against network partition events. You might otherwise continue operating thinking that your transactions have finality when in reality you were operating in a network split, and you were accepting unconfirmed bitcoin payments.

The satellites use multiple uplinks, we have two uplinks. If there was a network obstruction in one place, it can receive information from the other location. This provides cross-satellite resiliency. This is useful in situations where merchants might have a problem with having outages, and they could use this service to have extra resilience.

# Satellite API

We are offering access to the satellite broadcast using our satellite API. You can send short messages, paid with lightning through an API. You can broadcast data to the satellite nodes. This is useful for applications and could be used for price information, app info, blogging, news, Satoshi's Treasure, things like that. It's an internet-connected HTTP REST API. You pay for it with lightning.

I think there's someone operating a news site. There's all kinds of use cases.

# How do you send?

If you are receiving bitcoin transactions from the satellite, how are you sending data? Transactions are small, like 250 bytes. Even at $10/megabyte, which you might be charged if you had a fancy satellite internet connection, transactions could still be sent in a few seconds. So you can use Iridium MIfi, or a hughes bi-directional satellite data device. Or Povol Rusnak's bitcoin SMS gateway, or meshnets like gotenna + muletools.

# What's next?

We want bigger re-transmit windows, so that you can have more downtime and get caught up with blocks. There's a small coverage gap in Eastern Europe right now that we want to fix. We want to lower the equipment cost, and put things together in kits. We also want this thing to be easier to use, and we want more third-party developers to build out use cases in emerging markets and other applications.
