---
title: Incentivizing Payment Channel Watchtowers
transcript_by: Bryan Bishop
tags:
  - eltoo
  - watchtowers
speakers:
  - Zeta Avarikioti
---

<https://twitter.com/kanzure/status/1048767166823071746>

# Introduction

Hi. Good morning. I am Zeta. I am going to talk about how to incentivize payment channel watchtowers. This is joint work with my collaborators.

# Micropayment channels

There are many ways to construct channels such as lightning channels and duplex channels. There's hops, you can route payments, and other proposals more recent ones for doing channels in payment networks like sprites, eltoo, all of them although they are different they all share the fundamental nature of channels. Thus they share the same problems. One of the most important problems in channels is that they are not really secure. One party can cheat the other party if the other party is offline. The channel security depends on the ability of both parties to be online and constantly watching the blockchain.

# The problem

Suppose we have this payment channel and these are the update transactions. Suppose now that this party goes offline. In this transaction, this party has less money than in the previous one. He's incentivized to publish the previous state. Since the other party is not online to check, and if this happens for quite a while, then this is considered valid and will close the channel in a wrong state.

# Watchtowers

We wanted to solve this problem. We want back to how the channels work. The only people who know what's happening in the channel are the channel party participants. They are the only ones that know the transactions. A natural solution would be to introduce a third-party. This is what the watchtowers are. The watchtowers can be anyone- a friend of you, a payment service provider, or a trusted node on the network. The watchtower stays online and broadcasts a justice transaction or provides a proof of fraud and recover the funds in the event that the counterparty cheats. In lightning, there is a revocation transaction that the two parties agreed on before rolling the state forward.

# Original watchtowers

The original watchtower proposals were focused on privacy. It would help with outsourcing the watchtower. The original proposal used the txid of the justice transaction divided into two parts, and they took the first part as an identifier and gave it to the watchtower. The second part was used to encrypt the revocation transaction and they gave it to the watchtower. For each new transaction the watchtower was watching, they would need to store increasingly more data. The lookup time is high. There is no incentive for the watchtower to actually watch the channels because channels are supposed to have a long life, and fraud may not happen for long periods of time and they wont get rewards.

We would like to have a distributed protocol where anyone can act as a watchtower. But in original watchtowers, the channel parties had to go and pick a specific watchtower. We want a more modern solution for watchtowers.

# Free market

We supposed we could make a free market for watchtowers. We use the anyonecanspend method. Then we broadcast that to the entire network and if fraud happens, then someone will go and claim it becaus ethey have incentive to do so. This doesn't actually work, though. We looked at the properties for what we wanted- we wanted security for the channels, and we have to prove that the watchtowers have incentive to publish the proof of fraud. We also need incentives for propagation in the bitcoin network, and incentives for participating. We wanted to have low overhead, and also ideally if we could we would like to have some privacy. Our free market protocol only achieves security, but none of the other features. The watchtowers have incentive to publish a proof of fraud, but no incentive to publish the message to the network because he is giving it to his competitors. The overhead isn't that good, either. Also, this is centralized.

# Enforce who gets the reward by protocol design

The protocol we propose is as follows. There will be layers of watchtowers around each participant on the channel. The first phase is disclose and cascade. He sends the revocation transaction to all of his neighbors. He includes a new transaction that says from the output of the revocatoin transaction, you get to claim some percentage or some reward, after some number of blocks. In the next layer, it's done a similar way. So he propagates the same thing, the same revocation transaction, and then he says okay I will sign some new transaction and pay another watchtower, and this goes from layer to layer.

When fraud actually happens, it's a watch and commit protocol. The party publishes a previous state from the channel. The other party is not online to dispute it. After k blocks pass, which is the timelock on the first transaction, the first layer (the neihgborhood of the party) is given a chance to publish a proof-of-fraud on the blockchain. If that does not occur, then the second layer has a chance to do so.

To see if the protocol is secure (DCDW protocol), we look at the rewards. Are the rewards proportional to the amount locked on the channel? We want the reward to be high enough because this avoids the ... imagine you have a channel with 10 coins, and you give a reward of 1. If you have 10 watchtowers that have the reward, then they have no incentive to... because ... expected pay that is higher, the last one. The second part is the incentives- we need to prove that this protocol is incentive-compatible in the sense that the watchtowers will propagate the transactions. The reason this holds is the timelocks. Every layer gets its own chance to publish the proof-of-fraud. The expected payoff for propagation goes up. If this watchtower in this layer did not propagate the transaction then the probability he's offline at this period of time when fraud occurs, times hte reward, divided by the number of people that are in the same layer as that watchtower. If he propagates, then he gets an additional expected reward. If he's offline, and someone from another laye rand published it, and it came from his own path, then he gets a reward too. So everyone is incentivized to propagate. The overhead of the protocol is the same as the free market, but it doesn't improve on anything. The privacy at the moment--- we can fix this by using the original idea and at least obfuscate the balance in the channels. We can use the txid to hide and encrypt the revocation transaction. We're all more or less close to the direction we want and it has the properties. It doesn't require forks or changes in lightning nodes.

# More...

What about incentives for participation? Channels are supposed to have a long life. Watchtowers are supposed to watch channels because they get their reward. If the parties don't cheat, then the watchtowers don't make any money. We need to break the cycle somehow. We thought, well let's pay regularly to the watchtower with some premium. We can't guarantee they are doing their job, even if they are getting paid. So we need to check that they are doing their job that we are paying for. There are two directions we can go to see if we have cheating watchtowers; the first one is to employ punishment, and the second one is rewards. You could also sample the watchtowers and see if they return the data that you expect (even if they might not perform the other behaviors they promise). So you could put down a security deposit in case fraud happens; I think it works, but I don't like it very much. If you want to be a watchtower, then you need to put down collateral and this is only for wealthy people then. We want anyone on the network to be able to be a watchtower. So let's go with the give a dog a bone approach. It's a work in progress.

The main idea was to create the bone or incentive for the watchtower. Suppose you're participating in a channel and you want a network of watchtowers. You want to create frauds to pay the watchtower on a regular basis. You can create fake channels with yourself and at random intervals you can create fraud. If the watchtower is watching, he can claim the reward. If this happens regularly enough then the watchtower is getting paid. If he's not doing his job, then he's not penalized but he's not gaining anything. This seems like a good way to incentivize the payments.

There are other problems, like privacy, which has a tradeoff with efficiency. We would like to have lower overhead, lower lookup time and faster local storage. Watchtowers have to keep all the data for a long time. But if we could use the eltoo proposal or SIGHASH\_NOINPUT then this could be much easier and we could keep lower information per channel.

