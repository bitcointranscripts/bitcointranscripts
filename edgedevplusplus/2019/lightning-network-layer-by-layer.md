---
title: A walk through the layers of Lightning
transcript_by: Caralie Chrisco
tags:
  - lightning
speakers:
  - Carla Kirk-Cohen
media: https://www.youtube.com/watch?v=tie0Gpq2eJI
date: 2019-09-10
aliases:
  - /scalingbitcoin/tel-aviv-2019/edgedevplusplus/lightning-network-layer-by-layer
---
# Introduction

Good afternoon everyone. My name is Carla. I'm one of the Chaincode residents from the summer residency that they ran in New York this year and this afternoon I'm going to be talking about Lightning. In this talk, I'm gonna be walking you through the protocol layer by layer and having a look at the different components that make up the Lightning Network.

I'm sure a lot of you are pretty familiar with what the Lightning Network is. It is an off-chain scaling solution, which consists of a peer-to-peer network of payment channels which looks something like this scary gray blob over here. It allows payments to be forwarded by nodes in exchange for fees which allows us to exacerbate the amount of scaling we achieve. The way that we scale is with something called a payment channel.

# Payment Channels

So in this construction, if you can think of two individuals who transact fairly regularly, let's call them an Alice and Bob -- very regular Bitcoin users. So if Alice makes a send of one bitcoin to Bob, that’s going to go on chain. If Bob sends that same UTXO back to Alice with 0.5 bitcoin, that’s going to go on chain. Then if Alice makes another send back to Bob of 0.2 bitcoin, or any other amount really, that's also going to go on chain. And that's a lot of transactions just for two users in the network to produce.

What payment channels do is allow users to commit to what's called a funding transaction, and this is a 2-of-2 multisig which goes on chain. It commits a certain balance into a payment channel. Then what they do from this point is they update a net payout from this 2-of-2 multisig which assigns balance to each user. So when we start out, Alice will have two and Bob will have zero because Alice put the money into the 2-of-2 multisig. Then they can continue to update the balance in this payment channel to reflect payments that are being made.

So if Alice sends Bob one bitcoin, they update the state and then each of them have one. They can do this, almost indefinitely, continuing to update the state off-chain by delaying broadcast to the blockchain and achieve great scale, just between the two of them. Eventually, if they do decide they want their coins on-chain and they want to settle, they can net out the blockchain by just broadcasting the most recent state. And then on top of this, you extend this across channels. So if Alice makes a payment to Carol, who is connected to Bob in a payment channel, but not directly to Alice, we can further extend the amount of scaling we get.

# Layers Overview

This is the issue the Lightning Network aims to serve and it does that with a layer protocol stack. Starting out at the bottom, there is the transport layer, which allows us to achieve encrypted authenticated communication between nodes in the network. There is the base layer, which describes how we communicate in this network and negotiate features. There is the update layer, which is a really interesting layer. This allows nodes to trustlessly agree on state within a payment channel -- so how much each person has -- and to trustlessly revoke past states so they can change their state and advances without the risk of a party broadcasting an old state and maybe stealing some of their coins.

We've seen a few iterations of this. So at the moment we have LN-Penalty, which is what Andrew briefly described earlier. There's also an old construction called duplex micropayment channels, which Christian Decker from Blockstream produced. Then there's a new proposal called Eltoo, which as you've heard is dependent on a new sighash opcode and has slightly different constructions as well.

Once we have an update layer we can agree on state, but we need an atomic and trustless way to transition between states. This is achieved through the HTLC, which allows us to transfer value between two participants in a payment channel. Finally, on top all of that we have Sphinx, or multi-hop layer, which allows us to propagate these HTLCs through the peer-to-peer network.

# Transport Layer

So jumping into the transport layer right at the bottom of the stack. What we want to get from this is authenticating node identity. We want to make sure we're talking to who we're talking to. We also want to do this in a way which is fingerprint-resistant, which means that if I randomly connect to a node that I do not know in the network, I cannot obtain their ID from initiating this communication protocol. So you can't figure out who someone is just by sort of brute force randomly connecting. Finally, we want transport encryption, which just makes sure that no one can read what we're transmitting and we want the usual triad of confidentiality, integrity of messages, and authentication of nodes. The tool used to achieve this is something called the Noise_XK protocol. It's a set of tools that you can arrange in various ways to get properties that you like. The one the Lightning Network has gone with is, the unknown/known variation.

So nodes in the Lightning Network announce their listening address and they sign this message and broadcast it over the gossip protocol. So when we connect to them we know that that IP is associated with that ID. However when you're making a connection you don't advertise your outbound IP. So they actually don't know who you are and they need to authenticate who you are. This requires persistent identities, so it's very different to Bitcoin, where we want all nodes to be different. In Lightning we actually need to be able to identify nodes so that we can specifically route through certain payment channels. The way that we achieve authenticated encrypted transport through the noise protocol is through a sequence of Diffie-Hellman operations in a handshake protocol. Then we hash the results of these Diffie-Hellmans into a shared secret, which we then use to encrypt all of our traffic.

# Base Layer

Once we have the transport layer, we know that we're talking to who we want to, and we can trust those messages. We need to figure out how we're going to communicate and this is achieved by the base layer. So the goal of this layer is to know how to interpret messages. So figure out the format of these messages and what they mean, and also to signal feature support so the protocol can move forward hopefully in a backwards compatible way.

Lightning's message framing is pretty simple. There is a 2-byte type which specifies the format of the payload. The type is set by the bit location, not the numeric value, so if you have type 2 it's actually the second most significant bit is set, not the numeric 2-bit is set. It also runs on a rule which is called “it's okay to be odd.” If you run into an odd typed Lightning message that you do not understand, you can still continue to communicate with that node. It's fine. It allows for backward compatibility messages. But if you run into an even one that you don't understand, you have to break your connection with that node. That's a pretty interesting difference to Bitcoin because we don't quite have a consensus in Lightning. It's just a peer-to-peer layer, so if we do end up with some ghastly interoperability bug where someone signals an even bit without us knowing about it, then we can actually break up the network by implementation quite easily.

# Payloads

Finally Lightning payloads have also recently in respect been updated to have TLV fields and this just allows for backwards-compatible expansion of existing types. One of the interesting
messages in the Lightning Network, although it was updated a week ago, so after I made my slides, is the way that we initialize nodes in the network.

The first message that we send out, this starts with the type, which has the 16th most significant bit set. It used to have the global length so a Ulint sixteen, which indicated how many global features we were signaling followed by global features and visa features that would apply to the network as a whole, affect the higher up layers of routing and HTLC's, and then followed by the local length, which would signal more local communications between nodes. If you are signaling specific features which do not affect the network as a whole they would go in here, followed by a local features set. Now these global features have recently been scrapped in the protocol. They've decided to just flatten it out and make it a lot easier and they're just replacing these two fields with a must be zero field, which is fine because they haven't actually got any global features agreed on in the specification yet. So they are going to move forward with just a flat feature set from now on.

# Update Layer

The really interesting one in Lightning is the update layer. What we need to do here is create an updated state between two peers and then trustlessly invalidate old states, so that old states cannot be broadcast. Some early iterations of this, we started out with simple payment channels which was a unidirectional payment channel. A sending party would pay in 2-of-2 multi-sig with a certain amount with the recipient party, and then as they decided to spend they would simply send over signatures for increasing amounts of bitcoin. The sending party can't release old states because they don't have the receiving party's key and the receiving party has no incentive to release old states because they're always receiving increasing amounts of bitcoin.

There's no need to revoke state in this very simple implementation. However, this is limited by your funding amount. If you put one bitcoin into this channel, you're only ever going to send one bitcoin. You can't do unit bi-directional sends. A second thing produced by Christian Decker of Blockstream is duplex micropayment channels. These channels did allow for bi-directional sends. You could commit to a funding transaction and be able to send back and forth. Instead of using one directional things these would use timestamps to revoke old states. The oldest state would start with a very long time stamp in the bitcoin transaction and that would decrease over time until you got down to zero, at which point you could no longer use the channel anymore. You can be confident that the newest state will always make it onto the blockchain first, but once you run out of timelocks you need to close your payment channel.

So what we need to do in the Lightning Network, essentially in the update layer, is allow the signing of multiple double spends from a UTXO while trustlessly revoking all but the most recent transaction. The way that the LN-Penalty update mechanism does this is by allowing revocation through a punishment where you literally steal your counterparty’s funds if they try to cheat you.

So if Alice and Bob want to open up a channel, they set up a 2-of-2 vending transaction, which currently can only be funded by one person in the protocol. Then they create a spend from this, signing all the money to the funder and none of the money to the other participant. It is important in this construction that this commitment transaction is signed before the funder releases the 2-of-2 multi-sig. Because if you just sign this 2-of-2 multi-sig and give it over to your channel party, they can just hold you hostage for all of the money in that channel. They can say, “give me half or I'm never going to sign it.” So you do have to have your first commitment transaction signed and then you can broadcast your funding transaction.

So now from this, let’s say Alice wants to send one bitcoin to Bob. We could just create another spending transaction from this multi-sig, giving Bob a little bit more bitcoin. However, both of these are valid bitcoin transactions. They both sign, they're both ready to go in the blockchain. If we did it like this, we'd create a race. If Alice could broadcast the original state where she has more bitcoin, she could get it on-chain quicker, then Bob would lose out on all his money.

What we do instead is introduce a revocation transaction, which is produced by giving your counterparty a key, which they can use to spend all of your bitcoin in all of the states. You have to relinquish this key before they will accept the new state as given. So in the first case we'd
only really have one key relinquished, so Bob would get a key in which he can spend Alice's three bitcoin, but Alice doesn't have any outputs so she would relinquish a key but it wouldn't really be necessary. So now if we want to update this next state what we would do would be first release the keys to revoke either of the old states and then update the transaction accordingly.

However, this simplified diagram has two mistakes in it, which the LN-Penalty protocol addresses. The first is that there's still a race introduced, it’s just further down the line. If Alice broadcasts the first transaction, she's still allowed to spend these two bitcoins. So if she can get that transaction on-chain before the penalty transaction gets on-chain then she gets the funds anyway and she's got away with it. The other issue is that you can't attribute blame if you have one commitment transaction spending from each funding transaction. So Bob could be sneaky and broadcast the first commitment transaction and then claim the penalty even though he was the person to break the state. The way that we address this in the LN Penalty is through something called asymmetric verbal commitment transactions. Instead of having a single commitment per state, we actually have two commitments. So one will be held by Alice, one will be signed by Bob. Each party's commitment is signed by the other party, so it just needs their signature to go on chain. It has a slightly different set of properties for each one.

If we have a look at Alice's transaction, it'll spend from the funding transaction like all updates do. However, it will first check if there's a revocation key presence. If Bob does have the revocation key for the state, he can spend it immediately. And then if Bob doesn't have the
revocation key for this update, then Alice can spend these funds after a delay.

This is pretty important in this protocol. This addresses the issue of a race for a penalty. So her funds will be locked up with a `to_self_delay`, which is negotiated upon opening of the channel. She won't be able to spend these funds on-chain until that delay has passed. That gives Bob time to watch the blockchain and see that his funds have been stolen and broadcast the penalty transactions sweeping the funds away. If he's not online during this period then he will still lose the funds. This is one of the big trade-offs in the LN-Penalty and in Lightning in general. It's actually not LN-Penalty specific. Then finally Bob’s output is completely unhindered. You cannot broadcast old states and pretend that someone has cheated you, because Bob's coins are available to him immediately. There is no revocation condition on this output.

Thinking of it from the other side, for Bob. So it's also spending from the front funding transaction, because we're double spending, off chain double spending. It still can be revoked verification key, however Bob's output is now delayed by the time lock and Alice's output is unhindered. So this solves both those problems and when we have these kind of commitments transactions you can endlessly update commitment transactions in the LN penalty model with the assurance that no old transactions will steal your money if you are online over a given period.


# Closing Channels

And once you choose to end your channel with a peer, if you want to get those funds back on chain, there are three ways you can do it. The first is a collaborative close which is when both parties agree to close the channel. In that case, they actually clear the time locks and sign a new commitment transaction which just releases funds comfortably to both parties. This is the ideal case. This is what we're hoping to see.

However at the moment, a lot of peers tend to be offline a lot in the Lightning Network. So you have to close unilaterally, which is when you can't get your peer to sign this new commitment transaction because they're offline. You just have to broadcast the latest one you have and wait for the time delay to be over.

Then finally the breach close, which we've covered a bit, is when someone broadcasts an old state and then you have to pick up that they have broadcast an old state and claim your funds back.

# LN-Penalty Tradeoffs

So we do have some tradeoffs in the LN penalty, which have already been touched on. The first one is a really harsh one -- maintaining state is critical and state grows with the number of updates you have. If you lose your states, if you lose one or two channels in your Lightning node, you're actually in a lot of trouble because you might accidentally breach close. You might accidentally close a channel which has advanced but you've lost a bit of data and then you end up losing all of your money, which I think has happened to a few people. One of the ways that you go about addressing this in the protocol is something called data loss protection, which is when you query your peers for the most recent commitment number, so you can figure out where you are relative to them when you come back online. But the big problem with this is when you go to your peer and you say, “hey, where were we again?” It's a pretty good indication that you've actually lost a bit of data and they can try and game you and take your funds anyway.

Another thing which is Lightning specific, not LN-Penalty specific, is that you have to be always online. You need to be watching on-chain for these breach closes so you can figure that out and pick up your funds. This is addressed with watchtowers in Lightning, which is the outsourcing of revocation to a third party who's always on and you rely on. However they also face a few scaling issues because they still need to maintain this ever-growing state of commitment transactions on behalf of another party. And again it’s not LN-Penalty specific. This update construction, you do have to be always on. With other update constructions like Eltoo, you need to be always on, however it addresses the ever-growing state issue which is such a big problem in LN penalty.

# Cross Payment Channels

Once we get to the ability to agree between two states we need to be able to update that state. The goals of the transfer layer is to be able to move value between parties and you need to be able to do so in an atomic and trustless way. Trustless is a word we all understand, but to do atomically, specifically we're looking at cross payment channels. This specifically means that the payment will either complete or not complete. There is no state in which it half happens and someone loses money along the way. The construction we use for this is something called HTLC, the hash lock time contract. This will pay out to a node if they can reveal something called a preimage. It's an agreement between two parties. If you give me the secret I will give you some bitcoin. If you do not give me the secret and a certain timeout is reached, I will rescind my offer and you can no longer take it.

Finally, a little Lightning penalty specific thing is that in Lightning these transactions do have a revocation pub key at the top and this is an instance where the update layer is actually leaking into the transfer layer, which is not ideal because it makes it slightly more difficult to switch out these layers if we choose to. Another thing about HTLCs, which isn't immediately apparent when you look at the script, is that from the get-go these can be redeemed with a preimage. However after the timeout, both the preimage and the timeout are valid. So you don't want to get into a state where your funds are timed out but actually the preimage has been released. Because then someone can actually claim those funds even though you timed them out, because it is a valid Bitcoin script and both of them are valid spend paths.

So that's something that really you need to be aware of in terms of the timing in the Lightning Network. The way this works in action is that if Dave wants to receive a payment, he creates a secret, so a preimage, which we’ll call R. He hashes it and he puts it an invoice which he then sends to A who is gonna pay him. Alice has a look at the network and realizes she needs to route from A to B to C to D to make this payment. She updates her channel with B to add an HTLC output to that commitment. This is using the update layer. At the moment this is irrevocably committed to, either B will provide Alice with the preimage R or Alice will take
back the funds after a certain time out. And this can happen on-chain if they just decide to close the channel or off chain if they do it so with clarity. Then when B receives this instruction to route, B will lock in a similar HTLC into this channel with the same hash but a lower time lock. This is so you make sure that they shall see you have downstream doesn't timeout before you have a chance to give them the preimage because you may have to settle on chain. Finally C will update their commitment transaction to add the HTLC in the channel with D, who will realize that they are the recipient of this payment and so they must release their preimage to C. C will have a look at this preimage and check that it matches the hash and realize that if D wanted to he could settle this channel on-chain now and claim from that script.

However because we're trying to stay off chain, they just decide to settle the channel. C updates the channel balance to give D more of the balance, the amount that was agreed on and then they clear the HTLC because it's been satisfied. However C doesn't want to send these bitcoins to D. They didn't make the original payment, so they need to pull them through the network. That's achieved by sending R back to B and clearing out the HTLC in that channel and finally sending R back to A and clearing the HTLC in that channel. This is the really great case where it all happens on chain. We know that we could enforce on-chain at any time but we're keeping the load light on the blockchain. So we have a situation where D receives the bitcoin and A has the unique preimage which can serve as a proof of payment. However this doesn't always work out if peers are offline or uncooperative, you need to go on chain.

Take the case where D relinquishes the preimage to C and they clear the HTLC, but B is offline. Now C cannot update their commitment transactions to clear this HTLC and needs to do so before two o'clock on Monday for example because that's when B can reclaim those funds as well so they might not get them. What you need to do is close that channel so the transaction needs to go on-chain and you broadcast your latest commitments sig which contains the HTLC now because C has R she can sweep the output from this transaction. So you sweep with witness data including the preimage and then you can see those coins to yourself and they cannot be swept by the timeout. Now you've got them and now C's been given her bitcoin because she claims it on chain. But now B is sitting with this HTLC. Now if the node comes back online then B can observe that the preimage is on-chain and that his channel has been
closed and then use that preimage to settle the final HTLC with Alice.

So we still have the amount of bitcoin that has been paid today. We still have the preimage which serves as a proof of payment however a channel has been closed and we have two on-chain transactions. In the difficult case, we lead to a much bigger on-chain footprint but the payment is still atomic and it will go through.

# Multi Hub Layer

The multi hub layer is right at the top and it has a few objectives. The first is to route payments through the network and to do so in a way that maintains privacy. This is one of the big trade-offs in the Lightning Network. We suffer a lot on the routing side of things because we need to have good privacy. We achieve this through a construction called Sphinx Onion Routing.

So first of all we use source based routing which means that if A is sending to E, A needs to calculate a route all the way through the network to the final node. We also do so in an onion encrypted way which means A will calculate ephemeral keys with each of the nodes along the path and create an onion which they will pass on to the next node and they can unwrap this onion using their secret. Now this node knows that it came from A and they know that it's going to C because they've unwrapped the onion but they don't know anything else about the paths. They don’t know that A is the sender; they could just be another link along the chain. They send that onion on and the same is true for every single hub along the route. They know where it comes from and they know where it goes to but they do not know where it is coming from long term or going to long term.

Another construction we use is something called Sphinx which obfuscates the length and position within a route. This is really important because you can kind of try and figure out the length of, in the Lightning Network we are limited to 20 hubs, so you can figure out where payment maybe going or coming from if you can figure out where you are in that route.

It's important to also hide that information which means we have pretty good big routing packets. We have 1300 bytes of hubs in a traditional routing packet, but it does achieve perfect privacy for the sender and near perfect privacy for the recipient. The only privacy that is damaged is the fact that the sender knows who the recipient is.

Although we have a layer two protocol, it's actually a whole bunch of layers on top of layer two. We have transport and base, which allow us to communicate privately and securely. We have the update layer which can be swapped out at any point if we choose to. The transfer layer which is the HTLC which except for a small leak from the LN penalty is pretty isolated. Then the Sphinx routing layer which allows us to communicate across a network of channels.

Thank you.

Applause

# Q&A

Audience Member asks a question (inaudible)

Carla: I think that you can figure out multi-party channels in LN penalty. It's just a bit more challenging, but I would have to look deep into that specification. I think Eltoo does make for much easier multi-party channels.

Audience Member asks a question (inaudible)

Carla: Right. Obviously I can't speak for the Lightning Network as a whole. I would say from my perspective with the current LN penalty mechanism, I think addressing the data loss side of things is really critical. So when you are requiring users to have perfect state, perfectly backed up databases, I think that's still a risk. That's not something you can expect of regular users so I'd say that that's the big milestone. But I know that having in terms of limitations of the network the ability to make larger channels has been agreed on for the 1.1 spec, so it's definitely moving in that direction, where we are becoming more mainstream and more stable.

Audience Member: You talked about the revocation….(inaudible)

Carla: Yeah, it does. So you wouldn't have to have the revocation key in the HTLC because L2 allows you to just cover all your previous states with one transaction, with the newest transaction

Audience Member asks a question (inaudible)

Carla: I would say that the opening and closing of channels would be changed to a tapscript. So that would mean that the opening closing in channels on-chain would be indistinguishable in the good typescript case from any other transaction. That would really enhance privacy a lot and I think will be a big win for everyone.

Audience Member speaks (inaudible)

Carla: Thank you everyone.
