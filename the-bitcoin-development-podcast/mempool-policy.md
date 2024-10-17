---
title: "Mempool Policy"
transcript_by: kouloumos via tstbtc v1.0.0 --needs-review
media: https://podcasters.spotify.com/pod/show/bitcoinbrink/episodes/Mempool-Policy-e182ul0
tags: ['rbf', 'transaction-pinning']
speakers: ['John Newbery', 'Gloria Zhao']
summary: "Brink co-founder, John Newbery, and Brink fellow, Gloria Zhao, discuss Bitcoin Core's mempool policy."
date: 2021-11-10
additional_resources:
  - title: BIP125 Replace by Fee (RBF)
    url: https://bitcoinops.org/en/topics/replace-by-fee/
  - title: Transaction pinning
    url: https://bitcoinops.org/en/topics/transaction-pinning/
  - title: Discourage upgradable
    url: https://github.com/bitcoin/bitcoin/pull/5000
  - title: https://brink.dev/
    url: https://brink.dev/
---
Speaker 0: 00:00:00

Hi Gloria.

Speaker 1: 00:00:01

Hi John.

Speaker 0: 00:00:02

We're here to talk about Bitcoin.

Speaker 1: 00:00:04

Yes, we are.
What are we going to talk about?

Speaker 0: 00:00:06

Well, I think you wanted to talk about policy.

Speaker 1: 00:00:09

Yes, that's what I wanted to talk about.
What kind of policy?
Mempool policy, not legislative policy or miniscript policy.
Mempool policy.

Speaker 0: 00:00:20

Okay, well, let's start with the basics.
What is a mempool?

## What is a mempool and why have one?

Speaker 1: 00:00:23

Well, the mempool is a data structure that's designed to store the best candidates for mining.
That being the transactions or groups of transactions with the highest fee rate that a miner might want to include in the next block so that they get the best fees.

Speaker 0: 00:00:40

Okay, so these are transactions that aren't yet confirmed, they're not included in the blockchain and miners might at some point include them in a block?

Speaker 1: 00:00:51

Yeah, I mean at some point everyone was mining, right?

Speaker 0: 00:00:55

Yeah, I guess so in 0.1, kind of the original release of Bitcoin, well first it was just Satoshi mining and then I guess Halfenny started mining.

Speaker 1: 00:01:04

Yeah, so it was like default mining would be on as opposed to now where it's off.

Speaker 0: 00:01:09

Right.
So the mempool was for those miners to, so they could select transactions to include in a block.
But today we have lots of full nodes that aren't mining, but they still have the mempool.

Speaker 1: 00:01:19

Yeah, I mean, a mempool, or like, even if you're not mining, you would care what miners are going to put in their next transaction or in their next block, sorry.

Speaker 0: 00:01:29

Why?

Speaker 1: 00:01:30

Well, first and foremost, like even if you're not broadcasting your own transactions, even if you don't have a wallet attached, looking at the unconfirmed transactions before they're included in a block, as long as you have like kind of an accurate mempool, you are going to be caching those script checks, you're caching the signature checks, and that really helps with your block validation speed later when the blocks do get mined.

Speaker 0: 00:01:54

That's actually a really interesting point that the scripts inside the transactions are context-free, So you can check the validity of scripts even if the transaction is not in a block.

Speaker 1: 00:02:05

Yeah, and we do just the scripts because it's particularly expensive to be checking those scripts and signatures.

Speaker 0: 00:02:12

Okay, so you receive a transaction, you put it in your mempool, and as part of doing that, you're checking the scripts.
And then if you receive a block in the future that contains that transaction you don't need to recheck that script.
Okay.

Speaker 1: 00:02:25

Yep.
All you do is check your signature cache with the WTX ID and the verification flags.
You're like, okay.

Speaker 0: 00:02:32

Okay.
So that's one good reason to have a mempool.
What else?

Speaker 1: 00:02:35

If you are going to be broadcasting your transactions, having a mempool really helps with fee estimation.
Like you could go check a centralized API, but really what you should be doing is querying your own mempool, which hopefully is an accurate pool of transactions that a miner would be looking at as well when they're selecting what's going to be in their next block.
And then you're like, oh, okay, like what fee rate should I put on my transaction so that I can be in the top however many like virtual bytes to be in like the next one block or the next 10 blocks or the next however many blocks, however urgent your transaction is.
And usually you'll want a mempool so you can validate your transaction before you broadcast it.
And just in general, Bitcoin core nodes, at least we broadcast what's in our mempool, like transaction propagation is based on like what you have in your mempool.
So like if your peer queries you for it, you look into your mempool when you're announcing to your peers, look into what's in your mempool, etc.
Etc.

Speaker 0: 00:03:38

Okay, so you mentioned script caching.
Another interesting aspect of speeding up block validation relay is compact blocks, right?

Speaker 1: 00:03:46

Right, Yeah.
So if you already have the transactions or like the mempool will contain the transactions themselves obviously.
And if you're relaying blocks through compact blocks, hopefully 99% or like all the transactions apart from the Coinbase you already have and then you don't have to download that from your peers.
You can just go, whoop.

Speaker 0: 00:04:06

So saving bandwidth as well as computation.

Speaker 1: 00:04:08

Yeah, network bandwidth.

Speaker 0: 00:04:10

Great.
And then finally, another reason you'd have a mempool is kind of central to decentralization.
Oh dear.
So can you explain that?
How does a mempool or how does transaction relay help with decentralization?

Speaker 1: 00:04:24

Right.
So I think what we're trying to avoid here is you needing to do anything beyond like run a regular node in order to broadcast transactions.
So you wouldn't need a mempool, like no one would need a mempool if the way to get your transaction mined would be to connect to a miner.
And then they're like, oh, okay, yeah.
Let me see if I have space for you.
Ideally, what happens is you just plug in your little Raspberry Pi node, it bootstraps itself, it connects to peers and those peers somehow are connected to miners, you hit broadcast transaction, and then like magically it ends up in a block, like a few minutes from now, or a few hours or whatever it is.
That's helpful for censorship, that's helpful for decentralization in general.
And it kind of relies on the network kind of being a little bit of I scratch your back, you scratch mine.
A little bit of altruism is required.
But like I said, there's so many pros to having your own mempool that hopefully everyone participating in transaction propagation is not too expensive.

Speaker 0: 00:05:39

Right, so it's altruistic in a sense that we're relying on nodes and peers of peers existing and relaying the transaction.
So clearly for that to work, we can't allow the cost of having a mempool and relaying transactions to be too high.

Speaker 1: 00:05:56

Yeah.
Yeah.
I think that's kind of the key part of mempool validation and why it's like, very fascinating to me.
So you have this like very interesting trade-off where ideally you have exactly the transactions that are consensus valid or are going to make it into the next few blocks and are the highest fee rate, whatever.
But you are exposing this on the P2P network.
And that means these computational resources and memory that you've allocated for mempool validation can be abused by random computers on the network.
And so there's this very interesting trade-off of like, how do we make the mempool as useful as possible and as accurate as possible without exposing ourselves to DOS attacks?
And when we're creating rules and setting heuristics for like protecting ourselves, let's not create pinning vectors or censorship vectors.

Speaker 0: 00:06:55

Okay, we'll get into those a bit later.

## Denial of service protection

Speaker 0: 00:06:57

So Bitcoin has this peer-to-peer network.
And if we're talking about block propagation, we have this inbuilt kind of rate limiter or protection from DOS, which is proof of work, right?

Speaker 1: 00:07:10

Right.
I think you know block download a bit better than I do.
Like, what do you do when someone sends you block headers?

Speaker 0: 00:07:16

So one of the first things you do once you've deserialized it and made sure that it's not malformed or anything like that, is you check the work on it.
So the block header contains various other fields and you check that once you've hashed everything together, the digest is below the target.
And for that to happen, the person who created that header needed to have done work.
That's kind of the critical insight that makes Bitcoin possible.
So when someone's feeding you headers or blocks, it's very cheap for you to verify that they've done that work.

Speaker 1: 00:07:50

Yeah, but very expensive if they want to send you garbage, but they have to provide a solution.

Speaker 0: 00:07:56

Right, so yeah, the key thing there is the asymmetry of expensive to create and cheap to validate.
Whereas we don't have that with transactions.

Speaker 1: 00:08:07

Right, yeah.
It's very cheap to create a transaction, especially if it's going to be invalid.
Yeah, computationally, like, yeah.

Speaker 0: 00:08:15

Yeah, So when we receive that transaction, so an unconfirmed transaction that a peer has told us about, we need some way or some ways to make sure that peer isn't just feeding us data that's going to be expensive for us computationally or in terms of memory or in terms of bandwidth.
So how do we do that?

Speaker 1: 00:08:33

We use policy.
Great, okay.

## What is mempool policy?

Speaker 0: 00:08:37

We have policy, and so what is policy?

Speaker 1: 00:08:40

Policy, I would define as a set of validation rules that you apply in addition to consensus on unconfirmed transactions.
So key there is unconfirmed.
This is not relevant at all for transactions and blocks.
And when I say addition to there's kind of a blurry line because some policies might include consensus kind of naturally baked into them, but a set of rules in addition, as in it's stricter than consensus.
Because ideally we would only have consensus rules because there's no reason, like let's say this was just a private permission network where it's just your friends and family sending you transactions and you trust them, there would be no reason to apply anything other than consensus.
Or if you had like an unlimited mempool and unlimited computational resources to be like validating all these transactions.
Sure, there's no reason to do more than consensus, but we are resource constrained.
So we have policy, which is even stricter than consensus.

Speaker 0: 00:09:45

Right.
So there's that difference between the ideal mempool, which contains just the transactions that maximize the fee for the miner in the next block, and then there's reality, which is we live in this world where our resources are constrained, be that memory or computational bandwidth, and we need to have some kind of heuristics, I guess, to make sure that we don't have unbounded usage of those resources.

## 3 types of mempool policy and examples of each

Speaker 1: 00:10:14

I think that we can roughly categorize memorable policy into three buckets for reasons where we're applying them.
And of course, like one policy can fall into multiple buckets.
The first being, we are using some kind of heuristic to boost the usefulness of our mempool.
So anything that's fee rate based where we're favoring higher fee rates over lower fee rates, that would fall under this category.
And then the second one is one that we've talked about a lot, which is protecting ourselves from resource exhaustion or DOS.
That's kind of the bulk of many policies, I think.
And then the third one is some set of rules that the node operator or kind of a group within the network or whatever has agreed as a good rule to follow or in preparation for a consensus rule in the future.
So we enforce it as policy so that we don't have it in our mempool and like mine it into a block.

Speaker 0: 00:11:18

Okay, so can you give me some examples of policy rules?

Speaker 1: 00:11:22

I have three favorites that I think we should talk about today.
Actually, three and a half.
So one big part of Mempool policy or Mempool validation that I find really, really important is the kind of fail fast idea.
So the order in which we do these checks really, really matters.
For example, we'll do context free size checks first, too small or too big before we check things like what's already in our mempool or what inputs are available from the UTXO set.
And we do all this before the most expensive thing, which is script and signature checking.
So relevant to this, I think three policies that kind of nicely fit into the three buckets we just mentioned.
The first one is literally the size of the transaction.
So it can't be too small or too big.
And then another one of my favorites is BIP 125 replaced by fee.
And another one that people probably haven't heard a lot about is the script verify flags, discourage upgradable flicks.

## Mempool policy: transaction size too small or too large

Speaker 0: 00:12:30

Let's dig into some of those.
So the first one you mentioned was too small.
So we will, from our mempool, or before we get into our mempool, in our accept to memory pool checks, reject any transaction that is 82 virtual bytes or smaller.
Yeah.
Okay.
Can you explain why that is?

Speaker 1: 00:12:50

I think the reason is twofold.
One of them is that I can't tell you how many bytes off the top of my head the smallest possible consensus valid transaction would be.
But I think if it's less than 82 bytes, that has to mean that there's like no outputs or something.
And so in our policy checks, we don't really fathom that being something useful to a user.
So it's like kind of a rule that we just agreed, like, okay, if it's less than 82 bytes, it's probably a useless transaction.

Speaker 0: 00:13:22

Right.
It's not economically useful.
You can't pay anyone with transactions.

Speaker 1: 00:13:27

Right.
Yeah.
A consensus valid payment has to be at least 82 bytes.

Speaker 0: 00:13:31

Because you need a signature from spending the input and you need a pubkey essentially or something that commits to the pubkey in the output and that's already getting you over that limit.
But it's also interesting because that might eventually be a consensus rule.

Speaker 1: 00:13:47

Really?

Speaker 0: 00:13:48

Yeah, so the quote, great consensus cleanup is various consensus rule changes that might happen in the future.
And one of them would be disallowing, I believe, transactions that are smaller than 82 bytes.
And the reason for that is because it protects against some forms of Merkle tree malleability.

Speaker 1: 00:14:08

Right.
If it's 64 bytes.

Speaker 0: 00:14:10

Right.
We don't want a transaction that's 64 bytes because when we put those transactions into a Merkle tree, the intermediate nodes in that Merkle tree, the digests are 64 bytes.
So we don't know whether that would be a leaf or an intermediate node.
So this policy rule is partially in anticipation of that, potentially.
Okay, so the next one you talked about was too large, so 100 kilobytes.

Speaker 1: 00:14:39

100 kilobytes.
I think this would fall into the category of like, we want to keep our memphle useful.
And so you can imagine a situation, an imaginary situation that is not a vector that can be taken advantage of right now is like, let's say you're a miner, and you haven't broadcast the transaction yet, and you're going to include it in your next block.
So what you do right before you publish this new block that you've mined with this transaction is you publish a big, gigantic, conflicting transaction, and then let's say you add like really big descendants to it as well and that takes up like 300 megabytes which would be the size of most people's mempools and you publish that and then everyone replaces all the transactions in their mempool with this like super, by the way, you add like a super high fee to this.
So everyone's like, oh yeah, this is definitely gonna get mine.
And so you fill everyone's mempools with this, and then you publish your block, and then that transaction gets evicted, or it gets conflicted out because we would prioritize a transaction in a block over an unconfirmed transaction.
And then now you've just emptied out everyone's mempools and it's completely useless.
And I guess you could do this kind of, but you're limited to like 25 transactions and they can't be more than 100 kilovirtual bytes.
So you take a very small.

Speaker 0: 00:16:08

You're limited to 25 transactions, why is that?

Speaker 1: 00:16:11

Oh, I'm kind of talking about two policies here.
So one is the transactions cannot individually be more than 100 kilovirtualbytes, and then it, including all of its descendants, can't be more than 101 kilovirtualbytes.
So you wouldn't be able to take advantage of this imaginary attack vector that I just talked about and like clear out everyone's mempool.
You could only do like a tiny portion.

Speaker 0: 00:16:37

And also a transaction can't have more than 24 descendants in the mempool or 24 ancestors.
We can't have chains or families of transactions that are larger than...

Speaker 1: 00:16:47

Well you can have families larger but yeah it wouldn't be like as cut and dry as this.

Speaker 0: 00:16:53

Right.
And those rules exist to, as you say, protect space in our mempool, and specifically space in our mempool when transactions change.
So when we receive a block and transactions get conflicted out of our mempool, or when transactions expire or get replaced, it's quite important that we kind of bound the churn that that can generate in our mempool, because if it's unbounded, like you say, an attacker could essentially empty out our men pool by Filling it up and then conflicting or filling it up and then replacing Okay, cool.

## Mempool policy: BIP125 Replace by Fee (RBF)

Speaker 0: 00:17:26

And your second example was bit one two five replaced by fee.

Speaker 1: 00:17:30

So replaced by fee is essentially you can replace a transaction in an unconfirmed transaction in a mempool by spending the same inputs and then adding doing it such that it has a higher fee rate.
And this is useful because it allows users to bump their transactions.
And it's very much minor incentive aligned because they would want the one with more fees.
However, there's a lot of sub rules that are included in BIP 125 that make it slightly more complex, but they're necessary to prevent people using BIP-125 to create DOS attacks.
For example, one of the sub-rules is that you have to increase the fee rate of the transactions by at least one Satoshi per virtual byte.
And this is to prevent something like, let's say I send out a transaction, I mark it as replaceable, and then I send out another one, and it has one extra Satoshi.
And then I do it again and again and again.
The fee is one extra Satoshi.
The fee has one extra Satoshi.

Speaker 0: 00:18:33

Right, so maybe I spend some of my outputs to you and I have a change output to me and I just reduce the amount of that change output by one Satoshi.
And that's incentive.
If we're talking about incentive compatibility, the miner wants that second one, right?
Because they get one extra Satoshi.
But then I can do it again and I can send a third transaction which bumps the fee by one additional Satoshi and again and again.
But the outcome of that is I've used up a whole bunch of bandwidth, enormous amount of bandwidth, potentially, and not just bandwidth between me and you, or me and my peers, but bandwidth between my peers and their peers and their peers, and it kind of propagates out through the network.
It's a transitive bandwidth usage.
So very cheaply, I can use up loads of bandwidth across the network.
So how do we stop that?

Speaker 1: 00:19:27

Well, we have that rule where you have to be at least incremental relay fee extra.
And there's also other rules about like you can't evict more than a hundred transactions.
You can't cause a lot of churn and you can't cause just like endless replacements.

Speaker 0: 00:19:45

So this is a great example of that difference between the ideal mempool, which is maximizing fee for the miners, and a real world mempool that has some constraints on its resources.

## Transaction pinning attacks

Speaker 0: 00:19:57

Okay, well, that's not quite the end of the story, is it?

Speaker 1: 00:20:00

Yeah, well, so like it's, you have a trade off between you want it really accurate, but also you don't want to spend too many resources.
But those heuristics that you're using to bound the computational resources, if you're too restrictive, or you make them too naive, they can, like an attacker can take advantage of that to pin a transaction or even censor a transaction in some cases.
So a pinning attack is where an attacker is able to prevent a transaction from being mined, typically by dragging down the fee rate.
So you can imagine, let's say, Alice and Bob are creating a transaction where they each have an output.

Speaker 0: 00:20:44

OK, So for example, a lightning, some kind of transaction.

Speaker 1: 00:20:47

Yeah, like a lightning close or something.
Yeah.
And so let's say Bob doesn't want this to get mined just yet, or let's say he just wants to delay it from being mined.
So he wants to pin it in mempools.
So one policy that we have is we limit the amount of descendants or the total size of the transactions and its descendants in the mempool.
And this is to prevent us having to go through very complex computation to evict or update these transactions.
We don't want huge chains of families.
And so one of the rules is Allison Bob's transaction, plus all of their all of its descendants cannot be more than 101 kilovirtual bytes.
So Bob could pin this transaction by publishing a child that spends from his output and just dominating that limit.
And so this would prevent Alice from publishing a child-faced parent like fee bump together transaction mind in a block, because if she tries to submit something to the mempool, it'll be like, oh, sorry, you've already hit your descendant limit and I'm not going to validate this.
So that would be a pinning vector.
So we can't have too naive, in response to this, we have CPFB carve out, which I guess we probably shouldn't get into today.
But that's an example of why if you have too simple of a heuristic, it can be taken advantage of.

Speaker 0: 00:22:21

Yeah, that's a very good point.
And pinning is a fascinating subject that we can talk about some other time.
But maybe important to highlight the difference there.
But When you say attack, it's not really attacking the mempool, it's attacking users or people involved in contracts, in smart contracts or Lightning or whatever.
Just that having these policy rules is something that people implementing those contracts need to keep in mind and add some kind of complexity or difficulty to implementing those things cool the third policy rule you talked about was Discourage upgradeable thing.

## Mempool policy: Discourage upgradable NOPs, witness versions, taproot leaf versions, etc

Speaker 0: 00:23:00

Yeah.
Okay.
So can you give examples of that?

Speaker 1: 00:23:04

Yeah.
So, you go to source slash script slash interpreter dot h, you get a bunch of script verification flags.
And those are kind of like the little buttons that you push in your script interpreter to say like what rules to apply.
And some of them might be like enforced taproot rules.
And so that would be the flag that we push on activation day.
But even before we had taproot, Even before we thought about Taproot, we had Segwit, which started with version, Witness version zero.
And part of that was a policy to discourage upgradable witness versions.
So if we saw something trying to spend version one and above, if we saw it in a block so that we would have a soft fork, we would accept it.

Speaker 0: 00:23:59

Just to recap how soft forks work, the rules start off as relaxed, and then a soft fork tightens up those rules.
So from forever, a witness output has been spendable, it's been consensus valid, and then, So a witness output is a push of one byte, which is between 0 and 15.
The version followed by the program, which is some number of bytes.
I can't remember what the limit on the number is, but that's always been a valid spend according to consensus.
And then Segwit came along and made witness version zero.
So that's a push of zero followed by a push of 20 bytes or 32 bytes invalid unless it was correct according to the Segwit rules.
But a push of one byte and then a push of any number of bytes, so one and then in something, is still consensus valid today.
And then we'll have a soft fork in November that will tighten up those rules and add semantic meaning to how we can spend that output.

Speaker 1: 00:24:59

Right.
But.
But we discourage, not disallow, but discourage version one even today, even though Tabard is not active in policy, not in consensus.
And this prevents a scenario where, let's say your node has not yet upgraded to include the activation rules or not even upgraded to 0.21 for the taproot rules and someone is spending a witness version one and you validate against your mount pool and you like accept it because we have like, according to your node, it's not aware of any rules around witness version one and then accept it to the mount pool and then like activation rolls around and then you still have that floating in your mempool, that's not possible because you are discouraging that and not accepting it to your mempool.

Speaker 0: 00:25:57

Okay, so when activation happens, which will be November, there won't be any transactions in my mempool or a miner's mempool that are spending taproot outputs.
Because prior to that, there was no way to validate them.
The taproot rules were not being applied.
Well thank you Gloria, it's been fascinating.

Speaker 1: 00:26:16

Thank you John.

Speaker 0: 00:26:17

Let's do this again sometime.

Speaker 1: 00:26:18

Let's do it again sometime.
Bye-bye.
