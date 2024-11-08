---
title: Htc
transcript_by: Bryan Bishop
speakers:
  - Phil Chen
date: 2019-05-11
media: https://youtu.be/CyieujRFk3g?t=8077
---
HTC / Exodus

# Introduction

SM: This conversation started a couple months ago in Hong Kong with Phil Chen and Adam Back were sitting in a bar talking about the bitcoin industry and what would move it forward. Without further adue, please welcome Phil Chen.

# Special announcement from HTC Exodus

Hi. I am Phil Chen from HTC. As you may know, we  built the first Android phone in 2008. The reason why we did that was because we believe in open-source. We believe in the promise of the internet. As we all know in this room, the whole open-source movement is incredibly important. In 2018, HTC launched the Exodus phone. The key was, how do we empower users to keep their own keys?

We wanted to build something on top of bitcoin. If you don't own your keys, then you don't have your assets. We built on top of this to let users control their keys.  We wanted a phone that can also support identity.

# Exodus

So we focused first on holding your own keys. We also implemented social key recovery. We built something on top of Shamir secret sharing. You can share your keys with your friends so that if you lose your phone you can recover it. One of the most important things for the whole industry is key management. One of the features we have is, we're going to open-source our code and our social key recovery mechanism.

# Social security

We have found a lot of supports including Vitalik Buterin who was excited about social key recovery in our phone. Charlie Lee was also an advisor for Exodus.

# Key management

Key management is one of the most important things in this industry. How do we manage wallets and keys? We have a secure element in our phone. It's kept in a hardware element. This is a trusted execution environment where you can sign with your keys. We're calling this the zion vault.

<ttps://github.com/htczion/ZionVaultSDK>

I want to show a video of something we did with the Opera browser, built in with crypto wallets. You can sign in with your private keys, and you can use your wallet attached with it to do micropayments. There's no audio, but it has a trusted execution environment.

# Securing the network

We want to figure out how we can help secure the network even more. Exodus 1S will be running a full bitcoin node. We validate transactions and blocks, we relay transactions and blocks to other nodes. We want to help app developers make better wallets. This will be coming to Exodus 1 and Exodus 1S in Q3 2019.

https://www.htcxodus.com/

twitter: philchen913
