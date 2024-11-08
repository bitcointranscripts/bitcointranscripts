---
title: 'OmniLedger: A Secure, Scale-Out, Decentralized Ledger via Sharding'
transcript_by: Bryan Bishop
speakers:
  - Eleftherios Kokoris-Kogias
---
paper: <https://eprint.iacr.org/2017/406.pdf>

<https://twitter.com/kanzure/status/1048733316839432192>

# Introduction

I am Lefteris. I am a 4th year PhD student. I am here to talk about omniledger. It's our architecture for a blockchain. It's not directly related to bitcoin because it's a different architecture. To begin, I would like to acknowledge my coauthors who collaborated on this project.

# Agenda

We are going to look at the motivation, describe omniledger, evaluate it, and then summarize.

# Scaling

Scaling is important. The ethereum network is getting jammed up because people are rushing to buy cartoon cats on its blockchain. We want a scale-out property in a distributed system. In bittorrent, if you have more nodes, then you can download more data per second. Scale-out is where the throughput increases linearly with the available resources.

# Scaling is not easy

We looked at prior distributed system scaling work. There is a tradeoff between decentralization, scale-out, and security. Elastico "A secure sharding protocol for open blockchains" was proposed. Another protocol was "RSCoin" presented in 2016 called RScoin which had scale-out and security but not decentralization. Another one was "ByzCoin" which had decentralization and security but not scale-out, published in "Enhancing bitcoin security and performance with strong consistency via collective signatures".

# Sharding

We want to parallelize transaction validation into different shards. Having two shards double the throughput. It's not as trivial as adding a second blockchain and therefore saying we have a single blockchain with double the throughput. How do validators choose which blockchain to work on? How can you pay between shards?

# Random validator assignment

For adequately large shard size, randomly assign validators can work. Otherwise, if the validators choose, all malicious validators can choose the same chain. In bitcoin, we don't know who the validators are. We use an idea from byzcoin for bootstrapping identities with PKI (public key infrastructure) for proof-of-work. Once there's a bunch of identities, we do a byzantine consensus classical method. We have microblocks.

# Strawman: SimpleLedger

Trusted randomness beacon emits random value, and validators use the randomness to compute shard assignment (ensuring shard security), and they process transactions using consensus within one shard (byzcoin). This is not good because the randomness beacon requires a trusted third-party, no transaction processing during validator re-assignment, and there's no support for transactions crossing between shards. Also, it has the failure modes of byzcoin and it has high storage and bootstrapping cost. There's also a throughput vs latency tradeoff that we can see in almost all our block syncs.

# Roadmap

First we used sharding via distributed randomness, we have multiple partitions, we introduced a protocol called atomix (for atomic cross-hard transactions and swaps), then we did byzcoinX for robust byzantine fault-tolerance consensus, we do shard ledger pruning, and then trust-but-verify validation with throughput/latency tradeoff.

# Shard validator assignment

We use two randomness protocols. One needs a trusted leader. See "Scalable bias-resistant distributed randomness" 2017. RandHound is a multi-party computation protocol. The basic idea is that given a leader, we can produce a fully-unbiasable unpredictable random number. The only thing the leader can do is isolate node participant. If the leader is honest, then the random numbers it produces are absolutely provably unbiasable.

# Atomix: atomic cross-shard transactions

We looked into distributed databases where you have this classic problems of multiple databases, you want to execute a single query, and you want to ask everyone whether the query can be executed. This is similar to atomic commit and two-phase commit. We have a coordinator who asks every server that has part of the database whether they can actually commit or abort. The server replies with yes I'm prepared to commit, or no something is wrong I'm aborting. The coordinator collects those messages and then says okay commit or they say some of you cannot commit so therefore you should rollback because the transaction is invalid.

We wanted to use this idea in our protocol, but the problem we had is that we can't have a coordinator because that could be malicious, and someone could say "abort" all the time. We had to go one layer higher. The basic idea is to use a two-phase commit not among the validators, but the shards as processes. The good thing is that we constructed this to be ... as a result, we have a bit of the self bone malicious also reply, and as a result, they are also not going to stop working forever. If this is true, then we can basically use the client as a coordinator who actually has incentives to run the protocol and he is going to basically request that has his inputs are those inputs available then he is going to get a reply saying they are available or not, and this reply has to be on the blockchain and be verifiable so that we can ensure everything happened correctly. Every shard is a lite client for every other shard so that we can validate proofs of inclusion or proofs of exclusion of the other shards. The client can give a rejection proof to other clients. We can get liveness even under failures.

# Trust-but-verify transaction validation

We want to decrease the latency, and there's a latency vs throughput tradeoff. We give the client the option of lowering his security in order to get higher throughput and lower latency. This is only an option for the client. It's like the first layer of validation in bitcoin.

We construct two kinds of shards, there are shards that are small and some are insecure.. the client contacts those shards and accesses those value. You can either say that's fine for me my transaction is not important, or wait for a second layer of shards, which is actually big and tends to be secure probabilistically.  Optimistically-validated blocks.. this means that they are going to ... any .. that happen during validation, on the order of something like 1 minute. They have 1 minute to attack the small shards; but how much damage can they do? The client might decide optimistic validation is good enough. Only the final block is actually appended... the small blocks are just there for the clients to use if they want to go more quickly.

# Evaluation

We get the scale-out property. On throughput, we looked at the regular omniledger and also trust-but-verify omniledger. These results are for 1800 validators. Transaction confirmation latency in seconds for regular and multi-level validation (table).

# Conclusion

Omniledger allows for secure scale-out distributed ledger framework. We have a few modules including atomix for cross-shard transactions, byzcoinx is a robust intra-shard BFT consensus algorithm which could be deployed without sharding. We can get visa-level throughput and beyond. The trust-but-verify validation has no latency vs throughput tradeoff.

<https://github.com/dedis>
