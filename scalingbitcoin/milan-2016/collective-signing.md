---
title: Enhancing Bitcoin Security and Performance with Strong Consistency via Collective Signing
transcript_by: Bryan Bishop
tags:
  - research
  - cryptography
speakers:
  - Eleftherios Kokoris-Kogias
---
<https://twitter.com/kanzure/status/785102844839985153>

We are starting the session called "breaking the chain". We will first have collective signing presentation. Thank you.

This is joint work with some collaborators.

What we have now is that real-time verification is not safe. What we managed to get is that we get transaction commitment in about 20-90 seconds at close to 1,000 transactions/second. In byzcoin, irrevocable transaction commitment in 20-90 second. Throughput up to 974 transactions per second.

We change to the practical byzantine fault tolerance protocol. We use collective signing to scale to thousands of nodes and decrease latency. We scale PBFT to thousands of nodes. We use PoW to create hybrid model. Bitcoin-NG.

We will identify the problems with bitcoin, then change consensus and propose PBFTcoin. From MACs to collective signing. Decoupling transaction verification from leader election. Performance evaluation for scalability.

So this is a blockchain. We know this structure. We can add forks because this is bad because ... persist... one more blocks being mined on top. For .. inside the blockchain.. say it is in there. But again, we can add layers. This is just going to remove the two last blocks. If this is so, we can double spend and so on.

## Problem statement

In bitcoin there is no verifiable commitment of the system that a block will persist. Clients rely on probabilities. We're going to change this and make a strawman design for PBFTcoin.

## Strawman design: PBFTcoin

.. then there is a commitment by the supermajority that this will be there forever. Non-probabilistic strong consistency. No forks/inconsistencies.

Problem: needs a static consensus group. We can't just implement this on top of bitcoin and have a party. The other problem is scalability. The communication that previously used is very dense and this limits the consensus group size. Secondly, because of high verification cost because every client will have to verify his individual commitment of his participation in the consensus, it's tough for mobile devices. Because this uses matrix multiplication it means that every client must have a pre-defined secret... so if you have 100,000 clients this scales very badly because of all the shared secrets.

## Opening the consensus group

We're going to use proof-of-work to protect against sybil attacks. One share per block. Not every miner has the same hash power. So the miners have a percentage of shares proportional to hashpower. Finally, we're using a window mechanism to allow for enough miners and protect against inactive miners.

## From MACs to collective signing

We need to move from matrix multiplication. We need to use signatures. We can substitute MAC-based authentication (symmetric crypto) with public-key cryptography using ECDSA which provides more efficiency. This makes it third-party verifiable. We can just get a block and look at the signatures and verif against the public keys of the miners. This can be done with the PKI of the public blockchain already. PoW blockchain as PKI. We can be sure that the key inside the block would have presented of the miner that actually created that block.

This also enables sparser communication pattersn such as ring or star patterns.

However, we want to do better than that approach. For this reason we have to answer two questions. Can we get better communication patterns? Multicast protocols transmit information in sublinear steps. Use trees. Also, can we allow lightweight verification? Schnorr multisignatures could be verified in constant time no matter how many signers are signing the block.

Schnorr multisignatures plus communication trees == collective signing paper.

## CoSi

An implementation was made already.

<https://github.com/dedis/cosi>

For Ed25519 curve, 82 bytes instead of 9 KB for 144 co-signers. And for 190 bytes instead of 63 KB for 1008 co-signers.

CoSi is not a BFT protocol. PBFT can be implemented over two subsequent CoSi rounds, used as a primitive in both a prepare round and a commit round. We presented this at USENIX conference. This gives a verifiable commitment from the system that a block will persist. Throughput of this system is limited by forks. Increasing block size increases fork probability. It's limited by forks. We can't get verify frequency because they have decreasing security. Liveness exacerbation...

## Bitcoin-NG

Makes the observation that block mining implements two distinct functionalities. Transaction verification and leader election. Once a miner mines the blocks, he gets the right to verify transactions. We enhance bitcoin-ng with byzantine consensus and our PBFT protocol. We have no double-spending. We have non-probabilistic security. And also we have leaders who cannot misbehave.

## Decoupling transaction verification from leader election

Key blocks: PoW block and share value. Leader election. Microblocks: validating client transations and issued by the leader. Microblocks do not verify work, they have a load factor, only created by the leader.

## Performance evaluation

We evaluated on DeterLab network testbed. We simulated up to 1,008 miners multiplexed on top of 36 machines. Impose 200 ms on....

What size consensus groups can byzcoin scale to?

What transaction throughput can this system handle?

In order to compare our system with others, we implemented a byzcoin with... we each it implemented without collective signing too. Flat/MAC PBFT scales up to 100 miners. Tree/individual and tree/CoSi byzcoin scales up to about 1000 miners much better.

On the throughput side, as you can see, even with the 1 megabyte block that bitcoin has, ... so we get throughput of around ... while if we use the 3, we can get a high of around a fifth of a 100 megabyte block; if we increase the block, we suffer a bit the latency, but for a 32 megabyte block we get 1000 transactions/second whereas the latest for creating and sending this block is about 90 seconds and less than 1 hour.

## Ongoing work

What about an attacker with more than 1/3 of the shares? Switch to probabilistic consensus perhaps? Can currently only scale-up not scale-out... the performance deteriorates, and this is the problem with every block signing protocols. Also another small problem is that leaders are incentivized to exclude miners from consensus. Perhaps donate bitcoin instead?

## FAQ

What happens when an attacker gets more than 1/3rd of the shares.

Does selfish mining occur in the key-block chain? If you can have it in there, then they can get more blocks inside there which means more shares there.

Also, how is the consensus group size selected? Is it 100 nodes, 2000 nodes, how many shares is a good group have?

And finally, how do the miners make money?

## Surviving 34% attacks

We're going to attack this. Key-blocks keep being collectively signed with a needed margin of 51%. This is already better than bitcoin. Whoever verifies the blocks will use consistency- and after... is it going to be enough like in... the strong consistency is not immediate. Blocks will commit after 6 confirmations. Window starts from the last committed block. Micro-blocks forfeit liveliness.

## Defending against selfish mining

The PoW chain is (almost) fair even under 34% attacks. He wont be able to find a signature-- when he tries to play a new block, he needs to have a previous block, but it can only be cast when the collective signatures are pending. So he better just release it because he has not gained there.

## Choosing window size

Random sampling experiment. Probability that the system picks less than c = w/3. As you can see, P>0.99.

p|w, 12, 100, 144, 288, 1008, 2016
0.5, 0.842, 0.972, 0.990, 0.999, 0.999, 1.000
0.30, 0.723, 0.779,,,,,

## How do miners make money?

Why do the miners pick blocks? Why sign blocks? Why not mine for another? Why participate? They mine blocks and they get consensus group shares. They get money by participating in consensus. The coinbase outputs are distributed equally to the consensus group participates. The miner is incentivized to stay alive because he profits more if he stays alive for the full window. The more shares he has in the window, the higher percentage of fees and mining he makes when he signs the block.

## Future work

We also want to look into alternatives to Proof-of-Work like Proof-of-Stake. It might be interesting to prevent PoS problems. We also want to look to sharding. We also want to look at incremental deployment to existing cryptocurrencies. How are we going to model the system on bitcoi's adversary? Analysis of the blockchain protocol in asynchronous networks (Pass, Seeman, Shelat). How do minres discover each other?

## Summary

We use collective signing for BFT protocols. We use PoW to create hybrid permissionless BFT. We combine the above with bitcoin-ng to also increase throughput. We demonstrate that it's practical and that it could be deployed. For example, for 1 megabyte blocks we can commit the transactions in 24 seconds and get about 150 transactions/sec throughput. For 32 megabyte blocks, we commit transactions in 90 seconds and get 1000 transactions/sec throughput. Because of the strong consistency we can increase the throughput of bitcoin.

## Q&A

Q: How would you go about improving the security of bitcoin's existing consensus system using your ideas?

A: We would add an optional collective signatures so that if miners agree and maybe 80% perhaps, then the client would know that these transactions are going to stay there after 1 confirmation instead of 6 confirmations.

## References

paper <https://arxiv.org/pdf/1602.06997v3>

