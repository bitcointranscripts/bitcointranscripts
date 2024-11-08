---
title: 'ValueShuffle: Mixing Confidential Transactions'
transcript_by: Bryan Bishop
tags:
  - research
  - privacy-enhancements
  - coinjoin
speakers:
  - Tim Ruffing
date: 2017-11-04
media: https://www.youtube.com/watch?v=BPNs9EVxWrA&t=5065s
---
paper: <https://eprint.iacr.org/2017/238.pdf>


Thank you.

We have seen two talks now about putting privacy in layer two. But let's talk about layer one. We still don't have great privacy there. So the title of this talk is valueshuffle - mixing confidential transactions. I don't have to convince you that bitcoin at the moment is not really private. There are a lot of possibilities to link... to deal them as, to link addresses together. We can even link addresses automatically, there are companies that offer deanonymization as a service and we need to stop them. One simple way to break some of the linkability is to use coinjoin.

The idea of coinjoin is that you have a few users and for example they- let's really, let's use a simple case where they each have 1 BTC and they want to get some anonymity. They do a simultaneous transaction and send their coins to fresh addresses of their own. And all of these coins are used in a single coinjoin transaction. You need fresh addresses. If you do the naieve thing and others could say... a new address based on their old one or something. You need to come up with a mix list of fresh addresses. The cryptographic primitive here is called peer-to-peer mixing.

To explain about valueshuffle, we have to look at an old peer-to-peer mixing protocol. We did this work actually, including Aniket Kate. The idea is that we have a few users, say 4 users. We have a few messages. We want to come up with a mix or anonymized list of messages and also in some sense they want to agree on this list of addresses and messages. You want to use coinjoin, the agreement is just signing the coinjoin transaction. This works in a p2p model. The users might not trust each other, and there's no external anonymity routers like tor or ....

((... power problems ...))




