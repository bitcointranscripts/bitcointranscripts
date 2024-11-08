---
title: Concurrency And Privacy With Payment Channel Networks
transcript_by: Bryan Bishop
tags:
  - research
  - lightning
speakers:
  - Pedro Moreno-Sanchez
---
paper: <https://eprint.iacr.org/2017/820.pdf>

## Introduction

I am going to talk about concurrency and privacy. This was joint work with my collaborators.

Bitcoin has scalability issues. That's the main reason why we are here today. Currently the bitcoin network allows for less than 10 transactions/second. Today we have more than 135 gigabytes of memory requirement. And there are some high fees and micropayments are not really possible. One of the proposals to fix this is payment channels.

## Payment channels

For those wo don't know how payment channels work, it allows payments between two users, without putting every payment in the blockchain. In the figure, Alice creates a payment channel with Bob. They will create a deposit with Bob because it's not a network. Alice and Bob might not trust each other. They use a contract that allows the originals to receive their coins back after a certain amount of time. This is called the opening of the channel. Once it's open, they can sign transactions to each other. Once they finish, they can close the channel and send the transactions that go to the network. They get the coins in the channel from the last state they agreed upon. This requires one transaction to open and one to close.

Instead of having a payment channel between every two users, you can use a network of channels. You can use some of the other nodes in the network as an intermediary such that payments are forwarded. In this example, Bob (the intermediary) has to be trusted. We need something that allows us to create multi-hop payment without trusted intermedaries. As for this example, to save time, I will just call it a multi-hop payment.

## Hash time-lock contracts (HTLCs)

In order to have this payment network, we use hash time-lock contracts. You allow conditional payments between users even if they might not trust each other. So Alice is going to pay Bob 1 bitcoin under the condition that Bob shows a value H(x) such that it satisfies the condition. So he has to show this value x and send it to the bitcoin network, and thus show that the one coin that was conditionally paid by Alice.

HTLCs have been proposed for the lightning network to build a multi-hop payment network. Bob will forward the payment with the same condition 'y'. He knows that as soon as 'x' is revealed for the conditional payment with Cat, he can use it to pull coins from Alice. And once this multi-hop payment is settled, Cat can just open this value x, pull the money from Bob, and now Bob takes this x and gets the coins from Alice. These hashed time-lock contracts ensure that it works.

Our contribution is that we are looking at payment channel networks and analyze the privacy and security aspects. We study the issue of concurrency in payment channels.

## Security properties

We considered two security properites. One is called balance security. The main idea is that a payment channel network must ensure that every honest node in the path from a sneder to receiver must not lose coins. If delta here is the balance of the channels that the users have, it must not be the case that the balance changes after the payment because he was an intermediary. The other property is serializability. They must be sequential payments. These two consecutive payments should have the same serialization.

## Privacy properties

From the privacy point of view, we considered two privacy properties. The first one is that off-path value privacy. If someone was not participating in the path, then it means that... if the attacker was in the path, then they know how much was routed in the payment. Anothe rproperty we are after is that on-path relationship anonymity. If the attacker is in the path, then they should not be able to figure out which actual sender sent the payment. So now we have a set of senders, a set of receivers, all of them are spending, you should not be able to figur eout which ones are paying to which.


## Privacy in PCNs

All of the payments happen off-chain. What are the privacy issues then? The problem is that if you have these conditional payments, you can use the same conditions on each of the hops. By looking at the condition, you can figure out which channels are being used. In light of this problem, we are trying to propose a solution to solve this problem.  Our solution is Fulgor: based on multi-hop HTLC method. We want to have standard hash time-lock contract, and take all of the other cryptographic operations and they must be off-chain. We are fully compatible with the current Bitcoin script.

The solution we propose is Fulgor. It's multi-hop HTLCs.

## Multi-hop HTLCs

We use a building block called non-interactive zero knowledge (ZKBoo [GMO16]). There are two things-- x0 and x1 and y0 and y1. The privacy you get is that the.. two values are the same. For anybody else these look like two random numbers being used for the conditions of the payment. Now that we have the conditions settled, we need to.... Cat will open.. and pull the money from Bob. And now Bob can take this x0 that he knows and pull the money from Alice in this manner.

This NIZK ensures that Bob doesn't lose coins. Bob is convinced of the relationship between the values. Bob doesn't learn the information. He can't steal coins. Bob does not lose coins either. We can use a channel between them, like Sphinx, to do that communication.

## Concurrency in PCNs

Here we observe that concurrency on-chain transactions is somewhat easy to be solved. Miners have a view of all the transactions and they can take some of them and sort them or order them. No user has a complete view of off-chain payments. No user in the network has a complete view of all payments occurring in the network. No entity can look at all those transactions. So the approach is a blocking solution that can lead to deadlocks. As soon as they reach a channel with enough credit, that payment will... and then the payment... conditional payments will just timeout at this point. However, since a blocking solution can lead to deadlocks.... Here's an example. The red payment here, and Bob wants to pay to Edward for the sake of example, each channel might have the capacity for only one payment. Concurrent payments will be routed on different paths, and now the blue payment goes to Carol and she can't forward to Edward, and she had already used her coins for the red payment. So you can see how there is a deadlock here. Using a blocking solution, both payments get aborted because there's not enough credit, and both payments get released.

What we propose is a non-blocking solution called Rayo. The property we are after is that in a set of concurrent payments, we want to make sure that at least one of the payments finishes. We use global transaction identifiers. For every transaction there is an identifier tha tevery node in the network knows. In the previous example, the red transaction and blue transactions have identifiers. Every node can locally check and order the transactions. The policy we implement is that payments with a lower identifier will get aborted. Now the nodes will know which payment to abort to resolve the problem.

## Tradeoffs

The identifier might interfere with privacy of the payments. Is this a problem? Yes. In the paper, we show that it is impossible to have a non-blocking solution and a solution with full privacy. So there is a tradeoff here. The system we propose, we have to give up one of the two. Either you give up concurrency or you give up privacy.

## numbers

We have been prototyping our system. The running time is largely dominated by the NIZKs. The creation of a proof requires 309 ms. The verification of a proof requires 130 ms. The size of a proof that we need is about 1.65 megabytes. In order to do a realistic scenario, we wanted a payment with 5 hops. We have been testing with the non-rpviate version of the lightning network, where we measured it as taking 609 ms. In our privacy solution, it takes about 1929 ms and we need 5 megabytes of communication between the nodes.

The main point here is that ... we don't require etra information in transactions. These are data that are passed off-chain.

## Conclusions

In this work, we define security and privacy properties of interest in payment channel networks. There is an inherent tradeoff between concurrency and privacy. We have to loo kat that tradeoff and give up one of the two. There is Fulgor and Rayo which we have proposed. Two approaches for concurrency and privacy. Fulgor is blocking, but full privacy. Rayo is for concurrecy, but not private.

We showed our solutions are efficient, compatible with bitcoin script, and they don't require storage overhead in the blockchain.

Thank you for your attention happy to answer any questions.

## Q&A

Q: Lightning network uses onion routing. What is the threat model for...

A: I can't hear.

Q: ... Routing is set by the sender. So I'm wondering what is the supposed threat model here where privacy is leaked? The information is only shared with the participant of the route.

A: I was talking about man-in-the-middle attacks in the path. We use the same technique, we use onion routing to send these zero-knowledge proofs and these x values. The privacy thing here is that even if you are only sending information to users in the path... the conditional payment requrires the y value the same everywhere. Two users in the path... they can figure out they are part of the sam eptah.

Q: They can already do that by amount and timing.

A: That's true. ... We need to send these.. to hide the amount and hide the leak, yeah.

Q: When you're tlaking about the method of comunication from the sender to all the people that get the intermediate values, in Fulgor.. you said they can use the sphinx network?

A: In the paper, we ... routing mechanism in the sense that.. we assume every user in the path can.. every ... in the network. The sender can figure out the path. ... We can use any onion routing mechanism. Our techniques are basically ... the routing..

Q: .....

A: We looked at sphinx. Onion routing. Also another technique. ... Testing them. We propose a... necessity. Interesting problem. See the paper.

Got time for one more really fast question.

Q: Can you get the proof size down?

A: Ah definitely. We have talked with the authors. They are working on a better solution .We are looking at testing that. Their proofs are smaller now. With better implementations, we can go lower in proof size. One last thing, our implementation needs a non-interactive zero knowledge. If tomorrow there is a better solution with slower proofs but still has the same properties, we can still use it.








