---
title: Taxonomy Of Ln Nodes
transcript_by: Bryan Bishop
tags:
  - lightning
  - c-lightning
speakers:
  - Lisa Neigut
date: 2019-05-11
media: https://youtu.be/A4i5cEI1jnc
---
# Introduction

Hello. I work at Blockstream on c-lightning. I am here today to talk to you about a taxonomy of nodes about who's who on the lightning network. I wnat ot go through the tools that have been built, looking through the perspectives of what different nodes are trying to accomplish.

# LN map

There's a bunch of nodes on the network. Let's look at some stats. There's a little over 8,317 nodes. There are two categories so far. On the LN statistics site, it will say about 3374 public nodes, 490 nodes running over tor.... Those are publicly addressable nodes where you can go and create a channel with them because you know how to reach them. There's about 4453 nodes that aren't publicly accessible.

# Categories

I am going to further divide the nodes into three different categories.

Consumer: One is the consumer category, people who want to make payments over the lightning network.

Vendors: These are individuals who want to sell things on the lightning network, like stores that sell stickers.

Liquidity providers

To get a better understanding of what these different perspectives have, I am going to walk you through quickly how payments owrk on lightning network.

# Lightning payments

Open a channel, fund a channel, create a balance of payments in the channel. One of the nodes opened the channel so it will have a balance. There's a network of these nodes with open channels. Also, you can send money through the network and there's hops on the network. Based on the topology, you might not be able to route a payment because there's not enough liquidity pointing in the right direction to get that payment completed.

That's how payment flows have directionality. When we're talking about routing, it's not just the channel topology but also the balances in the channels.

# More categorization

If you take a step back for a second, you can also classify based on the types of payment flows you're going to see. You can see that funds flow into a node, and we call that a vendor.

On the other hand, if it's largely making outflows, that's a consumer.

So you can make a generalization that there's consumers and vendors and the net flow of payments is from consumers to vendor. It would be bad to assume that every consumer would directly connect to vendors to send payments. But in general, consumers use liquidity providers to get to vendors.

# Existing infrastructure

You can already classify some infrastructure. Some of the tools fit multiple categories, but I've divided them based on 3 things to see how these existing projects can fit into these silos.

We can start with consumers, projects that help consumers achieve their goal on the network. The first one is autopilot.

# Autopilot

Autopilot is an automated service that runs on your LN node. It looks at the network and it decides which nodes are good to connect to, such that you have the ability to route payments. It runs automatically so the name is autopilot. There's a plugin for c-lightning called autopilot, and lnd has autopilot but I think it starts automatically without user opt-in but I'm not sure.

# Wallets

Another technology for the consumers is wallets. There's a lightning wallet from Lightning Labs. They don't list your IP address or your node ID anywhere on it. It also doesn't talk about channels, it just has a balance. It abstracts this away. It's a unified interface. If you want to make a payment, nevermind how, this is how much money you have. So you only really care about your balance not the technical details.

# Node proxies

These assume that you already have a separate node and you just want to be able to access it to send payments from a desktop or a mobile app. You can see this in chrome extensions, like Kiilowatt for c-lightning, and Joule... and then there's things like Spark Wallet for c-lightning which is the set of projects and that's... desktop client and mobile client. You can use a proxy to talk to your node.

# Infrastructure for vendors

If you want to sell things on the lightning network, what kind of tools have been created to accept payments?

# Payment plugins

The plugin I am most familiar with is a Woocommerce plugin for Wordpress. There's also one for PrestaShop. I'm sure there are more.

# All-in-one solutions

This is a superset of the payment plugins. It takes everything you need and puts it in a box. An example of this is btcpay, and another one is LN store-in-a-box which is a collection of wordpress, lightning node, bitcoind and woocommerce plugin all in one so that you can put this on a server and setup and run it. So you go to lightninginabox.com and it has a bunch of software on it already.

# Third-party proxies

One example is opennode. It's a semi-custodial thing that runs the node for you and you can proxy through them.

# Infrastructure for liquidity providers

So what are the tools that help with liquidity providers? There's tools to help move money on and off the lightning network. Then there's rebalancers, where if you have a bunch of channels open and you want to move funds between them, there's a plugi nfor c-lightning called the rebalancer. And then finally there's some services you can do that you can go and get liquidity from. And then there's one called Thor, and someone wrote a form that will send you liquidity when you need it.

# Future infrastructure

I want to talk about some new projects in the pipeline and how they fit into these three categories.

# Trampoline payments

I think the trampoline payments proposal was sent out in late March or early April on the lightning-dev network. It was pierre and cdecker who came up with it. Instead of the client needing-- the consumer needing to know the exact route, instead they delegate some of the pathfinding responsibility to a larger liquidity provider and to help them get to the final destination.

# Neutrino wallets

This is basically the latest version of SPV that is supposed to help make better mobile clients and do self-custody more effectively.

# Dual-funded channels

I have a proposal for dual-funded channels that helps with liquidity. So people will be able to start with more balanced channels. Right now when opening a LN channel, only one person can contribute funds.

# Splicing

Splicing is where you take loop-in and loop-out, which is what the Lightning Labs people did, and moving it into the spec so that anyone would be able to fund on and off chain on their own.

# Liquidity advertisement

Nodes have liquidity and they will be able to advertise their liquidity so that if people needed it, they could find an easier way to go and get that liquidity.

# Future stuff

I've been running a niftynei twitch channel where I livestream my dual-funded channel work. If you want to see what it's like to work on c-lightning, check out my channel. It's on twitch.
