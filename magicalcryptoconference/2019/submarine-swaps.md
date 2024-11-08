---
title: Bridging Off-Chain and On-Chain with Submarine Swaps
transcript_by: Bryan Bishop
tags:
  - lightning
  - submarine swaps
speakers:
  - Alex Bosworth
date: 2019-05-11
media: https://youtu.be/SCxaV2HCQ5o
---
## Introduction

Hi, I work at Lightning Labs. I want to talk about the dawn of hyperloop. It's a new concept.

## Hyperloop

To zoom out on what problem we're working on here, we had this cool lightning network. But it's, the way the lightning network works, is that it's complementary to the bitcoin network. Each side has its pros and cons. If you want the most effective way to send capital around, you want to leverage both.

When we talk about high scale, it's going to take optimization of these technologies to actually realize the scale benefits that are theoretical.

Lightning Loop is a service that Lightning Labs is operating as a product. We're standing behind it, and you can go and try it out. It's currently in alpha.

## Flow

I want to go back to the original LN whitepaper which says bitcoin can scale to billions of users without the risk of blockchain centralization or custodial risk. That's a bold statement. It would take years of creating channels to do that, because of the block size limit. Even if you did create channels for billions of people, they would run into a situation where they would deplete their channels, and the balance wouldn't flow back and forth perfectly. So you would need to move liquidity around. This is the concept of flow. This is a characteristic of the lightning network. It's not so obvious. But it's like the internet, if you have an internet connection using dialup and the rest of the internet is not dialup, it doesn't matter how fast they are, it's how fast you are. It's the concept of bandwidth. Even if you have great bandwidth, and the destination doesn't, then you're limited by that flow.

## Submarine swaps with lightning loop

Submarine swaps addresses an issue where you have this unbalancing. So maybe your channel has been depleted, or people have spent down a channel in your direction and you're a successful merchant and all the liquidity has come to your side. Once you get there, there's nothing in the lightning network that can fix that. Say you received all the payments you could receive and you reached a limit. There's no internal balancing of that situation. In that case, you have to go to an external settlement mechanism. One way would be you can go to a lightning-enabled exchange.

Submarine swaps is a method of internal settlement. So you want to spend down your channel to the greater network, but you are going to receive back the same amount of funds, using the same HTLC. It uses the chain as an external settlement mechanism. They are locked into the same HTLC that LN usually uses.

So we built this out as a service. The big thing we're focusing on is this .... and the network path. A lot of the time, people are talking about liquidity providers and you can pay them and get liquidity. But there's only a few people that will actively create this as a business. But we want a well-distributed network. Lightning Loop with any node in the network, you can get inbound liquidity from any node in the network. We believe this will provide the most health and strength to the network.

Loop-Out is from LN to the chain, and loop-in is to go the other way.

## Costs of submarine swaps

The cost of submarine swaps is what I really want to talk about. Right now we have released Lightning Loop in production and you can try it on mainnet and testnet. The big thing that we focused on is creating that non-custodial experience and the network health experience. What we're working on in the future is this idea that we want this to be an efficient experience. I want to talk about some of the problems of these optimizations right now is that they have these costs. In the illustration, you can see what a submarine swap looks like.

When you fund the pay transaction into this swap, you have the funding phase, and maybe you have multiple inputs because you need multiple inputs or coins to do this. Once you fund the swap, you're probably not going to have exact change, so some of the funds need to go into the swap itself, some into the destination and some go back to yourself because that's how normal bitcoin transactions work. Then they go into the sweep phase, and then they need to be laid out into a future destination you want to send them to. It's a heavyweight operation, it's not just one transaction, there's multiple transactions and multiple outputs which makes this expensive. Also another cost is that you reveal that you're doing this swap on the chain.

## Hyperloop

One thing I'm working on at Lightning Labs is that we can minimize those costs. I tried to think about what is the absolute minimum we can get to. Can we use multisig, batching, and MuSig N-of-N? We can actually take part of the swap off the chain, so instead of putting the HTLC on to the chain, we can create a temporary channel setup to do the swap but actually it deposits it into a multisig. So we sign all the transactions as if we were going to the chain, but then we replace all of them with a cooperative transaction that skips the HTLC that would live on the chain. We're working on combining multisig signatures so that many people could combine their signatures into one signature. So if we have 1000 people all talking at once, that can be collapsed into one single signature. In this diagram up here, this is the entire transaction all the inputs and outputs for the swap. Instead of having five different inputs, and three different outputs, you have one input that funds the entire swap and this is all going into the multisig between all the participants in the swap. The outputs are pretty small, like 30 bytes depending on how you construct it. That means we can swap huge numbers of people in one combined elapsed transaction and get huge space savings maybe 10x or more.

## Scalability

The net of this is that we can scale rebalancing. How many swaps can we do? We can do up to 2 billion people rebalanced per year, with no forks. No rules changed. On the current infrastructure. We know this is going to improve, too. This is potentially cheaper than splicing, which is very ad hoc. But if you can organize a lot of people together into one transaction, you can get even better scaling characteristics if everyone themselves had their own inputs and their own outputs.

Submarine swaps is not only something you can use today to get inbound liquidity to your node, it's something that can be potentially part of the LN going forward as a way to do deal with the unbalancing.

