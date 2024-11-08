---
title: Transaction Rebroadcast
transcript_by: Michael Folkson
tags:
  - bitcoin-core
speakers:
  - Amiti Uttarwar
date: 2019-09-09
media: https://www.youtube.com/watch?v=v4TXfwwz_VI
---
<https://twitter.com/kanzure/status/1199710296199385088>

<http://diyhpl.us/wiki/transcripts/scalingbitcoin/tel-aviv-2019/edgedevplusplus/rebroadcasting/>

# Introduction

Hello. Thank you for joining me today. My name is Amiti and I’d like to tell you a bit about my Bitcoin journey.

# Professional Background

I graduated from Carnegie Mellon five years ago and ever since I’ve worked at a few different startups in San Francisco Bay Area. My adventures with blockchains began when I worked at Simbi. Simbi is a marketplace for trading and bartering services. Here I found a community of people who were living outside of their means. Based on the services they wanted to offer to the community they were able to find the services they needed or desired whether it be a personal accountant, a massage therapist or someone to build them a website. This alternate economy was offering them a way of life not available to them in the conventional system which really brought up the question for me: what does it mean to be wealthy?

# What is wealth?

It is obvious in this day and age that wealth goes beyond a number in your bank account. For me it has more to do with the standard of living, a way of life that affords you the privilege of being able to pursue mental, physical, emotional well being. Our monetary system intends to capture these ideas. It has become very apparent to me the ways in which it is broken. I was primed. When I learned about blockchains I was deeply captivated.

# Trust models

Blockchains introduce a fundamentally new trust model. Historically we’ve only ever seen two trust models. One is direct. I get to know you and we build trust. Based on that we can do business, make future promises, agree on what happened. The second one is hierarchical. That’s what prevalent in our society today allowing our society to grow to the size that we’re at. This is everything from businesses to schools to banks and government. It is what we’re using when you use Airbnb to book an apartment across the country and stay for one week at the place of someone who you’ve never met and you never will meet. You trust the reputation system of this website and the insurance policy as a fallback. The problem is that that trust is expensive. The people who are providing it unproportionally profit versus the people who are providing those services. With blockchains we have a totally radical new opportunity because we have a new trust model. Blockchains say that two strangers can come to an agreement without actually trusting one another. The implications of what this could mean for our society is totally unimaginable. I was in, I’m ready.

# Coinbase

So I got closer. Most recently I’ve been employed by Coinbase where I’ve been working on the crypto operations team. I handled our Bitcoin hot wallet, send and receive functionality, transaction efficiency and problems of that nature. I also worked on a project to move over our cold storage systems and I moved $5 billion of funds from the old cold storage system to the new cold storage system. But I wasn’t satisfied. I wanted to work directly on developing a better monetary system so that’s why this summer it has been such a privilege to be here at Chaincode and get to work directly on Bitcoin Core and contribute to the protocol.

# Money requires privacy

So let me tell you a little about what I’ve been up to. First, a premise. Money requires privacy. I’m not going to argue this claim because I don’t think anyone wants their credit card statement to be public information. I’m just putting it forward as a premise.

# Transaction Rebroadcasting

In Bitcoin Core right now the current rebroadcast logic is terrible for privacy. Let’s take a look at why. The way it works is, say you have a node and what is depicted here is your mempool with all of its transactions and it is ordered by fee rate. Let’s say you make two transactions through your local wallet. One is at a high fee rate and one is at a low fee rate. You initially propagate these out to the network by sending INV messages to your peers and hopefully those transactions make it to their mempools and they spread it further into the network. Then you see a new block gets mined and comes in. It removes roughly the top block worth of transactions in your mempool assuming that propagation has worked well. That leaves behind your low fee rate transaction which is to be expected in this use case. But the behavior is that just in case the transaction didn’t successfully propagate, you’ll send another INV message and rebroadcast it to your peers. This has a few problems. One, nodes don’t consider what should have been confirmed. Instead every time a block comes in they tell their peers “Here are all of my unconfirmed transactions.” What makes it worse is that nodes only ever rebroadcast their own transactions so if a spy node is paying attention it can easily identify which transactions you are the source wallet for by knowing if you have sent a INV message for it before.

# Dust Attack

This leaves room for a vulnerability called a dust attack. The way this works is an attacker would make a large transaction with a lot of dust and send it too many different addresses. Then it would just pay attention because the way a wallet decides if a transaction is mine is if my address is involved at all. So wallets will start rebroadcasting that dust they received and make it very straightforward for a spy node to identify that they are the source wallet for these addresses making privacy a dead giveaway. If this is so bad for privacy why rebroadcast at all?

# Why Rebroadcast?

Maybe a block comes in and you do have a high fee rate transaction that you expect would get picked up but it isn’t. Maybe that is because of issues with relay or because your transaction got expired from the mempool or evicted in a competitive fee rate market. Who knows? It would be important for you to send out another INV message, rebroadcast it to the peers and propagate it to their mempools so your transaction has a chance of being confirmed. With all of this in mind I have envisioned a new way that rebroadcasting logic can work.

# Rebroadcasting: A New Way

Fundamentally it comes down to this. All nodes will rebroadcast transactions that they think should have been confirmed by now. I define “should have been confirmed” as looking at the top of the mempool by fee rate and applying a recency filter saying that the transaction must be older than 30 minutes. I’ve put this altogether and I have a PR up [PR #16698](https://github.com/bitcoin/bitcoin/pull/16698). If you are interested in the details I highly encourage taking a look and I’m happy to answer any questions. Just to give you a little highlight of some of the functionality needed to enable rebroadcasting. I extract the logic from the wallet into the node and I use the block assembler so that we can identify the top of the mempool in a comparable way to how my node will be looking at it. I update the wallet logic to resubmit unconfirmed transactions to the node instead of sending it directly to its peers. I add a recency filter in the block creation logic so that we can ignore the new recent transactions and I add a data structure in the mempool so that we can track local transactions and ensure that there is a successful initial broadcast. Then I add a lot of tests to make sure that’s actually what my code is doing. But not I’m done. In fact I’m just getting started.

# I’m just getting started

I have a bunch of follow up PRs that I think could help improve the codebase. For example I want to improve the test utility to make it really easy to create transactions with specific fee rates. I want to update all the invocations of the Poisson method to use mockable time. I want to clean up wallet code now I’ve removed some of the dependencies and make it simpler. I also want to get more involved in the ecosystem. I want to review PRs and provide this valuable input that people have been so generous providing for me. I want to host a PR review club on IRC and encourage more contributors to get involved. I have a lot more work to do. I get so excited to wake up every day and to do that work because Bitcoin matters.

# Bitcoin Matters

It matters to me and it matters to the world. All of the biggest challenges we face today, we face as a global society. But we don’t have a method for organizing at that level. The internet has enabled global communication but we don’t have any model for how to scale our human interactions effectively at that level of complexity. We need a global society and building a global money is the first step toward building a global society. While I do believe that Bitcoin is an experiment I think it is an incredibly important experiment because together we’re envisioning what global money could possibly look like. We’re taking small steps towards solving some of the most consequential problems that we face as humans today. If we want Bitcoin to be the best money it can possibly be we need all hands on deck. We need people to contribute from all walks of life and bring their unique perspectives with them.

# Diversity

Right now one area where this is apparently lacking is in gender diversity. I don’t know of any other women contributors in Bitcoin Core and I don’t think that’s ok. I’m working to fix it. It starts with myself, it starts with making more changes and PRs and reviews and establishing myself as a valuable contributor but it doesn’t end there. I want to onboard more, I want to put my face out there and encourage other women and people of minorities to get involved and show them that the Bitcoin Core community is actually really welcoming. It is so amazing to work on challenges that are difficult and impactful. Because Bitcoin matters. I want Bitcoin to be the best Bitcoin it can possibly be. Thank you for listening.

