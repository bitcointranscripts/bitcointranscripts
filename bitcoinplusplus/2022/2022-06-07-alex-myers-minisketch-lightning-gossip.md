---
title: Minisketch and Lightning gossip
transcript_by: Michael Folkson
tags:
  - lightning
  - P2P
speakers:
  - Alex Myers
date: 2022-06-07
media: https://www.youtube.com/watch?v=e0u59hSsmio
---
Location: Bitcoin++

Slides: <https://endothermic.dev/presentations/magical-minisketch>

Rusty Russell on using Minisketch for Lightning gossip: <https://gnusha.org/url/https://lists.linuxfoundation.org/pipermail/lightning-dev/2018-December/001741.html>

Minisketch library: <https://github.com/sipa/minisketch>

Bitcoin Core PR review club on Minisketch (3 sessions):

<https://bitcoincore.reviews/minisketch-26>

<https://bitcoincore.reviews/minisketch-26-2>

<https://bitcoincore.reviews/minisketch>



# Introduction

Pretty new to Lightning Network development, joined the Core Lightning team. I’m going to present on Minisketch and what I’ve learnt about the gossip network.

# Topics

I am going to go over the role of gossip in the Lightning Network. Is everyone familiar with Lightning or at least semi enthusiast? I am not going to spend too much time on the background of how Lightning works. But I will explain how gossip ties into it. I’ll try to give a high level overview of how Minisketch works, go through an example and then explain how we can use this to improve Lightning gossip.

# Role of gossip

The role of gossip in the Lightning Network, I thought it would be fun to explain this through examples. We are going to dive into a basic Lightning transaction.

# Make a Lightning payment

For an average user I figured it is probably like pull out your mobile app, you are presented with a QR code or an invoice so you scan that. Then on your app it gives you the memo with the notes, you verify the amount looks roughly correct and you hit Send. WIth any luck a moment later you get your little green check box showing that it was successful. Given we are enthusiasts here I think we should go a level deeper and see what was going on behind the scenes.

# Lightning Payment - Enhance

In Core Lightning at least there are a lot of CLI commands we can use to get some more information.

`lightning-cli listpays <BOLT 11>`

In this case we can see that it did indeed went through. It looks complete, there’s the preimage, that is kind of like our receipt of payment on the Lightning Network. Interestingly down here we see that this was split into 12 different parts. That’s 12 different routes that were calculated and all filled in order to fulfil that invoice.

`lightning-cli listpaystatus <BOLT 11>`

Let’s go one level deeper. We can see that it wasn’t just 12 routes that were attempted, there were actually 53 different payment attempts. That is part of a multipart payment. Some of those timed out. We got some errors before it was successful. This particular CLI command, it prints out pages of data. But we can actually tell on each failure how many hops deep that was and we get this text encoded string here (`0x1007…`). If we feed that into another tool (devtools/decodemsg) we can actually decode this. This part of BOLT 4. It specifies that `1007` means we had a `temporary_channel_failure`. We actually included in there a channel update (`0x1000`, new channel update enclosed). There is a complete channel update packet. That intermediate node, it doesn’t know who we are because everything is onion routed, it doesn’t know where we are trying to get. It is saying “Whatever you are doing I think you are barking up the wrong tree. You obviously have some outdated information and I think you need to see this.” In this particular case we can see we’ve got information on what sort of fees this particular channel charges, what the `cltv_expiry_delta` is, how many blocks we need to add for that timeout. The important part is right here, `channel_flags=1`. It doesn’t sound like much but this is the flag you look up in the protocol and it says this channel is disabled. Obviously when we were calculating a route we didn’t have that information and that was why this particular route failed.

# Lightning Payment - Takeaway

So basic example, what did we learn? There were 70 different channels that were utilized to make this payment. Even on a fairly simple scenario. On some of them we have outdated information but we were able to retrieve some new gossip there, update the routing graph which is kind of like our map of what the network looks like. With that new information we were able to recalculate our paths such that we were able to ultimately succeed and make a payment.

# Role of Gossip

Backing up, starting from a high level now, what is generally the role of gossip in the network? It is kind of just like in real life. Gossip is second hand information that you share about peers who you are not directly communicating with. In the Lightning Network we have got all these different nodes that are connected. We might have direct connections to a handful of them but if we are down here in that lower left corner we need to collect information on all the different nodes that are out there. We do this in the form of a gossip message called the `node_announcement`. This one gives the public key of every node and it also gives addresses for how to reach them if we wanted to connect to them directly. That’s like your IP address, onion address or web socket, anything you can dream up you can include that in the node announcement. The next thing we need to know is where the channels are. We have got a `channel_announcement` type. All that really does is it says between node A and node B there exists a channel and it was funded with a transaction on the blockchain. It lists the short channel ID which is everything you need to look it up and see which UTXO on the blockchain funded it. That part in particular is not great for privacy but it is really good to prevent denial of service. You have to prove that you have a UTXO to open the channel. Now we have the basic topography of the network if we wanted to route across it. It helps to have a little bit more information. We get this in the form of a `channel_update`. This is stuff like fees or if the channel has a max HTLC size set too low or is otherwise disabled like we saw in those examples. Those are things where we would want to eliminate that from our choices when we go to calculate a route.

Now we have everything we need to be able to construct our route. Why did I call this talk the Lightning Gossip Network? Aren’t we just talking about the Lightning Network? The short answer is not really. It is a little bit different in that we see all the connections we have, the channels between nodes on the Lightning Network. But when we talk about gossip we are actually only communicating with a subset of those. Depending on the implementation, Core Lightning uses 5 peers I think, it is anywhere between 3 and 5 that you’re connected with and gossiping with. It doesn’t have to be one of your peers that you are gossiping with. You can gossip with any nodes. It doesn’t even have to be a node so long as there is a machine out there that knows the protocol and is providing new information that you didn’t have from your other peers about gossip. We are totally happy communicating back and forth with you and gathering new information on the state of the network. The last important detail about it, it operates by flood propagation. Say you are connected to 5 peers, you receive information from one peer and if it is new information you rebroadcast that to 4 other peers. This is really efficient early on in the propagation because you quickly fan out the information to all the peers. But even after several hops it starts to lose efficacy. All of a sudden from multiple sources you are seeing the same data, you are losing efficiency.

# Gossip Statistics

Some basic statistics on the state of the Lightning Network. Right now we’ve got 80,000 different channels and 17,000 different public nodes. Going back to that flood propagation, if we are looking at the bare minimum of three connected gossiping peers, that means in order to fan out and reach the entire network we are looking at a minimum of 14 hops. There is kind of like rate limiting built in to gossip propagation. You actually batch all the gossip you receive and you wait 60-90 seconds. Core Lightning uses 60 seconds but I think LND maybe uses a 90 second cycle. You periodically broadcast all the new gossip you receive in that time to your gossip peers. That means that we are looking at 14 hops, 60-90 seconds between each one. It takes a while to fully propagate to the whole network. In practice we are seeing something like 95 percent of the network receives it within 13 minutes. You probably need 20 minutes, a good rule of thumb at minimum, before you can count on everyone seeing the new information.

# What is Minisketch?

Switching gears, I am going to try to explain Minisketch. I will do my best here. It is a set reconciliation protocol. Set reconciliation, we have two datasets, you can see with this Venn diagram that they are largely overlapping. In this case they both have valid data and we want to make sure that we get some of that data, make sure both of them are updated with it. In this case we are interested in the symmetric difference between the sets. That is what Minisketch helps us do. If you are like I was a few months ago you might think that this is a hard problem to solve, there is going to be some overhead in trying to reconcile these two sets. You are going to send more information than is strictly required. You don’t know what your peer doesn’t have. But like me you would be wrong. Minisketch has some really cool properties.

# Background

It actually comes from a family of error correction codes called BCH error correction. It uses a map like the Berlekamp-Massey algorithm. I am going to go through a really brief high level example.

# BCH Example

Imagine we have two sets of data. They contain the elements (1,2,3) and (1,2,3,4). A cool trick we can do if we want to reconcile these sets and make sure both of them have all the data. We take a sum of the elements. Here we have got 6 and 10. If we are on the left side we want to transmit to this set on the right. “Here is my sum. It is 6. We can take the difference (10-6) and we arrive at 4 which is our missing element.” Ok cool property but we are basically just doing subtraction here. This is how it works with exactly one element. Any more and there is obviously no way we can do anything. But we can actually do another trick where say we want to encode 2 differences, we can take the simple sum of the elements in this array… Here’s our array, the first element is the sum of the elements. The next element of our array is the sum of the squares. I’ve done this basic math. This is the data in this array that we are going to transmit to the other guy. It is twice as much to reconcile two differences now. We can take the difference here. We say “That difference is the sum of the elements and this one is the sum of the squares.” Thinking back to algebra we’ve got two equations, two unknowns. That means it is solvable. As this order gets harder it becomes a really difficult problem. That’s where the Berlekamp-Massey algorithm comes in. It is a really efficient way to solve this.

# Constructing a large sketch

We can use this for an arbitrarily large set size. We can go all the way up to an order of n. Obviously it takes a little longer the higher this order goes. You have to encode every entry that you have up to the nth order. But it does work and we can resolve a large number of differences with it.

# Minisketch

Minisketch library: <https://github.com/sipa/minisketch>

Minisketch is a C++ library that was developed by Pieter Wuille. It is implementing the PinSketch algorithm. It runs on a wide range of architectures and hardware. It is optimized with some tables to help solve the roots in a time efficient manner. He has also got a pure Python implementation which is really impressive in itself. It can do all the calculations in like 500 lines of code that kind of blows my mind. It is pretty accessible, I encourage you to check out this GitHub page.

# Using Minisketch

But supposing you are just an engineer like me. How do we use this fancy math in practice? It looks something like this. First we initialize a sketch and in order to do that we need to know what’s the width of the data that we want to encode. In this case we are talking 64 bits wide. We give it 64 bits and then we need to tell it the capacity. This is how many differences do we want to be able to reconcile between the two sets. If we think we are going to have about 5 differences between them we might choose something like 8 just to make sure we are covered. But we don’t want to get too carried away. Then we add our data and we calculate the syndromes. That is like each line of the “Constructing a large sketch” array. Then we serialize and transmit that over from Alice to Bob. Bob goes through the exact same procedure. He builds his sketch and he merges the two together. It is pretty interesting. He needs to choose the same data width but his capacity can actually be different. The way that the math works out is you can actually truncate this array at any point so that they’re equal and then you can merge those two sketches. You lose some of your capacity there but they are able to be solved just fine. Then you use that Berlekamp-Massey algorithm, that solves it and the result is all the data that you are missing between the two.

# Black Box Properties

What properties does this have as we use it? It can support anywhere from 2 to 64 bit wide data. The really cool thing is that the serialized size that you are transmitting between the peers is actually the sketch capacity, the number of entities that you want to resolve, times the data width. If you choose that sketch capacity just right it is like 100 percent efficient in how much data you can get out of it.

`Serialized size = sketch capacity * data width`

That part really blew my mind. Some other things to keep in mind. As you increase sketch capacity the reconciliation time scales (linearly) up. Depending on the number of differences that you actually have to resolve, that scales quadratically. You want to keep the differences bounded. You don’t want to get too carried away with how big the set differences are there.

# Limitations

A couple of basic considerations to keep in mind. You can’t encode an element of zero when we initialize our sketch. You can choose any number apart from zero. The other thing is it is also generally helpful to make sure that the number of elements that are in each sketch, that they are not so different that they exceed the sketch capacity. Normally this isn’t a problem but if you imagine you have 50 entries in one sketch and 100 entries in the other and your sketch capacity is only 10. There is no way it is ever going to solve because the capacity is just not there. The cool thing is that it gives you a warning if it can’t solve it. It says “I can’t find any polynomial that actually satisfies this equation”. That works most of the time.

# Erlay

Some background on how we are going to use this. Bitcoin ran into a fairly similar problem that Lightning Network gossip is facing. They were faced with the issue of transaction relay also not scaling very well with flood propagation. If you are familiar with the Erlay protocol, that’s what Minisketch was actually developed for. Erlay uses this to encode each transaction that is in the mempool. You want to share that with peer Bitcoin nodes. Those are 32 byte transaction IDs. Obviously we are limited to only 8 bytes with Minisketch. So we need to compress that down to a smaller fingerprint where we know what transaction we are talking about. There is a hash function to do that. They reconcile inventory sets in order to do that. That’s another element that complicates a little. Say we have the whole mempool, one way you could do it is encode every single transaction in there into a sketch. All the peers do that. They resolve it and they see what differences they have. That’s not actually how Erlay works. What Erlay does is it keeps track of each peer that it is communicating with and it says “It has been 15 seconds since we last talked. I am keeping an inventory of everything that I wanted to tell you about but I haven’t yet. Here’s 5 items that I’ve been meaning to tell you about.” Meanwhile your peer, Bob over there, he’s doing the same but maybe he collected 7 items. Instead of encoding however many thousand items in the mempool, it is really just the 5 items and the 7 items. We reconcile those and maybe we find that there is only 3 differences between the two. Once those are reconciled those inventory sets are zeroed out and they are ready for the next round that is going to take place in another 15 seconds.

# LN Gossip vs Bitcoin tx relay

The problem that Bitcoin faced with transaction relay was pretty similar but there are a few differences. For one, any time you introduce that short hash function that produces a 64 bit fingerprint you have to be concerned with collisions between hash functions. Someone could potentially take advantage of that and grind out a hash that would resolve to the same fingerprint. That would be a denial of service vector. There’s some concerns like that. Also timing analysis with transactions that were private. We don’t have to deal with hiding those things with gossip because it is public by nature. Also instead of having to use that hash function we have a trick that I’ll get to in a moment. We don’t just have a single data type, we have 3 different messages that we want to relay.

# Application to Gossip

Those messages are the `channel_update`, the `node_announcement` and the `channel_announcement`. Of these the `channel_update`, that’s your fees, whether the channels are active or disabled, what’s the maximum HTLC it can support, that kind of thing. That is like 97 percent of the network traffic, that is the big one that we want to make more efficient. These top two (`channel_update`, `node_announcement`), they are only valid for a 2 week period. These are repeatedly broadcast.

# Challenge

Our challenge is we encode all 3 of these message types. We can only use 8 bytes but we have a tool in the form of the short channel ID (SCID). That is what links a channel to the funding transaction on the blockchain. By its nature there can only be one unique transaction on the blockchain. That’s a cool shortcut we can use. On this `node_announcement` this doesn’t have any channels linked to it so it is kind of hard to use the short channel ID here. Ideally we would like to refer to the node ID, the public key of the node. But unfortunately that is 32 bytes so we’d have to hash it or something.

# Encoding Scheme

But what we can actually do when we encode this is use these elements here (block height, transaction index, output index), this is the short channel ID. We can refer to a node announcement by just saying “Here’s the node’s oldest channel” and we just point to which side of the channel that node is on. That way we have a way to canonically identify which node we are talking about. This is normally 8 bytes of data and we are trying to fit the whole thing into 8 bytes. What we have done is shaved off a few bits that we don’t really need. If we can get 32,000 transactions into a block that’s probably sufficient. If you are funding a Lightning channel you are probably not going to have like 1000 outputs. We have saved a few bytes here. Now we have room to leave for a couple of bits, which message type we are talking about and which side of the channel that is on. This is the way we can identify in just 64 bits exactly what the gossip message is we are talking about. Finally we have the timestamp. For those periodic messages we need to know which ones the new one, which one is the old one. Having some bits down there to differentiate those is helpful.

# Set Reconciliation benefits

What does this buy us? The short answer is we can save at least 60 percent on bandwidth and such for gossip. Now we’ve done this we can communicate with more peers. Communicating with more peers is really great because that increases the reliability of gossip propagation. In particular node announcements have suffered in the past because the other two types you have some simple heuristics to figure out if you are probably missing one of them. For a channel update we saw in that example at the beginning, the worst case scenario is we fail a route and that error packet would get an update anyway. We can get some of the other data types back but node announcements, that tells you the IP address of the peer to connect to. If they change that and you never see it you might not be able to connect to your peer. That one is really catastrophic and should really benefit from the increased reliability.

# What’s next?

I still have a couple outstanding issues to decide upon. One of these is we can keep either global sketches or we can do the per-peer sketches with inventory sets. There are arguments for both. Another thing is we also have rate limits when we accept gossip. If we are rate limiting gossip pretty aggressively this really cuts into our sketch capacity. It would be nice for the implementations that opt into this set reconciliation if everyone can agree on a common criteria for when to rate limit. I’m for using the block height. I’m trying to get everyone onboard, if we can link each gossip message to the current block height. Let’s say you get one message per block height or for every 100 blocks or something. That’s really easy for anyone to validate since you are already running a full node anyway. Then finally in the future we’d really like to get away from the short channel ID in gossip because it does leak privacy. You don’t really want to dox all your onchain UTXOs. We are not quite ready for that just yet but when we do it is going to lead to this per peer inventory set solution. That will probably inform this decision.

# Conclusion

Gossip is what lets us build our graph view of the entire Lightning Network and find a route. Minisketch is really cool, everyone should check it out. Hopefully we will be able to use it to improve the reliability of Lightning Network gossip. Here’s my contact info if you want to follow my work. You can see some of it on the lightning-dev mailing list. I’m endothermicdev on GitHub and Twitter. Feel free to reach out.

