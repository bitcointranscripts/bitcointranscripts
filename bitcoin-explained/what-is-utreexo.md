---
title: What Is Utreexo?
transcript_by: Sjors, edilmedeiros
media: https://www.youtube.com/watch?v=sWK7aqPjQLI
tags:
  - utreexo
speakers:
  - Sjors Provoost
  - Aaron van Wirdum
  - Ruben Somsen
date: 2020-10-30
episode: 15
summary: The discussion revolves around Utreexo, a novel proposal aimed at enhancing Bitcoin's scalability by optimizing the UTXO set storage through a compact, Merkle tree-based structure. Utreexo seeks to address the challenges of node synchronization speeds and RAM usage by allowing nodes to store a much smaller representation of the UTXO set, thus potentially accelerating the syncing process and making the network more efficient. The conversation delves into the technical mechanisms of Utreexo, its implementation challenges, and the practical benefits it offers, including reduced memory requirements and the facilitation of faster node operations. While acknowledging Utreexo's promising advantages for Bitcoin's scalability, the participants also weigh its potential downsides, such as increased bandwidth for block transmission and the necessity for significant network adoption to realize its full benefits.
---
## Introduction

Aaron van Wirdum:

And the proposal we're discussing this week is Utreexo.

Ruben Somsen:

That is correct.

Sjors Provoost:

Utreexo, and the tree is for tree.
The thing that grows in the forest.

Aaron van Wirdum:

Did you know that was the pun, Ruben? I didn't realize...

Ruben Somsen:

Well, I heard Tadge say that so I was aware of that, but there is a very specific reason why I was enthusiastic to talk about it.
Well, one, I've used it in one of the things I've been working on so I like Utreexo a lot conceptually.
But there's also a close friend of mine, Calvin Kim, who was a regular attendee of the Seoul Bitcoin meetup who is now actively working on Utreexo together with Tadge and I told him I would shout out the other guys that are working on the project.
Jannis Trulsen, which is apparently not a Dutch person.
I think he's German or something.
And Niklas Gögge.
Hopefully I pronounce it correctly, but those are the four guys that are currently working on Utreexo.
Hopefully it will eventually get to a point where this can be useful for Bitcoin.
But we should obviously start explaining what Utreexo is, because we're just talking about the conceptual-

Sjors Provoost:

Oh, we've got to keep it exciting.

Aaron van Wirdum:

Well, really quick.
Are you guys with DG Lab?

Ruben Somsen:

No, no, that's completely separate, yeah.
I'm not super familiar with this, but Tadge is with MIT, and then the other three guys are just working on this separately.
So they're not involved with MIT or DG Labs.
DG Labs mainly works on DLC.
That's one of their main projects.

## The UTXO Set and Its Challenges

Aaron van Wirdum:

So Sjors, what problem are we solving?

Sjors Provoost:

Problem, problem.
Challenge.
No, so one of the constraints when you're syncing a new Bitcoin node, we talked about sync a couple times, is the amount of RAM memory you have.
Now, it's not a hard constraint.
You don't need a lot of RAM, but if you want to sync it fast, you do.
And the reason is this thing called the UTXO set.
The UTXO set is a list of coins that you own, and we talked about that last time, I guess.
But every time the new block comes in, what you do is, for every transaction in the block, you check if it's spending something that exists, namely, one UTXO.
And so in order to check if something exists, well, it has to be somewhere.
It has to be in a database of sorts.
And where is that database? Well, if that database is sitting in your RAM memory, that's extremely fast.
If on the other hand, that database is sitting on your hard disk, if it's an SSD drive, it's meh.

Aaron van Wirdum:

What you mean is, it's much faster to look up if it's in there.
If it's in your RAM, then your computer will be able to look it up within...
Well, I don't know how fast, but faster than if it's on your drive, at least.

Sjors Provoost:

It's probably at least 10 times faster than if it's on your SSD drive, and if you're using a magnetic drive, it's even worse.
And then the other side of it is, once you create this new coin, which the transaction does on the output side, it has to store that.
So it has to write it somewhere on the disc, which is also slow.
And if you have a magnetic spin disc, then it has to move to read somewhere and it has to move somewhere else to write again and these are gigabytes apart, so that's horrible.

Aaron van Wirdum:

So to make it very concrete, I guess the biggest difference you would notice when you're syncing a new node, and if you would somehow be able to keep the UTXO set in RAM, it will only take, I don't know, couple hours?

Sjors Provoost:

But it depends on your computer.
I have a somewhat recent MacBook Pro and I think I can sync the whole chain in five hours-

Aaron van Wirdum:

If you keep it in RAM.

Sjors Provoost:

But that takes about 11 gigabytes of RAM.
But if you do it on, say, a typical Raspberry Pi, you might have two gigabytes these days, maybe four.
So that means you're going to sync the chain and you're going to keep as much as possible in RAM, but at some point it overflows, the UTXO set, and then usually what it does is it writes everything to disk, clears everything, and then it starts caching again, and this takes a long time.
It can take days on these machines.

Aaron van Wirdum:

So the point being, as you can keep more of the UTXO set in RAM, you'll sync faster, or your node will just work faster, operate faster in general.
So it would be good if we could somehow decrease the size of the UTXO set.

Sjors Provoost:

Well, we can't decrease the size of the UTXO set.
That's the problem.

Aaron van Wirdum:

That's a bummer.

Sjors Provoost:

There is a limit on the size of blocks.

Aaron van Wirdum:

Well, it can decrease-

Sjors Provoost:

For megabytes.

Aaron van Wirdum:

It can decrease, it's just not something we can do.

Sjors Provoost:

Yeah, it decreases when people spend-

Aaron van Wirdum:

I don't know how much UTXOs you own, Sjors.
I bet a lot, so maybe you could play a part in decreasing the UTXO.

Sjors Provoost:

I have millions of UTXOs on testnet.
No, so the idea is that if you're spending more coins than you're creating, then obviously the number of UTXOs goes down and the RAM usage goes down.
But there's a lot of junk in the UTXO set, because there were people in the old days that created transactions to multi-sig addresses that were fake just in order to put pictures of Obama in the blockchain.
And those are all sitting in your RAM because you node has no idea that they're nonsense.

Sjors Provoost:

But the other thing is, if we expect everybody in the world eventually to use Bitcoin and everybody to have at least one or two UTXOs, well, that's a lot of RAM.
That's like seven billion people.
And there's really no limit to how big that can get, there's no constraint.
It might take a while because it takes a lot of fees to create all these transactions, but eventually it could take as much RAM as...
There's no limit, and we don't like things that don't have a limit.
Unbounded stuff, it's a bit bad.

Aaron van Wirdum:

Yeah, you mean the UTXO set can get as big as it will get until the point where not everyone can use it and sync it from RAM?

Sjors Provoost:

Fewer and fewer people will have enough RAM to sync it quickly and that could become a problem.

Aaron van Wirdum:

Okay, so you agree, it's a problem.
Not just a challenge.
It a problem, Sjors.
Now how do we solve it?

## What is Utreexo

Sjors Provoost:

Yeah, it's a challenge.
Well, one way to solve it is Tadge Dryja's proposal, the Utreexo.

Ruben Somsen:

That's right, yep.

Sjors Provoost:

And the idea there, I guess that's what we'll need to explain, right? How that works.

Aaron van Wirdum:

Well, Ruben wanted to explain it to us, so let's hear it.

Ruben Somsen:

Well, I first wanted to say that I thought, Aaron, your analogy with basically saying that it's pruning for the UTXO set, I thought that was a very good analogy, where currently we have pruning in Bitcoin-

Aaron van Wirdum:

This was an off-record analogy.
But now it's an on-record analogy.

Ruben Somsen:

Now's it's on record, yes.
I'm repeating something that you had told me before the show.
So with Bitcoin, currently you have pruning in the sense that you take a block, you process it, you extract the UTXO set out, basically from all the blocks, and then that's all that you keep.
You only keep the UTXO set and then you can throw everything else away and that's called pruning.

Ruben Somsen:

There is a downside, which is that then you don't have the blocks.
So if you want to prove to another person that the UTXO set is valid, you can't actually give them the blocks, but the assumption is that somebody else will have the block so it's fine.

Ruben Somsen:

And here, what you're pruning is something else.
You're pruning UTXO sets and your essentially throwing away all the transactions and you're just keeping a Merkle roots.
And inside of that Merkle roots is basically a commitment.
Every single UTXO is committed in there and you only keep the Merkle proofs of the UTXOs that you care about, that you own.

Aaron van Wirdum:

What is a Merkle root?

Sjors Provoost:

Maybe to put it another way, normally when somebody sends you a transaction, the transaction says, 'I'm spending this input and you, as the person running a node, has the responsibility to check whether that input exists in your own database.' And you're flipping this around and you're telling the other node, 'I have no idea which coins exist, because I don't have RAM.
You prove to me that this coin actually existed.' And that's what you use this Merkle proof for.
So the burden of evidence is reversed here.
You need to prove that a transaction exists.
And then the question is how are we going to do that?

## Technical Mechanisms of Utreexo

Aaron van Wirdum:

Okay, so we're reversing the burden of proof.
Usually when you're sending a transaction...
When I send a transaction to you, Sjors, then you check inside your node and the database with your UTXO set, whether the transaction is spending valid UTXOs.

Sjors Provoost:

Yes.

Aaron van Wirdum:

Now I'm actually going to have to provide you with the proof that my transaction is spending existing UTXOs.
However, you still need something in order to make sure that my proof is valid, and that's this Utreexo, which is a hash tree.

Sjors Provoost:

Yes, a Merkel tree of hashes.

Aaron van Wirdum:

A Merkel tree, right.
So what is this and how does it work?

Sjors Provoost:

It's kind of nice.
All the UTXOs that are in existence would be put into this tree and everybody can construct this tree if you replay the whole blockchain.
But the question is-

Aaron van Wirdum:

It's not an actual tree though, is it, Sjors?

Sjors Provoost:

It is not an actual tree.

Ruben Somsen:

Do you give it water?

Sjors Provoost:

No, basically what the tree would look like is you have the first UTXO, and then the second UTXO right next to each other, and then you take the hash of those two, basically combined, and that is one new hash.
So, you see this little pyramid shape and you can do that again for another two UTXOs that exist.
They have their own little mini tree, but now you see, oh, there's two trees.
Let me just combine those two trees.

Aaron van Wirdum:

Two hashes, and you're combining these two hashes, yes.

Sjors Provoost:

So now you have four UTXOs.
Two of them are shared and then those two are shared again.

Aaron van Wirdum:

Yeah, so you end up with one hash?

Sjors Provoost:

You end up with one hash.
Now, the key here is that these things are so called, I believe, perfect trees, which means that they are always a multiple of two.

Aaron van Wirdum:

And so now the challenge is that for every new block, this tree needs to be updated, right? Because we have one big tree for all of the UTXOs.
Now a new block is found, it includes all sorts of new transactions, so new UTXOs exist and old UTXOs are destroyed, so now we need a new tree.

Sjors Provoost:

Yeah.
Well, it's even more than one tree, right? It is a forest.
Every tree has to be a multiple of two, so there can be four things at the bottom or eight things at the bottom or 16 things at the bottom.
When you have a number of transactions that doesn't fit that way, you'll have multiple trees that look like that.
So you have a collection of trees for which you really only need to remember the top hashes.
And now the question is, how do you add something to that tree?

Aaron van Wirdum:

So you might have one tree with 16 at the bottom, one tree with eight at the bottom, one tree with two UTXOs at the bottom.

Sjors Provoost:

One at the bottom.

Aaron van Wirdum:

Yeah, exactly.
So you have multiple trees.

Sjors Provoost:

Yeah, right.
And now in order to prove that something is in this tree and also to replace it with, say, the output...
Because basically you destroy one UTXO so that you're spending and you create a new UTXO you're creating.

Sjors Provoost:

So you can actually take the UTXO that you're spending out of the tree and then put the new one into the tree.
And in order to do that, you need to recalculate the tree and you do that by knowing its neighbors.
So, the way you prove that something is inside a Merkle tree is to say, well, at the bottom of the tree, there's these two pairs and I'm going to give you the other side.
And then at the next level, again, there's a pair and I'm going to give you the other side.
And again and again and again, and that proves that something is actually in the tree.
And that's exactly the same information that you need to put something else at the bottom of the tree, and then provide the new hash.

Aaron van Wirdum:

So by putting something else at the bottom of the tree, to be clear, the entire tree changes, or at least the one hash you end up with changes.
You're just computing a whole new tree, but you're able to do that because you have all the data you need.
So you can add things to the forest and you can remove things from the forest.
It's actually possible.
It's actually easier than I thought it would be when I saw Tadge explain it.
I don't know if it's going to be easy when people hear us explain this.

Sjors Provoost:

I recommend looking at Tadge explain it after you hear us explain it, because you need to see it-

Aaron van Wirdum:

Yeah, visuals really help.

Ruben Somsen:

Exactly.
I think his presentations are great.
He's very good at explaining it and he has slides so that's a lot easier than what we are doing.
We're trying to explain it in words.
Especially in Merkle trees, I think, it's great if you have an actual picture there.

Sjors Provoost:

But now the idea is that you're not tracking everything.
So you could, when you're syncing the blockchain, keep track of the entire tree, but then you need a lot of RAM, just like in the original scenario.
But what you'll actually do is you're going to remember the top of every tree and there might be 10 or 20 or whatever trees, and that's all you're going to remember, and when somebody has a new transaction that you want to verify, they need to give you the Merkle proofs for all the inputs that they're spending, so they prove that they exist.
And then they also tell you which outputs are there, which are going to be swapped in at the same places where those inputs were.
Plus new trees if it's making more.

Ruben Somsen:

The outputs are under blocks, right?

Ruben Somsen:

Yeah, so that's really, I think, the very elegant side of Utreexo, where the same proofs that are proving that these UTXOs are in the UTXO set, are also exactly what you need to remove them from the set, update your root hash and add the new UTXOs from the latest block, so that works out quite elegantly.

## Implementation and Practical Considerations

Aaron van Wirdum:

Okay, so in an ideal scenario...
What we've been explaining so far is the ultimate version of Utreexo, so let's stick with that for a minute.
So I wanted to send a transaction to the network and you, Sjors, you had a node and you wanted to validate the transaction.
You have this tree in your RAM apparently.
That's what's nice about it.

Sjors Provoost:

I have the top of the trees in my RAM.

Aaron van Wirdum:

Yeah, exactly.
So now I want to send this transaction, so now it's my responsibility to send to you the transaction, as well as the proof that the transaction is valid, which also includes information for you so you know where to find it in the forest, right?

Sjors Provoost:

Exactly.
You need to prove to me that the things you are spending are in the forest, because I forgot what the forest looked like.

Aaron van Wirdum:

All right, so that's me sending the transaction with the proof.
Now, the other way you could get a transaction is if it's already in the block.
So if a miner mines a block and the transaction is in there, you still have your Utreexo thing on your node.
But how do you now get the proof?

Sjors Provoost:

Right, because if you spend the transaction, you're not going to talk to every node that ever downloaded a block to send that proof around.
So how does that proof get to the node?

Aaron van Wirdum:

That wouldn't scale very well, at least.

Sjors Provoost:

No.
Well, what you would probably want to have is something called a bridge node.

Aaron van Wirdum:

A bridge node.

Sjors Provoost:

A bridge node would be a node that has the actual UTXO set, the old-fashioned way, so it has lots of RAM or it's just slow.
And it produces all these proofs and it sends them around to whoever wants them.

Ruben Somsen:

Yeah, so what essentially happens is that when this bridge node receives a transaction and this transaction does not have a Merkle proof, proving the inclusion in the Utreexo root, this bridge node basically just takes the proof that they have and they attach it to the transaction and now they send it on to other Utreexo nodes.
It's a bridge between Utreexo nodes and non-Utreexo nodes.

Aaron van Wirdum:

But they could also construct the proof themselves, right? If they see a certain transaction is included in a block, they can just figure-

Sjors Provoost:

That's right, there's nothing secret here.
So if you have the original UTXO set in memory somewhere, you can construct the proof for any transaction.

Ruben Somsen:

And they have the entire tree, essentially.
So the entire UTXO tree that you create and then prune, they just don't prune it essentially.
So they just have the full UTXO set.
Basically, the UTXO set with all the Merkle proofs connecting to it, so then they can just take any UTXO in there and create a proof from it and just send it on, or for an entire block or whatever.

Aaron van Wirdum:

Right, so what would happen in practice? Sjors, your node would see a transaction in a block and it would wonder, 'Hmm, is there actually proof for that? I never saw the transaction before.' And you would request it from a bridge node.

Sjors Provoost:

My guess is, when you get the whole block, you're going to call a bridge node and say, 'Give me the proofs for that entire block.'

Aaron van Wirdum:

Just all of them?

Sjors Provoost:

Yeah.

Aaron van Wirdum:

Why not just the ones you need, the ones you haven't seen before?

Sjors Provoost:

My guess is that's too much back and forth because if you have to call a node for every single individual transaction, and that's a lot of overhead, whereas just downloading a couple hundred kilobytes is easier.

Aaron van Wirdum:

Anyways, that's an implementation detail.

Ruben Somsen:

Yeah, but I think this is just an automated process, where you just connect to the network.
But the problem is, when you're the first Utreexo node, and you're pruning all the data and then everybody else on the network is an old-fashioned node, like the way we run it today, nobody's going to give you the proofs, right?

Ruben Somsen:

So what you need is at least a single bridge node, so at least you can connect to that one.
And then other people are connecting to the bridge node because the bridge node basically speaks both languages.
They speak the Utreexo language and they speak the old-fashioned language.
So they translate for you, and as long as one bridge node exists, it can bootstrap the network essentially, but they don't have to have special rules.
From the perspective of the Utreexo node, the bridge node is just also Utreexo node, and from the perspective of the old-fashioned nodes, it's just an old-fashioned node.

Sjors Provoost:

Right, that's another point.
So, you don't need everybody to do this translation, only one person needs to do it or a couple.
The other nodes know how to relay that information even if they can't produce it, so that's good news.
But of course-

Aaron van Wirdum:

Can we have a future without bridge nodes?

Sjors Provoost:

Well, we should point out what the problem is with these bridge nodes, because they are nice people.
We don't want to rely on nice people.
That's not how we roll, because nice people can stop being nice.

Aaron van Wirdum:

Or they can be forced to stop being nice.

Sjors Provoost:

Or they can just disappear or run out of battery.
Then you can look at the longer-term picture, if people like this given the advantages, or even if they don't like it, if the UTXO set just becomes insane and it just takes too long to sync on any normal computer, then you could basically make a soft fork which contains the proofs.
So the proofs become part of the blockchain, just like SegWit added the whole bunch of data to blocks.
You could then add these proofs to the blocks, making the blocks even bigger.
But the trade-off there is, you have more bandwidth, but you have less RAM need.

Aaron van Wirdum:

Yeah, the reason this could be done as a soft fork, same with SegWit, is because you'd include the hash of the proofs somewhere in the coinbase transaction or something like that.
Old nodes just won't notice anything interesting, but upgraded nodes will see a whole tree, which they share with each other, which does make the blocks a bit bigger for them.

Sjors Provoost:

Yeah, so old nodes keep doing what they're doing.
They get blocks, they can verify those blocks, because nothing changes about the transactions in the blocks.
New nodes will save some RAM memory.
They'll use that extra data.
They'll download that extra data and they'll use it.
That's generally the idea.

Ruben Somsen:

Yeah, so personally at least, I think this is not likely to happen until we really get a UTXO set bloating issue where the UTXO set becomes so big that people start liking this trade-off to the point where it's preferable.
I think as long as we're not at that point, I don't think we'll see this as a soft fork, but that's my personal view.

## Potential Benefits of Utreexo

Sjors Provoost:

I do want to point out some cool things you can do with it.

Aaron van Wirdum:

Yes, tell us the bullish part, Sjors.

Sjors Provoost:

I'm all just copy pasting from what Tadge said, we like to do that.
Basically because you don't need a lot of RAM, you can start doing things in specialized hardware like in ASIC, because one of the things that's hard to do in an ASIC is lots of memory.
And having specialized hardware, maybe it's a part of your chip, so maybe Bitcoin becomes the standard and every phone that you buy has a CPU, has a little mini processor right next to it that just checks all the Bitcoin validation rules.
And because it's custom silicon, it might be able to validate the entire blockchain at the speed that it can download it, which is pretty cool.

Aaron van Wirdum:

An ASIC for regular nodes?

Sjors Provoost:

Exactly, yeah.
So not to mine coins, but to verify coins, which would be cool.
And then you have the protocol literally set in stone or at least set in silicon.
And of course soft forks can still happen under that circumstance, but if somebody wants to do a hard fork, you'd have to break all the node hardware, and not just all the mining hardware.
So, that's a nice extra barrier to not do hard forks.

Ruben Somsen:

It's ossification-

Aaron van Wirdum:

It's also not perfect for soft fork.
Is that what you just said, Ruben?

Ruben Somsen:

No, no.
That's what Sjors just said.

Sjors Provoost:

I think its hard to verify soft forks.
You don't have to verify the soft fork, but you can't verify the soft fork, at least not with the accelerated hardware, so your computer would have to slow down to check all the new rules whenever it encounters it.

Aaron van Wirdum:

Yeah, or you would have to buy a new phone because the soft fork happened.

Sjors Provoost:

Exactly.

Ruben Somsen:

Your phone is too old, maybe it's possible, right? That's that's what happens now.
People buy new phones every couple of years, so maybe it's not too much to ask.

Aaron van Wirdum:

True.

Sjors Provoost:

The other thing we talked last week about is Assume UTXO thing, where one of the problems is, now when you start, you still need to get that three gigabyte thing from somewhere.
And if this thing becomes a hundred gigabytes, you have to get that from somewhere.
But now, with this proposal, we just have a kilobyte.
So you can put the entire UTXO set, you can represent it in a kilobyte which can just be inside the source code.
So, you don't need a hash and then go and fetch something, you just put the thing itself in there and know it's going to start instantly at that height and then do the same thing that we described last week.
So, sync all the way to the tip and then start the genesis and make sure everything is what it should be.

Ruben Somsen:

Yeah, that's a really nice feature that you have the entire UTXO set in essentially a single hash or a forest.

Sjors Provoost:

Yeah, a small little forest-

Ruben Somsen:

One kilobyte, yeah.

Aaron van Wirdum:

Are there more benefits?

Sjors Provoost:

Yeah, so the last one would be, you could sync with a phone node.
So right now, if you have a node on your phone, it might be very slow.
Maybe with this proposal, it wouldn't be slow, but let's say it's still slow.
What you would do is you sync your node on your desktop or whatever it is, you scan a QR code which can be pretty long, and now your little phone has the recent UTXO set and that doesn't even require any kind of commitments, because your phone trusts your laptop.
So that's a feature you could use right now.

Aaron van Wirdum:

Are there any downsides or risks? Ruben, you thought about this?

Ruben Somsen:

Sure, but I want to add one more interesting feature that we haven't discussed yet.

Sjors Provoost:

Before we burn it all down.

Ruben Somsen:

Before we burn it down, yeah.
It's a good question though.
And that's parallel validation.
So what you can do is, you can theoretically take two computers and just take a Utreexo hash off the middle state of the blockchain.
So, if we're at block 2000, you just take block 1000 and you take the Utreexo hash from that moment in time, and then you start validating 1000 to 2000.
And on the other computer, you start validating 0 to 1000.
And if they match up after you validated both, then you validate the entire blockchain while splitting up the work.
And that's interesting and can be very useful, I think, maybe in the future also when you have more and more CPUs on a single chip.

Sjors Provoost:

Right, so it wouldn't be necessarily multiple computers doing this, but just multiple chips doing it, because we see that clock speed is not going up much.
But you get more and more parallel stuff, and the problem with the Bitcoin chain is, you can verify signatures in parallel and a Bitcoin node does that, but some things are intrinsically serial, so you cannot verify block 10 before you've verified block 9, and it's nice if you can get rid of that.

Ruben Somsen:

Yeah, so now you can essentially.

Sjors Provoost:

You can too with the Assume UTXO but you need multiple, very large snapshots.

Ruben Somsen:

Yeah, exactly.

Sjors Provoost:

So, very cool stuff.
So let's burn it down.

Aaron van Wirdum:

Go for the kill, Ruben.

Ruben Somsen:

One more thing to add is apparently you can also do a backwards validation.
I'm not sure exactly how it works, but apparently you can go from block 1000 to 999, so that's possible too.

Sjors Provoost:

Well, you need to, because you need to be able to roll back.

Ruben Somsen:

That too, yeah.
I just haven't looked into that sufficiently to fully grasp it-

Sjors Provoost:

You just explained that in order to prove that something is in a Merkle tree, that's the same thing you can do to change something in a Merkle tree.
So you can change the old thing with the new thing that way, or you can change the new thing with the old thing.

Ruben Somsen:

Right, so it makes sense.
I agree with that, I just haven't sat down and just gone through it.

Sjors Provoost:

One other thing we can also mention is that this tree that we just described, the general name for it is an accumulator.
It's something that you can use to add stuff to, and in this case also remove stuff from.
But there are all sorts of mathematical tricks you can deploy to do this.
This is just something that's conceptually simple.
If other people than us explain it and you see it in front of you, it's very simple with the Merkle trees, but there's been other proposals, like an RSA accumulator.
There's all sorts of cool cryptographic math you can do to just add things to a set and remove them from a set, essentially.
Perhaps another mechanism would be used eventually.

## Challenges and Downsides of Utreexo

Ruben Somsen:

Right, and that's maybe also one of the downsides that we can talk about now, where if you start using this and then later somebody finds a better accumulator, then you have to, yet again, switch to that next proposal, which is okay as long as you don't commit it into a block.
But once you make this an actual soft fork and then you find, 'Oh, there is this even better accumulator that we should have been using,' now you're stuck because you can't undo a soft fork, at least not unless you put in some kind of sunset date or something.
But that's generally not really done, at least hasn't been done so far.

Sjors Provoost:

No, so that's another reason why you wouldn't expect this to be a soft fork, unless the world is burning or it's been used for so and so long that people think, 'Okay, this is mature.' But we're nowhere near that.
It's pretty experimental, as many of the things we discuss here.

Ruben Somsen:

And I guess the second thing that I consider a downside is that bandwidth seems to be pretty much the bottleneck right now for Bitcoin.
And this is something that makes that bottleneck worse.
So for that reason, I personally see this as more of an option that people can opt into if, in their case, bandwidth isn't a problem, but they're CPU, or Disk I/O restricted or RAM restricted, or maybe they want to use an ASIC or something like that.
So from that perspective, I don't expect everybody to use this, but I also think Sjors pointed out correctly that if the UTXO set grows to a significant degree where it does become a burden and it slows down validation, then maybe this becomes more appealing.

Sjors Provoost:

Yeah, so keep an eye on it.

Aaron van Wirdum:

Yeah, and I guess the increased block size in one of the variants could be considered a downside.
Although I think that-

Sjors Provoost:

Well, that's what we meant, with more bandwidth basically.

Ruben Somsen:

Exactly

