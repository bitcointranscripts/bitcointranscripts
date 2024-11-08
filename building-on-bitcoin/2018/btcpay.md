---
title: How to make everyone run their own full node
transcript_by: Bryan Bishop
tags:
  - security
speakers:
  - Nicolas Dorier
date: 2018-07-03
media: https://www.youtube.com/watch?v=0UiMhpz9eLA
---
<https://twitter.com/kanzure/status/1014166857958461440>

I am the maintainer of Nbitcoin and btcpay. I am a dot net fanboy. I am happy that the number of people working on bitcoin in C# has spread from one about four years ago to about ten in this room toay. That's great. I work at DG Lab in Japan.

The goal of my talk is to continue what Jonas Schnelli was talking about. He was speaking about how to get the best wallet and get the three components of security, privacy and trust. I have a solution I think.

So to be clear, I am not doing an ICO, I am not starting a company, I am not asking for funding. I need open-source developers, not money.

btcpay was started as a reaction to B2X, which was a shitcoin that died before being born. I really liked bitpay in the past and I was shocked when they started getting political. As someone that advised people to use bitpay originally, I felt that they broke my trust and I decided to make an open-source version that shares the same API such that if you have your backend already working with bitpay then you can switch and use btcpay without rewriting your backend basically. It started as a project mainly for merchants, but btcpay is not about merchants. My goal is that every user should be able to run a full node.

Why are full nodes important?

There's no third-party bullshit like KYC and AML or surprise account freezes. No hostage situations, like central parties trying to redefine bitcoin. And this can unleash programmable aspects of this form of money.

Why does Alice not run a full node?

She can receive money on her mobile wallet just fine. She doesn't care about decentralization until it is too late. She can use Trezor or Ledger desktop app just fine and it works. Bitcoin QT always needs to sync when she needs to use it. You need to wait hours. It's really a pain in the ass. It's not user friendly, despite lots of work that Jonas Schnelli has done on the UI. Also, it takes a lot of space, except in pruned nodes.

How to make the dog eat its medicine?

You put the medicine in a beef ball and you let the dog eat the meat ball. That was btcpay in a nutshell.

Wallets using block explorer, like copay, or Samurai Wallet... but it's bad for privacy. If you are the one running the block explorer then you can spy on what the user is doing. Using bip37, with bloom filters, it's terrible for privacy because now not only--- in the case of block explorer, only the block explorer company can see your UTXO, but in the case with bloomfilters, all of the network can try to sniff your transactions and the user experience is also really bad because you still need to sync. Another type of wallet, the client-side filtering like bip158, which is better privacy but the synchronization is still needed.

Someone put a bitcoin full node on mobile phones. It has a bad user experience due to the syncing, and it's resource consuming (storage, bandwidth, power). Bandwidth can be pretty poor in developing countries. It's not perfect, so.

Lightning makes things even worse because now you need layer 1 tradeoffs as well as layer 2 tradeoffs. And you are unable to reliably receive payments because you might be offline. And you need occassional connectivity in order to update your channels and so on.

We should try to make mobile do everything. What if having an always connected bitcoin server was easier and cheaper than paying for a Netflix subscription?

A mobile app have good UX but is occassionally connected. Hosting a server has bad UX but it's always connected.

A lot of good tools in bitcoin but they are difficult to integrate. I come from Windows where there's giant software that does everything and we just go there. Bitcoin Core was like that originally. As time passes, and as bitcoin has become more focused on the linux community, much of the developers do their own tools that do one specific thing and then the community pipes stuff together to make new things work. It's good but you spend lots of time trying to stick everything together with scotch tape. It's not perfect.

You can try to do everything in software, or you can just glue two phones together and put it on the phone.  I am trying to glue multiple tools together.

When the first release of btcpay started, I tried to use docker. Iused postgresql, nginx, woocommerce, nbxplorer, and Bitcoin Core. I used a btcpay plugino on woocommerce. Then Iused letsencrypt-nginx-proxy-companion nginx-gen, to Let's Encrypt.

Since btcpay uses the same API as bitpay, I was able to fork a lot of bitpay plugins as well, and got all of that work for free.

NBXplorer was made at DG Labs originally for Elements. I asked them if it could be open-source and they said yes. It's a simple REST API. It doesn't index, it just tracks your own key.

I am using docker-compose to facilitate this. My second task was to integrate lightning, including c-lightning and lightning charge. I am also working on lnd integration. Zap Wallet is a good desktop wallet for lightning.

One downside is that you can't run lightning on a pruned bitcoin node. And also, docker installation on custom hosting is like $10/mo. If we used pruned nodes with lightning then it could bring the cost down to $5/month. And the downside is that the user needs to search for the hosts and run btcpay-install.sh to install and use this btcpay replacement.

I also setup a deploy to azure template. The downside is that this is expensive, about $60/month on Azure. Can go to $20/month but you need to do some manual stuff after the sync is done. It requires some technical skills. And also another downside is that you're using Microsoft so that's basically not an option for many of the people here.

Has a tedious deployment, but this could work with raspberry pi.

It's more user friendly to run your own user node. btcpay will expose a block explorer  to you. You don't need your phone to sync to the blockchain network. It's better to have your full node on a server.

I am planning to do exchange integration. I think this is actually the most boring thing. When somebody pays you, ... with bitpay, you have like the payment processing, and then the... we can think about this where the payment processor stays open source and then integrates with exchanges. Imagine there's a small reserve on their exchange, then somebodgy pays them, and then immediately the merchant can sell the BTC on the exchange, and that can be used to replenish the reserve. So merchants would be able to hedge against the volatility of bitcoin by using their own full node.

Using discreet log contracts, you don't need fiat to hedge against bitcoin volatility. Actually, this is not true. You can hedge yourself against bitcoin by using discreet log contracts. I am hoping to facilitate that in the future.
