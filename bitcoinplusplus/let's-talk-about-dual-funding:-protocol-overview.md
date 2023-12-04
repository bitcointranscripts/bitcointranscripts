---
title: "Let's Talk About Dual Funding: Protocol Overview"
transcript_by: saltykate via review.btctranscripts.com
media: https://www.youtube.com/watch?v=OFMU1xV5uQk
tags: ["lightning","dual funding","Dual Funded Channels","Multisig"]
speakers: ["Lisa Neigut"]
categories: ["conference"]
date: 2023-03-16
---
# Dual Funding Protocol Overview

## Unspent Transactions Output
Unspent transaction object is locked up.
Bitcoin is unspent, but it requires two parties to sign.
In order to spend it, you need two people to sign off on it.
How do we make that happen?
Multisig that two people sign off, 2 of 2 multisig.

## Lightning Channels and Multisig, Bitcoin Script and the Lightning protocol
We're talking about lightning channels.
A lightning channel is a UTXO that is locked up with a 2 of 2.
The process of opening a lightning channel, what does that involve?
We want to open a channel.
That means where two people, lightning nodes, are going to make a 2 of 2 outputs.
What does that mean?
What does it take to make a 2 of 2 output?
It's a script.
What does a Bitcoin script do?
It helps you lock up Bitcoins.
It locks Bitcoins up.
This is how you write contracts.
You write programs in Bitcoin writing Bitcoin scripts.
This is the script definition for opening a Lightning channel.
The reason we're going through this is so we know what we need to open a channel.
We need some information.
Two parties are going to come together.
Lightning is a protocol.
What is protocol design?
Protocol is figuring out what two people need to communicate to accomplish a task?
Most protocols are two people talking.
You can get multi-party ones if they're complicated.
Lightning is written, you have two people having a conversation.
We need to figure out what they need to tell each other so that we can make it UTXO on chain.
What we want to do is make it 2 of 2 multisig.
And we want to end up with a UTXO at the end of this process.
We need to know what we need to talk about in our conversation to make this happen.
In order to know what we should talk about, we need to know what we're putting information into.
This is the script that we're going to put on chain.

##Open Lightning Channel Between Two Nodes and Checking Multisig with Pubkeys 
Notice there's two things we're missing "OP_2 <pubkey1> <pubkey2> OP_2 
    OP_CHECKMULTISIG"

We're missing a pubkey1 and a pubkey2.
To check how multisig works we watch a check_multisig.
The point is that in order to make this script, there's two items, two pieces of information we need, we need one pubkey and we need two pubkeys.

## Checking Signatures Match
The general idea behind a check multisig is you're going to need a signature that matches each of the pubkeys.
There are two pubkeys in here,  pubkey1 and pubkey2, one from each participant.
You are going to be given a pubkey, and you're going to put it into this contract, then you lock the money up on chain.
It can't move anywhere unless both of these pubkeys sign off.
To build this, we need to get a pubkey for the other party.
Everyone knows that we have a transaction.
You have a list of inputs, and then you have a list of outputs.
One of these list of outputs needs to be a 2 of 2 multisig.
Historically, anyone using V1 channel opens on lightning.
The way that this works on two nodes is you have node1, and then on the other side of the channel, you have node2 talking to each other.
Node1 is going to send a message to node2 saying, I want to open a channel.
Part of that message is that I have pubkey1 and going to send that over to node2.
Node2 is going to get that message.
Node2 is going to send a message back and say no,  and hang up on you and the end of the conversation.
They can do that and just end the conversation.
They don't have to talk to you, but if they say yes, you can open a channel to me, here's Pubkey2.
That's how we send each other pubkeys back and forth.

## [Lightning Network In-Progress Specifications](https://github.com/lightning/bolts) 

We're talking about [Channel Establishment](https://github.com/lightning/bolts/blob/master/02-peer-protocol.md#channel-establishment) building and opening a channel.
The official name is Open Channel "open_channel"  the formal name for this response is Accept Channel "accept_channel" - open channel/accept channel.
What's inside the message they're actually sending.
More info than just the pubkey.
Funding is how much money you want to put in a channel.
Push inside is how much money I want you to have.
The funding pubkey.
There's an object, a piece of info called funding pubkey, which I've been calling pubkey1.
There is a message that  everyone can see.
You send to node2, and has all this information.
The funding pubkey is the pubkey, and then 2 of 2 multisig scripts are the funding transaction output.
The spec writes out exactly how you should consider each of these things.
The other node sends back the accept channel message.
Part of this is their pubkey but hey also have a funding pubkey.
They also send back a funding pubkey which is also known as pubkey2 "funding_pubkey (pubkey2)".
## Exchange Signatures
At the end of these two message exchanges, both parties know what pubkey1 and pubkey2.
Node1 sent pubkey1 to node2, and node2 responded back with pubkey2 "OP_2 <pubkey1> <pubkey2> OP_2_CHECKMULTISIG" and veryone has everything they need to build.
Everyone has everything they need to fill in all the blanks.
We can make a locking script for our Bitcoin, and we can send our Bitcoin to this output, and we have a channel.
We have all the info we need to open a channel.
You can send bitcoins.
Let's say we have an enormous amount of bitcoin.
Five bitcoin.
We send some money to BTC address.
5 btc ==> btc address.
It takes two signals.
The way it works is node1 is going to send money to this address, locking up their money into this address.
Node1 is makes a transaction to the Bitcoin address.
In order to move their 5 bitcoin, they need a sign off from node2.
Node2 needs to sign to move the 5 bitcoin.
What are some downsides to doing this?
When the channel opens, who has Bitcoin that they can spend in the channel?
Only node1.
node1 sent money to that address and node2 knows the address.
Node2 could also just send money to that address.
Everyone knows what the address is.
What if we just all start sending money to the address?
We'll have lots of UTXOs with money locked into it.
This is a problem though,as the protocol only supports once you send money to the transactions.
Signature from node2 is needed to spend it.
If you send money to this Bitcoin address and don't already have the ability to spend it already and your peer disappears, five Bitcoin is lost.
You send five bitcoin to an address, and someone else, some rando node on the internet, gave you a pubkey that you locked up the money with, and you cannot get your money back without their signature.
This is not good idea.
More needed in the protocol, and "open_channel", needed before we send money to this address.

## Downsides to Putting Money in Channel

The new protocol isn't going to fix thise.
Downsides are that only one side can put money into a channle open.
You rdon't want to send money to the open address, until you know you can spend it.
You send money to an address, but you want to make sure you can spend from that address before you send money there.
I've had some people that did that a few years ago for Lightning, and changed the protocol work to give them more ability to use any wallet.
They wanted to open a Lightning channel, and they sent money to an address without getting the ability to spend it first.
The other node went away and closed the channel, and it was lost forever.
Node1, after receiving accept channel, is going to build the transaction.
A transaction that sends money to that address, because now they can make that address.
Node1 builds a transaction that sends money to node2.
Node1 sends the TXID and the funding out point, the V out, called funding out point "txid, vout (funding outpoint)" This tells node2 where to look for money on chain that will be found in channel open.
Node2 is notified and node1 builds the transaction, and sends to node2 the information and a signature.
We're sending an output number.
These two pieces of information uniquely identify where you see your Bitcoin on chain.
Not sent yet.
This is pre-planning for node1.
We send a signature, lets node2 rescue their money if this transaction ends up on chain.
When I send the money to this address, you can use this signature from me, along with your own signature, to rescue the money.
Node2 can get their money back if something goes wrong with the funding output.
If I send all my money to it and then disappear, node2 in theory could get their money out.
Node2 receives, and sends back another message include their signature so that node1 can then get their money out.
Once node1 has a signature from node2, the transaction is sent.
Permission is needed from peer to get your money out of that address before you send anything to that address.
This is called the signature and called a commitment transaction.
The next message is a funding sign message and inside of it, is a signature.
A message called funding sign.
Transaction is sent and both sides wait for the funding, for the channel to open, and wait for the transaction that has the script that locks all the money up.
Waiting for the output that has node1's money to get mined into a block and confirmed to certain depth.

## Channel Ready Lock Transaction and Broadcast to Blockchain

When the channel opens, we send a message, called channel ready.
Both nodes send "channel_ready", when node1 sees transaction is mined,after certain number of negotiate blocks,  node1 will send a channel ready.
To recap, two people want to talk to  have a conversation about opening a channel, they exchange pub keys, and exchange signatures.
Once they get their signatures, the person who built the transaction sends the transaction out to the blockchain, and as soon as it gets mined that channels considered open and existing.

## Dealing with Liquidity

Drawbacks are that the money is only on one side.
The problem or why that is sub-optimal is there's no liquidity.
You can receive payments, but you can't send payments one way.
Every channel that opens in Bitcoin and lightning gun can only send one way every time a new channel opens.
If you want to send money in the opposite direction you need to make a payment or convince someone else to open a channel with you (towards you).
This costs money as every time you want to open a channel you make an on-chain transaction, and that has a world cost.
You could push a channel to peer, but you don't know the other node you're opening it with, a semi-anonymous set of people with money in the channel.
Common ownership risk, because only one person opened it, all funds in that channel open belong to the same party.
Its only 1 of the 2  in there.
It hard for new nodes to get inbound liquidity.

## Receiving Payments Without liquidity

In the real world, you can't receive payments.
Receiving payments over Lightning is hard.
If you wanted to open a cookie shop, it would be very difficult to get people to accept payments over Lightning because you need other people to open channels to you in order to receive incoming payments.
You have to spend the same amount that you receive, or pre-spend it to have the inbound liquidity, which is not very profitable.

## Getting Inbound Liquidity with a Protocol that Receives UTXOs from Two Parties

We want to make it easier to get inbound.
In order to do that, built the transaction together.
Make a protocol where everyone can put money into the channel at open.
Build a transaction that has UTXOs from two parties, one transaction with UTXOs from both people.
A transaction is a list of inputs and then a list of outputs.
Two people could talk and put input from node1 and input from node2, and these outputs are the channel funding, the 2 of 2 multisig.
Leaving the change output for node1, and change output for node2.
If inputs for node1 is 10btc, and for node2 is 5btc, and the funding output for the multisig is 8btc, derived from node1 (6 btc) and node2 (2 btc).
The change output for node1 is 4btc and for node2 is 3btc.
This is like a joint account you've created and it becomes hard to tell where the Bitcoin went because some of it went into a joint account and you don't know who has how much at the start.
Benefits are both nodes will have money in the channel and makes it possible that both can both send and receive immediately through this channel.
amounts differ, but you get or receive payments all at once.
You get some savings by having one channel deployed.
When designing a protocol, the first thing you figure out is what you want to do, what information to shared to achieve our goal.
Goal is to build a transaction together, and have a transaction.
Both sides need to know all the information.
We want both sides to be able to build a transaction.
Now we send information about the transaction over the wire.

##  Construction of Interactive Transaction Protocol

We needed a new protocol.
One way to think of protocol is like a closed conversation, what am I allowed to say back and forth?
Like writing a script in a play for two actors that are very dry robots.
We came up with an interactive transaction construction protocol.
We use this for splicing and reuse the same protocol, because splicing does the same work of making a new transaction with two parties.
The same work and with different setup and a different ending, but the middle part of when you're building the transaction is the same.
The way we constructed the transaction makes building a transaction with parties that are just the two that are having the conversation.
There is plausible deniability about who the inputs you're sending to your peer belong to.
Whereas, if you do it in a batch transaction way, you can't lose that capability.
Whether or not this is something we should preserve and lightening is maybe a question, but you can do cool stuff with it.
Lets you build, open start multiple channel opens at the same time and build one transaction that opens multiple  channels in the same transaction.
You get decentralized multi-party transaction that anyone who runs the Lightning node can kick off any time they want.
It just looks like outputs for the other nodes.

## Core Lightning
This is implement on Core Lightning already.
Everything I'm talking about today exists on Core Lightning.
Core Lightning is implemented, a project I work on [interactive_tx: Add dual funding flow](https://github.com/lightning/bolts/pull/851).
Eclair, a French team that does Lightning, has also implemented it.
We are in final stages.This pull request is proposal.
I made a whole video where I explain it too, so if you want to watch me watch through another video where I explain how it works, there's that exists in the pull request.
We have now changed channel establishment and have this whole section of new stuff called the interactive transaction construction.

## RBF (replace by fee)

We have ability to do RBF now.
If you attempt to open a channel and want renegotiate it, we give you a protocol to be able to attempt to RBF with the collaboration of both funders.
This is how we were walking through how it works.
Node1 is going to send a message, after picking a node that you want to open a channel with.
Liquidity ads is supposed to help with who am I opening a channel with question and expectation of them to put money in.
There is coordination of how you coordinate that someone's going to put money in the channel with you as liquidity.
I'm going to open a channel with you,  send you an open channel message, and open a channel that's going to have a whole bunch of information in it about my pubkey and previous information we covered.
The other side will agree to open a channel  accept your proposal to open a channel.

## Transaction Collaboration Communication for Transactions

We get into a section that I call transaction collaboration, where we send each other the inputs and outputs and communicate, the input(s) that I want to add to a channel.
One by one, each of you takes a turn and if don't have anything to add, you decline.
As soon as you get two people decline or pass, it ends.
We're both gonna have the same set of inputs and outputs, and take this information that we've sent each other, and we're going to build a transaction with what each party wants to add.
Each input gets registered separately, non-batched.
You can get inputs from a third party and send them and get kind of a ladder effect.
If you want third party inputs, then ownership groups are a lot more difficult.
It's possible that someone could send you complete junk and you build a transaction that they can't send you valid signatures for, in that case, well you just lost some time.
Each one solves it by signing a single user transaction with that input already that the merchant could broadcast.

##  Relationship Between UTXOs

There's a possibility that you link UTXOs for each other, but a thought in Lightning is that your UTXOs aren't as important in Lightning as they are for payments.
They represent the ability to make batches of payments.
There's less of a relationship between your UTXOs and the amount of payments that represents.
You're talking about UTXOs that actually end up in the channel.
There's plausible deniability that it's not your UTXO, that's why it's not batched, and we preserve the deniability that they're not your UTXOs.  We also have the ability to remove inputs and outputs, so you could add and then remove them later.
If you had a third party that was in the new notation and then dropped out, you could remove them.

##  Construct Exchange and Spend and Exchange Signatures to Broadcast

After you construct the transaction, exchange signatures that let you spend from that transaction, and then spend from that transaction.
This means you don't want to publish the transaction before you have signature it.
The last thing you do is you exchange signatures to broadcast and you spend the funding transaction.
There are more steps than original one, more messages and communication needs to happen.
Go back to this PR  851 [PR851](https://github.com/lightning/bolts/pull/851), to learn more about how to make this work.
Look up multi-fund channel and command for establishing multiple Lightning channels.
If you do the request amount, there's a few little parameters in here you can add to each of them to buy liquidity ads.
The liquidity ad is how to coordination and convince your peer to put money in the channel, and incentivize them, by offering to  put money in the channel and pay you for it.
The liquidity ad is a coordination mechanism and you get multi-fund channel with multiple channels that you buy liquidity from at the same time.
That is how you would get a decentralized, self-coordinated fund join.
