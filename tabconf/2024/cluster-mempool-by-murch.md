---
title: Cluster Mempool by Murch
speakers: null
source_file: https://www.youtube.com/watch?v=PeqE0Gqs9g4
media: https://www.youtube.com/watch?v=PeqE0Gqs9g4
date: "2024-12-20"
summary:
    "Cluster Mempool is an effort to rearchitect how Bitcoin Core stores\
    \ unconfirmed transactions, builds blocks, and evaluates replacement candidates.\
    \ It is expected to drastically simplify package relay with bigger packages than\
    \ two transactions, speed up block building, and generalize CPFP to descendants-pay-for-ancestors.\n\
    \n What would an attendee learn from this talk?\n\n- What issues exist in the\
    \ current mempool design?\n- How does the Cluster Mempool approach address those\
    \ issues?\n- How does Cluster Mempool work?\n- How does this change affect users\
    \ and other network participants?\n\n Is there anything folks should read up on\
    \ before they attend this talk?\n\n- Basic knowledge about unconfirmed transactions\
    \ and mempool is useful\n\n Relevant Links\n\n- [Proposal for a new mempool design\
    \ bitcoin/bitcoin#27677](https://github.com/bitcoin/bitcoin/issues/27677)\n- https://delvingbitcoin.org/t/cluster-mempool-definitions-theory/202\n\
    - https://delvingbitcoin.org/t/cluster-mempool-rbf-thoughts/156\n- https://delvingbitcoin.org/t/how-to-linearize-your-cluster/303\n\
    \n About the Speaker\n\nMurch is an engineer at Chaincode Labs. He contributes\
    \ to Bitcoin Core, Bitcoin Optech, and Bitcoin Stack Exchange. He is a co-host\
    \ of NYC BitDevs and the Bitcoin Optech Recap.\n\n Social Links\n\n!https://github.githubassets.com/images/icons/emoji/octocat.png\n\
    \nhttps://github.com/murchandamus/\n\n\U0001F426 https://twitter.com/murchandamus\n\
    \n\nTABConf 6 GitHub link\nhttps://github.com/TABConf/6.tabconf.com/issues/45"
tags: []
categories:
    - Education
transcript_by: 0tuedon via tstbtc v1.0.0 --needs-review
---

Speaker 0: 00:00:05

Hi. Sorry for running a little late.
We're going to talk, I'm Mert, nice to meet you all.
We're going to talk about Cluster Mempool today.
Cluster Mempool is a work by primarily Suhas Daftwar and Peter Welle.
So I'm reporting on other people's work.
I've been a close by bystander, so I hope I'll be able to give you a good overview, but I might not be able to answer all your questions, but keep them coming anyway.
So generally the idea with cluster mempool is to basically change how the data structure, the mempool data structure inside of Bitcoin Core would work and we're, it's a little reverb-y up here, is that normal?
Excuse me.
It's pretty reverb-y up here.
Yeah, thank you.
Okay, yeah, much better, thank you.
Yeah, okay, cool.
So the idea is to re-architect how the mempool works.
The mempool is a data structure, of course, that we use to keep track of all of the unconfirmed transactions that your node knows about, right?
So We use this, of course, to do several things.
For example, to build block templates, to inform ourselves of our fee rates that we should be using when we're building transactions, to manage our resources if the mempool overflows and we are, for example, running on a device that has limited memory, we can't keep everything that we ever learn about because sometimes there's just more transactions than fit into our memory.
So we'll have to know which ones we want to keep.
And in case we have multiple transactions that we want to relay at the same time, we also use the information in the mempool to decide which ones we prioritize.
So, I don't know how many of you have a good idea of how the mempool works today in Bitcoin Core, so I'm gonna talk a little bit about that.
The mempool currently uses something called an ancestor set to decide which transactions will be picked into the block next.
So for every single transaction, we look at what other transactions have to go into the block before them, their ancestors.
And this is the context by which we can decide how interesting it is to pick a transaction into the block next.
So if we look at this very simple example with five transactions, we can think about what the dependencies for each transaction is.
So for example, let's talk about it a little first.
So for example, transaction A doesn't have any ancestors and its ancestor fee rate is one sat per V byte.
It would be, if there were no other transaction that were connected to it, it would be picked into a block at one sat per V byte.
Transaction B though, makes this a CPFP constellation, the child pays for the parent.
So together, these two transactions as a package are a lot more attractive than one set per V byte.
All my transactions here have the same size, so the package AB will have a fee rate of eight sets per V byte.
15 plus one divided by two, very simple.
So it gets a lot more interesting if you have two children because for C, C alone would be picked into the block at five sets per rebuy.
D does nothing to help with that because D itself would only be picked into a block at three sets per rebind.
But E is also a CPFP here, so E will bump C to a fee rate of six set per rebind in the package.
The thing is, of course, you can't put E into the block before C is in there, otherwise the output doesn't exist that E spends, right?
So, if we look at this table, The first thing that will get picked into the block out of those five transactions is A and B together.
A first, because topologically A has to stand in front of B in the block.
And then the next thing is C and E, and last, D will be picked into the block.
So far, so simple.
We see one of the first problems right here.
So the ancestor set fee rate of D, if we look at all the transactions it depends on, would calculate to be four sets per V byte.
But actually, if that conflicts, or if the ancestor set fee rate is higher than the transaction's individual fee rate, obviously it's more attractive to just pick the parent, right?
C gives us more fees per byte than D.
So actually D's fee rate in the end will only be three sets per V byte.
So the ancestor set doesn't actually inform us here.
This is a fairly simple example.
There's more complicated examples where this would have even more weight.
The problem is after you pick C and E into the block, you have to recalculate all of their descendants' fee rates because now the set of ancestors that they were calculated with has changed, right?
So while we're building a block template, every time we pick any transactions with descendants into the block, we have to recalculate all of their ancestors at fee rates.
That's kind of a drag.
A, because we don't know what fee rate they'll eventually be picked into the block, and B, because, well, yeah, because we don't know what fee rate they'll eventually have, and we have to do that extra computation.
Okay.
So this becomes a little more obvious if we look at the other side.
So let's say our mempool, someone is creating a staking protocol on Bitcoin, the mempool overflows, and we're starting to evict some transactions out of our mempool to reduce the memory footprint of that data structure.
If you look at this cluster, and we'll use that term more, a cluster refers to all the transactions that are related by parent-child relationships transitively, so like the biggest connected component in the mempool.
So we are looking at a cluster right here, a single cluster.
If you look at this cluster, does anyone want to hazard a guess which transaction we would kick out of the mempool first if we had to reduce the mempool footprint?
K, yes, excellent.
K has a fee rate of one set per rebuy, and clearly that's gonna get picked into the block last, per looking at this carefully.
And it also has the lowest descendant set fee rate.
So descendant sets are exactly the same as ancestor sets except we look at it from the other side.
So for a descendant set, we look at the transaction and all of its descendants, we sum up their views and sum up their sizes, and that gives us the descendant fee rate.
So if we look at what's gonna get picked into a block here, maybe that's not completely obvious, but, sorry, Let me tell you a little more about the other descendant set phi rates here.
So if you look at the descendants of I, I doesn't have any descendants.
It has the highest descendant set phi rate.
G and h both have a pretty decent descendant set phi rate of six because only I is a descendant of them.
And J has a great descendant set fee rate, especially once K is gone.
But F in this constellation after k is gone has the lowest fee rate.
So we kicked out k because it was the lowest, and now the next thing that we would evict out of this whole mempool would be f.
And once we kick out f, all of these other transactions are missing an ancestor, So we would literally kick out the transaction that we would mine next when we evict.
All right, maybe I jumped a little too far into this one.
When we evict, we want to really get rid of the transactions that we would mine last.
But in order to find out what we would mine last, the only way to really find out what their final fee rate would be would be to build a block of the size of the whole mempool.
We'd have to literally pick everything out of the mempool.
And then the last thing that's left over is what we want to throw away.
You might imagine if the mempool's 300 megabytes, our data structure is full because that's when we evict.
That's going to be a lot of computation.
And we don't want to do that for every single transaction that we evict.
So that's why we use this heuristic where we look at the descendent set fee rates and we just throw out what has the lowest descendent set fee rate.
But yeah, it's broken.
It doesn't give us the thing that we will mine last, but just the thing that has the lowest descendent set fewer.
All right, so far so good?
You see, it's pretty low here, I hope you can see it, actually, but F has only five sets per V by, which is the lowest that's left after case call.
All right, so we have found out.
Block building currently is expensive because we have to recalculate all the ancestor set scores whenever we pick any ancestors of another transaction into the block.
Eviction is broken, it doesn't actually evict the last things we want to mine.
And this one I haven't motivated more yet, but actually the current replace by fee rules do not always give us the best block templates.
So some, yes sir?
What do miners do with their?
Right.
Like, do they use any sort of block?
Okay, so what do miners do right now?
Actually, right now we do use this data structure with the multi-index.
For each transaction, We have the ancestor set score on record, and we have the descendant set score on record.
And we use those two indexes, one for the block building and one for the eviction.
It is highly optimized, and it works fairly well.
But there's a few issues with it.
And so this has motivated some people to put in quite the elbow grease to do a lot of research.
If you're a consumer of delving Bitcoin, you might have seen several chapters in a book of research on how we could improve this process.
All right, so what we really would, sorry, I was talking about the replace by fee stuff.
It becomes really, really hard to see what exactly you have to add where in a transaction graph in order to bump a specific transaction to an intended fee rate, or if you have conflicts, what you want to evict and what you want to keep.
I'll just leave it at that.
If you want to know all the details, I'm sure Gloria's written a few things about this.
All right, so what we would really love to have is something we have been calling a mining score.
A mining score that tells us at what fee rate a transaction will be mined into a block.
And if we had that for every transaction, we would know how to sort those transactions across the mempool, and it would inform us both for block building, for eviction, and for other matters like RBF.
Well, it turns out if we redesign how we keep all that data in the mempool, we can get pretty close to that.
So let's look at clusters.
What are clusters?
As I said, clusters are all the transactions that are related in some manner.
So in some manner.
So right here we're looking at three clusters.
There's A, B, C, D, and E, and the more complicated cluster that we saw for the descendants at fee rates.
Now, if you're thinking about what fee rate a transaction will finally have, or at what fee rate it'll effectively be mined into the block, you might realize that only transactions that are related to other transactions will affect their mining score.
The transaction D will not change at what fee rate transaction A will be mined into a block.
So what if we just pick apart the mempool, divide it into these clusters, and then we sort those clusters in the order in which the transactions would be picked into blocks.
Let's say I did that.
And we look at the first cluster.
The first cluster is gonna be mined in the order A and B.
B has a much higher fee rate, but it depends on A, so A has to stand in front of B in the block.
For CDE, E has the higher fee rate, and it bumps C, so it'll be C before E because C has to come first, but D will go last because it has the lowest fee rate.
And I've also done the third cluster where we find that J bumps F, and together they have a package fee rate of six SATs per V byte.
Then we get G, H, and I picked into the block at 13 thirds, 4.3 sets per V byte.
And last, we would pick K at one set per V byte.
So, this is actually fairly computationally intensive if your clusters get more complicated and get big.
This is actually one of the places where a ton of the research that Peter and Suhas have been doing, has been going into.
Like how do you linearize clusters as fast as possible?
What size clusters can you linearize effectively?
My understanding is that they think that we can always optimally sort clusters of 15 to 20 transactions.
And we might want to generally limit to, we will have to generally limit how many transactions are allowed to be related at once, because it'll become too expensive otherwise to linearize them.
We're thinking 64 transaction clusters will probably be fine.
This is somewhat in line with the 25 descendant limit that we currently use.
So currently, a transaction cannot have more than 24 descending transactions, and, or that's at least the standardness rules per which the Bitcoin core nodes are configured by default.
All right, so, if you were in the Socratic village yesterday, we talked a little bit about modern mempool stuff, and Gloria actually had an example of a really complicated cluster with 490 transactions.
So my colleague Claire and I, we did some block building research a couple of years ago.
And we found some really, really horrible clusters in that data.
So 64 is a limit that will be hit, but probably not by most users.
Most users create a single transaction.
Maybe they'll spend an unconfirmed output once or twice or do a CPFP, and then they'll have a cluster of two or maybe three transactions.
If you get to 490 something transactions in a cluster, you're probably doing something that you should rethink.
All right, so we have linearized our clusters.
We know in which order the transactions have been, will be picked into the block.
I'll not go into more detail on how we linearize them.
Check out Delving, Peter's literally written a book on it.
All right, Let's look at that third more complicated cluster, and I'll introduce some, a way of thinking about the cluster in terms of its size and fee rate.
So we call this a fee rate diagram and where at the bottom you see the total weight, the transactions are all each weight one right here, so that's easy.
And on the y-axis you see the absolute fee, the sum of fees in the cluster up to that point.
And now we found the order of the, here, cool.
So I hope you believe that this is a good linearization for that cluster.
But now if we draw it on the first transaction, f, we'll collect three sets on the first weight unit.
And then we'll collect nine sets on J to the point where we have two weight units.
So if we pick those two together, that'll be six sets per V byte, and We'll just have, we can represent this package as a single line together, which actually is nicer than just looking at the first transaction.
The first transaction would indicate that we only get three sets per byte for each weight unit there, but now we get six, right?
We can do the same thing for the second segment here.
We are basically creating this convex hull over this V-rate diagram.
And once we have done this, we end up seeing what we would like to pick into the block together.
So we have chunked f and j together into a single package.
We have chunked g, h, and I together in a single package, and k has a terrible fee rate and is all by itself in the last chunk, k, right?
So even though we now had originally six transactions in our cluster, the way it will be picked into the block will actually only be three chunks.
Cool?
All right.
So we've linearized our cluster, We've chunked the linearization into packages that will be picked into the block together and have calculated their fee rates.
And you might notice now, If we pick f and j together into the block, they will be picked at a fee rate of six SATs per V byte.
And the fee rate of gh and I will not change because it's already not the ancestor set that we're calculating, we're calculating with the chunk.
GH and I, and the fee rate doesn't change.
It's exactly the fee rate that we have pre-computed that is left once we have picked F and J, right?
It's still 4.3, well, 13 thirds that we'll get out of that package.
So, by linearizing and chunking, we get a recipe in which order we should consume a cluster, and we don't have to recalculate anything if we just consume it from the front to the back.
And because we considered the topological dependencies while building the linearization, as long as we pick from the front, we'll always get the highest fee rate first.
And all the topological requirements will also be adhered to.
All right, let's cluster all of the chunks.
So we get a single chunk out of A and B, which has eight sets per V byte and a weight of two.
We get C and E as a chunk, D as a separate chunk.
We get F, J, G, H, I, and K.
So now our, what is it, 15, No, sorry.
11 transactions become six chunks, right?
And now, if we were to build a block, does anyone have a good idea how we would go about that?
Well, we have to, yeah, go ahead.
Right?
So we walk each cluster from the front, pick the highest fee rate chunk, and then just sort of remember which chunks we've picked.
So our total order for those clusters would be the first chunk from the first cluster, the first chunk from the second cluster, or the first chunk from the third cluster.
They have an equivalent feed rate.
Sorry, I should have built a better example.
And then the second cluster from the third, the second chunk from the second cluster, and finally the third chunk from the third cluster.
So what do we have now?
We have a total order on all transactions in the mempool.
We'd get that by just finding what transactions are related and ordering those transactions independently in the context of their relatives.
We can blazingly fast pick the block template because we basically are doing a merge sort.
We're just looking at each cluster from the front and we pick from each cluster until we have a full block.
And eviction is the opposite of mining.
Because to evict, we look at our clusters and go from the back and kick out the chunk with the lowest free reign.
So out of our mempool, we kick out k, then we kick out d, and then we would kick out ghi.
But we no longer kick out the first thing that we wouldn't mind, which is f.
Cool, So I'm maybe a little faster than I thought, so I have lots of time for your questions.
There are a couple caveats.
First, we'll need a cluster limit that so far hasn't existed.
The cluster limit will be a lot smaller than current cluster or than the worst-case clusters we've seen in our research.
But it'll probably be reasonably big for anything reasonable people are doing on the network.
We can probably not optimally sort all the clusters because big clusters, A linearization is basically a power set that grows exponentially.
The computational effort for sorting, it grows exponentially in the size of the cluster.
So probably to 15 or maybe, yeah, about 15, we can ultimately sort maybe 20 transactions.
And above that, we'll use something simpler, like ancestor set sort on a cluster in order.
We sort of run this mini mining algorithm on a cluster with ancestor sort, the same strategy that we have.
And then we get a decent linearization that's at least as good as we would have been doing before.
And then if we have time, our computer maybe in the background can crunch more optimal cluster linearizations.
And then when we build the next block template, we might be able to just have optimally linearized clusters to pick from.
One thing that is a little annoying is it might be less obvious to end user wallets exactly what they need to do to get a transaction through at exactly the right fee rate.
But I think that will be fine because I think most end users just gauge it and then bump if it's not enough.
So that will still work.
Yeah.
So I have 15 minutes for your questions.
All right, here, question up front?

Speaker 1: 00:25:27

Here we go, raise your hand high if you have a question, I will bring a mic to you.

Speaker 0: 00:25:39

Maybe I missed this part, but how do you figure out what goes in the chunks?
Let me explain that better maybe.
Okay, so we, I'm sort of mixing it a little bit, but if you first look at the cluster as being only topologically sorted, it might not be the order in which you would pick it into the block.
So what you, on an abstract level, do is you run a mining, like a block template building algorithm, on just the cluster.
Similar to the mini-miner in Bitcoin Core, if someone's followed the Bumfee calculation PRs from last year, how we calculate Bumfees for more complex packages.
And you basically, you just look at the whole cluster.
Out of this cluster, what would I pick first into the block?
What's left?
What would I pick then?
And so forth.
And you basically, you make that your linearization.
Now, Peter would probably make quite the face because he's spent a lot more time, so there's rules on how you can shift transactions against each other to improve the linearization, how you would calculate the linearization in the first place and all that.
But I don't want to get into all those details.
But if you assume you get the optimal order of the transactions in the cluster, and then you draw them in the fee rate diagram like this, you can basically draw the convex hull over this fee rate diagram, And it will indicate what the chunks are.
On a less abstract way, whenever you have transactions that have higher fee rates following transactions that have lower fee rates, they will form a chunk.
But for example, you will not get a child pays for parents situation if you have multiple children, but you will get a children pay for parents situation.
If they both bump the parent, you will discover that they will form a chunk together, unless one of them bumps it to a higher free rate than the other child by itself.
Thanks.
Cool?
All right, another question here?

Speaker 2: 00:27:58

So I was curious how this, I guess, CPFP carve out, there's a wrench in this, and long-term adoption, if it becomes easier for miners to identify lightning channels on chain.

Speaker 0: 00:28:16

Yes, okay, so cluster mempool is incompatible with the CPFP carve out because you basically would have to allow a transaction to attach to any ancestor in the cluster.
And it wouldn't be clear what you would do if a second one came in or...
So the answer to that is truck transactions actually.
We will have hopefully the Lightning developers opt into restricting the topologies for the transaction to just packages of two, a parent and a child.
And then you don't need a CPFP carve out because the package is limited to two.
If you create another transaction that spends from the parent transaction, it'll sibling evict the first child and just keep the child with the higher fee rate.
So either of the two parties will always be able to bump the parent, And the only way to bump the parent is by incentivizing the parent with a higher fee.
So maybe lightning channels will look more obvious because they might use v3 transactions at that point.
But v3 transactions will also be useful for other things, for other L2 proposals maybe.
I think ARC needs more than two transactions potentially, but there's several other contracting protocols, layer two protocols, where packages of two transactions would be feasible.
Also, so earlier I said that RBF rules, as we have them right now, are not always gonna create the most incentive compatible outcome.
So we might accept sometimes a replacement that actually doesn't lead to a better block template, or not accept a replacement that would lead to a better outcome.
But with the fee rate diagram, actually, it becomes much easier to compare replacements.
You might not have, or recently we got the opportunistic 1P1C package relay merged into Bitcoin Core that was released in 28.
And this package relay already allows also replace, or in conjunction with that, we also got package replacement for truck transactions and other two packages of two transaction replacements.
So we already used the fee rate diagram comparison there to see, like, we just draw these two.
Sorry, I don't have an example with me right here.
But you draw basically the two fee rate diagrams of the original and the replacement.
And if the fee rate diagram of the replacement is the same or higher in every point of the chart, then you accept the replacement.
And that's always gonna be better.
So, we'll be able to hopefully extend that towards bigger packages because the cluster mempool proposal will make it much easier to reason about bigger packages.
And then hopefully, v3 transactions won't stick out as much.
V3 transactions could potentially even be extended to slightly bigger packages.
Now Gloria's not gonna kill me.
Okay, good.
So yeah, the idea is with cluster mempool it'll get so much easier to reason about all this that we'll hopefully be able to do package replacements more easily and we'll have less of these restrictions that make things stick out.
Did I cover all of your questions?
Cool.
Next question, here.

Speaker 3: 00:32:08

You said that linearization of clustering is computationally expensive.
What makes this still worth it for that trade-off?

Speaker 0: 00:32:20

Uh-huh, right.
So, theoretically, it would be enough to just topologically sort transactions in a cluster.
You'd already have a valid linearization, right?
You just need any order in which you can validly pick transactions into the block.
But, you do want to be at least as good as our previous approach, which is ancestor set based.
So the first thing we'll do is we'll sort each cluster by the ancestor set scores.
And we can do that already today, so it's not more expensive.
And after that, we can even make delinearization better.
Discover, for example, children pays for parent or descendants pay for ancestor situations, whereas staff chunks better together, and you get chunks with higher fee rates.
So why is this worth it?
A, you can sort of pre-compute all of that before you're actually doing the block template building.
So it doesn't slow down the block template when you just quickly want a new template.
Block was found, you immediately want to be able to instruct your miners to mine on a new template.
At that point, it's very cheap because you just use the currently pre-computed clusters.
So you can use computational resources where you don't urgently use them for other things and you get this total order on the mempool, which allows you to look at every transaction in the mempool and say at what fee rate, what the mining score will be, what the chunk fee rate is that will pick it into the block.
This makes it easier to bump transactions.
This makes it easier to evaluate RBF.
This makes it easier to estimate when transactions are going to be picked into blocks, and all without building a mega block out of the whole mempool.
Cool?
All right.
Another question here?

Speaker 4: 00:34:16

I had one as well.
If you're not creating block templates as a miner and you're just a normal node on the network and say your mempool is getting full, would this algorithm also determine what transactions you're gonna purge from your mempool?

Speaker 0: 00:34:32

Yes.
So the big benefit of cluster mempool, one of the design goals really, is eviction becomes the opposite of block building.
And as long as you have a reasonably good linearization, the things that you will evict from your mempool are either, if you had an optimal sort, really the last things that you would pick into the block out of all the things that you know about, or at least very far in the back.
So generally it should do better on the outcomes of eviction than our current mempool.
And if you have a less computationally powerful device, it'll probably have fewer optimal clusters, but it'll still have pretty decent clusters all around.
So at least there will be ancestors that's sorted.
And you still get this benefit where you look at the clusters from the, yeah, I think this was it, Where you can look at each cluster, and the candidate for the eviction is the last chunk in one of the clusters.
And you just have to compare all the last chunks in all of the clusters and kick out the one.
So You could have, for example, a heap on that, and you always know which transaction or which chunk is up for eviction next.

Speaker 5: 00:35:56

Perhaps we're looking at it, but it's a little hard to tell.
Can you come up with an example where the descendent set score gives a worse incentive compatible outcome than the linearization?

Speaker 0: 00:36:13

Uh-huh, yes.
So, here, let's look at this again, right?
If you look at this cluster, what ancestor set would you pick into the block first?

Speaker 5: 00:36:29

JNF.

Speaker 0: 00:36:31

Correct, they have a ancestor set fee rate of six, and that's the highest here in this set, right?
But if you look at each of the descendant set scores, so currently the mempool has these two indexes, right?
It's a multi-index data structure.
The ancestor set scores for each transaction, the descendent set score.
And we look at the descendent set score, the lowest descendent set score, as the heuristic to kick out something, right?
So what we found in the final slide was we'll kick out g, h, I first and keep f and j, right?
And here, the lowest descendent set fee rate is the one of F.
F has a descendent set fee rate of five.
G, H, I, or sorry, I should say, I has 11, G and H each have six, which is higher than F.
J has nine.
So the first thing you would evict is also the thing that you would mine out of this cluster.

Speaker 5: 00:37:36

Okay, thank you.

Speaker 6: 00:37:40

All right, so we're trying to compute the mining rate, the mining score, right?
And does cluster mempool compute it exactly, or does it fall short somewhere?

Speaker 0: 00:37:53

Uh-huh, very good question.
So, it will compute it exactly if you have the optimal order.
If you have not optimally ordered some of the clusters, the mining scores, or sorry, the chunk fee rates might not exactly match the mining scores in the end.
But Generally, they should be a lot closer because previously, we were looking at the ancestor set score for each transaction in that context.
And that changes all the time as more ancestors are picked into blocks.
We always have to recalculate it.
So we actually do not get any information on the final mining score.
The fee rate that a transaction actually will get into the block with the old mempool.
And here, we at least get a very close guess, even if the clusters are not optimally sorted.
Does that cover your question?

Speaker 6: 00:38:51

Is it hard to optimally order the clusters?
It seems easy at first glance, you know?

Speaker 0: 00:38:58

Yes, so for small clusters, it's pretty easy.
We will definitely be able to optimally order clusters of up to 15 transactions, maybe even 20.
But if you look at a cluster with like 60 transactions, a bunch of diamond structures, tons of ancestors, descendants that are all interconnected in some ways, it can become fairly complicated.
So Peter's been doing a ton of fuzz testing on this and he's found some very complicated examples where the number of calculations that you have to do just exceed the computation time that we want to allocate.
And that start, like the worst clusters of like 25 are out of the range of what we want to initially allocate.
But the cool thing is we can have sort of this, we can sort of have a lazy evaluation where we just keep a topological sort slash ancestor set sort of the cluster.
And if we have time, we can optimally linearize it with just biting the bullet and calculating the complicated cluster.

Speaker 6: 00:40:17

So the algorithm kind of has a timeout built in.
When we hit the timeout, there's a fallback heuristic that will not yield the optimal solution, but it will get close.
And so this is where cluster mempool falls short of computing the mining score.

Speaker 0: 00:40:35

I think that matches my understanding.
Again, I want to say I'm not one of the leaders on this project and I hope I'm not misrepresenting, but My understanding is everything is at least going to be as good as ancestor scores, which we currently use, and then hopefully a lot of the clusters.
I think most, maybe over 90% of all transactions are single transaction clusters.
Most other clusters are pretty small, and it's only very occasional that we get these huge sprawling clusters.
So for the most part, all of the mempool will be optimally sorted with the occasional cluster in there that is not.

Speaker 6: 00:41:15

Cool, thanks.

Speaker 3: 00:41:18

Do all your examples assume the same number of vbytes for the transaction and does this take into account the size of the cluster?

Speaker 0: 00:41:31

That's a fair question.
All my examples are simple and have transactions of the same weight.
Peter, in his write-ups in Suhas, they both have more complicated examples in there.
I would encourage you to take a look at delvingbitcoin.org.
The Cluster Mempool Working Group tag will find you a few articles where they've laid out in a lot of detail their approach to linearization, terminology about cluster mempool, some of which I've introduced, and more complicated example where it becomes hard to find the optimal cluster, how they go about that.
Yeah, so, sorry, yes, I only have very simple examples.
If you want, I can pull up some later from their blog posts, and we can talk about them offline.

Speaker 1: 00:42:25

All right, big round of applause, everybody.

Speaker 0: 00:42:27

Thank you.
Thank you.
Thank you.
