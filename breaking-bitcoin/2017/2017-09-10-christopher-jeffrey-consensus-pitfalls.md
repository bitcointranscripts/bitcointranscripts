---
title: Pitfalls of Consensus Implementation
transcript_by: Michael Folkson
date: 2017-09-10
speakers:
  - Christopher Jeffrey
media: https://youtu.be/0WCaoGiAOHE?t=9000
---
## Intro

I’d like to talk about breaking Bitcoin today. Before I do that I’d like to give a short demonstration.

## Demo

Right now I am SSH’d into a server with a couple of nodes on it. I am going to start up a bitcoind node and I am going to connect to one of these nodes and have it serve me a chain. The chain is kind of big. I predownloaded a lot of it. It is a regtest chain that I mine myself. As you can see here is the debug log. I’ve already synced it up for the sake of convenience. I would like to show you what happens when I sync a chain with it. I am going to start up bitcoind now. It is syncing this chain. I think we have about 400 blocks to go so this shouldn’t take too long. It is going pretty fast, these are all 1 megabyte blocks. Kudos to Bitcoin Core for the benchmark times. When it gets up to something like 24,103 what I am going to do is switch over to this tab which is htop. It is going to show us what is going on memory wise with the bitcoind process. We’ve got about a hundred blocks to go. I tried to time this perfectly to pre-sync it but you never really know. We’ve sort of stopped there. If we look at htop you can see bitcoind at the top there. It is using a lot of CPU. Memory seems to be growing at a very high pace. If we look back at the log still nothing is happening. It looks like we are stuck on a block. This server has 12 gigabytes of memory. Right now we are using about 7 gigabytes. Can we go for 8? We are at 8 gigabytes. Almost 9. If we hit 12 what will probably happen is the kernel killer will kick in and just kill the bitcoind process. We are almost maxed out in memory. The server may become unresponsive for a bit. We are using all our memory and the process died. There is no more bitcoind process here.

`ps aux | grep bitcoind`

That was Bitcoin Core trying to process a single block in a regtest chain that I mined and it crashed on that block. I am going to explain to you why that happened.

## History of Forks

But first I’d like to go into some history about things like this. If we look at the history of forks, all the unintentional hard forks or potential hard forks in the past. In 2013 we had the LevelDB fork. The LevelDB fork was basically caused by Bitcoin Core 0.8 upgraded to using LevelDB instead of BerkeleyDB. What people didn’t know is that BerkeleyDB was inadvertently creating a new consensus rule, basically limiting the input count in blocks. For the longest time Bitcoin blocks weren’t that big. Around the same time Bitcoin Core upgraded to LevelDB so now we had a selection of BerkeleyDB nodes and LevelDB nodes. When people started mining bigger blocks the BerkeleyDB nodes could not handle it because it depended on a number of locks configured with BDB, a number of locks for reads. The reads for UTXOs in inputs ended up causing a fork. I’m sure a lot of you know the rest of that story. Then I guess it was a total of 6 years was BIP 66. BIP 66 was pitched as a malleability fix but it was really to prevent a potential hard fork in the protocol. It had to do with lib OpenSSL and the way it parsed DER formatted signatures. The way OpenSSL implemented it differed across architectures. That was a ticking time bomb at any point. There could have been a fork between 32 bit and 64 bit nodes. But what I’d like to point out here is these are both implementation details. LevelDB and BerkeleyDB or OpenSSL those are not required by the Bitcoin protocol, it is just how the programmers decided to implement Bitcoin. Bitcoin is just a protocol in the abstract. A theoretical implementation at the time could have chosen not to use BerkeleyDB and not to use OpenSSL. They would have implemented the consensus rules as they exist today.

## History of DoS vectors

Moving along from that we can look at the history of DoS vectors too. What I want to compare here is protocol bugs vs implementation bugs. You all know the quadratic sighashing (CPU) issue in Bitcoin. That is a protocol bug. It is actually required by the protocol. There is no good way to optimize it. Luckily now that SegWit is activated that is mitigated a lot because SegWit actually makes sighashing linear complexity instead of quadratic complexity. Then there is a number of other things. Satoshi originally implemented script numbers as bignums. He had a bunch of opcodes that are disabled now but a lot of them could allocate a bunch of memory like OP_CAT, OP_MUL, OP_DIV, division is slow, that could use a lot of CPU and so on (OP_LSHIFT, OP_RSHIFT). The other one was a more recent one that Sergio Lerner did a [write up](https://bitslog.com/2017/04/17/new-quadratic-delays-in-bitcoin-scripts/) on it. He noticed the quadratic complexity in `vfExec` which is the IF stack in the Bitcoin Core scripting system. And the implementation of OP_ROLL. The difference between this last one here, the `vfExec` and OP_ROLL is that it is actually an implementation detail. That is fixable without any changes to the consensus protocol.

## How to Break Bitcoin

If we want to break Bitcoin what do we do? We can look at all these past examples of how Bitcoin almost broke and maybe try to take the best properties of each. I think we should focus on machine details which were the cause of BIP 66 and the LevelDB fork. Focus on abusing everything: memory, CPU and disk I/O. And target consensus. If you wanted to do some kind of DoS attack on Bitcoin you could target the peer-to-peer layer. That would be pretty effective for breaking things. But the consensus layer is the scariest place to have some kind of DoS vector.

## UTXOs

I promised I would explain to you how I crashed Bitcoin Core in the beginning. I am going into detail about that now. We have to explain UTXOs, the UTXO set and how the UTXO set is implemented and how the data management actually works. UTXOs are the heart and soul of Bitcoin. At the end of the day the UTXOs are the end state of the blockchain and all that really matters. There are many ways to implement UTXOs. Satoshi originally implemented them as sort of a database index for flat files. What he would do is when a new transaction would come in on the blockchain he would take the output vector and then he would take the file number offset position, size, whatever and pack them into this other vector and serialize that as a record in the database. It was just a pointer to the actual data in a flat file. The important thing to remember about this is that because it was just a pointer, the database record was just a bunch of pointers, it had constant size of 12 bytes. Each member in this vector (vSpent) which was just a vector of pointers, it tracked spentness of outputs. That’s pretty small, 12 bytes. In Bitcoin Core v0.8 this code was completely rewritten for storage reasons. What it would do is it would now store UTXOs in the database itself. This was great because it reduced size a lot. Satoshi originally had a full transaction index. A lot of you might remember back in the day `getrawtransaction`, you could get any transaction. You can’t do that anymore because of this optimization that came out in Bitcoin Core v0.8. That seems like a decent idea. It seems pretty clever. There is a lot less space, there are a lot less keys in the database which is nice. A lot of databases have trouble handling lots of different keys. This seemed like a good idea at the time. It eventually became a popular model for doing UTXO data management. It was adopted by other Bitcoin implementations like Bcoin, btcd and Bitcoin.

## Indexing new UTXOs

This is basically how it works. When a new transaction comes in on the blockchain all of the outputs, the entire output vector is serialized and placed under a single record in the database. Say another transaction comes in that wants to redeem an output from that original incoming transaction, what it has to do is read that entire record for 1 input. We only need 1 output but instead it reads the entire output vector that is in that database record.

#Vector-based UTXOs

This is another visualization of it. We end up reading a lot of data we don’t need. We see Tx1 and Tx2 are funding transactions. We only need the second output from the first transaction and the first output from the second transaction because Tx3 is spending them. But we end up reading all the other outputs as well. The tricky part about this is that once we read them and we spend those outputs, when we are processing a block, now we need to take that output vector, remove the output that was spent and then reserialize the whole thing and write it back to the same record. That seems like an inefficiency.

## Implications

There are some important things here. Members of this new UTXO vector that is stored in the database are no longer constant size like they were with Satoshi’s code. They are no longer 12 bytes per member. (Each requires extra logic and CPU time spent on compression during serialization.) They can be variable size because they can be scripts and scripts can be variable size. The standard scripts are pretty well compressed but in theory you could have a lot of non-standard scripts that are really huge and you would end up reading those and reserializing them and writing them back as well.  (Variable size scripts must be read, pruned, reserialized and inserted to a cache which is eventually written to a LevelDB atomic write batch.) After one of these records is reserialized it is inserted into a cache and that cache is eventually flushed with a LevelDB atomic write batch. The tricky thing about LevelDB atomic write batches is they actually must be stored in memory in their entirety until a write is completed. Whatever UTXO vectors you read into memory when you are processing a block, they actually have to be held into memory until that block is finished processing for the writes to be atomic.

## The Problem

I went over a lot of this slide already. All of this is a problem. We are reading these UTXO vectors, we only need one output but we are getting all these sibling outputs too. In retrospect it seems like a pretty inefficient idea even though it seemed nice at the time.

(For each input being spent in a block, an entire UTXO vector must be read, which encompasses the referenced output as well as all of its sibling outputs. Once this vector is read, the output must be pruned, and all of the sibling outputs must be reserialized and written back. Due to the way LevelDB write batches work, all UTXO vectors being redeemed by a block must be held in memory until block processing has completed.)

## Exploiting the problem (in theory)

So how can we exploit this? How can we break Bitcoin? I can’t remember what got me thinking about this, I think it was the talk of all the forks going on at the time and changes to consensus rules, all the drama. I was thinking about different DoS vectors that you could do if there were different consensus rules. I started thinking about places I would attack if I were an attacker. After this talk I hope I’m not perceived an attacker. The basic idea would be you create as many funding transactions as possible. Due to the block size limit the max amount of P2SH outputs you can have in a block is about 31,000 due to the 1 megabyte limit. We want to use P2SH outputs because we can’t really use non-standard outputs because they won’t get mined. Let’s just keep it simple and use anyone-can-spend P2SH outputs. Redeeming these outputs is pretty simple. We provide an OP_TRUE and an empty redeem script for the input. The max number of inputs we can have for a block redeeming all of these outputs is about 24,000. If we create our final attack block using this idea and we redeem one output from each one of the transactions we created. All of these giant UTXO vectors get loaded into memory for every single input. It results in about 24 gigabytes of data read into memory and reserialized and written back. And it needs to be held in a LevelDB write batch so there is no way to incrementally free it up. It actually needs to be there in memory. It is also important to note, it only seems like 24 gigabytes on its face, in reality due to the way C++ heap operates and due to all the intermediate logic that’s happening when a block processing occurs, the memory usage is actually amplified 3 to 4 times. It is probably not 64 gigabytes actually, it is probably more like 100 gigabytes. This was the attack that I showed you in the beginning. It is sort of unrealistic. It is sort of far fetched. We have to mine a bunch of 1 megabyte transactions. First of all you have to be a miner to do that. Secondly, of course someone is going to notice 24,000 blocks that only have a 1 megabyte transaction in them. It would be obvious if some kind of attack like this was happening. You need to be miner or know a miner to pull it off.

1) Create as many funding transactions as possible. Due to the block size limit, the max P2SH outputs a single transaction can have is around 31,000 (1MB of data)

2) The max inputs for a block redeeming anyone-can-spend P2SH outputs is around 24,000

3) Our final attack block will redeem one output from each of our 24,000 transactions

4) Each transaction output vector is roughly 1MB in size, this results in 24 gigabytes of data being read, mutated, reserialized and written back to the database.

## Exploiting the problem (in practice)

So let’s think about how we can exploit this problem in practice. There is a policy version of the attack which does not require the participation of a miner. The main differences are you have to abide my policy rules. You have to make sure that your transactions are 100 kilobytes or less. That means these UTXO vectors that we read into memory can only be 100 kilobytes per input. That makes it about a tenth as bad as the actual miner attack. It is like 2.4 gigabytes read instead of 24. Again that is also amplified because of all the intermediate logic, the C++ heap and whatever. That would probably be about 10 gigabytes read. The other difference is instead of spending money running a mining farm, the bottleneck for an attacker now becomes transaction fees. To mine the number of transactions you would need, you would need to fill up several blocks with your own transactions. If you look at the total block fees that is a huge amount of Bitcoin. That would be many millions of dollars USD. But the nice thing about this version of the attack is that it is less noticeable. Not as many people are going to notice a 100 kilobyte transaction every block.

(A “policy version” of this attack does not require the participation of a miner. Abiding by policy rules results in an attack that is only 1/10th as deadly as the theoretical “miner version” of the attack. This is due to the policy rule which limits transactions to 100KB in size (2.4GB read instead of 24GB). Instead of spending massive amounts of money on mining hardware, massive amounts of money must instead be spent on transaction fees (several millions in USD). The setup for the attack is now less noticeable)

## Why this works

When I started thinking about this more and I started testing it more I kept second guessing myself. Oh no this wouldn’t work because we can’t make the final attack block because of policy rules or mempools would have trouble accepting it or miners would re-org it out because it takes so long to process. The more I thought about it the more I realized that these aren’t actually potential problems for the attack. Unlike the sighash attack the final attack block does not need to be a single transaction. With the sighash attack the attack block has to be a 1 megabyte transaction if you want to make it as deadly as possible. But with this attack it can actually be split into many transactions which means that you don’t need a miner to do it. In fact it could just be a bunch of 200 byte transactions so that’s not really a big deal. But what about mempools? Would mempools reject these attack or pre-attack transactions? Actually probably not because when transactions enter the mempool they do read all of the UTXO records that use up a lot of memory, but they don’t have to prune these UTXOs and they don’t have to put them in an atomic write batch. Transactions enter incrementally so they don’t have to process all of these transactions all at once. It is a lot less load on the node. I think most nodes could probably handle this. The other point is why wouldn’t miners, these blocks would probably take so long to process or they would crash mining nodes, there is no way a miner would mine on top of an attack block like this. Well it turns out miners have pretty beefy servers. They can handle using 10 gigabytes of memory no problem. But most of the network, a lot of the network probably doesn’t have 10 gigabytes of memory to spare. It seems like this attack might actually work. The scariest part is that once you have all the setup transactions this attack is basically free. You have very little diminishing returns because you can keep redeeming outputs from the same transaction. You can do this with very little effort. The setup phase is what is expensive to miners or a non-miner.

## Fixing the Problem

Luckily because this is an implementation detail and not a protocol bug like sighashing is there is an easy fix. We don’t have to fix consensus. Bitcoin Core actually implemented this. sipa inadvertently fixed this problem with his per-tx branch of Bitcoin Core that was merged into master a little while ago. What it does is instead of storing outputs in their own vectors in serialized database records what they do is each output gets its own record in the database. It is much simpler. Now instead of reading a whole record by transaction ID, getting a bunch of outputs and then pulling out the output at a certain index, we can just look up an outpoint and grab the output data directly. This is nice because now we don’t have to reserialize a bunch of data and write it all back. That seems to work well.

## Storing per output

This is what is looks like. You remember before we were reading all these other outputs for no reason but here we can just directly pull the outputs themselves out the database to redeem the inputs. This was implemented in Bitcoin Core for performance reasons but it actually ended up inadvertently solving this attack which is pretty cool.

## Fixes

So like I said there were many alternative implementations of Bitcoin that adopted the Bitcoin Core 0.8 vector based model. Luckily this is fixed in Bitcoin Core 0.15. Bcoin 0.15 and Bitcoin ABC 0.15, they are all 15 for some reason which is kind of creepy. The btc1 and btcd developers have also been informed of this and are hopefully deploying a fix soon. But the interesting thing is, like I said this is not a protocol bug, there are implementations that are completely unaffected because they decided to implement UTXOs in a different way. Those implementations are Libbitcoin, BitcoinJ and Parity Bitcoin. There may be some other ones that I didn’t actually see.

## Brick your full node (proof of concept)

So if any of you want to brick your full node I’ve set up a server with two nodes on it. Just point your Bitcoin Core 0.14.2 at it. The first version is the miner attack which is pretty big, it is like 24 gigabyte blockchain. That will almost guarantee to invoke the OOM killer for your operating system. The non-miner version, it seems to use about 8,9 gigabytes in Bitcoin Core when it is processing the attack block. It does successfully process it but it takes several minutes like 2 or 3 minutes. That is from my own experimentation on a I7 64 bit with a decent chunk of RAM. If you want to invoke your OOM killer you can run a single command and the OOM killer will kill Bitcoin Core. By the way these actually have hard checkpoints so don’t try to reorg my regtest nodes please.

`bitcoind -regtest -connect=insert_IP_address`

## Conclusions (specifically my own conclusions)

Here are my biased conclusions on this issue. I’ll have to respectfully disagree with Eric Lombrozo on this. A more diverse range of Bitcoin implementations would have prevented this as a threat entirely. It would have mitigated this greatly if we didn’t have a single Bitcoin implementation with 99 percent market share. If there is some kind of fault like this that is implemented in the implementation that everybody is using the entire network goes down. For example, if there was a higher percentage of market share for libbitcoin or BitcoinJ it still would have been a problem because presumably Bitcoin Core still has a significant chunk of market share but it would have been less of a problem if you had a lot of users and miners running different implementations. I guess the final point I’d like to leave you with is that development and implementation centralization are a big threat to Bitcoin. I think more people should be talking about it because here most of the talk just seems to be about miner centralization.

## Q&A

Q - My understanding is that 0.15 is not out yet in terms of the fix. It is not fully out, people haven’t upgraded yet. Do you think it is ok to talk about this before we’ve had a release where it is fixed?

A - That’s only one implementation of Bitcoin. There are several other implementations that don’t have…

Q - But this is the one that most people are using.

A - It is one implementation of Bitcoin. This is a decentralized protocol and it is just a protocol. It is not an implementation. Anyone can implement it. You all are using different implementations, that is what we do in decentralized protocols I hope. I’d also like to say that this is a theoretical attack. It would be very difficult to pull off in practice. It would take several months to set up and cost several millions of dollars.

Q - Do you think what Satoshi said about different implementations is not applicable anymore? Something changed in the ecosystem or you think it is still valid that different implementations are more of a risk than a help?

A - I think what Satoshi was talking about was that there are a risk in different ways. They are a risk in terms of consensus faults, not reimplementing consensus correctly. But they can be very beneficial in a case like this where there could be some kind of attack that doesn’t necessarily pertain to a consensus difference.  I understand where Satoshi was coming from with that and where a lot of people come from with that. But I see different Bitcoin implementations has having a lot of benefits.

Q - How much worse is this on Bitcoin Cash? You have 8 megabytes of room to play with all this.

A - It would be a lot more severe on Bitcoin Cash. I disclosed this attack to sipa several months ago and he was made aware of it. It was already merged in to master. sipa came up with the per-txout code and fixed this inadvertently with that. I also informed Bitcoin Cash of this vulnerability recently. They shipped a new version which does implement per-txout. As long as people are using the latest version of Bitcoin-ABC it shouldn’t be an issue.

Q - Who did you inform about this?

A - sipa

Q - Who else?

A - I informed sipa, Jeff Garzik, Laolu for btcd and Amaury.

Q - Did you ask any of those people before you announced it? Before people actually released their code?

A - I gave them several months heads up.

Q - Obviously this is a structural with the database. Did you ask them? That you planned to announce this?

A - I did mention that to sipa that I would like to do a full write up. We agreed we should keep this on the DL for now. Now the Bitcoin Core release candidate…

Q - Did you tell anyone that you’d be announcing it in public? Did you give them a date? People who are implementing fixes. Standard responsible disclosure.

A - Yeah I did.

Q - Did you inform people that you were going to make the announcement on this date? Did you ever try to get feedback on that? Specifically you told people you would be making this presentation? Did you say that you’d do it this date? Did you say you’d do it eventually?

A - First of all I preferred to give the longest amount of time I could. I mentioned that I would be disclosing an attack but I didn’t mention the exact details. It is a pretty severe attack but hypothetical.

Q - For starters you don’t necessarily know that. Bitcoin Cash is a good example.

A - This attack has never been executed before. It is purely theoretical.

Q - As an example people have been doing spam attacks. There may be entities that do actually have a pile of 100k transactions sitting around.

A - It is possible.

Q - I wouldn’t say it is that theoretical. And yet you are disclosing it without telling people you are going to disclose it and getting any feedback on that. You’re not following any of the standard responsible disclosure procedures that are standard in industry.

A - I disclosed this to several maintainers of different Bitcoin implementations. They are in the process of deploying fixes. This conference is called Breaking Bitcoin.

