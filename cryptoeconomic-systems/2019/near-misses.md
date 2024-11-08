---
title: Near Misses
transcript_by: Bryan Bishop
tags:
  - security
  - research
speakers:
  - Ethan Heilman
---
Near misses: What could have gone wrong

# Introduction

Thank you. I am Ethan Heilman. I am a research whose has done a bunch of work in security of cryptocurrencies. I am also CTO of Arwen which does secure atomic swaps. I am a little sick today so please excuse my coughing, wheezing and drinking lots of water.

# Bitcoin scary stories

The general outline of this talk is going to be "scary stories in bitcoin". Bitcoin has a long history and many of these lessons are applicable to other cryptocurrencies. Many of these problems were found a long time ago. I think bitcoin has done enormous amounts of work making itself more secure. All the vulnerabilities discussed in this talk have been patched in Bitcoin Core and they are all publicly known. I have not tested them at all, I am just relying on the public vulnerability reports and published research reports and somewhat careful reading of the source code.

I am going to tell several bitcoin scary stories today. The first one is going to be about a network-wide memory exhaustion attack which is something I personally interfaced with. The second one, I'll go through several bitcoin vulnerabilities many from the early days of bitcoin to look at them to get flavor and pry people's imaginations for what these vulnerabilities look like. Finally as a thought experiment I am going to think about what a worst-case exploit in bitcoin would look like.

# Why tell scary stories

Well, to understand the past and use that understanding and to adapt and think about how we can mitigate some of these issues, but also as a way to generate scenarios. If we're thinking about what can go wrong in bitcoin in 10 years, then let's look back at the last 10 years in bitcoin which can provide a starting place for things that could go wrong.

Solutions are the motivation for this talk, but I won't be talking about that. Just talking about some things that happened. It has a series of questions though.

# Network-wide memory exhaustion attack

I was doing an experiment on bitcoin's p2p network and my advisor chair said I need to be really careful because software and network systems are really fragile. If you're sending packets and so on to the production network, you need to be careful. I didn't take the warning seriously. I figured I shouldn't take precautions. Later, I figured out that I was close to triggering a DoS vulnerability in bitcoin. The vulnerability was patched a few months earlier; if I hadn't taken the precautions and they hadn't patched it recently, then I would have triggered it.

I had some attack code that was sending header messages, which are packets of IP addresses, to a bitcoin node. As a property of the bitcoin p2p protocol, these ADDR messages are repeated to other bitcoin nodes. This was the experiment that I almost did. The precaution I took was adding a shim inside the bitcoin node and only used particular IP address ranges and I prevented those particular IP address ranges from being re-transmitted to the network.

Later, I came across the paper "Deanonymization of clients in bitcoin p2p network". If you read the appendix, it scared me quite a bit because it describes an attack where if you send lots of ADDR messages like I was sending, then they would just be stored in RAM and they would grow without bound and then crash the node. This is what the vulnerability looks like-- they had a set that stored the known addresses, and whenever you got an ADDR message, you grow the set. It grows without bound, you run out of RAM and then you crash.

Even worse, each time a node receives an ADDR message, if it contains 10 or less addresses, then it sends it to 2 other nodes. So this is viral and it keeps going. So this is really bad because with a small amount of traffic you can cause a very big problem. Even if you stop the attack, as nodes crash and come back online, they forget which messages they have sent to other nodes and they continue to do the attack. So the attack has a self-sustaining property.

If this had been exploited, how bad would it have been bad? I think it wouldn't be that bad; I think you patch nodes, and the unpatched nodes would crash and not come back up. But I'm not aware of anything like this having been exploited in practice on any cryptocurrency. Maybe someone in the audience has an example like this.

But what about something like this where all the nodes are retransmitting the same message to everyone, even after the attack stops, what's the right action to take?

This was fixed in 2014. Here's the fix. There's the set, and the set is now limited to 500 addresses, and when you get a new address you kick out the old address. It's a most recently used set.

# Bitcoin CVEs

CVEs are a system for registering vulnerabilities. You can assign a unique ID to a vulnerability. When you talk about a CVE number, everyone knows which one you're talking about. It stands for Common Vulnerabilities and Exposures. The bitcoin wiki has a list of these CVEs and also additional vulnerabilities that have not been given CVE numbers. As far as I know, this is not a complete list. But the vulnerability I just described, I wasn't able to find it on there, maybe it was named something obscure. It's fun to go to the bitcoin wiki and just read about all the bitcoin CVEs.

The four CVEs that I will be talking about most of them are in the beginning, 2010, 2010, 2012, and then I will briefly talk about the 2018 CVE.

# CVE-2010-5137: OP\_LSHIFT crash

Cory alluded to this one. This is the OP\_LSHIFT crash. Bitcoin has a scripting language. One of the original instructions that you could run in the scripting language was OP\_LSHIFT which would shift a number a certain number of places to the left. It was discovered that when using OP\_LSHIFT on some machines, processing the transaction would cause the machine to crash.

So this is actually the code. I think this is an interesting exercise, but for the people familiar with C++, we often think that if you point out exactly where the problem is, you should be able to find it. I've only spent an hour or so looking at this, but it's not clear to me that in this OP\_LSHIFT case why does that cause a crash? I have a theory. If we have time, I'll throw up a slide about this.

Just as a general way to think about how hard these bugs are to find--- there's nothing that jumps out at you that this code is wrong.

The way that ythis would work is that yo uwould make an evil transaction and send it to a bitcoin node, and then the bitcoin node would crash. The CVE says that it only crashed some nodes. I think this might be worse than having 100% crashes. Think in your head about how you would go about solving this. Say you solve it by making OP\_LSHIFT no longer crash machines. So 40% of the network upgrades so that they don't crash when they see OP\_LSHIFT -- which means the evil transaction gets included in the block. Now the people who haven't upgraded, when they see these blocks they would crash. This seems kind of bad, and it would cause a hard-fork or a bit of a fork.

They actually fixed it in a slightly different way. I'm not saying they fixed it in this other way for that reason, but they did fix it differently. They had a bunch of opcodes causing trouble, and if you use any of them then your transaction is invalid, the script just returns false. If you're vulnerable to this, you crash, and if you're not, you drop the transaction and you don't re-transmit it so that you don't crash nodes.

I haven't been able to find discussion about why it was fixed this way; the obvious fix may not have been as good as the way they did fix it. It's an interesting case study.

# CVE-2010-5139: Inflation bug

This was a bug that allowed you to print more money. The code that was problem was about adding up all the outputs and all the inputs in the bitcoin transaction, you subtract all the inputs from the outputs, and if you got a negative number then that meant your outputs were greater than your inputs and that's bad and then it would fail which is what we see there. So it turned out that there was an overflow bug, as someone pointed out, they saw this transaction in a block and they said hey is that close to the maximum 64 bit unsigned integer and it was if you added up the two gigantic outputs for billions of bitcoin you actually get -0.1 BTC. So this allowed you to print money, and this was exploited on mainnet. Someone posted this transaction, and even worse some people mined on top of these blocks. Billions of BTC were produced.

So how do you fix this problem? Well, what everyone did is they patched their bitcoin software to make it so that you couldn't print money and then they started mining forking from the original attack point. So even the nodes that weren't patched, eventually would accept this new chain. Because the majority of the mining power was on this new chain and the new chain had fixed the bug, it got orphaned out and the bug got solved.

I think this is an interesting case study because pretty much everyone would agree that increasing bitcoin's supply by 200 billion BTC was a bad thing, so everyone wanted to work together to work. It's an inflation bug that violates the core principles of bitcoin, and because it effected everyone, they all had incentive to come together and fix it. So at least as I understand it, this was not particularly destructive. But this was also the early days of bitcoin. There was only one other transaction in the block where this was mined.

# CVE-2012-2459: Netsplit

The next one is CVE-2012-2459 from 2012. So a bit more mature code base for bitcoin, it's been around for like 3 years at this point. CVE-2012-2459 exploits the fact that you can have two blocks with a different meaning with different transactions in it that hash to the same value. It doesn't mean the hash value is broken, it means that the way you represent the blocks when you go to hash them, they collide, and because they collide you get the same value even though the blocks are different themselves.

So the way this worked in CVE-2012-2459 is that you had two blocks-- the second one would be invalid-- when you go to hash the transactions for the merkle root, bitcoin had a rule that you would pad it out and so the way the padding would work is you repeat the last transaction until the end. So the first block's padding results in the same bytes as the second block (which was invalid).

When the first bitcoin node sends the first (valid) block to the second node, the other node says this is a valid block and that's fine. When the other node sends another block with the wrong transactions, it's double spending with the same transaction, that's totally invalid and I'm going to reject. If one node sees one of the other blocks first, it hashes it and determines it's a bad block, he knows that if the hash is the wrong block then seeing another block with the same hash in the future it will say well I already know this hash corresponds to something invalid. So what ends up happening is that the parts of the network that see block 2 first conclude that the block is invalid, and this causes a fork in the network.

I sort of wonder what would happen today if something like this were to occur. It's not that the blocks are different; the blockhashes are still the same, but some of these nodes are dropping the first block on the floor and some of them aren't.

The way in which this was fixed was to say hey, if a transaction repeats in a block, then don't cache that result as a bad result. Just reject that block and don't re-transmit it.

# CVE-2018-17144: DoS + inflation

The final CVE I am going to discuss today was discovered last year. It was a recent one. There are some details which this picture is sort of hiding. Essentially what happened was that a check was removed, and without this check, under very specific circumstances, it was possible for a transaction to have more than one input spending the same output. There were a number of rules and conditions to be met to bypass the checks against this. There were circumstances where this could occur, and a transaction would be able to inflate the supply of coins.

This was not exploited in the wild, but it did exist in the Bitcoin Core codebase. It didn't exist in older versions; this check was removed as an unnecessary check that had a high performance cost. I guess I wonder like, would the reaction to this have been the same in 2010 when people were like well this got exploited and someone printed 150 billion BTC, if bitcoin is going to have value we have to fork this out. How many-- the original attacker, in the earlier CVE, was kind of the exploit required them to be greedy and produce billion of BTC. But what if the attacker only produces 1 BTC with it? How does the incentive to work together change if someone can now double spend thousands of BTC at an exchange, but the attacker only printed one bitcoin. Are we willing to live with that? What's the right solution to this?

# Imagining a worst case non-cryptologic exploit

What would be the worst case non-cryptography exploit in bitcoin? Well, bitcoin relies on its underlying cryptography so an attacker that can forge ECDSA signatures instantly in zero time or could break sha256 preimages is really bad. But these breaks in cryptography is pretty rare, and usually you see a series of attacks and you can see an algorithm getting less secure over time and you can adapt your system.

However, software vulnerabilities are relatively common. What's the worst software vulnerability we can imagine? I came up with an answer when I thought about it; I'm not saying this is the right answer. But just to think about what could go wrong, maybe come up with things worse. Maybe you think mine isn't that bad.

What I came up with was a valid transaction which when evaluated by a bitcoin node causes that node to execute a program written by that attacker. This is usually called arbitrary code execution or remote code execution. People used to call these network worms.

Attacks that keep the blockchain valid are quite worse because you can't rally people to come together. You could distort what the node tells the user about the blockchain. You could perform an attack where transactions are being sent, and they just don't see those transactions. You could make invalid transactions appear valid and confirm. You go to an exchange and you send them a bunch of bitcoin, and the exchange sees it as a valid transaction but maybe it never gets confirmed in the chain. You could also do things like leak keys, compromise random number generation, replace pubkeys, etc. You could have transactions that specifically cause speculative execution side effects, too.

I don't think this is likely to ever happen. It would need to work on different versions of Bitcoin Core and on different architectures. And conceivably, the evil code might be able to patch the code so that it's an invalid transaction but now Bitcoin Core treats it as a valid transaction and sends it out to other nodes as if it were. I'm not aware of any vulnerabilities in bitcoin that allowed arbitrary code execution. So I think it's an unlikely threat, but it's the worst case I could come up with. You could probably come up with something much worse.

# Open questions

What would happen if an inflation bug was exploited in bitcoin in 2019?

Which bugs in this talk were the most dangerous- net splits, inflation, which ones?

What countermeasures can we take to reduce the risk and the impact of a serious bitcoin software vulnerability exploited in the wild?

An exploit that hits only some of the nodes is much worse than an attack that hits all the nodes.

