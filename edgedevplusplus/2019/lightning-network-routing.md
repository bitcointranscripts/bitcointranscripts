---
title: Lightning Network Routing
transcript_by: Bryan Bishop
tags:
  - lightning
speakers:
  - Carla Kirk-Cohen
aliases:
  - /scalingbitcoin/tel-aviv-2019/edgedevplusplus/lightning-network-routing
---
## Introduction

Good afternoon everyone. My name is Carla. I am one of the chaincode residents this summer. This talk is going to walk through the protocol layer by layer and look at the different components that make up the network. Lightning is an off-chain scaling solution which consists of a p2p network of payment channels. It allows payments to be forwarded by nodes in exchange for fees.

## Scaling with payment channels

This involves a payment channel. It's a construction where 2 individuals Alice and Bob are regularly transacting with each other. Normally a single bitcoin transaction would go through the chain. But a payment channel lets you commit to a funding transaction that goes on on-chain, and then subsequent transactions don't need to go on the chain. They update a net payout from that 2-of-2 multisig and they update the balances in the outputs for either Alice or Bob to reflect payments being paid. Eventually, they can net out to the blockchain by broadcasting the most recent state from the payment channel.

You can also make a multi-hop payment channel network where as long as you can route through the network over channels then you can make payments to individuals you do not personally have a channel open directly against.

## Layers

There's a transport layer, a base layer, and then an update layer. The update layer allows you to trustlessly agree on state and trustlessly revoke past states without the risk of a party broadcasting an old state and being able to steal old bitcoin. There's a penalty transaction but also a DMC and also eltoo which is a new proposal. Eltoo requires SIGHASH\_NOINPUT. Once we have the update layer, we can agree on states. We need an atomic and trustless way to... so that requires the transfer layer like HTLCs. Then we have a multi-hop layer like Sphinx which lets us propagate these HTLCs through the network.

## Transport layer

The bottom of the stack is the transport layer. We want to use this to authenticate node identity. We want to do this in a way that is fingerprint-resistant. If I randomly associate with a node in the network, I shouldn't be able to figure out who someone is just by bruteforce randomly connecting. Also we want bruteforfce-resistant communication, we want confidentiality and integrity of messages.

The tool to achieve this is the Noise\_XK protocol. It's a set of tools that you can arrange in various ways. We use the unknown/known variation. When we connect to nodes, we know that the IP is associated with an ID. However, when you're making a connection, you don't advertise your outbound and they don't know who you are so you have to authenticate who you are.

This requires persistent identity. This is different from bitcoin where we want all nodes to be indistinguishable. But in lightning we need to do routing so we need node identity. We use a sequence of Diffie-Hellman operations in a handshake protocol and then we establish a shared secret.

## Base layer

This is how we communicate between nodes. The base layer has the goal of figuring out messages and what they mean. It also signals feature support so that the protocol can move forward hopefully in a backwards-compatible way.

## Message framing

There's a two byte type that specifies the format of the payload. The type is the bit location, not the numerical value. It's the most significant value not the... IT's okay for messages to be odd, but if you run into an even one then you have to break your connection with that node. If we end up with a gossipy interoperability bug, then we can break up the lightning network by implementation quite easily. Also, the message in the lightning spec has been updated to have TLV fields to allow for rapid expansion of existing types.

## Control messages: init

One thing that is interesting is how we initialize nodes in hte network. There's 16 most significant bits set, it used to have a global length or uint 16 indicating how many signals we're signaling, and then the features. Then it had a local length which was another uint 16 signalling local communications between node. If you're signalling specific features which don't effect the network as a whole. Local features have been scrapped in the protocol, and they are replacing these two fields with a must-be-zero feature which is fine because every node implementation is still compatible with that.

## Update layer

In the update layer, we need to create an updated state between two peers and we have to make sure old states cannot be broadcasted. Some early implementations started with simple payment channels, which was a unidirectional payment channel based on a 2-of-2 multisig construction where signatures would be sent over for increasing amounts of bitcoin. The receiving party has no incentive to release old states to the network, because they are always receiving increasing amounts of bitcoin. However, this is limited by the funding amount. If you put 1 bitcoin into this channel, you can't do bidirectional sends.

## Past update mechanisms

Another idea was from cdecker at Blockstream where you would be able to send back and forth instead of unidirectional. These would use timestamps to revoke old states. The timestamp would eventually make it so that you can't run the channel anymore once you run out of timelocks you need to close your payment channel.

In the lightning network, in the update layer we need to be able to sign multiple double spends while trustlessly revoking all the recent transactions. The lightning penalty update mechanism is a transaction where you steal all of the funds from your counterparty when they try to cheat you. This commitment transaction is signed before the 2-of-2 multisig is funded, because otherwise the counterparty will be able to ransom your coins or hold it hostage. So you must insist on collecting those signatures first.





