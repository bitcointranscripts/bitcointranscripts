---
title: 'Let''s Talk About Dual Funding: Protocol Overview'
transcript_by: saltykate via review.btctranscripts.com
media: https://www.youtube.com/watch?v=OFMU1xV5uQk
tags:
  - lightning
  - dual-funding
speakers:
  - Lisa Neigut
date: 2023-03-16
---
## Openning a Lightning Channel

Unspent transaction output is locked up.
Bitcoin is unspent, but it requires two parties to sign.
In order to spend it, you need two people to sign off on it.
How do we make that happen?
A multisig that two people sign off, so it's 2 of 2 multisig.

We're talking about lightning channels.
A lightning channel is a UTXO that is locked up with a 2 of 2 (multisig).
The process of opening a lightning channel, what does that involve?
We want to open a channel.
That means where two people (lightning nodes) are going to make a 2 of 2 output.
What does that mean?
What does it take to make a 2 of 2 output?

What does a Bitcoin script do?
It locks Bitcoins up.
This is how you write contracts.
How you write programs in Bitcoin is you write Bitcoin scripts.
This is the script definition for opening a Lightning channel.
`OP_2 <pubkey1> <pubkey2> OP_2 OP_CHECKMULTISIG`
The reason we're going through this is so we know what we need to open a channel.
We need some information.
Two parties are going to come together.

Lightning is a protocol.
What is protocol design?
Protocol is figuring out what two people need to communicate to accomplish a task.
Most protocols are two people talking.
You can get multi-party ones if they're complicated.
Lightning is all written, you have two people having a conversation.
We need to figure out what they need to tell each other so that we can make a UTXO on-chain.
We want to end up with one of these (referring to the multisig) at the end of this process.
We're going to have a conversation.
And we need to know what we need to talk about in our conversation to make this happen.
In order to know what we should talk about, we need to know what we're putting information into.

### The multisig (OP_CHECKMULTISIG)

This is the script that we're going to put on-chain.
`OP_2 <pubkey1> <pubkey2> OP_2 OP_CHECKMULTISIG`
Notice there's two things we're missing.

We're missing a pubkey1 and a pubkey2.
In order to make this script, there's two items, two pieces of information we need, we need one pubkey and we need two pubkeys.
The general idea behind `OP_CHECKMULTISIG` is you're going to need a signature that matches each of the pubkeys.
There are two pubkeys in here, `<pubkey1>` and `<pubkey2>`, one from each participant.
You are going to be given a pubkey, and you're going to put it into this contract, then you lock the money up on-chain.
It can't move anywhere unless both of these pubkeys sign off.
To build this, we need to get a pubkey for the other party.
(In a transaction) You have a list of inputs, and then you have a list of outputs.
One of these listed outputs needs to be a 2 of 2 multisig.

### Getting a pubkey from each party

The way that this works on two nodes is you have node1, and then on the other side of the channel, you have node2 talking to each other.
Node1 is going to send a message to node2 saying, I want to open a channel.
Part of that message is that I have pubkey1 and going to send that over to node2.
Node2 is going to get that message.
Node2 is going to send a message back and say no, and hang up on you.
They can do that and just end the conversation.
They don't have to talk to you if they don't want to.
But let's say that they're like "sure, you can open a channel to me, here's a pubkey too".
That's how we send each other pubkeys back and forth.
You might be like, Lisa, what?
Surely this is not what specs look like, right?
It doesn't look much different at all, let's go find it.

So what is [the specification](https://github.com/lightning/bolts)?
It's just literally writing out this stuff like this, except in a little fancier terminology.
We're talking about [Channel Establishment](https://github.com/lightning/bolts/blob/master/02-peer-protocol.md#channel-establishment) building and opening a channel.
The official name for "Hey, I want to open a channel" is `open_channel`.
The formal name for this response is `accept_channel` - open channel/accept channel.
What's inside the message they're actually sending.
More info than just the pubkey.
`funding_satoshis` is how much money you want to put in a channel.
`push_msat` is how much money I'm just giving you because I decided I want you to have it - it's a bribe, sort of.
There's an object, a piece of info called `funding_pubkey`, which I've been calling pubkey1.
There is a message that everyone can see.
You send it over the wire to node2, and now node2 has all this information.
`funding_pubkey` is the pubkey, in the 2 of 2 multisig script of the funding transaction output.
The spec writes out exactly how you should consider each of these things.
Then the other node sends back the accept channel message, and part of this is their pubkey.
They also send back a `funding_pubkey` which is also known as pubkey2.
At the end of these two message exchanges, both parties know what pubkey1 and pubkey2 are.
Node1 sent pubkey1 to node2, and node2 responded back with pubkey2.
At this point, everyone has everything they need to fill in all the blanks.
We can make a locking script for our Bitcoin, and we can send our Bitcoin to this output, and we have a channel.
We have all the info we need to open a channel.

Let's say we have an enormous amount of bitcoin.
Five bitcoin.
We send some money to Bitcoin address.
The way it works is node1 is going to send money to this address, locking up their money into this address.
Node1 makes a transaction to the Bitcoin address.
In order to move their 5 BTC, they need a sign off from node2.
Node2 needs to sign to move the 5 BTC.
What are some downsides to doing this?
When the channel opens, who has Bitcoin that they can spend in the channel?
Only node1.
node1 sent money to that address and node2 knows the address.
Node2 could also just send money to that address.
Everyone knows what the address is.
What if we just all start sending money to the address?
We'll have lots of UTXOs with money locked into it.
This is a problem though.
Once you send money to the transactions, you need the other node's signature to spend it, to get it out.
If you send money to this Bitcoin address and you don't have the ability to spend it and your peer disappears, you just lost five Bitcoin.
You send five bitcoin to an address, and someone else, some random node on the internet, gave you a pubkey that you locked up the money with, and you cannot get your money back without their signature.
Thit doesn't seem like a good idea.
So we need a little more in the "open_channel" protocol.
We need a little more information before we send money to this address.

Some downsides to this:
- Only one side can put money into a channel open.
- You send money to an address, but you want to make sure you can spend from that address before you send money there.

### Building a tx that sends money to the multisig address

Node1, after receiving accept channel, is going to build the transaction that sends money to that address, because now they can make that address.
They' are going to send over the wire the `txid` and the `vout`, called funding out point.
This tells node2 where to look for money on-chain that will be found in channel open.
One side builds the transaction, and then they send to node 2 the information about that.
We also send a signature.

We're sending the `txid`, and we're sending an output number (`vout`).
These two pieces of information uniquely identify where you will expect to see your Bitcoin on-chain.
Notice we haven't sent it yet.
This is pre-planning for node1.
We also send a signature, that lets node2 rescue their money if this transaction ends up on-chain.
This is like, "When I send the money to this address, you can use this signature from me, along with your own signature, to rescue the money".
This lets node2 to get their money back if something goes wrong with the funding output.
If I send all my money to it and then disappear, node2, in theory, could get their money out.
Node2 gets it (the `funding_created` message), and sends back another message (the `funding_signed` message) that's going to include their signature so that node1 can then get their money out.
Once node1 has a signature from node2, they're going to go ahead and send the (funding) transaction.
You're going to wait until you have the other party's permission to get your money out of that address before you send anything to that address.
So you have a get out of jail card just in case the peer goes away.

The next message that they (node2) send back is a `funding_signed` message and inside of it is a signature.
So that's it.
That's the conversation.
Transaction is sent and both sides wait for the channel to open, which means we're waiting for the transaction that has the script that locks all the money up.
But all the money is only node1's money.
So we are waiting for the output that has all of node1's money to get mined into a block and then get buried to certain depth, and at that point, channel's open!

When the channel opens, we both (nodes) send a message, called `channel_ready`.
When node1 sees it get mined to a certain depth (the transaction) it will send a `channel_ready`, and then node2 will send a `channel_ready`.

So, we have two people who want to have a conversation about opening a channel, they have to exchange some pubkeys, and then they have to exchange some signatures.
Once they get their signatures, one person who's built the transaction sends the transaction out to the blockchain, and as soon as it gets mined that channel is considered open and existing.

## Downsides

### All the Money is on One Side

Drawbacks are that the money is only on one side.
The problem or why that is sub-optimal is there's no liquidity.
You can receive payments, but you can't send payments one way.
Every channel that opens in Bitcoin and lightning can only send one way.
If you want to send money in the opposite direction you need to make a payment or convince someone else to open a channel towards you.
This costs money because every time you want to open a channel, we have to make an on-chain transaction, and that has a literal world cost.
[inaudible]

But what if you don't know the other node you're opening it with.
What if you want to open a channel because it's good for your node to be connected in a graph in that way, but you don't know that guy.
You're not supposed to know who runs the nodes, in theory.
It's supposed to be a semi-anonymous set of people with money in the channel.

### Channel's not balanced

Audience: "There is a couple more disadvantages to this, right?
First of all, the fact that the channel is not balanced.
A lot of lightning is based around the idea that there is a punishment risk, which is based around there being something to lose.
So, an unbalanced channel is a kind of a shitty thing."

### Everybody knows who opened the channel

Audience: "The second thing is, which is very relevant to what you're about to say, is if you pay into a lighnting channel, let's say one UTXO, somebody knows it's yours.
They know who owns the funds in the channel at that point.
The privacy is quite poor, at least when you start with a single-funded channel."

Common ownership risk, because only one person opened it, all the funds in that channel open belong to the same party, and its one 1 of the 2 in there.

### Hard for new nodes to get inbound liquidity.

Audience: "There's another one too, which is that it's hard for new nodes to get inbound liquidity."

What this means in the real world, practically, is that you can't receive payments.
Receiving payments over Lightning is hard.
If you wanted to open a shop and get people to buy cookies from you, it would be very difficult to accept payments over Lightning because you need other people to open channels to you in order to receive money.

## Designing a New Protocol

### Transaction with UTXOs From Two Parties

We are going to make a new protocol.
We want to make it easier to get inbound.
What if we led both sides construct the channel together, built the transaction together.

Let's make a protocol where everyone can put money into the channel at open.
We want to be able to build a transaction that has UTXOs from two parties.
Two parties can make one transaction with UTXOs from both people.
A transaction is a list of inputs and then a list of outputs.
Two people could talk and put input from node1 and input from node2, and these outputs are the channel funding, the 2 of 2 multisig.
Then we can have  the change output for node1, andthe change output for node2.
If inputs for node1 is 10 BTC, and for node2 is 5 BTC, and the funding output for the multisig is 8 BTC, derived from node1 (6 BTC) and node2 (2 BTC).
The change output for node1 is 4 BTC and for node2 is 3 BTC.
This is like a joint account you've created and it becomes hard to tell where the Bitcoin went because some of it went into a joint account and you don't know who has how much at the start.

There's a couple of cool things you can notice here.
One is both nodes will have money in the channel, it's not an even amount, bit it makes it possible that both can both send and receive immediately through this channel.
Amounts differ, but it makes it such that you can send and receive payments all at once.

It's only one transaction, and you get a little bit of savings in the fact that it's only one.
You get some savings by having one channel deployed.

So in order to make this happen, what are we going to have to change?

When designing a protocol, the first thing that you figure out is what you want to do, what information do we need to have a conversation about so that we can achieve our goal.
Our goal is to build a transaction together.
We want to be able to have a transaction, so both sides need to know all the information.
That's not strictly true, but we like doing things balanced for reasons and decentralized protocols.

We could send all the information to one node, right?
We could have just one node send all of their input information to the other node, have them construct a transaction and then just send the, which transaction I need back to the other node, right?
We don't want to do that, we want both sides to be able to build a transaction.

### Interactive transaction construction protocol

We need to send information about the transaction back and forth, over the wire.
We needed a new protocol for that.
One way to think of protocol is like a closed conversation, what am I allowed to say back and forth?
Like writing a script in a play for two actors that are very dry robots.
We came up with an interactive transaction construction protocol.
We are reusing this for splicing, because splicing does the same work of making a new transaction with two parties.
(It's) The same work, there is a different setup and a different ending, but the middle part of when you're building the transaction is the same.

Audience: "could it be used for non-Lightning stuff?"

Sure, actually the DLC people, they took the protocol that we wrote, changed it, because we wrote it in a way that it's quite flexible in terms of...
The way that we constructed the transaction makes it such that you can build a transaction with parties that aren't just the two that are having the conversation.
So, there is some plausible deniability about who the inputs you're sending to your peer belong to.
Whereas, if you do it in a batch transaction way, you can't lose that capability.
Whether or not this is something we should preserve in lightning is maybe a question, but you can do cool stuff with it.

It basically lets you start multiple channel opens at the same time and build one transaction that opens multiple - four, five, six - channels in the same transaction.
You get a decentralized multi-party transaction that anyone who runs the Lightning node can kick off any time they want.

Audience: "So you're trying to preserve the idea that not everyone needs to know about all the other channels [inaudible], so you might not know about other ones that have."

Yeah, it just looks like outputs for the other nodes.
Fun fact, you can do this on Core Lightning already, it's already implemented.
Everything I'm talking about today exists on Core Lightning.

## Dual Funding

Let's just go browse though what's kind of changed about it.
It's in a Pull Request ([interactive_tx: Add dual-funding flow, using the interactive tx protocol](https://github.com/lightning/bolts/pull/851)), it's a proposal.
Core Lightning is implemented it, that's the project I work on.
Eclair, a French team that does Lightning, has also implemented it.
We are in final stages of getting it ratified so it would be considered part of the spec.
Let's just go look at the file changes.

I made a whole video where I explain it too, so if you want to watch me [inaudible] another video where I explain how it works, that exists in the pull request.
We have changed channel establishment, we've now given it this nice little name "v1" and we've added a whole new thing of "v2".
We still have an `open_channel` message and `accept_channel` message.
Then we have this whole section of new stuff called the interactive transaction construction.

### RBF (replace by fee)

We have ability to do RBF now.
If you attempt to open a channel and then you want to renegotiate it, we give you a protocol to be able to attempt to RBF with the collaboration of both funders.
There's no guarantee that this will work.
But it's there, which is kind of cool.

### Channel Establisment v2

We can walk through how it works.
We have some [diagrams in the specs that also do this](https://github.com/lightning/bolts/blob/master/02-peer-protocol.md#channel-establishment-v2).

Before all this there's a process of picking a node that you want to open a channel with.
That's like a whole separate thing.
You have to decide who you want to open a channel with, and liquidity ads is supposed to help with some of this.
It helps answer the question, "who can I open a channel with and expect them to put money in?".
Whatever, but hand-wave over that.
So that's how you coordinate that someone's going to put money in the channel with you as liquidity.
That's a whole other proposal, also included in Core Lightning, which is fun.

(back to Channel Establisment v2)
First of all, it's going to be like, "OK, you, I'm going to open a channel with you".
I'm going to send you an `open_channel` message that's going to have a whole bunch of information in it about my pubkey and all that other stuff we already saw.
Then, the other side they'll say,"OK, yes, I accept your proposal to open a channel".

#### Transaction Collaboration

Then we get into a section that I call transaction collaboration, which you just send each other back and forth all the inputs and outputs that you expect on this transaction.
One by one, each of you takes a turn, if you don't have anything to add, you just say no.
You're kind of like dealing cards back and forth between each other, going around back and forth.
And then at the end, after both say pass two (times) in a row, you're like, okay, let's look at all the cards that people put on the table.
As soon as you get two people decline or pass, it ends.
We're both gonna have the same set of inputs and outputs, and we're gonna take all this information that we've sent each other, and we're going to build a transaction with basically the set of cards that everyone's put in the middle.
The cards are sort of your inputs and outputs.
We're both gonna have the same set of inputs and outputs, and take this information that we've sent each other, and we're going to build a transaction with what each party wants to add.

[Audience]: "Each input gets registered separately?"

Yes, non-batched, so that you can get inputs from a third party.
You can be talking to someone else about this, so as you get inputs from a third party you can send them to another one.
You get kind of a ladder effect but then it looks like it's from (a single party).

[Audience]: "And there's no ownership proof for those inputs?"

No, it's very basic.
So it's a little griefable.
This is a very basic, let's-get-the-protocol-working process.

[Audience]: "But if you want third party inputs, then ownership proofs are a lot more difficult, but still doable."

It's possible that someone could send you complete junk and you build a transaction that they can't send you valid signatures for, in that case, well you just lost some time.
You haven't really lost any money.
As long as you don't actually reserve any of those inputs until they get spent, it just doesn't...

[Audience]: "The attacker might at that point learn your inputs."

Right, so this is an interesting aspect of it being a lightning open, and that's that all lightning opens become public information at some point.
They're gonna know your inputs, it's a little bit of information.

[Audience]: "PayJoin has a similar issue, right?
That the sender can query the UTXOs of the merchant."

It's a common problem with interactive transaction instruction things.

[Audience]: "PayJoin solves it by signing a single user transaction with that input already that the merchant could broadcast.

There are proposals on how to fix it, but currently there's just this agreement.
There's a possibility that you link UTXOs for each other, that's true.

But there's a little bit of a thought in Lightning that your UTXOs aren't as important in Lightning as they are in, I mean they are important in terms of how much money you have the ability to spend, but they don't represent payments.
They represent the ability to make batches of payments.
There's less of a relationship between your UTXOs and the amount of payments that represents.

[Audience]: "You're talking about UTXOs that actually end up in the channel."

That's true.
Yes, there are some definite downsides to this.

[Audience]: "Even the griefing isn't that bad because there could be a third party input that you included."

So there's plausible deniability that it's not your UTXO, that's why it's not batched.
We preserve the plausible deniability that they're not your UTXOs.
They could be someone else's.

We also have the ability to remove inputs and outputs, so you could add stuff and then remove it later.
If you had a third party that was in the [inaudible] and then dropped out, you could remove them.

OK, so that's the back and forth stuff.
This is basically the big change between v1 and v2.

After you construct the transaction, then you exchange signatures that let you spend from that transaction.
It's the same problem as before, you don't want to publish the transaction before your signatures, so you get the signatures to do it.
The last thing you do is you exchange signatures to broadcast the funding transaction.
There are more steps than original one, more messages and communication needs to happen.

If you want to know more about the proposal, the whole thing is up on the internet.
It's [PR#851](https://github.com/lightning/bolts/pull/851), if you'd like to chime in.

## Multi-fund channel

If you want to learn more about how to make this work on Core Lightning, I feel like the fun one is multi-fund channel with liquidity APIs, but I need to make a tutorial on how that works because that's fun.
It's a command for establishing multiple Lightning channels.
If you do the `request_amt`, there's a few little parameters in here you can add to each of them to buy liquidity ads.
The liquidity ads is how you do the coordination to convince your peer to put money in the channel.
The way you convince them is you bribe them, you give them money, you're like, "hey, I would like you to put money in the channel with me, and I'll pay you for it".

The liquidity ad is a coordination mechanism for doing that, so you get multi-fund channel with a bunch of channels that you buy liquidity from at the same time.
That is how you would get a decentralized, self-coordinated coinjoin.
