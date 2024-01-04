---
title: "Tradeoffs in Permissionless Systems"
transcript_by: BlueeeMoon via review.btctranscripts.com
media: https://www.youtube.com/watch?v=s_I_Nj5GMgk
tags: ["bitcoin-core","mempool","incentives"]
speakers: ["Gloria Zhao"]
categories: ["conference"]
date: 2022-07-05
---
## Introduction

Hello.
I wanted to make a talk about what I work on because I consider it the, well, the area of code that I work in, because I considered it to be one of the most fascinating and definitely the most underrated part of Bitcoin that no one ever talks about.
And the reason is I kind of see it as where one of the most important ideological goals of Bitcoin translates into technical challenges, which also happens to be very, very interesting.
So I'm going to talk about the ideological component, permissionless, to boil it down, and then the technological component, which is mempool and mempool policy.
And I expect this to be new for most people, because, yeah.

## What is Permissionless?

Okay, so the ideology that we boil down into one statement is we want Bitcoin to enable a world where anyone can pay anyone, regardless of what country they live in, the political situation there, what their personal political values are, and what they say on the internet or what they work on.
Right, we want anyone to be able to pay anyone.
And this is usually called permissionless or censorship resistance or what have you.
Anyone should be able to do this.
And technologically, the way I break it down is it translates into two kind of very difficult goals and somewhat contradictory.

## User Requirements & Goals

One is the user requirements for your software must be reasonable.
So if we released Bitcoin software that needed 64 gigs of RAM in order to function or required $2,000 a month of operating costs, or only built for Linux, like you couldn't run it on Windows, or it requires you to register with a central authority that would take down your name and whatnot.
These are all kind of unacceptable things when we think about what permissionless means.
And the other part is, okay, anyone can join, which means you should probably expect bad guys to join.

## Security Model

And what I'm really trying to say here is our security model cannot be like, oh yeah, there's this DOS vector, but it's okay because we can always just ask the government who is using this IP address and then ban them for the network or something.
Like something stupid like that, as your security assumption, is just not gonna work.
And I'll get more into this, but unfortunately these two goals are a little bit hard to manage at the same time.
Okay, so first I'll talk a little bit about how Bitcoin achieves this anyone should be able to pay anyone philosophy.

## Peer-to-Peer Network

So we have a peer-to-peer network where anyone should be able to run some kind of node software, join as a peer, and then broadcast their transaction, and eventually it propagates to a miner.
That includes this transaction in a block.
And then there's all the other magic that is frequently talked about on, about Bitcoin and popular media.
But I like to focus on this transaction relay portion because I think it's very underrated, essentially.
Okay, so what does this peer-to-peer network look like?
Well, ideally, it's a mix of a lot of different types of software running on different hardware.
So you might have ASICs which represent miners and you might have, these are supposed to be servers, like cloud servers if someone is running a node on AWS or they're on a smartphone and connecting to like Coinbase, which has their own servers running, hopefully more beefed up nodes.
And so everyone's kind of model is a little bit different and the network is supposed to be heterogeneous.
But ideally, anyone broadcasts their transaction, everyone looks the same, this provides a little bit of privacy since you can kind of obfuscate the origin of a transaction, and yay, you have something that is supposed to look like a permissionless way for anyone to pay anyone.

## Mempool

And then I wanted to make sure I defined mempool, just in case for those of you that are unaware, every node on the network has a cache of these unconfirmed, as in pre-block transactions.
And for miners, obviously, they need this mempool in order to remember what transactions to put in the block, but for nodes as well, if they didn't keep a mempool, it would be just disastrous for bandwidth and for all kinds of things.
And it also allows the bandwidth requirements to be more reasonable since when a block comes and you already have 99% of the transactions, you don't need to redownload them all over again.
Okay, The dangerous part here is remember the thing where I said the user requirements to run a node need to be reasonable, which means these mempools cannot take up infinite space or have infinite computational possibilities.
It needs to be reasonable.
So the problem is, the peer-to-peer network is like the Wild West.
Anyone could be your peer.
And so it could be someone trying to launch a distributed denial of service attack.
So let's say they give you a transaction.
This is very different from a block where it already has a proof of work attached to it and you're like, okay, someone spent a lot of time and energy creating this transaction.
You can make transactions, like millions of them, in a second.
You don't have that asymmetry of the cost to create versus the cost to verify.
So this transaction might cause you to spin for like half a second, just like looking at the data.
That's one possibility.
They could maybe be trying to get an out of memory error.
Let's say they looked at the Bitcoin core source code and they're like, oh, if I send a transaction with these bytes in it, it'll hit this logic that asserts true and it'll be false and then everyone will crash.
That would be a disastrous bug.
If they're just trying to launch some kind of attack where everyone in the network stalls for like half a second.
That could be a significant boost in them trying to mine the next block.
Like that's a significant head start.
Hopefully this gives you a sense of like, maybe the dangers of allowing anyone to connect to your node as a peer.
And the last one is, what if you have inconsistent logic, where if something is sent to various peers, half of the network will say yes and half of the network will say no, and then they'll disconnect peers that don't get the same result as them, and then you have a network split.
That would be also a very bad disaster that you could possibly run into if you didn't do this right.
Okay, so how do we defend against these denial of service attacks?
Well, we have to set some limits on what transactions we expose our validation engine to and what we allocate memory to store.
So one thing is like, a standard transaction is not allowed to be 100,000 virtual bytes.

## Unconfirmed Transactions

I've never come across a use case where you needed anything remotely close to that, but this is an example of a reasonable policy that we put on transactions that we receive on the peer-to-peer network.
Are we familiar with the UTXO-based model?
You have inputs and outputs, which means you could have a transaction spending the output of an unconfirmed transaction.
Which means in your mempool, not all the transactions are gonna be independent.
Some might spend from another.
Okay, cool, I see a lot of nodding, that's a good sign.
So, what happens if you had one transaction and then the attacker made 500 descendants spending from that transaction and then they made 500 from each of them, and then all of a sudden you have hundreds of megabytes worth of transactions that all hinge on this one confirmed output, for example.
Then that allows the attacker to flush your mempool really easily because let's say a conflicting transaction is mined, you're like, oh, okay, let's throw away all these transactions that can no longer be valid on the current chain state.
So that's another example.
We limit the descendant size.
So like we limit the tree of unconfirmed transactions that will admit into our mempool.
Another thing is like signature verification is quite expensive computationally.
So we save that for the very end.
That's like a basic fail fast, do the more, the cheaper checks first and the more expensive checks last.
And also we'll reject transactions with too many signature operations.
And these are all rules that are not consensus rules.
Consensus valid transactions can be up to a few million bytes, or a few million virtual bytes.
So these are not consensus rules, they're just node practical rules that they're going to impose on transactions they receive on P2P.

## Policy

Okay, so this leads me to the definition of mempool policy.
So if you've never heard of policy before, this is how I define it.
It's just a node's set of local validation rules in addition to consensus that they enforce on unconfirmed transactions.
So this has nothing to do with block validation.
If you see a non-standard transaction in a block, obviously it's still valid.
But that transaction has to be part of something that they put a proof of work on.
These are like random stuff that you received on P2P.
Okay, so these rules are user configurable, they can be different across the network, and that's something that we have to deal with.
But what I work on is Bitcoin Core, which is one of the node implementations of Bitcoin.
And so when we're creating the default mempool policy, we want to adhere to those original goals of it needs to be accessible.
It cannot be exorbitantly expensive for you to run a full node and participate in P2P transaction relay.
And it also needs to be safe for this node operator to be exposing their validation engine to random peers.
So that's the definition of mempool policy.
So let's talk about how do we create a mempool policy?

## Perfect Mempool

Some people think of it as this linear line, where on the one side we have the perfect mempool where let's say you had infinite computational resources and every time you received a transaction on the wire you could freeze time and then allocate whatever resources and then you also had infinite amount of storage to store all of these transactions.
Then maybe you would just always validate every single transaction that you get on the network and accept all of the ones that meet consensus.
Because why not?

## Perfect Defensive

And then on the other hand, you have the kind of perfectly defensive where you say, okay, I'm only going to validate transactions that are from people that I trust.
So they have to ask me, they have to send me an email, and then I whitelist them, and then their peer can connect to my node, for example.
This completely goes against our original vision of anyone should be able to pay anyone, and it's definitely not something reasonable that we can put in default Bitcoin Core.
So some people think about it on this spectrum, and then I'm sorry for spending so much time talking about it because it's a completely wrong mental model.
And here's an example of why it doesn't make any sense.

## Infinite Computational Resources

So even if you had infinite computational resources, Would you validate every consensus valid transaction and accept it to your mempool?
How many of you guys think that's a good idea?
Nobody raised their hand.
You guys are all so smart.
Okay, so here's a concrete example of why that would be a terrible idea.

## Consensus Invalid Transactions

So right now, let's pretend we have the space of all of the transactions we might receive on the P2P network, some of which may be consensus invalid.
And as a subset of that, we have all the transactions that are consensus valid.
And then an even smaller subset of that is the transactions that will be consensus valid after some kind of future soft fork.
So hopefully you can see where this is going.
Let's say we deployed a soft fork and not everybody upgraded their nodes.
That's a possibility that we have to be okay with as we're creating permissionless software.
We cannot force everyone to upgrade their nodes.
So, this happened with Taproot.
Recent current event, I'm quoting a link from 0xb10c with permission, thank you very much.
So as we saw with Taproot, some miner, like the miner signaled that they were ready for Taproot, and then Taproot activated, and we saw that some miners were not including taproot transactions in their blocks, presumably because they weren't validating taproot yet.
They hadn't upgraded their nodes.
So, the question is, what would have happened if version one witness transactions were allowed in their mempools at the time.
So someone could have sent them an invalid Taproot spend and then they would have mined it into a block and then suddenly they're on their own fork and all the nodes that upgraded would be on one and then all the nodes that didn't upgrade would be on this other one where they had a very free mempool policy.
And obviously this would resolve as long as most of the hash rate was on the fork that did upgrade and whatnot but this is pretty bad.
So the way that we address this is, we just say everything that might change in the future, we're gonna ban.
Which is why you saw, what was it, F2Pool was the one that didn't, sorry for calling them out, was the one that didn't mine Taproot transactions, what they were probably running was some previous version of Bitcoin Core that did not, just banned all transactions using Witness version one.
And that mitigates this issue of like, what happens if we upgrade and some people don't upgrade.

## Upgradeability

So this goes for witness versions greater than one, now all of the upgradable NOPs, the upgradable N versions, these are all non-standard so that we can safely upgrade in the future without requiring everyone to upgrade at the same time.
On the other hand, there's a question of like, okay, can we go wrong if we're just extremely, extremely, extremely conservative?
Raise your hand if you think this is fine.
Oh, nobody raised their hands.
Oh no, one person.
Okay, I'm gonna prove you wrong.
Okay, so here's where we go into a territory where you can see exploitations and censorship attacks because of conservative mempool policies.

## Descendent Limit

So, you know how I mentioned we have a descendant limit where you cannot create just like an infinite chain of descendants and expect mempools to accept them.
So we're only going to accept the top 101 kilovirtualbytes.
Well, that was a problem in Lightning when they decided, okay, we're gonna try to deploy anchor outputs.
And this is going to allow people to adjust their fees at broadcast time.
So your commitment transaction, for example, you could attach a high fee child to fee bump the priority of the commitment transaction.
But obviously you're gonna have an anchor output for each participant in the Lightning channel, which allows both of them to fee bump the commitment transaction.
So then the question was, okay, what happens if one of them just is an asshole and attaches 100 kilovirtual bytes, thereby monopolizing this descendant limit.
Now, all of the nodes that are running this very reasonable mempool policy where they limit the number of descendants you can attach to a transaction are going to reject this fee bumping attempt.

## Pinning Attacks

And this leads us to, hopefully that makes sense, this leads us to a class of censorship attacks, which I like to call pinning attacks, where they take advantage of the conservative nature of mempool policy in order to prevent a transaction from either making it into the mempool or getting mined.
So when we talk about censorship, a lot of people are often like, oh, if the node is dropping transactions, or they're trying to stop transactions from being sent.
But this is also a pretty valid security concern when it comes to censorship.

## Quiz Time 

### Two Transactions Quiz

So, now I'm gonna talk about more policy.
Quiz.
This should be pretty obvious.
So there's two transactions.
They're both 100 virtual bytes.
One pays 200 Satoshis in fees, and the other one pays 100 satoshis in fees.
Raise your hand if you think the one on the left is better.
Yes.
And the one on the right?
Okay, one person is wrong, but cool.

### Child Quiz Part Two

Next one, slightly harder.
We have the same transactions, but now the one on the right has a child, which depends upon it in order to be mined and pays 1,000 satoshis and is also only 100 virtual bytes.
Raise your hand if you think the one on the left is better.
Raise your hand if you think the one on the right is better.
Cool, okay.
New question.
Okay, actually, sorry, going back.
So, it's quiz time, I'm sorry.
I'm sure you didn't want to be quizzed.
But, so essentially, when you're looking at mempool, looking at transactions, and you only have limited space in your mempool, you're gonna have to make a judgment call at some point, where you're like, okay, my mempool's full.
Obviously I want to maximize fees.
So these are not conflicting transactions and usually you could have both in your mempool as long as it's not like super congested.
But what if the transaction's conflicted?
As in they spent the same prev outs, the same UTXOs.
So now you can't have both, because one is a double spend of the other.

### Quiz Part Three

So, quiz again.
One is 500 Satoshis, and the other one is 5,000.
Hopefully it's obvious.
Okay, so these two illustrate, the quiz, they illustrate mempool policies that help users communicate the urgency of their transactions and allow them to bump the priority of when they expect this transaction to be confirmed by adding new fees.
So one is you can replace, that was the last example I put, where if you have two conflicting transactions, you're gonna wanna take the one that has more fees, even though you received one before the other.
And the other one is you can add a high-fee child to a transaction in order to fee bump it.
And these are called replace by fee and child pays for parent, respectively, if you've heard of those things.
So it's the mempool policy that we implement that then translates to this feature that users are able to use called RBF and CPFP.

## Conclusion

So in conclusion, today we've introduced what mempool policy is and hopefully illustrated that it's a very interesting space full of tradeoffs and dangerous lines to tiptoe.
And we gave a few different examples of why we want mempool policy.
The biggest one is denial of service protection.
But also, it includes things like incentive compatibility, where we want to have an incentive compatible policy in order to help users.
It allows us to upgrade the network and Softforks safely, and we also want to consider censorship attacks that result from the policy itself.
So thank you for listening to my talk and hopefully I've convinced you that mempool policy is a very interesting thing to work on.
Thank you.

## Q&A

Audience:
So is there the possibility to optimize the mempool?
Let's say if you're running a mining pool or doing DeFi, is there the ability for one person to exploit the mempool in a better way than maybe competitors?
There are a lot of different trade-offs.
So that implies that doing one thing might end up in a different outcome than the other.
And so how you weight those, or depending on if the mempool is really backed up, do you take lower values?
So is there a way to optimize this or are there people doing that?

Gloria Zhao:
Do you mean optimize the mempool policy itself or optimize?

Audience:
So if you're a miner, for example.

Gloria Zhao:
Yeah, so miners, so policy is configurable.
Again, everyone can run their own version of a Bitcoin node as long as it adheres to consensus and P2P.
And so I think miners usually will have a much bigger mempool and for example, they'll have, because they have access to more computational resources and more memory, they can configure it to be like five gigabytes instead of 300 megabytes.
Or they can allow descendant chains up to 100 instead of 25.
So yeah, there is, like if you care more about incentives and maximizing fees and less about economical use of resources, then you can optimize for that.

Audience:
Okay, first, thank you, this is a fantastic talk.
Second is, when we're thinking about, in general, the health of blockchains, is there meaningful research going into the diversification of mempool policies?
Theoretically, however you produce it, there is going to be some best way to manipulate and to attack that mempool.
So I'm assuming there's some effort going into the diversification of mempool policies to make sure that we don't all have the same policies.

Gloria Zhao:
Yeah, that's a really good point.
As you said, as long as there's some consensus valid transaction that your mempool policy doesn't accept, there's room for pinning attacks, leveraging that space.
And your question was whether or not there's research into different types of mempool policy.
I think about it sometimes, but I don't know if there's research out there.

Audience:
Do you know if there are any efforts between people who are running mempools to make sure that they don't all have the same policies?

Gloria Zhao:
Ooh, I've done a Twitter poll that suggests that everyone's just running default Bitcoin core.
Which is why we go for safest, most reasonable resource requirements.


Audience:
Are there randomized mempool rules?
Or are these random?

Gloria Zhao:
Like, any policies that have some form of randomness in them?
There's like the order in which you receive transactions could affect what ends up in your mempool.
Yes, there is.
There are a few things like how we manage orphan transactions where we'll evict randomly.
So for example, this is probably not what you're looking for.
This is just me being nerd sniped.
So when you receive a transaction, like when you receive the child before the parent, which can happen because it's a peer-to-peer network and you receive things out of order, you'll store this in an orphan pool because you don't have access to this input, you're not able to look that up in your current chain state.
So you put this in an orphan pool, and you'll wait for receiving this transaction, and then you'll accept this, and then you'll validate this and put it in your mempool.
But the orphan pool is like an extremely dangerous other, like essentially resources that you've allocated for completely unvalidated transactions, like you could make an infinite number of these because you don't even need a valid prev out.
And so the way in that we evict transactions from our orphan pool, if it fills up, because obviously the resources are bounded, needs to be random so that nobody can just be like, oh, okay, so I'll just send you 100 orphans and then you've forgotten about this transaction.
So there's a bit of randomness there.
Sorry for me just rambling because I got excited.
Thank you.
