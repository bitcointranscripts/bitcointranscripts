---
title: Efficient P2P Transaction Relay
transcript_by: Bryan Bishop
tags:
  - erlay
speakers:
  - Gleb Naumenko
  - Pieter Wuille
date: 2018-10-08
aliases:
  - /bitcoin-core-dev-tech/2018-10-08-efficient-p2p-transaction-relay/
---
## p2p transaction relay protocol improvements with set reconciliation

gleb

I don't know if I need to motivate this problem. I presented a work in progress session at Scaling. The cost of relaying transactions or announcing a transaction in a network-- how many announcements do you have? Every link has an announcement in either direction right now, and then there's the number of nodes multiplied by the number of connections per node.  This is like 8 connections on average. If there are more transactions then this situation gets worse. Ideally, we want to have a number of nodes without that multiplier..

The observation is that every node needs to learn about each transaction only once, but right now it learns about each transaction once per connection it has. It's not fair to say that every node wants to hear the transaction only once, because it's also good to sync your state with other peers so you still want to get that information that your peer knows about the transaction. It also makes compact block relay actually work. Not just you want to learn about every transaction once, but learn about every transaction once within a reasonable timeframe. Also, you want to make sure your peers hear the transaction too. We want the cost to be equal to the number of nodes; we want to talk to each peer and make sure they know all the transactions being made. We still want every node to hear each message at least once.

Right now this scales poorly; the number of messages in the network goes up and to the right with the number of messages. The protocol that we would like to build would be a slower slope.  It's a discontinuous exponential graph so that's why the horizontal axis changes here.  The x-axis is not linear in that graph. We want the bandwidth scalability with the number of nodes and increasing messages to grow acceptably.

Protocol design, metrics to consider: bandwidth, latency (propagation delay for propagation to 100% of the nodes) and robustness to adversarial behavior. We don't want to leak a lot of information. This is always about trade-offs.

The efficient transaction relay protocol is that you relay a transaction to a subset of your peers, and the next node does the same. It then grows through a big chunk of the network. Other nodes do reconciliation based on a certain period or some other schedule and learn about the transactions in a more efficient way than just sending all the announcements they have.

So to do this, you do transaction reconciliation.  Every node maintains a set of transactions it would have sent to every peer. Assume that node B chooses some other peer in the network to relay a transaction and not C, we only relay to some subset of peers. B relays to somewhere else. Node B stores this list for every peer that it would have announced a transaction to, but did not. We received the message from A, so we don't store that. But for node D, normally we would have announced to that node. For now we can think about storing just the transaction hash, but actually we're storing it in a different data structure. After node D learns about another transaction and announces it somewhere else in the network, then records it in this set for peer B. Node D also has a set for A and C but it doesn't matter in this example. Node B has some timer to reconcile with each peer. The timer says, consult with node D. And then they exchange some information based on this set so that node D and node B learn which transactions they are missing. The simplest way to do this is to send sets to each other and that's just batching, but it's not efficient. After reconciliation, the memory sets are cleared for that peer that reconciliation occurred on. This is obviously not the inv, getdata, tx protocol. When B finishes reconciliation with D, it may or may not do announcement to its peers. That's not clear yet. It's still being measured.

In dandelion, there's a stem phase. Dandelion is strictly about sending to one peer only. This is about efficient propagation which is exactly what dandelion is not trying to do. Yes, this is replacing the ploomb phase for dandelion.

Once you reconcile, the decision about what to do is not clear. There's a tradeoff between bandwidth for announcements, how much time you want to wait for transaction relay, and so on. The question is, should node B relay the new transactions? If it does, it will make latency lower, but it's probably the case that some of its peers already knew about it. Reconciliation is slower than flooding. That's why there's a high probability that node B will choose a peer which already knows about this transaction. Putting it in another way, if we use normal relay with sending to 3 peers each, so you have a branching factor of 3, this has a high probability of reaching nearly every node in the network already. So in theory, one is enough. If you manage to form a cycle that reaches everyone, it's very unlikely. If you pick 2 or 3, you're going to reach nearly everyone- only when peers go offline or there's some highly unprobable cycle. The reconciliation is just to make sure that the ones that haven't heard about it through the normal protocol are still guaranteed to learn about it. Ideally, hardly any bandwidth goes into reconciliation because we assume the normal mechanism has reached almost everyone. There are many parameters to look at.

Q: If you learn something new through set reconciliation, then doens't that change the a priori likelihood of other nodes knowing about the transaction? Probably not many other nodes know about it yet if you don't.

After reconciliation, the nodes clear their sets and start over. During set reconciliation, there's two round trips.

## Finding set differences with BCH codes

We use BCH codes to make this efficient. Say Alice has 7 transactions in their set, and Bob has 7 transactions in their set, and they have no idea which ones are shared and which are not. They assume most of them are shared. Every five seconds, a node picks a peer from a queue. So basically, which means, if you have 8 peers, then every reconciliation happens on average every 40 seconds because it's 5 * 8. During that time, we learned a lot from other peers and so on.

Q: Have you considered doing anything... you're currnetly syncing the whole mempool every time?

A: No. You're reconciling the set of transactions you would have relayed since the previous reconciliation.

Every 40 seconds, this set gets empty, and then you fill it up again with new transactions. This is why it's fair to assume that most of the set elements are shared between the two nodes already. Once they learn about transactions that they mutually don't know about, then they do reconciliations. It's possible to make this happen by-- if a transaction ID is 32 bytes, it's enough to send just....... Alice estimates diff set size, Alice computes a summary of her set, Alice sends the summary to Bob, Bob computes his summary, Bob XORs the summaries, Bob can then find transactions that he is missing. If Alice underestimated and sent a summary of size 1, Bob will fail to do the last step because underestimation... yeah he just can't recover, and he will observe the failure and request another iteration of the protocol or something. If Alice overestimated and sent 3 elements, that's fine, there's just a bit of extra bandwidth because it's not optimal anywhere.

## Simulation results

Right now this is what I'm observing. This is with 10,000 nodes. We need to reduce redundancy in initial fan-out. Also some of this is due to reconciliation failures (underestimations). Half of the nodes never hear about transactions, and half hear about the same transactions twice or more. Underestimation is when set reconciliation failed and we need to send more data across the network. In the event of a set reconciliation failure, Alice can fall back to the original protocol and send the full thing.

If nodes go offline and cycles form, even without any other things, there will be nodes that don't learn about certain things.

Q: Are you modeling nodes dropping offline?

A: No.

If your graph is connected and you have initial relay to 3 peers, then I assume the whole network gets everything. A very small percentage wont get all the transactions, without reconciliation that is. It's because cycles form. I was simulating with 20% outgoing connections, you broadcast to 1/5th of the incoming connections. Most of the nodes have 60 incoming connections in my simulation. Currently in the network there's a ratio of 1 to 10 for 1 reachable node to 10 private nodes. Each one has 8 outgoing connections, so a reachable node has 60 incoming connections on average. That's how it is right now on mainnet. There's some distribution because some olds are node and some reachable nodes are new. You just have two classes of nodes.

Q: You simulate delays in propagation?

A: Yes.

There is a nice property of this set reconciliation using BCH codes.

Every element gets expanded into this sketch of a certain size that you estimate, then you XOR all the sketches together of the different elements, then you cancel them out across-- both sides compute the XORs of their sketches, then you XOR them together, then the ones that occur on both sides get canceled out. There's an algorithm (without going into details of what a sketch is) where if there are fewer elements in the sketch after canceling out, then the size of the sketch, you can find them.

If this is your number of things you want to reconcile, but there are too many of them to match the other side, the XOR of all of them I guess, if this has too many differences, I can retry by sending the XOR of just the first half and you can compute the sketch of the second half by taking what I sent you before and XORing it with what I had sent now. So you send the whole thing, and if it's not enough, you send the first half, and the other side recomputes the second half and now they can do reconciliation separately on the first half and the second half. You can also recurse again, I don't know how many iterations deep you want to go... But this is pretty neat because if you do this iteratively and with small overshoots, you're never going to have too much or not much too much. It reduces the cost of failure in the first iteration. Your peer is bisecting the set in the same way. The alternative is I give you a bigger sketch and this works, you can reuse the first part of-- a sketch that has higher capacity is just one for a lower capacity extended with some more data. If I send you one that can reconstruct 100 elements and it's not enough, you can also send here are the next 100 elements for the sketch and now you hav esomething that can reconstruct 200. The reconstruction algorithm is quadratic in the difference. But this has linear CPU cost rather than quadratic. I can also go into the actual construction of the sketches if there's interest.

We can bisect on these too. The bisection is on the id, not on an ordered list. If you use the ids and their salts and short hashes, salted by-- chosen by the peer... it's per-connection based, or per node. One node, all of its connections use the same salt. You need to have the same salt as the other side, but it's one side that chooses the salt.

We use short ids of transactions for two reasons. We can reduce bandwidth dramatically by using short ids for announcements, and the collision rate is fairly low, and we can survive a certain collision rate. This construction can work with short ids. The CPU cost goes up dramatically if you make the ids bigger, I think cubic or something. I think the ids are 20, 30, 40 bits. They are very small amounts of data. You're talking about the transactions that would have been relayed in the frame of a couple minutes, so you can do pretty short things.

Collisions may be bad in that a transaction may stuck... the same transaction with the same short id on both sides, and reconciliation might think they are the same. This is a porblem. If you salt every connection with a different salt, then that's fine. If they are the same short id, then the transaction wont propagate to the other node. It is not a problem if there's collisions just within the transactions you're trying to relay; it's only when there's a different transaction on both sides that collides. You having two transactions with the same short id, you just send the transaction. You don't need to resalt, you can just send, because you're missing that.

## Some benchmarks of BCH libraries

BCH codes are fairly expensive without optimization. IBLT is another set reconciliation method. IBLT is much simpler to implement, and computationally it's better than BCH codes, but for small sets it has a pretty high overhead from small integers. Not 10% overhead, but 3x overhead. This is information theoretically extremely close: if you can accurately predict the difference, then the bandwidth is only the difference, which is pretty amazing.

BCH code libraries-- you can compute 50 differences in 4.48 ms, this is computed every 5 seconds on every node running the protocol in my simulation. On a Kaby Lake processor, it's 0.3 ms for 50 elements. 150 elements is 26.91 ms on an ARM iMX.6, and 2.1 ms on the Kaby Lake i7-7820HQ processor.

The construction of the sketch is virtually free, it's extremely fast. Given a sketch, try to find the elements in it, that's expensive. The protocol is designed to make the one who requests the reconciliation to do all the work. That's 5 seconds with 1 peer, and if you have 8 peers then it's 40 seconds. The number of differences is over a 40 second window or more, if you have more peers. If the CPU cost of the scheme was lower, then we would pick bigger... it doesn't scale linearly if you make-- if you increase the time between events, the number of differences is not going to keep going up linearly. Can you tune your node to request less often, and then your peers do the work? ((laughter))

That may not be true. Some of my measurements, that's not confirmed. There's asymmetry in nodes. Private nodes always learn more than reachable nodes. Reachable nodes has 60 connections and if every link is on average reconciling once every 40 second, then every reachable node you reconcile with someone 2 times per second. So there will be collisions in the reachable nodes receiving.. even in set reconciliation, they will receive the same announcement a few times. So that's why I'm trying to not send announcements back sometimes. I'm trying both ways. Probably it's better to request your data for what you're missing and that's it; I'm looking into that.

Are the short ids based on the wtxid? Haven't really thought about it. Yes, I guess. Use wtxids. What if you malleate the wtxid? If two nodes have different versions of the same transaction, then they are not going to accept another version of it already anyway. That's how things work now, right? So, if you have the same txid but different wtxid, then the reconciliation will not do anything. Because it wont help you reconcile. You would try to reconcile, but... you could avoid all that by just sending the txid. If you have a malleated version that you rejected earlier, then I don't know-- we should look at the rejection stuff again. We don't have good data. Nothing is getting rejected for too low fee right now, so we don't have good data on the reject filter being used. We don't get the benefit of the reject filter, because we're not rejecting anything for too low fee, so we don't have data. Right now we have 8x cost on segwit transactions that are below the.. whatever.. Even in the absence of malleation, we're not using the reject filter for segwit transactions. So we don't know what bandwidth it is. The fee filter is designed to protect against this without the reject filter.. the fee filter should go up. But if it's not in the reject pool, then compact blocks wont use it. Oh.

Combined with short IDs, this set reconciliation method uses up to 44x less bandwidth. I'd like to have more reviewers or more people testing with my simulator or writing their own simulators.

<https://github.com/naumenkogs/Bitcoin-Simulator>

Should we announce transactions to reconcile? I want to get the protocol gets closer to the ideal case. I'm considering writing up a prototype for Bitcoin Core. I have some ideas. I wanted to run a network of 100 nodes. Is it a good idea ot do a million nodes? Or is running 100 nodes on a single computer bad?

I would not suggest running that many nodes on one machine. No, I want to run 100 real nodes. On regtest it will be fine. Everyone has 64 gigabytes of RAM, right?

Once sipa posts something about BCH codes, then we will publish transaction relay stuff. First we should get everyone to write up how they think it works, then we do a reconciliation between them. Or we could do a BCH code thing right now and then publish whatever kanzure types.

## Sketch reconciliation

sipa

There's really two ways of explaining it. One is as a BCH code. BCH code is an error correction code that some people may know something about, now that we have an address format that uses it. Say we're working with 20 bit short IDs. We need a hash function that never produces 0 as an output; if it's 0 then turn it into 1 instead. We can do better. We treat the short IDs as field elements in a characteristic field. We can multiply them together, we can solve sets of equations over them, we can add them together, all those things. One way of looking at it is that... you can think of it as a code where your code words are in fact 2^20 bits long. Every set element is a code word with all 0s and ... so our hash is, we're remarkably lucky, in this example it's a low number, like 4700000.. and we can find an error correcting code over this construction which is something you can do in a variety of standard ways. This solves the problem because we take... the error correcting codes are linear, which means-- I add a checksum to it, with some properites we will define later. The important property is that these are linear. For every element, I compute my sketch, which is my code words, I compute the checksum for it, I XOR them. I have a checksum and a word with a number of 1s in it. If the number of 1s in this set is less than 7, then whatever. And my code is designed to correct 7 errors. You do an error correction assuming everything before it is 0, and now you find the error positions and it will tell you which ones were wrong. This is an intuitive explanation, but there's a number of optimizations to make this efficient.

The size of the checksum is related to how many errors you want to be able to correct. This is both for correction and detection. Under normal circumstances, you need a distance to encode... Our goal is to correct errors, not just detection. Due to the fact that if our base field is just 0s and 1s, we don't care about learning about the errors if we know their positions that's enough because if a bit is wrong then it's always wrong by 1. Once I talk about the other formulation, you will see the normal rule of needing 2x as many elements in your checksum for correcting your errors doesn't apply because information theoretically the reason you need those 2n is because you need to learn both the positions and the errors.

Q: Does it matter what field you use? Is it just a binary code?

A: It has to be a characteristic 2 field, otherwise you immediately get a factor 2 blow-up.

So that's a description of where BCH codes come from. I am going to start over, and we'll get to another point of view to get back to that.

## Sketches

If my elements are x, y and z, then the sketch consists of x+y+z, which is really the XOR of the bits. That's the first element of the sketch. The second one is x^3 + y^3 + z^3... and the next one is x^5 + y^5 + z^5. They must all be raised to these powers.. The first step when doing correction.... you see that, I have... If you need 10, then you go up to x^19 and clearly this has linearity properties. If I have a sketch for x, y and z, and I xor them together, then I have one that has added them up so I'll get an output sketch. ... Square root is a linear transformation, you can derive all sorts of funny properties from this. If you have x + y + z, you can compute x^2 + y^2 + z^2 because it's just squaring this number. For the sum of the 4th powers, you compute the squaring the numbers for the second powers. And 6th, you do ti for the third powers. So what I'm getting at is that even though you are only sending the odd numbers, the receiver can really compute it for all. This is specific to using a characteristic 2 field. If you weren't doing that, you would need to give all the intermediates.

The mathematical objects is field elements, and we're talking about addition over field elements. If the field elements are bits over an integer, then XOR represents the addition of the bits over the integer. Multiplication is far harder. All of the code optimization is about making multiplication fast.

If I'm given a whole number of elements, how do I find what x, y and z are? These are not simple linear equations or operations. Say there's only one element in our set, like x, so after the expansion of our squares we have this sequence of x, x^2, x^3, x^4, x^5... Ignoring that x is just there, you can find x by taking the ratio of the elements. There's a recursion relation that holds over this sequence. The relation is... if you take any two elements and apply this multiplication to it... any two subsequent elements in this sequence, I can apply this linear transformation to it and I will get zero. So this is a recursion relation, element multiplied by x plus one times the next element which holds for every element in this sequence.

What's also true is that, if you see this recursion relation as a polynomial, then multiplying this linear transformation by anything else will also map it to zero. Any two elements I apply this transformation to, maps it to zero. If I multiply that result with anything else, it remains zero. So the set of all linear transformations that map subsequent elements to zero, are all multiples of this polynomial here (x-1)... these are the coefficients of the polynomial. If I do the same with y, y^2, y^3, y^4, etc., obviously my relation is now (y, -1). This is going to hold. The observation is that if you XOR these together, the relation that will hold is in fact (x-1) * (y-1) where you multiply by (y-1). Any relation that was true for both this sequence and this sequence, will remain true after you add them up. If you find the common factors in these linear transformations and write those together, that will be something that holds for the sum. I'm jumping ahead here, I guess.

This linear relation holds for the sequence of y, y^2, y^3, etc., because they would add up to zero. And (x, -1) linear transformation holds for this other one. So (x, -1) * (y, -1) is the same as-- you multiply them as polynomials. So you agree that this relation will inevitably hold for this sequence and this sequence. It's a linear transformation. Adds these two up, and this transformation holds for the sum. I'ts not necessarily the simplest that holds for the sum, but it's guaranteed.

What I'm getting at here is that if we were to be able to find from the sequence of numbers, the relation that holds between them, and then find and factor this, we would find the x and y values. Turns out there's an algorithm for doing this, called Burlycam Massy. It gives you the simplest linear relation that holds for all the elements. It's the basis for Reed-Solomon codes and BCH codes, and that's where this comes in. The stuff is, you take your sums of powers, you expand it using an endomorphism to get the even powers, you use Burlycam Massy to get the linear transformation that holds for all the elements, then you find the roots for this polynomial and those roots for the polynomial are your numbers x and y and z. And then all the complexity is in making that computationally fast.

I can also explain how to find roots.

If you don't have a characteristic 2 field, then you can't use the the endomorphism to compute the sum of the powers from the others..

Q: Is this a BCH code? What are the parameters of the code? How would you describe it succinctly?

A: It's not actually a BCH code, it's just very similar to it. You would call it one where the... the relation is just ordering the elements, but it matters for efficiency. It is a BCH code where the size of the base field is 2, the size of the extension field you're using is the size of your elements-- no, wait, that's not right.

Q: You could imagine a code where the field you're using doesn't matter at all. It could be a field of 2^n.

A: The length of the code is 2^20. The extension field is just the number of elements you're currently.... It's a good question.

Q: Here's a dumb way of looking at this. Think about hamming codes.

A: Hamming codes are not very long. You can make them longer, I guess. That's a good question.

Why do you want to do correction and not detection? If you detect an error, then you want to get it again right? The goal is not for addresses here. This is set reconciliation for transactions. It's using a BCH code like bech32, but it's for another purpose.
