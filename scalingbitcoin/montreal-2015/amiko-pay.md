---
title: Amiko Pay
transcript_by: Bryan Bishop
tags:
  - lightning
speakers:
  - Come Plooy
---
Amiko Pay aims to become an implementation of the lightning network. So that previous presentation was a great setup. There's a little bit more to Amiko Pay. If you look through the basic design of the lightning network, there's a network of payment channels. There have been several variations of this idea. Lightning Network happens to be the best so far. What Amiko Pay aims to do is to focus on the nodes, and do the routing between nodes. The other big problem of Amiko Pay making the payment channels, for different types of channels you can make different plugins. This kind of design makes it possible to have different kinds of channel within the same network. This opens up a couple of possibilities.

These channels can be different in technology, they can offer a different security/convenience tradeoff. They could actually be running on different blockchains. That would make that network useful for transfer of payments between sidechains. When they are sidechains, they are still trading BTC. But what about on different channels and sidechains you are trading different assets? Then the nodes become a mesh network of different assets and multiple channel types. For now, I am not going to implement that in Amiko Pay. This could give you decentralized exchanges in the future.

In terms of channel types, what has been implemented for now is a Ripple-style IOU channel. It is an object that fills in place, and only does some bookkeeping of who owns what. This gives no protection or security whatsoever, but for software testing it is fairly useful because it is trivial to implement. I think that in the future this will continue to be useful, for example for nodes that are trusting each other, or nodes that are run by the same organization and can fully trust each other.

In the future we need a true lightning channel. There are two approaches towards developing this. The lightning developers are developing it on a sidechain because the lightning channel design requires certain features in bitcoin that are not yet present. So the lightning developers are working on that sidechain with those new features. For Amiko Pay I chose a different approach, I don't want to depend on the bitcoin developers to give me those new features. So I designed a different channel type that emulates these missing features with an escrow service. So now you have to depend on the escrow service to evaluate all of the things that are not evaluated by bitcoin script. It's not as nearly secure, but I wrote a paper about this. I think it is good enough for real-world usage.

There are multiple payments going on at once through a channel, and it's related to the state of the transaction, and this effects the state of another channel it is connected to. It's hard to keep everything consistent. The only remaining problem here is that because of this complexity, there's a lot of open issues in the security of the software. It's a long todo list of solving security issues and as soon as the length of that list drops to zero it will be ready for release.

Transaction malleability continues to be a problem, even for Amiko Pay, so my message to the core developers of bitcoin, please solve transaction malleability issue. There has been some discussion on the lightning-dev mailing list. I am a bit skeptical about armchair economics, and I think we should try it in practice and see what works and see what people will do. What I hope is that Amiko Pay will make this possible and let's see how it goes.
