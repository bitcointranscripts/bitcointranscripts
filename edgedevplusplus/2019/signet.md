---
title: Signet annd its uses for development
transcript_by: Bryan Bishop
tags:
  - signet
speakers:
  - Kalle Alm
media: https://www.youtube.com/watch?v=btzLev5bO_M
date: 2019-09-10
aliases:
  - /scalingbitcoin/tel-aviv-2019/edgedevplusplus/signet
---
<https://twitter.com/kanzure/status/1171310731100381184>

<https://explorer.bc-2.jp/>

# Introduction

I was going to talk about signet yesterday but people had some delay downloading docker images. How many of you have signet right now? How many think you have signet right now? How many downloaded something yesterday? How many docker users? And how many people have compiled it themselves? Okay. I think we have like 10 people. The people that compiled it yourself, I think you're going to be able to do this. The people who are using docker, I think the Tel Aviv University network is going to give you problems. If you have your own internet connection though, then it should work out of the box.

# Signet

I'll talk a little bit about what signet is. So why signet? There's something called testnet for bitcoin. Bitcoin has two networks. Mainnet, which is where actual money is being transmitted, and testnet which is where people take and try things out. The coins on testnet are meant to be worthless. There's some problems with testnet. In particular, testnet has an incentive problem because you have to actually mine blocks on testnet for it to move forward. Why would you do that if you don't get anything out of it? Mining testnet is more altruistic or something. You tend to see bursts of blocks and then nothing for like a week. That's not ideal testing grounds for something meant for running on mainnet. Also, on testnet there tend to be 10,000 block reorgs and now your wallet or your application is broken- but is it because your app is broken, or is testnet broken? 10,000 block reorgs aren't common on mainnet. It's not very useful for people, and lightning developers have complained about problems for their channels as well.

Regtest is a regression testing system. It's not even really a network. You run it locally on your machine. You could connect to other regtest nodes but anyone on that regtest network can reorg as much as they want or add as many blocks or data as they want. So that doesn't work for federated testing.

Signet is a custom testing network where anyone can join at any time they want, and it doesn't have these problems I just described. Regtest is really not a network. Signet is built for allow for arbitrary number of simultaneous networks. It's easy to use faucets and explorers etc. I also want to implement double spend as a service (double-spend-as-a-service). The signet mining server will mine that transaction for you, and then a few blocks later will reorg the transaction. This way, you can test your wallet software and make sure it can handle reorgs in a global setting. This is kind of implemented, there's just not a public interface yet. There are scripts that do this.

# What makes signet special?

Well, signet is 100% centralized. It's not a decentralized network like bitcoin. Signet is run by one or several people that have special keys. Each block has a required signature. Everything else is the same; you still do proof-of-work (although usually at very low difficulty). This is a really controlled environment for testing specific conditions.

# Let's try it out

I recommend using tor if you have compiled this yourself. On macosx, do not use tor browser. Use "brew install tor". If you're on linux or ubuntu, then I think--- no, it's more complicated to install tor. It's super easy, but you have to google it. Alright. I want to try doing things with you guys. It's not going to work because of the network but if you really want to try it out. Yeah, we could open a hotspot. If you want to try it out later, we can gather up together here.

If you're running through tor, then you have to type proxy=9091 I think is the tor port. If you have a tor hidden service you can do that; but that's not complicated either.

First, you need to compile Bitcoin Core with the signet branch. If you do everything in my slides, you'll have a compiled bitcoin node but also the docker images which is fine but you should consider just doing one of them. I saw a few people doing "sudo docker run" which I don't recommend; I suggest just adding yourself to the docker usre group. On macosx, I think that just works.

Once you run the signet node, you need to run a script like "getcoins.sh" and point to a faucet at an IP address with a --password parameter and --faucet parameter. Run bitcoind with "-signet -daemon".

Okay, how many of you have peers? Are any of you connected? I'll just show you. I'm starting tor, up there. I'm starting bitcoind on this side here. As you can see, it's getting outbound connections. If you were running on tor, you would see connections stuff. If you're not running on tor, you will see zero blocks and zero peers.

The reason we're going through tor is that tor doesn't give a damn about the university's firewalls. Tel Aviv University is blocking some ports. The firewall here is even blocking me from calling my wife. We can't even get a video call to my wife, but we can get a bitcoin signet network working. Cool.

Increase the block size? You traitor. Oh, the font size.

Okay, I'm going to end this presentation. I'm going to go around and poke you guys and see if I can get you to run this with me. Who's trying right now and failing? You're not sure? Okay, I'll come to you. Anyone else actually trying?

# See also

<https://diyhpl.us/wiki/transcripts/bitcoin-core-dev-tech/2019-06-07-signet/>

<https://bitcoin.stackexchange.com/questions/89640/what-are-the-key-differences-between-regtest-and-the-proposed-signet>


